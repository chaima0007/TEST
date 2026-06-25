"""Module 263 — Autonomous Supply Chain Resilience & Disruption Intelligence Engine

Assesses supply chain node resilience across concentration risk, disruption
exposure, adaptive recovery capacity, and digital intelligence coverage to
identify fragile nodes and trigger autonomous mitigation actions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# ─── Input ────────────────────────────────────────────────────────────────────

@dataclass
class SupplyChainInput:
    node_id: str
    node_type: str   # tier1_supplier | tier2_supplier | distribution_hub | manufacturing_plant
                     # | last_mile | cold_chain | digital_supply | nearshoring_cluster
    region: str
    # Concentration & dependency (all 0.0–1.0)
    supplier_concentration_risk: float
    lead_time_variability: float
    inventory_buffer_adequacy: float
    demand_forecast_accuracy: float
    geopolitical_disruption_exposure: float
    climate_disruption_risk: float
    single_source_dependency: float
    digital_twin_coverage: float
    autonomous_reorder_capability: float
    supplier_financial_health: float
    nearshoring_readiness: float
    multi_modal_transport_flexibility: float
    real_time_visibility_score: float
    circular_economy_integration: float
    carbon_footprint_compliance: float
    ethical_sourcing_score: float
    disruption_recovery_speed: float


# ─── Result ───────────────────────────────────────────────────────────────────

@dataclass
class SupplyChainResult:
    node_id: str
    node_type: str
    region: str
    disruption_risk: str
    disruption_pattern: str
    disruption_severity: str
    recommended_action: str
    concentration_score: float
    disruption_score: float
    resilience_score: float
    intelligence_score: float
    supply_chain_composite: float
    has_critical_exposure: bool
    requires_immediate_intervention: bool
    estimated_disruption_impact_index: float
    disruption_signal: str

    def to_dict(self) -> dict:
        return {
            "node_id":                           self.node_id,
            "region":                            self.region,
            "disruption_risk":                   self.disruption_risk,
            "disruption_pattern":                self.disruption_pattern,
            "disruption_severity":               self.disruption_severity,
            "recommended_action":                self.recommended_action,
            "concentration_score":               self.concentration_score,
            "disruption_score":                  self.disruption_score,
            "resilience_score":                  self.resilience_score,
            "intelligence_score":                self.intelligence_score,
            "supply_chain_composite":            self.supply_chain_composite,
            "has_critical_exposure":             self.has_critical_exposure,
            "requires_immediate_intervention":   self.requires_immediate_intervention,
            "estimated_disruption_impact_index": self.estimated_disruption_impact_index,
            "disruption_signal":                 self.disruption_signal,
        }


# ─── Engine ───────────────────────────────────────────────────────────────────

class AutonomousSupplyChainEngine:

    def __init__(self) -> None:
        self._results: list[SupplyChainResult] = []

    # ── Sub-scores ─────────────────────────────────────────────────────────────

    def _concentration_score(self, inp: SupplyChainInput) -> float:
        """0.30 weight — concentration & single-source risk (higher = worse)."""
        s = 0.0
        # supplier_concentration_risk: high value = more concentrated = risky
        if   inp.supplier_concentration_risk >= 0.70: s += 40
        elif inp.supplier_concentration_risk >= 0.50: s += 22
        elif inp.supplier_concentration_risk >= 0.30: s += 8

        # single_source_dependency: high = risky
        if   inp.single_source_dependency >= 0.75: s += 35
        elif inp.single_source_dependency >= 0.50: s += 18
        elif inp.single_source_dependency >= 0.25: s += 6

        # supplier_financial_health: inverted — low health = high risk
        if   inp.supplier_financial_health <= 0.25: s += 25
        elif inp.supplier_financial_health <= 0.50: s += 12

        return min(s, 100.0)

    def _disruption_score(self, inp: SupplyChainInput) -> float:
        """0.25 weight — external disruption exposure (higher = worse)."""
        s = 0.0
        if   inp.geopolitical_disruption_exposure >= 0.70: s += 40
        elif inp.geopolitical_disruption_exposure >= 0.50: s += 22
        elif inp.geopolitical_disruption_exposure >= 0.30: s += 8

        if   inp.climate_disruption_risk >= 0.70: s += 35
        elif inp.climate_disruption_risk >= 0.50: s += 18
        elif inp.climate_disruption_risk >= 0.30: s += 6

        if   inp.lead_time_variability >= 0.65: s += 25
        elif inp.lead_time_variability >= 0.40: s += 12

        return min(s, 100.0)

    def _resilience_score(self, inp: SupplyChainInput) -> float:
        """0.25 weight — adaptive recovery capacity (inverted — higher score = worse resilience)."""
        s = 0.0
        # disruption_recovery_speed inverted: low speed = high risk
        if   inp.disruption_recovery_speed <= 0.25: s += 40
        elif inp.disruption_recovery_speed <= 0.50: s += 22
        elif inp.disruption_recovery_speed <= 0.70: s += 8

        # inventory_buffer_adequacy inverted: low buffer = high risk
        if   inp.inventory_buffer_adequacy <= 0.25: s += 35
        elif inp.inventory_buffer_adequacy <= 0.50: s += 18
        elif inp.inventory_buffer_adequacy <= 0.70: s += 6

        # multi_modal_transport_flexibility inverted: low flex = high risk
        if   inp.multi_modal_transport_flexibility <= 0.25: s += 25
        elif inp.multi_modal_transport_flexibility <= 0.50: s += 12

        return min(s, 100.0)

    def _intelligence_score(self, inp: SupplyChainInput) -> float:
        """0.20 weight — digital intelligence coverage (inverted — higher score = worse coverage)."""
        s = 0.0
        # digital_twin_coverage inverted: low coverage = high risk
        if   inp.digital_twin_coverage <= 0.20: s += 40
        elif inp.digital_twin_coverage <= 0.45: s += 22
        elif inp.digital_twin_coverage <= 0.65: s += 8

        # autonomous_reorder_capability inverted: low = high risk
        if   inp.autonomous_reorder_capability <= 0.20: s += 35
        elif inp.autonomous_reorder_capability <= 0.45: s += 18
        elif inp.autonomous_reorder_capability <= 0.65: s += 6

        # real_time_visibility_score inverted: low = high risk
        if   inp.real_time_visibility_score <= 0.25: s += 25
        elif inp.real_time_visibility_score <= 0.50: s += 12

        return min(s, 100.0)

    def _composite(
        self, conc: float, disr: float, res: float, intel: float
    ) -> float:
        return min(
            round(conc * 0.30 + disr * 0.25 + res * 0.25 + intel * 0.20, 2),
            100.0,
        )

    # ── Classification ─────────────────────────────────────────────────────────

    def _disruption_risk(self, composite: float) -> str:
        if composite >= 60: return "critical"
        if composite >= 40: return "high"
        if composite >= 20: return "moderate"
        return "low"

    def _disruption_severity(self, composite: float) -> str:
        if composite >= 60: return "fractured"
        if composite >= 40: return "stressed"
        if composite >= 20: return "adaptive"
        return "autonomous"

    def _disruption_pattern(self, inp: SupplyChainInput) -> str:
        if inp.supplier_concentration_risk >= 0.70 and inp.single_source_dependency >= 0.65:
            return "supplier_collapse"
        if inp.geopolitical_disruption_exposure >= 0.65 or inp.climate_disruption_risk >= 0.70:
            return "climate_disruption"
        if inp.demand_forecast_accuracy <= 0.35:
            return "demand_shock"
        if inp.multi_modal_transport_flexibility <= 0.25 and inp.lead_time_variability >= 0.60:
            return "logistics_breakdown"
        if inp.digital_twin_coverage <= 0.20 and inp.real_time_visibility_score <= 0.25:
            return "digital_blindspot"
        return "none"

    def _recommended_action(self, risk: str, pattern: str) -> str:
        if risk == "critical":
            if pattern in ("supplier_collapse", "demand_shock"):
                return "emergency_sourcing"
            return "supply_diversification"
        if risk == "high":
            if pattern in ("climate_disruption", "logistics_breakdown"):
                return "nearshoring_acceleration"
            return "buffer_stockpiling"
        if risk == "moderate":
            return "resilience_monitoring"
        return "no_action"

    # ── Signal ─────────────────────────────────────────────────────────────────

    def _disruption_signal(
        self, inp: SupplyChainInput, pattern: str, composite: float
    ) -> str:
        if composite < 20:
            return (
                "Chaîne d'approvisionnement autonome — résilience forte, "
                "couverture digitale optimale, risque de rupture minimal"
            )
        labels: dict[str, str] = {
            "supplier_collapse":  "Effondrement fournisseur",
            "demand_shock":       "Choc demande",
            "logistics_breakdown":"Rupture logistique",
            "digital_blindspot":  "Angle mort digital",
            "climate_disruption": "Disruption climatique",
        }
        label = labels.get(pattern, pattern.replace("_", " "))
        return (
            f"{label} — concentration {inp.supplier_concentration_risk:.2f} "
            f"— exposition géopolitique {inp.geopolitical_disruption_exposure:.2f} "
            f"— récupération {inp.disruption_recovery_speed:.2f} "
            f"— composite {round(composite)}"
        )

    # ── Main assess ────────────────────────────────────────────────────────────

    def assess(self, inp: SupplyChainInput) -> SupplyChainResult:
        conc  = round(self._concentration_score(inp), 1)
        disr  = round(self._disruption_score(inp), 1)
        res   = round(self._resilience_score(inp), 1)
        intel = round(self._intelligence_score(inp), 1)
        comp  = self._composite(conc, disr, res, intel)

        pattern  = self._disruption_pattern(inp)
        risk     = self._disruption_risk(comp)
        severity = self._disruption_severity(comp)
        action   = self._recommended_action(risk, pattern)
        signal   = self._disruption_signal(inp, pattern, comp)

        has_critical = (
            comp >= 40
            or inp.supplier_concentration_risk >= 0.70
            or inp.single_source_dependency >= 0.75
            or inp.geopolitical_disruption_exposure >= 0.65
        )
        requires_intervention = (
            comp >= 25
            or inp.climate_disruption_risk >= 0.65
            or inp.digital_twin_coverage <= 0.20
            or inp.disruption_recovery_speed <= 0.20
        )
        impact_index = min(
            round(comp / 100 * (1 - inp.demand_forecast_accuracy + 0.01) * 10, 2),
            10.0,
        )

        result = SupplyChainResult(
            node_id                          = inp.node_id,
            node_type                        = inp.node_type,
            region                           = inp.region,
            disruption_risk                  = risk,
            disruption_pattern               = pattern,
            disruption_severity              = severity,
            recommended_action               = action,
            concentration_score              = conc,
            disruption_score                 = disr,
            resilience_score                 = res,
            intelligence_score               = intel,
            supply_chain_composite           = comp,
            has_critical_exposure            = has_critical,
            requires_immediate_intervention  = requires_intervention,
            estimated_disruption_impact_index= impact_index,
            disruption_signal                = signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[SupplyChainInput]) -> list[SupplyChainResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.supply_chain_composite, reverse=True)
        return results

    # ── Summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        results = self._results
        n = len(results)
        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_supply_chain_composite": 0.0,
                "critical_exposure_count": 0,
                "intervention_required_count": 0,
                "avg_concentration_score": 0.0,
                "avg_disruption_score": 0.0,
                "avg_resilience_score": 0.0,
                "avg_intelligence_score": 0.0,
                "avg_estimated_disruption_impact_index": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        t_comp = t_conc = t_disr = t_res = t_intel = t_impact = 0.0
        crit_c = interv_c = 0

        for r in results:
            risk_counts[r.disruption_risk]       = risk_counts.get(r.disruption_risk, 0) + 1
            pattern_counts[r.disruption_pattern] = pattern_counts.get(r.disruption_pattern, 0) + 1
            severity_counts[r.disruption_severity] = severity_counts.get(r.disruption_severity, 0) + 1
            action_counts[r.recommended_action]  = action_counts.get(r.recommended_action, 0) + 1
            t_comp  += r.supply_chain_composite
            t_conc  += r.concentration_score
            t_disr  += r.disruption_score
            t_res   += r.resilience_score
            t_intel += r.intelligence_score
            t_impact += r.estimated_disruption_impact_index
            if r.has_critical_exposure:          crit_c += 1
            if r.requires_immediate_intervention: interv_c += 1

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_supply_chain_composite":           round(t_comp / n, 1),
            "critical_exposure_count":              crit_c,
            "intervention_required_count":          interv_c,
            "avg_concentration_score":              round(t_conc / n, 1),
            "avg_disruption_score":                 round(t_disr / n, 1),
            "avg_resilience_score":                 round(t_res / n, 1),
            "avg_intelligence_score":               round(t_intel / n, 1),
            "avg_estimated_disruption_impact_index": round(t_impact / n, 2),
        }

    def reset(self) -> None:
        self._results = []
