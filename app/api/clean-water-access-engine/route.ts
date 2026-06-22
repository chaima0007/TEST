import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[clean-water-access-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Clean Water Access Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/clean-water-access-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Clean Water Access Agent")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "Clean Water Access Agent"),
      { status: 502 }
    ));
  }
}

function getMockData() {
  const entities = [
    {
      id: "WAT-001",
      name: "Bassin du Lac Tchad",
      country: "Tchad",
      sector: "Ressources Hydriques",
      composite_score: 90.0,
      water_stress_score: 95.0,
      contamination_score: 88.0,
      infrastructure_failure_score: 90.0,
      access_exclusion_score: 85.0,
      risk_level: "critique",
      primary_pattern: "Stress Hydrique Extrême",
      key_signals: ["Stress hydrique: 95/100", "Contamination source: 88/100", "Défaillance infra: 90/100"],
      estimated_water_index: 9.0,
      last_updated: "2026-06-18",
    },
    {
      id: "WAT-002",
      name: "Aquifère Ogallala Kansas",
      country: "États-Unis",
      sector: "Agriculture & Irrigation",
      composite_score: 83.6,
      water_stress_score: 85.0,
      contamination_score: 82.0,
      infrastructure_failure_score: 80.0,
      access_exclusion_score: 88.0,
      risk_level: "critique",
      primary_pattern: "Stress Hydrique Extrême",
      key_signals: ["Stress hydrique: 85/100", "Contamination source: 82/100", "Exclusion accès: 88/100"],
      estimated_water_index: 8.36,
      last_updated: "2026-06-17",
    },
    {
      id: "WAT-003",
      name: "Péninsule Arabique Yémen",
      country: "Yémen",
      sector: "Eau Potable Urbaine",
      composite_score: 76.55,
      water_stress_score: 78.0,
      contamination_score: 80.0,
      infrastructure_failure_score: 75.0,
      access_exclusion_score: 72.0,
      risk_level: "critique",
      primary_pattern: "Contamination Critique de Source",
      key_signals: ["Contamination source: 80/100", "Stress hydrique: 78/100", "Défaillance infra: 75/100"],
      estimated_water_index: 7.66,
      last_updated: "2026-06-16",
    },
    {
      id: "WAT-004",
      name: "Delta du Gange Bengale",
      country: "Bangladesh",
      sector: "Assainissement & Eau",
      composite_score: 66.5,
      water_stress_score: 70.0,
      contamination_score: 62.0,
      infrastructure_failure_score: 68.0,
      access_exclusion_score: 65.0,
      risk_level: "critique",
      primary_pattern: "Stress Hydrique Extrême",
      key_signals: ["Stress hydrique: 70/100", "Défaillance infra: 68/100", "Exclusion accès: 65/100"],
      estimated_water_index: 6.65,
      last_updated: "2026-06-15",
    },
    {
      id: "WAT-005",
      name: "Zones Rurales Mozambique",
      country: "Mozambique",
      sector: "Développement Rural",
      composite_score: 49.1,
      water_stress_score: 52.0,
      contamination_score: 48.0,
      infrastructure_failure_score: 50.0,
      access_exclusion_score: 45.0,
      risk_level: "élevé",
      primary_pattern: "Risque Gouvernance Eau",
      key_signals: ["Score composite eau: 49.1/100", "Score composite eau: 49.1/100", "Score composite eau: 49.1/100"],
      estimated_water_index: 4.91,
      last_updated: "2026-06-14",
    },
    {
      id: "WAT-006",
      name: "Hauts Plateaux Bolivie",
      country: "Bolivie",
      sector: "Eau Communautaire",
      composite_score: 41.6,
      water_stress_score: 45.0,
      contamination_score: 42.0,
      infrastructure_failure_score: 40.0,
      access_exclusion_score: 38.0,
      risk_level: "élevé",
      primary_pattern: "Risque Gouvernance Eau",
      key_signals: ["Score composite eau: 41.6/100", "Score composite eau: 41.6/100", "Score composite eau: 41.6/100"],
      estimated_water_index: 4.16,
      last_updated: "2026-06-13",
    },
    {
      id: "WAT-007",
      name: "Province Rurale Ouganda",
      country: "Ouganda",
      sector: "WASH & Santé Publique",
      composite_score: 26.55,
      water_stress_score: 28.0,
      contamination_score: 25.0,
      infrastructure_failure_score: 30.0,
      access_exclusion_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "Risque Gouvernance Eau",
      key_signals: ["Score composite eau: 26.55/100", "Score composite eau: 26.55/100", "Score composite eau: 26.55/100"],
      estimated_water_index: 2.66,
      last_updated: "2026-06-12",
    },
    {
      id: "WAT-008",
      name: "Réseau Eau Potable Danemark",
      country: "Danemark",
      sector: "Infrastructure Municipale",
      composite_score: 8.55,
      water_stress_score: 8.0,
      contamination_score: 5.0,
      infrastructure_failure_score: 10.0,
      access_exclusion_score: 12.0,
      risk_level: "faible",
      primary_pattern: "Risque Gouvernance Eau",
      key_signals: ["Score composite eau: 8.55/100", "Score composite eau: 8.55/100", "Score composite eau: 8.55/100"],
      estimated_water_index: 0.86,
      last_updated: "2026-06-11",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 55.31,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: {
      "Stress Hydrique Extrême": 3,
      "Contamination Critique de Source": 1,
      "Défaillance Infrastructurelle Majeure": 0,
      "Exclusion d'Accès Populations Vulnérables": 0,
      "Risque Gouvernance Eau": 4,
    },
    top_risk_entities: ["Bassin du Lac Tchad", "Aquifère Ogallala Kansas", "Péninsule Arabique Yémen"],
    critical_alerts: 4,
    last_analysis: "2026-06-20",
    engine_version: "2.1.0",
    domain: "water",
    confidence_score: 89.2,
    data_sources: ["OMS", "UNICEF JMP", "FAO AQUASTAT", "World Resources Institute", "PNUE"],
    entities,
    avg_estimated_water_index: 5.53,
  };

  return { entities, summary };
}
