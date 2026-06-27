from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class WaterPrivatizationInput:
    entity_id: str
    water_system: str
    region: str
    private_control_share: float
    price_unaffordability: float
    access_inequality: float
    aquifer_depletion_rate: float
    corporate_extraction: float
    public_utility_divestment: float
    regulatory_capture: float
    treaty_compliance: float
    drought_frequency: float
    infrastructure_privatization: float
    community_rights_erosion: float
    indigenous_water_rights: float
    agricultural_monopoly: float
    investment_return_priority: float
    service_quality_decline: float
    tariff_shock_index: float
    cross_border_tension: float


@dataclass
class WaterPrivatizationResult:
    entity_id: str
    water_system: str
    region: str
    access_score: float
    privatization_score: float
    governance_score: float
    conflict_score: float
    composite_score: float
    risk_level: str
    water_pattern: str
    severity: str
    recommended_action: str
    signal: str
    private_control_share: float
    aquifer_depletion_rate: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "water_system": self.water_system,
            "region": self.region,
            "access_score": self.access_score,
            "privatization_score": self.privatization_score,
            "governance_score": self.governance_score,
            "conflict_score": self.conflict_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "water_pattern": self.water_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "private_control_share": self.private_control_share,
            "aquifer_depletion_rate": self.aquifer_depletion_rate,
        }


def _access_score(e: WaterPrivatizationInput) -> float:
    raw = (
        e.access_inequality * 0.4
        + e.price_unaffordability * 0.35
        + e.service_quality_decline * 0.25
    ) * 100
    return round(raw * 100) / 100


def _privatization_score(e: WaterPrivatizationInput) -> float:
    raw = (
        e.private_control_share * 0.4
        + e.infrastructure_privatization * 0.35
        + e.public_utility_divestment * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: WaterPrivatizationInput) -> float:
    raw = (
        e.regulatory_capture * 0.4
        + e.community_rights_erosion * 0.35
        + e.investment_return_priority * 0.25
    ) * 100
    return round(raw * 100) / 100


def _conflict_score(e: WaterPrivatizationInput) -> float:
    raw = (
        e.cross_border_tension * 0.4
        + e.treaty_compliance * 0.35
        + e.indigenous_water_rights * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    access: float,
    privatization: float,
    governance: float,
    conflict: float,
) -> float:
    return round(
        (access * 0.30 + privatization * 0.25 + governance * 0.25 + conflict * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _water_pattern(e: WaterPrivatizationInput) -> str:
    if e.private_control_share > 0.85 and e.public_utility_divestment > 0.80:
        return "corporate_water_monopoly"
    if e.price_unaffordability > 0.85 and e.tariff_shock_index > 0.80:
        return "affordability_crisis_collapse"
    if e.aquifer_depletion_rate > 0.85 and e.corporate_extraction > 0.80:
        return "aquifer_depletion_emergency"
    if e.cross_border_tension > 0.80 and e.treaty_compliance > 0.75:
        return "cross_border_water_conflict"
    if e.drought_frequency > 0.80 and e.agricultural_monopoly > 0.75:
        return "climate_water_scarcity_trap"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_privatisation_eau_systémique"
    if composite >= 40:
        return "crise_bien_commun_hydrique_majeure"
    if composite >= 20:
        return "inégalité_accès_eau_structurelle"
    return "accès_eau_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_remunicipalisation_eau_critique"
    if risk == "high":
        return "régulation_renforcée_tarifs_eau_communautés_vulnérables"
    if risk == "moderate":
        return "renforcement_gouvernance_bien_commun_hydrique"
    return "veille_accès_eau_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise privatisation eau systémique — bien commun hydrique en péril"
    if risk == "high":
        return "🟠 Crise bien commun hydrique majeure détectée"
    if risk == "moderate":
        return "🟡 Inégalité accès eau structurelle active"
    return "🟢 Accès eau sous surveillance"


def analyze_water_privatization(e: WaterPrivatizationInput) -> WaterPrivatizationResult:
    access = _access_score(e)
    privatization = _privatization_score(e)
    governance = _governance_score(e)
    conflict = _conflict_score(e)
    composite = _composite_score(access, privatization, governance, conflict)
    risk = _risk_level(composite)
    pattern = _water_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return WaterPrivatizationResult(
        entity_id=e.entity_id,
        water_system=e.water_system,
        region=e.region,
        access_score=access,
        privatization_score=privatization,
        governance_score=governance,
        conflict_score=conflict,
        composite_score=composite,
        risk_level=risk,
        water_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        private_control_share=e.private_control_share,
        aquifer_depletion_rate=e.aquifer_depletion_rate,
    )


class WaterPrivatizationEngine:
    def analyze(self, entities: List[WaterPrivatizationInput]) -> Dict[str, Any]:
        results = [analyze_water_privatization(e) for e in entities]

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
            pattern_distribution[r.water_pattern] = pattern_distribution.get(r.water_pattern, 0) + 1
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
        results: List[WaterPrivatizationResult] = None,
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
            "module_id": 404,
            "module_name": "Privatisation Eau & Bien Commun Hydrique Intelligence Engine",
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
            "avg_estimated_water_commons_index": round(avg_composite / 100 * 10, 2),
        }
