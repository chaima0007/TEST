import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[semanticadvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/semanticadvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "semanticadvertising-advertising",
      entities: [
        { name: "DoubleVerify Semantic Engine", composite_score: 93.40, risk_level: "critique", estimated_semanticadvertising_index: 9.34 },
        { name: "Integral Ad Science Context", composite_score: 86.70, risk_level: "critique", estimated_semanticadvertising_index: 8.67 },
        { name: "Oracle Contextual Intelligence", composite_score: 78.90, risk_level: "critique", estimated_semanticadvertising_index: 7.89 },
        { name: "GumGum Verity Contextual", composite_score: 71.20, risk_level: "critique", estimated_semanticadvertising_index: 7.12 },
        { name: "Peer39 Semantic Targeting", composite_score: 54.80, risk_level: "élevé", estimated_semanticadvertising_index: 5.48 },
        { name: "Grapeshot Keyword Safety", composite_score: 43.50, risk_level: "élevé", estimated_semanticadvertising_index: 4.35 },
        { name: "Zeta Global Semantic", composite_score: 26.10, risk_level: "modéré", estimated_semanticadvertising_index: 2.61 },
        { name: "Admixer Contextual Ads", composite_score: 12.40, risk_level: "faible", estimated_semanticadvertising_index: 1.24 },
      ],
      avg_composite: 58.38,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
