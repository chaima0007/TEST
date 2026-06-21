import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[housing-forced-evictions-gentrification-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "housing-forced-evictions-gentrification-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "HFE-001",
      name: "Inde/Mumbai Dharavi Démolitions — 1 Million Habitants Bidonville, Redéveloppement Adani, Relogement Insuffisant, PIDESC Art. 11",
      composite_score: 83.8,
      risk_level: "critique",
      estimated_housing_rights_index: 8.38,
    },
    {
      id: "HFE-002",
      name: "Kenya/Nairobi Mathare Expulsions — 500 000 Résidents, Bulldozers Sans Préavis, Défenseurs Logement Assassinés, ONU Alerte",
      composite_score: 80.85,
      risk_level: "critique",
      estimated_housing_rights_index: 8.09,
    },
    {
      id: "HFE-003",
      name: "Brésil/Rio Favelas JO 2016 — 77 000 Expulsés Pré-Olympique, Comunidade Vila Autódromo, Impunité Totale Post-Jeux",
      composite_score: 76.5,
      risk_level: "critique",
      estimated_housing_rights_index: 7.65,
    },
    {
      id: "HFE-004",
      name: "Philippines/Manille Duterte Slum Clearance — 100 000 Déplacés Balik-Probinsya, Sans Consultation, Pauvreté Urbaine Persistante",
      composite_score: 73.25,
      risk_level: "critique",
      estimated_housing_rights_index: 7.33,
    },
    {
      id: "HFE-005",
      name: "Chine/Hutong Pékin Rénovation Urbaine — 1 Million Déplacés Périphérie, Droit Pétition Réprimé, Pas De Recours Judiciaire",
      composite_score: 54.2,
      risk_level: "élevé",
      estimated_housing_rights_index: 5.42,
    },
    {
      id: "HFE-006",
      name: "USA/Los Angeles Sans-Abri Sweeps — 70 000 Encampments Démantelés/An, Biens Confisqués, Martin v. City of Boise Contourné",
      composite_score: 48.3,
      risk_level: "élevé",
      estimated_housing_rights_index: 4.83,
    },
    {
      id: "HFE-007",
      name: "Espagne/Madrid Gentrification — Quartiers Lavapiés-Malasaña, Airbnb +300%, Loyers +80%, Loi Logement 2023 Partielle",
      composite_score: 34.6,
      risk_level: "modéré",
      estimated_housing_rights_index: 3.46,
    },
    {
      id: "HFE-008",
      name: "Pays-Bas/Amsterdam Housing First Modèle — Sans-Abri -70%, Encadrement Loyers, Priorité Logement Social, Référence EU",
      composite_score: 8.35,
      risk_level: "faible",
      estimated_housing_rights_index: 0.84,
    },
  ],
  avg_composite: 57.48,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/housing-forced-evictions-gentrification-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
