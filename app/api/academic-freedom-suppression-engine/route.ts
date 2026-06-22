import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[academic-freedom-suppression-engine] SWARM_API_URL is not set — running in mock mode.");
}

// ── Static dataset — Wave 197 / CaelumSwarm™ ─────────────────────────────────

const ENTITIES = [
  {
    id: "AFS-001",
    name: "China",
    country: "China",
    composite_score: 91.20,
    severity: "critique",
    estimated_academic_freedom_suppression_index: 9.12,
    key_violation: "Censure académique systématique — interdiction sujets politiques, surveillance chercheurs, expulsion universitaires étrangers",
  },
  {
    id: "AFS-002",
    name: "Turkey",
    country: "Turkey",
    composite_score: 85.00,
    severity: "critique",
    estimated_academic_freedom_suppression_index: 8.50,
    key_violation: "Purges post-2016 — 6 000 académiciens licenciés, pétition Paix signataires emprisonnés",
  },
  {
    id: "AFS-003",
    name: "Iran",
    country: "Iran",
    composite_score: 82.05,
    severity: "critique",
    estimated_academic_freedom_suppression_index: 8.21,
    key_violation: "Exclusion disciplines jugées impures — femmes bannies de certaines filières, arrestations chercheurs dissidents",
  },
  {
    id: "AFS-004",
    name: "Saudi Arabia",
    country: "Saudi Arabia",
    composite_score: 75.70,
    severity: "critique",
    estimated_academic_freedom_suppression_index: 7.57,
    key_violation: "Contrôle curricula par autorités religieuses — arrestations économistes et sociologues critiques du régime",
  },
  {
    id: "AFS-005",
    name: "Russia",
    country: "Russia",
    composite_score: 57.95,
    severity: "élevé",
    estimated_academic_freedom_suppression_index: 5.80,
    key_violation: "Lois agents étrangers — fermeture Memorial, pression sur sciences sociales et politiques",
  },
  {
    id: "AFS-006",
    name: "Hungary",
    country: "Hungary",
    composite_score: 53.75,
    severity: "élevé",
    estimated_academic_freedom_suppression_index: 5.38,
    key_violation: "Expulsion CEU — réforme gouvernance universités, contrôle politique de la recherche",
  },
  {
    id: "AFS-007",
    name: "UNESCO",
    country: "France",
    composite_score: 25.50,
    severity: "modéré",
    estimated_academic_freedom_suppression_index: 2.55,
    key_violation: "Monitoring insuffisant — rapports liberté académique limités, pression États membres sur recommandations",
  },
  {
    id: "AFS-008",
    name: "Scholars at Risk",
    country: "USA",
    composite_score: 10.75,
    severity: "faible",
    estimated_academic_freedom_suppression_index: 1.08,
    key_violation: "ONG protection académiciens — réseau 600 institutions, plaidoyer cas individuels, modèle exemplaire",
  },
];

const AVG_SCORE = 60.24;

const ACCENT = "#7c3aed";
const WAVE = 197;

export const revalidate = 30;

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(sealResponse({ error: "SWARM_API_URL not configured" }), { status: 502 });
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/academic-freedom-suppression-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data));
  } catch {
    const fallback = {
      source: "mock",
      wave: WAVE,
      accent: ACCENT,
      avg_composite_score: AVG_SCORE,
      entity_count: ENTITIES.length,
      entities: ENTITIES,
    };
    return NextResponse.json(sealResponse(fallback), { status: 502 });
  }
}
