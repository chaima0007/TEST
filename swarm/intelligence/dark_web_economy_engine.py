"""
Module 384 — Dark Web Economy & Underground Market Intelligence Engine
Monitors ransomware ecosystems, underground drug/weapon/human markets,
crypto laundering, nation-state crime, AI-driven automation, and
criminal marketplace consolidation across digital underground economies.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DarkWebEconomyInput:
    entity_id: str
    market_type: str
    region: str
    # 17 float fields (0.0–1.0)
    ransomware_ecosystem_scale: float
    drug_market_volume: float
    stolen_data_market_size: float
    weapon_trafficking_intensity: float
    human_trafficking_digital: float
    cybercrime_as_service: float
    crypto_laundering_volume: float
    nation_state_marketplace: float
    darknet_market_resilience: float
    exit_scam_frequency: float
    law_enforcement_effectiveness_gap: float
    AI_crime_automation: float
    zero_day_exploit_market: float
    credential_market_saturation: float
    darkweb_to_mainstream_spillover: float
    illicit_services_professionalization: float
    criminal_marketplace_consolidation: float


@dataclass
class DarkWebEconomyResult:
    entity_id: str
    market_type: str
    region: str
    risk_level: str
    crime_pattern: str
    severity: str
    recommended_action: str
    crime_scale_score: float
    ecosystem_score: float
    enforcement_gap_score: float
    spillover_score: float
    composite_score: float
    is_darkweb_systemic: bool
    requires_darkweb_intervention: bool
    signal: str
    ransomware_ecosystem_scale: float
    crypto_laundering_volume: float

    def to_dict(self) -> Dict:
        return {
            "entity_id":                    self.entity_id,
            "market_type":                  self.market_type,
            "region":                       self.region,
            "crime_scale_score":            self.crime_scale_score,
            "ecosystem_score":              self.ecosystem_score,
            "enforcement_gap_score":        self.enforcement_gap_score,
            "spillover_score":              self.spillover_score,
            "composite_score":              self.composite_score,
            "risk_level":                   self.risk_level,
            "crime_pattern":                self.crime_pattern,
            "severity":                     self.severity,
            "recommended_action":           self.recommended_action,
            "signal":                       self.signal,
            "ransomware_ecosystem_scale":   self.ransomware_ecosystem_scale,
            "crypto_laundering_volume":     self.crypto_laundering_volume,
        }


class DarkWebEconomyEngine:
    """
    Module 384 — Dark Web Economy & Underground Market Intelligence Engine
    Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
    """

    def __init__(self) -> None:
        self._results: List[DarkWebEconomyResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100)                                                  #
    # ------------------------------------------------------------------ #

    def _crime_scale_score(self, i: DarkWebEconomyInput) -> float:
        return round(
            (
                i.ransomware_ecosystem_scale * 0.40
                + i.drug_market_volume * 0.35
                + i.weapon_trafficking_intensity * 0.25
            ) * 100,
            2,
        )

    def _ecosystem_score(self, i: DarkWebEconomyInput) -> float:
        return round(
            (
                i.cybercrime_as_service * 0.40
                + i.darknet_market_resilience * 0.35
                + i.criminal_marketplace_consolidation * 0.25
            ) * 100,
            2,
        )

    def _enforcement_gap_score(self, i: DarkWebEconomyInput) -> float:
        return round(
            (
                i.law_enforcement_effectiveness_gap * 0.40
                + i.crypto_laundering_volume * 0.35
                + i.exit_scam_frequency * 0.25
            ) * 100,
            2,
        )

    def _spillover_score(self, i: DarkWebEconomyInput) -> float:
        return round(
            (
                i.darkweb_to_mainstream_spillover * 0.40
                + i.AI_crime_automation * 0.35
                + i.illicit_services_professionalization * 0.25
            ) * 100,
            2,
        )

    def _composite(
        self,
        crime_scale: float,
        ecosystem: float,
        enforcement_gap: float,
        spillover: float,
    ) -> float:
        return round(
            crime_scale * 0.30
            + ecosystem * 0.25
            + enforcement_gap * 0.25
            + spillover * 0.20,
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

    def _pattern(self, i: DarkWebEconomyInput) -> str:
        if i.ransomware_ecosystem_scale > 0.85 and i.cybercrime_as_service > 0.80:
            return "ransomware_industrial_complex"
        if i.nation_state_marketplace > 0.85 and i.zero_day_exploit_market > 0.80:
            return "nation_state_crime_market"
        if i.criminal_marketplace_consolidation > 0.85 and i.illicit_services_professionalization > 0.80:
            return "criminal_marketplace_empire"
        if i.AI_crime_automation > 0.80 and i.darkweb_to_mainstream_spillover > 0.75:
            return "AI_crime_automation_crisis"
        if i.human_trafficking_digital > 0.80 and i.crypto_laundering_volume > 0.75:
            return "human_trafficking_digital_network"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity                                                            #
    # ------------------------------------------------------------------ #

    def _severity(self, risk: str) -> str:
        if risk == "critical":
            return "économie_criminelle_systémique"
        if risk == "high":
            return "marché_souterrain_majeur"
        if risk == "moderate":
            return "vulnérabilité_darkweb_structurelle"
        return "risque_darkweb_contenu"

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: str) -> str:
        if risk == "critical":
            return "démantèlement_urgence_darkweb"
        if risk == "high":
            return "neutralisation_réseau_souterrain"
        if risk == "moderate":
            return "surveillance_renforcée_marchés_illicites"
        return "veille_darkweb_continue"

    # ------------------------------------------------------------------ #
    #  French signal                                                       #
    # ------------------------------------------------------------------ #

    def _signal(self, risk: str) -> str:
        signals = {
            "critical": "🔴 Économie criminelle systémique — marché souterrain à grande échelle",
            "high":     "🟠 Marché souterrain majeur détecté — intervention requise",
            "moderate": "🟡 Vulnérabilité darkweb structurelle active",
            "low":      "🟢 Risque darkweb contenu et surveillé",
        }
        return signals.get(risk, "Statut inconnu")

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def _analyze_one(self, i: DarkWebEconomyInput) -> DarkWebEconomyResult:
        crime_scale     = self._crime_scale_score(i)
        ecosystem       = self._ecosystem_score(i)
        enforcement_gap = self._enforcement_gap_score(i)
        spillover       = self._spillover_score(i)
        composite       = self._composite(crime_scale, ecosystem, enforcement_gap, spillover)
        risk            = self._risk(composite)
        pattern         = self._pattern(i)
        severity        = self._severity(risk)
        action          = self._action(risk)
        signal          = self._signal(risk)

        return DarkWebEconomyResult(
            entity_id=i.entity_id,
            market_type=i.market_type,
            region=i.region,
            risk_level=risk,
            crime_pattern=pattern,
            severity=severity,
            recommended_action=action,
            crime_scale_score=crime_scale,
            ecosystem_score=ecosystem,
            enforcement_gap_score=enforcement_gap,
            spillover_score=spillover,
            composite_score=composite,
            is_darkweb_systemic=composite >= 60,
            requires_darkweb_intervention=composite >= 40,
            signal=signal,
            ransomware_ecosystem_scale=i.ransomware_ecosystem_scale,
            crypto_laundering_volume=i.crypto_laundering_volume,
        )

    def analyze(self, entities: List[DarkWebEconomyInput]) -> List[DarkWebEconomyResult]:
        results = [self._analyze_one(i) for i in entities]
        self._results.extend(results)
        return results

    def summary(self) -> Dict:
        if not self._results:
            return {
                "module_id":                        384,
                "module_name":                      "Dark Web Economy & Underground Market Intelligence Engine",
                "total":                            0,
                "critical":                         0,
                "high":                             0,
                "moderate":                         0,
                "low":                              0,
                "avg_composite":                    0.0,
                "pattern_distribution":             {},
                "risk_distribution":                {},
                "severity_distribution":            {},
                "action_distribution":              {},
                "avg_estimated_darkweb_risk_index": 0.0,
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
            pattern_distribution[r.crime_pattern]      = pattern_distribution.get(r.crime_pattern, 0) + 1
            risk_distribution[r.risk_level]            = risk_distribution.get(r.risk_level, 0) + 1
            severity_distribution[r.severity]          = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action]  = action_distribution.get(r.recommended_action, 0) + 1

        return {
            "module_id":                        384,
            "module_name":                      "Dark Web Economy & Underground Market Intelligence Engine",
            "total":                            n,
            "critical":                         critical_count,
            "high":                             high_count,
            "moderate":                         moderate_count,
            "low":                              low_count,
            "avg_composite":                    round(avg_composite, 2),
            "pattern_distribution":             pattern_distribution,
            "risk_distribution":                risk_distribution,
            "severity_distribution":            severity_distribution,
            "action_distribution":              action_distribution,
            "avg_estimated_darkweb_risk_index": round(avg_composite / 100 * 10, 2),
        }
