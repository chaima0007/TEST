import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_INITIATIVES = [
  // CI-001 ops EMEA — critical process_stagnation
  { initiative_id:"CI-001", business_unit:"ops",         region:"EMEA",  process_efficiency_trend:-0.30, waste_reduction_pct:0.05, cycle_time_improvement_pct:2,  rework_elimination_rate:0.10, innovation_idea_adoption_rate:0.20, kpi_attainment_rate:0.25, continuous_improvement_engagement_score:0.22, lean_methodology_adherence:0.15, change_adoption_velocity:0.18, retrospective_action_completion:0.25, cross_functional_collaboration_score:0.28, customer_feedback_integration_score:0.20, automation_adoption_rate:0.12, benchmark_performance_gap:0.72, employee_improvement_suggestion_rate:0.15, measurement_system_maturity:0.18, standardization_compliance_pct:0.22 },
  // CI-002 engineering NAMER — low excellent
  { initiative_id:"CI-002", business_unit:"engineering", region:"NAMER", process_efficiency_trend:0.40,  waste_reduction_pct:0.85, cycle_time_improvement_pct:35, rework_elimination_rate:0.90, innovation_idea_adoption_rate:0.82, kpi_attainment_rate:0.95, continuous_improvement_engagement_score:0.92, lean_methodology_adherence:0.92, change_adoption_velocity:0.88, retrospective_action_completion:0.95, cross_functional_collaboration_score:0.90, customer_feedback_integration_score:0.88, automation_adoption_rate:0.85, benchmark_performance_gap:0.08, employee_improvement_suggestion_rate:0.90, measurement_system_maturity:0.92, standardization_compliance_pct:0.95 },
  // CI-003 sales APAC — high innovation_deficit
  { initiative_id:"CI-003", business_unit:"sales",       region:"APAC",  process_efficiency_trend:0.02,  waste_reduction_pct:0.48, cycle_time_improvement_pct:8,  rework_elimination_rate:0.52, innovation_idea_adoption_rate:0.12, kpi_attainment_rate:0.70, continuous_improvement_engagement_score:0.55, lean_methodology_adherence:0.58, change_adoption_velocity:0.52, retrospective_action_completion:0.62, cross_functional_collaboration_score:0.58, customer_feedback_integration_score:0.50, automation_adoption_rate:0.15, benchmark_performance_gap:0.65, employee_improvement_suggestion_rate:0.38, measurement_system_maturity:0.55, standardization_compliance_pct:0.60 },
  // CI-004 finance LATAM — low progressing
  { initiative_id:"CI-004", business_unit:"finance",     region:"LATAM", process_efficiency_trend:0.25,  waste_reduction_pct:0.78, cycle_time_improvement_pct:22, rework_elimination_rate:0.80, innovation_idea_adoption_rate:0.68, kpi_attainment_rate:0.88, continuous_improvement_engagement_score:0.82, lean_methodology_adherence:0.80, change_adoption_velocity:0.78, retrospective_action_completion:0.85, cross_functional_collaboration_score:0.80, customer_feedback_integration_score:0.78, automation_adoption_rate:0.70, benchmark_performance_gap:0.12, employee_improvement_suggestion_rate:0.75, measurement_system_maturity:0.80, standardization_compliance_pct:0.88 },
  // CI-005 product EMEA — critical kpi_degradation
  { initiative_id:"CI-005", business_unit:"product",     region:"EMEA",  process_efficiency_trend:-0.20, waste_reduction_pct:0.30, cycle_time_improvement_pct:3,  rework_elimination_rate:0.28, innovation_idea_adoption_rate:0.35, kpi_attainment_rate:0.28, continuous_improvement_engagement_score:0.30, lean_methodology_adherence:0.32, change_adoption_velocity:0.20, retrospective_action_completion:0.22, cross_functional_collaboration_score:0.32, customer_feedback_integration_score:0.28, automation_adoption_rate:0.22, benchmark_performance_gap:0.68, employee_improvement_suggestion_rate:0.22, measurement_system_maturity:0.28, standardization_compliance_pct:0.30 },
  // CI-006 HR NAMER — moderate change_fatigue
  { initiative_id:"CI-006", business_unit:"HR",          region:"NAMER", process_efficiency_trend:0.05,  waste_reduction_pct:0.55, cycle_time_improvement_pct:10, rework_elimination_rate:0.58, innovation_idea_adoption_rate:0.48, kpi_attainment_rate:0.62, continuous_improvement_engagement_score:0.35, lean_methodology_adherence:0.60, change_adoption_velocity:0.22, retrospective_action_completion:0.55, cross_functional_collaboration_score:0.52, customer_feedback_integration_score:0.48, automation_adoption_rate:0.42, benchmark_performance_gap:0.38, employee_improvement_suggestion_rate:0.40, measurement_system_maturity:0.58, standardization_compliance_pct:0.62 },
  // CI-007 logistics APAC — high waste_accumulation
  { initiative_id:"CI-007", business_unit:"logistics",   region:"APAC",  process_efficiency_trend:-0.05, waste_reduction_pct:0.12, cycle_time_improvement_pct:5,  rework_elimination_rate:0.20, innovation_idea_adoption_rate:0.38, kpi_attainment_rate:0.65, continuous_improvement_engagement_score:0.55, lean_methodology_adherence:0.50, change_adoption_velocity:0.55, retrospective_action_completion:0.60, cross_functional_collaboration_score:0.50, customer_feedback_integration_score:0.45, automation_adoption_rate:0.35, benchmark_performance_gap:0.55, employee_improvement_suggestion_rate:0.42, measurement_system_maturity:0.50, standardization_compliance_pct:0.55 },
  // CI-008 marketing MEA — critical innovation_deficit
  { initiative_id:"CI-008", business_unit:"marketing",   region:"MEA",   process_efficiency_trend:-0.15, waste_reduction_pct:0.22, cycle_time_improvement_pct:2,  rework_elimination_rate:0.28, innovation_idea_adoption_rate:0.08, kpi_attainment_rate:0.40, continuous_improvement_engagement_score:0.28, lean_methodology_adherence:0.12, change_adoption_velocity:0.18, retrospective_action_completion:0.30, cross_functional_collaboration_score:0.25, customer_feedback_integration_score:0.22, automation_adoption_rate:0.10, benchmark_performance_gap:0.78, employee_improvement_suggestion_rate:0.15, measurement_system_maturity:0.15, standardization_compliance_pct:0.20 },
];

