import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-surveillance-mass-monitoring-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "digital-surveillance-mass-monitoring",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "DSM-001",
      name: "Chine/SCS Reconnaissance Faciale — 600M Caméras, Système Crédit Social, Surveillance Totale Xinjiang & Contrôle Biométrique Généralisé",
      composite_score: 95.65,
      risk_level: "critique",
      estimated_surveillance_rights_index: 9.56,
    },
    {
      id: "DSM-002",
      name: "Corée du Nord/Surveillance Totale — Absence Internet Civil, Écoutes Domestiques Systématiques, Contrôle Absolu Communications & Intranet Kwangmyong",
      composite_score: 93.2,
      risk_level: "critique",
      estimated_surveillance_rights_index: 9.32,
    },
    {
      id: "DSM-003",
      name: "Russie/SORM Espionnage — Interception Légale Totale Télécoms, Logiciels Pegasus-like Journalistes, SORM-3 Métadonnées & Loi Yarovaya",
      composite_score: 82.8,
      risk_level: "critique",
      estimated_surveillance_rights_index: 8.28,
    },
    {
      id: "DSM-004",
      name: "USA/NSA PRISM — Programme Snowden, FISA Court Secrète, Surveillance Globale Sans Mandat Étrangers & Section 702 Collecte Masse",
      composite_score: 69.9,
      risk_level: "critique",
      estimated_surveillance_rights_index: 6.99,
    },
    {
      id: "DSM-005",
      name: "Inde/Aadhar NATGRID — Biométrie 1.4Mrd Habitants, Fusion Bases Données Gouvernementales, Loi Surveillance Sans Garanties & Coupures Cachemire",
      composite_score: 53.6,
      risk_level: "élevé",
      estimated_surveillance_rights_index: 5.36,
    },
    {
      id: "DSM-006",
      name: "Brésil/SINAE Surveillance — Monitoring Mouvements Sociaux, Journalistes Ciblés, Absence Cadre Légal Clair & Données Biométriques Police",
      composite_score: 45.2,
      risk_level: "élevé",
      estimated_surveillance_rights_index: 4.52,
    },
    {
      id: "DSM-007",
      name: "UE/RGPD Protection Partielle — Cadre Légal Avancé Mais Surveillance Sécurité Nationale Possible, Accords MLAT & Lacunes Renseignement",
      composite_score: 21.9,
      risk_level: "modéré",
      estimated_surveillance_rights_index: 2.19,
    },
    {
      id: "DSM-008",
      name: "Allemagne/BfDI Protection Forte — Commissaire Données Indépendant, Recours Effectif Citoyens, Contrôle Parlementaire BND & Arrêts Constitutionnels",
      composite_score: 5.95,
      risk_level: "faible",
      estimated_surveillance_rights_index: 0.60,
    },
  ],
  avg_composite: 58.52,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-surveillance-mass-monitoring-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
