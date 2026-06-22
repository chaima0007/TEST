import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[healthcare-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/healthcare_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Johnson & Johnson", composite_score: 95.2, risk_level: "critique", estimated_index: 9.52 },
        { name: "Pfizer", composite_score: 89.45, risk_level: "critique", estimated_index: 8.95 },
        { name: "Roche", composite_score: 81.95, risk_level: "critique", estimated_index: 8.20 },
        { name: "Novartis", composite_score: 76.95, risk_level: "critique", estimated_index: 7.70 },
        { name: "Bayer", composite_score: 57.95, risk_level: "élevé", estimated_index: 5.80 },
        { name: "Abbott", composite_score: 47.95, risk_level: "élevé", estimated_index: 4.80 },
        { name: "Sanofi", composite_score: 28.95, risk_level: "modéré", estimated_index: 2.90 },
        { name: "Moderna", composite_score: 10.0, risk_level: "faible", estimated_index: 1.0 },
      ],
      avg_composite: 61.05,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
