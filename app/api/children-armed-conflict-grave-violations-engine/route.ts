import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Children Armed Conflict Grave Violations Engine Agent",
  domain: "children_armed_conflict_grave_violations",
  total_entities: 8,
  avg_composite: 62.43,
  confidence_score: 0.90,
  avg_estimated_children_conflict_index: 6.24,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_security_council_children_armed_conflict_mailing_2023",
    "unicef_grave_violations_monitoring_2023",
    "save_the_children_conflict_impact_2022",
    "watchlist_children_armed_conflict_2023",
  ],
  critical_alerts: [],
  entities: [
    {
      id: "SD-001",
      name: "Sudan — RSF & SAF Conflict",
      composite_score: 91.65,
      risk_level: "critique",
      estimated_children_conflict_index: 9.17,
    },
    {
      id: "CD-002",
      name: "DRC — Eastern Congo (M23 / FDLR)",
      composite_score: 88.4,
      risk_level: "critique",
      estimated_children_conflict_index: 8.84,
    },
    {
      id: "MM-003",
      name: "Myanmar — Junta & Armed Groups",
      composite_score: 87.15,
      risk_level: "critique",
      estimated_children_conflict_index: 8.71,
    },
    {
      id: "YE-004",
      name: "Yemen — Houthi & Coalition Forces",
      composite_score: 84.65,
      risk_level: "critique",
      estimated_children_conflict_index: 8.46,
    },
    {
      id: "SO-005",
      name: "Somalia — Al-Shabaab & Clan Violence",
      composite_score: 52.15,
      risk_level: "élevé",
      estimated_children_conflict_index: 5.21,
    },
    {
      id: "ML-006",
      name: "Mali — Sahel Jihadist Groups",
      composite_score: 49.45,
      risk_level: "élevé",
      estimated_children_conflict_index: 4.95,
    },
    {
      id: "CO-007",
      name: "Colombia — FARC Dissidents & ELN",
      composite_score: 34.35,
      risk_level: "modéré",
      estimated_children_conflict_index: 3.44,
    },
    {
      id: "SL-008",
      name: "Sierra Leone — Post-War Recovery Model",
      composite_score: 11.65,
      risk_level: "faible",
      estimated_children_conflict_index: 1.17,
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[children-armed-conflict-grave-violations-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/children-armed-conflict-grave-violations-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
