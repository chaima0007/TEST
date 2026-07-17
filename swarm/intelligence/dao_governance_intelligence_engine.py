from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class DAOGovernanceInput:
    entity_id: str
    dao_type: str
    region: str
    voter_participation_rate: float
    plutocracy_concentration: float
    proposal_quality_score: float
    treasury_sustainability_index: float
    governance_attack_resistance: float
    delegate_diversity: float
    decision_execution_speed: float
    coordination_effectiveness: float
    sybil_attack_risk: float
    governance_fatigue_rate: float
    legal_wrapper_clarity: float
    cross_dao_collaboration: float
    token_distribution_equity: float
    emergency_mechanism_quality: float
    fork_risk_level: float
    constitutional_stability: float
    incentive_alignment: float


@dataclass
class DAOGovernanceResult:
    entity_id: str
    region: str
    dao_type: str
    dao_risk: str
    dao_pattern: str
    dao_severity: str
    recommended_action: str
    participation_score: float
    plutocracy_score: float
    treasury_score: float
    coordination_score: float
    dao_composite: float
    is_in_dao_crisis: bool
    requires_dao_intervention: bool
    dao_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "dao_type": self.dao_type,
            "dao_risk": self.dao_risk,
            "dao_pattern": self.dao_pattern,
            "dao_severity": self.dao_severity,
            "recommended_action": self.recommended_action,
            "participation_score": self.participation_score,
            "plutocracy_score": self.plutocracy_score,
            "treasury_score": self.treasury_score,
            "coordination_score": self.coordination_score,
            "dao_composite": self.dao_composite,
            "is_in_dao_crisis": self.is_in_dao_crisis,
            "requires_dao_intervention": self.requires_dao_intervention,
            "dao_signal": self.dao_signal,
        }


def _participation_score(inp: DAOGovernanceInput) -> float:
    return ((1 - inp.voter_participation_rate) * 0.4
            + inp.governance_fatigue_rate * 0.35
            + (1 - inp.delegate_diversity) * 0.25) * 100


def _plutocracy_score(inp: DAOGovernanceInput) -> float:
    return (inp.plutocracy_concentration * 0.4
            + (1 - inp.token_distribution_equity) * 0.35
            + (1 - inp.incentive_alignment) * 0.25) * 100


def _treasury_score(inp: DAOGovernanceInput) -> float:
    return ((1 - inp.treasury_sustainability_index) * 0.4
            + (1 - inp.governance_attack_resistance) * 0.35
            + inp.sybil_attack_risk * 0.25) * 100


def _coordination_score(inp: DAOGovernanceInput) -> float:
    return ((1 - inp.coordination_effectiveness) * 0.4
            + inp.fork_risk_level * 0.35
            + (1 - inp.constitutional_stability) * 0.25) * 100


def _composite(part: float, plut: float, treas: float, coord: float) -> float:
    return part * 0.30 + plut * 0.25 + treas * 0.25 + coord * 0.20


def _dao_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _dao_pattern(inp: DAOGovernanceInput) -> str:
    if (1 - inp.voter_participation_rate) >= 0.70 and inp.governance_fatigue_rate >= 0.65:
        return "voter_apathy_collapse"
    if inp.plutocracy_concentration >= 0.70 and (1 - inp.token_distribution_equity) >= 0.60:
        return "plutocracy_takeover"
    if (1 - inp.treasury_sustainability_index) >= 0.65 and (1 - inp.governance_attack_resistance) >= 0.55:
        return "treasury_drain"
    if inp.fork_risk_level >= 0.70 and (1 - inp.constitutional_stability) >= 0.60:
        return "fork_war"
    if inp.sybil_attack_risk >= 0.70 and (1 - inp.governance_attack_resistance) >= 0.60:
        return "sybil_governance_attack"
    return "none"


def _dao_severity(composite: float) -> str:
    if composite >= 75:
        return "dao_collapse"
    if composite >= 50:
        return "high_governance_failure"
    if composite >= 25:
        return "governance_stress"
    return "dao_thriving"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "dao_emergency_governance"
    if risk == "high" and pattern == "plutocracy_takeover":
        return "plutocracy_intervention"
    if risk == "high":
        return "governance_restructuring"
    if risk == "moderate":
        return "dao_monitoring"
    return "no_action"


def _dao_signal(inp: DAOGovernanceInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — participation votants {int(inp.voter_participation_rate * 100)}% "
            f"— concentration plutocratique {int(inp.plutocracy_concentration * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — durabilité trésorerie {int(inp.treasury_sustainability_index * 100)}% "
            f"— risque fourche {int(inp.fork_risk_level * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — fatigue gouvernance {int(inp.governance_fatigue_rate * 100)}% "
            f"— composite {comp_int}"
        )
    return "DAO gouvernance optimale — participation active, trésorerie durable, coordination efficace"


def analyze_dao_governance(inp: DAOGovernanceInput) -> DAOGovernanceResult:
    part = _participation_score(inp)
    plut = _plutocracy_score(inp)
    treas = _treasury_score(inp)
    coord = _coordination_score(inp)
    comp = _composite(part, plut, treas, coord)
    risk = _dao_risk(comp)
    pattern = _dao_pattern(inp)
    severity = _dao_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _dao_signal(inp, risk, comp)

    return DAOGovernanceResult(
        entity_id=inp.entity_id,
        region=inp.region,
        dao_type=inp.dao_type,
        dao_risk=risk,
        dao_pattern=pattern,
        dao_severity=severity,
        recommended_action=action,
        participation_score=round(part, 2),
        plutocracy_score=round(plut, 2),
        treasury_score=round(treas, 2),
        coordination_score=round(coord, 2),
        dao_composite=round(comp, 2),
        is_in_dao_crisis=comp >= 60,
        requires_dao_intervention=comp >= 40,
        dao_signal=signal,
    )


class DAOGovernanceIntelligenceEngine:
    def __init__(self, inputs: List[DAOGovernanceInput]):
        self.inputs = inputs
        self.results: List[DAOGovernanceResult] = [analyze_dao_governance(i) for i in inputs]

    def summary(self) -> Dict[str, Any]:
        n = len(self.results)
        if n == 0:
            return {}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        total_composite = 0.0
        total_participation = 0.0
        total_plutocracy = 0.0
        total_treasury = 0.0
        total_coordination = 0.0
        dao_crisis_count = 0
        dao_intervention_count = 0

        for r in self.results:
            risk_counts[r.dao_risk] = risk_counts.get(r.dao_risk, 0) + 1
            pattern_counts[r.dao_pattern] = pattern_counts.get(r.dao_pattern, 0) + 1
            severity_counts[r.dao_severity] = severity_counts.get(r.dao_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.dao_composite
            total_participation += r.participation_score
            total_plutocracy += r.plutocracy_score
            total_treasury += r.treasury_score
            total_coordination += r.coordination_score
            if r.is_in_dao_crisis:
                dao_crisis_count += 1
            if r.requires_dao_intervention:
                dao_intervention_count += 1

        avg_composite = total_composite / n

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_dao_composite": round(avg_composite, 2),
            "dao_crisis_count": dao_crisis_count,
            "dao_intervention_count": dao_intervention_count,
            "avg_participation_score": round(total_participation / n, 2),
            "avg_plutocracy_score": round(total_plutocracy / n, 2),
            "avg_treasury_score": round(total_treasury / n, 2),
            "avg_coordination_score": round(total_coordination / n, 2),
            "avg_estimated_dao_risk_index": round(avg_composite / 100 * 10, 2),
        }
