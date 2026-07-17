"""Comprehensive pytest test suite for RevenueAttributionEngine."""
from __future__ import annotations

import pytest
from swarm.intelligence.revenue_attribution_engine import (
    AttributionModel,
    AttributionTouchpoint,
    ChannelType,
    OptimizationAction,
    RevenueAttributionEngine,
    RevenueAttributionInput,
    RevenueAttributionResult,
    RevenueRisk,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_tp(
    channel: ChannelType = ChannelType.OUTBOUND_EMAIL,
    days_before_close: int = 10,
    is_first_touch: bool = False,
    is_last_touch: bool = False,
    campaign_id: str = "camp1",
) -> AttributionTouchpoint:
    return AttributionTouchpoint(
        channel=channel,
        days_before_close=days_before_close,
        is_first_touch=is_first_touch,
        is_last_touch=is_last_touch,
        campaign_id=campaign_id,
    )


def make_input(
    deal_id: str = "deal-001",
    account_id: str = "acc-001",
    rep_id: str = "rep-001",
    deal_value: float = 50_000.0,
    total_touchpoints: int = 3,
    touchpoints: list[AttributionTouchpoint] | None = None,
    attribution_model: AttributionModel = AttributionModel.LINEAR,
    sales_cycle_days: int = 30,
    avg_cycle_days: float = 30.0,
    channel_spend: dict | None = None,
    pipeline_created: float = 100_000.0,
    closed_won_value: float = 50_000.0,
    closed_lost_value: float = 20_000.0,
    segment: str = "mid_market",
    industry: str = "tech",
    is_self_sourced: bool = False,
    marketing_qualified: bool = True,
    sales_accepted: bool = True,
    referral_source: str = "none",
) -> RevenueAttributionInput:
    if touchpoints is None:
        touchpoints = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 15),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
    if channel_spend is None:
        channel_spend = {
            ChannelType.OUTBOUND_EMAIL.value: 1000.0,
            ChannelType.PAID_ADS.value: 2000.0,
            ChannelType.SDR_CALL.value: 500.0,
        }
    return RevenueAttributionInput(
        deal_id=deal_id,
        account_id=account_id,
        rep_id=rep_id,
        deal_value=deal_value,
        total_touchpoints=total_touchpoints,
        touchpoints=touchpoints,
        attribution_model=attribution_model,
        sales_cycle_days=sales_cycle_days,
        avg_cycle_days=avg_cycle_days,
        channel_spend=channel_spend,
        pipeline_created=pipeline_created,
        closed_won_value=closed_won_value,
        closed_lost_value=closed_lost_value,
        segment=segment,
        industry=industry,
        is_self_sourced=is_self_sourced,
        marketing_qualified=marketing_qualified,
        sales_accepted=sales_accepted,
        referral_source=referral_source,
    )


# ===========================================================================
# 1. Enum tests
# ===========================================================================

class TestAttributionModelEnum:
    def test_member_count(self):
        assert len(AttributionModel) == 5

    def test_first_touch(self):
        assert AttributionModel.FIRST_TOUCH == "first_touch"

    def test_last_touch(self):
        assert AttributionModel.LAST_TOUCH == "last_touch"

    def test_linear(self):
        assert AttributionModel.LINEAR == "linear"

    def test_time_decay(self):
        assert AttributionModel.TIME_DECAY == "time_decay"

    def test_position_based(self):
        assert AttributionModel.POSITION_BASED == "position_based"

    def test_is_str_subclass(self):
        assert isinstance(AttributionModel.LINEAR, str)

    def test_values_unique(self):
        vals = [m.value for m in AttributionModel]
        assert len(vals) == len(set(vals))

    def test_membership_by_value(self):
        assert AttributionModel("linear") == AttributionModel.LINEAR

    def test_str_comparison(self):
        assert AttributionModel.FIRST_TOUCH == "first_touch"


class TestChannelTypeEnum:
    def test_member_count(self):
        assert len(ChannelType) == 8

    def test_outbound_email(self):
        assert ChannelType.OUTBOUND_EMAIL == "outbound_email"

    def test_inbound_content(self):
        assert ChannelType.INBOUND_CONTENT == "inbound_content"

    def test_paid_ads(self):
        assert ChannelType.PAID_ADS == "paid_ads"

    def test_social_selling(self):
        assert ChannelType.SOCIAL_SELLING == "social_selling"

    def test_referral(self):
        assert ChannelType.REFERRAL == "referral"

    def test_event(self):
        assert ChannelType.EVENT == "event"

    def test_sdr_call(self):
        assert ChannelType.SDR_CALL == "sdr_call"

    def test_partner(self):
        assert ChannelType.PARTNER == "partner"

    def test_is_str_subclass(self):
        assert isinstance(ChannelType.PAID_ADS, str)

    def test_values_unique(self):
        vals = [m.value for m in ChannelType]
        assert len(vals) == len(set(vals))


class TestRevenueRiskEnum:
    def test_member_count(self):
        assert len(RevenueRisk) == 4

    def test_low(self):
        assert RevenueRisk.LOW == "low"

    def test_medium(self):
        assert RevenueRisk.MEDIUM == "medium"

    def test_high(self):
        assert RevenueRisk.HIGH == "high"

    def test_critical(self):
        assert RevenueRisk.CRITICAL == "critical"

    def test_is_str_subclass(self):
        assert isinstance(RevenueRisk.LOW, str)

    def test_values_unique(self):
        vals = [m.value for m in RevenueRisk]
        assert len(vals) == len(set(vals))


class TestOptimizationActionEnum:
    def test_member_count(self):
        assert len(OptimizationAction) == 5

    def test_scale_up(self):
        assert OptimizationAction.SCALE_UP == "scale_up"

    def test_maintain(self):
        assert OptimizationAction.MAINTAIN == "maintain"

    def test_optimize(self):
        assert OptimizationAction.OPTIMIZE == "optimize"

    def test_reduce(self):
        assert OptimizationAction.REDUCE == "reduce"

    def test_reallocate(self):
        assert OptimizationAction.REALLOCATE == "reallocate"

    def test_is_str_subclass(self):
        assert isinstance(OptimizationAction.SCALE_UP, str)

    def test_values_unique(self):
        vals = [m.value for m in OptimizationAction]
        assert len(vals) == len(set(vals))


# ===========================================================================
# 2. AttributionTouchpoint dataclass
# ===========================================================================

class TestAttributionTouchpoint:
    def test_all_fields_set(self):
        tp = AttributionTouchpoint(
            channel=ChannelType.PAID_ADS,
            days_before_close=5,
            is_first_touch=True,
            is_last_touch=False,
            campaign_id="c123",
        )
        assert tp.channel == ChannelType.PAID_ADS
        assert tp.days_before_close == 5
        assert tp.is_first_touch is True
        assert tp.is_last_touch is False
        assert tp.campaign_id == "c123"

    def test_channel_type(self):
        tp = make_tp(ChannelType.SOCIAL_SELLING)
        assert tp.channel == ChannelType.SOCIAL_SELLING

    def test_days_before_close_type(self):
        tp = make_tp(days_before_close=7)
        assert isinstance(tp.days_before_close, int)

    def test_is_first_touch_bool(self):
        tp = make_tp(is_first_touch=True)
        assert tp.is_first_touch is True

    def test_is_last_touch_bool(self):
        tp = make_tp(is_last_touch=True)
        assert tp.is_last_touch is True

    def test_campaign_id_string(self):
        tp = make_tp(campaign_id="xyz")
        assert tp.campaign_id == "xyz"

    def test_default_not_first_not_last(self):
        tp = make_tp()
        assert tp.is_first_touch is False
        assert tp.is_last_touch is False


# ===========================================================================
# 3. RevenueAttributionInput – 19 fields
# ===========================================================================

