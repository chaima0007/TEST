"""
Module 334 — Gig Economy Fragility & Precariat Intelligence Engine
Caelum Partners Swarm Intelligence Platform
Monitors platform worker precarity, rights erosion, exploitation patterns,
and systemic labor market dualization in gig economy contexts.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GigEconomyFragilityInput:
    entity_id: str
    labor_sector: str
    region: str
    # 17 float fields 0-1
    platform_worker_precarity_index: float = 0.0
    social_protection_absence_rate: float = 0.0
    income_volatility_severity: float = 0.0
    algorithmic_management_oppression: float = 0.0
    classification_misuse_rate: float = 0.0
    collective_bargaining_erosion: float = 0.0
    platform_monopoly_dependency: float = 0.0
    health_insecurity_exposure: float = 0.0
    housing_instability_cascade: float = 0.0
    gig_poverty_trap_prevalence: float = 0.0
    skills_atrophy_rate: float = 0.0
    demographic_exploitation_index: float = 0.0
    regulatory_arbitrage_exploitation: float = 0.0
    platform_exit_barrier: float = 0.0
    cross_platform_competition_race: float = 0.0
    gig_economy_gdp_dependency: float = 0.0
    labor_market_dualization_index: float = 0.0


class GigEconomyFragilityEngine:
    """
    Assesses gig economy fragility and precariat conditions across labor sectors.
    """

    # ── sub-scores ──────────────────────────────────────────────────────────────

    def _precarity_score(self, inp: GigEconomyFragilityInput) -> float:
        return (
            inp.platform_worker_precarity_index * 0.4
            + inp.income_volatility_severity * 0.35
            + inp.gig_poverty_trap_prevalence * 0.25
        ) * 100

    def _rights_score(self, inp: GigEconomyFragilityInput) -> float:
        return (
            inp.social_protection_absence_rate * 0.4
            + inp.collective_bargaining_erosion * 0.35
            + inp.classification_misuse_rate * 0.25
        ) * 100

    def _exploitation_score(self, inp: GigEconomyFragilityInput) -> float:
        return (
            inp.algorithmic_management_oppression * 0.4
            + inp.demographic_exploitation_index * 0.35
            + inp.regulatory_arbitrage_exploitation * 0.25
        ) * 100

    def _systemic_score(self, inp: GigEconomyFragilityInput) -> float:
        return (
            inp.labor_market_dualization_index * 0.4
            + inp.platform_monopoly_dependency * 0.35
            + inp.gig_economy_gdp_dependency * 0.25
        ) * 100

    def _composite(
        self,
        precarity: float,
        rights: float,
        exploitation: float,
        systemic: float,
    ) -> float:
        return precarity * 0.30 + rights * 0.25 + exploitation * 0.25 + systemic * 0.20

    # ── classification ───────────────────────────────────────────────────────────

    def _get_risk(self, composite: float) -> str:
        if composite >= 60:
            return "critical"
        if composite >= 40:
            return "high"
        if composite >= 20:
            return "moderate"
        return "low"

    def _get_pattern(self, inp: GigEconomyFragilityInput) -> str:
        if inp.platform_worker_precarity_index >= 0.70 and inp.social_protection_absence_rate >= 0.65:
            return "precariat_explosion"
        if inp.algorithmic_management_oppression >= 0.70 and inp.platform_monopoly_dependency >= 0.65:
            return "algorithmic_serfdom"
        if inp.collective_bargaining_erosion >= 0.70 and inp.classification_misuse_rate >= 0.65:
            return "rights_collapse"
        if inp.demographic_exploitation_index >= 0.70 and inp.income_volatility_severity >= 0.65:
            return "demographic_exploitation"
        if inp.labor_market_dualization_index >= 0.70 and inp.gig_economy_gdp_dependency >= 0.65:
            return "systemic_dualization"
        return "none"

    def _get_severity(self, composite: float) -> str:
        if composite >= 60:
            return "effondrement_social_précariat"
        if composite >= 40:
            return "crise_travail_platformisé"
        if composite >= 20:
            return "précarisation_structurelle"
        return "tensions_gig_contenues"

    def _get_action(self, risk: str) -> str:
        if risk == "critical":
            return "intervention_sociale_urgente"
        if risk == "high":
            return "régulation_plateforme_activée"
        if risk == "moderate":
            return "renforcement_droits_travailleurs_gig"
        return "veille_précarité_continue"

    def _get_signal(self, risk: str) -> str:
        signals = {
            "critical": "🔴 Effondrement social précariat — crise du travail critique",
            "high": "🟠 Crise du travail platformisé détectée",
            "moderate": "🟡 Précarisation structurelle en cours",
            "low": "🟢 Économie gig relativement stable",
        }
        return signals.get(risk, "")

    # ── per-entity analysis ──────────────────────────────────────────────────────

    def _analyze_entity(self, inp: GigEconomyFragilityInput) -> Dict[str, Any]:
        precarity = self._precarity_score(inp)
        rights = self._rights_score(inp)
        exploitation = self._exploitation_score(inp)
        systemic = self._systemic_score(inp)
        composite = self._composite(precarity, rights, exploitation, systemic)
        risk = self._get_risk(composite)
        pattern = self._get_pattern(inp)
        severity = self._get_severity(composite)
        action = self._get_action(risk)
        signal = self._get_signal(risk)

        return {
            "entity_id": inp.entity_id,
            "labor_sector": inp.labor_sector,
            "region": inp.region,
            "precarity_score": round(precarity, 2),
            "rights_score": round(rights, 2),
            "exploitation_score": round(exploitation, 2),
            "systemic_score": round(systemic, 2),
            "composite_score": round(composite, 2),
            "risk_level": risk,
            "gig_pattern": pattern,
            "severity": severity,
            "recommended_action": action,
            "signal": signal,
            "platform_worker_precarity_index": inp.platform_worker_precarity_index,
            "labor_market_dualization_index": inp.labor_market_dualization_index,
        }

    def analyze(self, entities: List[GigEconomyFragilityInput]) -> Dict[str, Any]:
        results = [self._analyze_entity(e) for e in entities]
        return {"entities": results, "summary": self.summary(results)}

    # ── summary (exactly 13 keys) ────────────────────────────────────────────────

    def summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        total = len(results)
        if total == 0:
            return {
                "module_id": 334,
                "module_name": "Gig Economy Fragility & Precariat Intelligence Engine",
                "total_entities": 0,
                "critical_count": 0,
                "high_count": 0,
                "moderate_count": 0,
                "low_count": 0,
                "avg_composite": 0.0,
                "pattern_distribution": {},
                "risk_distribution": {},
                "severity_distribution": {},
                "action_distribution": {},
                "avg_estimated_precarity_index": 0.0,
            }

        critical_count = sum(1 for r in results if r["risk_level"] == "critical")
        high_count = sum(1 for r in results if r["risk_level"] == "high")
        moderate_count = sum(1 for r in results if r["risk_level"] == "moderate")
        low_count = sum(1 for r in results if r["risk_level"] == "low")
        avg_composite = sum(r["composite_score"] for r in results) / total

        pattern_distribution: Dict[str, int] = {}
        risk_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        for r in results:
            pattern_distribution[r["gig_pattern"]] = pattern_distribution.get(r["gig_pattern"], 0) + 1
            risk_distribution[r["risk_level"]] = risk_distribution.get(r["risk_level"], 0) + 1
            severity_distribution[r["severity"]] = severity_distribution.get(r["severity"], 0) + 1
            action_distribution[r["recommended_action"]] = action_distribution.get(r["recommended_action"], 0) + 1

        return {
            "module_id": 334,
            "module_name": "Gig Economy Fragility & Precariat Intelligence Engine",
            "total_entities": total,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": round(avg_composite, 2),
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_precarity_index": round(avg_composite / 100 * 10, 2),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys — one result-shape record describing this engine."""
        return {
            "entity_id": "GigEconomyFragilityEngine",
            "labor_sector": "multi-sector",
            "region": "global",
            "precarity_score": 0.0,
            "rights_score": 0.0,
            "exploitation_score": 0.0,
            "systemic_score": 0.0,
            "composite_score": 0.0,
            "risk_level": "low",
            "gig_pattern": "none",
            "severity": "tensions_gig_contenues",
            "recommended_action": "veille_précarité_continue",
            "signal": "🟢 Économie gig relativement stable",
            "platform_worker_precarity_index": 0.0,
            "labor_market_dualization_index": 0.0,
        }
