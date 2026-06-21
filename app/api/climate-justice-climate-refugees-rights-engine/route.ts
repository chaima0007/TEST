import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-justice-climate-refugees-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "climate-justice-climate-refugees-rights-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "CJR-001", name: "Bangladesh/Cyclones Déplacement — 13M Déplacés Climatiques 2050 Delta Submergé Chars Flottants Adaption", composite_score: 93.30, risk_level: "critique", estimated_climate_justice_index: 9.33 },
    { id: "CJR-002", name: "Tuvalu/Disparition Totale — Nation Insulaire 11 000 Habitants Submersion 2050 Accord NZ Migration Dignité", composite_score: 89.30, risk_level: "critique", estimated_climate_justice_index: 8.93 },
    { id: "CJR-003", name: "Pakistan/Inondations 2022 — 33M Affectés 1/3 Pays Sous Eau Pertes $30Mds Compensation Nulle Pollueurs", composite_score: 81.30, risk_level: "critique", estimated_climate_justice_index: 8.13 },
    { id: "CJR-004", name: "Somalie/Sécheresse Conflit — 7.8M Insécurité Alimentaire Déplacement Triple Nexus Conflit-Climat-Faim", composite_score: 75.30, risk_level: "critique", estimated_climate_justice_index: 7.53 },
    { id: "CJR-005", name: "Philippines/Yolanda Typhon — 6 300 Morts 4M Déplacés Reconstruction Inégale Droit Reconstruction Refusé", composite_score: 57.90, risk_level: "élevé", estimated_climate_justice_index: 5.79 },
    { id: "CJR-006", name: "Mozambique/Idai Cyclone — 3M Affectés 2019 Reconstruction Lente Justice Climatique Procès Énergéticiens", composite_score: 49.90, risk_level: "élevé", estimated_climate_justice_index: 4.99 },
    { id: "CJR-007", name: "USA/Puerto Rico Maria — $90Mds Dégâts Réponse Fédérale Discriminatoire Lenteur Reconstruction", composite_score: 33.50, risk_level: "modéré", estimated_climate_justice_index: 3.35 },
    { id: "CJR-008", name: "Allemagne/Klimaseniorinnen — Cour Européenne DH Obligation Climatique États Modèle Litiges Stratégiques", composite_score: 13.90, risk_level: "faible", estimated_climate_justice_index: 1.39 },
  ],
  avg_composite: 61.80,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate-justice-climate-refugees-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
