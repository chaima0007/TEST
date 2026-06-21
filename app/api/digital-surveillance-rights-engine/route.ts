import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[CAELUM] SWARM_API_URL not set — digital-surveillance-rights-engine using mock data")
}

const MOCK = {
  engine: "digital_surveillance_rights_engine",
  domain: "digital_surveillance_rights",
  wave: 195,
  accent_color: "#6d28d9",
  entities: [
    {
      id: "DSR_001",
      name: "NSO Group Technologies",
      country: "IL",
      sector: "Spyware",
      composite_score: 89.55,
      severity: "critique",
      estimated_digital_surveillance_rights_index: 8.96,
      key_violation: "Pegasus — ciblage journalistes, défenseurs droits humains, chefs d'État",
    },
    {
      id: "DSR_002",
      name: "Hikvision",
      country: "CN",
      sector: "Surveillance Hardware",
      composite_score: 86.40,
      severity: "critique",
      estimated_digital_surveillance_rights_index: 8.64,
      key_violation: "Caméras IA Xinjiang — surveillance biométrique de masse Ouïghours",
    },
    {
      id: "DSR_003",
      name: "Palantir Technologies",
      country: "US",
      sector: "Data Analytics",
      composite_score: 78.05,
      severity: "critique",
      estimated_digital_surveillance_rights_index: 7.81,
      key_violation: "Contrats ICE/CBP — profilage racial & surveillance immigration",
    },
    {
      id: "DSR_004",
      name: "Clearview AI",
      country: "US",
      sector: "Facial Recognition",
      composite_score: 75.40,
      severity: "critique",
      estimated_digital_surveillance_rights_index: 7.54,
      key_violation: "Base 30Mrd visages scrapés sans consentement — RGPD violations",
    },
    {
      id: "DSR_005",
      name: "Meta Platforms Inc",
      country: "US",
      sector: "Social Media",
      composite_score: 58.80,
      severity: "élevé",
      estimated_digital_surveillance_rights_index: 5.88,
      key_violation: "Cambridge Analytica legacy — profilage comportemental publicitaire",
    },
    {
      id: "DSR_006",
      name: "ByteDance/TikTok",
      country: "CN/US",
      sector: "Social Media",
      composite_score: 56.15,
      severity: "élevé",
      estimated_digital_surveillance_rights_index: 5.62,
      key_violation: "Accès données utilisateurs US par ingénieurs Chine — CFIUS review",
    },
    {
      id: "DSR_007",
      name: "Signal Foundation",
      country: "US",
      sector: "Privacy Tech",
      composite_score: 26.80,
      severity: "modéré",
      estimated_digital_surveillance_rights_index: 2.68,
      key_violation: "Adoption limitée — vulnérabilités métadonnées réseaux",
    },
    {
      id: "DSR_008",
      name: "Tor Project",
      country: "US",
      sector: "Privacy Tech",
      composite_score: 11.15,
      severity: "faible",
      estimated_digital_surveillance_rights_index: 1.12,
      key_violation: "Meilleure pratique anonymat — infrastructure décentralisée",
    },
  ],
  summary: {
    total_entities: 8,
    critique: 4,
    élevé: 2,
    modéré: 1,
    faible: 1,
    avg_composite: 60.29,
    distribution_valid: true,
  },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-surveillance-rights-engine`, {
      next: { revalidate: 30 },
    })
    if (!res.ok) throw new Error(`upstream ${res.status}`)
    const data = await res.json()
    return NextResponse.json(await sealResponse(data.payload ?? data))
  } catch {
    return NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 })
  }
}
