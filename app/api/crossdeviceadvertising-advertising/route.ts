import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[crossdeviceadvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/crossdeviceadvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "crossdeviceadvertising-advertising",
      entities: [
        { name: "LiveRamp Identity Graph", composite_score: 94.10, risk_level: "critique", estimated_crossdeviceadvertising_index: 9.41 },
        { name: "Tapad Device Graph", composite_score: 87.30, risk_level: "critique", estimated_crossdeviceadvertising_index: 8.73 },
        { name: "Nielsen Digital Ad Ratings", composite_score: 79.50, risk_level: "critique", estimated_crossdeviceadvertising_index: 7.95 },
        { name: "Oracle Data Cloud CrossDevice", composite_score: 72.80, risk_level: "critique", estimated_crossdeviceadvertising_index: 7.28 },
        { name: "Neustar Identity Resolution", composite_score: 55.60, risk_level: "élevé", estimated_crossdeviceadvertising_index: 5.56 },
        { name: "Verizon Media ConnectID", composite_score: 44.20, risk_level: "élevé", estimated_crossdeviceadvertising_index: 4.42 },
        { name: "Drawbridge Cross-Device", composite_score: 25.40, risk_level: "modéré", estimated_crossdeviceadvertising_index: 2.54 },
        { name: "AdBrain Device Mapping", composite_score: 11.30, risk_level: "faible", estimated_crossdeviceadvertising_index: 1.13 },
      ],
      avg_composite: 61.28,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
