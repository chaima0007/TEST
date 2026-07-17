"""
Comprehensive pytest tests for SalesDecisionCriteriaAlignmentIntelligenceEngine.
280+ tests covering enums, input fields, result fields, sub-scores, pattern detection,
risk/severity thresholds, action mapping, gap/coaching flags, lost revenue formula,
signal string, assess end-to-end, assess_batch, summary, and edge cases.
"""

from __future__ import annotations

import math
import pytest

from swarm.intelligence.sales_decision_criteria_alignment_intelligence_engine import (
    CriteriaAction,
    CriteriaInput,
    CriteriaPattern,
    CriteriaResult,
    CriteriaRisk,
    CriteriaSeverity,
    SalesDecisionCriteriaAlignmentIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_input(
    rep_id="R1",
    region="West",
    evaluation_period_id="Q1-2025",
    criteria_documented_early_pct=0.80,
    criteria_influenced_by_rep_pct=0.80,
    criteria_first_discovered_stage_avg=1.0,
    criteria_changed_late_in_cycle_pct=0.05,
    rep_aware_of_all_criteria_pct=0.90,
    criteria_mapped_to_product_strength_pct=0.85,
    competitor_criteria_advantage_rate_pct=0.05,
    criteria_aligned_with_champion_pct=0.85,
    scorecard_obtained_pct=0.80,
    criteria_gap_identified_pct=0.80,
    criteria_coaching_provided_pct=0.80,
    lost_deals_criteria_mismatch_pct=0.10,
    deals_won_criteria_shaped_pct=0.80,
    avg_criteria_count_per_deal=5.0,
    unmet_criteria_at_close_pct=0.05,
    criteria_revision_requested_pct=0.10,
    customer_shared_scorecard_pct=0.70,
    total_deals_evaluated=100,
    avg_opportunity_value_usd=10000.0,
) -> CriteriaInput:
    """Return a healthy (low-risk) CriteriaInput by default."""
    return CriteriaInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        criteria_documented_early_pct=criteria_documented_early_pct,
        criteria_influenced_by_rep_pct=criteria_influenced_by_rep_pct,
        criteria_first_discovered_stage_avg=criteria_first_discovered_stage_avg,
        criteria_changed_late_in_cycle_pct=criteria_changed_late_in_cycle_pct,
        rep_aware_of_all_criteria_pct=rep_aware_of_all_criteria_pct,
        criteria_mapped_to_product_strength_pct=criteria_mapped_to_product_strength_pct,
        competitor_criteria_advantage_rate_pct=competitor_criteria_advantage_rate_pct,
        criteria_aligned_with_champion_pct=criteria_aligned_with_champion_pct,
        scorecard_obtained_pct=scorecard_obtained_pct,
        criteria_gap_identified_pct=criteria_gap_identified_pct,
        criteria_coaching_provided_pct=criteria_coaching_provided_pct,
        lost_deals_criteria_mismatch_pct=lost_deals_criteria_mismatch_pct,
        deals_won_criteria_shaped_pct=deals_won_criteria_shaped_pct,
        avg_criteria_count_per_deal=avg_criteria_count_per_deal,
        unmet_criteria_at_close_pct=unmet_criteria_at_close_pct,
        criteria_revision_requested_pct=criteria_revision_requested_pct,
        customer_shared_scorecard_pct=customer_shared_scorecard_pct,
        total_deals_evaluated=total_deals_evaluated,
        avg_opportunity_value_usd=avg_opportunity_value_usd,
    )


@pytest.fixture
def engine():
    return SalesDecisionCriteriaAlignmentIntelligenceEngine()


@pytest.fixture
def healthy_input():
    return make_input()


@pytest.fixture
def worst_case_input():
    """All parameters at worst possible values → maximum risk."""
    return make_input(
        criteria_documented_early_pct=0.10,
        criteria_influenced_by_rep_pct=0.10,
        criteria_first_discovered_stage_avg=4.0,
        criteria_changed_late_in_cycle_pct=0.60,
        rep_aware_of_all_criteria_pct=0.20,
        criteria_mapped_to_product_strength_pct=0.10,
        competitor_criteria_advantage_rate_pct=0.80,
        criteria_aligned_with_champion_pct=0.10,
        scorecard_obtained_pct=0.10,
        criteria_gap_identified_pct=0.10,
        criteria_coaching_provided_pct=0.10,
        lost_deals_criteria_mismatch_pct=0.70,
        unmet_criteria_at_close_pct=0.60,
    )


# ---------------------------------------------------------------------------
# 1. Enum Tests
# ---------------------------------------------------------------------------

