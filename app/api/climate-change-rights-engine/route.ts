import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-change-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[climate-change-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Climate Change Rights Engine Agent",
  domain: "climate_change_rights",
  total_entities: 8,
  avg_composite: 61.48,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Bangladesh — Inondations massives & déplacements climatiques irréversibles",
    "Îles Marshall — Submersion imminente & droits des réfugiés climatiques",
    "Pakistan — Vagues de chaleur extrêmes & inégalités d&apos;adaptation",
  ],
  critical_alerts: [
    "Bangladesh: Millions de déplacés climatiques sans protection légale",
    "Îles Marshall: Territoire national menacé de disparition totale",
    "Pakistan: Inondations 2022 — un tiers du territoire submergé",
    "Sahel: Sécheresses chroniques & conflits ressources aggravés",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_climate_change_rights_index: 6.15,
  entities: [
    {
      entity_id: "CCR-001",
      name: "Bangladesh — Inondations massives & déplacements climatiques irréversibles",
      country: "Bangladesh",
      climate_vulnerability_score: 96.0,
      climate_adaptation_failure_score: 90.0,
      fossil_fuel_harm_score: 72.0,
      climate_justice_gap_score: 94.0,
      composite_score: 88.9,
      risk_level: "critique",
      primary_pattern: "Mass climate displacement & coastal erosion without legal protection",
      estimated_climate_change_rights_index: 8.89,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CCR-002",
      name: "Îles Marshall — Submersion imminente & droits des réfugiés climatiques",
      country: "Îles Marshall",
      climate_vulnerability_score: 99.0,
      climate_adaptation_failure_score: 85.0,
      fossil_fuel_harm_score: 30.0,
      climate_justice_gap_score: 98.0,
      composite_score: 80.45,
      risk_level: "critique",
      primary_pattern: "National territory disappearance & stateless climate refugees",
      estimated_climate_change_rights_index: 8.05,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CCR-003",
      name: "Pakistan — Vagues de chaleur extrêmes & inégalités d&apos;adaptation",
      country: "Pakistan",
      climate_vulnerability_score: 88.0,
      climate_adaptation_failure_score: 82.0,
      fossil_fuel_harm_score: 70.0,
      climate_justice_gap_score: 85.0,
      composite_score: 81.85,
      risk_level: "critique",
      primary_pattern: "Extreme heat & catastrophic flooding disproportionately harming poor",
      estimated_climate_change_rights_index: 8.19,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CCR-004",
      name: "Sahel (Mali/Niger/Burkina Faso) — Sécheresses & conflits ressources",
      country: "Sahel",
      climate_vulnerability_score: 90.0,
      climate_adaptation_failure_score: 88.0,
      fossil_fuel_harm_score: 55.0,
      climate_justice_gap_score: 91.0,
      composite_score: 81.45,
      risk_level: "critique",
      primary_pattern: "Chronic drought fuelling resource conflicts & mass migration",
      estimated_climate_change_rights_index: 8.15,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CCR-005",
      name: "Inde — Villes inhabitables & pollution industrielle climatique",
      country: "Inde",
      climate_vulnerability_score: 65.0,
      climate_adaptation_failure_score: 60.0,
      fossil_fuel_harm_score: 75.0,
      climate_justice_gap_score: 68.0,
      composite_score: 66.75,
      risk_level: "élevé",
      primary_pattern: "Industrial emissions & urban heat islands affecting marginalised communities",
      estimated_climate_change_rights_index: 6.68,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CCR-006",
      name: "Brésil — Déforestation Amazonie & droits climatiques autochtones",
      country: "Brésil",
      climate_vulnerability_score: 58.0,
      climate_adaptation_failure_score: 55.0,
      fossil_fuel_harm_score: 60.0,
      climate_justice_gap_score: 62.0,
      composite_score: 58.65,
      risk_level: "élevé",
      primary_pattern: "Amazon deforestation & climate rights violations of Indigenous peoples",
      estimated_climate_change_rights_index: 5.87,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CCR-007",
      name: "États-Unis — Communautés frontline & injustice climatique systémique",
      country: "États-Unis",
      climate_vulnerability_score: 35.0,
      climate_adaptation_failure_score: 30.0,
      fossil_fuel_harm_score: 80.0,
      climate_justice_gap_score: 38.0,
      composite_score: 44.0,
      risk_level: "modéré",
      primary_pattern: "Frontline communities facing fossil fuel harm & climate inequality",
      estimated_climate_change_rights_index: 4.4,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "CCR-008",
      name: "Danemark — Neutralité carbone & droits climatiques protégés",
      country: "Danemark",
      climate_vulnerability_score: 8.0,
      climate_adaptation_failure_score: 6.0,
      fossil_fuel_harm_score: 10.0,
      climate_justice_gap_score: 7.0,
      composite_score: 7.85,
      risk_level: "faible",
      primary_pattern: "Carbon neutrality commitments & strong climate rights framework",
      estimated_climate_change_rights_index: 0.79,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/climate-change-rights-engine`, {
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
