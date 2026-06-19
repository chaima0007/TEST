import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    conversation_risk: "low", conversation_pattern: "none",
    conversation_severity: "sharp", recommended_action: "no_action",
    engagement_quality_score: 0.0, discovery_depth_score: 0.0,
    objection_handling_score: 0.0, next_step_discipline_score: 0.0,
    conversation_composite: 0.0,
    has_conversation_gap: false, requires_call_coaching: false,
    estimated_revenue_impact_usd: 0.0,
    conversation_signal: "Conversation quality healthy — discovery, objection handling, and next steps within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    conversation_risk: "low", conversation_pattern: "none",
    conversation_severity: "sharp", recommended_action: "no_action",
    engagement_quality_score: 4.0, discovery_depth_score: 3.0,
    objection_handling_score: 5.0, next_step_discipline_score: 2.0,
    conversation_composite: 3.65,
    has_conversation_gap: false, requires_call_coaching: false,
    estimated_revenue_impact_usd: 0.0,
    conversation_signal: "Conversation quality healthy — discovery, objection handling, and next steps within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    conversation_risk: "moderate", conversation_pattern: "low_engagement_calls",
    conversation_severity: "developing", recommended_action: "call_coaching_session",
    engagement_quality_score: 20.0, discovery_depth_score: 18.0,
    objection_handling_score: 15.0, next_step_discipline_score: 20.0,
    conversation_composite: 18.55,
    has_conversation_gap: false, requires_call_coaching: false,
    estimated_revenue_impact_usd: 11400.0,
    conversation_signal: "Low engagement calls — 1.6x talk/listen ratio — 65% calls with next step — 38% pain identified — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    conversation_risk: "moderate", conversation_pattern: "shallow_discovery",
    conversation_severity: "developing", recommended_action: "call_coaching_session",
    engagement_quality_score: 18.0, discovery_depth_score: 32.0,
    objection_handling_score: 20.0, next_step_discipline_score: 16.0,
    conversation_composite: 22.1,
    has_conversation_gap: false, requires_call_coaching: true,
    estimated_revenue_impact_usd: 19500.0,
    conversation_signal: "Shallow discovery — 1.7x talk/listen ratio — 62% calls with next step — 28% pain identified — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    conversation_risk: "high", conversation_pattern: "no_next_step_discipline",
    conversation_severity: "weak", recommended_action: "next_step_discipline_review",
    engagement_quality_score: 32.0, discovery_depth_score: 30.0,
    objection_handling_score: 35.0, next_step_discipline_score: 48.0,
    conversation_composite: 35.2,
    has_conversation_gap: true, requires_call_coaching: true,
    estimated_revenue_impact_usd: 58500.0,
    conversation_signal: "No next step discipline — 1.9x talk/listen ratio — 45% calls with next step — 32% pain identified — composite 35",
  },
  {
    rep_id: "rep_006", region: "West",
    conversation_risk: "high", conversation_pattern: "poor_objection_handling",
    conversation_severity: "weak", recommended_action: "call_coaching_session",
    engagement_quality_score: 40.0, discovery_depth_score: 35.0,
    objection_handling_score: 52.0, next_step_discipline_score: 30.0,
    conversation_composite: 40.05,
    has_conversation_gap: true, requires_call_coaching: true,
    estimated_revenue_impact_usd: 91800.0,
    conversation_signal: "Poor objection handling — 2.1x talk/listen ratio — 48% calls with next step — 28% pain identified — composite 40",
  },
  {
    rep_id: "rep_007", region: "APAC",
    conversation_risk: "critical", conversation_pattern: "monologue_tendency",
    conversation_severity: "failing", recommended_action: "call_recording_audit",
    engagement_quality_score: 72.0, discovery_depth_score: 65.0,
    objection_handling_score: 58.0, next_step_discipline_score: 55.0,
    conversation_composite: 64.45,
    has_conversation_gap: true, requires_call_coaching: true,
    estimated_revenue_impact_usd: 146700.0,
    conversation_signal: "Monologue tendency — 2.6x talk/listen ratio — 38% calls with next step — 25% pain identified — composite 64",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    conversation_risk: "critical", conversation_pattern: "monologue_tendency",
    conversation_severity: "failing", recommended_action: "objection_handling_workshop",
    engagement_quality_score: 85.0, discovery_depth_score: 80.0,
    objection_handling_score: 78.0, next_step_discipline_score: 72.0,
    conversation_composite: 80.05,
    has_conversation_gap: true, requires_call_coaching: true,
    estimated_revenue_impact_usd: 175959.0,
    conversation_signal: "Monologue tendency — 2.8x talk/listen ratio — 35% calls with next step — 22% pain identified — composite 88",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-conversation-quality-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.conversation_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.conversation_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_eng = 0, total_disc = 0, total_obj = 0, total_nxt = 0, total_impact = 0;

  for (const r of mockReps) {
    risk_counts[r.conversation_risk]       = (risk_counts[r.conversation_risk] || 0) + 1;
    pattern_counts[r.conversation_pattern] = (pattern_counts[r.conversation_pattern] || 0) + 1;
    severity_counts[r.conversation_severity] = (severity_counts[r.conversation_severity] || 0) + 1;
    action_counts[r.recommended_action]    = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.conversation_composite;
    total_eng    += r.engagement_quality_score;
    total_disc   += r.discovery_depth_score;
    total_obj    += r.objection_handling_score;
    total_nxt    += r.next_step_discipline_score;
    total_impact += r.estimated_revenue_impact_usd;
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
      avg_conversation_composite:               Math.round((total_comp / n) * 10) / 10,
      conversation_gap_count:                   mockReps.filter((r) => r.has_conversation_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_call_coaching).length,
      avg_engagement_quality_score:             Math.round((total_eng / n) * 10) / 10,
      avg_discovery_depth_score:                Math.round((total_disc / n) * 10) / 10,
      avg_objection_handling_score:             Math.round((total_obj / n) * 10) / 10,
      avg_next_step_discipline_score:           Math.round((total_nxt / n) * 10) / 10,
      total_estimated_revenue_impact_usd:       Math.round(total_impact * 100) / 100,
    },
  });
}
