import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockTerritories = [
  {
    territory_id: "t_001",
    territory_name: "Enterprise DACH",
    region: "emea",
    rep_name: "Sophie Müller",
    territory_health: "optimal",
    territory_action: "maintain",
    coverage_risk: "low",
    balance_score: 87.0,
    quota_attainment_pct: 112.5,
    pipeline_coverage_ratio: 3.8,
    white_space_pct: 8.0,
    strengths: [
      "Couverture pipeline excellente — 3.8x le quota",
      "Atteinte quota à 113% — performance commerciale au niveau",
      "Santé comptes élevée (82/100) — portefeuille stable",
      "Excellent taux de pénétration — seulement 8% de comptes vierges",
      "Cadence QBR forte — 78% des comptes suivis",
      "Rep expérimentée — 24 mois sur le territoire, connaissance approfondie",
    ],
    gaps: [],
    recommendations: [
      "Documenter les meilleures pratiques — territoire modèle à partager",
      "Planifier des QBRs pour les comptes sans revue depuis 90j+",
    ],
    territory_kpis: {
      pipeline_coverage_ratio: 3.8,
      quota_attainment_pct: 112.5,
      white_space_pct: 8.0,
      active_account_pct: 88.0,
      avg_account_health: 82.0,
      qbr_coverage_pct: 78.0,
      market_penetration_pct: 42.0,
      deals_in_flight: 12,
      accounts_at_risk: 2,
      closed_won_ytd_eur: 285000,
    },
  },
  {
    territory_id: "t_002",
    territory_name: "Mid-Market Benelux",
    region: "emea",
    rep_name: "Lucas Dubois",
    territory_health: "optimal",
    territory_action: "maintain",
    coverage_risk: "low",
    balance_score: 81.5,
    quota_attainment_pct: 98.0,
    pipeline_coverage_ratio: 3.2,
    white_space_pct: 12.0,
    strengths: [
      "Couverture pipeline excellente — 3.2x le quota",
      "Progression quota solide — 98% d'atteinte",
      "Santé comptes élevée (75/100) — portefeuille stable",
      "Cadence QBR forte — 72% des comptes suivis",
    ],
    gaps: [],
    recommendations: [
      "Accélérer pour franchir les 100% de quota avant fin de trimestre",
      "Lancer une campagne de prospection sur les 12% de comptes vierges",
    ],
    territory_kpis: {
      pipeline_coverage_ratio: 3.2,
      quota_attainment_pct: 98.0,
      white_space_pct: 12.0,
      active_account_pct: 82.0,
      avg_account_health: 75.0,
      qbr_coverage_pct: 72.0,
      market_penetration_pct: 35.0,
      deals_in_flight: 9,
      accounts_at_risk: 1,
      closed_won_ytd_eur: 210000,
    },
  },
  {
    territory_id: "t_003",
    territory_name: "Enterprise France",
    region: "emea",
    rep_name: "Marie Fontaine",
    territory_health: "balanced",
    territory_action: "maintain",
    coverage_risk: "medium",
    balance_score: 66.0,
    quota_attainment_pct: 79.0,
    pipeline_coverage_ratio: 2.4,
    white_space_pct: 22.0,
    strengths: [
      "Bonne couverture pipeline — 2.4x le quota",
      "Progression quota solide — 79% d'atteinte",
    ],
    gaps: [
      "22% de comptes non couverts — potentiel commercial inexploité",
      "Cadence QBR faible (45%) — risque de décrochage clients",
    ],
    recommendations: [
      "Lancer une campagne de prospection sur les comptes vierges",
      "Planifier des QBRs pour les comptes sans revue depuis 90j+",
      "Accélérer la génération pipeline — objectif couverture 3x quota",
    ],
    territory_kpis: {
      pipeline_coverage_ratio: 2.4,
      quota_attainment_pct: 79.0,
      white_space_pct: 22.0,
      active_account_pct: 74.0,
      avg_account_health: 68.0,
      qbr_coverage_pct: 45.0,
      market_penetration_pct: 28.0,
      deals_in_flight: 7,
      accounts_at_risk: 3,
      closed_won_ytd_eur: 158000,
    },
  },
  {
    territory_id: "t_004",
    territory_name: "SMB UK & Ireland",
    region: "emea",
    rep_name: "James O'Brien",
    territory_health: "balanced",
    territory_action: "rebalance",
    coverage_risk: "high",
    balance_score: 60.5,
    quota_attainment_pct: 85.0,
    pipeline_coverage_ratio: 2.8,
    white_space_pct: 28.0,
    strengths: [
      "Bonne couverture pipeline — 2.8x le quota",
      "Progression quota solide — 85% d'atteinte",
    ],
    gaps: [
      "28% de comptes non couverts — potentiel commercial inexploité",
      "Cadence QBR faible (38%) — risque de décrochage clients",
      "4 comptes à risque — ARR exposé à identifier",
    ],
    recommendations: [
      "Rebalancer la couverture — prioriser les comptes à fort potentiel non couverts",
      "Lancer une campagne de prospection sur les comptes vierges",
      "Planifier des QBRs pour les comptes sans revue depuis 90j+",
      "Déployer une intervention CS sur les 4 comptes à risque",
    ],
    territory_kpis: {
      pipeline_coverage_ratio: 2.8,
      quota_attainment_pct: 85.0,
      white_space_pct: 28.0,
      active_account_pct: 71.0,
      avg_account_health: 65.0,
      qbr_coverage_pct: 38.0,
      market_penetration_pct: 22.0,
      deals_in_flight: 8,
      accounts_at_risk: 4,
      closed_won_ytd_eur: 170000,
    },
  },
  {
    territory_id: "t_005",
    territory_name: "Enterprise AMER East",
    region: "amer",
    rep_name: "David Chen",
    territory_health: "imbalanced",
    territory_action: "rebalance",
    coverage_risk: "high",
    balance_score: 42.0,
    quota_attainment_pct: 55.0,
    pipeline_coverage_ratio: 1.6,
    white_space_pct: 38.0,
    strengths: [],
    gaps: [
      "Pipeline insuffisant — seulement 1.6x le quota (objectif ≥ 3x)",
      "38% de comptes non couverts — potentiel commercial inexploité",
      "Cadence QBR faible (32%) — risque de décrochage clients",
      "Atteinte quota à 55% — sous-performance critique",
    ],
    recommendations: [
      "Rebalancer la couverture — prioriser les comptes à fort potentiel non couverts",
      "Lancer une campagne de prospection sur les comptes vierges",
      "Accélérer la génération pipeline — objectif couverture 3x quota",
      "Planifier des QBRs pour les comptes sans revue depuis 90j+",
    ],
    territory_kpis: {
      pipeline_coverage_ratio: 1.6,
      quota_attainment_pct: 55.0,
      white_space_pct: 38.0,
      active_account_pct: 62.0,
      avg_account_health: 52.0,
      qbr_coverage_pct: 32.0,
      market_penetration_pct: 18.0,
      deals_in_flight: 5,
      accounts_at_risk: 6,
      closed_won_ytd_eur: 110000,
    },
  },
  {
    territory_id: "t_006",
    territory_name: "APAC South East Asia",
    region: "apac",
    rep_name: "Aisha Tan",
    territory_health: "imbalanced",
    territory_action: "hire",
    coverage_risk: "critical",
    balance_score: 38.5,
    quota_attainment_pct: 62.0,
    pipeline_coverage_ratio: 1.3,
    white_space_pct: 45.0,
    strengths: [],
    gaps: [
      "Pipeline insuffisant — seulement 1.3x le quota (objectif ≥ 3x)",
      "45% de comptes non couverts — potentiel commercial inexploité",
      "Cadence QBR faible (25%) — risque de décrochage clients",
      "7 comptes à risque — ARR exposé à identifier",
      "Territoire surchargé — 115 comptes difficiles à couvrir correctement",
    ],
    recommendations: [
      "Recruter un rep additionnel — charge de travail actuelle dépasse la capacité",
      "Définir les critères de partage du territoire avant l'embauche",
      "Accélérer la génération pipeline — objectif couverture 3x quota",
      "Déployer une intervention CS sur les 7 comptes à risque",
      "Cartographier le TAM résiduel — 8% de pénétration laisse 92% d'opportunités",
    ],
    territory_kpis: {
      pipeline_coverage_ratio: 1.3,
      quota_attainment_pct: 62.0,
      white_space_pct: 45.0,
      active_account_pct: 55.0,
      avg_account_health: 48.0,
      qbr_coverage_pct: 25.0,
      market_penetration_pct: 8.0,
      deals_in_flight: 6,
      accounts_at_risk: 7,
      closed_won_ytd_eur: 124000,
    },
  },
  {
    territory_id: "t_007",
    territory_name: "Enterprise AMER West",
    region: "amer",
    rep_name: "Carlos Rivera",
    territory_health: "critical",
    territory_action: "rebalance",
    coverage_risk: "critical",
    balance_score: 28.0,
    quota_attainment_pct: 32.0,
    pipeline_coverage_ratio: 0.9,
    white_space_pct: 52.0,
    strengths: [],
    gaps: [
      "Pipeline insuffisant — seulement 0.9x le quota (objectif ≥ 3x)",
      "52% de comptes non couverts — potentiel commercial inexploité",
      "Cadence QBR faible (18%) — risque de décrochage clients",
      "8 comptes à risque — ARR exposé à identifier",
      "Atteinte quota à 32% — sous-performance critique",
      "Rep en cours de ramp — pleine capacité pas encore atteinte",
    ],
    recommendations: [
      "Rebalancer la couverture — prioriser les comptes à fort potentiel non couverts",
      "Accélérer la génération pipeline — objectif couverture 3x quota",
      "Planifier des QBRs pour les comptes sans revue depuis 90j+",
      "Déployer une intervention CS sur les 8 comptes à risque",
      "Accélérer le ramp — buddy system avec un rep senior pour montée en puissance",
    ],
    territory_kpis: {
      pipeline_coverage_ratio: 0.9,
      quota_attainment_pct: 32.0,
      white_space_pct: 52.0,
      active_account_pct: 48.0,
      avg_account_health: 42.0,
      qbr_coverage_pct: 18.0,
      market_penetration_pct: 12.0,
      deals_in_flight: 3,
      accounts_at_risk: 8,
      closed_won_ytd_eur: 64000,
    },
  },
  {
    territory_id: "t_008",
    territory_name: "SMB Nordics",
    region: "emea",
    rep_name: "Erik Lindström",
    territory_health: "critical",
    territory_action: "rebalance",
    coverage_risk: "critical",
    balance_score: 22.0,
    quota_attainment_pct: 18.0,
    pipeline_coverage_ratio: 0.7,
    white_space_pct: 60.0,
    strengths: [],
    gaps: [
      "Pipeline insuffisant — seulement 0.7x le quota (objectif ≥ 3x)",
      "60% de comptes non couverts — potentiel commercial inexploité",
      "Cadence QBR faible (15%) — risque de décrochage clients",
      "9 comptes à risque — ARR exposé à identifier",
      "Atteinte quota à 18% — sous-performance critique",
      "Faible pénétration marché (6%) — TAM largement inexploité",
      "Pression concurrentielle forte (78/100) — perte de comptes risquée",
    ],
    recommendations: [
      "Rebalancer la couverture — prioriser les comptes à fort potentiel non couverts",
      "Lancer une campagne de prospection sur les comptes vierges",
      "Accélérer la génération pipeline — objectif couverture 3x quota",
      "Déployer une intervention CS sur les 9 comptes à risque",
      "Cartographier le TAM résiduel — 6% de pénétration laisse 94% d'opportunités",
    ],
    territory_kpis: {
      pipeline_coverage_ratio: 0.7,
      quota_attainment_pct: 18.0,
      white_space_pct: 60.0,
      active_account_pct: 40.0,
      avg_account_health: 38.0,
      qbr_coverage_pct: 15.0,
      market_penetration_pct: 6.0,
      deals_in_flight: 2,
      accounts_at_risk: 9,
      closed_won_ytd_eur: 36000,
    },
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const health = searchParams.get("health");
  const action = searchParams.get("action");
  const region = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/territory-optimizer`);
      if (health) url.searchParams.set("health", health);
      if (action) url.searchParams.set("action", action);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let territories = [...mockTerritories];
  if (health) territories = territories.filter((t) => t.territory_health === health);
  if (action) territories = territories.filter((t) => t.territory_action === action);
  if (region) territories = territories.filter((t) => t.region === region);

  const health_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const risk_counts: Record<string, number> = {};
  let total_score = 0;
  let total_attainment = 0;

  for (const t of mockTerritories) {
    health_counts[t.territory_health] = (health_counts[t.territory_health] || 0) + 1;
    action_counts[t.territory_action] = (action_counts[t.territory_action] || 0) + 1;
    risk_counts[t.coverage_risk] = (risk_counts[t.coverage_risk] || 0) + 1;
    total_score += t.balance_score;
    total_attainment += t.quota_attainment_pct;
  }

  const n = mockTerritories.length;

  return NextResponse.json({
    territories,
    summary: {
      total: n,
      health_counts,
      action_counts,
      risk_counts,
      avg_balance_score: Math.round((total_score / n) * 10) / 10,
      avg_quota_attainment_pct: Math.round((total_attainment / n) * 10) / 10,
      needs_rebalance_count: mockTerritories.filter((t) =>
        ["rebalance", "split", "hire"].includes(t.territory_action)
      ).length,
      optimal_count: mockTerritories.filter((t) => t.territory_health === "optimal").length,
      critical_count: mockTerritories.filter((t) => t.territory_health === "critical").length,
    },
  });
}
