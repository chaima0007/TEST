import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── scoring helpers (mirrors Python engine exactly) ──────────────────────────

function clamp(v: number): number {
  return Math.max(0, Math.min(100, v));
}

function pipelineScore(p: RawInput): number {
  let score = 0;
  if (p.pipeline_success_rate_pct <= 0.80) score += 40;
  else if (p.pipeline_success_rate_pct <= 0.92) score += 22;
  else if (p.pipeline_success_rate_pct <= 0.97) score += 8;
  if (p.avg_pipeline_lag_minutes >= 120) score += 35;
  else if (p.avg_pipeline_lag_minutes >= 60) score += 18;
  else if (p.avg_pipeline_lag_minutes >= 30) score += 6;
  if (p.source_system_failure_count >= 5) score += 25;
  else if (p.source_system_failure_count >= 2) score += 12;
  return clamp(score);
}

function qualityScore(p: RawInput): number {
  let score = 0;
  if (p.data_completeness_pct <= 0.85) score += 40;
  else if (p.data_completeness_pct <= 0.92) score += 22;
  else if (p.data_completeness_pct <= 0.97) score += 8;
  if (p.null_rate_pct >= 0.10) score += 35;
  else if (p.null_rate_pct >= 0.05) score += 18;
  else if (p.null_rate_pct >= 0.02) score += 6;
  if (p.duplicate_record_rate_pct >= 0.05) score += 25;
  else if (p.duplicate_record_rate_pct >= 0.02) score += 12;
  return clamp(score);
}

function analyticsScore(p: RawInput): number {
  let score = 0;
  if (p.data_drift_score >= 0.60) score += 45;
  else if (p.data_drift_score >= 0.35) score += 25;
  else if (p.data_drift_score >= 0.15) score += 10;
  if (p.model_accuracy_decay_pct >= 0.20) score += 30;
  else if (p.model_accuracy_decay_pct >= 0.10) score += 15;
  if (p.dashboard_error_rate_pct >= 0.15) score += 25;
  else if (p.dashboard_error_rate_pct >= 0.05) score += 12;
  return clamp(score);
}

function governanceScore(p: RawInput): number {
  let score = 0;
  if (p.access_control_violations >= 5) score += 40;
  else if (p.access_control_violations >= 2) score += 22;
  else if (p.access_control_violations >= 1) score += 8;
  if (p.data_retention_compliance_pct <= 0.70) score += 35;
  else if (p.data_retention_compliance_pct <= 0.85) score += 18;
  else if (p.data_retention_compliance_pct <= 0.95) score += 6;
  if (p.cross_system_reconciliation_gap_pct >= 0.15) score += 25;
  else if (p.cross_system_reconciliation_gap_pct >= 0.08) score += 12;
  return clamp(score);
}

function classifyRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function classifySeverity(composite: number): string {
  if (composite >= 60) return "blind";
  if (composite >= 40) return "unreliable";
  if (composite >= 20) return "degraded";
  return "reliable";
}

function classifyPattern(p: RawInput): string {
  if (p.pipeline_success_rate_pct <= 0.85 && p.source_system_failure_count >= 3)
    return "pipeline_failure";
  if (p.data_drift_score >= 0.50 && p.feature_distribution_shift >= 0.40)
    return "data_drift";
  if (p.data_completeness_pct <= 0.88 && p.null_rate_pct >= 0.08)
    return "quality_degradation";
  if (p.model_accuracy_decay_pct >= 0.15 && p.prediction_confidence_score <= 0.55)
    return "model_staleness";
  if (p.dashboard_error_rate_pct >= 0.12 && p.analyst_query_failure_rate_pct >= 0.10)
    return "insight_gap";
  return "none";
}

function classifyAction(risk: string, pattern: string): string {
  if (risk === "critical" && (pattern === "pipeline_failure" || pattern === "data_drift"))
    return "analytics_emergency";
  if (risk === "critical") return "data_governance_review";
  if (risk === "high") {
    if (pattern === "pipeline_failure") return "pipeline_repair";
    if (pattern === "data_drift") return "drift_investigation";
    if (pattern === "quality_degradation") return "data_quality_remediation";
    if (pattern === "model_staleness") return "model_retraining";
    if (pattern === "insight_gap") return "schema_validation";
    return "data_monitoring";
  }
  if (risk === "moderate") return "data_monitoring";
  return "no_action";
}

