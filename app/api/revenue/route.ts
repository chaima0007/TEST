import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

type RevenuePeriod = "monthly" | "quarterly" | "annual";
type ConfidenceLevel = "low" | "medium" | "high" | "very_high";

interface DealSignals {
  deal_id: string;
  name: string;
  company: string;
  sector: string;
  stage: string;
  deal_value_eur: number;
  probability: number;
  expected_close_days: number;
  lead_score: number;
  churn_risk_score: number;
  months_in_pipeline: number;
}

interface RevenuePrediction {
  deal: DealSignals;
  adjusted_probability: number;
  weighted_value_eur: number;
  confidence: ConfidenceLevel;
  expected_close_date_offset_days: number;
  risk_factors: string[];
  upside_factors: string[];
}

interface PeriodForecast {
  period: RevenuePeriod;
  predictions: RevenuePrediction[];
  total_pipeline_eur: number;
  expected_revenue_eur: number;
  conservative_eur: number;
  optimistic_eur: number;
  by_stage: Record<string, { count: number; pipeline_eur: number; weighted_eur: number }>;
  by_sector: Record<string, number>;
  confidence_distribution: Record<ConfidenceLevel, number>;
}

const STAGE_FACTOR: Record<string, number> = {
  prospecting: 0.70,
  qualified: 0.85,
  proposal: 0.95,
  negotiation: 1.00,
  closing: 1.05,
};

const MOCK_DEALS: DealSignals[] = [
  { deal_id: "deal_001", name: "CRM Migration", company: "Renault Digital", sector: "automotive", stage: "closing", deal_value_eur: 85000, probability: 0.82, expected_close_days: 12, lead_score: 88, churn_risk_score: 18, months_in_pipeline: 2 },
  { deal_id: "deal_002", name: "Data Platform", company: "BNP Paribas", sector: "finance", stage: "negotiation", deal_value_eur: 140000, probability: 0.71, expected_close_days: 28, lead_score: 79, churn_risk_score: 22, months_in_pipeline: 4 },
  { deal_id: "deal_003", name: "Security Audit", company: "AXA Group", sector: "insurance", stage: "proposal", deal_value_eur: 55000, probability: 0.58, expected_close_days: 35, lead_score: 65, churn_risk_score: 35, months_in_pipeline: 3 },
  { deal_id: "deal_004", name: "ERP Integration", company: "Saint-Gobain", sector: "manufacturing", stage: "negotiation", deal_value_eur: 210000, probability: 0.64, expected_close_days: 45, lead_score: 72, churn_risk_score: 28, months_in_pipeline: 5 },
  { deal_id: "deal_005", name: "AI Assistant", company: "Orange Business", sector: "telecom", stage: "qualified", deal_value_eur: 38000, probability: 0.45, expected_close_days: 60, lead_score: 55, churn_risk_score: 42, months_in_pipeline: 2 },
  { deal_id: "deal_006", name: "Analytics Suite", company: "Carrefour Tech", sector: "retail", stage: "proposal", deal_value_eur: 72000, probability: 0.52, expected_close_days: 40, lead_score: 61, churn_risk_score: 30, months_in_pipeline: 3 },
  { deal_id: "deal_007", name: "Cloud Migration", company: "Société Générale", sector: "finance", stage: "closing", deal_value_eur: 95000, probability: 0.78, expected_close_days: 18, lead_score: 84, churn_risk_score: 15, months_in_pipeline: 3 },
  { deal_id: "deal_008", name: "DevOps Platform", company: "Michelin IT", sector: "manufacturing", stage: "qualified", deal_value_eur: 48000, probability: 0.38, expected_close_days: 75, lead_score: 44, churn_risk_score: 55, months_in_pipeline: 7 },
  { deal_id: "deal_009", name: "HR System", company: "L'Oréal Digital", sector: "consumer", stage: "prospecting", deal_value_eur: 32000, probability: 0.28, expected_close_days: 90, lead_score: 35, churn_risk_score: 68, months_in_pipeline: 8 },
  { deal_id: "deal_010", name: "Marketing Automation", company: "Decathlon", sector: "retail", stage: "proposal", deal_value_eur: 61000, probability: 0.55, expected_close_days: 50, lead_score: 68, churn_risk_score: 25, months_in_pipeline: 4 },
  { deal_id: "deal_011", name: "IoT Dashboard", company: "Schneider Electric", sector: "energy", stage: "negotiation", deal_value_eur: 118000, probability: 0.69, expected_close_days: 30, lead_score: 76, churn_risk_score: 20, months_in_pipeline: 6 },
  { deal_id: "deal_012", name: "Compliance Tool", company: "Crédit Agricole", sector: "finance", stage: "qualified", deal_value_eur: 43000, probability: 0.42, expected_close_days: 65, lead_score: 50, churn_risk_score: 48, months_in_pipeline: 5 },
];

