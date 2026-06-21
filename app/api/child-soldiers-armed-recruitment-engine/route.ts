import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[child-soldiers-armed-recruitment-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "child-soldiers-armed-recruitment",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "CSR-001",
      name: "RDC/M23 FDLR — 30K+ Enfants Recrutés, Résolution ONU Ignorée, Groupes Armés Est-Congo & Recrutement Forcé Zones Rurales",
      composite_score: 88.9,
      risk_level: "critique",
      estimated_child_soldiers_index: 8.89,
    },
    {
      id: "CSR-002",
      name: "Soudan du Sud/RSF SPLA-IO — Child Recruitment Lists ONU 2024, Conflit Armé Permanent, Enfants Soldats Documentés & Impunité Commandants",
      composite_score: 83.85,
      risk_level: "critique",
      estimated_child_soldiers_index: 8.38,
    },
    {
      id: "CSR-003",
      name: "Myanmar/Tatmadaw — Usage Systématique Enfants Soldats, ACRP ONU, Recrutement Forces Armées Nationales & Groupes Ethniques Armés",
      composite_score: 82.8,
      risk_level: "critique",
      estimated_child_soldiers_index: 8.28,
    },
    {
      id: "CSR-004",
      name: "Somalie/Al-Shabaab — Recrutement Forcé Zones Rurales, Endoctrinement Madrasas, Enfants Combattants & Absence Autorité Étatique Zones Contrôlées",
      composite_score: 74.4,
      risk_level: "critique",
      estimated_child_soldiers_index: 7.44,
    },
    {
      id: "CSR-005",
      name: "Afghanistan/Taliban Post-2021 — Madrassa Pipelines Vers Combattants, Recrutement Idéologique, Enfants Utilisés Opérations & Fermeture Écoles Filles",
      composite_score: 54.3,
      risk_level: "élevé",
      estimated_child_soldiers_index: 5.43,
    },
    {
      id: "CSR-006",
      name: "CAR/Milices Locales — Enfants Combattants et Utilisés Logistique, Seleka Anti-Balaka Legacy, Groupes Armés Multiples & Contrôle Territorial Fragmenté",
      composite_score: 45.3,
      risk_level: "élevé",
      estimated_child_soldiers_index: 4.53,
    },
    {
      id: "CSR-007",
      name: "Nigeria/Boko Haram Legacy — Réintégration Partielle, Programmes UNICEF DDR, Enfants Associés Forces Armées & Stigmatisation Communautaire",
      composite_score: 25.3,
      risk_level: "modéré",
      estimated_child_soldiers_index: 2.53,
    },
    {
      id: "CSR-008",
      name: "Uruguay/Modèle Protection — Zéro Recrutement Enfants, Âge Légal Militaire 18+, OPAC Ratifié & Programmes Éducation Paix Certifiés ONU",
      composite_score: 3.8,
      risk_level: "faible",
      estimated_child_soldiers_index: 0.38,
    },
  ],
  avg_composite: 57.33,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-soldiers-armed-recruitment-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
