import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[nexus-crisis-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Nexus Crisis Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nexus-crisis-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Nexus Crisis Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Nexus Crisis Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "NX-001", name: "Sahel & Corne de l'Afrique", country: "Afrique", sector: "Sécurité Alimentaire Hydrique", composite_score: 86.25, water_stress_score: 92.0, food_security_deficit_score: 88.0, energy_dependency_score: 80.0, nexus_coupling_score: 85.0, risk_level: "critique", primary_pattern: "vortex_nexus_total", key_signals: ["Vortex Nexus critique — convergence eau-alimentation-énergie en rupture", "Effets de cascade inter-sectoriels au-delà des seuils de résilience", "Couplage Nexus pathologique — intervention systémique requise"], estimated_nexus_index: 8.63, last_updated: "2026-06-20" },
    { entity_id: "NX-002", name: "Moyen-Orient & Péninsule Arabique", country: "MENA", sector: "Eau & Énergie Fossile", composite_score: 75.05, water_stress_score: 90.0, food_security_deficit_score: 78.0, energy_dependency_score: 35.0, nexus_coupling_score: 82.0, risk_level: "critique", primary_pattern: "cascade_eau_energie", key_signals: ["Vortex Nexus critique — stress hydrique extrême malgré abondance énergétique", "Dépendance alimentaire importée — fragilité structurelle majeure", "Couplage eau-dessalement-énergie critique sous pression climatique"], estimated_nexus_index: 7.51, last_updated: "2026-06-20" },
    { entity_id: "NX-003", name: "Asie du Sud (Gange-Indus)", country: "Asie du Sud", sector: "Agriculture & Eau Souterraine", composite_score: 76.95, water_stress_score: 82.0, food_security_deficit_score: 80.0, energy_dependency_score: 65.0, nexus_coupling_score: 78.0, risk_level: "critique", primary_pattern: "vortex_nexus_total", key_signals: ["Crise Nexus critique — surexploitation des aquifères Gange-Indus", "Agriculture intensive épuisant les nappes phréatiques", "Sécurité alimentaire d'1,7 milliard de personnes menacée"], estimated_nexus_index: 7.70, last_updated: "2026-06-20" },
    { entity_id: "NX-004", name: "Asie Centrale (Mer d'Aral)", country: "Asie Centrale", sector: "Eau & Agriculture", composite_score: 80.75, water_stress_score: 88.0, food_security_deficit_score: 75.0, energy_dependency_score: 70.0, nexus_coupling_score: 80.0, risk_level: "critique", primary_pattern: "vortex_nexus_total", key_signals: ["Catastrophe Nexus en cours — assèchement systémique de la Mer d'Aral", "Compétition hydrique inter-étatique Amu-Darya/Syr-Darya", "Cercle vicieux désertification-agriculture-eau"], estimated_nexus_index: 8.08, last_updated: "2026-06-20" },
    { entity_id: "NX-005", name: "Amérique Centrale", country: "Amériques", sector: "Corridor de la Sécheresse", composite_score: 61.25, water_stress_score: 65.0, food_security_deficit_score: 62.0, energy_dependency_score: 58.0, nexus_coupling_score: 55.0, risk_level: "critique", primary_pattern: "tension_nexus_elevee", key_signals: ["Stress Nexus élevé — corridor sec d'Amérique centrale sous pression", "Migration climatique liée aux déficits eau-nourriture", "Fragilité énergétique amplifiant les crises agricoles"], estimated_nexus_index: 6.13, last_updated: "2026-06-20" },
    { entity_id: "NX-006", name: "Europe Méditerranéenne", country: "Europe", sector: "Agriculture & Eau Douce", composite_score: 43.5, water_stress_score: 48.0, food_security_deficit_score: 42.0, energy_dependency_score: 38.0, nexus_coupling_score: 45.0, risk_level: "élevé", primary_pattern: "tension_nexus_elevee", key_signals: ["Tensions Nexus élevées — sécheresses méditerranéennes s'intensifiant", "Agriculture sous pression hydrique — adaptation nécessaire", "Dépendance énergétique aux importations crée une vulnérabilité"], estimated_nexus_index: 4.35, last_updated: "2026-06-20" },
    { entity_id: "NX-007", name: "Amérique du Nord", country: "Amériques", sector: "Aquifères & Énergie", composite_score: 29.0, water_stress_score: 32.0, food_security_deficit_score: 25.0, energy_dependency_score: 28.0, nexus_coupling_score: 30.0, risk_level: "modéré", primary_pattern: "stress_sectoriel", key_signals: ["Stress Nexus modéré — Ogallala aquifer sous pression croissante", "Sécurité alimentaire robuste mais fragilités régionales", "Indépendance énergétique maintenue — gestion préventive suffisante"], estimated_nexus_index: 2.90, last_updated: "2026-06-20" },
    { entity_id: "NX-008", name: "Europe du Nord", country: "Europe", sector: "Ressources Durables", composite_score: 11.5, water_stress_score: 12.0, food_security_deficit_score: 10.0, energy_dependency_score: 15.0, nexus_coupling_score: 8.0, risk_level: "faible", primary_pattern: "nexus_resilient", key_signals: ["Nexus eau-alimentation-énergie en équilibre exemplaire", "Ressources hydriques abondantes et agriculture durable", "Transition énergétique avancée — résilience Nexus renforcée"], estimated_nexus_index: 1.15, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 1, "modéré": 1, faible: 1 },
    pattern_distribution: { vortex_nexus_total: 3, cascade_eau_energie: 1, tension_nexus_elevee: 2, stress_sectoriel: 1, nexus_resilient: 1 },
    top_risk_entities: ["Sahel & Corne de l'Afrique", "Asie Centrale (Mer d'Aral)", "Asie du Sud (Gange-Indus)"],
    critical_alerts: ["Sahel & Corne de l'Afrique: vortex nexus total", "Asie Centrale: vortex nexus total", "Asie du Sud: vortex nexus total"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "nexus",
    confidence_score: 0.89,
    data_sources: ["water_stress_index", "global_food_security_index", "energy_dependency_tracker"],
    entities,
    avg_estimated_nexus_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
