import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[space-colonization-indigenous-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "space_colonization_indigenous_rights_engine",
  domain: "space_colonization_indigenous_rights",
  total_entities: 8,
  avg_composite: 59.97,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    resource_extraction_colonialism: 3,
    military_space_dominance: 2,
    indigenous_heritage_erasure: 2,
    governance_vacuum: 1,
  },
  top_risk_entities: [
    { id: "SCI-001", name: "États-Unis — NASA/SpaceX, Extraction Lune-Mars Sans Consentement Peuples Autochtones", score: 91.75, risk: "critique" },
    { id: "SCI-002", name: "Chine — Programme Lunaire Chang'e, Hégémonie Orbitale Revendiquée", score: 90.7, risk: "critique" },
    { id: "SCI-004", name: "Russie — Roscosmos Militarisation Orbitale, Veto Traité Espace", score: 82.35, risk: "critique" },
  ],
  critical_alerts: [
    "SCI-001: États-Unis — NASA/SpaceX, Extraction Lune-Mars Sans Consentement Peuples Autochtones — composite 91.75",
    "SCI-002: Chine — Programme Lunaire Chang'e, Hégémonie Orbitale Revendiquée — composite 90.7",
    "SCI-003: Hawaï — Mauna Kea, Télescopes Géants sur Sites Sacrés Autochtones — composite 76.9",
    "SCI-004: Russie — Roscosmos Militarisation Orbitale, Veto Traité Espace — composite 82.35",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_space_colonization_indigenous_rights_index: 6.0,
  data_sources: [
    "un_committee_peaceful_uses_outer_space_2024",
    "indigenous_space_rights_initiative_2023",
    "dark_skies_astronomy_indigenous_report_2024",
    "space_policy_institute_colonialism_analysis_2025",
  ],
  entities: [
    {
      id: "SCI-001",
      name: "États-Unis — NASA/SpaceX, Extraction Lune-Mars Sans Consentement Peuples Autochtones",
      country: "États-Unis",
      space_resource_extraction_colonialism_score: 93.0,
      indigenous_celestial_heritage_erasure_score: 90.0,
      military_space_dominance_score: 95.0,
      international_governance_accountability_score: 88.0,
      composite_score: 91.75,
      risk_level: "critique",
      primary_pattern: "US Space Act 2015 légalisant extraction ressources spatiales, Artemis Program sans consultation peuples autochtones, militarisation orbitale via USSF",
      estimated_space_colonization_indigenous_rights_index: 9.18,
      last_updated: "2026-06-21",
    },
    {
      id: "SCI-002",
      name: "Chine — Programme Lunaire Chang'e, Hégémonie Orbitale Revendiquée",
      country: "Chine",
      space_resource_extraction_colonialism_score: 91.0,
      indigenous_celestial_heritage_erasure_score: 87.0,
      military_space_dominance_score: 93.0,
      international_governance_accountability_score: 92.0,
      composite_score: 90.7,
      risk_level: "critique",
      primary_pattern: "Chang'e 6 extraction ressources Lune face cachée, CNSA rejet traité Artemis Accords, PLA satellites anti-satellitaires ASAT",
      estimated_space_colonization_indigenous_rights_index: 9.07,
      last_updated: "2026-06-21",
    },
    {
      id: "SCI-003",
      name: "Hawaï — Mauna Kea, Télescopes Géants sur Sites Sacrés Autochtones",
      country: "États-Unis (Hawaï)",
      space_resource_extraction_colonialism_score: 78.0,
      indigenous_celestial_heritage_erasure_score: 96.0,
      military_space_dominance_score: 62.0,
      international_governance_accountability_score: 70.0,
      composite_score: 76.9,
      risk_level: "critique",
      primary_pattern: "TMT Thirty Meter Telescope sur sommet sacré Mauna Kea, résistance kānaka maoli ignorée, héritage cosmologique autochtone effacé par infrastructure",
      estimated_space_colonization_indigenous_rights_index: 7.69,
      last_updated: "2026-06-21",
    },
    {
      id: "SCI-004",
      name: "Russie — Roscosmos Militarisation Orbitale, Veto Traité Espace",
      country: "Russie",
      space_resource_extraction_colonialism_score: 80.0,
      indigenous_celestial_heritage_erasure_score: 72.0,
      military_space_dominance_score: 91.0,
      international_governance_accountability_score: 88.0,
      composite_score: 82.35,
      risk_level: "critique",
      primary_pattern: "Armes anti-satellite testées 2021 (débris ISS), veto résolutions ONU espace pacifique, Roscosmos extraction lune projetée sans cadre international",
      estimated_space_colonization_indigenous_rights_index: 8.24,
      last_updated: "2026-06-21",
    },
    {
      id: "SCI-005",
      name: "SpaceX/Starlink — Mégaconstellations, Pollution Lumineuse Sites Sacrés",
      country: "Multinationale",
      space_resource_extraction_colonialism_score: 58.0,
      indigenous_celestial_heritage_erasure_score: 65.0,
      military_space_dominance_score: 55.0,
      international_governance_accountability_score: 60.0,
      composite_score: 59.4,
      risk_level: "élevé",
      primary_pattern: "6000+ satellites Starlink effaçant ciel nocturne observatoires autochtones, absence consultation communautés astronomiques traditionnelles",
      estimated_space_colonization_indigenous_rights_index: 5.94,
      last_updated: "2026-06-21",
    },
    {
      id: "SCI-006",
      name: "UAE — Programme Spatial Mars, Extraction Sans Gouvernance",
      country: "Émirats Arabes Unis",
      space_resource_extraction_colonialism_score: 52.0,
      indigenous_celestial_heritage_erasure_score: 45.0,
      military_space_dominance_score: 48.0,
      international_governance_accountability_score: 55.0,
      composite_score: 49.85,
      risk_level: "élevé",
      primary_pattern: "Hope Mars Mission sans participation cadre gouvernance internationale, plans extraction asteroïdes sans traité contraignant",
      estimated_space_colonization_indigenous_rights_index: 4.99,
      last_updated: "2026-06-21",
    },
    {
      id: "SCI-007",
      name: "ESA — Partenariat Partiel Artemis, Tentatives Gouvernance Responsable",
      country: "Union Européenne",
      space_resource_extraction_colonialism_score: 28.0,
      indigenous_celestial_heritage_erasure_score: 22.0,
      military_space_dominance_score: 25.0,
      international_governance_accountability_score: 20.0,
      composite_score: 24.15,
      risk_level: "modéré",
      primary_pattern: "ESA signataire Artemis Accords mais promotion gouvernance multilatérale, initiatives dialogue peuples autochtones astronomie",
      estimated_space_colonization_indigenous_rights_index: 2.42,
      last_updated: "2026-06-21",
    },
    {
      id: "SCI-008",
      name: "Nouvelle-Zélande — Législation Maori Espace, Modèle Droits Autochtones",
      country: "Nouvelle-Zélande",
      space_resource_extraction_colonialism_score: 6.0,
      indigenous_celestial_heritage_erasure_score: 5.0,
      military_space_dominance_score: 4.0,
      international_governance_accountability_score: 3.0,
      composite_score: 4.65,
      risk_level: "faible",
      primary_pattern: "Rocket Lab consultations iwi Maori, législation spatiale incluant whakapapa céleste, référence internationale pour droits autochtones cosmologiques",
      estimated_space_colonization_indigenous_rights_index: 0.47,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/space-colonization-indigenous-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data.payload ?? data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }));
  }
}
