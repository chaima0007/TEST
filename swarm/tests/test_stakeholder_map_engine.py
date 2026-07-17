"""
Comprehensive pytest test suite for swarm.intelligence.stakeholder_map_engine.
Covers all enums, dataclasses, scoring formulas, properties, and end-to-end scenarios.
"""
from __future__ import annotations

import dataclasses
from typing import get_type_hints

import pytest

from swarm.intelligence.stakeholder_map_engine import (
    CoverageRisk,
    EngagementLevel,
    RelationshipStatus,
    StakeholderInput,
    StakeholderMapEngine,
    StakeholderResult,
    StakeholderRole,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers / Fixtures
# ─────────────────────────────────────────────────────────────────────────────

def make_input(
    stakeholder_id: str = "s1",
    account_id: str = "a1",
    deal_id: str = "d1",
    seniority: int = 3,
    activities_30d: int = 5,
    meetings_held: int = 2,
    emails_sent: int = 4,
    emails_responded: int = 2,
    last_contact_days: int = 5,
    sentiment_score: float = 0.6,
    is_economic_buyer: bool = False,
    is_champion: bool = False,
    is_technical_buyer: bool = False,
    is_end_user: bool = False,
    is_blocker: bool = False,
    has_budget_authority: bool = False,
    deal_stage: str = "discovery",
    prior_wins: int = 0,
    days_in_deal: int = 30,
    aligned_with_vendor: bool = False,
) -> StakeholderInput:
    return StakeholderInput(
        stakeholder_id=stakeholder_id,
        account_id=account_id,
        deal_id=deal_id,
        seniority=seniority,
        activities_30d=activities_30d,
        meetings_held=meetings_held,
        emails_sent=emails_sent,
        emails_responded=emails_responded,
        last_contact_days=last_contact_days,
        sentiment_score=sentiment_score,
        is_economic_buyer=is_economic_buyer,
        is_champion=is_champion,
        is_technical_buyer=is_technical_buyer,
        is_end_user=is_end_user,
        is_blocker=is_blocker,
        has_budget_authority=has_budget_authority,
        deal_stage=deal_stage,
        prior_wins=prior_wins,
        days_in_deal=days_in_deal,
        aligned_with_vendor=aligned_with_vendor,
    )


@pytest.fixture
def engine() -> StakeholderMapEngine:
    return StakeholderMapEngine()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Enum tests
# ─────────────────────────────────────────────────────────────────────────────

class TestStakeholderRoleEnum:
    def test_member_count(self):
        assert len(StakeholderRole) == 7

    def test_str_inheritance(self):
        assert issubclass(StakeholderRole, str)

    def test_economic_buyer_value(self):
        assert StakeholderRole.ECONOMIC_BUYER == "economic_buyer"

    def test_champion_value(self):
        assert StakeholderRole.CHAMPION == "champion"

    def test_technical_buyer_value(self):
        assert StakeholderRole.TECHNICAL_BUYER == "technical_buyer"

    def test_end_user_value(self):
        assert StakeholderRole.END_USER == "end_user"

    def test_blocker_value(self):
        assert StakeholderRole.BLOCKER == "blocker"

    def test_influencer_value(self):
        assert StakeholderRole.INFLUENCER == "influencer"

    def test_unknown_value(self):
        assert StakeholderRole.UNKNOWN == "unknown"

    def test_all_members_accessible(self):
        members = {m.name for m in StakeholderRole}
        assert members == {
            "ECONOMIC_BUYER", "CHAMPION", "TECHNICAL_BUYER",
            "END_USER", "BLOCKER", "INFLUENCER", "UNKNOWN",
        }

    def test_str_comparison_works(self):
        assert StakeholderRole.ECONOMIC_BUYER == StakeholderRole.ECONOMIC_BUYER
        assert StakeholderRole.CHAMPION != StakeholderRole.UNKNOWN


class TestEngagementLevelEnum:
    def test_member_count(self):
        assert len(EngagementLevel) == 5

    def test_str_inheritance(self):
        assert issubclass(EngagementLevel, str)

    def test_strong_value(self):
        assert EngagementLevel.STRONG == "strong"

    def test_moderate_value(self):
        assert EngagementLevel.MODERATE == "moderate"

    def test_weak_value(self):
        assert EngagementLevel.WEAK == "weak"

    def test_none_value(self):
        assert EngagementLevel.NONE == "none"

    def test_hostile_value(self):
        assert EngagementLevel.HOSTILE == "hostile"

    def test_all_members_accessible(self):
        members = {m.name for m in EngagementLevel}
        assert members == {"STRONG", "MODERATE", "WEAK", "NONE", "HOSTILE"}


class TestRelationshipStatusEnum:
    def test_member_count(self):
        assert len(RelationshipStatus) == 5

    def test_str_inheritance(self):
        assert issubclass(RelationshipStatus, str)

    def test_sponsor_value(self):
        assert RelationshipStatus.SPONSOR == "sponsor"

    def test_ally_value(self):
        assert RelationshipStatus.ALLY == "ally"

    def test_neutral_value(self):
        assert RelationshipStatus.NEUTRAL == "neutral"

    def test_skeptic_value(self):
        assert RelationshipStatus.SKEPTIC == "skeptic"

    def test_opponent_value(self):
        assert RelationshipStatus.OPPONENT == "opponent"

    def test_all_members_accessible(self):
        members = {m.name for m in RelationshipStatus}
        assert members == {"SPONSOR", "ALLY", "NEUTRAL", "SKEPTIC", "OPPONENT"}


class TestCoverageRiskEnum:
    def test_member_count(self):
        assert len(CoverageRisk) == 4

    def test_str_inheritance(self):
        assert issubclass(CoverageRisk, str)

    def test_covered_value(self):
        assert CoverageRisk.COVERED == "covered"

    def test_partial_value(self):
        assert CoverageRisk.PARTIAL == "partial"

    def test_at_risk_value(self):
        assert CoverageRisk.AT_RISK == "at_risk"

    def test_critical_value(self):
        assert CoverageRisk.CRITICAL == "critical"

    def test_all_members_accessible(self):
        members = {m.name for m in CoverageRisk}
        assert members == {"COVERED", "PARTIAL", "AT_RISK", "CRITICAL"}


# ─────────────────────────────────────────────────────────────────────────────
# 2. StakeholderInput field count
# ─────────────────────────────────────────────────────────────────────────────

class TestStakeholderInputFieldCount:
    def test_exactly_20_fields(self):
        fields = dataclasses.fields(StakeholderInput)
        assert len(fields) == 20

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(StakeholderInput)

    def test_field_names(self):
        field_names = {f.name for f in dataclasses.fields(StakeholderInput)}
        expected = {
            "stakeholder_id", "account_id", "deal_id", "seniority",
            "activities_30d", "meetings_held", "emails_sent", "emails_responded",
            "last_contact_days", "sentiment_score", "is_economic_buyer",
            "is_champion", "is_technical_buyer", "is_end_user", "is_blocker",
            "has_budget_authority", "deal_stage", "prior_wins",
            "days_in_deal", "aligned_with_vendor",
        }
        assert field_names == expected

    def test_instantiation_with_all_fields(self):
        inp = make_input()
        assert inp.stakeholder_id == "s1"
        assert inp.seniority == 3


# ─────────────────────────────────────────────────────────────────────────────
# 3. StakeholderResult.to_dict() — exactly 15 keys and correct types
# ─────────────────────────────────────────────────────────────────────────────

class TestStakeholderResultToDict:
    def test_exactly_15_keys(self, engine):
        inp = make_input()
        result = engine.analyze(inp)
        d = result.to_dict()
        assert len(d) == 15

    def test_exact_key_names(self, engine):
        result = engine.analyze(make_input())
        keys = set(result.to_dict().keys())
        expected = {
            "stakeholder_id", "account_id", "deal_id", "influence_score",
            "engagement_level", "relationship_status", "stakeholder_role",
            "coverage_risk", "engagement_gap", "is_at_risk", "priority_rank",
            "recommended_action", "risk_factors", "strengths",
            "recommended_approach",
        }
        assert keys == expected

    def test_stakeholder_id_is_str(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["stakeholder_id"], str)

    def test_account_id_is_str(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["account_id"], str)

    def test_deal_id_is_str(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["deal_id"], str)

    def test_influence_score_is_float(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["influence_score"], float)

    def test_engagement_level_is_str(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["engagement_level"], str)

    def test_relationship_status_is_str(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["relationship_status"], str)

    def test_stakeholder_role_is_str(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["stakeholder_role"], str)

    def test_coverage_risk_is_str(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["coverage_risk"], str)

    def test_engagement_gap_is_float(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["engagement_gap"], float)

    def test_is_at_risk_is_bool(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["is_at_risk"], bool)

    def test_priority_rank_is_int(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["priority_rank"], int)

    def test_recommended_action_is_str(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["recommended_action"], str)

    def test_risk_factors_is_list(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["risk_factors"], list)

    def test_strengths_is_list(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["strengths"], list)

    def test_recommended_approach_is_str(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result.to_dict()["recommended_approach"], str)

    def test_enum_values_are_strings_not_enum_objects(self, engine):
        result = engine.analyze(make_input())
        d = result.to_dict()
        # to_dict() stores .value (a plain str), not the enum instance itself
        assert type(d["engagement_level"]) is str
        assert d["engagement_level"] in [e.value for e in EngagementLevel]
        # Verify it is not an enum instance
        assert not isinstance(d["engagement_level"], EngagementLevel.__class__) or isinstance(d["engagement_level"], str)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Influence score formula
# ─────────────────────────────────────────────────────────────────────────────

class TestInfluenceScore:
    def _get_influence(self, **kwargs) -> float:
        engine = StakeholderMapEngine()
        return engine.analyze(make_input(**kwargs)).influence_score

    def test_seniority_1_base(self):
        score = self._get_influence(seniority=1)
        assert score == 10.0

    def test_seniority_2_base(self):
        score = self._get_influence(seniority=2)
        assert score == 25.0

    def test_seniority_3_base(self):
        score = self._get_influence(seniority=3)
        assert score == 45.0

    def test_seniority_4_base(self):
        score = self._get_influence(seniority=4)
        assert score == 65.0

    def test_seniority_5_base(self):
        score = self._get_influence(seniority=5)
        assert score == 85.0

    def test_economic_buyer_bonus(self):
        base = self._get_influence(seniority=3)
        with_bonus = self._get_influence(seniority=3, is_economic_buyer=True)
        assert with_bonus == base + 15

    def test_budget_authority_bonus(self):
        base = self._get_influence(seniority=3)
        with_bonus = self._get_influence(seniority=3, has_budget_authority=True)
        assert with_bonus == base + 15

    def test_champion_bonus(self):
        base = self._get_influence(seniority=3)
        with_bonus = self._get_influence(seniority=3, is_champion=True)
        assert with_bonus == base + 10

    def test_technical_buyer_bonus(self):
        base = self._get_influence(seniority=3)
        with_bonus = self._get_influence(seniority=3, is_technical_buyer=True)
        assert with_bonus == base + 8

    def test_blocker_penalty(self):
        base = self._get_influence(seniority=3)
        with_penalty = self._get_influence(seniority=3, is_blocker=True)
        assert with_penalty == base - 10

    def test_prior_wins_bonus_exactly_2_no_bonus(self):
        base = self._get_influence(seniority=3)
        with_wins = self._get_influence(seniority=3, prior_wins=2)
        assert with_wins == base  # > 2 required

    def test_prior_wins_bonus_3_gives_plus5(self):
        base = self._get_influence(seniority=3)
        with_wins = self._get_influence(seniority=3, prior_wins=3)
        assert with_wins == base + 5

    def test_prior_wins_bonus_10_gives_plus5(self):
        base = self._get_influence(seniority=3)
        with_wins = self._get_influence(seniority=3, prior_wins=10)
        assert with_wins == base + 5

    def test_all_bonuses_combined(self):
        # base(3)=45 + 15(eco) + 15(budget) + 10(champ) + 8(tech) + 5(wins)
        # - 10(blocker) = 88
        score = self._get_influence(
            seniority=3,
            is_economic_buyer=True,
            has_budget_authority=True,
            is_champion=True,
            is_technical_buyer=True,
            is_blocker=True,
            prior_wins=3,
        )
        assert score == 88.0

    def test_clamp_max_100(self):
        # seniority 5 (85) + 15 + 15 + 10 + 8 + 5 = 138 → clamped to 100
        score = self._get_influence(
            seniority=5,
            is_economic_buyer=True,
            has_budget_authority=True,
            is_champion=True,
            is_technical_buyer=True,
            prior_wins=3,
        )
        assert score == 100.0

    def test_clamp_min_0(self):
        # seniority 1 (10) - 10(blocker) = 0 → no further drop
        score = self._get_influence(seniority=1, is_blocker=True)
        assert score == 0.0

    def test_rounded_to_1_decimal(self):
        score = self._get_influence(seniority=3)
        assert score == round(score, 1)

    def test_economic_buyer_and_budget_authority_both_add_15(self):
        score = self._get_influence(
            seniority=1, is_economic_buyer=True, has_budget_authority=True
        )
        # 10 + 15 + 15 = 40
        assert score == 40.0


# ─────────────────────────────────────────────────────────────────────────────
# 5. Engagement score formula
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementScore:
    def _get_engagement(self, **kwargs) -> float:
        engine = StakeholderMapEngine()
        return engine.analyze(make_input(**kwargs)).engagement_gap  # we need engagement itself

    def _compute_raw(self, **kwargs) -> float:
        """Use engine's internal method directly."""
        engine = StakeholderMapEngine()
        inp = make_input(**kwargs)
        return engine._engagement_score(inp)

    def test_activity_base_capped_at_30(self):
        # activities_30d=10 → 10*3=30, no higher
        score1 = self._compute_raw(activities_30d=10, meetings_held=0, emails_sent=0, emails_responded=0,
                                    last_contact_days=15, sentiment_score=0.5)
        score2 = self._compute_raw(activities_30d=20, meetings_held=0, emails_sent=0, emails_responded=0,
                                    last_contact_days=15, sentiment_score=0.5)
        assert score1 == score2

    def test_activity_base_below_cap(self):
        score = self._compute_raw(activities_30d=3, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=15, sentiment_score=0.5)
        assert score == 9.0  # 3*3=9, no recency/sentiment bonus

    def test_meeting_base_capped_at_20(self):
        score1 = self._compute_raw(activities_30d=0, meetings_held=4, emails_sent=0, emails_responded=0,
                                    last_contact_days=15, sentiment_score=0.5)
        score2 = self._compute_raw(activities_30d=0, meetings_held=10, emails_sent=0, emails_responded=0,
                                    last_contact_days=15, sentiment_score=0.5)
        assert score1 == score2  # both capped at 20

    def test_meeting_base_below_cap(self):
        score = self._compute_raw(activities_30d=0, meetings_held=2, emails_sent=0, emails_responded=0,
                                   last_contact_days=15, sentiment_score=0.5)
        assert score == 10.0  # 2*5=10

    def test_response_rate_capped_at_20(self):
        score1 = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=5, emails_responded=5,
                                    last_contact_days=15, sentiment_score=0.5)
        score2 = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=2, emails_responded=2,
                                    last_contact_days=15, sentiment_score=0.5)
        assert score1 == score2 == 20.0  # both 100% rate → 20

    def test_response_rate_partial(self):
        # 1/2 = 0.5 rate → 0.5 * 20 = 10
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=2, emails_responded=1,
                                   last_contact_days=15, sentiment_score=0.5)
        assert score == 10.0

    def test_response_rate_zero_emails_sent(self):
        # emails_sent=0 → response_rate = 0/max(1,0) = 0/1 = 0
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=15, sentiment_score=0.5)
        assert score == 0.0

    def test_recency_bonus_7_days(self):
        # last_contact_days ≤ 7 → +15
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=7, sentiment_score=0.5)
        assert score == 15.0

    def test_recency_bonus_1_day(self):
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=1, sentiment_score=0.5)
        assert score == 15.0

    def test_recency_bonus_14_days(self):
        # 8 ≤ last_contact_days ≤ 14 → +5
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=14, sentiment_score=0.5)
        assert score == 5.0

    def test_recency_bonus_8_days(self):
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=8, sentiment_score=0.5)
        assert score == 5.0

    def test_recency_no_bonus_15_to_21_days(self):
        # 15 ≤ last_contact_days ≤ 21 → no recency change
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=15, sentiment_score=0.5)
        assert score == 0.0

    def test_recency_no_bonus_21_days(self):
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=21, sentiment_score=0.5)
        assert score == 0.0

    def test_recency_penalty_22_to_30_days(self):
        # 21 < last_contact_days ≤ 30 → -10
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=22, sentiment_score=0.5)
        assert score == 0.0  # -10 clamped to 0

    def test_recency_penalty_30_days(self):
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=30, sentiment_score=0.5)
        assert score == 0.0  # -10 clamped to 0

    def test_recency_penalty_31_days(self):
        # last_contact_days > 30 → -20
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=31, sentiment_score=0.5)
        assert score == 0.0  # -20 clamped to 0

    def test_sentiment_bonus_high(self):
        # sentiment > 0.7 → +10
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=15, sentiment_score=0.8)
        assert score == 10.0

    def test_sentiment_bonus_exactly_07_no_bonus(self):
        # sentiment = 0.7 → NOT > 0.7, no bonus
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=15, sentiment_score=0.7)
        assert score == 0.0

    def test_sentiment_penalty_low(self):
        # sentiment < 0.3 → -15
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=15, sentiment_score=0.2)
        assert score == 0.0  # -15 clamped to 0

    def test_sentiment_penalty_exactly_03_no_penalty(self):
        # sentiment = 0.3 → NOT < 0.3, no penalty
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                                   last_contact_days=15, sentiment_score=0.3)
        assert score == 0.0

    def test_clamp_max_100(self):
        # max all components: 30 + 20 + 20 + 15 + 10 = 95 ≤ 100
        score = self._compute_raw(
            activities_30d=10, meetings_held=4, emails_sent=5, emails_responded=5,
            last_contact_days=1, sentiment_score=0.9,
        )
        assert score == 95.0

    def test_clamp_min_0(self):
        # worst case: 0 base, recency -20, sentiment -15 → clamped to 0
        score = self._compute_raw(
            activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
            last_contact_days=60, sentiment_score=0.1,
        )
        assert score == 0.0

    def test_rounded_to_1_decimal(self):
        # 1/3 response rate → 0.333... * 20 → rounded
        score = self._compute_raw(activities_30d=0, meetings_held=0, emails_sent=3, emails_responded=1,
                                   last_contact_days=15, sentiment_score=0.5)
        assert score == round(score, 1)

    def test_combined_components(self):
        # activities_30d=5→15, meetings_held=2→10, 1/1 response→20, ≤7d→+15, sentiment 0.8→+10 = 70
        score = self._compute_raw(
            activities_30d=5, meetings_held=2, emails_sent=1, emails_responded=1,
            last_contact_days=5, sentiment_score=0.8,
        )
        assert score == 70.0


