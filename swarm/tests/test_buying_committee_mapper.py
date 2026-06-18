"""Comprehensive pytest tests for BuyingCommitteeMapper."""
from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.buying_committee_mapper import (
    BuyingCommitteeMapper,
    BuyingCommitteeInput,
    BuyingCommitteeResult,
    CommitteeCoverage,
    CommitteeRisk,
    DealComplexity,
    CommitteeAction,
)


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def make_input(
    deal_id: str = "D001",
    deal_name: str = "Test Deal",
    rep_id: str = "R01",
    economic_buyer_identified: int = 1,
    economic_buyer_engaged: int = 1,
    champion_identified: int = 1,
    champion_engaged: int = 1,
    technical_evaluator_identified: int = 1,
    technical_evaluator_engaged: int = 1,
    end_user_identified: int = 1,
    end_user_engaged: int = 1,
    blocker_identified: int = 0,
    blocker_neutralized: int = 0,
    total_stakeholders_mapped: int = 6,
    total_stakeholders_engaged: int = 5,
    exec_sponsor_exists: int = 1,
    procurement_involved: int = 1,
    legal_involved: int = 1,
    deal_size_usd: float = 200_000.0,
    deal_stage_numeric: int = 4,
    days_to_close: int = 30,
    last_new_stakeholder_days_ago: int = 7,
) -> BuyingCommitteeInput:
    """Return a fully-populated BuyingCommitteeInput (all good defaults)."""
    return BuyingCommitteeInput(
        deal_id=deal_id,
        deal_name=deal_name,
        rep_id=rep_id,
        economic_buyer_identified=economic_buyer_identified,
        economic_buyer_engaged=economic_buyer_engaged,
        champion_identified=champion_identified,
        champion_engaged=champion_engaged,
        technical_evaluator_identified=technical_evaluator_identified,
        technical_evaluator_engaged=technical_evaluator_engaged,
        end_user_identified=end_user_identified,
        end_user_engaged=end_user_engaged,
        blocker_identified=blocker_identified,
        blocker_neutralized=blocker_neutralized,
        total_stakeholders_mapped=total_stakeholders_mapped,
        total_stakeholders_engaged=total_stakeholders_engaged,
        exec_sponsor_exists=exec_sponsor_exists,
        procurement_involved=procurement_involved,
        legal_involved=legal_involved,
        deal_size_usd=deal_size_usd,
        deal_stage_numeric=deal_stage_numeric,
        days_to_close=days_to_close,
        last_new_stakeholder_days_ago=last_new_stakeholder_days_ago,
    )


@pytest.fixture
def mapper() -> BuyingCommitteeMapper:
    return BuyingCommitteeMapper()


@pytest.fixture
def good_input() -> BuyingCommitteeInput:
    """A well-covered deal: all roles identified + engaged, no blocker."""
    return make_input()


@pytest.fixture
def weak_input() -> BuyingCommitteeInput:
    """A poorly-covered deal: no roles identified, single stakeholder."""
    return make_input(
        deal_id="D002",
        economic_buyer_identified=0,
        economic_buyer_engaged=0,
        champion_identified=0,
        champion_engaged=0,
        technical_evaluator_identified=0,
        technical_evaluator_engaged=0,
        end_user_identified=0,
        end_user_engaged=0,
        blocker_identified=0,
        total_stakeholders_mapped=1,
        total_stakeholders_engaged=1,
        exec_sponsor_exists=0,
        procurement_involved=0,
        legal_involved=0,
        deal_size_usd=10_000.0,
        deal_stage_numeric=1,
        days_to_close=90,
        last_new_stakeholder_days_ago=60,
    )


# ---------------------------------------------------------------------------
# 1. Structural invariants
# ---------------------------------------------------------------------------

class TestStructuralInvariants:
    def test_buying_committee_input_has_22_fields(self):
        fields = dataclasses.fields(BuyingCommitteeInput)
        assert len(fields) == 22, f"Expected 22 fields, got {len(fields)}"

    def test_to_dict_returns_exactly_15_keys(self, mapper, good_input):
        result = mapper.map(good_input)
        d = result.to_dict()
        assert len(d) == 15, f"Expected 15 keys, got {len(d)}"

    def test_to_dict_correct_key_names(self, mapper, good_input):
        result = mapper.map(good_input)
        d = result.to_dict()
        expected_keys = {
            "deal_id", "deal_name", "committee_coverage", "committee_risk",
            "deal_complexity", "committee_action", "role_coverage_score",
            "engagement_breadth_score", "blocker_management_score",
            "late_stage_alignment_score", "committee_composite",
            "coverage_ratio", "missing_role_count", "is_well_covered",
            "needs_expansion",
        }
        assert set(d.keys()) == expected_keys

    def test_summary_returns_exactly_13_keys_when_empty(self, mapper):
        s = mapper.summary()
        assert len(s) == 13, f"Expected 13 keys, got {len(s)}"

    def test_summary_returns_exactly_13_keys_with_data(self, mapper, good_input):
        mapper.map(good_input)
        s = mapper.summary()
        assert len(s) == 13, f"Expected 13 keys, got {len(s)}"

    def test_summary_correct_key_names(self, mapper, good_input):
        mapper.map(good_input)
        s = mapper.summary()
        expected_keys = {
            "total", "coverage_counts", "risk_counts", "complexity_counts",
            "action_counts", "avg_committee_composite", "avg_coverage_ratio",
            "well_covered_count", "expansion_needed_count",
            "avg_role_coverage_score", "avg_engagement_breadth_score",
            "avg_blocker_management_score", "avg_late_stage_alignment_score",
        }
        assert set(s.keys()) == expected_keys


# ---------------------------------------------------------------------------
# 2. Enum values
# ---------------------------------------------------------------------------

class TestEnums:
    def test_committee_coverage_values(self):
        assert CommitteeCoverage.FULL_COVERAGE.value == "full_coverage"
        assert CommitteeCoverage.PARTIAL.value == "partial"
        assert CommitteeCoverage.THIN.value == "thin"
        assert CommitteeCoverage.SINGLE_THREADED.value == "single_threaded"
        assert len(CommitteeCoverage) == 4

    def test_committee_risk_values(self):
        assert CommitteeRisk.LOW.value == "low"
        assert CommitteeRisk.MODERATE.value == "moderate"
        assert CommitteeRisk.HIGH.value == "high"
        assert CommitteeRisk.CRITICAL.value == "critical"
        assert len(CommitteeRisk) == 4

    def test_deal_complexity_values(self):
        assert DealComplexity.SIMPLE.value == "simple"
        assert DealComplexity.STANDARD.value == "standard"
        assert DealComplexity.COMPLEX.value == "complex"
        assert DealComplexity.ENTERPRISE.value == "enterprise"
        assert len(DealComplexity) == 4

    def test_committee_action_values(self):
        assert CommitteeAction.MAINTAIN.value == "maintain"
        assert CommitteeAction.EXPAND_COVERAGE.value == "expand_coverage"
        assert CommitteeAction.NEUTRALIZE_BLOCKER.value == "neutralize_blocker"
        assert CommitteeAction.EXECUTIVE_ALIGNMENT.value == "executive_alignment"
        assert len(CommitteeAction) == 4

    def test_enums_are_str_subclass(self):
        for enum_cls in (CommitteeCoverage, CommitteeRisk, DealComplexity, CommitteeAction):
            for member in enum_cls:
                assert isinstance(member, str)


