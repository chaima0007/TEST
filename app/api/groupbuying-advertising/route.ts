import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[groupbuying-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/groupbuying_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Group Buy Platform Corp", composite_score: 95.6, risk_level: "critique", estimated_groupbuying_index: 9.56 },
        { name: "Bulk Manufacturer Direct", composite_score: 89.65, risk_level: "critique", estimated_groupbuying_index: 8.97 },
        { name: "Community Purchase Tech", composite_score: 81.75, risk_level: "critique", estimated_groupbuying_index: 8.18 },
        { name: "Volume Discount Systems", composite_score: 76.6, risk_level: "critique", estimated_groupbuying_index: 7.66 },
        { name: "Collective Order Ops", composite_score: 58.15, risk_level: "élevé", estimated_groupbuying_index: 5.82 },
        { name: "Cooperative Supply Co", composite_score: 48.15, risk_level: "élevé", estimated_groupbuying_index: 4.82 },
        { name: "Local Distribution Co", composite_score: 29.0, risk_level: "modéré", estimated_groupbuying_index: 2.9 },
        { name: "Factory Direct Labor", composite_score: 9.9, risk_level: "faible", estimated_groupbuying_index: 0.99 },
      ],
      avg_composite: 61.03,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
