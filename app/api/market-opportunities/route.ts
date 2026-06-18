import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

type OpportunityPhase = "emerging" | "growing" | "mature" | "declining";
type RiskLevel = "low" | "medium" | "high" | "critical";

interface MarketSignals {
  opportunity_id: string;
  market_name: string;
  sector: string;
  sub_sector: string;
  total_addressable_market_eur: number;
  annual_growth_rate_pct: number;
  competitor_count: number;
  our_market_share_pct: number;
  avg_deal_size_eur: number;
  avg_sales_cycle_days: number;
  demand_trend: number;
  regulatory_complexity: number;
  tech_disruption_risk: number;
  our_expertise_score: number;
}

interface ScoredOpportunity {
  market: MarketSignals;
  opportunity_score: number;
  opportunity_phase: OpportunityPhase;
  risk_level: RiskLevel;
  market_attractiveness: number;
  penetrability: number;
  strategic_fit: number;
  projected_revenue_2y_eur: number;
  key_advantages: string[];
  key_risks: string[];
  recommended_actions: string[];
}

const ADVANTAGES: Record<string, string> = {
  fast_growing_market: "Marché en forte croissance (>20%/an)",
  low_competition: "Faible concurrence détectée",
  strong_demand: "Tendance de demande très positive",
  high_expertise: "Forte expertise interne dans ce secteur",
  existing_share: "Part de marché existante — avantage acquis",
  large_tam: "Marché total adressable très large (>100M€)",
  optimal_deal_size: "Taille de deal optimale pour notre équipe commerciale",
};

const RISKS: Record<string, string> = {
  high_saturation: "Marché saturé — différenciation difficile",
  regulatory_barrier: "Complexité réglementaire élevée",
  tech_disruption: "Risque de disruption technologique imminente",
  declining_demand: "Tendance de demande négative détectée",
  slow_growth: "Croissance de marché faible ou nulle",
  no_expertise: "Expertise interne insuffisante dans ce secteur",
  large_competitors: "Présence de grands acteurs établis (>10 concurrents)",
};

const ACTIONS: Record<string, string> = {
  invest_now: "Allouer des ressources commerciales en priorité dès maintenant",
  pilot_first: "Lancer un projet pilote pour valider l'approche avant d'investir",
  differentiate: "Développer une proposition de valeur différenciante avant d'entrer",
  monitor: "Surveiller l'évolution du marché — pas d'action immédiate recommandée",
  exit_or_optimize: "Optimiser les opérations existantes ou envisager un retrait progressif",
  hire_expertise: "Recruter des experts sectoriels avant d'approcher ce marché",
  partner: "Envisager un partenariat avec un acteur local pour réduire le risque d'entrée",
};

