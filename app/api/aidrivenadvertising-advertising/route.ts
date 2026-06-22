import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[aidrivenadvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/aidrivenadvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "aidrivenadvertising-advertising",
      entities: [
        { name: "Meta Advantage+ AI Ads", composite_score: 96.30, risk_level: "critique", estimated_aidrivenadvertising_index: 9.63 },
        { name: "Google Performance Max", composite_score: 88.50, risk_level: "critique", estimated_aidrivenadvertising_index: 8.85 },
        { name: "Amazon Sponsored AI", composite_score: 80.70, risk_level: "critique", estimated_aidrivenadvertising_index: 8.07 },
        { name: "Adobe Advertising AI", composite_score: 73.90, risk_level: "critique", estimated_aidrivenadvertising_index: 7.39 },
        { name: "Basis Technologies AI", composite_score: 56.40, risk_level: "élevé", estimated_aidrivenadvertising_index: 5.64 },
        { name: "Quantcast AI Targeting", composite_score: 45.80, risk_level: "élevé", estimated_aidrivenadvertising_index: 4.58 },
        { name: "Choozle AI Campaigns", composite_score: 27.30, risk_level: "modéré", estimated_aidrivenadvertising_index: 2.73 },
        { name: "Simpli.fi AI Bidding", composite_score: 13.60, risk_level: "faible", estimated_aidrivenadvertising_index: 1.36 },
      ],
      avg_composite: 60.32,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
