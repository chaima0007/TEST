"""
Comprehensive pytest test suite for SalesStakeholderMappingIntelligenceEngine.
"""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_stakeholder_mapping_intelligence_engine import (
    SalesStakeholderMappingIntelligenceEngine,
    StakeholderMappingInput,
    StakeholderMappingResult,
    StakeholderRisk,
    StakeholderPattern,
    StakeholderSeverity,
    StakeholderAction,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**kwargs) -> StakeholderMappingInput:
    """Return a baseline 'healthy' input, overriding any field via kwargs."""
    defaults = dict(
        rep_id="REP-001",
        region="Northeast",
        evaluation_period_id="Q1-2026",
        total_active_deals=10,
        single_threaded_deals=1,
        multi_threaded_deals=9,
        avg_contacts_per_deal=3.0,
        economic_buyer_identified_count=8,
        economic_buyer_engaged_count=7,
        champion_identified_count=8,
        champion_active_count=7,
        executive_sponsor_deals=4,
        decision_maker_met_count=7,
        avg_stakeholder_influence_score=7.0,
        deals_with_legal_involved=3,
        deals_with_procurement_involved=2,
        committee_buying_deals=2,
        multi_department_deals=5,
        lost_deals_single_threaded=0,
        deals_stalled_no_champion=0,
        avg_deal_size_multi_stakeholder_usd=50000.0,
        avg_deal_size_single_stakeholder_usd=20000.0,
    )
    defaults.update(kwargs)
    return StakeholderMappingInput(**defaults)


def engine() -> SalesStakeholderMappingIntelligenceEngine:
    return SalesStakeholderMappingIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum tests
# ---------------------------------------------------------------------------

class TestStakeholderRiskEnum:
    def test_values_exist(self):
        assert StakeholderRisk.low.value == "low"
        assert StakeholderRisk.moderate.value == "moderate"
        assert StakeholderRisk.high.value == "high"
        assert StakeholderRisk.critical.value == "critical"

    def test_is_str_subclass(self):
        assert isinstance(StakeholderRisk.low, str)

    def test_four_members(self):
        assert len(StakeholderRisk) == 4

    def test_membership(self):
        assert "low" in [r.value for r in StakeholderRisk]
        assert "critical" in [r.value for r in StakeholderRisk]

    def test_identity_comparison(self):
        assert StakeholderRisk.low == StakeholderRisk.low
        assert StakeholderRisk.high != StakeholderRisk.low


class TestStakeholderPatternEnum:
    def test_all_values(self):
        expected = {
            "none", "single_threaded", "no_economic_buyer",
            "champion_gap", "executive_avoidance",
            "poor_stakeholder_advancement",
        }
        assert {p.value for p in StakeholderPattern} == expected

    def test_six_members(self):
        assert len(StakeholderPattern) == 6

    def test_is_str_subclass(self):
        assert isinstance(StakeholderPattern.none, str)

    def test_individual_values(self):
        assert StakeholderPattern.single_threaded.value == "single_threaded"
        assert StakeholderPattern.no_economic_buyer.value == "no_economic_buyer"
        assert StakeholderPattern.champion_gap.value == "champion_gap"
        assert StakeholderPattern.executive_avoidance.value == "executive_avoidance"
        assert StakeholderPattern.poor_stakeholder_advancement.value == "poor_stakeholder_advancement"
        assert StakeholderPattern.none.value == "none"


class TestStakeholderSeverityEnum:
    def test_all_values(self):
        expected = {"engaged", "developing", "fragile", "exposed"}
        assert {s.value for s in StakeholderSeverity} == expected

    def test_four_members(self):
        assert len(StakeholderSeverity) == 4

    def test_is_str_subclass(self):
        assert isinstance(StakeholderSeverity.engaged, str)

    def test_individual_values(self):
        assert StakeholderSeverity.engaged.value == "engaged"
        assert StakeholderSeverity.developing.value == "developing"
        assert StakeholderSeverity.fragile.value == "fragile"
        assert StakeholderSeverity.exposed.value == "exposed"


class TestStakeholderActionEnum:
    def test_all_values(self):
        expected = {
            "no_action", "multi_threading_coaching", "economic_buyer_strategy",
            "champion_development", "stakeholder_mapping_review",
            "executive_access_plan",
        }
        assert {a.value for a in StakeholderAction} == expected

    def test_six_members(self):
        assert len(StakeholderAction) == 6

    def test_is_str_subclass(self):
        assert isinstance(StakeholderAction.no_action, str)

    def test_individual_values(self):
        assert StakeholderAction.no_action.value == "no_action"
        assert StakeholderAction.multi_threading_coaching.value == "multi_threading_coaching"
        assert StakeholderAction.economic_buyer_strategy.value == "economic_buyer_strategy"
        assert StakeholderAction.champion_development.value == "champion_development"
        assert StakeholderAction.stakeholder_mapping_review.value == "stakeholder_mapping_review"
        assert StakeholderAction.executive_access_plan.value == "executive_access_plan"


# ---------------------------------------------------------------------------
# 2. _coverage_breadth_score
# ---------------------------------------------------------------------------

