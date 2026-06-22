import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[emotionadvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/emotionadvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "emotionadvertising-advertising",
      entities: [
        { name: "Affectiva Emotion AI Ads", composite_score: 96.50, risk_level: "critique", estimated_emotionadvertising_index: 9.65 },
        { name: "Realeyes Attention Ads", composite_score: 87.30, risk_level: "critique", estimated_emotionadvertising_index: 8.73 },
        { name: "iMotions Neuromarketing", composite_score: 79.80, risk_level: "critique", estimated_emotionadvertising_index: 7.98 },
        { name: "Noldus FaceReader Ads", composite_score: 71.20, risk_level: "critique", estimated_emotionadvertising_index: 7.12 },
        { name: "CrowdEmotion Analytics", composite_score: 55.40, risk_level: "élevé", estimated_emotionadvertising_index: 5.54 },
        { name: "Emotient Sentiment Ads", composite_score: 46.90, risk_level: "élevé", estimated_emotionadvertising_index: 4.69 },
        { name: "Sensum Biometric Ads", composite_score: 29.60, risk_level: "modéré", estimated_emotionadvertising_index: 2.96 },
        { name: "Nielsen NeuroFocus Ads", composite_score: 14.30, risk_level: "faible", estimated_emotionadvertising_index: 1.43 },
      ],
      avg_composite: 60.13,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
