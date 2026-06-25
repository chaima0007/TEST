"""
Module 352 — Anti-Money Laundering & Financial Crime Intelligence Engine
Monitors money laundering networks, sanction evasion, kleptocracy systems,
crypto crime integration, and professional complicity across financial sectors.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class FinancialCrimeInput:
    entity_id: str
    financial_sector: str
    region: str
    # 17 float fields (0.0–1.0)
    money_laundering_volume_index: float
    correspondent_banking_vulnerability: float
    shell_company_opacity_level: float
    crypto_crime_laundering_integration: float
    trade_based_money_laundering_rate: float
    real_estate_laundering_density: float
    beneficial_ownership_opacity: float
    AML_enforcement_weakness_index: float
    financial_intelligence_gap: float
    kleptocracy_asset_repatriation_failure: float
    state_sponsored_financial_crime_level: float
    offshore_secrecy_exploitation: float
    sanction_evasion_sophistication: float
    narco_financial_integration: float
    terrorist_financing_detection_gap: float
    professional_enabler_complicity_rate: float
    regulatory_arbitrage_financial_crime: float


@dataclass
class FinancialCrimeResult:
    entity_id: str
    financial_sector: str
    region: str
    risk_level: str
    crime_pattern: str
    severity: str
    recommended_action: str
    laundering_score: float
    evasion_score: float
    opacity_score: float
    governance_score: float
    composite_score: float
    is_financial_crime_systemic: bool
    requires_AML_intervention: bool
    signal: str
    money_laundering_volume_index: float
    sanction_evasion_sophistication: float

    def to_dict(self) -> Dict:
        return {
            "entity_id":                        self.entity_id,
            "financial_sector":                 self.financial_sector,
            "region":                           self.region,
            "laundering_score":                 self.laundering_score,
            "evasion_score":                    self.evasion_score,
            "opacity_score":                    self.opacity_score,
            "governance_score":                 self.governance_score,
            "composite_score":                  self.composite_score,
            "risk_level":                       self.risk_level,
            "crime_pattern":                    self.crime_pattern,
            "severity":                         self.severity,
            "recommended_action":               self.recommended_action,
            "signal":                           self.signal,
            "money_laundering_volume_index":    self.money_laundering_volume_index,
            "sanction_evasion_sophistication":  self.sanction_evasion_sophistication,
        }


class FinancialCrimeEngine:
    """
    Module 352 — Anti-Money Laundering & Financial Crime Intelligence Engine
    Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
    """

    def __init__(self) -> None:
        self._results: List[FinancialCrimeResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100)                                                  #
    # ------------------------------------------------------------------ #

    def _laundering_score(self, i: FinancialCrimeInput) -> float:
        return round(
            (
                i.money_laundering_volume_index * 0.4
                + i.shell_company_opacity_level * 0.35
                + i.real_estate_laundering_density * 0.25
            ) * 100,
            2,
        )

    def _evasion_score(self, i: FinancialCrimeInput) -> float:
        return round(
            (
                i.sanction_evasion_sophistication * 0.4
                + i.offshore_secrecy_exploitation * 0.35
                + i.regulatory_arbitrage_financial_crime * 0.25
            ) * 100,
            2,
        )

    def _opacity_score(self, i: FinancialCrimeInput) -> float:
        return round(
            (
                i.beneficial_ownership_opacity * 0.4
                + i.correspondent_banking_vulnerability * 0.35
                + i.trade_based_money_laundering_rate * 0.25
            ) * 100,
            2,
        )

    def _governance_score(self, i: FinancialCrimeInput) -> float:
        return round(
            (
                i.AML_enforcement_weakness_index * 0.4
                + i.financial_intelligence_gap * 0.35
                + i.kleptocracy_asset_repatriation_failure * 0.25
            ) * 100,
            2,
        )

    def _composite(
        self,
        laundering: float,
        evasion: float,
        opacity: float,
        governance: float,
    ) -> float:
        return round(
            laundering * 0.30
            + evasion * 0.25
            + opacity * 0.25
            + governance * 0.20,
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

    def _pattern(self, i: FinancialCrimeInput) -> str:
        if i.money_laundering_volume_index >= 0.70 and i.shell_company_opacity_level >= 0.65:
            return "systemic_laundering_network"
        if i.sanction_evasion_sophistication >= 0.70 and i.offshore_secrecy_exploitation >= 0.65:
            return "sanction_evasion_empire"
        if i.kleptocracy_asset_repatriation_failure >= 0.70 and i.state_sponsored_financial_crime_level >= 0.65:
            return "kleptocracy_financial_system"
        if i.crypto_crime_laundering_integration >= 0.70 and i.AML_enforcement_weakness_index >= 0.65:
            return "crypto_crime_integration"
        if i.professional_enabler_complicity_rate >= 0.70 and i.beneficial_ownership_opacity >= 0.65:
            return "professional_complicity_network"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity                                                            #
    # ------------------------------------------------------------------ #

    def _severity(self, risk: str) -> str:
        if risk == "critical":
            return "crime_financier_systémique"
        if risk == "high":
            return "réseau_criminel_financier_majeur"
        if risk == "moderate":
            return "vulnérabilité_financière_structurelle"
        return "risque_crime_financier_contenu"

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: str) -> str:
        if risk == "critical":
            return "intervention_AML_urgente"
        if risk == "high":
            return "démantèlement_réseau_financier_criminel"
        if risk == "moderate":
            return "renforcement_compliance_AML_systémique"
        return "veille_crime_financier_continue"

    # ------------------------------------------------------------------ #
    #  French signal                                                       #
    # ------------------------------------------------------------------ #

    def _signal(self, risk: str) -> str:
        signals = {
            "critical": "🔴 Crime financier systémique — blanchiment à grande échelle",
            "high":     "🟠 Réseau criminel financier majeur détecté",
            "moderate": "🟡 Vulnérabilité financière structurelle active",
            "low":      "🟢 Risque crime financier contenu et surveillé",
        }
        return signals.get(risk, "Statut inconnu")

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def _analyze_one(self, i: FinancialCrimeInput) -> FinancialCrimeResult:
        laundering = self._laundering_score(i)
        evasion    = self._evasion_score(i)
        opacity    = self._opacity_score(i)
        governance = self._governance_score(i)
        composite  = self._composite(laundering, evasion, opacity, governance)
        risk       = self._risk(composite)
        pattern    = self._pattern(i)
        severity   = self._severity(risk)
        action     = self._action(risk)
        signal     = self._signal(risk)

        return FinancialCrimeResult(
            entity_id=i.entity_id,
            financial_sector=i.financial_sector,
            region=i.region,
            risk_level=risk,
            crime_pattern=pattern,
            severity=severity,
            recommended_action=action,
            laundering_score=laundering,
            evasion_score=evasion,
            opacity_score=opacity,
            governance_score=governance,
            composite_score=composite,
            is_financial_crime_systemic=composite >= 60,
            requires_AML_intervention=composite >= 40,
            signal=signal,
            money_laundering_volume_index=i.money_laundering_volume_index,
            sanction_evasion_sophistication=i.sanction_evasion_sophistication,
        )

    def analyze(self, entities: List[FinancialCrimeInput]) -> List[FinancialCrimeResult]:
        results = [self._analyze_one(i) for i in entities]
        self._results.extend(results)
        return results

    def summary(self) -> Dict:
        if not self._results:
            return {
                "module_id":                        352,
                "module_name":                      "Anti-Money Laundering & Financial Crime Intelligence Engine",
                "total_entities":                   0,
                "critical_count":                   0,
                "high_count":                       0,
                "moderate_count":                   0,
                "low_count":                        0,
                "avg_composite":                    0.0,
                "pattern_distribution":             {},
                "risk_distribution":                {},
                "severity_distribution":            {},
                "action_distribution":              {},
                "avg_estimated_financial_crime_index": 0.0,
            }

        n = len(self._results)
        critical_count  = sum(1 for r in self._results if r.risk_level == "critical")
        high_count      = sum(1 for r in self._results if r.risk_level == "high")
        moderate_count  = sum(1 for r in self._results if r.risk_level == "moderate")
        low_count       = sum(1 for r in self._results if r.risk_level == "low")
        avg_composite   = sum(r.composite_score for r in self._results) / n

        pattern_distribution:  Dict[str, int] = {}
        risk_distribution:     Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution:   Dict[str, int] = {}

        for r in self._results:
            pattern_distribution[r.crime_pattern]    = pattern_distribution.get(r.crime_pattern, 0) + 1
            risk_distribution[r.risk_level]          = risk_distribution.get(r.risk_level, 0) + 1
            severity_distribution[r.severity]        = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action] = action_distribution.get(r.recommended_action, 0) + 1

        return {
            "module_id":                        352,
            "module_name":                      "Anti-Money Laundering & Financial Crime Intelligence Engine",
            "total_entities":                   n,
            "critical_count":                   critical_count,
            "high_count":                       high_count,
            "moderate_count":                   moderate_count,
            "low_count":                        low_count,
            "avg_composite":                    round(avg_composite, 2),
            "pattern_distribution":             pattern_distribution,
            "risk_distribution":                risk_distribution,
            "severity_distribution":            severity_distribution,
            "action_distribution":              action_distribution,
            "avg_estimated_financial_crime_index": round(avg_composite / 100 * 10, 2),
        }
