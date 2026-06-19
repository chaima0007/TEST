import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    leverage_risk: "low", leverage_pattern: "none",
    leverage_severity: "commanding", recommended_action: "no_action",
    tactical_score: 0.0, urgency_score: 0.0,
    discipline_score: 0.0, positioning_score: 0.0,
    leverage_composite: 0.0,
    has_leverage_gap: false, requires_leverage_coaching: false,
    estimated_margin_conceded_usd: 0.0,
    leverage_signal: "Negotiation leverage healthy — tactical use, urgency framing, and concession discipline within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    leverage_risk: "low", leverage_pattern: "none",
    leverage_severity: "commanding", recommended_action: "no_action",
    tactical_score: 3.0, urgency_score: 4.0,
    discipline_score: 2.0, positioning_score: 5.0,
    leverage_composite: 3.45,
    has_leverage_gap: false, requires_leverage_coaching: false,
    estimated_margin_conceded_usd: 0.0,
    leverage_signal: "Negotiation leverage healthy — tactical use, urgency framing, and concession discipline within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    leverage_risk: "moderate", leverage_pattern: "single_lever_dependency",
    leverage_severity: "balanced", recommended_action: "leverage_awareness_coaching",
    tactical_score: 20.0, urgency_score: 18.0,
    discipline_score: 22.0, positioning_score: 15.0,
    leverage_composite: 19.25,
    has_leverage_gap: false, requires_leverage_coaching: true,
    estimated_margin_conceded_usd: 64000.0,
    leverage_signal: "Single lever dependency — 35% concessions without counter-ask — 25% competitive pressure used — 22% value-anchored before price — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    leverage_risk: "moderate", leverage_pattern: "urgency_manufacturing_failure",
    leverage_severity: "balanced", recommended_action: "leverage_awareness_coaching",
    tactical_score: 25.0, urgency_score: 22.0,
    discipline_score: 20.0, positioning_score: 18.0,
    leverage_composite: 21.85,
    has_leverage_gap: false, requires_leverage_coaching: true,
    estimated_margin_conceded_usd: 128000.0,
    leverage_signal: "Urgency manufacturing failure — 38% concessions without counter-ask — 20% competitive pressure used — 28% value-anchored before price — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    leverage_risk: "high", leverage_pattern: "deadline_blind_negotiator",
    leverage_severity: "reactive", recommended_action: "deadline_framing_coaching",
    tactical_score: 42.0, urgency_score: 48.0,
    discipline_score: 38.0, positioning_score: 30.0,
    leverage_composite: 40.15,
    has_leverage_gap: true, requires_leverage_coaching: true,
    estimated_margin_conceded_usd: 432000.0,
    leverage_signal: "Deadline blind negotiator — 48% concessions without counter-ask — 18% competitive pressure used — 20% value-anchored before price — composite 40",
  },
  {
    rep_id: "rep_006", region: "West",
    leverage_risk: "high", leverage_pattern: "competitive_leverage_avoidance",
    leverage_severity: "reactive", recommended_action: "leverage_awareness_coaching",
    tactical_score: 55.0, urgency_score: 45.0,
    discipline_score: 48.0, positioning_score: 52.0,
    leverage_composite: 50.45,
    has_leverage_gap: true, requires_leverage_coaching: true,
    estimated_margin_conceded_usd: 720000.0,
    leverage_signal: "Competitive leverage avoidance — 52% concessions without counter-ask — 12% competitive pressure used — 18% value-anchored before price — composite 50",
  },
  {
    rep_id: "rep_007", region: "APAC",
    leverage_risk: "critical", leverage_pattern: "concession_without_ask",
    leverage_severity: "powerless", recommended_action: "concession_discipline_coaching",
    tactical_score: 72.0, urgency_score: 68.0,
    discipline_score: 75.0, positioning_score: 65.0,
    leverage_composite: 71.05,
    has_leverage_gap: true, requires_leverage_coaching: true,
    estimated_margin_conceded_usd: 1680000.0,
    leverage_signal: "Concession without ask — 62% concessions without counter-ask — 8% competitive pressure used — 12% value-anchored before price — composite 71",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    leverage_risk: "critical", leverage_pattern: "concession_without_ask",
    leverage_severity: "powerless", recommended_action: "concession_discipline_coaching",
    tactical_score: 100.0, urgency_score: 100.0,
    discipline_score: 100.0, positioning_score: 100.0,
    leverage_composite: 100.0,
    has_leverage_gap: true, requires_leverage_coaching: true,
    estimated_margin_conceded_usd: 3640000.0,
    leverage_signal: "Concession without ask — 70% concessions without counter-ask — 5% competitive pressure used — 10% value-anchored before price — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-negotiation-leverage-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.leverage_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.leverage_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_tac = 0, total_urg = 0, total_dis = 0, total_pos = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.leverage_risk]         = (risk_counts[r.leverage_risk] || 0) + 1;
    pattern_counts[r.leverage_pattern]   = (pattern_counts[r.leverage_pattern] || 0) + 1;
    severity_counts[r.leverage_severity] = (severity_counts[r.leverage_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.leverage_composite;
    total_tac  += r.tactical_score;
    total_urg  += r.urgency_score;
    total_dis  += r.discipline_score;
    total_pos  += r.positioning_score;
    total_loss += r.estimated_margin_conceded_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                   n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_leverage_composite:                  Math.round((total_comp / n) * 10) / 10,
      leverage_gap_count:                      mockReps.filter((r) => r.has_leverage_gap).length,
      coaching_count:                          mockReps.filter((r) => r.requires_leverage_coaching).length,
      avg_tactical_score:                      Math.round((total_tac / n) * 10) / 10,
      avg_urgency_score:                       Math.round((total_urg / n) * 10) / 10,
      avg_discipline_score:                    Math.round((total_dis / n) * 10) / 10,
      avg_positioning_score:                   Math.round((total_pos / n) * 10) / 10,
      total_estimated_margin_conceded_usd:     Math.round(total_loss * 100) / 100,
    },
  });
}
