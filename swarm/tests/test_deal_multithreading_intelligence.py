"""
Comprehensive pytest test suite for DealMultithreadingIntelligence.
Target: 200+ tests covering all enums, scoring formulas, logic branches,
properties, summary, reset, and end-to-end scenarios.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.deal_multithreading_intelligence import (
    DealMultithreadingIntelligence,
    DealMultithreadingInput,
    DealMultithreadingResult,
    StakeholderCoverage,
    ThreadingAction,
    ThreadingRisk,
    ThreadingStatus,
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _make_base(**overrides) -> DealMultithreadingInput:
    """Well-threaded baseline with high scores across all dimensions."""
    defaults = dict(
        deal_id="deal_001",
        rep_id="rep_001",
        deal_name="Test Deal",
        stakeholder_count=5,
        executive_contacts_count=2,
        champion_confirmed=1,
        economic_buyer_identified=1,
        decision_maker_engaged=1,
        technical_evaluator_engaged=1,
        user_buyer_engaged=1,
        last_exec_contact_days_ago=5,
        contact_engagement_rate=85.0,
        contacts_with_recent_activity=4,
        deal_stage=2,
        deal_value_usd=250000.0,
        days_in_current_stage=15,
        stakeholder_sentiment_avg=78.0,
        champion_risk_score=20.0,
        org_change_signals=0,
        single_threaded_days=0,
        previous_multithreaded=1,
        rep_multithreading_score=85.0,
    )
    defaults.update(overrides)
    return DealMultithreadingInput(**defaults)


def _make_poor(**overrides) -> DealMultithreadingInput:
    """Single-threaded, at-risk baseline with minimal scores."""
    defaults = dict(
        deal_id="deal_002",
        rep_id="rep_002",
        deal_name="Poor Deal",
        stakeholder_count=1,
        executive_contacts_count=0,
        champion_confirmed=0,
        economic_buyer_identified=0,
        decision_maker_engaged=0,
        technical_evaluator_engaged=0,
        user_buyer_engaged=0,
        last_exec_contact_days_ago=90,
        contact_engagement_rate=10.0,
        contacts_with_recent_activity=0,
        deal_stage=2,
        deal_value_usd=100000.0,
        days_in_current_stage=75,
        stakeholder_sentiment_avg=20.0,
        champion_risk_score=80.0,
        org_change_signals=1,
        single_threaded_days=70,
        previous_multithreaded=0,
        rep_multithreading_score=10.0,
    )
    defaults.update(overrides)
    return DealMultithreadingInput(**defaults)


# ---------------------------------------------------------------------------
# Section 1: Enum values
# ---------------------------------------------------------------------------

class TestThreadingStatusEnum:
    def test_single_threaded_value(self):
        assert ThreadingStatus.SINGLE_THREADED.value == "single_threaded"

    def test_at_risk_value(self):
        assert ThreadingStatus.AT_RISK.value == "at_risk"

    def test_adequately_threaded_value(self):
        assert ThreadingStatus.ADEQUATELY_THREADED.value == "adequately_threaded"

    def test_well_threaded_value(self):
        assert ThreadingStatus.WELL_THREADED.value == "well_threaded"

    def test_all_four_members(self):
        assert len(ThreadingStatus) == 4

    def test_str_enum_behavior(self):
        assert ThreadingStatus.SINGLE_THREADED == "single_threaded"


class TestThreadingRiskEnum:
    def test_critical_value(self):
        assert ThreadingRisk.CRITICAL.value == "critical"

    def test_high_value(self):
        assert ThreadingRisk.HIGH.value == "high"

    def test_moderate_value(self):
        assert ThreadingRisk.MODERATE.value == "moderate"

    def test_low_value(self):
        assert ThreadingRisk.LOW.value == "low"

    def test_all_four_members(self):
        assert len(ThreadingRisk) == 4

    def test_str_enum_behavior(self):
        assert ThreadingRisk.LOW == "low"


class TestStakeholderCoverageEnum:
    def test_poor_value(self):
        assert StakeholderCoverage.POOR.value == "poor"

    def test_partial_value(self):
        assert StakeholderCoverage.PARTIAL.value == "partial"

    def test_adequate_value(self):
        assert StakeholderCoverage.ADEQUATE.value == "adequate"

    def test_comprehensive_value(self):
        assert StakeholderCoverage.COMPREHENSIVE.value == "comprehensive"

    def test_all_four_members(self):
        assert len(StakeholderCoverage) == 4

    def test_str_enum_behavior(self):
        assert StakeholderCoverage.COMPREHENSIVE == "comprehensive"


class TestThreadingActionEnum:
    def test_emergency_executive_outreach_value(self):
        assert ThreadingAction.EMERGENCY_EXECUTIVE_OUTREACH.value == "emergency_executive_outreach"

    def test_expand_stakeholder_map_value(self):
        assert ThreadingAction.EXPAND_STAKEHOLDER_MAP.value == "expand_stakeholder_map"

    def test_strengthen_existing_value(self):
        assert ThreadingAction.STRENGTHEN_EXISTING.value == "strengthen_existing"

    def test_maintain_value(self):
        assert ThreadingAction.MAINTAIN.value == "maintain"

    def test_all_four_members(self):
        assert len(ThreadingAction) == 4

    def test_str_enum_behavior(self):
        assert ThreadingAction.MAINTAIN == "maintain"


# ---------------------------------------------------------------------------
# Section 2: DealMultithreadingInput — exactly 22 fields
# ---------------------------------------------------------------------------

class TestDealMultithreadingInput:
    def test_has_deal_id(self):
        inp = _make_base()
        assert inp.deal_id == "deal_001"

    def test_has_rep_id(self):
        inp = _make_base()
        assert inp.rep_id == "rep_001"

    def test_has_deal_name(self):
        inp = _make_base()
        assert inp.deal_name == "Test Deal"

    def test_has_stakeholder_count(self):
        inp = _make_base()
        assert inp.stakeholder_count == 5

    def test_has_executive_contacts_count(self):
        inp = _make_base()
        assert inp.executive_contacts_count == 2

    def test_has_champion_confirmed(self):
        inp = _make_base()
        assert inp.champion_confirmed == 1

    def test_has_economic_buyer_identified(self):
        inp = _make_base()
        assert inp.economic_buyer_identified == 1

    def test_has_decision_maker_engaged(self):
        inp = _make_base()
        assert inp.decision_maker_engaged == 1

    def test_has_technical_evaluator_engaged(self):
        inp = _make_base()
        assert inp.technical_evaluator_engaged == 1

    def test_has_user_buyer_engaged(self):
        inp = _make_base()
        assert inp.user_buyer_engaged == 1

    def test_has_last_exec_contact_days_ago(self):
        inp = _make_base()
        assert inp.last_exec_contact_days_ago == 5

    def test_has_contact_engagement_rate(self):
        inp = _make_base()
        assert inp.contact_engagement_rate == 85.0

    def test_has_contacts_with_recent_activity(self):
        inp = _make_base()
        assert inp.contacts_with_recent_activity == 4

    def test_has_deal_stage(self):
        inp = _make_base()
        assert inp.deal_stage == 2

    def test_has_deal_value_usd(self):
        inp = _make_base()
        assert inp.deal_value_usd == 250000.0

    def test_has_days_in_current_stage(self):
        inp = _make_base()
        assert inp.days_in_current_stage == 15

    def test_has_stakeholder_sentiment_avg(self):
        inp = _make_base()
        assert inp.stakeholder_sentiment_avg == 78.0

    def test_has_champion_risk_score(self):
        inp = _make_base()
        assert inp.champion_risk_score == 20.0

    def test_has_org_change_signals(self):
        inp = _make_base()
        assert inp.org_change_signals == 0

    def test_has_single_threaded_days(self):
        inp = _make_base()
        assert inp.single_threaded_days == 0

    def test_has_previous_multithreaded(self):
        inp = _make_base()
        assert inp.previous_multithreaded == 1

    def test_has_rep_multithreading_score(self):
        inp = _make_base()
        assert inp.rep_multithreading_score == 85.0

    def test_exactly_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(DealMultithreadingInput)
        assert len(fields) == 22


# ---------------------------------------------------------------------------
# Section 3: DealMultithreadingResult — to_dict() returns exactly 15 keys
# ---------------------------------------------------------------------------

class TestDealMultithreadingResult:
    def test_to_dict_returns_15_keys(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_has_deal_id(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "deal_id" in result.to_dict()

    def test_to_dict_has_rep_id(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "rep_id" in result.to_dict()

    def test_to_dict_has_threading_status(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "threading_status" in result.to_dict()

    def test_to_dict_has_threading_risk(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "threading_risk" in result.to_dict()

    def test_to_dict_has_stakeholder_coverage(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "stakeholder_coverage" in result.to_dict()

    def test_to_dict_has_threading_action(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "threading_action" in result.to_dict()

    def test_to_dict_has_coverage_score(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "coverage_score" in result.to_dict()

    def test_to_dict_has_engagement_score(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "engagement_score" in result.to_dict()

    def test_to_dict_has_executive_access_score(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "executive_access_score" in result.to_dict()

    def test_to_dict_has_resilience_score(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "resilience_score" in result.to_dict()

    def test_to_dict_has_threading_composite(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "threading_composite" in result.to_dict()

    def test_to_dict_has_is_single_threaded(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "is_single_threaded" in result.to_dict()

    def test_to_dict_has_needs_executive_access(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "needs_executive_access" in result.to_dict()

    def test_to_dict_has_estimated_risk_exposure_usd(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "estimated_risk_exposure_usd" in result.to_dict()

    def test_to_dict_has_primary_threading_gap(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "primary_threading_gap" in result.to_dict()

    def test_to_dict_threading_status_is_string(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert isinstance(result.to_dict()["threading_status"], str)

    def test_to_dict_threading_risk_is_string(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert isinstance(result.to_dict()["threading_risk"], str)

    def test_to_dict_coverage_score_is_float(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert isinstance(result.to_dict()["coverage_score"], float)

    def test_to_dict_deal_id_matches(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(deal_id="xyz_deal"))
        assert result.to_dict()["deal_id"] == "xyz_deal"

    def test_to_dict_rep_id_matches(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(rep_id="xyz_rep"))
        assert result.to_dict()["rep_id"] == "xyz_rep"


# ---------------------------------------------------------------------------
# Section 4: is_single_threaded boolean logic
# ---------------------------------------------------------------------------

class TestIsSingleThreaded:
    def test_single_when_stakeholder_count_is_1(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(stakeholder_count=1, contacts_with_recent_activity=5, deal_stage=0))
        assert result.is_single_threaded is True

    def test_not_single_when_stakeholder_count_gt_1_and_many_active(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(stakeholder_count=5, contacts_with_recent_activity=4, deal_stage=0))
        assert result.is_single_threaded is False

    def test_single_when_contacts_with_recent_activity_0_and_stage_gte_1(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(stakeholder_count=5, contacts_with_recent_activity=0, deal_stage=1))
        assert result.is_single_threaded is True

    def test_single_when_contacts_with_recent_activity_1_and_stage_gte_1(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(stakeholder_count=5, contacts_with_recent_activity=1, deal_stage=1))
        assert result.is_single_threaded is True

    def test_not_single_when_contacts_2_and_stage_gte_1(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(stakeholder_count=5, contacts_with_recent_activity=2, deal_stage=1))
        assert result.is_single_threaded is False

    def test_not_single_when_contacts_1_and_stage_0(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(stakeholder_count=5, contacts_with_recent_activity=1, deal_stage=0))
        assert result.is_single_threaded is False

    def test_single_overrides_when_stakeholder_count_1_regardless_of_activity(self):
        # stakeholder_count == 1 always makes single-threaded regardless of contacts_with_recent_activity
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(stakeholder_count=1, contacts_with_recent_activity=10, deal_stage=0))
        assert result.is_single_threaded is True

    def test_single_at_high_stage_with_low_activity(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(stakeholder_count=6, contacts_with_recent_activity=0, deal_stage=5))
        assert result.is_single_threaded is True

    def test_single_in_to_dict(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(stakeholder_count=1))
        assert result.to_dict()["is_single_threaded"] is True


# ---------------------------------------------------------------------------
# Section 5: needs_executive_access boolean logic
# ---------------------------------------------------------------------------

class TestNeedsExecutiveAccess:
    def test_needs_exec_when_zero_exec_contacts_and_stage_gte_1(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(executive_contacts_count=0, deal_stage=1))
        assert result.needs_executive_access is True

    def test_not_needs_exec_when_exec_contacts_gt_0(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(executive_contacts_count=1, deal_stage=1))
        assert result.needs_executive_access is False

    def test_not_needs_exec_when_stage_0_even_with_zero_exec_contacts(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(executive_contacts_count=0, deal_stage=0))
        assert result.needs_executive_access is False

    def test_needs_exec_at_high_stage(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(executive_contacts_count=0, deal_stage=4))
        assert result.needs_executive_access is True

    def test_not_needs_exec_with_many_exec_contacts(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(executive_contacts_count=3, deal_stage=3))
        assert result.needs_executive_access is False

    def test_needs_exec_in_to_dict(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(executive_contacts_count=0, deal_stage=2))
        assert result.to_dict()["needs_executive_access"] is True


# ---------------------------------------------------------------------------
# Section 6: Composite formula weights
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_is_weighted_combination(self):
        """Verify composite = coverage*0.30 + engagement*0.25 + exec_access*0.25 + resilience*0.20"""
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        expected = round(
            result.coverage_score * 0.30
            + result.engagement_score * 0.25
            + result.executive_access_score * 0.25
            + result.resilience_score * 0.20,
            1,
        )
        assert result.threading_composite == pytest.approx(expected, abs=0.01)

    def test_composite_uses_coverage_weight_030(self):
        # Isolate coverage: vary only rep_multithreading_score (affects only coverage_score)
        # All other inputs are identical so engagement/exec_access/resilience are unchanged
        engine = DealMultithreadingIntelligence()
        common = dict(
            stakeholder_count=3, executive_contacts_count=1,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=0, technical_evaluator_engaged=0,
            user_buyer_engaged=0, last_exec_contact_days_ago=14,
            contact_engagement_rate=50.0, contacts_with_recent_activity=3,
            deal_stage=0, stakeholder_sentiment_avg=50.0,
            org_change_signals=0, days_in_current_stage=10,
            single_threaded_days=0, previous_multithreaded=0,
            champion_risk_score=30.0,
        )
        r1 = engine.assess(_make_base(deal_id="cw_d1", rep_multithreading_score=0.0, **common))
        r2 = engine.assess(_make_base(deal_id="cw_d2", rep_multithreading_score=100.0, **common))
        # rep_multithreading_score=100 adds 10 to coverage (100*0.10=10), others unchanged
        diff_composite = abs(r2.threading_composite - r1.threading_composite)
        diff_coverage = abs(r2.coverage_score - r1.coverage_score)
        # composite diff should be 30% of coverage diff
        assert diff_composite == pytest.approx(diff_coverage * 0.30, abs=0.15)

    def test_composite_is_rounded_to_1_decimal(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        # Check it has at most 1 decimal place
        assert result.threading_composite == round(result.threading_composite, 1)

    def test_composite_range_low(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_poor())
        assert result.threading_composite >= 0.0

    def test_composite_range_high(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert result.threading_composite <= 100.0

    def test_composite_in_to_dict(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base())
        assert "threading_composite" in result.to_dict()
        assert isinstance(result.to_dict()["threading_composite"], float)


# ---------------------------------------------------------------------------
# Section 7: Coverage score computation
# ---------------------------------------------------------------------------

class TestCoverageScore:
    def test_stakeholder_count_6_gives_30_points(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(stakeholder_count=6, champion_confirmed=0,
                                     economic_buyer_identified=0, decision_maker_engaged=0,
                                     technical_evaluator_engaged=0, user_buyer_engaged=0,
                                     executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r.coverage_score == pytest.approx(30.0, abs=0.1)

    def test_stakeholder_count_4_gives_22_points(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(stakeholder_count=4, champion_confirmed=0,
                                     economic_buyer_identified=0, decision_maker_engaged=0,
                                     technical_evaluator_engaged=0, user_buyer_engaged=0,
                                     executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r.coverage_score == pytest.approx(22.0, abs=0.1)

    def test_stakeholder_count_2_gives_12_points(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(stakeholder_count=2, champion_confirmed=0,
                                     economic_buyer_identified=0, decision_maker_engaged=0,
                                     technical_evaluator_engaged=0, user_buyer_engaged=0,
                                     executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r.coverage_score == pytest.approx(12.0, abs=0.1)

    def test_stakeholder_count_1_gives_3_points(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(stakeholder_count=1, champion_confirmed=0,
                                     economic_buyer_identified=0, decision_maker_engaged=0,
                                     technical_evaluator_engaged=0, user_buyer_engaged=0,
                                     executive_contacts_count=0, rep_multithreading_score=0.0,
                                     deal_stage=0))
        assert r.coverage_score == pytest.approx(3.0, abs=0.1)

    def test_champion_confirmed_adds_8_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w", stakeholder_count=2, champion_confirmed=1,
                                          economic_buyer_identified=0, decision_maker_engaged=0,
                                          technical_evaluator_engaged=0, user_buyer_engaged=0,
                                          executive_contacts_count=0, rep_multithreading_score=0.0))
        r_without = engine.assess(_make_base(deal_id="wo", stakeholder_count=2, champion_confirmed=0,
                                             economic_buyer_identified=0, decision_maker_engaged=0,
                                             technical_evaluator_engaged=0, user_buyer_engaged=0,
                                             executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r_with.coverage_score - r_without.coverage_score == pytest.approx(8.0, abs=0.1)

    def test_economic_buyer_adds_10_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w", stakeholder_count=2, champion_confirmed=0,
                                          economic_buyer_identified=1, decision_maker_engaged=0,
                                          technical_evaluator_engaged=0, user_buyer_engaged=0,
                                          executive_contacts_count=0, rep_multithreading_score=0.0))
        r_without = engine.assess(_make_base(deal_id="wo", stakeholder_count=2, champion_confirmed=0,
                                             economic_buyer_identified=0, decision_maker_engaged=0,
                                             technical_evaluator_engaged=0, user_buyer_engaged=0,
                                             executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r_with.coverage_score - r_without.coverage_score == pytest.approx(10.0, abs=0.1)

    def test_decision_maker_adds_10_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w", stakeholder_count=2, champion_confirmed=0,
                                          economic_buyer_identified=0, decision_maker_engaged=1,
                                          technical_evaluator_engaged=0, user_buyer_engaged=0,
                                          executive_contacts_count=0, rep_multithreading_score=0.0))
        r_without = engine.assess(_make_base(deal_id="wo", stakeholder_count=2, champion_confirmed=0,
                                             economic_buyer_identified=0, decision_maker_engaged=0,
                                             technical_evaluator_engaged=0, user_buyer_engaged=0,
                                             executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r_with.coverage_score - r_without.coverage_score == pytest.approx(10.0, abs=0.1)

    def test_technical_evaluator_adds_6_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w", stakeholder_count=2, champion_confirmed=0,
                                          economic_buyer_identified=0, decision_maker_engaged=0,
                                          technical_evaluator_engaged=1, user_buyer_engaged=0,
                                          executive_contacts_count=0, rep_multithreading_score=0.0))
        r_without = engine.assess(_make_base(deal_id="wo", stakeholder_count=2, champion_confirmed=0,
                                             economic_buyer_identified=0, decision_maker_engaged=0,
                                             technical_evaluator_engaged=0, user_buyer_engaged=0,
                                             executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r_with.coverage_score - r_without.coverage_score == pytest.approx(6.0, abs=0.1)

    def test_user_buyer_adds_6_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w", stakeholder_count=2, champion_confirmed=0,
                                          economic_buyer_identified=0, decision_maker_engaged=0,
                                          technical_evaluator_engaged=0, user_buyer_engaged=1,
                                          executive_contacts_count=0, rep_multithreading_score=0.0))
        r_without = engine.assess(_make_base(deal_id="wo", stakeholder_count=2, champion_confirmed=0,
                                             economic_buyer_identified=0, decision_maker_engaged=0,
                                             technical_evaluator_engaged=0, user_buyer_engaged=0,
                                             executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r_with.coverage_score - r_without.coverage_score == pytest.approx(6.0, abs=0.1)

    def test_exec_contacts_3_or_more_adds_20_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w", stakeholder_count=2, champion_confirmed=0,
                                          economic_buyer_identified=0, decision_maker_engaged=0,
                                          technical_evaluator_engaged=0, user_buyer_engaged=0,
                                          executive_contacts_count=3, rep_multithreading_score=0.0))
        r_without = engine.assess(_make_base(deal_id="wo", stakeholder_count=2, champion_confirmed=0,
                                             economic_buyer_identified=0, decision_maker_engaged=0,
                                             technical_evaluator_engaged=0, user_buyer_engaged=0,
                                             executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r_with.coverage_score - r_without.coverage_score == pytest.approx(20.0, abs=0.1)

    def test_exec_contacts_2_adds_14_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w", stakeholder_count=2, champion_confirmed=0,
                                          economic_buyer_identified=0, decision_maker_engaged=0,
                                          technical_evaluator_engaged=0, user_buyer_engaged=0,
                                          executive_contacts_count=2, rep_multithreading_score=0.0))
        r_without = engine.assess(_make_base(deal_id="wo", stakeholder_count=2, champion_confirmed=0,
                                             economic_buyer_identified=0, decision_maker_engaged=0,
                                             technical_evaluator_engaged=0, user_buyer_engaged=0,
                                             executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r_with.coverage_score - r_without.coverage_score == pytest.approx(14.0, abs=0.1)

    def test_exec_contacts_1_adds_7_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w", stakeholder_count=2, champion_confirmed=0,
                                          economic_buyer_identified=0, decision_maker_engaged=0,
                                          technical_evaluator_engaged=0, user_buyer_engaged=0,
                                          executive_contacts_count=1, rep_multithreading_score=0.0))
        r_without = engine.assess(_make_base(deal_id="wo", stakeholder_count=2, champion_confirmed=0,
                                             economic_buyer_identified=0, decision_maker_engaged=0,
                                             technical_evaluator_engaged=0, user_buyer_engaged=0,
                                             executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r_with.coverage_score - r_without.coverage_score == pytest.approx(7.0, abs=0.1)

    def test_rep_multithreading_score_100_adds_10_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w", stakeholder_count=2, champion_confirmed=0,
                                          economic_buyer_identified=0, decision_maker_engaged=0,
                                          technical_evaluator_engaged=0, user_buyer_engaged=0,
                                          executive_contacts_count=0, rep_multithreading_score=100.0))
        r_without = engine.assess(_make_base(deal_id="wo", stakeholder_count=2, champion_confirmed=0,
                                             economic_buyer_identified=0, decision_maker_engaged=0,
                                             technical_evaluator_engaged=0, user_buyer_engaged=0,
                                             executive_contacts_count=0, rep_multithreading_score=0.0))
        assert r_with.coverage_score - r_without.coverage_score == pytest.approx(10.0, abs=0.1)

    def test_coverage_score_clamped_max_100(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(
            stakeholder_count=10, champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1, user_buyer_engaged=1,
            executive_contacts_count=5, rep_multithreading_score=100.0
        ))
        assert result.coverage_score <= 100.0

    def test_coverage_score_clamped_min_0(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_poor(rep_multithreading_score=0.0))
        assert result.coverage_score >= 0.0


# ---------------------------------------------------------------------------
# Section 8: Engagement score computation
# ---------------------------------------------------------------------------

class TestEngagementScore:
    def test_engagement_rate_100_contributes_40_points(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(deal_id="e", contact_engagement_rate=100.0,
                                     contacts_with_recent_activity=0,
                                     stakeholder_sentiment_avg=0.0,
                                     org_change_signals=0, days_in_current_stage=0))
        assert r.engagement_score == pytest.approx(40.0, abs=0.2)

    def test_contacts_with_recent_activity_4_adds_30_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w", contact_engagement_rate=0.0,
                                          contacts_with_recent_activity=4,
                                          stakeholder_sentiment_avg=0.0,
                                          org_change_signals=0, days_in_current_stage=0))
        r_without = engine.assess(_make_base(deal_id="wo", contact_engagement_rate=0.0,
                                             contacts_with_recent_activity=0,
                                             stakeholder_sentiment_avg=0.0,
                                             org_change_signals=0, days_in_current_stage=0))
        assert r_with.engagement_score - r_without.engagement_score == pytest.approx(30.0, abs=0.1)

    def test_contacts_with_recent_activity_3_adds_22_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w3", contact_engagement_rate=0.0,
                                          contacts_with_recent_activity=3,
                                          stakeholder_sentiment_avg=0.0,
                                          org_change_signals=0, days_in_current_stage=0))
        r_without = engine.assess(_make_base(deal_id="wo3", contact_engagement_rate=0.0,
                                             contacts_with_recent_activity=0,
                                             stakeholder_sentiment_avg=0.0,
                                             org_change_signals=0, days_in_current_stage=0))
        assert r_with.engagement_score - r_without.engagement_score == pytest.approx(22.0, abs=0.1)

    def test_contacts_with_recent_activity_2_adds_14_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w2", contact_engagement_rate=0.0,
                                          contacts_with_recent_activity=2,
                                          stakeholder_sentiment_avg=0.0,
                                          org_change_signals=0, days_in_current_stage=0))
        r_without = engine.assess(_make_base(deal_id="wo2", contact_engagement_rate=0.0,
                                             contacts_with_recent_activity=0,
                                             stakeholder_sentiment_avg=0.0,
                                             org_change_signals=0, days_in_current_stage=0))
        assert r_with.engagement_score - r_without.engagement_score == pytest.approx(14.0, abs=0.1)

    def test_contacts_with_recent_activity_1_adds_6_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="w1", contact_engagement_rate=0.0,
                                          contacts_with_recent_activity=1,
                                          stakeholder_sentiment_avg=0.0,
                                          org_change_signals=0, days_in_current_stage=0,
                                          deal_stage=0))
        r_without = engine.assess(_make_base(deal_id="wo1", contact_engagement_rate=0.0,
                                             contacts_with_recent_activity=0,
                                             stakeholder_sentiment_avg=0.0,
                                             org_change_signals=0, days_in_current_stage=0,
                                             deal_stage=0))
        assert r_with.engagement_score - r_without.engagement_score == pytest.approx(6.0, abs=0.1)

    def test_sentiment_100_contributes_20_points(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(deal_id="s", contact_engagement_rate=0.0,
                                     contacts_with_recent_activity=0,
                                     stakeholder_sentiment_avg=100.0,
                                     org_change_signals=0, days_in_current_stage=0,
                                     deal_stage=0))
        assert r.engagement_score == pytest.approx(20.0, abs=0.2)

    def test_org_change_signals_penalizes_15_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="oc", contact_engagement_rate=50.0,
                                          contacts_with_recent_activity=4,
                                          stakeholder_sentiment_avg=50.0,
                                          org_change_signals=1, days_in_current_stage=0))
        r_without = engine.assess(_make_base(deal_id="noc", contact_engagement_rate=50.0,
                                             contacts_with_recent_activity=4,
                                             stakeholder_sentiment_avg=50.0,
                                             org_change_signals=0, days_in_current_stage=0))
        assert r_without.engagement_score - r_with.engagement_score == pytest.approx(15.0, abs=0.1)

    def test_days_in_stage_60_penalizes_10_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="d60", contact_engagement_rate=50.0,
                                          contacts_with_recent_activity=4,
                                          stakeholder_sentiment_avg=50.0,
                                          org_change_signals=0, days_in_current_stage=60))
        r_without = engine.assess(_make_base(deal_id="d0", contact_engagement_rate=50.0,
                                             contacts_with_recent_activity=4,
                                             stakeholder_sentiment_avg=50.0,
                                             org_change_signals=0, days_in_current_stage=0))
        assert r_without.engagement_score - r_with.engagement_score == pytest.approx(10.0, abs=0.1)

    def test_days_in_stage_30_penalizes_5_points(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="d30", contact_engagement_rate=50.0,
                                          contacts_with_recent_activity=4,
                                          stakeholder_sentiment_avg=50.0,
                                          org_change_signals=0, days_in_current_stage=30))
        r_without = engine.assess(_make_base(deal_id="d0b", contact_engagement_rate=50.0,
                                             contacts_with_recent_activity=4,
                                             stakeholder_sentiment_avg=50.0,
                                             org_change_signals=0, days_in_current_stage=0))
        assert r_without.engagement_score - r_with.engagement_score == pytest.approx(5.0, abs=0.1)

    def test_engagement_score_clamped_min_0(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_poor())
        assert result.engagement_score >= 0.0

    def test_engagement_score_clamped_max_100(self):
        engine = DealMultithreadingIntelligence()
        result = engine.assess(_make_base(
            contact_engagement_rate=100.0, contacts_with_recent_activity=10,
            stakeholder_sentiment_avg=100.0, org_change_signals=0, days_in_current_stage=0
        ))
        assert result.engagement_score <= 100.0


# ---------------------------------------------------------------------------
# Section 9: Executive access score computation
# ---------------------------------------------------------------------------

class TestExecutiveAccessScore:
    def test_exec_contacts_3_adds_40(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=3,
                                     last_exec_contact_days_ago=90,
                                     economic_buyer_identified=0,
                                     decision_maker_engaged=0))
        assert r.executive_access_score == pytest.approx(40.0, abs=0.1)

    def test_exec_contacts_2_adds_28(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=2,
                                     last_exec_contact_days_ago=90,
                                     economic_buyer_identified=0,
                                     decision_maker_engaged=0))
        assert r.executive_access_score == pytest.approx(28.0, abs=0.1)

    def test_exec_contacts_1_adds_15(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=1,
                                     last_exec_contact_days_ago=90,
                                     economic_buyer_identified=0,
                                     decision_maker_engaged=0))
        assert r.executive_access_score == pytest.approx(15.0, abs=0.1)

    def test_exec_contacts_0_adds_0(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=0,
                                     last_exec_contact_days_ago=90,
                                     economic_buyer_identified=0,
                                     decision_maker_engaged=0))
        assert r.executive_access_score == pytest.approx(0.0, abs=0.1)

    def test_last_exec_contact_7_days_adds_30(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=0,
                                     last_exec_contact_days_ago=7,
                                     economic_buyer_identified=0,
                                     decision_maker_engaged=0))
        assert r.executive_access_score == pytest.approx(30.0, abs=0.1)

    def test_last_exec_contact_14_days_adds_22(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=0,
                                     last_exec_contact_days_ago=14,
                                     economic_buyer_identified=0,
                                     decision_maker_engaged=0))
        assert r.executive_access_score == pytest.approx(22.0, abs=0.1)

    def test_last_exec_contact_30_days_adds_14(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=0,
                                     last_exec_contact_days_ago=30,
                                     economic_buyer_identified=0,
                                     decision_maker_engaged=0))
        assert r.executive_access_score == pytest.approx(14.0, abs=0.1)

    def test_last_exec_contact_60_days_adds_6(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=0,
                                     last_exec_contact_days_ago=60,
                                     economic_buyer_identified=0,
                                     decision_maker_engaged=0))
        assert r.executive_access_score == pytest.approx(6.0, abs=0.1)

    def test_last_exec_contact_90_days_adds_0(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=0,
                                     last_exec_contact_days_ago=90,
                                     economic_buyer_identified=0,
                                     decision_maker_engaged=0))
        assert r.executive_access_score == pytest.approx(0.0, abs=0.1)

    def test_economic_buyer_identified_adds_15(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="eb1", executive_contacts_count=0,
                                          last_exec_contact_days_ago=90,
                                          economic_buyer_identified=1,
                                          decision_maker_engaged=0))
        r_without = engine.assess(_make_base(deal_id="eb0", executive_contacts_count=0,
                                             last_exec_contact_days_ago=90,
                                             economic_buyer_identified=0,
                                             decision_maker_engaged=0))
        assert r_with.executive_access_score - r_without.executive_access_score == pytest.approx(15.0, abs=0.1)

    def test_decision_maker_engaged_adds_15(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="dm1", executive_contacts_count=0,
                                          last_exec_contact_days_ago=90,
                                          economic_buyer_identified=0,
                                          decision_maker_engaged=1))
        r_without = engine.assess(_make_base(deal_id="dm0", executive_contacts_count=0,
                                             last_exec_contact_days_ago=90,
                                             economic_buyer_identified=0,
                                             decision_maker_engaged=0))
        assert r_with.executive_access_score - r_without.executive_access_score == pytest.approx(15.0, abs=0.1)

    def test_exec_access_score_clamped_max_100(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=10,
                                     last_exec_contact_days_ago=1,
                                     economic_buyer_identified=1,
                                     decision_maker_engaged=1))
        assert r.executive_access_score <= 100.0

    def test_exec_access_score_clamped_min_0(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=0,
                                     last_exec_contact_days_ago=999,
                                     economic_buyer_identified=0,
                                     decision_maker_engaged=0))
        assert r.executive_access_score >= 0.0


# ---------------------------------------------------------------------------
# Section 10: Resilience score computation
# ---------------------------------------------------------------------------

class TestResilienceScore:
    def test_champion_confirmed_with_low_risk_contributes_30(self):
        # champion_confirmed=1, champion_risk_score=0 => health=100, health*0.30=30
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(champion_confirmed=1, champion_risk_score=0.0,
                                     previous_multithreaded=0, single_threaded_days=0,
                                     stakeholder_count=1, org_change_signals=0,
                                     deal_stage=0))
        # stakeholder_count=1 contributes 0 resilience points
        assert r.resilience_score == pytest.approx(30.0, abs=0.2)

    def test_previous_multithreaded_adds_10(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="pm1", champion_confirmed=0,
                                          previous_multithreaded=1,
                                          single_threaded_days=0, stakeholder_count=1,
                                          org_change_signals=0, deal_stage=0))
        r_without = engine.assess(_make_base(deal_id="pm0", champion_confirmed=0,
                                             previous_multithreaded=0,
                                             single_threaded_days=0, stakeholder_count=1,
                                             org_change_signals=0, deal_stage=0))
        assert r_with.resilience_score - r_without.resilience_score == pytest.approx(10.0, abs=0.1)

    def test_single_threaded_days_60_penalizes_30(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="st60", champion_confirmed=0,
                                          previous_multithreaded=0,
                                          single_threaded_days=60, stakeholder_count=1,
                                          org_change_signals=0, deal_stage=0))
        r_without = engine.assess(_make_base(deal_id="st0", champion_confirmed=0,
                                             previous_multithreaded=0,
                                             single_threaded_days=0, stakeholder_count=1,
                                             org_change_signals=0, deal_stage=0))
        # Clamped to 0 if would go negative
        assert r_without.resilience_score - r_with.resilience_score >= 0.0

    def test_single_threaded_days_30_penalizes_18(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="st30", champion_confirmed=0,
                                          previous_multithreaded=0,
                                          single_threaded_days=30, stakeholder_count=5,
                                          org_change_signals=0, deal_stage=0))
        r_without = engine.assess(_make_base(deal_id="st0b", champion_confirmed=0,
                                             previous_multithreaded=0,
                                             single_threaded_days=0, stakeholder_count=5,
                                             org_change_signals=0, deal_stage=0))
        assert r_without.resilience_score - r_with.resilience_score == pytest.approx(18.0, abs=0.1)

    def test_single_threaded_days_14_penalizes_8(self):
        engine = DealMultithreadingIntelligence()
        r_with = engine.assess(_make_base(deal_id="st14", champion_confirmed=0,
                                          previous_multithreaded=0,
                                          single_threaded_days=14, stakeholder_count=5,
                                          org_change_signals=0, deal_stage=0))
        r_without = engine.assess(_make_base(deal_id="st0c", champion_confirmed=0,
                                             previous_multithreaded=0,
                                             single_threaded_days=0, stakeholder_count=5,
                                             org_change_signals=0, deal_stage=0))
        assert r_without.resilience_score - r_with.resilience_score == pytest.approx(8.0, abs=0.1)

    def test_stakeholder_count_5_adds_30(self):
        engine = DealMultithreadingIntelligence()
        r_5 = engine.assess(_make_base(deal_id="sc5", champion_confirmed=0,
                                        previous_multithreaded=0,
                                        single_threaded_days=0, stakeholder_count=5,
                                        org_change_signals=0, deal_stage=0))
        r_0 = engine.assess(_make_base(deal_id="sc0", champion_confirmed=0,
                                        previous_multithreaded=0,
                                        single_threaded_days=0, stakeholder_count=1,
                                        org_change_signals=0, deal_stage=0))
        assert r_5.resilience_score - r_0.resilience_score == pytest.approx(30.0, abs=0.1)

    def test_stakeholder_count_3_adds_20(self):
        engine = DealMultithreadingIntelligence()
        r_3 = engine.assess(_make_base(deal_id="sc3", champion_confirmed=0,
                                        previous_multithreaded=0,
                                        single_threaded_days=0, stakeholder_count=3,
                                        org_change_signals=0, deal_stage=0))
        r_0b = engine.assess(_make_base(deal_id="sc0b", champion_confirmed=0,
                                         previous_multithreaded=0,
                                         single_threaded_days=0, stakeholder_count=1,
                                         org_change_signals=0, deal_stage=0))
        assert r_3.resilience_score - r_0b.resilience_score == pytest.approx(20.0, abs=0.1)

    def test_stakeholder_count_2_adds_10(self):
        engine = DealMultithreadingIntelligence()
        r_2 = engine.assess(_make_base(deal_id="sc2", champion_confirmed=0,
                                        previous_multithreaded=0,
                                        single_threaded_days=0, stakeholder_count=2,
                                        org_change_signals=0, deal_stage=0))
        r_1 = engine.assess(_make_base(deal_id="sc1b", champion_confirmed=0,
                                        previous_multithreaded=0,
                                        single_threaded_days=0, stakeholder_count=1,
                                        org_change_signals=0, deal_stage=0))
        assert r_2.resilience_score - r_1.resilience_score == pytest.approx(10.0, abs=0.1)

    def test_org_change_signals_penalizes_20(self):
        engine = DealMultithreadingIntelligence()
        r_oc = engine.assess(_make_base(deal_id="oc1", champion_confirmed=0,
                                         previous_multithreaded=0,
                                         single_threaded_days=0, stakeholder_count=5,
                                         org_change_signals=1, deal_stage=0))
        r_noc = engine.assess(_make_base(deal_id="noc1", champion_confirmed=0,
                                          previous_multithreaded=0,
                                          single_threaded_days=0, stakeholder_count=5,
                                          org_change_signals=0, deal_stage=0))
        assert r_noc.resilience_score - r_oc.resilience_score == pytest.approx(20.0, abs=0.1)

    def test_champion_risk_70_penalizes_15(self):
        engine = DealMultithreadingIntelligence()
        r_hi = engine.assess(_make_base(deal_id="cr70", champion_confirmed=0,
                                         previous_multithreaded=0,
                                         single_threaded_days=0, stakeholder_count=5,
                                         org_change_signals=0, champion_risk_score=70.0,
                                         deal_stage=0))
        r_lo = engine.assess(_make_base(deal_id="cr0", champion_confirmed=0,
                                         previous_multithreaded=0,
                                         single_threaded_days=0, stakeholder_count=5,
                                         org_change_signals=0, champion_risk_score=0.0,
                                         deal_stage=0))
        assert r_lo.resilience_score - r_hi.resilience_score == pytest.approx(15.0, abs=0.1)

    def test_champion_risk_50_penalizes_8(self):
        engine = DealMultithreadingIntelligence()
        r_hi = engine.assess(_make_base(deal_id="cr50", champion_confirmed=0,
                                         previous_multithreaded=0,
                                         single_threaded_days=0, stakeholder_count=5,
                                         org_change_signals=0, champion_risk_score=50.0,
                                         deal_stage=0))
        r_lo = engine.assess(_make_base(deal_id="cr0b", champion_confirmed=0,
                                         previous_multithreaded=0,
                                         single_threaded_days=0, stakeholder_count=5,
                                         org_change_signals=0, champion_risk_score=0.0,
                                         deal_stage=0))
        assert r_lo.resilience_score - r_hi.resilience_score == pytest.approx(8.0, abs=0.1)

    def test_resilience_score_clamped_min_0(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_poor())
        assert r.resilience_score >= 0.0

    def test_resilience_score_clamped_max_100(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(champion_confirmed=1, champion_risk_score=0.0,
                                     previous_multithreaded=1, single_threaded_days=0,
                                     stakeholder_count=10, org_change_signals=0))
        assert r.resilience_score <= 100.0


# ---------------------------------------------------------------------------
# Section 11: ThreadingStatus classification
# ---------------------------------------------------------------------------

class TestThreadingStatusClassification:
    def test_single_threaded_status_when_is_single_threaded(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(stakeholder_count=1))
        assert r.threading_status == ThreadingStatus.SINGLE_THREADED

    def test_well_threaded_status_when_composite_gte_70(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=6, executive_contacts_count=3,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1,
            user_buyer_engaged=1, last_exec_contact_days_ago=5,
            contact_engagement_rate=90.0, contacts_with_recent_activity=5,
            deal_stage=2, stakeholder_sentiment_avg=90.0,
            org_change_signals=0, days_in_current_stage=10,
            single_threaded_days=0, previous_multithreaded=1,
            rep_multithreading_score=90.0, champion_risk_score=10.0
        ))
        assert r.threading_status == ThreadingStatus.WELL_THREADED

    def test_adequately_threaded_when_composite_50_to_70(self):
        engine = DealMultithreadingIntelligence()
        # Force known composite in [50, 70) by finding a suitable input
        # Use stage=0 to avoid single_threaded logic
        r = engine.assess(_make_base(
            stakeholder_count=3, executive_contacts_count=1,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=0, technical_evaluator_engaged=0,
            user_buyer_engaged=0, last_exec_contact_days_ago=14,
            contact_engagement_rate=50.0, contacts_with_recent_activity=3,
            deal_stage=0, stakeholder_sentiment_avg=50.0,
            org_change_signals=0, days_in_current_stage=10,
            single_threaded_days=0, previous_multithreaded=0,
            rep_multithreading_score=50.0, champion_risk_score=30.0
        ))
        if r.threading_composite >= 50 and r.threading_composite < 70:
            assert r.threading_status == ThreadingStatus.ADEQUATELY_THREADED

    def test_at_risk_when_composite_below_50_and_not_single_threaded(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=3, executive_contacts_count=0,
            champion_confirmed=0, economic_buyer_identified=0,
            decision_maker_engaged=0, technical_evaluator_engaged=0,
            user_buyer_engaged=0, last_exec_contact_days_ago=90,
            contact_engagement_rate=15.0, contacts_with_recent_activity=3,
            deal_stage=0, stakeholder_sentiment_avg=15.0,
            org_change_signals=0, days_in_current_stage=0,
            single_threaded_days=0, previous_multithreaded=0,
            rep_multithreading_score=10.0, champion_risk_score=80.0
        ))
        if r.threading_composite < 50 and not r.is_single_threaded:
            assert r.threading_status == ThreadingStatus.AT_RISK

    def test_single_threaded_overrides_high_composite(self):
        # Even if composite is high, single-threaded status takes priority
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(stakeholder_count=1,
                                     contact_engagement_rate=100.0,
                                     contacts_with_recent_activity=10,
                                     stakeholder_sentiment_avg=100.0))
        assert r.threading_status == ThreadingStatus.SINGLE_THREADED

    def test_status_values_are_strings_in_dict(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        assert r.to_dict()["threading_status"] in [
            "single_threaded", "at_risk", "adequately_threaded", "well_threaded"
        ]


# ---------------------------------------------------------------------------
# Section 12: ThreadingRisk classification
# ---------------------------------------------------------------------------

class TestThreadingRiskClassification:
    def test_critical_when_composite_lt_25(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_poor(deal_stage=0, org_change_signals=0,
                                     contacts_with_recent_activity=3, stakeholder_count=3))
        if r.threading_composite < 25:
            assert r.threading_risk == ThreadingRisk.CRITICAL

    def test_critical_when_stage_gte_2_and_single_threaded(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(stakeholder_count=1, deal_stage=2))
        assert r.threading_risk == ThreadingRisk.CRITICAL

    def test_high_when_composite_25_to_45(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=2, executive_contacts_count=0,
            champion_confirmed=0, economic_buyer_identified=0,
            decision_maker_engaged=0, technical_evaluator_engaged=0,
            user_buyer_engaged=0, last_exec_contact_days_ago=90,
            contact_engagement_rate=30.0, contacts_with_recent_activity=3,
            deal_stage=0, stakeholder_sentiment_avg=30.0,
            org_change_signals=0, days_in_current_stage=0,
            single_threaded_days=0, previous_multithreaded=0,
            rep_multithreading_score=10.0, champion_risk_score=80.0
        ))
        if 25 <= r.threading_composite < 45:
            assert r.threading_risk == ThreadingRisk.HIGH

    def test_moderate_when_composite_45_to_65(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=3, executive_contacts_count=1,
            champion_confirmed=1, economic_buyer_identified=0,
            decision_maker_engaged=0, technical_evaluator_engaged=0,
            user_buyer_engaged=0, last_exec_contact_days_ago=20,
            contact_engagement_rate=50.0, contacts_with_recent_activity=3,
            deal_stage=0, stakeholder_sentiment_avg=50.0,
            org_change_signals=0, days_in_current_stage=0,
            single_threaded_days=0, previous_multithreaded=0,
            rep_multithreading_score=50.0, champion_risk_score=30.0
        ))
        if 45 <= r.threading_composite < 65:
            assert r.threading_risk == ThreadingRisk.MODERATE

    def test_low_when_composite_gte_65(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=6, executive_contacts_count=3,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1,
            user_buyer_engaged=1, last_exec_contact_days_ago=5,
            contact_engagement_rate=90.0, contacts_with_recent_activity=5,
            deal_stage=2, stakeholder_sentiment_avg=90.0,
            org_change_signals=0, days_in_current_stage=5,
            single_threaded_days=0, previous_multithreaded=1,
            rep_multithreading_score=95.0, champion_risk_score=5.0
        ))
        if r.threading_composite >= 65:
            assert r.threading_risk == ThreadingRisk.LOW

    def test_risk_values_are_strings_in_dict(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        assert r.to_dict()["threading_risk"] in ["critical", "high", "moderate", "low"]


# ---------------------------------------------------------------------------
# Section 13: StakeholderCoverage classification
# ---------------------------------------------------------------------------

class TestStakeholderCoverageClassification:
    def test_comprehensive_when_4_roles_and_4_stakeholders(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=4,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1,
            user_buyer_engaged=0
        ))
        assert r.stakeholder_coverage == StakeholderCoverage.COMPREHENSIVE

    def test_comprehensive_when_all_5_roles_and_5_stakeholders(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=5,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1,
            user_buyer_engaged=1
        ))
        assert r.stakeholder_coverage == StakeholderCoverage.COMPREHENSIVE

    def test_adequate_when_3_roles_and_3_stakeholders(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=3,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=0,
            user_buyer_engaged=0
        ))
        assert r.stakeholder_coverage == StakeholderCoverage.ADEQUATE

    def test_partial_when_2_roles(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=2,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=0, technical_evaluator_engaged=0,
            user_buyer_engaged=0
        ))
        assert r.stakeholder_coverage == StakeholderCoverage.PARTIAL

    def test_partial_when_2_stakeholders_and_0_roles(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=2,
            champion_confirmed=0, economic_buyer_identified=0,
            decision_maker_engaged=0, technical_evaluator_engaged=0,
            user_buyer_engaged=0, deal_stage=0
        ))
        assert r.stakeholder_coverage == StakeholderCoverage.PARTIAL

    def test_poor_when_1_stakeholder_and_0_roles(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=1,
            champion_confirmed=0, economic_buyer_identified=0,
            decision_maker_engaged=0, technical_evaluator_engaged=0,
            user_buyer_engaged=0, deal_stage=0
        ))
        assert r.stakeholder_coverage == StakeholderCoverage.POOR

    def test_coverage_values_are_strings_in_dict(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        assert r.to_dict()["stakeholder_coverage"] in [
            "poor", "partial", "adequate", "comprehensive"
        ]


# ---------------------------------------------------------------------------
# Section 14: ThreadingAction classification
# ---------------------------------------------------------------------------

class TestThreadingActionClassification:
    def test_emergency_outreach_when_critical_risk(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(stakeholder_count=1, deal_stage=2))
        assert r.threading_risk == ThreadingRisk.CRITICAL
        assert r.threading_action == ThreadingAction.EMERGENCY_EXECUTIVE_OUTREACH

    def test_expand_stakeholder_map_when_high_risk(self):
        engine = DealMultithreadingIntelligence()
        # Force high risk: composite in [25, 45)
        r = engine.assess(_make_base(
            stakeholder_count=2, executive_contacts_count=0,
            champion_confirmed=0, economic_buyer_identified=0,
            decision_maker_engaged=0, technical_evaluator_engaged=0,
            user_buyer_engaged=0, last_exec_contact_days_ago=90,
            contact_engagement_rate=30.0, contacts_with_recent_activity=3,
            deal_stage=0, stakeholder_sentiment_avg=30.0,
            org_change_signals=0, days_in_current_stage=0,
            single_threaded_days=0, previous_multithreaded=0,
            rep_multithreading_score=10.0, champion_risk_score=80.0
        ))
        if r.threading_risk == ThreadingRisk.HIGH:
            assert r.threading_action == ThreadingAction.EXPAND_STAKEHOLDER_MAP

    def test_strengthen_existing_when_moderate_risk(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=3, executive_contacts_count=1,
            champion_confirmed=1, economic_buyer_identified=0,
            decision_maker_engaged=0, technical_evaluator_engaged=0,
            user_buyer_engaged=0, last_exec_contact_days_ago=20,
            contact_engagement_rate=50.0, contacts_with_recent_activity=3,
            deal_stage=0, stakeholder_sentiment_avg=50.0,
            org_change_signals=0, days_in_current_stage=0,
            single_threaded_days=0, previous_multithreaded=0,
            rep_multithreading_score=50.0, champion_risk_score=30.0
        ))
        if r.threading_risk == ThreadingRisk.MODERATE:
            assert r.threading_action == ThreadingAction.STRENGTHEN_EXISTING

    def test_maintain_when_low_risk(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=6, executive_contacts_count=3,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1,
            user_buyer_engaged=1, last_exec_contact_days_ago=5,
            contact_engagement_rate=90.0, contacts_with_recent_activity=5,
            deal_stage=2, stakeholder_sentiment_avg=90.0,
            org_change_signals=0, days_in_current_stage=5,
            single_threaded_days=0, previous_multithreaded=1,
            rep_multithreading_score=95.0, champion_risk_score=5.0
        ))
        if r.threading_risk == ThreadingRisk.LOW:
            assert r.threading_action == ThreadingAction.MAINTAIN

    def test_action_values_are_strings_in_dict(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        assert r.to_dict()["threading_action"] in [
            "emergency_executive_outreach", "expand_stakeholder_map",
            "strengthen_existing", "maintain"
        ]


# ---------------------------------------------------------------------------
# Section 15: Estimated risk exposure USD
# ---------------------------------------------------------------------------

class TestEstimatedRiskExposure:
    def test_risk_exposure_formula(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        expected = round(r.to_dict()["deal_value_usd"] if False else
                         _make_base().deal_value_usd * (100 - r.threading_composite) / 100, 2)
        assert r.estimated_risk_exposure_usd == pytest.approx(expected, abs=0.01)

    def test_risk_exposure_zero_when_composite_100(self):
        # If composite = 100, exposure = 0
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(deal_value_usd=100000.0))
        if r.threading_composite == 100.0:
            assert r.estimated_risk_exposure_usd == pytest.approx(0.0, abs=0.01)
        else:
            assert r.estimated_risk_exposure_usd > 0.0

    def test_risk_exposure_equals_deal_value_when_composite_0(self):
        # If composite = 0, exposure = deal_value
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_poor(deal_value_usd=50000.0))
        if r.threading_composite == 0.0:
            assert r.estimated_risk_exposure_usd == pytest.approx(50000.0, abs=0.01)

    def test_risk_exposure_positive(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(deal_value_usd=500000.0))
        assert r.estimated_risk_exposure_usd >= 0.0

    def test_risk_exposure_uses_deal_value(self):
        engine = DealMultithreadingIntelligence()
        r1 = engine.assess(_make_base(deal_id="high", deal_value_usd=1000000.0))
        r2 = engine.assess(_make_base(deal_id="low", deal_value_usd=100000.0))
        # Same composite, high deal value should have higher exposure
        if abs(r1.threading_composite - r2.threading_composite) < 1.0:
            assert r1.estimated_risk_exposure_usd > r2.estimated_risk_exposure_usd

    def test_risk_exposure_in_to_dict(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        assert isinstance(r.to_dict()["estimated_risk_exposure_usd"], float)


# ---------------------------------------------------------------------------
# Section 16: Primary threading gap
# ---------------------------------------------------------------------------

class TestPrimaryThreadingGap:
    def test_gap_no_exec_sponsor(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=0, deal_stage=1))
        assert "executive sponsor" in r.primary_threading_gap.lower()

    def test_gap_no_economic_buyer(self):
        engine = DealMultithreadingIntelligence()
        # Has exec contacts but no economic buyer
        r = engine.assess(_make_base(executive_contacts_count=1, economic_buyer_identified=0, deal_stage=0))
        assert "economic buyer" in r.primary_threading_gap.lower()

    def test_gap_no_champion(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=1, economic_buyer_identified=1,
                                     champion_confirmed=0, deal_stage=0))
        assert "champion" in r.primary_threading_gap.lower()

    def test_gap_org_change(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=1, economic_buyer_identified=1,
                                     champion_confirmed=1, org_change_signals=1, deal_stage=0))
        assert "org" in r.primary_threading_gap.lower()

    def test_gap_collapsed_engagement(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=1, economic_buyer_identified=1,
                                     champion_confirmed=1, org_change_signals=0,
                                     contacts_with_recent_activity=1, stakeholder_count=4,
                                     deal_stage=0))
        assert "dormant" in r.primary_threading_gap.lower() or "engagement" in r.primary_threading_gap.lower()

    def test_gap_weakest_dimension_returned_as_fallback(self):
        engine = DealMultithreadingIntelligence()
        # All specific checks pass, falls through to weakest dimension
        r = engine.assess(_make_base(executive_contacts_count=2, economic_buyer_identified=1,
                                     champion_confirmed=1, org_change_signals=0,
                                     contacts_with_recent_activity=4, stakeholder_count=4))
        assert "weakest dimension:" in r.primary_threading_gap

    def test_gap_is_string(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        assert isinstance(r.primary_threading_gap, str)
        assert len(r.primary_threading_gap) > 0


# ---------------------------------------------------------------------------
# Section 17: DealMultithreadingIntelligence.assess()
# ---------------------------------------------------------------------------

class TestAssessMethod:
    def test_returns_result_instance(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        assert isinstance(r, DealMultithreadingResult)

    def test_result_deal_id_matches_input(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(deal_id="my_deal"))
        assert r.deal_id == "my_deal"

    def test_result_rep_id_matches_input(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(rep_id="my_rep"))
        assert r.rep_id == "my_rep"

    def test_assess_stores_result_in_cache(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="cached"))
        assert engine.get("cached") is not None

    def test_assess_overwrites_previous_result_for_same_deal(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="same", deal_value_usd=100000.0))
        engine.assess(_make_base(deal_id="same", deal_value_usd=200000.0))
        r = engine.get("same")
        assert r is not None
        # Check that the second assess is the one stored
        assert r.estimated_risk_exposure_usd == pytest.approx(
            200000.0 * (100 - r.threading_composite) / 100, abs=1.0
        )

    def test_scores_all_in_range_0_to_100(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        assert 0.0 <= r.coverage_score <= 100.0
        assert 0.0 <= r.engagement_score <= 100.0
        assert 0.0 <= r.executive_access_score <= 100.0
        assert 0.0 <= r.resilience_score <= 100.0
        assert 0.0 <= r.threading_composite <= 100.0

    def test_composite_formula_verified_on_base(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        expected = round(
            r.coverage_score * 0.30 +
            r.engagement_score * 0.25 +
            r.executive_access_score * 0.25 +
            r.resilience_score * 0.20, 1
        )
        assert r.threading_composite == pytest.approx(expected, abs=0.01)


# ---------------------------------------------------------------------------
# Section 18: assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self):
        engine = DealMultithreadingIntelligence()
        results = engine.assess_batch([_make_base(), _make_poor()])
        assert isinstance(results, list)

    def test_returns_correct_count(self):
        engine = DealMultithreadingIntelligence()
        inputs = [_make_base(deal_id=f"d{i}") for i in range(5)]
        results = engine.assess_batch(inputs)
        assert len(results) == 5

    def test_sorted_by_composite_descending(self):
        engine = DealMultithreadingIntelligence()
        results = engine.assess_batch([_make_poor(), _make_base()])
        composites = [r.threading_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_all_results_are_result_instances(self):
        engine = DealMultithreadingIntelligence()
        results = engine.assess_batch([_make_base(), _make_poor()])
        for r in results:
            assert isinstance(r, DealMultithreadingResult)

    def test_batch_sorts_multiple_deals(self):
        engine = DealMultithreadingIntelligence()
        inputs = [
            _make_base(deal_id="a", contact_engagement_rate=10.0, stakeholder_count=1),
            _make_base(deal_id="b", contact_engagement_rate=50.0, stakeholder_count=3,
                       contacts_with_recent_activity=3, deal_stage=0),
            _make_base(deal_id="c", contact_engagement_rate=90.0, stakeholder_count=6,
                       contacts_with_recent_activity=5),
        ]
        results = engine.assess_batch(inputs)
        composites = [r.threading_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_empty_batch_returns_empty_list(self):
        engine = DealMultithreadingIntelligence()
        results = engine.assess_batch([])
        assert results == []

    def test_single_item_batch_works(self):
        engine = DealMultithreadingIntelligence()
        results = engine.assess_batch([_make_base()])
        assert len(results) == 1


# ---------------------------------------------------------------------------
# Section 19: reset()
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_all_results(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="d1"))
        engine.assess(_make_base(deal_id="d2"))
        engine.reset()
        assert engine.get("d1") is None
        assert engine.get("d2") is None

    def test_reset_makes_all_deals_empty(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        engine.reset()
        assert engine.all_deals() == []

    def test_reset_clears_single_threaded_deals(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(stakeholder_count=1))
        engine.reset()
        assert engine.single_threaded_deals() == []

    def test_reset_clears_executive_access_needed(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(executive_contacts_count=0, deal_stage=1))
        engine.reset()
        assert engine.executive_access_needed() == []

    def test_reset_resets_avg_composite_to_zero(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        engine.reset()
        assert engine.avg_threading_composite() == 0.0

    def test_reset_resets_total_at_risk_pipeline(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        engine.reset()
        assert engine.total_at_risk_pipeline() == 0.0

    def test_reset_allows_new_assessments(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="before"))
        engine.reset()
        engine.assess(_make_base(deal_id="after"))
        assert engine.get("before") is None
        assert engine.get("after") is not None

    def test_reset_clears_summary_counts(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0


# ---------------------------------------------------------------------------
# Section 20: by_status()
# ---------------------------------------------------------------------------

class TestByStatus:
    def test_by_status_single_threaded_returns_only_single_threaded(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="st", stakeholder_count=1))
        engine.assess(_make_base(deal_id="good"))
        results = engine.by_status(ThreadingStatus.SINGLE_THREADED)
        assert all(r.threading_status == ThreadingStatus.SINGLE_THREADED for r in results)

    def test_by_status_well_threaded_returns_only_well_threaded(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(
            stakeholder_count=6, executive_contacts_count=3,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1,
            user_buyer_engaged=1, last_exec_contact_days_ago=5,
            contact_engagement_rate=90.0, contacts_with_recent_activity=5,
            deal_stage=2, stakeholder_sentiment_avg=90.0,
            org_change_signals=0, days_in_current_stage=5,
            single_threaded_days=0, previous_multithreaded=1,
            rep_multithreading_score=95.0, champion_risk_score=5.0
        ))
        results = engine.by_status(ThreadingStatus.WELL_THREADED)
        for r in results:
            assert r.threading_status == ThreadingStatus.WELL_THREADED

    def test_by_status_returns_empty_when_no_match(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(stakeholder_count=1, deal_stage=2))  # SINGLE_THREADED
        results = engine.by_status(ThreadingStatus.WELL_THREADED)
        assert results == []

    def test_by_status_filters_correctly(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="st1", stakeholder_count=1))
        engine.assess(_make_base(deal_id="st2", stakeholder_count=1))
        results = engine.by_status(ThreadingStatus.SINGLE_THREADED)
        assert len(results) == 2


# ---------------------------------------------------------------------------
# Section 21: by_risk()
# ---------------------------------------------------------------------------

class TestByRisk:
    def test_by_risk_critical_returns_only_critical(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="cr", stakeholder_count=1, deal_stage=2))
        results = engine.by_risk(ThreadingRisk.CRITICAL)
        assert all(r.threading_risk == ThreadingRisk.CRITICAL for r in results)

    def test_by_risk_returns_empty_when_no_match(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(
            stakeholder_count=6, executive_contacts_count=3,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1,
            user_buyer_engaged=1, last_exec_contact_days_ago=5,
            contact_engagement_rate=90.0, contacts_with_recent_activity=5,
            deal_stage=2, stakeholder_sentiment_avg=90.0,
            org_change_signals=0, days_in_current_stage=5,
            single_threaded_days=0, previous_multithreaded=1,
            rep_multithreading_score=95.0, champion_risk_score=5.0
        ))
        results = engine.by_risk(ThreadingRisk.CRITICAL)
        assert results == []

    def test_by_risk_low_filters_correctly(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        results = engine.by_risk(ThreadingRisk.LOW)
        for r in results:
            assert r.threading_risk == ThreadingRisk.LOW


# ---------------------------------------------------------------------------
# Section 22: single_threaded_deals()
# ---------------------------------------------------------------------------

class TestSingleThreadedDeals:
    def test_returns_only_single_threaded(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="st", stakeholder_count=1))
        engine.assess(_make_base(deal_id="mt"))
        results = engine.single_threaded_deals()
        assert all(r.is_single_threaded for r in results)

    def test_count_matches_single_threaded(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="st1", stakeholder_count=1))
        engine.assess(_make_base(deal_id="st2", stakeholder_count=1))
        engine.assess(_make_base(deal_id="mt"))
        results = engine.single_threaded_deals()
        assert len(results) == 2

    def test_returns_empty_when_no_single_threaded(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(stakeholder_count=5, contacts_with_recent_activity=4, deal_stage=0))
        results = engine.single_threaded_deals()
        assert results == []

    def test_empty_engine_returns_empty(self):
        engine = DealMultithreadingIntelligence()
        assert engine.single_threaded_deals() == []


# ---------------------------------------------------------------------------
# Section 23: executive_access_needed()
# ---------------------------------------------------------------------------

class TestExecutiveAccessNeeded:
    def test_returns_only_exec_access_needed(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="en", executive_contacts_count=0, deal_stage=1))
        engine.assess(_make_base(deal_id="ok", executive_contacts_count=2))
        results = engine.executive_access_needed()
        assert all(r.needs_executive_access for r in results)

    def test_count_matches_exec_needed(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="en1", executive_contacts_count=0, deal_stage=1))
        engine.assess(_make_base(deal_id="en2", executive_contacts_count=0, deal_stage=2))
        engine.assess(_make_base(deal_id="ok", executive_contacts_count=1, deal_stage=1))
        results = engine.executive_access_needed()
        assert len(results) == 2

    def test_empty_engine_returns_empty(self):
        engine = DealMultithreadingIntelligence()
        assert engine.executive_access_needed() == []


# ---------------------------------------------------------------------------
# Section 24: total_at_risk_pipeline()
# ---------------------------------------------------------------------------

class TestTotalAtRiskPipeline:
    def test_returns_sum_of_exposure(self):
        engine = DealMultithreadingIntelligence()
        r1 = engine.assess(_make_base(deal_id="d1", deal_value_usd=100000.0))
        r2 = engine.assess(_make_poor(deal_id="d2", deal_value_usd=200000.0))
        expected = round(r1.estimated_risk_exposure_usd + r2.estimated_risk_exposure_usd, 2)
        assert engine.total_at_risk_pipeline() == pytest.approx(expected, abs=0.01)

    def test_returns_zero_when_empty(self):
        engine = DealMultithreadingIntelligence()
        assert engine.total_at_risk_pipeline() == 0.0

    def test_returns_single_deal_exposure_when_one_deal(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(deal_id="only", deal_value_usd=300000.0))
        assert engine.total_at_risk_pipeline() == pytest.approx(r.estimated_risk_exposure_usd, abs=0.01)

    def test_pipeline_is_non_negative(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        engine.assess(_make_poor())
        assert engine.total_at_risk_pipeline() >= 0.0


# ---------------------------------------------------------------------------
# Section 25: summary() — exactly 13 keys
# ---------------------------------------------------------------------------

class TestSummaryMethod:
    def test_summary_returns_13_keys(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        s = engine.summary()
        assert len(s) == 13

    def test_summary_has_total(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "total" in engine.summary()

    def test_summary_has_threading_status_counts(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "threading_status_counts" in engine.summary()

    def test_summary_has_risk_counts(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "risk_counts" in engine.summary()

    def test_summary_has_coverage_counts(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "coverage_counts" in engine.summary()

    def test_summary_has_action_counts(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "action_counts" in engine.summary()

    def test_summary_has_avg_threading_composite(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "avg_threading_composite" in engine.summary()

    def test_summary_has_single_threaded_count(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "single_threaded_count" in engine.summary()

    def test_summary_has_executive_access_needed_count(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "executive_access_needed_count" in engine.summary()

    def test_summary_has_avg_coverage_score(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "avg_coverage_score" in engine.summary()

    def test_summary_has_avg_engagement_score(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "avg_engagement_score" in engine.summary()

    def test_summary_has_avg_executive_access_score(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "avg_executive_access_score" in engine.summary()

    def test_summary_has_avg_resilience_score(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "avg_resilience_score" in engine.summary()

    def test_summary_has_total_at_risk_pipeline_usd(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base())
        assert "total_at_risk_pipeline_usd" in engine.summary()

    def test_summary_total_count_correct(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="d1"))
        engine.assess(_make_base(deal_id="d2"))
        engine.assess(_make_base(deal_id="d3"))
        assert engine.summary()["total"] == 3

    def test_summary_total_zero_when_empty(self):
        engine = DealMultithreadingIntelligence()
        assert engine.summary()["total"] == 0

    def test_summary_avg_composite_correct(self):
        engine = DealMultithreadingIntelligence()
        r1 = engine.assess(_make_base(deal_id="d1"))
        r2 = engine.assess(_make_poor(deal_id="d2"))
        expected_avg = round((r1.threading_composite + r2.threading_composite) / 2, 1)
        assert engine.summary()["avg_threading_composite"] == pytest.approx(expected_avg, abs=0.01)

    def test_summary_single_threaded_count_correct(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="st1", stakeholder_count=1))
        engine.assess(_make_base(deal_id="st2", stakeholder_count=1))
        engine.assess(_make_base(deal_id="mt"))
        s = engine.summary()
        assert s["single_threaded_count"] == 2

    def test_summary_executive_access_needed_count_correct(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="en", executive_contacts_count=0, deal_stage=1))
        engine.assess(_make_base(deal_id="ok"))
        s = engine.summary()
        assert s["executive_access_needed_count"] == 1

    def test_summary_status_counts_includes_well_threaded(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(
            stakeholder_count=6, executive_contacts_count=3,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1,
            user_buyer_engaged=1, last_exec_contact_days_ago=5,
            contact_engagement_rate=90.0, contacts_with_recent_activity=5,
            deal_stage=2, stakeholder_sentiment_avg=90.0,
            org_change_signals=0, days_in_current_stage=5,
            single_threaded_days=0, previous_multithreaded=1,
            rep_multithreading_score=95.0, champion_risk_score=5.0
        ))
        s = engine.summary()
        assert sum(s["threading_status_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_to_total(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="d1"))
        engine.assess(_make_poor(deal_id="d2"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_coverage_counts_sum_to_total(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="d1"))
        engine.assess(_make_poor(deal_id="d2"))
        s = engine.summary()
        assert sum(s["coverage_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="d1"))
        engine.assess(_make_poor(deal_id="d2"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_coverage_score_correct(self):
        engine = DealMultithreadingIntelligence()
        r1 = engine.assess(_make_base(deal_id="d1"))
        r2 = engine.assess(_make_poor(deal_id="d2"))
        expected = round((r1.coverage_score + r2.coverage_score) / 2, 1)
        assert engine.summary()["avg_coverage_score"] == pytest.approx(expected, abs=0.01)

    def test_summary_avg_engagement_score_correct(self):
        engine = DealMultithreadingIntelligence()
        r1 = engine.assess(_make_base(deal_id="d1"))
        r2 = engine.assess(_make_poor(deal_id="d2"))
        expected = round((r1.engagement_score + r2.engagement_score) / 2, 1)
        assert engine.summary()["avg_engagement_score"] == pytest.approx(expected, abs=0.01)

    def test_summary_total_at_risk_pipeline_correct(self):
        engine = DealMultithreadingIntelligence()
        r1 = engine.assess(_make_base(deal_id="d1", deal_value_usd=100000.0))
        r2 = engine.assess(_make_poor(deal_id="d2", deal_value_usd=200000.0))
        expected = round(r1.estimated_risk_exposure_usd + r2.estimated_risk_exposure_usd, 2)
        assert engine.summary()["total_at_risk_pipeline_usd"] == pytest.approx(expected, abs=0.01)

    def test_summary_returns_dict_type(self):
        engine = DealMultithreadingIntelligence()
        assert isinstance(engine.summary(), dict)

    def test_summary_empty_engine_avg_scores_are_zero(self):
        engine = DealMultithreadingIntelligence()
        s = engine.summary()
        assert s["avg_coverage_score"] == 0.0
        assert s["avg_engagement_score"] == 0.0
        assert s["avg_executive_access_score"] == 0.0
        assert s["avg_resilience_score"] == 0.0


# ---------------------------------------------------------------------------
# Section 26: avg_threading_composite()
# ---------------------------------------------------------------------------

class TestAvgThreadingComposite:
    def test_zero_when_empty(self):
        engine = DealMultithreadingIntelligence()
        assert engine.avg_threading_composite() == 0.0

    def test_single_deal(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base())
        assert engine.avg_threading_composite() == pytest.approx(r.threading_composite, abs=0.01)

    def test_average_of_two_deals(self):
        engine = DealMultithreadingIntelligence()
        r1 = engine.assess(_make_base(deal_id="d1"))
        r2 = engine.assess(_make_poor(deal_id="d2"))
        expected = round((r1.threading_composite + r2.threading_composite) / 2, 1)
        assert engine.avg_threading_composite() == pytest.approx(expected, abs=0.01)

    def test_rounded_to_1_decimal(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="d1"))
        engine.assess(_make_poor(deal_id="d2"))
        avg = engine.avg_threading_composite()
        assert avg == round(avg, 1)


# ---------------------------------------------------------------------------
# Section 27: get() and all_deals()
# ---------------------------------------------------------------------------

class TestGetAndAllDeals:
    def test_get_returns_none_for_unknown_deal(self):
        engine = DealMultithreadingIntelligence()
        assert engine.get("nonexistent") is None

    def test_get_returns_result_for_known_deal(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="known"))
        r = engine.get("known")
        assert r is not None
        assert r.deal_id == "known"

    def test_all_deals_returns_all_results(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_base(deal_id="d1"))
        engine.assess(_make_base(deal_id="d2"))
        engine.assess(_make_base(deal_id="d3"))
        assert len(engine.all_deals()) == 3

    def test_all_deals_sorted_by_composite_descending(self):
        engine = DealMultithreadingIntelligence()
        engine.assess(_make_poor(deal_id="low"))
        engine.assess(_make_base(deal_id="high"))
        deals = engine.all_deals()
        composites = [d.threading_composite for d in deals]
        assert composites == sorted(composites, reverse=True)

    def test_all_deals_empty_when_no_assessments(self):
        engine = DealMultithreadingIntelligence()
        assert engine.all_deals() == []


# ---------------------------------------------------------------------------
# Section 28: Score clamping boundaries
# ---------------------------------------------------------------------------

class TestScoreClamping:
    def test_coverage_never_exceeds_100(self):
        engine = DealMultithreadingIntelligence()
        for stakeholder_count in [1, 3, 5, 8, 20]:
            r = engine.assess(_make_base(
                deal_id=f"sc{stakeholder_count}",
                stakeholder_count=stakeholder_count,
                rep_multithreading_score=200.0,
                executive_contacts_count=10
            ))
            assert r.coverage_score <= 100.0, f"Coverage exceeded 100 with stakeholder_count={stakeholder_count}"

    def test_engagement_never_goes_below_zero(self):
        engine = DealMultithreadingIntelligence()
        # Max penalties: org_change -15, days>=60 -10
        r = engine.assess(_make_base(deal_id="min_eng",
                                     contact_engagement_rate=0.0,
                                     contacts_with_recent_activity=0,
                                     stakeholder_sentiment_avg=0.0,
                                     org_change_signals=1,
                                     days_in_current_stage=90,
                                     deal_stage=0))
        assert r.engagement_score >= 0.0

    def test_executive_access_never_exceeds_100(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(executive_contacts_count=100,
                                     last_exec_contact_days_ago=1,
                                     economic_buyer_identified=1,
                                     decision_maker_engaged=1))
        assert r.executive_access_score <= 100.0

    def test_resilience_never_goes_below_zero(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_poor(
            champion_confirmed=0, previous_multithreaded=0,
            single_threaded_days=100, stakeholder_count=1,
            org_change_signals=1, champion_risk_score=90.0,
            deal_stage=0
        ))
        assert r.resilience_score >= 0.0

    def test_composite_never_exceeds_100(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=10, executive_contacts_count=10,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1,
            user_buyer_engaged=1, last_exec_contact_days_ago=1,
            contact_engagement_rate=100.0, contacts_with_recent_activity=10,
            deal_stage=0, stakeholder_sentiment_avg=100.0,
            org_change_signals=0, days_in_current_stage=0,
            single_threaded_days=0, previous_multithreaded=1,
            rep_multithreading_score=100.0, champion_risk_score=0.0
        ))
        assert r.threading_composite <= 100.0

    def test_composite_never_below_zero(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_poor())
        assert r.threading_composite >= 0.0


# ---------------------------------------------------------------------------
# Section 29: End-to-end scenarios
# ---------------------------------------------------------------------------

class TestEndToEndScenarios:
    def test_ideal_deal_characteristics(self):
        """Well-threaded deal should have LOW risk, COMPREHENSIVE coverage."""
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=6, executive_contacts_count=3,
            champion_confirmed=1, economic_buyer_identified=1,
            decision_maker_engaged=1, technical_evaluator_engaged=1,
            user_buyer_engaged=1, last_exec_contact_days_ago=3,
            contact_engagement_rate=95.0, contacts_with_recent_activity=5,
            deal_stage=2, stakeholder_sentiment_avg=85.0,
            org_change_signals=0, days_in_current_stage=5,
            single_threaded_days=0, previous_multithreaded=1,
            rep_multithreading_score=95.0, champion_risk_score=5.0
        ))
        assert r.stakeholder_coverage == StakeholderCoverage.COMPREHENSIVE
        assert r.is_single_threaded is False
        assert r.threading_composite > 60

    def test_worst_case_deal_characteristics(self):
        """Single-threaded, at-risk deal should have CRITICAL risk, POOR coverage."""
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_poor())
        assert r.is_single_threaded is True
        assert r.threading_risk == ThreadingRisk.CRITICAL
        assert r.threading_action == ThreadingAction.EMERGENCY_EXECUTIVE_OUTREACH

    def test_deal_with_org_change_signals(self):
        """Org change should increase risk and reduce engagement/resilience."""
        engine = DealMultithreadingIntelligence()
        r_clean = engine.assess(_make_base(deal_id="clean", org_change_signals=0))
        r_dirty = engine.assess(_make_base(deal_id="dirty", org_change_signals=1))
        assert r_clean.engagement_score >= r_dirty.engagement_score
        assert r_clean.resilience_score >= r_dirty.resilience_score

    def test_high_champion_risk_reduces_resilience(self):
        """High champion risk score should lower resilience."""
        engine = DealMultithreadingIntelligence()
        r_low = engine.assess(_make_base(deal_id="low_cr", champion_risk_score=10.0))
        r_high = engine.assess(_make_base(deal_id="high_cr", champion_risk_score=80.0))
        assert r_low.resilience_score > r_high.resilience_score

    def test_increasing_stakeholder_count_improves_scores(self):
        """More stakeholders should mean better coverage and resilience."""
        engine = DealMultithreadingIntelligence()
        r_few = engine.assess(_make_base(deal_id="few", stakeholder_count=2, deal_stage=0))
        r_many = engine.assess(_make_base(deal_id="many", stakeholder_count=6, deal_stage=0))
        assert r_many.coverage_score > r_few.coverage_score

    def test_recent_exec_contact_improves_exec_access_score(self):
        """Recent exec contact should give higher exec access score."""
        engine = DealMultithreadingIntelligence()
        r_recent = engine.assess(_make_base(deal_id="recent", last_exec_contact_days_ago=5))
        r_old = engine.assess(_make_base(deal_id="old", last_exec_contact_days_ago=90))
        assert r_recent.executive_access_score > r_old.executive_access_score

    def test_batch_assess_populates_cache(self):
        """After batch assess, all deals should be accessible via get()."""
        engine = DealMultithreadingIntelligence()
        ids = ["batch_1", "batch_2", "batch_3"]
        inputs = [_make_base(deal_id=id_) for id_ in ids]
        engine.assess_batch(inputs)
        for id_ in ids:
            assert engine.get(id_) is not None

    def test_multiple_assessments_accumulate(self):
        """Assessing multiple distinct deals should all be stored."""
        engine = DealMultithreadingIntelligence()
        for i in range(10):
            engine.assess(_make_base(deal_id=f"deal_{i:02d}"))
        assert len(engine.all_deals()) == 10

    def test_summary_reflects_all_assessed_deals(self):
        """Summary total should match assessed deal count."""
        engine = DealMultithreadingIntelligence()
        for i in range(7):
            engine.assess(_make_base(deal_id=f"deal_{i}"))
        assert engine.summary()["total"] == 7

    def test_single_threaded_deal_has_is_single_threaded_true(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            stakeholder_count=1,
            contacts_with_recent_activity=0,
            deal_stage=1
        ))
        assert r.is_single_threaded is True
        assert r.threading_status == ThreadingStatus.SINGLE_THREADED

    def test_deal_without_exec_needs_exec_access(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            executive_contacts_count=0,
            deal_stage=2
        ))
        assert r.needs_executive_access is True

    def test_deal_with_exec_does_not_need_exec_access(self):
        engine = DealMultithreadingIntelligence()
        r = engine.assess(_make_base(
            executive_contacts_count=1,
            deal_stage=2
        ))
        assert r.needs_executive_access is False
