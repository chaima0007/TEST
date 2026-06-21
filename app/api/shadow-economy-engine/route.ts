import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[shadow-economy-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Shadow Economy Engine Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/shadow-economy-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Shadow Economy Engine Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Shadow Economy Engine Agent"), { status: 502 });
  }
}

function getMockData() {
  const entities = [
    { id: "SE-001", name: "Afrique Subsaharienne Moyenne", country: "Afrique", sector: "Informalité Structurelle >60% PIB", composite_score: 86.75, informal_sector_dominance_score: 90.0, tax_evasion_systemic_score: 85.0, corruption_lubricant_score: 88.0, regulatory_arbitrage_score: 82.0, risk_level: "critique", primary_pattern: "economie_parallele_totale", key_signals: ["Économie parallèle totale dans Afrique Subsaharienne — secteur informel dominant l'économie réelle", "Corruption structurelle comme lubrifiant indispensable des transactions économiques", "Divorce État-économie — administration fiscale contournée à grande échelle"], estimated_shadow_index: 8.68, last_updated: "2026-06-20" },
    { id: "SE-002", name: "Myanmar & Cambodge", country: "Asie du Sud-Est", sector: "Économie Grise & Trafics Légalisés", composite_score: 83.25, informal_sector_dominance_score: 85.0, tax_evasion_systemic_score: 80.0, corruption_lubricant_score: 88.0, regulatory_arbitrage_score: 78.0, risk_level: "critique", primary_pattern: "economie_parallele_totale", key_signals: ["Économie parallèle totale dans Myanmar & Cambodge — secteur informel dominant l'économie réelle", "Corruption structurelle comme lubrifiant indispensable des transactions économiques", "Divorce État-économie — administration fiscale contournée à grande échelle"], estimated_shadow_index: 8.33, last_updated: "2026-06-20" },
    { id: "SE-003", name: "Venezuela & Bolivie", country: "Amériques", sector: "Marché Noir Structurant l'Économie", composite_score: 81.75, informal_sector_dominance_score: 82.0, tax_evasion_systemic_score: 85.0, corruption_lubricant_score: 80.0, regulatory_arbitrage_score: 75.0, risk_level: "critique", primary_pattern: "economie_parallele_totale", key_signals: ["Économie parallèle totale dans Venezuela & Bolivie — secteur informel dominant l'économie réelle", "Corruption structurelle comme lubrifiant indispensable des transactions économiques", "Divorce État-économie — administration fiscale contournée à grande échelle"], estimated_shadow_index: 8.18, last_updated: "2026-06-20" },
    { id: "SE-004", name: "Nigeria & Cameroun", country: "Afrique", sector: "Informalité Commerciale Totale", composite_score: 78.75, informal_sector_dominance_score: 80.0, tax_evasion_systemic_score: 78.0, corruption_lubricant_score: 82.0, regulatory_arbitrage_score: 72.0, risk_level: "critique", primary_pattern: "economie_parallele_totale", key_signals: ["Économie parallèle totale dans Nigeria & Cameroun — secteur informel dominant l'économie réelle", "Corruption structurelle comme lubrifiant indispensable des transactions économiques", "Divorce État-économie — administration fiscale contournée à grande échelle"], estimated_shadow_index: 7.88, last_updated: "2026-06-20" },
    { id: "SE-005", name: "Mexique — Économie Cartel", country: "Amériques", sector: "Pénétration Criminelle des Marchés", composite_score: 64.0, informal_sector_dominance_score: 65.0, tax_evasion_systemic_score: 62.0, corruption_lubricant_score: 68.0, regulatory_arbitrage_score: 60.0, risk_level: "élevé", primary_pattern: "evasion_systemique", key_signals: ["Dualisme économique avancé dans Mexique — deux économies coexistant sans convergence", "Évasion fiscale systémique compromettant les finances publiques", "Arbitrage réglementaire structurel — acteurs économiques évitant le cadre formel"], estimated_shadow_index: 6.4, last_updated: "2026-06-20" },
    { id: "SE-006", name: "Russie Post-Soviétique", country: "Europe de l'Est", sector: "Oligarchie & Évasion Structurelle", composite_score: 56.0, informal_sector_dominance_score: 55.0, tax_evasion_systemic_score: 58.0, corruption_lubricant_score: 60.0, regulatory_arbitrage_score: 52.0, risk_level: "élevé", primary_pattern: "dualisme_economique", key_signals: ["Dualisme économique avancé dans Russie — deux économies coexistant sans convergence", "Évasion fiscale systémique compromettant les finances publiques", "Arbitrage réglementaire structurel — acteurs économiques évitant le cadre formel"], estimated_shadow_index: 5.6, last_updated: "2026-06-20" },
    { id: "SE-007", name: "Italie du Sud & Grèce", country: "Europe", sector: "Économie Grise Méditerranéenne", composite_score: 37.25, informal_sector_dominance_score: 38.0, tax_evasion_systemic_score: 42.0, corruption_lubricant_score: 35.0, regulatory_arbitrage_score: 30.0, risk_level: "modéré", primary_pattern: "tensions_formelles", key_signals: ["Secteur informel significatif dans Italie du Sud & Grèce — tensions entre formalité et informalité", "Évasion fiscale partielle — réformes simplificatrices nécessaires", "Barrières à la formalisation à réduire pour intégrer l'économie parallèle"], estimated_shadow_index: 3.73, last_updated: "2026-06-20" },
    { id: "SE-008", name: "Suisse & Pays-Bas", country: "Europe du Nord", sector: "Économie Formelle Exemplaire", composite_score: 9.25, informal_sector_dominance_score: 10.0, tax_evasion_systemic_score: 8.0, corruption_lubricant_score: 6.0, regulatory_arbitrage_score: 12.0, risk_level: "faible", primary_pattern: "economie_formelle", key_signals: ["Suisse & Pays-Bas maintient une économie formelle dominante — compliance fiscale élevée", "Administration fiscale efficace et barrières à la formalisation basses", "Modèle de gouvernance économique à préserver et exporter"], estimated_shadow_index: 0.93, last_updated: "2026-06-20" },
  ];

  const avg = Math.round(entities.reduce((s, e) => s + e.composite_score, 0) / entities.length * 100) / 100;
  return {
    total_entities: 8,
    avg_composite: avg,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: { economie_parallele_totale: 4, evasion_systemique: 1, dualisme_economique: 1, tensions_formelles: 1, economie_formelle: 1 },
    top_risk_entities: ["Afrique Subsaharienne Moyenne", "Myanmar & Cambodge", "Venezuela & Bolivie"],
    critical_alerts: ["Afrique Subsaharienne: économie parallèle totale", "Myanmar & Cambodge: économie parallèle totale", "Venezuela & Bolivie: économie parallèle totale", "Nigeria & Cameroun: économie parallèle totale"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "shadow_econ",
    confidence_score: 0.72,
    data_sources: ["ilo_informal_economy", "world_bank_informality", "tax_justice_network"],
    entities,
    avg_estimated_shadow_index: Math.round(avg / 100 * 10 * 100) / 100,
  };
}
