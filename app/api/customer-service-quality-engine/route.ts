import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockTickets = [
  {
    ticket_id: "CS-001", region: "West",
    service_risk: "low", service_pattern: "none", service_severity: "excellent",
    recommended_action: "no_action",
    resolution_score: 8.0, escalation_score: 5.0, satisfaction_score: 6.0, capacity_score: 4.0,
    service_composite: 5.9, has_service_gap: false, requires_management_action: false,
    estimated_churn_risk_pct: 0.01,
    service_signal: "Service quality excellent — resolution, escalation, satisfaction and capacity within benchmarks",
    agent_id: "AGT-11",
    first_contact_resolution_pct: 0.88,
    customer_satisfaction_score: 0.91,
    sla_breach_rate_pct: 0.04,
    escalation_rate_pct: 0.05,
    agent_utilization_pct: 0.62,
  },
  {
    ticket_id: "CS-002", region: "East",
    service_risk: "moderate", service_pattern: "none", service_severity: "acceptable",
    recommended_action: "team_rebalancing",
    resolution_score: 22.0, escalation_score: 18.0, satisfaction_score: 10.0, capacity_score: 22.0,
    service_composite: 18.2, has_service_gap: false, requires_management_action: false,
    estimated_churn_risk_pct: 0.04,
    service_signal: "Moderate — 72% FCR — CSAT 79 — 10% SLA breach — composite 18",
    agent_id: "AGT-07",
    first_contact_resolution_pct: 0.72,
    customer_satisfaction_score: 0.79,
    sla_breach_rate_pct: 0.10,
    escalation_rate_pct: 0.11,
    agent_utilization_pct: 0.75,
  },
  {
    ticket_id: "CS-003", region: "Central",
    service_risk: "moderate", service_pattern: "resolution_failure", service_severity: "acceptable",
    recommended_action: "team_rebalancing",
    resolution_score: 40.0, escalation_score: 8.0, satisfaction_score: 25.0, capacity_score: 6.0,
    service_composite: 22.0, has_service_gap: false, requires_management_action: false,
    estimated_churn_risk_pct: 0.08,
    service_signal: "Moderate — 42% FCR — CSAT 72 — 12% SLA breach — composite 22",
    agent_id: "AGT-03",
    first_contact_resolution_pct: 0.42,
    customer_satisfaction_score: 0.72,
    sla_breach_rate_pct: 0.12,
    escalation_rate_pct: 0.09,
    agent_utilization_pct: 0.68,
  },
  {
    ticket_id: "CS-004", region: "Southeast",
    service_risk: "high", service_pattern: "sla_breach", service_severity: "degraded",
    recommended_action: "sla_recovery_plan",
    resolution_score: 37.0, escalation_score: 37.0, satisfaction_score: 25.0, capacity_score: 31.0,
    service_composite: 33.2, has_service_gap: true, requires_management_action: true,
    estimated_churn_risk_pct: 0.19,
    service_signal: "High — 58% FCR — CSAT 65 — 27% SLA breach — composite 33",
    agent_id: "AGT-14",
    first_contact_resolution_pct: 0.58,
    customer_satisfaction_score: 0.65,
    sla_breach_rate_pct: 0.27,
    escalation_rate_pct: 0.21,
    agent_utilization_pct: 0.82,
  },
  {
    ticket_id: "CS-005", region: "Northeast",
    service_risk: "high", service_pattern: "escalation_cascade", service_severity: "degraded",
    recommended_action: "escalation_process_review",
    resolution_score: 28.0, escalation_score: 75.0, satisfaction_score: 10.0, capacity_score: 18.0,
    service_composite: 35.7, has_service_gap: true, requires_management_action: true,
    estimated_churn_risk_pct: 0.22,
    service_signal: "High — 65% FCR — CSAT 78 — 32% SLA breach — composite 36",
    agent_id: "AGT-02",
    first_contact_resolution_pct: 0.65,
    customer_satisfaction_score: 0.78,
    sla_breach_rate_pct: 0.32,
    escalation_rate_pct: 0.38,
    agent_utilization_pct: 0.79,
  },
  {
    ticket_id: "CS-006", region: "Northwest",
    service_risk: "high", service_pattern: "agent_burnout", service_severity: "degraded",
    recommended_action: "agent_support_program",
    resolution_score: 22.0, escalation_score: 22.0, satisfaction_score: 45.0, capacity_score: 62.0,
    service_composite: 36.8, has_service_gap: true, requires_management_action: true,
    estimated_churn_risk_pct: 0.29,
    service_signal: "High — 70% FCR — CSAT 51 — 18% SLA breach — composite 37",
    agent_id: "AGT-09",
    first_contact_resolution_pct: 0.70,
    customer_satisfaction_score: 0.51,
    sla_breach_rate_pct: 0.18,
    escalation_rate_pct: 0.13,
    agent_utilization_pct: 0.92,
  },
  {
    ticket_id: "CS-007", region: "Southwest",
    service_risk: "critical", service_pattern: "satisfaction_collapse", service_severity: "failing",
    recommended_action: "executive_service_review",
    resolution_score: 75.0, escalation_score: 57.0, satisfaction_score: 75.0, capacity_score: 40.0,
    service_composite: 64.2, has_service_gap: true, requires_management_action: true,
    estimated_churn_risk_pct: 0.71,
    service_signal: "Critical — 38% FCR — CSAT 44 — 33% SLA breach — composite 64",
    agent_id: "AGT-06",
    first_contact_resolution_pct: 0.38,
    customer_satisfaction_score: 0.44,
    sla_breach_rate_pct: 0.33,
    escalation_rate_pct: 0.27,
    agent_utilization_pct: 0.87,
  },
  {
    ticket_id: "CS-008", region: "Central",
    service_risk: "critical", service_pattern: "escalation_cascade", service_severity: "failing",
    recommended_action: "executive_service_review",
    resolution_score: 100.0, escalation_score: 100.0, satisfaction_score: 100.0, capacity_score: 100.0,
    service_composite: 100.0, has_service_gap: true, requires_management_action: true,
    estimated_churn_risk_pct: 1.0,
    service_signal: "Critical — 25% FCR — CSAT 28 — 45% SLA breach — composite 100",
    agent_id: "AGT-01",
    first_contact_resolution_pct: 0.25,
    customer_satisfaction_score: 0.28,
    sla_breach_rate_pct: 0.45,
    escalation_rate_pct: 0.42,
    agent_utilization_pct: 0.97,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/customer-service-quality-engine`);
      if (risk)    url.searchParams.set("risk",    risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let items = [...mockTickets];
  if (risk)    items = items.filter((t) => t.service_risk    === risk);
  if (pattern) items = items.filter((t) => t.service_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_res = 0, total_esc = 0, total_sat = 0, total_cap = 0, total_churn = 0;

  for (const t of mockTickets) {
    risk_counts[t.service_risk]         = (risk_counts[t.service_risk] || 0) + 1;
    pattern_counts[t.service_pattern]   = (pattern_counts[t.service_pattern] || 0) + 1;
    severity_counts[t.service_severity] = (severity_counts[t.service_severity] || 0) + 1;
    action_counts[t.recommended_action] = (action_counts[t.recommended_action] || 0) + 1;
    total_comp  += t.service_composite;
    total_res   += t.resolution_score;
    total_esc   += t.escalation_score;
    total_sat   += t.satisfaction_score;
    total_cap   += t.capacity_score;
    total_churn += t.estimated_churn_risk_pct;
  }

  const n = mockTickets.length;

  return NextResponse.json({
    items,
    summary: {
      total:                        n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_service_composite:        Math.round((total_comp  / n) * 10) / 10,
      service_gap_count:            mockTickets.filter((t) => t.has_service_gap).length,
      management_action_count:      mockTickets.filter((t) => t.requires_management_action).length,
      avg_resolution_score:         Math.round((total_res   / n) * 10) / 10,
      avg_escalation_score:         Math.round((total_esc   / n) * 10) / 10,
      avg_satisfaction_score:       Math.round((total_sat   / n) * 10) / 10,
      avg_capacity_score:           Math.round((total_cap   / n) * 10) / 10,
      avg_estimated_churn_risk_pct: Math.round((total_churn / n) * 100) / 100,
    },
  });
}
