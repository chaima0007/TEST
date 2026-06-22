import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[carboncapture-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/carboncapture_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Direct Air Capture Corp", composite_score: 95.6, risk_level: "critique", estimated_carboncapture_index: 9.56 },
        { name: "Carbon Storage Systems", composite_score: 89.65, risk_level: "critique", estimated_carboncapture_index: 8.97 },
        { name: "CCS Equipment MFG", composite_score: 81.75, risk_level: "critique", estimated_carboncapture_index: 8.18 },
        { name: "Point Source Capture Ltd", composite_score: 76.6, risk_level: "critique", estimated_carboncapture_index: 7.66 },
        { name: "Carbon Pipeline Network", composite_score: 58.15, risk_level: "élevé", estimated_carboncapture_index: 5.82 },
        { name: "Sequestration Tech Inc", composite_score: 48.15, risk_level: "élevé", estimated_carboncapture_index: 4.82 },
        { name: "Mineral Carbonation Co", composite_score: 29.0, risk_level: "modéré", estimated_carboncapture_index: 2.9 },
        { name: "Raw Material Supply", composite_score: 9.9, risk_level: "faible", estimated_carboncapture_index: 0.99 },
      ],
      avg_composite: 61.03,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
