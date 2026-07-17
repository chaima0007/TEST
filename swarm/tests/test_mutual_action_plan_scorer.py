"""Comprehensive pytest test suite for Module 74 — Mutual Action Plan Adherence Scorer."""
from __future__ import annotations

import pytest

from swarm.intelligence.mutual_action_plan_scorer import (
    MAPHealth,
    AdherencePattern,
    CommitmentSignal,
    MAPAction,
    MutualActionPlanInput,
    MAPAdherenceResult,
    MutualActionPlanScorer,
)


# ---------------------------------------------------------------------------
# Helper factory — all fields have sensible defaults
# ---------------------------------------------------------------------------

def make_inp(
    deal_id: str = "deal-1",
    deal_name: str = "Acme Corp",
    rep_id: str = "rep-1",
    map_start_date_days_ago: int = 30,
    total_milestones: int = 10,
    rep_milestones_completed: int = 5,
    rep_milestones_missed: int = 1,
    buyer_milestones_completed: int = 5,
    buyer_milestones_missed: int = 1,
    buyer_response_time_avg_hours: float = 12.0,
    map_last_reviewed_days_ago: int = 7,
    close_date_agreed_in_map: int = 1,
    close_date_changes_since_map: int = 0,
    legal_milestone_in_map: int = 0,
    legal_milestone_completed: int = 0,
    technical_milestone_in_map: int = 0,
    technical_milestone_completed: int = 0,
    executive_sign_off_milestone: int = 0,
    executive_sign_off_done: int = 0,
    mutual_success_criteria_defined: int = 1,
    buyer_shared_map_internally: int = 0,
    deal_value: float = 50_000.0,
) -> MutualActionPlanInput:
    return MutualActionPlanInput(
        deal_id=deal_id,
        deal_name=deal_name,
        rep_id=rep_id,
        map_start_date_days_ago=map_start_date_days_ago,
        total_milestones=total_milestones,
        rep_milestones_completed=rep_milestones_completed,
        rep_milestones_missed=rep_milestones_missed,
        buyer_milestones_completed=buyer_milestones_completed,
        buyer_milestones_missed=buyer_milestones_missed,
        buyer_response_time_avg_hours=buyer_response_time_avg_hours,
        map_last_reviewed_days_ago=map_last_reviewed_days_ago,
        close_date_agreed_in_map=close_date_agreed_in_map,
        close_date_changes_since_map=close_date_changes_since_map,
        legal_milestone_in_map=legal_milestone_in_map,
        legal_milestone_completed=legal_milestone_completed,
        technical_milestone_in_map=technical_milestone_in_map,
        technical_milestone_completed=technical_milestone_completed,
        executive_sign_off_milestone=executive_sign_off_milestone,
        executive_sign_off_done=executive_sign_off_done,
        mutual_success_criteria_defined=mutual_success_criteria_defined,
        buyer_shared_map_internally=buyer_shared_map_internally,
        deal_value=deal_value,
    )


def make_scorer() -> MutualActionPlanScorer:
    return MutualActionPlanScorer()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestMAPHealthEnum:
    def test_on_track_value(self):
        assert MAPHealth.ON_TRACK.value == "on_track"

    def test_slipping_value(self):
        assert MAPHealth.SLIPPING.value == "slipping"

    def test_at_risk_value(self):
        assert MAPHealth.AT_RISK.value == "at_risk"

    def test_broken_value(self):
        assert MAPHealth.BROKEN.value == "broken"

    def test_all_members_count(self):
        assert len(MAPHealth) == 4

    def test_str_subclass(self):
        assert isinstance(MAPHealth.ON_TRACK, str)
        assert MAPHealth.ON_TRACK == "on_track"

    def test_enum_iteration(self):
        values = {m.value for m in MAPHealth}
        assert values == {"on_track", "slipping", "at_risk", "broken"}


class TestAdherencePatternEnum:
    def test_both_committed_value(self):
        assert AdherencePattern.BOTH_COMMITTED.value == "both_committed"

    def test_rep_only_value(self):
        assert AdherencePattern.REP_ONLY.value == "rep_only"

    def test_buyer_leading_value(self):
        assert AdherencePattern.BUYER_LEADING.value == "buyer_leading"

    def test_buyer_ghosting_value(self):
        assert AdherencePattern.BUYER_GHOSTING.value == "buyer_ghosting"

    def test_mutual_drift_value(self):
        assert AdherencePattern.MUTUAL_DRIFT.value == "mutual_drift"

    def test_complete_breakdown_value(self):
        assert AdherencePattern.COMPLETE_BREAKDOWN.value == "complete_breakdown"

    def test_all_members_count(self):
        assert len(AdherencePattern) == 6

    def test_str_subclass(self):
        assert isinstance(AdherencePattern.BOTH_COMMITTED, str)


class TestCommitmentSignalEnum:
    def test_strong_value(self):
        assert CommitmentSignal.STRONG.value == "strong"

    def test_moderate_value(self):
        assert CommitmentSignal.MODERATE.value == "moderate"

    def test_weak_value(self):
        assert CommitmentSignal.WEAK.value == "weak"

    def test_absent_value(self):
        assert CommitmentSignal.ABSENT.value == "absent"

    def test_all_members_count(self):
        assert len(CommitmentSignal) == 4

    def test_str_subclass(self):
        assert isinstance(CommitmentSignal.STRONG, str)


class TestMAPActionEnum:
    def test_accelerate_value(self):
        assert MAPAction.ACCELERATE.value == "accelerate"

    def test_reaffirm_value(self):
        assert MAPAction.REAFFIRM.value == "reaffirm"

    def test_reset_map_value(self):
        assert MAPAction.RESET_MAP.value == "reset_map"

    def test_escalate_value(self):
        assert MAPAction.ESCALATE.value == "escalate"

    def test_all_members_count(self):
        assert len(MAPAction) == 4

    def test_str_subclass(self):
        assert isinstance(MAPAction.ACCELERATE, str)


# ===========================================================================
# 2. INPUT FIELD COUNT
# ===========================================================================

class TestMutualActionPlanInputFields:
    def test_exactly_22_fields(self):
        inp = make_inp()
        fields = list(inp.__dataclass_fields__.keys())
        assert len(fields) == 22

    def test_field_names(self):
        expected = {
            "deal_id", "deal_name", "rep_id", "map_start_date_days_ago",
            "total_milestones", "rep_milestones_completed", "rep_milestones_missed",
            "buyer_milestones_completed", "buyer_milestones_missed",
            "buyer_response_time_avg_hours", "map_last_reviewed_days_ago",
            "close_date_agreed_in_map", "close_date_changes_since_map",
            "legal_milestone_in_map", "legal_milestone_completed",
            "technical_milestone_in_map", "technical_milestone_completed",
            "executive_sign_off_milestone", "executive_sign_off_done",
            "mutual_success_criteria_defined", "buyer_shared_map_internally",
            "deal_value",
        }
        inp = make_inp()
        assert set(inp.__dataclass_fields__.keys()) == expected

    def test_is_dataclass(self):
        from dataclasses import fields
        inp = make_inp()
        assert len(fields(inp)) == 22


# ===========================================================================
# 3. RESULT FIELD COUNT
# ===========================================================================

class TestMAPAdherenceResultFields:
    def test_to_dict_exactly_15_keys(self):
        scorer = make_scorer()
        result = scorer.score(make_inp())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        expected = {
            "deal_id", "deal_name", "map_health", "adherence_pattern",
            "commitment_signal", "map_action", "rep_adherence_score",
            "buyer_adherence_score", "milestone_progress_score",
            "map_quality_score", "map_adherence_composite",
            "estimated_close_confidence", "days_to_close_risk",
            "is_healthy_map", "needs_map_reset",
        }
        scorer = make_scorer()
        result = scorer.score(make_inp())
        assert set(result.to_dict().keys()) == expected

    def test_to_dict_enum_values_are_strings(self):
        scorer = make_scorer()
        d = scorer.score(make_inp()).to_dict()
        assert isinstance(d["map_health"], str)
        assert isinstance(d["adherence_pattern"], str)
        assert isinstance(d["commitment_signal"], str)
        assert isinstance(d["map_action"], str)

    def test_to_dict_bool_fields(self):
        scorer = make_scorer()
        d = scorer.score(make_inp()).to_dict()
        assert isinstance(d["is_healthy_map"], bool)
        assert isinstance(d["needs_map_reset"], bool)

    def test_to_dict_preserves_deal_id(self):
        scorer = make_scorer()
        d = scorer.score(make_inp(deal_id="xyz-123")).to_dict()
        assert d["deal_id"] == "xyz-123"

    def test_to_dict_preserves_deal_name(self):
        scorer = make_scorer()
        d = scorer.score(make_inp(deal_name="Big Corp")).to_dict()
        assert d["deal_name"] == "Big Corp"


# ===========================================================================
# 4. SUMMARY KEY COUNT
# ===========================================================================

