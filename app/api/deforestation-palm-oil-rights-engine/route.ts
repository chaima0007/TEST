import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[deforestation-palm-oil-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[deforestation-palm-oil-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

export const revalidate = 30;

const MOCK = {
  engine: "DPO_ENGINE",
  domain: "deforestation_palm_oil_rights",
  total_entities: 8,
  avg_composite: 59.9,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["forest_watch_global", "rspo_certification_database", "global_deforestation_tracker"],
  entities: [
    { id: "DPO-001", name: "Palm Oil Companies Indonesia", country: "Indonésie", composite_score: 89.5, risk_level: "critique", primary_pattern: "deforestation_massive_borneo", estimated_deforestation_palm_oil_rights_index: 8.95, last_updated: "2026-06-22" },
    { id: "DPO-002", name: "Wilmar International", country: "Singapour", composite_score: 85.2, risk_level: "critique", primary_pattern: "sourcing_huile_non_certifiee", estimated_deforestation_palm_oil_rights_index: 8.52, last_updated: "2026-06-22" },
    { id: "DPO-003", name: "Cargill Palm", country: "USA", composite_score: 80.8, risk_level: "critique", primary_pattern: "destruction_habitat_orang_outan", estimated_deforestation_palm_oil_rights_index: 8.08, last_updated: "2026-06-22" },
    { id: "DPO-004", name: "Sime Darby Plantation", country: "Malaisie", composite_score: 76.4, risk_level: "critique", primary_pattern: "travail_force_plantation", estimated_deforestation_palm_oil_rights_index: 7.64, last_updated: "2026-06-22" },
    { id: "DPO-005", name: "Nestlé Supply Chain", country: "Suisse", composite_score: 55.3, risk_level: "élevé", primary_pattern: "traçabilite_huile_insuffisante", estimated_deforestation_palm_oil_rights_index: 5.53, last_updated: "2026-06-22" },
    { id: "DPO-006", name: "Unilever Palm", country: "Pays-Bas", composite_score: 51.1, risk_level: "élevé", primary_pattern: "certification_partielle_rspo", estimated_deforestation_palm_oil_rights_index: 5.11, last_updated: "2026-06-22" },
    { id: "DPO-007", name: "Ferrero CSR", country: "Italie", composite_score: 28.6, risk_level: "modéré", primary_pattern: "engagement_rspo_partiel", estimated_deforestation_palm_oil_rights_index: 2.86, last_updated: "2026-06-22" },
    { id: "DPO-008", name: "RSPO Certification", country: "Global", composite_score: 12.4, risk_level: "faible", primary_pattern: "certification_responsable_huile_palme", estimated_deforestation_palm_oil_rights_index: 1.24, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/deforestation-palm-oil-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
