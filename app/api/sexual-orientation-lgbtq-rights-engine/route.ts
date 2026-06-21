import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sexual-orientation-lgbtq-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Sexual Orientation LGBTQ Rights Engine Agent",
  domain: "sexual_orientation_lgbtq_rights",
  total_entities: 8,
  avg_composite: 62.12,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { lgbtq_criminalization_imprisonment_severity: 3, lgbtq_violence_hate_crime_impunity_scale: 3, same_sex_partnership_legal_recognition_absence: 2 },
  top_risk_entities: [
    "Ouganda — Anti-Homosexualité Loi Peine Mort 2023, Refuges LGBT Fermés, Journalistes Outés & Familles Reniement",
    "Iran/Arabie Saoudite — Homosexualité Mort/Flagellation, Exécutions Publiques, Transgenres Forcés Opération & Arrestations Systématiques",
    "Russie — Loi Propagande LGBT+ Totale, Organisations Liquidées, Chechen Camps Concentration & Arrestations Pride",
  ],
  critical_alerts: [
    "Ouganda: lgbtq_criminalization_imprisonment_severity",
    "Iran/Arabie Saoudite: lgbtq_criminalization_imprisonment_severity",
    "Russie: lgbtq_violence_hate_crime_impunity_scale",
    "Chine: same_sex_partnership_legal_recognition_absence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_sexual_orientation_lgbtq_rights_index: 6.21,
  data_sources: [
    "ilga_world_state_sponsored_homophobia_report",
    "rainbow_europe_lgbti_rights_annual_index",
    "human_rights_watch_lgbtq_violence_documentation",
  ],
  entities: [
    { id: "SOL-001", name: "Ouganda — Anti-Homosexualité Loi Peine Mort 2023, Refuges LGBT Fermés, Journalistes Outés & Familles Reniement", country: "Ouganda", composite_score: 94.2, lgbtq_criminalization_imprisonment_severity_score: 96.0, lgbtq_violence_hate_crime_impunity_scale_score: 93.0, same_sex_partnership_legal_recognition_absence_score: 95.0, lgbtq_asylum_protection_deficit_gap_score: 92.0, risk_level: "critique", primary_pattern: "lgbtq_criminalization_imprisonment_severity", estimated_sexual_orientation_lgbtq_rights_index: 9.42, last_updated: "2026-06-21" },
    { id: "SOL-002", name: "Iran/Arabie Saoudite — Homosexualité Mort/Flagellation, Exécutions Publiques, Transgenres Forcés Opération & Arrestations Systématiques", country: "Iran/Arabie Saoudite", composite_score: 91.65, lgbtq_criminalization_imprisonment_severity_score: 93.0, lgbtq_violence_hate_crime_impunity_scale_score: 91.0, same_sex_partnership_legal_recognition_absence_score: 92.0, lgbtq_asylum_protection_deficit_gap_score: 90.0, risk_level: "critique", primary_pattern: "lgbtq_criminalization_imprisonment_severity", estimated_sexual_orientation_lgbtq_rights_index: 9.17, last_updated: "2026-06-21" },
    { id: "SOL-003", name: "Russie — Loi Propagande LGBT+ Totale, Organisations Liquidées, Chechen Camps Concentration & Arrestations Pride", country: "Russie", composite_score: 87.65, lgbtq_criminalization_imprisonment_severity_score: 89.0, lgbtq_violence_hate_crime_impunity_scale_score: 87.0, same_sex_partnership_legal_recognition_absence_score: 88.0, lgbtq_asylum_protection_deficit_gap_score: 86.0, risk_level: "critique", primary_pattern: "lgbtq_violence_hate_crime_impunity_scale", estimated_sexual_orientation_lgbtq_rights_index: 8.77, last_updated: "2026-06-21" },
    { id: "SOL-004", name: "Chine — Dépathologisation Sans Droits, Applications Gay Bloquées, Transgenres Hôpitaux Psychiatriques & Organizations Fermées", country: "Chine", composite_score: 84.6, lgbtq_criminalization_imprisonment_severity_score: 86.0, lgbtq_violence_hate_crime_impunity_scale_score: 83.0, same_sex_partnership_legal_recognition_absence_score: 85.0, lgbtq_asylum_protection_deficit_gap_score: 84.0, risk_level: "critique", primary_pattern: "same_sex_partnership_legal_recognition_absence", estimated_sexual_orientation_lgbtq_rights_index: 8.46, last_updated: "2026-06-21" },
    { id: "SOL-005", name: "Pologne/Hongrie — Zones LGBT-Free, Adoption Interdite Couples Même Sexe, Propaganda Laws & Pride Bâton Pologne", country: "Pologne/Hongrie", composite_score: 55.65, lgbtq_criminalization_imprisonment_severity_score: 57.0, lgbtq_violence_hate_crime_impunity_scale_score: 55.0, same_sex_partnership_legal_recognition_absence_score: 56.0, lgbtq_asylum_protection_deficit_gap_score: 54.0, risk_level: "élevé", primary_pattern: "same_sex_partnership_legal_recognition_absence", estimated_sexual_orientation_lgbtq_rights_index: 5.57, last_updated: "2026-06-21" },
    { id: "SOL-006", name: "USA/Brésil — State-Level Bans 20 États Trans Mineurs, Violences Anti-Trans Record, Bolsonaro Héritage & Felony Drag", country: "USA/Brésil", composite_score: 52.65, lgbtq_criminalization_imprisonment_severity_score: 54.0, lgbtq_violence_hate_crime_impunity_scale_score: 53.0, same_sex_partnership_legal_recognition_absence_score: 52.0, lgbtq_asylum_protection_deficit_gap_score: 51.0, risk_level: "élevé", primary_pattern: "lgbtq_violence_hate_crime_impunity_scale", estimated_sexual_orientation_lgbtq_rights_index: 5.27, last_updated: "2026-06-21" },
    { id: "SOL-007", name: "ILGA World/Rainbow Europe — Cartographie Droits LGBTI, Criminalisation Map, Standards Protection & Rapports Annuels", country: "Global", composite_score: 26.1, lgbtq_criminalization_imprisonment_severity_score: 24.0, lgbtq_violence_hate_crime_impunity_scale_score: 28.0, same_sex_partnership_legal_recognition_absence_score: 26.0, lgbtq_asylum_protection_deficit_gap_score: 27.0, risk_level: "modéré", primary_pattern: "lgbtq_violence_hate_crime_impunity_scale", estimated_sexual_orientation_lgbtq_rights_index: 2.61, last_updated: "2026-06-21" },
    { id: "SOL-008", name: "ONU/Principes Yogyakarta — Principes Orientation Sexuelle Identité Genre, Résolution CDHONU & SDG 10 Inégalités", country: "Global", composite_score: 4.45, lgbtq_criminalization_imprisonment_severity_score: 4.0, lgbtq_violence_hate_crime_impunity_scale_score: 5.0, same_sex_partnership_legal_recognition_absence_score: 4.0, lgbtq_asylum_protection_deficit_gap_score: 5.0, risk_level: "faible", primary_pattern: "lgbtq_criminalization_imprisonment_severity", estimated_sexual_orientation_lgbtq_rights_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sexual-orientation-lgbtq-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
