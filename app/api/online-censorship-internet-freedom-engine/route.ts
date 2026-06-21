import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[online-censorship-internet-freedom-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "online-censorship-internet-freedom-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "OCF-001",
      name: "Chine/Grand Firewall — 1M+ Sites Bloqués, DPI Systématique, 1 000+ Emprisonnés Droits Numériques, Projet SAURON",
      composite_score: 95.0,
      risk_level: "critique",
      estimated_internet_freedom_index: 9.50,
    },
    {
      id: "OCF-002",
      name: "Corée Nord/Kwangmyong Intranet — Isolation Totale Internet Mondial, 28 Sites Autorisés, Peine Mort Accès Étranger",
      composite_score: 94.4,
      risk_level: "critique",
      estimated_internet_freedom_index: 9.44,
    },
    {
      id: "OCF-003",
      name: "Iran/Coupures Internet Manifestations — Mahsa Amini 2022 : 5 Jours Shutdown Total, 80M Coupés, 500 Morts Documentés",
      composite_score: 86.3,
      risk_level: "critique",
      estimated_internet_freedom_index: 8.63,
    },
    {
      id: "OCF-004",
      name: "Russie/SORM-3 Blocages 2022 — 300 000 Sites Bloqués Post-Invasion, Meta Interdit, Journalistes Emprisonnés",
      composite_score: 79.1,
      risk_level: "critique",
      estimated_internet_freedom_index: 7.91,
    },
    {
      id: "OCF-005",
      name: "Myanmar/Coup 2021 Meta Blocage — Shutdown 77 Jours Complets, 1 000+ Arrestations Posts Facebook, Génocide Rohingya Amplification",
      composite_score: 50.3,
      risk_level: "élevé",
      estimated_internet_freedom_index: 5.03,
    },
    {
      id: "OCF-006",
      name: "Éthiopie/Coupures Tigray 2020-2022 — 18 Mois Sans Internet Région, Atrocités Cachées, Rapport ONU Violations Documentées",
      composite_score: 44.5,
      risk_level: "élevé",
      estimated_internet_freedom_index: 4.45,
    },
    {
      id: "OCF-007",
      name: "Inde/Cachemire Shutdown Record Démocratie — 552 Jours Coupure 2019-2021, Art. 19 Constitution, Internet Essential Service Act",
      composite_score: 33.1,
      risk_level: "modéré",
      estimated_internet_freedom_index: 3.31,
    },
    {
      id: "OCF-008",
      name: "Islande/Freedom of Information Modèle — Score 96/100 Freedom House, Loi IMMI Protection Journalistes, Zero Shutdown Historique",
      composite_score: 4.0,
      risk_level: "faible",
      estimated_internet_freedom_index: 0.40,
    },
  ],
  avg_composite: 60.84,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/online-censorship-internet-freedom-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