const MOCK_MARKETS: MarketSignals[] = [
  { opportunity_id: "mkt_001", market_name: "IA Générative B2B", sector: "tech", sub_sector: "ai_saas", total_addressable_market_eur: 4_500_000_000, annual_growth_rate_pct: 0.45, competitor_count: 8, our_market_share_pct: 0, avg_deal_size_eur: 85000, avg_sales_cycle_days: 45, demand_trend: 0.90, regulatory_complexity: 25, tech_disruption_risk: 70, our_expertise_score: 72 },
  { opportunity_id: "mkt_002", market_name: "Cybersécurité PME", sector: "security", sub_sector: "smb_security", total_addressable_market_eur: 1_200_000_000, annual_growth_rate_pct: 0.28, competitor_count: 5, our_market_share_pct: 2, avg_deal_size_eur: 35000, avg_sales_cycle_days: 30, demand_trend: 0.75, regulatory_complexity: 35, tech_disruption_risk: 40, our_expertise_score: 85 },
  { opportunity_id: "mkt_003", market_name: "ERP Industrie 4.0", sector: "manufacturing", sub_sector: "erp", total_addressable_market_eur: 800_000_000, annual_growth_rate_pct: 0.15, competitor_count: 12, our_market_share_pct: 1, avg_deal_size_eur: 150000, avg_sales_cycle_days: 90, demand_trend: 0.40, regulatory_complexity: 20, tech_disruption_risk: 45, our_expertise_score: 60 },
  { opportunity_id: "mkt_004", market_name: "Conformité RGPD SaaS", sector: "legal_tech", sub_sector: "compliance", total_addressable_market_eur: 350_000_000, annual_growth_rate_pct: 0.22, competitor_count: 3, our_market_share_pct: 5, avg_deal_size_eur: 28000, avg_sales_cycle_days: 20, demand_trend: 0.65, regulatory_complexity: 60, tech_disruption_risk: 20, our_expertise_score: 78 },
  { opportunity_id: "mkt_005", market_name: "CRM Banque & Assurance", sector: "fintech", sub_sector: "crm", total_addressable_market_eur: 2_100_000_000, annual_growth_rate_pct: 0.08, competitor_count: 18, our_market_share_pct: 0.5, avg_deal_size_eur: 200000, avg_sales_cycle_days: 120, demand_trend: 0.20, regulatory_complexity: 80, tech_disruption_risk: 55, our_expertise_score: 55 },
  { opportunity_id: "mkt_006", market_name: "Automatisation RH", sector: "hrtech", sub_sector: "automation", total_addressable_market_eur: 600_000_000, annual_growth_rate_pct: 0.18, competitor_count: 6, our_market_share_pct: 0, avg_deal_size_eur: 45000, avg_sales_cycle_days: 35, demand_trend: 0.55, regulatory_complexity: 40, tech_disruption_risk: 35, our_expertise_score: 50 },
  { opportunity_id: "mkt_007", market_name: "E-commerce Intelligence", sector: "retail", sub_sector: "analytics", total_addressable_market_eur: 900_000_000, annual_growth_rate_pct: 0.25, competitor_count: 4, our_market_share_pct: 1.5, avg_deal_size_eur: 60000, avg_sales_cycle_days: 40, demand_trend: 0.70, regulatory_complexity: 15, tech_disruption_risk: 50, our_expertise_score: 68 },
  { opportunity_id: "mkt_008", market_name: "Santé Numérique", sector: "healthtech", sub_sector: "digital_health", total_addressable_market_eur: 3_000_000_000, annual_growth_rate_pct: 0.30, competitor_count: 9, our_market_share_pct: 0, avg_deal_size_eur: 120000, avg_sales_cycle_days: 100, demand_trend: 0.80, regulatory_complexity: 75, tech_disruption_risk: 30, our_expertise_score: 30 },
  { opportunity_id: "mkt_009", market_name: "Logistique & Supply Chain", sector: "logistics", sub_sector: "supply_chain", total_addressable_market_eur: 1_500_000_000, annual_growth_rate_pct: 0.12, competitor_count: 7, our_market_share_pct: 0, avg_deal_size_eur: 95000, avg_sales_cycle_days: 60, demand_trend: 0.30, regulatory_complexity: 25, tech_disruption_risk: 60, our_expertise_score: 42 },
  { opportunity_id: "mkt_010", market_name: "Analytics Education", sector: "edtech", sub_sector: "analytics", total_addressable_market_eur: 280_000_000, annual_growth_rate_pct: 0.05, competitor_count: 15, our_market_share_pct: 0, avg_deal_size_eur: 15000, avg_sales_cycle_days: 45, demand_trend: -0.10, regulatory_complexity: 30, tech_disruption_risk: 65, our_expertise_score: 25 },
];

