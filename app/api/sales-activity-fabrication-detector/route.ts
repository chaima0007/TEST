import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-activity-fabrication-detector] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Alice Chen", region: "West", manager_id: "mgr_01",
    fabrication_risk: "none", fabrication_severity: "clean",
    primary_fabrication_pattern: "none", recommended_action: "no_action",
    call_authenticity_score: 5.0, meeting_authenticity_score: 4.0,
    timing_anomaly_score: 3.0, corroboration_score: 6.0,
    fabrication_composite: 4.5, is_likely_fabricating: false, requires_audit: false,
    estimated_fake_activity_pct: 3.6,
    fabrication_signal: "activity patterns authentic — all indicators within normal range",
  },
  {
    rep_id: "rep_002", rep_name: "Marcus Hayes", region: "East", manager_id: "mgr_01",
    fabrication_risk: "low", fabrication_severity: "suspicious",
    primary_fabrication_pattern: "timestamp_clustering", recommended_action: "monitor",
    call_authenticity_score: 22.0, meeting_authenticity_score: 18.0,
    timing_anomaly_score: 35.0, corroboration_score: 20.0,
    fabrication_composite: 23.4, is_likely_fabricating: false, requires_audit: false,
    estimated_fake_activity_pct: 18.7,
    fabrication_signal: "timestamp clustering — 52% of activities end-of-month — composite 23",
  },
  {
    rep_id: "rep_003", rep_name: "Sofia Reyes", region: "Central", manager_id: "mgr_02",
    fabrication_risk: "moderate", fabrication_severity: "suspicious",
    primary_fabrication_pattern: "no_follow_up", recommended_action: "audit_request",
    call_authenticity_score: 38.0, meeting_authenticity_score: 32.0,
    timing_anomaly_score: 28.0, corroboration_score: 55.0,
    fabrication_composite: 37.8, is_likely_fabricating: false, requires_audit: true,
    estimated_fake_activity_pct: 30.2,
    fabrication_signal: "no follow-up pattern — 12% follow-up rate after contacts — composite 38",
  },
  {
    rep_id: "rep_004", rep_name: "Ryan Blackwell", region: "Southeast", manager_id: "mgr_02",
    fabrication_risk: "moderate", fabrication_severity: "suspicious",
    primary_fabrication_pattern: "bulk_logging", recommended_action: "audit_request",
    call_authenticity_score: 42.0, meeting_authenticity_score: 28.0,
    timing_anomaly_score: 65.0, corroboration_score: 35.0,
    fabrication_composite: 42.3, is_likely_fabricating: false, requires_audit: true,
    estimated_fake_activity_pct: 33.8,
    fabrication_signal: "bulk logging detected — 4 bulk events, 58% end-of-month activity — composite 42",
  },
  {
    rep_id: "rep_005", rep_name: "Priya Nair", region: "Northeast", manager_id: "mgr_03",
    fabrication_risk: "high", fabrication_severity: "likely_fabricated",
    primary_fabrication_pattern: "phantom_calls", recommended_action: "manager_review",
    call_authenticity_score: 82.0, meeting_authenticity_score: 55.0,
    timing_anomaly_score: 60.0, corroboration_score: 70.0,
    fabrication_composite: 67.4, is_likely_fabricating: true, requires_audit: true,
    estimated_fake_activity_pct: 53.9,
    fabrication_signal: "phantom call pattern — avg 18s call duration, 3/42 calls with notes — composite 67",
  },
  {
    rep_id: "rep_006", rep_name: "Jordan Walsh", region: "Northwest", manager_id: "mgr_03",
    fabrication_risk: "none", fabrication_severity: "clean",
    primary_fabrication_pattern: "none", recommended_action: "no_action",
    call_authenticity_score: 4.0, meeting_authenticity_score: 5.0,
    timing_anomaly_score: 8.0, corroboration_score: 7.0,
    fabrication_composite: 5.8, is_likely_fabricating: false, requires_audit: false,
    estimated_fake_activity_pct: 4.6,
    fabrication_signal: "activity patterns authentic — all indicators within normal range",
  },
  {
    rep_id: "rep_007", rep_name: "Caleb Stone", region: "Southwest", manager_id: "mgr_04",
    fabrication_risk: "moderate", fabrication_severity: "suspicious",
    primary_fabrication_pattern: "note_absence", recommended_action: "audit_request",
    call_authenticity_score: 52.0, meeting_authenticity_score: 20.0,
    timing_anomaly_score: 25.0, corroboration_score: 40.0,
    fabrication_composite: 36.0, is_likely_fabricating: false, requires_audit: true,
    estimated_fake_activity_pct: 28.8,
    fabrication_signal: "note absence anomaly — 38 calls with no notes — composite 36",
  },
  {
    rep_id: "rep_008", rep_name: "Nina Cross", region: "Central", manager_id: "mgr_04",
    fabrication_risk: "critical", fabrication_severity: "confirmed_fraud",
    primary_fabrication_pattern: "fake_meetings", recommended_action: "hr_escalation",
    call_authenticity_score: 75.0, meeting_authenticity_score: 95.0,
    timing_anomaly_score: 80.0, corroboration_score: 78.0,
    fabrication_composite: 81.3, is_likely_fabricating: true, requires_audit: true,
    estimated_fake_activity_pct: 65.0,
    fabrication_signal: "meeting fabrication risk — 18% calendar match, 5% with notes — composite 81",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk     = searchParams.get("risk");
  const severity = searchParams.get("severity");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-activity-fabrication-detector`);
      if (risk)     url.searchParams.set("risk",     risk);
      if (severity) url.searchParams.set("severity", severity);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)     reps = reps.filter((r) => r.fabrication_risk     === risk);
  if (severity) reps = reps.filter((r) => r.fabrication_severity === severity);

  const risk_counts:     Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_call = 0, total_meeting = 0, total_timing = 0, total_corr = 0, total_fake = 0;

  for (const r of mockReps) {
    risk_counts[r.fabrication_risk]              = (risk_counts[r.fabrication_risk] || 0) + 1;
    severity_counts[r.fabrication_severity]      = (severity_counts[r.fabrication_severity] || 0) + 1;
    pattern_counts[r.primary_fabrication_pattern] = (pattern_counts[r.primary_fabrication_pattern] || 0) + 1;
    action_counts[r.recommended_action]          = (action_counts[r.recommended_action] || 0) + 1;
    total_comp    += r.fabrication_composite;
    total_call    += r.call_authenticity_score;
    total_meeting += r.meeting_authenticity_score;
    total_timing  += r.timing_anomaly_score;
    total_corr    += r.corroboration_score;
    total_fake    += r.estimated_fake_activity_pct;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                           n,
      risk_counts,
      severity_counts,
      pattern_counts,
      action_counts,
      avg_fabrication_composite:       Math.round((total_comp    / n) * 10) / 10,
      likely_fabricating_count:        mockReps.filter((r) => r.is_likely_fabricating).length,
      audit_required_count:            mockReps.filter((r) => r.requires_audit).length,
      avg_call_authenticity_score:     Math.round((total_call    / n) * 10) / 10,
      avg_meeting_authenticity_score:  Math.round((total_meeting / n) * 10) / 10,
      avg_timing_anomaly_score:        Math.round((total_timing  / n) * 10) / 10,
      avg_corroboration_score:         Math.round((total_corr    / n) * 10) / 10,
      avg_estimated_fake_activity_pct: Math.round((total_fake    / n) * 10) / 10,
    },
  }));
}
