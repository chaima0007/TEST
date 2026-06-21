import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[stateless-persons-nationality-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "stateless-persons-nationality-rights-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "SNR-001",
      name: "Myanmar/Rohingya Apatrides — 600 000+ Privés Nationalité Loi 1982, Génocide ICJ, Camps Bangladesh Kutupalong, Aucun Retour",
      composite_score: 90.35,
      risk_level: "critique",
      estimated_statelessness_rights_index: 9.04,
    },
    {
      id: "SNR-002",
      name: "Kirghizstan/Communauté Dungan — 50 000 Apatrides Post-URSS, Pogrom 2020, Réfugiés Kazakhstan, Naturalisation Bloquée",
      composite_score: 77.15,
      risk_level: "critique",
      estimated_statelessness_rights_index: 7.72,
    },
    {
      id: "SNR-003",
      name: "Koweït/Bidoon — 100 000 Apatrides Exclus Fondation État, Décrets Discrimination, Apatridie Héréditaire 3 Générations",
      composite_score: 75.15,
      risk_level: "critique",
      estimated_statelessness_rights_index: 7.52,
    },
    {
      id: "SNR-004",
      name: "République Dominicaine/Haïtiens Déchus — Arrêt TC/0168/13, 200 000 Naturalisés Déchus, Condamnation IACHR, Apatridie de Masse",
      composite_score: 71.8,
      risk_level: "critique",
      estimated_statelessness_rights_index: 7.18,
    },
    {
      id: "SNR-005",
      name: "Thaïlande/Hill Tribes — 480 000 Apatrides Montagnards, Restrictions Mouvement, Accès Éducation-Santé Limité, Enregistrement Complexe",
      composite_score: 53.45,
      risk_level: "élevé",
      estimated_statelessness_rights_index: 5.35,
    },
    {
      id: "SNR-006",
      name: "Lettonie/Non-Citoyens Post-Soviétiques — 200 000 Aliens, Pas Droit Vote National, Statut Amélioré Mais Persistant, OSCE Monitoring",
      composite_score: 41.5,
      risk_level: "élevé",
      estimated_statelessness_rights_index: 4.15,
    },
    {
      id: "SNR-007",
      name: "Estonie/Apatrides Post-Soviétiques — 70 000 Nationalité Indéterminée, Passeport Apatride EU, Naturalisation Accessible, Progrès Relatifs",
      composite_score: 26.9,
      risk_level: "modéré",
      estimated_statelessness_rights_index: 2.69,
    },
    {
      id: "SNR-008",
      name: "Belgique/UNHCR Modèle — Convention 1954 Ratifiée, Procédure Détermination Apatridie, Plan Action UNHCR, Référence EU",
      composite_score: 7.1,
      risk_level: "faible",
      estimated_statelessness_rights_index: 0.71,
    },
  ],
  avg_composite: 55.42,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/stateless-persons-nationality-rights-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
