import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[ecommerce-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/ecommerce_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Amazon", composite_score: 95.20, risk_level: "critique", estimated_index: 9.52 },
        { name: "Alibaba", composite_score: 89.45, risk_level: "critique", estimated_index: 8.95 },
        { name: "eBay", composite_score: 81.95, risk_level: "critique", estimated_index: 8.20 },
        { name: "Shopify", composite_score: 76.95, risk_level: "critique", estimated_index: 7.70 },
        { name: "Etsy", composite_score: 57.95, risk_level: "élevé", estimated_index: 5.80 },
        { name: "Rakuten", composite_score: 47.95, risk_level: "élevé", estimated_index: 4.80 },
        { name: "Zalando", composite_score: 28.95, risk_level: "modéré", estimated_index: 2.90 },
        { name: "ASOS", composite_score: 10.00, risk_level: "faible", estimated_index: 1.00 },
      ],
      avg_composite: 61.02,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
