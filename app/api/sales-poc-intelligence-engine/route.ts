import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-poc-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    poc_risk: "low", poc_pattern: "none",
    poc_severity: "structured", recommended_action: "no_action",
    poc_structure_score: 0.0, poc_execution_score: 0.0,
    poc_stakeholder_score: 0.0, poc_conversion_score: 0.0,
    poc_composite: 0.0,
    has_poc_gap: false, requires_poc_coaching: false,
    estimated_pipeline_loss_usd: 0.0,
    poc_signal: "POC execution healthy — structure, conversion, and champion engagement within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    poc_risk: "low", poc_pattern: "none",
    poc_severity: "structured", recommended_action: "no_action",
    poc_structure_score: 4.0, poc_execution_score: 3.0,
    poc_stakeholder_score: 5.0, poc_conversion_score: 2.0,
    poc_composite: 3.65,
    has_poc_gap: false, requires_poc_coaching: false,
    estimated_pipeline_loss_usd: 0.0,
    poc_signal: "POC execution healthy — structure, conversion, and champion engagement within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    poc_risk: "moderate", poc_pattern: "success_criteria_gap",
    poc_severity: "developing", recommended_action: "success_criteria_alignment",
    poc_structure_score: 22.0, poc_execution_score: 14.0,
    poc_stakeholder_score: 20.0, poc_conversion_score: 10.0,
    poc_composite: 17.65,
    has_poc_gap: false, requires_poc_coaching: false,
    estimated_pipeline_loss_usd: 7200.0,
    poc_signal: "Success criteria gap — 55% POC-to-close — 20% stalled POCs — 28 avg POC days — composite 18",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    poc_risk: "moderate", poc_pattern: "no_champion_during_poc",
    poc_severity: "developing", recommended_action: "success_criteria_alignment",
    poc_structure_score: 18.0, poc_execution_score: 20.0,
    poc_stakeholder_score: 35.0, poc_conversion_score: 15.0,
    poc_composite: 22.5,
    has_poc_gap: false, requires_poc_coaching: true,
    estimated_pipeline_loss_usd: 18000.0,
    poc_signal: "No champion during poc — 48% POC-to-close — 22% stalled POCs — 35 avg POC days — composite 23",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    poc_risk: "high", poc_pattern: "poc_stall",
    poc_severity: "uncontrolled", recommended_action: "poc_structure_coaching",
    poc_structure_score: 35.0, poc_execution_score: 55.0,
    poc_stakeholder_score: 30.0, poc_conversion_score: 25.0,
    poc_composite: 38.5,
    has_poc_gap: true, requires_poc_coaching: true,
    estimated_pipeline_loss_usd: 54000.0,
    poc_signal: "Poc stall — 38% POC-to-close — 45% stalled POCs — 52 avg POC days — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    poc_risk: "high", poc_pattern: "scope_creep",
    poc_severity: "uncontrolled", recommended_action: "scope_control_training",
    poc_structure_score: 40.0, poc_execution_score: 58.0,
    poc_stakeholder_score: 35.0, poc_conversion_score: 30.0,
    poc_composite: 42.25,
    has_poc_gap: true, requires_poc_coaching: true,
    estimated_pipeline_loss_usd: 81000.0,
    poc_signal: "Scope creep — 32% POC-to-close — 52% stalled POCs — 60 avg POC days — composite 42",
  },
  {
    rep_id: "rep_007", region: "APAC",
    poc_risk: "critical", poc_pattern: "technical_validation_failure",
    poc_severity: "failing", recommended_action: "technical_escalation_support",
    poc_structure_score: 62.0, poc_execution_score: 70.0,
    poc_stakeholder_score: 65.0, poc_conversion_score: 78.0,
    poc_composite: 68.0,
    has_poc_gap: true, requires_poc_coaching: true,
    estimated_pipeline_loss_usd: 162000.0,
    poc_signal: "Technical validation failure — 22% POC-to-close — 62% stalled POCs — 72 avg POC days — composite 68",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    poc_risk: "critical", poc_pattern: "poc_stall",
    poc_severity: "failing", recommended_action: "poc_structure_coaching",
    poc_structure_score: 100.0, poc_execution_score: 100.0,
    poc_stakeholder_score: 100.0, poc_conversion_score: 100.0,
    poc_composite: 100.0,
    has_poc_gap: true, requires_poc_coaching: true,
    estimated_pipeline_loss_usd: 300000.0,
    poc_signal: "Poc stall — 10% POC-to-close — 80% stalled POCs — 90 avg POC days — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-poc-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.poc_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.poc_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_str = 0, total_exc = 0, total_stk = 0, total_cvt = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.poc_risk]          = (risk_counts[r.poc_risk] || 0) + 1;
    pattern_counts[r.poc_pattern]    = (pattern_counts[r.poc_pattern] || 0) + 1;
    severity_counts[r.poc_severity]  = (severity_counts[r.poc_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.poc_composite;
    total_str  += r.poc_structure_score;
    total_exc  += r.poc_execution_score;
    total_stk  += r.poc_stakeholder_score;
    total_cvt  += r.poc_conversion_score;
    total_loss += r.estimated_pipeline_loss_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_poc_composite:                    Math.round((total_comp / n) * 10) / 10,
      poc_gap_count:                        mockReps.filter((r) => r.has_poc_gap).length,
      coaching_count:                       mockReps.filter((r) => r.requires_poc_coaching).length,
      avg_poc_structure_score:              Math.round((total_str / n) * 10) / 10,
      avg_poc_execution_score:              Math.round((total_exc / n) * 10) / 10,
      avg_poc_stakeholder_score:            Math.round((total_stk / n) * 10) / 10,
      avg_poc_conversion_score:             Math.round((total_cvt / n) * 10) / 10,
      total_estimated_pipeline_loss_usd:    Math.round(total_loss * 100) / 100,
    },
  }));
}
