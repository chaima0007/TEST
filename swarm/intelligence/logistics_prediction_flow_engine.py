"""Logistics Prediction & Flow Management Engine — predictive optimization of supply chain flows."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LogisticsRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class FlowPattern(str, Enum):
    NONE = "none"
    SUPPLY_DISRUPTION = "supply_disruption"
    DEMAND_SURGE = "demand_surge"
    BOTTLENECK_CASCADE = "bottleneck_cascade"
    LAST_MILE_FAILURE = "last_mile_failure"
    INVENTORY_IMBALANCE = "inventory_imbalance"


class LogisticsSeverity(str, Enum):
    FLUID = "fluid"
    CONSTRAINED = "constrained"
    DISRUPTED = "disrupted"
    CRITICAL = "critical"


class LogisticsAction(str, Enum):
    NO_ACTION = "no_action"
    FLOW_MONITORING = "flow_monitoring"
    BUFFER_ACTIVATION = "buffer_activation"
    ROUTE_OPTIMIZATION = "route_optimization"
    DEMAND_REBALANCING = "demand_rebalancing"
    SUPPLIER_ESCALATION = "supplier_escalation"
    EMERGENCY_REROUTING = "emergency_rerouting"
    CRISIS_LOGISTICS = "crisis_logistics"
    SUPPLY_CHAIN_RESET = "supply_chain_reset"


@dataclass
class LogisticsInput:
    flow_id: str
    logistics_type: str                       # inbound/outbound/reverse/last_mile/warehouse/cross_dock
    region: str
    on_time_delivery_rate: float              # 0-1, 1=perfect
    fill_rate: float                          # 0-1, 1=perfect
    inventory_turnover_score: float           # 0-1, 1=optimal
    stockout_rate: float                      # 0-1, 1=always out
    overstock_rate: float                     # 0-1, 1=always overstocked
    supplier_reliability_score: float         # 0-1, 1=perfectly reliable
    lead_time_variance_days: float            # days of variance
    demand_forecast_accuracy: float           # 0-1, 1=perfect forecast
    transportation_cost_index: float          # 0-1, 1=very expensive
    route_efficiency_score: float             # 0-1, 1=optimal
    customs_clearance_delay_days: float       # days
    last_mile_success_rate: float             # 0-1, 1=perfect
    reverse_logistics_efficiency: float       # 0-1, 1=perfect
    cross_dock_efficiency: float              # 0-1, 1=optimal
    carbon_footprint_score: float             # 0-1, 1=high carbon
    resilience_node_redundancy: float         # 0-1, 1=high redundancy
    real_time_visibility_score: float         # 0-1, 1=full visibility


@dataclass
class LogisticsResult:
    flow_id: str
    region: str
    logistics_risk: LogisticsRisk
    flow_pattern: FlowPattern
    logistics_severity: LogisticsSeverity
    recommended_action: LogisticsAction
    delivery_score: float
    efficiency_score: float
    reliability_score: float
    resilience_score: float
    logistics_composite: float
    has_flow_alert: bool
    requires_strategic_review: bool
    estimated_supply_disruption_index: float  # 0-10
    logistics_signal: str

    def to_dict(self) -> dict:
        return {
            "flow_id": self.flow_id,
            "region": self.region,
            "logistics_risk": self.logistics_risk.value,
            "flow_pattern": self.flow_pattern.value,
            "logistics_severity": self.logistics_severity.value,
            "recommended_action": self.recommended_action.value,
            "delivery_score": self.delivery_score,
            "efficiency_score": self.efficiency_score,
            "reliability_score": self.reliability_score,
            "resilience_score": self.resilience_score,
            "logistics_composite": self.logistics_composite,
            "has_flow_alert": self.has_flow_alert,
            "requires_strategic_review": self.requires_strategic_review,
            "estimated_supply_disruption_index": self.estimated_supply_disruption_index,
            "logistics_signal": self.logistics_signal,
        }


# ── sub-score calculators ─────────────────────────────────────────────────────

def _delivery_score(inp: LogisticsInput) -> float:
    """0.30 weight — penalize low on_time_delivery_rate, low fill_rate, high stockout_rate."""
    score = 0.0
    if inp.on_time_delivery_rate <= 0.60:
        score += 40
    elif inp.on_time_delivery_rate <= 0.75:
        score += 22
    elif inp.on_time_delivery_rate <= 0.88:
        score += 9
    if inp.fill_rate <= 0.60:
        score += 35
    elif inp.fill_rate <= 0.75:
        score += 18
    elif inp.fill_rate <= 0.88:
        score += 7
    if inp.stockout_rate >= 0.40:
        score += 25
    elif inp.stockout_rate >= 0.20:
        score += 12
    elif inp.stockout_rate >= 0.10:
        score += 5
    return round(min(score, 100.0), 2)


def _efficiency_score(inp: LogisticsInput) -> float:
    """0.25 weight — penalize low route_efficiency_score, high transportation_cost_index, high lead_time_variance_days (scaled)."""
    score = 0.0
    if inp.route_efficiency_score <= 0.40:
        score += 40
    elif inp.route_efficiency_score <= 0.60:
        score += 22
    elif inp.route_efficiency_score <= 0.75:
        score += 9
    if inp.transportation_cost_index >= 0.75:
        score += 35
    elif inp.transportation_cost_index >= 0.50:
        score += 18
    elif inp.transportation_cost_index >= 0.30:
        score += 7
    # lead_time_variance_days: scale up to 20 days = 100%
    ltv_scaled = min(inp.lead_time_variance_days / 20.0, 1.0)
    if ltv_scaled >= 0.75:
        score += 25
    elif ltv_scaled >= 0.50:
        score += 12
    elif ltv_scaled >= 0.25:
        score += 5
    return round(min(score, 100.0), 2)


def _reliability_score(inp: LogisticsInput) -> float:
    """0.25 weight — penalize low supplier_reliability_score, low demand_forecast_accuracy, high customs_clearance_delay_days (scaled)."""
    score = 0.0
    if inp.supplier_reliability_score <= 0.40:
        score += 40
    elif inp.supplier_reliability_score <= 0.60:
        score += 22
    elif inp.supplier_reliability_score <= 0.75:
        score += 9
    if inp.demand_forecast_accuracy <= 0.40:
        score += 35
    elif inp.demand_forecast_accuracy <= 0.60:
        score += 18
    elif inp.demand_forecast_accuracy <= 0.75:
        score += 7
    # customs_clearance_delay_days: scale up to 14 days = 100%
    ccd_scaled = min(inp.customs_clearance_delay_days / 14.0, 1.0)
    if ccd_scaled >= 0.75:
        score += 25
    elif ccd_scaled >= 0.50:
        score += 12
    elif ccd_scaled >= 0.25:
        score += 5
    return round(min(score, 100.0), 2)


def _resilience_score(inp: LogisticsInput) -> float:
    """0.20 weight — penalize low resilience_node_redundancy, low real_time_visibility_score, high carbon_footprint_score."""
    score = 0.0
    if inp.resilience_node_redundancy <= 0.30:
        score += 40
    elif inp.resilience_node_redundancy <= 0.50:
        score += 22
    elif inp.resilience_node_redundancy <= 0.70:
        score += 9
    if inp.real_time_visibility_score <= 0.30:
        score += 35
    elif inp.real_time_visibility_score <= 0.50:
        score += 18
    elif inp.real_time_visibility_score <= 0.70:
        score += 7
    if inp.carbon_footprint_score >= 0.75:
        score += 25
    elif inp.carbon_footprint_score >= 0.50:
        score += 12
    elif inp.carbon_footprint_score >= 0.30:
        score += 5
    return round(min(score, 100.0), 2)


def _composite(deliv: float, eff: float, rel: float, res: float) -> float:
    return round(deliv * 0.30 + eff * 0.25 + rel * 0.25 + res * 0.20, 2)


def _risk(composite: float) -> LogisticsRisk:
    if composite >= 60:
        return LogisticsRisk.CRITICAL
    if composite >= 40:
        return LogisticsRisk.HIGH
    if composite >= 20:
        return LogisticsRisk.MODERATE
    return LogisticsRisk.LOW


def _severity(composite: float) -> LogisticsSeverity:
    if composite >= 60:
        return LogisticsSeverity.CRITICAL
    if composite >= 40:
        return LogisticsSeverity.DISRUPTED
    if composite >= 20:
        return LogisticsSeverity.CONSTRAINED
    return LogisticsSeverity.FLUID


def _pattern(inp: LogisticsInput) -> FlowPattern:
    # Priority order
    if inp.supplier_reliability_score <= 0.4 or inp.lead_time_variance_days >= 10:
        return FlowPattern.SUPPLY_DISRUPTION
    if inp.stockout_rate >= 0.4 and inp.demand_forecast_accuracy <= 0.5:
        return FlowPattern.DEMAND_SURGE
    if inp.route_efficiency_score <= 0.4 and inp.cross_dock_efficiency <= 0.4:
        return FlowPattern.BOTTLENECK_CASCADE
    if inp.last_mile_success_rate <= 0.6:
        return FlowPattern.LAST_MILE_FAILURE
    if inp.overstock_rate >= 0.4 or (inp.stockout_rate >= 0.3 and inp.overstock_rate >= 0.2):
        return FlowPattern.INVENTORY_IMBALANCE
    return FlowPattern.NONE


def _action(risk: LogisticsRisk, pattern: FlowPattern) -> LogisticsAction:
    if risk == LogisticsRisk.CRITICAL:
        if pattern == FlowPattern.SUPPLY_DISRUPTION:
            return LogisticsAction.SUPPLY_CHAIN_RESET
        if pattern == FlowPattern.BOTTLENECK_CASCADE:
            return LogisticsAction.EMERGENCY_REROUTING
        return LogisticsAction.CRISIS_LOGISTICS
    if risk == LogisticsRisk.HIGH:
        if pattern == FlowPattern.SUPPLY_DISRUPTION:
            return LogisticsAction.SUPPLIER_ESCALATION
        if pattern == FlowPattern.DEMAND_SURGE:
            return LogisticsAction.DEMAND_REBALANCING
        if pattern == FlowPattern.BOTTLENECK_CASCADE:
            return LogisticsAction.EMERGENCY_REROUTING
        if pattern == FlowPattern.LAST_MILE_FAILURE:
            return LogisticsAction.ROUTE_OPTIMIZATION
        if pattern == FlowPattern.INVENTORY_IMBALANCE:
            return LogisticsAction.BUFFER_ACTIVATION
        return LogisticsAction.FLOW_MONITORING
    if risk == LogisticsRisk.MODERATE:
        return LogisticsAction.FLOW_MONITORING
    return LogisticsAction.NO_ACTION


def _signal(inp: LogisticsInput, comp: float, risk: LogisticsRisk) -> str:
    if comp < 20:
        return "Flux logistiques optimaux — livraisons fiables, stocks équilibrés, fournisseurs performants"
    label = risk.value.replace("_", " ").title()
    return (
        f"{label} — livraisons à temps {round(inp.on_time_delivery_rate * 100)}%"
        f" — ruptures {round(inp.stockout_rate * 100)}%"
        f" — fiabilité fournisseurs {round(inp.supplier_reliability_score * 100)}%"
        f" — composite {round(comp)}"
    )


# ── Mock flows ─────────────────────────────────────────────────────────────────

_MOCK_FLOWS: list[LogisticsInput] = [
    # Fields after region: on_time_delivery_rate fill_rate inventory_turnover_score stockout_rate overstock_rate
    #   supplier_reliability_score lead_time_variance_days demand_forecast_accuracy transportation_cost_index
    #   route_efficiency_score customs_clearance_delay_days last_mile_success_rate reverse_logistics_efficiency
    #   cross_dock_efficiency carbon_footprint_score resilience_node_redundancy real_time_visibility_score  (17)
    # LF-001 inbound EMEA critical supply_disruption
    LogisticsInput("LF-001", "inbound", "EMEA",
                   0.50, 0.48, 0.40, 0.45, 0.20, 0.25, 15.0, 0.30, 0.80, 0.35, 1.5, 0.45, 0.40, 0.30, 0.75, 0.20, 0.22),
    # LF-002 outbound NAMER low fluid
    LogisticsInput("LF-002", "outbound", "NAMER",
                   0.95, 0.92, 0.90, 0.05, 0.05, 0.92, 1.0, 0.95, 0.12, 0.95, 0.5, 0.90, 0.88, 0.90, 0.15, 0.88, 0.92),
    # LF-003 last_mile APAC high last_mile_failure
    LogisticsInput("LF-003", "last_mile", "APAC",
                   0.65, 0.62, 0.55, 0.20, 0.15, 0.65, 5.0, 0.60, 0.35, 0.55, 3.0, 0.40, 0.68, 0.58, 0.45, 0.40, 0.55),
    # LF-004 warehouse LATAM moderate inventory_imbalance
    LogisticsInput("LF-004", "warehouse", "LATAM",
                   0.78, 0.75, 0.60, 0.25, 0.42, 0.72, 4.0, 0.65, 0.38, 0.70, 2.0, 0.75, 0.72, 0.68, 0.45, 0.55, 0.65),
    # LF-005 cross_dock MEA critical bottleneck_cascade
    LogisticsInput("LF-005", "cross_dock", "MEA",
                   0.45, 0.40, 0.35, 0.42, 0.22, 0.35, 12.0, 0.30, 0.75, 0.30, 5.0, 0.55, 0.35, 0.30, 0.80, 0.22, 0.28),
    # LF-006 reverse EMEA moderate constrained
    LogisticsInput("LF-006", "reverse", "EMEA",
                   0.72, 0.70, 0.58, 0.18, 0.22, 0.68, 3.5, 0.62, 0.40, 0.65, 1.5, 0.65, 0.62, 0.60, 0.48, 0.55, 0.60),
    # LF-007 inbound NAMER high demand_surge
    LogisticsInput("LF-007", "inbound", "NAMER",
                   0.60, 0.55, 0.48, 0.45, 0.18, 0.60, 7.0, 0.38, 0.55, 0.55, 2.5, 0.62, 0.58, 0.52, 0.42, 0.45, 0.50),
    # LF-008 outbound APAC low fluid
    LogisticsInput("LF-008", "outbound", "APAC",
                   0.92, 0.90, 0.88, 0.06, 0.08, 0.90, 1.2, 0.92, 0.15, 0.90, 0.5, 0.92, 0.88, 0.88, 0.18, 0.88, 0.90),
]


class LogisticsPredictionFlowEngine:
    """Predicts supply chain disruptions and optimizes logistics flow management."""

    def __init__(self) -> None:
        self._results: list[LogisticsResult] = []

    def evaluate(self, inp: LogisticsInput) -> LogisticsResult:
        deliv_s = _delivery_score(inp)
        eff_s = _efficiency_score(inp)
        rel_s = _reliability_score(inp)
        res_s = _resilience_score(inp)
        comp = _composite(deliv_s, eff_s, rel_s, res_s)

        risk = _risk(comp)
        severity = _severity(comp)
        pattern = _pattern(inp)
        action = _action(risk, pattern)

        has_alert = (
            comp >= 40
            or inp.on_time_delivery_rate <= 0.7
            or inp.stockout_rate >= 0.35
            or inp.supplier_reliability_score <= 0.4
        )
        requires_review = (
            comp >= 25
            or inp.resilience_node_redundancy <= 0.35
            or inp.demand_forecast_accuracy <= 0.4
        )
        disruption_idx = round(min(comp / 100 * (1 - inp.resilience_node_redundancy + 0.01) * 10, 10.0), 2)
        sig = _signal(inp, comp, risk)

        result = LogisticsResult(
            flow_id=inp.flow_id,
            region=inp.region,
            logistics_risk=risk,
            flow_pattern=pattern,
            logistics_severity=severity,
            recommended_action=action,
            delivery_score=deliv_s,
            efficiency_score=eff_s,
            reliability_score=rel_s,
            resilience_score=res_s,
            logistics_composite=comp,
            has_flow_alert=has_alert,
            requires_strategic_review=requires_review,
            estimated_supply_disruption_index=disruption_idx,
            logistics_signal=sig,
        )
        self._results.append(result)
        return result

    def evaluate_batch(self, inputs: list[LogisticsInput]) -> list[LogisticsResult]:
        for inp in inputs:
            self.evaluate(inp)
        self._results.sort(key=lambda r: r.logistics_composite, reverse=True)
        return self._results

    def load_mock_flows(self) -> list[LogisticsResult]:
        self._results.clear()
        return self.evaluate_batch(_MOCK_FLOWS)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_logistics_composite": 0.0,
                "flow_alert_count": 0,
                "strategic_review_count": 0,
                "avg_delivery_score": 0.0,
                "avg_efficiency_score": 0.0,
                "avg_reliability_score": 0.0,
                "avg_resilience_score": 0.0,
                "avg_estimated_supply_disruption_index": 0.0,
            }
        risk_counts: dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_comp = total_deliv = total_eff = total_rel = total_res = total_idx = 0.0
        for r in self._results:
            risk_counts[r.logistics_risk.value] = risk_counts.get(r.logistics_risk.value, 0) + 1
            pattern_counts[r.flow_pattern.value] = pattern_counts.get(r.flow_pattern.value, 0) + 1
            severity_counts[r.logistics_severity.value] = severity_counts.get(r.logistics_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.logistics_composite
            total_deliv += r.delivery_score
            total_eff += r.efficiency_score
            total_rel += r.reliability_score
            total_res += r.resilience_score
            total_idx += r.estimated_supply_disruption_index
        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_logistics_composite": round(total_comp / n, 2),
            "flow_alert_count": sum(1 for r in self._results if r.has_flow_alert),
            "strategic_review_count": sum(1 for r in self._results if r.requires_strategic_review),
            "avg_delivery_score": round(total_deliv / n, 2),
            "avg_efficiency_score": round(total_eff / n, 2),
            "avg_reliability_score": round(total_rel / n, 2),
            "avg_resilience_score": round(total_res / n, 2),
            "avg_estimated_supply_disruption_index": round(total_idx / n, 2),
        }
