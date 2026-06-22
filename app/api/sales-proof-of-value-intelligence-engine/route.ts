import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-proof-of-value-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    value_risk: "low", value_pattern: "none",
    value_severity: "outcome_driven", recommended_action: "no_action",
    quantification_score: 0.0, executive_score: 0.0,
    proof_score: 0.0, outcome_score: 0.0,
    value_composite: 0.0,
    has_value_gap: false, requires_value_coaching: false,
    estimated_value_leak_usd: 0.0,
    value_signal: "Value selling strong — ROI quantification, executive engagement, and proof of value within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    value_risk: "low", value_pattern: "none",
    value_severity: "outcome_driven", recommended_action: "no_action",
    quantification_score: 4.0, executive_score: 3.0,
    proof_score: 5.0, outcome_score: 2.0,
    value_composite: 3.65,
    has_value_gap: false, requires_value_coaching: false,
    estimated_value_leak_usd: 0.0,
    value_signal: "Value selling strong — ROI quantification, executive engagement, and proof of value within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    value_risk: "moderate", value_pattern: "roi_avoidance",
    value_severity: "adequate", recommended_action: "value_selling_coaching",
    quantification_score: 22.0, executive_score: 18.0,
    proof_score: 20.0, outcome_score: 15.0,
    value_composite: 19.55,
    has_value_gap: false, requires_value_coaching: true,
    estimated_value_leak_usd: 84000.0,
    value_signal: "ROI avoidance — 38% ROI quantified before proposal — 55% feature demos without ROI — 12% deals lost on price — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    value_risk: "moderate", value_pattern: "champion_dependency",
    value_severity: "adequate", recommended_action: "value_selling_coaching",
    quantification_score: 20.0, executive_score: 25.0,
    proof_score: 18.0, outcome_score: 22.0,
    value_composite: 21.0,
    has_value_gap: false, requires_value_coaching: true,
    estimated_value_leak_usd: 156000.0,
    value_signal: "Champion dependency — 42% ROI quantified before proposal — 48% exec sponsor engaged — 22% deals lost on price — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    value_risk: "high", value_pattern: "executive_misalignment",
    value_severity: "feature_led", recommended_action: "executive_engagement_coaching",
    quantification_score: 38.0, executive_score: 50.0,
    proof_score: 35.0, outcome_score: 30.0,
    value_composite: 38.95,
    has_value_gap: false, requires_value_coaching: true,
    estimated_value_leak_usd: 540000.0,
    value_signal: "Executive misalignment — 28% ROI quantified before proposal — 22% exec sponsor engaged — 28% deals lost on price — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    value_risk: "high", value_pattern: "value_gap_at_close",
    value_severity: "feature_led", recommended_action: "business_case_coaching",
    quantification_score: 45.0, executive_score: 38.0,
    proof_score: 42.0, outcome_score: 48.0,
    value_composite: 43.05,
    has_value_gap: true, requires_value_coaching: true,
    estimated_value_leak_usd: 1260000.0,
    value_signal: "Value gap at close — 20% ROI quantified before proposal — 30% exec sponsor engaged — 35% deals lost on price — composite 43",
  },
  {
    rep_id: "rep_007", region: "APAC",
    value_risk: "critical", value_pattern: "feature_seller",
    value_severity: "value_blind", recommended_action: "value_selling_coaching",
    quantification_score: 72.0, executive_score: 68.0,
    proof_score: 65.0, outcome_score: 70.0,
    value_composite: 69.05,
    has_value_gap: true, requires_value_coaching: true,
    estimated_value_leak_usd: 2800000.0,
    value_signal: "Feature seller — 10% ROI quantified before proposal — 12% exec sponsor engaged — 48% deals lost on price — composite 69",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    value_risk: "critical", value_pattern: "roi_avoidance",
    value_severity: "value_blind", recommended_action: "roi_case_building_coaching",
    quantification_score: 100.0, executive_score: 100.0,
    proof_score: 100.0, outcome_score: 100.0,
    value_composite: 100.0,
    has_value_gap: true, requires_value_coaching: true,
    estimated_value_leak_usd: 5600000.0,
    value_signal: "ROI avoidance — 5% ROI quantified before proposal — 8% exec sponsor engaged — 55% deals lost on price — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-proof-of-value-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.value_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.value_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_qua = 0, total_exe = 0, total_pro = 0, total_out = 0, total_leak = 0;

  for (const r of mockReps) {
    risk_counts[r.value_risk]         = (risk_counts[r.value_risk] || 0) + 1;
    pattern_counts[r.value_pattern]   = (pattern_counts[r.value_pattern] || 0) + 1;
    severity_counts[r.value_severity] = (severity_counts[r.value_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.value_composite;
    total_qua  += r.quantification_score;
    total_exe  += r.executive_score;
    total_pro  += r.proof_score;
    total_out  += r.outcome_score;
    total_leak += r.estimated_value_leak_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                               n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_value_composite:                 Math.round((total_comp / n) * 10) / 10,
      value_gap_count:                     mockReps.filter((r) => r.has_value_gap).length,
      coaching_count:                      mockReps.filter((r) => r.requires_value_coaching).length,
      avg_quantification_score:            Math.round((total_qua / n) * 10) / 10,
      avg_executive_score:                 Math.round((total_exe / n) * 10) / 10,
      avg_proof_score:                     Math.round((total_pro / n) * 10) / 10,
      avg_outcome_score:                   Math.round((total_out / n) * 10) / 10,
      total_estimated_value_leak_usd:      Math.round(total_leak * 100) / 100,
    },
  }));
}
