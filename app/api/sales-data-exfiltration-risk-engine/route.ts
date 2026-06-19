import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    exfiltration_risk: "low", exfiltration_pattern: "none",
    exfiltration_severity: "normal", recommended_action: "no_action",
    export_anomaly_score: 0.0, access_pattern_score: 0.0,
    boundary_violation_score: 0.0, behavioral_risk_score: 0.0,
    exfiltration_composite: 0.0, is_exfiltration_risk: false, requires_immediate_review: false,
    estimated_records_at_risk: 50,
    exfiltration_signal: "CRM access behavior within normal parameters",
  },
  {
    rep_id: "rep_002", region: "East",
    exfiltration_risk: "low", exfiltration_pattern: "territory_boundary_breach",
    exfiltration_severity: "normal", recommended_action: "audit_trail_review",
    export_anomaly_score: 5.0, access_pattern_score: 8.0,
    boundary_violation_score: 22.0, behavioral_risk_score: 0.0,
    exfiltration_composite: 8.7, is_exfiltration_risk: false, requires_immediate_review: false,
    estimated_records_at_risk: 120,
    exfiltration_signal: "8 accounts outside territory — 5 violation(s) — composite 9",
  },
  {
    rep_id: "rep_003", region: "Central",
    exfiltration_risk: "moderate", exfiltration_pattern: "unusual_access_hours",
    exfiltration_severity: "suspicious", recommended_action: "audit_trail_review",
    export_anomaly_score: 8.0, access_pattern_score: 38.0,
    boundary_violation_score: 12.0, behavioral_risk_score: 5.0,
    exfiltration_composite: 16.3, is_exfiltration_risk: false, requires_immediate_review: false,
    estimated_records_at_risk: 250,
    exfiltration_signal: "3 after-hours bulk action(s) — 12 off-hours sessions — composite 16",
  },
  {
    rep_id: "rep_004", region: "Southeast",
    exfiltration_risk: "moderate", exfiltration_pattern: "bulk_export",
    exfiltration_severity: "suspicious", recommended_action: "audit_trail_review",
    export_anomaly_score: 40.0, access_pattern_score: 15.0,
    boundary_violation_score: 8.0, behavioral_risk_score: 5.0,
    exfiltration_composite: 19.8, is_exfiltration_risk: false, requires_immediate_review: false,
    estimated_records_at_risk: 1200,
    exfiltration_signal: "8 CRM exports — 1200 records — 2 bulk downloads — composite 20",
  },
  {
    rep_id: "rep_005", region: "Northeast",
    exfiltration_risk: "high", exfiltration_pattern: "bulk_export",
    exfiltration_severity: "concerning", recommended_action: "access_restriction",
    export_anomaly_score: 55.0, access_pattern_score: 30.0,
    boundary_violation_score: 20.0, behavioral_risk_score: 10.0,
    exfiltration_composite: 30.8, is_exfiltration_risk: false, requires_immediate_review: true,
    estimated_records_at_risk: 3500,
    exfiltration_signal: "15 CRM exports — 3500 records — 4 bulk downloads — composite 31",
  },
  {
    rep_id: "rep_006", region: "Northwest",
    exfiltration_risk: "high", exfiltration_pattern: "territory_boundary_breach",
    exfiltration_severity: "concerning", recommended_action: "access_restriction",
    export_anomaly_score: 20.0, access_pattern_score: 35.0,
    boundary_violation_score: 48.0, behavioral_risk_score: 15.0,
    exfiltration_composite: 30.5, is_exfiltration_risk: false, requires_immediate_review: true,
    estimated_records_at_risk: 580,
    exfiltration_signal: "22 accounts outside territory — 12 violation(s) — composite 31",
  },
  {
    rep_id: "rep_007", region: "Southwest",
    exfiltration_risk: "critical", exfiltration_pattern: "pre_departure_download",
    exfiltration_severity: "threat", recommended_action: "immediate_lockdown",
    export_anomaly_score: 65.0, access_pattern_score: 50.0,
    boundary_violation_score: 35.0, behavioral_risk_score: 40.0,
    exfiltration_composite: 49.8, is_exfiltration_risk: true, requires_immediate_review: true,
    estimated_records_at_risk: 8500,
    exfiltration_signal: "Resignation signal 14d ago — 8500 records exported — 5 bulk downloads — composite 50",
  },
  {
    rep_id: "rep_008", region: "Mountain",
    exfiltration_risk: "critical", exfiltration_pattern: "account_scraping",
    exfiltration_severity: "threat", recommended_action: "immediate_lockdown",
    export_anomaly_score: 75.0, access_pattern_score: 65.0,
    boundary_violation_score: 50.0, behavioral_risk_score: 70.0,
    exfiltration_composite: 65.8, is_exfiltration_risk: true, requires_immediate_review: true,
    estimated_records_at_risk: 15000,
    exfiltration_signal: "2 admin impersonation attempt(s) — 3 personal storage alert(s) — composite 66",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-data-exfiltration-risk-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.exfiltration_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.exfiltration_pattern === pattern);

  const risk_counts:    Record<string, number> = {};
  const pattern_counts: Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  let total_comp = 0, total_exp = 0, total_acc = 0, total_bnd = 0, total_beh = 0;
  let total_rec = 0;

  for (const r of mockReps) {
    risk_counts[r.exfiltration_risk]       = (risk_counts[r.exfiltration_risk] || 0) + 1;
    pattern_counts[r.exfiltration_pattern] = (pattern_counts[r.exfiltration_pattern] || 0) + 1;
    severity_counts[r.exfiltration_severity] = (severity_counts[r.exfiltration_severity] || 0) + 1;
    action_counts[r.recommended_action]    = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.exfiltration_composite;
    total_exp  += r.export_anomaly_score;
    total_acc  += r.access_pattern_score;
    total_bnd  += r.boundary_violation_score;
    total_beh  += r.behavioral_risk_score;
    total_rec  += r.estimated_records_at_risk;
  }

  const n = mockReps.length;

  return NextResponse.json(sealResponse({
    reps,
    summary: {
      total:                           n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_exfiltration_composite:      Math.round((total_comp / n) * 10) / 10,
      exfiltration_risk_count:         mockReps.filter((r) => r.is_exfiltration_risk).length,
      immediate_review_count:          mockReps.filter((r) => r.requires_immediate_review).length,
      avg_export_anomaly_score:        Math.round((total_exp  / n) * 10) / 10,
      avg_access_pattern_score:        Math.round((total_acc  / n) * 10) / 10,
      avg_boundary_violation_score:    Math.round((total_bnd  / n) * 10) / 10,
      avg_behavioral_risk_score:       Math.round((total_beh  / n) * 10) / 10,
      total_estimated_records_at_risk: total_rec,
    },
  } as Record<string,unknown>));
}
