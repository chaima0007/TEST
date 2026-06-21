import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[elderly-rights-age-discrimination-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Elderly Rights Age Discrimination Engine Agent",
  domain: "elderly_rights_age_discrimination",
  total_entities: 8,
  avg_composite: 61.32,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    elder_abuse_neglect_institutional_severity: 4,
    pension_social_security_denial_scale: 2,
    age_discrimination_employment_exclusion: 1,
    elderly_healthcare_access_dignity_deficit_gap: 1,
  },
  top_risk_entities: [
    "Chine/Maisons Retraite Abandons Covid Scandale — Aînés Isolés Morts Confinement, Familles Séparées & Maltraitance Institutionnelle Documentée",
    "Inde/Abandons Aînés Temples Vieillesse — 3.7M Personnes Âgées Sans Abri, Abandon Familial Structurel & Discrimination Caste-Âge Cumulée",
    "Brésil/EHPAD Abus Maltraitance Pandémie — 36 000 Morts Résidences 2020, Surmortalité Aînés Pauvres & Négligence Institutionnelle Systémique",
  ],
  critical_alerts: [
    "Chine/Maisons Retraite Abandons Covid Scandale: elder_abuse_neglect_institutional_severity",
    "Inde/Abandons Aînés Temples Vieillesse: pension_social_security_denial_scale",
    "Brésil/EHPAD Abus Maltraitance Pandémie: elder_abuse_neglect_institutional_severity",
    "Russie/Retraites Gelées Inflation Pauvreté Aînés: age_discrimination_employment_exclusion",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_elderly_rights_age_discrimination_index: 6.13,
  data_sources: [
    "helpage_global_agewatch_index_annual_report",
    "who_elder_abuse_global_status_report",
    "ilo_age_discrimination_employment_survey",
  ],
  entities: [
    {
      entity_id: "ERA-001",
      name: "Chine/Maisons Retraite Abandons Covid Scandale — Aînés Isolés Morts Confinement, Familles Séparées & Maltraitance Institutionnelle Documentée",
      country: "Chine",
      elder_abuse_neglect_institutional_severity_score: 93.0,
      pension_social_security_denial_scale_score: 88.0,
      age_discrimination_employment_exclusion_score: 87.0,
      elderly_healthcare_access_dignity_deficit_gap_score: 91.0,
      composite_score: 89.85,
      risk_level: "critique",
      primary_pattern: "elder_abuse_neglect_institutional_severity",
      estimated_elderly_rights_age_discrimination_index: 8.99,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ERA-002",
      name: "Inde/Abandons Aînés Temples Vieillesse — 3.7M Personnes Âgées Sans Abri, Abandon Familial Structurel & Discrimination Caste-Âge Cumulée",
      country: "Inde",
      elder_abuse_neglect_institutional_severity_score: 90.0,
      pension_social_security_denial_scale_score: 89.0,
      age_discrimination_employment_exclusion_score: 85.0,
      elderly_healthcare_access_dignity_deficit_gap_score: 88.0,
      composite_score: 88.1,
      risk_level: "critique",
      primary_pattern: "pension_social_security_denial_scale",
      estimated_elderly_rights_age_discrimination_index: 8.81,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ERA-003",
      name: "Brésil/EHPAD Abus Maltraitance Pandémie — 36 000 Morts Résidences 2020, Surmortalité Aînés Pauvres & Négligence Institutionnelle Systémique",
      country: "Brésil",
      elder_abuse_neglect_institutional_severity_score: 88.0,
      pension_social_security_denial_scale_score: 84.0,
      age_discrimination_employment_exclusion_score: 83.0,
      elderly_healthcare_access_dignity_deficit_gap_score: 86.0,
      composite_score: 85.35,
      risk_level: "critique",
      primary_pattern: "elder_abuse_neglect_institutional_severity",
      estimated_elderly_rights_age_discrimination_index: 8.54,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ERA-004",
      name: "Russie/Retraites Gelées Inflation Pauvreté Aînés — Âge Retraite Relevé 2018, Pensions Insuffisantes & Discrimination Emploi 50+ Documentée",
      country: "Russie",
      elder_abuse_neglect_institutional_severity_score: 85.0,
      pension_social_security_denial_scale_score: 87.0,
      age_discrimination_employment_exclusion_score: 86.0,
      elderly_healthcare_access_dignity_deficit_gap_score: 83.0,
      composite_score: 85.35,
      risk_level: "critique",
      primary_pattern: "age_discrimination_employment_exclusion",
      estimated_elderly_rights_age_discrimination_index: 8.54,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ERA-005",
      name: "USA/Maisons Retraite Abus 1.5M Signalements/An — Under-Staffing Chronique, Abus Financiers Aînés & Discrimination Couleur dans EHPAD",
      country: "USA",
      elder_abuse_neglect_institutional_severity_score: 58.0,
      pension_social_security_denial_scale_score: 54.0,
      age_discrimination_employment_exclusion_score: 57.0,
      elderly_healthcare_access_dignity_deficit_gap_score: 55.0,
      composite_score: 56.15,
      risk_level: "élevé",
      primary_pattern: "elder_abuse_neglect_institutional_severity",
      estimated_elderly_rights_age_discrimination_index: 5.62,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ERA-006",
      name: "Afrique Sub-Saharienne/Sorcellerie Accusations Aîné Exclusion — Aînés Accusés Sorcellerie, Lynchages, Expulsions & Violence Communautaire Ritualisée",
      country: "Afrique Sub-Saharienne",
      elder_abuse_neglect_institutional_severity_score: 55.0,
      pension_social_security_denial_scale_score: 52.0,
      age_discrimination_employment_exclusion_score: 50.0,
      elderly_healthcare_access_dignity_deficit_gap_score: 58.0,
      composite_score: 53.6,
      risk_level: "élevé",
      primary_pattern: "elderly_healthcare_access_dignity_deficit_gap",
      estimated_elderly_rights_age_discrimination_index: 5.36,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ERA-007",
      name: "HelpAge/AARP Alliance Internationale Vieillissement — Plaidoyer Convention ONU Droits Aînés, Rapport Global AgeWatch & Indicateurs Inclusion",
      country: "Global",
      elder_abuse_neglect_institutional_severity_score: 28.0,
      pension_social_security_denial_scale_score: 26.0,
      age_discrimination_employment_exclusion_score: 27.0,
      elderly_healthcare_access_dignity_deficit_gap_score: 25.0,
      composite_score: 26.65,
      risk_level: "modéré",
      primary_pattern: "elder_abuse_neglect_institutional_severity",
      estimated_elderly_rights_age_discrimination_index: 2.67,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ERA-008",
      name: "ONU/Plan Madrid 2002 Vieillissement & MIPAA — Cadre International Non-Discrimination Âge, Résolutions AG Personnes Âgées & SDG Inclusion",
      country: "Global",
      elder_abuse_neglect_institutional_severity_score: 6.0,
      pension_social_security_denial_scale_score: 5.0,
      age_discrimination_employment_exclusion_score: 5.0,
      elderly_healthcare_access_dignity_deficit_gap_score: 6.0,
      composite_score: 5.5,
      risk_level: "faible",
      primary_pattern: "pension_social_security_denial_scale",
      estimated_elderly_rights_age_discrimination_index: 0.55,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/elderly-rights-age-discrimination-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
