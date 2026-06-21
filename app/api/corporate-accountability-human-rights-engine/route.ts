import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[corporate-accountability-human-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Corporate Accountability Human Rights Engine Agent",
  domain: "corporate_accountability_human_rights",
  total_entities: 8,
  avg_composite: 61.93,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { environmental_destruction_community_displacement_scale: 2, supply_chain_forced_labor_complicity_severity: 2, corporate_impunity_legal_accountability_gap: 2, human_rights_due_diligence_failure_deficit_gap: 2 },
  top_risk_entities: [
    "Shell/Nigeria — Delta Niger Pollution 50 Ans, Ogoni 9 Pendus 1995, Droits Eau Détruits & Aucune Réparation Judiciaire",
    "Apple/Foxconn — Suicides Ouvriers Chine 2010, Filets Anti-Suicide, Travail Enfant Cobalt RDC & Conditions 12h/Jour",
    "Nestlé/Cacao — Travail Enfant Côte d'Ivoire 1.5M, Cacao Certifié Mensonger, Poursuites USA Rejetées & Chaîne Opaque",
  ],
  critical_alerts: [
    "Shell/Nigeria: environmental_destruction_community_displacement_scale",
    "Apple/Foxconn: supply_chain_forced_labor_complicity_severity",
    "Nestlé/Cacao: corporate_impunity_legal_accountability_gap",
    "BP/Deepwater: environmental_destruction_community_displacement_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_corporate_accountability_human_rights_index: 6.19,
  data_sources: [
    "un_guiding_principles_business_human_rights",
    "corporate_accountability_lab_supply_chain_report",
    "amnesty_international_corporate_complicity_report",
  ],
  entities: [
    { id: "CAH-001", name: "Shell/Nigeria — Delta Niger Pollution 50 Ans, Ogoni 9 Pendus 1995, Droits Eau Détruits & Aucune Réparation Judiciaire", country: "Nigeria", composite_score: 94.55, supply_chain_forced_labor_complicity_severity_score: 95.0, environmental_destruction_community_displacement_scale_score: 96.0, corporate_impunity_legal_accountability_gap_score: 93.0, human_rights_due_diligence_failure_deficit_gap_score: 94.0, risk_level: "critique", primary_pattern: "environmental_destruction_community_displacement_scale", estimated_corporate_accountability_human_rights_index: 9.46, last_updated: "2026-06-21" },
    { id: "CAH-002", name: "Apple/Foxconn — Suicides Ouvriers Chine 2010, Filets Anti-Suicide, Travail Enfant Cobalt RDC & Conditions 12h/Jour", country: "Chine", composite_score: 91.15, supply_chain_forced_labor_complicity_severity_score: 92.0, environmental_destruction_community_displacement_scale_score: 90.0, corporate_impunity_legal_accountability_gap_score: 93.0, human_rights_due_diligence_failure_deficit_gap_score: 89.0, risk_level: "critique", primary_pattern: "supply_chain_forced_labor_complicity_severity", estimated_corporate_accountability_human_rights_index: 9.12, last_updated: "2026-06-21" },
    { id: "CAH-003", name: "Nestlé/Cacao — Travail Enfant Côte d'Ivoire 1.5M, Cacao Certifié Mensonger, Poursuites USA Rejetées & Chaîne Opaque", country: "Côte d'Ivoire", composite_score: 87.6, supply_chain_forced_labor_complicity_severity_score: 88.0, environmental_destruction_community_displacement_scale_score: 87.0, corporate_impunity_legal_accountability_gap_score: 89.0, human_rights_due_diligence_failure_deficit_gap_score: 86.0, risk_level: "critique", primary_pattern: "corporate_impunity_legal_accountability_gap", estimated_corporate_accountability_human_rights_index: 8.76, last_updated: "2026-06-21" },
    { id: "CAH-004", name: "BP/Deepwater — Marée Noire 2010 Golfe Mexique, Pêcheurs Ruinés, Compensations Insuffisantes & Lobbying Déréglementation", country: "USA", composite_score: 83.55, supply_chain_forced_labor_complicity_severity_score: 84.0, environmental_destruction_community_displacement_scale_score: 85.0, corporate_impunity_legal_accountability_gap_score: 82.0, human_rights_due_diligence_failure_deficit_gap_score: 83.0, risk_level: "critique", primary_pattern: "environmental_destruction_community_displacement_scale", estimated_corporate_accountability_human_rights_index: 8.36, last_updated: "2026-06-21" },
    { id: "CAH-005", name: "Amazon/Entrepôts — Blessures 2× Industrie, Surveillance Algorithmes, Syndicalistes Licenciés & Conditions Chaleur Létale", country: "USA", composite_score: 55.45, supply_chain_forced_labor_complicity_severity_score: 56.0, environmental_destruction_community_displacement_scale_score: 54.0, corporate_impunity_legal_accountability_gap_score: 55.0, human_rights_due_diligence_failure_deficit_gap_score: 57.0, risk_level: "élevé", primary_pattern: "human_rights_due_diligence_failure_deficit_gap", estimated_corporate_accountability_human_rights_index: 5.55, last_updated: "2026-06-21" },
    { id: "CAH-006", name: "Volkswagen/Dieselgate — Émissions Frauduleuses, Santé Communautés Autoroutes, Amendes Sans Prison & Victimes Non Indemnisées", country: "Allemagne", composite_score: 52.55, supply_chain_forced_labor_complicity_severity_score: 53.0, environmental_destruction_community_displacement_scale_score: 51.0, corporate_impunity_legal_accountability_gap_score: 54.0, human_rights_due_diligence_failure_deficit_gap_score: 52.0, risk_level: "élevé", primary_pattern: "corporate_impunity_legal_accountability_gap", estimated_corporate_accountability_human_rights_index: 5.26, last_updated: "2026-06-21" },
    { id: "CAH-007", name: "UNGP/OCDE — Principes Directeurs ONU Entreprises Droits Humains, Lignes OCDE, Devoir Vigilance France & CSDDD EU", country: "Global", composite_score: 26.6, supply_chain_forced_labor_complicity_severity_score: 27.0, environmental_destruction_community_displacement_scale_score: 26.0, corporate_impunity_legal_accountability_gap_score: 28.0, human_rights_due_diligence_failure_deficit_gap_score: 25.0, risk_level: "modéré", primary_pattern: "human_rights_due_diligence_failure_deficit_gap", estimated_corporate_accountability_human_rights_index: 2.66, last_updated: "2026-06-21" },
    { id: "CAH-008", name: "ISO/GRI — ISO 26000 RSE, GRI Standards Rapportage, B-Corp Certification & Initiative Reporting Mondial", country: "Global", composite_score: 4.0, supply_chain_forced_labor_complicity_severity_score: 4.0, environmental_destruction_community_displacement_scale_score: 4.0, corporate_impunity_legal_accountability_gap_score: 4.0, human_rights_due_diligence_failure_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "supply_chain_forced_labor_complicity_severity", estimated_corporate_accountability_human_rights_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/corporate-accountability-human-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
