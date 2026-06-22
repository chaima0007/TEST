import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[crypto-financial-crime-engine] SWARM_API_URL non défini — mode mock activé");
}

const MOCK_ENTITIES = [
  {
    id: "CRY-001",
    name: "DarkChain Exchange",
    country: "Russie",
    sector: "Exchange Crypto Non Régulé",
    composite_score: 86.65,
    laundering_risk_score: 90.0,
    fraud_score: 85.0,
    sanctions_evasion_score: 88.0,
    aml_compliance_gap: 82.0,
    risk_level: "critique",
    primary_pattern: "Évasion Sanctions Cryptographiques",
    key_signals: [
      "12,000 wallets OFAC sanctionnés détectés comme actifs",
      "Volume mixer $850M en 6 mois — Tornado Cash dérivé",
      "Absence totale de procédures KYC/AML",
    ],
    estimated_crypto_index: 8.67,
    last_updated: "2026-06-20",
  },
  {
    id: "CRY-002",
    name: "CryptoHaven Protocol",
    country: "Îles Caïmans",
    sector: "Protocole Mixage Crypto",
    composite_score: 83.75,
    laundering_risk_score: 88.0,
    fraud_score: 82.0,
    sanctions_evasion_score: 85.0,
    aml_compliance_gap: 78.0,
    risk_level: "critique",
    primary_pattern: "Blanchiment Crypto Massif",
    key_signals: [
      "Service mixer $2.1B en flux anonymisés détectés",
      "Liens avec groupe ransomware Lazarus confirmés",
      "Opération sur 47 juridictions sans licences",
    ],
    estimated_crypto_index: 8.38,
    last_updated: "2026-06-19",
  },
  {
    id: "CRY-003",
    name: "NovaCoin Darknet",
    country: "Corée du Nord",
    sector: "Marché Darknet Crypto",
    composite_score: 78.5,
    laundering_risk_score: 82.0,
    fraud_score: 78.0,
    sanctions_evasion_score: 80.0,
    aml_compliance_gap: 72.0,
    risk_level: "critique",
    primary_pattern: "Évasion Sanctions Cryptographiques",
    key_signals: [
      "Financement programme nucléaire via crypto confirmé par ONU",
      "Attaques Lazarus Group — $620M Axie Infinity récupérés",
      "Utilisation chaînes obscurcissement multi-couches",
    ],
    estimated_crypto_index: 7.85,
    last_updated: "2026-06-18",
  },
  {
    id: "CRY-004",
    name: "QuickSwap DeFi",
    country: "Singapour",
    sector: "Protocole DeFi",
    composite_score: 60.25,
    laundering_risk_score: 60.0,
    fraud_score: 62.0,
    sanctions_evasion_score: 55.0,
    aml_compliance_gap: 65.0,
    risk_level: "élevé",
    primary_pattern: "Fraude DeFi & Rug Pull",
    key_signals: [
      "Draineur liquidité détecté — $45M en pool USDC/ETH",
      "Équipe anonyme — aucune identité vérifiable",
      "Smart contract non audité avec backdoor admin",
    ],
    estimated_crypto_index: 6.03,
    last_updated: "2026-06-17",
  },
  {
    id: "CRY-005",
    name: "CryptoVault Exchange",
    country: "Malaisie",
    sector: "Exchange Crypto Semi-Régulé",
    composite_score: 56.55,
    laundering_risk_score: 58.0,
    fraud_score: 55.0,
    sanctions_evasion_score: 60.0,
    aml_compliance_gap: 52.0,
    risk_level: "élevé",
    primary_pattern: "Vide AML Plateforme Crypto",
    key_signals: [
      "KYC effectué pour seulement 28% des comptes actifs",
      "Transactions suspectes non signalées > $500k",
      "Flux crypto vers wallets russes non bloqués",
    ],
    estimated_crypto_index: 5.66,
    last_updated: "2026-06-16",
  },
  {
    id: "CRY-006",
    name: "AltCoin Market EU",
    country: "Malte",
    sector: "Exchange Crypto Régulé MiCA",
    composite_score: 35.75,
    laundering_risk_score: 38.0,
    fraud_score: 35.0,
    sanctions_evasion_score: 40.0,
    aml_compliance_gap: 28.0,
    risk_level: "modéré",
    primary_pattern: "Manipulation Marché Crypto",
    key_signals: [
      "Indicateurs wash trading sur paires BTC/EUR à 34%",
      "Conformité MiCA partielle — 72% des exigences satisfaites",
      "Signalement TRACFIN en cours pour 3 comptes VIP",
    ],
    estimated_crypto_index: 3.58,
    last_updated: "2026-06-15",
  },
  {
    id: "CRY-007",
    name: "SwissBlock Custody",
    country: "Suisse",
    sector: "Custody & Banque Crypto",
    composite_score: 10.2,
    laundering_risk_score: 10.0,
    fraud_score: 12.0,
    sanctions_evasion_score: 8.0,
    aml_compliance_gap: 11.0,
    risk_level: "faible",
    primary_pattern: "Manipulation Marché Crypto",
    key_signals: [
      "FINMA agréé — conformité AML 98% vérifiée",
      "KYC renforcé avec vérification biométrique",
      "Zéro transaction vers wallets sanctionnés depuis 18 mois",
    ],
    estimated_crypto_index: 1.02,
    last_updated: "2026-06-14",
  },
  {
    id: "CRY-008",
    name: "EUROCoin Regulated Exchange",
    country: "France",
    sector: "Exchange Crypto Régulé PSAN",
    composite_score: 9.55,
    laundering_risk_score: 8.0,
    fraud_score: 10.0,
    sanctions_evasion_score: 9.0,
    aml_compliance_gap: 12.0,
    risk_level: "faible",
    primary_pattern: "Vide AML Plateforme Crypto",
    key_signals: [
      "PSAN enregistré AMF — conformité totale AMLD6",
      "Monitoring temps réel toutes transactions > 1000€",
      "Rapport TRACFIN trimestriel transmis sans anomalie",
    ],
    estimated_crypto_index: 0.96,
    last_updated: "2026-06-13",
  },
];

