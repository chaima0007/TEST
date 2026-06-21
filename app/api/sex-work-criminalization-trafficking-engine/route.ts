import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[sex-work-criminalization-trafficking-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "sex-work-criminalization-trafficking-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "SWT-001",
      name: "République Dominicaine/Tourisme Sexuel Enfants — ONUDC 100 000 Victimes Mineures Resorts Complicité Impunité Systémique",
      composite_score: 89.3,
      risk_level: "critique",
      estimated_sex_work_rights_index: 8.93,
    },
    {
      id: "SWT-002",
      name: "Nigeria/Benin City Traite EU — 40 000 Femmes Edo Trafiquées Europe/An Madams Juju Serment Dette Bondage",
      composite_score: 86.6,
      risk_level: "critique",
      estimated_sex_work_rights_index: 8.66,
    },
    {
      id: "SWT-003",
      name: "Thaïlande/Pattaya Traite Déguisée — 250 000 Travailleuses Sexuelles Industrie 6.4Mds USD Proxénétisme Crime Organisé",
      composite_score: 76.2,
      risk_level: "critique",
      estimated_sex_work_rights_index: 7.62,
    },
    {
      id: "SWT-004",
      name: "Inde/Sonagachi 100 000 Travailleurs Sexuels Stigmatisés — Durbar Mahila Samanwaya Résistance SIDA Criminalisation",
      composite_score: 68.4,
      risk_level: "critique",
      estimated_sex_work_rights_index: 6.84,
    },
    {
      id: "SWT-005",
      name: "Corée du Sud/Criminalisation 2004 Stigmate — Special Law Anti-Prostitution 140 000 Travailleuses Marginalisées Violence",
      composite_score: 47.7,
      risk_level: "élevé",
      estimated_sex_work_rights_index: 4.77,
    },
    {
      id: "SWT-006",
      name: "Pays-Bas/Légalisation Zones Contrôlées — Fenêtres Amsterdam Traite Résiduelle Projet 1012 Fermeture 40% Fenêtres",
      composite_score: 45.4,
      risk_level: "élevé",
      estimated_sex_work_rights_index: 4.54,
    },
    {
      id: "SWT-007",
      name: "Suède/Modèle Nordic Client Criminalisé — Sex Purchase Act 1999 Réduction Demande 50% Modèle Exporté EU",
      composite_score: 25.3,
      risk_level: "modéré",
      estimated_sex_work_rights_index: 2.53,
    },
    {
      id: "SWT-008",
      name: "Nouvelle-Zélande/Prostitution Reform Act 2003 Modèle — Décriminalisation Droits Travailleurs Santé Accès Justice",
      composite_score: 5.0,
      risk_level: "faible",
      estimated_sex_work_rights_index: 0.50,
    },
  ],
  avg_composite: 55.49,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sex-work-criminalization-trafficking-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
