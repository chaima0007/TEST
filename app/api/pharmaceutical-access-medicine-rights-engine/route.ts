import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[pharmaceutical-access-medicine-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "pharmaceutical-access-medicine-rights-engine",
  generated_at: new Date().toISOString(),
  avg_composite: 56.96,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    {
      id: "PAM-001",
      name: "Afrique Sub-Saharienne/ARV 25M VIH — Accès Antirétroviraux 73% Médicaments Brevets Pfizer Prohibitifs MSF Dénonce",
      composite_score: 89.4,
      risk_level: "critique",
      estimated_medicine_access_rights_index: 8.94,
    },
    {
      id: "PAM-002",
      name: "USA/Insuline 300$/Mois — Brevets Eli Lilly Novo Nordisk Morts Rationnement Prix 10x Europe 37M Diabétiques",
      composite_score: 84.2,
      risk_level: "critique",
      estimated_medicine_access_rights_index: 8.42,
    },
    {
      id: "PAM-003",
      name: "Yémen/MSF Accès Bloqué — Blocus Médicaments Essentiels 21M Personnes Besoin Choléra Malnutrition Sévère",
      composite_score: 79.6,
      risk_level: "critique",
      estimated_medicine_access_rights_index: 7.96,
    },
    {
      id: "PAM-004",
      name: "Venezuela/Pénurie 85% Médicaments — Sanctions Bloquent Importations Cancer VIH Diabète Non Traités Exodus",
      composite_score: 71.1,
      risk_level: "critique",
      estimated_medicine_access_rights_index: 7.11,
    },
    {
      id: "PAM-005",
      name: "Inde/Génériques Pharmaco — Licences Obligatoires TRIPS Sorafenib 2012 Résistance Brevets Pharma Multinationale",
      composite_score: 53.8,
      risk_level: "élevé",
      estimated_medicine_access_rights_index: 5.38,
    },
    {
      id: "PAM-006",
      name: "Brésil/Licence Obligatoire Efavirenz — Décret 2007 ARV Merck Generic Bayer Kaletra Modèle Mondial TRIPS",
      composite_score: 46.9,
      risk_level: "élevé",
      estimated_medicine_access_rights_index: 4.69,
    },
    {
      id: "PAM-007",
      name: "OMS/Flexibilités TRIPS Accord Doha — Déclaration 2001 Santé Publique Priorité Accès Médicaments PVD Négoce",
      composite_score: 24.7,
      risk_level: "modéré",
      estimated_medicine_access_rights_index: 2.47,
    },
    {
      id: "PAM-008",
      name: "Bangladesh/Modèle PMA — Exemption TRIPS 2033 Génériques Locaux Production Nationale ARV Vaccins Accès",
      composite_score: 6.0,
      risk_level: "faible",
      estimated_medicine_access_rights_index: 0.60,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/pharmaceutical-access-medicine-rights-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
