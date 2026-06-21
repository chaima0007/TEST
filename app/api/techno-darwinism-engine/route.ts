import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[techno-darwinism-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Techno-Darwinism Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/techno-darwinism-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Techno-Darwinism Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Techno-Darwinism Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "TD-001", name: "Afrique Subsaharienne", country: "Afrique", sector: "Sans Infrastructure Numérique", composite_score: 88.5, technological_adaptation_lag_score: 92.0, workforce_displacement_vulnerability_score: 88.0, innovation_ecosystem_deficit_score: 90.0, regulatory_agility_deficit_score: 82.0, risk_level: "critique", primary_pattern: "extinction_technologique", key_signals: ["Extinction technologique imminente pour Afrique Subsaharienne — fossé avec les leaders s'élargissant", "Main-d'œuvre massivement vulnérable à l'automatisation sans filet social suffisant", "Absence d'écosystème d'innovation local — dépendance technologique totale"], estimated_technodarwin_index: 8.85, last_updated: "2026-06-20" },
    { id: "TD-002", name: "MENA Rentier (hors Golfe)", country: "Moyen-Orient", sector: "Dépendance Hydrocarbures & Stagnation Tech", composite_score: 81.5, technological_adaptation_lag_score: 85.0, workforce_displacement_vulnerability_score: 80.0, innovation_ecosystem_deficit_score: 85.0, regulatory_agility_deficit_score: 75.0, risk_level: "critique", primary_pattern: "decrochage_numerique", key_signals: ["Extinction technologique imminente pour MENA Rentier — fossé avec les leaders s'élargissant", "Main-d'œuvre massivement vulnérable à l'automatisation sans filet social suffisant", "Absence d'écosystème d'innovation local — dépendance technologique totale"], estimated_technodarwin_index: 8.15, last_updated: "2026-06-20" },
    { id: "TD-003", name: "Amérique Latine Moyenne", country: "Amériques", sector: "Sans Écosystème Innovation", composite_score: 78.0, technological_adaptation_lag_score: 80.0, workforce_displacement_vulnerability_score: 78.0, innovation_ecosystem_deficit_score: 82.0, regulatory_agility_deficit_score: 70.0, risk_level: "critique", primary_pattern: "decrochage_numerique", key_signals: ["Extinction technologique imminente pour Amérique Latine Moyenne — fossé avec les leaders s'élargissant", "Main-d'œuvre massivement vulnérable à l'automatisation sans filet social suffisant", "Absence d'écosystème d'innovation local — dépendance technologique totale"], estimated_technodarwin_index: 7.80, last_updated: "2026-06-20" },
    { id: "TD-004", name: "Asie du Sud (hors Inde Tech)", country: "Asie du Sud", sector: "Croissance Sans Innovation Endogène", composite_score: 70.5, technological_adaptation_lag_score: 72.0, workforce_displacement_vulnerability_score: 70.0, innovation_ecosystem_deficit_score: 75.0, regulatory_agility_deficit_score: 65.0, risk_level: "critique", primary_pattern: "decrochage_numerique", key_signals: ["Extinction technologique imminente pour Asie du Sud — fossé avec les leaders s'élargissant", "Main-d'œuvre massivement vulnérable à l'automatisation sans filet social suffisant", "Absence d'écosystème d'innovation local — dépendance technologique totale"], estimated_technodarwin_index: 7.05, last_updated: "2026-06-20" },
    { id: "TD-005", name: "Europe Continentale — Sur-réglementée", country: "Europe", sector: "Innovation vs Précaution Réglementaire", composite_score: 51.1, technological_adaptation_lag_score: 50.0, workforce_displacement_vulnerability_score: 45.0, innovation_ecosystem_deficit_score: 52.0, regulatory_agility_deficit_score: 58.0, risk_level: "élevé", primary_pattern: "transition_douloureuse", key_signals: ["Décrochage numérique avancé en Europe Continentale — transition technologique douloureuse", "Workforce displacement massif sans reconversion suffisante — choc social tech", "Écosystème d'innovation insuffisant — dépendance aux technologies étrangères"], estimated_technodarwin_index: 5.11, last_updated: "2026-06-20" },
    { id: "TD-006", name: "USA/UK — Inégalités d'Accès Tech", country: "Anglosaxon", sector: "Innovation Maximale & Exclusion Sociale", composite_score: 29.0, technological_adaptation_lag_score: 30.0, workforce_displacement_vulnerability_score: 35.0, innovation_ecosystem_deficit_score: 22.0, regulatory_agility_deficit_score: 28.0, risk_level: "modéré", primary_pattern: "adaptation_partielle", key_signals: ["Adaptation technologique partielle aux USA/UK — capacité de rattrapage existante", "Tensions entre vitesse d'adaptation tech et protection sociale des travailleurs", "Réglementation en retard sur les nouvelles technologies — risque d'inadaptation"], estimated_technodarwin_index: 2.90, last_updated: "2026-06-20" },
    { id: "TD-007", name: "Asie du Nord-Est (Japon/Corée)", country: "Asie", sector: "Adaptation Rapide & Résilience", composite_score: 16.5, technological_adaptation_lag_score: 18.0, workforce_displacement_vulnerability_score: 15.0, innovation_ecosystem_deficit_score: 20.0, regulatory_agility_deficit_score: 12.0, risk_level: "faible", primary_pattern: "darwinisme_positif", key_signals: ["Asie du Nord-Est démontre un darwinisme technologique positif — adaptation rapide et continue", "Écosystème d'innovation robuste — capacité à créer et adopter les nouvelles technologies", "Modèle de transition technologique exemplaire à étudier et diffuser"], estimated_technodarwin_index: 1.65, last_updated: "2026-06-20" },
    { id: "TD-008", name: "Chine & Singapour — Leaders Tech", country: "Asie", sector: "Darwinisme Technologique Positif Total", composite_score: 7.9, technological_adaptation_lag_score: 8.0, workforce_displacement_vulnerability_score: 10.0, innovation_ecosystem_deficit_score: 5.0, regulatory_agility_deficit_score: 6.0, risk_level: "faible", primary_pattern: "darwinisme_positif", key_signals: ["Chine & Singapour démontre un darwinisme technologique positif — adaptation rapide et continue", "Écosystème d'innovation robuste — capacité à créer et adopter les nouvelles technologies", "Modèle de transition technologique exemplaire à étudier et diffuser"], estimated_technodarwin_index: 0.79, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 1, "modéré": 1, faible: 2 },
    pattern_distribution: { extinction_technologique: 1, decrochage_numerique: 3, transition_douloureuse: 1, adaptation_partielle: 1, darwinisme_positif: 2 },
    top_risk_entities: ["Afrique Subsaharienne", "MENA Rentier (hors Golfe)", "Amérique Latine Moyenne"],
    critical_alerts: ["Afrique: extinction technologique", "MENA rentier: décrochage numérique", "Amérique Latine: décrochage numérique", "Asie du Sud: décrochage numérique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "technodarwin",
    confidence_score: 0.80,
    data_sources: ["global_innovation_index", "automation_vulnerability_tracker", "digital_readiness_monitor"],
    entities,
    avg_estimated_technodarwin_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