# ---------------------------------------------------------------------------
# 3. _role_coverage_score
# ---------------------------------------------------------------------------

class TestRoleCoverageScore:
    def test_all_roles_identified_engaged_no_exec(self, mapper):
        inp = make_input(exec_sponsor_exists=0)
        # 15+15+12+13+10+10+7+8 = 90
        score = mapper._role_coverage_score(inp)
        assert score == 90.0

    def test_all_roles_identified_engaged_with_exec(self, mapper):
        inp = make_input(exec_sponsor_exists=1)
        # 90 + 10 = 100
        score = mapper._role_coverage_score(inp)
        assert score == 100.0

    def test_no_roles_identified_or_engaged_no_exec(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, economic_buyer_engaged=0,
            champion_identified=0, champion_engaged=0,
            technical_evaluator_identified=0, technical_evaluator_engaged=0,
            end_user_identified=0, end_user_engaged=0,
            exec_sponsor_exists=0,
        )
        assert mapper._role_coverage_score(inp) == 0.0

    def test_only_economic_buyer_identified(self, mapper):
        inp = make_input(
            economic_buyer_identified=1, economic_buyer_engaged=0,
            champion_identified=0, champion_engaged=0,
            technical_evaluator_identified=0, technical_evaluator_engaged=0,
            end_user_identified=0, end_user_engaged=0,
            exec_sponsor_exists=0,
        )
        assert mapper._role_coverage_score(inp) == 15.0

    def test_economic_buyer_identified_and_engaged(self, mapper):
        inp = make_input(
            economic_buyer_identified=1, economic_buyer_engaged=1,
            champion_identified=0, champion_engaged=0,
            technical_evaluator_identified=0, technical_evaluator_engaged=0,
            end_user_identified=0, end_user_engaged=0,
            exec_sponsor_exists=0,
        )
        assert mapper._role_coverage_score(inp) == 30.0

    def test_champion_only_identified(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, economic_buyer_engaged=0,
            champion_identified=1, champion_engaged=0,
            technical_evaluator_identified=0, technical_evaluator_engaged=0,
            end_user_identified=0, end_user_engaged=0,
            exec_sponsor_exists=0,
        )
        assert mapper._role_coverage_score(inp) == 12.0

    def test_champion_identified_and_engaged(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, economic_buyer_engaged=0,
            champion_identified=1, champion_engaged=1,
            technical_evaluator_identified=0, technical_evaluator_engaged=0,
            end_user_identified=0, end_user_engaged=0,
            exec_sponsor_exists=0,
        )
        assert mapper._role_coverage_score(inp) == 25.0

    def test_exec_sponsor_bonus_does_not_exceed_100(self, mapper):
        inp = make_input(exec_sponsor_exists=1)
        score = mapper._role_coverage_score(inp)
        assert score <= 100.0

    def test_score_bounded_0_100(self, mapper):
        for combo in [make_input(exec_sponsor_exists=0), make_input(exec_sponsor_exists=1)]:
            s = mapper._role_coverage_score(combo)
            assert 0.0 <= s <= 100.0

    def test_end_user_points(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, economic_buyer_engaged=0,
            champion_identified=0, champion_engaged=0,
            technical_evaluator_identified=0, technical_evaluator_engaged=0,
            end_user_identified=1, end_user_engaged=1,
            exec_sponsor_exists=0,
        )
        assert mapper._role_coverage_score(inp) == 15.0  # 7 + 8

    def test_technical_evaluator_points(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, economic_buyer_engaged=0,
            champion_identified=0, champion_engaged=0,
            technical_evaluator_identified=1, technical_evaluator_engaged=1,
            end_user_identified=0, end_user_engaged=0,
            exec_sponsor_exists=0,
        )
        assert mapper._role_coverage_score(inp) == 20.0  # 10 + 10


# ---------------------------------------------------------------------------
# 4. _engagement_breadth_score
# ---------------------------------------------------------------------------

class TestEngagementBreadthScore:
    def test_eight_or_more_engaged_high_ratio_recent(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=8,
            total_stakeholders_mapped=8,
            last_new_stakeholder_days_ago=7,
            exec_sponsor_exists=1,
        )
        # 40 (>=8) + 35 (ratio>=0.8) + 15 (<=14 days) + 10 (exec) = 100
        score = mapper._engagement_breadth_score(inp)
        assert score == 100.0

    def test_five_to_seven_engaged(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=5,
            total_stakeholders_mapped=10,  # ratio=0.5 -> 12 pts
            last_new_stakeholder_days_ago=60,
            exec_sponsor_exists=0,
        )
        # 28 + 12 + 0 = 40
        score = mapper._engagement_breadth_score(inp)
        assert score == 40.0

    def test_three_to_four_engaged(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=3,
            total_stakeholders_mapped=10,  # ratio=0.3 -> 0 pts
            last_new_stakeholder_days_ago=60,
            exec_sponsor_exists=0,
        )
        # 16 + 0 + 0 = 16
        score = mapper._engagement_breadth_score(inp)
        assert score == 16.0

    def test_two_engaged(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=2,
            total_stakeholders_mapped=10,
            last_new_stakeholder_days_ago=60,
            exec_sponsor_exists=0,
        )
        # 8 + 0 + 0 = 8
        score = mapper._engagement_breadth_score(inp)
        assert score == 8.0

    def test_one_engaged(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=1,
            total_stakeholders_mapped=10,
            last_new_stakeholder_days_ago=60,
            exec_sponsor_exists=0,
        )
        # 3 + 0 + 0 = 3
        score = mapper._engagement_breadth_score(inp)
        assert score == 3.0

    def test_zero_engaged(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=0,
            total_stakeholders_mapped=5,
            last_new_stakeholder_days_ago=60,
            exec_sponsor_exists=0,
        )
        assert mapper._engagement_breadth_score(inp) == 0.0

    def test_ratio_0_8_threshold(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=4,
            total_stakeholders_mapped=5,  # ratio=0.8 exactly
            last_new_stakeholder_days_ago=60,
            exec_sponsor_exists=0,
        )
        # 8 (2 engaged) + 35 (ratio>=0.8) + 0 = 43... wait engaged=4 -> 8? No:
        # engaged=4: neither >=8 nor >=5 nor >=3? 4>=3 -> 16
        # 16 + 35 + 0 = 51
        score = mapper._engagement_breadth_score(inp)
        assert score == 51.0

    def test_ratio_0_6_threshold(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=3,
            total_stakeholders_mapped=5,  # ratio=0.6 exactly
            last_new_stakeholder_days_ago=60,
            exec_sponsor_exists=0,
        )
        # 16 + 22 + 0 = 38
        score = mapper._engagement_breadth_score(inp)
        assert score == 38.0

    def test_stakeholder_added_within_14_days(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=3,
            total_stakeholders_mapped=10,
            last_new_stakeholder_days_ago=14,
            exec_sponsor_exists=0,
        )
        # 16 + 0 + 15 = 31
        score = mapper._engagement_breadth_score(inp)
        assert score == 31.0

    def test_stakeholder_added_15_to_30_days(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=3,
            total_stakeholders_mapped=10,
            last_new_stakeholder_days_ago=30,
            exec_sponsor_exists=0,
        )
        # 16 + 0 + 8 = 24
        score = mapper._engagement_breadth_score(inp)
        assert score == 24.0

    def test_zero_mapped_no_ratio_points(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=3,
            total_stakeholders_mapped=0,
            last_new_stakeholder_days_ago=60,
            exec_sponsor_exists=0,
        )
        # 16 + 0 + 0 = 16
        score = mapper._engagement_breadth_score(inp)
        assert score == 16.0

    def test_score_bounded_0_100(self, mapper):
        score = mapper._engagement_breadth_score(make_input())
        assert 0.0 <= score <= 100.0


