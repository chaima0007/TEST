import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[media-integrity-engine] SWARM_API_URL non défini — mode mock activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const entities = [
  {
    entity_id: "MED-001",
    name: "Russia Today Network",
    country: "Russie",
    sector: "Médias d'État",
    disinformation_spread_score: 88.0,
    source_credibility_gap_score: 85.0,
    editorial_independence_score: 82.0,
    regulatory_compliance_score: 80.0,
    composite_score: 84.15,
    risk_level: "critique",
    primary_pattern: "Réseau de Désinformation Organisé",
    key_signals: ["désinformation:88.0%", "crédibilité:85.0%", "indépendance:82.0%"],
    estimated_media_index: 8.42,
    last_updated: "2026-06-20",
    alert_level: "ROUGE",
  },
  {
    entity_id: "MED-002",
    name: "Réseau InfoWars Global",
    country: "États-Unis",
    sector: "Médias Alternatifs",
    disinformation_spread_score: 82.0,
    source_credibility_gap_score: 79.0,
    editorial_independence_score: 78.0,
    regulatory_compliance_score: 70.0,
    composite_score: 77.85,
    risk_level: "critique",
    primary_pattern: "Déficit de Vérification des Sources",
    key_signals: ["désinformation:82.0%", "crédibilité:79.0%", "indépendance:78.0%"],
    estimated_media_index: 7.79,
    last_updated: "2026-06-20",
    alert_level: "ROUGE",
  },
  {
    entity_id: "MED-003",
    name: "CCTV International",
    country: "Chine",
    sector: "Médias d'État International",
    disinformation_spread_score: 75.0,
    source_credibility_gap_score: 72.0,
    editorial_independence_score: 80.0,
    regulatory_compliance_score: 55.0,
    composite_score: 71.5,
    risk_level: "critique",
    primary_pattern: "Déficit de Vérification des Sources",
    key_signals: ["désinformation:75.0%", "crédibilité:72.0%", "indépendance:80.0%"],
    estimated_media_index: 7.15,
    last_updated: "2026-06-20",
    alert_level: "ROUGE",
  },
  {
    entity_id: "MED-004",
    name: "Canal Politique Partisan",
    country: "Hongrie",
    sector: "Médias Politiques",
    disinformation_spread_score: 58.0,
    source_credibility_gap_score: 52.0,
    editorial_independence_score: 55.0,
    regulatory_compliance_score: 45.0,
    composite_score: 53.15,
    risk_level: "élevé",
    primary_pattern: "Polarisation Médiatique Progressive",
    key_signals: ["désinformation:58.0%", "crédibilité:52.0%", "indépendance:55.0%"],
    estimated_media_index: 5.32,
    last_updated: "2026-06-20",
    alert_level: "ORANGE",
  },
  {
    entity_id: "MED-005",
    name: "Chaîne Commerciale Biaisée",
    country: "Brésil",
    sector: "Médias Commerciaux",
    disinformation_spread_score: 50.0,
    source_credibility_gap_score: 47.0,
    editorial_independence_score: 48.0,
    regulatory_compliance_score: 38.0,
    composite_score: 46.35,
    risk_level: "élevé",
    primary_pattern: "Polarisation Médiatique Progressive",
    key_signals: ["désinformation:50.0%", "crédibilité:47.0%", "indépendance:48.0%"],
    estimated_media_index: 4.64,
    last_updated: "2026-06-20",
    alert_level: "ORANGE",
  },
  {
    entity_id: "MED-006",
    name: "Presse Régionale Indépendante",
    country: "Italie",
    sector: "Presse Écrite",
    disinformation_spread_score: 35.0,
    source_credibility_gap_score: 30.0,
    editorial_independence_score: 28.0,
    regulatory_compliance_score: 25.0,
    composite_score: 30.0,
    risk_level: "modéré",
    primary_pattern: "Surveillance Standard",
    key_signals: ["désinformation:35.0%", "crédibilité:30.0%", "indépendance:28.0%"],
    estimated_media_index: 3.0,
    last_updated: "2026-06-20",
    alert_level: "JAUNE",
  },
  {
    entity_id: "MED-007",
    name: "BBC World Service",
    country: "Royaume-Uni",
    sector: "Service Public",
    disinformation_spread_score: 15.0,
    source_credibility_gap_score: 12.0,
    editorial_independence_score: 10.0,
    regulatory_compliance_score: 8.0,
    composite_score: 11.6,
    risk_level: "faible",
    primary_pattern: "Surveillance Standard",
    key_signals: ["désinformation:15.0%", "crédibilité:12.0%", "indépendance:10.0%"],
    estimated_media_index: 1.16,
    last_updated: "2026-06-20",
    alert_level: "VERT",
  },
  {
    entity_id: "MED-008",
    name: "Reuters Foundation",
    country: "Royaume-Uni",
    sector: "Agence de Presse",
    disinformation_spread_score: 10.0,
    source_credibility_gap_score: 8.0,
    editorial_independence_score: 7.0,
    regulatory_compliance_score: 5.0,
    composite_score: 7.75,
    risk_level: "faible",
    primary_pattern: "Surveillance Standard",
    key_signals: ["désinformation:10.0%", "crédibilité:8.0%", "indépendance:7.0%"],
    estimated_media_index: 0.78,
    last_updated: "2026-06-20",
    alert_level: "VERT",
  },
];

function getMockData() {
  return {
    total_entities: 8,
    avg_composite: 47.79,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      "Réseau de Désinformation Organisé": 1,
      "Déficit de Vérification des Sources": 2,
      "Polarisation Médiatique Progressive": 2,
      "Surveillance Standard": 3,
    },
    top_risk_entities: ["Russia Today Network", "Réseau InfoWars Global", "CCTV International"],
    critical_alerts: 3,
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "media",
    confidence_score: 88.0,
    data_sources: ["RSF Index", "Freedom House", "EIU Democracy Index"],
    entities,
    avg_estimated_media_index: 4.78,
  };
}

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData() as Record<string, unknown>, "Media Integrity Agent"));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/media-integrity-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data as Record<string, unknown>, "Media Integrity Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData() as Record<string, unknown>, "Media Integrity Agent"),
      { status: 502 }
    );
  }
}
