import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SR-001 company EMEA — critical governance_failure
  { id:"SR-001", entity_type:"company",    region:"EMEA",  strategic_goal_attainment:0.28, market_position_trend:-0.22, competitive_moat_score:0.35, board_effectiveness_score:0.18, executive_alignment_score:0.22, financial_health_score:0.25, esg_compliance_score:0.30, reputational_risk_score:0.82, regulatory_relationship_quality:0.28, strategic_initiative_completion_pct:0.25, stakeholder_trust_score:0.22, market_disruption_exposure:0.60, scenario_planning_maturity:0.22, risk_appetite_alignment_score:0.20, whistleblower_incident_count:5, cyber_resilience_score:0.28, succession_plan_completeness:0.20 },
  // SR-002 division NAMER — low sound
  { id:"SR-002", entity_type:"division",   region:"NAMER", strategic_goal_attainment:0.95, market_position_trend:0.25,  competitive_moat_score:0.90, board_effectiveness_score:0.92, executive_alignment_score:0.95, financial_health_score:0.94, esg_compliance_score:0.92, reputational_risk_score:0.08, regulatory_relationship_quality:0.95, strategic_initiative_completion_pct:0.95, stakeholder_trust_score:0.95, market_disruption_exposure:0.08, scenario_planning_maturity:0.92, risk_appetite_alignment_score:0.95, whistleblower_incident_count:0, cyber_resilience_score:0.92, succession_plan_completeness:0.90 },
  // SR-003 subsidiary APAC — high market_disruption
  { id:"SR-003", entity_type:"subsidiary", region:"APAC",  strategic_goal_attainment:0.55, market_position_trend:-0.35, competitive_moat_score:0.30, board_effectiveness_score:0.58, executive_alignment_score:0.60, financial_health_score:0.60, esg_compliance_score:0.62, reputational_risk_score:0.42, regulatory_relationship_quality:0.60, strategic_initiative_completion_pct:0.55, stakeholder_trust_score:0.58, market_disruption_exposure:0.78, scenario_planning_maturity:0.45, risk_appetite_alignment_score:0.50, whistleblower_incident_count:1, cyber_resilience_score:0.52, succession_plan_completeness:0.48 },
  // SR-004 jv LATAM — low monitored
  { id:"SR-004", entity_type:"jv",         region:"LATAM", strategic_goal_attainment:0.82, market_position_trend:0.12,  competitive_moat_score:0.78, board_effectiveness_score:0.85, executive_alignment_score:0.88, financial_health_score:0.88, esg_compliance_score:0.85, reputational_risk_score:0.12, regulatory_relationship_quality:0.88, strategic_initiative_completion_pct:0.82, stakeholder_trust_score:0.88, market_disruption_exposure:0.15, scenario_planning_maturity:0.82, risk_appetite_alignment_score:0.85, whistleblower_incident_count:0, cyber_resilience_score:0.85, succession_plan_completeness:0.80 },
  // SR-005 company EMEA — critical financial_exposure
  { id:"SR-005", entity_type:"company",    region:"EMEA",  strategic_goal_attainment:0.35, market_position_trend:-0.18, competitive_moat_score:0.28, board_effectiveness_score:0.42, executive_alignment_score:0.45, financial_health_score:0.12, esg_compliance_score:0.22, reputational_risk_score:0.78, regulatory_relationship_quality:0.32, strategic_initiative_completion_pct:0.32, stakeholder_trust_score:0.22, market_disruption_exposure:0.55, scenario_planning_maturity:0.28, risk_appetite_alignment_score:0.22, whistleblower_incident_count:4, cyber_resilience_score:0.30, succession_plan_completeness:0.25 },
  // SR-006 division NAMER — moderate strategic_drift
  { id:"SR-006", entity_type:"division",   region:"NAMER", strategic_goal_attainment:0.35, market_position_trend:-0.05, competitive_moat_score:0.60, board_effectiveness_score:0.62, executive_alignment_score:0.65, financial_health_score:0.72, esg_compliance_score:0.68, reputational_risk_score:0.28, regulatory_relationship_quality:0.70, strategic_initiative_completion_pct:0.32, stakeholder_trust_score:0.62, market_disruption_exposure:0.32, scenario_planning_maturity:0.60, risk_appetite_alignment_score:0.58, whistleblower_incident_count:0, cyber_resilience_score:0.65, succession_plan_completeness:0.60 },
  // SR-007 subsidiary APAC — high reputational_crisis
  { id:"SR-007", entity_type:"subsidiary", region:"APAC",  strategic_goal_attainment:0.58, market_position_trend:0.02,  competitive_moat_score:0.52, board_effectiveness_score:0.50, executive_alignment_score:0.55, financial_health_score:0.58, esg_compliance_score:0.38, reputational_risk_score:0.82, regulatory_relationship_quality:0.45, strategic_initiative_completion_pct:0.55, stakeholder_trust_score:0.25, market_disruption_exposure:0.40, scenario_planning_maturity:0.48, risk_appetite_alignment_score:0.45, whistleblower_incident_count:2, cyber_resilience_score:0.50, succession_plan_completeness:0.45 },
  // SR-008 jv MEA — critical market_disruption
  { id:"SR-008", entity_type:"jv",         region:"MEA",   strategic_goal_attainment:0.28, market_position_trend:-0.40, competitive_moat_score:0.18, board_effectiveness_score:0.48, executive_alignment_score:0.52, financial_health_score:0.30, esg_compliance_score:0.45, reputational_risk_score:0.55, regulatory_relationship_quality:0.40, strategic_initiative_completion_pct:0.28, stakeholder_trust_score:0.40, market_disruption_exposure:0.88, scenario_planning_maturity:0.30, risk_appetite_alignment_score:0.28, whistleblower_incident_count:1, cyber_resilience_score:0.35, succession_plan_completeness:0.28 },
];

