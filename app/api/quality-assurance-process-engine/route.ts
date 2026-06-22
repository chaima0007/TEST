import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[quality-assurance-process-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockProcesses = [
  {
    process_id: "QA-001", process_type: "manufacturing", region: "EMEA",
    quality_risk: "critical", quality_pattern: "defect_surge",
    quality_severity: "critical", recommended_action: "emergency_quality_lockdown",
    defect_score: 100, process_score: 44, compliance_score: 62, supplier_score: 27,
    quality_composite: 67.9, has_quality_alert: true,
    requires_immediate_action: true,
    estimated_quality_risk_index: 8.85,
    quality_signal: "Surge de défauts — défauts 18% — SLA 8% — audit 42% — composite 68",
  },
  {
    process_id: "QA-002", process_type: "software", region: "NAMER",
    quality_risk: "low", quality_pattern: "none",
    quality_severity: "excellent", recommended_action: "no_action",
    defect_score: 0, process_score: 0, compliance_score: 0, supplier_score: 0,
    quality_composite: 0.0, has_quality_alert: false,
    requires_immediate_action: false,
    estimated_quality_risk_index: 0.0,
    quality_signal: "Qualité excellente — aucun défaut significatif, conformité maintenue, fournisseurs fiables",
  },
  {
    process_id: "QA-003", process_type: "service", region: "APAC",
    quality_risk: "high", quality_pattern: "sla_breach",
    quality_severity: "degraded", recommended_action: "sla_remediation",
    defect_score: 22, process_score: 24, compliance_score: 59, supplier_score: 10,
    quality_composite: 29.55, has_quality_alert: true,
    requires_immediate_action: false,
    estimated_quality_risk_index: 1.42,
    quality_signal: "Violation SLA — défauts 8% — SLA 22% — audit 72% — composite 30",
  },
  {
    process_id: "QA-004", process_type: "delivery", region: "LATAM",
    quality_risk: "low", quality_pattern: "none",
    quality_severity: "excellent", recommended_action: "no_action",
    defect_score: 8, process_score: 0, compliance_score: 0, supplier_score: 10,
    quality_composite: 4.4, has_quality_alert: false,
    requires_immediate_action: false,
    estimated_quality_risk_index: 0.04,
    quality_signal: "Qualité excellente — aucun défaut significatif, conformité maintenue, fournisseurs fiables",
  },
  {
    process_id: "QA-005", process_type: "procurement", region: "EMEA",
    quality_risk: "critical", quality_pattern: "defect_surge",
    quality_severity: "critical", recommended_action: "emergency_quality_lockdown",
    defect_score: 75, process_score: 65, compliance_score: 90, supplier_score: 100,
    quality_composite: 81.25, has_quality_alert: true,
    requires_immediate_action: true,
    estimated_quality_risk_index: 8.12,
    quality_signal: "Surge de défauts — défauts 14% — SLA 9% — audit 45% — composite 81",
  },
  {
    process_id: "QA-006", process_type: "manufacturing", region: "NAMER",
    quality_risk: "moderate", quality_pattern: "process_deviation",
    quality_severity: "acceptable", recommended_action: "quality_monitoring",
    defect_score: 14, process_score: 57, compliance_score: 18, supplier_score: 16,
    quality_composite: 27.15, has_quality_alert: false,
    requires_immediate_action: false,
    estimated_quality_risk_index: 0.99,
    quality_signal: "Déviation processus — défauts 6% — SLA 5% — audit 78% — composite 27",
  },
  {
    process_id: "QA-007", process_type: "software", region: "APAC",
    quality_risk: "moderate", quality_pattern: "audit_failure",
    quality_severity: "acceptable", recommended_action: "quality_monitoring",
    defect_score: 8, process_score: 34, compliance_score: 75, supplier_score: 15,
    quality_composite: 34.25, has_quality_alert: true,
    requires_immediate_action: false,
    estimated_quality_risk_index: 1.58,
    quality_signal: "Échec audit — défauts 5% — SLA 14% — audit 38% — composite 34",
  },
  {
    process_id: "QA-008", process_type: "service", region: "MEA",
    quality_risk: "critical", quality_pattern: "defect_surge",
    quality_severity: "critical", recommended_action: "emergency_quality_lockdown",
    defect_score: 100, process_score: 90, compliance_score: 47, supplier_score: 75,
    quality_composite: 81.55, has_quality_alert: true,
    requires_immediate_action: true,
    estimated_quality_risk_index: 8.81,
    quality_signal: "Surge de défauts — défauts 20% — SLA 12% — audit 55% — composite 82",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/quality-assurance-process-engine`);
      if (risk)    url.searchParams.set("risk",    risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region",  region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let processes = [...mockProcesses];
  if (risk)    processes = processes.filter((p) => p.quality_risk === risk);
  if (pattern) processes = processes.filter((p) => p.quality_pattern === pattern);
  if (region)  processes = processes.filter((p) => p.region === region);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_def = 0, total_proc = 0, total_comp_s = 0,
      total_sup = 0, total_idx = 0;

  for (const p of mockProcesses) {
    risk_counts[p.quality_risk]         = (risk_counts[p.quality_risk] || 0) + 1;
    pattern_counts[p.quality_pattern]   = (pattern_counts[p.quality_pattern] || 0) + 1;
    severity_counts[p.quality_severity] = (severity_counts[p.quality_severity] || 0) + 1;
    action_counts[p.recommended_action] = (action_counts[p.recommended_action] || 0) + 1;
    total_comp   += p.quality_composite;
    total_def    += p.defect_score;
    total_proc   += p.process_score;
    total_comp_s += p.compliance_score;
    total_sup    += p.supplier_score;
    total_idx    += p.estimated_quality_risk_index;
  }

  const n = mockProcesses.length;

  return sealResponse(NextResponse.json({
    processes,
    summary: {
      total:                            n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_quality_composite:            Math.round((total_comp / n) * 10) / 10,
      quality_alert_count:              mockProcesses.filter((p) => p.has_quality_alert).length,
      immediate_action_count:           mockProcesses.filter((p) => p.requires_immediate_action).length,
      avg_defect_score:                 Math.round((total_def / n) * 10) / 10,
      avg_process_score:                Math.round((total_proc / n) * 10) / 10,
      avg_compliance_score:             Math.round((total_comp_s / n) * 10) / 10,
      avg_supplier_score:               Math.round((total_sup / n) * 10) / 10,
      avg_estimated_quality_risk_index: Math.round((total_idx / n) * 100) / 100,
    },
  }));
}
