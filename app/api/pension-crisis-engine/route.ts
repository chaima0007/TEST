import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[pension-crisis-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Pension Crisis Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/pension-crisis-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Pension Crisis Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Pension Crisis Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { entity_id: "PC-001", name: "Japon — Archipel du Vieillissement", country: "Asie", sector: "30% de 65+ — Ratio Actifs/Retraités en Effondrement Structurel", composite_score: 84.9, demographic_pressure_score: 95.0, funding_gap_score: 88.0, intergenerational_conflict_score: 80.0, reform_political_resistance_score: 72.0, risk_level: "critique", primary_pattern: "insolvabilite_systemique", key_signals: ["Crise de solvabilité des retraites dans Japon — déficits actuariels insoutenables sans réforme immédiate", "Bombe démographique — ratio actifs/retraités en chute libre, financement par répartition insoutenable", "Conflit intergénérationnel latent — jeunes actifs subventionnant des retraites promises non-financées"], estimated_pension_crisis_index: 8.49, last_updated: "2026-06-20" },
    { entity_id: "PC-002", name: "Italie & Grèce — Europe du Sud Sous Pression", country: "Europe", sector: "Retraites 16% PIB — Réformes Bloquées par Résistance Syndicale", composite_score: 83.1, demographic_pressure_score: 85.0, funding_gap_score: 82.0, intergenerational_conflict_score: 78.0, reform_political_resistance_score: 88.0, risk_level: "critique", primary_pattern: "insolvabilite_systemique", key_signals: ["Crise de solvabilité des retraites dans Italie & Grèce — déficits actuariels insoutenables sans réforme immédiate", "Bombe démographique — ratio actifs/retraités en chute libre, financement par répartition insoutenable", "Conflit intergénérationnel latent — jeunes actifs subventionnant des retraites promises non-financées"], estimated_pension_crisis_index: 8.31, last_updated: "2026-06-20" },
    { entity_id: "PC-003", name: "Chine — Vieillissement Post-Enfant Unique", country: "Asie", sector: "Politique Enfant Unique — Bombe Démographique Actuarielle à Retardement", composite_score: 75.85, demographic_pressure_score: 82.0, funding_gap_score: 78.0, intergenerational_conflict_score: 75.0, reform_political_resistance_score: 65.0, risk_level: "critique", primary_pattern: "insolvabilite_systemique", key_signals: ["Crise de solvabilité des retraites dans Chine — déficits actuariels insoutenables sans réforme immédiate", "Bombe démographique — ratio actifs/retraités en chute libre, financement par répartition insoutenable", "Conflit intergénérationnel latent — jeunes actifs subventionnant des retraites promises non-financées"], estimated_pension_crisis_index: 7.59, last_updated: "2026-06-20" },
    { entity_id: "PC-004", name: "France — Conflit Générationnel Retraites", country: "Europe", sector: "Réforme 64 ans 2023 — Crise Sociale & Légitimité Démocratique Fragilisée", composite_score: 76.1, demographic_pressure_score: 70.0, funding_gap_score: 65.0, intergenerational_conflict_score: 85.0, reform_political_resistance_score: 88.0, risk_level: "critique", primary_pattern: "bombe_intergenerationnelle", key_signals: ["Crise de solvabilité des retraites dans France — déficits actuariels insoutenables sans réforme immédiate", "Bombe démographique — ratio actifs/retraités en chute libre, financement par répartition insoutenable", "Conflit intergénérationnel latent — jeunes actifs subventionnant des retraites promises non-financées"], estimated_pension_crisis_index: 7.61, last_updated: "2026-06-20" },
    { entity_id: "PC-005", name: "USA — Fonds Publics Locaux Déficitaires", country: "Amérique du Nord", sector: "Pensions Illinois/New Jersey — Déficits Actuariels Multi-Milliards $", composite_score: 58.25, demographic_pressure_score: 55.0, funding_gap_score: 68.0, intergenerational_conflict_score: 55.0, reform_political_resistance_score: 55.0, risk_level: "élevé", primary_pattern: "pression_fiscale_critique", key_signals: ["Pression retraite sévère dans USA — déficits des fonds de pension nécessitant réformes urgentes", "Dépenses retraite dévorant le budget — arbitrages défavorables pour éducation et infrastructure", "Résistance politique aux réformes — syndicats et partis bloquant les ajustements nécessaires"], estimated_pension_crisis_index: 5.83, last_updated: "2026-06-20" },
    { entity_id: "PC-006", name: "Russie — Réforme 2018 & Impopularité", country: "Europe de l'Est", sector: "Âge Retraite Relevé à 60/65 ans — Résistance Populaire & Fragilité Sociale", composite_score: 51.35, demographic_pressure_score: 52.0, funding_gap_score: 52.0, intergenerational_conflict_score: 55.0, reform_political_resistance_score: 45.0, risk_level: "élevé", primary_pattern: "pression_fiscale_critique", key_signals: ["Pression retraite sévère dans Russie — déficits des fonds de pension nécessitant réformes urgentes", "Dépenses retraite dévorant le budget — arbitrages défavorables pour éducation et infrastructure", "Résistance politique aux réformes — syndicats et partis bloquant les ajustements nécessaires"], estimated_pension_crisis_index: 5.14, last_updated: "2026-06-20" },
    { entity_id: "PC-007", name: "Brésil & Argentine — Retraites & Populisme", country: "Amériques", sector: "Systèmes par Répartition Déséquilibrés — Clientélisme et Déficits Chroniques", composite_score: 33.45, demographic_pressure_score: 32.0, funding_gap_score: 38.0, intergenerational_conflict_score: 35.0, reform_political_resistance_score: 28.0, risk_level: "modéré", primary_pattern: "ajustement_douloureux", key_signals: ["Tensions retraite gérables dans Brésil & Argentine — ajustements nécessaires mais marge de manœuvre existante", "Pression démographique croissante — vieillissement accélérant les déséquilibres actuariels", "Réformes paramétriques en discussion — âge de départ, taux de cotisation et conditions d'indexation"], estimated_pension_crisis_index: 3.35, last_updated: "2026-06-20" },
    { entity_id: "PC-008", name: "Scandinavie — Modèles NDC Réformés", country: "Europe du Nord", sector: "Systèmes à Comptes Notionnels — Durabilité Actuarielle Garantie", composite_score: 10.0, demographic_pressure_score: 15.0, funding_gap_score: 10.0, intergenerational_conflict_score: 8.0, reform_political_resistance_score: 5.0, risk_level: "faible", primary_pattern: "equilibre_soutenable", key_signals: ["Scandinavie maintient un système de retraite soutenable — réformes préventives réussies et démographie maîtrisée", "Fonds de pension bien capitalisés et mix répartition-capitalisation équilibré", "Modèle de durabilité retraite à partager — gouvernance actuarielle transparente et adaptation continue"], estimated_pension_crisis_index: 1.0, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { insolvabilite_systemique: 3, bombe_intergenerationnelle: 1, pression_fiscale_critique: 2, ajustement_douloureux: 1, equilibre_soutenable: 1 },
    top_risk_entities: ["Japon — Archipel du Vieillissement", "France — Conflit Générationnel Retraites", "Italie & Grèce — Europe du Sud Sous Pression"],
    critical_alerts: ["Japon: insolvabilité systémique", "Italie & Grèce: insolvabilité systémique", "Chine: insolvabilité systémique", "France: bombe intergénérationnelle"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "pension_crisis",
    confidence_score: 0.89,
    data_sources: ["oecd_pension_outlook", "imf_fiscal_monitor_pensions", "mercer_melbourne_global_pension_index"],
    entities,
    avg_estimated_pension_crisis_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