# ---------------------------------------------------------------------------
# 5. _blocker_management_score
# ---------------------------------------------------------------------------

class TestBlockerManagementScore:
    def test_no_blocker_returns_75(self, mapper):
        inp = make_input(blocker_identified=0, blocker_neutralized=0)
        assert mapper._blocker_management_score(inp) == 75.0

    def test_blocker_neutralized_returns_80(self, mapper):
        inp = make_input(blocker_identified=1, blocker_neutralized=1)
        assert mapper._blocker_management_score(inp) == 80.0

    def test_blocker_not_neutralized_base_20(self, mapper):
        inp = make_input(
            blocker_identified=1, blocker_neutralized=0,
            deal_stage_numeric=2, days_to_close=60,
        )
        # base=20, stage<4 no penalty, days>14 no penalty
        assert mapper._blocker_management_score(inp) == 20.0

    def test_blocker_not_neutralized_late_stage_penalty(self, mapper):
        inp = make_input(
            blocker_identified=1, blocker_neutralized=0,
            deal_stage_numeric=4, days_to_close=60,
        )
        # base=20 - 10 (stage>=4) = 10
        assert mapper._blocker_management_score(inp) == 10.0

    def test_blocker_not_neutralized_near_close_penalty(self, mapper):
        inp = make_input(
            blocker_identified=1, blocker_neutralized=0,
            deal_stage_numeric=2, days_to_close=14,
        )
        # base=20 - 10 (days<=14) = 10
        assert mapper._blocker_management_score(inp) == 10.0

    def test_blocker_not_neutralized_both_penalties(self, mapper):
        inp = make_input(
            blocker_identified=1, blocker_neutralized=0,
            deal_stage_numeric=5, days_to_close=7,
        )
        # base=20 - 10 - 10 = 0
        assert mapper._blocker_management_score(inp) == 0.0

    def test_score_bounded_0_100(self, mapper):
        for inp in [
            make_input(blocker_identified=0),
            make_input(blocker_identified=1, blocker_neutralized=1),
            make_input(blocker_identified=1, blocker_neutralized=0, deal_stage_numeric=6, days_to_close=1),
        ]:
            s = mapper._blocker_management_score(inp)
            assert 0.0 <= s <= 100.0


# ---------------------------------------------------------------------------
# 6. _late_stage_alignment_score
# ---------------------------------------------------------------------------

class TestLateStageAlignmentScore:
    def test_all_factors_late_stage(self, mapper):
        inp = make_input(
            economic_buyer_engaged=1,
            exec_sponsor_exists=1,
            procurement_involved=1,
            legal_involved=1,
            deal_stage_numeric=5,
            champion_engaged=1,
            technical_evaluator_engaged=1,
            end_user_engaged=1,
        )
        # 35 (eb late) + 25 (exec late) + 20 (proc) + 10 (legal) + 10 (all 4) = 100
        score = mapper._late_stage_alignment_score(inp)
        assert score == 100.0

    def test_economic_buyer_engaged_early_stage(self, mapper):
        inp = make_input(
            economic_buyer_engaged=1,
            exec_sponsor_exists=0,
            procurement_involved=0,
            legal_involved=0,
            deal_stage_numeric=2,
            champion_engaged=0,
            technical_evaluator_engaged=0,
            end_user_engaged=0,
        )
        # 20 (eb early) + 0 + 0 + 0 + 0 = 20
        score = mapper._late_stage_alignment_score(inp)
        assert score == 20.0

    def test_economic_buyer_engaged_late_stage(self, mapper):
        inp = make_input(
            economic_buyer_engaged=1,
            exec_sponsor_exists=0,
            procurement_involved=0,
            legal_involved=0,
            deal_stage_numeric=4,
            champion_engaged=0,
            technical_evaluator_engaged=0,
            end_user_engaged=0,
        )
        # 35 (eb late) = 35
        score = mapper._late_stage_alignment_score(inp)
        assert score == 35.0

    def test_exec_sponsor_early_vs_late(self, mapper):
        early = make_input(
            economic_buyer_engaged=0, exec_sponsor_exists=1,
            procurement_involved=0, legal_involved=0,
            deal_stage_numeric=3, champion_engaged=0,
            technical_evaluator_engaged=0, end_user_engaged=0,
        )
        late = make_input(
            economic_buyer_engaged=0, exec_sponsor_exists=1,
            procurement_involved=0, legal_involved=0,
            deal_stage_numeric=4, champion_engaged=0,
            technical_evaluator_engaged=0, end_user_engaged=0,
        )
        assert mapper._late_stage_alignment_score(early) == 12.0
        assert mapper._late_stage_alignment_score(late) == 25.0

    def test_procurement_adds_20(self, mapper):
        inp = make_input(
            economic_buyer_engaged=0, exec_sponsor_exists=0,
            procurement_involved=1, legal_involved=0,
            deal_stage_numeric=1, champion_engaged=0,
            technical_evaluator_engaged=0, end_user_engaged=0,
        )
        assert mapper._late_stage_alignment_score(inp) == 20.0

    def test_legal_adds_10(self, mapper):
        inp = make_input(
            economic_buyer_engaged=0, exec_sponsor_exists=0,
            procurement_involved=0, legal_involved=1,
            deal_stage_numeric=1, champion_engaged=0,
            technical_evaluator_engaged=0, end_user_engaged=0,
        )
        assert mapper._late_stage_alignment_score(inp) == 10.0

    def test_all_4_roles_bonus_10(self, mapper):
        inp = make_input(
            economic_buyer_engaged=1, exec_sponsor_exists=0,
            procurement_involved=0, legal_involved=0,
            deal_stage_numeric=2,
            champion_engaged=1, technical_evaluator_engaged=1, end_user_engaged=1,
        )
        # 20 (eb early) + 10 (all 4) = 30
        assert mapper._late_stage_alignment_score(inp) == 30.0

    def test_no_factors_returns_0(self, mapper):
        inp = make_input(
            economic_buyer_engaged=0, exec_sponsor_exists=0,
            procurement_involved=0, legal_involved=0,
            deal_stage_numeric=1, champion_engaged=0,
            technical_evaluator_engaged=0, end_user_engaged=0,
        )
        assert mapper._late_stage_alignment_score(inp) == 0.0

    def test_score_bounded_0_100(self, mapper):
        score = mapper._late_stage_alignment_score(make_input())
        assert 0.0 <= score <= 100.0


