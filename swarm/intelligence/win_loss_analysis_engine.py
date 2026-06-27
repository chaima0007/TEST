"""
Win/Loss Analysis Intelligence Engine

Analyse les patterns de victoire et défaite commerciale pour identifier
les facteurs clés : prix, concurrence, relation, timing, adéquation produit.
"""

from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields
from enum import Enum
from typing import Optional


class WinLossRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class WinLossPattern(str, Enum):
    none = "none"
    price_sensitivity = "price_sensitivity"
    competitive_displacement = "competitive_displacement"
    relationship_deficit = "relationship_deficit"
    timing_mismatch = "timing_mismatch"
    product_fit_gap = "product_fit_gap"
    process_failure = "process_failure"


class WinLossSeverity(str, Enum):
    strong = "strong"
    improving = "improving"
    declining = "declining"
    at_risk = "at_risk"


class WinLossAction(str, Enum):
    maintain = "maintain"
    pricing_review = "pricing_review"
    competitive_enablement = "competitive_enablement"
    relationship_investment = "relationship_investment"
    timing_alignment = "timing_alignment"
    product_feedback_loop = "product_feedback_loop"


@dataclass
class WinLossInput:
    total_deals_analyzed: int = 50
    won_deals: int = 25
    lost_to_price: int = 8
    lost_to_competitor: int = 6
    lost_to_no_decision: int = 4
    lost_product_fit: int = 3
    lost_relationship: int = 2
    lost_timing: int = 2
    avg_sales_cycle_won: float = 45.0
    avg_sales_cycle_lost: float = 65.0
    avg_deal_value_won: float = 30000.0
    avg_deal_value_lost: float = 28000.0
    competitor_mentioned_pct: float = 40.0
    top_competitor_win_rate_vs: float = 45.0
    discount_rate_won_avg: float = 8.0
    discount_rate_lost_avg: float = 5.0
    champion_present_won_pct: float = 80.0
    champion_present_lost_pct: float = 30.0
    executive_sponsor_won_pct: float = 70.0
    executive_sponsor_lost_pct: float = 25.0
    num_competitors_tracked: int = 5
    quarter: str = "Q1"


@dataclass
class WinLossResult:
    composite_score: float
    risk: WinLossRisk
    pattern: WinLossPattern
    severity: WinLossSeverity
    action: WinLossAction
    win_rate_score: float
    competitive_score: float
    relationship_score: float
    process_efficiency_score: float
    win_rate_pct: float
    primary_loss_reason: str
    estimated_recoverable_revenue: float
    signal: str
    champion_impact_delta: float
    price_sensitivity_index: float

    def to_dict(self) -> dict:
        return {
            "composite_score": self.composite_score,
            "risk": self.risk.value,
            "pattern": self.pattern.value,
            "severity": self.severity.value,
            "action": self.action.value,
            "win_rate_score": self.win_rate_score,
            "competitive_score": self.competitive_score,
            "relationship_score": self.relationship_score,
            "process_efficiency_score": self.process_efficiency_score,
            "win_rate_pct": self.win_rate_pct,
            "primary_loss_reason": self.primary_loss_reason,
            "estimated_recoverable_revenue": self.estimated_recoverable_revenue,
            "signal": self.signal,
            "champion_impact_delta": self.champion_impact_delta,
            "price_sensitivity_index": self.price_sensitivity_index,
        }