class TestSummaryKeyCount:
    def test_empty_summary_has_13_keys(self):
        scorer = make_scorer()
        s = scorer.summary()
        assert len(s) == 13

    def test_nonempty_summary_has_13_keys(self):
        scorer = make_scorer()
        scorer.score(make_inp())
        s = scorer.summary()
        assert len(s) == 13

    def test_summary_key_names(self):
        expected = {
            "total", "health_counts", "pattern_counts", "signal_counts",
            "action_counts", "avg_map_adherence_composite", "avg_close_confidence",
            "healthy_map_count", "reset_needed_count", "avg_rep_adherence_score",
            "avg_buyer_adherence_score", "avg_milestone_progress_score",
            "avg_map_quality_score",
        }
        scorer = make_scorer()
        assert set(scorer.summary().keys()) == expected

    def test_summary_empty_totals(self):
        scorer = make_scorer()
        s = scorer.summary()
        assert s["total"] == 0
        assert s["avg_map_adherence_composite"] == 0.0
        assert s["avg_close_confidence"] == 0.0
        assert s["healthy_map_count"] == 0
        assert s["reset_needed_count"] == 0
        assert s["avg_rep_adherence_score"] == 0.0
        assert s["avg_buyer_adherence_score"] == 0.0
        assert s["avg_milestone_progress_score"] == 0.0
        assert s["avg_map_quality_score"] == 0.0

    def test_summary_empty_dicts(self):
        scorer = make_scorer()
        s = scorer.summary()
        assert s["health_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["signal_counts"] == {}
        assert s["action_counts"] == {}


# ===========================================================================
# 5. REP ADHERENCE SCORE
# ===========================================================================

class TestRepAdherenceScore:
    def setup_method(self):
        self.scorer = make_scorer()

    def _score(self, **kwargs) -> float:
        return self.scorer._rep_adherence_score(make_inp(**kwargs))

    def test_no_data_returns_50(self):
        assert self._score(rep_milestones_completed=0, rep_milestones_missed=0) == 50.0

    def test_perfect_rate_no_bonus(self):
        # completed=1, missed=0: rate=1.0 → 80; but completed<2 so no +20; reviewed=7 → +10
        score = self._score(rep_milestones_completed=1, rep_milestones_missed=0,
                            map_last_reviewed_days_ago=7)
        assert score == min(100.0, 80.0 + 10.0)

    def test_perfect_rate_with_bonus(self):
        # completed=2, missed=0 → 80+20=100; reviewed=7 → +10 → clamped 100
        score = self._score(rep_milestones_completed=2, rep_milestones_missed=0,
                            map_last_reviewed_days_ago=7)
        assert score == 100.0

    def test_perfect_rate_bonus_no_recent_review(self):
        # completed=2, missed=0 → 100; reviewed=15 (neither <=7 nor >=30)
        score = self._score(rep_milestones_completed=2, rep_milestones_missed=0,
                            map_last_reviewed_days_ago=15)
        assert score == 100.0

    def test_50pct_rate_no_bonus(self):
        # rate=0.5 → 40; reviewed=15
        score = self._score(rep_milestones_completed=1, rep_milestones_missed=1,
                            map_last_reviewed_days_ago=15)
        assert score == 40.0

    def test_reviewed_recently_adds_10(self):
        # completed=1, missed=1 → 40; reviewed=7 → +10
        score = self._score(rep_milestones_completed=1, rep_milestones_missed=1,
                            map_last_reviewed_days_ago=7)
        assert score == 50.0

    def test_reviewed_exactly_7_adds_10(self):
        score = self._score(rep_milestones_completed=1, rep_milestones_missed=1,
                            map_last_reviewed_days_ago=7)
        assert score == 50.0

    def test_reviewed_exactly_30_subtracts_10(self):
        score = self._score(rep_milestones_completed=1, rep_milestones_missed=1,
                            map_last_reviewed_days_ago=30)
        assert score == 30.0

    def test_reviewed_31_days_subtracts_10(self):
        score = self._score(rep_milestones_completed=1, rep_milestones_missed=1,
                            map_last_reviewed_days_ago=31)
        assert score == 30.0

    def test_reviewed_8_days_no_bonus(self):
        # 8 days: not <=7 and not >=30
        score = self._score(rep_milestones_completed=1, rep_milestones_missed=1,
                            map_last_reviewed_days_ago=8)
        assert score == 40.0

    def test_reviewed_29_days_no_penalty(self):
        score = self._score(rep_milestones_completed=1, rep_milestones_missed=1,
                            map_last_reviewed_days_ago=29)
        assert score == 40.0

    def test_clamp_min_zero(self):
        # rate=0, miss=5, reviewed>=30 → 0*80-10=-10 → clamped 0
        score = self._score(rep_milestones_completed=0, rep_milestones_missed=5,
                            map_last_reviewed_days_ago=30)
        assert score == 0.0

    def test_clamp_max_100(self):
        # completed=3, missed=0 → 80+20=100; reviewed=7 → +10 → 100
        score = self._score(rep_milestones_completed=3, rep_milestones_missed=0,
                            map_last_reviewed_days_ago=7)
        assert score == 100.0

    def test_zero_completed_nonzero_missed(self):
        # rate=0 → 0; reviewed=15 → 0
        score = self._score(rep_milestones_completed=0, rep_milestones_missed=3,
                            map_last_reviewed_days_ago=15)
        assert score == 0.0

    def test_score_is_rounded_to_1_decimal(self):
        # rate=1/3 → 26.666... → 26.7
        score = self._score(rep_milestones_completed=1, rep_milestones_missed=2,
                            map_last_reviewed_days_ago=15)
        assert score == round(80.0 / 3.0, 1)

    def test_bonus_requires_exactly_2_completed(self):
        # completed=2, missed=0 → qualifies for bonus
        score_2 = self._score(rep_milestones_completed=2, rep_milestones_missed=0,
                              map_last_reviewed_days_ago=15)
        # completed=1, missed=0 → no bonus
        score_1 = self._score(rep_milestones_completed=1, rep_milestones_missed=0,
                              map_last_reviewed_days_ago=15)
        assert score_2 == 100.0
        assert score_1 == 80.0

    def test_bonus_not_awarded_when_missed_gt_0(self):
        # completed=3, missed=1 → no bonus; rate=3/4=0.75 → 60
        score = self._score(rep_milestones_completed=3, rep_milestones_missed=1,
                            map_last_reviewed_days_ago=15)
        assert score == round(0.75 * 80.0, 1)

    def test_recent_review_clamps_at_100(self):
        # rate=1.0, comp=2, reviewed=7: 80+20+10 → clamped 100
        score = self._score(rep_milestones_completed=2, rep_milestones_missed=0,
                            map_last_reviewed_days_ago=7)
        assert score == 100.0

    def test_stale_review_can_push_below_zero_clamped(self):
        # rate=0 miss=1 reviewed>=30 → 0-10=-10 → 0
        score = self._score(rep_milestones_completed=0, rep_milestones_missed=1,
                            map_last_reviewed_days_ago=45)
        assert score == 0.0


# ===========================================================================
# 6. BUYER ADHERENCE SCORE
# ===========================================================================

class TestBuyerAdherenceScore:
    def setup_method(self):
        self.scorer = make_scorer()

    def _score(self, **kwargs) -> float:
        return self.scorer._buyer_adherence_score(make_inp(**kwargs))

    def test_no_data_returns_40(self):
        assert self._score(buyer_milestones_completed=0, buyer_milestones_missed=0) == 40.0

    def test_perfect_rate_no_shared(self):
        # completed=3, missed=0 → rate=1.0 → 70; shared=0; resp=12 (neutral)
        score = self._score(buyer_milestones_completed=3, buyer_milestones_missed=0,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=12.0)
        assert score == 70.0

    def test_shared_internally_adds_20(self):
        # rate=1.0 → 70+20=90; resp=12
        score = self._score(buyer_milestones_completed=3, buyer_milestones_missed=0,
                            buyer_shared_map_internally=1, buyer_response_time_avg_hours=12.0)
        assert score == 90.0

    def test_fast_response_adds_10(self):
        # rate=1.0 → 70; resp<=4 → +10 = 80
        score = self._score(buyer_milestones_completed=3, buyer_milestones_missed=0,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=4.0)
        assert score == 80.0

    def test_fast_response_exactly_4h(self):
        score = self._score(buyer_milestones_completed=3, buyer_milestones_missed=0,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=4.0)
        assert score == 80.0

    def test_slow_response_48h_subtracts_15(self):
        # rate=1.0 → 70; resp>=48 → -15 = 55
        score = self._score(buyer_milestones_completed=3, buyer_milestones_missed=0,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=48.0)
        assert score == 55.0

    def test_slow_response_exactly_48h(self):
        score = self._score(buyer_milestones_completed=3, buyer_milestones_missed=0,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=48.0)
        assert score == 55.0

    def test_medium_response_24h_subtracts_8(self):
        # rate=1.0 → 70; resp>=24 (but <48) → -8 = 62
        score = self._score(buyer_milestones_completed=3, buyer_milestones_missed=0,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=24.0)
        assert score == 62.0

    def test_medium_response_exactly_24h(self):
        score = self._score(buyer_milestones_completed=3, buyer_milestones_missed=0,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=24.0)
        assert score == 62.0

    def test_neutral_response_5h(self):
        # 5h: not <=4, not >=24 → no adjustment
        score = self._score(buyer_milestones_completed=3, buyer_milestones_missed=0,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=5.0)
        assert score == 70.0

    def test_shared_and_fast_response_clamp(self):
        # rate=1.0 → 70+20=90; resp<=4 → +10 → 100
        score = self._score(buyer_milestones_completed=3, buyer_milestones_missed=0,
                            buyer_shared_map_internally=1, buyer_response_time_avg_hours=1.0)
        assert score == 100.0

    def test_zero_buyer_completed_nonzero_missed(self):
        # rate=0 → 0; shared=0; resp=12 → 0
        score = self._score(buyer_milestones_completed=0, buyer_milestones_missed=3,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=12.0)
        assert score == 0.0

    def test_clamp_min_zero_via_slow_response(self):
        # rate=0 → 0; resp>=48 → -15 → clamped 0
        score = self._score(buyer_milestones_completed=0, buyer_milestones_missed=3,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=72.0)
        assert score == 0.0

    def test_50pct_rate_no_adjustments(self):
        # rate=0.5 → 35
        score = self._score(buyer_milestones_completed=1, buyer_milestones_missed=1,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=12.0)
        assert score == 35.0

    def test_shared_and_very_slow_response(self):
        # rate=0.5 → 35+20=55; resp>=48 → -15=40
        score = self._score(buyer_milestones_completed=1, buyer_milestones_missed=1,
                            buyer_shared_map_internally=1, buyer_response_time_avg_hours=72.0)
        assert score == 40.0

    def test_score_rounded_to_1_decimal(self):
        # rate=2/3 → 46.666... → 46.7
        score = self._score(buyer_milestones_completed=2, buyer_milestones_missed=1,
                            buyer_shared_map_internally=0, buyer_response_time_avg_hours=12.0)
        assert score == round(70.0 * 2 / 3, 1)


# ===========================================================================
# 7. MILESTONE PROGRESS SCORE
# ===========================================================================

class TestMilestoneProgressScore:
    def setup_method(self):
        self.scorer = make_scorer()

    def _score(self, **kwargs) -> float:
        return self.scorer._milestone_progress_score(make_inp(**kwargs))

    def test_zero_total_milestones_returns_20(self):
        assert self._score(total_milestones=0) == 20.0

    def test_basic_completion_pct(self):
        # total=10, rep_comp=5, buyer_comp=5 → completed=10/10=1.0 → 60; no critical, no changes
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=0,
                            technical_milestone_in_map=0, executive_sign_off_milestone=0,
                            close_date_changes_since_map=0)
        assert score == 60.0

    def test_legal_completed_adds_15(self):
        # total=10, complete=10 → 60; legal in map + completed → +15 = 75
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=1,
                            legal_milestone_completed=1, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, close_date_changes_since_map=0)
        assert score == 75.0

    def test_legal_in_map_not_completed_subtracts_5(self):
        # 60 - 5 = 55
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=1,
                            legal_milestone_completed=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, close_date_changes_since_map=0)
        assert score == 55.0

    def test_technical_completed_adds_12(self):
        # 60 + 12 = 72
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=0,
                            technical_milestone_in_map=1, technical_milestone_completed=1,
                            executive_sign_off_milestone=0, close_date_changes_since_map=0)
        assert score == 72.0

    def test_technical_in_map_not_completed_no_bonus(self):
        # no bonus, no penalty for technical not completed
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=0,
                            technical_milestone_in_map=1, technical_milestone_completed=0,
                            executive_sign_off_milestone=0, close_date_changes_since_map=0)
        assert score == 60.0

    def test_exec_done_adds_13(self):
        # 60 + 13 = 73
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=0,
                            technical_milestone_in_map=0, executive_sign_off_milestone=1,
                            executive_sign_off_done=1, close_date_changes_since_map=0)
        assert score == 73.0

    def test_exec_milestone_not_done_no_bonus(self):
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=0,
                            technical_milestone_in_map=0, executive_sign_off_milestone=1,
                            executive_sign_off_done=0, close_date_changes_since_map=0)
        assert score == 60.0

    def test_close_date_change_1_subtracts_7(self):
        # 60 - 7 = 53
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=0,
                            technical_milestone_in_map=0, executive_sign_off_milestone=0,
                            close_date_changes_since_map=1)
        assert score == 53.0

    def test_close_date_changes_capped_at_20(self):
        # 3 changes → 3*7=21 → capped 20; 60-20=40
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=0,
                            technical_milestone_in_map=0, executive_sign_off_milestone=0,
                            close_date_changes_since_map=3)
        assert score == 40.0

    def test_close_date_changes_exactly_at_cap_boundary(self):
        # 2 changes → 2*7=14 → <20; 60-14=46
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=0,
                            technical_milestone_in_map=0, executive_sign_off_milestone=0,
                            close_date_changes_since_map=2)
        assert score == 46.0

    def test_completion_pct_capped_at_1(self):
        # rep_comp+buyer_comp > total_milestones → pct capped at 1
        score = self._score(total_milestones=5, rep_milestones_completed=4,
                            buyer_milestones_completed=4, legal_milestone_in_map=0,
                            technical_milestone_in_map=0, executive_sign_off_milestone=0,
                            close_date_changes_since_map=0)
        assert score == 60.0

    def test_all_critical_milestones_complete(self):
        # 60 + 15 + 12 + 13 = 100
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=1,
                            legal_milestone_completed=1, technical_milestone_in_map=1,
                            technical_milestone_completed=1, executive_sign_off_milestone=1,
                            executive_sign_off_done=1, close_date_changes_since_map=0)
        assert score == 100.0

    def test_clamp_max_100(self):
        score = self._score(total_milestones=10, rep_milestones_completed=5,
                            buyer_milestones_completed=5, legal_milestone_in_map=1,
                            legal_milestone_completed=1, technical_milestone_in_map=1,
                            technical_milestone_completed=1, executive_sign_off_milestone=1,
                            executive_sign_off_done=1, close_date_changes_since_map=0)
        assert score <= 100.0

    def test_clamp_min_zero(self):
        # completion=0, legal not done, 3+ changes
        score = self._score(total_milestones=10, rep_milestones_completed=0,
                            buyer_milestones_completed=0, legal_milestone_in_map=1,
                            legal_milestone_completed=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, close_date_changes_since_map=10)
        assert score == 0.0

    def test_partial_completion(self):
        # total=8, rep_comp=2, buyer_comp=2 → 4/8=0.5 → 30; no critical
        score = self._score(total_milestones=8, rep_milestones_completed=2,
                            buyer_milestones_completed=2, legal_milestone_in_map=0,
                            technical_milestone_in_map=0, executive_sign_off_milestone=0,
                            close_date_changes_since_map=0)
        assert score == 30.0


