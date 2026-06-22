import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[quantum-economic-disruption-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Quantum Economic Disruption Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/quantum-economic-disruption-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Quantum Economic Disruption Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Quantum Economic Disruption Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    {
      id: "QED-001",
      name: "Federal Reserve Quantum Division",
      country: "USA",
      sector: "Finance",
      composite_score: 74.75,
      cryptographic_vulnerability_score: 85.0,
      economic_disruption_score: 70.0,
      quantum_readiness_gap_score: 75.0,
      geopolitical_exposure_score: 65.0,
      risk_level: "critique",
      primary_pattern: "cryptographic_collapse",
      key_signals: [
        "Algorithmes RSA-2048 exposés aux attaques quantiques",
        "Systèmes financiers sans protection post-quantique",
        "Délai de migration cryptographique insuffisant",
      ],
      estimated_quantum_index: 7.48,
      last_updated: "2026-06-20",
      confidence_level: 0.87,
    },
    {
      id: "QED-002",
      name: "Sinoquantum Technologies Group",
      country: "China",
      sector: "Technology",
      composite_score: 66.5,
      cryptographic_vulnerability_score: 60.0,
      economic_disruption_score: 65.0,
      quantum_readiness_gap_score: 65.0,
      geopolitical_exposure_score: 80.0,
      risk_level: "critique",
      primary_pattern: "geopolitical_quantum_race",
      key_signals: [
        "Programme quantique militaire sino-américain en escalade",
        "Investissements quantiques étatiques multipliés par 5",
        "Alliances technologiques quantiques remises en question",
      ],
      estimated_quantum_index: 6.65,
      last_updated: "2026-06-20",
      confidence_level: 0.82,
    },
    {
      id: "QED-003",
      name: "Rostec Quantum Defense Systems",
      country: "Russia",
      sector: "Defense",
      composite_score: 63.5,
      cryptographic_vulnerability_score: 65.0,
      economic_disruption_score: 72.0,
      quantum_readiness_gap_score: 60.0,
      geopolitical_exposure_score: 55.0,
      risk_level: "critique",
      primary_pattern: "economic_disruption_cascade",
      key_signals: [
        "Secteur défense exposé à la disruption économique quantique",
        "Infrastructure critique sans chiffrement post-quantique",
        "Capacités industrielles vulnérables aux avantages quantiques adverses",
      ],
      estimated_quantum_index: 6.35,
      last_updated: "2026-06-20",
      confidence_level: 0.79,
    },
    {
      id: "QED-004",
      name: "Bundesverband Industrie Quantique",
      country: "Germany",
      sector: "Manufacturing",
      composite_score: 53.35,
      cryptographic_vulnerability_score: 55.0,
      economic_disruption_score: 45.0,
      quantum_readiness_gap_score: 72.0,
      geopolitical_exposure_score: 38.0,
      risk_level: "élevé",
      primary_pattern: "quantum_readiness_gap",
      key_signals: [
        "Industrie manufacturière en retard sur l'adoption quantique",
        "Chaînes d'approvisionnement non préparées aux perturbations quantiques",
        "Déficit de compétences quantiques dans le secteur industriel",
      ],
      estimated_quantum_index: 5.34,
      last_updated: "2026-06-20",
      confidence_level: 0.84,
    },
    {
      id: "QED-005",
      name: "Tata Quantum Innovation Labs",
      country: "India",
      sector: "Technology",
      composite_score: 48.25,
      cryptographic_vulnerability_score: 45.0,
      economic_disruption_score: 40.0,
      quantum_readiness_gap_score: 75.0,
      geopolitical_exposure_score: 30.0,
      risk_level: "élevé",
      primary_pattern: "quantum_readiness_gap",
      key_signals: [
        "Écosystème technologique en transition quantique partielle",
        "Adoption quantique insuffisante face aux concurrents asiatiques",
        "Programmes de formation quantique en phase de démarrage",
      ],
      estimated_quantum_index: 4.83,
      last_updated: "2026-06-20",
      confidence_level: 0.76,
    },
    {
      id: "QED-006",
      name: "Banco do Brasil Quantum Initiative",
      country: "Brazil",
      sector: "Finance",
      composite_score: 29.75,
      cryptographic_vulnerability_score: 30.0,
      economic_disruption_score: 28.0,
      quantum_readiness_gap_score: 35.0,
      geopolitical_exposure_score: 25.0,
      risk_level: "modéré",
      primary_pattern: "quantum_stable",
      key_signals: [
        "Exposition modérée aux risques cryptographiques quantiques",
        "Marché financier brésilien en phase d'évaluation quantique",
        "Partenariats internationaux quantiques en cours de négociation",
      ],
      estimated_quantum_index: 2.98,
      last_updated: "2026-06-20",
      confidence_level: 0.71,
    },
    {
      id: "QED-007",
      name: "Canadian Quantum Computing Initiative",
      country: "Canada",
      sector: "Technology",
      composite_score: 13.75,
      cryptographic_vulnerability_score: 10.0,
      economic_disruption_score: 12.0,
      quantum_readiness_gap_score: 15.0,
      geopolitical_exposure_score: 20.0,
      risk_level: "faible",
      primary_pattern: "quantum_stable",
      key_signals: [
        "Système cryptographique partiellement mis à jour",
        "Investissements publics en informatique quantique en cours",
        "Cadre réglementaire quantique avancé et proactif",
      ],
      estimated_quantum_index: 1.38,
      last_updated: "2026-06-20",
      confidence_level: 0.90,
    },
    {
      id: "QED-008",
      name: "Swiss National Bank Quantum Lab",
      country: "Switzerland",
      sector: "Finance",
      composite_score: 9.3,
      cryptographic_vulnerability_score: 8.0,
      economic_disruption_score: 8.0,
      quantum_readiness_gap_score: 10.0,
      geopolitical_exposure_score: 12.0,
      risk_level: "faible",
      primary_pattern: "quantum_stable",
      key_signals: [
        "Infrastructure bancaire dotée de protections post-quantiques pilotes",
        "Recherche quantique académique de niveau mondial",
        "Stabilité géopolitique favorable à la coopération quantique",
      ],
      estimated_quantum_index: 0.93,
      last_updated: "2026-06-20",
      confidence_level: 0.93,
    },
  ];

  const avg_composite =
    Math.round(
      (entities.reduce((s, e) => s + e.composite_score, 0) / entities.length) * 100
    ) / 100;

  const avg_confidence =
    Math.round(
      (entities.reduce((s, e) => s + e.confidence_level, 0) / entities.length) * 100
    ) / 100;

  const summary = {
    total_entities: entities.length,
    avg_composite,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      cryptographic_collapse: 1,
      economic_disruption_cascade: 1,
      quantum_readiness_gap: 2,
      geopolitical_quantum_race: 1,
      quantum_stable: 3,
    },
    top_risk_entities: [
      "Federal Reserve Quantum Division",
      "Sinoquantum Technologies Group",
      "Rostec Quantum Defense Systems",
    ],
    critical_alerts: [
      "Federal Reserve Quantum Division",
      "Sinoquantum Technologies Group",
      "Rostec Quantum Defense Systems",
    ],
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "quantum",
    confidence_score: avg_confidence,
    data_sources: [
      "IMF Quantum Economic Reports",
      "NIST Post-Quantum Standards",
      "Quantum Computing Market Data",
    ],
    entities,
    avg_estimated_quantum_index: Math.round((avg_composite / 100) * 10 * 100) / 100,
  };

  return { entities, summary };
}
