import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[corporate-impunity-accountability-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "corporate-impunity-accountability-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "CIA-001",
      name: "Nestlé/Cacao Côte d&apos;Ivoire — Travail Enfants Documenté, 72% Plantations Non-Conformes, Absence Traçabilité",
      composite_score: 77.25,
      risk_level: "critique",
      estimated_corporate_impunity_index: 7.72,
    },
    {
      id: "CIA-002",
      name: "Apple/Foxconn Chine — Suicides Usines Shenzhen, Conditions Travail Extrêmes, Uyghurs Xinjiang Supply Chain",
      composite_score: 76.35,
      risk_level: "critique",
      estimated_corporate_impunity_index: 7.63,
    },
    {
      id: "CIA-003",
      name: "TotalEnergies Myanmar — Financement Junta Militaire Post-Coup, Pipeline Yadana, Complicité Crimes Contre Humanité",
      composite_score: 82.40,
      risk_level: "critique",
      estimated_corporate_impunity_index: 8.24,
    },
    {
      id: "CIA-004",
      name: "Glencore RDC — Cobalt Mines Artisanales, Travail Enfants, Pollution Environnementale, Impunité Totale",
      composite_score: 79.30,
      risk_level: "critique",
      estimated_corporate_impunity_index: 7.93,
    },
    {
      id: "CIA-005",
      name: "H&amp;M Bangladesh/Cambodge — Salaires Misère Post-Rana Plaza, Répression Syndicats, Audits Superficiels",
      composite_score: 53.75,
      risk_level: "élevé",
      estimated_corporate_impunity_index: 5.38,
    },
    {
      id: "CIA-006",
      name: "Amazon Logistique EU — Conditions Travail Entrepôts, Répression Syndicale Systématique, Surveillance Workers",
      composite_score: 50.25,
      risk_level: "élevé",
      estimated_corporate_impunity_index: 5.02,
    },
    {
      id: "CIA-007",
      name: "Patagonia Supply Chain — Progrès Audits Tiers, Transparence Partielle, Efforts Traçabilité En Cours",
      composite_score: 28.65,
      risk_level: "modéré",
      estimated_corporate_impunity_index: 2.86,
    },
    {
      id: "CIA-008",
      name: "Danone — Politique Droits Humains Certifiée B-Corp, Reporting CSDDD Avancé, Mécanismes Recours Actifs",
      composite_score: 12.90,
      risk_level: "faible",
      estimated_corporate_impunity_index: 1.29,
    },
  ],
  avg_composite: 57.61,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/corporate-impunity-accountability-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
