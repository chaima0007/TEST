import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[palm-oil-peatland-rights] SWARM_API_URL is not set — falling back to mock data");
}

export const revalidate = 30;

const MOCK = {
  engine: "POPR_ENGINE",
  domain: "palm_oil_peatland_rights",
  total_entities: 8,
  avg_composite: 61.44,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["global_peatland_initiative", "rspo_peatland_compliance_db", "gfw_peatland_destruction_index"],
  entities: [
    { id: "POPR-001", name: "Astra Agro Lestari", country: "Indonésie", composite_score: 91.2, risk_level: "critique", primary_pattern: "drainage_tourbieres_borneo_illegal", estimated_palm_oil_peatland_rights_index: 9.12, last_updated: "2026-06-22" },
    { id: "POPR-002", name: "IOI Group Malaysia", country: "Malaisie", composite_score: 86.5, risk_level: "critique", primary_pattern: "destruction_ecosysteme_tourbiere_sarawak", estimated_palm_oil_peatland_rights_index: 8.65, last_updated: "2026-06-22" },
    { id: "POPR-003", name: "Bumitama Agri", country: "Indonésie", composite_score: 81.3, risk_level: "critique", primary_pattern: "expansion_plantation_zones_protegees", estimated_palm_oil_peatland_rights_index: 8.13, last_updated: "2026-06-22" },
    { id: "POPR-004", name: "Salim Group Palm", country: "Indonésie", composite_score: 76.8, risk_level: "critique", primary_pattern: "incendies_tourbieres_non_declares", estimated_palm_oil_peatland_rights_index: 7.68, last_updated: "2026-06-22" },
    { id: "POPR-005", name: "Kuala Lumpur Kepong", country: "Malaisie", composite_score: 53.7, risk_level: "élevé", primary_pattern: "compensation_communautes_indigenes_insuffisante", estimated_palm_oil_peatland_rights_index: 5.37, last_updated: "2026-06-22" },
    { id: "POPR-006", name: "Musim Mas Holdings", country: "Singapour", composite_score: 48.9, risk_level: "élevé", primary_pattern: "traçabilite_supply_chain_incomplete", estimated_palm_oil_peatland_rights_index: 4.89, last_updated: "2026-06-22" },
    { id: "POPR-007", name: "Apical Group", country: "Singapour", composite_score: 29.1, risk_level: "modéré", primary_pattern: "engagement_no_deforestation_partiel", estimated_palm_oil_peatland_rights_index: 2.91, last_updated: "2026-06-22" },
    { id: "POPR-008", name: "Peatland Conservation Initiative", country: "Global", composite_score: 11.5, risk_level: "faible", primary_pattern: "restauration_tourbieres_certifiee", estimated_palm_oil_peatland_rights_index: 1.15, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/palm-oil-peatland-rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
