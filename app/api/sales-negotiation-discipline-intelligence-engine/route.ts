import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    negotiation_risk: "low", negotiation_pattern: "none",
    negotiation_severity: "clean", recommended_action: "no_action",
    discount_discipline_score: 0.0, concession_behavior_score: 0.0,
    deal_construction_score: 0.0, close_effectiveness_score: 0.0,
    negotiation_composite: 0.0,
    has_negotiation_gap: false, requires_negotiation_coaching: false,
    estimated_revenue_dilution_usd: 0.0,
    negotiation_signal: "Negotiation discipline strong — discount defense, concession sequencing, and deal construction within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    negotiation_risk: "low", negotiation_pattern: "none",
    negotiation_severity: "clean", recommended_action: "no_action",
    discount_discipline_score: 5.0, concession_behavior_score: 4.0,
    deal_construction_score: 3.0, close_effectiveness_score: 5.0,
    negotiation_composite: 4.2,
    has_negotiation_gap: false, requires_negotiation_coaching: false,
    estimated_revenue_dilution_usd: 0.0,
    negotiation_signal: "Negotiation discipline strong — discount defense, concession sequencing, and deal construction within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    negotiation_risk: "moderate", negotiation_pattern: "none",
    negotiation_severity: "managing", recommended_action: "negotiation_process_coaching",
    discount_discipline_score: 22.0, concession_behavior_score: 18.0,
    deal_construction_score: 20.0, close_effectiveness_score: 15.0,
    negotiation_composite: 19.7,
    has_negotiation_gap: false, requires_negotiation_coaching: false,
    estimated_revenue_dilution_usd: 0.0,
    negotiation_signal: "Negotiation risk — 12% avg discount given — 25% concessions without value exchange — 18% closed at list price — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    negotiation_risk: "moderate", negotiation_pattern: "late_stage_collapse",
    negotiation_severity: "managing", recommended_action: "negotiation_process_coaching",
    discount_discipline_score: 18.0, concession_behavior_score: 20.0,
    deal_construction_score: 22.0, close_effectiveness_score: 30.0,
    negotiation_composite: 21.3,
    has_negotiation_gap: false, requires_negotiation_coaching: false,
    estimated_revenue_dilution_usd: 51120.0,
    negotiation_signal: "Late stage collapse — 15% avg discount given — 30% concessions without value exchange — 12% closed at list price — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    negotiation_risk: "high", negotiation_pattern: "single_threaded_close",
    negotiation_severity: "struggling", recommended_action: "stakeholder_expansion_coaching",
    discount_discipline_score: 45.0, concession_behavior_score: 35.0,
    deal_construction_score: 55.0, close_effectiveness_score: 30.0,
    negotiation_composite: 42.5,
    has_negotiation_gap: true, requires_negotiation_coaching: true,
    estimated_revenue_dilution_usd: 382500.0,
    negotiation_signal: "Single threaded close — 22% avg discount given — 45% concessions without value exchange — 8% closed at list price — composite 43",
  },
  {
    rep_id: "rep_006", region: "West",
    negotiation_risk: "high", negotiation_pattern: "value_cave",
    negotiation_severity: "struggling", recommended_action: "negotiation_process_coaching",
    discount_discipline_score: 40.0, concession_behavior_score: 55.0,
    deal_construction_score: 40.0, close_effectiveness_score: 35.0,
    negotiation_composite: 44.0,
    has_negotiation_gap: true, requires_negotiation_coaching: true,
    estimated_revenue_dilution_usd: 528000.0,
    negotiation_signal: "Value cave — 25% avg discount given — 55% concessions without value exchange — 10% closed at list price — composite 44",
  },
  {
    rep_id: "rep_007", region: "APAC",
    negotiation_risk: "critical", negotiation_pattern: "chronic_discounter",
    negotiation_severity: "collapsing", recommended_action: "discount_defense_intervention",
    discount_discipline_score: 75.0, concession_behavior_score: 65.0,
    deal_construction_score: 60.0, close_effectiveness_score: 55.0,
    negotiation_composite: 66.8,
    has_negotiation_gap: true, requires_negotiation_coaching: true,
    estimated_revenue_dilution_usd: 1337500.0,
    negotiation_signal: "Chronic discounter — 35% avg discount given — 65% concessions without value exchange — 5% closed at list price — composite 67",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    negotiation_risk: "critical", negotiation_pattern: "chronic_discounter",
    negotiation_severity: "collapsing", recommended_action: "discount_defense_intervention",
    discount_discipline_score: 100.0, concession_behavior_score: 100.0,
    deal_construction_score: 100.0, close_effectiveness_score: 100.0,
    negotiation_composite: 100.0,
    has_negotiation_gap: true, requires_negotiation_coaching: true,
    estimated_revenue_dilution_usd: 1600000.0,
    negotiation_signal: "Chronic discounter — 40% avg discount given — 80% concessions without value exchange — 5% closed at list price — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-negotiation-discipline-intelligence-engine`);
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
  let total_comp = 0, total_dis = 0, total_con = 0, total_con2 = 0, total_clo = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.negotiation_risk]         = (risk_counts[r.negotiation_risk] || 0) + 1;
    pattern_counts[r.negotiation_pattern]   = (pattern_counts[r.negotiation_pattern] || 0) + 1;
    severity_counts[r.negotiation_severity] = (severity_counts[r.negotiation_severity] || 0) + 1;
    action_counts[r.recommended_action]     = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.negotiation_composite;
    total_dis   += r.discount_discipline_score;
    total_con   += r.concession_behavior_score;
    total_con2  += r.deal_construction_score;
    total_clo   += r.close_effectiveness_score;
    total_loss  += r.estimated_revenue_dilution_usd;
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
      negotiation_gap_count:                  mockReps.filter((r) => r.has_negotiation_gap).length,
      coaching_count:                         mockReps.filter((r) => r.requires_negotiation_coaching).length,
      avg_discount_discipline_score:          Math.round((total_dis / n) * 10) / 10,
      avg_concession_behavior_score:          Math.round((total_con / n) * 10) / 10,
      avg_deal_construction_score:            Math.round((total_con2 / n) * 10) / 10,
      avg_close_effectiveness_score:          Math.round((total_clo / n) * 10) / 10,
      total_estimated_revenue_dilution_usd:   Math.round(total_loss * 100) / 100,
    },
  });
}
