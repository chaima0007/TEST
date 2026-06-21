import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[pandemic-preparedness-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Pandemic Preparedness Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/pandemic-preparedness-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Pandemic Preparedness Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Pandemic Preparedness Agent"),
      { status: 502 }
    );
  }
}

function getMockData(): Record<string, unknown> {
  const entities = [
    {
      id: "PAN-001",
      name: "Système de Santé Sahélien",
      country: "Niger",
      sector: "Santé Publique",
      composite_score: 83.0,
      surveillance_gap_score: 88.0,
      healthcare_capacity_gap_score: 84.0,
      vaccine_access_deficit_score: 80.0,
      response_coordination_gap_score: 78.0,
      risk_level: "critique",
      primary_pattern: "Effondrement du Système de Surveillance",
      key_signals: ["surveillance:88.0%", "capacité_santé:84.0%", "vaccin_accès:80.0%"],
      estimated_pandemic_index: 8.3,
      last_updated: "2026-06-20",
      alert_level: "ROUGE",
    },
    {
      id: "PAN-002",
      name: "Infrastructure Médicale Yéménite",
      country: "Yémen",
      sector: "Santé en Zone de Conflit",
      composite_score: 76.7,
      surveillance_gap_score: 82.0,
      healthcare_capacity_gap_score: 78.0,
      vaccine_access_deficit_score: 76.0,
      response_coordination_gap_score: 68.0,
      risk_level: "critique",
      primary_pattern: "Saturation des Capacités Hospitalières",
      key_signals: ["surveillance:82.0%", "capacité_santé:78.0%", "vaccin_accès:76.0%"],
      estimated_pandemic_index: 7.67,
      last_updated: "2026-06-20",
      alert_level: "ROUGE",
    },
    {
      id: "PAN-003",
      name: "Réseau Sanitaire Amazonien",
      country: "Brésil",
      sector: "Santé Tropicale",
      composite_score: 69.1,
      surveillance_gap_score: 74.0,
      healthcare_capacity_gap_score: 70.0,
      vaccine_access_deficit_score: 68.0,
      response_coordination_gap_score: 62.0,
      risk_level: "critique",
      primary_pattern: "Désert Vaccinal Critique",
      key_signals: ["surveillance:74.0%", "capacité_santé:70.0%", "vaccin_accès:68.0%"],
      estimated_pandemic_index: 6.91,
      last_updated: "2026-06-20",
      alert_level: "ROUGE",
    },
    {
      id: "PAN-004",
      name: "Système Hospitalier Bangladais",
      country: "Bangladesh",
      sector: "Santé Densité Urbaine",
      composite_score: 53.15,
      surveillance_gap_score: 58.0,
      healthcare_capacity_gap_score: 55.0,
      vaccine_access_deficit_score: 52.0,
      response_coordination_gap_score: 45.0,
      risk_level: "élevé",
      primary_pattern: "Fragilité Sanitaire Structurelle",
      key_signals: ["surveillance:58.0%", "capacité_santé:55.0%", "vaccin_accès:52.0%"],
      estimated_pandemic_index: 5.32,
      last_updated: "2026-06-20",
      alert_level: "ORANGE",
    },
    {
      id: "PAN-005",
      name: "Infrastructure Sanitaire Philippine",
      country: "Philippines",
      sector: "Santé Insulaire",
      composite_score: 45.5,
      surveillance_gap_score: 50.0,
      healthcare_capacity_gap_score: 46.0,
      vaccine_access_deficit_score: 44.0,
      response_coordination_gap_score: 40.0,
      risk_level: "élevé",
      primary_pattern: "Fragilité Sanitaire Structurelle",
      key_signals: ["surveillance:50.0%", "capacité_santé:46.0%", "vaccin_accès:44.0%"],
      estimated_pandemic_index: 4.55,
      last_updated: "2026-06-20",
      alert_level: "ORANGE",
    },
    {
      id: "PAN-006",
      name: "Réseau Santé Régional Balkans",
      country: "Serbie",
      sector: "Santé Régionale",
      composite_score: 30.0,
      surveillance_gap_score: 35.0,
      healthcare_capacity_gap_score: 30.0,
      vaccine_access_deficit_score: 28.0,
      response_coordination_gap_score: 25.0,
      risk_level: "modéré",
      primary_pattern: "Surveillance Standard",
      key_signals: ["surveillance:35.0%", "capacité_santé:30.0%", "vaccin_accès:28.0%"],
      estimated_pandemic_index: 3.0,
      last_updated: "2026-06-20",
      alert_level: "JAUNE",
    },
    {
      id: "PAN-007",
      name: "Système Santé Nordique",
      country: "Norvège",
      sector: "Santé Publique Avancée",
      composite_score: 10.8,
      surveillance_gap_score: 14.0,
      healthcare_capacity_gap_score: 10.0,
      vaccine_access_deficit_score: 10.0,
      response_coordination_gap_score: 8.0,
      risk_level: "faible",
      primary_pattern: "Surveillance Standard",
      key_signals: ["surveillance:14.0%", "capacité_santé:10.0%", "vaccin_accès:10.0%"],
      estimated_pandemic_index: 1.08,
      last_updated: "2026-06-20",
      alert_level: "VERT",
    },
    {
      id: "PAN-008",
      name: "CDC & Systèmes OMS Genève",
      country: "Suisse",
      sector: "Coordination Internationale",
      composite_score: 7.75,
      surveillance_gap_score: 10.0,
      healthcare_capacity_gap_score: 8.0,
      vaccine_access_deficit_score: 7.0,
      response_coordination_gap_score: 5.0,
      risk_level: "faible",
      primary_pattern: "Surveillance Standard",
      key_signals: ["surveillance:10.0%", "capacité_santé:8.0%", "vaccin_accès:7.0%"],
      estimated_pandemic_index: 0.78,
      last_updated: "2026-06-20",
      alert_level: "VERT",
    },
  ];

  return {
    total_entities: 8,
    avg_composite: 47.0,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      "Effondrement du Système de Surveillance": 1,
      "Saturation des Capacités Hospitalières": 1,
      "Désert Vaccinal Critique": 1,
      "Fragilité Sanitaire Structurelle": 2,
      "Surveillance Standard": 3,
    },
    top_risk_entities: [
      "Système de Santé Sahélien",
      "Infrastructure Médicale Yéménite",
      "Réseau Sanitaire Amazonien",
    ],
    critical_alerts: 3,
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "pandemic",
    confidence_score: 86.0,
    data_sources: ["OMS", "GHS Index", "JHU CSSE"],
    entities,
    avg_estimated_pandemic_index: 4.7,
  };
}
