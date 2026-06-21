import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Internet Freedom Censorship Engine Agent",
  domain: "internet_freedom_censorship",
  total_entities: 8,
  avg_composite: 62.58,
  confidence_score: 0.87,
  avg_estimated_internet_freedom_censorship_index: 6.26,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "freedom_house_freedom_net_internet_2023",
    "netblocks_internet_shutdown_tracker_2023",
    "article_19_internet_freedom_report_2023",
    "access_now_keepiton_report_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[internet-freedom-censorship-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/internet-freedom-censorship-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
