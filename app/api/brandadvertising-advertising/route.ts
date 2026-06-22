import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[brandadvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/brandadvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "brandadvertising-advertising",
      entities: [
        { name: "Nike Global Brand Campaigns", composite_score: 91.40, risk_level: "critique", estimated_index: 9.14 },
        { name: "Coca-Cola Brand Storytelling", composite_score: 84.75, risk_level: "critique", estimated_index: 8.48 },
        { name: "Apple Brand Identity Ads", composite_score: 77.60, risk_level: "critique", estimated_index: 7.76 },
        { name: "Samsung Brand Awareness", composite_score: 65.90, risk_level: "critique", estimated_index: 6.59 },
        { name: "Unilever Purpose-Led Branding", composite_score: 52.30, risk_level: "élevé", estimated_index: 5.23 },
        { name: "L'Oréal Brand Equity", composite_score: 43.80, risk_level: "élevé", estimated_index: 4.38 },
        { name: "LVMH Luxury Brand Management", composite_score: 29.50, risk_level: "modéré", estimated_index: 2.95 },
        { name: "Zara Fast Fashion Branding", composite_score: 12.70, risk_level: "faible", estimated_index: 1.27 },
      ],
      avg_composite: 57.24,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