function dataSignal(composite: number, p: RawInput, risk: string): string {
  if (composite < 20)
    return "Data pipelines reliable — quality, analytics and governance within operational standards";
  const label = risk.charAt(0).toUpperCase() + risk.slice(1);
  return (
    `${label} — ${Math.round(p.pipeline_success_rate_pct * 100)}% pipeline success` +
    ` — ${Math.round(p.data_completeness_pct * 100)}% completeness` +
    ` — drift ${Math.round(p.data_drift_score * 100)}` +
    ` — composite ${Math.round(composite)}`
  );
}

function assessPipeline(p: RawInput): Pipeline {
  const ps = pipelineScore(p);
  const qs = qualityScore(p);
  const as_ = analyticsScore(p);
  const gs = governanceScore(p);
  const raw = ps * 0.30 + qs * 0.25 + as_ * 0.25 + gs * 0.20;
  const composite = Math.min(Math.round(raw * 100) / 100, 100.0);
  const risk = classifyRisk(composite);
  const severity = classifySeverity(composite);
  const pattern = classifyPattern(p);
  const action = classifyAction(risk, pattern);
  const has_data_alert =
    composite >= 40 || p.pipeline_success_rate_pct <= 0.90 || p.data_drift_score >= 0.35;
  const requires_data_governance =
    composite >= 25 || p.access_control_violations >= 1 || p.data_retention_compliance_pct <= 0.90;
  const estimated_insight_delay_hours =
    Math.round((p.avg_pipeline_lag_minutes / 60) * (composite / 100 + 1) * 100) / 100;
  return {
    pipeline_id: p.pipeline_id,
    region: p.region,
    data_domain: p.data_domain,
    data_risk: risk,
    data_pattern: pattern,
    data_severity: severity,
    recommended_action: action,
    pipeline_score: Math.round(ps * 10) / 10,
    quality_score: Math.round(qs * 10) / 10,
    analytics_score: Math.round(as_ * 10) / 10,
    governance_score: Math.round(gs * 10) / 10,
    data_composite: composite,
    has_data_alert,
    requires_data_governance,
    estimated_insight_delay_hours,
    data_signal: dataSignal(composite, p, risk),
  };
}

// ── types ────────────────────────────────────────────────────────────────────

interface RawInput {
  pipeline_id: string;
  data_domain: string;
  region: string;
  pipeline_success_rate_pct: number;
  avg_pipeline_lag_minutes: number;
  data_completeness_pct: number;
  null_rate_pct: number;
  duplicate_record_rate_pct: number;
  schema_change_count_30d: number;
  data_drift_score: number;
  feature_distribution_shift: number;
  model_accuracy_decay_pct: number;
  prediction_confidence_score: number;
  report_delivery_failure_rate_pct: number;
  dashboard_error_rate_pct: number;
  analyst_query_failure_rate_pct: number;
  data_volume_anomaly_pct: number;
  source_system_failure_count: number;
  data_retention_compliance_pct: number;
  access_control_violations: number;
  row_count_variance_pct: number;
  cross_system_reconciliation_gap_pct: number;
}

interface Pipeline {
  pipeline_id: string;
  region: string;
  data_domain: string;
  data_risk: string;
  data_pattern: string;
  data_severity: string;
  recommended_action: string;
  pipeline_score: number;
  quality_score: number;
  analytics_score: number;
  governance_score: number;
  data_composite: number;
  has_data_alert: boolean;
  requires_data_governance: boolean;
  estimated_insight_delay_hours: number;
  data_signal: string;
}

// ── mock raw inputs ───────────────────────────────────────────────────────────

