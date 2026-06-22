import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[blood-diamond-conflict-mineral-rights] SWARM_API_URL non défini");
}

const MOCK = {
  agent: "Blood Diamond Conflict Mineral Rights Engine Agent",
  domain: "blood_diamond_conflict_mineral_rights",
  total_entities: 8,
  avg_composite: 61.08,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: { armed_group_revenue_capture: 2, civilian_forced_labor_extraction: 2, conflict_financing_supply_chain: 2, due_diligence_failure_scale: 2 },
  top_risk_entities: [
    "RDC — Maï-Maï/M23 Mines Coltan/Or Est-Congo, Travail Forcé & Financement Belligérants",
    "Sierra Leone/Libéria — Héritage Diamants du Sang, Trafic Persistant & Certif Kimberley Contournée",
    "Zimbabwe — Marange Diamonds, ZANU-PF Militarisation, Massacres 2008 & Profits Opaque",
  ],
  critical_alerts: [
    "RDC Est: armed_group_revenue_capture",
    "Zimbabwe Marange: civilian_forced_labor_extraction",
    "CAR: conflict_financing_supply_chain",
    "Myanmar Jade: due_diligence_failure_scale",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_blood_diamond_conflict_mineral_rights_index: 6.11,
  data_sources: [
    "un_panel_experts_drc_minerals_arms_embargo_violations_report",
    "kimberley_process_certification_scheme_review_civil_society",
    "global_witness_conflict_minerals_supply_chain_accountability",
  ],
  entities: [
    { id: "BD-001", name: "RDC — Maï-Maï/M23 Mines Coltan/Or Est-Congo, Travail Forcé & Financement Belligérants", country: "Afrique Centrale", composite_score: 94.1, armed_group_revenue_capture_score: 96.0, civilian_forced_labor_extraction_score: 93.0, conflict_financing_supply_chain_score: 95.0, due_diligence_failure_scale_score: 92.0, risk_level: "critique", primary_pattern: "armed_group_revenue_capture", estimated_blood_diamond_conflict_mineral_rights_index: 9.41, last_updated: "2026-06-22" },
    { id: "BD-002", name: "Zimbabwe — Marange Diamonds, ZANU-PF Militarisation, Massacres 2008 & Profits Opaques", country: "Afrique Australe", composite_score: 87.6, armed_group_revenue_capture_score: 86.0, civilian_forced_labor_extraction_score: 92.0, conflict_financing_supply_chain_score: 84.0, due_diligence_failure_scale_score: 88.0, risk_level: "critique", primary_pattern: "civilian_forced_labor_extraction", estimated_blood_diamond_conflict_mineral_rights_index: 8.76, last_updated: "2026-06-22" },
    { id: "BD-003", name: "RCA — Forces Séléka/Anti-Balaka, Mines Diamants Financement Guerre Civile & Embargo Contourné", country: "Afrique Centrale", composite_score: 86.3, armed_group_revenue_capture_score: 88.0, civilian_forced_labor_extraction_score: 82.0, conflict_financing_supply_chain_score: 92.0, due_diligence_failure_scale_score: 83.0, risk_level: "critique", primary_pattern: "conflict_financing_supply_chain", estimated_blood_diamond_conflict_mineral_rights_index: 8.63, last_updated: "2026-06-22" },
    { id: "BD-004", name: "Myanmar — Jade Kachin, Armée Tatmadaw & Milices, Travail Forcé & Blanchiment via Chine", country: "Asie du Sud-Est", composite_score: 82.9, armed_group_revenue_capture_score: 80.0, civilian_forced_labor_extraction_score: 85.0, conflict_financing_supply_chain_score: 80.0, due_diligence_failure_scale_score: 87.0, risk_level: "critique", primary_pattern: "due_diligence_failure_scale", estimated_blood_diamond_conflict_mineral_rights_index: 8.29, last_updated: "2026-06-22" },
    { id: "BD-005", name: "Sierra Leone — Post-Conflit, Trafic Résiduel Diamants Bruts, Corruption & Communautés Exclues Bénéfices", country: "Afrique de l'Ouest", composite_score: 51.7, armed_group_revenue_capture_score: 50.0, civilian_forced_labor_extraction_score: 53.0, conflict_financing_supply_chain_score: 50.0, due_diligence_failure_scale_score: 54.0, risk_level: "élevé", primary_pattern: "due_diligence_failure_scale", estimated_blood_diamond_conflict_mineral_rights_index: 5.17, last_updated: "2026-06-22" },
    { id: "BD-006", name: "Angola — Lunda Norte, Garimpeiros Expulsés Violemment & Violations SODIAM Documentées HRW", country: "Afrique Centrale", composite_score: 50.1, armed_group_revenue_capture_score: 48.0, civilian_forced_labor_extraction_score: 52.0, conflict_financing_supply_chain_score: 48.0, due_diligence_failure_scale_score: 52.0, risk_level: "élevé", primary_pattern: "civilian_forced_labor_extraction", estimated_blood_diamond_conflict_mineral_rights_index: 5.01, last_updated: "2026-06-22" },
    { id: "BD-007", name: "Processus Kimberley/OCDE DDG — Réforme Certification, Traçabilité Blockchain & Audit Indépendant", country: "Global", composite_score: 25.6, armed_group_revenue_capture_score: 24.0, civilian_forced_labor_extraction_score: 26.0, conflict_financing_supply_chain_score: 25.0, due_diligence_failure_scale_score: 27.0, risk_level: "modéré", primary_pattern: "conflict_financing_supply_chain", estimated_blood_diamond_conflict_mineral_rights_index: 2.56, last_updated: "2026-06-22" },
    { id: "BD-008", name: "Global Witness/PAX — Documentation Indépendante Minerais Sang & Plaidoyer Réforme Supply Chain", country: "Global", composite_score: 4.6, armed_group_revenue_capture_score: 4.0, civilian_forced_labor_extraction_score: 5.0, conflict_financing_supply_chain_score: 4.0, due_diligence_failure_scale_score: 6.0, risk_level: "faible", primary_pattern: "armed_group_revenue_capture", estimated_blood_diamond_conflict_mineral_rights_index: 0.46, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/blood_diamond_conflict_mineral_rights_engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