# ---------------------------------------------------------------------------
# 7. _composite
# ---------------------------------------------------------------------------

class TestComposite:
    def test_composite_formula(self, mapper):
        # role*0.35 + breadth*0.30 + blocker*0.20 + late*0.15
        result = mapper._composite(80.0, 60.0, 75.0, 50.0)
        expected = round(80.0 * 0.35 + 60.0 * 0.30 + 75.0 * 0.20 + 50.0 * 0.15, 1)
        assert result == expected

    def test_composite_all_100(self, mapper):
        assert mapper._composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_composite_all_zero(self, mapper):
        assert mapper._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_weights_sum_to_1(self):
        assert abs(0.35 + 0.30 + 0.20 + 0.15 - 1.0) < 1e-9

    def test_composite_bounded_0_100(self, mapper):
        c = mapper._composite(50.0, 50.0, 50.0, 50.0)
        assert 0.0 <= c <= 100.0

    def test_composite_exact_values(self, mapper):
        # role=60, breadth=40, blocker=75, late=30
        # 60*0.35 + 40*0.30 + 75*0.20 + 30*0.15
        # = 21 + 12 + 15 + 4.5 = 52.5
        result = mapper._composite(60.0, 40.0, 75.0, 30.0)
        assert result == 52.5


# ---------------------------------------------------------------------------
# 8. _missing_role_count
# ---------------------------------------------------------------------------

class TestMissingRoleCount:
    def test_all_identified_returns_0(self, mapper):
        inp = make_input(
            economic_buyer_identified=1, champion_identified=1,
            technical_evaluator_identified=1, end_user_identified=1,
        )
        assert mapper._missing_role_count(inp) == 0

    def test_none_identified_returns_4(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, champion_identified=0,
            technical_evaluator_identified=0, end_user_identified=0,
        )
        assert mapper._missing_role_count(inp) == 4

    def test_one_missing(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, champion_identified=1,
            technical_evaluator_identified=1, end_user_identified=1,
        )
        assert mapper._missing_role_count(inp) == 1

    def test_two_missing(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, champion_identified=0,
            technical_evaluator_identified=1, end_user_identified=1,
        )
        assert mapper._missing_role_count(inp) == 2

    def test_three_missing(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, champion_identified=0,
            technical_evaluator_identified=0, end_user_identified=1,
        )
        assert mapper._missing_role_count(inp) == 3

    def test_engaged_flags_do_not_affect_count(self, mapper):
        # Only _identified flags matter, not _engaged
        inp = make_input(
            economic_buyer_identified=0, economic_buyer_engaged=1,
            champion_identified=0, champion_engaged=1,
            technical_evaluator_identified=0, technical_evaluator_engaged=1,
            end_user_identified=0, end_user_engaged=1,
        )
        assert mapper._missing_role_count(inp) == 4


# ---------------------------------------------------------------------------
# 9. _committee_coverage classifier
# ---------------------------------------------------------------------------

class TestCommitteeCoverage:
    def test_full_coverage_high_composite_many_engaged(self, mapper):
        # composite >=70, engaged >=5
        result = mapper._committee_coverage(75.0, make_input(total_stakeholders_engaged=5))
        assert result == CommitteeCoverage.FULL_COVERAGE

    def test_partial_composite_55_engaged_3(self, mapper):
        result = mapper._committee_coverage(60.0, make_input(total_stakeholders_engaged=3))
        assert result == CommitteeCoverage.PARTIAL

    def test_thin_engaged_2(self, mapper):
        result = mapper._committee_coverage(30.0, make_input(total_stakeholders_engaged=2))
        assert result == CommitteeCoverage.THIN

    def test_single_threaded_one_engaged(self, mapper):
        result = mapper._committee_coverage(10.0, make_input(total_stakeholders_engaged=1))
        assert result == CommitteeCoverage.SINGLE_THREADED

    def test_full_coverage_boundary_composite_70(self, mapper):
        result = mapper._committee_coverage(70.0, make_input(total_stakeholders_engaged=5))
        assert result == CommitteeCoverage.FULL_COVERAGE

    def test_partial_boundary_composite_55(self, mapper):
        result = mapper._committee_coverage(55.0, make_input(total_stakeholders_engaged=3))
        assert result == CommitteeCoverage.PARTIAL

    def test_high_composite_but_few_engaged_falls_through(self, mapper):
        # composite>=70 but engaged=4 (not >=5) -> check if partial applies: 70>=55 and 4>=3 -> partial
        result = mapper._committee_coverage(70.0, make_input(total_stakeholders_engaged=4))
        assert result == CommitteeCoverage.PARTIAL

    def test_zero_engaged_single_threaded(self, mapper):
        result = mapper._committee_coverage(0.0, make_input(total_stakeholders_engaged=0))
        assert result == CommitteeCoverage.SINGLE_THREADED


# ---------------------------------------------------------------------------
# 10. _committee_risk classifier
# ---------------------------------------------------------------------------

