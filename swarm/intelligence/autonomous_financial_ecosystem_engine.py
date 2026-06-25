from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class AutonomousFinancialInput:
    entity_id: str
    ecosystem_type: str
    region: str
    autonomous_liquidity_depth: float
    algorithmic_governance_maturity: float
    self_regulation_effectiveness: float
    market_maker_concentration: float
    flash_crash_susceptibility: float
    liquidity_fragmentation: float
    order_flow_toxicity: float
    price_discovery_efficiency: float
    systemic_correlation: float
    circuit_breaker_effectiveness: float
    dark_pool_opacity: float
    hft_dominance: float
    regulatory_arbitrage_exposure: float
    cross_market_contagion: float
    autonomous_agent_conflict_rate: float
    market_microstructure_stress: float
    information_latency_risk: float


@dataclass
class AutonomousFinancialResult:
    entity_id: str
    region: str
    ecosystem_type: str
    ecosystem_risk: str
    ecosystem_pattern: str
    ecosystem_severity: str
    recommended_action: str
    liquidity_score: float
    governance_score: float
    microstructure_score: float
    contagion_score: float
    ecosystem_composite: float
    is_in_ecosystem_crisis: bool
    requires_ecosystem_intervention: bool
    ecosystem_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "ecosystem_type": self.ecosystem_type,
            "ecosystem_risk": self.ecosystem_risk,
            "ecosystem_pattern": self.ecosystem_pattern,
            "ecosystem_severity": self.ecosystem_severity,
            "recommended_action": self.recommended_action,
            "liquidity_score": self.liquidity_score,
            "governance_score": self.governance_score,
            "microstructure_score": self.microstructure_score,
            "contagion_score": self.contagion_score,
            "ecosystem_composite": self.ecosystem_composite,
            "is_in_ecosystem_crisis": self.is_in_ecosystem_crisis,
            "requires_ecosystem_intervention": self.requires_ecosystem_intervention,
            "ecosystem_signal": self.ecosystem_signal,
        }


def _liquidity_score(inp: AutonomousFinancialInput) -> float:
    raw = (
        inp.liquidity_fragmentation * 0.4
        + (1 - inp.autonomous_liquidity_depth) * 0.3
        + inp.market_maker_concentration * 0.3
    ) * 100
    return round(raw * 100) / 100


