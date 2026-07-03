import { shopifyApiKey, shopifyApiSecret } from "./config";
import { prisma } from "./db";

// Exchanges an App Bridge session token for an offline Admin API access token
// (Shopify-managed installation — no OAuth redirect dance needed).
// https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/token-exchange

interface TokenExchangeResponse {
  access_token: string;
  scope: string;
}

export async function exchangeSessionToken(shop: string, sessionToken: string): Promise<TokenExchangeResponse> {
  const response = await fetch(`https://${shop}/admin/oauth/access_token`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({
      client_id: shopifyApiKey(),
      client_secret: shopifyApiSecret(),
      grant_type: "urn:ietf:params:oauth:grant-type:token-exchange",
      subject_token: sessionToken,
      subject_token_type: "urn:ietf:params:oauth:token-type:id_token",
      requested_token_type: "urn:shopify:params:oauth:token-type:offline-access-token",
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Token exchange failed for ${shop}: ${response.status} ${body}`);
  }

  return (await response.json()) as TokenExchangeResponse;
}

export async function getOrCreateAccessToken(shop: string, sessionToken: string): Promise<string> {
  const db = prisma();
  const existing = await db.shopifyShop.findUnique({ where: { shop } });
  if (existing && !existing.uninstalledAt) return existing.accessToken;

  const { access_token, scope } = await exchangeSessionToken(shop, sessionToken);
  await db.shopifyShop.upsert({
    where: { shop },
    create: { shop, accessToken: access_token, scope },
    update: { accessToken: access_token, scope, uninstalledAt: null },
  });
  return access_token;
}
