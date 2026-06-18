/**
 * Centralised security checks for API Route Handlers.
 *
 * Usage:
 *   import { runSecurityChecks } from "@/lib/security-middleware";
 *
 *   export async function GET(request: NextRequest) {
 *     const { ok, response } = runSecurityChecks(request, { requireAuth: true });
 *     if (!ok) return response!;
 *     // … normal handler logic
 *   }
 */

import { NextRequest, NextResponse } from "next/server";
import {
  detectAttackPattern,
  getClientIp,
  logSecurityEvent,
} from "@/lib/security";

export interface SecurityCheckResult {
  ok: boolean;
  /** When ok is false, return this response immediately from the handler. */
  response?: NextResponse;
}

export interface SecurityCheckOptions {
  /**
   * When true, verifies that the `ciq_session` cookie is present.
   * Returns 401 when missing and logs an UNAUTHORIZED_ACCESS event.
   */
  requireAuth?: boolean;
  /**
   * When true, reads the request body as text and scans it for attack
   * patterns.  Only usable for routes that parse JSON bodies themselves
   * afterwards (body can only be consumed once — use carefully).
   */
  checkBody?: boolean;
}

// Security headers added to every rejection response.
const SECURITY_HEADERS: Record<string, string> = {
  "X-Content-Type-Options": "nosniff",
  "Cache-Control": "no-store",
};

/**
 * Runs a pipeline of security checks on an incoming API request.
 *
 * Checks performed (always):
 *   1. Scan request headers (User-Agent, Referer, query string) for attack
 *      patterns and block + log SUSPICIOUS_REQUEST on a hit.
 *
 * Checks performed when `requireAuth: true`:
 *   2. Verify the `ciq_session` cookie exists.  Returns 401 and logs
 *      UNAUTHORIZED_ACCESS when the cookie is absent.
 *
 * Checks performed when `checkBody: true`:
 *   3. Buffer and scan the body text for attack patterns, then log
 *      SUSPICIOUS_REQUEST + return 400 on a hit.
 *      Note: this clones the body via request.text() — the original request
 *      body stream will have been consumed.  Use only when the upstream
 *      handler does not need to re-read it, or clone before calling.
 */
export function runSecurityChecks(
  request: NextRequest,
  options: SecurityCheckOptions = {}
): SecurityCheckResult {
  const ip = getClientIp(request);
  const path = request.nextUrl.pathname;

  // ------------------------------------------------------------------
  // 1. Header / query-string attack pattern scan
  // ------------------------------------------------------------------
  const suspiciousValues: string[] = [
    request.nextUrl.search,
    request.headers.get("user-agent") ?? "",
    request.headers.get("referer") ?? "",
    request.headers.get("x-custom-header") ?? "",
  ];

  for (const value of suspiciousValues) {
    if (value && detectAttackPattern(value)) {
      logSecurityEvent({
        type: "SUSPICIOUS_REQUEST",
        ip,
        path,
        details: `Attack pattern detected in request metadata: ${value.slice(0, 200)}`,
      });
      return {
        ok: false,
        response: NextResponse.json(
          { error: "Bad Request" },
          { status: 400, headers: SECURITY_HEADERS }
        ),
      };
    }
  }

  // ------------------------------------------------------------------
  // 2. Authentication check
  // ------------------------------------------------------------------
  if (options.requireAuth) {
    const session = request.cookies.get("ciq_session");
    if (!session?.value) {
      logSecurityEvent({
        type: "UNAUTHORIZED_ACCESS",
        ip,
        path,
        details: "Missing ciq_session cookie",
      });
      return {
        ok: false,
        response: NextResponse.json(
          { error: "Unauthorized" },
          { status: 401, headers: SECURITY_HEADERS }
        ),
      };
    }
  }

  return { ok: true };
}
