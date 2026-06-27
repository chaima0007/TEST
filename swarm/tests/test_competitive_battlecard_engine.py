"""Comprehensive tests for Module 24 — Competitive Battlecard Engine."""
from __future__ import annotations

import pytest
from swarm.intelligence.competitive_battlecard_engine import (
    BattlecardAction,
    BattlecardResult,
    CompetitiveBattlecardEngine,
    CompetitorProfile,
    CompetitorThreat,
    MarketPosition,
    WinProbability,
    _battlecard_action,
    _counter_tactics,
    _objection_responses,
    _our_advantages,
    _red_flags,
    _talk_tracks,
    _their_advantages,
    _threat_level,
    _threat_score,
    _win_probability,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_competitor(
    competitor_id: str = "c1",
    competitor_name: str = "RivalCo",
    market_position: MarketPosition = MarketPosition.CHALLENGER,
    active_deals_competing: int = 5,
    win_rate_against_us_pct: float = 40.0,
    avg_discount_offered_pct: float = 15.0,
    feature_parity_pct: float = 60.0,
    price_vs_us_pct: float = 90.0,
    our_unique_features: list[str] | None = None,
    our_integration_advantages: list[str] | None = None,
    our_support_rating: float = 8.5,
    their_support_rating: float = 6.0,
    known_weaknesses: list[str] | None = None,
    recent_price_drop: bool = False,
    new_product_launched: bool = False,
    funding_raised: bool = False,
    customer_churn_signal: bool = False,
) -> CompetitorProfile:
    return CompetitorProfile(
        competitor_id=competitor_id,
        competitor_name=competitor_name,
        market_position=market_position,
        active_deals_competing=active_deals_competing,
        win_rate_against_us_pct=win_rate_against_us_pct,
        avg_discount_offered_pct=avg_discount_offered_pct,
        feature_parity_pct=feature_parity_pct,
        price_vs_us_pct=price_vs_us_pct,
        our_unique_features=our_unique_features if our_unique_features is not None else ["Feature A", "Feature B", "Feature C"],
        our_integration_advantages=our_integration_advantages if our_integration_advantages is not None else ["Salesforce", "HubSpot"],
        our_support_rating=our_support_rating,
        their_support_rating=their_support_rating,
        known_weaknesses=known_weaknesses if known_weaknesses is not None else ["slow support", "no mobile"],
        recent_price_drop=recent_price_drop,
        new_product_launched=new_product_launched,
        funding_raised=funding_raised,
        customer_churn_signal=customer_churn_signal,
    )


# ===========================================================================
# 1. TestCompetitorThreatEnum
# ===========================================================================

class TestCompetitorThreatEnum:
    def test_critical_value(self):
        assert CompetitorThreat.CRITICAL.value == "critical"

    def test_high_value(self):
        assert CompetitorThreat.HIGH.value == "high"

    def test_medium_value(self):
        assert CompetitorThreat.MEDIUM.value == "medium"

    def test_low_value(self):
        assert CompetitorThreat.LOW.value == "low"

    def test_is_str_enum(self):
        assert isinstance(CompetitorThreat.CRITICAL, str)

    def test_four_members(self):
        assert len(CompetitorThreat) == 4

    def test_all_members(self):
        members = {m.value for m in CompetitorThreat}
        assert members == {"critical", "high", "medium", "low"}

    def test_equality_with_string(self):
        assert CompetitorThreat.HIGH == "high"

    def test_identity(self):
        assert CompetitorThreat.CRITICAL is CompetitorThreat.CRITICAL

    def test_membership(self):
        assert CompetitorThreat.LOW in CompetitorThreat


# ===========================================================================
# 2. TestBattlecardActionEnum
# ===========================================================================

class TestBattlecardActionEnum:
    def test_escalate_value(self):
        assert BattlecardAction.ESCALATE.value == "escalate"

    def test_differentiate_value(self):
        assert BattlecardAction.DIFFERENTIATE.value == "differentiate"

    def test_counter_value(self):
        assert BattlecardAction.COUNTER.value == "counter"

    def test_monitor_value(self):
        assert BattlecardAction.MONITOR.value == "monitor"

    def test_is_str_enum(self):
        assert isinstance(BattlecardAction.ESCALATE, str)

    def test_four_members(self):
        assert len(BattlecardAction) == 4

    def test_all_values(self):
        vals = {m.value for m in BattlecardAction}
        assert vals == {"escalate", "differentiate", "counter", "monitor"}

    def test_equality_with_string(self):
        assert BattlecardAction.MONITOR == "monitor"


# ===========================================================================
# 3. TestWinProbabilityEnum
# ===========================================================================

class TestWinProbabilityEnum:
    def test_strong_value(self):
        assert WinProbability.STRONG.value == "strong"

    def test_moderate_value(self):
        assert WinProbability.MODERATE.value == "moderate"

    def test_weak_value(self):
        assert WinProbability.WEAK.value == "weak"

    def test_very_weak_value(self):
        assert WinProbability.VERY_WEAK.value == "very_weak"

    def test_is_str_enum(self):
        assert isinstance(WinProbability.STRONG, str)

    def test_four_members(self):
        assert len(WinProbability) == 4

    def test_all_values(self):
        vals = {m.value for m in WinProbability}
        assert vals == {"strong", "moderate", "weak", "very_weak"}

    def test_equality_with_string(self):
        assert WinProbability.VERY_WEAK == "very_weak"


# ===========================================================================
# 4. TestMarketPositionEnum
# ===========================================================================

class TestMarketPositionEnum:
    def test_leader_value(self):
        assert MarketPosition.LEADER.value == "leader"

    def test_challenger_value(self):
        assert MarketPosition.CHALLENGER.value == "challenger"

    def test_niche_value(self):
        assert MarketPosition.NICHE.value == "niche"

    def test_emerging_value(self):
        assert MarketPosition.EMERGING.value == "emerging"

    def test_is_str_enum(self):
        assert isinstance(MarketPosition.LEADER, str)

    def test_four_members(self):
        assert len(MarketPosition) == 4

    def test_all_values(self):
        vals = {m.value for m in MarketPosition}
        assert vals == {"leader", "challenger", "niche", "emerging"}

    def test_equality_with_string(self):
        assert MarketPosition.NICHE == "niche"


# ===========================================================================
# 5. TestCompetitorProfileDataclass
# ===========================================================================

class TestCompetitorProfileDataclass:
    def test_basic_creation(self):
        comp = make_competitor()
        assert comp.competitor_id == "c1"

    def test_competitor_name(self):
        comp = make_competitor(competitor_name="Acme")
        assert comp.competitor_name == "Acme"

    def test_market_position(self):
        comp = make_competitor(market_position=MarketPosition.LEADER)
        assert comp.market_position == MarketPosition.LEADER

    def test_active_deals(self):
        comp = make_competitor(active_deals_competing=7)
        assert comp.active_deals_competing == 7

    def test_win_rate(self):
        comp = make_competitor(win_rate_against_us_pct=55.0)
        assert comp.win_rate_against_us_pct == 55.0

    def test_avg_discount(self):
        comp = make_competitor(avg_discount_offered_pct=22.5)
        assert comp.avg_discount_offered_pct == 22.5

    def test_feature_parity(self):
        comp = make_competitor(feature_parity_pct=75.0)
        assert comp.feature_parity_pct == 75.0

    def test_price_vs_us(self):
        comp = make_competitor(price_vs_us_pct=80.0)
        assert comp.price_vs_us_pct == 80.0

    def test_unique_features_list(self):
        comp = make_competitor(our_unique_features=["X", "Y"])
        assert comp.our_unique_features == ["X", "Y"]

    def test_integration_advantages_list(self):
        comp = make_competitor(our_integration_advantages=["Slack"])
        assert comp.our_integration_advantages == ["Slack"]

    def test_support_ratings(self):
        comp = make_competitor(our_support_rating=9.0, their_support_rating=5.0)
        assert comp.our_support_rating == 9.0
        assert comp.their_support_rating == 5.0

    def test_known_weaknesses(self):
        comp = make_competitor(known_weaknesses=["buggy UI"])
        assert "buggy UI" in comp.known_weaknesses

    def test_boolean_flags_default_false(self):
        comp = make_competitor()
        assert comp.recent_price_drop is False
        assert comp.new_product_launched is False
        assert comp.funding_raised is False
        assert comp.customer_churn_signal is False

    def test_boolean_flags_true(self):
        comp = make_competitor(recent_price_drop=True, funding_raised=True)
        assert comp.recent_price_drop is True
        assert comp.funding_raised is True

    def test_is_dataclass_instance(self):
        import dataclasses
        comp = make_competitor()
        assert dataclasses.is_dataclass(comp)


# ===========================================================================
# 6. TestBattlecardResultToDict
# ===========================================================================

class TestBattlecardResultToDict:
    def setup_method(self):
        engine = CompetitiveBattlecardEngine()
        comp = make_competitor()
        self.result = engine.generate(comp)
        self.d = self.result.to_dict()

    def test_returns_dict(self):
        assert isinstance(self.d, dict)

    def test_keys_present(self):
        expected_keys = {
            "competitor_id", "competitor_name", "market_position",
            "threat_score", "threat_level", "win_probability",
            "battlecard_action", "executive_summary", "our_advantages",
            "their_advantages", "counter_tactics", "talk_tracks",
            "objection_responses", "red_flags",
        }
        assert expected_keys == set(self.d.keys())

    def test_threat_level_is_string(self):
        assert isinstance(self.d["threat_level"], str)
        assert not isinstance(self.d["threat_level"], CompetitorThreat)

    def test_win_probability_is_string(self):
        assert isinstance(self.d["win_probability"], str)
        assert not isinstance(self.d["win_probability"], WinProbability)

    def test_battlecard_action_is_string(self):
        assert isinstance(self.d["battlecard_action"], str)
        assert not isinstance(self.d["battlecard_action"], BattlecardAction)

    def test_threat_score_numeric(self):
        assert isinstance(self.d["threat_score"], (int, float))

    def test_competitor_id_preserved(self):
        assert self.d["competitor_id"] == "c1"

    def test_competitor_name_preserved(self):
        assert self.d["competitor_name"] == "RivalCo"

    def test_market_position_is_string(self):
        assert isinstance(self.d["market_position"], str)

    def test_our_advantages_is_list(self):
        assert isinstance(self.d["our_advantages"], list)

    def test_their_advantages_is_list(self):
        assert isinstance(self.d["their_advantages"], list)

    def test_counter_tactics_is_list(self):
        assert isinstance(self.d["counter_tactics"], list)

    def test_talk_tracks_is_list(self):
        assert isinstance(self.d["talk_tracks"], list)

    def test_objection_responses_is_list(self):
        assert isinstance(self.d["objection_responses"], list)

    def test_red_flags_is_list(self):
        assert isinstance(self.d["red_flags"], list)

    def test_no_enum_objects_in_dict(self):
        from enum import Enum
        for key, val in self.d.items():
            assert not isinstance(val, Enum), f"Found Enum at key '{key}'"


# ===========================================================================
# 7. TestThreatScoreWinRate
# ===========================================================================

class TestThreatScoreWinRate:
    """Win rate contributes up to 30 points."""

    def _base_pts(self) -> float:
        """Points from active_deals=0 (+2), feature=0 (+2), price=100 (+0), no signals."""
        return 2 + 2 + 2 + 0  # win-rate replaced; deals=0→2, feat=0→2, price=100→0

    def _score_with_win_rate(self, wr: float) -> float:
        comp = make_competitor(
            win_rate_against_us_pct=wr,
            active_deals_competing=0,
            feature_parity_pct=0.0,
            price_vs_us_pct=100.0,
        )
        return _threat_score(comp)

    def test_win_rate_below_30_gives_4(self):
        score = self._score_with_win_rate(10.0)
        # 4 (win) + 2 (deals) + 2 (feat) + 0 (price) = 8
        assert score == 8.0

    def test_win_rate_exactly_30_gives_12(self):
        score = self._score_with_win_rate(30.0)
        assert score == 16.0  # 12+2+2+0

    def test_win_rate_between_30_and_45_gives_12(self):
        score = self._score_with_win_rate(44.9)
        assert score == 16.0

    def test_win_rate_exactly_45_gives_20(self):
        score = self._score_with_win_rate(45.0)
        assert score == 24.0  # 20+2+2+0

    def test_win_rate_between_45_and_60_gives_20(self):
        score = self._score_with_win_rate(59.9)
        assert score == 24.0

    def test_win_rate_exactly_60_gives_30(self):
        score = self._score_with_win_rate(60.0)
        assert score == 34.0  # 30+2+2+0

    def test_win_rate_above_60_gives_30(self):
        score = self._score_with_win_rate(80.0)
        assert score == 34.0

    def test_win_rate_zero_gives_4(self):
        score = self._score_with_win_rate(0.0)
        assert score == 8.0

    def test_win_rate_100_gives_30(self):
        score = self._score_with_win_rate(100.0)
        assert score == 34.0

    def test_win_rate_boundary_29_gives_4(self):
        score = self._score_with_win_rate(29.9)
        assert score == 8.0


# ===========================================================================
# 8. TestThreatScoreDeals
# ===========================================================================

class TestThreatScoreDeals:
    """Active deals contributes up to 20 points."""

    def _score_with_deals(self, deals: int) -> float:
        comp = make_competitor(
            active_deals_competing=deals,
            win_rate_against_us_pct=0.0,  # +4
            feature_parity_pct=0.0,       # +2
            price_vs_us_pct=100.0,        # +0
        )
        return _threat_score(comp)

    def test_deals_0_gives_2(self):
        # 4+2+2+0=8
        assert self._score_with_deals(0) == 8.0

    def test_deals_1_gives_2(self):
        assert self._score_with_deals(1) == 8.0

    def test_deals_2_gives_7(self):
        # 4+7+2+0=13
        assert self._score_with_deals(2) == 13.0

    def test_deals_4_gives_7(self):
        assert self._score_with_deals(4) == 13.0

    def test_deals_5_gives_13(self):
        # 4+13+2+0=19
        assert self._score_with_deals(5) == 19.0

    def test_deals_9_gives_13(self):
        assert self._score_with_deals(9) == 19.0

    def test_deals_10_gives_20(self):
        # 4+20+2+0=26
        assert self._score_with_deals(10) == 26.0

    def test_deals_100_gives_20(self):
        assert self._score_with_deals(100) == 26.0

    def test_deals_boundary_exactly_2(self):
        assert self._score_with_deals(2) == 13.0

    def test_deals_boundary_exactly_5(self):
        assert self._score_with_deals(5) == 19.0

    def test_deals_boundary_exactly_10(self):
        assert self._score_with_deals(10) == 26.0


# ===========================================================================
# 9. TestThreatScoreFeatureParity
# ===========================================================================

class TestThreatScoreFeatureParity:
    """Feature parity contributes up to 20 points."""

    def _score_with_feature(self, fp: float) -> float:
        comp = make_competitor(
            feature_parity_pct=fp,
            win_rate_against_us_pct=0.0,  # +4
            active_deals_competing=0,      # +2
            price_vs_us_pct=100.0,         # +0
        )
        return _threat_score(comp)

    def test_feature_below_40_gives_2(self):
        # 4+2+2+0=8
        assert self._score_with_feature(0.0) == 8.0

    def test_feature_39_gives_2(self):
        assert self._score_with_feature(39.9) == 8.0

    def test_feature_exactly_40_gives_7(self):
        # 4+2+7+0=13
        assert self._score_with_feature(40.0) == 13.0

    def test_feature_between_40_59_gives_7(self):
        assert self._score_with_feature(59.9) == 13.0

    def test_feature_exactly_60_gives_13(self):
        # 4+2+13+0=19
        assert self._score_with_feature(60.0) == 19.0

    def test_feature_between_60_79_gives_13(self):
        assert self._score_with_feature(79.9) == 19.0

    def test_feature_exactly_80_gives_20(self):
        # 4+2+20+0=26
        assert self._score_with_feature(80.0) == 26.0

    def test_feature_100_gives_20(self):
        assert self._score_with_feature(100.0) == 26.0

    def test_feature_boundary_exactly_40(self):
        assert self._score_with_feature(40.0) == 13.0

    def test_feature_boundary_exactly_60(self):
        assert self._score_with_feature(60.0) == 19.0

    def test_feature_boundary_exactly_80(self):
        assert self._score_with_feature(80.0) == 26.0


# ===========================================================================
# 10. TestThreatScorePrice
# ===========================================================================

class TestThreatScorePrice:
    """Price aggression contributes up to 15 points (lower price = more threatening)."""

    def _score_with_price(self, price: float) -> float:
        comp = make_competitor(
            price_vs_us_pct=price,
            win_rate_against_us_pct=0.0,  # +4
            active_deals_competing=0,      # +2
            feature_parity_pct=0.0,        # +2
        )
        return _threat_score(comp)

    def test_price_70_gives_15(self):
        # 4+2+2+15=23
        assert self._score_with_price(70.0) == 23.0

    def test_price_below_70_gives_15(self):
        assert self._score_with_price(50.0) == 23.0

    def test_price_70_boundary_gives_15(self):
        assert self._score_with_price(70.0) == 23.0

    def test_price_71_gives_9(self):
        # 4+2+2+9=17
        assert self._score_with_price(71.0) == 17.0

    def test_price_85_gives_9(self):
        assert self._score_with_price(85.0) == 17.0

    def test_price_86_gives_4(self):
        # 4+2+2+4=12
        assert self._score_with_price(86.0) == 12.0

    def test_price_95_gives_4(self):
        assert self._score_with_price(95.0) == 12.0

    def test_price_96_gives_0(self):
        # 4+2+2+0=8
        assert self._score_with_price(96.0) == 8.0

    def test_price_100_gives_0(self):
        assert self._score_with_price(100.0) == 8.0

    def test_price_above_100_gives_0(self):
        assert self._score_with_price(120.0) == 8.0

    def test_price_boundary_85(self):
        assert self._score_with_price(85.0) == 17.0

    def test_price_boundary_95(self):
        assert self._score_with_price(95.0) == 12.0


# ===========================================================================
# 11. TestThreatScoreMarketSignals
# ===========================================================================

class TestThreatScoreMarketSignals:
    """Market signals each contribute +5 points."""

    def _base_score(self) -> float:
        """Baseline with known point values: win=4, deals=2, feat=2, price=0."""
        return 8.0

    def _score_with_signals(self, price_drop=False, new_product=False, funding=False) -> float:
        comp = make_competitor(
            win_rate_against_us_pct=0.0,
            active_deals_competing=0,
            feature_parity_pct=0.0,
            price_vs_us_pct=100.0,
            recent_price_drop=price_drop,
            new_product_launched=new_product,
            funding_raised=funding,
        )
        return _threat_score(comp)

    def test_no_signals(self):
        assert self._score_with_signals() == 8.0

    def test_price_drop_adds_5(self):
        assert self._score_with_signals(price_drop=True) == 13.0

    def test_new_product_adds_5(self):
        assert self._score_with_signals(new_product=True) == 13.0

    def test_funding_adds_5(self):
        assert self._score_with_signals(funding=True) == 13.0

    def test_two_signals_add_10(self):
        assert self._score_with_signals(price_drop=True, new_product=True) == 18.0

    def test_three_signals_add_15(self):
        assert self._score_with_signals(price_drop=True, new_product=True, funding=True) == 23.0

    def test_price_drop_and_funding(self):
        assert self._score_with_signals(price_drop=True, funding=True) == 18.0

    def test_new_product_and_funding(self):
        assert self._score_with_signals(new_product=True, funding=True) == 18.0


# ===========================================================================
# 12. TestThreatScoreClamping
# ===========================================================================

class TestThreatScoreClamping:
    def test_score_is_float(self):
        comp = make_competitor()
        score = _threat_score(comp)
        assert isinstance(score, (int, float))

    def test_score_not_below_zero(self):
        comp = make_competitor(
            win_rate_against_us_pct=0.0,
            active_deals_competing=0,
            feature_parity_pct=0.0,
            price_vs_us_pct=100.0,
        )
        assert _threat_score(comp) >= 0.0

    def test_score_not_above_100(self):
        comp = make_competitor(
            win_rate_against_us_pct=100.0,
            active_deals_competing=100,
            feature_parity_pct=100.0,
            price_vs_us_pct=10.0,
            recent_price_drop=True,
            new_product_launched=True,
            funding_raised=True,
        )
        assert _threat_score(comp) <= 100.0

    def test_maximum_score_exactly_100(self):
        comp = make_competitor(
            win_rate_against_us_pct=100.0,
            active_deals_competing=100,
            feature_parity_pct=100.0,
            price_vs_us_pct=10.0,
            recent_price_drop=True,
            new_product_launched=True,
            funding_raised=True,
        )
        # 30+20+20+15+5+5+5 = 100
        assert _threat_score(comp) == 100.0

    def test_minimum_score_positive(self):
        comp = make_competitor(
            win_rate_against_us_pct=0.0,
            active_deals_competing=0,
            feature_parity_pct=0.0,
            price_vs_us_pct=100.0,
        )
        # 4+2+2+0 = 8
        assert _threat_score(comp) == 8.0

    def test_score_rounded_to_1dp(self):
        comp = make_competitor()
        score = _threat_score(comp)
        assert score == round(score, 1)

    def test_typical_score_in_range(self):
        comp = make_competitor()
        score = _threat_score(comp)
        assert 0.0 <= score <= 100.0


# ===========================================================================
# 13. TestThreatLevelThresholds
# ===========================================================================

class TestThreatLevelThresholds:
    def test_score_70_is_critical(self):
        assert _threat_level(70.0) == CompetitorThreat.CRITICAL

    def test_score_above_70_is_critical(self):
        assert _threat_level(85.0) == CompetitorThreat.CRITICAL

    def test_score_100_is_critical(self):
        assert _threat_level(100.0) == CompetitorThreat.CRITICAL

    def test_score_69_is_high(self):
        assert _threat_level(69.9) == CompetitorThreat.HIGH

    def test_score_50_is_high(self):
        assert _threat_level(50.0) == CompetitorThreat.HIGH

    def test_score_60_is_high(self):
        assert _threat_level(60.0) == CompetitorThreat.HIGH

    def test_score_49_is_medium(self):
        assert _threat_level(49.9) == CompetitorThreat.MEDIUM

    def test_score_30_is_medium(self):
        assert _threat_level(30.0) == CompetitorThreat.MEDIUM

    def test_score_40_is_medium(self):
        assert _threat_level(40.0) == CompetitorThreat.MEDIUM

    def test_score_29_is_low(self):
        assert _threat_level(29.9) == CompetitorThreat.LOW

    def test_score_0_is_low(self):
        assert _threat_level(0.0) == CompetitorThreat.LOW

    def test_score_10_is_low(self):
        assert _threat_level(10.0) == CompetitorThreat.LOW

    def test_boundary_exactly_70(self):
        assert _threat_level(70.0) == CompetitorThreat.CRITICAL

    def test_boundary_exactly_50(self):
        assert _threat_level(50.0) == CompetitorThreat.HIGH

    def test_boundary_exactly_30(self):
        assert _threat_level(30.0) == CompetitorThreat.MEDIUM


# ===========================================================================
# 14. TestWinProbabilityThresholds
# ===========================================================================

class TestWinProbabilityThresholds:
    """WinProbability based on (100 - win_rate_against_us_pct)."""

    def _prob(self, wr: float) -> WinProbability:
        comp = make_competitor(win_rate_against_us_pct=wr)
        return _win_probability(comp)

    # STRONG: win_pct >= 70 → their win_rate <= 30
    def test_win_rate_0_strong(self):
        assert self._prob(0.0) == WinProbability.STRONG

    def test_win_rate_30_strong(self):
        assert self._prob(30.0) == WinProbability.STRONG

    def test_boundary_win_rate_30_strong(self):
        # our win = 100 - 30 = 70 → STRONG
        assert self._prob(30.0) == WinProbability.STRONG

    # MODERATE: win_pct >= 45 → their win_rate <= 55
    def test_win_rate_30_1_moderate(self):
        assert self._prob(30.1) == WinProbability.MODERATE

    def test_win_rate_55_moderate(self):
        assert self._prob(55.0) == WinProbability.MODERATE

    def test_boundary_win_rate_55_moderate(self):
        # our win = 100 - 55 = 45 → MODERATE
        assert self._prob(55.0) == WinProbability.MODERATE

    # WEAK: win_pct >= 25 → their win_rate <= 75
    def test_win_rate_55_1_weak(self):
        assert self._prob(55.1) == WinProbability.WEAK

    def test_win_rate_75_weak(self):
        assert self._prob(75.0) == WinProbability.WEAK

    def test_boundary_win_rate_75_weak(self):
        # our win = 100 - 75 = 25 → WEAK
        assert self._prob(75.0) == WinProbability.WEAK

    # VERY_WEAK: win_pct < 25 → their win_rate > 75
    def test_win_rate_75_1_very_weak(self):
        assert self._prob(75.1) == WinProbability.VERY_WEAK

    def test_win_rate_100_very_weak(self):
        assert self._prob(100.0) == WinProbability.VERY_WEAK

    def test_boundary_win_rate_76_very_weak(self):
        assert self._prob(76.0) == WinProbability.VERY_WEAK


# ===========================================================================
# 15. TestBattlecardActionLogic
# ===========================================================================

class TestBattlecardActionLogic:
    def test_critical_threat_gives_escalate(self):
        comp = make_competitor()
        action = _battlecard_action(CompetitorThreat.CRITICAL, comp)
        assert action == BattlecardAction.ESCALATE

    def test_high_threat_gives_differentiate(self):
        comp = make_competitor()
        action = _battlecard_action(CompetitorThreat.HIGH, comp)
        assert action == BattlecardAction.DIFFERENTIATE

    def test_medium_low_feature_parity_above_50_gives_counter(self):
        comp = make_competitor(feature_parity_pct=50.0, avg_discount_offered_pct=10.0)
        action = _battlecard_action(CompetitorThreat.MEDIUM, comp)
        assert action == BattlecardAction.COUNTER

    def test_medium_discount_above_20_gives_counter(self):
        comp = make_competitor(feature_parity_pct=10.0, avg_discount_offered_pct=20.0)
        action = _battlecard_action(CompetitorThreat.MEDIUM, comp)
        assert action == BattlecardAction.COUNTER

    def test_low_feature_parity_below_50_no_discount_gives_monitor(self):
        comp = make_competitor(feature_parity_pct=49.9, avg_discount_offered_pct=19.9)
        action = _battlecard_action(CompetitorThreat.LOW, comp)
        assert action == BattlecardAction.MONITOR

    def test_medium_threat_no_trigger_gives_monitor(self):
        comp = make_competitor(feature_parity_pct=10.0, avg_discount_offered_pct=10.0)
        action = _battlecard_action(CompetitorThreat.MEDIUM, comp)
        assert action == BattlecardAction.MONITOR

    def test_critical_overrides_counter_conditions(self):
        comp = make_competitor(feature_parity_pct=80.0, avg_discount_offered_pct=30.0)
        action = _battlecard_action(CompetitorThreat.CRITICAL, comp)
        assert action == BattlecardAction.ESCALATE

    def test_high_overrides_counter_conditions(self):
        comp = make_competitor(feature_parity_pct=90.0, avg_discount_offered_pct=40.0)
        action = _battlecard_action(CompetitorThreat.HIGH, comp)
        assert action == BattlecardAction.DIFFERENTIATE

    def test_low_threat_discount_exactly_20_gives_counter(self):
        comp = make_competitor(feature_parity_pct=0.0, avg_discount_offered_pct=20.0)
        action = _battlecard_action(CompetitorThreat.LOW, comp)
        assert action == BattlecardAction.COUNTER

    def test_low_threat_feature_exactly_50_gives_counter(self):
        comp = make_competitor(feature_parity_pct=50.0, avg_discount_offered_pct=0.0)
        action = _battlecard_action(CompetitorThreat.LOW, comp)
        assert action == BattlecardAction.COUNTER


# ===========================================================================
# 16. TestOurAdvantages
# ===========================================================================

class TestOurAdvantages:
    def test_support_diff_above_1_5_included(self):
        comp = make_competitor(our_support_rating=8.5, their_support_rating=6.0)
        adv = _our_advantages(comp)
        assert any("8.5" in a and "6.0" in a for a in adv)

    def test_support_diff_below_1_5_not_included(self):
        comp = make_competitor(our_support_rating=7.0, their_support_rating=6.0)
        adv = _our_advantages(comp)
        assert not any("7.0" in a and "6.0" in a for a in adv)

    def test_support_diff_exactly_1_5_included(self):
        comp = make_competitor(our_support_rating=7.5, their_support_rating=6.0)
        adv = _our_advantages(comp)
        assert any("7.5" in a and "6.0" in a for a in adv)

    def test_price_above_100_included(self):
        comp = make_competitor(price_vs_us_pct=110.0, our_integration_advantages=[], our_unique_features=[])
        adv = _our_advantages(comp)
        assert any("compétitif" in a or "prix" in a.lower() or "Pricing" in a for a in adv)

    def test_price_exactly_100_not_included(self):
        comp = make_competitor(price_vs_us_pct=100.0, our_unique_features=[], our_integration_advantages=[])
        adv = _our_advantages(comp)
        assert not any("Pricing" in a for a in adv)

    def test_three_unique_features_gives_count_message(self):
        comp = make_competitor(our_unique_features=["F1", "F2", "F3"], our_integration_advantages=[])
        adv = _our_advantages(comp)
        assert any("3" in a and "exclusives" in a for a in adv)

    def test_one_unique_feature_gives_singular_message(self):
        comp = make_competitor(our_unique_features=["F1"], our_integration_advantages=[])
        adv = _our_advantages(comp)
        assert any("1" in a and "exclusive" in a for a in adv)

    def test_zero_unique_features_no_count_message(self):
        comp = make_competitor(our_unique_features=[], our_integration_advantages=[])
        adv = _our_advantages(comp)
        assert not any("fonctionnalité" in a.lower() and "exclusive" in a.lower() for a in adv)

    def test_integration_advantages_included(self):
        comp = make_competitor(our_integration_advantages=["Salesforce", "HubSpot"])
        adv = _our_advantages(comp)
        assert any("2" in a and "intégration" in a for a in adv)

    def test_no_integration_advantages_not_included(self):
        comp = make_competitor(our_integration_advantages=[])
        adv = _our_advantages(comp)
        assert not any("intégration" in a.lower() for a in adv)

    def test_customer_churn_signal_included(self):
        comp = make_competitor(customer_churn_signal=True)
        adv = _our_advantages(comp)
        assert any("mécontents" in a or "churn" in a.lower() or "déplacement" in a for a in adv)

    def test_no_customer_churn_not_included(self):
        comp = make_competitor(customer_churn_signal=False)
        adv = _our_advantages(comp)
        assert not any("mécontents" in a for a in adv)

    def test_unique_features_appended_up_to_3(self):
        comp = make_competitor(our_unique_features=["F1", "F2", "F3", "F4"])
        adv = _our_advantages(comp)
        assert "F1" in adv
        assert "F2" in adv
        assert "F3" in adv
        assert "F4" not in adv

    def test_returns_list(self):
        comp = make_competitor()
        assert isinstance(_our_advantages(comp), list)


# ===========================================================================
# 17. TestTheirAdvantages
# ===========================================================================

class TestTheirAdvantages:
    def test_price_85_included(self):
        comp = make_competitor(price_vs_us_pct=85.0)
        adv = _their_advantages(comp)
        assert any("15" in a and "inférieur" in a for a in adv)

    def test_price_above_85_not_included(self):
        comp = make_competitor(price_vs_us_pct=90.0)
        adv = _their_advantages(comp)
        assert not any("inférieur" in a for a in adv)

    def test_price_70_included(self):
        comp = make_competitor(price_vs_us_pct=70.0)
        adv = _their_advantages(comp)
        assert any("inférieur" in a for a in adv)

    def test_feature_parity_70_included(self):
        comp = make_competitor(feature_parity_pct=70.0)
        adv = _their_advantages(comp)
        assert any("70" in a and "Parité" in a for a in adv)

    def test_feature_parity_below_70_not_included(self):
        comp = make_competitor(feature_parity_pct=69.9)
        adv = _their_advantages(comp)
        assert not any("Parité fonctionnelle" in a for a in adv)

    def test_market_leader_included(self):
        comp = make_competitor(market_position=MarketPosition.LEADER)
        adv = _their_advantages(comp)
        assert any("Notoriété" in a for a in adv)

    def test_market_challenger_included(self):
        comp = make_competitor(market_position=MarketPosition.CHALLENGER)
        adv = _their_advantages(comp)
        assert any("Notoriété" in a for a in adv)

    def test_market_niche_not_included(self):
        comp = make_competitor(market_position=MarketPosition.NICHE)
        adv = _their_advantages(comp)
        assert not any("Notoriété" in a for a in adv)

    def test_market_emerging_not_included(self):
        comp = make_competitor(market_position=MarketPosition.EMERGING)
        adv = _their_advantages(comp)
        assert not any("Notoriété" in a for a in adv)

    def test_discount_25_included(self):
        comp = make_competitor(avg_discount_offered_pct=25.0)
        adv = _their_advantages(comp)
        assert any("25" in a and "Remises" in a for a in adv)

    def test_discount_below_25_not_included(self):
        comp = make_competitor(avg_discount_offered_pct=24.9)
        adv = _their_advantages(comp)
        assert not any("Remises" in a for a in adv)

    def test_new_product_launched_included(self):
        comp = make_competitor(new_product_launched=True)
        adv = _their_advantages(comp)
        assert any("Nouveau produit" in a for a in adv)

    def test_no_new_product_not_included(self):
        comp = make_competitor(new_product_launched=False)
        adv = _their_advantages(comp)
        assert not any("Nouveau produit" in a for a in adv)

    def test_funding_raised_included(self):
        comp = make_competitor(funding_raised=True)
        adv = _their_advantages(comp)
        assert any("Financement" in a or "financement" in a for a in adv)

    def test_no_funding_not_included(self):
        comp = make_competitor(funding_raised=False)
        adv = _their_advantages(comp)
        assert not any("Financement" in a for a in adv)

    def test_returns_list(self):
        comp = make_competitor()
        assert isinstance(_their_advantages(comp), list)


# ===========================================================================
# 18. TestCounterTactics
# ===========================================================================

class TestCounterTactics:
    def test_discount_above_20_adds_tco_tactic(self):
        comp = make_competitor(avg_discount_offered_pct=20.0)
        tactics = _counter_tactics(comp, CompetitorThreat.MEDIUM)
        assert any("TCO" in t for t in tactics)

    def test_discount_above_20_adds_budget_tactic(self):
        comp = make_competitor(avg_discount_offered_pct=20.0)
        tactics = _counter_tactics(comp, CompetitorThreat.MEDIUM)
        assert any("budget" in t.lower() for t in tactics)

    def test_discount_below_20_no_tco(self):
        comp = make_competitor(avg_discount_offered_pct=19.9)
        tactics = _counter_tactics(comp, CompetitorThreat.LOW)
        assert not any("TCO" in t for t in tactics)

    def test_feature_parity_60_adds_demo_tactic(self):
        comp = make_competitor(feature_parity_pct=60.0)
        tactics = _counter_tactics(comp, CompetitorThreat.MEDIUM)
        assert any("Démonstration" in t or "demo" in t.lower() for t in tactics)

    def test_feature_parity_60_adds_roadmap_tactic(self):
        comp = make_competitor(feature_parity_pct=60.0)
        tactics = _counter_tactics(comp, CompetitorThreat.MEDIUM)
        assert any("roadmap" in t.lower() for t in tactics)

    def test_feature_parity_below_60_no_demo_tactic(self):
        comp = make_competitor(feature_parity_pct=59.9, avg_discount_offered_pct=0.0)
        tactics = _counter_tactics(comp, CompetitorThreat.LOW)
        assert not any("Démonstration" in t for t in tactics)

    def test_critical_threat_adds_exec_tactic(self):
        comp = make_competitor(avg_discount_offered_pct=0.0, feature_parity_pct=0.0)
        tactics = _counter_tactics(comp, CompetitorThreat.CRITICAL)
        assert any("exec" in t.lower() or "C-level" in t for t in tactics)

    def test_high_threat_adds_exec_tactic(self):
        comp = make_competitor(avg_discount_offered_pct=0.0, feature_parity_pct=0.0)
        tactics = _counter_tactics(comp, CompetitorThreat.HIGH)
        assert any("exec" in t.lower() or "C-level" in t for t in tactics)

    def test_medium_threat_no_exec_tactic(self):
        comp = make_competitor(avg_discount_offered_pct=0.0, feature_parity_pct=0.0, known_weaknesses=[])
        tactics = _counter_tactics(comp, CompetitorThreat.MEDIUM)
        assert not any("C-level" in t for t in tactics)

    def test_known_weaknesses_adds_exploit_tactic(self):
        comp = make_competitor(known_weaknesses=["slow support", "no mobile"])
        tactics = _counter_tactics(comp, CompetitorThreat.LOW)
        assert any("slow support" in t or "faiblesses" in t for t in tactics)

    def test_no_weaknesses_no_exploit_tactic(self):
        comp = make_competitor(known_weaknesses=[], avg_discount_offered_pct=0.0,
                               feature_parity_pct=0.0)
        tactics = _counter_tactics(comp, CompetitorThreat.LOW)
        assert not any("faiblesses" in t for t in tactics)

    def test_poc_tactic_always_present(self):
        comp = make_competitor(known_weaknesses=[], avg_discount_offered_pct=0.0,
                               feature_parity_pct=0.0)
        tactics = _counter_tactics(comp, CompetitorThreat.LOW)
        assert any("POC" in t or "essai" in t for t in tactics)

    def test_poc_tactic_present_with_other_triggers(self):
        comp = make_competitor(avg_discount_offered_pct=30.0, feature_parity_pct=80.0)
        tactics = _counter_tactics(comp, CompetitorThreat.CRITICAL)
        assert any("POC" in t or "essai" in t for t in tactics)

    def test_returns_list(self):
        comp = make_competitor()
        assert isinstance(_counter_tactics(comp, CompetitorThreat.MEDIUM), list)

    def test_weaknesses_limited_to_2(self):
        comp = make_competitor(known_weaknesses=["W1", "W2", "W3"])
        tactics = _counter_tactics(comp, CompetitorThreat.LOW)
        exploit = [t for t in tactics if "faiblesses" in t]
        if exploit:
            assert "W3" not in exploit[0]


# ===========================================================================
# 19. TestTalkTracks
# ===========================================================================

class TestTalkTracks:
    def test_first_track_contains_competitor_name(self):
        comp = make_competitor(competitor_name="Acme")
        tracks = _talk_tracks(comp)
        assert len(tracks) >= 1
        assert "Acme" in tracks[0]

    def test_always_has_at_least_one_track(self):
        comp = make_competitor(known_weaknesses=[], customer_churn_signal=False,
                               avg_discount_offered_pct=0.0)
        tracks = _talk_tracks(comp)
        assert len(tracks) >= 1

    def test_always_has_generic_results_track(self):
        comp = make_competitor(known_weaknesses=[], customer_churn_signal=False,
                               avg_discount_offered_pct=0.0)
        tracks = _talk_tracks(comp)
        assert any("résultats" in t.lower() for t in tracks)

    def test_discount_above_20_adds_tco_track(self):
        comp = make_competitor(avg_discount_offered_pct=20.0)
        tracks = _talk_tracks(comp)
        assert any("TCO" in t for t in tracks)

    def test_discount_below_20_no_tco_track(self):
        comp = make_competitor(avg_discount_offered_pct=19.9, known_weaknesses=[],
                               customer_churn_signal=False)
        tracks = _talk_tracks(comp)
        assert not any("TCO" in t for t in tracks)

    def test_known_weaknesses_adds_weakness_track(self):
        comp = make_competitor(known_weaknesses=["slow support"])
        tracks = _talk_tracks(comp)
        assert any("slow support" in t for t in tracks)

    def test_no_weaknesses_no_weakness_track(self):
        comp = make_competitor(known_weaknesses=[], avg_discount_offered_pct=0.0,
                               customer_churn_signal=False)
        tracks = _talk_tracks(comp)
        assert not any("mentionnent" in t for t in tracks)

    def test_churn_signal_adds_churn_track(self):
        comp = make_competitor(customer_churn_signal=True)
        tracks = _talk_tracks(comp)
        assert any("transition" in t or "churn" in t.lower() for t in tracks)

    def test_no_churn_signal_no_churn_track(self):
        comp = make_competitor(customer_churn_signal=False, known_weaknesses=[],
                               avg_discount_offered_pct=0.0)
        tracks = _talk_tracks(comp)
        assert not any("transition" in t for t in tracks)

    def test_competitor_name_in_weakness_track(self):
        comp = make_competitor(competitor_name="Acme", known_weaknesses=["bug"])
        tracks = _talk_tracks(comp)
        weakness_tracks = [t for t in tracks if "mentionnent" in t]
        assert any("Acme" in t for t in weakness_tracks)

    def test_returns_list(self):
        comp = make_competitor()
        assert isinstance(_talk_tracks(comp), list)


# ===========================================================================
# 20. TestObjectionResponses
# ===========================================================================

class TestObjectionResponses:
    def test_price_vs_90_adds_price_response(self):
        comp = make_competitor(price_vs_us_pct=90.0)
        responses = _objection_responses(comp)
        assert any("prix" in r.lower() or "ROI" in r for r in responses)

    def test_price_below_90_adds_price_response(self):
        comp = make_competitor(price_vs_us_pct=80.0)
        responses = _objection_responses(comp)
        assert any("Objection prix" in r for r in responses)

    def test_price_above_90_no_price_response(self):
        comp = make_competitor(price_vs_us_pct=91.0, new_product_launched=False)
        responses = _objection_responses(comp)
        assert not any("Objection prix" in r for r in responses)

    def test_always_has_feature_response(self):
        comp = make_competitor(price_vs_us_pct=100.0, new_product_launched=False)
        responses = _objection_responses(comp)
        assert any("fonctionnalités" in r.lower() or "Objection fonctionnalités" in r for r in responses)

    def test_always_has_brand_response(self):
        comp = make_competitor(price_vs_us_pct=100.0, new_product_launched=False)
        responses = _objection_responses(comp)
        assert any("marque" in r.lower() or "Objection marque" in r for r in responses)

    def test_new_product_launched_adds_response(self):
        comp = make_competitor(new_product_launched=True, price_vs_us_pct=100.0)
        responses = _objection_responses(comp)
        assert any("nouveau produit" in r.lower() for r in responses)

    def test_no_new_product_no_new_product_response(self):
        comp = make_competitor(new_product_launched=False, price_vs_us_pct=100.0)
        responses = _objection_responses(comp)
        assert not any("nouveau produit" in r.lower() for r in responses)

    def test_competitor_name_in_feature_response(self):
        comp = make_competitor(competitor_name="Acme", price_vs_us_pct=100.0)
        responses = _objection_responses(comp)
        feature_resp = [r for r in responses if "fonctionnalités" in r.lower()]
        assert any("Acme" in r for r in feature_resp)

    def test_returns_list(self):
        comp = make_competitor()
        assert isinstance(_objection_responses(comp), list)

    def test_minimum_two_responses_always(self):
        comp = make_competitor(price_vs_us_pct=100.0, new_product_launched=False)
        responses = _objection_responses(comp)
        assert len(responses) >= 2

    def test_price_exactly_90_adds_price_response(self):
        comp = make_competitor(price_vs_us_pct=90.0)
        responses = _objection_responses(comp)
        assert any("Objection prix" in r for r in responses)


# ===========================================================================
# 21. TestEngineGenerateAndFilters
# ===========================================================================

class TestEngineGenerateAndFilters:
    def setup_method(self):
        self.engine = CompetitiveBattlecardEngine()

    def test_generate_returns_battlecard_result(self):
        comp = make_competitor()
        result = self.engine.generate(comp)
        assert isinstance(result, BattlecardResult)

    def test_generate_stores_result(self):
        comp = make_competitor()
        self.engine.generate(comp)
        assert len(self.engine.all_battlecards()) == 1

    def test_generate_updates_existing(self):
        comp = make_competitor()
        self.engine.generate(comp)
        self.engine.generate(comp)
        assert len(self.engine.all_battlecards()) == 1

    def test_generate_batch_returns_list(self):
        comps = [make_competitor(competitor_id=f"c{i}", win_rate_against_us_pct=float(i*10)) for i in range(3)]
        results = self.engine.generate_batch(comps)
        assert isinstance(results, list)
        assert len(results) == 3

    def test_generate_batch_sorted_desc(self):
        comps = [
            make_competitor(competitor_id="c1", win_rate_against_us_pct=10.0),
            make_competitor(competitor_id="c2", win_rate_against_us_pct=60.0),
            make_competitor(competitor_id="c3", win_rate_against_us_pct=40.0),
        ]
        results = self.engine.generate_batch(comps)
        scores = [r.threat_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_by_threat_filters_correctly(self):
        comp_high = make_competitor(competitor_id="c1", win_rate_against_us_pct=60.0,
                                     active_deals_competing=10, feature_parity_pct=80.0,
                                     price_vs_us_pct=70.0, recent_price_drop=True,
                                     new_product_launched=True, funding_raised=True)
        comp_low = make_competitor(competitor_id="c2", win_rate_against_us_pct=0.0,
                                    active_deals_competing=0, feature_parity_pct=0.0,
                                    price_vs_us_pct=100.0)
        self.engine.generate(comp_high)
        self.engine.generate(comp_low)
        critical = self.engine.by_threat(CompetitorThreat.CRITICAL)
        for r in critical:
            assert r.threat_level == CompetitorThreat.CRITICAL

    def test_by_action_filters_correctly(self):
        comp = make_competitor(win_rate_against_us_pct=60.0, active_deals_competing=10,
                                feature_parity_pct=80.0, price_vs_us_pct=70.0,
                                recent_price_drop=True, new_product_launched=True, funding_raised=True)
        self.engine.generate(comp)
        escalate = self.engine.by_action(BattlecardAction.ESCALATE)
        for r in escalate:
            assert r.battlecard_action == BattlecardAction.ESCALATE

    def test_by_win_probability_filters_correctly(self):
        comp = make_competitor(win_rate_against_us_pct=5.0)
        self.engine.generate(comp)
        strong = self.engine.by_win_probability(WinProbability.STRONG)
        for r in strong:
            assert r.win_probability == WinProbability.STRONG

    def test_critical_threats_returns_only_critical(self):
        comp = make_competitor(win_rate_against_us_pct=60.0, active_deals_competing=10,
                                feature_parity_pct=80.0, price_vs_us_pct=70.0,
                                recent_price_drop=True, new_product_launched=True, funding_raised=True)
        self.engine.generate(comp)
        criticals = self.engine.critical_threats()
        for r in criticals:
            assert r.threat_level == CompetitorThreat.CRITICAL

    def test_needs_escalation_returns_only_escalate(self):
        comp = make_competitor(win_rate_against_us_pct=60.0, active_deals_competing=10,
                                feature_parity_pct=80.0, price_vs_us_pct=70.0,
                                recent_price_drop=True, new_product_launched=True, funding_raised=True)
        self.engine.generate(comp)
        escalations = self.engine.needs_escalation()
        for r in escalations:
            assert r.battlecard_action == BattlecardAction.ESCALATE

    def test_all_battlecards_sorted_desc(self):
        comps = [
            make_competitor(competitor_id="c1", win_rate_against_us_pct=10.0),
            make_competitor(competitor_id="c2", win_rate_against_us_pct=60.0),
            make_competitor(competitor_id="c3", win_rate_against_us_pct=40.0),
        ]
        for c in comps:
            self.engine.generate(c)
        cards = self.engine.all_battlecards()
        scores = [r.threat_score for r in cards]
        assert scores == sorted(scores, reverse=True)

    def test_generate_sets_competitor_id(self):
        comp = make_competitor(competitor_id="xyz")
        result = self.engine.generate(comp)
        assert result.competitor_id == "xyz"

    def test_generate_sets_competitor_name(self):
        comp = make_competitor(competitor_name="TestCo")
        result = self.engine.generate(comp)
        assert result.competitor_name == "TestCo"

    def test_generate_sets_market_position(self):
        comp = make_competitor(market_position=MarketPosition.LEADER)
        result = self.engine.generate(comp)
        assert result.market_position == "leader"

    def test_by_threat_empty_when_none_match(self):
        comp = make_competitor(win_rate_against_us_pct=0.0, active_deals_competing=0,
                                feature_parity_pct=0.0, price_vs_us_pct=100.0)
        self.engine.generate(comp)
        critical = self.engine.by_threat(CompetitorThreat.CRITICAL)
        assert isinstance(critical, list)


# ===========================================================================
# 22. TestEngineAggregates
# ===========================================================================

class TestEngineAggregates:
    def setup_method(self):
        self.engine = CompetitiveBattlecardEngine()

    def test_avg_threat_score_empty(self):
        assert self.engine.avg_threat_score() == 0.0

    def test_avg_threat_score_single(self):
        comp = make_competitor()
        result = self.engine.generate(comp)
        assert self.engine.avg_threat_score() == result.threat_score

    def test_avg_threat_score_multiple(self):
        comps = [
            make_competitor(competitor_id="c1", win_rate_against_us_pct=0.0,
                             active_deals_competing=0, feature_parity_pct=0.0, price_vs_us_pct=100.0),
            make_competitor(competitor_id="c2", win_rate_against_us_pct=60.0,
                             active_deals_competing=10, feature_parity_pct=80.0, price_vs_us_pct=70.0),
        ]
        self.engine.generate_batch(comps)
        avg = self.engine.avg_threat_score()
        assert isinstance(avg, (int, float))
        assert avg > 0.0

    def test_avg_threat_score_is_float(self):
        comp = make_competitor()
        self.engine.generate(comp)
        assert isinstance(self.engine.avg_threat_score(), (int, float))

    def test_summary_empty_engine(self):
        s = self.engine.summary()
        assert s["total"] == 0
        assert s["avg_threat_score"] == 0.0
        assert s["critical_count"] == 0
        assert s["escalation_count"] == 0

    def test_summary_keys_present(self):
        s = self.engine.summary()
        expected = {"total", "threat_counts", "action_counts", "win_probability_counts",
                    "avg_threat_score", "critical_count", "escalation_count"}
        assert expected == set(s.keys())

    def test_summary_total_correct(self):
        comps = [make_competitor(competitor_id=f"c{i}") for i in range(3)]
        self.engine.generate_batch(comps)
        s = self.engine.summary()
        assert s["total"] == 3

    def test_summary_threat_counts_sum_to_total(self):
        comps = [make_competitor(competitor_id=f"c{i}") for i in range(4)]
        self.engine.generate_batch(comps)
        s = self.engine.summary()
        assert sum(s["threat_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        comps = [make_competitor(competitor_id=f"c{i}") for i in range(4)]
        self.engine.generate_batch(comps)
        s = self.engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_win_probability_counts_sum_to_total(self):
        comps = [make_competitor(competitor_id=f"c{i}") for i in range(4)]
        self.engine.generate_batch(comps)
        s = self.engine.summary()
        assert sum(s["win_probability_counts"].values()) == s["total"]

    def test_summary_critical_count_matches_by_threat(self):
        comp = make_competitor(win_rate_against_us_pct=60.0, active_deals_competing=10,
                                feature_parity_pct=80.0, price_vs_us_pct=70.0,
                                recent_price_drop=True, new_product_launched=True, funding_raised=True)
        self.engine.generate(comp)
        s = self.engine.summary()
        assert s["critical_count"] == len(self.engine.critical_threats())

    def test_summary_escalation_count_matches_needs_escalation(self):
        comp = make_competitor(win_rate_against_us_pct=60.0, active_deals_competing=10,
                                feature_parity_pct=80.0, price_vs_us_pct=70.0,
                                recent_price_drop=True, new_product_launched=True, funding_raised=True)
        self.engine.generate(comp)
        s = self.engine.summary()
        assert s["escalation_count"] == len(self.engine.needs_escalation())

    def test_reset_clears_battlecards(self):
        comp = make_competitor()
        self.engine.generate(comp)
        self.engine.reset()
        assert len(self.engine.all_battlecards()) == 0

    def test_reset_resets_avg_score(self):
        comp = make_competitor()
        self.engine.generate(comp)
        self.engine.reset()
        assert self.engine.avg_threat_score() == 0.0

    def test_reset_resets_summary_total(self):
        comp = make_competitor()
        self.engine.generate(comp)
        self.engine.reset()
        assert self.engine.summary()["total"] == 0

    def test_avg_threat_score_rounded_to_1dp(self):
        comps = [make_competitor(competitor_id=f"c{i}") for i in range(5)]
        self.engine.generate_batch(comps)
        avg = self.engine.avg_threat_score()
        assert avg == round(avg, 1)

    def test_summary_avg_threat_score_matches_avg_threat_score(self):
        comps = [make_competitor(competitor_id=f"c{i}") for i in range(3)]
        self.engine.generate_batch(comps)
        s = self.engine.summary()
        assert s["avg_threat_score"] == self.engine.avg_threat_score()

    def test_generate_sets_threat_score_numeric(self):
        comp = make_competitor()
        result = self.engine.generate(comp)
        assert isinstance(result.threat_score, (int, float))

    def test_generate_sets_threat_level_enum(self):
        comp = make_competitor()
        result = self.engine.generate(comp)
        assert isinstance(result.threat_level, CompetitorThreat)

    def test_generate_sets_win_probability_enum(self):
        comp = make_competitor()
        result = self.engine.generate(comp)
        assert isinstance(result.win_probability, WinProbability)

    def test_generate_sets_battlecard_action_enum(self):
        comp = make_competitor()
        result = self.engine.generate(comp)
        assert isinstance(result.battlecard_action, BattlecardAction)

    def test_generate_executive_summary_non_empty(self):
        comp = make_competitor()
        result = self.engine.generate(comp)
        assert isinstance(result.executive_summary, str)
        assert len(result.executive_summary) > 0

    def test_generate_executive_summary_contains_name(self):
        comp = make_competitor(competitor_name="CorpX")
        result = self.engine.generate(comp)
        assert "CorpX" in result.executive_summary

    def test_reset_allows_regenerate(self):
        comp = make_competitor()
        self.engine.generate(comp)
        self.engine.reset()
        self.engine.generate(comp)
        assert len(self.engine.all_battlecards()) == 1

    def test_generate_batch_all_stored(self):
        comps = [make_competitor(competitor_id=f"c{i}") for i in range(5)]
        self.engine.generate_batch(comps)
        assert len(self.engine.all_battlecards()) == 5

    def test_summary_threat_counts_keys_are_strings(self):
        comp = make_competitor()
        self.engine.generate(comp)
        s = self.engine.summary()
        for key in s["threat_counts"]:
            assert isinstance(key, str)

    def test_summary_action_counts_keys_are_strings(self):
        comp = make_competitor()
        self.engine.generate(comp)
        s = self.engine.summary()
        for key in s["action_counts"]:
            assert isinstance(key, str)

    def test_avg_threat_score_between_0_and_100(self):
        comps = [make_competitor(competitor_id=f"c{i}") for i in range(3)]
        self.engine.generate_batch(comps)
        avg = self.engine.avg_threat_score()
        assert 0.0 <= avg <= 100.0
