import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[prison-labor-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[prison-labor-rights-engine] SWARM_API_URL is not set — running in mock mode.");
}

// ── Static dataset — Wave 196 / CaelumSwarm™ ─────────────────────────────────

const ENTITIES = [
  {
    id: "PLR-001",
    name: "CoreCivic (formerly CCA)",
    country: "USA",
    composite_score: 87.75,
    severity: "critique",
    estimated_prison_labor_rights_index: 8.78,
    key_violation: "Privatisation carcérale — conditions de détention sous-standard, lobbying anti-réforme",
  },
  {
    id: "PLR-002",
    name: "The GEO Group",
    country: "USA",
    composite_score: 85.50,
    severity: "critique",
    estimated_prison_labor_rights_index: 8.55,
    key_violation: "Centres de détention ICE — violations droits humains, travail forcé",
  },
  {
    id: "PLR-003",
    name: "Aramark Correctional",
    country: "USA",
    composite_score: 77.90,
    severity: "critique",
    estimated_prison_labor_rights_index: 7.79,
    key_violation: "Services restauration prisons — exploitation main-d'œuvre détenue",
  },
  {
    id: "PLR-004",
    name: "UNICOR Federal Prison Industries",
    country: "USA",
    composite_score: 73.60,
    severity: "critique",
    estimated_prison_labor_rights_index: 7.36,
    key_violation: "Programme travail fédéral — salaires 0,23–1,15$/h, concurrence privé",
  },
  {
    id: "PLR-005",
    name: "Sodexo Justice Services",
    country: "France",
    composite_score: 58.90,
    severity: "élevé",
    estimated_prison_labor_rights_index: 5.89,
    key_violation: "Gestion pénitentiaire 8 pays — opacité conditions travail détenus",
  },
  {
    id: "PLR-006",
    name: "Serco Group plc",
    country: "UK",
    composite_score: 54.90,
    severity: "élevé",
    estimated_prison_labor_rights_index: 5.49,
    key_violation: "Prisons Australie/UK — incidents violences, audits défavorables",
  },
  {
    id: "PLR-007",
    name: "Salvation Army",
    country: "USA",
    composite_score: 28.70,
    severity: "modéré",
    estimated_prison_labor_rights_index: 2.87,
    key_violation: "Programmes réinsertion — critiques sur travail conditionnel aux services",
  },
  {
    id: "PLR-008",
    name: "Prison Fellowship International",
    country: "USA",
    composite_score: 13.80,
    severity: "faible",
    estimated_prison_labor_rights_index: 1.38,
    key_violation: "ONG réhabilitation — modèle axé droits, programmes certifiés",
  },
];

const AVG_SCORE = 60.13;

const ACCENT = "#4c1d95";
const WAVE = 196;

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(
        `${SWARM_API_URL}/engines/prison-labor-rights`,
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
