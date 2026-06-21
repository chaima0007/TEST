import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[autonomous-weapons-killer-robots-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "autonomous-weapons-killer-robots-engine",
  generated_at: new Date().toISOString(),
  avg_composite: 60.08,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    {
      id: "AWR-001",
      name: "Russie/Kalashnikov KUB-BLA Drone Kamikaze — IA Autonome Déployée Ukraine Décision Létale Sans Humain Interdit",
      composite_score: 94.1,
      risk_level: "critique",
      estimated_autonomous_weapons_risk_index: 9.41,
    },
    {
      id: "AWR-002",
      name: "Chine/STR Sharp Sword UAS Nucléaire — Programme LAWS Classifié 2035 Objectif IA Défense Mondiale Opacité Totale",
      composite_score: 91.5,
      risk_level: "critique",
      estimated_autonomous_weapons_risk_index: 9.15,
    },
    {
      id: "AWR-003",
      name: "Turquie/Kargu-2 UCAV Autonome — Premier Usage Documenté ONU Libye 2020 Sans Opérateur IA Ciblage",
      composite_score: 85.2,
      risk_level: "critique",
      estimated_autonomous_weapons_risk_index: 8.52,
    },
    {
      id: "AWR-004",
      name: "Israël/Harop Loitering Munition — Drone Autonome Anti-Radiation Ciblage Automatique Vendu 15+ Pays",
      composite_score: 78.6,
      risk_level: "critique",
      estimated_autonomous_weapons_risk_index: 7.86,
    },
    {
      id: "AWR-005",
      name: "USA/LAWS Programme DoD — Budget 18Mds USD 2024 Projet Replicator 1000 Drones Autonomes IA Battlefield",
      composite_score: 55.3,
      risk_level: "élevé",
      estimated_autonomous_weapons_risk_index: 5.53,
    },
    {
      id: "AWR-006",
      name: "Corée du Sud/SGR-A1 Robot Sentinelle — Zone Démilitarisée Détection Automatique Humaine Politique Engagement",
      composite_score: 49.7,
      risk_level: "élevé",
      estimated_autonomous_weapons_risk_index: 4.97,
    },
    {
      id: "AWR-007",
      name: "UE/Campagne Stop Killer Robots — 26 ONG Coalition Interdiction Traité Multilatéral Négociation CCW Genève",
      composite_score: 22.1,
      risk_level: "modéré",
      estimated_autonomous_weapons_risk_index: 2.21,
    },
    {
      id: "AWR-008",
      name: "ONU/GGE Négociations CCW — Consensus Fragile Principes Non-Contraignants Russie-Chine Bloquent Traité",
      composite_score: 4.1,
      risk_level: "faible",
      estimated_autonomous_weapons_risk_index: 0.41,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/autonomous-weapons-killer-robots-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
