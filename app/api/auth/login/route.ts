import { NextRequest, NextResponse } from "next/server";

// Credentials MUST be supplied via environment variables — no hardcoded fallbacks
const DEMO_EMAIL = process.env.DEMO_EMAIL ?? "";
const DEMO_PASSWORD = process.env.DEMO_PASSWORD ?? "";
const ALLOWED_ORIGIN = process.env.NEXT_PUBLIC_APP_URL ?? "";

// --- Rate limiter (in-memory, per IP) ---
// Max 5 attempts per IP per 15-minute window
interface RateLimitEntry {
  count: number;
  windowStart: number;
}
const rateLimitStore = new Map<string, RateLimitEntry>();
const RATE_LIMIT_MAX = 5;
const RATE_LIMIT_WINDOW_MS = 15 * 60 * 1000; // 15 minutes

function getClientIp(req: NextRequest): string {
  return (
    req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ??
    req.headers.get("x-real-ip") ??
    "unknown"
  );
}

function checkRateLimit(ip: string): { allowed: boolean; retryAfterSeconds: number } {
  const now = Date.now();
  const entry = rateLimitStore.get(ip);

  if (!entry || now - entry.windowStart > RATE_LIMIT_WINDOW_MS) {
    // New window
    rateLimitStore.set(ip, { count: 1, windowStart: now });
    return { allowed: true, retryAfterSeconds: 0 };
  }

  if (entry.count >= RATE_LIMIT_MAX) {
    const retryAfterSeconds = Math.ceil(
      (RATE_LIMIT_WINDOW_MS - (now - entry.windowStart)) / 1000
    );
    return { allowed: false, retryAfterSeconds };
  }

  entry.count += 1;
  return { allowed: true, retryAfterSeconds: 0 };
}

function resetRateLimit(ip: string): void {
  rateLimitStore.delete(ip);
}

// --- Security headers for all responses ---
const SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Cache-Control": "no-store",
};

export async function POST(req: NextRequest) {
  // 1. CORS — reject unknown origins
  const origin = req.headers.get("origin");
  if (origin && ALLOWED_ORIGIN && origin !== ALLOWED_ORIGIN) {
    return NextResponse.json(
      { error: "Forbidden" },
      { status: 403, headers: SECURITY_HEADERS }
    );
  }

  // 2. Rate limiting
  const ip = getClientIp(req);
  const { allowed, retryAfterSeconds } = checkRateLimit(ip);
  if (!allowed) {
    return NextResponse.json(
      { error: "Trop de tentatives. Veuillez réessayer plus tard." },
      {
        status: 429,
        headers: {
          ...SECURITY_HEADERS,
          "Retry-After": String(retryAfterSeconds),
        },
      }
    );
  }

  // 3. Parse body safely
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json(
      { error: "Corps de requête invalide" },
      { status: 400, headers: SECURITY_HEADERS }
    );
  }

  // 4. Input validation
  if (
    typeof body !== "object" ||
    body === null ||
    Array.isArray(body)
  ) {
    return NextResponse.json(
      { error: "Corps de requête invalide" },
      { status: 400, headers: SECURITY_HEADERS }
    );
  }

  const { email, password } = body as Record<string, unknown>;

  if (typeof email !== "string" || typeof password !== "string") {
    return NextResponse.json(
      { error: "Identifiants invalides" },
      { status: 401, headers: SECURITY_HEADERS }
    );
  }

  if (email.length > 200 || password.length > 200) {
    return NextResponse.json(
      { error: "Identifiants invalides" },
      { status: 401, headers: SECURITY_HEADERS }
    );
  }

  // 5. Authentication — generic message regardless of which field is wrong
  const emailMatch =
    email.trim().toLowerCase() === DEMO_EMAIL.toLowerCase();
  const passwordMatch = password === DEMO_PASSWORD;

  if (!emailMatch || !passwordMatch) {
    return NextResponse.json(
      { error: "Identifiants invalides" },
      { status: 401, headers: SECURITY_HEADERS }
    );
  }

  // 6. Success — reset rate limit and set secure cookie
  resetRateLimit(ip);

  const response = NextResponse.json({ ok: true }, { headers: SECURITY_HEADERS });
  response.cookies.set("ciq_session", "authenticated", {
    httpOnly: true,
    sameSite: "strict",
    path: "/",
    maxAge: 60 * 60 * 24 * 7, // 7 days
    secure: process.env.NODE_ENV === "production",
  });
  return response;
}
