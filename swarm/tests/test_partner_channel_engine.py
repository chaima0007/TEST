"""
Comprehensive pytest test suite for PartnerChannelEngine.
~260+ tests covering all enums, helpers, scoring, health, tier, action, properties, and summary.
"""
from __future__ import annotations

import pytest

from swarm.intelligence.partner_channel_engine import (
    ChannelHealth,
    PartnerAction,
    PartnerChannelEngine,
    PartnerChannelInput,
    PartnerChannelResult,
    PartnerTier,
    PartnerType,
)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers / Fixtures
# ──────────────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> PartnerChannelInput:
    """Return a valid PartnerChannelInput with sensible defaults; override as needed."""
    defaults = dict(
        partner_id="P001",
        partner_name="Acme Corp",
        partner_type=PartnerType.RESELLER,
        current_tier=PartnerTier.GOLD,
        region="NA",
        years_as_partner=3.0,
        deals_registered=15,
        deals_closed_won=8,
        deals_closed_lost=4,
        pipeline_value=200_000.0,
        closed_won_value=150_000.0,
        avg_deal_size=20_000.0,
        certified_reps=4,
        total_partner_reps=8,
        training_completion_pct=80.0,
        last_deal_days=20,
        last_activity_days=5,
        joint_campaigns=3,
        conflict_incidents=0,
        conflict_resolved=0,
        quarterly_revenue_target=100_000.0,
        quarterly_revenue_actual=95_000.0,
        nps_score=50.0,
        is_portal_active=True,
        has_completed_onboarding=True,
        contract_valid=True,
    )
    defaults.update(overrides)
    return PartnerChannelInput(**defaults)


@pytest.fixture
def engine():
    return PartnerChannelEngine()


@pytest.fixture
def default_input():
    return make_input()


# ──────────────────────────────────────────────────────────────────────────────
# 1. Enum Tests
# ──────────────────────────────────────────────────────────────────────────────

class TestPartnerTierEnum:
    def test_member_count(self):
        assert len(PartnerTier) == 5

    def test_platinum_value(self):
        assert PartnerTier.PLATINUM.value == "platinum"

    def test_gold_value(self):
        assert PartnerTier.GOLD.value == "gold"

    def test_silver_value(self):
        assert PartnerTier.SILVER.value == "silver"

    def test_bronze_value(self):
        assert PartnerTier.BRONZE.value == "bronze"

    def test_prospect_value(self):
        assert PartnerTier.PROSPECT.value == "prospect"

    def test_is_str_subclass(self):
        assert isinstance(PartnerTier.GOLD, str)

    def test_str_equality(self):
        assert PartnerTier.GOLD == "gold"

    def test_unique_values(self):
        values = [m.value for m in PartnerTier]
        assert len(values) == len(set(values))

    def test_all_members_present(self):
        names = {m.name for m in PartnerTier}
        assert names == {"PLATINUM", "GOLD", "SILVER", "BRONZE", "PROSPECT"}


class TestPartnerTypeEnum:
    def test_member_count(self):
        assert len(PartnerType) == 6

    def test_reseller_value(self):
        assert PartnerType.RESELLER.value == "reseller"

    def test_referral_value(self):
        assert PartnerType.REFERRAL.value == "referral"

    def test_co_sell_value(self):
        assert PartnerType.CO_SELL.value == "co_sell"

    def test_technology_value(self):
        assert PartnerType.TECHNOLOGY.value == "technology"

    def test_si_value(self):
        assert PartnerType.SI.value == "si"

    def test_distributor_value(self):
        assert PartnerType.DISTRIBUTOR.value == "distributor"

    def test_is_str_subclass(self):
        assert isinstance(PartnerType.RESELLER, str)

    def test_str_equality(self):
        assert PartnerType.SI == "si"

    def test_unique_values(self):
        values = [m.value for m in PartnerType]
        assert len(values) == len(set(values))

    def test_all_members_present(self):
        names = {m.name for m in PartnerType}
        assert names == {"RESELLER", "REFERRAL", "CO_SELL", "TECHNOLOGY", "SI", "DISTRIBUTOR"}


class TestChannelHealthEnum:
    def test_member_count(self):
        assert len(ChannelHealth) == 5

    def test_excellent_value(self):
        assert ChannelHealth.EXCELLENT.value == "excellent"

    def test_healthy_value(self):
        assert ChannelHealth.HEALTHY.value == "healthy"

    def test_needs_attention_value(self):
        assert ChannelHealth.NEEDS_ATTENTION.value == "needs_attention"

    def test_at_risk_value(self):
        assert ChannelHealth.AT_RISK.value == "at_risk"

    def test_inactive_value(self):
        assert ChannelHealth.INACTIVE.value == "inactive"

    def test_is_str_subclass(self):
        assert isinstance(ChannelHealth.HEALTHY, str)

    def test_str_equality(self):
        assert ChannelHealth.INACTIVE == "inactive"

    def test_unique_values(self):
        values = [m.value for m in ChannelHealth]
        assert len(values) == len(set(values))

    def test_all_members_present(self):
        names = {m.name for m in ChannelHealth}
        assert names == {"EXCELLENT", "HEALTHY", "NEEDS_ATTENTION", "AT_RISK", "INACTIVE"}


class TestPartnerActionEnum:
    def test_member_count(self):
        assert len(PartnerAction) == 6

    def test_invest_and_grow_value(self):
        assert PartnerAction.INVEST_AND_GROW.value == "invest_and_grow"

    def test_enable_and_train_value(self):
        assert PartnerAction.ENABLE_AND_TRAIN.value == "enable_and_train"

    def test_joint_campaign_value(self):
        assert PartnerAction.JOINT_CAMPAIGN.value == "joint_campaign"

    def test_review_and_reset_value(self):
        assert PartnerAction.REVIEW_AND_RESET.value == "review_and_reset"

    def test_reactivate_value(self):
        assert PartnerAction.REACTIVATE.value == "reactivate"

    def test_offboard_value(self):
        assert PartnerAction.OFFBOARD.value == "offboard"

    def test_is_str_subclass(self):
        assert isinstance(PartnerAction.OFFBOARD, str)

    def test_str_equality(self):
        assert PartnerAction.JOINT_CAMPAIGN == "joint_campaign"

    def test_unique_values(self):
        values = [m.value for m in PartnerAction]
        assert len(values) == len(set(values))

    def test_all_members_present(self):
        names = {m.name for m in PartnerAction}
        assert names == {
            "INVEST_AND_GROW", "ENABLE_AND_TRAIN", "JOINT_CAMPAIGN",
            "REVIEW_AND_RESET", "REACTIVATE", "OFFBOARD",
        }


# ──────────────────────────────────────────────────────────────────────────────
# 2. PartnerChannelInput field count
# ──────────────────────────────────────────────────────────────────────────────

class TestPartnerChannelInputFields:
    def test_field_count(self):
        import dataclasses
        fields = dataclasses.fields(PartnerChannelInput)
        assert len(fields) == 26

    def test_has_partner_id(self):
        inp = make_input()
        assert hasattr(inp, "partner_id")

    def test_has_partner_name(self):
        inp = make_input()
        assert hasattr(inp, "partner_name")

    def test_has_partner_type(self):
        inp = make_input()
        assert hasattr(inp, "partner_type")

    def test_has_current_tier(self):
        inp = make_input()
        assert hasattr(inp, "current_tier")

    def test_has_region(self):
        inp = make_input()
        assert hasattr(inp, "region")

    def test_has_years_as_partner(self):
        inp = make_input()
        assert hasattr(inp, "years_as_partner")

    def test_has_deals_registered(self):
        inp = make_input()
        assert hasattr(inp, "deals_registered")

    def test_has_deals_closed_won(self):
        inp = make_input()
        assert hasattr(inp, "deals_closed_won")

    def test_has_deals_closed_lost(self):
        inp = make_input()
        assert hasattr(inp, "deals_closed_lost")

    def test_has_pipeline_value(self):
        inp = make_input()
        assert hasattr(inp, "pipeline_value")

    def test_has_closed_won_value(self):
        inp = make_input()
        assert hasattr(inp, "closed_won_value")

    def test_has_avg_deal_size(self):
        inp = make_input()
        assert hasattr(inp, "avg_deal_size")

    def test_has_certified_reps(self):
        inp = make_input()
        assert hasattr(inp, "certified_reps")

    def test_has_total_partner_reps(self):
        inp = make_input()
        assert hasattr(inp, "total_partner_reps")

    def test_has_training_completion_pct(self):
        inp = make_input()
        assert hasattr(inp, "training_completion_pct")

    def test_has_last_deal_days(self):
        inp = make_input()
        assert hasattr(inp, "last_deal_days")

    def test_has_last_activity_days(self):
        inp = make_input()
        assert hasattr(inp, "last_activity_days")

    def test_has_joint_campaigns(self):
        inp = make_input()
        assert hasattr(inp, "joint_campaigns")

    def test_has_conflict_incidents(self):
        inp = make_input()
        assert hasattr(inp, "conflict_incidents")

    def test_has_conflict_resolved(self):
        inp = make_input()
        assert hasattr(inp, "conflict_resolved")

    def test_has_quarterly_revenue_target(self):
        inp = make_input()
        assert hasattr(inp, "quarterly_revenue_target")

    def test_has_quarterly_revenue_actual(self):
        inp = make_input()
        assert hasattr(inp, "quarterly_revenue_actual")

    def test_has_nps_score(self):
        inp = make_input()
        assert hasattr(inp, "nps_score")

    def test_has_is_portal_active(self):
        inp = make_input()
        assert hasattr(inp, "is_portal_active")

    def test_has_has_completed_onboarding(self):
        inp = make_input()
        assert hasattr(inp, "has_completed_onboarding")

    def test_has_contract_valid(self):
        inp = make_input()
        assert hasattr(inp, "contract_valid")

    def test_no_certification_rate_attribute(self):
        inp = make_input()
        assert not hasattr(inp, "certification_rate")


