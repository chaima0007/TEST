import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[extraordinary-rendition-secret-detention-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "extraordinary-rendition-secret-detention-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "ERD-001",
      name: "USA/CIA Programme Post-9/11 — 136 Détenus, 54 Pays Complices, Rapport Senate 2014, Waterboarding Documenté",
      composite_score: 85.15,
      risk_level: "critique",
      estimated_rendition_rights_index: 8.52,
    },
    {
      id: "ERD-002",
      name: "Égypte/Extraordinary Rendition Hub — Destination Principale Transferts CIA, Mohamed Al-Zery, Torture Officielle",
      composite_score: 81.95,
      risk_level: "critique",
      estimated_rendition_rights_index: 8.20,
    },
    {
      id: "ERD-003",
      name: "Syrie/Assad Torture Centres — CIA Renditions vers Assad, Maher Arar, Détention al-Mazzeh, Impunité Totale",
      composite_score: 79.75,
      risk_level: "critique",
      estimated_rendition_rights_index: 7.98,
    },
    {
      id: "ERD-004",
      name: "Pakistan/ISI Collaboration — Capture HVTs Post-9/11, Disparitions Forcées Baloutchistan, Complice Renditions",
      composite_score: 72.75,
      risk_level: "critique",
      estimated_rendition_rights_index: 7.28,
    },
    {
      id: "ERD-005",
      name: "Pologne-Roumanie-Lituanie/Sites Noirs CIA Europe — Arrêts CEDH, Abu Zubaydah vs Pologne, Compensations",
      composite_score: 55.05,
      risk_level: "élevé",
      estimated_rendition_rights_index: 5.51,
    },
    {
      id: "ERD-006",
      name: "Maroc/DGED Coopération — Témara Prison Noire, Coalition CIA-MI6, Impunité Persistante, Amnesty Rapports",
      composite_score: 48.15,
      risk_level: "élevé",
      estimated_rendition_rights_index: 4.82,
    },
    {
      id: "ERD-007",
      name: "Royaume-Uni/Complicité Partielle — Rapport ISC 2018, Belhaj v UK, Dédommagements Partiels, Réformes MI6",
      composite_score: 30.05,
      risk_level: "modéré",
      estimated_rendition_rights_index: 3.01,
    },
    {
      id: "ERD-008",
      name: "Allemagne/Recours Khaled El-Masri — Condamnation CEDH CIA, Réformes Parlementaires Renseignement, BND",
      composite_score: 9.85,
      risk_level: "faible",
      estimated_rendition_rights_index: 0.99,
    },
  ],
  avg_composite: 57.84,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/extraordinary-rendition-secret-detention-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
