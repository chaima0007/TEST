"""
Module 360 — AI Governance & Regulatory Intelligence Engine
Caelum Partners — Chaima Mhadbi, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AIGovernanceInput:
    entity_id: str
    governance_context: str
    region: str
    # 17 float fields (0-1)
    AI_regulatory_fragmentation_index: float
    AI_safety_standard_gap: float
    autonomous_system_accountability_vacuum: float
    AI_liability_unclarity_risk: float
    algorithmic_auditing_deficit: float
    AI_international_cooperation_failure: float
    AI_compute_governance_gap: float
    AI_training_data_governance_risk: float
    AI_deployment_speed_vs_governance_gap: float
    existential_risk_regulatory_blindspot: float
    AI_market_concentration_regulatory_gap: float
    democratic_AI_oversight_weakness: float
    AI_whistleblower_protection_gap: float
    AI_incident_reporting_deficit: float
    regulatory_capture_by_AI_industry: float
    AI_rights_legal_framework_absence: float
    AI_geopolitical_standards_war: float


def _regulatory_score(inp: AIGovernanceInput) -> float:
    raw = (
        inp.AI_regulatory_fragmentation_index * 0.4
        + inp.AI_safety_standard_gap * 0.35
        + inp.AI_deployment_speed_vs_governance_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _accountability_score(inp: AIGovernanceInput) -> float:
    raw = (
        inp.autonomous_system_accountability_vacuum * 0.4
        + inp.AI_liability_unclarity_risk * 0.35
        + inp.algorithmic_auditing_deficit * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(inp: AIGovernanceInput) -> float:
    raw = (
        inp.AI_international_cooperation_failure * 0.4
        + inp.democratic_AI_oversight_weakness * 0.35
        + inp.regulatory_capture_by_AI_industry * 0.25
    ) * 100
    return round(raw * 100) / 100


def _systemic_score(inp: AIGovernanceInput) -> float:
    raw = (
        inp.existential_risk_regulatory_blindspot * 0.4
        + inp.AI_market_concentration_regulatory_gap * 0.35
        + inp.AI_geopolitical_standards_war * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    regulatory: float,
    accountability: float,
    governance: float,
    systemic: float,
) -> float:
    return round(
        regulatory * 0.30
        + accountability * 0.25
        + governance * 0.25
        + systemic * 0.20,
        2,
    )


def _ai_governance_pattern(inp: AIGovernanceInput) -> str:
    if inp.AI_regulatory_fragmentation_index >= 0.70 and inp.AI_deployment_speed_vs_governance_gap >= 0.65:
        return "governance_vacuum_crisis"
    if inp.autonomous_system_accountability_vacuum >= 0.70 and inp.AI_liability_unclarity_risk >= 0.65:
        return "accountability_collapse"
    if inp.regulatory_capture_by_AI_industry >= 0.70 and inp.democratic_AI_oversight_weakness >= 0.65:
        return "AI_regulatory_capture"
    if inp.existential_risk_regulatory_blindspot >= 0.70 and inp.AI_safety_standard_gap >= 0.65:
        return "existential_risk_blindspot"
    if inp.AI_geopolitical_standards_war >= 0.70 and inp.AI_international_cooperation_failure >= 0.65:
        return "geopolitical_standards_war"
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
        return "vide_gouvernance_IA_systémique"
    if risk == "high":
        return "crise_régulation_IA_majeure"
    if risk == "moderate":
        return "fragilité_gouvernance_IA_structurelle"
    return "gouvernance_IA_relative"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_gouvernance_IA_urgente"
    if risk == "high":
        return "régulation_IA_internationale_accélérée"
    if risk == "moderate":
        return "renforcement_oversight_IA_démocratique"
    return "veille_gouvernance_IA_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Vide gouvernance IA systémique — IA hors contrôle démocratique"
    if risk == "high":
        return "🟠 Crise régulation IA majeure détectée"
    if risk == "moderate":
        return "🟡 Fragilité gouvernance IA structurelle active"
    return "🟢 Gouvernance IA relativement maintenue"


def _analyze_one(inp: AIGovernanceInput) -> Dict[str, Any]:
    reg = _regulatory_score(inp)
    acc = _accountability_score(inp)
    gov = _governance_score(inp)
    sys = _systemic_score(inp)
    comp = _composite(reg, acc, gov, sys)
    pat = _ai_governance_pattern(inp)
    risk = _risk_level(comp)
    sev = _severity(risk)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return {
        "entity_id": inp.entity_id,
        "governance_context": inp.governance_context,
        "region": inp.region,
        "regulatory_score": reg,
        "accountability_score": acc,
        "governance_score": gov,
        "systemic_score": sys,
        "composite_score": comp,
        "risk_level": risk,
        "ai_governance_pattern": pat,
        "severity": sev,
        "recommended_action": action,
        "signal": sig,
        "AI_regulatory_fragmentation_index": inp.AI_regulatory_fragmentation_index,
        "existential_risk_regulatory_blindspot": inp.existential_risk_regulatory_blindspot,
    }


class AIGovernanceEngine:
    def __init__(self, inputs: List[AIGovernanceInput]):
        self.inputs = inputs
        self._results: List[Dict[str, Any]] = []

    def analyze_all(self) -> List[Dict[str, Any]]:
        self._results = [_analyze_one(inp) for inp in self.inputs]
        return self._results

    def summary(self) -> Dict[str, Any]:
        if not self._results:
            self.analyze_all()

        n = len(self._results)
        if n == 0:
            return {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0
        pattern_distribution: Dict[str, int] = {}
        risk_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        for r in self._results:
            total_composite += r["composite_score"]

            risk = r["risk_level"]
            if risk == "critical":
                critical_count += 1
            elif risk == "high":
                high_count += 1
            elif risk == "moderate":
                moderate_count += 1
            else:
                low_count += 1

            pat = r["ai_governance_pattern"]
            pattern_distribution[pat] = pattern_distribution.get(pat, 0) + 1

            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1

            sev = r["severity"]
            severity_distribution[sev] = severity_distribution.get(sev, 0) + 1

            action = r["recommended_action"]
            action_distribution[action] = action_distribution.get(action, 0) + 1

        avg_composite = round(total_composite / n, 2)

        return {
            "module_id": 360,
            "module_name": "AI Governance & Regulatory Intelligence Engine",
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
            "avg_estimated_ai_governance_index": round(avg_composite / 100 * 10, 2),
        }
