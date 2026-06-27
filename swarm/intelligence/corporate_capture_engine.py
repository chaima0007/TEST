"""
Module 339 — Corporate Power Capture & Regulatory Arbitrage Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CorporateCaptureInput:
    entity_id: str
    industry_sector: str
    region: str
    # 17 float fields (0.0–1.0)
    regulatory_capture_depth: float
    lobbying_expenditure_ratio: float
    revolving_door_intensity: float
    market_concentration_index: float
    antitrust_enforcement_weakness: float
    tax_arbitrage_sophistication: float
    regulatory_arbitrage_exploitation: float
    corporate_sovereignty_over_state: float
    standard_setting_capture: float
    judicial_capture_risk: float
    legislative_capture_index: float
    agency_capture_prevalence: float
    dark_money_political_influence: float
    patent_system_weaponization: float
    regulatory_complexity_weaponization: float
    state_aid_capture_mechanism: float
    private_enforcement_substitution: float


@dataclass
class CorporateCaptureResult:
    entity_id: str
    industry_sector: str
    region: str
    capture_score: float
    market_score: float
    influence_score: float
    sovereignty_score: float
    composite_score: float
    risk_level: str
    capture_pattern: str
    severity: str
    recommended_action: str
    signal: str
    regulatory_capture_depth: float
    corporate_sovereignty_over_state: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "industry_sector": self.industry_sector,
            "region": self.region,
            "capture_score": self.capture_score,
            "market_score": self.market_score,
            "influence_score": self.influence_score,
            "sovereignty_score": self.sovereignty_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "capture_pattern": self.capture_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "regulatory_capture_depth": self.regulatory_capture_depth,
            "corporate_sovereignty_over_state": self.corporate_sovereignty_over_state,
        }


def _capture_score(inp: CorporateCaptureInput) -> float:
    raw = (
        inp.regulatory_capture_depth * 0.4
        + inp.agency_capture_prevalence * 0.35
        + inp.legislative_capture_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _market_score(inp: CorporateCaptureInput) -> float:
    raw = (
        inp.market_concentration_index * 0.4
        + inp.antitrust_enforcement_weakness * 0.35
        + inp.patent_system_weaponization * 0.25
    ) * 100
    return round(raw * 100) / 100


def _influence_score(inp: CorporateCaptureInput) -> float:
    raw = (
        inp.lobbying_expenditure_ratio * 0.4
        + inp.dark_money_political_influence * 0.35
        + inp.revolving_door_intensity * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sovereignty_score(inp: CorporateCaptureInput) -> float:
    raw = (
        inp.corporate_sovereignty_over_state * 0.4
        + inp.tax_arbitrage_sophistication * 0.35
        + inp.regulatory_arbitrage_exploitation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    capture: float,
    market: float,
    influence: float,
    sovereignty: float,
) -> float:
    return round(
        capture * 0.30
        + market * 0.25
        + influence * 0.25
        + sovereignty * 0.20,
        2,
    )


def _capture_pattern(inp: CorporateCaptureInput) -> str:
    if inp.regulatory_capture_depth >= 0.70 and inp.agency_capture_prevalence >= 0.65:
        return "regulatory_capture_complete"
    if inp.market_concentration_index >= 0.70 and inp.antitrust_enforcement_weakness >= 0.65:
        return "antitrust_collapse"
    if inp.dark_money_political_influence >= 0.70 and inp.lobbying_expenditure_ratio >= 0.65:
        return "dark_money_dominance"
    if inp.corporate_sovereignty_over_state >= 0.70 and inp.tax_arbitrage_sophistication >= 0.65:
        return "corporate_sovereignty"
    if inp.standard_setting_capture >= 0.70 and inp.regulatory_complexity_weaponization >= 0.65:
        return "standard_capture_hegemony"
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
        return "capture_corporative_systémique"
    if composite >= 40:
        return "pouvoir_corporatif_dominant"
    if composite >= 20:
        return "dérive_corporative_structurelle"
    return "équilibre_régulateur_relatif"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "restauration_souveraineté_régulatrice_urgente"
    if risk == "high":
        return "démantèlement_capture_corporative"
    if risk == "moderate":
        return "renforcement_antitrust_systémique"
    return "veille_pouvoir_corporatif"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Capture corporative systémique — État sous contrôle privé"
    if risk == "high":
        return "🟠 Pouvoir corporatif dominant détecté"
    if risk == "moderate":
        return "🟡 Dérive corporative structurelle active"
    return "🟢 Équilibre régulateur relatif maintenu"


def analyze(inp: CorporateCaptureInput) -> CorporateCaptureResult:
    cap = _capture_score(inp)
    mkt = _market_score(inp)
    inf = _influence_score(inp)
    sov = _sovereignty_score(inp)
    comp = _composite(cap, mkt, inf, sov)
    pat = _capture_pattern(inp)
    risk = _risk_level(comp)
    sev = _severity(comp)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return CorporateCaptureResult(
        entity_id=inp.entity_id,
        industry_sector=inp.industry_sector,
        region=inp.region,
        capture_score=cap,
        market_score=mkt,
        influence_score=inf,
        sovereignty_score=sov,
        composite_score=comp,
        risk_level=risk,
        capture_pattern=pat,
        severity=sev,
        recommended_action=action,
        signal=sig,
        regulatory_capture_depth=inp.regulatory_capture_depth,
        corporate_sovereignty_over_state=inp.corporate_sovereignty_over_state,
    )


class CorporateCaptureEngine:
    def __init__(self, inputs: List[CorporateCaptureInput]):
        self.inputs = inputs
        self.results: List[CorporateCaptureResult] = [analyze(i) for i in inputs]

    def analyze(self, entities: List[CorporateCaptureInput]) -> Dict[str, Any]:
        results = [analyze(e) for e in entities]
        return CorporateCaptureEngine.summary(results)

    @staticmethod
    def summary(results: List[CorporateCaptureResult]) -> Dict[str, Any]:
        n = len(results)
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

        for r in results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            pattern_distribution[r.capture_pattern] = pattern_distribution.get(r.capture_pattern, 0) + 1
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
            "module_id": 339,
            "module_name": "Corporate Power Capture & Regulatory Arbitrage Intelligence Engine",
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
            "avg_estimated_capture_index": round(avg_composite / 100 * 10, 2),
        }
