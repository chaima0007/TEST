from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class NoisePollutionInput:
    entity_id: str
    urban_type: str
    region: str
    # 17 float fields (0-1)
    noise_level_db: float
    traffic_exposure: float
    aviation_exposure: float
    industrial_noise: float
    cardiovascular_risk: float
    sleep_disruption: float
    cognitive_impact: float
    mental_health_burden: float
    school_noise_exposure: float
    hospital_quiet_zone_compliance: float
    low_income_exposure: float
    racial_disparity: float
    regulatory_compliance: float
    green_barrier_coverage: float
    complaint_response_rate: float
    nighttime_violations: float
    tinnitus_prevalence: float


@dataclass
class NoisePollutionResult:
    entity_id: str
    urban_type: str
    region: str
    exposure_score: float
    health_impact_score: float
    inequality_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    noise_pattern: str
    severity: str
    recommended_action: str
    signal: str
    noise_level_db: float
    sleep_disruption: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "urban_type": self.urban_type,
            "region": self.region,
            "exposure_score": self.exposure_score,
            "health_impact_score": self.health_impact_score,
            "inequality_score": self.inequality_score,
            "governance_score": self.governance_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "noise_pattern": self.noise_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "noise_level_db": self.noise_level_db,
            "sleep_disruption": self.sleep_disruption,
        }


def _exposure_score(e: NoisePollutionInput) -> float:
    raw = (
        e.noise_level_db * 0.40
        + e.traffic_exposure * 0.35
        + e.aviation_exposure * 0.15
        + e.industrial_noise * 0.10
    ) * 100
    return round(raw * 100) / 100


def _health_impact_score(e: NoisePollutionInput) -> float:
    raw = (
        e.cardiovascular_risk * 0.35
        + e.sleep_disruption * 0.30
        + e.cognitive_impact * 0.20
        + e.mental_health_burden * 0.15
    ) * 100
    return round(raw * 100) / 100


def _inequality_score(e: NoisePollutionInput) -> float:
    raw = (
        e.low_income_exposure * 0.40
        + e.racial_disparity * 0.35
        + e.school_noise_exposure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: NoisePollutionInput) -> float:
    raw = (
        (1.0 - e.regulatory_compliance) * 0.40
        + e.nighttime_violations * 0.35
        + (1.0 - e.complaint_response_rate) * 0.15
        + (1.0 - e.green_barrier_coverage) * 0.10
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    exposure: float,
    health: float,
    inequality: float,
    governance: float,
) -> float:
    return round(
        (exposure * 0.30 + health * 0.25 + inequality * 0.25 + governance * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _noise_pattern(e: NoisePollutionInput) -> str:
    if e.cardiovascular_risk > 0.85 and e.noise_level_db > 0.80:
        return "chronic_cardiovascular_noise_crisis"
    if e.sleep_disruption > 0.85 and e.nighttime_violations > 0.80:
        return "sleep_deprivation_pandemic"
    if e.school_noise_exposure > 0.85 and e.cognitive_impact > 0.80:
        return "childhood_cognitive_impairment"
    if e.low_income_exposure > 0.85 and e.racial_disparity > 0.80:
        return "noise_poverty_inequality_trap"
    if e.regulatory_compliance < 0.20 and e.complaint_response_rate < 0.20:
        return "regulatory_enforcement_collapse"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_pollution_sonore_systémique"
    if composite >= 40:
        return "crise_santé_urbaine_majeure"
    if composite >= 20:
        return "nuisance_sonore_structurelle"
    return "environnement_sonore_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_pollution_sonore_critique"
    if risk == "high":
        return "plan_réduction_bruit_accéléré_zones_vulnérables"
    if risk == "moderate":
        return "renforcement_réglementation_acoustique_urbaine"
    return "veille_environnement_sonore_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise pollution sonore systémique — santé urbaine en péril"
    if risk == "high":
        return "🟠 Crise santé urbaine majeure détectée"
    if risk == "moderate":
        return "🟡 Nuisance sonore structurelle active"
    return "🟢 Environnement sonore sous surveillance"


def analyze_noise_pollution(e: NoisePollutionInput) -> NoisePollutionResult:
    exposure = _exposure_score(e)
    health = _health_impact_score(e)
    inequality = _inequality_score(e)
    governance = _governance_score(e)
    composite = _composite_score(exposure, health, inequality, governance)
    risk = _risk_level(composite)
    pattern = _noise_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return NoisePollutionResult(
        entity_id=e.entity_id,
        urban_type=e.urban_type,
        region=e.region,
        exposure_score=exposure,
        health_impact_score=health,
        inequality_score=inequality,
        governance_score=governance,
        composite_score=composite,
        risk_level=risk,
        noise_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        noise_level_db=e.noise_level_db,
        sleep_disruption=e.sleep_disruption,
    )


class NoisePollutionEngine:
    def analyze(self, entities: List[NoisePollutionInput]) -> Dict[str, Any]:
        results = [analyze_noise_pollution(e) for e in entities]

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
            pattern_distribution[r.noise_pattern] = pattern_distribution.get(r.noise_pattern, 0) + 1
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
        results: List[NoisePollutionResult] = None,
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
            "module_id": 398,
            "module_name": "Pollution Sonore & Santé Urbaine Intelligence Engine",
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
            "avg_estimated_noise_health_index": round(avg_composite / 100 * 10, 2),
        }
