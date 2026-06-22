import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-pricing-negotiation-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    negotiation_risk: "low", negotiation_pattern: "none",
    negotiation_severity: "disciplined", recommended_action: "no_action",
    discount_discipline_score: 0.0, value_retention_score: 0.0,
    margin_protection_score: 0.0, negotiation_efficiency_score: 0.0,
    negotiation_effectiveness_composite: 0.0, is_margin_at_risk: false,
    requires_pricing_intervention: false, estimated_margin_loss_usd: 0.0,
    negotiation_signal: "Pricing discipline maintained across negotiations",
  },
  {
    rep_id: "rep_002", region: "East",
    negotiation_risk: "low", negotiation_pattern: "none",
    negotiation_severity: "disciplined", recommended_action: "no_action",
    discount_discipline_score: 7.0, value_retention_score: 0.0,
    margin_protection_score: 8.0, negotiation_efficiency_score: 5.0,
    negotiation_effectiveness_composite: 5.0, is_margin_at_risk: false,
    requires_pricing_intervention: false, estimated_margin_loss_usd: 0.0,
    negotiation_signal: "Pricing discipline maintained across negotiations",
  },
  {
    rep_id: "rep_003", region: "Central",
    negotiation_risk: "moderate", negotiation_pattern: "price_concession_habit",
    negotiation_severity: "lenient", recommended_action: "discount_discipline_review",
    discount_discipline_score: 22.0, value_retention_score: 18.0,
    margin_protection_score: 15.0, negotiation_efficiency_score: 30.0,
    negotiation_effectiveness_composite: 20.0, is_margin_at_risk: false,
    requires_pricing_intervention: false, estimated_margin_loss_usd: 4800.0,
    negotiation_signal: "Price concession habit — 12% avg discount — 2.5 avg concession rounds — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    negotiation_risk: "moderate", negotiation_pattern: "value_erosion",
    negotiation_severity: "lenient", recommended_action: "discount_discipline_review",
    discount_discipline_score: 18.0, value_retention_score: 30.0,
    margin_protection_score: 20.0, negotiation_efficiency_score: 18.0,
    negotiation_effectiveness_composite: 22.0, is_margin_at_risk: false,
    requires_pricing_intervention: true, estimated_margin_loss_usd: 9500.0,
    negotiation_signal: "Value erosion — 15% avg discount — 1 below-floor deals — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    negotiation_risk: "high", negotiation_pattern: "chronic_discounting",
    negotiation_severity: "compromised", recommended_action: "discount_discipline_review",
    discount_discipline_score: 45.0, value_retention_score: 30.0,
    margin_protection_score: 28.0, negotiation_efficiency_score: 25.0,
    negotiation_effectiveness_composite: 34.0, is_margin_at_risk: false,
    requires_pricing_intervention: true, estimated_margin_loss_usd: 36000.0,
    negotiation_signal: "Chronic discounting — 22% avg discount — 3 below-floor deals — 3.0 avg concession rounds — composite 34",
  },
  {
    rep_id: "rep_006", region: "West",
    negotiation_risk: "high", negotiation_pattern: "competitive_surrender",
    negotiation_severity: "compromised", recommended_action: "negotiation_coaching",
    discount_discipline_score: 38.0, value_retention_score: 35.0,
    margin_protection_score: 40.0, negotiation_efficiency_score: 38.0,
    negotiation_effectiveness_composite: 37.0, is_margin_at_risk: true,
    requires_pricing_intervention: true, estimated_margin_loss_usd: 58000.0,
    negotiation_signal: "Competitive surrender — 25% avg discount — 4 below-floor deals — 3.5 avg concession rounds — composite 37",
  },
  {
    rep_id: "rep_007", region: "APAC",
    negotiation_risk: "critical", negotiation_pattern: "chronic_discounting",
    negotiation_severity: "collapsing", recommended_action: "pricing_floor_enforcement",
    discount_discipline_score: 65.0, value_retention_score: 55.0,
    margin_protection_score: 60.0, negotiation_efficiency_score: 55.0,
    negotiation_effectiveness_composite: 60.0, is_margin_at_risk: true,
    requires_pricing_intervention: true, estimated_margin_loss_usd: 150000.0,
    negotiation_signal: "Chronic discounting — 35% avg discount — 7 below-floor deals — 4.5 avg concession rounds — composite 60",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    negotiation_risk: "critical", negotiation_pattern: "margin_collapse",
    negotiation_severity: "collapsing", recommended_action: "deal_desk_escalation",
    discount_discipline_score: 75.0, value_retention_score: 70.0,
    margin_protection_score: 80.0, negotiation_efficiency_score: 65.0,
    negotiation_effectiveness_composite: 73.0, is_margin_at_risk: true,
    requires_pricing_intervention: true, estimated_margin_loss_usd: 320000.0,
    negotiation_signal: "Margin collapse — 45% avg discount — 10 below-floor deals — 5.0 avg concession rounds — 4 lost on price alone — composite 73",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-pricing-negotiation-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.negotiation_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.negotiation_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_disc = 0, total_val = 0, total_mar = 0, total_eff = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.negotiation_risk]         = (risk_counts[r.negotiation_risk] || 0) + 1;
    pattern_counts[r.negotiation_pattern]   = (pattern_counts[r.negotiation_pattern] || 0) + 1;
    severity_counts[r.negotiation_severity] = (severity_counts[r.negotiation_severity] || 0) + 1;
    action_counts[r.recommended_action]     = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.negotiation_effectiveness_composite;
    total_disc += r.discount_discipline_score;
    total_val  += r.value_retention_score;
    total_mar  += r.margin_protection_score;
    total_eff  += r.negotiation_efficiency_score;
    total_loss += r.estimated_margin_loss_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_negotiation_effectiveness_composite:  Math.round((total_comp / n) * 10) / 10,
      margin_at_risk_count:                     mockReps.filter((r) => r.is_margin_at_risk).length,
      pricing_intervention_count:               mockReps.filter((r) => r.requires_pricing_intervention).length,
      avg_discount_discipline_score:            Math.round((total_disc / n) * 10) / 10,
      avg_value_retention_score:                Math.round((total_val / n) * 10) / 10,
      avg_margin_protection_score:              Math.round((total_mar / n) * 10) / 10,
      avg_negotiation_efficiency_score:         Math.round((total_eff / n) * 10) / 10,
      total_estimated_margin_loss_usd:          Math.round(total_loss * 100) / 100,
    },
  }));
}
