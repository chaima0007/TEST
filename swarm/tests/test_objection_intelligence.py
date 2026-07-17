"""
Comprehensive tests for swarm/intelligence/objection_intelligence.py

Run from /home/user/TEST:
    python -m pytest swarm/tests/test_objection_intelligence.py -v
"""

from __future__ import annotations

import pytest
from swarm.intelligence.objection_intelligence import (
    ObjectionBurden,
    ObjectionAction,
    ObjectionInput,
    ObjectionResult,
    ObjectionIntelligenceEngine,
    _OBJECTION_WEIGHTS,
    _MAX_RAW,
    _burden_score,
    _resolution_score,
    _objection_burden,
    _objection_action,
    _build_signals,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers / Factories
# ─────────────────────────────────────────────────────────────────────────────

def make_input(
    deal_id: str = "D001",
    deal_name: str = "Test Deal",
    account_name: str = "Acme Corp",
    arr_eur: float = 100_000.0,
    stage: str = "proposal",
    price_objections: int = 0,
    competitor_objections: int = 0,
    authority_objections: int = 0,
    timing_objections: int = 0,
    implementation_objections: int = 0,
    trust_objections: int = 0,
    objections_handled_this_session: int = 0,
    days_oldest_unresolved: int = 0,
    budget_confirmed: bool = False,
    champion_vouched: bool = False,
    case_study_shared: bool = False,
    proof_of_concept_done: bool = False,
    references_provided: bool = False,
    executive_sponsor_engaged: bool = False,
    timeline_agreed: bool = False,
    competitor_named: bool = False,
    evaluated_alternatives: int = 0,
) -> ObjectionInput:
    return ObjectionInput(
        deal_id=deal_id,
        deal_name=deal_name,
        account_name=account_name,
        arr_eur=arr_eur,
        stage=stage,
        price_objections=price_objections,
        competitor_objections=competitor_objections,
        authority_objections=authority_objections,
        timing_objections=timing_objections,
        implementation_objections=implementation_objections,
        trust_objections=trust_objections,
        objections_handled_this_session=objections_handled_this_session,
        days_oldest_unresolved=days_oldest_unresolved,
        budget_confirmed=budget_confirmed,
        champion_vouched=champion_vouched,
        case_study_shared=case_study_shared,
        proof_of_concept_done=proof_of_concept_done,
        references_provided=references_provided,
        executive_sponsor_engaged=executive_sponsor_engaged,
        timeline_agreed=timeline_agreed,
        competitor_named=competitor_named,
        evaluated_alternatives=evaluated_alternatives,
    )


def engine() -> ObjectionIntelligenceEngine:
    return ObjectionIntelligenceEngine()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Constants
# ─────────────────────────────────────────────────────────────────────────────

class TestConstants:
    def test_weights_keys(self):
        expected = {"price", "competitor", "authority", "trust", "timing", "implementation"}
        assert set(_OBJECTION_WEIGHTS.keys()) == expected

    def test_price_weight(self):
        assert _OBJECTION_WEIGHTS["price"] == 22

    def test_competitor_weight(self):
        assert _OBJECTION_WEIGHTS["competitor"] == 18

    def test_authority_weight(self):
        assert _OBJECTION_WEIGHTS["authority"] == 16

    def test_trust_weight(self):
        assert _OBJECTION_WEIGHTS["trust"] == 15

    def test_timing_weight(self):
        assert _OBJECTION_WEIGHTS["timing"] == 15

    def test_implementation_weight(self):
        assert _OBJECTION_WEIGHTS["implementation"] == 14

    def test_max_raw_value(self):
        assert _MAX_RAW == 200

    def test_max_raw_formula(self):
        computed = sum(w * 2 for w in _OBJECTION_WEIGHTS.values())
        assert _MAX_RAW == computed


# ─────────────────────────────────────────────────────────────────────────────
# 2. ObjectionBurden enum
# ─────────────────────────────────────────────────────────────────────────────

class TestObjectionBurdenEnum:
    def test_clear_value(self):
        assert ObjectionBurden.CLEAR == "clear"

    def test_moderate_value(self):
        assert ObjectionBurden.MODERATE == "moderate"

    def test_heavy_value(self):
        assert ObjectionBurden.HEAVY == "heavy"

    def test_critical_value(self):
        assert ObjectionBurden.CRITICAL == "critical"

    def test_four_members(self):
        assert len(ObjectionBurden) == 4

    def test_is_str_enum(self):
        assert isinstance(ObjectionBurden.CLEAR, str)


# ─────────────────────────────────────────────────────────────────────────────
# 3. ObjectionAction enum
# ─────────────────────────────────────────────────────────────────────────────

class TestObjectionActionEnum:
    def test_advance_value(self):
        assert ObjectionAction.ADVANCE == "advance"

    def test_address_value(self):
        assert ObjectionAction.ADDRESS == "address"

    def test_escalate_value(self):
        assert ObjectionAction.ESCALATE == "escalate"

    def test_reassess_value(self):
        assert ObjectionAction.REASSESS == "reassess"

    def test_four_members(self):
        assert len(ObjectionAction) == 4


# ─────────────────────────────────────────────────────────────────────────────
# 4. _objection_burden boundaries
# ─────────────────────────────────────────────────────────────────────────────

class TestObjectionBurdenBoundaries:
    def test_score_0_is_clear(self):
        assert _objection_burden(0.0) == ObjectionBurden.CLEAR

    def test_score_10_is_clear(self):
        assert _objection_burden(10.0) == ObjectionBurden.CLEAR

    def test_score_20_is_clear(self):
        assert _objection_burden(20.0) == ObjectionBurden.CLEAR

    def test_score_21_is_moderate(self):
        assert _objection_burden(21.0) == ObjectionBurden.MODERATE

    def test_score_33_is_moderate(self):
        assert _objection_burden(33.0) == ObjectionBurden.MODERATE

    def test_score_45_is_moderate(self):
        assert _objection_burden(45.0) == ObjectionBurden.MODERATE

    def test_score_46_is_heavy(self):
        assert _objection_burden(46.0) == ObjectionBurden.HEAVY

    def test_score_60_is_heavy(self):
        assert _objection_burden(60.0) == ObjectionBurden.HEAVY

    def test_score_70_is_heavy(self):
        assert _objection_burden(70.0) == ObjectionBurden.HEAVY

    def test_score_71_is_critical(self):
        assert _objection_burden(71.0) == ObjectionBurden.CRITICAL

    def test_score_85_is_critical(self):
        assert _objection_burden(85.0) == ObjectionBurden.CRITICAL

    def test_score_100_is_critical(self):
        assert _objection_burden(100.0) == ObjectionBurden.CRITICAL

    def test_fractional_20_dot_01_is_moderate(self):
        assert _objection_burden(20.01) == ObjectionBurden.MODERATE

    def test_fractional_45_dot_01_is_heavy(self):
        assert _objection_burden(45.01) == ObjectionBurden.HEAVY

    def test_fractional_70_dot_01_is_critical(self):
        assert _objection_burden(70.01) == ObjectionBurden.CRITICAL


# ─────────────────────────────────────────────────────────────────────────────
# 5. _burden_score — basic calculations
# ─────────────────────────────────────────────────────────────────────────────

class TestBurdenScoreBasic:
    def test_no_objections_no_age_returns_zero(self):
        inp = make_input()
        score, primary, total = _burden_score(inp)
        assert score == 0.0
        assert primary == "none"
        assert total == 0

    def test_total_is_sum_of_all_objection_types(self):
        inp = make_input(price_objections=2, competitor_objections=1, trust_objections=3)
        _, _, total = _burden_score(inp)
        assert total == 6

    def test_score_is_float(self):
        inp = make_input(price_objections=1)
        score, _, _ = _burden_score(inp)
        assert isinstance(score, float)

    def test_score_clamped_min_0(self):
        # Max reductions, no objections
        inp = make_input(
            budget_confirmed=True, champion_vouched=True, proof_of_concept_done=True,
            executive_sponsor_engaged=True, timeline_agreed=True,
            case_study_shared=True, references_provided=True,
        )
        score, _, _ = _burden_score(inp)
        assert score >= 0.0

    def test_score_clamped_max_100(self):
        # Worst possible input
        inp = make_input(
            price_objections=10, competitor_objections=10, authority_objections=10,
            timing_objections=10, implementation_objections=10, trust_objections=10,
            days_oldest_unresolved=100,
        )
        score, _, _ = _burden_score(inp)
        assert score <= 100.0

    def test_single_price_objection_raw(self):
        # price=1 → raw = 22; score_raw = 22/200*100 = 11.0; no age/reductions
        inp = make_input(price_objections=1)
        score, primary, total = _burden_score(inp)
        assert score == pytest.approx(11.0, abs=0.01)
        assert primary == "price"
        assert total == 1

    def test_two_price_objections_caps_at_2x_weight(self):
        # price=2 → raw = 44 (= 2*22 = max); price=3 also → 44
        inp2 = make_input(price_objections=2)
        inp3 = make_input(price_objections=3)
        score2, _, _ = _burden_score(inp2)
        score3, _, _ = _burden_score(inp3)
        assert score2 == score3

    def test_cap_is_2x_weight_per_type(self):
        # All types at 2 → raw = 200 → score_raw = 100
        inp = make_input(
            price_objections=2, competitor_objections=2, authority_objections=2,
            trust_objections=2, timing_objections=2, implementation_objections=2,
        )
        score, _, _ = _burden_score(inp)
        # score_raw = 100, age=0, reductions=0 → score=100
        assert score == pytest.approx(100.0, abs=0.01)

    def test_single_competitor_objection(self):
        # competitor=1 → raw=18 → 18/200*100 = 9.0
        inp = make_input(competitor_objections=1)
        score, primary, total = _burden_score(inp)
        assert score == pytest.approx(9.0, abs=0.01)
        assert primary == "competitor"
        assert total == 1

    def test_single_authority_objection(self):
        # authority=1 → raw=16 → 16/200*100 = 8.0
        inp = make_input(authority_objections=1)
        score, primary, _ = _burden_score(inp)
        assert score == pytest.approx(8.0, abs=0.01)
        assert primary == "authority"

    def test_single_trust_objection(self):
        # trust=1 → raw=15 → 7.5
        inp = make_input(trust_objections=1)
        score, primary, _ = _burden_score(inp)
        assert score == pytest.approx(7.5, abs=0.01)
        assert primary == "trust"

    def test_single_timing_objection(self):
        # timing=1 → raw=15 → 7.5
        inp = make_input(timing_objections=1)
        score, primary, _ = _burden_score(inp)
        assert score == pytest.approx(7.5, abs=0.01)
        assert primary == "timing"

    def test_single_implementation_objection(self):
        # implementation=1 → raw=14 → 7.0
        inp = make_input(implementation_objections=1)
        score, primary, _ = _burden_score(inp)
        assert score == pytest.approx(7.0, abs=0.01)
        assert primary == "implementation"


# ─────────────────────────────────────────────────────────────────────────────
# 6. _burden_score — age penalty
# ─────────────────────────────────────────────────────────────────────────────

class TestBurdenScoreAgePenalty:
    def test_no_age_no_penalty(self):
        inp = make_input(days_oldest_unresolved=0)
        score, _, _ = _burden_score(inp)
        assert score == 0.0

    def test_age_1_day_penalty(self):
        # 1 * 1.5 = 1.5
        inp = make_input(days_oldest_unresolved=1)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(1.5, abs=0.01)

    def test_age_5_days_penalty(self):
        # 5 * 1.5 = 7.5
        inp = make_input(days_oldest_unresolved=5)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(7.5, abs=0.01)

    def test_age_10_days_penalty(self):
        # min(15, 10*1.5) = 15
        inp = make_input(days_oldest_unresolved=10)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(15.0, abs=0.01)

    def test_age_penalty_caps_at_15(self):
        # 20 days → min(15, 30) = 15
        inp = make_input(days_oldest_unresolved=20)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(15.0, abs=0.01)

    def test_age_penalty_caps_at_15_large_value(self):
        # 1000 days → still 15
        inp_20 = make_input(days_oldest_unresolved=20)
        inp_1000 = make_input(days_oldest_unresolved=1000)
        score20, _, _ = _burden_score(inp_20)
        score1000, _, _ = _burden_score(inp_1000)
        assert score20 == score1000

    def test_exact_cap_boundary_10_days(self):
        # 10 * 1.5 = 15.0 exactly
        inp = make_input(days_oldest_unresolved=10)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(15.0, abs=0.01)

    def test_9_days_below_cap(self):
        # 9 * 1.5 = 13.5 < 15
        inp = make_input(days_oldest_unresolved=9)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(13.5, abs=0.01)


# ─────────────────────────────────────────────────────────────────────────────
# 7. _burden_score — reductions
# ─────────────────────────────────────────────────────────────────────────────

class TestBurdenScoreReductions:
    def _base_score(self) -> float:
        # price=1 → raw=22 → 11.0; age=0
        return 11.0

    def test_budget_confirmed_reduces_12(self):
        inp = make_input(price_objections=1, budget_confirmed=True)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(max(0.0, self._base_score() - 12.0), abs=0.01)

    def test_champion_vouched_reduces_10(self):
        inp = make_input(price_objections=1, champion_vouched=True)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(max(0.0, self._base_score() - 10.0), abs=0.01)

    def test_poc_done_reduces_8(self):
        inp = make_input(price_objections=1, proof_of_concept_done=True)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(max(0.0, self._base_score() - 8.0), abs=0.01)

    def test_exec_sponsor_reduces_8(self):
        inp = make_input(price_objections=1, executive_sponsor_engaged=True)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(max(0.0, self._base_score() - 8.0), abs=0.01)

    def test_timeline_agreed_reduces_6(self):
        inp = make_input(price_objections=1, timeline_agreed=True)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(max(0.0, self._base_score() - 6.0), abs=0.01)

    def test_case_study_reduces_6(self):
        inp = make_input(price_objections=1, case_study_shared=True)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(max(0.0, self._base_score() - 6.0), abs=0.01)

    def test_references_reduces_5(self):
        inp = make_input(price_objections=1, references_provided=True)
        score, _, _ = _burden_score(inp)
        assert score == pytest.approx(max(0.0, self._base_score() - 5.0), abs=0.01)

    def test_all_reductions_combined(self):
        # All factors → total reduction = 12+10+8+8+6+6+5 = 55
        inp = make_input(
            price_objections=1,
            budget_confirmed=True, champion_vouched=True, proof_of_concept_done=True,
            executive_sponsor_engaged=True, timeline_agreed=True,
            case_study_shared=True, references_provided=True,
        )
        score, _, _ = _burden_score(inp)
        # 11.0 - 55 = -44 → clamped to 0
        assert score == 0.0

    def test_reductions_floor_at_zero(self):
        inp = make_input(
            budget_confirmed=True, champion_vouched=True, proof_of_concept_done=True,
            executive_sponsor_engaged=True, timeline_agreed=True,
            case_study_shared=True, references_provided=True,
        )
        score, _, _ = _burden_score(inp)
        assert score >= 0.0

    def test_all_reductions_total_55(self):
        # Verify total reduction value
        total_reduction = 12 + 10 + 8 + 8 + 6 + 6 + 5
        assert total_reduction == 55


# ─────────────────────────────────────────────────────────────────────────────
# 8. _burden_score — primary objection type
# ─────────────────────────────────────────────────────────────────────────────

class TestBurdenScorePrimaryType:
    def test_no_objections_primary_is_none(self):
        inp = make_input()
        _, primary, _ = _burden_score(inp)
        assert primary == "none"

    def test_only_price_primary_is_price(self):
        inp = make_input(price_objections=1)
        _, primary, _ = _burden_score(inp)
        assert primary == "price"

    def test_only_competitor_primary_is_competitor(self):
        inp = make_input(competitor_objections=1)
        _, primary, _ = _burden_score(inp)
        assert primary == "competitor"

    def test_only_authority_primary_is_authority(self):
        inp = make_input(authority_objections=1)
        _, primary, _ = _burden_score(inp)
        assert primary == "authority"

    def test_only_trust_primary_is_trust(self):
        inp = make_input(trust_objections=1)
        _, primary, _ = _burden_score(inp)
        assert primary == "trust"

    def test_only_timing_primary_is_timing(self):
        inp = make_input(timing_objections=1)
        _, primary, _ = _burden_score(inp)
        assert primary == "timing"

    def test_only_implementation_primary_is_implementation(self):
        inp = make_input(implementation_objections=1)
        _, primary, _ = _burden_score(inp)
        assert primary == "implementation"

    def test_primary_is_max_by_weighted_count(self):
        # price=1 → 1*22=22; competitor=1 → 1*18=18 → price wins
        inp = make_input(price_objections=1, competitor_objections=1)
        _, primary, _ = _burden_score(inp)
        assert primary == "price"

    def test_primary_type_is_valid_string(self):
        valid = {"price", "competitor", "authority", "trust", "timing", "implementation"}
        inp = make_input(price_objections=2, competitor_objections=3)
        _, primary, _ = _burden_score(inp)
        assert primary in valid

    def test_high_count_low_weight_vs_low_count_high_weight(self):
        # implementation=5 → 5*14=70; price=2 → 2*22=44 (capped) but raw already 44
        # For primary: count*weight comparison: impl=5*14=70 > price=2*22=44 → impl wins
        inp = make_input(implementation_objections=5, price_objections=2)
        _, primary, _ = _burden_score(inp)
        assert primary == "implementation"


# ─────────────────────────────────────────────────────────────────────────────
# 9. _resolution_score
# ─────────────────────────────────────────────────────────────────────────────

class TestResolutionScore:
    def test_zero_total_returns_100(self):
        inp = make_input()
        score = _resolution_score(inp, 0)
        assert isinstance(score, (int, float))
        assert score == 100.0

    def test_returns_float_type(self):
        inp = make_input(price_objections=1)
        score = _resolution_score(inp, 1)
        assert isinstance(score, (int, float))

    def test_no_handled_base_zero(self):
        # total=4, handled=0 → base=0
        inp = make_input(price_objections=4)
        score = _resolution_score(inp, 4)
        assert score == 0.0

    def test_all_handled_base_50(self):
        # total=4, handled=4 → base=50
        inp = make_input(price_objections=4, objections_handled_this_session=4)
        score = _resolution_score(inp, 4)
        assert score == pytest.approx(50.0, abs=0.01)

    def test_handled_capped_at_total(self):
        # handled=10 > total=4 → use 4
        inp = make_input(price_objections=4, objections_handled_this_session=10)
        score = _resolution_score(inp, 4)
        assert score == pytest.approx(50.0, abs=0.01)

    def test_half_handled_base_25(self):
        inp = make_input(price_objections=4, objections_handled_this_session=2)
        score = _resolution_score(inp, 4)
        assert score == pytest.approx(25.0, abs=0.01)

    def test_budget_confirmed_adds_12(self):
        inp = make_input(price_objections=4, budget_confirmed=True)
        score = _resolution_score(inp, 4)
        assert score == pytest.approx(12.0, abs=0.01)

    def test_champion_vouched_adds_10(self):
        inp = make_input(price_objections=4, champion_vouched=True)
        score = _resolution_score(inp, 4)
        assert score == pytest.approx(10.0, abs=0.01)

    def test_poc_done_adds_10(self):
        inp = make_input(price_objections=4, proof_of_concept_done=True)
        score = _resolution_score(inp, 4)
        assert score == pytest.approx(10.0, abs=0.01)

    def test_timeline_agreed_adds_8(self):
        inp = make_input(price_objections=4, timeline_agreed=True)
        score = _resolution_score(inp, 4)
        assert score == pytest.approx(8.0, abs=0.01)

    def test_case_study_adds_6(self):
        inp = make_input(price_objections=4, case_study_shared=True)
        score = _resolution_score(inp, 4)
        assert score == pytest.approx(6.0, abs=0.01)

    def test_references_adds_4(self):
        inp = make_input(price_objections=4, references_provided=True)
        score = _resolution_score(inp, 4)
        assert score == pytest.approx(4.0, abs=0.01)

    def test_all_bonuses_combined(self):
        # base=50 + 12+10+10+8+6+4 = 50+50=100
        inp = make_input(
            price_objections=4, objections_handled_this_session=4,
            budget_confirmed=True, champion_vouched=True, proof_of_concept_done=True,
            timeline_agreed=True, case_study_shared=True, references_provided=True,
        )
        score = _resolution_score(inp, 4)
        assert score == pytest.approx(100.0, abs=0.01)

    def test_score_capped_at_100(self):
        # Overflow: base=50, all bonuses=50 → 100, capped
        inp = make_input(
            price_objections=1, objections_handled_this_session=10,
            budget_confirmed=True, champion_vouched=True, proof_of_concept_done=True,
            timeline_agreed=True, case_study_shared=True, references_provided=True,
        )
        score = _resolution_score(inp, 1)
        assert score <= 100.0

    def test_score_floored_at_0(self):
        inp = make_input(price_objections=4)
        score = _resolution_score(inp, 4)
        assert score >= 0.0

    def test_partial_bonuses(self):
        # base=0 + budget(12) + poc(10) = 22
        inp = make_input(price_objections=2, budget_confirmed=True, proof_of_concept_done=True)
        score = _resolution_score(inp, 2)
        assert score == pytest.approx(22.0, abs=0.01)


# ─────────────────────────────────────────────────────────────────────────────
# 10. _objection_action
# ─────────────────────────────────────────────────────────────────────────────

class TestObjectionAction:
    def test_critical_always_reassess(self):
        inp = make_input()
        action = _objection_action(inp, ObjectionBurden.CRITICAL)
        assert action == ObjectionAction.REASSESS

    def test_critical_even_with_mitigations(self):
        inp = make_input(
            budget_confirmed=True, champion_vouched=True,
            proof_of_concept_done=True, executive_sponsor_engaged=True,
        )
        action = _objection_action(inp, ObjectionBurden.CRITICAL)
        assert action == ObjectionAction.REASSESS

    def test_heavy_with_authority_escalates(self):
        inp = make_input(authority_objections=1)
        action = _objection_action(inp, ObjectionBurden.HEAVY)
        assert action == ObjectionAction.ESCALATE

    def test_heavy_with_competitor_gt_1_escalates(self):
        inp = make_input(competitor_objections=2)
        action = _objection_action(inp, ObjectionBurden.HEAVY)
        assert action == ObjectionAction.ESCALATE

    def test_heavy_with_competitor_eq_1_does_not_escalate(self):
        # competitor=1, no authority, alternatives<2 → ADDRESS
        inp = make_input(competitor_objections=1)
        action = _objection_action(inp, ObjectionBurden.HEAVY)
        assert action == ObjectionAction.ADDRESS

    def test_heavy_with_alternatives_ge_2_escalates(self):
        inp = make_input(evaluated_alternatives=2)
        action = _objection_action(inp, ObjectionBurden.HEAVY)
        assert action == ObjectionAction.ESCALATE

    def test_heavy_with_alternatives_lt_2_no_authority_no_competitor(self):
        inp = make_input(evaluated_alternatives=1)
        action = _objection_action(inp, ObjectionBurden.HEAVY)
        assert action == ObjectionAction.ADDRESS

    def test_heavy_no_escalation_conditions_addresses(self):
        inp = make_input()
        action = _objection_action(inp, ObjectionBurden.HEAVY)
        assert action == ObjectionAction.ADDRESS

    def test_moderate_always_address(self):
        inp = make_input()
        action = _objection_action(inp, ObjectionBurden.MODERATE)
        assert action == ObjectionAction.ADDRESS

    def test_moderate_with_authority_still_address(self):
        # ESCALATE condition only applies to HEAVY
        inp = make_input(authority_objections=1, evaluated_alternatives=5)
        action = _objection_action(inp, ObjectionBurden.MODERATE)
        assert action == ObjectionAction.ADDRESS

    def test_clear_always_advance(self):
        inp = make_input()
        action = _objection_action(inp, ObjectionBurden.CLEAR)
        assert action == ObjectionAction.ADVANCE

    def test_clear_with_objections_still_advance(self):
        inp = make_input(price_objections=1)
        action = _objection_action(inp, ObjectionBurden.CLEAR)
        assert action == ObjectionAction.ADVANCE

    def test_heavy_with_all_three_escalation_conditions(self):
        inp = make_input(authority_objections=1, competitor_objections=2, evaluated_alternatives=3)
        action = _objection_action(inp, ObjectionBurden.HEAVY)
        assert action == ObjectionAction.ESCALATE


# ─────────────────────────────────────────────────────────────────────────────
# 11. _build_signals — risks
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildSignalsRisks:
    def test_no_objections_no_risks(self):
        inp = make_input()
        risks, _, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert risks == []

    def test_price_objection_adds_risk(self):
        inp = make_input(price_objections=1)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 1, "price")
        assert any("prix" in r.lower() or "price" in r.lower() for r in risks)

    def test_price_with_no_budget_mentions_budget(self):
        inp = make_input(price_objections=2, budget_confirmed=False)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 2, "price")
        price_risks = [r for r in risks if "prix" in r.lower()]
        assert len(price_risks) == 1
        # Should mention budget not confirmed
        assert "budget" in price_risks[0].lower() or "non confirmé" in price_risks[0]

    def test_competitor_objection_adds_risk(self):
        inp = make_input(competitor_objections=1)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 1, "competitor")
        assert any("concurrent" in r.lower() for r in risks)

    def test_authority_objection_adds_risk(self):
        inp = make_input(authority_objections=2)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 2, "authority")
        assert any("autorité" in r.lower() or "prenante" in r.lower() for r in risks)

    def test_timing_objection_adds_risk(self):
        inp = make_input(timing_objections=1)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 1, "timing")
        assert any("timing" in r.lower() for r in risks)

    def test_implementation_objection_adds_risk(self):
        inp = make_input(implementation_objections=1)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 1, "implementation")
        assert any("implémentation" in r.lower() for r in risks)

    def test_trust_objection_adds_risk(self):
        inp = make_input(trust_objections=1)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 1, "trust")
        assert any("confiance" in r.lower() or "crédibilité" in r.lower() for r in risks)

    def test_days_gt_14_stagnation_risk(self):
        inp = make_input(days_oldest_unresolved=15)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert any("stagnation" in r.lower() for r in risks)

    def test_days_gt_7_lte_14_persisting_risk(self):
        inp = make_input(days_oldest_unresolved=10)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert any("persistante" in r.lower() for r in risks)

    def test_days_7_no_persisting_risk(self):
        inp = make_input(days_oldest_unresolved=7)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert not any("persistante" in r.lower() for r in risks)

    def test_days_14_no_stagnation_risk(self):
        inp = make_input(days_oldest_unresolved=14)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert not any("stagnation" in r.lower() for r in risks)

    def test_evaluated_alternatives_ge_3_strong_competition_risk(self):
        inp = make_input(evaluated_alternatives=3)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert any("forte concurrence" in r.lower() or "alternative" in r.lower() for r in risks)

    def test_evaluated_alternatives_2_no_strong_competition_risk(self):
        inp = make_input(evaluated_alternatives=2)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert not any("forte concurrence" in r.lower() for r in risks)

    def test_critical_no_exec_sponsor_adds_risk(self):
        inp = make_input(executive_sponsor_engaged=False)
        risks, _, _ = _build_signals(inp, ObjectionBurden.CRITICAL, 0, "none")
        assert any("sponsor" in r.lower() or "exécutif" in r.lower() for r in risks)

    def test_critical_with_exec_sponsor_no_sponsor_risk(self):
        inp = make_input(executive_sponsor_engaged=True)
        risks, _, _ = _build_signals(inp, ObjectionBurden.CRITICAL, 0, "none")
        assert not any("sponsor exécutif non activé" in r.lower() for r in risks)

    def test_non_critical_no_exec_sponsor_no_sponsor_risk(self):
        inp = make_input(executive_sponsor_engaged=False)
        risks, _, _ = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert not any("sponsor exécutif non activé" in r for r in risks)