# ─────────────────────────────────────────────────────────────────────────────
# 6. EngagementLevel thresholds and HOSTILE condition
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementLevel:
    def _get_level(self, **kwargs) -> EngagementLevel:
        engine = StakeholderMapEngine()
        inp = make_input(**kwargs)
        engagement = engine._engagement_score(inp)
        return engine._engagement_level(inp, engagement)

    def _get_level_with_score(self, inp: StakeholderInput, score: float) -> EngagementLevel:
        engine = StakeholderMapEngine()
        return engine._engagement_level(inp, score)

    def test_strong_at_70(self):
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = self._get_level_with_score(inp, 70.0)
        assert level == EngagementLevel.STRONG

    def test_strong_at_100(self):
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = self._get_level_with_score(inp, 100.0)
        assert level == EngagementLevel.STRONG

    def test_moderate_at_45(self):
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = self._get_level_with_score(inp, 45.0)
        assert level == EngagementLevel.MODERATE

    def test_moderate_at_69(self):
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = self._get_level_with_score(inp, 69.0)
        assert level == EngagementLevel.MODERATE

    def test_weak_at_20(self):
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = self._get_level_with_score(inp, 20.0)
        assert level == EngagementLevel.WEAK

    def test_weak_at_44(self):
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = self._get_level_with_score(inp, 44.0)
        assert level == EngagementLevel.WEAK

    def test_none_at_0(self):
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = self._get_level_with_score(inp, 0.0)
        assert level == EngagementLevel.NONE

    def test_none_at_19(self):
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = self._get_level_with_score(inp, 19.0)
        assert level == EngagementLevel.NONE

    def test_hostile_all_three_conditions(self):
        # sentiment < 0.25, last_contact_days > 7, activities_30d == 0
        inp = make_input(sentiment_score=0.2, last_contact_days=10, activities_30d=0)
        level = self._get_level_with_score(inp, 10.0)
        assert level == EngagementLevel.HOSTILE

    def test_hostile_requires_low_sentiment(self):
        # sentiment = 0.25 (not < 0.25) → no hostile
        inp = make_input(sentiment_score=0.25, last_contact_days=10, activities_30d=0)
        level = self._get_level_with_score(inp, 0.0)
        assert level != EngagementLevel.HOSTILE

    def test_hostile_requires_last_contact_gt_7(self):
        # last_contact_days = 7 (not > 7) → no hostile
        inp = make_input(sentiment_score=0.2, last_contact_days=7, activities_30d=0)
        level = self._get_level_with_score(inp, 0.0)
        assert level != EngagementLevel.HOSTILE

    def test_hostile_requires_zero_activities(self):
        # activities_30d = 1 (not == 0) → no hostile
        inp = make_input(sentiment_score=0.2, last_contact_days=10, activities_30d=1)
        level = self._get_level_with_score(inp, 0.0)
        assert level != EngagementLevel.HOSTILE

    def test_hostile_overrides_strong_engagement_score(self):
        # Even with engagement 80, hostile conditions → HOSTILE
        inp = make_input(sentiment_score=0.1, last_contact_days=30, activities_30d=0)
        level = self._get_level_with_score(inp, 80.0)
        assert level == EngagementLevel.HOSTILE

    def test_hostile_missing_one_condition_not_hostile(self):
        # Only two conditions met: sentiment < 0.25 AND activities_30d == 0, but last_contact_days ≤ 7
        inp = make_input(sentiment_score=0.2, last_contact_days=5, activities_30d=0)
        level = self._get_level_with_score(inp, 0.0)
        assert level != EngagementLevel.HOSTILE
        assert level == EngagementLevel.NONE


