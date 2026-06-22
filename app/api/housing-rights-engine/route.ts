import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[housing-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Housing Rights Engine Agent",
  domain: "housing_rights",
  total_entities: 8,
  avg_composite: 60.89,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { forced_eviction_displacement_severity: 3, housing_discrimination_marginalized: 1, rent_speculation_financialization_gap: 3, homelessness_inadequate_housing_scale: 1 },
  top_risk_entities: [
    "Kenya/Nairobi — Kibera 700k Habitants Bidonvilles, Expulsions Bulldozer Sans Préavis & Zéro Relogement",
    "Philippines — 3,1M Sans Abri Manille, Expulsions Duterte Drug War & Bidonvilles Inondables",
    "India — 5M Expulsés Projets Infra/Jeux, DUSIB Delhi Démolitions & Dalits/Tribaux Ciblés",
  ],
  critical_alerts: [
    "Kenya/Nairobi: forced_eviction_displacement_severity",
    "Philippines: forced_eviction_displacement_severity",
    "India: housing_discrimination_marginalized",
    "Brazil/Rio: rent_speculation_financialization_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_housing_rights_index: 6.09,
  data_sources: [
    "cohre_forced_evictions_violations_human_rights_report",
    "un_habitat_world_cities_report_2022",
    "pidesc_committee_general_comment_4_adequate_housing",
  ],
  entities: [
    { id: "HR-001", name: "Kenya/Nairobi — Kibera 700k Habitants Bidonvilles, Expulsions Bulldozer Sans Préavis & Zéro Relogement", country: "Kenya", composite_score: 92.95, forced_eviction_displacement_severity_score: 95.0, homelessness_inadequate_housing_scale_score: 92.0, housing_discrimination_marginalized_score: 93.0, rent_speculation_financialization_gap_score: 91.0, risk_level: "critique", primary_pattern: "forced_eviction_displacement_severity", estimated_housing_rights_index: 9.3, last_updated: "2026-06-21" },
    { id: "HR-002", name: "Philippines — 3,1M Sans Abri Manille, Expulsions Duterte Drug War & Bidonvilles Inondables", country: "Philippines", composite_score: 89.75, forced_eviction_displacement_severity_score: 92.0, homelessness_inadequate_housing_scale_score: 89.0, housing_discrimination_marginalized_score: 90.0, rent_speculation_financialization_gap_score: 87.0, risk_level: "critique", primary_pattern: "forced_eviction_displacement_severity", estimated_housing_rights_index: 8.98, last_updated: "2026-06-21" },
    { id: "HR-003", name: "India — 5M Expulsés Projets Infra/Jeux, DUSIB Delhi Démolitions & Dalits/Tribaux Ciblés", country: "Inde", composite_score: 86.75, forced_eviction_displacement_severity_score: 89.0, homelessness_inadequate_housing_scale_score: 86.0, housing_discrimination_marginalized_score: 87.0, rent_speculation_financialization_gap_score: 84.0, risk_level: "critique", primary_pattern: "housing_discrimination_marginalized", estimated_housing_rights_index: 8.68, last_updated: "2026-06-21" },
    { id: "HR-004", name: "Brazil/Rio — Favelas Pacification Expulsions Forcées, Spéculation Immobilière & Gentrification Olympique", country: "Brésil", composite_score: 83.95, forced_eviction_displacement_severity_score: 86.0, homelessness_inadequate_housing_scale_score: 83.0, housing_discrimination_marginalized_score: 84.0, rent_speculation_financialization_gap_score: 82.0, risk_level: "critique", primary_pattern: "rent_speculation_financialization_gap", estimated_housing_rights_index: 8.4, last_updated: "2026-06-21" },
    { id: "HR-005", name: "USA — 650k Sans Abri, Sweeps Campements & Criminalization Homelessness Anti-Camping Laws", country: "USA", composite_score: 52.95, forced_eviction_displacement_severity_score: 55.0, homelessness_inadequate_housing_scale_score: 53.0, housing_discrimination_marginalized_score: 52.0, rent_speculation_financialization_gap_score: 51.0, risk_level: "élevé", primary_pattern: "homelessness_inadequate_housing_scale", estimated_housing_rights_index: 5.3, last_updated: "2026-06-21" },
    { id: "HR-006", name: "Western Europe — Crise Logement Amsterdam/London/Paris, Airbnb Speculation & Familles Expulsées", country: "Europe Occidentale", composite_score: 50.95, forced_eviction_displacement_severity_score: 53.0, homelessness_inadequate_housing_scale_score: 50.0, housing_discrimination_marginalized_score: 51.0, rent_speculation_financialization_gap_score: 49.0, risk_level: "élevé", primary_pattern: "rent_speculation_financialization_gap", estimated_housing_rights_index: 5.1, last_updated: "2026-06-21" },
    { id: "HR-007", name: "COHRE/HIC — Centre Droit Logement Expulsions, Plaidoyer Droit Logement & Standards PIDESC", country: "Global", composite_score: 25.65, forced_eviction_displacement_severity_score: 27.0, homelessness_inadequate_housing_scale_score: 25.0, housing_discrimination_marginalized_score: 26.0, rent_speculation_financialization_gap_score: 24.0, risk_level: "modéré", primary_pattern: "forced_eviction_displacement_severity", estimated_housing_rights_index: 2.57, last_updated: "2026-06-21" },
    { id: "HR-008", name: "ONU/PIDESC — Article 11 Droit Logement Convenable, Rapporteur Logement & SDG 11.1", country: "Global", composite_score: 4.2, forced_eviction_displacement_severity_score: 4.0, homelessness_inadequate_housing_scale_score: 4.0, housing_discrimination_marginalized_score: 4.0, rent_speculation_financialization_gap_score: 5.0, risk_level: "faible", primary_pattern: "rent_speculation_financialization_gap", estimated_housing_rights_index: 0.42, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/housing-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
