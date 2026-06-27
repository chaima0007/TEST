"""
Module 369 — Carbon Credit Market & Climate Finance Fraud Intelligence Engine
Caelum Partners Swarm Intelligence Platform
"""

from dataclasses import dataclass
from typing import Optional
import statistics


@dataclass
class CarbonCreditInput:
    entity_id: str
    market_type: str
    region: str
    # 17 float fields 0-1
    fraud_prevalence: float
    additionality_failure: float
    permanence_risk: float
    double_counting_rate: float
    verification_opacity: float
    greenwashing_integration: float
    REDD_collapse_risk: float
    voluntary_market_manipulation: float
    corporate_offset_abuse: float
    regulatory_arbitrage: float
    biodiversity_credit_fraud: float
    social_impact_fabrication: float
    methodology_gaming: float
    registry_manipulation: float
    carbon_washing_intensity: float
    market_concentration: float
    standard_capture: float


class CarbonCreditResult:
    """Wrapper for a single analysis result with a to_dict() method."""

    def __init__(self, data: dict):
        self._data = data

    def to_dict(self) -> dict:
        """Returns exactly 15 keys."""
        return {
            "entity_id":                self._data["entity_id"],
            "market_type":              self._data["market_type"],
            "region":                   self._data["region"],
            "fraud_score":              self._data["fraud_score"],
            "greenwash_score":          self._data["greenwash_score"],
            "systemic_score":           self._data["systemic_score"],
            "manipulation_score":       self._data["manipulation_score"],
            "composite_score":          self._data["composite_score"],
            "risk_level":               self._data["risk_level"],
            "carbon_credit_pattern":    self._data["carbon_credit_pattern"],
            "severity":                 self._data["severity"],
            "recommended_action":       self._data["recommended_action"],
            "signal":                   self._data["signal"],
            "fraud_prevalence":         self._data["fraud_prevalence"],
            "greenwashing_integration": self._data["greenwashing_integration"],
        }


