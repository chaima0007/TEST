import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[CAELUM] SWARM_API_URL not set — forced-eviction-land-rights-engine using mock data")
}

const MOCK = {
  engine: "forced_eviction_land_rights_engine",
  domain: "forced_eviction_land_rights",
  wave: 195,
  accent_color: "#0f766e",
  entities: [
    {
      id: "FEL_001",
      name: "Rio Tinto plc",
      country: "GB/AU",
      sector: "Mining",
      composite_score: 89.30,
      severity: "critique",
      estimated_forced_eviction_land_rights_index: 8.93,
      key_violation: "Destruction Juukan Gorge — sites sacrés Aborigènes Pilbara",
    },
    {
      id: "FEL_002",
      name: "Vedanta Resources",
      country: "GB/IN",
      sector: "Mining",
      composite_score: 86.00,
      severity: "critique",
      estimated_forced_eviction_land_rights_index: 8.60,
      key_violation: "Niyamgiri — déplacements tribaux Dongria Kondh Odisha",
    },
    {
      id: "FEL_003",
      name: "Glencore International",
      country: "CH",
      sector: "Mining & Commodities",
      composite_score: 80.70,
      severity: "critique",
      estimated_forced_eviction_land_rights_index: 8.07,
      key_violation: "RDC Kolwezi — expulsions communautés minières sans compensation",
    },
    {
      id: "FEL_004",
      name: "Bolloré SE",
      country: "FR",
      sector: "Agribusiness / Logistics",
      composite_score: 77.10,
      severity: "critique",
      estimated_forced_eviction_land_rights_index: 7.71,
      key_violation: "Plantations palmier Cameroun/Guinée — déplacements forcés villageois",
    },
    {
      id: "FEL_005",
      name: "Wilmar International",
      country: "SG",
      sector: "Palm Oil",
      composite_score: 57.15,
      severity: "élevé",
      estimated_forced_eviction_land_rights_index: 5.72,
      key_violation: "Huile palme Indonésie — déforestation & dépossession terres coutumières",
    },
    {
      id: "FEL_006",
      name: "TotalEnergies SE",
      country: "FR",
      sector: "Oil & Gas",
      composite_score: 52.40,
      severity: "élevé",
      estimated_forced_eviction_land_rights_index: 5.24,
      key_violation: "EACOP Ouganda/Tanzanie — 100k+ personnes déplacées pipeline",
    },
    {
      id: "FEL_007",
      name: "Rainforest Alliance",
      country: "US",
      sector: "Certification",
      composite_score: 27.85,
      severity: "modéré",
      estimated_forced_eviction_land_rights_index: 2.79,
      key_violation: "Standards FPIC imparfaits — lacunes consentement préalable",
    },
    {
      id: "FEL_008",
      name: "Landesa",
      country: "US",
      sector: "Land Rights NGO",
      composite_score: 12.65,
      severity: "faible",
      estimated_forced_eviction_land_rights_index: 1.27,
      key_violation: "Meilleure pratique — titres fonciers communautés rurales",
    },
  ],
  summary: {
    total_entities: 8,
    critique: 4,
    élevé: 2,
    modéré: 1,
    faible: 1,
    avg_composite: 60.39,
    distribution_valid: true,
  },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/forced-eviction-land-rights-engine`, {
      next: { revalidate: 30 },
    })
    if (!res.ok) throw new Error(`upstream ${res.status}`)
    const data = await res.json()
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)))
  } catch {
    return sealResponse(NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 }))
  }
}
