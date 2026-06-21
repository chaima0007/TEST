import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Malnutrition Child Nutrition Rights Engine Agent",
  domain: "malnutrition_child_nutrition_rights",
  total_entities: 8,
  avg_composite: 63.50,
  confidence_score: 0.89,
  avg_estimated_malnutrition_child_nutrition_rights_index: 6.35,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "unicef_malnutrition_report_2023",
    "who_global_nutrition_targets_2023",
    "world_food_programme_hunger_map_2023",
    "lancet_child_nutrition_series_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[malnutrition-child-nutrition-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/malnutrition-child-nutrition-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
