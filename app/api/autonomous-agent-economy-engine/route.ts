import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // AAE-001 — EMEA, knowledge_workers → critical, mass_displacement_crisis
  // labor_displacement_rate>=0.70 AND (1-human_reskilling_velocity)>=0.60 → mass_displacement_crisis
  // composite should be >=60 → critical
  {
    id: "AAE-001", agent_category: "knowledge_workers", region: "EMEA",
    agent_market_penetration: 0.85,
    labor_displacement_rate: 0.82,
    human_agent_collaboration_index: 0.20,
    agent_specialization_depth: 0.78,
    task_automation_coverage: 0.75,
    agent_governance_maturity: 0.25,
    economic_value_capture_by_agents: 0.70,
    human_reskilling_velocity: 0.22,
    agent_accountability_gap: 0.72,
    wage_floor_erosion: 0.68,
    agent_coordination_efficiency: 0.80,
    monopolization_risk: 0.65,
    agent_safety_compliance: 0.30,
    income_redistribution_mechanism: 0.20,
    agent_bias_prevalence: 0.60,
    sovereign_agent_dependency: 0.65,
    agent_ecosystem_diversity: 0.25,
  },
  // AAE-002 — APAC, creative_agents → low, agent_economy_thriving / none
  // composite < 20 → low; no pattern triggers
  {
    id: "AAE-002", agent_category: "creative_agents", region: "APAC",
    agent_market_penetration: 0.20,
    labor_displacement_rate: 0.10,
    human_agent_collaboration_index: 0.88,
    agent_specialization_depth: 0.40,
    task_automation_coverage: 0.12,
    agent_governance_maturity: 0.88,
    economic_value_capture_by_agents: 0.15,
    human_reskilling_velocity: 0.90,
    agent_accountability_gap: 0.10,
    wage_floor_erosion: 0.08,
    agent_coordination_efficiency: 0.85,
    monopolization_risk: 0.10,
    agent_safety_compliance: 0.92,
    income_redistribution_mechanism: 0.85,
    agent_bias_prevalence: 0.08,
    sovereign_agent_dependency: 0.10,
    agent_ecosystem_diversity: 0.90,
  },
  // AAE-003 — NOAM, service_robots → high, agent_monopoly
  // monopolization_risk>=0.70 AND economic_value_capture_by_agents>=0.65 → agent_monopoly
  // composite >=40 and <60 → high
  {
    id: "AAE-003", agent_category: "service_robots", region: "NOAM",
    agent_market_penetration: 0.65,
    labor_displacement_rate: 0.48,
    human_agent_collaboration_index: 0.42,
    agent_specialization_depth: 0.60,
    task_automation_coverage: 0.50,
    agent_governance_maturity: 0.45,
    economic_value_capture_by_agents: 0.75,
    human_reskilling_velocity: 0.50,
    agent_accountability_gap: 0.45,
    wage_floor_erosion: 0.40,
    agent_coordination_efficiency: 0.70,
    monopolization_risk: 0.78,
    agent_safety_compliance: 0.55,
    income_redistribution_mechanism: 0.45,
    agent_bias_prevalence: 0.38,
    sovereign_agent_dependency: 0.42,
    agent_ecosystem_diversity: 0.48,
  },
  // AAE-004 — LATAM, creative_agents → low, agent_economy_thriving / none
  // composite < 20 → low; no pattern triggers
  {
    id: "AAE-004", agent_category: "creative_agents", region: "LATAM",
    agent_market_penetration: 0.15,
    labor_displacement_rate: 0.08,
    human_agent_collaboration_index: 0.90,
    agent_specialization_depth: 0.35,
    task_automation_coverage: 0.10,
    agent_governance_maturity: 0.85,
    economic_value_capture_by_agents: 0.12,
    human_reskilling_velocity: 0.88,
    agent_accountability_gap: 0.12,
    wage_floor_erosion: 0.10,
    agent_coordination_efficiency: 0.80,
    monopolization_risk: 0.12,
    agent_safety_compliance: 0.90,
    income_redistribution_mechanism: 0.82,
    agent_bias_prevalence: 0.10,
    sovereign_agent_dependency: 0.12,
    agent_ecosystem_diversity: 0.88,
  },
  // AAE-005 — MEA, knowledge_workers → critical, governance_vacuum
  // (1-agent_governance_maturity)>=0.65 AND agent_accountability_gap>=0.60 → governance_vacuum
  // composite >=60 → critical
  {
    id: "AAE-005", agent_category: "knowledge_workers", region: "MEA",
    agent_market_penetration: 0.72,
    labor_displacement_rate: 0.60,
    human_agent_collaboration_index: 0.25,
    agent_specialization_depth: 0.65,
    task_automation_coverage: 0.68,
    agent_governance_maturity: 0.18,
    economic_value_capture_by_agents: 0.58,
    human_reskilling_velocity: 0.45,
    agent_accountability_gap: 0.72,
    wage_floor_erosion: 0.58,
    agent_coordination_efficiency: 0.55,
    monopolization_risk: 0.55,
    agent_safety_compliance: 0.32,
    income_redistribution_mechanism: 0.28,
    agent_bias_prevalence: 0.55,
    sovereign_agent_dependency: 0.62,
    agent_ecosystem_diversity: 0.28,
  },
  // AAE-006 — EMEA, logistics_bots → moderate, none
  // composite >=20 and <40 → moderate; no pattern triggers
  {
    id: "AAE-006", agent_category: "logistics_bots", region: "EMEA",
    agent_market_penetration: 0.42,
    labor_displacement_rate: 0.28,
    human_agent_collaboration_index: 0.60,
    agent_specialization_depth: 0.45,
    task_automation_coverage: 0.32,
    agent_governance_maturity: 0.58,
    economic_value_capture_by_agents: 0.35,
    human_reskilling_velocity: 0.62,
    agent_accountability_gap: 0.32,
    wage_floor_erosion: 0.28,
    agent_coordination_efficiency: 0.62,
    monopolization_risk: 0.30,
    agent_safety_compliance: 0.65,
    income_redistribution_mechanism: 0.55,
    agent_bias_prevalence: 0.28,
    sovereign_agent_dependency: 0.30,
    agent_ecosystem_diversity: 0.60,
  },
  // AAE-007 — APAC, service_robots → high, equity_collapse
  // (1-income_redistribution_mechanism)>=0.70 AND wage_floor_erosion>=0.65 → equity_collapse
  // composite >=40 and <60 → high
  {
    id: "AAE-007", agent_category: "service_robots", region: "APAC",
    agent_market_penetration: 0.58,
    labor_displacement_rate: 0.50,
    human_agent_collaboration_index: 0.38,
    agent_specialization_depth: 0.52,
    task_automation_coverage: 0.48,
    agent_governance_maturity: 0.48,
    economic_value_capture_by_agents: 0.52,
    human_reskilling_velocity: 0.48,
    agent_accountability_gap: 0.40,
    wage_floor_erosion: 0.72,
    agent_coordination_efficiency: 0.55,
    monopolization_risk: 0.48,
    agent_safety_compliance: 0.52,
    income_redistribution_mechanism: 0.22,
    agent_bias_prevalence: 0.40,
    sovereign_agent_dependency: 0.45,
    agent_ecosystem_diversity: 0.50,
  },
  // AAE-008 — NOAM, knowledge_workers → critical, safety_failure
  // agent_bias_prevalence>=0.65 AND (1-agent_safety_compliance)>=0.60 → safety_failure
  // composite >=60 → critical
  {
    id: "AAE-008", agent_category: "knowledge_workers", region: "NOAM",
    agent_market_penetration: 0.78,
    labor_displacement_rate: 0.62,
    human_agent_collaboration_index: 0.22,
    agent_specialization_depth: 0.70,
    task_automation_coverage: 0.65,
    agent_governance_maturity: 0.30,
    economic_value_capture_by_agents: 0.60,
    human_reskilling_velocity: 0.35,
    agent_accountability_gap: 0.58,
    wage_floor_erosion: 0.55,
    agent_coordination_efficiency: 0.60,
    monopolization_risk: 0.60,
    agent_safety_compliance: 0.28,
    income_redistribution_mechanism: 0.32,
    agent_bias_prevalence: 0.72,
    sovereign_agent_dependency: 0.60,
    agent_ecosystem_diversity: 0.30,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function displacementScore(e: Entity): number {
  const raw = (
    e.labor_displacement_rate * 0.4 +
    e.task_automation_coverage * 0.35 +
    e.wage_floor_erosion * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function governanceScore(e: Entity): number {
  const raw = (
    (1 - e.agent_governance_maturity) * 0.4 +
    e.agent_accountability_gap * 0.35 +
    (1 - e.agent_ecosystem_diversity) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function equityScore(e: Entity): number {
  const raw = (
    (1 - e.income_redistribution_mechanism) * 0.4 +
    e.monopolization_risk * 0.35 +
    (1 - e.human_reskilling_velocity) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function safetyScore(e: Entity): number {
  const raw = (
    e.agent_bias_prevalence * 0.4 +
    (1 - e.agent_safety_compliance) * 0.35 +
    e.sovereign_agent_dependency * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function agentComposite(disp: number, gov: number, eq: number, saf: number): number {
  return Math.round((disp * 0.30 + gov * 0.25 + eq * 0.25 + saf * 0.20) * 100) / 100;
}

function agentPattern(e: Entity): string {
  if (e.labor_displacement_rate >= 0.70 && (1 - e.human_reskilling_velocity) >= 0.60)
    return "mass_displacement_crisis";
  if (e.monopolization_risk >= 0.70 && e.economic_value_capture_by_agents >= 0.65)
    return "agent_monopoly";
  if ((1 - e.agent_governance_maturity) >= 0.65 && e.agent_accountability_gap >= 0.60)
    return "governance_vacuum";
  if ((1 - e.income_redistribution_mechanism) >= 0.70 && e.wage_floor_erosion >= 0.65)
    return "equity_collapse";
  if (e.agent_bias_prevalence >= 0.65 && (1 - e.agent_safety_compliance) >= 0.60)
    return "safety_failure";
  return "none";
}

function agentRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function agentSeverity(comp: number): string {
  if (comp >= 75) return "agent_economy_emergency";
  if (comp >= 50) return "high_disruption";
  if (comp >= 25) return "labor_stress";
  return "agent_economy_thriving";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "agent_economy_emergency_governance";
  if (risk === "high" && pattern === "mass_displacement_crisis") return "displacement_mitigation";
  if (risk === "high") return "agent_regulation";
  if (risk === "moderate") return "agent_monitoring";
  return "no_action";
}

function agentSignal(e: Entity, risk: string, comp: number): string {
  if (risk === "critical") {
    return `Critique — déplacement emplois ${Math.round(e.labor_displacement_rate * 100)}% — risque monopolisation ${Math.round(e.monopolization_risk * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — maturité gouvernance agents ${Math.round(e.agent_governance_maturity * 100)}% — redistribution revenus ${Math.round(e.income_redistribution_mechanism * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — couverture automatisation ${Math.round(e.task_automation_coverage * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Économie agents autonomes florissante — collaboration humain-agent optimale, gouvernance solide";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const disp = displacementScore(e);
      const gov  = governanceScore(e);
      const eq   = equityScore(e);
      const saf  = safetyScore(e);
      const comp = agentComposite(disp, gov, eq, saf);
      const pat  = agentPattern(e);
      const risk = agentRisk(comp);
      const sev  = agentSeverity(comp);
      const act  = recommendedAction(risk, pat);
      const sig  = agentSignal(e, risk, comp);
      return {
        id:                    e.entity_id,
        region:                       e.region,
        agent_category:               e.agent_category,
        agent_risk:                   risk,
        agent_pattern:                pat,
        agent_severity:               sev,
        recommended_action:           act,
        displacement_score:           disp,
        governance_score:             gov,
        equity_score:                 eq,
        safety_score:                 saf,
        agent_composite:              comp,
        is_in_agent_crisis:           comp >= 60,
        requires_agent_intervention:  comp >= 40,
        agent_signal:                 sig,
      };
    });

    const rc: Record<string,number> = {};
    const pc: Record<string,number> = {};
    const sc: Record<string,number> = {};
    const ac: Record<string,number> = {};
    let tDisp=0, tGov=0, tEq=0, tSaf=0, tComp=0, crisisC=0, interventionC=0;

    for (const ent of entities) {
      rc[ent.agent_risk]           = (rc[ent.agent_risk]           || 0) + 1;
      pc[ent.agent_pattern]        = (pc[ent.agent_pattern]        || 0) + 1;
      sc[ent.agent_severity]       = (sc[ent.agent_severity]       || 0) + 1;
      ac[ent.recommended_action]   = (ac[ent.recommended_action]   || 0) + 1;
      tDisp += ent.displacement_score;
      tGov  += ent.governance_score;
      tEq   += ent.equity_score;
      tSaf  += ent.safety_score;
      tComp += ent.agent_composite;
      if (ent.is_in_agent_crisis)          crisisC++;
      if (ent.requires_agent_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;
    const summary = {
      total:                               n,
      risk_counts:                         rc,
      pattern_counts:                      pc,
      severity_counts:                     sc,
      action_counts:                       ac,
      avg_agent_composite:                 avgComp,
      agent_crisis_count:                  crisisC,
      agent_intervention_count:            interventionC,
      avg_displacement_score:              Math.round(tDisp / n * 10) / 10,
      avg_governance_score:                Math.round(tGov  / n * 10) / 10,
      avg_equity_score:                    Math.round(tEq   / n * 10) / 10,
      avg_safety_score:                    Math.round(tSaf  / n * 10) / 10,
      avg_estimated_agent_disruption_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "autonomous-agent-economy-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/autonomous-agent-economy-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "autonomous-agent-economy-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream agent economy engine unavailable" }, "autonomous-agent-economy-engine"),
      { status: 502 }
    );
  }
}
