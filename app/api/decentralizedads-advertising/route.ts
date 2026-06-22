import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[decentralizedads-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/decentralizedads_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "decentralizedads-advertising",
      entities: [
        { name: "Mirror Protocol Ads", composite_score: 94.50, risk_level: "critique", estimated_decentralizedads_index: 9.45 },
        { name: "dApp Ad Consortium", composite_score: 87.80, risk_level: "critique", estimated_decentralizedads_index: 8.78 },
        { name: "Uniswap Community Ads", composite_score: 79.60, risk_level: "critique", estimated_decentralizedads_index: 7.96 },
        { name: "DAO Advertising Network", composite_score: 73.40, risk_level: "critique", estimated_decentralizedads_index: 7.34 },
        { name: "P2P Ad Exchange", composite_score: 55.20, risk_level: "élevé", estimated_decentralizedads_index: 5.52 },
        { name: "Lens Protocol Ads", composite_score: 49.10, risk_level: "élevé", estimated_decentralizedads_index: 4.91 },
        { name: "Farcaster Ad Layer", composite_score: 28.30, risk_level: "modéré", estimated_decentralizedads_index: 2.83 },
        { name: "IPFS Ad Indexer", composite_score: 10.90, risk_level: "faible", estimated_decentralizedads_index: 1.09 },
      ],
      avg_composite: 61.03,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
