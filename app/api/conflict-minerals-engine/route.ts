import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[conflict-minerals-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Conflict Minerals Engine Agent",
  domain: "conflict_minerals",
  total_entities: 8,
  avg_composite: 60.89,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { armed_group_financing_scale: 2, supply_chain_due_diligence_failure: 2, civilian_exploitation_harm: 1, corporate_accountability_gap: 3 },
  top_risk_entities: [
    "RDC/3TG — Coltan Financement M23/FDLR, 200K Mineurs Artisanaux & Apple/Samsung Chaîne Opaque",
    "RDC/Cobalt — 70% Réserves Mondiales, Glencore/Artisanal, 40K Enfants Mines & Tesla Due Diligence",
    "Birmanie/Jade & Rubis — Armée Financement Coup État 2021, Kachin & Myanmar Gems Sanctionnées",
  ],
  critical_alerts: [
    "RDC/3TG: armed_group_financing_scale",
    "RDC/Cobalt: supply_chain_due_diligence_failure",
    "Birmanie/Jade & Rubis: civilian_exploitation_harm",
    "Mali/Or: corporate_accountability_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_conflict_minerals_index: 6.09,
  data_sources: [
    "un_group_experts_drc_conflict_minerals_sanctions_report",
    "global_witness_ipis_mining_conflict_supply_chain_database",
    "oecd_due_diligence_guidance_responsible_mineral_supply_chains",
  ],
  entities: [
    { id: "CM-001", name: "RDC/3TG — Coltan Financement M23/FDLR, 200K Mineurs Artisanaux & Apple/Samsung Chaîne Opaque", country: "Afrique Centrale", composite_score: 92.5, armed_group_financing_scale_score: 95.0, supply_chain_due_diligence_failure_score: 92.0, civilian_exploitation_harm_score: 92.0, corporate_accountability_gap_score: 90.0, risk_level: "critique", primary_pattern: "armed_group_financing_scale", estimated_conflict_minerals_index: 9.25, last_updated: "2026-06-21" },
    { id: "CM-002", name: "RDC/Cobalt — 70% Réserves Mondiales, Glencore/Artisanal, 40K Enfants Mines & Tesla Due Diligence", country: "Afrique Centrale", composite_score: 89.6, armed_group_financing_scale_score: 90.0, supply_chain_due_diligence_failure_score: 92.0, civilian_exploitation_harm_score: 88.0, corporate_accountability_gap_score: 88.0, risk_level: "critique", primary_pattern: "supply_chain_due_diligence_failure", estimated_conflict_minerals_index: 8.96, last_updated: "2026-06-21" },
    { id: "CM-003", name: "Birmanie/Jade & Rubis — Armée Financement Coup État 2021, Kachin & Myanmar Gems Sanctionnées", country: "Asie du Sud-Est", composite_score: 86.65, armed_group_financing_scale_score: 88.0, supply_chain_due_diligence_failure_score: 85.0, civilian_exploitation_harm_score: 88.0, corporate_accountability_gap_score: 85.0, risk_level: "critique", primary_pattern: "civilian_exploitation_harm", estimated_conflict_minerals_index: 8.67, last_updated: "2026-06-21" },
    { id: "CM-004", name: "Mali/Or — Groupes Armés Jihadistes Taxation Mines, WAGENINGEN Rapport & Sanctions OFAC", country: "Afrique de l'Ouest", composite_score: 84.25, armed_group_financing_scale_score: 85.0, supply_chain_due_diligence_failure_score: 85.0, civilian_exploitation_harm_score: 82.0, corporate_accountability_gap_score: 85.0, risk_level: "critique", primary_pattern: "corporate_accountability_gap", estimated_conflict_minerals_index: 8.43, last_updated: "2026-06-21" },
    { id: "CM-005", name: "Rwanda — Coltan Ré-Export RDC, OCCRP Rapport Blanchiment Minéraux & Pression Diplomatique", country: "Afrique de l'Est", composite_score: 53.5, armed_group_financing_scale_score: 55.0, supply_chain_due_diligence_failure_score: 52.0, civilian_exploitation_harm_score: 52.0, corporate_accountability_gap_score: 55.0, risk_level: "élevé", primary_pattern: "supply_chain_due_diligence_failure", estimated_conflict_minerals_index: 5.35, last_updated: "2026-06-21" },
    { id: "CM-006", name: "UE/Règlement Minerais Conflit 2021 & Dodd-Frank 1502 — Enforcement Lacunaire & Portée Limitée", country: "Global", composite_score: 50.4, armed_group_financing_scale_score: 50.0, supply_chain_due_diligence_failure_score: 52.0, civilian_exploitation_harm_score: 48.0, corporate_accountability_gap_score: 52.0, risk_level: "élevé", primary_pattern: "corporate_accountability_gap", estimated_conflict_minerals_index: 5.04, last_updated: "2026-06-21" },
    { id: "CM-007", name: "Global Witness/IPIS — Cartographie Mines Conflit, Monitoring Chaînes Approvisionnement & Plaidoyer", country: "Global", composite_score: 25.85, armed_group_financing_scale_score: 22.0, supply_chain_due_diligence_failure_score: 28.0, civilian_exploitation_harm_score: 25.0, corporate_accountability_gap_score: 30.0, risk_level: "modéré", primary_pattern: "corporate_accountability_gap", estimated_conflict_minerals_index: 2.59, last_updated: "2026-06-21" },
    { id: "CM-008", name: "ONU/GE RDC — Rapport Experts Groupe Sanctions, Résolution 1533 & Mécanisme Suivi Minerais", country: "Global", composite_score: 4.4, armed_group_financing_scale_score: 4.0, supply_chain_due_diligence_failure_score: 5.0, civilian_exploitation_harm_score: 3.0, corporate_accountability_gap_score: 6.0, risk_level: "faible", primary_pattern: "armed_group_financing_scale", estimated_conflict_minerals_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/conflict-minerals-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
