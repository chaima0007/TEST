import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001",
    deal_name: "CloudScale SaaS — Enterprise Expansion",
    recommended_price_eur: 88000,
    recommended_strategy: "value_based",
    discount_pct: 12.0,
    discount_risk: "low",
    deal_urgency: "high",
    price_score: 84.5,
    win_probability_boost_pct: 16.8,
    margin_pct: 68.2,
    value_gap_eur: 8000,
    pricing_signals: [
      "Champion fort — peut justifier le prix sans discount agressif",
      "Business case préparé — pricing value-based justifiable",
      "Décideur impliqué — cycle court, moins de pression prix",
    ],
    negotiation_tips: [
      "Présenter le ROI chiffré avec la business case et des benchmarks sectoriels",
      "Conditionner le discount à une signature avant fin de trimestre",
      "Organiser un exec-to-exec call pour valider le budget et la timeline",
    ],
    risk_flags: [],
  },
  {
    deal_id: "deal_002",
    deal_name: "FinTech Ventures — CRM Platform",
    recommended_price_eur: 52000,
    recommended_strategy: "competitive",
    discount_pct: 18.5,
    discount_risk: "medium",
    deal_urgency: "critical",
    price_score: 71.2,
    win_probability_boost_pct: 14.4,
    margin_pct: 52.3,
    value_gap_eur: -5000,
    pricing_signals: [
      "Décideur impliqué — cycle court, moins de pression prix",
      "Business case préparé — pricing value-based justifiable",
    ],
    negotiation_tips: [
      "Demander une liste des concurrents évalués et personaliser les objections",
      "Conditionner le discount à une signature avant fin de trimestre",
      "Proposer un prix d'entrée réduit avec engagement de upsell formalisé",
    ],
    risk_flags: [
      "Urgence critique — risque de churn si décision non prise rapidement",
      "4 concurrents — évaluation très compétitive",
    ],
  },
  {
    deal_id: "deal_003",
    deal_name: "StartupAI — Seed Stage Entry",
    recommended_price_eur: 14400,
    recommended_strategy: "freemium",
    discount_pct: 20.0,
    discount_risk: "medium",
    deal_urgency: "medium",
    price_score: 62.8,
    win_probability_boost_pct: 14.0,
    margin_pct: 44.4,
    value_gap_eur: 3000,
    pricing_signals: [
      "Fort potentiel d'expansion — accepter un prix initial inférieur",
      "Compétiteurs plus chers — avantage prix naturel",
    ],
    negotiation_tips: [
      "Conditionner le discount à une signature avant fin de trimestre",
      "Proposer un prix d'entrée réduit avec engagement de upsell formalisé",
    ],
    risk_flags: [
      "Marge faible (44%) — risque sur la profitabilité",
    ],
  },
  {
    deal_id: "deal_004",
    deal_name: "ManufactGroup — Legacy CRM Migration",
    recommended_price_eur: 135000,
    recommended_strategy: "anchor",
    discount_pct: 25.0,
    discount_risk: "medium",
    deal_urgency: "critical",
    price_score: 68.4,
    win_probability_boost_pct: 20.0,
    margin_pct: 55.6,
    value_gap_eur: 12000,
    pricing_signals: [
      "Contrat long terme — discount multi-annuel possible",
      "Business case préparé — pricing value-based justifiable",
    ],
    negotiation_tips: [
      "Commencer avec le prix plein, puis accorder le discount progressivement",
      "Demander une liste des concurrents évalués et personaliser les objections",
      "Conditionner le discount à une signature avant fin de trimestre",
      "Organiser un exec-to-exec call pour valider le budget et la timeline",
    ],
    risk_flags: [
      "Urgence critique — risque de churn si décision non prise rapidement",
      "5 concurrents — évaluation très compétitive",
    ],
  },
  {
    deal_id: "deal_005",
    deal_name: "Premium Tech — Solo Product",
    recommended_price_eur: 28000,
    recommended_strategy: "premium",
    discount_pct: 0.0,
    discount_risk: "none",
    deal_urgency: "low",
    price_score: 76.3,
    win_probability_boost_pct: 8.0,
    margin_pct: 71.4,
    value_gap_eur: 6000,
    pricing_signals: [
      "Champion fort — peut justifier le prix sans discount agressif",
      "Compétiteurs plus chers — avantage prix naturel",
    ],
    negotiation_tips: [
      "Organiser un exec-to-exec call pour valider le budget et la timeline",
    ],
    risk_flags: [],
  },
  {
    deal_id: "deal_006",
    deal_name: "RetailChain — Basic Plan",
    recommended_price_eur: 19200,
    recommended_strategy: "penetration",
    discount_pct: 20.0,
    discount_risk: "medium",
    deal_urgency: "high",
    price_score: 42.1,
    win_probability_boost_pct: 15.0,
    margin_pct: 36.0,
    value_gap_eur: -8000,
    pricing_signals: [],
    negotiation_tips: [
      "Demander une liste des concurrents évalués et personaliser les objections",
      "Conditionner le discount à une signature avant fin de trimestre",
    ],
    risk_flags: [
      "Marge faible (36%) — risque sur la profitabilité",
      "Champion faible — deal à risque sans renforcement de la relation",
      "3 concurrents — évaluation très compétitive",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const strategy = searchParams.get("strategy");
  const urgency = searchParams.get("urgency");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/pricing-optimizer`);
      if (strategy) url.searchParams.set("strategy", strategy);
      if (urgency) url.searchParams.set("urgency", urgency);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (strategy) deals = deals.filter((d) => d.recommended_strategy === strategy);
  if (urgency) deals = deals.filter((d) => d.deal_urgency === urgency);

  const strategy_counts: Record<string, number> = {};
  const urgency_counts: Record<string, number> = {};
  let total_score = 0, total_discount = 0, total_margin = 0, total_pipeline = 0;

  for (const d of mockDeals) {
    strategy_counts[d.recommended_strategy] = (strategy_counts[d.recommended_strategy] || 0) + 1;
    urgency_counts[d.deal_urgency] = (urgency_counts[d.deal_urgency] || 0) + 1;
    total_score += d.price_score;
    total_discount += d.discount_pct;
    total_margin += d.margin_pct;
    total_pipeline += d.recommended_price_eur;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      strategy_counts,
      urgency_counts,
      avg_price_score: Math.round((total_score / n) * 10) / 10,
      avg_discount_pct: Math.round((total_discount / n) * 10) / 10,
      avg_margin_pct: Math.round((total_margin / n) * 10) / 10,
      total_pipeline_eur: total_pipeline,
    },
  });
}
