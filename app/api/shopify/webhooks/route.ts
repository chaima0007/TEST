import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/shopify/db";
import { isValidShopDomain } from "@/lib/shopify/config";
import { verifyWebhookHmac } from "@/lib/shopify/webhooks";
import { mapFulfillmentToStatus } from "@/lib/shopify/tracking";

// Charge utile d'un webhook fulfillments/create|update (sous-ensemble utilisé).
interface FulfillmentWebhookPayload {
  order_id?: number | string;
  status?: string | null;
  shipment_status?: string | null;
  tracking_url?: string | null;
  tracking_urls?: string[] | null;
  estimated_delivery_at?: string | null;
}

// Enregistre l'avancement d'une commande à partir d'un webhook fulfillment.
// Toutes les entrées viennent d'un payload signé (HMAC déjà vérifié) mais
// restent validées avant d'alimenter Prisma (défense en profondeur).
async function recordFulfillment(shop: string, rawBody: string): Promise<void> {
  const payload = JSON.parse(rawBody) as FulfillmentWebhookPayload;

  const orderId = payload.order_id != null ? String(payload.order_id) : "";
  // order_id Shopify est un entier positif ; on rejette tout le reste.
  if (!/^\d{1,20}$/.test(orderId)) return;

  const status = mapFulfillmentToStatus(payload.status, payload.shipment_status);

  const trackingUrlRaw = payload.tracking_url ?? payload.tracking_urls?.[0] ?? null;
  // N'accepte qu'une URL http(s) bien formée pour le lien transporteur.
  let trackingUrl: string | null = null;
  if (trackingUrlRaw) {
    try {
      const parsed = new URL(trackingUrlRaw);
      if (parsed.protocol === "http:" || parsed.protocol === "https:") trackingUrl = parsed.toString();
    } catch {
      trackingUrl = null;
    }
  }

  let estimatedDelivery: Date | null = null;
  if (payload.estimated_delivery_at) {
    const d = new Date(payload.estimated_delivery_at);
    if (!Number.isNaN(d.getTime())) estimatedDelivery = d;
  }

  await prisma().orderTracking.upsert({
    where: { shop_orderId: { shop, orderId } },
    create: { shop, orderId, status, trackingUrl, estimatedDelivery },
    update: { status, trackingUrl, estimatedDelivery },
  });
}

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
    // Transparence logistique : on suit l'avancement des livraisons pour la
    // page publique /suivi/[orderId] (docs/ARCHITECTURE_BOUTIQUE.md §2).
    case "fulfillments/create":
    case "fulfillments/update": {
      await recordFulfillment(shop, rawBody);
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
