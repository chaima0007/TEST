"""
Module 312 — Geopolitical Alliance Fracture & Multipolar Realignment Intelligence Engine
Monitors alliance cohesion, defection risk, trust erosion, legitimacy crises, and
multipolar fragmentation across global alliance structures.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AllianceFractureInput:
    entity_id: str
    alliance_type: str
    region: str
    # 17 float fields (0.0–1.0)
    internal_cohesion_erosion: float            # 0-1
    burden_sharing_imbalance: float             # 0-1
    strategic_interest_divergence: float        # 0-1
    external_pressure_index: float              # 0-1
    defection_incentive_strength: float         # 0-1
    alternative_alignment_attractiveness: float # 0-1
    historical_grievance_activation: float      # 0-1
    democratic_backsliding_within_alliance: float  # 0-1
    economic_decoupling_pressure: float         # 0-1
    nuclear_deterrence_reliability: float       # 0-1, inverse: high=good
    intelligence_trust_deficit: float           # 0-1
    sanctions_fatigue_index: float              # 0-1
    populist_alliance_skepticism: float         # 0-1
    technology_rivalry_within_alliance: float   # 0-1
    leadership_legitimacy_crisis: float         # 0-1
    treaty_obligation_strain: float             # 0-1
    multipolar_fragmentation_index: float       # 0-1


@dataclass
class AllianceFractureResult:
    entity_id: str
    region: str
    alliance_type: str
    fracture_risk: str
    fracture_pattern: str
    fracture_severity: str
    recommended_action: str
    cohesion_score: float
    defection_score: float
    trust_score: float
    legitimacy_score: float
    fracture_composite: float
    is_fracture_crisis: bool
    requires_fracture_intervention: bool
    fracture_signal: str

    def to_dict(self) -> Dict:
        return {
            "entity_id":                      self.entity_id,
            "region":                         self.region,
            "alliance_type":                  self.alliance_type,
            "fracture_risk":                  self.fracture_risk,
            "fracture_pattern":               self.fracture_pattern,
            "fracture_severity":              self.fracture_severity,
            "recommended_action":             self.recommended_action,
            "cohesion_score":                 self.cohesion_score,
            "defection_score":                self.defection_score,
            "trust_score":                    self.trust_score,
            "legitimacy_score":               self.legitimacy_score,
            "fracture_composite":             self.fracture_composite,
            "is_fracture_crisis":             self.is_fracture_crisis,
            "requires_fracture_intervention": self.requires_fracture_intervention,
            "fracture_signal":                self.fracture_signal,
        }


class GeopoliticalAllianceFractureEngine:
    """
    Module 312 — Geopolitical Alliance Fracture & Multipolar Realignment Intelligence Engine
    Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
    """

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100)                                                  #
    # ------------------------------------------------------------------ #

    def _cohesion_score(self, i: AllianceFractureInput) -> float:
        return round(
            (
                i.internal_cohesion_erosion * 0.4
                + i.strategic_interest_divergence * 0.35
                + i.burden_sharing_imbalance * 0.25
            ) * 100,
            2,
        )

    def _defection_score(self, i: AllianceFractureInput) -> float:
        return round(
            (
                i.defection_incentive_strength * 0.4
                + i.alternative_alignment_attractiveness * 0.35
                + i.economic_decoupling_pressure * 0.25
            ) * 100,
            2,
        )

    def _trust_score(self, i: AllianceFractureInput) -> float:
        return round(
            (
                i.intelligence_trust_deficit * 0.4
                + i.treaty_obligation_strain * 0.35
                + (1 - i.nuclear_deterrence_reliability) * 0.25
            ) * 100,
            2,
        )

    def _legitimacy_score(self, i: AllianceFractureInput) -> float:
        return round(
            (
                i.leadership_legitimacy_crisis * 0.4
                + i.populist_alliance_skepticism * 0.35
                + i.democratic_backsliding_within_alliance * 0.25
            ) * 100,
            2,
        )

    def _composite(
        self,
        cohesion: float,
        defection: float,
        trust: float,
        legitimacy: float,
    ) -> float:
        return round(
            cohesion * 0.30
            + defection * 0.25
            + trust * 0.25
            + legitimacy * 0.20,
            2,
        )

    # ------------------------------------------------------------------ #
    #  Risk classification                                                 #
    # ------------------------------------------------------------------ #

    def _risk(self, composite: float) -> str:
        if composite >= 60:
            return "critical"
        if composite >= 40:
            return "high"
        if composite >= 20:
            return "moderate"
        return "low"

    # ------------------------------------------------------------------ #
    #  Pattern detection (first match wins)                                #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: AllianceFractureInput) -> str:
        if i.internal_cohesion_erosion >= 0.70 and i.defection_incentive_strength >= 0.65:
            return "alliance_dissolution"
        if i.alternative_alignment_attractiveness >= 0.70 and i.strategic_interest_divergence >= 0.65:
            return "strategic_pivot"
        if i.intelligence_trust_deficit >= 0.70 and i.treaty_obligation_strain >= 0.65:
            return "trust_collapse"
        if i.populist_alliance_skepticism >= 0.70 and i.leadership_legitimacy_crisis >= 0.65:
            return "populist_defection"
        if i.economic_decoupling_pressure >= 0.70 and i.technology_rivalry_within_alliance >= 0.65:
            return "economic_fracture"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity                                                            #
    # ------------------------------------------------------------------ #

    def _severity(self, composite: float) -> str:
        if composite >= 75:
            return "alliance_emergency"
        if composite >= 50:
            return "high_fracture_risk"
        if composite >= 25:
            return "fracture_developing"
        return "alliance_stable"

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: str, pattern: str) -> str:
        if risk == "critical":
            return "alliance_emergency_summit"
        if risk == "high":
            if pattern == "strategic_pivot":
                return "realignment_containment"
            return "cohesion_reinforcement"
        if risk == "moderate":
            return "alliance_monitoring"
        return "no_action"

    # ------------------------------------------------------------------ #
    #  French signal                                                       #
    # ------------------------------------------------------------------ #

    def _signal(
        self,
        i: AllianceFractureInput,
        pattern: str,
        composite: float,
    ) -> str:
        if composite < 20:
            return (
                "Alliance stable — cohésion interne préservée, "
                "confiance mutuelle maintenue, risques de fracture maîtrisés"
            )
        if composite >= 60:
            return (
                f"Fracture critique détectée — cohésion {i.internal_cohesion_erosion:.2f}"
                f" — défection {i.defection_incentive_strength:.2f}"
                f" — confiance {i.intelligence_trust_deficit:.2f}"
                f" — composite {composite:.0f}"
            )
        if composite >= 40:
            labels: Dict[str, str] = {
                "alliance_dissolution": "Dissolution d'alliance",
                "strategic_pivot":      "Pivot stratégique",
                "trust_collapse":       "Effondrement de confiance",
                "populist_defection":   "Défection populiste",
                "economic_fracture":    "Fracture économique",
            }
            label = labels.get(pattern, pattern.replace("_", " ").title())
            return (
                f"Risque de fracture élevé — {label}"
                f" — cohésion {i.internal_cohesion_erosion:.2f}"
                f" — défection {i.defection_incentive_strength:.2f}"
                f" — composite {composite:.0f}"
            )
        return (
            f"Fracture en développement — tensions observées"
            f" — fragmentation multipolaire {i.multipolar_fragmentation_index:.2f}"
            f" — composite {composite:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def _analyze_one(self, i: AllianceFractureInput) -> AllianceFractureResult:
        cohesion   = self._cohesion_score(i)
        defection  = self._defection_score(i)
        trust      = self._trust_score(i)
        legitimacy = self._legitimacy_score(i)
        composite  = self._composite(cohesion, defection, trust, legitimacy)
        risk       = self._risk(composite)
        pattern    = self._pattern(i)
        severity   = self._severity(composite)
        action     = self._action(risk, pattern)
        signal     = self._signal(i, pattern, composite)

        return AllianceFractureResult(
            entity_id=i.entity_id,
            region=i.region,
            alliance_type=i.alliance_type,
            fracture_risk=risk,
            fracture_pattern=pattern,
            fracture_severity=severity,
            recommended_action=action,
            cohesion_score=cohesion,
            defection_score=defection,
            trust_score=trust,
            legitimacy_score=legitimacy,
            fracture_composite=composite,
            is_fracture_crisis=composite >= 60,
            requires_fracture_intervention=composite >= 40,
            fracture_signal=signal,
        )

    def analyze(self, entities: List[AllianceFractureInput]) -> Dict:
        results = [self._analyze_one(i) for i in entities]

        if not results:
            return {
                "module":                     "Module 312",
                "engine":                     "Geopolitical Alliance Fracture & Multipolar Realignment Intelligence Engine",
                "analyst":                    "Chaima Mhadbi",
                "location":                   "Bruxelles",
                "total_entities_analyzed":    0,
                "critical_fractures":         0,
                "high_fractures":             0,
                "moderate_fractures":         0,
                "stable_alliances":           0,
                "avg_estimated_fracture_index": 0.0,
                "fracture_crisis_entities":   [],
                "dominant_fracture_pattern":  "none",
                "results":                    [],
            }

        n = len(results)
        critical_fractures = sum(1 for r in results if r.fracture_risk == "critical")
        high_fractures     = sum(1 for r in results if r.fracture_risk == "high")
        moderate_fractures = sum(1 for r in results if r.fracture_risk == "moderate")
        stable_alliances   = sum(1 for r in results if r.fracture_risk == "low")

        avg_composite = sum(r.fracture_composite for r in results) / n

        fracture_crisis_entities = [r.entity_id for r in results if r.is_fracture_crisis]

        pattern_counts: Dict[str, int] = {}
        for r in results:
            pattern_counts[r.fracture_pattern] = pattern_counts.get(r.fracture_pattern, 0) + 1
        dominant_fracture_pattern = max(pattern_counts, key=lambda k: pattern_counts[k])

        return {
            "module":                        "Module 312",
            "engine":                        "Geopolitical Alliance Fracture & Multipolar Realignment Intelligence Engine",
            "analyst":                       "Chaima Mhadbi",
            "location":                      "Bruxelles",
            "total_entities_analyzed":       n,
            "critical_fractures":            critical_fractures,
            "high_fractures":                high_fractures,
            "moderate_fractures":            moderate_fractures,
            "stable_alliances":              stable_alliances,
            "avg_estimated_fracture_index":  round(avg_composite / 100 * 10, 2),
            "fracture_crisis_entities":      fracture_crisis_entities,
            "dominant_fracture_pattern":     dominant_fracture_pattern,
            "results":                       [r.to_dict() for r in results],
        }
