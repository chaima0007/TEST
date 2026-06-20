import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[child-marriage-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Child Marriage Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-marriage-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Child Marriage Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Child Marriage Agent"),
      { status: 502 }
    );
  }
}

function getMockData() {
  const entities = [
    {
      entity_id: "MAR-001",
      name: "Région Sahel Niger",
      country: "Niger",
      sector: "Droits Humains & Protection",
      composite_score: 89.1,
      prevalence_score: 92.0,
      legal_protection_gap_score: 88.0,
      education_gap_score: 90.0,
      socioeconomic_pressure_score: 85.0,
      risk_level: "critique",
      primary_pattern: "Prévalence Mariage Infantile Critique",
      key_signals: ["Prévalence critique: 92/100", "Défaillance législative: 88/100", "Exclusion scolaire: 90/100"],
      estimated_marriage_index: 8.91,
      last_updated: "2026-06-18",
    },
    {
      entity_id: "MAR-002",
      name: "Zone Rurale Bangladesh",
      country: "Bangladesh",
      sector: "Développement Rural",
      composite_score: 83.6,
      prevalence_score: 85.0,
      legal_protection_gap_score: 82.0,
      education_gap_score: 80.0,
      socioeconomic_pressure_score: 88.0,
      risk_level: "critique",
      primary_pattern: "Prévalence Mariage Infantile Critique",
      key_signals: ["Prévalence critique: 85/100", "Défaillance législative: 82/100", "Pression socio-économique: 88/100"],
      estimated_marriage_index: 8.36,
      last_updated: "2026-06-17",
    },
    {
      entity_id: "MAR-003",
      name: "Province Nord Mali",
      country: "Mali",
      sector: "Gouvernance Locale",
      composite_score: 76.65,
      prevalence_score: 80.0,
      legal_protection_gap_score: 78.0,
      education_gap_score: 75.0,
      socioeconomic_pressure_score: 72.0,
      risk_level: "critique",
      primary_pattern: "Prévalence Mariage Infantile Critique",
      key_signals: ["Prévalence critique: 80/100", "Défaillance législative: 78/100", "Score composite mariage: 76.65/100"],
      estimated_marriage_index: 7.67,
      last_updated: "2026-06-16",
    },
    {
      entity_id: "MAR-004",
      name: "Districts Ruraux Pakistan",
      country: "Pakistan",
      sector: "Protection de l'Enfance",
      composite_score: 66.65,
      prevalence_score: 70.0,
      legal_protection_gap_score: 65.0,
      education_gap_score: 68.0,
      socioeconomic_pressure_score: 62.0,
      risk_level: "critique",
      primary_pattern: "Prévalence Mariage Infantile Critique",
      key_signals: ["Prévalence critique: 70/100", "Défaillance législative: 65/100", "Exclusion scolaire: 68/100"],
      estimated_marriage_index: 6.67,
      last_updated: "2026-06-15",
    },
    {
      entity_id: "MAR-005",
      name: "Communautés Rurales Éthiopie",
      country: "Éthiopie",
      sector: "Développement Communautaire",
      composite_score: 50.0,
      prevalence_score: 55.0,
      legal_protection_gap_score: 48.0,
      education_gap_score: 50.0,
      socioeconomic_pressure_score: 45.0,
      risk_level: "élevé",
      primary_pattern: "Risque Norme Culturelle Persistante",
      key_signals: ["Score composite mariage: 50/100", "Score composite mariage: 50/100", "Score composite mariage: 50/100"],
      estimated_marriage_index: 5.0,
      last_updated: "2026-06-14",
    },
    {
      entity_id: "MAR-006",
      name: "Zones Tribales Afghanistan",
      country: "Afghanistan",
      sector: "Droit Coutumier & Tribal",
      composite_score: 41.6,
      prevalence_score: 45.0,
      legal_protection_gap_score: 42.0,
      education_gap_score: 40.0,
      socioeconomic_pressure_score: 38.0,
      risk_level: "élevé",
      primary_pattern: "Risque Norme Culturelle Persistante",
      key_signals: ["Score composite mariage: 41.6/100", "Score composite mariage: 41.6/100", "Score composite mariage: 41.6/100"],
      estimated_marriage_index: 4.16,
      last_updated: "2026-06-13",
    },
    {
      entity_id: "MAR-007",
      name: "Régions Rurales Inde",
      country: "Inde",
      sector: "Réforme Législative",
      composite_score: 26.65,
      prevalence_score: 30.0,
      legal_protection_gap_score: 25.0,
      education_gap_score: 28.0,
      socioeconomic_pressure_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "Risque Norme Culturelle Persistante",
      key_signals: ["Score composite mariage: 26.65/100", "Score composite mariage: 26.65/100", "Score composite mariage: 26.65/100"],
      estimated_marriage_index: 2.67,
      last_updated: "2026-06-12",
    },
    {
      entity_id: "MAR-008",
      name: "Programme ONG Maroc",
      country: "Maroc",
      sector: "ONG & Société Civile",
      composite_score: 10.0,
      prevalence_score: 10.0,
      legal_protection_gap_score: 8.0,
      education_gap_score: 12.0,
      socioeconomic_pressure_score: 10.0,
      risk_level: "faible",
      primary_pattern: "Risque Norme Culturelle Persistante",
      key_signals: ["Score composite mariage: 10/100", "Score composite mariage: 10/100", "Score composite mariage: 10/100"],
      estimated_marriage_index: 1.0,
      last_updated: "2026-06-11",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 55.53,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: {
      "Prévalence Mariage Infantile Critique": 4,
      "Défaillance Législative Grave": 0,
      "Exclusion Scolaire Féminine": 0,
      "Pression Socio-Économique Familiale": 0,
      "Risque Norme Culturelle Persistante": 4,
    },
    top_risk_entities: ["Région Sahel Niger", "Zone Rurale Bangladesh", "Province Nord Mali"],
    critical_alerts: 4,
    last_analysis: "2026-06-20",
    engine_version: "2.1.0",
    domain: "marriage",
    confidence_score: 82.9,
    data_sources: ["UNICEF", "OMS", "UNFPA", "Girls Not Brides", "World Bank"],
    entities,
    avg_estimated_marriage_index: 5.55,
  };

  return { entities, summary };
}
