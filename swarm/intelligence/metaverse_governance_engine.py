from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MetaverseGovernanceInput:
    entity_id: str
    platform_type: str
    region: str
    platform_concentration: float
    user_lock_in: float
    virtual_labor_rights: float
    economic_extraction: float
    identity_exploitation: float
    biometric_harvesting: float
    addiction_mechanics: float
    minor_exposure: float
    psychological_manipulation: float
    interoperability_barrier: float
    regulatory_gap: float
    tax_avoidance: float
    virtual_crime_rate: float
    property_rights_clarity: float
    content_moderation_failure: float
    environmental_footprint: float
    wealth_inequality_virtual: float


@dataclass
class MetaverseGovernanceResult:
    entity_id: str
    platform_type: str
    region: str
    monopoly_score: float
    exploitation_score: float
    identity_score: float
    addiction_score: float
    composite_score: float
    risk_level: str
    metaverse_pattern: str
    severity: str
    recommended_action: str
    signal: str
    platform_concentration: float
    regulatory_gap: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "platform_type": self.platform_type,
            "region": self.region,
            "monopoly_score": self.monopoly_score,
            "exploitation_score": self.exploitation_score,
            "identity_score": self.identity_score,
            "addiction_score": self.addiction_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "metaverse_pattern": self.metaverse_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "platform_concentration": self.platform_concentration,
            "regulatory_gap": self.regulatory_gap,
        }


def _monopoly_score(e: MetaverseGovernanceInput) -> float:
    raw = (
        e.platform_concentration * 0.40
        + e.user_lock_in * 0.35
        + e.interoperability_barrier * 0.25
    ) * 100
    return round(raw * 100) / 100


def _exploitation_score(e: MetaverseGovernanceInput) -> float:
    raw = (
        e.virtual_labor_rights * 0.40
        + e.economic_extraction * 0.35
        + e.wealth_inequality_virtual * 0.25
    ) * 100
    return round(raw * 100) / 100


def _identity_score(e: MetaverseGovernanceInput) -> float:
    raw = (
        e.identity_exploitation * 0.40
        + e.biometric_harvesting * 0.35
        + e.tax_avoidance * 0.25
    ) * 100
    return round(raw * 100) / 100


def _addiction_score(e: MetaverseGovernanceInput) -> float:
    raw = (
        e.addiction_mechanics * 0.40
        + e.minor_exposure * 0.35
        + e.psychological_manipulation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    monopoly: float,
    exploitation: float,
    identity: float,
    addiction: float,
) -> float:
    return round(
        (monopoly * 0.30 + exploitation * 0.25 + identity * 0.25 + addiction * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _metaverse_pattern(e: MetaverseGovernanceInput) -> str:
    if e.platform_concentration > 0.85 and e.user_lock_in > 0.80:
        return "platform_monopoly_capture"
    if e.virtual_labor_rights > 0.85 and e.economic_extraction > 0.80:
        return "virtual_labor_exploitation"
    if e.identity_exploitation > 0.85 and e.biometric_harvesting > 0.80:
        return "identity_data_colonialism"
    if e.addiction_mechanics > 0.85 and e.minor_exposure > 0.80:
        return "addiction_by_design_crisis"
    if e.regulatory_gap > 0.80 and e.tax_avoidance > 0.75:
        return "regulatory_jurisdiction_vacuum"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_gouvernance_métavers_systémique"
    if composite >= 40:
        return "crise_économie_virtuelle_majeure"
    if composite >= 20:
        return "déséquilibre_pouvoir_numérique_structurel"
    return "surveillance_métavers_active"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_régulation_métavers_critique"
    if risk == "high":
        return "réforme_accélérée_économie_virtuelle_exploitée"
    if risk == "moderate":
        return "renforcement_gouvernance_numérique_mondiale"
    return "veille_métavers_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise gouvernance métavers systémique — souveraineté numérique en péril"
    if risk == "high":
        return "🟠 Crise économie virtuelle majeure détectée"
    if risk == "moderate":
        return "🟡 Déséquilibre pouvoir numérique structurel actif"
    return "🟢 Métavers sous surveillance active"


def analyze_metaverse_governance(e: MetaverseGovernanceInput) -> MetaverseGovernanceResult:
    monopoly = _monopoly_score(e)
    exploitation = _exploitation_score(e)
    identity = _identity_score(e)
    addiction = _addiction_score(e)
    composite = _composite_score(monopoly, exploitation, identity, addiction)
    risk = _risk_level(composite)
    pattern = _metaverse_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return MetaverseGovernanceResult(
        entity_id=e.entity_id,
        platform_type=e.platform_type,
        region=e.region,
        monopoly_score=monopoly,
        exploitation_score=exploitation,
        identity_score=identity,
        addiction_score=addiction,
        composite_score=composite,
        risk_level=risk,
        metaverse_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        platform_concentration=e.platform_concentration,
        regulatory_gap=e.regulatory_gap,
    )


class MetaverseGovernanceEngine:
    def analyze(self, entities: List[MetaverseGovernanceInput]) -> Dict[str, Any]:
        results = [analyze_metaverse_governance(e) for e in entities]

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
            pattern_distribution[r.metaverse_pattern] = pattern_distribution.get(r.metaverse_pattern, 0) + 1
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
        results: List[MetaverseGovernanceResult] = None,
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
            "module_id": 400,
            "module_name": "Gouvernance Métavers & Économie Monde Virtuel Intelligence Engine",
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
            "avg_estimated_metaverse_governance_index": round(avg_composite / 100 * 10, 2),
        }