function leadFactor(leadScore: number): number {
  const c = Math.max(0, Math.min(100, leadScore));
  return 0.50 + (c / 100) * 0.50;
}

function churnFactor(churnRiskScore: number): number {
  const c = Math.max(0, Math.min(100, churnRiskScore));
  return 1.0 - c / 200.0;
}

function stageFactor(stage: string): number {
  return STAGE_FACTOR[stage.toLowerCase()] ?? 0.80;
}

function adjustedProbability(deal: DealSignals): number {
  const adj = deal.probability * leadFactor(deal.lead_score) * churnFactor(deal.churn_risk_score) * stageFactor(deal.stage);
  return Math.round(Math.max(0, Math.min(1, adj)) * 10000) / 10000;
}

function confidence(adjProb: number, stage: string, leadScore: number): ConfidenceLevel {
  const s = stage.toLowerCase();
  const late = s === "negotiation" || s === "closing";
  const mid = s === "proposal";
  if (adjProb >= 0.70 && late && leadScore >= 60) return "very_high";
  if (adjProb >= 0.50 && (late || mid)) return "high";
  if (adjProb >= 0.30) return "medium";
  return "low";
}

function riskFactors(deal: DealSignals): string[] {
  const risks: string[] = [];
  if (deal.churn_risk_score > 60) risks.push("Haut risque de churn client");
  if (deal.months_in_pipeline > 6) risks.push("Pipeline trop long (>6 mois)");
  if (deal.lead_score < 40) risks.push("Score lead faible (<40)");
  if (deal.expected_close_days > 90) risks.push("Délai de clôture élevé (>90 jours)");
  if (deal.probability < 0.30) risks.push("Probabilité de base insuffisante");
  return risks;
}

function upsideFactors(deal: DealSignals): string[] {
  const upsides: string[] = [];
  if (deal.lead_score >= 75) upsides.push("Score lead élevé (≥75)");
  if (deal.churn_risk_score <= 25) upsides.push("Faible risque de churn");
  const s = deal.stage.toLowerCase();
  if ((s === "negotiation" || s === "closing") && deal.months_in_pipeline <= 3)
    upsides.push("Progression pipeline rapide");
  if (deal.deal_value_eur >= 50_000) upsides.push("Opportunité haute valeur (≥50k€)");
  if (deal.probability >= 0.70) upsides.push("Forte probabilité de base");
  return upsides;
}

function predictOne(deal: DealSignals): RevenuePrediction {
  const adjProb = adjustedProbability(deal);
  return {
    deal,
    adjusted_probability: adjProb,
    weighted_value_eur: Math.round(deal.deal_value_eur * adjProb * 100) / 100,
    confidence: confidence(adjProb, deal.stage, deal.lead_score),
    expected_close_date_offset_days: deal.expected_close_days,
    risk_factors: riskFactors(deal),
    upside_factors: upsideFactors(deal),
  };
}

