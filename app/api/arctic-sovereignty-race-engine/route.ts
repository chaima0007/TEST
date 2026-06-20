import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[arctic-sovereignty-race-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Arctic Sovereignty Race Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/arctic-sovereignty-race-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Arctic Sovereignty Race Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Arctic Sovereignty Race Agent"),
      { status: 502 }
    );
  }
}

function getMockData() {
  const entities = [
    {
      entity_id: "SOV-001",
      name: "Opération Polaire Russe",
      country: "Russie",
      sector: "Défense & Militaire",
      composite_score: 88.85,
      territorial_claim_score: 92.0,
      military_buildup_score: 88.0,
      resource_extraction_score: 85.0,
      maritime_route_score: 90.0,
      risk_level: "critique",
      primary_pattern: "Militarisation Arctique",
      key_signals: ["Militarisation critique: 88/100", "Route maritime contestée: 90/100", "Extraction illégale: 85/100"],
      estimated_sovereignty_index: 8.89,
      last_updated: "2026-06-18",
    },
    {
      entity_id: "SOV-002",
      name: "Base Arctique Severomorsk",
      country: "Russie",
      sector: "Infrastructure Militaire",
      composite_score: 84.4,
      territorial_claim_score: 85.0,
      military_buildup_score: 92.0,
      resource_extraction_score: 78.0,
      maritime_route_score: 82.0,
      risk_level: "critique",
      primary_pattern: "Militarisation Arctique",
      key_signals: ["Militarisation critique: 92/100", "Route maritime contestée: 82/100", "Revendication territoriale: 85/100"],
      estimated_sovereignty_index: 8.44,
      last_updated: "2026-06-17",
    },
    {
      entity_id: "SOV-003",
      name: "Projet Extraction Pétrole Arctique",
      country: "Russie",
      sector: "Énergie & Extraction",
      composite_score: 79.9,
      territorial_claim_score: 80.0,
      military_buildup_score: 78.0,
      resource_extraction_score: 88.0,
      maritime_route_score: 72.0,
      risk_level: "critique",
      primary_pattern: "Militarisation Arctique",
      key_signals: ["Militarisation critique: 78/100", "Extraction illégale: 88/100", "Revendication territoriale: 80/100"],
      estimated_sovereignty_index: 7.99,
      last_updated: "2026-06-16",
    },
    {
      entity_id: "SOV-004",
      name: "Revendication Passage Nord-Est",
      country: "Chine",
      sector: "Commerce Maritime",
      composite_score: 61.4,
      territorial_claim_score: 68.0,
      military_buildup_score: 62.0,
      resource_extraction_score: 58.0,
      maritime_route_score: 55.0,
      risk_level: "critique",
      primary_pattern: "Revendication Territoriale Escaladante",
      key_signals: ["Revendication territoriale: 68/100", "Score composite souveraineté: 61.4/100", "Score composite souveraineté: 61.4/100"],
      estimated_sovereignty_index: 6.14,
      last_updated: "2026-06-15",
    },
    {
      entity_id: "SOV-005",
      name: "Programme Arctique Norvégien",
      country: "Norvège",
      sector: "Ressources Naturelles",
      composite_score: 48.15,
      territorial_claim_score: 55.0,
      military_buildup_score: 48.0,
      resource_extraction_score: 45.0,
      maritime_route_score: 42.0,
      risk_level: "élevé",
      primary_pattern: "Tension de Gouvernance Arctique",
      key_signals: ["Score composite souveraineté: 48.15/100", "Score composite souveraineté: 48.15/100", "Score composite souveraineté: 48.15/100"],
      estimated_sovereignty_index: 4.82,
      last_updated: "2026-06-14",
    },
    {
      entity_id: "SOV-006",
      name: "Initiative Groenland Danois",
      country: "Danemark",
      sector: "Gouvernance Territoriale",
      composite_score: 40.9,
      territorial_claim_score: 48.0,
      military_buildup_score: 38.0,
      resource_extraction_score: 40.0,
      maritime_route_score: 35.0,
      risk_level: "élevé",
      primary_pattern: "Tension de Gouvernance Arctique",
      key_signals: ["Score composite souveraineté: 40.9/100", "Score composite souveraineté: 40.9/100", "Score composite souveraineté: 40.9/100"],
      estimated_sovereignty_index: 4.09,
      last_updated: "2026-06-13",
    },
    {
      entity_id: "SOV-007",
      name: "Patrouille Côtière Canada",
      country: "Canada",
      sector: "Garde-Côtes & Surveillance",
      composite_score: 24.75,
      territorial_claim_score: 30.0,
      military_buildup_score: 22.0,
      resource_extraction_score: 25.0,
      maritime_route_score: 20.0,
      risk_level: "modéré",
      primary_pattern: "Tension de Gouvernance Arctique",
      key_signals: ["Score composite souveraineté: 24.75/100", "Score composite souveraineté: 24.75/100", "Score composite souveraineté: 24.75/100"],
      estimated_sovereignty_index: 2.48,
      last_updated: "2026-06-12",
    },
    {
      entity_id: "SOV-008",
      name: "Station Recherche Arctique USA",
      country: "États-Unis",
      sector: "Recherche Scientifique",
      composite_score: 11.1,
      territorial_claim_score: 12.0,
      military_buildup_score: 8.0,
      resource_extraction_score: 10.0,
      maritime_route_score: 15.0,
      risk_level: "faible",
      primary_pattern: "Tension de Gouvernance Arctique",
      key_signals: ["Score composite souveraineté: 11.1/100", "Score composite souveraineté: 11.1/100", "Score composite souveraineté: 11.1/100"],
      estimated_sovereignty_index: 1.11,
      last_updated: "2026-06-11",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 54.93,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: {
      "Militarisation Arctique": 3,
      "Contestation de Route Maritime": 0,
      "Extraction Illégale de Ressources": 0,
      "Revendication Territoriale Escaladante": 1,
      "Tension de Gouvernance Arctique": 4,
    },
    top_risk_entities: ["Opération Polaire Russe", "Base Arctique Severomorsk", "Projet Extraction Pétrole Arctique"],
    critical_alerts: 4,
    last_analysis: "2026-06-20",
    engine_version: "2.1.0",
    domain: "sovereignty",
    confidence_score: 87.4,
    data_sources: ["Arctic Council", "SIPRI", "UN Law of the Sea", "NATO Intelligence", "Satellite Imagery"],
    entities,
    avg_estimated_sovereignty_index: 5.49,
  };

  return { entities, summary };
}
