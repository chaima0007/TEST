from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SpaceDebrisInput:
    entity_id: str
    orbital_shell: str
    region: str
    debris_density: float
    collision_probability: float
    cascade_initiation_risk: float
    mega_constellation_contribution: float
    mitigation_compliance_failure: float
    active_debris_removal_gap: float
    conjunction_event_rate: float
    weaponized_debris_risk: float
    LEO_saturation_level: float
    GEO_contamination_risk: float
    orbital_slot_exhaustion: float
    launch_cadence_impact: float
    international_governance_failure: float
    insurance_market_collapse: float
    space_weather_amplification: float
    debris_weaponization: float
    remediation_technology_lag: float


@dataclass
class SpaceDebrisResult:
    entity_id: str
    orbital_shell: str
    region: str
    cascade_score: float
    density_score: float
    governance_score: float
    weaponization_score: float
    composite_score: float
    risk_level: str
    debris_pattern: str
    severity: str
    recommended_action: str
    signal: str
    debris_density: float
    collision_probability: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "orbital_shell": self.orbital_shell,
            "region": self.region,
            "cascade_score": self.cascade_score,
            "density_score": self.density_score,
            "governance_score": self.governance_score,
            "weaponization_score": self.weaponization_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "debris_pattern": self.debris_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "debris_density": self.debris_density,
            "collision_probability": self.collision_probability,
        }


def _cascade_score(e: SpaceDebrisInput) -> float:
    raw = (
        e.cascade_initiation_risk * 0.4
        + e.collision_probability * 0.35
        + e.conjunction_event_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _density_score(e: SpaceDebrisInput) -> float:
    raw = (
        e.debris_density * 0.4
        + e.LEO_saturation_level * 0.35
        + e.GEO_contamination_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: SpaceDebrisInput) -> float:
    raw = (
        e.international_governance_failure * 0.4
        + e.mitigation_compliance_failure * 0.35
        + e.remediation_technology_lag * 0.25
    ) * 100
    return round(raw * 100) / 100


def _weaponization_score(e: SpaceDebrisInput) -> float:
    raw = (
        e.weaponized_debris_risk * 0.4
        + e.debris_weaponization * 0.35
        + e.insurance_market_collapse * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    cascade: float,
    density: float,
    governance: float,
    weaponization: float,
) -> float:
    return round(
        (cascade * 0.30 + density * 0.25 + governance * 0.25 + weaponization * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _debris_pattern(e: SpaceDebrisInput) -> str:
    if e.cascade_initiation_risk > 0.85 and e.debris_density > 0.80:
        return "kessler_syndrome_onset"
    if e.mega_constellation_contribution > 0.85 and e.LEO_saturation_level > 0.80:
        return "mega_constellation_crisis"
    if e.weaponized_debris_risk > 0.85 and e.debris_weaponization > 0.80:
        return "debris_weaponization_cascade"
    if e.international_governance_failure > 0.80 and e.active_debris_removal_gap > 0.75:
        return "governance_remediation_failure"
    if e.orbital_slot_exhaustion > 0.80 and e.launch_cadence_impact > 0.75:
        return "orbital_commons_collapse"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "effondrement_orbital_systémique"
    if composite >= 40:
        return "crise_débris_spatiaux_majeure"
    if composite >= 20:
        return "saturation_orbitale_structurelle"
    return "débris_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_débris_urgence_mondiale"
    if risk == "high":
        return "retrait_débris_actifs_urgence"
    if risk == "moderate":
        return "renforcement_gouvernance_orbitale"
    return "veille_débris_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Syndrome Kessler imminent — effondrement orbital critique"
    if risk == "high":
        return "🟠 Crise débris spatiaux majeure détectée"
    if risk == "moderate":
        return "🟡 Saturation orbitale structurelle active"
    return "🟢 Débris spatiaux sous surveillance et contenus"


def analyze_space_debris(e: SpaceDebrisInput) -> SpaceDebrisResult:
    cascade = _cascade_score(e)
    density = _density_score(e)
    governance = _governance_score(e)
    weaponization = _weaponization_score(e)
    composite = _composite_score(cascade, density, governance, weaponization)
    risk = _risk_level(composite)
    pattern = _debris_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return SpaceDebrisResult(
        entity_id=e.entity_id,
        orbital_shell=e.orbital_shell,
        region=e.region,
        cascade_score=cascade,
        density_score=density,
        governance_score=governance,
        weaponization_score=weaponization,
        composite_score=composite,
        risk_level=risk,
        debris_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        debris_density=e.debris_density,
        collision_probability=e.collision_probability,
    )


class SpaceDebrisEngine:
    def analyze(self, entities: List[SpaceDebrisInput]) -> Dict[str, Any]:
        results = [analyze_space_debris(e) for e in entities]

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
            pattern_distribution[r.debris_pattern] = pattern_distribution.get(r.debris_pattern, 0) + 1
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

        return self._summary(
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

    def _summary(
        self,
        results: List[SpaceDebrisResult],
        risk_distribution: Dict[str, int],
        pattern_distribution: Dict[str, int],
        severity_distribution: Dict[str, int],
        action_distribution: Dict[str, int],
        avg_composite: float,
        critical_count: int,
        high_count: int,
        moderate_count: int,
        low_count: int,
    ) -> Dict[str, Any]:
        return {
            "module_id": 370,
            "module_name": "Space Debris & Kessler Syndrome Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_kessler_risk_index": round(avg_composite / 100 * 10, 2),
        }

    def summary(self, entities: List[SpaceDebrisInput]) -> Dict[str, Any]:
        return self.analyze(entities)
