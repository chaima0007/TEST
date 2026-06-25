from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class BiosurveillanceInput:
    entity_id: str
    surveillance_system: str
    region: str
    outbreak_detection_delay: float
    genomic_sequencing_gap: float
    zoonotic_interface_monitoring: float
    one_health_integration_failure: float
    lab_network_capacity: float
    data_sharing_obstruction: float
    early_warning_system_weakness: float
    cross_border_surveillance_gap: float
    community_level_detection_gap: float
    mobile_surveillance_coverage: float
    veterinary_surveillance_failure: float
    environmental_health_monitoring_gap: float
    WHO_reporting_compliance: float
    climate_disease_nexus_monitoring: float
    wastewater_surveillance_implementation: float
    AI_surveillance_deployment: float
    political_outbreak_suppression: float


@dataclass
class BiosurveillanceResult:
    entity_id: str
    surveillance_system: str
    region: str
    detection_score: float
    response_score: float
    governance_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    biosurveillance_pattern: str
    severity: str
    recommended_action: str
    signal: str
    outbreak_detection_delay: float
    genomic_sequencing_gap: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "surveillance_system": self.surveillance_system,
            "region": self.region,
            "detection_score": self.detection_score,
            "response_score": self.response_score,
            "governance_score": self.governance_score,
            "systemic_score": self.systemic_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "biosurveillance_pattern": self.biosurveillance_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "outbreak_detection_delay": self.outbreak_detection_delay,
            "genomic_sequencing_gap": self.genomic_sequencing_gap,
        }


def _detection_score(e: BiosurveillanceInput) -> float:
    raw = (
        e.outbreak_detection_delay * 0.40
        + e.early_warning_system_weakness * 0.35
        + e.community_level_detection_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _response_score(e: BiosurveillanceInput) -> float:
    raw = (
        e.cross_border_surveillance_gap * 0.40
        + e.lab_network_capacity * 0.35
        + e.mobile_surveillance_coverage * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: BiosurveillanceInput) -> float:
    raw = (
        e.WHO_reporting_compliance * 0.40
        + e.data_sharing_obstruction * 0.35
        + e.political_outbreak_suppression * 0.25
    ) * 100
    return round(raw * 100) / 100


def _systemic_score(e: BiosurveillanceInput) -> float:
    raw = (
        e.one_health_integration_failure * 0.40
        + e.zoonotic_interface_monitoring * 0.35
        + e.genomic_sequencing_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    detection: float,
    response: float,
    governance: float,
    systemic: float,
) -> float:
    return round(
        (detection * 0.30 + response * 0.25 + governance * 0.25 + systemic * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _biosurveillance_pattern(e: BiosurveillanceInput) -> str:
    if e.outbreak_detection_delay > 0.85 and e.early_warning_system_weakness > 0.80:
        return "outbreak_detection_failure"
    if e.political_outbreak_suppression > 0.85 and e.WHO_reporting_compliance > 0.80:
        return "data_sharing_political_suppression"
    if e.zoonotic_interface_monitoring > 0.85 and e.veterinary_surveillance_failure > 0.80:
        return "zoonotic_surveillance_gap"
    if e.genomic_sequencing_gap > 0.80 and e.lab_network_capacity > 0.75:
        return "genomic_surveillance_collapse"
    if e.cross_border_surveillance_gap > 0.80 and e.data_sharing_obstruction > 0.75:
        return "cross_border_surveillance_failure"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "effondrement_biosurveillance_systémique"
    if composite >= 40:
        return "crise_alerte_précoce_épidémique_majeure"
    if composite >= 20:
        return "défaillance_biosurveillance_structurelle"
    return "biosurveillance_sous_contrôle"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_biosurveillance_urgence_mondiale"
    if risk == "high":
        return "renforcement_alerte_précoce_urgence"
    if risk == "moderate":
        return "amélioration_surveillance_épidémique_systémique"
    return "veille_biosurveillance_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Effondrement biosurveillance — alerte épidémique critique"
    if risk == "high":
        return "🟠 Crise alerte précoce épidémique majeure détectée"
    if risk == "moderate":
        return "🟡 Défaillance biosurveillance structurelle active"
    return "🟢 Biosurveillance sous contrôle et contenue"


def analyze_biosurveillance(e: BiosurveillanceInput) -> BiosurveillanceResult:
    detection = _detection_score(e)
    response = _response_score(e)
    governance = _governance_score(e)
    systemic = _systemic_score(e)
    composite = _composite_score(detection, response, governance, systemic)
    risk = _risk_level(composite)
    pattern = _biosurveillance_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return BiosurveillanceResult(
        entity_id=e.entity_id,
        surveillance_system=e.surveillance_system,
        region=e.region,
        detection_score=detection,
        response_score=response,
        governance_score=governance,
        systemic_score=systemic,
        composite_score=composite,
        risk_level=risk,
        biosurveillance_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        outbreak_detection_delay=e.outbreak_detection_delay,
        genomic_sequencing_gap=e.genomic_sequencing_gap,
    )


class BiosurveillanceEngine:
    def analyze(self, entities: List[BiosurveillanceInput]) -> Dict[str, Any]:
        results = [analyze_biosurveillance(e) for e in entities]

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
            pattern_distribution[r.biosurveillance_pattern] = pattern_distribution.get(r.biosurveillance_pattern, 0) + 1
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
        results: List[BiosurveillanceResult],
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
            "module_id": 391,
            "module_name": "Biosurveillance & Epidemic Early Warning Intelligence Engine",
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
            "avg_estimated_biosurveillance_index": round(avg_composite / 100 * 10, 2),
        }

    def summary(self, entities: List[BiosurveillanceInput]) -> Dict[str, Any]:
        return self.analyze(entities)
