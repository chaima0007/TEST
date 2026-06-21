import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[refugee-weaponization-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Refugee Weaponization Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/refugee-weaponization-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Refugee Weaponization Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Refugee Weaponization Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "RW-001", name: "Biélorussie — Crise Frontalière 2021 UE", country: "Europe de l'Est", sector: "Loukachenko Orchestrant Transit Migrants Moyen-Orientaux vers Pologne", composite_score: 88.85, deliberate_flow_manipulation_score: 92.0, political_leverage_score: 88.0, humanitarian_access_denial_score: 85.0, destabilization_intent_score: 90.0, risk_level: "critique", primary_pattern: "weaponisation_active", key_signals: ["Weaponisation active des réfugiés par Biélorussie — Crise Frontalière 2021 UE — flux migratoires délibérément orchestrés comme arme géopolitique", "Chantage migratoire explicite — menaces d'ouvrir les frontières utilisées pour extorquer des concessions politiques", "Populations réfugiées instrumentalisées — violation du droit humanitaire international à des fins géopolitiques"], estimated_refugee_weapon_index: 8.89, last_updated: "2026-06-20" },
    { id: "RW-002", name: "Turquie — Chantage Migratoire Chronique", country: "MENA/Europe", sector: "Erdoğan Menaçant l'UE d'Ouvrir les Vannes — 3.6M Syriens comme Levier", composite_score: 83.3, deliberate_flow_manipulation_score: 80.0, political_leverage_score: 92.0, humanitarian_access_denial_score: 72.0, destabilization_intent_score: 85.0, risk_level: "critique", primary_pattern: "chantage_migratoire", key_signals: ["Weaponisation active des réfugiés par Turquie — Chantage Migratoire Chronique — flux migratoires délibérément orchestrés comme arme géopolitique", "Chantage migratoire explicite — menaces d'ouvrir les frontières utilisées pour extorquer des concessions politiques", "Populations réfugiées instrumentalisées — violation du droit humanitaire international à des fins géopolitiques"], estimated_refugee_weapon_index: 8.33, last_updated: "2026-06-20" },
    { id: "RW-003", name: "Russie — Déplacements Ukrainiens Instrumentalisés", country: "Europe de l'Est", sector: "Attaques Infrastructures Créant Vagues Migratoires vers l'Europe", composite_score: 83.4, deliberate_flow_manipulation_score: 85.0, political_leverage_score: 78.0, humanitarian_access_denial_score: 88.0, destabilization_intent_score: 82.0, risk_level: "critique", primary_pattern: "weaponisation_active", key_signals: ["Weaponisation active des réfugiés par Russie — Déplacements Ukrainiens Instrumentalisés — flux migratoires délibérément orchestrés comme arme géopolitique", "Chantage migratoire explicite — menaces d'ouvrir les frontières utilisées pour extorquer des concessions politiques", "Populations réfugiées instrumentalisées — violation du droit humanitaire international à des fins géopolitiques"], estimated_refugee_weapon_index: 8.34, last_updated: "2026-06-20" },
    { id: "RW-004", name: "Libye — Trafic Migrants comme Industrie d'État", country: "MENA", sector: "Factions Libyennes Contrôlant Flux Africains vers l'Europe — Chantage", composite_score: 79.1, deliberate_flow_manipulation_score: 78.0, political_leverage_score: 80.0, humanitarian_access_denial_score: 82.0, destabilization_intent_score: 75.0, risk_level: "critique", primary_pattern: "chantage_migratoire", key_signals: ["Weaponisation active des réfugiés par Libye — Trafic Migrants comme Industrie d'État — flux migratoires délibérément orchestrés comme arme géopolitique", "Chantage migratoire explicite — menaces d'ouvrir les frontières utilisées pour extorquer des concessions politiques", "Populations réfugiées instrumentalisées — violation du droit humanitaire international à des fins géopolitiques"], estimated_refugee_weapon_index: 7.91, last_updated: "2026-06-20" },
    { id: "RW-005", name: "Maroc — Flux Ceutistes 2021 comme Pression", country: "MENA/Europe", sector: "Crise Ceuta 2021 — Ouverture Frontière pour Punir l'Espagne sur Sahara", composite_score: 48.65, deliberate_flow_manipulation_score: 48.0, political_leverage_score: 55.0, humanitarian_access_denial_score: 42.0, destabilization_intent_score: 50.0, risk_level: "élevé", primary_pattern: "destabilisation_frontaliere", key_signals: ["Instrumentalisation migratoire significative par Maroc — Flux Ceutistes 2021 comme Pression — flux exploités pour fragiliser les États voisins ou partenaires", "Facilitation opaque des flux transfrontaliers — complaisance délibérée envers les passeurs pour créer des pressions", "Utilisation des réfugiés comme variable d'ajustement dans les négociations politiques bilatérales"], estimated_refugee_weapon_index: 4.87, last_updated: "2026-06-20" },
    { id: "RW-006", name: "Éthiopie & Érythrée — Flux comme Arme de Guerre", country: "Afrique de l'Est", sector: "Déplacements Tigré Utilisés comme Arme de Pression Régionale", composite_score: 53.6, deliberate_flow_manipulation_score: 52.0, political_leverage_score: 48.0, humanitarian_access_denial_score: 60.0, destabilization_intent_score: 55.0, risk_level: "élevé", primary_pattern: "destabilisation_frontaliere", key_signals: ["Instrumentalisation migratoire significative par Éthiopie & Érythrée — Flux comme Arme de Guerre — flux exploités pour fragiliser les États voisins ou partenaires", "Facilitation opaque des flux transfrontaliers — complaisance délibérée envers les passeurs pour créer des pressions", "Utilisation des réfugiés comme variable d'ajustement dans les négociations politiques bilatérales"], estimated_refugee_weapon_index: 5.36, last_updated: "2026-06-20" },
    { id: "RW-007", name: "Venezuela — Crise Migratoire Exportée", country: "Amériques", sector: "6M de Réfugiés Vénézuéliens comme Fardeau pour les Voisins Régionaux", composite_score: 39.65, deliberate_flow_manipulation_score: 38.0, political_leverage_score: 42.0, humanitarian_access_denial_score: 35.0, destabilization_intent_score: 45.0, risk_level: "modéré", primary_pattern: "instrumentalisation_partielle", key_signals: ["Risques d'instrumentalisation migratoire dans Venezuela — Crise Migratoire Exportée — tension entre gestion humanitaire et calculs géopolitiques", "Flux migratoires partiellement utilisés à des fins de pression politique modérée", "Monitoring humanitaire nécessaire pour distinguer gestion légitime et weaponisation émergente"], estimated_refugee_weapon_index: 3.97, last_updated: "2026-06-20" },
    { id: "RW-008", name: "UNHCR & Canada — Modèles d'Accueil", country: "Global", sector: "Systèmes de Parrainage Privé et Réinstallation Planifiée Non-Instrumentalisée", composite_score: 4.6, deliberate_flow_manipulation_score: 5.0, political_leverage_score: 4.0, humanitarian_access_denial_score: 6.0, destabilization_intent_score: 3.0, risk_level: "faible", primary_pattern: "gestion_humanitaire", key_signals: ["UNHCR & Canada — Modèles d'Accueil gère les flux migratoires conformément au droit humanitaire international", "Protection effective des réfugiés sans instrumentalisation à des fins de pression politique", "Modèle de gestion humanitaire à partager — accueil, protection et intégration sans weaponisation"], estimated_refugee_weapon_index: 0.46, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { weaponisation_active: 2, chantage_migratoire: 2, destabilisation_frontaliere: 2, instrumentalisation_partielle: 1, gestion_humanitaire: 1 },
    top_risk_entities: ["Biélorussie — Crise Frontalière 2021 UE", "Russie — Déplacements Ukrainiens Instrumentalisés", "Turquie — Chantage Migratoire Chronique"],
    critical_alerts: ["Biélorussie: weaponisation active", "Russie: weaponisation active", "Turquie: chantage migratoire", "Libye: chantage migratoire"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "refugee_weapon",
    confidence_score: 0.81,
    data_sources: ["unhcr_global_trends", "iom_migration_data_portal", "migrants_as_weapon_monitor"],
    entities,
    avg_estimated_refugee_weapon_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
