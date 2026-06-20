import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[crypto-financial-crime-engine] SWARM_API_URL non défini — mode mock activé");
}

function getMockData() {
  const entities = [
    {
      entity_id: "CRP-001",
      name: "DarkChain Exchange",
      country: "Russie",
      sector: "Exchange Crypto",
      composite_score: 86.85,
      laundering_risk_score: 92.0,
      sanctions_exposure_score: 88.0,
      darknet_flow_score: 85.0,
      traceability_gap_score: 80.0,
      risk_level: "critique",
      primary_pattern: "Blanchiment Crypto Structuré",
      key_signals: [
        "$2.3B transactions sanctionnées OFAC",
        "Mixing automatique tous fonds",
        "Adresses Hydra Market liées",
      ],
      estimated_crypto_index: 8.69,
      last_updated: "2026-06-20",
      watchlist_flag: true,
    },
    {
      entity_id: "CRP-002",
      name: "NovaCoin Broker",
      country: "Émirats Arabes Unis",
      sector: "OTC Crypto",
      composite_score: 80.5,
      laundering_risk_score: 85.0,
      sanctions_exposure_score: 82.0,
      darknet_flow_score: 78.0,
      traceability_gap_score: 75.0,
      risk_level: "critique",
      primary_pattern: "Transaction Entité Sanctionnée",
      key_signals: [
        "Transactions directes entités IRGC",
        "KYC minimal contourné",
        "Portefeuilles multisig opaques",
      ],
      estimated_crypto_index: 8.05,
      last_updated: "2026-06-20",
      watchlist_flag: true,
    },
    {
      entity_id: "CRP-003",
      name: "TorSwap Protocol",
      country: "Anonyme",
      sector: "DEX Anonyme",
      composite_score: 79.8,
      laundering_risk_score: 78.0,
      sanctions_exposure_score: 72.0,
      darknet_flow_score: 88.0,
      traceability_gap_score: 82.0,
      risk_level: "critique",
      primary_pattern: "Flux Marché Darknet",
      key_signals: [
        "Interface Tor exclusive",
        "80% flux darknet tracés",
        "Absence totale AML",
      ],
      estimated_crypto_index: 7.98,
      last_updated: "2026-06-20",
      watchlist_flag: true,
    },
    {
      entity_id: "CRP-004",
      name: "MixMaster Finance",
      country: "Pays-Bas",
      sector: "Mixing Service",
      composite_score: 53.1,
      laundering_risk_score: 55.0,
      sanctions_exposure_score: 48.0,
      darknet_flow_score: 52.0,
      traceability_gap_score: 58.0,
      risk_level: "élevé",
      primary_pattern: "Opacité Mixer Crypto",
      key_signals: [
        "Service tumbling Bitcoin",
        "CoinJoin automatisé",
        "Utilisateurs VPN masqués",
      ],
      estimated_crypto_index: 5.31,
      last_updated: "2026-06-20",
      watchlist_flag: true,
    },
    {
      entity_id: "CRP-005",
      name: "RansomTrack Wallet",
      country: "Ukraine",
      sector: "Portefeuille Crypto",
      composite_score: 56.05,
      laundering_risk_score: 58.0,
      sanctions_exposure_score: 50.0,
      darknet_flow_score: 55.0,
      traceability_gap_score: 62.0,
      risk_level: "élevé",
      primary_pattern: "Paiement Ransomware Détecté",
      key_signals: [
        "Paiements REvil confirmés",
        "Conversion rapide USDT",
        "Dispersion multi-wallets",
      ],
      estimated_crypto_index: 5.61,
      last_updated: "2026-06-20",
      watchlist_flag: true,
    },
    {
      entity_id: "CRP-006",
      name: "GreyZone Trading",
      country: "Malte",
      sector: "Trading Crypto",
      composite_score: 38.85,
      laundering_risk_score: 42.0,
      sanctions_exposure_score: 35.0,
      darknet_flow_score: 38.0,
      traceability_gap_score: 40.0,
      risk_level: "modéré",
      primary_pattern: "Opacité Mixer Crypto",
      key_signals: [
        "KYC partiel implémenté",
        "Transactions suspectes modérées",
        "Conformité AML en cours",
      ],
      estimated_crypto_index: 3.89,
      last_updated: "2026-06-20",
      watchlist_flag: false,
    },
    {
      entity_id: "CRP-007",
      name: "Coinbase Institutional",
      country: "USA",
      sector: "Exchange Régulé",
      composite_score: 8.65,
      laundering_risk_score: 10.0,
      sanctions_exposure_score: 8.0,
      darknet_flow_score: 5.0,
      traceability_gap_score: 12.0,
      risk_level: "faible",
      primary_pattern: "Blanchiment Crypto Structuré",
      key_signals: [
        "Licence BitLicense NY",
        "OFAC screening temps réel",
        "Chainalysis intégré",
      ],
      estimated_crypto_index: 0.87,
      last_updated: "2026-06-20",
      watchlist_flag: false,
    },
    {
      entity_id: "CRP-008",
      name: "Kraken Europe MiCA",
      country: "Irlande",
      sector: "Exchange Régulé",
      composite_score: 6.9,
      laundering_risk_score: 8.0,
      sanctions_exposure_score: 6.0,
      darknet_flow_score: 4.0,
      traceability_gap_score: 10.0,
      risk_level: "faible",
      primary_pattern: "Transaction Entité Sanctionnée",
      key_signals: [
        "Conformité MiCA certifiée",
        "AML niveau bancaire",
        "Reporting automatique AMLA",
      ],
      estimated_crypto_index: 0.69,
      last_updated: "2026-06-20",
      watchlist_flag: false,
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 51.34,
    risk_distribution: {
      critique: 3,
      "élevé": 2,
      "modéré": 1,
      faible: 2,
    },
    pattern_distribution: {
      "Blanchiment Crypto Structuré": 2,
      "Transaction Entité Sanctionnée": 2,
      "Flux Marché Darknet": 1,
      "Opacité Mixer Crypto": 2,
      "Paiement Ransomware Détecté": 1,
    },
    top_risk_entities: ["DarkChain Exchange", "NovaCoin Broker", "TorSwap Protocol"],
    critical_alerts: 3,
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "crypto",
    confidence_score: 0.91,
    data_sources: [
      "OFAC SDN List",
      "Chainalysis Reactor",
      "Europol EC3 Darknet Reports",
      "TRACFIN Intelligence",
      "CipherTrace AML",
    ],
    entities,
    avg_estimated_crypto_index: 5.13,
  };

  return { entities, summary };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Crypto Financial Crime Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/crypto-financial-crime-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Crypto Financial Crime Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Crypto Financial Crime Agent"), { status: 502 });
  }
}
