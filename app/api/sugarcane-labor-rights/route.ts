import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[sugarcane-labor-rights] SWARM_API_URL is not set — falling back to mock data");
}

export const revalidate = 30;

const MOCK = {
  engine: "SLR_ENGINE",
  domain: "sugarcane_labor_rights",
  total_entities: 8,
  avg_composite: 61.25,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["ilo_sugarcane_labor_reports", "fair_trade_certification_db", "sugarcane_workers_global_index"],
  entities: [
    { id: "SLR-001", name: "Mitr Phol Sugar Corp", country: "Thaïlande", composite_score: 88.7, risk_level: "critique", primary_pattern: "travail_force_coupe_canne", estimated_sugarcane_labor_rights_index: 8.87, last_updated: "2026-06-22" },
    { id: "SLR-002", name: "Raizen Brazil", country: "Brésil", composite_score: 84.3, risk_level: "critique", primary_pattern: "conditions_travail_inhumaines_plantation", estimated_sugarcane_labor_rights_index: 8.43, last_updated: "2026-06-22" },
    { id: "SLR-003", name: "Illovo Sugar Africa", country: "Afrique du Sud", composite_score: 79.6, risk_level: "critique", primary_pattern: "travail_enfant_canne_malawi", estimated_sugarcane_labor_rights_index: 7.96, last_updated: "2026-06-22" },
    { id: "SLR-004", name: "Central Romana Corp", country: "République Dominicaine", composite_score: 74.1, risk_level: "critique", primary_pattern: "servitude_dette_travailleurs_haitiens", estimated_sugarcane_labor_rights_index: 7.41, last_updated: "2026-06-22" },
    { id: "SLR-005", name: "Fanjul Corp", country: "USA", composite_score: 54.8, risk_level: "élevé", primary_pattern: "violation_droits_travailleur_migrant", estimated_sugarcane_labor_rights_index: 5.48, last_updated: "2026-06-22" },
    { id: "SLR-006", name: "EID Parry India", country: "Inde", composite_score: 49.2, risk_level: "élevé", primary_pattern: "absence_contrat_travail_formel", estimated_sugarcane_labor_rights_index: 4.92, last_updated: "2026-06-22" },
    { id: "SLR-007", name: "Complant Sugarcane", country: "Éthiopie", composite_score: 27.4, risk_level: "modéré", primary_pattern: "salaire_insuffisant_coupeurs_canne", estimated_sugarcane_labor_rights_index: 2.74, last_updated: "2026-06-22" },
    { id: "SLR-008", name: "Fairtrade Sugar Coop", country: "Maurice", composite_score: 11.8, risk_level: "faible", primary_pattern: "certification_equitable_reconnue", estimated_sugarcane_labor_rights_index: 1.18, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/sugarcane-labor-rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