class TestCommitteeRisk:
    def test_critical_one_stakeholder(self, mapper):
        inp = make_input(total_stakeholders_engaged=1)
        result = mapper._committee_risk(50.0, inp)
        assert result == CommitteeRisk.CRITICAL

    def test_critical_low_composite(self, mapper):
        inp = make_input(total_stakeholders_engaged=5)
        result = mapper._committee_risk(15.0, inp)
        assert result == CommitteeRisk.CRITICAL

    def test_high_composite_below_35(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=4,
            blocker_identified=0,
        )
        result = mapper._committee_risk(30.0, inp)
        assert result == CommitteeRisk.HIGH

    def test_high_due_to_blocker_late_stage(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=5,
            blocker_identified=1,
            blocker_neutralized=0,
            deal_stage_numeric=4,
        )
        result = mapper._committee_risk(60.0, inp)
        assert result == CommitteeRisk.HIGH

    def test_moderate_composite_35_to_54(self, mapper):
        inp = make_input(total_stakeholders_engaged=4, blocker_identified=0)
        result = mapper._committee_risk(45.0, inp)
        assert result == CommitteeRisk.MODERATE

    def test_low_composite_55_plus(self, mapper):
        inp = make_input(total_stakeholders_engaged=5, blocker_identified=0)
        result = mapper._committee_risk(65.0, inp)
        assert result == CommitteeRisk.LOW

    def test_boundary_critical_below_20(self, mapper):
        # composite < 20 (strictly) triggers CRITICAL; == 20 does NOT
        inp = make_input(total_stakeholders_engaged=3, blocker_identified=0)
        assert mapper._committee_risk(19.9, inp) == CommitteeRisk.CRITICAL
        assert mapper._committee_risk(20.0, inp) != CommitteeRisk.CRITICAL

    def test_boundary_high_at_35(self, mapper):
        inp = make_input(total_stakeholders_engaged=3, blocker_identified=0)
        result = mapper._committee_risk(35.0, inp)
        assert result == CommitteeRisk.MODERATE

    def test_boundary_moderate_at_55(self, mapper):
        inp = make_input(total_stakeholders_engaged=3, blocker_identified=0)
        result = mapper._committee_risk(55.0, inp)
        assert result == CommitteeRisk.LOW


# ---------------------------------------------------------------------------
# 11. _deal_complexity classifier
# ---------------------------------------------------------------------------

class TestDealComplexity:
    def test_enterprise_by_size(self, mapper):
        inp = make_input(deal_size_usd=500_000, total_stakeholders_mapped=2)
        assert mapper._deal_complexity(inp) == DealComplexity.ENTERPRISE

    def test_enterprise_by_stakeholders(self, mapper):
        inp = make_input(deal_size_usd=10_000, total_stakeholders_mapped=10)
        assert mapper._deal_complexity(inp) == DealComplexity.ENTERPRISE

    def test_complex_by_size(self, mapper):
        inp = make_input(deal_size_usd=150_000, total_stakeholders_mapped=2)
        assert mapper._deal_complexity(inp) == DealComplexity.COMPLEX

    def test_complex_by_stakeholders(self, mapper):
        inp = make_input(deal_size_usd=10_000, total_stakeholders_mapped=6)
        assert mapper._deal_complexity(inp) == DealComplexity.COMPLEX

    def test_standard_by_size(self, mapper):
        inp = make_input(deal_size_usd=50_000, total_stakeholders_mapped=1)
        assert mapper._deal_complexity(inp) == DealComplexity.STANDARD

    def test_standard_by_stakeholders(self, mapper):
        inp = make_input(deal_size_usd=1_000, total_stakeholders_mapped=3)
        assert mapper._deal_complexity(inp) == DealComplexity.STANDARD

    def test_simple_small(self, mapper):
        inp = make_input(deal_size_usd=10_000, total_stakeholders_mapped=2)
        assert mapper._deal_complexity(inp) == DealComplexity.SIMPLE

    def test_enterprise_boundary_500k(self, mapper):
        inp = make_input(deal_size_usd=500_000, total_stakeholders_mapped=1)
        assert mapper._deal_complexity(inp) == DealComplexity.ENTERPRISE

    def test_complex_boundary_150k(self, mapper):
        inp = make_input(deal_size_usd=150_000, total_stakeholders_mapped=1)
        assert mapper._deal_complexity(inp) == DealComplexity.COMPLEX

    def test_standard_boundary_50k(self, mapper):
        inp = make_input(deal_size_usd=50_000, total_stakeholders_mapped=1)
        assert mapper._deal_complexity(inp) == DealComplexity.STANDARD


# ---------------------------------------------------------------------------
# 12. _committee_action classifier
# ---------------------------------------------------------------------------

class TestCommitteeAction:
    def test_neutralize_blocker_when_blocker_not_neutralized(self, mapper):
        inp = make_input(blocker_identified=1, blocker_neutralized=0, deal_stage_numeric=2)
        action = mapper._committee_action(CommitteeRisk.LOW, False, inp)
        assert action == CommitteeAction.NEUTRALIZE_BLOCKER

    def test_executive_alignment_no_eb_late_stage(self, mapper):
        inp = make_input(
            blocker_identified=0, economic_buyer_engaged=0, deal_stage_numeric=3,
        )
        action = mapper._committee_action(CommitteeRisk.LOW, False, inp)
        assert action == CommitteeAction.EXECUTIVE_ALIGNMENT

    def test_expand_coverage_needs_expansion_true(self, mapper):
        inp = make_input(blocker_identified=0, economic_buyer_engaged=1, deal_stage_numeric=2)
        action = mapper._committee_action(CommitteeRisk.LOW, True, inp)
        assert action == CommitteeAction.EXPAND_COVERAGE

    def test_expand_coverage_high_risk(self, mapper):
        inp = make_input(blocker_identified=0, economic_buyer_engaged=1, deal_stage_numeric=2)
        action = mapper._committee_action(CommitteeRisk.HIGH, False, inp)
        assert action == CommitteeAction.EXPAND_COVERAGE

    def test_expand_coverage_critical_risk(self, mapper):
        inp = make_input(blocker_identified=0, economic_buyer_engaged=1, deal_stage_numeric=2)
        action = mapper._committee_action(CommitteeRisk.CRITICAL, False, inp)
        assert action == CommitteeAction.EXPAND_COVERAGE

    def test_maintain_low_risk_no_expansion(self, mapper):
        inp = make_input(blocker_identified=0, economic_buyer_engaged=1, deal_stage_numeric=2)
        action = mapper._committee_action(CommitteeRisk.LOW, False, inp)
        assert action == CommitteeAction.MAINTAIN

    def test_maintain_moderate_risk_no_expansion(self, mapper):
        inp = make_input(blocker_identified=0, economic_buyer_engaged=1, deal_stage_numeric=2)
        action = mapper._committee_action(CommitteeRisk.MODERATE, False, inp)
        assert action == CommitteeAction.MAINTAIN

    def test_blocker_takes_priority_over_executive_alignment(self, mapper):
        # Both blocker AND no EB engaged late stage: blocker wins
        inp = make_input(
            blocker_identified=1, blocker_neutralized=0,
            economic_buyer_engaged=0, deal_stage_numeric=4,
        )
        action = mapper._committee_action(CommitteeRisk.HIGH, False, inp)
        assert action == CommitteeAction.NEUTRALIZE_BLOCKER

    def test_eb_not_engaged_early_stage_no_exec_alignment(self, mapper):
        # Stage < 3: no executive_alignment triggered
        inp = make_input(blocker_identified=0, economic_buyer_engaged=0, deal_stage_numeric=2)
        action = mapper._committee_action(CommitteeRisk.LOW, False, inp)
        # eb not engaged but stage=2 < 3, so falls through to expand/maintain
        assert action == CommitteeAction.MAINTAIN

    def test_neutralized_blocker_does_not_trigger_neutralize(self, mapper):
        inp = make_input(blocker_identified=1, blocker_neutralized=1, economic_buyer_engaged=1, deal_stage_numeric=2)
        action = mapper._committee_action(CommitteeRisk.LOW, False, inp)
        assert action == CommitteeAction.MAINTAIN


