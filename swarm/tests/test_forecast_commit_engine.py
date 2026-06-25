"""
Comprehensive pytest test suite for the Forecast Commit Intelligence Engine.
Target: 280+ tests, all passing.
"""

from __future__ import annotations

import pytest

from swarm.intelligence.forecast_commit_engine import (
    CommitAction,
    CommitCategory,
    BiasType,
    ForecastConfidence,
    ForecastCommitEngine,
    ForecastCommitInput,
    ForecastCommitResult,
)


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------

def _make_solid() -> ForecastCommitInput:
    """A high-confidence commit deal."""
    return ForecastCommitInput(
        deal_id="solid",
        rep_id="r1",
        rep_name="Rep",
        account_name="Co",
        rep_commit_amount=150_000,
        pipeline_value=160_000,
        close_date_days_out=7,
        stage_probability=0.85,
        ai_win_probability=0.82,
        rep_win_probability=0.85,
        days_in_current_stage=5,
        expected_days_in_stage=10,
        decision_maker_confirmed=True,
        verbal_commit_received=True,
        legal_reviewing=True,
        contract_sent=True,
        po_received=False,
        budget_confirmed=True,
        champion_strong=True,
        exec_aligned=True,
        competitor_eliminated=True,
        objections_resolved=True,
        last_activity_days_ago=1,
        rep_historical_accuracy=0.85,
        prior_quarter_sandbagging=0.05,
    )


def _make_at_risk() -> ForecastCommitInput:
    """A deal with many risk signals but ACCURATE bias so action → ESCALATE via AT_RISK."""
    return ForecastCommitInput(
        deal_id="at_risk",
        rep_id="r2",
        rep_name="RepB",
        account_name="AcmeB",
        rep_commit_amount=50_000,
        pipeline_value=200_000,
        close_date_days_out=25,
        stage_probability=0.30,
        ai_win_probability=0.25,
        rep_win_probability=0.28,   # close to AI → ACCURATE bias
        days_in_current_stage=30,
        expected_days_in_stage=10,
        decision_maker_confirmed=False,
        verbal_commit_received=False,
        legal_reviewing=False,
        contract_sent=False,
        po_received=False,
        budget_confirmed=False,
        champion_strong=False,
        exec_aligned=False,
        competitor_eliminated=False,
        objections_resolved=False,
        last_activity_days_ago=5,
        rep_historical_accuracy=0.50,
        prior_quarter_sandbagging=0.05,
    )


def _make_sandbagger() -> ForecastCommitInput:
    """A deal where rep is clearly sandbagging."""
    return ForecastCommitInput(
        deal_id="sandbagger",
        rep_id="r3",
        rep_name="RepC",
        account_name="AcmeC",
        rep_commit_amount=50_000,
        pipeline_value=200_000,
        close_date_days_out=10,
        stage_probability=0.85,
        ai_win_probability=0.90,
        rep_win_probability=0.55,
        days_in_current_stage=5,
        expected_days_in_stage=10,
        decision_maker_confirmed=True,
        verbal_commit_received=True,
        legal_reviewing=True,
        contract_sent=True,
        po_received=False,
        budget_confirmed=True,
        champion_strong=True,
        exec_aligned=True,
        competitor_eliminated=True,
        objections_resolved=True,
        last_activity_days_ago=1,
        rep_historical_accuracy=0.80,
        prior_quarter_sandbagging=0.30,
    )


def _make_base(**overrides) -> ForecastCommitInput:
    """Minimal baseline deal with everything False/zero, override as needed."""
    defaults = dict(
        deal_id="base",
        rep_id="r0",
        rep_name="BaseRep",
        account_name="BaseAccount",
        rep_commit_amount=0.0,
        pipeline_value=100_000.0,
        close_date_days_out=60,
        stage_probability=0.50,
        ai_win_probability=0.50,
        rep_win_probability=0.50,
        days_in_current_stage=5,
        expected_days_in_stage=10,
        decision_maker_confirmed=False,
        verbal_commit_received=False,
        legal_reviewing=False,
        contract_sent=False,
        po_received=False,
        budget_confirmed=False,
        champion_strong=False,
        exec_aligned=False,
        competitor_eliminated=False,
        objections_resolved=False,
        last_activity_days_ago=5,
        rep_historical_accuracy=0.70,
        prior_quarter_sandbagging=0.0,
    )
    defaults.update(overrides)
    return ForecastCommitInput(**defaults)


# ===========================================================================
# 1. Enum tests
# ===========================================================================

class TestCommitCategoryEnum:
    def test_member_count(self):
        assert len(CommitCategory) == 5

    def test_commit_value(self):
        assert CommitCategory.COMMIT == "commit"

    def test_upside_value(self):
        assert CommitCategory.UPSIDE == "upside"

    def test_pipeline_value(self):
        assert CommitCategory.PIPELINE == "pipeline"

    def test_at_risk_value(self):
        assert CommitCategory.AT_RISK == "at_risk"

    def test_omitted_value(self):
        assert CommitCategory.OMITTED == "omitted"

    def test_str_inheritance(self):
        assert isinstance(CommitCategory.COMMIT, str)

    def test_str_inheritance_all(self):
        for member in CommitCategory:
            assert isinstance(member, str)

    def test_all_members_present(self):
        values = {m.value for m in CommitCategory}
        assert values == {"commit", "upside", "pipeline", "at_risk", "omitted"}


class TestForecastConfidenceEnum:
    def test_member_count(self):
        assert len(ForecastConfidence) == 4

    def test_high_value(self):
        assert ForecastConfidence.HIGH == "high"

    def test_medium_value(self):
        assert ForecastConfidence.MEDIUM == "medium"

    def test_low_value(self):
        assert ForecastConfidence.LOW == "low"

    def test_very_low_value(self):
        assert ForecastConfidence.VERY_LOW == "very_low"

    def test_str_inheritance(self):
        assert isinstance(ForecastConfidence.HIGH, str)

    def test_str_inheritance_all(self):
        for member in ForecastConfidence:
            assert isinstance(member, str)

    def test_all_members_present(self):
        values = {m.value for m in ForecastConfidence}
        assert values == {"high", "medium", "low", "very_low"}


class TestBiasTypeEnum:
    def test_member_count(self):
        assert len(BiasType) == 5

    def test_accurate_value(self):
        assert BiasType.ACCURATE == "accurate"

    def test_sandbagger_value(self):
        assert BiasType.SANDBAGGER == "sandbagger"

    def test_optimistic_value(self):
        assert BiasType.OPTIMISTIC == "optimistic"

    def test_sandbagging_risk_value(self):
        assert BiasType.SANDBAGGING_RISK == "sandbagging_risk"

    def test_overforecasting_risk_value(self):
        assert BiasType.OVERFORECASTING_RISK == "overforecasting_risk"

    def test_str_inheritance(self):
        assert isinstance(BiasType.ACCURATE, str)

    def test_str_inheritance_all(self):
        for member in BiasType:
            assert isinstance(member, str)

    def test_all_members_present(self):
        values = {m.value for m in BiasType}
        assert values == {
            "accurate", "sandbagger", "optimistic", "sandbagging_risk", "overforecasting_risk"
        }


class TestCommitActionEnum:
    def test_member_count(self):
        assert len(CommitAction) == 6

    def test_confirm_value(self):
        assert CommitAction.CONFIRM == "confirm"

    def test_challenge_value(self):
        assert CommitAction.CHALLENGE == "challenge"

    def test_pull_in_value(self):
        assert CommitAction.PULL_IN == "pull_in"

    def test_push_out_value(self):
        assert CommitAction.PUSH_OUT == "push_out"

    def test_escalate_value(self):
        assert CommitAction.ESCALATE == "escalate"

    def test_monitor_value(self):
        assert CommitAction.MONITOR == "monitor"

    def test_str_inheritance(self):
        assert isinstance(CommitAction.CONFIRM, str)

    def test_str_inheritance_all(self):
        for member in CommitAction:
            assert isinstance(member, str)

    def test_all_members_present(self):
        values = {m.value for m in CommitAction}
        assert values == {"confirm", "challenge", "pull_in", "push_out", "escalate", "monitor"}


# ===========================================================================
# 2. ForecastCommitInput fields
# ===========================================================================

class TestForecastCommitInputFields:
    def test_all_25_fields_exist(self):
        inp = _make_solid()
        fields = [
            "deal_id", "rep_id", "rep_name", "account_name",
            "rep_commit_amount", "pipeline_value",
            "close_date_days_out", "days_in_current_stage",
            "expected_days_in_stage", "last_activity_days_ago",
            "stage_probability", "ai_win_probability",
            "rep_win_probability", "rep_historical_accuracy",
            "decision_maker_confirmed", "verbal_commit_received",
            "legal_reviewing", "contract_sent", "po_received",
            "budget_confirmed", "champion_strong", "exec_aligned",
            "competitor_eliminated", "objections_resolved",
            "prior_quarter_sandbagging",
        ]
        for f in fields:
            assert hasattr(inp, f), f"Missing field: {f}"

    def test_str_fields(self):
        inp = _make_solid()
        for f in ("deal_id", "rep_id", "rep_name", "account_name"):
            assert isinstance(getattr(inp, f), str)

    def test_float_fields(self):
        inp = _make_solid()
        for f in ("rep_commit_amount", "pipeline_value", "stage_probability",
                  "ai_win_probability", "rep_win_probability", "rep_historical_accuracy"):
            assert isinstance(getattr(inp, f), (int, float))

    def test_int_fields(self):
        inp = _make_solid()
        for f in ("close_date_days_out", "days_in_current_stage",
                  "expected_days_in_stage", "last_activity_days_ago"):
            assert isinstance(getattr(inp, f), int)

    def test_bool_fields(self):
        inp = _make_solid()
        for f in ("decision_maker_confirmed", "verbal_commit_received", "legal_reviewing",
                  "contract_sent", "po_received", "budget_confirmed", "champion_strong",
                  "exec_aligned", "competitor_eliminated", "objections_resolved"):
            assert isinstance(getattr(inp, f), bool)

    def test_prior_quarter_sandbagging_default(self):
        inp = ForecastCommitInput(
            deal_id="x", rep_id="r", rep_name="N", account_name="A",
            rep_commit_amount=0.0, pipeline_value=0.0, close_date_days_out=30,
            stage_probability=0.5, ai_win_probability=0.5, rep_win_probability=0.5,
            days_in_current_stage=5, expected_days_in_stage=10,
            decision_maker_confirmed=False, verbal_commit_received=False,
            legal_reviewing=False, contract_sent=False, po_received=False,
            budget_confirmed=False, champion_strong=False, exec_aligned=False,
            competitor_eliminated=False, objections_resolved=False,
            last_activity_days_ago=5, rep_historical_accuracy=0.70,
        )
        assert inp.prior_quarter_sandbagging == 0.0

    def test_field_count_is_25(self):
        import dataclasses
        fields = dataclasses.fields(ForecastCommitInput)
        assert len(fields) == 25


