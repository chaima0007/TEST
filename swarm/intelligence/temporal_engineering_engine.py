from dataclasses import dataclass
from typing import List


@dataclass
class TemporalHorizonInput:
    horizon_id: str
    temporal_domain: str  # micro_tactical/meso_strategic/macro_structural/meta_civilizational/quantum_temporal/cyclical_historical/emergent_futures/retroactive_causality
    region: str
    timeline_divergence_risk: float            # higher=worse
    chronological_coherence_score: float
    anticipation_horizon_depth: float
    temporal_blind_spot_ratio: float           # higher=worse
    multi_scale_synchronization: float
    intervention_window_precision: float
    causal_loop_detection_score: float         # higher=worse if uncontrolled
    future_optionality_score: float
    temporal_leverage_index: float
    chronological_risk_concentration: float    # higher=worse
    scenario_branching_factor: float           # higher=worse — too many branches = chaos
    retroactive_impact_sensitivity: float      # higher=worse
    temporal_resilience_score: float
    clock_speed_mismatch_risk: float           # higher=worse — misalign between org clock vs market clock
    anticipation_accuracy_score: float
    decision_timing_optimality: float
    temporal_arbitrage_potential: float


def _clamp(v: float) -> float:
    return max(0.0, min(1.0, v))


def _divergence_score(h: TemporalHorizonInput) -> float:
    """Higher = worse divergence (bad). Uses direct risk values."""
    return _clamp(
        h.timeline_divergence_risk * 0.40
        + h.scenario_branching_factor * 0.35
        + h.chronological_risk_concentration * 0.25
    )


def _anticipation_score(h: TemporalHorizonInput) -> float:
    """Higher = worse anticipation. temporal_blind_spot_ratio direct; others inverted."""
    return _clamp(
        h.temporal_blind_spot_ratio * 0.40
        + (1.0 - h.anticipation_accuracy_score) * 0.35
        + (1.0 - h.intervention_window_precision) * 0.25
    )


def _synchronization_score(h: TemporalHorizonInput) -> float:
    """Higher = worse synchronisation."""
    return _clamp(
        h.clock_speed_mismatch_risk * 0.40
        + (1.0 - h.multi_scale_synchronization) * 0.35
        + (1.0 - h.chronological_coherence_score) * 0.25
    )


def _resilience_score(h: TemporalHorizonInput) -> float:
    """Higher = worse resilience."""
    return _clamp(
        (1.0 - h.temporal_resilience_score) * 0.40
        + h.retroactive_impact_sensitivity * 0.35
        + h.causal_loop_detection_score * 0.25
    )


def _composite(div: float, ant: float, syn: float, res: float) -> float:
    return round(
        (div * 0.30 + ant * 0.25 + syn * 0.25 + res * 0.20) * 100, 2
    )


def _pattern(h: TemporalHorizonInput) -> str:
    if h.timeline_divergence_risk >= 0.70 and h.scenario_branching_factor >= 0.65:
        return "timeline_bifurcation"
    if h.temporal_blind_spot_ratio >= 0.65 and h.anticipation_accuracy_score <= 0.35:
        return "temporal_blind_spot"
    if h.clock_speed_mismatch_risk >= 0.65 and h.multi_scale_synchronization <= 0.40:
        return "chronological_desync"
    if h.causal_loop_detection_score >= 0.70:
        return "causal_loop_trap"
    if h.future_optionality_score <= 0.25 and h.scenario_branching_factor <= 0.25:
        return "future_optionality_collapse"
    return "none"


def _risk(comp: float) -> str:
    if comp >= 60:
        return "critical"
    if comp >= 40:
        return "high"
    if comp >= 20:
        return "moderate"
    return "low"


def _severity(comp: float) -> str:
    if comp >= 60:
        return "temporally_lost"
    if comp >= 40:
        return "desynchronized"
    if comp >= 20:
        return "anticipating"
    return "temporally_mastered"


def _action(r: str, p: str) -> str:
    if r == "critical":
        if p in ("timeline_bifurcation", "causal_loop_trap", "future_optionality_collapse"):
            return "temporal_emergency_realignment"
        return "timeline_convergence_protocol"
    if r == "high":
        if p in ("chronological_desync",):
            return "chronological_resync"
        return "anticipation_upgrade"
    if r == "moderate":
        return "temporal_monitoring"
    return "no_action"


def _signal(h: TemporalHorizonInput, pat: str, comp: float) -> str:
    coh_pct = round(h.chronological_coherence_score * 100)
    win_pct = round(h.intervention_window_precision * 100)
    arb = round(h.temporal_arbitrage_potential, 2)
    if comp < 20:
        return (
            f"Maîtrise temporelle multi-chronologique — cohérence {coh_pct}% "
            f"— fenêtre intervention {win_pct}% — arbitrage temporel {arb}"
        )
    labels = {
        "timeline_bifurcation": "Bifurcation temporelle détectée",
        "temporal_blind_spot": "Zone aveugle temporelle critique",
        "chronological_desync": "Désynchronisation chronologique active",
        "causal_loop_trap": "Piège boucle causale identifiée",
        "future_optionality_collapse": "Effondrement optionnalité future",
        "none": "Anomalie temporelle diffuse",
    }
    label = labels.get(pat, pat.replace("_", " "))
    div_pct = round(h.timeline_divergence_risk * 100)
    blind_pct = round(h.temporal_blind_spot_ratio * 100)
    return (
        f"{label} — divergence timeline {div_pct}% — zone aveugle {blind_pct}% "
        f"— cohérence {coh_pct}% — fenêtre intervention {win_pct}% "
        f"— arbitrage temporel {arb} — composite {round(comp)}"
    )