# ─────────────────────────────────────────────────────────────────────────────
# 12. _build_signals — mitigations
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildSignalsMitigations:
    def test_no_mitigations_when_none_present(self):
        inp = make_input()
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert mitigations == []

    def test_budget_confirmed_mitigation(self):
        inp = make_input(budget_confirmed=True)
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("budget" in m.lower() for m in mitigations)

    def test_champion_vouched_mitigation(self):
        inp = make_input(champion_vouched=True)
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("champion" in m.lower() for m in mitigations)

    def test_poc_done_mitigation(self):
        inp = make_input(proof_of_concept_done=True)
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("poc" in m.lower() for m in mitigations)

    def test_exec_sponsor_mitigation(self):
        inp = make_input(executive_sponsor_engaged=True)
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("sponsor" in m.lower() for m in mitigations)

    def test_case_study_mitigation(self):
        inp = make_input(case_study_shared=True)
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("case" in m.lower() or "business" in m.lower() for m in mitigations)

    def test_references_mitigation(self):
        inp = make_input(references_provided=True)
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("référence" in m.lower() or "référen" in m.lower() for m in mitigations)

    def test_timeline_agreed_mitigation(self):
        inp = make_input(timeline_agreed=True)
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("timeline" in m.lower() for m in mitigations)

    def test_objections_handled_this_session_mitigation(self):
        inp = make_input(objections_handled_this_session=3)
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("3" in m for m in mitigations)

    def test_zero_handled_no_session_mitigation(self):
        inp = make_input(objections_handled_this_session=0)
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert not any("session" in m.lower() for m in mitigations)

    def test_all_mitigations_present(self):
        inp = make_input(
            budget_confirmed=True, champion_vouched=True, proof_of_concept_done=True,
            executive_sponsor_engaged=True, case_study_shared=True,
            references_provided=True, timeline_agreed=True,
            objections_handled_this_session=2,
        )
        _, mitigations, _ = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert len(mitigations) == 8


