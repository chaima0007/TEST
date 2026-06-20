import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[prison-labor-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Prison Labor Engine Agent",
  domain: "prison_labor",
  total_entities: 8,
  avg_composite: 61.24,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { legal_protection_absence: 2, coercion_punishment: 2, below_minimum_wage: 2, forced_labor_scale: 2 },
  top_risk_entities: [
    "USA — 1.2M Prisonniers Travaillant, Clause 13e Amendement & Corporations Prison-Industrie",
    "Chine/Laogai — 1.2M Détenus Ouïghours, Système Laogai & Travail Forcé Politique",
    "Corée du Nord — Kwan-li-so, Colonies Pénitentiaires & Production Export Forcé",
  ],
  critical_alerts: [
    "USA: legal_protection_absence",
    "Chine/Laogai: coercion_punishment",
    "Corée du Nord: below_minimum_wage",
    "Russie: forced_labor_scale",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_prison_labor_index: 6.12,
  data_sources: [
    "american_civil_liberties_union_captive_labor_exploitation_prison_industries_report",
    "ilo_hard_to_see_harder_to_count_survey_guidelines_forced_labour_prisons",
    "un_subcommittee_prevention_torture_annual_report_detention_labor",
  ],
  entities: [
    { entity_id: "PL-001", name: "USA — 1.2M Prisonniers Travaillant, Clause 13e Amendement & Corporations Prison-Industrie", country: "Amérique du Nord", composite_score: 91.35, forced_labor_scale_score: 92.0, below_minimum_wage_score: 95.0, coercion_punishment_score: 88.0, legal_protection_absence_score: 90.0, risk_level: "critique", primary_pattern: "legal_protection_absence", estimated_prison_labor_index: 9.14, last_updated: "2026-06-20" },
    { entity_id: "PL-002", name: "Chine/Laogai — 1.2M Détenus Ouïghours, Système Laogai & Travail Forcé Politique", country: "Asie du Nord-Est", composite_score: 91.35, forced_labor_scale_score: 90.0, below_minimum_wage_score: 92.0, coercion_punishment_score: 95.0, legal_protection_absence_score: 88.0, risk_level: "critique", primary_pattern: "coercion_punishment", estimated_prison_labor_index: 9.14, last_updated: "2026-06-20" },
    { entity_id: "PL-003", name: "Corée du Nord — Kwan-li-so, Colonies Pénitentiaires & Production Export Forcé", country: "Asie du Nord-Est", composite_score: 89.0, forced_labor_scale_score: 90.0, below_minimum_wage_score: 88.0, coercion_punishment_score: 92.0, legal_protection_absence_score: 85.0, risk_level: "critique", primary_pattern: "below_minimum_wage", estimated_prison_labor_index: 8.9, last_updated: "2026-06-20" },
    { entity_id: "PL-004", name: "Russie — Colonies Pénitentiaires IK, Travail Forcé État & Entreprises Russes Contrats", country: "Europe de l'Est", composite_score: 81.35, forced_labor_scale_score: 82.0, below_minimum_wage_score: 78.0, coercion_punishment_score: 85.0, legal_protection_absence_score: 80.0, risk_level: "critique", primary_pattern: "forced_labor_scale", estimated_prison_labor_index: 8.14, last_updated: "2026-06-20" },
    { entity_id: "PL-005", name: "Thaïlande/Myanmar — Migrants Détenus, Centres Rétention & Travail Forcé Non Payé", country: "Asie du Sud-Est", composite_score: 53.85, forced_labor_scale_score: 52.0, below_minimum_wage_score: 55.0, coercion_punishment_score: 58.0, legal_protection_absence_score: 50.0, risk_level: "élevé", primary_pattern: "forced_labor_scale", estimated_prison_labor_index: 5.39, last_updated: "2026-06-20" },
    { entity_id: "PL-006", name: "Brésil/Mexique — Travail Carcéral Sous-Payé, Maquiladoras Prison & Réductions Peine", country: "Amérique Latine", composite_score: 51.15, forced_labor_scale_score: 48.0, below_minimum_wage_score: 52.0, coercion_punishment_score: 55.0, legal_protection_absence_score: 50.0, risk_level: "élevé", primary_pattern: "below_minimum_wage", estimated_prison_labor_index: 5.12, last_updated: "2026-06-20" },
    { entity_id: "PL-007", name: "UE — Travail Carcéral Légalisé, Rémunération Inégale & Standards Minimum Disparates", country: "Europe", composite_score: 27.5, forced_labor_scale_score: 22.0, below_minimum_wage_score: 30.0, coercion_punishment_score: 28.0, legal_protection_absence_score: 32.0, risk_level: "modéré", primary_pattern: "legal_protection_absence", estimated_prison_labor_index: 2.75, last_updated: "2026-06-20" },
    { entity_id: "PL-008", name: "ONU/OIT/OPCAT — Convention 29, Mécanismes Nationaux Prévention & Standards Travail Détenu", country: "Global", composite_score: 4.4, forced_labor_scale_score: 4.0, below_minimum_wage_score: 5.0, coercion_punishment_score: 3.0, legal_protection_absence_score: 6.0, risk_level: "faible", primary_pattern: "coercion_punishment", estimated_prison_labor_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/prison-labor-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