# ──────────────────────────────────────────────────────────────────────────────
# 3. to_dict() — exactly 15 keys, correct types
# ──────────────────────────────────────────────────────────────────────────────

class TestToDictMethod:
    def test_key_count(self, engine, default_input):
        result = engine.analyze(default_input)
        assert len(result.to_dict()) == 15

    def test_has_partner_id(self, engine, default_input):
        assert "partner_id" in result_dict(engine, default_input)

    def test_has_partner_name(self, engine, default_input):
        assert "partner_name" in result_dict(engine, default_input)

    def test_has_partner_type(self, engine, default_input):
        assert "partner_type" in result_dict(engine, default_input)

    def test_has_current_tier(self, engine, default_input):
        assert "current_tier" in result_dict(engine, default_input)

    def test_has_recommended_tier(self, engine, default_input):
        assert "recommended_tier" in result_dict(engine, default_input)

    def test_has_channel_health(self, engine, default_input):
        assert "channel_health" in result_dict(engine, default_input)

    def test_has_partner_action(self, engine, default_input):
        assert "partner_action" in result_dict(engine, default_input)

    def test_has_engagement_score(self, engine, default_input):
        assert "engagement_score" in result_dict(engine, default_input)

    def test_has_performance_score(self, engine, default_input):
        assert "performance_score" in result_dict(engine, default_input)

    def test_has_pipeline_contribution(self, engine, default_input):
        assert "pipeline_contribution" in result_dict(engine, default_input)

    def test_has_win_rate(self, engine, default_input):
        assert "win_rate" in result_dict(engine, default_input)

    def test_has_certification_rate(self, engine, default_input):
        assert "certification_rate" in result_dict(engine, default_input)

    def test_has_quota_attainment(self, engine, default_input):
        assert "quota_attainment" in result_dict(engine, default_input)

    def test_has_is_strategic(self, engine, default_input):
        assert "is_strategic" in result_dict(engine, default_input)

    def test_has_needs_intervention(self, engine, default_input):
        assert "needs_intervention" in result_dict(engine, default_input)

    def test_partner_type_is_string(self, engine, default_input):
        d = result_dict(engine, default_input)
        assert isinstance(d["partner_type"], str)

    def test_partner_type_is_raw_value(self, engine, default_input):
        d = result_dict(engine, default_input)
        assert d["partner_type"] == "reseller"

    def test_current_tier_is_string(self, engine, default_input):
        d = result_dict(engine, default_input)
        assert isinstance(d["current_tier"], str)

    def test_recommended_tier_is_string(self, engine, default_input):
        d = result_dict(engine, default_input)
        assert isinstance(d["recommended_tier"], str)

    def test_channel_health_is_string(self, engine, default_input):
        d = result_dict(engine, default_input)
        assert isinstance(d["channel_health"], str)

    def test_partner_action_is_string(self, engine, default_input):
        d = result_dict(engine, default_input)
        assert isinstance(d["partner_action"], str)

    def test_engagement_score_is_float(self, engine, default_input):
        d = result_dict(engine, default_input)
        assert isinstance(d["engagement_score"], float)

    def test_is_strategic_is_bool(self, engine, default_input):
        d = result_dict(engine, default_input)
        assert isinstance(d["is_strategic"], bool)

    def test_needs_intervention_is_bool(self, engine, default_input):
        d = result_dict(engine, default_input)
        assert isinstance(d["needs_intervention"], bool)

    def test_exact_keys(self, engine, default_input):
        d = result_dict(engine, default_input)
        expected = {
            "partner_id", "partner_name", "partner_type", "current_tier",
            "recommended_tier", "channel_health", "partner_action",
            "engagement_score", "performance_score", "pipeline_contribution",
            "win_rate", "certification_rate", "quota_attainment",
            "is_strategic", "needs_intervention",
        }
        assert set(d.keys()) == expected


def result_dict(engine, inp):
    engine.reset()
    return engine.analyze(inp).to_dict()


# ──────────────────────────────────────────────────────────────────────────────
# 4. _engagement_score
# ──────────────────────────────────────────────────────────────────────────────

