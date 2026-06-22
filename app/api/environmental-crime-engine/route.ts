import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[environmental-crime-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Environmental Crime Engine Agent",
  domain: "environmental_crime",
  total_entities: 8,
  avg_composite: 60.1,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { environmental_defender_killings: 2, wildlife_trafficking_networks: 2, illegal_extraction_corruption: 2, ecocide_scale_impunity: 2 },
  top_risk_entities: [
    "Brésil/Amazonie — Déforestation Illégale 10K km²/an, Garimpeiros & Défenseurs Assassinés",
    "Afrique/Braconnage — Trafic Ivoire/Rhinocéros, Réseaux Asie & Corruption Gardes Parcs",
    "Asie SE/Déforestation — Huile Palme Bornéo, Concessions Illégales & Incendies Délibérés",
  ],
  critical_alerts: [
    "Brésil/Amazonie: environmental_defender_killings",
    "Afrique/Braconnage: wildlife_trafficking_networks",
    "Asie SE/Déforestation: illegal_extraction_corruption",
    "Russie/Arctique: ecocide_scale_impunity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_environmental_crime_index: 6.01,
  data_sources: [
    "global_witness_environmental_defenders_killed_annual_report",
    "unodc_world_wildlife_crime_report_trafficking_analysis",
    "interpol_environmental_crime_global_threat_assessment",
  ],
  entities: [
    { id: "EC-001", name: "Brésil/Amazonie — Déforestation Illégale 10K km²/an, Garimpeiros & Défenseurs Assassinés", country: "Amérique Latine", composite_score: 91.75, ecocide_scale_impunity_score: 95.0, wildlife_trafficking_networks_score: 85.0, illegal_extraction_corruption_score: 92.0, environmental_defender_killings_score: 95.0, risk_level: "critique", primary_pattern: "environmental_defender_killings", estimated_environmental_crime_index: 9.18, last_updated: "2026-06-21" },
    { id: "EC-002", name: "Afrique/Braconnage — Trafic Ivoire/Rhinocéros, Réseaux Asie & Corruption Gardes Parcs", country: "Afrique Sub-Saharienne", composite_score: 88.25, ecocide_scale_impunity_score: 85.0, wildlife_trafficking_networks_score: 95.0, illegal_extraction_corruption_score: 88.0, environmental_defender_killings_score: 85.0, risk_level: "critique", primary_pattern: "wildlife_trafficking_networks", estimated_environmental_crime_index: 8.83, last_updated: "2026-06-21" },
    { id: "EC-003", name: "Asie SE/Déforestation — Huile Palme Bornéo, Concessions Illégales & Incendies Délibérés", country: "Asie du Sud-Est", composite_score: 86.4, ecocide_scale_impunity_score: 88.0, wildlife_trafficking_networks_score: 82.0, illegal_extraction_corruption_score: 90.0, environmental_defender_killings_score: 85.0, risk_level: "critique", primary_pattern: "illegal_extraction_corruption", estimated_environmental_crime_index: 8.64, last_updated: "2026-06-21" },
    { id: "EC-004", name: "Russie/Arctique — Extraction Pétrole Zone Protégée, Marée Norilsk 2020 & Impunité Norilsk Nickel", country: "Europe de l'Est", composite_score: 80.25, ecocide_scale_impunity_score: 82.0, wildlife_trafficking_networks_score: 72.0, illegal_extraction_corruption_score: 85.0, environmental_defender_killings_score: 82.0, risk_level: "critique", primary_pattern: "ecocide_scale_impunity", estimated_environmental_crime_index: 8.03, last_updated: "2026-06-21" },
    { id: "EC-005", name: "Mexique/Honduras — Défenseurs Terres Assassinés, Cartels Mines Illégales & État Complice", country: "Amérique Centrale", composite_score: 55.6, ecocide_scale_impunity_score: 55.0, wildlife_trafficking_networks_score: 52.0, illegal_extraction_corruption_score: 58.0, environmental_defender_killings_score: 58.0, risk_level: "élevé", primary_pattern: "environmental_defender_killings", estimated_environmental_crime_index: 5.56, last_updated: "2026-06-21" },
    { id: "EC-006", name: "UE/Déchets Toxiques — Export Illégal DEEE Afrique, Responsabilité Producteur Insuffisante", country: "Europe", composite_score: 48.3, ecocide_scale_impunity_score: 48.0, wildlife_trafficking_networks_score: 50.0, illegal_extraction_corruption_score: 52.0, environmental_defender_killings_score: 42.0, risk_level: "élevé", primary_pattern: "illegal_extraction_corruption", estimated_environmental_crime_index: 4.83, last_updated: "2026-06-21" },
    { id: "EC-007", name: "Global Witness/EIA — Investigation Crimes Environnementaux, Défenseurs & Plaidoyer Écocide", country: "Global", composite_score: 25.85, ecocide_scale_impunity_score: 22.0, wildlife_trafficking_networks_score: 25.0, illegal_extraction_corruption_score: 28.0, environmental_defender_killings_score: 30.0, risk_level: "modéré", primary_pattern: "ecocide_scale_impunity", estimated_environmental_crime_index: 2.59, last_updated: "2026-06-21" },
    { id: "EC-008", name: "ONU/UNEP — Programme Environnement, Crime Environnemental & Initiative Ecocide CPI Débat", country: "Global", composite_score: 4.4, ecocide_scale_impunity_score: 4.0, wildlife_trafficking_networks_score: 5.0, illegal_extraction_corruption_score: 3.0, environmental_defender_killings_score: 6.0, risk_level: "faible", primary_pattern: "wildlife_trafficking_networks", estimated_environmental_crime_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/environmental-crime-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
