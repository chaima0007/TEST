"""
Module 324 — Longevity Tech & Anti-Aging Economy Intelligence Engine
Caelum Partners — Chaima Mhadbi, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class LongevityTechInput:
    entity_id: str
    longevity_sector: str
    region: str
    # 17 float fields (0.0–1.0)
    senolytic_therapy_access_inequality: float
    epigenetic_reprogramming_risk: float
    longevity_wealth_concentration: float
    healthcare_system_disruption_rate: float
    pension_system_longevity_shock: float
    intergenerational_resource_conflict: float
    immortality_elite_emergence_risk: float
    regulatory_approval_gap: float
    bioethics_framework_deficit: float
    longevity_data_sovereignty_risk: float
    anti_aging_inequality_index: float
    youth_labor_market_displacement: float
    democratic_longevity_governance_gap: float
    biotech_monopoly_formation: float
    longevity_economy_transition_speed: float
    social_cohesion_longevity_tension: float
    longevity_misinformation_exposure: float


@dataclass
class LongevityTechResult:
    entity_id: str
    region: str
    longevity_sector: str
    longevity_risk: str
    longevity_pattern: str
    longevity_severity: str
    recommended_action: str
    access_score: float
    disruption_score: float
    governance_score: float
    societal_score: float
    longevity_composite: float
    is_longevity_crisis: bool
    requires_longevity_intervention: bool
    longevity_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "longevity_sector": self.longevity_sector,
            "longevity_risk": self.longevity_risk,
            "longevity_pattern": self.longevity_pattern,
            "longevity_severity": self.longevity_severity,
            "recommended_action": self.recommended_action,
            "access_score": self.access_score,
            "disruption_score": self.disruption_score,
            "governance_score": self.governance_score,
            "societal_score": self.societal_score,
            "longevity_composite": self.longevity_composite,
            "is_longevity_crisis": self.is_longevity_crisis,
            "requires_longevity_intervention": self.requires_longevity_intervention,
            "longevity_signal": self.longevity_signal,
        }


def _access_score(inp: LongevityTechInput) -> float:
    raw = (
        inp.senolytic_therapy_access_inequality * 0.4
        + inp.anti_aging_inequality_index * 0.35
        + inp.longevity_wealth_concentration * 0.25
    ) * 100
    return round(raw * 100) / 100


def _disruption_score(inp: LongevityTechInput) -> float:
    raw = (
        inp.healthcare_system_disruption_rate * 0.4
        + inp.pension_system_longevity_shock * 0.35
        + inp.longevity_economy_transition_speed * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(inp: LongevityTechInput) -> float:
    raw = (
        inp.regulatory_approval_gap * 0.4
        + inp.bioethics_framework_deficit * 0.35
        + inp.democratic_longevity_governance_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _societal_score(inp: LongevityTechInput) -> float:
    raw = (
        inp.immortality_elite_emergence_risk * 0.4
        + inp.intergenerational_resource_conflict * 0.35
        + inp.social_cohesion_longevity_tension * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    access: float,
    disruption: float,
    governance: float,
    societal: float,
) -> float:
    return round(
        access * 0.30
        + disruption * 0.25
        + governance * 0.25
        + societal * 0.20,
        2,
    )


def _longevity_pattern(inp: LongevityTechInput) -> str:
    if inp.senolytic_therapy_access_inequality >= 0.70 and inp.longevity_wealth_concentration >= 0.65:
        return "immortality_apartheid"
    if inp.healthcare_system_disruption_rate >= 0.70 and inp.pension_system_longevity_shock >= 0.65:
        return "system_collapse_shock"
    if inp.biotech_monopoly_formation >= 0.70 and inp.longevity_data_sovereignty_risk >= 0.65:
        return "biotech_monopoly"
    if inp.regulatory_approval_gap >= 0.70 and inp.bioethics_framework_deficit >= 0.65:
        return "governance_vacuum"
    if inp.intergenerational_resource_conflict >= 0.70 and inp.youth_labor_market_displacement >= 0.65:
        return "intergenerational_war"
    return "none"


def _longevity_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _longevity_severity(composite: float) -> str:
    if composite >= 75:
        return "longevity_emergency"
    if composite >= 50:
        return "high_longevity_disruption"
    if composite >= 25:
        return "longevity_tension"
    return "longevity_managed"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "longevity_emergency_governance"
    if risk == "high" and pattern == "immortality_apartheid":
        return "universal_longevity_access"
    if risk == "high":
        return "longevity_transition_framework"
    if risk == "moderate":
        return "longevity_monitoring"
    return "no_action"


def _longevity_signal(
    inp: LongevityTechInput, risk: str, composite: float, access_score: float
) -> str:
    if risk == "critical":
        return (
            f"Critique — apartheid de l'immortalité émergent — inégalité d'accès {access_score:.0f}%"
            f" — composite {composite:.1f}"
        )
    if risk == "high":
        return (
            f"Élevé — disruption système longévité {int(inp.healthcare_system_disruption_rate * 100)}%"
            f" — lacune gouvernance {int(inp.regulatory_approval_gap * 100)}%"
            f" — composite {composite:.1f}"
        )
    if risk == "moderate":
        return (
            f"Modéré — tension sociale longévité {int(inp.social_cohesion_longevity_tension * 100)}%"
            f" — composite {composite:.1f}"
        )
    return (
        "Technologie longévité gérée — accès équitable, gouvernance solide, cohésion sociale préservée"
    )


def analyze(inp: LongevityTechInput) -> LongevityTechResult:
    access = _access_score(inp)
    disruption = _disruption_score(inp)
    governance = _governance_score(inp)
    societal = _societal_score(inp)
    comp = _composite(access, disruption, governance, societal)
    pattern = _longevity_pattern(inp)
    risk = _longevity_risk(comp)
    severity = _longevity_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _longevity_signal(inp, risk, comp, access)

    return LongevityTechResult(
        entity_id=inp.entity_id,
        region=inp.region,
        longevity_sector=inp.longevity_sector,
        longevity_risk=risk,
        longevity_pattern=pattern,
        longevity_severity=severity,
        recommended_action=action,
        access_score=access,
        disruption_score=disruption,
        governance_score=governance,
        societal_score=societal,
        longevity_composite=comp,
        is_longevity_crisis=comp >= 60,
        requires_longevity_intervention=comp >= 40,
        longevity_signal=signal,
    )


class LongevityTechEngine:
    def analyze(self, entities: List[LongevityTechInput]) -> Dict[str, Any]:
        results = [analyze(inp) for inp in entities]
        n = len(results)
        if n == 0:
            return {}

        critical = sum(1 for r in results if r.longevity_risk == "critical")
        high = sum(1 for r in results if r.longevity_risk == "high")
        moderate = sum(1 for r in results if r.longevity_risk == "moderate")
        low = sum(1 for r in results if r.longevity_risk == "low")
        intervention = sum(1 for r in results if r.requires_longevity_intervention)
        crisis = sum(1 for r in results if r.is_longevity_crisis)

        avg_access = round(sum(r.access_score for r in results) / n, 2)
        avg_disruption = round(sum(r.disruption_score for r in results) / n, 2)
        avg_governance = round(sum(r.governance_score for r in results) / n, 2)
        avg_societal = round(sum(r.societal_score for r in results) / n, 2)
        avg_composite = round(sum(r.longevity_composite for r in results) / n, 2)

        return {
            "total_entities": n,
            "critical_entities": critical,
            "high_entities": high,
            "moderate_entities": moderate,
            "low_entities": low,
            "entities_requiring_intervention": intervention,
            "longevity_crisis_entities": crisis,
            "avg_access_score": avg_access,
            "avg_disruption_score": avg_disruption,
            "avg_governance_score": avg_governance,
            "avg_societal_score": avg_societal,
            "avg_longevity_composite": avg_composite,
            "avg_estimated_longevity_disruption_index": round(avg_composite / 100 * 10, 2),
        }
