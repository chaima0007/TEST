"""
Sovereign Debt Crisis & Fiscal Contagion Intelligence Engine
Module 309 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class SovereignDebtInput:
    entity_id: str
    sovereign_type: str
    region: str
    debt_to_gdp_ratio: float = 0.0
    fiscal_deficit_trajectory: float = 0.0
    foreign_currency_exposure: float = 0.0
    rollover_risk_index: float = 0.0
    interest_burden_rate: float = 0.0
    credit_rating_deterioration: float = 0.0
    primary_balance_gap: float = 0.0
    capital_flight_velocity: float = 0.0
    contagion_spillover_risk: float = 0.0
    imf_program_dependency: float = 0.0
    currency_crisis_coupling: float = 0.0
    banking_sector_exposure: float = 0.0
    political_fiscal_risk: float = 0.0
    market_confidence_erosion: float = 0.0
    debt_monetization_risk: float = 0.0
    external_financing_gap: float = 0.0
    demographic_fiscal_pressure: float = 0.0


@dataclass
class SovereignDebtResult:
    entity_id: str
    region: str
    sovereign_type: str
    debt_risk: str
    debt_pattern: str
    debt_severity: str
    recommended_action: str
    solvency_score: float
    liquidity_score: float
    contagion_score: float
    confidence_score: float
    debt_composite: float
    is_debt_crisis: bool
    requires_debt_intervention: bool
    debt_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "sovereign_type": self.sovereign_type,
            "debt_risk": self.debt_risk,
            "debt_pattern": self.debt_pattern,
            "debt_severity": self.debt_severity,
            "recommended_action": self.recommended_action,
            "solvency_score": self.solvency_score,
            "liquidity_score": self.liquidity_score,
            "contagion_score": self.contagion_score,
            "confidence_score": self.confidence_score,
            "debt_composite": self.debt_composite,
            "is_debt_crisis": self.is_debt_crisis,
            "requires_debt_intervention": self.requires_debt_intervention,
            "debt_signal": self.debt_signal,
        }


def _solvency_score(i: SovereignDebtInput) -> float:
    return (i.debt_to_gdp_ratio * 0.4 + i.fiscal_deficit_trajectory * 0.35 + i.primary_balance_gap * 0.25) * 100


def _liquidity_score(i: SovereignDebtInput) -> float:
    return (i.rollover_risk_index * 0.4 + i.external_financing_gap * 0.35 + i.capital_flight_velocity * 0.25) * 100


def _contagion_score(i: SovereignDebtInput) -> float:
    return (i.contagion_spillover_risk * 0.4 + i.banking_sector_exposure * 0.35 + i.currency_crisis_coupling * 0.25) * 100


def _confidence_score(i: SovereignDebtInput) -> float:
    return (i.market_confidence_erosion * 0.4 + i.credit_rating_deterioration * 0.35 + i.political_fiscal_risk * 0.25) * 100


def _composite(sol: float, liq: float, con: float, conf: float) -> float:
    return sol * 0.30 + liq * 0.25 + con * 0.25 + conf * 0.20


def _debt_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _debt_pattern(i: SovereignDebtInput) -> str:
    if i.debt_to_gdp_ratio >= 0.70 and i.fiscal_deficit_trajectory >= 0.65:
        return "debt_spiral"
    if i.rollover_risk_index >= 0.70 and i.external_financing_gap >= 0.65:
        return "liquidity_trap"
    if i.contagion_spillover_risk >= 0.70 and i.banking_sector_exposure >= 0.65:
        return "contagion_cascade"
    if i.market_confidence_erosion >= 0.70 and i.credit_rating_deterioration >= 0.65:
        return "confidence_collapse"
    if i.currency_crisis_coupling >= 0.70 and i.foreign_currency_exposure >= 0.65:
        return "currency_debt_spiral"
    return "none"


def _debt_severity(composite: float) -> str:
    if composite >= 75:
        return "fiscal_emergency"
    if composite >= 50:
        return "high_fiscal_stress"
    if composite >= 25:
        return "fiscal_tension"
    return "fiscal_stable"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "sovereign_debt_restructuring"
    if risk == "high" and pattern == "contagion_cascade":
        return "contagion_firewall"
    if risk == "high":
        return "fiscal_consolidation_program"
    if risk == "moderate":
        return "fiscal_monitoring"
    return "no_action"


def _debt_signal(i: SovereignDebtInput, pattern: str, composite: float) -> str:
    if composite < 20:
        return "Stabilité fiscale souveraine — les indicateurs de solvabilité, liquidité, contagion et confiance restent dans les seuils de référence"
    pattern_labels: Dict[str, str] = {
        "debt_spiral": "Spirale de la dette",
        "liquidity_trap": "Trappe de liquidité",
        "contagion_cascade": "Cascade de contagion",
        "confidence_collapse": "Effondrement de la confiance",
        "currency_debt_spiral": "Spirale dette-devises",
    }
    label = pattern_labels.get(pattern, pattern.replace("_", " "))
    return (
        f"{label} — ratio dette/PIB {i.debt_to_gdp_ratio:.0%} — "
        f"déficit fiscal {i.fiscal_deficit_trajectory:.0%} — "
        f"risque de contagion {i.contagion_spillover_risk:.0%} — "
        f"composite {round(composite)}"
    )


def _analyze_entity(i: SovereignDebtInput) -> SovereignDebtResult:
    sol = round(_solvency_score(i), 2)
    liq = round(_liquidity_score(i), 2)
    con = round(_contagion_score(i), 2)
    conf = round(_confidence_score(i), 2)
    comp = round(_composite(sol, liq, con, conf), 2)
    risk = _debt_risk(comp)
    pattern = _debt_pattern(i)
    severity = _debt_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _debt_signal(i, pattern, comp)

    return SovereignDebtResult(
        entity_id=i.entity_id,
        region=i.region,
        sovereign_type=i.sovereign_type,
        debt_risk=risk,
        debt_pattern=pattern,
        debt_severity=severity,
        recommended_action=action,
        solvency_score=sol,
        liquidity_score=liq,
        contagion_score=con,
        confidence_score=conf,
        debt_composite=comp,
        is_debt_crisis=comp >= 60,
        requires_debt_intervention=comp >= 40,
        debt_signal=signal,
    )


class SovereignDebtCrisisEngine:
    def analyze(self, entities: List[SovereignDebtInput]) -> Dict[str, Any]:
        results = [_analyze_entity(e) for e in entities]
        result_dicts = [r.to_dict() for r in results]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_sol = total_liq = total_con = total_conf = total_comp = 0.0
        crisis_count = intervention_count = 0

        for r in results:
            risk_counts[r.debt_risk] = risk_counts.get(r.debt_risk, 0) + 1
            pattern_counts[r.debt_pattern] = pattern_counts.get(r.debt_pattern, 0) + 1
            severity_counts[r.debt_severity] = severity_counts.get(r.debt_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_sol += r.solvency_score
            total_liq += r.liquidity_score
            total_con += r.contagion_score
            total_conf += r.confidence_score
            total_comp += r.debt_composite
            if r.is_debt_crisis:
                crisis_count += 1
            if r.requires_debt_intervention:
                intervention_count += 1

        n = len(results) or 1
        avg_comp = total_comp / n

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_solvency_score": round(total_sol / n, 2),
            "avg_liquidity_score": round(total_liq / n, 2),
            "avg_contagion_score": round(total_con / n, 2),
            "avg_confidence_score": round(total_conf / n, 2),
            "avg_debt_composite": round(avg_comp, 2),
            "debt_crisis_count": crisis_count,
            "debt_intervention_count": intervention_count,
            "avg_estimated_fiscal_stress_index": round(avg_comp / 100 * 10, 2),
            "entities": result_dicts,
        }
