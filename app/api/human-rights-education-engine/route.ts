import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[human-rights-education-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Human Rights Education Engine Agent",
  domain: "human_rights_education",
  total_entities: 8,
  avg_composite: 59.49,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { civil_society_repression: 2, access_denial_marginalized: 2, international_framework_gap: 2, curriculum_obstruction: 2 },
  top_risk_entities: [
    "Chine — Éducation Patriotique Obligatoire, Suppression Contenu Droits & Contrôle Internet",
    "Russie — Loi Agents Étrangers ONG, Interdiction Contenu Droits & Écoles Propagande",
    "Iran — Curriculum Islamiste Exclusif, ONG Droits Humains Interdites & Femmes Exclus",
  ],
  critical_alerts: [
    "Chine: civil_society_repression",
    "Russie: civil_society_repression",
    "Iran: access_denial_marginalized",
    "Arabie Saoudite: international_framework_gap",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_human_rights_education_index: 5.95,
  data_sources: [
    "un_declaration_human_rights_education_training_2011_implementation_report",
    "amnesty_international_human_rights_education_program_global_survey",
    "hrea_human_rights_education_associates_global_status_report",
  ],
  entities: [
    { entity_id: "HRE-001", name: "Chine — Éducation Patriotique Obligatoire, Suppression Contenu Droits & Contrôle Internet", country: "Asie du Nord-Est", composite_score: 89.0, curriculum_obstruction_score: 90.0, civil_society_repression_score: 92.0, access_denial_marginalized_score: 88.0, international_framework_gap_score: 85.0, risk_level: "critique", primary_pattern: "civil_society_repression", estimated_human_rights_education_index: 8.9, last_updated: "2026-06-20" },
    { entity_id: "HRE-002", name: "Russie — Loi Agents Étrangers ONG, Interdiction Contenu Droits & Écoles Propagande", country: "Europe de l'Est", composite_score: 86.55, curriculum_obstruction_score: 88.0, civil_society_repression_score: 90.0, access_denial_marginalized_score: 85.0, international_framework_gap_score: 82.0, risk_level: "critique", primary_pattern: "civil_society_repression", estimated_human_rights_education_index: 8.66, last_updated: "2026-06-20" },
    { entity_id: "HRE-003", name: "Iran — Curriculum Islamiste Exclusif, ONG Droits Humains Interdites & Femmes Exclus", country: "Moyen-Orient", composite_score: 83.85, curriculum_obstruction_score: 82.0, civil_society_repression_score: 85.0, access_denial_marginalized_score: 88.0, international_framework_gap_score: 80.0, risk_level: "critique", primary_pattern: "access_denial_marginalized", estimated_human_rights_education_index: 8.39, last_updated: "2026-06-20" },
    { entity_id: "HRE-004", name: "Arabie Saoudite — Droits Humains Absents Curricula, Militantes Emprisonnées & Contrôle Religieux", country: "Moyen-Orient", composite_score: 81.0, curriculum_obstruction_score: 80.0, civil_society_repression_score: 78.0, access_denial_marginalized_score: 82.0, international_framework_gap_score: 85.0, risk_level: "critique", primary_pattern: "international_framework_gap", estimated_human_rights_education_index: 8.1, last_updated: "2026-06-20" },
    { entity_id: "HRE-005", name: "Inde — Manuels Scolaires Révisés BJP, Minorités Effacées & ONG Droits sous Pression FCRA", country: "Asie du Sud", composite_score: 53.85, curriculum_obstruction_score: 52.0, civil_society_repression_score: 55.0, access_denial_marginalized_score: 58.0, international_framework_gap_score: 50.0, risk_level: "élevé", primary_pattern: "access_denial_marginalized", estimated_human_rights_education_index: 5.39, last_updated: "2026-06-20" },
    { entity_id: "HRE-006", name: "Turquie — Restriction ONG Post-Coup, Contenu Kémaliste Imposé & Minorités Kurdes Exclues", country: "Europe de l'Est", composite_score: 51.15, curriculum_obstruction_score: 48.0, civil_society_repression_score: 52.0, access_denial_marginalized_score: 55.0, international_framework_gap_score: 50.0, risk_level: "élevé", primary_pattern: "curriculum_obstruction", estimated_human_rights_education_index: 5.12, last_updated: "2026-06-20" },
    { entity_id: "HRE-007", name: "UE/UNESCO — Programme Mondial EDH, Plan Action 2020-2024 & Intégration Partielle Curricula", country: "Europe/Global", composite_score: 26.1, curriculum_obstruction_score: 22.0, civil_society_repression_score: 28.0, access_denial_marginalized_score: 30.0, international_framework_gap_score: 25.0, risk_level: "modéré", primary_pattern: "curriculum_obstruction", estimated_human_rights_education_index: 2.61, last_updated: "2026-06-20" },
    { entity_id: "HRE-008", name: "ONU/HCDH — Déclaration ONU EDH 2011, Rapporteur Spécial & Ressources Pédagogiques", country: "Global", composite_score: 4.4, curriculum_obstruction_score: 4.0, civil_society_repression_score: 5.0, access_denial_marginalized_score: 3.0, international_framework_gap_score: 6.0, risk_level: "faible", primary_pattern: "international_framework_gap", estimated_human_rights_education_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/human-rights-education-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
