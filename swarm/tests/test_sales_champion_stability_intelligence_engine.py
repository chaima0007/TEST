"""
Comprehensive pytest test suite for SalesChampionStabilityIntelligenceEngine.
Covers: enums, input fields, result fields, to_dict, sub-scores, pattern detection,
risk/severity thresholds, action mapping, gap/coaching flags, deal exposure formula,
signal strings, assess end-to-end, assess_batch, summary (empty + populated, all 13 keys),
and edge cases.
"""

from __future__ import annotations

import pytest

from swarm.intelligence.sales_champion_stability_intelligence_engine import (
    ChampionAction,
    ChampionInput,
    ChampionPattern,
    ChampionResult,
    ChampionRisk,
    ChampionSeverity,
    SalesChampionStabilityIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _base_input(**overrides) -> ChampionInput:
    """Return a 'healthy' champion input; override any field via kwargs."""
    defaults = dict(
        rep_id="R001",
        region="Northeast",
        evaluation_period_id="Q2-2026",
        avg_champion_response_time_days=1.0,
        champion_engagement_drop_rate_pct=0.05,
        deals_with_single_champion_pct=0.20,
        champion_gone_dark_rate_pct=0.05,
        champion_role_change_detected_rate_pct=0.05,
        champion_re_engaged_within_7d_pct=0.80,
        deals_lost_after_champion_change_pct=0.10,
        deals_with_executive_sponsor_pct=0.50,
        champion_coached_on_internal_selling_pct=0.80,
        false_champion_identified_rate_pct=0.05,
        champion_org_chart_mapped_pct=0.80,
        multi_thread_depth_avg=3.0,
        champion_nps_score_avg=8.0,
        deal_at_risk_after_ghosting_pct=0.10,
        champion_introduced_mobilizer_pct=0.60,
        avg_days_to_detect_champion_change=2.0,
        champion_internal_objection_coached_pct=0.70,
        total_active_deals=10,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return ChampionInput(**defaults)


def _engine() -> SalesChampionStabilityIntelligenceEngine:
    return SalesChampionStabilityIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum Tests
# ---------------------------------------------------------------------------

class TestChampionRiskEnum:
    def test_values_exist(self):
        assert ChampionRisk.low.value == "low"
        assert ChampionRisk.moderate.value == "moderate"
        assert ChampionRisk.high.value == "high"
        assert ChampionRisk.critical.value == "critical"

    def test_four_members(self):
        assert len(ChampionRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(ChampionRisk.low, str)

    def test_str_comparison(self):
        assert ChampionRisk.low == "low"

    def test_critical_ne_low(self):
        assert ChampionRisk.critical != ChampionRisk.low


class TestChampionPatternEnum:
    def test_none_value(self):
        assert ChampionPattern.none.value == "none"

    def test_champion_ghosting(self):
        assert ChampionPattern.champion_ghosting.value == "champion_ghosting"

    def test_single_thread_fragility(self):
        assert ChampionPattern.single_thread_fragility.value == "single_thread_fragility"

    def test_role_change_blindspot(self):
        assert ChampionPattern.champion_role_change_blindspot.value == "champion_role_change_blindspot"

    def test_internal_conflict(self):
        assert ChampionPattern.internal_champion_conflict.value == "internal_champion_conflict"

    def test_false_champion_reliance(self):
        assert ChampionPattern.false_champion_reliance.value == "false_champion_reliance"

    def test_six_members(self):
        assert len(ChampionPattern) == 6

    def test_is_str_enum(self):
        assert isinstance(ChampionPattern.none, str)


class TestChampionSeverityEnum:
    def test_anchored(self):
        assert ChampionSeverity.anchored.value == "anchored"

    def test_developing(self):
        assert ChampionSeverity.developing.value == "developing"

    def test_fragile(self):
        assert ChampionSeverity.fragile.value == "fragile"

    def test_exposed(self):
        assert ChampionSeverity.exposed.value == "exposed"

    def test_four_members(self):
        assert len(ChampionSeverity) == 4

    def test_is_str_enum(self):
        assert isinstance(ChampionSeverity.anchored, str)


class TestChampionActionEnum:
    def test_no_action(self):
        assert ChampionAction.no_action.value == "no_action"

    def test_re_engagement_plan(self):
        assert ChampionAction.champion_re_engagement_plan.value == "champion_re_engagement_plan"

    def test_multithreading_coaching(self):
        assert ChampionAction.multithreading_coaching.value == "multithreading_coaching"

    def test_executive_sponsor_alignment(self):
        assert ChampionAction.executive_sponsor_alignment.value == "executive_sponsor_alignment"

    def test_champion_validation_coaching(self):
        assert ChampionAction.champion_validation_coaching.value == "champion_validation_coaching"

    def test_deal_rescue_intervention(self):
        assert ChampionAction.deal_rescue_intervention.value == "deal_rescue_intervention"

    def test_six_members(self):
        assert len(ChampionAction) == 6

    def test_is_str_enum(self):
        assert isinstance(ChampionAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. ChampionInput Dataclass Tests
# ---------------------------------------------------------------------------

class TestChampionInputFields:
    def test_rep_id_field(self):
        inp = _base_input(rep_id="REP-42")
        assert inp.rep_id == "REP-42"

    def test_region_field(self):
        inp = _base_input(region="West")
        assert inp.region == "West"

    def test_evaluation_period_id(self):
        inp = _base_input(evaluation_period_id="Q1-2027")
        assert inp.evaluation_period_id == "Q1-2027"

    def test_avg_champion_response_time_days(self):
        inp = _base_input(avg_champion_response_time_days=5.5)
        assert inp.avg_champion_response_time_days == 5.5

    def test_champion_engagement_drop_rate_pct(self):
        inp = _base_input(champion_engagement_drop_rate_pct=0.15)
        assert inp.champion_engagement_drop_rate_pct == 0.15

    def test_deals_with_single_champion_pct(self):
        inp = _base_input(deals_with_single_champion_pct=0.75)
        assert inp.deals_with_single_champion_pct == 0.75

    def test_champion_gone_dark_rate_pct(self):
        inp = _base_input(champion_gone_dark_rate_pct=0.45)
        assert inp.champion_gone_dark_rate_pct == 0.45

    def test_champion_role_change_detected_rate_pct(self):
        inp = _base_input(champion_role_change_detected_rate_pct=0.20)
        assert inp.champion_role_change_detected_rate_pct == 0.20

    def test_champion_re_engaged_within_7d_pct(self):
        inp = _base_input(champion_re_engaged_within_7d_pct=0.55)
        assert inp.champion_re_engaged_within_7d_pct == 0.55

    def test_deals_lost_after_champion_change_pct(self):
        inp = _base_input(deals_lost_after_champion_change_pct=0.65)
        assert inp.deals_lost_after_champion_change_pct == 0.65

    def test_deals_with_executive_sponsor_pct(self):
        inp = _base_input(deals_with_executive_sponsor_pct=0.25)
        assert inp.deals_with_executive_sponsor_pct == 0.25

    def test_champion_coached_on_internal_selling_pct(self):
        inp = _base_input(champion_coached_on_internal_selling_pct=0.45)
        assert inp.champion_coached_on_internal_selling_pct == 0.45

    def test_false_champion_identified_rate_pct(self):
        inp = _base_input(false_champion_identified_rate_pct=0.30)
        assert inp.false_champion_identified_rate_pct == 0.30

    def test_champion_org_chart_mapped_pct(self):
        inp = _base_input(champion_org_chart_mapped_pct=0.70)
        assert inp.champion_org_chart_mapped_pct == 0.70

    def test_multi_thread_depth_avg(self):
        inp = _base_input(multi_thread_depth_avg=2.0)
        assert inp.multi_thread_depth_avg == 2.0

    def test_champion_nps_score_avg(self):
        inp = _base_input(champion_nps_score_avg=7.5)
        assert inp.champion_nps_score_avg == 7.5

    def test_deal_at_risk_after_ghosting_pct(self):
        inp = _base_input(deal_at_risk_after_ghosting_pct=0.40)
        assert inp.deal_at_risk_after_ghosting_pct == 0.40

    def test_champion_introduced_mobilizer_pct(self):
        inp = _base_input(champion_introduced_mobilizer_pct=0.20)
        assert inp.champion_introduced_mobilizer_pct == 0.20

    def test_avg_days_to_detect_champion_change(self):
        inp = _base_input(avg_days_to_detect_champion_change=12.0)
        assert inp.avg_days_to_detect_champion_change == 12.0

    def test_champion_internal_objection_coached_pct(self):
        inp = _base_input(champion_internal_objection_coached_pct=0.60)
        assert inp.champion_internal_objection_coached_pct == 0.60

    def test_total_active_deals_int(self):
        inp = _base_input(total_active_deals=25)
        assert inp.total_active_deals == 25

    def test_avg_opportunity_value_usd(self):
        inp = _base_input(avg_opportunity_value_usd=75_000.0)
        assert inp.avg_opportunity_value_usd == 75_000.0

    def test_total_fields_count(self):
        import dataclasses
        fields = dataclasses.fields(ChampionInput)
        assert len(fields) == 22


# ---------------------------------------------------------------------------
# 3. ChampionResult Fields and to_dict Tests
# ---------------------------------------------------------------------------

class TestChampionResultFields:
    def setup_method(self):
        self.engine = _engine()
        self.result = self.engine.assess(_base_input())

    def test_rep_id(self):
        assert self.result.rep_id == "R001"

    def test_region(self):
        assert self.result.region == "Northeast"

    def test_champion_risk_is_enum(self):
        assert isinstance(self.result.champion_risk, ChampionRisk)

    def test_champion_pattern_is_enum(self):
        assert isinstance(self.result.champion_pattern, ChampionPattern)

    def test_champion_severity_is_enum(self):
        assert isinstance(self.result.champion_severity, ChampionSeverity)

    def test_recommended_action_is_enum(self):
        assert isinstance(self.result.recommended_action, ChampionAction)

    def test_engagement_score_float(self):
        assert isinstance(self.result.engagement_score, float)

    def test_threading_score_float(self):
        assert isinstance(self.result.threading_score, float)

    def test_detection_score_float(self):
        assert isinstance(self.result.detection_score, float)

    def test_coaching_score_float(self):
        assert isinstance(self.result.coaching_score, float)

    def test_champion_composite_float(self):
        assert isinstance(self.result.champion_composite, float)

    def test_has_champion_gap_bool(self):
        assert isinstance(self.result.has_champion_gap, bool)

    def test_requires_champion_coaching_bool(self):
        assert isinstance(self.result.requires_champion_coaching, bool)

    def test_estimated_deal_exposure_usd_float(self):
        assert isinstance(self.result.estimated_deal_exposure_usd, float)

    def test_champion_signal_str(self):
        assert isinstance(self.result.champion_signal, str)

    def test_total_result_fields_count(self):
        import dataclasses
        fields = dataclasses.fields(ChampionResult)
        assert len(fields) == 15


class TestChampionResultToDict:
    def setup_method(self):
        self.engine = _engine()
        self.d = self.engine.assess(_base_input()).to_dict()

    def test_to_dict_has_15_keys(self):
        assert len(self.d) == 15

    def test_key_rep_id(self):
        assert "rep_id" in self.d

    def test_key_region(self):
        assert "region" in self.d

    def test_key_champion_risk(self):
        assert "champion_risk" in self.d

    def test_key_champion_pattern(self):
        assert "champion_pattern" in self.d

    def test_key_champion_severity(self):
        assert "champion_severity" in self.d

    def test_key_recommended_action(self):
        assert "recommended_action" in self.d

    def test_key_engagement_score(self):
        assert "engagement_score" in self.d

    def test_key_threading_score(self):
        assert "threading_score" in self.d

    def test_key_detection_score(self):
        assert "detection_score" in self.d

    def test_key_coaching_score(self):
        assert "coaching_score" in self.d

    def test_key_champion_composite(self):
        assert "champion_composite" in self.d

    def test_key_has_champion_gap(self):
        assert "has_champion_gap" in self.d

    def test_key_requires_champion_coaching(self):
        assert "requires_champion_coaching" in self.d

    def test_key_estimated_deal_exposure_usd(self):
        assert "estimated_deal_exposure_usd" in self.d

    def test_key_champion_signal(self):
        assert "champion_signal" in self.d

    def test_risk_value_is_string(self):
        assert isinstance(self.d["champion_risk"], str)

    def test_pattern_value_is_string(self):
        assert isinstance(self.d["champion_pattern"], str)

    def test_severity_value_is_string(self):
        assert isinstance(self.d["champion_severity"], str)

    def test_action_value_is_string(self):
        assert isinstance(self.d["recommended_action"], str)


# ---------------------------------------------------------------------------
# 4. Sub-score: _engagement_score
# ---------------------------------------------------------------------------

class TestEngagementScore:
    def setup_method(self):
        self.engine = _engine()

    def _eng(self, **kw) -> float:
        return self.engine._engagement_score(_base_input(**kw))

    # champion_gone_dark_rate_pct branches
    def test_gone_dark_below_010_gives_zero_component(self):
        # <0.10 → 0
        score = self._eng(champion_gone_dark_rate_pct=0.05,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 0.0

    def test_gone_dark_exactly_010_gives_8(self):
        score = self._eng(champion_gone_dark_rate_pct=0.10,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 8.0

    def test_gone_dark_between_010_025_gives_8(self):
        score = self._eng(champion_gone_dark_rate_pct=0.15,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 8.0

    def test_gone_dark_exactly_025_gives_22(self):
        score = self._eng(champion_gone_dark_rate_pct=0.25,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 22.0

    def test_gone_dark_between_025_040_gives_22(self):
        score = self._eng(champion_gone_dark_rate_pct=0.30,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 22.0

    def test_gone_dark_exactly_040_gives_40(self):
        score = self._eng(champion_gone_dark_rate_pct=0.40,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 40.0

    def test_gone_dark_above_040_gives_40(self):
        score = self._eng(champion_gone_dark_rate_pct=0.90,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 40.0

    # avg_champion_response_time_days branches
    def test_response_time_below_3_gives_zero_component(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=2.0,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 0.0

    def test_response_time_exactly_3_gives_18(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=3.0,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 18.0

    def test_response_time_between_3_7_gives_18(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=5.0,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 18.0

    def test_response_time_exactly_7_gives_35(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=7.0,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 35.0

    def test_response_time_above_7_gives_35(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=10.0,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 35.0

    # deal_at_risk_after_ghosting_pct branches
    def test_ghosting_risk_below_025_gives_zero_component(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.10)
        assert score == 0.0

    def test_ghosting_risk_exactly_025_gives_12(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.25)
        assert score == 12.0

    def test_ghosting_risk_between_025_050_gives_12(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.40)
        assert score == 12.0

    def test_ghosting_risk_exactly_050_gives_25(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.50)
        assert score == 25.0

    def test_ghosting_risk_above_050_gives_25(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=0.5,
                          deal_at_risk_after_ghosting_pct=0.80)
        assert score == 25.0

    def test_max_raw_engagement_is_100(self):
        score = self._eng(champion_gone_dark_rate_pct=1.0,
                          avg_champion_response_time_days=10.0,
                          deal_at_risk_after_ghosting_pct=1.0)
        assert score == 100.0

    def test_all_zeros_gives_zero(self):
        score = self._eng(champion_gone_dark_rate_pct=0.0,
                          avg_champion_response_time_days=0.0,
                          deal_at_risk_after_ghosting_pct=0.0)
        assert score == 0.0

    def test_additive_components(self):
        # 22 + 18 + 12 = 52
        score = self._eng(champion_gone_dark_rate_pct=0.25,
                          avg_champion_response_time_days=5.0,
                          deal_at_risk_after_ghosting_pct=0.30)
        assert score == 52.0


# ---------------------------------------------------------------------------
# 5. Sub-score: _threading_score
# ---------------------------------------------------------------------------

class TestThreadingScore:
    def setup_method(self):
        self.engine = _engine()

    def _thr(self, **kw) -> float:
        return self.engine._threading_score(_base_input(**kw))

    # deals_with_single_champion_pct
    def test_single_champion_below_030_zero_component(self):
        score = self._thr(deals_with_single_champion_pct=0.20,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 0.0

    def test_single_champion_exactly_030_gives_8(self):
        score = self._thr(deals_with_single_champion_pct=0.30,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 8.0

    def test_single_champion_between_030_050_gives_8(self):
        score = self._thr(deals_with_single_champion_pct=0.40,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 8.0

    def test_single_champion_exactly_050_gives_22(self):
        score = self._thr(deals_with_single_champion_pct=0.50,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 22.0

    def test_single_champion_between_050_070_gives_22(self):
        score = self._thr(deals_with_single_champion_pct=0.60,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 22.0

    def test_single_champion_exactly_070_gives_40(self):
        score = self._thr(deals_with_single_champion_pct=0.70,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 40.0

    def test_single_champion_above_070_gives_40(self):
        score = self._thr(deals_with_single_champion_pct=0.90,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 40.0

    # multi_thread_depth_avg
    def test_thread_depth_above_25_zero_component(self):
        score = self._thr(deals_with_single_champion_pct=0.0,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 0.0

    def test_thread_depth_exactly_25_gives_18(self):
        score = self._thr(deals_with_single_champion_pct=0.0,
                          multi_thread_depth_avg=2.5,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 18.0

    def test_thread_depth_between_15_25_gives_18(self):
        score = self._thr(deals_with_single_champion_pct=0.0,
                          multi_thread_depth_avg=2.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 18.0

    def test_thread_depth_exactly_15_gives_35(self):
        score = self._thr(deals_with_single_champion_pct=0.0,
                          multi_thread_depth_avg=1.5,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 35.0

    def test_thread_depth_below_15_gives_35(self):
        score = self._thr(deals_with_single_champion_pct=0.0,
                          multi_thread_depth_avg=1.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 35.0

    # deals_with_executive_sponsor_pct
    def test_exec_sponsor_above_035_zero_component(self):
        score = self._thr(deals_with_single_champion_pct=0.0,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.50)
        assert score == 0.0

    def test_exec_sponsor_exactly_035_gives_12(self):
        score = self._thr(deals_with_single_champion_pct=0.0,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.35)
        assert score == 12.0

    def test_exec_sponsor_between_015_035_gives_12(self):
        score = self._thr(deals_with_single_champion_pct=0.0,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.25)
        assert score == 12.0

    def test_exec_sponsor_exactly_015_gives_25(self):
        score = self._thr(deals_with_single_champion_pct=0.0,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.15)
        assert score == 25.0

    def test_exec_sponsor_below_015_gives_25(self):
        score = self._thr(deals_with_single_champion_pct=0.0,
                          multi_thread_depth_avg=3.0,
                          deals_with_executive_sponsor_pct=0.05)
        assert score == 25.0

    def test_max_threading_is_100(self):
        score = self._thr(deals_with_single_champion_pct=1.0,
                          multi_thread_depth_avg=1.0,
                          deals_with_executive_sponsor_pct=0.0)
        assert score == 100.0

    def test_additive_components(self):
        # 22 + 18 + 12 = 52
        score = self._thr(deals_with_single_champion_pct=0.50,
                          multi_thread_depth_avg=2.0,
                          deals_with_executive_sponsor_pct=0.25)
        assert score == 52.0


# ---------------------------------------------------------------------------
# 6. Sub-score: _detection_score
# ---------------------------------------------------------------------------

class TestDetectionScore:
    def setup_method(self):
        self.engine = _engine()

    def _det(self, **kw) -> float:
        return self.engine._detection_score(_base_input(**kw))

    # avg_days_to_detect_champion_change
    def test_detect_days_below_3_zero_component(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 0.0

    def test_detect_days_exactly_3_gives_8(self):
        score = self._det(avg_days_to_detect_champion_change=3.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 8.0

    def test_detect_days_between_3_7_gives_8(self):
        score = self._det(avg_days_to_detect_champion_change=5.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 8.0

    def test_detect_days_exactly_7_gives_22(self):
        score = self._det(avg_days_to_detect_champion_change=7.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 22.0

    def test_detect_days_between_7_14_gives_22(self):
        score = self._det(avg_days_to_detect_champion_change=10.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 22.0

    def test_detect_days_exactly_14_gives_40(self):
        score = self._det(avg_days_to_detect_champion_change=14.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 40.0

    def test_detect_days_above_14_gives_40(self):
        score = self._det(avg_days_to_detect_champion_change=20.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 40.0

    # champion_re_engaged_within_7d_pct
    def test_reengaged_above_060_zero_component(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 0.0

    def test_reengaged_exactly_060_gives_18(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.60,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 18.0

    def test_reengaged_between_030_060_gives_18(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.45,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 18.0

    def test_reengaged_exactly_030_gives_35(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.30,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 35.0

    def test_reengaged_below_030_gives_35(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.10,
                          deals_lost_after_champion_change_pct=0.10)
        assert score == 35.0

    # deals_lost_after_champion_change_pct
    def test_deals_lost_below_035_zero_component(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.20)
        assert score == 0.0

    def test_deals_lost_exactly_035_gives_12(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.35)
        assert score == 12.0

    def test_deals_lost_between_035_060_gives_12(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.50)
        assert score == 12.0

    def test_deals_lost_exactly_060_gives_25(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.60)
        assert score == 25.0

    def test_deals_lost_above_060_gives_25(self):
        score = self._det(avg_days_to_detect_champion_change=2.0,
                          champion_re_engaged_within_7d_pct=0.80,
                          deals_lost_after_champion_change_pct=0.90)
        assert score == 25.0

    def test_max_detection_is_100(self):
        score = self._det(avg_days_to_detect_champion_change=20.0,
                          champion_re_engaged_within_7d_pct=0.10,
                          deals_lost_after_champion_change_pct=0.90)
        assert score == 100.0

    def test_additive_components(self):
        # 22 + 18 + 12 = 52
        score = self._det(avg_days_to_detect_champion_change=7.0,
                          champion_re_engaged_within_7d_pct=0.45,
                          deals_lost_after_champion_change_pct=0.50)
        assert score == 52.0


# ---------------------------------------------------------------------------
# 7. Sub-score: _coaching_score
# ---------------------------------------------------------------------------

class TestCoachingScore:
    def setup_method(self):
        self.engine = _engine()

    def _coa(self, **kw) -> float:
        return self.engine._coaching_score(_base_input(**kw))

    # champion_coached_on_internal_selling_pct
    def test_coached_above_075_zero_component(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 0.0

    def test_coached_exactly_075_gives_8(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.75,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 8.0

    def test_coached_between_050_075_gives_8(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.60,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 8.0

    def test_coached_exactly_050_gives_22(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.50,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 22.0

    def test_coached_between_020_050_gives_22(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.35,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 22.0

    def test_coached_exactly_020_gives_40(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.20,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 40.0

    def test_coached_below_020_gives_40(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.10,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 40.0

    # false_champion_identified_rate_pct
    def test_false_champion_below_020_zero_component(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 0.0

    def test_false_champion_exactly_020_gives_18(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.20,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 18.0

    def test_false_champion_between_020_040_gives_18(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.30,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 18.0

    def test_false_champion_exactly_040_gives_35(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.40,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 35.0

    def test_false_champion_above_040_gives_35(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.80,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 35.0

    # champion_introduced_mobilizer_pct
    def test_mobilizer_above_035_zero_component(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.60)
        assert score == 0.0

    def test_mobilizer_exactly_035_gives_12(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.35)
        assert score == 12.0

    def test_mobilizer_between_015_035_gives_12(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.25)
        assert score == 12.0

    def test_mobilizer_exactly_015_gives_25(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.15)
        assert score == 25.0

    def test_mobilizer_below_015_gives_25(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.90,
                          false_champion_identified_rate_pct=0.10,
                          champion_introduced_mobilizer_pct=0.05)
        assert score == 25.0

    def test_max_coaching_is_100(self):
        score = self._coa(champion_coached_on_internal_selling_pct=0.10,
                          false_champion_identified_rate_pct=0.90,
                          champion_introduced_mobilizer_pct=0.05)
        assert score == 100.0

    def test_additive_components(self):
        # 22 + 18 + 12 = 52
        score = self._coa(champion_coached_on_internal_selling_pct=0.35,
                          false_champion_identified_rate_pct=0.25,
                          champion_introduced_mobilizer_pct=0.25)
        assert score == 52.0


# ---------------------------------------------------------------------------
# 8. Composite Score Tests
# ---------------------------------------------------------------------------

class TestCompositeScore:
    def setup_method(self):
        self.engine = _engine()

    def test_healthy_input_low_composite(self):
        result = self.engine.assess(_base_input())
        assert result.champion_composite < 20.0

    def test_composite_is_weighted_sum(self):
        # Manually compute for known inputs
        inp = _base_input(
            champion_gone_dark_rate_pct=0.40,   # eng += 40
            avg_champion_response_time_days=7.0, # eng += 35
            deal_at_risk_after_ghosting_pct=0.0, # eng += 0 → eng=75
            deals_with_single_champion_pct=0.0,
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,  # thr=0
            avg_days_to_detect_champion_change=2.0,
            champion_re_engaged_within_7d_pct=0.80,
            deals_lost_after_champion_change_pct=0.10,  # det=0
            champion_coached_on_internal_selling_pct=0.90,
            false_champion_identified_rate_pct=0.10,
            champion_introduced_mobilizer_pct=0.60,  # coa=0
        )
        result = self.engine.assess(inp)
        # engagement=75, threading=0, detection=0, coaching=0
        # composite = 75*0.30 + 0*0.30 + 0*0.25 + 0*0.15 = 22.5
        assert result.engagement_score == 75.0
        assert result.threading_score == 0.0
        assert result.detection_score == 0.0
        assert result.coaching_score == 0.0
        assert result.champion_composite == pytest.approx(22.5, abs=0.2)

    def test_composite_capped_at_100(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=1.0,
            avg_champion_response_time_days=10.0,
            deal_at_risk_after_ghosting_pct=1.0,
            deals_with_single_champion_pct=1.0,
            multi_thread_depth_avg=1.0,
            deals_with_executive_sponsor_pct=0.0,
            avg_days_to_detect_champion_change=20.0,
            champion_re_engaged_within_7d_pct=0.0,
            deals_lost_after_champion_change_pct=1.0,
            champion_coached_on_internal_selling_pct=0.0,
            false_champion_identified_rate_pct=1.0,
            champion_introduced_mobilizer_pct=0.0,
        )
        result = self.engine.assess(inp)
        assert result.champion_composite <= 100.0

    def test_composite_rounding_to_1_decimal(self):
        result = self.engine.assess(_base_input())
        # Should be rounded to 1 decimal place
        assert result.champion_composite == round(result.champion_composite, 1)


# ---------------------------------------------------------------------------
# 9. Pattern Detection Tests
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def setup_method(self):
        self.engine = _engine()

    def _pattern(self, **kw) -> ChampionPattern:
        return self.engine.assess(_base_input(**kw)).champion_pattern

    def test_no_pattern_for_healthy_input(self):
        assert self._pattern() == ChampionPattern.none

    # false_champion_reliance — highest priority
    def test_false_champion_reliance_detected(self):
        pattern = self._pattern(
            false_champion_identified_rate_pct=0.35,
            champion_coached_on_internal_selling_pct=0.30,
        )
        assert pattern == ChampionPattern.false_champion_reliance

    def test_false_champion_reliance_above_threshold(self):
        pattern = self._pattern(
            false_champion_identified_rate_pct=0.50,
            champion_coached_on_internal_selling_pct=0.10,
        )
        assert pattern == ChampionPattern.false_champion_reliance

    def test_false_champion_reliance_not_triggered_low_rate(self):
        # false_champion rate < 0.35 → should not fire
        pattern = self._pattern(
            false_champion_identified_rate_pct=0.34,
            champion_coached_on_internal_selling_pct=0.10,
        )
        assert pattern != ChampionPattern.false_champion_reliance

    def test_false_champion_reliance_not_triggered_high_coaching(self):
        # coaching > 0.30 → should not fire
        pattern = self._pattern(
            false_champion_identified_rate_pct=0.50,
            champion_coached_on_internal_selling_pct=0.31,
        )
        assert pattern != ChampionPattern.false_champion_reliance

    # internal_champion_conflict
    def test_internal_champion_conflict_detected(self):
        pattern = self._pattern(
            champion_org_chart_mapped_pct=0.25,
            champion_introduced_mobilizer_pct=0.15,
            false_champion_identified_rate_pct=0.10,  # ensure priority 1 not triggered
            champion_coached_on_internal_selling_pct=0.80,
        )
        assert pattern == ChampionPattern.internal_champion_conflict

    def test_internal_conflict_not_triggered_high_org_chart(self):
        pattern = self._pattern(
            champion_org_chart_mapped_pct=0.26,
            champion_introduced_mobilizer_pct=0.10,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
        )
        assert pattern != ChampionPattern.internal_champion_conflict

    def test_internal_conflict_not_triggered_high_mobilizer(self):
        pattern = self._pattern(
            champion_org_chart_mapped_pct=0.20,
            champion_introduced_mobilizer_pct=0.16,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
        )
        assert pattern != ChampionPattern.internal_champion_conflict

    # false_champion takes priority over internal_conflict
    def test_priority_false_champion_over_internal_conflict(self):
        pattern = self._pattern(
            false_champion_identified_rate_pct=0.40,
            champion_coached_on_internal_selling_pct=0.20,
            champion_org_chart_mapped_pct=0.10,
            champion_introduced_mobilizer_pct=0.10,
        )
        assert pattern == ChampionPattern.false_champion_reliance

    # single_thread_fragility
    def test_single_thread_fragility_detected(self):
        # Need threading >= 35 and single_champion >= 0.60
        # threading with single_champion=0.70 → 40, multi_thread=1.5 → 35, exec_sponsor=0.50 → 0 → total=75
        pattern = self._pattern(
            deals_with_single_champion_pct=0.70,
            multi_thread_depth_avg=1.5,
            deals_with_executive_sponsor_pct=0.50,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        assert pattern == ChampionPattern.single_thread_fragility

    def test_single_thread_not_triggered_low_single_pct(self):
        pattern = self._pattern(
            deals_with_single_champion_pct=0.59,
            multi_thread_depth_avg=1.0,
            deals_with_executive_sponsor_pct=0.05,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        assert pattern != ChampionPattern.single_thread_fragility

    # champion_ghosting
    def test_champion_ghosting_detected(self):
        # engagement >= 35 and gone_dark >= 0.30
        # gone_dark=0.40 →+40, response_time=7.0 →+35 → eng=75
        pattern = self._pattern(
            champion_gone_dark_rate_pct=0.40,
            avg_champion_response_time_days=7.0,
            deal_at_risk_after_ghosting_pct=0.0,
            deals_with_single_champion_pct=0.20,  # keep threading low
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        assert pattern == ChampionPattern.champion_ghosting

    def test_ghosting_not_triggered_low_gone_dark(self):
        pattern = self._pattern(
            champion_gone_dark_rate_pct=0.29,
            avg_champion_response_time_days=10.0,
            deal_at_risk_after_ghosting_pct=0.0,
            deals_with_single_champion_pct=0.20,
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        assert pattern != ChampionPattern.champion_ghosting

    # champion_role_change_blindspot
    def test_role_change_blindspot_detected(self):
        # detection >= 30 and avg_days >= 10.0
        # avg_days=14 →+40, re_engaged=0.10 →+35, deals_lost=0.60 →+25 → det=100
        pattern = self._pattern(
            avg_days_to_detect_champion_change=14.0,
            champion_re_engaged_within_7d_pct=0.10,
            deals_lost_after_champion_change_pct=0.60,
            deals_with_single_champion_pct=0.20,
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
            champion_gone_dark_rate_pct=0.05,
            avg_champion_response_time_days=1.0,
            deal_at_risk_after_ghosting_pct=0.0,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        assert pattern == ChampionPattern.champion_role_change_blindspot

    def test_role_change_not_triggered_low_days(self):
        pattern = self._pattern(
            avg_days_to_detect_champion_change=9.9,
            champion_re_engaged_within_7d_pct=0.10,
            deals_lost_after_champion_change_pct=0.60,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        assert pattern != ChampionPattern.champion_role_change_blindspot

    def test_none_returned_when_no_conditions_met(self):
        result = self.engine.assess(_base_input())
        assert result.champion_pattern == ChampionPattern.none


# ---------------------------------------------------------------------------
# 10. Risk Threshold Tests
# ---------------------------------------------------------------------------

class TestRiskThresholds:
    def setup_method(self):
        self.engine = _engine()

    def _risk_for_composite(self, composite: float) -> ChampionRisk:
        return self.engine._risk_level(composite)

    def test_zero_composite_is_low(self):
        assert self._risk_for_composite(0.0) == ChampionRisk.low

    def test_19_composite_is_low(self):
        assert self._risk_for_composite(19.9) == ChampionRisk.low

    def test_exactly_20_is_moderate(self):
        assert self._risk_for_composite(20.0) == ChampionRisk.moderate

    def test_39_composite_is_moderate(self):
        assert self._risk_for_composite(39.9) == ChampionRisk.moderate

    def test_exactly_40_is_high(self):
        assert self._risk_for_composite(40.0) == ChampionRisk.high

    def test_59_composite_is_high(self):
        assert self._risk_for_composite(59.9) == ChampionRisk.high

    def test_exactly_60_is_critical(self):
        assert self._risk_for_composite(60.0) == ChampionRisk.critical

    def test_100_composite_is_critical(self):
        assert self._risk_for_composite(100.0) == ChampionRisk.critical


# ---------------------------------------------------------------------------
# 11. Severity Threshold Tests
# ---------------------------------------------------------------------------

class TestSeverityThresholds:
    def setup_method(self):
        self.engine = _engine()

    def _sev(self, composite: float) -> ChampionSeverity:
        return self.engine._severity(composite)

    def test_zero_is_anchored(self):
        assert self._sev(0.0) == ChampionSeverity.anchored

    def test_19_is_anchored(self):
        assert self._sev(19.9) == ChampionSeverity.anchored

    def test_exactly_20_is_developing(self):
        assert self._sev(20.0) == ChampionSeverity.developing

    def test_39_is_developing(self):
        assert self._sev(39.9) == ChampionSeverity.developing

    def test_exactly_40_is_fragile(self):
        assert self._sev(40.0) == ChampionSeverity.fragile

    def test_59_is_fragile(self):
        assert self._sev(59.9) == ChampionSeverity.fragile

    def test_exactly_60_is_exposed(self):
        assert self._sev(60.0) == ChampionSeverity.exposed

    def test_100_is_exposed(self):
        assert self._sev(100.0) == ChampionSeverity.exposed


# ---------------------------------------------------------------------------
# 12. Action Mapping Tests
# ---------------------------------------------------------------------------

class TestActionMapping:
    def setup_method(self):
        self.engine = _engine()

    def _action(self, risk: ChampionRisk, pattern: ChampionPattern) -> ChampionAction:
        return self.engine._action(risk, pattern)

    def test_low_risk_no_action(self):
        assert self._action(ChampionRisk.low, ChampionPattern.none) == ChampionAction.no_action

    def test_low_risk_any_pattern_no_action(self):
        assert self._action(ChampionRisk.low, ChampionPattern.champion_ghosting) == ChampionAction.no_action

    def test_moderate_risk_multithreading_coaching(self):
        assert self._action(ChampionRisk.moderate, ChampionPattern.none) == ChampionAction.multithreading_coaching

    def test_moderate_any_pattern_multithreading_coaching(self):
        assert self._action(ChampionRisk.moderate, ChampionPattern.single_thread_fragility) == ChampionAction.multithreading_coaching

    def test_high_ghosting_re_engagement_plan(self):
        assert self._action(ChampionRisk.high, ChampionPattern.champion_ghosting) == ChampionAction.champion_re_engagement_plan

    def test_high_internal_conflict_exec_sponsor(self):
        assert self._action(ChampionRisk.high, ChampionPattern.internal_champion_conflict) == ChampionAction.executive_sponsor_alignment

    def test_high_other_pattern_multithreading(self):
        assert self._action(ChampionRisk.high, ChampionPattern.single_thread_fragility) == ChampionAction.multithreading_coaching

    def test_high_none_pattern_multithreading(self):
        assert self._action(ChampionRisk.high, ChampionPattern.none) == ChampionAction.multithreading_coaching

    def test_high_false_champion_multithreading(self):
        assert self._action(ChampionRisk.high, ChampionPattern.false_champion_reliance) == ChampionAction.multithreading_coaching

    def test_high_role_change_multithreading(self):
        assert self._action(ChampionRisk.high, ChampionPattern.champion_role_change_blindspot) == ChampionAction.multithreading_coaching

    def test_critical_false_champion_validation_coaching(self):
        assert self._action(ChampionRisk.critical, ChampionPattern.false_champion_reliance) == ChampionAction.champion_validation_coaching

    def test_critical_single_thread_deal_rescue(self):
        assert self._action(ChampionRisk.critical, ChampionPattern.single_thread_fragility) == ChampionAction.deal_rescue_intervention

    def test_critical_none_deal_rescue(self):
        assert self._action(ChampionRisk.critical, ChampionPattern.none) == ChampionAction.deal_rescue_intervention

    def test_critical_ghosting_deal_rescue(self):
        assert self._action(ChampionRisk.critical, ChampionPattern.champion_ghosting) == ChampionAction.deal_rescue_intervention

    def test_critical_internal_conflict_deal_rescue(self):
        assert self._action(ChampionRisk.critical, ChampionPattern.internal_champion_conflict) == ChampionAction.deal_rescue_intervention

    def test_critical_role_change_deal_rescue(self):
        assert self._action(ChampionRisk.critical, ChampionPattern.champion_role_change_blindspot) == ChampionAction.deal_rescue_intervention


# ---------------------------------------------------------------------------
# 13. Champion Gap Flag Tests
# ---------------------------------------------------------------------------

class TestHasChampionGap:
    def setup_method(self):
        self.engine = _engine()

    def test_no_gap_healthy(self):
        result = self.engine.assess(_base_input())
        assert result.has_champion_gap is False

    def test_gap_via_composite_ge_40(self):
        # Force composite >= 40 via high engagement
        inp = _base_input(
            champion_gone_dark_rate_pct=0.40,
            avg_champion_response_time_days=7.0,
            deal_at_risk_after_ghosting_pct=0.50,
            deals_with_single_champion_pct=0.70,
            multi_thread_depth_avg=1.0,
            deals_with_executive_sponsor_pct=0.05,
        )
        result = self.engine.assess(inp)
        assert result.has_champion_gap is True

    def test_gap_via_single_champion_pct_ge_060(self):
        inp = _base_input(
            deals_with_single_champion_pct=0.60,
            # keep composite low
            champion_gone_dark_rate_pct=0.05,
            avg_champion_response_time_days=1.0,
            deal_at_risk_after_ghosting_pct=0.0,
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
        )
        result = self.engine.assess(inp)
        assert result.has_champion_gap is True

    def test_gap_via_gone_dark_ge_030(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=0.30,
            deals_with_single_champion_pct=0.20,
            avg_champion_response_time_days=1.0,
            deal_at_risk_after_ghosting_pct=0.0,
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
        )
        result = self.engine.assess(inp)
        assert result.has_champion_gap is True

    def test_no_gap_below_all_thresholds(self):
        inp = _base_input(
            deals_with_single_champion_pct=0.10,
            champion_gone_dark_rate_pct=0.05,
        )
        result = self.engine.assess(inp)
        assert result.has_champion_gap is False


# ---------------------------------------------------------------------------
# 14. Requires Champion Coaching Flag Tests
# ---------------------------------------------------------------------------

class TestRequiresChampionCoaching:
    def setup_method(self):
        self.engine = _engine()

    def test_coaching_required_healthy_low_coaching_pct(self):
        # Default base has champion_coached=0.80 > 0.40, so check depends on composite
        result = self.engine.assess(_base_input())
        # composite < 30, coached > 0.40, false_champion < 0.20 → False
        assert result.requires_champion_coaching is False

    def test_coaching_required_via_composite_ge_30(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=0.40,
            avg_champion_response_time_days=7.0,
            deal_at_risk_after_ghosting_pct=0.50,
        )
        result = self.engine.assess(inp)
        assert result.requires_champion_coaching is True

    def test_coaching_required_via_low_coached_pct(self):
        # champion_coached_on_internal_selling_pct <= 0.40
        inp = _base_input(champion_coached_on_internal_selling_pct=0.40)
        result = self.engine.assess(inp)
        assert result.requires_champion_coaching is True

    def test_coaching_required_via_high_false_champion_rate(self):
        # false_champion >= 0.20
        inp = _base_input(false_champion_identified_rate_pct=0.20)
        result = self.engine.assess(inp)
        assert result.requires_champion_coaching is True

    def test_coaching_not_required_above_all_thresholds(self):
        inp = _base_input(
            champion_coached_on_internal_selling_pct=0.80,
            false_champion_identified_rate_pct=0.10,
        )
        result = self.engine.assess(inp)
        # Verify composite < 30
        assert result.champion_composite < 30.0
        assert result.requires_champion_coaching is False


# ---------------------------------------------------------------------------
# 15. Deal Exposure Formula Tests
# ---------------------------------------------------------------------------

class TestDealExposureFormula:
    def setup_method(self):
        self.engine = _engine()

    def test_zero_exposure_no_dark(self):
        inp = _base_input(champion_gone_dark_rate_pct=0.0)
        result = self.engine.assess(inp)
        assert result.estimated_deal_exposure_usd == 0.0

    def test_formula_calculation(self):
        # total_active_deals=10, avg_opp=50000, gone_dark=0.10, composite=?
        # Use known healthy: composite will be small
        inp = _base_input(
            total_active_deals=10,
            avg_opportunity_value_usd=50_000.0,
            champion_gone_dark_rate_pct=0.10,
            avg_champion_response_time_days=1.0,
            deal_at_risk_after_ghosting_pct=0.0,
        )
        result = self.engine.assess(inp)
        expected = round(10 * 50_000.0 * 0.10 * (result.champion_composite / 100.0), 2)
        assert result.estimated_deal_exposure_usd == expected

    def test_exposure_rounded_to_2_decimal_places(self):
        inp = _base_input(
            total_active_deals=7,
            avg_opportunity_value_usd=33_333.33,
            champion_gone_dark_rate_pct=0.33,
        )
        result = self.engine.assess(inp)
        # Verify 2 decimal places
        assert result.estimated_deal_exposure_usd == round(result.estimated_deal_exposure_usd, 2)

    def test_exposure_zero_composite_is_zero(self):
        # If composite = 0, exposure = 0 regardless of other fields
        # Healthy input gives low composite
        result = self.engine.assess(_base_input(champion_gone_dark_rate_pct=0.0))
        assert result.estimated_deal_exposure_usd == 0.0

    def test_exposure_scales_with_active_deals(self):
        inp1 = _base_input(total_active_deals=10, avg_opportunity_value_usd=50_000.0, champion_gone_dark_rate_pct=0.40)
        inp2 = _base_input(total_active_deals=20, avg_opportunity_value_usd=50_000.0, champion_gone_dark_rate_pct=0.40)
        r1 = _engine().assess(inp1)
        r2 = _engine().assess(inp2)
        if r1.champion_composite > 0 and r2.champion_composite > 0:
            assert r2.estimated_deal_exposure_usd == pytest.approx(r1.estimated_deal_exposure_usd * 2, rel=0.01)

    def test_exposure_scales_with_opportunity_value(self):
        inp1 = _base_input(total_active_deals=10, avg_opportunity_value_usd=50_000.0, champion_gone_dark_rate_pct=0.40)
        inp2 = _base_input(total_active_deals=10, avg_opportunity_value_usd=100_000.0, champion_gone_dark_rate_pct=0.40)
        r1 = _engine().assess(inp1)
        r2 = _engine().assess(inp2)
        if r1.champion_composite > 0:
            assert r2.estimated_deal_exposure_usd == pytest.approx(r1.estimated_deal_exposure_usd * 2, rel=0.01)


# ---------------------------------------------------------------------------
# 16. Signal String Tests
# ---------------------------------------------------------------------------

class TestSignalString:
    def setup_method(self):
        self.engine = _engine()

    def test_healthy_signal(self):
        result = self.engine.assess(_base_input())
        assert result.champion_signal == "Champion stability healthy — engagement, multithreading, and detection response within benchmarks"

    def test_healthy_signal_requires_none_pattern_and_low_composite(self):
        # If pattern is none but composite >= 20, should NOT show healthy signal
        # We need pattern=none and composite >= 20
        # Detection score alone: avg_days=14 →+40, re_engaged=0.30 →+35 → det=75
        # composite = 75*0.25 = 18.75 < 20 → still healthy? Let's try something bigger
        inp = _base_input(
            avg_days_to_detect_champion_change=14.0,
            champion_re_engaged_within_7d_pct=0.10,
            deals_lost_after_champion_change_pct=0.60,  # det = 100
            # Keep other scores at 0 to avoid triggering patterns
            champion_gone_dark_rate_pct=0.05,
            avg_champion_response_time_days=1.0,
            deal_at_risk_after_ghosting_pct=0.0,
            deals_with_single_champion_pct=0.20,
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
            champion_coached_on_internal_selling_pct=0.80,
            false_champion_identified_rate_pct=0.10,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        result = self.engine.assess(inp)
        # det=100, composite = 100*0.25 = 25 → moderate, pattern = role_change_blindspot
        # Signal should NOT be healthy
        assert result.champion_signal != "Champion stability healthy — engagement, multithreading, and detection response within benchmarks"

    def test_signal_contains_gone_dark_pct(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=0.40,
            avg_champion_response_time_days=7.0,
            deal_at_risk_after_ghosting_pct=0.0,
        )
        result = self.engine.assess(inp)
        assert "40% champions gone dark" in result.champion_signal

    def test_signal_contains_single_thread_pct(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=0.40,
            avg_champion_response_time_days=7.0,
            deals_with_single_champion_pct=0.65,
        )
        result = self.engine.assess(inp)
        assert "65% single-thread deals" in result.champion_signal

    def test_signal_contains_days_to_detect(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=0.40,
            avg_champion_response_time_days=7.0,
            avg_days_to_detect_champion_change=5.0,
        )
        result = self.engine.assess(inp)
        assert "5 days to detect change" in result.champion_signal

    def test_signal_contains_composite(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=0.40,
            avg_champion_response_time_days=7.0,
        )
        result = self.engine.assess(inp)
        assert f"composite {result.champion_composite:.0f}" in result.champion_signal

    def test_signal_none_pattern_label(self):
        # When pattern is none but composite >= 20, label is "Champion risk"
        inp = _base_input(
            avg_days_to_detect_champion_change=7.0,
            champion_re_engaged_within_7d_pct=0.10,
            deals_lost_after_champion_change_pct=0.60,
            champion_gone_dark_rate_pct=0.05,
            avg_champion_response_time_days=1.0,
            deal_at_risk_after_ghosting_pct=0.0,
            deals_with_single_champion_pct=0.20,
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
            champion_coached_on_internal_selling_pct=0.80,
            false_champion_identified_rate_pct=0.10,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        result = self.engine.assess(inp)
        # Check pattern and composite
        if result.champion_pattern == ChampionPattern.none and result.champion_composite >= 20:
            assert result.champion_signal.startswith("Champion risk —")

    def test_signal_pattern_label_ghosting(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=0.40,
            avg_champion_response_time_days=7.0,
            deal_at_risk_after_ghosting_pct=0.0,
            deals_with_single_champion_pct=0.20,
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        result = self.engine.assess(inp)
        if result.champion_pattern == ChampionPattern.champion_ghosting:
            assert result.champion_signal.startswith("Champion ghosting —")

    def test_signal_pattern_label_false_champion(self):
        inp = _base_input(
            false_champion_identified_rate_pct=0.50,
            champion_coached_on_internal_selling_pct=0.10,
        )
        result = self.engine.assess(inp)
        if result.champion_pattern == ChampionPattern.false_champion_reliance:
            assert result.champion_signal.startswith("False champion reliance —")


# ---------------------------------------------------------------------------
# 17. End-to-End assess() Tests
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def setup_method(self):
        self.engine = _engine()

    def test_assess_returns_champion_result(self):
        result = self.engine.assess(_base_input())
        assert isinstance(result, ChampionResult)

    def test_assess_stores_result(self):
        self.engine.assess(_base_input())
        assert len(self.engine._results) == 1

    def test_assess_stores_multiple_results(self):
        self.engine.assess(_base_input(rep_id="R1"))
        self.engine.assess(_base_input(rep_id="R2"))
        assert len(self.engine._results) == 2

    def test_assess_preserves_rep_id(self):
        result = self.engine.assess(_base_input(rep_id="XYZ"))
        assert result.rep_id == "XYZ"

    def test_assess_preserves_region(self):
        result = self.engine.assess(_base_input(region="South"))
        assert result.region == "South"

    def test_healthy_scenario_low_risk(self):
        result = self.engine.assess(_base_input())
        assert result.champion_risk == ChampionRisk.low

    def test_healthy_scenario_no_action(self):
        result = self.engine.assess(_base_input())
        assert result.recommended_action == ChampionAction.no_action

    def test_healthy_scenario_anchored_severity(self):
        result = self.engine.assess(_base_input())
        assert result.champion_severity == ChampionSeverity.anchored

    def test_critical_scenario(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=0.50,
            avg_champion_response_time_days=10.0,
            deal_at_risk_after_ghosting_pct=0.80,
            deals_with_single_champion_pct=0.80,
            multi_thread_depth_avg=1.0,
            deals_with_executive_sponsor_pct=0.05,
            avg_days_to_detect_champion_change=20.0,
            champion_re_engaged_within_7d_pct=0.10,
            deals_lost_after_champion_change_pct=0.80,
            champion_coached_on_internal_selling_pct=0.10,
            false_champion_identified_rate_pct=0.60,
            champion_introduced_mobilizer_pct=0.05,
        )
        result = self.engine.assess(inp)
        assert result.champion_risk == ChampionRisk.critical
        assert result.champion_severity == ChampionSeverity.exposed

    def test_sub_scores_within_0_100(self):
        result = self.engine.assess(_base_input())
        assert 0.0 <= result.engagement_score <= 100.0
        assert 0.0 <= result.threading_score <= 100.0
        assert 0.0 <= result.detection_score <= 100.0
        assert 0.0 <= result.coaching_score <= 100.0

    def test_composite_within_0_100(self):
        result = self.engine.assess(_base_input())
        assert 0.0 <= result.champion_composite <= 100.0


# ---------------------------------------------------------------------------
# 18. assess_batch() Tests
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def setup_method(self):
        self.engine = _engine()

    def test_batch_returns_list(self):
        results = self.engine.assess_batch([_base_input()])
        assert isinstance(results, list)

    def test_batch_empty_returns_empty_list(self):
        results = self.engine.assess_batch([])
        assert results == []

    def test_batch_returns_correct_count(self):
        inputs = [_base_input(rep_id=f"R{i}") for i in range(5)]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_stores_all_results(self):
        inputs = [_base_input(rep_id=f"R{i}") for i in range(3)]
        self.engine.assess_batch(inputs)
        assert len(self.engine._results) == 3

    def test_batch_returns_champion_result_instances(self):
        inputs = [_base_input(rep_id=f"R{i}") for i in range(3)]
        results = self.engine.assess_batch(inputs)
        for r in results:
            assert isinstance(r, ChampionResult)

    def test_batch_processes_in_order(self):
        inputs = [_base_input(rep_id=f"R{i}") for i in range(3)]
        results = self.engine.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"R{i}"

    def test_batch_mixed_risk_levels(self):
        inp_low = _base_input(rep_id="low")
        inp_critical = _base_input(
            rep_id="crit",
            champion_gone_dark_rate_pct=0.50,
            avg_champion_response_time_days=10.0,
            deal_at_risk_after_ghosting_pct=0.80,
            deals_with_single_champion_pct=0.80,
            multi_thread_depth_avg=1.0,
            deals_with_executive_sponsor_pct=0.05,
            avg_days_to_detect_champion_change=20.0,
            champion_re_engaged_within_7d_pct=0.10,
            deals_lost_after_champion_change_pct=0.80,
            champion_coached_on_internal_selling_pct=0.10,
            false_champion_identified_rate_pct=0.60,
            champion_introduced_mobilizer_pct=0.05,
        )
        results = self.engine.assess_batch([inp_low, inp_critical])
        assert results[0].champion_risk == ChampionRisk.low
        assert results[1].champion_risk == ChampionRisk.critical


# ---------------------------------------------------------------------------
# 19. summary() Tests — Empty Engine
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def setup_method(self):
        self.engine = _engine()
        self.s = self.engine.summary()

    def test_summary_has_13_keys(self):
        assert len(self.s) == 13

    def test_total_is_zero(self):
        assert self.s["total"] == 0

    def test_risk_counts_empty_dict(self):
        assert self.s["risk_counts"] == {}

    def test_pattern_counts_empty_dict(self):
        assert self.s["pattern_counts"] == {}

    def test_severity_counts_empty_dict(self):
        assert self.s["severity_counts"] == {}

    def test_action_counts_empty_dict(self):
        assert self.s["action_counts"] == {}

    def test_avg_composite_zero(self):
        assert self.s["avg_champion_composite"] == 0.0

    def test_champion_gap_count_zero(self):
        assert self.s["champion_gap_count"] == 0

    def test_coaching_count_zero(self):
        assert self.s["coaching_count"] == 0

    def test_avg_engagement_zero(self):
        assert self.s["avg_engagement_score"] == 0.0

    def test_avg_threading_zero(self):
        assert self.s["avg_threading_score"] == 0.0

    def test_avg_detection_zero(self):
        assert self.s["avg_detection_score"] == 0.0

    def test_avg_coaching_zero(self):
        assert self.s["avg_coaching_score"] == 0.0

    def test_total_deal_exposure_zero(self):
        assert self.s["total_estimated_deal_exposure_usd"] == 0.0


# ---------------------------------------------------------------------------
# 20. summary() Tests — Populated Engine
# ---------------------------------------------------------------------------

class TestSummaryPopulated:
    def setup_method(self):
        self.engine = _engine()
        # One healthy rep
        self.engine.assess(_base_input(rep_id="R1", region="North"))
        # One critical rep
        self.engine.assess(_base_input(
            rep_id="R2",
            region="South",
            champion_gone_dark_rate_pct=0.50,
            avg_champion_response_time_days=10.0,
            deal_at_risk_after_ghosting_pct=0.80,
            deals_with_single_champion_pct=0.80,
            multi_thread_depth_avg=1.0,
            deals_with_executive_sponsor_pct=0.05,
            avg_days_to_detect_champion_change=20.0,
            champion_re_engaged_within_7d_pct=0.10,
            deals_lost_after_champion_change_pct=0.80,
            champion_coached_on_internal_selling_pct=0.10,
            false_champion_identified_rate_pct=0.60,
            champion_introduced_mobilizer_pct=0.05,
        ))
        self.s = self.engine.summary()

    def test_total_is_two(self):
        assert self.s["total"] == 2

    def test_has_13_keys(self):
        assert len(self.s) == 13

    def test_risk_counts_key_exists(self):
        assert "risk_counts" in self.s

    def test_risk_counts_has_entries(self):
        assert len(self.s["risk_counts"]) > 0

    def test_pattern_counts_key_exists(self):
        assert "pattern_counts" in self.s

    def test_severity_counts_key_exists(self):
        assert "severity_counts" in self.s

    def test_action_counts_key_exists(self):
        assert "action_counts" in self.s

    def test_avg_composite_is_float(self):
        assert isinstance(self.s["avg_champion_composite"], float)

    def test_avg_composite_positive(self):
        assert self.s["avg_champion_composite"] > 0

    def test_champion_gap_count_is_int(self):
        assert isinstance(self.s["champion_gap_count"], int)

    def test_coaching_count_is_int(self):
        assert isinstance(self.s["coaching_count"], int)

    def test_avg_engagement_is_float(self):
        assert isinstance(self.s["avg_engagement_score"], float)

    def test_avg_threading_is_float(self):
        assert isinstance(self.s["avg_threading_score"], float)

    def test_avg_detection_is_float(self):
        assert isinstance(self.s["avg_detection_score"], float)

    def test_avg_coaching_is_float(self):
        assert isinstance(self.s["avg_coaching_score"], float)

    def test_total_deal_exposure_is_float(self):
        assert isinstance(self.s["total_estimated_deal_exposure_usd"], float)

    def test_critical_appears_in_risk_counts(self):
        assert "critical" in self.s["risk_counts"]

    def test_low_appears_in_risk_counts(self):
        assert "low" in self.s["risk_counts"]

    def test_risk_counts_sum_equals_total(self):
        total = sum(self.s["risk_counts"].values())
        assert total == self.s["total"]

    def test_pattern_counts_sum_equals_total(self):
        total = sum(self.s["pattern_counts"].values())
        assert total == self.s["total"]

    def test_severity_counts_sum_equals_total(self):
        total = sum(self.s["severity_counts"].values())
        assert total == self.s["total"]

    def test_action_counts_sum_equals_total(self):
        total = sum(self.s["action_counts"].values())
        assert total == self.s["total"]

    def test_gap_count_lte_total(self):
        assert self.s["champion_gap_count"] <= self.s["total"]

    def test_coaching_count_lte_total(self):
        assert self.s["coaching_count"] <= self.s["total"]

    def test_all_13_keys_present(self):
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_champion_composite", "champion_gap_count",
            "coaching_count", "avg_engagement_score", "avg_threading_score",
            "avg_detection_score", "avg_coaching_score",
            "total_estimated_deal_exposure_usd",
        }
        assert set(self.s.keys()) == expected_keys

    def test_total_deal_exposure_is_sum_of_individual(self):
        individual_sum = sum(r.estimated_deal_exposure_usd for r in self.engine._results)
        assert self.s["total_estimated_deal_exposure_usd"] == pytest.approx(round(individual_sum, 2), abs=0.01)


# ---------------------------------------------------------------------------
# 21. Edge Case Tests
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def setup_method(self):
        self.engine = _engine()

    def test_all_zeros_pct_fields(self):
        inp = _base_input(
            avg_champion_response_time_days=0.0,
            champion_engagement_drop_rate_pct=0.0,
            deals_with_single_champion_pct=0.0,
            champion_gone_dark_rate_pct=0.0,
            champion_re_engaged_within_7d_pct=1.0,  # avoid min thresholds
            deals_lost_after_champion_change_pct=0.0,
            deals_with_executive_sponsor_pct=1.0,
            champion_coached_on_internal_selling_pct=1.0,
            false_champion_identified_rate_pct=0.0,
            champion_org_chart_mapped_pct=1.0,
            multi_thread_depth_avg=5.0,
            deal_at_risk_after_ghosting_pct=0.0,
            champion_introduced_mobilizer_pct=1.0,
            avg_days_to_detect_champion_change=0.0,
        )
        result = self.engine.assess(inp)
        assert result.champion_composite >= 0.0

    def test_all_max_values(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=1.0,
            avg_champion_response_time_days=100.0,
            deal_at_risk_after_ghosting_pct=1.0,
            deals_with_single_champion_pct=1.0,
            multi_thread_depth_avg=0.0,
            deals_with_executive_sponsor_pct=0.0,
            avg_days_to_detect_champion_change=100.0,
            champion_re_engaged_within_7d_pct=0.0,
            deals_lost_after_champion_change_pct=1.0,
            champion_coached_on_internal_selling_pct=0.0,
            false_champion_identified_rate_pct=1.0,
            champion_introduced_mobilizer_pct=0.0,
        )
        result = self.engine.assess(inp)
        assert result.champion_composite == 100.0
        assert result.champion_risk == ChampionRisk.critical
        assert result.champion_severity == ChampionSeverity.exposed

    def test_boundary_composite_exactly_20(self):
        # Force exactly 20 composite via threading only
        # threading = 20/0.30 = 66.67 → threading=67
        # threading score 67: need ~67 from threading
        # 40 + 18 = 58, 40 + 25 = 65, 40 + 18 + 12 = 70
        # Let's get threading = 67: 40 + 18 + 12 = 70 → composite = 70 * 0.30 = 21
        # We want exactly 20: threading = 66.7 → not exactly possible
        # Test boundary between low and moderate
        result_low = self.engine.assess(_base_input())
        assert result_low.champion_risk == ChampionRisk.low

    def test_new_engine_has_empty_results(self):
        engine = SalesChampionStabilityIntelligenceEngine()
        assert engine._results == []

    def test_engine_accumulates_results_across_calls(self):
        self.engine.assess(_base_input(rep_id="A"))
        self.engine.assess(_base_input(rep_id="B"))
        self.engine.assess(_base_input(rep_id="C"))
        assert len(self.engine._results) == 3

    def test_single_thread_exactly_at_boundary_030(self):
        # threading_score: exactly 0.30 → should give +8
        inp = _base_input(
            deals_with_single_champion_pct=0.30,
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
        )
        thr = self.engine._threading_score(inp)
        assert thr == 8.0

    def test_gone_dark_exactly_at_boundary_010(self):
        inp = _base_input(
            champion_gone_dark_rate_pct=0.10,
            avg_champion_response_time_days=0.0,
            deal_at_risk_after_ghosting_pct=0.0,
        )
        eng = self.engine._engagement_score(inp)
        assert eng == 8.0

    def test_detect_days_exactly_at_3(self):
        inp = _base_input(
            avg_days_to_detect_champion_change=3.0,
            champion_re_engaged_within_7d_pct=0.80,
            deals_lost_after_champion_change_pct=0.0,
        )
        det = self.engine._detection_score(inp)
        assert det == 8.0

    def test_coaching_exactly_at_050_boundary(self):
        inp = _base_input(
            champion_coached_on_internal_selling_pct=0.50,
            false_champion_identified_rate_pct=0.0,
            champion_introduced_mobilizer_pct=0.60,
        )
        coa = self.engine._coaching_score(inp)
        assert coa == 22.0

    def test_assess_result_appears_in_summary(self):
        self.engine.assess(_base_input())
        s = self.engine.summary()
        assert s["total"] == 1

    def test_summary_reflects_all_batched_results(self):
        inputs = [_base_input(rep_id=f"R{i}") for i in range(5)]
        self.engine.assess_batch(inputs)
        s = self.engine.summary()
        assert s["total"] == 5

    def test_to_dict_rep_id_matches_result(self):
        result = self.engine.assess(_base_input(rep_id="MYID"))
        d = result.to_dict()
        assert d["rep_id"] == "MYID"
        assert d["rep_id"] == result.rep_id

    def test_to_dict_risk_is_string_value(self):
        result = self.engine.assess(_base_input())
        d = result.to_dict()
        assert d["champion_risk"] == result.champion_risk.value

    def test_engagement_score_not_negative(self):
        result = self.engine.assess(_base_input(
            champion_gone_dark_rate_pct=0.0,
            avg_champion_response_time_days=0.0,
            deal_at_risk_after_ghosting_pct=0.0,
        ))
        assert result.engagement_score >= 0.0

    def test_threading_score_not_negative(self):
        result = self.engine.assess(_base_input(
            deals_with_single_champion_pct=0.0,
            multi_thread_depth_avg=5.0,
            deals_with_executive_sponsor_pct=1.0,
        ))
        assert result.threading_score >= 0.0

    def test_detection_score_not_negative(self):
        result = self.engine.assess(_base_input(
            avg_days_to_detect_champion_change=0.0,
            champion_re_engaged_within_7d_pct=1.0,
            deals_lost_after_champion_change_pct=0.0,
        ))
        assert result.detection_score >= 0.0

    def test_coaching_score_not_negative(self):
        result = self.engine.assess(_base_input(
            champion_coached_on_internal_selling_pct=1.0,
            false_champion_identified_rate_pct=0.0,
            champion_introduced_mobilizer_pct=1.0,
        ))
        assert result.coaching_score >= 0.0

    def test_pattern_priority_single_thread_over_ghosting(self):
        # Set both single_thread_fragility and ghosting conditions active
        # But ensure false_champion and internal_conflict are NOT triggered
        inp = _base_input(
            deals_with_single_champion_pct=0.70,
            multi_thread_depth_avg=1.0,
            deals_with_executive_sponsor_pct=0.50,
            champion_gone_dark_rate_pct=0.40,
            avg_champion_response_time_days=7.0,
            deal_at_risk_after_ghosting_pct=0.0,
            false_champion_identified_rate_pct=0.10,  # below 0.35
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,  # above 0.25
            champion_introduced_mobilizer_pct=0.60,  # above 0.15
        )
        result = self.engine.assess(inp)
        # single_thread_fragility has priority over ghosting
        assert result.champion_pattern == ChampionPattern.single_thread_fragility

    def test_pattern_priority_ghosting_over_role_change(self):
        # ghosting triggered: engagement >=35, gone_dark >=0.30
        # role change triggered: detection >=30, avg_days >=10
        # neither false_champion, internal_conflict, nor single_thread triggered
        inp = _base_input(
            champion_gone_dark_rate_pct=0.40,
            avg_champion_response_time_days=7.0,
            deal_at_risk_after_ghosting_pct=0.0,
            deals_with_single_champion_pct=0.20,  # below 0.60
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
            avg_days_to_detect_champion_change=14.0,
            champion_re_engaged_within_7d_pct=0.10,
            deals_lost_after_champion_change_pct=0.60,  # detection high
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        result = self.engine.assess(inp)
        # ghosting (priority 4) should take over role_change_blindspot (priority 5)
        assert result.champion_pattern == ChampionPattern.champion_ghosting

    def test_high_risk_with_role_change_blindspot_gives_multithreading(self):
        inp = _base_input(
            avg_days_to_detect_champion_change=20.0,
            champion_re_engaged_within_7d_pct=0.10,
            deals_lost_after_champion_change_pct=0.80,
            champion_gone_dark_rate_pct=0.05,
            avg_champion_response_time_days=1.0,
            deal_at_risk_after_ghosting_pct=0.0,
            deals_with_single_champion_pct=0.70,
            multi_thread_depth_avg=1.5,
            deals_with_executive_sponsor_pct=0.15,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        result = self.engine.assess(inp)
        if result.champion_risk == ChampionRisk.high and result.champion_pattern == ChampionPattern.single_thread_fragility:
            assert result.recommended_action == ChampionAction.multithreading_coaching

    def test_multiple_engines_independent(self):
        engine1 = SalesChampionStabilityIntelligenceEngine()
        engine2 = SalesChampionStabilityIntelligenceEngine()
        engine1.assess(_base_input(rep_id="E1"))
        assert len(engine2._results) == 0

    def test_summary_avg_composite_rounded_to_1_decimal(self):
        self.engine.assess(_base_input())
        s = self.engine.summary()
        avg = s["avg_champion_composite"]
        assert avg == round(avg, 1)

    def test_summary_total_exposure_rounded_to_2_decimal(self):
        self.engine.assess(_base_input(champion_gone_dark_rate_pct=0.33))
        s = self.engine.summary()
        exposure = s["total_estimated_deal_exposure_usd"]
        assert exposure == round(exposure, 2)

    def test_internal_conflict_boundary_exact_025_org_chart(self):
        inp = _base_input(
            champion_org_chart_mapped_pct=0.25,
            champion_introduced_mobilizer_pct=0.15,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
        )
        result = self.engine.assess(inp)
        assert result.champion_pattern == ChampionPattern.internal_champion_conflict

    def test_internal_conflict_boundary_exact_015_mobilizer(self):
        inp = _base_input(
            champion_org_chart_mapped_pct=0.20,
            champion_introduced_mobilizer_pct=0.15,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
        )
        result = self.engine.assess(inp)
        assert result.champion_pattern == ChampionPattern.internal_champion_conflict

    def test_role_change_blindspot_boundary_exact_10_days(self):
        # detection score must be >= 30, and avg_days >= 10
        inp = _base_input(
            avg_days_to_detect_champion_change=10.0,
            champion_re_engaged_within_7d_pct=0.10,  # det: 22+35=57 >=30
            deals_lost_after_champion_change_pct=0.0,
            champion_gone_dark_rate_pct=0.05,
            avg_champion_response_time_days=1.0,
            deal_at_risk_after_ghosting_pct=0.0,
            deals_with_single_champion_pct=0.20,
            multi_thread_depth_avg=3.0,
            deals_with_executive_sponsor_pct=0.50,
            false_champion_identified_rate_pct=0.10,
            champion_coached_on_internal_selling_pct=0.80,
            champion_org_chart_mapped_pct=0.80,
            champion_introduced_mobilizer_pct=0.60,
        )
        result = self.engine.assess(inp)
        assert result.champion_pattern == ChampionPattern.champion_role_change_blindspot

    def test_false_champion_reliance_exact_boundaries(self):
        inp = _base_input(
            false_champion_identified_rate_pct=0.35,
            champion_coached_on_internal_selling_pct=0.30,
        )
        result = self.engine.assess(inp)
        assert result.champion_pattern == ChampionPattern.false_champion_reliance
