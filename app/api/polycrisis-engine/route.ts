import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[polycrisis-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Polycrisis Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/polycrisis-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Polycrisis Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Polycrisis Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "PC-001", name: "Système Méditerranéen", country: "Europe/Afrique du Nord", sector: "Géopolitique Régionale", composite_score: 82.3, crisis_density_score: 88.0, cascade_velocity_score: 82.0, institutional_resilience_gap_score: 78.0, global_contagion_score: 76.0, risk_level: "critique", primary_pattern: "cascade_systemique", key_signals: ["Polycrise critique — confluence systémique détectée", "Vitesse de cascade au-delà des seuils maximaux", "Effondrement potentiel des mécanismes de résilience"], estimated_polycrisis_index: 8.23, last_updated: "2026-06-20" },
    { id: "PC-002", name: "Asie du Sud-Est", country: "Asie-Pacifique", sector: "Stabilité Régionale", composite_score: 75.05, crisis_density_score: 82.0, cascade_velocity_score: 75.0, institutional_resilience_gap_score: 72.0, global_contagion_score: 68.0, risk_level: "critique", primary_pattern: "cascade_systemique", key_signals: ["Polycrise critique — confluence systémique détectée", "Vecteurs de crise convergents identifiés", "Contagion globale en trajectoire dégradée"], estimated_polycrisis_index: 7.51, last_updated: "2026-06-20" },
    { id: "PC-003", name: "Sahel Sub-Saharien", country: "Afrique", sector: "Développement & Sécurité", composite_score: 75.8, crisis_density_score: 79.0, cascade_velocity_score: 71.0, institutional_resilience_gap_score: 85.0, global_contagion_score: 64.0, risk_level: "critique", primary_pattern: "amplification_reciproque", key_signals: ["Polycrise critique — effets d'amplification réciproque", "Déficit institutionnel aggravant les crises sécuritaires", "Boucles de rétroaction entre crise climatique et conflits"], estimated_polycrisis_index: 7.58, last_updated: "2026-06-20" },
    { id: "PC-004", name: "Arctique Circumpolaire", country: "Polaire", sector: "Gouvernance Climatique", composite_score: 53.25, crisis_density_score: 58.0, cascade_velocity_score: 55.0, institutional_resilience_gap_score: 48.0, global_contagion_score: 52.0, risk_level: "élevé", primary_pattern: "tipping_point_regional", key_signals: ["Risque polycrise élevé — tipping points climatiques", "Convergence de crises régionales identifiée", "Contagion systémique en progression"], estimated_polycrisis_index: 5.33, last_updated: "2026-06-20" },
    { id: "PC-005", name: "Bassin Amazonien", country: "Amérique du Sud", sector: "Biodiversité & Climat", composite_score: 48.0, crisis_density_score: 52.0, cascade_velocity_score: 48.0, institutional_resilience_gap_score: 44.0, global_contagion_score: 46.0, risk_level: "élevé", primary_pattern: "stress_test_systemique", key_signals: ["Risque élevé — pression polycrisis croissante", "Stress systémique sur plusieurs dimensions", "Indicateurs de résilience sous pression"], estimated_polycrisis_index: 4.80, last_updated: "2026-06-20" },
    { id: "PC-006", name: "Europe Centrale-Est", country: "Europe", sector: "Sécurité Énergétique", composite_score: 29.5, crisis_density_score: 32.0, cascade_velocity_score: 28.0, institutional_resilience_gap_score: 30.0, global_contagion_score: 26.0, risk_level: "modéré", primary_pattern: "stress_test_systemique", key_signals: ["Risque modéré — tensions géopolitiques persistantes", "Stress énergétique gérable avec interventions ciblées", "Résilience maintenue sous surveillance"], estimated_polycrisis_index: 2.95, last_updated: "2026-06-20" },
    { id: "PC-007", name: "Océanie Insulaire", country: "Pacifique", sector: "Adaptation Climatique", composite_score: 15.0, crisis_density_score: 18.0, cascade_velocity_score: 14.0, institutional_resilience_gap_score: 12.0, global_contagion_score: 16.0, risk_level: "faible", primary_pattern: "resilience_maintenue", key_signals: ["Résilience maintenue face aux défis climatiques", "Systèmes d'adaptation fonctionnels", "Surveillance polycrise — pas d'action urgente"], estimated_polycrisis_index: 1.50, last_updated: "2026-06-20" },
    { id: "PC-008", name: "Scandinavie", country: "Europe du Nord", sector: "Gouvernance Durable", composite_score: 8.5, crisis_density_score: 8.0, cascade_velocity_score: 10.0, institutional_resilience_gap_score: 6.0, global_contagion_score: 9.0, risk_level: "faible", primary_pattern: "resilience_maintenue", key_signals: ["Haute résilience systémique — modèle de référence", "Capacités d'absorption polycrisis exemplaires", "Veille maintenue — aucun indicateur préoccupant"], estimated_polycrisis_index: 0.85, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: { cascade_systemique: 2, amplification_reciproque: 1, tipping_point_regional: 1, stress_test_systemique: 2, resilience_maintenue: 2 },
    top_risk_entities: ["Système Méditerranéen", "Sahel Sub-Saharien", "Asie du Sud-Est"],
    critical_alerts: ["Système Méditerranéen: cascade systémique", "Sahel: amplification réciproque", "Asie du Sud-Est: cascade systémique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "polycrisis",
    confidence_score: 0.88,
    data_sources: ["resilience_index", "crisis_monitor_global", "systemic_risk_tracker"],
    entities,
    avg_estimated_polycrisis_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
