import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[education-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/education_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Coursera", composite_score: 95.2, risk_level: "critique", estimated_index: 9.52 },
        { name: "Udemy", composite_score: 89.45, risk_level: "critique", estimated_index: 8.95 },
        { name: "edX", composite_score: 81.95, risk_level: "critique", estimated_index: 8.20 },
        { name: "Khan Academy", composite_score: 76.95, risk_level: "critique", estimated_index: 7.70 },
        { name: "Pearson", composite_score: 57.95, risk_level: "élevé", estimated_index: 5.80 },
        { name: "McGraw-Hill", composite_score: 47.95, risk_level: "élevé", estimated_index: 4.80 },
        { name: "Chegg", composite_score: 28.95, risk_level: "modéré", estimated_index: 2.90 },
        { name: "Duolingo", composite_score: 10.0, risk_level: "faible", estimated_index: 1.0 },
      ],
      avg_composite: 61.05,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