# ===========================================================================
# 8. MAP QUALITY SCORE
# ===========================================================================

class TestMAPQualityScore:
    def setup_method(self):
        self.scorer = make_scorer()

    def _score(self, **kwargs) -> float:
        return self.scorer._map_quality_score(make_inp(**kwargs))

    def test_base_score_is_30(self):
        # no flags set, reviewed recently
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=5)
        assert score == 30.0

    def test_close_date_agreed_adds_20(self):
        score = self._score(close_date_agreed_in_map=1, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=5)
        assert score == 50.0

    def test_success_criteria_adds_20(self):
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=1,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=5)
        assert score == 50.0

    def test_legal_in_map_adds_10(self):
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=1, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=5)
        assert score == 40.0

    def test_technical_in_map_adds_10(self):
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=1,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=5)
        assert score == 40.0

    def test_exec_milestone_adds_10(self):
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=1, map_last_reviewed_days_ago=5)
        assert score == 40.0

    def test_all_positive_flags(self):
        # 30+20+20+10+10+10 = 100
        score = self._score(close_date_agreed_in_map=1, mutual_success_criteria_defined=1,
                            legal_milestone_in_map=1, technical_milestone_in_map=1,
                            executive_sign_off_milestone=1, map_last_reviewed_days_ago=5)
        assert score == 100.0

    def test_stale_review_21d_subtracts_15(self):
        # 30 - 15 = 15
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=21)
        assert score == 15.0

    def test_stale_review_exactly_21d(self):
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=21)
        assert score == 15.0

    def test_stale_review_14d_subtracts_7(self):
        # 30 - 7 = 23
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=14)
        assert score == 23.0

    def test_stale_review_exactly_14d(self):
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=14)
        assert score == 23.0

    def test_review_between_14_21_applies_7_penalty(self):
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=18)
        assert score == 23.0

    def test_review_less_than_14d_no_penalty(self):
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=13)
        assert score == 30.0

    def test_clamp_min_zero(self):
        score = self._score(close_date_agreed_in_map=0, mutual_success_criteria_defined=0,
                            legal_milestone_in_map=0, technical_milestone_in_map=0,
                            executive_sign_off_milestone=0, map_last_reviewed_days_ago=100)
        assert score >= 0.0

    def test_all_positive_with_stale_review(self):
        # 100 - 15 = 85
        score = self._score(close_date_agreed_in_map=1, mutual_success_criteria_defined=1,
                            legal_milestone_in_map=1, technical_milestone_in_map=1,
                            executive_sign_off_milestone=1, map_last_reviewed_days_ago=21)
        assert score == 85.0


# ===========================================================================
# 9. COMPOSITE SCORE
# ===========================================================================

class TestCompositeScore:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_weights_sum_to_1(self):
        # rep*0.25 + buyer*0.35 + milestone*0.25 + quality*0.15
        assert abs(0.25 + 0.35 + 0.25 + 0.15 - 1.0) < 1e-9

    def test_all_100_gives_100(self):
        assert self.scorer._composite(100, 100, 100, 100) == 100.0

    def test_all_0_gives_0(self):
        assert self.scorer._composite(0, 0, 0, 0) == 0.0

    def test_rep_weight_025(self):
        c = self.scorer._composite(100, 0, 0, 0)
        assert c == 25.0

    def test_buyer_weight_035(self):
        c = self.scorer._composite(0, 100, 0, 0)
        assert c == 35.0

    def test_milestone_weight_025(self):
        c = self.scorer._composite(0, 0, 100, 0)
        assert c == 25.0

    def test_quality_weight_015(self):
        c = self.scorer._composite(0, 0, 0, 100)
        assert c == 15.0

    def test_known_combination(self):
        # 80*0.25 + 70*0.35 + 60*0.25 + 50*0.15
        expected = round(80 * 0.25 + 70 * 0.35 + 60 * 0.25 + 50 * 0.15, 1)
        assert self.scorer._composite(80, 70, 60, 50) == expected

    def test_rounded_to_1_decimal(self):
        # 33.3 * 0.25 + 33.3 * 0.35 + 33.3 * 0.25 + 33.3 * 0.15
        c = self.scorer._composite(33.3, 33.3, 33.3, 33.3)
        assert c == round(33.3, 1)

    def test_clamp_max_100(self):
        c = self.scorer._composite(200, 200, 200, 200)
        assert c == 100.0

    def test_clamp_min_zero(self):
        c = self.scorer._composite(-50, -50, -50, -50)
        assert c == 0.0


