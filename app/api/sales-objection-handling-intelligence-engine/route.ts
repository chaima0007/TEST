import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    obj_risk: "low", obj_pattern: "none",
    obj_severity: "expert", recommended_action: "no_action",
    resolution_effectiveness_score: 0.0, objection_intelligence_score: 0.0,
    resilience_score: 0.0, evidence_utilization_score: 0.0,
    obj_composite: 0.0,
    has_obj_gap: false, requires_obj_coaching: false,
    estimated_deal_loss_usd: 0.0,
    obj_signal: "Objection handling strong — resolution rate, reframe quality, and evidence use within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    obj_risk: "low", obj_pattern: "none",
    obj_severity: "expert", recommended_action: "no_action",
    resolution_effectiveness_score: 4.0, objection_intelligence_score: 3.0,
    resilience_score: 5.0, evidence_utilization_score: 2.0,
    obj_composite: 3.7,
    has_obj_gap: false, requires_obj_coaching: true,
    estimated_deal_loss_usd: 0.0,
    obj_signal: "Objection handling strong — resolution rate, reframe quality, and evidence use within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    obj_risk: "moderate", obj_pattern: "timing_deferrer",
    obj_severity: "competent", recommended_action: "reframe_coaching",
    resolution_effectiveness_score: 20.0, objection_intelligence_score: 22.0,
    resilience_score: 18.0, evidence_utilization_score: 14.0,
    obj_composite: 19.35,
    has_obj_gap: true, requires_obj_coaching: true,
    estimated_deal_loss_usd: 46000.0,
    obj_signal: "Timing deferrer — 58% objections resolved — 32% concede after price obj — 38% use evidence — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    obj_risk: "moderate", obj_pattern: "status_quo_deflector",
    obj_severity: "competent", recommended_action: "reframe_coaching",
    resolution_effectiveness_score: 22.0, objection_intelligence_score: 28.0,
    resilience_score: 18.0, evidence_utilization_score: 12.0,
    obj_composite: 21.1,
    has_obj_gap: true, requires_obj_coaching: true,
    estimated_deal_loss_usd: 72000.0,
    obj_signal: "Status quo deflector — 52% objections resolved — 28% concede after price obj — 35% use evidence — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    obj_risk: "high", obj_pattern: "authority_blocker",
    obj_severity: "developing", recommended_action: "multi_threading_coaching",
    resolution_effectiveness_score: 40.0, objection_intelligence_score: 38.0,
    resilience_score: 42.0, evidence_utilization_score: 35.0,
    obj_composite: 39.2,
    has_obj_gap: true, requires_obj_coaching: true,
    estimated_deal_loss_usd: 216000.0,
    obj_signal: "Authority blocker — 40% objections resolved — 45% concede after price obj — 22% use evidence — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    obj_risk: "high", obj_pattern: "feature_objector",
    obj_severity: "developing", recommended_action: "feature_gap_coaching",
    resolution_effectiveness_score: 48.0, objection_intelligence_score: 42.0,
    resilience_score: 40.0, evidence_utilization_score: 50.0,
    obj_composite: 44.7,
    has_obj_gap: true, requires_obj_coaching: true,
    estimated_deal_loss_usd: 432000.0,
    obj_signal: "Feature objector — 32% objections resolved — 48% concede after price obj — 18% use evidence — composite 45",
  },
  {
    rep_id: "rep_007", region: "APAC",
    obj_risk: "critical", obj_pattern: "price_caver",
    obj_severity: "struggling", recommended_action: "objection_handling_intervention",
    resolution_effectiveness_score: 72.0, objection_intelligence_score: 65.0,
    resilience_score: 68.0, evidence_utilization_score: 70.0,
    obj_composite: 69.2,
    has_obj_gap: true, requires_obj_coaching: true,
    estimated_deal_loss_usd: 1134000.0,
    obj_signal: "Price caver — 18% objections resolved — 68% concede after price obj — 8% use evidence — composite 69",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    obj_risk: "critical", obj_pattern: "price_caver",
    obj_severity: "struggling", recommended_action: "objection_handling_intervention",
    resolution_effectiveness_score: 100.0, objection_intelligence_score: 100.0,
    resilience_score: 100.0, evidence_utilization_score: 100.0,
    obj_composite: 100.0,
    has_obj_gap: true, requires_obj_coaching: true,
    estimated_deal_loss_usd: 3240000.0,
    obj_signal: "Price caver — 10% objections resolved — 82% concede after price obj — 5% use evidence — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-objection-handling-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.obj_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.obj_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, tre = 0, toi = 0, trs = 0, teu = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.obj_risk]             = (risk_counts[r.obj_risk] || 0) + 1;
    pattern_counts[r.obj_pattern]       = (pattern_counts[r.obj_pattern] || 0) + 1;
    severity_counts[r.obj_severity]     = (severity_counts[r.obj_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.obj_composite;
    tre        += r.resolution_effectiveness_score;
    toi        += r.objection_intelligence_score;
    trs        += r.resilience_score;
    teu        += r.evidence_utilization_score;
    total_loss += r.estimated_deal_loss_usd;
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
      avg_obj_composite:                      Math.round((total_comp / n) * 10) / 10,
      obj_gap_count:                          mockReps.filter((r) => r.has_obj_gap).length,
      coaching_count:                         mockReps.filter((r) => r.requires_obj_coaching).length,
      avg_resolution_effectiveness_score:     Math.round((tre / n) * 10) / 10,
      avg_objection_intelligence_score:       Math.round((toi / n) * 10) / 10,
      avg_resilience_score:                   Math.round((trs / n) * 10) / 10,
      avg_evidence_utilization_score:         Math.round((teu / n) * 10) / 10,
      total_estimated_deal_loss_usd:          Math.round(total_loss * 100) / 100,
    },
  });
}
