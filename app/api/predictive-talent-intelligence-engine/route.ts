import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_TALENTS = [
  // PTI-001 emerging_leader EMEA — critical, talent_obsolescence
  {
    talent_id: "PTI-001", talent_segment: "emerging_leader", region: "EMEA",
    skill_half_life_risk: 0.82, learning_velocity_score: 0.18, potential_trajectory_score: 0.25,
    flight_risk_index: 0.45, human_capital_value_score: 0.38, adaptability_coefficient: 0.22,
    knowledge_transfer_depth: 0.42, mentorship_multiplier_score: 0.38, strategic_indispensability_score: 0.35,
    skills_future_alignment: 0.18, innovation_contribution_rate: 0.28, retention_investment_roi: 0.55,
    succession_pipeline_readiness: 0.42, cultural_influence_score: 0.50, cross_domain_synthesis_ability: 0.20,
    resilience_under_pressure: 0.30, talent_ecosystem_connectivity: 0.28,
  },
  // PTI-002 deep_specialist NAMER — low, thriving (none)
  {
    talent_id: "PTI-002", talent_segment: "deep_specialist", region: "NAMER",
    skill_half_life_risk: 0.12, learning_velocity_score: 0.92, potential_trajectory_score: 0.90,
    flight_risk_index: 0.08, human_capital_value_score: 0.95, adaptability_coefficient: 0.88,
    knowledge_transfer_depth: 0.90, mentorship_multiplier_score: 0.88, strategic_indispensability_score: 0.92,
    skills_future_alignment: 0.90, innovation_contribution_rate: 0.88, retention_investment_roi: 0.92,
    succession_pipeline_readiness: 0.90, cultural_influence_score: 0.88, cross_domain_synthesis_ability: 0.85,
    resilience_under_pressure: 0.92, talent_ecosystem_connectivity: 0.90,
  },
  // PTI-003 cross_functional_connector APAC — high, flight_risk_crisis
  {
    talent_id: "PTI-003", talent_segment: "cross_functional_connector", region: "APAC",
    skill_half_life_risk: 0.38, learning_velocity_score: 0.62, potential_trajectory_score: 0.58,
    flight_risk_index: 0.78, human_capital_value_score: 0.65, adaptability_coefficient: 0.60,
    knowledge_transfer_depth: 0.55, mentorship_multiplier_score: 0.50, strategic_indispensability_score: 0.60,
    skills_future_alignment: 0.55, innovation_contribution_rate: 0.58, retention_investment_roi: 0.22,
    succession_pipeline_readiness: 0.55, cultural_influence_score: 0.40, cross_domain_synthesis_ability: 0.62,
    resilience_under_pressure: 0.55, talent_ecosystem_connectivity: 0.60,
  },
  // PTI-004 cultural_guardian LATAM — low, developing (none)
  {
    talent_id: "PTI-004", talent_segment: "cultural_guardian", region: "LATAM",
    skill_half_life_risk: 0.20, learning_velocity_score: 0.78, potential_trajectory_score: 0.75,
    flight_risk_index: 0.15, human_capital_value_score: 0.82, adaptability_coefficient: 0.80,
    knowledge_transfer_depth: 0.78, mentorship_multiplier_score: 0.80, strategic_indispensability_score: 0.78,
    skills_future_alignment: 0.80, innovation_contribution_rate: 0.72, retention_investment_roi: 0.85,
    succession_pipeline_readiness: 0.78, cultural_influence_score: 0.88, cross_domain_synthesis_ability: 0.72,
    resilience_under_pressure: 0.80, talent_ecosystem_connectivity: 0.75,
  },
  // PTI-005 technical_architect MEA — critical, knowledge_drain
  {
    talent_id: "PTI-005", talent_segment: "technical_architect", region: "MEA",
    skill_half_life_risk: 0.62, learning_velocity_score: 0.28, potential_trajectory_score: 0.42,
    flight_risk_index: 0.55, human_capital_value_score: 0.30, adaptability_coefficient: 0.32,
    knowledge_transfer_depth: 0.18, mentorship_multiplier_score: 0.20, strategic_indispensability_score: 0.38,
    skills_future_alignment: 0.28, innovation_contribution_rate: 0.25, retention_investment_roi: 0.48,
    succession_pipeline_readiness: 0.35, cultural_influence_score: 0.42, cross_domain_synthesis_ability: 0.28,
    resilience_under_pressure: 0.35, talent_ecosystem_connectivity: 0.22,
  },
  // PTI-006 innovation_scout NAMER — moderate, none
  {
    talent_id: "PTI-006", talent_segment: "innovation_scout", region: "NAMER",
    skill_half_life_risk: 0.35, learning_velocity_score: 0.60, potential_trajectory_score: 0.58,
    flight_risk_index: 0.38, human_capital_value_score: 0.62, adaptability_coefficient: 0.60,
    knowledge_transfer_depth: 0.55, mentorship_multiplier_score: 0.58, strategic_indispensability_score: 0.60,
    skills_future_alignment: 0.62, innovation_contribution_rate: 0.65, retention_investment_roi: 0.60,
    succession_pipeline_readiness: 0.55, cultural_influence_score: 0.58, cross_domain_synthesis_ability: 0.62,
    resilience_under_pressure: 0.60, talent_ecosystem_connectivity: 0.58,
  },
  // PTI-007 succession_candidate EMEA — high, succession_gap
  {
    talent_id: "PTI-007", talent_segment: "succession_candidate", region: "EMEA",
    skill_half_life_risk: 0.48, learning_velocity_score: 0.42, potential_trajectory_score: 0.32,
    flight_risk_index: 0.52, human_capital_value_score: 0.50, adaptability_coefficient: 0.48,
    knowledge_transfer_depth: 0.50, mentorship_multiplier_score: 0.55, strategic_indispensability_score: 0.50,
    skills_future_alignment: 0.48, innovation_contribution_rate: 0.45, retention_investment_roi: 0.50,
    succession_pipeline_readiness: 0.22, cultural_influence_score: 0.50, cross_domain_synthesis_ability: 0.42,
    resilience_under_pressure: 0.48, talent_ecosystem_connectivity: 0.45,
  },
  // PTI-008 creative_catalyst APAC — critical, potential_stagnation
  {
    talent_id: "PTI-008", talent_segment: "creative_catalyst", region: "APAC",
    skill_half_life_risk: 0.70, learning_velocity_score: 0.22, potential_trajectory_score: 0.20,
    flight_risk_index: 0.60, human_capital_value_score: 0.28, adaptability_coefficient: 0.28,
    knowledge_transfer_depth: 0.38, mentorship_multiplier_score: 0.35, strategic_indispensability_score: 0.28,
    skills_future_alignment: 0.25, innovation_contribution_rate: 0.22, retention_investment_roi: 0.40,
    succession_pipeline_readiness: 0.38, cultural_influence_score: 0.35, cross_domain_synthesis_ability: 0.20,
    resilience_under_pressure: 0.22, talent_ecosystem_connectivity: 0.25,
  },
];