type Entity = typeof MOCK_ENTITIES[0];

function strategicScore(i: Entity): number {
  let s = 0;
  if      (i.strategic_goal_attainment <= 0.40) s += 40; else if (i.strategic_goal_attainment <= 0.60) s += 22; else if (i.strategic_goal_attainment <= 0.75) s += 8;
  if      (i.market_position_trend <= -0.3) s += 35; else if (i.market_position_trend <= -0.1) s += 18; else if (i.market_position_trend <= 0) s += 6;
  if      (i.competitive_moat_score <= 0.30) s += 25; else if (i.competitive_moat_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function governanceScore(i: Entity): number {
  let s = 0;
  if      (i.board_effectiveness_score <= 0.40) s += 40; else if (i.board_effectiveness_score <= 0.60) s += 22; else if (i.board_effectiveness_score <= 0.75) s += 8;
  if      (i.executive_alignment_score <= 0.40) s += 35; else if (i.executive_alignment_score <= 0.60) s += 18; else if (i.executive_alignment_score <= 0.75) s += 6;
  if      (i.whistleblower_incident_count >= 5) s += 25; else if (i.whistleblower_incident_count >= 2) s += 12; else if (i.whistleblower_incident_count >= 1) s += 6;
  return Math.min(s, 100);
}
function financialRiskScore(i: Entity): number {
  let s = 0;
  if      (i.financial_health_score <= 0.30) s += 40; else if (i.financial_health_score <= 0.55) s += 22; else if (i.financial_health_score <= 0.75) s += 8;
  if      (i.esg_compliance_score <= 0.40) s += 35; else if (i.esg_compliance_score <= 0.60) s += 18; else if (i.esg_compliance_score <= 0.75) s += 6;
  if      (i.reputational_risk_score >= 0.70) s += 25; else if (i.reputational_risk_score >= 0.45) s += 12; else if (i.reputational_risk_score >= 0.25) s += 6;
  return Math.min(s, 100);
}
function resilienceScore(i: Entity): number {
  let s = 0;
  if      (i.scenario_planning_maturity <= 0.30) s += 40; else if (i.scenario_planning_maturity <= 0.55) s += 22; else if (i.scenario_planning_maturity <= 0.70) s += 8;
  if      (i.cyber_resilience_score <= 0.30) s += 35; else if (i.cyber_resilience_score <= 0.55) s += 18; else if (i.cyber_resilience_score <= 0.70) s += 6;
  if      (i.succession_plan_completeness <= 0.30) s += 25; else if (i.succession_plan_completeness <= 0.55) s += 12;
  return Math.min(s, 100);
}
function composite(st: number, gov: number, fin: number, res: number): number {
  return Math.min(Math.round((st * 0.30 + gov * 0.25 + fin * 0.25 + res * 0.20) * 100) / 100, 100);
}
function riskPattern(i: Entity): string {
  if (i.board_effectiveness_score <= 0.35 || i.executive_alignment_score <= 0.35 || i.whistleblower_incident_count >= 3) return "governance_failure";
  if (i.market_disruption_exposure >= 0.65 || i.market_position_trend <= -0.25) return "market_disruption";
  if (i.financial_health_score <= 0.35 || i.esg_compliance_score <= 0.35)       return "financial_exposure";
  if (i.reputational_risk_score >= 0.70 || i.stakeholder_trust_score <= 0.30)   return "reputational_crisis";
  if (i.strategic_goal_attainment <= 0.40 || i.strategic_initiative_completion_pct <= 0.35) return "strategic_drift";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "crisis"; if (c >= 40) return "exposed"; if (c >= 20) return "monitored"; return "sound"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "governance_failure")  return "emergency_governance";
    if (p === "reputational_crisis") return "reputational_intervention";
    if (p === "financial_exposure")  return "financial_restructuring";
    return "strategic_transformation";
  }
  if (r === "high") {
    if (p === "governance_failure")  return "board_alert";
    if (p === "market_disruption")   return "strategic_pivot";
    if (p === "financial_exposure")  return "governance_review";
    if (p === "strategic_drift")     return "board_alert";
    return "risk_monitoring";
  }
  if (r === "moderate") return "risk_monitoring";
  return "no_action";
}
function signal(i: Entity, pat: string, comp: number): string {
  if (comp < 20) return "Gouvernance solide — stratégie claire, finances saines, conseil efficace, risques maîtrisés";
  const labels: Record<string,string> = {
    market_disruption:"Disruption marché", governance_failure:"Défaillance gouvernance",
    reputational_crisis:"Crise réputationnelle", financial_exposure:"Exposition financière", strategic_drift:"Dérive stratégique",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — atteinte stratégique ${Math.round(i.strategic_goal_attainment*100)}% — santé financière ${Math.round(i.financial_health_score*100)}% — réputation ${Math.round(i.reputational_risk_score*100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(i => {
      const st = strategicScore(i), gov = governanceScore(i), fin = financialRiskScore(i), res = resilienceScore(i);
      const comp = composite(st, gov, fin, res), pat = riskPattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        id: i.entity_id, region: i.region,
        governance_risk: r, risk_pattern: pat, governance_severity: sev, recommended_action: act,
        strategic_score: st, governance_score: gov, financial_risk_score: fin, resilience_score: res,
        governance_composite: comp,
        has_governance_alert: comp >= 40 || i.board_effectiveness_score <= 0.40 || i.reputational_risk_score >= 0.65 || i.financial_health_score <= 0.40,
        requires_board_action: comp >= 25 || i.whistleblower_incident_count >= 2 || i.market_disruption_exposure >= 0.60 || i.strategic_goal_attainment <= 0.40,
        estimated_strategic_risk_index: Math.min(Math.round(comp/100*(1-i.risk_appetite_alignment_score+0.01)*10*100)/100, 10.0),
        governance_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tst=0,tgov=0,tfin=0,tres=0,tcomp=0,tridx=0,alertC=0,boardC=0;
    for (const e of entities) {
      rc[e.governance_risk]=(rc[e.governance_risk]||0)+1;
      pc[e.risk_pattern]=(pc[e.risk_pattern]||0)+1;
      sc[e.governance_severity]=(sc[e.governance_severity]||0)+1;
      ac[e.recommended_action]=(ac[e.recommended_action]||0)+1;
      tst+=e.strategic_score; tgov+=e.governance_score; tfin+=e.financial_risk_score; tres+=e.resilience_score;
      tcomp+=e.governance_composite; tridx+=e.estimated_strategic_risk_index;
      if (e.has_governance_alert) alertC++;
      if (e.requires_board_action) boardC++;
    }
    const n = entities.length;
    return NextResponse.json(sealResponse({ entities, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_governance_composite: Math.round(tcomp/n*10)/10,
      governance_alert_count: alertC, board_action_count: boardC,
      avg_strategic_score: Math.round(tst/n*10)/10,
      avg_governance_score: Math.round(tgov/n*10)/10,
      avg_financial_risk_score: Math.round(tfin/n*10)/10,
      avg_resilience_score: Math.round(tres/n*10)/10,
      avg_estimated_strategic_risk_index: Math.round(tridx/n*100)/100,
    } as Record<string, unknown>}, "strategic-risk-governance-engine") as Parameters<typeof NextResponse.json>[0]);
  }
  return NextResponse.json(sealResponse(await (await fetch(`${process.env.SWARM_API_URL}/strategic-risk-governance-engine`)).json(), "strategic-risk-governance-engine") as Parameters<typeof NextResponse.json>[0]);
}
