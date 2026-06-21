import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[agribusiness-land-grab-community-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "agribusiness-land-grab-community-rights-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "ALG-001",
      name: "Indonésie / Palmier Kalimantan — 6M Ha Déforestation, Expulsion Dayaks, Feux 2019, Golden Agri-Resources NDPE Fictif",
      composite_score: 87.95,
      risk_level: "critique",
      estimated_land_grab_rights_index: 8.80,
    },
    {
      id: "ALG-002",
      name: "Cambodge / Sucre EBA — Union Européenne EBA Suspendu, 400 000 Ha Concessions, Expulsions Violentes Kampong Speu",
      composite_score: 83.95,
      risk_level: "critique",
      estimated_land_grab_rights_index: 8.40,
    },
    {
      id: "ALG-003",
      name: "Brésil / Soja Cerrado — 50M Ha Déforestation, Garimpeiros Terres Yanomami, Bolsonaro Héritage, Cargill-ADM",
      composite_score: 79.05,
      risk_level: "critique",
      estimated_land_grab_rights_index: 7.91,
    },
    {
      id: "ALG-004",
      name: "Sierra Leone / Sucre Addax — Land Matrix 57 700 Ha, Déplacement 13 Villages, Echec Projet, Abandonné 2015",
      composite_score: 71.95,
      risk_level: "critique",
      estimated_land_grab_rights_index: 7.20,
    },
    {
      id: "ALG-005",
      name: "Philippines / Ananas Dole-Del Monte — CARPER Contourné, Hacienda Luisita, Travailleurs Journaliers Sans Droits",
      composite_score: 52.9,
      risk_level: "élevé",
      estimated_land_grab_rights_index: 5.29,
    },
    {
      id: "ALG-006",
      name: "Pérou / Palmier Amazonie — AIDESEP Alertes, Shipibo-Konibo Expulsions, Certifications RSPO Insuffisantes",
      composite_score: 44.7,
      risk_level: "élevé",
      estimated_land_grab_rights_index: 4.47,
    },
    {
      id: "ALG-007",
      name: "Colombie / Post-Accord Terres — Restitution Terres UARIV, Assassinats Leaders, 8M Déplacés Internes, Progrès Relatifs",
      composite_score: 27.6,
      risk_level: "modéré",
      estimated_land_grab_rights_index: 2.76,
    },
    {
      id: "ALG-008",
      name: "Pays-Bas / Responsible Business Conduct — IMVO Loi 2025, Due Diligence Supply Chain, Modèle EU CSDDD",
      composite_score: 6.95,
      risk_level: "faible",
      estimated_land_grab_rights_index: 0.70,
    },
  ],
  avg_composite: 56.88,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/agribusiness-land-grab-community-rights-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