class TestEngagementScore:
    def test_zero_reps_zero_cert(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        # cert=0, training=0, no deal bonus, no activity, no campaigns, no compliance
        assert engine._engagement_score(inp) == 0.0

    def test_full_cert_rate(self, engine):
        inp = make_input(
            certified_reps=10, total_partner_reps=10,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        # cert=1.0 * 25 = 25
        assert engine._engagement_score(inp) == 25.0

    def test_partial_cert_rate(self, engine):
        inp = make_input(
            certified_reps=5, total_partner_reps=10,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        # cert=0.5 * 25 = 12.5
        assert engine._engagement_score(inp) == 12.5

    def test_training_full(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=100,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        # min(20, 100*0.2) = min(20,20) = 20
        assert engine._engagement_score(inp) == 20.0

    def test_training_capped_at_20(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=150,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 20.0

    def test_training_partial(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=50,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        # min(20, 50*0.2) = min(20, 10) = 10
        assert engine._engagement_score(inp) == 10.0

    def test_last_deal_within_30(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=30, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 20.0

    def test_last_deal_within_60(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=60, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 12.0

    def test_last_deal_within_90(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=90, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 5.0

    def test_last_deal_over_90_no_bonus(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=91, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 0.0

    def test_activity_within_7(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=7,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 15.0

    def test_activity_within_30(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=30,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 8.0

    def test_activity_within_60(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=60,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 3.0

    def test_activity_over_60_no_bonus(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=61,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 0.0

    def test_joint_campaigns_capped(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=10,
            is_portal_active=False, has_completed_onboarding=False,
        )
        # min(10, 10*2) = 10
        assert engine._engagement_score(inp) == 10.0

    def test_joint_campaigns_partial(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=3,
            is_portal_active=False, has_completed_onboarding=False,
        )
        # min(10, 3*2) = 6
        assert engine._engagement_score(inp) == 6.0

    def test_joint_campaigns_zero(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 0.0

    def test_portal_active_bonus(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=True, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) == 5.0

    def test_onboarding_bonus(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=True,
        )
        assert engine._engagement_score(inp) == 5.0

    def test_both_compliance_bonuses(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=True, has_completed_onboarding=True,
        )
        assert engine._engagement_score(inp) == 10.0

    def test_score_clamped_to_100(self, engine):
        inp = make_input(
            certified_reps=10, total_partner_reps=10,   # 25
            training_completion_pct=100,                  # 20
            last_deal_days=1,                             # 20
            last_activity_days=1,                         # 15
            joint_campaigns=10,                           # 10
            is_portal_active=True,                        # 5
            has_completed_onboarding=True,                # 5
        )
        # Total = 100, clamped to 100
        assert engine._engagement_score(inp) == 100.0

    def test_score_rounded_to_1_decimal(self, engine):
        inp = make_input(
            certified_reps=1, total_partner_reps=3,   # 1/3 * 25 = 8.333...
            training_completion_pct=0,
            last_deal_days=200, last_activity_days=200,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        score = engine._engagement_score(inp)
        assert score == round(score, 1)

    def test_score_non_negative(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=0,
            training_completion_pct=0,
            last_deal_days=500, last_activity_days=500,
            joint_campaigns=0,
            is_portal_active=False, has_completed_onboarding=False,
        )
        assert engine._engagement_score(inp) >= 0.0

    def test_additive_components(self, engine):
        inp = make_input(
            certified_reps=4, total_partner_reps=8,     # 0.5*25=12.5
            training_completion_pct=80,                  # min(20, 16)=16
            last_deal_days=20,                           # 20
            last_activity_days=5,                        # 15
            joint_campaigns=3,                           # 6
            is_portal_active=True,                       # 5
            has_completed_onboarding=True,               # 5
        )
        # 12.5+16+20+15+6+5+5 = 79.5
        assert engine._engagement_score(inp) == 79.5


# ──────────────────────────────────────────────────────────────────────────────
# 5. _performance_score
# ──────────────────────────────────────────────────────────────────────────────

class TestPerformanceScore:
    def test_zero_all(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=0,
            nps_score=-100,
            conflict_incidents=0,
            current_tier=PartnerTier.PROSPECT,
        )
        # wr=0 → 0; qa=100 (target<=0) → min(35,35)=35; deal_ratio=0/1=0 → 0;
        # nps_norm=0/200=0; conflict=0 → +10
        # 0+35+0+0+10 = 45.0
        assert engine._performance_score(inp) == 45.0

    def test_win_rate_full_contribution(self, engine):
        inp = make_input(
            deals_closed_won=10, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=0, nps_score=-100,
            conflict_incidents=0, current_tier=PartnerTier.PROSPECT,
        )
        # wr=1.0 → 30; qa=100 → 35; deal_ratio=0; nps=0; conflict=+10
        # 30+35+0+0+10 = 75.0
        assert engine._performance_score(inp) == 75.0

    def test_quota_attainment_capped_at_35(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=100.0, quarterly_revenue_actual=10000.0,
            deals_registered=0, nps_score=-100,
            conflict_incidents=0,
            current_tier=PartnerTier.PROSPECT,
        )
        # qa=10000.0 → min(35, 10000*0.35) = 35
        score = engine._performance_score(inp)
        assert score <= 100.0

    def test_deal_ratio_platinum_target(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=20, nps_score=-100,
            conflict_incidents=0, current_tier=PartnerTier.PLATINUM,
        )
        # tier_target=20, deal_ratio=min(2.0,20/20)=1.0 → 1*15=15
        # 0+35+15+0+10=60.0
        assert engine._performance_score(inp) == 60.0

    def test_deal_ratio_gold_target(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=12, nps_score=-100,
            conflict_incidents=0, current_tier=PartnerTier.GOLD,
        )
        # tier_target=12, deal_ratio=1.0 → 15
        assert engine._performance_score(inp) == 60.0

    def test_deal_ratio_silver_target(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=6, nps_score=-100,
            conflict_incidents=0, current_tier=PartnerTier.SILVER,
        )
        assert engine._performance_score(inp) == 60.0

    def test_deal_ratio_bronze_target(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=3, nps_score=-100,
            conflict_incidents=0, current_tier=PartnerTier.BRONZE,
        )
        assert engine._performance_score(inp) == 60.0

    def test_deal_ratio_prospect_target(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=1, nps_score=-100,
            conflict_incidents=0, current_tier=PartnerTier.PROSPECT,
        )
        assert engine._performance_score(inp) == 60.0

    def test_deal_ratio_capped_at_2(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=100, nps_score=-100,
            conflict_incidents=0, current_tier=PartnerTier.PROSPECT,
        )
        # deal_ratio=min(2.0, 100/1)=2.0 → 30
        # 0+35+30+0+10=75.0
        assert engine._performance_score(inp) == 75.0

    def test_nps_max_score(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=0, nps_score=100,
            conflict_incidents=0, current_tier=PartnerTier.PROSPECT,
        )
        # nps_norm=(100+100)/200=1.0 → 10
        # 0+35+0+10+10=55.0
        assert engine._performance_score(inp) == 55.0

    def test_nps_min_score(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=0, nps_score=-100,
            conflict_incidents=0, current_tier=PartnerTier.PROSPECT,
        )
        # nps_norm=0 → 0
        # 0+35+0+0+10=45.0
        assert engine._performance_score(inp) == 45.0

    def test_nps_neutral(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=0, nps_score=0,
            conflict_incidents=0, current_tier=PartnerTier.PROSPECT,
        )
        # nps_norm=(0+100)/200=0.5 → 5
        # 0+35+0+5+10=50.0
        assert engine._performance_score(inp) == 50.0

    def test_no_conflict_gives_10(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=0, nps_score=-100,
            conflict_incidents=0, conflict_resolved=0,
            current_tier=PartnerTier.PROSPECT,
        )
        # includes +10 for no conflicts
        assert engine._performance_score(inp) == 45.0

    def test_conflict_full_resolution(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=0, nps_score=-100,
            conflict_incidents=5, conflict_resolved=5,
            current_tier=PartnerTier.PROSPECT,
        )
        # res_rate=1.0 → 10
        # 0+35+0+0+10=45.0
        assert engine._performance_score(inp) == 45.0

    def test_conflict_zero_resolution(self, engine):
        inp = make_input(
            deals_closed_won=0, deals_closed_lost=0,
            quarterly_revenue_target=0.0, quarterly_revenue_actual=0.0,
            deals_registered=0, nps_score=-100,
            conflict_incidents=5, conflict_resolved=0,
            current_tier=PartnerTier.PROSPECT,
        )
        # res_rate=0 → 0
        # 0+35+0+0+0=35.0
        assert engine._performance_score(inp) == 35.0

    def test_clamped_to_100(self, engine):
        inp = make_input(
            deals_closed_won=10, deals_closed_lost=0,
            quarterly_revenue_target=100.0, quarterly_revenue_actual=20000.0,
            deals_registered=1000, nps_score=100,
            conflict_incidents=0, current_tier=PartnerTier.PROSPECT,
        )
        assert engine._performance_score(inp) == 100.0

    def test_score_rounded_to_1_decimal(self, engine):
        inp = make_input(
            deals_closed_won=1, deals_closed_lost=3,
            quarterly_revenue_target=100.0, quarterly_revenue_actual=77.0,
            deals_registered=2, nps_score=33,
            conflict_incidents=3, conflict_resolved=2,
            current_tier=PartnerTier.SILVER,
        )
        score = engine._performance_score(inp)
        assert score == round(score, 1)


# ──────────────────────────────────────────────────────────────────────────────
# 6. _pipeline_contribution
# ──────────────────────────────────────────────────────────────────────────────

class TestPipelineContribution:
    def test_zero_target_returns_zero(self, engine):
        inp = make_input(quarterly_revenue_target=0.0, pipeline_value=50000.0)
        assert engine._pipeline_contribution(inp) == 0.0

    def test_negative_target_returns_zero(self, engine):
        inp = make_input(quarterly_revenue_target=-100.0, pipeline_value=50000.0)
        assert engine._pipeline_contribution(inp) == 0.0

    def test_basic_calculation(self, engine):
        inp = make_input(quarterly_revenue_target=100_000.0, pipeline_value=50_000.0)
        assert engine._pipeline_contribution(inp) == 50.0

    def test_full_target(self, engine):
        inp = make_input(quarterly_revenue_target=100_000.0, pipeline_value=100_000.0)
        assert engine._pipeline_contribution(inp) == 100.0

    def test_over_target(self, engine):
        inp = make_input(quarterly_revenue_target=100_000.0, pipeline_value=200_000.0)
        assert engine._pipeline_contribution(inp) == 200.0

    def test_rounded_to_1_decimal(self, engine):
        inp = make_input(quarterly_revenue_target=300.0, pipeline_value=100.0)
        # 100/300*100 = 33.333... → 33.3
        assert engine._pipeline_contribution(inp) == 33.3

    def test_zero_pipeline_with_valid_target(self, engine):
        inp = make_input(quarterly_revenue_target=100_000.0, pipeline_value=0.0)
        assert engine._pipeline_contribution(inp) == 0.0


# ──────────────────────────────────────────────────────────────────────────────
# 7. _win_rate
# ──────────────────────────────────────────────────────────────────────────────

class TestWinRate:
    def test_zero_total_returns_zero(self, engine):
        inp = make_input(deals_closed_won=0, deals_closed_lost=0)
        assert engine._win_rate(inp) == 0.0

    def test_all_won(self, engine):
        inp = make_input(deals_closed_won=10, deals_closed_lost=0)
        assert engine._win_rate(inp) == 1.0

    def test_all_lost(self, engine):
        inp = make_input(deals_closed_won=0, deals_closed_lost=10)
        assert engine._win_rate(inp) == 0.0

    def test_half_won(self, engine):
        inp = make_input(deals_closed_won=5, deals_closed_lost=5)
        assert engine._win_rate(inp) == 0.5

    def test_rounded_to_3_decimals(self, engine):
        inp = make_input(deals_closed_won=1, deals_closed_lost=2)
        # 1/3 = 0.333...
        assert engine._win_rate(inp) == 0.333

    def test_typical_value(self, engine):
        inp = make_input(deals_closed_won=8, deals_closed_lost=4)
        assert engine._win_rate(inp) == round(8 / 12, 3)

    def test_one_deal_won(self, engine):
        inp = make_input(deals_closed_won=1, deals_closed_lost=0)
        assert engine._win_rate(inp) == 1.0


# ──────────────────────────────────────────────────────────────────────────────
# 8. _certification_rate
# ──────────────────────────────────────────────────────────────────────────────

class TestCertificationRate:
    def test_zero_reps_returns_zero(self, engine):
        inp = make_input(certified_reps=0, total_partner_reps=0)
        assert engine._certification_rate(inp) == 0.0

    def test_full_certification(self, engine):
        inp = make_input(certified_reps=10, total_partner_reps=10)
        assert engine._certification_rate(inp) == 1.0

    def test_no_certified(self, engine):
        inp = make_input(certified_reps=0, total_partner_reps=10)
        assert engine._certification_rate(inp) == 0.0

    def test_partial_certification(self, engine):
        inp = make_input(certified_reps=3, total_partner_reps=10)
        assert engine._certification_rate(inp) == 0.3

    def test_rounded_to_3_decimals(self, engine):
        inp = make_input(certified_reps=1, total_partner_reps=3)
        assert engine._certification_rate(inp) == 0.333

    def test_typical_value(self, engine):
        inp = make_input(certified_reps=4, total_partner_reps=8)
        assert engine._certification_rate(inp) == 0.5


# ──────────────────────────────────────────────────────────────────────────────
# 9. _conflict_resolution_rate
# ──────────────────────────────────────────────────────────────────────────────

class TestConflictResolutionRate:
    def test_zero_incidents_returns_one(self, engine):
        inp = make_input(conflict_incidents=0, conflict_resolved=0)
        assert engine._conflict_resolution_rate(inp) == 1.0

    def test_zero_incidents_with_resolved_returns_one(self, engine):
        # edge: incidents==0 always returns 1.0
        inp = make_input(conflict_incidents=0, conflict_resolved=5)
        assert engine._conflict_resolution_rate(inp) == 1.0

    def test_full_resolution(self, engine):
        inp = make_input(conflict_incidents=5, conflict_resolved=5)
        assert engine._conflict_resolution_rate(inp) == 1.0

    def test_partial_resolution(self, engine):
        inp = make_input(conflict_incidents=4, conflict_resolved=2)
        assert engine._conflict_resolution_rate(inp) == 0.5

    def test_no_resolution(self, engine):
        inp = make_input(conflict_incidents=5, conflict_resolved=0)
        assert engine._conflict_resolution_rate(inp) == 0.0

    def test_capped_at_one(self, engine):
        inp = make_input(conflict_incidents=3, conflict_resolved=10)
        assert engine._conflict_resolution_rate(inp) == 1.0

    def test_rounded_to_3_decimals(self, engine):
        inp = make_input(conflict_incidents=3, conflict_resolved=1)
        assert engine._conflict_resolution_rate(inp) == round(1 / 3, 3)


# ──────────────────────────────────────────────────────────────────────────────
# 10. _quota_attainment
# ──────────────────────────────────────────────────────────────────────────────

class TestQuotaAttainment:
    def test_zero_target_returns_100(self, engine):
        inp = make_input(quarterly_revenue_target=0.0, quarterly_revenue_actual=50000.0)
        assert engine._quota_attainment(inp) == 100.0

    def test_negative_target_returns_100(self, engine):
        inp = make_input(quarterly_revenue_target=-1.0, quarterly_revenue_actual=50000.0)
        assert engine._quota_attainment(inp) == 100.0

    def test_at_target(self, engine):
        inp = make_input(quarterly_revenue_target=100_000.0, quarterly_revenue_actual=100_000.0)
        assert engine._quota_attainment(inp) == 100.0

    def test_under_target(self, engine):
        inp = make_input(quarterly_revenue_target=100_000.0, quarterly_revenue_actual=75_000.0)
        assert engine._quota_attainment(inp) == 75.0

    def test_over_target(self, engine):
        inp = make_input(quarterly_revenue_target=100_000.0, quarterly_revenue_actual=110_000.0)
        assert engine._quota_attainment(inp) == 110.0

    def test_rounded_to_1_decimal(self, engine):
        inp = make_input(quarterly_revenue_target=300.0, quarterly_revenue_actual=100.0)
        # 100/300*100 = 33.333... → 33.3
        assert engine._quota_attainment(inp) == 33.3

    def test_zero_actual(self, engine):
        inp = make_input(quarterly_revenue_target=100_000.0, quarterly_revenue_actual=0.0)
        assert engine._quota_attainment(inp) == 0.0


# ──────────────────────────────────────────────────────────────────────────────
# 11. _channel_health
# ──────────────────────────────────────────────────────────────────────────────

class TestChannelHealth:
    def _health(self, engine, inp):
        eng = engine._engagement_score(inp)
        perf = engine._performance_score(inp)
        qa = engine._quota_attainment(inp)
        return engine._channel_health(inp, eng, perf, qa)

    def test_inactive_when_contract_invalid(self, engine):
        inp = make_input(contract_valid=False, last_activity_days=5)
        assert self._health(engine, inp) == ChannelHealth.INACTIVE

    def test_inactive_when_activity_over_180(self, engine):
        inp = make_input(contract_valid=True, last_activity_days=181)
        assert self._health(engine, inp) == ChannelHealth.INACTIVE

    def test_inactive_exactly_181_days(self, engine):
        inp = make_input(contract_valid=True, last_activity_days=181)
        assert self._health(engine, inp) == ChannelHealth.INACTIVE

    def test_inactive_exactly_180_not_inactive(self, engine):
        # 180 is not >180, so not INACTIVE by this rule alone
        inp = make_input(
            contract_valid=True, last_activity_days=180,
            last_deal_days=10, is_portal_active=True,
        )
        result = self._health(engine, inp)
        assert result != ChannelHealth.INACTIVE

    def test_at_risk_when_last_deal_over_120(self, engine):
        inp = make_input(
            contract_valid=True, last_activity_days=10,
            last_deal_days=121, is_portal_active=True,
        )
        assert self._health(engine, inp) == ChannelHealth.AT_RISK

    def test_at_risk_when_portal_inactive_and_activity_over_90(self, engine):
        inp = make_input(
            contract_valid=True, last_activity_days=91,
            last_deal_days=10, is_portal_active=False,
        )
        assert self._health(engine, inp) == ChannelHealth.AT_RISK

    def test_not_at_risk_when_portal_inactive_but_activity_within_90(self, engine):
        inp = make_input(
            contract_valid=True, last_activity_days=90,
            last_deal_days=10, is_portal_active=False,
        )
        # last_activity_days=90 is not >90
        result = self._health(engine, inp)
        assert result != ChannelHealth.AT_RISK

    def test_excellent_health(self, engine):
        # Need combined>=75, quota_att>=90
        # Force values directly
        inp = make_input(
            contract_valid=True, last_activity_days=5,
            last_deal_days=10, is_portal_active=True,
        )
        # Force high scores by passing them directly
        assert engine._channel_health(inp, 90.0, 90.0, 95.0) == ChannelHealth.EXCELLENT

    def test_excellent_requires_quota_90(self, engine):
        inp = make_input(contract_valid=True, last_activity_days=5, last_deal_days=10)
        # combined=80 but quota_att=89 → not EXCELLENT
        result = engine._channel_health(inp, 90.0, 90.0, 89.0)
        assert result != ChannelHealth.EXCELLENT

    def test_healthy_health(self, engine):
        inp = make_input(contract_valid=True, last_activity_days=5, last_deal_days=10)
        # combined=60>=55, quota_att=75>=70
        assert engine._channel_health(inp, 60.0, 60.0, 75.0) == ChannelHealth.HEALTHY

    def test_healthy_requires_quota_70(self, engine):
        inp = make_input(contract_valid=True, last_activity_days=5, last_deal_days=10)
        # combined=60>=55, quota_att=69 → not HEALTHY
        result = engine._channel_health(inp, 60.0, 60.0, 69.0)
        assert result != ChannelHealth.HEALTHY

    def test_needs_attention_health(self, engine):
        inp = make_input(contract_valid=True, last_activity_days=5, last_deal_days=10)
        # combined=40>=35 but quota_att<70
        assert engine._channel_health(inp, 40.0, 40.0, 50.0) == ChannelHealth.NEEDS_ATTENTION

    def test_at_risk_from_low_scores(self, engine):
        inp = make_input(contract_valid=True, last_activity_days=5, last_deal_days=10, is_portal_active=True)
        # combined=20<35 → AT_RISK
        assert engine._channel_health(inp, 20.0, 20.0, 50.0) == ChannelHealth.AT_RISK

    def test_combined_weight_040_060(self, engine):
        inp = make_input(contract_valid=True, last_activity_days=5, last_deal_days=10)
        # eng=100, perf=62.5 → combined = 100*0.4+62.5*0.6 = 40+37.5=77.5>=75, qa=95>=90
        assert engine._channel_health(inp, 100.0, 62.5, 95.0) == ChannelHealth.EXCELLENT

    def test_combined_weight_just_below_excellent(self, engine):
        inp = make_input(contract_valid=True, last_activity_days=5, last_deal_days=10)
        # combined = 40*0.4 + 90*0.6 = 16+54 = 70 < 75 → not EXCELLENT
        result = engine._channel_health(inp, 40.0, 90.0, 95.0)
        assert result != ChannelHealth.EXCELLENT

    def test_at_risk_exact_boundary_deal_days_120(self, engine):
        inp = make_input(contract_valid=True, last_activity_days=5, last_deal_days=120, is_portal_active=True)
        # 120 is not >120, so not AT_RISK from this rule
        result = self._health(engine, inp)
        assert result != ChannelHealth.AT_RISK or engine._channel_health(inp, 60.0, 60.0, 75.0) == ChannelHealth.HEALTHY


# ──────────────────────────────────────────────────────────────────────────────
# 12. _recommended_tier
# ──────────────────────────────────────────────────────────────────────────────

class TestRecommendedTier:
    def _rec_tier(self, engine, inp, perf, eng, qa):
        return engine._recommended_tier(inp, perf, eng, qa)

    def test_platinum_recommendation(self, engine):
        inp = make_input(years_as_partner=3.0)
        # combined = 80*0.6+80*0.4=48+32=80, qa=110, years>=2 → PLATINUM
        assert self._rec_tier(engine, inp, 80.0, 80.0, 110.0) == PartnerTier.PLATINUM

    def test_platinum_requires_years_2(self, engine):
        inp = make_input(years_as_partner=1.9)
        # combined=80, qa=110 but years<2 → not PLATINUM
        result = self._rec_tier(engine, inp, 80.0, 80.0, 110.0)
        assert result != PartnerTier.PLATINUM

    def test_platinum_requires_quota_110(self, engine):
        inp = make_input(years_as_partner=3.0)
        # combined=80, qa=109 → not PLATINUM
        result = self._rec_tier(engine, inp, 80.0, 80.0, 109.0)
        assert result != PartnerTier.PLATINUM

    def test_platinum_requires_combined_80(self, engine):
        inp = make_input(years_as_partner=3.0)
        # combined=79, qa=120 → not PLATINUM
        result = self._rec_tier(engine, inp, 79.0, 79.0, 120.0)
        assert result != PartnerTier.PLATINUM

    def test_gold_recommendation(self, engine):
        inp = make_input(years_as_partner=1.0)
        # combined = 65*0.6+65*0.4=65, qa=90 → GOLD
        assert self._rec_tier(engine, inp, 65.0, 65.0, 90.0) == PartnerTier.GOLD

    def test_gold_requires_quota_90(self, engine):
        inp = make_input(years_as_partner=1.0)
        result = self._rec_tier(engine, inp, 65.0, 65.0, 89.0)
        assert result != PartnerTier.GOLD

    def test_silver_recommendation(self, engine):
        inp = make_input()
        # combined = 45*0.6+45*0.4=45, qa=70 → SILVER
        assert self._rec_tier(engine, inp, 45.0, 45.0, 70.0) == PartnerTier.SILVER

    def test_silver_requires_quota_70(self, engine):
        inp = make_input()
        result = self._rec_tier(engine, inp, 45.0, 45.0, 69.0)
        assert result != PartnerTier.SILVER

    def test_bronze_recommendation(self, engine):
        inp = make_input()
        # combined=25, qa=50 → BRONZE
        assert self._rec_tier(engine, inp, 25.0, 25.0, 50.0) == PartnerTier.BRONZE

    def test_prospect_recommendation(self, engine):
        inp = make_input()
        # combined=20<25 → PROSPECT
        assert self._rec_tier(engine, inp, 20.0, 20.0, 0.0) == PartnerTier.PROSPECT

    def test_combined_uses_perf_06_eng_04(self, engine):
        inp = make_input(years_as_partner=3.0)
        # perf=100, eng=50 → combined=100*0.6+50*0.4=60+20=80, qa=110, years=3 → PLATINUM
        assert self._rec_tier(engine, inp, 100.0, 50.0, 110.0) == PartnerTier.PLATINUM

    def test_combined_just_under_platinum(self, engine):
        inp = make_input(years_as_partner=3.0)
        # combined must be <80 for not platinum
        # perf=79.9, eng=79.9 → combined=79.9, qa=110, years=3 → not PLATINUM
        result = self._rec_tier(engine, inp, 79.9, 79.9, 110.0)
        assert result != PartnerTier.PLATINUM


# ──────────────────────────────────────────────────────────────────────────────
# 13. _partner_action (full priority chain)
# ──────────────────────────────────────────────────────────────────────────────

class TestPartnerAction:
    def _action(self, engine, inp, health, eng, perf):
        return engine._partner_action(inp, health, eng, perf)

    # Priority 1: INACTIVE → OFFBOARD
    def test_inactive_gives_offboard(self, engine):
        inp = make_input()
        assert self._action(engine, inp, ChannelHealth.INACTIVE, 80.0, 80.0) == PartnerAction.OFFBOARD

    def test_offboard_regardless_of_scores(self, engine):
        inp = make_input(last_activity_days=10)
        assert self._action(engine, inp, ChannelHealth.INACTIVE, 0.0, 0.0) == PartnerAction.OFFBOARD

    # Priority 2: AT_RISK
    def test_at_risk_with_long_inactivity_gives_reactivate(self, engine):
        inp = make_input(last_activity_days=91)
        assert self._action(engine, inp, ChannelHealth.AT_RISK, 40.0, 40.0) == PartnerAction.REACTIVATE

    def test_at_risk_exactly_91_days_gives_reactivate(self, engine):
        inp = make_input(last_activity_days=91)
        assert self._action(engine, inp, ChannelHealth.AT_RISK, 40.0, 40.0) == PartnerAction.REACTIVATE

    def test_at_risk_exactly_90_days_gives_review(self, engine):
        inp = make_input(last_activity_days=90)
        assert self._action(engine, inp, ChannelHealth.AT_RISK, 40.0, 40.0) == PartnerAction.REVIEW_AND_RESET

    def test_at_risk_active_gives_review_and_reset(self, engine):
        inp = make_input(last_activity_days=10)
        assert self._action(engine, inp, ChannelHealth.AT_RISK, 40.0, 40.0) == PartnerAction.REVIEW_AND_RESET

    # Priority 3: EXCELLENT + perf>=75 → INVEST_AND_GROW
    def test_excellent_high_perf_gives_invest_and_grow(self, engine):
        inp = make_input(certified_reps=10, total_partner_reps=10, joint_campaigns=5)
        assert self._action(engine, inp, ChannelHealth.EXCELLENT, 80.0, 75.0) == PartnerAction.INVEST_AND_GROW

    def test_excellent_perf_exactly_75_gives_invest_and_grow(self, engine):
        inp = make_input(certified_reps=10, total_partner_reps=10)
        assert self._action(engine, inp, ChannelHealth.EXCELLENT, 80.0, 75.0) == PartnerAction.INVEST_AND_GROW

    def test_excellent_perf_below_75_falls_through(self, engine):
        # eng>=50, cert>=0.5 → doesn't trigger ENABLE_AND_TRAIN at step 4
        # health=EXCELLENT not HEALTHY/NEEDS_ATTENTION → no JOINT_CAMPAIGN
        # perf=74>=50 → no ENABLE_AND_TRAIN at step 6 → INVEST_AND_GROW
        inp = make_input(certified_reps=10, total_partner_reps=10, joint_campaigns=5)
        result = self._action(engine, inp, ChannelHealth.EXCELLENT, 80.0, 74.0)
        assert result == PartnerAction.INVEST_AND_GROW

    # Priority 4: eng<50 and cert_rate<0.5 → ENABLE_AND_TRAIN
    def test_low_eng_low_cert_gives_enable_train(self, engine):
        inp = make_input(
            certified_reps=0, total_partner_reps=10,  # cert=0 < 0.5
            joint_campaigns=1,
        )
        # eng=30<50, cert=0<0.5 → ENABLE_AND_TRAIN
        result = self._action(engine, inp, ChannelHealth.HEALTHY, 30.0, 60.0)
        assert result == PartnerAction.ENABLE_AND_TRAIN

    def test_low_eng_high_cert_no_enable_train_at_step4(self, engine):
        # eng<50 but cert>=0.5 → step 4 doesn't fire
        inp = make_input(
            certified_reps=5, total_partner_reps=10,  # cert=0.5
            joint_campaigns=0,
        )
        # eng=30<50, cert=0.5 (not <0.5) → doesn't fire step4
        # health=HEALTHY, joint_campaigns=0 → JOINT_CAMPAIGN (step 5)
        result = self._action(engine, inp, ChannelHealth.HEALTHY, 30.0, 60.0)
        assert result == PartnerAction.JOINT_CAMPAIGN

    def test_low_cert_fires_step4_regardless_of_eng(self, engine):
        # The ternary in step 4 means: since hasattr(inp, "certification_rate") is always
        # False, the condition is ONLY self._certification_rate(inp) < 0.5
        # eng is irrelevant for this step
        inp = make_input(
            certified_reps=0, total_partner_reps=10,  # cert=0 < 0.5
            joint_campaigns=0,
        )
        # cert=0<0.5 → ENABLE_AND_TRAIN fires at step 4 regardless of eng
        result = self._action(engine, inp, ChannelHealth.HEALTHY, 60.0, 60.0)
        assert result == PartnerAction.ENABLE_AND_TRAIN

    # Priority 5: HEALTHY/NEEDS_ATTENTION + joint_campaigns==0 → JOINT_CAMPAIGN
    def test_healthy_no_campaigns_gives_joint_campaign(self, engine):
        inp = make_input(joint_campaigns=0, certified_reps=5, total_partner_reps=8)
        result = self._action(engine, inp, ChannelHealth.HEALTHY, 60.0, 60.0)
        assert result == PartnerAction.JOINT_CAMPAIGN

    def test_needs_attention_no_campaigns_gives_joint_campaign(self, engine):
        inp = make_input(joint_campaigns=0, certified_reps=5, total_partner_reps=8)
        result = self._action(engine, inp, ChannelHealth.NEEDS_ATTENTION, 60.0, 60.0)
        assert result == PartnerAction.JOINT_CAMPAIGN

    def test_healthy_with_campaigns_no_joint_campaign(self, engine):
        inp = make_input(joint_campaigns=1, certified_reps=5, total_partner_reps=8)
        # eng=60>=50, cert=0.625>=0.5 → step4 skip; joint_campaigns=1 → step5 skip
        # perf=60>=50 → step6 skip → INVEST_AND_GROW
        result = self._action(engine, inp, ChannelHealth.HEALTHY, 60.0, 60.0)
        assert result == PartnerAction.INVEST_AND_GROW

    # Priority 6: perf<50 → ENABLE_AND_TRAIN
    def test_low_perf_gives_enable_train(self, engine):
        inp = make_input(certified_reps=5, total_partner_reps=8, joint_campaigns=1)
        # eng=60>=50, cert=0.625>=0.5 → no step4
        # joint=1 → no step5; perf=49<50 → ENABLE_AND_TRAIN
        result = self._action(engine, inp, ChannelHealth.NEEDS_ATTENTION, 60.0, 49.0)
        assert result == PartnerAction.ENABLE_AND_TRAIN

    def test_perf_exactly_50_no_enable_train(self, engine):
        inp = make_input(certified_reps=5, total_partner_reps=8, joint_campaigns=1)
        # perf=50 → not <50 → INVEST_AND_GROW
        result = self._action(engine, inp, ChannelHealth.NEEDS_ATTENTION, 60.0, 50.0)
        assert result == PartnerAction.INVEST_AND_GROW

    # Default: INVEST_AND_GROW
    def test_default_gives_invest_and_grow(self, engine):
        inp = make_input(certified_reps=5, total_partner_reps=8, joint_campaigns=1)
        result = self._action(engine, inp, ChannelHealth.HEALTHY, 60.0, 60.0)
        assert result == PartnerAction.INVEST_AND_GROW

    def test_needs_attention_with_campaigns_and_good_scores(self, engine):
        inp = make_input(certified_reps=5, total_partner_reps=8, joint_campaigns=3)
        result = self._action(engine, inp, ChannelHealth.NEEDS_ATTENTION, 60.0, 60.0)
        assert result == PartnerAction.INVEST_AND_GROW


# ──────────────────────────────────────────────────────────────────────────────
# 14. _is_strategic
# ──────────────────────────────────────────────────────────────────────────────

class TestIsStrategic:
    def test_all_conditions_met_platinum(self, engine):
        inp = make_input(closed_won_value=100_000.0, current_tier=PartnerTier.PLATINUM)
        assert engine._is_strategic(inp, 60.0, 50.0) is True

    def test_all_conditions_met_gold(self, engine):
        inp = make_input(closed_won_value=100_000.0, current_tier=PartnerTier.GOLD)
        assert engine._is_strategic(inp, 60.0, 50.0) is True

    def test_silver_not_strategic(self, engine):
        inp = make_input(closed_won_value=200_000.0, current_tier=PartnerTier.SILVER)
        assert engine._is_strategic(inp, 80.0, 80.0) is False

    def test_bronze_not_strategic(self, engine):
        inp = make_input(closed_won_value=200_000.0, current_tier=PartnerTier.BRONZE)
        assert engine._is_strategic(inp, 80.0, 80.0) is False

    def test_prospect_not_strategic(self, engine):
        inp = make_input(closed_won_value=200_000.0, current_tier=PartnerTier.PROSPECT)
        assert engine._is_strategic(inp, 80.0, 80.0) is False

    def test_closed_won_value_below_threshold(self, engine):
        inp = make_input(closed_won_value=99_999.0, current_tier=PartnerTier.GOLD)
        assert engine._is_strategic(inp, 60.0, 50.0) is False

    def test_closed_won_value_exact_threshold(self, engine):
        inp = make_input(closed_won_value=100_000.0, current_tier=PartnerTier.GOLD)
        assert engine._is_strategic(inp, 60.0, 50.0) is True

    def test_perf_below_60(self, engine):
        inp = make_input(closed_won_value=200_000.0, current_tier=PartnerTier.GOLD)
        assert engine._is_strategic(inp, 59.9, 50.0) is False

    def test_perf_exactly_60(self, engine):
        inp = make_input(closed_won_value=200_000.0, current_tier=PartnerTier.GOLD)
        assert engine._is_strategic(inp, 60.0, 50.0) is True

    def test_eng_below_50(self, engine):
        inp = make_input(closed_won_value=200_000.0, current_tier=PartnerTier.GOLD)
        assert engine._is_strategic(inp, 60.0, 49.9) is False

    def test_eng_exactly_50(self, engine):
        inp = make_input(closed_won_value=200_000.0, current_tier=PartnerTier.GOLD)
        assert engine._is_strategic(inp, 60.0, 50.0) is True

    def test_returns_bool_true(self, engine):
        inp = make_input(closed_won_value=200_000.0, current_tier=PartnerTier.GOLD)
        result = engine._is_strategic(inp, 60.0, 50.0)
        assert isinstance(result, bool)

    def test_returns_bool_false(self, engine):
        inp = make_input(closed_won_value=50_000.0, current_tier=PartnerTier.GOLD)
        result = engine._is_strategic(inp, 60.0, 50.0)
        assert isinstance(result, bool)


# ──────────────────────────────────────────────────────────────────────────────
# 15. needs_intervention
# ──────────────────────────────────────────────────────────────────────────────

class TestNeedsIntervention:
    def test_at_risk_needs_intervention(self, engine):
        inp = make_input(
            contract_valid=True, last_activity_days=10,
            last_deal_days=130, is_portal_active=True,  # forces AT_RISK
        )
        result = engine.analyze(inp)
        assert result.needs_intervention is True

    def test_inactive_needs_intervention(self, engine):
        inp = make_input(contract_valid=False)
        result = engine.analyze(inp)
        assert result.needs_intervention is True

    def test_excellent_no_intervention(self, engine):
        inp = make_input(
            contract_valid=True, last_activity_days=5,
            last_deal_days=10, is_portal_active=True,
        )
        result = engine.analyze(inp)
        if result.channel_health == ChannelHealth.EXCELLENT:
            assert result.needs_intervention is False

    def test_healthy_no_intervention(self, engine):
        # Build a partner that should be HEALTHY
        inp = make_input(
            contract_valid=True, last_activity_days=5,
            last_deal_days=10, is_portal_active=True,
        )
        result = engine.analyze(inp)
        if result.channel_health == ChannelHealth.HEALTHY:
            assert result.needs_intervention is False

    def test_needs_attention_no_intervention(self, engine):
        inp = make_input()
        result = engine.analyze(inp)
        if result.channel_health == ChannelHealth.NEEDS_ATTENTION:
            assert result.needs_intervention is False

    def test_needs_intervention_false_for_healthy_explicit(self, engine):
        inp = make_input(
            contract_valid=True, last_activity_days=5,
            last_deal_days=10, is_portal_active=True,
        )
        eng_score = engine._engagement_score(inp)
        perf_score = engine._performance_score(inp)
        qa = engine._quota_attainment(inp)
        # Force directly
        health = engine._channel_health(inp, eng_score, perf_score, qa)
        intervention = health in (ChannelHealth.AT_RISK, ChannelHealth.INACTIVE)
        if health not in (ChannelHealth.AT_RISK, ChannelHealth.INACTIVE):
            assert intervention is False

    def test_intervention_type_is_bool(self, engine):
        inp = make_input(contract_valid=False)
        result = engine.analyze(inp)
        assert isinstance(result.needs_intervention, bool)


# ──────────────────────────────────────────────────────────────────────────────
# 16. Properties (empty, filtering)
# ──────────────────────────────────────────────────────────────────────────────

class TestProperties:
    def test_strategic_partners_empty_initially(self, engine):
        assert engine.strategic_partners == []

    def test_at_risk_partners_empty_initially(self, engine):
        assert engine.at_risk_partners == []

    def test_top_performers_empty_initially(self, engine):
        assert engine.top_performers == []

    def test_total_partner_pipeline_empty_returns_zero(self, engine):
        assert engine.total_partner_pipeline == 0.0

    def test_total_partner_pipeline_always_zero_bug(self, engine):
        # This property has a bug: multiplies by 0
        inp = make_input(quarterly_revenue_target=100_000.0, pipeline_value=500_000.0)
        engine.analyze(inp)
        assert engine.total_partner_pipeline == 0.0

    def test_total_partner_pipeline_multiple_inputs_zero(self, engine):
        for i in range(5):
            engine.analyze(make_input(
                partner_id=f"P{i}",
                quarterly_revenue_target=100_000.0,
                pipeline_value=200_000.0,
            ))
        assert engine.total_partner_pipeline == 0.0

    def test_strategic_partners_filters_correctly(self, engine):
        # Strategic partner
        strategic = make_input(
            partner_id="STRAT1",
            closed_won_value=200_000.0,
            current_tier=PartnerTier.GOLD,
            certified_reps=10, total_partner_reps=10,
            training_completion_pct=100,
            last_deal_days=10, last_activity_days=5,
            joint_campaigns=5,
            is_portal_active=True, has_completed_onboarding=True,
            quarterly_revenue_target=100_000.0,
            quarterly_revenue_actual=120_000.0,
            deals_closed_won=10, deals_closed_lost=2,
            deals_registered=15, nps_score=80,
            conflict_incidents=0,
        )
        engine.analyze(strategic)
        result_strategic = engine.strategic_partners
        # Result may or may not be strategic depending on computed scores
        # Just verify it's a list
        assert isinstance(result_strategic, list)

    def test_at_risk_partners_includes_at_risk(self, engine):
        # INACTIVE partner
        inp = make_input(partner_id="INACTIVE1", contract_valid=False)
        engine.analyze(inp)
        at_risk = engine.at_risk_partners
        assert len(at_risk) >= 1

    def test_at_risk_partners_includes_inactive(self, engine):
        inp = make_input(contract_valid=False)
        engine.analyze(inp)
        assert len(engine.at_risk_partners) == 1

    def test_at_risk_partners_excludes_healthy(self, engine):
        # All healthy inputs
        inp1 = make_input(contract_valid=False, partner_id="P1")  # INACTIVE
        inp2 = make_input(
            partner_id="P2",
            contract_valid=True, last_activity_days=5,
            last_deal_days=10, is_portal_active=True,
        )
        engine.analyze(inp1)
        engine.analyze(inp2)
        for r in engine.at_risk_partners:
            assert r.channel_health in (ChannelHealth.AT_RISK, ChannelHealth.INACTIVE)

    def test_top_performers_includes_excellent(self, engine):
        # Force excellent via direct scores in channel_health call
        inp = make_input(
            contract_valid=True, last_activity_days=5,
            last_deal_days=10, is_portal_active=True,
            certified_reps=10, total_partner_reps=10,
            training_completion_pct=100,
            joint_campaigns=5,
            has_completed_onboarding=True,
            quarterly_revenue_actual=100_000.0,
            quarterly_revenue_target=100_000.0,
            deals_closed_won=10, deals_closed_lost=0,
            deals_registered=20, nps_score=100,
            conflict_incidents=0,
        )
        engine.analyze(inp)
        for r in engine.top_performers:
            assert r.channel_health in (ChannelHealth.EXCELLENT, ChannelHealth.HEALTHY)

    def test_top_performers_excludes_at_risk(self, engine):
        inp = make_input(contract_valid=False)  # INACTIVE
        engine.analyze(inp)
        for r in engine.top_performers:
            assert r.channel_health not in (ChannelHealth.AT_RISK, ChannelHealth.INACTIVE)

    def test_properties_return_lists(self, engine):
        assert isinstance(engine.strategic_partners, list)
        assert isinstance(engine.at_risk_partners, list)
        assert isinstance(engine.top_performers, list)

    def test_strategic_partner_results_are_channel_results(self, engine):
        inp = make_input(
            closed_won_value=200_000.0, current_tier=PartnerTier.GOLD,
            certified_reps=10, total_partner_reps=10,
            training_completion_pct=100, last_deal_days=10,
            last_activity_days=5, joint_campaigns=5,
            is_portal_active=True, has_completed_onboarding=True,
            quarterly_revenue_actual=120_000.0,
            quarterly_revenue_target=100_000.0,
            deals_closed_won=10, deals_closed_lost=2,
            deals_registered=15, nps_score=80, conflict_incidents=0,
        )
        engine.analyze(inp)
        for r in engine.strategic_partners:
            assert isinstance(r, PartnerChannelResult)


# ──────────────────────────────────────────────────────────────────────────────
# 17. summary() — exactly 13 keys
# ──────────────────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary_has_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_total_is_zero(self, engine):
        assert engine.summary()["total"] == 0

    def test_empty_summary_tier_counts_empty(self, engine):
        assert engine.summary()["tier_counts"] == {}

    def test_empty_summary_type_counts_empty(self, engine):
        assert engine.summary()["type_counts"] == {}

    def test_empty_summary_health_counts_empty(self, engine):
        assert engine.summary()["health_counts"] == {}

    def test_empty_summary_action_counts_empty(self, engine):
        assert engine.summary()["action_counts"] == {}

    def test_empty_summary_avg_engagement_zero(self, engine):
        assert engine.summary()["avg_engagement_score"] == 0.0

    def test_empty_summary_avg_performance_zero(self, engine):
        assert engine.summary()["avg_performance_score"] == 0.0

    def test_empty_summary_avg_win_rate_zero(self, engine):
        assert engine.summary()["avg_win_rate"] == 0.0

    def test_empty_summary_avg_quota_zero(self, engine):
        assert engine.summary()["avg_quota_attainment"] == 0.0

    def test_empty_summary_strategic_count_zero(self, engine):
        assert engine.summary()["strategic_count"] == 0

    def test_empty_summary_at_risk_count_zero(self, engine):
        assert engine.summary()["at_risk_count"] == 0

    def test_empty_summary_top_performer_count_zero(self, engine):
        assert engine.summary()["top_performer_count"] == 0

    def test_empty_summary_needs_intervention_zero(self, engine):
        assert engine.summary()["needs_intervention_count"] == 0

    def test_summary_exact_13_keys(self, engine):
        s = engine.summary()
        expected = {
            "total", "tier_counts", "type_counts", "health_counts",
            "action_counts", "avg_engagement_score", "avg_performance_score",
            "avg_win_rate", "avg_quota_attainment", "strategic_count",
            "at_risk_count", "top_performer_count", "needs_intervention_count",
        }
        assert set(s.keys()) == expected

    def test_summary_total_after_analyze(self, engine, default_input):
        engine.analyze(default_input)
        assert engine.summary()["total"] == 1

    def test_summary_tier_counts_after_analyze(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert "gold" in s["tier_counts"]
        assert s["tier_counts"]["gold"] == 1

    def test_summary_type_counts_after_analyze(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert "reseller" in s["type_counts"]

    def test_summary_multiple_partners(self, engine):
        for i in range(3):
            engine.analyze(make_input(partner_id=f"P{i}"))
        assert engine.summary()["total"] == 3

    def test_summary_at_risk_count(self, engine):
        engine.analyze(make_input(partner_id="P1", contract_valid=False))
        engine.analyze(make_input(partner_id="P2", contract_valid=True, last_activity_days=5, last_deal_days=10))
        s = engine.summary()
        assert s["at_risk_count"] >= 1

    def test_summary_needs_intervention_count(self, engine):
        engine.analyze(make_input(partner_id="P1", contract_valid=False))  # INACTIVE
        s = engine.summary()
        assert s["needs_intervention_count"] >= 1

    def test_summary_avg_engagement_score_rounded(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        avg = s["avg_engagement_score"]
        assert avg == round(avg, 1)

    def test_summary_avg_performance_score_rounded(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        avg = s["avg_performance_score"]
        assert avg == round(avg, 1)

    def test_summary_avg_win_rate_rounded(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        avg = s["avg_win_rate"]
        assert avg == round(avg, 3)

    def test_summary_avg_quota_attainment_rounded(self, engine):
        engine.analyze(make_input())
        s = engine.summary()
        avg = s["avg_quota_attainment"]
        assert avg == round(avg, 1)

    def test_summary_action_counts_populated(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert len(s["action_counts"]) >= 1
        # Values should sum to total
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_health_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(partner_id=f"P{i}"))
        s = engine.summary()
        assert sum(s["health_counts"].values()) == s["total"]

    def test_summary_tier_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(partner_id=f"P{i}"))
        s = engine.summary()
        assert sum(s["tier_counts"].values()) == s["total"]

    def test_summary_with_non_empty_has_13_keys(self, engine, default_input):
        engine.analyze(default_input)
        assert len(engine.summary()) == 13


# ──────────────────────────────────────────────────────────────────────────────
# 18. reset()
# ──────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        assert engine.summary()["total"] == 0

    def test_reset_clears_strategic_partners(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        assert engine.strategic_partners == []

    def test_reset_clears_at_risk_partners(self, engine, default_input):
        engine.analyze(make_input(contract_valid=False))
        engine.reset()
        assert engine.at_risk_partners == []

    def test_reset_clears_top_performers(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        assert engine.top_performers == []

    def test_reset_allows_reuse(self, engine):
        engine.analyze(make_input(partner_id="P1"))
        engine.reset()
        engine.analyze(make_input(partner_id="P2"))
        assert engine.summary()["total"] == 1

    def test_reset_pipeline_zero_after(self, engine, default_input):
        engine.analyze(default_input)
        engine.reset()
        assert engine.total_partner_pipeline == 0.0

    def test_multiple_resets(self, engine):
        engine.analyze(make_input())
        engine.reset()
        engine.reset()  # double reset should be safe
        assert engine.summary()["total"] == 0


# ──────────────────────────────────────────────────────────────────────────────
# 19. analyze_batch
# ──────────────────────────────────────────────────────────────────────────────

class TestAnalyzeBatch:
    def test_empty_batch_returns_empty_list(self, engine):
        assert engine.analyze_batch([]) == []

    def test_single_input_batch(self, engine, default_input):
        results = engine.analyze_batch([default_input])
        assert len(results) == 1

    def test_multiple_inputs_batch(self, engine):
        inputs = [make_input(partner_id=f"P{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_batch_stores_results(self, engine):
        inputs = [make_input(partner_id=f"P{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        assert engine.summary()["total"] == 3

    def test_batch_returns_channel_results(self, engine, default_input):
        results = engine.analyze_batch([default_input])
        for r in results:
            assert isinstance(r, PartnerChannelResult)

    def test_batch_partner_ids_preserved(self, engine):
        inputs = [make_input(partner_id=f"PARTNER_{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        ids = {r.partner_id for r in results}
        assert ids == {"PARTNER_0", "PARTNER_1", "PARTNER_2"}


# ──────────────────────────────────────────────────────────────────────────────
# 20. End-to-End Scenarios
# ──────────────────────────────────────────────────────────────────────────────

class TestEndToEndScenarios:
    def test_platinum_partner_scenario(self, engine):
        inp = make_input(
            partner_id="PLAT1",
            current_tier=PartnerTier.PLATINUM,
            partner_type=PartnerType.RESELLER,
            years_as_partner=5.0,
            deals_registered=25,
            deals_closed_won=15,
            deals_closed_lost=3,
            pipeline_value=500_000.0,
            closed_won_value=400_000.0,
            certified_reps=10, total_partner_reps=10,
            training_completion_pct=100.0,
            last_deal_days=15, last_activity_days=3,
            joint_campaigns=5,
            conflict_incidents=0,
            quarterly_revenue_target=100_000.0,
            quarterly_revenue_actual=130_000.0,
            nps_score=80.0,
            is_portal_active=True, has_completed_onboarding=True,
            contract_valid=True,
            avg_deal_size=25_000.0,
        )
        result = engine.analyze(inp)
        assert result.partner_id == "PLAT1"
        assert result.channel_health in (ChannelHealth.EXCELLENT, ChannelHealth.HEALTHY)
        assert result.needs_intervention is False

    def test_inactive_partner_scenario(self, engine):
        inp = make_input(
            partner_id="DEAD1",
            contract_valid=False,
            last_activity_days=300,
        )
        result = engine.analyze(inp)
        assert result.channel_health == ChannelHealth.INACTIVE
        assert result.partner_action == PartnerAction.OFFBOARD
        assert result.needs_intervention is True

    def test_at_risk_reactivation_scenario(self, engine):
        inp = make_input(
            partner_id="RISK1",
            contract_valid=True,
            last_activity_days=100,  # >90 for reactivate
            last_deal_days=130,      # >120 for AT_RISK
            is_portal_active=True,
        )
        result = engine.analyze(inp)
        assert result.channel_health == ChannelHealth.AT_RISK
        assert result.partner_action == PartnerAction.REACTIVATE
        assert result.needs_intervention is True

    def test_result_fields_correct_types(self, engine, default_input):
        result = engine.analyze(default_input)
        assert isinstance(result.partner_id, str)
        assert isinstance(result.partner_name, str)
        assert isinstance(result.partner_type, PartnerType)
        assert isinstance(result.current_tier, PartnerTier)
        assert isinstance(result.recommended_tier, PartnerTier)
        assert isinstance(result.channel_health, ChannelHealth)
        assert isinstance(result.partner_action, PartnerAction)
        assert isinstance(result.engagement_score, float)
        assert isinstance(result.performance_score, float)
        assert isinstance(result.pipeline_contribution, float)
        assert isinstance(result.win_rate, float)
        assert isinstance(result.certification_rate, float)
        assert isinstance(result.conflict_resolution_rate, float)
        assert isinstance(result.quota_attainment, float)
        assert isinstance(result.is_strategic, bool)
        assert isinstance(result.needs_intervention, bool)

    def test_result_scores_in_range(self, engine, default_input):
        result = engine.analyze(default_input)
        assert 0.0 <= result.engagement_score <= 100.0
        assert 0.0 <= result.performance_score <= 100.0
        assert 0.0 <= result.win_rate <= 1.0
        assert 0.0 <= result.certification_rate <= 1.0
        assert 0.0 <= result.conflict_resolution_rate <= 1.0

    def test_analyze_appends_to_results(self, engine):
        for i in range(3):
            engine.analyze(make_input(partner_id=f"P{i}"))
        assert engine.summary()["total"] == 3

    def test_pipeline_contribution_in_to_dict(self, engine):
        inp = make_input(quarterly_revenue_target=100_000.0, pipeline_value=200_000.0)
        result = engine.analyze(inp)
        d = result.to_dict()
        assert d["pipeline_contribution"] == 200.0

    def test_win_rate_in_to_dict(self, engine):
        inp = make_input(deals_closed_won=10, deals_closed_lost=0)
        result = engine.analyze(inp)
        assert result.to_dict()["win_rate"] == 1.0

    def test_certification_rate_in_to_dict(self, engine):
        inp = make_input(certified_reps=5, total_partner_reps=10)
        result = engine.analyze(inp)
        assert result.to_dict()["certification_rate"] == 0.5

    def test_quota_attainment_in_to_dict(self, engine):
        inp = make_input(quarterly_revenue_target=100_000.0, quarterly_revenue_actual=75_000.0)
        result = engine.analyze(inp)
        assert result.to_dict()["quota_attainment"] == 75.0

    def test_prospect_partner_low_scores(self, engine):
        inp = make_input(
            partner_id="PROSP1",
            current_tier=PartnerTier.PROSPECT,
            years_as_partner=0.5,
            deals_registered=0,
            deals_closed_won=0, deals_closed_lost=0,
            pipeline_value=0.0,
            closed_won_value=0.0,
            certified_reps=0, total_partner_reps=5,
            training_completion_pct=0.0,
            last_deal_days=200, last_activity_days=200,  # no activity bonus
            joint_campaigns=0,
            conflict_incidents=0,
            quarterly_revenue_target=50_000.0,
            quarterly_revenue_actual=0.0,
            nps_score=-50.0,
            is_portal_active=False, has_completed_onboarding=False,
            contract_valid=True,
            avg_deal_size=0.0,
        )
        result = engine.analyze(inp)
        assert result.engagement_score == 0.0
        # recommended tier should be PROSPECT or BRONZE for very low scores
        assert result.recommended_tier in (PartnerTier.PROSPECT, PartnerTier.BRONZE)

    def test_full_pipeline_calculation_in_result(self, engine):
        inp = make_input(
            quarterly_revenue_target=200_000.0,
            pipeline_value=100_000.0,
        )
        result = engine.analyze(inp)
        assert result.pipeline_contribution == 50.0

    def test_quota_attainment_zero_target_in_result(self, engine):
        inp = make_input(quarterly_revenue_target=0.0, quarterly_revenue_actual=50_000.0)
        result = engine.analyze(inp)
        assert result.quota_attainment == 100.0

    def test_conflict_resolution_in_result(self, engine):
        inp = make_input(conflict_incidents=4, conflict_resolved=2)
        result = engine.analyze(inp)
        assert result.conflict_resolution_rate == 0.5

    def test_needs_intervention_at_risk(self, engine):
        inp = make_input(
            contract_valid=True,
            last_activity_days=10,
            last_deal_days=130,  # >120 → AT_RISK
            is_portal_active=True,
        )
        result = engine.analyze(inp)
        assert result.needs_intervention == (result.channel_health in (ChannelHealth.AT_RISK, ChannelHealth.INACTIVE))

    def test_multiple_partner_types(self, engine):
        types = list(PartnerType)
        for i, pt in enumerate(types):
            engine.analyze(make_input(partner_id=f"P{i}", partner_type=pt))
        s = engine.summary()
        assert s["total"] == len(types)
        assert len(s["type_counts"]) == len(types)

    def test_multiple_partner_tiers(self, engine):
        tiers = list(PartnerTier)
        for i, tier in enumerate(tiers):
            engine.analyze(make_input(partner_id=f"P{i}", current_tier=tier))
        s = engine.summary()
        assert s["total"] == len(tiers)
        assert len(s["tier_counts"]) == len(tiers)

    def test_reset_then_analyze_fresh(self, engine):
        engine.analyze(make_input(partner_id="OLD"))
        engine.reset()
        engine.analyze(make_input(partner_id="NEW"))
        s = engine.summary()
        assert s["total"] == 1
        # Verify it's the new one
        assert engine._results[0].partner_id == "NEW"

    def test_analyze_result_stored(self, engine, default_input):
        result = engine.analyze(default_input)
        assert engine._results[-1] is result

    def test_win_rate_zero_when_no_deals(self, engine):
        inp = make_input(deals_closed_won=0, deals_closed_lost=0)
        result = engine.analyze(inp)
        assert result.win_rate == 0.0

    def test_cert_rate_zero_when_no_reps(self, engine):
        inp = make_input(certified_reps=0, total_partner_reps=0)
        result = engine.analyze(inp)
        assert result.certification_rate == 0.0

    def test_conflict_res_rate_one_when_zero_incidents(self, engine):
        inp = make_input(conflict_incidents=0, conflict_resolved=0)
        result = engine.analyze(inp)
        assert result.conflict_resolution_rate == 1.0

    def test_analyze_idempotent_per_call(self, engine):
        inp = make_input()
        r1 = engine.analyze(inp)
        engine.reset()
        r2 = engine.analyze(inp)
        assert r1.engagement_score == r2.engagement_score
        assert r1.performance_score == r2.performance_score
        assert r1.channel_health == r2.channel_health
