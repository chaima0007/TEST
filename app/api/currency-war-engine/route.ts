import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[currency-war-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Currency War Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/currency-war-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Currency War Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Currency War Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "CW-001", name: "Chine — e-CNY & Pétro-Yuan BRICS Dé-Dollarisation", country: "Asie", sector: "e-CNY 260Md$ Testé, Accord Pétro-Yuan Arabie/Russie, CIPS 103 Pays & BRICS Monnaie Commune", composite_score: 90.35, dedollarization_strategy_score: 92.0, currency_manipulation_score: 88.0, cbdc_geopolitical_score: 95.0, gold_reserve_weaponization_score: 85.0, risk_level: "critique", primary_pattern: "dedollarisation_systemique", key_signals: ["Dé-dollarisation active par Chine — stratégie monétaire offensive visant à réduire l'hégémonie du dollar dans les échanges internationaux", "Construction d'alternatives monétaires — CBDC géopolitiques, yuan pétrolier, accord BRICS et réserves d'or hors-dollar", "Fragmentation du système monétaire mondial — émergence de blocs monétaires incompatibles et fin du dollar comme monnaie de réserve unique"], estimated_currency_war_index: 9.04, last_updated: "2026-06-20" },
    { id: "CW-002", name: "Russie — Réserves Or 70% & SWIFT Alternatif MIR", country: "Europe de l'Est", sector: "Or 2355 Tonnes Réserves, Système MIR 90 Pays, SPFS SWIFT Alternatif & Yuanisation Échanges", composite_score: 86.05, dedollarization_strategy_score: 88.0, currency_manipulation_score: 85.0, cbdc_geopolitical_score: 80.0, gold_reserve_weaponization_score: 92.0, risk_level: "critique", primary_pattern: "or_comme_arme_monetaire", key_signals: ["Dé-dollarisation active par Russie — stratégie monétaire offensive visant à réduire l'hégémonie du dollar dans les échanges internationaux", "Construction d'alternatives monétaires — CBDC géopolitiques, yuan pétrolier, accord BRICS et réserves d'or hors-dollar", "Fragmentation du système monétaire mondial — émergence de blocs monétaires incompatibles et fin du dollar comme monnaie de réserve unique"], estimated_currency_war_index: 8.61, last_updated: "2026-06-20" },
    { id: "CW-003", name: "Arabie Saoudite — Pétrodollar & Diversification BRICS", country: "MENA", sector: "Ventes Pétrole en Yuan Négociées, BRICS+ Membership 2024 & Réserves Or en Augmentation", composite_score: 79.85, dedollarization_strategy_score: 82.0, currency_manipulation_score: 78.0, cbdc_geopolitical_score: 75.0, gold_reserve_weaponization_score: 85.0, risk_level: "critique", primary_pattern: "or_comme_arme_monetaire", key_signals: ["Dé-dollarisation active par Arabie Saoudite — stratégie monétaire offensive visant à réduire l'hégémonie du dollar dans les échanges internationaux", "Construction d'alternatives monétaires — CBDC géopolitiques, yuan pétrolier, accord BRICS et réserves d'or hors-dollar", "Fragmentation du système monétaire mondial — émergence de blocs monétaires incompatibles et fin du dollar comme monnaie de réserve unique"], estimated_currency_war_index: 7.99, last_updated: "2026-06-20" },
    { id: "CW-004", name: "Inde — Rupee Internationalisation & BRICS+", country: "Asie du Sud", sector: "Pétrole Russe en Roupies, Accords Swap Bilatéraux 22 Pays & UPI System International", composite_score: 74.9, dedollarization_strategy_score: 78.0, currency_manipulation_score: 72.0, cbdc_geopolitical_score: 70.0, gold_reserve_weaponization_score: 80.0, risk_level: "critique", primary_pattern: "guerre_monetaire_regionale", key_signals: ["Dé-dollarisation active par Inde — stratégie monétaire offensive visant à réduire l'hégémonie du dollar dans les échanges internationaux", "Construction d'alternatives monétaires — CBDC géopolitiques, yuan pétrolier, accord BRICS et réserves d'or hors-dollar", "Fragmentation du système monétaire mondial — émergence de blocs monétaires incompatibles et fin du dollar comme monnaie de réserve unique"], estimated_currency_war_index: 7.49, last_updated: "2026-06-20" },
    { id: "CW-005", name: "Turquie — Livre & Indépendance Monétaire Erdoğan", country: "MENA/Europe", sector: "Dévaluation Délibérée Livre, Réserves Or Achat Massif & Swap Chine/Qatar Sans Dollar", composite_score: 55.15, dedollarization_strategy_score: 55.0, currency_manipulation_score: 65.0, cbdc_geopolitical_score: 48.0, gold_reserve_weaponization_score: 52.0, risk_level: "élevé", primary_pattern: "guerre_monetaire_regionale", key_signals: ["Guerre monétaire régionale par Turquie — manœuvres actives pour réduire la dépendance au dollar dans les échanges bilatéraux", "Accords de swap bilatéraux — transactions en monnaies locales contournant SWIFT et les sanctions américaines", "Instabilité monétaire — volatilité des taux de change alimentée par des politiques monétaires à visée géopolitique"], estimated_currency_war_index: 5.52, last_updated: "2026-06-20" },
    { id: "CW-006", name: "Iran & BRICS — Économies Sanctionnées Hors-Dollar", country: "MENA", sector: "Troc Pétrole-Marchandises, Crypto-Rial Envisagé & Commerce Bilatéral Yuan/Rouble/Roupie", composite_score: 53.45, dedollarization_strategy_score: 52.0, currency_manipulation_score: 58.0, cbdc_geopolitical_score: 55.0, gold_reserve_weaponization_score: 48.0, risk_level: "élevé", primary_pattern: "guerre_monetaire_regionale", key_signals: ["Guerre monétaire régionale par Iran & BRICS — manœuvres actives pour réduire la dépendance au dollar dans les échanges bilatéraux", "Accords de swap bilatéraux — transactions en monnaies locales contournant SWIFT et les sanctions américaines", "Instabilité monétaire — volatilité des taux de change alimentée par des politiques monétaires à visée géopolitique"], estimated_currency_war_index: 5.35, last_updated: "2026-06-20" },
    { id: "CW-007", name: "UE — Euro Digital & Souveraineté Monétaire Défensive", country: "Europe", sector: "Digital Euro BCE Projet Pilote, Réforme SWIFT Européen & Instruments Anti-Coercition Monétaire", composite_score: 28.55, dedollarization_strategy_score: 28.0, currency_manipulation_score: 25.0, cbdc_geopolitical_score: 38.0, gold_reserve_weaponization_score: 22.0, risk_level: "modéré", primary_pattern: "guerre_monetaire_regionale", key_signals: ["Souveraineté monétaire défensive de UE — mesures de protection sans stratégie offensive de dé-dollarisation", "Dépendance aux conditions financières mondiales — exposition aux décisions de la Fed et aux flux de capitaux spéculatifs", "CBDC défensive en développement — euro numérique ou monnaie digitale nationale pour préserver la souveraineté monétaire"], estimated_currency_war_index: 2.86, last_updated: "2026-06-20" },
    { id: "CW-008", name: "FMI & Dollar — Stabilité Monétaire Multilatérale", country: "Global", sector: "DTS 650Md$ Allocation Covid, Surveillance Articles IV & Prêteur Dernier Ressort Mondial", composite_score: 4.45, dedollarization_strategy_score: 5.0, currency_manipulation_score: 4.0, cbdc_geopolitical_score: 3.0, gold_reserve_weaponization_score: 6.0, risk_level: "faible", primary_pattern: "stabilite_monetaire_cooperative", key_signals: ["FMI & Dollar soutient la stabilité monétaire multilatérale — coopération FMI, droits de tirage spéciaux et transparence des réserves", "Architecture de Bretton Woods renforcée — maintien du dollar comme ancre de stabilité et coordination des politiques monétaires G20", "Modèle de gouvernance monétaire à préserver — FMI réformé, surveillance des taux de change et mécanismes de prévention des crises"], estimated_currency_war_index: 0.45, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { dedollarisation_systemique: 1, or_comme_arme_monetaire: 2, manipulation_monetaire_offensive: 0, guerre_monetaire_regionale: 4, stabilite_monetaire_cooperative: 1 },
    top_risk_entities: ["Chine — e-CNY & Pétro-Yuan BRICS Dé-Dollarisation", "Russie — Réserves Or 70% & SWIFT Alternatif MIR", "Arabie Saoudite — Pétrodollar & Diversification BRICS"],
    critical_alerts: ["Chine: dédollarisation systémique", "Russie: or comme arme monétaire", "Arabie Saoudite: or comme arme monétaire", "Inde: guerre monétaire régionale"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "currency_war",
    confidence_score: 0.79,
    data_sources: ["bis_currency_report", "imf_reserve_currency_monitor", "atlantic_council_geoeconomics"],
    entities,
    avg_estimated_currency_war_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
