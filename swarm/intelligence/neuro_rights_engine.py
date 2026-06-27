from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class NeuroRightsInput:
    entity_id: str
    neurotechnology_type: str
    region: str
    neural_data_collection: float
    mental_privacy_protection: float
    cognitive_manipulation_risk: float
    bci_corporate_control: float
    informed_consent_quality: float
    algorithmic_thought_influence: float
    emotion_detection_deployment: float
    memory_augmentation_inequality: float
    mental_health_surveillance: float
    neuro_data_commercialization: float
    regulatory_framework_gap: float
    equity_of_enhancement_access: float
    cross_border_data_flow: float
    re_identification_risk: float
    military_application_risk: float
    therapeutic_vs_enhancement_boundary: float
    judicial_neural_evidence: float


@dataclass
class NeuroRightsResult:
    entity_id: str
    neurotechnology_type: str
    region: str
    mental_privacy_score: float
    cognitive_liberty_score: float
    consent_score: float
    equity_score: float
    composite_score: float
    risk_level: str
    neuro_pattern: str
    severity: str
    recommended_action: str
    signal: str
    neural_data_collection: float
    cognitive_manipulation_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "neurotechnology_type": self.neurotechnology_type,
            "region": self.region,
            "mental_privacy_score": self.mental_privacy_score,
            "cognitive_liberty_score": self.cognitive_liberty_score,
            "consent_score": self.consent_score,
            "equity_score": self.equity_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "neuro_pattern": self.neuro_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "neural_data_collection": self.neural_data_collection,
            "cognitive_manipulation_risk": self.cognitive_manipulation_risk,
        }


def _mental_privacy_score(e: NeuroRightsInput) -> float:
    raw = (
        e.neural_data_collection * 0.4
        + e.mental_health_surveillance * 0.35
        + e.re_identification_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _cognitive_liberty_score(e: NeuroRightsInput) -> float:
    raw = (
        e.cognitive_manipulation_risk * 0.4
        + e.algorithmic_thought_influence * 0.35
        + e.bci_corporate_control * 0.25
    ) * 100
    return round(raw * 100) / 100


def _consent_score(e: NeuroRightsInput) -> float:
    raw = (
        (1.0 - e.informed_consent_quality) * 0.4
        + e.regulatory_framework_gap * 0.35
        + e.neuro_data_commercialization * 0.25
    ) * 100
    return round(raw * 100) / 100


def _equity_score(e: NeuroRightsInput) -> float:
    raw = (
        e.memory_augmentation_inequality * 0.4
        + (1.0 - e.equity_of_enhancement_access) * 0.35
        + e.military_application_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    privacy: float,
    liberty: float,
    consent: float,
    equity: float,
) -> float:
    return round(
        (privacy * 0.30 + liberty * 0.25 + consent * 0.25 + equity * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _neuro_pattern(e: NeuroRightsInput) -> str:
    if e.neural_data_collection > 0.85 and e.mental_health_surveillance > 0.80:
        return "mental_surveillance_state"
    if e.cognitive_manipulation_risk > 0.85 and e.algorithmic_thought_influence > 0.80:
        return "cognitive_manipulation_crisis"
    if e.neuro_data_commercialization > 0.85 and e.re_identification_risk > 0.80:
        return "neural_data_commodification"
    if e.bci_corporate_control > 0.80 and e.regulatory_framework_gap > 0.75:
        return "bci_corporate_monopoly"
    if e.memory_augmentation_inequality > 0.80 and e.equity_of_enhancement_access < 0.25:
        return "brain_enhancement_inequality"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_neurodroits_systémique"
    if composite >= 40:
        return "crise_souveraineté_cérébrale_majeure"
    if composite >= 20:
        return "inégalité_neuro_structurelle"
    return "neurodroits_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_protection_neurodroits"
    if risk == "high":
        return "régulation_neurotechnologies_accélérée"
    if risk == "moderate":
        return "renforcement_cadre_consentement_neuronal"
    return "veille_neurodroits_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise neurodroits systémique — souveraineté cérébrale en péril"
    if risk == "high":
        return "🟠 Crise souveraineté cérébrale majeure détectée"
    if risk == "moderate":
        return "🟡 Inégalité neuro structurelle active"
    return "🟢 Neurodroits sous surveillance"


def analyze_neuro_rights(e: NeuroRightsInput) -> NeuroRightsResult:
    privacy = _mental_privacy_score(e)
    liberty = _cognitive_liberty_score(e)
    consent = _consent_score(e)
    equity = _equity_score(e)
    composite = _composite_score(privacy, liberty, consent, equity)
    risk = _risk_level(composite)
    pattern = _neuro_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return NeuroRightsResult(
        entity_id=e.entity_id,
        neurotechnology_type=e.neurotechnology_type,
        region=e.region,
        mental_privacy_score=privacy,
        cognitive_liberty_score=liberty,
        consent_score=consent,
        equity_score=equity,
        composite_score=composite,
        risk_level=risk,
        neuro_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        neural_data_collection=e.neural_data_collection,
        cognitive_manipulation_risk=e.cognitive_manipulation_risk,
    )


class NeuroRightsEngine:
    def analyze(self, entities: List[NeuroRightsInput]) -> Dict[str, Any]:
        results = [analyze_neuro_rights(e) for e in entities]

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
            pattern_distribution[r.neuro_pattern] = pattern_distribution.get(r.neuro_pattern, 0) + 1
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
        results: List[NeuroRightsResult] = None,
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
            "module_id": 416,
            "module_name": "Neurodroits & Souveraineté Données Cérébrales Intelligence Engine",
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
            "avg_estimated_neuro_rights_index": round(avg_composite / 100 * 10, 2),
        }
