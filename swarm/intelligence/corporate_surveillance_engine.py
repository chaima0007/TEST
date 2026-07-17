"""
Module 381 — Corporate Surveillance & Employee Monitoring Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CorporateSurveillanceInput:
    entity_id: str
    industry_type: str
    region: str
    # 17 float fields (0.0–1.0)
    employee_monitoring_intensity: float
    productivity_scoring_opacity: float
    biometric_workplace_data: float
    algorithmic_management_control: float
    consumer_behavior_extraction: float
    location_tracking_scope: float
    emotion_recognition_deployment: float
    keystroke_surveillance: float
    performance_anxiety_induction: float
    union_busting_surveillance: float
    consumer_manipulation_depth: float
    health_data_employer_access: float
    housing_tenant_surveillance: float
    gig_worker_score_opacity: float
    data_broker_corporate_integration: float
    regulatory_capture_privacy: float
    psychological_profiling_depth: float


@dataclass
class CorporateSurveillanceResult:
    entity_id: str
    industry_type: str
    region: str
    monitoring_score: float
    manipulation_score: float
    extraction_score: float
    control_score: float
    composite_score: float
    risk_level: str
    surveillance_pattern: str
    severity: str
    recommended_action: str
    signal: str
    employee_monitoring_intensity: float
    biometric_workplace_data: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "industry_type": self.industry_type,
            "region": self.region,
            "monitoring_score": self.monitoring_score,
            "manipulation_score": self.manipulation_score,
            "extraction_score": self.extraction_score,
            "control_score": self.control_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "surveillance_pattern": self.surveillance_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "employee_monitoring_intensity": self.employee_monitoring_intensity,
            "biometric_workplace_data": self.biometric_workplace_data,
        }


def _monitoring_score(inp: CorporateSurveillanceInput) -> float:
    raw = (
        inp.employee_monitoring_intensity * 0.4
        + inp.keystroke_surveillance * 0.35
        + inp.biometric_workplace_data * 0.25
    ) * 100
    return round(raw * 100) / 100


def _manipulation_score(inp: CorporateSurveillanceInput) -> float:
    raw = (
        inp.consumer_manipulation_depth * 0.4
        + inp.psychological_profiling_depth * 0.35
        + inp.performance_anxiety_induction * 0.25
    ) * 100
    return round(raw * 100) / 100


def _extraction_score(inp: CorporateSurveillanceInput) -> float:
    raw = (
        inp.consumer_behavior_extraction * 0.4
        + inp.data_broker_corporate_integration * 0.35
        + inp.location_tracking_scope * 0.25
    ) * 100
    return round(raw * 100) / 100


def _control_score(inp: CorporateSurveillanceInput) -> float:
    raw = (
        inp.algorithmic_management_control * 0.4
        + inp.regulatory_capture_privacy * 0.35
        + inp.union_busting_surveillance * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    monitoring: float,
    manipulation: float,
    extraction: float,
    control: float,
) -> float:
    return round(
        monitoring * 0.30
        + manipulation * 0.25
        + extraction * 0.25
        + control * 0.20,
        2,
    )


def _surveillance_pattern(inp: CorporateSurveillanceInput) -> str:
    if inp.employee_monitoring_intensity > 0.85 and inp.biometric_workplace_data > 0.80:
        return "total_employee_surveillance"
    if inp.algorithmic_management_control > 0.85 and inp.productivity_scoring_opacity > 0.80:
        return "algorithmic_management_tyranny"
    if inp.consumer_manipulation_depth > 0.85 and inp.psychological_profiling_depth > 0.80:
        return "consumer_manipulation_empire"
    if inp.gig_worker_score_opacity > 0.80 and inp.union_busting_surveillance > 0.75:
        return "gig_worker_score_oppression"
    if inp.health_data_employer_access > 0.80 and inp.housing_tenant_surveillance > 0.75:
        return "health_housing_surveillance_fusion"
    return "none"


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _severity(risk: str) -> str:
    if risk == "critical":
        return "surveillance_corporative_totale"
    if risk == "high":
        return "controle_employes_massif"
    if risk == "moderate":
        return "surveillance_structurelle_active"
    return "surveillance_contenue"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "regulation_surveillance_employes_urgente"
    if risk == "high":
        return "demantelement_controle_algorithmique"
    if risk == "moderate":
        return "renforcement_droits_travailleurs"
    return "veille_surveillance_corporative"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Surveillance corporative totale — contrôle employés systémique"
    if risk == "high":
        return "🟠 Contrôle des employés massif détecté"
    if risk == "moderate":
        return "🟡 Surveillance structurelle active des employés"
    return "🟢 Surveillance corporative contenue"


def analyze(inp: CorporateSurveillanceInput) -> CorporateSurveillanceResult:
    mon = _monitoring_score(inp)
    man = _manipulation_score(inp)
    ext = _extraction_score(inp)
    ctrl = _control_score(inp)
    comp = _composite(mon, man, ext, ctrl)
    pat = _surveillance_pattern(inp)
    risk = _risk_level(comp)
    sev = _severity(risk)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return CorporateSurveillanceResult(
        entity_id=inp.entity_id,
        industry_type=inp.industry_type,
        region=inp.region,
        monitoring_score=mon,
        manipulation_score=man,
        extraction_score=ext,
        control_score=ctrl,
        composite_score=comp,
        risk_level=risk,
        surveillance_pattern=pat,
        severity=sev,
        recommended_action=action,
        signal=sig,
        employee_monitoring_intensity=inp.employee_monitoring_intensity,
        biometric_workplace_data=inp.biometric_workplace_data,
    )


class CorporateSurveillanceEngine:
    def __init__(self, inputs: List[CorporateSurveillanceInput]):
        self.inputs = inputs
        self.results: List[CorporateSurveillanceResult] = [analyze(i) for i in inputs]

    def analyze(self, entities: List[CorporateSurveillanceInput]) -> Dict[str, Any]:
        results = [analyze(e) for e in entities]
        return self.summary([r.to_dict() for r in results])

    @staticmethod
    def summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
        n = len(results)
        if n == 0:
            return {}

        pattern_distribution: Dict[str, int] = {}
        risk_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in results:
            risk = r["risk_level"]
            pat = r["surveillance_pattern"]
            sev = r["severity"]
            act = r["recommended_action"]

            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
            pattern_distribution[pat] = pattern_distribution.get(pat, 0) + 1
            severity_distribution[sev] = severity_distribution.get(sev, 0) + 1
            action_distribution[act] = action_distribution.get(act, 0) + 1

            total_composite += r["composite_score"]

            if risk == "critical":
                critical_count += 1
            elif risk == "high":
                high_count += 1
            elif risk == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        avg_composite = round(total_composite / n, 2)

        # 13 keys: module_id, module_name, total, critical, high, moderate, low,
        # avg_composite, pattern_distribution, risk_distribution,
        # severity_distribution, action_distribution,
        # avg_estimated_corporate_surveillance_index
        return {
            "module_id": 381,
            "module_name": "Corporate Surveillance & Employee Monitoring Intelligence Engine",
            "total": n,
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_corporate_surveillance_index": round(avg_composite / 100 * 10, 2),
        }
