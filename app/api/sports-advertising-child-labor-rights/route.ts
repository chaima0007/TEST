import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sports-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sports_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Nike", composite_score: 97, risk_level: "critique", estimated_index: 9.7 },
        { name: "Adidas", composite_score: 89, risk_level: "critique", estimated_index: 8.9 },
        { name: "Puma", composite_score: 83, risk_level: "critique", estimated_index: 8.3 },
        { name: "Under Armour", composite_score: 76, risk_level: "critique", estimated_index: 7.6 },
        { name: "New Balance", composite_score: 63, risk_level: "élevé", estimated_index: 6.3 },
        { name: "Reebok", composite_score: 52, risk_level: "élevé", estimated_index: 5.2 },
        { name: "ASICS", composite_score: 31, risk_level: "modéré", estimated_index: 3.1 },
        { name: "Fila", composite_score: 15, risk_level: "faible", estimated_index: 1.5 },
      ],
      avg_composite: 63.25,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
