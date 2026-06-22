import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[revenue-forecaster] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001",
    deal_name: "Nexaline Corp — Enterprise Platform",
    amount_eur: 185000,
    stage: "negotiation",
    segment: "enterprise",
    close_date_days: 22,
    base_win_probability_pct: 70.0,
    adjusted_win_probability_pct: 87.0,
    weighted_value_eur: 160950,
    conservative_value_eur: 112665,
    optimistic_value_eur: 179745,
    deal_risk: "none",
    quarter_label: "current_quarter",
    risk_factors: [],
    upside_factors: [
      "Budget approuvé — décision financière validée",
      "Engagement verbal confirmé — probabilité de signature élevée",
      "Champion fort (85/100) — advocacy interne solide",
      "Clôture prévue dans 22j — momentum actif",
    ],
  },
  {
    deal_id: "deal_002",
    deal_name: "FinEdge Solutions — CRM Expansion",
    amount_eur: 124000,
    stage: "closing",
    segment: "mid_market",
    close_date_days: 8,
    base_win_probability_pct: 85.0,
    adjusted_win_probability_pct: 82.0,
    weighted_value_eur: 101680,
    conservative_value_eur: 71176,
    optimistic_value_eur: 120796,
    deal_risk: "low",
    quarter_label: "current_quarter",
    risk_factors: [
      "3 concurrents — évaluation comparative en cours",
    ],
    upside_factors: [
      "Budget approuvé — décision financière validée",
      "Clôture prévue dans 8j — momentum actif",
    ],
  },
  {
    deal_id: "deal_003",
    deal_name: "ManuGroup International — Legacy Migration",
    amount_eur: 210000,
    stage: "proposal",
    segment: "enterprise",
    close_date_days: 45,
    base_win_probability_pct: 50.0,
    adjusted_win_probability_pct: 58.0,
    weighted_value_eur: 121800,
    conservative_value_eur: 85260,
    optimistic_value_eur: 145145,
    deal_risk: "low",
    quarter_label: "current_quarter",
    risk_factors: [
      "5 concurrents — pression compétitive forte",
    ],
    upside_factors: [
      "Champion fort (78/100) — advocacy interne solide",
      "Renouvellement — historique client positif",
    ],
  },
  {
    deal_id: "deal_004",
    deal_name: "RetailPro Chain — SaaS Suite",
    amount_eur: 87000,
    stage: "demo",
    segment: "mid_market",
    close_date_days: 72,
    base_win_probability_pct: 35.0,
    adjusted_win_probability_pct: 43.0,
    weighted_value_eur: 37410,
    conservative_value_eur: 26187,
    optimistic_value_eur: 44421,
    deal_risk: "medium",
    quarter_label: "current_quarter",
    risk_factors: [
      "Budget non approuvé à ce stade avancé du cycle",
    ],
    upside_factors: [
      "Engagement verbal confirmé — probabilité de signature élevée",
    ],
  },
  {
    deal_id: "deal_005",
    deal_name: "TechStart AI — Seed Entry",
    amount_eur: 32000,
    stage: "qualification",
    segment: "startup",
    close_date_days: 55,
    base_win_probability_pct: 20.0,
    adjusted_win_probability_pct: 28.0,
    weighted_value_eur: 8960,
    conservative_value_eur: 6272,
    optimistic_value_eur: 10643,
    deal_risk: "medium",
    quarter_label: "current_quarter",
    risk_factors: [],
    upside_factors: [
      "Budget approuvé — décision financière validée",
      "Champion fort (80/100) — advocacy interne solide",
    ],
  },
  {
    deal_id: "deal_006",
    deal_name: "LogiFreight GmbH — Ops Platform",
    amount_eur: 156000,
    stage: "proposal",
    segment: "enterprise",
    close_date_days: 110,
    base_win_probability_pct: 50.0,
    adjusted_win_probability_pct: 55.0,
    weighted_value_eur: 85800,
    conservative_value_eur: 60060,
    optimistic_value_eur: 101985,
    deal_risk: "low",
    quarter_label: "next_quarter",
    risk_factors: [
      "2 concurrents — évaluation comparative en cours",
    ],
    upside_factors: [
      "Budget approuvé — décision financière validée",
      "Renouvellement — historique client positif",
    ],
  },
  {
    deal_id: "deal_007",
    deal_name: "HealthCo Belgium — Compliance Suite",
    amount_eur: 95000,
    stage: "negotiation",
    segment: "mid_market",
    close_date_days: 135,
    base_win_probability_pct: 70.0,
    adjusted_win_probability_pct: 63.0,
    weighted_value_eur: 59850,
    conservative_value_eur: 41895,
    optimistic_value_eur: 71113,
    deal_risk: "low",
    quarter_label: "next_quarter",
    risk_factors: [
      "4 concurrents — pression compétitive forte",
    ],
    upside_factors: [
      "Champion fort (72/100) — advocacy interne solide",
    ],
  },
  {
    deal_id: "deal_008",
    deal_name: "PropTech Venture — Data Platform",
    amount_eur: 68000,
    stage: "prospecting",
    segment: "smb",
    close_date_days: -5,
    base_win_probability_pct: 10.0,
    adjusted_win_probability_pct: 3.0,
    weighted_value_eur: 2040,
    conservative_value_eur: 1428,
    optimistic_value_eur: 2427,
    deal_risk: "high",
    quarter_label: "current_quarter",
    risk_factors: [
      "Clôture en retard de 5j — risque de glissement",
      "Champion faible (25/100) — deal instable",
    ],
    upside_factors: [],
  },
  {
    deal_id: "deal_009",
    deal_name: "EduGroup NL — Learning Platform",
    amount_eur: 48000,
    stage: "qualification",
    segment: "smb",
    close_date_days: 210,
    base_win_probability_pct: 20.0,
    adjusted_win_probability_pct: 18.0,
    weighted_value_eur: 8640,
    conservative_value_eur: 6048,
    optimistic_value_eur: 10272,
    deal_risk: "medium",
    quarter_label: "beyond",
    risk_factors: [
      "Champion faible (35/100) — deal instable",
    ],
    upside_factors: [],
  },
];

