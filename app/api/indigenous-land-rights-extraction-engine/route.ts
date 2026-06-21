import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[indigenous-land-rights-extraction-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Indigenous Land Rights Extraction Engine Agent",
  domain: "indigenous_land_rights_extraction",
  total_entities: 8,
  avg_composite: 61.68,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { extractive_industry_territory_invasion_severity: 3, fpic_violation_forced_displacement_scale: 2, indigenous_environmental_defender_killing: 1, legal_title_recognition_land_rights_deficit_gap: 2 },
  top_risk_entities: ["Brésil/Amazonie — Garimpos Illégaux Yanomami, Terras Indígenas Envahies, Garimpeiros Armés & Lula Belo Monte Concessions", "Canada/Pipeline — TMX Trans Mountain Wet'suwet'en, GRC Expulsions Militarisées, Fracking Terres Sacrées & Site C Barrage Non-Consulté", "Philippines/Mindanao — Lumad Schools Fermées Armée, Mines Or Terres Ancestrales, Défenseurs Tués 2020-24 & Permis Extractifs Sans FPIC"],
  critical_alerts: ["Brésil/Amazonie: extractive_industry_territory_invasion_severity", "Canada/Pipeline: fpic_violation_forced_displacement_scale", "Philippines/Mindanao: indigenous_environmental_defender_killing", "Pérou/TIPNIS: extractive_industry_territory_invasion_severity"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_indigenous_land_rights_extraction_index: 6.17,
  data_sources: ["global_witness_land_defender_killings_report", "un_special_rapporteur_indigenous_peoples_land", "cultural_survival_fpic_violation_report"],
  entities: [
    { entity_id: "ILE-001", name: "Brésil/Amazonie — Garimpos Illégaux Yanomami, Terras Indígenas Envahies, Garimpeiros Armés & Lula Belo Monte Concessions", country: "Brésil", composite_score: 93.55, extractive_industry_territory_invasion_severity_score: 95.0, fpic_violation_forced_displacement_scale_score: 93.0, indigenous_environmental_defender_killing_score: 92.0, legal_title_recognition_land_rights_deficit_gap_score: 94.0, risk_level: "critique", primary_pattern: "extractive_industry_territory_invasion_severity", estimated_indigenous_land_rights_extraction_index: 9.36, last_updated: "2026-06-21" }
    { entity_id: "ILE-002", name: "Canada/Pipeline — TMX Trans Mountain Wet'suwet'en, GRC Expulsions Militarisées, Fracking Terres Sacrées & Site C Barrage Non-Consulté", country: "Canada", composite_score: 90.3, extractive_industry_territory_invasion_severity_score: 91.0, fpic_violation_forced_displacement_scale_score: 92.0, indigenous_environmental_defender_killing_score: 88.0, legal_title_recognition_land_rights_deficit_gap_score: 90.0, risk_level: "critique", primary_pattern: "fpic_violation_forced_displacement_scale", estimated_indigenous_land_rights_extraction_index: 9.03, last_updated: "2026-06-21" }
    { entity_id: "ILE-003", name: "Philippines/Mindanao — Lumad Schools Fermées Armée, Mines Or Terres Ancestrales, Défenseurs Tués 2020-24 & Permis Extractifs Sans FPIC", country: "Philippines", composite_score: 87.55, extractive_industry_territory_invasion_severity_score: 88.0, fpic_violation_forced_displacement_scale_score: 86.0, indigenous_environmental_defender_killing_score: 89.0, legal_title_recognition_land_rights_deficit_gap_score: 87.0, risk_level: "critique", primary_pattern: "indigenous_environmental_defender_killing", estimated_indigenous_land_rights_extraction_index: 8.75, last_updated: "2026-06-21" }
    { entity_id: "ILE-004", name: "Pérou/TIPNIS — Communautés Amazonie Expulsées Pétrole, Consultation Simulacre, Défenseurs Criminalisés & Accords Chevron Confidentiels", country: "Pérou", composite_score: 83.55, extractive_industry_territory_invasion_severity_score: 84.0, fpic_violation_forced_displacement_scale_score: 82.0, indigenous_environmental_defender_killing_score: 85.0, legal_title_recognition_land_rights_deficit_gap_score: 83.0, risk_level: "critique", primary_pattern: "extractive_industry_territory_invasion_severity", estimated_indigenous_land_rights_extraction_index: 8.36, last_updated: "2026-06-21" }
    { entity_id: "ILE-005", name: "Australie/Mines — Aboriginal Sacred Sites Destroyed Rio Tinto Juukan Gorge 2020, Native Title Contournement & Consultation Pro-Forma", country: "Australie", composite_score: 55.45, extractive_industry_territory_invasion_severity_score: 56.0, fpic_violation_forced_displacement_scale_score: 54.0, indigenous_environmental_defender_killing_score: 55.0, legal_title_recognition_land_rights_deficit_gap_score: 57.0, risk_level: "élevé", primary_pattern: "legal_title_recognition_land_rights_deficit_gap", estimated_indigenous_land_rights_extraction_index: 5.54, last_updated: "2026-06-21" }
    { entity_id: "ILE-006", name: "Kenya/Maasai — Expulsions Parc Ngorongoro, Tourisme Sans Bénéfice, Terres Ancestrales Privatisées & Cattle Confiscated", country: "Kenya", composite_score: 52.45, extractive_industry_territory_invasion_severity_score: 53.0, fpic_violation_forced_displacement_scale_score: 51.0, indigenous_environmental_defender_killing_score: 52.0, legal_title_recognition_land_rights_deficit_gap_score: 54.0, risk_level: "élevé", primary_pattern: "fpic_violation_forced_displacement_scale", estimated_indigenous_land_rights_extraction_index: 5.25, last_updated: "2026-06-21" }
    { entity_id: "ILE-007", name: "FILAC/IITC — Fonds Développement Peuples Indigènes, International Indian Treaty Council, Standards FPIC & Monitoring Mécanismes ONU", country: "Global", composite_score: 26.6, extractive_industry_territory_invasion_severity_score: 27.0, fpic_violation_forced_displacement_scale_score: 26.0, indigenous_environmental_defender_killing_score: 28.0, legal_title_recognition_land_rights_deficit_gap_score: 25.0, risk_level: "modéré", primary_pattern: "legal_title_recognition_land_rights_deficit_gap", estimated_indigenous_land_rights_extraction_index: 2.66, last_updated: "2026-06-21" }
    { entity_id: "ILE-008", name: "ONU/DRIP Terres — DRIP Art.26-32 Terres Ressources, Agenda 2030 ODD 15, Mécanisme Expert Peuples Autochtones & Rapporteur Spécial", country: "Global", composite_score: 4.0, extractive_industry_territory_invasion_severity_score: 4.0, fpic_violation_forced_displacement_scale_score: 4.0, indigenous_environmental_defender_killing_score: 4.0, legal_title_recognition_land_rights_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "extractive_industry_territory_invasion_severity", estimated_indigenous_land_rights_extraction_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/indigenous-land-rights-extraction-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