# ===========================================================================
# 10. MAP HEALTH THRESHOLDS
# ===========================================================================

class TestMAPHealth:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_composite_65_is_on_track(self):
        assert self.scorer._map_health(65.0) == MAPHealth.ON_TRACK

    def test_composite_66_is_on_track(self):
        assert self.scorer._map_health(66.0) == MAPHealth.ON_TRACK

    def test_composite_100_is_on_track(self):
        assert self.scorer._map_health(100.0) == MAPHealth.ON_TRACK

    def test_composite_64_9_is_slipping(self):
        assert self.scorer._map_health(64.9) == MAPHealth.SLIPPING

    def test_composite_45_is_slipping(self):
        assert self.scorer._map_health(45.0) == MAPHealth.SLIPPING

    def test_composite_44_9_is_at_risk(self):
        assert self.scorer._map_health(44.9) == MAPHealth.AT_RISK

    def test_composite_25_is_at_risk(self):
        assert self.scorer._map_health(25.0) == MAPHealth.AT_RISK

    def test_composite_24_9_is_broken(self):
        assert self.scorer._map_health(24.9) == MAPHealth.BROKEN

    def test_composite_0_is_broken(self):
        assert self.scorer._map_health(0.0) == MAPHealth.BROKEN

    def test_boundary_65_exact(self):
        assert self.scorer._map_health(65.0) == MAPHealth.ON_TRACK

    def test_boundary_just_below_65(self):
        assert self.scorer._map_health(64.99) == MAPHealth.SLIPPING

    def test_boundary_45_exact(self):
        assert self.scorer._map_health(45.0) == MAPHealth.SLIPPING

    def test_boundary_just_below_45(self):
        assert self.scorer._map_health(44.99) == MAPHealth.AT_RISK

    def test_boundary_25_exact(self):
        assert self.scorer._map_health(25.0) == MAPHealth.AT_RISK

    def test_boundary_just_below_25(self):
        assert self.scorer._map_health(24.99) == MAPHealth.BROKEN


# ===========================================================================
# 11. ADHERENCE PATTERN PRIORITY
# ===========================================================================

class TestAdherencePattern:
    def setup_method(self):
        self.scorer = make_scorer()

    def _pattern(self, rep: float, buyer: float, buyer_missed: int = 0) -> AdherencePattern:
        inp = make_inp(buyer_milestones_missed=buyer_missed)
        return self.scorer._adherence_pattern(rep, buyer, inp)

    def test_buyer_ghosting_priority_over_others(self):
        # buyer_missed>=3 AND rep>=70 → BUYER_GHOSTING even if buyer<30
        p = self._pattern(rep=75, buyer=20, buyer_missed=3)
        assert p == AdherencePattern.BUYER_GHOSTING

    def test_buyer_ghosting_exact_boundary(self):
        p = self._pattern(rep=70, buyer=10, buyer_missed=3)
        assert p == AdherencePattern.BUYER_GHOSTING

    def test_buyer_ghosting_rep_below_70_no_trigger(self):
        # rep=69, buyer_missed=3 → falls through to next rule
        p = self._pattern(rep=69, buyer=20, buyer_missed=3)
        # rep<30? No. rep<40? No. buyer>=70? No. rep>=70? No. rep>=65? No → mutual_drift
        assert p == AdherencePattern.MUTUAL_DRIFT

    def test_buyer_ghosting_missed_2_no_trigger(self):
        p = self._pattern(rep=80, buyer=10, buyer_missed=2)
        assert p != AdherencePattern.BUYER_GHOSTING

    def test_complete_breakdown_priority_over_mutual_drift(self):
        # rep<30 and buyer<30 → COMPLETE_BREAKDOWN (not mutual_drift)
        p = self._pattern(rep=25, buyer=25, buyer_missed=0)
        assert p == AdherencePattern.COMPLETE_BREAKDOWN

    def test_complete_breakdown_boundary_29(self):
        p = self._pattern(rep=29, buyer=29, buyer_missed=0)
        assert p == AdherencePattern.COMPLETE_BREAKDOWN

    def test_mutual_drift_rep_and_buyer_under_40(self):
        # rep=35, buyer=35, both <40 but not both <30
        p = self._pattern(rep=35, buyer=35, buyer_missed=0)
        assert p == AdherencePattern.MUTUAL_DRIFT

    def test_mutual_drift_boundary_39(self):
        p = self._pattern(rep=39, buyer=39, buyer_missed=0)
        assert p == AdherencePattern.MUTUAL_DRIFT

    def test_buyer_leading_buyer_high_rep_low(self):
        # buyer>=70, rep<50
        p = self._pattern(rep=45, buyer=72, buyer_missed=0)
        assert p == AdherencePattern.BUYER_LEADING

    def test_buyer_leading_boundary(self):
        p = self._pattern(rep=49, buyer=70, buyer_missed=0)
        assert p == AdherencePattern.BUYER_LEADING

    def test_rep_only_rep_high_buyer_low(self):
        # rep>=70, buyer<50
        p = self._pattern(rep=75, buyer=45, buyer_missed=0)
        assert p == AdherencePattern.REP_ONLY

    def test_rep_only_boundary(self):
        p = self._pattern(rep=70, buyer=49, buyer_missed=0)
        assert p == AdherencePattern.REP_ONLY

    def test_both_committed(self):
        # rep>=65, buyer>=65
        p = self._pattern(rep=70, buyer=70, buyer_missed=0)
        assert p == AdherencePattern.BOTH_COMMITTED

    def test_both_committed_exact_boundary(self):
        p = self._pattern(rep=65, buyer=65, buyer_missed=0)
        assert p == AdherencePattern.BOTH_COMMITTED

    def test_default_mutual_drift(self):
        # rep=55, buyer=55 → doesn't match any earlier rule → MUTUAL_DRIFT
        p = self._pattern(rep=55, buyer=55, buyer_missed=0)
        assert p == AdherencePattern.MUTUAL_DRIFT

    def test_rep_only_not_triggered_when_buyer_50(self):
        # rep>=70 but buyer==50 (not <50)
        p = self._pattern(rep=75, buyer=50, buyer_missed=0)
        # buyer=50 is not <50; rep=75>=65, buyer=50 is not >=65 → mutual_drift
        assert p == AdherencePattern.MUTUAL_DRIFT

    def test_buyer_leading_not_triggered_when_rep_50(self):
        # buyer>=70 but rep==50 (not <50)
        p = self._pattern(rep=50, buyer=75, buyer_missed=0)
        # rep=50 is not <50; rep not >=70; rep>=65? No → mutual_drift
        assert p == AdherencePattern.MUTUAL_DRIFT


# ===========================================================================
# 12. COMMITMENT SIGNAL
# ===========================================================================

class TestCommitmentSignal:
    def setup_method(self):
        self.scorer = make_scorer()

    def _signal(self, buyer: float, composite: float, shared: int = 0) -> CommitmentSignal:
        inp = make_inp(buyer_shared_map_internally=shared)
        return self.scorer._commitment_signal(buyer, composite, inp)

    def test_strong_buyer_70_shared(self):
        assert self._signal(buyer=70, composite=50, shared=1) == CommitmentSignal.STRONG

    def test_strong_buyer_80_shared(self):
        assert self._signal(buyer=80, composite=60, shared=1) == CommitmentSignal.STRONG

    def test_strong_requires_buyer_ge_70(self):
        # buyer=69, shared=1 → falls through
        s = self._signal(buyer=69, composite=70, shared=1)
        assert s != CommitmentSignal.STRONG

    def test_strong_requires_shared(self):
        # buyer=70, shared=0 → falls through to moderate or weak
        s = self._signal(buyer=70, composite=60, shared=0)
        assert s != CommitmentSignal.STRONG

    def test_moderate_buyer_55_composite_55(self):
        assert self._signal(buyer=55, composite=55, shared=0) == CommitmentSignal.MODERATE

    def test_moderate_buyer_60_composite_60(self):
        assert self._signal(buyer=60, composite=60, shared=0) == CommitmentSignal.MODERATE

    def test_moderate_requires_both_thresholds(self):
        # buyer=55 but composite<55
        s = self._signal(buyer=55, composite=54, shared=0)
        assert s == CommitmentSignal.WEAK

    def test_moderate_buyer_below_55(self):
        s = self._signal(buyer=54, composite=60, shared=0)
        # buyer<55 → not moderate; buyer>=40 → weak
        assert s == CommitmentSignal.WEAK

    def test_weak_buyer_40(self):
        assert self._signal(buyer=40, composite=30, shared=0) == CommitmentSignal.WEAK

    def test_weak_buyer_50(self):
        assert self._signal(buyer=50, composite=40, shared=0) == CommitmentSignal.WEAK

    def test_absent_buyer_below_40(self):
        assert self._signal(buyer=39, composite=30, shared=0) == CommitmentSignal.ABSENT

    def test_absent_buyer_0(self):
        assert self._signal(buyer=0, composite=0, shared=0) == CommitmentSignal.ABSENT

    def test_buyer_70_shared_overrides_moderate(self):
        # buyer=70, composite=70, shared=1 → STRONG (first match)
        s = self._signal(buyer=70, composite=70, shared=1)
        assert s == CommitmentSignal.STRONG

    def test_weak_boundary_exact_40(self):
        s = self._signal(buyer=40, composite=20, shared=0)
        assert s == CommitmentSignal.WEAK


# ===========================================================================
# 13. IS_HEALTHY_MAP AND NEEDS_MAP_RESET
# ===========================================================================

