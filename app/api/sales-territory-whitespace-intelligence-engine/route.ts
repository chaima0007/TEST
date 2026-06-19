import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    territory_risk: "low", territory_pattern: "none",
    territory_severity: "optimal", recommended_action: "no_action",
    coverage_score: 0.0, penetration_score: 0.0,
    growth_score: 0.0, competitive_score: 0.0,
    territory_composite: 0.0,
    has_territory_gap: false, requires_territory_coaching: false,
    estimated_whitespace_opportunity_usd: 0.0,
    territory_signal: "Territory coverage strong — ICP engagement, new logo pursuit, and competitive displacement within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    territory_risk: "low", territory_pattern: "none",
    territory_severity: "optimal", recommended_action: "no_action",
    coverage_score: 4.0, penetration_score: 3.0,
    growth_score: 5.0, competitive_score: 2.0,
    territory_composite: 3.65,
    has_territory_gap: false, requires_territory_coaching: false,
    estimated_whitespace_opportunity_usd: 0.0,
    territory_signal: "Territory coverage strong — ICP engagement, new logo pursuit, and competitive displacement within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    territory_risk: "moderate", territory_pattern: "none",
    territory_severity: "acceptable", recommended_action: "territory_planning_coaching",
    coverage_score: 20.0, penetration_score: 18.0,
    growth_score: 22.0, competitive_score: 15.0,
    territory_composite: 19.55,
    has_territory_gap: false, requires_territory_coaching: true,
    estimated_whitespace_opportunity_usd: 312000.0,
    territory_signal: "Territory risk — 48% ICP accounts engaged — 12% new logos acquired — 22% dormant 90d — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    territory_risk: "moderate", territory_pattern: "vertical_concentration",
    territory_severity: "acceptable", recommended_action: "territory_planning_coaching",
    coverage_score: 18.0, penetration_score: 22.0,
    growth_score: 20.0, competitive_score: 28.0,
    territory_composite: 21.2,
    has_territory_gap: false, requires_territory_coaching: true,
    estimated_whitespace_opportunity_usd: 576000.0,
    territory_signal: "Vertical concentration — 45% ICP accounts engaged — 10% new logos acquired — 20% dormant 90d — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    territory_risk: "high", territory_pattern: "expansion_neglect",
    territory_severity: "concerning", recommended_action: "new_logo_coaching",
    coverage_score: 38.0, penetration_score: 35.0,
    growth_score: 55.0, competitive_score: 30.0,
    territory_composite: 40.25,
    has_territory_gap: true, requires_territory_coaching: true,
    estimated_whitespace_opportunity_usd: 1890000.0,
    territory_signal: "Expansion neglect — 30% ICP accounts engaged — 5% new logos acquired — 35% dormant 90d — composite 40",
  },
  {
    rep_id: "rep_006", region: "West",
    territory_risk: "high", territory_pattern: "competitive_blindspot",
    territory_severity: "concerning", recommended_action: "competitive_territory_coaching",
    coverage_score: 42.0, penetration_score: 40.0,
    growth_score: 38.0, competitive_score: 55.0,
    territory_composite: 43.25,
    has_territory_gap: true, requires_territory_coaching: true,
    estimated_whitespace_opportunity_usd: 2520000.0,
    territory_signal: "Competitive blindspot — 28% ICP accounts engaged — 8% new logos acquired — 40% dormant 90d — composite 43",
  },
  {
    rep_id: "rep_007", region: "APAC",
    territory_risk: "critical", territory_pattern: "coverage_avoidance",
    territory_severity: "stagnant", recommended_action: "territory_coverage_intervention",
    coverage_score: 72.0, penetration_score: 68.0,
    growth_score: 65.0, competitive_score: 58.0,
    territory_composite: 67.15,
    has_territory_gap: true, requires_territory_coaching: true,
    estimated_whitespace_opportunity_usd: 8100000.0,
    territory_signal: "Coverage avoidance — 15% ICP accounts engaged — 3% new logos acquired — 72% dormant 90d — composite 67",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    territory_risk: "critical", territory_pattern: "coverage_avoidance",
    territory_severity: "stagnant", recommended_action: "territory_strategy_reset",
    coverage_score: 100.0, penetration_score: 100.0,
    growth_score: 100.0, competitive_score: 100.0,
    territory_composite: 100.0,
    has_territory_gap: true, requires_territory_coaching: true,
    estimated_whitespace_opportunity_usd: 21600000.0,
    territory_signal: "Coverage avoidance — 10% ICP accounts engaged — 2% new logos acquired — 90% dormant 90d — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-territory-whitespace-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.territory_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.territory_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_cov = 0, total_pen = 0, total_gro = 0, total_com = 0, total_opp = 0;

  for (const r of mockReps) {
    risk_counts[r.territory_risk]         = (risk_counts[r.territory_risk] || 0) + 1;
    pattern_counts[r.territory_pattern]   = (pattern_counts[r.territory_pattern] || 0) + 1;
    severity_counts[r.territory_severity] = (severity_counts[r.territory_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.territory_composite;
    total_cov  += r.coverage_score;
    total_pen  += r.penetration_score;
    total_gro  += r.growth_score;
    total_com  += r.competitive_score;
    total_opp  += r.estimated_whitespace_opportunity_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                        n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_territory_composite:                      Math.round((total_comp / n) * 10) / 10,
      territory_gap_count:                          mockReps.filter((r) => r.has_territory_gap).length,
      coaching_count:                               mockReps.filter((r) => r.requires_territory_coaching).length,
      avg_coverage_score:                           Math.round((total_cov / n) * 10) / 10,
      avg_penetration_score:                        Math.round((total_pen / n) * 10) / 10,
      avg_growth_score:                             Math.round((total_gro / n) * 10) / 10,
      avg_competitive_score:                        Math.round((total_com / n) * 10) / 10,
      total_estimated_whitespace_opportunity_usd:   Math.round(total_opp * 100) / 100,
    },
  });
}
