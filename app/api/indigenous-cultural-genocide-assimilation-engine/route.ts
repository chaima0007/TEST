import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[indigenous-cultural-genocide-assimilation-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Indigenous Cultural Genocide Assimilation Engine Agent",
  domain: "indigenous_cultural_genocide_assimilation",
  total_entities: 8,
  avg_composite: 61.85,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: { forced_assimilation_child_removal_severity: 5, state_accountability_reparations_gap: 1, territorial_dispossession_violence: 2 },
  top_risk_entities: [
    "Chine/Internats Tibétains Séparation Familles — 800 000+ Enfants Tibétains Retirés 2019-2024, Sinisation Forcée",
    "Canada/Pensionnats 150 000 Enfants Arrachés — Politique Assimilation 1831-1996, 3213 Décès Confirmés Tombes",
    "USA/Boarding Schools 50 000 Enfants Autochtones — Kill Indian Save Man, 50+ Écoles Fédérales, Abus Systémiques",
  ],
  critical_alerts: [
    "Chine/Internats Tibétains Séparation Familles: state_accountability_reparations_gap",
    "Canada/Pensionnats 150 000 Enfants Arrachés: forced_assimilation_child_removal_severity",
    "USA/Boarding Schools 50 000 Enfants Autochtones: forced_assimilation_child_removal_severity",
    "Australie/Stolen Generation Politique Assimilation: forced_assimilation_child_removal_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_indigenous_cultural_genocide_index: 6.19,
  data_sources: [
    "nctr_canada_final_report_truth_reconciliation_commission",
    "bring_them_home_report_australia_stolen_generation_1997",
    "un_special_rapporteur_indigenous_peoples_cultural_genocide",
    "human_rights_watch_china_tibet_boarding_schools_2024",
  ],
  entities: [
    { id: "ICG-001", name: "Canada/Pensionnats 150 000 Enfants Arrachés — Politique Assimilation 1831-1996, 3213 Décès Confirmés Tombes", country: "Canada", composite_score: 87.05, forced_assimilation_child_removal_severity_score: 93.0, language_cultural_suppression_scale_score: 91.0, territorial_dispossession_violence_score: 88.0, state_accountability_reparations_gap_score: 72.0, risk_level: "critique", primary_pattern: "forced_assimilation_child_removal_severity", estimated_indigenous_cultural_genocide_index: 8.71, last_updated: "2026-06-21" },
    { id: "ICG-002", name: "Australie/Stolen Generation Politique Assimilation — 100 000 Enfants Mêlés Retirés 1910-1970, Dommages Générationnels", country: "Australie", composite_score: 85.65, forced_assimilation_child_removal_severity_score: 91.0, language_cultural_suppression_scale_score: 89.0, territorial_dispossession_violence_score: 90.0, state_accountability_reparations_gap_score: 68.0, risk_level: "critique", primary_pattern: "forced_assimilation_child_removal_severity", estimated_indigenous_cultural_genocide_index: 8.57, last_updated: "2026-06-21" },
    { id: "ICG-003", name: "USA/Boarding Schools 50 000 Enfants Autochtones — Kill Indian Save Man, 50+ Écoles Fédérales, Abus Systémiques", country: "USA", composite_score: 86.3, forced_assimilation_child_removal_severity_score: 89.0, language_cultural_suppression_scale_score: 87.0, territorial_dispossession_violence_score: 85.0, state_accountability_reparations_gap_score: 83.0, risk_level: "critique", primary_pattern: "forced_assimilation_child_removal_severity", estimated_indigenous_cultural_genocide_index: 8.63, last_updated: "2026-06-21" },
    { id: "ICG-004", name: "Chine/Internats Tibétains Séparation Familles — 800 000+ Enfants Tibétains Retirés 2019-2024, Sinisation Forcée", country: "Chine", composite_score: 94.9, forced_assimilation_child_removal_severity_score: 95.0, language_cultural_suppression_scale_score: 96.0, territorial_dispossession_violence_score: 92.0, state_accountability_reparations_gap_score: 97.0, risk_level: "critique", primary_pattern: "state_accountability_reparations_gap", estimated_indigenous_cultural_genocide_index: 9.49, last_updated: "2026-06-21" },
    { id: "ICG-005", name: "Brésil/Amazonie Garimpeiros Yanomami — Orpaillage Illégal Mercure, 570 Morts 2021-2023, Terres Envahies", country: "Brésil", composite_score: 53.4, forced_assimilation_child_removal_severity_score: 48.0, language_cultural_suppression_scale_score: 52.0, territorial_dispossession_violence_score: 60.0, state_accountability_reparations_gap_score: 55.0, risk_level: "élevé", primary_pattern: "territorial_dispossession_violence", estimated_indigenous_cultural_genocide_index: 5.34, last_updated: "2026-06-21" },
    { id: "ICG-006", name: "Colombie/Peuples Isolés FARC Territoires — Dissidences FARC ELN Envahissent Terres Sacrées, 100+ Peuples Menacés", country: "Colombie", composite_score: 59.5, forced_assimilation_child_removal_severity_score: 52.0, language_cultural_suppression_scale_score: 58.0, territorial_dispossession_violence_score: 68.0, state_accountability_reparations_gap_score: 62.0, risk_level: "élevé", primary_pattern: "territorial_dispossession_violence", estimated_indigenous_cultural_genocide_index: 5.95, last_updated: "2026-06-21" },
    { id: "ICG-007", name: "Bolivie/Droits Constitutionnels Modèle — 36 Peuples Reconnus Constitution 2009, Terres Collectives Garanties", country: "Bolivie", composite_score: 21.35, forced_assimilation_child_removal_severity_score: 22.0, language_cultural_suppression_scale_score: 18.0, territorial_dispossession_violence_score: 25.0, state_accountability_reparations_gap_score: 20.0, risk_level: "modéré", primary_pattern: "forced_assimilation_child_removal_severity", estimated_indigenous_cultural_genocide_index: 2.14, last_updated: "2026-06-21" },
    { id: "ICG-008", name: "Nouvelle-Zélande/Traité Waitangi Modèle — Maori Co-Gouvernance 1840, Revitalisation Langue Te Reo, Tribunaux Actifs", country: "Nouvelle-Zélande", composite_score: 6.65, forced_assimilation_child_removal_severity_score: 8.0, language_cultural_suppression_scale_score: 6.0, territorial_dispossession_violence_score: 7.0, state_accountability_reparations_gap_score: 5.0, risk_level: "faible", primary_pattern: "forced_assimilation_child_removal_severity", estimated_indigenous_cultural_genocide_index: 0.67, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/indigenous-cultural-genocide-assimilation-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
