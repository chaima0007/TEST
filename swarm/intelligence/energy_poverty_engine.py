from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class EnergyPovertyInput:
    entity_id: str
    energy_sector: str
    region: str
    energy_access_gap: float
    fossil_fuel_dependency_lock: float
    green_transition_inequality: float
    energy_cost_burden: float
    grid_infrastructure_failure: float
    rural_electrification_gap: float
    just_transition_policy_failure: float
    stranded_community_risk: float
    climate_migration_energy: float
    colonial_energy_debt: float
    renewable_transition_exclusion: float
    energy_affordability_crisis: float
    utility_privatization_harm: float
    subsidy_capture_by_wealthy: float
    carbon_tax_regressive_impact: float
    global_south_transition_gap: float
    energy_democracy_erosion: float


@dataclass
class EnergyPovertyResult:
    entity_id: str
    energy_sector: str
    region: str
    access_score: float
    justice_score: float
    transition_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    energy_pattern: str
    severity: str
    recommended_action: str
    signal: str
    energy_access_gap: float
    rural_electrification_gap: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "energy_sector": self.energy_sector,
            "region": self.region,
            "access_score": self.access_score,
            "justice_score": self.justice_score,
            "transition_score": self.transition_score,
            "systemic_score": self.systemic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "energy_pattern": self.energy_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "energy_access_gap": self.energy_access_gap,
            "rural_electrification_gap": self.rural_electrification_gap,
        }


def _access_score(e: EnergyPovertyInput) -> float:
    raw = (
        e.energy_access_gap * 0.4
        + e.grid_infrastructure_failure * 0.35
        + e.rural_electrification_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _justice_score(e: EnergyPovertyInput) -> float:
    raw = (
        e.energy_cost_burden * 0.4
        + e.subsidy_capture_by_wealthy * 0.35
        + e.utility_privatization_harm * 0.25
    ) * 100
    return round(raw * 100) / 100


def _transition_score(e: EnergyPovertyInput) -> float:
    raw = (
        e.just_transition_policy_failure * 0.4
        + e.renewable_transition_exclusion * 0.35
        + e.green_transition_inequality * 0.25
    ) * 100
    return round(raw * 100) / 100


def _systemic_score(e: EnergyPovertyInput) -> float:
    raw = (
        e.colonial_energy_debt * 0.4
        + e.global_south_transition_gap * 0.35
        + e.energy_democracy_erosion * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    access: float,
    justice: float,
    transition: float,
    systemic: float,
) -> float:
    return round(
        (access * 0.30 + justice * 0.25 + transition * 0.25 + systemic * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _energy_pattern(e: EnergyPovertyInput) -> str:
    if e.energy_access_gap > 0.85 and e.rural_electrification_gap > 0.80:
        return "energy_access_collapse"
    if e.just_transition_policy_failure > 0.85 and e.stranded_community_risk > 0.80:
        return "just_transition_failure"
    if e.green_transition_inequality > 0.85 and e.renewable_transition_exclusion > 0.80:
        return "green_inequality_trap"
    if e.colonial_energy_debt > 0.80 and e.global_south_transition_gap > 0.75:
        return "colonial_energy_debt_crisis"
    if e.energy_affordability_crisis > 0.80 and e.carbon_tax_regressive_impact > 0.75:
        return "energy_affordability_crisis_pattern"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_pauvreté_énergétique_systémique"
    if composite >= 40:
        return "crise_justice_climatique_majeure"
    if composite >= 20:
        return "inégalité_énergétique_structurelle"
    return "accès_énergie_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_accès_énergie_critique"
    if risk == "high":
        return "transition_juste_accélérée_communautés_vulnérables"
    if risk == "moderate":
        return "renforcement_politiques_justice_énergétique"
    return "veille_accès_énergie_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise pauvreté énergétique systémique — justice climatique en péril"
    if risk == "high":
        return "🟠 Crise justice climatique majeure détectée"
    if risk == "moderate":
        return "🟡 Inégalité énergétique structurelle active"
    return "🟢 Accès énergie sous surveillance"


def analyze_energy_poverty(e: EnergyPovertyInput) -> EnergyPovertyResult:
    access = _access_score(e)
    justice = _justice_score(e)
    transition = _transition_score(e)
    systemic = _systemic_score(e)
    composite = _composite_score(access, justice, transition, systemic)
    risk = _risk_level(composite)
    pattern = _energy_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return EnergyPovertyResult(
        entity_id=e.entity_id,
        energy_sector=e.energy_sector,
        region=e.region,
        access_score=access,
        justice_score=justice,
        transition_score=transition,
        systemic_score=systemic,
        composite_score=composite,
        risk_level=risk,
        energy_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        energy_access_gap=e.energy_access_gap,
        rural_electrification_gap=e.rural_electrification_gap,
    )


class EnergyPovertyEngine:
    def analyze(self, entities: List[EnergyPovertyInput]) -> Dict[str, Any]:
        results = [analyze_energy_poverty(e) for e in entities]

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
            pattern_distribution[r.energy_pattern] = pattern_distribution.get(r.energy_pattern, 0) + 1
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
        results: List[EnergyPovertyResult] = None,
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
            "module_id": 379,
            "module_name": "Energy Poverty & Climate Justice Intelligence Engine",
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
            "avg_estimated_energy_justice_index": round(avg_composite / 100 * 10, 2),
        }
