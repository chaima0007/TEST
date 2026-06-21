import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[mega-infrastructure-construction-labor-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "mega-infrastructure-construction-labor-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "MIL-001",
      name: "Arabie Saoudite/NEOM — 500Mrd$ Méga-Projet, 20 000 Howeitat Expulsés, Tirs sur Résistants, Zéro Syndicats",
      composite_score: 92.35,
      risk_level: "critique",
      estimated_megaproject_labor_index: 9.24,
    },
    {
      id: "MIL-002",
      name: "Qatar/FIFA 2022 Chantiers — 6 500 Décès Estimés Guardian, Système Kafala, Chaleur Mortelle, Impunité FIFA",
      composite_score: 89.15,
      risk_level: "critique",
      estimated_megaproject_labor_index: 8.92,
    },
    {
      id: "MIL-003",
      name: "Émirats/Dubai Construction — 3,5M Migrants, Passeports Confisqués, Dette Recrutement, Camps Insalubres Kafala",
      composite_score: 85.15,
      risk_level: "critique",
      estimated_megaproject_labor_index: 8.52,
    },
    {
      id: "MIL-004",
      name: "Laos/Barrage Nam Theun — Déplacement 6 000 Nakai, Pollution Mékong, Garanties BM Non-Tenues",
      composite_score: 71.95,
      risk_level: "critique",
      estimated_megaproject_labor_index: 7.20,
    },
    {
      id: "MIL-005",
      name: "Chine/BRI Éthiopie-Pakistan — Travailleurs Locaux Sous-Payés, Accidents Piraeus, Dettes Souveraines États",
      composite_score: 53.05,
      risk_level: "élevé",
      estimated_megaproject_labor_index: 5.31,
    },
    {
      id: "MIL-006",
      name: "Inde/Smart Cities — Déplacements Bidonvilles Mumbai-Delhi, Travailleurs Sans Contrat, Violences Chantiers",
      composite_score: 45.25,
      risk_level: "élevé",
      estimated_megaproject_labor_index: 4.53,
    },
    {
      id: "MIL-007",
      name: "Brésil/Itaipu Legacy — 25 000 Déplacés Compensés, Monitoring IACHR, Réformes Partielles, Fond Communautaire",
      composite_score: 27.05,
      risk_level: "modéré",
      estimated_megaproject_labor_index: 2.71,
    },
    {
      id: "MIL-008",
      name: "Danemark/Pont Øresund — Standards ILO Respectés, Syndicats Inclus, Ratio Accidents <0,1%, Modèle Nordique",
      composite_score: 5.80,
      risk_level: "faible",
      estimated_megaproject_labor_index: 0.58,
    },
  ],
  avg_composite: 58.72,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/mega-infrastructure-construction-labor-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
