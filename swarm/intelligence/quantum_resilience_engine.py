"""
Quantum Resilience & Adaptive Defense Engine — Module 280

Évalue la résilience organisationnelle/systémique via des stratégies de
défense adaptative d'inspiration quantique.

Scores sub-composites (0-100, plus haut = risque plus élevé):
  coherence_score      (poids 0.30)
  adaptation_score     (poids 0.25)
  neutralization_score (poids 0.25)
  synchrony_score      (poids 0.20)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


# ── Input ──────────────────────────────────────────────────────────────────────

@dataclass
class QuantumResilienceInput:
    entity_id: str
    defense_layer: str
    region: str
    # 17 float fields (0.0–1.0)
    quantum_coherence: float
    adaptive_capacity: float
    threat_neutralization: float
    system_redundancy: float
    attack_surface_reduction: float
    recovery_velocity: float
    cross_layer_synchrony: float
    anomaly_detection: float
    self_healing_rate: float
    defensive_posture: float
    resilience_depth: float
    entropy_management: float
    cascade_prevention: float
    adaptive_immunity: float
    quantum_entanglement_index: float
    decoherence_risk: float
    vulnerability_exposure: float


# ── Output ─────────────────────────────────────────────────────────────────────

@dataclass
class QuantumResilienceResult:
    entity_id: str
    region: str
    defense_layer: str
    resilience_risk: str
    resilience_pattern: str
    resilience_severity: str
    recommended_action: str
    coherence_score: float
    adaptation_score: float
    neutralization_score: float
    synchrony_score: float
    resilience_composite: float
    is_in_resilience_crisis: bool
    requires_immediate_reinforcement: bool
    resilience_signal: str

    def to_dict(self) -> dict:
        return {
            "entity_id":                      self.entity_id,
            "region":                         self.region,
            "defense_layer":                  self.defense_layer,
            "resilience_risk":                self.resilience_risk,
            "resilience_pattern":             self.resilience_pattern,
            "resilience_severity":            self.resilience_severity,
            "recommended_action":             self.recommended_action,
            "coherence_score":                round(self.coherence_score, 2),
            "adaptation_score":               round(self.adaptation_score, 2),
            "neutralization_score":           round(self.neutralization_score, 2),
            "synchrony_score":                round(self.synchrony_score, 2),
            "resilience_composite":           round(self.resilience_composite, 2),
            "is_in_resilience_crisis":        self.is_in_resilience_crisis,
            "requires_immediate_reinforcement": self.requires_immediate_reinforcement,
            "resilience_signal":              self.resilience_signal,
        }


# ── Scoring helpers ─────────────────────────────────────────────────────────────

def _coherence_score(inp: QuantumResilienceInput) -> float:
    """weight 0.30 — higher = worse coherence (more decoherence risk)"""
    return (
        inp.decoherence_risk * 0.4
        + inp.vulnerability_exposure * 0.3
        + (1 - inp.quantum_coherence) * 0.3
    ) * 100


def _adaptation_score(inp: QuantumResilienceInput) -> float:
    """weight 0.25 — higher = worse adaptation"""
    return (
        (1 - inp.adaptive_capacity) * 0.35
        + (1 - inp.adaptive_immunity) * 0.35
        + (1 - inp.self_healing_rate) * 0.30
    ) * 100


def _neutralization_score(inp: QuantumResilienceInput) -> float:
    """weight 0.25 — higher = worse neutralization"""
    return (
        (1 - inp.threat_neutralization) * 0.4
        + (1 - inp.anomaly_detection) * 0.3
        + (1 - inp.attack_surface_reduction) * 0.3
    ) * 100


def _synchrony_score(inp: QuantumResilienceInput) -> float:
    """weight 0.20 — higher = worse synchrony"""
    return (
        (1 - inp.cross_layer_synchrony) * 0.4
        + (1 - inp.cascade_prevention) * 0.35
        + (1 - inp.entropy_management) * 0.25
    ) * 100


def _composite(coh: float, ada: float, neu: float, syn: float) -> float:
    return coh * 0.30 + ada * 0.25 + neu * 0.25 + syn * 0.20


def _risk_level(comp: float) -> str:
    if comp >= 60:
        return "critical"
    if comp >= 40:
        return "high"
    if comp >= 20:
        return "moderate"
    return "low"


def _pattern(inp: QuantumResilienceInput) -> str:
    if inp.decoherence_risk >= 0.65 and (1 - inp.quantum_coherence) >= 0.50:
        return "quantum_decoherence"
    if (1 - inp.adaptive_capacity) >= 0.60 and (1 - inp.self_healing_rate) >= 0.55:
        return "adaptive_failure"
    if (1 - inp.cascade_prevention) >= 0.65 and (1 - inp.cross_layer_synchrony) >= 0.55:
        return "cascade_collapse"
    if inp.vulnerability_exposure >= 0.65 and (1 - inp.threat_neutralization) >= 0.55:
        return "vulnerability_breach"
    if (1 - inp.adaptive_immunity) >= 0.65:
        return "immune_breakdown"
    return "none"


def _severity(comp: float) -> str:
    if comp >= 75:
        return "collapsed"
    if comp >= 50:
        return "critical_stress"
    if comp >= 25:
        return "degrading"
    return "resilient"


def _action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "quantum_reinforcement_emergency"
    if risk == "high":
        if pattern == "quantum_decoherence":
            return "decoherence_correction"
        return "adaptive_defense_protocol"
    if risk == "moderate":
        return "resilience_monitoring"
    return "no_action"


def _signal(
    inp: QuantumResilienceInput,
    risk: str,
    coherence_score: float,
    adaptation_score: float,
    synchrony_score: float,
    composite: float,
) -> str:
    if risk == "critical":
        return (
            f"Critique — cohérence quantique {100 - int(coherence_score)}% "
            f"— immunité adaptative {100 - int(adaptation_score)}% "
            f"— composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — vulnérabilité {int(inp.vulnerability_exposure * 100)}% "
            f"— synchronie {100 - int(synchrony_score)}% "
            f"— composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — capacité adaptative {int(inp.adaptive_capacity * 100)}% "
            f"— résilience composite {int(composite)}"
        )
    return "Résilience quantique optimale — défenses adaptatives stables, cohérence maintenue"


# ── Engine ─────────────────────────────────────────────────────────────────────

class QuantumResilienceEngine:
    """Évalue un batch d'entités et produit un résumé agrégé."""

    def _assess_one(self, inp: QuantumResilienceInput) -> QuantumResilienceResult:
        coh = _coherence_score(inp)
        ada = _adaptation_score(inp)
        neu = _neutralization_score(inp)
        syn = _synchrony_score(inp)
        comp = _composite(coh, ada, neu, syn)

        risk = _risk_level(comp)
        pat = _pattern(inp)
        sev = _severity(comp)
        act = _action(risk, pat)
        sig = _signal(inp, risk, coh, ada, syn, comp)

        return QuantumResilienceResult(
            entity_id=inp.entity_id,
            region=inp.region,
            defense_layer=inp.defense_layer,
            resilience_risk=risk,
            resilience_pattern=pat,
            resilience_severity=sev,
            recommended_action=act,
            coherence_score=coh,
            adaptation_score=ada,
            neutralization_score=neu,
            synchrony_score=syn,
            resilience_composite=comp,
            is_in_resilience_crisis=(comp >= 60),
            requires_immediate_reinforcement=(comp >= 40),
            resilience_signal=sig,
        )

    def assess_batch(self, inputs: List[QuantumResilienceInput]) -> List[dict]:
        """Évalue une liste d'entités, retourne une liste de dicts."""
        return [self._assess_one(inp).to_dict() for inp in inputs]

    def summary(self, results: List[dict]) -> dict:
        """
        Retourne exactement 13 clés agrégées:
          total, risk_counts, pattern_counts, severity_counts, action_counts,
          avg_resilience_composite, resilience_crisis_count,
          immediate_reinforcement_count,
          avg_coherence_score, avg_adaptation_score,
          avg_neutralization_score, avg_synchrony_score,
          avg_estimated_resilience_index
        """
        n = len(results)
        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_resilience_composite": 0.0,
                "resilience_crisis_count": 0,
                "immediate_reinforcement_count": 0,
                "avg_coherence_score": 0.0,
                "avg_adaptation_score": 0.0,
                "avg_neutralization_score": 0.0,
                "avg_synchrony_score": 0.0,
                "avg_estimated_resilience_index": 0.0,
            }

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        t_comp = 0.0
        t_coh = 0.0
        t_ada = 0.0
        t_neu = 0.0
        t_syn = 0.0
        crisis_count = 0
        reinf_count = 0

        for r in results:
            rk = r["resilience_risk"]
            pt = r["resilience_pattern"]
            sv = r["resilience_severity"]
            ac = r["recommended_action"]
            risk_counts[rk]    = risk_counts.get(rk, 0) + 1
            pattern_counts[pt] = pattern_counts.get(pt, 0) + 1
            severity_counts[sv] = severity_counts.get(sv, 0) + 1
            action_counts[ac]  = action_counts.get(ac, 0) + 1

            t_comp += r["resilience_composite"]
            t_coh  += r["coherence_score"]
            t_ada  += r["adaptation_score"]
            t_neu  += r["neutralization_score"]
            t_syn  += r["synchrony_score"]

            if r["is_in_resilience_crisis"]:
                crisis_count += 1
            if r["requires_immediate_reinforcement"]:
                reinf_count += 1

        avg_comp = round(t_comp / n, 1)

        return {
            "total":                          n,
            "risk_counts":                    risk_counts,
            "pattern_counts":                 pattern_counts,
            "severity_counts":                severity_counts,
            "action_counts":                  action_counts,
            "avg_resilience_composite":       avg_comp,
            "resilience_crisis_count":        crisis_count,
            "immediate_reinforcement_count":  reinf_count,
            "avg_coherence_score":            round(t_coh / n, 1),
            "avg_adaptation_score":           round(t_ada / n, 1),
            "avg_neutralization_score":       round(t_neu / n, 1),
            "avg_synchrony_score":            round(t_syn / n, 1),
            "avg_estimated_resilience_index": round(avg_comp / 100 * 10, 2),
        }
