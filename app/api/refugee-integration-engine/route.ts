import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[refugee-integration-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Refugee Integration Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/refugee-integration-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Refugee Integration Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Refugee Integration Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    {
      id: "REF-001",
      name: "Programme d'Accueil Berlin",
      country: "Syria",
      sector: "Germany",
      composite_score: 69.45,
      social_integration_barrier_score: 82.0,
      economic_exclusion_score: 65.0,
      legal_vulnerability_score: 60.0,
      mental_health_crisis_score: 68.0,
      risk_level: "critique",
      primary_pattern: "integration_failure",
      key_signals: [
        "Isolement linguistique et culturel sévère détecté",
        "Accès limité aux services d'intégration communautaire",
        "Discrimination systémique sur le marché du logement",
      ],
      estimated_refugee_index: 6.95,
      last_updated: "2026-06-20",
      confidence_level: 0.83,
    },
    {
      id: "REF-002",
      name: "Centre d'Intégration Paris",
      country: "Afghanistan",
      sector: "France",
      composite_score: 66.40,
      social_integration_barrier_score: 65.0,
      economic_exclusion_score: 60.0,
      legal_vulnerability_score: 78.0,
      mental_health_crisis_score: 62.0,
      risk_level: "critique",
      primary_pattern: "legal_precarity",
      key_signals: [
        "Statut juridique précaire et procédures d'asile bloquées",
        "Risque élevé d'expulsion et absence de protection temporaire",
        "Accès restreint aux droits sociaux fondamentaux",
      ],
      estimated_refugee_index: 6.64,
      last_updated: "2026-06-20",
      confidence_level: 0.79,
    },
    {
      id: "REF-003",
      name: "Foyer d'Accueil Bruxelles",
      country: "Sudan",
      sector: "Belgium",
      composite_score: 61.25,
      social_integration_barrier_score: 60.0,
      economic_exclusion_score: 55.0,
      legal_vulnerability_score: 58.0,
      mental_health_crisis_score: 75.0,
      risk_level: "critique",
      primary_pattern: "mental_health_crisis",
      key_signals: [
        "Traumatismes post-conflictuels non traités et détresse sévère",
        "Absence de soutien psychologique spécialisé disponible",
        "Rupture des liens familiaux et isolement social profond",
      ],
      estimated_refugee_index: 6.13,
      last_updated: "2026-06-20",
      confidence_level: 0.85,
    },
    {
      id: "REF-004",
      name: "Centre Varsovie",
      country: "Ukraine",
      sector: "Poland",
      composite_score: 51.75,
      social_integration_barrier_score: 55.0,
      economic_exclusion_score: 72.0,
      legal_vulnerability_score: 45.0,
      mental_health_crisis_score: 30.0,
      risk_level: "élevé",
      primary_pattern: "economic_exclusion",
      key_signals: [
        "Exclusion du marché du travail malgré qualifications reconnues",
        "Barrières linguistiques bloquant l'insertion professionnelle",
        "Dépendance aux aides sociales faute d'accès à l'emploi",
      ],
      estimated_refugee_index: 5.18,
      last_updated: "2026-06-20",
      confidence_level: 0.81,
    },
    {
      id: "REF-005",
      name: "Programme Rome",
      country: "Ethiopia",
      sector: "Italy",
      composite_score: 48.40,
      social_integration_barrier_score: 78.0,
      economic_exclusion_score: 42.0,
      legal_vulnerability_score: 38.0,
      mental_health_crisis_score: 25.0,
      risk_level: "élevé",
      primary_pattern: "integration_failure",
      key_signals: [
        "Fragmentation communautaire et absence de réseaux de soutien",
        "Difficultés majeures d'accès aux services locaux d'intégration",
        "Rejet social et marginalisation dans les quartiers d'accueil",
      ],
      estimated_refugee_index: 4.84,
      last_updated: "2026-06-20",
      confidence_level: 0.77,
    },
    {
      id: "REF-006",
      name: "Accueil Madrid",
      country: "Venezuela",
      sector: "Spain",
      composite_score: 29.40,
      social_integration_barrier_score: 35.0,
      economic_exclusion_score: 30.0,
      legal_vulnerability_score: 28.0,
      mental_health_crisis_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "successful_integration",
      key_signals: [
        "Intégration partielle avec quelques obstacles résiduels",
        "Accès aux services de base en cours de consolidation",
        "Liens communautaires en développement progressif",
      ],
      estimated_refugee_index: 2.94,
      last_updated: "2026-06-20",
      confidence_level: 0.88,
    },
    {
      id: "REF-007",
      name: "Centre Amsterdam",
      country: "Colombia",
      sector: "Netherlands",
      composite_score: 14.80,
      social_integration_barrier_score: 15.0,
      economic_exclusion_score: 12.0,
      legal_vulnerability_score: 18.0,
      mental_health_crisis_score: 14.0,
      risk_level: "faible",
      primary_pattern: "successful_integration",
      key_signals: [
        "Intégration socio-économique réussie et autonomie établie",
        "Statut légal sécurisé et accès complet aux droits sociaux",
        "Réseau communautaire solide et participation civique active",
      ],
      estimated_refugee_index: 1.48,
      last_updated: "2026-06-20",
      confidence_level: 0.91,
    },
    {
      id: "REF-008",
      name: "Programme Genève",
      country: "Morocco",
      sector: "Switzerland",
      composite_score: 10.00,
      social_integration_barrier_score: 10.0,
      economic_exclusion_score: 8.0,
      legal_vulnerability_score: 12.0,
      mental_health_crisis_score: 10.0,
      risk_level: "faible",
      primary_pattern: "successful_integration",
      key_signals: [
        "Modèle d'intégration exemplaire à fort potentiel de réplication",
        "Insertion professionnelle complète avec progression de carrière",
        "Bien-être psychologique et cohésion sociale remarquables",
      ],
      estimated_refugee_index: 1.00,
      last_updated: "2026-06-20",
      confidence_level: 0.93,
    },
  ];

  return {
    total_entities: 8,
    avg_composite: 43.93,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: {
      integration_failure: 2,
      economic_exclusion: 1,
      legal_precarity: 1,
      mental_health_crisis: 1,
      successful_integration: 3,
    },
    top_risk_entities: [
      "Programme d'Accueil Berlin",
      "Centre d'Intégration Paris",
      "Foyer d'Accueil Bruxelles",
    ],
    critical_alerts: [
      "Programme d'Accueil Berlin",
      "Centre d'Intégration Paris",
      "Foyer d'Accueil Bruxelles",
    ],
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "refugee",
    confidence_score: 0.85,
    data_sources: [
      "UNHCR Integration Reports",
      "EU Asylum Statistics",
      "IOM Migration Data",
    ],
    entities,
    avg_estimated_refugee_index: 4.39,
  };
}
