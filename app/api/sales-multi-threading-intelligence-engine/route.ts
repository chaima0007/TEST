import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    multithread_risk: "low", multithread_pattern: "none",
    multithread_severity: "networked", recommended_action: "no_action",
    depth_score: 0.0, breadth_score: 0.0,
    executive_access_score: 0.0, risk_exposure_score: 0.0,
    multithread_composite: 0.0,
    has_multithread_gap: false, requires_multithread_coaching: false,
    estimated_deal_risk_usd: 0.0,
    multithread_signal: "Multi-threading strong — stakeholder depth, org breadth, and executive access within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    multithread_risk: "low", multithread_pattern: "none",
    multithread_severity: "networked", recommended_action: "no_action",
    depth_score: 4.0, breadth_score: 3.0,
    executive_access_score: 5.0, risk_exposure_score: 2.0,
    multithread_composite: 3.65,
    has_multithread_gap: false, requires_multithread_coaching: true,
    estimated_deal_risk_usd: 0.0,
    multithread_signal: "Multi-threading strong — stakeholder depth, org breadth, and executive access within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    multithread_risk: "moderate", multithread_pattern: "breadth_shallow",
    multithread_severity: "adequate", recommended_action: "stakeholder_mapping_coaching",
    depth_score: 20.0, breadth_score: 22.0,
    executive_access_score: 18.0, risk_exposure_score: 15.0,
    multithread_composite: 19.85,
    has_multithread_gap: false, requires_multithread_coaching: true,
    estimated_deal_risk_usd: 124000.0,
    multithread_signal: "Breadth shallow — 2.1 avg contacts/deal — 38% single-contact deals — 35% exec engaged — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    multithread_risk: "moderate", multithread_pattern: "executive_bypass",
    multithread_severity: "adequate", recommended_action: "stakeholder_mapping_coaching",
    depth_score: 18.0, breadth_score: 20.0,
    executive_access_score: 28.0, risk_exposure_score: 15.0,
    multithread_composite: 20.0,
    has_multithread_gap: false, requires_multithread_coaching: true,
    estimated_deal_risk_usd: 192000.0,
    multithread_signal: "Executive bypass — 2.0 avg contacts/deal — 35% single-contact deals — 18% exec engaged — composite 20",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    multithread_risk: "high", multithread_pattern: "org_chart_blind",
    multithread_severity: "shallow", recommended_action: "organization_navigation_coaching",
    depth_score: 40.0, breadth_score: 45.0,
    executive_access_score: 38.0, risk_exposure_score: 30.0,
    multithread_composite: 39.75,
    has_multithread_gap: true, requires_multithread_coaching: true,
    estimated_deal_risk_usd: 648000.0,
    multithread_signal: "Org chart blind — 1.6 avg contacts/deal — 55% single-contact deals — 22% exec engaged — composite 40",
  },
  {
    rep_id: "rep_006", region: "West",
    multithread_risk: "high", multithread_pattern: "champion_only_reliance",
    multithread_severity: "shallow", recommended_action: "champion_diversification_coaching",
    depth_score: 48.0, breadth_score: 42.0,
    executive_access_score: 50.0, risk_exposure_score: 40.0,
    multithread_composite: 45.7,
    has_multithread_gap: true, requires_multithread_coaching: true,
    estimated_deal_risk_usd: 1215000.0,
    multithread_signal: "Champion-only reliance — 1.4 avg contacts/deal — 62% single-contact deals — 15% exec engaged — composite 46",
  },
  {
    rep_id: "rep_007", region: "APAC",
    multithread_risk: "critical", multithread_pattern: "single_contact_dependency",
    multithread_severity: "isolated", recommended_action: "deal_at_risk_intervention",
    depth_score: 72.0, breadth_score: 68.0,
    executive_access_score: 65.0, risk_exposure_score: 72.0,
    multithread_composite: 69.55,
    has_multithread_gap: true, requires_multithread_coaching: true,
    estimated_deal_risk_usd: 2835000.0,
    multithread_signal: "Single contact dependency — 1.3 avg contacts/deal — 78% single-contact deals — 10% exec engaged — composite 70",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    multithread_risk: "critical", multithread_pattern: "single_contact_dependency",
    multithread_severity: "isolated", recommended_action: "deal_at_risk_intervention",
    depth_score: 100.0, breadth_score: 100.0,
    executive_access_score: 100.0, risk_exposure_score: 100.0,
    multithread_composite: 100.0,
    has_multithread_gap: true, requires_multithread_coaching: true,
    estimated_deal_risk_usd: 4500000.0,
    multithread_signal: "Single contact dependency — 1.2 avg contacts/deal — 85% single-contact deals — 10% exec engaged — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-multi-threading-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.multithread_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.multithread_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_d = 0, total_b = 0, total_e = 0, total_r = 0, total_risk_usd = 0;

  for (const rep of mockReps) {
    risk_counts[rep.multithread_risk]       = (risk_counts[rep.multithread_risk] || 0) + 1;
    pattern_counts[rep.multithread_pattern] = (pattern_counts[rep.multithread_pattern] || 0) + 1;
    severity_counts[rep.multithread_severity] = (severity_counts[rep.multithread_severity] || 0) + 1;
    action_counts[rep.recommended_action]   = (action_counts[rep.recommended_action] || 0) + 1;
    total_comp     += rep.multithread_composite;
    total_d        += rep.depth_score;
    total_b        += rep.breadth_score;
    total_e        += rep.executive_access_score;
    total_r        += rep.risk_exposure_score;
    total_risk_usd += rep.estimated_deal_risk_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                             n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_multithread_composite:         Math.round((total_comp / n) * 10) / 10,
      multithread_gap_count:             mockReps.filter((r) => r.has_multithread_gap).length,
      coaching_count:                    mockReps.filter((r) => r.requires_multithread_coaching).length,
      avg_depth_score:                   Math.round((total_d / n) * 10) / 10,
      avg_breadth_score:                 Math.round((total_b / n) * 10) / 10,
      avg_executive_access_score:        Math.round((total_e / n) * 10) / 10,
      avg_risk_exposure_score:           Math.round((total_r / n) * 10) / 10,
      total_estimated_deal_risk_usd:     Math.round(total_risk_usd * 100) / 100,
    },
  });
}
