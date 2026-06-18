import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    negotiation_risk: "low", negotiation_pattern: "none",
    negotiation_severity: "strong", recommended_action: "no_action",
    discount_discipline_score: 0.0, concession_behavior_score: 0.0,
    value_defense_score: 0.0, close_effectiveness_score: 0.0,
    negotiation_composite: 0.0,
    has_pricing_risk: false, requires_negotiation_coaching: false,
    estimated_margin_erosion_usd: 0.0,
    negotiation_signal: "Negotiation effectiveness healthy — pricing discipline and value defense within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    negotiation_risk: "low", negotiation_pattern: "none",
    negotiation_severity: "strong", recommended_action: "no_action",
    discount_discipline_score: 5.0, concession_behavior_score: 3.0,
    value_defense_score: 4.0, close_effectiveness_score: 2.0,
    negotiation_composite: 3.8,
    has_pricing_risk: false, requires_negotiation_coaching: false,
    estimated_margin_erosion_usd: 0.0,
    negotiation_signal: "Negotiation effectiveness healthy — pricing discipline and value defense within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    negotiation_risk: "moderate", negotiation_pattern: "negotiation_avoidance",
    negotiation_severity: "developing", recommended_action: "negotiation_coaching",
    discount_discipline_score: 15.0, concession_behavior_score: 20.0,
    value_defense_score: 18.0, close_effectiveness_score: 22.0,
    negotiation_composite: 18.3,
    has_pricing_risk: false, requires_negotiation_coaching: false,
    estimated_margin_erosion_usd: 12600.0,
    negotiation_signal: "Negotiation avoidance — 12% avg discount — 4d first concession — 88% of target ACV — composite 18",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    negotiation_risk: "moderate", negotiation_pattern: "value_abandonment",
    negotiation_severity: "developing", recommended_action: "negotiation_coaching",
    discount_discipline_score: 22.0, concession_behavior_score: 18.0,
    value_defense_score: 26.0, close_effectiveness_score: 14.0,
    negotiation_composite: 21.0,
    has_pricing_risk: false, requires_negotiation_coaching: true,
    estimated_margin_erosion_usd: 24500.0,
    negotiation_signal: "Value abandonment — 15% avg discount — 5d first concession — 85% of target ACV — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    negotiation_risk: "high", negotiation_pattern: "premature_concession",
    negotiation_severity: "vulnerable", recommended_action: "negotiation_coaching",
    discount_discipline_score: 35.0, concession_behavior_score: 48.0,
    value_defense_score: 30.0, close_effectiveness_score: 28.0,
    negotiation_composite: 36.45,
    has_pricing_risk: true, requires_negotiation_coaching: true,
    estimated_margin_erosion_usd: 68400.0,
    negotiation_signal: "Premature concession — 20% avg discount — 1d first concession — 82% of target ACV — composite 36",
  },
  {
    rep_id: "rep_006", region: "West",
    negotiation_risk: "high", negotiation_pattern: "price_erosion",
    negotiation_severity: "vulnerable", recommended_action: "discount_authority_review",
    discount_discipline_score: 40.0, concession_behavior_score: 32.0,
    value_defense_score: 45.0, close_effectiveness_score: 35.0,
    negotiation_composite: 38.95,
    has_pricing_risk: true, requires_negotiation_coaching: true,
    estimated_margin_erosion_usd: 96250.0,
    negotiation_signal: "Price erosion — 22% avg discount — 3d first concession — 78% of target ACV — composite 39",
  },
  {
    rep_id: "rep_007", region: "APAC",
    negotiation_risk: "critical", negotiation_pattern: "excessive_discounting",
    negotiation_severity: "collapsing", recommended_action: "deal_desk_escalation",
    discount_discipline_score: 70.0, concession_behavior_score: 60.0,
    value_defense_score: 55.0, close_effectiveness_score: 50.0,
    negotiation_composite: 60.25,
    has_pricing_risk: true, requires_negotiation_coaching: true,
    estimated_margin_erosion_usd: 168000.0,
    negotiation_signal: "Excessive discounting — 28% avg discount — 1d first concession — 73% of target ACV — composite 60",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    negotiation_risk: "critical", negotiation_pattern: "excessive_discounting",
    negotiation_severity: "collapsing", recommended_action: "pricing_integrity_program",
    discount_discipline_score: 85.0, concession_behavior_score: 75.0,
    value_defense_score: 80.0, close_effectiveness_score: 70.0,
    negotiation_composite: 79.0,
    has_pricing_risk: true, requires_negotiation_coaching: true,
    estimated_margin_erosion_usd: 196672.0,
    negotiation_signal: "Excessive discounting — 28% avg discount — 2d first concession — 72% of target ACV — composite 88",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-negotiation-effectiveness-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.negotiation_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.negotiation_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_disc = 0, total_conc = 0, total_val = 0, total_close = 0, total_erosion = 0;

  for (const r of mockReps) {
    risk_counts[r.negotiation_risk]       = (risk_counts[r.negotiation_risk] || 0) + 1;
    pattern_counts[r.negotiation_pattern] = (pattern_counts[r.negotiation_pattern] || 0) + 1;
    severity_counts[r.negotiation_severity] = (severity_counts[r.negotiation_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp    += r.negotiation_composite;
    total_disc    += r.discount_discipline_score;
    total_conc    += r.concession_behavior_score;
    total_val     += r.value_defense_score;
    total_close   += r.close_effectiveness_score;
    total_erosion += r.estimated_margin_erosion_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                  n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_negotiation_composite:              Math.round((total_comp / n) * 10) / 10,
      pricing_risk_count:                     mockReps.filter((r) => r.has_pricing_risk).length,
      coaching_count:                         mockReps.filter((r) => r.requires_negotiation_coaching).length,
      avg_discount_discipline_score:          Math.round((total_disc / n) * 10) / 10,
      avg_concession_behavior_score:          Math.round((total_conc / n) * 10) / 10,
      avg_value_defense_score:                Math.round((total_val / n) * 10) / 10,
      avg_close_effectiveness_score:          Math.round((total_close / n) * 10) / 10,
      total_estimated_margin_erosion_usd:     Math.round(total_erosion * 100) / 100,
    },
  });
}
