import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[tokenadvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/tokenadvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "tokenadvertising-advertising",
      entities: [
        { name: "BAT Token Rewards", composite_score: 96.20, risk_level: "critique", estimated_tokenadvertising_index: 9.62 },
        { name: "Theta Ad Token", composite_score: 89.10, risk_level: "critique", estimated_tokenadvertising_index: 8.91 },
        { name: "Chiliz Fan Token Ads", composite_score: 81.70, risk_level: "critique", estimated_tokenadvertising_index: 8.17 },
        { name: "Rally Creator Tokens", composite_score: 75.50, risk_level: "critique", estimated_tokenadvertising_index: 7.55 },
        { name: "Audius Token Ads", composite_score: 57.30, risk_level: "élevé", estimated_tokenadvertising_index: 5.73 },
        { name: "Social Token Network", composite_score: 46.90, risk_level: "élevé", estimated_tokenadvertising_index: 4.69 },
        { name: "NFT Ad Marketplace", composite_score: 26.80, risk_level: "modéré", estimated_tokenadvertising_index: 2.68 },
        { name: "Micro-Token Ad Layer", composite_score: 12.40, risk_level: "faible", estimated_tokenadvertising_index: 1.24 },
      ],
      avg_composite: 61.03,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
