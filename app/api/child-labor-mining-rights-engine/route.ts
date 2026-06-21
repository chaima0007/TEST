import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[child-labor-mining-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Child Labor Mining Rights Engine Agent",
  domain: "child_labor_mining_rights",
  total_entities: 8,
  avg_composite: 62.01,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { hazardous_child_mining_prevalence: 4, supply_chain_corporate_impunity_scale: 2, legal_enforcement_child_labor_mining_gap: 2 },
  top_risk_entities: [
    "RDC/Cobalt — 40 000 Enfants Mines Artisanales, Chaîne EV Batteries & Impunité Multinationales",
    "Ghana/Or Artisanal — Galamsey Enfants 8-14 Ans, Mercure & Zéro Scolarisation",
    "Inde/Mica — Mica Cosmétiques & Électronique, Enfants Jharkhand, Mines Clandestines",
  ],
  critical_alerts: [
    "RDC/Cobalt: hazardous_child_mining_prevalence",
    "Ghana/Or Artisanal: hazardous_child_mining_prevalence",
    "Inde/Mica: supply_chain_corporate_impunity_scale",
    "Philippines/Or-Charbon: hazardous_child_mining_prevalence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_child_labor_mining_rights_index: 6.20,
  data_sources: [
    "amnesty_international_cobalt_child_labor_drc_mining_report",
    "ilo_ipec_child_labour_mining_hazardous_work_global_report",
    "somo_centre_research_multinationals_child_labor_minerals_report",
  ],
  entities: [
    { id: "CLM-001", name: "RDC/Cobalt — 40 000 Enfants Mines Artisanales, Chaîne EV Batteries & Impunité Multinationales", country: "RDC", sector: "Mines Cobalt Artisanales", composite_score: 94.45, hazardous_child_mining_prevalence_score: 97.0, supply_chain_corporate_impunity_scale_score: 95.0, school_access_child_miner_exclusion_score: 92.0, legal_enforcement_child_labor_mining_gap_score: 93.0, risk_level: "critique", primary_pattern: "hazardous_child_mining_prevalence", estimated_child_labor_mining_rights_index: 9.45, last_updated: "2026-06-21" },
    { id: "CLM-002", name: "Ghana/Or Artisanal — Galamsey Enfants 8-14 Ans, Mercure & Zéro Scolarisation", country: "Ghana", sector: "Mines Or Galamsey", composite_score: 91.2, hazardous_child_mining_prevalence_score: 94.0, supply_chain_corporate_impunity_scale_score: 91.0, school_access_child_miner_exclusion_score: 89.0, legal_enforcement_child_labor_mining_gap_score: 90.0, risk_level: "critique", primary_pattern: "hazardous_child_mining_prevalence", estimated_child_labor_mining_rights_index: 9.12, last_updated: "2026-06-21" },
    { id: "CLM-003", name: "Inde/Mica — Mica Cosmétiques & Électronique, Enfants Jharkhand, Mines Clandestines", country: "Inde", sector: "Mines Mica Clandestines", composite_score: 88.2, hazardous_child_mining_prevalence_score: 91.0, supply_chain_corporate_impunity_scale_score: 88.0, school_access_child_miner_exclusion_score: 86.0, legal_enforcement_child_labor_mining_gap_score: 87.0, risk_level: "critique", primary_pattern: "supply_chain_corporate_impunity_scale", estimated_child_labor_mining_rights_index: 8.82, last_updated: "2026-06-21" },
    { id: "CLM-004", name: "Philippines/Or-Charbon — Tunnel Mining Enfants, Accidents Mortels & DENR Inefficace", country: "Philippines", sector: "Mines Tunnel Artisanales", composite_score: 85.2, hazardous_child_mining_prevalence_score: 88.0, supply_chain_corporate_impunity_scale_score: 85.0, school_access_child_miner_exclusion_score: 83.0, legal_enforcement_child_labor_mining_gap_score: 84.0, risk_level: "critique", primary_pattern: "hazardous_child_mining_prevalence", estimated_child_labor_mining_rights_index: 8.52, last_updated: "2026-06-21" },
    { id: "CLM-005", name: "Bolivie/Étain-Argent — Cerro Rico Enfants, Pression Économique Familiale & Syndicats Miniers", country: "Bolivie", sector: "Mines Cerro Rico", composite_score: 54.2, hazardous_child_mining_prevalence_score: 57.0, supply_chain_corporate_impunity_scale_score: 54.0, school_access_child_miner_exclusion_score: 52.0, legal_enforcement_child_labor_mining_gap_score: 53.0, risk_level: "élevé", primary_pattern: "legal_enforcement_child_labor_mining_gap", estimated_child_labor_mining_rights_index: 5.42, last_updated: "2026-06-21" },
    { id: "CLM-006", name: "Mali/Or Artisanal — Conflit Armé & Mines, Enfants Recrutés & Zéro Protection", country: "Mali", sector: "Mines Or Zones Conflit", composite_score: 52.2, hazardous_child_mining_prevalence_score: 55.0, supply_chain_corporate_impunity_scale_score: 52.0, school_access_child_miner_exclusion_score: 50.0, legal_enforcement_child_labor_mining_gap_score: 51.0, risk_level: "élevé", primary_pattern: "hazardous_child_mining_prevalence", estimated_child_labor_mining_rights_index: 5.22, last_updated: "2026-06-21" },
    { id: "CLM-007", name: "IPEC/Stop Child Labor — Programme ILO, Certification Minière Responsable & Due Diligence", country: "Global", sector: "Certification & Plaidoyer", composite_score: 26.55, hazardous_child_mining_prevalence_score: 28.0, supply_chain_corporate_impunity_scale_score: 25.0, school_access_child_miner_exclusion_score: 26.0, legal_enforcement_child_labor_mining_gap_score: 27.0, risk_level: "modéré", primary_pattern: "supply_chain_corporate_impunity_scale", estimated_child_labor_mining_rights_index: 2.66, last_updated: "2026-06-21" },
    { id: "CLM-008", name: "ONU/ILO C182 — Convention Pires Formes Travail Enfants, SDG 8.7 & Accord Volontaire", country: "Global", sector: "Cadre Normatif International", composite_score: 4.1, hazardous_child_mining_prevalence_score: 5.0, supply_chain_corporate_impunity_scale_score: 4.0, school_access_child_miner_exclusion_score: 4.0, legal_enforcement_child_labor_mining_gap_score: 3.0, risk_level: "faible", primary_pattern: "legal_enforcement_child_labor_mining_gap", estimated_child_labor_mining_rights_index: 0.41, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-labor-mining-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
