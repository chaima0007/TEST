import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[caelum-synthesis-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Caelum Synthesis Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/caelum-synthesis-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Caelum Synthesis Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Caelum Synthesis Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "SYN-001", name: "Proche-Orient & Golfe", country: "MENA", sector: "Géopolitique & Énergie", composite_score: 79.45, environmental_risk_score: 82.0, geopolitical_risk_score: 90.0, socioeconomic_risk_score: 78.0, technology_disruption_score: 65.0, risk_level: "critique", primary_pattern: "convergence_civilisationnelle", key_signals: ["Convergence critique multi-domaines détectée pour Proche-Orient & Golfe", "Interactions amplificatrices entre risques environnementaux et géopolitiques", "Score de synthèse Caelum au niveau d'alerte maximale"], estimated_synthesis_index: 7.95, last_updated: "2026-06-20" },
    { id: "SYN-002", name: "Asie du Sud (Arc de Crise)", country: "Asie du Sud", sector: "Sécurité Régionale", composite_score: 77.7, environmental_risk_score: 76.0, geopolitical_risk_score: 85.0, socioeconomic_risk_score: 80.0, technology_disruption_score: 68.0, risk_level: "critique", primary_pattern: "convergence_civilisationnelle", key_signals: ["Convergence critique multi-domaines détectée pour Asie du Sud", "Interactions amplificatrices entre risques environnementaux et géopolitiques", "Score de synthèse Caelum au niveau d'alerte maximale"], estimated_synthesis_index: 7.77, last_updated: "2026-06-20" },
    { id: "SYN-003", name: "Afrique Sub-Saharienne", country: "Afrique", sector: "Développement Humain", composite_score: 75.25, environmental_risk_score: 80.0, geopolitical_risk_score: 72.0, socioeconomic_risk_score: 85.0, technology_disruption_score: 60.0, risk_level: "critique", primary_pattern: "convergence_civilisationnelle", key_signals: ["Convergence critique multi-domaines détectée pour Afrique Sub-Saharienne", "Interactions amplificatrices entre risques environnementaux et géopolitiques", "Score de synthèse Caelum au niveau d'alerte maximale"], estimated_synthesis_index: 7.53, last_updated: "2026-06-20" },
    { id: "SYN-004", name: "Amérique Latine", country: "Amériques", sector: "Stabilité Socioéconomique", composite_score: 62.65, environmental_risk_score: 65.0, geopolitical_risk_score: 58.0, socioeconomic_risk_score: 72.0, technology_disruption_score: 52.0, risk_level: "critique", primary_pattern: "stress_test_global", key_signals: ["Stress transsectoriel élevé identifié pour Amérique Latine", "Plusieurs vecteurs de risque en trajectoire convergente", "Surveillance renforcée recommandée par le moteur Caelum"], estimated_synthesis_index: 6.27, last_updated: "2026-06-20" },
    { id: "SYN-005", name: "Eurasie Centrale", country: "Eurasie", sector: "Ressources & Transit", composite_score: 65.85, environmental_risk_score: 68.0, geopolitical_risk_score: 75.0, socioeconomic_risk_score: 55.0, technology_disruption_score: 48.0, risk_level: "critique", primary_pattern: "amplification_transsectorielle", key_signals: ["Convergence critique multi-domaines détectée pour Eurasie Centrale", "Interactions amplificatrices entre risques environnementaux et géopolitiques", "Score de synthèse Caelum au niveau d'alerte maximale"], estimated_synthesis_index: 6.59, last_updated: "2026-06-20" },
    { id: "SYN-006", name: "Europe Occidentale", country: "Europe", sector: "Démocratie & Sécurité", composite_score: 38.75, environmental_risk_score: 42.0, geopolitical_risk_score: 38.0, socioeconomic_risk_score: 35.0, technology_disruption_score: 40.0, risk_level: "modéré", primary_pattern: "vigilance_transversale", key_signals: ["Tension systémique modérée pour Europe Occidentale — veille active conseillée", "Indicateurs inter-domaines à surveiller", "Pas de convergence critique — gestion préventive suffisante"], estimated_synthesis_index: 3.88, last_updated: "2026-06-20" },
    { id: "SYN-007", name: "Amérique du Nord", country: "Amériques", sector: "Stabilité Démocratique", composite_score: 33.6, environmental_risk_score: 35.0, geopolitical_risk_score: 32.0, socioeconomic_risk_score: 30.0, technology_disruption_score: 38.0, risk_level: "modéré", primary_pattern: "vigilance_transversale", key_signals: ["Tension systémique modérée pour Amérique du Nord — veille active conseillée", "Indicateurs inter-domaines à surveiller", "Pas de convergence critique — gestion préventive suffisante"], estimated_synthesis_index: 3.36, last_updated: "2026-06-20" },
    { id: "SYN-008", name: "Asie-Pacifique Développée", country: "Asie-Pacifique", sector: "Économies Avancées", composite_score: 18.65, environmental_risk_score: 20.0, geopolitical_risk_score: 18.0, socioeconomic_risk_score: 15.0, technology_disruption_score: 22.0, risk_level: "faible", primary_pattern: "stabilite_systemique", key_signals: ["Asie-Pacifique Développée affiche une stabilité systémique confirmée", "Tous les indicateurs Caelum dans les zones vertes", "Rapport de synthèse : environnement favorable"], estimated_synthesis_index: 1.87, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 0, "modéré": 2, faible: 1 },
    pattern_distribution: { convergence_civilisationnelle: 3, amplification_transsectorielle: 1, stress_test_global: 1, vigilance_transversale: 2, stabilite_systemique: 1 },
    top_risk_entities: ["Proche-Orient & Golfe", "Asie du Sud (Arc de Crise)", "Afrique Sub-Saharienne"],
    critical_alerts: ["Proche-Orient & Golfe: convergence civilisationnelle", "Asie du Sud: convergence civilisationnelle", "Afrique Sub-Saharienne: convergence civilisationnelle"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "synthesis",
    confidence_score: 0.91,
    data_sources: ["all_caelum_engines", "global_risk_aggregator", "synthesis_model_v1"],
    entities,
    avg_estimated_synthesis_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
