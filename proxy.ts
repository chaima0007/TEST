import { NextRequest, NextResponse } from "next/server";
import { getClientIp, logSecurityEvent } from "@/lib/security";

const PROTECTED = ["/dashboard", "/api/alerts", "/api/competitors", "/api/reports", "/api/stats"];
const ALLOWED_ORIGIN = process.env.NEXT_PUBLIC_APP_URL ?? "";

// Only allow same-origin redirects for the `next` parameter (no open redirect)
const SAFE_NEXT_PATTERN = /^\/[a-zA-Z0-9\-_/?=&%#.]+$/;

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // CORS: reject cross-origin requests to protected endpoints
  const origin = request.headers.get("origin");
  if (origin && ALLOWED_ORIGIN && origin !== ALLOWED_ORIGIN) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const isProtected = PROTECTED.some((p) => pathname.startsWith(p));
  if (!isProtected) return NextResponse.next();

  const session = request.cookies.get("ciq_session");
  if (!session?.value) {
    // Log the unauthenticated access attempt before redirecting.
    logSecurityEvent({
      type: "UNAUTHORIZED_ACCESS",
      ip: getClientIp(request),
      path: pathname,
      details: "No ciq_session cookie — redirecting to /login",
    });

    const loginUrl = new URL("/login", request.url);

    // Validate `next` to prevent open redirect (only allow relative paths)
    if (SAFE_NEXT_PATTERN.test(pathname)) {
      loginUrl.searchParams.set("next", pathname);
    }

    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/api/alerts/:path*",
    "/api/competitors/:path*",
    "/api/reports/:path*",
    "/api/stats/:path*",
  ],
};