function buildForecast(deals: typeof mockDeals) {
  const totalPipeline = deals.reduce((s, d) => s + d.amount_eur, 0);
  const baseF = deals.reduce((s, d) => s + d.weighted_value_eur, 0);
  const consF = deals.reduce((s, d) => s + d.conservative_value_eur, 0);
  const optF = deals.reduce((s, d) => s + d.optimistic_value_eur, 0);

  const cq = deals.filter((d) => d.quarter_label === "current_quarter").reduce((s, d) => s + d.weighted_value_eur, 0);
  const nq = deals.filter((d) => d.quarter_label === "next_quarter").reduce((s, d) => s + d.weighted_value_eur, 0);
  const bq = deals.filter((d) => d.quarter_label === "beyond").reduce((s, d) => s + d.weighted_value_eur, 0);

  const avgProb = deals.length ? deals.reduce((s, d) => s + d.adjusted_win_probability_pct, 0) / deals.length : 0;
  const highRiskCount = deals.filter((d) => d.deal_risk === "high").length;

  const segmentBreakdown: Record<string, number> = {};
  const stageBreakdown: Record<string, number> = {};
  for (const d of deals) {
    segmentBreakdown[d.segment] = (segmentBreakdown[d.segment] ?? 0) + d.weighted_value_eur;
    stageBreakdown[d.stage] = (stageBreakdown[d.stage] ?? 0) + d.weighted_value_eur;
  }

  const highRiskPct = deals.length ? (highRiskCount / deals.length) * 100 : 0;
  const healthScore = Math.max(0, Math.min(100, avgProb - highRiskPct * 0.3));

  return {
    total_pipeline_eur: Math.round(totalPipeline),
    conservative_forecast_eur: Math.round(consF),
    base_forecast_eur: Math.round(baseF),
    optimistic_forecast_eur: Math.round(optF),
    current_quarter_pipeline_eur: Math.round(cq),
    next_quarter_pipeline_eur: Math.round(nq),
    beyond_pipeline_eur: Math.round(bq),
    avg_win_probability_pct: Math.round(avgProb * 10) / 10,
    pipeline_health_score: Math.round(healthScore * 10) / 10,
    deal_count: deals.length,
    high_risk_count: highRiskCount,
    segment_breakdown: segmentBreakdown,
    stage_breakdown: stageBreakdown,
  };
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk = searchParams.get("risk");
  const quarter = searchParams.get("quarter");
  const segment = searchParams.get("segment");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/revenue-forecaster`);
      if (risk) url.searchParams.set("risk", risk);
      if (quarter) url.searchParams.set("quarter", quarter);
      if (segment) url.searchParams.set("segment", segment);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (risk) deals = deals.filter((d) => d.deal_risk === risk);
  if (quarter) deals = deals.filter((d) => d.quarter_label === quarter);
  if (segment) deals = deals.filter((d) => d.segment === segment);

  const summary = buildForecast(mockDeals);

  return sealResponse(NextResponse.json({ deals, summary }));
}
