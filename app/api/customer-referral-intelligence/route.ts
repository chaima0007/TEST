import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockCustomers = [
  {
    customer_id: "cust_001", customer_name: "TechCorp Global", rep_id: "rep_001",
    referral_velocity: "accelerating", advocacy_level: "champion",
    referral_risk: "low", referral_action: "activate_referral",
    advocacy_score: 90.0, relationship_depth_score: 88.0,
    referral_propensity_score: 87.0, advocacy_impact_score: 92.0,
    referral_composite: 89.4, estimated_referral_pipeline_usd: 225000.0,
    is_active_referrer: true, needs_advocacy_activation: false,
    primary_advocacy_signal: "speaker + case study — elite advocate, maximize referral program",
    contract_value_usd: 150000.0, nps_score: 72.0,
  },
  {
    customer_id: "cust_002", customer_name: "Meridian Finance", rep_id: "rep_002",
    referral_velocity: "inactive", advocacy_level: "detractor",
    referral_risk: "critical", referral_action: "convert_detractor",
    advocacy_score: 5.0, relationship_depth_score: 22.0,
    referral_propensity_score: 8.0, advocacy_impact_score: 3.0,
    referral_composite: 9.8, estimated_referral_pipeline_usd: 10000.0,
    is_active_referrer: false, needs_advocacy_activation: false,
    primary_advocacy_signal: "NPS -45 — detractor risk, prioritize recovery",
    contract_value_usd: 80000.0, nps_score: -45.0,
  },
  {
    customer_id: "cust_003", customer_name: "Apex Solutions", rep_id: "rep_001",
    referral_velocity: "steady", advocacy_level: "promoter",
    referral_risk: "low", referral_action: "activate_referral",
    advocacy_score: 72.0, relationship_depth_score: 68.0,
    referral_propensity_score: 65.0, advocacy_impact_score: 70.0,
    referral_composite: 69.2, estimated_referral_pipeline_usd: 105000.0,
    is_active_referrer: true, needs_advocacy_activation: false,
    primary_advocacy_signal: "3 referrals given — 2 converted to deals",
    contract_value_usd: 120000.0, nps_score: 58.0,
  },
  {
    customer_id: "cust_004", customer_name: "Orion Healthcare", rep_id: "rep_003",
    referral_velocity: "inactive", advocacy_level: "passive",
    referral_risk: "moderate", referral_action: "nurture_advocate",
    advocacy_score: 48.0, relationship_depth_score: 55.0,
    referral_propensity_score: 42.0, advocacy_impact_score: 38.0,
    referral_composite: 46.5, estimated_referral_pipeline_usd: 35625.0,
    is_active_referrer: false, needs_advocacy_activation: true,
    primary_advocacy_signal: "NPS promoter never asked for referral — activate now",
    contract_value_usd: 95000.0, nps_score: 42.0,
  },
  {
    customer_id: "cust_005", customer_name: "Lumina Retail", rep_id: "rep_002",
    referral_velocity: "accelerating", advocacy_level: "champion",
    referral_risk: "low", referral_action: "activate_referral",
    advocacy_score: 95.0, relationship_depth_score: 92.0,
    referral_propensity_score: 90.0, advocacy_impact_score: 88.0,
    referral_composite: 91.8, estimated_referral_pipeline_usd: 300000.0,
    is_active_referrer: true, needs_advocacy_activation: false,
    primary_advocacy_signal: "5 referrals given — 3 converted to deals",
    contract_value_usd: 200000.0, nps_score: 85.0,
  },
  {
    customer_id: "cust_006", customer_name: "Cascade Logistics", rep_id: "rep_004",
    referral_velocity: "declining", advocacy_level: "passive",
    referral_risk: "high", referral_action: "re_engage",
    advocacy_score: 28.0, relationship_depth_score: 35.0,
    referral_propensity_score: 22.0, advocacy_impact_score: 18.0,
    referral_composite: 26.3, estimated_referral_pipeline_usd: 7500.0,
    is_active_referrer: false, needs_advocacy_activation: false,
    primary_advocacy_signal: "last referral 280 days ago — re-engagement needed",
    contract_value_usd: 60000.0, nps_score: 15.0,
  },
  {
    customer_id: "cust_007", customer_name: "Nexus Energy", rep_id: "rep_003",
    referral_velocity: "steady", advocacy_level: "promoter",
    referral_risk: "low", referral_action: "nurture_advocate",
    advocacy_score: 62.0, relationship_depth_score: 72.0,
    referral_propensity_score: 58.0, advocacy_impact_score: 55.0,
    referral_composite: 62.3, estimated_referral_pipeline_usd: 61250.0,
    is_active_referrer: true, needs_advocacy_activation: false,
    primary_advocacy_signal: "case study agreed — activate for peer referrals",
    contract_value_usd: 110000.0, nps_score: 48.0,
  },
  {
    customer_id: "cust_008", customer_name: "Vertex Pharma", rep_id: "rep_001",
    referral_velocity: "inactive", advocacy_level: "passive",
    referral_risk: "moderate", referral_action: "nurture_advocate",
    advocacy_score: 52.0, relationship_depth_score: 62.0,
    referral_propensity_score: 48.0, advocacy_impact_score: 42.0,
    referral_composite: 52.0, estimated_referral_pipeline_usd: 48750.0,
    is_active_referrer: false, needs_advocacy_activation: true,
    primary_advocacy_signal: "high renewal confidence — strong referral candidate",
    contract_value_usd: 130000.0, nps_score: 35.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const velocity = searchParams.get("velocity");
  const level    = searchParams.get("level");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/customer-referral-intelligence`);
      if (velocity) url.searchParams.set("velocity", velocity);
      if (level)    url.searchParams.set("level", level);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let customers = [...mockCustomers];
  if (velocity) customers = customers.filter((c) => c.referral_velocity === velocity);
  if (level)    customers = customers.filter((c) => c.advocacy_level === level);

  const vel_counts: Record<string, number> = {};
  const adv_counts: Record<string, number> = {};
  const rsk_counts: Record<string, number> = {};
  const act_counts: Record<string, number> = {};
  let total_comp = 0, total_adv = 0, total_rel = 0, total_prop = 0, total_imp = 0, total_pipe = 0;

  for (const c of mockCustomers) {
    vel_counts[c.referral_velocity]  = (vel_counts[c.referral_velocity] || 0) + 1;
    adv_counts[c.advocacy_level]     = (adv_counts[c.advocacy_level] || 0) + 1;
    rsk_counts[c.referral_risk]      = (rsk_counts[c.referral_risk] || 0) + 1;
    act_counts[c.referral_action]    = (act_counts[c.referral_action] || 0) + 1;
    total_comp  += c.referral_composite;
    total_adv   += c.advocacy_score;
    total_rel   += c.relationship_depth_score;
    total_prop  += c.referral_propensity_score;
    total_imp   += c.advocacy_impact_score;
    total_pipe  += c.estimated_referral_pipeline_usd;
  }

  const n = mockCustomers.length;

  return NextResponse.json({
    customers,
    summary: {
      total: n,
      velocity_counts: vel_counts,
      advocacy_counts: adv_counts,
      risk_counts: rsk_counts,
      action_counts: act_counts,
      avg_referral_composite:               Math.round((total_comp / n) * 10) / 10,
      active_referrer_count:                mockCustomers.filter((c) => c.is_active_referrer).length,
      activation_needed_count:              mockCustomers.filter((c) => c.needs_advocacy_activation).length,
      avg_advocacy_score:                   Math.round((total_adv / n) * 10) / 10,
      avg_relationship_depth_score:         Math.round((total_rel / n) * 10) / 10,
      avg_referral_propensity_score:        Math.round((total_prop / n) * 10) / 10,
      avg_advocacy_impact_score:            Math.round((total_imp / n) * 10) / 10,
      total_estimated_referral_pipeline_usd: Math.round(total_pipe),
    },
  });
}
