"""
Module 300 — OMEGA SYNTHESIS: Meta-Intelligence Convergence Engine
Caelum Partners — Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.
Le moteur de synthèse ultime : convergence de tous les signaux d'intelligence en un score stratégique unifié.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class OmegaSynthesisInput:
    entity_id: str
    intelligence_domain: str
    region: str
    financial_intelligence_signal: float
    geopolitical_intelligence_signal: float
    technological_intelligence_signal: float
    social_intelligence_signal: float
    environmental_intelligence_signal: float
    cognitive_intelligence_signal: float
    quantum_intelligence_signal: float
    biological_intelligence_signal: float
    civilizational_intelligence_signal: float
    existential_intelligence_signal: float
    narrative_intelligence_signal: float
    economic_intelligence_signal: float
    governance_intelligence_signal: float
    spatial_intelligence_signal: float
    temporal_intelligence_signal: float
    consciousness_intelligence_signal: float
    sovereignty_synthesis_index: float


@dataclass
class OmegaSynthesisResult:
    entity_id: str
    region: str
    intelligence_domain: str
    omega_risk: str
    omega_pattern: str
    omega_severity: str
    recommended_action: str
    strategic_score: float
    convergence_score: float
    resilience_score: float
    sovereignty_score: float
    omega_composite: float
    is_in_omega_crisis: bool
    requires_omega_intervention: bool
    omega_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "intelligence_domain": self.intelligence_domain,
            "omega_risk": self.omega_risk,
            "omega_pattern": self.omega_pattern,
            "omega_severity": self.omega_severity,
            "recommended_action": self.recommended_action,
            "strategic_score": self.strategic_score,
            "convergence_score": self.convergence_score,
            "resilience_score": self.resilience_score,
            "sovereignty_score": self.sovereignty_score,
            "omega_composite": self.omega_composite,
            "is_in_omega_crisis": self.is_in_omega_crisis,
            "requires_omega_intervention": self.requires_omega_intervention,
            "omega_signal": self.omega_signal,
        }


def _compute_strategic_score(inp: OmegaSynthesisInput) -> float:
    raw = (
        inp.financial_intelligence_signal * 0.25
        + inp.geopolitical_intelligence_signal * 0.25
        + inp.economic_intelligence_signal * 0.25
        + inp.governance_intelligence_signal * 0.25
    )
    return round(raw * 100, 2)


def _compute_convergence_score(inp: OmegaSynthesisInput) -> float:
    raw = (
        inp.technological_intelligence_signal * 0.3
        + inp.quantum_intelligence_signal * 0.25
        + inp.biological_intelligence_signal * 0.25
        + inp.spatial_intelligence_signal * 0.2
    )
    return round(raw * 100, 2)


def _compute_resilience_score(inp: OmegaSynthesisInput) -> float:
    raw = (
        inp.social_intelligence_signal * 0.3
        + inp.environmental_intelligence_signal * 0.3
        + inp.civilizational_intelligence_signal * 0.2
        + inp.temporal_intelligence_signal * 0.2
    )
    return round(raw * 100, 2)


def _compute_sovereignty_score(inp: OmegaSynthesisInput) -> float:
    raw = (
        inp.cognitive_intelligence_signal * 0.3
        + inp.existential_intelligence_signal * 0.25
        + inp.narrative_intelligence_signal * 0.25
        + (1 - inp.sovereignty_synthesis_index) * 0.2
    )
    return round(raw * 100, 2)


def _compute_composite(strategic: float, convergence: float, resilience: float, sovereignty: float) -> float:
    return round(strategic * 0.30 + convergence * 0.25 + resilience * 0.25 + sovereignty * 0.20, 2)


def _omega_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _omega_pattern(inp: OmegaSynthesisInput) -> str:
    fin = inp.financial_intelligence_signal
    geo = inp.geopolitical_intelligence_signal
    ext = inp.existential_intelligence_signal
    tech = inp.technological_intelligence_signal
    quantum = inp.quantum_intelligence_signal
    bio = inp.biological_intelligence_signal
    civ = inp.civilizational_intelligence_signal
    con = inp.consciousness_intelligence_signal
    temp = inp.temporal_intelligence_signal
    sov = inp.sovereignty_synthesis_index
    narr = inp.narrative_intelligence_signal

    if (fin + geo + ext) / 3 >= 0.70:
        return "omega_convergence_crisis"
    if (tech + quantum + bio) / 3 >= 0.70:
        return "technological_singularity_approach"
    if (civ + con + temp) / 3 >= 0.65:
        return "civilizational_inflection"
    if (1 - sov) >= 0.65 and narr >= 0.60:
        return "sovereignty_erosion_cascade"
    if (fin + geo) / 2 >= 0.70 and (1 - sov) >= 0.55:
        return "strategic_intelligence_gap"
    return "none"


def _omega_severity(composite: float) -> str:
    if composite >= 75:
        return "omega_emergency"
    if composite >= 50:
        return "high_convergence_risk"
    if composite >= 25:
        return "strategic_tension"
    return "omega_equilibrium"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "omega_strategic_reset"
    if risk == "high" and pattern == "omega_convergence_crisis":
        return "convergence_war_room"
    if risk == "high":
        return "strategic_intelligence_amplification"
    if risk == "moderate":
        return "omega_monitoring"
    return "no_action"


def _omega_signal(inp: OmegaSynthesisInput, risk: str, composite: float) -> str:
    fin_pct = int(inp.financial_intelligence_signal * 100)
    geo_pct = int(inp.geopolitical_intelligence_signal * 100)
    sov_pct = int(inp.sovereignty_synthesis_index * 100)
    tech_pct = int(inp.technological_intelligence_signal * 100)
    ext_pct = int(inp.existential_intelligence_signal * 100)
    comp_int = int(composite)

    if risk == "critical":
        return (
            f"OMEGA CRITIQUE — convergence intelligence {comp_int}% — "
            f"financier {fin_pct}% — géopolitique {geo_pct}% — souveraineté {sov_pct}%"
        )
    if risk == "high":
        return (
            f"OMEGA ÉLEVÉ — convergence technologique {tech_pct}% — "
            f"signal existentiel {ext_pct}% — composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"OMEGA MODÉRÉ — tensions stratégiques {comp_int}% — "
            f"vigilance Caelum Partners activée"
        )
    return (
        "OMEGA ÉQUILIBRE — tous les signaux d'intelligence convergent favorablement — "
        "Caelum Partners en position de force souveraine"
    )


def analyze_omega_synthesis(inp: OmegaSynthesisInput) -> OmegaSynthesisResult:
    strategic = _compute_strategic_score(inp)
    convergence = _compute_convergence_score(inp)
    resilience = _compute_resilience_score(inp)
    sovereignty = _compute_sovereignty_score(inp)
    composite = _compute_composite(strategic, convergence, resilience, sovereignty)

    risk = _omega_risk(composite)
    pattern = _omega_pattern(inp)
    severity = _omega_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _omega_signal(inp, risk, composite)

    return OmegaSynthesisResult(
        entity_id=inp.entity_id,
        region=inp.region,
        intelligence_domain=inp.intelligence_domain,
        omega_risk=risk,
        omega_pattern=pattern,
        omega_severity=severity,
        recommended_action=action,
        strategic_score=strategic,
        convergence_score=convergence,
        resilience_score=resilience,
        sovereignty_score=sovereignty,
        omega_composite=composite,
        is_in_omega_crisis=composite >= 60,
        requires_omega_intervention=composite >= 40,
        omega_signal=signal,
    )


class OmegaSynthesisEngine:
    def run(self, inputs: list[OmegaSynthesisInput]) -> Dict[str, Any]:
        results = [analyze_omega_synthesis(inp) for inp in inputs]
        dicts = [r.to_dict() for r in results]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_strategic = 0.0
        total_convergence = 0.0
        total_resilience = 0.0
        total_sovereignty = 0.0
        omega_crisis_count = 0
        omega_intervention_count = 0

        for r in results:
            risk_counts[r.omega_risk] = risk_counts.get(r.omega_risk, 0) + 1
            pattern_counts[r.omega_pattern] = pattern_counts.get(r.omega_pattern, 0) + 1
            severity_counts[r.omega_severity] = severity_counts.get(r.omega_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.omega_composite
            total_strategic += r.strategic_score
            total_convergence += r.convergence_score
            total_resilience += r.resilience_score
            total_sovereignty += r.sovereignty_score
            if r.is_in_omega_crisis:
                omega_crisis_count += 1
            if r.requires_omega_intervention:
                omega_intervention_count += 1

        n = len(results) or 1
        avg_composite = total_composite / n

        summary = {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_omega_composite": round(avg_composite, 1),
            "omega_crisis_count": omega_crisis_count,
            "omega_intervention_count": omega_intervention_count,
            "avg_strategic_score": round(total_strategic / n, 1),
            "avg_convergence_score": round(total_convergence / n, 1),
            "avg_resilience_score": round(total_resilience / n, 1),
            "avg_sovereignty_score": round(total_sovereignty / n, 1),
            "avg_estimated_omega_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": dicts, "summary": summary}