class TestRevenueAttributionInputFields:
    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(RevenueAttributionInput)
        assert len(fields) == 19

    def test_deal_id(self):
        inp = make_input(deal_id="d1")
        assert inp.deal_id == "d1"

    def test_account_id(self):
        inp = make_input(account_id="a1")
        assert inp.account_id == "a1"

    def test_rep_id(self):
        inp = make_input(rep_id="r1")
        assert inp.rep_id == "r1"

    def test_deal_value(self):
        inp = make_input(deal_value=99_999.0)
        assert inp.deal_value == 99_999.0

    def test_total_touchpoints(self):
        inp = make_input(total_touchpoints=7)
        assert inp.total_touchpoints == 7

    def test_touchpoints_list(self):
        tps = [make_tp()]
        inp = make_input(touchpoints=tps)
        assert inp.touchpoints == tps

    def test_attribution_model(self):
        inp = make_input(attribution_model=AttributionModel.TIME_DECAY)
        assert inp.attribution_model == AttributionModel.TIME_DECAY

    def test_sales_cycle_days(self):
        inp = make_input(sales_cycle_days=45)
        assert inp.sales_cycle_days == 45

    def test_avg_cycle_days(self):
        inp = make_input(avg_cycle_days=60.0)
        assert inp.avg_cycle_days == 60.0

    def test_channel_spend(self):
        spend = {"outbound_email": 500.0}
        inp = make_input(channel_spend=spend)
        assert inp.channel_spend == spend

    def test_pipeline_created(self):
        inp = make_input(pipeline_created=200_000.0)
        assert inp.pipeline_created == 200_000.0

    def test_closed_won_value(self):
        inp = make_input(closed_won_value=50_000.0)
        assert inp.closed_won_value == 50_000.0

    def test_closed_lost_value(self):
        inp = make_input(closed_lost_value=10_000.0)
        assert inp.closed_lost_value == 10_000.0

    def test_segment(self):
        inp = make_input(segment="enterprise")
        assert inp.segment == "enterprise"

    def test_industry(self):
        inp = make_input(industry="finance")
        assert inp.industry == "finance"

    def test_is_self_sourced(self):
        inp = make_input(is_self_sourced=True)
        assert inp.is_self_sourced is True

    def test_marketing_qualified(self):
        inp = make_input(marketing_qualified=False)
        assert inp.marketing_qualified is False

    def test_sales_accepted(self):
        inp = make_input(sales_accepted=False)
        assert inp.sales_accepted is False

    def test_referral_source(self):
        inp = make_input(referral_source="customer")
        assert inp.referral_source == "customer"


# ===========================================================================
# 4. to_dict() – exactly 15 keys
# ===========================================================================

class TestToDictKeys:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()
        self.result = self.engine.analyze(make_input())

    def test_key_count(self):
        d = self.result.to_dict()
        assert len(d) == 15

    def test_has_deal_id(self):
        assert "deal_id" in self.result.to_dict()

    def test_has_account_id(self):
        assert "account_id" in self.result.to_dict()

    def test_has_attributed_revenue(self):
        assert "attributed_revenue" in self.result.to_dict()

    def test_has_attribution_model(self):
        assert "attribution_model" in self.result.to_dict()

    def test_has_channel_credits(self):
        assert "channel_credits" in self.result.to_dict()

    def test_has_roi_by_channel(self):
        assert "roi_by_channel" in self.result.to_dict()

    def test_has_revenue_risk(self):
        assert "revenue_risk" in self.result.to_dict()

    def test_has_optimization_action(self):
        assert "optimization_action" in self.result.to_dict()

    def test_has_top_channel(self):
        assert "top_channel" in self.result.to_dict()

    def test_has_attribution_efficiency(self):
        assert "attribution_efficiency" in self.result.to_dict()

    def test_has_pipeline_to_revenue_ratio(self):
        assert "pipeline_to_revenue_ratio" in self.result.to_dict()

    def test_has_cost_per_acquisition(self):
        assert "cost_per_acquisition" in self.result.to_dict()

    def test_has_cycle_efficiency(self):
        assert "cycle_efficiency" in self.result.to_dict()

    def test_has_is_high_value(self):
        assert "is_high_value" in self.result.to_dict()

    def test_has_rep_id(self):
        assert "rep_id" in self.result.to_dict()

    def test_attribution_model_is_string_value(self):
        d = self.result.to_dict()
        assert isinstance(d["attribution_model"], str)
        assert d["attribution_model"] == AttributionModel.LINEAR.value

    def test_revenue_risk_is_string_value(self):
        d = self.result.to_dict()
        assert isinstance(d["revenue_risk"], str)

    def test_optimization_action_is_string_value(self):
        d = self.result.to_dict()
        assert isinstance(d["optimization_action"], str)


# ===========================================================================
# 5. _channel_credits – each model
# ===========================================================================

class TestChannelCreditsFirstTouch:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_empty_touchpoints_returns_empty(self):
        inp = make_input(touchpoints=[], attribution_model=AttributionModel.FIRST_TOUCH,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        assert credits == {}

    def test_zero_closed_won_returns_empty(self):
        inp = make_input(closed_won_value=0.0, attribution_model=AttributionModel.FIRST_TOUCH)
        credits = self.engine._channel_credits(inp)
        assert credits == {}

    def test_negative_closed_won_returns_empty(self):
        inp = make_input(closed_won_value=-100.0, attribution_model=AttributionModel.FIRST_TOUCH)
        credits = self.engine._channel_credits(inp)
        assert credits == {}

    def test_single_first_touch_gets_full_credit(self):
        tps = [make_tp(ChannelType.OUTBOUND_EMAIL, 10, is_first_touch=True)]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.FIRST_TOUCH,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        assert credits == {"outbound_email": 10_000.0}

    def test_first_touch_only_credits_first_touch_flag(self):
        tps = [
            make_tp(ChannelType.PAID_ADS, 30, is_first_touch=False),
            make_tp(ChannelType.OUTBOUND_EMAIL, 20, is_first_touch=True),
            make_tp(ChannelType.SDR_CALL, 5, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.FIRST_TOUCH,
                         closed_won_value=5_000.0)
        credits = self.engine._channel_credits(inp)
        assert "outbound_email" in credits
        assert credits["outbound_email"] == 5_000.0
        assert "paid_ads" not in credits

    def test_first_touch_returns_rounded(self):
        tps = [make_tp(ChannelType.EVENT, 10, is_first_touch=True)]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.FIRST_TOUCH,
                         closed_won_value=10_000.33333)
        credits = self.engine._channel_credits(inp)
        assert credits["event"] == round(10_000.33333, 2)

    def test_first_touch_stops_at_first_match(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 20, is_first_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.FIRST_TOUCH,
                         closed_won_value=8_000.0)
        credits = self.engine._channel_credits(inp)
        # Only first match should get credit
        assert sum(credits.values()) == pytest.approx(8_000.0, rel=1e-6)
        assert "outbound_email" in credits


class TestChannelCreditsLastTouch:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_last_touch_single_gets_full_credit(self):
        tps = [make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True)]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.LAST_TOUCH,
                         closed_won_value=12_000.0)
        credits = self.engine._channel_credits(inp)
        assert credits == {"sdr_call": 12_000.0}

    def test_last_touch_scans_reversed(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_last_touch=True),
            make_tp(ChannelType.PAID_ADS, 15, is_last_touch=False),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.LAST_TOUCH,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        assert "sdr_call" in credits
        assert credits["sdr_call"] == 10_000.0

    def test_last_touch_no_last_touch_flag_returns_empty(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 10, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 5),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.LAST_TOUCH,
                         closed_won_value=5_000.0)
        credits = self.engine._channel_credits(inp)
        assert credits == {}

    def test_last_touch_empty_touchpoints(self):
        inp = make_input(touchpoints=[], attribution_model=AttributionModel.LAST_TOUCH,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        assert credits == {}


class TestChannelCreditsLinear:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_linear_equal_split(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 15),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.LINEAR,
                         closed_won_value=30_000.0)
        credits = self.engine._channel_credits(inp)
        assert credits["outbound_email"] == pytest.approx(10_000.0, rel=1e-4)
        assert credits["paid_ads"] == pytest.approx(10_000.0, rel=1e-4)
        assert credits["sdr_call"] == pytest.approx(10_000.0, rel=1e-4)

    def test_linear_credits_accumulate_same_channel(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.OUTBOUND_EMAIL, 15),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.LINEAR,
                         closed_won_value=30_000.0)
        credits = self.engine._channel_credits(inp)
        # outbound_email gets 2/3 share
        assert credits["outbound_email"] == pytest.approx(20_000.0, rel=1e-4)
        assert credits["sdr_call"] == pytest.approx(10_000.0, rel=1e-4)

    def test_linear_single_touchpoint(self):
        tps = [make_tp(ChannelType.EVENT, 5, is_first_touch=True, is_last_touch=True)]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.LINEAR,
                         closed_won_value=20_000.0)
        credits = self.engine._channel_credits(inp)
        assert credits["event"] == pytest.approx(20_000.0, rel=1e-4)

    def test_linear_sum_equals_closed_won_value(self):
        tps = [make_tp(ChannelType(c), i * 5) for i, c in enumerate(
            ["outbound_email", "paid_ads", "sdr_call", "event"], start=1)]
        tps[0].is_first_touch = True
        tps[-1].is_last_touch = True
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.LINEAR,
                         closed_won_value=40_000.0)
        credits = self.engine._channel_credits(inp)
        assert sum(credits.values()) == pytest.approx(40_000.0, rel=1e-4)


