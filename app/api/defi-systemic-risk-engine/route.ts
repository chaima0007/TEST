import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[defi-systemic-risk-engine] SWARM_API_URL non défini — mode mock activé");
}

// ── Mock entity type ───────────────────────────────────────────────────────────
type DeFiEntity = {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  protocol_risk_score: number;
  liquidity_risk_score: number;
  contagion_risk_score: number;
  governance_risk_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_defi_index: number;
  last_updated: string;
  domain: string;
};

// ── Mock data ──────────────────────────────────────────────────────────────────
function getMockData(): { entities: DeFiEntity[]; summary: Record<string, unknown> } {
  const entities: DeFiEntity[] = [
    // ── CRITIQUE (3) ────────────────────────────────────────────────────────
    {
      id: "DFI-001",
      name: "VulnSwap Protocol",
      country: "Anonyme",
      sector: "DEX / AMM",
      protocol_risk_score: 92.0,
      liquidity_risk_score: 85.0,
      contagion_risk_score: 88.0,
      governance_risk_score: 80.0,
      composite_score: 86.85,
      risk_level: "critique",
      primary_pattern: "Exploit Protocole Critique",
      key_signals: [
        "Reentrancy bug confirmé audit",
        "$450M TVL à risque immédiat",
        "Dépendances 12 protocoles connectés",
      ],
      estimated_defi_index: 8.69,
      last_updated: "2026-06-20",
      domain: "defi",
    },
    {
      id: "DFI-002",
      name: "TerraClone Finance",
      country: "Corée du Sud",
      sector: "Stablecoin Algorithmique",
      protocol_risk_score: 82.0,
      liquidity_risk_score: 90.0,
      contagion_risk_score: 85.0,
      governance_risk_score: 75.0,
      composite_score: 83.35,
      risk_level: "critique",
      primary_pattern: "Crise Liquidité Systémique",
      key_signals: [
        "Mécanisme ancrage similaire Terra-LUNA",
        "Réserves insuffisantes run bancaire",
        "Contagion pools Curve/Balancer",
      ],
      estimated_defi_index: 8.34,
      last_updated: "2026-06-20",
      domain: "defi",
    },
    {
      id: "DFI-003",
      name: "WhaleDAO Governance",
      country: "Îles Caïmans",
      sector: "Protocole Gouvernance",
      protocol_risk_score: 78.0,
      liquidity_risk_score: 72.0,
      contagion_risk_score: 80.0,
      governance_risk_score: 88.0,
      composite_score: 79.0,
      risk_level: "critique",
      primary_pattern: "Attaque Gouvernance DAO",
      key_signals: [
        "3 baleines = 67% votes",
        "Proposition hostile soumise",
        "Quorum aisément manipulable",
      ],
      estimated_defi_index: 7.9,
      last_updated: "2026-06-20",
      domain: "defi",
    },
    // ── ÉLEVÉ (2) ───────────────────────────────────────────────────────────
    {
      id: "DFI-004",
      name: "CrossChain Bridge Alpha",
      country: "Singapour",
      sector: "Bridge Inter-Chaînes",
      protocol_risk_score: 35.0,
      liquidity_risk_score: 45.0,
      contagion_risk_score: 68.0,
      governance_risk_score: 40.0,
      composite_score: 46.75,
      risk_level: "élevé",
      primary_pattern: "Contagion Inter-Protocoles",
      key_signals: [
        "Bridge historiquement exploité",
        "Validateurs centralisés 5 nœuds",
        "$1.2B locked sans assurance",
      ],
      estimated_defi_index: 4.68,
      last_updated: "2026-06-20",
      domain: "defi",
    },
    {
      id: "DFI-005",
      name: "LeverageFarm Ultra",
      country: "Îles Vierges Britanniques",
      sector: "Yield Farming Levieré",
      protocol_risk_score: 45.0,
      liquidity_risk_score: 55.0,
      contagion_risk_score: 42.0,
      governance_risk_score: 38.0,
      composite_score: 45.35,
      risk_level: "élevé",
      primary_pattern: "Dépeg Stablecoin Partiel",
      key_signals: [
        "Levier 20x positions ouvertes",
        "Oracle Chainlink mono-source",
        "Liquidations en cascade risque",
      ],
      estimated_defi_index: 4.54,
      last_updated: "2026-06-20",
      domain: "defi",
    },
    // ── MODÉRÉ (1) ──────────────────────────────────────────────────────────
    // composite: 42*0.30 + 38*0.25 + 40*0.25 + 35*0.20 = 12.6+9.5+10+7 = 39.1
    {
      id: "DFI-006",
      name: "StableYield Moderate",
      country: "Suisse",
      sector: "Lending Protocol",
      protocol_risk_score: 42.0,
      liquidity_risk_score: 38.0,
      contagion_risk_score: 40.0,
      governance_risk_score: 35.0,
      composite_score: 39.1,
      risk_level: "modéré",
      primary_pattern: "Dépeg Stablecoin Partiel",
      key_signals: [
        "Collatéral excédentaire 150%",
        "Audit Certik récent",
        "Gouvernance multi-sig 5/9",
      ],
      estimated_defi_index: 3.91,
      last_updated: "2026-06-20",
      domain: "defi",
    },
    // ── FAIBLE (2) ──────────────────────────────────────────────────────────
    {
      id: "DFI-007",
      name: "Aave Secure V4",
      country: "Royaume-Uni",
      sector: "Lending Régulé",
      protocol_risk_score: 12.0,
      liquidity_risk_score: 10.0,
      contagion_risk_score: 8.0,
      governance_risk_score: 15.0,
      composite_score: 11.1,
      risk_level: "faible",
      primary_pattern: "Exploit Protocole Critique",
      key_signals: [
        "3 audits majeurs annuels",
        "Circuit breaker automatique",
        "Gouvernance décentralisée réelle",
      ],
      estimated_defi_index: 1.11,
      last_updated: "2026-06-20",
      domain: "defi",
    },
    {
      id: "DFI-008",
      name: "Uniswap Foundation",
      country: "USA",
      sector: "DEX Mature",
      protocol_risk_score: 8.0,
      liquidity_risk_score: 6.0,
      contagion_risk_score: 10.0,
      governance_risk_score: 12.0,
      composite_score: 8.8,
      risk_level: "faible",
      primary_pattern: "Attaque Gouvernance DAO",
      key_signals: [
        "Liquidité $5B+ dispersée",
        "Contrats immutables vérifiés",
        "Gouvernance UNI 300k+ holders",
      ],
      estimated_defi_index: 0.88,
      last_updated: "2026-06-20",
      domain: "defi",
    },
  ];

  const avgComposite = Math.round(
    entities.reduce((acc, e) => acc + e.composite_score, 0) / entities.length * 100
  ) / 100;

  const risk_distribution: Record<string, number> = { critique: 0, "élevé": 0, "modéré": 0, faible: 0 };
  const pattern_distribution: Record<string, number> = {};
  const sector_distribution: Record<string, number> = {};
  const country_distribution: Record<string, number> = {};

  for (const e of entities) {
    risk_distribution[e.risk_level] = (risk_distribution[e.risk_level] || 0) + 1;
    pattern_distribution[e.primary_pattern] = (pattern_distribution[e.primary_pattern] || 0) + 1;
    sector_distribution[e.sector] = (sector_distribution[e.sector] || 0) + 1;
    country_distribution[e.country] = (country_distribution[e.country] || 0) + 1;
  }

  const top_risk_entities = [...entities]
    .sort((a, b) => b.composite_score - a.composite_score)
    .slice(0, 3)
    .map((e) => e.name);

  const summary = {
    total_entities: entities.length,
    avg_composite: avgComposite,
    risk_distribution,
    pattern_distribution,
    top_risk_entities,
    critical_alerts: risk_distribution["critique"],
    last_analysis: "2026-06-20",
    engine_version: "1.0.0",
    domain: "defi",
    confidence_score: 0.91,
    data_sources: [
      "DeFiLlama Protocol Data",
      "Chainalysis On-Chain Analytics",
      "OpenZeppelin Security Audits",
      "Dune Analytics DeFi Metrics",
      "CoinGecko Market Data",
      "DAO Governance Snapshot",
      "Certik Audit Reports",
      "Nansen Wallet Intelligence",
    ],
    entities,
    avg_estimated_defi_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    // Extra distributions for dashboard
    sector_distribution,
    country_distribution,
  };

  return { entities, summary };
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "DeFi Systemic Risk Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/defi-systemic-risk-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "DeFi Systemic Risk Agent")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "DeFi Systemic Risk Agent"),
      { status: 502 }
    ));
  }
}
