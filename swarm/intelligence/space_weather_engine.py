from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SpaceWeatherInput:
    entity_id: str
    infrastructure_type: str
    region: str
    solar_activity_exposure: float
    grid_hardening_level: float
    transformer_vulnerability: float
    satellite_shielding: float
    gps_dependency: float
    communication_backup: float
    financial_system_exposure: float
    emergency_power_reserve: float
    early_warning_capability: float
    geomagnetic_latitude_risk: float
    critical_system_redundancy: float
    international_coordination: float
    public_awareness: float
    recovery_time_estimate: float
    data_center_protection: float
    aviation_vulnerability: float
    space_situational_awareness: float


@dataclass
class SpaceWeatherResult:
    entity_id: str
    infrastructure_type: str
    region: str
    exposure_score: float
    resilience_score: float
    preparedness_score: float
    cascade_score: float
    composite_score: float
    risk_level: str
    space_weather_pattern: str
    severity: str
    recommended_action: str
    signal: str
    solar_activity_exposure: float
    geomagnetic_latitude_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "infrastructure_type": self.infrastructure_type,
            "region": self.region,
            "exposure_score": self.exposure_score,
            "resilience_score": self.resilience_score,
            "preparedness_score": self.preparedness_score,
            "cascade_score": self.cascade_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "space_weather_pattern": self.space_weather_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "solar_activity_exposure": self.solar_activity_exposure,
            "geomagnetic_latitude_risk": self.geomagnetic_latitude_risk,
        }


def _exposure_score(e: SpaceWeatherInput) -> float:
    raw = (
        e.solar_activity_exposure * 0.4
        + e.geomagnetic_latitude_risk * 0.35
        + e.transformer_vulnerability * 0.25
    ) * 100
    return round(raw * 100) / 100


def _resilience_score(e: SpaceWeatherInput) -> float:
    raw = (
        (1.0 - e.grid_hardening_level) * 0.4
        + (1.0 - e.satellite_shielding) * 0.35
        + (1.0 - e.critical_system_redundancy) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _preparedness_score(e: SpaceWeatherInput) -> float:
    raw = (
        (1.0 - e.early_warning_capability) * 0.4
        + (1.0 - e.emergency_power_reserve) * 0.35
        + (1.0 - e.communication_backup) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _cascade_score(e: SpaceWeatherInput) -> float:
    raw = (
        e.financial_system_exposure * 0.4
        + e.gps_dependency * 0.35
        + e.aviation_vulnerability * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    exposure: float,
    resilience: float,
    preparedness: float,
    cascade: float,
) -> float:
    return round(
        (exposure * 0.30 + resilience * 0.25 + preparedness * 0.25 + cascade * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _space_weather_pattern(e: SpaceWeatherInput) -> str:
    if e.solar_activity_exposure > 0.85 and e.transformer_vulnerability > 0.80:
        return "carrington_level_event_risk"
    if e.geomagnetic_latitude_risk > 0.85 and e.grid_hardening_level < 0.20:
        return "grid_infrastructure_collapse"
    if e.satellite_shielding < 0.20 and e.space_situational_awareness < 0.20:
        return "satellite_constellation_disruption"
    if e.financial_system_exposure > 0.80 and e.data_center_protection < 0.25:
        return "financial_system_blackout"
    if e.emergency_power_reserve < 0.20 and e.international_coordination < 0.20:
        return "emergency_coordination_failure"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_tempête_solaire_systémique"
    if composite >= 40:
        return "crise_météo_spatiale_majeure"
    if composite >= 20:
        return "perturbation_géomagnétique_structurelle"
    return "météo_spatiale_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_protection_infrastructures_critiques"
    if risk == "high":
        return "renforcement_durcissement_systèmes_haute_priorité"
    if risk == "moderate":
        return "amélioration_préparation_alerte_précoce"
    return "veille_météo_spatiale_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise tempête solaire systémique — infrastructures critiques en péril"
    if risk == "high":
        return "🟠 Crise météo spatiale majeure détectée"
    if risk == "moderate":
        return "🟡 Perturbation géomagnétique structurelle active"
    return "🟢 Météo spatiale sous surveillance"


def analyze_space_weather(e: SpaceWeatherInput) -> SpaceWeatherResult:
    exposure = _exposure_score(e)
    resilience = _resilience_score(e)
    preparedness = _preparedness_score(e)
    cascade = _cascade_score(e)
    composite = _composite_score(exposure, resilience, preparedness, cascade)
    risk = _risk_level(composite)
    pattern = _space_weather_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return SpaceWeatherResult(
        entity_id=e.entity_id,
        infrastructure_type=e.infrastructure_type,
        region=e.region,
        exposure_score=exposure,
        resilience_score=resilience,
        preparedness_score=preparedness,
        cascade_score=cascade,
        composite_score=composite,
        risk_level=risk,
        space_weather_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        solar_activity_exposure=e.solar_activity_exposure,
        geomagnetic_latitude_risk=e.geomagnetic_latitude_risk,
    )


class SpaceWeatherEngine:
    def analyze(self, entities: List[SpaceWeatherInput]) -> Dict[str, Any]:
        results = [analyze_space_weather(e) for e in entities]

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
            pattern_distribution[r.space_weather_pattern] = pattern_distribution.get(r.space_weather_pattern, 0) + 1
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
        results: List[SpaceWeatherResult] = None,
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
            "module_id": 407,
            "module_name": "Météo Spatiale & Tempête Solaire Infrastructure Intelligence Engine",
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
            "avg_estimated_space_weather_index": round(avg_composite / 100 * 10, 2),
        }
