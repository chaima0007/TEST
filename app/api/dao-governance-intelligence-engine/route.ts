import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // DGI-001: EMEA, protocol_dao → critical, voter_apathy_collapse
  {
    entity_id: "DGI-001", dao_type: "protocol_dao", region: "EMEA",
    voter_participation_rate: 0.10, plutocracy_concentration: 0.62,
    proposal_quality_score: 0.30, treasury_sustainability_index: 0.40,
    governance_attack_resistance: 0.38, delegate_diversity: 0.15,
    decision_execution_speed: 0.35, coordination_effectiveness: 0.38,
    sybil_attack_risk: 0.50, governance_fatigue_rate: 0.82,
    legal_wrapper_clarity: 0.35, cross_dao_collaboration: 0.30,
    token_distribution_equity: 0.30, emergency_mechanism_quality: 0.35,
    fork_risk_level: 0.50, constitutional_stability: 0.42,
    incentive_alignment: 0.32,
  },
  // DGI-002: APAC, investment_dao → low, dao_thriving/none
  {
    entity_id: "DGI-002", dao_type: "investment_dao", region: "APAC",
    voter_participation_rate: 0.82, plutocracy_concentration: 0.18,
    proposal_quality_score: 0.85, treasury_sustainability_index: 0.88,
    governance_attack_resistance: 0.90, delegate_diversity: 0.85,
    decision_execution_speed: 0.88, coordination_effectiveness: 0.90,
    sybil_attack_risk: 0.10, governance_fatigue_rate: 0.12,
    legal_wrapper_clarity: 0.88, cross_dao_collaboration: 0.82,
    token_distribution_equity: 0.88, emergency_mechanism_quality: 0.90,
    fork_risk_level: 0.10, constitutional_stability: 0.92,
    incentive_alignment: 0.88,
  },
  // DGI-003: NOAM, social_dao → high, plutocracy_takeover
  {
    entity_id: "DGI-003", dao_type: "social_dao", region: "NOAM",
    voter_participation_rate: 0.50, plutocracy_concentration: 0.75,
    proposal_quality_score: 0.38, treasury_sustainability_index: 0.55,
    governance_attack_resistance: 0.55, delegate_diversity: 0.45,
    decision_execution_speed: 0.42, coordination_effectiveness: 0.50,
    sybil_attack_risk: 0.35, governance_fatigue_rate: 0.45,
    legal_wrapper_clarity: 0.42, cross_dao_collaboration: 0.38,
    token_distribution_equity: 0.32, emergency_mechanism_quality: 0.40,
    fork_risk_level: 0.38, constitutional_stability: 0.55,
    incentive_alignment: 0.42,
  },
  // DGI-004: LATAM, investment_dao → low, dao_thriving/none
  {
    entity_id: "DGI-004", dao_type: "investment_dao", region: "LATAM",
    voter_participation_rate: 0.78, plutocracy_concentration: 0.20,
    proposal_quality_score: 0.80, treasury_sustainability_index: 0.82,
    governance_attack_resistance: 0.85, delegate_diversity: 0.80,
    decision_execution_speed: 0.82, coordination_effectiveness: 0.85,
    sybil_attack_risk: 0.12, governance_fatigue_rate: 0.15,
    legal_wrapper_clarity: 0.82, cross_dao_collaboration: 0.78,
    token_distribution_equity: 0.82, emergency_mechanism_quality: 0.85,
    fork_risk_level: 0.12, constitutional_stability: 0.88,
    incentive_alignment: 0.85,
  },
  // DGI-005: MEA, protocol_dao → critical, treasury_drain
  {
    entity_id: "DGI-005", dao_type: "protocol_dao", region: "MEA",
    voter_participation_rate: 0.42, plutocracy_concentration: 0.58,
    proposal_quality_score: 0.30, treasury_sustainability_index: 0.22,
    governance_attack_resistance: 0.35, delegate_diversity: 0.35,
    decision_execution_speed: 0.32, coordination_effectiveness: 0.35,
    sybil_attack_risk: 0.65, governance_fatigue_rate: 0.58,
    legal_wrapper_clarity: 0.32, cross_dao_collaboration: 0.30,
    token_distribution_equity: 0.35, emergency_mechanism_quality: 0.32,
    fork_risk_level: 0.55, constitutional_stability: 0.42,
    incentive_alignment: 0.32,
  },
  // DGI-006: EMEA, grant_dao → moderate, none
  {
    entity_id: "DGI-006", dao_type: "grant_dao", region: "EMEA",
    voter_participation_rate: 0.58, plutocracy_concentration: 0.35,
    proposal_quality_score: 0.60, treasury_sustainability_index: 0.62,
    governance_attack_resistance: 0.65, delegate_diversity: 0.60,
    decision_execution_speed: 0.58, coordination_effectiveness: 0.65,
    sybil_attack_risk: 0.28, governance_fatigue_rate: 0.38,
    legal_wrapper_clarity: 0.60, cross_dao_collaboration: 0.58,
    token_distribution_equity: 0.65, emergency_mechanism_quality: 0.62,
    fork_risk_level: 0.30, constitutional_stability: 0.68,
    incentive_alignment: 0.62,
  },
  // DGI-007: APAC, social_dao → high, fork_war
  {
    entity_id: "DGI-007", dao_type: "social_dao", region: "APAC",
    voter_participation_rate: 0.48, plutocracy_concentration: 0.45,
    proposal_quality_score: 0.38, treasury_sustainability_index: 0.50,
    governance_attack_resistance: 0.52, delegate_diversity: 0.45,
    decision_execution_speed: 0.40, coordination_effectiveness: 0.42,
    sybil_attack_risk: 0.40, governance_fatigue_rate: 0.50,
    legal_wrapper_clarity: 0.42, cross_dao_collaboration: 0.38,
    token_distribution_equity: 0.50, emergency_mechanism_quality: 0.42,
    fork_risk_level: 0.75, constitutional_stability: 0.32,
    incentive_alignment: 0.45,
  },
  // DGI-008: NOAM, protocol_dao → critical, sybil_governance_attack
  {
    entity_id: "DGI-008", dao_type: "protocol_dao", region: "NOAM",
    voter_participation_rate: 0.35, plutocracy_concentration: 0.55,
    proposal_quality_score: 0.30, treasury_sustainability_index: 0.40,
    governance_attack_resistance: 0.30, delegate_diversity: 0.38,
    decision_execution_speed: 0.32, coordination_effectiveness: 0.38,
    sybil_attack_risk: 0.80, governance_fatigue_rate: 0.60,
    legal_wrapper_clarity: 0.32, cross_dao_collaboration: 0.30,
    token_distribution_equity: 0.38, emergency_mechanism_quality: 0.32,
    fork_risk_level: 0.55, constitutional_stability: 0.45,
    incentive_alignment: 0.35,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function participationScore(e: Entity): number {
  return ((1 - e.voter_participation_rate) * 0.4
    + e.governance_fatigue_rate * 0.35
    + (1 - e.delegate_diversity) * 0.25) * 100;
}

function plutocracyScore(e: Entity): number {
  return (e.plutocracy_concentration * 0.4
    + (1 - e.token_distribution_equity) * 0.35
    + (1 - e.incentive_alignment) * 0.25) * 100;
}

function treasuryScore(e: Entity): number {
  return ((1 - e.treasury_sustainability_index) * 0.4
    + (1 - e.governance_attack_resistance) * 0.35
    + e.sybil_attack_risk * 0.25) * 100;
}

function coordinationScore(e: Entity): number {
  return ((1 - e.coordination_effectiveness) * 0.4
    + e.fork_risk_level * 0.35
    + (1 - e.constitutional_stability) * 0.25) * 100;
}

function daoComposite(part: number, plut: number, treas: number, coord: number): number {
  return Math.round((part * 0.30 + plut * 0.25 + treas * 0.25 + coord * 0.20) * 100) / 100;
}

function daoRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function daoPattern(e: Entity): string {
  if ((1 - e.voter_participation_rate) >= 0.70 && e.governance_fatigue_rate >= 0.65)
    return "voter_apathy_collapse";
  if (e.plutocracy_concentration >= 0.70 && (1 - e.token_distribution_equity) >= 0.60)
    return "plutocracy_takeover";
  if ((1 - e.treasury_sustainability_index) >= 0.65 && (1 - e.governance_attack_resistance) >= 0.55)
    return "treasury_drain";
  if (e.fork_risk_level >= 0.70 && (1 - e.constitutional_stability) >= 0.60)
    return "fork_war";
  if (e.sybil_attack_risk >= 0.70 && (1 - e.governance_attack_resistance) >= 0.60)
    return "sybil_governance_attack";
  return "none";
}

function daoSeverity(comp: number): string {
  if (comp >= 75) return "dao_collapse";
  if (comp >= 50) return "high_governance_failure";
  if (comp >= 25) return "governance_stress";
  return "dao_thriving";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "dao_emergency_governance";
  if (risk === "high" && pattern === "plutocracy_takeover") return "plutocracy_intervention";
  if (risk === "high") return "governance_restructuring";
  if (risk === "moderate") return "dao_monitoring";
  return "no_action";
}

function daoSignal(e: Entity, risk: string, comp: number): string {
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — participation votants ${Math.round(e.voter_participation_rate * 100)}% — concentration plutocratique ${Math.round(e.plutocracy_concentration * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — durabilité trésorerie ${Math.round(e.treasury_sustainability_index * 100)}% — risque fourche ${Math.round(e.fork_risk_level * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — fatigue gouvernance ${Math.round(e.governance_fatigue_rate * 100)}% — composite ${compInt}`;
  }
  return "DAO gouvernance optimale — participation active, trésorerie durable, coordination efficace";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const part  = participationScore(e);
      const plut  = plutocracyScore(e);
      const treas = treasuryScore(e);
      const coord = coordinationScore(e);
      const comp  = daoComposite(part, plut, treas, coord);
      const risk  = daoRisk(comp);
      const pat   = daoPattern(e);
      const sev   = daoSeverity(comp);
      const act   = recommendedAction(risk, pat);
      const sig   = daoSignal(e, risk, comp);
      return {
        entity_id:                e.entity_id,
        region:                   e.region,
        dao_type:                 e.dao_type,
        dao_risk:                 risk,
        dao_pattern:              pat,
        dao_severity:             sev,
        recommended_action:       act,
        participation_score:      Math.round(part * 100) / 100,
        plutocracy_score:         Math.round(plut * 100) / 100,
        treasury_score:           Math.round(treas * 100) / 100,
        coordination_score:       Math.round(coord * 100) / 100,
        dao_composite:            comp,
        is_in_dao_crisis:         comp >= 60,
        requires_dao_intervention: comp >= 40,
        dao_signal:               sig,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tPart = 0, tPlut = 0, tTreas = 0, tCoord = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.dao_risk]          = (rc[ent.dao_risk]          || 0) + 1;
      pc[ent.dao_pattern]       = (pc[ent.dao_pattern]       || 0) + 1;
      sc[ent.dao_severity]      = (sc[ent.dao_severity]      || 0) + 1;
      ac[ent.recommended_action]= (ac[ent.recommended_action]|| 0) + 1;
      tPart  += ent.participation_score;
      tPlut  += ent.plutocracy_score;
      tTreas += ent.treasury_score;
      tCoord += ent.coordination_score;
      tComp  += ent.dao_composite;
      if (ent.is_in_dao_crisis)          crisisCount++;
      if (ent.requires_dao_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComposite = tComp / n;
    const summary = {
      total:                        n,
      risk_counts:                  rc,
      pattern_counts:               pc,
      severity_counts:              sc,
      action_counts:                ac,
      avg_dao_composite:            Math.round(avgComposite * 10) / 10,
      dao_crisis_count:             crisisCount,
      dao_intervention_count:       interventionCount,
      avg_participation_score:      Math.round(tPart  / n * 10) / 10,
      avg_plutocracy_score:         Math.round(tPlut  / n * 10) / 10,
      avg_treasury_score:           Math.round(tTreas / n * 10) / 10,
      avg_coordination_score:       Math.round(tCoord / n * 10) / 10,
      avg_estimated_dao_risk_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "dao-governance-intelligence-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/dao-governance-intelligence-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "dao-governance-intelligence-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream DAO Governance Intelligence Engine unavailable" }, "dao-governance-intelligence-engine"),
      { status: 502 }
    );
  }
}