function buildForecast(deals: DealSignals[], period: RevenuePeriod): PeriodForecast {
  const periodMonths: Record<RevenuePeriod, number> = { monthly: 1, quarterly: 3, annual: 12 };
  const daysLimit = periodMonths[period] * 30;

  const allPreds = deals.map(predictOne);
  const inPeriod = allPreds.filter(p => p.deal.expected_close_days <= daysLimit);
  const sorted = [...inPeriod].sort((a, b) => b.weighted_value_eur - a.weighted_value_eur);

  const totalPipeline = inPeriod.reduce((s, p) => s + p.deal.deal_value_eur, 0);
  const expected = inPeriod.reduce((s, p) => s + p.weighted_value_eur, 0);

  const byStage: PeriodForecast["by_stage"] = {};
  const bySector: Record<string, number> = {};
  const confDist: Record<ConfidenceLevel, number> = { low: 0, medium: 0, high: 0, very_high: 0 };

  for (const p of inPeriod) {
    const st = p.deal.stage;
    if (!byStage[st]) byStage[st] = { count: 0, pipeline_eur: 0, weighted_eur: 0 };
    byStage[st].count++;
    byStage[st].pipeline_eur = Math.round((byStage[st].pipeline_eur + p.deal.deal_value_eur) * 100) / 100;
    byStage[st].weighted_eur = Math.round((byStage[st].weighted_eur + p.weighted_value_eur) * 100) / 100;

    const sec = p.deal.sector;
    bySector[sec] = Math.round(((bySector[sec] ?? 0) + p.weighted_value_eur) * 100) / 100;
    confDist[p.confidence]++;
  }

  return {
    period,
    predictions: sorted,
    total_pipeline_eur: Math.round(totalPipeline * 100) / 100,
    expected_revenue_eur: Math.round(expected * 100) / 100,
    conservative_eur: Math.round(expected * 0.75 * 100) / 100,
    optimistic_eur: Math.round(expected * 1.25 * 100) / 100,
    by_stage: byStage,
    by_sector: bySector,
    confidence_distribution: confDist,
  };
}

function computeSummary(predictions: RevenuePrediction[]) {
  const count = predictions.length;
  if (count === 0) return {
    total_deals: 0, total_pipeline_eur: 0, expected_revenue_eur: 0,
    conservative_eur: 0, optimistic_eur: 0, avg_adjusted_probability: 0,
    at_risk_count: 0, confidence_distribution: { low: 0, medium: 0, high: 0, very_high: 0 },
  };

  const totalPipeline = predictions.reduce((s, p) => s + p.deal.deal_value_eur, 0);
  const expected = predictions.reduce((s, p) => s + p.weighted_value_eur, 0);
  const avgProb = predictions.reduce((s, p) => s + p.adjusted_probability, 0) / count;
  const confDist: Record<ConfidenceLevel, number> = { low: 0, medium: 0, high: 0, very_high: 0 };
  for (const p of predictions) confDist[p.confidence]++;

  return {
    total_deals: count,
    total_pipeline_eur: Math.round(totalPipeline * 100) / 100,
    expected_revenue_eur: Math.round(expected * 100) / 100,
    conservative_eur: Math.round(expected * 0.75 * 100) / 100,
    optimistic_eur: Math.round(expected * 1.25 * 100) / 100,
    avg_adjusted_probability: Math.round(avgProb * 10000) / 10000,
    at_risk_count: predictions.filter(p => p.risk_factors.length > 0).length,
    confidence_distribution: confDist,
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/revenue`, { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch { /* fall through */ }
  }

  const quarterly = buildForecast(MOCK_DEALS, "quarterly");
  const monthly = buildForecast(MOCK_DEALS, "monthly");
  const annual = buildForecast(MOCK_DEALS, "annual");
  const allPredictions = MOCK_DEALS.map(predictOne).sort((a, b) => b.weighted_value_eur - a.weighted_value_eur);
  const summary = computeSummary(allPredictions);

  return NextResponse.json({
    predictions: allPredictions,
    summary,
    quarterly,
    monthly,
    annual,
    last_updated: new Date().toISOString(),
  });
}