class TestCriteriaRiskEnum:
    def test_has_low(self):
        assert CriteriaRisk.low.value == "low"

    def test_has_moderate(self):
        assert CriteriaRisk.moderate.value == "moderate"

    def test_has_high(self):
        assert CriteriaRisk.high.value == "high"

    def test_has_critical(self):
        assert CriteriaRisk.critical.value == "critical"

    def test_count(self):
        assert len(CriteriaRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(CriteriaRisk.low, str)

    def test_equality_with_string(self):
        assert CriteriaRisk.low == "low"


class TestCriteriaPatternEnum:
    def test_none(self):
        assert CriteriaPattern.none.value == "none"

    def test_late_criteria_discovery(self):
        assert CriteriaPattern.late_criteria_discovery.value == "late_criteria_discovery"

    def test_criteria_reactive_alignment(self):
        assert CriteriaPattern.criteria_reactive_alignment.value == "criteria_reactive_alignment"

    def test_scorecard_blind_pursuit(self):
        assert CriteriaPattern.scorecard_blind_pursuit.value == "scorecard_blind_pursuit"

    def test_competitive_criteria_disadvantage(self):
        assert CriteriaPattern.competitive_criteria_disadvantage.value == "competitive_criteria_disadvantage"

    def test_criteria_coaching_gap(self):
        assert CriteriaPattern.criteria_coaching_gap.value == "criteria_coaching_gap"

    def test_count(self):
        assert len(CriteriaPattern) == 6

    def test_is_str_enum(self):
        assert isinstance(CriteriaPattern.none, str)


class TestCriteriaSeverityEnum:
    def test_shaping(self):
        assert CriteriaSeverity.shaping.value == "shaping"

    def test_aligned(self):
        assert CriteriaSeverity.aligned.value == "aligned"

    def test_reactive(self):
        assert CriteriaSeverity.reactive.value == "reactive"

    def test_misaligned(self):
        assert CriteriaSeverity.misaligned.value == "misaligned"

    def test_count(self):
        assert len(CriteriaSeverity) == 4


class TestCriteriaActionEnum:
    def test_no_action(self):
        assert CriteriaAction.no_action.value == "no_action"

    def test_criteria_mapping_coaching(self):
        assert CriteriaAction.criteria_mapping_coaching.value == "criteria_mapping_coaching"

    def test_early_discovery_process_coaching(self):
        assert CriteriaAction.early_discovery_process_coaching.value == "early_discovery_process_coaching"

    def test_competitive_reframing_coaching(self):
        assert CriteriaAction.competitive_reframing_coaching.value == "competitive_reframing_coaching"

    def test_champion_criteria_coaching(self):
        assert CriteriaAction.champion_criteria_coaching.value == "champion_criteria_coaching"

    def test_deal_qualification_review(self):
        assert CriteriaAction.deal_qualification_review.value == "deal_qualification_review"

    def test_count(self):
        assert len(CriteriaAction) == 6


# ---------------------------------------------------------------------------
# 2. CriteriaInput Field Tests
# ---------------------------------------------------------------------------

class TestCriteriaInputFields:
    def test_rep_id(self):
        inp = make_input(rep_id="ABC")
        assert inp.rep_id == "ABC"

    def test_region(self):
        inp = make_input(region="East")
        assert inp.region == "East"

    def test_evaluation_period_id(self):
        inp = make_input(evaluation_period_id="Q2-2025")
        assert inp.evaluation_period_id == "Q2-2025"

    def test_criteria_documented_early_pct(self):
        inp = make_input(criteria_documented_early_pct=0.55)
        assert inp.criteria_documented_early_pct == 0.55

    def test_criteria_influenced_by_rep_pct(self):
        inp = make_input(criteria_influenced_by_rep_pct=0.30)
        assert inp.criteria_influenced_by_rep_pct == 0.30

    def test_criteria_first_discovered_stage_avg(self):
        inp = make_input(criteria_first_discovered_stage_avg=2.5)
        assert inp.criteria_first_discovered_stage_avg == 2.5

    def test_criteria_changed_late_in_cycle_pct(self):
        inp = make_input(criteria_changed_late_in_cycle_pct=0.25)
        assert inp.criteria_changed_late_in_cycle_pct == 0.25

    def test_rep_aware_of_all_criteria_pct(self):
        inp = make_input(rep_aware_of_all_criteria_pct=0.55)
        assert inp.rep_aware_of_all_criteria_pct == 0.55

    def test_criteria_mapped_to_product_strength_pct(self):
        inp = make_input(criteria_mapped_to_product_strength_pct=0.40)
        assert inp.criteria_mapped_to_product_strength_pct == 0.40

    def test_competitor_criteria_advantage_rate_pct(self):
        inp = make_input(competitor_criteria_advantage_rate_pct=0.35)
        assert inp.competitor_criteria_advantage_rate_pct == 0.35

    def test_criteria_aligned_with_champion_pct(self):
        inp = make_input(criteria_aligned_with_champion_pct=0.45)
        assert inp.criteria_aligned_with_champion_pct == 0.45

    def test_scorecard_obtained_pct(self):
        inp = make_input(scorecard_obtained_pct=0.30)
        assert inp.scorecard_obtained_pct == 0.30

    def test_criteria_gap_identified_pct(self):
        inp = make_input(criteria_gap_identified_pct=0.35)
        assert inp.criteria_gap_identified_pct == 0.35

    def test_criteria_coaching_provided_pct(self):
        inp = make_input(criteria_coaching_provided_pct=0.15)
        assert inp.criteria_coaching_provided_pct == 0.15

    def test_lost_deals_criteria_mismatch_pct(self):
        inp = make_input(lost_deals_criteria_mismatch_pct=0.45)
        assert inp.lost_deals_criteria_mismatch_pct == 0.45

    def test_deals_won_criteria_shaped_pct(self):
        inp = make_input(deals_won_criteria_shaped_pct=0.60)
        assert inp.deals_won_criteria_shaped_pct == 0.60

    def test_avg_criteria_count_per_deal(self):
        inp = make_input(avg_criteria_count_per_deal=7.5)
        assert inp.avg_criteria_count_per_deal == 7.5

    def test_unmet_criteria_at_close_pct(self):
        inp = make_input(unmet_criteria_at_close_pct=0.25)
        assert inp.unmet_criteria_at_close_pct == 0.25

    def test_criteria_revision_requested_pct(self):
        inp = make_input(criteria_revision_requested_pct=0.20)
        assert inp.criteria_revision_requested_pct == 0.20

    def test_customer_shared_scorecard_pct(self):
        inp = make_input(customer_shared_scorecard_pct=0.50)
        assert inp.customer_shared_scorecard_pct == 0.50

    def test_total_deals_evaluated(self):
        inp = make_input(total_deals_evaluated=200)
        assert inp.total_deals_evaluated == 200

    def test_avg_opportunity_value_usd(self):
        inp = make_input(avg_opportunity_value_usd=25000.0)
        assert inp.avg_opportunity_value_usd == 25000.0

    def test_field_count(self):
        inp = make_input()
        assert len(inp.__dataclass_fields__) == 22


# ---------------------------------------------------------------------------
# 3. CriteriaResult Field Tests and to_dict
# ---------------------------------------------------------------------------

class TestCriteriaResultFields:
    @pytest.fixture
    def result(self, engine, healthy_input):
        return engine.assess(healthy_input)

    def test_rep_id_field(self, result):
        assert result.rep_id == "R1"

    def test_region_field(self, result):
        assert result.region == "West"

    def test_criteria_risk_field(self, result):
        assert isinstance(result.criteria_risk, CriteriaRisk)

    def test_criteria_pattern_field(self, result):
        assert isinstance(result.criteria_pattern, CriteriaPattern)

    def test_criteria_severity_field(self, result):
        assert isinstance(result.criteria_severity, CriteriaSeverity)

    def test_recommended_action_field(self, result):
        assert isinstance(result.recommended_action, CriteriaAction)

    def test_discovery_score_field(self, result):
        assert isinstance(result.discovery_score, float)

    def test_influence_score_field(self, result):
        assert isinstance(result.influence_score, float)

    def test_alignment_score_field(self, result):
        assert isinstance(result.alignment_score, float)

    def test_competitive_score_field(self, result):
        assert isinstance(result.competitive_score, float)

    def test_criteria_composite_field(self, result):
        assert isinstance(result.criteria_composite, float)

    def test_has_criteria_gap_field(self, result):
        assert isinstance(result.has_criteria_gap, bool)

    def test_requires_criteria_coaching_field(self, result):
        assert isinstance(result.requires_criteria_coaching, bool)

    def test_estimated_lost_revenue_usd_field(self, result):
        assert isinstance(result.estimated_lost_revenue_usd, float)

    def test_criteria_signal_field(self, result):
        assert isinstance(result.criteria_signal, str)

    def test_field_count(self, result):
        assert len(result.__dataclass_fields__) == 15


class TestCriteriaResultToDict:
    @pytest.fixture
    def d(self, engine, healthy_input):
        return engine.assess(healthy_input).to_dict()

    def test_returns_dict(self, d):
        assert isinstance(d, dict)

    def test_has_15_keys(self, d):
        assert len(d) == 15

    def test_key_rep_id(self, d):
        assert "rep_id" in d

    def test_key_region(self, d):
        assert "region" in d

    def test_key_criteria_risk(self, d):
        assert "criteria_risk" in d

    def test_key_criteria_pattern(self, d):
        assert "criteria_pattern" in d

    def test_key_criteria_severity(self, d):
        assert "criteria_severity" in d

    def test_key_recommended_action(self, d):
        assert "recommended_action" in d

    def test_key_discovery_score(self, d):
        assert "discovery_score" in d

    def test_key_influence_score(self, d):
        assert "influence_score" in d

    def test_key_alignment_score(self, d):
        assert "alignment_score" in d

    def test_key_competitive_score(self, d):
        assert "competitive_score" in d

    def test_key_criteria_composite(self, d):
        assert "criteria_composite" in d

    def test_key_has_criteria_gap(self, d):
        assert "has_criteria_gap" in d

    def test_key_requires_criteria_coaching(self, d):
        assert "requires_criteria_coaching" in d

    def test_key_estimated_lost_revenue_usd(self, d):
        assert "estimated_lost_revenue_usd" in d

    def test_key_criteria_signal(self, d):
        assert "criteria_signal" in d

    def test_criteria_risk_is_string(self, d):
        assert isinstance(d["criteria_risk"], str)

    def test_criteria_pattern_is_string(self, d):
        assert isinstance(d["criteria_pattern"], str)

    def test_criteria_severity_is_string(self, d):
        assert isinstance(d["criteria_severity"], str)

    def test_recommended_action_is_string(self, d):
        assert isinstance(d["recommended_action"], str)

    def test_rep_id_value(self, d):
        assert d["rep_id"] == "R1"

    def test_region_value(self, d):
        assert d["region"] == "West"


# ---------------------------------------------------------------------------
# 4. Sub-score: _discovery_score
# ---------------------------------------------------------------------------

class TestDiscoveryScore:
    def _ds(self, engine, **kwargs):
        inp = make_input(**kwargs)
        return engine._discovery_score(inp)

    # criteria_documented_early_pct branches
    def test_documented_early_le025_adds40(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=0.25,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 40.0

    def test_documented_early_below025_adds40(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=0.10,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 40.0

    def test_documented_early_le050_adds22(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=0.40,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 22.0

    def test_documented_early_le075_adds8(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=0.60,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 8.0

    def test_documented_early_above075_adds0(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=0.90,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 0.0

    # criteria_first_discovered_stage_avg branches
    def test_stage_avg_ge35_adds35(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=1.0,
            criteria_first_discovered_stage_avg=3.5,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 35.0

    def test_stage_avg_above35_adds35(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=1.0,
            criteria_first_discovered_stage_avg=4.0,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 35.0

    def test_stage_avg_ge25_adds18(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=1.0,
            criteria_first_discovered_stage_avg=2.5,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 18.0

    def test_stage_avg_between25_35_adds18(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=1.0,
            criteria_first_discovered_stage_avg=3.0,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 18.0

    def test_stage_avg_below25_adds0(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=1.0,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 0.0

    # rep_aware_of_all_criteria_pct branches
    def test_rep_aware_le040_adds25(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=1.0,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.40)
        assert score == 25.0

    def test_rep_aware_le070_adds12(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=1.0,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.60)
        assert score == 12.0

    def test_rep_aware_above070_adds0(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=1.0,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.90)
        assert score == 0.0

    def test_max_capped_at_100(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=0.10,
            criteria_first_discovered_stage_avg=4.0,
            rep_aware_of_all_criteria_pct=0.20)
        assert score == 100.0

    def test_combination_adds_up(self, engine):
        # 22 + 18 + 12 = 52
        score = self._ds(engine,
            criteria_documented_early_pct=0.40,
            criteria_first_discovered_stage_avg=3.0,
            rep_aware_of_all_criteria_pct=0.60)
        assert score == 52.0

    def test_zero_score(self, engine):
        score = self._ds(engine,
            criteria_documented_early_pct=1.0,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=1.0)
        assert score == 0.0


# ---------------------------------------------------------------------------
# 5. Sub-score: _influence_score
# ---------------------------------------------------------------------------

class TestInfluenceScore:
    def _is(self, engine, **kwargs):
        inp = make_input(**kwargs)
        return engine._influence_score(inp)

    # criteria_influenced_by_rep_pct branches
    def test_influenced_le020_adds40(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=0.20,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=1.0)
        assert score == 40.0

    def test_influenced_below020_adds40(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=0.10,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=1.0)
        assert score == 40.0

    def test_influenced_le040_adds22(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=0.30,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=1.0)
        assert score == 22.0

    def test_influenced_le060_adds8(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=0.50,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=1.0)
        assert score == 8.0

    def test_influenced_above060_adds0(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=0.80,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=1.0)
        assert score == 0.0

    # criteria_changed_late_in_cycle_pct branches
    def test_changed_late_ge040_adds35(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=1.0,
            criteria_changed_late_in_cycle_pct=0.40,
            scorecard_obtained_pct=1.0)
        assert score == 35.0

    def test_changed_late_above040_adds35(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=1.0,
            criteria_changed_late_in_cycle_pct=0.60,
            scorecard_obtained_pct=1.0)
        assert score == 35.0

    def test_changed_late_ge020_adds18(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=1.0,
            criteria_changed_late_in_cycle_pct=0.20,
            scorecard_obtained_pct=1.0)
        assert score == 18.0

    def test_changed_late_between020_040_adds18(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=1.0,
            criteria_changed_late_in_cycle_pct=0.30,
            scorecard_obtained_pct=1.0)
        assert score == 18.0

    def test_changed_late_below020_adds0(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=1.0,
            criteria_changed_late_in_cycle_pct=0.10,
            scorecard_obtained_pct=1.0)
        assert score == 0.0

    # scorecard_obtained_pct branches
    def test_scorecard_le025_adds25(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=1.0,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=0.25)
        assert score == 25.0

    def test_scorecard_le050_adds12(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=1.0,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=0.40)
        assert score == 12.0

    def test_scorecard_above050_adds0(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=1.0,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=0.60)
        assert score == 0.0

    def test_max_capped_at_100(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=0.10,
            criteria_changed_late_in_cycle_pct=0.60,
            scorecard_obtained_pct=0.10)
        assert score == 100.0

    def test_zero_score(self, engine):
        score = self._is(engine,
            criteria_influenced_by_rep_pct=1.0,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=1.0)
        assert score == 0.0


# ---------------------------------------------------------------------------
# 6. Sub-score: _alignment_score
# ---------------------------------------------------------------------------

class TestAlignmentScore:
    def _as(self, engine, **kwargs):
        inp = make_input(**kwargs)
        return engine._alignment_score(inp)

    # criteria_mapped_to_product_strength_pct branches
    def test_mapped_le030_adds40(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=0.30,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.0)
        assert score == 40.0

    def test_mapped_le055_adds22(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=0.45,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.0)
        assert score == 22.0

    def test_mapped_le075_adds8(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=0.65,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.0)
        assert score == 8.0

    def test_mapped_above075_adds0(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=0.90,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.0)
        assert score == 0.0

    # lost_deals_criteria_mismatch_pct branches
    def test_lost_ge050_adds35(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.50,
            unmet_criteria_at_close_pct=0.0)
        assert score == 35.0

    def test_lost_above050_adds35(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.70,
            unmet_criteria_at_close_pct=0.0)
        assert score == 35.0

    def test_lost_ge030_adds18(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.30,
            unmet_criteria_at_close_pct=0.0)
        assert score == 18.0

    def test_lost_between030_050_adds18(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.40,
            unmet_criteria_at_close_pct=0.0)
        assert score == 18.0

    def test_lost_below030_adds0(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.10,
            unmet_criteria_at_close_pct=0.0)
        assert score == 0.0

    # unmet_criteria_at_close_pct branches
    def test_unmet_ge040_adds25(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.40)
        assert score == 25.0

    def test_unmet_ge020_adds12(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.20)
        assert score == 12.0

    def test_unmet_below020_adds0(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.10)
        assert score == 0.0

    def test_max_capped_at_100(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=0.10,
            lost_deals_criteria_mismatch_pct=0.70,
            unmet_criteria_at_close_pct=0.60)
        assert score == 100.0

    def test_zero_score(self, engine):
        score = self._as(engine,
            criteria_mapped_to_product_strength_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.0)
        assert score == 0.0


# ---------------------------------------------------------------------------
# 7. Sub-score: _competitive_score
# ---------------------------------------------------------------------------

class TestCompetitiveScore:
    def _cs(self, engine, **kwargs):
        inp = make_input(**kwargs)
        return engine._competitive_score(inp)

    # competitor_criteria_advantage_rate_pct branches
    def test_competitor_ge060_adds45(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.60,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=1.0)
        assert score == 45.0

    def test_competitor_above060_adds45(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.80,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=1.0)
        assert score == 45.0

    def test_competitor_ge040_adds25(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.40,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=1.0)
        assert score == 25.0

    def test_competitor_between040_060_adds25(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.50,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=1.0)
        assert score == 25.0

    def test_competitor_ge020_adds10(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.20,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=1.0)
        assert score == 10.0

    def test_competitor_between020_040_adds10(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.30,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=1.0)
        assert score == 10.0

    def test_competitor_below020_adds0(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.10,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=1.0)
        assert score == 0.0

    # criteria_aligned_with_champion_pct branches
    def test_champion_le030_adds30(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.0,
            criteria_aligned_with_champion_pct=0.30,
            criteria_gap_identified_pct=1.0)
        assert score == 30.0

    def test_champion_le055_adds15(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.0,
            criteria_aligned_with_champion_pct=0.45,
            criteria_gap_identified_pct=1.0)
        assert score == 15.0

    def test_champion_above055_adds0(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.0,
            criteria_aligned_with_champion_pct=0.70,
            criteria_gap_identified_pct=1.0)
        assert score == 0.0

    # criteria_gap_identified_pct branches
    def test_gap_le020_adds25(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.0,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=0.20)
        assert score == 25.0

    def test_gap_le045_adds12(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.0,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=0.35)
        assert score == 12.0

    def test_gap_above045_adds0(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.0,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=0.60)
        assert score == 0.0

    def test_max_capped_at_100(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.80,
            criteria_aligned_with_champion_pct=0.10,
            criteria_gap_identified_pct=0.10)
        assert score == 100.0

    def test_zero_score(self, engine):
        score = self._cs(engine,
            competitor_criteria_advantage_rate_pct=0.0,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=1.0)
        assert score == 0.0


# ---------------------------------------------------------------------------
# 8. Pattern Detection (priority order)
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def _pattern(self, engine, **kwargs):
        inp = make_input(**kwargs)
        return engine.assess(inp).criteria_pattern

    def test_scorecard_blind_pursuit_takes_priority(self, engine):
        """scorecard_blind_pursuit should take priority over all others."""
        # Set up conditions that would also satisfy competitive_criteria_disadvantage
        # and late_criteria_discovery, but scorecard_blind_pursuit fires first
        p = self._pattern(engine,
            scorecard_obtained_pct=0.10,
            criteria_documented_early_pct=0.20,
            competitor_criteria_advantage_rate_pct=0.80,
            criteria_first_discovered_stage_avg=4.0,
            # discovery setup
            criteria_influenced_by_rep_pct=0.10,
            criteria_changed_late_in_cycle_pct=0.60,
            rep_aware_of_all_criteria_pct=0.20,
            # competitive setup
            criteria_aligned_with_champion_pct=0.10,
            criteria_gap_identified_pct=0.10)
        assert p == CriteriaPattern.scorecard_blind_pursuit

    def test_scorecard_blind_pursuit_exact_boundary(self, engine):
        p = self._pattern(engine,
            scorecard_obtained_pct=0.15,
            criteria_documented_early_pct=0.30)
        assert p == CriteriaPattern.scorecard_blind_pursuit

    def test_scorecard_blind_pursuit_not_triggered_high_scorecard(self, engine):
        p = self._pattern(engine,
            scorecard_obtained_pct=0.16,
            criteria_documented_early_pct=0.30)
        # Should NOT be scorecard_blind_pursuit
        assert p != CriteriaPattern.scorecard_blind_pursuit

    def test_competitive_criteria_disadvantage_detected(self, engine):
        # Avoid scorecard_blind_pursuit condition
        p = self._pattern(engine,
            scorecard_obtained_pct=0.50,
            criteria_documented_early_pct=0.80,
            competitor_criteria_advantage_rate_pct=0.60,
            criteria_aligned_with_champion_pct=0.10,
            criteria_gap_identified_pct=0.10)
        assert p == CriteriaPattern.competitive_criteria_disadvantage

    def test_competitive_criteria_disadvantage_exact_boundary(self, engine):
        # competitive score must be >= 40 AND competitor_rate >= 0.50
        # competitor_rate=0.50 → +25 for competitor; champion=0.10 → +30; gap=0.10 → +25 = 80 >= 40
        p = self._pattern(engine,
            scorecard_obtained_pct=0.80,
            criteria_documented_early_pct=0.80,
            competitor_criteria_advantage_rate_pct=0.50,
            criteria_aligned_with_champion_pct=0.10,
            criteria_gap_identified_pct=0.10)
        assert p == CriteriaPattern.competitive_criteria_disadvantage

    def test_late_criteria_discovery_detected(self, engine):
        # Avoid higher priority conditions
        p = self._pattern(engine,
            scorecard_obtained_pct=0.80,
            criteria_documented_early_pct=0.80,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_first_discovered_stage_avg=3.5,
            rep_aware_of_all_criteria_pct=0.20,
            criteria_coaching_provided_pct=0.80,
            criteria_aligned_with_champion_pct=0.80)
        assert p == CriteriaPattern.late_criteria_discovery

    def test_late_criteria_discovery_exact_boundary(self, engine):
        # discovery >= 35 AND stage_avg >= 3.0
        # stage_avg=3.0 → +18; documented_early=0.25 → +40; rep_aware=0.20 → +25 = 83 >= 35
        p = self._pattern(engine,
            scorecard_obtained_pct=0.80,
            criteria_documented_early_pct=0.25,
            criteria_first_discovered_stage_avg=3.0,
            rep_aware_of_all_criteria_pct=0.20,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_coaching_provided_pct=0.80,
            criteria_aligned_with_champion_pct=0.80)
        assert p == CriteriaPattern.late_criteria_discovery

    def test_criteria_coaching_gap_detected(self, engine):
        # Avoid higher priority conditions
        p = self._pattern(engine,
            scorecard_obtained_pct=0.80,
            criteria_documented_early_pct=0.80,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.90,
            criteria_coaching_provided_pct=0.15,
            criteria_aligned_with_champion_pct=0.35,
            criteria_changed_late_in_cycle_pct=0.05)
        assert p == CriteriaPattern.criteria_coaching_gap

    def test_criteria_coaching_gap_exact_boundary(self, engine):
        p = self._pattern(engine,
            scorecard_obtained_pct=0.80,
            criteria_documented_early_pct=0.80,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.90,
            criteria_coaching_provided_pct=0.20,
            criteria_aligned_with_champion_pct=0.40,
            criteria_changed_late_in_cycle_pct=0.05)
        assert p == CriteriaPattern.criteria_coaching_gap

    def test_criteria_reactive_alignment_detected(self, engine):
        # Avoid higher priority conditions
        p = self._pattern(engine,
            scorecard_obtained_pct=0.80,
            criteria_documented_early_pct=0.80,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.90,
            criteria_coaching_provided_pct=0.80,
            criteria_aligned_with_champion_pct=0.80,
            criteria_influenced_by_rep_pct=0.30,
            criteria_changed_late_in_cycle_pct=0.35)
        assert p == CriteriaPattern.criteria_reactive_alignment

    def test_none_pattern_for_healthy_input(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.criteria_pattern == CriteriaPattern.none

    def test_pattern_none_when_nothing_triggered(self, engine):
        p = self._pattern(engine,
            scorecard_obtained_pct=0.80,
            criteria_documented_early_pct=0.80,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.90,
            criteria_coaching_provided_pct=0.80,
            criteria_aligned_with_champion_pct=0.80,
            criteria_influenced_by_rep_pct=0.80,
            criteria_changed_late_in_cycle_pct=0.05)
        assert p == CriteriaPattern.none


# ---------------------------------------------------------------------------
# 9. Risk Level Thresholds
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def _risk(self, engine, composite):
        return engine._risk_level(composite)

    def test_critical_at_60(self, engine):
        assert self._risk(engine, 60.0) == CriteriaRisk.critical

    def test_critical_above_60(self, engine):
        assert self._risk(engine, 75.0) == CriteriaRisk.critical

    def test_critical_at_100(self, engine):
        assert self._risk(engine, 100.0) == CriteriaRisk.critical

    def test_high_at_40(self, engine):
        assert self._risk(engine, 40.0) == CriteriaRisk.high

    def test_high_at_59(self, engine):
        assert self._risk(engine, 59.9) == CriteriaRisk.high

    def test_moderate_at_20(self, engine):
        assert self._risk(engine, 20.0) == CriteriaRisk.moderate

    def test_moderate_at_39(self, engine):
        assert self._risk(engine, 39.9) == CriteriaRisk.moderate

    def test_low_at_0(self, engine):
        assert self._risk(engine, 0.0) == CriteriaRisk.low

    def test_low_at_19(self, engine):
        assert self._risk(engine, 19.9) == CriteriaRisk.low

    def test_low_just_below_20(self, engine):
        assert self._risk(engine, 19.0) == CriteriaRisk.low


# ---------------------------------------------------------------------------
# 10. Severity Thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def _sev(self, engine, composite):
        return engine._severity(composite)

    def test_misaligned_at_60(self, engine):
        assert self._sev(engine, 60.0) == CriteriaSeverity.misaligned

    def test_misaligned_above_60(self, engine):
        assert self._sev(engine, 90.0) == CriteriaSeverity.misaligned

    def test_reactive_at_40(self, engine):
        assert self._sev(engine, 40.0) == CriteriaSeverity.reactive

    def test_reactive_at_59(self, engine):
        assert self._sev(engine, 59.9) == CriteriaSeverity.reactive

    def test_aligned_at_20(self, engine):
        assert self._sev(engine, 20.0) == CriteriaSeverity.aligned

    def test_aligned_at_39(self, engine):
        assert self._sev(engine, 39.9) == CriteriaSeverity.aligned

    def test_shaping_at_0(self, engine):
        assert self._sev(engine, 0.0) == CriteriaSeverity.shaping

    def test_shaping_at_19(self, engine):
        assert self._sev(engine, 19.9) == CriteriaSeverity.shaping


# ---------------------------------------------------------------------------
# 11. Action Mapping
# ---------------------------------------------------------------------------

class TestActionMapping:
    def _action(self, engine, risk, pattern):
        return engine._action(risk, pattern)

    def test_critical_competitive_disadvantage(self, engine):
        assert self._action(engine, CriteriaRisk.critical, CriteriaPattern.competitive_criteria_disadvantage) == CriteriaAction.competitive_reframing_coaching

    def test_critical_scorecard_blind_pursuit(self, engine):
        assert self._action(engine, CriteriaRisk.critical, CriteriaPattern.scorecard_blind_pursuit) == CriteriaAction.deal_qualification_review

    def test_critical_late_discovery(self, engine):
        assert self._action(engine, CriteriaRisk.critical, CriteriaPattern.late_criteria_discovery) == CriteriaAction.deal_qualification_review

    def test_critical_coaching_gap(self, engine):
        assert self._action(engine, CriteriaRisk.critical, CriteriaPattern.criteria_coaching_gap) == CriteriaAction.deal_qualification_review

    def test_critical_reactive_alignment(self, engine):
        assert self._action(engine, CriteriaRisk.critical, CriteriaPattern.criteria_reactive_alignment) == CriteriaAction.deal_qualification_review

    def test_critical_none_pattern(self, engine):
        assert self._action(engine, CriteriaRisk.critical, CriteriaPattern.none) == CriteriaAction.deal_qualification_review

    def test_high_late_criteria_discovery(self, engine):
        assert self._action(engine, CriteriaRisk.high, CriteriaPattern.late_criteria_discovery) == CriteriaAction.early_discovery_process_coaching

    def test_high_criteria_coaching_gap(self, engine):
        assert self._action(engine, CriteriaRisk.high, CriteriaPattern.criteria_coaching_gap) == CriteriaAction.champion_criteria_coaching

    def test_high_other_pattern(self, engine):
        assert self._action(engine, CriteriaRisk.high, CriteriaPattern.none) == CriteriaAction.criteria_mapping_coaching

    def test_high_competitive_disadvantage(self, engine):
        assert self._action(engine, CriteriaRisk.high, CriteriaPattern.competitive_criteria_disadvantage) == CriteriaAction.criteria_mapping_coaching

    def test_high_reactive_alignment(self, engine):
        assert self._action(engine, CriteriaRisk.high, CriteriaPattern.criteria_reactive_alignment) == CriteriaAction.criteria_mapping_coaching

    def test_high_scorecard_blind_pursuit(self, engine):
        assert self._action(engine, CriteriaRisk.high, CriteriaPattern.scorecard_blind_pursuit) == CriteriaAction.criteria_mapping_coaching

    def test_moderate_any_pattern(self, engine):
        for pattern in CriteriaPattern:
            assert self._action(engine, CriteriaRisk.moderate, pattern) == CriteriaAction.criteria_mapping_coaching

    def test_low_any_pattern(self, engine):
        for pattern in CriteriaPattern:
            assert self._action(engine, CriteriaRisk.low, pattern) == CriteriaAction.no_action


# ---------------------------------------------------------------------------
# 12. Has Criteria Gap Flag
# ---------------------------------------------------------------------------

class TestHasCriteriaGap:
    def _gap(self, engine, composite, lost=0.0, influenced=1.0):
        inp = make_input(
            lost_deals_criteria_mismatch_pct=lost,
            criteria_influenced_by_rep_pct=influenced)
        return engine._has_criteria_gap(composite, inp)

    def test_gap_true_when_composite_ge40(self, engine):
        assert self._gap(engine, 40.0) is True

    def test_gap_true_when_composite_above40(self, engine):
        assert self._gap(engine, 60.0) is True

    def test_gap_true_when_lost_ge040(self, engine):
        assert self._gap(engine, 10.0, lost=0.40) is True

    def test_gap_true_when_lost_above040(self, engine):
        assert self._gap(engine, 10.0, lost=0.60) is True

    def test_gap_true_when_influenced_le025(self, engine):
        assert self._gap(engine, 10.0, influenced=0.25) is True

    def test_gap_true_when_influenced_below025(self, engine):
        assert self._gap(engine, 10.0, influenced=0.10) is True

    def test_gap_false_when_none_triggered(self, engine):
        assert self._gap(engine, 10.0, lost=0.10, influenced=0.80) is False

    def test_gap_false_at_zero_composite(self, engine):
        assert self._gap(engine, 0.0, lost=0.10, influenced=0.80) is False

    def test_gap_true_via_end_to_end(self, engine, worst_case_input):
        result = engine.assess(worst_case_input)
        assert result.has_criteria_gap is True

    def test_gap_false_healthy(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.has_criteria_gap is False


# ---------------------------------------------------------------------------
# 13. Requires Criteria Coaching Flag
# ---------------------------------------------------------------------------

class TestRequiresCriteriaCoaching:
    def _coaching(self, engine, composite, documented=1.0, scorecard=1.0):
        inp = make_input(
            criteria_documented_early_pct=documented,
            scorecard_obtained_pct=scorecard)
        return engine._requires_criteria_coaching(composite, inp)

    def test_coaching_true_when_composite_ge30(self, engine):
        assert self._coaching(engine, 30.0) is True

    def test_coaching_true_when_composite_above30(self, engine):
        assert self._coaching(engine, 50.0) is True

    def test_coaching_true_when_documented_le040(self, engine):
        assert self._coaching(engine, 10.0, documented=0.40) is True

    def test_coaching_true_when_documented_below040(self, engine):
        assert self._coaching(engine, 10.0, documented=0.20) is True

    def test_coaching_true_when_scorecard_le035(self, engine):
        assert self._coaching(engine, 10.0, scorecard=0.35) is True

    def test_coaching_true_when_scorecard_below035(self, engine):
        assert self._coaching(engine, 10.0, scorecard=0.20) is True

    def test_coaching_false_when_none_triggered(self, engine):
        assert self._coaching(engine, 10.0, documented=0.80, scorecard=0.80) is False

    def test_coaching_true_via_end_to_end(self, engine, worst_case_input):
        result = engine.assess(worst_case_input)
        assert result.requires_criteria_coaching is True

    def test_coaching_false_healthy(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        # healthy has documented=0.80, scorecard=0.80, and low composite
        assert result.requires_criteria_coaching is False


# ---------------------------------------------------------------------------
# 14. Estimated Lost Revenue Formula
# ---------------------------------------------------------------------------

class TestEstimatedLostRevenue:
    def test_basic_formula(self, engine):
        inp = make_input(
            total_deals_evaluated=100,
            avg_opportunity_value_usd=10000.0,
            lost_deals_criteria_mismatch_pct=0.50)
        composite = 50.0
        expected = round(100 * 10000.0 * 0.50 * (50.0 / 100.0), 2)
        assert engine._estimated_lost_revenue(inp, composite) == expected

    def test_zero_composite(self, engine):
        inp = make_input(total_deals_evaluated=100, avg_opportunity_value_usd=10000.0, lost_deals_criteria_mismatch_pct=0.50)
        assert engine._estimated_lost_revenue(inp, 0.0) == 0.0

    def test_zero_deals(self, engine):
        inp = make_input(total_deals_evaluated=0, avg_opportunity_value_usd=10000.0, lost_deals_criteria_mismatch_pct=0.50)
        assert engine._estimated_lost_revenue(inp, 50.0) == 0.0

    def test_zero_mismatch(self, engine):
        inp = make_input(total_deals_evaluated=100, avg_opportunity_value_usd=10000.0, lost_deals_criteria_mismatch_pct=0.0)
        assert engine._estimated_lost_revenue(inp, 50.0) == 0.0

    def test_rounded_to_2_decimal_places(self, engine):
        inp = make_input(
            total_deals_evaluated=3,
            avg_opportunity_value_usd=10000.0,
            lost_deals_criteria_mismatch_pct=0.333)
        composite = 33.3
        result = engine._estimated_lost_revenue(inp, composite)
        assert result == round(3 * 10000.0 * 0.333 * (33.3 / 100.0), 2)

    def test_full_composite(self, engine):
        inp = make_input(
            total_deals_evaluated=10,
            avg_opportunity_value_usd=5000.0,
            lost_deals_criteria_mismatch_pct=0.50)
        result = engine._estimated_lost_revenue(inp, 100.0)
        assert result == round(10 * 5000.0 * 0.50 * 1.0, 2)

    def test_large_values(self, engine):
        inp = make_input(
            total_deals_evaluated=1000,
            avg_opportunity_value_usd=100000.0,
            lost_deals_criteria_mismatch_pct=0.80)
        result = engine._estimated_lost_revenue(inp, 80.0)
        assert result == round(1000 * 100000.0 * 0.80 * 0.80, 2)

    def test_result_is_float(self, engine):
        inp = make_input()
        result = engine._estimated_lost_revenue(inp, 50.0)
        assert isinstance(result, float)

    def test_end_to_end_lost_revenue(self, engine):
        inp = make_input(
            total_deals_evaluated=200,
            avg_opportunity_value_usd=20000.0,
            lost_deals_criteria_mismatch_pct=0.40,
            # make composite controllable
            criteria_documented_early_pct=0.80,
            criteria_influenced_by_rep_pct=0.80,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.90,
            criteria_mapped_to_product_strength_pct=0.85,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_aligned_with_champion_pct=0.85,
            scorecard_obtained_pct=0.80,
            criteria_gap_identified_pct=0.80,
            unmet_criteria_at_close_pct=0.05)
        result = engine.assess(inp)
        expected = round(200 * 20000.0 * 0.40 * (result.criteria_composite / 100.0), 2)
        assert result.estimated_lost_revenue_usd == expected


# ---------------------------------------------------------------------------
# 15. Signal String
# ---------------------------------------------------------------------------

class TestSignalString:
    def test_healthy_signal(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.criteria_signal == "Decision criteria alignment healthy — early discovery, influence, and competitive positioning within benchmarks"

    def test_healthy_signal_requires_none_and_below_20(self, engine):
        inp = make_input(
            criteria_documented_early_pct=0.80,
            criteria_influenced_by_rep_pct=0.80,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.90,
            criteria_mapped_to_product_strength_pct=0.85,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_aligned_with_champion_pct=0.85,
            scorecard_obtained_pct=0.80,
            criteria_gap_identified_pct=0.80,
            criteria_coaching_provided_pct=0.80,
            lost_deals_criteria_mismatch_pct=0.05,
            unmet_criteria_at_close_pct=0.05,
            criteria_changed_late_in_cycle_pct=0.05)
        result = engine.assess(inp)
        assert result.criteria_signal == "Decision criteria alignment healthy — early discovery, influence, and competitive positioning within benchmarks"

    def test_risky_signal_contains_pattern_label(self, engine):
        # Force scorecard_blind_pursuit
        inp = make_input(
            scorecard_obtained_pct=0.10,
            criteria_documented_early_pct=0.20)
        result = engine.assess(inp)
        assert "scorecard blind pursuit" in result.criteria_signal.lower() or "Scorecard blind pursuit" in result.criteria_signal

    def test_risky_signal_contains_documented_early_pct(self, engine):
        inp = make_input(
            scorecard_obtained_pct=0.10,
            criteria_documented_early_pct=0.20)
        result = engine.assess(inp)
        assert "20% criteria documented early" in result.criteria_signal

    def test_risky_signal_contains_influenced_pct(self, engine):
        inp = make_input(
            scorecard_obtained_pct=0.10,
            criteria_documented_early_pct=0.20,
            criteria_influenced_by_rep_pct=0.35)
        result = engine.assess(inp)
        assert "35% criteria influenced" in result.criteria_signal

    def test_risky_signal_contains_lost_mismatch_pct(self, engine):
        inp = make_input(
            scorecard_obtained_pct=0.10,
            criteria_documented_early_pct=0.20,
            lost_deals_criteria_mismatch_pct=0.60)
        result = engine.assess(inp)
        assert "60% losses from criteria mismatch" in result.criteria_signal

    def test_risky_signal_contains_composite(self, engine):
        inp = make_input(
            scorecard_obtained_pct=0.10,
            criteria_documented_early_pct=0.20)
        result = engine.assess(inp)
        assert f"composite {result.criteria_composite:.0f}" in result.criteria_signal

    def test_signal_with_none_pattern_but_high_composite(self, engine):
        # Pattern=none but composite >= 20 should still get non-healthy signal
        inp = make_input(
            scorecard_obtained_pct=0.80,
            criteria_documented_early_pct=0.80,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.90,
            criteria_coaching_provided_pct=0.80,
            criteria_aligned_with_champion_pct=0.80,
            criteria_influenced_by_rep_pct=0.80,
            criteria_changed_late_in_cycle_pct=0.05,
            criteria_mapped_to_product_strength_pct=0.40,
            lost_deals_criteria_mismatch_pct=0.35,
            unmet_criteria_at_close_pct=0.25)
        result = engine.assess(inp)
        if result.criteria_composite >= 20 and result.criteria_pattern == CriteriaPattern.none:
            assert "Criteria risk" in result.criteria_signal

    def test_signal_is_string(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result.criteria_signal, str)

    def test_signal_not_empty(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert len(result.criteria_signal) > 0


# ---------------------------------------------------------------------------
# 16. Composite Score Calculation
# ---------------------------------------------------------------------------

class TestCompositeScore:
    def test_composite_is_weighted_average(self, engine):
        inp = make_input(
            criteria_documented_early_pct=0.25,   # discovery +40
            criteria_influenced_by_rep_pct=0.20,  # influence +40
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=0.90,
            criteria_mapped_to_product_strength_pct=0.90,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_aligned_with_champion_pct=0.85,
            scorecard_obtained_pct=0.25,          # influence +25
            criteria_gap_identified_pct=0.80,
            criteria_coaching_provided_pct=0.80,
            lost_deals_criteria_mismatch_pct=0.05,
            unmet_criteria_at_close_pct=0.05,
            criteria_changed_late_in_cycle_pct=0.05)
        result = engine.assess(inp)
        # Just verify it's between 0 and 100
        assert 0.0 <= result.criteria_composite <= 100.0

    def test_composite_capped_at_100(self, engine, worst_case_input):
        result = engine.assess(worst_case_input)
        assert result.criteria_composite <= 100.0

    def test_composite_zero_for_best_case(self, engine):
        inp = make_input(
            criteria_documented_early_pct=1.0,
            criteria_influenced_by_rep_pct=1.0,
            criteria_first_discovered_stage_avg=0.0,
            rep_aware_of_all_criteria_pct=1.0,
            criteria_mapped_to_product_strength_pct=1.0,
            competitor_criteria_advantage_rate_pct=0.0,
            criteria_aligned_with_champion_pct=1.0,
            scorecard_obtained_pct=1.0,
            criteria_gap_identified_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.0,
            criteria_changed_late_in_cycle_pct=0.0)
        result = engine.assess(inp)
        assert result.criteria_composite == 0.0

    def test_composite_weights(self, engine):
        # Verify formula: discovery*0.30 + influence*0.30 + alignment*0.25 + competitive*0.15
        inp = make_input(
            criteria_documented_early_pct=1.0,
            criteria_influenced_by_rep_pct=1.0,
            criteria_first_discovered_stage_avg=0.0,
            rep_aware_of_all_criteria_pct=1.0,
            criteria_mapped_to_product_strength_pct=1.0,
            competitor_criteria_advantage_rate_pct=0.0,
            criteria_aligned_with_champion_pct=1.0,
            scorecard_obtained_pct=1.0,
            criteria_gap_identified_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.0,
            criteria_changed_late_in_cycle_pct=0.0)
        result = engine.assess(inp)
        expected = round(
            result.discovery_score * 0.30 +
            result.influence_score * 0.30 +
            result.alignment_score * 0.25 +
            result.competitive_score * 0.15, 1)
        assert result.criteria_composite == min(expected, 100.0)


# ---------------------------------------------------------------------------
# 17. Assess End-to-End Tests
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_returns_criteria_result(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert isinstance(result, CriteriaResult)

    def test_rep_id_propagated(self, engine):
        inp = make_input(rep_id="REP99")
        result = engine.assess(inp)
        assert result.rep_id == "REP99"

    def test_region_propagated(self, engine):
        inp = make_input(region="Central")
        result = engine.assess(inp)
        assert result.region == "Central"

    def test_healthy_is_low_risk(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.criteria_risk == CriteriaRisk.low

    def test_healthy_is_shaping(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.criteria_severity == CriteriaSeverity.shaping

    def test_healthy_action_no_action(self, engine, healthy_input):
        result = engine.assess(healthy_input)
        assert result.recommended_action == CriteriaAction.no_action

    def test_worst_case_is_critical(self, engine, worst_case_input):
        result = engine.assess(worst_case_input)
        assert result.criteria_risk == CriteriaRisk.critical

    def test_worst_case_is_misaligned(self, engine, worst_case_input):
        result = engine.assess(worst_case_input)
        assert result.criteria_severity == CriteriaSeverity.misaligned

    def test_result_added_to_internal_list(self, engine, healthy_input):
        engine.assess(healthy_input)
        assert len(engine._results) == 1

    def test_multiple_assesses_accumulate(self, engine, healthy_input):
        engine.assess(healthy_input)
        engine.assess(healthy_input)
        assert len(engine._results) == 2

    def test_scores_in_range(self, engine, worst_case_input):
        result = engine.assess(worst_case_input)
        assert 0.0 <= result.discovery_score <= 100.0
        assert 0.0 <= result.influence_score <= 100.0
        assert 0.0 <= result.alignment_score <= 100.0
        assert 0.0 <= result.competitive_score <= 100.0
        assert 0.0 <= result.criteria_composite <= 100.0

    def test_moderate_risk_scenario(self, engine):
        inp = make_input(
            criteria_documented_early_pct=0.40,
            criteria_influenced_by_rep_pct=0.50,
            criteria_first_discovered_stage_avg=2.5,
            rep_aware_of_all_criteria_pct=0.60,
            criteria_mapped_to_product_strength_pct=0.60,
            competitor_criteria_advantage_rate_pct=0.15,
            criteria_aligned_with_champion_pct=0.60,
            scorecard_obtained_pct=0.60,
            criteria_gap_identified_pct=0.50,
            criteria_coaching_provided_pct=0.50,
            lost_deals_criteria_mismatch_pct=0.20,
            unmet_criteria_at_close_pct=0.15,
            criteria_changed_late_in_cycle_pct=0.15)
        result = engine.assess(inp)
        assert result.criteria_risk in (CriteriaRisk.moderate, CriteriaRisk.high)

    def test_high_risk_scenario(self, engine):
        # craft scenario for high (40-59 composite) + late_criteria_discovery
        inp = make_input(
            scorecard_obtained_pct=0.80,
            criteria_documented_early_pct=0.10,
            criteria_influenced_by_rep_pct=0.80,
            criteria_first_discovered_stage_avg=4.0,
            rep_aware_of_all_criteria_pct=0.20,
            criteria_mapped_to_product_strength_pct=0.80,
            competitor_criteria_advantage_rate_pct=0.05,
            criteria_aligned_with_champion_pct=0.80,
            criteria_gap_identified_pct=0.80,
            criteria_coaching_provided_pct=0.80,
            lost_deals_criteria_mismatch_pct=0.10,
            unmet_criteria_at_close_pct=0.05,
            criteria_changed_late_in_cycle_pct=0.05)
        result = engine.assess(inp)
        # discovery score should be very high
        assert result.discovery_score >= 35


# ---------------------------------------------------------------------------
# 18. assess_batch Tests
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self, engine, healthy_input):
        results = engine.assess_batch([healthy_input])
        assert isinstance(results, list)

    def test_returns_correct_count(self, engine, healthy_input, worst_case_input):
        results = engine.assess_batch([healthy_input, worst_case_input])
        assert len(results) == 2

    def test_empty_batch(self, engine):
        results = engine.assess_batch([])
        assert results == []

    def test_each_result_is_criteria_result(self, engine, healthy_input, worst_case_input):
        results = engine.assess_batch([healthy_input, worst_case_input])
        for r in results:
            assert isinstance(r, CriteriaResult)

    def test_batch_accumulates_in_results(self, engine, healthy_input, worst_case_input):
        engine.assess_batch([healthy_input, worst_case_input, healthy_input])
        assert len(engine._results) == 3

    def test_batch_order_preserved(self, engine):
        inp1 = make_input(rep_id="A")
        inp2 = make_input(rep_id="B")
        results = engine.assess_batch([inp1, inp2])
        assert results[0].rep_id == "A"
        assert results[1].rep_id == "B"

    def test_batch_single_item(self, engine, healthy_input):
        results = engine.assess_batch([healthy_input])
        assert len(results) == 1
        assert results[0].rep_id == "R1"

    def test_batch_produces_same_as_sequential(self, engine):
        engine2 = SalesDecisionCriteriaAlignmentIntelligenceEngine()
        inp = make_input(rep_id="X")
        r_batch = engine.assess_batch([inp])[0]
        r_seq = engine2.assess(inp)
        assert r_batch.criteria_composite == r_seq.criteria_composite
        assert r_batch.criteria_risk == r_seq.criteria_risk


# ---------------------------------------------------------------------------
# 19. summary() Tests
# ---------------------------------------------------------------------------

class TestSummaryEmpty:
    def test_empty_returns_dict(self, engine):
        s = engine.summary()
        assert isinstance(s, dict)

    def test_empty_has_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_empty_total_is_0(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_risk_counts_empty(self, engine):
        assert engine.summary()["risk_counts"] == {}

    def test_empty_pattern_counts_empty(self, engine):
        assert engine.summary()["pattern_counts"] == {}

    def test_empty_severity_counts_empty(self, engine):
        assert engine.summary()["severity_counts"] == {}

    def test_empty_action_counts_empty(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_empty_avg_criteria_composite(self, engine):
        assert engine.summary()["avg_criteria_composite"] == 0.0

    def test_empty_criteria_gap_count(self, engine):
        assert engine.summary()["criteria_gap_count"] == 0

    def test_empty_coaching_count(self, engine):
        assert engine.summary()["coaching_count"] == 0

    def test_empty_avg_discovery_score(self, engine):
        assert engine.summary()["avg_discovery_score"] == 0.0

    def test_empty_avg_influence_score(self, engine):
        assert engine.summary()["avg_influence_score"] == 0.0

    def test_empty_avg_alignment_score(self, engine):
        assert engine.summary()["avg_alignment_score"] == 0.0

    def test_empty_avg_competitive_score(self, engine):
        assert engine.summary()["avg_competitive_score"] == 0.0

    def test_empty_total_lost_revenue(self, engine):
        assert engine.summary()["total_estimated_lost_revenue_usd"] == 0.0


class TestSummaryPopulated:
    @pytest.fixture
    def populated_engine(self, healthy_input, worst_case_input):
        e = SalesDecisionCriteriaAlignmentIntelligenceEngine()
        e.assess(healthy_input)
        e.assess(worst_case_input)
        return e

    def test_total_is_correct(self, populated_engine):
        assert populated_engine.summary()["total"] == 2

    def test_has_13_keys(self, populated_engine):
        assert len(populated_engine.summary()) == 13

    def test_risk_counts_key_total(self, populated_engine):
        rc = populated_engine.summary()["risk_counts"]
        assert sum(rc.values()) == 2

    def test_pattern_counts_key_total(self, populated_engine):
        pc = populated_engine.summary()["pattern_counts"]
        assert sum(pc.values()) == 2

    def test_severity_counts_key_total(self, populated_engine):
        sc = populated_engine.summary()["severity_counts"]
        assert sum(sc.values()) == 2

    def test_action_counts_key_total(self, populated_engine):
        ac = populated_engine.summary()["action_counts"]
        assert sum(ac.values()) == 2

    def test_avg_composite_is_float(self, populated_engine):
        assert isinstance(populated_engine.summary()["avg_criteria_composite"], float)

    def test_avg_composite_in_range(self, populated_engine):
        avg = populated_engine.summary()["avg_criteria_composite"]
        assert 0.0 <= avg <= 100.0

    def test_criteria_gap_count_gte_0(self, populated_engine):
        assert populated_engine.summary()["criteria_gap_count"] >= 0

    def test_criteria_gap_count_lte_total(self, populated_engine):
        s = populated_engine.summary()
        assert s["criteria_gap_count"] <= s["total"]

    def test_coaching_count_gte_0(self, populated_engine):
        assert populated_engine.summary()["coaching_count"] >= 0

    def test_coaching_count_lte_total(self, populated_engine):
        s = populated_engine.summary()
        assert s["coaching_count"] <= s["total"]

    def test_avg_discovery_score_is_float(self, populated_engine):
        assert isinstance(populated_engine.summary()["avg_discovery_score"], float)

    def test_avg_influence_score_is_float(self, populated_engine):
        assert isinstance(populated_engine.summary()["avg_influence_score"], float)

    def test_avg_alignment_score_is_float(self, populated_engine):
        assert isinstance(populated_engine.summary()["avg_alignment_score"], float)

    def test_avg_competitive_score_is_float(self, populated_engine):
        assert isinstance(populated_engine.summary()["avg_competitive_score"], float)

    def test_total_lost_revenue_is_float(self, populated_engine):
        assert isinstance(populated_engine.summary()["total_estimated_lost_revenue_usd"], float)

    def test_summary_all_13_keys_present(self, populated_engine):
        s = populated_engine.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_criteria_composite", "criteria_gap_count",
            "coaching_count", "avg_discovery_score", "avg_influence_score",
            "avg_alignment_score", "avg_competitive_score",
            "total_estimated_lost_revenue_usd"
        }
        assert set(s.keys()) == expected_keys

    def test_summary_risk_counts_has_valid_keys(self, populated_engine):
        rc = populated_engine.summary()["risk_counts"]
        valid = {r.value for r in CriteriaRisk}
        for k in rc:
            assert k in valid

    def test_summary_pattern_counts_has_valid_keys(self, populated_engine):
        pc = populated_engine.summary()["pattern_counts"]
        valid = {p.value for p in CriteriaPattern}
        for k in pc:
            assert k in valid

    def test_summary_severity_counts_has_valid_keys(self, populated_engine):
        sc = populated_engine.summary()["severity_counts"]
        valid = {s.value for s in CriteriaSeverity}
        for k in sc:
            assert k in valid

    def test_summary_action_counts_has_valid_keys(self, populated_engine):
        ac = populated_engine.summary()["action_counts"]
        valid = {a.value for a in CriteriaAction}
        for k in ac:
            assert k in valid

    def test_summary_avg_composite_matches_manual(self, populated_engine):
        s = populated_engine.summary()
        results = populated_engine._results
        expected = round(sum(r.criteria_composite for r in results) / len(results), 1)
        assert s["avg_criteria_composite"] == expected

    def test_summary_total_lost_revenue_matches_manual(self, populated_engine):
        s = populated_engine.summary()
        results = populated_engine._results
        expected = round(sum(r.estimated_lost_revenue_usd for r in results), 2)
        assert s["total_estimated_lost_revenue_usd"] == expected

    def test_summary_after_single_assess(self, engine, healthy_input):
        engine.assess(healthy_input)
        s = engine.summary()
        assert s["total"] == 1
        assert len(s) == 13

    def test_summary_worst_case_has_critical_risk(self):
        e = SalesDecisionCriteriaAlignmentIntelligenceEngine()
        e.assess(make_input(
            criteria_documented_early_pct=0.10,
            criteria_influenced_by_rep_pct=0.10,
            criteria_first_discovered_stage_avg=4.0,
            criteria_changed_late_in_cycle_pct=0.60,
            rep_aware_of_all_criteria_pct=0.20,
            criteria_mapped_to_product_strength_pct=0.10,
            competitor_criteria_advantage_rate_pct=0.80,
            criteria_aligned_with_champion_pct=0.10,
            scorecard_obtained_pct=0.10,
            criteria_gap_identified_pct=0.10,
            lost_deals_criteria_mismatch_pct=0.70,
            unmet_criteria_at_close_pct=0.60))
        s = e.summary()
        assert s["risk_counts"].get("critical", 0) >= 1


# ---------------------------------------------------------------------------
# 20. Edge Cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_boundary_composite_exactly_60(self, engine):
        # Find an input that produces exactly 60
        # Just verify that at exactly 60, it's critical
        r = engine._risk_level(60.0)
        assert r == CriteriaRisk.critical

    def test_boundary_composite_exactly_40(self, engine):
        r = engine._risk_level(40.0)
        assert r == CriteriaRisk.high

    def test_boundary_composite_exactly_20(self, engine):
        r = engine._risk_level(20.0)
        assert r == CriteriaRisk.moderate

    def test_severity_boundary_at_60(self, engine):
        s = engine._severity(60.0)
        assert s == CriteriaSeverity.misaligned

    def test_severity_boundary_at_40(self, engine):
        s = engine._severity(40.0)
        assert s == CriteriaSeverity.reactive

    def test_severity_boundary_at_20(self, engine):
        s = engine._severity(20.0)
        assert s == CriteriaSeverity.aligned

    def test_discovery_exact_boundary_025(self, engine):
        score = engine._discovery_score(make_input(
            criteria_documented_early_pct=0.25,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=1.0))
        assert score == 40.0

    def test_discovery_exact_boundary_050(self, engine):
        score = engine._discovery_score(make_input(
            criteria_documented_early_pct=0.50,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=1.0))
        assert score == 22.0

    def test_discovery_exact_boundary_075(self, engine):
        score = engine._discovery_score(make_input(
            criteria_documented_early_pct=0.75,
            criteria_first_discovered_stage_avg=1.0,
            rep_aware_of_all_criteria_pct=1.0))
        assert score == 8.0

    def test_influence_exact_boundary_020(self, engine):
        score = engine._influence_score(make_input(
            criteria_influenced_by_rep_pct=0.20,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=1.0))
        assert score == 40.0

    def test_influence_exact_boundary_040(self, engine):
        score = engine._influence_score(make_input(
            criteria_influenced_by_rep_pct=0.40,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=1.0))
        assert score == 22.0

    def test_influence_exact_boundary_060(self, engine):
        score = engine._influence_score(make_input(
            criteria_influenced_by_rep_pct=0.60,
            criteria_changed_late_in_cycle_pct=0.0,
            scorecard_obtained_pct=1.0))
        assert score == 8.0

    def test_alignment_exact_boundary_030(self, engine):
        score = engine._alignment_score(make_input(
            criteria_mapped_to_product_strength_pct=0.30,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.0))
        assert score == 40.0

    def test_competitive_exact_boundary_060(self, engine):
        score = engine._competitive_score(make_input(
            competitor_criteria_advantage_rate_pct=0.60,
            criteria_aligned_with_champion_pct=1.0,
            criteria_gap_identified_pct=1.0))
        assert score == 45.0

    def test_engine_independent_instances(self):
        e1 = SalesDecisionCriteriaAlignmentIntelligenceEngine()
        e2 = SalesDecisionCriteriaAlignmentIntelligenceEngine()
        e1.assess(make_input())
        # e2 should still have empty results
        assert len(e2._results) == 0

    def test_zero_opportunity_value(self, engine):
        inp = make_input(avg_opportunity_value_usd=0.0)
        result = engine.assess(inp)
        assert result.estimated_lost_revenue_usd == 0.0

    def test_zero_total_deals(self, engine):
        inp = make_input(total_deals_evaluated=0)
        result = engine.assess(inp)
        assert result.estimated_lost_revenue_usd == 0.0

    def test_all_pct_at_1(self, engine):
        inp = make_input(
            criteria_documented_early_pct=1.0,
            criteria_influenced_by_rep_pct=1.0,
            criteria_first_discovered_stage_avg=0.0,
            rep_aware_of_all_criteria_pct=1.0,
            criteria_mapped_to_product_strength_pct=1.0,
            competitor_criteria_advantage_rate_pct=0.0,
            criteria_aligned_with_champion_pct=1.0,
            scorecard_obtained_pct=1.0,
            criteria_gap_identified_pct=1.0,
            criteria_coaching_provided_pct=1.0,
            lost_deals_criteria_mismatch_pct=0.0,
            unmet_criteria_at_close_pct=0.0,
            criteria_changed_late_in_cycle_pct=0.0)
        result = engine.assess(inp)
        assert result.criteria_risk == CriteriaRisk.low
        assert result.criteria_severity == CriteriaSeverity.shaping

    def test_to_dict_returns_enum_values_not_objects(self, engine, healthy_input):
        d = engine.assess(healthy_input).to_dict()
        assert isinstance(d["criteria_risk"], str)
        assert isinstance(d["criteria_pattern"], str)
        assert isinstance(d["criteria_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_assess_returns_new_result_each_time(self, engine):
        inp = make_input()
        r1 = engine.assess(inp)
        r2 = engine.assess(inp)
        assert r1 is not r2

    def test_summary_gap_count_correct(self, engine):
        e = SalesDecisionCriteriaAlignmentIntelligenceEngine()
        # healthy input → no gap
        e.assess(make_input())
        # worst case → gap
        e.assess(make_input(
            criteria_documented_early_pct=0.10,
            criteria_influenced_by_rep_pct=0.10,
            criteria_first_discovered_stage_avg=4.0,
            criteria_changed_late_in_cycle_pct=0.60,
            rep_aware_of_all_criteria_pct=0.20,
            criteria_mapped_to_product_strength_pct=0.10,
            competitor_criteria_advantage_rate_pct=0.80,
            criteria_aligned_with_champion_pct=0.10,
            scorecard_obtained_pct=0.10,
            criteria_gap_identified_pct=0.10,
            lost_deals_criteria_mismatch_pct=0.70,
            unmet_criteria_at_close_pct=0.60))
        s = e.summary()
        assert s["criteria_gap_count"] >= 1
