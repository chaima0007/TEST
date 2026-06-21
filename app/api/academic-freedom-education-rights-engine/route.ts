import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[academic-freedom-education-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Academic Freedom Education Rights Engine Agent",
  domain: "academic_freedom_education_rights",
  total_entities: 8,
  avg_composite: 61.36,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    girls_education_access_denial_gap: 2,
    curriculum_ideological_control_censorship_scale: 1,
    scholar_persecution_imprisonment_severity: 3,
    university_autonomy_state_capture: 2,
  },
  top_risk_entities: [
    "Afghanistan/Taliban — Filles Bannies Éducation, Universités Femmes Fermées, Chercheurs Exilés & Manuels Brûlés",
    "Chine — Uighur Scholars Disparus, Universités Idéologie Xi, Manuels Réécrits Histoire & Chercheurs Étrangers Espionnage",
    "Turquie/Erdoğan — 6 000 Académiciens Virés Post-2016, Pétition Paix Signée→Procès, Universités Recteurs Nommés Gouvernement",
  ],
  critical_alerts: [
    "Afghanistan/Taliban: girls_education_access_denial_gap",
    "Chine: curriculum_ideological_control_censorship_scale",
    "Turquie/Erdoğan: scholar_persecution_imprisonment_severity",
    "Hongrie/Orbán: university_autonomy_state_capture",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_academic_freedom_education_rights_index: 6.14,
  data_sources: [
    "scholars_at_risk_free_to_think_annual_report",
    "iff_academic_freedom_index_global_ranking",
    "hrw_education_rights_violations_documentation",
  ],
  entities: [
    {
      entity_id: "AFE-001",
      name: "Afghanistan/Taliban — Filles Bannies Éducation, Universités Femmes Fermées, Chercheurs Exilés & Manuels Brûlés",
      country: "Afghanistan",
      scholar_persecution_imprisonment_severity_score: 95.0,
      curriculum_ideological_control_censorship_scale_score: 93.0,
      university_autonomy_state_capture_score: 92.0,
      girls_education_access_denial_gap_score: 91.0,
      composite_score: 92.95,
      risk_level: "critique",
      primary_pattern: "girls_education_access_denial_gap",
      estimated_academic_freedom_education_rights_index: 9.3,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "AFE-002",
      name: "Chine — Uighur Scholars Disparus, Universités Idéologie Xi, Manuels Réécrits Histoire & Chercheurs Étrangers Espionnage",
      country: "Chine",
      scholar_persecution_imprisonment_severity_score: 92.0,
      curriculum_ideological_control_censorship_scale_score: 90.0,
      university_autonomy_state_capture_score: 89.0,
      girls_education_access_denial_gap_score: 88.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "curriculum_ideological_control_censorship_scale",
      estimated_academic_freedom_education_rights_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "AFE-003",
      name: "Turquie/Erdoğan — 6 000 Académiciens Virés Post-2016, Pétition Paix Signée→Procès, Universités Recteurs Nommés Gouvernement",
      country: "Turquie",
      scholar_persecution_imprisonment_severity_score: 89.0,
      curriculum_ideological_control_censorship_scale_score: 87.0,
      university_autonomy_state_capture_score: 86.0,
      girls_education_access_denial_gap_score: 85.0,
      composite_score: 86.95,
      risk_level: "critique",
      primary_pattern: "scholar_persecution_imprisonment_severity",
      estimated_academic_freedom_education_rights_index: 8.7,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "AFE-004",
      name: "Hongrie/Orbán — CEU Expulsé Budapest, Études Genre Interdites, Académie Sciences Sous Contrôle & Think Tanks Fermés",
      country: "Hongrie",
      scholar_persecution_imprisonment_severity_score: 86.0,
      curriculum_ideological_control_censorship_scale_score: 84.0,
      university_autonomy_state_capture_score: 83.0,
      girls_education_access_denial_gap_score: 82.0,
      composite_score: 83.95,
      risk_level: "critique",
      primary_pattern: "university_autonomy_state_capture",
      estimated_academic_freedom_education_rights_index: 8.4,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "AFE-005",
      name: "Russie/Belarus — Profs Anti-Guerre Licenciés, Étudiants Arrêtés Manifestations, Histoire Réécriture Ukrainienne & LGBTQ+ Curricula Bannis",
      country: "Russie/Belarus",
      scholar_persecution_imprisonment_severity_score: 57.0,
      curriculum_ideological_control_censorship_scale_score: 55.0,
      university_autonomy_state_capture_score: 54.0,
      girls_education_access_denial_gap_score: 53.0,
      composite_score: 54.95,
      risk_level: "élevé",
      primary_pattern: "scholar_persecution_imprisonment_severity",
      estimated_academic_freedom_education_rights_index: 5.5,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "AFE-006",
      name: "USA/UK — DEI Programmes Attaqués, Campus Speech Codes, Donors Political Pressure & Academic Boycott Palestine",
      country: "USA/UK",
      scholar_persecution_imprisonment_severity_score: 54.0,
      curriculum_ideological_control_censorship_scale_score: 52.0,
      university_autonomy_state_capture_score: 51.0,
      girls_education_access_denial_gap_score: 50.0,
      composite_score: 51.95,
      risk_level: "élevé",
      primary_pattern: "university_autonomy_state_capture",
      estimated_academic_freedom_education_rights_index: 5.2,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "AFE-007",
      name: "Scholars at Risk/SAR — Réseau Protection Académiciens Persécutés, Free to Think Report & Monitoring Attaques",
      country: "Global",
      scholar_persecution_imprisonment_severity_score: 27.0,
      curriculum_ideological_control_censorship_scale_score: 26.0,
      university_autonomy_state_capture_score: 25.0,
      girls_education_access_denial_gap_score: 25.0,
      composite_score: 25.85,
      risk_level: "modéré",
      primary_pattern: "scholar_persecution_imprisonment_severity",
      estimated_academic_freedom_education_rights_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "AFE-008",
      name: "ONU/Art.13 DESC — Droit Éducation, Recommandation UNESCO Chercheurs 1997 & SDG 4 Éducation Qualité",
      country: "Global",
      scholar_persecution_imprisonment_severity_score: 5.0,
      curriculum_ideological_control_censorship_scale_score: 4.0,
      university_autonomy_state_capture_score: 4.0,
      girls_education_access_denial_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "girls_education_access_denial_gap",
      estimated_academic_freedom_education_rights_index: 0.43,
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
      `${process.env.SWARM_API_URL}/academic-freedom-education-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
