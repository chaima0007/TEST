from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class PsychedelicMedicineInput:
    entity_id: str
    substance_category: str
    region: str
    clinical_evidence_gap: float
    fda_scheduling_barrier: float
    insurance_coverage_exclusion: float
    therapist_training_deficit: float
    clinical_trial_access: float
    indigenous_knowledge_theft: float
    commercialization_monopoly_risk: float
    harm_reduction_suppression: float
    mental_health_treatment_gap: float
    war_on_drugs_incarceration: float
    racial_disparity_enforcement: float
    decriminalization_policy_gap: float
    patient_access_equity: float
    research_funding_barrier: float
    synthetic_analogues_risk: float
    underground_session_risk: float
    informed_consent_gap: float


@dataclass
class PsychedelicMedicineResult:
    entity_id: str
    substance_category: str
    region: str
    clinical_score: float
    access_score: float
    regulatory_score: float
    equity_score: float
    composite_score: float
    risk_level: str
    psychedelic_pattern: str
    severity: str
    recommended_action: str
    signal: str
    clinical_trial_access: float
    racial_disparity_enforcement: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "substance_category": self.substance_category,
            "region": self.region,
            "clinical_score": self.clinical_score,
            "access_score": self.access_score,
            "regulatory_score": self.regulatory_score,
            "equity_score": self.equity_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "psychedelic_pattern": self.psychedelic_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "clinical_trial_access": self.clinical_trial_access,
            "racial_disparity_enforcement": self.racial_disparity_enforcement,
        }


def _clinical_score(e: PsychedelicMedicineInput) -> float:
    raw = (
        e.clinical_evidence_gap * 0.4
        + e.research_funding_barrier * 0.35
        + e.informed_consent_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _access_score(e: PsychedelicMedicineInput) -> float:
    raw = (
        e.clinical_trial_access * 0.4
        + e.insurance_coverage_exclusion * 0.35
        + e.therapist_training_deficit * 0.25
    ) * 100
    return round(raw * 100) / 100


def _regulatory_score(e: PsychedelicMedicineInput) -> float:
    raw = (
        e.fda_scheduling_barrier * 0.4
        + e.decriminalization_policy_gap * 0.35
        + e.harm_reduction_suppression * 0.25
    ) * 100
    return round(raw * 100) / 100


def _equity_score(e: PsychedelicMedicineInput) -> float:
    raw = (
        e.racial_disparity_enforcement * 0.4
        + e.war_on_drugs_incarceration * 0.35
        + e.patient_access_equity * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    clinical: float,
    access: float,
    regulatory: float,
    equity: float,
) -> float:
    return round(
        (clinical * 0.30 + access * 0.25 + regulatory * 0.25 + equity * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _psychedelic_pattern(e: PsychedelicMedicineInput) -> str:
    if e.clinical_trial_access > 0.85 and e.research_funding_barrier > 0.80:
        return "clinical_trial_access_barrier"
    if e.fda_scheduling_barrier > 0.85 and e.decriminalization_policy_gap > 0.80:
        return "regulatory_scheduling_blockade"
    if e.commercialization_monopoly_risk > 0.85 and e.insurance_coverage_exclusion > 0.80:
        return "commercialization_equity_gap"
    if e.indigenous_knowledge_theft > 0.80 and e.commercialization_monopoly_risk > 0.75:
        return "indigenous_knowledge_appropriation"
    if e.harm_reduction_suppression > 0.80 and e.underground_session_risk > 0.75:
        return "harm_reduction_policy_failure"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_médecine_psychédélique_systémique"
    if composite >= 40:
        return "blocage_réforme_politique_drogues_majeur"
    if composite >= 20:
        return "inégalité_accès_thérapies_psychédéliques"
    return "surveillance_réforme_politique_drogues"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_réforme_politique_drogues_critique"
    if risk == "high":
        return "accélération_déprogrammation_accès_essais_cliniques"
    if risk == "moderate":
        return "renforcement_politiques_médecine_psychédélique"
    return "veille_réforme_drogues_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise médecine psychédélique systémique — réforme politique drogues en péril"
    if risk == "high":
        return "🟠 Blocage réforme politique drogues majeur détecté"
    if risk == "moderate":
        return "🟡 Inégalité accès thérapies psychédéliques active"
    return "🟢 Surveillance réforme politique drogues"


def analyze_psychedelic_medicine(e: PsychedelicMedicineInput) -> PsychedelicMedicineResult:
    clinical = _clinical_score(e)
    access = _access_score(e)
    regulatory = _regulatory_score(e)
    equity = _equity_score(e)
    composite = _composite_score(clinical, access, regulatory, equity)
    risk = _risk_level(composite)
    pattern = _psychedelic_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return PsychedelicMedicineResult(
        entity_id=e.entity_id,
        substance_category=e.substance_category,
        region=e.region,
        clinical_score=clinical,
        access_score=access,
        regulatory_score=regulatory,
        equity_score=equity,
        composite_score=composite,
        risk_level=risk,
        psychedelic_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        clinical_trial_access=e.clinical_trial_access,
        racial_disparity_enforcement=e.racial_disparity_enforcement,
    )


class PsychedelicMedicineEngine:
    def analyze(self, entities: List[PsychedelicMedicineInput]) -> Dict[str, Any]:
        results = [analyze_psychedelic_medicine(e) for e in entities]

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
            pattern_distribution[r.psychedelic_pattern] = pattern_distribution.get(r.psychedelic_pattern, 0) + 1
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
        results: List[PsychedelicMedicineResult] = None,
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
            "module_id": 437,
            "module_name": "Médecine Psychédélique & Réforme Politique des Drogues Intelligence Engine",
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
            "avg_estimated_drug_reform_index": round(avg_composite / 100 * 10, 2),
        }
