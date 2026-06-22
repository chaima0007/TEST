import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-territory-overlap-conflict-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    overlap_risk: "low", overlap_pattern: "none",
    overlap_severity: "clean", recommended_action: "no_action",
    account_collision_score: 0.0, pipeline_duplication_score: 0.0,
    channel_conflict_score: 0.0, boundary_integrity_score: 0.0,
    overlap_composite: 0.0, is_territory_conflict: false, requires_arbitration: false,
    estimated_at_risk_pipeline_usd: 0.0,
    overlap_signal: "Territory boundaries respected — no conflict detected",
  },
  {
    rep_id: "rep_002", region: "East",
    overlap_risk: "low", overlap_pattern: "segment_spillover",
    overlap_severity: "clean", recommended_action: "no_action",
    account_collision_score: 6.0, pipeline_duplication_score: 4.0,
    channel_conflict_score: 8.0, boundary_integrity_score: 5.0,
    overlap_composite: 6.1, is_territory_conflict: false, requires_arbitration: false,
    estimated_at_risk_pipeline_usd: 3050.0,
    overlap_signal: "4 accounts outside segment — 2 cross-segment activities — composite 6",
  },
  {
    rep_id: "rep_003", region: "Central",
    overlap_risk: "moderate", overlap_pattern: "territory_boundary_blur",
    overlap_severity: "watch", recommended_action: "account_reassignment",
    account_collision_score: 20.0, pipeline_duplication_score: 15.0,
    channel_conflict_score: 18.0, boundary_integrity_score: 28.0,
    overlap_composite: 19.9, is_territory_conflict: false, requires_arbitration: false,
    estimated_at_risk_pipeline_usd: 29850.0,
    overlap_signal: "3 violation flags — 2 disputed accounts — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    overlap_risk: "moderate", overlap_pattern: "channel_partner_conflict",
    overlap_severity: "watch", recommended_action: "account_reassignment",
    account_collision_score: 18.0, pipeline_duplication_score: 22.0,
    channel_conflict_score: 37.0, boundary_integrity_score: 12.0,
    overlap_composite: 23.6, is_territory_conflict: false, requires_arbitration: false,
    estimated_at_risk_pipeline_usd: 47200.0,
    overlap_signal: "4 partner conflicts — partner score 55 — composite 24",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    overlap_risk: "high", overlap_pattern: "dual_rep_same_account",
    overlap_severity: "contested", recommended_action: "territory_review",
    account_collision_score: 40.0, pipeline_duplication_score: 48.0,
    channel_conflict_score: 25.0, boundary_integrity_score: 22.0,
    overlap_composite: 37.3, is_territory_conflict: false, requires_arbitration: true,
    estimated_at_risk_pipeline_usd: 186500.0,
    overlap_signal: "3 dual-rep deals — 2 commission disputes — composite 37",
  },
  {
    rep_id: "rep_006", region: "West",
    overlap_risk: "high", overlap_pattern: "acquisition_overlap",
    overlap_severity: "contested", recommended_action: "territory_review",
    account_collision_score: 53.0, pipeline_duplication_score: 44.0,
    channel_conflict_score: 28.0, boundary_integrity_score: 30.0,
    overlap_composite: 42.8, is_territory_conflict: true, requires_arbitration: true,
    estimated_at_risk_pipeline_usd: 342400.0,
    overlap_signal: "4 repeat overlap accounts — $800,000 pipeline at risk — composite 43",
  },
  {
    rep_id: "rep_007", region: "APAC",
    overlap_risk: "critical", overlap_pattern: "dual_rep_same_account",
    overlap_severity: "conflict", recommended_action: "manager_mediation",
    account_collision_score: 73.0, pipeline_duplication_score: 68.0,
    channel_conflict_score: 40.0, boundary_integrity_score: 55.0,
    overlap_composite: 61.4, is_territory_conflict: true, requires_arbitration: true,
    estimated_at_risk_pipeline_usd: 920000.0,
    overlap_signal: "5 dual-rep deals — 3 commission disputes — composite 61",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    overlap_risk: "critical", overlap_pattern: "acquisition_overlap",
    overlap_severity: "conflict", recommended_action: "executive_arbitration",
    account_collision_score: 85.0, pipeline_duplication_score: 80.0,
    channel_conflict_score: 60.0, boundary_integrity_score: 70.0,
    overlap_composite: 75.3, is_territory_conflict: true, requires_arbitration: true,
    estimated_at_risk_pipeline_usd: 1507500.0,
    overlap_signal: "6 repeat overlap accounts — $2,000,000 pipeline at risk — composite 75",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-territory-overlap-conflict-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.overlap_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.overlap_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_acc = 0, total_pip = 0, total_ch = 0, total_bnd = 0;
  let total_at_risk = 0;

  for (const r of mockReps) {
    risk_counts[r.overlap_risk]       = (risk_counts[r.overlap_risk] || 0) + 1;
    pattern_counts[r.overlap_pattern] = (pattern_counts[r.overlap_pattern] || 0) + 1;
    severity_counts[r.overlap_severity] = (severity_counts[r.overlap_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp     += r.overlap_composite;
    total_acc      += r.account_collision_score;
    total_pip      += r.pipeline_duplication_score;
    total_ch       += r.channel_conflict_score;
    total_bnd      += r.boundary_integrity_score;
    total_at_risk  += r.estimated_at_risk_pipeline_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                  n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_overlap_composite:                  Math.round((total_comp / n) * 10) / 10,
      territory_conflict_count:               mockReps.filter((r) => r.is_territory_conflict).length,
      arbitration_count:                      mockReps.filter((r) => r.requires_arbitration).length,
      avg_account_collision_score:            Math.round((total_acc  / n) * 10) / 10,
      avg_pipeline_duplication_score:         Math.round((total_pip  / n) * 10) / 10,
      avg_channel_conflict_score:             Math.round((total_ch   / n) * 10) / 10,
      avg_boundary_integrity_score:           Math.round((total_bnd  / n) * 10) / 10,
      total_estimated_at_risk_pipeline_usd:   Math.round(total_at_risk * 100) / 100,
    },
  }));
}