# ─────────────────────────────────────────────────────────────────────────────
# 13. _build_signals — tactics
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildSignalsTactics:
    def test_no_tactics_clean_proposal(self):
        inp = make_input(stage="demo")
        _, _, tactics = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert tactics == []

    def test_no_objections_proposal_stage_tactic(self):
        inp = make_input(stage="proposal")
        _, _, tactics = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("contractuel" in t.lower() or "next" in t.lower() for t in tactics)

    def test_no_objections_negotiation_stage_tactic(self):
        inp = make_input(stage="negotiation")
        _, _, tactics = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("contractuel" in t.lower() for t in tactics)

    def test_no_objections_closing_stage_tactic(self):
        inp = make_input(stage="closing")
        _, _, tactics = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert any("contractuel" in t.lower() for t in tactics)

    def test_no_objections_qualification_stage_no_contract_tactic(self):
        inp = make_input(stage="qualification")
        _, _, tactics = _build_signals(inp, ObjectionBurden.CLEAR, 0, "none")
        assert not any("contractuel" in t.lower() for t in tactics)

    def test_price_no_budget_tactic(self):
        inp = make_input(price_objections=1, budget_confirmed=False)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 1, "price")
        assert any("roi" in t.lower() or "budget" in t.lower() for t in tactics)

    def test_price_with_budget_no_roi_tactic(self):
        inp = make_input(price_objections=1, budget_confirmed=True)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 1, "price")
        assert not any("roi" in t.lower() and "budget" in t.lower() for t in tactics)

    def test_competitor_named_battlecard_tactic(self):
        inp = make_input(competitor_objections=1, competitor_named=True)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 1, "competitor")
        assert any("battle" in t.lower() for t in tactics)

    def test_competitor_not_named_identify_tactic(self):
        inp = make_input(competitor_objections=1, competitor_named=False)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 1, "competitor")
        assert any("identifier" in t.lower() for t in tactics)

    def test_authority_no_exec_sponsor_tactic(self):
        inp = make_input(authority_objections=1, executive_sponsor_engaged=False)
        _, _, tactics = _build_signals(inp, ObjectionBurden.HEAVY, 1, "authority")
        assert any("sponsor" in t.lower() or "exécutif" in t.lower() for t in tactics)

    def test_authority_with_exec_sponsor_no_sponsor_tactic(self):
        inp = make_input(authority_objections=1, executive_sponsor_engaged=True)
        _, _, tactics = _build_signals(inp, ObjectionBurden.HEAVY, 1, "authority")
        assert not any("activer le sponsor" in t.lower() for t in tactics)

    def test_timing_no_timeline_tactic(self):
        inp = make_input(timing_objections=1, timeline_agreed=False)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 1, "timing")
        assert any("urgency" in t.lower() or "timing" in t.lower() for t in tactics)

    def test_timing_with_timeline_no_urgency_tactic(self):
        inp = make_input(timing_objections=1, timeline_agreed=True)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 1, "timing")
        assert not any("urgency" in t.lower() for t in tactics)

    def test_implementation_no_poc_tactic(self):
        inp = make_input(implementation_objections=1, proof_of_concept_done=False)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 1, "implementation")
        assert any("poc" in t.lower() for t in tactics)

    def test_implementation_with_poc_no_poc_tactic(self):
        inp = make_input(implementation_objections=1, proof_of_concept_done=True)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 1, "implementation")
        assert not any("poc" in t.lower() for t in tactics)

    def test_trust_no_references_tactic(self):
        inp = make_input(trust_objections=1, references_provided=False)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 1, "trust")
        assert any("référence" in t.lower() for t in tactics)

    def test_trust_no_case_study_tactic(self):
        inp = make_input(trust_objections=1, case_study_shared=False)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 1, "trust")
        assert any("business case" in t.lower() or "cas" in t.lower() for t in tactics)

    def test_days_gt_7_followup_tactic(self):
        inp = make_input(days_oldest_unresolved=8)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert any("suivi" in t.lower() or "appel" in t.lower() for t in tactics)

    def test_days_7_no_followup_tactic(self):
        inp = make_input(days_oldest_unresolved=7)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert not any("suivi" in t.lower() for t in tactics)

    def test_alternatives_ge_2_criteria_tactic(self):
        inp = make_input(evaluated_alternatives=2)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert any("critère" in t.lower() or "sélection" in t.lower() for t in tactics)

    def test_alternatives_lt_2_no_criteria_tactic(self):
        inp = make_input(evaluated_alternatives=1)
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert not any("critère" in t.lower() for t in tactics)

    def test_critical_burden_icp_tactic(self):
        inp = make_input()
        _, _, tactics = _build_signals(inp, ObjectionBurden.CRITICAL, 0, "none")
        assert any("icp" in t.lower() for t in tactics)

    def test_non_critical_no_icp_tactic(self):
        inp = make_input()
        _, _, tactics = _build_signals(inp, ObjectionBurden.MODERATE, 0, "none")
        assert not any("icp" in t.lower() for t in tactics)


