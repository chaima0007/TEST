import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[revenue-attribution] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "d_001",
    account_id: "acc_001",
    rep_id: "rep_001",
    attributed_revenue: 120000.0,
    attribution_model: "position_based",
    channel_credits: { outbound_email: 48000, sdr_call: 48000, inbound_content: 24000 },
    roi_by_channel: { outbound_email: 96.0, sdr_call: 60.0, inbound_content: 120.0 },
    revenue_risk: "low",
    optimization_action: "scale_up",
    top_channel: "outbound_email",
    attribution_efficiency: 75.6,
    pipeline_to_revenue_ratio: 0.4,
    cost_per_acquisition: 1500.0,
    cycle_efficiency: 52.5,
    is_high_value: false,
    deal_name: "ERP Integration",
    account_name: "TechCorp SA",
    segment: "mid_market",
    industry: "saas",
    total_touchpoints: 3,
    pipeline_created: 300000.0,
    closed_won_value: 120000.0,
    closed_lost_value: 80000.0,
  },
  {
    deal_id: "d_002",
    account_id: "acc_002",
    rep_id: "rep_002",
    attributed_revenue: 250000.0,
    attribution_model: "time_decay",
    channel_credits: { paid_ads: 75000, outbound_email: 100000, event: 75000 },
    roi_by_channel: { paid_ads: 3.75, outbound_email: 5.0, event: 6.25 },
    revenue_risk: "low",
    optimization_action: "scale_up",
    top_channel: "outbound_email",
    attribution_efficiency: 82.1,
    pipeline_to_revenue_ratio: 0.5,
    cost_per_acquisition: 12000.0,
    cycle_efficiency: 70.0,
    is_high_value: true,
    deal_name: "Platform Migration",
    account_name: "HealthTech Pro",
    segment: "enterprise",
    industry: "healthtech",
    total_touchpoints: 8,
    pipeline_created: 500000.0,
    closed_won_value: 250000.0,
    closed_lost_value: 50000.0,
  },
  {
    deal_id: "d_003",
    account_id: "acc_003",
    rep_id: "rep_003",
    attributed_revenue: 45000.0,
    attribution_model: "linear",
    channel_credits: { social_selling: 15000, referral: 15000, inbound_content: 15000 },
    roi_by_channel: { social_selling: 7.5, referral: 15.0, inbound_content: 10.0 },
    revenue_risk: "medium",
    optimization_action: "maintain",
    top_channel: "referral",
    attribution_efficiency: 61.5,
    pipeline_to_revenue_ratio: 0.45,
    cost_per_acquisition: 3500.0,
    cycle_efficiency: 63.0,
    is_high_value: true,
    deal_name: "LMS Deployment",
    account_name: "EduSmart Group",
    segment: "smb",
    industry: "edtech",
    total_touchpoints: 3,
    pipeline_created: 100000.0,
    closed_won_value: 45000.0,
    closed_lost_value: 30000.0,
  },
  {
    deal_id: "d_004",
    account_id: "acc_004",
    rep_id: "rep_001",
    attributed_revenue: 185000.0,
    attribution_model: "first_touch",
    channel_credits: { partner: 185000 },
    roi_by_channel: { partner: 12.33 },
    revenue_risk: "low",
    optimization_action: "scale_up",
    top_channel: "partner",
    attribution_efficiency: 79.8,
    pipeline_to_revenue_ratio: 0.617,
    cost_per_acquisition: 15000.0,
    cycle_efficiency: 77.0,
    is_high_value: false,
    deal_name: "Analytics Platform",
    account_name: "MediaGroup SAS",
    segment: "mid_market",
    industry: "media",
    total_touchpoints: 5,
    pipeline_created: 300000.0,
    closed_won_value: 185000.0,
    closed_lost_value: 20000.0,
  },
  {
    deal_id: "d_005",
    account_id: "acc_005",
    rep_id: "rep_004",
    attributed_revenue: 65000.0,
    attribution_model: "last_touch",
    channel_credits: { sdr_call: 65000 },
    roi_by_channel: { sdr_call: 4.33 },
    revenue_risk: "medium",
    optimization_action: "optimize",
    top_channel: "sdr_call",
    attribution_efficiency: 43.8,
    pipeline_to_revenue_ratio: 0.325,
    cost_per_acquisition: 15000.0,
    cycle_efficiency: 42.0,
    is_high_value: false,
    deal_name: "CRM Unification",
    account_name: "GlobalFinance SARL",
    segment: "mid_market",
    industry: "finance",
    total_touchpoints: 6,
    pipeline_created: 200000.0,
    closed_won_value: 65000.0,
    closed_lost_value: 90000.0,
  },
  {
    deal_id: "d_006",
    account_id: "acc_006",
    rep_id: "rep_002",
    attributed_revenue: 320000.0,
    attribution_model: "position_based",
    channel_credits: { event: 128000, paid_ads: 64000, outbound_email: 128000 },
    roi_by_channel: { event: 8.0, paid_ads: 4.27, outbound_email: 12.8 },
    revenue_risk: "low",
    optimization_action: "scale_up",
    top_channel: "event",
    attribution_efficiency: 88.2,
    pipeline_to_revenue_ratio: 0.64,
    cost_per_acquisition: 40000.0,
    cycle_efficiency: 84.0,
    is_high_value: true,
    deal_name: "Risk Analytics Suite",
    account_name: "FinServ Capital",
    segment: "enterprise",
    industry: "finance",
    total_touchpoints: 12,
    pipeline_created: 500000.0,
    closed_won_value: 320000.0,
    closed_lost_value: 10000.0,
  },
  {
    deal_id: "d_007",
    account_id: "acc_007",
    rep_id: "rep_003",
    attributed_revenue: 28000.0,
    attribution_model: "linear",
    channel_credits: { inbound_content: 9333, social_selling: 9333, outbound_email: 9334 },
    roi_by_channel: { inbound_content: 4.67, social_selling: 4.67, outbound_email: 4.67 },
    revenue_risk: "high",
    optimization_action: "reduce",
    top_channel: "outbound_email",
    attribution_efficiency: 28.0,
    pipeline_to_revenue_ratio: 0.14,
    cost_per_acquisition: 6000.0,
    cycle_efficiency: 25.2,
    is_high_value: true,
    deal_name: "Customer 360",
    account_name: "RetailChain Nord",
    segment: "smb",
    industry: "retail",
    total_touchpoints: 3,
    pipeline_created: 200000.0,
    closed_won_value: 28000.0,
    closed_lost_value: 130000.0,
  },
  {
    deal_id: "d_008",
    account_id: "acc_008",
    rep_id: "rep_004",
    attributed_revenue: 95000.0,
    attribution_model: "time_decay",
    channel_credits: { referral: 47500, outbound_email: 28500, sdr_call: 19000 },
    roi_by_channel: { referral: 19.0, outbound_email: 5.7, sdr_call: 2.38 },
    revenue_risk: "low",
    optimization_action: "maintain",
    top_channel: "referral",
    attribution_efficiency: 63.7,
    pipeline_to_revenue_ratio: 0.475,
    cost_per_acquisition: 5000.0,
    cycle_efficiency: 63.0,
    is_high_value: false,
    deal_name: "Supply Chain Intelligence",
    account_name: "LogisticsPlus SA",
    segment: "mid_market",
    industry: "logistics",
    total_touchpoints: 7,
    pipeline_created: 200000.0,
    closed_won_value: 95000.0,
    closed_lost_value: 40000.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const model  = searchParams.get("model");
  const risk   = searchParams.get("risk");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/revenue-attribution`);
      if (model)  url.searchParams.set("model", model);
      if (risk)   url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (model)  deals = deals.filter((d) => d.attribution_model === model);
  if (risk)   deals = deals.filter((d) => d.revenue_risk === risk);
  if (action) deals = deals.filter((d) => d.optimization_action === action);

  const model_counts:   Record<string, number> = {};
  const risk_counts:    Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  const channel_counts: Record<string, number> = {};
  let total_rev = 0, total_eff = 0, total_ptr = 0, total_cyc = 0, total_cpa = 0;

  for (const d of mockDeals) {
    model_counts[d.attribution_model]   = (model_counts[d.attribution_model] || 0) + 1;
    risk_counts[d.revenue_risk]         = (risk_counts[d.revenue_risk] || 0) + 1;
    action_counts[d.optimization_action] = (action_counts[d.optimization_action] || 0) + 1;
    channel_counts[d.top_channel]       = (channel_counts[d.top_channel] || 0) + 1;
    total_rev += d.attributed_revenue;
    total_eff += d.attribution_efficiency;
    total_ptr += d.pipeline_to_revenue_ratio;
    total_cyc += d.cycle_efficiency;
    total_cpa += d.cost_per_acquisition;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json({
    deals,
    summary: {
      total:                          n,
      model_counts,
      risk_counts,
      action_counts,
      top_channel_counts:             channel_counts,
      total_attributed_revenue:       Math.round(total_rev * 100) / 100,
      avg_attribution_efficiency:     Math.round((total_eff / n) * 10) / 10,
      avg_pipeline_to_revenue_ratio:  Math.round((total_ptr / n) * 1000) / 1000,
      avg_cycle_efficiency:           Math.round((total_cyc / n) * 10) / 10,
      high_value_count:               mockDeals.filter((d) => d.is_high_value).length,
      high_risk_count:                mockDeals.filter((d) => ["high", "critical"].includes(d.revenue_risk)).length,
      scale_up_count:                 mockDeals.filter((d) => d.optimization_action === "scale_up").length,
      avg_cost_per_acquisition:       Math.round((total_cpa / n) * 100) / 100,
    },
  }));
}