# ---------------------------------------------------------------------------
# 13. is_well_covered and needs_expansion
# ---------------------------------------------------------------------------

class TestWellCoveredAndNeedsExpansion:
    def test_is_well_covered_true_when_composite_ge_65_missing_0(self, mapper):
        inp = make_input()
        result = mapper.map(inp)
        # Verify it actually is well-covered under good conditions
        if result.committee_composite >= 65 and result.missing_role_count == 0:
            assert result.is_well_covered is True
        else:
            assert result.is_well_covered is False

    def test_is_well_covered_false_when_missing_gt_0(self, mapper):
        inp = make_input(economic_buyer_identified=0)
        result = mapper.map(inp)
        assert result.is_well_covered is False

    def test_is_well_covered_false_when_composite_lt_65(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, economic_buyer_engaged=0,
            champion_identified=0, champion_engaged=0,
            total_stakeholders_engaged=2, exec_sponsor_exists=0,
            procurement_involved=0, legal_involved=0,
        )
        result = mapper.map(inp)
        assert result.committee_composite < 65 or result.missing_role_count > 0
        assert result.is_well_covered is False

    def test_needs_expansion_true_low_composite(self, mapper):
        inp = make_input(
            economic_buyer_identified=0, economic_buyer_engaged=0,
            champion_identified=0, champion_engaged=0,
            technical_evaluator_identified=0, technical_evaluator_engaged=0,
            end_user_identified=0, end_user_engaged=0,
            total_stakeholders_engaged=1, exec_sponsor_exists=0,
            procurement_involved=0, legal_involved=0,
            blocker_identified=0, deal_size_usd=5_000,
            deal_stage_numeric=1, days_to_close=180,
            last_new_stakeholder_days_ago=90,
        )
        result = mapper.map(inp)
        assert result.needs_expansion is True

    def test_needs_expansion_true_when_missing_ge_2(self, mapper):
        # Force missing >= 2
        inp = make_input(
            economic_buyer_identified=0,
            champion_identified=0,
            technical_evaluator_identified=1,
            end_user_identified=1,
            total_stakeholders_engaged=5,
        )
        result = mapper.map(inp)
        assert result.missing_role_count >= 2
        assert result.needs_expansion is True

    def test_needs_expansion_true_when_total_engaged_lt_3(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=2,
            total_stakeholders_mapped=2,
        )
        result = mapper.map(inp)
        assert result.total_stakeholders_engaged < 3 if hasattr(result, 'total_stakeholders_engaged') else True
        assert result.needs_expansion is True

    def test_well_covered_requires_both_conditions(self, mapper):
        # composite >= 65 but missing > 0 -> NOT well covered
        inp = make_input(economic_buyer_identified=0)
        result = mapper.map(inp)
        assert result.missing_role_count > 0
        assert result.is_well_covered is False


# ---------------------------------------------------------------------------
# 14. coverage_ratio
# ---------------------------------------------------------------------------

class TestCoverageRatio:
    def test_ratio_calculation(self, mapper):
        inp = make_input(total_stakeholders_engaged=3, total_stakeholders_mapped=5)
        result = mapper.map(inp)
        assert result.coverage_ratio == round(3 / 5, 2)

    def test_ratio_zero_when_none_mapped(self, mapper):
        inp = make_input(total_stakeholders_engaged=0, total_stakeholders_mapped=0)
        result = mapper.map(inp)
        assert result.coverage_ratio == 0.0

    def test_ratio_one_when_all_engaged(self, mapper):
        inp = make_input(total_stakeholders_engaged=5, total_stakeholders_mapped=5)
        result = mapper.map(inp)
        assert result.coverage_ratio == 1.0

    def test_ratio_rounded_to_2_decimals(self, mapper):
        inp = make_input(total_stakeholders_engaged=1, total_stakeholders_mapped=3)
        result = mapper.map(inp)
        assert result.coverage_ratio == round(1 / 3, 2)


# ---------------------------------------------------------------------------
# 15. map() integration
# ---------------------------------------------------------------------------

class TestMapIntegration:
    def test_map_returns_result_instance(self, mapper, good_input):
        result = mapper.map(good_input)
        assert isinstance(result, BuyingCommitteeResult)

    def test_map_stores_result_in_internal_list(self, mapper, good_input):
        mapper.map(good_input)
        assert len(mapper._results) == 1

    def test_map_accumulates_results(self, mapper):
        for i in range(3):
            mapper.map(make_input(deal_id=f"D{i:03}"))
        assert len(mapper._results) == 3

    def test_map_deal_id_propagated(self, mapper):
        inp = make_input(deal_id="XYZZY")
        result = mapper.map(inp)
        assert result.deal_id == "XYZZY"

    def test_map_deal_name_propagated(self, mapper):
        inp = make_input(deal_name="Mega Deal")
        result = mapper.map(inp)
        assert result.deal_name == "Mega Deal"

    def test_map_result_scores_in_range(self, mapper, good_input):
        result = mapper.map(good_input)
        for score in (
            result.role_coverage_score, result.engagement_breadth_score,
            result.blocker_management_score, result.late_stage_alignment_score,
            result.committee_composite,
        ):
            assert 0.0 <= score <= 100.0

    def test_map_weak_deal(self, mapper, weak_input):
        result = mapper.map(weak_input)
        assert result.needs_expansion is True
        assert result.committee_composite < 50

    def test_map_to_dict_enum_values_are_strings(self, mapper, good_input):
        d = mapper.map(good_input).to_dict()
        assert isinstance(d["committee_coverage"], str)
        assert isinstance(d["committee_risk"], str)
        assert isinstance(d["deal_complexity"], str)
        assert isinstance(d["committee_action"], str)


