import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[social-media-mental-health-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Social Media Mental Health Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/social-media-mental-health-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Social Media Mental Health Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Social Media Mental Health Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    {
      id: "MNH-001",
      name: "TikTok US Operations",
      country: "USA",
      sector: "Social Media",
      composite_score: 77.50,
      algorithmic_harm_amplification_score: 82.0,
      youth_vulnerability_exposure_score: 88.0,
      mental_disorder_correlation_score: 74.0,
      platform_accountability_deficit_score: 62.0,
      risk_level: "critique",
      primary_pattern: "youth_mental_crisis",
      key_signals: [
        "Algorithme de recommandation TikTok expose 85% des mineurs à des contenus d'anxiété en moins de 10 min",
        "Durée moyenne de session de 95 min/jour chez les adolescents corrélée à une hausse de 47% de dépression",
        "Fonctionnalité d'affichage du compteur de vues amplificatrice de comportements compulsifs chez les jeunes",
      ],
      estimated_mentalhealth_index: 7.75,
      last_updated: "2026-06-20",
      confidence_level: 0.91,
    },
    {
      id: "MNH-002",
      name: "Instagram Meta Platform",
      country: "USA",
      sector: "Social Media",
      composite_score: 70.55,
      algorithmic_harm_amplification_score: 78.0,
      youth_vulnerability_exposure_score: 65.0,
      mental_disorder_correlation_score: 66.0,
      platform_accountability_deficit_score: 72.0,
      risk_level: "critique",
      primary_pattern: "algorithmic_radicalization",
      key_signals: [
        "Filtre beauté Instagram renforce les troubles dysmorphiques corporels chez 62% des utilisatrices 13-17 ans",
        "Algorithme Explore amplifie les contenus pro-anorexie malgré les politiques de contenu déclarées",
        "Absence de limite de temps d'écran native entraîne une addiction documentée par 38 études cliniques",
      ],
      estimated_mentalhealth_index: 7.06,
      last_updated: "2026-06-20",
      confidence_level: 0.87,
    },
    {
      id: "MNH-003",
      name: "Twitter/X Platform",
      country: "USA",
      sector: "Social Media",
      composite_score: 63.20,
      algorithmic_harm_amplification_score: 60.0,
      youth_vulnerability_exposure_score: 58.0,
      mental_disorder_correlation_score: 62.0,
      platform_accountability_deficit_score: 76.0,
      risk_level: "critique",
      primary_pattern: "platform_negligence",
      key_signals: [
        "Suppression de 80% des équipes de modération corrélée à une explosion des contenus haineux et suicidaires",
        "Algorithme de trending amplifie le contenu polarisant multipliant l'exposition à la détresse émotionnelle",
        "Déficit critique de mécanismes de signalement pour contenus à risque suicidaire depuis la restructuration",
      ],
      estimated_mentalhealth_index: 6.32,
      last_updated: "2026-06-20",
      confidence_level: 0.83,
    },
    {
      id: "MNH-004",
      name: "WeChat International",
      country: "China",
      sector: "Social Media",
      composite_score: 54.55,
      algorithmic_harm_amplification_score: 48.0,
      youth_vulnerability_exposure_score: 55.0,
      mental_disorder_correlation_score: 72.0,
      platform_accountability_deficit_score: 42.0,
      risk_level: "élevé",
      primary_pattern: "depression_anxiety_nexus",
      key_signals: [
        "Intégration WeChat aux plateformes de jeu amplifie les comportements addictifs chez les utilisateurs isolés",
        "Corrélation de 0.71 entre usage intensif WeChat et symptômes dépressifs dans les études longitudinales",
        "Manque de transparence algorithmique empêche l'audit indépendant des impacts santé mentale",
      ],
      estimated_mentalhealth_index: 5.46,
      last_updated: "2026-06-20",
      confidence_level: 0.79,
    },
    {
      id: "MNH-005",
      name: "Snapchat EU Operations",
      country: "UK",
      sector: "Social Media",
      composite_score: 45.70,
      algorithmic_harm_amplification_score: 42.0,
      youth_vulnerability_exposure_score: 58.0,
      mental_disorder_correlation_score: 44.0,
      platform_accountability_deficit_score: 38.0,
      risk_level: "élevé",
      primary_pattern: "platform_responsible",
      key_signals: [
        "Snaps éphémères génèrent une anxiété de FOMO (Fear Of Missing Out) chez 54% des utilisateurs adolescents",
        "Streak feature entraîne des comportements compulsifs documentés chez les utilisateurs de 13 à 19 ans",
        "Exposition à des contenus de bullying via Snap Maps supérieure à la moyenne des plateformes équivalentes",
      ],
      estimated_mentalhealth_index: 4.57,
      last_updated: "2026-06-20",
      confidence_level: 0.76,
    },
    {
      id: "MNH-006",
      name: "LinkedIn DACH",
      country: "Germany",
      sector: "Professional Network",
      composite_score: 25.85,
      algorithmic_harm_amplification_score: 22.0,
      youth_vulnerability_exposure_score: 25.0,
      mental_disorder_correlation_score: 28.0,
      platform_accountability_deficit_score: 30.0,
      risk_level: "modéré",
      primary_pattern: "platform_responsible",
      key_signals: [
        "LinkedIn génère du stress de comparaison professionnelle modéré mais gérable selon les études de 2025",
        "Mécanismes de modération actifs limitent l'exposition aux contenus de détresse professionnelle",
        "Politiques de bien-être numérique conformes aux directives DSA avec audits trimestriels documentés",
      ],
      estimated_mentalhealth_index: 2.59,
      last_updated: "2026-06-20",
      confidence_level: 0.72,
    },
    {
      id: "MNH-007",
      name: "Discord Nordic",
      country: "Finland",
      sector: "Gaming/Social",
      composite_score: 11.35,
      algorithmic_harm_amplification_score: 10.0,
      youth_vulnerability_exposure_score: 12.0,
      mental_disorder_correlation_score: 15.0,
      platform_accountability_deficit_score: 8.0,
      risk_level: "faible",
      primary_pattern: "platform_responsible",
      key_signals: [
        "Discord Nordic met en oeuvre des outils de bien-être mental intégrés et des ressources d'aide en crise",
        "Communautés de soutien modérées activement réduisent l'isolement social et favorisent la résilience",
        "Faible corrélation entre usage Discord et symptômes dépressifs grâce aux protocoles de protection",
      ],
      estimated_mentalhealth_index: 1.14,
      last_updated: "2026-06-20",
      confidence_level: 0.68,
    },
    {
      id: "MNH-008",
      name: "Pinterest Benelux",
      country: "Netherlands",
      sector: "Creative Platform",
      composite_score: 7.20,
      algorithmic_harm_amplification_score: 5.0,
      youth_vulnerability_exposure_score: 8.0,
      mental_disorder_correlation_score: 10.0,
      platform_accountability_deficit_score: 6.0,
      risk_level: "faible",
      primary_pattern: "platform_responsible",
      key_signals: [
        "Pinterest Benelux présente des impacts positifs sur créativité et estime de soi dans 73% des études",
        "Algorithme orienté inspiration plutôt qu'engagement compulsif réduit les risques de dépendance",
        "Initiatives bien-être numérique proactives incluant des limites de temps et filtres de contenu robustes",
      ],
      estimated_mentalhealth_index: 0.72,
      last_updated: "2026-06-20",
      confidence_level: 0.65,
    },
  ];

  const n = entities.length;
  const avgComposite = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / n * 100) / 100;
  const avgConfidence = Math.round(entities.reduce((s, e) => s + e.confidence_level, 0) / n * 100) / 100;

  const riskDistribution: Record<string, number> = { critique: 0, "élevé": 0, "modéré": 0, faible: 0 };
  const patternDistribution: Record<string, number> = {
    algorithmic_radicalization: 0,
    youth_mental_crisis: 0,
    depression_anxiety_nexus: 0,
    platform_negligence: 0,
    platform_responsible: 0,
  };
  for (const e of entities) {
    riskDistribution[e.risk_level] = (riskDistribution[e.risk_level] || 0) + 1;
    patternDistribution[e.primary_pattern] = (patternDistribution[e.primary_pattern] || 0) + 1;
  }

  const topRiskEntities = [...entities]
    .sort((a, b) => b.composite_score - a.composite_score)
    .slice(0, 3)
    .map(e => e.name);

  const criticalAlerts = entities.filter(e => e.risk_level === "critique").map(e => e.name);

  const summary = {
    total_entities: n,
    avg_composite: avgComposite,
    risk_distribution: riskDistribution,
    pattern_distribution: patternDistribution,
    top_risk_entities: topRiskEntities,
    critical_alerts: criticalAlerts,
    last_analysis: "2026-06-20T00:00:00Z",
    engine_version: "1.0.0",
    domain: "mentalhealth",
    confidence_score: avgConfidence,
    data_sources: [
      "WHO Mental Health Reports",
      "American Psychological Association",
      "EU Digital Services Act Reports",
    ],
    entities,
    avg_estimated_mentalhealth_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
  };

  return summary;
}
