"""
Module 322 — Techno-Féodalisme & Concentration Pouvoir Plateformes
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class TechnoFeudalismInput:
    entity_id: str
    platform_domain: str
    region: str
    # 17 float fields (0.0–1.0)
    platform_market_capture: float
    cloud_rent_extraction_rate: float
    data_feudal_rent_index: float
    digital_labor_exploitation_rate: float
    api_dependency_lock_in: float
    algorithmic_sovereignty_erosion: float
    gatekeeper_tax_burden: float
    network_effect_moat_strength: float
    surveillance_capitalism_depth: float
    digital_commons_enclosure_rate: float
    platform_worker_precarity: float
    sovereign_cloud_dependency: float
    content_moderation_power: float
    antitrust_evasion_sophistication: float
    digital_exit_barrier_height: float
    small_business_platform_dependency: float
    innovation_tax_to_gatekeeper: float


@dataclass
class TechnoFeudalismResult:
    entity_id: str
    region: str
    platform_domain: str
    feudal_risk: str
    feudal_pattern: str
    feudal_severity: str
    recommended_action: str
    capture_score: float
    rent_score: float
    dependency_score: float
    sovereignty_score: float
    feudal_composite: float
    is_feudal_crisis: bool
    requires_feudal_intervention: bool
    feudal_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "platform_domain": self.platform_domain,
            "feudal_risk": self.feudal_risk,
            "feudal_pattern": self.feudal_pattern,
            "feudal_severity": self.feudal_severity,
            "recommended_action": self.recommended_action,
            "capture_score": self.capture_score,
            "rent_score": self.rent_score,
            "dependency_score": self.dependency_score,
            "sovereignty_score": self.sovereignty_score,
            "feudal_composite": self.feudal_composite,
            "is_feudal_crisis": self.is_feudal_crisis,
            "requires_feudal_intervention": self.requires_feudal_intervention,
            "feudal_signal": self.feudal_signal,
        }


def _capture_score(inp: TechnoFeudalismInput) -> float:
    raw = (
        inp.platform_market_capture * 0.4
        + inp.network_effect_moat_strength * 0.35
        + inp.gatekeeper_tax_burden * 0.25
    ) * 100
    return round(raw * 100) / 100


def _rent_score(inp: TechnoFeudalismInput) -> float:
    raw = (
        inp.data_feudal_rent_index * 0.4
        + inp.cloud_rent_extraction_rate * 0.35
        + inp.innovation_tax_to_gatekeeper * 0.25
    ) * 100
    return round(raw * 100) / 100


def _dependency_score(inp: TechnoFeudalismInput) -> float:
    raw = (
        inp.api_dependency_lock_in * 0.4
        + inp.digital_exit_barrier_height * 0.35
        + inp.small_business_platform_dependency * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sovereignty_score(inp: TechnoFeudalismInput) -> float:
    raw = (
        inp.algorithmic_sovereignty_erosion * 0.4
        + inp.sovereign_cloud_dependency * 0.35
        + inp.digital_commons_enclosure_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    capture: float,
    rent: float,
    dependency: float,
    sovereignty: float,
) -> float:
    return round(
        capture * 0.30
        + rent * 0.25
        + dependency * 0.25
        + sovereignty * 0.20,
        2,
    )


def _feudal_pattern(inp: TechnoFeudalismInput) -> str:
    if inp.platform_market_capture >= 0.70 and inp.gatekeeper_tax_burden >= 0.65:
        return "monopoly_feudalism"
    if inp.data_feudal_rent_index >= 0.70 and inp.surveillance_capitalism_depth >= 0.65:
        return "data_serfdom"
    if inp.sovereign_cloud_dependency >= 0.70 and inp.api_dependency_lock_in >= 0.65:
        return "cloud_colonialism"
    if inp.digital_commons_enclosure_rate >= 0.70 and inp.digital_exit_barrier_height >= 0.65:
        return "digital_enclosure"
    if inp.digital_labor_exploitation_rate >= 0.70 and inp.platform_worker_precarity >= 0.65:
        return "worker_feudalization"
    return "none"


def _feudal_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _feudal_severity(composite: float) -> str:
    if composite >= 75:
        return "feudal_emergency"
    if composite >= 50:
        return "high_feudalization"
    if composite >= 25:
        return "feudal_dynamics_emerging"
    return "digital_commons_healthy"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "antitrust_emergency_action"
    if risk == "high" and pattern == "cloud_colonialism":
        return "sovereign_cloud_program"
    if risk == "high":
        return "platform_regulation"
    if risk == "moderate":
        return "market_monitoring"
    return "no_action"


def _feudal_signal(inp: TechnoFeudalismInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — capture marché plateforme {int(inp.platform_market_capture * 100)}% "
            f"— rente féodale données {int(inp.data_feudal_rent_index * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — dépendance cloud souverain {int(inp.sovereign_cloud_dependency * 100)}% "
            f"— verrouillage API {int(inp.api_dependency_lock_in * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — enclosure communs numériques {int(inp.digital_commons_enclosure_rate * 100)}% "
            f"— composite {int(composite)}"
        )
    return "Communs numériques florissants — concurrence saine, souveraineté préservée, plateformes équilibrées"


def analyze(inp: TechnoFeudalismInput) -> TechnoFeudalismResult:
    cap = _capture_score(inp)
    rent = _rent_score(inp)
    dep = _dependency_score(inp)
    sov = _sovereignty_score(inp)
    comp = _composite(cap, rent, dep, sov)
    pat = _feudal_pattern(inp)
    risk = _feudal_risk(comp)
    sev = _feudal_severity(comp)
    action = _recommended_action(risk, pat)
    sig = _feudal_signal(inp, risk, comp)

    return TechnoFeudalismResult(
        entity_id=inp.entity_id,
        region=inp.region,
        platform_domain=inp.platform_domain,
        feudal_risk=risk,
        feudal_pattern=pat,
        feudal_severity=sev,
        recommended_action=action,
        capture_score=cap,
        rent_score=rent,
        dependency_score=dep,
        sovereignty_score=sov,
        feudal_composite=comp,
        is_feudal_crisis=comp >= 60,
        requires_feudal_intervention=comp >= 40,
        feudal_signal=sig,
    )


class TechnoFeudalismEngine:
    def __init__(self, inputs: List[TechnoFeudalismInput]):
        self.inputs = inputs
        self.results: List[TechnoFeudalismResult] = [analyze(i) for i in inputs]

    def analyze(self, entities: List[TechnoFeudalismInput]) -> Dict[str, Any]:
        results = [analyze(e) for e in entities]
        return self._summarize(results)

    def summary(self) -> Dict[str, Any]:
        return self._summarize(self.results)

    def _summarize(self, results: List[TechnoFeudalismResult]) -> Dict[str, Any]:
        n = len(results)
        if n == 0:
            return {}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_capture = 0.0
        total_rent = 0.0
        total_dependency = 0.0
        total_sovereignty = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.feudal_risk] = risk_counts.get(r.feudal_risk, 0) + 1
            pattern_counts[r.feudal_pattern] = pattern_counts.get(r.feudal_pattern, 0) + 1
            severity_counts[r.feudal_severity] = severity_counts.get(r.feudal_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1

            total_composite += r.feudal_composite
            total_capture += r.capture_score
            total_rent += r.rent_score
            total_dependency += r.dependency_score
            total_sovereignty += r.sovereignty_score

            if r.is_feudal_crisis:
                crisis_count += 1
            if r.requires_feudal_intervention:
                intervention_count += 1

        avg_composite = round(total_composite / n * 10) / 10

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_feudal_composite": avg_composite,
            "feudal_crisis_count": crisis_count,
            "feudal_intervention_count": intervention_count,
            "avg_capture_score": round(total_capture / n * 10) / 10,
            "avg_rent_score": round(total_rent / n * 10) / 10,
            "avg_dependency_score": round(total_dependency / n * 10) / 10,
            "avg_sovereignty_score": round(total_sovereignty / n * 10) / 10,
            "avg_estimated_feudalization_index": round(avg_composite / 100 * 10, 2),
        }
