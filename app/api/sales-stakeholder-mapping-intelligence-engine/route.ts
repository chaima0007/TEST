import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    stakeholder_risk: "low", stakeholder_pattern: "none",
    stakeholder_severity: "engaged", recommended_action: "no_action",
    coverage_breadth_score: 0.0, buyer_alignment_score: 0.0,
    champion_development_score: 0.0, executive_access_score: 0.0,
    stakeholder_effectiveness_composite: 0.0,
    has_stakeholder_gap: false, requires_stakeholder_coaching: false,
    estimated_deal_risk_usd: 0.0,
    stakeholder_signal: "Stakeholder engagement and multi-threading on track",
  },
  {
    rep_id: "rep_002", region: "East",
    stakeholder_risk: "low", stakeholder_pattern: "none",
    stakeholder_severity: "engaged", recommended_action: "no_action",
    coverage_breadth_score: 5.0, buyer_alignment_score: 5.0,
    champion_development_score: 5.0, executive_access_score: 5.0,
    stakeholder_effectiveness_composite: 5.0,
    has_stakeholder_gap: false, requires_stakeholder_coaching: false,
    estimated_deal_risk_usd: 0.0,
    stakeholder_signal: "Stakeholder engagement and multi-threading on track",
  },
  {
    rep_id: "rep_003", region: "Central",
    stakeholder_risk: "moderate", stakeholder_pattern: "poor_stakeholder_advancement",
    stakeholder_severity: "developing", recommended_action: "multi_threading_coaching",
    coverage_breadth_score: 15.0, buyer_alignment_score: 25.0,
    champion_development_score: 18.0, executive_access_score: 20.0,
    stakeholder_effectiveness_composite: 19.45,
    has_stakeholder_gap: false, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 14000.0,
    stakeholder_signal: "Poor stakeholder advancement — 3 single-threaded deals — 4 champions identified — 2 exec sponsors engaged — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    stakeholder_risk: "moderate", stakeholder_pattern: "champion_gap",
    stakeholder_severity: "developing", recommended_action: "multi_threading_coaching",
    coverage_breadth_score: 10.0, buyer_alignment_score: 20.0,
    champion_development_score: 30.0, executive_access_score: 15.0,
    stakeholder_effectiveness_composite: 18.75,
    has_stakeholder_gap: false, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 18000.0,
    stakeholder_signal: "Champion gap — 2 single-threaded deals — 2 champions identified — 1 exec sponsors engaged — composite 19",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    stakeholder_risk: "high", stakeholder_pattern: "no_economic_buyer",
    stakeholder_severity: "fragile", recommended_action: "multi_threading_coaching",
    coverage_breadth_score: 25.0, buyer_alignment_score: 38.0,
    champion_development_score: 28.0, executive_access_score: 30.0,
    stakeholder_effectiveness_composite: 30.2,
    has_stakeholder_gap: false, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 45000.0,
    stakeholder_signal: "No economic buyer — 5 single-threaded deals — 3 champions identified — 1 exec sponsors engaged — composite 30",
  },
  {
    rep_id: "rep_006", region: "West",
    stakeholder_risk: "high", stakeholder_pattern: "single_threaded",
    stakeholder_severity: "fragile", recommended_action: "multi_threading_coaching",
    coverage_breadth_score: 45.0, buyer_alignment_score: 28.0,
    champion_development_score: 22.0, executive_access_score: 25.0,
    stakeholder_effectiveness_composite: 31.05,
    has_stakeholder_gap: true, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 70000.0,
    stakeholder_signal: "Single threaded — 6 single-threaded deals — 2 champions identified — 0 exec sponsors engaged — composite 31",
  },
  {
    rep_id: "rep_007", region: "APAC",
    stakeholder_risk: "critical", stakeholder_pattern: "single_threaded",
    stakeholder_severity: "exposed", recommended_action: "multi_threading_coaching",
    coverage_breadth_score: 70.0, buyer_alignment_score: 55.0,
    champion_development_score: 55.0, executive_access_score: 50.0,
    stakeholder_effectiveness_composite: 59.5,
    has_stakeholder_gap: true, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 180000.0,
    stakeholder_signal: "Single threaded — 9 single-threaded deals — 1 champions identified — 0 exec sponsors engaged — composite 60",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    stakeholder_risk: "critical", stakeholder_pattern: "no_economic_buyer",
    stakeholder_severity: "exposed", recommended_action: "economic_buyer_strategy",
    coverage_breadth_score: 75.0, buyer_alignment_score: 70.0,
    champion_development_score: 65.0, executive_access_score: 60.0,
    stakeholder_effectiveness_composite: 68.25,
    has_stakeholder_gap: true, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 320000.0,
    stakeholder_signal: "No economic buyer — 10 single-threaded deals — 0 champions identified — 0 exec sponsors engaged — composite 68",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-stakeholder-mapping-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.stakeholder_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.stakeholder_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_cov = 0, total_buy = 0, total_champ = 0, total_exec = 0, total_risk = 0;

  for (const r of mockReps) {
    risk_counts[r.stakeholder_risk]       = (risk_counts[r.stakeholder_risk] || 0) + 1;
    pattern_counts[r.stakeholder_pattern] = (pattern_counts[r.stakeholder_pattern] || 0) + 1;
    severity_counts[r.stakeholder_severity] = (severity_counts[r.stakeholder_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.stakeholder_effectiveness_composite;
    total_cov   += r.coverage_breadth_score;
    total_buy   += r.buyer_alignment_score;
    total_champ += r.champion_development_score;
    total_exec  += r.executive_access_score;
    total_risk  += r.estimated_deal_risk_usd;
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
      avg_stakeholder_effectiveness_composite:  Math.round((total_comp / n) * 10) / 10,
      stakeholder_gap_count:                    mockReps.filter((r) => r.has_stakeholder_gap).length,
      stakeholder_coaching_count:               mockReps.filter((r) => r.requires_stakeholder_coaching).length,
      avg_coverage_breadth_score:               Math.round((total_cov / n) * 10) / 10,
      avg_buyer_alignment_score:                Math.round((total_buy / n) * 10) / 10,
      avg_champion_development_score:           Math.round((total_champ / n) * 10) / 10,
      avg_executive_access_score:               Math.round((total_exec / n) * 10) / 10,
      total_estimated_deal_risk_usd:            Math.round(total_risk * 100) / 100,
    },
  });
}
