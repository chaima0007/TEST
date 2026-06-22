import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[black-swan-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Black Swan Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/black-swan-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Black Swan Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Black Swan Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "BS-001", name: "Système Financier Global", country: "Mondial", sector: "Finance Systémique", composite_score: 83.45, tail_risk_score: 92.0, detectability_gap_score: 88.0, systemic_fragility_score: 82.0, cascade_amplification_score: 78.0, risk_level: "critique", primary_pattern: "cygne_noir_imminent", key_signals: ["Cygne noir potentiel — distribution de queue pathologique", "Risque catastrophique sous-estimé par les modèles standards", "Opacité systémique critique dans les marchés dérivés"], estimated_blackswan_index: 8.35, last_updated: "2026-06-20" },
    { id: "BS-002", name: "Internet & Infrastructures Numériques", country: "Mondial", sector: "Infrastructure Critique", composite_score: 78.25, tail_risk_score: 85.0, detectability_gap_score: 80.0, systemic_fragility_score: 75.0, cascade_amplification_score: 72.0, risk_level: "critique", primary_pattern: "cygne_noir_imminent", key_signals: ["Vulnérabilités critiques des protocoles fondamentaux", "Single points of failure dans l'infrastructure BGP", "Accumulation de dettes techniques non cartographiées"], estimated_blackswan_index: 7.83, last_updated: "2026-06-20" },
    { id: "BS-003", name: "Chaînes Alimentaires Mondiales", country: "Mondial", sector: "Sécurité Alimentaire", composite_score: 75.25, tail_risk_score: 78.0, detectability_gap_score: 72.0, systemic_fragility_score: 80.0, cascade_amplification_score: 68.0, risk_level: "critique", primary_pattern: "accumulation_risques_opaques", key_signals: ["Fragilités cachées dans les approvisionnements agricoles", "Dépendances opaques sur 3 cultures de base mondiales", "Risques combinés eau/sol/énergie non-modélisés"], estimated_blackswan_index: 7.53, last_updated: "2026-06-20" },
    { id: "BS-004", name: "Systèmes Géomagnétiques", country: "Planète", sector: "Risques Naturels", composite_score: 51.25, tail_risk_score: 55.0, detectability_gap_score: 50.0, systemic_fragility_score: 48.0, cascade_amplification_score: 52.0, risk_level: "élevé", primary_pattern: "signal_faible_critique", key_signals: ["Risque élevé — activité solaire en cycle 25 ascendant", "Fragilité des infrastructures électriques face aux EMP", "Signaux faibles dans les données magnétosphériques"], estimated_blackswan_index: 5.13, last_updated: "2026-06-20" },
    { id: "BS-005", name: "IA Transformative Unbounded", country: "Mondial", sector: "Technologie Extrême", composite_score: 52.85, tail_risk_score: 58.0, detectability_gap_score: 62.0, systemic_fragility_score: 45.0, cascade_amplification_score: 48.0, risk_level: "élevé", primary_pattern: "signal_faible_critique", key_signals: ["Risque élevé — capacités émergentes hors modèles de prévision", "Détectabilité faible des ruptures technologiques soudaines", "Absence de mécanismes de gouvernance adaptés aux scénarios extrêmes"], estimated_blackswan_index: 5.29, last_updated: "2026-06-20" },
    { id: "BS-006", name: "Pandémie Pathogène Inconnu", country: "Mondial", sector: "Santé Globale", composite_score: 29.25, tail_risk_score: 30.0, detectability_gap_score: 28.0, systemic_fragility_score: 32.0, cascade_amplification_score: 26.0, risk_level: "modéré", primary_pattern: "fragility_systemique", key_signals: ["Fragilités résiduelles post-COVID dans les systèmes de santé", "Zones sous-surveillance épidémiologique identifiées", "Capacités de réponse rapide encore en reconstruction"], estimated_blackswan_index: 2.93, last_updated: "2026-06-20" },
    { id: "BS-007", name: "Événements Géophysiques Majeurs", country: "Planète", sector: "Risques Naturels", composite_score: 14.25, tail_risk_score: 16.0, detectability_gap_score: 12.0, systemic_fragility_score: 14.0, cascade_amplification_score: 18.0, risk_level: "faible", primary_pattern: "vigilance_maintenue", key_signals: ["Profil de risque géophysique dans les normes historiques", "Surveillance volcanique et sismique opérationnelle", "Systèmes d'alerte précoce maintenus"], estimated_blackswan_index: 1.43, last_updated: "2026-06-20" },
    { id: "BS-008", name: "Institutions Multilatérales", country: "Mondial", sector: "Gouvernance Globale", composite_score: 8.5, tail_risk_score: 8.0, detectability_gap_score: 10.0, systemic_fragility_score: 6.0, cascade_amplification_score: 9.0, risk_level: "faible", primary_pattern: "vigilance_maintenue", key_signals: ["Résilience institutionnelle maintenue — coopération fonctionnelle", "Mécanismes de gouvernance globale opérationnels", "Veille cygne noir — aucun signal d'alerte critique"], estimated_blackswan_index: 0.85, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 3, "élevé": 2, "modéré": 1, faible: 2 },
    pattern_distribution: { cygne_noir_imminent: 2, accumulation_risques_opaques: 1, fragility_systemique: 1, signal_faible_critique: 2, vigilance_maintenue: 2 },
    top_risk_entities: ["Système Financier Global", "Internet & Infrastructures Numériques", "Chaînes Alimentaires Mondiales"],
    critical_alerts: ["Système Financier: cygne noir imminent", "Internet: vulnérabilités systémiques critiques", "Alimentation mondiale: accumulation risques opaques"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "blackswan",
    confidence_score: 0.72,
    data_sources: ["tail_risk_models", "systemic_fragility_index", "black_swan_observatory"],
    entities,
    avg_estimated_blackswan_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
