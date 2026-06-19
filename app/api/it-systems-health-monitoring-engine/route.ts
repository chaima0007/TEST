import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockSystems = [
  {
    system_id: "SYS-001", environment: "production", region: "us-east-1",
    system_risk: "critical", system_pattern: "security_incident",
    system_severity: "critical", recommended_action: "disaster_recovery",
    performance_score: 48.0, capacity_score: 65.0, security_score: 80.0, reliability_score: 55.0,
    system_composite: 61.5,
    has_system_alert: true, requires_immediate_action: true,
    estimated_downtime_risk_hours: 4.32,
    system_signal: "CRITICAL — 72% CPU — 12% error rate — 94.5% uptime — 12 vulns — composite 62",
    cpu_utilization_pct: 0.72, memory_utilization_pct: 0.68, disk_utilization_pct: 0.55,
    network_latency_ms: 320, error_rate_pct: 0.12, uptime_pct: 0.945,
    incident_count_30d: 9, mean_time_to_recovery_hours: 6.5,
    security_vulnerability_count: 12, failed_security_scans: 4,
    patch_compliance_pct: 0.52, integration_failure_rate_pct: 0.08,
    api_error_rate_pct: 0.06, data_pipeline_lag_minutes: 45.0,
    sla_compliance_pct: 0.88, backup_success_rate_pct: 0.75,
    change_failure_rate_pct: 0.18, deployment_frequency_per_week: 3.0,
    avg_response_time_ms: 1800,
  },
  {
    system_id: "SYS-002", environment: "production", region: "eu-west-1",
    system_risk: "high", system_pattern: "performance_degradation",
    system_severity: "impaired", recommended_action: "performance_tuning",
    performance_score: 75.0, capacity_score: 30.0, security_score: 22.0, reliability_score: 35.0,
    system_composite: 42.5,
    has_system_alert: true, requires_immediate_action: true,
    estimated_downtime_risk_hours: 1.87,
    system_signal: "HIGH — 58% CPU — 9% error rate — 97.2% uptime — 6 vulns — composite 43",
    cpu_utilization_pct: 0.58, memory_utilization_pct: 0.62, disk_utilization_pct: 0.48,
    network_latency_ms: 640, error_rate_pct: 0.09, uptime_pct: 0.972,
    incident_count_30d: 5, mean_time_to_recovery_hours: 4.0,
    security_vulnerability_count: 6, failed_security_scans: 1,
    patch_compliance_pct: 0.74, integration_failure_rate_pct: 0.05,
    api_error_rate_pct: 0.04, data_pipeline_lag_minutes: 18.0,
    sla_compliance_pct: 0.91, backup_success_rate_pct: 0.90,
    change_failure_rate_pct: 0.12, deployment_frequency_per_week: 5.0,
    avg_response_time_ms: 1650,
  },
  {
    system_id: "SYS-003", environment: "staging", region: "us-west-2",
    system_risk: "high", system_pattern: "capacity_breach",
    system_severity: "impaired", recommended_action: "capacity_expansion",
    performance_score: 30.0, capacity_score: 75.0, security_score: 18.0, reliability_score: 25.0,
    system_composite: 37.5,
    has_system_alert: true, requires_immediate_action: true,
    estimated_downtime_risk_hours: 0.94,
    system_signal: "HIGH — 91% CPU — 4% error rate — 98.8% uptime — 3 vulns — composite 38",
    cpu_utilization_pct: 0.91, memory_utilization_pct: 0.87, disk_utilization_pct: 0.76,
    network_latency_ms: 95, error_rate_pct: 0.04, uptime_pct: 0.988,
    incident_count_30d: 3, mean_time_to_recovery_hours: 2.5,
    security_vulnerability_count: 3, failed_security_scans: 0,
    patch_compliance_pct: 0.88, integration_failure_rate_pct: 0.03,
    api_error_rate_pct: 0.02, data_pipeline_lag_minutes: 8.0,
    sla_compliance_pct: 0.95, backup_success_rate_pct: 0.97,
    change_failure_rate_pct: 0.08, deployment_frequency_per_week: 8.0,
    avg_response_time_ms: 420,
  },
  {
    system_id: "SYS-004", environment: "production", region: "ap-southeast-1",
    system_risk: "critical", system_pattern: "service_outage",
    system_severity: "critical", recommended_action: "disaster_recovery",
    performance_score: 55.0, capacity_score: 40.0, security_score: 55.0, reliability_score: 61.0,
    system_composite: 52.3,
    has_system_alert: true, requires_immediate_action: true,
    estimated_downtime_risk_hours: 3.58,
    system_signal: "CRITICAL — 80% CPU — 7% error rate — 93.0% uptime — 8 vulns — composite 52",
    cpu_utilization_pct: 0.80, memory_utilization_pct: 0.74, disk_utilization_pct: 0.62,
    network_latency_ms: 210, error_rate_pct: 0.07, uptime_pct: 0.930,
    incident_count_30d: 8, mean_time_to_recovery_hours: 7.0,
    security_vulnerability_count: 8, failed_security_scans: 2,
    patch_compliance_pct: 0.65, integration_failure_rate_pct: 0.09,
    api_error_rate_pct: 0.07, data_pipeline_lag_minutes: 32.0,
    sla_compliance_pct: 0.82, backup_success_rate_pct: 0.84,
    change_failure_rate_pct: 0.22, deployment_frequency_per_week: 2.0,
    avg_response_time_ms: 980,
  },
  {
    system_id: "SYS-005", environment: "development", region: "us-east-1",
    system_risk: "moderate", system_pattern: "integration_failure",
    system_severity: "degraded", recommended_action: "health_monitoring",
    performance_score: 14.0, capacity_score: 8.0, security_score: 22.0, reliability_score: 28.0,
    system_composite: 17.5,
    has_system_alert: true, requires_immediate_action: true,
    estimated_downtime_risk_hours: 0.28,
    system_signal: "MODERATE — 55% CPU — 3% error rate — 98.5% uptime — 4 vulns — composite 18",
    cpu_utilization_pct: 0.55, memory_utilization_pct: 0.48, disk_utilization_pct: 0.40,
    network_latency_ms: 140, error_rate_pct: 0.03, uptime_pct: 0.985,
    incident_count_30d: 4, mean_time_to_recovery_hours: 1.8,
    security_vulnerability_count: 4, failed_security_scans: 1,
    patch_compliance_pct: 0.82, integration_failure_rate_pct: 0.18,
    api_error_rate_pct: 0.12, data_pipeline_lag_minutes: 22.0,
    sla_compliance_pct: 0.93, backup_success_rate_pct: 0.94,
    change_failure_rate_pct: 0.10, deployment_frequency_per_week: 12.0,
    avg_response_time_ms: 310,
  },
  {
    system_id: "SYS-006", environment: "production", region: "eu-central-1",
    system_risk: "low", system_pattern: "none",
    system_severity: "nominal", recommended_action: "no_action",
    performance_score: 6.0, capacity_score: 8.0, security_score: 10.0, reliability_score: 6.0,
    system_composite: 7.5,
    has_system_alert: false, requires_immediate_action: false,
    estimated_downtime_risk_hours: 0.03,
    system_signal: "System health nominal — performance, capacity, security and reliability within operational thresholds",
    cpu_utilization_pct: 0.42, memory_utilization_pct: 0.38, disk_utilization_pct: 0.30,
    network_latency_ms: 45, error_rate_pct: 0.01, uptime_pct: 0.999,
    incident_count_30d: 1, mean_time_to_recovery_hours: 0.5,
    security_vulnerability_count: 1, failed_security_scans: 0,
    patch_compliance_pct: 0.96, integration_failure_rate_pct: 0.01,
    api_error_rate_pct: 0.01, data_pipeline_lag_minutes: 2.0,
    sla_compliance_pct: 0.99, backup_success_rate_pct: 0.99,
    change_failure_rate_pct: 0.02, deployment_frequency_per_week: 10.0,
    avg_response_time_ms: 120,
  },
  {
    system_id: "SYS-007", environment: "staging", region: "ap-northeast-1",
    system_risk: "moderate", system_pattern: "none",
    system_severity: "degraded", recommended_action: "health_monitoring",
    performance_score: 22.0, capacity_score: 18.0, security_score: 25.0, reliability_score: 24.0,
    system_composite: 22.3,
    has_system_alert: true, requires_immediate_action: true,
    estimated_downtime_risk_hours: 0.45,
    system_signal: "MODERATE — 63% CPU — 2% error rate — 97.8% uptime — 5 vulns — composite 22",
    cpu_utilization_pct: 0.63, memory_utilization_pct: 0.58, disk_utilization_pct: 0.52,
    network_latency_ms: 88, error_rate_pct: 0.02, uptime_pct: 0.978,
    incident_count_30d: 2, mean_time_to_recovery_hours: 2.0,
    security_vulnerability_count: 5, failed_security_scans: 1,
    patch_compliance_pct: 0.79, integration_failure_rate_pct: 0.04,
    api_error_rate_pct: 0.03, data_pipeline_lag_minutes: 12.0,
    sla_compliance_pct: 0.96, backup_success_rate_pct: 0.91,
    change_failure_rate_pct: 0.07, deployment_frequency_per_week: 6.0,
    avg_response_time_ms: 380,
  },
  {
    system_id: "SYS-008", environment: "production", region: "us-west-2",
    system_risk: "low", system_pattern: "none",
    system_severity: "nominal", recommended_action: "no_action",
    performance_score: 0.0, capacity_score: 8.0, security_score: 10.0, reliability_score: 6.0,
    system_composite: 5.9,
    has_system_alert: false, requires_immediate_action: false,
    estimated_downtime_risk_hours: 0.01,
    system_signal: "System health nominal — performance, capacity, security and reliability within operational thresholds",
    cpu_utilization_pct: 0.35, memory_utilization_pct: 0.30, disk_utilization_pct: 0.25,
    network_latency_ms: 28, error_rate_pct: 0.005, uptime_pct: 0.9997,
    incident_count_30d: 0, mean_time_to_recovery_hours: 0.25,
    security_vulnerability_count: 1, failed_security_scans: 0,
    patch_compliance_pct: 0.99, integration_failure_rate_pct: 0.005,
    api_error_rate_pct: 0.004, data_pipeline_lag_minutes: 1.0,
    sla_compliance_pct: 1.00, backup_success_rate_pct: 1.00,
    change_failure_rate_pct: 0.01, deployment_frequency_per_week: 14.0,
    avg_response_time_ms: 85,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/it-systems-health-monitoring-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let systems = [...mockSystems];
  if (risk)    systems = systems.filter((s) => s.system_risk === risk);
  if (pattern) systems = systems.filter((s) => s.system_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp  = 0, total_perf = 0, total_cap = 0, total_sec = 0,
      total_rel   = 0, total_dtr  = 0;

  for (const s of mockSystems) {
    risk_counts[s.system_risk]       = (risk_counts[s.system_risk] || 0) + 1;
    pattern_counts[s.system_pattern] = (pattern_counts[s.system_pattern] || 0) + 1;
    severity_counts[s.system_severity] = (severity_counts[s.system_severity] || 0) + 1;
    action_counts[s.recommended_action] = (action_counts[s.recommended_action] || 0) + 1;
    total_comp += s.system_composite;
    total_perf += s.performance_score;
    total_cap  += s.capacity_score;
    total_sec  += s.security_score;
    total_rel  += s.reliability_score;
    total_dtr  += s.estimated_downtime_risk_hours;
  }

  const n = mockSystems.length;

  return NextResponse.json({
    systems,
    summary: {
      total:                             n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_system_composite:              Math.round((total_comp / n) * 10) / 10,
      system_alert_count:                mockSystems.filter((s) => s.has_system_alert).length,
      immediate_action_count:            mockSystems.filter((s) => s.requires_immediate_action).length,
      avg_performance_score:             Math.round((total_perf / n) * 10) / 10,
      avg_capacity_score:                Math.round((total_cap / n) * 10) / 10,
      avg_security_score:                Math.round((total_sec / n) * 10) / 10,
      avg_reliability_score:             Math.round((total_rel / n) * 10) / 10,
      avg_estimated_downtime_risk_hours: Math.round((total_dtr / n) * 100) / 100,
    },
  });
}
