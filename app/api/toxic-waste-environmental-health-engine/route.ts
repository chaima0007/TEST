import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[toxic-waste-environmental-health-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[toxic-waste-environmental-health-engine] SWARM_API_URL is not set — running in mock mode.");
}

// ── Static dataset — Wave 196 / CaelumSwarm™ ─────────────────────────────────

const ENTITIES = [
  {
    id: "TWE-001",
    name: "Dow Chemical Company",
    country: "USA",
    composite_score: 86.95,
    severity: "critique",
    estimated_toxic_waste_environmental_health_index: 8.70,
    key_violation: "Contamination PFAS/dioxine — class actions 50+ États",
  },
  {
    id: "TWE-002",
    name: "Chevron Corporation",
    country: "USA",
    composite_score: 84.25,
    severity: "critique",
    estimated_toxic_waste_environmental_health_index: 8.43,
    key_violation: "Lago Agrio Équateur — 30Mds$ contamination 30 ans",
  },
  {
    id: "TWE-003",
    name: "Trafigura Group",
    country: "Singapore",
    composite_score: 81.95,
    severity: "critique",
    estimated_toxic_waste_environmental_health_index: 8.20,
    key_violation: "Déchets toxiques Abidjan 2006 — 100 000 victimes",
  },
  {
    id: "TWE-004",
    name: "Syngenta AG",
    country: "Suisse",
    composite_score: 78.80,
    severity: "critique",
    estimated_toxic_waste_environmental_health_index: 7.88,
    key_violation: "Atrazine — contamination eaux potables 30 États US",
  },
  {
    id: "TWE-005",
    name: "Veolia Environment",
    country: "France",
    composite_score: 56.55,
    severity: "élevé",
    estimated_toxic_waste_environmental_health_index: 5.66,
    key_violation: "Incidents gestion déchets — 12 pays, sanctions EPA",
  },
  {
    id: "TWE-006",
    name: "Waste Management Inc",
    country: "USA",
    composite_score: 51.80,
    severity: "élevé",
    estimated_toxic_waste_environmental_health_index: 5.18,
    key_violation: "Landfills communautés défavorisées — justice environnementale",
  },
  {
    id: "TWE-007",
    name: "SUEZ Group",
    country: "France",
    composite_score: 28.70,
    severity: "modéré",
    estimated_toxic_waste_environmental_health_index: 2.87,
    key_violation: "Amélioration progressive — certifications ISO 14001",
  },
  {
    id: "TWE-008",
    name: "Interface Inc",
    country: "USA",
    composite_score: 12.85,
    severity: "faible",
    estimated_toxic_waste_environmental_health_index: 1.29,
    key_violation: "Leader durabilité — Mission Zero atteint 2020",
  },
];

const AVG_SCORE = 60.23;

const ACCENT = "#b45309";
const WAVE = 196;

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(
        `${SWARM_API_URL}/engines/toxic-waste-environmental-health`,
        { next: { revalidate: 30 } }
      );
      if (res.ok) {
        const live = await res.json();
        return sealResponse(NextResponse.json(sealResponse({ ...live, source: "live" })));
      }
    } catch {
      /* fall through to mock */
    }
  }

  return sealResponse(NextResponse.json(
    sealResponse({
      source: "mock",
      wave: WAVE,
      accent: ACCENT,
      avg_composite_score: AVG_SCORE,
      entity_count: ENTITIES.length,
      entities: ENTITIES,
    })
  ));
}
