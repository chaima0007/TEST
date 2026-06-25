"""
Module 301 — Autonomous Agent Economy & Robot Labor Market Engine
Caelum Partners — Chaima Mhadbi, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AutonomousAgentEconomyInput:
    entity_id: str
    agent_category: str
    region: str
    # 17 float fields
    agent_market_penetration: float
    labor_displacement_rate: float
    human_agent_collaboration_index: float
    agent_specialization_depth: float
    task_automation_coverage: float
    agent_governance_maturity: float
    economic_value_capture_by_agents: float
    human_reskilling_velocity: float
    agent_accountability_gap: float
    wage_floor_erosion: float
    agent_coordination_efficiency: float
    monopolization_risk: float
    agent_safety_compliance: float
    income_redistribution_mechanism: float
    agent_bias_prevalence: float
    sovereign_agent_dependency: float
    agent_ecosystem_diversity: float


@dataclass
class AutonomousAgentEconomyResult:
    entity_id: str
    region: str
    agent_category: str
    agent_risk: str
    agent_pattern: str
    agent_severity: str
    recommended_action: str
    displacement_score: float
    governance_score: float
    equity_score: float
    safety_score: float
    agent_composite: float
    is_in_agent_crisis: bool
    requires_agent_intervention: bool
    agent_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "agent_category": self.agent_category,
            "agent_risk": self.agent_risk,
            "agent_pattern": self.agent_pattern,
            "agent_severity": self.agent_severity,
            "recommended_action": self.recommended_action,
            "displacement_score": self.displacement_score,
            "governance_score": self.governance_score,
            "equity_score": self.equity_score,
            "safety_score": self.safety_score,
            "agent_composite": self.agent_composite,
            "is_in_agent_crisis": self.is_in_agent_crisis,
            "requires_agent_intervention": self.requires_agent_intervention,
            "agent_signal": self.agent_signal,
        }


def _displacement_score(inp: AutonomousAgentEconomyInput) -> float:
    raw = (
        inp.labor_displacement_rate * 0.4
        + inp.task_automation_coverage * 0.35
        + inp.wage_floor_erosion * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(inp: AutonomousAgentEconomyInput) -> float:
    raw = (
        (1 - inp.agent_governance_maturity) * 0.4
        + inp.agent_accountability_gap * 0.35
        + (1 - inp.agent_ecosystem_diversity) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _equity_score(inp: AutonomousAgentEconomyInput) -> float:
    raw = (
        (1 - inp.income_redistribution_mechanism) * 0.4
        + inp.monopolization_risk * 0.35
        + (1 - inp.human_reskilling_velocity) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _safety_score(inp: AutonomousAgentEconomyInput) -> float:
    raw = (
        inp.agent_bias_prevalence * 0.4
        + (1 - inp.agent_safety_compliance) * 0.35
        + inp.sovereign_agent_dependency * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    displacement: float,
    governance: float,
    equity: float,
    safety: float,
) -> float:
    return round(
        displacement * 0.30
        + governance * 0.25
        + equity * 0.25
        + safety * 0.20,
        2,
    )


def _agent_pattern(inp: AutonomousAgentEconomyInput) -> str:
    if inp.labor_displacement_rate >= 0.70 and (1 - inp.human_reskilling_velocity) >= 0.60:
        return "mass_displacement_crisis"
    if inp.monopolization_risk >= 0.70 and inp.economic_value_capture_by_agents >= 0.65:
        return "agent_monopoly"
    if (1 - inp.agent_governance_maturity) >= 0.65 and inp.agent_accountability_gap >= 0.60:
        return "governance_vacuum"
    if (1 - inp.income_redistribution_mechanism) >= 0.70 and inp.wage_floor_erosion >= 0.65:
        return "equity_collapse"
    if inp.agent_bias_prevalence >= 0.65 and (1 - inp.agent_safety_compliance) >= 0.60:
        return "safety_failure"
    return "none"


def _agent_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _agent_severity(composite: float) -> str:
    if composite >= 75:
        return "agent_economy_emergency"
    if composite >= 50:
        return "high_disruption"
    if composite >= 25:
        return "labor_stress"
    return "agent_economy_thriving"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "agent_economy_emergency_governance"
    if risk == "high" and pattern == "mass_displacement_crisis":
        return "displacement_mitigation"
    if risk == "high":
        return "agent_regulation"
    if risk == "moderate":
        return "agent_monitoring"
    return "no_action"


def _agent_signal(inp: AutonomousAgentEconomyInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — déplacement emplois {int(inp.labor_displacement_rate * 100)}% "
            f"— risque monopolisation {int(inp.monopolization_risk * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — maturité gouvernance agents {int(inp.agent_governance_maturity * 100)}% "
            f"— redistribution revenus {int(inp.income_redistribution_mechanism * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — couverture automatisation {int(inp.task_automation_coverage * 100)}% "
            f"— composite {int(composite)}"
        )
    return "Économie agents autonomes florissante — collaboration humain-agent optimale, gouvernance solide"


def analyze(inp: AutonomousAgentEconomyInput) -> AutonomousAgentEconomyResult:
    disp = _displacement_score(inp)
    gov = _governance_score(inp)
    eq = _equity_score(inp)
    saf = _safety_score(inp)
    comp = _composite(disp, gov, eq, saf)
    pat = _agent_pattern(inp)
    risk = _agent_risk(comp)
    sev = _agent_severity(comp)
    action = _recommended_action(risk, pat)
    sig = _agent_signal(inp, risk, comp)

    return AutonomousAgentEconomyResult(
        entity_id=inp.entity_id,
        region=inp.region,
        agent_category=inp.agent_category,
        agent_risk=risk,
        agent_pattern=pat,
        agent_severity=sev,
        recommended_action=action,
        displacement_score=disp,
        governance_score=gov,
        equity_score=eq,
        safety_score=saf,
        agent_composite=comp,
        is_in_agent_crisis=comp >= 60,
        requires_agent_intervention=comp >= 40,
        agent_signal=sig,
    )


class AutonomousAgentEconomyEngine:
    def __init__(self, inputs: List[AutonomousAgentEconomyInput]):
        self.inputs = inputs
        self.results: List[AutonomousAgentEconomyResult] = [analyze(i) for i in inputs]

    def summary(self) -> Dict[str, Any]:
        n = len(self.results)
        if n == 0:
            return {}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_displacement = 0.0
        total_governance = 0.0
        total_equity = 0.0
        total_safety = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in self.results:
            risk_counts[r.agent_risk] = risk_counts.get(r.agent_risk, 0) + 1
            pattern_counts[r.agent_pattern] = pattern_counts.get(r.agent_pattern, 0) + 1
            severity_counts[r.agent_severity] = severity_counts.get(r.agent_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1

            total_composite += r.agent_composite
            total_displacement += r.displacement_score
            total_governance += r.governance_score
            total_equity += r.equity_score
            total_safety += r.safety_score

            if r.is_in_agent_crisis:
                crisis_count += 1
            if r.requires_agent_intervention:
                intervention_count += 1

        avg_composite = round(total_composite / n * 10) / 10

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_agent_composite": avg_composite,
            "agent_crisis_count": crisis_count,
            "agent_intervention_count": intervention_count,
            "avg_displacement_score": round(total_displacement / n * 10) / 10,
            "avg_governance_score": round(total_governance / n * 10) / 10,
            "avg_equity_score": round(total_equity / n * 10) / 10,
            "avg_safety_score": round(total_safety / n * 10) / 10,
            "avg_estimated_agent_disruption_index": round(avg_composite / 100 * 10, 2),
        }
