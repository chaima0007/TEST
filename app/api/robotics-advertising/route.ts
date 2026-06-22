import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[robotics-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/robotics_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Boston Dynamics Ad Hub", composite_score: 95.20, risk_level: "critique", estimated_index: 9.52 },
        { name: "ABB Robotics Campaign", composite_score: 89.45, risk_level: "critique", estimated_index: 8.95 },
        { name: "FANUC Brand Intelligence", composite_score: 81.45, risk_level: "critique", estimated_index: 8.15 },
        { name: "KUKA Digital Outreach", composite_score: 76.45, risk_level: "critique", estimated_index: 7.65 },
        { name: "Yaskawa Media Engine", composite_score: 57.45, risk_level: "élevé", estimated_index: 5.75 },
        { name: "Universal Robots Comms", composite_score: 47.45, risk_level: "élevé", estimated_index: 4.75 },
        { name: "Rethink Robotics Reach", composite_score: 28.45, risk_level: "modéré", estimated_index: 2.85 },
        { name: "Kawasaki Ad Mesh", composite_score: 10.20, risk_level: "faible", estimated_index: 1.02 },
      ],
      avg_composite: 61.02,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
