import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[CAELUM] SWARM_API_URL not set — child-agricultural-labor-engine using mock data")
}

const MOCK = {
  engine: "child_agricultural_labor_engine",
  domain: "child_agricultural_labor",
  wave: 195,
  accent_color: "#ea580c",
  entities: [
    {
      id: "CAL_001",
      name: "Nestlé SA",
      country: "CH/CI",
      sector: "Food & Beverage",
      composite_score: 86.90,
      severity: "critique",
      estimated_child_agricultural_labor_index: 8.69,
      key_violation: "Cacao Côte d'Ivoire — 1.56M enfants dans chaîne cacao",
    },
    {
      id: "CAL_002",
      name: "Cargill Incorporated",
      country: "US/Global",
      sector: "Agriculture",
      composite_score: 84.85,
      severity: "critique",
      estimated_child_agricultural_labor_index: 8.49,
      key_violation: "Tabac & canne à sucre — travail saisonnier enfants",
    },
    {
      id: "CAL_003",
      name: "Barry Callebaut AG",
      country: "CH/CI",
      sector: "Chocolate",
      composite_score: 82.85,
      severity: "critique",
      estimated_child_agricultural_labor_index: 8.29,
      key_violation: "Chaîne cacao — audit gaps reconnus",
    },
    {
      id: "CAL_004",
      name: "JDE Peet's NV",
      country: "NL/KE/ET",
      sector: "Coffee",
      composite_score: 80.85,
      severity: "critique",
      estimated_child_agricultural_labor_index: 8.09,
      key_violation: "Café Kenya/Éthiopie — travail enfants fermes caféières",
    },
    {
      id: "CAL_005",
      name: "Thai Union Group PCL",
      country: "TH",
      sector: "Seafood",
      composite_score: 56.50,
      severity: "élevé",
      estimated_child_agricultural_labor_index: 5.65,
      key_violation: "Industrie pêche — travail forcé enfants migrants",
    },
    {
      id: "CAL_006",
      name: "Sucromiles SA Colombia",
      country: "CO",
      sector: "Sugar",
      composite_score: 52.50,
      severity: "élevé",
      estimated_child_agricultural_labor_index: 5.25,
      key_violation: "Canne à sucre Colombie — travail saisonnier",
    },
    {
      id: "CAL_007",
      name: "Rainforest Alliance",
      country: "US",
      sector: "Certification",
      composite_score: 30.55,
      severity: "modéré",
      estimated_child_agricultural_labor_index: 3.06,
      key_violation: "Certification partielle — gaps monitoring",
    },
    {
      id: "CAL_008",
      name: "Fairtrade Foundation",
      country: "UK",
      sector: "Certification",
      composite_score: 14.60,
      severity: "faible",
      estimated_child_agricultural_labor_index: 1.46,
      key_violation: "Meilleure pratique — standards stricts",
    },
  ],
  summary: {
    total_entities: 8,
    critique: 4,
    élevé: 2,
    modéré: 1,
    faible: 1,
    avg_composite: 61.20,
    distribution_valid: true,
  },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-agricultural-labor-engine`, {
      next: { revalidate: 30 },
    })
    if (!res.ok) throw new Error(`upstream ${res.status}`)
    const data = await res.json()
    return NextResponse.json(await sealResponse(data.payload ?? data))
  } catch {
    return NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 })
  }
}
