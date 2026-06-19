import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    deal_desk_risk: "low", deal_desk_pattern: "none",
    deal_desk_severity: "autonomous", recommended_action: "no_action",
    approval_dependency_score: 0.0, exception_complexity_score: 0.0,
    exception_urgency_score: 0.0, exception_impact_score: 0.0,
    deal_desk_composite: 0.0,
    has_deal_desk_gap: false, requires_deal_desk_coaching: false,
    estimated_margin_risk_usd: 0.0,
    deal_desk_signal: "Deal desk utilization healthy — pricing discipline and exception management within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    deal_desk_risk: "low", deal_desk_pattern: "none",
    deal_desk_severity: "autonomous", recommended_action: "no_action",
    approval_dependency_score: 3.0, exception_complexity_score: 2.0,
    exception_urgency_score: 4.0, exception_impact_score: 1.0,
    deal_desk_composite: 2.65,
    has_deal_desk_gap: false, requires_deal_desk_coaching: false,
    estimated_margin_risk_usd: 0.0,
    deal_desk_signal: "Deal desk utilization healthy — pricing discipline and exception management within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    deal_desk_risk: "moderate", deal_desk_pattern: "competitive_capitulation",
    deal_desk_severity: "developing", recommended_action: "pricing_authority_coaching",
    approval_dependency_score: 15.0, exception_complexity_score: 18.0,
    exception_urgency_score: 25.0, exception_impact_score: 10.0,
    deal_desk_composite: 17.85,
    has_deal_desk_gap: false, requires_deal_desk_coaching: false,
    estimated_margin_risk_usd: 9000.0,
    deal_desk_signal: "Competitive capitulation — 18% deals need approval — 22% late-stage escalations — 1.5 avg desk cycles — composite 18",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    deal_desk_risk: "moderate", deal_desk_pattern: "discount_authority_abuse",
    deal_desk_severity: "developing", recommended_action: "pricing_authority_coaching",
    approval_dependency_score: 32.0, exception_complexity_score: 12.0,
    exception_urgency_score: 15.0, exception_impact_score: 18.0,
    deal_desk_composite: 20.7,
    has_deal_desk_gap: false, requires_deal_desk_coaching: true,
    estimated_margin_risk_usd: 16800.0,
    deal_desk_signal: "Discount authority abuse — 28% deals need approval — 28% late-stage escalations — 1.8 avg desk cycles — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    deal_desk_risk: "high", deal_desk_pattern: "last_minute_escalation",
    deal_desk_severity: "dependent", recommended_action: "deal_desk_training",
    approval_dependency_score: 32.0, exception_complexity_score: 30.0,
    exception_urgency_score: 55.0, exception_impact_score: 25.0,
    deal_desk_composite: 36.5,
    has_deal_desk_gap: true, requires_deal_desk_coaching: true,
    estimated_margin_risk_usd: 72000.0,
    deal_desk_signal: "Last minute escalation — 42% deals need approval — 52% late-stage escalations — 2.2 avg desk cycles — composite 37",
  },
  {
    rep_id: "rep_006", region: "West",
    deal_desk_risk: "high", deal_desk_pattern: "deal_desk_dependent",
    deal_desk_severity: "dependent", recommended_action: "deal_desk_training",
    approval_dependency_score: 55.0, exception_complexity_score: 35.0,
    exception_urgency_score: 30.0, exception_impact_score: 38.0,
    deal_desk_composite: 41.75,
    has_deal_desk_gap: true, requires_deal_desk_coaching: true,
    estimated_margin_risk_usd: 108000.0,
    deal_desk_signal: "Deal desk dependent — 55% deals need approval — 45% late-stage escalations — 2.8 avg desk cycles — composite 42",
  },
  {
    rep_id: "rep_007", region: "APAC",
    deal_desk_risk: "critical", deal_desk_pattern: "legal_escalation_pattern",
    deal_desk_severity: "entrenched", recommended_action: "legal_escalation_reduction",
    approval_dependency_score: 72.0, exception_complexity_score: 78.0,
    exception_urgency_score: 58.0, exception_impact_score: 52.0,
    deal_desk_composite: 67.0,
    has_deal_desk_gap: true, requires_deal_desk_coaching: true,
    estimated_margin_risk_usd: 216000.0,
    deal_desk_signal: "Legal escalation pattern — 65% deals need approval — 60% late-stage escalations — 3.2 avg desk cycles — composite 67",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    deal_desk_risk: "critical", deal_desk_pattern: "deal_desk_dependent",
    deal_desk_severity: "entrenched", recommended_action: "deal_desk_intervention",
    approval_dependency_score: 100.0, exception_complexity_score: 100.0,
    exception_urgency_score: 100.0, exception_impact_score: 100.0,
    deal_desk_composite: 100.0,
    has_deal_desk_gap: true, requires_deal_desk_coaching: true,
    estimated_margin_risk_usd: 325000.0,
    deal_desk_signal: "Deal desk dependent — 72% deals need approval — 68% late-stage escalations — 3.5 avg desk cycles — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-deal-desk-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.deal_desk_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.deal_desk_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_app = 0, total_cpx = 0, total_urg = 0, total_imp = 0, total_impact = 0;

  for (const r of mockReps) {
    risk_counts[r.deal_desk_risk]       = (risk_counts[r.deal_desk_risk] || 0) + 1;
    pattern_counts[r.deal_desk_pattern] = (pattern_counts[r.deal_desk_pattern] || 0) + 1;
    severity_counts[r.deal_desk_severity] = (severity_counts[r.deal_desk_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.deal_desk_composite;
    total_app    += r.approval_dependency_score;
    total_cpx    += r.exception_complexity_score;
    total_urg    += r.exception_urgency_score;
    total_imp    += r.exception_impact_score;
    total_impact += r.estimated_margin_risk_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_deal_desk_composite:                  Math.round((total_comp / n) * 10) / 10,
      deal_desk_gap_count:                      mockReps.filter((r) => r.has_deal_desk_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_deal_desk_coaching).length,
      avg_approval_dependency_score:            Math.round((total_app / n) * 10) / 10,
      avg_exception_complexity_score:           Math.round((total_cpx / n) * 10) / 10,
      avg_exception_urgency_score:              Math.round((total_urg / n) * 10) / 10,
      avg_exception_impact_score:               Math.round((total_imp / n) * 10) / 10,
      total_estimated_margin_risk_usd:          Math.round(total_impact * 100) / 100,
    },
  });
}