class TestCoverageBreadthScore:
    def setup_method(self):
        self.eng = engine()

    # single_rate branch
    def test_single_rate_zero(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0, avg_contacts_per_deal=3.0, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 0.0  # 0% single, >=2.5 contacts, >=3 multi

    def test_single_rate_exactly_20pct(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=2, avg_contacts_per_deal=3.0, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 10.0  # 0.20 → +10

    def test_single_rate_just_below_40pct(self):
        # 3/10 = 0.30
        inp = make_input(total_active_deals=10, single_threaded_deals=3, avg_contacts_per_deal=3.0, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 10.0

    def test_single_rate_exactly_40pct(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=4, avg_contacts_per_deal=3.0, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 25.0  # 0.40 → +25

    def test_single_rate_just_below_60pct(self):
        # 5/10 = 0.50
        inp = make_input(total_active_deals=10, single_threaded_deals=5, avg_contacts_per_deal=3.0, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 25.0

    def test_single_rate_exactly_60pct(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=6, avg_contacts_per_deal=3.0, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 45.0  # 0.60 → +45

    def test_single_rate_above_60pct(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=8, avg_contacts_per_deal=3.0, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 45.0

    # avg_contacts branch
    def test_contacts_below_1_5(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0, avg_contacts_per_deal=1.0, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 30.0  # +30 for <1.5

    def test_contacts_exactly_1_5(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0, avg_contacts_per_deal=1.5, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 15.0  # 1.5 is NOT < 1.5, falls into <2.5 → +15

    def test_contacts_exactly_2_5(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0, avg_contacts_per_deal=2.5, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 0.0  # 2.5 is NOT < 2.5

    def test_contacts_between_1_5_and_2_5(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0, avg_contacts_per_deal=2.0, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 15.0

    # multi_threaded branch
    def test_multi_threaded_zero(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0, avg_contacts_per_deal=3.0, multi_threaded_deals=0)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 20.0

    def test_multi_threaded_one(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0, avg_contacts_per_deal=3.0, multi_threaded_deals=1)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 10.0

    def test_multi_threaded_two(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0, avg_contacts_per_deal=3.0, multi_threaded_deals=2)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 10.0  # <3 → +10

    def test_multi_threaded_three_or_more(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0, avg_contacts_per_deal=3.0, multi_threaded_deals=3)
        s = self.eng._coverage_breadth_score(inp)
        assert s == 0.0

    # max possible is 95 (45+30+20); score never exceeds that
    def test_max_possible_is_95(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=10, avg_contacts_per_deal=0.5, multi_threaded_deals=0)
        s = self.eng._coverage_breadth_score(inp)
        # 45 (single_rate>=0.60) + 30 (contacts<1.5) + 20 (multi==0) = 95
        assert s == 95.0

    def test_score_never_exceeds_100(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=10, avg_contacts_per_deal=0.5, multi_threaded_deals=0)
        s = self.eng._coverage_breadth_score(inp)
        assert s <= 100.0

    # zero deals guard
    def test_zero_total_deals_guard(self):
        inp = make_input(total_active_deals=0, single_threaded_deals=0, avg_contacts_per_deal=3.0, multi_threaded_deals=5)
        s = self.eng._coverage_breadth_score(inp)
        assert s >= 0.0  # Should not raise; total clamped to 1

    # combined
    def test_all_components_combined(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=6, avg_contacts_per_deal=1.0, multi_threaded_deals=0)
        s = self.eng._coverage_breadth_score(inp)
        # 45 + 30 + 20 = 95
        assert s == 95.0


# ---------------------------------------------------------------------------
# 3. _buyer_alignment_score
# ---------------------------------------------------------------------------

class TestBuyerAlignmentScore:
    def setup_method(self):
        self.eng = engine()

    # eb_rate branch
    def test_eb_rate_below_30pct(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=2,
                         economic_buyer_engaged_count=2, decision_maker_met_count=5)
        s = self.eng._buyer_alignment_score(inp)
        assert s >= 40.0  # +40

    def test_eb_rate_exactly_30pct(self):
        # 3/10 = 0.30, NOT < 0.30 → +20 (falls into < 0.50)
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=3,
                         economic_buyer_engaged_count=3, decision_maker_met_count=5)
        s = self.eng._buyer_alignment_score(inp)
        # 0.30 >= 0.30, then checks < 0.50 → +20
        assert s >= 20.0

    def test_eb_rate_exactly_50pct(self):
        # 5/10 = 0.50, not < 0.50 → checks < 0.70 → +8
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=5,
                         economic_buyer_engaged_count=5, decision_maker_met_count=5)
        s = self.eng._buyer_alignment_score(inp)
        assert 8.0 <= s  # at least +8

    def test_eb_rate_exactly_70pct(self):
        # 7/10 = 0.70, not < 0.70 → 0 from this branch
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=7,
                         economic_buyer_engaged_count=7, decision_maker_met_count=7)
        s = self.eng._buyer_alignment_score(inp)
        assert s == 0.0  # all rates high, no penalty

    # engaged_rate branch
    def test_engaged_rate_below_40pct(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=5,
                         economic_buyer_engaged_count=1, decision_maker_met_count=7)
        s = self.eng._buyer_alignment_score(inp)
        # 5/10=0.50, +8; engaged 1/5=0.20 <0.40 → +30; dm 7/10=0.70 no add
        assert s == 38.0

    def test_engaged_rate_between_40_and_60(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=5,
                         economic_buyer_engaged_count=2, decision_maker_met_count=7)
        # engaged 2/5=0.40, NOT <0.40 → checks <0.60 → +15
        s = self.eng._buyer_alignment_score(inp)
        assert s == 23.0  # +8 +15

    def test_no_economic_buyer_skips_engaged_branch(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=0,
                         economic_buyer_engaged_count=0, decision_maker_met_count=7)
        s = self.eng._buyer_alignment_score(inp)
        # eb_rate=0 → +40; economic_buyer_identified_count==0 so no engaged branch
        assert 40.0 <= s

    # dm_rate branch
    def test_dm_rate_below_30pct(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=7,
                         economic_buyer_engaged_count=7, decision_maker_met_count=2)
        s = self.eng._buyer_alignment_score(inp)
        assert s == 20.0  # +20 for dm_rate <0.30

    def test_dm_rate_exactly_30pct(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=7,
                         economic_buyer_engaged_count=7, decision_maker_met_count=3)
        # dm_rate=0.30, not <0.30 → checks <0.50 → +10
        s = self.eng._buyer_alignment_score(inp)
        assert s == 10.0

    def test_dm_rate_exactly_50pct(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=7,
                         economic_buyer_engaged_count=7, decision_maker_met_count=5)
        # dm_rate=0.50, not <0.50 → 0
        s = self.eng._buyer_alignment_score(inp)
        assert s == 0.0

    # cap
    def test_capped_at_100(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=1,
                         economic_buyer_engaged_count=0, decision_maker_met_count=0)
        s = self.eng._buyer_alignment_score(inp)
        assert s <= 100.0

    def test_zero_total_deals_guard(self):
        inp = make_input(total_active_deals=0, economic_buyer_identified_count=0,
                         economic_buyer_engaged_count=0, decision_maker_met_count=0)
        s = self.eng._buyer_alignment_score(inp)
        assert s >= 0.0


# ---------------------------------------------------------------------------
# 4. _champion_development_score
# ---------------------------------------------------------------------------

class TestChampionDevelopmentScore:
    def setup_method(self):
        self.eng = engine()

    def test_champ_rate_below_30pct(self):
        inp = make_input(total_active_deals=10, champion_identified_count=2,
                         champion_active_count=2, deals_stalled_no_champion=0)
        s = self.eng._champion_development_score(inp)
        assert s >= 40.0

    def test_champ_rate_exactly_30pct(self):
        inp = make_input(total_active_deals=10, champion_identified_count=3,
                         champion_active_count=3, deals_stalled_no_champion=0)
        # 0.30, not <0.30 → +20
        s = self.eng._champion_development_score(inp)
        assert s >= 20.0

    def test_champ_rate_exactly_50pct(self):
        inp = make_input(total_active_deals=10, champion_identified_count=5,
                         champion_active_count=5, deals_stalled_no_champion=0)
        # 0.50, not <0.50 → +8
        s = self.eng._champion_development_score(inp)
        assert s >= 8.0

    def test_champ_rate_70pct_or_above(self):
        inp = make_input(total_active_deals=10, champion_identified_count=7,
                         champion_active_count=7, deals_stalled_no_champion=0)
        s = self.eng._champion_development_score(inp)
        assert s == 0.0

    def test_active_rate_below_40pct(self):
        inp = make_input(total_active_deals=10, champion_identified_count=5,
                         champion_active_count=1, deals_stalled_no_champion=0)
        # champ_rate=0.50, +8; active_rate=1/5=0.20 <0.40 → +30
        s = self.eng._champion_development_score(inp)
        assert s == 38.0

    def test_active_rate_between_40_and_60(self):
        inp = make_input(total_active_deals=10, champion_identified_count=5,
                         champion_active_count=2, deals_stalled_no_champion=0)
        # active_rate=0.40, not <0.40 → checks <0.60 → +15
        s = self.eng._champion_development_score(inp)
        assert s == 23.0

    def test_no_champion_skips_active_branch(self):
        inp = make_input(total_active_deals=10, champion_identified_count=0,
                         champion_active_count=0, deals_stalled_no_champion=0)
        # champion_identified_count=0 → skip active branch; champ_rate=0 → +40
        s = self.eng._champion_development_score(inp)
        assert s == 40.0

    def test_stalled_deals_zero(self):
        inp = make_input(total_active_deals=10, champion_identified_count=7,
                         champion_active_count=7, deals_stalled_no_champion=0)
        s = self.eng._champion_development_score(inp)
        assert s == 0.0

    def test_stalled_deals_one(self):
        inp = make_input(total_active_deals=10, champion_identified_count=7,
                         champion_active_count=7, deals_stalled_no_champion=1)
        s = self.eng._champion_development_score(inp)
        assert s == 10.0

    def test_stalled_deals_two(self):
        inp = make_input(total_active_deals=10, champion_identified_count=7,
                         champion_active_count=7, deals_stalled_no_champion=2)
        s = self.eng._champion_development_score(inp)
        assert s == 10.0

    def test_stalled_deals_three(self):
        inp = make_input(total_active_deals=10, champion_identified_count=7,
                         champion_active_count=7, deals_stalled_no_champion=3)
        s = self.eng._champion_development_score(inp)
        assert s == 20.0

    def test_capped_at_100(self):
        inp = make_input(total_active_deals=10, champion_identified_count=1,
                         champion_active_count=0, deals_stalled_no_champion=5)
        s = self.eng._champion_development_score(inp)
        assert s <= 100.0


# ---------------------------------------------------------------------------
# 5. _executive_access_score
# ---------------------------------------------------------------------------

class TestExecutiveAccessScore:
    def setup_method(self):
        self.eng = engine()

    def test_exec_rate_below_10pct(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=0,
                         avg_stakeholder_influence_score=7.0, committee_buying_deals=0)
        s = self.eng._executive_access_score(inp)
        assert s == 45.0  # +45

    def test_exec_rate_exactly_10pct(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=1,
                         avg_stakeholder_influence_score=7.0, committee_buying_deals=0)
        # 1/10=0.10, not <0.10 → checks <0.20 → +25
        s = self.eng._executive_access_score(inp)
        assert s == 25.0

    def test_exec_rate_exactly_20pct(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=2,
                         avg_stakeholder_influence_score=7.0, committee_buying_deals=0)
        # 0.20, not <0.20 → checks <0.35 → +10
        s = self.eng._executive_access_score(inp)
        assert s == 10.0

    def test_exec_rate_exactly_35pct(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=4,
                         avg_stakeholder_influence_score=7.0, committee_buying_deals=0)
        # 4/10=0.40, not <0.35 → 0
        s = self.eng._executive_access_score(inp)
        # 0.35 ≤ 0.40 → no add from exec branch
        assert s == 0.0

    def test_influence_below_4(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=4,
                         avg_stakeholder_influence_score=3.9, committee_buying_deals=0)
        s = self.eng._executive_access_score(inp)
        assert s == 30.0

    def test_influence_exactly_4(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=4,
                         avg_stakeholder_influence_score=4.0, committee_buying_deals=0)
        # 4.0 not <4.0 → checks <6.0 → +15
        s = self.eng._executive_access_score(inp)
        assert s == 15.0

    def test_influence_exactly_6(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=4,
                         avg_stakeholder_influence_score=6.0, committee_buying_deals=0)
        # 6.0 not <6.0 → 0
        s = self.eng._executive_access_score(inp)
        assert s == 0.0

    def test_committee_no_exec_sponsor(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=0,
                         avg_stakeholder_influence_score=7.0, committee_buying_deals=3)
        # exec=0 → +45; influence 7 → 0; committee>0 and exec==0 → +20
        s = self.eng._executive_access_score(inp)
        assert s == 65.0

    def test_committee_low_exec_rate(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=1,
                         avg_stakeholder_influence_score=7.0, committee_buying_deals=3)
        # exec=1/10=0.10, +25; committee>0 and exec_rate<0.20 → +10
        s = self.eng._executive_access_score(inp)
        assert s == 35.0

    def test_committee_adequate_exec_rate(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=3,
                         avg_stakeholder_influence_score=7.0, committee_buying_deals=3)
        # exec_rate=0.30, +10; committee>0 but exec_rate=0.30 >= 0.20 → no +10
        s = self.eng._executive_access_score(inp)
        assert s == 10.0

    def test_capped_at_100(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=0,
                         avg_stakeholder_influence_score=1.0, committee_buying_deals=5)
        s = self.eng._executive_access_score(inp)
        assert s == 95.0  # 45+30+20=95 (all three penalties)

    def test_zero_total_deals_guard(self):
        inp = make_input(total_active_deals=0, executive_sponsor_deals=0,
                         avg_stakeholder_influence_score=7.0, committee_buying_deals=0)
        s = self.eng._executive_access_score(inp)
        assert s >= 0.0


# ---------------------------------------------------------------------------
# 6. _detect_pattern (all 6 patterns + priority ordering)
# ---------------------------------------------------------------------------

class TestDetectPattern:
    def setup_method(self):
        self.eng = engine()

    def _call(self, inp, coverage, buyer, champion, executive):
        return self.eng._detect_pattern(inp, coverage, buyer, champion, executive)

    def test_none_pattern(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=8,
                         executive_sponsor_deals=5, avg_stakeholder_influence_score=7.0)
        pat = self._call(inp, 10.0, 10.0, 10.0, 10.0)
        assert pat == StakeholderPattern.none

    def test_single_threaded_pattern(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=6)
        pat = self._call(inp, 35.0, 10.0, 10.0, 10.0)
        assert pat == StakeholderPattern.single_threaded

    def test_single_threaded_requires_coverage_ge_35(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=6)
        pat = self._call(inp, 34.9, 10.0, 10.0, 10.0)
        # coverage < 35 → shouldn't be single_threaded
        assert pat != StakeholderPattern.single_threaded

    def test_single_threaded_requires_single_rate_ge_50pct(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=4)  # 0.40 < 0.50
        pat = self._call(inp, 35.0, 10.0, 10.0, 10.0)
        assert pat != StakeholderPattern.single_threaded

    def test_no_economic_buyer_pattern(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=3)  # 0.30 < 0.40
        pat = self._call(inp, 10.0, 30.0, 10.0, 10.0)
        assert pat == StakeholderPattern.no_economic_buyer

    def test_no_economic_buyer_requires_buyer_ge_30(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=3)
        pat = self._call(inp, 10.0, 29.9, 10.0, 10.0)
        assert pat != StakeholderPattern.no_economic_buyer

    def test_champion_gap_pattern(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=3)
        pat = self._call(inp, 10.0, 10.0, 30.0, 10.0)
        assert pat == StakeholderPattern.champion_gap

    def test_champion_gap_requires_champion_ge_30(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=3)
        pat = self._call(inp, 10.0, 10.0, 29.9, 10.0)
        assert pat != StakeholderPattern.champion_gap

    def test_champion_gap_requires_champ_rate_below_40pct(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=4)  # 0.40, not <0.40
        pat = self._call(inp, 10.0, 10.0, 30.0, 10.0)
        assert pat != StakeholderPattern.champion_gap

    def test_executive_avoidance_pattern(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=8,
                         executive_sponsor_deals=1)  # 0.10 < 0.15
        pat = self._call(inp, 10.0, 10.0, 10.0, 30.0)
        assert pat == StakeholderPattern.executive_avoidance

    def test_executive_avoidance_requires_exec_ge_30(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=8,
                         executive_sponsor_deals=1)
        pat = self._call(inp, 10.0, 10.0, 10.0, 29.9)
        assert pat != StakeholderPattern.executive_avoidance

    def test_executive_avoidance_requires_exec_rate_below_15pct(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=8,
                         executive_sponsor_deals=2)  # 0.20, not <0.15
        pat = self._call(inp, 10.0, 10.0, 10.0, 30.0)
        assert pat != StakeholderPattern.executive_avoidance

    def test_poor_stakeholder_advancement_pattern(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=8,
                         executive_sponsor_deals=5, avg_stakeholder_influence_score=4.5)
        pat = self._call(inp, 10.0, 25.0, 10.0, 10.0)
        assert pat == StakeholderPattern.poor_stakeholder_advancement

    def test_poor_stakeholder_advancement_requires_buyer_ge_25(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=8,
                         executive_sponsor_deals=5, avg_stakeholder_influence_score=4.5)
        pat = self._call(inp, 10.0, 24.9, 10.0, 10.0)
        assert pat != StakeholderPattern.poor_stakeholder_advancement

    def test_poor_stakeholder_advancement_requires_influence_below_5(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=8,
                         executive_sponsor_deals=5, avg_stakeholder_influence_score=5.0)
        pat = self._call(inp, 10.0, 25.0, 10.0, 10.0)
        assert pat != StakeholderPattern.poor_stakeholder_advancement

    def test_priority_single_threaded_wins_over_no_economic_buyer(self):
        """single_threaded is checked first; if true, should return that."""
        inp = make_input(total_active_deals=10, single_threaded_deals=6,
                         economic_buyer_identified_count=2)
        pat = self._call(inp, 35.0, 30.0, 10.0, 10.0)
        assert pat == StakeholderPattern.single_threaded

    def test_priority_no_economic_buyer_wins_over_champion_gap(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=2, champion_identified_count=2)
        pat = self._call(inp, 10.0, 30.0, 30.0, 10.0)
        assert pat == StakeholderPattern.no_economic_buyer

    def test_priority_champion_gap_wins_over_executive_avoidance(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         economic_buyer_identified_count=8, champion_identified_count=2,
                         executive_sponsor_deals=1)
        pat = self._call(inp, 10.0, 10.0, 30.0, 30.0)
        assert pat == StakeholderPattern.champion_gap


# ---------------------------------------------------------------------------
# 7. _risk_level boundaries
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def setup_method(self):
        self.eng = engine()

    def test_below_20_is_low(self):
        assert self.eng._risk_level(0.0) == StakeholderRisk.low
        assert self.eng._risk_level(19.9) == StakeholderRisk.low

    def test_exactly_20_is_moderate(self):
        assert self.eng._risk_level(20.0) == StakeholderRisk.moderate

    def test_between_20_and_40_is_moderate(self):
        assert self.eng._risk_level(30.0) == StakeholderRisk.moderate
        assert self.eng._risk_level(39.9) == StakeholderRisk.moderate

    def test_exactly_40_is_high(self):
        assert self.eng._risk_level(40.0) == StakeholderRisk.high

    def test_between_40_and_60_is_high(self):
        assert self.eng._risk_level(50.0) == StakeholderRisk.high
        assert self.eng._risk_level(59.9) == StakeholderRisk.high

    def test_exactly_60_is_critical(self):
        assert self.eng._risk_level(60.0) == StakeholderRisk.critical

    def test_above_60_is_critical(self):
        assert self.eng._risk_level(80.0) == StakeholderRisk.critical
        assert self.eng._risk_level(100.0) == StakeholderRisk.critical


# ---------------------------------------------------------------------------
# 8. _severity boundaries
# ---------------------------------------------------------------------------

class TestSeverity:
    def setup_method(self):
        self.eng = engine()

    def test_below_20_is_engaged(self):
        assert self.eng._severity(0.0) == StakeholderSeverity.engaged
        assert self.eng._severity(19.9) == StakeholderSeverity.engaged

    def test_exactly_20_is_developing(self):
        assert self.eng._severity(20.0) == StakeholderSeverity.developing

    def test_between_20_and_40_is_developing(self):
        assert self.eng._severity(30.0) == StakeholderSeverity.developing
        assert self.eng._severity(39.9) == StakeholderSeverity.developing

    def test_exactly_40_is_fragile(self):
        assert self.eng._severity(40.0) == StakeholderSeverity.fragile

    def test_between_40_and_60_is_fragile(self):
        assert self.eng._severity(50.0) == StakeholderSeverity.fragile
        assert self.eng._severity(59.9) == StakeholderSeverity.fragile

    def test_exactly_60_is_exposed(self):
        assert self.eng._severity(60.0) == StakeholderSeverity.exposed

    def test_above_60_is_exposed(self):
        assert self.eng._severity(80.0) == StakeholderSeverity.exposed
        assert self.eng._severity(100.0) == StakeholderSeverity.exposed


# ---------------------------------------------------------------------------
# 9. _action for all risk × pattern combos
# ---------------------------------------------------------------------------

class TestAction:
    def setup_method(self):
        self.eng = engine()

    # critical
    def test_critical_single_threaded(self):
        assert self.eng._action(StakeholderRisk.critical, StakeholderPattern.single_threaded) == StakeholderAction.multi_threading_coaching

    def test_critical_no_economic_buyer(self):
        assert self.eng._action(StakeholderRisk.critical, StakeholderPattern.no_economic_buyer) == StakeholderAction.economic_buyer_strategy

    def test_critical_champion_gap(self):
        assert self.eng._action(StakeholderRisk.critical, StakeholderPattern.champion_gap) == StakeholderAction.stakeholder_mapping_review

    def test_critical_executive_avoidance(self):
        assert self.eng._action(StakeholderRisk.critical, StakeholderPattern.executive_avoidance) == StakeholderAction.stakeholder_mapping_review

    def test_critical_poor_stakeholder_advancement(self):
        assert self.eng._action(StakeholderRisk.critical, StakeholderPattern.poor_stakeholder_advancement) == StakeholderAction.stakeholder_mapping_review

    def test_critical_none(self):
        assert self.eng._action(StakeholderRisk.critical, StakeholderPattern.none) == StakeholderAction.stakeholder_mapping_review

    # high
    def test_high_champion_gap(self):
        assert self.eng._action(StakeholderRisk.high, StakeholderPattern.champion_gap) == StakeholderAction.champion_development

    def test_high_executive_avoidance(self):
        assert self.eng._action(StakeholderRisk.high, StakeholderPattern.executive_avoidance) == StakeholderAction.executive_access_plan

    def test_high_single_threaded(self):
        assert self.eng._action(StakeholderRisk.high, StakeholderPattern.single_threaded) == StakeholderAction.multi_threading_coaching

    def test_high_no_economic_buyer(self):
        assert self.eng._action(StakeholderRisk.high, StakeholderPattern.no_economic_buyer) == StakeholderAction.multi_threading_coaching

    def test_high_poor_stakeholder_advancement(self):
        assert self.eng._action(StakeholderRisk.high, StakeholderPattern.poor_stakeholder_advancement) == StakeholderAction.multi_threading_coaching

    def test_high_none(self):
        assert self.eng._action(StakeholderRisk.high, StakeholderPattern.none) == StakeholderAction.multi_threading_coaching

    # moderate
    def test_moderate_any_pattern_returns_coaching(self):
        for pat in StakeholderPattern:
            result = self.eng._action(StakeholderRisk.moderate, pat)
            assert result == StakeholderAction.multi_threading_coaching

    # low
    def test_low_any_pattern_returns_no_action(self):
        for pat in StakeholderPattern:
            result = self.eng._action(StakeholderRisk.low, pat)
            assert result == StakeholderAction.no_action


# ---------------------------------------------------------------------------
# 10. _has_stakeholder_gap
# ---------------------------------------------------------------------------

class TestHasStakeholderGap:
    def setup_method(self):
        self.eng = engine()

    def test_gap_true_composite_ge_40(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0,
                         champion_identified_count=5)
        assert self.eng._has_stakeholder_gap(40.0, inp) is True

    def test_gap_false_composite_below_40_single_rate_low_champion_present(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=2,
                         champion_identified_count=5)
        # composite=30 (<40); single_rate=0.20 (<0.50); champion>0
        assert self.eng._has_stakeholder_gap(30.0, inp) is False

    def test_gap_true_single_rate_ge_50pct(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=5,
                         champion_identified_count=5)
        # composite=10 (<40), single_rate=0.50 >=0.50
        assert self.eng._has_stakeholder_gap(10.0, inp) is True

    def test_gap_true_single_rate_just_at_50pct(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=5,
                         champion_identified_count=5)
        assert self.eng._has_stakeholder_gap(5.0, inp) is True

    def test_gap_false_single_rate_just_below_50pct(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=4,
                         champion_identified_count=5)
        # 0.40 < 0.50; composite < 40; champion > 0
        assert self.eng._has_stakeholder_gap(5.0, inp) is False

    def test_gap_true_champion_zero(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         champion_identified_count=0)
        # composite<40, single_rate<0.50, but champion==0
        assert self.eng._has_stakeholder_gap(10.0, inp) is True

    def test_gap_false_all_conditions_negative(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         champion_identified_count=5)
        assert self.eng._has_stakeholder_gap(10.0, inp) is False

    def test_gap_true_only_composite(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         champion_identified_count=5)
        assert self.eng._has_stakeholder_gap(60.0, inp) is True

    def test_gap_boundary_composite_exactly_40(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         champion_identified_count=5)
        assert self.eng._has_stakeholder_gap(40.0, inp) is True

    def test_gap_boundary_composite_just_below_40(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=1,
                         champion_identified_count=5)
        assert self.eng._has_stakeholder_gap(39.9, inp) is False


# ---------------------------------------------------------------------------
# 11. _requires_stakeholder_coaching
# ---------------------------------------------------------------------------

class TestRequiresStakeholderCoaching:
    def setup_method(self):
        self.eng = engine()

    def test_coaching_true_composite_ge_30(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=5,
                         avg_contacts_per_deal=3.0)
        assert self.eng._requires_stakeholder_coaching(30.0, inp) is True

    def test_coaching_false_all_negative(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=5,
                         avg_contacts_per_deal=3.0)
        # composite=10 <30; eb_rate=0.50 >=0.40; contacts=3.0 >=2.0
        assert self.eng._requires_stakeholder_coaching(10.0, inp) is False

    def test_coaching_true_eb_rate_below_40pct(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=3,
                         avg_contacts_per_deal=3.0)
        # eb_rate=0.30 <0.40
        assert self.eng._requires_stakeholder_coaching(10.0, inp) is True

    def test_coaching_false_eb_rate_exactly_40pct(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=4,
                         avg_contacts_per_deal=3.0)
        # eb_rate=0.40 NOT <0.40; composite<30; contacts>=2.0
        assert self.eng._requires_stakeholder_coaching(10.0, inp) is False

    def test_coaching_true_contacts_below_2(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=5,
                         avg_contacts_per_deal=1.9)
        assert self.eng._requires_stakeholder_coaching(10.0, inp) is True

    def test_coaching_false_contacts_exactly_2(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=5,
                         avg_contacts_per_deal=2.0)
        # contacts=2.0 NOT <2.0; eb_rate=0.50 >=0.40; composite<30
        assert self.eng._requires_stakeholder_coaching(10.0, inp) is False

    def test_coaching_boundary_composite_just_below_30(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=5,
                         avg_contacts_per_deal=3.0)
        assert self.eng._requires_stakeholder_coaching(29.9, inp) is False

    def test_coaching_boundary_composite_exactly_30(self):
        inp = make_input(total_active_deals=10, economic_buyer_identified_count=5,
                         avg_contacts_per_deal=3.0)
        assert self.eng._requires_stakeholder_coaching(30.0, inp) is True


# ---------------------------------------------------------------------------
# 12. _estimated_deal_risk
# ---------------------------------------------------------------------------

class TestEstimatedDealRisk:
    def setup_method(self):
        self.eng = engine()

    def test_basic_calculation(self):
        inp = make_input(single_threaded_deals=5, avg_deal_size_single_stakeholder_usd=10000.0)
        result = self.eng._estimated_deal_risk(inp, 50.0)
        assert result == round(5 * 10000.0 * 0.50, 2)

    def test_zero_composite(self):
        inp = make_input(single_threaded_deals=5, avg_deal_size_single_stakeholder_usd=10000.0)
        assert self.eng._estimated_deal_risk(inp, 0.0) == 0.0

    def test_zero_single_threaded_deals(self):
        inp = make_input(single_threaded_deals=0, avg_deal_size_single_stakeholder_usd=10000.0)
        assert self.eng._estimated_deal_risk(inp, 50.0) == 0.0

    def test_zero_deal_size(self):
        inp = make_input(single_threaded_deals=5, avg_deal_size_single_stakeholder_usd=0.0)
        assert self.eng._estimated_deal_risk(inp, 50.0) == 0.0

    def test_composite_100(self):
        inp = make_input(single_threaded_deals=2, avg_deal_size_single_stakeholder_usd=20000.0)
        assert self.eng._estimated_deal_risk(inp, 100.0) == 40000.0

    def test_returns_rounded_float(self):
        inp = make_input(single_threaded_deals=3, avg_deal_size_single_stakeholder_usd=33333.33)
        result = self.eng._estimated_deal_risk(inp, 33.0)
        expected = round(3 * 33333.33 * 0.33, 2)
        assert result == expected

    def test_large_values(self):
        inp = make_input(single_threaded_deals=20, avg_deal_size_single_stakeholder_usd=500000.0)
        result = self.eng._estimated_deal_risk(inp, 75.0)
        assert result == round(20 * 500000.0 * 0.75, 2)


# ---------------------------------------------------------------------------
# 13. _signal
# ---------------------------------------------------------------------------

class TestSignal:
    def setup_method(self):
        self.eng = engine()

    def test_on_track_signal(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0,
                         champion_identified_count=10, executive_sponsor_deals=10)
        sig = self.eng._signal(inp, StakeholderPattern.none, 10.0)
        assert sig == "Stakeholder engagement and multi-threading on track"

    def test_none_pattern_high_composite_not_on_track(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=3,
                         champion_identified_count=10, executive_sponsor_deals=10)
        sig = self.eng._signal(inp, StakeholderPattern.none, 25.0)
        assert "Stakeholder risk" in sig

    def test_single_threaded_label_in_signal(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=6,
                         champion_identified_count=10, executive_sponsor_deals=10)
        sig = self.eng._signal(inp, StakeholderPattern.single_threaded, 50.0)
        assert "single threaded" in sig.lower()

    def test_single_threaded_count_in_signal(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=6,
                         champion_identified_count=10, executive_sponsor_deals=10)
        sig = self.eng._signal(inp, StakeholderPattern.single_threaded, 50.0)
        assert "6 single-threaded deals" in sig

    def test_champion_count_in_signal(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0,
                         champion_identified_count=3, executive_sponsor_deals=10)
        sig = self.eng._signal(inp, StakeholderPattern.champion_gap, 35.0)
        assert "3 champions identified" in sig

    def test_exec_sponsor_count_in_signal(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0,
                         champion_identified_count=10, executive_sponsor_deals=2)
        sig = self.eng._signal(inp, StakeholderPattern.executive_avoidance, 35.0)
        assert "2 exec sponsors engaged" in sig

    def test_composite_value_in_signal(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=3,
                         champion_identified_count=5, executive_sponsor_deals=2)
        sig = self.eng._signal(inp, StakeholderPattern.none, 42.0)
        assert "composite 42" in sig

    def test_none_pattern_with_all_parts(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=3,
                         champion_identified_count=5, executive_sponsor_deals=2)
        sig = self.eng._signal(inp, StakeholderPattern.none, 42.0)
        assert "Stakeholder risk" in sig

    def test_no_parts_fallback_message(self):
        # All counts at their totals so no parts are appended
        inp = make_input(total_active_deals=10, single_threaded_deals=0,
                         champion_identified_count=10, executive_sponsor_deals=10)
        sig = self.eng._signal(inp, StakeholderPattern.none, 25.0)
        assert "stakeholder engagement declining" in sig

    def test_pattern_value_capitalized_in_label(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=5,
                         champion_identified_count=10, executive_sponsor_deals=10)
        sig = self.eng._signal(inp, StakeholderPattern.single_threaded, 50.0)
        assert sig[0].isupper()

    def test_underscores_replaced_in_label(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=5,
                         champion_identified_count=5, executive_sponsor_deals=1)
        sig = self.eng._signal(inp, StakeholderPattern.poor_stakeholder_advancement, 30.0)
        assert "poor stakeholder advancement" in sig.lower()


# ---------------------------------------------------------------------------
# 14. assess() → StakeholderMappingResult & to_dict() 15 keys
# ---------------------------------------------------------------------------

class TestAssess:
    def setup_method(self):
        self.eng = engine()
        self.inp = make_input()

    def test_returns_result_type(self):
        r = self.eng.assess(self.inp)
        assert isinstance(r, StakeholderMappingResult)

    def test_rep_id_preserved(self):
        r = self.eng.assess(self.inp)
        assert r.rep_id == "REP-001"

    def test_region_preserved(self):
        r = self.eng.assess(self.inp)
        assert r.region == "Northeast"

    def test_to_dict_has_15_keys(self):
        r = self.eng.assess(self.inp)
        d = r.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self):
        r = self.eng.assess(self.inp)
        d = r.to_dict()
        expected_keys = {
            "rep_id", "region", "stakeholder_risk", "stakeholder_pattern",
            "stakeholder_severity", "recommended_action",
            "coverage_breadth_score", "buyer_alignment_score",
            "champion_development_score", "executive_access_score",
            "stakeholder_effectiveness_composite",
            "has_stakeholder_gap", "requires_stakeholder_coaching",
            "estimated_deal_risk_usd", "stakeholder_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        r = self.eng.assess(self.inp)
        d = r.to_dict()
        assert isinstance(d["stakeholder_risk"], str)
        assert isinstance(d["stakeholder_pattern"], str)
        assert isinstance(d["stakeholder_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_composite_is_weighted_average(self):
        r = self.eng.assess(self.inp)
        expected = round(
            r.coverage_breadth_score * 0.30
            + r.buyer_alignment_score * 0.30
            + r.champion_development_score * 0.25
            + r.executive_access_score * 0.15,
            1,
        )
        assert r.stakeholder_effectiveness_composite == expected

    def test_scores_are_floats_within_range(self):
        r = self.eng.assess(self.inp)
        for score in [r.coverage_breadth_score, r.buyer_alignment_score,
                      r.champion_development_score, r.executive_access_score,
                      r.stakeholder_effectiveness_composite]:
            assert 0.0 <= score <= 100.0

    def test_result_appended_to_internal_list(self):
        self.eng.assess(self.inp)
        assert len(self.eng._results) == 1

    def test_multiple_assessments_accumulate(self):
        self.eng.assess(self.inp)
        self.eng.assess(self.inp)
        assert len(self.eng._results) == 2

    def test_estimated_deal_risk_usd_matches_formula(self):
        r = self.eng.assess(self.inp)
        expected = round(
            self.inp.single_threaded_deals
            * self.inp.avg_deal_size_single_stakeholder_usd
            * (r.stakeholder_effectiveness_composite / 100.0),
            2,
        )
        assert r.estimated_deal_risk_usd == expected

    def test_risk_consistent_with_composite(self):
        r = self.eng.assess(self.inp)
        c = r.stakeholder_effectiveness_composite
        if c >= 60:
            assert r.stakeholder_risk == StakeholderRisk.critical
        elif c >= 40:
            assert r.stakeholder_risk == StakeholderRisk.high
        elif c >= 20:
            assert r.stakeholder_risk == StakeholderRisk.moderate
        else:
            assert r.stakeholder_risk == StakeholderRisk.low

    def test_severity_consistent_with_composite(self):
        r = self.eng.assess(self.inp)
        c = r.stakeholder_effectiveness_composite
        if c >= 60:
            assert r.stakeholder_severity == StakeholderSeverity.exposed
        elif c >= 40:
            assert r.stakeholder_severity == StakeholderSeverity.fragile
        elif c >= 20:
            assert r.stakeholder_severity == StakeholderSeverity.developing
        else:
            assert r.stakeholder_severity == StakeholderSeverity.engaged

    def test_healthy_rep_gets_low_risk(self):
        r = self.eng.assess(self.inp)
        assert r.stakeholder_risk == StakeholderRisk.low

    def test_single_threaded_rep_gets_high_risk(self):
        inp = make_input(
            total_active_deals=10, single_threaded_deals=8, multi_threaded_deals=2,
            avg_contacts_per_deal=1.0, economic_buyer_identified_count=1,
            economic_buyer_engaged_count=0, champion_identified_count=1,
            champion_active_count=0, executive_sponsor_deals=0,
            decision_maker_met_count=0, avg_stakeholder_influence_score=2.0,
            deals_stalled_no_champion=5, committee_buying_deals=3,
        )
        r = self.eng.assess(inp)
        assert r.stakeholder_risk in (StakeholderRisk.high, StakeholderRisk.critical)


# ---------------------------------------------------------------------------
# 15. summary() → 13 keys
# ---------------------------------------------------------------------------

class TestSummary:
    def setup_method(self):
        self.eng = engine()

    def test_summary_empty_returns_13_keys(self):
        s = self.eng.summary()
        assert len(s) == 13

    def test_summary_empty_total_zero(self):
        s = self.eng.summary()
        assert s["total"] == 0

    def test_summary_empty_risk_counts_empty(self):
        s = self.eng.summary()
        assert s["risk_counts"] == {}

    def test_summary_empty_pattern_counts_empty(self):
        s = self.eng.summary()
        assert s["pattern_counts"] == {}

    def test_summary_empty_severity_counts_empty(self):
        s = self.eng.summary()
        assert s["severity_counts"] == {}

    def test_summary_empty_action_counts_empty(self):
        s = self.eng.summary()
        assert s["action_counts"] == {}

    def test_summary_empty_avg_composite_zero(self):
        s = self.eng.summary()
        assert s["avg_stakeholder_effectiveness_composite"] == 0.0

    def test_summary_empty_total_deal_risk_zero(self):
        s = self.eng.summary()
        assert s["total_estimated_deal_risk_usd"] == 0.0

    def test_summary_after_assess_has_correct_total(self):
        inp = make_input()
        self.eng.assess(inp)
        self.eng.assess(inp)
        s = self.eng.summary()
        assert s["total"] == 2

    def test_summary_13_keys_after_assess(self):
        inp = make_input()
        self.eng.assess(inp)
        s = self.eng.summary()
        assert len(s) == 13

    def test_summary_key_names(self):
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_stakeholder_effectiveness_composite",
            "stakeholder_gap_count", "stakeholder_coaching_count",
            "avg_coverage_breadth_score", "avg_buyer_alignment_score",
            "avg_champion_development_score", "avg_executive_access_score",
            "total_estimated_deal_risk_usd",
        }
        s = self.eng.summary()
        assert set(s.keys()) == expected_keys

    def test_summary_risk_counts_populated(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        total_from_counts = sum(s["risk_counts"].values())
        assert total_from_counts == 1

    def test_summary_pattern_counts_populated(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        total_from_counts = sum(s["pattern_counts"].values())
        assert total_from_counts == 1

    def test_summary_severity_counts_populated(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        total_from_counts = sum(s["severity_counts"].values())
        assert total_from_counts == 1

    def test_summary_action_counts_populated(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        total_from_counts = sum(s["action_counts"].values())
        assert total_from_counts == 1

    def test_summary_gap_count(self):
        self.eng.assess(make_input())  # healthy rep → False
        s = self.eng.summary()
        assert s["stakeholder_gap_count"] == 0

    def test_summary_coaching_count(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        assert isinstance(s["stakeholder_coaching_count"], int)

    def test_summary_avg_scores_non_negative(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        assert s["avg_coverage_breadth_score"] >= 0.0
        assert s["avg_buyer_alignment_score"] >= 0.0
        assert s["avg_champion_development_score"] >= 0.0
        assert s["avg_executive_access_score"] >= 0.0

    def test_summary_total_deal_risk_sum(self):
        inp = make_input()
        r = self.eng.assess(inp)
        s = self.eng.summary()
        assert s["total_estimated_deal_risk_usd"] == round(r.estimated_deal_risk_usd, 2)

    def test_summary_resets_with_new_engine(self):
        eng2 = engine()
        s = eng2.summary()
        assert s["total"] == 0

    def test_summary_avg_composite_matches_manual_average(self):
        inp = make_input()
        r = self.eng.assess(inp)
        s = self.eng.summary()
        assert s["avg_stakeholder_effectiveness_composite"] == r.stakeholder_effectiveness_composite


# ---------------------------------------------------------------------------
# 16. assess_batch()
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def setup_method(self):
        self.eng = engine()

    def test_batch_returns_list(self):
        results = self.eng.assess_batch([make_input(), make_input()])
        assert isinstance(results, list)

    def test_batch_length_matches_input(self):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(5)]
        results = self.eng.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_empty_returns_empty_list(self):
        results = self.eng.assess_batch([])
        assert results == []

    def test_batch_preserves_rep_ids(self):
        inputs = [make_input(rep_id=f"REP-{i}") for i in range(3)]
        results = self.eng.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"REP-{i}"

    def test_batch_accumulates_in_results(self):
        self.eng.assess_batch([make_input(), make_input(), make_input()])
        assert len(self.eng._results) == 3

    def test_batch_results_all_result_type(self):
        results = self.eng.assess_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, StakeholderMappingResult)

    def test_batch_then_summary_total(self):
        self.eng.assess_batch([make_input() for _ in range(7)])
        s = self.eng.summary()
        assert s["total"] == 7

    def test_batch_single_item(self):
        results = self.eng.assess_batch([make_input()])
        assert len(results) == 1

    def test_batch_different_regions(self):
        inputs = [make_input(region="East"), make_input(region="West")]
        results = self.eng.assess_batch(inputs)
        assert results[0].region == "East"
        assert results[1].region == "West"


# ---------------------------------------------------------------------------
# 17. End-to-end / integration scenarios
# ---------------------------------------------------------------------------

class TestEndToEndScenarios:
    def setup_method(self):
        self.eng = engine()

    def test_perfect_rep_all_low(self):
        inp = make_input(
            total_active_deals=10, single_threaded_deals=0, multi_threaded_deals=10,
            avg_contacts_per_deal=4.0, economic_buyer_identified_count=10,
            economic_buyer_engaged_count=10, champion_identified_count=10,
            champion_active_count=10, executive_sponsor_deals=5,
            decision_maker_met_count=10, avg_stakeholder_influence_score=8.0,
            deals_stalled_no_champion=0, committee_buying_deals=0,
        )
        r = self.eng.assess(inp)
        assert r.stakeholder_risk == StakeholderRisk.low
        assert r.stakeholder_severity == StakeholderSeverity.engaged
        assert r.recommended_action == StakeholderAction.no_action
        assert r.has_stakeholder_gap is False

    def test_worst_rep_all_critical(self):
        inp = make_input(
            total_active_deals=10, single_threaded_deals=9, multi_threaded_deals=1,
            avg_contacts_per_deal=1.0, economic_buyer_identified_count=1,
            economic_buyer_engaged_count=0, champion_identified_count=1,
            champion_active_count=0, executive_sponsor_deals=0,
            decision_maker_met_count=0, avg_stakeholder_influence_score=1.0,
            deals_stalled_no_champion=5, committee_buying_deals=3,
        )
        r = self.eng.assess(inp)
        assert r.stakeholder_risk == StakeholderRisk.critical

    def test_assess_and_summary_consistency(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        self.eng.assess_batch(inputs)
        s = self.eng.summary()
        assert s["total"] == 5
        assert sum(s["risk_counts"].values()) == 5
        assert sum(s["pattern_counts"].values()) == 5
        assert sum(s["severity_counts"].values()) == 5
        assert sum(s["action_counts"].values()) == 5

    def test_gap_count_in_summary_all_healthy(self):
        inputs = [make_input() for _ in range(3)]
        self.eng.assess_batch(inputs)
        s = self.eng.summary()
        # All healthy → no gaps
        assert s["stakeholder_gap_count"] == 0

    def test_gap_count_in_summary_all_single_threaded(self):
        inputs = [make_input(total_active_deals=10, single_threaded_deals=6,
                             champion_identified_count=1) for _ in range(3)]
        self.eng.assess_batch(inputs)
        s = self.eng.summary()
        assert s["stakeholder_gap_count"] == 3

    def test_to_dict_boolean_types(self):
        r = self.eng.assess(make_input())
        d = r.to_dict()
        assert isinstance(d["has_stakeholder_gap"], bool)
        assert isinstance(d["requires_stakeholder_coaching"], bool)

    def test_signal_string_is_non_empty(self):
        r = self.eng.assess(make_input())
        assert isinstance(r.stakeholder_signal, str)
        assert len(r.stakeholder_signal) > 0

    def test_multiple_engines_independent(self):
        eng1 = SalesStakeholderMappingIntelligenceEngine()
        eng2 = SalesStakeholderMappingIntelligenceEngine()
        eng1.assess(make_input())
        assert len(eng2._results) == 0

    def test_composite_capped_at_100(self):
        inp = make_input(
            total_active_deals=1, single_threaded_deals=1, multi_threaded_deals=0,
            avg_contacts_per_deal=0.5, economic_buyer_identified_count=0,
            economic_buyer_engaged_count=0, champion_identified_count=0,
            champion_active_count=0, executive_sponsor_deals=0,
            decision_maker_met_count=0, avg_stakeholder_influence_score=1.0,
            deals_stalled_no_champion=5, committee_buying_deals=2,
        )
        r = self.eng.assess(inp)
        assert r.stakeholder_effectiveness_composite <= 100.0

    def test_to_dict_numeric_types(self):
        r = self.eng.assess(make_input())
        d = r.to_dict()
        for key in ["coverage_breadth_score", "buyer_alignment_score",
                    "champion_development_score", "executive_access_score",
                    "stakeholder_effectiveness_composite", "estimated_deal_risk_usd"]:
            assert isinstance(d[key], (int, float))


# ---------------------------------------------------------------------------
# 18. Additional edge-case tests
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def setup_method(self):
        self.eng = engine()

    def test_single_deal_total(self):
        inp = make_input(total_active_deals=1, single_threaded_deals=1,
                         multi_threaded_deals=0)
        r = self.eng.assess(inp)
        assert r is not None

    def test_zero_total_active_deals(self):
        inp = make_input(total_active_deals=0, single_threaded_deals=0,
                         multi_threaded_deals=0)
        r = self.eng.assess(inp)
        assert r is not None

    def test_large_deal_counts(self):
        inp = make_input(total_active_deals=1000, single_threaded_deals=100,
                         multi_threaded_deals=900, avg_contacts_per_deal=5.0,
                         economic_buyer_identified_count=900,
                         economic_buyer_engaged_count=800,
                         champion_identified_count=900, champion_active_count=800,
                         executive_sponsor_deals=400, decision_maker_met_count=900)
        r = self.eng.assess(inp)
        assert r.stakeholder_risk == StakeholderRisk.low

    def test_exact_boundary_composite_20_gives_moderate(self):
        # Craft inputs to yield exactly composite ≈ 20
        # We call _risk_level directly for precision
        assert self.eng._risk_level(20.0) == StakeholderRisk.moderate
        assert self.eng._severity(20.0) == StakeholderSeverity.developing

    def test_exact_boundary_composite_40_gives_high(self):
        assert self.eng._risk_level(40.0) == StakeholderRisk.high
        assert self.eng._severity(40.0) == StakeholderSeverity.fragile

    def test_exact_boundary_composite_60_gives_critical(self):
        assert self.eng._risk_level(60.0) == StakeholderRisk.critical
        assert self.eng._severity(60.0) == StakeholderSeverity.exposed

    def test_rep_id_and_region_roundtrip(self):
        inp = make_input(rep_id="SPECIAL-999", region="Pacific")
        r = self.eng.assess(inp)
        d = r.to_dict()
        assert d["rep_id"] == "SPECIAL-999"
        assert d["region"] == "Pacific"

    def test_no_multi_threaded_adds_20_to_coverage(self):
        base = make_input(total_active_deals=10, single_threaded_deals=0,
                          avg_contacts_per_deal=3.0, multi_threaded_deals=3)
        with_zero = make_input(total_active_deals=10, single_threaded_deals=0,
                               avg_contacts_per_deal=3.0, multi_threaded_deals=0)
        s_base = self.eng._coverage_breadth_score(base)
        s_zero = self.eng._coverage_breadth_score(with_zero)
        assert s_zero - s_base == 20.0

    def test_high_exec_rate_no_committee_zero_score(self):
        inp = make_input(total_active_deals=10, executive_sponsor_deals=5,
                         avg_stakeholder_influence_score=8.0, committee_buying_deals=0)
        s = self.eng._executive_access_score(inp)
        assert s == 0.0

    def test_pattern_none_low_composite_signal(self):
        inp = make_input(total_active_deals=10, single_threaded_deals=0,
                         champion_identified_count=10, executive_sponsor_deals=10)
        sig = self.eng._signal(inp, StakeholderPattern.none, 10.0)
        assert "on track" in sig.lower()

    def test_assess_batch_preserves_order(self):
        inputs = [make_input(rep_id=f"X-{i}") for i in range(10)]
        results = self.eng.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"X-{i}"

    def test_summary_avg_composite_is_float(self):
        self.eng.assess(make_input())
        s = self.eng.summary()
        assert isinstance(s["avg_stakeholder_effectiveness_composite"], float)

    def test_deal_risk_non_negative(self):
        r = self.eng.assess(make_input())
        assert r.estimated_deal_risk_usd >= 0.0

    def test_coverage_score_returns_float(self):
        inp = make_input()
        s = self.eng._coverage_breadth_score(inp)
        assert isinstance(s, float)

    def test_buyer_score_returns_float(self):
        inp = make_input()
        s = self.eng._buyer_alignment_score(inp)
        assert isinstance(s, float)

    def test_champion_score_returns_float(self):
        inp = make_input()
        s = self.eng._champion_development_score(inp)
        assert isinstance(s, float)

    def test_executive_score_returns_float(self):
        inp = make_input()
        s = self.eng._executive_access_score(inp)
        assert isinstance(s, float)