class TestIsHealthyAndNeedsReset:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_is_healthy_when_composite_ge_65(self):
        # Build scenario where composite >= 65
        inp = make_inp(
            rep_milestones_completed=5, rep_milestones_missed=0,
            buyer_milestones_completed=5, buyer_milestones_missed=0,
            buyer_shared_map_internally=1,
            buyer_response_time_avg_hours=2,
            map_last_reviewed_days_ago=5,
            close_date_agreed_in_map=1,
            mutual_success_criteria_defined=1,
            legal_milestone_in_map=1, legal_milestone_completed=1,
            close_date_changes_since_map=0,
            total_milestones=10,
        )
        result = self.scorer.score(inp)
        assert result.is_healthy_map == (result.map_adherence_composite >= 65.0)

    def test_not_healthy_when_composite_below_65(self):
        inp = make_inp(
            rep_milestones_completed=0, rep_milestones_missed=5,
            buyer_milestones_completed=0, buyer_milestones_missed=5,
            buyer_shared_map_internally=0,
            buyer_response_time_avg_hours=72,
            map_last_reviewed_days_ago=45,
            close_date_agreed_in_map=0,
            mutual_success_criteria_defined=0,
            close_date_changes_since_map=3,
            total_milestones=10,
        )
        result = self.scorer.score(inp)
        assert result.is_healthy_map == (result.map_adherence_composite >= 65.0)

    def test_needs_reset_when_composite_below_35(self):
        # Ensure composite < 35
        inp = make_inp(
            rep_milestones_completed=0, rep_milestones_missed=5,
            buyer_milestones_completed=0, buyer_milestones_missed=1,
            buyer_shared_map_internally=0,
            buyer_response_time_avg_hours=72,
            map_last_reviewed_days_ago=60,
            close_date_agreed_in_map=0,
            mutual_success_criteria_defined=0,
            close_date_changes_since_map=3,
            total_milestones=10,
        )
        result = self.scorer.score(inp)
        assert result.needs_map_reset == (result.map_adherence_composite < 35.0 or
                                          inp.buyer_milestones_missed >= 3)

    def test_needs_reset_when_buyer_missed_ge_3(self):
        # Even if composite is decent, buyer_missed>=3 triggers reset
        inp = make_inp(
            buyer_milestones_missed=3,
            buyer_milestones_completed=5,
            rep_milestones_completed=5, rep_milestones_missed=0,
        )
        result = self.scorer.score(inp)
        assert result.needs_map_reset is True

    def test_needs_reset_exact_boundary_buyer_missed_3(self):
        inp = make_inp(buyer_milestones_missed=3)
        result = self.scorer.score(inp)
        assert result.needs_map_reset is True

    def test_no_reset_when_buyer_missed_2_and_composite_ok(self):
        inp = make_inp(
            buyer_milestones_missed=2,
            buyer_milestones_completed=5,
            rep_milestones_completed=5, rep_milestones_missed=0,
            buyer_shared_map_internally=1,
            close_date_agreed_in_map=1,
            mutual_success_criteria_defined=1,
            map_last_reviewed_days_ago=5,
        )
        result = self.scorer.score(inp)
        # Only reset if composite<35 OR buyer_missed>=3
        assert result.needs_map_reset == (result.map_adherence_composite < 35.0 or
                                          inp.buyer_milestones_missed >= 3)

    def test_is_healthy_composite_exactly_65(self):
        # We test the boundary via direct scorer logic
        scorer = make_scorer()
        # Construct inputs that give composite ~65; check is_healthy
        # With known scores: verify is_healthy matches composite>=65
        for trial_inp in [make_inp(), make_inp(rep_milestones_completed=2, rep_milestones_missed=0)]:
            r = scorer.score(trial_inp)
            assert r.is_healthy_map == (r.map_adherence_composite >= 65.0)


# ===========================================================================
# 14. ESTIMATED CLOSE CONFIDENCE
# ===========================================================================

class TestEstimatedCloseConfidence:
    def setup_method(self):
        self.scorer = make_scorer()

    def _confidence(self, composite: float, **kwargs) -> float:
        inp = make_inp(**kwargs)
        return self.scorer._estimated_close_confidence(inp, composite)

    def test_base_equals_composite(self):
        c = self._confidence(composite=50, close_date_agreed_in_map=0,
                             buyer_shared_map_internally=0, mutual_success_criteria_defined=0,
                             close_date_changes_since_map=0)
        assert c == 50.0

    def test_close_date_agreed_adds_10(self):
        c = self._confidence(composite=50, close_date_agreed_in_map=1,
                             buyer_shared_map_internally=0, mutual_success_criteria_defined=0,
                             close_date_changes_since_map=0)
        assert c == 60.0

    def test_shared_internally_adds_12(self):
        c = self._confidence(composite=50, close_date_agreed_in_map=0,
                             buyer_shared_map_internally=1, mutual_success_criteria_defined=0,
                             close_date_changes_since_map=0)
        assert c == 62.0

    def test_success_criteria_adds_8(self):
        c = self._confidence(composite=50, close_date_agreed_in_map=0,
                             buyer_shared_map_internally=0, mutual_success_criteria_defined=1,
                             close_date_changes_since_map=0)
        assert c == 58.0

    def test_close_date_change_1_subtracts_8(self):
        c = self._confidence(composite=50, close_date_agreed_in_map=0,
                             buyer_shared_map_internally=0, mutual_success_criteria_defined=0,
                             close_date_changes_since_map=1)
        assert c == 42.0

    def test_close_date_changes_2_subtracts_16(self):
        c = self._confidence(composite=50, close_date_agreed_in_map=0,
                             buyer_shared_map_internally=0, mutual_success_criteria_defined=0,
                             close_date_changes_since_map=2)
        assert c == 34.0

    def test_all_bonuses(self):
        # 50 + 10 + 12 + 8 = 80
        c = self._confidence(composite=50, close_date_agreed_in_map=1,
                             buyer_shared_map_internally=1, mutual_success_criteria_defined=1,
                             close_date_changes_since_map=0)
        assert c == 80.0

    def test_clamp_max_100(self):
        c = self._confidence(composite=90, close_date_agreed_in_map=1,
                             buyer_shared_map_internally=1, mutual_success_criteria_defined=1,
                             close_date_changes_since_map=0)
        assert c == 100.0

    def test_clamp_min_zero(self):
        c = self._confidence(composite=0, close_date_agreed_in_map=0,
                             buyer_shared_map_internally=0, mutual_success_criteria_defined=0,
                             close_date_changes_since_map=10)
        assert c == 0.0

    def test_all_bonuses_and_changes_penalty(self):
        # 50 + 10 + 12 + 8 = 80; -2*8 = 16; 80-16=64
        c = self._confidence(composite=50, close_date_agreed_in_map=1,
                             buyer_shared_map_internally=1, mutual_success_criteria_defined=1,
                             close_date_changes_since_map=2)
        assert c == 64.0

    def test_result_rounded_to_1_decimal(self):
        c = self._confidence(composite=33.3, close_date_agreed_in_map=0,
                             buyer_shared_map_internally=0, mutual_success_criteria_defined=0,
                             close_date_changes_since_map=0)
        assert c == 33.3


# ===========================================================================
# 15. DAYS TO CLOSE RISK
# ===========================================================================

class TestDaysToCloseRisk:
    def setup_method(self):
        self.scorer = make_scorer()

    def _risk(self, composite: float, changes: int) -> int:
        inp = make_inp(close_date_changes_since_map=changes)
        return self.scorer._days_to_close_risk(inp, composite)

    def test_composite_75_returns_0(self):
        assert self._risk(75.0, 5) == 0

    def test_composite_80_returns_0(self):
        assert self._risk(80.0, 3) == 0

    def test_composite_100_returns_0(self):
        assert self._risk(100.0, 10) == 0

    def test_composite_74_9_uses_changes_times_14(self):
        assert self._risk(74.9, 2) == 2 * 14

    def test_composite_55_uses_changes_times_14(self):
        assert self._risk(55.0, 3) == 3 * 14

    def test_composite_60_uses_changes_times_14(self):
        assert self._risk(60.0, 1) == 1 * 14

    def test_composite_54_9_uses_changes_times_21_plus_14(self):
        assert self._risk(54.9, 2) == 2 * 21 + 14

    def test_composite_35_uses_changes_times_21_plus_14(self):
        assert self._risk(35.0, 1) == 1 * 21 + 14

    def test_composite_34_9_uses_changes_times_30_plus_30(self):
        assert self._risk(34.9, 2) == 2 * 30 + 30

    def test_composite_0_uses_changes_times_30_plus_30(self):
        assert self._risk(0.0, 1) == 1 * 30 + 30

    def test_zero_changes_composite_55(self):
        assert self._risk(55.0, 0) == 0

    def test_zero_changes_composite_35(self):
        assert self._risk(35.0, 0) == 14

    def test_zero_changes_composite_10(self):
        assert self._risk(10.0, 0) == 30

    def test_composite_boundary_75_exact(self):
        assert self._risk(75.0, 3) == 0

    def test_composite_boundary_just_below_75(self):
        assert self._risk(74.99, 2) == 2 * 14

    def test_composite_boundary_55_exact(self):
        assert self._risk(55.0, 2) == 2 * 14

    def test_composite_boundary_just_below_55(self):
        assert self._risk(54.99, 2) == 2 * 21 + 14

    def test_composite_boundary_35_exact(self):
        assert self._risk(35.0, 2) == 2 * 21 + 14

    def test_composite_boundary_just_below_35(self):
        assert self._risk(34.99, 2) == 2 * 30 + 30


# ===========================================================================
# 16. MAP ACTION LOGIC
# ===========================================================================

