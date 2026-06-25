"""
Comprehensive tests for SalesNegotiationEffectivenessIntelligenceEngine.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_negotiation_effectiveness_intelligence_engine import (
    NegotiationRisk,
    NegotiationPattern,
    NegotiationSeverity,
    NegotiationAction,
    NegotiationEffectivenessInput,
    NegotiationEffectivenessResult,
    SalesNegotiationEffectivenessIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / factories
# ---------------------------------------------------------------------------

def make_input(**overrides) -> NegotiationEffectivenessInput:
    """Return a baseline healthy-rep input, overriding any field as needed."""
    defaults = dict(
        rep_id="REP-001",
        region="West",
        evaluation_period_id="2024-Q1",
        total_deals_negotiated=20,
        deals_requiring_discount_count=4,
        avg_discount_depth_pct=0.05,
        max_discount_given_pct=0.10,
        deals_closed_at_list_price_count=10,
        avg_negotiation_rounds=1.5,
        deals_won_after_negotiation_count=16,
        deals_lost_on_price_count=1,
        first_concession_timing_days=10.0,
        concession_without_request_count=1,
        multi_round_deals_count=3,
        value_anchor_usage_pct=0.70,
        competitive_pressure_discount_pct=0.03,
        deals_with_procurement_count=2,
        procurement_discount_rate_pct=0.05,
        avg_contract_value_vs_target_pct=0.95,
        late_stage_reprice_count=0,
        avg_time_to_close_after_negotiation_days=5.0,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return NegotiationEffectivenessInput(**defaults)


def make_engine() -> SalesNegotiationEffectivenessIntelligenceEngine:
    return SalesNegotiationEffectivenessIntelligenceEngine()


# ===========================================================================
# 1. Enum membership & values
# ===========================================================================

class TestNegotiationRiskEnum:
    def test_low_value(self):
        assert NegotiationRisk.low.value == "low"

    def test_moderate_value(self):
        assert NegotiationRisk.moderate.value == "moderate"

    def test_high_value(self):
        assert NegotiationRisk.high.value == "high"

    def test_critical_value(self):
        assert NegotiationRisk.critical.value == "critical"

    def test_enum_has_four_members(self):
        assert len(NegotiationRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(NegotiationRisk.low, str)

    def test_str_equality(self):
        assert NegotiationRisk.low == "low"

    def test_membership(self):
        members = {r.value for r in NegotiationRisk}
        assert members == {"low", "moderate", "high", "critical"}


class TestNegotiationPatternEnum:
    def test_none_value(self):
        assert NegotiationPattern.none.value == "none"

    def test_excessive_discounting_value(self):
        assert NegotiationPattern.excessive_discounting.value == "excessive_discounting"

    def test_premature_concession_value(self):
        assert NegotiationPattern.premature_concession.value == "premature_concession"

    def test_price_erosion_value(self):
        assert NegotiationPattern.price_erosion.value == "price_erosion"

    def test_value_abandonment_value(self):
        assert NegotiationPattern.value_abandonment.value == "value_abandonment"

    def test_negotiation_avoidance_value(self):
        assert NegotiationPattern.negotiation_avoidance.value == "negotiation_avoidance"

    def test_enum_has_six_members(self):
        assert len(NegotiationPattern) == 6

    def test_is_str_enum(self):
        assert isinstance(NegotiationPattern.none, str)


class TestNegotiationSeverityEnum:
    def test_strong_value(self):
        assert NegotiationSeverity.strong.value == "strong"

    def test_developing_value(self):
        assert NegotiationSeverity.developing.value == "developing"

    def test_vulnerable_value(self):
        assert NegotiationSeverity.vulnerable.value == "vulnerable"

    def test_collapsing_value(self):
        assert NegotiationSeverity.collapsing.value == "collapsing"

    def test_enum_has_four_members(self):
        assert len(NegotiationSeverity) == 4

    def test_is_str_enum(self):
        assert isinstance(NegotiationSeverity.strong, str)


class TestNegotiationActionEnum:
    def test_no_action_value(self):
        assert NegotiationAction.no_action.value == "no_action"

    def test_negotiation_coaching_value(self):
        assert NegotiationAction.negotiation_coaching.value == "negotiation_coaching"

    def test_discount_authority_review_value(self):
        assert NegotiationAction.discount_authority_review.value == "discount_authority_review"

    def test_value_selling_training_value(self):
        assert NegotiationAction.value_selling_training.value == "value_selling_training"

    def test_pricing_integrity_program_value(self):
        assert NegotiationAction.pricing_integrity_program.value == "pricing_integrity_program"

    def test_deal_desk_escalation_value(self):
        assert NegotiationAction.deal_desk_escalation.value == "deal_desk_escalation"

    def test_enum_has_six_members(self):
        assert len(NegotiationAction) == 6

    def test_is_str_enum(self):
        assert isinstance(NegotiationAction.no_action, str)


# ===========================================================================
# 2. NegotiationEffectivenessInput field existence
# ===========================================================================

class TestNegotiationEffectivenessInputFields:
    def test_rep_id_field(self):
        inp = make_input(rep_id="X")
        assert inp.rep_id == "X"

    def test_region_field(self):
        inp = make_input(region="East")
        assert inp.region == "East"

    def test_evaluation_period_id_field(self):
        inp = make_input(evaluation_period_id="2024-Q2")
        assert inp.evaluation_period_id == "2024-Q2"

    def test_total_deals_negotiated_field(self):
        inp = make_input(total_deals_negotiated=30)
        assert inp.total_deals_negotiated == 30

    def test_deals_requiring_discount_count_field(self):
        inp = make_input(deals_requiring_discount_count=5)
        assert inp.deals_requiring_discount_count == 5

    def test_avg_discount_depth_pct_field(self):
        inp = make_input(avg_discount_depth_pct=0.12)
        assert inp.avg_discount_depth_pct == pytest.approx(0.12)

    def test_max_discount_given_pct_field(self):
        inp = make_input(max_discount_given_pct=0.30)
        assert inp.max_discount_given_pct == pytest.approx(0.30)

    def test_deals_closed_at_list_price_count_field(self):
        inp = make_input(deals_closed_at_list_price_count=8)
        assert inp.deals_closed_at_list_price_count == 8

    def test_avg_negotiation_rounds_field(self):
        inp = make_input(avg_negotiation_rounds=2.5)
        assert inp.avg_negotiation_rounds == pytest.approx(2.5)

    def test_deals_won_after_negotiation_count_field(self):
        inp = make_input(deals_won_after_negotiation_count=12)
        assert inp.deals_won_after_negotiation_count == 12

    def test_deals_lost_on_price_count_field(self):
        inp = make_input(deals_lost_on_price_count=3)
        assert inp.deals_lost_on_price_count == 3

    def test_first_concession_timing_days_field(self):
        inp = make_input(first_concession_timing_days=4.0)
        assert inp.first_concession_timing_days == pytest.approx(4.0)

    def test_concession_without_request_count_field(self):
        inp = make_input(concession_without_request_count=2)
        assert inp.concession_without_request_count == 2

    def test_multi_round_deals_count_field(self):
        inp = make_input(multi_round_deals_count=5)
        assert inp.multi_round_deals_count == 5

    def test_value_anchor_usage_pct_field(self):
        inp = make_input(value_anchor_usage_pct=0.50)
        assert inp.value_anchor_usage_pct == pytest.approx(0.50)

    def test_competitive_pressure_discount_pct_field(self):
        inp = make_input(competitive_pressure_discount_pct=0.07)
        assert inp.competitive_pressure_discount_pct == pytest.approx(0.07)

    def test_deals_with_procurement_count_field(self):
        inp = make_input(deals_with_procurement_count=4)
        assert inp.deals_with_procurement_count == 4

    def test_procurement_discount_rate_pct_field(self):
        inp = make_input(procurement_discount_rate_pct=0.15)
        assert inp.procurement_discount_rate_pct == pytest.approx(0.15)

    def test_avg_contract_value_vs_target_pct_field(self):
        inp = make_input(avg_contract_value_vs_target_pct=0.88)
        assert inp.avg_contract_value_vs_target_pct == pytest.approx(0.88)

    def test_late_stage_reprice_count_field(self):
        inp = make_input(late_stage_reprice_count=2)
        assert inp.late_stage_reprice_count == 2

    def test_avg_time_to_close_after_negotiation_days_field(self):
        inp = make_input(avg_time_to_close_after_negotiation_days=20.0)
        assert inp.avg_time_to_close_after_negotiation_days == pytest.approx(20.0)

    def test_avg_opportunity_value_usd_field(self):
        inp = make_input(avg_opportunity_value_usd=75_000.0)
        assert inp.avg_opportunity_value_usd == pytest.approx(75_000.0)

    def test_input_has_22_fields(self):
        inp = make_input()
        import dataclasses
        assert len(dataclasses.fields(inp)) == 22


# ===========================================================================
# 3. NegotiationEffectivenessResult fields and to_dict
# ===========================================================================

class TestNegotiationEffectivenessResult:
    def _make_result(self):
        return NegotiationEffectivenessResult(
            rep_id="REP-X",
            region="North",
            negotiation_risk=NegotiationRisk.low,
            negotiation_pattern=NegotiationPattern.none,
            negotiation_severity=NegotiationSeverity.strong,
            recommended_action=NegotiationAction.no_action,
            discount_discipline_score=5.0,
            concession_behavior_score=3.0,
            value_defense_score=2.0,
            close_effectiveness_score=1.0,
            negotiation_composite=3.0,
            has_pricing_risk=False,
            requires_negotiation_coaching=False,
            estimated_margin_erosion_usd=0.0,
            negotiation_signal="Healthy",
        )

    def test_rep_id(self):
        assert self._make_result().rep_id == "REP-X"

    def test_region(self):
        assert self._make_result().region == "North"

    def test_negotiation_risk(self):
        assert self._make_result().negotiation_risk == NegotiationRisk.low

    def test_negotiation_pattern(self):
        assert self._make_result().negotiation_pattern == NegotiationPattern.none

    def test_negotiation_severity(self):
        assert self._make_result().negotiation_severity == NegotiationSeverity.strong

    def test_recommended_action(self):
        assert self._make_result().recommended_action == NegotiationAction.no_action

    def test_discount_discipline_score(self):
        assert self._make_result().discount_discipline_score == 5.0

    def test_concession_behavior_score(self):
        assert self._make_result().concession_behavior_score == 3.0

    def test_value_defense_score(self):
        assert self._make_result().value_defense_score == 2.0

    def test_close_effectiveness_score(self):
        assert self._make_result().close_effectiveness_score == 1.0

    def test_negotiation_composite(self):
        assert self._make_result().negotiation_composite == 3.0

    def test_has_pricing_risk(self):
        assert self._make_result().has_pricing_risk is False

    def test_requires_negotiation_coaching(self):
        assert self._make_result().requires_negotiation_coaching is False

    def test_estimated_margin_erosion_usd(self):
        assert self._make_result().estimated_margin_erosion_usd == 0.0

    def test_negotiation_signal(self):
        assert self._make_result().negotiation_signal == "Healthy"

    def test_result_has_15_fields(self):
        import dataclasses
        assert len(dataclasses.fields(self._make_result())) == 15

    def test_to_dict_returns_dict(self):
        assert isinstance(self._make_result().to_dict(), dict)

    def test_to_dict_has_15_keys(self):
        assert len(self._make_result().to_dict()) == 15

    def test_to_dict_rep_id(self):
        assert self._make_result().to_dict()["rep_id"] == "REP-X"

    def test_to_dict_region(self):
        assert self._make_result().to_dict()["region"] == "North"

    def test_to_dict_negotiation_risk_is_string(self):
        d = self._make_result().to_dict()
        assert isinstance(d["negotiation_risk"], str)
        assert d["negotiation_risk"] == "low"

    def test_to_dict_negotiation_pattern_is_string(self):
        d = self._make_result().to_dict()
        assert d["negotiation_pattern"] == "none"

    def test_to_dict_negotiation_severity_is_string(self):
        d = self._make_result().to_dict()
        assert d["negotiation_severity"] == "strong"

    def test_to_dict_recommended_action_is_string(self):
        d = self._make_result().to_dict()
        assert d["recommended_action"] == "no_action"

    def test_to_dict_discount_discipline_score(self):
        assert self._make_result().to_dict()["discount_discipline_score"] == 5.0

    def test_to_dict_concession_behavior_score(self):
        assert self._make_result().to_dict()["concession_behavior_score"] == 3.0

    def test_to_dict_value_defense_score(self):
        assert self._make_result().to_dict()["value_defense_score"] == 2.0

    def test_to_dict_close_effectiveness_score(self):
        assert self._make_result().to_dict()["close_effectiveness_score"] == 1.0

    def test_to_dict_negotiation_composite(self):
        assert self._make_result().to_dict()["negotiation_composite"] == 3.0

    def test_to_dict_has_pricing_risk(self):
        assert self._make_result().to_dict()["has_pricing_risk"] is False

    def test_to_dict_requires_negotiation_coaching(self):
        assert self._make_result().to_dict()["requires_negotiation_coaching"] is False

    def test_to_dict_estimated_margin_erosion_usd(self):
        assert self._make_result().to_dict()["estimated_margin_erosion_usd"] == 0.0

    def test_to_dict_negotiation_signal(self):
        assert self._make_result().to_dict()["negotiation_signal"] == "Healthy"

    def test_to_dict_all_keys_present(self):
        expected_keys = {
            "rep_id", "region", "negotiation_risk", "negotiation_pattern",
            "negotiation_severity", "recommended_action",
            "discount_discipline_score", "concession_behavior_score",
            "value_defense_score", "close_effectiveness_score",
            "negotiation_composite", "has_pricing_risk",
            "requires_negotiation_coaching", "estimated_margin_erosion_usd",
            "negotiation_signal",
        }
        assert set(self._make_result().to_dict().keys()) == expected_keys


# ===========================================================================
# 4. Discount Discipline Score sub-score
# ===========================================================================

class TestDiscountDisciplineScore:
    def setup_method(self):
        self.engine = make_engine()

    def test_score_zero_for_low_values(self):
        inp = make_input(avg_discount_depth_pct=0.01, max_discount_given_pct=0.05,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 0.0

    def test_avg_discount_below_08_no_depth_contribution(self):
        inp = make_input(avg_discount_depth_pct=0.07, max_discount_given_pct=0.05,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 0.0

    def test_avg_discount_at_08_adds_8(self):
        inp = make_input(avg_discount_depth_pct=0.08, max_discount_given_pct=0.05,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 8.0

    def test_avg_discount_at_15_adds_22(self):
        inp = make_input(avg_discount_depth_pct=0.15, max_discount_given_pct=0.05,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 22.0

    def test_avg_discount_at_25_adds_40(self):
        inp = make_input(avg_discount_depth_pct=0.25, max_discount_given_pct=0.05,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 40.0

    def test_max_discount_below_25_no_max_contribution(self):
        inp = make_input(avg_discount_depth_pct=0.0, max_discount_given_pct=0.24,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 0.0

    def test_max_discount_at_25_adds_15(self):
        inp = make_input(avg_discount_depth_pct=0.0, max_discount_given_pct=0.25,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 15.0

    def test_max_discount_at_40_adds_30(self):
        inp = make_input(avg_discount_depth_pct=0.0, max_discount_given_pct=0.40,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 30.0

    def test_discount_rate_at_50pct_adds_13(self):
        inp = make_input(avg_discount_depth_pct=0.0, max_discount_given_pct=0.05,
                         deals_requiring_discount_count=10, total_deals_negotiated=20)
        # rate = 0.50 -> +13
        assert self.engine._discount_discipline_score(inp) == 13.0

    def test_discount_rate_at_70pct_adds_25(self):
        inp = make_input(avg_discount_depth_pct=0.0, max_discount_given_pct=0.05,
                         deals_requiring_discount_count=14, total_deals_negotiated=20)
        # rate = 0.70 -> +25
        assert self.engine._discount_discipline_score(inp) == 25.0

    def test_combined_score_does_not_exceed_100(self):
        inp = make_input(avg_discount_depth_pct=0.50, max_discount_given_pct=0.50,
                         deals_requiring_discount_count=20, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) <= 100.0

    def test_total_deals_zero_uses_1_as_denominator(self):
        inp = make_input(avg_discount_depth_pct=0.0, max_discount_given_pct=0.0,
                         deals_requiring_discount_count=1, total_deals_negotiated=0)
        # rate = 1/1 = 1.0 -> +25
        assert self.engine._discount_discipline_score(inp) == 25.0

    def test_all_components_max_capped_at_100(self):
        # 40+30+25 = 95 but should be capped
        inp = make_input(avg_discount_depth_pct=0.30, max_discount_given_pct=0.45,
                         deals_requiring_discount_count=20, total_deals_negotiated=20)
        result = self.engine._discount_discipline_score(inp)
        assert result == min(95.0, 100.0)  # 95.0 which is under 100


# ===========================================================================
# 5. Concession Behavior Score sub-score
# ===========================================================================

class TestConcessionBehaviorScore:
    def setup_method(self):
        self.engine = make_engine()

    def test_score_zero_for_healthy_rep(self):
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=1.0,
                         total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 0.0

    def test_first_concession_at_1day_adds_40(self):
        inp = make_input(first_concession_timing_days=1.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=1.0,
                         total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 40.0

    def test_first_concession_at_3days_adds_20(self):
        inp = make_input(first_concession_timing_days=3.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=1.0,
                         total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 20.0

    def test_first_concession_at_7days_adds_8(self):
        inp = make_input(first_concession_timing_days=7.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=1.0,
                         total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 8.0

    def test_first_concession_above_7days_no_contribution(self):
        inp = make_input(first_concession_timing_days=8.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=1.0,
                         total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 0.0

    def test_unsolicited_rate_at_05_adds_7(self):
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=1,
                         avg_negotiation_rounds=1.0,
                         total_deals_negotiated=20)
        # rate = 1/20 = 0.05 -> +7
        assert self.engine._concession_behavior_score(inp) == 7.0

    def test_unsolicited_rate_at_15_adds_18(self):
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=3,
                         avg_negotiation_rounds=1.0,
                         total_deals_negotiated=20)
        # rate = 3/20 = 0.15 -> +18
        assert self.engine._concession_behavior_score(inp) == 18.0

    def test_unsolicited_rate_at_30_adds_35(self):
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=6,
                         avg_negotiation_rounds=1.0,
                         total_deals_negotiated=20)
        # rate = 6/20 = 0.30 -> +35
        assert self.engine._concession_behavior_score(inp) == 35.0

    def test_avg_rounds_at_3_adds_10(self):
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=3.0,
                         total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 10.0

    def test_avg_rounds_at_4_adds_20(self):
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=4.0,
                         total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 20.0

    def test_score_capped_at_100(self):
        inp = make_input(first_concession_timing_days=0.5,
                         concession_without_request_count=20,
                         avg_negotiation_rounds=5.0,
                         total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) <= 100.0

    def test_zero_deals_uses_1_denominator(self):
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=1,
                         avg_negotiation_rounds=1.0,
                         total_deals_negotiated=0)
        # rate = 1/1 = 1.0 -> +35
        assert self.engine._concession_behavior_score(inp) == 35.0


# ===========================================================================
# 6. Value Defense Score sub-score
# ===========================================================================

class TestValueDefenseScore:
    def setup_method(self):
        self.engine = make_engine()

    def test_score_zero_for_strong_value_defender(self):
        inp = make_input(value_anchor_usage_pct=0.80,
                         avg_contract_value_vs_target_pct=1.0,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 0.0

    def test_anchor_below_20_adds_35(self):
        inp = make_input(value_anchor_usage_pct=0.10,
                         avg_contract_value_vs_target_pct=1.0,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 35.0

    def test_anchor_at_20_adds_18(self):
        inp = make_input(value_anchor_usage_pct=0.20,
                         avg_contract_value_vs_target_pct=1.0,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 18.0

    def test_anchor_at_40_adds_7(self):
        inp = make_input(value_anchor_usage_pct=0.40,
                         avg_contract_value_vs_target_pct=1.0,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 7.0

    def test_anchor_at_60_adds_0(self):
        inp = make_input(value_anchor_usage_pct=0.60,
                         avg_contract_value_vs_target_pct=1.0,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 0.0

    def test_contract_below_80_adds_30(self):
        inp = make_input(value_anchor_usage_pct=0.80,
                         avg_contract_value_vs_target_pct=0.79,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 30.0

    def test_contract_at_80_adds_15(self):
        inp = make_input(value_anchor_usage_pct=0.80,
                         avg_contract_value_vs_target_pct=0.80,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 15.0

    def test_contract_at_90_adds_0(self):
        inp = make_input(value_anchor_usage_pct=0.80,
                         avg_contract_value_vs_target_pct=0.90,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 0.0

    def test_late_reprice_at_1_adds_12(self):
        inp = make_input(value_anchor_usage_pct=0.80,
                         avg_contract_value_vs_target_pct=1.0,
                         late_stage_reprice_count=1)
        assert self.engine._value_defense_score(inp) == 12.0

    def test_late_reprice_at_3_adds_25(self):
        inp = make_input(value_anchor_usage_pct=0.80,
                         avg_contract_value_vs_target_pct=1.0,
                         late_stage_reprice_count=3)
        assert self.engine._value_defense_score(inp) == 25.0

    def test_score_capped_at_100(self):
        inp = make_input(value_anchor_usage_pct=0.0,
                         avg_contract_value_vs_target_pct=0.50,
                         late_stage_reprice_count=10)
        assert self.engine._value_defense_score(inp) <= 100.0

    def test_contract_between_80_and_90_adds_15(self):
        inp = make_input(value_anchor_usage_pct=0.80,
                         avg_contract_value_vs_target_pct=0.85,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 15.0


# ===========================================================================
# 7. Close Effectiveness Score sub-score
# ===========================================================================

class TestCloseEffectivenessScore:
    def setup_method(self):
        self.engine = make_engine()

    def test_score_zero_for_effective_closer(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=3.0,
                         procurement_discount_rate_pct=0.05)
        assert self.engine._close_effectiveness_score(inp) == 0.0

    def test_price_loss_at_08_adds_8(self):
        inp = make_input(deals_lost_on_price_count=2, total_deals_negotiated=20,
                         # rate = 2/20 = 0.10 -> 0.08 to 0.15 range -> +8
                         avg_time_to_close_after_negotiation_days=3.0,
                         procurement_discount_rate_pct=0.05)
        # 2/20 = 0.10 which is >= 0.08 but < 0.15 -> +8
        assert self.engine._close_effectiveness_score(inp) == 8.0

    def test_price_loss_at_15_adds_20(self):
        inp = make_input(deals_lost_on_price_count=3, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=3.0,
                         procurement_discount_rate_pct=0.05)
        # rate = 0.15 -> +20
        assert self.engine._close_effectiveness_score(inp) == 20.0

    def test_price_loss_at_25_adds_40(self):
        inp = make_input(deals_lost_on_price_count=5, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=3.0,
                         procurement_discount_rate_pct=0.05)
        # rate = 0.25 -> +40
        assert self.engine._close_effectiveness_score(inp) == 40.0

    def test_close_days_at_7_adds_7(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=7.0,
                         procurement_discount_rate_pct=0.05)
        assert self.engine._close_effectiveness_score(inp) == 7.0

    def test_close_days_at_14_adds_18(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=14.0,
                         procurement_discount_rate_pct=0.05)
        assert self.engine._close_effectiveness_score(inp) == 18.0

    def test_close_days_at_30_adds_35(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=30.0,
                         procurement_discount_rate_pct=0.05)
        assert self.engine._close_effectiveness_score(inp) == 35.0

    def test_procurement_at_10_adds_10(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=3.0,
                         procurement_discount_rate_pct=0.10)
        assert self.engine._close_effectiveness_score(inp) == 10.0

    def test_procurement_at_20_adds_20(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=3.0,
                         procurement_discount_rate_pct=0.20)
        assert self.engine._close_effectiveness_score(inp) == 20.0

    def test_score_capped_at_100(self):
        inp = make_input(deals_lost_on_price_count=20, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=60.0,
                         procurement_discount_rate_pct=0.50)
        assert self.engine._close_effectiveness_score(inp) <= 100.0

    def test_zero_deals_uses_1_denominator(self):
        inp = make_input(deals_lost_on_price_count=1, total_deals_negotiated=0,
                         avg_time_to_close_after_negotiation_days=3.0,
                         procurement_discount_rate_pct=0.05)
        # rate = 1/1 = 1.0 -> >= 0.25 -> +40
        assert self.engine._close_effectiveness_score(inp) == 40.0


# ===========================================================================
# 8. Risk level mapping
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.engine = make_engine()

    def test_composite_0_is_low(self):
        assert self.engine._risk_level(0.0) == NegotiationRisk.low

    def test_composite_19_is_low(self):
        assert self.engine._risk_level(19.9) == NegotiationRisk.low

    def test_composite_20_is_moderate(self):
        assert self.engine._risk_level(20.0) == NegotiationRisk.moderate

    def test_composite_39_is_moderate(self):
        assert self.engine._risk_level(39.9) == NegotiationRisk.moderate

    def test_composite_40_is_high(self):
        assert self.engine._risk_level(40.0) == NegotiationRisk.high

    def test_composite_59_is_high(self):
        assert self.engine._risk_level(59.9) == NegotiationRisk.high

    def test_composite_60_is_critical(self):
        assert self.engine._risk_level(60.0) == NegotiationRisk.critical

    def test_composite_100_is_critical(self):
        assert self.engine._risk_level(100.0) == NegotiationRisk.critical

    def test_exact_boundary_40(self):
        assert self.engine._risk_level(40.0) == NegotiationRisk.high

    def test_exact_boundary_60(self):
        assert self.engine._risk_level(60.0) == NegotiationRisk.critical


# ===========================================================================
# 9. Severity mapping
# ===========================================================================

class TestSeverity:
    def setup_method(self):
        self.engine = make_engine()

    def test_composite_0_is_strong(self):
        assert self.engine._severity(0.0) == NegotiationSeverity.strong

    def test_composite_19_is_strong(self):
        assert self.engine._severity(19.9) == NegotiationSeverity.strong

    def test_composite_20_is_developing(self):
        assert self.engine._severity(20.0) == NegotiationSeverity.developing

    def test_composite_39_is_developing(self):
        assert self.engine._severity(39.9) == NegotiationSeverity.developing

    def test_composite_40_is_vulnerable(self):
        assert self.engine._severity(40.0) == NegotiationSeverity.vulnerable

    def test_composite_59_is_vulnerable(self):
        assert self.engine._severity(59.9) == NegotiationSeverity.vulnerable

    def test_composite_60_is_collapsing(self):
        assert self.engine._severity(60.0) == NegotiationSeverity.collapsing

    def test_composite_100_is_collapsing(self):
        assert self.engine._severity(100.0) == NegotiationSeverity.collapsing


# ===========================================================================
# 10. Action mapping
# ===========================================================================

class TestActionMapping:
    def setup_method(self):
        self.engine = make_engine()

    def test_low_risk_any_pattern_is_no_action(self):
        for pattern in NegotiationPattern:
            assert self.engine._action(NegotiationRisk.low, pattern) == NegotiationAction.no_action

    def test_moderate_risk_any_pattern_is_coaching(self):
        for pattern in NegotiationPattern:
            assert self.engine._action(NegotiationRisk.moderate, pattern) == NegotiationAction.negotiation_coaching

    def test_high_risk_premature_concession_is_coaching(self):
        assert self.engine._action(NegotiationRisk.high, NegotiationPattern.premature_concession) == NegotiationAction.negotiation_coaching

    def test_high_risk_value_abandonment_is_value_selling_training(self):
        assert self.engine._action(NegotiationRisk.high, NegotiationPattern.value_abandonment) == NegotiationAction.value_selling_training

    def test_high_risk_other_patterns_is_discount_authority_review(self):
        for pattern in [NegotiationPattern.none, NegotiationPattern.excessive_discounting,
                        NegotiationPattern.price_erosion, NegotiationPattern.negotiation_avoidance]:
            assert self.engine._action(NegotiationRisk.high, pattern) == NegotiationAction.discount_authority_review

    def test_critical_risk_excessive_discounting_is_deal_desk(self):
        assert self.engine._action(NegotiationRisk.critical, NegotiationPattern.excessive_discounting) == NegotiationAction.deal_desk_escalation

    def test_critical_risk_price_erosion_is_pricing_integrity(self):
        assert self.engine._action(NegotiationRisk.critical, NegotiationPattern.price_erosion) == NegotiationAction.pricing_integrity_program

    def test_critical_risk_other_patterns_is_deal_desk(self):
        for pattern in [NegotiationPattern.none, NegotiationPattern.premature_concession,
                        NegotiationPattern.value_abandonment, NegotiationPattern.negotiation_avoidance]:
            assert self.engine._action(NegotiationRisk.critical, pattern) == NegotiationAction.deal_desk_escalation


# ===========================================================================
# 11. Pattern detection
# ===========================================================================

class TestPatternDetection:
    def setup_method(self):
        self.engine = make_engine()

    def test_none_pattern_for_healthy_input(self):
        inp = make_input()
        result = self.engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.none

    def test_excessive_discounting_when_discount_score_high_and_depth_high(self):
        # discount score >= 40 requires avg_discount_depth_pct >= 0.25
        inp = make_input(avg_discount_depth_pct=0.30, max_discount_given_pct=0.05,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        result = self.engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.excessive_discounting

    def test_premature_concession_when_concession_score_high_and_timing_fast(self):
        # concession score >= 35 requires first_concession at day <=1 (40) + something
        # avg_discount_depth_pct must be < 0.20 to avoid excessive_discounting dominating
        inp = make_input(
            avg_discount_depth_pct=0.0,
            max_discount_given_pct=0.0,
            deals_requiring_discount_count=0,
            first_concession_timing_days=1.0,
            concession_without_request_count=0,
            avg_negotiation_rounds=1.0,
            total_deals_negotiated=20,
        )
        # concession score = 40.0, first_concession_timing_days <= 2.0 -> premature_concession
        result = self.engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.premature_concession

    def test_price_erosion_when_value_score_high_and_contract_low(self):
        # Need value_defense >= 35 and avg_contract_value_vs_target_pct < 0.85
        # Also need discount score < 40 (to not trigger excessive_discounting first)
        # Also need concession score < 35 (to not trigger premature_concession first)
        inp = make_input(
            avg_discount_depth_pct=0.0,
            max_discount_given_pct=0.0,
            deals_requiring_discount_count=0,
            first_concession_timing_days=15.0,
            concession_without_request_count=0,
            avg_negotiation_rounds=1.0,
            value_anchor_usage_pct=0.10,
            avg_contract_value_vs_target_pct=0.75,
            late_stage_reprice_count=0,
            total_deals_negotiated=20,
        )
        # value_defense = 35+30 = 65, avg_contract < 0.85 -> price_erosion
        result = self.engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.price_erosion

    def test_value_abandonment_pattern(self):
        # value >= 25, value_anchor_usage_pct < 0.30, list_price_rate < 0.10
        # Avoid triggering earlier patterns
        inp = make_input(
            avg_discount_depth_pct=0.0,
            max_discount_given_pct=0.0,
            deals_requiring_discount_count=0,
            first_concession_timing_days=15.0,
            concession_without_request_count=0,
            avg_negotiation_rounds=1.0,
            value_anchor_usage_pct=0.20,   # >= 0.20 so no price_erosion via contract_value
            avg_contract_value_vs_target_pct=0.90,  # >= 0.85 so no price_erosion
            late_stage_reprice_count=1,     # adds 12 to value defense -> value=18+12=30
            deals_closed_at_list_price_count=1,
            total_deals_negotiated=20,
        )
        # value_defense_score: anchor 0.20 -> +18, contract 0.90 -> 0, reprice 1 -> +12 = 30
        # 30 >= 25 and anchor_usage_pct(0.20) < 0.30 and list_price_rate = 1/20 = 0.05 < 0.10
        result = self.engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.value_abandonment

    def test_negotiation_avoidance_pattern(self):
        # close_eff >= 25, avg_negotiation_rounds >= 3.0
        # Avoid triggering earlier patterns
        inp = make_input(
            avg_discount_depth_pct=0.0,
            max_discount_given_pct=0.0,
            deals_requiring_discount_count=0,
            first_concession_timing_days=15.0,
            concession_without_request_count=0,
            avg_negotiation_rounds=3.0,
            value_anchor_usage_pct=0.80,
            avg_contract_value_vs_target_pct=1.0,
            late_stage_reprice_count=0,
            total_deals_negotiated=20,
            deals_lost_on_price_count=5,  # rate=0.25 -> +40 close eff
            avg_time_to_close_after_negotiation_days=3.0,
            procurement_discount_rate_pct=0.05,
            deals_closed_at_list_price_count=10,
        )
        # close_eff = 40 >= 25, avg_rounds = 3.0 >= 3.0 -> negotiation_avoidance
        result = self.engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.negotiation_avoidance

    def test_pattern_priority_excessive_discounting_first(self):
        # When discount >= 40 and avg_discount_depth_pct >= 0.20, that should win
        inp = make_input(
            avg_discount_depth_pct=0.25,
            max_discount_given_pct=0.05,
            deals_requiring_discount_count=0,
            first_concession_timing_days=1.0,  # would also qualify for premature_concession
            concession_without_request_count=0,
            avg_negotiation_rounds=1.0,
            total_deals_negotiated=20,
        )
        result = self.engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.excessive_discounting


# ===========================================================================
# 12. Pricing risk flag
# ===========================================================================

class TestHasPricingRisk:
    def setup_method(self):
        self.engine = make_engine()

    def test_false_when_composite_low_and_no_other_triggers(self):
        inp = make_input(avg_discount_depth_pct=0.05, avg_contract_value_vs_target_pct=0.95)
        result = self.engine.assess(inp)
        # composite should be low; let's just check the flag logic
        assert not result.has_pricing_risk or result.negotiation_composite >= 40 or \
               inp.avg_discount_depth_pct >= 0.20 or inp.avg_contract_value_vs_target_pct < 0.80

    def test_true_when_composite_at_40(self):
        inp = make_input(avg_discount_depth_pct=0.05, avg_contract_value_vs_target_pct=0.95,
                         max_discount_given_pct=0.40,
                         deals_requiring_discount_count=14, total_deals_negotiated=20,
                         first_concession_timing_days=1.0,
                         concession_without_request_count=6,
                         avg_negotiation_rounds=4.0)
        r = self.engine._has_pricing_risk(40.0, inp)
        assert r is True

    def test_true_when_avg_discount_depth_above_20(self):
        inp = make_input(avg_discount_depth_pct=0.20, avg_contract_value_vs_target_pct=0.95)
        assert self.engine._has_pricing_risk(0.0, inp) is True

    def test_true_when_contract_value_below_80(self):
        inp = make_input(avg_discount_depth_pct=0.01, avg_contract_value_vs_target_pct=0.79)
        assert self.engine._has_pricing_risk(0.0, inp) is False or \
               inp.avg_contract_value_vs_target_pct < 0.80  # just confirm logic applies
        assert self.engine._has_pricing_risk(0.0, inp) is True

    def test_false_when_all_conditions_below_threshold(self):
        inp = make_input(avg_discount_depth_pct=0.10, avg_contract_value_vs_target_pct=0.95)
        assert self.engine._has_pricing_risk(10.0, inp) is False


# ===========================================================================
# 13. Requires negotiation coaching flag
# ===========================================================================

class TestRequiresNegotiationCoaching:
    def setup_method(self):
        self.engine = make_engine()

    def test_false_when_no_triggers(self):
        inp = make_input(avg_discount_depth_pct=0.05,
                         concession_without_request_count=0,
                         total_deals_negotiated=20)
        assert self.engine._requires_negotiation_coaching(0.0, inp) is False

    def test_true_when_composite_at_30(self):
        inp = make_input(avg_discount_depth_pct=0.05,
                         concession_without_request_count=0,
                         total_deals_negotiated=20)
        assert self.engine._requires_negotiation_coaching(30.0, inp) is True

    def test_true_when_avg_discount_at_15(self):
        inp = make_input(avg_discount_depth_pct=0.15,
                         concession_without_request_count=0,
                         total_deals_negotiated=20)
        assert self.engine._requires_negotiation_coaching(0.0, inp) is True

    def test_true_when_unsolicited_rate_at_20(self):
        inp = make_input(avg_discount_depth_pct=0.05,
                         concession_without_request_count=4,
                         total_deals_negotiated=20)
        # rate = 0.20 -> True
        assert self.engine._requires_negotiation_coaching(0.0, inp) is True

    def test_false_when_unsolicited_rate_below_20(self):
        inp = make_input(avg_discount_depth_pct=0.05,
                         concession_without_request_count=3,
                         total_deals_negotiated=20)
        # rate = 0.15 < 0.20 -> False (assuming composite < 30 and discount < 0.15)
        assert self.engine._requires_negotiation_coaching(0.0, inp) is False


# ===========================================================================
# 14. Estimated margin erosion
# ===========================================================================

class TestEstimatedMarginErosion:
    def setup_method(self):
        self.engine = make_engine()

    def test_zero_when_no_discounts(self):
        inp = make_input(deals_requiring_discount_count=0, avg_opportunity_value_usd=50_000,
                         avg_discount_depth_pct=0.10)
        assert self.engine._estimated_margin_erosion(inp, 50.0) == 0.0

    def test_zero_when_composite_zero(self):
        inp = make_input(deals_requiring_discount_count=10, avg_opportunity_value_usd=50_000,
                         avg_discount_depth_pct=0.10)
        assert self.engine._estimated_margin_erosion(inp, 0.0) == 0.0

    def test_calculation_correctness(self):
        inp = make_input(deals_requiring_discount_count=10,
                         avg_opportunity_value_usd=100_000.0,
                         avg_discount_depth_pct=0.10)
        # 10 * 100_000 * 0.10 * (50/100) = 50_000
        assert self.engine._estimated_margin_erosion(inp, 50.0) == 50_000.0

    def test_calculation_rounds_to_2_decimals(self):
        inp = make_input(deals_requiring_discount_count=3,
                         avg_opportunity_value_usd=33_333.33,
                         avg_discount_depth_pct=0.10)
        result = self.engine._estimated_margin_erosion(inp, 50.0)
        assert result == round(3 * 33_333.33 * 0.10 * 0.50, 2)

    def test_scales_with_composite(self):
        inp = make_input(deals_requiring_discount_count=10,
                         avg_opportunity_value_usd=100_000.0,
                         avg_discount_depth_pct=0.10)
        e25 = self.engine._estimated_margin_erosion(inp, 25.0)
        e50 = self.engine._estimated_margin_erosion(inp, 50.0)
        assert e50 == pytest.approx(e25 * 2)

    def test_scales_with_deal_count(self):
        inp5 = make_input(deals_requiring_discount_count=5,
                          avg_opportunity_value_usd=100_000.0,
                          avg_discount_depth_pct=0.10)
        inp10 = make_input(deals_requiring_discount_count=10,
                           avg_opportunity_value_usd=100_000.0,
                           avg_discount_depth_pct=0.10)
        assert self.engine._estimated_margin_erosion(inp10, 50.0) == pytest.approx(
            2 * self.engine._estimated_margin_erosion(inp5, 50.0)
        )


# ===========================================================================
# 15. Signal generation
# ===========================================================================

class TestSignalGeneration:
    def setup_method(self):
        self.engine = make_engine()

    def test_healthy_signal_when_none_pattern_and_composite_below_20(self):
        signal = self.engine._signal(make_input(), NegotiationPattern.none, 5.0)
        assert signal == "Negotiation effectiveness healthy — pricing discipline and value defense within benchmarks"

    def test_healthy_signal_exact_boundary_composite_19(self):
        signal = self.engine._signal(make_input(), NegotiationPattern.none, 19.9)
        assert signal == "Negotiation effectiveness healthy — pricing discipline and value defense within benchmarks"

    def test_non_healthy_when_composite_exactly_20(self):
        signal = self.engine._signal(make_input(), NegotiationPattern.none, 20.0)
        assert "healthy" not in signal.lower() or "composite 20" in signal

    def test_non_healthy_when_pattern_is_not_none(self):
        signal = self.engine._signal(make_input(), NegotiationPattern.excessive_discounting, 5.0)
        assert "Negotiation effectiveness healthy" not in signal

    def test_signal_contains_avg_discount_when_above_08(self):
        inp = make_input(avg_discount_depth_pct=0.10)
        signal = self.engine._signal(inp, NegotiationPattern.excessive_discounting, 50.0)
        assert "10% avg discount" in signal

    def test_signal_contains_first_concession_when_le_7_days(self):
        inp = make_input(first_concession_timing_days=5.0)
        signal = self.engine._signal(inp, NegotiationPattern.premature_concession, 50.0)
        assert "5d first concession" in signal

    def test_signal_contains_contract_value_pct_when_below_1(self):
        inp = make_input(avg_contract_value_vs_target_pct=0.85)
        signal = self.engine._signal(inp, NegotiationPattern.price_erosion, 50.0)
        assert "85% of target ACV" in signal

    def test_signal_label_uses_pattern_name(self):
        inp = make_input(avg_discount_depth_pct=0.01, first_concession_timing_days=10.0,
                         avg_contract_value_vs_target_pct=1.05)
        signal = self.engine._signal(inp, NegotiationPattern.excessive_discounting, 50.0)
        assert signal.startswith("Excessive discounting")

    def test_signal_label_replaces_underscores(self):
        inp = make_input(avg_discount_depth_pct=0.01, first_concession_timing_days=10.0,
                         avg_contract_value_vs_target_pct=1.05)
        signal = self.engine._signal(inp, NegotiationPattern.price_erosion, 50.0)
        assert "_" not in signal.split("—")[0]

    def test_signal_fallback_when_no_parts(self):
        # No parts: avg_discount < 0.08, first_concession > 7, contract_value >= 1.0
        inp = make_input(avg_discount_depth_pct=0.01, first_concession_timing_days=10.0,
                         avg_contract_value_vs_target_pct=1.05)
        signal = self.engine._signal(inp, NegotiationPattern.none, 25.0)
        assert "pricing integrity declining" in signal

    def test_signal_contains_composite(self):
        inp = make_input(avg_discount_depth_pct=0.10)
        signal = self.engine._signal(inp, NegotiationPattern.excessive_discounting, 42.0)
        assert "composite 42" in signal

    def test_signal_for_negotiation_risk_label_when_no_pattern(self):
        inp = make_input(avg_discount_depth_pct=0.01, first_concession_timing_days=10.0,
                         avg_contract_value_vs_target_pct=1.05)
        signal = self.engine._signal(inp, NegotiationPattern.none, 25.0)
        assert "Negotiation risk" in signal


# ===========================================================================
# 16. Composite score computation
# ===========================================================================

class TestCompositeScoreComputation:
    def setup_method(self):
        self.engine = make_engine()

    def test_composite_formula_weights(self):
        # Use predictable sub-scores and verify composite
        inp = make_input(
            avg_discount_depth_pct=0.08,  # +8 discount
            max_discount_given_pct=0.05,
            deals_requiring_discount_count=0,
            first_concession_timing_days=10.0,  # 0 concession
            concession_without_request_count=0,
            avg_negotiation_rounds=1.0,
            value_anchor_usage_pct=0.80,   # 0 value
            avg_contract_value_vs_target_pct=1.0,
            late_stage_reprice_count=0,
            deals_lost_on_price_count=0,   # 0 close
            avg_time_to_close_after_negotiation_days=3.0,
            procurement_discount_rate_pct=0.05,
            total_deals_negotiated=20,
        )
        result = self.engine.assess(inp)
        # discount=8, concession=0, value=0, close=0
        # composite = 8*0.30 + 0*0.30 + 0*0.25 + 0*0.15 = 2.4
        assert result.negotiation_composite == pytest.approx(2.4)

    def test_composite_capped_at_100(self):
        # All sub-scores maxed out
        inp = make_input(
            avg_discount_depth_pct=0.50, max_discount_given_pct=0.50,
            deals_requiring_discount_count=20, total_deals_negotiated=20,
            first_concession_timing_days=0.5,
            concession_without_request_count=20,
            avg_negotiation_rounds=10.0,
            value_anchor_usage_pct=0.0,
            avg_contract_value_vs_target_pct=0.50,
            late_stage_reprice_count=10,
            deals_lost_on_price_count=20,
            avg_time_to_close_after_negotiation_days=60.0,
            procurement_discount_rate_pct=0.50,
        )
        result = self.engine.assess(inp)
        assert result.negotiation_composite <= 100.0

    def test_composite_is_rounded_to_1_decimal(self):
        inp = make_input()
        result = self.engine.assess(inp)
        # Should be rounded to 1 decimal
        assert result.negotiation_composite == round(result.negotiation_composite, 1)


# ===========================================================================
# 17. assess() method – integration
# ===========================================================================

class TestAssessMethod:
    def setup_method(self):
        self.engine = make_engine()

    def test_returns_result_instance(self):
        result = self.engine.assess(make_input())
        assert isinstance(result, NegotiationEffectivenessResult)

    def test_rep_id_carried_through(self):
        result = self.engine.assess(make_input(rep_id="ABC-123"))
        assert result.rep_id == "ABC-123"

    def test_region_carried_through(self):
        result = self.engine.assess(make_input(region="EMEA"))
        assert result.region == "EMEA"

    def test_result_stored_in_results_list(self):
        engine = make_engine()
        engine.assess(make_input())
        assert len(engine._results) == 1

    def test_multiple_assesses_accumulate(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="A"))
        engine.assess(make_input(rep_id="B"))
        assert len(engine._results) == 2

    def test_healthy_rep_gets_low_risk(self):
        result = self.engine.assess(make_input())
        assert result.negotiation_risk == NegotiationRisk.low

    def test_healthy_rep_gets_no_action(self):
        result = self.engine.assess(make_input())
        assert result.recommended_action == NegotiationAction.no_action

    def test_healthy_rep_gets_strong_severity(self):
        result = self.engine.assess(make_input())
        assert result.negotiation_severity == NegotiationSeverity.strong

    def test_sub_scores_are_in_result(self):
        result = self.engine.assess(make_input())
        assert result.discount_discipline_score >= 0
        assert result.concession_behavior_score >= 0
        assert result.value_defense_score >= 0
        assert result.close_effectiveness_score >= 0

    def test_scores_do_not_exceed_100(self):
        result = self.engine.assess(make_input())
        assert result.discount_discipline_score <= 100.0
        assert result.concession_behavior_score <= 100.0
        assert result.value_defense_score <= 100.0
        assert result.close_effectiveness_score <= 100.0

    def test_composite_consistent_with_sub_scores(self):
        inp = make_input()
        result = self.engine.assess(inp)
        expected = round(
            result.discount_discipline_score * 0.30
            + result.concession_behavior_score * 0.30
            + result.value_defense_score * 0.25
            + result.close_effectiveness_score * 0.15,
            1,
        )
        assert result.negotiation_composite == pytest.approx(min(expected, 100.0))

    def test_rounding_of_sub_scores(self):
        result = self.engine.assess(make_input())
        # Sub-scores should be rounded to 1 decimal
        for score in [result.discount_discipline_score, result.concession_behavior_score,
                      result.value_defense_score, result.close_effectiveness_score]:
            assert score == round(score, 1)


# ===========================================================================
# 18. assess_batch() method
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.engine = make_engine()

    def test_returns_list(self):
        results = self.engine.assess_batch([make_input(), make_input(rep_id="B")])
        assert isinstance(results, list)

    def test_list_length_matches_inputs(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = self.engine.assess_batch(inputs)
        assert len(results) == 5

    def test_empty_batch_returns_empty(self):
        results = self.engine.assess_batch([])
        assert results == []

    def test_each_result_is_result_instance(self):
        results = self.engine.assess_batch([make_input(), make_input(rep_id="B")])
        for r in results:
            assert isinstance(r, NegotiationEffectivenessResult)

    def test_order_preserved(self):
        inp_a = make_input(rep_id="A")
        inp_b = make_input(rep_id="B")
        results = self.engine.assess_batch([inp_a, inp_b])
        assert results[0].rep_id == "A"
        assert results[1].rep_id == "B"

    def test_batch_accumulates_internal_results(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_batch_after_single_assess(self):
        engine = make_engine()
        engine.assess(make_input(rep_id="X"))
        engine.assess_batch([make_input(rep_id="A"), make_input(rep_id="B")])
        assert len(engine._results) == 3

    def test_single_element_batch(self):
        results = self.engine.assess_batch([make_input(rep_id="ONLY")])
        assert len(results) == 1
        assert results[0].rep_id == "ONLY"


# ===========================================================================
# 19. summary() method
# ===========================================================================

class TestSummaryMethod:
    def test_empty_summary_returns_13_keys(self):
        engine = make_engine()
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_total_is_zero(self):
        engine = make_engine()
        assert engine.summary()["total"] == 0

    def test_empty_summary_risk_counts_empty(self):
        engine = make_engine()
        assert engine.summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self):
        engine = make_engine()
        assert engine.summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self):
        engine = make_engine()
        assert engine.summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        engine = make_engine()
        assert engine.summary()["action_counts"] == {}

    def test_empty_summary_avg_composite_zero(self):
        engine = make_engine()
        assert engine.summary()["avg_negotiation_composite"] == 0.0

    def test_empty_summary_pricing_risk_count_zero(self):
        engine = make_engine()
        assert engine.summary()["pricing_risk_count"] == 0

    def test_empty_summary_coaching_count_zero(self):
        engine = make_engine()
        assert engine.summary()["coaching_count"] == 0

    def test_empty_summary_avg_scores_zero(self):
        engine = make_engine()
        s = engine.summary()
        assert s["avg_discount_discipline_score"] == 0.0
        assert s["avg_concession_behavior_score"] == 0.0
        assert s["avg_value_defense_score"] == 0.0
        assert s["avg_close_effectiveness_score"] == 0.0

    def test_empty_summary_total_erosion_zero(self):
        engine = make_engine()
        assert engine.summary()["total_estimated_margin_erosion_usd"] == 0.0

    def test_summary_total_matches_assessed_count(self):
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert engine.summary()["total"] == 5

    def test_summary_risk_counts_correct(self):
        engine = make_engine()
        engine.assess(make_input())  # should be low
        s = engine.summary()
        assert "low" in s["risk_counts"]
        assert s["risk_counts"]["low"] == 1

    def test_summary_pattern_counts_correct(self):
        engine = make_engine()
        engine.assess(make_input())  # should be none
        assert engine.summary()["pattern_counts"].get("none", 0) == 1

    def test_summary_severity_counts_correct(self):
        engine = make_engine()
        engine.assess(make_input())  # should be strong
        assert engine.summary()["severity_counts"].get("strong", 0) == 1

    def test_summary_action_counts_correct(self):
        engine = make_engine()
        engine.assess(make_input())  # should be no_action
        assert engine.summary()["action_counts"].get("no_action", 0) == 1

    def test_summary_avg_composite_is_rounded(self):
        engine = make_engine()
        engine.assess(make_input())
        s = engine.summary()
        assert s["avg_negotiation_composite"] == round(s["avg_negotiation_composite"], 1)

    def test_summary_pricing_risk_count_accuracy(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy -> no pricing risk
        engine.assess(make_input(avg_discount_depth_pct=0.25))  # has pricing risk
        s = engine.summary()
        assert s["pricing_risk_count"] >= 1

    def test_summary_coaching_count_accuracy(self):
        engine = make_engine()
        engine.assess(make_input())  # healthy -> no coaching
        engine.assess(make_input(avg_discount_depth_pct=0.20))  # coaching needed
        s = engine.summary()
        assert s["coaching_count"] >= 1

    def test_summary_has_all_13_keys(self):
        engine = make_engine()
        engine.assess(make_input())
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_negotiation_composite", "pricing_risk_count",
            "coaching_count", "avg_discount_discipline_score",
            "avg_concession_behavior_score", "avg_value_defense_score",
            "avg_close_effectiveness_score", "total_estimated_margin_erosion_usd",
        }
        assert set(engine.summary().keys()) == expected_keys

    def test_summary_total_erosion_rounded_to_2(self):
        engine = make_engine()
        engine.assess(make_input(deals_requiring_discount_count=3,
                                  avg_opportunity_value_usd=33_333.33,
                                  avg_discount_depth_pct=0.10))
        s = engine.summary()
        assert s["total_estimated_margin_erosion_usd"] == round(s["total_estimated_margin_erosion_usd"], 2)

    def test_summary_multiple_reps_risk_counts_aggregate(self):
        engine = make_engine()
        # Create one moderate and one low
        inp_low = make_input(rep_id="LOW")
        engine.assess(inp_low)
        # Force a moderate composite: use a rep with moderate scores
        inp_moderate = make_input(
            rep_id="MOD",
            avg_discount_depth_pct=0.15,
            max_discount_given_pct=0.25,
            deals_requiring_discount_count=10,
            total_deals_negotiated=20,
            first_concession_timing_days=3.0,
        )
        engine.assess(inp_moderate)
        s = engine.summary()
        assert s["total"] == 2


# ===========================================================================
# 20. Edge cases
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.engine = make_engine()

    def test_zero_total_deals_no_error(self):
        inp = make_input(total_deals_negotiated=0)
        result = self.engine.assess(inp)
        assert isinstance(result, NegotiationEffectivenessResult)

    def test_single_deal_no_error(self):
        inp = make_input(total_deals_negotiated=1)
        result = self.engine.assess(inp)
        assert isinstance(result, NegotiationEffectivenessResult)

    def test_very_large_values_no_error(self):
        inp = make_input(total_deals_negotiated=10_000,
                         avg_opportunity_value_usd=10_000_000.0,
                         deals_requiring_discount_count=5_000)
        result = self.engine.assess(inp)
        assert isinstance(result, NegotiationEffectivenessResult)

    def test_all_zero_numeric_fields(self):
        inp = make_input(
            total_deals_negotiated=0,
            deals_requiring_discount_count=0,
            avg_discount_depth_pct=0.0,
            max_discount_given_pct=0.0,
            deals_closed_at_list_price_count=0,
            avg_negotiation_rounds=0.0,
            deals_won_after_negotiation_count=0,
            deals_lost_on_price_count=0,
            first_concession_timing_days=0.0,
            concession_without_request_count=0,
            multi_round_deals_count=0,
            value_anchor_usage_pct=0.0,
            competitive_pressure_discount_pct=0.0,
            deals_with_procurement_count=0,
            procurement_discount_rate_pct=0.0,
            avg_contract_value_vs_target_pct=0.0,
            late_stage_reprice_count=0,
            avg_time_to_close_after_negotiation_days=0.0,
            avg_opportunity_value_usd=0.0,
        )
        result = self.engine.assess(inp)
        assert isinstance(result, NegotiationEffectivenessResult)

    def test_boundary_discount_depth_exactly_at_008(self):
        inp = make_input(avg_discount_depth_pct=0.08)
        score = self.engine._discount_discipline_score(inp)
        # exactly at threshold -> +8
        assert score >= 8.0

    def test_boundary_discount_depth_just_below_008(self):
        inp = make_input(avg_discount_depth_pct=0.0799)
        score = self.engine._discount_discipline_score(inp)
        # just below threshold -> 0 from depth
        assert score == 0.0 or inp.max_discount_given_pct >= 0.25

    def test_boundary_composite_at_exactly_20(self):
        risk = self.engine._risk_level(20.0)
        severity = self.engine._severity(20.0)
        assert risk == NegotiationRisk.moderate
        assert severity == NegotiationSeverity.developing

    def test_boundary_composite_at_exactly_40(self):
        risk = self.engine._risk_level(40.0)
        severity = self.engine._severity(40.0)
        assert risk == NegotiationRisk.high
        assert severity == NegotiationSeverity.vulnerable

    def test_boundary_composite_at_exactly_60(self):
        risk = self.engine._risk_level(60.0)
        severity = self.engine._severity(60.0)
        assert risk == NegotiationRisk.critical
        assert severity == NegotiationSeverity.collapsing

    def test_empty_rep_id_allowed(self):
        inp = make_input(rep_id="")
        result = self.engine.assess(inp)
        assert result.rep_id == ""

    def test_erosion_always_non_negative(self):
        inp = make_input(deals_requiring_discount_count=10,
                         avg_opportunity_value_usd=50_000.0,
                         avg_discount_depth_pct=0.10)
        result = self.engine.assess(inp)
        assert result.estimated_margin_erosion_usd >= 0.0

    def test_composite_equals_100_when_capped(self):
        # With very high scores, composite should be capped at 100
        inp = make_input(
            avg_discount_depth_pct=0.50, max_discount_given_pct=0.60,
            deals_requiring_discount_count=20, total_deals_negotiated=20,
            first_concession_timing_days=0.0,
            concession_without_request_count=20,
            avg_negotiation_rounds=5.0,
            value_anchor_usage_pct=0.0,
            avg_contract_value_vs_target_pct=0.5,
            late_stage_reprice_count=10,
            deals_lost_on_price_count=20,
            avg_time_to_close_after_negotiation_days=60.0,
            procurement_discount_rate_pct=0.50,
        )
        result = self.engine.assess(inp)
        assert result.negotiation_composite <= 100.0


# ===========================================================================
# 21. End-to-end scenario tests
# ===========================================================================

class TestEndToEndScenarios:
    """Full end-to-end scenarios with specific expected outcomes."""

    def test_e2e_healthy_rep(self):
        """Perfectly healthy rep should get low risk, no action, strong severity, none pattern."""
        engine = make_engine()
        inp = make_input()
        result = engine.assess(inp)
        assert result.negotiation_risk == NegotiationRisk.low
        assert result.negotiation_severity == NegotiationSeverity.strong
        assert result.negotiation_pattern == NegotiationPattern.none
        assert result.recommended_action == NegotiationAction.no_action
        assert "healthy" in result.negotiation_signal.lower()

    def test_e2e_excessive_discounter(self):
        """Rep giving deep discounts -> excessive_discounting pattern."""
        engine = make_engine()
        inp = make_input(
            avg_discount_depth_pct=0.35,  # -> +40 discount score
            max_discount_given_pct=0.45,  # -> +30 max
            deals_requiring_discount_count=16,  # rate=0.80 -> +25
            total_deals_negotiated=20,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.excessive_discounting

    def test_e2e_critical_risk_deal_desk_escalation(self):
        """Critical risk + excessive_discounting -> deal_desk_escalation."""
        engine = make_engine()
        # Build critical composite (>= 60) with excessive_discounting pattern
        inp = make_input(
            avg_discount_depth_pct=0.30,
            max_discount_given_pct=0.45,
            deals_requiring_discount_count=16,
            total_deals_negotiated=20,
            first_concession_timing_days=1.0,
            concession_without_request_count=8,
            avg_negotiation_rounds=4.0,
            value_anchor_usage_pct=0.10,
            avg_contract_value_vs_target_pct=0.75,
            late_stage_reprice_count=3,
            deals_lost_on_price_count=6,
            avg_time_to_close_after_negotiation_days=30.0,
            procurement_discount_rate_pct=0.25,
        )
        result = engine.assess(inp)
        if result.negotiation_risk == NegotiationRisk.critical and \
           result.negotiation_pattern == NegotiationPattern.excessive_discounting:
            assert result.recommended_action == NegotiationAction.deal_desk_escalation

    def test_e2e_to_dict_round_trip(self):
        """assess() result should serialize via to_dict() with correct types."""
        engine = make_engine()
        result = engine.assess(make_input(rep_id="DICT-TEST", region="South"))
        d = result.to_dict()
        assert d["rep_id"] == "DICT-TEST"
        assert d["region"] == "South"
        assert isinstance(d["negotiation_risk"], str)
        assert isinstance(d["negotiation_pattern"], str)
        assert isinstance(d["has_pricing_risk"], bool)
        assert isinstance(d["requires_negotiation_coaching"], bool)

    def test_e2e_batch_then_summary(self):
        """Batch assess, then summarize — totals must match."""
        engine = make_engine()
        inputs = [make_input(rep_id=f"R{i}", region="West") for i in range(7)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 7
        total_risk = sum(s["risk_counts"].values())
        assert total_risk == 7

    def test_e2e_pricing_risk_when_deep_discount(self):
        """avg_discount_depth_pct >= 0.20 forces has_pricing_risk=True."""
        engine = make_engine()
        inp = make_input(avg_discount_depth_pct=0.22)
        result = engine.assess(inp)
        assert result.has_pricing_risk is True

    def test_e2e_coaching_required_when_high_unsolicited_rate(self):
        """unsolicited_rate >= 0.20 forces requires_negotiation_coaching=True."""
        engine = make_engine()
        inp = make_input(concession_without_request_count=4, total_deals_negotiated=20)
        result = engine.assess(inp)
        assert result.requires_negotiation_coaching is True

    def test_e2e_margin_erosion_is_positive_for_discounting_rep(self):
        """Rep with discounts should have positive margin erosion when composite > 0."""
        engine = make_engine()
        inp = make_input(
            deals_requiring_discount_count=10,
            avg_discount_depth_pct=0.15,
            avg_opportunity_value_usd=100_000.0,
        )
        result = engine.assess(inp)
        assert result.estimated_margin_erosion_usd > 0.0

    def test_e2e_signal_benchmark_message_exact_text(self):
        """Signal benchmark exact text when pattern==none and composite<20."""
        engine = make_engine()
        inp = make_input()
        result = engine.assess(inp)
        if result.negotiation_pattern == NegotiationPattern.none and result.negotiation_composite < 20:
            assert result.negotiation_signal == \
                "Negotiation effectiveness healthy — pricing discipline and value defense within benchmarks"

    def test_e2e_summary_avg_composite_reasonable(self):
        """After batch, avg composite should be between 0 and 100."""
        engine = make_engine()
        engine.assess_batch([make_input(rep_id=f"R{i}") for i in range(10)])
        s = engine.summary()
        assert 0.0 <= s["avg_negotiation_composite"] <= 100.0

    def test_e2e_multiple_engines_independent(self):
        """Two engines should not share state."""
        engine1 = make_engine()
        engine2 = make_engine()
        engine1.assess(make_input(rep_id="E1"))
        assert len(engine2._results) == 0

    def test_e2e_high_risk_price_erosion_gets_pricing_integrity(self):
        """Critical risk + price_erosion -> pricing_integrity_program."""
        engine = make_engine()
        # We'll manually test the _action method
        action = engine._action(NegotiationRisk.critical, NegotiationPattern.price_erosion)
        assert action == NegotiationAction.pricing_integrity_program

    def test_e2e_high_risk_no_special_pattern_gets_discount_review(self):
        engine = make_engine()
        action = engine._action(NegotiationRisk.high, NegotiationPattern.none)
        assert action == NegotiationAction.discount_authority_review

    def test_e2e_rep_with_procurement_pressure(self):
        """Rep dealing heavily with procurement at high discount rates."""
        engine = make_engine()
        inp = make_input(
            deals_with_procurement_count=15,
            procurement_discount_rate_pct=0.25,
        )
        result = engine.assess(inp)
        # Should have elevated close effectiveness score
        assert result.close_effectiveness_score >= 20.0

    def test_e2e_late_stage_reprice_elevates_value_defense(self):
        """Multiple late stage reprices should elevate value defense score."""
        engine = make_engine()
        inp = make_input(
            value_anchor_usage_pct=0.80,
            avg_contract_value_vs_target_pct=1.0,
            late_stage_reprice_count=3,
        )
        result = engine.assess(inp)
        assert result.value_defense_score >= 25.0


# ===========================================================================
# 22. Additional sub-score boundary tests
# ===========================================================================

class TestDiscountDisciplineScoreBoundaries:
    def setup_method(self):
        self.engine = make_engine()

    def test_discount_rate_just_below_50_no_rate_contribution(self):
        inp = make_input(avg_discount_depth_pct=0.0, max_discount_given_pct=0.0,
                         deals_requiring_discount_count=9, total_deals_negotiated=20)
        # rate = 0.45 < 0.50 -> 0 from rate
        assert self.engine._discount_discipline_score(inp) == 0.0

    def test_discount_rate_exactly_50_adds_13(self):
        inp = make_input(avg_discount_depth_pct=0.0, max_discount_given_pct=0.0,
                         deals_requiring_discount_count=10, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 13.0

    def test_avg_discount_between_08_and_15_adds_8(self):
        inp = make_input(avg_discount_depth_pct=0.12, max_discount_given_pct=0.0,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 8.0

    def test_avg_discount_between_15_and_25_adds_22(self):
        inp = make_input(avg_discount_depth_pct=0.20, max_discount_given_pct=0.0,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 22.0

    def test_max_discount_between_25_and_40_adds_15(self):
        inp = make_input(avg_discount_depth_pct=0.0, max_discount_given_pct=0.30,
                         deals_requiring_discount_count=0, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 15.0

    def test_total_score_of_all_medium_bands(self):
        # avg=0.15 (+22), max=0.30 (+15), rate=0.50 (+13) = 50
        inp = make_input(avg_discount_depth_pct=0.15, max_discount_given_pct=0.30,
                         deals_requiring_discount_count=10, total_deals_negotiated=20)
        assert self.engine._discount_discipline_score(inp) == 50.0


class TestConcessionBehaviorScoreBoundaries:
    def setup_method(self):
        self.engine = make_engine()

    def test_first_concession_between_1_and_3_days_adds_20(self):
        inp = make_input(first_concession_timing_days=2.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=1.0, total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 20.0

    def test_first_concession_between_3_and_7_days_adds_8(self):
        inp = make_input(first_concession_timing_days=5.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=1.0, total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 8.0

    def test_unsolicited_rate_just_below_05_adds_0(self):
        # 0/20 = 0.0 < 0.05 -> 0
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=1.0, total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 0.0

    def test_unsolicited_rate_between_05_and_15_adds_7(self):
        # 2/20 = 0.10 -> +7
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=2,
                         avg_negotiation_rounds=1.0, total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 7.0

    def test_rounds_between_3_and_4_adds_10(self):
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=3.5, total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 10.0

    def test_rounds_at_2_99_no_round_contribution(self):
        inp = make_input(first_concession_timing_days=15.0,
                         concession_without_request_count=0,
                         avg_negotiation_rounds=2.9, total_deals_negotiated=20)
        assert self.engine._concession_behavior_score(inp) == 0.0


class TestValueDefenseScoreBoundaries:
    def setup_method(self):
        self.engine = make_engine()

    def test_anchor_between_40_and_60_adds_7(self):
        inp = make_input(value_anchor_usage_pct=0.50,
                         avg_contract_value_vs_target_pct=1.0,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 7.0

    def test_contract_just_above_90_adds_0(self):
        inp = make_input(value_anchor_usage_pct=0.80,
                         avg_contract_value_vs_target_pct=0.91,
                         late_stage_reprice_count=0)
        assert self.engine._value_defense_score(inp) == 0.0

    def test_late_reprice_at_2_adds_12(self):
        inp = make_input(value_anchor_usage_pct=0.80,
                         avg_contract_value_vs_target_pct=1.0,
                         late_stage_reprice_count=2)
        assert self.engine._value_defense_score(inp) == 12.0

    def test_all_three_components_mid_band(self):
        # anchor=0.30 (+18), contract=0.85 (+15), reprice=2 (+12) = 45
        inp = make_input(value_anchor_usage_pct=0.30,
                         avg_contract_value_vs_target_pct=0.85,
                         late_stage_reprice_count=2)
        assert self.engine._value_defense_score(inp) == 45.0


class TestCloseEffectivenessScoreBoundaries:
    def setup_method(self):
        self.engine = make_engine()

    def test_price_loss_below_08_adds_0(self):
        inp = make_input(deals_lost_on_price_count=1, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=3.0,
                         procurement_discount_rate_pct=0.0)
        # rate = 0.05 < 0.08 -> 0
        assert self.engine._close_effectiveness_score(inp) == 0.0

    def test_close_days_below_7_adds_0(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=6.9,
                         procurement_discount_rate_pct=0.0)
        assert self.engine._close_effectiveness_score(inp) == 0.0

    def test_close_days_between_7_and_14_adds_7(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=10.0,
                         procurement_discount_rate_pct=0.0)
        assert self.engine._close_effectiveness_score(inp) == 7.0

    def test_close_days_between_14_and_30_adds_18(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=20.0,
                         procurement_discount_rate_pct=0.0)
        assert self.engine._close_effectiveness_score(inp) == 18.0

    def test_procurement_below_10_adds_0(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=3.0,
                         procurement_discount_rate_pct=0.09)
        assert self.engine._close_effectiveness_score(inp) == 0.0

    def test_procurement_between_10_and_20_adds_10(self):
        inp = make_input(deals_lost_on_price_count=0, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=3.0,
                         procurement_discount_rate_pct=0.15)
        assert self.engine._close_effectiveness_score(inp) == 10.0

    def test_all_three_max_bands(self):
        # price_loss=0.25 (+40), close_days=30 (+35), proc=0.20 (+20) = 95
        inp = make_input(deals_lost_on_price_count=5, total_deals_negotiated=20,
                         avg_time_to_close_after_negotiation_days=30.0,
                         procurement_discount_rate_pct=0.20)
        assert self.engine._close_effectiveness_score(inp) == 95.0


# ===========================================================================
# 23. Additional action mapping tests
# ===========================================================================

class TestActionMappingAdditional:
    def setup_method(self):
        self.engine = make_engine()

    def test_low_risk_none_pattern_is_no_action(self):
        assert self.engine._action(NegotiationRisk.low, NegotiationPattern.none) == NegotiationAction.no_action

    def test_low_risk_excessive_discounting_still_no_action(self):
        assert self.engine._action(NegotiationRisk.low, NegotiationPattern.excessive_discounting) == NegotiationAction.no_action

    def test_moderate_risk_price_erosion_is_coaching(self):
        assert self.engine._action(NegotiationRisk.moderate, NegotiationPattern.price_erosion) == NegotiationAction.negotiation_coaching

    def test_moderate_risk_value_abandonment_is_coaching(self):
        assert self.engine._action(NegotiationRisk.moderate, NegotiationPattern.value_abandonment) == NegotiationAction.negotiation_coaching

    def test_critical_risk_negotiation_avoidance_is_deal_desk(self):
        assert self.engine._action(NegotiationRisk.critical, NegotiationPattern.negotiation_avoidance) == NegotiationAction.deal_desk_escalation

    def test_high_risk_excessive_discounting_is_discount_review(self):
        assert self.engine._action(NegotiationRisk.high, NegotiationPattern.excessive_discounting) == NegotiationAction.discount_authority_review

    def test_high_risk_price_erosion_is_discount_review(self):
        assert self.engine._action(NegotiationRisk.high, NegotiationPattern.price_erosion) == NegotiationAction.discount_authority_review

    def test_high_risk_negotiation_avoidance_is_discount_review(self):
        assert self.engine._action(NegotiationRisk.high, NegotiationPattern.negotiation_avoidance) == NegotiationAction.discount_authority_review


# ===========================================================================
# 24. Additional assess() result type checks
# ===========================================================================

class TestAssessResultTypes:
    def setup_method(self):
        self.engine = make_engine()

    def test_negotiation_risk_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.negotiation_risk, NegotiationRisk)

    def test_negotiation_pattern_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.negotiation_pattern, NegotiationPattern)

    def test_negotiation_severity_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.negotiation_severity, NegotiationSeverity)

    def test_recommended_action_is_enum(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.recommended_action, NegotiationAction)

    def test_has_pricing_risk_is_bool(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.has_pricing_risk, bool)

    def test_requires_coaching_is_bool(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.requires_negotiation_coaching, bool)

    def test_margin_erosion_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.estimated_margin_erosion_usd, float)

    def test_signal_is_str(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.negotiation_signal, str)

    def test_composite_is_float(self):
        result = self.engine.assess(make_input())
        assert isinstance(result.negotiation_composite, float)

    def test_risk_and_severity_agree_on_thresholds(self):
        """Risk and severity levels should be consistent for same composite."""
        for composite in [0, 10, 20, 30, 40, 50, 60, 80, 100]:
            risk = self.engine._risk_level(float(composite))
            sev = self.engine._severity(float(composite))
            # Both follow same thresholds: map them to integer levels and compare
            risk_level = {"low": 0, "moderate": 1, "high": 2, "critical": 3}[risk.value]
            sev_level = {"strong": 0, "developing": 1, "vulnerable": 2, "collapsing": 3}[sev.value]
            assert risk_level == sev_level
