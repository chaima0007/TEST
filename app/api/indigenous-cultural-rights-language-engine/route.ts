import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[indigenous-cultural-rights-language-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "indigenous-cultural-rights-language-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "ICR-001", name: "Australie (Stolen Generations legacy)", composite_score: 82.40, level: "critique", estimated_cultural_rights_index: 8.24 },
    { entity_id: "ICR-002", name: "Canada (pensionnats legacy)", composite_score: 77.80, level: "critique", estimated_cultural_rights_index: 7.78 },
    { entity_id: "ICR-003", name: "USA (langues amérindiennes mourantes)", composite_score: 74.60, level: "critique", estimated_cultural_rights_index: 7.46 },
    { entity_id: "ICR-004", name: "Brésil (Amazonie — 270 langues menacées)", composite_score: 69.85, level: "critique", estimated_cultural_rights_index: 6.99 },
    { entity_id: "ICR-005", name: "Mexique (52 langues autochtones)", composite_score: 53.70, level: "élevé", estimated_cultural_rights_index: 5.37 },
    { entity_id: "ICR-006", name: "Guatemala (Maya — discrimination)", composite_score: 45.90, level: "élevé", estimated_cultural_rights_index: 4.59 },
    { entity_id: "ICR-007", name: "Nouvelle-Zélande (revitalisation Māori)", composite_score: 26.75, level: "modéré", estimated_cultural_rights_index: 2.68 },
    { entity_id: "ICR-008", name: "Bolivie (plurinationalité constitutionnelle)", composite_score: 13.45, level: "faible", estimated_cultural_rights_index: 1.35 },
  ],
  avg_composite: 55.56,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/indigenous-cultural-rights-language-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
