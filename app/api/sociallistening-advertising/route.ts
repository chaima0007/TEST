import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sociallistening-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sociallistening_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "sociallistening-advertising",
      entities: [
        { name: "Brandwatch Consumer Research", composite_score: 93.10, risk_level: "critique", estimated_index: 9.31 },
        { name: "Sprout Social Listening", composite_score: 85.45, risk_level: "critique", estimated_index: 8.55 },
        { name: "Mention Real-Time Monitoring", composite_score: 78.20, risk_level: "critique", estimated_index: 7.82 },
        { name: "Hootsuite Insights", composite_score: 67.30, risk_level: "critique", estimated_index: 6.73 },
        { name: "Talkwalker Social Intelligence", composite_score: 54.80, risk_level: "élevé", estimated_index: 5.48 },
        { name: "Meltwater Media Monitoring", composite_score: 44.60, risk_level: "élevé", estimated_index: 4.46 },
        { name: "Keyhole Hashtag Analytics", composite_score: 27.90, risk_level: "modéré", estimated_index: 2.79 },
        { name: "Awario Brand Monitoring", composite_score: 11.30, risk_level: "faible", estimated_index: 1.13 },
      ],
      avg_composite: 57.83,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