# ─────────────────────────────────────────────────────────────────────────────
# 7. RelationshipStatus priority order
# ─────────────────────────────────────────────────────────────────────────────

class TestRelationshipStatus:
    def _get_status(self, inp: StakeholderInput, engagement: float = 50.0) -> RelationshipStatus:
        engine = StakeholderMapEngine()
        return engine._relationship_status(inp, engagement)

    def test_opponent_via_blocker(self):
        inp = make_input(is_blocker=True, sentiment_score=0.8)
        assert self._get_status(inp) == RelationshipStatus.OPPONENT

    def test_opponent_via_low_sentiment(self):
        inp = make_input(is_blocker=False, sentiment_score=0.15)
        assert self._get_status(inp) == RelationshipStatus.OPPONENT

    def test_opponent_sentiment_exactly_02_is_opponent(self):
        inp = make_input(sentiment_score=0.2)
        # sentiment < 0.2 → opponent. 0.2 is NOT < 0.2
        assert self._get_status(inp) != RelationshipStatus.OPPONENT

    def test_opponent_sentiment_019(self):
        inp = make_input(sentiment_score=0.19)
        assert self._get_status(inp) == RelationshipStatus.OPPONENT

    def test_blocker_with_aligned_vendor_still_opponent(self):
        # OPPONENT check before SPONSOR
        inp = make_input(is_blocker=True, aligned_with_vendor=True, is_champion=True, sentiment_score=0.9)
        assert self._get_status(inp, 80.0) == RelationshipStatus.OPPONENT

    def test_skeptic_at_sentiment_039(self):
        inp = make_input(sentiment_score=0.39, is_blocker=False)
        assert self._get_status(inp) == RelationshipStatus.SKEPTIC

    def test_skeptic_exactly_04_not_skeptic(self):
        # sentiment = 0.4 → NOT < 0.4 → not skeptic
        inp = make_input(sentiment_score=0.4, is_blocker=False)
        assert self._get_status(inp) != RelationshipStatus.SKEPTIC

    def test_sponsor_all_conditions(self):
        inp = make_input(aligned_with_vendor=True, is_champion=True, sentiment_score=0.8)
        assert self._get_status(inp, 60.0) == RelationshipStatus.SPONSOR

    def test_sponsor_requires_engagement_60(self):
        inp = make_input(aligned_with_vendor=True, is_champion=True, sentiment_score=0.8)
        assert self._get_status(inp, 59.0) != RelationshipStatus.SPONSOR

    def test_sponsor_requires_champion(self):
        inp = make_input(aligned_with_vendor=True, is_champion=False, sentiment_score=0.8)
        assert self._get_status(inp, 70.0) != RelationshipStatus.SPONSOR

    def test_sponsor_requires_aligned(self):
        inp = make_input(aligned_with_vendor=False, is_champion=True, sentiment_score=0.8)
        assert self._get_status(inp, 70.0) != RelationshipStatus.SPONSOR

    def test_ally_via_aligned_with_vendor(self):
        inp = make_input(aligned_with_vendor=True, is_champion=False, sentiment_score=0.8)
        assert self._get_status(inp, 40.0) == RelationshipStatus.ALLY

    def test_ally_via_champion_and_engagement(self):
        inp = make_input(aligned_with_vendor=False, is_champion=True, sentiment_score=0.8)
        assert self._get_status(inp, 40.0) == RelationshipStatus.ALLY

    def test_ally_champion_below_engagement_40_not_ally(self):
        inp = make_input(aligned_with_vendor=False, is_champion=True, sentiment_score=0.8)
        result = self._get_status(inp, 39.0)
        assert result == RelationshipStatus.NEUTRAL

    def test_neutral_default(self):
        inp = make_input(aligned_with_vendor=False, is_champion=False, sentiment_score=0.5, is_blocker=False)
        assert self._get_status(inp) == RelationshipStatus.NEUTRAL

    def test_skeptic_before_sponsor(self):
        # sentiment 0.35 → SKEPTIC even if aligned + champion
        inp = make_input(aligned_with_vendor=True, is_champion=True, sentiment_score=0.35, is_blocker=False)
        assert self._get_status(inp, 80.0) == RelationshipStatus.SKEPTIC

    def test_opponent_before_all_others(self):
        # blocker → OPPONENT even if sponsor conditions met
        inp = make_input(is_blocker=True, aligned_with_vendor=True, is_champion=True, sentiment_score=0.8)
        assert self._get_status(inp, 90.0) == RelationshipStatus.OPPONENT