class TestMAPAction:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_escalate_when_broken_no_reset(self):
        action = self.scorer._map_action(MAPHealth.BROKEN, False, 10.0)
        assert action == MAPAction.ESCALATE

    def test_escalate_when_needs_reset(self):
        action = self.scorer._map_action(MAPHealth.ON_TRACK, True, 70.0)
        assert action == MAPAction.ESCALATE

    def test_escalate_when_broken_and_needs_reset(self):
        action = self.scorer._map_action(MAPHealth.BROKEN, True, 10.0)
        assert action == MAPAction.ESCALATE

    def test_reset_map_when_at_risk_no_reset(self):
        action = self.scorer._map_action(MAPHealth.AT_RISK, False, 30.0)
        assert action == MAPAction.RESET_MAP

    def test_reaffirm_when_slipping_no_reset(self):
        action = self.scorer._map_action(MAPHealth.SLIPPING, False, 50.0)
        assert action == MAPAction.REAFFIRM

    def test_accelerate_when_on_track_no_reset(self):
        action = self.scorer._map_action(MAPHealth.ON_TRACK, False, 70.0)
        assert action == MAPAction.ACCELERATE

    def test_needs_reset_overrides_on_track(self):
        # on_track but needs_reset → escalate
        action = self.scorer._map_action(MAPHealth.ON_TRACK, True, 70.0)
        assert action == MAPAction.ESCALATE

    def test_needs_reset_overrides_slipping(self):
        action = self.scorer._map_action(MAPHealth.SLIPPING, True, 50.0)
        assert action == MAPAction.ESCALATE

    def test_needs_reset_overrides_at_risk(self):
        action = self.scorer._map_action(MAPHealth.AT_RISK, True, 30.0)
        assert action == MAPAction.ESCALATE


# ===========================================================================
# 17. SCORE METHOD (END-TO-END)
# ===========================================================================

class TestScoreMethod:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_returns_map_adherence_result(self):
        result = self.scorer.score(make_inp())
        assert isinstance(result, MAPAdherenceResult)

    def test_result_stored_in_results(self):
        result = self.scorer.score(make_inp())
        assert result in self.scorer._results

    def test_multiple_scores_accumulate(self):
        self.scorer.score(make_inp(deal_id="d1"))
        self.scorer.score(make_inp(deal_id="d2"))
        assert len(self.scorer._results) == 2

    def test_deal_id_preserved(self):
        result = self.scorer.score(make_inp(deal_id="my-deal-42"))
        assert result.deal_id == "my-deal-42"

    def test_deal_name_preserved(self):
        result = self.scorer.score(make_inp(deal_name="BigCorp 2025"))
        assert result.deal_name == "BigCorp 2025"

    def test_scores_in_range_0_100(self):
        result = self.scorer.score(make_inp())
        assert 0 <= result.rep_adherence_score <= 100
        assert 0 <= result.buyer_adherence_score <= 100
        assert 0 <= result.milestone_progress_score <= 100
        assert 0 <= result.map_quality_score <= 100
        assert 0 <= result.map_adherence_composite <= 100
        assert 0 <= result.estimated_close_confidence <= 100

    def test_days_to_close_risk_non_negative(self):
        result = self.scorer.score(make_inp())
        assert result.days_to_close_risk >= 0

    def test_map_health_is_enum(self):
        result = self.scorer.score(make_inp())
        assert isinstance(result.map_health, MAPHealth)

    def test_adherence_pattern_is_enum(self):
        result = self.scorer.score(make_inp())
        assert isinstance(result.adherence_pattern, AdherencePattern)

    def test_commitment_signal_is_enum(self):
        result = self.scorer.score(make_inp())
        assert isinstance(result.commitment_signal, CommitmentSignal)

    def test_map_action_is_enum(self):
        result = self.scorer.score(make_inp())
        assert isinstance(result.map_action, MAPAction)

    def test_is_healthy_consistent_with_composite(self):
        result = self.scorer.score(make_inp())
        assert result.is_healthy_map == (result.map_adherence_composite >= 65.0)

    def test_needs_reset_consistent_with_composite_and_buyer_missed(self):
        inp = make_inp()
        result = self.scorer.score(inp)
        expected = result.map_adherence_composite < 35.0 or inp.buyer_milestones_missed >= 3
        assert result.needs_map_reset == expected


# ===========================================================================
# 18. SCORE_BATCH METHOD
# ===========================================================================

class TestScoreBatch:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_returns_list(self):
        results = self.scorer.score_batch([make_inp()])
        assert isinstance(results, list)

    def test_empty_batch(self):
        results = self.scorer.score_batch([])
        assert results == []

    def test_batch_length_matches_input(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(5)]
        results = self.scorer.score_batch(inputs)
        assert len(results) == 5

    def test_batch_accumulates_in_results(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(3)]
        self.scorer.score_batch(inputs)
        assert len(self.scorer._results) == 3

    def test_batch_results_match_individual(self):
        inp1 = make_inp(deal_id="d1")
        inp2 = make_inp(deal_id="d2")
        scorer_individual = make_scorer()
        r1 = scorer_individual.score(inp1)
        r2 = scorer_individual.score(inp2)

        scorer_batch = make_scorer()
        batch = scorer_batch.score_batch([inp1, inp2])

        assert batch[0].map_adherence_composite == r1.map_adherence_composite
        assert batch[1].map_adherence_composite == r2.map_adherence_composite

    def test_batch_preserves_order(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(4)]
        results = self.scorer.score_batch(inputs)
        for i, r in enumerate(results):
            assert r.deal_id == f"d{i}"


# ===========================================================================
# 19. RESET METHOD
# ===========================================================================

class TestResetMethod:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_reset_clears_results(self):
        self.scorer.score(make_inp())
        self.scorer.score(make_inp())
        self.scorer.reset()
        assert self.scorer._results == []

    def test_reset_empty_scorer_no_error(self):
        self.scorer.reset()  # no error
        assert self.scorer._results == []

    def test_reset_allows_fresh_scoring(self):
        self.scorer.score(make_inp(deal_id="d1"))
        self.scorer.reset()
        self.scorer.score(make_inp(deal_id="d2"))
        assert len(self.scorer._results) == 1
        assert self.scorer._results[0].deal_id == "d2"

    def test_reset_resets_summary(self):
        self.scorer.score(make_inp())
        self.scorer.reset()
        s = self.scorer.summary()
        assert s["total"] == 0


# ===========================================================================
# 20. PROPERTIES
# ===========================================================================

class TestProperties:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_healthy_maps_empty_initially(self):
        assert self.scorer.healthy_maps == []

    def test_maps_needing_reset_empty_initially(self):
        assert self.scorer.maps_needing_reset == []

    def test_avg_close_confidence_zero_when_empty(self):
        assert self.scorer.avg_close_confidence == 0.0

    def test_avg_map_adherence_composite_zero_when_empty(self):
        assert self.scorer.avg_map_adherence_composite == 0.0

    def test_healthy_maps_filters_correctly(self):
        # Ensure a healthy deal
        healthy_inp = make_inp(
            rep_milestones_completed=5, rep_milestones_missed=0,
            buyer_milestones_completed=5, buyer_milestones_missed=0,
            buyer_shared_map_internally=1, buyer_response_time_avg_hours=2,
            map_last_reviewed_days_ago=5, close_date_agreed_in_map=1,
            mutual_success_criteria_defined=1, legal_milestone_in_map=1,
            legal_milestone_completed=1, total_milestones=10,
            close_date_changes_since_map=0,
        )
        unhealthy_inp = make_inp(
            rep_milestones_completed=0, rep_milestones_missed=5,
            buyer_milestones_completed=0, buyer_milestones_missed=1,
            buyer_shared_map_internally=0, buyer_response_time_avg_hours=72,
            map_last_reviewed_days_ago=60, close_date_agreed_in_map=0,
            mutual_success_criteria_defined=0, total_milestones=10,
            close_date_changes_since_map=3,
        )
        self.scorer.score(healthy_inp)
        self.scorer.score(unhealthy_inp)
        healthy = self.scorer.healthy_maps
        for r in healthy:
            assert r.is_healthy_map is True

    def test_maps_needing_reset_filters_correctly(self):
        reset_inp = make_inp(buyer_milestones_missed=3)
        no_reset_inp = make_inp(
            buyer_milestones_missed=0,
            rep_milestones_completed=5, rep_milestones_missed=0,
            buyer_milestones_completed=5,
            buyer_shared_map_internally=1,
            close_date_agreed_in_map=1,
            mutual_success_criteria_defined=1,
            map_last_reviewed_days_ago=5,
        )
        self.scorer.score(reset_inp)
        self.scorer.score(no_reset_inp)
        needing_reset = self.scorer.maps_needing_reset
        for r in needing_reset:
            assert r.needs_map_reset is True

    def test_avg_close_confidence_single(self):
        result = self.scorer.score(make_inp())
        assert self.scorer.avg_close_confidence == round(result.estimated_close_confidence, 1)

    def test_avg_map_adherence_composite_single(self):
        result = self.scorer.score(make_inp())
        assert self.scorer.avg_map_adherence_composite == round(result.map_adherence_composite, 1)

    def test_avg_close_confidence_multiple(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(4)])
        expected = round(
            sum(r.estimated_close_confidence for r in self.scorer._results) / 4, 1
        )
        assert self.scorer.avg_close_confidence == expected

    def test_avg_composite_multiple(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(4)])
        expected = round(
            sum(r.map_adherence_composite for r in self.scorer._results) / 4, 1
        )
        assert self.scorer.avg_map_adherence_composite == expected

    def test_avg_rounded_to_1_decimal(self):
        self.scorer.score(make_inp(deal_id="d1"))
        self.scorer.score(make_inp(deal_id="d2"))
        assert isinstance(self.scorer.avg_close_confidence, float)
        # Check it is rounded to 1 decimal
        val = self.scorer.avg_close_confidence
        assert val == round(val, 1)


# ===========================================================================
# 21. SUMMARY CONTENT
# ===========================================================================