function getMockData() {
  const entities = MOCK_ENTITIES;
  const n = entities.length;
  const avgComposite =
    Math.round((entities.reduce((s, e) => s + e.composite_score, 0) / n) * 100) / 100;

  const riskDistribution: Record<string, number> = { critique: 0, élevé: 0, modéré: 0, faible: 0 };
  const patternDistribution: Record<string, number> = {};

  for (const e of entities) {
    riskDistribution[e.risk_level] = (riskDistribution[e.risk_level] || 0) + 1;
    patternDistribution[e.primary_pattern] = (patternDistribution[e.primary_pattern] || 0) + 1;
  }

  const sorted = [...entities].sort((a, b) => b.composite_score - a.composite_score);
  const topRiskEntities = sorted.slice(0, 3).map((e) => e.name);
  const criticalAlerts = entities
    .filter((e) => e.risk_level === "critique")
    .map((e) => `${e.name} (${e.country}) — composite ${e.composite_score}`);

  const summary = {
    total_entities: n,
    avg_composite: avgComposite,
    risk_distribution: riskDistribution,
    pattern_distribution: patternDistribution,
    top_risk_entities: topRiskEntities,
    critical_alerts: criticalAlerts,
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "crypto",
    confidence_score: 0.92,
    data_sources: [
      "Chainalysis Reactor Intelligence",
      "Elliptic Forensics Database",
      "FATF Crypto Risk Reports",
      "OFAC Sanctions Blockchain Monitor",
      "Europol Financial Intelligence Unit",
    ],
    entities,
    avg_estimated_crypto_index: Math.round((avgComposite / 100) * 10 * 100) / 100,
  };

  return { entities, summary };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Crypto Financial Crime Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/crypto-financial-crime-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Crypto Financial Crime Agent")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "Crypto Financial Crime Agent"),
      { status: 502 }
    ));
  }
}
