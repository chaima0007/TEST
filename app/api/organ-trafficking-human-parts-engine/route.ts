import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[organ-trafficking-human-parts-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "organ-trafficking-human-parts-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "OTH-001",
      name: "Chine/Prisonniers Conscience Falun Gong — China Tribunal 2019 : Prélèvements Forcés Systémiques, Ouïghours, Crimes Contre l'Humanité",
      composite_score: 92.35,
      risk_level: "critique",
      estimated_organ_trafficking_index: 9.24,
    },
    {
      id: "OTH-002",
      name: "Pakistan/Rein Commercial Karachi — 2 500 Reins Vendus/An, Trafiquants Intermédiaires, Donors Ruraux Endettés Exploités",
      composite_score: 82.65,
      risk_level: "critique",
      estimated_organ_trafficking_index: 8.27,
    },
    {
      id: "OTH-003",
      name: "Égypte/Trafic Organes Post-Révolution — Vulnérabilité Économique 2011-2015, Réseaux Alexandrie-Sinai, Réfugiés Syriens Ciblés",
      composite_score: 75.3,
      risk_level: "critique",
      estimated_organ_trafficking_index: 7.53,
    },
    {
      id: "OTH-004",
      name: "Kosovo/Organes Guerre 1999 Dossier Marty — Rapport Conseil Europe 2010, Maison Jaune Albanie, UCK Crimes Non-Jugés",
      composite_score: 72.9,
      risk_level: "critique",
      estimated_organ_trafficking_index: 7.29,
    },
    {
      id: "OTH-005",
      name: "Inde/Rein Pauvreté Chennai — Appukuttanpatti Village Rein, 10 000 Ventes Estimées, Exploitation Caste Dalit Femmes",
      composite_score: 58.9,
      risk_level: "élevé",
      estimated_organ_trafficking_index: 5.89,
    },
    {
      id: "OTH-006",
      name: "Israël/Intermédiaires Organes — Courtiers Transplant Tourism, Loi 2008 Adoption Tardive, Cas Moldavie-Turquie-Ukraine Documentés",
      composite_score: 44.0,
      risk_level: "élevé",
      estimated_organ_trafficking_index: 4.40,
    },
    {
      id: "OTH-007",
      name: "Philippines/Transplant Tourism Manille — Loi 2009, Réduction 60%, Résidus Commerce Rein Mindanao, Monitoring OMS",
      composite_score: 27.4,
      risk_level: "modéré",
      estimated_organ_trafficking_index: 2.74,
    },
    {
      id: "OTH-008",
      name: "Espagne/Modèle Don CNT — Opt-Out Consentement Présumé, 50+ Dons/Ppm Population, Trafic Quasi-Éliminé, Standard ONDT",
      composite_score: 5.1,
      risk_level: "faible",
      estimated_organ_trafficking_index: 0.51,
    },
  ],
  avg_composite: 57.33,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/organ-trafficking-human-parts-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