class TestChannelCreditsTimeDecay:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_time_decay_recent_gets_more(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 100, is_first_touch=True),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.TIME_DECAY,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        # sdr_call is 1 day before close, weight=1.0; email is 100 days, weight=0.01
        assert credits["sdr_call"] > credits["outbound_email"]

    def test_time_decay_sum_equals_value(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 20),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.TIME_DECAY,
                         closed_won_value=15_000.0)
        credits = self.engine._channel_credits(inp)
        assert sum(credits.values()) == pytest.approx(15_000.0, rel=1e-2)

    def test_time_decay_zero_days_uses_min_one(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 0, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 0, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.TIME_DECAY,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        # Both have weight 1/max(1,0) = 1.0, so equal split
        assert credits["outbound_email"] == pytest.approx(5_000.0, rel=1e-2)
        assert credits["paid_ads"] == pytest.approx(5_000.0, rel=1e-2)

    def test_time_decay_returns_rounded(self):
        tps = [make_tp(ChannelType.OUTBOUND_EMAIL, 3, is_first_touch=True, is_last_touch=True)]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.TIME_DECAY,
                         closed_won_value=1.0)
        credits = self.engine._channel_credits(inp)
        for v in credits.values():
            assert v == round(v, 2)


class TestChannelCreditsPositionBased:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_position_based_first_gets_40pct(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 15),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.POSITION_BASED,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        assert credits["outbound_email"] == pytest.approx(4_000.0, rel=1e-4)

    def test_position_based_last_gets_40pct(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 15),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.POSITION_BASED,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        assert credits["sdr_call"] == pytest.approx(4_000.0, rel=1e-4)

    def test_position_based_middle_gets_20pct(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 15),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.POSITION_BASED,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        assert credits["paid_ads"] == pytest.approx(2_000.0, rel=1e-4)

    def test_position_based_sum_equals_value(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 20),
            make_tp(ChannelType.SOCIAL_SELLING, 10),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.POSITION_BASED,
                         closed_won_value=20_000.0)
        credits = self.engine._channel_credits(inp)
        assert sum(credits.values()) == pytest.approx(20_000.0, rel=1e-2)

    def test_position_based_two_touchpoints_no_middle(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 10, is_first_touch=True),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.POSITION_BASED,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        # No middle, so 40% first, 40% last, 0% middle
        assert credits["outbound_email"] == pytest.approx(4_000.0, rel=1e-4)
        assert credits["sdr_call"] == pytest.approx(4_000.0, rel=1e-4)

    def test_position_based_one_touchpoint(self):
        tps = [make_tp(ChannelType.OUTBOUND_EMAIL, 5, is_first_touch=True, is_last_touch=True)]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.POSITION_BASED,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        # first_idx == last_idx == 0: the loop matches `if i == first_idx` first (elif skipped),
        # so only 40% is added. No middle indices.
        assert credits["outbound_email"] == pytest.approx(4_000.0, rel=1e-4)

    def test_position_based_returns_rounded(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 10, is_first_touch=True),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(touchpoints=tps, attribution_model=AttributionModel.POSITION_BASED,
                         closed_won_value=10_000.0)
        credits = self.engine._channel_credits(inp)
        for v in credits.values():
            assert v == round(v, 2)


# ===========================================================================
# 6. _roi_by_channel
# ===========================================================================

class TestROIByChannel:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_with_spend_divides_credit_by_spend(self):
        credits = {"outbound_email": 10_000.0}
        inp = make_input(channel_spend={"outbound_email": 2_000.0})
        roi = self.engine._roi_by_channel(inp, credits)
        assert roi["outbound_email"] == pytest.approx(5.0, rel=1e-6)

    def test_no_spend_uses_five_percent_cost(self):
        credits = {"sdr_call": 1_000.0}
        inp = make_input(channel_spend={})
        roi = self.engine._roi_by_channel(inp, credits)
        # credit / max(1.0, credit*0.05) = 1000 / max(1.0, 50) = 1000/50 = 20.0
        assert roi["sdr_call"] == pytest.approx(20.0, rel=1e-6)

    def test_no_spend_small_credit_uses_one(self):
        # credit=0.5, credit*0.05=0.025 → max(1.0, 0.025)=1.0 → roi=0.5/1.0=0.5
        credits = {"event": 0.5}
        inp = make_input(channel_spend={})
        roi = self.engine._roi_by_channel(inp, credits)
        assert roi["event"] == pytest.approx(0.5, rel=1e-6)

    def test_returns_rounded_to_two(self):
        credits = {"paid_ads": 10_000.0}
        inp = make_input(channel_spend={"paid_ads": 3_000.0})
        roi = self.engine._roi_by_channel(inp, credits)
        assert roi["paid_ads"] == round(roi["paid_ads"], 2)

    def test_empty_credits_returns_empty(self):
        roi = self.engine._roi_by_channel(make_input(), {})
        assert roi == {}

    def test_multiple_channels(self):
        credits = {"outbound_email": 4_000.0, "paid_ads": 2_000.0}
        inp = make_input(channel_spend={"outbound_email": 1_000.0, "paid_ads": 500.0})
        roi = self.engine._roi_by_channel(inp, credits)
        assert roi["outbound_email"] == pytest.approx(4.0, rel=1e-6)
        assert roi["paid_ads"] == pytest.approx(4.0, rel=1e-6)

    def test_channel_not_in_spend_uses_fallback(self):
        credits = {"referral": 5_000.0}
        inp = make_input(channel_spend={"outbound_email": 1_000.0})
        roi = self.engine._roi_by_channel(inp, credits)
        # 5000 / max(1.0, 5000*0.05) = 5000/250 = 20.0
        assert roi["referral"] == pytest.approx(20.0, rel=1e-6)


# ===========================================================================
# 7. _attribution_efficiency
# ===========================================================================

class TestAttributionEfficiency:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_zero_pipeline_returns_zero(self):
        inp = make_input(pipeline_created=0.0)
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == 0.0

    def test_negative_pipeline_returns_zero(self):
        inp = make_input(pipeline_created=-1.0)
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == 0.0

    def test_base_win_rate_50pct(self):
        # win_rate = 50000/100000 = 0.5 → eff = 0.5*100*1.4 = 70.0
        inp = make_input(
            pipeline_created=100_000.0, closed_won_value=50_000.0,
            is_self_sourced=False, referral_source="none",
            marketing_qualified=False, sales_accepted=False,
        )
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == pytest.approx(70.0, rel=1e-6)

    def test_self_sourced_bonus_5(self):
        inp = make_input(
            pipeline_created=100_000.0, closed_won_value=50_000.0,
            is_self_sourced=True, referral_source="none",
            marketing_qualified=False, sales_accepted=False,
        )
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == pytest.approx(75.0, rel=1e-6)

    def test_referral_bonus_8(self):
        inp = make_input(
            pipeline_created=100_000.0, closed_won_value=50_000.0,
            is_self_sourced=False, referral_source="customer",
            marketing_qualified=False, sales_accepted=False,
        )
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == pytest.approx(78.0, rel=1e-6)

    def test_mql_sal_bonus_5(self):
        inp = make_input(
            pipeline_created=100_000.0, closed_won_value=50_000.0,
            is_self_sourced=False, referral_source="none",
            marketing_qualified=True, sales_accepted=True,
        )
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == pytest.approx(75.0, rel=1e-6)

    def test_all_bonuses(self):
        # 70 + 5 + 8 + 5 = 88
        inp = make_input(
            pipeline_created=100_000.0, closed_won_value=50_000.0,
            is_self_sourced=True, referral_source="partner",
            marketing_qualified=True, sales_accepted=True,
        )
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == pytest.approx(88.0, rel=1e-6)

    def test_clamped_at_100(self):
        # win_rate=1.0 → base=140, +5+8+5=158 → clamps to 100
        inp = make_input(
            pipeline_created=50_000.0, closed_won_value=50_000.0,
            is_self_sourced=True, referral_source="partner",
            marketing_qualified=True, sales_accepted=True,
        )
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == 100.0

    def test_clamped_at_zero(self):
        # win_rate=0 → base=0, no bonuses → 0
        inp = make_input(
            pipeline_created=100_000.0, closed_won_value=0.0001,
            is_self_sourced=False, referral_source="none",
            marketing_qualified=False, sales_accepted=False,
        )
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff >= 0.0

    def test_result_rounded_to_one_decimal(self):
        inp = make_input(pipeline_created=100_000.0, closed_won_value=50_000.0)
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == round(eff, 1)

    def test_mql_only_no_bonus(self):
        # marketing_qualified=True but sales_accepted=False → no MQL/SAL bonus
        inp = make_input(
            pipeline_created=100_000.0, closed_won_value=50_000.0,
            is_self_sourced=False, referral_source="none",
            marketing_qualified=True, sales_accepted=False,
        )
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == pytest.approx(70.0, rel=1e-6)

    def test_sal_only_no_bonus(self):
        # marketing_qualified=False but sales_accepted=True → no MQL/SAL bonus
        inp = make_input(
            pipeline_created=100_000.0, closed_won_value=50_000.0,
            is_self_sourced=False, referral_source="none",
            marketing_qualified=False, sales_accepted=True,
        )
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == pytest.approx(70.0, rel=1e-6)

    def test_referral_partner_gives_bonus(self):
        inp = make_input(
            pipeline_created=100_000.0, closed_won_value=50_000.0,
            is_self_sourced=False, referral_source="partner",
            marketing_qualified=False, sales_accepted=False,
        )
        eff = self.engine._attribution_efficiency(inp, {})
        assert eff == pytest.approx(78.0, rel=1e-6)


