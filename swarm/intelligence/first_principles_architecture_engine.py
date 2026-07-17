"""
Engine: First Principles Architecture Intelligence Engine
Module 313 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class FirstPrinciplesInput:
    entity_id: str
    domain_type: str
    region: str
    assumption_density: float
    conventional_wisdom_dependency: float
    analogy_reasoning_reliance: float
    first_order_thinking_dominance: float
    mental_model_rigidity: float
    epistemic_closure_risk: float
    innovation_constraint_index: float
    reasoning_from_authority_bias: float
    complexity_masking_fundamentals: float
    cost_estimation_accuracy: float  # inverse: high=good
    physics_constraint_violation_risk: float
    path_dependency_lock_in: float
    abstraction_layer_opacity: float
    benchmark_anchoring_distortion: float
    consensus_capture_risk: float
    inversion_thinking_deficit: float
    regenerative_capacity: float  # inverse: high=good


@dataclass
class FirstPrinciplesResult:
    entity_id: str
    region: str
    domain_type: str
    principles_risk: str
    principles_pattern: str
    principles_severity: str
    recommended_action: str
    assumption_score: float
    rigidity_score: float
    blindspot_score: float
    innovation_score: float
    principles_composite: float
    is_principles_crisis: bool
    requires_principles_intervention: bool
    principles_signal: str

    def to_dict(self) -> Dict:
        return {
            "entity_id":                        self.entity_id,
            "region":                           self.region,
            "domain_type":                      self.domain_type,
            "principles_risk":                  self.principles_risk,
            "principles_pattern":               self.principles_pattern,
            "principles_severity":              self.principles_severity,
            "recommended_action":               self.recommended_action,
            "assumption_score":                 self.assumption_score,
            "rigidity_score":                   self.rigidity_score,
            "blindspot_score":                  self.blindspot_score,
            "innovation_score":                 self.innovation_score,
            "principles_composite":             self.principles_composite,
            "is_principles_crisis":             self.is_principles_crisis,
            "requires_principles_intervention": self.requires_principles_intervention,
            "principles_signal":                self.principles_signal,
        }


class FirstPrinciplesArchitectureEngine:
    def __init__(self) -> None:
        self._results: List[FirstPrinciplesResult] = []

    def _assumption_score(self, i: FirstPrinciplesInput) -> float:
        return round(
            (i.assumption_density * 0.4
             + i.conventional_wisdom_dependency * 0.35
             + i.analogy_reasoning_reliance * 0.25) * 100,
            2,
        )

    def _rigidity_score(self, i: FirstPrinciplesInput) -> float:
        return round(
            (i.mental_model_rigidity * 0.4
             + i.epistemic_closure_risk * 0.35
             + i.path_dependency_lock_in * 0.25) * 100,
            2,
        )

    def _blindspot_score(self, i: FirstPrinciplesInput) -> float:
        return round(
            (i.complexity_masking_fundamentals * 0.4
             + i.abstraction_layer_opacity * 0.35
             + i.benchmark_anchoring_distortion * 0.25) * 100,
            2,
        )

    def _innovation_score(self, i: FirstPrinciplesInput) -> float:
        return round(
            (i.innovation_constraint_index * 0.4
             + i.inversion_thinking_deficit * 0.35
             + (1 - i.regenerative_capacity) * 0.25) * 100,
            2,
        )

    def _composite(self, assumption: float, rigidity: float, blindspot: float, innovation: float) -> float:
        return round(
            assumption * 0.30
            + rigidity * 0.25
            + blindspot * 0.25
            + innovation * 0.20,
            2,
        )

    def _risk(self, c: float) -> str:
        if c >= 60: return "critical"
        if c >= 40: return "high"
        if c >= 20: return "moderate"
        return "low"

    def _pattern(self, i: FirstPrinciplesInput) -> str:
        if i.assumption_density >= 0.70 and i.conventional_wisdom_dependency >= 0.65:
            return "assumption_collapse"
        if i.mental_model_rigidity >= 0.70 and i.epistemic_closure_risk >= 0.65:
            return "epistemic_lock"
        if i.complexity_masking_fundamentals >= 0.70 and i.abstraction_layer_opacity >= 0.65:
            return "complexity_blindness"
        if i.innovation_constraint_index >= 0.70 and i.inversion_thinking_deficit >= 0.65:
            return "innovation_atrophy"
        if i.benchmark_anchoring_distortion >= 0.70 and i.consensus_capture_risk >= 0.65:
            return "benchmark_trap"
        return "none"

    def _severity(self, c: float) -> str:
        if c >= 75: return "systemic_blindness_crisis"
        if c >= 50: return "high_assumption_risk"
        if c >= 25: return "assumption_accumulation"
        return "first_principles_sound"

    def _action(self, risk: str, pattern: str) -> str:
        if risk == "critical":
            return "full_assumption_audit"
        if risk == "high" and pattern == "epistemic_lock":
            return "mindset_reconstruction"
        if risk == "high":
            return "first_principles_review"
        if risk == "moderate":
            return "assumption_mapping"
        return "no_action"

    def _signal(self, i: FirstPrinciplesInput, pattern: str, comp: float) -> str:
        if comp < 20:
            return (
                "Premiers principes solides — densité d'hypothèses faible, "
                "modèles mentaux flexibles, angles morts limités, innovation active"
            )
        pattern_labels: Dict[str, str] = {
            "assumption_collapse":  "Effondrement d'hypothèses",
            "epistemic_lock":       "Verrouillage épistémique",
            "complexity_blindness": "Aveuglement par la complexité",
            "innovation_atrophy":   "Atrophie de l'innovation",
            "benchmark_trap":       "Piège du benchmark",
        }
        label = pattern_labels.get(pattern, "Critique")
        return (
            f"{label} — "
            f"densité d'hypothèses non vérifiées {round(i.assumption_density * 100)}% — "
            f"verrouillage épistémique — "
            f"composite {round(comp)}"
        )

    def _analyze_one(self, i: FirstPrinciplesInput) -> FirstPrinciplesResult:
        assumption  = self._assumption_score(i)
        rigidity    = self._rigidity_score(i)
        blindspot   = self._blindspot_score(i)
        innovation  = self._innovation_score(i)
        comp        = self._composite(assumption, rigidity, blindspot, innovation)
        risk        = self._risk(comp)
        pattern     = self._pattern(i)
        severity    = self._severity(comp)
        action      = self._action(risk, pattern)

        result = FirstPrinciplesResult(
            entity_id=i.entity_id,
            region=i.region,
            domain_type=i.domain_type,
            principles_risk=risk,
            principles_pattern=pattern,
            principles_severity=severity,
            recommended_action=action,
            assumption_score=assumption,
            rigidity_score=rigidity,
            blindspot_score=blindspot,
            innovation_score=innovation,
            principles_composite=comp,
            is_principles_crisis=comp >= 60,
            requires_principles_intervention=comp >= 40,
            principles_signal=self._signal(i, pattern, comp),
        )
        self._results.append(result)
        return result

    def analyze(self, entities: List[FirstPrinciplesInput]) -> Dict[str, Any]:
        results = [self._analyze_one(e) for e in entities]
        n = len(results)
        if n == 0:
            return {
                "total_entities_analyzed":              0,
                "critical_principles_risk":             0,
                "high_principles_risk":                 0,
                "moderate_principles_risk":             0,
                "low_principles_risk":                  0,
                "principles_crises_detected":           0,
                "requires_intervention_count":          0,
                "avg_assumption_score":                 0.0,
                "avg_rigidity_score":                   0.0,
                "avg_blindspot_score":                  0.0,
                "avg_innovation_score":                 0.0,
                "avg_estimated_principles_weakness_index": 0.0,
                "entity_results":                       [],
            }

        critical_count  = sum(1 for r in results if r.principles_risk == "critical")
        high_count      = sum(1 for r in results if r.principles_risk == "high")
        moderate_count  = sum(1 for r in results if r.principles_risk == "moderate")
        low_count       = sum(1 for r in results if r.principles_risk == "low")
        crisis_count    = sum(1 for r in results if r.is_principles_crisis)
        interv_count    = sum(1 for r in results if r.requires_principles_intervention)

        avg_assumption  = round(sum(r.assumption_score  for r in results) / n, 1)
        avg_rigidity    = round(sum(r.rigidity_score    for r in results) / n, 1)
        avg_blindspot   = round(sum(r.blindspot_score   for r in results) / n, 1)
        avg_innovation  = round(sum(r.innovation_score  for r in results) / n, 1)
        avg_composite   = sum(r.principles_composite for r in results) / n
        weakness_index  = round(avg_composite / 100 * 10, 2)

        return {
            "total_entities_analyzed":                  n,
            "critical_principles_risk":                 critical_count,
            "high_principles_risk":                     high_count,
            "moderate_principles_risk":                 moderate_count,
            "low_principles_risk":                      low_count,
            "principles_crises_detected":               crisis_count,
            "requires_intervention_count":              interv_count,
            "avg_assumption_score":                     avg_assumption,
            "avg_rigidity_score":                       avg_rigidity,
            "avg_blindspot_score":                      avg_blindspot,
            "avg_innovation_score":                     avg_innovation,
            "avg_estimated_principles_weakness_index":  weakness_index,
            "entity_results":                           [r.to_dict() for r in results],
        }