type Initiative = typeof MOCK_INITIATIVES[0];

function processScore(i: Initiative): number {
  let s = 0;
  if      (i.process_efficiency_trend <= -0.1) s += 40; else if (i.process_efficiency_trend <= 0) s += 22; else if (i.process_efficiency_trend <= 0.1) s += 8;
  if      (i.waste_reduction_pct <= 0.20) s += 35; else if (i.waste_reduction_pct <= 0.40) s += 18; else if (i.waste_reduction_pct <= 0.60) s += 6;
  if      (i.rework_elimination_rate <= 0.30) s += 25; else if (i.rework_elimination_rate <= 0.55) s += 12;
  return Math.min(s, 100);
}
function innovationScore(i: Initiative): number {
  let s = 0;
  if      (i.innovation_idea_adoption_rate <= 0.20) s += 40; else if (i.innovation_idea_adoption_rate <= 0.40) s += 22; else if (i.innovation_idea_adoption_rate <= 0.60) s += 8;
  if      (i.automation_adoption_rate <= 0.20) s += 35; else if (i.automation_adoption_rate <= 0.40) s += 18; else if (i.automation_adoption_rate <= 0.60) s += 6;
  if      (i.benchmark_performance_gap >= 0.55) s += 25; else if (i.benchmark_performance_gap >= 0.35) s += 12;
  return Math.min(s, 100);
}
function executionScore(i: Initiative): number {
  let s = 0;
  if      (i.retrospective_action_completion <= 0.40) s += 40; else if (i.retrospective_action_completion <= 0.60) s += 22; else if (i.retrospective_action_completion <= 0.75) s += 8;
  if      (i.kpi_attainment_rate <= 0.50) s += 35; else if (i.kpi_attainment_rate <= 0.65) s += 18; else if (i.kpi_attainment_rate <= 0.80) s += 6;
  if      (i.change_adoption_velocity <= 0.30) s += 25; else if (i.change_adoption_velocity <= 0.50) s += 12;
  return Math.min(s, 100);
}
function maturityScore(i: Initiative): number {
  let s = 0;
  if      (i.lean_methodology_adherence <= 0.30) s += 40; else if (i.lean_methodology_adherence <= 0.55) s += 22; else if (i.lean_methodology_adherence <= 0.70) s += 8;
  if      (i.measurement_system_maturity <= 0.30) s += 35; else if (i.measurement_system_maturity <= 0.55) s += 18; else if (i.measurement_system_maturity <= 0.70) s += 6;
  if      (i.standardization_compliance_pct <= 0.50) s += 25; else if (i.standardization_compliance_pct <= 0.70) s += 12;
  return Math.min(s, 100);
}
function composite(pr: number, inn: number, ex: number, mat: number): number {
  return Math.min(Math.round((pr * 0.30 + inn * 0.25 + ex * 0.25 + mat * 0.20) * 100) / 100, 100);
}
function improvementPattern(i: Initiative): string {
  if (i.process_efficiency_trend <= 0 && i.waste_reduction_pct <= 0.30) return "process_stagnation";
  if (i.rework_elimination_rate <= 0.25 || i.waste_reduction_pct <= 0.20) return "waste_accumulation";
  if (i.innovation_idea_adoption_rate <= 0.25 && i.automation_adoption_rate <= 0.25) return "innovation_deficit";
  if (i.kpi_attainment_rate <= 0.50 || i.retrospective_action_completion <= 0.35) return "kpi_degradation";
  if (i.change_adoption_velocity <= 0.25 && i.continuous_improvement_engagement_score <= 0.40) return "change_fatigue";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "declining"; if (c >= 40) return "stagnating"; if (c >= 20) return "progressing"; return "excellent"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "process_stagnation") return "transformation_program";
    if (p === "kpi_degradation")    return "process_reengineering";
    return "change_management";
  }
  if (r === "high") {
    if (p === "process_stagnation") return "process_reengineering";
    if (p === "waste_accumulation") return "lean_review";
    if (p === "innovation_deficit") return "innovation_sprint";
    if (p === "kpi_degradation")    return "kpi_reset";
    if (p === "change_fatigue")     return "change_management";
    return "kaizen_initiative";
  }
  if (r === "moderate") return "improvement_monitoring";
  return "no_action";
}
function signal(i: Initiative, pat: string, comp: number): string {
  if (comp < 20) return "Excellence opérationnelle forte — amélioration continue active, KPIs atteints, innovation en cours";
  const labels: Record<string,string> = {
    process_stagnation:"Stagnation process", waste_accumulation:"Accumulation déchets",
    innovation_deficit:"Déficit innovation", kpi_degradation:"Dégradation KPIs", change_fatigue:"Fatigue du changement",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  const sign = i.process_efficiency_trend >= 0 ? "+" : "";
  return `${label} — trend process ${sign}${i.process_efficiency_trend.toFixed(2)} — KPIs ${Math.round(i.kpi_attainment_rate*100)}% — adoption inn. ${Math.round(i.innovation_idea_adoption_rate*100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[continuous-improvement-excellence-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tpr=0,tinn=0,tex=0,tmat=0,tcomp=0,tgap=0,stagC=0,transfC=0;
    for (const init of initiatives) {
      rc[init.improvement_risk]=(rc[init.improvement_risk]||0)+1;
      pc[init.improvement_pattern]=(pc[init.improvement_pattern]||0)+1;
      sc[init.improvement_severity]=(sc[init.improvement_severity]||0)+1;
      ac[init.recommended_action]=(ac[init.recommended_action]||0)+1;
      tpr+=init.process_score; tinn+=init.innovation_score; tex+=init.execution_score; tmat+=init.maturity_score;
      tcomp+=init.improvement_composite; tgap+=init.estimated_improvement_gap_index;
      if (init.has_stagnation_signal) stagC++;
      if (init.requires_transformation) transfC++;
    }
    const n = initiatives.length;
    return sealResponse(NextResponse.json(sealResponse({ initiatives, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_improvement_composite: Math.round(tcomp/n*10)/10,
      stagnation_signal_count: stagC, transformation_required_count: transfC,
      avg_process_score: Math.round(tpr/n*10)/10,
      avg_innovation_score: Math.round(tinn/n*10)/10,
      avg_execution_score: Math.round(tex/n*10)/10,
      avg_maturity_score: Math.round(tmat/n*10)/10,
      avg_estimated_improvement_gap_index: Math.round(tgap/n*100)/100,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/continuous-improvement-excellence-engine`, { next: { revalidate: 30 } })).json()));
}
