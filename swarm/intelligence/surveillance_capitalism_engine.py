"""
Module 335 — Surveillance Capitalism & Data Extraction Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SurveillanceCapitalismInput:
    entity_id: str
    platform_type: str
    region: str
    # 17 float fields (0.0–1.0)
    behavioral_surplus_extraction_rate: float
    prediction_product_invasiveness: float
    attention_capture_monopoly: float
    psychological_profiling_depth: float
    consent_manufacturing_level: float
    behavioral_modification_intensity: float
    data_broker_ecosystem_density: float
    third_party_surveillance_reach: float
    shadow_profiling_prevalence: float
    continuous_tracking_saturation: float
    intimate_data_commodification: float
    behavioral_futures_market_size: float
    autonomy_erosion_index: float
    prediction_weaponization_rate: float
    surveillance_competitive_advantage: float
    data_colonialism_index: float
    behavioral_totalitarianism_risk: float


@dataclass
class SurveillanceCapitalismResult:
    entity_id: str
    platform_type: str
    region: str
    extraction_score: float
    manipulation_score: float
    profiling_score: float
    autonomy_score: float
    composite_score: float
    risk_level: str
    surveillance_pattern: str
    severity: str
    recommended_action: str
    signal: str
    behavioral_surplus_extraction_rate: float
    behavioral_totalitarianism_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "platform_type": self.platform_type,
            "region": self.region,
            "extraction_score": self.extraction_score,
            "manipulation_score": self.manipulation_score,
            "profiling_score": self.profiling_score,
            "autonomy_score": self.autonomy_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "surveillance_pattern": self.surveillance_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "behavioral_surplus_extraction_rate": self.behavioral_surplus_extraction_rate,
            "behavioral_totalitarianism_risk": self.behavioral_totalitarianism_risk,
        }


def _extraction_score(inp: SurveillanceCapitalismInput) -> float:
    raw = (
        inp.behavioral_surplus_extraction_rate * 0.4
        + inp.behavioral_futures_market_size * 0.35
        + inp.data_broker_ecosystem_density * 0.25
    ) * 100
    return round(raw * 100) / 100


def _manipulation_score(inp: SurveillanceCapitalismInput) -> float:
    raw = (
        inp.behavioral_modification_intensity * 0.4
        + inp.attention_capture_monopoly * 0.35
        + inp.consent_manufacturing_level * 0.25
    ) * 100
    return round(raw * 100) / 100


def _profiling_score(inp: SurveillanceCapitalismInput) -> float:
    raw = (
        inp.psychological_profiling_depth * 0.4
        + inp.shadow_profiling_prevalence * 0.35
        + inp.intimate_data_commodification * 0.25
    ) * 100
    return round(raw * 100) / 100


def _autonomy_score(inp: SurveillanceCapitalismInput) -> float:
    raw = (
        inp.autonomy_erosion_index * 0.4
        + inp.behavioral_totalitarianism_risk * 0.35
        + inp.data_colonialism_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    extraction: float,
    manipulation: float,
    profiling: float,
    autonomy: float,
) -> float:
    return round(
        extraction * 0.30
        + manipulation * 0.25
        + profiling * 0.25
        + autonomy * 0.20,
        2,
    )


def _surveillance_pattern(inp: SurveillanceCapitalismInput) -> str:
    if inp.behavioral_totalitarianism_risk >= 0.70 and inp.autonomy_erosion_index >= 0.65:
        return "behavioral_totalitarianism"
    if inp.prediction_product_invasiveness >= 0.70 and inp.behavioral_futures_market_size >= 0.65:
        return "prediction_product_hegemony"
    if inp.consent_manufacturing_level >= 0.70 and inp.behavioral_modification_intensity >= 0.65:
        return "consent_manufacturing_crisis"
    if inp.shadow_profiling_prevalence >= 0.70 and inp.psychological_profiling_depth >= 0.65:
        return "shadow_profiling_empire"
    if inp.data_colonialism_index >= 0.70 and inp.third_party_surveillance_reach >= 0.65:
        return "data_colonialism"
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
        return "capitalisme_surveillance_total"
    if risk == "high":
        return "extraction_comportementale_massive"
    if risk == "moderate":
        return "surveillance_structurelle_active"
    return "surveillance_contenue"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "régulation_surveillance_urgente"
    if risk == "high":
        return "démantèlement_extraction_comportementale"
    if risk == "moderate":
        return "renforcement_consentement_éclairé"
    return "veille_surveillance_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Capitalisme de surveillance total — extraction comportementale systémique"
    if risk == "high":
        return "🟠 Extraction comportementale massive détectée"
    if risk == "moderate":
        return "🟡 Surveillance structurelle active"
    return "🟢 Surveillance capitaliste contenue"


def analyze(inp: SurveillanceCapitalismInput) -> SurveillanceCapitalismResult:
    ext = _extraction_score(inp)
    man = _manipulation_score(inp)
    pro = _profiling_score(inp)
    aut = _autonomy_score(inp)
    comp = _composite(ext, man, pro, aut)
    pat = _surveillance_pattern(inp)
    risk = _risk_level(comp)
    sev = _severity(risk)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return SurveillanceCapitalismResult(
        entity_id=inp.entity_id,
        platform_type=inp.platform_type,
        region=inp.region,
        extraction_score=ext,
        manipulation_score=man,
        profiling_score=pro,
        autonomy_score=aut,
        composite_score=comp,
        risk_level=risk,
        surveillance_pattern=pat,
        severity=sev,
        recommended_action=action,
        signal=sig,
        behavioral_surplus_extraction_rate=inp.behavioral_surplus_extraction_rate,
        behavioral_totalitarianism_risk=inp.behavioral_totalitarianism_risk,
    )


class SurveillanceCapitalismEngine:
    def __init__(self, inputs: List[SurveillanceCapitalismInput]):
        self.inputs = inputs
        self.results: List[SurveillanceCapitalismResult] = [analyze(i) for i in inputs]

    def analyze(self, entities: List[SurveillanceCapitalismInput]) -> Dict[str, Any]:
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

        return {
            "module_id": 335,
            "module_name": "Surveillance Capitalism & Data Extraction Intelligence Engine",
            "total_entities": n,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_surveillance_capitalism_index": round(avg_composite / 100 * 10, 2),
        }
