import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_SWARMS = [
  // SO-001 sales EMEA — critical deadlock
  { swarm_id:"SO-001", swarm_type:"sales",   region:"EMEA",  task_conflict_rate:0.38, resource_contention_score:0.70, goal_alignment_score:0.25, inter_agent_communication_latency_ms:420, message_failure_rate:0.28, agent_response_time_variance:45, deadlock_occurrence_count:3, cascade_failure_risk_score:0.72, coordination_overhead_pct:0.42, task_duplication_rate:0.28, role_overlap_score:0.62, priority_conflict_count:11, consensus_achievement_rate:0.32, autonomy_balance_score:0.30, workload_distribution_gini:0.58, human_escalation_rate:0.38, orchestration_efficiency_score:0.22 },
  // SO-002 ops NAMER — low harmonized
  { swarm_id:"SO-002", swarm_type:"ops",     region:"NAMER", task_conflict_rate:0.02, resource_contention_score:0.05, goal_alignment_score:0.95, inter_agent_communication_latency_ms:45,  message_failure_rate:0.01, agent_response_time_variance:4,  deadlock_occurrence_count:0, cascade_failure_risk_score:0.05, coordination_overhead_pct:0.05, task_duplication_rate:0.02, role_overlap_score:0.04, priority_conflict_count:0,  consensus_achievement_rate:0.97, autonomy_balance_score:0.95, workload_distribution_gini:0.08, human_escalation_rate:0.02, orchestration_efficiency_score:0.95 },
  // SO-003 finance APAC — high cascade_failure
  { swarm_id:"SO-003", swarm_type:"finance", region:"APAC",  task_conflict_rate:0.28, resource_contention_score:0.50, goal_alignment_score:0.52, inter_agent_communication_latency_ms:210, message_failure_rate:0.16, agent_response_time_variance:28, deadlock_occurrence_count:1, cascade_failure_risk_score:0.78, coordination_overhead_pct:0.30, task_duplication_rate:0.18, role_overlap_score:0.40, priority_conflict_count:6,  consensus_achievement_rate:0.58, autonomy_balance_score:0.50, workload_distribution_gini:0.38, human_escalation_rate:0.40, orchestration_efficiency_score:0.48 },
  // SO-004 product LATAM — low balanced
  { swarm_id:"SO-004", swarm_type:"product", region:"LATAM", task_conflict_rate:0.03, resource_contention_score:0.08, goal_alignment_score:0.90, inter_agent_communication_latency_ms:55,  message_failure_rate:0.02, agent_response_time_variance:5,  deadlock_occurrence_count:0, cascade_failure_risk_score:0.08, coordination_overhead_pct:0.06, task_duplication_rate:0.03, role_overlap_score:0.06, priority_conflict_count:1,  consensus_achievement_rate:0.94, autonomy_balance_score:0.92, workload_distribution_gini:0.10, human_escalation_rate:0.03, orchestration_efficiency_score:0.92 },
  // SO-005 support EMEA — critical cascade_failure
  { swarm_id:"SO-005", swarm_type:"support", region:"EMEA",  task_conflict_rate:0.35, resource_contention_score:0.65, goal_alignment_score:0.28, inter_agent_communication_latency_ms:380, message_failure_rate:0.24, agent_response_time_variance:52, deadlock_occurrence_count:2, cascade_failure_risk_score:0.82, coordination_overhead_pct:0.45, task_duplication_rate:0.30, role_overlap_score:0.68, priority_conflict_count:13, consensus_achievement_rate:0.30, autonomy_balance_score:0.25, workload_distribution_gini:0.65, human_escalation_rate:0.45, orchestration_efficiency_score:0.18 },
  // SO-006 sales NAMER — moderate goal_misalignment
  { swarm_id:"SO-006", swarm_type:"sales",   region:"NAMER", task_conflict_rate:0.18, resource_contention_score:0.38, goal_alignment_score:0.30, inter_agent_communication_latency_ms:140, message_failure_rate:0.07, agent_response_time_variance:15, deadlock_occurrence_count:0, cascade_failure_risk_score:0.22, coordination_overhead_pct:0.15, task_duplication_rate:0.10, role_overlap_score:0.28, priority_conflict_count:10, consensus_achievement_rate:0.55, autonomy_balance_score:0.62, workload_distribution_gini:0.30, human_escalation_rate:0.14, orchestration_efficiency_score:0.65 },
  // SO-007 ops APAC — high communication_breakdown
  { swarm_id:"SO-007", swarm_type:"ops",     region:"APAC",  task_conflict_rate:0.15, resource_contention_score:0.42, goal_alignment_score:0.60, inter_agent_communication_latency_ms:650, message_failure_rate:0.22, agent_response_time_variance:35, deadlock_occurrence_count:0, cascade_failure_risk_score:0.45, coordination_overhead_pct:0.38, task_duplication_rate:0.14, role_overlap_score:0.35, priority_conflict_count:5,  consensus_achievement_rate:0.62, autonomy_balance_score:0.55, workload_distribution_gini:0.40, human_escalation_rate:0.20, orchestration_efficiency_score:0.52 },
  // SO-008 finance MEA — critical resource_contention
  { swarm_id:"SO-008", swarm_type:"finance", region:"MEA",   task_conflict_rate:0.40, resource_contention_score:0.78, goal_alignment_score:0.42, inter_agent_communication_latency_ms:290, message_failure_rate:0.14, agent_response_time_variance:40, deadlock_occurrence_count:1, cascade_failure_risk_score:0.55, coordination_overhead_pct:0.35, task_duplication_rate:0.22, role_overlap_score:0.70, priority_conflict_count:12, consensus_achievement_rate:0.48, autonomy_balance_score:0.38, workload_distribution_gini:0.52, human_escalation_rate:0.28, orchestration_efficiency_score:0.32 },
];