# ---------------------------------------------------------------------------
# 16. map_batch()
# ---------------------------------------------------------------------------

class TestMapBatch:
    def test_map_batch_returns_list(self, mapper):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        results = mapper.map_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 3

    def test_map_batch_all_results_are_result_instances(self, mapper):
        inputs = [make_input(deal_id=f"D{i}") for i in range(4)]
        results = mapper.map_batch(inputs)
        for r in results:
            assert isinstance(r, BuyingCommitteeResult)

    def test_map_batch_stores_all_in_internal_results(self, mapper):
        inputs = [make_input(deal_id=f"D{i}") for i in range(5)]
        mapper.map_batch(inputs)
        assert len(mapper._results) == 5

    def test_map_batch_empty_list(self, mapper):
        results = mapper.map_batch([])
        assert results == []
        assert len(mapper._results) == 0

    def test_map_batch_deal_ids_match(self, mapper):
        inputs = [make_input(deal_id=f"DEAL{i}") for i in range(3)]
        results = mapper.map_batch(inputs)
        for inp, result in zip(inputs, results):
            assert result.deal_id == inp.deal_id

    def test_map_batch_accumulates_with_prior_calls(self, mapper):
        mapper.map(make_input(deal_id="D0"))
        mapper.map_batch([make_input(deal_id=f"D{i}") for i in range(1, 4)])
        assert len(mapper._results) == 4


# ---------------------------------------------------------------------------
# 17. reset()
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_results(self, mapper):
        mapper.map(make_input(deal_id="D1"))
        mapper.map(make_input(deal_id="D2"))
        mapper.reset()
        assert len(mapper._results) == 0

    def test_reset_clears_well_covered(self, mapper, good_input):
        mapper.map(good_input)
        mapper.reset()
        assert mapper.well_covered_deals == []

    def test_reset_clears_expansion_queue(self, mapper, weak_input):
        mapper.map(weak_input)
        mapper.reset()
        assert mapper.expansion_needed_queue == []

    def test_reset_resets_avg_composite(self, mapper, good_input):
        mapper.map(good_input)
        mapper.reset()
        assert mapper.avg_committee_composite == 0.0

    def test_reset_allows_new_accumulation(self, mapper):
        mapper.map(make_input(deal_id="D1"))
        mapper.reset()
        mapper.map(make_input(deal_id="D2"))
        assert len(mapper._results) == 1
        assert mapper._results[0].deal_id == "D2"


# ---------------------------------------------------------------------------
# 18. Properties
# ---------------------------------------------------------------------------

class TestProperties:
    def test_well_covered_deals_empty_on_init(self, mapper):
        assert mapper.well_covered_deals == []

    def test_expansion_needed_queue_empty_on_init(self, mapper):
        assert mapper.expansion_needed_queue == []

    def test_avg_committee_composite_zero_on_init(self, mapper):
        assert mapper.avg_committee_composite == 0.0

    def test_avg_coverage_ratio_zero_on_init(self, mapper):
        assert mapper.avg_coverage_ratio == 0.0

    def test_well_covered_deals_filters_correctly(self, mapper):
        mapper.map(make_input(deal_id="D1"))
        mapper.map(make_input(
            deal_id="D2",
            economic_buyer_identified=0, economic_buyer_engaged=0,
            champion_identified=0, champion_engaged=0,
            total_stakeholders_engaged=1, exec_sponsor_exists=0,
            procurement_involved=0, legal_involved=0,
        ))
        covered = mapper.well_covered_deals
        for r in covered:
            assert r.is_well_covered is True

    def test_expansion_needed_queue_filters_correctly(self, mapper, weak_input):
        mapper.map(weak_input)
        for r in mapper.expansion_needed_queue:
            assert r.needs_expansion is True

    def test_avg_committee_composite_single(self, mapper, good_input):
        result = mapper.map(good_input)
        assert mapper.avg_committee_composite == round(result.committee_composite, 1)

    def test_avg_committee_composite_multiple(self, mapper):
        r1 = mapper.map(make_input(deal_id="D1"))
        r2 = mapper.map(make_input(deal_id="D2", total_stakeholders_engaged=1,
                                    exec_sponsor_exists=0, procurement_involved=0,
                                    legal_involved=0))
        expected = round((r1.committee_composite + r2.committee_composite) / 2, 1)
        assert mapper.avg_committee_composite == expected

    def test_avg_coverage_ratio_single(self, mapper):
        inp = make_input(total_stakeholders_engaged=3, total_stakeholders_mapped=5)
        result = mapper.map(inp)
        assert mapper.avg_coverage_ratio == result.coverage_ratio

    def test_avg_coverage_ratio_multiple(self, mapper):
        r1 = mapper.map(make_input(deal_id="D1", total_stakeholders_engaged=4, total_stakeholders_mapped=5))
        r2 = mapper.map(make_input(deal_id="D2", total_stakeholders_engaged=2, total_stakeholders_mapped=4))
        expected = round((r1.coverage_ratio + r2.coverage_ratio) / 2, 2)
        assert mapper.avg_coverage_ratio == expected


# ---------------------------------------------------------------------------
# 19. summary()
# ---------------------------------------------------------------------------

