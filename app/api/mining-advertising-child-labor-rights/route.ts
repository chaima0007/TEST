import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[mining-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/mining_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Glencore", composite_score: 98, risk_level: "critique", estimated_index: 9.8 },
        { name: "Rio Tinto", composite_score: 92, risk_level: "critique", estimated_index: 9.2 },
        { name: "BHP", composite_score: 86, risk_level: "critique", estimated_index: 8.6 },
        { name: "Anglo American", composite_score: 77, risk_level: "critique", estimated_index: 7.7 },
        { name: "Vale", composite_score: 64, risk_level: "élevé", estimated_index: 6.4 },
        { name: "Freeport-McMoRan", composite_score: 55, risk_level: "élevé", estimated_index: 5.5 },
        { name: "Barrick Gold", composite_score: 29, risk_level: "modéré", estimated_index: 2.9 },
        { name: "Newmont", composite_score: 12, risk_level: "faible", estimated_index: 1.2 },
      ],
      avg_composite: 64.13,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
