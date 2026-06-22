import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[menstrual-health-education-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Menstrual Health Education Engine Agent",
  domain: "menstrual_health_education",
  total_entities: 8,
  avg_composite: 61.32,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { menstrual_taboo_exclusion_severity: 3, education_dropout_period_poverty: 2, hygiene_infrastructure_denial: 2, healthcare_menstrual_disorder_neglect: 1 },
  top_risk_entities: [
    "Népal — Chhaupadi: Exil Menstruation Cabanes, Femmes Mortes Froid/Serpents & Illégal Non Appliqué",
    "Inde/Bangladesh — 88% Filles Sans Serviettes Hygiéniques, 50% Écoles Sans Toilettes & Décrochage",
    "Kenya/Afrique Sub-Saharienne — 1/10 Filles Absente École/Règles, Échange Sexe Contre Serviettes",
  ],
  critical_alerts: [
    "Népal: menstrual_taboo_exclusion_severity",
    "Inde/Bangladesh: education_dropout_period_poverty",
    "Kenya/Afrique Sub-Saharienne: education_dropout_period_poverty",
    "Soudan/Yémen: hygiene_infrastructure_denial",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_menstrual_health_education_index: 6.13,
  data_sources: [
    "unicef_wash_menstrual_health_management_schools_global_report",
    "days_for_girls_period_poverty_mhm_global_monitoring",
    "un_women_menstrual_health_human_rights_framework_sdg6",
  ],
  entities: [
    { id: "MHE-001", name: "Népal — Chhaupadi: Exil Menstruation Cabanes, Femmes Mortes Froid/Serpents & Illégal Non Appliqué", country: "Asie du Sud", composite_score: 91.1, menstrual_taboo_exclusion_severity_score: 95.0, education_dropout_period_poverty_score: 90.0, hygiene_infrastructure_denial_score: 90.0, healthcare_menstrual_disorder_neglect_score: 88.0, risk_level: "critique", primary_pattern: "menstrual_taboo_exclusion_severity", estimated_menstrual_health_education_index: 9.11, last_updated: "2026-06-21" },
    { id: "MHE-002", name: "Inde/Bangladesh — 88% Filles Sans Serviettes Hygiéniques, 50% Écoles Sans Toilettes & Décrochage", country: "Asie du Sud", composite_score: 90.75, menstrual_taboo_exclusion_severity_score: 88.0, education_dropout_period_poverty_score: 95.0, hygiene_infrastructure_denial_score: 92.0, healthcare_menstrual_disorder_neglect_score: 88.0, risk_level: "critique", primary_pattern: "education_dropout_period_poverty", estimated_menstrual_health_education_index: 9.08, last_updated: "2026-06-21" },
    { id: "MHE-003", name: "Kenya/Afrique Sub-Saharienne — 1/10 Filles Absente École/Règles, Échange Sexe Contre Serviettes", country: "Afrique de l'Est", composite_score: 88.5, menstrual_taboo_exclusion_severity_score: 88.0, education_dropout_period_poverty_score: 90.0, hygiene_infrastructure_denial_score: 88.0, healthcare_menstrual_disorder_neglect_score: 88.0, risk_level: "critique", primary_pattern: "education_dropout_period_poverty", estimated_menstrual_health_education_index: 8.85, last_updated: "2026-06-21" },
    { id: "MHE-004", name: "Soudan/Yémen — Conflits Interrompent MHM, Camps Réfugiées Sans Sanitaires & Dignité Absente", country: "Moyen-Orient/Afrique", composite_score: 86.45, menstrual_taboo_exclusion_severity_score: 82.0, education_dropout_period_poverty_score: 85.0, hygiene_infrastructure_denial_score: 92.0, healthcare_menstrual_disorder_neglect_score: 88.0, risk_level: "critique", primary_pattern: "hygiene_infrastructure_denial", estimated_menstrual_health_education_index: 8.65, last_updated: "2026-06-21" },
    { id: "MHE-005", name: "Guatemala/Mexique Indigène — Tabous Culturels Menstruation, Exclusion Rituelle & Honte Institutionnelle", country: "Amérique Latine", composite_score: 52.5, menstrual_taboo_exclusion_severity_score: 55.0, education_dropout_period_poverty_score: 52.0, hygiene_infrastructure_denial_score: 52.0, healthcare_menstrual_disorder_neglect_score: 50.0, risk_level: "élevé", primary_pattern: "menstrual_taboo_exclusion_severity", estimated_menstrual_health_education_index: 5.25, last_updated: "2026-06-21" },
    { id: "MHE-006", name: "Pakistan — Filles Abandonnent École Dès 1ères Règles, 50% Femmes Croient Menstruation Impure", country: "Asie du Sud", composite_score: 51.0, menstrual_taboo_exclusion_severity_score: 55.0, education_dropout_period_poverty_score: 50.0, hygiene_infrastructure_denial_score: 48.0, healthcare_menstrual_disorder_neglect_score: 50.0, risk_level: "élevé", primary_pattern: "healthcare_menstrual_disorder_neglect", estimated_menstrual_health_education_index: 5.1, last_updated: "2026-06-21" },
    { id: "MHE-007", name: "Days for Girls/WASH NGO — Kits MHM, Éducation Menstruelle, Plaidoyer ODD 6.2 & Genre", country: "Global", composite_score: 25.85, menstrual_taboo_exclusion_severity_score: 22.0, education_dropout_period_poverty_score: 28.0, hygiene_infrastructure_denial_score: 25.0, healthcare_menstrual_disorder_neglect_score: 30.0, risk_level: "modéré", primary_pattern: "hygiene_infrastructure_denial", estimated_menstrual_health_education_index: 2.59, last_updated: "2026-06-21" },
    { id: "MHE-008", name: "ONU Femmes/UNICEF — Politique MHM Globale, SDG 6.2 Genre-Sensitive WASH & Rapport 2023", country: "Global", composite_score: 4.4, menstrual_taboo_exclusion_severity_score: 4.0, education_dropout_period_poverty_score: 5.0, hygiene_infrastructure_denial_score: 3.0, healthcare_menstrual_disorder_neglect_score: 6.0, risk_level: "faible", primary_pattern: "menstrual_taboo_exclusion_severity", estimated_menstrual_health_education_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/menstrual-health-education-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
