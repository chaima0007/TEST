"""
Pytest test suite for SalesBuyerIntentSignalDecayEngine (Module 213).
"""
import pytest
from swarm.intelligence.sales_buyer_intent_signal_decay_engine import (
    IntentAction,
    IntentInput,
    IntentPattern,
    IntentResult,
    IntentRisk,
    IntentSeverity,
    SalesBuyerIntentSignalDecayEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> IntentInput:
    """Return a baseline IntentInput with all signals at benign / low-decay values."""
    defaults = dict(
        rep_id="rep-001",
        region="EMEA",
        evaluation_period_id="2026-Q2",
        website_visit_decay_rate_pct=0.0,
        email_open_rate_decay_pct=0.0,
        content_download_decay_rate_pct=0.0,
        avg_days_since_last_digital_touch=0.0,
        demo_no_show_rate_pct=0.0,
        demo_follow_up_response_rate_pct=1.0,
        evaluation_activity_score=1.0,
        trial_feature_adoption_rate_pct=1.0,
        champion_response_latency_days=0.0,
        champion_meeting_acceptance_rate_pct=1.0,
        champion_internal_forward_rate_pct=1.0,
        intent_score_trend=1.0,
        buying_committee_engagement_score=1.0,
        multi_contact_engagement_rate_pct=1.0,
        days_since_last_positive_signal=0.0,
        intent_data_coverage_score=1.0,
        deals_with_intent_decay=0,
        avg_deal_value_usd=0.0,
    )
    defaults.update(overrides)
    return IntentInput(**defaults)


def fresh_engine() -> SalesBuyerIntentSignalDecayEngine:
    return SalesBuyerIntentSignalDecayEngine()


# ---------------------------------------------------------------------------
# 1. Enum values — string subclass
# ---------------------------------------------------------------------------

class TestEnums:
    def test_intent_risk_is_str_subclass(self):
        for member in IntentRisk:
            assert isinstance(member, str)

    def test_intent_risk_values(self):
        assert {m.value for m in IntentRisk} == {"low", "moderate", "high", "critical"}

    def test_intent_pattern_is_str_subclass(self):
        for member in IntentPattern:
            assert isinstance(member, str)

    def test_intent_pattern_values(self):
        assert {m.value for m in IntentPattern} == {
            "none",
            "digital_ghost",
            "content_disengagement",
            "demo_dropout",
            "champion_signal_fade",
            "evaluation_abandonment",
        }

    def test_intent_severity_is_str_subclass(self):
        for member in IntentSeverity:
            assert isinstance(member, str)

    def test_intent_severity_values(self):
        assert {m.value for m in IntentSeverity} == {
            "engaged", "warming", "cooling", "cold"
        }

    def test_intent_action_is_str_subclass(self):
        for member in IntentAction:
            assert isinstance(member, str)

    def test_intent_action_values(self):
        assert {m.value for m in IntentAction} == {
            "no_action",
            "intent_monitoring",
            "re_engagement_outreach",
            "content_nurture_activation",
            "demo_reactivation_campaign",
            "champion_reactivation_call",
            "deal_rescue_intervention",
            "pipeline_purge_recommendation",
            "executive_reconnect_protocol",
        }


# ---------------------------------------------------------------------------
# 2. to_dict — exactly 15 keys, enums serialized as plain strings
# ---------------------------------------------------------------------------

class TestToDict:
    def test_to_dict_has_15_keys(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_expected_keys(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        expected = {
            "rep_id", "region", "intent_risk", "intent_pattern", "intent_severity",
            "recommended_action", "engagement_score", "signal_score", "champion_score",
            "freshness_score", "intent_composite", "has_intent_gap",
            "requires_reengagement", "estimated_cold_pipeline_usd", "intent_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_enums_are_plain_strings(self):
        engine = fresh_engine()
        d = engine.assess(make_input()).to_dict()
        for key in ("intent_risk", "intent_pattern", "intent_severity", "recommended_action"):
            assert type(d[key]) is str, f"{key} should be plain str"


# ---------------------------------------------------------------------------
# 3. Sub-scores — threshold tiers, cap at 100, additive
# ---------------------------------------------------------------------------

class TestEngagementScore:
    def setup_method(self):
        self.e = fresh_engine()

    def test_zero_inputs_give_zero(self):
        assert self.e._engagement_score(make_input()) == 0

    def test_website_tier_low(self):
        i = make_input(website_visit_decay_rate_pct=0.18)
        assert self.e._engagement_score(i) == 8

    def test_website_tier_mid(self):
        i = make_input(website_visit_decay_rate_pct=0.35)
        assert self.e._engagement_score(i) == 22

    def test_website_tier_high(self):
        i = make_input(website_visit_decay_rate_pct=0.60)
        assert self.e._engagement_score(i) == 40

    def test_email_tier_mid(self):
        i = make_input(email_open_rate_decay_pct=0.30)
        assert self.e._engagement_score(i) == 18

    def test_email_tier_high(self):
        i = make_input(email_open_rate_decay_pct=0.55)
        assert self.e._engagement_score(i) == 35

    def test_digital_touch_tier_mid(self):
        i = make_input(avg_days_since_last_digital_touch=14)
        assert self.e._engagement_score(i) == 12

    def test_digital_touch_tier_high(self):
        i = make_input(avg_days_since_last_digital_touch=30)
        assert self.e._engagement_score(i) == 25

    def test_additive(self):
        i = make_input(
            website_visit_decay_rate_pct=0.60,   # +40
            email_open_rate_decay_pct=0.55,       # +35
            avg_days_since_last_digital_touch=30, # +25
        )
        assert self.e._engagement_score(i) == 100  # 100 capped

    def test_cap_at_100(self):
        i = make_input(
            website_visit_decay_rate_pct=1.0,
            email_open_rate_decay_pct=1.0,
            avg_days_since_last_digital_touch=100,
        )
        assert self.e._engagement_score(i) == 100


class TestSignalScore:
    def setup_method(self):
        self.e = fresh_engine()

    def test_zero_inputs_give_zero(self):
        assert self.e._signal_score(make_input()) == 0

    def test_trend_tier_low(self):
        i = make_input(intent_score_trend=-0.10)
        assert self.e._signal_score(i) == 10

    def test_trend_tier_mid(self):
        i = make_input(intent_score_trend=-0.30)
        assert self.e._signal_score(i) == 25

    def test_trend_tier_high(self):
        i = make_input(intent_score_trend=-0.60)
        assert self.e._signal_score(i) == 45

    def test_committee_tier_mid(self):
        i = make_input(buying_committee_engagement_score=0.45)
        assert self.e._signal_score(i) == 15

    def test_committee_tier_high(self):
        i = make_input(buying_committee_engagement_score=0.20)
        assert self.e._signal_score(i) == 30

    def test_multi_contact_tier_mid(self):
        i = make_input(multi_contact_engagement_rate_pct=0.35)
        assert self.e._signal_score(i) == 12

    def test_multi_contact_tier_high(self):
        i = make_input(multi_contact_engagement_rate_pct=0.15)
        assert self.e._signal_score(i) == 25

    def test_cap_at_100(self):
        i = make_input(
            intent_score_trend=-1.0,
            buying_committee_engagement_score=0.0,
            multi_contact_engagement_rate_pct=0.0,
        )
        assert self.e._signal_score(i) == 100


class TestChampionScore:
    def setup_method(self):
        self.e = fresh_engine()

    def test_zero_inputs_give_zero(self):
        assert self.e._champion_score(make_input()) == 0

    def test_latency_tier_low(self):
        i = make_input(champion_response_latency_days=3.5)
        assert self.e._champion_score(i) == 8

    def test_latency_tier_mid(self):
        i = make_input(champion_response_latency_days=7.0)
        assert self.e._champion_score(i) == 22

    def test_latency_tier_high(self):
        i = make_input(champion_response_latency_days=14.0)
        assert self.e._champion_score(i) == 40

    def test_meeting_accept_tier_mid(self):
        i = make_input(champion_meeting_acceptance_rate_pct=0.45)
        assert self.e._champion_score(i) == 18

    def test_meeting_accept_tier_high(self):
        i = make_input(champion_meeting_acceptance_rate_pct=0.20)
        assert self.e._champion_score(i) == 35

    def test_forward_tier_mid(self):
        i = make_input(champion_internal_forward_rate_pct=0.25)
        assert self.e._champion_score(i) == 12

    def test_forward_tier_high(self):
        i = make_input(champion_internal_forward_rate_pct=0.10)
        assert self.e._champion_score(i) == 25

    def test_cap_at_100(self):
        i = make_input(
            champion_response_latency_days=100.0,
            champion_meeting_acceptance_rate_pct=0.0,
            champion_internal_forward_rate_pct=0.0,
        )
        assert self.e._champion_score(i) == 100


class TestFreshnessScore:
    def setup_method(self):
        self.e = fresh_engine()

    def test_zero_inputs_give_zero(self):
        assert self.e._freshness_score(make_input()) == 0

    def test_days_tier_low(self):
        i = make_input(days_since_last_positive_signal=10)
        assert self.e._freshness_score(i) == 10

    def test_days_tier_mid(self):
        i = make_input(days_since_last_positive_signal=21)
        assert self.e._freshness_score(i) == 25

    def test_days_tier_high(self):
        i = make_input(days_since_last_positive_signal=45)
        assert self.e._freshness_score(i) == 45

    def test_content_download_tier_mid(self):
        i = make_input(content_download_decay_rate_pct=0.30)
        assert self.e._freshness_score(i) == 15

    def test_content_download_tier_high(self):
        i = make_input(content_download_decay_rate_pct=0.55)
        assert self.e._freshness_score(i) == 30

    def test_coverage_tier_mid(self):
        i = make_input(intent_data_coverage_score=0.45)
        assert self.e._freshness_score(i) == 12

    def test_coverage_tier_high(self):
        i = make_input(intent_data_coverage_score=0.20)
        assert self.e._freshness_score(i) == 25

    def test_cap_at_100(self):
        i = make_input(
            days_since_last_positive_signal=100,
            content_download_decay_rate_pct=1.0,
            intent_data_coverage_score=0.0,
        )
        assert self.e._freshness_score(i) == 100


# ---------------------------------------------------------------------------
# 4. Composite weights and cap
# ---------------------------------------------------------------------------

class TestComposite:
    def setup_method(self):
        self.e = fresh_engine()

    def test_weights_sum_correctly(self):
        # en=100, si=0, ch=0, fr=0  → 100*0.30 = 30
        assert self.e._composite(100, 0, 0, 0) == 30.0

    def test_all_weights(self):
        # 40*0.30 + 60*0.25 + 80*0.25 + 100*0.20
        # = 12 + 15 + 20 + 20 = 67
        assert self.e._composite(40, 60, 80, 100) == 67.0

    def test_cap_at_100(self):
        assert self.e._composite(100, 100, 100, 100) == 100.0

    def test_rounding_to_2dp(self):
        # 10*0.30 + 10*0.25 + 10*0.25 + 10*0.20 = 10.00
        result = self.e._composite(10, 10, 10, 10)
        assert result == round(result, 2)

    def test_zero_gives_zero(self):
        assert self.e._composite(0, 0, 0, 0) == 0.0


# ---------------------------------------------------------------------------
# 5. Risk thresholds
# ---------------------------------------------------------------------------

class TestRisk:
    def setup_method(self):
        self.e = fresh_engine()

    def test_low(self):
        assert self.e._risk(0.0) == IntentRisk.low
        assert self.e._risk(19.99) == IntentRisk.low

    def test_moderate(self):
        assert self.e._risk(20.0) == IntentRisk.moderate
        assert self.e._risk(39.99) == IntentRisk.moderate

    def test_high(self):
        assert self.e._risk(40.0) == IntentRisk.high
        assert self.e._risk(59.99) == IntentRisk.high

    def test_critical(self):
        assert self.e._risk(60.0) == IntentRisk.critical
        assert self.e._risk(100.0) == IntentRisk.critical


# ---------------------------------------------------------------------------
# 6. Severity thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def setup_method(self):
        self.e = fresh_engine()

    def test_engaged(self):
        assert self.e._severity(0.0) == IntentSeverity.engaged
        assert self.e._severity(19.99) == IntentSeverity.engaged

    def test_warming(self):
        assert self.e._severity(20.0) == IntentSeverity.warming
        assert self.e._severity(39.99) == IntentSeverity.warming

    def test_cooling(self):
        assert self.e._severity(40.0) == IntentSeverity.cooling
        assert self.e._severity(59.99) == IntentSeverity.cooling

    def test_cold(self):
        assert self.e._severity(60.0) == IntentSeverity.cold
        assert self.e._severity(100.0) == IntentSeverity.cold


# ---------------------------------------------------------------------------
# 7. Pattern priority
# ---------------------------------------------------------------------------

class TestPattern:
    def setup_method(self):
        self.e = fresh_engine()

    def test_none_pattern_when_no_flags(self):
        assert self.e._pattern(make_input()) == IntentPattern.none

    def test_digital_ghost(self):
        i = make_input(website_visit_decay_rate_pct=0.55, avg_days_since_last_digital_touch=21)
        assert self.e._pattern(i) == IntentPattern.digital_ghost

    def test_content_disengagement(self):
        i = make_input(content_download_decay_rate_pct=0.50, buying_committee_engagement_score=0.25)
        assert self.e._pattern(i) == IntentPattern.content_disengagement

    def test_demo_dropout(self):
        i = make_input(demo_no_show_rate_pct=0.50, demo_follow_up_response_rate_pct=0.25)
        assert self.e._pattern(i) == IntentPattern.demo_dropout

    def test_champion_signal_fade(self):
        i = make_input(champion_response_latency_days=10.0, champion_meeting_acceptance_rate_pct=0.25)
        assert self.e._pattern(i) == IntentPattern.champion_signal_fade

    def test_evaluation_abandonment(self):
        i = make_input(evaluation_activity_score=0.20, trial_feature_adoption_rate_pct=0.20)
        assert self.e._pattern(i) == IntentPattern.evaluation_abandonment

    def test_digital_ghost_wins_over_content_disengagement(self):
        """digital_ghost is checked first and should take priority."""
        i = make_input(
            website_visit_decay_rate_pct=0.55,
            avg_days_since_last_digital_touch=21,
            content_download_decay_rate_pct=0.50,
            buying_committee_engagement_score=0.25,
        )
        assert self.e._pattern(i) == IntentPattern.digital_ghost


# ---------------------------------------------------------------------------
# 8. Action rules for each risk × pattern combination
# ---------------------------------------------------------------------------

class TestAction:
    def setup_method(self):
        self.e = fresh_engine()

    # Critical risk
    def test_critical_digital_ghost(self):
        assert self.e._action(IntentRisk.critical, IntentPattern.digital_ghost) == IntentAction.pipeline_purge_recommendation

    def test_critical_evaluation_abandonment(self):
        assert self.e._action(IntentRisk.critical, IntentPattern.evaluation_abandonment) == IntentAction.pipeline_purge_recommendation

    def test_critical_champion_signal_fade(self):
        assert self.e._action(IntentRisk.critical, IntentPattern.champion_signal_fade) == IntentAction.executive_reconnect_protocol

    def test_critical_content_disengagement(self):
        assert self.e._action(IntentRisk.critical, IntentPattern.content_disengagement) == IntentAction.deal_rescue_intervention

    def test_critical_demo_dropout(self):
        assert self.e._action(IntentRisk.critical, IntentPattern.demo_dropout) == IntentAction.deal_rescue_intervention

    def test_critical_none(self):
        assert self.e._action(IntentRisk.critical, IntentPattern.none) == IntentAction.deal_rescue_intervention

    # High risk
    def test_high_digital_ghost(self):
        assert self.e._action(IntentRisk.high, IntentPattern.digital_ghost) == IntentAction.re_engagement_outreach

    def test_high_content_disengagement(self):
        assert self.e._action(IntentRisk.high, IntentPattern.content_disengagement) == IntentAction.content_nurture_activation

    def test_high_demo_dropout(self):
        assert self.e._action(IntentRisk.high, IntentPattern.demo_dropout) == IntentAction.demo_reactivation_campaign

    def test_high_champion_signal_fade(self):
        assert self.e._action(IntentRisk.high, IntentPattern.champion_signal_fade) == IntentAction.champion_reactivation_call

    def test_high_evaluation_abandonment(self):
        assert self.e._action(IntentRisk.high, IntentPattern.evaluation_abandonment) == IntentAction.deal_rescue_intervention

    def test_high_none(self):
        assert self.e._action(IntentRisk.high, IntentPattern.none) == IntentAction.intent_monitoring

    # Moderate risk
    def test_moderate_any_pattern(self):
        for pat in IntentPattern:
            assert self.e._action(IntentRisk.moderate, pat) == IntentAction.intent_monitoring

    # Low risk
    def test_low_any_pattern(self):
        for pat in IntentPattern:
            assert self.e._action(IntentRisk.low, pat) == IntentAction.no_action


# ---------------------------------------------------------------------------
# 9. has_intent_gap
# ---------------------------------------------------------------------------

class TestHasIntentGap:
    def setup_method(self):
        self.e = fresh_engine()

    def test_false_when_all_below_thresholds(self):
        i = make_input(
            days_since_last_positive_signal=0,
            buying_committee_engagement_score=1.0,
        )
        assert self.e._has_intent_gap(i, 0.0) is False

    def test_true_via_composite_gte_40(self):
        i = make_input(buying_committee_engagement_score=1.0, days_since_last_positive_signal=0)
        assert self.e._has_intent_gap(i, 40.0) is True

    def test_true_via_days_gte_21(self):
        i = make_input(days_since_last_positive_signal=21, buying_committee_engagement_score=1.0)
        assert self.e._has_intent_gap(i, 0.0) is True

    def test_true_via_committee_lte_035(self):
        i = make_input(buying_committee_engagement_score=0.35, days_since_last_positive_signal=0)
        assert self.e._has_intent_gap(i, 0.0) is True

    def test_boundary_days_20_is_false(self):
        i = make_input(days_since_last_positive_signal=20, buying_committee_engagement_score=1.0)
        assert self.e._has_intent_gap(i, 0.0) is False

    def test_boundary_committee_036_is_false(self):
        i = make_input(buying_committee_engagement_score=0.36, days_since_last_positive_signal=0)
        assert self.e._has_intent_gap(i, 0.0) is False


# ---------------------------------------------------------------------------
# 10. requires_reengagement
# ---------------------------------------------------------------------------

class TestRequiresReengagement:
    def setup_method(self):
        self.e = fresh_engine()

    def test_false_when_all_below_thresholds(self):
        i = make_input(champion_response_latency_days=0.0, website_visit_decay_rate_pct=0.0)
        assert self.e._requires_reengagement(i, 0.0) is False

    def test_true_via_composite_gte_25(self):
        i = make_input(champion_response_latency_days=0.0, website_visit_decay_rate_pct=0.0)
        assert self.e._requires_reengagement(i, 25.0) is True

    def test_true_via_latency_gte_7(self):
        i = make_input(champion_response_latency_days=7.0, website_visit_decay_rate_pct=0.0)
        assert self.e._requires_reengagement(i, 0.0) is True

    def test_true_via_website_decay_gte_030(self):
        i = make_input(website_visit_decay_rate_pct=0.30, champion_response_latency_days=0.0)
        assert self.e._requires_reengagement(i, 0.0) is True

    def test_boundary_latency_69_is_false(self):
        i = make_input(champion_response_latency_days=6.9, website_visit_decay_rate_pct=0.0)
        assert self.e._requires_reengagement(i, 0.0) is False

    def test_boundary_decay_029_is_false(self):
        i = make_input(website_visit_decay_rate_pct=0.29, champion_response_latency_days=0.0)
        assert self.e._requires_reengagement(i, 0.0) is False


# ---------------------------------------------------------------------------
# 11. estimated_cold_pipeline_usd
# ---------------------------------------------------------------------------

class TestColdPipeline:
    def setup_method(self):
        self.e = fresh_engine()

    def test_zero_deals_gives_zero(self):
        i = make_input(deals_with_intent_decay=0, avg_deal_value_usd=50_000.0, buying_committee_engagement_score=0.5)
        assert self.e._cold_pipeline(i, 80.0) == 0.0

    def test_zero_composite_gives_zero(self):
        i = make_input(deals_with_intent_decay=5, avg_deal_value_usd=50_000.0)
        assert self.e._cold_pipeline(i, 0.0) == 0.0

    def test_formula_basic(self):
        # 2 * 100_000 * (1 - 0.6) * (50/100) = 200_000 * 0.4 * 0.5 = 40_000
        i = make_input(deals_with_intent_decay=2, avg_deal_value_usd=100_000.0,
                       buying_committee_engagement_score=0.6)
        assert self.e._cold_pipeline(i, 50.0) == 40_000.0

    def test_min_engagement_floor_at_005(self):
        # engagement=0.00 → max(0.00, 0.05)=0.05 → factor=(1-0.05)=0.95
        # 1 * 10_000 * 0.95 * (100/100) = 9_500.0
        i = make_input(deals_with_intent_decay=1, avg_deal_value_usd=10_000.0,
                       buying_committee_engagement_score=0.0)
        assert self.e._cold_pipeline(i, 100.0) == 9_500.0

    def test_result_rounded_to_2dp(self):
        i = make_input(deals_with_intent_decay=3, avg_deal_value_usd=33_333.33,
                       buying_committee_engagement_score=0.5)
        result = self.e._cold_pipeline(i, 75.0)
        assert result == round(result, 2)


# ---------------------------------------------------------------------------
# 12. intent_signal
# ---------------------------------------------------------------------------

class TestIntentSignal:
    def setup_method(self):
        self.e = fresh_engine()

    def test_stable_message_when_composite_below_20(self):
        sig = self.e._signal(make_input(), IntentPattern.none, 19.99)
        assert "healthy" in sig.lower()
        assert "benchmark" in sig.lower()

    def test_active_label_digital_ghost(self):
        i = make_input(website_visit_decay_rate_pct=0.55, days_since_last_positive_signal=25, champion_response_latency_days=5.0)
        sig = self.e._signal(i, IntentPattern.digital_ghost, 70.0)
        assert "Digital ghost" in sig

    def test_active_label_content_disengagement(self):
        i = make_input(website_visit_decay_rate_pct=0.0, days_since_last_positive_signal=5, champion_response_latency_days=1.0)
        sig = self.e._signal(i, IntentPattern.content_disengagement, 50.0)
        assert "Content disengagement" in sig

    def test_active_label_demo_dropout(self):
        i = make_input()
        sig = self.e._signal(i, IntentPattern.demo_dropout, 50.0)
        assert "Demo dropout" in sig

    def test_active_label_champion_signal_fade(self):
        i = make_input()
        sig = self.e._signal(i, IntentPattern.champion_signal_fade, 50.0)
        assert "Champion signal fade" in sig

    def test_active_label_evaluation_abandonment(self):
        i = make_input()
        sig = self.e._signal(i, IntentPattern.evaluation_abandonment, 50.0)
        assert "Evaluation abandonment" in sig

    def test_active_signal_contains_composite(self):
        i = make_input(website_visit_decay_rate_pct=0.4, days_since_last_positive_signal=10, champion_response_latency_days=2.0)
        sig = self.e._signal(i, IntentPattern.digital_ghost, 65.0)
        assert "65" in sig

    def test_active_signal_contains_web_decay_pct(self):
        i = make_input(website_visit_decay_rate_pct=0.42, days_since_last_positive_signal=5, champion_response_latency_days=1.0)
        sig = self.e._signal(i, IntentPattern.none, 30.0)
        assert "42%" in sig


# ---------------------------------------------------------------------------
# 13. assess(), assess_batch(), summary() with 13 keys
# ---------------------------------------------------------------------------

class TestAssess:
    def test_assess_returns_intent_result(self):
        engine = fresh_engine()
        result = engine.assess(make_input())
        assert isinstance(result, IntentResult)

    def test_assess_rep_id_and_region_propagated(self):
        engine = fresh_engine()
        r = engine.assess(make_input(rep_id="REP-X", region="APAC"))
        assert r.rep_id == "REP-X"
        assert r.region == "APAC"

    def test_assess_low_risk_all_zeros(self):
        engine = fresh_engine()
        r = engine.assess(make_input())
        assert r.intent_risk == "low"
        assert r.intent_composite == 0.0


class TestAssessBatch:
    def test_returns_list_of_results(self):
        engine = fresh_engine()
        inputs = [make_input(rep_id=f"rep-{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5
        assert all(isinstance(r, IntentResult) for r in results)

    def test_batch_accumulates_in_engine(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(), make_input()])
        assert engine.summary()["total"] == 2


class TestSummary:
    def test_empty_summary_has_13_keys(self):
        engine = fresh_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_values(self):
        engine = fresh_engine()
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_intent_composite"] == 0.0
        assert s["total_estimated_cold_pipeline_usd"] == 0.0

    def test_summary_after_assessments(self):
        engine = fresh_engine()
        engine.assess_batch([make_input(), make_input()])
        s = engine.summary()
        assert s["total"] == 2
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 2

    def test_summary_13_keys_after_assessments(self):
        engine = fresh_engine()
        engine.assess(make_input())
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_intent_composite", "intent_gap_count",
            "reengagement_count", "avg_engagement_score", "avg_signal_score",
            "avg_champion_score", "avg_freshness_score",
            "total_estimated_cold_pipeline_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_cold_pipeline_aggregation(self):
        engine = fresh_engine()
        # Two inputs each producing non-zero cold pipeline
        i1 = make_input(deals_with_intent_decay=1, avg_deal_value_usd=10_000.0,
                        buying_committee_engagement_score=0.5,
                        # push composite above 0 via website decay
                        website_visit_decay_rate_pct=0.60,
                        email_open_rate_decay_pct=0.55,
                        avg_days_since_last_digital_touch=30)
        engine.assess_batch([i1, i1])
        s = engine.summary()
        # Each should produce the same pipeline value; total = 2×
        single = engine.assess(i1)
        assert s["total_estimated_cold_pipeline_usd"] == pytest.approx(
            2 * single.estimated_cold_pipeline_usd, rel=1e-3
        )


# ---------------------------------------------------------------------------
# 14. Edge cases: zero input, max input, engine isolation
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_input_no_exception(self):
        """All-zero fields trigger <= thresholds in signal/champion/freshness scores.
        The composite will be non-zero; assert no exception is raised and the
        pipeline is zero because deals_with_intent_decay=0."""
        engine = fresh_engine()
        i = make_input(
            website_visit_decay_rate_pct=0.0,
            email_open_rate_decay_pct=0.0,
            content_download_decay_rate_pct=0.0,
            avg_days_since_last_digital_touch=0.0,
            demo_no_show_rate_pct=0.0,
            demo_follow_up_response_rate_pct=0.0,
            evaluation_activity_score=0.0,
            trial_feature_adoption_rate_pct=0.0,
            champion_response_latency_days=0.0,
            champion_meeting_acceptance_rate_pct=0.0,
            champion_internal_forward_rate_pct=0.0,
            intent_score_trend=0.0,
            buying_committee_engagement_score=0.0,
            multi_contact_engagement_rate_pct=0.0,
            days_since_last_positive_signal=0.0,
            intent_data_coverage_score=0.0,
            deals_with_intent_decay=0,
            avg_deal_value_usd=0.0,
        )
        r = engine.assess(i)
        # composite may be non-zero (0.0 triggers <= thresholds); pipeline is zero
        assert isinstance(r.intent_composite, float)
        assert r.estimated_cold_pipeline_usd == 0.0

    def test_max_input_capped_at_100(self):
        engine = fresh_engine()
        i = make_input(
            website_visit_decay_rate_pct=1.0,
            email_open_rate_decay_pct=1.0,
            content_download_decay_rate_pct=1.0,
            avg_days_since_last_digital_touch=365.0,
            demo_no_show_rate_pct=1.0,
            demo_follow_up_response_rate_pct=0.0,
            evaluation_activity_score=0.0,
            trial_feature_adoption_rate_pct=0.0,
            champion_response_latency_days=365.0,
            champion_meeting_acceptance_rate_pct=0.0,
            champion_internal_forward_rate_pct=0.0,
            intent_score_trend=-1.0,
            buying_committee_engagement_score=0.0,
            multi_contact_engagement_rate_pct=0.0,
            days_since_last_positive_signal=365.0,
            intent_data_coverage_score=0.0,
            deals_with_intent_decay=100,
            avg_deal_value_usd=1_000_000.0,
        )
        r = engine.assess(i)
        assert r.engagement_score <= 100
        assert r.signal_score <= 100
        assert r.champion_score <= 100
        assert r.freshness_score <= 100
        assert r.intent_composite <= 100.0
        assert r.intent_risk == "critical"
        assert r.intent_severity == "cold"

    def test_engine_isolation(self):
        """Two separate engines do not share state."""
        e1 = fresh_engine()
        e2 = fresh_engine()
        e1.assess(make_input())
        assert e1.summary()["total"] == 1
        assert e2.summary()["total"] == 0

    def test_results_accumulate_across_calls(self):
        engine = fresh_engine()
        for _ in range(10):
            engine.assess(make_input())
        assert engine.summary()["total"] == 10

    def test_intent_score_trend_boundary_exactly_minus_010(self):
        e = fresh_engine()
        i = make_input(intent_score_trend=-0.10)
        assert e._signal_score(i) == 10

    def test_buying_committee_boundary_exactly_045(self):
        e = fresh_engine()
        i = make_input(buying_committee_engagement_score=0.45)
        assert e._signal_score(i) == 15

    def test_cold_pipeline_floor_engagement_not_below_005(self):
        e = fresh_engine()
        # negative-like value should still floor at 0.05 via max()
        i = make_input(deals_with_intent_decay=1, avg_deal_value_usd=1000.0,
                       buying_committee_engagement_score=-0.5)
        result = e._cold_pipeline(i, 100.0)
        # max(-0.5, 0.05) = 0.05 → (1 - 0.05) = 0.95
        assert result == pytest.approx(950.0)