class TestSummary:
    def test_summary_empty_state(self, mapper):
        s = mapper.summary()
        assert s["total"] == 0
        assert s["coverage_counts"] == {}
        assert s["risk_counts"] == {}
        assert s["complexity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_committee_composite"] == 0.0
        assert s["avg_coverage_ratio"] == 0.0
        assert s["well_covered_count"] == 0
        assert s["expansion_needed_count"] == 0
        assert s["avg_role_coverage_score"] == 0.0
        assert s["avg_engagement_breadth_score"] == 0.0
        assert s["avg_blocker_management_score"] == 0.0
        assert s["avg_late_stage_alignment_score"] == 0.0

    def test_summary_total_count(self, mapper):
        mapper.map_batch([make_input(deal_id=f"D{i}") for i in range(3)])
        assert mapper.summary()["total"] == 3

    def test_summary_coverage_counts_populated(self, mapper):
        mapper.map(make_input(deal_id="D1"))
        s = mapper.summary()
        assert sum(s["coverage_counts"].values()) == 1

    def test_summary_risk_counts_populated(self, mapper):
        mapper.map(make_input(deal_id="D1"))
        s = mapper.summary()
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_complexity_counts_populated(self, mapper):
        mapper.map(make_input(deal_id="D1"))
        s = mapper.summary()
        assert sum(s["complexity_counts"].values()) == 1

    def test_summary_action_counts_populated(self, mapper):
        mapper.map(make_input(deal_id="D1"))
        s = mapper.summary()
        assert sum(s["action_counts"].values()) == 1

    def test_summary_avg_committee_composite_matches_property(self, mapper):
        mapper.map_batch([make_input(deal_id=f"D{i}") for i in range(3)])
        s = mapper.summary()
        assert s["avg_committee_composite"] == mapper.avg_committee_composite

    def test_summary_avg_coverage_ratio_matches_property(self, mapper):
        mapper.map_batch([make_input(deal_id=f"D{i}") for i in range(3)])
        s = mapper.summary()
        assert s["avg_coverage_ratio"] == mapper.avg_coverage_ratio

    def test_summary_well_covered_count_matches(self, mapper):
        mapper.map_batch([make_input(deal_id=f"D{i}") for i in range(3)])
        s = mapper.summary()
        assert s["well_covered_count"] == len(mapper.well_covered_deals)

    def test_summary_expansion_needed_count_matches(self, mapper):
        mapper.map_batch([make_input(deal_id=f"D{i}") for i in range(3)])
        s = mapper.summary()
        assert s["expansion_needed_count"] == len(mapper.expansion_needed_queue)

    def test_summary_avg_scores_are_floats(self, mapper):
        mapper.map(make_input())
        s = mapper.summary()
        for key in ("avg_role_coverage_score", "avg_engagement_breadth_score",
                    "avg_blocker_management_score", "avg_late_stage_alignment_score"):
            assert isinstance(s[key], float)

    def test_summary_coverage_counts_uses_enum_values(self, mapper):
        mapper.map(make_input())
        s = mapper.summary()
        for key in s["coverage_counts"]:
            assert key in {e.value for e in CommitteeCoverage}

    def test_summary_risk_counts_uses_enum_values(self, mapper):
        mapper.map(make_input())
        s = mapper.summary()
        for key in s["risk_counts"]:
            assert key in {e.value for e in CommitteeRisk}

    def test_summary_after_reset_returns_empty_state(self, mapper):
        mapper.map(make_input())
        mapper.reset()
        s = mapper.summary()
        assert s["total"] == 0
        assert len(s) == 13

    def test_summary_avg_role_coverage_score_value(self, mapper):
        r = mapper.map(make_input())
        s = mapper.summary()
        assert s["avg_role_coverage_score"] == round(r.role_coverage_score, 1)

    def test_summary_avg_engagement_breadth_score_value(self, mapper):
        r = mapper.map(make_input())
        s = mapper.summary()
        assert s["avg_engagement_breadth_score"] == round(r.engagement_breadth_score, 1)

    def test_summary_avg_blocker_management_score_value(self, mapper):
        r = mapper.map(make_input())
        s = mapper.summary()
        assert s["avg_blocker_management_score"] == round(r.blocker_management_score, 1)

    def test_summary_avg_late_stage_alignment_score_value(self, mapper):
        r = mapper.map(make_input())
        s = mapper.summary()
        assert s["avg_late_stage_alignment_score"] == round(r.late_stage_alignment_score, 1)


# ---------------------------------------------------------------------------
# 20. Edge cases and boundary conditions
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_zero_mapped_stakeholders_coverage_ratio(self, mapper):
        inp = make_input(total_stakeholders_mapped=0, total_stakeholders_engaged=0)
        result = mapper.map(inp)
        assert result.coverage_ratio == 0.0

    def test_large_deal_is_enterprise(self, mapper):
        inp = make_input(deal_size_usd=1_000_000)
        result = mapper.map(inp)
        assert result.deal_complexity == DealComplexity.ENTERPRISE

    def test_many_stakeholders_enterprise(self, mapper):
        inp = make_input(total_stakeholders_mapped=15, total_stakeholders_engaged=10)
        result = mapper.map(inp)
        assert result.deal_complexity == DealComplexity.ENTERPRISE

    def test_blocker_identified_triggers_neutralize_action(self, mapper):
        inp = make_input(blocker_identified=1, blocker_neutralized=0)
        result = mapper.map(inp)
        assert result.committee_action == CommitteeAction.NEUTRALIZE_BLOCKER

    def test_no_blocker_neutralized_flag_without_blocker_identified(self, mapper):
        # blocker_neutralized=1 but blocker_identified=0 -> no penalty
        inp = make_input(blocker_identified=0, blocker_neutralized=1)
        result = mapper.map(inp)
        assert result.blocker_management_score == 75.0

    def test_single_threaded_deal(self, mapper):
        inp = make_input(
            total_stakeholders_engaged=1,
            total_stakeholders_mapped=1,
        )
        result = mapper.map(inp)
        assert result.committee_coverage == CommitteeCoverage.SINGLE_THREADED

    def test_missing_role_count_in_result(self, mapper):
        inp = make_input(
            economic_buyer_identified=0,
            champion_identified=0,
            technical_evaluator_identified=1,
            end_user_identified=1,
        )
        result = mapper.map(inp)
        assert result.missing_role_count == 2

    def test_composite_matches_formula(self, mapper):
        inp = make_input()
        role = mapper._role_coverage_score(inp)
        breadth = mapper._engagement_breadth_score(inp)
        blocker = mapper._blocker_management_score(inp)
        late = mapper._late_stage_alignment_score(inp)
        expected = mapper._composite(role, breadth, blocker, late)
        result = mapper.map(inp)
        assert result.committee_composite == expected

    def test_to_dict_values_types(self, mapper, good_input):
        d = mapper.map(good_input).to_dict()
        assert isinstance(d["deal_id"], str)
        assert isinstance(d["deal_name"], str)
        assert isinstance(d["committee_composite"], float)
        assert isinstance(d["coverage_ratio"], float)
        assert isinstance(d["missing_role_count"], int)
        assert isinstance(d["is_well_covered"], bool)
        assert isinstance(d["needs_expansion"], bool)

    def test_map_does_not_mutate_input(self, mapper):
        inp = make_input(deal_id="ORIGINAL")
        mapper.map(inp)
        assert inp.deal_id == "ORIGINAL"

    def test_multiple_resets_safe(self, mapper):
        mapper.map(make_input())
        mapper.reset()
        mapper.reset()
        assert len(mapper._results) == 0
        assert mapper.avg_committee_composite == 0.0
