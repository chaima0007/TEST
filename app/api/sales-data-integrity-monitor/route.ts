import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockRecords = [
  {
    record_id: "rec_001", rep_id: "rep_alice",
    integrity_risk: "clean", anomaly_type: "missing_required_fields",
    data_quality: "excellent", integrity_action: "no_action",
    pipeline_accuracy_score: 97.0, data_completeness_score: 95.0,
    behavioral_consistency_score: 98.0, compliance_score: 99.0,
    integrity_composite: 97.0, risk_signal_count: 0,
    is_clean: true, needs_escalation: false,
    primary_integrity_signal: "data integrity within acceptable parameters",
  },
  {
    record_id: "rec_002", rep_id: "rep_bruno",
    integrity_risk: "critical_breach", anomaly_type: "inflated_deal_value",
    data_quality: "poor", integrity_action: "compliance_escalation",
    pipeline_accuracy_score: 28.0, data_completeness_score: 22.0,
    behavioral_consistency_score: 18.0, compliance_score: 15.0,
    integrity_composite: 21.1, risk_signal_count: 7,
    is_clean: false, needs_escalation: true,
    primary_integrity_signal: "5 CRM login anomalies — potential unauthorized access",
  },
  {
    record_id: "rec_003", rep_id: "rep_clara",
    integrity_risk: "minor_issues", anomaly_type: "missing_required_fields",
    data_quality: "good", integrity_action: "flag_for_review",
    pipeline_accuracy_score: 82.0, data_completeness_score: 78.0,
    behavioral_consistency_score: 85.0, compliance_score: 88.0,
    integrity_composite: 83.6, risk_signal_count: 1,
    is_clean: false, needs_escalation: false,
    primary_integrity_signal: "close date changed 3x — forecast manipulation risk",
  },
  {
    record_id: "rec_004", rep_id: "rep_diego",
    integrity_risk: "moderate_issues", anomaly_type: "close_date_manipulation",
    data_quality: "fair", integrity_action: "manager_alert",
    pipeline_accuracy_score: 55.0, data_completeness_score: 60.0,
    behavioral_consistency_score: 52.0, compliance_score: 48.0,
    integrity_composite: 54.2, risk_signal_count: 3,
    is_clean: false, needs_escalation: false,
    primary_integrity_signal: "4 backdated activities — data integrity concern",
  },
  {
    record_id: "rec_005", rep_id: "rep_elena",
    integrity_risk: "clean", anomaly_type: "missing_required_fields",
    data_quality: "excellent", integrity_action: "no_action",
    pipeline_accuracy_score: 92.0, data_completeness_score: 94.0,
    behavioral_consistency_score: 96.0, compliance_score: 97.0,
    integrity_composite: 95.0, risk_signal_count: 0,
    is_clean: true, needs_escalation: false,
    primary_integrity_signal: "data integrity within acceptable parameters",
  },
  {
    record_id: "rec_006", rep_id: "rep_felix",
    integrity_risk: "critical_breach", anomaly_type: "pipeline_stuffing",
    data_quality: "poor", integrity_action: "compliance_escalation",
    pipeline_accuracy_score: 18.0, data_completeness_score: 35.0,
    behavioral_consistency_score: 28.0, compliance_score: 22.0,
    integrity_composite: 25.8, risk_signal_count: 6,
    is_clean: false, needs_escalation: true,
    primary_integrity_signal: "deal size 80%+ above historical average — potential inflation",
  },
  {
    record_id: "rec_007", rep_id: "rep_gabriela",
    integrity_risk: "minor_issues", anomaly_type: "ghost_deal",
    data_quality: "good", integrity_action: "flag_for_review",
    pipeline_accuracy_score: 75.0, data_completeness_score: 80.0,
    behavioral_consistency_score: 72.0, compliance_score: 85.0,
    integrity_composite: 77.2, risk_signal_count: 2,
    is_clean: false, needs_escalation: false,
    primary_integrity_signal: "4 ghost deals with no activity in 30 days",
  },
  {
    record_id: "rec_008", rep_id: "rep_hiro",
    integrity_risk: "moderate_issues", anomaly_type: "duplicate_entry",
    data_quality: "fair", integrity_action: "manager_alert",
    pipeline_accuracy_score: 62.0, data_completeness_score: 55.0,
    behavioral_consistency_score: 48.0, compliance_score: 58.0,
    integrity_composite: 55.8, risk_signal_count: 3,
    is_clean: false, needs_escalation: false,
    primary_integrity_signal: "3 approval bypasses — compliance risk",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const quality = searchParams.get("quality");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-data-integrity-monitor`);
      if (risk)    url.searchParams.set("risk", risk);
      if (quality) url.searchParams.set("quality", quality);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let records = [...mockRecords];
  if (risk)    records = records.filter((r) => r.integrity_risk === risk);
  if (quality) records = records.filter((r) => r.data_quality === quality);

  const risk_counts:    Record<string, number> = {};
  const anomaly_counts: Record<string, number> = {};
  const quality_counts: Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  let total_comp = 0, total_pipe = 0, total_comp_ = 0, total_beh = 0, total_compl = 0;

  for (const r of mockRecords) {
    risk_counts[r.integrity_risk]      = (risk_counts[r.integrity_risk] || 0) + 1;
    anomaly_counts[r.anomaly_type]     = (anomaly_counts[r.anomaly_type] || 0) + 1;
    quality_counts[r.data_quality]     = (quality_counts[r.data_quality] || 0) + 1;
    action_counts[r.integrity_action]  = (action_counts[r.integrity_action] || 0) + 1;
    total_comp  += r.integrity_composite;
    total_pipe  += r.pipeline_accuracy_score;
    total_comp_ += r.data_completeness_score;
    total_beh   += r.behavioral_consistency_score;
    total_compl += r.compliance_score;
  }

  const n = mockRecords.length;

  return NextResponse.json({
    records,
    summary: {
      total: n,
      risk_counts,
      anomaly_counts,
      quality_counts,
      action_counts,
      avg_integrity_composite:          Math.round((total_comp / n) * 10) / 10,
      clean_count:                      mockRecords.filter((r) => r.is_clean).length,
      escalation_count:                 mockRecords.filter((r) => r.needs_escalation).length,
      avg_pipeline_accuracy_score:      Math.round((total_pipe / n) * 10) / 10,
      avg_data_completeness_score:      Math.round((total_comp_ / n) * 10) / 10,
      avg_behavioral_consistency_score: Math.round((total_beh / n) * 10) / 10,
      avg_compliance_score:             Math.round((total_compl / n) * 10) / 10,
      high_risk_rep_count:              mockRecords.filter((r) => r.integrity_risk === "critical_breach").length,
    },
  });
}
