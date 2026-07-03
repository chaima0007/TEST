import { createHmac, timingSafeEqual } from "node:crypto";
import { shopifyApiSecret } from "./config";

// Webhook payloads are signed with the app's API secret; the signature arrives
// base64-encoded in the X-Shopify-Hmac-Sha256 header.
export function verifyWebhookHmac(rawBody: string, hmacHeader: string | null): boolean {
  if (!hmacHeader) return false;
  const digest = createHmac("sha256", shopifyApiSecret()).update(rawBody, "utf8").digest();
  let received: Buffer;
  try {
    received = Buffer.from(hmacHeader, "base64");
  } catch {
    return false;
  }
  return received.length === digest.length && timingSafeEqual(received, digest);
}