type Talent = typeof MOCK_TALENTS[0];

function obsolescenceScore(t: Talent): number {
  return Math.min(
    t.skill_half_life_risk * 0.40 + (1 - t.skills_future_alignment) * 0.35 + (1 - t.adaptability_coefficient) * 0.25,
    1.0,
  );
}

function flightScore(t: Talent): number {
  return Math.min(
    t.flight_risk_index * 0.45 + (1 - t.retention_investment_roi) * 0.30 + (1 - t.cultural_influence_score) * 0.25,
    1.0,
  );
}

function valueScore(t: Talent): number {
  return Math.min(
    (1 - t.human_capital_value_score) * 0.40 + (1 - t.strategic_indispensability_score) * 0.35 + (1 - t.innovation_contribution_rate) * 0.25,
    1.0,
  );
}

function successionScore(t: Talent): number {
  return Math.min(
    (1 - t.succession_pipeline_readiness) * 0.40 + (1 - t.knowledge_transfer_depth) * 0.35 + (1 - t.mentorship_multiplier_score) * 0.25,
    1.0,
  );
}

function composite(obs: number, flt: number, val: number, suc: number): number {
  return Math.min(Math.round((obs * 0.30 + flt * 0.25 + val * 0.25 + suc * 0.20) * 100 * 100) / 100, 100);
}

function talentPattern(t: Talent): string {
  if (t.skill_half_life_risk >= 0.70 && t.skills_future_alignment <= 0.35) return "talent_obsolescence";
  if (t.flight_risk_index >= 0.68 && t.retention_investment_roi <= 0.38)   return "flight_risk_crisis";
  if (t.knowledge_transfer_depth <= 0.30 && t.mentorship_multiplier_score <= 0.35) return "knowledge_drain";
  if (t.succession_pipeline_readiness <= 0.30 && t.potential_trajectory_score <= 0.40) return "succession_gap";
  if (t.potential_trajectory_score <= 0.32 && t.learning_velocity_score <= 0.35) return "potential_stagnation";
  return "none";
}

function talentRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function talentSeverity(comp: number): string {
  if (comp >= 60) return "at_risk";
  if (comp >= 40) return "declining";
  if (comp >= 20) return "developing";
  return "thriving";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") {
    if (pattern === "talent_obsolescence" || pattern === "potential_stagnation") return "reskilling_program";
    return "talent_emergency_retention";
  }
  if (risk === "high") {
    if (pattern === "flight_risk_crisis") return "engagement_intervention";
    return "succession_acceleration";
  }
  if (risk === "moderate") return "talent_monitoring";
  return "no_action";
}

