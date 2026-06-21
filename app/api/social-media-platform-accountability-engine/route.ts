import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[social-media-platform-accountability-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "social_media_platform_accountability",
  generated_at: new Date().toISOString(),
  avg_composite: 58.32,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  entities: [
    {
      entity_id: "SMP-001",
      name: "Meta (Myanmar genocide enabler)",
      composite_score: 87.65,
      risk_level: "critique",
      estimated_platform_accountability_index: 8.77,
    },
    {
      entity_id: "SMP-002",
      name: "TikTok (propagande État + enfants)",
      composite_score: 82.10,
      risk_level: "critique",
      estimated_platform_accountability_index: 8.21,
    },
    {
      entity_id: "SMP-003",
      name: "Telegram (terrorisme + trafic humain)",
      composite_score: 77.85,
      risk_level: "critique",
      estimated_platform_accountability_index: 7.79,
    },
    {
      entity_id: "SMP-004",
      name: "X/Twitter (post-Musk modération effondrée)",
      composite_score: 73.60,
      risk_level: "critique",
      estimated_platform_accountability_index: 7.36,
    },
    {
      entity_id: "SMP-005",
      name: "YouTube (radicalisation algorithme)",
      composite_score: 56.90,
      risk_level: "élevé",
      estimated_platform_accountability_index: 5.69,
    },
    {
      entity_id: "SMP-006",
      name: "WhatsApp (Inde mob lynchings)",
      composite_score: 48.65,
      risk_level: "élevé",
      estimated_platform_accountability_index: 4.87,
    },
    {
      entity_id: "SMP-007",
      name: "Facebook EU (DSA compliance partielle)",
      composite_score: 30.85,
      risk_level: "modéré",
      estimated_platform_accountability_index: 3.09,
    },
    {
      entity_id: "SMP-008",
      name: "Signal (chiffrement + privacy)",
      composite_score: 8.95,
      risk_level: "faible",
      estimated_platform_accountability_index: 0.90,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/social-media-platform-accountability-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
