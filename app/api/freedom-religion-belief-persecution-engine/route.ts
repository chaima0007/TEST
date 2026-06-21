import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[freedom-religion-belief-persecution-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "freedom-religion-belief-persecution-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "RBP-001",
      name: "Chine/Falun Gong &amp; Ouïghours — Camps Rééducation Xinjiang, Prélèvement Organes Prisonniers, Temples Détruits",
      composite_score: 89.40,
      risk_level: "critique",
      estimated_religious_persecution_index: 8.94,
    },
    {
      id: "RBP-002",
      name: "Myanmar/Rohingya — Épuration Ethnique-Religieuse Bouddhiste-Musulmane, Génocide ONU Reconnu, Villages Brûlés",
      composite_score: 88.20,
      risk_level: "critique",
      estimated_religious_persecution_index: 8.82,
    },
    {
      id: "RBP-003",
      name: "Pakistan/Loi Blasphème — Ahmadis Chrétiens Hindous Ciblés, Lynchages Populaires, Condamnations à Mort Fréquentes",
      composite_score: 86.90,
      risk_level: "critique",
      estimated_religious_persecution_index: 8.69,
    },
    {
      id: "RBP-004",
      name: "Arabie Saoudite — Apostasie Peine de Mort, Zéro Liberté Culte Non-Musulman, Conversions Criminalisées",
      composite_score: 87.60,
      risk_level: "critique",
      estimated_religious_persecution_index: 8.76,
    },
    {
      id: "RBP-005",
      name: "Inde/Minorités — Lynchages Anti-Musulmans Impunis, Loi CAA Discriminatoire, Montée BJP Nationalisme Hindou",
      composite_score: 54.75,
      risk_level: "élevé",
      estimated_religious_persecution_index: 5.47,
    },
    {
      id: "RBP-006",
      name: "Nigeria/Boko Haram — Persécution Chrétiens Nord, Enlèvements Filles Chibok, Conflit Interreligieux Plateau State",
      composite_score: 52.40,
      risk_level: "élevé",
      estimated_religious_persecution_index: 5.24,
    },
    {
      id: "RBP-007",
      name: "France — Laïcité Controversée, Voile Scolaire Interdit, Discrimination Perçue Musulmans, Abaya Interdite 2023",
      composite_score: 23.25,
      risk_level: "modéré",
      estimated_religious_persecution_index: 2.33,
    },
    {
      id: "RBP-008",
      name: "Canada — Charte Droits Libertés Religieuses, Multiculturalisme Officiel, Protection Légale Minorités Robuste",
      composite_score: 5.10,
      risk_level: "faible",
      estimated_religious_persecution_index: 0.51,
    },
  ],
  avg_composite: 60.95,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/freedom-religion-belief-persecution-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