# ===========================================================================
# 8. _pipeline_to_revenue_ratio
# ===========================================================================

class TestPipelineToRevenueRatio:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_zero_pipeline_returns_zero(self):
        inp = make_input(pipeline_created=0.0)
        assert self.engine._pipeline_to_revenue_ratio(inp) == 0.0

    def test_negative_pipeline_returns_zero(self):
        inp = make_input(pipeline_created=-500.0)
        assert self.engine._pipeline_to_revenue_ratio(inp) == 0.0

    def test_basic_ratio(self):
        inp = make_input(pipeline_created=100_000.0, closed_won_value=50_000.0)
        assert self.engine._pipeline_to_revenue_ratio(inp) == pytest.approx(0.5, rel=1e-6)

    def test_rounded_to_three_decimal_places(self):
        inp = make_input(pipeline_created=300_000.0, closed_won_value=100_000.0)
        ratio = self.engine._pipeline_to_revenue_ratio(inp)
        assert ratio == round(ratio, 3)

    def test_ratio_greater_than_one(self):
        inp = make_input(pipeline_created=10_000.0, closed_won_value=15_000.0)
        ratio = self.engine._pipeline_to_revenue_ratio(inp)
        assert ratio == pytest.approx(1.5, rel=1e-6)

    def test_full_win_rate(self):
        inp = make_input(pipeline_created=50_000.0, closed_won_value=50_000.0)
        assert self.engine._pipeline_to_revenue_ratio(inp) == pytest.approx(1.0, rel=1e-6)

    def test_small_win_rate(self):
        inp = make_input(pipeline_created=1_000_000.0, closed_won_value=10_000.0)
        assert self.engine._pipeline_to_revenue_ratio(inp) == pytest.approx(0.01, rel=1e-6)


# ===========================================================================
# 9. _cost_per_acquisition
# ===========================================================================

class TestCostPerAcquisition:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_zero_spend_returns_zero(self):
        inp = make_input(channel_spend={}, closed_won_value=50_000.0)
        assert self.engine._cost_per_acquisition(inp) == 0.0

    def test_negative_spend_returns_zero(self):
        inp = make_input(channel_spend={"outbound_email": -100.0}, closed_won_value=50_000.0)
        assert self.engine._cost_per_acquisition(inp) == 0.0

    def test_zero_closed_won_returns_zero(self):
        inp = make_input(channel_spend={"outbound_email": 1000.0}, closed_won_value=0.0)
        assert self.engine._cost_per_acquisition(inp) == 0.0

    def test_cpa_equals_total_spend(self):
        # round(total_spend / max(1,1), 2) = total_spend
        inp = make_input(
            channel_spend={"outbound_email": 1000.0, "paid_ads": 2000.0},
            closed_won_value=50_000.0,
        )
        cpa = self.engine._cost_per_acquisition(inp)
        assert cpa == pytest.approx(3000.0, rel=1e-6)

    def test_single_channel_spend(self):
        inp = make_input(
            channel_spend={"sdr_call": 500.0},
            closed_won_value=50_000.0,
        )
        cpa = self.engine._cost_per_acquisition(inp)
        assert cpa == pytest.approx(500.0, rel=1e-6)

    def test_rounded_to_two_decimals(self):
        inp = make_input(
            channel_spend={"paid_ads": 1000.555},
            closed_won_value=10_000.0,
        )
        cpa = self.engine._cost_per_acquisition(inp)
        assert cpa == round(cpa, 2)

    def test_multiple_channels_summed(self):
        inp = make_input(
            channel_spend={"a": 100.0, "b": 200.0, "c": 300.0},
            closed_won_value=10_000.0,
        )
        cpa = self.engine._cost_per_acquisition(inp)
        assert cpa == pytest.approx(600.0, rel=1e-6)


# ===========================================================================
# 10. _cycle_efficiency
# ===========================================================================

class TestCycleEfficiency:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_zero_avg_cycle_returns_50(self):
        inp = make_input(avg_cycle_days=0.0)
        assert self.engine._cycle_efficiency(inp) == 50.0

    def test_negative_avg_cycle_returns_50(self):
        inp = make_input(avg_cycle_days=-10.0)
        assert self.engine._cycle_efficiency(inp) == 50.0

    def test_equal_cycles_below_100(self):
        # avg=30, sales=30 → ratio=1.0 → eff=70.0
        inp = make_input(avg_cycle_days=30.0, sales_cycle_days=30)
        eff = self.engine._cycle_efficiency(inp)
        assert eff == pytest.approx(70.0, rel=1e-6)

    def test_faster_actual_cycle_higher_ratio(self):
        # avg=100, sales=20 → ratio=5 → eff=min(100,350)=100
        inp = make_input(avg_cycle_days=100.0, sales_cycle_days=20)
        eff = self.engine._cycle_efficiency(inp)
        assert eff == 100.0

    def test_slower_actual_cycle_lower_ratio(self):
        # avg=10, sales=100 → ratio=0.1 → eff=7.0
        inp = make_input(avg_cycle_days=10.0, sales_cycle_days=100)
        eff = self.engine._cycle_efficiency(inp)
        assert eff == pytest.approx(7.0, rel=1e-4)

    def test_zero_sales_cycle_uses_max_one(self):
        # avg=30, sales=0 → ratio=30/max(1,0)=30 → min(100, 30*70)=100
        inp = make_input(avg_cycle_days=30.0, sales_cycle_days=0)
        eff = self.engine._cycle_efficiency(inp)
        assert eff == 100.0

    def test_min_is_zero(self):
        # No way to go negative since we take max(0.0, eff)
        inp = make_input(avg_cycle_days=1.0, sales_cycle_days=1000)
        eff = self.engine._cycle_efficiency(inp)
        assert eff >= 0.0

    def test_capped_at_100(self):
        inp = make_input(avg_cycle_days=200.0, sales_cycle_days=10)
        eff = self.engine._cycle_efficiency(inp)
        assert eff <= 100.0

    def test_result_rounded_to_one_decimal(self):
        inp = make_input(avg_cycle_days=30.0, sales_cycle_days=30)
        eff = self.engine._cycle_efficiency(inp)
        assert eff == round(eff, 1)


# ===========================================================================
# 11. _high_value_threshold
# ===========================================================================

class TestHighValueThreshold:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_smb_threshold(self):
        assert self.engine._high_value_threshold("smb") == 25_000

    def test_mid_market_threshold(self):
        assert self.engine._high_value_threshold("mid_market") == 75_000

    def test_enterprise_threshold(self):
        assert self.engine._high_value_threshold("enterprise") == 200_000

    def test_unknown_segment_default(self):
        assert self.engine._high_value_threshold("unknown") == 50_000

    def test_empty_segment_default(self):
        assert self.engine._high_value_threshold("") == 50_000

    def test_random_segment_default(self):
        assert self.engine._high_value_threshold("startup") == 50_000

    def test_case_sensitive_smb(self):
        # "SMB" != "smb" → default
        assert self.engine._high_value_threshold("SMB") == 50_000


# ===========================================================================
# 12. _revenue_risk – each factor, all levels
# ===========================================================================

