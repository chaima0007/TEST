import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[gig-workers-platform-economy-engine] SWARM_API_URL is not set — running in mock mode.");
}

// ── Static dataset — Wave 196 / CaelumSwarm™ ─────────────────────────────────

const ENTITIES = [
  {
    id: "GWP-001",
    name: "Uber Technologies Inc",
    country: "USA",
    composite_score: 86.60,
    severity: "critique",
    estimated_gig_workers_platform_economy_index: 8.66,
    key_violation: "Classification erronée travailleurs — 20+ États, amendes $1,1Md Californie",
  },
  {
    id: "GWP-002",
    name: "Deliveroo Holdings plc",
    country: "UK",
    composite_score: 83.25,
    severity: "critique",
    estimated_gig_workers_platform_economy_index: 8.33,
    key_violation: "Livreurs auto-entrepreneurs — refus statut salarié malgré arrêts UK/FR",
  },
  {
    id: "GWP-003",
    name: "Amazon Flex",
    country: "USA",
    composite_score: 82.50,
    severity: "critique",
    estimated_gig_workers_platform_economy_index: 8.25,
    key_violation: "Livreurs indépendants — algorithme opaque, désactivations sans recours",
  },
  {
    id: "GWP-004",
    name: "Glovo App SL",
    country: "Espagne",
    composite_score: 76.85,
    severity: "critique",
    estimated_gig_workers_platform_economy_index: 7.69,
    key_violation: "Loi Rider Espagne — condamné 79M€, résistance systématique requalification",
  },
  {
    id: "GWP-005",
    name: "Lyft Inc",
    country: "USA",
    composite_score: 59.00,
    severity: "élevé",
    estimated_gig_workers_platform_economy_index: 5.90,
    key_violation: "Prop 22 Californie — campagne $200M contre droits chauffeurs",
  },
  {
    id: "GWP-006",
    name: "Fiverr International",
    country: "Israël",
    composite_score: 52.80,
    severity: "élevé",
    estimated_gig_workers_platform_economy_index: 5.28,
    key_violation: "Freelances pays émergents — commissions 20%, paiements différés 14j",
  },
  {
    id: "GWP-007",
    name: "Etsy Inc",
    country: "USA",
    composite_score: 30.10,
    severity: "modéré",
    estimated_gig_workers_platform_economy_index: 3.01,
    key_violation: "Vendeurs indépendants — hausses frais contestées, grève vendeuses 2022",
  },
  {
    id: "GWP-008",
    name: "Fairwork Foundation",
    country: "UK",
    composite_score: 13.10,
    severity: "faible",
    estimated_gig_workers_platform_economy_index: 1.31,
    key_violation: "ONG notation plateformes — référence mondiale droits travailleurs gig",
  },
];

const AVG_SCORE = 60.53;

const ACCENT = "#0369a1";
const WAVE = 196;

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(
        `${SWARM_API_URL}/engines/gig-workers-platform-economy`,
        { next: { revalidate: 30 } }
      );
      if (res.ok) {
        const live = await res.json();
        return NextResponse.json(sealResponse({ ...live, source: "live" }));
      }
    } catch {
      /* fall through to mock */
    }
  }

  return NextResponse.json(
    sealResponse({
      source: "mock",
      wave: WAVE,
      accent: ACCENT,
      avg_composite_score: AVG_SCORE,
      entity_count: ENTITIES.length,
      entities: ENTITIES,
    })
  );
}