function marketAttractiveness(m: MarketSignals): { score: number; advKeys: string[]; riskKeys: string[] } {
  const advKeys: string[] = []; const riskKeys: string[] = [];

  const growthScore = Math.max(0, Math.min(100, 50 + m.annual_growth_rate_pct * 500));
  if (m.annual_growth_rate_pct >= 0.20) advKeys.push("fast_growing_market");
  else if (m.annual_growth_rate_pct < 0) riskKeys.push("slow_growth");

  const demandClamped = Math.max(-1, Math.min(1, m.demand_trend));
  const demandScore = (demandClamped + 1) / 2 * 100;
  if (m.demand_trend < -0.20) riskKeys.push("declining_demand");
  else if (m.demand_trend > 0.50) advKeys.push("strong_demand");

  const tam = m.total_addressable_market_eur;
  const sizeScore = tam > 0 ? Math.min(100, Math.log10(Math.max(1, tam)) / 9 * 100) : 0;
  if (tam >= 100_000_000) advKeys.push("large_tam");

  const score = growthScore * 0.40 + demandScore * 0.35 + sizeScore * 0.25;
  return { score: Math.round(score * 100) / 100, advKeys, riskKeys };
}

function penetrabilityScore(m: MarketSignals): { score: number; advKeys: string[]; riskKeys: string[] } {
  const advKeys: string[] = []; const riskKeys: string[] = [];
  const saturation = Math.max(0, 100 - m.competitor_count * 10);
  if (m.competitor_count <= 3) advKeys.push("low_competition");
  if (m.competitor_count > 10) { riskKeys.push("large_competitors"); riskKeys.push("high_saturation"); }
  const regulatory = Math.max(0, 100 - m.regulatory_complexity);
  if (m.regulatory_complexity > 50) riskKeys.push("regulatory_barrier");
  const disruption = Math.max(0, 100 - m.tech_disruption_risk);
  if (m.tech_disruption_risk > 55) riskKeys.push("tech_disruption");
  const score = saturation * 0.40 + regulatory * 0.35 + disruption * 0.25;
  return { score: Math.round(Math.max(0, score) * 100) / 100, advKeys, riskKeys };
}

function strategicFitScore(m: MarketSignals): { score: number; advKeys: string[]; riskKeys: string[] } {
  const advKeys: string[] = []; const riskKeys: string[] = [];
  const expertise = m.our_expertise_score;
  if (expertise >= 75) advKeys.push("high_expertise");
  else if (expertise < 35) riskKeys.push("no_expertise");
  const marketShareBonus = Math.min(30, m.our_market_share_pct * 2);
  if (m.our_market_share_pct > 0) advKeys.push("existing_share");
  const deal = m.avg_deal_size_eur;
  let dealScore: number;
  if (deal >= 20000 && deal <= 200000) { dealScore = 100; advKeys.push("optimal_deal_size"); }
  else if ((deal >= 10000 && deal < 20000) || (deal > 200000 && deal <= 500000)) { dealScore = 80; }
  else { dealScore = 60; }
  const score = expertise * 0.50 + marketShareBonus * (100 / 30) * 0.20 + dealScore * 0.30;
  return { score: Math.round(Math.min(100, score) * 100) / 100, advKeys, riskKeys };
}

function opportunityPhase(m: MarketSignals): OpportunityPhase {
  const saturation = Math.max(0, 100 - m.competitor_count * 10);
  const g = m.annual_growth_rate_pct;
  const d = m.demand_trend;
  if (g >= 0.20 && saturation >= 70 && d > 0.30) return "emerging";
  if (g >= 0.08 || (g >= 0 && d > 0.10)) return "growing";
  if (g >= -0.05) return "mature";
  return "declining";
}

function riskLevel(m: MarketSignals): RiskLevel {
  if (m.regulatory_complexity > 70 || m.tech_disruption_risk > 75 || m.competitor_count > 15) return "critical";
  if (m.regulatory_complexity > 50 || m.tech_disruption_risk > 55 || m.competitor_count > 8) return "high";
  if (m.regulatory_complexity > 30 || m.competitor_count > 4) return "medium";
  return "low";
}

