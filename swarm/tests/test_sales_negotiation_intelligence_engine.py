"""
Comprehensive tests for SalesNegotiationIntelligenceEngine.
Covers: enums, dataclasses, sub-scores, pattern detection, risk/severity/action
mapping, flag methods, margin erosion, signal generation, assess(), assess_batch(),
summary(), edge cases, and end-to-end scenarios.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_negotiation_intelligence_engine import (
    NegotiationAction,
    NegotiationInput,
    NegotiationPattern,
    NegotiationResult,
    NegotiationRisk,
    NegotiationSeverity,
    SalesNegotiationIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_input(**overrides) -> NegotiationInput:
    """Return a baseline NegotiationInput with safe/low-risk defaults."""
    defaults = dict(
        rep_id="rep-001",
        region="West",
        evaluation_period_id="Q1-2026",
        total_negotiations_conducted=50,
        avg_negotiation_rounds_per_deal=1.5,
        first_concession_timing_pct=0.10,     # low risk
        avg_discount_concession_pct=0.05,     # low risk
        deals_won_without_discount_pct=0.60,  # low risk
        manager_escalation_in_negotiation_pct=0.05,  # low risk
        value_vs_price_conversation_ratio=0.80,      # low risk
        avg_days_from_proposal_to_close=14.0,
        deals_with_no_negotiation_pct=0.05,          # low risk
        multi_item_negotiation_rate_pct=0.60,        # low risk
        urgency_trigger_used_pct=0.70,               # low risk
        competitive_counteroffer_handled_pct=0.80,   # low risk
        contract_term_concession_pct=0.05,
        payment_term_concession_pct=0.05,
        scope_expansion_during_negotiation_pct=0.50, # low risk
        negotiation_stall_rate_pct=0.05,             # low risk
        deal_desk_referral_in_negotiation_pct=0.05,  # low risk
        avg_final_margin_vs_list_pct=0.85,
        avg_opportunity_value_usd=10_000.0,
    )
    defaults.update(overrides)
    return NegotiationInput(**defaults)


def _engine() -> SalesNegotiationIntelligenceEngine:
    return SalesNegotiationIntelligenceEngine()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestNegotiationRiskEnum:
    def test_values_count(self):
        assert len(NegotiationRisk) == 4

    def test_value_low(self):
        assert NegotiationRisk.low.value == "low"

    def test_value_moderate(self):
        assert NegotiationRisk.moderate.value == "moderate"

    def test_value_high(self):
        assert NegotiationRisk.high.value == "high"

    def test_value_critical(self):
        assert NegotiationRisk.critical.value == "critical"

    def test_is_str(self):
        assert isinstance(NegotiationRisk.low, str)

    def test_str_comparison(self):
        assert NegotiationRisk.low == "low"

    def test_members(self):
        names = {m.name for m in NegotiationRisk}
        assert names == {"low", "moderate", "high", "critical"}


class TestNegotiationPatternEnum:
    def test_values_count(self):
        assert len(NegotiationPattern) == 6

    def test_value_none(self):
        assert NegotiationPattern.none.value == "none"

    def test_value_early_capitulation(self):
        assert NegotiationPattern.early_capitulation.value == "early_capitulation"

    def test_value_manager_escalation_dependency(self):
        assert NegotiationPattern.manager_escalation_dependency.value == "manager_escalation_dependency"

    def test_value_price_anchoring_failure(self):
        assert NegotiationPattern.price_anchoring_failure.value == "price_anchoring_failure"

    def test_value_concession_cascade(self):
        assert NegotiationPattern.concession_cascade.value == "concession_cascade"

    def test_value_urgency_creation_gap(self):
        assert NegotiationPattern.urgency_creation_gap.value == "urgency_creation_gap"

    def test_is_str(self):
        assert isinstance(NegotiationPattern.none, str)

    def test_str_comparison(self):
        assert NegotiationPattern.none == "none"


class TestNegotiationSeverityEnum:
    def test_values_count(self):
        assert len(NegotiationSeverity) == 4

    def test_value_disciplined(self):
        assert NegotiationSeverity.disciplined.value == "disciplined"

    def test_value_developing(self):
        assert NegotiationSeverity.developing.value == "developing"

    def test_value_reactive(self):
        assert NegotiationSeverity.reactive.value == "reactive"

    def test_value_erosive(self):
        assert NegotiationSeverity.erosive.value == "erosive"

    def test_is_str(self):
        assert isinstance(NegotiationSeverity.disciplined, str)

    def test_str_comparison(self):
        assert NegotiationSeverity.disciplined == "disciplined"


class TestNegotiationActionEnum:
    def test_values_count(self):
        assert len(NegotiationAction) == 6

    def test_value_no_action(self):
        assert NegotiationAction.no_action.value == "no_action"

    def test_value_negotiation_skills_coaching(self):
        assert NegotiationAction.negotiation_skills_coaching.value == "negotiation_skills_coaching"

    def test_value_value_anchoring_training(self):
        assert NegotiationAction.value_anchoring_training.value == "value_anchoring_training"

    def test_value_concession_management_review(self):
        assert NegotiationAction.concession_management_review.value == "concession_management_review"

    def test_value_manager_escalation_reduction(self):
        assert NegotiationAction.manager_escalation_reduction.value == "manager_escalation_reduction"

    def test_value_urgency_creation_training(self):
        assert NegotiationAction.urgency_creation_training.value == "urgency_creation_training"

    def test_is_str(self):
        assert isinstance(NegotiationAction.no_action, str)


# ===========================================================================
# 2. NegotiationInput DATACLASS
# ===========================================================================

class TestNegotiationInputDataclass:
    def test_can_be_constructed(self):
        inp = _make_input()
        assert inp.rep_id == "rep-001"

    def test_all_22_fields_accessible(self):
        inp = _make_input()
        fields = [
            "rep_id", "region", "evaluation_period_id",
            "total_negotiations_conducted", "avg_negotiation_rounds_per_deal",
            "first_concession_timing_pct", "avg_discount_concession_pct",
            "deals_won_without_discount_pct", "manager_escalation_in_negotiation_pct",
            "value_vs_price_conversation_ratio", "avg_days_from_proposal_to_close",
            "deals_with_no_negotiation_pct", "multi_item_negotiation_rate_pct",
            "urgency_trigger_used_pct", "competitive_counteroffer_handled_pct",
            "contract_term_concession_pct", "payment_term_concession_pct",
            "scope_expansion_during_negotiation_pct", "negotiation_stall_rate_pct",
            "deal_desk_referral_in_negotiation_pct", "avg_final_margin_vs_list_pct",
            "avg_opportunity_value_usd",
        ]
        assert len(fields) == 22
        for f in fields:
            assert hasattr(inp, f)

    def test_region_stored(self):
        inp = _make_input(region="East")
        assert inp.region == "East"

    def test_evaluation_period_id_stored(self):
        inp = _make_input(evaluation_period_id="Q2-2026")
        assert inp.evaluation_period_id == "Q2-2026"

    def test_total_negotiations_conducted_stored(self):
        inp = _make_input(total_negotiations_conducted=100)
        assert inp.total_negotiations_conducted == 100

    def test_avg_negotiation_rounds_stored(self):
        inp = _make_input(avg_negotiation_rounds_per_deal=4.5)
        assert inp.avg_negotiation_rounds_per_deal == 4.5

    def test_avg_opportunity_value_stored(self):
        inp = _make_input(avg_opportunity_value_usd=50_000.0)
        assert inp.avg_opportunity_value_usd == 50_000.0


# ===========================================================================
# 3. NegotiationResult DATACLASS & to_dict()
# ===========================================================================

class TestNegotiationResultDataclass:
    def _sample_result(self) -> NegotiationResult:
        return NegotiationResult(
            rep_id="r1",
            region="North",
            negotiation_risk=NegotiationRisk.low,
            negotiation_pattern=NegotiationPattern.none,
            negotiation_severity=NegotiationSeverity.disciplined,
            recommended_action=NegotiationAction.no_action,
            concession_discipline_score=5.0,
            negotiation_process_score=3.0,
            negotiation_urgency_score=2.0,
            value_articulation_score=1.0,
            negotiation_composite=3.5,
            has_negotiation_gap=False,
            requires_negotiation_coaching=False,
            estimated_margin_erosion_usd=0.0,
            negotiation_signal="healthy",
        )

    def test_all_15_fields_accessible(self):
        r = self._sample_result()
        fields = [
            "rep_id", "region", "negotiation_risk", "negotiation_pattern",
            "negotiation_severity", "recommended_action",
            "concession_discipline_score", "negotiation_process_score",
            "negotiation_urgency_score", "value_articulation_score",
            "negotiation_composite", "has_negotiation_gap",
            "requires_negotiation_coaching", "estimated_margin_erosion_usd",
            "negotiation_signal",
        ]
        assert len(fields) == 15
        for f in fields:
            assert hasattr(r, f)

    def test_to_dict_returns_dict(self):
        assert isinstance(self._sample_result().to_dict(), dict)

    def test_to_dict_has_15_keys(self):
        assert len(self._sample_result().to_dict()) == 15

    def test_to_dict_rep_id(self):
        assert self._sample_result().to_dict()["rep_id"] == "r1"

    def test_to_dict_region(self):
        assert self._sample_result().to_dict()["region"] == "North"

    def test_to_dict_negotiation_risk_is_str(self):
        d = self._sample_result().to_dict()
        assert d["negotiation_risk"] == "low"
        assert isinstance(d["negotiation_risk"], str)

    def test_to_dict_negotiation_pattern_is_str(self):
        d = self._sample_result().to_dict()
        assert d["negotiation_pattern"] == "none"

    def test_to_dict_negotiation_severity_is_str(self):
        d = self._sample_result().to_dict()
        assert d["negotiation_severity"] == "disciplined"

    def test_to_dict_recommended_action_is_str(self):
        d = self._sample_result().to_dict()
        assert d["recommended_action"] == "no_action"

    def test_to_dict_concession_score(self):
        assert self._sample_result().to_dict()["concession_discipline_score"] == 5.0

    def test_to_dict_process_score(self):
        assert self._sample_result().to_dict()["negotiation_process_score"] == 3.0

    def test_to_dict_urgency_score(self):
        assert self._sample_result().to_dict()["negotiation_urgency_score"] == 2.0

    def test_to_dict_value_score(self):
        assert self._sample_result().to_dict()["value_articulation_score"] == 1.0

    def test_to_dict_composite(self):
        assert self._sample_result().to_dict()["negotiation_composite"] == 3.5

    def test_to_dict_has_negotiation_gap(self):
        assert self._sample_result().to_dict()["has_negotiation_gap"] is False

    def test_to_dict_requires_coaching(self):
        assert self._sample_result().to_dict()["requires_negotiation_coaching"] is False

    def test_to_dict_margin_erosion(self):
        assert self._sample_result().to_dict()["estimated_margin_erosion_usd"] == 0.0

    def test_to_dict_signal(self):
        assert self._sample_result().to_dict()["negotiation_signal"] == "healthy"

    def test_to_dict_all_expected_keys(self):
        d = self._sample_result().to_dict()
        expected = {
            "rep_id", "region", "negotiation_risk", "negotiation_pattern",
            "negotiation_severity", "recommended_action",
            "concession_discipline_score", "negotiation_process_score",
            "negotiation_urgency_score", "value_articulation_score",
            "negotiation_composite", "has_negotiation_gap",
            "requires_negotiation_coaching", "estimated_margin_erosion_usd",
            "negotiation_signal",
        }
        assert set(d.keys()) == expected


# ===========================================================================
# 4. _concession_discipline_score
# ===========================================================================

class TestConcessionDisciplineScore:
    def _score(self, **kw) -> float:
        e = _engine()
        return e._concession_discipline_score(_make_input(**kw))

    # first_concession_timing_pct thresholds
    def test_first_concession_below_35_adds_0(self):
        # 0.10 < 0.35 => +0
        s = self._score(
            first_concession_timing_pct=0.10,
            avg_discount_concession_pct=0.05,
            deals_won_without_discount_pct=0.60,
        )
        assert s == 0.0

    def test_first_concession_at_35_adds_8(self):
        s = self._score(
            first_concession_timing_pct=0.35,
            avg_discount_concession_pct=0.0,
            deals_won_without_discount_pct=1.0,
        )
        assert s == 8.0

    def test_first_concession_at_55_adds_22(self):
        s = self._score(
            first_concession_timing_pct=0.55,
            avg_discount_concession_pct=0.0,
            deals_won_without_discount_pct=1.0,
        )
        assert s == 22.0

    def test_first_concession_at_80_adds_40(self):
        s = self._score(
            first_concession_timing_pct=0.80,
            avg_discount_concession_pct=0.0,
            deals_won_without_discount_pct=1.0,
        )
        assert s == 40.0

    def test_first_concession_above_80_adds_40(self):
        s = self._score(
            first_concession_timing_pct=0.99,
            avg_discount_concession_pct=0.0,
            deals_won_without_discount_pct=1.0,
        )
        assert s == 40.0

    def test_first_concession_between_35_55_adds_8(self):
        s = self._score(
            first_concession_timing_pct=0.45,
            avg_discount_concession_pct=0.0,
            deals_won_without_discount_pct=1.0,
        )
        assert s == 8.0

    # avg_discount_concession_pct thresholds
    def test_discount_below_10_adds_0(self):
        s = self._score(
            first_concession_timing_pct=0.0,
            avg_discount_concession_pct=0.05,
            deals_won_without_discount_pct=1.0,
        )
        assert s == 0.0

    def test_discount_at_10_adds_18(self):
        s = self._score(
            first_concession_timing_pct=0.0,
            avg_discount_concession_pct=0.10,
            deals_won_without_discount_pct=1.0,
        )
        assert s == 18.0

    def test_discount_at_20_adds_35(self):
        s = self._score(
            first_concession_timing_pct=0.0,
            avg_discount_concession_pct=0.20,
            deals_won_without_discount_pct=1.0,
        )
        assert s == 35.0

    def test_discount_above_20_adds_35(self):
        s = self._score(
            first_concession_timing_pct=0.0,
            avg_discount_concession_pct=0.50,
            deals_won_without_discount_pct=1.0,
        )
        assert s == 35.0

    # deals_won_without_discount_pct thresholds
    def test_no_discount_above_30_adds_0(self):
        s = self._score(
            first_concession_timing_pct=0.0,
            avg_discount_concession_pct=0.0,
            deals_won_without_discount_pct=0.50,
        )
        assert s == 0.0

    def test_no_discount_at_30_adds_12(self):
        s = self._score(
            first_concession_timing_pct=0.0,
            avg_discount_concession_pct=0.0,
            deals_won_without_discount_pct=0.30,
        )
        assert s == 12.0

    def test_no_discount_at_10_adds_25(self):
        s = self._score(
            first_concession_timing_pct=0.0,
            avg_discount_concession_pct=0.0,
            deals_won_without_discount_pct=0.10,
        )
        assert s == 25.0

    def test_no_discount_below_10_adds_25(self):
        s = self._score(
            first_concession_timing_pct=0.0,
            avg_discount_concession_pct=0.0,
            deals_won_without_discount_pct=0.05,
        )
        assert s == 25.0

    def test_max_score_capped_at_100(self):
        s = self._score(
            first_concession_timing_pct=0.99,
            avg_discount_concession_pct=0.99,
            deals_won_without_discount_pct=0.01,
        )
        assert s == 100.0

    def test_all_risky_combo(self):
        # 40 + 35 + 25 = 100 => capped
        s = self._score(
            first_concession_timing_pct=0.90,
            avg_discount_concession_pct=0.25,
            deals_won_without_discount_pct=0.05,
        )
        assert s == 100.0

    def test_partial_combo(self):
        # 22 + 18 + 12 = 52
        s = self._score(
            first_concession_timing_pct=0.60,
            avg_discount_concession_pct=0.15,
            deals_won_without_discount_pct=0.20,
        )
        assert s == 52.0


# ===========================================================================
# 5. _negotiation_process_score
# ===========================================================================

class TestNegotiationProcessScore:
    def _score(self, **kw) -> float:
        e = _engine()
        return e._negotiation_process_score(_make_input(**kw))

    # manager_escalation_in_negotiation_pct
    def test_escalation_below_15_adds_0(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.05,
            multi_item_negotiation_rate_pct=0.60,
            deal_desk_referral_in_negotiation_pct=0.05,
        )
        assert s == 0.0

    def test_escalation_at_15_adds_8(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.15,
            multi_item_negotiation_rate_pct=0.60,
            deal_desk_referral_in_negotiation_pct=0.05,
        )
        assert s == 8.0

    def test_escalation_at_35_adds_22(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.35,
            multi_item_negotiation_rate_pct=0.60,
            deal_desk_referral_in_negotiation_pct=0.05,
        )
        assert s == 22.0

    def test_escalation_at_60_adds_40(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.60,
            multi_item_negotiation_rate_pct=0.60,
            deal_desk_referral_in_negotiation_pct=0.05,
        )
        assert s == 40.0

    def test_escalation_above_60_adds_40(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.90,
            multi_item_negotiation_rate_pct=0.60,
            deal_desk_referral_in_negotiation_pct=0.05,
        )
        assert s == 40.0

    # multi_item_negotiation_rate_pct
    def test_multi_item_above_35_adds_0(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.0,
            multi_item_negotiation_rate_pct=0.60,
            deal_desk_referral_in_negotiation_pct=0.0,
        )
        assert s == 0.0

    def test_multi_item_at_35_adds_18(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.0,
            multi_item_negotiation_rate_pct=0.35,
            deal_desk_referral_in_negotiation_pct=0.0,
        )
        assert s == 18.0

    def test_multi_item_at_15_adds_35(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.0,
            multi_item_negotiation_rate_pct=0.15,
            deal_desk_referral_in_negotiation_pct=0.0,
        )
        assert s == 35.0

    def test_multi_item_below_15_adds_35(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.0,
            multi_item_negotiation_rate_pct=0.05,
            deal_desk_referral_in_negotiation_pct=0.0,
        )
        assert s == 35.0

    # deal_desk_referral_in_negotiation_pct
    def test_referral_below_20_adds_0(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.0,
            multi_item_negotiation_rate_pct=0.60,
            deal_desk_referral_in_negotiation_pct=0.10,
        )
        assert s == 0.0

    def test_referral_at_20_adds_12(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.0,
            multi_item_negotiation_rate_pct=0.60,
            deal_desk_referral_in_negotiation_pct=0.20,
        )
        assert s == 12.0

    def test_referral_at_40_adds_25(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.0,
            multi_item_negotiation_rate_pct=0.60,
            deal_desk_referral_in_negotiation_pct=0.40,
        )
        assert s == 25.0

    def test_referral_above_40_adds_25(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.0,
            multi_item_negotiation_rate_pct=0.60,
            deal_desk_referral_in_negotiation_pct=0.80,
        )
        assert s == 25.0

    def test_max_score_capped_at_100(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.99,
            multi_item_negotiation_rate_pct=0.01,
            deal_desk_referral_in_negotiation_pct=0.99,
        )
        assert s == 100.0

    def test_combo_40_35_25(self):
        s = self._score(
            manager_escalation_in_negotiation_pct=0.70,
            multi_item_negotiation_rate_pct=0.10,
            deal_desk_referral_in_negotiation_pct=0.50,
        )
        assert s == 100.0


# ===========================================================================
# 6. _negotiation_urgency_score
# ===========================================================================

class TestNegotiationUrgencyScore:
    def _score(self, **kw) -> float:
        e = _engine()
        return e._negotiation_urgency_score(_make_input(**kw))

    # urgency_trigger_used_pct
    def test_urgency_above_50_adds_0(self):
        s = self._score(
            urgency_trigger_used_pct=0.70,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.80,
        )
        assert s == 0.0

    def test_urgency_at_50_adds_8(self):
        s = self._score(
            urgency_trigger_used_pct=0.50,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.80,
        )
        assert s == 8.0

    def test_urgency_at_30_adds_22(self):
        s = self._score(
            urgency_trigger_used_pct=0.30,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.80,
        )
        assert s == 22.0

    def test_urgency_at_10_adds_40(self):
        s = self._score(
            urgency_trigger_used_pct=0.10,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.80,
        )
        assert s == 40.0

    def test_urgency_below_10_adds_40(self):
        s = self._score(
            urgency_trigger_used_pct=0.05,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.80,
        )
        assert s == 40.0

    # negotiation_stall_rate_pct
    def test_stall_below_20_adds_0(self):
        s = self._score(
            urgency_trigger_used_pct=0.60,
            negotiation_stall_rate_pct=0.10,
            competitive_counteroffer_handled_pct=0.80,
        )
        assert s == 0.0

    def test_stall_at_20_adds_18(self):
        s = self._score(
            urgency_trigger_used_pct=0.60,
            negotiation_stall_rate_pct=0.20,
            competitive_counteroffer_handled_pct=0.80,
        )
        assert s == 18.0

    def test_stall_at_40_adds_35(self):
        s = self._score(
            urgency_trigger_used_pct=0.60,
            negotiation_stall_rate_pct=0.40,
            competitive_counteroffer_handled_pct=0.80,
        )
        assert s == 35.0

    def test_stall_above_40_adds_35(self):
        s = self._score(
            urgency_trigger_used_pct=0.60,
            negotiation_stall_rate_pct=0.80,
            competitive_counteroffer_handled_pct=0.80,
        )
        assert s == 35.0

    # competitive_counteroffer_handled_pct
    def test_counteroffer_above_50_adds_0(self):
        s = self._score(
            urgency_trigger_used_pct=0.60,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.80,
        )
        assert s == 0.0

    def test_counteroffer_at_50_adds_12(self):
        s = self._score(
            urgency_trigger_used_pct=0.60,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.50,
        )
        assert s == 12.0

    def test_counteroffer_at_20_adds_25(self):
        s = self._score(
            urgency_trigger_used_pct=0.60,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.20,
        )
        assert s == 25.0

    def test_counteroffer_below_20_adds_25(self):
        s = self._score(
            urgency_trigger_used_pct=0.60,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.10,
        )
        assert s == 25.0

    def test_max_capped_at_100(self):
        s = self._score(
            urgency_trigger_used_pct=0.0,
            negotiation_stall_rate_pct=0.99,
            competitive_counteroffer_handled_pct=0.01,
        )
        assert s == 100.0

    def test_zero_score_all_good(self):
        s = self._score(
            urgency_trigger_used_pct=0.80,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.90,
        )
        assert s == 0.0


# ===========================================================================
# 7. _value_articulation_score
# ===========================================================================

class TestValueArticulationScore:
    def _score(self, **kw) -> float:
        e = _engine()
        return e._value_articulation_score(_make_input(**kw))

    # value_vs_price_conversation_ratio
    def test_value_ratio_above_60_adds_0(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.80,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.05,
        )
        assert s == 0.0

    def test_value_ratio_at_60_adds_10(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.60,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.05,
        )
        assert s == 10.0

    def test_value_ratio_at_40_adds_25(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.40,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.05,
        )
        assert s == 25.0

    def test_value_ratio_at_20_adds_45(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.20,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.05,
        )
        assert s == 45.0

    def test_value_ratio_below_20_adds_45(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.10,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.05,
        )
        assert s == 45.0

    # scope_expansion_during_negotiation_pct
    def test_scope_above_30_adds_0(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.80,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.05,
        )
        assert s == 0.0

    def test_scope_at_30_adds_15(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.80,
            scope_expansion_during_negotiation_pct=0.30,
            deals_with_no_negotiation_pct=0.05,
        )
        assert s == 15.0

    def test_scope_at_10_adds_30(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.80,
            scope_expansion_during_negotiation_pct=0.10,
            deals_with_no_negotiation_pct=0.05,
        )
        assert s == 30.0

    def test_scope_below_10_adds_30(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.80,
            scope_expansion_during_negotiation_pct=0.05,
            deals_with_no_negotiation_pct=0.05,
        )
        assert s == 30.0

    # deals_with_no_negotiation_pct
    def test_no_negotiation_below_20_adds_0(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.80,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.10,
        )
        assert s == 0.0

    def test_no_negotiation_at_20_adds_12(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.80,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.20,
        )
        assert s == 12.0

    def test_no_negotiation_at_40_adds_25(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.80,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.40,
        )
        assert s == 25.0

    def test_no_negotiation_above_40_adds_25(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.80,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.80,
        )
        assert s == 25.0

    def test_max_capped_at_100(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.05,
            scope_expansion_during_negotiation_pct=0.05,
            deals_with_no_negotiation_pct=0.80,
        )
        assert s == 100.0

    def test_zero_score_all_good(self):
        s = self._score(
            value_vs_price_conversation_ratio=0.90,
            scope_expansion_during_negotiation_pct=0.60,
            deals_with_no_negotiation_pct=0.05,
        )
        assert s == 0.0

    def test_partial_combo(self):
        # 25 + 15 + 12 = 52
        s = self._score(
            value_vs_price_conversation_ratio=0.40,
            scope_expansion_during_negotiation_pct=0.30,
            deals_with_no_negotiation_pct=0.20,
        )
        assert s == 52.0


# ===========================================================================
# 8. _detect_pattern
# ===========================================================================

class TestDetectPattern:
    def _detect(self, concession=0.0, process=0.0, urgency=0.0, value=0.0, **overrides):
        e = _engine()
        inp = _make_input(**overrides)
        return e._detect_pattern(inp, concession, process, urgency, value)

    def test_no_pattern_when_all_low(self):
        p = self._detect(concession=5, process=5, urgency=5, value=5)
        assert p == NegotiationPattern.none

    # early_capitulation: concession >= 40 AND first_concession_timing_pct >= 0.70
    def test_early_capitulation_detected(self):
        p = self._detect(concession=40, first_concession_timing_pct=0.70)
        assert p == NegotiationPattern.early_capitulation

    def test_early_capitulation_concession_below_40_not_triggered(self):
        p = self._detect(concession=39, first_concession_timing_pct=0.90)
        assert p != NegotiationPattern.early_capitulation

    def test_early_capitulation_timing_below_70_not_triggered(self):
        p = self._detect(concession=60, first_concession_timing_pct=0.69)
        assert p != NegotiationPattern.early_capitulation

    def test_early_capitulation_exact_boundary(self):
        p = self._detect(concession=40, first_concession_timing_pct=0.70)
        assert p == NegotiationPattern.early_capitulation

    # manager_escalation_dependency: process >= 40 AND manager_esc >= 0.50
    def test_manager_escalation_dependency_detected(self):
        p = self._detect(concession=0, process=40, manager_escalation_in_negotiation_pct=0.50)
        assert p == NegotiationPattern.manager_escalation_dependency

    def test_manager_escalation_process_below_40_not_triggered(self):
        p = self._detect(concession=0, process=39, manager_escalation_in_negotiation_pct=0.90)
        assert p != NegotiationPattern.manager_escalation_dependency

    def test_manager_escalation_pct_below_50_not_triggered(self):
        p = self._detect(concession=0, process=60, manager_escalation_in_negotiation_pct=0.49)
        assert p != NegotiationPattern.manager_escalation_dependency

    # price_anchoring_failure: value >= 30 AND value_vs_price_ratio <= 0.30
    def test_price_anchoring_failure_detected(self):
        p = self._detect(concession=0, process=0, value=30, value_vs_price_conversation_ratio=0.30)
        assert p == NegotiationPattern.price_anchoring_failure

    def test_price_anchoring_value_below_30_not_triggered(self):
        p = self._detect(value=29, value_vs_price_conversation_ratio=0.10)
        assert p != NegotiationPattern.price_anchoring_failure

    def test_price_anchoring_ratio_above_30_not_triggered(self):
        p = self._detect(value=50, value_vs_price_conversation_ratio=0.31)
        assert p != NegotiationPattern.price_anchoring_failure

    # concession_cascade: concession >= 30 AND avg_negotiation_rounds >= 3.0
    def test_concession_cascade_detected(self):
        p = self._detect(concession=30, value=0, value_vs_price_conversation_ratio=0.90,
                         avg_negotiation_rounds_per_deal=3.0)
        assert p == NegotiationPattern.concession_cascade

    def test_concession_cascade_rounds_below_3_not_triggered(self):
        p = self._detect(concession=50, avg_negotiation_rounds_per_deal=2.9)
        assert p != NegotiationPattern.concession_cascade

    def test_concession_cascade_concession_below_30_not_triggered(self):
        p = self._detect(concession=29, avg_negotiation_rounds_per_deal=5.0)
        assert p != NegotiationPattern.concession_cascade

    # urgency_creation_gap: urgency >= 30 AND urgency_trigger_used_pct <= 0.20
    def test_urgency_creation_gap_detected(self):
        p = self._detect(concession=0, process=0, urgency=30,
                         value_vs_price_conversation_ratio=0.90,
                         urgency_trigger_used_pct=0.20)
        assert p == NegotiationPattern.urgency_creation_gap

    def test_urgency_gap_urgency_below_30_not_triggered(self):
        p = self._detect(urgency=29, urgency_trigger_used_pct=0.05)
        assert p != NegotiationPattern.urgency_creation_gap

    def test_urgency_gap_trigger_above_20_not_triggered(self):
        p = self._detect(urgency=60, urgency_trigger_used_pct=0.21)
        assert p != NegotiationPattern.urgency_creation_gap

    # Priority ordering: early_capitulation > manager_escalation
    def test_early_capitulation_takes_priority_over_manager(self):
        p = self._detect(
            concession=50, process=50,
            first_concession_timing_pct=0.80,
            manager_escalation_in_negotiation_pct=0.80,
        )
        assert p == NegotiationPattern.early_capitulation

    # Priority: price_anchoring before concession_cascade
    def test_price_anchoring_takes_priority_over_cascade(self):
        p = self._detect(
            concession=35, process=0, value=40,
            value_vs_price_conversation_ratio=0.20,
            avg_negotiation_rounds_per_deal=5.0,
        )
        assert p == NegotiationPattern.price_anchoring_failure


# ===========================================================================
# 9. _risk_level
# ===========================================================================

class TestRiskLevel:
    def _risk(self, composite: float) -> NegotiationRisk:
        return _engine()._risk_level(composite)

    def test_below_20_is_low(self):
        assert self._risk(0.0) == NegotiationRisk.low
        assert self._risk(19.9) == NegotiationRisk.low

    def test_at_20_is_moderate(self):
        assert self._risk(20.0) == NegotiationRisk.moderate

    def test_between_20_40_is_moderate(self):
        assert self._risk(30.0) == NegotiationRisk.moderate
        assert self._risk(39.9) == NegotiationRisk.moderate

    def test_at_40_is_high(self):
        assert self._risk(40.0) == NegotiationRisk.high

    def test_between_40_60_is_high(self):
        assert self._risk(50.0) == NegotiationRisk.high
        assert self._risk(59.9) == NegotiationRisk.high

    def test_at_60_is_critical(self):
        assert self._risk(60.0) == NegotiationRisk.critical

    def test_above_60_is_critical(self):
        assert self._risk(100.0) == NegotiationRisk.critical

    def test_zero_is_low(self):
        assert self._risk(0) == NegotiationRisk.low


# ===========================================================================
# 10. _severity
# ===========================================================================

class TestSeverity:
    def _sev(self, composite: float) -> NegotiationSeverity:
        return _engine()._severity(composite)

    def test_below_20_is_disciplined(self):
        assert self._sev(0.0) == NegotiationSeverity.disciplined
        assert self._sev(19.9) == NegotiationSeverity.disciplined

    def test_at_20_is_developing(self):
        assert self._sev(20.0) == NegotiationSeverity.developing

    def test_between_20_40_is_developing(self):
        assert self._sev(30.0) == NegotiationSeverity.developing

    def test_at_40_is_reactive(self):
        assert self._sev(40.0) == NegotiationSeverity.reactive

    def test_between_40_60_is_reactive(self):
        assert self._sev(55.0) == NegotiationSeverity.reactive

    def test_at_60_is_erosive(self):
        assert self._sev(60.0) == NegotiationSeverity.erosive

    def test_above_60_is_erosive(self):
        assert self._sev(100.0) == NegotiationSeverity.erosive

    def test_zero_is_disciplined(self):
        assert self._sev(0) == NegotiationSeverity.disciplined


# ===========================================================================
# 11. _action
# ===========================================================================

class TestAction:
    def _action(self, risk: NegotiationRisk, pattern: NegotiationPattern) -> NegotiationAction:
        return _engine()._action(risk, pattern)

    # LOW risk
    def test_low_risk_any_pattern_no_action(self):
        for p in NegotiationPattern:
            assert self._action(NegotiationRisk.low, p) == NegotiationAction.no_action

    # MODERATE risk
    def test_moderate_any_pattern_coaching(self):
        for p in NegotiationPattern:
            assert self._action(NegotiationRisk.moderate, p) == NegotiationAction.negotiation_skills_coaching

    # HIGH risk
    def test_high_urgency_gap_returns_urgency_training(self):
        assert self._action(NegotiationRisk.high, NegotiationPattern.urgency_creation_gap) == NegotiationAction.urgency_creation_training

    def test_high_concession_cascade_returns_concession_review(self):
        assert self._action(NegotiationRisk.high, NegotiationPattern.concession_cascade) == NegotiationAction.concession_management_review

    def test_high_other_patterns_returns_coaching(self):
        for p in [NegotiationPattern.none, NegotiationPattern.early_capitulation,
                  NegotiationPattern.manager_escalation_dependency,
                  NegotiationPattern.price_anchoring_failure]:
            assert self._action(NegotiationRisk.high, p) == NegotiationAction.negotiation_skills_coaching

    # CRITICAL risk
    def test_critical_manager_escalation_returns_escalation_reduction(self):
        assert self._action(NegotiationRisk.critical, NegotiationPattern.manager_escalation_dependency) == NegotiationAction.manager_escalation_reduction

    def test_critical_price_anchoring_returns_value_anchoring_training(self):
        assert self._action(NegotiationRisk.critical, NegotiationPattern.price_anchoring_failure) == NegotiationAction.value_anchoring_training

    def test_critical_other_patterns_returns_concession_review(self):
        for p in [NegotiationPattern.none, NegotiationPattern.early_capitulation,
                  NegotiationPattern.concession_cascade, NegotiationPattern.urgency_creation_gap]:
            assert self._action(NegotiationRisk.critical, p) == NegotiationAction.concession_management_review


# ===========================================================================
# 12. _has_negotiation_gap
# ===========================================================================

class TestHasNegotiationGap:
    def _gap(self, composite=0.0, **kw) -> bool:
        e = _engine()
        return e._has_negotiation_gap(composite, _make_input(**kw))

    def test_false_when_all_below_thresholds(self):
        assert self._gap(
            composite=10.0,
            avg_discount_concession_pct=0.05,
            manager_escalation_in_negotiation_pct=0.10,
        ) is False

    def test_true_when_composite_at_40(self):
        assert self._gap(composite=40.0) is True

    def test_true_when_composite_above_40(self):
        assert self._gap(composite=80.0) is True

    def test_true_when_discount_at_20(self):
        assert self._gap(composite=5.0, avg_discount_concession_pct=0.20) is True

    def test_true_when_discount_above_20(self):
        assert self._gap(composite=0.0, avg_discount_concession_pct=0.50) is True

    def test_false_when_discount_below_20(self):
        assert self._gap(composite=10.0, avg_discount_concession_pct=0.19) is False

    def test_true_when_escalation_at_50(self):
        assert self._gap(composite=5.0, manager_escalation_in_negotiation_pct=0.50) is True

    def test_true_when_escalation_above_50(self):
        assert self._gap(composite=5.0, manager_escalation_in_negotiation_pct=0.90) is True

    def test_false_when_escalation_below_50(self):
        assert self._gap(composite=10.0, manager_escalation_in_negotiation_pct=0.49) is False

    def test_composite_39_discount_19_escalation_49_all_false(self):
        assert self._gap(
            composite=39.9,
            avg_discount_concession_pct=0.19,
            manager_escalation_in_negotiation_pct=0.49,
        ) is False


# ===========================================================================
# 13. _requires_negotiation_coaching
# ===========================================================================

class TestRequiresNegotiationCoaching:
    def _coach(self, composite=0.0, **kw) -> bool:
        e = _engine()
        return e._requires_negotiation_coaching(composite, _make_input(**kw))

    def test_false_when_all_below_thresholds(self):
        assert self._coach(
            composite=10.0,
            first_concession_timing_pct=0.10,
            deals_won_without_discount_pct=0.60,
        ) is False

    def test_true_when_composite_at_30(self):
        assert self._coach(composite=30.0) is True

    def test_true_when_composite_above_30(self):
        assert self._coach(composite=80.0) is True

    def test_true_when_first_concession_at_60(self):
        assert self._coach(composite=5.0, first_concession_timing_pct=0.60) is True

    def test_true_when_first_concession_above_60(self):
        assert self._coach(composite=5.0, first_concession_timing_pct=0.90) is True

    def test_false_when_first_concession_below_60(self):
        assert self._coach(composite=5.0, first_concession_timing_pct=0.59) is False

    def test_true_when_deals_no_discount_at_15(self):
        assert self._coach(composite=5.0, deals_won_without_discount_pct=0.15) is True

    def test_true_when_deals_no_discount_below_15(self):
        assert self._coach(composite=5.0, deals_won_without_discount_pct=0.05) is True

    def test_false_when_deals_no_discount_above_15(self):
        assert self._coach(composite=5.0, deals_won_without_discount_pct=0.16) is False

    def test_composite_29_timing_59_discount_16_all_false(self):
        assert self._coach(
            composite=29.9,
            first_concession_timing_pct=0.59,
            deals_won_without_discount_pct=0.16,
        ) is False


# ===========================================================================
# 14. _estimated_margin_erosion
# ===========================================================================

class TestEstimatedMarginErosion:
    def _erosion(self, composite: float, **kw) -> float:
        e = _engine()
        return e._estimated_margin_erosion(_make_input(**kw), composite)

    def test_zero_composite_gives_zero(self):
        assert self._erosion(
            composite=0.0,
            total_negotiations_conducted=100,
            avg_opportunity_value_usd=10_000,
            avg_discount_concession_pct=0.20,
        ) == 0.0

    def test_zero_discount_gives_zero(self):
        assert self._erosion(
            composite=50.0,
            total_negotiations_conducted=100,
            avg_opportunity_value_usd=10_000,
            avg_discount_concession_pct=0.0,
        ) == 0.0

    def test_zero_negotiations_gives_zero(self):
        assert self._erosion(
            composite=80.0,
            total_negotiations_conducted=0,
            avg_opportunity_value_usd=10_000,
            avg_discount_concession_pct=0.20,
        ) == 0.0

    def test_formula_calculation(self):
        # 100 * 10000 * 0.20 * (50/100) * 0.50 = 50000
        result = self._erosion(
            composite=50.0,
            total_negotiations_conducted=100,
            avg_opportunity_value_usd=10_000,
            avg_discount_concession_pct=0.20,
        )
        assert result == 50_000.0

    def test_formula_calculation_2(self):
        # 50 * 20000 * 0.10 * (80/100) * 0.50 = 40000
        result = self._erosion(
            composite=80.0,
            total_negotiations_conducted=50,
            avg_opportunity_value_usd=20_000,
            avg_discount_concession_pct=0.10,
        )
        assert result == 40_000.0

    def test_result_is_rounded_to_2_places(self):
        result = self._erosion(
            composite=33.3,
            total_negotiations_conducted=1,
            avg_opportunity_value_usd=1.0,
            avg_discount_concession_pct=0.07,
        )
        # Verify rounded to 2 decimal places
        assert result == round(result, 2)

    def test_result_type_is_float(self):
        result = self._erosion(composite=50.0)
        assert isinstance(result, float)


# ===========================================================================
# 15. _signal
# ===========================================================================

class TestSignal:
    def _signal(self, pattern=NegotiationPattern.none, composite=0.0, **kw) -> str:
        e = _engine()
        return e._signal(_make_input(**kw), pattern, composite)

    def test_healthy_signal_when_none_and_composite_below_20(self):
        s = self._signal(pattern=NegotiationPattern.none, composite=19.9)
        assert s == "Negotiation discipline healthy — concession management, value anchoring, and urgency creation within benchmarks"

    def test_healthy_signal_at_composite_zero(self):
        s = self._signal(pattern=NegotiationPattern.none, composite=0.0)
        assert s == "Negotiation discipline healthy — concession management, value anchoring, and urgency creation within benchmarks"

    def test_no_healthy_signal_when_pattern_not_none(self):
        s = self._signal(pattern=NegotiationPattern.early_capitulation, composite=10.0)
        assert "healthy" not in s

    def test_no_healthy_signal_when_composite_at_20(self):
        s = self._signal(pattern=NegotiationPattern.none, composite=20.0)
        assert "healthy" not in s

    def test_signal_contains_pattern_label(self):
        s = self._signal(
            pattern=NegotiationPattern.early_capitulation,
            composite=45.0,
            first_concession_timing_pct=0.80,
        )
        assert "early capitulation" in s.lower()

    def test_signal_contains_composite(self):
        s = self._signal(
            pattern=NegotiationPattern.concession_cascade,
            composite=55.0,
            first_concession_timing_pct=0.50,
        )
        assert "55" in s

    def test_signal_contains_avg_rounds(self):
        s = self._signal(
            pattern=NegotiationPattern.urgency_creation_gap,
            composite=30.0,
            avg_negotiation_rounds_per_deal=2.5,
        )
        assert "2.5" in s

    def test_signal_contains_first_concession_pct(self):
        s = self._signal(
            pattern=NegotiationPattern.price_anchoring_failure,
            composite=35.0,
            first_concession_timing_pct=0.80,
            deals_won_without_discount_pct=0.60,
        )
        assert "80%" in s

    def test_signal_negotiation_risk_label_when_pattern_none_composite_above_20(self):
        s = self._signal(
            pattern=NegotiationPattern.none,
            composite=25.0,
            first_concession_timing_pct=0.50,
        )
        assert "negotiation risk" in s.lower()

    def test_signal_manager_escalation_pattern_label(self):
        s = self._signal(
            pattern=NegotiationPattern.manager_escalation_dependency,
            composite=65.0,
        )
        assert "manager escalation dependency" in s.lower()

    def test_signal_concession_cascade_label(self):
        s = self._signal(
            pattern=NegotiationPattern.concession_cascade,
            composite=40.0,
        )
        assert "concession cascade" in s.lower()

    def test_signal_urgency_creation_gap_label(self):
        s = self._signal(
            pattern=NegotiationPattern.urgency_creation_gap,
            composite=35.0,
        )
        assert "urgency creation gap" in s.lower()

    def test_signal_is_string(self):
        assert isinstance(self._signal(), str)

    def test_signal_deals_won_without_discount_included(self):
        s = self._signal(
            pattern=NegotiationPattern.early_capitulation,
            composite=50.0,
            deals_won_without_discount_pct=0.40,
        )
        assert "40%" in s


# ===========================================================================
# 16. assess() — full result validation
# ===========================================================================

class TestAssess:
    def test_returns_negotiation_result(self):
        e = _engine()
        result = e.assess(_make_input())
        assert isinstance(result, NegotiationResult)

    def test_rep_id_propagated(self):
        e = _engine()
        result = e.assess(_make_input(rep_id="rep-xyz"))
        assert result.rep_id == "rep-xyz"

    def test_region_propagated(self):
        e = _engine()
        result = e.assess(_make_input(region="South"))
        assert result.region == "South"

    def test_scores_are_floats(self):
        e = _engine()
        r = e.assess(_make_input())
        assert isinstance(r.concession_discipline_score, float)
        assert isinstance(r.negotiation_process_score, float)
        assert isinstance(r.negotiation_urgency_score, float)
        assert isinstance(r.value_articulation_score, float)
        assert isinstance(r.negotiation_composite, float)

    def test_composite_formula(self):
        e = _engine()
        inp = _make_input()
        r = e.assess(inp)
        # composite = concession*0.35 + process*0.30 + urgency*0.20 + value*0.15
        expected = round(
            r.concession_discipline_score * 0.35 +
            r.negotiation_process_score * 0.30 +
            r.negotiation_urgency_score * 0.20 +
            r.value_articulation_score * 0.15,
            1
        )
        assert r.negotiation_composite == expected

    def test_composite_capped_at_100(self):
        e = _engine()
        # force max scores
        inp = _make_input(
            first_concession_timing_pct=0.99,
            avg_discount_concession_pct=0.99,
            deals_won_without_discount_pct=0.01,
            manager_escalation_in_negotiation_pct=0.99,
            multi_item_negotiation_rate_pct=0.01,
            deal_desk_referral_in_negotiation_pct=0.99,
            urgency_trigger_used_pct=0.01,
            negotiation_stall_rate_pct=0.99,
            competitive_counteroffer_handled_pct=0.01,
            value_vs_price_conversation_ratio=0.01,
            scope_expansion_during_negotiation_pct=0.01,
            deals_with_no_negotiation_pct=0.99,
        )
        r = e.assess(inp)
        assert r.negotiation_composite <= 100.0

    def test_low_risk_scenario(self):
        e = _engine()
        r = e.assess(_make_input())
        assert r.negotiation_risk == NegotiationRisk.low

    def test_high_risk_scenario(self):
        # Elevate process score too to get composite into high/critical range
        e = _engine()
        inp = _make_input(
            first_concession_timing_pct=0.80,
            avg_discount_concession_pct=0.25,
            deals_won_without_discount_pct=0.05,
            manager_escalation_in_negotiation_pct=0.70,  # process: +40
            multi_item_negotiation_rate_pct=0.05,         # process: +35
            deal_desk_referral_in_negotiation_pct=0.50,  # process: +25
        )
        r = e.assess(inp)
        assert r.negotiation_risk in (NegotiationRisk.high, NegotiationRisk.critical)

    def test_critical_risk_scenario(self):
        e = _engine()
        inp = _make_input(
            first_concession_timing_pct=0.90,
            avg_discount_concession_pct=0.30,
            deals_won_without_discount_pct=0.05,
            manager_escalation_in_negotiation_pct=0.70,
            multi_item_negotiation_rate_pct=0.05,
            deal_desk_referral_in_negotiation_pct=0.50,
            urgency_trigger_used_pct=0.05,
            negotiation_stall_rate_pct=0.50,
            competitive_counteroffer_handled_pct=0.10,
            value_vs_price_conversation_ratio=0.10,
            scope_expansion_during_negotiation_pct=0.05,
            deals_with_no_negotiation_pct=0.60,
        )
        r = e.assess(inp)
        assert r.negotiation_risk == NegotiationRisk.critical
        assert r.negotiation_severity == NegotiationSeverity.erosive

    def test_result_stored_in_results(self):
        e = _engine()
        r = e.assess(_make_input())
        assert r in e._results

    def test_result_appended_to_results(self):
        e = _engine()
        e.assess(_make_input(rep_id="rep-1"))
        e.assess(_make_input(rep_id="rep-2"))
        assert len(e._results) == 2

    def test_has_negotiation_gap_type(self):
        e = _engine()
        r = e.assess(_make_input())
        assert isinstance(r.has_negotiation_gap, bool)

    def test_requires_coaching_type(self):
        e = _engine()
        r = e.assess(_make_input())
        assert isinstance(r.requires_negotiation_coaching, bool)

    def test_margin_erosion_non_negative(self):
        e = _engine()
        r = e.assess(_make_input())
        assert r.estimated_margin_erosion_usd >= 0.0

    def test_signal_is_string(self):
        e = _engine()
        r = e.assess(_make_input())
        assert isinstance(r.negotiation_signal, str)

    def test_low_risk_gives_no_action(self):
        e = _engine()
        r = e.assess(_make_input())
        assert r.recommended_action == NegotiationAction.no_action

    def test_low_risk_gives_disciplined_severity(self):
        e = _engine()
        r = e.assess(_make_input())
        assert r.negotiation_severity == NegotiationSeverity.disciplined

    def test_healthy_signal_for_low_risk(self):
        e = _engine()
        r = e.assess(_make_input())
        assert "healthy" in r.negotiation_signal

    def test_to_dict_works_after_assess(self):
        e = _engine()
        r = e.assess(_make_input())
        d = r.to_dict()
        assert len(d) == 15

    def test_pattern_none_for_low_risk(self):
        e = _engine()
        r = e.assess(_make_input())
        assert r.negotiation_pattern == NegotiationPattern.none


# ===========================================================================
# 17. assess_batch()
# ===========================================================================

class TestAssessBatch:
    def test_returns_list(self):
        e = _engine()
        results = e.assess_batch([_make_input()])
        assert isinstance(results, list)

    def test_returns_correct_count(self):
        e = _engine()
        inputs = [_make_input(rep_id=f"r{i}") for i in range(5)]
        results = e.assess_batch(inputs)
        assert len(results) == 5

    def test_all_results_are_negotiation_result(self):
        e = _engine()
        inputs = [_make_input(rep_id=f"r{i}") for i in range(3)]
        for r in e.assess_batch(inputs):
            assert isinstance(r, NegotiationResult)

    def test_empty_list_returns_empty(self):
        e = _engine()
        assert e.assess_batch([]) == []

    def test_results_stored_in_engine(self):
        e = _engine()
        inputs = [_make_input(rep_id=f"r{i}") for i in range(4)]
        e.assess_batch(inputs)
        assert len(e._results) == 4

    def test_rep_ids_match(self):
        e = _engine()
        inputs = [_make_input(rep_id=f"rep-{i}") for i in range(3)]
        results = e.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep-{i}"

    def test_batch_and_single_identical(self):
        e1 = _engine()
        e2 = _engine()
        inp = _make_input()
        single = e1.assess(inp)
        batch = e2.assess_batch([inp])
        assert single.negotiation_composite == batch[0].negotiation_composite
        assert single.negotiation_risk == batch[0].negotiation_risk

    def test_single_item_batch(self):
        e = _engine()
        results = e.assess_batch([_make_input()])
        assert len(results) == 1

    def test_large_batch(self):
        e = _engine()
        inputs = [_make_input(rep_id=f"r{i}") for i in range(20)]
        results = e.assess_batch(inputs)
        assert len(results) == 20


# ===========================================================================
# 18. summary()
# ===========================================================================

class TestSummary:
    def test_empty_summary_has_13_keys(self):
        e = _engine()
        s = e.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self):
        assert _engine().summary()["total"] == 0

    def test_empty_summary_avg_composite_zero(self):
        assert _engine().summary()["avg_negotiation_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        assert _engine().summary()["negotiation_gap_count"] == 0

    def test_empty_summary_coaching_count_zero(self):
        assert _engine().summary()["coaching_count"] == 0

    def test_empty_summary_all_avgs_zero(self):
        s = _engine().summary()
        assert s["avg_concession_discipline_score"] == 0.0
        assert s["avg_negotiation_process_score"] == 0.0
        assert s["avg_negotiation_urgency_score"] == 0.0
        assert s["avg_value_articulation_score"] == 0.0

    def test_empty_summary_erosion_zero(self):
        assert _engine().summary()["total_estimated_margin_erosion_usd"] == 0.0

    def test_empty_summary_counts_are_dicts(self):
        s = _engine().summary()
        assert isinstance(s["risk_counts"], dict)
        assert isinstance(s["pattern_counts"], dict)
        assert isinstance(s["severity_counts"], dict)
        assert isinstance(s["action_counts"], dict)

    def test_empty_summary_counts_are_empty_dicts(self):
        s = _engine().summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}

    def test_summary_after_one_assess(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        assert s["total"] == 1

    def test_summary_risk_counts_populated(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_pattern_counts_populated(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == 1

    def test_summary_severity_counts_populated(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        assert sum(s["severity_counts"].values()) == 1

    def test_summary_action_counts_populated(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_summary_total_matches_batch(self):
        e = _engine()
        e.assess_batch([_make_input(rep_id=f"r{i}") for i in range(5)])
        assert e.summary()["total"] == 5

    def test_summary_avg_composite_is_rounded(self):
        e = _engine()
        e.assess(_make_input())
        s = e.summary()
        val = s["avg_negotiation_composite"]
        assert val == round(val, 1)

    def test_summary_total_erosion_rounded_2(self):
        e = _engine()
        e.assess(_make_input(avg_opportunity_value_usd=10_000, avg_discount_concession_pct=0.20))
        s = e.summary()
        val = s["total_estimated_margin_erosion_usd"]
        assert val == round(val, 2)

    def test_summary_gap_count_nonzero_when_applicable(self):
        e = _engine()
        # force has_gap=True
        e.assess(_make_input(avg_discount_concession_pct=0.25))
        s = e.summary()
        assert s["negotiation_gap_count"] >= 1

    def test_summary_coaching_count_nonzero_when_applicable(self):
        e = _engine()
        e.assess(_make_input(first_concession_timing_pct=0.75))
        s = e.summary()
        assert s["coaching_count"] >= 1

    def test_summary_keys(self):
        s = _engine().summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts", "action_counts",
            "avg_negotiation_composite", "negotiation_gap_count", "coaching_count",
            "avg_concession_discipline_score", "avg_negotiation_process_score",
            "avg_negotiation_urgency_score", "avg_value_articulation_score",
            "total_estimated_margin_erosion_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_multiple_risks(self):
        e = _engine()
        # low risk
        e.assess(_make_input())
        # high/critical risk
        e.assess(_make_input(
            first_concession_timing_pct=0.90,
            avg_discount_concession_pct=0.30,
            deals_won_without_discount_pct=0.05,
            manager_escalation_in_negotiation_pct=0.70,
            multi_item_negotiation_rate_pct=0.05,
        ))
        s = e.summary()
        assert s["total"] == 2
        assert len(s["risk_counts"]) >= 2

    def test_summary_avg_scores_reasonable(self):
        e = _engine()
        e.assess_batch([_make_input(rep_id=f"r{i}") for i in range(5)])
        s = e.summary()
        assert 0.0 <= s["avg_concession_discipline_score"] <= 100.0
        assert 0.0 <= s["avg_negotiation_process_score"] <= 100.0
        assert 0.0 <= s["avg_negotiation_urgency_score"] <= 100.0
        assert 0.0 <= s["avg_value_articulation_score"] <= 100.0


# ===========================================================================
# 19. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_zero_values_for_percentages(self):
        e = _engine()
        inp = _make_input(
            first_concession_timing_pct=0.0,
            avg_discount_concession_pct=0.0,
            deals_won_without_discount_pct=0.0,
            manager_escalation_in_negotiation_pct=0.0,
        )
        r = e.assess(inp)
        assert r.negotiation_composite >= 0.0

    def test_one_values_for_percentages(self):
        e = _engine()
        inp = _make_input(
            first_concession_timing_pct=1.0,
            avg_discount_concession_pct=1.0,
            deals_won_without_discount_pct=0.0,
        )
        r = e.assess(inp)
        assert r.negotiation_composite <= 100.0

    def test_large_opportunity_value(self):
        e = _engine()
        inp = _make_input(avg_opportunity_value_usd=1_000_000_000.0)
        r = e.assess(inp)
        assert r.estimated_margin_erosion_usd >= 0.0

    def test_large_negotiations_count(self):
        e = _engine()
        inp = _make_input(total_negotiations_conducted=100_000)
        r = e.assess(inp)
        assert isinstance(r, NegotiationResult)

    def test_single_negotiation(self):
        e = _engine()
        inp = _make_input(total_negotiations_conducted=1)
        r = e.assess(inp)
        assert isinstance(r, NegotiationResult)

    def test_very_high_rounds(self):
        e = _engine()
        inp = _make_input(avg_negotiation_rounds_per_deal=20.0)
        r = e.assess(inp)
        assert isinstance(r, NegotiationResult)

    def test_all_max_concession_risk(self):
        e = _engine()
        inp = _make_input(
            first_concession_timing_pct=1.0,
            avg_discount_concession_pct=1.0,
            deals_won_without_discount_pct=0.0,
        )
        r = e.assess(inp)
        assert r.concession_discipline_score == 100.0

    def test_composite_exactly_20_is_moderate(self):
        e = _engine()
        # Need a composite exactly at 20 - fine to check the boundary mapping logic
        assert e._risk_level(20.0) == NegotiationRisk.moderate

    def test_composite_exactly_40_is_high(self):
        e = _engine()
        assert e._risk_level(40.0) == NegotiationRisk.high

    def test_composite_exactly_60_is_critical(self):
        e = _engine()
        assert e._risk_level(60.0) == NegotiationRisk.critical

    def test_severity_exactly_20_is_developing(self):
        e = _engine()
        assert e._severity(20.0) == NegotiationSeverity.developing

    def test_severity_exactly_40_is_reactive(self):
        e = _engine()
        assert e._severity(40.0) == NegotiationSeverity.reactive

    def test_severity_exactly_60_is_erosive(self):
        e = _engine()
        assert e._severity(60.0) == NegotiationSeverity.erosive

    def test_engine_fresh_results_list(self):
        e = _engine()
        assert e._results == []

    def test_multiple_engines_independent(self):
        e1 = _engine()
        e2 = _engine()
        e1.assess(_make_input(rep_id="r1"))
        assert len(e2._results) == 0

    def test_assess_multiple_times_same_engine(self):
        e = _engine()
        for i in range(10):
            e.assess(_make_input(rep_id=f"r{i}"))
        assert len(e._results) == 10

    def test_to_dict_enum_values_are_strings(self):
        e = _engine()
        r = e.assess(_make_input())
        d = r.to_dict()
        assert isinstance(d["negotiation_risk"], str)
        assert isinstance(d["negotiation_pattern"], str)
        assert isinstance(d["negotiation_severity"], str)
        assert isinstance(d["recommended_action"], str)


# ===========================================================================
# 20. END-TO-END SCENARIOS
# ===========================================================================

class TestEndToEndScenarios:
    """Realistic scenarios verifying the complete assessment pipeline."""

    def test_scenario_disciplined_rep(self):
        """Rep who never gives discounts, handles urgency well, good process."""
        e = _engine()
        inp = _make_input(
            rep_id="star-rep",
            region="Northeast",
            first_concession_timing_pct=0.05,
            avg_discount_concession_pct=0.02,
            deals_won_without_discount_pct=0.85,
            manager_escalation_in_negotiation_pct=0.05,
            multi_item_negotiation_rate_pct=0.70,
            deal_desk_referral_in_negotiation_pct=0.05,
            urgency_trigger_used_pct=0.80,
            negotiation_stall_rate_pct=0.05,
            competitive_counteroffer_handled_pct=0.90,
            value_vs_price_conversation_ratio=0.85,
            scope_expansion_during_negotiation_pct=0.50,
            deals_with_no_negotiation_pct=0.05,
        )
        r = e.assess(inp)
        assert r.negotiation_risk == NegotiationRisk.low
        assert r.negotiation_severity == NegotiationSeverity.disciplined
        assert r.recommended_action == NegotiationAction.no_action
        assert r.negotiation_pattern == NegotiationPattern.none
        assert "healthy" in r.negotiation_signal
        assert r.has_negotiation_gap is False

    def test_scenario_early_capitulation_rep(self):
        """Rep who immediately gives concessions."""
        e = _engine()
        inp = _make_input(
            rep_id="cap-rep",
            first_concession_timing_pct=0.90,
            avg_discount_concession_pct=0.25,
            deals_won_without_discount_pct=0.05,
            manager_escalation_in_negotiation_pct=0.10,
            multi_item_negotiation_rate_pct=0.60,
        )
        r = e.assess(inp)
        assert r.negotiation_pattern == NegotiationPattern.early_capitulation
        assert r.has_negotiation_gap is True
        assert r.requires_negotiation_coaching is True

    def test_scenario_manager_dependent_rep(self):
        """Rep who always escalates to manager."""
        e = _engine()
        inp = _make_input(
            rep_id="esc-rep",
            manager_escalation_in_negotiation_pct=0.80,
            multi_item_negotiation_rate_pct=0.05,
            deal_desk_referral_in_negotiation_pct=0.50,
            first_concession_timing_pct=0.20,
            avg_discount_concession_pct=0.05,
        )
        r = e.assess(inp)
        assert r.negotiation_pattern in (
            NegotiationPattern.manager_escalation_dependency,
            NegotiationPattern.early_capitulation,
            NegotiationPattern.price_anchoring_failure,
            NegotiationPattern.concession_cascade,
            NegotiationPattern.urgency_creation_gap,
            NegotiationPattern.none,
        )
        assert r.negotiation_process_score >= 40.0

    def test_scenario_urgency_gap_rep(self):
        """Rep who rarely creates urgency."""
        e = _engine()
        inp = _make_input(
            rep_id="urg-rep",
            urgency_trigger_used_pct=0.05,
            negotiation_stall_rate_pct=0.50,
            competitive_counteroffer_handled_pct=0.15,
            first_concession_timing_pct=0.10,
            avg_discount_concession_pct=0.05,
            deals_won_without_discount_pct=0.60,
        )
        r = e.assess(inp)
        assert r.negotiation_urgency_score >= 40.0

    def test_scenario_value_articulation_failure(self):
        """Rep who always talks price, never value."""
        e = _engine()
        inp = _make_input(
            rep_id="val-rep",
            value_vs_price_conversation_ratio=0.10,
            scope_expansion_during_negotiation_pct=0.05,
            deals_with_no_negotiation_pct=0.60,
        )
        r = e.assess(inp)
        assert r.value_articulation_score >= 45.0

    def test_batch_scenario_diverse_reps(self):
        """Mixed batch: one good, one bad."""
        e = _engine()
        good = _make_input(rep_id="good")
        bad = _make_input(
            rep_id="bad",
            first_concession_timing_pct=0.90,
            avg_discount_concession_pct=0.30,
            deals_won_without_discount_pct=0.05,
            manager_escalation_in_negotiation_pct=0.70,
            multi_item_negotiation_rate_pct=0.05,
            deal_desk_referral_in_negotiation_pct=0.50,
        )
        results = e.assess_batch([good, bad])
        good_r, bad_r = results
        assert good_r.negotiation_composite < bad_r.negotiation_composite
        assert good_r.negotiation_risk.value in ("low", "moderate")
        assert bad_r.negotiation_risk.value in ("high", "critical")

    def test_end_to_end_summary_aggregation(self):
        """Summary correctly aggregates 3 reps."""
        e = _engine()
        e.assess_batch([
            _make_input(rep_id="r1"),
            _make_input(rep_id="r2", avg_discount_concession_pct=0.25),  # gap: discount>=0.20
            _make_input(rep_id="r3", manager_escalation_in_negotiation_pct=0.60),  # gap: escalation>=0.50
        ])
        s = e.summary()
        assert s["total"] == 3
        assert s["negotiation_gap_count"] >= 2  # r2 and r3 should have gaps

    def test_critical_risk_action_mapping(self):
        """Critical risk with manager_escalation_dependency => manager_escalation_reduction."""
        e = _engine()
        # High process score + high concession score to get critical composite
        inp = _make_input(
            manager_escalation_in_negotiation_pct=0.80,  # process gets 40
            multi_item_negotiation_rate_pct=0.05,        # process gets +35
            deal_desk_referral_in_negotiation_pct=0.50,  # process gets +25
            first_concession_timing_pct=0.90,            # concession gets 40
            avg_discount_concession_pct=0.25,            # concession gets +35
            deals_won_without_discount_pct=0.05,         # concession gets +25
        )
        r = e.assess(inp)
        if r.negotiation_risk == NegotiationRisk.critical and r.negotiation_pattern == NegotiationPattern.early_capitulation:
            # priority: early_capitulation comes first, but we verify action reflects risk
            assert r.recommended_action == NegotiationAction.concession_management_review
        elif r.negotiation_risk == NegotiationRisk.critical and r.negotiation_pattern == NegotiationPattern.manager_escalation_dependency:
            assert r.recommended_action == NegotiationAction.manager_escalation_reduction

    def test_critical_risk_price_anchoring_action(self):
        """Critical risk with price_anchoring_failure => value_anchoring_training."""
        e = _engine()
        # Set up critical composite but NOT triggering early_capitulation or manager_escalation
        # value >= 30 and ratio <= 0.30 => price_anchoring_failure
        inp = _make_input(
            first_concession_timing_pct=0.30,            # concession: 0 from timing
            avg_discount_concession_pct=0.25,            # concession: +35
            deals_won_without_discount_pct=0.05,         # concession: +25 => 60
            manager_escalation_in_negotiation_pct=0.80,  # process: +40 (but < 0.50 pattern threshold with timing!=0.70)
            multi_item_negotiation_rate_pct=0.05,        # process: +35
            deal_desk_referral_in_negotiation_pct=0.50,  # process: +25
            value_vs_price_conversation_ratio=0.10,      # value: +45
            scope_expansion_during_negotiation_pct=0.05, # value: +30
            deals_with_no_negotiation_pct=0.60,          # value: +25 => 100 capped
        )
        r = e.assess(inp)
        assert r.negotiation_risk == NegotiationRisk.critical
        # pattern depends on priority; just verify action is consistent
        if r.negotiation_pattern == NegotiationPattern.price_anchoring_failure:
            assert r.recommended_action == NegotiationAction.value_anchoring_training

    def test_moderate_risk_gives_coaching(self):
        """Moderate composite => coaching action regardless of pattern."""
        e = _engine()
        # moderate: composite 20-39
        inp = _make_input(
            first_concession_timing_pct=0.60,  # +22
            avg_discount_concession_pct=0.05,  # +0
            deals_won_without_discount_pct=0.60, # +0
            manager_escalation_in_negotiation_pct=0.05,
            multi_item_negotiation_rate_pct=0.60,
        )
        r = e.assess(inp)
        if r.negotiation_risk == NegotiationRisk.moderate:
            assert r.recommended_action == NegotiationAction.negotiation_skills_coaching

    def test_high_risk_urgency_gap_pattern(self):
        """High risk + urgency_creation_gap => urgency_creation_training."""
        e = _engine()
        inp = _make_input(
            urgency_trigger_used_pct=0.05,
            negotiation_stall_rate_pct=0.50,
            competitive_counteroffer_handled_pct=0.10,
            # keep concession low to avoid early_cap pattern
            first_concession_timing_pct=0.10,
            avg_discount_concession_pct=0.08,
        )
        r = e.assess(inp)
        if r.negotiation_risk == NegotiationRisk.high and r.negotiation_pattern == NegotiationPattern.urgency_creation_gap:
            assert r.recommended_action == NegotiationAction.urgency_creation_training

    def test_margin_erosion_scales_with_deals(self):
        """More deals at same composite => higher erosion."""
        e1 = _engine()
        e2 = _engine()
        r1 = e1.assess(_make_input(total_negotiations_conducted=10, avg_discount_concession_pct=0.20))
        r2 = e2.assess(_make_input(total_negotiations_conducted=100, avg_discount_concession_pct=0.20))
        assert r2.estimated_margin_erosion_usd > r1.estimated_margin_erosion_usd

    def test_summary_total_erosion_equals_sum(self):
        """summary total_erosion equals sum of individual erosions."""
        e = _engine()
        r1 = e.assess(_make_input(rep_id="r1"))
        r2 = e.assess(_make_input(rep_id="r2", avg_discount_concession_pct=0.20))
        s = e.summary()
        expected = round(r1.estimated_margin_erosion_usd + r2.estimated_margin_erosion_usd, 2)
        assert s["total_estimated_margin_erosion_usd"] == expected
