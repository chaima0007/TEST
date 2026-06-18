from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AttributionModel(str, Enum):
    FIRST_TOUCH = "first_touch"
    LAST_TOUCH = "last_touch"
    LINEAR = "linear"
    TIME_DECAY = "time_decay"
    POSITION_BASED = "position_based"


class ChannelType(str, Enum):
    OUTBOUND_EMAIL = "outbound_email"
    INBOUND_CONTENT = "inbound_content"
    PAID_ADS = "paid_ads"
    SOCIAL_SELLING = "social_selling"
    REFERRAL = "referral"
    EVENT = "event"
    SDR_CALL = "sdr_call"
    PARTNER = "partner"


class RevenueRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class OptimizationAction(str, Enum):
    SCALE_UP = "scale_up"
    MAINTAIN = "maintain"
    OPTIMIZE = "optimize"
    REDUCE = "reduce"
    REALLOCATE = "reallocate"


@dataclass
class AttributionTouchpoint:
    channel: ChannelType
    days_before_close: int    # how many days before deal close this touch occurred
    is_first_touch: bool
    is_last_touch: bool
    campaign_id: str


@dataclass
class RevenueAttributionInput:
    deal_id: str
    account_id: str
    rep_id: str
    deal_value: float
    total_touchpoints: int
    touchpoints: list[AttributionTouchpoint]
    attribution_model: AttributionModel
    sales_cycle_days: int
    avg_cycle_days: float             # benchmark for this segment
    channel_spend: dict[str, float]   # {channel: cost_spent}
    pipeline_created: float           # total pipeline from these touches
    closed_won_value: float
    closed_lost_value: float
    segment: str                      # "smb", "mid_market", "enterprise"
    industry: str
    is_self_sourced: bool             # rep sourced without marketing
    marketing_qualified: bool
    sales_accepted: bool
    referral_source: str              # "customer", "partner", "none"


@dataclass
class RevenueAttributionResult:
    deal_id: str
    account_id: str
    rep_id: str
    attributed_revenue: float
    attribution_model: AttributionModel
    channel_credits: dict[str, float]   # {channel: credited_amount}
    roi_by_channel: dict[str, float]    # {channel: ROI ratio}
    revenue_risk: RevenueRisk
    optimization_action: OptimizationAction
    top_channel: str
    attribution_efficiency: float       # 0–100
    pipeline_to_revenue_ratio: float
    cost_per_acquisition: float
    cycle_efficiency: float             # 0–100 (100 = at benchmark)
    is_high_value: bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                    self.deal_id,
            "account_id":                 self.account_id,
            "attributed_revenue":         self.attributed_revenue,
            "attribution_model":          self.attribution_model.value,
            "channel_credits":            self.channel_credits,
            "roi_by_channel":             self.roi_by_channel,
            "revenue_risk":               self.revenue_risk.value,
            "optimization_action":        self.optimization_action.value,
            "top_channel":                self.top_channel,
            "attribution_efficiency":     self.attribution_efficiency,
            "pipeline_to_revenue_ratio":  self.pipeline_to_revenue_ratio,
            "cost_per_acquisition":       self.cost_per_acquisition,
            "cycle_efficiency":           self.cycle_efficiency,
            "is_high_value":              self.is_high_value,
            "rep_id":                     self.rep_id,
        }


