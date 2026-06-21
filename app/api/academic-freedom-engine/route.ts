import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[academic-freedom-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Academic Freedom Engine Agent",
  domain: "academic_freedom",
  total_entities: 8,
  avg_composite: 60.18,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { campus_surveillance_control: 1, scholar_arrest_persecution: 3, curriculum_state_interference: 3, international_collaboration_restriction: 1 },
  top_risk_entities: [
    "Chine — Purges Académiques Xinjiang/Tibet, Surveillance Campus & Interdiction Pensée Critique",
    "Iran — Épurations Universités Post-2022, Arrestations Professeurs & Islamisation Curricula",
    "Turquie — 6000 Académiciens Licenciés Post-2016, Pétition Paix & Passeports Confisqués",
  ],
  critical_alerts: [
    "Chine: campus_surveillance_control",
    "Iran: scholar_arrest_persecution",
    "Turquie: scholar_arrest_persecution",
    "Russie: curriculum_state_interference",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_academic_freedom_index: 6.02,
  data_sources: [
    "scholars_at_risk_network_academic_freedom_monitoring_project",
    "academic_freedom_index_global_public_policy_institute_report",
    "human_rights_watch_university_repression_global_report",
  ],
  entities: [
    { entity_id: "AF-001", name: "Chine — Purges Académiques Xinjiang/Tibet, Surveillance Campus & Interdiction Pensée Critique", country: "Asie du Nord-Est", composite_score: 92.85, scholar_arrest_persecution_score: 95.0, curriculum_state_interference_score: 92.0, campus_surveillance_control_score: 95.0, international_collaboration_restriction_score: 88.0, risk_level: "critique", primary_pattern: "campus_surveillance_control", estimated_academic_freedom_index: 9.29, last_updated: "2026-06-21" },
    { entity_id: "AF-002", name: "Iran — Épurations Universités Post-2022, Arrestations Professeurs & Islamisation Curricula", country: "Moyen-Orient", composite_score: 88.85, scholar_arrest_persecution_score: 92.0, curriculum_state_interference_score: 88.0, campus_surveillance_control_score: 85.0, international_collaboration_restriction_score: 90.0, risk_level: "critique", primary_pattern: "scholar_arrest_persecution", estimated_academic_freedom_index: 8.89, last_updated: "2026-06-21" },
    { entity_id: "AF-003", name: "Turquie — 6000 Académiciens Licenciés Post-2016, Pétition Paix & Passeports Confisqués", country: "Europe/Moyen-Orient", composite_score: 84.5, scholar_arrest_persecution_score: 88.0, curriculum_state_interference_score: 82.0, campus_surveillance_control_score: 80.0, international_collaboration_restriction_score: 88.0, risk_level: "critique", primary_pattern: "scholar_arrest_persecution", estimated_academic_freedom_index: 8.45, last_updated: "2026-06-21" },
    { entity_id: "AF-004", name: "Russie — Exode Scientifiques Post-Ukraine, Censure Syllabi & Propagande Obligatoire", country: "Europe de l'Est", composite_score: 82.25, scholar_arrest_persecution_score: 82.0, curriculum_state_interference_score: 85.0, campus_surveillance_control_score: 80.0, international_collaboration_restriction_score: 82.0, risk_level: "critique", primary_pattern: "curriculum_state_interference", estimated_academic_freedom_index: 8.23, last_updated: "2026-06-21" },
    { entity_id: "AF-005", name: "USA — Lois Anti-DEI, Interdictions Livres Universités & Pressions Politique sur Campus", country: "Amérique du Nord", composite_score: 52.5, scholar_arrest_persecution_score: 52.0, curriculum_state_interference_score: 58.0, campus_surveillance_control_score: 48.0, international_collaboration_restriction_score: 52.0, risk_level: "élevé", primary_pattern: "curriculum_state_interference", estimated_academic_freedom_index: 5.25, last_updated: "2026-06-21" },
    { entity_id: "AF-006", name: "Hongrie/Orbán — CEU Expulsée, Lois Gender Studies & Contrôle Financement Recherche", country: "Europe", composite_score: 50.25, scholar_arrest_persecution_score: 48.0, curriculum_state_interference_score: 55.0, campus_surveillance_control_score: 50.0, international_collaboration_restriction_score: 48.0, risk_level: "élevé", primary_pattern: "curriculum_state_interference", estimated_academic_freedom_index: 5.03, last_updated: "2026-06-21" },
    { entity_id: "AF-007", name: "Scholars at Risk — Réseau 600+ Universités, Cas Documentés & Plaidoyer Protection", country: "Global", composite_score: 25.85, scholar_arrest_persecution_score: 22.0, curriculum_state_interference_score: 25.0, campus_surveillance_control_score: 28.0, international_collaboration_restriction_score: 30.0, risk_level: "modéré", primary_pattern: "scholar_arrest_persecution", estimated_academic_freedom_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "AF-008", name: "ONU/UNESCO — Recommandation Liberté Académique 1997, Suivi & Mécanismes Rapport", country: "Global", composite_score: 4.4, scholar_arrest_persecution_score: 4.0, curriculum_state_interference_score: 5.0, campus_surveillance_control_score: 3.0, international_collaboration_restriction_score: 6.0, risk_level: "faible", primary_pattern: "international_collaboration_restriction", estimated_academic_freedom_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/academic-freedom-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
