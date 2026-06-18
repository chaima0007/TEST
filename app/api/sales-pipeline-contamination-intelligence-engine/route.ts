import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "REP-001", region: "West",
    contam_risk: "low", contam_pattern: "none",
    contam_severity: "clean", recommended_action: "no_action",
    zombie_score: 4.0, qualification_score: 5.0,
    accuracy_score: 5.0, hygiene_score: 4.0,
    contam_composite: 4.55,
    has_contam_gap: false, requires_contam_intervention: false,
    estimated_phantom_pipeline_usd: 0.0,
    contam_signal: "Pipeline contamination low — deal quality, qualification, forecast accuracy, and hygiene within benchmarks",
  },
  {
    rep_id: "REP-002", region: "East",
    contam_risk: "low", contam_pattern: "none",
    contam_severity: "clean", recommended_action: "no_action",
    zombie_score: 8.0, qualification_score: 7.0,
    accuracy_score: 6.0, hygiene_score: 8.0,
    contam_composite: 7.3,
    has_contam_gap: false, requires_contam_intervention: false,
    estimated_phantom_pipeline_usd: 12000.0,
    contam_signal: "Pipeline contamination low — deal quality, qualification, forecast accuracy, and hygiene within benchmarks",
  },
  {
    rep_id: "REP-003", region: "Central",
    contam_risk: "moderate", contam_pattern: "none",
    contam_severity: "adequate", recommended_action: "pipeline_scrub",
    zombie_score: 22.0, qualification_score: 18.0,
    accuracy_score: 20.0, hygiene_score: 16.0,
    contam_composite: 19.7,
    has_contam_gap: false, requires_contam_intervention: true,
    estimated_phantom_pipeline_usd: 35000.0,
    contam_signal: "None — 10% zombie deals — 15% close date pushed 3+ times — 12% unqualified — composite 20",
  },
  {
    rep_id: "REP-004", region: "Northeast",
    contam_risk: "moderate", contam_pattern: "dark_pipeline",
    contam_severity: "adequate", recommended_action: "pipeline_scrub",
    zombie_score: 28.0, qualification_score: 22.0,
    accuracy_score: 18.0, hygiene_score: 28.0,
    contam_composite: 23.8,
    has_contam_gap: false, requires_contam_intervention: true,
    estimated_phantom_pipeline_usd: 60000.0,
    contam_signal: "Dark pipeline — 15% zombie deals — 20% close date pushed 3+ times — 18% unqualified — composite 24",
  },
  {
    rep_id: "REP-005", region: "Southeast",
    contam_risk: "high", contam_pattern: "unqualified_bloat",
    contam_severity: "contaminated", recommended_action: "qualification_coaching",
    zombie_score: 35.0, qualification_score: 48.0,
    accuracy_score: 32.0, hygiene_score: 38.0,
    contam_composite: 38.35,
    has_contam_gap: true, requires_contam_intervention: true,
    estimated_phantom_pipeline_usd: 110000.0,
    contam_signal: "Unqualified bloat — 22% zombie deals — 30% close date pushed 3+ times — 38% unqualified — composite 38",
  },
  {
    rep_id: "REP-006", region: "West",
    contam_risk: "high", contam_pattern: "stage_freezer",
    contam_severity: "contaminated", recommended_action: "deal_inspection",
    zombie_score: 45.0, qualification_score: 38.0,
    accuracy_score: 42.0, hygiene_score: 35.0,
    contam_composite: 41.05,
    has_contam_gap: true, requires_contam_intervention: true,
    estimated_phantom_pipeline_usd: 185000.0,
    contam_signal: "Stage freezer — 28% zombie deals — 38% close date pushed 3+ times — 30% unqualified — composite 41",
  },
  {
    rep_id: "REP-007", region: "APAC",
    contam_risk: "critical", contam_pattern: "zombie_accumulator",
    contam_severity: "toxic", recommended_action: "executive_pipeline_reset",
    zombie_score: 70.0, qualification_score: 58.0,
    accuracy_score: 62.0, hygiene_score: 55.0,
    contam_composite: 63.25,
    has_contam_gap: true, requires_contam_intervention: true,
    estimated_phantom_pipeline_usd: 420000.0,
    contam_signal: "Zombie accumulator — 50% zombie deals — 55% close date pushed 3+ times — 50% unqualified — composite 63",
  },
  {
    rep_id: "REP-008", region: "EMEA",
    contam_risk: "critical", contam_pattern: "forecast_padder",
    contam_severity: "toxic", recommended_action: "executive_pipeline_reset",
    zombie_score: 80.0, qualification_score: 72.0,
    accuracy_score: 78.0, hygiene_score: 68.0,
    contam_composite: 75.5,
    has_contam_gap: true, requires_contam_intervention: true,
    estimated_phantom_pipeline_usd: 700000.0,
    contam_signal: "Forecast padder — 60% zombie deals — 65% close date pushed 3+ times — 60% unqualified — composite 76",
  },
];

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/api/sales-pipeline-contamination-intelligence-engine`, { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_z = 0, total_q = 0, total_a = 0, total_h = 0, total_pp = 0;

  for (const r of mockReps) {
    risk_counts[r.contam_risk]       = (risk_counts[r.contam_risk] || 0) + 1;
    pattern_counts[r.contam_pattern] = (pattern_counts[r.contam_pattern] || 0) + 1;
    severity_counts[r.contam_severity] = (severity_counts[r.contam_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.contam_composite;
    total_z    += r.zombie_score;
    total_q    += r.qualification_score;
    total_a    += r.accuracy_score;
    total_h    += r.hygiene_score;
    total_pp   += r.estimated_phantom_pipeline_usd;
  }

  const n = mockReps.length;
  return NextResponse.json({
    reps: mockReps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_contam_composite:                     Math.round((total_comp / n) * 10) / 10,
      contam_gap_count:                         mockReps.filter((r) => r.has_contam_gap).length,
      intervention_count:                       mockReps.filter((r) => r.requires_contam_intervention).length,
      avg_zombie_score:                         Math.round((total_z / n) * 10) / 10,
      avg_qualification_score:                  Math.round((total_q / n) * 10) / 10,
      avg_accuracy_score:                       Math.round((total_a / n) * 10) / 10,
      avg_hygiene_score:                        Math.round((total_h / n) * 10) / 10,
      total_estimated_phantom_pipeline_usd:     Math.round(total_pp * 100) / 100,
    },
  });
}