# ─────────────────────────────────────────────────────────────────────────────
# 14. ObjectionResult dataclass
# ─────────────────────────────────────────────────────────────────────────────

class TestObjectionResult:
    def _make_result(self) -> ObjectionResult:
        eng = engine()
        inp = make_input(price_objections=1, arr_eur=50_000.0)
        return eng.analyze(inp)

    def test_result_has_deal_id(self):
        r = self._make_result()
        assert r.deal_id == "D001"

    def test_result_has_burden_score(self):
        r = self._make_result()
        assert isinstance(r.burden_score, (int, float))

    def test_result_has_objection_burden(self):
        r = self._make_result()
        assert isinstance(r.objection_burden, ObjectionBurden)

    def test_result_has_objection_action(self):
        r = self._make_result()
        assert isinstance(r.objection_action, ObjectionAction)

    def test_result_deal_impact_eur_computed(self):
        r = self._make_result()
        expected = round(50_000.0 * r.burden_score / 100.0, 2)
        assert r.deal_impact_eur == pytest.approx(expected, abs=0.01)

    def test_result_total_active_objections(self):
        eng = engine()
        inp = make_input(price_objections=2, trust_objections=1)
        r = eng.analyze(inp)
        assert r.total_active_objections == 3

    def test_result_resolution_score_type(self):
        r = self._make_result()
        assert isinstance(r.resolution_score, (int, float))

    def test_result_risk_factors_list(self):
        r = self._make_result()
        assert isinstance(r.risk_factors, list)

    def test_result_mitigating_factors_list(self):
        r = self._make_result()
        assert isinstance(r.mitigating_factors, list)

    def test_result_recommended_tactics_list(self):
        r = self._make_result()
        assert isinstance(r.recommended_tactics, list)

    def test_to_dict_returns_dict(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d, dict)

    def test_to_dict_burden_is_string(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d["objection_burden"], str)

    def test_to_dict_action_is_string(self):
        r = self._make_result()
        d = r.to_dict()
        assert isinstance(d["objection_action"], str)

    def test_to_dict_all_expected_keys(self):
        r = self._make_result()
        d = r.to_dict()
        for key in [
            "deal_id", "deal_name", "account_name", "arr_eur", "stage",
            "objection_burden", "objection_action", "burden_score",
            "total_active_objections", "resolution_score", "primary_objection_type",
            "deal_impact_eur", "risk_factors", "mitigating_factors", "recommended_tactics",
        ]:
            assert key in d


