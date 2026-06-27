from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class NuclearWasteInput:
    entity_id: str
    waste_category: str
    region: str
    containment_integrity: float
    repository_capacity: float
    geological_stability: float
    cooling_system_safety: float
    governance_effectiveness: float
    regulatory_independence: float
    transparency_index: float
    public_trust: float
    intergenerational_equity: float
    time_horizon_planning: float
    proliferation_risk: float
    security_measures: float
    transport_safety: float
    worker_exposure: float
    emergency_preparedness: float
    community_consent: float
    decommissioning_readiness: float


@dataclass
class NuclearWasteResult:
    entity_id: str
    waste_category: str
    region: str
    containment_score: float
    governance_score: float
    intergenerational_score: float
    proliferation_score: float
    composite_score: float
    risk_level: str
    nuclear_pattern: str
    severity: str
    recommended_action: str
    signal: str
    containment_integrity: float
    proliferation_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "waste_category": self.waste_category,
            "region": self.region,
            "containment_score": self.containment_score,
            "governance_score": self.governance_score,
            "intergenerational_score": self.intergenerational_score,
            "proliferation_score": self.proliferation_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "nuclear_pattern": self.nuclear_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "containment_integrity": self.containment_integrity,
            "proliferation_risk": self.proliferation_risk,
        }


def _containment_score(e: NuclearWasteInput) -> float:
    raw = (
        (1 - e.containment_integrity) * 0.4
        + (1 - e.repository_capacity) * 0.35
        + (1 - e.geological_stability) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: NuclearWasteInput) -> float:
    raw = (
        (1 - e.governance_effectiveness) * 0.4
        + (1 - e.regulatory_independence) * 0.35
        + (1 - e.transparency_index) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _intergenerational_score(e: NuclearWasteInput) -> float:
    raw = (
        (1 - e.intergenerational_equity) * 0.4
        + (1 - e.time_horizon_planning) * 0.35
        + (1 - e.community_consent) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _proliferation_score(e: NuclearWasteInput) -> float:
    raw = (
        e.proliferation_risk * 0.4
        + (1 - e.security_measures) * 0.35
        + (1 - e.transport_safety) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    containment: float,
    governance: float,
    intergenerational: float,
    proliferation: float,
) -> float:
    return round(
        (containment * 0.30 + governance * 0.25 + intergenerational * 0.25 + proliferation * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _nuclear_pattern(e: NuclearWasteInput) -> str:
    if e.containment_integrity < 0.15 and e.repository_capacity < 0.20:
        return "repository_failure_crisis"
    if e.intergenerational_equity < 0.15 and e.time_horizon_planning < 0.20:
        return "intergenerational_justice_void"
    if e.proliferation_risk > 0.85 and e.security_measures < 0.20:
        return "proliferation_leakage_risk"
    if e.regulatory_independence < 0.15 and e.governance_effectiveness < 0.20:
        return "regulatory_capture_collapse"
    if e.worker_exposure > 0.80 and e.decommissioning_readiness < 0.25:
        return "legacy_contamination_spread"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_nucléaire_sécurité_systémique"
    if composite >= 40:
        return "risque_gestion_déchets_majeur"
    if composite >= 20:
        return "surveillance_confinement_active"
    return "gestion_déchets_sous_contrôle"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_sécurité_nucléaire_critique"
    if risk == "high":
        return "renforcement_confinement_gouvernance_accéléré"
    if risk == "moderate":
        return "surveillance_renforcée_déchets_nucléaires"
    return "veille_sécurité_long_terme_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise nucléaire systémique — sécurité long-terme en péril immédiat"
    if risk == "high":
        return "🟠 Risque gestion déchets majeur détecté"
    if risk == "moderate":
        return "🟡 Surveillance confinement nucléaire active"
    return "🟢 Gestion déchets nucléaires sous contrôle"


def analyze_nuclear_waste(e: NuclearWasteInput) -> NuclearWasteResult:
    containment = _containment_score(e)
    governance = _governance_score(e)
    intergenerational = _intergenerational_score(e)
    proliferation = _proliferation_score(e)
    composite = _composite_score(containment, governance, intergenerational, proliferation)
    risk = _risk_level(composite)
    pattern = _nuclear_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return NuclearWasteResult(
        entity_id=e.entity_id,
        waste_category=e.waste_category,
        region=e.region,
        containment_score=containment,
        governance_score=governance,
        intergenerational_score=intergenerational,
        proliferation_score=proliferation,
        composite_score=composite,
        risk_level=risk,
        nuclear_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        containment_integrity=e.containment_integrity,
        proliferation_risk=e.proliferation_risk,
    )


class NuclearWasteEngine:
    def analyze(self, entities: List[NuclearWasteInput]) -> Dict[str, Any]:
        results = [analyze_nuclear_waste(e) for e in entities]

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            pattern_distribution[r.nuclear_pattern] = pattern_distribution.get(r.nuclear_pattern, 0) + 1
            severity_distribution[r.severity] = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action] = action_distribution.get(r.recommended_action, 0) + 1
            total_composite += r.composite_score
            if r.risk_level == "critical":
                critical_count += 1
            elif r.risk_level == "high":
                high_count += 1
            elif r.risk_level == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        n = len(results) or 1
        avg_composite = round(total_composite / n * 10) / 10

        return self.summary(
            results=results,
            risk_distribution=risk_distribution,
            pattern_distribution=pattern_distribution,
            severity_distribution=severity_distribution,
            action_distribution=action_distribution,
            avg_composite=avg_composite,
            critical_count=critical_count,
            high_count=high_count,
            moderate_count=moderate_count,
            low_count=low_count,
        )

    def summary(
        self,
        results: List[NuclearWasteResult] = None,
        risk_distribution: Dict[str, int] = None,
        pattern_distribution: Dict[str, int] = None,
        severity_distribution: Dict[str, int] = None,
        action_distribution: Dict[str, int] = None,
        avg_composite: float = 0.0,
        critical_count: int = 0,
        high_count: int = 0,
        moderate_count: int = 0,
        low_count: int = 0,
    ) -> Dict[str, Any]:
        results = results or []
        return {
            "module_id": 401,
            "module_name": "Gestion Déchets Nucléaires & Sécurité Long-Terme Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution or {},
            "risk_distribution": risk_distribution or {},
            "severity_distribution": severity_distribution or {},
            "action_distribution": action_distribution or {},
            "avg_estimated_nuclear_waste_index": round(avg_composite / 100 * 10, 2),
        }