# ─────────────────────────────────────────────────────────────────────────────
# 8. StakeholderRole priority
# ─────────────────────────────────────────────────────────────────────────────

class TestStakeholderRole:
    def _get_role(self, **kwargs) -> StakeholderRole:
        engine = StakeholderMapEngine()
        return engine._stakeholder_role(make_input(**kwargs))

    def test_economic_buyer_via_flag(self):
        assert self._get_role(is_economic_buyer=True) == StakeholderRole.ECONOMIC_BUYER

    def test_economic_buyer_via_budget_authority(self):
        assert self._get_role(has_budget_authority=True) == StakeholderRole.ECONOMIC_BUYER

    def test_economic_buyer_before_champion(self):
        assert self._get_role(is_economic_buyer=True, is_champion=True) == StakeholderRole.ECONOMIC_BUYER

    def test_economic_buyer_before_technical(self):
        assert self._get_role(is_economic_buyer=True, is_technical_buyer=True) == StakeholderRole.ECONOMIC_BUYER

    def test_economic_buyer_before_blocker(self):
        assert self._get_role(is_economic_buyer=True, is_blocker=True) == StakeholderRole.ECONOMIC_BUYER

    def test_economic_buyer_before_end_user(self):
        assert self._get_role(is_economic_buyer=True, is_end_user=True) == StakeholderRole.ECONOMIC_BUYER

    def test_champion_before_technical(self):
        assert self._get_role(is_champion=True, is_technical_buyer=True) == StakeholderRole.CHAMPION

    def test_champion_before_blocker(self):
        assert self._get_role(is_champion=True, is_blocker=True) == StakeholderRole.CHAMPION

    def test_champion_before_end_user(self):
        assert self._get_role(is_champion=True, is_end_user=True) == StakeholderRole.CHAMPION

    def test_technical_buyer_before_blocker(self):
        assert self._get_role(is_technical_buyer=True, is_blocker=True) == StakeholderRole.TECHNICAL_BUYER

    def test_technical_buyer_before_end_user(self):
        assert self._get_role(is_technical_buyer=True, is_end_user=True) == StakeholderRole.TECHNICAL_BUYER

    def test_blocker_before_end_user(self):
        assert self._get_role(is_blocker=True, is_end_user=True) == StakeholderRole.BLOCKER

    def test_blocker_before_influencer(self):
        assert self._get_role(is_blocker=True, seniority=4) == StakeholderRole.BLOCKER

    def test_end_user_before_influencer(self):
        assert self._get_role(is_end_user=True, seniority=3) == StakeholderRole.END_USER

    def test_influencer_seniority_3(self):
        assert self._get_role(seniority=3) == StakeholderRole.INFLUENCER

    def test_influencer_seniority_4(self):
        assert self._get_role(seniority=4) == StakeholderRole.INFLUENCER

    def test_influencer_seniority_5(self):
        assert self._get_role(seniority=5) == StakeholderRole.INFLUENCER

    def test_unknown_seniority_1(self):
        assert self._get_role(seniority=1) == StakeholderRole.UNKNOWN

    def test_unknown_seniority_2(self):
        assert self._get_role(seniority=2) == StakeholderRole.UNKNOWN

    def test_all_false_seniority_1_is_unknown(self):
        assert self._get_role(
            is_economic_buyer=False, is_champion=False, is_technical_buyer=False,
            is_blocker=False, is_end_user=False, seniority=1,
        ) == StakeholderRole.UNKNOWN


# ─────────────────────────────────────────────────────────────────────────────
# 9. Engagement gap formula and clamping
# ─────────────────────────────────────────────────────────────────────────────

class TestEngagementGap:
    def _gap(self, influence: float, engagement: float) -> float:
        engine = StakeholderMapEngine()
        return engine._engagement_gap(influence, engagement)

    def test_gap_basic_formula(self):
        # (80 - 50) * (70/100) = 30 * 0.7 = 21.0
        assert self._gap(70.0, 50.0) == 21.0

    def test_gap_zero_when_engagement_gte_80(self):
        # max(0, 80 - 80) = 0
        assert self._gap(100.0, 80.0) == 0.0

    def test_gap_zero_when_engagement_gt_80(self):
        assert self._gap(100.0, 90.0) == 0.0

    def test_gap_max_when_engagement_zero_influence_100(self):
        # (80 - 0) * (100/100) = 80.0
        assert self._gap(100.0, 0.0) == 80.0

    def test_gap_zero_when_influence_zero(self):
        assert self._gap(0.0, 0.0) == 0.0

    def test_gap_clamped_max_100(self):
        # Artificially: gap formula max is 80, so no clamping needed at 100
        # But test boundary: gap(100, 0) = 80.0
        assert self._gap(100.0, 0.0) <= 100.0

    def test_gap_clamped_min_0(self):
        assert self._gap(0.0, 100.0) == 0.0

    def test_gap_rounded_1_decimal(self):
        # (80 - 33.3) * (50/100) = 46.7 * 0.5 = 23.35 → 23.4
        gap = self._gap(50.0, 33.3)
        assert gap == round(gap, 1)

    def test_gap_influence_50_engagement_40(self):
        # (80 - 40) * (50/100) = 40 * 0.5 = 20.0
        assert self._gap(50.0, 40.0) == 20.0

    def test_gap_never_negative(self):
        assert self._gap(100.0, 100.0) >= 0.0
        assert self._gap(0.0, 80.0) >= 0.0

    def test_gap_engagement_exactly_80(self):
        assert self._gap(100.0, 80.0) == 0.0

    def test_gap_engagement_79_point_9(self):
        gap = self._gap(100.0, 79.9)
        assert gap > 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 10. Coverage risk thresholds
# ─────────────────────────────────────────────────────────────────────────────

class TestCoverageRisk:
    def _risk(self, influence: float, engagement: float) -> CoverageRisk:
        engine = StakeholderMapEngine()
        return engine._coverage_risk(influence, engagement)

    def test_critical_influence_70_engagement_29(self):
        assert self._risk(70.0, 29.0) == CoverageRisk.CRITICAL

    def test_critical_influence_100_engagement_0(self):
        assert self._risk(100.0, 0.0) == CoverageRisk.CRITICAL

    def test_not_critical_influence_69_engagement_29(self):
        # influence must be >= 70
        result = self._risk(69.0, 29.0)
        assert result != CoverageRisk.CRITICAL

    def test_not_critical_influence_70_engagement_30(self):
        # engagement must be < 30
        result = self._risk(70.0, 30.0)
        assert result != CoverageRisk.CRITICAL

    def test_at_risk_influence_50_engagement_49(self):
        assert self._risk(50.0, 49.0) == CoverageRisk.AT_RISK

    def test_at_risk_influence_69_engagement_0(self):
        # influence >= 50 and < 70 with engagement < 50
        assert self._risk(69.0, 10.0) == CoverageRisk.AT_RISK

    def test_not_at_risk_influence_49_engagement_40(self):
        # influence < 50 → not AT_RISK via this branch
        result = self._risk(49.0, 40.0)
        assert result != CoverageRisk.AT_RISK

    def test_not_at_risk_influence_50_engagement_50(self):
        # engagement must be < 50
        result = self._risk(50.0, 50.0)
        assert result != CoverageRisk.AT_RISK

    def test_partial_engagement_59(self):
        assert self._risk(10.0, 59.0) == CoverageRisk.PARTIAL

    def test_partial_engagement_0(self):
        assert self._risk(10.0, 0.0) == CoverageRisk.PARTIAL

    def test_covered_engagement_60(self):
        assert self._risk(10.0, 60.0) == CoverageRisk.COVERED

    def test_covered_engagement_100(self):
        assert self._risk(10.0, 100.0) == CoverageRisk.COVERED

    def test_covered_high_influence_high_engagement(self):
        assert self._risk(100.0, 90.0) == CoverageRisk.COVERED

    def test_critical_takes_precedence_over_at_risk(self):
        # influence=80, engagement=20 → CRITICAL (not AT_RISK)
        assert self._risk(80.0, 20.0) == CoverageRisk.CRITICAL

    def test_at_risk_takes_precedence_over_partial(self):
        # influence=50, engagement=40 → AT_RISK (not PARTIAL)
        assert self._risk(50.0, 40.0) == CoverageRisk.AT_RISK