function projectedRevenue(m: MarketSignals, score: number): number {
  const shareGain = (score / 100) * 0.03;
  const tamTarget = m.total_addressable_market_eur * shareGain;
  if (m.avg_deal_size_eur > 0 && m.avg_sales_cycle_days > 0) {
    const dealsPerYear = (365 / m.avg_sales_cycle_days) * (score / 100) * 5;
    const revenueFromDeals = dealsPerYear * 2 * m.avg_deal_size_eur;
    return Math.round((tamTarget * 0.50 + revenueFromDeals * 0.50) * 100) / 100;
  }
  return Math.round(tamTarget * 100) / 100;
}

function scoreMarket(m: MarketSignals): ScoredOpportunity {
  const attr = marketAttractiveness(m);
  const penet = penetrabilityScore(m);
  const fit = strategicFitScore(m);

  const score = Math.round((attr.score * 0.40 + penet.score * 0.35 + fit.score * 0.25) * 100) / 100;
  const phase = opportunityPhase(m);
  const risk = riskLevel(m);
  const proj = projectedRevenue(m, score);

  const allAdvKeys = [...new Set([...attr.advKeys, ...penet.advKeys, ...fit.advKeys])];
  const allRiskKeys = [...new Set([...attr.riskKeys, ...penet.riskKeys, ...fit.riskKeys])];
  const advantages = allAdvKeys.map(k => ADVANTAGES[k]).filter(Boolean);
  const risks = allRiskKeys.map(k => RISKS[k]).filter(Boolean);

  const actions: string[] = [];
  if (phase === "emerging" && (risk === "low" || risk === "medium")) actions.push(ACTIONS.invest_now);
  else if (phase === "growing" && risk !== "critical") actions.push(ACTIONS.pilot_first);
  else if (phase === "mature") { actions.push(ACTIONS.differentiate); actions.push(ACTIONS.monitor); }
  else if (phase === "declining") actions.push(ACTIONS.exit_or_optimize);
  if (m.our_expertise_score < 40) actions.push(ACTIONS.hire_expertise);
  if (m.competitor_count > 3 && (risk === "high" || risk === "critical")) actions.push(ACTIONS.partner);

  return {
    market: m,
    opportunity_score: score,
    opportunity_phase: phase,
    risk_level: risk,
    market_attractiveness: attr.score,
    penetrability: penet.score,
    strategic_fit: fit.score,
    projected_revenue_2y_eur: proj,
    key_advantages: advantages,
    key_risks: risks,
    recommended_actions: [...new Set(actions)],
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/market-opportunities`, { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch { /* fall through */ }
  }

  const opportunities = MOCK_MARKETS.map(scoreMarket).sort((a, b) => b.opportunity_score - a.opportunity_score);

  const phaseCounts: Record<OpportunityPhase, number> = { emerging: 0, growing: 0, mature: 0, declining: 0 };
  const riskCounts: Record<RiskLevel, number> = { low: 0, medium: 0, high: 0, critical: 0 };
  const sectorRevenue: Record<string, number> = {};

  for (const o of opportunities) {
    phaseCounts[o.opportunity_phase]++;
    riskCounts[o.risk_level]++;
    sectorRevenue[o.market.sector] = (sectorRevenue[o.market.sector] ?? 0) + o.projected_revenue_2y_eur;
  }

  const totalProj = opportunities.reduce((s, o) => s + o.projected_revenue_2y_eur, 0);
  const avgScore = opportunities.length ? opportunities.reduce((s, o) => s + o.opportunity_score, 0) / opportunities.length : 0;
  const topSector = Object.entries(sectorRevenue).sort(([, a], [, b]) => b - a)[0]?.[0] ?? null;

  return NextResponse.json({
    opportunities,
    summary: {
      total: opportunities.length,
      phase_counts: phaseCounts,
      risk_counts: riskCounts,
      avg_opportunity_score: Math.round(avgScore * 100) / 100,
      total_projected_revenue_2y_eur: Math.round(totalProj * 100) / 100,
      top_sector: topSector,
    },
    last_updated: new Date().toISOString(),
  });
}