class CarbonCreditEngine:
    MODULE_ID = 369
    MODULE_NAME = "Carbon Credit Market & Climate Finance Fraud Intelligence Engine"

    def __init__(self):
        self.results: list[dict] = []

    def _compute_scores(self, inp: CarbonCreditInput) -> dict:
        fraud_score = (
            inp.fraud_prevalence * 0.40
            + inp.double_counting_rate * 0.35
            + inp.additionality_failure * 0.25
        ) * 100

        greenwash_score = (
            inp.greenwashing_integration * 0.40
            + inp.corporate_offset_abuse * 0.35
            + inp.carbon_washing_intensity * 0.25
        ) * 100

        systemic_score = (
            inp.REDD_collapse_risk * 0.40
            + inp.permanence_risk * 0.35
            + inp.biodiversity_credit_fraud * 0.25
        ) * 100

        manipulation_score = (
            inp.voluntary_market_manipulation * 0.40
            + inp.market_concentration * 0.35
            + inp.registry_manipulation * 0.25
        ) * 100

        composite = (
            fraud_score * 0.30
            + greenwash_score * 0.25
            + systemic_score * 0.25
            + manipulation_score * 0.20
        )

        return {
            "fraud_score":        round(fraud_score, 2),
            "greenwash_score":    round(greenwash_score, 2),
            "systemic_score":     round(systemic_score, 2),
            "manipulation_score": round(manipulation_score, 2),
            "composite_score":    round(composite, 2),
        }

    def _detect_pattern(self, inp: CarbonCreditInput) -> str:
        if inp.fraud_prevalence > 0.85 and inp.double_counting_rate > 0.80:
            return "systematic_carbon_fraud"
        if inp.REDD_collapse_risk > 0.85 and inp.additionality_failure > 0.80:
            return "REDD_ecosystem_collapse"
        if inp.greenwashing_integration > 0.85 and inp.corporate_offset_abuse > 0.80:
            return "corporate_greenwashing_empire"
        if inp.voluntary_market_manipulation > 0.80 and inp.market_concentration > 0.75:
            return "market_manipulation_capture"
        if inp.standard_capture > 0.80 and inp.registry_manipulation > 0.75:
            return "standard_regulatory_capture"
        return "none"

    def _classify_risk(self, composite: float) -> str:
        if composite >= 60:
            return "critical"
        if composite >= 40:
            return "high"
        if composite >= 20:
            return "moderate"
        return "low"

    def _get_severity(self, risk_level: str) -> str:
        mapping = {
            "critical": "crise_fraude_carbone_systémique",
            "high":     "risque_manipulation_marché_carbone_majeur",
            "moderate": "fragilité_intégrité_crédit_carbone_structurelle",
            "low":      "marché_carbone_sous_surveillance",
        }
        return mapping[risk_level]

    def _get_action(self, risk_level: str) -> str:
        mapping = {
            "critical": "intervention_fraude_carbone_urgente",
            "high":     "audit_marché_carbone_accéléré",
            "moderate": "renforcement_vérification_crédit_carbone",
            "low":      "veille_marché_carbone_continue",
        }
        return mapping[risk_level]

    def _get_signal(self, risk_level: str) -> str:
        mapping = {
            "critical": "🔴 Crise fraude carbone systémique — intégrité marchés climatiques compromise",
            "high":     "🟠 Risque manipulation marché carbone majeur détecté",
            "moderate": "🟡 Fragilité intégrité crédit carbone structurelle active",
            "low":      "🟢 Marché carbone sous surveillance",
        }
        return mapping[risk_level]

    def analyze(self, inp: CarbonCreditInput) -> dict:
        scores = self._compute_scores(inp)
        risk_level = self._classify_risk(scores["composite_score"])
        pattern = self._detect_pattern(inp)
        severity = self._get_severity(risk_level)
        action = self._get_action(risk_level)
        signal = self._get_signal(risk_level)

        result = {
            "entity_id":                inp.entity_id,
            "market_type":              inp.market_type,
            "region":                   inp.region,
            "fraud_score":              scores["fraud_score"],
            "greenwash_score":          scores["greenwash_score"],
            "systemic_score":           scores["systemic_score"],
            "manipulation_score":       scores["manipulation_score"],
            "composite_score":          scores["composite_score"],
            "risk_level":               risk_level,
            "carbon_credit_pattern":    pattern,
            "severity":                 severity,
            "recommended_action":       action,
            "signal":                   signal,
            "fraud_prevalence":         inp.fraud_prevalence,
            "greenwashing_integration": inp.greenwashing_integration,
        }
        self.results.append(result)
        return result

    def to_dict(self, inp: CarbonCreditInput) -> dict:
        """Returns exactly 15 keys."""
        scores = self._compute_scores(inp)
        risk_level = self._classify_risk(scores["composite_score"])
        pattern = self._detect_pattern(inp)
        severity = self._get_severity(risk_level)
        action = self._get_action(risk_level)
        signal = self._get_signal(risk_level)

        return {
            "entity_id":                inp.entity_id,
            "market_type":              inp.market_type,
            "region":                   inp.region,
            "fraud_score":              scores["fraud_score"],
            "greenwash_score":          scores["greenwash_score"],
            "systemic_score":           scores["systemic_score"],
            "manipulation_score":       scores["manipulation_score"],
            "composite_score":          scores["composite_score"],
            "risk_level":               risk_level,
            "carbon_credit_pattern":    pattern,
            "severity":                 severity,
            "recommended_action":       action,
            "signal":                   signal,
            "fraud_prevalence":         inp.fraud_prevalence,
            "greenwashing_integration": inp.greenwashing_integration,
        }

    def summary(self) -> dict:
        """Returns exactly 13 keys."""
        if not self.results:
            return {
                "module_id":                        self.MODULE_ID,
                "module_name":                      self.MODULE_NAME,
                "total":                            0,
                "critical":                         0,
                "high":                             0,
                "moderate":                         0,
                "low":                              0,
                "avg_composite":                    0.0,
                "distributions":                    {},
                "avg_estimated_carbon_fraud_index": 0.0,
                "risk_distribution":                {},
                "severity_distribution":            {},
                "action_distribution":              {},
            }

        total = len(self.results)
        critical = sum(1 for r in self.results if r["risk_level"] == "critical")
        high     = sum(1 for r in self.results if r["risk_level"] == "high")
        moderate = sum(1 for r in self.results if r["risk_level"] == "moderate")
        low      = sum(1 for r in self.results if r["risk_level"] == "low")
        avg_composite = round(statistics.mean(r["composite_score"] for r in self.results), 2)

        distributions: dict[str, int] = {}
        risk_distribution: dict[str, int] = {}
        severity_distribution: dict[str, int] = {}
        action_distribution: dict[str, int] = {}

        for r in self.results:
            p = r["carbon_credit_pattern"]
            distributions[p] = distributions.get(p, 0) + 1
            rl = r["risk_level"]
            risk_distribution[rl] = risk_distribution.get(rl, 0) + 1
            s = r["severity"]
            severity_distribution[s] = severity_distribution.get(s, 0) + 1
            a = r["recommended_action"]
            action_distribution[a] = action_distribution.get(a, 0) + 1

        avg_estimated_carbon_fraud_index = round(avg_composite / 100 * 10, 2)

        return {
            "module_id":                        self.MODULE_ID,
            "module_name":                      self.MODULE_NAME,
            "total":                            total,
            "critical":                         critical,
            "high":                             high,
            "moderate":                         moderate,
            "low":                              low,
            "avg_composite":                    avg_composite,
            "distributions":                    distributions,
            "avg_estimated_carbon_fraud_index": avg_estimated_carbon_fraud_index,
            "risk_distribution":                risk_distribution,
            "severity_distribution":            severity_distribution,
            "action_distribution":              action_distribution,
        }