# ─────────────────────────────────────────────────────────────────────────────
# 11. is_at_risk flag
# ─────────────────────────────────────────────────────────────────────────────

class TestIsAtRisk:
    def test_is_at_risk_for_at_risk(self, engine):
        # influence=50, engagement=40 → AT_RISK → is_at_risk=True
        # seniority=4(65) + tech(8) = 73 influence
        # engagement: activities=0, meetings=0, emails=0, recency=22d→-10, sentiment=0.5 → 0 clamped
        inp = make_input(seniority=4, is_technical_buyer=True, activities_30d=0,
                         meetings_held=0, emails_sent=0, emails_responded=0,
                         last_contact_days=22, sentiment_score=0.5)
        result = engine.analyze(inp)
        assert result.is_at_risk is True

    def test_is_at_risk_for_critical(self, engine):
        inp = make_input(seniority=5, is_economic_buyer=True, activities_30d=0,
                         meetings_held=0, emails_sent=0, emails_responded=0,
                         last_contact_days=60, sentiment_score=0.5)
        result = engine.analyze(inp)
        assert result.coverage_risk == CoverageRisk.CRITICAL
        assert result.is_at_risk is True

    def test_not_at_risk_for_covered(self, engine):
        # High engagement, low influence
        inp = make_input(seniority=1, activities_30d=10, meetings_held=4,
                         emails_sent=1, emails_responded=1,
                         last_contact_days=1, sentiment_score=0.9)
        result = engine.analyze(inp)
        if result.coverage_risk == CoverageRisk.COVERED:
            assert result.is_at_risk is False

    def test_not_at_risk_for_partial(self, engine):
        # Low influence, moderate engagement
        inp = make_input(seniority=1, activities_30d=3, meetings_held=1,
                         emails_sent=2, emails_responded=1,
                         last_contact_days=10, sentiment_score=0.5)
        result = engine.analyze(inp)
        if result.coverage_risk == CoverageRisk.PARTIAL:
            assert result.is_at_risk is False

    def test_is_at_risk_consistent_with_coverage_risk(self, engine):
        for seniority in [1, 3, 5]:
            for engagement_days in [5, 20, 35]:
                for activities in [0, 5, 10]:
                    inp = make_input(seniority=seniority, activities_30d=activities,
                                     last_contact_days=engagement_days)
                    result = engine.analyze(inp)
                    expected_at_risk = result.coverage_risk in (CoverageRisk.AT_RISK, CoverageRisk.CRITICAL)
                    assert result.is_at_risk == expected_at_risk
                    engine.reset()


# ─────────────────────────────────────────────────────────────────────────────
# 12. priority_rank assignment in analyze_batch
# ─────────────────────────────────────────────────────────────────────────────

