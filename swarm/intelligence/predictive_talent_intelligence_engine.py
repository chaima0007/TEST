"""
Module 277 — Predictive Talent Intelligence & Human Capital Engine
Caelum Partners Swarm Intelligence Platform
© Chaima Mhadbi — Fondatrice Caelum Partners, Bruxelles — 2026
"""

from dataclasses import dataclass
from typing import List, Dict, Any


TALENT_SEGMENTS = (
    "emerging_leader",
    "deep_specialist",
    "creative_catalyst",
    "cross_functional_connector",
    "technical_architect",
    "cultural_guardian",
    "innovation_scout",
    "succession_candidate",
)


@dataclass
class TalentInput:
    talent_id: str
    talent_segment: str
    region: str
    # 17 numeric fields (0.0–1.0)
    skill_half_life_risk: float               # higher = worse
    learning_velocity_score: float
    potential_trajectory_score: float
    flight_risk_index: float                  # higher = worse
    human_capital_value_score: float
    adaptability_coefficient: float
    knowledge_transfer_depth: float
    mentorship_multiplier_score: float
    strategic_indispensability_score: float
    skills_future_alignment: float
    innovation_contribution_rate: float
    retention_investment_roi: float
    succession_pipeline_readiness: float
    cultural_influence_score: float
    cross_domain_synthesis_ability: float
    resilience_under_pressure: float
    talent_ecosystem_connectivity: float


def _obsolescence_score(t: TalentInput) -> float:
    """0.30 weight — higher = worse obsolescence risk."""
    return min(
        t.skill_half_life_risk * 0.40
        + (1.0 - t.skills_future_alignment) * 0.35
        + (1.0 - t.adaptability_coefficient) * 0.25,
        1.0,
    )


def _flight_score(t: TalentInput) -> float:
    """0.25 weight — higher = worse flight risk."""
    return min(
        t.flight_risk_index * 0.45
        + (1.0 - t.retention_investment_roi) * 0.30
        + (1.0 - t.cultural_influence_score) * 0.25,
        1.0,
    )


def _value_score(t: TalentInput) -> float:
    """0.25 weight — higher = lower human capital value (inverted inputs)."""
    return min(
        (1.0 - t.human_capital_value_score) * 0.40
        + (1.0 - t.strategic_indispensability_score) * 0.35
        + (1.0 - t.innovation_contribution_rate) * 0.25,
        1.0,
    )


def _succession_score(t: TalentInput) -> float:
    """0.20 weight — higher = worse succession readiness."""
    return min(
        (1.0 - t.succession_pipeline_readiness) * 0.40
        + (1.0 - t.knowledge_transfer_depth) * 0.35
        + (1.0 - t.mentorship_multiplier_score) * 0.25,
        1.0,
    )


def _composite(obs: float, flt: float, val: float, suc: float) -> float:
    return round(
        (obs * 0.30 + flt * 0.25 + val * 0.25 + suc * 0.20) * 100, 2
    )


def _talent_pattern(t: TalentInput) -> str:
    if t.skill_half_life_risk >= 0.70 and t.skills_future_alignment <= 0.35:
        return "talent_obsolescence"
    if t.flight_risk_index >= 0.68 and t.retention_investment_roi <= 0.38:
        return "flight_risk_crisis"
    if t.knowledge_transfer_depth <= 0.30 and t.mentorship_multiplier_score <= 0.35:
        return "knowledge_drain"
    if t.succession_pipeline_readiness <= 0.30 and t.potential_trajectory_score <= 0.40:
        return "succession_gap"
    if t.potential_trajectory_score <= 0.32 and t.learning_velocity_score <= 0.35:
        return "potential_stagnation"
    return "none"


def _risk(comp: float) -> str:
    if comp >= 60.0:
        return "critical"
    if comp >= 40.0:
        return "high"
    if comp >= 20.0:
        return "moderate"
    return "low"


def _severity(comp: float) -> str:
    if comp >= 60.0:
        return "at_risk"
    if comp >= 40.0:
        return "declining"
    if comp >= 20.0:
        return "developing"
    return "thriving"


def _action(risk: str, pattern: str) -> str:
    if risk == "critical":
        if pattern in ("talent_obsolescence", "potential_stagnation"):
            return "reskilling_program"
        return "talent_emergency_retention"
    if risk == "high":
        if pattern in ("flight_risk_crisis",):
            return "engagement_intervention"
        return "succession_acceleration"
    if risk == "moderate":
        return "talent_monitoring"
    return "no_action"


def _signal(t: TalentInput, pattern: str, comp: float) -> str:
    if comp < 20.0:
        return (
            "Talent florissant — trajectoire élevée, forte valeur humaine, "
            "transmission du savoir active, alignement futur confirmé"
        )
    labels: Dict[str, str] = {
        "talent_obsolescence": "Obsolescence des compétences",
        "flight_risk_crisis": "Crise de rétention — risque de départ imminent",
        "knowledge_drain": "Fuite du savoir organisationnel",
        "succession_gap": "Écart dans le pipeline de succession",
        "potential_stagnation": "Stagnation du potentiel",
    }
    label = labels.get(pattern, pattern.replace("_", " "))
    return (
        f"{label} — demi-vie compétences {t.skill_half_life_risk:.2f} — "
        f"risque départ {t.flight_risk_index:.2f} — "
        f"valeur humaine {t.human_capital_value_score:.2f} — "
        f"succession {t.succession_pipeline_readiness:.2f} — "
        f"composite {comp:.1f}"
    )


