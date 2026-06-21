import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Nonconsensual Intimate Image Abuse Engine Agent",
  domain: "nonconsensual_intimate_image_abuse",
  total_entities: 8,
  avg_composite: 54.85,
  confidence_score: 0.89,
  avg_estimated_nonconsensual_intimate_image_abuse_index: 5.49,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["cyber_civil_rights_initiative_2023","revenge_porn_helpline_2023","europol_image_abuse_2022","un_women_online_violence_2022"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[nonconsensual-intimate-image-abuse-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nonconsensual-intimate-image-abuse-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
