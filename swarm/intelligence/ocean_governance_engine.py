from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class OceanGovernanceInput:
    entity_id: str
    ocean_zone: str
    region: str
    jurisdictional_gap: float
    flag_state_compliance: float
    illegal_fishing_intensity: float
    treaty_ratification_rate: float
    marine_protected_coverage: float
    biodiversity_loss_rate: float
    enforcement_capacity: float
    satellite_monitoring: float
    high_seas_treaty_implementation: float
    deep_sea_mining_governance: float
    military_use_regulation: float
    pollution_accountability: float
    equity_of_access: float
    benefit_sharing_mechanism: float
    climate_adaptation_integration: float
    indigenous_maritime_rights: float
    corporate_accountability: float


@dataclass
class OceanGovernanceResult:
    entity_id: str
    ocean_zone: str
    region: str
    jurisdiction_score: float
    conservation_score: float
    enforcement_score: float
    equity_score: float
    composite_score: float
    risk_level: str
    ocean_pattern: str
    severity: str
    recommended_action: str
    signal: str
    jurisdictional_gap: float
    illegal_fishing_intensity: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "ocean_zone": self.ocean_zone,
            "region": self.region,
            "jurisdiction_score": self.jurisdiction_score,
            "conservation_score": self.conservation_score,
            "enforcement_score": self.enforcement_score,
            "equity_score": self.equity_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "ocean_pattern": self.ocean_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "jurisdictional_gap": self.jurisdictional_gap,
            "illegal_fishing_intensity": self.illegal_fishing_intensity,
        }


def _jurisdiction_score(e: OceanGovernanceInput) -> float:
    raw = (
        e.jurisdictional_gap * 0.4
        + e.flag_state_compliance * 0.35
        + e.illegal_fishing_intensity * 0.25
    ) * 100
    return round(raw * 100) / 100


def _conservation_score(e: OceanGovernanceInput) -> float:
    raw = (
        e.biodiversity_loss_rate * 0.4
        + e.marine_protected_coverage * 0.35
        + e.treaty_ratification_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _enforcement_score(e: OceanGovernanceInput) -> float:
    raw = (
        e.enforcement_capacity * 0.4
        + e.satellite_monitoring * 0.35
        + e.high_seas_treaty_implementation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _equity_score(e: OceanGovernanceInput) -> float:
    raw = (
        e.equity_of_access * 0.4
        + e.benefit_sharing_mechanism * 0.35
        + e.indigenous_maritime_rights * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    jurisdiction: float,
    conservation: float,
    enforcement: float,
    equity: float,
) -> float:
    return round(
        (jurisdiction * 0.30 + conservation * 0.25 + enforcement * 0.25 + equity * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _ocean_pattern(e: OceanGovernanceInput) -> str:
    if e.jurisdictional_gap > 0.85 and e.flag_state_compliance > 0.80:
        return "high_seas_jurisdiction_vacuum"
    if e.illegal_fishing_intensity > 0.85 and e.enforcement_capacity > 0.80:
        return "illeagal_fishing_impunity"
    if e.biodiversity_loss_rate > 0.85 and e.treaty_ratification_rate > 0.80:
        return "biodiversity_treaty_collapse"
    if e.deep_sea_mining_governance > 0.80 and e.corporate_accountability > 0.75:
        return "deep_sea_resource_capture"
    if e.marine_protected_coverage > 0.80 and e.biodiversity_loss_rate > 0.75:
        return "marine_protected_area_failure"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_gouvernance_océanique_systémique"
    if composite >= 40:
        return "crise_haute_mer_majeure"
    if composite >= 20:
        return "déficit_gouvernance_maritime_structurel"
    return "gouvernance_océanique_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_traité_haute_mer_critique"
    if risk == "high":
        return "renforcement_accéléré_juridiction_maritime"
    if risk == "moderate":
        return "consolidation_politiques_conservation_marine"
    return "veille_gouvernance_océanique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise gouvernance océanique systémique — traité haute mer en péril"
    if risk == "high":
        return "🟠 Crise haute mer majeure détectée"
    if risk == "moderate":
        return "🟡 Déficit gouvernance maritime structurel actif"
    return "🟢 Gouvernance océanique sous surveillance"


def analyze_ocean_governance(e: OceanGovernanceInput) -> OceanGovernanceResult:
    jurisdiction = _jurisdiction_score(e)
    conservation = _conservation_score(e)
    enforcement = _enforcement_score(e)
    equity = _equity_score(e)
    composite = _composite_score(jurisdiction, conservation, enforcement, equity)
    risk = _risk_level(composite)
    pattern = _ocean_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return OceanGovernanceResult(
        entity_id=e.entity_id,
        ocean_zone=e.ocean_zone,
        region=e.region,
        jurisdiction_score=jurisdiction,
        conservation_score=conservation,
        enforcement_score=enforcement,
        equity_score=equity,
        composite_score=composite,
        risk_level=risk,
        ocean_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        jurisdictional_gap=e.jurisdictional_gap,
        illegal_fishing_intensity=e.illegal_fishing_intensity,
    )


class OceanGovernanceEngine:
    def analyze(self, entities: List[OceanGovernanceInput]) -> Dict[str, Any]:
        results = [analyze_ocean_governance(e) for e in entities]

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
            pattern_distribution[r.ocean_pattern] = pattern_distribution.get(r.ocean_pattern, 0) + 1
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
        results: List[OceanGovernanceResult] = None,
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
            "module_id": 420,
            "module_name": "Gouvernance Océans & Traité Haute Mer Intelligence Engine",
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
            "avg_estimated_ocean_governance_index": round(avg_composite / 100 * 10, 2),
        }
