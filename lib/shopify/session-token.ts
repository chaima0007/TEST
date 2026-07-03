import { createHmac, timingSafeEqual } from "node:crypto";
import { isValidShopDomain, shopifyApiKey, shopifyApiSecret } from "./config";

// App Bridge session tokens are HS256 JWTs signed with the app's API secret.
// https://shopify.dev/docs/apps/build/authentication-authorization/session-tokens

export interface SessionTokenPayload {
  iss: string;
  dest: string;
  aud: string;
  sub: string;
  exp: number;
  nbf: number;
  iat: number;
  jti: string;
  sid: string;
}

const CLOCK_SKEW_SECONDS = 10;

function base64UrlDecode(segment: string): Buffer {
  return Buffer.from(segment.replace(/-/g, "+").replace(/_/g, "/"), "base64");
}

export class SessionTokenError extends Error {}

export function verifySessionToken(token: string): SessionTokenPayload {
  const parts = token.split(".");
  if (parts.length !== 3) throw new SessionTokenError("Malformed session token");
  const [headerB64, payloadB64, signatureB64] = parts;

  const expected = createHmac("sha256", shopifyApiSecret())
    .update(`${headerB64}.${payloadB64}`)
    .digest();
  const received = base64UrlDecode(signatureB64);
  if (received.length !== expected.length || !timingSafeEqual(received, expected)) {
    throw new SessionTokenError("Invalid session token signature");
  }

  const header = JSON.parse(base64UrlDecode(headerB64).toString("utf8"));
  if (header.alg !== "HS256") throw new SessionTokenError("Unexpected signing algorithm");

  const payload = JSON.parse(base64UrlDecode(payloadB64).toString("utf8")) as SessionTokenPayload;
  const now = Math.floor(Date.now() / 1000);
  if (payload.exp < now - CLOCK_SKEW_SECONDS) throw new SessionTokenError("Session token expired");
  if (payload.nbf > now + CLOCK_SKEW_SECONDS) throw new SessionTokenError("Session token not yet valid");
  if (payload.aud !== shopifyApiKey()) throw new SessionTokenError("Session token audience mismatch");

  const shop = new URL(payload.dest).hostname;
  if (!isValidShopDomain(shop)) throw new SessionTokenError("Invalid shop in session token");

  // Shopify recommends confirming that `iss` and `dest` designate the same shop.
  // `iss` looks like https://{shop}.myshopify.com/admin — its hostname must match.
  let issHostname: string;
  try {
    issHostname = new URL(payload.iss).hostname;
  } catch {
    throw new SessionTokenError("Invalid issuer in session token");
  }
  if (issHostname !== shop) throw new SessionTokenError("Session token issuer/destination mismatch");

  return payload;
}

export function shopFromPayload(payload: SessionTokenPayload): string {
  return new URL(payload.dest).hostname;
}
