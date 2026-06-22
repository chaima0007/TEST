import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[creatoreconomy-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/creatoreconomy_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "creatoreconomy-advertising",
      entities: [
        { name: "YouTube Partner Program", composite_score: 94.10, risk_level: "critique", estimated_creatoreconomy_index: 9.41 },
        { name: "TikTok Creator Fund", composite_score: 86.30, risk_level: "critique", estimated_creatoreconomy_index: 8.63 },
        { name: "Instagram Creator Marketplace", composite_score: 78.50, risk_level: "critique", estimated_creatoreconomy_index: 7.85 },
        { name: "Twitch Affiliate Program", composite_score: 71.20, risk_level: "critique", estimated_creatoreconomy_index: 7.12 },
        { name: "Patreon Revenue Share", composite_score: 54.80, risk_level: "élevé", estimated_creatoreconomy_index: 5.48 },
        { name: "Substack Creator Ads", composite_score: 44.60, risk_level: "élevé", estimated_creatoreconomy_index: 4.46 },
        { name: "OnlyFans Creator Platform", composite_score: 28.40, risk_level: "modéré", estimated_creatoreconomy_index: 2.84 },
        { name: "Gumroad Creator Tools", composite_score: 14.20, risk_level: "faible", estimated_creatoreconomy_index: 1.42 },
      ],
      avg_composite: 59.01,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