const mockInputs: RawInput[] = [
  {
    pipeline_id: "DP-001", data_domain: "sales", region: "AMER",
    pipeline_success_rate_pct: 0.99, avg_pipeline_lag_minutes: 5,
    data_completeness_pct: 0.99, null_rate_pct: 0.005,
    duplicate_record_rate_pct: 0.003, schema_change_count_30d: 0,
    data_drift_score: 0.05, feature_distribution_shift: 0.03,
    model_accuracy_decay_pct: 0.02, prediction_confidence_score: 0.95,
    report_delivery_failure_rate_pct: 0.02, dashboard_error_rate_pct: 0.01,
    analyst_query_failure_rate_pct: 0.01, data_volume_anomaly_pct: 0.02,
    source_system_failure_count: 0, data_retention_compliance_pct: 0.99,
    access_control_violations: 0, row_count_variance_pct: 0.01,
    cross_system_reconciliation_gap_pct: 0.01,
  },
  {
    pipeline_id: "DP-002", data_domain: "finance", region: "EMEA",
    pipeline_success_rate_pct: 0.94, avg_pipeline_lag_minutes: 25,
    data_completeness_pct: 0.95, null_rate_pct: 0.015,
    duplicate_record_rate_pct: 0.008, schema_change_count_30d: 1,
    data_drift_score: 0.20, feature_distribution_shift: 0.15,
    model_accuracy_decay_pct: 0.06, prediction_confidence_score: 0.85,
    report_delivery_failure_rate_pct: 0.05, dashboard_error_rate_pct: 0.03,
    analyst_query_failure_rate_pct: 0.03, data_volume_anomaly_pct: 0.05,
    source_system_failure_count: 1, data_retention_compliance_pct: 0.93,
    access_control_violations: 1, row_count_variance_pct: 0.05,
    cross_system_reconciliation_gap_pct: 0.04,
  },
  {
    pipeline_id: "DP-003", data_domain: "marketing", region: "APAC",
    pipeline_success_rate_pct: 0.89, avg_pipeline_lag_minutes: 45,
    data_completeness_pct: 0.90, null_rate_pct: 0.04,
    duplicate_record_rate_pct: 0.015, schema_change_count_30d: 2,
    data_drift_score: 0.38, feature_distribution_shift: 0.32,
    model_accuracy_decay_pct: 0.12, prediction_confidence_score: 0.75,
    report_delivery_failure_rate_pct: 0.10, dashboard_error_rate_pct: 0.06,
    analyst_query_failure_rate_pct: 0.06, data_volume_anomaly_pct: 0.10,
    source_system_failure_count: 2, data_retention_compliance_pct: 0.88,
    access_control_violations: 2, row_count_variance_pct: 0.10,
    cross_system_reconciliation_gap_pct: 0.07,
  },
  {
    pipeline_id: "DP-004", data_domain: "operations", region: "LATAM",
    pipeline_success_rate_pct: 0.82, avg_pipeline_lag_minutes: 75,
    data_completeness_pct: 0.86, null_rate_pct: 0.09,
    duplicate_record_rate_pct: 0.03, schema_change_count_30d: 3,
    data_drift_score: 0.55, feature_distribution_shift: 0.45,
    model_accuracy_decay_pct: 0.18, prediction_confidence_score: 0.60,
    report_delivery_failure_rate_pct: 0.18, dashboard_error_rate_pct: 0.10,
    analyst_query_failure_rate_pct: 0.10, data_volume_anomaly_pct: 0.20,
    source_system_failure_count: 3, data_retention_compliance_pct: 0.82,
    access_control_violations: 0, row_count_variance_pct: 0.18,
    cross_system_reconciliation_gap_pct: 0.12,
  },
  {
    pipeline_id: "DP-005", data_domain: "hr", region: "AMER",
    pipeline_success_rate_pct: 0.75, avg_pipeline_lag_minutes: 100,
    data_completeness_pct: 0.80, null_rate_pct: 0.15,
    duplicate_record_rate_pct: 0.06, schema_change_count_30d: 4,
    data_drift_score: 0.65, feature_distribution_shift: 0.55,
    model_accuracy_decay_pct: 0.25, prediction_confidence_score: 0.45,
    report_delivery_failure_rate_pct: 0.28, dashboard_error_rate_pct: 0.18,
    analyst_query_failure_rate_pct: 0.18, data_volume_anomaly_pct: 0.30,
    source_system_failure_count: 4, data_retention_compliance_pct: 0.75,
    access_control_violations: 3, row_count_variance_pct: 0.28,
    cross_system_reconciliation_gap_pct: 0.18,
  },
  {
    pipeline_id: "DP-006", data_domain: "product", region: "EMEA",
    pipeline_success_rate_pct: 0.65, avg_pipeline_lag_minutes: 150,
    data_completeness_pct: 0.70, null_rate_pct: 0.22,
    duplicate_record_rate_pct: 0.09, schema_change_count_30d: 6,
    data_drift_score: 0.75, feature_distribution_shift: 0.70,
    model_accuracy_decay_pct: 0.35, prediction_confidence_score: 0.30,
    report_delivery_failure_rate_pct: 0.38, dashboard_error_rate_pct: 0.28,
    analyst_query_failure_rate_pct: 0.28, data_volume_anomaly_pct: 0.40,
    source_system_failure_count: 5, data_retention_compliance_pct: 0.65,
    access_control_violations: 5, row_count_variance_pct: 0.40,
    cross_system_reconciliation_gap_pct: 0.25,
  },
  {
    pipeline_id: "DP-007", data_domain: "support", region: "APAC",
    pipeline_success_rate_pct: 0.55, avg_pipeline_lag_minutes: 180,
    data_completeness_pct: 0.60, null_rate_pct: 0.30,
    duplicate_record_rate_pct: 0.12, schema_change_count_30d: 8,
    data_drift_score: 0.85, feature_distribution_shift: 0.80,
    model_accuracy_decay_pct: 0.45, prediction_confidence_score: 0.20,
    report_delivery_failure_rate_pct: 0.50, dashboard_error_rate_pct: 0.40,
    analyst_query_failure_rate_pct: 0.40, data_volume_anomaly_pct: 0.55,
    source_system_failure_count: 6, data_retention_compliance_pct: 0.55,
    access_control_violations: 6, row_count_variance_pct: 0.55,
    cross_system_reconciliation_gap_pct: 0.35,
  },
  {
    pipeline_id: "DP-008", data_domain: "logistics", region: "GLOBAL",
    pipeline_success_rate_pct: 0.50, avg_pipeline_lag_minutes: 200,
    data_completeness_pct: 0.60, null_rate_pct: 0.20,
    duplicate_record_rate_pct: 0.10, schema_change_count_30d: 8,
    data_drift_score: 0.80, feature_distribution_shift: 0.75,
    model_accuracy_decay_pct: 0.35, prediction_confidence_score: 0.20,
    report_delivery_failure_rate_pct: 0.40, dashboard_error_rate_pct: 0.30,
    analyst_query_failure_rate_pct: 0.25, data_volume_anomaly_pct: 0.50,
    source_system_failure_count: 6, data_retention_compliance_pct: 0.50,
    access_control_violations: 6, row_count_variance_pct: 0.40,
    cross_system_reconciliation_gap_pct: 0.30,
  },
];