class PredictiveTalentIntelligenceEngine:
    """Assesses talent trajectories and human capital risks."""

    def __init__(self) -> None:
        self._results: List[Dict[str, Any]] = []

    def assess_batch(self, talents: List[TalentInput]) -> List[Dict[str, Any]]:
        self._results = [self._assess(t) for t in talents]
        return self._results

    def _assess(self, t: TalentInput) -> Dict[str, Any]:
        obs = _obsolescence_score(t)
        flt = _flight_score(t)
        val = _value_score(t)
        suc = _succession_score(t)
        comp = _composite(obs, flt, val, suc)
        pattern = _talent_pattern(t)
        risk = _risk(comp)
        sev = _severity(comp)
        act = _action(risk, pattern)
        sig = _signal(t, pattern, comp)

        return {
            "talent_id": t.talent_id,
            "talent_segment": t.talent_segment,
            "region": t.region,
            "talent_risk": risk,
            "talent_pattern": pattern,
            "talent_severity": sev,
            "recommended_action": act,
            "obsolescence_score": round(obs * 100, 2),
            "flight_score": round(flt * 100, 2),
            "value_score": round(val * 100, 2),
            "succession_score": round(suc * 100, 2),
            "talent_composite": comp,
            "has_obsolescence_signal": comp >= 40.0 or t.skill_half_life_risk >= 0.60 or t.skills_future_alignment <= 0.30,
            "requires_urgent_intervention": comp >= 25.0 or t.flight_risk_index >= 0.65 or t.succession_pipeline_readiness <= 0.25,
            "estimated_talent_risk_index": min(round(comp / 100.0 * (1.0 - t.human_capital_value_score + 0.01) * 10 * 100) / 100, 10.0),
            "talent_signal": sig,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        if not self._results:
            return {}
        n = len(self._results)
        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        t_obs = t_flt = t_val = t_suc = t_comp = t_risk_idx = 0.0
        obs_c = urgent_c = 0

        for r in self._results:
            risk_counts[r["talent_risk"]] = risk_counts.get(r["talent_risk"], 0) + 1
            pattern_counts[r["talent_pattern"]] = pattern_counts.get(r["talent_pattern"], 0) + 1
            severity_counts[r["talent_severity"]] = severity_counts.get(r["talent_severity"], 0) + 1
            action_counts[r["recommended_action"]] = action_counts.get(r["recommended_action"], 0) + 1
            t_obs += r["obsolescence_score"]
            t_flt += r["flight_score"]
            t_val += r["value_score"]
            t_suc += r["succession_score"]
            t_comp += r["talent_composite"]
            t_risk_idx += r["estimated_talent_risk_index"]
            if r["has_obsolescence_signal"]:
                obs_c += 1
            if r["requires_urgent_intervention"]:
                urgent_c += 1

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_obsolescence_score": round(t_obs / n, 1),
            "avg_flight_score": round(t_flt / n, 1),
            "avg_value_score": round(t_val / n, 1),
            "avg_succession_score": round(t_suc / n, 1),
            "avg_talent_composite": round(t_comp / n, 1),
            "obsolescence_signal_count": obs_c,
            "urgent_intervention_count": urgent_c,
            "avg_estimated_talent_risk_index": round(t_risk_idx / n, 2),
            "talents": self._results,
            "engine": "predictive_talent_intelligence_engine_v277",
        }

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        if not self._results:
            return {}
        n = len(self._results)
        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        t_obs = t_flt = t_val = t_suc = t_comp = t_risk_idx = 0.0
        obs_c = urgent_c = 0

        for r in self._results:
            risk_counts[r["talent_risk"]] = risk_counts.get(r["talent_risk"], 0) + 1
            pattern_counts[r["talent_pattern"]] = pattern_counts.get(r["talent_pattern"], 0) + 1
            severity_counts[r["talent_severity"]] = severity_counts.get(r["talent_severity"], 0) + 1
            action_counts[r["recommended_action"]] = action_counts.get(r["recommended_action"], 0) + 1
            t_obs += r["obsolescence_score"]
            t_flt += r["flight_score"]
            t_val += r["value_score"]
            t_suc += r["succession_score"]
            t_comp += r["talent_composite"]
            t_risk_idx += r["estimated_talent_risk_index"]
            if r["has_obsolescence_signal"]:
                obs_c += 1
            if r["requires_urgent_intervention"]:
                urgent_c += 1

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_talent_composite": round(t_comp / n, 1),
            "obsolescence_signal_count": obs_c,
            "urgent_intervention_count": urgent_c,
            "avg_obsolescence_score": round(t_obs / n, 1),
            "avg_flight_score": round(t_flt / n, 1),
            "avg_succession_score": round(t_suc / n, 1),
            "avg_value_score": round(t_val / n, 1),
            "avg_estimated_talent_risk_index": round(t_risk_idx / n, 2),
        }
