"""
Module 383 — Industrial Policy & Reshoring Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class IndustrialPolicyInput:
    entity_id: str
    industrial_sector: str
    region: str
    # 17 float fields (0.0–1.0)
    strategic_dependency_exposure: float
    reshoring_policy_effectiveness: float
    friend_shoring_progress: float
    industrial_subsidy_distortion: float
    supply_chain_resilience_gap: float
    semiconductor_dependency: float
    pharmaceutical_reshoring_lag: float
    green_tech_manufacturing_gap: float
    workforce_skills_mismatch: float
    regulatory_fragmentation: float
    protectionism_trade_war_risk: float
    IRA_like_subsidy_race: float
    strategic_autonomy_index: float
    de_risking_progress: float
    manufacturing_capacity_gap: float
    innovation_policy_effectiveness: float
    geopolitical_industrial_leverage: float


@dataclass
class IndustrialPolicyResult:
    entity_id: str
    industrial_sector: str
    region: str
    dependency_score: float
    policy_score: float
    resilience_score: float
    geopolitical_score: float
    composite_score: float
    risk_level: str
    industrial_pattern: str
    severity: str
    recommended_action: str
    signal: str
    strategic_dependency_exposure: float
    semiconductor_dependency: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "industrial_sector": self.industrial_sector,
            "region": self.region,
            "dependency_score": self.dependency_score,
            "policy_score": self.policy_score,
            "resilience_score": self.resilience_score,
            "geopolitical_score": self.geopolitical_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "industrial_pattern": self.industrial_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "strategic_dependency_exposure": self.strategic_dependency_exposure,
            "semiconductor_dependency": self.semiconductor_dependency,
        }


def _dependency_score(inp: IndustrialPolicyInput) -> float:
    raw = (
        inp.strategic_dependency_exposure * 0.4
        + inp.semiconductor_dependency * 0.35
        + inp.pharmaceutical_reshoring_lag * 0.25
    ) * 100
    return round(raw * 100) / 100


def _policy_score(inp: IndustrialPolicyInput) -> float:
    raw = (
        inp.reshoring_policy_effectiveness * 0.4
        + inp.IRA_like_subsidy_race * 0.35
        + inp.industrial_subsidy_distortion * 0.25
    ) * 100
    return round(raw * 100) / 100


def _resilience_score(inp: IndustrialPolicyInput) -> float:
    raw = (
        inp.supply_chain_resilience_gap * 0.4
        + inp.manufacturing_capacity_gap * 0.35
        + inp.workforce_skills_mismatch * 0.25
    ) * 100
    return round(raw * 100) / 100


def _geopolitical_score(inp: IndustrialPolicyInput) -> float:
    raw = (
        inp.geopolitical_industrial_leverage * 0.4
        + inp.protectionism_trade_war_risk * 0.35
        + inp.de_risking_progress * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    dependency: float,
    policy: float,
    resilience: float,
    geopolitical: float,
) -> float:
    return round(
        dependency * 0.30
        + policy * 0.25
        + resilience * 0.25
        + geopolitical * 0.20,
        2,
    )


def _industrial_pattern(inp: IndustrialPolicyInput) -> str:
    if inp.strategic_dependency_exposure > 0.85 and inp.semiconductor_dependency > 0.80:
        return "strategic_dependency_crisis"
    if inp.IRA_like_subsidy_race > 0.85 and inp.protectionism_trade_war_risk > 0.80:
        return "subsidy_trade_war_escalation"
    if inp.reshoring_policy_effectiveness > 0.85 and inp.workforce_skills_mismatch > 0.80:
        return "reshoring_policy_failure"
    if inp.pharmaceutical_reshoring_lag > 0.80 and inp.supply_chain_resilience_gap > 0.75:
        return "pharmaceutical_supply_collapse"
    if inp.green_tech_manufacturing_gap > 0.80 and inp.strategic_autonomy_index > 0.75:
        return "green_manufacturing_gap_crisis"
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
        return "crise_politique_industrielle_systémique"
    if composite >= 40:
        return "disruption_industrielle_majeure"
    if composite >= 20:
        return "restructuration_industrielle_active"
    return "politique_industrielle_gérée"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_politique_industrielle"
    if risk == "high":
        return "renforcement_stratégie_relocalisation"
    if risk == "moderate":
        return "surveillance_dépendances_industrielles"
    return "veille_politique_industrielle_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise politique industrielle — dépendance stratégique systémique"
    if risk == "high":
        return "🟠 Disruption industrielle majeure détectée"
    if risk == "moderate":
        return "🟡 Restructuration industrielle active en cours"
    return "🟢 Politique industrielle gérée et surveillée"


def analyze(inp: IndustrialPolicyInput) -> IndustrialPolicyResult:
    dep = _dependency_score(inp)
    pol = _policy_score(inp)
    res = _resilience_score(inp)
    geo = _geopolitical_score(inp)
    comp = _composite(dep, pol, res, geo)
    pat = _industrial_pattern(inp)
    risk = _risk_level(comp)
    sev = _severity(comp)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return IndustrialPolicyResult(
        entity_id=inp.entity_id,
        industrial_sector=inp.industrial_sector,
        region=inp.region,
        dependency_score=dep,
        policy_score=pol,
        resilience_score=res,
        geopolitical_score=geo,
        composite_score=comp,
        risk_level=risk,
        industrial_pattern=pat,
        severity=sev,
        recommended_action=action,
        signal=sig,
        strategic_dependency_exposure=inp.strategic_dependency_exposure,
        semiconductor_dependency=inp.semiconductor_dependency,
    )


class IndustrialPolicyEngine:
    def __init__(self, inputs: List[IndustrialPolicyInput]):
        self.inputs = inputs
        self.results: List[IndustrialPolicyResult] = [analyze(i) for i in inputs]

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
            pattern_distribution[r.industrial_pattern] = pattern_distribution.get(r.industrial_pattern, 0) + 1
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
            "module_id": 383,
            "module_name": "Industrial Policy & Reshoring Intelligence Engine",
            "total": n,
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "risk_distribution": risk_distribution,
            "pattern_distribution": pattern_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_reshoring_index": round(avg_composite / 100 * 10, 2),
        }