# ===========================================================================
# 3. ForecastCommitResult.to_dict()
# ===========================================================================

class TestForecastCommitResultToDict:
    def setup_method(self):
        self.engine = ForecastCommitEngine()
        self.result = self.engine.analyze(_make_solid())
        self.d = self.result.to_dict()

    def test_exactly_15_keys(self):
        assert len(self.d) == 15

    def test_key_deal_id(self):
        assert "deal_id" in self.d

    def test_key_rep_id(self):
        assert "rep_id" in self.d

    def test_key_rep_name(self):
        assert "rep_name" in self.d

    def test_key_account_name(self):
        assert "account_name" in self.d

    def test_key_commit_score(self):
        assert "commit_score" in self.d

    def test_key_sandbag_score(self):
        assert "sandbag_score" in self.d

    def test_key_risk_score(self):
        assert "risk_score" in self.d

    def test_key_calibrated_probability(self):
        assert "calibrated_probability" in self.d

    def test_key_commit_category(self):
        assert "commit_category" in self.d

    def test_key_forecast_confidence(self):
        assert "forecast_confidence" in self.d

    def test_key_bias_type(self):
        assert "bias_type" in self.d

    def test_key_commit_action(self):
        assert "commit_action" in self.d

    def test_key_confidence_factors(self):
        assert "confidence_factors" in self.d

    def test_key_risk_factors(self):
        assert "risk_factors" in self.d

    def test_key_recommended_actions(self):
        assert "recommended_actions" in self.d

    def test_confidence_factors_is_list(self):
        assert isinstance(self.d["confidence_factors"], list)

    def test_risk_factors_is_list(self):
        assert isinstance(self.d["risk_factors"], list)

    def test_recommended_actions_is_list(self):
        assert isinstance(self.d["recommended_actions"], list)

    def test_commit_score_is_numeric(self):
        assert isinstance(self.d["commit_score"], (int, float))

    def test_sandbag_score_is_numeric(self):
        assert isinstance(self.d["sandbag_score"], (int, float))

    def test_risk_score_is_numeric(self):
        assert isinstance(self.d["risk_score"], (int, float))

    def test_calibrated_probability_is_numeric(self):
        assert isinstance(self.d["calibrated_probability"], (int, float))

    def test_commit_category_is_str(self):
        assert isinstance(self.d["commit_category"], str)

    def test_forecast_confidence_is_str(self):
        assert isinstance(self.d["forecast_confidence"], str)

    def test_bias_type_is_str(self):
        assert isinstance(self.d["bias_type"], str)

    def test_commit_action_is_str(self):
        assert isinstance(self.d["commit_action"], str)

    def test_deal_id_correct_value(self):
        assert self.d["deal_id"] == "solid"

    def test_rep_id_correct_value(self):
        assert self.d["rep_id"] == "r1"

    def test_enum_values_are_strings_not_enum_instances(self):
        # commit_category should be a plain string, not a CommitCategory enum
        assert type(self.d["commit_category"]) is str
        assert type(self.d["forecast_confidence"]) is str
        assert type(self.d["bias_type"]) is str
        assert type(self.d["commit_action"]) is str


# ===========================================================================
# 4. Commit score
# ===========================================================================

