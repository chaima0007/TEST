import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[toxic-waste-environmental-racism-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "toxic_waste_environmental_racism",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "TWE-001", name: "Nigeria Delta Niger — Shell Legacy, Ogoniland Pollué & UNEP Report Nettoyage 25 Ans", composite_score: 92.80, risk_level: "critique", estimated_environmental_racism_index: 9.28 },
    { entity_id: "TWE-002", name: "Inde Bhopal — Union Carbide Impunité 40 Ans, 20K Morts & Sol Contaminé", composite_score: 89.20, risk_level: "critique", estimated_environmental_racism_index: 8.92 },
    { entity_id: "TWE-003", name: "Ghana Agbogbloshie — Décharge E-Waste Mondiale, Enfants Brûlent Câbles & Métaux Lourds", composite_score: 82.80, risk_level: "critique", estimated_environmental_racism_index: 8.28 },
    { entity_id: "TWE-004", name: "USA Cancer Alley Louisiane — 150 Usines Pétrochimiques, Afro-Américains & EPA Inaction", composite_score: 74.80, risk_level: "critique", estimated_environmental_racism_index: 7.48 },
    { entity_id: "TWE-005", name: "Chine Zones Pollution Industrielle — Villages Cancer, Déchets Métallurgie & Migration Forcée", composite_score: 56.80, risk_level: "élevé", estimated_environmental_racism_index: 5.68 },
    { entity_id: "TWE-006", name: "Bangladesh Tanneries Hazaribagh — Chrome Hexavalent, Travailleurs Malades & Relocalisation Lente", composite_score: 49.20, risk_level: "élevé", estimated_environmental_racism_index: 4.92 },
    { entity_id: "TWE-007", name: "France Outre-Mer Chlordécone — Pesticide Banane Interdit, Antilles Contaminées & Cancer Prostate", composite_score: 30.80, risk_level: "modéré", estimated_environmental_racism_index: 3.08 },
    { entity_id: "TWE-008", name: "Pays-Bas Droit Environnemental Avancé — Urgenda, Klimaatakkoord & PFAS Réglementation Stricte", composite_score: 8.65, risk_level: "faible", estimated_environmental_racism_index: 0.87 },
  ],
  avg_composite: 60.63,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/toxic-waste-environmental-racism-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