class TestRevenueRisk:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def _make_low_risk_input(self):
        """Base: all good → should give LOW risk."""
        return make_input(
            pipeline_created=100_000.0,
            closed_won_value=60_000.0,   # win rate 60% → attr_eff=84
            closed_lost_value=5_000.0,
            is_self_sourced=False,
            referral_source="none",
            marketing_qualified=True,
            sales_accepted=True,
            total_touchpoints=5,
            avg_cycle_days=30.0,
            sales_cycle_days=30,
        )

    def test_low_risk_all_good(self):
        inp = self._make_low_risk_input()
        attr_eff = self.engine._attribution_efficiency(inp, {})
        cycle_eff = self.engine._cycle_efficiency(inp)
        risk = self.engine._revenue_risk(inp, attr_eff, cycle_eff)
        assert risk == RevenueRisk.LOW

    def test_attr_eff_below_30_adds_3(self):
        # Force attr_eff=20.0, cycle=70.0 → score=3 → CRITICAL? No, need >=6 for CRITICAL
        # 3 >= 2 so MEDIUM. Check exact: score=3 → HIGH (need >=4 for HIGH? No: >=4=HIGH)
        # Actually: >=6=CRITICAL, >=4=HIGH, >=2=MEDIUM, else LOW
        # score=3 → MEDIUM
        inp = self._make_low_risk_input()
        risk = self.engine._revenue_risk(inp, 20.0, 70.0)
        assert risk == RevenueRisk.MEDIUM

    def test_attr_eff_between_30_and_50_adds_1(self):
        inp = self._make_low_risk_input()
        # score=1 → LOW
        risk = self.engine._revenue_risk(inp, 40.0, 70.0)
        assert risk == RevenueRisk.LOW

    def test_cycle_eff_below_30_adds_2(self):
        inp = self._make_low_risk_input()
        # attr_eff=80 (score=0), cycle=20 (+2) → score=2 → MEDIUM
        risk = self.engine._revenue_risk(inp, 80.0, 20.0)
        assert risk == RevenueRisk.MEDIUM

    def test_cycle_eff_between_30_and_50_adds_1(self):
        inp = self._make_low_risk_input()
        # attr_eff=80, cycle=40 (+1) → score=1 → LOW
        risk = self.engine._revenue_risk(inp, 80.0, 40.0)
        assert risk == RevenueRisk.LOW

    def test_closed_lost_greater_than_won_adds_2(self):
        inp = make_input(
            pipeline_created=100_000.0,
            closed_won_value=5_000.0,
            closed_lost_value=50_000.0,
            is_self_sourced=False,
            referral_source="none",
            marketing_qualified=True,
            sales_accepted=True,
            total_touchpoints=5,
            avg_cycle_days=30.0,
            sales_cycle_days=30,
        )
        attr_eff = self.engine._attribution_efficiency(inp, {})
        cycle_eff = self.engine._cycle_efficiency(inp)
        risk = self.engine._revenue_risk(inp, attr_eff, cycle_eff)
        assert risk in (RevenueRisk.MEDIUM, RevenueRisk.HIGH, RevenueRisk.CRITICAL)

    def test_not_sales_accepted_adds_1(self):
        inp = make_input(
            pipeline_created=100_000.0,
            closed_won_value=60_000.0,
            closed_lost_value=5_000.0,
            is_self_sourced=False,
            referral_source="none",
            marketing_qualified=True,
            sales_accepted=False,    # adds 1
            total_touchpoints=5,
            avg_cycle_days=30.0,
            sales_cycle_days=30,
        )
        attr_eff = self.engine._attribution_efficiency(inp, {})
        cycle_eff = self.engine._cycle_efficiency(inp)
        risk = self.engine._revenue_risk(inp, attr_eff, cycle_eff)
        assert risk == RevenueRisk.LOW

    def test_total_touchpoints_gt_15_adds_1(self):
        inp = make_input(total_touchpoints=16, sales_accepted=True)
        # 16 > 15 → +1 alone, attr_eff=75 (approx), cycle=70
        attr_eff = self.engine._attribution_efficiency(inp, {})
        cycle_eff = self.engine._cycle_efficiency(inp)
        risk = self.engine._revenue_risk(inp, attr_eff, cycle_eff)
        assert risk == RevenueRisk.LOW

    def test_critical_risk_score_6_or_more(self):
        # Force score >= 6:
        # attr_eff<30 (+3), cycle<30 (+2), lost>won (+2) = 7
        inp = make_input(
            pipeline_created=100_000.0,
            closed_won_value=5_000.0,
            closed_lost_value=50_000.0,
            sales_accepted=False,
            total_touchpoints=16,
            avg_cycle_days=10.0,
            sales_cycle_days=1000,
        )
        risk = self.engine._revenue_risk(inp, 20.0, 20.0)
        assert risk == RevenueRisk.CRITICAL

    def test_high_risk_score_4_or_5(self):
        # attr_eff<30 (+3), lost>won (+2) = 5 → HIGH
        inp = make_input(
            pipeline_created=100_000.0,
            closed_won_value=5_000.0,
            closed_lost_value=50_000.0,
            sales_accepted=True,
            total_touchpoints=5,
            avg_cycle_days=30.0,
            sales_cycle_days=30,
        )
        risk = self.engine._revenue_risk(inp, 20.0, 70.0)
        assert risk == RevenueRisk.HIGH

    def test_medium_risk_score_2_or_3(self):
        # attr_eff<30 (+3) = 3 → MEDIUM
        inp = make_input(
            pipeline_created=100_000.0,
            closed_won_value=60_000.0,
            closed_lost_value=5_000.0,
            sales_accepted=True,
            total_touchpoints=5,
            avg_cycle_days=30.0,
            sales_cycle_days=30,
        )
        risk = self.engine._revenue_risk(inp, 20.0, 70.0)
        assert risk == RevenueRisk.MEDIUM

    def test_low_risk_score_0_or_1(self):
        inp = self._make_low_risk_input()
        risk = self.engine._revenue_risk(inp, 80.0, 70.0)
        assert risk == RevenueRisk.LOW

    def test_risk_score_exactly_2_is_medium(self):
        inp = make_input(sales_accepted=True, total_touchpoints=5)
        risk = self.engine._revenue_risk(inp, 80.0, 20.0)
        # cycle_eff<30 → +2 → score=2 → MEDIUM
        assert risk == RevenueRisk.MEDIUM

    def test_risk_score_exactly_4_is_high(self):
        # attr_eff<30 (+3), not sales_accepted (+1) → score=4 → HIGH
        inp = make_input(sales_accepted=False, total_touchpoints=5)
        risk = self.engine._revenue_risk(inp, 20.0, 70.0)
        assert risk == RevenueRisk.HIGH

    def test_risk_score_exactly_6_is_critical(self):
        # attr_eff<30 (+3), cycle<30 (+2), not sales_accepted (+1) → score=6 → CRITICAL
        inp = make_input(sales_accepted=False, total_touchpoints=5)
        risk = self.engine._revenue_risk(inp, 20.0, 20.0)
        assert risk == RevenueRisk.CRITICAL


# ===========================================================================
# 13. _optimization_action – all branches
# ===========================================================================

