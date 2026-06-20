import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sovereign-ai-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Sovereign AI Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sovereign-ai-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Sovereign AI Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Sovereign AI Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "SA-001", name: "Afrique Subsaharienne", country: "Afrique", sector: "Vassalité IA Totale", composite_score: 88.9, ai_dependency_exposure_score: 90.0, domestic_ai_capability_deficit_score: 88.0, ai_talent_gap_score: 85.0, compute_autonomy_deficit_score: 92.0, risk_level: "critique", primary_pattern: "vassalite_ia_totale", key_signals: ["Vassalité IA critique pour Afrique Subsaharienne — infrastructure IA sous contrôle technologique étranger", "Déficit de capacités IA domestiques — dépendance aux modèles et puces étrangers totale", "Risque géopolitique majeur — coupure IA possible en cas de tension diplomatique"], estimated_ai_sovereignty_index: 8.89, last_updated: "2026-06-20" },
    { entity_id: "SA-002", name: "Amérique Latine (hors Brésil)", country: "Amériques", sector: "Dépendance IA Structurelle", composite_score: 82.25, ai_dependency_exposure_score: 85.0, domestic_ai_capability_deficit_score: 80.0, ai_talent_gap_score: 82.0, compute_autonomy_deficit_score: 78.0, risk_level: "critique", primary_pattern: "dependance_ia_structurelle", key_signals: ["Vassalité IA critique pour Amérique Latine — infrastructure IA sous contrôle technologique étranger", "Déficit de capacités IA domestiques — dépendance aux modèles et puces étrangers totale", "Risque géopolitique majeur — coupure IA possible en cas de tension diplomatique"], estimated_ai_sovereignty_index: 8.23, last_updated: "2026-06-20" },
    { entity_id: "SA-003", name: "Moyen-Orient (hors Golfe)", country: "MENA", sector: "Capacités IA Minimales", composite_score: 79.25, ai_dependency_exposure_score: 82.0, domestic_ai_capability_deficit_score: 78.0, ai_talent_gap_score: 80.0, compute_autonomy_deficit_score: 75.0, risk_level: "critique", primary_pattern: "dependance_ia_structurelle", key_signals: ["Vassalité IA critique pour Moyen-Orient — infrastructure IA sous contrôle technologique étranger", "Déficit de capacités IA domestiques — dépendance aux modèles et puces étrangers totale", "Risque géopolitique majeur — coupure IA possible en cas de tension diplomatique"], estimated_ai_sovereignty_index: 7.93, last_updated: "2026-06-20" },
    { entity_id: "SA-004", name: "Asie du Sud-Est", country: "Asie", sector: "Dépendance Mixte USA/Chine", composite_score: 74.75, ai_dependency_exposure_score: 78.0, domestic_ai_capability_deficit_score: 72.0, ai_talent_gap_score: 75.0, compute_autonomy_deficit_score: 70.0, risk_level: "critique", primary_pattern: "dependance_ia_structurelle", key_signals: ["Vassalité IA critique pour Asie du Sud-Est — infrastructure IA sous contrôle technologique étranger", "Déficit de capacités IA domestiques — dépendance aux modèles et puces étrangers totale", "Risque géopolitique majeur — coupure IA possible en cas de tension diplomatique"], estimated_ai_sovereignty_index: 7.48, last_updated: "2026-06-20" },
    { entity_id: "SA-005", name: "Europe (hors France/Allemagne)", country: "Europe", sector: "Dépendance Cloud US", composite_score: 57.25, ai_dependency_exposure_score: 60.0, domestic_ai_capability_deficit_score: 55.0, ai_talent_gap_score: 58.0, compute_autonomy_deficit_score: 52.0, risk_level: "élevé", primary_pattern: "autonomie_ia_partielle", key_signals: ["Dépendance IA avancée pour Europe — autonomie stratégique compromise", "Talent IA insuffisant et absence de champions nationaux compétitifs", "Compute souverain inexistant — cloud et puces sous juridiction étrangère"], estimated_ai_sovereignty_index: 5.73, last_updated: "2026-06-20" },
    { entity_id: "SA-006", name: "Inde — IA Émergente", country: "Asie du Sud", sector: "Autonomie IA en Construction", composite_score: 38.75, ai_dependency_exposure_score: 42.0, domestic_ai_capability_deficit_score: 38.0, ai_talent_gap_score: 35.0, compute_autonomy_deficit_score: 40.0, risk_level: "modéré", primary_pattern: "strategie_ia_emergente", key_signals: ["Autonomie IA partielle pour Inde — stratégie souveraineté en construction", "Capacités IA domestiques émergentes mais insuffisantes face aux géants technologiques", "Investissements en cours — horizont de souveraineté réaliste à moyen terme"], estimated_ai_sovereignty_index: 3.88, last_updated: "2026-06-20" },
    { entity_id: "SA-007", name: "Europe (France+Allemagne+UK)", country: "Europe", sector: "Stratégie IA Souveraine Partielle", composite_score: 24.25, ai_dependency_exposure_score: 28.0, domestic_ai_capability_deficit_score: 22.0, ai_talent_gap_score: 25.0, compute_autonomy_deficit_score: 20.0, risk_level: "modéré", primary_pattern: "strategie_ia_emergente", key_signals: ["Autonomie IA partielle pour Europe (France+Allemagne+UK) — stratégie souveraineté en construction", "Capacités IA domestiques émergentes mais insuffisantes face aux géants technologiques", "Investissements en cours — horizont de souveraineté réaliste à moyen terme"], estimated_ai_sovereignty_index: 2.43, last_updated: "2026-06-20" },
    { entity_id: "SA-008", name: "USA & Chine — Duopole IA", country: "Global", sector: "Souveraineté IA Maximale", composite_score: 5.75, ai_dependency_exposure_score: 5.0, domestic_ai_capability_deficit_score: 8.0, ai_talent_gap_score: 6.0, compute_autonomy_deficit_score: 4.0, risk_level: "faible", primary_pattern: "souverainete_ia_consolidee", key_signals: ["USA & Chine — Duopole IA dispose d'une souveraineté IA consolidée — infrastructure et talent domestiques solides", "Champions IA nationaux compétitifs et compute souverain opérationnel", "Capacité d'exportation technologique — influence IA mondiale significative"], estimated_ai_sovereignty_index: 0.58, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 1, "modéré": 2, faible: 1 },
    pattern_distribution: { vassalite_ia_totale: 1, dependance_ia_structurelle: 3, autonomie_ia_partielle: 1, strategie_ia_emergente: 2, souverainete_ia_consolidee: 1 },
    top_risk_entities: ["Afrique Subsaharienne", "Amérique Latine (hors Brésil)", "Moyen-Orient (hors Golfe)"],
    critical_alerts: ["Afrique: vassalité IA totale", "Amérique Latine: dépendance IA structurelle", "Moyen-Orient: dépendance IA structurelle", "Asie du Sud-Est: dépendance IA structurelle"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "aisovreignty",
    confidence_score: 0.82,
    data_sources: ["stanford_ai_index", "compute_tracker", "ai_talent_concentration_monitor"],
    entities,
    avg_estimated_ai_sovereignty_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
