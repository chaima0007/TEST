import { adminGraphql } from "./admin";
import { isValidShopDomain } from "./config";
import { prisma } from "./db";

// Couche « transparence logistique » (docs/ARCHITECTURE_BOUTIQUE.md §2).
// Un seul vocabulaire de statut, partagé par la page publique /suivi/[orderId]
// et par le webhook fulfillments/* — pour éviter toute divergence.

export type TrackingStatus = "confirmed" | "shipped" | "in_transit" | "delivered";

export const TRACKING_STEPS: ReadonlyArray<{
  status: TrackingStatus;
  label: string;
  description: string;
}> = [
  { status: "confirmed", label: "Confirmée", description: "Commande reçue et confirmée" },
  { status: "shipped", label: "Expédiée", description: "Colis remis au transporteur" },
  { status: "in_transit", label: "En livraison", description: "Colis en route vers vous" },
  { status: "delivered", label: "Livrée", description: "Colis remis au destinataire" },
];

const STATUS_ORDER: Record<TrackingStatus, number> = {
  confirmed: 0,
  shipped: 1,
  in_transit: 2,
  delivered: 3,
};

export function isTrackingStatus(value: unknown): value is TrackingStatus {
  return (
    value === "confirmed" ||
    value === "shipped" ||
    value === "in_transit" ||
    value === "delivered"
  );
}

// Étape enrichie pour l'affichage : chaque jalon sait s'il est atteint / en cours.
export interface TrackingStep {
  status: TrackingStatus;
  label: string;
  description: string;
  completed: boolean;
  current: boolean;
}

export interface OrderTrackingView {
  orderId: string;
  orderNumber: string;
  status: TrackingStatus;
  statusLabel: string;
  estimatedDelivery: string | null; // ISO 8601 ; formaté côté page
  trackingUrl: string | null;
  trackingCompany: string | null;
  updatedAt: string; // ISO 8601
  steps: TrackingStep[];
  isDemo: boolean; // true tant qu'aucune boutique n'est connectée
}

function buildSteps(status: TrackingStatus): TrackingStep[] {
  const currentRank = STATUS_ORDER[status];
  return TRACKING_STEPS.map((step) => {
    const rank = STATUS_ORDER[step.status];
    return {
      ...step,
      completed: rank < currentRank || rank === currentRank,
      current: rank === currentRank,
    };
  });
}

function statusLabel(status: TrackingStatus): string {
  return TRACKING_STEPS.find((s) => s.status === status)?.label ?? status;
}

// ── Entrées non fiables ──────────────────────────────────────────────────────
// L'orderId vient de l'URL publique : on n'accepte qu'un identifiant numérique
// Shopify ou un GID `gid://shopify/Order/<digits>`, et on renvoie un GID
// canonique. Tout le reste est rejeté (la page appelle alors notFound()).
export function parseOrderGid(raw: string): string | null {
  const value = decodeURIComponent(raw).trim();
  const gidMatch = /^gid:\/\/shopify\/Order\/(\d+)$/.exec(value);
  if (gidMatch) return `gid://shopify/Order/${gidMatch[1]}`;
  if (/^\d{1,20}$/.test(value) && value !== "0") return `gid://shopify/Order/${value}`;
  return null;
}

// Convertit les champs d'un webhook fulfillment (status + shipment_status) vers
// notre vocabulaire. Utilisé par app/api/shopify/webhooks/route.ts.
export function mapFulfillmentToStatus(
  status: string | null | undefined,
  shipmentStatus: string | null | undefined,
): TrackingStatus {
  const shipment = (shipmentStatus ?? "").toLowerCase();
  if (shipment === "delivered") return "delivered";
  if (
    shipment === "in_transit" ||
    shipment === "out_for_delivery" ||
    shipment === "attempted_delivery" ||
    shipment === "ready_for_pickup"
  ) {
    return "in_transit";
  }
  // Un fulfillment "success"/"open" sans info d'acheminement = expédié.
  const fulfillmentStatus = (status ?? "").toLowerCase();
  if (fulfillmentStatus === "success" || fulfillmentStatus === "open" || fulfillmentStatus === "pending") {
    return "shipped";
  }
  return "confirmed";
}

// ── Chemin réel : Admin API (query order → fulfillments) ─────────────────────
// NOTE : à valider contre le schéma live (MCP validate_graphql_codeblocks)
// dès qu'une boutique de dev est connectée. Version API : 2026-07.
const ORDER_TRACKING_QUERY = /* GraphQL */ `
  query OrderTracking($id: ID!) {
    order(id: $id) {
      id
      name
      displayFulfillmentStatus
      fulfillments(first: 10) {
        status
        estimatedDeliveryAt
        updatedAt
        trackingInfo(first: 1) {
          number
          url
          company
        }
        events(first: 20, sortKey: HAPPENED_AT, reverse: true) {
          nodes {
            status
            happenedAt
          }
        }
      }
    }
  }
`;

