import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[land-degradation-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Land Degradation Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/land-degradation-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data as Record<string, unknown>, "Land Degradation Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Land Degradation Agent"), { status: 502 }));
  }
}

function getMockData(): Record<string, unknown> {
  // avg_composite = (84.15 + 79.55 + 70.75 + 53.5 + 45.5 + 30.6 + 11.6 + 7.95) / 8
  //              = 383.6 / 8 = 47.95
  const entities = [
    // ── CRITIQUE (3) ──────────────────────────────────────────────────────────
    {
      id: "LND-001",
      name: "Sahel Occidental",
      country: "Mali",
      sector: "Agriculture & Élevage",
      composite_score: 84.15,
      soil_erosion_score: 88.0,
      desertification_score: 85.0,
      deforestation_score: 82.0,
      land_use_pressure_score: 80.0,
      risk_level: "critique",
      primary_pattern: "Érosion Catastrophique des Sols",
      key_signals: ["erosion:88.0%", "désertification:85.0%", "déforestation:82.0%"],
      estimated_land_index: 8.42,
      last_updated: "2026-06-20",
      alert_level: "ROUGE",
    },
    {
      id: "LND-002",
      name: "Amazonie Brésilienne Nord",
      country: "Brésil",
      sector: "Déforestation Tropicale",
      composite_score: 79.55,
      soil_erosion_score: 80.0,
      desertification_score: 77.0,
      deforestation_score: 86.0,
      land_use_pressure_score: 74.0,
      risk_level: "critique",
      primary_pattern: "Pression Agricole Intensive",
      key_signals: ["erosion:80.0%", "désertification:77.0%", "déforestation:86.0%"],
      estimated_land_index: 7.96,
      last_updated: "2026-06-20",
      alert_level: "ROUGE",
    },
    {
      id: "LND-003",
      name: "Plaines d'Asie Centrale",
      country: "Kazakhstan",
      sector: "Terres Agricoles Dégradées",
      composite_score: 70.75,
      soil_erosion_score: 75.0,
      desertification_score: 72.0,
      deforestation_score: 65.0,
      land_use_pressure_score: 70.0,
      risk_level: "critique",
      primary_pattern: "Dégradation Progressive",
      key_signals: ["erosion:75.0%", "désertification:72.0%", "déforestation:65.0%"],
      estimated_land_index: 7.08,
      last_updated: "2026-06-20",
      alert_level: "ROUGE",
    },
    // ── ÉLEVÉ (2) ─────────────────────────────────────────────────────────────
    {
      id: "LND-004",
      name: "Bassin du Congo Central",
      country: "RDC",
      sector: "Forêts Tropicales",
      composite_score: 53.5,
      soil_erosion_score: 55.0,
      desertification_score: 52.0,
      deforestation_score: 60.0,
      land_use_pressure_score: 45.0,
      risk_level: "élevé",
      primary_pattern: "Dégradation Progressive",
      key_signals: ["erosion:55.0%", "désertification:52.0%", "déforestation:60.0%"],
      estimated_land_index: 5.35,
      last_updated: "2026-06-20",
      alert_level: "ORANGE",
    },
    {
      id: "LND-005",
      name: "Méditerranée du Sud",
      country: "Algérie",
      sector: "Agriculture Semi-Aride",
      composite_score: 45.5,
      soil_erosion_score: 50.0,
      desertification_score: 48.0,
      deforestation_score: 42.0,
      land_use_pressure_score: 40.0,
      risk_level: "élevé",
      primary_pattern: "Dégradation Progressive",
      key_signals: ["erosion:50.0%", "désertification:48.0%", "déforestation:42.0%"],
      estimated_land_index: 4.55,
      last_updated: "2026-06-20",
      alert_level: "ORANGE",
    },
    // ── MODÉRÉ (1) ────────────────────────────────────────────────────────────
    {
      id: "LND-006",
      name: "Plaines Européennes Est",
      country: "Pologne",
      sector: "Agriculture Intensive",
      composite_score: 30.6,
      soil_erosion_score: 35.0,
      desertification_score: 28.0,
      deforestation_score: 30.0,
      land_use_pressure_score: 28.0,
      risk_level: "modéré",
      primary_pattern: "Surveillance Standard",
      key_signals: ["erosion:35.0%", "désertification:28.0%", "déforestation:30.0%"],
      estimated_land_index: 3.06,
      last_updated: "2026-06-20",
      alert_level: "JAUNE",
    },
    // ── FAIBLE (2) ────────────────────────────────────────────────────────────
    {
      id: "LND-007",
      name: "Scandinavie Forestière",
      country: "Suède",
      sector: "Gestion Forestière Durable",
      composite_score: 11.6,
      soil_erosion_score: 15.0,
      desertification_score: 10.0,
      deforestation_score: 12.0,
      land_use_pressure_score: 8.0,
      risk_level: "faible",
      primary_pattern: "Surveillance Standard",
      key_signals: ["erosion:15.0%", "désertification:10.0%", "déforestation:12.0%"],
      estimated_land_index: 1.16,
      last_updated: "2026-06-20",
      alert_level: "VERT",
    },
    {
      id: "LND-008",
      name: "Patagonie Protégée",
      country: "Argentine",
      sector: "Aires Protégées",
      composite_score: 7.95,
      soil_erosion_score: 10.0,
      desertification_score: 8.0,
      deforestation_score: 7.0,
      land_use_pressure_score: 6.0,
      risk_level: "faible",
      primary_pattern: "Surveillance Standard",
      key_signals: ["erosion:10.0%", "désertification:8.0%", "déforestation:7.0%"],
      estimated_land_index: 0.8,
      last_updated: "2026-06-20",
      alert_level: "VERT",
    },
  ];

  return {
    total_entities: 8,
    avg_composite: 47.95,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      "Érosion Catastrophique des Sols": 1,
      "Pression Agricole Intensive": 1,
      "Dégradation Progressive": 3,
      "Surveillance Standard": 3,
    },
    top_risk_entities: ["Sahel Occidental", "Amazonie Brésilienne Nord", "Plaines d'Asie Centrale"],
    critical_alerts: 3,
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "land",
    confidence_score: 85.0,
    data_sources: ["FAO", "UNCCD", "Global Land Watch"],
    entities,
    avg_estimated_land_index: 4.79,
  };
}
