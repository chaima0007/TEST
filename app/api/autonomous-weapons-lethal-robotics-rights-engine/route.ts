import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Autonomous Weapons Lethal Robotics Rights Engine Agent",
  domain: "autonomous_weapons_lethal_robotics_rights",
  total_entities: 8,
  avg_composite: 57.91,
  confidence_score: 0.87,
  avg_estimated_autonomous_weapons_lethal_robotics_rights_index: 5.79,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "campaign_to_stop_killer_robots_2023",
    "icrc_autonomous_weapons_2023",
    "un_group_governmental_experts_laws_2022",
    "article36_autonomous_weapons_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[autonomous-weapons-lethal-robotics-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/autonomous-weapons-lethal-robotics-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
