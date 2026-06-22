import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[migrant-detention-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Migrant Detention Engine Agent",
  domain: "migrant_detention",
  total_entities: 8,
  avg_composite: 59.04,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { indefinite_detention_scale: 1, detention_conditions: 2, deportation_refoulement_risk: 3, legal_aid_denial: 2 },
  top_risk_entities: [
    "Australie — Offshore Detention Manus/Nauru, Détention Indéfinie & Refoulement Systématique",
    "USA/ICE — Centres Détention Privés, Séparation Familles & Conditions Inhumaines Frontière",
    "UE/Libye — Externalisation Migration, Garde-Côtes Libyens & Centres Détention Tortures",
  ],
  critical_alerts: [
    "Australie: indefinite_detention_scale",
    "USA/ICE: detention_conditions",
    "UE/Libye: deportation_refoulement_risk",
    "Mexique: deportation_refoulement_risk",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_migrant_detention_index: 5.9,
  data_sources: [
    "global_detention_project_immigration_detention_global_report",
    "human_rights_watch_immigration_enforcement_detention_report_annual",
    "unhcr_detention_guidelines_asylum_seekers_stateless_persons",
  ],
  entities: [
    { id: "MD-001", name: "Australie — Offshore Detention Manus/Nauru, Détention Indéfinie & Refoulement Systématique", country: "Océanie", composite_score: 88.9, detention_conditions_score: 88.0, indefinite_detention_scale_score: 92.0, deportation_refoulement_risk_score: 90.0, legal_aid_denial_score: 85.0, risk_level: "critique", primary_pattern: "indefinite_detention_scale", estimated_migrant_detention_index: 8.89, last_updated: "2026-06-20" },
    { id: "MD-002", name: "USA/ICE — Centres Détention Privés, Séparation Familles & Conditions Inhumaines Frontière", country: "Amérique du Nord", composite_score: 85.15, detention_conditions_score: 85.0, indefinite_detention_scale_score: 88.0, deportation_refoulement_risk_score: 85.0, legal_aid_denial_score: 82.0, risk_level: "critique", primary_pattern: "detention_conditions", estimated_migrant_detention_index: 8.52, last_updated: "2026-06-20" },
    { id: "MD-003", name: "UE/Libye — Externalisation Migration, Garde-Côtes Libyens & Centres Détention Tortures", country: "Afrique du Nord/Europe", composite_score: 83.85, detention_conditions_score: 82.0, indefinite_detention_scale_score: 85.0, deportation_refoulement_risk_score: 88.0, legal_aid_denial_score: 80.0, risk_level: "critique", primary_pattern: "deportation_refoulement_risk", estimated_migrant_detention_index: 8.39, last_updated: "2026-06-20" },
    { id: "MD-004", name: "Mexique — INM Centres Détention, Violence Gardes & Complicité Trafiquants", country: "Amérique Centrale", composite_score: 78.9, detention_conditions_score: 78.0, indefinite_detention_scale_score: 80.0, deportation_refoulement_risk_score: 82.0, legal_aid_denial_score: 75.0, risk_level: "critique", primary_pattern: "deportation_refoulement_risk", estimated_migrant_detention_index: 7.89, last_updated: "2026-06-20" },
    { id: "MD-005", name: "Turquie — 3,5M Réfugiés Syriens, Refoulements Frontière & Centres Surpeuplés", country: "Europe de l'Est", composite_score: 53.85, detention_conditions_score: 52.0, indefinite_detention_scale_score: 55.0, deportation_refoulement_risk_score: 58.0, legal_aid_denial_score: 50.0, risk_level: "élevé", primary_pattern: "deportation_refoulement_risk", estimated_migrant_detention_index: 5.39, last_updated: "2026-06-20" },
    { id: "MD-006", name: "Maroc/Algérie — Expulsions Massives Subsahariens, Violence & Absence Recours Légaux", country: "Afrique du Nord", composite_score: 51.15, detention_conditions_score: 48.0, indefinite_detention_scale_score: 52.0, deportation_refoulement_risk_score: 55.0, legal_aid_denial_score: 50.0, risk_level: "élevé", primary_pattern: "legal_aid_denial", estimated_migrant_detention_index: 5.12, last_updated: "2026-06-20" },
    { id: "MD-007", name: "Canada — Détention Arbitraire Limitée, Alternatives Détention & Réforme Partielle", country: "Amérique du Nord", composite_score: 26.1, detention_conditions_score: 22.0, indefinite_detention_scale_score: 28.0, deportation_refoulement_risk_score: 30.0, legal_aid_denial_score: 25.0, risk_level: "modéré", primary_pattern: "detention_conditions", estimated_migrant_detention_index: 2.61, last_updated: "2026-06-20" },
    { id: "MD-008", name: "HCR/ONU — Principes Directeurs Détention, Règles Mandela & Alternatives à la Détention", country: "Global", composite_score: 4.4, detention_conditions_score: 4.0, indefinite_detention_scale_score: 5.0, deportation_refoulement_risk_score: 3.0, legal_aid_denial_score: 6.0, risk_level: "faible", primary_pattern: "legal_aid_denial", estimated_migrant_detention_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/migrant-detention-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
