import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[critical-minerals-transition-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "critical-minerals-transition-rights-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "CMR-001",
      name: "RDC/Cobalt Artisanal — 40 000 Enfants Katanga-Lualaba, 70% Cobalt Mondial, Chaîne EV-Batteries, Amnesty 2016",
      composite_score: 90.35,
      risk_level: "critique",
      estimated_critical_minerals_rights_index: 9.04,
    },
    {
      id: "CMR-002",
      name: "Bolivie/Lithium Indigènes — Salar Uyuni, Communautés Aymara Déplacées, Absence FPIC, Nationalisation Controversée",
      composite_score: 75.15,
      risk_level: "critique",
      estimated_critical_minerals_rights_index: 7.52,
    },
    {
      id: "CMR-003",
      name: "Chine/Terres Rares Mongolie Intérieure — Pollution Radioactive Baotou, Villages Toxiques, Déplacements Forcés",
      composite_score: 78.35,
      risk_level: "critique",
      estimated_critical_minerals_rights_index: 7.84,
    },
    {
      id: "CMR-004",
      name: "Myanmar/Jade-Terres Rares-Étain — Financement Junta Post-Coup, Travail Forcé, Absence Contrats, Kachin Conflict",
      composite_score: 73.15,
      risk_level: "critique",
      estimated_critical_minerals_rights_index: 7.32,
    },
    {
      id: "CMR-005",
      name: "Chili/Lithium Triangle Atacama — Eau Atacameñes, Stress Hydrique Désert, Consultation Insuffisante, SQM-Albemarle",
      composite_score: 52.05,
      risk_level: "élevé",
      estimated_critical_minerals_rights_index: 5.21,
    },
    {
      id: "CMR-006",
      name: "Philippines/Nickel Palawan-Mindanao — Indigènes Sans EIA, Pollution Rivières, Mines Illégales, DENR Défaillant",
      composite_score: 47.25,
      risk_level: "élevé",
      estimated_critical_minerals_rights_index: 4.73,
    },
    {
      id: "CMR-007",
      name: "Argentine/Lithium Jujuy — Tensions Communautaires Tilcara, FPIC Partiel, Progrès Réglementaires CONICET",
      composite_score: 27.05,
      risk_level: "modéré",
      estimated_critical_minerals_rights_index: 2.71,
    },
    {
      id: "CMR-008",
      name: "Finlande/Nickel-Cobalt Terrafame — Standards EU Battery Regulation, Due Diligence, ILO Compliance, Audit Tiers",
      composite_score: 7.80,
      risk_level: "faible",
      estimated_critical_minerals_rights_index: 0.78,
    },
  ],
  avg_composite: 56.39,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/critical-minerals-transition-rights-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
