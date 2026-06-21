import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Climate Finance Loss & Damage Rights Engine Agent",
  domain: "climate_finance_loss_damage_rights",
  total_entities: 8,
  avg_composite: 61.26,
  confidence_score: 0.89,
  avg_estimated_climate_finance_loss_damage_index: 6.13,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "unfccc_loss_damage_fund_cop28_2023",
    "ipcc_ar6_climate_impacts_2022",
    "v20_vulnerable_twenty_finance_gap_2023",
    "loss_damage_collaboration_tracker_2023",
  ],
  critical_alerts: [],
  entities: [
    {
      id: "BD-001",
      name: "Bangladesh",
      composite_score: 86.1,
      risk_level: "critique",
      estimated_climate_finance_loss_damage_index: 8.61,
    },
    {
      id: "PK-002",
      name: "Pakistan",
      composite_score: 84.8,
      risk_level: "critique",
      estimated_climate_finance_loss_damage_index: 8.48,
    },
    {
      id: "MZ-003",
      name: "Mozambique",
      composite_score: 84.15,
      risk_level: "critique",
      estimated_climate_finance_loss_damage_index: 8.42,
    },
    {
      id: "TV-004",
      name: "Tuvalu",
      composite_score: 91.55,
      risk_level: "critique",
      estimated_climate_finance_loss_damage_index: 9.15,
    },
    {
      id: "PH-005",
      name: "Philippines",
      composite_score: 48.7,
      risk_level: "élevé",
      estimated_climate_finance_loss_damage_index: 4.87,
    },
    {
      id: "HN-006",
      name: "Honduras",
      composite_score: 46.4,
      risk_level: "élevé",
      estimated_climate_finance_loss_damage_index: 4.64,
    },
    {
      id: "FJ-007",
      name: "Fiji",
      composite_score: 38.05,
      risk_level: "modéré",
      estimated_climate_finance_loss_damage_index: 3.8,
    },
    {
      id: "EU-LD-008",
      name: "EU Loss and Damage Fund Pledges",
      composite_score: 10.35,
      risk_level: "faible",
      estimated_climate_finance_loss_damage_index: 1.03,
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[climate-finance-loss-damage-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate-finance-loss-damage-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
