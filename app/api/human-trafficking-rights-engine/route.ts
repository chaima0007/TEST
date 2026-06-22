import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[human-trafficking-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "HumanTraffickingRights Engine Agent",
  domain: "human_trafficking_rights",
  total_entities: 8,
  avg_composite: 60.18,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Corée du Nord — Trafic femmes vers Chine & organ harvesting",
    "Syrie — Esclavage sexuel ISIS, trafic réfugiés",
    "Afghanistan — Bacha bazi, filles vendues, traite Iran",
  ],
  critical_alerts: [
    "Corée du Nord: State-sponsored trafficking & forced organ extraction",
    "Syrie: Conflict-driven sexual slavery & refugee trafficking",
    "Afghanistan: Taliban-era child trafficking & forced marriage",
    "Thaïlande: Sex tourism hub & forced fishery labour",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_human_trafficking_rights_index: 6.02,
  entities: [
    {
      entity_id: "HTR-001",
      name: "Corée du Nord — Trafic femmes vers Chine & organ harvesting",
      country: "Corée du Nord",
      sex_trafficking_score: 98.0,
      labor_trafficking_score: 95.0,
      organ_trafficking_score: 96.0,
      victim_protection_gap_score: 99.0,
      composite_score: 96.95,
      risk_level: "critique",
      primary_pattern: "State-sponsored trafficking & forced organ extraction",
      estimated_human_trafficking_rights_index: 9.7,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HTR-002",
      name: "Syrie — Esclavage sexuel ISIS, trafic réfugiés",
      country: "Syrie",
      sex_trafficking_score: 92.0,
      labor_trafficking_score: 85.0,
      organ_trafficking_score: 78.0,
      victim_protection_gap_score: 94.0,
      composite_score: 87.15,
      risk_level: "critique",
      primary_pattern: "Conflict-driven sexual slavery & refugee trafficking",
      estimated_human_trafficking_rights_index: 8.72,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HTR-003",
      name: "Afghanistan — Bacha bazi, filles vendues, traite Iran",
      country: "Afghanistan",
      sex_trafficking_score: 86.0,
      labor_trafficking_score: 80.0,
      organ_trafficking_score: 70.0,
      victim_protection_gap_score: 88.0,
      composite_score: 80.9,
      risk_level: "critique",
      primary_pattern: "Taliban-era child trafficking & forced marriage",
      estimated_human_trafficking_rights_index: 8.09,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HTR-004",
      name: "Thaïlande — Hub traite Asie-Pacifique, tourisme sexuel",
      country: "Thaïlande",
      sex_trafficking_score: 82.0,
      labor_trafficking_score: 80.0,
      organ_trafficking_score: 65.0,
      victim_protection_gap_score: 84.0,
      composite_score: 77.65,
      risk_level: "critique",
      primary_pattern: "Sex tourism hub & forced fishery labour",
      estimated_human_trafficking_rights_index: 7.77,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HTR-005",
      name: "Mexique — Cartels, traite frontalière, 80k victimes/an",
      country: "Mexique",
      sex_trafficking_score: 58.0,
      labor_trafficking_score: 55.0,
      organ_trafficking_score: 48.0,
      victim_protection_gap_score: 56.0,
      composite_score: 54.35,
      risk_level: "élevé",
      primary_pattern: "Cartel-controlled border trafficking corridor",
      estimated_human_trafficking_rights_index: 5.44,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HTR-006",
      name: "UE (Roumanie/Bulgarie) — 40% victimes traite identifiées en EU",
      country: "Roumanie/Bulgarie",
      sex_trafficking_score: 50.0,
      labor_trafficking_score: 46.0,
      organ_trafficking_score: 38.0,
      victim_protection_gap_score: 48.0,
      composite_score: 45.6,
      risk_level: "élevé",
      primary_pattern: "Intra-EU source countries, exploitation networks",
      estimated_human_trafficking_rights_index: 4.56,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HTR-007",
      name: "USA — Demande prostitution, trafficking interstate",
      country: "États-Unis",
      sex_trafficking_score: 34.0,
      labor_trafficking_score: 28.0,
      organ_trafficking_score: 18.0,
      victim_protection_gap_score: 30.0,
      composite_score: 27.7,
      risk_level: "modéré",
      primary_pattern: "Demand-side trafficking, Palermo Protocol ratified",
      estimated_human_trafficking_rights_index: 2.77,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HTR-008",
      name: "Pays-Bas — Modèle nordique, criminalisation acheteurs",
      country: "Pays-Bas",
      sex_trafficking_score: 14.0,
      labor_trafficking_score: 10.0,
      organ_trafficking_score: 8.0,
      victim_protection_gap_score: 12.0,
      composite_score: 11.1,
      risk_level: "faible",
      primary_pattern: "Nordic model buyer criminalisation, GRETA compliance",
      estimated_human_trafficking_rights_index: 1.11,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/human-trafficking-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ payload: FALLBACK_PAYLOAD }, { status: 502 })
    );
  }
}
