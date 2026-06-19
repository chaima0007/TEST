"""
Module 386 — Crypto Exchange & Digital Asset Regulation Intelligence Engine
Monitors exchange collapse risk, market manipulation, regulatory arbitrage,
custody failures, stablecoin depegging, and crypto oligopoly formation.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class CryptoRegulationInput:
    entity_id: str
    exchange_type: str
    region: str
    # 17 float fields (0.0–1.0)
    exchange_collapse_risk: float
    fractional_reserve_crypto: float
    regulatory_arbitrage_intensity: float
    custody_failure_risk: float
    market_manipulation_scale: float
    insider_trading_prevalence: float
    stablecoin_depegging_risk: float
    CBDC_competitive_threat: float
    AML_compliance_failure: float
    exchange_concentration_risk: float
    retail_investor_harm: float
    geopolitical_ban_risk: float
    proof_of_reserve_failure: float
    contagion_from_collapse: float
    regulatory_fragmentation_global: float
    consumer_protection_gap: float
    crypto_oligopoly_formation: float


@dataclass
class CryptoRegulationResult:
    entity_id: str
    exchange_type: str
    region: str
    risk_level: str
    crypto_pattern: str
    severity: str
    recommended_action: str
    collapse_score: float
    manipulation_score: float
    regulatory_score: float
    concentration_score: float
    composite_score: float
    is_crypto_systemic: bool
    requires_regulatory_intervention: bool
    signal: str
    exchange_collapse_risk: float
    crypto_oligopoly_formation: float

    def to_dict(self) -> Dict:
        return {
            "entity_id":                          self.entity_id,
            "exchange_type":                      self.exchange_type,
            "region":                             self.region,
            "collapse_score":                     self.collapse_score,
            "manipulation_score":                 self.manipulation_score,
            "regulatory_score":                   self.regulatory_score,
            "concentration_score":                self.concentration_score,
            "composite_score":                    self.composite_score,
            "risk_level":                         self.risk_level,
            "crypto_pattern":                     self.crypto_pattern,
            "severity":                           self.severity,
            "recommended_action":                 self.recommended_action,
            "signal":                             self.signal,
            "exchange_collapse_risk":             self.exchange_collapse_risk,
            "crypto_oligopoly_formation":         self.crypto_oligopoly_formation,
        }


class CryptoRegulationEngine:
    """
    Module 386 — Crypto Exchange & Digital Asset Regulation Intelligence Engine
    Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
    """

    def __init__(self) -> None:
        self._results: List[CryptoRegulationResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100)                                                  #
    # ------------------------------------------------------------------ #

    def _collapse_score(self, i: CryptoRegulationInput) -> float:
        return round(
            (
                i.exchange_collapse_risk * 0.40
                + i.fractional_reserve_crypto * 0.35
                + i.custody_failure_risk * 0.25
            ) * 100,
            2,
        )

    def _manipulation_score(self, i: CryptoRegulationInput) -> float:
        return round(
            (
                i.market_manipulation_scale * 0.40
                + i.insider_trading_prevalence * 0.35
                + i.retail_investor_harm * 0.25
            ) * 100,
            2,
        )

    def _regulatory_score(self, i: CryptoRegulationInput) -> float:
        return round(
            (
                i.AML_compliance_failure * 0.40
                + i.regulatory_arbitrage_intensity * 0.35
                + i.regulatory_fragmentation_global * 0.25
            ) * 100,
            2,
        )

    def _concentration_score(self, i: CryptoRegulationInput) -> float:
        return round(
            (
                i.exchange_concentration_risk * 0.40
                + i.crypto_oligopoly_formation * 0.35
                + i.consumer_protection_gap * 0.25
            ) * 100,
            2,
        )

    def _composite(
        self,
        collapse: float,
        manipulation: float,
        regulatory: float,
        concentration: float,
    ) -> float:
        return round(
            collapse * 0.30
            + manipulation * 0.25
            + regulatory * 0.25
            + concentration * 0.20,
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

    def _pattern(self, i: CryptoRegulationInput) -> str:
        if i.exchange_collapse_risk > 0.85 and i.contagion_from_collapse > 0.80:
            return "exchange_collapse_cascade"
        if i.fractional_reserve_crypto > 0.85 and i.proof_of_reserve_failure > 0.80:
            return "fractional_reserve_crisis"
        if i.market_manipulation_scale > 0.85 and i.insider_trading_prevalence > 0.80:
            return "market_manipulation_empire"
        if i.geopolitical_ban_risk > 0.80 and i.regulatory_fragmentation_global > 0.75:
            return "regulatory_ban_extermination"
        if i.crypto_oligopoly_formation > 0.80 and i.exchange_concentration_risk > 0.75:
            return "crypto_oligopoly_capture"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity                                                            #
    # ------------------------------------------------------------------ #

    def _severity(self, risk: str) -> str:
        if risk == "critical":
            return "effondrement_crypto_systémique"
        if risk == "high":
            return "crise_réglementaire_crypto_majeure"
        if risk == "moderate":
            return "vulnérabilité_structurelle_crypto"
        return "risque_crypto_contenu"

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: str) -> str:
        if risk == "critical":
            return "intervention_réglementaire_urgente_crypto"
        if risk == "high":
            return "supervision_renforcée_exchange_crypto"
        if risk == "moderate":
            return "audit_conformité_actifs_numériques"
        return "veille_réglementaire_crypto_continue"

    # ------------------------------------------------------------------ #
    #  French signal                                                       #
    # ------------------------------------------------------------------ #

    def _signal(self, risk: str) -> str:
        signals = {
            "critical": "🔴 Effondrement crypto systémique — risque contagion majeur",
            "high":     "🟠 Crise réglementaire crypto majeure détectée",
            "moderate": "🟡 Vulnérabilité structurelle crypto active",
            "low":      "🟢 Risque crypto contenu et surveillé",
        }
        return signals.get(risk, "Statut inconnu")

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def _analyze_one(self, i: CryptoRegulationInput) -> CryptoRegulationResult:
        collapse      = self._collapse_score(i)
        manipulation  = self._manipulation_score(i)
        regulatory    = self._regulatory_score(i)
        concentration = self._concentration_score(i)
        composite     = self._composite(collapse, manipulation, regulatory, concentration)
        risk          = self._risk(composite)
        pattern       = self._pattern(i)
        severity      = self._severity(risk)
        action        = self._action(risk)
        signal        = self._signal(risk)

        return CryptoRegulationResult(
            entity_id=i.entity_id,
            exchange_type=i.exchange_type,
            region=i.region,
            risk_level=risk,
            crypto_pattern=pattern,
            severity=severity,
            recommended_action=action,
            collapse_score=collapse,
            manipulation_score=manipulation,
            regulatory_score=regulatory,
            concentration_score=concentration,
            composite_score=composite,
            is_crypto_systemic=composite >= 60,
            requires_regulatory_intervention=composite >= 40,
            signal=signal,
            exchange_collapse_risk=i.exchange_collapse_risk,
            crypto_oligopoly_formation=i.crypto_oligopoly_formation,
        )

    def analyze(self, entities: List[CryptoRegulationInput]) -> List[CryptoRegulationResult]:
        results = [self._analyze_one(i) for i in entities]
        self._results.extend(results)
        return results

    def summary(self) -> Dict:
        if not self._results:
            return {
                "module_id":                              386,
                "module_name":                            "Crypto Exchange & Digital Asset Regulation Intelligence Engine",
                "total":                                  0,
                "critical":                               0,
                "high":                                   0,
                "moderate":                               0,
                "low":                                    0,
                "avg_composite":                          0.0,
                "distributions":                          {
                    "pattern":  {},
                    "risk":     {},
                    "severity": {},
                    "action":   {},
                },
                "avg_estimated_crypto_regulatory_index":  0.0,
                "avg_collapse_score":                     0.0,
                "avg_manipulation_score":                 0.0,
                "avg_regulatory_score":                   0.0,
            }

        n              = len(self._results)
        critical       = sum(1 for r in self._results if r.risk_level == "critical")
        high           = sum(1 for r in self._results if r.risk_level == "high")
        moderate       = sum(1 for r in self._results if r.risk_level == "moderate")
        low            = sum(1 for r in self._results if r.risk_level == "low")
        avg_composite  = sum(r.composite_score    for r in self._results) / n
        avg_collapse   = sum(r.collapse_score     for r in self._results) / n
        avg_manip      = sum(r.manipulation_score for r in self._results) / n
        avg_reg        = sum(r.regulatory_score   for r in self._results) / n

        pattern_distribution:  Dict[str, int] = {}
        risk_distribution:     Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution:   Dict[str, int] = {}

        for r in self._results:
            pattern_distribution[r.crypto_pattern]    = pattern_distribution.get(r.crypto_pattern, 0) + 1
            risk_distribution[r.risk_level]           = risk_distribution.get(r.risk_level, 0) + 1
            severity_distribution[r.severity]         = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action] = action_distribution.get(r.recommended_action, 0) + 1

        return {
            "module_id":   386,
            "module_name": "Crypto Exchange & Digital Asset Regulation Intelligence Engine",
            "total":       n,
            "critical":    critical,
            "high":        high,
            "moderate":    moderate,
            "low":         low,
            "avg_composite": round(avg_composite, 2),
            "distributions": {
                "pattern":   pattern_distribution,
                "risk":      risk_distribution,
                "severity":  severity_distribution,
                "action":    action_distribution,
            },
            "avg_estimated_crypto_regulatory_index": round(avg_composite / 100 * 10, 2),
            "avg_collapse_score":                    round(avg_collapse, 2),
            "avg_manipulation_score":                round(avg_manip, 2),
            "avg_regulatory_score":                  round(avg_reg, 2),
        }
