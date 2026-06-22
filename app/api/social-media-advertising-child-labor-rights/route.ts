import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[social-media-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/social_media_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Facebook Ads", composite_score: 99, risk_level: "critique", estimated_index: 9.9 },
        { name: "Instagram Ads", composite_score: 93, risk_level: "critique", estimated_index: 9.3 },
        { name: "TikTok Ads", composite_score: 85, risk_level: "critique", estimated_index: 8.5 },
        { name: "Twitter/X Ads", composite_score: 80, risk_level: "critique", estimated_index: 8.0 },
        { name: "Snapchat Ads", composite_score: 61, risk_level: "élevé", estimated_index: 6.1 },
        { name: "Pinterest Ads", composite_score: 51, risk_level: "élevé", estimated_index: 5.1 },
        { name: "LinkedIn Ads", composite_score: 32, risk_level: "modéré", estimated_index: 3.2 },
        { name: "BeReal Ads", composite_score: 13, risk_level: "faible", estimated_index: 1.3 },
      ],
      avg_composite: 61.02,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
