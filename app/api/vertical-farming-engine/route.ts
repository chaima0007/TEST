import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[vertical-farming-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Vertical Farming Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/vertical-farming-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Vertical Farming Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Vertical Farming Agent"), { status: 502 });
  }
}

function getMockData() {
  const lastAnalysis = "2026-06-20T08:00:00Z";

  const entities = [
    {
      entity_id: "VF-001",
      name: "AeroFarm Detroit",
      country: "USA",
      sector: "Vertical Farming",
      domain: "farming",
      composite_score: 65.5,
      yield_score: 72.0,
      energy_score: 68.0,
      sustainability_score: 58.0,
      scalability_score: 62.0,
      risk_level: "critique",
      primary_pattern: "Rendement Insuffisant Critique",
      key_signals: [
        "Rendement en kg/m² inférieur de 45% aux benchmarks sectoriels américains",
        "Coût de production unitaire non compétitif face aux importations mexicaines",
        "Turnover opérateur de 38% sur 12 mois fragilisant la continuité des cycles",
      ],
      estimated_farming_index: 6.55,
      last_updated: lastAnalysis,
    },
    {
      entity_id: "VF-002",
      name: "UrbanCrop Asia",
      country: "Bangladesh",
      sector: "Urban Agriculture",
      domain: "farming",
      composite_score: 65.5,
      yield_score: 65.0,
      energy_score: 78.0,
      sustainability_score: 62.0,
      scalability_score: 55.0,
      risk_level: "critique",
      primary_pattern: "Consommation Énergie Excessive",
      key_signals: [
        "Consommation électrique de 28 kWh/kg — plus de 2x la moyenne sectorielle asiatique",
        "Réseau électrique local instable provoquant 14% de pertes de cycles sur l'année",
        "Absence de contrat PPA solaire malgré un ensoleillement potentiel de 5,2 kWh/m²/j",
      ],
      estimated_farming_index: 6.55,
      last_updated: lastAnalysis,
    },
    {
      entity_id: "VF-003",
      name: "GrowTech Africa",
      country: "Nigeria",
      sector: "AgriTech",
      domain: "farming",
      composite_score: 64.85,
      yield_score: 70.0,
      energy_score: 60.0,
      sustainability_score: 65.0,
      scalability_score: 63.0,
      risk_level: "critique",
      primary_pattern: "Rendement Insuffisant Critique",
      key_signals: [
        "Infrastructure d'irrigation hydroponique vieillissante causant 22% de perte nutritive",
        "Chaîne du froid insuffisante entraînant 18% de pertes post-récolte avant distribution",
        "Manque de techniciens spécialisés en agriculture verticale sur le marché local nigérian",
      ],
      estimated_farming_index: 6.48,
      last_updated: lastAnalysis,
    },
    {
      entity_id: "VF-004",
      name: "VerticalVeg UK",
      country: "United Kingdom",
      sector: "Horticulture",
      domain: "farming",
      composite_score: 46.0,
      yield_score: 48.0,
      energy_score: 44.0,
      sustainability_score: 52.0,
      scalability_score: 38.0,
      risk_level: "élevé",
      primary_pattern: "Échec Scalabilité",
      key_signals: [
        "Croissance de la surface cultivée de 40% non suivie d'une hausse proportionnelle du rendement",
        "Systèmes de contrôle climatique non centralisés limitant la gestion multi-sites",
        "Brexit complexifiant l'approvisionnement en intrants et équipements spécialisés européens",
      ],
      estimated_farming_index: 4.6,
      last_updated: lastAnalysis,
    },
    {
      entity_id: "VF-005",
      name: "FarmBot EU GmbH",
      country: "Germany",
      sector: "AgriTech",
      domain: "farming",
      composite_score: 45.9,
      yield_score: 45.0,
      energy_score: 50.0,
      sustainability_score: 42.0,
      scalability_score: 47.0,
      risk_level: "élevé",
      primary_pattern: "Impact Carbone Élevé",
      key_signals: [
        "Mix énergétique à 61% fossile malgré les objectifs ESG déclarés pour 2025",
        "Empreinte carbone de 3,8 kgCO₂eq/kg produit — dépassant les seuils de labellisation bio",
        "Pression réglementaire croissante de la nouvelle directive européenne sur l'agriculture durable",
      ],
      estimated_farming_index: 4.59,
      last_updated: lastAnalysis,
    },
    {
      entity_id: "VF-006",
      name: "HydroFarm SARL",
      country: "France",
      sector: "Hydroponic",
      domain: "farming",
      composite_score: 31.15,
      yield_score: 28.0,
      energy_score: 32.0,
      sustainability_score: 35.0,
      scalability_score: 30.0,
      risk_level: "modéré",
      primary_pattern: "Risque Rentabilité",
      key_signals: [
        "Marge brute en baisse de 8 points sur 18 mois sous pression des coûts énergétiques",
        "Portefeuille produits concentré sur la laitue (72% du CA) — diversification insuffisante",
        "Contrats grande distribution à prix fixes ne reflétant pas la hausse des coûts opérationnels",
      ],
      estimated_farming_index: 3.12,
      last_updated: lastAnalysis,
    },
    {
      entity_id: "VF-007",
      name: "Nordic GreenFarm AS",
      country: "Norway",
      sector: "Sustainable Agriculture",
      domain: "farming",
      composite_score: 14.65,
      yield_score: 12.0,
      energy_score: 15.0,
      sustainability_score: 18.0,
      scalability_score: 14.0,
      risk_level: "faible",
      primary_pattern: "Risque Rentabilité",
      key_signals: [
        "Modèle économique solide avec marge brute de 42% grâce à l'énergie hydraulique locale",
        "Certification Nordic Swan obtenue — prime prix de 25% sur les marchés premium nordiques",
        "Partenariat stratégique avec NorgesGruppen couvrant 35% de la capacité de production",
      ],
      estimated_farming_index: 1.46,
      last_updated: lastAnalysis,
    },
    {
      entity_id: "VF-008",
      name: "EcoFarm Netherlands BV",
      country: "Netherlands",
      sector: "Sustainable Agriculture",
      domain: "farming",
      composite_score: 10.9,
      yield_score: 10.0,
      energy_score: 8.0,
      sustainability_score: 14.0,
      scalability_score: 12.0,
      risk_level: "faible",
      primary_pattern: "Risque Rentabilité",
      key_signals: [
        "Leader sectoriel : rendement de 42 kg/m²/an en laitue — 2,3x la moyenne européenne",
        "100% énergie renouvelable via PPA éolien offshore — coût électrique de 0,04 €/kWh",
        "Expansion planifiée de 12 000 m² supplémentaires financée par Rabobank Agri-Finance",
      ],
      estimated_farming_index: 1.09,
      last_updated: lastAnalysis,
    },
  ];

  const avgComposite = Math.round(
    (entities.reduce((s, e) => s + e.composite_score, 0) / entities.length) * 100
  ) / 100;

  return {
    total_entities: entities.length,
    avg_composite: avgComposite,
    risk_distribution: {
      critique: 3,
      "élevé": 2,
      "modéré": 1,
      faible: 2,
    },
    pattern_distribution: {
      "Rendement Insuffisant Critique": 2,
      "Consommation Énergie Excessive": 1,
      "Échec Scalabilité": 1,
      "Impact Carbone Élevé": 1,
      "Risque Rentabilité": 3,
    },
    top_risk_entities: entities.filter((e) => e.composite_score >= 40),
    critical_alerts: [
      "AeroFarm Detroit (USA) — score composite 66/100 — Rendement Insuffisant Critique",
      "UrbanCrop Asia (Bangladesh) — score composite 66/100 — Consommation Énergie Excessive",
      "GrowTech Africa (Nigeria) — score composite 65/100 — Rendement Insuffisant Critique",
    ],
    last_analysis: lastAnalysis,
    engine_version: "1.0.0",
    domain: "farming",
    confidence_score: 80.0,
    data_sources: [
      "FAO Vertical Farming Statistics 2024",
      "USDA Urban Agriculture Report",
      "EU Farm to Fork Strategy Data",
      "IEA Energy in Agriculture 2024",
    ],
    entities,
    avg_estimated_farming_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
  };
}
