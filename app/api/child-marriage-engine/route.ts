import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[child-marriage-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Child Marriage Engine Agent",
  domain: "child_marriage",
  total_entities: 8,
  avg_composite: 59.71,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { prevalence_underage_unions: 2, health_maternal_mortality: 2, girls_education_dropout: 2, legal_enforcement_gap: 2 },
  top_risk_entities: [
    "Niger — 76% Filles Mariées Avant 18 Ans, Taux Mondial le Plus Élevé & Fistules Obstétricales",
    "Bangladesh — 59% Filles Mariées Avant 18 Ans, Exception Légale & Violences Conjugales",
    "Mali — 52% Filles Mariées Avant 18 Ans, Mariages Forcés Sahel & Abandon Scolaire Massif",
  ],
  critical_alerts: [
    "Niger: prevalence_underage_unions",
    "Bangladesh: health_maternal_mortality",
    "Mali: girls_education_dropout",
    "Inde: legal_enforcement_gap",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_child_marriage_index: 5.97,
  data_sources: [
    "unicef_girls_not_brides_global_child_marriage_data_portal",
    "save_the_children_too_young_to_wed_global_report",
    "un_women_child_early_forced_marriage_prevention_framework",
  ],
  entities: [
    { entity_id: "CM-001", name: "Niger — 76% Filles Mariées Avant 18 Ans, Taux Mondial le Plus Élevé & Fistules Obstétricales", country: "Afrique de l'Ouest", composite_score: 91.6, prevalence_underage_unions_score: 95.0, girls_education_dropout_score: 90.0, health_maternal_mortality_score: 92.0, legal_enforcement_gap_score: 88.0, risk_level: "critique", primary_pattern: "prevalence_underage_unions", estimated_child_marriage_index: 9.16, last_updated: "2026-06-20" },
    { entity_id: "CM-002", name: "Bangladesh — 59% Filles Mariées Avant 18 Ans, Exception Légale & Violences Conjugales", country: "Asie du Sud", composite_score: 86.65, prevalence_underage_unions_score: 88.0, girls_education_dropout_score: 85.0, health_maternal_mortality_score: 88.0, legal_enforcement_gap_score: 85.0, risk_level: "critique", primary_pattern: "health_maternal_mortality", estimated_child_marriage_index: 8.67, last_updated: "2026-06-20" },
    { entity_id: "CM-003", name: "Mali — 52% Filles Mariées Avant 18 Ans, Mariages Forcés Sahel & Abandon Scolaire Massif", country: "Afrique de l'Ouest", composite_score: 84.0, prevalence_underage_unions_score: 85.0, girls_education_dropout_score: 88.0, health_maternal_mortality_score: 82.0, legal_enforcement_gap_score: 80.0, risk_level: "critique", primary_pattern: "girls_education_dropout", estimated_child_marriage_index: 8.4, last_updated: "2026-06-20" },
    { entity_id: "CM-004", name: "Inde — 27% Filles Mariées Avant 18 Ans, 15M Mariages Enfants/An & Application Loi Défaillante", country: "Asie du Sud", composite_score: 80.4, prevalence_underage_unions_score: 80.0, girls_education_dropout_score: 82.0, health_maternal_mortality_score: 78.0, legal_enforcement_gap_score: 82.0, risk_level: "critique", primary_pattern: "legal_enforcement_gap", estimated_child_marriage_index: 8.04, last_updated: "2026-06-20" },
    { entity_id: "CM-005", name: "Éthiopie — 40% Filles Mariées Avant 18 Ans, Régions Rurales Isolées & Pauvreté Structurelle", country: "Afrique de l'Est", composite_score: 53.85, prevalence_underage_unions_score: 52.0, girls_education_dropout_score: 55.0, health_maternal_mortality_score: 58.0, legal_enforcement_gap_score: 50.0, risk_level: "élevé", primary_pattern: "health_maternal_mortality", estimated_child_marriage_index: 5.39, last_updated: "2026-06-20" },
    { entity_id: "CM-006", name: "Proche-Orient/Réfugiés Syriens — Mariages Précoces Camps Jordanie/Liban & Vulnérabilité", country: "Moyen-Orient", composite_score: 50.9, prevalence_underage_unions_score: 48.0, girls_education_dropout_score: 52.0, health_maternal_mortality_score: 50.0, legal_enforcement_gap_score: 55.0, risk_level: "élevé", primary_pattern: "legal_enforcement_gap", estimated_child_marriage_index: 5.09, last_updated: "2026-06-20" },
    { entity_id: "CM-007", name: "ONU/UNICEF Girls Not Brides — Alliance Mondiale 1500 ONG, Plaidoyer & Programmes Éducation", country: "Global", composite_score: 25.85, prevalence_underage_unions_score: 22.0, girls_education_dropout_score: 28.0, health_maternal_mortality_score: 25.0, legal_enforcement_gap_score: 30.0, risk_level: "modéré", primary_pattern: "girls_education_dropout", estimated_child_marriage_index: 2.59, last_updated: "2026-06-20" },
    { entity_id: "CM-008", name: "ONU/CEDAW — Convention Élimination Discrimination Femmes, Art.16 Mariage Enfants & Suivi", country: "Global", composite_score: 4.4, prevalence_underage_unions_score: 4.0, girls_education_dropout_score: 5.0, health_maternal_mortality_score: 3.0, legal_enforcement_gap_score: 6.0, risk_level: "faible", primary_pattern: "prevalence_underage_unions", estimated_child_marriage_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-marriage-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