# ─────────────────────────────────────────────────────────────────────────────
# 15. ObjectionIntelligenceEngine — analyze
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineAnalyze:
    def test_analyze_returns_result(self):
        eng = engine()
        inp = make_input()
        result = eng.analyze(inp)
        assert isinstance(result, ObjectionResult)

    def test_analyze_stores_result(self):
        eng = engine()
        inp = make_input()
        eng.analyze(inp)
        assert eng.get("D001") is not None

    def test_analyze_overwrites_existing(self):
        eng = engine()
        inp1 = make_input(price_objections=0)
        inp2 = make_input(price_objections=2)
        eng.analyze(inp1)
        eng.analyze(inp2)
        result = eng.get("D001")
        assert result.total_active_objections == 2

    def test_analyze_correct_burden_clear(self):
        eng = engine()
        inp = make_input()
        r = eng.analyze(inp)
        assert r.objection_burden == ObjectionBurden.CLEAR

    def test_analyze_correct_burden_critical(self):
        eng = engine()
        # All objections=2, no mitigations → score=100 → CRITICAL
        inp = make_input(
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
        )
        r = eng.analyze(inp)
        assert r.objection_burden == ObjectionBurden.CRITICAL

    def test_analyze_deal_impact_computed(self):
        eng = engine()
        inp = make_input(arr_eur=200_000.0, price_objections=2)
        r = eng.analyze(inp)
        expected = round(200_000.0 * r.burden_score / 100.0, 2)
        assert r.deal_impact_eur == pytest.approx(expected, abs=0.01)


