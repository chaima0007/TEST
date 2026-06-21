import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[sexual-violence-conflict-weapon-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "sexual-violence-conflict-weapon",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "SVC-001",
      name: "RDC/Capitale Mondiale Viol ONU — 400K Cas/An, Kivu Ituri Zones Actives, Viols Systématiques Arme Guerre & Impunité Totale Miliciens",
      composite_score: 93.3,
      risk_level: "critique",
      estimated_conflict_sexual_violence_index: 9.33,
    },
    {
      id: "SVC-002",
      name: "Soudan/Darfour RSF 2023 — Viols de Masse RSF Khartoum, 10K Cas Rapportés, Violence Sexuelle Tactique Déplacement & Absence Poursuites",
      composite_score: 89.0,
      risk_level: "critique",
      estimated_conflict_sexual_violence_index: 8.9,
    },
    {
      id: "SVC-003",
      name: "Syrie/Assad IS — Forces Assad et Daech, Viols Comme Tactique Déplacement Forcé, Détentions Arbitraires & Esclavage Sexuel Yézidies",
      composite_score: 85.7,
      risk_level: "critique",
      estimated_conflict_sexual_violence_index: 8.57,
    },
    {
      id: "SVC-004",
      name: "Myanmar/Rohingya Tatmadaw — Viols Documentés ICJ ONU, Tactique Nettoyage Ethnique, Villages Brûlés & Responsabilité Commandement Absente",
      composite_score: 79.7,
      risk_level: "critique",
      estimated_conflict_sexual_violence_index: 7.97,
    },
    {
      id: "SVC-005",
      name: "Yémen/Houthis Coalition — Viols en Détention Documentés, Rapports OHCHR, Violence Sexuelle Prisonniers & Impunité Acteurs Non-Étatiques",
      composite_score: 55.2,
      risk_level: "élevé",
      estimated_conflict_sexual_violence_index: 5.52,
    },
    {
      id: "SVC-006",
      name: "Ukraine/Viols Russes 2022 — Documentés OHCHR depuis Invasion, Rapport ICC Mandats Arrêt, Violence Sexuelle Occupations & Poursuites Engagées",
      composite_score: 48.7,
      risk_level: "élevé",
      estimated_conflict_sexual_violence_index: 4.87,
    },
    {
      id: "SVC-007",
      name: "Colombie/Legacy Conflit FARC-ELN — JEP Reconnaissance Partielle, Programmes Réparation Victimes, Persistance Violence & Progrès Judiciaires Lents",
      composite_score: 27.2,
      risk_level: "modéré",
      estimated_conflict_sexual_violence_index: 2.72,
    },
    {
      id: "SVC-008",
      name: "Rwanda/Post-Génocide Gacaca — Tribunaux Communautaires Opérationnels, Réintégration Sociale, Mémorial National & Modèle Justice Transitionnelle",
      composite_score: 7.4,
      risk_level: "faible",
      estimated_conflict_sexual_violence_index: 0.74,
    },
  ],
  avg_composite: 60.77,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sexual-violence-conflict-weapon-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
