import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[academic-freedom-university-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Academic Freedom University Rights Engine Agent",
  domain: "academic_freedom_university_rights",
  total_entities: 8,
  avg_composite: 62.68,
  confidence_score: 0.85,
  risk_distribution: { "critique": 4, "élevé": 2, "modéré": 1, "faible": 1 },
  pattern_distribution: { "curriculum_ideology_state_control_scale": 1, "university_autonomy_governance_deficit_gap": 3, "scholar_arrest_exile_persecution_severity": 3, "research_publication_censorship": 1 },
  top_risk_entities: ["Chine/Confucius Instituts Censure — Surveillance Étudiants Étrangers, Auto-Censure Universités Mondiales & Propagande Xi dans Campus Internationaux", "Turkménistan/Universités Contrôle Total Idéologique — Manuels Réécrits Culte Dirigeant, Chercheurs Interdits Voyager & Internet Académique Bloqué", "Iran/Université Épurations Professeures — 800 Académiciennes Exclues 2023, Arrestations Protestants Campus & Interdiction Sciences Politiques Femmes"],
  critical_alerts: ["Chine/Confucius Instituts Censure: curriculum_ideology_state_control_scale", "Turkménistan/Universités Contrôle Total Idéologique: university_autonomy_governance_deficit_gap", "Iran/Université Épurations Professeures: scholar_arrest_exile_persecution_severity", "Turquie/3 500 Académiciens Révoqués Post-Coup: scholar_arrest_exile_persecution_severity"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_academic_freedom_university_rights_index: 6.27,
  data_sources: ["scholars_at_risk_free_to_think_report", "aaup_academic_freedom_index", "scholars_at_risk_monitoring_network"],
  entities: [
    {
,      entity_id: "AFU-001"
      name: "Chine/Confucius Instituts Censure — Surveillance Étudiants Étrangers, Auto-Censure Universités Mondiales & Propagande Xi dans Campus Internationaux"
      country: "Chine"
      scholar_arrest_exile_persecution_severity_score: 93.0
      curriculum_ideology_state_control_scale_score: 92.0
      research_publication_censorship_score: 91.0
      university_autonomy_governance_deficit_gap_score: 90.0
      composite_score: 91.65
      risk_level: "critique"
      primary_pattern: "curriculum_ideology_state_control_scale"
      estimated_academic_freedom_university_rights_index: 9.17
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AFU-002"
      name: "Turkménistan/Universités Contrôle Total Idéologique — Manuels Réécrits Culte Dirigeant, Chercheurs Interdits Voyager & Internet Académique Bloqué"
      country: "Turkménistan"
      scholar_arrest_exile_persecution_severity_score: 91.0
      curriculum_ideology_state_control_scale_score: 93.0
      research_publication_censorship_score: 90.0
      university_autonomy_governance_deficit_gap_score: 92.0
      composite_score: 91.45
      risk_level: "critique"
      primary_pattern: "university_autonomy_governance_deficit_gap"
      estimated_academic_freedom_university_rights_index: 9.14
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AFU-003"
      name: "Iran/Université Épurations Professeures — 800 Académiciennes Exclues 2023, Arrestations Protestants Campus & Interdiction Sciences Politiques Femmes"
      country: "Iran"
      scholar_arrest_exile_persecution_severity_score: 90.0
      curriculum_ideology_state_control_scale_score: 88.0
      research_publication_censorship_score: 87.0
      university_autonomy_governance_deficit_gap_score: 89.0
      composite_score: 88.55
      risk_level: "critique"
      primary_pattern: "scholar_arrest_exile_persecution_severity"
      estimated_academic_freedom_university_rights_index: 8.86
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AFU-004"
      name: "Turquie/3 500 Académiciens Révoqués Post-Coup — Décrets Urgence Suppressions, Passeports Confisqués Chercheurs & Pétition Paix 2016 Procès Masse"
      country: "Turquie"
      scholar_arrest_exile_persecution_severity_score: 88.0
      curriculum_ideology_state_control_scale_score: 85.0
      research_publication_censorship_score: 84.0
      university_autonomy_governance_deficit_gap_score: 87.0
      composite_score: 86.05
      risk_level: "critique"
      primary_pattern: "scholar_arrest_exile_persecution_severity"
      estimated_academic_freedom_university_rights_index: 8.6
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AFU-005"
      name: "Hongrie/CEU Expulsion Budapest Orbán — Central European University Forcée Vienne 2019, Études Genre Interdites & ONG Académiques Taxées"
      country: "Hongrie"
      scholar_arrest_exile_persecution_severity_score: 57.0
      curriculum_ideology_state_control_scale_score: 58.0
      research_publication_censorship_score: 55.0
      university_autonomy_governance_deficit_gap_score: 59.0
      composite_score: 57.15
      risk_level: "élevé"
      primary_pattern: "university_autonomy_governance_deficit_gap"
      estimated_academic_freedom_university_rights_index: 5.71
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AFU-006"
      name: "Russie/Académiciens Anti-Guerre Radiés — 1 400 Chercheurs Exilés Post-2022, Poursuites Discrédit Scientifique & Censure Publications Ukraine"
      country: "Russie"
      scholar_arrest_exile_persecution_severity_score: 55.0
      curriculum_ideology_state_control_scale_score: 56.0
      research_publication_censorship_score: 57.0
      university_autonomy_governance_deficit_gap_score: 54.0
      composite_score: 55.55
      risk_level: "élevé"
      primary_pattern: "research_publication_censorship"
      estimated_academic_freedom_university_rights_index: 5.55
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AFU-007"
      name: "Scholars at Risk/AAUP Network — Monitoring Attaques Académiciens Worldwide, Free to Think Report Annuel & Réseau Accueil Chercheurs Persécutés"
      country: "Global"
      scholar_arrest_exile_persecution_severity_score: 27.0
      curriculum_ideology_state_control_scale_score: 26.0
      research_publication_censorship_score: 25.0
      university_autonomy_governance_deficit_gap_score: 26.0
      composite_score: 26.05
      risk_level: "modéré"
      primary_pattern: "scholar_arrest_exile_persecution_severity"
      estimated_academic_freedom_university_rights_index: 2.6
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "AFU-008"
      name: "ONU/UNESCO Recommandation Enseignement Supérieur 1997 — Cadre Normatif Liberté Académique, Autonomie Universitaire & Protection Statut Enseignants"
      country: "Global"
      scholar_arrest_exile_persecution_severity_score: 5.0
      curriculum_ideology_state_control_scale_score: 5.0
      research_publication_censorship_score: 5.0
      university_autonomy_governance_deficit_gap_score: 5.0
      composite_score: 5.0
      risk_level: "faible"
      primary_pattern: "university_autonomy_governance_deficit_gap"
      estimated_academic_freedom_university_rights_index: 0.5
      last_updated: "2026-06-21"
    }
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/academic-freedom-university-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
