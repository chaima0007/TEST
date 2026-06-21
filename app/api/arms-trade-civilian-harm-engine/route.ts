import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Arms Trade Civilian Harm Engine Agent",
  domain: "arms_trade_civilian_harm",
  total_entities: 8,
  avg_composite: 61.81,
  confidence_score: 0.88,
  avg_estimated_arms_trade_civilian_harm_index: 6.18,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["sipri_arms_transfers_database_2023","action_on_armed_violence_ewipa_report_2023","amnesty_international_arms_trade_report_2023","arms_control_association_att_implementation_2023"],
  critical_alerts: [],
  entities: [
    { entity_id: "ATCH-001", name: "Yémen/Coalition Arabie Saoudite — bombes à sous-munitions UK/US, frappes hôpitaux & marchés documentées", composite_score: 93.15, risk_level: "critique", estimated_arms_trade_civilian_harm_index: 9.32 },
    { entity_id: "ATCH-002", name: "Myanmar — armes importées utilisées génocide Rohingya, junta armée post-coup 2021", composite_score: 86.35, risk_level: "critique", estimated_arms_trade_civilian_harm_index: 8.64 },
    { entity_id: "ATCH-003", name: "Soudan — RSF armée par Émirats, massacres Darfour 2023-2024, embargo violé ouvertement", composite_score: 87.55, risk_level: "critique", estimated_arms_trade_civilian_harm_index: 8.76 },
    { entity_id: "ATCH-004", name: "Libye — embargo ONU violé par multiples acteurs, milices armées, civils victimes trafics", composite_score: 85.2, risk_level: "critique", estimated_arms_trade_civilian_harm_index: 8.52 },
    { entity_id: "ATCH-005", name: "Ukraine/Russie — EWIPA massif zones peuplées, armes à sous-munitions Russie, usage civils illicite", composite_score: 59.4, risk_level: "élevé", estimated_arms_trade_civilian_harm_index: 5.94 },
    { entity_id: "ATCH-006", name: "Philippines — armes US utilisées guerre drogue extrajudiciaire, 30 000 morts impunité Duterte", composite_score: 50.15, risk_level: "élevé", estimated_arms_trade_civilian_harm_index: 5.02 },
    { entity_id: "ATCH-007", name: "Brésil — armes légères trafiquées vers favelas, détournements stocks militaires documentés", composite_score: 28.65, risk_level: "modéré", estimated_arms_trade_civilian_harm_index: 2.87 },
    { entity_id: "ATCH-008", name: "Norvège — politique stricte transferts armes, rapport ATT exemplaire, aucune vente régimes abusifs", composite_score: 4.0, risk_level: "faible", estimated_arms_trade_civilian_harm_index: 0.4 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[arms-trade-civilian-harm-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/arms-trade-civilian-harm-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
