import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[music-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/music_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Universal Music", composite_score: 96, risk_level: "critique", estimated_index: 9.6 },
        { name: "Sony Music", composite_score: 88, risk_level: "critique", estimated_index: 8.8 },
        { name: "Warner Music", composite_score: 82, risk_level: "critique", estimated_index: 8.2 },
        { name: "Live Nation", composite_score: 75, risk_level: "critique", estimated_index: 7.5 },
        { name: "Ticketmaster", composite_score: 61, risk_level: "élevé", estimated_index: 6.1 },
        { name: "Spotify", composite_score: 50, risk_level: "élevé", estimated_index: 5.0 },
        { name: "Apple Music", composite_score: 32, risk_level: "modéré", estimated_index: 3.2 },
        { name: "Amazon Music", composite_score: 16, risk_level: "faible", estimated_index: 1.6 },
      ],
      avg_composite: 62.50,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
