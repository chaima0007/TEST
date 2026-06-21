import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[disability-rights-social-exclusion-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "disability-rights-social-exclusion-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "DRS-001",
      name: "Inde/Institutions Psychiatriques — 700 000 Internés Forcés, Loi Mental Healthcare Act Non-Appliquée, Conditions Inhumaines",
      composite_score: 83.05,
      risk_level: "critique",
      estimated_disability_rights_index: 8.31,
    },
    {
      id: "DRS-002",
      name: "Éthiopie/Lépreux Exclus — Colonies Ségrégées Addis Abeba, Stigmatisation Extrême, Accès Soins Zéro, Mendicité Forcée",
      composite_score: 79.85,
      risk_level: "critique",
      estimated_disability_rights_index: 7.99,
    },
    {
      id: "DRS-003",
      name: "Yémen/Handicapés Conflit — 4M Nouveaux Handicapés Guerre, Infrastructures Détruites, Réhabilitation Inexistante",
      composite_score: 77.95,
      risk_level: "critique",
      estimated_disability_rights_index: 7.80,
    },
    {
      id: "DRS-004",
      name: "Maroc/Enfants Handicapés — 95% Exclus Système Scolaire Ordinaire, Centres Spécialisés Insuffisants, CRPD Ratifié 2009",
      composite_score: 67.1,
      risk_level: "critique",
      estimated_disability_rights_index: 6.71,
    },
    {
      id: "DRS-005",
      name: "Turquie/Discrimination Emploi — Quota 3% Non-Appliqué, Licenciements Personnes Handicapées Post-Coup 2016, Accessibilité Défaillante",
      composite_score: 52.8,
      risk_level: "élevé",
      estimated_disability_rights_index: 5.28,
    },
    {
      id: "DRS-006",
      name: "Mexique/Accessibilité Urbaine — Modèle Médical Dominant, 7M Personnes Handicapées Sous Seuil Pauvreté, Réformes Partielles",
      composite_score: 45.75,
      risk_level: "élevé",
      estimated_disability_rights_index: 4.58,
    },
    {
      id: "DRS-007",
      name: "Allemagne/Autonomie CRPD — Désinstitutionnalisation Progressive, Werkstätten Critiqués ONU, Vie Indépendante Art. 19 CRPD",
      composite_score: 25.55,
      risk_level: "modéré",
      estimated_disability_rights_index: 2.56,
    },
    {
      id: "DRS-008",
      name: "Canada/AODA Ontario Modèle — Accessibilité 2025 Presque Atteinte, Stratégie Inclusive Fédérale, Standard International",
      composite_score: 10.65,
      risk_level: "faible",
      estimated_disability_rights_index: 1.07,
    },
  ],
  avg_composite: 55.34,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/disability-rights-social-exclusion-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
