import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/shopify/db";
import { isValidShopDomain } from "@/lib/shopify/config";
import { verifyWebhookHmac } from "@/lib/shopify/webhooks";

// Receives the webhooks declared in shopify.app.toml. Shopify requires a 200
// within 5 seconds and a 401 on invalid HMAC.
export async function POST(request: NextRequest) {
  const rawBody = await request.text();
  const hmac = request.headers.get("x-shopify-hmac-sha256");
  if (!verifyWebhookHmac(rawBody, hmac)) {
    return NextResponse.json({ error: "Invalid HMAC" }, { status: 401 });
  }

  const topic = request.headers.get("x-shopify-topic") ?? "";
  const shop = request.headers.get("x-shopify-shop-domain") ?? "";

  // Defense in depth: the shop domain feeds Prisma queries below. Even though
  // HMAC has already passed, reject a malformed domain before using it.
  if (!isValidShopDomain(shop)) {
    return NextResponse.json({ error: "Invalid shop domain" }, { status: 400 });
  }

  switch (topic) {
    case "app/uninstalled": {
      // Access tokens are revoked on uninstall; mark the shop so a reinstall
      // triggers a fresh token exchange.
      await prisma().shopifyShop.updateMany({
        where: { shop },
        data: { uninstalledAt: new Date() },
      });
      break;
    }
    case "app/scopes_update": {
      const payload = JSON.parse(rawBody) as { current?: string[] };
      await prisma().shopifyShop.updateMany({
        where: { shop },
        data: { scope: payload.current?.join(",") ?? null },
      });
      break;
    }
    // GDPR compliance topics: CompeteIQ stores no customer data, so there is
    // nothing to export or redact — acknowledging with a 200 is sufficient.
    case "customers/data_request":
    case "customers/redact":
      break;
    case "shop/redact": {
      await prisma().shopifyShop.deleteMany({ where: { shop } });
      break;
    }
    default:
      break;
  }

  return NextResponse.json({ ok: true });
}
