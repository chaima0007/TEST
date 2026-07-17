from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AcademicIntegrityInput:
    entity_id: str
    research_field: str
    region: str
    retraction_rate: float
    data_fabrication_index: float
    plagiarism_detection_gap: float
    predatory_journal_prevalence: float
    paper_mill_activity: float
    peer_review_quality: float
    open_access_integrity: float
    replication_success_rate: float
    statistical_manipulation: float
    conflicts_of_interest: float
    industry_funding_bias: float
    ai_generated_content_rate: float
    preprint_misinformation: float
    institutional_misconduct_response: float
    whistleblower_protection: float
    reproducibility_infrastructure: float
    research_fraud_prosecution: float


@dataclass
class AcademicIntegrityResult:
    entity_id: str
    research_field: str
    region: str
    fraud_score: float
    publishing_score: float
    replication_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    integrity_pattern: str
    severity: str
    recommended_action: str
    signal: str
    retraction_rate: float
    data_fabrication_index: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "research_field": self.research_field,
            "region": self.region,
            "fraud_score": self.fraud_score,
            "publishing_score": self.publishing_score,
            "replication_score": self.replication_score,
            "governance_score": self.governance_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "integrity_pattern": self.integrity_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "retraction_rate": self.retraction_rate,
            "data_fabrication_index": self.data_fabrication_index,
        }


def _fraud_score(e: AcademicIntegrityInput) -> float:
    raw = (
        e.data_fabrication_index * 0.4
        + e.retraction_rate * 0.35
        + e.statistical_manipulation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _publishing_score(e: AcademicIntegrityInput) -> float:
    raw = (
        e.predatory_journal_prevalence * 0.4
        + e.paper_mill_activity * 0.35
        + e.plagiarism_detection_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _replication_score(e: AcademicIntegrityInput) -> float:
    raw = (
        e.replication_success_rate * 0.4
        + e.preprint_misinformation * 0.35
        + e.ai_generated_content_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: AcademicIntegrityInput) -> float:
    raw = (
        e.peer_review_quality * 0.4
        + e.institutional_misconduct_response * 0.35
        + e.conflicts_of_interest * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    fraud: float,
    publishing: float,
    replication: float,
    governance: float,
) -> float:
    return round(
        (fraud * 0.30 + publishing * 0.25 + replication * 0.25 + governance * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _integrity_pattern(e: AcademicIntegrityInput) -> str:
    if e.data_fabrication_index > 0.85 and e.retraction_rate > 0.80:
        return "data_fabrication_fraud_ring"
    if e.predatory_journal_prevalence > 0.85 and e.paper_mill_activity > 0.80:
        return "predatory_publishing_ecosystem"
    if e.replication_success_rate > 0.85 and e.preprint_misinformation > 0.80:
        return "replication_crisis_collapse"
    if e.peer_review_quality > 0.80 and e.conflicts_of_interest > 0.75:
        return "peer_review_capture"
    if e.ai_generated_content_rate > 0.80 and e.plagiarism_detection_gap > 0.75:
        return "ai_generated_research_flood"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_intégrité_recherche_systémique"
    if composite >= 40:
        return "crise_fraude_scientifique_majeure"
    if composite >= 20:
        return "déficit_intégrité_académique_structurel"
    return "surveillance_intégrité_recherche_continue"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_intégrité_recherche_critique"
    if risk == "high":
        return "renforcement_mécanismes_détection_fraude_accéléré"
    if risk == "moderate":
        return "amélioration_gouvernance_publication_scientifique"
    return "veille_intégrité_académique_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise intégrité recherche systémique — fraude scientifique en péril"
    if risk == "high":
        return "🟠 Crise fraude scientifique majeure détectée"
    if risk == "moderate":
        return "🟡 Déficit intégrité académique structurel actif"
    return "🟢 Intégrité recherche sous surveillance"


def analyze_academic_integrity(e: AcademicIntegrityInput) -> AcademicIntegrityResult:
    fraud = _fraud_score(e)
    publishing = _publishing_score(e)
    replication = _replication_score(e)
    governance = _governance_score(e)
    composite = _composite_score(fraud, publishing, replication, governance)
    risk = _risk_level(composite)
    pattern = _integrity_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return AcademicIntegrityResult(
        entity_id=e.entity_id,
        research_field=e.research_field,
        region=e.region,
        fraud_score=fraud,
        publishing_score=publishing,
        replication_score=replication,
        governance_score=governance,
        composite_score=composite,
        risk_level=risk,
        integrity_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        retraction_rate=e.retraction_rate,
        data_fabrication_index=e.data_fabrication_index,
    )


class AcademicIntegrityEngine:
    def analyze(self, entities: List[AcademicIntegrityInput]) -> Dict[str, Any]:
        results = [analyze_academic_integrity(e) for e in entities]

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
            pattern_distribution[r.integrity_pattern] = pattern_distribution.get(r.integrity_pattern, 0) + 1
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
        results: List[AcademicIntegrityResult] = None,
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
            "module_id": 428,
            "module_name": "Intégrité Recherche Académique & Fraude Scientifique Intelligence Engine",
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
            "avg_estimated_research_integrity_index": round(avg_composite / 100 * 10, 2),
        }
