import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[indigenous-peoples-rights-engine] SWARM_API_URL is not set — running in mock mode.");
}

// ── Static dataset — Wave 197 / CaelumSwarm™ ─────────────────────────────────

const ENTITIES = [
  {
    id: "IPR-001",
    name: "Vale",
    country: "Brazil",
    composite_score: 89.80,
    severity: "critique",
    estimated_indigenous_peoples_rights_index: 8.98,
    key_violation: "Exploitation minière terres autochtones — catastrophes Mariana et Brumadinho, déplacements forcés communautés",
  },
  {
    id: "IPR-002",
    name: "BHP",
    country: "Australia",
    composite_score: 85.00,
    severity: "critique",
    estimated_indigenous_peoples_rights_index: 8.50,
    key_violation: "Destruction sites sacrés Juukan Gorge — absence consentement préalable éclairé peuples Puutu Kunti Kurrama",
  },
  {
    id: "IPR-003",
    name: "Newmont",
    country: "USA",
    composite_score: 80.85,
    severity: "critique",
    estimated_indigenous_peoples_rights_index: 8.09,
    key_violation: "Mines or pays en développement — contamination eau, violations FPIC, expulsions communautés",
  },
  {
    id: "IPR-004",
    name: "Freeport-McMoRan",
    country: "USA",
    composite_score: 76.90,
    severity: "critique",
    estimated_indigenous_peoples_rights_index: 7.69,
    key_violation: "Mine Grasberg Papouasie — pollution rivière Ok Tedi, impact peuple Amungme et Kamoro",
  },
  {
    id: "IPR-005",
    name: "First Quantum Minerals",
    country: "Canada",
    composite_score: 55.80,
    severity: "élevé",
    estimated_indigenous_peoples_rights_index: 5.58,
    key_violation: "Opérations Zambie et Panama — consultations insuffisantes, résistances communautaires autochtones",
  },
  {
    id: "IPR-006",
    name: "Barrick Gold",
    country: "Canada",
    composite_score: 51.85,
    severity: "élevé",
    estimated_indigenous_peoples_rights_index: 5.19,
    key_violation: "Mines Afrique et Amérique latine — droits fonciers non respectés, violences agents sécurité",
  },
  {
    id: "IPR-007",
    name: "IFC (International Finance Corporation)",
    country: "USA",
    composite_score: 28.70,
    severity: "modéré",
    estimated_indigenous_peoples_rights_index: 2.87,
    key_violation: "Financement projets impactants — conditionnalités FPIC partiellement appliquées",
  },
  {
    id: "IPR-008",
    name: "Forest Peoples Programme",
    country: "UK",
    composite_score: 11.90,
    severity: "faible",
    estimated_indigenous_peoples_rights_index: 1.19,
    key_violation: "ONG défense droits — modèle centré consentement libre, plaidoyer FPIC international",
  },
];

const AVG_SCORE = 60.10;

const ACCENT = "#92400e";
const WAVE = 197;

export const revalidate = 30;

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(sealResponse({ error: "SWARM_API_URL not configured" }), { status: 502 });
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/indigenous-peoples-rights-engine`, { next: { revalidate: 30 } });
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
