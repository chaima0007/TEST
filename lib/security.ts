/**
 * Security utilities — SIEM-grade helpers for intrusion detection and
 * security monitoring.  All security events are written to stderr so they
 * are captured by external log-aggregation / SIEM systems (e.g. Datadog,
 * Splunk, Elastic) without being mixed with normal application output.
 */

// ---------------------------------------------------------------------------
// Rate Limiter (in-memory, IP-based)
// ---------------------------------------------------------------------------

interface RateLimitEntry {
  count: number;
  windowStart: number;
}

export interface RateLimiter {
  /** Returns true when the IP is within the allowed rate, false when blocked. */
  check(ip: string): { allowed: boolean; retryAfterSeconds: number };
  /** Resets the counter for an IP (e.g. on successful authentication). */
  reset(ip: string): void;
}

/**
 * Creates a sliding-window in-memory rate limiter.
 *
 * @param maxAttempts  Maximum number of requests allowed in the window.
 * @param windowMs     Window duration in milliseconds.
 */
export function createRateLimiter(
  maxAttempts: number,
  windowMs: number
): RateLimiter {
  const store = new Map<string, RateLimitEntry>();

  return {
    check(ip: string) {
      const now = Date.now();
      const entry = store.get(ip);

      if (!entry || now - entry.windowStart > windowMs) {
        store.set(ip, { count: 1, windowStart: now });
        return { allowed: true, retryAfterSeconds: 0 };
      }

      if (entry.count >= maxAttempts) {
        const retryAfterSeconds = Math.ceil(
          (windowMs - (now - entry.windowStart)) / 1000
        );
        return { allowed: false, retryAfterSeconds };
      }

      entry.count += 1;
      return { allowed: true, retryAfterSeconds: 0 };
    },

    reset(ip: string) {
      store.delete(ip);
    },
  };
}

// ---------------------------------------------------------------------------
// Security Event Logger
// ---------------------------------------------------------------------------

export type SecurityEventType =
  | "LOGIN_FAILURE"
  | "LOGIN_SUCCESS"
  | "RATE_LIMITED"
  | "INVALID_INPUT"
  | "UNAUTHORIZED_ACCESS"
  | "SUSPICIOUS_REQUEST";

export interface SecurityEvent {
  type: SecurityEventType;
  ip: string;
  path: string;
  details?: string;
}

/**
 * Writes a structured security event to stderr.
 * Format is JSON so it can be parsed by log-aggregation pipelines.
 *
 * Example output:
 *   {"timestamp":"2026-06-18T12:00:00.000Z","level":"SECURITY","type":"LOGIN_FAILURE","ip":"1.2.3.4","path":"/api/auth/login","details":"..."}
 */
export function logSecurityEvent(event: SecurityEvent): void {
  const entry = JSON.stringify({
    timestamp: new Date().toISOString(),
    level: "SECURITY",
    ...event,
  });
  console.error(entry);
}

// ---------------------------------------------------------------------------
// Slug / ID Validator
// ---------------------------------------------------------------------------

/**
 * Validates and sanitises a URL slug or numeric-like ID.
 * Accepts only alphanumeric characters, hyphens, and underscores (1–128 chars).
 *
 * @returns The trimmed input on success, or null when invalid.
 */
export function validateSlug(input: unknown): string | null {
  if (typeof input !== "string") return null;
  const trimmed = input.trim();
  // Allow alphanumeric, hyphens and underscores only — no path separators,
  // no dots, no special characters that could enable injection.
  if (!/^[a-zA-Z0-9_-]{1,128}$/.test(trimmed)) return null;
  return trimmed;
}

// ---------------------------------------------------------------------------
// Redirect-Path Validator (anti open-redirect)
// ---------------------------------------------------------------------------

/**
 * Validates a redirect target to prevent open-redirect attacks.
 * Accepts only relative paths that start with "/" and do not contain
 * protocol-relative URLs (//), control characters, or newlines.
 *
 * @returns A safe relative path, or "/" when the input is unacceptable.
 */
export function validateRedirectPath(input: unknown): string {
  if (typeof input !== "string") return "/";

  const trimmed = input.trim();

  // Must start with a single "/" but not "//" (protocol-relative)
  if (!trimmed.startsWith("/") || trimmed.startsWith("//")) return "/";

  // Reject newlines and carriage-returns (HTTP response-splitting)
  if (/[\r\n]/.test(trimmed)) return "/";

  // Reject URLs that contain a scheme (e.g. javascript:, data:, https:)
  if (/[a-zA-Z][a-zA-Z0-9+\-.]*:/.test(trimmed)) return "/";

  // Reject path traversal attempts
  if (trimmed.includes("..")) return "/";

  // Limit length
  if (trimmed.length > 512) return "/";

  return trimmed;
}

