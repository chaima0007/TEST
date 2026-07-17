"""
Module 287: Sovereign Wealth Intelligence & Capital Allocation Engine
Caelum Partners — Intelligence layer for sovereign wealth funds
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class SovereignWealthInput:
    entity_id: str
    fund_type: str
    region: str
    mandate_alignment: float
    diversification_quality: float
    liquidity_buffer: float
    geopolitical_exposure: float
    currency_concentration: float
    return_on_mandate: float
    esg_compliance: float
    governance_maturity: float
    political_interference_risk: float
    rebalancing_agility: float
    alternative_asset_integration: float
    sovereign_debt_exposure: float
    concentration_risk: float
    duration_mismatch: float
    transparency_index: float
    intergenerational_equity: float
    shock_absorption_capacity: float


@dataclass
class SovereignWealthResult:
    entity_id: str
    region: str
    fund_type: str
    sw_risk: str
    sw_pattern: str
    sw_severity: str
    recommended_action: str
    allocation_score: float
    governance_score: float
    resilience_score: float
    mandate_score: float
    sw_composite: float
    is_in_sw_crisis: bool
    requires_sw_intervention: bool
    sw_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "fund_type": self.fund_type,
            "sw_risk": self.sw_risk,
            "sw_pattern": self.sw_pattern,
            "sw_severity": self.sw_severity,
            "recommended_action": self.recommended_action,
            "allocation_score": self.allocation_score,
            "governance_score": self.governance_score,
            "resilience_score": self.resilience_score,
            "mandate_score": self.mandate_score,
            "sw_composite": self.sw_composite,
            "is_in_sw_crisis": self.is_in_sw_crisis,
            "requires_sw_intervention": self.requires_sw_intervention,
            "sw_signal": self.sw_signal,
        }


def _compute_allocation_score(e: SovereignWealthInput) -> float:
    raw = (
        e.concentration_risk * 0.4
        + e.currency_concentration * 0.3
        + (1 - e.diversification_quality) * 0.3
    ) * 100
    return round(raw * 100) / 100


def _compute_governance_score(e: SovereignWealthInput) -> float:
    raw = (
        e.political_interference_risk * 0.4
        + (1 - e.governance_maturity) * 0.35
        + (1 - e.transparency_index) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _compute_resilience_score(e: SovereignWealthInput) -> float:
    raw = (
        (1 - e.shock_absorption_capacity) * 0.4
        + (1 - e.liquidity_buffer) * 0.35
        + e.duration_mismatch * 0.25
    ) * 100
    return round(raw * 100) / 100


def _compute_mandate_score(e: SovereignWealthInput) -> float:
    raw = (
        (1 - e.mandate_alignment) * 0.4
        + (1 - e.return_on_mandate) * 0.35
        + (1 - e.intergenerational_equity) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _compute_composite(
    allocation: float, governance: float, resilience: float, mandate: float
) -> float:
    return round(
        (allocation * 0.30 + governance * 0.25 + resilience * 0.25 + mandate * 0.20)
        * 100
    ) / 100


def _sw_pattern(e: SovereignWealthInput) -> str:
    if e.concentration_risk >= 0.65 and (1 - e.diversification_quality) >= 0.55:
        return "capital_misallocation"
    if e.political_interference_risk >= 0.65 and (1 - e.governance_maturity) >= 0.55:
        return "political_capture"
    if (1 - e.liquidity_buffer) >= 0.65 and (1 - e.shock_absorption_capacity) >= 0.55:
        return "liquidity_trap"
    if (1 - e.mandate_alignment) >= 0.65 and (1 - e.return_on_mandate) >= 0.55:
        return "mandate_drift"
    if e.geopolitical_exposure >= 0.70 and e.sovereign_debt_exposure >= 0.60:
        return "geopolitical_overexposure"
    return "none"


def _sw_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _sw_severity(composite: float) -> str:
    if composite >= 75:
        return "sovereign_crisis"
    if composite >= 50:
        return "high_dysfunction"
    if composite >= 25:
        return "capital_stress"
    return "optimal_allocation"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "sovereign_emergency_rebalancing"
    if risk == "high" and pattern == "political_capture":
        return "governance_intervention"
    if risk == "high":
        return "capital_reallocation"
    if risk == "moderate":
        return "sw_monitoring"
    return "no_action"


def _sw_signal(e: SovereignWealthInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — concentration risque {int(e.concentration_risk * 100)}%"
            f" — interférence politique {int(e.political_interference_risk * 100)}%"
            f" — composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — alignement mandat {int(e.mandate_alignment * 100)}%"
            f" — buffer liquidité {int(e.liquidity_buffer * 100)}%"
            f" — composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — qualité diversification {int(e.diversification_quality * 100)}%"
            f" — composite {comp_int}"
        )
    return "Fonds souverain optimal — allocation équilibrée, mandat respecté, gouvernance solide"


def analyze_entity(e: SovereignWealthInput) -> SovereignWealthResult:
    allocation = _compute_allocation_score(e)
    governance = _compute_governance_score(e)
    resilience = _compute_resilience_score(e)
    mandate = _compute_mandate_score(e)
    composite = _compute_composite(allocation, governance, resilience, mandate)

    pattern = _sw_pattern(e)
    risk = _sw_risk(composite)
    severity = _sw_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _sw_signal(e, risk, composite)

    return SovereignWealthResult(
        entity_id=e.entity_id,
        region=e.region,
        fund_type=e.fund_type,
        sw_risk=risk,
        sw_pattern=pattern,
        sw_severity=severity,
        recommended_action=action,
        allocation_score=allocation,
        governance_score=governance,
        resilience_score=resilience,
        mandate_score=mandate,
        sw_composite=composite,
        is_in_sw_crisis=composite >= 60,
        requires_sw_intervention=composite >= 40,
        sw_signal=signal,
    )


class SovereignWealthIntelligenceEngine:
    """Intelligence engine for sovereign wealth fund analysis."""

    def analyze(self, entities: List[SovereignWealthInput]) -> Dict[str, Any]:
        results = [analyze_entity(e) for e in entities]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_allocation = 0.0
        total_governance = 0.0
        total_resilience = 0.0
        total_mandate = 0.0
        sw_crisis_count = 0
        sw_intervention_count = 0

        for r in results:
            risk_counts[r.sw_risk] = risk_counts.get(r.sw_risk, 0) + 1
            pattern_counts[r.sw_pattern] = pattern_counts.get(r.sw_pattern, 0) + 1
            severity_counts[r.sw_severity] = severity_counts.get(r.sw_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.sw_composite
            total_allocation += r.allocation_score
            total_governance += r.governance_score
            total_resilience += r.resilience_score
            total_mandate += r.mandate_score
            if r.is_in_sw_crisis:
                sw_crisis_count += 1
            if r.requires_sw_intervention:
                sw_intervention_count += 1

        n = len(results)
        avg_composite = total_composite / n if n else 0.0

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_sw_composite": round(avg_composite * 10) / 10,
            "sw_crisis_count": sw_crisis_count,
            "sw_intervention_count": sw_intervention_count,
            "avg_allocation_score": round(total_allocation / n * 10) / 10 if n else 0.0,
            "avg_governance_score": round(total_governance / n * 10) / 10 if n else 0.0,
            "avg_resilience_score": round(total_resilience / n * 10) / 10 if n else 0.0,
            "avg_mandate_score": round(total_mandate / n * 10) / 10 if n else 0.0,
            "avg_estimated_capital_risk_index": round(avg_composite / 100 * 10 * 100) / 100,
        }

    def run(self, entities: List[SovereignWealthInput]) -> Dict[str, Any]:
        results = [analyze_entity(e) for e in entities]
        summary = self.analyze(entities)
        return {
            "entities": [r.to_dict() for r in results],
            "summary": summary,
        }
