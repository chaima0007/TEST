import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[hyperlocaladvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/hyperlocaladvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "hyperlocaladvertising-advertising",
      entities: [
        { name: "Foursquare Location Ads", composite_score: 94.20, risk_level: "critique", estimated_hyperlocaladvertising_index: 9.42 },
        { name: "Near Intelligence Geo-Ads", composite_score: 85.60, risk_level: "critique", estimated_hyperlocaladvertising_index: 8.56 },
        { name: "GroundTruth Hyperlocal", composite_score: 77.40, risk_level: "critique", estimated_hyperlocaladvertising_index: 7.74 },
        { name: "Unacast Proximity Ads", composite_score: 68.90, risk_level: "critique", estimated_hyperlocaladvertising_index: 6.89 },
        { name: "Blis Geo-Fencing Platform", composite_score: 52.30, risk_level: "élevé", estimated_hyperlocaladvertising_index: 5.23 },
        { name: "Factual Audience Targeting", composite_score: 44.70, risk_level: "élevé", estimated_hyperlocaladvertising_index: 4.47 },
        { name: "Reveal Mobile Local Ads", composite_score: 28.50, risk_level: "modéré", estimated_hyperlocaladvertising_index: 2.85 },
        { name: "Outfront SmartSCOUT", composite_score: 12.10, risk_level: "faible", estimated_hyperlocaladvertising_index: 1.21 },
      ],
      avg_composite: 57.97,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