class RevenueAttributionEngine:
    def __init__(self) -> None:
        self._results: list[RevenueAttributionResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: RevenueAttributionInput) -> RevenueAttributionResult:
        credits    = self._channel_credits(inp)
        roi        = self._roi_by_channel(inp, credits)
        top_ch     = max(credits, key=lambda k: credits[k]) if credits else "unknown"
        attr_eff   = self._attribution_efficiency(inp, credits)
        ptr        = self._pipeline_to_revenue_ratio(inp)
        cpa        = self._cost_per_acquisition(inp)
        cycle_eff  = self._cycle_efficiency(inp)
        risk       = self._revenue_risk(inp, attr_eff, cycle_eff)
        action     = self._optimization_action(inp, attr_eff, roi, risk)
        high_val   = inp.deal_value >= self._high_value_threshold(inp.segment)

        result = RevenueAttributionResult(
            deal_id=inp.deal_id,
            account_id=inp.account_id,
            rep_id=inp.rep_id,
            attributed_revenue=round(inp.closed_won_value, 2),
            attribution_model=inp.attribution_model,
            channel_credits=credits,
            roi_by_channel=roi,
            revenue_risk=risk,
            optimization_action=action,
            top_channel=top_ch,
            attribution_efficiency=attr_eff,
            pipeline_to_revenue_ratio=ptr,
            cost_per_acquisition=cpa,
            cycle_efficiency=cycle_eff,
            is_high_value=high_val,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[RevenueAttributionInput]
    ) -> list[RevenueAttributionResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def high_value_deals(self) -> list[RevenueAttributionResult]:
        return [r for r in self._results if r.is_high_value]

    @property
    def high_risk_revenue(self) -> list[RevenueAttributionResult]:
        return [r for r in self._results
                if r.revenue_risk in (RevenueRisk.HIGH, RevenueRisk.CRITICAL)]

    @property
    def scale_up_channels(self) -> list[RevenueAttributionResult]:
        return [r for r in self._results
                if r.optimization_action == OptimizationAction.SCALE_UP]

    @property
    def total_attributed_revenue(self) -> float:
        return round(sum(r.attributed_revenue for r in self._results), 2)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _channel_credits(self, inp: RevenueAttributionInput) -> dict[str, float]:
        if not inp.touchpoints or inp.closed_won_value <= 0:
            return {}

        value = inp.closed_won_value
        n     = len(inp.touchpoints)
        credits: dict[str, float] = {}

        if inp.attribution_model == AttributionModel.FIRST_TOUCH:
            for tp in inp.touchpoints:
                if tp.is_first_touch:
                    ch = tp.channel.value
                    credits[ch] = credits.get(ch, 0.0) + value
                    break

        elif inp.attribution_model == AttributionModel.LAST_TOUCH:
            for tp in reversed(inp.touchpoints):
                if tp.is_last_touch:
                    ch = tp.channel.value
                    credits[ch] = credits.get(ch, 0.0) + value
                    break

        elif inp.attribution_model == AttributionModel.LINEAR:
            share = value / n
            for tp in inp.touchpoints:
                ch = tp.channel.value
                credits[ch] = credits.get(ch, 0.0) + share

        elif inp.attribution_model == AttributionModel.TIME_DECAY:
            # More recent = more credit; weight = 1/days_before_close (min 1)
            weights = [1.0 / max(1, tp.days_before_close) for tp in inp.touchpoints]
            total_w = sum(weights)
            for tp, w in zip(inp.touchpoints, weights):
                ch = tp.channel.value
                credits[ch] = credits.get(ch, 0.0) + value * (w / total_w)

        elif inp.attribution_model == AttributionModel.POSITION_BASED:
            # 40% first, 40% last, 20% split among middle
            first_idx = next((i for i, t in enumerate(inp.touchpoints) if t.is_first_touch), 0)
            last_idx  = next((i for i in range(len(inp.touchpoints) - 1, -1, -1)
                              if inp.touchpoints[i].is_last_touch), n - 1)
            middle_indices = [i for i in range(n) if i != first_idx and i != last_idx]
            middle_share   = (0.20 * value / len(middle_indices)) if middle_indices else 0.0

            for i, tp in enumerate(inp.touchpoints):
                ch = tp.channel.value
                if i == first_idx:
                    credits[ch] = credits.get(ch, 0.0) + value * 0.40
                elif i == last_idx:
                    credits[ch] = credits.get(ch, 0.0) + value * 0.40
                else:
                    credits[ch] = credits.get(ch, 0.0) + middle_share

        return {ch: round(v, 2) for ch, v in credits.items()}

    def _roi_by_channel(
        self, inp: RevenueAttributionInput, credits: dict[str, float]
    ) -> dict[str, float]:
        roi: dict[str, float] = {}
        for ch, credit in credits.items():
            spend = inp.channel_spend.get(ch, 0.0)
            if spend > 0:
                roi[ch] = round(credit / spend, 2)
            else:
                roi[ch] = round(credit / max(1.0, credit * 0.05), 2)  # assume 5% cost if unknown
        return roi

    def _attribution_efficiency(
        self, inp: RevenueAttributionInput, credits: dict[str, float]
    ) -> float:
        if inp.pipeline_created <= 0:
            return 0.0
        win_rate = inp.closed_won_value / inp.pipeline_created
        # Base efficiency from win rate (50% win rate = 70 efficiency)
        efficiency = win_rate * 100 * 1.4
        # Boost for self-sourced
        if inp.is_self_sourced: efficiency += 5
        # Boost for referral
        if inp.referral_source != "none": efficiency += 8
        # MQL/SAL alignment
        if inp.marketing_qualified and inp.sales_accepted: efficiency += 5
        return round(max(0.0, min(100.0, efficiency)), 1)

    def _pipeline_to_revenue_ratio(self, inp: RevenueAttributionInput) -> float:
        if inp.pipeline_created <= 0:
            return 0.0
        return round(inp.closed_won_value / inp.pipeline_created, 3)

    def _cost_per_acquisition(self, inp: RevenueAttributionInput) -> float:
        total_spend = sum(inp.channel_spend.values())
        if total_spend <= 0 or inp.closed_won_value <= 0:
            return 0.0
        return round(total_spend / max(1, 1), 2)  # CPA per deal

    def _cycle_efficiency(self, inp: RevenueAttributionInput) -> float:
        if inp.avg_cycle_days <= 0:
            return 50.0
        ratio = inp.avg_cycle_days / max(1, inp.sales_cycle_days)
        efficiency = min(100.0, ratio * 70.0)
        return round(max(0.0, efficiency), 1)

    def _high_value_threshold(self, segment: str) -> float:
        return {"smb": 25_000, "mid_market": 75_000, "enterprise": 200_000}.get(
            segment, 50_000
        )

    def _revenue_risk(
        self, inp: RevenueAttributionInput, attr_eff: float, cycle_eff: float
    ) -> RevenueRisk:
        risk_score = 0
        if attr_eff < 30:          risk_score += 3
        elif attr_eff < 50:        risk_score += 1
        if cycle_eff < 30:         risk_score += 2
        elif cycle_eff < 50:       risk_score += 1
        if inp.closed_lost_value > inp.closed_won_value: risk_score += 2
        if not inp.sales_accepted: risk_score += 1
        if inp.total_touchpoints > 15: risk_score += 1

        if risk_score >= 6: return RevenueRisk.CRITICAL
        if risk_score >= 4: return RevenueRisk.HIGH
        if risk_score >= 2: return RevenueRisk.MEDIUM
        return RevenueRisk.LOW

    def _optimization_action(
        self,
        inp: RevenueAttributionInput,
        attr_eff: float,
        roi: dict[str, float],
        risk: RevenueRisk,
    ) -> OptimizationAction:
        if risk == RevenueRisk.CRITICAL:
            return OptimizationAction.REALLOCATE
        avg_roi = sum(roi.values()) / max(1, len(roi))
        if avg_roi >= 5.0 and attr_eff >= 70:
            return OptimizationAction.SCALE_UP
        if attr_eff >= 60:
            return OptimizationAction.MAINTAIN
        if attr_eff >= 40:
            return OptimizationAction.OPTIMIZE
        if risk == RevenueRisk.HIGH:
            return OptimizationAction.REDUCE
        return OptimizationAction.OPTIMIZE

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total": 0,
                "model_counts": {},
                "risk_counts": {},
                "action_counts": {},
                "top_channel_counts": {},
                "total_attributed_revenue": 0.0,
                "avg_attribution_efficiency": 0.0,
                "avg_pipeline_to_revenue_ratio": 0.0,
                "avg_cycle_efficiency": 0.0,
                "high_value_count": 0,
                "high_risk_count": 0,
                "scale_up_count": 0,
                "avg_cost_per_acquisition": 0.0,
            }

        model_counts:   dict[str, int] = {}
        risk_counts:    dict[str, int] = {}
        action_counts:  dict[str, int] = {}
        top_ch_counts:  dict[str, int] = {}
        total_rev  = 0.0
        total_eff  = 0.0
        total_ptr  = 0.0
        total_cyc  = 0.0
        total_cpa  = 0.0

        for r in self._results:
            model_counts[r.attribution_model.value]  = model_counts.get(r.attribution_model.value, 0) + 1
            risk_counts[r.revenue_risk.value]        = risk_counts.get(r.revenue_risk.value, 0) + 1
            action_counts[r.optimization_action.value] = action_counts.get(r.optimization_action.value, 0) + 1
            top_ch_counts[r.top_channel]             = top_ch_counts.get(r.top_channel, 0) + 1
            total_rev  += r.attributed_revenue
            total_eff  += r.attribution_efficiency
            total_ptr  += r.pipeline_to_revenue_ratio
            total_cyc  += r.cycle_efficiency
            total_cpa  += r.cost_per_acquisition

        return {
            "total":                        n,
            "model_counts":                 model_counts,
            "risk_counts":                  risk_counts,
            "action_counts":                action_counts,
            "top_channel_counts":           top_ch_counts,
            "total_attributed_revenue":     round(total_rev, 2),
            "avg_attribution_efficiency":   round(total_eff / n, 1),
            "avg_pipeline_to_revenue_ratio": round(total_ptr / n, 3),
            "avg_cycle_efficiency":         round(total_cyc / n, 1),
            "high_value_count":             len(self.high_value_deals),
            "high_risk_count":              len(self.high_risk_revenue),
            "scale_up_count":               len(self.scale_up_channels),
            "avg_cost_per_acquisition":     round(total_cpa / n, 2),
        }