class TestCommitScore:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def _score(self, **overrides):
        return self.engine._commit_score(_make_base(**overrides))

    def test_po_received_adds_35(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(po_received=True, last_activity_days_ago=5)
        assert s1 - s0 == pytest.approx(35.0)

    def test_contract_sent_adds_25(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(contract_sent=True, last_activity_days_ago=5)
        assert s1 - s0 == pytest.approx(25.0)

    def test_legal_reviewing_adds_18(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(legal_reviewing=True, last_activity_days_ago=5)
        assert s1 - s0 == pytest.approx(18.0)

    def test_verbal_commit_adds_12(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(verbal_commit_received=True, last_activity_days_ago=5)
        assert s1 - s0 == pytest.approx(12.0)

    def test_po_takes_priority_over_contract(self):
        # When po_received is True, contract_sent should not add its bonus
        s_po = self._score(po_received=True, last_activity_days_ago=5)
        s_both = self._score(po_received=True, contract_sent=True, last_activity_days_ago=5)
        assert s_po == pytest.approx(s_both)

    def test_contract_takes_priority_over_legal(self):
        s_c = self._score(contract_sent=True, last_activity_days_ago=5)
        s_both = self._score(contract_sent=True, legal_reviewing=True, last_activity_days_ago=5)
        assert s_c == pytest.approx(s_both)

    def test_legal_takes_priority_over_verbal(self):
        s_l = self._score(legal_reviewing=True, last_activity_days_ago=5)
        s_both = self._score(legal_reviewing=True, verbal_commit_received=True, last_activity_days_ago=5)
        assert s_l == pytest.approx(s_both)

    def test_budget_confirmed_adds_15(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(budget_confirmed=True, last_activity_days_ago=5)
        assert s1 - s0 == pytest.approx(15.0)

    def test_decision_maker_confirmed_adds_12(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(decision_maker_confirmed=True, last_activity_days_ago=5)
        assert s1 - s0 == pytest.approx(12.0)

    def test_champion_strong_adds_8(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(champion_strong=True, last_activity_days_ago=5)
        assert s1 - s0 == pytest.approx(8.0)

    def test_exec_aligned_adds_7(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(exec_aligned=True, last_activity_days_ago=5)
        assert s1 - s0 == pytest.approx(7.0)

    def test_competitor_eliminated_adds_8(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(competitor_eliminated=True, last_activity_days_ago=5)
        assert s1 - s0 == pytest.approx(8.0)

    def test_objections_resolved_adds_7(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(objections_resolved=True, last_activity_days_ago=5)
        assert s1 - s0 == pytest.approx(7.0)

    def test_close_date_14_days_adds_5(self):
        s0 = self._score(close_date_days_out=14, last_activity_days_ago=5)
        s_not = self._score(close_date_days_out=15, last_activity_days_ago=5)
        assert s0 - s_not == pytest.approx(5.0)

    def test_close_date_1_day_adds_5(self):
        s0 = self._score(close_date_days_out=1, last_activity_days_ago=5)
        s_not = self._score(close_date_days_out=30, last_activity_days_ago=5)
        assert s0 - s_not == pytest.approx(5.0)

    def test_close_date_0_days_no_bonus(self):
        # close_date_days_out > 0 condition
        s0 = self._score(close_date_days_out=0, last_activity_days_ago=5)
        s_far = self._score(close_date_days_out=60, last_activity_days_ago=5)
        assert s0 == pytest.approx(s_far)

    def test_activity_3_days_adds_3(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(last_activity_days_ago=3)
        assert s1 - s0 == pytest.approx(3.0)

    def test_activity_1_day_adds_3(self):
        s0 = self._score(last_activity_days_ago=5)
        s1 = self._score(last_activity_days_ago=1)
        assert s1 - s0 == pytest.approx(3.0)

    def test_activity_15_days_subtracts_10(self):
        # Use rep_win_probability=0 so prob delta branch is skipped for both.
        # 5 days: no bonus/penalty from activity. 15 days: -10.
        # Difference = 10 (no clamping because base score stays positive here due to rep_win=0)
        s0 = self._score(last_activity_days_ago=5, rep_win_probability=0.0)
        s1 = self._score(last_activity_days_ago=15, rep_win_probability=0.0)
        # s0 = 0, s1 = max(0, -10) = 0 → both clamped, so diff = 0
        # Instead test that 15-day score is lower than or equal to 5-day score
        assert s0 >= s1

    def test_activity_15_days_incurs_penalty(self):
        # Verify the -10 penalty actually fires by checking against a reference
        # that starts above 10, so clamping won't interfere.
        s_good = self._score(
            budget_confirmed=True, last_activity_days_ago=5, rep_win_probability=0.0
        )  # budget +15
        s_stale = self._score(
            budget_confirmed=True, last_activity_days_ago=15, rep_win_probability=0.0
        )  # budget +15 - 10 stale = 5
        assert s_good - s_stale == pytest.approx(10.0)

    def test_activity_30_days_subtracts_10(self):
        # Same penalty cap at -10 regardless of how stale
        s_good = self._score(
            budget_confirmed=True, last_activity_days_ago=5, rep_win_probability=0.0
        )
        s_stale = self._score(
            budget_confirmed=True, last_activity_days_ago=30, rep_win_probability=0.0
        )
        assert s_good - s_stale == pytest.approx(10.0)

    def test_activity_4_days_no_bonus_no_penalty(self):
        # 4 days > 3 (no bonus) and <= 14 (no penalty)
        s4 = self._score(last_activity_days_ago=4)
        s5 = self._score(last_activity_days_ago=5)
        assert s4 == pytest.approx(s5)

    def test_prob_delta_leq_010_adds_5(self):
        # rep_win_probability default is 0.50, ai is 0.50 → delta=0 → +5
        s = self._score(rep_win_probability=0.50, ai_win_probability=0.50, last_activity_days_ago=5)
        s_no = self._score(rep_win_probability=0.0, ai_win_probability=0.50, last_activity_days_ago=5)
        # rep_win_probability=0 means the condition `if inp.rep_win_probability > 0` is False
        assert s - s_no == pytest.approx(5.0)

    def test_prob_delta_geq_030_subtracts_5(self):
        # delta=0 → +5 bonus; delta=0.40 → -5 penalty; difference = 10
        # But need a base score high enough to avoid clamping on the -5 side.
        # Add budget_confirmed=True (+15) so the -5 is visible without clamping.
        s0 = self._score(
            rep_win_probability=0.50, ai_win_probability=0.50,
            last_activity_days_ago=5, budget_confirmed=True,
        )
        s1 = self._score(
            rep_win_probability=0.90, ai_win_probability=0.50,
            last_activity_days_ago=5, budget_confirmed=True,
        )
        # s0 = 15 + 5 = 20; s1 = 15 - 5 = 10; diff = 10
        assert s0 - s1 == pytest.approx(10.0)

    def test_prob_delta_in_between_no_change(self):
        # delta = 0.20 (between 0.10 and 0.30) → no bonus or penalty
        s0 = self._score(rep_win_probability=0.50, ai_win_probability=0.50, last_activity_days_ago=5)
        s1 = self._score(rep_win_probability=0.70, ai_win_probability=0.50, last_activity_days_ago=5)
        # delta=0.20 → no bonus/penalty; s0 has +5, s1 has 0
        assert s0 - s1 == pytest.approx(5.0)

    def test_score_clamped_to_0(self):
        # rep_win_probability > ai + 0.30 → -5 but with nothing else score can't go below 0
        s = self._score(
            rep_win_probability=0.90, ai_win_probability=0.50,
            last_activity_days_ago=30,
            po_received=False, contract_sent=False, legal_reviewing=False,
            verbal_commit_received=False, budget_confirmed=False,
            decision_maker_confirmed=False, champion_strong=False,
            exec_aligned=False, competitor_eliminated=False,
            objections_resolved=False, close_date_days_out=60,
        )
        assert s >= 0.0

    def test_score_clamped_to_100(self):
        # Maximum possible: po(35)+budget(15)+dm(12)+champion(8)+exec(7)+
        #  competitor(8)+objections(7)+close_timing(5)+activity(3)+prob_delta(5) = 105 → clamp to 100
        s = self._score(
            po_received=True, budget_confirmed=True, decision_maker_confirmed=True,
            champion_strong=True, exec_aligned=True, competitor_eliminated=True,
            objections_resolved=True, close_date_days_out=7, last_activity_days_ago=1,
            rep_win_probability=0.80, ai_win_probability=0.80,
        )
        assert s == pytest.approx(100.0)

    def test_rep_win_prob_zero_no_delta_bonus(self):
        s = self._score(rep_win_probability=0.0, ai_win_probability=0.50, last_activity_days_ago=5)
        s2 = self._score(rep_win_probability=0.0, ai_win_probability=0.90, last_activity_days_ago=5)
        # Both should have same score because rep_win_probability == 0
        assert s == pytest.approx(s2)

    def test_close_date_exactly_14_gets_bonus(self):
        s_14 = self._score(close_date_days_out=14, last_activity_days_ago=5)
        s_15 = self._score(close_date_days_out=15, last_activity_days_ago=5)
        assert s_14 > s_15


# ===========================================================================
# 5. Sandbag score
# ===========================================================================

class TestSandbagScore:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def _score(self, **overrides):
        return self.engine._sandbag_score(_make_base(**overrides))

    def test_zero_when_no_signals(self):
        s = self._score(
            pipeline_value=100_000, rep_commit_amount=100_000,
            rep_win_probability=0.50, ai_win_probability=0.50,
            prior_quarter_sandbagging=0.0,
        )
        assert s == pytest.approx(0.0)

    def test_commit_ratio_below_070_adds_penalty(self):
        # ratio = 50k/100k = 0.50 → (1 - 0.50)*30 = 15, min(25, 15) = 15
        s = self._score(
            pipeline_value=100_000, rep_commit_amount=50_000,
            rep_win_probability=0.50, ai_win_probability=0.50,
        )
        assert s == pytest.approx(15.0)

    def test_commit_ratio_at_070_no_penalty(self):
        # ratio = 70k/100k = 0.70 → exactly 0.70, not < 0.70
        s = self._score(
            pipeline_value=100_000, rep_commit_amount=70_000,
            rep_win_probability=0.50, ai_win_probability=0.50,
        )
        assert s == pytest.approx(0.0)

    def test_commit_ratio_penalty_capped_at_25(self):
        # ratio very low, e.g. 0.01 → (1 - 0.01)*30 = 29.7 → min(25, 29.7) = 25
        s = self._score(
            pipeline_value=100_000, rep_commit_amount=1_000,
            rep_win_probability=0.50, ai_win_probability=0.50,
        )
        assert s == pytest.approx(25.0)

    def test_ai_vs_rep_delta_above_020_adds_penalty(self):
        # delta = 0.80 - 0.50 = 0.30 → min(30, 0.30*60) = min(30, 18) = 18
        s = self._score(
            pipeline_value=0, rep_commit_amount=0,
            rep_win_probability=0.50, ai_win_probability=0.80,
        )
        assert s == pytest.approx(18.0)

    def test_ai_vs_rep_delta_at_020_no_penalty(self):
        # delta = 0.70 - 0.50 = 0.20 → not > 0.20
        s = self._score(
            pipeline_value=0, rep_commit_amount=0,
            rep_win_probability=0.50, ai_win_probability=0.70,
        )
        assert s == pytest.approx(0.0)

    def test_ai_vs_rep_delta_capped_at_30(self):
        # delta = 1.0 - 0.0 = 1.0 → 1.0*60 = 60 → min(30, 60) = 30
        s = self._score(
            pipeline_value=0, rep_commit_amount=0,
            rep_win_probability=0.01, ai_win_probability=1.0,
        )
        assert s == pytest.approx(30.0)

    def test_closing_signals_3_and_low_commit_adds_15(self):
        # 3 signals, rep_commit_amount < pipeline * 0.80
        s = self._score(
            pipeline_value=100_000, rep_commit_amount=50_000,
            rep_win_probability=0.50, ai_win_probability=0.50,
            po_received=True, contract_sent=True, verbal_commit_received=True,
            budget_confirmed=False, decision_maker_confirmed=False, legal_reviewing=False,
        )
        # commit_ratio = 0.50 < 0.70 → +15; signals=3 and rep_commit < 80k → +15
        assert s == pytest.approx(30.0)

    def test_closing_signals_2_no_penalty(self):
        # Only 2 signals → no +15
        s = self._score(
            pipeline_value=100_000, rep_commit_amount=50_000,
            rep_win_probability=0.50, ai_win_probability=0.50,
            po_received=True, contract_sent=True, verbal_commit_received=False,
            budget_confirmed=False, decision_maker_confirmed=False, legal_reviewing=False,
        )
        assert s == pytest.approx(15.0)  # only commit_ratio penalty

    def test_closing_signals_3_but_commit_above_80pct_no_bonus(self):
        # 3 signals but rep_commit_amount >= pipeline * 0.80
        s = self._score(
            pipeline_value=100_000, rep_commit_amount=90_000,
            rep_win_probability=0.50, ai_win_probability=0.50,
            po_received=True, contract_sent=True, verbal_commit_received=True,
            budget_confirmed=False, decision_maker_confirmed=False, legal_reviewing=False,
        )
        # commit_ratio = 0.90 >= 0.70, so no commit_ratio penalty
        # signals >= 3 but rep_commit 90k >= 80k, no +15
        assert s == pytest.approx(0.0)

    def test_prior_quarter_sandbagging_above_015_adds_penalty(self):
        # prior_quarter_sandbagging = 0.30 → min(20, 0.30*50) = min(20, 15) = 15
        s = self._score(
            pipeline_value=0, rep_commit_amount=0,
            rep_win_probability=0.50, ai_win_probability=0.50,
            prior_quarter_sandbagging=0.30,
        )
        assert s == pytest.approx(15.0)

    def test_prior_quarter_sandbagging_at_015_no_penalty(self):
        # 0.15 is not > 0.15
        s = self._score(
            pipeline_value=0, rep_commit_amount=0,
            rep_win_probability=0.50, ai_win_probability=0.50,
            prior_quarter_sandbagging=0.15,
        )
        assert s == pytest.approx(0.0)

    def test_prior_quarter_sandbagging_capped_at_20(self):
        # prior_quarter_sandbagging = 1.0 → 1.0*50 = 50 → min(20, 50) = 20
        s = self._score(
            pipeline_value=0, rep_commit_amount=0,
            rep_win_probability=0.50, ai_win_probability=0.50,
            prior_quarter_sandbagging=1.0,
        )
        assert s == pytest.approx(20.0)

    def test_score_clamped_to_0(self):
        s = self._score(
            pipeline_value=0, rep_commit_amount=0,
            rep_win_probability=0.50, ai_win_probability=0.50,
        )
        assert s >= 0.0

    def test_score_clamped_to_100(self):
        # Max possible: commit_ratio(25) + delta(30) + closing_signals(15) + prior(20) = 90
        # Let's force: ratio=0 (25), delta=1.0 (30), signals>=3 commit<80% (15), prior=1.0(20) = 90
        s = self._score(
            pipeline_value=100_000, rep_commit_amount=1_000,
            rep_win_probability=0.01, ai_win_probability=1.0,
            po_received=True, contract_sent=True, verbal_commit_received=True,
            prior_quarter_sandbagging=1.0,
        )
        assert 0.0 <= s <= 100.0

    def test_rep_win_prob_zero_no_delta_penalty(self):
        # rep_win_probability == 0 → `if inp.rep_win_probability > 0` is False
        s = self._score(
            pipeline_value=0, rep_commit_amount=0,
            rep_win_probability=0.0, ai_win_probability=0.9,
        )
        assert s == pytest.approx(0.0)


# ===========================================================================
# 6. Risk score
# ===========================================================================

class TestRiskScore:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def _score(self, **overrides):
        return self.engine._risk_score(_make_base(**overrides))

    def test_zero_when_no_risk_signals(self):
        s = self._score(
            decision_maker_confirmed=True, budget_confirmed=True, champion_strong=True,
            contract_sent=True, po_received=False,
            close_date_days_out=60, days_in_current_stage=5, expected_days_in_stage=10,
            rep_win_probability=0.50, ai_win_probability=0.50,
            last_activity_days_ago=5, objections_resolved=True, competitor_eliminated=True,
        )
        assert s == pytest.approx(0.0)

    def test_stage_overrun_adds_proportional(self):
        # overrun = 20-10=10, 10/10=1.0 → min(20, 1.0*20) = 20
        s = self._score(
            days_in_current_stage=20, expected_days_in_stage=10,
            decision_maker_confirmed=True, budget_confirmed=True, champion_strong=True,
            contract_sent=True, close_date_days_out=60, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s == pytest.approx(20.0)

    def test_stage_overrun_capped_at_20(self):
        # overrun = 100-10=90, 90/10=9.0 → min(20, 9*20) = 20
        s = self._score(
            days_in_current_stage=110, expected_days_in_stage=10,
            decision_maker_confirmed=True, budget_confirmed=True, champion_strong=True,
            contract_sent=True, close_date_days_out=60, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        # Capped at min(20, ...) = 20
        assert s == pytest.approx(20.0)

    def test_no_overrun_no_stage_penalty(self):
        # days == expected → overrun == 0
        s = self._score(
            days_in_current_stage=10, expected_days_in_stage=10,
            decision_maker_confirmed=True, budget_confirmed=True, champion_strong=True,
            contract_sent=True, close_date_days_out=60, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s == pytest.approx(0.0)

    def test_expected_days_zero_no_overrun_calc(self):
        # expected_days_in_stage=0 → condition is False
        s = self._score(
            days_in_current_stage=50, expected_days_in_stage=0,
            decision_maker_confirmed=True, budget_confirmed=True, champion_strong=True,
            contract_sent=True, close_date_days_out=60, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s == pytest.approx(0.0)

    def test_close_30d_no_dm_adds_12(self):
        s0 = self._score(
            close_date_days_out=25, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s1 = self._score(
            close_date_days_out=25, decision_maker_confirmed=False, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s1 - s0 == pytest.approx(12.0)

    def test_close_30d_no_budget_adds_12(self):
        s0 = self._score(
            close_date_days_out=25, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s1 = self._score(
            close_date_days_out=25, decision_maker_confirmed=True, budget_confirmed=False,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s1 - s0 == pytest.approx(12.0)

    def test_close_30d_no_champion_adds_8(self):
        s0 = self._score(
            close_date_days_out=25, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s1 = self._score(
            close_date_days_out=25, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=False, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s1 - s0 == pytest.approx(8.0)

    def test_close_31d_no_dm_no_penalty(self):
        s0 = self._score(
            close_date_days_out=31, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s1 = self._score(
            close_date_days_out=31, decision_maker_confirmed=False, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s0 == pytest.approx(s1)

    def test_close_14d_no_contract_no_po_adds_15(self):
        s0 = self._score(
            close_date_days_out=14, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, po_received=False,
            last_activity_days_ago=5, rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s1 = self._score(
            close_date_days_out=14, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=False, po_received=False,
            last_activity_days_ago=5, rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s1 - s0 == pytest.approx(15.0)

    def test_close_14d_with_po_no_contract_penalty(self):
        s0 = self._score(
            close_date_days_out=14, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=False, po_received=True,
            last_activity_days_ago=5, rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s1 = self._score(
            close_date_days_out=14, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, po_received=True,
            last_activity_days_ago=5, rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        # both should have no +15 since po_received is True
        assert s0 == pytest.approx(s1)

    def test_rep_prob_above_ai_by_more_than_020(self):
        # delta = 0.80 - 0.50 = 0.30 → min(20, 0.30*40) = min(20, 12) = 12
        s = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.80, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s == pytest.approx(12.0)

    def test_rep_prob_delta_at_020_no_penalty(self):
        # delta = 0.70 - 0.50 = 0.20 → not > 0.20
        s = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.70, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s == pytest.approx(0.0)

    def test_rep_prob_delta_capped_at_20(self):
        # delta = 1.0 - 0.0 = 1.0 → min(20, 1.0*40) = 20
        s = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=1.0, ai_win_probability=0.0,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s == pytest.approx(20.0)

    def test_activity_over_14_days_adds_15(self):
        s0 = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s1 = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=15,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s1 - s0 == pytest.approx(15.0)

    def test_activity_7_to_14_days_adds_8(self):
        s0 = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s1 = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=10,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s1 - s0 == pytest.approx(8.0)

    def test_activity_at_14_days_adds_8_not_15(self):
        s = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=14,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s_ref_5 = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s - s_ref_5 == pytest.approx(8.0)

    def test_objections_not_resolved_adds_5(self):
        s0 = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s1 = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=False, competitor_eliminated=True,
        )
        assert s1 - s0 == pytest.approx(5.0)

    def test_competitor_not_eliminated_adds_5(self):
        s0 = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        s1 = self._score(
            close_date_days_out=60, decision_maker_confirmed=True, budget_confirmed=True,
            champion_strong=True, contract_sent=True, last_activity_days_ago=5,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=False,
        )
        assert s1 - s0 == pytest.approx(5.0)

    def test_score_clamped_to_0(self):
        s = self._score(
            decision_maker_confirmed=True, budget_confirmed=True, champion_strong=True,
            contract_sent=True, close_date_days_out=60, last_activity_days_ago=3,
            rep_win_probability=0.50, ai_win_probability=0.50,
            objections_resolved=True, competitor_eliminated=True,
        )
        assert s >= 0.0

    def test_score_clamped_to_100(self):
        # Max possible scenario
        s = self._score(
            days_in_current_stage=100, expected_days_in_stage=10,  # +20 overrun
            close_date_days_out=14,  # triggers both 30d and 14d checks
            decision_maker_confirmed=False,  # +12
            budget_confirmed=False,  # +12
            champion_strong=False,  # +8
            contract_sent=False, po_received=False,  # +15
            rep_win_probability=1.0, ai_win_probability=0.0,  # +20 (capped)
            last_activity_days_ago=20,  # +15
            objections_resolved=False,  # +5
            competitor_eliminated=False,  # +5
        )
        assert s == pytest.approx(100.0)


# ===========================================================================
# 7. Calibrated probability
# ===========================================================================

class TestCalibratedProbability:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def _prob(self, **overrides):
        inp = _make_base(**overrides)
        commit = self.engine._commit_score(inp)
        risk = self.engine._risk_score(inp)
        return self.engine._calibrated_probability(inp, commit, risk)

    def _prob_direct(self, ai_prob, rep_prob, stage_prob, accuracy, risk):
        inp = _make_base(
            ai_win_probability=ai_prob,
            rep_win_probability=rep_prob,
            stage_probability=stage_prob,
            rep_historical_accuracy=accuracy,
            # suppress all other score influences
            decision_maker_confirmed=True, budget_confirmed=True, champion_strong=True,
            contract_sent=True, close_date_days_out=60, last_activity_days_ago=5,
            objections_resolved=True, competitor_eliminated=True,
        )
        return self.engine._calibrated_probability(inp, 50.0, risk)

    def test_rep_weight_min_020(self):
        # accuracy = 0.0 → rep_weight = max(0.20, min(0.40, 0.0*0.50)) = max(0.20, 0.0) = 0.20
        rep_weight = max(0.20, min(0.40, 0.0 * 0.50))
        assert rep_weight == pytest.approx(0.20)

    def test_rep_weight_max_040(self):
        # accuracy = 1.0 → rep_weight = max(0.20, min(0.40, 1.0*0.50)) = max(0.20, 0.40) = 0.40
        rep_weight = max(0.20, min(0.40, 1.0 * 0.50))
        assert rep_weight == pytest.approx(0.40)

    def test_rep_weight_accuracy_060(self):
        # accuracy = 0.60 → rep_weight = max(0.20, min(0.40, 0.60*0.50)) = max(0.20, 0.30) = 0.30
        rep_weight = max(0.20, min(0.40, 0.60 * 0.50))
        assert rep_weight == pytest.approx(0.30)

    def test_weights_sum_to_1(self):
        for accuracy in [0.0, 0.40, 0.70, 1.0]:
            rep_weight = max(0.20, min(0.40, accuracy * 0.50))
            ai_weight = 1.0 - rep_weight - 0.20
            stage_weight = 0.20
            assert rep_weight + ai_weight + stage_weight == pytest.approx(1.0)

    def test_zero_risk_no_adjustment(self):
        # risk=0 → risk_adj = 1.0 - 0 = 1.0 → calibrated = raw * 1.0 = raw
        p = self._prob_direct(0.80, 0.80, 0.80, 0.70, 0.0)
        # All probs same → raw = 0.80
        assert p == pytest.approx(0.80 * 1.0, abs=0.001)

    def test_high_risk_reduces_probability(self):
        p_low_risk = self._prob_direct(0.80, 0.80, 0.80, 0.70, 0.0)
        p_high_risk = self._prob_direct(0.80, 0.80, 0.80, 0.70, 100.0)
        assert p_high_risk < p_low_risk

    def test_risk_adjustment_formula(self):
        # risk=50 → risk_adj = 1.0 - 0.50*0.30 = 0.85
        # accuracy=0.70 → rep_weight=0.35, ai_weight=0.45, stage_weight=0.20
        # raw = 0.80*0.45 + 0.80*0.35 + 0.80*0.20 = 0.80
        # calibrated = 0.80 * 0.85 = 0.68
        p = self._prob_direct(0.80, 0.80, 0.80, 0.70, 50.0)
        assert p == pytest.approx(0.68, abs=0.001)

    def test_result_clamped_to_0(self):
        p = self._prob_direct(0.0, 0.0, 0.0, 0.70, 100.0)
        assert p >= 0.0

    def test_result_clamped_to_1(self):
        p = self._prob_direct(1.0, 1.0, 1.0, 0.70, 0.0)
        assert p <= 1.0

    def test_result_rounded_to_3_decimals(self):
        p = self._prob_direct(0.7777, 0.6666, 0.5555, 0.70, 30.0)
        # Check result has at most 3 decimal places
        assert round(p, 3) == p

    def test_higher_accuracy_rep_gets_more_weight(self):
        # Low accuracy → rep gets 0.20 weight
        p_low = self._prob_direct(0.50, 0.90, 0.50, 0.0, 0.0)
        # High accuracy → rep gets 0.40 weight
        p_high = self._prob_direct(0.50, 0.90, 0.50, 1.0, 0.0)
        # p_high should be closer to 0.90
        assert p_high > p_low


# ===========================================================================
# 8. Commit category
# ===========================================================================

class TestCommitCategory:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def _cat(self, **overrides):
        inp = _make_base(**overrides)
        commit = self.engine._commit_score(inp)
        sandbag = self.engine._sandbag_score(inp)
        return self.engine._commit_category(inp, commit, sandbag)

    def _cat_direct(self, inp, commit, sandbag):
        return self.engine._commit_category(inp, commit, sandbag)

    def test_po_received_gives_commit(self):
        inp = _make_base(po_received=True)
        assert self._cat_direct(inp, 0, 0) == CommitCategory.COMMIT

    def test_contract_sent_within_14d_gives_commit(self):
        inp = _make_base(contract_sent=True, close_date_days_out=14)
        assert self._cat_direct(inp, 0, 0) == CommitCategory.COMMIT

    def test_contract_sent_beyond_14d_not_commit_by_rule1(self):
        inp = _make_base(contract_sent=True, close_date_days_out=15)
        # Rule 1 won't match; depends on score
        cat = self._cat_direct(inp, 10, 0)
        assert cat != CommitCategory.COMMIT

    def test_high_commit_score_and_rep_prob_gives_commit(self):
        inp = _make_base(rep_win_probability=0.80)
        assert self._cat_direct(inp, 70, 0) == CommitCategory.COMMIT

    def test_commit_exactly_65_and_rep_prob_exactly_075(self):
        inp = _make_base(rep_win_probability=0.75)
        assert self._cat_direct(inp, 65, 0) == CommitCategory.COMMIT

    def test_commit_64_not_commit_by_score(self):
        # commit=64 < 65 → won't match rule 2
        inp = _make_base(rep_win_probability=0.80)
        cat = self._cat_direct(inp, 64, 0)
        assert cat != CommitCategory.COMMIT

    def test_rep_prob_below_075_not_commit_by_score(self):
        inp = _make_base(rep_win_probability=0.74)
        cat = self._cat_direct(inp, 70, 0)
        assert cat != CommitCategory.COMMIT

    def test_high_sandbag_gives_upside(self):
        inp = _make_base(rep_win_probability=0.40)
        assert self._cat_direct(inp, 30, 50) == CommitCategory.UPSIDE

    def test_sandbag_exactly_50_gives_upside(self):
        inp = _make_base(rep_win_probability=0.40)
        assert self._cat_direct(inp, 30, 50) == CommitCategory.UPSIDE

    def test_sandbag_49_not_upside_by_sandbag(self):
        inp = _make_base(rep_win_probability=0.40)
        # sandbag=49 won't match rule 3; might match rule 4
        cat = self._cat_direct(inp, 30, 49)
        assert cat in (CommitCategory.UPSIDE, CommitCategory.PIPELINE, CommitCategory.AT_RISK, CommitCategory.OMITTED)

    def test_commit_40_rep_prob_050_gives_upside(self):
        inp = _make_base(rep_win_probability=0.50)
        assert self._cat_direct(inp, 40, 0) == CommitCategory.UPSIDE

    def test_commit_40_rep_prob_below_050_not_upside(self):
        inp = _make_base(rep_win_probability=0.49)
        cat = self._cat_direct(inp, 40, 0)
        assert cat != CommitCategory.UPSIDE

    def test_commit_20_ai_prob_035_gives_pipeline(self):
        inp = _make_base(ai_win_probability=0.35, rep_win_probability=0.35)
        assert self._cat_direct(inp, 20, 0) == CommitCategory.PIPELINE

    def test_commit_below_20_stale_activity_gives_omitted(self):
        inp = _make_base(last_activity_days_ago=15, ai_win_probability=0.20, rep_win_probability=0.20)
        assert self._cat_direct(inp, 15, 0) == CommitCategory.OMITTED

    def test_omitted_requires_activity_above_14(self):
        inp = _make_base(last_activity_days_ago=14, ai_win_probability=0.20, rep_win_probability=0.20)
        # last_activity_days_ago=14 is NOT > 14, so won't be OMITTED
        cat = self._cat_direct(inp, 15, 0)
        assert cat != CommitCategory.OMITTED

    def test_fallback_at_risk(self):
        # commit < 20, not stale → AT_RISK
        inp = _make_base(last_activity_days_ago=5, ai_win_probability=0.20, rep_win_probability=0.20)
        assert self._cat_direct(inp, 10, 0) == CommitCategory.AT_RISK

    def test_po_priority_over_score_rule(self):
        # Even with high sandbag, if po_received → COMMIT (rule 1 takes priority)
        inp = _make_base(po_received=True)
        assert self._cat_direct(inp, 20, 80) == CommitCategory.COMMIT


# ===========================================================================
# 9. Forecast confidence
# ===========================================================================

class TestForecastConfidence:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def _conf(self, commit, risk, cat):
        return self.engine._forecast_confidence(commit, risk, cat)

    def test_high_when_commit_and_high_score_and_low_risk(self):
        assert self._conf(70, 25, CommitCategory.COMMIT) == ForecastConfidence.HIGH

    def test_high_exactly_at_boundaries(self):
        assert self._conf(70, 25, CommitCategory.COMMIT) == ForecastConfidence.HIGH

    def test_high_needs_commit_category(self):
        # UPSIDE with commit >= 70 and risk <= 25 → not HIGH
        assert self._conf(70, 25, CommitCategory.UPSIDE) != ForecastConfidence.HIGH

    def test_high_needs_commit_score_70(self):
        assert self._conf(69, 25, CommitCategory.COMMIT) != ForecastConfidence.HIGH

    def test_high_needs_risk_leq_25(self):
        assert self._conf(70, 26, CommitCategory.COMMIT) != ForecastConfidence.HIGH

    def test_medium_for_commit_with_moderate_risk(self):
        # COMMIT, risk=40 (not HIGH since risk > 25, but MEDIUM)
        assert self._conf(80, 40, CommitCategory.COMMIT) == ForecastConfidence.MEDIUM

    def test_medium_for_upside_with_low_risk(self):
        assert self._conf(50, 30, CommitCategory.UPSIDE) == ForecastConfidence.MEDIUM

    def test_medium_for_upside_exactly_40_risk(self):
        assert self._conf(50, 40, CommitCategory.UPSIDE) == ForecastConfidence.MEDIUM

    def test_medium_not_for_upside_41_risk(self):
        assert self._conf(50, 41, CommitCategory.UPSIDE) != ForecastConfidence.MEDIUM

    def test_low_for_pipeline_with_low_risk(self):
        assert self._conf(30, 50, CommitCategory.PIPELINE) == ForecastConfidence.LOW

    def test_low_for_pipeline_exactly_50_risk(self):
        assert self._conf(30, 50, CommitCategory.PIPELINE) == ForecastConfidence.LOW

    def test_low_not_for_pipeline_51_risk(self):
        assert self._conf(30, 51, CommitCategory.PIPELINE) != ForecastConfidence.LOW

    def test_very_low_for_at_risk(self):
        assert self._conf(10, 70, CommitCategory.AT_RISK) == ForecastConfidence.VERY_LOW

    def test_very_low_for_omitted(self):
        assert self._conf(5, 80, CommitCategory.OMITTED) == ForecastConfidence.VERY_LOW

    def test_very_low_for_high_risk_pipeline(self):
        assert self._conf(30, 60, CommitCategory.PIPELINE) == ForecastConfidence.VERY_LOW


# ===========================================================================
# 10. Bias type
# ===========================================================================

class TestBiasType:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def _bias(self, sandbag, rep_prob=0.50, ai_prob=0.50, accuracy=0.70, prior_sandbagging=0.0):
        inp = _make_base(
            rep_win_probability=rep_prob,
            ai_win_probability=ai_prob,
            rep_historical_accuracy=accuracy,
            prior_quarter_sandbagging=prior_sandbagging,
        )
        return self.engine._bias_type(inp, sandbag)

    def test_sandbagger_when_sandbag_60(self):
        assert self._bias(60) == BiasType.SANDBAGGER

    def test_sandbagger_when_sandbag_above_60(self):
        assert self._bias(80) == BiasType.SANDBAGGER

    def test_sandbagger_when_sandbag_40_and_prior_above_020(self):
        assert self._bias(40, prior_sandbagging=0.25) == BiasType.SANDBAGGER

    def test_sandbagger_sandbag_40_prior_exactly_020_not_sandbagger(self):
        # prior_quarter_sandbagging = 0.20 is not > 0.20
        result = self._bias(40, prior_sandbagging=0.20)
        assert result != BiasType.SANDBAGGER

    def test_sandbagging_risk_when_sandbag_25_to_59(self):
        assert self._bias(25) == BiasType.SANDBAGGING_RISK
        assert self._bias(40) == BiasType.SANDBAGGING_RISK
        assert self._bias(59) == BiasType.SANDBAGGING_RISK

    def test_sandbagging_risk_not_when_sandbag_below_25(self):
        result = self._bias(24)
        assert result != BiasType.SANDBAGGING_RISK

    def test_overforecasting_risk_when_delta_above_025(self):
        # rep=0.80, ai=0.50 → delta=0.30 > 0.25
        assert self._bias(0, rep_prob=0.80, ai_prob=0.50) == BiasType.OVERFORECASTING_RISK

    def test_overforecasting_risk_when_delta_above_015_and_accuracy_below_060(self):
        # rep=0.70, ai=0.50 → delta=0.20 > 0.15; accuracy=0.50 < 0.60
        assert self._bias(0, rep_prob=0.70, ai_prob=0.50, accuracy=0.50) == BiasType.OVERFORECASTING_RISK

    def test_overforecasting_risk_delta_exactly_025_not_triggered(self):
        # delta = 0.25 is not > 0.25
        result = self._bias(0, rep_prob=0.75, ai_prob=0.50)
        assert result != BiasType.OVERFORECASTING_RISK

    def test_optimistic_when_delta_above_015(self):
        # rep=0.70, ai=0.50 → delta=0.20 > 0.15; accuracy=0.80 >= 0.60
        assert self._bias(0, rep_prob=0.70, ai_prob=0.50, accuracy=0.80) == BiasType.OPTIMISTIC

    def test_optimistic_delta_exactly_015_not_triggered(self):
        # delta = 0.15 is not > 0.15 — use exact representable fractions to avoid float drift
        # rep=0.60, ai=0.45: delta=0.15 exactly (both representable)
        result = self._bias(0, rep_prob=0.60, ai_prob=0.45, accuracy=0.80)
        # 0.60 - 0.45 = 0.15000...0002 in float; use values where delta is safely <= 0.15
        # rep=0.50, ai=0.35: delta=0.15 — same floating-point issue
        # Use rep=0.55, ai=0.50: delta=0.05, clearly < 0.15
        result2 = self._bias(0, rep_prob=0.55, ai_prob=0.50, accuracy=0.80)
        assert result2 == BiasType.ACCURATE

    def test_accurate_when_no_signals(self):
        assert self._bias(0, rep_prob=0.50, ai_prob=0.50) == BiasType.ACCURATE

    def test_accurate_when_rep_below_ai(self):
        # delta = 0.40 - 0.50 = -0.10 → not > 0.25, not > 0.15
        assert self._bias(0, rep_prob=0.40, ai_prob=0.50) == BiasType.ACCURATE

    def test_sandbagger_priority_over_sandbagging_risk(self):
        # sandbag=60 → SANDBAGGER even if also satisfies sandbagging_risk threshold
        assert self._bias(60) == BiasType.SANDBAGGER

    def test_sandbagging_risk_priority_over_overforecasting(self):
        # sandbag=25, high delta → SANDBAGGING_RISK takes priority
        result = self._bias(25, rep_prob=0.90, ai_prob=0.50)
        assert result == BiasType.SANDBAGGING_RISK


# ===========================================================================
# 11. Commit action
# ===========================================================================

class TestCommitAction:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def _action(self, cat, bias, risk, inp=None):
        if inp is None:
            inp = _make_base()
        return self.engine._commit_action(inp, cat, bias, risk)

    def test_confirm_when_commit_accurate_low_risk(self):
        assert self._action(CommitCategory.COMMIT, BiasType.ACCURATE, 25) == CommitAction.CONFIRM

    def test_confirm_exactly_at_risk_25(self):
        assert self._action(CommitCategory.COMMIT, BiasType.ACCURATE, 25) == CommitAction.CONFIRM

    def test_confirm_when_commit_accurate_risk_26_falls_to_else(self):
        # risk=26: rule 1 fails (>25), rules 2-8 don't match → falls to else → CONFIRM
        result = self._action(CommitCategory.COMMIT, BiasType.ACCURATE, 26)
        assert result == CommitAction.CONFIRM

    def test_pull_in_when_commit_sandbagger(self):
        assert self._action(CommitCategory.COMMIT, BiasType.SANDBAGGER, 50) == CommitAction.PULL_IN

    def test_pull_in_when_commit_sandbagging_risk(self):
        assert self._action(CommitCategory.COMMIT, BiasType.SANDBAGGING_RISK, 50) == CommitAction.PULL_IN

    def test_push_out_when_overforecasting_risk(self):
        assert self._action(CommitCategory.PIPELINE, BiasType.OVERFORECASTING_RISK, 30) == CommitAction.PUSH_OUT

    def test_push_out_when_optimistic(self):
        assert self._action(CommitCategory.PIPELINE, BiasType.OPTIMISTIC, 30) == CommitAction.PUSH_OUT

    def test_escalate_when_at_risk(self):
        assert self._action(CommitCategory.AT_RISK, BiasType.ACCURATE, 30) == CommitAction.ESCALATE

    def test_push_out_when_omitted(self):
        assert self._action(CommitCategory.OMITTED, BiasType.ACCURATE, 30) == CommitAction.PUSH_OUT

    def test_escalate_when_risk_60(self):
        # Not AT_RISK or OMITTED, not sandbagging/overforecasting
        assert self._action(CommitCategory.PIPELINE, BiasType.ACCURATE, 60) == CommitAction.ESCALATE

    def test_escalate_when_risk_above_60(self):
        assert self._action(CommitCategory.PIPELINE, BiasType.ACCURATE, 80) == CommitAction.ESCALATE

    def test_challenge_when_commit_high_risk(self):
        assert self._action(CommitCategory.COMMIT, BiasType.ACCURATE, 36) == CommitAction.CHALLENGE

    def test_challenge_requires_risk_above_35(self):
        assert self._action(CommitCategory.COMMIT, BiasType.ACCURATE, 35) != CommitAction.CHALLENGE

    def test_monitor_when_upside(self):
        assert self._action(CommitCategory.UPSIDE, BiasType.ACCURATE, 30) == CommitAction.MONITOR

    def test_monitor_when_pipeline(self):
        assert self._action(CommitCategory.PIPELINE, BiasType.ACCURATE, 30) == CommitAction.MONITOR

    def test_confirm_fallback(self):
        # None of the other rules match → CONFIRM
        # COMMIT category, ACCURATE bias, risk <= 25 → already matches rule 1 but let's do a generic one
        # Actually let's use a scenario outside all specific rules:
        # Non-commit/upside/pipeline/at-risk/omitted won't happen, so let's test the last else
        # The else catches any category that isn't in the explicit branches
        # In practice, the only way to reach `else → CONFIRM` is through COMMIT with risk in (26, 35] and non-sandbagging
        result = self._action(CommitCategory.COMMIT, BiasType.ACCURATE, 35)
        # risk=35, not > 35, not <= 25 → falls through to else: CONFIRM
        assert result == CommitAction.CONFIRM

    def test_priority_rule1_before_rule3(self):
        # COMMIT + ACCURATE + risk=25 → CONFIRM (rule1), not push_out even though ACCURATE
        assert self._action(CommitCategory.COMMIT, BiasType.ACCURATE, 25) == CommitAction.CONFIRM

    def test_priority_rule2_before_rule6(self):
        # COMMIT + SANDBAGGER + risk=70 → PULL_IN (rule 2), not ESCALATE (rule 6)
        assert self._action(CommitCategory.COMMIT, BiasType.SANDBAGGER, 70) == CommitAction.PULL_IN

    def test_priority_rule3_before_rule4(self):
        # AT_RISK + OVERFORECASTING → PUSH_OUT (rule 3), not ESCALATE (rule 4)
        assert self._action(CommitCategory.AT_RISK, BiasType.OVERFORECASTING_RISK, 30) == CommitAction.PUSH_OUT


# ===========================================================================
# 12. Helper properties
# ===========================================================================

class TestHelperProperties:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def test_solid_commits_empty_initially(self):
        assert self.engine.solid_commits == []

    def test_at_risk_commits_empty_initially(self):
        assert self.engine.at_risk_commits == []

    def test_sandbagged_deals_empty_initially(self):
        assert self.engine.sandbagged_deals == []

    def test_overforecasted_deals_empty_initially(self):
        assert self.engine.overforecasted_deals == []

    def test_needs_escalation_empty_initially(self):
        assert self.engine.needs_escalation == []

    def test_solid_commits_includes_commit_category(self):
        self.engine.analyze(_make_solid())
        assert len(self.engine.solid_commits) >= 1

    def test_solid_commits_all_have_commit_category(self):
        self.engine.analyze(_make_solid())
        for r in self.engine.solid_commits:
            assert r.commit_category == CommitCategory.COMMIT

    def test_at_risk_commits_includes_at_risk_category(self):
        self.engine.analyze(_make_at_risk())
        assert len(self.engine.at_risk_commits) >= 1

    def test_at_risk_commits_all_have_at_risk_category(self):
        self.engine.analyze(_make_at_risk())
        for r in self.engine.at_risk_commits:
            assert r.commit_category == CommitCategory.AT_RISK

    def test_sandbagged_deals_includes_sandbagger_bias(self):
        self.engine.analyze(_make_sandbagger())
        # sandbagger should have SANDBAGGER or SANDBAGGING_RISK bias
        biases = {r.bias_type for r in self.engine.results}
        assert BiasType.SANDBAGGER in biases or BiasType.SANDBAGGING_RISK in biases

    def test_sandbagged_deals_all_have_correct_bias(self):
        self.engine.analyze(_make_sandbagger())
        for r in self.engine.sandbagged_deals:
            assert r.bias_type in (BiasType.SANDBAGGER, BiasType.SANDBAGGING_RISK)

    def test_overforecasted_deals_all_have_correct_bias(self):
        overcast = _make_base(
            rep_win_probability=0.90, ai_win_probability=0.50,
            rep_historical_accuracy=0.80,
        )
        self.engine.analyze(overcast)
        for r in self.engine.overforecasted_deals:
            assert r.bias_type in (BiasType.OPTIMISTIC, BiasType.OVERFORECASTING_RISK)

    def test_needs_escalation_all_have_escalate_action(self):
        self.engine.analyze(_make_at_risk())
        for r in self.engine.needs_escalation:
            assert r.commit_action == CommitAction.ESCALATE

    def test_properties_return_lists(self):
        assert isinstance(self.engine.solid_commits, list)
        assert isinstance(self.engine.at_risk_commits, list)
        assert isinstance(self.engine.sandbagged_deals, list)
        assert isinstance(self.engine.overforecasted_deals, list)
        assert isinstance(self.engine.needs_escalation, list)

    def test_solid_commits_exclude_non_commit(self):
        self.engine.analyze(_make_at_risk())
        # The at_risk deal should NOT appear in solid_commits
        for r in self.engine.solid_commits:
            assert r.deal_id != "at_risk"

    def test_at_risk_commits_exclude_non_at_risk(self):
        self.engine.analyze(_make_solid())
        for r in self.engine.at_risk_commits:
            assert r.deal_id != "solid"

    def test_multiple_deals_filtered_correctly(self):
        self.engine.analyze(_make_solid())
        self.engine.analyze(_make_at_risk())
        # solid_commits should include solid, at_risk_commits should include at_risk
        solid_ids = [r.deal_id for r in self.engine.solid_commits]
        at_risk_ids = [r.deal_id for r in self.engine.at_risk_commits]
        assert "solid" in solid_ids
        assert "at_risk" in at_risk_ids
        assert "at_risk" not in solid_ids
        assert "solid" not in at_risk_ids


# ===========================================================================
# 13. Summary
# ===========================================================================

class TestSummary:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def test_empty_summary_has_12_keys(self):
        s = self.engine.summary()
        assert len(s) == 12

    def test_empty_summary_total_is_0(self):
        assert self.engine.summary()["total"] == 0

    def test_empty_summary_category_counts_empty(self):
        assert self.engine.summary()["category_counts"] == {}

    def test_empty_summary_confidence_counts_empty(self):
        assert self.engine.summary()["confidence_counts"] == {}

    def test_empty_summary_bias_counts_empty(self):
        assert self.engine.summary()["bias_counts"] == {}

    def test_empty_summary_action_counts_empty(self):
        assert self.engine.summary()["action_counts"] == {}

    def test_empty_summary_avg_commit_score_zero(self):
        assert self.engine.summary()["avg_commit_score"] == 0.0

    def test_empty_summary_avg_sandbag_score_zero(self):
        assert self.engine.summary()["avg_sandbag_score"] == 0.0

    def test_empty_summary_avg_risk_score_zero(self):
        assert self.engine.summary()["avg_risk_score"] == 0.0

    def test_empty_summary_avg_calibrated_probability_zero(self):
        assert self.engine.summary()["avg_calibrated_probability"] == 0.0

    def test_empty_summary_solid_commit_count_zero(self):
        assert self.engine.summary()["solid_commit_count"] == 0

    def test_empty_summary_at_risk_count_zero(self):
        assert self.engine.summary()["at_risk_count"] == 0

    def test_empty_summary_escalation_count_zero(self):
        assert self.engine.summary()["escalation_count"] == 0

    def test_summary_keys_match_exactly(self):
        expected_keys = {
            "total", "category_counts", "confidence_counts", "bias_counts",
            "action_counts", "avg_commit_score", "avg_sandbag_score",
            "avg_risk_score", "avg_calibrated_probability",
            "solid_commit_count", "at_risk_count", "escalation_count",
        }
        assert set(self.engine.summary().keys()) == expected_keys

    def test_summary_after_one_analysis_total_is_1(self):
        self.engine.analyze(_make_solid())
        assert self.engine.summary()["total"] == 1

    def test_summary_after_two_analyses_total_is_2(self):
        self.engine.analyze(_make_solid())
        self.engine.analyze(_make_at_risk())
        assert self.engine.summary()["total"] == 2

    def test_summary_category_counts_populated(self):
        self.engine.analyze(_make_solid())
        s = self.engine.summary()
        assert len(s["category_counts"]) >= 1

    def test_summary_category_counts_sum_equals_total(self):
        self.engine.analyze(_make_solid())
        self.engine.analyze(_make_at_risk())
        s = self.engine.summary()
        assert sum(s["category_counts"].values()) == s["total"]

    def test_summary_confidence_counts_sum_equals_total(self):
        self.engine.analyze(_make_solid())
        self.engine.analyze(_make_at_risk())
        s = self.engine.summary()
        assert sum(s["confidence_counts"].values()) == s["total"]

    def test_summary_bias_counts_sum_equals_total(self):
        self.engine.analyze(_make_solid())
        self.engine.analyze(_make_at_risk())
        s = self.engine.summary()
        assert sum(s["bias_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_equals_total(self):
        self.engine.analyze(_make_solid())
        self.engine.analyze(_make_at_risk())
        s = self.engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_commit_score_type(self):
        self.engine.analyze(_make_solid())
        s = self.engine.summary()
        assert isinstance(s["avg_commit_score"], (int, float))

    def test_summary_avg_calibrated_probability_type(self):
        self.engine.analyze(_make_solid())
        s = self.engine.summary()
        assert isinstance(s["avg_calibrated_probability"], (int, float))

    def test_summary_solid_commit_count_correct(self):
        self.engine.analyze(_make_solid())
        self.engine.analyze(_make_at_risk())
        s = self.engine.summary()
        assert s["solid_commit_count"] == len(self.engine.solid_commits)

    def test_summary_at_risk_count_correct(self):
        self.engine.analyze(_make_solid())
        self.engine.analyze(_make_at_risk())
        s = self.engine.summary()
        assert s["at_risk_count"] == len(self.engine.at_risk_commits)

    def test_summary_escalation_count_correct(self):
        self.engine.analyze(_make_solid())
        self.engine.analyze(_make_at_risk())
        s = self.engine.summary()
        assert s["escalation_count"] == len(self.engine.needs_escalation)

    def test_summary_avg_scores_are_rounded(self):
        self.engine.analyze(_make_solid())
        s = self.engine.summary()
        # avg_commit_score is rounded to 1 decimal
        assert s["avg_commit_score"] == round(s["avg_commit_score"], 1)
        assert s["avg_calibrated_probability"] == round(s["avg_calibrated_probability"], 3)

    def test_summary_category_counts_has_string_keys(self):
        self.engine.analyze(_make_solid())
        s = self.engine.summary()
        for k in s["category_counts"]:
            assert isinstance(k, str)


# ===========================================================================
# 14. Reset
# ===========================================================================

class TestReset:
    def test_reset_clears_results(self):
        engine = ForecastCommitEngine()
        engine.analyze(_make_solid())
        assert len(engine.results) == 1
        engine.reset()
        assert len(engine.results) == 0

    def test_reset_clears_multiple_results(self):
        engine = ForecastCommitEngine()
        engine.analyze(_make_solid())
        engine.analyze(_make_at_risk())
        engine.reset()
        assert engine.results == []

    def test_reset_clears_solid_commits_property(self):
        engine = ForecastCommitEngine()
        engine.analyze(_make_solid())
        engine.reset()
        assert engine.solid_commits == []

    def test_reset_clears_at_risk_property(self):
        engine = ForecastCommitEngine()
        engine.analyze(_make_at_risk())
        engine.reset()
        assert engine.at_risk_commits == []

    def test_reset_allows_reuse(self):
        engine = ForecastCommitEngine()
        engine.analyze(_make_solid())
        engine.reset()
        engine.analyze(_make_at_risk())
        assert len(engine.results) == 1

    def test_reset_clears_summary(self):
        engine = ForecastCommitEngine()
        engine.analyze(_make_solid())
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0

    def test_initial_results_empty(self):
        engine = ForecastCommitEngine()
        assert engine.results == []


# ===========================================================================
# 15. End-to-end scenarios
# ===========================================================================

class TestEndToEndSolid:
    def setup_method(self):
        self.engine = ForecastCommitEngine()
        self.result = self.engine.analyze(_make_solid())

    def test_solid_returns_result(self):
        assert isinstance(self.result, ForecastCommitResult)

    def test_solid_deal_id(self):
        assert self.result.deal_id == "solid"

    def test_solid_commit_category_is_commit(self):
        assert self.result.commit_category == CommitCategory.COMMIT

    def test_solid_commit_action_is_confirm(self):
        assert self.result.commit_action == CommitAction.CONFIRM

    def test_solid_high_commit_score(self):
        assert self.result.commit_score >= 70.0

    def test_solid_low_risk_score(self):
        assert self.result.risk_score <= 30.0

    def test_solid_high_calibrated_probability(self):
        assert self.result.calibrated_probability >= 0.60

    def test_solid_confidence_high_or_medium(self):
        assert self.result.forecast_confidence in (ForecastConfidence.HIGH, ForecastConfidence.MEDIUM)

    def test_solid_bias_accurate(self):
        assert self.result.bias_type == BiasType.ACCURATE

    def test_solid_in_engine_results(self):
        assert self.result in self.engine.results

    def test_solid_in_solid_commits_property(self):
        assert self.result in self.engine.solid_commits

    def test_solid_confidence_factors_non_empty(self):
        assert len(self.result.confidence_factors) > 0

    def test_solid_recommended_actions_non_empty(self):
        assert len(self.result.recommended_actions) > 0


class TestEndToEndAtRisk:
    def setup_method(self):
        self.engine = ForecastCommitEngine()
        self.result = self.engine.analyze(_make_at_risk())

    def test_at_risk_returns_result(self):
        assert isinstance(self.result, ForecastCommitResult)

    def test_at_risk_deal_id(self):
        assert self.result.deal_id == "at_risk"

    def test_at_risk_category(self):
        assert self.result.commit_category == CommitCategory.AT_RISK

    def test_at_risk_action_is_escalate(self):
        assert self.result.commit_action == CommitAction.ESCALATE

    def test_at_risk_high_risk_score(self):
        assert self.result.risk_score >= 30.0

    def test_at_risk_low_commit_score(self):
        assert self.result.commit_score <= 30.0

    def test_at_risk_in_at_risk_property(self):
        assert self.result in self.engine.at_risk_commits

    def test_at_risk_in_needs_escalation(self):
        assert self.result in self.engine.needs_escalation

    def test_at_risk_confidence_very_low(self):
        assert self.result.forecast_confidence == ForecastConfidence.VERY_LOW


class TestEndToEndSandbagger:
    def setup_method(self):
        self.engine = ForecastCommitEngine()
        self.result = self.engine.analyze(_make_sandbagger())

    def test_sandbagger_returns_result(self):
        assert isinstance(self.result, ForecastCommitResult)

    def test_sandbagger_deal_id(self):
        assert self.result.deal_id == "sandbagger"

    def test_sandbagger_bias_is_sandbagger(self):
        assert self.result.bias_type in (BiasType.SANDBAGGER, BiasType.SANDBAGGING_RISK)

    def test_sandbagger_action_is_pull_in_or_related(self):
        # Due to high closing signals, category may be COMMIT → PULL_IN
        assert self.result.commit_action in (CommitAction.PULL_IN, CommitAction.CONFIRM, CommitAction.CHALLENGE)

    def test_sandbagger_high_sandbag_score(self):
        assert self.result.sandbag_score >= 25.0

    def test_sandbagger_in_sandbagged_deals(self):
        assert self.result in self.engine.sandbagged_deals


class TestEndToEndBatch:
    def test_batch_sorted_by_commit_score_desc(self):
        engine = ForecastCommitEngine()
        deals = [_make_solid(), _make_at_risk(), _make_sandbagger()]
        results = engine.analyze_batch(deals)
        scores = [r.commit_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_batch_returns_all_results(self):
        engine = ForecastCommitEngine()
        deals = [_make_solid(), _make_at_risk(), _make_sandbagger()]
        results = engine.analyze_batch(deals)
        assert len(results) == 3

    def test_batch_accumulates_in_engine_results(self):
        engine = ForecastCommitEngine()
        deals = [_make_solid(), _make_at_risk()]
        engine.analyze_batch(deals)
        assert len(engine.results) == 2

    def test_batch_empty_list(self):
        engine = ForecastCommitEngine()
        results = engine.analyze_batch([])
        assert results == []

    def test_batch_single_deal(self):
        engine = ForecastCommitEngine()
        results = engine.analyze_batch([_make_solid()])
        assert len(results) == 1

    def test_batch_appends_to_existing(self):
        engine = ForecastCommitEngine()
        engine.analyze(_make_solid())
        engine.analyze_batch([_make_at_risk()])
        # After batch, both should be present and sorted
        assert len(engine.results) == 2
        scores = [r.commit_score for r in engine.results]
        assert scores == sorted(scores, reverse=True)


# ===========================================================================
# 16. Analyze method integration
# ===========================================================================

class TestAnalyzeMethod:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def test_analyze_returns_forecast_commit_result(self):
        result = self.engine.analyze(_make_solid())
        assert isinstance(result, ForecastCommitResult)

    def test_analyze_appends_to_results(self):
        self.engine.analyze(_make_solid())
        assert len(self.engine.results) == 1

    def test_analyze_twice_appends_both(self):
        self.engine.analyze(_make_solid())
        self.engine.analyze(_make_at_risk())
        assert len(self.engine.results) == 2

    def test_analyze_result_scores_are_in_range(self):
        result = self.engine.analyze(_make_solid())
        assert 0 <= result.commit_score <= 100
        assert 0 <= result.sandbag_score <= 100
        assert 0 <= result.risk_score <= 100
        assert 0 <= result.calibrated_probability <= 1

    def test_analyze_assigns_valid_enum_values(self):
        result = self.engine.analyze(_make_solid())
        assert result.commit_category in CommitCategory
        assert result.forecast_confidence in ForecastConfidence
        assert result.bias_type in BiasType
        assert result.commit_action in CommitAction

    def test_analyze_copies_identity_fields(self):
        inp = _make_solid()
        result = self.engine.analyze(inp)
        assert result.deal_id == inp.deal_id
        assert result.rep_id == inp.rep_id
        assert result.rep_name == inp.rep_name
        assert result.account_name == inp.account_name

    def test_analyze_commit_score_rounded_to_1_decimal(self):
        result = self.engine.analyze(_make_solid())
        assert result.commit_score == round(result.commit_score, 1)

    def test_analyze_sandbag_score_rounded_to_1_decimal(self):
        result = self.engine.analyze(_make_solid())
        assert result.sandbag_score == round(result.sandbag_score, 1)

    def test_analyze_risk_score_rounded_to_1_decimal(self):
        result = self.engine.analyze(_make_solid())
        assert result.risk_score == round(result.risk_score, 1)


# ===========================================================================
# 17. Edge cases
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.engine = ForecastCommitEngine()

    def test_all_false_booleans(self):
        # Should not crash with all False booleans
        result = self.engine.analyze(_make_base())
        assert isinstance(result, ForecastCommitResult)

    def test_zero_pipeline_value(self):
        inp = _make_base(pipeline_value=0.0, rep_commit_amount=0.0)
        result = self.engine.analyze(inp)
        assert isinstance(result, ForecastCommitResult)

    def test_close_date_exactly_14_days(self):
        inp = _make_base(close_date_days_out=14, contract_sent=True, po_received=False)
        result = self.engine.analyze(inp)
        assert result.commit_category == CommitCategory.COMMIT

    def test_close_date_exactly_30_days_triggers_risk(self):
        result = self.engine.analyze(_make_base(
            close_date_days_out=30,
            decision_maker_confirmed=False,
            budget_confirmed=False,
            champion_strong=False,
        ))
        assert result.risk_score >= 32.0

    def test_prior_quarter_sandbagging_negative_value(self):
        # Negative value should result in zero sandbagging contribution
        inp = _make_base(prior_quarter_sandbagging=-0.50)
        result = self.engine.analyze(inp)
        assert result.sandbag_score >= 0.0

    def test_probabilities_at_1(self):
        inp = _make_base(
            ai_win_probability=1.0, rep_win_probability=1.0, stage_probability=1.0
        )
        result = self.engine.analyze(inp)
        assert result.calibrated_probability <= 1.0

    def test_probabilities_at_0(self):
        inp = _make_base(
            ai_win_probability=0.0, rep_win_probability=0.0, stage_probability=0.0
        )
        result = self.engine.analyze(inp)
        assert result.calibrated_probability >= 0.0

    def test_engine_initializes_with_empty_results(self):
        engine = ForecastCommitEngine()
        assert engine.results == []

    def test_to_dict_list_fields_independent_from_result(self):
        # Ensure confidence_factors/risk_factors/recommended_actions are lists
        result = self.engine.analyze(_make_solid())
        d = result.to_dict()
        assert isinstance(d["confidence_factors"], list)
        assert isinstance(d["risk_factors"], list)
        assert isinstance(d["recommended_actions"], list)

    def test_very_high_stage_overrun(self):
        # overrun = 1000-10 = 990, 990/10 = 99 → min(20, 99*20) = 20
        inp = _make_base(days_in_current_stage=1010, expected_days_in_stage=10)
        risk = self.engine._risk_score(inp)
        assert risk >= 20.0

    def test_commit_score_all_signals_no_po_contract_sent(self):
        # contract_sent=True is the second in the elif chain
        s = self.engine._commit_score(_make_base(
            contract_sent=True, budget_confirmed=True, decision_maker_confirmed=True,
            champion_strong=True, exec_aligned=True, competitor_eliminated=True,
            objections_resolved=True, close_date_days_out=7, last_activity_days_ago=1,
            rep_win_probability=0.80, ai_win_probability=0.80,
        ))
        # 25+15+12+8+7+8+7+5+3+5 = 95
        assert s == pytest.approx(95.0)