interface AdminOrderTracking {
  order: {
    id: string;
    name: string;
    displayFulfillmentStatus: string | null;
    fulfillments: Array<{
      status: string | null;
      estimatedDeliveryAt: string | null;
      updatedAt: string | null;
      trackingInfo: Array<{ number: string | null; url: string | null; company: string | null }>;
      events: { nodes: Array<{ status: string | null; happenedAt: string | null }> };
    }>;
  } | null;
}

function statusFromAdminOrder(order: NonNullable<AdminOrderTracking["order"]>): TrackingStatus {
  const fulfillment = order.fulfillments[0];
  if (!fulfillment) return "confirmed";
  // L'événement le plus récent fait foi (events triés reverse=true).
  const latestEvent = fulfillment.events.nodes[0]?.status?.toUpperCase() ?? "";
  if (latestEvent === "DELIVERED") return "delivered";
  if (
    latestEvent === "IN_TRANSIT" ||
    latestEvent === "OUT_FOR_DELIVERY" ||
    latestEvent === "ATTEMPTED_DELIVERY" ||
    latestEvent === "READY_FOR_PICKUP"
  ) {
    return "in_transit";
  }
  return "shipped";
}

async function fetchOrderTrackingFromAdmin(
  shop: string,
  accessToken: string,
  orderGid: string,
): Promise<OrderTrackingView | null> {
  const data = await adminGraphql<AdminOrderTracking>(shop, accessToken, ORDER_TRACKING_QUERY, {
    id: orderGid,
  });
  const order = data.order;
  if (!order) return null;

  const status = statusFromAdminOrder(order);
  const fulfillment = order.fulfillments[0];
  const tracking = fulfillment?.trackingInfo[0];

  return {
    orderId: order.id,
    orderNumber: order.name,
    status,
    statusLabel: statusLabel(status),
    estimatedDelivery: fulfillment?.estimatedDeliveryAt ?? null,
    trackingUrl: tracking?.url ?? null,
    trackingCompany: tracking?.company ?? null,
    updatedAt: fulfillment?.updatedAt ?? new Date().toISOString(),
    steps: buildSteps(status),
    isDemo: false,
  };
}

// Résout la boutique cible pour la page publique. Aucune donnée secrète ici :
// le domaine peut être fixé via SHOPIFY_STORE_DOMAIN, sinon on prend la seule
// boutique installée. Renvoie null si rien n'est connecté (→ mode démo).
async function resolveConnectedShop(): Promise<{ shop: string; accessToken: string } | null> {
  const envDomain = process.env.SHOPIFY_STORE_DOMAIN;
  try {
    const db = prisma();
    if (envDomain && isValidShopDomain(envDomain)) {
      const record = await db.shopifyShop.findUnique({ where: { shop: envDomain } });
      if (record && !record.uninstalledAt) {
        return { shop: record.shop, accessToken: record.accessToken };
      }
      return null;
    }
    const record = await db.shopifyShop.findFirst({ where: { uninstalledAt: null } });
    if (record) return { shop: record.shop, accessToken: record.accessToken };
    return null;
  } catch {
    // Pas de base accessible (ex. environnement de build) → mode démo.
    return null;
  }
}

// Données de démonstration TYPÉES, servies tant qu'aucune boutique n'est
// connectée. La boutique n'existe pas encore (docs/PLAN_LANCEMENT.md §4) :
// dès qu'une boutique de dev est reliée et qu'un token est stocké, le chemin
// Admin API ci-dessus prend le relais automatiquement.
function demoTrackingView(orderGid: string): OrderTrackingView {
  const numericId = orderGid.split("/").pop() ?? "1001";
  const status: TrackingStatus = "in_transit"; // scénario vitrine : en livraison
  const eta = new Date(Date.now() + 2 * 24 * 60 * 60 * 1000); // +2 jours
  return {
    orderId: orderGid,
    orderNumber: `#${numericId}`,
    status,
    statusLabel: statusLabel(status),
    estimatedDelivery: eta.toISOString(),
    trackingUrl: null,
    trackingCompany: "Colissimo",
    updatedAt: new Date().toISOString(),
    steps: buildSteps(status),
    isDemo: true,
  };
}

// Point d'entrée de la page publique. Renvoie null uniquement si l'orderId est
// invalide ou introuvable côté Admin API (→ état « commande introuvable »).
export async function getOrderTrackingView(rawOrderId: string): Promise<OrderTrackingView | null> {
  const orderGid = parseOrderGid(rawOrderId);
  if (!orderGid) return null;

  const connected = await resolveConnectedShop();
  if (!connected) {
    // Aucune boutique connectée : on sert la démo typée (jamais null, pour
    // qu'un lien de suivi reste présentable pendant la phase de construction).
    return demoTrackingView(orderGid);
  }

  return fetchOrderTrackingFromAdmin(connected.shop, connected.accessToken, orderGid);
}
