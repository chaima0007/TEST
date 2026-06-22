import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[video-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/video_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "YouTube Ads", composite_score: 99, risk_level: "critique", estimated_index: 9.9 },
        { name: "Meta Video Ads", composite_score: 93, risk_level: "critique", estimated_index: 9.3 },
        { name: "TikTok Video Ads", composite_score: 85, risk_level: "critique", estimated_index: 8.5 },
        { name: "Snapchat Video Ads", composite_score: 80, risk_level: "critique", estimated_index: 8.0 },
        { name: "Twitter/X Video Ads", composite_score: 61, risk_level: "élevé", estimated_index: 6.1 },
        { name: "LinkedIn Video Ads", composite_score: 51, risk_level: "élevé", estimated_index: 5.1 },
        { name: "Pinterest Video Ads", composite_score: 32, risk_level: "modéré", estimated_index: 3.2 },
        { name: "Amazon Video Ads", composite_score: 13, risk_level: "faible", estimated_index: 1.3 },
      ],
      avg_composite: 61.02,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
