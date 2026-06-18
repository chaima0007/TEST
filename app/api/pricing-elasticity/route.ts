import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockSegments = [
  {
    segment_id: "seg_001", segment_name: "Enterprise SaaS",
    industry: "Technology", region: "NAMER",
    elasticity_category: "moderate", pricing_risk: "medium",
    pricing_stance: "neutral", pricing_action: "hold",
    price_elasticity_index: 47.4, discount_leak_score: 45.6,
    competitive_pressure_score: 38.2, revenue_at_risk: 310176,
    expansion_opportunity: 75600, optimal_price_adjustment_pct: 0.0,
    pricing_confidence_score: 100.0,
    is_price_sensitive: false, needs_pricing_review: false,
    avg_deal_size_current: 48000, total_pipeline_value: 2400000,
  },
  {
    segment_id: "seg_002", segment_name: "Mid-Market Fintech",
    industry: "Financial Services", region: "EMEA",
    elasticity_category: "high", pricing_risk: "high",
    pricing_stance: "defensive", pricing_action: "optimize",
    price_elasticity_index: 62.8, discount_leak_score: 58.4,
    competitive_pressure_score: 52.6, revenue_at_risk: 486000,
    expansion_opportunity: 0, optimal_price_adjustment_pct: -6.3,
    pricing_confidence_score: 100.0,
    is_price_sensitive: true, needs_pricing_review: true,
    avg_deal_size_current: 24000, total_pipeline_value: 1800000,
  },
  {
    segment_id: "seg_003", segment_name: "SMB Retail",
    industry: "Retail", region: "APAC",
    elasticity_category: "extreme", pricing_risk: "critical",
    pricing_stance: "vulnerable", pricing_action: "restructure",
    price_elasticity_index: 82.4, discount_leak_score: 72.6,
    competitive_pressure_score: 74.8, revenue_at_risk: 672000,
    expansion_opportunity: 0, optimal_price_adjustment_pct: -12.5,
    pricing_confidence_score: 80.0,
    is_price_sensitive: true, needs_pricing_review: true,
    avg_deal_size_current: 8000, total_pipeline_value: 1200000,
  },
  {
    segment_id: "seg_004", segment_name: "Strategic Manufacturing",
    industry: "Manufacturing", region: "EMEA",
    elasticity_category: "inelastic", pricing_risk: "low",
    pricing_stance: "premium", pricing_action: "increase",
    price_elasticity_index: 12.6, discount_leak_score: 18.2,
    competitive_pressure_score: 14.4, revenue_at_risk: 98400,
    expansion_opportunity: 423000, optimal_price_adjustment_pct: 8.4,
    pricing_confidence_score: 100.0,
    is_price_sensitive: false, needs_pricing_review: false,
    avg_deal_size_current: 120000, total_pipeline_value: 4200000,
  },
  {
    segment_id: "seg_005", segment_name: "Growth Healthcare",
    industry: "Healthcare", region: "NAMER",
    elasticity_category: "low", pricing_risk: "low",
    pricing_stance: "competitive", pricing_action: "optimize",
    price_elasticity_index: 28.4, discount_leak_score: 32.6,
    competitive_pressure_score: 28.8, revenue_at_risk: 156000,
    expansion_opportunity: 188100, optimal_price_adjustment_pct: 4.2,
    pricing_confidence_score: 100.0,
    is_price_sensitive: false, needs_pricing_review: false,
    avg_deal_size_current: 32000, total_pipeline_value: 1560000,
  },
  {
    segment_id: "seg_006", segment_name: "Mid-Market Logistics",
    industry: "Logistics", region: "LATAM",
    elasticity_category: "moderate", pricing_risk: "medium",
    pricing_stance: "neutral", pricing_action: "discount_control",
    price_elasticity_index: 38.6, discount_leak_score: 56.8,
    competitive_pressure_score: 42.4, revenue_at_risk: 234000,
    expansion_opportunity: 98600, optimal_price_adjustment_pct: 3.8,
    pricing_confidence_score: 80.0,
    is_price_sensitive: false, needs_pricing_review: true,
    avg_deal_size_current: 18000, total_pipeline_value: 980000,
  },
  {
    segment_id: "seg_007", segment_name: "Enterprise Consulting",
    industry: "Professional Services", region: "EMEA",
    elasticity_category: "low", pricing_risk: "low",
    pricing_stance: "premium", pricing_action: "increase",
    price_elasticity_index: 18.2, discount_leak_score: 14.6,
    competitive_pressure_score: 16.4, revenue_at_risk: 82800,
    expansion_opportunity: 312000, optimal_price_adjustment_pct: 10.5,
    pricing_confidence_score: 100.0,
    is_price_sensitive: false, needs_pricing_review: false,
    avg_deal_size_current: 86000, total_pipeline_value: 2760000,
  },
  {
    segment_id: "seg_008", segment_name: "SMB Education",
    industry: "Education", region: "APAC",
    elasticity_category: "high", pricing_risk: "high",
    pricing_stance: "defensive", pricing_action: "optimize",
    price_elasticity_index: 64.2, discount_leak_score: 48.4,
    competitive_pressure_score: 58.6, revenue_at_risk: 312000,
    expansion_opportunity: 0, optimal_price_adjustment_pct: -5.8,
    pricing_confidence_score: 60.0,
    is_price_sensitive: true, needs_pricing_review: true,
    avg_deal_size_current: 5400, total_pipeline_value: 720000,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const category = searchParams.get("category");
  const risk     = searchParams.get("risk");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/pricing-elasticity`);
      if (category) url.searchParams.set("category", category);
      if (risk)     url.searchParams.set("risk", risk);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let segments = [...mockSegments];
  if (category) segments = segments.filter((s) => s.elasticity_category === category);
  if (risk)     segments = segments.filter((s) => s.pricing_risk === risk);
  if (region)   segments = segments.filter((s) => s.region === region);

  const elasticity_counts: Record<string, number> = {};
  const risk_counts:       Record<string, number> = {};
  const stance_counts:     Record<string, number> = {};
  const action_counts:     Record<string, number> = {};
  let total_elasticity = 0, total_discount = 0, total_comp = 0,
      total_rev_risk = 0, total_exp_opp = 0, total_adj = 0;

  for (const s of mockSegments) {
    elasticity_counts[s.elasticity_category] = (elasticity_counts[s.elasticity_category] || 0) + 1;
    risk_counts[s.pricing_risk]              = (risk_counts[s.pricing_risk] || 0) + 1;
    stance_counts[s.pricing_stance]          = (stance_counts[s.pricing_stance] || 0) + 1;
    action_counts[s.pricing_action]          = (action_counts[s.pricing_action] || 0) + 1;
    total_elasticity += s.price_elasticity_index;
    total_discount   += s.discount_leak_score;
    total_comp       += s.competitive_pressure_score;
    total_rev_risk   += s.revenue_at_risk;
    total_exp_opp    += s.expansion_opportunity;
    total_adj        += s.optimal_price_adjustment_pct;
  }

  const n = mockSegments.length;

  return NextResponse.json({
    segments,
    summary: {
      total:                            n,
      elasticity_counts,
      risk_counts,
      stance_counts,
      action_counts,
      avg_price_elasticity_index:       Math.round((total_elasticity / n) * 10) / 10,
      avg_discount_leak_score:          Math.round((total_discount / n) * 10) / 10,
      total_revenue_at_risk:            Math.round(total_rev_risk),
      total_expansion_opportunity:      Math.round(total_exp_opp),
      price_sensitive_count:            mockSegments.filter((s) => s.is_price_sensitive).length,
      review_needed_count:              mockSegments.filter((s) => s.needs_pricing_review).length,
      avg_competitive_pressure_score:   Math.round((total_comp / n) * 10) / 10,
      avg_optimal_price_adjustment_pct: Math.round((total_adj / n) * 10) / 10,
    },
  });
}
