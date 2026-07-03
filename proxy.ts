import { NextRequest, NextResponse } from "next/server";

const PROTECTED = ["/dashboard", "/api/alerts", "/api/competitors", "/api/reports", "/api/stats"];

export function proxy(request: NextRequest) {
  const { pathname, searchParams } = request.nextUrl;

  // `shopify app dev` points the app URL at the tunnel root: requests coming
  // from the Shopify admin carry shop/host params and belong to the embedded UI.
  if (pathname === "/" && searchParams.has("shop") && (searchParams.has("host") || searchParams.has("embedded"))) {
    const embeddedUrl = request.nextUrl.clone();
    embeddedUrl.pathname = "/shopify";
    return NextResponse.redirect(embeddedUrl);
  }

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
  matcher: [
    "/",
    "/dashboard/:path*",
    "/api/alerts/:path*",
    "/api/competitors/:path*",
    "/api/reports/:path*",
    "/api/stats/:path*",
  ],
};
