import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[anti-corruption-rights-engine] SWARM_API_URL not set");

const FALLBACK = {
  agent: "Anti-Corruption Rights Engine",
  domain: "anti_corruption_rights",
  avg_composite: 61.77,
  confidence_score: 0.87,
  total_entities: 8,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  critical_alerts: [
    "Somalia:bribery_systemic",
    "Syria:public_fund_embezzlement",
    "Venezuela:judicial_corruption",
    "Libya:bribery_systemic",
  ],
  data_sources: [
    "transparency_international_cpi_2024",
    "un_convention_against_corruption",
    "world_bank_governance_indicators_2024",
    "global_integrity_report_2024",
  ],
  estimated_anti_corruption_rights_index: 6.18,
  entities: [
    { id: "ACR-001", name: "Somalia — IPC 11/100 Dernier Rang Monde, État Défaillant Total", country: "Somalie", composite_score: 90.90, risk_level: "critique", primary_pattern: "bribery_systemic", estimated_anti_corruption_rights_index: 9.09 },
    { id: "ACR-002", name: "Syria — Corruption Guerre Civile, Fonds Humanitaires Détournés", country: "Syrie", composite_score: 88.00, risk_level: "critique", primary_pattern: "public_fund_embezzlement", estimated_anti_corruption_rights_index: 8.80 },
    { id: "ACR-003", name: "Venezuela — Corruption PDVSA 300Mds$, CPI 170/180", country: "Venezuela", composite_score: 89.10, risk_level: "critique", primary_pattern: "judicial_corruption", estimated_anti_corruption_rights_index: 8.91 },
    { id: "ACR-004", name: "Libya — Corruption Milices, Pétrole Pillé, Institutions Inexistantes", country: "Libye", composite_score: 85.70, risk_level: "critique", primary_pattern: "bribery_systemic", estimated_anti_corruption_rights_index: 8.57 },
    { id: "ACR-005", name: "Mexico — Cartels Corrompent Fonctionnaires, Impunité 97%", country: "Mexique", composite_score: 54.80, risk_level: "élevé", primary_pattern: "anti_corruption_institution_weakness", estimated_anti_corruption_rights_index: 5.48 },
    { id: "ACR-006", name: "Brazil — Lava Jato, Petrobras, Recul Anticorruption 2019-2023", country: "Brésil", composite_score: 48.40, risk_level: "élevé", primary_pattern: "judicial_corruption", estimated_anti_corruption_rights_index: 4.84 },
    { id: "ACR-007", name: "EU Anticorruption — OLAF Partiellement Efficace, Lacunes Est", country: "Union Européenne", composite_score: 29.10, risk_level: "modéré", primary_pattern: "anti_corruption_institution_weakness", estimated_anti_corruption_rights_index: 2.91 },
    { id: "ACR-008", name: "Denmark/Finland/NZ — IPC 1-3 Meilleure Pratique Mondiale", country: "Danemark/Finlande/NZ", composite_score: 8.15, risk_level: "faible", primary_pattern: "bribery_systemic", estimated_anti_corruption_rights_index: 0.82 },
  ],
};

export async function GET() {
  try {
    const upstream = await fetch(`${SWARM_API_URL}/anti-corruption-rights-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(FALLBACK), { status: 502 });
  }
}
