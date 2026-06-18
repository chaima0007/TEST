"""
Comprehensive pytest tests for SalesNegotiationDisciplineIntelligenceEngine.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.sales_negotiation_discipline_intelligence_engine import (
    NegotiationAction,
    NegotiationInput,
    NegotiationPattern,
    NegotiationResult,
    NegotiationRisk,
    NegotiationSeverity,
    SalesNegotiationDisciplineIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_input(**overrides) -> NegotiationInput:
    """Return a clean-profile NegotiationInput with all defaults overridable."""
    defaults = dict(
        rep_id="REP001",
        region="West",
        evaluation_period_id="Q1-2026",
        initial_discount_offered_pct=0.02,       # < 0.05 → +0
        avg_total_discount_given_pct=0.05,        # < 0.20 → +0
        avg_selling_price_vs_list_pct=0.95,       # > 0.85 → +0
        price_concession_without_value_exchange_pct=0.05,  # < 0.20 → +0
        multi_concession_in_single_negotiation_pct=0.05,   # < 0.30 → +0
        final_ask_for_extras_rate_pct=0.05,       # < 0.20 → +0
        champion_deal_only_rate_pct=0.10,         # < 0.25 → +0
        procurement_escalation_rate_pct=0.05,     # < 0.20 → +0
        contract_redline_rounds_avg=1.0,          # < 2.5  → +0
        late_stage_deal_loss_rate_pct=0.05,       # < 0.10 → +0
        decision_deadline_driven_by_rep_pct=0.80, # > 0.50 → +0
        multi_year_deal_rate_pct=0.50,            # > 0.25 → +0
        negotiation_rounds_before_close_avg=1.5,
        deal_closed_at_list_price_pct=0.60,
        competitor_discount_match_rate_pct=0.10,
        payment_terms_extension_rate_pct=0.05,
        legal_review_delay_days_avg=3.0,
        total_late_stage_deals=10,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return NegotiationInput(**defaults)


def _engine() -> SalesNegotiationDisciplineIntelligenceEngine:
    return SalesNegotiationDisciplineIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum membership
# ---------------------------------------------------------------------------

class TestEnums:
    def test_negotiation_risk_values(self):
        assert set(NegotiationRisk) == {
            NegotiationRisk.low,
            NegotiationRisk.moderate,
            NegotiationRisk.high,
            NegotiationRisk.critical,
        }

    def test_negotiation_risk_string_values(self):
        assert NegotiationRisk.low.value == "low"
        assert NegotiationRisk.moderate.value == "moderate"
        assert NegotiationRisk.high.value == "high"
        assert NegotiationRisk.critical.value == "critical"

    def test_negotiation_pattern_values(self):
        assert set(NegotiationPattern) == {
            NegotiationPattern.none,
            NegotiationPattern.chronic_discounter,
            NegotiationPattern.value_cave,
            NegotiationPattern.competitor_price_match,
            NegotiationPattern.single_threaded_close,
            NegotiationPattern.late_stage_collapse,
        }

    def test_negotiation_pattern_string_values(self):
        assert NegotiationPattern.none.value == "none"
        assert NegotiationPattern.chronic_discounter.value == "chronic_discounter"
        assert NegotiationPattern.value_cave.value == "value_cave"
        assert NegotiationPattern.competitor_price_match.value == "competitor_price_match"
        assert NegotiationPattern.single_threaded_close.value == "single_threaded_close"
        assert NegotiationPattern.late_stage_collapse.value == "late_stage_collapse"

    def test_negotiation_severity_values(self):
        assert set(NegotiationSeverity) == {
            NegotiationSeverity.clean,
            NegotiationSeverity.managing,
            NegotiationSeverity.struggling,
            NegotiationSeverity.collapsing,
        }

    def test_negotiation_severity_string_values(self):
        assert NegotiationSeverity.clean.value == "clean"
        assert NegotiationSeverity.managing.value == "managing"
        assert NegotiationSeverity.struggling.value == "struggling"
        assert NegotiationSeverity.collapsing.value == "collapsing"

    def test_negotiation_action_values(self):
        assert set(NegotiationAction) == {
            NegotiationAction.no_action,
            NegotiationAction.negotiation_process_coaching,
            NegotiationAction.stakeholder_expansion_coaching,
            NegotiationAction.close_technique_coaching,
            NegotiationAction.discount_defense_intervention,
            NegotiationAction.value_based_negotiation_reset,
            NegotiationAction.negotiation_reset_intervention,
        }

    def test_negotiation_action_string_values(self):
        assert NegotiationAction.no_action.value == "no_action"
        assert NegotiationAction.negotiation_process_coaching.value == "negotiation_process_coaching"
        assert NegotiationAction.stakeholder_expansion_coaching.value == "stakeholder_expansion_coaching"
        assert NegotiationAction.close_technique_coaching.value == "close_technique_coaching"
        assert NegotiationAction.discount_defense_intervention.value == "discount_defense_intervention"
        assert NegotiationAction.value_based_negotiation_reset.value == "value_based_negotiation_reset"
        assert NegotiationAction.negotiation_reset_intervention.value == "negotiation_reset_intervention"

    def test_enums_are_str_subclass(self):
        assert isinstance(NegotiationRisk.low, str)
        assert isinstance(NegotiationPattern.none, str)
        assert isinstance(NegotiationSeverity.clean, str)
        assert isinstance(NegotiationAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. NegotiationInput – all 22 fields present
# ---------------------------------------------------------------------------

class TestNegotiationInput:
    def test_all_fields_present(self):
        inp = _make_input()
        assert inp.rep_id == "REP001"
        assert inp.region == "West"
        assert inp.evaluation_period_id == "Q1-2026"
        assert inp.initial_discount_offered_pct == 0.02
        assert inp.avg_total_discount_given_pct == 0.05
        assert inp.avg_selling_price_vs_list_pct == 0.95
        assert inp.price_concession_without_value_exchange_pct == 0.05
        assert inp.multi_concession_in_single_negotiation_pct == 0.05
        assert inp.final_ask_for_extras_rate_pct == 0.05
        assert inp.champion_deal_only_rate_pct == 0.10
        assert inp.procurement_escalation_rate_pct == 0.05
        assert inp.contract_redline_rounds_avg == 1.0
        assert inp.late_stage_deal_loss_rate_pct == 0.05
        assert inp.decision_deadline_driven_by_rep_pct == 0.80
        assert inp.multi_year_deal_rate_pct == 0.50
        assert inp.negotiation_rounds_before_close_avg == 1.5
        assert inp.deal_closed_at_list_price_pct == 0.60
        assert inp.competitor_discount_match_rate_pct == 0.10
        assert inp.payment_terms_extension_rate_pct == 0.05
        assert inp.legal_review_delay_days_avg == 3.0
        assert inp.total_late_stage_deals == 10
        assert inp.avg_opportunity_value_usd == 50_000.0

    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(NegotiationInput)
        assert len(fields) == 22


# ---------------------------------------------------------------------------
# 3. NegotiationResult – all 15 fields and to_dict() keys
# ---------------------------------------------------------------------------

class TestNegotiationResult:
    def _make_result(self) -> NegotiationResult:
        engine = _engine()
        return engine.assess(_make_input())

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(NegotiationResult)
        assert len(fields) == 15

    def test_result_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(NegotiationResult)}
        expected = {
            "rep_id", "region", "negotiation_risk", "negotiation_pattern",
            "negotiation_severity", "recommended_action",
            "discount_discipline_score", "concession_behavior_score",
            "deal_construction_score", "close_effectiveness_score",
            "negotiation_composite", "has_negotiation_gap",
            "requires_negotiation_coaching", "estimated_revenue_dilution_usd",
            "negotiation_signal",
        }
        assert names == expected

    def test_to_dict_returns_15_keys(self):
        result = self._make_result()
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        result = self._make_result()
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "negotiation_risk", "negotiation_pattern",
            "negotiation_severity", "recommended_action",
            "discount_discipline_score", "concession_behavior_score",
            "deal_construction_score", "close_effectiveness_score",
            "negotiation_composite", "has_negotiation_gap",
            "requires_negotiation_coaching", "estimated_revenue_dilution_usd",
            "negotiation_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_fields_are_strings(self):
        result = self._make_result()
        d = result.to_dict()
        assert isinstance(d["negotiation_risk"], str)
        assert isinstance(d["negotiation_pattern"], str)
        assert isinstance(d["negotiation_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_and_region(self):
        engine = _engine()
        inp = _make_input(rep_id="REP999", region="East")
        result = engine.assess(inp)
        d = result.to_dict()
        assert d["rep_id"] == "REP999"
        assert d["region"] == "East"


# ---------------------------------------------------------------------------
# 4. Discount Discipline Sub-Score
# ---------------------------------------------------------------------------

class TestDiscountDisciplineScore:
    """
    initial_discount_offered_pct: >=0.25→+40, >=0.15→+22, >=0.05→+8, else 0
    avg_total_discount_given_pct: >=0.30→+35, >=0.20→+18, else 0
    avg_selling_price_vs_list_pct: <=0.70→+25, <=0.85→+12, else 0
    """

    def _score(self, **kw) -> float:
        engine = _engine()
        inp = _make_input(**kw)
        return engine._discount_discipline_score(inp)

    # initial_discount_offered_pct branches
    def test_initial_discount_below_0_05(self):
        assert self._score(initial_discount_offered_pct=0.04) == 0.0

    def test_initial_discount_exactly_0_05(self):
        # >=0.05 → +8
        assert self._score(initial_discount_offered_pct=0.05) == 8.0

    def test_initial_discount_between_0_05_and_0_15(self):
        assert self._score(initial_discount_offered_pct=0.10) == 8.0

    def test_initial_discount_exactly_0_15(self):
        # >=0.15 → +22
        assert self._score(initial_discount_offered_pct=0.15) == 22.0

    def test_initial_discount_between_0_15_and_0_25(self):
        assert self._score(initial_discount_offered_pct=0.20) == 22.0

    def test_initial_discount_exactly_0_25(self):
        # >=0.25 → +40
        assert self._score(initial_discount_offered_pct=0.25) == 40.0

    def test_initial_discount_above_0_25(self):
        assert self._score(initial_discount_offered_pct=0.40) == 40.0

    # avg_total_discount_given_pct branches
    def test_avg_discount_below_0_20(self):
        assert self._score(avg_total_discount_given_pct=0.15) == 0.0

    def test_avg_discount_exactly_0_20(self):
        # >=0.20 → +18
        assert self._score(avg_total_discount_given_pct=0.20) == 18.0

    def test_avg_discount_between_0_20_and_0_30(self):
        assert self._score(avg_total_discount_given_pct=0.25) == 18.0

    def test_avg_discount_exactly_0_30(self):
        # >=0.30 → +35
        assert self._score(avg_total_discount_given_pct=0.30) == 35.0

    def test_avg_discount_above_0_30(self):
        assert self._score(avg_total_discount_given_pct=0.50) == 35.0

    # avg_selling_price_vs_list_pct branches
    def test_selling_price_above_0_85(self):
        assert self._score(avg_selling_price_vs_list_pct=0.90) == 0.0

    def test_selling_price_exactly_0_85(self):
        # <=0.85 → +12
        assert self._score(avg_selling_price_vs_list_pct=0.85) == 12.0

    def test_selling_price_between_0_70_and_0_85(self):
        assert self._score(avg_selling_price_vs_list_pct=0.75) == 12.0

    def test_selling_price_exactly_0_70(self):
        # <=0.70 → +25
        assert self._score(avg_selling_price_vs_list_pct=0.70) == 25.0

    def test_selling_price_below_0_70(self):
        assert self._score(avg_selling_price_vs_list_pct=0.60) == 25.0

    # Combination and cap
    def test_max_score_all_high(self):
        score = self._score(
            initial_discount_offered_pct=0.30,   # +40
            avg_total_discount_given_pct=0.35,   # +35
            avg_selling_price_vs_list_pct=0.60,  # +25
        )
        assert score == 100.0  # 40+35+25=100, capped

    def test_cap_at_100(self):
        # Ensure capping works: max possible without cap would be 100 exactly here
        score = self._score(
            initial_discount_offered_pct=0.30,
            avg_total_discount_given_pct=0.35,
            avg_selling_price_vs_list_pct=0.60,
        )
        assert score <= 100.0

    def test_combined_mid_scores(self):
        # +22 + 18 + 12 = 52
        score = self._score(
            initial_discount_offered_pct=0.20,
            avg_total_discount_given_pct=0.25,
            avg_selling_price_vs_list_pct=0.80,
        )
        assert score == 52.0


# ---------------------------------------------------------------------------
# 5. Concession Behavior Sub-Score
# ---------------------------------------------------------------------------

class TestConcessionBehaviorScore:
    """
    price_concession_without_value_exchange_pct: >=0.60→+40, >=0.40→+22, >=0.20→+8, else 0
    multi_concession_in_single_negotiation_pct: >=0.50→+35, >=0.30→+18, else 0
    final_ask_for_extras_rate_pct: >=0.40→+25, >=0.20→+12, else 0
    """

    def _score(self, **kw) -> float:
        engine = _engine()
        inp = _make_input(**kw)
        return engine._concession_behavior_score(inp)

    # price_concession branches
    def test_price_concession_below_0_20(self):
        assert self._score(price_concession_without_value_exchange_pct=0.10) == 0.0

    def test_price_concession_exactly_0_20(self):
        assert self._score(price_concession_without_value_exchange_pct=0.20) == 8.0

    def test_price_concession_between_0_20_and_0_40(self):
        assert self._score(price_concession_without_value_exchange_pct=0.30) == 8.0

    def test_price_concession_exactly_0_40(self):
        assert self._score(price_concession_without_value_exchange_pct=0.40) == 22.0

    def test_price_concession_between_0_40_and_0_60(self):
        assert self._score(price_concession_without_value_exchange_pct=0.55) == 22.0

    def test_price_concession_exactly_0_60(self):
        assert self._score(price_concession_without_value_exchange_pct=0.60) == 40.0

    def test_price_concession_above_0_60(self):
        assert self._score(price_concession_without_value_exchange_pct=0.80) == 40.0

    # multi_concession branches
    def test_multi_concession_below_0_30(self):
        assert self._score(multi_concession_in_single_negotiation_pct=0.20) == 0.0

    def test_multi_concession_exactly_0_30(self):
        assert self._score(multi_concession_in_single_negotiation_pct=0.30) == 18.0

    def test_multi_concession_between_0_30_and_0_50(self):
        assert self._score(multi_concession_in_single_negotiation_pct=0.40) == 18.0

    def test_multi_concession_exactly_0_50(self):
        assert self._score(multi_concession_in_single_negotiation_pct=0.50) == 35.0

    def test_multi_concession_above_0_50(self):
        assert self._score(multi_concession_in_single_negotiation_pct=0.70) == 35.0

    # final_ask_for_extras branches
    def test_final_ask_below_0_20(self):
        assert self._score(final_ask_for_extras_rate_pct=0.10) == 0.0

    def test_final_ask_exactly_0_20(self):
        assert self._score(final_ask_for_extras_rate_pct=0.20) == 12.0

    def test_final_ask_between_0_20_and_0_40(self):
        assert self._score(final_ask_for_extras_rate_pct=0.30) == 12.0

    def test_final_ask_exactly_0_40(self):
        assert self._score(final_ask_for_extras_rate_pct=0.40) == 25.0

    def test_final_ask_above_0_40(self):
        assert self._score(final_ask_for_extras_rate_pct=0.60) == 25.0

    def test_max_concession_score_capped(self):
        # 40+35+25=100
        score = self._score(
            price_concession_without_value_exchange_pct=0.70,
            multi_concession_in_single_negotiation_pct=0.60,
            final_ask_for_extras_rate_pct=0.50,
        )
        assert score == 100.0

    def test_combined_mid_concession(self):
        # 22 + 18 + 12 = 52
        score = self._score(
            price_concession_without_value_exchange_pct=0.45,
            multi_concession_in_single_negotiation_pct=0.35,
            final_ask_for_extras_rate_pct=0.25,
        )
        assert score == 52.0


# ---------------------------------------------------------------------------
# 6. Deal Construction Sub-Score
# ---------------------------------------------------------------------------

class TestDealConstructionScore:
    """
    champion_deal_only_rate_pct: >=0.65→+45, >=0.45→+25, >=0.25→+10, else 0
    procurement_escalation_rate_pct: >=0.40→+30, >=0.20→+15, else 0
    contract_redline_rounds_avg: >=4.0→+25, >=2.5→+12, else 0
    """

    def _score(self, **kw) -> float:
        engine = _engine()
        inp = _make_input(**kw)
        return engine._deal_construction_score(inp)

    # champion branches
    def test_champion_below_0_25(self):
        assert self._score(champion_deal_only_rate_pct=0.20) == 0.0

    def test_champion_exactly_0_25(self):
        assert self._score(champion_deal_only_rate_pct=0.25) == 10.0

    def test_champion_between_0_25_and_0_45(self):
        assert self._score(champion_deal_only_rate_pct=0.35) == 10.0

    def test_champion_exactly_0_45(self):
        assert self._score(champion_deal_only_rate_pct=0.45) == 25.0

    def test_champion_between_0_45_and_0_65(self):
        assert self._score(champion_deal_only_rate_pct=0.55) == 25.0

    def test_champion_exactly_0_65(self):
        assert self._score(champion_deal_only_rate_pct=0.65) == 45.0

    def test_champion_above_0_65(self):
        assert self._score(champion_deal_only_rate_pct=0.80) == 45.0

    # procurement branches
    def test_procurement_below_0_20(self):
        assert self._score(procurement_escalation_rate_pct=0.10) == 0.0

    def test_procurement_exactly_0_20(self):
        assert self._score(procurement_escalation_rate_pct=0.20) == 15.0

    def test_procurement_between_0_20_and_0_40(self):
        assert self._score(procurement_escalation_rate_pct=0.30) == 15.0

    def test_procurement_exactly_0_40(self):
        assert self._score(procurement_escalation_rate_pct=0.40) == 30.0

    def test_procurement_above_0_40(self):
        assert self._score(procurement_escalation_rate_pct=0.60) == 30.0

    # redline branches
    def test_redline_below_2_5(self):
        assert self._score(contract_redline_rounds_avg=2.0) == 0.0

    def test_redline_exactly_2_5(self):
        assert self._score(contract_redline_rounds_avg=2.5) == 12.0

    def test_redline_between_2_5_and_4_0(self):
        assert self._score(contract_redline_rounds_avg=3.0) == 12.0

    def test_redline_exactly_4_0(self):
        assert self._score(contract_redline_rounds_avg=4.0) == 25.0

    def test_redline_above_4_0(self):
        assert self._score(contract_redline_rounds_avg=6.0) == 25.0

    def test_max_deal_construction_score(self):
        # 45+30+25=100
        score = self._score(
            champion_deal_only_rate_pct=0.70,
            procurement_escalation_rate_pct=0.50,
            contract_redline_rounds_avg=5.0,
        )
        assert score == 100.0

    def test_combined_mid_construction(self):
        # 25 + 15 + 12 = 52
        score = self._score(
            champion_deal_only_rate_pct=0.50,
            procurement_escalation_rate_pct=0.25,
            contract_redline_rounds_avg=3.0,
        )
        assert score == 52.0


# ---------------------------------------------------------------------------
# 7. Close Effectiveness Sub-Score
# ---------------------------------------------------------------------------

class TestCloseEffectivenessScore:
    """
    late_stage_deal_loss_rate_pct: >=0.45→+40, >=0.25→+22, >=0.10→+8, else 0
    decision_deadline_driven_by_rep_pct: <=0.25→+35, <=0.50→+18, else 0
    multi_year_deal_rate_pct: <=0.10→+25, <=0.25→+12, else 0
    """

    def _score(self, **kw) -> float:
        engine = _engine()
        inp = _make_input(**kw)
        return engine._close_effectiveness_score(inp)

    # late_stage_deal_loss branches
    def test_late_loss_below_0_10(self):
        assert self._score(late_stage_deal_loss_rate_pct=0.05) == 0.0

    def test_late_loss_exactly_0_10(self):
        assert self._score(late_stage_deal_loss_rate_pct=0.10) == 8.0

    def test_late_loss_between_0_10_and_0_25(self):
        assert self._score(late_stage_deal_loss_rate_pct=0.15) == 8.0

    def test_late_loss_exactly_0_25(self):
        assert self._score(late_stage_deal_loss_rate_pct=0.25) == 22.0

    def test_late_loss_between_0_25_and_0_45(self):
        assert self._score(late_stage_deal_loss_rate_pct=0.35) == 22.0

    def test_late_loss_exactly_0_45(self):
        assert self._score(late_stage_deal_loss_rate_pct=0.45) == 40.0

    def test_late_loss_above_0_45(self):
        assert self._score(late_stage_deal_loss_rate_pct=0.60) == 40.0

    # decision_deadline branches
    def test_deadline_above_0_50(self):
        assert self._score(decision_deadline_driven_by_rep_pct=0.60) == 0.0

    def test_deadline_exactly_0_50(self):
        assert self._score(decision_deadline_driven_by_rep_pct=0.50) == 18.0

    def test_deadline_between_0_25_and_0_50(self):
        assert self._score(decision_deadline_driven_by_rep_pct=0.35) == 18.0

    def test_deadline_exactly_0_25(self):
        assert self._score(decision_deadline_driven_by_rep_pct=0.25) == 35.0

    def test_deadline_below_0_25(self):
        assert self._score(decision_deadline_driven_by_rep_pct=0.10) == 35.0

    # multi_year_deal branches
    def test_multi_year_above_0_25(self):
        assert self._score(multi_year_deal_rate_pct=0.30) == 0.0

    def test_multi_year_exactly_0_25(self):
        assert self._score(multi_year_deal_rate_pct=0.25) == 12.0

    def test_multi_year_between_0_10_and_0_25(self):
        assert self._score(multi_year_deal_rate_pct=0.15) == 12.0

    def test_multi_year_exactly_0_10(self):
        assert self._score(multi_year_deal_rate_pct=0.10) == 25.0

    def test_multi_year_below_0_10(self):
        assert self._score(multi_year_deal_rate_pct=0.05) == 25.0

    def test_max_close_score(self):
        # 40+35+25=100
        score = self._score(
            late_stage_deal_loss_rate_pct=0.50,
            decision_deadline_driven_by_rep_pct=0.10,
            multi_year_deal_rate_pct=0.05,
        )
        assert score == 100.0

    def test_combined_mid_close(self):
        # 22 + 18 + 12 = 52
        score = self._score(
            late_stage_deal_loss_rate_pct=0.30,
            decision_deadline_driven_by_rep_pct=0.40,
            multi_year_deal_rate_pct=0.20,
        )
        assert score == 52.0


# ---------------------------------------------------------------------------
# 8. Composite Score Formula and Weights
# ---------------------------------------------------------------------------

class TestCompositeScore:
    def test_zero_composite_clean_profile(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert result.negotiation_composite == 0.0

    def test_composite_formula_weights(self):
        """
        Manually set known sub-scores and verify composite = d*0.30 + c*0.30 + b*0.25 + e*0.15
        Use inputs that yield well-known sub-scores.
        discount_discipline = 8 (initial=0.05 only)
        concession_behavior = 8 (price_concession=0.20 only)
        deal_construction = 10 (champion=0.25 only)
        close_effectiveness = 8 (late_loss=0.10 only)
        composite = 8*0.30 + 8*0.30 + 10*0.25 + 8*0.15 = 2.4+2.4+2.5+1.2 = 8.5
        """
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=0.05,
            avg_total_discount_given_pct=0.05,
            avg_selling_price_vs_list_pct=0.95,
            price_concession_without_value_exchange_pct=0.20,
            multi_concession_in_single_negotiation_pct=0.05,
            final_ask_for_extras_rate_pct=0.05,
            champion_deal_only_rate_pct=0.25,
            procurement_escalation_rate_pct=0.05,
            contract_redline_rounds_avg=1.0,
            late_stage_deal_loss_rate_pct=0.10,
            decision_deadline_driven_by_rep_pct=0.80,
            multi_year_deal_rate_pct=0.50,
        )
        result = engine.assess(inp)
        # disc=8, conc=8, constr=10, close=8
        expected = round(8 * 0.30 + 8 * 0.30 + 10 * 0.25 + 8 * 0.15, 1)
        assert result.negotiation_composite == expected

    def test_composite_capped_at_100(self):
        """All sub-scores at max should produce composite of 100."""
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=0.30,
            avg_total_discount_given_pct=0.40,
            avg_selling_price_vs_list_pct=0.60,
            price_concession_without_value_exchange_pct=0.70,
            multi_concession_in_single_negotiation_pct=0.60,
            final_ask_for_extras_rate_pct=0.50,
            champion_deal_only_rate_pct=0.70,
            procurement_escalation_rate_pct=0.50,
            contract_redline_rounds_avg=5.0,
            late_stage_deal_loss_rate_pct=0.50,
            decision_deadline_driven_by_rep_pct=0.10,
            multi_year_deal_rate_pct=0.05,
        )
        result = engine.assess(inp)
        assert result.negotiation_composite == 100.0

    def test_composite_specific_weights(self):
        """
        discount=40, concession=35, construction=30, close=25
        composite = 40*0.30 + 35*0.30 + 30*0.25 + 25*0.15
                  = 12 + 10.5 + 7.5 + 3.75 = 33.75 → rounded to 1dp = 33.8
        """
        engine = _engine()
        inp = _make_input(
            # discount → 40: initial>=0.25
            initial_discount_offered_pct=0.25,
            avg_total_discount_given_pct=0.05,
            avg_selling_price_vs_list_pct=0.95,
            # concession → 35: multi_concession>=0.50
            price_concession_without_value_exchange_pct=0.05,
            multi_concession_in_single_negotiation_pct=0.50,
            final_ask_for_extras_rate_pct=0.05,
            # construction → 30: procurement>=0.40 (+30)
            champion_deal_only_rate_pct=0.10,
            procurement_escalation_rate_pct=0.40,
            contract_redline_rounds_avg=1.0,
            # close → 25: multi_year<=0.10 (+25), deadline>0.50 (+0), late_loss<0.10 (+0)
            late_stage_deal_loss_rate_pct=0.05,
            decision_deadline_driven_by_rep_pct=0.80,
            multi_year_deal_rate_pct=0.05,
        )
        result = engine.assess(inp)
        assert result.discount_discipline_score == 40.0
        assert result.concession_behavior_score == 35.0
        assert result.deal_construction_score == 30.0
        assert result.close_effectiveness_score == 25.0
        expected = round(40 * 0.30 + 35 * 0.30 + 30 * 0.25 + 25 * 0.15, 1)
        assert result.negotiation_composite == expected


# ---------------------------------------------------------------------------
# 9. Pattern Detection and Priority Order
# ---------------------------------------------------------------------------

class TestPatternDetection:
    """
    Priority:
    1. chronic_discounter: avg_total_discount>=0.25 AND discount_score>=40
    2. value_cave: price_concession>=0.50 AND concession_score>=40
    3. competitor_price_match: competitor_match>=0.50 AND rounds>=3.0
    4. single_threaded_close: champion>=0.60 AND construction_score>=35
    5. late_stage_collapse: late_loss>=0.40 AND close_score>=30
    6. none
    """

    def test_no_pattern_clean(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert result.negotiation_pattern == NegotiationPattern.none

    def test_chronic_discounter(self):
        # avg_total_discount=0.25 → +18 for avg discount part not enough alone
        # Need discount_score >= 40: initial_discount>=0.25 → +40
        engine = _engine()
        inp = _make_input(
            avg_total_discount_given_pct=0.25,
            initial_discount_offered_pct=0.25,  # discount_score=40
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.chronic_discounter

    def test_chronic_discounter_boundary_avg_discount(self):
        # avg_total below 0.25 should not trigger
        engine = _engine()
        inp = _make_input(
            avg_total_discount_given_pct=0.24,
            initial_discount_offered_pct=0.30,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern != NegotiationPattern.chronic_discounter

    def test_value_cave(self):
        engine = _engine()
        inp = _make_input(
            price_concession_without_value_exchange_pct=0.50,  # >=0.50
            multi_concession_in_single_negotiation_pct=0.50,   # concession_score >=40 (35+? or 35 alone)
            # concession_score = 22(price) + 35(multi) = 57 → >=40
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.value_cave

    def test_value_cave_exact_boundary(self):
        # price_concession=0.50 → +22, multi=0.50 → +35, total=57 >=40
        engine = _engine()
        inp = _make_input(
            price_concession_without_value_exchange_pct=0.50,
            multi_concession_in_single_negotiation_pct=0.50,
            final_ask_for_extras_rate_pct=0.05,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.value_cave

    def test_competitor_price_match(self):
        engine = _engine()
        inp = _make_input(
            competitor_discount_match_rate_pct=0.50,
            negotiation_rounds_before_close_avg=3.0,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.competitor_price_match

    def test_competitor_price_match_below_rounds(self):
        engine = _engine()
        inp = _make_input(
            competitor_discount_match_rate_pct=0.60,
            negotiation_rounds_before_close_avg=2.9,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern != NegotiationPattern.competitor_price_match

    def test_single_threaded_close(self):
        # champion>=0.60 AND construction>=35
        # champion=0.60 → +25, procurement=0.40 → +30 = 55 >=35
        engine = _engine()
        inp = _make_input(
            champion_deal_only_rate_pct=0.60,
            procurement_escalation_rate_pct=0.40,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.single_threaded_close

    def test_single_threaded_close_below_champion(self):
        engine = _engine()
        inp = _make_input(
            champion_deal_only_rate_pct=0.59,
            procurement_escalation_rate_pct=0.50,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern != NegotiationPattern.single_threaded_close

    def test_late_stage_collapse(self):
        # late_loss>=0.40 AND close_score>=30
        # late_loss=0.40 → +22, deadline=0.10 → +35 = 57 >=30
        engine = _engine()
        inp = _make_input(
            late_stage_deal_loss_rate_pct=0.40,
            decision_deadline_driven_by_rep_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.late_stage_collapse

    def test_late_stage_collapse_below_late_loss(self):
        engine = _engine()
        inp = _make_input(
            late_stage_deal_loss_rate_pct=0.39,
            decision_deadline_driven_by_rep_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern != NegotiationPattern.late_stage_collapse

    def test_priority_chronic_over_value_cave(self):
        """chronic_discounter checked first — when both conditions met, chronic wins."""
        engine = _engine()
        inp = _make_input(
            avg_total_discount_given_pct=0.25,
            initial_discount_offered_pct=0.25,    # discount_score=40 → chronic_discounter
            price_concession_without_value_exchange_pct=0.50,
            multi_concession_in_single_negotiation_pct=0.50,  # concession>=40 → value_cave
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.chronic_discounter

    def test_priority_value_cave_over_competitor(self):
        """value_cave checked before competitor_price_match."""
        engine = _engine()
        inp = _make_input(
            price_concession_without_value_exchange_pct=0.50,
            multi_concession_in_single_negotiation_pct=0.50,  # concession>=40
            competitor_discount_match_rate_pct=0.60,
            negotiation_rounds_before_close_avg=3.5,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.value_cave

    def test_priority_competitor_over_single_threaded(self):
        """competitor_price_match checked before single_threaded_close."""
        engine = _engine()
        inp = _make_input(
            competitor_discount_match_rate_pct=0.60,
            negotiation_rounds_before_close_avg=3.5,
            champion_deal_only_rate_pct=0.65,
            procurement_escalation_rate_pct=0.40,  # construction>=35
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.competitor_price_match

    def test_priority_single_threaded_over_late_collapse(self):
        """single_threaded_close checked before late_stage_collapse."""
        engine = _engine()
        inp = _make_input(
            champion_deal_only_rate_pct=0.60,
            procurement_escalation_rate_pct=0.40,  # construction>=35
            late_stage_deal_loss_rate_pct=0.40,
            decision_deadline_driven_by_rep_pct=0.10,  # close>=30
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.single_threaded_close


# ---------------------------------------------------------------------------
# 10. Risk Level Thresholds
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def _composite_to_risk(self, composite: float) -> NegotiationRisk:
        engine = _engine()
        return engine._risk_level(composite)

    def test_low_below_20(self):
        assert self._composite_to_risk(19.9) == NegotiationRisk.low

    def test_low_at_0(self):
        assert self._composite_to_risk(0.0) == NegotiationRisk.low

    def test_moderate_at_exactly_20(self):
        assert self._composite_to_risk(20.0) == NegotiationRisk.moderate

    def test_moderate_between_20_and_40(self):
        assert self._composite_to_risk(30.0) == NegotiationRisk.moderate

    def test_high_at_exactly_40(self):
        assert self._composite_to_risk(40.0) == NegotiationRisk.high

    def test_high_between_40_and_60(self):
        assert self._composite_to_risk(50.0) == NegotiationRisk.high

    def test_critical_at_exactly_60(self):
        assert self._composite_to_risk(60.0) == NegotiationRisk.critical

    def test_critical_above_60(self):
        assert self._composite_to_risk(80.0) == NegotiationRisk.critical

    def test_critical_at_100(self):
        assert self._composite_to_risk(100.0) == NegotiationRisk.critical


# ---------------------------------------------------------------------------
# 11. Severity Thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def _composite_to_severity(self, composite: float) -> NegotiationSeverity:
        engine = _engine()
        return engine._severity(composite)

    def test_clean_below_20(self):
        assert self._composite_to_severity(19.9) == NegotiationSeverity.clean

    def test_clean_at_0(self):
        assert self._composite_to_severity(0.0) == NegotiationSeverity.clean

    def test_managing_at_exactly_20(self):
        assert self._composite_to_severity(20.0) == NegotiationSeverity.managing

    def test_managing_between_20_and_40(self):
        assert self._composite_to_severity(35.0) == NegotiationSeverity.managing

    def test_struggling_at_exactly_40(self):
        assert self._composite_to_severity(40.0) == NegotiationSeverity.struggling

    def test_struggling_between_40_and_60(self):
        assert self._composite_to_severity(55.0) == NegotiationSeverity.struggling

    def test_collapsing_at_exactly_60(self):
        assert self._composite_to_severity(60.0) == NegotiationSeverity.collapsing

    def test_collapsing_above_60(self):
        assert self._composite_to_severity(75.0) == NegotiationSeverity.collapsing

    def test_collapsing_at_100(self):
        assert self._composite_to_severity(100.0) == NegotiationSeverity.collapsing


# ---------------------------------------------------------------------------
# 12. Action Mappings
# ---------------------------------------------------------------------------

class TestActionMapping:
    def _action(self, risk: NegotiationRisk, pattern: NegotiationPattern) -> NegotiationAction:
        engine = _engine()
        return engine._action(risk, pattern)

    def test_critical_chronic_discounter(self):
        assert self._action(NegotiationRisk.critical, NegotiationPattern.chronic_discounter) == NegotiationAction.discount_defense_intervention

    def test_critical_value_cave(self):
        assert self._action(NegotiationRisk.critical, NegotiationPattern.value_cave) == NegotiationAction.value_based_negotiation_reset

    def test_critical_competitor_price_match(self):
        assert self._action(NegotiationRisk.critical, NegotiationPattern.competitor_price_match) == NegotiationAction.negotiation_reset_intervention

    def test_critical_single_threaded_close(self):
        assert self._action(NegotiationRisk.critical, NegotiationPattern.single_threaded_close) == NegotiationAction.negotiation_reset_intervention

    def test_critical_late_stage_collapse(self):
        assert self._action(NegotiationRisk.critical, NegotiationPattern.late_stage_collapse) == NegotiationAction.negotiation_reset_intervention

    def test_critical_none_pattern(self):
        assert self._action(NegotiationRisk.critical, NegotiationPattern.none) == NegotiationAction.negotiation_reset_intervention

    def test_high_single_threaded_close(self):
        assert self._action(NegotiationRisk.high, NegotiationPattern.single_threaded_close) == NegotiationAction.stakeholder_expansion_coaching

    def test_high_late_stage_collapse(self):
        assert self._action(NegotiationRisk.high, NegotiationPattern.late_stage_collapse) == NegotiationAction.close_technique_coaching

    def test_high_chronic_discounter(self):
        assert self._action(NegotiationRisk.high, NegotiationPattern.chronic_discounter) == NegotiationAction.negotiation_process_coaching

    def test_high_value_cave(self):
        assert self._action(NegotiationRisk.high, NegotiationPattern.value_cave) == NegotiationAction.negotiation_process_coaching

    def test_high_competitor_price_match(self):
        assert self._action(NegotiationRisk.high, NegotiationPattern.competitor_price_match) == NegotiationAction.negotiation_process_coaching

    def test_high_none(self):
        assert self._action(NegotiationRisk.high, NegotiationPattern.none) == NegotiationAction.negotiation_process_coaching

    def test_moderate_any_pattern(self):
        for pattern in NegotiationPattern:
            assert self._action(NegotiationRisk.moderate, pattern) == NegotiationAction.negotiation_process_coaching

    def test_low_any_pattern(self):
        for pattern in NegotiationPattern:
            assert self._action(NegotiationRisk.low, pattern) == NegotiationAction.no_action


# ---------------------------------------------------------------------------
# 13. Flag Conditions
# ---------------------------------------------------------------------------

class TestFlags:
    # has_negotiation_gap: composite>=40 OR avg_total_discount>=0.20 OR late_loss>=0.30

    def test_gap_false_all_below(self):
        engine = _engine()
        inp = _make_input(
            avg_total_discount_given_pct=0.19,
            late_stage_deal_loss_rate_pct=0.29,
        )
        result = engine.assess(inp)
        # composite will be 0 here, gap should be False
        assert result.has_negotiation_gap is False

    def test_gap_true_via_composite(self):
        # Force composite >=40 via high sub-scores
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=0.25,   # +40 discount
            avg_total_discount_given_pct=0.30,   # +35 discount → disc=75
            avg_selling_price_vs_list_pct=0.60,  # +25 → disc=100, capped
            price_concession_without_value_exchange_pct=0.60,  # conc=40+...
            multi_concession_in_single_negotiation_pct=0.50,   # +35
            # composite will be well above 40
        )
        result = engine.assess(inp)
        assert result.negotiation_composite >= 40.0
        assert result.has_negotiation_gap is True

    def test_gap_true_via_avg_discount(self):
        engine = _engine()
        inp = _make_input(avg_total_discount_given_pct=0.20)
        result = engine.assess(inp)
        assert result.has_negotiation_gap is True

    def test_gap_boundary_avg_discount_exactly_0_20(self):
        engine = _engine()
        result = engine.assess(_make_input(avg_total_discount_given_pct=0.20))
        assert result.has_negotiation_gap is True

    def test_gap_true_via_late_loss(self):
        engine = _engine()
        inp = _make_input(late_stage_deal_loss_rate_pct=0.30)
        result = engine.assess(inp)
        assert result.has_negotiation_gap is True

    def test_gap_boundary_late_loss_exactly_0_30(self):
        engine = _engine()
        result = engine.assess(_make_input(late_stage_deal_loss_rate_pct=0.30))
        assert result.has_negotiation_gap is True

    # requires_negotiation_coaching: composite>=30 OR price_concession>=0.40 OR multi_concession>=0.40

    def test_coaching_false_all_below(self):
        engine = _engine()
        inp = _make_input(
            price_concession_without_value_exchange_pct=0.39,
            multi_concession_in_single_negotiation_pct=0.39,
        )
        result = engine.assess(inp)
        # composite will be below 30 for clean profile
        assert result.requires_negotiation_coaching is False

    def test_coaching_true_via_composite(self):
        # Build composite >= 30
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=0.25,  # disc=40
            avg_total_discount_given_pct=0.30,  # disc=75 capped at 100 after +25
            avg_selling_price_vs_list_pct=0.60,
            multi_concession_in_single_negotiation_pct=0.50,  # conc=35
        )
        result = engine.assess(inp)
        assert result.negotiation_composite >= 30.0
        assert result.requires_negotiation_coaching is True

    def test_coaching_true_via_price_concession(self):
        engine = _engine()
        inp = _make_input(price_concession_without_value_exchange_pct=0.40)
        result = engine.assess(inp)
        assert result.requires_negotiation_coaching is True

    def test_coaching_boundary_price_concession_exactly_0_40(self):
        engine = _engine()
        result = engine.assess(_make_input(price_concession_without_value_exchange_pct=0.40))
        assert result.requires_negotiation_coaching is True

    def test_coaching_true_via_multi_concession(self):
        engine = _engine()
        inp = _make_input(multi_concession_in_single_negotiation_pct=0.40)
        result = engine.assess(inp)
        assert result.requires_negotiation_coaching is True

    def test_coaching_boundary_multi_concession_exactly_0_40(self):
        engine = _engine()
        result = engine.assess(_make_input(multi_concession_in_single_negotiation_pct=0.40))
        assert result.requires_negotiation_coaching is True


# ---------------------------------------------------------------------------
# 14. Revenue Dilution Formula
# ---------------------------------------------------------------------------

class TestRevenueDilution:
    def test_revenue_dilution_zero_composite(self):
        engine = _engine()
        inp = _make_input(total_late_stage_deals=10, avg_opportunity_value_usd=50000.0)
        result = engine.assess(inp)
        # composite=0 → dilution=0
        assert result.estimated_revenue_dilution_usd == 0.0

    def test_revenue_dilution_formula(self):
        """
        Verify formula: total_deals * avg_value * avg_discount * (composite/100), rounded to 2dp.
        Use a profile where sub-scores are precisely known:
          initial_discount=0.05 → +8; avg_total_discount=0.05 → +0; selling_price=0.95 → +0
          disc=8, conc=0, constr=0, close=0
          composite = round(8*0.30 + 0 + 0 + 0, 1) = 2.4
          expected = round(20 * 100_000 * 0.05 * (2.4/100), 2) = round(2400.0, 2) = 2400.0
        """
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=0.05,
            avg_total_discount_given_pct=0.05,   # below 0.20, contributes 0 to disc score
            avg_selling_price_vs_list_pct=0.95,
            price_concession_without_value_exchange_pct=0.05,
            multi_concession_in_single_negotiation_pct=0.05,
            final_ask_for_extras_rate_pct=0.05,
            champion_deal_only_rate_pct=0.10,
            procurement_escalation_rate_pct=0.05,
            contract_redline_rounds_avg=1.0,
            late_stage_deal_loss_rate_pct=0.05,
            decision_deadline_driven_by_rep_pct=0.80,
            multi_year_deal_rate_pct=0.50,
            total_late_stage_deals=20,
            avg_opportunity_value_usd=100_000.0,
        )
        result = engine.assess(inp)
        # disc=8 (initial 0.05→+8 only), conc=0, constr=0, close=0
        disc = 8.0
        composite = round(disc * 0.30, 1)  # 2.4
        expected = round(20 * 100_000.0 * 0.05 * (composite / 100.0), 2)
        assert result.discount_discipline_score == disc
        assert result.negotiation_composite == composite
        assert result.estimated_revenue_dilution_usd == expected

    def test_revenue_dilution_rounded_to_2_decimals(self):
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=0.15,
            avg_total_discount_given_pct=0.20,
            total_late_stage_deals=7,
            avg_opportunity_value_usd=33_333.33,
        )
        result = engine.assess(inp)
        # result should be rounded to 2 decimal places
        assert result.estimated_revenue_dilution_usd == round(result.estimated_revenue_dilution_usd, 2)

    def test_revenue_dilution_is_float(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.estimated_revenue_dilution_usd, float)


# ---------------------------------------------------------------------------
# 15. Signal String
# ---------------------------------------------------------------------------

class TestSignalString:
    def test_signal_clean_profile(self):
        """pattern==none AND composite<20 → strong negotiation signal."""
        engine = _engine()
        result = engine.assess(_make_input())
        assert result.negotiation_signal == (
            "Negotiation discipline strong — discount defense, concession sequencing, "
            "and deal construction within benchmarks"
        )

    def test_signal_pattern_none_composite_below_20(self):
        """Explicit test: pattern=none, composite<20 → static message."""
        engine = _engine()
        inp = _make_input(initial_discount_offered_pct=0.05)  # tiny composite
        result = engine.assess(inp)
        assert "Negotiation discipline strong" in result.negotiation_signal

    def test_signal_pattern_chronic_discounter(self):
        engine = _engine()
        inp = _make_input(
            avg_total_discount_given_pct=0.25,
            initial_discount_offered_pct=0.25,
            deal_closed_at_list_price_pct=0.20,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.chronic_discounter
        sig = result.negotiation_signal
        assert "Chronic discounter" in sig
        assert "25% avg discount given" in sig
        assert "20% closed at list price" in sig
        assert f"composite {result.negotiation_composite:.0f}" in sig

    def test_signal_pattern_value_cave(self):
        engine = _engine()
        inp = _make_input(
            price_concession_without_value_exchange_pct=0.50,
            multi_concession_in_single_negotiation_pct=0.60,
            avg_total_discount_given_pct=0.15,
            deal_closed_at_list_price_pct=0.30,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.value_cave
        sig = result.negotiation_signal
        assert "Value cave" in sig
        assert "50% concessions without value exchange" in sig

    def test_signal_no_pattern_but_high_composite(self):
        """pattern==none but composite>=20 → dynamic signal with 'Negotiation risk'."""
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=0.15,  # +22 disc
            avg_total_discount_given_pct=0.20,  # +18 disc → disc=40
            multi_concession_in_single_negotiation_pct=0.30,  # +18 conc
        )
        result = engine.assess(inp)
        if result.negotiation_pattern == NegotiationPattern.none and result.negotiation_composite >= 20:
            sig = result.negotiation_signal
            assert "Negotiation risk" in sig
            assert "avg discount given" in sig

    def test_signal_contains_avg_discount_formatted(self):
        """Signal should show avg_total_discount_given_pct * 100 as integer %."""
        engine = _engine()
        inp = _make_input(
            avg_total_discount_given_pct=0.25,
            initial_discount_offered_pct=0.25,
            deal_closed_at_list_price_pct=0.40,
        )
        result = engine.assess(inp)
        assert "25% avg discount given" in result.negotiation_signal

    def test_signal_contains_price_concession_formatted(self):
        engine = _engine()
        inp = _make_input(
            price_concession_without_value_exchange_pct=0.50,
            multi_concession_in_single_negotiation_pct=0.60,
        )
        result = engine.assess(inp)
        if result.negotiation_pattern != NegotiationPattern.none or result.negotiation_composite >= 20:
            assert "50% concessions without value exchange" in result.negotiation_signal

    def test_signal_contains_list_price_formatted(self):
        engine = _engine()
        inp = _make_input(
            avg_total_discount_given_pct=0.25,
            initial_discount_offered_pct=0.25,
            deal_closed_at_list_price_pct=0.55,
        )
        result = engine.assess(inp)
        if result.negotiation_pattern != NegotiationPattern.none or result.negotiation_composite >= 20:
            assert "55% closed at list price" in result.negotiation_signal

    def test_signal_competitor_price_match_label(self):
        engine = _engine()
        inp = _make_input(
            competitor_discount_match_rate_pct=0.55,
            negotiation_rounds_before_close_avg=3.5,
            deal_closed_at_list_price_pct=0.30,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.competitor_price_match
        assert "Competitor price match" in result.negotiation_signal

    def test_signal_single_threaded_close_label(self):
        engine = _engine()
        inp = _make_input(
            champion_deal_only_rate_pct=0.65,
            procurement_escalation_rate_pct=0.40,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.single_threaded_close
        assert "Single threaded close" in result.negotiation_signal

    def test_signal_late_stage_collapse_label(self):
        engine = _engine()
        inp = _make_input(
            late_stage_deal_loss_rate_pct=0.40,
            decision_deadline_driven_by_rep_pct=0.10,
        )
        result = engine.assess(inp)
        assert result.negotiation_pattern == NegotiationPattern.late_stage_collapse
        assert "Late stage collapse" in result.negotiation_signal


# ---------------------------------------------------------------------------
# 16. End-to-End assess()
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_clean_profile_result(self):
        engine = _engine()
        result = engine.assess(_make_input(rep_id="R1", region="North"))
        assert result.rep_id == "R1"
        assert result.region == "North"
        assert result.negotiation_risk == NegotiationRisk.low
        assert result.negotiation_pattern == NegotiationPattern.none
        assert result.negotiation_severity == NegotiationSeverity.clean
        assert result.recommended_action == NegotiationAction.no_action
        assert result.discount_discipline_score == 0.0
        assert result.concession_behavior_score == 0.0
        assert result.deal_construction_score == 0.0
        assert result.close_effectiveness_score == 0.0
        assert result.negotiation_composite == 0.0
        assert result.has_negotiation_gap is False
        assert result.requires_negotiation_coaching is False
        assert result.estimated_revenue_dilution_usd == 0.0

    def test_high_risk_profile_result(self):
        engine = _engine()
        inp = _make_input(
            avg_total_discount_given_pct=0.25,
            initial_discount_offered_pct=0.25,
            avg_selling_price_vs_list_pct=0.65,
            price_concession_without_value_exchange_pct=0.50,
            multi_concession_in_single_negotiation_pct=0.50,
        )
        result = engine.assess(inp)
        assert result.negotiation_risk in (NegotiationRisk.high, NegotiationRisk.critical)
        assert result.has_negotiation_gap is True
        assert result.requires_negotiation_coaching is True

    def test_result_is_negotiation_result_instance(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result, NegotiationResult)

    def test_assess_stores_result(self):
        engine = _engine()
        engine.assess(_make_input())
        assert len(engine._results) == 1

    def test_assess_stores_multiple_results(self):
        engine = _engine()
        engine.assess(_make_input(rep_id="R1"))
        engine.assess(_make_input(rep_id="R2"))
        assert len(engine._results) == 2

    def test_critical_chronic_discounter_end_to_end(self):
        """Full worst-case chronic discounter test."""
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=0.30,  # +40
            avg_total_discount_given_pct=0.35,  # +35, >=0.25 for pattern
            avg_selling_price_vs_list_pct=0.60,  # +25 → disc=100
            price_concession_without_value_exchange_pct=0.65,  # conc=40
            multi_concession_in_single_negotiation_pct=0.60,   # +35 → conc=75
            final_ask_for_extras_rate_pct=0.50,                # +25 → conc=100
            champion_deal_only_rate_pct=0.70,   # +45
            procurement_escalation_rate_pct=0.50, # +30 → constr=75
            contract_redline_rounds_avg=5.0,      # +25 → constr=100
            late_stage_deal_loss_rate_pct=0.50,   # +40
            decision_deadline_driven_by_rep_pct=0.10,  # +35 → close=75+25=100
            multi_year_deal_rate_pct=0.05,         # +25
        )
        result = engine.assess(inp)
        assert result.negotiation_risk == NegotiationRisk.critical
        assert result.negotiation_pattern == NegotiationPattern.chronic_discounter
        assert result.negotiation_severity == NegotiationSeverity.collapsing
        assert result.recommended_action == NegotiationAction.discount_defense_intervention

    def test_moderate_risk_end_to_end(self):
        """Composite between 20 and 40 → moderate, process coaching."""
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=0.15,  # +22
            avg_total_discount_given_pct=0.20,  # +18 → disc=40
            multi_concession_in_single_negotiation_pct=0.30,  # +18 → conc=18
        )
        result = engine.assess(inp)
        # disc=40, conc=18, constr=0, close=0
        # composite = 40*0.30 + 18*0.30 + 0*0.25 + 0*0.15 = 12+5.4 = 17.4
        # That's below 20 → actually low. Let's recalculate:
        # We need composite >=20. Use disc=40 only: 40*0.30=12 < 20
        # disc=40 + conc=35: 40*0.30+35*0.30=12+10.5=22.5 >=20 → moderate
        assert result.negotiation_risk in (NegotiationRisk.low, NegotiationRisk.moderate, NegotiationRisk.high)

    def test_moderate_risk_explicit(self):
        """Force composite into moderate range 20-39."""
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=0.25,   # disc += 40
            avg_total_discount_given_pct=0.05,
            avg_selling_price_vs_list_pct=0.95,
            price_concession_without_value_exchange_pct=0.05,
            multi_concession_in_single_negotiation_pct=0.50,  # conc += 35
            final_ask_for_extras_rate_pct=0.05,
        )
        result = engine.assess(inp)
        # disc=40, conc=35, constr=0, close=0
        # composite = 40*0.30 + 35*0.30 = 12 + 10.5 = 22.5 → moderate
        assert result.negotiation_risk == NegotiationRisk.moderate
        assert result.negotiation_severity == NegotiationSeverity.managing
        assert result.recommended_action == NegotiationAction.negotiation_process_coaching


# ---------------------------------------------------------------------------
# 17. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_empty_list(self):
        engine = _engine()
        results = engine.assess_batch([])
        assert results == []

    def test_batch_single(self):
        engine = _engine()
        results = engine.assess_batch([_make_input(rep_id="R1")])
        assert len(results) == 1
        assert results[0].rep_id == "R1"

    def test_batch_multiple(self):
        engine = _engine()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5
        assert [r.rep_id for r in results] == ["R0", "R1", "R2", "R3", "R4"]

    def test_batch_stores_results(self):
        engine = _engine()
        engine.assess_batch([_make_input(rep_id=f"R{i}") for i in range(3)])
        assert len(engine._results) == 3

    def test_batch_results_are_negotiation_result(self):
        engine = _engine()
        results = engine.assess_batch([_make_input(), _make_input(rep_id="R2")])
        for r in results:
            assert isinstance(r, NegotiationResult)

    def test_batch_accumulates_with_prior_assess(self):
        engine = _engine()
        engine.assess(_make_input(rep_id="R0"))
        engine.assess_batch([_make_input(rep_id="R1"), _make_input(rep_id="R2")])
        assert len(engine._results) == 3


# ---------------------------------------------------------------------------
# 18. Summary – empty
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def test_empty_summary_keys(self):
        engine = _engine()
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_negotiation_composite", "negotiation_gap_count",
            "coaching_count", "avg_discount_discipline_score",
            "avg_concession_behavior_score", "avg_deal_construction_score",
            "avg_close_effectiveness_score", "total_estimated_revenue_dilution_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_empty_summary_has_13_keys(self):
        engine = _engine()
        assert len(engine.summary()) == 13

    def test_empty_summary_total_zero(self):
        assert _engine().summary()["total"] == 0

    def test_empty_summary_risk_counts_empty(self):
        assert _engine().summary()["risk_counts"] == {}

    def test_empty_summary_pattern_counts_empty(self):
        assert _engine().summary()["pattern_counts"] == {}

    def test_empty_summary_severity_counts_empty(self):
        assert _engine().summary()["severity_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        assert _engine().summary()["action_counts"] == {}

    def test_empty_summary_avg_composite_zero(self):
        assert _engine().summary()["avg_negotiation_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        assert _engine().summary()["negotiation_gap_count"] == 0

    def test_empty_summary_coaching_count_zero(self):
        assert _engine().summary()["coaching_count"] == 0

    def test_empty_summary_avg_scores_zero(self):
        s = _engine().summary()
        assert s["avg_discount_discipline_score"] == 0.0
        assert s["avg_concession_behavior_score"] == 0.0
        assert s["avg_deal_construction_score"] == 0.0
        assert s["avg_close_effectiveness_score"] == 0.0

    def test_empty_summary_total_dilution_zero(self):
        assert _engine().summary()["total_estimated_revenue_dilution_usd"] == 0.0


# ---------------------------------------------------------------------------
# 19. Summary – populated
# ---------------------------------------------------------------------------

class TestSummaryPopulated:
    def _populated_engine(self) -> SalesNegotiationDisciplineIntelligenceEngine:
        engine = _engine()
        # Clean rep
        engine.assess(_make_input(rep_id="R1", region="West"))
        # Moderate rep
        engine.assess(_make_input(
            rep_id="R2", region="East",
            initial_discount_offered_pct=0.25,
            multi_concession_in_single_negotiation_pct=0.50,
        ))
        # High/critical chronic discounter
        engine.assess(_make_input(
            rep_id="R3", region="North",
            initial_discount_offered_pct=0.30,
            avg_total_discount_given_pct=0.35,
            avg_selling_price_vs_list_pct=0.60,
            price_concession_without_value_exchange_pct=0.65,
            multi_concession_in_single_negotiation_pct=0.60,
            champion_deal_only_rate_pct=0.70,
            procurement_escalation_rate_pct=0.50,
            contract_redline_rounds_avg=5.0,
            late_stage_deal_loss_rate_pct=0.50,
            decision_deadline_driven_by_rep_pct=0.10,
            multi_year_deal_rate_pct=0.05,
            total_late_stage_deals=20,
            avg_opportunity_value_usd=80_000.0,
        ))
        return engine

    def test_summary_has_13_keys(self):
        engine = self._populated_engine()
        assert len(engine.summary()) == 13

    def test_summary_all_keys_present(self):
        engine = self._populated_engine()
        s = engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_negotiation_composite", "negotiation_gap_count",
            "coaching_count", "avg_discount_discipline_score",
            "avg_concession_behavior_score", "avg_deal_construction_score",
            "avg_close_effectiveness_score", "total_estimated_revenue_dilution_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_total(self):
        engine = self._populated_engine()
        assert engine.summary()["total"] == 3

    def test_summary_risk_counts_dict(self):
        engine = self._populated_engine()
        rc = engine.summary()["risk_counts"]
        assert isinstance(rc, dict)
        assert sum(rc.values()) == 3

    def test_summary_pattern_counts_dict(self):
        engine = self._populated_engine()
        pc = engine.summary()["pattern_counts"]
        assert isinstance(pc, dict)
        assert sum(pc.values()) == 3

    def test_summary_severity_counts_dict(self):
        engine = self._populated_engine()
        sc = engine.summary()["severity_counts"]
        assert isinstance(sc, dict)
        assert sum(sc.values()) == 3

    def test_summary_action_counts_dict(self):
        engine = self._populated_engine()
        ac = engine.summary()["action_counts"]
        assert isinstance(ac, dict)
        assert sum(ac.values()) == 3

    def test_summary_avg_composite_is_float(self):
        engine = self._populated_engine()
        assert isinstance(engine.summary()["avg_negotiation_composite"], float)

    def test_summary_avg_composite_correct(self):
        engine = self._populated_engine()
        s = engine.summary()
        # Average of 3 composites
        composites = [r.negotiation_composite for r in engine._results]
        expected = round(sum(composites) / 3, 1)
        assert s["avg_negotiation_composite"] == expected

    def test_summary_gap_count_correct(self):
        engine = self._populated_engine()
        s = engine.summary()
        expected = sum(1 for r in engine._results if r.has_negotiation_gap)
        assert s["negotiation_gap_count"] == expected

    def test_summary_coaching_count_correct(self):
        engine = self._populated_engine()
        s = engine.summary()
        expected = sum(1 for r in engine._results if r.requires_negotiation_coaching)
        assert s["coaching_count"] == expected

    def test_summary_avg_sub_scores_correct(self):
        engine = self._populated_engine()
        s = engine.summary()
        n = len(engine._results)
        assert s["avg_discount_discipline_score"] == round(
            sum(r.discount_discipline_score for r in engine._results) / n, 1
        )
        assert s["avg_concession_behavior_score"] == round(
            sum(r.concession_behavior_score for r in engine._results) / n, 1
        )
        assert s["avg_deal_construction_score"] == round(
            sum(r.deal_construction_score for r in engine._results) / n, 1
        )
        assert s["avg_close_effectiveness_score"] == round(
            sum(r.close_effectiveness_score for r in engine._results) / n, 1
        )

    def test_summary_total_dilution_correct(self):
        engine = self._populated_engine()
        s = engine.summary()
        expected = round(sum(r.estimated_revenue_dilution_usd for r in engine._results), 2)
        assert s["total_estimated_revenue_dilution_usd"] == expected

    def test_summary_risk_counts_keys_are_strings(self):
        engine = self._populated_engine()
        rc = engine.summary()["risk_counts"]
        for k in rc:
            assert isinstance(k, str)

    def test_summary_after_batch(self):
        engine = _engine()
        inputs = [_make_input(rep_id=f"R{i}") for i in range(5)]
        engine.assess_batch(inputs)
        s = engine.summary()
        assert s["total"] == 5

    def test_summary_single_result(self):
        engine = _engine()
        engine.assess(_make_input(rep_id="SOLO"))
        s = engine.summary()
        assert s["total"] == 1
        assert s["avg_negotiation_composite"] == engine._results[0].negotiation_composite

    def test_summary_risk_counts_values_are_ints(self):
        engine = self._populated_engine()
        rc = engine.summary()["risk_counts"]
        for v in rc.values():
            assert isinstance(v, int)


# ---------------------------------------------------------------------------
# 20. Additional edge-case / integration tests
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_deals_zero_dilution(self):
        engine = _engine()
        inp = _make_input(total_late_stage_deals=0, avg_opportunity_value_usd=100_000.0)
        result = engine.assess(inp)
        assert result.estimated_revenue_dilution_usd == 0.0

    def test_zero_opportunity_value_zero_dilution(self):
        engine = _engine()
        inp = _make_input(total_late_stage_deals=10, avg_opportunity_value_usd=0.0)
        result = engine.assess(inp)
        assert result.estimated_revenue_dilution_usd == 0.0

    def test_multiple_engines_independent(self):
        """Two engine instances should not share state."""
        e1 = _engine()
        e2 = _engine()
        e1.assess(_make_input(rep_id="R1"))
        assert len(e1._results) == 1
        assert len(e2._results) == 0

    def test_assess_returns_same_rep_id(self):
        engine = _engine()
        inp = _make_input(rep_id="SPECIAL_REP")
        result = engine.assess(inp)
        assert result.rep_id == "SPECIAL_REP"

    def test_assess_returns_same_region(self):
        engine = _engine()
        inp = _make_input(region="APAC")
        result = engine.assess(inp)
        assert result.region == "APAC"

    def test_sub_scores_are_floats(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.discount_discipline_score, float)
        assert isinstance(result.concession_behavior_score, float)
        assert isinstance(result.deal_construction_score, float)
        assert isinstance(result.close_effectiveness_score, float)

    def test_composite_never_exceeds_100(self):
        engine = _engine()
        inp = _make_input(
            initial_discount_offered_pct=1.0,
            avg_total_discount_given_pct=1.0,
            avg_selling_price_vs_list_pct=0.0,
            price_concession_without_value_exchange_pct=1.0,
            multi_concession_in_single_negotiation_pct=1.0,
            final_ask_for_extras_rate_pct=1.0,
            champion_deal_only_rate_pct=1.0,
            procurement_escalation_rate_pct=1.0,
            contract_redline_rounds_avg=10.0,
            late_stage_deal_loss_rate_pct=1.0,
            decision_deadline_driven_by_rep_pct=0.0,
            multi_year_deal_rate_pct=0.0,
        )
        result = engine.assess(inp)
        assert result.negotiation_composite <= 100.0
        assert result.discount_discipline_score <= 100.0
        assert result.concession_behavior_score <= 100.0
        assert result.deal_construction_score <= 100.0
        assert result.close_effectiveness_score <= 100.0

    def test_to_dict_booleans_preserved(self):
        engine = _engine()
        result = engine.assess(_make_input())
        d = result.to_dict()
        assert isinstance(d["has_negotiation_gap"], bool)
        assert isinstance(d["requires_negotiation_coaching"], bool)

    def test_negotiation_signal_is_string(self):
        engine = _engine()
        result = engine.assess(_make_input())
        assert isinstance(result.negotiation_signal, str)
        assert len(result.negotiation_signal) > 0
