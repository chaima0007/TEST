import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-gender-gap-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Digital Gender Gap Rights Engine Agent",
  domain: "digital_gender_gap_rights",
  total_entities: 8,
  avg_composite: 61.49,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { internet_access_gender_gap_severity: 3, online_harassment_safety_barrier: 2, digital_skills_training_exclusion_scale: 1, platform_policy_gender_bias_gap: 2 },
  top_risk_entities: [
    "Afrique Sub-Saharienne — Fracture Numérique Genre 36% Moins Femmes En Ligne & Zéro Formation Digitale",
    "Asie du Sud — 67% Femmes Sans Internet, Harcèlement Mobile & Normes Patriarcales Numériques",
    "Moyen-Orient — Contrôle Masculin Accès Web, Surveillance Digitale Femmes & Censure Contenu Féminin",
  ],
  critical_alerts: [
    "Afrique Sub-Saharienne : internet_access_gender_gap_severity",
    "Asie du Sud : internet_access_gender_gap_severity",
    "Moyen-Orient : online_harassment_safety_barrier",
    "Asie du Sud-Est : digital_skills_training_exclusion_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_digital_gender_gap_rights_index: 6.15,
  data_sources: [
    "itu_measuring_digital_development_gender_gap_report",
    "web_foundation_womens_rights_online_access_barriers_study",
    "plan_international_online_safety_girls_harassment_report",
  ],
  entities: [
    { entity_id: "DGG-001", name: "Afrique Sub-Saharienne — Fracture Numérique Genre 36% Moins Femmes En Ligne & Zéro Formation Digitale", country: "Afrique Sub-Saharienne", composite_score: 92.55, internet_access_gender_gap_severity_score: 96.0, digital_skills_training_exclusion_scale_score: 92.0, online_harassment_safety_barrier_score: 91.0, platform_policy_gender_bias_gap_score: 90.0, risk_level: "critique", primary_pattern: "internet_access_gender_gap_severity", estimated_digital_gender_gap_rights_index: 9.26, last_updated: "2026-06-21" },
    { entity_id: "DGG-002", name: "Asie du Sud — 67% Femmes Sans Internet, Harcèlement Mobile & Normes Patriarcales Numériques", country: "Asie du Sud", composite_score: 90.25, internet_access_gender_gap_severity_score: 93.0, digital_skills_training_exclusion_scale_score: 89.0, online_harassment_safety_barrier_score: 90.0, platform_policy_gender_bias_gap_score: 88.0, risk_level: "critique", primary_pattern: "internet_access_gender_gap_severity", estimated_digital_gender_gap_rights_index: 9.03, last_updated: "2026-06-21" },
    { entity_id: "DGG-003", name: "Moyen-Orient — Contrôle Masculin Accès Web, Surveillance Digitale Femmes & Censure Contenu Féminin", country: "Moyen-Orient", composite_score: 88.25, internet_access_gender_gap_severity_score: 91.0, digital_skills_training_exclusion_scale_score: 87.0, online_harassment_safety_barrier_score: 88.0, platform_policy_gender_bias_gap_score: 86.0, risk_level: "critique", primary_pattern: "online_harassment_safety_barrier", estimated_digital_gender_gap_rights_index: 8.83, last_updated: "2026-06-21" },
    { entity_id: "DGG-004", name: "Asie du Sud-Est — Harcèlement En Ligne Systémique, Exclusion STEM & Biais Algorithmes Emploi", country: "Asie du Sud-Est", composite_score: 85.3, internet_access_gender_gap_severity_score: 88.0, digital_skills_training_exclusion_scale_score: 84.0, online_harassment_safety_barrier_score: 86.0, platform_policy_gender_bias_gap_score: 82.0, risk_level: "critique", primary_pattern: "digital_skills_training_exclusion_scale", estimated_digital_gender_gap_rights_index: 8.53, last_updated: "2026-06-21" },
    { entity_id: "DGG-005", name: "Amérique Latine — Violence Numérique Genrée, Deepfakes Non Consensuels & Impunité Plateformes", country: "Amérique Latine", composite_score: 53.0, internet_access_gender_gap_severity_score: 55.0, digital_skills_training_exclusion_scale_score: 52.0, online_harassment_safety_barrier_score: 54.0, platform_policy_gender_bias_gap_score: 50.0, risk_level: "élevé", primary_pattern: "online_harassment_safety_barrier", estimated_digital_gender_gap_rights_index: 5.3, last_updated: "2026-06-21" },
    { entity_id: "DGG-006", name: "Europe de l'Est — Sous-Représentation Tech Femmes, Harcèlement Politique En Ligne & Gender Pay Gap IA", country: "Europe de l'Est", composite_score: 51.75, internet_access_gender_gap_severity_score: 54.0, digital_skills_training_exclusion_scale_score: 51.0, online_harassment_safety_barrier_score: 52.0, platform_policy_gender_bias_gap_score: 49.0, risk_level: "élevé", primary_pattern: "platform_policy_gender_bias_gap", estimated_digital_gender_gap_rights_index: 5.18, last_updated: "2026-06-21" },
    { entity_id: "DGG-007", name: "Alliance4AI/Web Foundation — Droits Femmes En Ligne, Formation Digitale & Plaidoyer Plateformes", country: "Global", composite_score: 26.35, internet_access_gender_gap_severity_score: 22.0, digital_skills_training_exclusion_scale_score: 28.0, online_harassment_safety_barrier_score: 27.0, platform_policy_gender_bias_gap_score: 30.0, risk_level: "modéré", primary_pattern: "platform_policy_gender_bias_gap", estimated_digital_gender_gap_rights_index: 2.64, last_updated: "2026-06-21" },
    { entity_id: "DGG-008", name: "ONU/ITU — Rapport Genre Numérique, SDG 5.b Accès TIC & Recommandations Politiques Inclusives", country: "Global", composite_score: 4.45, internet_access_gender_gap_severity_score: 4.0, digital_skills_training_exclusion_scale_score: 5.0, online_harassment_safety_barrier_score: 4.0, platform_policy_gender_bias_gap_score: 5.0, risk_level: "faible", primary_pattern: "internet_access_gender_gap_severity", estimated_digital_gender_gap_rights_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-gender-gap-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
