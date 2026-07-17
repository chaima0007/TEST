"""
Comprehensive pytest test suite for SalesCompetitiveWinLossIntelligenceEngine.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_competitive_win_loss_intelligence_engine import (
    CompetitiveAction,
    CompetitivePattern,
    CompetitiveRisk,
    CompetitiveSeverity,
    CompetitiveWinLossInput,
    CompetitiveWinLossResult,
    SalesCompetitiveWinLossIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(
    rep_id: str = "rep1",
    region: str = "west",
    evaluation_period_id: str = "Q1-2026",
    total_competitive_deals: int = 10,
    competitive_wins: int = 6,
    competitive_losses: int = 3,
    competitive_ties: int = 1,
    deals_lost_on_price_competitive: int = 1,
    deals_lost_on_features_competitive: int = 1,
    deals_lost_on_relationship_competitive: int = 1,
    win_rate_vs_top_competitor_pct: float = 0.50,
    avg_deal_size_won_usd: float = 10000.0,
    avg_deal_size_lost_usd: float = 8000.0,
    competitive_intel_documented_count: int = 7,
    battle_card_used_count: int = 5,
    proof_of_concept_win_rate_pct: float = 0.60,
    multi_stakeholder_competitive_wins: int = 4,
    single_stakeholder_competitive_losses: int = 1,
    competitive_displacement_wins: int = 2,
    deals_displaced_by_competitor: int = 1,
    avg_competitive_cycle_days: float = 30.0,
    executive_involved_competitive_wins: int = 3,
) -> CompetitiveWinLossInput:
    return CompetitiveWinLossInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        total_competitive_deals=total_competitive_deals,
        competitive_wins=competitive_wins,
        competitive_losses=competitive_losses,
        competitive_ties=competitive_ties,
        deals_lost_on_price_competitive=deals_lost_on_price_competitive,
        deals_lost_on_features_competitive=deals_lost_on_features_competitive,
        deals_lost_on_relationship_competitive=deals_lost_on_relationship_competitive,
        win_rate_vs_top_competitor_pct=win_rate_vs_top_competitor_pct,
        avg_deal_size_won_usd=avg_deal_size_won_usd,
        avg_deal_size_lost_usd=avg_deal_size_lost_usd,
        competitive_intel_documented_count=competitive_intel_documented_count,
        battle_card_used_count=battle_card_used_count,
        proof_of_concept_win_rate_pct=proof_of_concept_win_rate_pct,
        multi_stakeholder_competitive_wins=multi_stakeholder_competitive_wins,
        single_stakeholder_competitive_losses=single_stakeholder_competitive_losses,
        competitive_displacement_wins=competitive_displacement_wins,
        deals_displaced_by_competitor=deals_displaced_by_competitor,
        avg_competitive_cycle_days=avg_competitive_cycle_days,
        executive_involved_competitive_wins=executive_involved_competitive_wins,
    )


@pytest.fixture
def engine():
    return SalesCompetitiveWinLossIntelligenceEngine()


@pytest.fixture
def good_input():
    """A healthy rep — low risk scores across the board."""
    return make_input(
        total_competitive_deals=10,
        competitive_wins=8,
        competitive_losses=1,
        competitive_ties=1,
        deals_lost_on_price_competitive=0,
        deals_lost_on_features_competitive=0,
        deals_lost_on_relationship_competitive=1,
        win_rate_vs_top_competitor_pct=0.60,
        competitive_intel_documented_count=9,
        battle_card_used_count=9,
        proof_of_concept_win_rate_pct=0.80,
        multi_stakeholder_competitive_wins=7,
        single_stakeholder_competitive_losses=0,
        competitive_displacement_wins=3,
        deals_displaced_by_competitor=1,
    )


@pytest.fixture
def bad_input():
    """A struggling rep — high risk scores everywhere."""
    return make_input(
        total_competitive_deals=10,
        competitive_wins=1,
        competitive_losses=8,
        competitive_ties=1,
        deals_lost_on_price_competitive=5,
        deals_lost_on_features_competitive=4,
        deals_lost_on_relationship_competitive=2,
        win_rate_vs_top_competitor_pct=0.10,
        competitive_intel_documented_count=1,
        battle_card_used_count=1,
        proof_of_concept_win_rate_pct=0.10,
        multi_stakeholder_competitive_wins=0,
        single_stakeholder_competitive_losses=6,
        competitive_displacement_wins=0,
        deals_displaced_by_competitor=5,
        avg_deal_size_lost_usd=20000.0,
    )


# ===========================================================================
# 1. ENUM VALUES
# ===========================================================================

class TestCompetitiveRisk:
    def test_low(self):
        assert CompetitiveRisk.low == "low"
        assert CompetitiveRisk.low.value == "low"

    def test_moderate(self):
        assert CompetitiveRisk.moderate == "moderate"
        assert CompetitiveRisk.moderate.value == "moderate"

    def test_high(self):
        assert CompetitiveRisk.high == "high"
        assert CompetitiveRisk.high.value == "high"

    def test_critical(self):
        assert CompetitiveRisk.critical == "critical"
        assert CompetitiveRisk.critical.value == "critical"

    def test_all_members(self):
        assert set(r.value for r in CompetitiveRisk) == {"low", "moderate", "high", "critical"}

    def test_is_str_enum(self):
        assert isinstance(CompetitiveRisk.low, str)


class TestCompetitivePattern:
    def test_none(self):
        assert CompetitivePattern.none == "none"
        assert CompetitivePattern.none.value == "none"

    def test_high_loss_rate(self):
        assert CompetitivePattern.high_loss_rate == "high_loss_rate"

    def test_no_competitive_intel(self):
        assert CompetitivePattern.no_competitive_intel == "no_competitive_intel"

    def test_price_driven_loss(self):
        assert CompetitivePattern.price_driven_loss == "price_driven_loss"

    def test_feature_gap_loss(self):
        assert CompetitivePattern.feature_gap_loss == "feature_gap_loss"

    def test_icp_mismatch(self):
        assert CompetitivePattern.icp_mismatch == "icp_mismatch"

    def test_all_members(self):
        expected = {"none", "high_loss_rate", "no_competitive_intel",
                    "price_driven_loss", "feature_gap_loss", "icp_mismatch"}
        assert set(p.value for p in CompetitivePattern) == expected

    def test_is_str_enum(self):
        assert isinstance(CompetitivePattern.none, str)


class TestCompetitiveSeverity:
    def test_dominant(self):
        assert CompetitiveSeverity.dominant == "dominant"

    def test_competitive(self):
        assert CompetitiveSeverity.competitive == "competitive"

    def test_challenged(self):
        assert CompetitiveSeverity.challenged == "challenged"

    def test_losing(self):
        assert CompetitiveSeverity.losing == "losing"

    def test_all_members(self):
        assert set(s.value for s in CompetitiveSeverity) == {
            "dominant", "competitive", "challenged", "losing"
        }

    def test_is_str_enum(self):
        assert isinstance(CompetitiveSeverity.dominant, str)


class TestCompetitiveAction:
    def test_no_action(self):
        assert CompetitiveAction.no_action == "no_action"

    def test_competitive_training(self):
        assert CompetitiveAction.competitive_training == "competitive_training"

    def test_deal_coaching(self):
        assert CompetitiveAction.deal_coaching == "deal_coaching"

    def test_value_positioning(self):
        assert CompetitiveAction.value_positioning == "value_positioning"

    def test_product_feedback_escalation(self):
        assert CompetitiveAction.product_feedback_escalation == "product_feedback_escalation"

    def test_competitive_win_back(self):
        assert CompetitiveAction.competitive_win_back == "competitive_win_back"

    def test_all_members(self):
        expected = {
            "no_action", "competitive_training", "deal_coaching",
            "value_positioning", "product_feedback_escalation", "competitive_win_back"
        }
        assert set(a.value for a in CompetitiveAction) == expected

    def test_is_str_enum(self):
        assert isinstance(CompetitiveAction.no_action, str)


# ===========================================================================
# 2. WIN RATE SCORE
# ===========================================================================

class TestWinRateScore:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    # --- win_rate thresholds ---
    def test_win_rate_below_0_25_adds_45(self):
        # wins=2/total=10 → win_rate=0.20 < 0.25 → +45
        inp = make_input(total_competitive_deals=10, competitive_wins=2, competitive_losses=5,
                         win_rate_vs_top_competitor_pct=0.50)
        s = self.eng._win_rate_score(inp)
        assert s >= 45.0

    def test_win_rate_exactly_0_25_not_below(self):
        # wins=5/total=20 → win_rate=0.25, NOT < 0.25 → +25 branch if < 0.40
        inp = make_input(total_competitive_deals=20, competitive_wins=5, competitive_losses=2,
                         win_rate_vs_top_competitor_pct=0.50)
        s = self.eng._win_rate_score(inp)
        assert s < 45.0  # 0.25 does NOT trigger < 0.25 branch

    def test_win_rate_0_30_adds_25(self):
        # wins=3/total=10 → win_rate=0.30 in [0.25, 0.40) → +25
        inp = make_input(total_competitive_deals=10, competitive_wins=3, competitive_losses=2,
                         win_rate_vs_top_competitor_pct=0.50)
        score_contribution = 25.0
        s = self.eng._win_rate_score(inp)
        # At least 25 from win_rate bucket
        assert s >= score_contribution

    def test_win_rate_0_40_not_in_25_bucket(self):
        # wins=8/total=20 → win_rate=0.40 NOT < 0.40 → +10 (if < 0.55)
        inp = make_input(total_competitive_deals=20, competitive_wins=8, competitive_losses=2,
                         win_rate_vs_top_competitor_pct=0.50)
        # Should be in 0.40–0.55 range: +10
        s = self.eng._win_rate_score(inp)
        assert s >= 10.0

    def test_win_rate_0_50_adds_10(self):
        # wins=5/total=10 → win_rate=0.50 in [0.40, 0.55) → +10
        inp = make_input(total_competitive_deals=10, competitive_wins=5, competitive_losses=1,
                         win_rate_vs_top_competitor_pct=0.50)
        s = self.eng._win_rate_score(inp)
        assert s >= 10.0

    def test_win_rate_0_55_adds_0(self):
        # wins=6/total=10 → 0.60 >= 0.55 → +0 from win bucket
        inp = make_input(total_competitive_deals=10, competitive_wins=6, competitive_losses=1,
                         win_rate_vs_top_competitor_pct=0.50)
        # Only other buckets contribute
        s = self.eng._win_rate_score(inp)
        # win rate bucket contributes 0 here
        assert s >= 0

    # --- loss_rate thresholds ---
    def test_loss_rate_ge_0_60_adds_30(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=1, competitive_losses=6,
                         win_rate_vs_top_competitor_pct=0.50)
        s = self.eng._win_rate_score(inp)
        # wins=1 → +45 (win_rate=0.1), losses=6 → +30, competitor_rate=0.5 → +0
        assert s == min(75.0, 100.0)

    def test_loss_rate_exactly_0_60_adds_30(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=1, competitive_losses=6,
                         win_rate_vs_top_competitor_pct=0.50)
        s = self.eng._win_rate_score(inp)
        assert s >= 30.0

    def test_loss_rate_0_50_adds_15(self):
        # losses=5/total=10 → 0.50 in [0.45, 0.60) → +15
        inp = make_input(total_competitive_deals=10, competitive_wins=3, competitive_losses=5,
                         win_rate_vs_top_competitor_pct=0.50)
        s = self.eng._win_rate_score(inp)
        assert s >= 15.0

    def test_loss_rate_0_30_adds_5(self):
        # losses=3/total=10 → 0.30 in [0.30, 0.45) → +5
        inp = make_input(total_competitive_deals=10, competitive_wins=6, competitive_losses=3,
                         win_rate_vs_top_competitor_pct=0.60)
        s = self.eng._win_rate_score(inp)
        assert s >= 5.0

    def test_loss_rate_below_0_30_adds_0(self):
        # losses=2/total=10 → 0.20 < 0.30 → +0
        inp = make_input(total_competitive_deals=10, competitive_wins=7, competitive_losses=2,
                         win_rate_vs_top_competitor_pct=0.60)
        s = self.eng._win_rate_score(inp)
        # wins=7 → 0.70 >= 0.55 → +0 from win, loss=0.20 → +0, competitor_rate >= 0.35 → +0
        assert s == 0.0

    # --- win_rate_vs_top_competitor thresholds ---
    def test_competitor_rate_below_0_20_adds_15(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7, competitive_losses=2,
                         win_rate_vs_top_competitor_pct=0.10)
        s = self.eng._win_rate_score(inp)
        assert s >= 15.0

    def test_competitor_rate_exactly_0_20_not_below(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7, competitive_losses=2,
                         win_rate_vs_top_competitor_pct=0.20)
        # 0.20 NOT < 0.20, but < 0.35 → +7
        s = self.eng._win_rate_score(inp)
        assert s >= 7.0

    def test_competitor_rate_0_30_adds_7(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7, competitive_losses=2,
                         win_rate_vs_top_competitor_pct=0.30)
        s = self.eng._win_rate_score(inp)
        assert s >= 7.0

    def test_competitor_rate_ge_0_35_adds_0(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7, competitive_losses=2,
                         win_rate_vs_top_competitor_pct=0.35)
        s = self.eng._win_rate_score(inp)
        # win=0.7 → +0, loss=0.2 → +0, competitor_rate=0.35 → +0
        assert s == 0.0

    def test_capped_at_100(self):
        # Max possible: +45 + 30 + 15 = 90 ≤ 100
        inp = make_input(total_competitive_deals=10, competitive_wins=1, competitive_losses=7,
                         win_rate_vs_top_competitor_pct=0.10)
        s = self.eng._win_rate_score(inp)
        assert s <= 100.0

    def test_total_zero_treated_as_one(self):
        inp = make_input(total_competitive_deals=0, competitive_wins=0, competitive_losses=0,
                         win_rate_vs_top_competitor_pct=0.50)
        s = self.eng._win_rate_score(inp)
        # wins/max(0,1)=0 → < 0.25 → +45; losses/1=0 → +0; competitor rate 0.5 → +0
        assert s == 45.0

    def test_returns_float(self):
        inp = make_input()
        s = self.eng._win_rate_score(inp)
        assert isinstance(s, float)


# ===========================================================================
# 3. COMPETITIVE INTEL SCORE
# ===========================================================================

class TestCompetitiveIntelScore:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_intel_rate_below_0_30_adds_40(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=2,
                         battle_card_used_count=5, proof_of_concept_win_rate_pct=0.60)
        s = self.eng._competitive_intel_score(inp)
        assert s >= 40.0

    def test_intel_rate_exactly_0_30_not_below(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=3,
                         battle_card_used_count=5, proof_of_concept_win_rate_pct=0.60)
        # 3/10=0.30 NOT < 0.30 → NOT +40, but < 0.50 → +20
        s = self.eng._competitive_intel_score(inp)
        assert s >= 20.0
        # Make sure the 40 bucket wasn't triggered
        # battle=5/10=0.50 → NOT < 0.40 → 0; poc=0.60 → 0
        assert s == 20.0

    def test_intel_rate_0_40_adds_20(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=4,
                         battle_card_used_count=9, proof_of_concept_win_rate_pct=0.60)
        # intel=0.40 in [0.30, 0.50) → +20; battle=0.9 → +0; poc=0.60 → +0
        s = self.eng._competitive_intel_score(inp)
        assert s == 20.0

    def test_intel_rate_0_60_adds_8(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=6,
                         battle_card_used_count=9, proof_of_concept_win_rate_pct=0.60)
        # intel=0.60 in [0.50, 0.70) → +8; battle=0.9 → +0; poc=0.60 → +0
        s = self.eng._competitive_intel_score(inp)
        assert s == 8.0

    def test_intel_rate_exactly_0_70_adds_0(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=7,
                         battle_card_used_count=9, proof_of_concept_win_rate_pct=0.60)
        # intel=0.70 NOT < 0.70 → +0; battle=0.9 → +0; poc=0.60 → +0
        s = self.eng._competitive_intel_score(inp)
        assert s == 0.0

    def test_battle_rate_below_0_20_adds_30(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=7,
                         battle_card_used_count=1, proof_of_concept_win_rate_pct=0.60)
        # intel=0.7 → +0; battle=0.10 < 0.20 → +30; poc=0.60 → +0
        s = self.eng._competitive_intel_score(inp)
        assert s == 30.0

    def test_battle_rate_exactly_0_20_not_below(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=7,
                         battle_card_used_count=2, proof_of_concept_win_rate_pct=0.60)
        # battle=0.20 NOT < 0.20 → checks < 0.40 → +15
        s = self.eng._competitive_intel_score(inp)
        assert s == 15.0

    def test_battle_rate_0_30_adds_15(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=7,
                         battle_card_used_count=3, proof_of_concept_win_rate_pct=0.60)
        s = self.eng._competitive_intel_score(inp)
        assert s == 15.0

    def test_battle_rate_exactly_0_40_adds_0(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=7,
                         battle_card_used_count=4, proof_of_concept_win_rate_pct=0.60)
        # battle=0.40 NOT < 0.40 → +0; intel=0.7 → +0; poc=0.60 → +0
        s = self.eng._competitive_intel_score(inp)
        assert s == 0.0

    def test_poc_below_0_30_adds_20(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=7,
                         battle_card_used_count=4, proof_of_concept_win_rate_pct=0.20)
        # poc=0.20 < 0.30 → +20; rest → +0
        s = self.eng._competitive_intel_score(inp)
        assert s == 20.0

    def test_poc_exactly_0_30_not_below(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=7,
                         battle_card_used_count=4, proof_of_concept_win_rate_pct=0.30)
        # poc=0.30 NOT < 0.30 → checks < 0.50 → +10
        s = self.eng._competitive_intel_score(inp)
        assert s == 10.0

    def test_poc_0_40_adds_10(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=7,
                         battle_card_used_count=4, proof_of_concept_win_rate_pct=0.40)
        s = self.eng._competitive_intel_score(inp)
        assert s == 10.0

    def test_poc_exactly_0_50_adds_0(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=7,
                         battle_card_used_count=4, proof_of_concept_win_rate_pct=0.50)
        s = self.eng._competitive_intel_score(inp)
        assert s == 0.0

    def test_capped_at_100(self):
        inp = make_input(total_competitive_deals=10, competitive_intel_documented_count=1,
                         battle_card_used_count=1, proof_of_concept_win_rate_pct=0.10)
        s = self.eng._competitive_intel_score(inp)
        # +40 + 30 + 20 = 90 ≤ 100
        assert s == 90.0
        assert s <= 100.0

    def test_total_zero_treated_as_one(self):
        inp = make_input(total_competitive_deals=0, competitive_intel_documented_count=0,
                         battle_card_used_count=0, proof_of_concept_win_rate_pct=0.50)
        s = self.eng._competitive_intel_score(inp)
        # intel=0/1=0 < 0.30 → +40; battle=0/1=0 < 0.20 → +30; poc=0.50 → +0
        assert s == 70.0

    def test_returns_float(self):
        assert isinstance(self.eng._competitive_intel_score(make_input()), float)


# ===========================================================================
# 4. DEAL QUALITY SCORE
# ===========================================================================

class TestDealQualityScore:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_price_loss_rate_ge_0_40_adds_40(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=4,
                         deals_lost_on_features_competitive=0, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        s = self.eng._deal_quality_score(inp)
        assert s >= 40.0

    def test_price_loss_rate_exactly_0_40_adds_40(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=4,
                         deals_lost_on_features_competitive=0, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        s = self.eng._deal_quality_score(inp)
        assert s == 40.0

    def test_price_loss_rate_0_30_adds_20(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=3,
                         deals_lost_on_features_competitive=0, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        s = self.eng._deal_quality_score(inp)
        assert s == 20.0

    def test_price_loss_rate_exactly_0_25_adds_20(self):
        inp = make_input(total_competitive_deals=20, deals_lost_on_price_competitive=5,
                         deals_lost_on_features_competitive=0, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        s = self.eng._deal_quality_score(inp)
        assert s == 20.0

    def test_price_loss_rate_0_10_adds_8(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=1,
                         deals_lost_on_features_competitive=0, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        s = self.eng._deal_quality_score(inp)
        assert s == 8.0

    def test_price_loss_rate_below_0_10_adds_0(self):
        inp = make_input(total_competitive_deals=20, deals_lost_on_price_competitive=1,
                         deals_lost_on_features_competitive=0, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        # 1/20=0.05 < 0.10 → +0
        s = self.eng._deal_quality_score(inp)
        assert s == 0.0

    def test_feature_loss_rate_ge_0_30_adds_30(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=3, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        s = self.eng._deal_quality_score(inp)
        assert s == 30.0

    def test_feature_loss_rate_exactly_0_30_adds_30(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=3, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        s = self.eng._deal_quality_score(inp)
        assert s >= 30.0

    def test_feature_loss_rate_0_20_adds_15(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=2, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        s = self.eng._deal_quality_score(inp)
        assert s == 15.0

    def test_feature_loss_rate_exactly_0_15_adds_15(self):
        inp = make_input(total_competitive_deals=20, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=3, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        s = self.eng._deal_quality_score(inp)
        assert s == 15.0

    def test_feature_loss_rate_below_0_15_adds_0(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=1, competitive_losses=1,
                         single_stakeholder_competitive_losses=0)
        # 1/10=0.10 < 0.15 → +0
        s = self.eng._deal_quality_score(inp)
        assert s == 0.0

    def test_single_loss_rate_ge_0_60_adds_20(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0, competitive_losses=5,
                         single_stakeholder_competitive_losses=3)
        # single_loss=3/5=0.60 >= 0.60 → +20
        s = self.eng._deal_quality_score(inp)
        assert s == 20.0

    def test_single_loss_rate_exactly_0_60_adds_20(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0, competitive_losses=5,
                         single_stakeholder_competitive_losses=3)
        s = self.eng._deal_quality_score(inp)
        assert s == 20.0

    def test_single_loss_rate_0_50_adds_10(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0, competitive_losses=4,
                         single_stakeholder_competitive_losses=2)
        # 2/4=0.50 >= 0.40 but < 0.60 → +10
        s = self.eng._deal_quality_score(inp)
        assert s == 10.0

    def test_single_loss_rate_below_0_40_adds_0(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0, competitive_losses=5,
                         single_stakeholder_competitive_losses=1)
        # 1/5=0.20 < 0.40 → +0
        s = self.eng._deal_quality_score(inp)
        assert s == 0.0

    def test_no_losses_skips_single_stakeholder_ge_0_60(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0, competitive_losses=0,
                         single_stakeholder_competitive_losses=5)
        # competitive_losses == 0 → condition not met
        s = self.eng._deal_quality_score(inp)
        assert s == 0.0

    def test_no_losses_skips_single_stakeholder_ge_0_40(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0, competitive_losses=0,
                         single_stakeholder_competitive_losses=3)
        s = self.eng._deal_quality_score(inp)
        assert s == 0.0

    def test_capped_at_100(self):
        inp = make_input(total_competitive_deals=10, deals_lost_on_price_competitive=4,
                         deals_lost_on_features_competitive=3, competitive_losses=5,
                         single_stakeholder_competitive_losses=3)
        s = self.eng._deal_quality_score(inp)
        # +40 + 30 + 20 = 90 ≤ 100
        assert s == 90.0

    def test_returns_float(self):
        assert isinstance(self.eng._deal_quality_score(make_input()), float)


# ===========================================================================
# 5. COMPETITIVE RESILIENCE SCORE
# ===========================================================================

class TestCompetitiveResilienceScore:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_displacement_net_ge_3_adds_40(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=5,
                         competitive_displacement_wins=1, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        # net=4 >= 3 → +40
        s = self.eng._competitive_resilience_score(inp)
        assert s >= 40.0

    def test_displacement_net_exactly_3_adds_40(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=4,
                         competitive_displacement_wins=1, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        # net=3 → +40
        s = self.eng._competitive_resilience_score(inp)
        assert s >= 40.0

    def test_displacement_net_1_adds_20(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=2,
                         competitive_displacement_wins=1, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        # net=1 >= 1 → +20
        s = self.eng._competitive_resilience_score(inp)
        assert s >= 20.0

    def test_displacement_net_exactly_1_adds_20(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=2,
                         competitive_displacement_wins=1, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        s = self.eng._competitive_resilience_score(inp)
        assert s >= 20.0

    def test_displacement_net_0_adds_0(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=2,
                         competitive_displacement_wins=2, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        # net=0 → +0 from displacement_net bucket
        s = self.eng._competitive_resilience_score(inp)
        # displacement_rate=2/10=0.20 → +30; multi_win=4/5=0.80 → +0
        assert s == 30.0

    def test_displacement_net_negative_adds_0(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=1,
                         competitive_displacement_wins=3, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        # net=-2 → +0
        s = self.eng._competitive_resilience_score(inp)
        # displacement_rate=1/10=0.10 → +15; multi_win=4/5=0.80 → +0
        assert s == 15.0

    def test_displacement_rate_ge_0_20_adds_30(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=2,
                         competitive_displacement_wins=2, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        # rate=2/10=0.20 >= 0.20 → +30
        s = self.eng._competitive_resilience_score(inp)
        assert s >= 30.0

    def test_displacement_rate_exactly_0_20_adds_30(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=2,
                         competitive_displacement_wins=2, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        s = self.eng._competitive_resilience_score(inp)
        assert s == 30.0

    def test_displacement_rate_0_15_adds_15(self):
        inp = make_input(total_competitive_deals=20, deals_displaced_by_competitor=3,
                         competitive_displacement_wins=3, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        # rate=3/20=0.15 in [0.10, 0.20) → +15
        s = self.eng._competitive_resilience_score(inp)
        assert s == 15.0

    def test_displacement_rate_exactly_0_10_adds_15(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=1,
                         competitive_displacement_wins=1, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        # rate=1/10=0.10 → +15
        s = self.eng._competitive_resilience_score(inp)
        assert s == 15.0

    def test_displacement_rate_below_0_10_adds_0(self):
        inp = make_input(total_competitive_deals=20, deals_displaced_by_competitor=1,
                         competitive_displacement_wins=1, competitive_wins=5,
                         multi_stakeholder_competitive_wins=4)
        # rate=1/20=0.05 → +0
        s = self.eng._competitive_resilience_score(inp)
        assert s == 0.0

    def test_multi_win_rate_below_0_30_adds_20(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=0,
                         competitive_displacement_wins=0, competitive_wins=5,
                         multi_stakeholder_competitive_wins=1)
        # rate=1/5=0.20 < 0.30 → +20
        s = self.eng._competitive_resilience_score(inp)
        assert s >= 20.0

    def test_multi_win_rate_exactly_0_30_not_below_0_30(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=0,
                         competitive_displacement_wins=0, competitive_wins=10,
                         multi_stakeholder_competitive_wins=3)
        # rate=3/10=0.30 NOT < 0.30, check < 0.50 → +10
        s = self.eng._competitive_resilience_score(inp)
        assert s == 10.0

    def test_multi_win_rate_0_40_adds_10(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=0,
                         competitive_displacement_wins=0, competitive_wins=10,
                         multi_stakeholder_competitive_wins=4)
        s = self.eng._competitive_resilience_score(inp)
        assert s == 10.0

    def test_multi_win_rate_exactly_0_50_adds_0(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=0,
                         competitive_displacement_wins=0, competitive_wins=10,
                         multi_stakeholder_competitive_wins=5)
        s = self.eng._competitive_resilience_score(inp)
        assert s == 0.0

    def test_no_wins_skips_multi_stakeholder_below_0_30(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=0,
                         competitive_displacement_wins=0, competitive_wins=0,
                         multi_stakeholder_competitive_wins=0)
        # competitive_wins == 0 → both multi_stakeholder branches skipped
        s = self.eng._competitive_resilience_score(inp)
        assert s == 0.0

    def test_capped_at_100(self):
        inp = make_input(total_competitive_deals=10, deals_displaced_by_competitor=8,
                         competitive_displacement_wins=1, competitive_wins=2,
                         multi_stakeholder_competitive_wins=0)
        # net=7 → +40; rate=8/10=0.80 → +30; multi=0/2=0.0 → +20 → total=90
        s = self.eng._competitive_resilience_score(inp)
        assert s <= 100.0

    def test_returns_float(self):
        assert isinstance(self.eng._competitive_resilience_score(make_input()), float)


# ===========================================================================
# 6. PATTERN DETECTION
# ===========================================================================

class TestDetectPattern:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def _call(self, inp, win_rate, intel, deal_quality, resilience):
        return self.eng._detect_pattern(inp, win_rate, intel, deal_quality, resilience)

    # --- high_loss_rate ---
    def test_high_loss_rate_detected(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=5,
                         competitive_intel_documented_count=7,
                         deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        # loss_rate=5/10=0.50 >= 0.50; win_rate_score=35 >= 35
        p = self._call(inp, win_rate=35, intel=10, deal_quality=10, resilience=10)
        assert p == CompetitivePattern.high_loss_rate

    def test_high_loss_rate_win_rate_score_exactly_35(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=5,
                         competitive_intel_documented_count=7,
                         deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        p = self._call(inp, win_rate=35, intel=10, deal_quality=10, resilience=10)
        assert p == CompetitivePattern.high_loss_rate

    def test_high_loss_rate_not_triggered_win_score_below_35(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=5,
                         competitive_intel_documented_count=2,
                         deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        # win_rate_score=34 < 35 → skip
        p = self._call(inp, win_rate=34, intel=10, deal_quality=10, resilience=10)
        assert p != CompetitivePattern.high_loss_rate

    def test_high_loss_rate_not_triggered_loss_rate_below_0_50(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=4,
                         competitive_intel_documented_count=7,
                         deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        # loss_rate=4/10=0.40 < 0.50 → skip
        p = self._call(inp, win_rate=35, intel=10, deal_quality=10, resilience=10)
        assert p != CompetitivePattern.high_loss_rate

    # --- no_competitive_intel ---
    def test_no_competitive_intel_detected(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=3,
                         deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        # intel_rate=3/10=0.30 < 0.40; intel_score=30 >= 30
        p = self._call(inp, win_rate=10, intel=30, deal_quality=10, resilience=10)
        assert p == CompetitivePattern.no_competitive_intel

    def test_no_competitive_intel_exactly_30_score(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=3,
                         deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        p = self._call(inp, win_rate=10, intel=30, deal_quality=10, resilience=10)
        assert p == CompetitivePattern.no_competitive_intel

    def test_no_competitive_intel_not_triggered_intel_score_below_30(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=3,
                         deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        p = self._call(inp, win_rate=10, intel=29, deal_quality=10, resilience=10)
        assert p != CompetitivePattern.no_competitive_intel

    def test_no_competitive_intel_not_triggered_intel_rate_ge_0_40(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=4,
                         deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        # intel_rate=4/10=0.40 NOT < 0.40
        p = self._call(inp, win_rate=10, intel=30, deal_quality=10, resilience=10)
        assert p != CompetitivePattern.no_competitive_intel

    # --- price_driven_loss ---
    def test_price_driven_loss_detected(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=3,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        # price_loss_rate=3/10=0.30 >= 0.30; deal_quality=30 >= 30
        p = self._call(inp, win_rate=10, intel=10, deal_quality=30, resilience=10)
        assert p == CompetitivePattern.price_driven_loss

    def test_price_driven_loss_not_triggered_deal_quality_below_30(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=3,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        p = self._call(inp, win_rate=10, intel=10, deal_quality=29, resilience=10)
        assert p != CompetitivePattern.price_driven_loss

    def test_price_driven_loss_not_triggered_price_rate_below_0_30(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=2,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        # price_rate=2/10=0.20 < 0.30
        p = self._call(inp, win_rate=10, intel=10, deal_quality=30, resilience=10)
        assert p != CompetitivePattern.price_driven_loss

    # --- feature_gap_loss ---
    def test_feature_gap_loss_detected(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=2,
                         deals_lost_on_features_competitive=2,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        # feature_loss_rate=2/10=0.20 >= 0.20; deal_quality=25 >= 25
        p = self._call(inp, win_rate=10, intel=10, deal_quality=25, resilience=10)
        assert p == CompetitivePattern.feature_gap_loss

    def test_feature_gap_loss_not_triggered_deal_quality_below_25(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=2,
                         deals_lost_on_features_competitive=2,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        p = self._call(inp, win_rate=10, intel=10, deal_quality=24, resilience=10)
        assert p != CompetitivePattern.feature_gap_loss

    def test_feature_gap_loss_not_triggered_feature_rate_below_0_20(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=2,
                         deals_lost_on_features_competitive=1,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        # 1/10=0.10 < 0.20
        p = self._call(inp, win_rate=10, intel=10, deal_quality=25, resilience=10)
        assert p != CompetitivePattern.feature_gap_loss

    # --- icp_mismatch ---
    def test_icp_mismatch_detected(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=1,
                         deals_lost_on_features_competitive=1,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=2)
        # displacement_net=2-0=2 >= 2; resilience=25 >= 25
        p = self._call(inp, win_rate=10, intel=10, deal_quality=10, resilience=25)
        assert p == CompetitivePattern.icp_mismatch

    def test_icp_mismatch_not_triggered_resilience_below_25(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=1,
                         deals_lost_on_features_competitive=1,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=2)
        p = self._call(inp, win_rate=10, intel=10, deal_quality=10, resilience=24)
        assert p != CompetitivePattern.icp_mismatch

    def test_icp_mismatch_not_triggered_displacement_net_below_2(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=1,
                         deals_lost_on_features_competitive=1,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=1)
        # net=1 < 2
        p = self._call(inp, win_rate=10, intel=10, deal_quality=10, resilience=25)
        assert p != CompetitivePattern.icp_mismatch

    # --- none ---
    def test_none_pattern_when_no_conditions_met(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=1,
                         competitive_intel_documented_count=7,
                         deals_lost_on_price_competitive=1,
                         deals_lost_on_features_competitive=1,
                         competitive_displacement_wins=2, deals_displaced_by_competitor=2)
        p = self._call(inp, win_rate=10, intel=10, deal_quality=10, resilience=10)
        assert p == CompetitivePattern.none

    # --- priority ordering ---
    def test_high_loss_rate_takes_priority_over_no_intel(self):
        """high_loss_rate checked before no_competitive_intel."""
        inp = make_input(total_competitive_deals=10, competitive_losses=5,
                         competitive_intel_documented_count=2,  # intel_rate=0.2 < 0.40
                         deals_lost_on_price_competitive=0,
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        # Both conditions met
        p = self._call(inp, win_rate=35, intel=40, deal_quality=30, resilience=25)
        assert p == CompetitivePattern.high_loss_rate

    def test_no_intel_takes_priority_over_price_driven(self):
        """no_competitive_intel checked before price_driven_loss."""
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=3,  # rate=0.30 < 0.40
                         deals_lost_on_price_competitive=3,    # rate=0.30 >= 0.30
                         deals_lost_on_features_competitive=0,
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        p = self._call(inp, win_rate=10, intel=30, deal_quality=30, resilience=10)
        assert p == CompetitivePattern.no_competitive_intel

    def test_price_driven_takes_priority_over_feature_gap(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=3,    # rate=0.30 >= 0.30
                         deals_lost_on_features_competitive=2, # rate=0.20 >= 0.20
                         competitive_displacement_wins=0, deals_displaced_by_competitor=0)
        p = self._call(inp, win_rate=10, intel=10, deal_quality=30, resilience=10)
        assert p == CompetitivePattern.price_driven_loss

    def test_feature_gap_takes_priority_over_icp_mismatch(self):
        inp = make_input(total_competitive_deals=10, competitive_losses=2,
                         competitive_intel_documented_count=5,
                         deals_lost_on_price_competitive=1,    # rate=0.10 < 0.30
                         deals_lost_on_features_competitive=2, # rate=0.20 >= 0.20
                         competitive_displacement_wins=0, deals_displaced_by_competitor=2)  # net=2
        p = self._call(inp, win_rate=10, intel=10, deal_quality=25, resilience=25)
        assert p == CompetitivePattern.feature_gap_loss


# ===========================================================================
# 7. RISK LEVEL
# ===========================================================================

class TestRiskLevel:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_below_20_is_low(self):
        assert self.eng._risk_level(0.0) == CompetitiveRisk.low
        assert self.eng._risk_level(19.9) == CompetitiveRisk.low

    def test_exactly_20_is_moderate(self):
        assert self.eng._risk_level(20.0) == CompetitiveRisk.moderate

    def test_20_to_39_9_is_moderate(self):
        assert self.eng._risk_level(25.0) == CompetitiveRisk.moderate
        assert self.eng._risk_level(39.9) == CompetitiveRisk.moderate

    def test_exactly_40_is_high(self):
        assert self.eng._risk_level(40.0) == CompetitiveRisk.high

    def test_40_to_59_9_is_high(self):
        assert self.eng._risk_level(50.0) == CompetitiveRisk.high
        assert self.eng._risk_level(59.9) == CompetitiveRisk.high

    def test_exactly_60_is_critical(self):
        assert self.eng._risk_level(60.0) == CompetitiveRisk.critical

    def test_above_60_is_critical(self):
        assert self.eng._risk_level(70.0) == CompetitiveRisk.critical
        assert self.eng._risk_level(100.0) == CompetitiveRisk.critical


# ===========================================================================
# 8. SEVERITY
# ===========================================================================

class TestSeverity:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_below_20_is_dominant(self):
        assert self.eng._severity(0.0) == CompetitiveSeverity.dominant
        assert self.eng._severity(19.9) == CompetitiveSeverity.dominant

    def test_exactly_20_is_competitive(self):
        assert self.eng._severity(20.0) == CompetitiveSeverity.competitive

    def test_20_to_39_9_is_competitive(self):
        assert self.eng._severity(25.0) == CompetitiveSeverity.competitive
        assert self.eng._severity(39.9) == CompetitiveSeverity.competitive

    def test_exactly_40_is_challenged(self):
        assert self.eng._severity(40.0) == CompetitiveSeverity.challenged

    def test_40_to_59_9_is_challenged(self):
        assert self.eng._severity(50.0) == CompetitiveSeverity.challenged
        assert self.eng._severity(59.9) == CompetitiveSeverity.challenged

    def test_exactly_60_is_losing(self):
        assert self.eng._severity(60.0) == CompetitiveSeverity.losing

    def test_above_60_is_losing(self):
        assert self.eng._severity(80.0) == CompetitiveSeverity.losing
        assert self.eng._severity(100.0) == CompetitiveSeverity.losing


# ===========================================================================
# 9. ACTION
# ===========================================================================

class TestAction:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    # critical risk
    def test_critical_high_loss_rate(self):
        a = self.eng._action(CompetitiveRisk.critical, CompetitivePattern.high_loss_rate)
        assert a == CompetitiveAction.competitive_win_back

    def test_critical_no_competitive_intel(self):
        a = self.eng._action(CompetitiveRisk.critical, CompetitivePattern.no_competitive_intel)
        assert a == CompetitiveAction.competitive_training

    def test_critical_price_driven_loss(self):
        a = self.eng._action(CompetitiveRisk.critical, CompetitivePattern.price_driven_loss)
        assert a == CompetitiveAction.deal_coaching

    def test_critical_feature_gap_loss(self):
        a = self.eng._action(CompetitiveRisk.critical, CompetitivePattern.feature_gap_loss)
        assert a == CompetitiveAction.deal_coaching

    def test_critical_icp_mismatch(self):
        a = self.eng._action(CompetitiveRisk.critical, CompetitivePattern.icp_mismatch)
        assert a == CompetitiveAction.deal_coaching

    def test_critical_none_pattern(self):
        a = self.eng._action(CompetitiveRisk.critical, CompetitivePattern.none)
        assert a == CompetitiveAction.deal_coaching

    # high risk
    def test_high_price_driven_loss(self):
        a = self.eng._action(CompetitiveRisk.high, CompetitivePattern.price_driven_loss)
        assert a == CompetitiveAction.value_positioning

    def test_high_feature_gap_loss(self):
        a = self.eng._action(CompetitiveRisk.high, CompetitivePattern.feature_gap_loss)
        assert a == CompetitiveAction.product_feedback_escalation

    def test_high_high_loss_rate(self):
        a = self.eng._action(CompetitiveRisk.high, CompetitivePattern.high_loss_rate)
        assert a == CompetitiveAction.deal_coaching

    def test_high_no_competitive_intel(self):
        a = self.eng._action(CompetitiveRisk.high, CompetitivePattern.no_competitive_intel)
        assert a == CompetitiveAction.deal_coaching

    def test_high_icp_mismatch(self):
        a = self.eng._action(CompetitiveRisk.high, CompetitivePattern.icp_mismatch)
        assert a == CompetitiveAction.deal_coaching

    def test_high_none_pattern(self):
        a = self.eng._action(CompetitiveRisk.high, CompetitivePattern.none)
        assert a == CompetitiveAction.deal_coaching

    # moderate risk
    def test_moderate_any_pattern_is_training(self):
        for p in CompetitivePattern:
            a = self.eng._action(CompetitiveRisk.moderate, p)
            assert a == CompetitiveAction.competitive_training

    # low risk
    def test_low_any_pattern_is_no_action(self):
        for p in CompetitivePattern:
            a = self.eng._action(CompetitiveRisk.low, p)
            assert a == CompetitiveAction.no_action


# ===========================================================================
# 10. IS_COMPETITIVE_THREAT
# ===========================================================================

class TestIsCompetitiveThreat:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_threat_due_to_composite_ge_40(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7,
                         deals_displaced_by_competitor=1, competitive_displacement_wins=1)
        assert self.eng._is_competitive_threat(40.0, inp) is True

    def test_threat_exactly_40_composite(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7,
                         deals_displaced_by_competitor=0, competitive_displacement_wins=0)
        assert self.eng._is_competitive_threat(40.0, inp) is True

    def test_no_threat_composite_39(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7,
                         deals_displaced_by_competitor=0, competitive_displacement_wins=0)
        # win_rate=7/10=0.70 >= 0.25; displacement_net=0; composite<40
        assert self.eng._is_competitive_threat(39.0, inp) is False

    def test_threat_due_to_win_rate_below_0_25(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=2,
                         deals_displaced_by_competitor=0, competitive_displacement_wins=0)
        # win_rate=2/10=0.20 < 0.25 → threat
        assert self.eng._is_competitive_threat(10.0, inp) is True

    def test_threat_win_rate_exactly_0_25_not_threat(self):
        inp = make_input(total_competitive_deals=20, competitive_wins=5,
                         deals_displaced_by_competitor=0, competitive_displacement_wins=0)
        # win_rate=5/20=0.25 NOT < 0.25 → no threat from this alone
        assert self.eng._is_competitive_threat(10.0, inp) is False

    def test_threat_due_to_displacement_net_ge_2(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7,
                         deals_displaced_by_competitor=3, competitive_displacement_wins=1)
        # net=2 >= 2 → threat
        assert self.eng._is_competitive_threat(10.0, inp) is True

    def test_threat_displacement_exactly_2(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7,
                         deals_displaced_by_competitor=2, competitive_displacement_wins=0)
        assert self.eng._is_competitive_threat(10.0, inp) is True

    def test_no_threat_displacement_net_1(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7,
                         deals_displaced_by_competitor=1, competitive_displacement_wins=0)
        # net=1 < 2
        assert self.eng._is_competitive_threat(10.0, inp) is False

    def test_no_threat_all_conditions_false(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=7,
                         deals_displaced_by_competitor=0, competitive_displacement_wins=0)
        assert self.eng._is_competitive_threat(10.0, inp) is False


# ===========================================================================
# 11. REQUIRES_COMPETITIVE_COACHING
# ===========================================================================

class TestRequiresCompetitiveCoaching:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_coaching_due_to_composite_ge_30(self):
        inp = make_input(total_competitive_deals=10,
                         competitive_intel_documented_count=5,
                         proof_of_concept_win_rate_pct=0.50)
        assert self.eng._requires_competitive_coaching(30.0, inp) is True

    def test_coaching_exactly_30_composite(self):
        inp = make_input(total_competitive_deals=10,
                         competitive_intel_documented_count=5,
                         proof_of_concept_win_rate_pct=0.50)
        assert self.eng._requires_competitive_coaching(30.0, inp) is True

    def test_no_coaching_composite_29(self):
        inp = make_input(total_competitive_deals=10,
                         competitive_intel_documented_count=5,
                         proof_of_concept_win_rate_pct=0.50)
        # intel_rate=5/10=0.50 >= 0.40; poc=0.50 >= 0.30
        assert self.eng._requires_competitive_coaching(29.0, inp) is False

    def test_coaching_due_to_intel_rate_below_0_40(self):
        inp = make_input(total_competitive_deals=10,
                         competitive_intel_documented_count=3,
                         proof_of_concept_win_rate_pct=0.50)
        # intel_rate=3/10=0.30 < 0.40
        assert self.eng._requires_competitive_coaching(10.0, inp) is True

    def test_no_coaching_intel_rate_exactly_0_40(self):
        inp = make_input(total_competitive_deals=10,
                         competitive_intel_documented_count=4,
                         proof_of_concept_win_rate_pct=0.50)
        # intel_rate=4/10=0.40 NOT < 0.40
        assert self.eng._requires_competitive_coaching(10.0, inp) is False

    def test_coaching_due_to_poc_below_0_30(self):
        inp = make_input(total_competitive_deals=10,
                         competitive_intel_documented_count=5,
                         proof_of_concept_win_rate_pct=0.20)
        assert self.eng._requires_competitive_coaching(10.0, inp) is True

    def test_no_coaching_poc_exactly_0_30(self):
        inp = make_input(total_competitive_deals=10,
                         competitive_intel_documented_count=5,
                         proof_of_concept_win_rate_pct=0.30)
        # poc=0.30 NOT < 0.30
        assert self.eng._requires_competitive_coaching(10.0, inp) is False

    def test_no_coaching_all_conditions_false(self):
        inp = make_input(total_competitive_deals=10,
                         competitive_intel_documented_count=5,
                         proof_of_concept_win_rate_pct=0.50)
        assert self.eng._requires_competitive_coaching(10.0, inp) is False


# ===========================================================================
# 12. ESTIMATED REVENUE AT RISK
# ===========================================================================

class TestEstimatedRevenueAtRisk:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_basic_calculation(self):
        inp = make_input(competitive_losses=5, avg_deal_size_lost_usd=10000.0)
        rev = self.eng._estimated_revenue_at_risk(inp, 50.0)
        assert rev == round(5 * 10000.0 * (50.0 / 100.0), 2)
        assert rev == 25000.0

    def test_zero_losses(self):
        inp = make_input(competitive_losses=0, avg_deal_size_lost_usd=10000.0)
        rev = self.eng._estimated_revenue_at_risk(inp, 50.0)
        assert rev == 0.0

    def test_zero_composite(self):
        inp = make_input(competitive_losses=5, avg_deal_size_lost_usd=10000.0)
        rev = self.eng._estimated_revenue_at_risk(inp, 0.0)
        assert rev == 0.0

    def test_100_composite(self):
        inp = make_input(competitive_losses=5, avg_deal_size_lost_usd=10000.0)
        rev = self.eng._estimated_revenue_at_risk(inp, 100.0)
        assert rev == 50000.0

    def test_returns_rounded_to_2_decimals(self):
        inp = make_input(competitive_losses=3, avg_deal_size_lost_usd=7777.77)
        rev = self.eng._estimated_revenue_at_risk(inp, 33.33)
        expected = round(3 * 7777.77 * 0.3333, 2)
        assert rev == expected

    def test_large_values(self):
        inp = make_input(competitive_losses=100, avg_deal_size_lost_usd=500000.0)
        rev = self.eng._estimated_revenue_at_risk(inp, 80.0)
        assert rev == round(100 * 500000.0 * 0.80, 2)


# ===========================================================================
# 13. SIGNAL STRING
# ===========================================================================

class TestSignal:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_benchmark_path_pattern_none_composite_below_20(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=8)
        s = self.eng._signal(inp, CompetitivePattern.none, 15.0)
        assert s == "Competitive win rates strong across all deal segments"

    def test_benchmark_path_exactly_composite_0(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=8)
        s = self.eng._signal(inp, CompetitivePattern.none, 0.0)
        assert s == "Competitive win rates strong across all deal segments"

    def test_benchmark_path_exactly_composite_19(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=8)
        s = self.eng._signal(inp, CompetitivePattern.none, 19.0)
        assert s == "Competitive win rates strong across all deal segments"

    def test_not_benchmark_when_composite_ge_20_even_if_none(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=8,
                         competitive_losses=0, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.none, 20.0)
        assert s != "Competitive win rates strong across all deal segments"

    def test_win_rate_part_below_50_pct(self):
        # wins=4/10=0.40 < 0.50 → include win rate
        inp = make_input(total_competitive_deals=10, competitive_wins=4,
                         competitive_losses=0, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.none, 25.0)
        assert "40% win rate" in s

    def test_win_rate_part_exactly_50_pct_not_included(self):
        # wins=5/10=0.50 NOT < 0.50 → not included
        inp = make_input(total_competitive_deals=10, competitive_wins=5,
                         competitive_losses=0, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.none, 25.0)
        assert "win rate" not in s

    def test_losses_part_included_when_ge_1(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=5,
                         competitive_losses=3, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.none, 25.0)
        assert "3 competitive losses" in s

    def test_losses_part_not_included_when_0(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=5,
                         competitive_losses=0, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.none, 25.0)
        assert "competitive losses" not in s

    def test_displaced_part_included_when_ge_1(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=5,
                         competitive_losses=0, deals_displaced_by_competitor=2)
        s = self.eng._signal(inp, CompetitivePattern.none, 25.0)
        assert "2 displaced by competitor" in s

    def test_displaced_part_not_included_when_0(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=5,
                         competitive_losses=0, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.none, 25.0)
        assert "displaced by competitor" not in s

    def test_fallback_message_when_no_parts(self):
        # wins=5/10=0.50 (not < 0.50); losses=0; displaced=0
        inp = make_input(total_competitive_deals=10, competitive_wins=5,
                         competitive_losses=0, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.none, 25.0)
        assert "competitive performance degrading" in s

    def test_label_for_pattern_none_is_competitive_risk(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=3,
                         competitive_losses=2, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.none, 25.0)
        assert s.startswith("Competitive risk")

    def test_label_for_high_loss_rate_pattern(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=3,
                         competitive_losses=5, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.high_loss_rate, 40.0)
        assert s.startswith("High loss rate")

    def test_label_for_no_competitive_intel_pattern(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=3,
                         competitive_losses=2, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.no_competitive_intel, 35.0)
        assert s.startswith("No competitive intel")

    def test_label_for_price_driven_loss_pattern(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=3,
                         competitive_losses=2, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.price_driven_loss, 35.0)
        assert s.startswith("Price driven loss")

    def test_label_for_feature_gap_loss_pattern(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=3,
                         competitive_losses=2, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.feature_gap_loss, 35.0)
        assert s.startswith("Feature gap loss")

    def test_label_for_icp_mismatch_pattern(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=3,
                         competitive_losses=2, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.icp_mismatch, 35.0)
        assert s.startswith("Icp mismatch")

    def test_composite_value_in_signal(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=3,
                         competitive_losses=2, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.none, 45.0)
        assert "composite 45" in s

    def test_signal_format_double_dash_separator(self):
        inp = make_input(total_competitive_deals=10, competitive_wins=3,
                         competitive_losses=2, deals_displaced_by_competitor=0)
        s = self.eng._signal(inp, CompetitivePattern.none, 45.0)
        assert " — " in s


# ===========================================================================
# 14. ASSESS
# ===========================================================================

class TestAssess:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_returns_competitive_win_loss_result(self, good_input):
        result = self.eng.assess(good_input)
        assert isinstance(result, CompetitiveWinLossResult)

    def test_rep_id_preserved(self):
        inp = make_input(rep_id="test_rep_123")
        result = self.eng.assess(inp)
        assert result.rep_id == "test_rep_123"

    def test_region_preserved(self):
        inp = make_input(region="northeast")
        result = self.eng.assess(inp)
        assert result.region == "northeast"

    def test_composite_is_weighted_average(self):
        inp = make_input(
            total_competitive_deals=10, competitive_wins=7, competitive_losses=2,
            win_rate_vs_top_competitor_pct=0.60,
            competitive_intel_documented_count=8, battle_card_used_count=5,
            proof_of_concept_win_rate_pct=0.70,
            deals_lost_on_price_competitive=1, deals_lost_on_features_competitive=1,
            single_stakeholder_competitive_losses=0,
            competitive_displacement_wins=2, deals_displaced_by_competitor=1,
            multi_stakeholder_competitive_wins=5,
        )
        r = self.eng.assess(inp)
        expected = round(
            r.win_rate_score * 0.35
            + r.competitive_intel_score * 0.25
            + r.deal_quality_score * 0.20
            + r.competitive_resilience_score * 0.20,
            1
        )
        assert r.competitive_effectiveness_composite == expected

    def test_composite_capped_at_100(self, bad_input):
        result = self.eng.assess(bad_input)
        assert result.competitive_effectiveness_composite <= 100.0

    def test_good_rep_low_risk(self, good_input):
        result = self.eng.assess(good_input)
        assert result.competitive_risk == CompetitiveRisk.low

    def test_good_rep_dominant_severity(self, good_input):
        result = self.eng.assess(good_input)
        assert result.competitive_severity == CompetitiveSeverity.dominant

    def test_bad_rep_high_or_critical_risk(self, bad_input):
        result = self.eng.assess(bad_input)
        assert result.competitive_risk in (CompetitiveRisk.high, CompetitiveRisk.critical)

    def test_result_appended_to_internal_list(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        inp = make_input()
        eng.assess(inp)
        assert len(eng._results) == 1

    def test_multiple_results_appended(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        for i in range(5):
            eng.assess(make_input(rep_id=f"rep{i}"))
        assert len(eng._results) == 5

    def test_to_dict_has_15_keys(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_keys(self):
        result = self.eng.assess(make_input())
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "competitive_risk", "competitive_pattern",
            "competitive_severity", "recommended_action", "win_rate_score",
            "competitive_intel_score", "deal_quality_score",
            "competitive_resilience_score", "competitive_effectiveness_composite",
            "is_competitive_threat", "requires_competitive_coaching",
            "estimated_revenue_at_risk_usd", "competitive_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_risk_value_is_string(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["competitive_risk"], str)

    def test_to_dict_pattern_value_is_string(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["competitive_pattern"], str)

    def test_to_dict_severity_value_is_string(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["competitive_severity"], str)

    def test_to_dict_action_value_is_string(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_is_competitive_threat_bool(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["is_competitive_threat"], bool)

    def test_to_dict_requires_coaching_bool(self):
        d = self.eng.assess(make_input()).to_dict()
        assert isinstance(d["requires_competitive_coaching"], bool)

    def test_win_rate_score_in_result_rounded_to_1(self):
        result = self.eng.assess(make_input())
        # Should be rounded to 1 decimal
        assert result.win_rate_score == round(result.win_rate_score, 1)

    def test_all_scores_between_0_and_100(self):
        result = self.eng.assess(make_input())
        for score in [
            result.win_rate_score, result.competitive_intel_score,
            result.deal_quality_score, result.competitive_resilience_score,
            result.competitive_effectiveness_composite
        ]:
            assert 0 <= score <= 100


# ===========================================================================
# 15. ASSESS_BATCH
# ===========================================================================

class TestAssessBatch:
    def setup_method(self):
        self.eng = SalesCompetitiveWinLossIntelligenceEngine()

    def test_returns_list(self):
        results = self.eng.assess_batch([make_input(), make_input(rep_id="rep2")])
        assert isinstance(results, list)

    def test_batch_empty_list(self):
        results = self.eng.assess_batch([])
        assert results == []

    def test_batch_single_item(self):
        results = self.eng.assess_batch([make_input(rep_id="solo")])
        assert len(results) == 1
        assert results[0].rep_id == "solo"

    def test_batch_three_items(self):
        inputs = [make_input(rep_id=f"rep{i}") for i in range(3)]
        results = self.eng.assess_batch(inputs)
        assert len(results) == 3

    def test_batch_all_appended_to_results(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        inputs = [make_input(rep_id=f"rep{i}") for i in range(5)]
        eng.assess_batch(inputs)
        assert len(eng._results) == 5

    def test_batch_preserves_order(self):
        inputs = [make_input(rep_id=f"rep{i}") for i in range(4)]
        results = self.eng.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.rep_id == f"rep{i}"

    def test_batch_all_return_correct_type(self):
        inputs = [make_input(rep_id=f"rep{i}") for i in range(3)]
        results = self.eng.assess_batch(inputs)
        for r in results:
            assert isinstance(r, CompetitiveWinLossResult)


# ===========================================================================
# 16. SUMMARY
# ===========================================================================

class TestSummary:
    def test_empty_summary_has_13_keys(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        s = eng.summary()
        assert len(s) == 13

    def test_empty_summary_keys(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        s = eng.summary()
        expected_keys = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_competitive_effectiveness_composite",
            "competitive_threat_count", "competitive_coaching_count",
            "avg_win_rate_score", "avg_competitive_intel_score",
            "avg_deal_quality_score", "avg_competitive_resilience_score",
            "total_estimated_revenue_at_risk_usd",
        }
        assert set(s.keys()) == expected_keys

    def test_empty_summary_total_is_0(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        assert eng.summary()["total"] == 0

    def test_empty_summary_counts_are_empty_dicts(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        s = eng.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_averages_are_0(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        s = eng.summary()
        assert s["avg_competitive_effectiveness_composite"] == 0.0
        assert s["avg_win_rate_score"] == 0.0
        assert s["avg_competitive_intel_score"] == 0.0
        assert s["avg_deal_quality_score"] == 0.0
        assert s["avg_competitive_resilience_score"] == 0.0

    def test_empty_summary_threat_coaching_counts_are_0(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        s = eng.summary()
        assert s["competitive_threat_count"] == 0
        assert s["competitive_coaching_count"] == 0

    def test_empty_summary_revenue_is_0(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        assert eng.summary()["total_estimated_revenue_at_risk_usd"] == 0.0

    def test_summary_total_after_one_assess(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        eng.assess(make_input())
        assert eng.summary()["total"] == 1

    def test_summary_total_after_batch(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        eng.assess_batch([make_input(rep_id=f"r{i}") for i in range(5)])
        assert eng.summary()["total"] == 5

    def test_summary_13_keys_after_data(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        eng.assess(make_input())
        assert len(eng.summary()) == 13

    def test_summary_risk_counts_populated(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r = eng.assess(make_input())
        s = eng.summary()
        assert r.competitive_risk.value in s["risk_counts"]
        assert s["risk_counts"][r.competitive_risk.value] == 1

    def test_summary_pattern_counts_populated(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r = eng.assess(make_input())
        s = eng.summary()
        assert r.competitive_pattern.value in s["pattern_counts"]

    def test_summary_severity_counts_populated(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r = eng.assess(make_input())
        s = eng.summary()
        assert r.competitive_severity.value in s["severity_counts"]

    def test_summary_action_counts_populated(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r = eng.assess(make_input())
        s = eng.summary()
        assert r.recommended_action.value in s["action_counts"]

    def test_summary_avg_composite_correct(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r1 = eng.assess(make_input(rep_id="r1"))
        r2 = eng.assess(make_input(rep_id="r2"))
        s = eng.summary()
        expected = round((r1.competitive_effectiveness_composite + r2.competitive_effectiveness_composite) / 2, 1)
        assert s["avg_competitive_effectiveness_composite"] == expected

    def test_summary_avg_win_rate_score_correct(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r1 = eng.assess(make_input(rep_id="r1"))
        r2 = eng.assess(make_input(rep_id="r2"))
        s = eng.summary()
        expected = round((r1.win_rate_score + r2.win_rate_score) / 2, 1)
        assert s["avg_win_rate_score"] == expected

    def test_summary_avg_intel_score_correct(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r1 = eng.assess(make_input(rep_id="r1"))
        r2 = eng.assess(make_input(rep_id="r2"))
        s = eng.summary()
        expected = round((r1.competitive_intel_score + r2.competitive_intel_score) / 2, 1)
        assert s["avg_competitive_intel_score"] == expected

    def test_summary_avg_deal_quality_score_correct(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r1 = eng.assess(make_input(rep_id="r1"))
        r2 = eng.assess(make_input(rep_id="r2"))
        s = eng.summary()
        expected = round((r1.deal_quality_score + r2.deal_quality_score) / 2, 1)
        assert s["avg_deal_quality_score"] == expected

    def test_summary_avg_resilience_score_correct(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r1 = eng.assess(make_input(rep_id="r1"))
        r2 = eng.assess(make_input(rep_id="r2"))
        s = eng.summary()
        expected = round((r1.competitive_resilience_score + r2.competitive_resilience_score) / 2, 1)
        assert s["avg_competitive_resilience_score"] == expected

    def test_summary_threat_count_correct(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        # threat rep: win_rate < 0.25
        eng.assess(make_input(rep_id="threat", total_competitive_deals=10, competitive_wins=2,
                               deals_displaced_by_competitor=0, competitive_displacement_wins=0))
        # safe rep
        eng.assess(make_input(rep_id="safe", total_competitive_deals=10, competitive_wins=8,
                               deals_displaced_by_competitor=0, competitive_displacement_wins=0))
        s = eng.summary()
        # at least 1 threat
        assert s["competitive_threat_count"] >= 1

    def test_summary_coaching_count_correct(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        # coaching needed: poc < 0.30
        r1 = eng.assess(make_input(rep_id="r1", proof_of_concept_win_rate_pct=0.10,
                                    competitive_intel_documented_count=5,
                                    total_competitive_deals=10))
        # no coaching needed
        r2 = eng.assess(make_input(rep_id="r2", proof_of_concept_win_rate_pct=0.80,
                                    competitive_intel_documented_count=5,
                                    total_competitive_deals=10))
        s = eng.summary()
        expected = sum([r1.requires_competitive_coaching, r2.requires_competitive_coaching])
        assert s["competitive_coaching_count"] == expected

    def test_summary_total_revenue_correct(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r1 = eng.assess(make_input(rep_id="r1"))
        r2 = eng.assess(make_input(rep_id="r2"))
        s = eng.summary()
        expected = round(r1.estimated_revenue_at_risk_usd + r2.estimated_revenue_at_risk_usd, 2)
        assert s["total_estimated_revenue_at_risk_usd"] == expected

    def test_summary_multiple_risks_counted(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        # force low risk
        eng.assess(make_input(rep_id="r1",
                               total_competitive_deals=10, competitive_wins=8, competitive_losses=1,
                               win_rate_vs_top_competitor_pct=0.60,
                               competitive_intel_documented_count=8, battle_card_used_count=8,
                               proof_of_concept_win_rate_pct=0.80,
                               deals_lost_on_price_competitive=0, deals_lost_on_features_competitive=0,
                               single_stakeholder_competitive_losses=0,
                               competitive_displacement_wins=1, deals_displaced_by_competitor=0,
                               multi_stakeholder_competitive_wins=7))
        # force critical risk
        eng.assess(make_input(rep_id="r2",
                               total_competitive_deals=10, competitive_wins=1, competitive_losses=8,
                               win_rate_vs_top_competitor_pct=0.10,
                               competitive_intel_documented_count=1, battle_card_used_count=1,
                               proof_of_concept_win_rate_pct=0.10,
                               deals_lost_on_price_competitive=5, deals_lost_on_features_competitive=4,
                               single_stakeholder_competitive_losses=6,
                               competitive_displacement_wins=0, deals_displaced_by_competitor=5,
                               multi_stakeholder_competitive_wins=0))
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == 2


# ===========================================================================
# 17. INTEGRATION / END-TO-END
# ===========================================================================

class TestIntegration:
    def test_full_workflow_dominant_rep(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        inp = make_input(
            rep_id="top_rep", region="west",
            total_competitive_deals=20, competitive_wins=17, competitive_losses=2,
            competitive_ties=1, deals_lost_on_price_competitive=1,
            deals_lost_on_features_competitive=0, deals_lost_on_relationship_competitive=1,
            win_rate_vs_top_competitor_pct=0.75,
            competitive_intel_documented_count=18, battle_card_used_count=16,
            proof_of_concept_win_rate_pct=0.85,
            multi_stakeholder_competitive_wins=14, single_stakeholder_competitive_losses=1,
            competitive_displacement_wins=5, deals_displaced_by_competitor=1,
        )
        r = eng.assess(inp)
        assert r.competitive_risk == CompetitiveRisk.low
        assert r.competitive_severity == CompetitiveSeverity.dominant
        assert r.recommended_action == CompetitiveAction.no_action
        assert r.is_competitive_threat is False
        assert r.competitive_signal == "Competitive win rates strong across all deal segments"

    def test_full_workflow_struggling_rep(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        inp = make_input(
            rep_id="struggling", region="east",
            total_competitive_deals=10, competitive_wins=1, competitive_losses=8,
            competitive_ties=1, deals_lost_on_price_competitive=5,
            deals_lost_on_features_competitive=4, deals_lost_on_relationship_competitive=2,
            win_rate_vs_top_competitor_pct=0.05,
            competitive_intel_documented_count=1, battle_card_used_count=1,
            proof_of_concept_win_rate_pct=0.10,
            multi_stakeholder_competitive_wins=0, single_stakeholder_competitive_losses=6,
            competitive_displacement_wins=0, deals_displaced_by_competitor=5,
            avg_deal_size_lost_usd=15000.0,
        )
        r = eng.assess(inp)
        assert r.competitive_risk in (CompetitiveRisk.high, CompetitiveRisk.critical)
        assert r.is_competitive_threat is True
        assert r.requires_competitive_coaching is True
        assert r.estimated_revenue_at_risk_usd > 0

    def test_assess_and_summary_consistent(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        inputs = [
            make_input(rep_id=f"rep{i}", total_competitive_deals=10,
                       competitive_wins=i % 10 + 1) for i in range(5)
        ]
        results = eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == 5
        assert sum(s["risk_counts"].values()) == 5
        assert sum(s["pattern_counts"].values()) == 5
        assert sum(s["severity_counts"].values()) == 5
        assert sum(s["action_counts"].values()) == 5

    def test_new_engine_has_empty_results(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        assert eng._results == []

    def test_separate_engine_instances_independent(self):
        eng1 = SalesCompetitiveWinLossIntelligenceEngine()
        eng2 = SalesCompetitiveWinLossIntelligenceEngine()
        eng1.assess(make_input(rep_id="r1"))
        assert len(eng1._results) == 1
        assert len(eng2._results) == 0

    def test_to_dict_risk_matches_enum(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r = eng.assess(make_input())
        d = r.to_dict()
        assert d["competitive_risk"] == r.competitive_risk.value

    def test_to_dict_pattern_matches_enum(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r = eng.assess(make_input())
        d = r.to_dict()
        assert d["competitive_pattern"] == r.competitive_pattern.value

    def test_to_dict_severity_matches_enum(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r = eng.assess(make_input())
        d = r.to_dict()
        assert d["competitive_severity"] == r.competitive_severity.value

    def test_to_dict_action_matches_enum(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        r = eng.assess(make_input())
        d = r.to_dict()
        assert d["recommended_action"] == r.recommended_action.value

    def test_estimated_revenue_consistent_with_subscores(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        inp = make_input(competitive_losses=4, avg_deal_size_lost_usd=12500.0)
        r = eng.assess(inp)
        expected = round(4 * 12500.0 * (r.competitive_effectiveness_composite / 100.0), 2)
        assert r.estimated_revenue_at_risk_usd == expected

    def test_risk_severity_alignment(self):
        """risk and severity should always map to the same composite bucket."""
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        for inp in [
            make_input(rep_id="a"),
            make_input(rep_id="b", total_competitive_deals=10, competitive_wins=1,
                       competitive_losses=8, win_rate_vs_top_competitor_pct=0.10,
                       competitive_intel_documented_count=1, battle_card_used_count=1,
                       proof_of_concept_win_rate_pct=0.10, deals_lost_on_price_competitive=5,
                       deals_lost_on_features_competitive=4, single_stakeholder_competitive_losses=6,
                       competitive_displacement_wins=0, deals_displaced_by_competitor=5,
                       multi_stakeholder_competitive_wins=0),
        ]:
            r = eng.assess(inp)
            c = r.competitive_effectiveness_composite
            if c >= 60:
                assert r.competitive_risk == CompetitiveRisk.critical
                assert r.competitive_severity == CompetitiveSeverity.losing
            elif c >= 40:
                assert r.competitive_risk == CompetitiveRisk.high
                assert r.competitive_severity == CompetitiveSeverity.challenged
            elif c >= 20:
                assert r.competitive_risk == CompetitiveRisk.moderate
                assert r.competitive_severity == CompetitiveSeverity.competitive
            else:
                assert r.competitive_risk == CompetitiveRisk.low
                assert r.competitive_severity == CompetitiveSeverity.dominant

    def test_batch_then_summary_revenue(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        inputs = [make_input(rep_id=f"r{i}", competitive_losses=i+1,
                              avg_deal_size_lost_usd=1000.0) for i in range(3)]
        results = eng.assess_batch(inputs)
        s = eng.summary()
        total = sum(r.estimated_revenue_at_risk_usd for r in results)
        assert s["total_estimated_revenue_at_risk_usd"] == round(total, 2)

    def test_coaching_count_in_summary_matches_results(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = eng.assess_batch(inputs)
        s = eng.summary()
        expected = sum(1 for r in results if r.requires_competitive_coaching)
        assert s["competitive_coaching_count"] == expected

    def test_threat_count_in_summary_matches_results(self):
        eng = SalesCompetitiveWinLossIntelligenceEngine()
        inputs = [make_input(rep_id=f"r{i}") for i in range(5)]
        results = eng.assess_batch(inputs)
        s = eng.summary()
        expected = sum(1 for r in results if r.is_competitive_threat)
        assert s["competitive_threat_count"] == expected
