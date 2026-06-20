import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[ai-alignment-risk-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "AI Alignment Risk Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/ai-alignment-risk-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "AI Alignment Risk Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "AI Alignment Risk Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "AR-001", name: "Chine — Course IA Totale", country: "Asie", sector: "Domination IA Militaire & Civile", composite_score: 90.75, arms_race_acceleration_score: 95.0, alignment_research_deficit_score: 85.0, governance_lag_score: 92.0, catastrophic_deployment_risk_score: 88.0, risk_level: "critique", primary_pattern: "course_catastrophique", key_signals: ["Course IA catastrophique dans Chine — puissance IA sans garantie d'alignement", "Pression compétitive sacrifiant la sécurité à la vitesse de déploiement", "Gouvernance IA en retard critique sur la puissance des systèmes déployés"], estimated_alignment_risk_index: 9.08, last_updated: "2026-06-20" },
    { entity_id: "AR-002", name: "Espace IA Global (OpenAI/Anthropic/Google)", country: "Cyberespace", sector: "Compétition Privée Accélérée", composite_score: 80.35, arms_race_acceleration_score: 85.0, alignment_research_deficit_score: 72.0, governance_lag_score: 80.0, catastrophic_deployment_risk_score: 78.0, risk_level: "critique", primary_pattern: "course_catastrophique", key_signals: ["Course IA catastrophique dans Espace IA Global — puissance IA sans garantie d'alignement", "Pression compétitive sacrifiant la sécurité à la vitesse de déploiement", "Gouvernance IA en retard critique sur la puissance des systèmes déployés"], estimated_alignment_risk_index: 8.04, last_updated: "2026-06-20" },
    { entity_id: "AR-003", name: "Russie — IA Militaire", country: "Europe de l'Est", sector: "Armement IA Autonome", composite_score: 81.75, arms_race_acceleration_score: 82.0, alignment_research_deficit_score: 80.0, governance_lag_score: 85.0, catastrophic_deployment_risk_score: 75.0, risk_level: "critique", primary_pattern: "course_catastrophique", key_signals: ["Course IA catastrophique dans Russie — puissance IA sans garantie d'alignement", "Pression compétitive sacrifiant la sécurité à la vitesse de déploiement", "Gouvernance IA en retard critique sur la puissance des systèmes déployés"], estimated_alignment_risk_index: 8.18, last_updated: "2026-06-20" },
    { entity_id: "AR-004", name: "USA — Silicon Valley Race", country: "Amérique du Nord", sector: "Course Privée vs Réglementation", composite_score: 74.35, arms_race_acceleration_score: 78.0, alignment_research_deficit_score: 65.0, governance_lag_score: 75.0, catastrophic_deployment_risk_score: 72.0, risk_level: "critique", primary_pattern: "desalignement_systemique", key_signals: ["Course IA catastrophique dans USA — puissance IA sans garantie d'alignement", "Pression compétitive sacrifiant la sécurité à la vitesse de déploiement", "Gouvernance IA en retard critique sur la puissance des systèmes déployés"], estimated_alignment_risk_index: 7.44, last_updated: "2026-06-20" },
    { entity_id: "AR-005", name: "Golfe & MENA — IA Achetée", country: "MENA", sector: "Déploiement sans Expertise Alignement", composite_score: 61.35, arms_race_acceleration_score: 60.0, alignment_research_deficit_score: 68.0, governance_lag_score: 62.0, catastrophic_deployment_risk_score: 55.0, risk_level: "critique", primary_pattern: "desalignement_systemique", key_signals: ["Course IA catastrophique dans Golfe & MENA — puissance IA sans garantie d'alignement", "Pression compétitive sacrifiant la sécurité à la vitesse de déploiement", "Gouvernance IA en retard critique sur la puissance des systèmes déployés"], estimated_alignment_risk_index: 6.14, last_updated: "2026-06-20" },
    { entity_id: "AR-006", name: "Europe — DSA & AI Act", country: "Europe", sector: "Régulation mais Pression Compétitive", composite_score: 39.35, arms_race_acceleration_score: 40.0, alignment_research_deficit_score: 38.0, governance_lag_score: 42.0, catastrophic_deployment_risk_score: 35.0, risk_level: "modéré", primary_pattern: "vigilance_requise", key_signals: ["Vigilance requise dans Europe — dynamiques de course partielles détectées", "Standards de sécurité IA en développement mais encore insuffisants", "Coopération internationale sur l'alignement nécessaire et en construction"], estimated_alignment_risk_index: 3.94, last_updated: "2026-06-20" },
    { entity_id: "AR-007", name: "UK — Frontier AI Safety", country: "Europe", sector: "Leadership Sécurité IA Partiel", composite_score: 26.5, arms_race_acceleration_score: 30.0, alignment_research_deficit_score: 22.0, governance_lag_score: 28.0, catastrophic_deployment_risk_score: 25.0, risk_level: "modéré", primary_pattern: "vigilance_requise", key_signals: ["Vigilance requise dans UK — dynamiques de course partielles détectées", "Standards de sécurité IA en développement mais encore insuffisants", "Coopération internationale sur l'alignement nécessaire et en construction"], estimated_alignment_risk_index: 2.65, last_updated: "2026-06-20" },
    { entity_id: "AR-008", name: "Instituts de Recherche (Anthropic/DeepMind)", country: "Global", sector: "Précaution Exemplaire & Safety First", composite_score: 12.7, arms_race_acceleration_score: 15.0, alignment_research_deficit_score: 8.0, governance_lag_score: 18.0, catastrophic_deployment_risk_score: 10.0, risk_level: "faible", primary_pattern: "precaution_exemplaire", key_signals: ["Instituts de Recherche maintient une précaution exemplaire sur l'alignement IA", "Investissements en recherche sur la sécurité IA proportionnels à la puissance développée", "Leadership mondial sur les normes d'alignement et de gouvernance IA"], estimated_alignment_risk_index: 1.27, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 0, "modéré": 2, faible: 1 },
    pattern_distribution: { course_catastrophique: 3, desalignement_systemique: 2, risque_emergeant: 0, vigilance_requise: 2, precaution_exemplaire: 1 },
    top_risk_entities: ["Chine — Course IA Totale", "Russie — IA Militaire", "Espace IA Global (OpenAI/Anthropic/Google)"],
    critical_alerts: ["Chine: course catastrophique", "Russie: course catastrophique", "Espace IA Global: course catastrophique", "USA: désalignement systémique", "Golfe & MENA: désalignement systémique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "ai_alignment",
    confidence_score: 0.73,
    data_sources: ["ai_safety_research_index", "frontier_ai_tracker", "arms_race_monitor"],
    entities,
    avg_estimated_alignment_risk_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
