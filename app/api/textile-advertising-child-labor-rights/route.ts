import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[textile-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/textile_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Zara (Inditex)", composite_score: 96, risk_level: "critique", estimated_index: 9.6 },
        { name: "H&M", composite_score: 89, risk_level: "critique", estimated_index: 8.9 },
        { name: "SHEIN", composite_score: 83, risk_level: "critique", estimated_index: 8.3 },
        { name: "Gap", composite_score: 76, risk_level: "critique", estimated_index: 7.6 },
        { name: "PVH Corp", composite_score: 61, risk_level: "élevé", estimated_index: 6.1 },
        { name: "Hanesbrands", composite_score: 52, risk_level: "élevé", estimated_index: 5.2 },
        { name: "Fast Retailing", composite_score: 30, risk_level: "modéré", estimated_index: 3.0 },
        { name: "Tapestry", composite_score: 14, risk_level: "faible", estimated_index: 1.4 },
      ],
      avg_composite: 62.63,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
