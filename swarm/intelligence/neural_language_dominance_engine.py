"""
Module 336 — Neural Language Dominance & Linguistic Intelligence Engine
Monitors AI-driven linguistic hegemony, cognitive colonisation, and the erosion
of multilingual sovereignty across language ecosystems.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class NeuralLanguageDominanceInput:
    entity_id: str
    language_domain: str
    region: str
    # 17 float fields (0.0–1.0)
    english_AI_training_bias: float               # 0-1
    linguistic_minority_exclusion_rate: float      # 0-1
    LLM_monolingual_dominance: float              # 0-1
    language_death_acceleration_index: float       # 0-1
    cognitive_framework_homogenization: float      # 0-1
    translation_sovereignty_risk: float            # 0-1
    AI_language_gatekeeping_power: float           # 0-1
    cultural_concept_untranslatability_loss: float # 0-1
    indigenous_language_AI_gap: float              # 0-1
    narrative_framing_linguistic_lock: float       # 0-1
    multilingual_AI_access_inequality: float       # 0-1
    syntactic_worldview_erosion: float             # 0-1
    linguistic_decolonization_resistance: float    # 0-1
    semantic_manipulation_via_language: float      # 0-1
    LLM_cultural_bias_propagation: float          # 0-1
    language_as_power_concentration: float         # 0-1
    cognitive_sovereignty_erosion_index: float     # 0-1


@dataclass
class NeuralLanguageDominanceResult:
    entity_id: str
    language_domain: str
    region: str
    dominance_score: float
    exclusion_score: float
    homogenization_score: float
    sovereignty_score: float
    composite_score: float
    risk_level: str
    language_pattern: str
    severity: str
    recommended_action: str
    signal: str
    english_AI_training_bias: float
    cognitive_sovereignty_erosion_index: float

    def to_dict(self) -> Dict:
        return {
            "entity_id":                             self.entity_id,
            "language_domain":                       self.language_domain,
            "region":                                self.region,
            "dominance_score":                       self.dominance_score,
            "exclusion_score":                       self.exclusion_score,
            "homogenization_score":                  self.homogenization_score,
            "sovereignty_score":                     self.sovereignty_score,
            "composite_score":                       self.composite_score,
            "risk_level":                            self.risk_level,
            "language_pattern":                      self.language_pattern,
            "severity":                              self.severity,
            "recommended_action":                    self.recommended_action,
            "signal":                                self.signal,
            "english_AI_training_bias":              self.english_AI_training_bias,
            "cognitive_sovereignty_erosion_index":   self.cognitive_sovereignty_erosion_index,
        }


class NeuralLanguageDominanceEngine:
    """
    Module 336 — Neural Language Dominance & Linguistic Intelligence Engine
    Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
    """

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100)                                                  #
    # ------------------------------------------------------------------ #

    def _dominance_score(self, i: NeuralLanguageDominanceInput) -> float:
        return round(
            (
                i.english_AI_training_bias * 0.40
                + i.LLM_monolingual_dominance * 0.35
                + i.AI_language_gatekeeping_power * 0.25
            ) * 100,
            2,
        )

    def _exclusion_score(self, i: NeuralLanguageDominanceInput) -> float:
        return round(
            (
                i.linguistic_minority_exclusion_rate * 0.40
                + i.multilingual_AI_access_inequality * 0.35
                + i.indigenous_language_AI_gap * 0.25
            ) * 100,
            2,
        )

    def _homogenization_score(self, i: NeuralLanguageDominanceInput) -> float:
        return round(
            (
                i.cognitive_framework_homogenization * 0.40
                + i.language_death_acceleration_index * 0.35
                + i.cultural_concept_untranslatability_loss * 0.25
            ) * 100,
            2,
        )

    def _sovereignty_score(self, i: NeuralLanguageDominanceInput) -> float:
        return round(
            (
                i.cognitive_sovereignty_erosion_index * 0.40
                + i.linguistic_decolonization_resistance * 0.35
                + i.language_as_power_concentration * 0.25
            ) * 100,
            2,
        )

    def _composite(
        self,
        dominance: float,
        exclusion: float,
        homogenization: float,
        sovereignty: float,
    ) -> float:
        return round(
            dominance * 0.30
            + exclusion * 0.25
            + homogenization * 0.25
            + sovereignty * 0.20,
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

    def _pattern(self, i: NeuralLanguageDominanceInput) -> str:
        if i.LLM_monolingual_dominance >= 0.70 and i.language_death_acceleration_index >= 0.65:
            return "linguistic_monoculture_collapse"
        if i.cognitive_framework_homogenization >= 0.70 and i.cognitive_sovereignty_erosion_index >= 0.65:
            return "cognitive_colonization"
        if i.english_AI_training_bias >= 0.70 and i.AI_language_gatekeeping_power >= 0.65:
            return "AI_language_hegemony"
        if i.indigenous_language_AI_gap >= 0.70 and i.linguistic_minority_exclusion_rate >= 0.65:
            return "indigenous_extinction"
        if i.semantic_manipulation_via_language >= 0.70 and i.LLM_cultural_bias_propagation >= 0.65:
            return "semantic_manipulation_crisis"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity                                                            #
    # ------------------------------------------------------------------ #

    def _severity(self, composite: float) -> str:
        if composite >= 60:
            return "hégémonie_linguistique_totale"
        if composite >= 40:
            return "domination_linguistique_avancée"
        if composite >= 20:
            return "homogénéisation_active"
        return "diversité_linguistique_relative"

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: str) -> str:
        if risk == "critical":
            return "souveraineté_linguistique_urgente"
        if risk == "high":
            return "décolonisation_linguistique_IA"
        if risk == "moderate":
            return "renforcement_multilinguisme_IA"
        return "veille_diversité_linguistique"

    # ------------------------------------------------------------------ #
    #  French signal                                                       #
    # ------------------------------------------------------------------ #

    def _signal(self, composite: float) -> str:
        if composite >= 60:
            return "🔴 Hégémonie linguistique totale — colonisation cognitive via IA"
        if composite >= 40:
            return "🟠 Domination linguistique avancée détectée"
        if composite >= 20:
            return "🟡 Homogénéisation linguistique en cours"
        return "🟢 Diversité linguistique relativement préservée"

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def _analyze_one(self, i: NeuralLanguageDominanceInput) -> NeuralLanguageDominanceResult:
        dominance      = self._dominance_score(i)
        exclusion      = self._exclusion_score(i)
        homogenization = self._homogenization_score(i)
        sovereignty    = self._sovereignty_score(i)
        composite      = self._composite(dominance, exclusion, homogenization, sovereignty)
        risk           = self._risk(composite)
        pattern        = self._pattern(i)
        severity       = self._severity(composite)
        action         = self._action(risk)
        signal         = self._signal(composite)

        return NeuralLanguageDominanceResult(
            entity_id=i.entity_id,
            language_domain=i.language_domain,
            region=i.region,
            dominance_score=dominance,
            exclusion_score=exclusion,
            homogenization_score=homogenization,
            sovereignty_score=sovereignty,
            composite_score=composite,
            risk_level=risk,
            language_pattern=pattern,
            severity=severity,
            recommended_action=action,
            signal=signal,
            english_AI_training_bias=i.english_AI_training_bias,
            cognitive_sovereignty_erosion_index=i.cognitive_sovereignty_erosion_index,
        )

    def analyze(self, entities: List[NeuralLanguageDominanceInput]) -> Dict:
        results = [self._analyze_one(i) for i in entities]
        return {"entities": [r.to_dict() for r in results], "summary": self.summary(results)}

    def summary(self, results: List[NeuralLanguageDominanceResult]) -> Dict:
        n = len(results)
        if n == 0:
            return {
                "module_id":                                336,
                "module_name":                              "Neural Language Dominance & Linguistic Intelligence Engine",
                "total_entities":                           0,
                "critical_count":                           0,
                "high_count":                               0,
                "moderate_count":                           0,
                "low_count":                                0,
                "avg_composite":                            0.0,
                "pattern_distribution":                     {},
                "risk_distribution":                        {},
                "severity_distribution":                    {},
                "action_distribution":                      {},
                "avg_estimated_linguistic_dominance_index": 0.0,
            }

        critical_count = sum(1 for r in results if r.risk_level == "critical")
        high_count     = sum(1 for r in results if r.risk_level == "high")
        moderate_count = sum(1 for r in results if r.risk_level == "moderate")
        low_count      = sum(1 for r in results if r.risk_level == "low")

        pattern_distribution: Dict[str, int] = {}
        risk_distribution: Dict[str, int]    = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int]  = {}
        total_composite = 0.0

        for r in results:
            pattern_distribution[r.language_pattern] = pattern_distribution.get(r.language_pattern, 0) + 1
            risk_distribution[r.risk_level]           = risk_distribution.get(r.risk_level, 0) + 1
            severity_distribution[r.severity]         = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action] = action_distribution.get(r.recommended_action, 0) + 1
            total_composite += r.composite_score

        avg_composite = round(total_composite / n, 2)

        return {
            "module_id":                                336,
            "module_name":                              "Neural Language Dominance & Linguistic Intelligence Engine",
            "total_entities":                           n,
            "critical_count":                           critical_count,
            "high_count":                               high_count,
            "moderate_count":                           moderate_count,
            "low_count":                                low_count,
            "avg_composite":                            avg_composite,
            "pattern_distribution":                     pattern_distribution,
            "risk_distribution":                        risk_distribution,
            "severity_distribution":                    severity_distribution,
            "action_distribution":                      action_distribution,
            "avg_estimated_linguistic_dominance_index": round(avg_composite / 100 * 10, 2),
        }
