import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[weatherbasedadvertising-advertising] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/weatherbasedadvertising_advertising`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      domain: "weatherbasedadvertising-advertising",
      entities: [
        { name: "The Weather Company Ads", composite_score: 92.80, risk_level: "critique", estimated_weatherbasedadvertising_index: 9.28 },
        { name: "AccuWeather Targeted Ads", composite_score: 84.50, risk_level: "critique", estimated_weatherbasedadvertising_index: 8.45 },
        { name: "Tomorrow.io Weather Ads", composite_score: 76.30, risk_level: "critique", estimated_weatherbasedadvertising_index: 7.63 },
        { name: "DTN Weather Marketing", composite_score: 67.80, risk_level: "critique", estimated_weatherbasedadvertising_index: 6.78 },
        { name: "ClimaCell Location Ads", composite_score: 54.10, risk_level: "élevé", estimated_weatherbasedadvertising_index: 5.41 },
        { name: "Pelmorex Weather Ads", composite_score: 43.60, risk_level: "élevé", estimated_weatherbasedadvertising_index: 4.36 },
        { name: "Foreca Conditional Ads", composite_score: 26.90, risk_level: "modéré", estimated_weatherbasedadvertising_index: 2.69 },
        { name: "Weather Underground Ads", composite_score: 11.70, risk_level: "faible", estimated_weatherbasedadvertising_index: 1.17 },
      ],
      avg_composite: 57.21,
      distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
