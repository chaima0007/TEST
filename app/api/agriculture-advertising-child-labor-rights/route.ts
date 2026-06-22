import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[agriculture-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/agriculture_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Cargill", composite_score: 97, risk_level: "critique", estimated_index: 9.7 },
        { name: "ADM", composite_score: 91, risk_level: "critique", estimated_index: 9.1 },
        { name: "Bunge", composite_score: 84, risk_level: "critique", estimated_index: 8.4 },
        { name: "Louis Dreyfus", composite_score: 79, risk_level: "critique", estimated_index: 7.9 },
        { name: "Nestlé Agri", composite_score: 62, risk_level: "élevé", estimated_index: 6.2 },
        { name: "Syngenta", composite_score: 53, risk_level: "élevé", estimated_index: 5.3 },
        { name: "Bayer CropScience", composite_score: 31, risk_level: "modéré", estimated_index: 3.1 },
        { name: "BASF Agro", composite_score: 11, risk_level: "faible", estimated_index: 1.1 },
      ],
      avg_composite: 63.50,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
