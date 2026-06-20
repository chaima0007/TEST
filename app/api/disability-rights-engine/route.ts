import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[disability-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Disability Rights Engine Agent",
  domain: "disability_rights",
  total_entities: 8,
  avg_composite: 59.2,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { institutionalization_forced: 2, legal_capacity_deprivation: 2, accessibility_infrastructure_failure: 2, crpd_implementation_gap: 2 },
  top_risk_entities: [
    "Russie/Europe Est — Internats Psychiatriques, Tutelle Abusive & Isolement Institutionnel Massif",
    "Chine — Système Hukou Exclus Handicap, Internats Forcés & Stérilisations Non Consenties",
    "Afrique Sub-Saharienne — Exorcismes/Guérisseurs, Abandon Famille, Exclusion Éducation & Pauvreté",
  ],
  critical_alerts: [
    "Russie/Europe Est: institutionalization_forced",
    "Chine: legal_capacity_deprivation",
    "Afrique Sub-Saharienne: accessibility_infrastructure_failure",
    "Inde: accessibility_infrastructure_failure",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_disability_rights_index: 5.92,
  data_sources: [
    "human_rights_watch_disability_institutionalization_global_report",
    "mental_disability_rights_international_global_report",
    "un_crpd_committee_state_party_reviews_concluding_observations",
  ],
  entities: [
    { entity_id: "DR-001", name: "Russie/Europe Est — Internats Psychiatriques, Tutelle Abusive & Isolement Institutionnel Massif", country: "Europe de l'Est", composite_score: 89.7, institutionalization_forced_score: 92.0, accessibility_infrastructure_failure_score: 88.0, legal_capacity_deprivation_score: 90.0, crpd_implementation_gap_score: 88.0, risk_level: "critique", primary_pattern: "institutionalization_forced", estimated_disability_rights_index: 8.97, last_updated: "2026-06-20" },
    { entity_id: "DR-002", name: "Chine — Système Hukou Exclus Handicap, Internats Forcés & Stérilisations Non Consenties", country: "Asie du Nord-Est", composite_score: 86.65, institutionalization_forced_score: 88.0, accessibility_infrastructure_failure_score: 85.0, legal_capacity_deprivation_score: 88.0, crpd_implementation_gap_score: 85.0, risk_level: "critique", primary_pattern: "legal_capacity_deprivation", estimated_disability_rights_index: 8.67, last_updated: "2026-06-20" },
    { entity_id: "DR-003", name: "Afrique Sub-Saharienne — Exorcismes/Guérisseurs, Abandon Famille, Exclusion Éducation & Pauvreté", country: "Afrique Sub-Saharienne", composite_score: 84.5, institutionalization_forced_score: 85.0, accessibility_infrastructure_failure_score: 88.0, legal_capacity_deprivation_score: 80.0, crpd_implementation_gap_score: 85.0, risk_level: "critique", primary_pattern: "accessibility_infrastructure_failure", estimated_disability_rights_index: 8.45, last_updated: "2026-06-20" },
    { entity_id: "DR-004", name: "Inde — Loi Personnes Handicap 2016 Non Appliquée, Stigmatisation Mentale & Institutions Vétustes", country: "Asie du Sud", composite_score: 80.4, institutionalization_forced_score: 80.0, accessibility_infrastructure_failure_score: 82.0, legal_capacity_deprivation_score: 78.0, crpd_implementation_gap_score: 82.0, risk_level: "critique", primary_pattern: "accessibility_infrastructure_failure", estimated_disability_rights_index: 8.04, last_updated: "2026-06-20" },
    { entity_id: "DR-005", name: "USA — ADA Gaps, Prisons Personnes Handicap Mental, Pauvreté & Inégalités Accès Soins", country: "Amérique du Nord", composite_score: 53.45, institutionalization_forced_score: 52.0, accessibility_infrastructure_failure_score: 50.0, legal_capacity_deprivation_score: 55.0, crpd_implementation_gap_score: 58.0, risk_level: "élevé", primary_pattern: "crpd_implementation_gap", estimated_disability_rights_index: 5.35, last_updated: "2026-06-20" },
    { entity_id: "DR-006", name: "UE/Désinstitutionnalisation — Fonds Structurels Mal Utilisés, Progrès Inégaux & CDPH Violations", country: "Europe", composite_score: 48.65, institutionalization_forced_score: 48.0, accessibility_infrastructure_failure_score: 45.0, legal_capacity_deprivation_score: 52.0, crpd_implementation_gap_score: 50.0, risk_level: "élevé", primary_pattern: "crpd_implementation_gap", estimated_disability_rights_index: 4.87, last_updated: "2026-06-20" },
    { entity_id: "DR-007", name: "IDA/Inclusion International — Alliance Mondiale, Désinstitutionnalisation & Vie Indépendante", country: "Global", composite_score: 25.85, institutionalization_forced_score: 22.0, accessibility_infrastructure_failure_score: 25.0, legal_capacity_deprivation_score: 28.0, crpd_implementation_gap_score: 30.0, risk_level: "modéré", primary_pattern: "institutionalization_forced", estimated_disability_rights_index: 2.59, last_updated: "2026-06-20" },
    { entity_id: "DR-008", name: "ONU/CDPH — Convention Droits Personnes Handicapées 2006, Comité & Protocole Facultatif", country: "Global", composite_score: 4.4, institutionalization_forced_score: 4.0, accessibility_infrastructure_failure_score: 5.0, legal_capacity_deprivation_score: 3.0, crpd_implementation_gap_score: 6.0, risk_level: "faible", primary_pattern: "legal_capacity_deprivation", estimated_disability_rights_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/disability-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
