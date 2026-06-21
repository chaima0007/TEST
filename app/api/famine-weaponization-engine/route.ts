import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[famine-weaponization-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Famine Weaponization Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/famine-weaponization-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Famine Weaponization Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Famine Weaponization Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "FW-001", name: "Yémen — Blocus & Famine Délibérée", country: "MENA", sector: "Coalition Saoudienne Bloquant l'Aide Humanitaire", composite_score: 91.35, blockade_intensity_score: 95.0, humanitarian_access_denial_score: 92.0, agricultural_destruction_score: 88.0, starvation_as_strategy_score: 90.0, risk_level: "critique", primary_pattern: "famine_deliberee_active", key_signals: ["Famine délibérée active dans Yémen — blocus systématique privant les civils d'accès alimentaire", "Violation grave du droit humanitaire international — faim utilisée comme arme de guerre", "Infrastructure agricole détruite délibérément — capacité alimentaire locale anéantie"], estimated_famine_weapon_index: 9.14, last_updated: "2026-06-20" },
    { id: "FW-002", name: "Gaza — Siège Total & Destruction Agricole", country: "MENA", sector: "Blocus Alimentaire Total dans le Territoire Assiégé", composite_score: 91.35, blockade_intensity_score: 92.0, humanitarian_access_denial_score: 95.0, agricultural_destruction_score: 90.0, starvation_as_strategy_score: 88.0, risk_level: "critique", primary_pattern: "famine_deliberee_active", key_signals: ["Famine délibérée active dans Gaza — blocus systématique privant les civils d'accès alimentaire", "Violation grave du droit humanitaire international — faim utilisée comme arme de guerre", "Infrastructure agricole détruite délibérément — capacité alimentaire locale anéantie"], estimated_famine_weapon_index: 9.14, last_updated: "2026-06-20" },
    { id: "FW-003", name: "Soudan — Famine comme Outil de Guerre Civile", country: "Afrique", sector: "RSF & SAF Bloquant l'Aide dans les Zones Adverses", composite_score: 83.25, blockade_intensity_score: 85.0, humanitarian_access_denial_score: 82.0, agricultural_destruction_score: 80.0, starvation_as_strategy_score: 85.0, risk_level: "critique", primary_pattern: "siege_alimentaire", key_signals: ["Famine délibérée active dans Soudan — blocus systématique privant les civils d'accès alimentaire", "Violation grave du droit humanitaire international — faim utilisée comme arme de guerre", "Infrastructure agricole détruite délibérément — capacité alimentaire locale anéantie"], estimated_famine_weapon_index: 8.33, last_updated: "2026-06-20" },
    { id: "FW-004", name: "Éthiopie Tigré — Siège & Starvation", country: "Afrique", sector: "Blocus Gouvernemental du Tigré 2020-2022", composite_score: 79.25, blockade_intensity_score: 80.0, humanitarian_access_denial_score: 78.0, agricultural_destruction_score: 75.0, starvation_as_strategy_score: 82.0, risk_level: "critique", primary_pattern: "siege_alimentaire", key_signals: ["Famine délibérée active dans Éthiopie Tigré — blocus systématique privant les civils d'accès alimentaire", "Violation grave du droit humanitaire international — faim utilisée comme arme de guerre", "Infrastructure agricole détruite délibérément — capacité alimentaire locale anéantie"], estimated_famine_weapon_index: 7.93, last_updated: "2026-06-20" },
    { id: "FW-005", name: "Myanmar — Minorités Ethniques Assiégées", country: "Asie du Sud-Est", sector: "Junta Militaire & Blocus Économique Ethnique", composite_score: 66.5, blockade_intensity_score: 68.0, humanitarian_access_denial_score: 65.0, agricultural_destruction_score: 70.0, starvation_as_strategy_score: 62.0, risk_level: "élevé", primary_pattern: "instrumentalisation_partielle", key_signals: ["Instrumentalisation de la faim dans Myanmar — aide humanitaire conditionnée à des objectifs militaires", "Accès humanitaire sévèrement restreint — populations en situation de pré-famine délibérée", "Destruction agricole partielle — réduction calculée des capacités alimentaires locales"], estimated_famine_weapon_index: 6.65, last_updated: "2026-06-20" },
    { id: "FW-006", name: "Syrie — Reconstruction Instrumentalisée", country: "MENA", sector: "Reconstruction Conditionnée comme Outil de Fidélisation", composite_score: 53.35, blockade_intensity_score: 55.0, humanitarian_access_denial_score: 52.0, agricultural_destruction_score: 48.0, starvation_as_strategy_score: 58.0, risk_level: "élevé", primary_pattern: "instrumentalisation_partielle", key_signals: ["Instrumentalisation de la faim dans Syrie — aide humanitaire conditionnée à des objectifs militaires", "Accès humanitaire sévèrement restreint — populations en situation de pré-famine délibérée", "Destruction agricole partielle — réduction calculée des capacités alimentaires locales"], estimated_famine_weapon_index: 5.34, last_updated: "2026-06-20" },
    { id: "FW-007", name: "Haïti — Gangs & Accès Humanitaire Bloqué", country: "Amériques", sector: "Milices Contrôlant l'Accès Alimentaire dans Zones Urbaines", composite_score: 39.5, blockade_intensity_score: 42.0, humanitarian_access_denial_score: 40.0, agricultural_destruction_score: 38.0, starvation_as_strategy_score: 35.0, risk_level: "modéré", primary_pattern: "risque_utilisation", key_signals: ["Risque d'utilisation de la faim dans Haïti — fragilité alimentaire dans un contexte conflictuel", "Tensions sur l'accès humanitaire — monitoring urgent nécessaire pour prévenir l'escalade", "Capacités agricoles fragilisées par le conflit — prépositionement de stocks d'urgence requis"], estimated_famine_weapon_index: 3.95, last_updated: "2026-06-20" },
    { id: "FW-008", name: "Ukraine — Destruction Céréalière Russe", country: "Europe de l'Est", sector: "Bombardement Silos Blés & Blocage Corridor Maritime", composite_score: 29.5, blockade_intensity_score: 30.0, humanitarian_access_denial_score: 25.0, agricultural_destruction_score: 35.0, starvation_as_strategy_score: 28.0, risk_level: "modéré", primary_pattern: "risque_utilisation", key_signals: ["Risque d'utilisation de la faim dans Ukraine — fragilité alimentaire dans un contexte conflictuel", "Tensions sur l'accès humanitaire — monitoring urgent nécessaire pour prévenir l'escalade", "Capacités agricoles fragilisées par le conflit — prépositionement de stocks d'urgence requis"], estimated_famine_weapon_index: 2.95, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 2, faible: 0 },
    pattern_distribution: { famine_deliberee_active: 2, siege_alimentaire: 2, instrumentalisation_partielle: 2, risque_utilisation: 2, respect_droit_humanitaire: 0 },
    top_risk_entities: ["Yémen — Blocus & Famine Délibérée", "Gaza — Siège Total & Destruction Agricole", "Soudan — Famine comme Outil de Guerre Civile"],
    critical_alerts: ["Yémen: famine délibérée active", "Gaza: famine délibérée active", "Soudan: siège alimentaire", "Éthiopie Tigré: siège alimentaire"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "famine_weapon",
    confidence_score: 0.88,
    data_sources: ["fews_net_famine_tracker", "ipc_acute_food_insecurity", "icrc_humanitarian_access_monitor"],
    entities,
    avg_estimated_famine_weapon_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
