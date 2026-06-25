"""
Module 359 — Climate Finance & Green Transition Risk Intelligence Engine
Caelum Partners Swarm Intelligence Platform
"""

from dataclasses import dataclass
from typing import Optional
import statistics


@dataclass
class ClimateFinanceInput:
    entity_id: str
    finance_domain: str
    region: str
    # 17 float fields 0-1
    stranded_asset_exposure_rate: float
    green_washing_prevalence_index: float
    climate_finance_gap_severity: float
    carbon_credit_integrity_risk: float
    transition_risk_repricing_speed: float
    physical_risk_underpricing_level: float
    fossil_fuel_finance_lock_in: float
    just_transition_funding_deficit: float
    green_bond_market_fragility: float
    climate_regulatory_arbitrage_risk: float
    sovereign_climate_default_risk: float
    climate_litigation_financial_risk: float
    insurance_climate_retreat_rate: float
    private_climate_finance_mobilization_gap: float
    carbon_border_adjustment_shock: float
    biodiversity_finance_gap: float
    climate_finance_south_north_inequality: float


class ClimateFinanceEngine:
    MODULE_ID = 359
    MODULE_NAME = "Climate Finance & Green Transition Risk Intelligence Engine"

    def __init__(self):
        self.results: list[dict] = []

    def _compute_scores(self, inp: ClimateFinanceInput) -> dict:
        stranded_score = (
            inp.stranded_asset_exposure_rate * 0.4
            + inp.fossil_fuel_finance_lock_in * 0.35
            + inp.transition_risk_repricing_speed * 0.25
        ) * 100

        integrity_score = (
            inp.green_washing_prevalence_index * 0.4
            + inp.carbon_credit_integrity_risk * 0.35
            + inp.climate_regulatory_arbitrage_risk * 0.25
        ) * 100

        gap_score = (
            inp.climate_finance_gap_severity * 0.4
            + inp.just_transition_funding_deficit * 0.35
            + inp.private_climate_finance_mobilization_gap * 0.25
        ) * 100

        systemic_score = (
            inp.sovereign_climate_default_risk * 0.4
            + inp.insurance_climate_retreat_rate * 0.35
            + inp.climate_finance_south_north_inequality * 0.25
        ) * 100

        composite = (
            stranded_score * 0.30
            + integrity_score * 0.25
            + gap_score * 0.25
            + systemic_score * 0.20
        )

        return {
            "stranded_score": round(stranded_score, 2),
            "integrity_score": round(integrity_score, 2),
            "gap_score": round(gap_score, 2),
            "systemic_score": round(systemic_score, 2),
            "composite_score": round(composite, 2),
        }

    def _detect_pattern(self, inp: ClimateFinanceInput) -> str:
        if inp.stranded_asset_exposure_rate >= 0.70 and inp.fossil_fuel_finance_lock_in >= 0.65:
            return "stranded_asset_crisis"
        if inp.green_washing_prevalence_index >= 0.70 and inp.carbon_credit_integrity_risk >= 0.65:
            return "green_washing_epidemic"
        if inp.climate_finance_gap_severity >= 0.70 and inp.private_climate_finance_mobilization_gap >= 0.65:
            return "climate_finance_collapse"
        if inp.sovereign_climate_default_risk >= 0.70 and inp.physical_risk_underpricing_level >= 0.65:
            return "sovereign_climate_default"
        if inp.insurance_climate_retreat_rate >= 0.70 and inp.climate_finance_south_north_inequality >= 0.65:
            return "insurance_retreat_cascade"
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
            "critical": "crise_finance_climatique_systémique",
            "high": "risque_transition_verte_majeur",
            "moderate": "fragilité_finance_climatique_structurelle",
            "low": "finance_climatique_sous_surveillance",
        }
        return mapping[risk_level]

    def _get_action(self, risk_level: str) -> str:
        mapping = {
            "critical": "intervention_finance_climatique_urgente",
            "high": "réforme_finance_verte_accélérée",
            "moderate": "renforcement_intégrité_finance_climatique",
            "low": "veille_finance_climatique_continue",
        }
        return mapping[risk_level]

    def _get_signal(self, risk_level: str) -> str:
        mapping = {
            "critical": "🔴 Crise finance climatique systémique — transition verte compromise",
            "high": "🟠 Risque transition verte majeur détecté",
            "moderate": "🟡 Fragilité finance climatique structurelle active",
            "low": "🟢 Finance climatique sous surveillance",
        }
        return mapping[risk_level]

    def analyze(self, inp: ClimateFinanceInput) -> dict:
        scores = self._compute_scores(inp)
        risk_level = self._classify_risk(scores["composite_score"])
        pattern = self._detect_pattern(inp)
        severity = self._get_severity(risk_level)
        action = self._get_action(risk_level)
        signal = self._get_signal(risk_level)

        result = {
            "entity_id": inp.entity_id,
            "finance_domain": inp.finance_domain,
            "region": inp.region,
            "stranded_score": scores["stranded_score"],
            "integrity_score": scores["integrity_score"],
            "gap_score": scores["gap_score"],
            "systemic_score": scores["systemic_score"],
            "composite_score": scores["composite_score"],
            "risk_level": risk_level,
            "climate_finance_pattern": pattern,
            "severity": severity,
            "recommended_action": action,
            "signal": signal,
            "stranded_asset_exposure_rate": inp.stranded_asset_exposure_rate,
            "climate_finance_gap_severity": inp.climate_finance_gap_severity,
        }
        self.results.append(result)
        return result

    def to_dict(self, inp: ClimateFinanceInput) -> dict:
        """Returns exactly 15 keys."""
        scores = self._compute_scores(inp)
        risk_level = self._classify_risk(scores["composite_score"])
        pattern = self._detect_pattern(inp)
        severity = self._get_severity(risk_level)
        action = self._get_action(risk_level)
        signal = self._get_signal(risk_level)

        return {
            "entity_id": inp.entity_id,
            "finance_domain": inp.finance_domain,
            "region": inp.region,
            "stranded_score": scores["stranded_score"],
            "integrity_score": scores["integrity_score"],
            "gap_score": scores["gap_score"],
            "systemic_score": scores["systemic_score"],
            "composite_score": scores["composite_score"],
            "risk_level": risk_level,
            "climate_finance_pattern": pattern,
            "severity": severity,
            "recommended_action": action,
            "signal": signal,
            "stranded_asset_exposure_rate": inp.stranded_asset_exposure_rate,
            "climate_finance_gap_severity": inp.climate_finance_gap_severity,
        }

    def summary(self) -> dict:
        """Returns exactly 13 keys."""
        if not self.results:
            return {
                "module_id": self.MODULE_ID,
                "module_name": self.MODULE_NAME,
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
                "avg_estimated_climate_finance_index": 0.0,
            }

        total = len(self.results)
        critical_count = sum(1 for r in self.results if r["risk_level"] == "critical")
        high_count = sum(1 for r in self.results if r["risk_level"] == "high")
        moderate_count = sum(1 for r in self.results if r["risk_level"] == "moderate")
        low_count = sum(1 for r in self.results if r["risk_level"] == "low")
        avg_composite = round(statistics.mean(r["composite_score"] for r in self.results), 2)

        pattern_distribution: dict[str, int] = {}
        risk_distribution: dict[str, int] = {}
        severity_distribution: dict[str, int] = {}
        action_distribution: dict[str, int] = {}

        for r in self.results:
            p = r["climate_finance_pattern"]
            pattern_distribution[p] = pattern_distribution.get(p, 0) + 1
            rl = r["risk_level"]
            risk_distribution[rl] = risk_distribution.get(rl, 0) + 1
            s = r["severity"]
            severity_distribution[s] = severity_distribution.get(s, 0) + 1
            a = r["recommended_action"]
            action_distribution[a] = action_distribution.get(a, 0) + 1

        avg_estimated_climate_finance_index = round(avg_composite / 100 * 10, 2)

        return {
            "module_id": self.MODULE_ID,
            "module_name": self.MODULE_NAME,
            "total_entities": total,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution,
            "risk_distribution": risk_distribution,
            "severity_distribution": severity_distribution,
            "action_distribution": action_distribution,
            "avg_estimated_climate_finance_index": avg_estimated_climate_finance_index,
        }