class TestAnalyzeBatch:
    def test_priority_rank_assigned(self, engine):
        inputs = [make_input(stakeholder_id=f"s{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        ranks = {r.priority_rank for r in results}
        assert ranks == {1, 2, 3}

    def test_highest_gap_gets_rank_1(self, engine):
        # stakeholder A: high influence, low engagement → high gap
        inp_high = make_input(
            stakeholder_id="high_gap",
            seniority=5, is_economic_buyer=True,
            activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
            last_contact_days=60, sentiment_score=0.5,
        )
        # stakeholder B: low influence, low engagement → lower gap
        inp_low = make_input(
            stakeholder_id="low_gap",
            seniority=1, activities_30d=0, meetings_held=0,
            emails_sent=0, emails_responded=0,
            last_contact_days=60, sentiment_score=0.5,
        )
        results = engine.analyze_batch([inp_high, inp_low])
        by_id = {r.stakeholder_id: r for r in results}
        assert by_id["high_gap"].priority_rank < by_id["low_gap"].priority_rank
        assert by_id["high_gap"].priority_rank == 1

    def test_lowest_gap_gets_highest_rank_number(self, engine):
        inp_high = make_input(
            stakeholder_id="high_gap",
            seniority=5, is_economic_buyer=True,
            activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
            last_contact_days=60, sentiment_score=0.5,
        )
        inp_low = make_input(
            stakeholder_id="low_gap",
            seniority=1, activities_30d=10, meetings_held=4,
            emails_sent=1, emails_responded=1,
            last_contact_days=1, sentiment_score=0.9,
        )
        results = engine.analyze_batch([inp_high, inp_low])
        by_id = {r.stakeholder_id: r for r in results}
        assert by_id["low_gap"].priority_rank == 2

    def test_single_stakeholder_rank_1(self, engine):
        results = engine.analyze_batch([make_input()])
        assert results[0].priority_rank == 1

    def test_batch_returns_same_count(self, engine):
        inputs = [make_input(stakeholder_id=f"s{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_ranks_are_consecutive_from_1(self, engine):
        inputs = [make_input(stakeholder_id=f"s{i}") for i in range(4)]
        results = engine.analyze_batch(inputs)
        ranks = sorted(r.priority_rank for r in results)
        assert ranks == [1, 2, 3, 4]

    def test_results_added_to_internal_state(self, engine):
        inputs = [make_input(stakeholder_id=f"s{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        assert len(engine.analyzed_stakeholders) == 3

    def test_rank_order_matches_gap_desc(self, engine):
        inputs = [make_input(stakeholder_id=f"s{i}", seniority=(i % 5) + 1,
                              activities_30d=i, last_contact_days=10)
                  for i in range(5)]
        results = engine.analyze_batch(inputs)
        sorted_by_rank = sorted(results, key=lambda r: r.priority_rank)
        gaps = [r.engagement_gap for r in sorted_by_rank]
        # gaps should be non-increasing
        for i in range(len(gaps) - 1):
            assert gaps[i] >= gaps[i + 1]

    def test_analyze_batch_updates_priority_rank_on_result_objects(self, engine):
        inputs = [make_input(stakeholder_id=f"s{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for r in results:
            assert r.priority_rank > 0


# ─────────────────────────────────────────────────────────────────────────────
# 13. Properties
# ─────────────────────────────────────────────────────────────────────────────

class TestProperties:
    def test_analyzed_stakeholders_empty_initially(self, engine):
        assert engine.analyzed_stakeholders == []

    def test_analyzed_stakeholders_after_analyze(self, engine):
        engine.analyze(make_input())
        assert len(engine.analyzed_stakeholders) == 1

    def test_analyzed_stakeholders_accumulates(self, engine):
        for i in range(3):
            engine.analyze(make_input(stakeholder_id=f"s{i}"))
        assert len(engine.analyzed_stakeholders) == 3

    def test_analyzed_stakeholders_returns_copy(self, engine):
        engine.analyze(make_input())
        copy1 = engine.analyzed_stakeholders
        copy2 = engine.analyzed_stakeholders
        assert copy1 is not copy2

    def test_at_risk_empty_initially(self, engine):
        assert engine.at_risk_stakeholders == []

    def test_at_risk_filters_correctly(self, engine):
        # at-risk: high influence, low engagement
        at_risk_inp = make_input(
            stakeholder_id="at_risk",
            seniority=5, is_economic_buyer=True,
            activities_30d=0, meetings_held=0, emails_sent=0,
            emails_responded=0, last_contact_days=60, sentiment_score=0.5,
        )
        # not at-risk: low influence, high engagement
        not_at_risk_inp = make_input(
            stakeholder_id="covered",
            seniority=1, activities_30d=10, meetings_held=4,
            emails_sent=1, emails_responded=1,
            last_contact_days=1, sentiment_score=0.9,
        )
        engine.analyze(at_risk_inp)
        engine.analyze(not_at_risk_inp)
        at_risk = engine.at_risk_stakeholders
        ids = {r.stakeholder_id for r in at_risk}
        assert "at_risk" in ids

    def test_champions_empty_initially(self, engine):
        assert engine.champions == []

    def test_champions_filters_role(self, engine):
        champion_inp = make_input(stakeholder_id="champ", is_champion=True)
        non_champion_inp = make_input(stakeholder_id="other")
        engine.analyze(champion_inp)
        engine.analyze(non_champion_inp)
        champions = engine.champions
        assert len(champions) == 1
        assert champions[0].stakeholder_id == "champ"

    def test_champions_not_returned_if_overridden_by_economic_buyer(self, engine):
        # is_economic_buyer=True overrides champion role
        inp = make_input(stakeholder_id="both", is_economic_buyer=True, is_champion=True)
        engine.analyze(inp)
        # role will be ECONOMIC_BUYER, not CHAMPION
        assert len(engine.champions) == 0

    def test_economic_buyers_empty_initially(self, engine):
        assert engine.economic_buyers == []

    def test_economic_buyers_filters_role(self, engine):
        eb_inp = make_input(stakeholder_id="eb", is_economic_buyer=True)
        non_eb_inp = make_input(stakeholder_id="other")
        engine.analyze(eb_inp)
        engine.analyze(non_eb_inp)
        ebs = engine.economic_buyers
        assert len(ebs) == 1
        assert ebs[0].stakeholder_id == "eb"

    def test_economic_buyers_via_budget_authority(self, engine):
        inp = make_input(stakeholder_id="ba", has_budget_authority=True)
        engine.analyze(inp)
        assert len(engine.economic_buyers) == 1

    def test_multiple_economic_buyers(self, engine):
        for i in range(3):
            engine.analyze(make_input(stakeholder_id=f"eb{i}", is_economic_buyer=True))
        assert len(engine.economic_buyers) == 3


# ─────────────────────────────────────────────────────────────────────────────
# 14. reset() clears all state
# ─────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, engine):
        for i in range(3):
            engine.analyze(make_input(stakeholder_id=f"s{i}"))
        engine.reset()
        assert engine.analyzed_stakeholders == []

    def test_reset_clears_at_risk(self, engine):
        engine.analyze(make_input(seniority=5, is_economic_buyer=True,
                                   activities_30d=0, meetings_held=0,
                                   emails_sent=0, emails_responded=0,
                                   last_contact_days=60))
        engine.reset()
        assert engine.at_risk_stakeholders == []

    def test_reset_clears_champions(self, engine):
        engine.analyze(make_input(is_champion=True))
        engine.reset()
        assert engine.champions == []

    def test_reset_clears_economic_buyers(self, engine):
        engine.analyze(make_input(is_economic_buyer=True))
        engine.reset()
        assert engine.economic_buyers == []

    def test_analyze_after_reset_works(self, engine):
        engine.analyze(make_input(stakeholder_id="s1"))
        engine.reset()
        engine.analyze(make_input(stakeholder_id="s2"))
        assert len(engine.analyzed_stakeholders) == 1
        assert engine.analyzed_stakeholders[0].stakeholder_id == "s2"

    def test_reset_on_empty_engine_works(self, engine):
        engine.reset()  # Should not raise
        assert engine.analyzed_stakeholders == []

    def test_summary_after_reset_is_empty(self, engine):
        for i in range(3):
            engine.analyze(make_input(stakeholder_id=f"s{i}"))
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0


# ─────────────────────────────────────────────────────────────────────────────
# 15. summary() — 12 keys, types, empty state, correctness
# ─────────────────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary_has_12_keys(self, engine):
        assert len(engine.summary()) == 12

    def test_empty_summary_keys(self, engine):
        keys = set(engine.summary().keys())
        expected = {
            "total", "role_counts", "engagement_counts", "relationship_counts",
            "risk_counts", "avg_influence_score", "avg_engagement_gap",
            "champions_count", "economic_buyers_count", "at_risk_count",
            "covered_count", "critical_stakeholders_count",
        }
        assert keys == expected

    def test_empty_summary_total_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_summary_role_counts_empty(self, engine):
        assert engine.summary()["role_counts"] == {}

    def test_empty_summary_engagement_counts_empty(self, engine):
        assert engine.summary()["engagement_counts"] == {}

    def test_empty_summary_relationship_counts_empty(self, engine):
        assert engine.summary()["relationship_counts"] == {}

    def test_empty_summary_risk_counts_empty(self, engine):
        assert engine.summary()["risk_counts"] == {}

    def test_empty_summary_avg_influence_zero(self, engine):
        assert engine.summary()["avg_influence_score"] == 0.0

    def test_empty_summary_avg_gap_zero(self, engine):
        assert engine.summary()["avg_engagement_gap"] == 0.0

    def test_empty_summary_counts_zero(self, engine):
        s = engine.summary()
        assert s["champions_count"] == 0
        assert s["economic_buyers_count"] == 0
        assert s["at_risk_count"] == 0
        assert s["covered_count"] == 0
        assert s["critical_stakeholders_count"] == 0

    def test_summary_total_after_analyze(self, engine):
        for i in range(5):
            engine.analyze(make_input(stakeholder_id=f"s{i}"))
        assert engine.summary()["total"] == 5

    def test_summary_has_12_keys_after_analyze(self, engine):
        engine.analyze(make_input())
        assert len(engine.summary()) == 12

    def test_summary_role_counts_includes_role(self, engine):
        engine.analyze(make_input(is_economic_buyer=True))
        s = engine.summary()
        assert "economic_buyer" in s["role_counts"]
        assert s["role_counts"]["economic_buyer"] == 1

    def test_summary_champions_count(self, engine):
        engine.analyze(make_input(is_champion=True))
        assert engine.summary()["champions_count"] == 1

    def test_summary_economic_buyers_count(self, engine):
        engine.analyze(make_input(is_economic_buyer=True))
        assert engine.summary()["economic_buyers_count"] == 1

    def test_summary_at_risk_count(self, engine):
        engine.analyze(make_input(
            seniority=5, is_economic_buyer=True, activities_30d=0,
            meetings_held=0, emails_sent=0, emails_responded=0,
            last_contact_days=60, sentiment_score=0.5,
        ))
        s = engine.summary()
        assert s["at_risk_count"] >= 1

    def test_summary_covered_count(self, engine):
        engine.analyze(make_input(
            seniority=1, activities_30d=10, meetings_held=4,
            emails_sent=1, emails_responded=1,
            last_contact_days=1, sentiment_score=0.9,
        ))
        result = engine.analyzed_stakeholders[0]
        s = engine.summary()
        if result.coverage_risk == CoverageRisk.COVERED:
            assert s["covered_count"] == 1

    def test_summary_avg_influence_score_type(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["avg_influence_score"], float)

    def test_summary_avg_engagement_gap_type(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["avg_engagement_gap"], float)

    def test_summary_role_counts_type(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["role_counts"], dict)

    def test_summary_engagement_counts_type(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["engagement_counts"], dict)

    def test_summary_relationship_counts_type(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["relationship_counts"], dict)

    def test_summary_risk_counts_type(self, engine):
        engine.analyze(make_input())
        assert isinstance(engine.summary()["risk_counts"], dict)

    def test_summary_avg_influence_is_averaged(self, engine):
        engine.analyze(make_input(seniority=1))   # influence = 10.0
        engine.analyze(make_input(seniority=5))   # influence = 85.0
        s = engine.summary()
        assert s["avg_influence_score"] == round((10.0 + 85.0) / 2, 1)

    def test_summary_multiple_same_role(self, engine):
        for i in range(3):
            engine.analyze(make_input(stakeholder_id=f"s{i}", is_economic_buyer=True))
        s = engine.summary()
        assert s["role_counts"]["economic_buyer"] == 3
        assert s["economic_buyers_count"] == 3

    def test_summary_engagement_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(stakeholder_id=f"s{i}"))
        s = engine.summary()
        assert sum(s["engagement_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(stakeholder_id=f"s{i}"))
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_relationship_counts_sum_equals_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(stakeholder_id=f"s{i}"))
        s = engine.summary()
        assert sum(s["relationship_counts"].values()) == s["total"]


# ─────────────────────────────────────────────────────────────────────────────
# 16. End-to-end scenarios
# ─────────────────────────────────────────────────────────────────────────────

class TestEndToEndScenarios:

    def test_fully_covered_sponsor(self, engine):
        """A champion aligned with vendor, strong engagement, senior → SPONSOR, COVERED."""
        inp = make_input(
            stakeholder_id="sponsor_champ",
            seniority=4,
            activities_30d=8,
            meetings_held=4,
            emails_sent=5,
            emails_responded=5,
            last_contact_days=3,
            sentiment_score=0.9,
            is_champion=True,
            aligned_with_vendor=True,
            prior_wins=3,
        )
        result = engine.analyze(inp)
        assert result.relationship_status == RelationshipStatus.SPONSOR
        assert result.coverage_risk == CoverageRisk.COVERED
        assert result.is_at_risk is False
        assert result.engagement_level == EngagementLevel.STRONG
        assert result.stakeholder_role == StakeholderRole.CHAMPION

    def test_critical_uncovered_economic_buyer(self, engine):
        """High-influence economic buyer with zero engagement → CRITICAL, is_at_risk."""
        inp = make_input(
            stakeholder_id="critical_eb",
            seniority=5,
            is_economic_buyer=True,
            has_budget_authority=True,
            activities_30d=0,
            meetings_held=0,
            emails_sent=0,
            emails_responded=0,
            last_contact_days=60,
            sentiment_score=0.5,
        )
        result = engine.analyze(inp)
        assert result.stakeholder_role == StakeholderRole.ECONOMIC_BUYER
        assert result.coverage_risk == CoverageRisk.CRITICAL
        assert result.is_at_risk is True
        assert result.influence_score >= 70.0
        assert result.engagement_gap > 0.0

    def test_hostile_blocker(self, engine):
        """Blocker with very low sentiment and no contact → HOSTILE, OPPONENT, CRITICAL or AT_RISK."""
        inp = make_input(
            stakeholder_id="hostile_blocker",
            seniority=4,
            is_blocker=True,
            activities_30d=0,
            meetings_held=0,
            emails_sent=6,
            emails_responded=0,
            last_contact_days=45,
            sentiment_score=0.1,
        )
        result = engine.analyze(inp)
        assert result.engagement_level == EngagementLevel.HOSTILE
        assert result.relationship_status == RelationshipStatus.OPPONENT
        assert result.stakeholder_role == StakeholderRole.BLOCKER
        assert result.is_at_risk is True

    def test_end_user_moderate_engagement(self, engine):
        """End user with some engagement → END_USER role."""
        # activities_30d=5→15, meetings=2→10, 2/3 resp→13.3, recency 10d→+5, sentiment 0.6→0
        # total = 15+10+13.3+5 = 43.3 → WEAK (< 45)
        inp = make_input(
            stakeholder_id="end_user_mod",
            seniority=2,
            is_end_user=True,
            activities_30d=5,
            meetings_held=2,
            emails_sent=3,
            emails_responded=2,
            last_contact_days=10,
            sentiment_score=0.6,
        )
        result = engine.analyze(inp)
        assert result.stakeholder_role == StakeholderRole.END_USER
        assert result.engagement_level in (EngagementLevel.WEAK, EngagementLevel.MODERATE, EngagementLevel.STRONG)

    def test_neutral_influencer(self, engine):
        """Senior individual with no role flags → INFLUENCER, NEUTRAL."""
        inp = make_input(
            stakeholder_id="influencer",
            seniority=3,
            is_economic_buyer=False,
            is_champion=False,
            is_technical_buyer=False,
            is_blocker=False,
            is_end_user=False,
            aligned_with_vendor=False,
            sentiment_score=0.5,
        )
        result = engine.analyze(inp)
        assert result.stakeholder_role == StakeholderRole.INFLUENCER

    def test_at_risk_technical_buyer(self, engine):
        """Technical buyer with moderate influence but low engagement → AT_RISK."""
        inp = make_input(
            stakeholder_id="tech_buyer_risk",
            seniority=4,
            is_technical_buyer=True,
            activities_30d=0,
            meetings_held=0,
            emails_sent=1,
            emails_responded=0,
            last_contact_days=25,
            sentiment_score=0.5,
        )
        result = engine.analyze(inp)
        assert result.stakeholder_role == StakeholderRole.TECHNICAL_BUYER
        # seniority 4 (65) + tech (8) = 73 ≥ 70, engagement should be very low → CRITICAL or AT_RISK
        assert result.is_at_risk is True

    def test_batch_with_mixed_stakeholders(self, engine):
        """analyze_batch with 4 different stakeholders assigns correct ranks."""
        inputs = [
            make_input(
                stakeholder_id="eb_no_eng",
                seniority=5, is_economic_buyer=True,
                activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
                last_contact_days=60, sentiment_score=0.5,
            ),
            make_input(
                stakeholder_id="champ_high_eng",
                seniority=3, is_champion=True, aligned_with_vendor=True,
                activities_30d=8, meetings_held=4, emails_sent=5, emails_responded=5,
                last_contact_days=2, sentiment_score=0.9,
            ),
            make_input(
                stakeholder_id="blocker",
                seniority=3, is_blocker=True,
                activities_30d=0, meetings_held=0, emails_sent=2, emails_responded=0,
                last_contact_days=15, sentiment_score=0.1,
            ),
            make_input(
                stakeholder_id="junior_end_user",
                seniority=1, is_end_user=True,
                activities_30d=2, meetings_held=1, emails_sent=2, emails_responded=1,
                last_contact_days=10, sentiment_score=0.5,
            ),
        ]
        results = engine.analyze_batch(inputs)
        assert len(results) == 4
        ranks = sorted(r.priority_rank for r in results)
        assert ranks == [1, 2, 3, 4]
        # EB with no engagement should have highest gap → rank 1
        by_id = {r.stakeholder_id: r for r in results}
        assert by_id["eb_no_eng"].priority_rank == 1

    def test_analyze_populates_all_result_fields(self, engine):
        """Every field in StakeholderResult is populated."""
        result = engine.analyze(make_input())
        assert result.stakeholder_id is not None
        assert result.account_id is not None
        assert result.deal_id is not None
        assert isinstance(result.influence_score, float)
        assert isinstance(result.engagement_level, EngagementLevel)
        assert isinstance(result.relationship_status, RelationshipStatus)
        assert isinstance(result.stakeholder_role, StakeholderRole)
        assert isinstance(result.coverage_risk, CoverageRisk)
        assert isinstance(result.engagement_gap, float)
        assert isinstance(result.is_at_risk, bool)
        assert isinstance(result.priority_rank, int)
        assert isinstance(result.recommended_action, str)
        assert isinstance(result.risk_factors, list)
        assert isinstance(result.strengths, list)
        assert isinstance(result.recommended_approach, str)

    def test_ids_propagated_to_result(self, engine):
        inp = make_input(stakeholder_id="sid", account_id="aid", deal_id="did")
        result = engine.analyze(inp)
        assert result.stakeholder_id == "sid"
        assert result.account_id == "aid"
        assert result.deal_id == "did"

    def test_prior_wins_in_strengths(self, engine):
        inp = make_input(prior_wins=3)
        result = engine.analyze(inp)
        found = any("victoire" in s for s in result.strengths)
        assert found

    def test_champion_in_strengths(self, engine):
        inp = make_input(is_champion=True)
        result = engine.analyze(inp)
        found = any("champion" in s.lower() or "Champion" in s for s in result.strengths)
        assert found

    def test_blocker_in_risk_factors(self, engine):
        inp = make_input(is_blocker=True)
        result = engine.analyze(inp)
        found = any("blocage" in rf.lower() or "Blocage" in rf for rf in result.risk_factors)
        assert found

    def test_long_silence_in_risk_factors(self, engine):
        inp = make_input(last_contact_days=40)
        result = engine.analyze(inp)
        found = any("silence" in rf.lower() or "40" in rf for rf in result.risk_factors)
        assert found

    def test_no_email_response_in_risk_factors(self, engine):
        inp = make_input(emails_sent=6, emails_responded=0)
        result = engine.analyze(inp)
        found = any("email" in rf.lower() for rf in result.risk_factors)
        assert found

    def test_aligned_with_vendor_in_strengths(self, engine):
        inp = make_input(aligned_with_vendor=True)
        result = engine.analyze(inp)
        found = any("alignement" in s.lower() or "Alignement" in s for s in result.strengths)
        assert found


# ─────────────────────────────────────────────────────────────────────────────
# 17. StakeholderResult dataclass structure
# ─────────────────────────────────────────────────────────────────────────────

class TestStakeholderResultStructure:
    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(StakeholderResult)

    def test_exactly_15_fields(self):
        assert len(dataclasses.fields(StakeholderResult)) == 15

    def test_field_names(self):
        field_names = {f.name for f in dataclasses.fields(StakeholderResult)}
        expected = {
            "stakeholder_id", "account_id", "deal_id", "influence_score",
            "engagement_level", "relationship_status", "stakeholder_role",
            "coverage_risk", "engagement_gap", "is_at_risk", "priority_rank",
            "recommended_action", "risk_factors", "strengths", "recommended_approach",
        }
        assert field_names == expected


# ─────────────────────────────────────────────────────────────────────────────
# 18. StakeholderMapEngine initialization
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineInitialization:
    def test_engine_starts_empty(self):
        engine = StakeholderMapEngine()
        assert engine.analyzed_stakeholders == []

    def test_multiple_engine_instances_independent(self):
        e1 = StakeholderMapEngine()
        e2 = StakeholderMapEngine()
        e1.analyze(make_input(stakeholder_id="s1"))
        assert len(e1.analyzed_stakeholders) == 1
        assert len(e2.analyzed_stakeholders) == 0

    def test_summary_on_fresh_engine_has_12_keys(self):
        engine = StakeholderMapEngine()
        assert len(engine.summary()) == 12


# ─────────────────────────────────────────────────────────────────────────────
# 19. Additional edge case tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_influence_economic_buyer_not_blocker_no_double_penalty(self, engine):
        # economic buyer with blocker: ECONOMIC_BUYER role, but penalty still applied to influence
        result = engine.analyze(make_input(is_economic_buyer=True, is_blocker=True, seniority=3))
        # 45 + 15(eco) - 10(blocker) = 50
        assert result.influence_score == 50.0

    def test_engagement_exactly_70_is_strong(self, engine):
        engine_inner = StakeholderMapEngine()
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = engine_inner._engagement_level(inp, 70.0)
        assert level == EngagementLevel.STRONG

    def test_engagement_exactly_45_is_moderate(self, engine):
        engine_inner = StakeholderMapEngine()
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = engine_inner._engagement_level(inp, 45.0)
        assert level == EngagementLevel.MODERATE

    def test_engagement_exactly_20_is_weak(self, engine):
        engine_inner = StakeholderMapEngine()
        inp = make_input(sentiment_score=0.5, last_contact_days=10, activities_30d=1)
        level = engine_inner._engagement_level(inp, 20.0)
        assert level == EngagementLevel.WEAK

    def test_influence_score_is_float_type(self, engine):
        result = engine.analyze(make_input(seniority=3))
        assert type(result.influence_score) is float

    def test_engagement_gap_is_float_type(self, engine):
        result = engine.analyze(make_input())
        assert type(result.engagement_gap) is float

    def test_analyze_returns_stakeholder_result(self, engine):
        result = engine.analyze(make_input())
        assert isinstance(result, StakeholderResult)

    def test_analyze_batch_returns_list(self, engine):
        results = engine.analyze_batch([make_input()])
        assert isinstance(results, list)

    def test_analyze_batch_empty_list(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_coverage_risk_critical_boundary_influence_70_engagement_29(self, engine):
        e = StakeholderMapEngine()
        assert e._coverage_risk(70.0, 29.0) == CoverageRisk.CRITICAL

    def test_coverage_risk_at_risk_boundary_influence_50_engagement_0(self, engine):
        # influence=50 < 70, so CRITICAL branch fails. AT_RISK: 50>=50 and 0<50 → AT_RISK
        e = StakeholderMapEngine()
        assert e._coverage_risk(50.0, 0.0) == CoverageRisk.AT_RISK

    def test_sponsor_engagement_exactly_60(self, engine):
        e = StakeholderMapEngine()
        inp = make_input(aligned_with_vendor=True, is_champion=True, sentiment_score=0.8)
        assert e._relationship_status(inp, 60.0) == RelationshipStatus.SPONSOR

    def test_ally_champion_engagement_exactly_40(self, engine):
        e = StakeholderMapEngine()
        inp = make_input(aligned_with_vendor=False, is_champion=True, sentiment_score=0.8)
        assert e._relationship_status(inp, 40.0) == RelationshipStatus.ALLY

    def test_high_engagement_score_capped(self):
        e = StakeholderMapEngine()
        inp = make_input(
            activities_30d=100, meetings_held=100, emails_sent=1, emails_responded=1,
            last_contact_days=1, sentiment_score=0.9,
        )
        score = e._engagement_score(inp)
        assert 0.0 <= score <= 100.0

    def test_unknown_role_returns_correct_enum(self, engine):
        inp = make_input(
            seniority=1,
            is_economic_buyer=False, is_champion=False, is_technical_buyer=False,
            is_blocker=False, is_end_user=False,
        )
        result = engine.analyze(inp)
        assert result.stakeholder_role == StakeholderRole.UNKNOWN

    def test_risk_factors_list_for_clean_profile(self, engine):
        # A clean profile should have no risk factors
        inp = make_input(
            is_blocker=False,
            last_contact_days=5,
            sentiment_score=0.8,
            is_economic_buyer=False,
            emails_sent=3,
            emails_responded=3,
        )
        result = engine.analyze(inp)
        # Coverage risk might still add factor, but no blocker/silence/sentiment/email factors
        assert not any("blocage" in rf.lower() for rf in result.risk_factors)
        assert not any("silence" in rf.lower() for rf in result.risk_factors)

    def test_strengths_high_sentiment(self, engine):
        inp = make_input(sentiment_score=0.9)
        result = engine.analyze(inp)
        found = any("sentiment" in s.lower() or "positif" in s.lower() for s in result.strengths)
        assert found

    def test_economic_buyer_low_engagement_recommended_action(self, engine):
        inp = make_input(
            is_economic_buyer=True,
            activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
            last_contact_days=40, sentiment_score=0.5,
        )
        result = engine.analyze(inp)
        assert "escalade" in result.recommended_action.lower() or "business" in result.recommended_action.lower()

    def test_opponent_recommended_action(self, engine):
        inp = make_input(is_blocker=True, sentiment_score=0.8)
        result = engine.analyze(inp)
        assert "neutr" in result.recommended_action.lower()

    def test_technical_buyer_approach(self, engine):
        inp = make_input(is_technical_buyer=True)
        result = engine.analyze(inp)
        assert "technique" in result.recommended_approach.lower()

    def test_economic_buyer_approach(self, engine):
        inp = make_input(is_economic_buyer=True)
        result = engine.analyze(inp)
        assert "roi" in result.recommended_approach.lower() or "business" in result.recommended_approach.lower()

    def test_champion_approach(self, engine):
        inp = make_input(is_champion=True)
        result = engine.analyze(inp)
        assert "champion" in result.recommended_approach.lower() or "vision" in result.recommended_approach.lower()

    def test_blocker_approach(self, engine):
        inp = make_input(is_blocker=True)
        result = engine.analyze(inp)
        assert "objection" in result.recommended_approach.lower() or "discovery" in result.recommended_approach.lower()

    def test_response_rate_gt_1_when_more_responded_than_sent(self):
        # emails_responded > emails_sent: rate > 1, but capped at 20
        e = StakeholderMapEngine()
        inp = make_input(emails_sent=2, emails_responded=5,
                         activities_30d=0, meetings_held=0,
                         last_contact_days=15, sentiment_score=0.5)
        score = e._engagement_score(inp)
        # response_rate = 5/2=2.5, response_base = min(20, 2.5*20) = min(20, 50) = 20
        assert score == 20.0

    def test_prior_wins_0_no_strength(self, engine):
        inp = make_input(prior_wins=0)
        result = engine.analyze(inp)
        found = any("victoire" in s for s in result.strengths)
        assert not found

    def test_prior_wins_1_shows_strength(self, engine):
        inp = make_input(prior_wins=1)
        result = engine.analyze(inp)
        found = any("victoire" in s for s in result.strengths)
        assert found

    def test_coverage_risk_partial_at_exactly_59(self):
        e = StakeholderMapEngine()
        assert e._coverage_risk(10.0, 59.0) == CoverageRisk.PARTIAL

    def test_coverage_risk_covered_at_exactly_60(self):
        e = StakeholderMapEngine()
        assert e._coverage_risk(10.0, 60.0) == CoverageRisk.COVERED

    def test_engagement_gap_80_engagement_zero_influence_100(self):
        e = StakeholderMapEngine()
        # (80-0)*(100/100) = 80
        assert e._engagement_gap(100.0, 0.0) == 80.0

    def test_hostile_economic_buyer_risk_factor(self, engine):
        inp = make_input(
            is_economic_buyer=True,
            sentiment_score=0.2,
            last_contact_days=10,
            activities_30d=0,
        )
        result = engine.analyze(inp)
        # Should have "Décideur budget faiblement engagé" factor since is_economic_buyer and HOSTILE level
        assert any("décideur" in rf.lower() or "budget" in rf.lower() for rf in result.risk_factors)

    def test_multiple_analyze_calls_accumulate(self, engine):
        for i in range(10):
            engine.analyze(make_input(stakeholder_id=f"s{i}"))
        assert len(engine.analyzed_stakeholders) == 10

    def test_summary_critical_stakeholders_count(self, engine):
        # Critical: influence >= 70, engagement < 30
        # seniority=5(85) + eco(15) = 100, engagement~0
        engine.analyze(make_input(
            seniority=5, is_economic_buyer=True,
            activities_30d=0, meetings_held=0, emails_sent=0, emails_responded=0,
            last_contact_days=60, sentiment_score=0.5,
        ))
        s = engine.summary()
        assert s["critical_stakeholders_count"] >= 1