type Swarm = typeof MOCK_SWARMS[0];

function conflictScore(i: Swarm): number {
  let s = 0;
  if      (i.task_conflict_rate >= 0.30) s += 40; else if (i.task_conflict_rate >= 0.15) s += 22; else if (i.task_conflict_rate >= 0.05) s += 8;
  if      (i.role_overlap_score >= 0.60) s += 35; else if (i.role_overlap_score >= 0.35) s += 18; else if (i.role_overlap_score >= 0.15) s += 6;
  if      (i.priority_conflict_count >= 10) s += 25; else if (i.priority_conflict_count >= 5) s += 12; else if (i.priority_conflict_count >= 2) s += 6;
  return Math.min(s, 100);
}
function coordinationScore(i: Swarm): number {
  let s = 0;
  if      (i.message_failure_rate >= 0.20) s += 40; else if (i.message_failure_rate >= 0.10) s += 22; else if (i.message_failure_rate >= 0.03) s += 8;
  if      (i.coordination_overhead_pct >= 0.40) s += 35; else if (i.coordination_overhead_pct >= 0.20) s += 18; else if (i.coordination_overhead_pct >= 0.08) s += 6;
  if      (i.consensus_achievement_rate <= 0.50) s += 25; else if (i.consensus_achievement_rate <= 0.70) s += 12;
  return Math.min(s, 100);
}
function efficiencyScore(i: Swarm): number {
  let s = 0;
  if      (i.task_duplication_rate >= 0.25) s += 40; else if (i.task_duplication_rate >= 0.12) s += 22; else if (i.task_duplication_rate >= 0.05) s += 8;
  if      (i.orchestration_efficiency_score <= 0.40) s += 35; else if (i.orchestration_efficiency_score <= 0.60) s += 18; else if (i.orchestration_efficiency_score <= 0.75) s += 6;
  if      (i.workload_distribution_gini >= 0.60) s += 25; else if (i.workload_distribution_gini >= 0.35) s += 12;
  return Math.min(s, 100);
}
function resilienceScore(i: Swarm): number {
  let s = 0;
  if      (i.deadlock_occurrence_count >= 3) s += 40; else if (i.deadlock_occurrence_count >= 1) s += 22;
  if      (i.cascade_failure_risk_score >= 0.60) s += 35; else if (i.cascade_failure_risk_score >= 0.35) s += 18; else if (i.cascade_failure_risk_score >= 0.15) s += 6;
  if      (i.human_escalation_rate >= 0.30) s += 25; else if (i.human_escalation_rate >= 0.15) s += 12;
  return Math.min(s, 100);
}
function composite(cf: number, co: number, ef: number, re: number): number {
  return Math.min(Math.round((cf * 0.30 + co * 0.25 + ef * 0.25 + re * 0.20) * 100) / 100, 100);
}
function conflictPattern(i: Swarm): string {
  if (i.deadlock_occurrence_count >= 2 || (i.message_failure_rate >= 0.20 && i.consensus_achievement_rate <= 0.40)) return "deadlock";
  if (i.cascade_failure_risk_score >= 0.65 || i.human_escalation_rate >= 0.35) return "cascade_failure";
  if (i.resource_contention_score >= 0.60 && i.task_conflict_rate >= 0.25)      return "resource_contention";
  if (i.goal_alignment_score <= 0.35 || i.priority_conflict_count >= 8)          return "goal_misalignment";
  if (i.message_failure_rate >= 0.18 || i.inter_agent_communication_latency_ms >= 500) return "communication_breakdown";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "degraded"; if (c >= 20) return "balanced"; return "harmonized"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "deadlock")        return "swarm_reset";
    if (p === "cascade_failure") return "emergency_reorchestration";
    return "emergency_reorchestration";
  }
  if (r === "high") {
    if (p === "deadlock")               return "deadlock_resolution";
    if (p === "cascade_failure")        return "cascade_isolation";
    if (p === "resource_contention")    return "task_redistribution";
    if (p === "goal_misalignment")      return "goal_realignment";
    if (p === "communication_breakdown") return "communication_protocol_update";
    return "coordination_monitoring";
  }
  if (r === "moderate") return "coordination_monitoring";
  return "no_action";
}
function signal(i: Swarm, pat: string, comp: number): string {
  if (comp < 20) return "Essaim bien orchestré — coordination fluide, aucun conflit, efficacité optimale";
  const labels: Record<string,string> = {
    resource_contention:"Contention ressources", goal_misalignment:"Désalignement objectifs",
    communication_breakdown:"Rupture communication", cascade_failure:"Défaillance en cascade", deadlock:"Situation de blocage",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — conflit ${Math.round(i.task_conflict_rate*100)}% — échec comm ${Math.round(i.message_failure_rate*100)}% — deadlocks ${i.deadlock_occurrence_count} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const swarms = MOCK_SWARMS.map(i => {
      const cf = conflictScore(i), co = coordinationScore(i), ef = efficiencyScore(i), re = resilienceScore(i);
      const comp = composite(cf, co, ef, re), pat = conflictPattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        swarm_id: i.swarm_id, region: i.region,
        orchestration_risk: r, conflict_pattern: pat, orchestration_severity: sev, recommended_action: act,
        conflict_score: cf, coordination_score: co, efficiency_score: ef, resilience_score: re,
        orchestration_composite: comp,
        has_orchestration_alert: comp >= 40 || i.deadlock_occurrence_count >= 1 || i.cascade_failure_risk_score >= 0.55 || i.task_conflict_rate >= 0.25,
        requires_human_intervention: comp >= 25 || i.deadlock_occurrence_count >= 2 || i.human_escalation_rate >= 0.25 || i.cascade_failure_risk_score >= 0.65,
        estimated_swarm_health_index: Math.min(Math.round((1 - comp/100) * i.orchestration_efficiency_score * 10 * 100) / 100, 10.0),
        orchestration_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tcf=0,tco=0,tef=0,tre=0,tcomp=0,thealth=0,alertC=0,humanC=0;
    for (const s of swarms) {
      rc[s.orchestration_risk]=(rc[s.orchestration_risk]||0)+1;
      pc[s.conflict_pattern]=(pc[s.conflict_pattern]||0)+1;
      sc[s.orchestration_severity]=(sc[s.orchestration_severity]||0)+1;
      ac[s.recommended_action]=(ac[s.recommended_action]||0)+1;
      tcf+=s.conflict_score; tco+=s.coordination_score; tef+=s.efficiency_score; tre+=s.resilience_score;
      tcomp+=s.orchestration_composite; thealth+=s.estimated_swarm_health_index;
      if (s.has_orchestration_alert) alertC++;
      if (s.requires_human_intervention) humanC++;
    }
    const n = swarms.length;
    return NextResponse.json(sealResponse({ swarms, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_orchestration_composite: Math.round(tcomp/n*10)/10,
      orchestration_alert_count: alertC, human_intervention_count: humanC,
      avg_conflict_score: Math.round(tcf/n*10)/10,
      avg_coordination_score: Math.round(tco/n*10)/10,
      avg_efficiency_score: Math.round(tef/n*10)/10,
      avg_resilience_score: Math.round(tre/n*10)/10,
      avg_estimated_swarm_health_index: Math.round(thealth/n*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/swarm-orchestration-conflict-engine`)).json());
}