// ---------------------------------------------------------------------------
// Client IP Extraction
// ---------------------------------------------------------------------------

/**
 * Extracts the real client IP from a Next.js / edge-runtime Request object.
 * Trusts X-Forwarded-For (first hop), then X-Real-IP, then falls back to
 * "unknown" when running locally or behind a non-standard proxy.
 */
export function getClientIp(request: Request): string {
  const xff = request.headers.get("x-forwarded-for");
  if (xff) {
    const firstIp = xff.split(",")[0]?.trim();
    if (firstIp) return firstIp;
  }

  const realIp = request.headers.get("x-real-ip");
  if (realIp) return realIp.trim();

  // Cloudflare
  const cfIp = request.headers.get("cf-connecting-ip");
  if (cfIp) return cfIp.trim();

  return "unknown";
}

// ---------------------------------------------------------------------------
// Attack Pattern Detector
// ---------------------------------------------------------------------------

/**
 * Detects common attack patterns in an arbitrary string input.
 * Covers:
 *   - SQL injection (UNION, SELECT, DROP, INSERT, UPDATE, comment sequences)
 *   - XSS (script tags, event handlers, javascript: URIs, data: URIs)
 *   - Path traversal (../, ..\, %2e%2e)
 *   - LDAP injection (parentheses sequences used in filter strings)
 *   - Command injection (shell metacharacters: ;, |, &&, $(), backtick)
 *
 * @returns true when an attack pattern is detected, false otherwise.
 */
export function detectAttackPattern(input: string): boolean {
  // Normalise: decode common URL-encodings before pattern matching
  let normalised: string;
  try {
    normalised = decodeURIComponent(input).toLowerCase();
  } catch {
    normalised = input.toLowerCase();
  }

  // --- SQL injection ---
  const sqlPatterns = [
    /'\s*(or|and)\s+['"\d]/,              // ' OR '1' / ' AND 1
    /\bunion\s+(all\s+)?select\b/,
    /\bselect\b.+\bfrom\b/,
    /\b(drop|truncate|delete)\s+(table|database|from)\b/,
    /\binsert\s+into\b/,
    /\bupdate\b.+\bset\b/,
    /--\s/,                                // SQL line comment
    /\/\*.*\*\//,                          // SQL block comment
    /;\s*(drop|select|insert|update|delete|exec|execute)\b/, // stacked queries
    /\bexec(\s|\()+/,                      // MSSQL exec
    /\bxp_cmdshell\b/,
  ];

  for (const re of sqlPatterns) {
    if (re.test(normalised)) return true;
  }

  // --- XSS ---
  const xssPatterns = [
    /<\s*script[\s>]/,
    /<\s*\/\s*script\s*>/,
    /javascript\s*:/,
    /vbscript\s*:/,
    /data\s*:\s*text\/html/,
    /on\w+\s*=/,                           // onerror=, onload=, onclick= …
    /<\s*iframe[\s>]/,
    /<\s*img[^>]+src\s*=/,
    /expression\s*\(/,                     // CSS expression()
    /document\s*\.\s*(cookie|write|location)/,
  ];

  for (const re of xssPatterns) {
    if (re.test(normalised)) return true;
  }

  // --- Path traversal ---
  const traversalPatterns = [
    /\.\.[/\\]/,
    /%2e%2e[%2f%5c]/,
    /\.\.%2f/,
    /\.\.%5c/,
    /%252e%252e/,                          // double-encoded
  ];

  for (const re of traversalPatterns) {
    if (re.test(normalised)) return true;
  }

  // --- LDAP injection ---
  const ldapPatterns = [
    /\*\)\s*\(/,                           // *)(
    /\)\s*\(\s*\|/,                        // )(|
    /\)\s*\(\s*&/,                         // )(&
    /\(objectclass=\*/,
  ];

  for (const re of ldapPatterns) {
    if (re.test(normalised)) return true;
  }

  // --- Command injection ---
  const cmdPatterns = [
    /[;|`]\s*(ls|cat|rm|wget|curl|bash|sh|python|perl|nc|ncat)\b/,
    /\$\s*\(/,                             // $( subshell )
    /`[^`]+`/,                             // backtick execution
    /&&\s*(ls|cat|rm|wget|curl|bash|sh)\b/,
  ];

  for (const re of cmdPatterns) {
    if (re.test(normalised)) return true;
  }

  return false;
}
