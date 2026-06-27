from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CoralReefInput:
    entity_id: str
    reef_type: str
    region: str
    bleaching_frequency: float
    temperature_anomaly: float
    ocean_acidification_ph: float
    coral_cover_loss: float
    biodiversity_decline: float
    nutrient_pollution: float
    sedimentation_rate: float
    destructive_fishing_intensity: float
    crown_of_thorns_outbreak: float
    sunscreen_chemical_impact: float
    mpa_effectiveness: float
    restoration_investment: float
    climate_trajectory: float
    tourism_damage: float
    coastal_development_pressure: float
    recovery_time_estimate: float
    genetic_diversity_reserve: float


@dataclass
class CoralReefResult:
    entity_id: str
    reef_type: str
    region: str
    bleaching_score: float
    pollution_score: float
    governance_score: float
    recovery_score: float
    composite_score: float
    risk_level: str
    reef_pattern: str
    severity: str
    recommended_action: str
    signal: str
    bleaching_frequency: float
    coral_cover_loss: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "reef_type": self.reef_type,
            "region": self.region,
            "bleaching_score": self.bleaching_score,
            "pollution_score": self.pollution_score,
            "governance_score": self.governance_score,
            "recovery_score": self.recovery_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "reef_pattern": self.reef_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "bleaching_frequency": self.bleaching_frequency,
            "coral_cover_loss": self.coral_cover_loss,
        }


def _bleaching_score(e: CoralReefInput) -> float:
    raw = (
        e.bleaching_frequency * 0.4
        + e.temperature_anomaly * 0.35
        + e.ocean_acidification_ph * 0.25
    ) * 100
    return round(raw * 100) / 100


def _pollution_score(e: CoralReefInput) -> float:
    raw = (
        e.nutrient_pollution * 0.4
        + e.sedimentation_rate * 0.35
        + e.sunscreen_chemical_impact * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: CoralReefInput) -> float:
    raw = (
        e.destructive_fishing_intensity * 0.4
        + e.tourism_damage * 0.35
        + e.coastal_development_pressure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _recovery_score(e: CoralReefInput) -> float:
    raw = (
        e.coral_cover_loss * 0.4
        + e.biodiversity_decline * 0.35
        + e.crown_of_thorns_outbreak * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    bleaching: float,
    pollution: float,
    governance: float,
    recovery: float,
) -> float:
    return round(
        (bleaching * 0.30 + pollution * 0.25 + governance * 0.25 + recovery * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _reef_pattern(e: CoralReefInput) -> str:
    if e.bleaching_frequency > 0.85 and e.temperature_anomaly > 0.80:
        return "mass_bleaching_extinction_event"
    if e.ocean_acidification_ph > 0.85 and e.coral_cover_loss > 0.80:
        return "ocean_acidification_dissolution"
    if e.nutrient_pollution > 0.85 and e.sedimentation_rate > 0.80:
        return "nutrient_runoff_algae_takeover"
    if e.destructive_fishing_intensity > 0.80 and e.biodiversity_decline > 0.75:
        return "destructive_fishing_collapse"
    if e.mpa_effectiveness > 0.80 and e.restoration_investment > 0.75:
        return "marine_protected_area_failure"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "effondrement_récifal_systémique_critique"
    if composite >= 40:
        return "dégradation_corallienne_majeure"
    if composite >= 20:
        return "stress_écosystème_marin_modéré"
    return "récif_sous_surveillance_active"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_récif_effondrement_critique"
    if risk == "high":
        return "restauration_corallienne_accélérée_zones_dégradées"
    if risk == "moderate":
        return "renforcement_protection_marine_surveillance_continue"
    return "veille_santé_récifale_préventive"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Effondrement récifal systémique — extinction massive imminente"
    if risk == "high":
        return "🟠 Dégradation corallienne majeure détectée"
    if risk == "moderate":
        return "🟡 Stress écosystème marin modéré actif"
    return "🟢 Récif sous surveillance active"


def analyze_coral_reef(e: CoralReefInput) -> CoralReefResult:
    bleaching = _bleaching_score(e)
    pollution = _pollution_score(e)
    governance = _governance_score(e)
    recovery = _recovery_score(e)
    composite = _composite_score(bleaching, pollution, governance, recovery)
    risk = _risk_level(composite)
    pattern = _reef_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return CoralReefResult(
        entity_id=e.entity_id,
        reef_type=e.reef_type,
        region=e.region,
        bleaching_score=bleaching,
        pollution_score=pollution,
        governance_score=governance,
        recovery_score=recovery,
        composite_score=composite,
        risk_level=risk,
        reef_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        bleaching_frequency=e.bleaching_frequency,
        coral_cover_loss=e.coral_cover_loss,
    )


class CoralReefEngine:
    def analyze(self, entities: List[CoralReefInput]) -> Dict[str, Any]:
        results = [analyze_coral_reef(e) for e in entities]

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
            pattern_distribution[r.reef_pattern] = pattern_distribution.get(r.reef_pattern, 0) + 1
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
        results: List[CoralReefResult] = None,
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
            "module_id": 424,
            "module_name": "Effondrement Récifs Coralliens & Écosystèmes Marins Intelligence Engine",
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
            "avg_estimated_coral_health_index": round(avg_composite / 100 * 10, 2),
        }
