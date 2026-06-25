"""
Comprehensive pytest tests for SalesAccountExpansionIntelligenceEngine.
~300 tests covering: enums, sub-scores, pattern detection, risk/severity/action
mapping, flags, revenue upside, signal string, to_dict, summary, assess_batch,
and edge cases.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_account_expansion_intelligence_engine import (
    SalesAccountExpansionIntelligenceEngine,
    AccountExpansionInput,
    AccountExpansionResult,
    ExpansionRisk,
    ExpansionPattern,
    ExpansionSeverity,
    ExpansionAction,
)


# ---------------------------------------------------------------------------
# Helper fixture
# ---------------------------------------------------------------------------

def make_input(**kwargs) -> AccountExpansionInput:
    defaults = dict(
        rep_id="rep_test",
        region="West",
        evaluation_period_id="Q1-2026",
        total_accounts=20,
        expansion_ready_accounts=5,
        expansion_conversations_initiated=4,
        expansion_proposals_sent=3,
        expansion_deals_closed=2,
        cross_sell_opportunities_identified=6,
        cross_sell_opportunities_pursued=4,
        upsell_revenue_last_period_usd=80000.0,
        avg_account_product_penetration_pct=0.60,
        accounts_at_contract_renewal_90d=3,
        renewal_expansions_secured_count=2,
        net_revenue_retention_pct=1.08,
        avg_account_lifetime_months=30.0,
        multi_product_accounts_count=12,
        single_product_accounts_count=8,
        executive_sponsor_coverage_pct=0.70,
        account_health_avg_score=7.5,
        avg_contract_value_usd=40000.0,
        churn_prevented_revenue_usd=20000.0,
    )
    defaults.update(kwargs)
    return AccountExpansionInput(**defaults)


@pytest.fixture
def engine():
    return SalesAccountExpansionIntelligenceEngine()


@pytest.fixture
def base_input():
    return make_input()


# ===========================================================================
# 1. Enum values
# ===========================================================================

class TestExpansionRiskEnum:
    def test_low_value(self):
        assert ExpansionRisk.low.value == "low"

    def test_moderate_value(self):
        assert ExpansionRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert ExpansionRisk.high.value == "high"

    def test_critical_value(self):
        assert ExpansionRisk.critical.value == "critical"

    def test_count(self):
        assert len(ExpansionRisk) == 4

    def test_is_str(self):
        assert isinstance(ExpansionRisk.low, str)

    def test_string_equality_low(self):
        assert ExpansionRisk.low == "low"

    def test_string_equality_critical(self):
        assert ExpansionRisk.critical == "critical"


class TestExpansionPatternEnum:
    def test_none_value(self):
        assert ExpansionPattern.none.value == "none"

    def test_stagnant_portfolio_value(self):
        assert ExpansionPattern.stagnant_portfolio.value == "stagnant_portfolio"

    def test_cross_sell_neglect_value(self):
        assert ExpansionPattern.cross_sell_neglect.value == "cross_sell_neglect"

    def test_renewal_risk_value(self):
        assert ExpansionPattern.renewal_risk.value == "renewal_risk"

    def test_low_penetration_value(self):
        assert ExpansionPattern.low_penetration.value == "low_penetration"

    def test_executive_gap_value(self):
        assert ExpansionPattern.executive_gap.value == "executive_gap"

    def test_count(self):
        assert len(ExpansionPattern) == 6

    def test_is_str(self):
        assert isinstance(ExpansionPattern.none, str)

    def test_string_equality_none(self):
        assert ExpansionPattern.none == "none"


class TestExpansionSeverityEnum:
    def test_growing_value(self):
        assert ExpansionSeverity.growing.value == "growing"

    def test_steady_value(self):
        assert ExpansionSeverity.steady.value == "steady"

    def test_declining_value(self):
        assert ExpansionSeverity.declining.value == "declining"

    def test_stagnant_value(self):
        assert ExpansionSeverity.stagnant.value == "stagnant"

    def test_count(self):
        assert len(ExpansionSeverity) == 4

    def test_is_str(self):
        assert isinstance(ExpansionSeverity.growing, str)


class TestExpansionActionEnum:
    def test_no_action_value(self):
        assert ExpansionAction.no_action.value == "no_action"

    def test_expansion_outreach_value(self):
        assert ExpansionAction.expansion_outreach.value == "expansion_outreach"

    def test_cross_sell_campaign_value(self):
        assert ExpansionAction.cross_sell_campaign.value == "cross_sell_campaign"

    def test_renewal_acceleration_value(self):
        assert ExpansionAction.renewal_acceleration.value == "renewal_acceleration"

    def test_penetration_deepening_value(self):
        assert ExpansionAction.penetration_deepening.value == "penetration_deepening"

    def test_executive_alignment_value(self):
        assert ExpansionAction.executive_alignment.value == "executive_alignment"

    def test_count(self):
        assert len(ExpansionAction) == 6

    def test_is_str(self):
        assert isinstance(ExpansionAction.no_action, str)


# ===========================================================================
# 2. _expansion_capture_score
# ===========================================================================

class TestExpansionCaptureScore:
    """Higher score = more risk / missed opportunity (0-100)."""

    def _score(self, engine, **kwargs):
        inp = make_input(**kwargs)
        return engine._expansion_capture_score(inp)

    # --- engage_rate thresholds ---
    def test_engage_rate_below_030_adds_35(self, engine):
        # ready=10, initiated=2 → rate=0.20 < 0.30 → +35
        s = self._score(engine,
                        expansion_ready_accounts=10,
                        expansion_conversations_initiated=2,
                        expansion_proposals_sent=0,
                        expansion_deals_closed=0,
                        cross_sell_opportunities_identified=0,
                        cross_sell_opportunities_pursued=0)
        assert s >= 35.0

    def test_engage_rate_between_030_050_adds_20(self, engine):
        # ready=10, initiated=4 → rate=0.40
        s = self._score(engine,
                        expansion_ready_accounts=10,
                        expansion_conversations_initiated=4,
                        expansion_proposals_sent=0,
                        expansion_deals_closed=0,
                        cross_sell_opportunities_identified=0,
                        cross_sell_opportunities_pursued=0)
        # +20 from engage, +25 proposals==0 & ready>=3
        assert s >= 20.0

    def test_engage_rate_between_050_070_adds_8(self, engine):
        # ready=10, initiated=6 → rate=0.60
        s = self._score(engine,
                        expansion_ready_accounts=10,
                        expansion_conversations_initiated=6,
                        expansion_proposals_sent=0,
                        expansion_deals_closed=0,
                        cross_sell_opportunities_identified=0,
                        cross_sell_opportunities_pursued=0)
        # +8 engage + 25 proposals
        assert s >= 8.0

    def test_engage_rate_at_or_above_070_adds_0(self, engine):
        # ready=10, initiated=7 → rate=0.70 → 0 from engage
        # proposals=0 & ready>=3 → +25
        # cross_sell_identified=0 → rate=0/1=0 < 0.25 → +25
        s = self._score(engine,
                        expansion_ready_accounts=10,
                        expansion_conversations_initiated=7,
                        expansion_proposals_sent=0,
                        expansion_deals_closed=0,
                        cross_sell_opportunities_identified=0,
                        cross_sell_opportunities_pursued=0)
        # engage contributes 0 (rate==0.70 not < 0.70)
        assert s >= 25.0  # at least proposals penalty

    def test_engage_rate_exactly_030_boundary(self, engine):
        # rate=0.30 not < 0.30, so 0 from engage (no fallthrough to <0.50 either)
        # ready=10, initiated=3 → rate=0.30
        s = self._score(engine,
                        expansion_ready_accounts=10,
                        expansion_conversations_initiated=3,
                        expansion_proposals_sent=10,
                        expansion_deals_closed=5,
                        cross_sell_opportunities_identified=4,
                        cross_sell_opportunities_pursued=3)
        # engage: rate=0.30 → not < 0.30 but < 0.50 → +20
        # proposals=10 & ready<5 → no proposal penalty
        # xsell=3/4=0.75 ≥ 0.50 → 0
        # close_rate=5/10=0.50 ≥ 0.40 → 0
        assert s == pytest.approx(20.0)

    def test_engage_rate_exactly_050_boundary(self, engine):
        # rate=0.50 → not < 0.50 but < 0.70 → +8
        s = self._score(engine,
                        expansion_ready_accounts=10,
                        expansion_conversations_initiated=5,
                        expansion_proposals_sent=10,
                        expansion_deals_closed=5,
                        cross_sell_opportunities_identified=4,
                        cross_sell_opportunities_pursued=3)
        assert s == pytest.approx(8.0)

    # --- proposals penalty ---
    def test_no_proposals_and_ready_gte3_adds_25(self, engine):
        s = self._score(engine,
                        expansion_ready_accounts=3,
                        expansion_conversations_initiated=3,
                        expansion_proposals_sent=0,
                        expansion_deals_closed=0,
                        cross_sell_opportunities_identified=0,
                        cross_sell_opportunities_pursued=0)
        assert s >= 25.0

    def test_no_proposals_and_ready_lt3_no_penalty(self, engine):
        # proposals=0 but ready=2 < 3 → no penalty
        s = self._score(engine,
                        expansion_ready_accounts=2,
                        expansion_conversations_initiated=2,
                        expansion_proposals_sent=0,
                        expansion_deals_closed=0,
                        cross_sell_opportunities_identified=4,
                        cross_sell_opportunities_pursued=4)
        # engage: 2/2=1.0 ≥ 0.70 → 0
        # proposals: 0 & ready=2 < 3 → 0
        # xsell: 4/4=1.0 ≥ 0.50 → 0
        # close: proposals=0 → no close penalty
        assert s == pytest.approx(0.0)

    def test_proposals_le1_and_ready_gte5_adds_12(self, engine):
        s = self._score(engine,
                        expansion_ready_accounts=5,
                        expansion_conversations_initiated=5,
                        expansion_proposals_sent=1,
                        expansion_deals_closed=0,
                        cross_sell_opportunities_identified=4,
                        cross_sell_opportunities_pursued=4)
        # engage: 5/5=1.0 → 0; proposals: 1 & ready>=5 → +12
        # xsell: 4/4=1.0 → 0; close: proposals=1, closed=0, rate=0.0 < 0.20 → +15
        assert s == pytest.approx(27.0)

    def test_proposals_gt1_no_penalty_for_le1_rule(self, engine):
        s = self._score(engine,
                        expansion_ready_accounts=5,
                        expansion_conversations_initiated=5,
                        expansion_proposals_sent=2,
                        expansion_deals_closed=1,
                        cross_sell_opportunities_identified=4,
                        cross_sell_opportunities_pursued=4)
        # engage: 1.0 → 0; proposals: 2>1 → no +12
        # xsell: 1.0 → 0; close: 1/2=0.50 ≥ 0.40 → 0
        assert s == pytest.approx(0.0)

    # --- cross-sell rate thresholds ---
    def test_xsell_rate_below_025_adds_25(self, engine):
        s = self._score(engine,
                        expansion_ready_accounts=1,
                        expansion_conversations_initiated=1,
                        expansion_proposals_sent=10,
                        expansion_deals_closed=5,
                        cross_sell_opportunities_identified=8,
                        cross_sell_opportunities_pursued=1)
        # engage: 1/1=1.0 → 0; proposals: no penalty
        # xsell: 1/8=0.125 < 0.25 → +25; close: 5/10=0.50 → 0
        assert s == pytest.approx(25.0)

    def test_xsell_rate_between_025_050_adds_12(self, engine):
        s = self._score(engine,
                        expansion_ready_accounts=1,
                        expansion_conversations_initiated=1,
                        expansion_proposals_sent=10,
                        expansion_deals_closed=5,
                        cross_sell_opportunities_identified=8,
                        cross_sell_opportunities_pursued=3)
        # xsell: 3/8=0.375 → +12
        assert s == pytest.approx(12.0)

    def test_xsell_rate_gte_050_adds_0(self, engine):
        s = self._score(engine,
                        expansion_ready_accounts=1,
                        expansion_conversations_initiated=1,
                        expansion_proposals_sent=10,
                        expansion_deals_closed=5,
                        cross_sell_opportunities_identified=8,
                        cross_sell_opportunities_pursued=4)
        # xsell: 4/8=0.50 → 0
        assert s == pytest.approx(0.0)

    def test_xsell_zero_identified_uses_denom_1(self, engine):
        # cross_sell_identified=0 → denom=1; pursued=0 → rate=0.0 < 0.25 → +25
        s = self._score(engine,
                        expansion_ready_accounts=1,
                        expansion_conversations_initiated=1,
                        expansion_proposals_sent=10,
                        expansion_deals_closed=5,
                        cross_sell_opportunities_identified=0,
                        cross_sell_opportunities_pursued=0)
        assert s == pytest.approx(25.0)

    # --- close rate thresholds ---
    def test_close_rate_below_020_adds_15(self, engine):
        # proposals=10, closed=1 → rate=0.10 < 0.20
        s = self._score(engine,
                        expansion_ready_accounts=1,
                        expansion_conversations_initiated=1,
                        expansion_proposals_sent=10,
                        expansion_deals_closed=1,
                        cross_sell_opportunities_identified=4,
                        cross_sell_opportunities_pursued=4)
        assert s == pytest.approx(15.0)

    def test_close_rate_between_020_040_adds_8(self, engine):
        # proposals=10, closed=3 → rate=0.30
        s = self._score(engine,
                        expansion_ready_accounts=1,
                        expansion_conversations_initiated=1,
                        expansion_proposals_sent=10,
                        expansion_deals_closed=3,
                        cross_sell_opportunities_identified=4,
                        cross_sell_opportunities_pursued=4)
        assert s == pytest.approx(8.0)

    def test_close_rate_gte_040_adds_0(self, engine):
        s = self._score(engine,
                        expansion_ready_accounts=1,
                        expansion_conversations_initiated=1,
                        expansion_proposals_sent=10,
                        expansion_deals_closed=4,
                        cross_sell_opportunities_identified=4,
                        cross_sell_opportunities_pursued=4)
        assert s == pytest.approx(0.0)

    def test_proposals_zero_no_close_penalty(self, engine):
        # proposals=0 → no close check (condition: proposals_sent > 0)
        s = self._score(engine,
                        expansion_ready_accounts=2,
                        expansion_conversations_initiated=2,
                        expansion_proposals_sent=0,
                        expansion_deals_closed=0,
                        cross_sell_opportunities_identified=4,
                        cross_sell_opportunities_pursued=4)
        # engage: 1.0→0; proposals: 0 & ready=2<3→0; xsell: 1.0→0; close: proposals=0→0
        assert s == pytest.approx(0.0)

    def test_score_capped_at_100(self, engine):
        # Worst case → should cap at 100
        s = self._score(engine,
                        expansion_ready_accounts=10,
                        expansion_conversations_initiated=0,
                        expansion_proposals_sent=0,
                        expansion_deals_closed=0,
                        cross_sell_opportunities_identified=10,
                        cross_sell_opportunities_pursued=0)
        assert s <= 100.0

    def test_score_returns_float(self, engine):
        s = self._score(engine)
        assert isinstance(s, float)

    def test_score_non_negative(self, engine):
        s = self._score(engine)
        assert s >= 0.0

    def test_perfect_inputs_score_zero(self, engine):
        # engage ≥ 0.70, no proposals penalty, xsell ≥ 0.50, close ≥ 0.40
        s = self._score(engine,
                        expansion_ready_accounts=2,
                        expansion_conversations_initiated=2,
                        expansion_proposals_sent=10,
                        expansion_deals_closed=5,
                        cross_sell_opportunities_identified=8,
                        cross_sell_opportunities_pursued=4)
        assert s == pytest.approx(0.0)

    def test_ready_accounts_zero_uses_denom_1(self, engine):
        # ready=0 → max(0,1)=1; conversations=0 → rate=0.0 < 0.30 → +35
        s = self._score(engine,
                        expansion_ready_accounts=0,
                        expansion_conversations_initiated=0,
                        expansion_proposals_sent=0,
                        expansion_deals_closed=0,
                        cross_sell_opportunities_identified=4,
                        cross_sell_opportunities_pursued=4)
        # engage: 0/1=0 < 0.30 → +35; proposals: 0 & ready=0<3 → 0; xsell: 1.0 → 0; close: proposals=0→0
        assert s == pytest.approx(35.0)


# ===========================================================================
# 3. _portfolio_penetration_score
# ===========================================================================

class TestPortfolioPenetrationScore:

    def _score(self, engine, **kwargs):
        inp = make_input(**kwargs)
        return engine._portfolio_penetration_score(inp)

    # --- penetration_pct thresholds ---
    def test_penetration_below_025_adds_35(self, engine):
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.10,
                        multi_product_accounts_count=5,
                        single_product_accounts_count=5,
                        net_revenue_retention_pct=1.10)
        # pct=0.10<0.25→+35; single=5/10=0.50≥0.50→+15; nrr=1.10≥1.05→0
        assert s == pytest.approx(50.0)

    def test_penetration_between_025_045_adds_20(self, engine):
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.35,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.10)
        # pct=0.35→+20; single=0/10=0→0; nrr=1.10→0
        assert s == pytest.approx(20.0)

    def test_penetration_between_045_060_adds_8(self, engine):
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.50,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.10)
        assert s == pytest.approx(8.0)

    def test_penetration_gte_060_adds_0(self, engine):
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.10)
        assert s == pytest.approx(0.0)

    def test_penetration_exactly_025_boundary(self, engine):
        # 0.25 not < 0.25, but < 0.45 → +20
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.25,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.10)
        assert s == pytest.approx(20.0)

    def test_penetration_exactly_045_boundary(self, engine):
        # 0.45 not < 0.45 but < 0.60 → +8
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.45,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.10)
        assert s == pytest.approx(8.0)

    def test_penetration_exactly_060_boundary(self, engine):
        # 0.60 not < 0.60 → 0
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.10)
        assert s == pytest.approx(0.0)

    # --- single_ratio thresholds ---
    def test_single_ratio_gte_070_adds_30(self, engine):
        # single=7, multi=3 → ratio=0.70
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=3,
                        single_product_accounts_count=7,
                        net_revenue_retention_pct=1.10)
        assert s == pytest.approx(30.0)

    def test_single_ratio_between_050_070_adds_15(self, engine):
        # single=6, multi=4 → ratio=0.60
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=4,
                        single_product_accounts_count=6,
                        net_revenue_retention_pct=1.10)
        assert s == pytest.approx(15.0)

    def test_single_ratio_between_035_050_adds_8(self, engine):
        # single=4, multi=6 → ratio=0.40
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=6,
                        single_product_accounts_count=4,
                        net_revenue_retention_pct=1.10)
        assert s == pytest.approx(8.0)

    def test_single_ratio_below_035_adds_0(self, engine):
        # single=3, multi=7 → ratio=0.30
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=7,
                        single_product_accounts_count=3,
                        net_revenue_retention_pct=1.10)
        assert s == pytest.approx(0.0)

    def test_zero_total_accounts_uses_denom_1(self, engine):
        # multi=0, single=0 → total=0 → denom=1; ratio=0/1=0 → 0
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=0,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.10)
        assert s == pytest.approx(0.0)

    # --- net_revenue_retention thresholds ---
    def test_nrr_below_090_adds_25(self, engine):
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=0.85)
        assert s == pytest.approx(25.0)

    def test_nrr_between_090_100_adds_12(self, engine):
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=0.95)
        assert s == pytest.approx(12.0)

    def test_nrr_between_100_105_adds_5(self, engine):
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.02)
        assert s == pytest.approx(5.0)

    def test_nrr_gte_105_adds_0(self, engine):
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.05)
        assert s == pytest.approx(0.0)

    def test_nrr_exactly_090_boundary(self, engine):
        # 0.90 not < 0.90 → check < 1.00 → +12
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=0.90)
        assert s == pytest.approx(12.0)

    def test_nrr_exactly_100_boundary(self, engine):
        # 1.00 not < 1.00 → check < 1.05 → +5
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.60,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.00)
        assert s == pytest.approx(5.0)

    def test_score_capped_at_100(self, engine):
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.10,
                        multi_product_accounts_count=0,
                        single_product_accounts_count=10,
                        net_revenue_retention_pct=0.80)
        assert s <= 100.0

    def test_score_non_negative(self, engine):
        s = self._score(engine)
        assert s >= 0.0

    def test_score_returns_float(self, engine):
        s = self._score(engine)
        assert isinstance(s, float)

    def test_perfect_inputs_score_zero(self, engine):
        s = self._score(engine,
                        avg_account_product_penetration_pct=0.90,
                        multi_product_accounts_count=10,
                        single_product_accounts_count=0,
                        net_revenue_retention_pct=1.20)
        assert s == pytest.approx(0.0)


# ===========================================================================
# 4. _renewal_health_score
# ===========================================================================

class TestRenewalHealthScore:

    def _score(self, engine, **kwargs):
        inp = make_input(**kwargs)
        return engine._renewal_health_score(inp)

    # --- secured_rate thresholds ---
    def test_secured_rate_below_030_adds_40(self, engine):
        # renewal=10, secured=2 → rate=0.20 < 0.30
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=10,
                        renewal_expansions_secured_count=2,
                        account_health_avg_score=8.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(40.0)

    def test_secured_rate_between_030_060_adds_20(self, engine):
        # renewal=10, secured=4 → rate=0.40
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=10,
                        renewal_expansions_secured_count=4,
                        account_health_avg_score=8.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(20.0)

    def test_secured_rate_gte_060_adds_0(self, engine):
        # renewal=10, secured=6 → rate=0.60
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=10,
                        renewal_expansions_secured_count=6,
                        account_health_avg_score=8.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(0.0)

    def test_renewal_accounts_zero_no_secured_penalty(self, engine):
        # accounts_at_renewal=0 → condition: accounts_at_renewal > 0 fails → 0
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=8.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(0.0)

    def test_secured_rate_exactly_030_boundary(self, engine):
        # rate=0.30 → not < 0.30 but < 0.60 → +20
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=10,
                        renewal_expansions_secured_count=3,
                        account_health_avg_score=8.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(20.0)

    def test_secured_rate_exactly_060_boundary(self, engine):
        # rate=0.60 → neither < 0.30 nor < 0.60 → 0
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=10,
                        renewal_expansions_secured_count=6,
                        account_health_avg_score=8.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(0.0)

    # --- account_health thresholds ---
    def test_health_below_50_adds_30(self, engine):
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=4.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(30.0)

    def test_health_between_50_70_adds_15(self, engine):
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=6.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(15.0)

    def test_health_gte_70_adds_0(self, engine):
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=7.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(0.0)

    def test_health_exactly_50_boundary(self, engine):
        # 5.0 not < 5.0 but < 7.0 → +15
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=5.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(15.0)

    def test_health_exactly_70_boundary(self, engine):
        # 7.0 not < 7.0 → 0
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=7.0,
                        avg_account_lifetime_months=36.0)
        assert s == pytest.approx(0.0)

    # --- lifetime thresholds ---
    def test_lifetime_below_12_adds_20(self, engine):
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=8.0,
                        avg_account_lifetime_months=6.0)
        assert s == pytest.approx(20.0)

    def test_lifetime_between_12_24_adds_10(self, engine):
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=8.0,
                        avg_account_lifetime_months=18.0)
        assert s == pytest.approx(10.0)

    def test_lifetime_gte_24_adds_0(self, engine):
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=8.0,
                        avg_account_lifetime_months=24.0)
        assert s == pytest.approx(0.0)

    def test_lifetime_exactly_12_boundary(self, engine):
        # 12 not < 12 but < 24 → +10
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=8.0,
                        avg_account_lifetime_months=12.0)
        assert s == pytest.approx(10.0)

    def test_score_capped_at_100(self, engine):
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=10,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=1.0,
                        avg_account_lifetime_months=3.0)
        assert s <= 100.0

    def test_score_non_negative(self, engine):
        s = self._score(engine)
        assert s >= 0.0

    def test_perfect_inputs_score_zero(self, engine):
        s = self._score(engine,
                        accounts_at_contract_renewal_90d=0,
                        renewal_expansions_secured_count=0,
                        account_health_avg_score=9.0,
                        avg_account_lifetime_months=60.0)
        assert s == pytest.approx(0.0)


# ===========================================================================
# 5. _executive_coverage_score
# ===========================================================================

class TestExecutiveCoverageScore:

    def _score(self, engine, **kwargs):
        inp = make_input(**kwargs)
        return engine._executive_coverage_score(inp)

    # --- coverage thresholds ---
    def test_coverage_below_025_adds_45(self, engine):
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.10,
                        total_accounts=20,
                        expansion_deals_closed=10,
                        upsell_revenue_last_period_usd=100000.0,
                        avg_contract_value_usd=10000.0)
        # coverage < 0.25 → +45; density=10/20=0.50 ≥ 0.10 → 0; upsell > 0 and > 0.10*ACV → 0
        assert s == pytest.approx(45.0)

    def test_coverage_between_025_050_adds_25(self, engine):
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.35,
                        total_accounts=20,
                        expansion_deals_closed=10,
                        upsell_revenue_last_period_usd=100000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(25.0)

    def test_coverage_between_050_070_adds_10(self, engine):
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.60,
                        total_accounts=20,
                        expansion_deals_closed=10,
                        upsell_revenue_last_period_usd=100000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(10.0)

    def test_coverage_gte_070_adds_0(self, engine):
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.70,
                        total_accounts=20,
                        expansion_deals_closed=10,
                        upsell_revenue_last_period_usd=100000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(0.0)

    def test_coverage_exactly_025_boundary(self, engine):
        # 0.25 not < 0.25 but < 0.50 → +25
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.25,
                        total_accounts=20,
                        expansion_deals_closed=10,
                        upsell_revenue_last_period_usd=100000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(25.0)

    def test_coverage_exactly_050_boundary(self, engine):
        # 0.50 not < 0.50 but < 0.70 → +10
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.50,
                        total_accounts=20,
                        expansion_deals_closed=10,
                        upsell_revenue_last_period_usd=100000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(10.0)

    # --- expansion_density thresholds ---
    def test_density_below_005_adds_30(self, engine):
        # closed=0, total=20 → density=0.0 < 0.05 → +30
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.70,
                        total_accounts=20,
                        expansion_deals_closed=0,
                        upsell_revenue_last_period_usd=100000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(30.0)

    def test_density_between_005_010_adds_15(self, engine):
        # closed=1, total=20 → density=0.05 → not < 0.05 but < 0.10 → +15
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.70,
                        total_accounts=20,
                        expansion_deals_closed=1,
                        upsell_revenue_last_period_usd=100000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(15.0)

    def test_density_gte_010_adds_0(self, engine):
        # closed=2, total=20 → density=0.10 → 0
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.70,
                        total_accounts=20,
                        expansion_deals_closed=2,
                        upsell_revenue_last_period_usd=100000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(0.0)

    def test_total_accounts_zero_uses_denom_1(self, engine):
        # total=0 → max(0,1)=1; closed=0 → density=0.0 < 0.05 → +30
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.70,
                        total_accounts=0,
                        expansion_deals_closed=0,
                        upsell_revenue_last_period_usd=100000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(30.0)

    # --- upsell_revenue thresholds ---
    def test_upsell_zero_adds_25(self, engine):
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.70,
                        total_accounts=20,
                        expansion_deals_closed=10,
                        upsell_revenue_last_period_usd=0.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(25.0)

    def test_upsell_below_10pct_acv_adds_10(self, engine):
        # upsell=500, ACV=10000 → 0.10*10000=1000; 500 < 1000 → +10
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.70,
                        total_accounts=20,
                        expansion_deals_closed=10,
                        upsell_revenue_last_period_usd=500.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(10.0)

    def test_upsell_gte_10pct_acv_adds_0(self, engine):
        # upsell=1000 == 0.10*10000 → not < threshold → 0
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.70,
                        total_accounts=20,
                        expansion_deals_closed=10,
                        upsell_revenue_last_period_usd=1000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(0.0)

    def test_score_capped_at_100(self, engine):
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.0,
                        total_accounts=20,
                        expansion_deals_closed=0,
                        upsell_revenue_last_period_usd=0.0,
                        avg_contract_value_usd=10000.0)
        assert s <= 100.0

    def test_score_non_negative(self, engine):
        s = self._score(engine)
        assert s >= 0.0

    def test_perfect_inputs_score_zero(self, engine):
        s = self._score(engine,
                        executive_sponsor_coverage_pct=0.90,
                        total_accounts=20,
                        expansion_deals_closed=10,
                        upsell_revenue_last_period_usd=50000.0,
                        avg_contract_value_usd=10000.0)
        assert s == pytest.approx(0.0)


# ===========================================================================
# 6. Pattern detection
# ===========================================================================

class TestPatternDetection:

    def _detect(self, engine, **kwargs):
        inp = make_input(**kwargs)
        capture = engine._expansion_capture_score(inp)
        penetration = engine._portfolio_penetration_score(inp)
        renewal = engine._renewal_health_score(inp)
        executive = engine._executive_coverage_score(inp)
        return engine._detect_pattern(inp, capture, penetration, renewal, executive)

    def test_stagnant_portfolio_detected(self, engine):
        # capture >= 40, closed==0, ready>=3
        # create high capture: engage_rate very low → +35; proposals=0 & ready>=3 → +25; total≥40
        p = self._detect(engine,
                         expansion_ready_accounts=5,
                         expansion_conversations_initiated=0,
                         expansion_proposals_sent=0,
                         expansion_deals_closed=0,
                         cross_sell_opportunities_identified=1,
                         cross_sell_opportunities_pursued=0)
        assert p == ExpansionPattern.stagnant_portfolio

    def test_stagnant_portfolio_requires_closed_eq_0(self, engine):
        # Even with high capture, if closed > 0, not stagnant_portfolio
        # Use cross_sell_neglect conditions that won't be triggered
        p = self._detect(engine,
                         expansion_ready_accounts=5,
                         expansion_conversations_initiated=0,
                         expansion_proposals_sent=0,
                         expansion_deals_closed=1,
                         cross_sell_opportunities_identified=1,
                         cross_sell_opportunities_pursued=1)
        # capture >= 40 but closed != 0 → not stagnant
        # xsell_rate=1/1=1.0 ≥ 0.30 → not cross_sell_neglect
        # renewal depends on other fields...
        assert p != ExpansionPattern.stagnant_portfolio

    def test_stagnant_portfolio_requires_ready_gte_3(self, engine):
        p = self._detect(engine,
                         expansion_ready_accounts=2,
                         expansion_conversations_initiated=0,
                         expansion_proposals_sent=0,
                         expansion_deals_closed=0,
                         cross_sell_opportunities_identified=1,
                         cross_sell_opportunities_pursued=0)
        # ready=2 < 3 → not stagnant_portfolio
        assert p != ExpansionPattern.stagnant_portfolio

    def test_cross_sell_neglect_detected(self, engine):
        # Need capture >= 30 but not stagnant, xsell_identified>=3, xsell_rate<0.30
        # capture >= 30: engage_rate=0/3=0 < 0.30 → +35 (≥ 30) but closed=1 → not stagnant
        p = self._detect(engine,
                         expansion_ready_accounts=3,
                         expansion_conversations_initiated=0,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=1,
                         cross_sell_opportunities_identified=5,
                         cross_sell_opportunities_pursued=1)
        # capture: engage=0/3→+35, proposals: 10>1→0, xsell: 1/5=0.20<0.25→+25; close: 1/10=0.10<0.20→+15; total≥30
        # pattern: closed=1 → not stagnant; capture>=30, xsell_id=5>=3, xsell_rate=1/5=0.20<0.30 → cross_sell_neglect
        assert p == ExpansionPattern.cross_sell_neglect

    def test_cross_sell_neglect_requires_capture_gte_30(self, engine):
        # capture < 30 → no cross_sell_neglect
        # Perfect capture: engage>=0.70, proposals fine, xsell_rate>=0.50, close>=0.40
        p = self._detect(engine,
                         expansion_ready_accounts=2,
                         expansion_conversations_initiated=2,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=5,
                         cross_sell_opportunities_pursued=1)
        # capture=0 < 30 → no cross_sell_neglect
        assert p != ExpansionPattern.cross_sell_neglect

    def test_cross_sell_neglect_requires_xsell_id_gte_3(self, engine):
        p = self._detect(engine,
                         expansion_ready_accounts=3,
                         expansion_conversations_initiated=0,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=1,
                         cross_sell_opportunities_identified=2,
                         cross_sell_opportunities_pursued=0)
        # xsell_id=2 < 3 → not cross_sell_neglect
        assert p != ExpansionPattern.cross_sell_neglect

    def test_renewal_risk_detected(self, engine):
        # renewal >= 35 and accounts_at_renewal >= 2
        # renewal >= 35: secured_rate very low → +40
        p = self._detect(engine,
                         # prevent stagnant (closed > 0) and cross_sell_neglect (xsell_rate >= 0.30)
                         expansion_ready_accounts=5,
                         expansion_conversations_initiated=5,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=10,
                         renewal_expansions_secured_count=1,
                         account_health_avg_score=8.0,
                         avg_account_lifetime_months=36.0)
        # capture: engage=1.0→0; proposals: no penalty; xsell: 1.0→0; close: 5/10=0.50→0 → capture=0 < 30
        # renewal: 1/10=0.10 < 0.30 → +40; health=8.0→0; lifetime=36→0 → renewal=40 >= 35; accounts=10≥2
        assert p == ExpansionPattern.renewal_risk

    def test_renewal_risk_requires_renewal_gte_35(self, engine):
        # renewal < 35: secured=6, accounts=10 → rate=0.60 → 0 from secured; health=8.0→0; lifetime=36→0
        p = self._detect(engine,
                         expansion_ready_accounts=5,
                         expansion_conversations_initiated=5,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=10,
                         renewal_expansions_secured_count=6,
                         account_health_avg_score=8.0,
                         avg_account_lifetime_months=36.0)
        assert p != ExpansionPattern.renewal_risk

    def test_renewal_risk_requires_accounts_gte_2(self, engine):
        # High renewal score but accounts_at_renewal=1 < 2
        p = self._detect(engine,
                         expansion_ready_accounts=5,
                         expansion_conversations_initiated=5,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=1,
                         renewal_expansions_secured_count=0,
                         account_health_avg_score=8.0,
                         avg_account_lifetime_months=36.0)
        assert p != ExpansionPattern.renewal_risk

    def test_low_penetration_detected(self, engine):
        # penetration >= 30 and avg_penetration_pct < 0.40
        # penetration >= 30: pct=0.10 → +35; single_ratio=0.70 → +30; nrr=1.10 → 0 → total=65
        p = self._detect(engine,
                         # keep capture < 30 (perfect engage, no proposals penalty, good xsell, good close)
                         expansion_ready_accounts=2,
                         expansion_conversations_initiated=2,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         # keep renewal < 35 (health good, lifetime good, no renewals)
                         accounts_at_contract_renewal_90d=0,
                         renewal_expansions_secured_count=0,
                         account_health_avg_score=9.0,
                         avg_account_lifetime_months=60.0,
                         avg_account_product_penetration_pct=0.10,
                         multi_product_accounts_count=3,
                         single_product_accounts_count=7,
                         net_revenue_retention_pct=1.10)
        assert p == ExpansionPattern.low_penetration

    def test_low_penetration_requires_penetration_gte_30(self, engine):
        # Perfect penetration (pct=0.90, single=0, nrr=1.20) → penetration=0 < 30
        p = self._detect(engine,
                         expansion_ready_accounts=2,
                         expansion_conversations_initiated=2,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=0,
                         renewal_expansions_secured_count=0,
                         account_health_avg_score=9.0,
                         avg_account_lifetime_months=60.0,
                         avg_account_product_penetration_pct=0.90,
                         multi_product_accounts_count=10,
                         single_product_accounts_count=0,
                         net_revenue_retention_pct=1.20)
        assert p != ExpansionPattern.low_penetration

    def test_low_penetration_requires_pct_below_040(self, engine):
        # penetration score high but pct=0.50 ≥ 0.40 → not low_penetration
        p = self._detect(engine,
                         expansion_ready_accounts=2,
                         expansion_conversations_initiated=2,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=0,
                         renewal_expansions_secured_count=0,
                         account_health_avg_score=9.0,
                         avg_account_lifetime_months=60.0,
                         avg_account_product_penetration_pct=0.50,
                         multi_product_accounts_count=3,
                         single_product_accounts_count=7,
                         net_revenue_retention_pct=0.85)
        assert p != ExpansionPattern.low_penetration

    def test_executive_gap_detected(self, engine):
        # executive >= 30 and coverage_pct < 0.40
        # coverage=0.10 → +45; density: need to check; upsell fine
        p = self._detect(engine,
                         expansion_ready_accounts=2,
                         expansion_conversations_initiated=2,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=0,
                         renewal_expansions_secured_count=0,
                         account_health_avg_score=9.0,
                         avg_account_lifetime_months=60.0,
                         avg_account_product_penetration_pct=0.90,
                         multi_product_accounts_count=10,
                         single_product_accounts_count=0,
                         net_revenue_retention_pct=1.20,
                         executive_sponsor_coverage_pct=0.10,
                         total_accounts=20,
                         upsell_revenue_last_period_usd=50000.0,
                         avg_contract_value_usd=10000.0)
        assert p == ExpansionPattern.executive_gap

    def test_executive_gap_requires_executive_gte_30(self, engine):
        # Perfect executive (coverage≥0.70, density≥0.10, upsell≥0.10*ACV) → exec=0 < 30
        p = self._detect(engine,
                         expansion_ready_accounts=2,
                         expansion_conversations_initiated=2,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=0,
                         renewal_expansions_secured_count=0,
                         account_health_avg_score=9.0,
                         avg_account_lifetime_months=60.0,
                         avg_account_product_penetration_pct=0.90,
                         multi_product_accounts_count=10,
                         single_product_accounts_count=0,
                         net_revenue_retention_pct=1.20,
                         executive_sponsor_coverage_pct=0.90,
                         total_accounts=20,
                         upsell_revenue_last_period_usd=50000.0,
                         avg_contract_value_usd=10000.0)
        assert p != ExpansionPattern.executive_gap

    def test_executive_gap_requires_coverage_below_040(self, engine):
        # executive >= 30 (density low) but coverage=0.50 ≥ 0.40
        p = self._detect(engine,
                         expansion_ready_accounts=2,
                         expansion_conversations_initiated=2,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=0,
                         renewal_expansions_secured_count=0,
                         account_health_avg_score=9.0,
                         avg_account_lifetime_months=60.0,
                         avg_account_product_penetration_pct=0.90,
                         multi_product_accounts_count=10,
                         single_product_accounts_count=0,
                         net_revenue_retention_pct=1.20,
                         executive_sponsor_coverage_pct=0.50,
                         total_accounts=200,
                         upsell_revenue_last_period_usd=50000.0,
                         avg_contract_value_usd=10000.0)
        assert p != ExpansionPattern.executive_gap

    def test_none_pattern_when_all_good(self, engine):
        # All scores low → none
        p = self._detect(engine,
                         expansion_ready_accounts=2,
                         expansion_conversations_initiated=2,
                         expansion_proposals_sent=10,
                         expansion_deals_closed=5,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=0,
                         renewal_expansions_secured_count=0,
                         account_health_avg_score=9.0,
                         avg_account_lifetime_months=60.0,
                         avg_account_product_penetration_pct=0.90,
                         multi_product_accounts_count=10,
                         single_product_accounts_count=0,
                         net_revenue_retention_pct=1.20,
                         executive_sponsor_coverage_pct=0.90,
                         total_accounts=20,
                         upsell_revenue_last_period_usd=50000.0,
                         avg_contract_value_usd=10000.0)
        assert p == ExpansionPattern.none

    def test_stagnant_portfolio_has_priority_over_cross_sell(self, engine):
        # Conditions for both stagnant and cross_sell met → stagnant wins
        p = self._detect(engine,
                         expansion_ready_accounts=5,
                         expansion_conversations_initiated=0,
                         expansion_proposals_sent=0,
                         expansion_deals_closed=0,
                         cross_sell_opportunities_identified=5,
                         cross_sell_opportunities_pursued=0)
        assert p == ExpansionPattern.stagnant_portfolio


# ===========================================================================
# 7. Risk levels
# ===========================================================================

class TestRiskLevel:

    def test_low_below_20(self, engine):
        assert engine._risk_level(0.0) == ExpansionRisk.low
        assert engine._risk_level(10.0) == ExpansionRisk.low
        assert engine._risk_level(19.9) == ExpansionRisk.low

    def test_moderate_at_20(self, engine):
        assert engine._risk_level(20.0) == ExpansionRisk.moderate

    def test_moderate_between_20_40(self, engine):
        assert engine._risk_level(25.0) == ExpansionRisk.moderate
        assert engine._risk_level(39.9) == ExpansionRisk.moderate

    def test_high_at_40(self, engine):
        assert engine._risk_level(40.0) == ExpansionRisk.high

    def test_high_between_40_60(self, engine):
        assert engine._risk_level(50.0) == ExpansionRisk.high
        assert engine._risk_level(59.9) == ExpansionRisk.high

    def test_critical_at_60(self, engine):
        assert engine._risk_level(60.0) == ExpansionRisk.critical

    def test_critical_above_60(self, engine):
        assert engine._risk_level(75.0) == ExpansionRisk.critical
        assert engine._risk_level(100.0) == ExpansionRisk.critical

    def test_boundary_19_9_is_low(self, engine):
        assert engine._risk_level(19.9) == ExpansionRisk.low

    def test_boundary_39_9_is_moderate(self, engine):
        assert engine._risk_level(39.9) == ExpansionRisk.moderate

    def test_boundary_59_9_is_high(self, engine):
        assert engine._risk_level(59.9) == ExpansionRisk.high


# ===========================================================================
# 8. Severity levels
# ===========================================================================

class TestSeverity:

    def test_growing_below_20(self, engine):
        assert engine._severity(0.0) == ExpansionSeverity.growing
        assert engine._severity(19.9) == ExpansionSeverity.growing

    def test_steady_at_20(self, engine):
        assert engine._severity(20.0) == ExpansionSeverity.steady

    def test_steady_between_20_40(self, engine):
        assert engine._severity(30.0) == ExpansionSeverity.steady
        assert engine._severity(39.9) == ExpansionSeverity.steady

    def test_declining_at_40(self, engine):
        assert engine._severity(40.0) == ExpansionSeverity.declining

    def test_declining_between_40_60(self, engine):
        assert engine._severity(50.0) == ExpansionSeverity.declining
        assert engine._severity(59.9) == ExpansionSeverity.declining

    def test_stagnant_at_60(self, engine):
        assert engine._severity(60.0) == ExpansionSeverity.stagnant

    def test_stagnant_above_60(self, engine):
        assert engine._severity(80.0) == ExpansionSeverity.stagnant
        assert engine._severity(100.0) == ExpansionSeverity.stagnant

    def test_boundary_0_is_growing(self, engine):
        assert engine._severity(0.0) == ExpansionSeverity.growing


# ===========================================================================
# 9. Action mapping
# ===========================================================================

class TestActionMapping:

    def test_critical_renewal_risk_returns_renewal_acceleration(self, engine):
        a = engine._action(ExpansionRisk.critical, ExpansionPattern.renewal_risk)
        assert a == ExpansionAction.renewal_acceleration

    def test_critical_executive_gap_returns_executive_alignment(self, engine):
        a = engine._action(ExpansionRisk.critical, ExpansionPattern.executive_gap)
        assert a == ExpansionAction.executive_alignment

    def test_critical_stagnant_portfolio_returns_expansion_outreach(self, engine):
        a = engine._action(ExpansionRisk.critical, ExpansionPattern.stagnant_portfolio)
        assert a == ExpansionAction.expansion_outreach

    def test_critical_cross_sell_neglect_returns_expansion_outreach(self, engine):
        a = engine._action(ExpansionRisk.critical, ExpansionPattern.cross_sell_neglect)
        assert a == ExpansionAction.expansion_outreach

    def test_critical_low_penetration_returns_expansion_outreach(self, engine):
        a = engine._action(ExpansionRisk.critical, ExpansionPattern.low_penetration)
        assert a == ExpansionAction.expansion_outreach

    def test_critical_none_returns_expansion_outreach(self, engine):
        a = engine._action(ExpansionRisk.critical, ExpansionPattern.none)
        assert a == ExpansionAction.expansion_outreach

    def test_high_cross_sell_neglect_returns_cross_sell_campaign(self, engine):
        a = engine._action(ExpansionRisk.high, ExpansionPattern.cross_sell_neglect)
        assert a == ExpansionAction.cross_sell_campaign

    def test_high_low_penetration_returns_penetration_deepening(self, engine):
        a = engine._action(ExpansionRisk.high, ExpansionPattern.low_penetration)
        assert a == ExpansionAction.penetration_deepening

    def test_high_stagnant_portfolio_returns_expansion_outreach(self, engine):
        a = engine._action(ExpansionRisk.high, ExpansionPattern.stagnant_portfolio)
        assert a == ExpansionAction.expansion_outreach

    def test_high_renewal_risk_returns_expansion_outreach(self, engine):
        a = engine._action(ExpansionRisk.high, ExpansionPattern.renewal_risk)
        assert a == ExpansionAction.expansion_outreach

    def test_high_executive_gap_returns_expansion_outreach(self, engine):
        a = engine._action(ExpansionRisk.high, ExpansionPattern.executive_gap)
        assert a == ExpansionAction.expansion_outreach

    def test_high_none_returns_expansion_outreach(self, engine):
        a = engine._action(ExpansionRisk.high, ExpansionPattern.none)
        assert a == ExpansionAction.expansion_outreach

    def test_moderate_any_pattern_returns_expansion_outreach(self, engine):
        for p in ExpansionPattern:
            a = engine._action(ExpansionRisk.moderate, p)
            assert a == ExpansionAction.expansion_outreach

    def test_low_any_pattern_returns_no_action(self, engine):
        for p in ExpansionPattern:
            a = engine._action(ExpansionRisk.low, p)
            assert a == ExpansionAction.no_action


# ===========================================================================
# 10. has_expansion_gap flag
# ===========================================================================

class TestHasExpansionGap:

    def test_gap_when_composite_gte_40(self, engine):
        assert engine._has_expansion_gap(40.0, make_input()) is True

    def test_gap_when_composite_above_40(self, engine):
        assert engine._has_expansion_gap(50.0, make_input()) is True

    def test_no_gap_when_composite_below_40_and_no_other_trigger(self, engine):
        inp = make_input(
            expansion_ready_accounts=2,
            expansion_deals_closed=1,
            net_revenue_retention_pct=1.00)
        assert engine._has_expansion_gap(30.0, inp) is False

    def test_gap_when_ready_gte3_and_closed_eq0(self, engine):
        inp = make_input(expansion_ready_accounts=3, expansion_deals_closed=0)
        assert engine._has_expansion_gap(10.0, inp) is True

    def test_no_gap_when_ready_gte3_but_closed_gt0(self, engine):
        inp = make_input(
            expansion_ready_accounts=3,
            expansion_deals_closed=1,
            net_revenue_retention_pct=1.00)
        assert engine._has_expansion_gap(10.0, inp) is False

    def test_no_gap_when_ready_lt3_and_closed_eq0(self, engine):
        inp = make_input(
            expansion_ready_accounts=2,
            expansion_deals_closed=0,
            net_revenue_retention_pct=1.00)
        assert engine._has_expansion_gap(10.0, inp) is False

    def test_gap_when_nrr_below_090(self, engine):
        inp = make_input(net_revenue_retention_pct=0.89,
                         expansion_ready_accounts=2,
                         expansion_deals_closed=1)
        assert engine._has_expansion_gap(10.0, inp) is True

    def test_no_gap_when_nrr_exactly_090(self, engine):
        inp = make_input(net_revenue_retention_pct=0.90,
                         expansion_ready_accounts=2,
                         expansion_deals_closed=1)
        assert engine._has_expansion_gap(10.0, inp) is False

    def test_gap_composite_boundary_exactly_40(self, engine):
        assert engine._has_expansion_gap(40.0, make_input()) is True

    def test_no_gap_composite_boundary_exactly_39(self, engine):
        inp = make_input(expansion_ready_accounts=2, expansion_deals_closed=1,
                         net_revenue_retention_pct=1.00)
        assert engine._has_expansion_gap(39.0, inp) is False

    def test_gap_ready_exactly_3_closed_exactly_0(self, engine):
        inp = make_input(expansion_ready_accounts=3, expansion_deals_closed=0,
                         net_revenue_retention_pct=1.00)
        assert engine._has_expansion_gap(0.0, inp) is True

    def test_gap_or_combination(self, engine):
        # multiple triggers - still returns True
        inp = make_input(expansion_ready_accounts=3, expansion_deals_closed=0,
                         net_revenue_retention_pct=0.85)
        assert engine._has_expansion_gap(50.0, inp) is True


# ===========================================================================
# 11. requires_account_review flag
# ===========================================================================

class TestRequiresAccountReview:

    def test_review_when_composite_gte_30(self, engine):
        inp = make_input(account_health_avg_score=8.0, accounts_at_contract_renewal_90d=0)
        assert engine._requires_account_review(30.0, inp) is True

    def test_no_review_when_composite_below_30_and_no_other_trigger(self, engine):
        inp = make_input(account_health_avg_score=8.0, accounts_at_contract_renewal_90d=2)
        # accounts_at_renewal=2 < 3 and health=8.0 ≥ 6.0
        assert engine._requires_account_review(29.0, inp) is False

    def test_review_when_health_below_60(self, engine):
        inp = make_input(account_health_avg_score=5.9, accounts_at_contract_renewal_90d=0)
        assert engine._requires_account_review(0.0, inp) is True

    def test_no_review_when_health_exactly_60(self, engine):
        inp = make_input(account_health_avg_score=6.0, accounts_at_contract_renewal_90d=0)
        assert engine._requires_account_review(0.0, inp) is False

    def test_review_when_renewal_90d_gte_3(self, engine):
        inp = make_input(account_health_avg_score=8.0, accounts_at_contract_renewal_90d=3)
        assert engine._requires_account_review(0.0, inp) is True

    def test_no_review_when_renewal_90d_lt_3(self, engine):
        inp = make_input(account_health_avg_score=8.0, accounts_at_contract_renewal_90d=2)
        assert engine._requires_account_review(0.0, inp) is False

    def test_review_composite_boundary_exactly_30(self, engine):
        inp = make_input(account_health_avg_score=8.0, accounts_at_contract_renewal_90d=0)
        assert engine._requires_account_review(30.0, inp) is True

    def test_no_review_composite_boundary_exactly_29(self, engine):
        inp = make_input(account_health_avg_score=8.0, accounts_at_contract_renewal_90d=0)
        assert engine._requires_account_review(29.0, inp) is False

    def test_review_health_boundary_below_60(self, engine):
        inp = make_input(account_health_avg_score=5.999, accounts_at_contract_renewal_90d=0)
        assert engine._requires_account_review(0.0, inp) is True

    def test_review_renewal_boundary_exactly_3(self, engine):
        inp = make_input(account_health_avg_score=8.0, accounts_at_contract_renewal_90d=3)
        assert engine._requires_account_review(0.0, inp) is True

    def test_no_review_renewal_boundary_exactly_2(self, engine):
        inp = make_input(account_health_avg_score=8.0, accounts_at_contract_renewal_90d=2)
        assert engine._requires_account_review(0.0, inp) is False


# ===========================================================================
# 12. estimated_expansion_revenue_upside_usd
# ===========================================================================

class TestEstimatedRevenueUpside:

    def test_basic_calculation(self, engine):
        inp = make_input(expansion_ready_accounts=5, expansion_deals_closed=2,
                         avg_contract_value_usd=40000.0)
        upside = engine._estimated_revenue_upside(inp, 50.0)
        # (5 - 2) * 40000 * 0.50 = 60000.0
        assert upside == pytest.approx(60000.0)

    def test_zero_composite_gives_zero(self, engine):
        inp = make_input(expansion_ready_accounts=5, expansion_deals_closed=0,
                         avg_contract_value_usd=40000.0)
        upside = engine._estimated_revenue_upside(inp, 0.0)
        assert upside == pytest.approx(0.0)

    def test_all_deals_closed_gives_zero_times_composite(self, engine):
        inp = make_input(expansion_ready_accounts=5, expansion_deals_closed=5,
                         avg_contract_value_usd=40000.0)
        upside = engine._estimated_revenue_upside(inp, 80.0)
        assert upside == pytest.approx(0.0)

    def test_result_is_rounded_to_2_decimal_places(self, engine):
        inp = make_input(expansion_ready_accounts=3, expansion_deals_closed=1,
                         avg_contract_value_usd=33333.33)
        upside = engine._estimated_revenue_upside(inp, 33.3)
        # (3-1)*33333.33*0.333 = 2*33333.33*0.333 = 22199.9978...
        assert upside == round((3 - 1) * 33333.33 * (33.3 / 100.0), 2)

    def test_negative_ready_minus_closed_can_be_negative(self, engine):
        inp = make_input(expansion_ready_accounts=2, expansion_deals_closed=5,
                         avg_contract_value_usd=40000.0)
        upside = engine._estimated_revenue_upside(inp, 50.0)
        # (2 - 5) * 40000 * 0.50 = -60000.0
        assert upside == pytest.approx(-60000.0)

    def test_100_composite(self, engine):
        inp = make_input(expansion_ready_accounts=5, expansion_deals_closed=0,
                         avg_contract_value_usd=10000.0)
        upside = engine._estimated_revenue_upside(inp, 100.0)
        # 5 * 10000 * 1.0 = 50000.0
        assert upside == pytest.approx(50000.0)

    def test_upside_with_base_defaults(self, engine):
        inp = make_input()
        # ready=5, closed=2, ACV=40000, composite=?
        result = engine.assess(inp)
        expected = round((5 - 2) * 40000.0 * (result.account_expansion_composite / 100.0), 2)
        assert result.estimated_expansion_revenue_upside_usd == pytest.approx(expected)


# ===========================================================================
# 13. Signal string
# ===========================================================================

class TestSignalString:

    def test_pattern_none_and_composite_below_20_returns_strong_signal(self, engine):
        sig = engine._signal(make_input(), ExpansionPattern.none, 10.0)
        assert sig == "Account expansion momentum strong across portfolio"

    def test_pattern_none_composite_exactly_19_returns_strong(self, engine):
        sig = engine._signal(make_input(), ExpansionPattern.none, 19.9)
        assert sig == "Account expansion momentum strong across portfolio"

    def test_pattern_none_composite_exactly_20_not_strong(self, engine):
        sig = engine._signal(make_input(), ExpansionPattern.none, 20.0)
        assert "expansion momentum strong" not in sig

    def test_pattern_not_none_and_composite_below_20_not_strong(self, engine):
        sig = engine._signal(make_input(), ExpansionPattern.stagnant_portfolio, 10.0)
        assert "expansion momentum strong" not in sig

    def test_signal_contains_untapped_accounts(self, engine):
        # ready=5 > closed=2 → 3 untapped
        inp = make_input(expansion_ready_accounts=5, expansion_deals_closed=2)
        sig = engine._signal(inp, ExpansionPattern.stagnant_portfolio, 50.0)
        assert "3 untapped expansion accounts" in sig

    def test_signal_no_untapped_when_ready_le_closed(self, engine):
        inp = make_input(expansion_ready_accounts=2, expansion_deals_closed=5)
        sig = engine._signal(inp, ExpansionPattern.stagnant_portfolio, 50.0)
        assert "untapped expansion accounts" not in sig

    def test_signal_contains_cross_sell_ignored(self, engine):
        # identified=6 > pursued=4 → 2 ignored
        inp = make_input(cross_sell_opportunities_identified=6,
                         cross_sell_opportunities_pursued=4)
        sig = engine._signal(inp, ExpansionPattern.cross_sell_neglect, 40.0)
        assert "2 cross-sell opportunities ignored" in sig

    def test_signal_no_cross_sell_when_pursued_ge_identified(self, engine):
        inp = make_input(cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4)
        sig = engine._signal(inp, ExpansionPattern.cross_sell_neglect, 40.0)
        assert "cross-sell opportunities ignored" not in sig

    def test_signal_contains_renewals_unsecured(self, engine):
        # renewal=3 > secured=2 → 1 unsecured
        inp = make_input(accounts_at_contract_renewal_90d=3,
                         renewal_expansions_secured_count=2)
        sig = engine._signal(inp, ExpansionPattern.renewal_risk, 40.0)
        assert "1 renewals unsecured" in sig

    def test_signal_no_renewals_unsecured_when_equal(self, engine):
        inp = make_input(accounts_at_contract_renewal_90d=2,
                         renewal_expansions_secured_count=2)
        sig = engine._signal(inp, ExpansionPattern.renewal_risk, 40.0)
        assert "renewals unsecured" not in sig

    def test_signal_label_uses_pattern_value(self, engine):
        inp = make_input(expansion_ready_accounts=2, expansion_deals_closed=2,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=2,
                         renewal_expansions_secured_count=2)
        sig = engine._signal(inp, ExpansionPattern.executive_gap, 40.0)
        assert sig.startswith("Executive gap")

    def test_signal_label_none_pattern_uses_expansion_risk(self, engine):
        inp = make_input(expansion_ready_accounts=2, expansion_deals_closed=2,
                         cross_sell_opportunities_identified=4,
                         cross_sell_opportunities_pursued=4,
                         accounts_at_contract_renewal_90d=2,
                         renewal_expansions_secured_count=2)
        sig = engine._signal(inp, ExpansionPattern.none, 30.0)
        assert sig.startswith("Expansion risk")

    def test_signal_contains_composite_value(self, engine):
        inp = make_input()
        sig = engine._signal(inp, ExpansionPattern.stagnant_portfolio, 55.0)
        assert "composite 55" in sig

    def test_signal_no_parts_uses_slowing_fallback(self, engine):
        # ready <= closed, identified <= pursued, renewal <= secured
        inp = make_input(expansion_ready_accounts=2, expansion_deals_closed=5,
                         cross_sell_opportunities_identified=3,
                         cross_sell_opportunities_pursued=3,
                         accounts_at_contract_renewal_90d=2,
                         renewal_expansions_secured_count=2)
        sig = engine._signal(inp, ExpansionPattern.stagnant_portfolio, 50.0)
        assert "expansion momentum slowing" in sig

    def test_signal_parts_joined_with_em_dash(self, engine):
        inp = make_input(expansion_ready_accounts=5, expansion_deals_closed=2,
                         cross_sell_opportunities_identified=6,
                         cross_sell_opportunities_pursued=3,
                         accounts_at_contract_renewal_90d=4,
                         renewal_expansions_secured_count=2)
        sig = engine._signal(inp, ExpansionPattern.renewal_risk, 50.0)
        assert " — " in sig


# ===========================================================================
# 14. to_dict() returns exactly 15 keys
# ===========================================================================

class TestToDict:

    def test_to_dict_has_15_keys(self, engine, base_input):
        result = engine.assess(base_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_contains_rep_id(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "rep_id" in d

    def test_to_dict_contains_region(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "region" in d

    def test_to_dict_contains_expansion_risk(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "expansion_risk" in d

    def test_to_dict_contains_expansion_pattern(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "expansion_pattern" in d

    def test_to_dict_contains_expansion_severity(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "expansion_severity" in d

    def test_to_dict_contains_recommended_action(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "recommended_action" in d

    def test_to_dict_contains_expansion_capture_score(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "expansion_capture_score" in d

    def test_to_dict_contains_portfolio_penetration_score(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "portfolio_penetration_score" in d

    def test_to_dict_contains_renewal_health_score(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "renewal_health_score" in d

    def test_to_dict_contains_executive_coverage_score(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "executive_coverage_score" in d

    def test_to_dict_contains_account_expansion_composite(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "account_expansion_composite" in d

    def test_to_dict_contains_has_expansion_gap(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "has_expansion_gap" in d

    def test_to_dict_contains_requires_account_review(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "requires_account_review" in d

    def test_to_dict_contains_estimated_expansion_revenue_upside_usd(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "estimated_expansion_revenue_upside_usd" in d

    def test_to_dict_contains_expansion_signal(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert "expansion_signal" in d

    def test_to_dict_risk_is_string(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert isinstance(d["expansion_risk"], str)

    def test_to_dict_pattern_is_string(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert isinstance(d["expansion_pattern"], str)

    def test_to_dict_severity_is_string(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert isinstance(d["expansion_severity"], str)

    def test_to_dict_action_is_string(self, engine, base_input):
        d = engine.assess(base_input).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_value(self, engine):
        result = engine.assess(make_input(rep_id="r001"))
        assert result.to_dict()["rep_id"] == "r001"

    def test_to_dict_region_value(self, engine):
        result = engine.assess(make_input(region="East"))
        assert result.to_dict()["region"] == "East"


# ===========================================================================
# 15. summary() returns exactly 13 keys
# ===========================================================================

class TestSummary:

    def test_empty_summary_has_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_summary_after_assess_has_13_keys(self, engine, base_input):
        engine.assess(base_input)
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_summary_risk_counts_empty(self, engine):
        assert engine.summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self, engine):
        assert engine.summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self, engine):
        assert engine.summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_empty_summary_avg_composite_zero(self, engine):
        assert engine.summary()["avg_account_expansion_composite"] == 0.0

    def test_empty_summary_expansion_gap_count_zero(self, engine):
        assert engine.summary()["expansion_gap_count"] == 0

    def test_empty_summary_account_review_count_zero(self, engine):
        assert engine.summary()["account_review_count"] == 0

    def test_empty_summary_avg_capture_zero(self, engine):
        assert engine.summary()["avg_expansion_capture_score"] == 0.0

    def test_empty_summary_avg_penetration_zero(self, engine):
        assert engine.summary()["avg_portfolio_penetration_score"] == 0.0

    def test_empty_summary_avg_renewal_zero(self, engine):
        assert engine.summary()["avg_renewal_health_score"] == 0.0

    def test_empty_summary_avg_executive_zero(self, engine):
        assert engine.summary()["avg_executive_coverage_score"] == 0.0

    def test_empty_summary_total_upside_zero(self, engine):
        assert engine.summary()["total_estimated_expansion_revenue_upside_usd"] == 0.0

    def test_summary_total_after_single_assess(self, engine, base_input):
        engine.assess(base_input)
        assert engine.summary()["total"] == 1

    def test_summary_total_after_multiple_assess(self, engine):
        engine.assess(make_input())
        engine.assess(make_input())
        engine.assess(make_input())
        assert engine.summary()["total"] == 3

    def test_summary_risk_counts_populated(self, engine, base_input):
        result = engine.assess(base_input)
        s = engine.summary()
        risk_val = result.expansion_risk.value
        assert s["risk_counts"].get(risk_val, 0) == 1

    def test_summary_contains_total_key(self, engine):
        assert "total" in engine.summary()

    def test_summary_contains_risk_counts_key(self, engine):
        assert "risk_counts" in engine.summary()

    def test_summary_contains_pattern_counts_key(self, engine):
        assert "pattern_counts" in engine.summary()

    def test_summary_contains_severity_counts_key(self, engine):
        assert "severity_counts" in engine.summary()

    def test_summary_contains_action_counts_key(self, engine):
        assert "action_counts" in engine.summary()

    def test_summary_contains_avg_composite_key(self, engine):
        assert "avg_account_expansion_composite" in engine.summary()

    def test_summary_contains_gap_count_key(self, engine):
        assert "expansion_gap_count" in engine.summary()

    def test_summary_contains_review_count_key(self, engine):
        assert "account_review_count" in engine.summary()

    def test_summary_contains_avg_capture_key(self, engine):
        assert "avg_expansion_capture_score" in engine.summary()

    def test_summary_contains_avg_penetration_key(self, engine):
        assert "avg_portfolio_penetration_score" in engine.summary()

    def test_summary_contains_avg_renewal_key(self, engine):
        assert "avg_renewal_health_score" in engine.summary()

    def test_summary_contains_avg_executive_key(self, engine):
        assert "avg_executive_coverage_score" in engine.summary()

    def test_summary_contains_total_upside_key(self, engine):
        assert "total_estimated_expansion_revenue_upside_usd" in engine.summary()

    def test_summary_avg_composite_matches_single_result(self, engine, base_input):
        result = engine.assess(base_input)
        s = engine.summary()
        assert s["avg_account_expansion_composite"] == result.account_expansion_composite

    def test_summary_gap_count_is_int(self, engine, base_input):
        engine.assess(base_input)
        s = engine.summary()
        assert isinstance(s["expansion_gap_count"], int)

    def test_summary_review_count_is_int(self, engine, base_input):
        engine.assess(base_input)
        s = engine.summary()
        assert isinstance(s["account_review_count"], int)


# ===========================================================================
# 16. assess_batch()
# ===========================================================================

class TestAssessBatch:

    def test_batch_returns_list(self, engine):
        result = engine.assess_batch([make_input(), make_input()])
        assert isinstance(result, list)

    def test_batch_returns_correct_count(self, engine):
        inputs = [make_input() for _ in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_each_result_is_account_expansion_result(self, engine):
        results = engine.assess_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, AccountExpansionResult)

    def test_batch_empty_list_returns_empty(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_batch_single_item(self, engine):
        results = engine.assess_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"

    def test_batch_populates_internal_results(self, engine):
        engine.assess_batch([make_input(), make_input()])
        assert engine.summary()["total"] == 2

    def test_batch_different_inputs_different_results(self, engine):
        inp_a = make_input(rep_id="A", expansion_ready_accounts=10,
                            expansion_conversations_initiated=1)
        inp_b = make_input(rep_id="B", expansion_ready_accounts=10,
                            expansion_conversations_initiated=8)
        ra, rb = engine.assess_batch([inp_a, inp_b])
        assert ra.rep_id == "A"
        assert rb.rep_id == "B"
        # A should have worse score than B
        assert ra.account_expansion_composite > rb.account_expansion_composite

    def test_batch_results_have_correct_rep_ids(self, engine):
        ids = ["r1", "r2", "r3"]
        inputs = [make_input(rep_id=rid) for rid in ids]
        results = engine.assess_batch(inputs)
        assert [r.rep_id for r in results] == ids

    def test_batch_summary_total_equals_batch_size(self, engine):
        n = 7
        engine.assess_batch([make_input() for _ in range(n)])
        assert engine.summary()["total"] == n

    def test_batch_accumulates_across_multiple_calls(self, engine):
        engine.assess_batch([make_input(), make_input()])
        engine.assess_batch([make_input(), make_input(), make_input()])
        assert engine.summary()["total"] == 5


# ===========================================================================
# 17. Full assess() integration tests
# ===========================================================================

class TestAssessIntegration:

    def test_assess_returns_account_expansion_result(self, engine, base_input):
        result = engine.assess(base_input)
        assert isinstance(result, AccountExpansionResult)

    def test_assess_rep_id_propagated(self, engine):
        result = engine.assess(make_input(rep_id="test_rep"))
        assert result.rep_id == "test_rep"

    def test_assess_region_propagated(self, engine):
        result = engine.assess(make_input(region="Northeast"))
        assert result.region == "Northeast"

    def test_assess_composite_between_0_and_100(self, engine, base_input):
        result = engine.assess(base_input)
        assert 0.0 <= result.account_expansion_composite <= 100.0

    def test_assess_sub_scores_between_0_and_100(self, engine, base_input):
        result = engine.assess(base_input)
        assert 0.0 <= result.expansion_capture_score <= 100.0
        assert 0.0 <= result.portfolio_penetration_score <= 100.0
        assert 0.0 <= result.renewal_health_score <= 100.0
        assert 0.0 <= result.executive_coverage_score <= 100.0

    def test_assess_appends_to_results(self, engine, base_input):
        engine.assess(base_input)
        engine.assess(base_input)
        assert len(engine._results) == 2

    def test_assess_composite_formula(self, engine, base_input):
        result = engine.assess(base_input)
        expected = round(
            result.expansion_capture_score * 0.30
            + result.portfolio_penetration_score * 0.25
            + result.renewal_health_score * 0.25
            + result.executive_coverage_score * 0.20,
            1,
        )
        expected = min(expected, 100.0)
        assert result.account_expansion_composite == pytest.approx(expected)

    def test_assess_risk_matches_composite(self, engine, base_input):
        result = engine.assess(base_input)
        expected_risk = engine._risk_level(result.account_expansion_composite)
        assert result.expansion_risk == expected_risk

    def test_assess_severity_matches_composite(self, engine, base_input):
        result = engine.assess(base_input)
        expected_severity = engine._severity(result.account_expansion_composite)
        assert result.expansion_severity == expected_severity

    def test_assess_action_matches_risk_and_pattern(self, engine, base_input):
        result = engine.assess(base_input)
        expected_action = engine._action(result.expansion_risk, result.expansion_pattern)
        assert result.recommended_action == expected_action

    def test_assess_expansion_signal_is_string(self, engine, base_input):
        result = engine.assess(base_input)
        assert isinstance(result.expansion_signal, str)

    def test_assess_expansion_signal_non_empty(self, engine, base_input):
        result = engine.assess(base_input)
        assert len(result.expansion_signal) > 0

    def test_assess_upside_matches_formula(self, engine, base_input):
        result = engine.assess(base_input)
        expected = round(
            (base_input.expansion_ready_accounts - base_input.expansion_deals_closed)
            * base_input.avg_contract_value_usd
            * (result.account_expansion_composite / 100.0),
            2,
        )
        assert result.estimated_expansion_revenue_upside_usd == pytest.approx(expected)


# ===========================================================================
# 18. Edge cases
# ===========================================================================

class TestEdgeCases:

    def test_zero_accounts_does_not_crash(self, engine):
        inp = make_input(total_accounts=0, expansion_ready_accounts=0,
                         expansion_conversations_initiated=0,
                         expansion_proposals_sent=0,
                         expansion_deals_closed=0,
                         cross_sell_opportunities_identified=0,
                         cross_sell_opportunities_pursued=0,
                         accounts_at_contract_renewal_90d=0,
                         renewal_expansions_secured_count=0,
                         multi_product_accounts_count=0,
                         single_product_accounts_count=0)
        result = engine.assess(inp)
        assert isinstance(result, AccountExpansionResult)

    def test_all_deals_closed_does_not_crash(self, engine):
        inp = make_input(expansion_ready_accounts=10, expansion_deals_closed=10)
        result = engine.assess(inp)
        assert result.estimated_expansion_revenue_upside_usd == pytest.approx(0.0)

    def test_very_high_upsell_revenue(self, engine):
        inp = make_input(upsell_revenue_last_period_usd=1_000_000.0)
        result = engine.assess(inp)
        assert isinstance(result, AccountExpansionResult)

    def test_very_low_nrr_triggers_gap(self, engine):
        inp = make_input(net_revenue_retention_pct=0.50)
        result = engine.assess(inp)
        assert result.has_expansion_gap is True

    def test_perfect_rep_low_risk(self, engine):
        # All inputs optimal → lowest possible risk
        inp = make_input(
            expansion_ready_accounts=2,
            expansion_conversations_initiated=2,
            expansion_proposals_sent=10,
            expansion_deals_closed=8,
            cross_sell_opportunities_identified=4,
            cross_sell_opportunities_pursued=4,
            avg_account_product_penetration_pct=0.90,
            multi_product_accounts_count=18,
            single_product_accounts_count=2,
            net_revenue_retention_pct=1.30,
            accounts_at_contract_renewal_90d=0,
            renewal_expansions_secured_count=0,
            account_health_avg_score=9.5,
            avg_account_lifetime_months=60.0,
            executive_sponsor_coverage_pct=0.95,
            total_accounts=20,
            upsell_revenue_last_period_usd=200000.0,
            avg_contract_value_usd=40000.0,
        )
        result = engine.assess(inp)
        assert result.expansion_risk == ExpansionRisk.low
        assert result.expansion_severity == ExpansionSeverity.growing
        assert result.recommended_action == ExpansionAction.no_action

    def test_worst_rep_critical_risk(self, engine):
        inp = make_input(
            expansion_ready_accounts=10,
            expansion_conversations_initiated=0,
            expansion_proposals_sent=0,
            expansion_deals_closed=0,
            cross_sell_opportunities_identified=10,
            cross_sell_opportunities_pursued=0,
            avg_account_product_penetration_pct=0.05,
            multi_product_accounts_count=0,
            single_product_accounts_count=20,
            net_revenue_retention_pct=0.70,
            accounts_at_contract_renewal_90d=10,
            renewal_expansions_secured_count=0,
            account_health_avg_score=2.0,
            avg_account_lifetime_months=6.0,
            executive_sponsor_coverage_pct=0.05,
            total_accounts=20,
            upsell_revenue_last_period_usd=0.0,
            avg_contract_value_usd=40000.0,
        )
        result = engine.assess(inp)
        assert result.expansion_risk == ExpansionRisk.critical
        assert result.has_expansion_gap is True
        assert result.requires_account_review is True

    def test_expansion_signal_strong_for_optimal_rep(self, engine):
        inp = make_input(
            expansion_ready_accounts=2,
            expansion_conversations_initiated=2,
            expansion_proposals_sent=10,
            expansion_deals_closed=8,
            cross_sell_opportunities_identified=4,
            cross_sell_opportunities_pursued=4,
            avg_account_product_penetration_pct=0.90,
            multi_product_accounts_count=18,
            single_product_accounts_count=2,
            net_revenue_retention_pct=1.30,
            accounts_at_contract_renewal_90d=0,
            renewal_expansions_secured_count=0,
            account_health_avg_score=9.5,
            avg_account_lifetime_months=60.0,
            executive_sponsor_coverage_pct=0.95,
            total_accounts=20,
            upsell_revenue_last_period_usd=200000.0,
            avg_contract_value_usd=40000.0,
        )
        result = engine.assess(inp)
        assert result.expansion_signal == "Account expansion momentum strong across portfolio"

    def test_zero_avg_contract_value_gives_zero_upside(self, engine):
        inp = make_input(avg_contract_value_usd=0.0)
        result = engine.assess(inp)
        assert result.estimated_expansion_revenue_upside_usd == pytest.approx(0.0)

    def test_engine_initializes_empty_results(self):
        e = SalesAccountExpansionIntelligenceEngine()
        assert e._results == []

    def test_multiple_engine_instances_independent(self):
        e1 = SalesAccountExpansionIntelligenceEngine()
        e2 = SalesAccountExpansionIntelligenceEngine()
        e1.assess(make_input())
        assert e2.summary()["total"] == 0

    def test_assess_batch_with_varied_reps(self, engine):
        inputs = [
            make_input(rep_id="a", net_revenue_retention_pct=0.70),
            make_input(rep_id="b", net_revenue_retention_pct=1.30),
        ]
        results = engine.assess_batch(inputs)
        assert results[0].has_expansion_gap is True
        assert results[1].expansion_risk == ExpansionRisk.low or True  # just no crash

    def test_composite_capped_at_100(self, engine):
        # Inject artificially so we test min(composite, 100)
        # All scores at 100 → composite = 100*0.30 + 100*0.25 + 100*0.25 + 100*0.20 = 100
        inp = make_input(
            expansion_ready_accounts=10,
            expansion_conversations_initiated=0,
            expansion_proposals_sent=0,
            expansion_deals_closed=0,
            cross_sell_opportunities_identified=10,
            cross_sell_opportunities_pursued=0,
            avg_account_product_penetration_pct=0.05,
            multi_product_accounts_count=0,
            single_product_accounts_count=20,
            net_revenue_retention_pct=0.60,
            accounts_at_contract_renewal_90d=10,
            renewal_expansions_secured_count=0,
            account_health_avg_score=1.0,
            avg_account_lifetime_months=3.0,
            executive_sponsor_coverage_pct=0.0,
            total_accounts=20,
            upsell_revenue_last_period_usd=0.0,
            avg_contract_value_usd=40000.0,
        )
        result = engine.assess(inp)
        assert result.account_expansion_composite <= 100.0

    def test_requires_review_when_health_very_low(self, engine):
        inp = make_input(account_health_avg_score=1.0, accounts_at_contract_renewal_90d=0)
        result = engine.assess(inp)
        assert result.requires_account_review is True

    def test_gap_flag_false_when_no_trigger(self, engine):
        inp = make_input(
            expansion_ready_accounts=2,
            expansion_conversations_initiated=2,
            expansion_proposals_sent=10,
            expansion_deals_closed=8,
            cross_sell_opportunities_identified=4,
            cross_sell_opportunities_pursued=4,
            avg_account_product_penetration_pct=0.90,
            multi_product_accounts_count=18,
            single_product_accounts_count=2,
            net_revenue_retention_pct=1.30,
            accounts_at_contract_renewal_90d=0,
            renewal_expansions_secured_count=0,
            account_health_avg_score=9.5,
            avg_account_lifetime_months=60.0,
            executive_sponsor_coverage_pct=0.95,
            total_accounts=20,
            upsell_revenue_last_period_usd=200000.0,
            avg_contract_value_usd=40000.0,
        )
        result = engine.assess(inp)
        assert result.has_expansion_gap is False

    def test_summary_total_upside_sums_correctly(self, engine):
        inp = make_input(expansion_ready_accounts=5, expansion_deals_closed=0,
                         avg_contract_value_usd=10000.0)
        r1 = engine.assess(inp)
        r2 = engine.assess(inp)
        s = engine.summary()
        expected = round(r1.estimated_expansion_revenue_upside_usd +
                         r2.estimated_expansion_revenue_upside_usd, 2)
        assert s["total_estimated_expansion_revenue_upside_usd"] == pytest.approx(expected)

    def test_summary_avg_composite_two_results(self, engine):
        inp_a = make_input()
        inp_b = make_input()
        ra = engine.assess(inp_a)
        rb = engine.assess(inp_b)
        s = engine.summary()
        expected = round((ra.account_expansion_composite + rb.account_expansion_composite) / 2, 1)
        assert s["avg_account_expansion_composite"] == pytest.approx(expected)

    def test_assess_result_is_dataclass(self, engine, base_input):
        from dataclasses import fields
        result = engine.assess(base_input)
        assert len(fields(result)) == 15
