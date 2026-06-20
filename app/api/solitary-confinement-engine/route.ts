import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[solitary-confinement-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Solitary Confinement Engine Agent",
  domain: "solitary_confinement",
  total_entities: 8,
  avg_composite: 59.39,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { isolation_duration_scale: 3, psychological_harm: 2, juvenile_elderly_application: 2, international_prohibition_gap: 1 },
  top_risk_entities: [
    "USA — Supermax ADX, 80 000 Détenus Isolement Prolongé & Placements SHU Indéfinis",
    "Russie — Shizo/PKT, Isolement Politique, Opposants Navalny & Violation Règles Mandela",
    "Chine — Cellules Spéciales Laogai, Isolement Ouïghours & Détention Incommunicado",
  ],
  critical_alerts: [
    "USA: isolation_duration_scale",
    "Russie: psychological_harm",
    "Chine: isolation_duration_scale",
    "Iran: juvenile_elderly_application",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_solitary_confinement_index: 5.94,
  data_sources: [
    "solitary_watch_supermax_isolation_global_report_annual",
    "un_subcommittee_prevention_torture_solitary_confinement_report",
    "mandela_rules_un_standard_minimum_treatment_prisoners_2015",
  ],
  entities: [
    { entity_id: "SC-001", name: "USA — Supermax ADX, 80 000 Détenus Isolement Prolongé & Placements SHU Indéfinis", country: "Amérique du Nord", composite_score: 89.1, isolation_duration_scale_score: 92.0, psychological_harm_score: 88.0, juvenile_elderly_application_score: 90.0, international_prohibition_gap_score: 85.0, risk_level: "critique", primary_pattern: "isolation_duration_scale", estimated_solitary_confinement_index: 8.91, last_updated: "2026-06-20" },
    { entity_id: "SC-002", name: "Russie — Shizo/PKT, Isolement Politique, Opposants Navalny & Violation Règles Mandela", country: "Europe de l'Est", composite_score: 85.15, isolation_duration_scale_score: 85.0, psychological_harm_score: 88.0, juvenile_elderly_application_score: 85.0, international_prohibition_gap_score: 82.0, risk_level: "critique", primary_pattern: "psychological_harm", estimated_solitary_confinement_index: 8.52, last_updated: "2026-06-20" },
    { entity_id: "SC-003", name: "Chine — Cellules Spéciales Laogai, Isolement Ouïghours & Détention Incommunicado", country: "Asie du Nord-Est", composite_score: 84.15, isolation_duration_scale_score: 88.0, psychological_harm_score: 85.0, juvenile_elderly_application_score: 82.0, international_prohibition_gap_score: 80.0, risk_level: "critique", primary_pattern: "isolation_duration_scale", estimated_solitary_confinement_index: 8.42, last_updated: "2026-06-20" },
    { entity_id: "SC-004", name: "Iran — Evin Section 209, Prisonniers Politiques Isolés des Années & Torture Psychologique", country: "Moyen-Orient", composite_score: 81.35, isolation_duration_scale_score: 80.0, psychological_harm_score: 82.0, juvenile_elderly_application_score: 85.0, international_prohibition_gap_score: 78.0, risk_level: "critique", primary_pattern: "juvenile_elderly_application", estimated_solitary_confinement_index: 8.14, last_updated: "2026-06-20" },
    { entity_id: "SC-005", name: "Égypte — Isolement Longue Durée, Prisonniers Politiques & Absence Contrôle Judiciaire", country: "Afrique du Nord", composite_score: 53.45, isolation_duration_scale_score: 52.0, psychological_harm_score: 55.0, juvenile_elderly_application_score: 50.0, international_prohibition_gap_score: 58.0, risk_level: "élevé", primary_pattern: "international_prohibition_gap", estimated_solitary_confinement_index: 5.35, last_updated: "2026-06-20" },
    { entity_id: "SC-006", name: "Mexique — Aislamiento en Cárceles Fédérales, Cartels & Absence Réforme Pénitentiaire", country: "Amérique Centrale", composite_score: 51.15, isolation_duration_scale_score: 48.0, psychological_harm_score: 52.0, juvenile_elderly_application_score: 55.0, international_prohibition_gap_score: 50.0, risk_level: "élevé", primary_pattern: "juvenile_elderly_application", estimated_solitary_confinement_index: 5.12, last_updated: "2026-06-20" },
    { entity_id: "SC-007", name: "UE/Danemark — Réforme Progressive, Limite 4 Semaines & Interdiction Mineurs", country: "Europe", composite_score: 26.4, isolation_duration_scale_score: 25.0, psychological_harm_score: 30.0, juvenile_elderly_application_score: 28.0, international_prohibition_gap_score: 22.0, risk_level: "modéré", primary_pattern: "psychological_harm", estimated_solitary_confinement_index: 2.64, last_updated: "2026-06-20" },
    { entity_id: "SC-008", name: "ONU/Règles Mandela — Art. 43-44, Interdiction Isolement Prolongé +15 Jours & Monitoring", country: "Global", composite_score: 4.4, isolation_duration_scale_score: 4.0, psychological_harm_score: 5.0, juvenile_elderly_application_score: 3.0, international_prohibition_gap_score: 6.0, risk_level: "faible", primary_pattern: "isolation_duration_scale", estimated_solitary_confinement_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/solitary-confinement-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