class WinLossAnalysisEngine:

    def _win_rate_score(self, inp: WinLossInput) -> float:
        if inp.total_deals_analyzed == 0:
            return 0.0
        win_rate = inp.won_deals / inp.total_deals_analyzed
        raw = win_rate * 100
        return min(max(round(raw, 1), 0.0), 100.0)

    def _competitive_score(self, inp: WinLossInput) -> float:
        win_rate_vs = min(inp.top_competitor_win_rate_vs, 100.0)
        competitor_exposure = min(inp.competitor_mentioned_pct / 100, 1.0)
        raw = win_rate_vs - (competitor_exposure * 20) + (inp.num_competitors_tracked * 2)
        return min(max(round(raw, 1), 0.0), 100.0)

    def _relationship_score(self, inp: WinLossInput) -> float:
        champion_delta = inp.champion_present_won_pct - inp.champion_present_lost_pct
        exec_delta = inp.executive_sponsor_won_pct - inp.executive_sponsor_lost_pct
        raw = (champion_delta * 0.5) + (exec_delta * 0.5)
        return min(max(round(raw, 1), 0.0), 100.0)

    def _process_efficiency_score(self, inp: WinLossInput) -> float:
        if inp.avg_sales_cycle_lost == 0:
            return 50.0
        cycle_ratio = inp.avg_sales_cycle_won / inp.avg_sales_cycle_lost
        efficiency = (1 - cycle_ratio) * 100 + 50
        return min(max(round(efficiency, 1), 0.0), 100.0)

    def _composite(self, w: float, c: float, r: float, p: float) -> float:
        return min(round(w * 0.40 + c * 0.25 + r * 0.20 + p * 0.15, 1), 100.0)

    def _risk_level(self, score: float) -> WinLossRisk:
        if score >= 60:
            return WinLossRisk.low
        if score >= 45:
            return WinLossRisk.moderate
        if score >= 30:
            return WinLossRisk.high
        return WinLossRisk.critical

    def _severity(self, risk: WinLossRisk) -> WinLossSeverity:
        return {
            WinLossRisk.low: WinLossSeverity.strong,
            WinLossRisk.moderate: WinLossSeverity.improving,
            WinLossRisk.high: WinLossSeverity.declining,
            WinLossRisk.critical: WinLossSeverity.at_risk,
        }[risk]

    def _primary_loss_reason(self, inp: WinLossInput) -> str:
        losses = {
            "price": inp.lost_to_price,
            "competitor": inp.lost_to_competitor,
            "no_decision": inp.lost_to_no_decision,
            "product_fit": inp.lost_product_fit,
            "relationship": inp.lost_relationship,
            "timing": inp.lost_timing,
        }
        if all(v == 0 for v in losses.values()):
            return "none"
        return max(losses, key=losses.get)

    def _detect_pattern(self, inp: WinLossInput, primary: str) -> WinLossPattern:
        total_lost = inp.total_deals_analyzed - inp.won_deals
        if total_lost == 0:
            return WinLossPattern.none
        if primary == "price" and inp.lost_to_price / total_lost > 0.35:
            return WinLossPattern.price_sensitivity
        if primary == "competitor" and inp.lost_to_competitor / total_lost > 0.25:
            return WinLossPattern.competitive_displacement
        if primary == "relationship" and inp.champion_present_won_pct - inp.champion_present_lost_pct > 40:
            return WinLossPattern.relationship_deficit
        if primary == "timing" and inp.avg_sales_cycle_lost > inp.avg_sales_cycle_won * 1.3:
            return WinLossPattern.timing_mismatch
        if primary == "product_fit":
            return WinLossPattern.product_fit_gap
        if inp.avg_sales_cycle_lost > inp.avg_sales_cycle_won * 1.5:
            return WinLossPattern.process_failure
        return WinLossPattern.none

    def _action(self, pattern: WinLossPattern) -> WinLossAction:
        mapping = {
            WinLossPattern.price_sensitivity: WinLossAction.pricing_review,
            WinLossPattern.competitive_displacement: WinLossAction.competitive_enablement,
            WinLossPattern.relationship_deficit: WinLossAction.relationship_investment,
            WinLossPattern.timing_mismatch: WinLossAction.timing_alignment,
            WinLossPattern.product_fit_gap: WinLossAction.product_feedback_loop,
            WinLossPattern.process_failure: WinLossAction.relationship_investment,
            WinLossPattern.none: WinLossAction.maintain,
        }
        return mapping[pattern]

    def _estimated_recoverable_revenue(self, inp: WinLossInput) -> float:
        total_lost = inp.total_deals_analyzed - inp.won_deals
        recoverable_pct = 0.30
        return round(total_lost * inp.avg_deal_value_lost * recoverable_pct, 2)

    def _signal(self, risk: WinLossRisk, pattern: WinLossPattern, win_rate: float) -> str:
        if risk == WinLossRisk.low and pattern == WinLossPattern.none:
            return f"Win/loss profile healthy — {win_rate:.0f}% win rate with no dominant loss pattern"
        signals = {
            WinLossPattern.price_sensitivity: "Price is primary loss driver — pricing strategy or value communication review needed",
            WinLossPattern.competitive_displacement: "Competitor displacement pattern — battlecard refresh and competitive enablement required",
            WinLossPattern.relationship_deficit: "Champion and executive sponsor gap explains most losses — relationship investment critical",
            WinLossPattern.timing_mismatch: "Timing misalignment driving losses — improve urgency creation and budget cycle alignment",
            WinLossPattern.product_fit_gap: "Product fit issues causing losses — feed insights to product team immediately",
            WinLossPattern.process_failure: "Process inefficiency detected — won deals close 50% faster than lost deals",
            WinLossPattern.none: f"Win/loss {risk.value} risk — win rate {win_rate:.0f}%, monitor trends",
        }
        return signals.get(pattern, "Win/loss analysis requires attention")

    def assess(self, inp: WinLossInput) -> WinLossResult:
        w = self._win_rate_score(inp)
        c = self._competitive_score(inp)
        r = self._relationship_score(inp)
        p = self._process_efficiency_score(inp)
        composite = self._composite(w, c, r, p)
        risk = self._risk_level(composite)
        severity = self._severity(risk)
        primary = self._primary_loss_reason(inp)
        pattern = self._detect_pattern(inp, primary)
        action = self._action(pattern)

        win_rate_pct = round(
            inp.won_deals / max(inp.total_deals_analyzed, 1) * 100, 1
        )
        champion_delta = round(inp.champion_present_won_pct - inp.champion_present_lost_pct, 1)
        price_sensitivity = round(
            inp.lost_to_price / max(inp.total_deals_analyzed - inp.won_deals, 1) * 100, 1
        )

        return WinLossResult(
            composite_score=composite,
            risk=risk,
            pattern=pattern,
            severity=severity,
            action=action,
            win_rate_score=w,
            competitive_score=c,
            relationship_score=r,
            process_efficiency_score=p,
            win_rate_pct=win_rate_pct,
            primary_loss_reason=primary,
            estimated_recoverable_revenue=self._estimated_recoverable_revenue(inp),
            signal=self._signal(risk, pattern, win_rate_pct),
            champion_impact_delta=champion_delta,
            price_sensitivity_index=price_sensitivity,
        )

    def batch(self, inputs: list[WinLossInput]) -> list[WinLossResult]:
        return [self.assess(inp) for inp in inputs]

    def summary(self, results: list[WinLossResult]) -> dict:
        if not results:
            return {}
        scores = [r.composite_score for r in results]
        return {
            "total_analyses": len(results),
            "avg_composite_score": round(sum(scores) / len(scores), 1),
            "avg_win_rate_pct": round(sum(r.win_rate_pct for r in results) / len(results), 1),
            "critical_count": sum(1 for r in results if r.risk == WinLossRisk.critical),
            "high_risk_count": sum(1 for r in results if r.risk == WinLossRisk.high),
            "top_pattern": max(set(r.pattern.value for r in results), key=lambda p: sum(1 for r in results if r.pattern.value == p)),
            "total_recoverable_revenue": round(sum(r.estimated_recoverable_revenue for r in results), 2),
            "avg_champion_delta": round(sum(r.champion_impact_delta for r in results) / len(results), 1),
            "price_sensitive_count": sum(1 for r in results if r.pattern == WinLossPattern.price_sensitivity),
            "competitive_threat_count": sum(1 for r in results if r.pattern == WinLossPattern.competitive_displacement),
            "min_score": min(scores),
            "max_score": max(scores),
            "low_risk_pct": round(sum(1 for r in results if r.risk == WinLossRisk.low) / len(results) * 100, 1),
        }
