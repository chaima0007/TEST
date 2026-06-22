import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[knowledge-gap-skills-analysis-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockEmployees = [
  {
    employee_id: "KG-001", region: "North America",
    skill_risk: "low", skill_pattern: "none", skill_severity: "proficient",
    recommended_action: "no_action",
    competency_score: 8.0, market_alignment_score: 6.0, leadership_score: 10.0, digital_score: 8.0,
    skill_composite: 8.05, has_skill_gap: false, requires_intervention: false,
    estimated_performance_impact: 0.08,
    skill_signal: "Skills profile strong — competency, market alignment, leadership and digital literacy meeting benchmarks",
  },
  {
    employee_id: "KG-002", region: "EMEA",
    skill_risk: "moderate", skill_pattern: "digital_literacy_gap", skill_severity: "developing",
    recommended_action: "mentoring_program",
    competency_score: 22.0, market_alignment_score: 18.0, leadership_score: 25.0, digital_score: 37.0,
    skill_composite: 24.85, has_skill_gap: false, requires_intervention: true,
    estimated_performance_impact: 2.24,
    skill_signal: "Moderate — 62% core proficiency — 58% market aligned — digital 45% — composite 25",
  },
  {
    employee_id: "KG-003", region: "APAC",
    skill_risk: "moderate", skill_pattern: "none", skill_severity: "developing",
    recommended_action: "mentoring_program",
    competency_score: 28.0, market_alignment_score: 20.0, leadership_score: 22.0, digital_score: 20.0,
    skill_composite: 22.9, has_skill_gap: false, requires_intervention: true,
    estimated_performance_impact: 2.52,
    skill_signal: "Moderate — 58% core proficiency — 65% market aligned — digital 52% — composite 23",
  },
  {
    employee_id: "KG-004", region: "LATAM",
    skill_risk: "high", skill_pattern: "market_mismatch", skill_severity: "gap",
    recommended_action: "reskilling_initiative",
    competency_score: 44.0, market_alignment_score: 62.0, leadership_score: 30.0, digital_score: 38.0,
    skill_composite: 43.7, has_skill_gap: true, requires_intervention: true,
    estimated_performance_impact: 5.24,
    skill_signal: "High — 48% core proficiency — 38% market aligned — digital 55% — composite 44",
  },
  {
    employee_id: "KG-005", region: "North America",
    skill_risk: "high", skill_pattern: "leadership_void", skill_severity: "gap",
    recommended_action: "leadership_development",
    competency_score: 38.0, market_alignment_score: 28.0, leadership_score: 75.0, digital_score: 30.0,
    skill_composite: 44.05, has_skill_gap: true, requires_intervention: true,
    estimated_performance_impact: 4.85,
    skill_signal: "High — 55% core proficiency — 60% market aligned — digital 60% — composite 44",
  },
  {
    employee_id: "KG-006", region: "EMEA",
    skill_risk: "high", skill_pattern: "obsolescence_risk", skill_severity: "gap",
    recommended_action: "digital_upskilling",
    competency_score: 30.0, market_alignment_score: 40.0, leadership_score: 38.0, digital_score: 70.0,
    skill_composite: 42.5, has_skill_gap: true, requires_intervention: true,
    estimated_performance_impact: 5.1,
    skill_signal: "High — 60% core proficiency — 55% market aligned — digital 38% — composite 43",
  },
  {
    employee_id: "KG-007", region: "APAC",
    skill_risk: "critical", skill_pattern: "critical_skill_gap", skill_severity: "critical",
    recommended_action: "emergency_capability_build",
    competency_score: 82.0, market_alignment_score: 62.0, leadership_score: 55.0, digital_score: 58.0,
    skill_composite: 65.05, has_skill_gap: true, requires_intervention: true,
    estimated_performance_impact: 7.81,
    skill_signal: "Critical — 38% core proficiency — 40% market aligned — digital 30% — composite 65",
  },
  {
    employee_id: "KG-008", region: "LATAM",
    skill_risk: "critical", skill_pattern: "market_mismatch", skill_severity: "critical",
    recommended_action: "emergency_capability_build",
    competency_score: 78.0, market_alignment_score: 80.0, leadership_score: 48.0, digital_score: 52.0,
    skill_composite: 64.9, has_skill_gap: true, requires_intervention: true,
    estimated_performance_impact: 8.44,
    skill_signal: "Critical — 35% core proficiency — 35% market aligned — digital 40% — composite 65",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk     = searchParams.get("risk");
  const pattern  = searchParams.get("pattern");
  const severity = searchParams.get("severity");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/knowledge-gap-skills-analysis-engine`);
      if (risk)     url.searchParams.set("risk",     risk);
      if (pattern)  url.searchParams.set("pattern",  pattern);
      if (severity) url.searchParams.set("severity", severity);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let employees = [...mockEmployees];
  if (risk)     employees = employees.filter((e) => e.skill_risk === risk);
  if (pattern)  employees = employees.filter((e) => e.skill_pattern === pattern);
  if (severity) employees = employees.filter((e) => e.skill_severity === severity);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_competency = 0, total_market = 0, total_leadership = 0, total_digital = 0, total_impact = 0;

  for (const e of mockEmployees) {
    risk_counts[e.skill_risk]           = (risk_counts[e.skill_risk] || 0) + 1;
    pattern_counts[e.skill_pattern]     = (pattern_counts[e.skill_pattern] || 0) + 1;
    severity_counts[e.skill_severity]   = (severity_counts[e.skill_severity] || 0) + 1;
    action_counts[e.recommended_action] = (action_counts[e.recommended_action] || 0) + 1;
    total_comp       += e.skill_composite;
    total_competency += e.competency_score;
    total_market     += e.market_alignment_score;
    total_leadership += e.leadership_score;
    total_digital    += e.digital_score;
    total_impact     += e.estimated_performance_impact;
  }

  const n = mockEmployees.length;

  return sealResponse(NextResponse.json(sealResponse({
    employees,
    summary: {
      total:                            n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_skill_composite:              Math.round((total_comp / n) * 100) / 100,
      skill_gap_count:                  mockEmployees.filter((e) => e.has_skill_gap).length,
      intervention_count:               mockEmployees.filter((e) => e.requires_intervention).length,
      avg_competency_score:             Math.round((total_competency / n) * 100) / 100,
      avg_market_alignment_score:       Math.round((total_market / n) * 100) / 100,
      avg_leadership_score:             Math.round((total_leadership / n) * 100) / 100,
      avg_digital_score:                Math.round((total_digital / n) * 100) / 100,
      avg_estimated_performance_impact: Math.round((total_impact / n) * 100) / 100,
    },
  } as Record<string,unknown>)));
}
