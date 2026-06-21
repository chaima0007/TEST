import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[algae-energy-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(
      sealResponse(getMockData(), "Algae Energy Engine Agent"),
    );
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/algae-energy-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Algae Energy Engine Agent"));
  } catch {
    return NextResponse.json(
      sealResponse(getMockData(), "Algae Energy Engine Agent"),
      { status: 502 },
    );
  }
}

function getMockData() {
  const entities = [
    {
      id: "ENT-001",
      name: "SolarAlgae Industries",
      country: "États-Unis",
      sector: "Bioénergie",
      composite_score: 69.85,
      productivity_score: 82.0,
      sustainability_score: 68.0,
      scalability_score: 65.0,
      efficiency_score: 60.0,
      risk_level: "critique",
      primary_pattern: "rendement_critique",
      key_signals: [
        "Niveau de risque critique détecté pour SolarAlgae Industries",
        "Production algale en surcharge — intervention urgente recommandée",
        "Indicateurs d'alerte rouge : rendement et durabilité compromis",
      ],
      estimated_algae_index: 6.99,
      last_updated: "2026-06-20",
      facility_count: 12,
    },
    {
      id: "ENT-002",
      name: "BioPetro Algae",
      country: "Brésil",
      sector: "Pétrochimie Verte",
      composite_score: 64.55,
      productivity_score: 68.0,
      sustainability_score: 75.0,
      scalability_score: 60.0,
      efficiency_score: 52.0,
      risk_level: "critique",
      primary_pattern: "durabilite_compromise",
      key_signals: [
        "Niveau de risque critique détecté pour BioPetro Algae",
        "Production algale en surcharge — intervention urgente recommandée",
        "Indicateurs d'alerte rouge : rendement et durabilité compromis",
      ],
      estimated_algae_index: 6.46,
      last_updated: "2026-06-20",
      facility_count: 8,
    },
    {
      id: "ENT-003",
      name: "AlgaFuel Nordic",
      country: "Norvège",
      sector: "Carburants Alternatifs",
      composite_score: 61.4,
      productivity_score: 65.0,
      sustainability_score: 62.0,
      scalability_score: 72.0,
      efficiency_score: 42.0,
      risk_level: "critique",
      primary_pattern: "echelle_bloquee",
      key_signals: [
        "Niveau de risque critique détecté pour AlgaFuel Nordic",
        "Production algale en surcharge — intervention urgente recommandée",
        "Indicateurs d'alerte rouge : rendement et durabilité compromis",
      ],
      estimated_algae_index: 6.14,
      last_updated: "2026-06-20",
      facility_count: 5,
    },
    {
      id: "ENT-004",
      name: "Spirulina Power SA",
      country: "France",
      sector: "Nutraceutique & Énergie",
      composite_score: 51.3,
      productivity_score: 58.0,
      sustainability_score: 52.0,
      scalability_score: 50.0,
      efficiency_score: 42.0,
      risk_level: "élevé",
      primary_pattern: "systeme_algal_stable",
      key_signals: [
        "Risque élevé identifié dans les opérations de Spirulina Power SA",
        "Surveillance renforcée des paramètres de croissance algale requise",
        "Tendances défavorables détectées sur plusieurs indicateurs clés",
      ],
      estimated_algae_index: 5.13,
      last_updated: "2026-06-20",
      facility_count: 3,
    },
    {
      id: "ENT-005",
      name: "MicroBloom Tech",
      country: "Australie",
      sector: "Biotechnologie Marine",
      composite_score: 44.0,
      productivity_score: 50.0,
      sustainability_score: 46.0,
      scalability_score: 42.0,
      efficiency_score: 35.0,
      risk_level: "élevé",
      primary_pattern: "systeme_algal_stable",
      key_signals: [
        "Risque élevé identifié dans les opérations de MicroBloom Tech",
        "Surveillance renforcée des paramètres de croissance algale requise",
        "Tendances défavorables détectées sur plusieurs indicateurs clés",
      ],
      estimated_algae_index: 4.4,
      last_updated: "2026-06-20",
      facility_count: 7,
    },
    {
      id: "ENT-006",
      name: "Chlorella Energy GmbH",
      country: "Allemagne",
      sector: "Énergie Renouvelable",
      composite_score: 26.9,
      productivity_score: 30.0,
      sustainability_score: 28.0,
      scalability_score: 26.0,
      efficiency_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "systeme_algal_stable",
      key_signals: [
        "Risque modéré pour Chlorella Energy GmbH — suivi régulier recommandé",
        "Performance algale acceptable avec marges d'amélioration identifiées",
        "Optimisation progressive des processus de bioénergie en cours",
      ],
      estimated_algae_index: 2.69,
      last_updated: "2026-06-20",
      facility_count: 2,
    },
    {
      id: "ENT-007",
      name: "AquaGreen Labs",
      country: "Pays-Bas",
      sector: "Recherche Appliquée",
      composite_score: 13.0,
      productivity_score: 15.0,
      sustainability_score: 14.0,
      scalability_score: 12.0,
      efficiency_score: 10.0,
      risk_level: "faible",
      primary_pattern: "systeme_algal_stable",
      key_signals: [
        "AquaGreen Labs affiche une performance algale satisfaisante",
        "Indicateurs de production et durabilité dans les normes",
        "Système algal opérationnel — veille technologique maintenue",
      ],
      estimated_algae_index: 1.3,
      last_updated: "2026-06-20",
      facility_count: 1,
    },
    {
      id: "ENT-008",
      name: "BlueTide Bioenergy",
      country: "Danemark",
      sector: "Énergie Côtière",
      composite_score: 6.85,
      productivity_score: 8.0,
      sustainability_score: 7.0,
      scalability_score: 6.0,
      efficiency_score: 6.0,
      risk_level: "faible",
      primary_pattern: "systeme_algal_stable",
      key_signals: [
        "BlueTide Bioenergy affiche une performance algale satisfaisante",
        "Indicateurs de production et durabilité dans les normes",
        "Système algal opérationnel — veille technologique maintenue",
      ],
      estimated_algae_index: 0.69,
      last_updated: "2026-06-20",
      facility_count: 1,
    },
  ];

  const avgComposite = Math.round(
    (entities.reduce((sum, e) => sum + e.composite_score, 0) / entities.length) * 100,
  ) / 100;

  return {
    total_entities: 8,
    avg_composite: avgComposite,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      rendement_critique: 1,
      durabilite_compromise: 1,
      echelle_bloquee: 1,
      efficience_degradee: 0,
      systeme_algal_stable: 5,
    },
    top_risk_entities: ["SolarAlgae Industries", "BioPetro Algae", "AlgaFuel Nordic"],
    critical_alerts: [
      "SolarAlgae Industries: rendement critique",
      "BioPetro Algae: durabilité compromise",
      "AlgaFuel Nordic: échelle bloquée",
    ],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "algae",
    confidence_score: 0.85,
    data_sources: ["bioreactor_sensors", "carbon_capture_data", "biomass_yield_reports"],
    entities,
    avg_estimated_algae_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
  };
}
