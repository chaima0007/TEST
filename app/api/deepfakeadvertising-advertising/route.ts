import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[deepfakeadvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/deepfakeadvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "deepfakeadvertising-advertising",
      entities: [
        { name: "Synthesia AI Video Ads", composite_score: 96.70, risk_level: "critique", estimated_deepfakeadvertising_index: 9.67 },
        { name: "D-ID Celebrity Deepfakes", composite_score: 89.20, risk_level: "critique", estimated_deepfakeadvertising_index: 8.92 },
        { name: "HeyGen Avatar Campaigns", composite_score: 81.40, risk_level: "critique", estimated_deepfakeadvertising_index: 8.14 },
        { name: "Runway Gen-3 Ad Creative", composite_score: 73.60, risk_level: "critique", estimated_deepfakeadvertising_index: 7.36 },
        { name: "ElevenLabs Voice Cloning Ads", composite_score: 56.80, risk_level: "élevé", estimated_deepfakeadvertising_index: 5.68 },
        { name: "Pika Labs Video Synthesis", composite_score: 46.30, risk_level: "élevé", estimated_deepfakeadvertising_index: 4.63 },
        { name: "Kling AI Commercial Content", composite_score: 29.10, risk_level: "modéré", estimated_deepfakeadvertising_index: 2.91 },
        { name: "Adobe Firefly Synthetic Ads", composite_score: 15.70, risk_level: "faible", estimated_deepfakeadvertising_index: 1.57 },
      ],
      avg_composite: 61.10,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
