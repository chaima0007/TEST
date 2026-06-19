import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockResources = [
  {
    resource_id: "RC-001", resource_type: "human", region: "EMEA",
    resource_risk: "critical", capacity_pattern: "resource_overload",
    resource_severity: "critical", recommended_action: "emergency_redeployment",
    utilization_score: 100, allocation_score: 46, efficiency_score: 52, planning_score: 100,
    resource_composite: 74.5, has_capacity_alert: true, requires_strategic_review: true,
    estimated_capacity_gap_index: 6.03,
    resource_signal: "Surcharge ressources — util. 98% — gap compétences 70% — couverture pointe 25% — composite 74",
  },
  {
    resource_id: "RC-002", resource_type: "tech", region: "NAMER",
    resource_risk: "low", capacity_pattern: "none",
    resource_severity: "optimal", recommended_action: "no_action",
    utilization_score: 6, allocation_score: 6, efficiency_score: 0, planning_score: 0,
    resource_composite: 3.3, has_capacity_alert: false, requires_strategic_review: false,
    estimated_capacity_gap_index: 0.05,
    resource_signal: "Ressources optimales — capacité équilibrée, pas de surcharge détectée",
  },
  {
    resource_id: "RC-003", resource_type: "financial", region: "APAC",
    resource_risk: "high", capacity_pattern: "constraint_bottleneck",
    resource_severity: "strained", recommended_action: "constraint_resolution",
    utilization_score: 52, allocation_score: 14, efficiency_score: 87, planning_score: 38,
    resource_composite: 48.45, has_capacity_alert: true, requires_strategic_review: true,
    estimated_capacity_gap_index: 3.2,
    resource_signal: "Goulot d'étranglement — util. 88% — gap compétences 30% — couverture pointe 65% — composite 48",
  },
  {
    resource_id: "RC-004", resource_type: "physical", region: "LATAM",
    resource_risk: "low", capacity_pattern: "none",
    resource_severity: "optimal", recommended_action: "no_action",
    utilization_score: 0, allocation_score: 6, efficiency_score: 0, planning_score: 0,
    resource_composite: 1.5, has_capacity_alert: false, requires_strategic_review: false,
    estimated_capacity_gap_index: 0.02,
    resource_signal: "Ressources optimales — capacité équilibrée, pas de surcharge détectée",
  },
  {
    resource_id: "RC-005", resource_type: "human", region: "EMEA",
    resource_risk: "critical", capacity_pattern: "capacity_gap",
    resource_severity: "critical", recommended_action: "strategic_capacity_review",
    utilization_score: 68, allocation_score: 58, efficiency_score: 52, planning_score: 82,
    resource_composite: 64.3, has_capacity_alert: true, requires_strategic_review: true,
    estimated_capacity_gap_index: 4.89,
    resource_signal: "Écart de capacité — util. 91% — gap compétences 65% — couverture pointe 30% — composite 64",
  },
  {
    resource_id: "RC-006", resource_type: "tech", region: "NAMER",
    resource_risk: "moderate", capacity_pattern: "utilization_inefficiency",
    resource_severity: "balanced", recommended_action: "utilization_monitoring",
    utilization_score: 14, allocation_score: 39, efficiency_score: 39, planning_score: 28,
    resource_composite: 29.3, has_capacity_alert: false, requires_strategic_review: true,
    estimated_capacity_gap_index: 1.35,
    resource_signal: "Inefficacité d'utilisation — util. 72% — gap compétences 20% — couverture pointe 72% — composite 29",
  },
  {
    resource_id: "RC-007", resource_type: "human", region: "APAC",
    resource_risk: "moderate", capacity_pattern: "allocation_imbalance",
    resource_severity: "balanced", recommended_action: "utilization_monitoring",
    utilization_score: 38, allocation_score: 26, efficiency_score: 52, planning_score: 26,
    resource_composite: 36.1, has_capacity_alert: false, requires_strategic_review: true,
    estimated_capacity_gap_index: 2.2,
    resource_signal: "Déséquilibre d'allocation — util. 85% — gap compétences 30% — couverture pointe 70% — composite 36",
  },
  {
    resource_id: "RC-008", resource_type: "financial", region: "MEA",
    resource_risk: "critical", capacity_pattern: "resource_overload",
    resource_severity: "critical", recommended_action: "emergency_redeployment",
    utilization_score: 100, allocation_score: 40, efficiency_score: 52, planning_score: 100,
    resource_composite: 73.0, has_capacity_alert: true, requires_strategic_review: true,
    estimated_capacity_gap_index: 6.28,
    resource_signal: "Surcharge ressources — util. 96% — gap compétences 45% — couverture pointe 20% — composite 73",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/resource-optimization-capacity-engine`);
      if (risk)    url.searchParams.set("risk",    risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let resources = [...mockResources];
  if (risk)    resources = resources.filter((r) => r.resource_risk === risk);
  if (pattern) resources = resources.filter((r) => r.capacity_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_util = 0, total_alloc = 0, total_eff = 0,
      total_plan = 0, total_gap = 0;

  for (const r of mockResources) {
    risk_counts[r.resource_risk]         = (risk_counts[r.resource_risk] || 0) + 1;
    pattern_counts[r.capacity_pattern]   = (pattern_counts[r.capacity_pattern] || 0) + 1;
    severity_counts[r.resource_severity] = (severity_counts[r.resource_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.resource_composite;
    total_util  += r.utilization_score;
    total_alloc += r.allocation_score;
    total_eff   += r.efficiency_score;
    total_plan  += r.planning_score;
    total_gap   += r.estimated_capacity_gap_index;
  }

  const n = mockResources.length;

  return NextResponse.json(sealResponse({
    resources,
    summary: {
      total:                            n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_resource_composite:           Math.round((total_comp  / n) * 10) / 10,
      capacity_alert_count:             mockResources.filter((r) => r.has_capacity_alert).length,
      strategic_review_count:           mockResources.filter((r) => r.requires_strategic_review).length,
      avg_utilization_score:            Math.round((total_util  / n) * 10) / 10,
      avg_allocation_score:             Math.round((total_alloc / n) * 10) / 10,
      avg_efficiency_score:             Math.round((total_eff   / n) * 10) / 10,
      avg_planning_score:               Math.round((total_plan  / n) * 10) / 10,
      avg_estimated_capacity_gap_index: Math.round((total_gap   / n) * 100) / 100,
    },
  } as Record<string,unknown>));
}
