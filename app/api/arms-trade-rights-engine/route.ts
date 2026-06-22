import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[arms-trade-rights-engine] SWARM_API_URL not set");

const MOCK = {
  agent: "Arms Trade Rights Engine Agent",
  domain: "arms_trade_rights",
  total_entities: 8,
  avg_composite: 60.44,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  critical_alerts: [
    "Wagner Group: illegal_arms_transfer",
    "Houthi Networks: child_soldier_recruitment",
    "Janjaweed/RSF: child_soldier_recruitment",
    "ISIS Weapons: civilian_targeting",
  ],
  data_sources: [
    "sipri_arms_transfers_database_2024",
    "un_panel_experts_reports_2024",
    "small_arms_survey_2024",
    "att_secretariat_annual_report",
  ],
  entities: [
    { id: "ATR-001", name: "Wagner Group (Russie) — Mercenaires Trafic Armes Afrique", country: "Russie/Afrique", composite_score: 93.65, risk_level: "critique", primary_pattern: "illegal_arms_transfer", estimated_arms_trade_rights_index: 9.37 },
    { id: "ATR-002", name: "Houthi Arms Networks (Yémen)", country: "Yémen", composite_score: 88.65, risk_level: "critique", primary_pattern: "child_soldier_recruitment", estimated_arms_trade_rights_index: 8.87 },
    { id: "ATR-003", name: "Janjaweed/RSF (Soudan)", country: "Soudan", composite_score: 83.55, risk_level: "critique", primary_pattern: "child_soldier_recruitment", estimated_arms_trade_rights_index: 8.36 },
    { id: "ATR-004", name: "ISIS Weapons Supply Chains", country: "International", composite_score: 77.40, risk_level: "critique", primary_pattern: "civilian_targeting", estimated_arms_trade_rights_index: 7.74 },
    { id: "ATR-005", name: "Saudi Arabia Arms Purchases (BAE Systems/USA)", country: "Arabie Saoudite", composite_score: 53.90, risk_level: "élevé", primary_pattern: "illegal_arms_transfer", estimated_arms_trade_rights_index: 5.39 },
    { id: "ATR-006", name: "USA Military-Industrial Complex (Lockheed/Raytheon)", country: "États-Unis", composite_score: 46.40, risk_level: "élevé", primary_pattern: "conflict_perpetuation", estimated_arms_trade_rights_index: 4.64 },
    { id: "ATR-007", name: "UN Arms Embargo Monitoring", country: "International", composite_score: 29.30, risk_level: "modéré", primary_pattern: "conflict_perpetuation", estimated_arms_trade_rights_index: 2.93 },
    { id: "ATR-008", name: "ICAN / ATT Treaty Framework", country: "International", composite_score: 10.65, risk_level: "faible", primary_pattern: "conflict_perpetuation", estimated_arms_trade_rights_index: 1.07 },
  ],
};

export async function GET() {
  try {
    const upstream = await fetch(`${SWARM_API_URL}/arms-trade-rights-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 });
  }
}