def _governance_score(inp: AutonomousFinancialInput) -> float:
    raw = (
        (1 - inp.self_regulation_effectiveness) * 0.4
        + (1 - inp.algorithmic_governance_maturity) * 0.35
        + inp.regulatory_arbitrage_exposure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _microstructure_score(inp: AutonomousFinancialInput) -> float:
    raw = (
        inp.flash_crash_susceptibility * 0.35
        + inp.order_flow_toxicity * 0.35
        + inp.market_microstructure_stress * 0.30
    ) * 100
    return round(raw * 100) / 100


def _contagion_score(inp: AutonomousFinancialInput) -> float:
    raw = (
        inp.systemic_correlation * 0.4
        + inp.cross_market_contagion * 0.35
        + (1 - inp.circuit_breaker_effectiveness) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(liq: float, gov: float, micro: float, cont: float) -> float:
    return round((liq * 0.30 + gov * 0.25 + micro * 0.25 + cont * 0.20) * 100) / 100


def _ecosystem_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _ecosystem_pattern(inp: AutonomousFinancialInput) -> str:
    if inp.liquidity_fragmentation >= 0.65 and (1 - inp.autonomous_liquidity_depth) >= 0.55:
        return "liquidity_vacuum"
    if inp.flash_crash_susceptibility >= 0.65 and inp.market_microstructure_stress >= 0.55:
        return "flash_crash_cascade"
    if (1 - inp.self_regulation_effectiveness) >= 0.65 and inp.regulatory_arbitrage_exposure >= 0.55:
        return "governance_failure"
    if inp.systemic_correlation >= 0.70 and inp.cross_market_contagion >= 0.60:
        return "contagion_spiral"
    if inp.hft_dominance >= 0.70 and inp.order_flow_toxicity >= 0.60:
        return "hft_predation"
    return "none"


def _ecosystem_severity(composite: float) -> str:
    if composite >= 75:
        return "systemic_collapse"
    if composite >= 50:
        return "high_dysfunction"
    if composite >= 25:
        return "market_stress"
    return "autonomous_equilibrium"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "market_circuit_breaker_emergency"
    if risk == "high":
        if pattern == "contagion_spiral":
            return "contagion_quarantine"
        return "ecosystem_stabilization"
    if risk == "moderate":
        return "market_monitoring"
    return "no_action"


def _ecosystem_signal(inp: AutonomousFinancialInput, risk: str, composite: float, governance_score: float) -> str:
    if risk == "critical":
        return (
            f"Critique — fragmentation liquidité {int(inp.liquidity_fragmentation * 100)}%"
            f" — corrélation systémique {int(inp.systemic_correlation * 100)}%"
            f" — composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — flash crash susceptibilité {int(inp.flash_crash_susceptibility * 100)}%"
            f" — gouvernance {100 - int(governance_score)}%"
            f" — composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — toxicité flux ordres {int(inp.order_flow_toxicity * 100)}%"
            f" — composite {int(composite)}"
        )
    return "Écosystème financier autonome stable — liquidité équilibrée, gouvernance algorithmique efficace"


def analyze(inp: AutonomousFinancialInput) -> AutonomousFinancialResult:
    liq = _liquidity_score(inp)
    gov = _governance_score(inp)
    micro = _microstructure_score(inp)
    cont = _contagion_score(inp)
    composite = _composite(liq, gov, micro, cont)
    risk = _ecosystem_risk(composite)
    pattern = _ecosystem_pattern(inp)
    severity = _ecosystem_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _ecosystem_signal(inp, risk, composite, gov)

    return AutonomousFinancialResult(
        entity_id=inp.entity_id,
        region=inp.region,
        ecosystem_type=inp.ecosystem_type,
        ecosystem_risk=risk,
        ecosystem_pattern=pattern,
        ecosystem_severity=severity,
        recommended_action=action,
        liquidity_score=liq,
        governance_score=gov,
        microstructure_score=micro,
        contagion_score=cont,
        ecosystem_composite=composite,
        is_in_ecosystem_crisis=composite >= 60,
        requires_ecosystem_intervention=composite >= 40,
        ecosystem_signal=signal,
    )


class AutonomousFinancialEcosystemEngine:
    def run(self, inputs: List[AutonomousFinancialInput]) -> Dict[str, Any]:
        results = [analyze(inp) for inp in inputs]
        dicts = [r.to_dict() for r in results]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_liq = 0.0
        total_gov = 0.0
        total_micro = 0.0
        total_cont = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.ecosystem_risk] = risk_counts.get(r.ecosystem_risk, 0) + 1
            pattern_counts[r.ecosystem_pattern] = pattern_counts.get(r.ecosystem_pattern, 0) + 1
            severity_counts[r.ecosystem_severity] = severity_counts.get(r.ecosystem_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.ecosystem_composite
            total_liq += r.liquidity_score
            total_gov += r.governance_score
            total_micro += r.microstructure_score
            total_cont += r.contagion_score
            if r.is_in_ecosystem_crisis:
                crisis_count += 1
            if r.requires_ecosystem_intervention:
                intervention_count += 1

        n = len(results)
        avg_composite = round(total_composite / n * 10) / 10 if n else 0.0

        summary = {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_ecosystem_composite": avg_composite,
            "ecosystem_crisis_count": crisis_count,
            "ecosystem_intervention_count": intervention_count,
            "avg_liquidity_score": round(total_liq / n * 10) / 10 if n else 0.0,
            "avg_governance_score": round(total_gov / n * 10) / 10 if n else 0.0,
            "avg_microstructure_score": round(total_micro / n * 10) / 10 if n else 0.0,
            "avg_contagion_score": round(total_cont / n * 10) / 10 if n else 0.0,
            "avg_estimated_ecosystem_stress_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": dicts, "summary": summary}
