import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Anti-Corruption Whistleblower Protection Engine Agent",
  domain: "anti_corruption_whistleblower_protection",
  total_entities: 8,
  avg_composite: 61.35,
  confidence_score: 0.89,
  avg_estimated_anti_corruption_whistleblower_protection_index: 6.14,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "transparency_international_corruption_perceptions_2023",
    "eu_whistleblower_directive_2019_1937_implementation",
    "human_rights_watch_journalist_killings_2023",
    "un_convention_against_corruption_uncac_review_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[anti-corruption-whistleblower-protection-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/anti-corruption-whistleblower-protection-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
