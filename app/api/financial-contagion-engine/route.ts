import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[financial-contagion-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Financial Contagion Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/financial-contagion-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Financial Contagion Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Financial Contagion Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "FC-001", name: "Marché des Dérivés OTC Global", country: "Global", sector: "700 Trilliards$ Dérivés Hors Bilan — Risque Systémique #1", composite_score: 91.35, interconnection_density_score: 95.0, leverage_excess_score: 92.0, regulatory_arbitrage_exposure_score: 90.0, crisis_transmission_speed_score: 88.0, risk_level: "critique", primary_pattern: "contagion_systemique_imminente", key_signals: ["Contagion systémique imminente dans Marché des Dérivés — nœuds too-big-to-fail avec levier excessif", "Vitesse de transmission de crise maximale — effets dominos potentiellement mondiaux en 72h", "Arbitrage réglementaire exposant le système — risques accumulés hors bilan et hors régulation"], estimated_contagion_index: 9.14, last_updated: "2026-06-20" },
    { id: "FC-002", name: "Chine — Immobilier & Evergrande Effect", country: "Asie", sector: "Bulle Immobilière & Banques Fantômes (Shadow Banking)", composite_score: 85.5, interconnection_density_score: 88.0, leverage_excess_score: 85.0, regulatory_arbitrage_exposure_score: 82.0, crisis_transmission_speed_score: 85.0, risk_level: "critique", primary_pattern: "contagion_systemique_imminente", key_signals: ["Contagion systémique imminente dans Chine — nœuds too-big-to-fail avec levier excessif", "Vitesse de transmission de crise maximale — effets dominos potentiellement mondiaux en 72h", "Arbitrage réglementaire exposant le système — risques accumulés hors bilan et hors régulation"], estimated_contagion_index: 8.55, last_updated: "2026-06-20" },
    { id: "FC-003", name: "Wall Street — Trop Grande pour Faire Faillite", country: "Amérique du Nord", sector: "JPMorgan/Goldman — Nœuds Systemically Important Globaux", composite_score: 79.25, interconnection_density_score: 82.0, leverage_excess_score: 78.0, regulatory_arbitrage_exposure_score: 75.0, crisis_transmission_speed_score: 80.0, risk_level: "critique", primary_pattern: "noeud_fragile_critique", key_signals: ["Contagion systémique imminente dans Wall Street — nœuds too-big-to-fail avec levier excessif", "Vitesse de transmission de crise maximale — effets dominos potentiellement mondiaux en 72h", "Arbitrage réglementaire exposant le système — risques accumulés hors bilan et hors régulation"], estimated_contagion_index: 7.93, last_updated: "2026-06-20" },
    { id: "FC-004", name: "Europe — Banques en Réseau Dense", country: "Europe", sector: "Deutsche Bank & Contagion Intra-Européenne", composite_score: 73.25, interconnection_density_score: 75.0, leverage_excess_score: 72.0, regulatory_arbitrage_exposure_score: 68.0, crisis_transmission_speed_score: 78.0, risk_level: "critique", primary_pattern: "vulnerabilite_contagion", key_signals: ["Vulnérabilité à la contagion sévère dans Europe — expositions croisées élevées sans pare-feux", "Effet de levier systémique excessif — amplification des pertes en cas de choc exogène", "Canaux de transmission de crise identifiés — stress tests révélant des lacunes critiques"], estimated_contagion_index: 7.33, last_updated: "2026-06-20" },
    { id: "FC-005", name: "Cryptomonnaies — Contagion DeFi", country: "Cyberespace", sector: "FTX Collapse Effect & Interconnexion DeFi-TradFi", composite_score: 71.75, interconnection_density_score: 70.0, leverage_excess_score: 68.0, regulatory_arbitrage_exposure_score: 85.0, crisis_transmission_speed_score: 65.0, risk_level: "critique", primary_pattern: "vulnerabilite_contagion", key_signals: ["Vulnérabilité à la contagion sévère dans Cryptomonnaies — expositions croisées élevées sans pare-feux", "Effet de levier systémique excessif — amplification des pertes en cas de choc exogène", "Canaux de transmission de crise identifiés — stress tests révélant des lacunes critiques"], estimated_contagion_index: 7.18, last_updated: "2026-06-20" },
    { id: "FC-006", name: "Marchés Émergents — Effet Dollar", country: "Global", sector: "Vulnérabilité au Dollar Fort & Sudden Stop des Capitaux", composite_score: 59.35, interconnection_density_score: 60.0, leverage_excess_score: 55.0, regulatory_arbitrage_exposure_score: 58.0, crisis_transmission_speed_score: 62.0, risk_level: "élevé", primary_pattern: "risque_modere_interconnecte", key_signals: ["Risque modéré d'interconnexion dans Marchés Émergents — canaux de contagion présents mais absorbeurs actifs", "Surveillance macroprudentielle en place — régulateurs alertes aux risques systémiques émergents", "Coussins de capital partiellement suffisants mais stress tests révélant des fragilités résiduelles"], estimated_contagion_index: 5.94, last_updated: "2026-06-20" },
    { id: "FC-007", name: "Japon — Dette Souveraine & Yen Carry Trade", country: "Asie du Nord-Est", sector: "Yen Carry Trade Dénouement & JGB Bubble", composite_score: 47.25, interconnection_density_score: 48.0, leverage_excess_score: 52.0, regulatory_arbitrage_exposure_score: 42.0, crisis_transmission_speed_score: 45.0, risk_level: "élevé", primary_pattern: "risque_modere_interconnecte", key_signals: ["Risque modéré d'interconnexion dans Japon — canaux de contagion présents mais absorbeurs actifs", "Surveillance macroprudentielle en place — régulateurs alertes aux risques systémiques émergents", "Coussins de capital partiellement suffisants mais stress tests révélant des fragilités résiduelles"], estimated_contagion_index: 4.73, last_updated: "2026-06-20" },
    { id: "FC-008", name: "Canada & Australie — Résilience Régulée", country: "Anglo-Saxon", sector: "Supervision Macroprudentielle Robuste & Coussins Capital", composite_score: 19.25, interconnection_density_score: 22.0, leverage_excess_score: 18.0, regulatory_arbitrage_exposure_score: 15.0, crisis_transmission_speed_score: 20.0, risk_level: "faible", primary_pattern: "resilience_systemique", key_signals: ["Canada & Australie maintient une résilience systémique — pare-feux financiers robustes et régulation efficace", "Standards prudentiels stricts et coordination internationale des régulateurs opérationnelle", "Modèle de résilience financière systémique — capacité d'absorption des chocs sans contagion externe"], estimated_contagion_index: 1.93, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 5, "élevé": 2, "modéré": 0, faible: 1 },
    pattern_distribution: { contagion_systemique_imminente: 2, noeud_fragile_critique: 1, vulnerabilite_contagion: 2, risque_modere_interconnecte: 2, resilience_systemique: 1 },
    top_risk_entities: ["Marché des Dérivés OTC Global", "Chine — Immobilier & Evergrande Effect", "Wall Street — Trop Grande pour Faire Faillite"],
    critical_alerts: ["Dérivés OTC: contagion systémique imminente", "Chine immobilier: contagion systémique imminente", "Wall Street: nœud fragile critique", "Europe bancaire: vulnérabilité contagion", "DeFi crypto: vulnérabilité contagion"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "financial_contagion",
    confidence_score: 0.76,
    data_sources: ["bis_systemic_risk_tracker", "fsb_interconnection_monitor", "imf_financial_stability_report"],
    entities,
    avg_estimated_contagion_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
