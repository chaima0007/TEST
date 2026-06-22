import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[performanceadvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/performanceadvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "performanceadvertising-advertising",
      entities: [
        { name: "Google Performance Max", composite_score: 94.50, risk_level: "critique", estimated_index: 9.45 },
        { name: "Meta Advantage+ Shopping", composite_score: 87.30, risk_level: "critique", estimated_index: 8.73 },
        { name: "Amazon Sponsored Products", composite_score: 79.80, risk_level: "critique", estimated_index: 7.98 },
        { name: "TikTok Performance Ads", composite_score: 68.40, risk_level: "critique", estimated_index: 6.84 },
        { name: "Snapchat Dynamic Ads", composite_score: 55.20, risk_level: "élevé", estimated_index: 5.52 },
        { name: "LinkedIn Lead Gen Forms", composite_score: 46.70, risk_level: "élevé", estimated_index: 4.67 },
        { name: "Pinterest Shopping Campaigns", composite_score: 31.10, risk_level: "modéré", estimated_index: 3.11 },
        { name: "Twitter Promoted Tweets", composite_score: 13.40, risk_level: "faible", estimated_index: 1.34 },
      ],
      avg_composite: 59.55,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
