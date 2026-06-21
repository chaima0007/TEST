import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[peacekeeping-accountability-governance-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "peacekeeping_accountability_governance",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "PAG-001", name: "RCA MINUSCA — Abus sexuels massifs, soldats francais Sangaris, ONU inaction documentee", composite_score: 90.90, risk_level: "critique", estimated_peacekeeping_accountability_index: 9.09 },
    { entity_id: "PAG-002", name: "Haiti MINUSTAH — Cholera importe ONU 2010, 10K morts, deni puis accord partiel", composite_score: 85.40, risk_level: "critique", estimated_peacekeeping_accountability_index: 8.54 },
    { entity_id: "PAG-003", name: "RDC MONUSCO — Abus sexuels Kivu, peacekeepers vendant armes aux rebelles", composite_score: 81.30, risk_level: "critique", estimated_peacekeeping_accountability_index: 8.13 },
    { entity_id: "PAG-004", name: "Mali MINUSMA — Accusations violations droits, retrait brusque 2023, impunite totale", composite_score: 71.30, risk_level: "critique", estimated_peacekeeping_accountability_index: 7.13 },
    { entity_id: "PAG-005", name: "Bosnie SFOR — Trafic humain peacekeeper annees 1990, lente reconnaissance ONU", composite_score: 51.60, risk_level: "élevé", estimated_peacekeeping_accountability_index: 5.16 },
    { entity_id: "PAG-006", name: "Soudan du Sud UNMISS — Abus sporadiques, mecanismes de plainte partiels", composite_score: 43.30, risk_level: "élevé", estimated_peacekeeping_accountability_index: 4.33 },
    { entity_id: "PAG-007", name: "Liban FINUL — Tensions moderees, quelques incidents signales, cooperation partielle", composite_score: 23.30, risk_level: "modéré", estimated_peacekeeping_accountability_index: 2.33 },
    { entity_id: "PAG-008", name: "Canada/Norvege modele — Standards conduite peacekeeper, formation DDHH obligatoire", composite_score: 4.65, risk_level: "faible", estimated_peacekeeping_accountability_index: 0.47 },
  ],
  avg_composite: 56.47,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/peacekeeping-accountability-governance-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
