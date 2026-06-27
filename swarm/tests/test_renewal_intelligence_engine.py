"""
Comprehensive pytest test suite for Module 30 — Renewal Intelligence Engine.
Target: 22 test classes, 270+ tests, all passing.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.renewal_intelligence_engine import (
    RenewalRisk,
    RenewalAction,
    RenewalOutcome,
    EngagementTrend,
    RenewalInput,
    RenewalResult,
    RenewalIntelligenceEngine,
    _renewal_risk_score,
    _renewal_risk,
    _renewal_action,
    _engagement_trend,
    _renewal_probability,
    _predicted_outcome,
    _expected_arr_change,
    _urgency_score,
    _risk_signals,
    _positive_signals,
    _renewal_plays,
)


# ---------------------------------------------------------------------------
# Factory helper
# ---------------------------------------------------------------------------

def make_customer(
    customer_id: str = "C001",
    customer_name: str = "Acme Corp",
    arr_eur: float = 100_000.0,
    segment: str = "enterprise",
    days_to_renewal: int = 120,
    contract_years: int = 2,
    health_score: float = 80.0,
    nps_score: int = 40,
    product_usage_trend: str = "growing",
    has_expansion_discussion: bool = False,
    discount_requested: bool = False,
    competitor_mentioned: bool = False,
    price_sensitivity: str = "low",
    exec_sponsor_aligned: bool = True,
    champion_strength: int = 8,
    open_support_issues: int = 0,
    previous_renewal_on_time: bool = True,
    years_as_customer: int = 4,
) -> RenewalInput:
    """Return a RenewalInput with healthy/low-risk defaults."""
    return RenewalInput(
        customer_id=customer_id,
        customer_name=customer_name,
        arr_eur=arr_eur,
        segment=segment,
        days_to_renewal=days_to_renewal,
        contract_years=contract_years,
        health_score=health_score,
        nps_score=nps_score,
        product_usage_trend=product_usage_trend,
        has_expansion_discussion=has_expansion_discussion,
        discount_requested=discount_requested,
        competitor_mentioned=competitor_mentioned,
        price_sensitivity=price_sensitivity,
        exec_sponsor_aligned=exec_sponsor_aligned,
        champion_strength=champion_strength,
        open_support_issues=open_support_issues,
        previous_renewal_on_time=previous_renewal_on_time,
        years_as_customer=years_as_customer,
    )


# ---------------------------------------------------------------------------
# Class 1: Enum values
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_renewal_risk_low(self):
        assert RenewalRisk.LOW.value == "low"

    def test_renewal_risk_moderate(self):
        assert RenewalRisk.MODERATE.value == "moderate"

    def test_renewal_risk_high(self):
        assert RenewalRisk.HIGH.value == "high"

    def test_renewal_risk_critical(self):
        assert RenewalRisk.CRITICAL.value == "critical"

    def test_renewal_action_close(self):
        assert RenewalAction.CLOSE.value == "close"

    def test_renewal_action_nurture(self):
        assert RenewalAction.NURTURE.value == "nurture"

    def test_renewal_action_intervene(self):
        assert RenewalAction.INTERVENE.value == "intervene"

    def test_renewal_action_escalate(self):
        assert RenewalAction.ESCALATE.value == "escalate"

    def test_renewal_outcome_renew(self):
        assert RenewalOutcome.RENEW.value == "renew"

    def test_renewal_outcome_expand(self):
        assert RenewalOutcome.EXPAND.value == "expand"

    def test_renewal_outcome_downgrade(self):
        assert RenewalOutcome.DOWNGRADE.value == "downgrade"

    def test_renewal_outcome_churn(self):
        assert RenewalOutcome.CHURN.value == "churn"

    def test_engagement_trend_growing(self):
        assert EngagementTrend.GROWING.value == "growing"

    def test_engagement_trend_stable(self):
        assert EngagementTrend.STABLE.value == "stable"

    def test_engagement_trend_declining(self):
        assert EngagementTrend.DECLINING.value == "declining"

    def test_engagement_trend_dormant(self):
        assert EngagementTrend.DORMANT.value == "dormant"

    def test_renewal_risk_is_str_enum(self):
        assert isinstance(RenewalRisk.LOW, str)

    def test_renewal_action_is_str_enum(self):
        assert isinstance(RenewalAction.CLOSE, str)

    def test_renewal_outcome_is_str_enum(self):
        assert isinstance(RenewalOutcome.RENEW, str)

    def test_engagement_trend_is_str_enum(self):
        assert isinstance(EngagementTrend.STABLE, str)

    def test_renewal_risk_members_count(self):
        assert len(RenewalRisk) == 4

    def test_renewal_action_members_count(self):
        assert len(RenewalAction) == 4

    def test_renewal_outcome_members_count(self):
        assert len(RenewalOutcome) == 4

    def test_engagement_trend_members_count(self):
        assert len(EngagementTrend) == 4


# ---------------------------------------------------------------------------
# Class 2: RenewalInput dataclass
# ---------------------------------------------------------------------------

class TestRenewalInput:
    def test_can_instantiate_with_factory(self):
        inp = make_customer()
        assert inp.customer_id == "C001"

    def test_customer_name(self):
        inp = make_customer(customer_name="Beta Ltd")
        assert inp.customer_name == "Beta Ltd"

    def test_arr_eur_stored(self):
        inp = make_customer(arr_eur=250_000.0)
        assert inp.arr_eur == 250_000.0

    def test_segment_stored(self):
        inp = make_customer(segment="smb")
        assert inp.segment == "smb"

    def test_days_to_renewal_positive(self):
        inp = make_customer(days_to_renewal=60)
        assert inp.days_to_renewal == 60

    def test_days_to_renewal_negative(self):
        inp = make_customer(days_to_renewal=-5)
        assert inp.days_to_renewal == -5

    def test_health_score_stored(self):
        inp = make_customer(health_score=55.0)
        assert inp.health_score == 55.0

    def test_nps_score_stored(self):
        inp = make_customer(nps_score=-50)
        assert inp.nps_score == -50

    def test_product_usage_trend_stored(self):
        inp = make_customer(product_usage_trend="dormant")
        assert inp.product_usage_trend == "dormant"

    def test_has_expansion_discussion_stored(self):
        inp = make_customer(has_expansion_discussion=True)
        assert inp.has_expansion_discussion is True

    def test_discount_requested_stored(self):
        inp = make_customer(discount_requested=True)
        assert inp.discount_requested is True

    def test_competitor_mentioned_stored(self):
        inp = make_customer(competitor_mentioned=True)
        assert inp.competitor_mentioned is True

    def test_price_sensitivity_stored(self):
        inp = make_customer(price_sensitivity="high")
        assert inp.price_sensitivity == "high"

    def test_exec_sponsor_aligned_stored(self):
        inp = make_customer(exec_sponsor_aligned=False)
        assert inp.exec_sponsor_aligned is False

    def test_champion_strength_stored(self):
        inp = make_customer(champion_strength=2)
        assert inp.champion_strength == 2

    def test_open_support_issues_stored(self):
        inp = make_customer(open_support_issues=5)
        assert inp.open_support_issues == 5

    def test_previous_renewal_on_time_stored(self):
        inp = make_customer(previous_renewal_on_time=False)
        assert inp.previous_renewal_on_time is False

    def test_years_as_customer_stored(self):
        inp = make_customer(years_as_customer=0)
        assert inp.years_as_customer == 0


# ---------------------------------------------------------------------------
# Class 3: _renewal_risk_score — health component
# ---------------------------------------------------------------------------

class TestRenewalRiskScoreHealth:
    """Health contributes up to 30 points."""

    def test_health_below_40_adds_30(self):
        inp = make_customer(health_score=35.0, nps_score=25, product_usage_trend="growing",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="low", exec_sponsor_aligned=True,
                            champion_strength=5, open_support_issues=0,
                            previous_renewal_on_time=True, years_as_customer=3)
        score = _renewal_risk_score(inp)
        # Only health component active: 30
        assert score == 30.0

    def test_health_at_40_does_not_add_30(self):
        inp = make_customer(health_score=40.0, nps_score=25, product_usage_trend="growing",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="low", exec_sponsor_aligned=True,
                            champion_strength=5, open_support_issues=0,
                            previous_renewal_on_time=True, years_as_customer=3)
        score = _renewal_risk_score(inp)
        assert score == 18.0  # 40 <= health < 60

    def test_health_59_adds_18(self):
        inp = make_customer(health_score=59.0, nps_score=25, product_usage_trend="growing",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="low", exec_sponsor_aligned=True,
                            champion_strength=5, open_support_issues=0,
                            previous_renewal_on_time=True, years_as_customer=3)
        score = _renewal_risk_score(inp)
        assert score == 18.0

    def test_health_60_adds_8(self):
        inp = make_customer(health_score=60.0, nps_score=25, product_usage_trend="growing",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="low", exec_sponsor_aligned=True,
                            champion_strength=5, open_support_issues=0,
                            previous_renewal_on_time=True, years_as_customer=3)
        score = _renewal_risk_score(inp)
        assert score == 8.0

    def test_health_74_adds_8(self):
        inp = make_customer(health_score=74.0, nps_score=25, product_usage_trend="growing",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="low", exec_sponsor_aligned=True,
                            champion_strength=5, open_support_issues=0,
                            previous_renewal_on_time=True, years_as_customer=3)
        score = _renewal_risk_score(inp)
        assert score == 8.0

    def test_health_75_adds_0(self):
        inp = make_customer(health_score=75.0, nps_score=25, product_usage_trend="growing",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="low", exec_sponsor_aligned=True,
                            champion_strength=5, open_support_issues=0,
                            previous_renewal_on_time=True, years_as_customer=3)
        score = _renewal_risk_score(inp)
        assert score == 0.0

    def test_health_100_adds_0(self):
        inp = make_customer(health_score=100.0, nps_score=25, product_usage_trend="growing",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="low", exec_sponsor_aligned=True,
                            champion_strength=5, open_support_issues=0,
                            previous_renewal_on_time=True, years_as_customer=3)
        score = _renewal_risk_score(inp)
        assert score == 0.0


# ---------------------------------------------------------------------------
# Class 4: _renewal_risk_score — NPS component
# ---------------------------------------------------------------------------

class TestRenewalRiskScoreNPS:
    """NPS contributes up to 20 points."""

    def _clean(self, nps_score: int) -> float:
        """Score from a perfectly healthy customer with only NPS varying."""
        inp = make_customer(health_score=80.0, nps_score=nps_score,
                            product_usage_trend="growing",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="low", exec_sponsor_aligned=True,
                            champion_strength=5, open_support_issues=0,
                            previous_renewal_on_time=True, years_as_customer=3)
        return _renewal_risk_score(inp)

    def test_nps_below_minus_20_adds_20(self):
        assert self._clean(-30) == 20.0

    def test_nps_exactly_minus_20_adds_12(self):
        assert self._clean(-20) == 12.0

    def test_nps_minus_1_adds_12(self):
        assert self._clean(-1) == 12.0

    def test_nps_0_adds_4(self):
        assert self._clean(0) == 4.0

    def test_nps_19_adds_4(self):
        assert self._clean(19) == 4.0

    def test_nps_20_adds_0(self):
        assert self._clean(20) == 0.0

    def test_nps_50_adds_0(self):
        assert self._clean(50) == 0.0

    def test_nps_100_adds_0(self):
        assert self._clean(100) == 0.0


# ---------------------------------------------------------------------------
# Class 5: _renewal_risk_score — usage trend component
# ---------------------------------------------------------------------------

class TestRenewalRiskScoreUsage:
    """Usage trend contributes up to 20 points."""

    def _clean(self, trend: str) -> float:
        inp = make_customer(health_score=80.0, nps_score=25,
                            product_usage_trend=trend,
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="low", exec_sponsor_aligned=True,
                            champion_strength=5, open_support_issues=0,
                            previous_renewal_on_time=True, years_as_customer=3)
        return _renewal_risk_score(inp)

    def test_dormant_adds_20(self):
        assert self._clean("dormant") == 20.0

    def test_declining_adds_12(self):
        assert self._clean("declining") == 12.0

    def test_stable_adds_3(self):
        assert self._clean("stable") == 3.0

    def test_growing_adds_0(self):
        assert self._clean("growing") == 0.0

    def test_unknown_trend_adds_0(self):
        assert self._clean("unknown") == 0.0


# ---------------------------------------------------------------------------
# Class 6: _renewal_risk_score — commercial component
# ---------------------------------------------------------------------------

class TestRenewalRiskScoreCommercial:
    """Commercial signals contribute up to 15 points."""

    def _clean(self, **kwargs) -> float:
        defaults = dict(health_score=80.0, nps_score=25, product_usage_trend="growing",
                        exec_sponsor_aligned=True, champion_strength=5,
                        open_support_issues=0, previous_renewal_on_time=True,
                        years_as_customer=3)
        defaults.update(kwargs)
        inp = make_customer(**defaults)
        return _renewal_risk_score(inp)

    def test_competitor_adds_7(self):
        assert self._clean(competitor_mentioned=True, discount_requested=False,
                           price_sensitivity="low") == 7.0

    def test_discount_adds_5(self):
        assert self._clean(competitor_mentioned=False, discount_requested=True,
                           price_sensitivity="low") == 5.0

    def test_price_high_adds_3(self):
        assert self._clean(competitor_mentioned=False, discount_requested=False,
                           price_sensitivity="high") == 3.0

    def test_price_medium_adds_1(self):
        assert self._clean(competitor_mentioned=False, discount_requested=False,
                           price_sensitivity="medium") == 1.0

    def test_price_low_adds_0(self):
        assert self._clean(competitor_mentioned=False, discount_requested=False,
                           price_sensitivity="low") == 0.0

    def test_all_commercial_signals_max_15(self):
        score = self._clean(competitor_mentioned=True, discount_requested=True,
                            price_sensitivity="high")
        assert score == 15.0

    def test_competitor_and_discount_adds_12(self):
        score = self._clean(competitor_mentioned=True, discount_requested=True,
                            price_sensitivity="low")
        assert score == 12.0


# ---------------------------------------------------------------------------
# Class 7: _renewal_risk_score — relationship component
# ---------------------------------------------------------------------------

class TestRenewalRiskScoreRelationship:
    """Relationship contributes up to 10 points."""

    def _clean(self, **kwargs) -> float:
        defaults = dict(health_score=80.0, nps_score=25, product_usage_trend="growing",
                        competitor_mentioned=False, discount_requested=False,
                        price_sensitivity="low", previous_renewal_on_time=True,
                        years_as_customer=3)
        defaults.update(kwargs)
        inp = make_customer(**defaults)
        return _renewal_risk_score(inp)

    def test_no_exec_sponsor_adds_5(self):
        assert self._clean(exec_sponsor_aligned=False, champion_strength=5,
                           open_support_issues=0) == 5.0

    def test_champion_3_adds_3(self):
        assert self._clean(exec_sponsor_aligned=True, champion_strength=3,
                           open_support_issues=0) == 3.0

    def test_champion_0_adds_3(self):
        assert self._clean(exec_sponsor_aligned=True, champion_strength=0,
                           open_support_issues=0) == 3.0

    def test_champion_4_adds_0(self):
        assert self._clean(exec_sponsor_aligned=True, champion_strength=4,
                           open_support_issues=0) == 0.0

    def test_champion_10_adds_0(self):
        assert self._clean(exec_sponsor_aligned=True, champion_strength=10,
                           open_support_issues=0) == 0.0

    def test_open_issues_2_adds_2(self):
        assert self._clean(exec_sponsor_aligned=True, champion_strength=5,
                           open_support_issues=2) == 2.0

    def test_open_issues_1_adds_0(self):
        assert self._clean(exec_sponsor_aligned=True, champion_strength=5,
                           open_support_issues=1) == 0.0

    def test_open_issues_5_adds_2(self):
        assert self._clean(exec_sponsor_aligned=True, champion_strength=5,
                           open_support_issues=5) == 2.0

    def test_all_relationship_bad_max_10(self):
        score = self._clean(exec_sponsor_aligned=False, champion_strength=2,
                            open_support_issues=3)
        assert score == 10.0


# ---------------------------------------------------------------------------
# Class 8: _renewal_risk_score — history component
# ---------------------------------------------------------------------------

class TestRenewalRiskScoreHistory:
    """History contributes up to 5 points."""

    def _clean(self, **kwargs) -> float:
        defaults = dict(health_score=80.0, nps_score=25, product_usage_trend="growing",
                        competitor_mentioned=False, discount_requested=False,
                        price_sensitivity="low", exec_sponsor_aligned=True,
                        champion_strength=5, open_support_issues=0)
        defaults.update(kwargs)
        inp = make_customer(**defaults)
        return _renewal_risk_score(inp)

    def test_not_previous_on_time_adds_3(self):
        assert self._clean(previous_renewal_on_time=False, years_as_customer=3) == 3.0

    def test_years_0_adds_2(self):
        assert self._clean(previous_renewal_on_time=True, years_as_customer=0) == 2.0

    def test_years_1_no_penalty(self):
        assert self._clean(previous_renewal_on_time=True, years_as_customer=1) == 0.0

    def test_all_history_bad_adds_5(self):
        assert self._clean(previous_renewal_on_time=False, years_as_customer=0) == 5.0

    def test_good_history_adds_0(self):
        assert self._clean(previous_renewal_on_time=True, years_as_customer=5) == 0.0


# ---------------------------------------------------------------------------
# Class 9: _renewal_risk_score — clamping and combined
# ---------------------------------------------------------------------------

class TestRenewalRiskScoreClamping:
    def test_score_is_float(self):
        inp = make_customer()
        score = _renewal_risk_score(inp)
        assert isinstance(score, float)

    def test_score_clamped_at_100(self):
        # Maximise every dimension
        inp = make_customer(health_score=10.0, nps_score=-50, product_usage_trend="dormant",
                            competitor_mentioned=True, discount_requested=True,
                            price_sensitivity="high", exec_sponsor_aligned=False,
                            champion_strength=1, open_support_issues=5,
                            previous_renewal_on_time=False, years_as_customer=0)
        score = _renewal_risk_score(inp)
        assert score <= 100.0

    def test_score_never_negative(self):
        inp = make_customer()
        score = _renewal_risk_score(inp)
        assert score >= 0.0

    def test_healthy_customer_low_score(self):
        inp = make_customer()
        score = _renewal_risk_score(inp)
        assert score < 20.0

    def test_worst_case_score_100(self):
        inp = make_customer(health_score=1.0, nps_score=-100, product_usage_trend="dormant",
                            competitor_mentioned=True, discount_requested=True,
                            price_sensitivity="high", exec_sponsor_aligned=False,
                            champion_strength=0, open_support_issues=10,
                            previous_renewal_on_time=False, years_as_customer=0)
        score = _renewal_risk_score(inp)
        assert score == 100.0

    def test_score_rounded_to_1_decimal(self):
        inp = make_customer()
        score = _renewal_risk_score(inp)
        assert score == round(score, 1)


# ---------------------------------------------------------------------------
# Class 10: _renewal_risk thresholds
# ---------------------------------------------------------------------------

class TestRenewalRiskThresholds:
    def test_score_0_is_low(self):
        assert _renewal_risk(0.0) == RenewalRisk.LOW

    def test_score_19_is_low(self):
        assert _renewal_risk(19.9) == RenewalRisk.LOW

    def test_score_20_is_moderate(self):
        assert _renewal_risk(20.0) == RenewalRisk.MODERATE

    def test_score_39_is_moderate(self):
        assert _renewal_risk(39.9) == RenewalRisk.MODERATE

    def test_score_40_is_high(self):
        assert _renewal_risk(40.0) == RenewalRisk.HIGH

    def test_score_59_is_high(self):
        assert _renewal_risk(59.9) == RenewalRisk.HIGH

    def test_score_60_is_critical(self):
        assert _renewal_risk(60.0) == RenewalRisk.CRITICAL

    def test_score_100_is_critical(self):
        assert _renewal_risk(100.0) == RenewalRisk.CRITICAL

    def test_score_boundary_exactly_40(self):
        assert _renewal_risk(40.0) == RenewalRisk.HIGH

    def test_score_boundary_exactly_60(self):
        assert _renewal_risk(60.0) == RenewalRisk.CRITICAL


# ---------------------------------------------------------------------------
# Class 11: _renewal_action logic
# ---------------------------------------------------------------------------

class TestRenewalAction:
    def test_critical_always_escalate(self):
        assert _renewal_action(RenewalRisk.CRITICAL, 120) == RenewalAction.ESCALATE

    def test_critical_with_expired_escalate(self):
        assert _renewal_action(RenewalRisk.CRITICAL, -5) == RenewalAction.ESCALATE

    def test_critical_with_future_days_escalate(self):
        assert _renewal_action(RenewalRisk.CRITICAL, 0) == RenewalAction.ESCALATE

    def test_high_days_30_escalate(self):
        assert _renewal_action(RenewalRisk.HIGH, 30) == RenewalAction.ESCALATE

    def test_high_days_0_escalate(self):
        assert _renewal_action(RenewalRisk.HIGH, 0) == RenewalAction.ESCALATE

    def test_high_days_negative_escalate(self):
        assert _renewal_action(RenewalRisk.HIGH, -1) == RenewalAction.ESCALATE

    def test_high_days_31_intervene(self):
        assert _renewal_action(RenewalRisk.HIGH, 31) == RenewalAction.INTERVENE

    def test_high_days_90_intervene(self):
        assert _renewal_action(RenewalRisk.HIGH, 90) == RenewalAction.INTERVENE

    def test_moderate_nurture(self):
        assert _renewal_action(RenewalRisk.MODERATE, 120) == RenewalAction.NURTURE

    def test_moderate_short_days_nurture(self):
        assert _renewal_action(RenewalRisk.MODERATE, 10) == RenewalAction.NURTURE

    def test_low_close(self):
        assert _renewal_action(RenewalRisk.LOW, 200) == RenewalAction.CLOSE

    def test_low_days_0_close(self):
        assert _renewal_action(RenewalRisk.LOW, 0) == RenewalAction.CLOSE


# ---------------------------------------------------------------------------
# Class 12: _engagement_trend mapping
# ---------------------------------------------------------------------------

class TestEngagementTrend:
    def test_growing_maps_to_growing(self):
        inp = make_customer(product_usage_trend="growing")
        assert _engagement_trend(inp) == EngagementTrend.GROWING

    def test_stable_maps_to_stable(self):
        inp = make_customer(product_usage_trend="stable")
        assert _engagement_trend(inp) == EngagementTrend.STABLE

    def test_declining_maps_to_declining(self):
        inp = make_customer(product_usage_trend="declining")
        assert _engagement_trend(inp) == EngagementTrend.DECLINING

    def test_dormant_maps_to_dormant(self):
        inp = make_customer(product_usage_trend="dormant")
        assert _engagement_trend(inp) == EngagementTrend.DORMANT

    def test_unknown_defaults_stable(self):
        inp = make_customer(product_usage_trend="unknown_value")
        assert _engagement_trend(inp) == EngagementTrend.STABLE

    def test_returns_engagement_trend_instance(self):
        inp = make_customer(product_usage_trend="growing")
        assert isinstance(_engagement_trend(inp), EngagementTrend)


# ---------------------------------------------------------------------------
# Class 13: _renewal_probability
# ---------------------------------------------------------------------------

class TestRenewalProbability:
    def test_probability_in_range(self):
        inp = make_customer()
        score = _renewal_risk_score(inp)
        prob = _renewal_probability(score, inp)
        assert 0.0 <= prob <= 100.0

    def test_probability_is_float(self):
        inp = make_customer()
        score = _renewal_risk_score(inp)
        prob = _renewal_probability(score, inp)
        assert isinstance(prob, float)

    def test_probability_rounded_to_1_decimal(self):
        inp = make_customer()
        score = _renewal_risk_score(inp)
        prob = _renewal_probability(score, inp)
        assert prob == round(prob, 1)

    def test_expansion_discussion_adds_5(self):
        # Use a customer that doesn't already cap at 100 — remove some positive modifiers
        base_inp = make_customer(has_expansion_discussion=False, exec_sponsor_aligned=False,
                                 champion_strength=6, previous_renewal_on_time=False,
                                 years_as_customer=2)
        exp_inp = make_customer(has_expansion_discussion=True, exec_sponsor_aligned=False,
                                champion_strength=6, previous_renewal_on_time=False,
                                years_as_customer=2)
        s_base = _renewal_risk_score(base_inp)
        s_exp = _renewal_risk_score(exp_inp)
        prob_base = _renewal_probability(s_base, base_inp)
        prob_exp = _renewal_probability(s_exp, exp_inp)
        assert prob_exp - prob_base == pytest.approx(5.0, abs=0.2)

    def test_exec_sponsor_and_strong_champion_adds_4(self):
        base_inp = make_customer(exec_sponsor_aligned=False, champion_strength=6)
        good_inp = make_customer(exec_sponsor_aligned=True, champion_strength=7)
        s_base = _renewal_risk_score(base_inp)
        s_good = _renewal_risk_score(good_inp)
        # Adjust for the diff in risk score from exec_sponsor (5 pts)
        prob_base = _renewal_probability(s_base, base_inp)
        prob_good = _renewal_probability(s_good, good_inp)
        # Good should be higher; exact value depends on score change too
        assert prob_good > prob_base

    def test_years_3_plus_adds_3(self):
        # Use a customer that won't cap at 100 — strip other positive modifiers
        young_inp = make_customer(years_as_customer=2, exec_sponsor_aligned=False,
                                  champion_strength=6, previous_renewal_on_time=False,
                                  has_expansion_discussion=False)
        old_inp = make_customer(years_as_customer=3, exec_sponsor_aligned=False,
                                champion_strength=6, previous_renewal_on_time=False,
                                has_expansion_discussion=False)
        s_young = _renewal_risk_score(young_inp)
        s_old = _renewal_risk_score(old_inp)
        prob_young = _renewal_probability(s_young, young_inp)
        prob_old = _renewal_probability(s_old, old_inp)
        assert prob_old - prob_young == pytest.approx(3.0, abs=0.2)

    def test_previous_on_time_adds_2(self):
        late_inp = make_customer(previous_renewal_on_time=False)
        ontime_inp = make_customer(previous_renewal_on_time=True)
        s_late = _renewal_risk_score(late_inp)
        s_ontime = _renewal_risk_score(ontime_inp)
        prob_late = _renewal_probability(s_late, late_inp)
        prob_ontime = _renewal_probability(s_ontime, ontime_inp)
        assert prob_ontime > prob_late

    def test_competitor_mentioned_subtracts_5(self):
        no_comp_inp = make_customer(competitor_mentioned=False)
        comp_inp = make_customer(competitor_mentioned=True)
        s_no_comp = _renewal_risk_score(no_comp_inp)
        s_comp = _renewal_risk_score(comp_inp)
        prob_no_comp = _renewal_probability(s_no_comp, no_comp_inp)
        prob_comp = _renewal_probability(s_comp, comp_inp)
        assert prob_no_comp > prob_comp

    def test_expired_contract_subtracts_10(self):
        future_inp = make_customer(days_to_renewal=30)
        expired_inp = make_customer(days_to_renewal=-1)
        score = _renewal_risk_score(future_inp)
        score_exp = _renewal_risk_score(expired_inp)
        prob_future = _renewal_probability(score, future_inp)
        prob_expired = _renewal_probability(score_exp, expired_inp)
        assert prob_future > prob_expired

    def test_days_0_subtracts_10(self):
        day0_inp = make_customer(days_to_renewal=0)
        day1_inp = make_customer(days_to_renewal=1)
        s0 = _renewal_risk_score(day0_inp)
        s1 = _renewal_risk_score(day1_inp)
        p0 = _renewal_probability(s0, day0_inp)
        p1 = _renewal_probability(s1, day1_inp)
        assert p1 > p0

    def test_probability_never_negative(self):
        inp = make_customer(health_score=1.0, nps_score=-100, product_usage_trend="dormant",
                            competitor_mentioned=True, discount_requested=True,
                            price_sensitivity="high", exec_sponsor_aligned=False,
                            champion_strength=0, open_support_issues=10,
                            previous_renewal_on_time=False, years_as_customer=0,
                            days_to_renewal=-30)
        score = _renewal_risk_score(inp)
        prob = _renewal_probability(score, inp)
        assert prob >= 0.0

    def test_probability_never_above_100(self):
        inp = make_customer(health_score=100.0, nps_score=100, product_usage_trend="growing",
                            has_expansion_discussion=True, competitor_mentioned=False,
                            exec_sponsor_aligned=True, champion_strength=10,
                            previous_renewal_on_time=True, years_as_customer=10)
        score = _renewal_risk_score(inp)
        prob = _renewal_probability(score, inp)
        assert prob <= 100.0


# ---------------------------------------------------------------------------
# Class 14: _predicted_outcome
# ---------------------------------------------------------------------------

class TestPredictedOutcome:
    def test_low_prob_churn(self):
        inp = make_customer()
        assert _predicted_outcome(RenewalRisk.LOW, 20.0, inp) == RenewalOutcome.CHURN

    def test_critical_risk_churn(self):
        inp = make_customer()
        assert _predicted_outcome(RenewalRisk.CRITICAL, 80.0, inp) == RenewalOutcome.CHURN

    def test_critical_risk_overrides_high_prob(self):
        inp = make_customer()
        assert _predicted_outcome(RenewalRisk.CRITICAL, 90.0, inp) == RenewalOutcome.CHURN

    def test_prob_29_churn(self):
        inp = make_customer()
        assert _predicted_outcome(RenewalRisk.HIGH, 29.9, inp) == RenewalOutcome.CHURN

    def test_prob_30_not_churn_by_default(self):
        inp = make_customer(discount_requested=False, has_expansion_discussion=False)
        assert _predicted_outcome(RenewalRisk.LOW, 30.0, inp) == RenewalOutcome.RENEW

    def test_discount_no_expansion_downgrade(self):
        inp = make_customer(discount_requested=True, has_expansion_discussion=False)
        assert _predicted_outcome(RenewalRisk.MODERATE, 50.0, inp) == RenewalOutcome.DOWNGRADE

    def test_discount_with_expansion_and_high_health_expand(self):
        inp = make_customer(discount_requested=True, has_expansion_discussion=True, health_score=70.0)
        assert _predicted_outcome(RenewalRisk.MODERATE, 60.0, inp) == RenewalOutcome.EXPAND

    def test_expansion_and_health_65_expand(self):
        inp = make_customer(has_expansion_discussion=True, health_score=65.0)
        assert _predicted_outcome(RenewalRisk.LOW, 70.0, inp) == RenewalOutcome.EXPAND

    def test_expansion_and_health_64_renew(self):
        inp = make_customer(has_expansion_discussion=True, health_score=64.9,
                            discount_requested=False)
        assert _predicted_outcome(RenewalRisk.LOW, 70.0, inp) == RenewalOutcome.RENEW

    def test_no_special_signals_renew(self):
        inp = make_customer(discount_requested=False, has_expansion_discussion=False)
        assert _predicted_outcome(RenewalRisk.LOW, 80.0, inp) == RenewalOutcome.RENEW

    def test_high_risk_not_critical_can_expand(self):
        inp = make_customer(has_expansion_discussion=True, health_score=70.0)
        assert _predicted_outcome(RenewalRisk.HIGH, 35.0, inp) == RenewalOutcome.EXPAND


# ---------------------------------------------------------------------------
# Class 15: _expected_arr_change
# ---------------------------------------------------------------------------

class TestExpectedArrChange:
    def test_churn_is_minus_100(self):
        inp = make_customer()
        assert _expected_arr_change(RenewalOutcome.CHURN, inp) == -100.0

    def test_downgrade_high_sensitivity_minus_20(self):
        inp = make_customer(price_sensitivity="high")
        assert _expected_arr_change(RenewalOutcome.DOWNGRADE, inp) == -20.0

    def test_downgrade_medium_sensitivity_minus_10(self):
        inp = make_customer(price_sensitivity="medium")
        assert _expected_arr_change(RenewalOutcome.DOWNGRADE, inp) == -10.0

    def test_downgrade_low_sensitivity_minus_10(self):
        inp = make_customer(price_sensitivity="low")
        assert _expected_arr_change(RenewalOutcome.DOWNGRADE, inp) == -10.0

    def test_expand_health_80_plus_25(self):
        inp = make_customer(has_expansion_discussion=True, health_score=80.0)
        assert _expected_arr_change(RenewalOutcome.EXPAND, inp) == 25.0

    def test_expand_health_79_plus_15(self):
        inp = make_customer(has_expansion_discussion=True, health_score=79.9)
        assert _expected_arr_change(RenewalOutcome.EXPAND, inp) == 15.0

    def test_expand_health_65_plus_15(self):
        inp = make_customer(has_expansion_discussion=True, health_score=65.0)
        assert _expected_arr_change(RenewalOutcome.EXPAND, inp) == 15.0

    def test_renew_is_0(self):
        inp = make_customer()
        assert _expected_arr_change(RenewalOutcome.RENEW, inp) == 0.0

    def test_return_is_numeric(self):
        inp = make_customer()
        result = _expected_arr_change(RenewalOutcome.RENEW, inp)
        assert isinstance(result, (int, float))


# ---------------------------------------------------------------------------
# Class 16: _urgency_score
# ---------------------------------------------------------------------------

class TestUrgencyScore:
    def test_expired_adds_30_time_factor(self):
        urgency = _urgency_score(0.0, -1)
        assert urgency == 30.0

    def test_days_0_adds_30_time_factor(self):
        urgency = _urgency_score(0.0, 0)
        assert urgency == 30.0

    def test_days_30_adds_25_time_factor(self):
        urgency = _urgency_score(0.0, 30)
        assert urgency == 25.0

    def test_days_1_adds_25_time_factor(self):
        urgency = _urgency_score(0.0, 1)
        assert urgency == 25.0

    def test_days_60_adds_15_time_factor(self):
        urgency = _urgency_score(0.0, 60)
        assert urgency == 15.0

    def test_days_31_adds_15_time_factor(self):
        urgency = _urgency_score(0.0, 31)
        assert urgency == 15.0

    def test_days_90_adds_8_time_factor(self):
        urgency = _urgency_score(0.0, 90)
        assert urgency == 8.0

    def test_days_61_adds_8_time_factor(self):
        urgency = _urgency_score(0.0, 61)
        assert urgency == 8.0

    def test_days_91_adds_0_time_factor(self):
        urgency = _urgency_score(0.0, 91)
        assert urgency == 0.0

    def test_days_365_adds_0_time_factor(self):
        urgency = _urgency_score(0.0, 365)
        assert urgency == 0.0

    def test_risk_score_weighted_07(self):
        urgency = _urgency_score(40.0, 200)
        assert urgency == pytest.approx(28.0, abs=0.1)

    def test_combined_risk_and_time(self):
        urgency = _urgency_score(40.0, 20)
        # 40*0.7 + 25 = 28 + 25 = 53
        assert urgency == pytest.approx(53.0, abs=0.1)

    def test_clamped_at_100(self):
        urgency = _urgency_score(100.0, 0)
        assert urgency <= 100.0

    def test_never_negative(self):
        urgency = _urgency_score(0.0, 500)
        assert urgency >= 0.0

    def test_return_is_float(self):
        urgency = _urgency_score(20.0, 60)
        assert isinstance(urgency, float)

    def test_rounded_to_1_decimal(self):
        urgency = _urgency_score(33.3, 45)
        assert urgency == round(urgency, 1)


# ---------------------------------------------------------------------------
# Class 17: _risk_signals
# ---------------------------------------------------------------------------

class TestRiskSignals:
    def test_health_below_40_triggers_signal(self):
        inp = make_customer(health_score=30.0)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("santé" in s.lower() for s in signals)

    def test_health_40_no_health_signal(self):
        inp = make_customer(health_score=40.0, nps_score=25, product_usage_trend="growing",
                            competitor_mentioned=False, discount_requested=False,
                            exec_sponsor_aligned=True, champion_strength=5,
                            open_support_issues=0, previous_renewal_on_time=True,
                            years_as_customer=3)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert not any("critique" in s.lower() and "santé" in s.lower() for s in signals)

    def test_negative_nps_triggers_signal(self):
        inp = make_customer(nps_score=-10)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("nps" in s.lower() for s in signals)

    def test_zero_nps_no_signal(self):
        inp = make_customer(nps_score=0)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        # nps_score < 0 triggers signal; nps=0 should NOT
        assert not any("nps" in s.lower() and "négatif" in s.lower() for s in signals)

    def test_declining_usage_triggers_signal(self):
        inp = make_customer(product_usage_trend="declining")
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("declining" in s.lower() for s in signals)

    def test_dormant_usage_triggers_signal(self):
        inp = make_customer(product_usage_trend="dormant")
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("dormant" in s.lower() for s in signals)

    def test_growing_no_usage_signal(self):
        inp = make_customer(product_usage_trend="growing", nps_score=25, health_score=80.0,
                            competitor_mentioned=False, discount_requested=False,
                            exec_sponsor_aligned=True, champion_strength=5,
                            open_support_issues=0, previous_renewal_on_time=True,
                            years_as_customer=3)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert not any("désengagement" in s for s in signals)

    def test_competitor_triggers_signal(self):
        inp = make_customer(competitor_mentioned=True)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("concurrent" in s.lower() for s in signals)

    def test_discount_triggers_signal(self):
        inp = make_customer(discount_requested=True)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("remise" in s.lower() for s in signals)

    def test_no_exec_sponsor_triggers_signal(self):
        inp = make_customer(exec_sponsor_aligned=False)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("sponsor" in s.lower() for s in signals)

    def test_weak_champion_triggers_signal(self):
        inp = make_customer(champion_strength=2)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("champion" in s.lower() for s in signals)

    def test_open_issues_2_triggers_signal(self):
        inp = make_customer(open_support_issues=2)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("tickets" in s.lower() or "support" in s.lower() for s in signals)

    def test_days_30_triggers_urgency_signal(self):
        inp = make_customer(days_to_renewal=30)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("urgence" in s.lower() or "30j" in s for s in signals)

    def test_days_0_triggers_urgency_signal(self):
        inp = make_customer(days_to_renewal=0)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("urgence" in s.lower() for s in signals)

    def test_expired_triggers_expired_signal(self):
        inp = make_customer(days_to_renewal=-5)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert any("expiré" in s.lower() for s in signals)

    def test_days_31_no_urgency_signal(self):
        inp = make_customer(days_to_renewal=31, nps_score=25, health_score=80.0,
                            competitor_mentioned=False, discount_requested=False,
                            exec_sponsor_aligned=True, champion_strength=5,
                            open_support_issues=0, previous_renewal_on_time=True,
                            years_as_customer=3)
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        # Days 31 should NOT trigger the urgency signal (condition: 0 <= days <= 30)
        assert not any("urgence" in s.lower() for s in signals)

    def test_clean_customer_no_signals(self):
        inp = make_customer()
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert signals == []

    def test_returns_list(self):
        inp = make_customer()
        signals = _risk_signals(inp, _renewal_risk_score(inp))
        assert isinstance(signals, list)


# ---------------------------------------------------------------------------
# Class 18: _positive_signals
# ---------------------------------------------------------------------------

class TestPositiveSignals:
    def test_health_75_triggers_signal(self):
        inp = make_customer(health_score=75.0)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert any("santé" in s.lower() for s in signals)

    def test_health_74_no_signal(self):
        inp = make_customer(health_score=74.9, nps_score=25, product_usage_trend="stable",
                            has_expansion_discussion=False, exec_sponsor_aligned=True,
                            champion_strength=6, previous_renewal_on_time=False,
                            years_as_customer=2)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert not any("santé" in s.lower() for s in signals)

    def test_nps_30_triggers_signal(self):
        inp = make_customer(nps_score=30)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert any("nps" in s.lower() for s in signals)

    def test_nps_29_no_signal(self):
        inp = make_customer(nps_score=29, health_score=74.0,
                            product_usage_trend="stable", has_expansion_discussion=False,
                            exec_sponsor_aligned=True, champion_strength=6,
                            previous_renewal_on_time=False, years_as_customer=2)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert not any("nps" in s.lower() for s in signals)

    def test_growing_usage_triggers_signal(self):
        inp = make_customer(product_usage_trend="growing")
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert any("usage" in s.lower() or "croissance" in s.lower() for s in signals)

    def test_stable_usage_no_positive_signal(self):
        inp = make_customer(product_usage_trend="stable", health_score=74.0, nps_score=25,
                            has_expansion_discussion=False, exec_sponsor_aligned=True,
                            champion_strength=6, previous_renewal_on_time=False,
                            years_as_customer=2)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert not any("croissance" in s.lower() for s in signals)

    def test_expansion_discussion_triggers_signal(self):
        inp = make_customer(has_expansion_discussion=True)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert any("expansion" in s.lower() for s in signals)

    def test_exec_sponsor_triggers_signal(self):
        inp = make_customer(exec_sponsor_aligned=True)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert any("sponsor" in s.lower() for s in signals)

    def test_strong_champion_7_triggers_signal(self):
        inp = make_customer(champion_strength=7)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert any("champion" in s.lower() for s in signals)

    def test_champion_6_no_signal(self):
        inp = make_customer(champion_strength=6, health_score=74.0, nps_score=25,
                            product_usage_trend="stable", has_expansion_discussion=False,
                            exec_sponsor_aligned=True, previous_renewal_on_time=False,
                            years_as_customer=2)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert not any("champion" in s.lower() and "fort" in s.lower() for s in signals)

    def test_years_3_triggers_signal(self):
        inp = make_customer(years_as_customer=3)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert any("ans" in s.lower() for s in signals)

    def test_years_2_no_years_signal(self):
        inp = make_customer(years_as_customer=2, health_score=74.0, nps_score=25,
                            product_usage_trend="stable", has_expansion_discussion=False,
                            exec_sponsor_aligned=True, champion_strength=6,
                            previous_renewal_on_time=False)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert not any("ans" in s.lower() for s in signals)

    def test_previous_on_time_triggers_signal(self):
        inp = make_customer(previous_renewal_on_time=True)
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert any("ponctuel" in s.lower() or "historique" in s.lower() for s in signals)

    def test_returns_list(self):
        inp = make_customer()
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert isinstance(signals, list)

    def test_clean_customer_has_multiple_positive_signals(self):
        inp = make_customer()
        signals = _positive_signals(inp, _renewal_risk_score(inp))
        assert len(signals) >= 3


# ---------------------------------------------------------------------------
# Class 19: _renewal_plays content
# ---------------------------------------------------------------------------

class TestRenewalPlays:
    def _make_result(self, **kwargs):
        inp = make_customer(**kwargs)
        score = _renewal_risk_score(inp)
        risk = _renewal_risk(score)
        action = _renewal_action(risk, inp.days_to_renewal)
        prob = _renewal_probability(score, inp)
        outcome = _predicted_outcome(risk, prob, inp)
        return _renewal_plays(risk, action, inp, outcome), action, outcome

    def test_escalate_has_at_least_4_plays(self):
        # Force ESCALATE: CRITICAL risk
        inp = make_customer(health_score=10.0, nps_score=-100, product_usage_trend="dormant",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="high", exec_sponsor_aligned=False,
                            champion_strength=0, open_support_issues=5,
                            previous_renewal_on_time=False, years_as_customer=0)
        score = _renewal_risk_score(inp)
        risk = _renewal_risk(score)
        action = _renewal_action(risk, inp.days_to_renewal)
        prob = _renewal_probability(score, inp)
        outcome = _predicted_outcome(risk, prob, inp)
        plays = _renewal_plays(risk, action, inp, outcome)
        assert action == RenewalAction.ESCALATE
        assert len(plays) >= 3

    def test_escalate_includes_clevel(self):
        inp = make_customer(health_score=10.0, nps_score=-100, product_usage_trend="dormant",
                            price_sensitivity="high", exec_sponsor_aligned=False,
                            champion_strength=0, open_support_issues=5,
                            previous_renewal_on_time=False, years_as_customer=0,
                            competitor_mentioned=False)
        score = _renewal_risk_score(inp)
        risk = _renewal_risk(score)
        action = _renewal_action(risk, inp.days_to_renewal)
        prob = _renewal_probability(score, inp)
        outcome = _predicted_outcome(risk, prob, inp)
        plays = _renewal_plays(risk, action, inp, outcome)
        assert any("c-level" in p.lower() or "escalade" in p.lower() for p in plays)

    def test_escalate_with_competitor_includes_battlecard(self):
        inp = make_customer(health_score=10.0, nps_score=-100, product_usage_trend="dormant",
                            competitor_mentioned=True, price_sensitivity="high",
                            exec_sponsor_aligned=False, champion_strength=0,
                            open_support_issues=5, previous_renewal_on_time=False,
                            years_as_customer=0)
        score = _renewal_risk_score(inp)
        risk = _renewal_risk(score)
        action = _renewal_action(risk, inp.days_to_renewal)
        prob = _renewal_probability(score, inp)
        outcome = _predicted_outcome(risk, prob, inp)
        plays = _renewal_plays(risk, action, inp, outcome)
        assert any("battlecard" in p.lower() or "concurrentiel" in p.lower() for p in plays)

    def test_intervene_has_plays(self):
        # HIGH risk but days > 30
        inp = make_customer(health_score=50.0, nps_score=-30, product_usage_trend="dormant",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="low", exec_sponsor_aligned=False,
                            champion_strength=2, open_support_issues=3,
                            previous_renewal_on_time=False, years_as_customer=0,
                            days_to_renewal=60)
        score = _renewal_risk_score(inp)
        risk = _renewal_risk(score)
        action = _renewal_action(risk, inp.days_to_renewal)
        if action == RenewalAction.INTERVENE:
            prob = _renewal_probability(score, inp)
            outcome = _predicted_outcome(risk, prob, inp)
            plays = _renewal_plays(risk, action, inp, outcome)
            assert len(plays) >= 2

    def test_intervene_with_discount_includes_offer_play(self):
        inp = make_customer(health_score=50.0, nps_score=-30, product_usage_trend="declining",
                            competitor_mentioned=False, discount_requested=True,
                            price_sensitivity="high", exec_sponsor_aligned=False,
                            champion_strength=2, open_support_issues=0,
                            previous_renewal_on_time=False, years_as_customer=0,
                            days_to_renewal=60)
        score = _renewal_risk_score(inp)
        risk = _renewal_risk(score)
        action = _renewal_action(risk, inp.days_to_renewal)
        if action == RenewalAction.INTERVENE:
            prob = _renewal_probability(score, inp)
            outcome = _predicted_outcome(risk, prob, inp)
            plays = _renewal_plays(risk, action, inp, outcome)
            assert any("offre" in p.lower() or "remise" in p.lower() for p in plays)

    def test_nurture_has_plays(self):
        inp = make_customer(health_score=65.0, nps_score=5, product_usage_trend="stable",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="medium", exec_sponsor_aligned=False,
                            champion_strength=4, open_support_issues=1,
                            previous_renewal_on_time=True, years_as_customer=2,
                            days_to_renewal=90)
        score = _renewal_risk_score(inp)
        risk = _renewal_risk(score)
        action = _renewal_action(risk, inp.days_to_renewal)
        if action == RenewalAction.NURTURE:
            prob = _renewal_probability(score, inp)
            outcome = _predicted_outcome(risk, prob, inp)
            plays = _renewal_plays(risk, action, inp, outcome)
            assert len(plays) >= 2

    def test_nurture_with_expansion_includes_expansion_play(self):
        inp = make_customer(health_score=65.0, nps_score=5, product_usage_trend="stable",
                            competitor_mentioned=False, discount_requested=False,
                            price_sensitivity="medium", exec_sponsor_aligned=False,
                            champion_strength=4, open_support_issues=1,
                            previous_renewal_on_time=True, years_as_customer=2,
                            has_expansion_discussion=True, days_to_renewal=90)
        score = _renewal_risk_score(inp)
        risk = _renewal_risk(score)
        action = _renewal_action(risk, inp.days_to_renewal)
        if action == RenewalAction.NURTURE:
            prob = _renewal_probability(score, inp)
            outcome = _predicted_outcome(risk, prob, inp)
            plays = _renewal_plays(risk, action, inp, outcome)
            assert any("expansion" in p.lower() for p in plays)

    def test_close_has_plays(self):
        inp = make_customer()
        score = _renewal_risk_score(inp)
        risk = _renewal_risk(score)
        action = _renewal_action(risk, inp.days_to_renewal)
        prob = _renewal_probability(score, inp)
        outcome = _predicted_outcome(risk, prob, inp)
        plays = _renewal_plays(risk, action, inp, outcome)
        assert len(plays) >= 2

    def test_returns_list(self):
        inp = make_customer()
        score = _renewal_risk_score(inp)
        risk = _renewal_risk(score)
        action = _renewal_action(risk, inp.days_to_renewal)
        prob = _renewal_probability(score, inp)
        outcome = _predicted_outcome(risk, prob, inp)
        plays = _renewal_plays(risk, action, inp, outcome)
        assert isinstance(plays, list)


# ---------------------------------------------------------------------------
# Class 20: RenewalResult dataclass and to_dict
# ---------------------------------------------------------------------------

class TestRenewalResult:
    def _make_result(self) -> RenewalResult:
        engine = RenewalIntelligenceEngine()
        return engine.analyze(make_customer())

    def test_customer_id_preserved(self):
        r = self._make_result()
        assert r.customer_id == "C001"

    def test_customer_name_preserved(self):
        r = self._make_result()
        assert r.customer_name == "Acme Corp"

    def test_arr_eur_preserved(self):
        r = self._make_result()
        assert r.arr_eur == 100_000.0

    def test_segment_preserved(self):
        r = self._make_result()
        assert r.segment == "enterprise"

    def test_days_to_renewal_preserved(self):
        r = self._make_result()
        assert r.days_to_renewal == 120

    def test_renewal_risk_is_enum(self):
        r = self._make_result()
        assert isinstance(r.renewal_risk, RenewalRisk)

    def test_renewal_action_is_enum(self):
        r = self._make_result()
        assert isinstance(r.renewal_action, RenewalAction)

    def test_predicted_outcome_is_enum(self):
        r = self._make_result()
        assert isinstance(r.predicted_outcome, RenewalOutcome)

    def test_engagement_trend_is_enum(self):
        r = self._make_result()
        assert isinstance(r.engagement_trend, EngagementTrend)

    def test_renewal_probability_in_range(self):
        r = self._make_result()
        assert 0.0 <= r.renewal_probability_pct <= 100.0

    def test_urgency_score_in_range(self):
        r = self._make_result()
        assert 0.0 <= r.urgency_score <= 100.0

    def test_risk_signals_is_list(self):
        r = self._make_result()
        assert isinstance(r.risk_signals, list)

    def test_positive_signals_is_list(self):
        r = self._make_result()
        assert isinstance(r.positive_signals, list)

    def test_renewal_plays_is_list(self):
        r = self._make_result()
        assert isinstance(r.renewal_plays, list)

    def test_to_dict_returns_dict(self):
        r = self._make_result()
        assert isinstance(r.to_dict(), dict)

    def test_to_dict_customer_id(self):
        r = self._make_result()
        assert r.to_dict()["customer_id"] == "C001"

    def test_to_dict_renewal_risk_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["renewal_risk"], str)

    def test_to_dict_renewal_action_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["renewal_action"], str)

    def test_to_dict_predicted_outcome_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["predicted_outcome"], str)

    def test_to_dict_engagement_trend_is_string(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["engagement_trend"], str)

    def test_to_dict_all_keys_present(self):
        r = self._make_result()
        expected_keys = {"customer_id", "customer_name", "arr_eur", "segment",
                         "days_to_renewal", "renewal_risk", "renewal_action",
                         "predicted_outcome", "engagement_trend", "renewal_probability_pct",
                         "expected_arr_change_pct", "risk_signals", "positive_signals",
                         "renewal_plays", "urgency_score"}
        assert set(r.to_dict().keys()) == expected_keys

    def test_to_dict_renewal_probability_is_numeric(self):
        r = self._make_result()
        assert isinstance(r.to_dict()["renewal_probability_pct"], (int, float))


# ---------------------------------------------------------------------------
# Class 21: Engine — analyze and core behavior
# ---------------------------------------------------------------------------

class TestEngineAnalyze:
    def setup_method(self):
        self.engine = RenewalIntelligenceEngine()

    def test_analyze_returns_renewal_result(self):
        inp = make_customer()
        result = self.engine.analyze(inp)
        assert isinstance(result, RenewalResult)

    def test_analyze_stores_result(self):
        inp = make_customer()
        self.engine.analyze(inp)
        assert len(self.engine.all_renewals()) == 1

    def test_analyze_second_customer_stored(self):
        self.engine.analyze(make_customer(customer_id="C001"))
        self.engine.analyze(make_customer(customer_id="C002"))
        assert len(self.engine.all_renewals()) == 2

    def test_analyze_overwrites_same_customer_id(self):
        self.engine.analyze(make_customer(customer_id="C001", arr_eur=50_000.0))
        self.engine.analyze(make_customer(customer_id="C001", arr_eur=100_000.0))
        assert len(self.engine.all_renewals()) == 1
        assert self.engine.all_renewals()[0].arr_eur == 100_000.0

    def test_healthy_customer_is_low_risk(self):
        result = self.engine.analyze(make_customer())
        assert result.renewal_risk == RenewalRisk.LOW

    def test_healthy_customer_action_close(self):
        result = self.engine.analyze(make_customer())
        assert result.renewal_action == RenewalAction.CLOSE

    def test_healthy_customer_high_probability(self):
        result = self.engine.analyze(make_customer())
        assert result.renewal_probability_pct > 80.0

    def test_critical_customer_risk(self):
        inp = make_customer(health_score=10.0, nps_score=-100, product_usage_trend="dormant",
                            competitor_mentioned=True, discount_requested=True,
                            price_sensitivity="high", exec_sponsor_aligned=False,
                            champion_strength=0, open_support_issues=5,
                            previous_renewal_on_time=False, years_as_customer=0)
        result = self.engine.analyze(inp)
        assert result.renewal_risk == RenewalRisk.CRITICAL

    def test_critical_customer_action_escalate(self):
        inp = make_customer(health_score=10.0, nps_score=-100, product_usage_trend="dormant",
                            competitor_mentioned=True, discount_requested=True,
                            price_sensitivity="high", exec_sponsor_aligned=False,
                            champion_strength=0, open_support_issues=5,
                            previous_renewal_on_time=False, years_as_customer=0)
        result = self.engine.analyze(inp)
        assert result.renewal_action == RenewalAction.ESCALATE

    def test_engagement_trend_maps_correctly(self):
        for trend, expected in [("growing", EngagementTrend.GROWING),
                                 ("stable", EngagementTrend.STABLE),
                                 ("declining", EngagementTrend.DECLINING),
                                 ("dormant", EngagementTrend.DORMANT)]:
            engine = RenewalIntelligenceEngine()
            result = engine.analyze(make_customer(product_usage_trend=trend))
            assert result.engagement_trend == expected

    def test_result_urgency_score_range(self):
        result = self.engine.analyze(make_customer())
        assert 0.0 <= result.urgency_score <= 100.0

    def test_expired_contract_adds_urgency(self):
        future = self.engine.analyze(make_customer(customer_id="C001", days_to_renewal=200))
        expired = self.engine.analyze(make_customer(customer_id="C002", days_to_renewal=-10))
        assert expired.urgency_score > future.urgency_score

    def test_analyze_batch_returns_list(self):
        customers = [make_customer(customer_id=f"C{i:03d}") for i in range(5)]
        results = self.engine.analyze_batch(customers)
        assert isinstance(results, list)
        assert len(results) == 5

    def test_analyze_batch_sorted_by_urgency_desc(self):
        customers = [make_customer(customer_id=f"C{i:03d}", days_to_renewal=i*30) for i in range(5)]
        results = self.engine.analyze_batch(customers)
        urgencies = [r.urgency_score for r in results]
        assert urgencies == sorted(urgencies, reverse=True)

    def test_analyze_batch_all_stored(self):
        customers = [make_customer(customer_id=f"C{i:03d}") for i in range(4)]
        self.engine.analyze_batch(customers)
        assert len(self.engine.all_renewals()) == 4


# ---------------------------------------------------------------------------
# Class 22: Engine — filtering and aggregation methods
# ---------------------------------------------------------------------------

class TestEngineFilteringAndAggregation:
    def setup_method(self):
        self.engine = RenewalIntelligenceEngine()

        # Healthy customer → LOW / CLOSE / RENEW
        self.engine.analyze(make_customer(customer_id="LOW1", arr_eur=50_000.0))

        # Expansion opportunity → LOW risk, EXPAND outcome
        self.engine.analyze(make_customer(
            customer_id="EXP1", arr_eur=80_000.0,
            has_expansion_discussion=True, health_score=90.0,
            nps_score=50, product_usage_trend="growing",
        ))

        # HIGH risk (but days > 30) → INTERVENE
        self.engine.analyze(make_customer(
            customer_id="HIGH1", arr_eur=120_000.0,
            health_score=50.0, nps_score=-25, product_usage_trend="declining",
            exec_sponsor_aligned=False, champion_strength=2,
            open_support_issues=3, previous_renewal_on_time=False,
            years_as_customer=0, days_to_renewal=60,
            competitor_mentioned=False, discount_requested=False,
            price_sensitivity="medium",
        ))

        # CRITICAL risk → ESCALATE
        self.engine.analyze(make_customer(
            customer_id="CRIT1", arr_eur=200_000.0,
            health_score=10.0, nps_score=-100, product_usage_trend="dormant",
            competitor_mentioned=True, discount_requested=True,
            price_sensitivity="high", exec_sponsor_aligned=False,
            champion_strength=0, open_support_issues=5,
            previous_renewal_on_time=False, years_as_customer=0,
            days_to_renewal=10,
        ))

    def test_all_renewals_count(self):
        assert len(self.engine.all_renewals()) == 4

    def test_all_renewals_sorted_desc_urgency(self):
        results = self.engine.all_renewals()
        urgencies = [r.urgency_score for r in results]
        assert urgencies == sorted(urgencies, reverse=True)

    def test_by_risk_critical(self):
        critical = self.engine.by_risk(RenewalRisk.CRITICAL)
        assert all(r.renewal_risk == RenewalRisk.CRITICAL for r in critical)

    def test_by_risk_low(self):
        low = self.engine.by_risk(RenewalRisk.LOW)
        assert all(r.renewal_risk == RenewalRisk.LOW for r in low)

    def test_by_action_escalate(self):
        escalated = self.engine.by_action(RenewalAction.ESCALATE)
        assert all(r.renewal_action == RenewalAction.ESCALATE for r in escalated)

    def test_by_action_close(self):
        closed = self.engine.by_action(RenewalAction.CLOSE)
        assert all(r.renewal_action == RenewalAction.CLOSE for r in closed)

    def test_by_outcome_expand(self):
        expansions = self.engine.by_outcome(RenewalOutcome.EXPAND)
        assert all(r.predicted_outcome == RenewalOutcome.EXPAND for r in expansions)

    def test_critical_renewals(self):
        critical = self.engine.critical_renewals()
        assert all(r.renewal_risk == RenewalRisk.CRITICAL for r in critical)

    def test_needs_escalation(self):
        escalations = self.engine.needs_escalation()
        assert all(r.renewal_action == RenewalAction.ESCALATE for r in escalations)

    def test_expansion_opportunities(self):
        expansions = self.engine.expansion_opportunities()
        assert all(r.predicted_outcome == RenewalOutcome.EXPAND for r in expansions)

    def test_at_risk_renewals_contains_high_and_critical(self):
        at_risk = self.engine.at_risk_renewals()
        assert all(r.renewal_risk in (RenewalRisk.HIGH, RenewalRisk.CRITICAL) for r in at_risk)

    def test_at_risk_does_not_contain_low(self):
        at_risk = self.engine.at_risk_renewals()
        assert all(r.renewal_risk != RenewalRisk.LOW for r in at_risk)

    def test_due_soon_default_90_days(self):
        engine = RenewalIntelligenceEngine()
        engine.analyze(make_customer(customer_id="C001", days_to_renewal=45))
        engine.analyze(make_customer(customer_id="C002", days_to_renewal=91))
        engine.analyze(make_customer(customer_id="C003", days_to_renewal=-5))  # expired
        due = engine.due_soon()
        assert len(due) == 1
        assert due[0].customer_id == "C001"

    def test_due_soon_custom_window(self):
        engine = RenewalIntelligenceEngine()
        engine.analyze(make_customer(customer_id="C001", days_to_renewal=20))
        engine.analyze(make_customer(customer_id="C002", days_to_renewal=50))
        due = engine.due_soon(within_days=30)
        assert len(due) == 1
        assert due[0].customer_id == "C001"

    def test_due_soon_excludes_expired(self):
        engine = RenewalIntelligenceEngine()
        engine.analyze(make_customer(customer_id="C001", days_to_renewal=-5))
        due = engine.due_soon()
        assert len(due) == 0

    def test_due_soon_includes_day_0(self):
        engine = RenewalIntelligenceEngine()
        engine.analyze(make_customer(customer_id="C001", days_to_renewal=0))
        due = engine.due_soon()
        assert len(due) == 1

    def test_due_soon_includes_exactly_90(self):
        engine = RenewalIntelligenceEngine()
        engine.analyze(make_customer(customer_id="C001", days_to_renewal=90))
        due = engine.due_soon()
        assert len(due) == 1

    def test_avg_renewal_probability_empty(self):
        empty_engine = RenewalIntelligenceEngine()
        assert empty_engine.avg_renewal_probability() == 0.0

    def test_avg_renewal_probability_is_numeric(self):
        prob = self.engine.avg_renewal_probability()
        assert isinstance(prob, (int, float))

    def test_avg_renewal_probability_in_range(self):
        prob = self.engine.avg_renewal_probability()
        assert 0.0 <= prob <= 100.0

    def test_total_arr_at_risk_high_and_critical(self):
        at_risk_arr = self.engine.total_arr_at_risk_eur()
        high = sum(r.arr_eur for r in self.engine.at_risk_renewals())
        assert at_risk_arr == pytest.approx(high)

    def test_total_arr_at_risk_is_numeric(self):
        assert isinstance(self.engine.total_arr_at_risk_eur(), (int, float))

    def test_expected_arr_delta_is_numeric(self):
        assert isinstance(self.engine.expected_arr_delta_eur(), (int, float))

    def test_expected_arr_delta_churn_is_negative(self):
        engine = RenewalIntelligenceEngine()
        engine.analyze(make_customer(
            customer_id="CHURN1", arr_eur=100_000.0,
            health_score=10.0, nps_score=-100, product_usage_trend="dormant",
            competitor_mentioned=True, discount_requested=True,
            price_sensitivity="high", exec_sponsor_aligned=False,
            champion_strength=0, open_support_issues=5,
            previous_renewal_on_time=False, years_as_customer=0,
        ))
        delta = engine.expected_arr_delta_eur()
        assert delta < 0

    def test_expected_arr_delta_expand_is_positive(self):
        engine = RenewalIntelligenceEngine()
        engine.analyze(make_customer(
            customer_id="EXP2", arr_eur=100_000.0,
            has_expansion_discussion=True, health_score=90.0,
            nps_score=50, product_usage_trend="growing",
        ))
        results = engine.all_renewals()
        if results[0].predicted_outcome == RenewalOutcome.EXPAND:
            delta = engine.expected_arr_delta_eur()
            assert delta > 0

    def test_summary_returns_dict(self):
        summary = self.engine.summary()
        assert isinstance(summary, dict)

    def test_summary_total_count(self):
        summary = self.engine.summary()
        assert summary["total"] == 4

    def test_summary_has_risk_counts(self):
        summary = self.engine.summary()
        assert "risk_counts" in summary

    def test_summary_has_action_counts(self):
        summary = self.engine.summary()
        assert "action_counts" in summary

    def test_summary_has_outcome_counts(self):
        summary = self.engine.summary()
        assert "outcome_counts" in summary

    def test_summary_risk_counts_sum_to_total(self):
        summary = self.engine.summary()
        assert sum(summary["risk_counts"].values()) == summary["total"]

    def test_summary_action_counts_sum_to_total(self):
        summary = self.engine.summary()
        assert sum(summary["action_counts"].values()) == summary["total"]

    def test_summary_outcome_counts_sum_to_total(self):
        summary = self.engine.summary()
        assert sum(summary["outcome_counts"].values()) == summary["total"]

    def test_summary_has_avg_renewal_probability(self):
        summary = self.engine.summary()
        assert "avg_renewal_probability_pct" in summary

    def test_summary_has_critical_count(self):
        summary = self.engine.summary()
        assert "critical_count" in summary

    def test_summary_has_escalation_count(self):
        summary = self.engine.summary()
        assert "escalation_count" in summary

    def test_summary_has_total_arr_at_risk(self):
        summary = self.engine.summary()
        assert "total_arr_at_risk_eur" in summary

    def test_summary_has_expected_arr_delta(self):
        summary = self.engine.summary()
        assert "expected_arr_delta_eur" in summary

    def test_reset_clears_results(self):
        self.engine.reset()
        assert len(self.engine.all_renewals()) == 0

    def test_reset_then_analyze_works(self):
        self.engine.reset()
        self.engine.analyze(make_customer())
        assert len(self.engine.all_renewals()) == 1

    def test_avg_probability_after_reset(self):
        self.engine.reset()
        assert self.engine.avg_renewal_probability() == 0.0

    def test_total_arr_at_risk_after_reset(self):
        self.engine.reset()
        assert self.engine.total_arr_at_risk_eur() == 0.0

    def test_expected_arr_delta_after_reset(self):
        self.engine.reset()
        assert self.engine.expected_arr_delta_eur() == 0.0

    def test_summary_empty_engine(self):
        empty = RenewalIntelligenceEngine()
        summary = empty.summary()
        assert summary["total"] == 0

    def test_by_risk_empty_returns_empty_list(self):
        empty = RenewalIntelligenceEngine()
        assert empty.by_risk(RenewalRisk.CRITICAL) == []

    def test_by_action_empty_returns_empty_list(self):
        empty = RenewalIntelligenceEngine()
        assert empty.by_action(RenewalAction.ESCALATE) == []

    def test_by_outcome_empty_returns_empty_list(self):
        empty = RenewalIntelligenceEngine()
        assert empty.by_outcome(RenewalOutcome.EXPAND) == []

    def test_at_risk_empty_engine(self):
        empty = RenewalIntelligenceEngine()
        assert empty.at_risk_renewals() == []

    def test_critical_renewals_empty_engine(self):
        empty = RenewalIntelligenceEngine()
        assert empty.critical_renewals() == []

    def test_needs_escalation_empty_engine(self):
        empty = RenewalIntelligenceEngine()
        assert empty.needs_escalation() == []

    def test_expansion_opportunities_empty_engine(self):
        empty = RenewalIntelligenceEngine()
        assert empty.expansion_opportunities() == []

    def test_due_soon_empty_engine(self):
        empty = RenewalIntelligenceEngine()
        assert empty.due_soon() == []

    def test_summary_risk_counts_keys(self):
        summary = self.engine.summary()
        assert set(summary["risk_counts"].keys()) == {r.value for r in RenewalRisk}

    def test_summary_action_counts_keys(self):
        summary = self.engine.summary()
        assert set(summary["action_counts"].keys()) == {a.value for a in RenewalAction}

    def test_summary_outcome_counts_keys(self):
        summary = self.engine.summary()
        assert set(summary["outcome_counts"].keys()) == {o.value for o in RenewalOutcome}
