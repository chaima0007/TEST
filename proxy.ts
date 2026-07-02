import { NextRequest, NextResponse } from "next/server";

const PROTECTED = ["/dashboard", "/api/alerts", "/api/competitors", "/api/reports", "/api/stats", "/api/outreach"];

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Désinscription : route publique, aucune authentification requise.
  if (pathname.startsWith("/api/outreach/unsubscribe")) return NextResponse.next();

  const isProtected = PROTECTED.some((p) => pathname.startsWith(p));
  if (!isProtected) return NextResponse.next();

  const session = request.cookies.get("ciq_session");
  if (!session?.value) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("next", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/api/alerts/:path*", "/api/competitors/:path*", "/api/reports/:path*", "/api/stats/:path*", "/api/outreach/:path*"],
};
