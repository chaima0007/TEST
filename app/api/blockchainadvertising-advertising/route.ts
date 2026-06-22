import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[blockchainadvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/blockchainadvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "blockchainadvertising-advertising",
      entities: [
        { name: "Brave Attention Token", composite_score: 95.10, risk_level: "critique", estimated_blockchainadvertising_index: 9.51 },
        { name: "AdEx Network", composite_score: 88.30, risk_level: "critique", estimated_blockchainadvertising_index: 8.83 },
        { name: "Basic Attention Token", composite_score: 80.45, risk_level: "critique", estimated_blockchainadvertising_index: 8.05 },
        { name: "Ethereum Ad Protocol", composite_score: 74.20, risk_level: "critique", estimated_blockchainadvertising_index: 7.42 },
        { name: "Solana Ad Layer", composite_score: 56.80, risk_level: "élevé", estimated_blockchainadvertising_index: 5.68 },
        { name: "Polygon AdTech", composite_score: 48.60, risk_level: "élevé", estimated_blockchainadvertising_index: 4.86 },
        { name: "Chainlink Ad Oracle", composite_score: 27.40, risk_level: "modéré", estimated_blockchainadvertising_index: 2.74 },
        { name: "IPFS Ad Storage", composite_score: 11.20, risk_level: "faible", estimated_blockchainadvertising_index: 1.12 },
      ],
      avg_composite: 61.03,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
