import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[private-military-contractors-accountability-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "private-military-contractors-accountability-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "PMC-001",
      name: "Wagner Group/Russie — Afrique Crimes Documentés ONU, Mali Moura 500 Civils, Impunité Totale",
      composite_score: 95.6,
      risk_level: "critique",
      estimated_pmc_accountability_index: 9.56,
    },
    {
      id: "PMC-002",
      name: "Blackwater/Nisour Square Irak — 17 Civils Tués 2007, Condamnations Annulées, Grâces Trump",
      composite_score: 90.3,
      risk_level: "critique",
      estimated_pmc_accountability_index: 9.03,
    },
    {
      id: "PMC-003",
      name: "DynCorp/Balkans — Trafic Humain Accusations Bosnia Kosovo, Non Poursuivies, Contrats Maintenus",
      composite_score: 84.65,
      risk_level: "critique",
      estimated_pmc_accountability_index: 8.46,
    },
    {
      id: "PMC-004",
      name: "Aegis/Irak — Vidéos Tirs Civils Non Sanctionnés, Enquête PMSC Inexistante, Contrats Reconduits",
      composite_score: 78.9,
      risk_level: "critique",
      estimated_pmc_accountability_index: 7.89,
    },
    {
      id: "PMC-005",
      name: "G4S/Prisons UK — Maltraitance Détenues Rapport 2017, Amendes Sans Poursuites Pénales",
      composite_score: 53.3,
      risk_level: "élevé",
      estimated_pmc_accountability_index: 5.33,
    },
    {
      id: "PMC-006",
      name: "MPRI/Balkans — Entraînement Armées, Responsabilité Floue, Opérations Tempête Croatie 1995",
      composite_score: 48.9,
      risk_level: "élevé",
      estimated_pmc_accountability_index: 4.89,
    },
    {
      id: "PMC-007",
      name: "Montreux Document/Suisse — Cadre Volontaire PMC, 57 États Adhérents, Normes Non Contraignantes",
      composite_score: 25.85,
      risk_level: "modéré",
      estimated_pmc_accountability_index: 2.58,
    },
    {
      id: "PMC-008",
      name: "ICoC/Code Conduite Contractants Privés — Mécanisme Plaintes 2013, Portée Limitée, Modèle",
      composite_score: 7.55,
      risk_level: "faible",
      estimated_pmc_accountability_index: 0.76,
    },
  ],
  avg_composite: 60.63,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/private-military-contractors-accountability-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
