import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Acid Attack Gender Violence Engine Agent",
  domain: "acid_attack_gender_violence",
  total_entities: 8,
  avg_composite: 54.32,
  confidence_score: 0.86,
  avg_estimated_acid_attack_gender_violence_index: 5.43,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["acid_survivors_trust_international_2023","un_women_gender_violence_2023","human_rights_watch_acid_attacks_2022","who_violence_women_2021"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[acid-attack-gender-violence-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/acid-attack-gender-violence-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
