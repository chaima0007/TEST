import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[small-arms-proliferation-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Small Arms Proliferation Engine Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/small-arms-proliferation-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Small Arms Proliferation Engine Agent")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Small Arms Proliferation Engine Agent"), { status: 502 }));
  }
}

function getMockData() {
  const entities = [
    { id: "SA-001", name: "Sahel — Zone de Saturation ALPC", country: "Afrique de l'Ouest", sector: "Flux Libye-Mali-Niger-Burkina — Arsenaux Djihadistes", composite_score: 88.55, illicit_flow_score: 92.0, stockpile_leakage_score: 88.0, non_state_actor_arming_score: 90.0, post_conflict_saturation_score: 85.0, risk_level: "critique", primary_pattern: "proliferation_incontrôlable", key_signals: ["Prolifération ALPC incontrôlable dans Sahel — flux illicites massifs alimentant violence et insécurité", "Armement des groupes non-étatiques — milices, gangs et groupes terroristes suréquipés en ALPC", "Saturation post-conflit — armes survivant aux conflits et recyclées dans de nouveaux cycles de violence"], estimated_arms_risk_index: 8.86, last_updated: "2026-06-20" },
    { id: "SA-002", name: "Haïti — Armes US Inondant les Gangs", country: "Amériques", sector: "Trafic Floride-Haïti — Gangs Contrôlant Port-au-Prince", composite_score: 85.15, illicit_flow_score: 85.0, stockpile_leakage_score: 82.0, non_state_actor_arming_score: 92.0, post_conflict_saturation_score: 78.0, risk_level: "critique", primary_pattern: "marche_gris_actif", key_signals: ["Prolifération ALPC incontrôlable dans Haïti — flux illicites massifs alimentant violence et insécurité", "Armement des groupes non-étatiques — milices, gangs et groupes terroristes suréquipés en ALPC", "Saturation post-conflit — armes survivant aux conflits et recyclées dans de nouveaux cycles de violence"], estimated_arms_risk_index: 8.52, last_updated: "2026-06-20" },
    { id: "SA-003", name: "Yémen & Somalie — Arsenaux en Dérive", country: "MENA/Afrique de l'Est", sector: "Blocus Contourné — Livraisons Maritimes Illicites d'ALPC", composite_score: 86.35, illicit_flow_score: 88.0, stockpile_leakage_score: 85.0, non_state_actor_arming_score: 82.0, post_conflict_saturation_score: 88.0, risk_level: "critique", primary_pattern: "proliferation_incontrôlable", key_signals: ["Prolifération ALPC incontrôlable dans Yémen & Somalie — flux illicites massifs alimentant violence et insécurité", "Armement des groupes non-étatiques — milices, gangs et groupes terroristes suréquipés en ALPC", "Saturation post-conflit — armes survivant aux conflits et recyclées dans de nouveaux cycles de violence"], estimated_arms_risk_index: 8.64, last_updated: "2026-06-20" },
    { id: "SA-004", name: "Balkans — Surplus Yougoslaves Persistants", country: "Europe du Sud-Est", sector: "Armes des Guerres 90s Alimentant Crime Organisé Européen", composite_score: 79.75, illicit_flow_score: 75.0, stockpile_leakage_score: 80.0, non_state_actor_arming_score: 72.0, post_conflict_saturation_score: 90.0, risk_level: "critique", primary_pattern: "proliferation_incontrôlable", key_signals: ["Prolifération ALPC incontrôlable dans Balkans — flux illicites massifs alimentant violence et insécurité", "Armement des groupes non-étatiques — milices, gangs et groupes terroristes suréquipés en ALPC", "Saturation post-conflit — armes survivant aux conflits et recyclées dans de nouveaux cycles de violence"], estimated_arms_risk_index: 7.98, last_updated: "2026-06-20" },
    { id: "SA-005", name: "Amérique Centrale — Armes US & Maras", country: "Amériques", sector: "AR-15 & Pistolets US Alimentant Gangs Honduras-Guatemala-Salvador", composite_score: 71.1, illicit_flow_score: 70.0, stockpile_leakage_score: 65.0, non_state_actor_arming_score: 80.0, post_conflict_saturation_score: 68.0, risk_level: "critique", primary_pattern: "marche_gris_actif", key_signals: ["Prolifération ALPC incontrôlable dans Amérique Centrale — flux illicites massifs alimentant violence et insécurité", "Armement des groupes non-étatiques — milices, gangs et groupes terroristes suréquipés en ALPC", "Saturation post-conflit — armes survivant aux conflits et recyclées dans de nouveaux cycles de violence"], estimated_arms_risk_index: 7.11, last_updated: "2026-06-20" },
    { id: "SA-006", name: "Ukraine — Dispersion Post-Conflit", country: "Europe de l'Est", sector: "ALPC Livrées par l'Ouest Risquant de Fuir vers Crime Organisé", composite_score: 58.1, illicit_flow_score: 55.0, stockpile_leakage_score: 62.0, non_state_actor_arming_score: 48.0, post_conflict_saturation_score: 70.0, risk_level: "élevé", primary_pattern: "flux_transfrontaliers", key_signals: ["Flux ALPC importants traversant Ukraine — corridors illicites alimentant les conflits régionaux", "Fuites de stocks étatiques — arsenaux mal sécurisés alimentant les marchés illicites locaux", "Acteurs non-étatiques armés — groupes criminels et paramilitaires en accès facilité aux ALPC"], estimated_arms_risk_index: 5.81, last_updated: "2026-06-20" },
    { id: "SA-007", name: "Inde & Pakistan — Frontières Poreuses", country: "Asie du Sud", sector: "Trafic ALPC aux Frontières — Alimentation Groupes Séparatistes", composite_score: 40.75, illicit_flow_score: 42.0, stockpile_leakage_score: 38.0, non_state_actor_arming_score: 45.0, post_conflict_saturation_score: 35.0, risk_level: "élevé", primary_pattern: "flux_transfrontaliers", key_signals: ["Flux ALPC importants traversant Inde & Pakistan — corridors illicites alimentant les conflits régionaux", "Fuites de stocks étatiques — arsenaux mal sécurisés alimentant les marchés illicites locaux", "Acteurs non-étatiques armés — groupes criminels et paramilitaires en accès facilité aux ALPC"], estimated_arms_risk_index: 4.08, last_updated: "2026-06-20" },
    { id: "SA-008", name: "Japon & Australie — Contrôle Exemplaire", country: "Asie-Pacifique", sector: "Registres Exhaustifs et Marchés Légaux Ultra-Régulés", composite_score: 4.5, illicit_flow_score: 5.0, stockpile_leakage_score: 4.0, non_state_actor_arming_score: 3.0, post_conflict_saturation_score: 6.0, risk_level: "faible", primary_pattern: "controle_efficace", key_signals: ["Japon & Australie maintient un contrôle ALPC efficace — registres à jour et transferts traçables", "Cadre légal robuste sur les armes légères avec sanctions effectives contre les trafiquants", "Participation active au Traité sur le Commerce des Armes et partage de renseignements balistiques"], estimated_arms_risk_index: 0.45, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 2, "modéré": 0, faible: 1 },
    pattern_distribution: { "proliferation_incontrôlable": 3, marche_gris_actif: 2, flux_transfrontaliers: 2, risque_accumulation: 0, controle_efficace: 1 },
    top_risk_entities: ["Sahel — Zone de Saturation ALPC", "Yémen & Somalie — Arsenaux en Dérive", "Haïti — Armes US Inondant les Gangs"],
    critical_alerts: ["Sahel: prolifération incontrôlable", "Yémen & Somalie: prolifération incontrôlable", "Haïti: marché gris actif", "Balkans: prolifération incontrôlable", "Amérique Centrale: marché gris actif"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "small_arms",
    confidence_score: 0.82,
    data_sources: ["small_arms_survey_geneva", "un_register_conventional_arms", "interpol_illicit_arms_tracker"],
    entities,
    avg_estimated_arms_risk_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
