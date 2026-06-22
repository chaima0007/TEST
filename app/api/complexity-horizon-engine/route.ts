import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[complexity-horizon-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Complexity Horizon Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/complexity-horizon-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Complexity Horizon Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Complexity Horizon Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "CH-001", name: "Union Européenne — Bureaucratie Maximale", country: "Europe", sector: "Surréglementation Supranationale", composite_score: 84.0, regulatory_complexity_score: 90.0, institutional_coordination_failure_score: 85.0, policy_coherence_deficit_score: 82.0, adaptive_capacity_degradation_score: 78.0, risk_level: "critique", primary_pattern: "collapse_complexite", key_signals: ["Horizon de complexité dépassé pour Union Européenne — effondrement institutionnel imminent", "Surcharge réglementaire chronique — les systèmes ne peuvent plus s'auto-comprendre", "Paralysie décisionnelle avancée — adaptation impossible à la vitesse des chocs externes"], estimated_complexity_index: 8.40, last_updated: "2026-06-20" },
    { id: "CH-002", name: "États-Unis — Gridlock Fédéral", country: "Amérique du Nord", sector: "Polarisation & Paralysie Législative", composite_score: 83.5, regulatory_complexity_score: 85.0, institutional_coordination_failure_score: 88.0, policy_coherence_deficit_score: 80.0, adaptive_capacity_degradation_score: 75.0, risk_level: "critique", primary_pattern: "surcharge_systemique", key_signals: ["Horizon de complexité dépassé pour États-Unis — effondrement institutionnel imminent", "Surcharge réglementaire chronique — les systèmes ne peuvent plus s'auto-comprendre", "Paralysie décisionnelle avancée — adaptation impossible à la vitesse des chocs externes"], estimated_complexity_index: 8.35, last_updated: "2026-06-20" },
    { id: "CH-003", name: "Chine — Complexité Autoritaire", country: "Asie", sector: "Bureaucratie Planifiée & Contrôle Total", composite_score: 79.25, regulatory_complexity_score: 82.0, institutional_coordination_failure_score: 78.0, policy_coherence_deficit_score: 75.0, adaptive_capacity_degradation_score: 80.0, risk_level: "critique", primary_pattern: "surcharge_systemique", key_signals: ["Horizon de complexité dépassé pour Chine — effondrement institutionnel imminent", "Surcharge réglementaire chronique — les systèmes ne peuvent plus s'auto-comprendre", "Paralysie décisionnelle avancée — adaptation impossible à la vitesse des chocs externes"], estimated_complexity_index: 7.93, last_updated: "2026-06-20" },
    { id: "CH-004", name: "Inde — Complexité Démocratique", country: "Asie du Sud", sector: "États Fédéraux & Diversité Réglementaire", composite_score: 73.5, regulatory_complexity_score: 78.0, institutional_coordination_failure_score: 72.0, policy_coherence_deficit_score: 68.0, adaptive_capacity_degradation_score: 70.0, risk_level: "critique", primary_pattern: "surcharge_systemique", key_signals: ["Horizon de complexité dépassé pour Inde — effondrement institutionnel imminent", "Surcharge réglementaire chronique — les systèmes ne peuvent plus s'auto-comprendre", "Paralysie décisionnelle avancée — adaptation impossible à la vitesse des chocs externes"], estimated_complexity_index: 7.35, last_updated: "2026-06-20" },
    { id: "CH-005", name: "Brésil — Complexité Tropicale", country: "Amériques", sector: "Fiscalité & Réglementation Extrêmes", composite_score: 70.25, regulatory_complexity_score: 72.0, institutional_coordination_failure_score: 68.0, policy_coherence_deficit_score: 75.0, adaptive_capacity_degradation_score: 65.0, risk_level: "critique", primary_pattern: "surcharge_systemique", key_signals: ["Horizon de complexité dépassé pour Brésil — effondrement institutionnel imminent", "Surcharge réglementaire chronique — les systèmes ne peuvent plus s'auto-comprendre", "Paralysie décisionnelle avancée — adaptation impossible à la vitesse des chocs externes"], estimated_complexity_index: 7.03, last_updated: "2026-06-20" },
    { id: "CH-006", name: "Japon — Sclérose Administrative", country: "Asie du Nord-Est", sector: "Bureaucratie Consensuelle & Lenteur", composite_score: 50.75, regulatory_complexity_score: 55.0, institutional_coordination_failure_score: 52.0, policy_coherence_deficit_score: 58.0, adaptive_capacity_degradation_score: 48.0, risk_level: "élevé", primary_pattern: "horizon_complexite", key_signals: ["Surcharge systémique élevée dans Japon — incohérence politique chronique détectée", "Coordination institutionnelle défaillante — silos bureaucratiques non communicants", "Capacité adaptative en dégradation — réponse aux crises de plus en plus lente"], estimated_complexity_index: 5.08, last_updated: "2026-06-20" },
    { id: "CH-007", name: "Allemagne — Rigidité Systémique", country: "Europe", sector: "Précision Réglementaire & Inertie", composite_score: 33.0, regulatory_complexity_score: 35.0, institutional_coordination_failure_score: 30.0, policy_coherence_deficit_score: 38.0, adaptive_capacity_degradation_score: 28.0, risk_level: "modéré", primary_pattern: "tension_gouvernance", key_signals: ["Tension de gouvernance modérée dans Allemagne — complexité croissante mais maîtrisable", "Signaux d'accumulation réglementaire à surveiller — risque de seuil critique", "Réformes simplificatrices nécessaires pour préserver la capacité d'adaptation"], estimated_complexity_index: 3.30, last_updated: "2026-06-20" },
    { id: "CH-008", name: "Singapour & Nouvelles-Zélande", country: "Asie/Pacifique", sector: "Gouvernance Adaptative Exemplaire", composite_score: 9.0, regulatory_complexity_score: 10.0, institutional_coordination_failure_score: 8.0, policy_coherence_deficit_score: 12.0, adaptive_capacity_degradation_score: 6.0, risk_level: "faible", primary_pattern: "resilience_institutionnelle", key_signals: ["Singapour & Nouvelles-Zélande maintient une résilience institutionnelle solide — complexité sous contrôle", "Systèmes d'adaptation opérationnels et cohérence politique préservée", "Modèle de gouvernance adaptative à étudier et diffuser"], estimated_complexity_index: 0.90, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 1, "modéré": 1, faible: 1 },
    pattern_distribution: { collapse_complexite: 1, surcharge_systemique: 4, horizon_complexite: 1, tension_gouvernance: 1, resilience_institutionnelle: 1 },
    top_risk_entities: ["Union Européenne — Bureaucratie Maximale", "États-Unis — Gridlock Fédéral", "Chine — Complexité Autoritaire"],
    critical_alerts: ["UE: collapse complexité", "États-Unis: surcharge systémique", "Chine: surcharge systémique", "Inde: surcharge systémique", "Brésil: surcharge systémique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "complexity",
    confidence_score: 0.78,
    data_sources: ["world_bank_doing_business", "regulatory_complexity_index", "institutional_quality_monitor"],
    entities,
    avg_estimated_complexity_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
