import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[freedom-assembly-association-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Freedom of Assembly Association Rights Engine Agent",
  domain: "freedom_assembly_association_rights",
  total_entities: 8,
  avg_composite: 62.81,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { assembly_permit_restriction_deficit_gap: 2, protest_crackdown_violence_severity: 2, civil_society_ngo_criminalization: 2, union_suppression_labor_rights_scale: 2 },
  top_risk_entities: [
    "Chine/Tiananmen Héritage — Hong Kong NSL 2019, Interdiction Totale Assemblée & Syndicats Contrôlés",
    "Biélorussie/Loukachenko 2020 — 35k Manifestants Arrêtés, Syndicats Interdits & ONG Liquidées",
    "Myanmar/Tatmadaw Coup — Syndicats Interdits, Manifestants Tués & Société Civile Clandestine",
  ],
  critical_alerts: [
    "Chine/Tiananmen Héritage: assembly_permit_restriction_deficit_gap",
    "Biélorussie/Loukachenko 2020: protest_crackdown_violence_severity",
    "Myanmar/Tatmadaw Coup: union_suppression_labor_rights_scale",
    "Iran/Mahsa Amini: civil_society_ngo_criminalization",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_freedom_assembly_association_rights_index: 6.28,
  data_sources: [
    "civicus_monitor_annual_report_civic_space_freedom_assembly_association",
    "un_special_rapporteur_rights_peaceful_assembly_freedom_association_reports",
    "amnesty_international_human_rights_watch_protest_crackdown_global_review",
  ],
  entities: [
    { id: "FAAR-001", name: "Chine/Tiananmen Héritage — Hong Kong NSL 2019, Interdiction Totale Assemblée & Syndicats Contrôlés", country: "Asie du Nord-Est", composite_score: 94.2, protest_crackdown_violence_severity_score: 95.0, union_suppression_labor_rights_scale_score: 92.0, civil_society_ngo_criminalization_score: 94.0, assembly_permit_restriction_deficit_gap_score: 96.0, risk_level: "critique", primary_pattern: "assembly_permit_restriction_deficit_gap", estimated_freedom_assembly_association_rights_index: 9.42, last_updated: "2026-06-21" },
    { id: "FAAR-002", name: "Biélorussie/Loukachenko 2020 — 35k Manifestants Arrêtés, Syndicats Interdits & ONG Liquidées", country: "Europe de l'Est", composite_score: 90.7, protest_crackdown_violence_severity_score: 92.0, union_suppression_labor_rights_scale_score: 90.0, civil_society_ngo_criminalization_score: 92.0, assembly_permit_restriction_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "protest_crackdown_violence_severity", estimated_freedom_assembly_association_rights_index: 9.07, last_updated: "2026-06-21" },
    { id: "FAAR-003", name: "Iran/Mahsa Amini — 500 Morts Manifestations 2022, Répression Syndicale & Criminalisation Société Civile", country: "Moyen-Orient", composite_score: 88.5, protest_crackdown_violence_severity_score: 90.0, union_suppression_labor_rights_scale_score: 88.0, civil_society_ngo_criminalization_score: 90.0, assembly_permit_restriction_deficit_gap_score: 85.0, risk_level: "critique", primary_pattern: "civil_society_ngo_criminalization", estimated_freedom_assembly_association_rights_index: 8.85, last_updated: "2026-06-21" },
    { id: "FAAR-004", name: "Myanmar/Tatmadaw Coup — Syndicats Interdits, Manifestants Tués & Société Civile Clandestine", country: "Asie du Sud-Est", composite_score: 89.4, protest_crackdown_violence_severity_score: 88.0, union_suppression_labor_rights_scale_score: 92.0, civil_society_ngo_criminalization_score: 88.0, assembly_permit_restriction_deficit_gap_score: 90.0, risk_level: "critique", primary_pattern: "union_suppression_labor_rights_scale", estimated_freedom_assembly_association_rights_index: 8.94, last_updated: "2026-06-21" },
    { id: "FAAR-005", name: "Russie/Anti-Guerre — 16k Manifestants Arrêtés 2022, Loi Discrédit Armée & ONG Agents Étrangers", country: "Europe de l'Est", composite_score: 56.9, protest_crackdown_violence_severity_score: 58.0, union_suppression_labor_rights_scale_score: 52.0, civil_society_ngo_criminalization_score: 62.0, assembly_permit_restriction_deficit_gap_score: 55.0, risk_level: "élevé", primary_pattern: "civil_society_ngo_criminalization", estimated_freedom_assembly_association_rights_index: 5.69, last_updated: "2026-06-21" },
    { id: "FAAR-006", name: "Thaïlande/Lèse-Majesté — Jeunesse Pro-Démocratie Arrêtée, Restriction Assemblée & Syndicats Limités", country: "Asie du Sud-Est", composite_score: 52.25, protest_crackdown_violence_severity_score: 48.0, union_suppression_labor_rights_scale_score: 55.0, civil_society_ngo_criminalization_score: 50.0, assembly_permit_restriction_deficit_gap_score: 58.0, risk_level: "élevé", primary_pattern: "assembly_permit_restriction_deficit_gap", estimated_freedom_assembly_association_rights_index: 5.23, last_updated: "2026-06-21" },
    { id: "FAAR-007", name: "CIVICUS/FIDH Monitor — Espace Civique Rétrécissant, Rapports Annuels Assemblée Pacifique", country: "Global", composite_score: 24.9, protest_crackdown_violence_severity_score: 24.0, union_suppression_labor_rights_scale_score: 28.0, civil_society_ngo_criminalization_score: 22.0, assembly_permit_restriction_deficit_gap_score: 26.0, risk_level: "modéré", primary_pattern: "union_suppression_labor_rights_scale", estimated_freedom_assembly_association_rights_index: 2.49, last_updated: "2026-06-21" },
    { id: "FAAR-008", name: "ONU/PIDCP Art.21-22 — Droit Réunion & Association, Rapporteur Spécial Libertés Fondamentales", country: "Global", composite_score: 5.6, protest_crackdown_violence_severity_score: 5.0, union_suppression_labor_rights_scale_score: 6.0, civil_society_ngo_criminalization_score: 4.0, assembly_permit_restriction_deficit_gap_score: 8.0, risk_level: "faible", primary_pattern: "protest_crackdown_violence_severity", estimated_freedom_assembly_association_rights_index: 0.56, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/freedom-assembly-association-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
