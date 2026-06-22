import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-migration-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Climate Migration Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate-migration-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Climate Migration Agent")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "Climate Migration Agent"),
      { status: 502 }
    ));
  }
}

function getMockData() {
  const entities = [
    {
      id: "MIG-001",
      name: "Îles Maldives",
      country: "Maldives",
      sector: "Réfugiés Climatiques Insulaires",
      composite_score: 89.75,
      displacement_score: 95.0,
      sea_level_risk_score: 88.0,
      desertification_score: 85.0,
      climate_vulnerability_score: 90.0,
      risk_level: "critique",
      primary_pattern: "Déplacement Massif Climatique",
      key_signals: ["Déplacement massif: 95/100", "Risque montée eaux: 88/100", "Vulnérabilité climatique: 90/100"],
      estimated_migration_index: 8.98,
      last_updated: "2026-06-18",
    },
    {
      id: "MIG-002",
      name: "Delta du Bangladesh",
      country: "Bangladesh",
      sector: "Migration Côtière",
      composite_score: 86.4,
      displacement_score: 88.0,
      sea_level_risk_score: 92.0,
      desertification_score: 80.0,
      climate_vulnerability_score: 85.0,
      risk_level: "critique",
      primary_pattern: "Déplacement Massif Climatique",
      key_signals: ["Déplacement massif: 88/100", "Risque montée eaux: 92/100", "Vulnérabilité climatique: 85/100"],
      estimated_migration_index: 8.64,
      last_updated: "2026-06-17",
    },
    {
      id: "MIG-003",
      name: "Sahel Subsaharien",
      country: "Soudan",
      sector: "Migration Aride & Famine",
      composite_score: 79.15,
      displacement_score: 80.0,
      sea_level_risk_score: 75.0,
      desertification_score: 88.0,
      climate_vulnerability_score: 72.0,
      risk_level: "critique",
      primary_pattern: "Déplacement Massif Climatique",
      key_signals: ["Déplacement massif: 80/100", "Désertification: 88/100", "Risque montée eaux: 75/100"],
      estimated_migration_index: 7.92,
      last_updated: "2026-06-16",
    },
    {
      id: "MIG-004",
      name: "Corne de l'Afrique",
      country: "Somalie",
      sector: "Déplacement & Sécheresse",
      composite_score: 66.65,
      displacement_score: 70.0,
      sea_level_risk_score: 65.0,
      desertification_score: 68.0,
      climate_vulnerability_score: 62.0,
      risk_level: "critique",
      primary_pattern: "Déplacement Massif Climatique",
      key_signals: ["Déplacement massif: 70/100", "Désertification: 68/100", "Risque montée eaux: 65/100"],
      estimated_migration_index: 6.67,
      last_updated: "2026-06-15",
    },
    {
      id: "MIG-005",
      name: "Amazonie Brésilienne",
      country: "Brésil",
      sector: "Migration Forêt Tropicale",
      composite_score: 50.0,
      displacement_score: 55.0,
      sea_level_risk_score: 50.0,
      desertification_score: 48.0,
      climate_vulnerability_score: 45.0,
      risk_level: "élevé",
      primary_pattern: "Tension Migratoire Frontalière",
      key_signals: ["Score composite migration: 50/100", "Score composite migration: 50/100", "Score composite migration: 50/100"],
      estimated_migration_index: 5.0,
      last_updated: "2026-06-14",
    },
    {
      id: "MIG-006",
      name: "Pacifique Central Kiribati",
      country: "Kiribati",
      sector: "Submersion Insulaire",
      composite_score: 41.6,
      displacement_score: 45.0,
      sea_level_risk_score: 42.0,
      desertification_score: 40.0,
      climate_vulnerability_score: 38.0,
      risk_level: "élevé",
      primary_pattern: "Tension Migratoire Frontalière",
      key_signals: ["Score composite migration: 41.6/100", "Score composite migration: 41.6/100", "Score composite migration: 41.6/100"],
      estimated_migration_index: 4.16,
      last_updated: "2026-06-13",
    },
    {
      id: "MIG-007",
      name: "Côte Méditerranéenne Maroc",
      country: "Maroc",
      sector: "Migration Climatique Régionale",
      composite_score: 26.55,
      displacement_score: 28.0,
      sea_level_risk_score: 25.0,
      desertification_score: 30.0,
      climate_vulnerability_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "Tension Migratoire Frontalière",
      key_signals: ["Score composite migration: 26.55/100", "Score composite migration: 26.55/100", "Score composite migration: 26.55/100"],
      estimated_migration_index: 2.66,
      last_updated: "2026-06-12",
    },
    {
      id: "MIG-008",
      name: "Pays-Bas Adaptation Côtière",
      country: "Pays-Bas",
      sector: "Génie Civil & Adaptation",
      composite_score: 8.65,
      displacement_score: 10.0,
      sea_level_risk_score: 8.0,
      desertification_score: 5.0,
      climate_vulnerability_score: 12.0,
      risk_level: "faible",
      primary_pattern: "Tension Migratoire Frontalière",
      key_signals: ["Score composite migration: 8.65/100", "Score composite migration: 8.65/100", "Score composite migration: 8.65/100"],
      estimated_migration_index: 0.87,
      last_updated: "2026-06-11",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 56.09,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: {
      "Déplacement Massif Climatique": 4,
      "Inondation Côtière Catastrophique": 0,
      "Désertification et Famine Induite": 0,
      "Vulnérabilité Infrastructurelle Climatique": 0,
      "Tension Migratoire Frontalière": 4,
    },
    top_risk_entities: ["Îles Maldives", "Delta du Bangladesh", "Sahel Subsaharien"],
    critical_alerts: 4,
    last_analysis: "2026-06-20",
    engine_version: "2.1.0",
    domain: "migration",
    confidence_score: 86.1,
    data_sources: ["IDMC", "UNHCR", "IPCC", "IOM", "World Bank Climate Portal"],
    entities,
    avg_estimated_migration_index: 5.61,
  };

  return { entities, summary };
}
