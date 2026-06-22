import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[water-access-rights-engine] SWARM_API_URL is not set — running in mock mode.");
}

// ── Static dataset — Wave 197 / CaelumSwarm™ ─────────────────────────────────

const ENTITIES = [
  {
    id: "WAR-001",
    name: "Nestlé Waters",
    country: "Switzerland",
    composite_score: 88.30,
    severity: "critique",
    estimated_water_access_rights_index: 8.83,
    key_violation: "Privatisation sources d'eau — extraction abusive dans zones de stress hydrique, conflits avec communautés locales",
  },
  {
    id: "WAR-002",
    name: "Suez",
    country: "France",
    composite_score: 84.00,
    severity: "critique",
    estimated_water_access_rights_index: 8.40,
    key_violation: "Gestion privatisée réseaux eau — tarifs prohibitifs, déconnexions populations vulnérables",
  },
  {
    id: "WAR-003",
    name: "Veolia Water",
    country: "France",
    composite_score: 80.85,
    severity: "critique",
    estimated_water_access_rights_index: 8.09,
    key_violation: "Concessions eau pays en développement — surcoûts, manque transparence, pression tarifaire",
  },
  {
    id: "WAR-004",
    name: "POSCO",
    country: "South Korea",
    composite_score: 77.15,
    severity: "critique",
    estimated_water_access_rights_index: 7.72,
    key_violation: "Sidérurgie grande consommatrice — prélèvements fluviaux excessifs, pollution nappes phréatiques",
  },
  {
    id: "WAR-005",
    name: "Coca-Cola",
    country: "USA",
    composite_score: 56.90,
    severity: "élevé",
    estimated_water_access_rights_index: 5.69,
    key_violation: "Embouteillage eau dans régions en pénurie — conflits Inde, Mexique, Kenya",
  },
  {
    id: "WAR-006",
    name: "PepsiCo",
    country: "USA",
    composite_score: 52.60,
    severity: "élevé",
    estimated_water_access_rights_index: 5.26,
    key_violation: "Extraction eau souterraine — dépassement quotas, concurrence usages agricoles",
  },
  {
    id: "WAR-007",
    name: "Thames Water",
    country: "UK",
    composite_score: 28.10,
    severity: "modéré",
    estimated_water_access_rights_index: 2.81,
    key_violation: "Fuites réseau massives — 25% eau perdue, investissements maintenance insuffisants",
  },
  {
    id: "WAR-008",
    name: "Xylem Inc.",
    country: "USA",
    composite_score: 12.55,
    severity: "faible",
    estimated_water_access_rights_index: 1.26,
    key_violation: "Solutions technologiques eau — modèle orienté accès universel, certifications droits humains",
  },
];

const AVG_SCORE = 60.06;

const ACCENT = "#0ea5e9";
const WAVE = 197;

export const revalidate = 30;

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(sealResponse({ error: "SWARM_API_URL not configured" }), { status: 502 });
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/water-access-rights-engine`, { next: { revalidate: 30 } });
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
