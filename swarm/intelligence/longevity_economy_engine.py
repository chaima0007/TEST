"""
Module 295: Longevity Economy & Silver Intelligence Engine
Caelum Partners — Swarm Intelligence Framework
Capitalizing on the longevity megatrend: aging population economics,
silver economy, longevity biotech, intergenerational wealth transfer.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class LongevityEconomyInput:
    entity_id: str
    longevity_segment: str
    region: str
    aging_population_rate: float
    longevity_biotech_adoption: float
    silver_spending_power: float
    intergenerational_wealth_transfer_rate: float
    pension_system_stress: float
    healthcare_cost_inflation: float
    productive_aging_index: float
    cognitive_decline_risk: float
    eldercare_infrastructure_gap: float
    longevity_financial_products_penetration: float
    age_discrimination_index: float
    social_isolation_risk: float
    multigenerational_workforce_integration: float
    longevity_insurance_penetration: float
    retirement_adequacy_gap: float
    silver_digital_inclusion: float
    geroscience_readiness: float


@dataclass
class LongevityEconomyResult:
    entity_id: str
    region: str
    longevity_segment: str
    longevity_risk: str
    longevity_pattern: str
    longevity_severity: str
    recommended_action: str
    aging_score: float
    financial_score: float
    health_score: float
    inclusion_score: float
    longevity_composite: float
    is_in_longevity_crisis: bool
    requires_longevity_intervention: bool
    longevity_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "longevity_segment": self.longevity_segment,
            "longevity_risk": self.longevity_risk,
            "longevity_pattern": self.longevity_pattern,
            "longevity_severity": self.longevity_severity,
            "recommended_action": self.recommended_action,
            "aging_score": self.aging_score,
            "financial_score": self.financial_score,
            "health_score": self.health_score,
            "inclusion_score": self.inclusion_score,
            "longevity_composite": self.longevity_composite,
            "is_in_longevity_crisis": self.is_in_longevity_crisis,
            "requires_longevity_intervention": self.requires_longevity_intervention,
            "longevity_signal": self.longevity_signal,
        }


def _aging_score(inp: LongevityEconomyInput) -> float:
    raw = (
        inp.aging_population_rate * 0.4
        + inp.pension_system_stress * 0.35
        + inp.retirement_adequacy_gap * 0.25
    ) * 100
    return round(raw, 2)


def _financial_score(inp: LongevityEconomyInput) -> float:
    raw = (
        (1 - inp.silver_spending_power) * 0.4
        + (1 - inp.longevity_financial_products_penetration) * 0.35
        + (1 - inp.longevity_insurance_penetration) * 0.25
    ) * 100
    return round(raw, 2)


def _health_score(inp: LongevityEconomyInput) -> float:
    raw = (
        inp.healthcare_cost_inflation * 0.4
        + inp.eldercare_infrastructure_gap * 0.35
        + inp.cognitive_decline_risk * 0.25
    ) * 100
    return round(raw, 2)


def _inclusion_score(inp: LongevityEconomyInput) -> float:
    raw = (
        inp.social_isolation_risk * 0.4
        + inp.age_discrimination_index * 0.35
        + (1 - inp.silver_digital_inclusion) * 0.25
    ) * 100
    return round(raw, 2)


def _composite(aging: float, financial: float, health: float, inclusion: float) -> float:
    return round(aging * 0.30 + financial * 0.25 + health * 0.25 + inclusion * 0.20, 2)


def _longevity_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _longevity_pattern(inp: LongevityEconomyInput) -> str:
    if inp.pension_system_stress >= 0.70 and inp.retirement_adequacy_gap >= 0.65:
        return "pension_collapse"
    if inp.healthcare_cost_inflation >= 0.70 and inp.eldercare_infrastructure_gap >= 0.60:
        return "healthcare_cost_spiral"
    if (1 - inp.silver_digital_inclusion) >= 0.65 and inp.social_isolation_risk >= 0.60:
        return "silver_exclusion"
    if (1 - inp.intergenerational_wealth_transfer_rate) >= 0.65 and inp.age_discrimination_index >= 0.55:
        return "intergenerational_wealth_lock"
    if (1 - inp.longevity_insurance_penetration) >= 0.70 and inp.retirement_adequacy_gap >= 0.60:
        return "longevity_insurance_gap"
    return "none"


def _longevity_severity(composite: float) -> str:
    if composite >= 75:
        return "longevity_emergency"
    if composite >= 50:
        return "high_longevity_risk"
    if composite >= 25:
        return "silver_stress"
    return "longevity_thriving"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "longevity_emergency_program"
    if risk == "high":
        if pattern == "pension_collapse":
            return "pension_rescue"
        return "silver_economy_stimulus"
    if risk == "moderate":
        return "longevity_monitoring"
    return "no_action"


def _longevity_signal(inp: LongevityEconomyInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — stress système pension {int(inp.pension_system_stress * 100)}%"
            f" — inflation soins santé {int(inp.healthcare_cost_inflation * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — isolation sociale seniors {int(inp.social_isolation_risk * 100)}%"
            f" — gap retraite {int(inp.retirement_adequacy_gap * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — inclusion digitale silver {int(inp.silver_digital_inclusion * 100)}%"
            f" — composite {int(composite)}"
        )
    return "Économie longévité florissante — silver power fort, systèmes de retraite robustes"


def analyze(inp: LongevityEconomyInput) -> LongevityEconomyResult:
    aging = _aging_score(inp)
    financial = _financial_score(inp)
    health = _health_score(inp)
    inclusion = _inclusion_score(inp)
    composite = _composite(aging, financial, health, inclusion)
    risk = _longevity_risk(composite)
    pattern = _longevity_pattern(inp)
    severity = _longevity_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _longevity_signal(inp, risk, composite)

    return LongevityEconomyResult(
        entity_id=inp.entity_id,
        region=inp.region,
        longevity_segment=inp.longevity_segment,
        longevity_risk=risk,
        longevity_pattern=pattern,
        longevity_severity=severity,
        recommended_action=action,
        aging_score=aging,
        financial_score=financial,
        health_score=health,
        inclusion_score=inclusion,
        longevity_composite=composite,
        is_in_longevity_crisis=composite >= 60,
        requires_longevity_intervention=composite >= 40,
        longevity_signal=signal,
    )


class LongevityEconomyEngine:
    def __init__(self) -> None:
        self._results: List[LongevityEconomyResult] = []

    def run(self, inputs: List[LongevityEconomyInput]) -> Dict[str, Any]:
        self._results = [analyze(inp) for inp in inputs]
        entities = [r.to_dict() for r in self._results]
        summary = self._summarize()
        return {"entities": entities, "summary": summary}

    def _summarize(self) -> Dict[str, Any]:
        results = self._results
        n = len(results)
        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_longevity_composite": 0.0,
                "longevity_crisis_count": 0,
                "longevity_intervention_count": 0,
                "avg_aging_score": 0.0,
                "avg_financial_score": 0.0,
                "avg_health_score": 0.0,
                "avg_inclusion_score": 0.0,
                "avg_estimated_longevity_risk_index": 0.0,
            }

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        total_composite = 0.0
        total_aging = 0.0
        total_financial = 0.0
        total_health = 0.0
        total_inclusion = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.longevity_risk] = risk_counts.get(r.longevity_risk, 0) + 1
            pattern_counts[r.longevity_pattern] = pattern_counts.get(r.longevity_pattern, 0) + 1
            severity_counts[r.longevity_severity] = severity_counts.get(r.longevity_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.longevity_composite
            total_aging += r.aging_score
            total_financial += r.financial_score
            total_health += r.health_score
            total_inclusion += r.inclusion_score
            if r.is_in_longevity_crisis:
                crisis_count += 1
            if r.requires_longevity_intervention:
                intervention_count += 1

        avg_composite = round(total_composite / n, 2)
        avg_estimated_longevity_risk_index = round(avg_composite / 100 * 10, 2)

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_longevity_composite": avg_composite,
            "longevity_crisis_count": crisis_count,
            "longevity_intervention_count": intervention_count,
            "avg_aging_score": round(total_aging / n, 2),
            "avg_financial_score": round(total_financial / n, 2),
            "avg_health_score": round(total_health / n, 2),
            "avg_inclusion_score": round(total_inclusion / n, 2),
            "avg_estimated_longevity_risk_index": avg_estimated_longevity_risk_index,
        }
