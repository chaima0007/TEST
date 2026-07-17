"""
Module 343 — Extreme Wealth Concentration & Plutocracy Intelligence Engine
Monitors wealth concentration dynamics, plutocratic capture, social mobility collapse,
and systemic tax impunity across global economic zones.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class WealthConcentrationInput:
    entity_id: str
    economic_zone: str
    region: str
    # 17 float fields (0.0–1.0)
    gini_coefficient_extreme_level: float
    billionaire_wealth_gdp_ratio: float
    top_1_percent_wealth_share: float
    tax_evasion_elite_impunity: float
    offshore_wealth_accumulation_rate: float
    democratic_process_plutocratic_capture: float
    inheritance_wealth_concentration: float
    intergenerational_mobility_collapse: float
    social_elevator_destruction: float
    luxury_asset_inflation_vs_wage_stagnation: float
    elite_network_exclusivity_index: float
    meritocracy_narrative_collapse: float
    plutocratic_media_ownership: float
    tax_haven_system_expansion: float
    wealth_effect_political_power: float
    housing_wealth_extraction_rate: float
    financial_asset_class_monopoly: float


@dataclass
class WealthConcentrationResult:
    entity_id: str
    economic_zone: str
    region: str
    concentration_score: float
    mobility_score: float
    capture_score: float
    systemic_score: float
    composite_score: float
    risk_level: str
    wealth_pattern: str
    severity: str
    recommended_action: str
    signal: str
    top_1_percent_wealth_share: float
    democratic_process_plutocratic_capture: float

    def to_dict(self) -> Dict:
        return {
            "entity_id":                              self.entity_id,
            "economic_zone":                          self.economic_zone,
            "region":                                 self.region,
            "concentration_score":                    self.concentration_score,
            "mobility_score":                         self.mobility_score,
            "capture_score":                          self.capture_score,
            "systemic_score":                         self.systemic_score,
            "composite_score":                        self.composite_score,
            "risk_level":                             self.risk_level,
            "wealth_pattern":                         self.wealth_pattern,
            "severity":                               self.severity,
            "recommended_action":                     self.recommended_action,
            "signal":                                 self.signal,
            "top_1_percent_wealth_share":             self.top_1_percent_wealth_share,
            "democratic_process_plutocratic_capture": self.democratic_process_plutocratic_capture,
        }


class WealthConcentrationEngine:
    """
    Module 343 — Extreme Wealth Concentration & Plutocracy Intelligence Engine
    Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
    """

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100)                                                  #
    # ------------------------------------------------------------------ #

    def _concentration_score(self, i: WealthConcentrationInput) -> float:
        return round(
            (
                i.top_1_percent_wealth_share * 0.4
                + i.billionaire_wealth_gdp_ratio * 0.35
                + i.offshore_wealth_accumulation_rate * 0.25
            ) * 100,
            2,
        )

    def _mobility_score(self, i: WealthConcentrationInput) -> float:
        return round(
            (
                i.intergenerational_mobility_collapse * 0.4
                + i.social_elevator_destruction * 0.35
                + i.meritocracy_narrative_collapse * 0.25
            ) * 100,
            2,
        )

    def _capture_score(self, i: WealthConcentrationInput) -> float:
        return round(
            (
                i.democratic_process_plutocratic_capture * 0.4
                + i.plutocratic_media_ownership * 0.35
                + i.wealth_effect_political_power * 0.25
            ) * 100,
            2,
        )

    def _systemic_score(self, i: WealthConcentrationInput) -> float:
        return round(
            (
                i.tax_evasion_elite_impunity * 0.4
                + i.tax_haven_system_expansion * 0.35
                + i.inheritance_wealth_concentration * 0.25
            ) * 100,
            2,
        )

    def _composite(
        self,
        concentration: float,
        mobility: float,
        capture: float,
        systemic: float,
    ) -> float:
        return round(
            concentration * 0.30
            + mobility * 0.25
            + capture * 0.25
            + systemic * 0.20,
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

    def _pattern(self, i: WealthConcentrationInput) -> str:
        if i.democratic_process_plutocratic_capture >= 0.70 and i.wealth_effect_political_power >= 0.65:
            return "plutocracy_lock_in"
        if i.top_1_percent_wealth_share >= 0.70 and i.billionaire_wealth_gdp_ratio >= 0.65:
            return "wealth_singularity"
        if i.intergenerational_mobility_collapse >= 0.70 and i.social_elevator_destruction >= 0.65:
            return "social_immobility_trap"
        if i.tax_evasion_elite_impunity >= 0.70 and i.tax_haven_system_expansion >= 0.65:
            return "tax_impunity_regime"
        if i.plutocratic_media_ownership >= 0.70 and i.meritocracy_narrative_collapse >= 0.65:
            return "media_plutocracy"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity (French)                                                   #
    # ------------------------------------------------------------------ #

    def _severity(self, risk: str) -> str:
        if risk == "critical":
            return "ploutocratie_systémique_avancée"
        if risk == "high":
            return "concentration_richesse_dangereuse"
        if risk == "moderate":
            return "inégalité_structurelle_active"
        return "inégalité_gérée"

    # ------------------------------------------------------------------ #
    #  Action selection (French)                                           #
    # ------------------------------------------------------------------ #

    def _action(self, risk: str) -> str:
        if risk == "critical":
            return "réforme_fiscale_urgente_ploutocratie"
        if risk == "high":
            return "démantèlement_capture_oligarchique"
        if risk == "moderate":
            return "renforcement_redistribution_systémique"
        return "veille_concentration_richesse"

    # ------------------------------------------------------------------ #
    #  Signal (French)                                                     #
    # ------------------------------------------------------------------ #

    def _signal(self, risk: str) -> str:
        if risk == "critical":
            return "🔴 Ploutocratie systémique — démocratie économique compromise"
        if risk == "high":
            return "🟠 Concentration richesse dangereuse détectée"
        if risk == "moderate":
            return "🟡 Inégalité structurelle active — surveillance requise"
        return "🟢 Inégalité économique relativement gérée"

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def _analyze_one(self, i: WealthConcentrationInput) -> WealthConcentrationResult:
        concentration = self._concentration_score(i)
        mobility      = self._mobility_score(i)
        capture       = self._capture_score(i)
        systemic      = self._systemic_score(i)
        composite     = self._composite(concentration, mobility, capture, systemic)
        risk          = self._risk(composite)
        pattern       = self._pattern(i)
        severity      = self._severity(risk)
        action        = self._action(risk)
        signal        = self._signal(risk)

        return WealthConcentrationResult(
            entity_id=i.entity_id,
            economic_zone=i.economic_zone,
            region=i.region,
            concentration_score=concentration,
            mobility_score=mobility,
            capture_score=capture,
            systemic_score=systemic,
            composite_score=composite,
            risk_level=risk,
            wealth_pattern=pattern,
            severity=severity,
            recommended_action=action,
            signal=signal,
            top_1_percent_wealth_share=i.top_1_percent_wealth_share,
            democratic_process_plutocratic_capture=i.democratic_process_plutocratic_capture,
        )

    def analyze(self, entities: List[WealthConcentrationInput]) -> List[Dict]:
        return [self._analyze_one(i).to_dict() for i in entities]

    def summary(self, results: List[Dict]) -> Dict:
        n = len(results)

        critical_count  = sum(1 for r in results if r["risk_level"] == "critical")
        high_count      = sum(1 for r in results if r["risk_level"] == "high")
        moderate_count  = sum(1 for r in results if r["risk_level"] == "moderate")
        low_count       = sum(1 for r in results if r["risk_level"] == "low")

        avg_composite = round(sum(r["composite_score"] for r in results) / n, 2) if n else 0.0

        pattern_distribution: Dict[str, int] = {}
        risk_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        for r in results:
            pat = r["wealth_pattern"]
            risk = r["risk_level"]
            sev = r["severity"]
            act = r["recommended_action"]
            pattern_distribution[pat]   = pattern_distribution.get(pat, 0) + 1
            risk_distribution[risk]     = risk_distribution.get(risk, 0) + 1
            severity_distribution[sev]  = severity_distribution.get(sev, 0) + 1
            action_distribution[act]    = action_distribution.get(act, 0) + 1

        return {
            "module_id":                    343,
            "module_name":                  "Extreme Wealth Concentration & Plutocracy Intelligence Engine",
            "total_entities":               n,
            "critical_count":               critical_count,
            "high_count":                   high_count,
            "moderate_count":               moderate_count,
            "low_count":                    low_count,
            "avg_composite":                avg_composite,
            "pattern_distribution":         pattern_distribution,
            "risk_distribution":            risk_distribution,
            "severity_distribution":        severity_distribution,
            "action_distribution":          action_distribution,
            "avg_estimated_plutocracy_index": round(avg_composite / 100 * 10, 2),
        }
