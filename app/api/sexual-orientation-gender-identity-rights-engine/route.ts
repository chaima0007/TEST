import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sexual-orientation-gender-identity-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Sexual Orientation Gender Identity Rights Engine Agent",
  domain: "sexual_orientation_gender_identity_rights",
  total_entities: 8,
  avg_composite: 62.19,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: { criminalization_legal_penalty_severity: 2, state_sanctioned_violence_impunity: 2, legal_protection_recognition_gap: 2, social_discrimination_hate_crime_exposure: 2 },
  top_risk_entities: [
    "Ouganda/Anti-Homosexuality Act 2023 Peine Mort — Aggravated Homosexuality, ONG Fermées, Exils Massifs",
    "Iran/Exécutions LGBTQ+ Légales — 100-200 Exécutions Annuelles, Article 237 Code Pénal, Pendaisons Publiques",
    "Tchétchénie/Camps Disparitions — Camps Secrets Hommes Présumés Gay, Torture & Meurtres Familiaux Honte",
  ],
  critical_alerts: [
    "Ouganda/Anti-Homosexuality Act 2023 Peine Mort: criminalization_legal_penalty_severity",
    "Iran/Exécutions LGBTQ+ Légales: state_sanctioned_violence_impunity",
    "Tchétchénie/Camps Disparitions: state_sanctioned_violence_impunity",
    "Russie/Loi Propagande LGBTQ Universelle: legal_protection_recognition_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_sogi_rights_index: 6.22,
  data_sources: [
    "ilga_world_state_sponsored_homophobia_report_2023",
    "human_rights_watch_chechen_lgbtq_persecution_camps",
    "amnesty_international_iran_lgbtq_executions_criminalization",
    "outright_international_sogi_rights_global_tracker",
  ],
  entities: [
    { id: "SGI-001", name: "Ouganda/Anti-Homosexuality Act 2023 Peine Mort — Aggravated Homosexuality, ONG Fermées, Exils Massifs", country: "Ouganda", composite_score: 95.55, criminalization_legal_penalty_severity_score: 97.0, state_sanctioned_violence_impunity_score: 94.0, social_discrimination_hate_crime_exposure_score: 95.0, legal_protection_recognition_gap_score: 96.0, risk_level: "critique", primary_pattern: "criminalization_legal_penalty_severity", estimated_sogi_rights_index: 9.56, last_updated: "2026-06-21" },
    { id: "SGI-002", name: "Iran/Exécutions LGBTQ+ Légales — 100-200 Exécutions Annuelles, Article 237 Code Pénal, Pendaisons Publiques", country: "Iran", composite_score: 94.8, criminalization_legal_penalty_severity_score: 95.0, state_sanctioned_violence_impunity_score: 97.0, social_discrimination_hate_crime_exposure_score: 93.0, legal_protection_recognition_gap_score: 94.0, risk_level: "critique", primary_pattern: "state_sanctioned_violence_impunity", estimated_sogi_rights_index: 9.48, last_updated: "2026-06-21" },
    { id: "SGI-003", name: "Russie/Loi Propagande LGBTQ Universelle — Interdiction Totale Toute Expression, Amendes & Arrestations ONG", country: "Russie", composite_score: 79.7, criminalization_legal_penalty_severity_score: 78.0, state_sanctioned_violence_impunity_score: 76.0, social_discrimination_hate_crime_exposure_score: 82.0, legal_protection_recognition_gap_score: 84.0, risk_level: "critique", primary_pattern: "legal_protection_recognition_gap", estimated_sogi_rights_index: 7.97, last_updated: "2026-06-21" },
    { id: "SGI-004", name: "Tchétchénie/Camps Disparitions — Camps Secrets Hommes Présumés Gay, Torture & Meurtres Familiaux Honte", country: "Russie/Tchétchénie", composite_score: 93.6, criminalization_legal_penalty_severity_score: 93.0, state_sanctioned_violence_impunity_score: 96.0, social_discrimination_hate_crime_exposure_score: 94.0, legal_protection_recognition_gap_score: 91.0, risk_level: "critique", primary_pattern: "state_sanctioned_violence_impunity", estimated_sogi_rights_index: 9.36, last_updated: "2026-06-21" },
    { id: "SGI-005", name: "Hongrie/Anti-Trans Loi Constitution — Interdiction Changement Sexe Légal 2020, Éducation LGBTQ Censurée", country: "Hongrie", composite_score: 56.4, criminalization_legal_penalty_severity_score: 55.0, state_sanctioned_violence_impunity_score: 52.0, social_discrimination_hate_crime_exposure_score: 58.0, legal_protection_recognition_gap_score: 62.0, risk_level: "élevé", primary_pattern: "legal_protection_recognition_gap", estimated_sogi_rights_index: 5.64, last_updated: "2026-06-21" },
    { id: "SGI-006", name: "Jamaïque/Buggery Law Violence — 10 Ans Emprisonnement, Lynchages Communautaires, Fuites Vers Amérique", country: "Jamaïque", composite_score: 51.35, criminalization_legal_penalty_severity_score: 52.0, state_sanctioned_violence_impunity_score: 48.0, social_discrimination_hate_crime_exposure_score: 55.0, legal_protection_recognition_gap_score: 50.0, risk_level: "élevé", primary_pattern: "social_discrimination_hate_crime_exposure", estimated_sogi_rights_index: 5.14, last_updated: "2026-06-21" },
    { id: "SGI-007", name: "Canada/Modèle Protection — Résidus Discriminatoires Persistants Certaines Provinces, Progrès Inégal Régions", country: "Canada", composite_score: 22.1, criminalization_legal_penalty_severity_score: 22.0, state_sanctioned_violence_impunity_score: 18.0, social_discrimination_hate_crime_exposure_score: 28.0, legal_protection_recognition_gap_score: 20.0, risk_level: "modéré", primary_pattern: "social_discrimination_hate_crime_exposure", estimated_sogi_rights_index: 2.21, last_updated: "2026-06-21" },
    { id: "SGI-008", name: "Taiwan/Mariage Égal Asie Modèle — Premier Pays Asie Mariage Same-Sex 2019, Protection Discrimination Emploi", country: "Taiwan", composite_score: 4.0, criminalization_legal_penalty_severity_score: 4.0, state_sanctioned_violence_impunity_score: 3.0, social_discrimination_hate_crime_exposure_score: 5.0, legal_protection_recognition_gap_score: 4.0, risk_level: "faible", primary_pattern: "criminalization_legal_penalty_severity", estimated_sogi_rights_index: 0.40, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sexual-orientation-gender-identity-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
