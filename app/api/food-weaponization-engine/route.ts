import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[food-weaponization-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Food Weaponization Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/food-weaponization-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Food Weaponization Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Food Weaponization Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "FW-001", name: "Russie — Blé comme Arme & Blocage Mer Noire", country: "Europe de l'Est", sector: "30% Exports Blé Mondial & Accord Mer Noire Sabordé comme Chantage MENA", composite_score: 84.45, grain_export_control_score: 92.0, fertilizer_monopolization_score: 85.0, agricultural_land_grab_score: 72.0, food_aid_coercion_score: 88.0, risk_level: "critique", primary_pattern: "arme_alimentaire_active", key_signals: ["Arme alimentaire active dans Russie — Blé comme Arme & Blocage Mer Noire — contrôle des exportations céréalières comme levier de coercition géopolitique existentielle", "Weaponisation des flux alimentaires — restrictions d'exportation ou accaparement de terres déstabilisant les marchés mondiaux", "Dépendances alimentaires exploitées — pays importateurs sous menace existentielle de pénurie et chantage alimentaire"], estimated_food_weapon_index: 8.45, last_updated: "2026-06-20" },
    { entity_id: "FW-002", name: "Chine — Land Grab Africain & Stocks Stratégiques", country: "Asie", sector: "3M Ha Africains & 65% Stocks Mondiaux Maïs/Blé/Riz — Arsenal Alimentaire", composite_score: 78.9, grain_export_control_score: 75.0, fertilizer_monopolization_score: 80.0, agricultural_land_grab_score: 88.0, food_aid_coercion_score: 72.0, risk_level: "critique", primary_pattern: "accaparement_terres_strategique", key_signals: ["Arme alimentaire active dans Chine — Land Grab Africain & Stocks Stratégiques — contrôle des exportations céréalières comme levier de coercition géopolitique existentielle", "Weaponisation des flux alimentaires — restrictions d'exportation ou accaparement de terres déstabilisant les marchés mondiaux", "Dépendances alimentaires exploitées — pays importateurs sous menace existentielle de pénurie et chantage alimentaire"], estimated_food_weapon_index: 7.89, last_updated: "2026-06-20" },
    { entity_id: "FW-003", name: "USA — Sanctions Alimentaires & Aid Conditionnalité", country: "Amérique du Nord", sector: "Embargo Alimentaire Cuba/Iran & USAID comme Levier de Politique Étrangère", composite_score: 70.65, grain_export_control_score: 68.0, fertilizer_monopolization_score: 72.0, agricultural_land_grab_score: 65.0, food_aid_coercion_score: 80.0, risk_level: "critique", primary_pattern: "coercition_alimentaire", key_signals: ["Arme alimentaire active dans USA — Sanctions Alimentaires & Aid Conditionnalité — contrôle des exportations céréalières comme levier de coercition géopolitique existentielle", "Weaponisation des flux alimentaires — restrictions d'exportation ou accaparement de terres déstabilisant les marchés mondiaux", "Dépendances alimentaires exploitées — pays importateurs sous menace existentielle de pénurie et chantage alimentaire"], estimated_food_weapon_index: 7.07, last_updated: "2026-06-20" },
    { entity_id: "FW-004", name: "Inde — Interdiction Export Riz 2023 & Blé", country: "Asie du Sud", sector: "Bans Export Riz/Blé Explosant Prix Mondiaux — 1.4Mds Mangent d'Abord", composite_score: 67.6, grain_export_control_score: 82.0, fertilizer_monopolization_score: 60.0, agricultural_land_grab_score: 68.0, food_aid_coercion_score: 55.0, risk_level: "critique", primary_pattern: "coercition_alimentaire", key_signals: ["Arme alimentaire active dans Inde — Interdiction Export Riz 2023 & Blé — contrôle des exportations céréalières comme levier de coercition géopolitique existentielle", "Weaponisation des flux alimentaires — restrictions d'exportation ou accaparement de terres déstabilisant les marchés mondiaux", "Dépendances alimentaires exploitées — pays importateurs sous menace existentielle de pénurie et chantage alimentaire"], estimated_food_weapon_index: 6.76, last_updated: "2026-06-20" },
    { entity_id: "FW-005", name: "Ukraine/UE — Couloir Céréalier & Dépendance MENA", country: "Europe/MENA", sector: "47 Pays Dépendants Corridor Mer Noire — Blocus Russe comme Levier", composite_score: 50.15, grain_export_control_score: 55.0, fertilizer_monopolization_score: 48.0, agricultural_land_grab_score: 45.0, food_aid_coercion_score: 52.0, risk_level: "élevé", primary_pattern: "coercition_alimentaire", key_signals: ["Coercition alimentaire significative dans Ukraine/UE — Couloir Céréalier & Dépendance MENA — politisation des exportations ou de l'aide alimentaire", "Conditionnalité alimentaire — aide ou accès aux marchés liés à des concessions politiques explicites", "Concentration alimentaire risquée — dépendance excessive d'États vulnérables à un fournisseur dominant"], estimated_food_weapon_index: 5.02, last_updated: "2026-06-20" },
    { entity_id: "FW-006", name: "Brésil/Argentine — Soja & Influence Régionale", country: "Amériques", sector: "60% Soja Mondial & Pouvoir de Marché sur Protéines Animales Globales", composite_score: 44.6, grain_export_control_score: 45.0, fertilizer_monopolization_score: 42.0, agricultural_land_grab_score: 52.0, food_aid_coercion_score: 38.0, risk_level: "élevé", primary_pattern: "coercition_alimentaire", key_signals: ["Coercition alimentaire significative dans Brésil/Argentine — Soja & Influence Régionale — politisation des exportations ou de l'aide alimentaire", "Conditionnalité alimentaire — aide ou accès aux marchés liés à des concessions politiques explicites", "Concentration alimentaire risquée — dépendance excessive d'États vulnérables à un fournisseur dominant"], estimated_food_weapon_index: 4.46, last_updated: "2026-06-20" },
    { entity_id: "FW-007", name: "Indonésie — Palm Oil Ban & Nationalisme Agricole", country: "Asie du Sud-Est", sector: "Interdiction Export Huile Palme 2022 — Souveraineté vs Marchés Mondiaux", composite_score: 32.0, grain_export_control_score: 35.0, fertilizer_monopolization_score: 38.0, agricultural_land_grab_score: 28.0, food_aid_coercion_score: 25.0, risk_level: "modéré", primary_pattern: "nationalisme_alimentaire", key_signals: ["Nationalisme alimentaire dans Indonésie — Palm Oil Ban & Nationalisme Agricole — restrictions d'exportation protectionnistes créant des tensions mondiales", "Protectionnisme agricole non coordonné — chocs en cascade sur les marchés alimentaires des pays les plus pauvres", "Risque de dérapage — nationalisme alimentaire pouvant basculer vers weaponisation sous pression géopolitique"], estimated_food_weapon_index: 3.2, last_updated: "2026-06-20" },
    { entity_id: "FW-008", name: "FAO & PAM — Architecture Alimentaire Mondiale", country: "Global", sector: "Systèmes Alerte Précoce, Réserves Humanitaires & Gouvernance Neutre FAO", composite_score: 5.6, grain_export_control_score: 5.0, fertilizer_monopolization_score: 4.0, agricultural_land_grab_score: 6.0, food_aid_coercion_score: 8.0, risk_level: "faible", primary_pattern: "gouvernance_alimentaire_mondiale", key_signals: ["FAO & PAM — Architecture Alimentaire Mondiale contribue positivement à la gouvernance alimentaire mondiale — architecture multilatérale équitable", "Systèmes d'alerte précoce alimentaire et mécanismes de stabilisation des prix efficaces et inclusifs", "Modèle de partage alimentaire à diffuser — solidarité alimentaire mondiale sans conditionnalité politique"], estimated_food_weapon_index: 0.56, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { arme_alimentaire_active: 1, accaparement_terres_strategique: 1, coercition_alimentaire: 4, nationalisme_alimentaire: 1, gouvernance_alimentaire_mondiale: 1 },
    top_risk_entities: ["Russie — Blé comme Arme & Blocage Mer Noire", "Chine — Land Grab Africain & Stocks Stratégiques", "USA — Sanctions Alimentaires & Aid Conditionnalité"],
    critical_alerts: ["Russie: arme alimentaire active", "Chine: accaparement terres stratégique", "USA: coercition alimentaire", "Inde: coercition alimentaire"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "food_weapon",
    confidence_score: 0.88,
    data_sources: ["fao_food_insecurity_monitor", "grain_market_international_panel", "oxfam_land_rights_tracker"],
    entities,
    avg_estimated_food_weapon_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