class TemporalEngineeringEngine:
    def __init__(self):
        self._results: list = []

    def assess_batch(self, horizons: List[TemporalHorizonInput]) -> List[dict]:
        self._results = [self._assess(h) for h in horizons]
        return self._results

    def _assess(self, h: TemporalHorizonInput) -> dict:
        div = _divergence_score(h)
        ant = _anticipation_score(h)
        syn = _synchronization_score(h)
        res = _resilience_score(h)
        comp = _composite(div, ant, syn, res)
        pat = _pattern(h)
        r = _risk(comp)
        sev = _severity(comp)
        act = _action(r, pat)
        sig = _signal(h, pat, comp)
        return {
            "horizon_id": h.horizon_id,
            "temporal_domain": h.temporal_domain,
            "region": h.region,
            "temporal_risk": r,
            "temporal_pattern": pat,
            "temporal_severity": sev,
            "recommended_action": act,
            "divergence_score": round(div * 100, 2),
            "anticipation_score": round(ant * 100, 2),
            "synchronization_score": round(syn * 100, 2),
            "resilience_score": round(res * 100, 2),
            "temporal_composite": comp,
            "has_bifurcation_signal": pat in ("timeline_bifurcation", "causal_loop_trap"),
            "requires_realignment": comp >= 25 or h.timeline_divergence_risk >= 0.55 or h.clock_speed_mismatch_risk >= 0.60,
            "estimated_temporal_risk_index": min(round(comp / 100 * (1 - h.temporal_resilience_score + 0.01) * 10 * 100) / 100, 10.0),
            "temporal_signal": sig,
        }

    def summary(self) -> dict:
        if not self._results:
            return {}
        n = len(self._results)
        rc: dict = {}
        pc: dict = {}
        sc: dict = {}
        ac: dict = {}
        t_div = t_ant = t_syn = t_res = t_comp = t_idx = 0.0
        bif_c = real_c = 0
        for r in self._results:
            rc[r["temporal_risk"]] = rc.get(r["temporal_risk"], 0) + 1
            pc[r["temporal_pattern"]] = pc.get(r["temporal_pattern"], 0) + 1
            sc[r["temporal_severity"]] = sc.get(r["temporal_severity"], 0) + 1
            ac[r["recommended_action"]] = ac.get(r["recommended_action"], 0) + 1
            t_div += r["divergence_score"]
            t_ant += r["anticipation_score"]
            t_syn += r["synchronization_score"]
            t_res += r["resilience_score"]
            t_comp += r["temporal_composite"]
            t_idx += r["estimated_temporal_risk_index"]
            if r["has_bifurcation_signal"]:
                bif_c += 1
            if r["requires_realignment"]:
                real_c += 1
        return {
            "total": n,
            "risk_counts": rc,
            "pattern_counts": pc,
            "severity_counts": sc,
            "action_counts": ac,
            "avg_temporal_composite": round(t_comp / n * 10) / 10,
            "bifurcation_signal_count": bif_c,
            "realignment_required_count": real_c,
            "avg_divergence_score": round(t_div / n * 10) / 10,
            "avg_anticipation_score": round(t_ant / n * 10) / 10,
            "avg_synchronization_score": round(t_syn / n * 10) / 10,
            "avg_resilience_score": round(t_res / n * 10) / 10,
            "avg_estimated_temporal_risk_index": round(t_idx / n * 100) / 100,
        }

    def to_dict(self) -> dict:
        """Returns exactly 15 keys."""
        s = self.summary()
        horizons = self._results
        n = len(horizons)
        critical = [h for h in horizons if h["temporal_risk"] == "critical"]
        high = [h for h in horizons if h["temporal_risk"] == "high"]
        return {
            "engine": "TemporalEngineeringEngine",
            "version": "1.0.0",
            "total_horizons": n,
            "critical_count": len(critical),
            "high_count": len(high),
            "bifurcation_signal_count": s.get("bifurcation_signal_count", 0),
            "realignment_required_count": s.get("realignment_required_count", 0),
            "avg_temporal_composite": s.get("avg_temporal_composite", 0.0),
            "avg_divergence_score": s.get("avg_divergence_score", 0.0),
            "avg_anticipation_score": s.get("avg_anticipation_score", 0.0),
            "avg_synchronization_score": s.get("avg_synchronization_score", 0.0),
            "avg_resilience_score": s.get("avg_resilience_score", 0.0),
            "avg_estimated_temporal_risk_index": s.get("avg_estimated_temporal_risk_index", 0.0),
            "summary": s,
            "horizons": horizons,
        }
