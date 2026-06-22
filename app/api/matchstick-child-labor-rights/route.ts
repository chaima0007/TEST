import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[matchstick-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[matchstick-child-labor-rights] SWARM_API_URL is not set — falling back to mock data");
}

export const revalidate = 30;

const MOCK = {
  engine: "MCLR_ENGINE",
  domain: "matchstick_child_labor_rights",
  total_entities: 8,
  avg_composite: 61.09,
  confidence_score: 0.81,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["ilo_child_labour_database", "match_industry_watchdog_reports", "unicef_hazardous_work_index"],
  entities: [
    { id: "MCLR-001", name: "WIMCO Matches India", country: "Inde", composite_score: 90.1, risk_level: "critique", primary_pattern: "travail_enfant_fabrique_allumettes_sivakasi", estimated_matchstick_child_labor_rights_index: 9.01, last_updated: "2026-06-22" },
    { id: "MCLR-002", name: "Bangladesh Match Industries", country: "Bangladesh", composite_score: 85.6, risk_level: "critique", primary_pattern: "exposition_phosphore_enfants_moins_12ans", estimated_matchstick_child_labor_rights_index: 8.56, last_updated: "2026-06-22" },
    { id: "MCLR-003", name: "Java Match Co.", country: "Indonésie", composite_score: 80.4, risk_level: "critique", primary_pattern: "travail_nuit_mineur_usine_chimique", estimated_matchstick_child_labor_rights_index: 8.04, last_updated: "2026-06-22" },
    { id: "MCLR-004", name: "Pakistan Match Factory Network", country: "Pakistan", composite_score: 75.2, risk_level: "critique", primary_pattern: "enfants_travaillant_sans_protection_chimique", estimated_matchstick_child_labor_rights_index: 7.52, last_updated: "2026-06-22" },
    { id: "MCLR-005", name: "Ansell Safety Matches", country: "Suède", composite_score: 52.3, risk_level: "élevé", primary_pattern: "sourcing_composants_pays_a_risque", estimated_matchstick_child_labor_rights_index: 5.23, last_updated: "2026-06-22" },
    { id: "MCLR-006", name: "Cheetah Match Kenya", country: "Kenya", composite_score: 47.8, risk_level: "élevé", primary_pattern: "absence_inspection_travail_usine", estimated_matchstick_child_labor_rights_index: 4.78, last_updated: "2026-06-22" },
    { id: "MCLR-007", name: "Solstickan Foundation", country: "Suède", composite_score: 26.5, risk_level: "modéré", primary_pattern: "certification_partielle_sans_travail_enfant", estimated_matchstick_child_labor_rights_index: 2.65, last_updated: "2026-06-22" },
    { id: "MCLR-008", name: "Fair Match Alliance", country: "Global", composite_score: 10.7, risk_level: "faible", primary_pattern: "production_certifiee_zero_travail_enfant", estimated_matchstick_child_labor_rights_index: 1.07, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/matchstick-child-labor-rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
