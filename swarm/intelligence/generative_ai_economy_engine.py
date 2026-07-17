"""
Module 350 — Generative AI & Creative Economy Disruption Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GenerativeAIEconomyInput:
    entity_id: str
    creative_sector: str
    region: str
    # 17 float fields (0.0–1.0)
    AI_creative_displacement_rate: float
    copyright_training_data_exploitation: float
    creator_income_collapse_index: float
    AI_aesthetic_homogenization_risk: float
    generative_model_monopoly_concentration: float
    human_creativity_devaluation: float
    cultural_diversity_AI_erosion: float
    misinformation_synthetic_content_volume: float
    AI_plagiarism_undetectability: float
    creative_class_economic_collapse: float
    AI_gatekeeper_content_control: float
    authenticity_market_collapse: float
    AI_artistic_labor_substitution: float
    emotional_labor_AI_replacement_risk: float
    creative_IP_extraction_rate: float
    training_consent_violation_scale: float
    AI_cultural_production_homogeny: float


@dataclass
class GenerativeAIEconomyResult:
    entity_id: str
    creative_sector: str
    region: str
    displacement_score: float
    control_score: float
    culture_score: float
    integrity_score: float
    composite_score: float
    risk_level: str
    genai_pattern: str
    severity: str
    recommended_action: str
    signal: str
    AI_creative_displacement_rate: float
    generative_model_monopoly_concentration: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "creative_sector": self.creative_sector,
            "region": self.region,
            "displacement_score": self.displacement_score,
            "control_score": self.control_score,
            "culture_score": self.culture_score,
            "integrity_score": self.integrity_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "genai_pattern": self.genai_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "AI_creative_displacement_rate": self.AI_creative_displacement_rate,
            "generative_model_monopoly_concentration": self.generative_model_monopoly_concentration,
        }


def _displacement_score(inp: GenerativeAIEconomyInput) -> float:
    raw = (
        inp.AI_creative_displacement_rate * 0.4
        + inp.creator_income_collapse_index * 0.35
        + inp.AI_artistic_labor_substitution * 0.25
    ) * 100
    return round(raw * 100) / 100


def _control_score(inp: GenerativeAIEconomyInput) -> float:
    raw = (
        inp.generative_model_monopoly_concentration * 0.4
        + inp.AI_gatekeeper_content_control * 0.35
        + inp.copyright_training_data_exploitation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _culture_score(inp: GenerativeAIEconomyInput) -> float:
    raw = (
        inp.AI_aesthetic_homogenization_risk * 0.4
        + inp.cultural_diversity_AI_erosion * 0.35
        + inp.AI_cultural_production_homogeny * 0.25
    ) * 100
    return round(raw * 100) / 100


def _integrity_score(inp: GenerativeAIEconomyInput) -> float:
    raw = (
        inp.misinformation_synthetic_content_volume * 0.4
        + inp.AI_plagiarism_undetectability * 0.35
        + inp.authenticity_market_collapse * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    displacement: float,
    control: float,
    culture: float,
    integrity: float,
) -> float:
    return round(
        displacement * 0.30
        + control * 0.25
        + culture * 0.25
        + integrity * 0.20,
        2,
    )


def _genai_pattern(inp: GenerativeAIEconomyInput) -> str:
    if inp.AI_creative_displacement_rate >= 0.70 and inp.creator_income_collapse_index >= 0.65:
        return "creative_class_extinction"
    if inp.generative_model_monopoly_concentration >= 0.70 and inp.AI_gatekeeper_content_control >= 0.65:
        return "generative_monopoly_capture"
    if inp.AI_aesthetic_homogenization_risk >= 0.70 and inp.AI_cultural_production_homogeny >= 0.65:
        return "cultural_homogenization_crisis"
    if inp.copyright_training_data_exploitation >= 0.70 and inp.training_consent_violation_scale >= 0.65:
        return "IP_extraction_empire"
    if inp.misinformation_synthetic_content_volume >= 0.70 and inp.AI_plagiarism_undetectability >= 0.65:
        return "synthetic_content_saturation"
    return "none"


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "effondrement_économie_créative"
    if composite >= 40:
        return "disruption_créative_majeure"
    if composite >= 20:
        return "restructuration_créative_active"
    return "disruption_créative_gérée"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "protection_urgente_économie_créative"
    if risk == "high":
        return "régulation_IA_générative_stricte"
    if risk == "moderate":
        return "renforcement_droits_créateurs_IA"
    return "veille_disruption_créative_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Effondrement économie créative — IA générative systémique"
    if risk == "high":
        return "🟠 Disruption créative majeure détectée"
    if risk == "moderate":
        return "🟡 Restructuration créative active en cours"
    return "🟢 Disruption créative gérée et surveillée"


def analyze(inp: GenerativeAIEconomyInput) -> GenerativeAIEconomyResult:
    disp = _displacement_score(inp)
    ctrl = _control_score(inp)
    cult = _culture_score(inp)
    intg = _integrity_score(inp)
    comp = _composite(disp, ctrl, cult, intg)
    pat = _genai_pattern(inp)
    risk = _risk_level(comp)
    sev = _severity(comp)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return GenerativeAIEconomyResult(
        entity_id=inp.entity_id,
        creative_sector=inp.creative_sector,
        region=inp.region,
        displacement_score=disp,
        control_score=ctrl,
        culture_score=cult,
        integrity_score=intg,
        composite_score=comp,
        risk_level=risk,
        genai_pattern=pat,
        severity=sev,
        recommended_action=action,
        signal=sig,
        AI_creative_displacement_rate=inp.AI_creative_displacement_rate,
        generative_model_monopoly_concentration=inp.generative_model_monopoly_concentration,
    )


class GenerativeAIEconomyEngine:
    def __init__(self, inputs: List[GenerativeAIEconomyInput]):
        self.inputs = inputs
        self.results: List[GenerativeAIEconomyResult] = [analyze(i) for i in inputs]

    def summary(self) -> Dict[str, Any]:
        n = len(self.results)
        if n == 0:
            return {}

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0
        total_composite = 0.0

        for r in self.results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            pattern_distribution[r.genai_pattern] = pattern_distribution.get(r.genai_pattern, 0) + 1
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

        avg_composite = round(total_composite / n, 1)

        return {
            "module_id": 350,
            "module_name": "Generative AI & Creative Economy Disruption Intelligence Engine",
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
            "avg_estimated_creative_disruption_index": round(avg_composite / 100 * 10, 2),
        }