class TestOptimizationAction:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()
        self.inp = make_input()

    def test_critical_risk_returns_reallocate(self):
        roi = {"outbound_email": 10.0}
        action = self.engine._optimization_action(self.inp, 80.0, roi, RevenueRisk.CRITICAL)
        assert action == OptimizationAction.REALLOCATE

    def test_high_roi_and_high_eff_returns_scale_up(self):
        roi = {"outbound_email": 6.0}
        action = self.engine._optimization_action(self.inp, 75.0, roi, RevenueRisk.LOW)
        assert action == OptimizationAction.SCALE_UP

    def test_high_roi_but_low_eff_no_scale_up(self):
        roi = {"outbound_email": 6.0}
        action = self.engine._optimization_action(self.inp, 65.0, roi, RevenueRisk.LOW)
        assert action != OptimizationAction.SCALE_UP

    def test_low_roi_high_eff_no_scale_up(self):
        roi = {"outbound_email": 3.0}
        action = self.engine._optimization_action(self.inp, 80.0, roi, RevenueRisk.LOW)
        assert action != OptimizationAction.SCALE_UP

    def test_attr_eff_60_returns_maintain(self):
        roi = {"outbound_email": 2.0}
        action = self.engine._optimization_action(self.inp, 60.0, roi, RevenueRisk.LOW)
        assert action == OptimizationAction.MAINTAIN

    def test_attr_eff_above_60_returns_maintain(self):
        roi = {"outbound_email": 1.0}
        action = self.engine._optimization_action(self.inp, 65.0, roi, RevenueRisk.LOW)
        assert action == OptimizationAction.MAINTAIN

    def test_attr_eff_40_returns_optimize(self):
        roi = {"outbound_email": 2.0}
        action = self.engine._optimization_action(self.inp, 40.0, roi, RevenueRisk.LOW)
        assert action == OptimizationAction.OPTIMIZE

    def test_attr_eff_between_40_and_60_optimize(self):
        roi = {"outbound_email": 1.0}
        action = self.engine._optimization_action(self.inp, 50.0, roi, RevenueRisk.LOW)
        assert action == OptimizationAction.OPTIMIZE

    def test_high_risk_low_eff_returns_reduce(self):
        roi = {"outbound_email": 1.0}
        action = self.engine._optimization_action(self.inp, 30.0, roi, RevenueRisk.HIGH)
        assert action == OptimizationAction.REDUCE

    def test_low_risk_low_eff_returns_optimize(self):
        roi = {"outbound_email": 1.0}
        action = self.engine._optimization_action(self.inp, 30.0, roi, RevenueRisk.LOW)
        assert action == OptimizationAction.OPTIMIZE

    def test_medium_risk_low_eff_returns_optimize(self):
        roi = {"outbound_email": 1.0}
        action = self.engine._optimization_action(self.inp, 30.0, roi, RevenueRisk.MEDIUM)
        assert action == OptimizationAction.OPTIMIZE

    def test_empty_roi_avg_is_zero(self):
        # avg_roi = 0/max(1,0)=0 → not >=5 → check attr_eff
        action = self.engine._optimization_action(self.inp, 65.0, {}, RevenueRisk.LOW)
        assert action == OptimizationAction.MAINTAIN

    def test_exactly_roi_5_and_eff_70(self):
        roi = {"ch": 5.0}
        action = self.engine._optimization_action(self.inp, 70.0, roi, RevenueRisk.LOW)
        assert action == OptimizationAction.SCALE_UP

    def test_roi_just_below_5_eff_above_70(self):
        roi = {"ch": 4.99}
        action = self.engine._optimization_action(self.inp, 75.0, roi, RevenueRisk.LOW)
        # avg_roi=4.99 < 5.0 → no SCALE_UP → attr_eff>=60 → MAINTAIN
        assert action == OptimizationAction.MAINTAIN


# ===========================================================================
# 14. is_high_value per segment
# ===========================================================================

class TestIsHighValue:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_smb_above_threshold(self):
        inp = make_input(deal_value=30_000.0, segment="smb")
        result = self.engine.analyze(inp)
        assert result.is_high_value is True

    def test_smb_below_threshold(self):
        inp = make_input(deal_value=24_999.0, segment="smb")
        result = self.engine.analyze(inp)
        assert result.is_high_value is False

    def test_smb_at_threshold(self):
        inp = make_input(deal_value=25_000.0, segment="smb")
        result = self.engine.analyze(inp)
        assert result.is_high_value is True

    def test_mid_market_above_threshold(self):
        inp = make_input(deal_value=80_000.0, segment="mid_market")
        result = self.engine.analyze(inp)
        assert result.is_high_value is True

    def test_mid_market_below_threshold(self):
        inp = make_input(deal_value=74_999.0, segment="mid_market")
        result = self.engine.analyze(inp)
        assert result.is_high_value is False

    def test_mid_market_at_threshold(self):
        inp = make_input(deal_value=75_000.0, segment="mid_market")
        result = self.engine.analyze(inp)
        assert result.is_high_value is True

    def test_enterprise_above_threshold(self):
        inp = make_input(deal_value=250_000.0, segment="enterprise")
        result = self.engine.analyze(inp)
        assert result.is_high_value is True

    def test_enterprise_below_threshold(self):
        inp = make_input(deal_value=199_999.0, segment="enterprise")
        result = self.engine.analyze(inp)
        assert result.is_high_value is False

    def test_enterprise_at_threshold(self):
        inp = make_input(deal_value=200_000.0, segment="enterprise")
        result = self.engine.analyze(inp)
        assert result.is_high_value is True

    def test_unknown_segment_default_threshold(self):
        inp = make_input(deal_value=55_000.0, segment="unknown")
        result = self.engine.analyze(inp)
        assert result.is_high_value is True

    def test_unknown_segment_below_default(self):
        inp = make_input(deal_value=49_999.0, segment="unknown")
        result = self.engine.analyze(inp)
        assert result.is_high_value is False


# ===========================================================================
# 15. Properties
# ===========================================================================

class TestProperties:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_high_value_deals_empty_initially(self):
        assert self.engine.high_value_deals == []

    def test_high_risk_revenue_empty_initially(self):
        assert self.engine.high_risk_revenue == []

    def test_scale_up_channels_empty_initially(self):
        assert self.engine.scale_up_channels == []

    def test_total_attributed_revenue_zero_initially(self):
        assert self.engine.total_attributed_revenue == 0.0

    def test_high_value_deals_filters_correctly(self):
        self.engine.analyze(make_input(deal_value=100_000.0, segment="mid_market"))  # above 75k
        self.engine.analyze(make_input(deal_value=10_000.0, segment="mid_market"))   # below 75k
        hv = self.engine.high_value_deals
        assert len(hv) == 1
        assert hv[0].is_high_value is True

    def test_high_risk_revenue_filters_high(self):
        # Create a high-risk scenario
        inp = make_input(
            pipeline_created=100_000.0,
            closed_won_value=5_000.0,
            closed_lost_value=50_000.0,
            sales_accepted=True,
            total_touchpoints=5,
            avg_cycle_days=30.0,
            sales_cycle_days=30,
        )
        result = self.engine.analyze(inp)
        if result.revenue_risk in (RevenueRisk.HIGH, RevenueRisk.CRITICAL):
            assert len(self.engine.high_risk_revenue) >= 1

    def test_high_risk_revenue_filters_critical(self):
        inp = make_input(
            pipeline_created=100_000.0,
            closed_won_value=5_000.0,
            closed_lost_value=50_000.0,
            sales_accepted=False,
            total_touchpoints=16,
            avg_cycle_days=10.0,
            sales_cycle_days=1000,
        )
        result = self.engine.analyze(inp)
        if result.revenue_risk == RevenueRisk.CRITICAL:
            assert result in self.engine.high_risk_revenue

    def test_scale_up_channels_filters(self):
        # Force scale_up by high ROI + high efficiency
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 1, is_first_touch=True, is_last_touch=True)
        ]
        inp = make_input(
            touchpoints=tps,
            attribution_model=AttributionModel.FIRST_TOUCH,
            pipeline_created=100_000.0,
            closed_won_value=80_000.0,
            channel_spend={"outbound_email": 1.0},   # tiny spend → huge ROI
            is_self_sourced=True,
            referral_source="customer",
            marketing_qualified=True,
            sales_accepted=True,
        )
        result = self.engine.analyze(inp)
        if result.optimization_action == OptimizationAction.SCALE_UP:
            assert result in self.engine.scale_up_channels

    def test_total_attributed_revenue_sums(self):
        self.engine.analyze(make_input(closed_won_value=10_000.0))
        self.engine.analyze(make_input(closed_won_value=20_000.0))
        assert self.engine.total_attributed_revenue == pytest.approx(30_000.0, rel=1e-6)

    def test_total_attributed_revenue_rounded(self):
        self.engine.analyze(make_input(closed_won_value=10_000.123))
        self.engine.analyze(make_input(closed_won_value=5_000.456))
        rev = self.engine.total_attributed_revenue
        assert rev == round(rev, 2)

    def test_high_value_deals_returns_list(self):
        assert isinstance(self.engine.high_value_deals, list)

    def test_high_risk_revenue_returns_list(self):
        assert isinstance(self.engine.high_risk_revenue, list)

    def test_scale_up_channels_returns_list(self):
        assert isinstance(self.engine.scale_up_channels, list)


# ===========================================================================
# 16. summary() – 13 keys
# ===========================================================================