# ─────────────────────────────────────────────────────────────────────────────
# 16. ObjectionIntelligenceEngine — analyze_batch
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineAnalyzeBatch:
    def test_batch_returns_list(self):
        eng = engine()
        results = eng.analyze_batch([make_input(deal_id="A"), make_input(deal_id="B")])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_batch_sorted_desc_by_burden_score(self):
        eng = engine()
        low = make_input(deal_id="LOW")
        high = make_input(deal_id="HIGH", price_objections=2, competitor_objections=2)
        results = eng.analyze_batch([low, high])
        scores = [r.burden_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_batch_stores_all_results(self):
        eng = engine()
        eng.analyze_batch([make_input(deal_id="X1"), make_input(deal_id="X2"), make_input(deal_id="X3")])
        assert eng.get("X1") is not None
        assert eng.get("X2") is not None
        assert eng.get("X3") is not None

    def test_batch_empty_list(self):
        eng = engine()
        results = eng.analyze_batch([])
        assert results == []

    def test_batch_single_item(self):
        eng = engine()
        results = eng.analyze_batch([make_input()])
        assert len(results) == 1


# ─────────────────────────────────────────────────────────────────────────────
# 17. ObjectionIntelligenceEngine — get, all_deals
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineGetAllDeals:
    def test_get_returns_none_for_unknown(self):
        eng = engine()
        assert eng.get("UNKNOWN") is None

    def test_get_returns_result_after_analyze(self):
        eng = engine()
        eng.analyze(make_input(deal_id="D99"))
        assert eng.get("D99") is not None

    def test_all_deals_empty_initially(self):
        eng = engine()
        assert eng.all_deals() == []

    def test_all_deals_returns_all(self):
        eng = engine()
        eng.analyze(make_input(deal_id="A"))
        eng.analyze(make_input(deal_id="B"))
        eng.analyze(make_input(deal_id="C"))
        assert len(eng.all_deals()) == 3

    def test_all_deals_sorted_desc_by_burden_score(self):
        eng = engine()
        eng.analyze(make_input(deal_id="LOW"))
        eng.analyze(make_input(deal_id="HIGH", price_objections=2, competitor_objections=2))
        results = eng.all_deals()
        scores = [r.burden_score for r in results]
        assert scores == sorted(scores, reverse=True)


# ─────────────────────────────────────────────────────────────────────────────
# 18. ObjectionIntelligenceEngine — filtering methods
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineFilteringMethods:
    def _setup_mixed_engine(self) -> ObjectionIntelligenceEngine:
        eng = engine()
        # CLEAR: no objections
        eng.analyze(make_input(deal_id="CLEAR1"))
        eng.analyze(make_input(deal_id="CLEAR2"))
        # MODERATE: 1 price objection → ~11 score → CLEAR actually,
        # Let's force moderate: 1 price + age penalty
        eng.analyze(make_input(deal_id="MOD1", price_objections=1, competitor_objections=1, days_oldest_unresolved=0))
        # HEAVY: needs ~46-70 score range
        eng.analyze(make_input(
            deal_id="HEAVY1",
            price_objections=2, competitor_objections=2,
            days_oldest_unresolved=0,
        ))
        # CRITICAL: max objections
        eng.analyze(make_input(
            deal_id="CRIT1",
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
        ))
        return eng

    def test_by_burden_returns_correct_subset(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CRIT",
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
        ))
        eng.analyze(make_input(deal_id="CLR"))
        criticals = eng.by_burden(ObjectionBurden.CRITICAL)
        assert all(r.objection_burden == ObjectionBurden.CRITICAL for r in criticals)

    def test_critical_method(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CRIT",
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
        ))
        criticals = eng.critical()
        assert len(criticals) >= 1
        assert all(r.objection_burden == ObjectionBurden.CRITICAL for r in criticals)

    def test_heavy_method(self):
        eng = engine()
        # Force a heavy score: price=2 (44), competitor=2 (36) → raw=80, score=40 → not heavy
        # Need higher: price=2+competitor=2+authority=2 → raw=44+36+32=112 → 56% → 56 → HEAVY
        eng.analyze(make_input(deal_id="HVY",
            price_objections=2, competitor_objections=2, authority_objections=2,
        ))
        heavy = eng.heavy()
        assert all(r.objection_burden == ObjectionBurden.HEAVY for r in heavy)

    def test_at_risk_includes_critical_and_heavy(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CRIT",
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
        ))
        eng.analyze(make_input(deal_id="CLR"))
        at_risk = eng.at_risk()
        assert all(r.objection_burden in (ObjectionBurden.CRITICAL, ObjectionBurden.HEAVY) for r in at_risk)

    def test_clear_method(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CLR"))
        clears = eng.clear()
        assert len(clears) >= 1
        assert all(r.objection_burden == ObjectionBurden.CLEAR for r in clears)

    def test_needs_escalation_escalate_or_reassess(self):
        eng = engine()
        # CRITICAL → REASSESS
        eng.analyze(make_input(deal_id="CRIT",
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
        ))
        escalation_needed = eng.needs_escalation()
        assert all(r.objection_action in (ObjectionAction.ESCALATE, ObjectionAction.REASSESS)
                   for r in escalation_needed)

    def test_ready_to_advance_advance_only(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CLR"))
        ready = eng.ready_to_advance()
        assert all(r.objection_action == ObjectionAction.ADVANCE for r in ready)

    def test_by_primary_objection(self):
        eng = engine()
        eng.analyze(make_input(deal_id="P1", price_objections=2))
        eng.analyze(make_input(deal_id="P2", price_objections=1))
        eng.analyze(make_input(deal_id="C1", competitor_objections=2))
        price_deals = eng.by_primary_objection("price")
        assert all(r.primary_objection_type == "price" for r in price_deals)

    def test_by_primary_objection_none(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CLEAN"))
        none_deals = eng.by_primary_objection("none")
        assert len(none_deals) >= 1

    def test_top_n_by_impact(self):
        eng = engine()
        eng.analyze(make_input(deal_id="A", arr_eur=10_000.0))
        eng.analyze(make_input(deal_id="B", arr_eur=500_000.0, price_objections=2))
        eng.analyze(make_input(deal_id="C", arr_eur=100_000.0, competitor_objections=1))
        top2 = eng.top_n_by_impact(2)
        assert len(top2) == 2
        assert top2[0].deal_impact_eur >= top2[1].deal_impact_eur

    def test_top_n_exceeds_total(self):
        eng = engine()
        eng.analyze(make_input(deal_id="A"))
        top5 = eng.top_n_by_impact(5)
        assert len(top5) == 1


# ─────────────────────────────────────────────────────────────────────────────
# 19. ObjectionIntelligenceEngine — financial metrics
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineFinancialMetrics:
    def test_total_arr_impacted_eur_empty(self):
        eng = engine()
        assert eng.total_arr_impacted_eur() == 0.0

    def test_total_arr_impacted_eur_is_sum_of_deal_impacts(self):
        eng = engine()
        inp1 = make_input(deal_id="A", arr_eur=100_000.0, price_objections=1)
        inp2 = make_input(deal_id="B", arr_eur=200_000.0, competitor_objections=1)
        r1 = eng.analyze(inp1)
        r2 = eng.analyze(inp2)
        expected = round(r1.deal_impact_eur + r2.deal_impact_eur, 2)
        assert eng.total_arr_impacted_eur() == pytest.approx(expected, abs=0.01)

    def test_total_arr_at_risk_eur_empty(self):
        eng = engine()
        assert eng.total_arr_at_risk_eur() == 0.0

    def test_total_arr_at_risk_eur_critical_only(self):
        eng = engine()
        # CRITICAL deal
        inp = make_input(deal_id="CRIT", arr_eur=300_000.0,
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
        )
        r = eng.analyze(inp)
        assert r.objection_burden == ObjectionBurden.CRITICAL
        assert eng.total_arr_at_risk_eur() == pytest.approx(300_000.0, abs=0.01)

    def test_total_arr_at_risk_eur_excludes_clear(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CLR", arr_eur=50_000.0))
        assert eng.total_arr_at_risk_eur() == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 20. ObjectionIntelligenceEngine — average scores
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineAverageScores:
    def test_avg_burden_score_empty_returns_0(self):
        eng = engine()
        assert eng.avg_burden_score() == 0.0

    def test_avg_resolution_score_empty_returns_0(self):
        eng = engine()
        assert eng.avg_resolution_score() == 0.0

    def test_avg_burden_score_single_deal(self):
        eng = engine()
        inp = make_input(price_objections=1)
        r = eng.analyze(inp)
        assert eng.avg_burden_score() == pytest.approx(r.burden_score, abs=0.1)

    def test_avg_resolution_score_single_deal(self):
        eng = engine()
        inp = make_input()
        r = eng.analyze(inp)
        assert eng.avg_resolution_score() == pytest.approx(r.resolution_score, abs=0.1)

    def test_avg_burden_score_multiple_deals(self):
        eng = engine()
        inp1 = make_input(deal_id="A", price_objections=1)
        inp2 = make_input(deal_id="B", price_objections=2)
        r1 = eng.analyze(inp1)
        r2 = eng.analyze(inp2)
        expected = round((r1.burden_score + r2.burden_score) / 2.0, 1)
        assert eng.avg_burden_score() == pytest.approx(expected, abs=0.1)


# ─────────────────────────────────────────────────────────────────────────────
# 21. ObjectionIntelligenceEngine — summary
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineSummary:
    def test_summary_empty(self):
        eng = engine()
        s = eng.summary()
        assert s["total"] == 0
        assert s["burden_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_burden_score"] == 0.0
        assert s["avg_resolution_score"] == 0.0
        assert s["total_arr_impacted_eur"] == 0.0
        assert s["total_arr_at_risk_eur"] == 0.0
        assert s["critical_count"] == 0
        assert s["escalation_count"] == 0
        assert s["advance_ready_count"] == 0

    def test_summary_all_keys_present(self):
        eng = engine()
        eng.analyze(make_input())
        s = eng.summary()
        for key in [
            "total", "burden_counts", "action_counts",
            "avg_burden_score", "avg_resolution_score",
            "total_arr_impacted_eur", "total_arr_at_risk_eur",
            "critical_count", "escalation_count", "advance_ready_count",
        ]:
            assert key in s

    def test_summary_total_count(self):
        eng = engine()
        eng.analyze(make_input(deal_id="A"))
        eng.analyze(make_input(deal_id="B"))
        eng.analyze(make_input(deal_id="C"))
        s = eng.summary()
        assert s["total"] == 3

    def test_summary_burden_counts_keys_are_strings(self):
        eng = engine()
        eng.analyze(make_input())
        s = eng.summary()
        for k in s["burden_counts"].keys():
            assert isinstance(k, str)

    def test_summary_critical_count_matches_critical_method(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CRIT",
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
        ))
        s = eng.summary()
        assert s["critical_count"] == len(eng.critical())

    def test_summary_escalation_count_matches_needs_escalation(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CRIT",
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
        ))
        s = eng.summary()
        assert s["escalation_count"] == len(eng.needs_escalation())

    def test_summary_advance_ready_count_matches(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CLR1"))
        eng.analyze(make_input(deal_id="CLR2"))
        s = eng.summary()
        assert s["advance_ready_count"] == len(eng.ready_to_advance())


# ─────────────────────────────────────────────────────────────────────────────
# 22. ObjectionIntelligenceEngine — reset
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineReset:
    def test_reset_clears_results(self):
        eng = engine()
        eng.analyze(make_input(deal_id="A"))
        eng.analyze(make_input(deal_id="B"))
        eng.reset()
        assert eng.all_deals() == []

    def test_reset_get_returns_none(self):
        eng = engine()
        eng.analyze(make_input(deal_id="A"))
        eng.reset()
        assert eng.get("A") is None

    def test_reset_averages_return_zero(self):
        eng = engine()
        eng.analyze(make_input(deal_id="A", price_objections=2))
        eng.reset()
        assert eng.avg_burden_score() == 0.0
        assert eng.avg_resolution_score() == 0.0

    def test_reset_then_analyze_works(self):
        eng = engine()
        eng.analyze(make_input(deal_id="A"))
        eng.reset()
        eng.analyze(make_input(deal_id="B"))
        assert len(eng.all_deals()) == 1
        assert eng.get("B") is not None


# ─────────────────────────────────────────────────────────────────────────────
# 23. Integration / end-to-end scenarios
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrationScenarios:
    def test_pristine_deal_is_clear_advance(self):
        eng = engine()
        r = eng.analyze(make_input(
            deal_id="PRISTINE",
            stage="proposal",
            budget_confirmed=True, champion_vouched=True,
        ))
        assert r.objection_burden == ObjectionBurden.CLEAR
        assert r.objection_action == ObjectionAction.ADVANCE

    def test_fully_loaded_deal_is_critical_reassess(self):
        eng = engine()
        r = eng.analyze(make_input(
            deal_id="NIGHTMARE",
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
            days_oldest_unresolved=30,
        ))
        assert r.objection_burden == ObjectionBurden.CRITICAL
        assert r.objection_action == ObjectionAction.REASSESS

    def test_heavy_deal_authority_escalates(self):
        eng = engine()
        # price=2+competitor=2+authority=1 → raw=44+36+16=96 → 48 → HEAVY; authority>0 → ESCALATE
        r = eng.analyze(make_input(
            deal_id="ESCALATE_ME",
            price_objections=2, competitor_objections=2, authority_objections=1,
        ))
        assert r.objection_burden == ObjectionBurden.HEAVY
        assert r.objection_action == ObjectionAction.ESCALATE

    def test_batch_pipeline_sorted_correctly(self):
        eng = engine()
        inputs = [
            make_input(deal_id="LOW"),
            make_input(deal_id="HIGH", price_objections=2, competitor_objections=2,
                       authority_objections=2, timing_objections=2,
                       implementation_objections=2, trust_objections=2),
            make_input(deal_id="MED", price_objections=1, competitor_objections=1),
        ]
        results = eng.analyze_batch(inputs)
        for i in range(len(results) - 1):
            assert results[i].burden_score >= results[i + 1].burden_score

    def test_resolution_score_100_with_no_objections(self):
        eng = engine()
        r = eng.analyze(make_input(deal_id="CLEAN"))
        assert r.resolution_score == 100.0

    def test_deal_with_stale_objection_has_followup_tactic(self):
        eng = engine()
        r = eng.analyze(make_input(deal_id="STALE", days_oldest_unresolved=15))
        assert any("suivi" in t.lower() or "appel" in t.lower() for t in r.recommended_tactics)

    def test_deal_with_stale_objection_has_stagnation_risk(self):
        eng = engine()
        r = eng.analyze(make_input(deal_id="STALE2", days_oldest_unresolved=20))
        assert any("stagnation" in rk.lower() for rk in r.risk_factors)

    def test_closing_stage_no_objections_suggests_contract(self):
        eng = engine()
        r = eng.analyze(make_input(deal_id="CLOSE", stage="closing"))
        assert any("contractuel" in t.lower() for t in r.recommended_tactics)

    def test_deal_impact_zero_when_burden_zero(self):
        eng = engine()
        r = eng.analyze(make_input(deal_id="ZERO", arr_eur=100_000.0))
        assert r.deal_impact_eur == 0.0

    def test_multiple_types_primary_is_highest_weighted_count(self):
        eng = engine()
        # price=2 → 2*22=44; competitor=3 → 3*18=54 → competitor wins
        r = eng.analyze(make_input(deal_id="PRI", price_objections=2, competitor_objections=3))
        assert r.primary_objection_type == "competitor"

    def test_engine_returns_same_result_on_repeated_analyze(self):
        eng = engine()
        inp = make_input()
        r1 = eng.analyze(inp)
        r2 = eng.analyze(inp)
        assert r1.burden_score == r2.burden_score
        assert r1.objection_burden == r2.objection_burden

    def test_at_risk_eur_is_arr_not_impact(self):
        eng = engine()
        # Critical deal with arr=500k
        inp = make_input(deal_id="BIG_CRIT", arr_eur=500_000.0,
            price_objections=2, competitor_objections=2, authority_objections=2,
            timing_objections=2, implementation_objections=2, trust_objections=2,
        )
        r = eng.analyze(inp)
        assert r.objection_burden == ObjectionBurden.CRITICAL
        # total_arr_at_risk uses arr_eur, not deal_impact_eur
        assert eng.total_arr_at_risk_eur() == pytest.approx(500_000.0, abs=0.01)

    def test_clear_deals_excluded_from_at_risk(self):
        eng = engine()
        eng.analyze(make_input(deal_id="CLR1", arr_eur=100_000.0))
        eng.analyze(make_input(deal_id="CLR2", arr_eur=200_000.0))
        assert eng.total_arr_at_risk_eur() == 0.0

    def test_avg_burden_score_rounded_to_one_decimal(self):
        eng = engine()
        eng.analyze(make_input(deal_id="A", price_objections=1))
        avg = eng.avg_burden_score()
        # Should be rounded to 1 decimal
        assert avg == round(avg, 1)
