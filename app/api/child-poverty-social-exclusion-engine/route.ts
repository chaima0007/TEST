import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[child-poverty-social-exclusion-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Child Poverty Social Exclusion Engine Agent",
  domain: "child_poverty_social_exclusion",
  total_entities: 8,
  avg_composite: 61.41,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { healthcare_nutrition_denial: 1, material_deprivation_severity: 3, social_exclusion_stigma: 2, education_access_barrier: 2 },
  top_risk_entities: [
    "Yémen — 2.2M Enfants Malnutrition Aiguë Sévère, Guerre & Effondrement Systèmes Services",
    "RDC — 6.9M Enfants Insécurité Alimentaire Sévère, Conflits Est & Scolarisation 60%",
    "Madagascar — 92% Population Sous Seuil Pauvreté, Enfants Travailleurs & UNICEF Urgence",
  ],
  critical_alerts: [
    "Yémen: healthcare_nutrition_denial",
    "RDC: material_deprivation_severity",
    "Madagascar: material_deprivation_severity",
    "USA: social_exclusion_stigma",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_child_poverty_social_exclusion_index: 6.14,
  data_sources: [
    "unicef_state_worlds_children_poverty_exclusion_report",
    "save_the_children_global_childhood_report_deprivation",
    "un_crc_committee_general_comment_26_childrens_rights_environment",
  ],
  entities: [
    { entity_id: "CP-001", name: "Yémen — 2.2M Enfants Malnutrition Aiguë Sévère, Guerre & Effondrement Systèmes Services", country: "Moyen-Orient", composite_score: 93.25, material_deprivation_severity_score: 95.0, education_access_barrier_score: 92.0, healthcare_nutrition_denial_score: 95.0, social_exclusion_stigma_score: 90.0, risk_level: "critique", primary_pattern: "healthcare_nutrition_denial", estimated_child_poverty_social_exclusion_index: 9.33, last_updated: "2026-06-21" },
    { entity_id: "CP-002", name: "RDC — 6.9M Enfants Insécurité Alimentaire Sévère, Conflits Est & Scolarisation 60%", country: "Afrique Centrale", composite_score: 90.6, material_deprivation_severity_score: 92.0, education_access_barrier_score: 90.0, healthcare_nutrition_denial_score: 90.0, social_exclusion_stigma_score: 90.0, risk_level: "critique", primary_pattern: "material_deprivation_severity", estimated_child_poverty_social_exclusion_index: 9.06, last_updated: "2026-06-21" },
    { entity_id: "CP-003", name: "Madagascar — 92% Population Sous Seuil Pauvreté, Enfants Travailleurs & UNICEF Urgence", country: "Afrique de l'Est", composite_score: 88.6, material_deprivation_severity_score: 90.0, education_access_barrier_score: 88.0, healthcare_nutrition_denial_score: 88.0, social_exclusion_stigma_score: 88.0, risk_level: "critique", primary_pattern: "material_deprivation_severity", estimated_child_poverty_social_exclusion_index: 8.86, last_updated: "2026-06-21" },
    { entity_id: "CP-004", name: "USA — 14M Enfants Pauvreté, Race Gap Structurel, Child Tax Credit Expiré & Housing Crisis", country: "Amérique du Nord", composite_score: 84.85, material_deprivation_severity_score: 85.0, education_access_barrier_score: 85.0, healthcare_nutrition_denial_score: 82.0, social_exclusion_stigma_score: 88.0, risk_level: "critique", primary_pattern: "social_exclusion_stigma", estimated_child_poverty_social_exclusion_index: 8.49, last_updated: "2026-06-21" },
    { entity_id: "CP-005", name: "UE/Bulgarie & Roumanie — Pauvreté Enfants Roms 30%+, Ségrégation Scolaire & Garantie Enfance", country: "Europe", composite_score: 54.25, material_deprivation_severity_score: 55.0, education_access_barrier_score: 55.0, healthcare_nutrition_denial_score: 52.0, social_exclusion_stigma_score: 55.0, risk_level: "élevé", primary_pattern: "education_access_barrier", estimated_child_poverty_social_exclusion_index: 5.43, last_updated: "2026-06-21" },
    { entity_id: "CP-006", name: "UK — Pauvreté Enfants 30% Post-Austérité, Food Banks Scolaires & Two-Child Benefit Cap", country: "Europe", composite_score: 49.5, material_deprivation_severity_score: 50.0, education_access_barrier_score: 48.0, healthcare_nutrition_denial_score: 50.0, social_exclusion_stigma_score: 50.0, risk_level: "élevé", primary_pattern: "material_deprivation_severity", estimated_child_poverty_social_exclusion_index: 4.95, last_updated: "2026-06-21" },
    { entity_id: "CP-007", name: "UNICEF/Save the Children — Monitoring Pauvreté Enfants Global, Rapport & Plaidoyer ODD", country: "Global", composite_score: 25.85, material_deprivation_severity_score: 22.0, education_access_barrier_score: 28.0, healthcare_nutrition_denial_score: 25.0, social_exclusion_stigma_score: 30.0, risk_level: "modéré", primary_pattern: "education_access_barrier", estimated_child_poverty_social_exclusion_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "CP-008", name: "ONU/CRC — Art.27 Niveau de Vie Adéquat Enfant, Protocole Facultatif & Comité Droits Enfant", country: "Global", composite_score: 4.4, material_deprivation_severity_score: 4.0, education_access_barrier_score: 5.0, healthcare_nutrition_denial_score: 3.0, social_exclusion_stigma_score: 6.0, risk_level: "faible", primary_pattern: "social_exclusion_stigma", estimated_child_poverty_social_exclusion_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-poverty-social-exclusion-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
