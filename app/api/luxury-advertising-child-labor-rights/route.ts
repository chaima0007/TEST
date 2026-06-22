import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[luxury-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/luxury_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "LVMH", composite_score: 98, risk_level: "critique", estimated_index: 9.8 },
        { name: "Richemont", composite_score: 91, risk_level: "critique", estimated_index: 9.1 },
        { name: "Kering", composite_score: 84, risk_level: "critique", estimated_index: 8.4 },
        { name: "Hermès", composite_score: 79, risk_level: "critique", estimated_index: 7.9 },
        { name: "Chanel", composite_score: 62, risk_level: "élevé", estimated_index: 6.2 },
        { name: "Prada", composite_score: 51, risk_level: "élevé", estimated_index: 5.1 },
        { name: "Burberry", composite_score: 33, risk_level: "modéré", estimated_index: 3.3 },
        { name: "Rolex", composite_score: 14, risk_level: "faible", estimated_index: 1.4 },
      ],
      avg_composite: 64.00,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
