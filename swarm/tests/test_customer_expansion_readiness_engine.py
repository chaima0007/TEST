"""
Comprehensive pytest test suite for
swarm/intelligence/customer_expansion_readiness_engine.py

Run from /home/user/TEST:
    python -m pytest swarm/tests/test_customer_expansion_readiness_engine.py -v
"""

from __future__ import annotations

import pytest

from swarm.intelligence.customer_expansion_readiness_engine import (
    ExpansionReadinessTier,
    ExpansionMotion,
    ExpansionPriority,
    ExpansionAction,
    CustomerExpansionInput,
    CustomerExpansionResult,
    CustomerExpansionReadinessEngine,
)


# ─── Fixture / Helper ──────────────────────────────────────────────────────────

def make_input(
    account_id: str = "acct_001",
    account_name: str = "Acme Corp",
    industry: str = "SaaS",
    region: str = "AMER",
    current_mrr: float = 10_000.0,
    contract_end_months: int = 6,
    seats_used: int = 80,
    seats_purchased: int = 100,
    max_seats_available: int = 150,
    feature_adoption_rate: float = 70.0,
    nps_score: float = 50.0,
    support_health_score: float = 80.0,
    executive_engagement_score: float = 70.0,
    last_qbr_months_ago: int = 2,
    expansion_conversations_had: int = 2,
    upsell_opportunity_count: int = 2,
    cross_sell_products_eligible: int = 2,
    contract_size_growth_yoy_pct: float = 20.0,
    avg_mau_pct: float = 75.0,
    business_outcomes_pct: float = 80.0,
    competitor_interest_signals: int = 0,
    champion_strength_score: float = 70.0,
) -> CustomerExpansionInput:
    return CustomerExpansionInput(
        account_id=account_id,
        account_name=account_name,
        industry=industry,
        region=region,
        current_mrr=current_mrr,
        contract_end_months=contract_end_months,
        seats_used=seats_used,
        seats_purchased=seats_purchased,
        max_seats_available=max_seats_available,
        feature_adoption_rate=feature_adoption_rate,
        nps_score=nps_score,
        support_health_score=support_health_score,
        executive_engagement_score=executive_engagement_score,
        last_qbr_months_ago=last_qbr_months_ago,
        expansion_conversations_had=expansion_conversations_had,
        upsell_opportunity_count=upsell_opportunity_count,
        cross_sell_products_eligible=cross_sell_products_eligible,
        contract_size_growth_yoy_pct=contract_size_growth_yoy_pct,
        avg_mau_pct=avg_mau_pct,
        business_outcomes_pct=business_outcomes_pct,
        competitor_interest_signals=competitor_interest_signals,
        champion_strength_score=champion_strength_score,
    )


@pytest.fixture
def engine() -> CustomerExpansionReadinessEngine:
    return CustomerExpansionReadinessEngine()


@pytest.fixture
def default_input() -> CustomerExpansionInput:
    return make_input()


# ─── 1. Enum values ────────────────────────────────────────────────────────────

class TestEnumValues:
    def test_expansion_readiness_tier_not_ready(self):
        assert ExpansionReadinessTier.NOT_READY.value == "not_ready"

    def test_expansion_readiness_tier_building(self):
        assert ExpansionReadinessTier.BUILDING.value == "building"

    def test_expansion_readiness_tier_ready(self):
        assert ExpansionReadinessTier.READY.value == "ready"

    def test_expansion_readiness_tier_primed(self):
        assert ExpansionReadinessTier.PRIMED.value == "primed"

    def test_expansion_readiness_tier_count(self):
        assert len(ExpansionReadinessTier) == 4

    def test_expansion_motion_seat_expansion(self):
        assert ExpansionMotion.SEAT_EXPANSION.value == "seat_expansion"

    def test_expansion_motion_upsell_tier(self):
        assert ExpansionMotion.UPSELL_TIER.value == "upsell_tier"

    def test_expansion_motion_cross_sell(self):
        assert ExpansionMotion.CROSS_SELL.value == "cross_sell"

    def test_expansion_motion_renewal_lock(self):
        assert ExpansionMotion.RENEWAL_LOCK.value == "renewal_lock"

    def test_expansion_motion_hold(self):
        assert ExpansionMotion.HOLD.value == "hold"

    def test_expansion_motion_count(self):
        assert len(ExpansionMotion) == 5

    def test_expansion_priority_low(self):
        assert ExpansionPriority.LOW.value == "low"

    def test_expansion_priority_medium(self):
        assert ExpansionPriority.MEDIUM.value == "medium"

    def test_expansion_priority_high(self):
        assert ExpansionPriority.HIGH.value == "high"

    def test_expansion_priority_urgent(self):
        assert ExpansionPriority.URGENT.value == "urgent"

    def test_expansion_priority_count(self):
        assert len(ExpansionPriority) == 4

    def test_expansion_action_maintain(self):
        assert ExpansionAction.MAINTAIN.value == "maintain"

    def test_expansion_action_nurture(self):
        assert ExpansionAction.NURTURE.value == "nurture"

    def test_expansion_action_engage(self):
        assert ExpansionAction.ENGAGE.value == "engage"

    def test_expansion_action_close_expansion(self):
        assert ExpansionAction.CLOSE_EXPANSION.value == "close_expansion"

    def test_expansion_action_count(self):
        assert len(ExpansionAction) == 4

    def test_enums_are_str_subclass(self):
        assert isinstance(ExpansionReadinessTier.PRIMED, str)
        assert isinstance(ExpansionMotion.CROSS_SELL, str)
        assert isinstance(ExpansionPriority.URGENT, str)
        assert isinstance(ExpansionAction.ENGAGE, str)


# ─── 2. CustomerExpansionInput field count ─────────────────────────────────────

class TestInputFields:
    def test_input_has_22_fields(self):
        import dataclasses
        fields = dataclasses.fields(CustomerExpansionInput)
        assert len(fields) == 22

    def test_input_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(CustomerExpansionInput)}
        expected = {
            "account_id", "account_name", "industry", "region",
            "current_mrr", "contract_end_months", "seats_used",
            "seats_purchased", "max_seats_available", "feature_adoption_rate",
            "nps_score", "support_health_score", "executive_engagement_score",
            "last_qbr_months_ago", "expansion_conversations_had",
            "upsell_opportunity_count", "cross_sell_products_eligible",
            "contract_size_growth_yoy_pct", "avg_mau_pct",
            "business_outcomes_pct", "competitor_interest_signals",
            "champion_strength_score",
        }
        assert names == expected

    def test_input_construction_defaults(self):
        inp = make_input()
        assert inp.account_id == "acct_001"
        assert inp.industry == "SaaS"
        assert inp.region == "AMER"

    def test_input_string_fields(self):
        inp = make_input(account_id="x", account_name="y", industry="z", region="w")
        assert inp.account_id == "x"
        assert inp.account_name == "y"
        assert inp.industry == "z"
        assert inp.region == "w"


# ─── 3. to_dict() key count ────────────────────────────────────────────────────

