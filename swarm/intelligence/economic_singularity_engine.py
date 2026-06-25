"""
Module 315 — Economic Singularity Simulation Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles

Models and detects economic systems approaching phase-transition singularities
where conventional economic rules break down due to accelerating AI/automation.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class EconomicSingularityInput:
    entity_id: str
    economy_type: str
    region: str
    # 17 float fields (0.0–1.0)
    ai_labor_displacement_velocity: float
    productivity_growth_acceleration: float
    capital_concentration_rate: float
    conventional_rule_breakdown_index: float
    automation_penetration_depth: float
    economic_phase_transition_proximity: float
    value_creation_redistribution_gap: float
    post_scarcity_emergence_index: float
    human_economic_relevance_erosion: float
    institutional_adaptation_lag: float
    winner_take_all_intensification: float
    economic_complexity_explosion: float
    regulatory_obsolescence_rate: float
    monetary_system_stress: float
    social_contract_dissolution_risk: float
    new_economy_emergence_rate: float
    singularity_resistance_capacity: float  # inverse: high = good


@dataclass
class EconomicSingularityResult:
    entity_id: str
    region: str
    economy_type: str
    singularity_risk: str
    singularity_pattern: str
    singularity_severity: str
    recommended_action: str
    displacement_score: float
    transition_score: float
    concentration_score: float
    disruption_score: float
    singularity_composite: float
    is_singularity_crisis: bool
    requires_singularity_intervention: bool
    singularity_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id":                        self.entity_id,
            "region":                           self.region,
            "economy_type":                     self.economy_type,
            "singularity_risk":                 self.singularity_risk,
            "singularity_pattern":              self.singularity_pattern,
            "singularity_severity":             self.singularity_severity,
            "recommended_action":               self.recommended_action,
            "displacement_score":               self.displacement_score,
            "transition_score":                 self.transition_score,
            "concentration_score":              self.concentration_score,
            "disruption_score":                 self.disruption_score,
            "singularity_composite":            self.singularity_composite,
            "is_singularity_crisis":            self.is_singularity_crisis,
            "requires_singularity_intervention": self.requires_singularity_intervention,
            "singularity_signal":               self.singularity_signal,
        }


# ── Sub-scores ──────────────────────────────────────────────────────────────

def _displacement_score(i: EconomicSingularityInput) -> float:
    raw = (
        i.ai_labor_displacement_velocity * 0.40
        + i.human_economic_relevance_erosion * 0.35
        + i.automation_penetration_depth * 0.25
    ) * 100
    return round(raw * 100) / 100


def _transition_score(i: EconomicSingularityInput) -> float:
    raw = (
        i.economic_phase_transition_proximity * 0.40
        + i.conventional_rule_breakdown_index * 0.35
        + i.institutional_adaptation_lag * 0.25
    ) * 100
    return round(raw * 100) / 100


def _concentration_score(i: EconomicSingularityInput) -> float:
    raw = (
        i.capital_concentration_rate * 0.40
        + i.winner_take_all_intensification * 0.35
        + i.value_creation_redistribution_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _disruption_score(i: EconomicSingularityInput) -> float:
    raw = (
        i.regulatory_obsolescence_rate * 0.40
        + i.social_contract_dissolution_risk * 0.35
        + (1 - i.singularity_resistance_capacity) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(disp: float, trans: float, conc: float, disrup: float) -> float:
    return round(
        min(disp * 0.30 + trans * 0.25 + conc * 0.25 + disrup * 0.20, 100.0),
        2,
    )


# ── Risk / severity ──────────────────────────────────────────────────────────

def _risk(c: float) -> str:
    if c >= 60: return "critical"
    if c >= 40: return "high"
    if c >= 20: return "moderate"
    return "low"


def _severity(c: float) -> str:
    if c >= 75: return "singularity_imminent"
    if c >= 50: return "phase_transition_critical"
    if c >= 25: return "singularity_approaching"
    return "pre_acceleration"


# ── Pattern detection ────────────────────────────────────────────────────────

def _pattern(i: EconomicSingularityInput) -> str:
    if (i.economic_phase_transition_proximity >= 0.70
            and i.conventional_rule_breakdown_index >= 0.65):
        return "singularity_threshold_breach"
    if (i.ai_labor_displacement_velocity >= 0.70
            and i.human_economic_relevance_erosion >= 0.65):
        return "labor_extinction_event"
    if (i.capital_concentration_rate >= 0.70
            and i.winner_take_all_intensification >= 0.65):
        return "capital_hypercentralization"
    if (i.institutional_adaptation_lag >= 0.70
            and i.regulatory_obsolescence_rate >= 0.65):
        return "institutional_collapse"
    if (i.social_contract_dissolution_risk >= 0.70
            and i.value_creation_redistribution_gap >= 0.65):
        return "social_contract_rupture"
    return "none"


# ── Action selection ─────────────────────────────────────────────────────────

def _action(risk: str, pat: str) -> str:
    if risk == "critical":
        return "emergency_economic_redesign"
    if risk == "high":
        if pat == "labor_extinction_event":
            return "universal_income_emergency"
        return "singularity_transition_program"
    if risk == "moderate":
        return "economic_monitoring"
    return "no_action"


# ── French signal ────────────────────────────────────────────────────────────

def _signal(i: EconomicSingularityInput, risk: str, comp: float) -> str:
    if risk == "critical":
        return (
            f"Critique — singularité économique imminente — "
            f"déplacement travail {round(i.ai_labor_displacement_velocity * 100)}% — "
            f"transition de phase — composite {round(comp)}"
        )
    if risk == "high":
        return (
            f"Élevé — accélération singularité — "
            f"déplacement travail {round(i.ai_labor_displacement_velocity * 100)}% — "
            f"concentration capital {round(i.capital_concentration_rate * 100)}% — "
            f"composite {round(comp)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — proximité transition économique {round(i.economic_phase_transition_proximity * 100)}% — "
            f"composite {round(comp)}"
        )
    return (
        "Économie résiliente — règles conventionnelles stables, singularité lointaine, "
        "capacité d'adaptation institutionnelle préservée"
    )


# ── Core analysis function ───────────────────────────────────────────────────

def analyze(i: EconomicSingularityInput) -> EconomicSingularityResult:
    disp  = _displacement_score(i)
    trans = _transition_score(i)
    conc  = _concentration_score(i)
    disrup = _disruption_score(i)
    comp  = _composite(disp, trans, conc, disrup)
    risk  = _risk(comp)
    sev   = _severity(comp)
    pat   = _pattern(i)
    act   = _action(risk, pat)
    sig   = _signal(i, risk, comp)

    return EconomicSingularityResult(
        entity_id=i.entity_id,
        region=i.region,
        economy_type=i.economy_type,
        singularity_risk=risk,
        singularity_pattern=pat,
        singularity_severity=sev,
        recommended_action=act,
        displacement_score=disp,
        transition_score=trans,
        concentration_score=conc,
        disruption_score=disrup,
        singularity_composite=comp,
        is_singularity_crisis=comp >= 60,
        requires_singularity_intervention=comp >= 40,
        singularity_signal=sig,
    )


# ── Engine ────────────────────────────────────────────────────────────────────

class EconomicSingularityEngine:
    def __init__(self) -> None:
        self.results: List[EconomicSingularityResult] = []

    def simulate(self, entities: List[EconomicSingularityInput]) -> Dict[str, Any]:
        self.results = [analyze(i) for i in entities]
        n = len(self.results)
        if n == 0:
            return {}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_displacement = 0.0
        total_transition = 0.0
        total_concentration = 0.0
        total_disruption = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in self.results:
            risk_counts[r.singularity_risk]       = risk_counts.get(r.singularity_risk, 0) + 1
            pattern_counts[r.singularity_pattern] = pattern_counts.get(r.singularity_pattern, 0) + 1
            severity_counts[r.singularity_severity] = severity_counts.get(r.singularity_severity, 0) + 1
            action_counts[r.recommended_action]   = action_counts.get(r.recommended_action, 0) + 1

            total_composite    += r.singularity_composite
            total_displacement += r.displacement_score
            total_transition   += r.transition_score
            total_concentration += r.concentration_score
            total_disruption   += r.disruption_score

            if r.is_singularity_crisis:           crisis_count += 1
            if r.requires_singularity_intervention: intervention_count += 1

        avg_composite = round(total_composite / n * 10) / 10

        return {
            "total":                                  n,
            "risk_counts":                            risk_counts,
            "pattern_counts":                         pattern_counts,
            "severity_counts":                        severity_counts,
            "action_counts":                          action_counts,
            "avg_singularity_composite":              avg_composite,
            "singularity_crisis_count":               crisis_count,
            "singularity_intervention_count":         intervention_count,
            "avg_displacement_score":                 round(total_displacement / n * 10) / 10,
            "avg_transition_score":                   round(total_transition / n * 10) / 10,
            "avg_concentration_score":                round(total_concentration / n * 10) / 10,
            "avg_disruption_score":                   round(total_disruption / n * 10) / 10,
            "avg_estimated_singularity_proximity_index": round(avg_composite / 100 * 10, 2),
        }


# ── Mock data ─────────────────────────────────────────────────────────────────

MOCK_ENTITIES = [
    # ESI-001: EMEA, advanced_economy → critical, singularity_threshold_breach
    EconomicSingularityInput(
        entity_id="ESI-001", economy_type="advanced_economy", region="EMEA",
        ai_labor_displacement_velocity=0.80,
        productivity_growth_acceleration=0.75,
        capital_concentration_rate=0.72,
        conventional_rule_breakdown_index=0.68,
        automation_penetration_depth=0.70,
        economic_phase_transition_proximity=0.78,
        value_creation_redistribution_gap=0.65,
        post_scarcity_emergence_index=0.60,
        human_economic_relevance_erosion=0.72,
        institutional_adaptation_lag=0.62,
        winner_take_all_intensification=0.70,
        economic_complexity_explosion=0.68,
        regulatory_obsolescence_rate=0.60,
        monetary_system_stress=0.65,
        social_contract_dissolution_risk=0.62,
        new_economy_emergence_rate=0.70,
        singularity_resistance_capacity=0.25,
    ),
    # ESI-002: APAC, emerging_economy → low, none
    EconomicSingularityInput(
        entity_id="ESI-002", economy_type="emerging_economy", region="APAC",
        ai_labor_displacement_velocity=0.15,
        productivity_growth_acceleration=0.45,
        capital_concentration_rate=0.22,
        conventional_rule_breakdown_index=0.18,
        automation_penetration_depth=0.20,
        economic_phase_transition_proximity=0.12,
        value_creation_redistribution_gap=0.20,
        post_scarcity_emergence_index=0.30,
        human_economic_relevance_erosion=0.15,
        institutional_adaptation_lag=0.18,
        winner_take_all_intensification=0.20,
        economic_complexity_explosion=0.25,
        regulatory_obsolescence_rate=0.15,
        monetary_system_stress=0.20,
        social_contract_dissolution_risk=0.18,
        new_economy_emergence_rate=0.35,
        singularity_resistance_capacity=0.80,
    ),
    # ESI-003: NOAM, tech_economy → high, labor_extinction_event
    EconomicSingularityInput(
        entity_id="ESI-003", economy_type="tech_economy", region="NOAM",
        ai_labor_displacement_velocity=0.75,
        productivity_growth_acceleration=0.80,
        capital_concentration_rate=0.55,
        conventional_rule_breakdown_index=0.48,
        automation_penetration_depth=0.70,
        economic_phase_transition_proximity=0.50,
        value_creation_redistribution_gap=0.55,
        post_scarcity_emergence_index=0.60,
        human_economic_relevance_erosion=0.68,
        institutional_adaptation_lag=0.45,
        winner_take_all_intensification=0.58,
        economic_complexity_explosion=0.60,
        regulatory_obsolescence_rate=0.50,
        monetary_system_stress=0.45,
        social_contract_dissolution_risk=0.52,
        new_economy_emergence_rate=0.75,
        singularity_resistance_capacity=0.40,
    ),
    # ESI-004: LATAM, developing_economy → low, none
    EconomicSingularityInput(
        entity_id="ESI-004", economy_type="developing_economy", region="LATAM",
        ai_labor_displacement_velocity=0.12,
        productivity_growth_acceleration=0.28,
        capital_concentration_rate=0.18,
        conventional_rule_breakdown_index=0.14,
        automation_penetration_depth=0.10,
        economic_phase_transition_proximity=0.10,
        value_creation_redistribution_gap=0.15,
        post_scarcity_emergence_index=0.12,
        human_economic_relevance_erosion=0.10,
        institutional_adaptation_lag=0.12,
        winner_take_all_intensification=0.14,
        economic_complexity_explosion=0.12,
        regulatory_obsolescence_rate=0.10,
        monetary_system_stress=0.15,
        social_contract_dissolution_risk=0.12,
        new_economy_emergence_rate=0.18,
        singularity_resistance_capacity=0.88,
    ),
    # ESI-005: MEA, resource_economy → critical, institutional_collapse
    EconomicSingularityInput(
        entity_id="ESI-005", economy_type="resource_economy", region="MEA",
        ai_labor_displacement_velocity=0.65,
        productivity_growth_acceleration=0.55,
        capital_concentration_rate=0.68,
        conventional_rule_breakdown_index=0.62,
        automation_penetration_depth=0.60,
        economic_phase_transition_proximity=0.65,
        value_creation_redistribution_gap=0.60,
        post_scarcity_emergence_index=0.40,
        human_economic_relevance_erosion=0.58,
        institutional_adaptation_lag=0.75,
        winner_take_all_intensification=0.60,
        economic_complexity_explosion=0.55,
        regulatory_obsolescence_rate=0.70,
        monetary_system_stress=0.65,
        social_contract_dissolution_risk=0.60,
        new_economy_emergence_rate=0.45,
        singularity_resistance_capacity=0.22,
    ),
    # ESI-006: EMEA, industrial_economy → moderate, none
    EconomicSingularityInput(
        entity_id="ESI-006", economy_type="industrial_economy", region="EMEA",
        ai_labor_displacement_velocity=0.38,
        productivity_growth_acceleration=0.42,
        capital_concentration_rate=0.35,
        conventional_rule_breakdown_index=0.30,
        automation_penetration_depth=0.42,
        economic_phase_transition_proximity=0.32,
        value_creation_redistribution_gap=0.38,
        post_scarcity_emergence_index=0.35,
        human_economic_relevance_erosion=0.30,
        institutional_adaptation_lag=0.35,
        winner_take_all_intensification=0.32,
        economic_complexity_explosion=0.38,
        regulatory_obsolescence_rate=0.35,
        monetary_system_stress=0.30,
        social_contract_dissolution_risk=0.35,
        new_economy_emergence_rate=0.40,
        singularity_resistance_capacity=0.62,
    ),
    # ESI-007: APAC, platform_economy → high, capital_hypercentralization
    EconomicSingularityInput(
        entity_id="ESI-007", economy_type="platform_economy", region="APAC",
        ai_labor_displacement_velocity=0.55,
        productivity_growth_acceleration=0.68,
        capital_concentration_rate=0.78,
        conventional_rule_breakdown_index=0.50,
        automation_penetration_depth=0.60,
        economic_phase_transition_proximity=0.52,
        value_creation_redistribution_gap=0.60,
        post_scarcity_emergence_index=0.55,
        human_economic_relevance_erosion=0.50,
        institutional_adaptation_lag=0.45,
        winner_take_all_intensification=0.72,
        economic_complexity_explosion=0.62,
        regulatory_obsolescence_rate=0.48,
        monetary_system_stress=0.50,
        social_contract_dissolution_risk=0.52,
        new_economy_emergence_rate=0.65,
        singularity_resistance_capacity=0.35,
    ),
    # ESI-008: NOAM, digital_economy → critical, social_contract_rupture
    EconomicSingularityInput(
        entity_id="ESI-008", economy_type="digital_economy", region="NOAM",
        ai_labor_displacement_velocity=0.65,   # <0.70 so labor_extinction_event won't fire first
        productivity_growth_acceleration=0.82,
        capital_concentration_rate=0.60,       # <0.70 so capital_hypercentralization won't fire
        conventional_rule_breakdown_index=0.55,
        automation_penetration_depth=0.75,
        economic_phase_transition_proximity=0.60,
        value_creation_redistribution_gap=0.72,
        post_scarcity_emergence_index=0.65,
        human_economic_relevance_erosion=0.60,  # <0.65 so labor_extinction won't fire
        institutional_adaptation_lag=0.55,
        winner_take_all_intensification=0.60,
        economic_complexity_explosion=0.72,
        regulatory_obsolescence_rate=0.62,
        monetary_system_stress=0.68,
        social_contract_dissolution_risk=0.78,
        new_economy_emergence_rate=0.75,
        singularity_resistance_capacity=0.18,
    ),
]


if __name__ == "__main__":
    engine = EconomicSingularityEngine()
    summary = engine.simulate(MOCK_ENTITIES)
    for r in engine.results:
        d = r.to_dict()
        print(
            f"{d['entity_id']} | {d['singularity_risk']:8s} | "
            f"{d['singularity_pattern']:30s} | composite={d['singularity_composite']:.1f}"
        )
    print("\nSummary:", summary)
