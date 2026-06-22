import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-objection-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    objection_risk: "low", objection_pattern: "none",
    objection_severity: "confident", recommended_action: "no_action",
    objection_resolution_score: 0.0, objection_preparation_score: 0.0,
    objection_response_score: 0.0, competitive_handling_score: 0.0,
    objection_composite: 0.0,
    has_objection_gap: false, requires_objection_coaching: false,
    estimated_deal_loss_usd: 0.0,
    objection_signal: "Objection handling healthy — resolution rate, preparation, and competitive handling within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    objection_risk: "low", objection_pattern: "none",
    objection_severity: "confident", recommended_action: "no_action",
    objection_resolution_score: 3.0, objection_preparation_score: 4.0,
    objection_response_score: 2.0, competitive_handling_score: 5.0,
    objection_composite: 3.45,
    has_objection_gap: false, requires_objection_coaching: false,
    estimated_deal_loss_usd: 0.0,
    objection_signal: "Objection handling healthy — resolution rate, preparation, and competitive handling within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    objection_risk: "moderate", objection_pattern: "late_stage_objection_surprise",
    objection_severity: "developing", recommended_action: "objection_handling_workshop",
    objection_resolution_score: 22.0, objection_preparation_score: 18.0,
    objection_response_score: 28.0, competitive_handling_score: 12.0,
    objection_composite: 21.3,
    has_objection_gap: false, requires_objection_coaching: false,
    estimated_deal_loss_usd: 18000.0,
    objection_signal: "Late stage objection surprise — 62% objections resolved — 20% competitive losses — 6 avg days to resolve — composite 21",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    objection_risk: "moderate", objection_pattern: "trust_objection_gap",
    objection_severity: "developing", recommended_action: "objection_handling_workshop",
    objection_resolution_score: 18.0, objection_preparation_score: 32.0,
    objection_response_score: 20.0, competitive_handling_score: 22.0,
    objection_composite: 23.1,
    has_objection_gap: false, requires_objection_coaching: true,
    estimated_deal_loss_usd: 32000.0,
    objection_signal: "Trust objection gap — 55% objections resolved — 28% competitive losses — 8 avg days to resolve — composite 23",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    objection_risk: "high", objection_pattern: "price_objection_paralysis",
    objection_severity: "reactive", recommended_action: "price_reframing_training",
    objection_resolution_score: 40.0, objection_preparation_score: 35.0,
    objection_response_score: 30.0, competitive_handling_score: 45.0,
    objection_composite: 37.5,
    has_objection_gap: false, requires_objection_coaching: true,
    estimated_deal_loss_usd: 90000.0,
    objection_signal: "Price objection paralysis — 42% objections resolved — 42% competitive losses — 11 avg days to resolve — composite 38",
  },
  {
    rep_id: "rep_006", region: "West",
    objection_risk: "high", objection_pattern: "technical_objection_avoidance",
    objection_severity: "reactive", recommended_action: "technical_proof_support",
    objection_resolution_score: 52.0, objection_preparation_score: 38.0,
    objection_response_score: 35.0, competitive_handling_score: 40.0,
    objection_composite: 43.25,
    has_objection_gap: true, requires_objection_coaching: true,
    estimated_deal_loss_usd: 144000.0,
    objection_signal: "Technical objection avoidance — 35% objections resolved — 48% competitive losses — 14 avg days to resolve — composite 43",
  },
  {
    rep_id: "rep_007", region: "APAC",
    objection_risk: "critical", objection_pattern: "competition_capitulation_under_objection",
    objection_severity: "paralyzed", recommended_action: "competitive_intelligence_training",
    objection_resolution_score: 65.0, objection_preparation_score: 70.0,
    objection_response_score: 60.0, competitive_handling_score: 78.0,
    objection_composite: 67.2,
    has_objection_gap: true, requires_objection_coaching: true,
    estimated_deal_loss_usd: 288000.0,
    objection_signal: "Competition capitulation under objection — 22% objections resolved — 65% competitive losses — 18 avg days to resolve — composite 67",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    objection_risk: "critical", objection_pattern: "price_objection_paralysis",
    objection_severity: "paralyzed", recommended_action: "objection_handling_workshop",
    objection_resolution_score: 100.0, objection_preparation_score: 100.0,
    objection_response_score: 100.0, competitive_handling_score: 100.0,
    objection_composite: 100.0,
    has_objection_gap: true, requires_objection_coaching: true,
    estimated_deal_loss_usd: 2500000.0,
    objection_signal: "Price objection paralysis — 10% objections resolved — 80% competitive losses — 21 avg days to resolve — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-objection-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.objection_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.objection_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_res = 0, total_pre = 0, total_rsp = 0, total_cmp = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.objection_risk]       = (risk_counts[r.objection_risk] || 0) + 1;
    pattern_counts[r.objection_pattern] = (pattern_counts[r.objection_pattern] || 0) + 1;
    severity_counts[r.objection_severity] = (severity_counts[r.objection_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.objection_composite;
    total_res  += r.objection_resolution_score;
    total_pre  += r.objection_preparation_score;
    total_rsp  += r.objection_response_score;
    total_cmp  += r.competitive_handling_score;
    total_loss += r.estimated_deal_loss_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_objection_composite:                  Math.round((total_comp / n) * 10) / 10,
      objection_gap_count:                      mockReps.filter((r) => r.has_objection_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_objection_coaching).length,
      avg_objection_resolution_score:           Math.round((total_res / n) * 10) / 10,
      avg_objection_preparation_score:          Math.round((total_pre / n) * 10) / 10,
      avg_objection_response_score:             Math.round((total_rsp / n) * 10) / 10,
      avg_competitive_handling_score:           Math.round((total_cmp / n) * 10) / 10,
      total_estimated_deal_loss_usd:            Math.round(total_loss * 100) / 100,
    },
  }));
}
