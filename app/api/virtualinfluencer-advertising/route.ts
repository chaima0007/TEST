import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[virtualinfluencer-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/virtualinfluencer_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "virtualinfluencer-advertising",
      entities: [
        { name: "Lil Miquela (Brud)", composite_score: 95.40, risk_level: "critique", estimated_virtualinfluencer_index: 9.54 },
        { name: "Shudu (Cameron-James Wilson)", composite_score: 87.60, risk_level: "critique", estimated_virtualinfluencer_index: 8.76 },
        { name: "Imma (ModelingCafe)", composite_score: 79.80, risk_level: "critique", estimated_virtualinfluencer_index: 7.98 },
        { name: "Noonoouri (Joerg Zuber)", composite_score: 72.10, risk_level: "critique", estimated_virtualinfluencer_index: 7.21 },
        { name: "Lu do Magalu (Magazine Luiza)", composite_score: 55.30, risk_level: "élevé", estimated_virtualinfluencer_index: 5.53 },
        { name: "Bermuda (Thalasya)", composite_score: 43.70, risk_level: "élevé", estimated_virtualinfluencer_index: 4.37 },
        { name: "Blawko (Brud)", composite_score: 26.90, risk_level: "modéré", estimated_virtualinfluencer_index: 2.69 },
        { name: "Knox Frost (Oliver Dietrich)", composite_score: 12.80, risk_level: "faible", estimated_virtualinfluencer_index: 1.28 },
      ],
      avg_composite: 59.20,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