class TestToDict:
    def test_to_dict_has_15_keys(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_expected_keys(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        expected_keys = {
            "account_id", "account_name", "expansion_readiness_tier",
            "expansion_motion", "expansion_priority", "expansion_action",
            "product_depth_score", "relationship_strength_score",
            "financial_health_score", "timing_score",
            "expansion_readiness_score", "estimated_expansion_arr",
            "expansion_confidence_score", "is_expansion_ready",
            "needs_success_intervention",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        assert isinstance(d["expansion_readiness_tier"], str)
        assert isinstance(d["expansion_motion"], str)
        assert isinstance(d["expansion_priority"], str)
        assert isinstance(d["expansion_action"], str)

    def test_to_dict_bool_fields(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        assert isinstance(d["is_expansion_ready"], bool)
        assert isinstance(d["needs_success_intervention"], bool)

    def test_to_dict_numeric_fields_are_float(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        for key in [
            "product_depth_score", "relationship_strength_score",
            "financial_health_score", "timing_score",
            "expansion_readiness_score", "estimated_expansion_arr",
            "expansion_confidence_score",
        ]:
            assert isinstance(d[key], (int, float)), f"{key} should be numeric"

    def test_to_dict_account_id_passthrough(self, engine):
        inp = make_input(account_id="acct_xyz")
        result = engine.analyze(inp)
        assert result.to_dict()["account_id"] == "acct_xyz"

    def test_to_dict_account_name_passthrough(self, engine):
        inp = make_input(account_name="Big Corp")
        result = engine.analyze(inp)
        assert result.to_dict()["account_name"] == "Big Corp"

    def test_to_dict_scores_bounded_0_100(self, engine, default_input):
        result = engine.analyze(default_input)
        d = result.to_dict()
        for key in [
            "product_depth_score", "relationship_strength_score",
            "financial_health_score", "timing_score",
            "expansion_readiness_score", "expansion_confidence_score",
        ]:
            assert 0.0 <= d[key] <= 100.0, f"{key} out of bounds: {d[key]}"


# ─── 4. summary() key count ────────────────────────────────────────────────────

class TestSummaryKeys:
    def test_summary_has_13_keys_empty(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_summary_has_13_keys_after_analyze(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        assert len(s) == 13

    def test_summary_expected_keys(self, engine, default_input):
        engine.analyze(default_input)
        s = engine.summary()
        expected_keys = {
            "total", "tier_counts", "motion_counts", "priority_counts",
            "action_counts", "avg_expansion_readiness_score",
            "total_estimated_expansion_arr", "ready_count",
            "intervention_needed_count", "avg_product_depth_score",
            "avg_relationship_strength_score", "avg_timing_score",
            "avg_expansion_confidence_score",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_empty_engine_zeros(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["avg_expansion_readiness_score"] == 0.0
        assert s["total_estimated_expansion_arr"] == 0.0
        assert s["ready_count"] == 0
        assert s["intervention_needed_count"] == 0
        assert s["avg_product_depth_score"] == 0.0
        assert s["avg_relationship_strength_score"] == 0.0
        assert s["avg_timing_score"] == 0.0
        assert s["avg_expansion_confidence_score"] == 0.0

    def test_summary_empty_counts_are_dicts(self, engine):
        s = engine.summary()
        assert isinstance(s["tier_counts"], dict)
        assert isinstance(s["motion_counts"], dict)
        assert isinstance(s["priority_counts"], dict)
        assert isinstance(s["action_counts"], dict)

    def test_summary_total_matches_analyzed(self, engine):
        engine.analyze(make_input(account_id="a1"))
        engine.analyze(make_input(account_id="a2"))
        engine.analyze(make_input(account_id="a3"))
        assert engine.summary()["total"] == 3


# ─── 5. _product_depth_score ───────────────────────────────────────────────────

class TestProductDepthScore:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_max_feature_adoption_caps_at_40(self):
        inp = make_input(feature_adoption_rate=100.0, seats_used=0, seats_purchased=100,
                         avg_mau_pct=0.0, business_outcomes_pct=0.0)
        score = self.engine._product_depth_score(inp)
        assert score == 40.0

    def test_feature_adoption_partial(self):
        inp = make_input(feature_adoption_rate=50.0, seats_used=0, seats_purchased=100,
                         avg_mau_pct=0.0, business_outcomes_pct=0.0)
        score = self.engine._product_depth_score(inp)
        assert score == 20.0

    def test_seat_utilization_100pct_adds_30(self):
        inp = make_input(feature_adoption_rate=0.0, seats_used=100, seats_purchased=100,
                         max_seats_available=150, avg_mau_pct=0.0, business_outcomes_pct=0.0)
        score = self.engine._product_depth_score(inp)
        assert score == 30.0

    def test_seat_utilization_zero_purchased(self):
        inp = make_input(feature_adoption_rate=0.0, seats_used=50, seats_purchased=0,
                         avg_mau_pct=0.0, business_outcomes_pct=0.0)
        score = self.engine._product_depth_score(inp)
        # seats_purchased == 0 branch skipped
        assert score == 0.0

    def test_mau_pct_caps_at_20(self):
        inp = make_input(feature_adoption_rate=0.0, seats_used=0, seats_purchased=100,
                         avg_mau_pct=100.0, business_outcomes_pct=0.0)
        score = self.engine._product_depth_score(inp)
        assert score == 20.0

    def test_business_outcomes_caps_at_10(self):
        inp = make_input(feature_adoption_rate=0.0, seats_used=0, seats_purchased=100,
                         avg_mau_pct=0.0, business_outcomes_pct=100.0)
        score = self.engine._product_depth_score(inp)
        assert score == 10.0

    def test_all_zeros_returns_zero(self):
        inp = make_input(feature_adoption_rate=0.0, seats_used=0, seats_purchased=100,
                         avg_mau_pct=0.0, business_outcomes_pct=0.0)
        assert self.engine._product_depth_score(inp) == 0.0

    def test_all_max_returns_100(self):
        inp = make_input(
            feature_adoption_rate=100.0, seats_used=100, seats_purchased=100,
            max_seats_available=150, avg_mau_pct=100.0, business_outcomes_pct=100.0,
        )
        assert self.engine._product_depth_score(inp) == 100.0

    def test_score_is_rounded_to_1dp(self):
        inp = make_input(feature_adoption_rate=33.3, seats_used=0, seats_purchased=100,
                         avg_mau_pct=0.0, business_outcomes_pct=0.0)
        score = self.engine._product_depth_score(inp)
        assert score == round(score, 1)

    def test_score_never_below_zero(self):
        inp = make_input(feature_adoption_rate=0.0, seats_used=0, seats_purchased=0,
                         avg_mau_pct=0.0, business_outcomes_pct=0.0)
        assert self.engine._product_depth_score(inp) >= 0.0

    def test_score_never_above_100(self):
        inp = make_input(feature_adoption_rate=200.0, seats_used=200, seats_purchased=100,
                         avg_mau_pct=200.0, business_outcomes_pct=200.0)
        assert self.engine._product_depth_score(inp) <= 100.0

    def test_partial_seat_utilization(self):
        inp = make_input(feature_adoption_rate=0.0, seats_used=50, seats_purchased=100,
                         max_seats_available=150, avg_mau_pct=0.0, business_outcomes_pct=0.0)
        # 50/100 * 100 = 50 util; min(30, 50*0.3) = 15
        assert self.engine._product_depth_score(inp) == 15.0

    def test_mau_partial(self):
        inp = make_input(feature_adoption_rate=0.0, seats_used=0, seats_purchased=100,
                         avg_mau_pct=50.0, business_outcomes_pct=0.0)
        assert self.engine._product_depth_score(inp) == 10.0

    def test_combined_score_additive(self):
        inp = make_input(
            feature_adoption_rate=100.0, seats_used=100, seats_purchased=100,
            max_seats_available=150, avg_mau_pct=50.0, business_outcomes_pct=50.0,
        )
        # 40 + 30 + 10 + 5 = 85
        assert self.engine._product_depth_score(inp) == 85.0


# ─── 6. _relationship_strength_score ──────────────────────────────────────────

class TestRelationshipStrengthScore:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_nps_100_contributes_35(self):
        inp = make_input(nps_score=100.0, executive_engagement_score=0.0,
                         champion_strength_score=0.0, last_qbr_months_ago=99)
        score = self.engine._relationship_strength_score(inp)
        assert score == 35.0

    def test_nps_minus_100_contributes_0(self):
        inp = make_input(nps_score=-100.0, executive_engagement_score=0.0,
                         champion_strength_score=0.0, last_qbr_months_ago=99)
        score = self.engine._relationship_strength_score(inp)
        assert score == 0.0

    def test_nps_0_contributes_half_of_35(self):
        inp = make_input(nps_score=0.0, executive_engagement_score=0.0,
                         champion_strength_score=0.0, last_qbr_months_ago=99)
        # (0 + 100) / 200 * 35 = 17.5
        score = self.engine._relationship_strength_score(inp)
        assert score == 17.5

    def test_executive_engagement_100_adds_30(self):
        inp = make_input(nps_score=-100.0, executive_engagement_score=100.0,
                         champion_strength_score=0.0, last_qbr_months_ago=99)
        assert self.engine._relationship_strength_score(inp) == 30.0

    def test_champion_strength_100_adds_25(self):
        inp = make_input(nps_score=-100.0, executive_engagement_score=0.0,
                         champion_strength_score=100.0, last_qbr_months_ago=99)
        assert self.engine._relationship_strength_score(inp) == 25.0

    def test_qbr_within_3_months_adds_10(self):
        inp = make_input(nps_score=-100.0, executive_engagement_score=0.0,
                         champion_strength_score=0.0, last_qbr_months_ago=3)
        assert self.engine._relationship_strength_score(inp) == 10.0

    def test_qbr_within_6_months_adds_6(self):
        inp = make_input(nps_score=-100.0, executive_engagement_score=0.0,
                         champion_strength_score=0.0, last_qbr_months_ago=6)
        assert self.engine._relationship_strength_score(inp) == 6.0

    def test_qbr_within_12_months_adds_2(self):
        inp = make_input(nps_score=-100.0, executive_engagement_score=0.0,
                         champion_strength_score=0.0, last_qbr_months_ago=12)
        assert self.engine._relationship_strength_score(inp) == 2.0

    def test_qbr_beyond_12_months_adds_0(self):
        inp = make_input(nps_score=-100.0, executive_engagement_score=0.0,
                         champion_strength_score=0.0, last_qbr_months_ago=13)
        assert self.engine._relationship_strength_score(inp) == 0.0

    def test_all_max_returns_100(self):
        inp = make_input(nps_score=100.0, executive_engagement_score=100.0,
                         champion_strength_score=100.0, last_qbr_months_ago=1)
        assert self.engine._relationship_strength_score(inp) == 100.0

    def test_score_capped_at_100(self):
        inp = make_input(nps_score=100.0, executive_engagement_score=200.0,
                         champion_strength_score=200.0, last_qbr_months_ago=1)
        assert self.engine._relationship_strength_score(inp) <= 100.0

    def test_score_never_negative(self):
        inp = make_input(nps_score=-100.0, executive_engagement_score=0.0,
                         champion_strength_score=0.0, last_qbr_months_ago=99)
        assert self.engine._relationship_strength_score(inp) >= 0.0

    def test_score_rounded_to_1dp(self):
        inp = make_input(nps_score=33.0, executive_engagement_score=33.0,
                         champion_strength_score=33.0, last_qbr_months_ago=99)
        score = self.engine._relationship_strength_score(inp)
        assert score == round(score, 1)

    def test_qbr_exactly_4_adds_6(self):
        inp = make_input(nps_score=-100.0, executive_engagement_score=0.0,
                         champion_strength_score=0.0, last_qbr_months_ago=4)
        assert self.engine._relationship_strength_score(inp) == 6.0

    def test_qbr_exactly_7_adds_2(self):
        inp = make_input(nps_score=-100.0, executive_engagement_score=0.0,
                         champion_strength_score=0.0, last_qbr_months_ago=7)
        assert self.engine._relationship_strength_score(inp) == 2.0


# ─── 7. _financial_health_score ───────────────────────────────────────────────

class TestFinancialHealthScore:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_support_health_100_adds_35(self):
        inp = make_input(support_health_score=100.0, contract_size_growth_yoy_pct=0.0,
                         business_outcomes_pct=0.0, competitor_interest_signals=0)
        assert self.engine._financial_health_score(inp) == 35.0

    def test_support_health_0_adds_0(self):
        inp = make_input(support_health_score=0.0, contract_size_growth_yoy_pct=0.0,
                         business_outcomes_pct=0.0, competitor_interest_signals=0)
        assert self.engine._financial_health_score(inp) == 0.0

    def test_contract_growth_positive_adds_up_to_35(self):
        inp = make_input(support_health_score=0.0, contract_size_growth_yoy_pct=30.0,
                         business_outcomes_pct=0.0, competitor_interest_signals=0)
        # 30 * 1.5 = 45 -> min(35, 45) = 35
        assert self.engine._financial_health_score(inp) == 35.0

    def test_contract_growth_small_positive(self):
        inp = make_input(support_health_score=0.0, contract_size_growth_yoy_pct=10.0,
                         business_outcomes_pct=0.0, competitor_interest_signals=0)
        # 10 * 1.5 = 15
        assert self.engine._financial_health_score(inp) == 15.0

    def test_contract_growth_negative_adds_0(self):
        inp = make_input(support_health_score=0.0, contract_size_growth_yoy_pct=-10.0,
                         business_outcomes_pct=0.0, competitor_interest_signals=0)
        assert self.engine._financial_health_score(inp) == 0.0

    def test_business_outcomes_100_adds_30(self):
        inp = make_input(support_health_score=0.0, contract_size_growth_yoy_pct=0.0,
                         business_outcomes_pct=100.0, competitor_interest_signals=0)
        assert self.engine._financial_health_score(inp) == 30.0

    def test_competitor_signals_reduce_score(self):
        inp = make_input(support_health_score=100.0, contract_size_growth_yoy_pct=0.0,
                         business_outcomes_pct=0.0, competitor_interest_signals=1)
        # 35 - 8 = 27
        assert self.engine._financial_health_score(inp) == 27.0

    def test_competitor_signals_capped_at_minus_20(self):
        inp = make_input(support_health_score=100.0, contract_size_growth_yoy_pct=0.0,
                         business_outcomes_pct=0.0, competitor_interest_signals=10)
        # 35 - min(20, 80) = 35 - 20 = 15
        assert self.engine._financial_health_score(inp) == 15.0

    def test_score_never_negative(self):
        inp = make_input(support_health_score=0.0, contract_size_growth_yoy_pct=0.0,
                         business_outcomes_pct=0.0, competitor_interest_signals=100)
        assert self.engine._financial_health_score(inp) >= 0.0

    def test_score_never_above_100(self):
        inp = make_input(support_health_score=100.0, contract_size_growth_yoy_pct=100.0,
                         business_outcomes_pct=100.0, competitor_interest_signals=0)
        assert self.engine._financial_health_score(inp) <= 100.0

    def test_score_rounded_to_1dp(self):
        inp = make_input(support_health_score=33.3, contract_size_growth_yoy_pct=0.0,
                         business_outcomes_pct=0.0, competitor_interest_signals=0)
        score = self.engine._financial_health_score(inp)
        assert score == round(score, 1)

    def test_all_max_returns_100(self):
        inp = make_input(support_health_score=100.0, contract_size_growth_yoy_pct=100.0,
                         business_outcomes_pct=100.0, competitor_interest_signals=0)
        assert self.engine._financial_health_score(inp) == 100.0

    def test_two_competitor_signals(self):
        inp = make_input(support_health_score=0.0, contract_size_growth_yoy_pct=0.0,
                         business_outcomes_pct=0.0, competitor_interest_signals=2)
        # -min(20, 2*8) = -16 -> max(0, -16) = 0
        assert self.engine._financial_health_score(inp) == 0.0


# ─── 8. _timing_score ──────────────────────────────────────────────────────────

class TestTimingScore:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_sweet_spot_3_to_9_months_adds_40(self):
        for months in [3, 6, 9]:
            inp = make_input(contract_end_months=months, expansion_conversations_had=0,
                             upsell_opportunity_count=0, competitor_interest_signals=0)
            score = self.engine._timing_score(inp)
            assert score == 40.0, f"months={months}"

    def test_too_close_1_to_2_months_adds_25(self):
        for months in [1, 2]:
            inp = make_input(contract_end_months=months, expansion_conversations_had=0,
                             upsell_opportunity_count=0, competitor_interest_signals=0)
            score = self.engine._timing_score(inp)
            assert score == 25.0, f"months={months}"

    def test_10_to_14_months_adds_20(self):
        for months in [10, 12, 14]:
            inp = make_input(contract_end_months=months, expansion_conversations_had=0,
                             upsell_opportunity_count=0, competitor_interest_signals=0)
            score = self.engine._timing_score(inp)
            assert score == 20.0, f"months={months}"

    def test_far_out_adds_5(self):
        for months in [0, 15, 24]:
            inp = make_input(contract_end_months=months, expansion_conversations_had=0,
                             upsell_opportunity_count=0, competitor_interest_signals=0)
            score = self.engine._timing_score(inp)
            assert score == 5.0, f"months={months}"

    def test_expansion_conversations_caps_at_30(self):
        inp = make_input(contract_end_months=20, expansion_conversations_had=5,
                         upsell_opportunity_count=0, competitor_interest_signals=0)
        # 5 + min(30, 5*10) = 5 + 30 = 35
        assert self.engine._timing_score(inp) == 35.0

    def test_expansion_conversations_partial(self):
        inp = make_input(contract_end_months=20, expansion_conversations_had=2,
                         upsell_opportunity_count=0, competitor_interest_signals=0)
        # 5 + 20 = 25
        assert self.engine._timing_score(inp) == 25.0

    def test_upsell_count_caps_at_20(self):
        inp = make_input(contract_end_months=20, expansion_conversations_had=0,
                         upsell_opportunity_count=3, competitor_interest_signals=0)
        # 5 + min(20, 3*7) = 5 + 20 = 25 (21 < 20 false; 21 > 20 so cap)
        # Actually min(20, 3*7) = min(20, 21) = 20
        assert self.engine._timing_score(inp) == 25.0

    def test_upsell_count_2_adds_14(self):
        inp = make_input(contract_end_months=20, expansion_conversations_had=0,
                         upsell_opportunity_count=2, competitor_interest_signals=0)
        # 5 + min(20, 14) = 19
        assert self.engine._timing_score(inp) == 19.0

    def test_competitor_signals_add_up_to_10(self):
        inp = make_input(contract_end_months=20, expansion_conversations_had=0,
                         upsell_opportunity_count=0, competitor_interest_signals=5)
        # 5 + min(10, 5*4) = 5 + 10 = 15
        assert self.engine._timing_score(inp) == 15.0

    def test_competitor_1_adds_4(self):
        inp = make_input(contract_end_months=20, expansion_conversations_had=0,
                         upsell_opportunity_count=0, competitor_interest_signals=1)
        # 5 + 4 = 9
        assert self.engine._timing_score(inp) == 9.0

    def test_score_capped_at_100(self):
        inp = make_input(contract_end_months=6, expansion_conversations_had=10,
                         upsell_opportunity_count=10, competitor_interest_signals=10)
        assert self.engine._timing_score(inp) <= 100.0

    def test_score_never_negative(self):
        inp = make_input(contract_end_months=0, expansion_conversations_had=0,
                         upsell_opportunity_count=0, competitor_interest_signals=0)
        assert self.engine._timing_score(inp) >= 0.0

    def test_score_rounded_to_1dp(self):
        inp = make_input()
        score = self.engine._timing_score(inp)
        assert score == round(score, 1)


# ─── 9. _expansion_readiness_score ────────────────────────────────────────────

class TestExpansionReadinessScore:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_all_zeros(self):
        assert self.engine._expansion_readiness_score(0, 0, 0, 0) == 0.0

    def test_all_100(self):
        assert self.engine._expansion_readiness_score(100, 100, 100, 100) == 100.0

    def test_weights_prod_depth(self):
        # Only prod_depth = 100, rest 0 → 100 * 0.30 = 30
        assert self.engine._expansion_readiness_score(100, 0, 0, 0) == 30.0

    def test_weights_rel_strength(self):
        # Only rel_strength = 100 → 100 * 0.30 = 30
        assert self.engine._expansion_readiness_score(0, 100, 0, 0) == 30.0

    def test_weights_fin_health(self):
        # Only fin_health = 100 → 100 * 0.20 = 20
        assert self.engine._expansion_readiness_score(0, 0, 100, 0) == 20.0

    def test_weights_timing(self):
        # Only timing = 100 → 100 * 0.20 = 20
        assert self.engine._expansion_readiness_score(0, 0, 0, 100) == 20.0

    def test_weights_sum_to_100(self):
        result = self.engine._expansion_readiness_score(100, 100, 100, 100)
        assert result == 100.0

    def test_rounded_to_1dp(self):
        score = self.engine._expansion_readiness_score(33.3, 33.3, 33.3, 33.3)
        assert score == round(score, 1)

    def test_capped_at_100(self):
        score = self.engine._expansion_readiness_score(200, 200, 200, 200)
        assert score <= 100.0

    def test_never_below_zero(self):
        score = self.engine._expansion_readiness_score(-10, -10, -10, -10)
        assert score >= 0.0

    def test_composite_50_50_50_50(self):
        # 50*0.30 + 50*0.30 + 50*0.20 + 50*0.20 = 15+15+10+10=50
        assert self.engine._expansion_readiness_score(50, 50, 50, 50) == 50.0


# ─── 10. Tier branching ────────────────────────────────────────────────────────

class TestReadinessTier:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_score_75_is_primed(self):
        assert self.engine._readiness_tier(75.0) == ExpansionReadinessTier.PRIMED

    def test_score_100_is_primed(self):
        assert self.engine._readiness_tier(100.0) == ExpansionReadinessTier.PRIMED

    def test_score_74_is_ready(self):
        assert self.engine._readiness_tier(74.9) == ExpansionReadinessTier.READY

    def test_score_55_is_ready(self):
        assert self.engine._readiness_tier(55.0) == ExpansionReadinessTier.READY

    def test_score_54_is_building(self):
        assert self.engine._readiness_tier(54.9) == ExpansionReadinessTier.BUILDING

    def test_score_35_is_building(self):
        assert self.engine._readiness_tier(35.0) == ExpansionReadinessTier.BUILDING

    def test_score_34_is_not_ready(self):
        assert self.engine._readiness_tier(34.9) == ExpansionReadinessTier.NOT_READY

    def test_score_0_is_not_ready(self):
        assert self.engine._readiness_tier(0.0) == ExpansionReadinessTier.NOT_READY

    def test_score_exactly_75_is_primed(self):
        assert self.engine._readiness_tier(75.0) == ExpansionReadinessTier.PRIMED

    def test_score_exactly_55_is_ready(self):
        assert self.engine._readiness_tier(55.0) == ExpansionReadinessTier.READY

    def test_score_exactly_35_is_building(self):
        assert self.engine._readiness_tier(35.0) == ExpansionReadinessTier.BUILDING


# ─── 11. Expansion motion branching ───────────────────────────────────────────

class TestExpansionMotion:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_low_readiness_returns_hold(self):
        inp = make_input(seats_used=50, seats_purchased=100, max_seats_available=200,
                         cross_sell_products_eligible=0, contract_end_months=10,
                         nps_score=50.0)
        motion = self.engine._expansion_motion(inp, prod_depth=40.0, readiness=25.0)
        assert motion == ExpansionMotion.HOLD

    def test_seat_headroom_and_depth_returns_seat_expansion(self):
        # headroom = (200 - 50) / 200 = 0.75 >= 0.3; prod_depth >= 60; readiness >= 30
        inp = make_input(seats_used=50, seats_purchased=100, max_seats_available=200,
                         cross_sell_products_eligible=0, contract_end_months=10,
                         nps_score=50.0)
        motion = self.engine._expansion_motion(inp, prod_depth=70.0, readiness=50.0)
        assert motion == ExpansionMotion.SEAT_EXPANSION

    def test_no_seat_headroom_skips_seat_expansion(self):
        # headroom = (100 - 95) / 100 = 0.05 < 0.3
        inp = make_input(seats_used=95, seats_purchased=100, max_seats_available=100,
                         cross_sell_products_eligible=3, contract_end_months=10,
                         nps_score=50.0)
        motion = self.engine._expansion_motion(inp, prod_depth=70.0, readiness=55.0)
        assert motion == ExpansionMotion.CROSS_SELL

    def test_cross_sell_eligible_returns_cross_sell(self):
        inp = make_input(seats_used=50, seats_purchased=100, max_seats_available=55,
                         cross_sell_products_eligible=3, contract_end_months=10,
                         nps_score=50.0)
        # headroom = (55 - 50) / 55 = 0.09 < 0.3, but cross_sell >= 2, readiness >= 50
        motion = self.engine._expansion_motion(inp, prod_depth=40.0, readiness=55.0)
        assert motion == ExpansionMotion.CROSS_SELL

    def test_renewal_lock_contract_end_4_high_nps(self):
        inp = make_input(seats_used=50, seats_purchased=100, max_seats_available=55,
                         cross_sell_products_eligible=0, contract_end_months=4,
                         nps_score=50.0)
        motion = self.engine._expansion_motion(inp, prod_depth=40.0, readiness=50.0)
        assert motion == ExpansionMotion.RENEWAL_LOCK

    def test_renewal_lock_requires_nps_ge_40(self):
        inp = make_input(seats_used=50, seats_purchased=100, max_seats_available=55,
                         cross_sell_products_eligible=0, contract_end_months=4,
                         nps_score=39.0)
        # NPS < 40 → falls through to upsell_tier since readiness >= 50
        motion = self.engine._expansion_motion(inp, prod_depth=40.0, readiness=55.0)
        assert motion == ExpansionMotion.UPSELL_TIER

    def test_default_upsell_tier(self):
        inp = make_input(seats_used=50, seats_purchased=100, max_seats_available=55,
                         cross_sell_products_eligible=0, contract_end_months=10,
                         nps_score=50.0)
        motion = self.engine._expansion_motion(inp, prod_depth=40.0, readiness=55.0)
        assert motion == ExpansionMotion.UPSELL_TIER

    def test_readiness_below_50_not_cross_sell(self):
        inp = make_input(seats_used=50, seats_purchased=100, max_seats_available=55,
                         cross_sell_products_eligible=3, contract_end_months=10,
                         nps_score=50.0)
        # cross_sell_products_eligible >= 2 but readiness < 50
        motion = self.engine._expansion_motion(inp, prod_depth=40.0, readiness=45.0)
        assert motion == ExpansionMotion.HOLD

    def test_zero_seats_purchased_skips_seat_expansion(self):
        inp = make_input(seats_used=0, seats_purchased=0, max_seats_available=100,
                         cross_sell_products_eligible=0, contract_end_months=10,
                         nps_score=50.0)
        motion = self.engine._expansion_motion(inp, prod_depth=70.0, readiness=55.0)
        assert motion == ExpansionMotion.UPSELL_TIER

    def test_prod_depth_below_60_skips_seat_expansion(self):
        inp = make_input(seats_used=50, seats_purchased=100, max_seats_available=200,
                         cross_sell_products_eligible=0, contract_end_months=10,
                         nps_score=50.0)
        motion = self.engine._expansion_motion(inp, prod_depth=59.0, readiness=55.0)
        assert motion == ExpansionMotion.UPSELL_TIER


# ─── 12. Expansion priority branching ─────────────────────────────────────────

class TestExpansionPriority:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_combined_ge_70_urgent(self):
        # combined = 80*0.6 + 70*0.4 = 48 + 28 = 76 >= 70
        inp = make_input(contract_end_months=10)
        priority = self.engine._expansion_priority(inp, readiness=80.0, timing=70.0)
        assert priority == ExpansionPriority.URGENT

    def test_contract_end_3_and_readiness_50_urgent(self):
        inp = make_input(contract_end_months=3)
        priority = self.engine._expansion_priority(inp, readiness=50.0, timing=20.0)
        assert priority == ExpansionPriority.URGENT

    def test_contract_end_2_readiness_50_urgent(self):
        inp = make_input(contract_end_months=2)
        priority = self.engine._expansion_priority(inp, readiness=55.0, timing=20.0)
        assert priority == ExpansionPriority.URGENT

    def test_combined_52_is_high(self):
        # combined = 60*0.6 + 40*0.4 = 36+16 = 52
        inp = make_input(contract_end_months=10)
        priority = self.engine._expansion_priority(inp, readiness=60.0, timing=40.0)
        assert priority == ExpansionPriority.HIGH

    def test_combined_35_is_medium(self):
        # combined = 40*0.6 + 25*0.4 = 24+10 = 34 — actually < 35
        # Let's use 50*0.6 + 12.5*0.4 = 30+5 = 35
        inp = make_input(contract_end_months=10)
        priority = self.engine._expansion_priority(inp, readiness=50.0, timing=12.5)
        assert priority == ExpansionPriority.MEDIUM

    def test_combined_below_35_is_low(self):
        # combined = 20*0.6 + 20*0.4 = 12+8 = 20
        inp = make_input(contract_end_months=10)
        priority = self.engine._expansion_priority(inp, readiness=20.0, timing=20.0)
        assert priority == ExpansionPriority.LOW

    def test_contract_end_3_but_readiness_49_not_urgent(self):
        # contract_end <= 3 and readiness >= 50 → urgent; readiness=49 breaks condition
        inp = make_input(contract_end_months=3)
        # combined = 49*0.6 + 20*0.4 = 29.4+8 = 37.4 → MEDIUM
        priority = self.engine._expansion_priority(inp, readiness=49.0, timing=20.0)
        assert priority == ExpansionPriority.MEDIUM

    def test_contract_end_4_does_not_trigger_urgent_via_months(self):
        inp = make_input(contract_end_months=4)
        # combined = 50*0.6 + 30*0.4 = 30+12 = 42 → MEDIUM
        priority = self.engine._expansion_priority(inp, readiness=50.0, timing=30.0)
        assert priority == ExpansionPriority.MEDIUM

    def test_exactly_combined_70_is_urgent(self):
        # readiness=70, timing=70 → 70*0.6+70*0.4 = 42+28 = 70
        inp = make_input(contract_end_months=10)
        priority = self.engine._expansion_priority(inp, readiness=70.0, timing=70.0)
        assert priority == ExpansionPriority.URGENT

    def test_exactly_combined_52_is_high(self):
        # combined = 86.67*0.6 + 0*0.4 → use 60*0.6 + 40*0.4 = 52
        inp = make_input(contract_end_months=10)
        priority = self.engine._expansion_priority(inp, readiness=60.0, timing=40.0)
        assert priority == ExpansionPriority.HIGH


# ─── 13. _expansion_action branching ──────────────────────────────────────────

class TestExpansionAction:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_needs_interv_and_not_ready_returns_nurture(self):
        action = self.engine._expansion_action(
            ExpansionReadinessTier.BUILDING, ExpansionPriority.MEDIUM,
            is_ready=False, needs_interv=True,
        )
        assert action == ExpansionAction.NURTURE

    def test_primed_tier_returns_close_expansion(self):
        action = self.engine._expansion_action(
            ExpansionReadinessTier.PRIMED, ExpansionPriority.MEDIUM,
            is_ready=False, needs_interv=False,
        )
        assert action == ExpansionAction.CLOSE_EXPANSION

    def test_urgent_priority_returns_close_expansion(self):
        action = self.engine._expansion_action(
            ExpansionReadinessTier.READY, ExpansionPriority.URGENT,
            is_ready=False, needs_interv=False,
        )
        assert action == ExpansionAction.CLOSE_EXPANSION

    def test_is_ready_returns_engage(self):
        action = self.engine._expansion_action(
            ExpansionReadinessTier.READY, ExpansionPriority.MEDIUM,
            is_ready=True, needs_interv=False,
        )
        assert action == ExpansionAction.ENGAGE

    def test_high_priority_returns_engage(self):
        action = self.engine._expansion_action(
            ExpansionReadinessTier.BUILDING, ExpansionPriority.HIGH,
            is_ready=False, needs_interv=False,
        )
        assert action == ExpansionAction.ENGAGE

    def test_building_tier_returns_nurture(self):
        action = self.engine._expansion_action(
            ExpansionReadinessTier.BUILDING, ExpansionPriority.LOW,
            is_ready=False, needs_interv=False,
        )
        assert action == ExpansionAction.NURTURE

    def test_not_ready_tier_medium_priority_returns_maintain(self):
        action = self.engine._expansion_action(
            ExpansionReadinessTier.NOT_READY, ExpansionPriority.MEDIUM,
            is_ready=False, needs_interv=False,
        )
        assert action == ExpansionAction.MAINTAIN

    def test_needs_interv_but_is_ready_does_not_nurture(self):
        # needs_interv=True but is_ready=True → condition (needs_interv and not is_ready) is False
        action = self.engine._expansion_action(
            ExpansionReadinessTier.PRIMED, ExpansionPriority.URGENT,
            is_ready=True, needs_interv=True,
        )
        assert action == ExpansionAction.CLOSE_EXPANSION

    def test_not_ready_tier_low_priority_returns_maintain(self):
        action = self.engine._expansion_action(
            ExpansionReadinessTier.NOT_READY, ExpansionPriority.LOW,
            is_ready=False, needs_interv=False,
        )
        assert action == ExpansionAction.MAINTAIN

    def test_ready_tier_medium_priority_is_ready_engage(self):
        action = self.engine._expansion_action(
            ExpansionReadinessTier.READY, ExpansionPriority.MEDIUM,
            is_ready=True, needs_interv=False,
        )
        assert action == ExpansionAction.ENGAGE


# ─── 14. is_expansion_ready & needs_success_intervention ──────────────────────

class TestExpansionReadyAndIntervention:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_is_ready_true_conditions(self):
        # High everything → readiness >= 60, nps >= 20
        inp = make_input(nps_score=50.0)
        result = self.engine.analyze(inp)
        if result.expansion_readiness_score >= 60.0 and inp.nps_score >= 20.0:
            assert result.is_expansion_ready is True

    def test_is_ready_false_low_nps(self):
        inp = make_input(nps_score=10.0,
                         feature_adoption_rate=100.0, avg_mau_pct=100.0,
                         business_outcomes_pct=100.0, support_health_score=100.0,
                         executive_engagement_score=100.0, champion_strength_score=100.0,
                         contract_size_growth_yoy_pct=100.0, competitor_interest_signals=0)
        result = self.engine.analyze(inp)
        # NPS < 20 → is_expansion_ready False
        assert result.is_expansion_ready is False

    def test_needs_intervention_negative_nps(self):
        inp = make_input(nps_score=-10.0)
        result = self.engine.analyze(inp)
        assert result.needs_success_intervention is True

    def test_needs_intervention_low_support_health(self):
        inp = make_input(support_health_score=30.0)
        result = self.engine.analyze(inp)
        assert result.needs_success_intervention is True

    def test_needs_intervention_low_mau(self):
        inp = make_input(avg_mau_pct=30.0)
        result = self.engine.analyze(inp)
        assert result.needs_success_intervention is True

    def test_no_intervention_healthy_account(self):
        inp = make_input(nps_score=50.0, support_health_score=80.0, avg_mau_pct=75.0)
        result = self.engine.analyze(inp)
        assert result.needs_success_intervention is False

    def test_readiness_threshold_exactly_60(self):
        # Force readiness exactly at boundary via direct score call
        score = self.engine._expansion_readiness_score(60, 60, 60, 60)
        # 60*0.3+60*0.3+60*0.2+60*0.2 = 60
        assert score == 60.0

    def test_intervention_support_score_exactly_40_not_triggered(self):
        inp = make_input(nps_score=50.0, support_health_score=40.0, avg_mau_pct=75.0)
        result = self.engine.analyze(inp)
        # support_health_score < 40 is False (exactly 40)
        assert result.needs_success_intervention is False

    def test_intervention_mau_exactly_40_not_triggered(self):
        inp = make_input(nps_score=50.0, support_health_score=80.0, avg_mau_pct=40.0)
        result = self.engine.analyze(inp)
        assert result.needs_success_intervention is False

    def test_intervention_nps_exactly_0_not_triggered(self):
        inp = make_input(nps_score=0.0, support_health_score=80.0, avg_mau_pct=75.0)
        result = self.engine.analyze(inp)
        # nps < 0 is False
        assert result.needs_success_intervention is False


# ─── 15. _estimated_expansion_arr ─────────────────────────────────────────────

class TestEstimatedExpansionArr:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_low_readiness_returns_zero(self):
        inp = make_input(current_mrr=10_000.0)
        arr = self.engine._estimated_expansion_arr(inp, readiness=34.9)
        assert arr == 0.0

    def test_readiness_35_not_zero(self):
        inp = make_input(current_mrr=10_000.0, seats_used=50, seats_purchased=100,
                         max_seats_available=200, cross_sell_products_eligible=0,
                         feature_adoption_rate=50.0)
        arr = self.engine._estimated_expansion_arr(inp, readiness=35.0)
        assert arr > 0.0

    def test_high_feature_adoption_uses_25pct_upsell(self):
        # feature_adoption_rate >= 70 → upsell = base_arr * 0.25
        inp = make_input(current_mrr=10_000.0, seats_used=100, seats_purchased=100,
                         max_seats_available=100, cross_sell_products_eligible=0,
                         feature_adoption_rate=70.0)
        arr = self.engine._estimated_expansion_arr(inp, readiness=100.0)
        base_arr = 10_000 * 12
        upsell_arr = base_arr * 0.25
        expected = (0 * 0.4 + 0 * 0.3 + upsell_arr * 0.3) * 1.0
        assert arr == round(expected, 2)

    def test_low_feature_adoption_uses_10pct_upsell(self):
        inp = make_input(current_mrr=10_000.0, seats_used=100, seats_purchased=100,
                         max_seats_available=100, cross_sell_products_eligible=0,
                         feature_adoption_rate=69.9)
        arr = self.engine._estimated_expansion_arr(inp, readiness=100.0)
        base_arr = 10_000 * 12
        upsell_arr = base_arr * 0.10
        expected = (0 * 0.4 + 0 * 0.3 + upsell_arr * 0.3) * 1.0
        assert arr == round(expected, 2)

    def test_seat_headroom_contributes(self):
        inp = make_input(current_mrr=10_000.0, seats_used=50, seats_purchased=100,
                         max_seats_available=200, cross_sell_products_eligible=0,
                         feature_adoption_rate=50.0)
        arr = self.engine._estimated_expansion_arr(inp, readiness=100.0)
        # seat_headroom = 200-50=150; seat_arr = (150 * 10000/100)*12 = 180000
        seat_arr = (150 * 10_000 / 100) * 12
        upsell_arr = (10_000 * 12) * 0.10
        expected = (seat_arr * 0.4 + 0 * 0.3 + upsell_arr * 0.3) * 1.0
        assert arr == round(expected, 2)

    def test_cross_sell_contributes(self):
        inp = make_input(current_mrr=10_000.0, seats_used=100, seats_purchased=100,
                         max_seats_available=100, cross_sell_products_eligible=2,
                         feature_adoption_rate=50.0)
        arr = self.engine._estimated_expansion_arr(inp, readiness=100.0)
        base_arr = 10_000 * 12
        cross_sell_arr = 2 * base_arr * 0.15
        upsell_arr = base_arr * 0.10
        expected = (0 * 0.4 + cross_sell_arr * 0.3 + upsell_arr * 0.3) * 1.0
        assert arr == round(expected, 2)

    def test_arr_never_negative(self):
        inp = make_input(current_mrr=0.0, seats_used=0, seats_purchased=1,
                         max_seats_available=1, cross_sell_products_eligible=0,
                         feature_adoption_rate=0.0)
        arr = self.engine._estimated_expansion_arr(inp, readiness=50.0)
        assert arr >= 0.0

    def test_probability_scales_with_readiness(self):
        inp = make_input(current_mrr=10_000.0, seats_used=100, seats_purchased=100,
                         max_seats_available=100, cross_sell_products_eligible=0,
                         feature_adoption_rate=70.0)
        arr_50 = self.engine._estimated_expansion_arr(inp, readiness=50.0)
        arr_100 = self.engine._estimated_expansion_arr(inp, readiness=100.0)
        assert arr_50 < arr_100

    def test_zero_mrr_returns_zero(self):
        inp = make_input(current_mrr=0.0)
        arr = self.engine._estimated_expansion_arr(inp, readiness=80.0)
        assert arr == 0.0


# ─── 16. _expansion_confidence ────────────────────────────────────────────────

class TestExpansionConfidence:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_zero_signals_returns_0(self):
        inp = make_input(expansion_conversations_had=0, upsell_opportunity_count=0,
                         last_qbr_months_ago=99, business_outcomes_pct=50.0,
                         champion_strength_score=50.0)
        assert self.engine._expansion_confidence(inp) == 0.0

    def test_all_five_signals_returns_100(self):
        inp = make_input(expansion_conversations_had=1, upsell_opportunity_count=1,
                         last_qbr_months_ago=3, business_outcomes_pct=80.0,
                         champion_strength_score=70.0)
        assert self.engine._expansion_confidence(inp) == 100.0

    def test_expansion_conversations_signal(self):
        inp = make_input(expansion_conversations_had=1, upsell_opportunity_count=0,
                         last_qbr_months_ago=99, business_outcomes_pct=50.0,
                         champion_strength_score=50.0)
        assert self.engine._expansion_confidence(inp) == 20.0

    def test_upsell_opportunity_signal(self):
        inp = make_input(expansion_conversations_had=0, upsell_opportunity_count=1,
                         last_qbr_months_ago=99, business_outcomes_pct=50.0,
                         champion_strength_score=50.0)
        assert self.engine._expansion_confidence(inp) == 20.0

    def test_qbr_recent_signal(self):
        inp = make_input(expansion_conversations_had=0, upsell_opportunity_count=0,
                         last_qbr_months_ago=6, business_outcomes_pct=50.0,
                         champion_strength_score=50.0)
        assert self.engine._expansion_confidence(inp) == 20.0

    def test_business_outcomes_70_signal(self):
        inp = make_input(expansion_conversations_had=0, upsell_opportunity_count=0,
                         last_qbr_months_ago=99, business_outcomes_pct=70.0,
                         champion_strength_score=50.0)
        assert self.engine._expansion_confidence(inp) == 20.0

    def test_champion_strength_60_signal(self):
        inp = make_input(expansion_conversations_had=0, upsell_opportunity_count=0,
                         last_qbr_months_ago=99, business_outcomes_pct=50.0,
                         champion_strength_score=60.0)
        assert self.engine._expansion_confidence(inp) == 20.0

    def test_qbr_7_months_not_counted(self):
        inp = make_input(expansion_conversations_had=0, upsell_opportunity_count=0,
                         last_qbr_months_ago=7, business_outcomes_pct=50.0,
                         champion_strength_score=50.0)
        assert self.engine._expansion_confidence(inp) == 0.0

    def test_business_outcomes_69_not_counted(self):
        inp = make_input(expansion_conversations_had=0, upsell_opportunity_count=0,
                         last_qbr_months_ago=99, business_outcomes_pct=69.0,
                         champion_strength_score=50.0)
        assert self.engine._expansion_confidence(inp) == 0.0

    def test_champion_strength_59_not_counted(self):
        inp = make_input(expansion_conversations_had=0, upsell_opportunity_count=0,
                         last_qbr_months_ago=99, business_outcomes_pct=50.0,
                         champion_strength_score=59.0)
        assert self.engine._expansion_confidence(inp) == 0.0

    def test_four_signals_returns_80(self):
        inp = make_input(expansion_conversations_had=1, upsell_opportunity_count=1,
                         last_qbr_months_ago=3, business_outcomes_pct=80.0,
                         champion_strength_score=50.0)
        assert self.engine._expansion_confidence(inp) == 80.0

    def test_score_is_float(self):
        inp = make_input()
        conf = self.engine._expansion_confidence(inp)
        assert isinstance(conf, float)


# ─── 17. analyze() integration ────────────────────────────────────────────────

class TestAnalyzeIntegration:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_analyze_returns_result_type(self, default_input):
        result = self.engine.analyze(default_input)
        assert isinstance(result, CustomerExpansionResult)

    def test_analyze_stores_result(self, default_input):
        self.engine.analyze(default_input)
        assert len(self.engine._results) == 1

    def test_analyze_account_id_passthrough(self):
        inp = make_input(account_id="xyz123")
        result = self.engine.analyze(inp)
        assert result.account_id == "xyz123"

    def test_analyze_account_name_passthrough(self):
        inp = make_input(account_name="Widget Inc")
        result = self.engine.analyze(inp)
        assert result.account_name == "Widget Inc"

    def test_analyze_scores_in_range(self):
        result = self.engine.analyze(make_input())
        assert 0.0 <= result.product_depth_score <= 100.0
        assert 0.0 <= result.relationship_strength_score <= 100.0
        assert 0.0 <= result.financial_health_score <= 100.0
        assert 0.0 <= result.timing_score <= 100.0
        assert 0.0 <= result.expansion_readiness_score <= 100.0
        assert 0.0 <= result.expansion_confidence_score <= 100.0

    def test_analyze_returns_valid_enum_tier(self):
        result = self.engine.analyze(make_input())
        assert result.expansion_readiness_tier in ExpansionReadinessTier

    def test_analyze_returns_valid_enum_motion(self):
        result = self.engine.analyze(make_input())
        assert result.expansion_motion in ExpansionMotion

    def test_analyze_returns_valid_enum_priority(self):
        result = self.engine.analyze(make_input())
        assert result.expansion_priority in ExpansionPriority

    def test_analyze_returns_valid_enum_action(self):
        result = self.engine.analyze(make_input())
        assert result.expansion_action in ExpansionAction

    def test_analyze_multiple_appends(self):
        self.engine.analyze(make_input(account_id="a1"))
        self.engine.analyze(make_input(account_id="a2"))
        assert len(self.engine._results) == 2

    def test_analyze_estimated_arr_nonnegative(self):
        result = self.engine.analyze(make_input())
        assert result.estimated_expansion_arr >= 0.0


# ─── 18. analyze_batch() ──────────────────────────────────────────────────────

class TestAnalyzeBatch:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_empty_batch_returns_empty_list(self):
        results = self.engine.analyze_batch([])
        assert results == []

    def test_batch_returns_correct_count(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(5)]
        results = self.engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_batch_all_results_in_engine(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(3)]
        self.engine.analyze_batch(inputs)
        assert len(self.engine._results) == 3

    def test_batch_results_are_result_instances(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(3)]
        results = self.engine.analyze_batch(inputs)
        for r in results:
            assert isinstance(r, CustomerExpansionResult)

    def test_batch_preserves_account_ids(self):
        inputs = [make_input(account_id=f"acct_{i}") for i in range(4)]
        results = self.engine.analyze_batch(inputs)
        for i, r in enumerate(results):
            assert r.account_id == f"acct_{i}"

    def test_batch_cumulative_with_analyze(self):
        self.engine.analyze(make_input(account_id="before"))
        inputs = [make_input(account_id=f"b{i}") for i in range(3)]
        self.engine.analyze_batch(inputs)
        assert len(self.engine._results) == 4

    def test_batch_single_item(self):
        results = self.engine.analyze_batch([make_input(account_id="solo")])
        assert len(results) == 1
        assert results[0].account_id == "solo"


# ─── 19. reset() ──────────────────────────────────────────────────────────────

class TestReset:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_reset_clears_results(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert len(self.engine._results) == 0

    def test_reset_empty_engine_safe(self):
        self.engine.reset()
        assert len(self.engine._results) == 0

    def test_reset_then_analyze(self):
        self.engine.analyze(make_input(account_id="first"))
        self.engine.reset()
        self.engine.analyze(make_input(account_id="second"))
        assert len(self.engine._results) == 1
        assert self.engine._results[0].account_id == "second"

    def test_reset_resets_summary(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        s = self.engine.summary()
        assert s["total"] == 0

    def test_reset_resets_properties(self):
        self.engine.analyze(make_input())
        self.engine.reset()
        assert self.engine.total_expansion_arr == 0.0
        assert self.engine.avg_readiness_score == 0.0

    def test_multiple_resets(self):
        for _ in range(3):
            self.engine.analyze(make_input())
            self.engine.reset()
        assert len(self.engine._results) == 0


# ─── 20. Properties ───────────────────────────────────────────────────────────

class TestProperties:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_expansion_ready_accounts_empty(self):
        assert self.engine.expansion_ready_accounts == []

    def test_intervention_needed_empty(self):
        assert self.engine.intervention_needed == []

    def test_total_expansion_arr_empty(self):
        assert self.engine.total_expansion_arr == 0.0

    def test_avg_readiness_score_empty(self):
        assert self.engine.avg_readiness_score == 0.0

    def test_expansion_ready_accounts_filters_correctly(self):
        # Ready: high readiness + good NPS
        ready_inp = make_input(
            account_id="ready",
            nps_score=50.0,
            feature_adoption_rate=100.0, avg_mau_pct=100.0,
            business_outcomes_pct=100.0, support_health_score=100.0,
            executive_engagement_score=100.0, champion_strength_score=100.0,
            contract_size_growth_yoy_pct=100.0, competitor_interest_signals=0,
            expansion_conversations_had=3, upsell_opportunity_count=3,
            last_qbr_months_ago=1,
        )
        # Not ready: very low scores
        not_ready_inp = make_input(
            account_id="not_ready",
            nps_score=10.0,
            feature_adoption_rate=0.0, avg_mau_pct=0.0,
            business_outcomes_pct=0.0, support_health_score=0.0,
            executive_engagement_score=0.0, champion_strength_score=0.0,
            contract_size_growth_yoy_pct=0.0, competitor_interest_signals=0,
            expansion_conversations_had=0, upsell_opportunity_count=0,
            last_qbr_months_ago=99,
        )
        r_ready = self.engine.analyze(ready_inp)
        r_not_ready = self.engine.analyze(not_ready_inp)
        ready_list = self.engine.expansion_ready_accounts
        for r in ready_list:
            assert r.is_expansion_ready is True

    def test_intervention_needed_filters_correctly(self):
        interv_inp = make_input(account_id="interv", nps_score=-10.0)
        no_interv_inp = make_input(account_id="no_interv", nps_score=50.0,
                                    support_health_score=80.0, avg_mau_pct=75.0)
        self.engine.analyze(interv_inp)
        self.engine.analyze(no_interv_inp)
        for r in self.engine.intervention_needed:
            assert r.needs_success_intervention is True

    def test_total_expansion_arr_sums_correctly(self):
        inp1 = make_input(account_id="a1")
        inp2 = make_input(account_id="a2")
        r1 = self.engine.analyze(inp1)
        r2 = self.engine.analyze(inp2)
        expected = round(r1.estimated_expansion_arr + r2.estimated_expansion_arr, 2)
        assert self.engine.total_expansion_arr == expected

    def test_avg_readiness_score_computed(self):
        inp1 = make_input(account_id="a1")
        inp2 = make_input(account_id="a2")
        r1 = self.engine.analyze(inp1)
        r2 = self.engine.analyze(inp2)
        expected = round((r1.expansion_readiness_score + r2.expansion_readiness_score) / 2, 1)
        assert self.engine.avg_readiness_score == expected

    def test_avg_readiness_rounded_to_1dp(self):
        for i in range(3):
            self.engine.analyze(make_input(account_id=f"a{i}"))
        score = self.engine.avg_readiness_score
        assert score == round(score, 1)

    def test_total_arr_is_float(self):
        self.engine.analyze(make_input())
        assert isinstance(self.engine.total_expansion_arr, float)

    def test_avg_readiness_is_float(self):
        self.engine.analyze(make_input())
        assert isinstance(self.engine.avg_readiness_score, float)


# ─── 21. summary() behavior ───────────────────────────────────────────────────

class TestSummaryBehavior:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_summary_tier_counts_match_analyzed(self):
        self.engine.analyze(make_input(account_id="a1"))
        s = self.engine.summary()
        # All tier counts should sum to total
        total_tiers = sum(s["tier_counts"].values())
        assert total_tiers == s["total"]

    def test_summary_motion_counts_sum_to_total(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(5)]
        self.engine.analyze_batch(inputs)
        s = self.engine.summary()
        assert sum(s["motion_counts"].values()) == s["total"]

    def test_summary_priority_counts_sum_to_total(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(5)]
        self.engine.analyze_batch(inputs)
        s = self.engine.summary()
        assert sum(s["priority_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(5)]
        self.engine.analyze_batch(inputs)
        s = self.engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_ready_count_matches_property(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(4)]
        self.engine.analyze_batch(inputs)
        s = self.engine.summary()
        assert s["ready_count"] == len(self.engine.expansion_ready_accounts)

    def test_summary_intervention_count_matches_property(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(4)]
        self.engine.analyze_batch(inputs)
        s = self.engine.summary()
        assert s["intervention_needed_count"] == len(self.engine.intervention_needed)

    def test_summary_total_arr_matches_property(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(3)]
        self.engine.analyze_batch(inputs)
        s = self.engine.summary()
        assert s["total_estimated_expansion_arr"] == self.engine.total_expansion_arr

    def test_summary_avg_readiness_score(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(3)]
        self.engine.analyze_batch(inputs)
        s = self.engine.summary()
        assert s["avg_expansion_readiness_score"] == self.engine.avg_readiness_score

    def test_summary_counts_are_dicts_after_analyze(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        assert isinstance(s["tier_counts"], dict)
        assert isinstance(s["motion_counts"], dict)
        assert isinstance(s["priority_counts"], dict)
        assert isinstance(s["action_counts"], dict)

    def test_summary_avg_scores_are_float(self):
        self.engine.analyze(make_input())
        s = self.engine.summary()
        for key in [
            "avg_expansion_readiness_score", "avg_product_depth_score",
            "avg_relationship_strength_score", "avg_timing_score",
            "avg_expansion_confidence_score",
        ]:
            assert isinstance(s[key], float), f"{key} should be float"


# ─── 22. End-to-end scenarios ─────────────────────────────────────────────────

class TestEndToEndScenarios:
    def setup_method(self):
        self.engine = CustomerExpansionReadinessEngine()

    def test_low_health_account_gets_nurture_or_maintain(self):
        inp = make_input(
            nps_score=-20.0, support_health_score=20.0, avg_mau_pct=20.0,
            feature_adoption_rate=10.0, executive_engagement_score=10.0,
            champion_strength_score=10.0, contract_size_growth_yoy_pct=-10.0,
            competitor_interest_signals=3,
        )
        result = self.engine.analyze(inp)
        assert result.expansion_action in (ExpansionAction.NURTURE, ExpansionAction.MAINTAIN)

    def test_champion_account_gets_primed_tier(self):
        inp = make_input(
            nps_score=80.0, support_health_score=90.0, avg_mau_pct=90.0,
            feature_adoption_rate=90.0, executive_engagement_score=90.0,
            champion_strength_score=90.0, contract_size_growth_yoy_pct=40.0,
            competitor_interest_signals=0, expansion_conversations_had=3,
            upsell_opportunity_count=3, last_qbr_months_ago=1,
            business_outcomes_pct=90.0, seats_used=90, seats_purchased=100,
            max_seats_available=200,
        )
        result = self.engine.analyze(inp)
        assert result.expansion_readiness_tier == ExpansionReadinessTier.PRIMED

    def test_at_risk_account_needs_intervention(self):
        inp = make_input(nps_score=-50.0, support_health_score=10.0, avg_mau_pct=10.0)
        result = self.engine.analyze(inp)
        assert result.needs_success_intervention is True

    def test_renewal_window_triggers_urgency(self):
        inp = make_input(contract_end_months=2, nps_score=50.0,
                         feature_adoption_rate=80.0, avg_mau_pct=80.0,
                         business_outcomes_pct=80.0, support_health_score=80.0,
                         executive_engagement_score=80.0, champion_strength_score=80.0,
                         expansion_conversations_had=2, upsell_opportunity_count=2)
        result = self.engine.analyze(inp)
        # contract_end_months=2 and reasonable readiness → URGENT
        assert result.expansion_priority == ExpansionPriority.URGENT

    def test_cross_sell_heavy_account(self):
        inp = make_input(
            seats_used=95, seats_purchased=100, max_seats_available=100,
            cross_sell_products_eligible=5, feature_adoption_rate=60.0,
            nps_score=50.0, support_health_score=70.0, avg_mau_pct=70.0,
            business_outcomes_pct=70.0, executive_engagement_score=70.0,
            champion_strength_score=70.0, contract_size_growth_yoy_pct=15.0,
            competitor_interest_signals=0, expansion_conversations_had=2,
            upsell_opportunity_count=2, last_qbr_months_ago=2,
            contract_end_months=6,
        )
        result = self.engine.analyze(inp)
        assert result.expansion_motion == ExpansionMotion.CROSS_SELL

    def test_seat_headroom_account(self):
        inp = make_input(
            seats_used=30, seats_purchased=100, max_seats_available=200,
            feature_adoption_rate=80.0, nps_score=50.0,
            support_health_score=70.0, avg_mau_pct=70.0,
            business_outcomes_pct=70.0, executive_engagement_score=70.0,
            champion_strength_score=70.0, contract_size_growth_yoy_pct=15.0,
            competitor_interest_signals=0,
        )
        result = self.engine.analyze(inp)
        # Large headroom + high prod depth → seat expansion
        assert result.expansion_motion == ExpansionMotion.SEAT_EXPANSION

    def test_batch_then_reset_then_summary(self):
        inputs = [make_input(account_id=f"a{i}") for i in range(5)]
        self.engine.analyze_batch(inputs)
        self.engine.reset()
        s = self.engine.summary()
        assert s["total"] == 0
        assert s["avg_expansion_readiness_score"] == 0.0

    def test_diverse_batch_summary_keys(self):
        inputs = [
            make_input(account_id="a1", nps_score=80.0, support_health_score=90.0),
            make_input(account_id="a2", nps_score=-10.0, support_health_score=20.0),
            make_input(account_id="a3", nps_score=30.0, support_health_score=60.0),
        ]
        self.engine.analyze_batch(inputs)
        s = self.engine.summary()
        assert s["total"] == 3
        assert len(s) == 13

    def test_to_dict_always_has_15_keys_across_inputs(self):
        inputs = [
            make_input(account_id="x1", nps_score=-50.0),
            make_input(account_id="x2", nps_score=80.0),
            make_input(account_id="x3", contract_end_months=2),
            make_input(account_id="x4", cross_sell_products_eligible=5),
        ]
        for inp in inputs:
            result = self.engine.analyze(inp)
            assert len(result.to_dict()) == 15

    def test_full_pipeline_happy_path(self):
        inp = make_input(
            account_id="happy",
            nps_score=70.0,
            feature_adoption_rate=85.0,
            seats_used=80,
            seats_purchased=100,
            max_seats_available=200,
            support_health_score=90.0,
            executive_engagement_score=85.0,
            champion_strength_score=80.0,
            contract_size_growth_yoy_pct=25.0,
            competitor_interest_signals=0,
            expansion_conversations_had=2,
            upsell_opportunity_count=2,
            last_qbr_months_ago=2,
            business_outcomes_pct=85.0,
            avg_mau_pct=85.0,
            contract_end_months=6,
            cross_sell_products_eligible=2,
        )
        result = self.engine.analyze(inp)
        assert result.expansion_readiness_score > 60
        assert result.is_expansion_ready is True
        assert result.needs_success_intervention is False
        assert result.estimated_expansion_arr > 0

    def test_full_pipeline_at_risk(self):
        inp = make_input(
            account_id="risk",
            nps_score=-30.0,
            feature_adoption_rate=15.0,
            seats_used=20,
            seats_purchased=100,
            max_seats_available=150,
            support_health_score=15.0,
            executive_engagement_score=10.0,
            champion_strength_score=10.0,
            contract_size_growth_yoy_pct=-20.0,
            competitor_interest_signals=5,
            expansion_conversations_had=0,
            upsell_opportunity_count=0,
            last_qbr_months_ago=18,
            business_outcomes_pct=10.0,
            avg_mau_pct=15.0,
            contract_end_months=24,
            cross_sell_products_eligible=0,
        )
        result = self.engine.analyze(inp)
        assert result.needs_success_intervention is True
        assert result.is_expansion_ready is False
        assert result.expansion_readiness_tier in (
            ExpansionReadinessTier.NOT_READY, ExpansionReadinessTier.BUILDING
        )

    def test_engine_init_fresh(self):
        eng = CustomerExpansionReadinessEngine()
        assert eng._results == []
        assert eng.avg_readiness_score == 0.0
        assert eng.total_expansion_arr == 0.0

    def test_result_is_dataclass(self):
        import dataclasses
        result = self.engine.analyze(make_input())
        assert dataclasses.is_dataclass(result)

    def test_input_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(CustomerExpansionInput)

    def test_result_has_15_fields(self):
        import dataclasses
        fields = dataclasses.fields(CustomerExpansionResult)
        assert len(fields) == 15
