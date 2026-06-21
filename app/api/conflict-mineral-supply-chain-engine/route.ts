import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[conflict-mineral-supply-chain-engine] SWARM_API_URL not set — using mock data");
}

const MOCK = {
  domain: "conflict_mineral_supply_chain",
  generated_at: new Date().toISOString(),
  accent: "#dc2626",
  avg_composite: 61.92,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    { id: "CMS-001", name: "DRC — Cobalt & Coltan Est-Congo, Financement Groupes Armés", composite_score: 93.20, risk_level: "critique", conflict_zone_sourcing_score: 97, armed_group_financing_score: 95, due_diligence_compliance_score: 91, artisanal_miner_protection_score: 88, estimated_conflict_mineral_supply_chain_index: 9.32 },
    { id: "CMS-002", name: "Myanmar — Jade & Rubis Kachin, Financement Armée & Milices", composite_score: 89.05, risk_level: "critique", conflict_zone_sourcing_score: 92, armed_group_financing_score: 90, due_diligence_compliance_score: 87, artisanal_miner_protection_score: 86, estimated_conflict_mineral_supply_chain_index: 8.90 },
    { id: "CMS-003", name: "Sudan/South Sudan — Or Darfour, Financement Milices Janjawid", composite_score: 85.75, risk_level: "critique", conflict_zone_sourcing_score: 90, armed_group_financing_score: 88, due_diligence_compliance_score: 83, artisanal_miner_protection_score: 80, estimated_conflict_mineral_supply_chain_index: 8.58 },
    { id: "CMS-004", name: "Zimbabwe — Chrome & Diamants Marange, Exploitation Militaire", composite_score: 82.10, risk_level: "critique", conflict_zone_sourcing_score: 85, armed_group_financing_score: 83, due_diligence_compliance_score: 81, artisanal_miner_protection_score: 78, estimated_conflict_mineral_supply_chain_index: 8.21 },
    { id: "CMS-005", name: "Colombie — Or Illégal Zones FARC, Blanchiment", composite_score: 56.80, risk_level: "élevé", conflict_zone_sourcing_score: 62, armed_group_financing_score: 58, due_diligence_compliance_score: 54, artisanal_miner_protection_score: 51, estimated_conflict_mineral_supply_chain_index: 5.68 },
    { id: "CMS-006", name: "Pérou — Or Madre de Dios, Orpaillage Illégal & Mercure", composite_score: 52.25, risk_level: "élevé", conflict_zone_sourcing_score: 57, armed_group_financing_score: 53, due_diligence_compliance_score: 50, artisanal_miner_protection_score: 47, estimated_conflict_mineral_supply_chain_index: 5.23 },
    { id: "CMS-007", name: "Bolivie — Étain Coopératives, Formalisation Partielle", composite_score: 28.15, risk_level: "modéré", conflict_zone_sourcing_score: 32, armed_group_financing_score: 29, due_diligence_compliance_score: 26, artisanal_miner_protection_score: 24, estimated_conflict_mineral_supply_chain_index: 2.82 },
    { id: "CMS-008", name: "Canada — Normes RSDC, Traçabilité Blockchain Minière", composite_score: 8.05, risk_level: "faible", conflict_zone_sourcing_score: 9, armed_group_financing_score: 8, due_diligence_compliance_score: 7, artisanal_miner_protection_score: 8, estimated_conflict_mineral_supply_chain_index: 0.81 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/conflict-mineral-supply-chain-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