const mockPipelines: Pipeline[] = mockInputs.map(assessPipeline);

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/data-analytics-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let pipelines = [...mockPipelines];
  if (risk)    pipelines = pipelines.filter((p) => p.data_risk    === risk);
  if (pattern) pipelines = pipelines.filter((p) => p.data_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_pipe = 0, total_qual = 0, total_anal = 0, total_gov = 0, total_delay = 0;

  for (const p of mockPipelines) {
    risk_counts[p.data_risk]         = (risk_counts[p.data_risk]         || 0) + 1;
    pattern_counts[p.data_pattern]   = (pattern_counts[p.data_pattern]   || 0) + 1;
    severity_counts[p.data_severity] = (severity_counts[p.data_severity] || 0) + 1;
    action_counts[p.recommended_action] = (action_counts[p.recommended_action] || 0) + 1;
    total_comp  += p.data_composite;
    total_pipe  += p.pipeline_score;
    total_qual  += p.quality_score;
    total_anal  += p.analytics_score;
    total_gov   += p.governance_score;
    total_delay += p.estimated_insight_delay_hours;
  }

  const n = mockPipelines.length;

  return NextResponse.json({
    pipelines,
    summary: {
      total:                            n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_data_composite:               Math.round((total_comp  / n) * 100) / 100,
      data_alert_count:                 mockPipelines.filter((p) => p.has_data_alert).length,
      governance_count:                 mockPipelines.filter((p) => p.requires_data_governance).length,
      avg_pipeline_score:               Math.round((total_pipe  / n) * 10) / 10,
      avg_quality_score:                Math.round((total_qual  / n) * 10) / 10,
      avg_analytics_score:              Math.round((total_anal  / n) * 10) / 10,
      avg_governance_score:             Math.round((total_gov   / n) * 10) / 10,
      avg_estimated_insight_delay_hours: Math.round((total_delay / n) * 100) / 100,
    },
  });
}