function talentSignal(t: Talent, pattern: string, comp: number): string {
  if (comp < 20) {
    return "Talent florissant — trajectoire élevée, forte valeur humaine, transmission du savoir active, alignement futur confirmé";
  }
  const labels: Record<string, string> = {
    talent_obsolescence: "Obsolescence des compétences",
    flight_risk_crisis:  "Crise de rétention — risque de départ imminent",
    knowledge_drain:     "Fuite du savoir organisationnel",
    succession_gap:      "Écart dans le pipeline de succession",
    potential_stagnation:"Stagnation du potentiel",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g, " ");
  return `${label} — demi-vie compétences ${t.skill_half_life_risk.toFixed(2)} — risque départ ${t.flight_risk_index.toFixed(2)} — valeur humaine ${t.human_capital_value_score.toFixed(2)} — succession ${t.succession_pipeline_readiness.toFixed(2)} — composite ${comp.toFixed(1)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const talents = MOCK_TALENTS.map(t => {
      const obs = obsolescenceScore(t);
      const flt = flightScore(t);
      const val = valueScore(t);
      const suc = successionScore(t);
      const comp = composite(obs, flt, val, suc);
      const pattern = talentPattern(t);
      const risk = talentRisk(comp);
      const severity = talentSeverity(comp);
      const action = recommendedAction(risk, pattern);
      return {
        talent_id: t.talent_id,
        talent_segment: t.talent_segment,
        region: t.region,
        talent_risk: risk,
        talent_pattern: pattern,
        talent_severity: severity,
        recommended_action: action,
        obsolescence_score: Math.round(obs * 100 * 100) / 100,
        flight_score: Math.round(flt * 100 * 100) / 100,
        value_score: Math.round(val * 100 * 100) / 100,
        succession_score: Math.round(suc * 100 * 100) / 100,
        talent_composite: comp,
        has_obsolescence_signal: comp >= 40 || t.skill_half_life_risk >= 0.60 || t.skills_future_alignment <= 0.30,
        requires_urgent_intervention: comp >= 25 || t.flight_risk_index >= 0.65 || t.succession_pipeline_readiness <= 0.25,
        estimated_talent_risk_index: Math.min(Math.round(comp / 100 * (1 - t.human_capital_value_score + 0.01) * 10 * 100) / 100, 10.0),
        talent_signal: talentSignal(t, pattern, comp),
      };
    });

    const rc: Record<string,number> = {};
    const pc: Record<string,number> = {};
    const sc: Record<string,number> = {};
    const ac: Record<string,number> = {};
    let tObs=0, tFlt=0, tVal=0, tSuc=0, tComp=0, tRiskIdx=0, obsC=0, urgentC=0;

    for (const tal of talents) {
      rc[tal.talent_risk]    = (rc[tal.talent_risk]    || 0) + 1;
      pc[tal.talent_pattern] = (pc[tal.talent_pattern] || 0) + 1;
      sc[tal.talent_severity] = (sc[tal.talent_severity] || 0) + 1;
      ac[tal.recommended_action] = (ac[tal.recommended_action] || 0) + 1;
      tObs  += tal.obsolescence_score;
      tFlt  += tal.flight_score;
      tVal  += tal.value_score;
      tSuc  += tal.succession_score;
      tComp += tal.talent_composite;
      tRiskIdx += tal.estimated_talent_risk_index;
      if (tal.has_obsolescence_signal) obsC++;
      if (tal.requires_urgent_intervention) urgentC++;
    }

    const n = talents.length;
    const summary = {
      total: n,
      risk_counts: rc,
      pattern_counts: pc,
      severity_counts: sc,
      action_counts: ac,
      avg_talent_composite: Math.round(tComp / n * 10) / 10,
      obsolescence_signal_count: obsC,
      urgent_intervention_count: urgentC,
      avg_obsolescence_score: Math.round(tObs / n * 10) / 10,
      avg_flight_score: Math.round(tFlt / n * 10) / 10,
      avg_succession_score: Math.round(tSuc / n * 10) / 10,
      avg_value_score: Math.round(tVal / n * 10) / 10,
      avg_estimated_talent_risk_index: Math.round(tRiskIdx / n * 100) / 100,
    };

    return NextResponse.json(sealResponse({ talents, summary }, "predictive-talent-intelligence-engine"));
  }

  return NextResponse.json(
    sealResponse(
      await (await fetch(`${process.env.SWARM_API_URL}/predictive-talent-intelligence-engine`)).json(),
      "predictive-talent-intelligence-engine",
    ),
  );
}
