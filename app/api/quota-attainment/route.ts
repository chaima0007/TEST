import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "r_001", rep_name: "Alice Martin", manager_id: "m_001",
    attainment_likelihood: "likely", attainment_risk: "medium",
    performance_trend: "slowing", attainment_action: "accelerate",
    attainment_pct: 80.0, projected_attainment: 92.9,
    gap_to_quota: 180000, coverage_ratio: 1.02,
    confidence_score: 57.5, momentum_score: 62.0, pace_score: 55.0,
    is_at_risk: false, needs_coaching: false,
    closed_won_ytd: 720000, quota_ytd: 900000,
  },
  {
    rep_id: "r_002", rep_name: "Bruno Costa", manager_id: "m_001",
    attainment_likelihood: "very_likely", attainment_risk: "low",
    performance_trend: "accelerating", attainment_action: "maintain",
    attainment_pct: 95.0, projected_attainment: 108.0,
    gap_to_quota: 0, coverage_ratio: 1.45,
    confidence_score: 82.0, momentum_score: 78.0, pace_score: 72.0,
    is_at_risk: false, needs_coaching: false,
    closed_won_ytd: 855000, quota_ytd: 900000,
  },
  {
    rep_id: "r_003", rep_name: "Carla Diaz", manager_id: "m_002",
    attainment_likelihood: "possible", attainment_risk: "high",
    performance_trend: "declining", attainment_action: "coaching_required",
    attainment_pct: 55.0, projected_attainment: 68.0,
    gap_to_quota: 360000, coverage_ratio: 0.72,
    confidence_score: 38.5, momentum_score: 32.0, pace_score: 28.0,
    is_at_risk: true, needs_coaching: true,
    closed_won_ytd: 440000, quota_ytd: 800000,
  },
  {
    rep_id: "r_004", rep_name: "David Lee", manager_id: "m_002",
    attainment_likelihood: "unlikely", attainment_risk: "critical",
    performance_trend: "declining", attainment_action: "urgent_review",
    attainment_pct: 38.0, projected_attainment: 42.0,
    gap_to_quota: 496000, coverage_ratio: 0.48,
    confidence_score: 22.0, momentum_score: 18.0, pace_score: 15.0,
    is_at_risk: true, needs_coaching: true,
    closed_won_ytd: 304000, quota_ytd: 800000,
  },
  {
    rep_id: "r_005", rep_name: "Elena Rossi", manager_id: "m_001",
    attainment_likelihood: "likely", attainment_risk: "medium",
    performance_trend: "on_track", attainment_action: "maintain",
    attainment_pct: 72.0, projected_attainment: 88.0,
    gap_to_quota: 210000, coverage_ratio: 0.96,
    confidence_score: 62.0, momentum_score: 55.0, pace_score: 48.0,
    is_at_risk: false, needs_coaching: false,
    closed_won_ytd: 540000, quota_ytd: 750000,
  },
  {
    rep_id: "r_006", rep_name: "Felix Müller", manager_id: "m_003",
    attainment_likelihood: "very_likely", attainment_risk: "low",
    performance_trend: "accelerating", attainment_action: "maintain",
    attainment_pct: 102.0, projected_attainment: 118.0,
    gap_to_quota: 0, coverage_ratio: 1.62,
    confidence_score: 88.0, momentum_score: 85.0, pace_score: 80.0,
    is_at_risk: false, needs_coaching: false,
    closed_won_ytd: 918000, quota_ytd: 900000,
  },
  {
    rep_id: "r_007", rep_name: "Grace Tanaka", manager_id: "m_003",
    attainment_likelihood: "possible", attainment_risk: "high",
    performance_trend: "slowing", attainment_action: "pipeline_build",
    attainment_pct: 48.0, projected_attainment: 62.0,
    gap_to_quota: 390000, coverage_ratio: 0.65,
    confidence_score: 34.0, momentum_score: 28.0, pace_score: 22.0,
    is_at_risk: true, needs_coaching: true,
    closed_won_ytd: 360000, quota_ytd: 750000,
  },
  {
    rep_id: "r_008", rep_name: "Hassan Ali", manager_id: "m_002",
    attainment_likelihood: "likely", attainment_risk: "medium",
    performance_trend: "on_track", attainment_action: "accelerate",
    attainment_pct: 68.0, projected_attainment: 84.0,
    gap_to_quota: 256000, coverage_ratio: 0.92,
    confidence_score: 58.0, momentum_score: 62.0, pace_score: 52.0,
    is_at_risk: false, needs_coaching: false,
    closed_won_ytd: 544000, quota_ytd: 800000,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const likelihood = searchParams.get("likelihood");
  const risk       = searchParams.get("risk");
  const manager    = searchParams.get("manager");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/quota-attainment`);
      if (likelihood) url.searchParams.set("likelihood", likelihood);
      if (risk)       url.searchParams.set("risk", risk);
      if (manager)    url.searchParams.set("manager", manager);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (likelihood) reps = reps.filter((r) => r.attainment_likelihood === likelihood);
  if (risk)       reps = reps.filter((r) => r.attainment_risk === risk);
  if (manager)    reps = reps.filter((r) => r.manager_id === manager);

  const likelihood_counts: Record<string, number> = {};
  const risk_counts:        Record<string, number> = {};
  const trend_counts:       Record<string, number> = {};
  const action_counts:      Record<string, number> = {};
  let total_attainment = 0, total_projected = 0,
      total_confidence = 0, total_momentum = 0;

  for (const r of mockReps) {
    likelihood_counts[r.attainment_likelihood] = (likelihood_counts[r.attainment_likelihood] || 0) + 1;
    risk_counts[r.attainment_risk]             = (risk_counts[r.attainment_risk] || 0) + 1;
    trend_counts[r.performance_trend]          = (trend_counts[r.performance_trend] || 0) + 1;
    action_counts[r.attainment_action]         = (action_counts[r.attainment_action] || 0) + 1;
    total_attainment  += r.attainment_pct;
    total_projected   += r.projected_attainment;
    total_confidence  += r.confidence_score;
    total_momentum    += r.momentum_score;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                    n,
      likelihood_counts,
      risk_counts,
      trend_counts,
      action_counts,
      avg_attainment_pct:       Math.round((total_attainment / n) * 10) / 10,
      avg_projected_attainment: Math.round((total_projected / n) * 10) / 10,
      total_gap_to_quota:       mockReps.reduce((s, r) => s + r.gap_to_quota, 0),
      at_risk_count:            mockReps.filter((r) => r.is_at_risk).length,
      coaching_count:           mockReps.filter((r) => r.needs_coaching).length,
      avg_confidence_score:     Math.round((total_confidence / n) * 10) / 10,
      avg_momentum_score:       Math.round((total_momentum / n) * 10) / 10,
      likely_attainer_count:    mockReps.filter((r) =>
        r.attainment_likelihood === "very_likely" || r.attainment_likelihood === "likely"
      ).length,
    },
  });
}
