import { NextRequest, NextResponse } from "next/server";
import { adminGraphql } from "./admin";
import { SessionTokenError, shopFromPayload, verifySessionToken } from "./session-token";
import { getOrCreateAccessToken } from "./token-exchange";

export interface ShopifyContext {
  shop: string;
  userId: string;
  admin: <T = unknown>(query: string, variables?: Record<string, unknown>) => Promise<T>;
}

// Authenticates an embedded-app request. App Bridge's fetch interception adds
// the session token as `Authorization: Bearer <token>` on same-origin calls.
export async function authenticateShopify(request: NextRequest): Promise<ShopifyContext> {
  const authorization = request.headers.get("authorization") ?? "";
  const token = authorization.startsWith("Bearer ") ? authorization.slice(7) : null;
  if (!token) throw new SessionTokenError("Missing Authorization header");

  const payload = verifySessionToken(token);
  const shop = shopFromPayload(payload);
  const accessToken = await getOrCreateAccessToken(shop, token);

  return {
    shop,
    userId: payload.sub,
    admin: (query, variables) => adminGraphql(shop, accessToken, query, variables),
  };
}

export function unauthorizedResponse(error: unknown): NextResponse {
  const message = error instanceof SessionTokenError ? error.message : "Unauthorized";
  // X-Shopify-Retry-Invalid-Session-Request tells App Bridge to retry with a fresh token.
  return NextResponse.json(
    { error: message },
    { status: 401, headers: { "X-Shopify-Retry-Invalid-Session-Request": "1" } },
  );
}
