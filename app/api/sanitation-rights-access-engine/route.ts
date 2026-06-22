import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sanitation-rights-access-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Sanitation Rights Access Engine Agent",
  domain: "sanitation_rights_access",
  total_entities: 8,
  avg_composite: 61.39,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { open_defecation_public_health: 2, water_sanitation_infrastructure_gap: 3, menstrual_hygiene_management_denial: 1, gender_disability_sanitation_exclusion: 2 },
  top_risk_entities: [
    "Inde — 700M Sans Toilettes 2014, Violences Femmes Défécation Plein Air & Caste Exclusion",
    "Niger/Tchad/Burkina — Sahel 80%+ Population Sans Assainissement Amélioré & COVID Amplification",
    "Bangladesh — Bidonvilles Dhaka, 40% Latrines Partagées Insalubres & Inondations Contamination",
  ],
  critical_alerts: [
    "Inde: open_defecation_public_health",
    "Niger/Tchad/Burkina: water_sanitation_infrastructure_gap",
    "Bangladesh: water_sanitation_infrastructure_gap",
    "Éthiopie: menstrual_hygiene_management_denial",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_sanitation_rights_access_index: 6.14,
  data_sources: [
    "who_unicef_joint_monitoring_programme_water_sanitation_hygiene",
    "un_special_rapporteur_human_right_safe_drinking_water_sanitation",
    "wateraid_wash_global_progress_report_sdg6",
  ],
  entities: [
    { id: "SA-001", name: "Inde — 700M Sans Toilettes 2014, Violences Femmes Défécation Plein Air & Caste Exclusion", country: "Asie du Sud", composite_score: 92.9, open_defecation_public_health_score: 95.0, menstrual_hygiene_management_denial_score: 92.0, water_sanitation_infrastructure_gap_score: 92.0, gender_disability_sanitation_exclusion_score: 92.0, risk_level: "critique", primary_pattern: "open_defecation_public_health", estimated_sanitation_rights_access_index: 9.29, last_updated: "2026-06-21" },
    { id: "SA-002", name: "Niger/Tchad/Burkina — Sahel 80%+ Population Sans Assainissement Amélioré & COVID Amplification", country: "Afrique de l'Ouest", composite_score: 90.7, open_defecation_public_health_score: 92.0, menstrual_hygiene_management_denial_score: 90.0, water_sanitation_infrastructure_gap_score: 92.0, gender_disability_sanitation_exclusion_score: 88.0, risk_level: "critique", primary_pattern: "water_sanitation_infrastructure_gap", estimated_sanitation_rights_access_index: 9.07, last_updated: "2026-06-21" },
    { id: "SA-003", name: "Bangladesh — Bidonvilles Dhaka, 40% Latrines Partagées Insalubres & Inondations Contamination", country: "Asie du Sud", composite_score: 87.9, open_defecation_public_health_score: 88.0, menstrual_hygiene_management_denial_score: 88.0, water_sanitation_infrastructure_gap_score: 90.0, gender_disability_sanitation_exclusion_score: 85.0, risk_level: "critique", primary_pattern: "water_sanitation_infrastructure_gap", estimated_sanitation_rights_access_index: 8.79, last_updated: "2026-06-21" },
    { id: "SA-004", name: "Éthiopie — 40% Défécation Plein Air, Écoles Rurales Sans Toilettes Filles & Abandon Scolaire", country: "Afrique de l'Est", composite_score: 85.75, open_defecation_public_health_score: 85.0, menstrual_hygiene_management_denial_score: 88.0, water_sanitation_infrastructure_gap_score: 85.0, gender_disability_sanitation_exclusion_score: 85.0, risk_level: "critique", primary_pattern: "menstrual_hygiene_management_denial", estimated_sanitation_rights_access_index: 8.58, last_updated: "2026-06-21" },
    { id: "SA-005", name: "Philippines — Manille Bidonvilles, 30% Résidents Taudis, Choléra Endémique & Typhons", country: "Asie du Sud-Est", composite_score: 53.65, open_defecation_public_health_score: 55.0, menstrual_hygiene_management_denial_score: 52.0, water_sanitation_infrastructure_gap_score: 55.0, gender_disability_sanitation_exclusion_score: 52.0, risk_level: "élevé", primary_pattern: "open_defecation_public_health", estimated_sanitation_rights_access_index: 5.37, last_updated: "2026-06-21" },
    { id: "SA-006", name: "Brésil — Favelas Non Raccordées, Nordeste Rural 40% Sans Assainissement & Racisme Environnemental", country: "Amérique Latine", composite_score: 50.0, open_defecation_public_health_score: 50.0, menstrual_hygiene_management_denial_score: 48.0, water_sanitation_infrastructure_gap_score: 52.0, gender_disability_sanitation_exclusion_score: 50.0, risk_level: "élevé", primary_pattern: "gender_disability_sanitation_exclusion", estimated_sanitation_rights_access_index: 5.0, last_updated: "2026-06-21" },
    { id: "SA-007", name: "WaterAid/WASH — SDG 6 Monitoring, 2 Milliards Sans Assainissement Sécurisé & Rapport Global", country: "Global", composite_score: 25.85, open_defecation_public_health_score: 22.0, menstrual_hygiene_management_denial_score: 28.0, water_sanitation_infrastructure_gap_score: 25.0, gender_disability_sanitation_exclusion_score: 30.0, risk_level: "modéré", primary_pattern: "gender_disability_sanitation_exclusion", estimated_sanitation_rights_access_index: 2.59, last_updated: "2026-06-21" },
    { id: "SA-008", name: "ONU/Résolution 64/292 — Droit à l'Eau & Assainissement 2010, Rapporteur Spécial WASH", country: "Global", composite_score: 4.4, open_defecation_public_health_score: 4.0, menstrual_hygiene_management_denial_score: 5.0, water_sanitation_infrastructure_gap_score: 3.0, gender_disability_sanitation_exclusion_score: 6.0, risk_level: "faible", primary_pattern: "water_sanitation_infrastructure_gap", estimated_sanitation_rights_access_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sanitation-rights-access-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