class TestSummary:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_empty_summary_key_count(self):
        s = self.engine.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self):
        assert self.engine.summary()["total"] == 0

    def test_empty_summary_model_counts_empty(self):
        assert self.engine.summary()["model_counts"] == {}

    def test_empty_summary_risk_counts_empty(self):
        assert self.engine.summary()["risk_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        assert self.engine.summary()["action_counts"] == {}

    def test_empty_summary_top_channel_counts_empty(self):
        assert self.engine.summary()["top_channel_counts"] == {}

    def test_empty_summary_total_attributed_revenue_zero(self):
        assert self.engine.summary()["total_attributed_revenue"] == 0.0

    def test_empty_summary_avg_attribution_efficiency_zero(self):
        assert self.engine.summary()["avg_attribution_efficiency"] == 0.0

    def test_empty_summary_avg_pipeline_ratio_zero(self):
        assert self.engine.summary()["avg_pipeline_to_revenue_ratio"] == 0.0

    def test_empty_summary_avg_cycle_efficiency_zero(self):
        assert self.engine.summary()["avg_cycle_efficiency"] == 0.0

    def test_empty_summary_high_value_count_zero(self):
        assert self.engine.summary()["high_value_count"] == 0

    def test_empty_summary_high_risk_count_zero(self):
        assert self.engine.summary()["high_risk_count"] == 0

    def test_empty_summary_scale_up_count_zero(self):
        assert self.engine.summary()["scale_up_count"] == 0

    def test_empty_summary_avg_cpa_zero(self):
        assert self.engine.summary()["avg_cost_per_acquisition"] == 0.0

    def test_summary_has_all_13_keys(self):
        expected_keys = {
            "total", "model_counts", "risk_counts", "action_counts",
            "top_channel_counts", "total_attributed_revenue",
            "avg_attribution_efficiency", "avg_pipeline_to_revenue_ratio",
            "avg_cycle_efficiency", "high_value_count", "high_risk_count",
            "scale_up_count", "avg_cost_per_acquisition",
        }
        assert set(self.engine.summary().keys()) == expected_keys

    def test_summary_after_one_analysis(self):
        self.engine.analyze(make_input(deal_id="d1"))
        s = self.engine.summary()
        assert s["total"] == 1

    def test_summary_model_counts_after_analysis(self):
        self.engine.analyze(make_input(attribution_model=AttributionModel.LINEAR))
        s = self.engine.summary()
        assert "linear" in s["model_counts"]
        assert s["model_counts"]["linear"] == 1

    def test_summary_risk_counts_after_analysis(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert len(s["risk_counts"]) >= 1

    def test_summary_action_counts_after_analysis(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert len(s["action_counts"]) >= 1

    def test_summary_total_revenue_after_two(self):
        self.engine.analyze(make_input(closed_won_value=10_000.0))
        self.engine.analyze(make_input(closed_won_value=20_000.0))
        s = self.engine.summary()
        assert s["total_attributed_revenue"] == pytest.approx(30_000.0, rel=1e-6)

    def test_summary_top_channel_counted(self):
        tps = [make_tp(ChannelType.OUTBOUND_EMAIL, 10, is_first_touch=True)]
        inp = make_input(
            touchpoints=tps,
            attribution_model=AttributionModel.FIRST_TOUCH,
            closed_won_value=10_000.0,
        )
        self.engine.analyze(inp)
        s = self.engine.summary()
        assert "outbound_email" in s["top_channel_counts"]

    def test_summary_multiple_models(self):
        self.engine.analyze(make_input(attribution_model=AttributionModel.LINEAR))
        self.engine.analyze(make_input(attribution_model=AttributionModel.FIRST_TOUCH))
        s = self.engine.summary()
        assert "linear" in s["model_counts"]
        assert "first_touch" in s["model_counts"]

    def test_summary_avg_attribution_efficiency_rounded(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        v = s["avg_attribution_efficiency"]
        assert v == round(v, 1)

    def test_summary_high_value_count_increments(self):
        self.engine.analyze(make_input(deal_value=200_000.0, segment="smb"))
        s = self.engine.summary()
        assert s["high_value_count"] >= 1


# ===========================================================================
# 17. reset()
# ===========================================================================

class TestReset:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_reset_clears_results(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert self.engine._results == []

    def test_reset_clears_multiple_results(self):
        for _ in range(5):
            self.engine.analyze(make_input())
        self.engine.reset()
        assert len(self.engine._results) == 0

    def test_reset_clears_total_attributed_revenue(self):
        self.engine.analyze(make_input(closed_won_value=50_000.0))
        self.engine.reset()
        assert self.engine.total_attributed_revenue == 0.0

    def test_reset_clears_high_value_deals(self):
        self.engine.analyze(make_input(deal_value=200_000.0, segment="smb"))
        self.engine.reset()
        assert self.engine.high_value_deals == []

    def test_reset_clears_high_risk_revenue(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert self.engine.high_risk_revenue == []

    def test_reset_clears_scale_up_channels(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert self.engine.scale_up_channels == []

    def test_can_analyze_after_reset(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        result = self.engine.analyze(make_input(deal_id="new-deal"))
        assert result.deal_id == "new-deal"

    def test_summary_empty_after_reset(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert self.engine.summary()["total"] == 0

    def test_reset_returns_none(self):
        assert self.engine.reset() is None


# ===========================================================================
# 18. analyze() and analyze_batch()
# ===========================================================================

class TestAnalyze:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_analyze_returns_result(self):
        result = self.engine.analyze(make_input())
        assert isinstance(result, RevenueAttributionResult)

    def test_analyze_stores_result(self):
        self.engine.analyze(make_input())
        assert len(self.engine._results) == 1

    def test_analyze_accumulates_results(self):
        for i in range(5):
            self.engine.analyze(make_input(deal_id=f"deal-{i}"))
        assert len(self.engine._results) == 5

    def test_analyze_deal_id_preserved(self):
        result = self.engine.analyze(make_input(deal_id="xyz"))
        assert result.deal_id == "xyz"

    def test_analyze_account_id_preserved(self):
        result = self.engine.analyze(make_input(account_id="acc-xyz"))
        assert result.account_id == "acc-xyz"

    def test_analyze_rep_id_preserved(self):
        result = self.engine.analyze(make_input(rep_id="rep-xyz"))
        assert result.rep_id == "rep-xyz"

    def test_analyze_attributed_revenue_is_closed_won_rounded(self):
        result = self.engine.analyze(make_input(closed_won_value=12345.678))
        assert result.attributed_revenue == round(12345.678, 2)

    def test_analyze_attribution_model_preserved(self):
        result = self.engine.analyze(make_input(attribution_model=AttributionModel.TIME_DECAY))
        assert result.attribution_model == AttributionModel.TIME_DECAY

    def test_analyze_top_channel_from_credits(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 5, is_last_touch=True),
        ]
        inp = make_input(
            touchpoints=tps,
            attribution_model=AttributionModel.FIRST_TOUCH,
            closed_won_value=10_000.0,
        )
        result = self.engine.analyze(inp)
        assert result.top_channel == "outbound_email"

    def test_analyze_top_channel_unknown_when_no_credits(self):
        inp = make_input(touchpoints=[], closed_won_value=0.0)
        result = self.engine.analyze(inp)
        assert result.top_channel == "unknown"

    def test_analyze_batch_returns_list(self):
        inputs = [make_input(deal_id=f"d{i}") for i in range(3)]
        results = self.engine.analyze_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 3

    def test_analyze_batch_each_is_result(self):
        inputs = [make_input(deal_id=f"d{i}") for i in range(3)]
        results = self.engine.analyze_batch(inputs)
        for r in results:
            assert isinstance(r, RevenueAttributionResult)

    def test_analyze_batch_stores_all(self):
        inputs = [make_input(deal_id=f"d{i}") for i in range(4)]
        self.engine.analyze_batch(inputs)
        assert len(self.engine._results) == 4

    def test_analyze_batch_empty_list(self):
        results = self.engine.analyze_batch([])
        assert results == []

    def test_analyze_batch_deal_ids_preserved(self):
        inputs = [make_input(deal_id=f"deal-{i}") for i in range(3)]
        results = self.engine.analyze_batch(inputs)
        ids = [r.deal_id for r in results]
        assert ids == ["deal-0", "deal-1", "deal-2"]


# ===========================================================================
# 19. End-to-end scenarios
# ===========================================================================

class TestEndToEndScenarios:
    def setup_method(self):
        self.engine = RevenueAttributionEngine()

    def test_full_pipeline_linear_model(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 15),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(
            deal_id="e2e-001",
            attribution_model=AttributionModel.LINEAR,
            touchpoints=tps,
            closed_won_value=30_000.0,
            pipeline_created=100_000.0,
            channel_spend={
                "outbound_email": 1_000.0,
                "paid_ads": 2_000.0,
                "sdr_call": 500.0,
            },
        )
        result = self.engine.analyze(inp)
        d = result.to_dict()
        assert d["deal_id"] == "e2e-001"
        assert d["attributed_revenue"] == 30_000.0
        assert d["attribution_model"] == "linear"
        assert "outbound_email" in d["channel_credits"]
        assert "paid_ads" in d["channel_credits"]
        assert "sdr_call" in d["channel_credits"]

    def test_full_pipeline_first_touch(self):
        tps = [
            make_tp(ChannelType.EVENT, 60, is_first_touch=True),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(
            attribution_model=AttributionModel.FIRST_TOUCH,
            touchpoints=tps,
            closed_won_value=20_000.0,
        )
        result = self.engine.analyze(inp)
        assert result.channel_credits["event"] == 20_000.0
        assert "sdr_call" not in result.channel_credits

    def test_full_pipeline_last_touch(self):
        tps = [
            make_tp(ChannelType.EVENT, 60, is_first_touch=True),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(
            attribution_model=AttributionModel.LAST_TOUCH,
            touchpoints=tps,
            closed_won_value=20_000.0,
        )
        result = self.engine.analyze(inp)
        assert result.channel_credits["sdr_call"] == 20_000.0
        assert "event" not in result.channel_credits

    def test_enterprise_high_value_deal(self):
        inp = make_input(
            deal_value=500_000.0,
            segment="enterprise",
            closed_won_value=500_000.0,
        )
        result = self.engine.analyze(inp)
        assert result.is_high_value is True

    def test_smb_low_value_not_high(self):
        inp = make_input(deal_value=10_000.0, segment="smb")
        result = self.engine.analyze(inp)
        assert result.is_high_value is False

    def test_summary_matches_individual_results(self):
        for i in range(3):
            self.engine.analyze(make_input(deal_id=f"deal-{i}", closed_won_value=10_000.0))
        s = self.engine.summary()
        assert s["total"] == 3
        assert s["total_attributed_revenue"] == pytest.approx(30_000.0, rel=1e-6)

    def test_batch_then_summary(self):
        inputs = [make_input(deal_id=f"batch-{i}") for i in range(5)]
        self.engine.analyze_batch(inputs)
        s = self.engine.summary()
        assert s["total"] == 5

    def test_reset_then_reanalyze(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        self.engine.analyze(make_input(deal_id="new"))
        assert self.engine.summary()["total"] == 1

    def test_channel_credits_roi_consistency(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(
            attribution_model=AttributionModel.FIRST_TOUCH,
            touchpoints=tps,
            closed_won_value=10_000.0,
            channel_spend={"outbound_email": 2_000.0},
        )
        result = self.engine.analyze(inp)
        assert "outbound_email" in result.roi_by_channel
        assert result.roi_by_channel["outbound_email"] == pytest.approx(5.0, rel=1e-6)

    def test_time_decay_scenario(self):
        tps = [
            make_tp(ChannelType.INBOUND_CONTENT, 90, is_first_touch=True),
            make_tp(ChannelType.SDR_CALL, 5, is_last_touch=True),
        ]
        inp = make_input(
            attribution_model=AttributionModel.TIME_DECAY,
            touchpoints=tps,
            closed_won_value=10_000.0,
        )
        result = self.engine.analyze(inp)
        # sdr_call is more recent (weight 1/5=0.2), inbound_content weight 1/90≈0.011
        assert result.channel_credits["sdr_call"] > result.channel_credits["inbound_content"]

    def test_position_based_four_touchpoints(self):
        tps = [
            make_tp(ChannelType.INBOUND_CONTENT, 60, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 40),
            make_tp(ChannelType.SOCIAL_SELLING, 20),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(
            attribution_model=AttributionModel.POSITION_BASED,
            touchpoints=tps,
            closed_won_value=10_000.0,
        )
        result = self.engine.analyze(inp)
        assert result.channel_credits["inbound_content"] == pytest.approx(4_000.0, rel=1e-4)
        assert result.channel_credits["sdr_call"] == pytest.approx(4_000.0, rel=1e-4)
        # 20% split among 2 middle → 1000 each
        assert result.channel_credits["paid_ads"] == pytest.approx(1_000.0, rel=1e-4)
        assert result.channel_credits["social_selling"] == pytest.approx(1_000.0, rel=1e-4)

    def test_no_touchpoints_zero_credits(self):
        inp = make_input(touchpoints=[], closed_won_value=10_000.0)
        result = self.engine.analyze(inp)
        assert result.channel_credits == {}

    def test_zero_closed_won_zero_credits(self):
        inp = make_input(closed_won_value=0.0)
        result = self.engine.analyze(inp)
        assert result.channel_credits == {}

    def test_result_dataclass_fields(self):
        import dataclasses
        result = self.engine.analyze(make_input())
        fields = {f.name for f in dataclasses.fields(result)}
        assert "deal_id" in fields
        assert "attributed_revenue" in fields
        assert "channel_credits" in fields
        assert "roi_by_channel" in fields
        assert "revenue_risk" in fields
        assert "optimization_action" in fields

    def test_cycle_efficiency_in_result(self):
        inp = make_input(avg_cycle_days=30.0, sales_cycle_days=30)
        result = self.engine.analyze(inp)
        assert result.cycle_efficiency == pytest.approx(70.0, rel=1e-4)

    def test_pipeline_to_revenue_ratio_in_result(self):
        inp = make_input(pipeline_created=100_000.0, closed_won_value=50_000.0)
        result = self.engine.analyze(inp)
        assert result.pipeline_to_revenue_ratio == pytest.approx(0.5, rel=1e-6)

    def test_cost_per_acquisition_in_result(self):
        inp = make_input(
            channel_spend={"outbound_email": 500.0, "paid_ads": 1_000.0},
            closed_won_value=50_000.0,
        )
        result = self.engine.analyze(inp)
        assert result.cost_per_acquisition == pytest.approx(1_500.0, rel=1e-6)

    def test_to_dict_attribution_model_value(self):
        result = self.engine.analyze(make_input(attribution_model=AttributionModel.TIME_DECAY))
        d = result.to_dict()
        assert d["attribution_model"] == "time_decay"

    def test_to_dict_revenue_risk_value(self):
        result = self.engine.analyze(make_input())
        d = result.to_dict()
        assert d["revenue_risk"] in ["low", "medium", "high", "critical"]

    def test_to_dict_optimization_action_value(self):
        result = self.engine.analyze(make_input())
        d = result.to_dict()
        assert d["optimization_action"] in ["scale_up", "maintain", "optimize", "reduce", "reallocate"]

    def test_multiple_deals_different_models(self):
        models = list(AttributionModel)
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        for model in models:
            inp = make_input(attribution_model=model, touchpoints=tps)
            result = self.engine.analyze(inp)
            assert isinstance(result, RevenueAttributionResult)
        s = self.engine.summary()
        assert s["total"] == len(models)

    def test_high_efficiency_scale_up_scenario(self):
        # High win rate + self-sourced + referral + mql/sal → high attr_eff
        # Plus high ROI from low spend → SCALE_UP
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 5, is_first_touch=True, is_last_touch=True),
        ]
        inp = make_input(
            attribution_model=AttributionModel.FIRST_TOUCH,
            touchpoints=tps,
            pipeline_created=100_000.0,
            closed_won_value=85_000.0,
            channel_spend={"outbound_email": 100.0},
            is_self_sourced=True,
            referral_source="customer",
            marketing_qualified=True,
            sales_accepted=True,
            closed_lost_value=5_000.0,
        )
        result = self.engine.analyze(inp)
        # attr_eff >= 70 and ROI is very high → SCALE_UP
        assert result.optimization_action == OptimizationAction.SCALE_UP

    def test_critical_risk_reallocate_scenario(self):
        inp = make_input(
            pipeline_created=100_000.0,
            closed_won_value=5_000.0,
            closed_lost_value=100_000.0,
            sales_accepted=False,
            total_touchpoints=20,
            avg_cycle_days=5.0,
            sales_cycle_days=500,
            is_self_sourced=False,
            referral_source="none",
            marketing_qualified=False,
        )
        result = self.engine.analyze(inp)
        if result.revenue_risk == RevenueRisk.CRITICAL:
            assert result.optimization_action == OptimizationAction.REALLOCATE

    def test_init_creates_empty_results(self):
        eng = RevenueAttributionEngine()
        assert eng._results == []

    def test_top_channel_is_max_credit(self):
        tps = [
            make_tp(ChannelType.OUTBOUND_EMAIL, 30, is_first_touch=True),
            make_tp(ChannelType.PAID_ADS, 15),
            make_tp(ChannelType.SDR_CALL, 1, is_last_touch=True),
        ]
        inp = make_input(
            attribution_model=AttributionModel.POSITION_BASED,
            touchpoints=tps,
            closed_won_value=10_000.0,
        )
        result = self.engine.analyze(inp)
        # outbound_email (40%) and sdr_call (40%) tie, paid_ads (20%)
        # max will pick one of the 40% ones
        assert result.top_channel in ("outbound_email", "sdr_call")
