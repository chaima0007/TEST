import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    champion_risk: "low", champion_pattern: "none",
    champion_severity: "anchored", recommended_action: "no_action",
    engagement_score: 0.0, threading_score: 0.0,
    detection_score: 0.0, coaching_score: 0.0,
    champion_composite: 0.0,
    has_champion_gap: false, requires_champion_coaching: false,
    estimated_deal_exposure_usd: 0.0,
    champion_signal: "Champion stability healthy — engagement, multithreading, and detection response within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    champion_risk: "low", champion_pattern: "none",
    champion_severity: "anchored", recommended_action: "no_action",
    engagement_score: 3.0, threading_score: 4.0,
    detection_score: 2.0, coaching_score: 5.0,
    champion_composite: 3.35,
    has_champion_gap: false, requires_champion_coaching: false,
    estimated_deal_exposure_usd: 0.0,
    champion_signal: "Champion stability healthy — engagement, multithreading, and detection response within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    champion_risk: "moderate", champion_pattern: "champion_role_change_blindspot",
    champion_severity: "developing", recommended_action: "multithreading_coaching",
    engagement_score: 18.0, threading_score: 22.0,
    detection_score: 25.0, coaching_score: 15.0,
    champion_composite: 20.45,
    has_champion_gap: false, requires_champion_coaching: true,
    estimated_deal_exposure_usd: 24000.0,
    champion_signal: "Champion role change blindspot — 12% champions gone dark — 35% single-thread deals — 10 days to detect change — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    champion_risk: "moderate", champion_pattern: "champion_ghosting",
    champion_severity: "developing", recommended_action: "multithreading_coaching",
    engagement_score: 25.0, threading_score: 20.0,
    detection_score: 22.0, coaching_score: 18.0,
    champion_composite: 22.05,
    has_champion_gap: false, requires_champion_coaching: true,
    estimated_deal_exposure_usd: 54000.0,
    champion_signal: "Champion ghosting — 18% champions gone dark — 42% single-thread deals — 8 days to detect change — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    champion_risk: "high", champion_pattern: "single_thread_fragility",
    champion_severity: "fragile", recommended_action: "multithreading_coaching",
    engagement_score: 35.0, threading_score: 48.0,
    detection_score: 30.0, coaching_score: 32.0,
    champion_composite: 37.55,
    has_champion_gap: true, requires_champion_coaching: true,
    estimated_deal_exposure_usd: 162000.0,
    champion_signal: "Single thread fragility — 28% champions gone dark — 68% single-thread deals — 12 days to detect change — composite 38",
  },
  {
    rep_id: "rep_006", region: "West",
    champion_risk: "high", champion_pattern: "internal_champion_conflict",
    champion_severity: "fragile", recommended_action: "executive_sponsor_alignment",
    engagement_score: 40.0, threading_score: 42.0,
    detection_score: 38.0, coaching_score: 45.0,
    champion_composite: 41.05,
    has_champion_gap: true, requires_champion_coaching: true,
    estimated_deal_exposure_usd: 290000.0,
    champion_signal: "Internal champion conflict — 35% champions gone dark — 72% single-thread deals — 14 days to detect change — composite 41",
  },
  {
    rep_id: "rep_007", region: "APAC",
    champion_risk: "critical", champion_pattern: "false_champion_reliance",
    champion_severity: "exposed", recommended_action: "champion_validation_coaching",
    engagement_score: 65.0, threading_score: 70.0,
    detection_score: 62.0, coaching_score: 75.0,
    champion_composite: 67.55,
    has_champion_gap: true, requires_champion_coaching: true,
    estimated_deal_exposure_usd: 680000.0,
    champion_signal: "False champion reliance — 45% champions gone dark — 85% single-thread deals — 18 days to detect change — composite 68",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    champion_risk: "critical", champion_pattern: "false_champion_reliance",
    champion_severity: "exposed", recommended_action: "champion_validation_coaching",
    engagement_score: 100.0, threading_score: 100.0,
    detection_score: 100.0, coaching_score: 100.0,
    champion_composite: 100.0,
    has_champion_gap: true, requires_champion_coaching: true,
    estimated_deal_exposure_usd: 1650000.0,
    champion_signal: "False champion reliance — 55% champions gone dark — 85% single-thread deals — 21 days to detect change — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-champion-stability-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.champion_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.champion_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_eng = 0, total_thr = 0, total_det = 0, total_coa = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.champion_risk]       = (risk_counts[r.champion_risk] || 0) + 1;
    pattern_counts[r.champion_pattern] = (pattern_counts[r.champion_pattern] || 0) + 1;
    severity_counts[r.champion_severity] = (severity_counts[r.champion_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.champion_composite;
    total_eng  += r.engagement_score;
    total_thr  += r.threading_score;
    total_det  += r.detection_score;
    total_coa  += r.coaching_score;
    total_loss += r.estimated_deal_exposure_usd;
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
      avg_champion_composite:                 Math.round((total_comp / n) * 10) / 10,
      champion_gap_count:                     mockReps.filter((r) => r.has_champion_gap).length,
      coaching_count:                         mockReps.filter((r) => r.requires_champion_coaching).length,
      avg_engagement_score:                   Math.round((total_eng / n) * 10) / 10,
      avg_threading_score:                    Math.round((total_thr / n) * 10) / 10,
      avg_detection_score:                    Math.round((total_det / n) * 10) / 10,
      avg_coaching_score:                     Math.round((total_coa / n) * 10) / 10,
      total_estimated_deal_exposure_usd:      Math.round(total_loss * 100) / 100,
    },
  });
}
