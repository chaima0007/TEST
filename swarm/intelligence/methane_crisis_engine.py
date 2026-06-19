"""
Module 345 — Methane Crisis & Arctic Methane Bomb Intelligence Engine
Monitors arctic permafrost methane release, clathrate destabilization,
agricultural emissions, feedback loops, and policy response gaps.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MethaneCrisisInput:
    entity_id: str
    methane_source: str
    region: str
    # 17 float fields (0.0–1.0)
    arctic_permafrost_methane_release_rate: float       # 0-1
    submarine_methane_hydrate_destabilization: float    # 0-1
    wetland_methane_emission_acceleration: float        # 0-1
    agricultural_methane_uncontrolled_growth: float     # 0-1
    fossil_fuel_methane_fugitive_emissions: float       # 0-1
    urban_landfill_methane_saturation: float            # 0-1
    atmospheric_methane_concentration_index: float      # 0-1
    methane_warming_feedback_loop_intensity: float      # 0-1
    permafrost_thaw_acceleration_rate: float            # 0-1
    clathrate_gun_hypothesis_proximity: float           # 0-1
    methane_monitoring_coverage_gap: float              # 0-1
    methane_capture_technology_deployment: float        # 0-1
    climate_policy_methane_neglect: float               # 0-1
    arctic_amplification_rate: float                    # 0-1
    methane_vs_CO2_substitution_risk: float             # 0-1
    deep_sea_methane_seep_activation: float             # 0-1
    tundra_fire_methane_cascade: float                  # 0-1


@dataclass
class MethaneCrisisResult:
    entity_id: str
    methane_source: str
    region: str
    arctic_score: float
    emission_score: float
    feedback_score: float
    response_score: float
    composite_score: float
    risk_level: str
    methane_pattern: str
    severity: str
    recommended_action: str
    signal: str
    arctic_permafrost_methane_release_rate: float
    methane_warming_feedback_loop_intensity: float

    def to_dict(self) -> Dict:
        return {
            "entity_id":                               self.entity_id,
            "methane_source":                          self.methane_source,
            "region":                                  self.region,
            "arctic_score":                            self.arctic_score,
            "emission_score":                          self.emission_score,
            "feedback_score":                          self.feedback_score,
            "response_score":                          self.response_score,
            "composite_score":                         self.composite_score,
            "risk_level":                              self.risk_level,
            "methane_pattern":                         self.methane_pattern,
            "severity":                                self.severity,
            "recommended_action":                      self.recommended_action,
            "signal":                                  self.signal,
            "arctic_permafrost_methane_release_rate":  self.arctic_permafrost_methane_release_rate,
            "methane_warming_feedback_loop_intensity": self.methane_warming_feedback_loop_intensity,
        }


class MethaneCrisisEngine:
    """
    Module 345 — Methane Crisis & Arctic Methane Bomb Intelligence Engine
    Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
    """

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100)                                                  #
    # ------------------------------------------------------------------ #

    def _arctic_score(self, i: MethaneCrisisInput) -> float:
        return round(
            (
                i.arctic_permafrost_methane_release_rate * 0.4
                + i.permafrost_thaw_acceleration_rate * 0.35
                + i.arctic_amplification_rate * 0.25
            ) * 100,
            2,
        )

    def _emission_score(self, i: MethaneCrisisInput) -> float:
        return round(
            (
                i.atmospheric_methane_concentration_index * 0.4
                + i.agricultural_methane_uncontrolled_growth * 0.35
                + i.fossil_fuel_methane_fugitive_emissions * 0.25
            ) * 100,
            2,
        )

    def _feedback_score(self, i: MethaneCrisisInput) -> float:
        return round(
            (
                i.methane_warming_feedback_loop_intensity * 0.4
                + i.clathrate_gun_hypothesis_proximity * 0.35
                + i.tundra_fire_methane_cascade * 0.25
            ) * 100,
            2,
        )

    def _response_score(self, i: MethaneCrisisInput) -> float:
        return round(
            (
                i.climate_policy_methane_neglect * 0.4
                + i.methane_monitoring_coverage_gap * 0.35
                + (1 - i.methane_capture_technology_deployment) * 0.25
            ) * 100,
            2,
        )

    def _composite(
        self,
        arctic: float,
        emission: float,
        feedback: float,
        response: float,
    ) -> float:
        return round(
            arctic * 0.30
            + emission * 0.25
            + feedback * 0.25
            + response * 0.20,
            2,
        )

    # ------------------------------------------------------------------ #
    #  Risk classification                                                 #
    # ------------------------------------------------------------------ #

    def _risk_level(self, composite: float) -> str:
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

    def _methane_pattern(self, i: MethaneCrisisInput) -> str:
        if (i.arctic_permafrost_methane_release_rate >= 0.70
                and i.clathrate_gun_hypothesis_proximity >= 0.65):
            return "permafrost_methane_bomb"
        if (i.submarine_methane_hydrate_destabilization >= 0.70
                and i.deep_sea_methane_seep_activation >= 0.65):
            return "clathrate_destabilization"
        if (i.agricultural_methane_uncontrolled_growth >= 0.70
                and i.climate_policy_methane_neglect >= 0.65):
            return "agricultural_methane_crisis"
        if (i.methane_warming_feedback_loop_intensity >= 0.70
                and i.arctic_amplification_rate >= 0.65):
            return "arctic_feedback_cascade"
        if (i.tundra_fire_methane_cascade >= 0.70
                and i.permafrost_thaw_acceleration_rate >= 0.65):
            return "tundra_methane_inferno"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity                                                            #
    # ------------------------------------------------------------------ #

    def _severity(self, composite: float) -> str:
        if composite >= 60:
            return "bombe_méthane_imminente"
        if composite >= 40:
            return "crise_méthane_accélérée"
        if composite >= 20:
            return "accumulation_méthane_critique"
        return "émissions_méthane_surveillées"

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _recommended_action(self, risk: str) -> str:
        if risk == "critical":
            return "intervention_méthane_urgence_planétaire"
        if risk == "high":
            return "réduction_méthane_accélérée"
        if risk == "moderate":
            return "surveillance_méthane_renforcée"
        return "monitoring_méthane_continu"

    # ------------------------------------------------------------------ #
    #  Signal                                                              #
    # ------------------------------------------------------------------ #

    def _signal(self, risk: str) -> str:
        if risk == "critical":
            return "🔴 Bombe méthane imminente — emballement climatique irréversible"
        if risk == "high":
            return "🟠 Crise méthane accélérée détectée"
        if risk == "moderate":
            return "🟡 Accumulation méthane critique — vigilance"
        return "🟢 Émissions méthane sous surveillance"

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def _analyze_one(self, i: MethaneCrisisInput) -> MethaneCrisisResult:
        arctic    = self._arctic_score(i)
        emission  = self._emission_score(i)
        feedback  = self._feedback_score(i)
        response  = self._response_score(i)
        composite = self._composite(arctic, emission, feedback, response)
        risk      = self._risk_level(composite)
        pattern   = self._methane_pattern(i)
        severity  = self._severity(composite)
        action    = self._recommended_action(risk)
        signal    = self._signal(risk)

        return MethaneCrisisResult(
            entity_id=i.entity_id,
            methane_source=i.methane_source,
            region=i.region,
            arctic_score=arctic,
            emission_score=emission,
            feedback_score=feedback,
            response_score=response,
            composite_score=composite,
            risk_level=risk,
            methane_pattern=pattern,
            severity=severity,
            recommended_action=action,
            signal=signal,
            arctic_permafrost_methane_release_rate=i.arctic_permafrost_methane_release_rate,
            methane_warming_feedback_loop_intensity=i.methane_warming_feedback_loop_intensity,
        )

    def analyze(self, entities: List[MethaneCrisisInput]) -> List[MethaneCrisisResult]:
        return [self._analyze_one(i) for i in entities]

    @staticmethod
    def summary(results: List[Dict]) -> Dict:
        """
        Takes a list of to_dict() outputs and returns exactly 13 keys.
        """
        n = len(results)
        critical_count = sum(1 for r in results if r["risk_level"] == "critical")
        high_count     = sum(1 for r in results if r["risk_level"] == "high")
        moderate_count = sum(1 for r in results if r["risk_level"] == "moderate")
        low_count      = sum(1 for r in results if r["risk_level"] == "low")

        avg_composite = round(sum(r["composite_score"] for r in results) / n, 2) if n else 0.0

        pattern_distribution:  Dict[str, int] = {}
        risk_distribution:     Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution:   Dict[str, int] = {}

        for r in results:
            pat = r["methane_pattern"]
            pattern_distribution[pat] = pattern_distribution.get(pat, 0) + 1

            rl = r["risk_level"]
            risk_distribution[rl] = risk_distribution.get(rl, 0) + 1

            sev = r["severity"]
            severity_distribution[sev] = severity_distribution.get(sev, 0) + 1

            act = r["recommended_action"]
            action_distribution[act] = action_distribution.get(act, 0) + 1

        return {
            "module_id":                        345,
            "module_name":                      "Methane Crisis & Arctic Methane Bomb Intelligence Engine",
            "total_entities":                   n,
            "critical_count":                   critical_count,
            "high_count":                       high_count,
            "moderate_count":                   moderate_count,
            "low_count":                        low_count,
            "avg_composite":                    avg_composite,
            "pattern_distribution":             pattern_distribution,
            "risk_distribution":                risk_distribution,
            "severity_distribution":            severity_distribution,
            "action_distribution":              action_distribution,
            "avg_estimated_methane_risk_index": round(avg_composite / 100 * 10, 2),
        }
