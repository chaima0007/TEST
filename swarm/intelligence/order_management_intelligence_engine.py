from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class OrderRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class OrderPattern(str, Enum):
    none                 = "none"
    fulfillment_delay    = "fulfillment_delay"
    inventory_shortage   = "inventory_shortage"
    supplier_failure     = "supplier_failure"
    quality_hold         = "quality_hold"
    logistics_bottleneck = "logistics_bottleneck"


class OrderSeverity(str, Enum):
    on_schedule = "on_schedule"
    at_risk     = "at_risk"
    delayed     = "delayed"
    blocked     = "blocked"


class OrderAction(str, Enum):
    no_action              = "no_action"
    order_monitoring       = "order_monitoring"
    expedite_fulfillment   = "expedite_fulfillment"
    supplier_escalation    = "supplier_escalation"
    inventory_reallocation = "inventory_reallocation"
    quality_inspection     = "quality_inspection"
    logistics_rerouting    = "logistics_rerouting"
    customer_notification  = "customer_notification"
    emergency_procurement  = "emergency_procurement"


@dataclass
class OrderInput:
    order_id: str
    client_id: str
    region: str
    days_past_promise_date: int
    fulfillment_cycle_time_days: float
    order_completion_pct: float
    warehouse_processing_delay_days: int
    inventory_availability_pct: float
    supplier_on_time_rate_pct: float
    backorder_item_count: int
    substitute_product_available: float
    quality_hold_count: int
    quality_rejection_rate_pct: float
    carrier_performance_score: float
    transit_delay_days: int
    customs_clearance_days: int
    client_priority_tier: int
    contract_sla_breach_count: int
    order_value_usd: float
    repeat_order_client: float
    escalation_requested: float


@dataclass
class OrderResult:
    order_id: str
    region: str
    order_risk: OrderRisk
    order_pattern: OrderPattern
    order_severity: OrderSeverity
    recommended_action: OrderAction
    fulfillment_score: float
    inventory_score: float
    quality_score: float
    logistics_score: float
    order_composite: float
    has_delivery_risk: bool
    requires_client_alert: bool
    estimated_delay_days: int
    order_signal: str

    def to_dict(self) -> dict:
        return {
            "order_id":              self.order_id,
            "region":                self.region,
            "order_risk":            self.order_risk.value,
            "order_pattern":         self.order_pattern.value,
            "order_severity":        self.order_severity.value,
            "recommended_action":    self.recommended_action.value,
            "fulfillment_score":     self.fulfillment_score,
            "inventory_score":       self.inventory_score,
            "quality_score":         self.quality_score,
            "logistics_score":       self.logistics_score,
            "order_composite":       self.order_composite,
            "has_delivery_risk":     self.has_delivery_risk,
            "requires_client_alert": self.requires_client_alert,
            "estimated_delay_days":  self.estimated_delay_days,
            "order_signal":          self.order_signal,
        }


class OrderManagementIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[OrderResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _fulfillment_score(self, inp: OrderInput) -> float:
        score = 0.0

        if inp.days_past_promise_date >= 10:
            score += 40.0
        elif inp.days_past_promise_date >= 5:
            score += 22.0
        elif inp.days_past_promise_date >= 2:
            score += 8.0

        if inp.order_completion_pct <= 0.30:
            score += 35.0
        elif inp.order_completion_pct <= 0.60:
            score += 18.0
        elif inp.order_completion_pct <= 0.80:
            score += 6.0

        if inp.warehouse_processing_delay_days >= 5:
            score += 25.0
        elif inp.warehouse_processing_delay_days >= 2:
            score += 12.0

        return min(score, 100.0)

    def _inventory_score(self, inp: OrderInput) -> float:
        score = 0.0

        if inp.inventory_availability_pct <= 0.30:
            score += 40.0
        elif inp.inventory_availability_pct <= 0.55:
            score += 22.0
        elif inp.inventory_availability_pct <= 0.75:
            score += 8.0

        if inp.backorder_item_count >= 8:
            score += 35.0
        elif inp.backorder_item_count >= 4:
            score += 18.0
        elif inp.backorder_item_count >= 1:
            score += 6.0

        if inp.supplier_on_time_rate_pct <= 0.50:
            score += 25.0
        elif inp.supplier_on_time_rate_pct <= 0.70:
            score += 12.0

        return min(score, 100.0)

    def _quality_score(self, inp: OrderInput) -> float:
        score = 0.0

        if inp.quality_hold_count >= 5:
            score += 45.0
        elif inp.quality_hold_count >= 2:
            score += 25.0
        elif inp.quality_hold_count >= 1:
            score += 10.0

        if inp.quality_rejection_rate_pct >= 0.15:
            score += 30.0
        elif inp.quality_rejection_rate_pct >= 0.05:
            score += 15.0

        if inp.contract_sla_breach_count >= 3:
            score += 25.0
        elif inp.contract_sla_breach_count >= 1:
            score += 12.0

        return min(score, 100.0)

    def _logistics_score(self, inp: OrderInput) -> float:
        score = 0.0

        if inp.transit_delay_days >= 10:
            score += 40.0
        elif inp.transit_delay_days >= 5:
            score += 22.0
        elif inp.transit_delay_days >= 2:
            score += 8.0

        if inp.carrier_performance_score <= 0.40:
            score += 35.0
        elif inp.carrier_performance_score <= 0.65:
            score += 18.0
        elif inp.carrier_performance_score <= 0.80:
            score += 6.0

        if inp.customs_clearance_days >= 10:
            score += 25.0
        elif inp.customs_clearance_days >= 5:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: OrderInput) -> OrderPattern:
        if inp.days_past_promise_date >= 7 and inp.order_completion_pct <= 0.60:
            return OrderPattern.fulfillment_delay
        if inp.inventory_availability_pct <= 0.40 and inp.backorder_item_count >= 3:
            return OrderPattern.inventory_shortage
        if inp.supplier_on_time_rate_pct <= 0.55 and inp.backorder_item_count >= 4:
            return OrderPattern.supplier_failure
        if inp.quality_hold_count >= 3 and inp.quality_rejection_rate_pct >= 0.10:
            return OrderPattern.quality_hold
        if inp.transit_delay_days >= 7 and inp.carrier_performance_score <= 0.55:
            return OrderPattern.logistics_bottleneck
        return OrderPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> OrderRisk:
        if composite >= 60:
            return OrderRisk.critical
        if composite >= 40:
            return OrderRisk.high
        if composite >= 20:
            return OrderRisk.moderate
        return OrderRisk.low

    def _severity(self, composite: float) -> OrderSeverity:
        if composite >= 60:
            return OrderSeverity.blocked
        if composite >= 40:
            return OrderSeverity.delayed
        if composite >= 20:
            return OrderSeverity.at_risk
        return OrderSeverity.on_schedule

    def _action(self, risk: OrderRisk, pattern: OrderPattern) -> OrderAction:
        if risk == OrderRisk.critical:
            if pattern in (OrderPattern.fulfillment_delay, OrderPattern.inventory_shortage):
                return OrderAction.emergency_procurement
            return OrderAction.customer_notification
        if risk == OrderRisk.high:
            if pattern == OrderPattern.fulfillment_delay:
                return OrderAction.expedite_fulfillment
            if pattern == OrderPattern.inventory_shortage:
                return OrderAction.inventory_reallocation
            if pattern == OrderPattern.supplier_failure:
                return OrderAction.supplier_escalation
            if pattern == OrderPattern.quality_hold:
                return OrderAction.quality_inspection
            if pattern == OrderPattern.logistics_bottleneck:
                return OrderAction.logistics_rerouting
            return OrderAction.order_monitoring
        if risk == OrderRisk.moderate:
            return OrderAction.customer_notification
        return OrderAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_delivery_risk(self, composite: float, inp: OrderInput) -> bool:
        return (
            composite >= 40
            or inp.days_past_promise_date >= 5
            or inp.inventory_availability_pct <= 0.50
        )

    def _requires_client_alert(self, composite: float, inp: OrderInput) -> bool:
        return (
            composite >= 25
            or inp.escalation_requested >= 0.5
            or inp.contract_sla_breach_count >= 1
        )

    # ------------------------------------------------------------------
    # Estimated delay days
    # ------------------------------------------------------------------

    def _estimated_delay_days(self, inp: OrderInput, composite: float) -> int:
        return max(0, round(
            (inp.days_past_promise_date + inp.transit_delay_days) * (composite / 100)
        ))

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: OrderInput, pattern: OrderPattern, composite: float) -> str:
        if composite < 20:
            return "Order fulfillment on track — inventory, quality and logistics within SLA benchmarks"
        label = pattern.value.replace("_", " ").capitalize() if pattern != OrderPattern.none else "Order at risk"
        return (
            f"{label} — {inp.days_past_promise_date}d past promise — "
            f"{round(inp.order_completion_pct * 100)}% complete — "
            f"${round(inp.order_value_usd / 1000)}k order — "
            f"composite {round(composite)}"
        )

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: OrderInput) -> OrderResult:
        fulfillment = round(self._fulfillment_score(inp), 1)
        inventory   = round(self._inventory_score(inp), 1)
        quality     = round(self._quality_score(inp), 1)
        logistics   = round(self._logistics_score(inp), 1)

        composite = min(
            round(
                fulfillment * 0.30
                + inventory * 0.25
                + quality   * 0.25
                + logistics * 0.20,
                2,
            ),
            100.0,
        )

        pattern  = self._detect_pattern(inp)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        delivery_risk  = self._has_delivery_risk(composite, inp)
        client_alert   = self._requires_client_alert(composite, inp)
        delay_days     = self._estimated_delay_days(inp, composite)
        signal         = self._signal(inp, pattern, composite)

        result = OrderResult(
            order_id=inp.order_id,
            region=inp.region,
            order_risk=risk,
            order_pattern=pattern,
            order_severity=severity,
            recommended_action=action,
            fulfillment_score=fulfillment,
            inventory_score=inventory,
            quality_score=quality,
            logistics_score=logistics,
            order_composite=composite,
            has_delivery_risk=delivery_risk,
            requires_client_alert=client_alert,
            estimated_delay_days=delay_days,
            order_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[OrderInput]) -> list[OrderResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                    0,
                "risk_counts":              {},
                "pattern_counts":           {},
                "severity_counts":          {},
                "action_counts":            {},
                "avg_order_composite":      0.0,
                "delivery_risk_count":      0,
                "client_alert_count":       0,
                "avg_fulfillment_score":    0.0,
                "avg_inventory_score":      0.0,
                "avg_quality_score":        0.0,
                "avg_logistics_score":      0.0,
                "avg_estimated_delay_days": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_ful = total_inv = total_qua = total_log = total_delay = 0.0

        for r in self._results:
            risk_counts[r.order_risk.value]          = risk_counts.get(r.order_risk.value, 0) + 1
            pattern_counts[r.order_pattern.value]    = pattern_counts.get(r.order_pattern.value, 0) + 1
            severity_counts[r.order_severity.value]  = severity_counts.get(r.order_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.order_composite
            total_ful   += r.fulfillment_score
            total_inv   += r.inventory_score
            total_qua   += r.quality_score
            total_log   += r.logistics_score
            total_delay += r.estimated_delay_days

        n = len(self._results)

        return {
            "total":                    n,
            "risk_counts":              risk_counts,
            "pattern_counts":           pattern_counts,
            "severity_counts":          severity_counts,
            "action_counts":            action_counts,
            "avg_order_composite":      round(total_comp / n, 1),
            "delivery_risk_count":      sum(1 for r in self._results if r.has_delivery_risk),
            "client_alert_count":       sum(1 for r in self._results if r.requires_client_alert),
            "avg_fulfillment_score":    round(total_ful / n, 1),
            "avg_inventory_score":      round(total_inv / n, 1),
            "avg_quality_score":        round(total_qua / n, 1),
            "avg_logistics_score":      round(total_log / n, 1),
            "avg_estimated_delay_days": round(total_delay / n, 1),
        }
