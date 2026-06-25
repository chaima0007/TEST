"""
Module 338 — Migration Crisis & Demographic Shock Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MigrationCrisisInput:
    entity_id: str
    migration_corridor: str
    region: str
    forced_displacement_rate: float
    climate_migration_acceleration: float
    economic_migration_pressure: float
    border_violence_index: float
    asylum_system_saturation: float
    integration_failure_rate: float
    xenophobia_political_exploitation: float
    demographic_aging_severity: float
    brain_drain_intensity: float
    stateless_population_growth: float
    migration_route_lethality: float
    remittance_dependency_fragility: float
    migration_policy_collapse: float
    diaspora_radicalisation_risk: float
    demographic_dividend_loss: float
    host_society_social_cohesion_erosion: float
    labor_market_displacement_cascade: float


@dataclass
class MigrationCrisisResult:
    entity_id: str
    migration_corridor: str
    region: str
    displacement_score: float
    reception_score: float
    social_score: float
    demographic_score: float
    composite_score: float
    risk_level: str
    migration_pattern: str
    severity: str
    recommended_action: str
    signal: str
    forced_displacement_rate: float
    climate_migration_acceleration: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "migration_corridor": self.migration_corridor,
            "region": self.region,
            "displacement_score": self.displacement_score,
            "reception_score": self.reception_score,
            "social_score": self.social_score,
            "demographic_score": self.demographic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "migration_pattern": self.migration_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "forced_displacement_rate": self.forced_displacement_rate,
            "climate_migration_acceleration": self.climate_migration_acceleration,
        }


def _displacement_score(e: MigrationCrisisInput) -> float:
    raw = (
        e.forced_displacement_rate * 0.4
        + e.climate_migration_acceleration * 0.35
        + e.migration_route_lethality * 0.25
    ) * 100
    return round(raw * 100) / 100


def _reception_score(e: MigrationCrisisInput) -> float:
    raw = (
        e.asylum_system_saturation * 0.4
        + e.integration_failure_rate * 0.35
        + e.migration_policy_collapse * 0.25
    ) * 100
    return round(raw * 100) / 100


def _social_score(e: MigrationCrisisInput) -> float:
    raw = (
        e.xenophobia_political_exploitation * 0.4
        + e.host_society_social_cohesion_erosion * 0.35
        + e.diaspora_radicalisation_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _demographic_score(e: MigrationCrisisInput) -> float:
    raw = (
        e.demographic_aging_severity * 0.4
        + e.brain_drain_intensity * 0.35
        + e.demographic_dividend_loss * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(displacement: float, reception: float, social: float, demographic: float) -> float:
    return round((displacement * 0.30 + reception * 0.25 + social * 0.25 + demographic * 0.20) * 100) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _migration_pattern(e: MigrationCrisisInput) -> str:
    if e.forced_displacement_rate >= 0.70 and e.migration_route_lethality >= 0.65:
        return "mass_displacement_crisis"
    if e.asylum_system_saturation >= 0.70 and e.migration_policy_collapse >= 0.65:
        return "asylum_system_collapse"
    if e.climate_migration_acceleration >= 0.70 and e.economic_migration_pressure >= 0.65:
        return "climate_exodus"
    if e.xenophobia_political_exploitation >= 0.70 and e.host_society_social_cohesion_erosion >= 0.65:
        return "xenophobia_cascade"
    if e.demographic_aging_severity >= 0.70 and e.brain_drain_intensity >= 0.65:
        return "demographic_implosion"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_migratoire_systémique"
    if composite >= 40:
        return "choc_démographique_majeur"
    if composite >= 20:
        return "pression_migratoire_structurelle"
    return "migration_gérée"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_humanitaire_urgente"
    if risk == "high":
        return "réforme_système_asile_accélérée"
    if risk == "moderate":
        return "renforcement_intégration_systémique"
    return "veille_démographique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise migratoire systémique — choc humanitaire extrême"
    if risk == "high":
        return "🟠 Choc démographique majeur détecté"
    if risk == "moderate":
        return "🟡 Pression migratoire structurelle active"
    return "🟢 Flux migratoires relativement gérés"


def analyze_entity(e: MigrationCrisisInput) -> MigrationCrisisResult:
    displacement = _displacement_score(e)
    reception = _reception_score(e)
    social = _social_score(e)
    demographic = _demographic_score(e)
    comp = _composite(displacement, reception, social, demographic)
    risk = _risk_level(comp)
    pattern = _migration_pattern(e)
    sev = _severity(comp)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return MigrationCrisisResult(
        entity_id=e.entity_id,
        migration_corridor=e.migration_corridor,
        region=e.region,
        displacement_score=displacement,
        reception_score=reception,
        social_score=social,
        demographic_score=demographic,
        composite_score=comp,
        risk_level=risk,
        migration_pattern=pattern,
        severity=sev,
        recommended_action=action,
        signal=sig,
        forced_displacement_rate=e.forced_displacement_rate,
        climate_migration_acceleration=e.climate_migration_acceleration,
    )


class MigrationCrisisEngine:
    def analyze(self, entities: List[MigrationCrisisInput]) -> Dict[str, Any]:
        results = [analyze_entity(e) for e in entities]
        entity_dicts = [r.to_dict() for r in results]

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
            pattern_distribution[r.migration_pattern] = pattern_distribution.get(r.migration_pattern, 0) + 1
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

        n = len(results)
        avg_composite = round(total_composite / n * 10) / 10 if n else 0.0

        smry = self.summary(
            total_entities=n,
            critical_count=critical_count,
            high_count=high_count,
            moderate_count=moderate_count,
            low_count=low_count,
            avg_composite=avg_composite,
            pattern_distribution=pattern_distribution,
            risk_distribution=risk_distribution,
            severity_distribution=severity_distribution,
            action_distribution=action_distribution,
        )

        return {"entities": entity_dicts, "summary": smry}

    def summary(
        self,
        total_entities: int,
        critical_count: int,
        high_count: int,
        moderate_count: int,
        low_count: int,
        avg_composite: float,
        pattern_distribution: Dict[str, int],
        risk_distribution: Dict[str, int],
        severity_distribution: Dict[str, int],
        action_distribution: Dict[str, int],
    ) -> Dict[str, Any]:
        return {
            "module_id": 338,
            "module_name": "Migration Crisis & Demographic Shock Intelligence Engine",
            "total_entities": total_entities,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_migration_crisis_index": round(avg_composite / 100 * 10, 2),
        }