class TestSummaryContent:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_summary_total_count(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(5)])
        assert self.scorer.summary()["total"] == 5

    def test_summary_health_counts_all_values_sum_to_total(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(4)])
        s = self.scorer.summary()
        assert sum(s["health_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_to_total(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(4)])
        s = self.scorer.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_signal_counts_sum_to_total(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(4)])
        s = self.scorer.summary()
        assert sum(s["signal_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(4)])
        s = self.scorer.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_matches_manual(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(3)]
        self.scorer.score_batch(inputs)
        s = self.scorer.summary()
        manual = round(
            sum(r.map_adherence_composite for r in self.scorer._results) / 3, 1
        )
        assert s["avg_map_adherence_composite"] == manual

    def test_summary_avg_confidence_matches_manual(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(3)]
        self.scorer.score_batch(inputs)
        s = self.scorer.summary()
        manual = round(
            sum(r.estimated_close_confidence for r in self.scorer._results) / 3, 1
        )
        assert s["avg_close_confidence"] == manual

    def test_summary_healthy_map_count(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(4)])
        s = self.scorer.summary()
        assert s["healthy_map_count"] == len(self.scorer.healthy_maps)

    def test_summary_reset_needed_count(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(4)])
        s = self.scorer.summary()
        assert s["reset_needed_count"] == len(self.scorer.maps_needing_reset)

    def test_summary_avg_rep_adherence(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(3)]
        self.scorer.score_batch(inputs)
        s = self.scorer.summary()
        manual = round(
            sum(r.rep_adherence_score for r in self.scorer._results) / 3, 1
        )
        assert s["avg_rep_adherence_score"] == manual

    def test_summary_avg_buyer_adherence(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(3)]
        self.scorer.score_batch(inputs)
        s = self.scorer.summary()
        manual = round(
            sum(r.buyer_adherence_score for r in self.scorer._results) / 3, 1
        )
        assert s["avg_buyer_adherence_score"] == manual

    def test_summary_avg_milestone_progress(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(3)]
        self.scorer.score_batch(inputs)
        s = self.scorer.summary()
        manual = round(
            sum(r.milestone_progress_score for r in self.scorer._results) / 3, 1
        )
        assert s["avg_milestone_progress_score"] == manual

    def test_summary_avg_map_quality(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(3)]
        self.scorer.score_batch(inputs)
        s = self.scorer.summary()
        manual = round(
            sum(r.map_quality_score for r in self.scorer._results) / 3, 1
        )
        assert s["avg_map_quality_score"] == manual

    def test_summary_health_counts_keys_are_valid_health_values(self):
        self.scorer.score(make_inp())
        s = self.scorer.summary()
        valid = {h.value for h in MAPHealth}
        for k in s["health_counts"]:
            assert k in valid

    def test_summary_pattern_counts_keys_are_valid_pattern_values(self):
        self.scorer.score(make_inp())
        s = self.scorer.summary()
        valid = {p.value for p in AdherencePattern}
        for k in s["pattern_counts"]:
            assert k in valid

    def test_summary_signal_counts_keys_are_valid(self):
        self.scorer.score(make_inp())
        s = self.scorer.summary()
        valid = {sig.value for sig in CommitmentSignal}
        for k in s["signal_counts"]:
            assert k in valid

    def test_summary_action_counts_keys_are_valid(self):
        self.scorer.score(make_inp())
        s = self.scorer.summary()
        valid = {a.value for a in MAPAction}
        for k in s["action_counts"]:
            assert k in valid

    def test_summary_reflects_reset(self):
        self.scorer.score(make_inp())
        self.scorer.reset()
        s = self.scorer.summary()
        assert s["total"] == 0


# ===========================================================================
# 22. END-TO-END SCENARIOS
# ===========================================================================

class TestEndToEndScenarios:
    def setup_method(self):
        self.scorer = make_scorer()

    def _perfect_map_input(self) -> MutualActionPlanInput:
        """Perfect MAP: both sides fully engaged, all milestones done, quality MAP."""
        return make_inp(
            rep_milestones_completed=5,
            rep_milestones_missed=0,
            buyer_milestones_completed=5,
            buyer_milestones_missed=0,
            buyer_shared_map_internally=1,
            buyer_response_time_avg_hours=2.0,
            map_last_reviewed_days_ago=3,
            close_date_agreed_in_map=1,
            close_date_changes_since_map=0,
            mutual_success_criteria_defined=1,
            legal_milestone_in_map=1,
            legal_milestone_completed=1,
            technical_milestone_in_map=1,
            technical_milestone_completed=1,
            executive_sign_off_milestone=1,
            executive_sign_off_done=1,
            total_milestones=10,
            deal_value=200_000.0,
        )

    def _breakdown_input(self) -> MutualActionPlanInput:
        """Complete breakdown: nobody doing anything."""
        return make_inp(
            rep_milestones_completed=0,
            rep_milestones_missed=5,
            buyer_milestones_completed=0,
            buyer_milestones_missed=5,
            buyer_shared_map_internally=0,
            buyer_response_time_avg_hours=96.0,
            map_last_reviewed_days_ago=60,
            close_date_agreed_in_map=0,
            close_date_changes_since_map=3,
            mutual_success_criteria_defined=0,
            legal_milestone_in_map=0,
            technical_milestone_in_map=0,
            executive_sign_off_milestone=0,
            total_milestones=10,
            deal_value=50_000.0,
        )

    def _buyer_ghosting_input(self) -> MutualActionPlanInput:
        """Buyer ghosting: rep high, buyer missed many."""
        return make_inp(
            rep_milestones_completed=5,
            rep_milestones_missed=0,
            buyer_milestones_completed=0,
            buyer_milestones_missed=4,
            buyer_shared_map_internally=0,
            buyer_response_time_avg_hours=72.0,
            map_last_reviewed_days_ago=30,
            close_date_agreed_in_map=1,
            close_date_changes_since_map=2,
            mutual_success_criteria_defined=0,
            total_milestones=10,
            deal_value=100_000.0,
        )

    def _rep_only_input(self) -> MutualActionPlanInput:
        """Rep-only effort: rep doing well, buyer not engaged."""
        return make_inp(
            rep_milestones_completed=5,
            rep_milestones_missed=0,
            buyer_milestones_completed=0,
            buyer_milestones_missed=2,
            buyer_shared_map_internally=0,
            buyer_response_time_avg_hours=36.0,
            map_last_reviewed_days_ago=10,
            close_date_agreed_in_map=1,
            close_date_changes_since_map=1,
            mutual_success_criteria_defined=1,
            total_milestones=10,
            deal_value=75_000.0,
        )

    # Perfect MAP
    def test_perfect_map_is_on_track(self):
        result = self.scorer.score(self._perfect_map_input())
        assert result.map_health == MAPHealth.ON_TRACK

    def test_perfect_map_is_healthy(self):
        result = self.scorer.score(self._perfect_map_input())
        assert result.is_healthy_map is True

    def test_perfect_map_both_committed(self):
        result = self.scorer.score(self._perfect_map_input())
        assert result.adherence_pattern == AdherencePattern.BOTH_COMMITTED

    def test_perfect_map_strong_signal(self):
        result = self.scorer.score(self._perfect_map_input())
        assert result.commitment_signal == CommitmentSignal.STRONG

    def test_perfect_map_accelerate_action(self):
        result = self.scorer.score(self._perfect_map_input())
        assert result.map_action == MAPAction.ACCELERATE

    def test_perfect_map_high_composite(self):
        result = self.scorer.score(self._perfect_map_input())
        assert result.map_adherence_composite >= 65.0

    def test_perfect_map_no_reset_needed(self):
        result = self.scorer.score(self._perfect_map_input())
        assert result.needs_map_reset is False

    # Complete breakdown
    def test_breakdown_is_broken_health(self):
        result = self.scorer.score(self._breakdown_input())
        assert result.map_health == MAPHealth.BROKEN

    def test_breakdown_complete_breakdown_pattern(self):
        result = self.scorer.score(self._breakdown_input())
        assert result.adherence_pattern == AdherencePattern.COMPLETE_BREAKDOWN

    def test_breakdown_absent_signal(self):
        result = self.scorer.score(self._breakdown_input())
        assert result.commitment_signal == CommitmentSignal.ABSENT

    def test_breakdown_escalate_action(self):
        result = self.scorer.score(self._breakdown_input())
        assert result.map_action == MAPAction.ESCALATE

    def test_breakdown_needs_reset(self):
        result = self.scorer.score(self._breakdown_input())
        assert result.needs_map_reset is True

    def test_breakdown_not_healthy(self):
        result = self.scorer.score(self._breakdown_input())
        assert result.is_healthy_map is False

    # Buyer ghosting
    def test_buyer_ghosting_pattern(self):
        result = self.scorer.score(self._buyer_ghosting_input())
        assert result.adherence_pattern == AdherencePattern.BUYER_GHOSTING

    def test_buyer_ghosting_needs_reset(self):
        result = self.scorer.score(self._buyer_ghosting_input())
        assert result.needs_map_reset is True

    def test_buyer_ghosting_escalate(self):
        result = self.scorer.score(self._buyer_ghosting_input())
        assert result.map_action == MAPAction.ESCALATE

    # Rep-only effort
    def test_rep_only_pattern(self):
        result = self.scorer.score(self._rep_only_input())
        # rep score will be high (missed=0, completed=5) → >=70; buyer score will be low
        assert result.adherence_pattern in (
            AdherencePattern.REP_ONLY, AdherencePattern.BUYER_GHOSTING,
            AdherencePattern.MUTUAL_DRIFT
        )

    def test_rep_only_rep_adherence_higher_than_buyer(self):
        result = self.scorer.score(self._rep_only_input())
        assert result.rep_adherence_score > result.buyer_adherence_score


# ===========================================================================
# 23. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_zero_total_milestones(self):
        inp = make_inp(total_milestones=0,
                       rep_milestones_completed=0, rep_milestones_missed=0,
                       buyer_milestones_completed=0, buyer_milestones_missed=0)
        result = self.scorer.score(inp)
        assert result.milestone_progress_score == 20.0

    def test_zero_rep_and_buyer_milestones_no_data(self):
        inp = make_inp(
            rep_milestones_completed=0, rep_milestones_missed=0,
            buyer_milestones_completed=0, buyer_milestones_missed=0,
            total_milestones=0,
        )
        result = self.scorer.score(inp)
        assert result.rep_adherence_score == 50.0
        assert result.buyer_adherence_score == 40.0

    def test_very_high_deal_value_has_no_effect_on_scores(self):
        inp_low = make_inp(deal_value=1_000.0)
        inp_high = make_inp(deal_value=10_000_000.0)
        r_low = self.scorer.score(inp_low)
        scorer2 = make_scorer()
        r_high = scorer2.score(inp_high)
        assert r_low.map_adherence_composite == r_high.map_adherence_composite

    def test_many_close_date_changes_caps_milestone_penalty(self):
        # 10 changes → 10*7=70 → capped at 20; milestone score can't go below 0
        result = self.scorer.score(make_inp(close_date_changes_since_map=10))
        assert result.milestone_progress_score >= 0.0

    def test_buyer_response_time_exactly_4h(self):
        score = self.scorer._buyer_adherence_score(
            make_inp(buyer_milestones_completed=1, buyer_milestones_missed=0,
                     buyer_shared_map_internally=0, buyer_response_time_avg_hours=4.0)
        )
        assert score == min(100.0, 70.0 + 10.0)

    def test_buyer_response_time_exactly_24h(self):
        score = self.scorer._buyer_adherence_score(
            make_inp(buyer_milestones_completed=1, buyer_milestones_missed=0,
                     buyer_shared_map_internally=0, buyer_response_time_avg_hours=24.0)
        )
        assert score == 70.0 - 8.0

    def test_buyer_response_time_exactly_48h(self):
        score = self.scorer._buyer_adherence_score(
            make_inp(buyer_milestones_completed=1, buyer_milestones_missed=0,
                     buyer_shared_map_internally=0, buyer_response_time_avg_hours=48.0)
        )
        assert score == 70.0 - 15.0

    def test_no_critical_milestones_at_all(self):
        inp = make_inp(
            legal_milestone_in_map=0, technical_milestone_in_map=0,
            executive_sign_off_milestone=0,
        )
        result = self.scorer.score(inp)
        assert isinstance(result, MAPAdherenceResult)

    def test_all_milestones_in_map_all_done(self):
        inp = make_inp(
            legal_milestone_in_map=1, legal_milestone_completed=1,
            technical_milestone_in_map=1, technical_milestone_completed=1,
            executive_sign_off_milestone=1, executive_sign_off_done=1,
        )
        result = self.scorer.score(inp)
        assert result.milestone_progress_score <= 100.0

    def test_scorer_state_independent_between_instances(self):
        s1 = make_scorer()
        s2 = make_scorer()
        s1.score(make_inp(deal_id="s1-d1"))
        assert len(s2._results) == 0

    def test_score_does_not_modify_input(self):
        inp = make_inp()
        original_buyer_missed = inp.buyer_milestones_missed
        self.scorer.score(inp)
        assert inp.buyer_milestones_missed == original_buyer_missed

    def test_score_with_zero_deal_value(self):
        inp = make_inp(deal_value=0.0)
        result = self.scorer.score(inp)
        assert isinstance(result, MAPAdherenceResult)

    def test_single_milestone_total(self):
        inp = make_inp(total_milestones=1, rep_milestones_completed=1,
                       buyer_milestones_completed=0)
        result = self.scorer.score(inp)
        assert result.milestone_progress_score >= 0.0

    def test_close_date_changes_zero(self):
        result = self.scorer.score(make_inp(close_date_changes_since_map=0))
        assert result.days_to_close_risk >= 0

    def test_no_close_date_agreed(self):
        result = self.scorer.score(make_inp(close_date_agreed_in_map=0))
        assert isinstance(result, MAPAdherenceResult)

    def test_map_reviewed_very_recently(self):
        result = self.scorer.score(make_inp(map_last_reviewed_days_ago=0))
        assert result.rep_adherence_score >= 0


# ===========================================================================
# 24. CROSS-VALIDATION TESTS
# ===========================================================================

class TestCrossValidation:
    def setup_method(self):
        self.scorer = make_scorer()

    def test_composite_matches_manual_calculation(self):
        """Score manually and verify composite formula."""
        inp = make_inp(
            rep_milestones_completed=3, rep_milestones_missed=1,
            buyer_milestones_completed=3, buyer_milestones_missed=1,
            buyer_shared_map_internally=0,
            buyer_response_time_avg_hours=12.0,
            map_last_reviewed_days_ago=10,
            close_date_agreed_in_map=1,
            close_date_changes_since_map=0,
            mutual_success_criteria_defined=1,
            legal_milestone_in_map=0,
            technical_milestone_in_map=0,
            executive_sign_off_milestone=0,
            total_milestones=10,
        )
        result = self.scorer.score(inp)

        rep = self.scorer._rep_adherence_score(inp)
        buyer = self.scorer._buyer_adherence_score(inp)
        milestone = self.scorer._milestone_progress_score(inp)
        quality = self.scorer._map_quality_score(inp)
        composite = self.scorer._composite(rep, buyer, milestone, quality)

        assert result.rep_adherence_score == rep
        assert result.buyer_adherence_score == buyer
        assert result.milestone_progress_score == milestone
        assert result.map_quality_score == quality
        assert result.map_adherence_composite == composite

    def test_map_health_consistent_with_composite(self):
        result = self.scorer.score(make_inp())
        composite = result.map_adherence_composite
        if composite >= 65:
            assert result.map_health == MAPHealth.ON_TRACK
        elif composite >= 45:
            assert result.map_health == MAPHealth.SLIPPING
        elif composite >= 25:
            assert result.map_health == MAPHealth.AT_RISK
        else:
            assert result.map_health == MAPHealth.BROKEN

    def test_action_consistent_with_health_and_needs_reset(self):
        result = self.scorer.score(make_inp())
        if result.needs_map_reset or result.map_health == MAPHealth.BROKEN:
            assert result.map_action == MAPAction.ESCALATE
        elif result.map_health == MAPHealth.AT_RISK:
            assert result.map_action == MAPAction.RESET_MAP
        elif result.map_health == MAPHealth.SLIPPING:
            assert result.map_action == MAPAction.REAFFIRM
        else:
            assert result.map_action == MAPAction.ACCELERATE

    def test_is_healthy_consistent_across_many(self):
        inputs = [make_inp(deal_id=f"d{i}",
                           rep_milestones_completed=i % 6,
                           buyer_milestones_completed=i % 6)
                  for i in range(10)]
        scorer = make_scorer()
        for inp in inputs:
            r = scorer.score(inp)
            assert r.is_healthy_map == (r.map_adherence_composite >= 65.0)

    def test_needs_reset_consistent_across_many(self):
        inputs = [make_inp(deal_id=f"d{i}",
                           buyer_milestones_missed=i % 5,
                           rep_milestones_missed=i % 4)
                  for i in range(12)]
        scorer = make_scorer()
        for inp in inputs:
            r = scorer.score(inp)
            expected = r.map_adherence_composite < 35.0 or inp.buyer_milestones_missed >= 3
            assert r.needs_map_reset == expected

    def test_summary_counts_after_batch(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(6)]
        self.scorer.score_batch(inputs)
        s = self.scorer.summary()
        assert s["total"] == 6
        assert sum(s["health_counts"].values()) == 6
        assert sum(s["action_counts"].values()) == 6

    def test_to_dict_round_trip(self):
        result = self.scorer.score(make_inp())
        d = result.to_dict()
        assert d["rep_adherence_score"] == result.rep_adherence_score
        assert d["buyer_adherence_score"] == result.buyer_adherence_score
        assert d["map_adherence_composite"] == result.map_adherence_composite
        assert d["is_healthy_map"] == result.is_healthy_map
        assert d["needs_map_reset"] == result.needs_map_reset
        assert d["map_health"] == result.map_health.value

    def test_properties_match_filtered_results(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(5)])
        assert self.scorer.healthy_maps == [r for r in self.scorer._results if r.is_healthy_map]
        assert self.scorer.maps_needing_reset == [r for r in self.scorer._results if r.needs_map_reset]

    def test_avg_properties_match_summary(self):
        self.scorer.score_batch([make_inp(deal_id=f"d{i}") for i in range(4)])
        s = self.scorer.summary()
        assert self.scorer.avg_close_confidence == s["avg_close_confidence"]
        assert self.scorer.avg_map_adherence_composite == s["avg_map_adherence_composite"]

    def test_score_batch_same_as_sequential_score(self):
        inputs = [make_inp(deal_id=f"d{i}", rep_milestones_completed=i % 5)
                  for i in range(5)]
        s_seq = make_scorer()
        s_bat = make_scorer()

        for inp in inputs:
            s_seq.score(inp)
        s_bat.score_batch(inputs)

        for i in range(5):
            assert s_seq._results[i].map_adherence_composite == s_bat._results[i].map_adherence_composite

    def test_commitment_signal_consistent_with_buyer_score(self):
        """Absent signal must correspond to buyer score < 40."""
        for deal in range(8):
            inp = make_inp(deal_id=f"d{deal}",
                           buyer_milestones_completed=deal % 4,
                           buyer_milestones_missed=deal % 3)
            r = self.scorer.score(inp)
            if r.commitment_signal == CommitmentSignal.ABSENT:
                assert r.buyer_adherence_score < 40.0
