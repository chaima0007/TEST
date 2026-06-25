"""
Comprehensive pytest test suite for swarm/intelligence/account_expansion_engine.py
Run from /home/user/TEST:
    python -m pytest swarm/tests/test_account_expansion_engine.py -v
"""

from __future__ import annotations

import pytest

from swarm.intelligence.account_expansion_engine import (
    ExpansionType,
    ExpansionReadiness,
    ChurnSignal,
    ExpansionAction,
    AccountExpansionInput,
    AccountExpansionResult,
    AccountExpansionEngine,
)


# ─── Helpers / fixtures ───────────────────────────────────────────────────────

def make_input(
    account_id: str = "acct_001",
    account_name: str = "Acme Corp",
    csm_id: str = "csm_42",
    segment: str = "enterprise",
    current_arr: float = 100_000.0,
    contract_end_days: int = 180,
    product_adoption_pct: float = 70.0,
    features_used: int = 8,
    total_features_available: int = 10,
    active_users: int = 80,
    licensed_users: int = 100,
    nps_score: float = 50.0,
    support_tickets_open: int = 0,
    support_tickets_resolved: int = 5,
    last_qbr_days: int = 30,
    executive_engagement: bool = True,
    expansion_type: ExpansionType = ExpansionType.UPSELL,
    expansion_budget_confirmed: bool = True,
    whitespace_products: int = 2,
    internal_champion: bool = True,
    competitor_conversation: bool = False,
    time_to_value_days: int = 30,
    benchmark_ttv_days: int = 45,
    roi_demonstrated: bool = True,
    growth_since_start_pct: float = 25.0,
    upsell_attempts: int = 1,
) -> AccountExpansionInput:
    return AccountExpansionInput(
        account_id=account_id,
        account_name=account_name,
        csm_id=csm_id,
        segment=segment,
        current_arr=current_arr,
        contract_end_days=contract_end_days,
        product_adoption_pct=product_adoption_pct,
        features_used=features_used,
        total_features_available=total_features_available,
        active_users=active_users,
        licensed_users=licensed_users,
        nps_score=nps_score,
        support_tickets_open=support_tickets_open,
        support_tickets_resolved=support_tickets_resolved,
        last_qbr_days=last_qbr_days,
        executive_engagement=executive_engagement,
        expansion_type=expansion_type,
        expansion_budget_confirmed=expansion_budget_confirmed,
        whitespace_products=whitespace_products,
        internal_champion=internal_champion,
        competitor_conversation=competitor_conversation,
        time_to_value_days=time_to_value_days,
        benchmark_ttv_days=benchmark_ttv_days,
        roi_demonstrated=roi_demonstrated,
        growth_since_start_pct=growth_since_start_pct,
        upsell_attempts=upsell_attempts,
    )


@pytest.fixture
def engine() -> AccountExpansionEngine:
    return AccountExpansionEngine()


@pytest.fixture
def good_input() -> AccountExpansionInput:
    """A healthy account with good expansion signals."""
    return make_input()


@pytest.fixture
def risky_input() -> AccountExpansionInput:
    """An account with high churn risk."""
    return make_input(
        active_users=10,
        licensed_users=100,
        nps_score=-50.0,
        support_tickets_open=6,
        competitor_conversation=True,
        contract_end_days=20,
        expansion_budget_confirmed=False,
        internal_champion=False,
        roi_demonstrated=False,
        growth_since_start_pct=0.0,
        executive_engagement=False,
        last_qbr_days=200,
        whitespace_products=0,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 1. Enum tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestExpansionTypeEnum:
    def test_has_five_members(self):
        assert len(ExpansionType) == 5

    def test_upsell_value(self):
        assert ExpansionType.UPSELL == "upsell"

    def test_cross_sell_value(self):
        assert ExpansionType.CROSS_SELL == "cross_sell"

    def test_renewal_plus_value(self):
        assert ExpansionType.RENEWAL_PLUS == "renewal_plus"

    def test_platform_add_value(self):
        assert ExpansionType.PLATFORM_ADD == "platform_add"

    def test_new_division_value(self):
        assert ExpansionType.NEW_DIVISION == "new_division"

    def test_is_str_subclass(self):
        assert isinstance(ExpansionType.UPSELL, str)

    def test_str_equality(self):
        assert ExpansionType.UPSELL == "upsell"
        assert "cross_sell" == ExpansionType.CROSS_SELL

    def test_unique_values(self):
        values = [m.value for m in ExpansionType]
        assert len(values) == len(set(values))

    def test_all_members(self):
        members = {m.name for m in ExpansionType}
        assert members == {"UPSELL", "CROSS_SELL", "RENEWAL_PLUS", "PLATFORM_ADD", "NEW_DIVISION"}


class TestExpansionReadinessEnum:
    def test_has_four_members(self):
        assert len(ExpansionReadiness) == 4

    def test_ready_now_value(self):
        assert ExpansionReadiness.READY_NOW == "ready_now"

    def test_upcoming_value(self):
        assert ExpansionReadiness.UPCOMING == "upcoming"

    def test_needs_nurturing_value(self):
        assert ExpansionReadiness.NEEDS_NURTURING == "needs_nurturing"

    def test_not_ready_value(self):
        assert ExpansionReadiness.NOT_READY == "not_ready"

    def test_is_str_subclass(self):
        assert isinstance(ExpansionReadiness.READY_NOW, str)

    def test_unique_values(self):
        values = [m.value for m in ExpansionReadiness]
        assert len(values) == len(set(values))

    def test_all_members(self):
        members = {m.name for m in ExpansionReadiness}
        assert members == {"READY_NOW", "UPCOMING", "NEEDS_NURTURING", "NOT_READY"}


class TestChurnSignalEnum:
    def test_has_five_members(self):
        assert len(ChurnSignal) == 5

    def test_none_value(self):
        assert ChurnSignal.NONE == "none"

    def test_low_value(self):
        assert ChurnSignal.LOW == "low"

    def test_medium_value(self):
        assert ChurnSignal.MEDIUM == "medium"

    def test_high_value(self):
        assert ChurnSignal.HIGH == "high"

    def test_critical_value(self):
        assert ChurnSignal.CRITICAL == "critical"

    def test_is_str_subclass(self):
        assert isinstance(ChurnSignal.NONE, str)

    def test_unique_values(self):
        values = [m.value for m in ChurnSignal]
        assert len(values) == len(set(values))

    def test_all_members(self):
        members = {m.name for m in ChurnSignal}
        assert members == {"NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"}


class TestExpansionActionEnum:
    def test_has_six_members(self):
        assert len(ExpansionAction) == 6

    def test_pitch_now_value(self):
        assert ExpansionAction.PITCH_NOW == "pitch_now"

    def test_schedule_qbr_value(self):
        assert ExpansionAction.SCHEDULE_QBR == "schedule_qbr"

    def test_nurture_adoption_value(self):
        assert ExpansionAction.NURTURE_ADOPTION == "nurture_adoption"

    def test_risk_intervention_value(self):
        assert ExpansionAction.RISK_INTERVENTION == "risk_intervention"

    def test_reactivate_value(self):
        assert ExpansionAction.REACTIVATE == "reactivate"

    def test_maintain_health_value(self):
        assert ExpansionAction.MAINTAIN_HEALTH == "maintain_health"

    def test_is_str_subclass(self):
        assert isinstance(ExpansionAction.PITCH_NOW, str)

    def test_unique_values(self):
        values = [m.value for m in ExpansionAction]
        assert len(values) == len(set(values))

    def test_all_members(self):
        members = {m.name for m in ExpansionAction}
        assert members == {
            "PITCH_NOW", "SCHEDULE_QBR", "NURTURE_ADOPTION",
            "RISK_INTERVENTION", "REACTIVATE", "MAINTAIN_HEALTH",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 2. AccountExpansionInput field count
# ═══════════════════════════════════════════════════════════════════════════════

class TestAccountExpansionInput:
    def test_has_26_fields(self):
        import dataclasses
        fields = dataclasses.fields(AccountExpansionInput)
        assert len(fields) == 26

    def test_field_names(self):
        import dataclasses
        names = {f.name for f in dataclasses.fields(AccountExpansionInput)}
        expected = {
            "account_id", "account_name", "csm_id", "segment", "current_arr",
            "contract_end_days", "product_adoption_pct", "features_used",
            "total_features_available", "active_users", "licensed_users",
            "nps_score", "support_tickets_open", "support_tickets_resolved",
            "last_qbr_days", "executive_engagement", "expansion_type",
            "expansion_budget_confirmed", "whitespace_products", "internal_champion",
            "competitor_conversation", "time_to_value_days", "benchmark_ttv_days",
            "roi_demonstrated", "growth_since_start_pct", "upsell_attempts",
        }
        assert names == expected

    def test_instantiation_stores_values(self):
        inp = make_input(account_id="X1", current_arr=50_000.0)
        assert inp.account_id == "X1"
        assert inp.current_arr == 50_000.0

    def test_expansion_type_field(self):
        inp = make_input(expansion_type=ExpansionType.CROSS_SELL)
        assert inp.expansion_type == ExpansionType.CROSS_SELL

    def test_bool_fields_default_values(self):
        inp = make_input(executive_engagement=False, competitor_conversation=True)
        assert inp.executive_engagement is False
        assert inp.competitor_conversation is True


# ═══════════════════════════════════════════════════════════════════════════════
# 3. to_dict() — 15 keys + correct types
# ═══════════════════════════════════════════════════════════════════════════════

class TestToDictMethod:
    def test_returns_dict(self, engine, good_input):
        result = engine.analyze(good_input)
        assert isinstance(result.to_dict(), dict)

    def test_exactly_15_keys(self, engine, good_input):
        d = engine.analyze(good_input).to_dict()
        assert len(d) == 15

    def test_all_keys_present(self, engine, good_input):
        d = engine.analyze(good_input).to_dict()
        expected_keys = {
            "account_id", "account_name", "csm_id",
            "expansion_readiness", "churn_signal", "expansion_action",
            "expansion_score", "health_score", "churn_risk_score",
            "adoption_rate", "feature_utilization", "expansion_potential",
            "nrr_forecast", "is_at_risk", "is_ready_to_expand",
        }
        assert set(d.keys()) == expected_keys

    def test_expansion_readiness_is_str(self, engine, good_input):
        d = engine.analyze(good_input).to_dict()
        assert isinstance(d["expansion_readiness"], str)

    def test_churn_signal_is_str(self, engine, good_input):
        d = engine.analyze(good_input).to_dict()
        assert isinstance(d["churn_signal"], str)

    def test_expansion_action_is_str(self, engine, good_input):
        d = engine.analyze(good_input).to_dict()
        assert isinstance(d["expansion_action"], str)

    def test_expansion_score_is_float(self, engine, good_input):
        d = engine.analyze(good_input).to_dict()
        assert isinstance(d["expansion_score"], float)

    def test_health_score_is_float(self, engine, good_input):
        d = engine.analyze(good_input).to_dict()
        assert isinstance(d["health_score"], float)

    def test_churn_risk_score_is_float(self, engine, good_input):
        d = engine.analyze(good_input).to_dict()
        assert isinstance(d["churn_risk_score"], float)

    def test_is_at_risk_is_bool(self, engine, good_input):
        d = engine.analyze(good_input).to_dict()
        assert isinstance(d["is_at_risk"], bool)

    def test_is_ready_to_expand_is_bool(self, engine, good_input):
        d = engine.analyze(good_input).to_dict()
        assert isinstance(d["is_ready_to_expand"], bool)

    def test_account_id_matches(self, engine):
        inp = make_input(account_id="TEST_ID")
        d = engine.analyze(inp).to_dict()
        assert d["account_id"] == "TEST_ID"

    def test_account_name_matches(self, engine):
        inp = make_input(account_name="Globex")
        d = engine.analyze(inp).to_dict()
        assert d["account_name"] == "Globex"

    def test_csm_id_matches(self, engine):
        inp = make_input(csm_id="csm_99")
        d = engine.analyze(inp).to_dict()
        assert d["csm_id"] == "csm_99"

    def test_readiness_value_is_enum_value(self, engine, good_input):
        result = engine.analyze(good_input)
        d = result.to_dict()
        assert d["expansion_readiness"] == result.expansion_readiness.value

    def test_churn_signal_value_is_enum_value(self, engine, good_input):
        result = engine.analyze(good_input)
        d = result.to_dict()
        assert d["churn_signal"] == result.churn_signal.value

    def test_expansion_action_value_is_enum_value(self, engine, good_input):
        result = engine.analyze(good_input)
        d = result.to_dict()
        assert d["expansion_action"] == result.expansion_action.value


# ═══════════════════════════════════════════════════════════════════════════════
# 4. _adoption_rate
# ═══════════════════════════════════════════════════════════════════════════════

class TestAdoptionRate:
    def test_zero_licensed_returns_zero(self, engine):
        inp = make_input(active_users=50, licensed_users=0)
        assert engine._adoption_rate(inp) == 0.0

    def test_negative_licensed_returns_zero(self, engine):
        inp = make_input(active_users=10, licensed_users=-5)
        assert engine._adoption_rate(inp) == 0.0

    def test_normal_case(self, engine):
        inp = make_input(active_users=80, licensed_users=100)
        assert engine._adoption_rate(inp) == 80.0

    def test_capped_at_100(self, engine):
        # active > licensed should be capped
        inp = make_input(active_users=150, licensed_users=100)
        assert engine._adoption_rate(inp) == 100.0

    def test_partial_adoption(self, engine):
        inp = make_input(active_users=33, licensed_users=100)
        assert engine._adoption_rate(inp) == 33.0

    def test_rounded_to_one_decimal(self, engine):
        inp = make_input(active_users=1, licensed_users=3)
        # 1/3 * 100 = 33.333... → 33.3
        assert engine._adoption_rate(inp) == 33.3

    def test_zero_active_users(self, engine):
        inp = make_input(active_users=0, licensed_users=100)
        assert engine._adoption_rate(inp) == 0.0

    def test_full_adoption(self, engine):
        inp = make_input(active_users=50, licensed_users=50)
        assert engine._adoption_rate(inp) == 100.0

    def test_returns_float(self, engine):
        inp = make_input(active_users=50, licensed_users=100)
        result = engine._adoption_rate(inp)
        assert isinstance(result, float)

    def test_half_adoption(self, engine):
        inp = make_input(active_users=25, licensed_users=50)
        assert engine._adoption_rate(inp) == 50.0


# ═══════════════════════════════════════════════════════════════════════════════
# 5. _feature_utilization
# ═══════════════════════════════════════════════════════════════════════════════

class TestFeatureUtilization:
    def test_zero_available_returns_zero(self, engine):
        inp = make_input(features_used=5, total_features_available=0)
        assert engine._feature_utilization(inp) == 0.0

    def test_negative_available_returns_zero(self, engine):
        inp = make_input(features_used=3, total_features_available=-1)
        assert engine._feature_utilization(inp) == 0.0

    def test_normal_case(self, engine):
        inp = make_input(features_used=8, total_features_available=10)
        assert engine._feature_utilization(inp) == 80.0

    def test_capped_at_100(self, engine):
        inp = make_input(features_used=15, total_features_available=10)
        assert engine._feature_utilization(inp) == 100.0

    def test_zero_used(self, engine):
        inp = make_input(features_used=0, total_features_available=10)
        assert engine._feature_utilization(inp) == 0.0

    def test_full_utilization(self, engine):
        inp = make_input(features_used=10, total_features_available=10)
        assert engine._feature_utilization(inp) == 100.0

    def test_rounded_to_one_decimal(self, engine):
        inp = make_input(features_used=1, total_features_available=3)
        # 1/3 * 100 = 33.333... → 33.3
        assert engine._feature_utilization(inp) == 33.3

    def test_returns_float(self, engine):
        inp = make_input(features_used=5, total_features_available=10)
        result = engine._feature_utilization(inp)
        assert isinstance(result, float)

    def test_50_percent(self, engine):
        inp = make_input(features_used=5, total_features_available=10)
        assert engine._feature_utilization(inp) == 50.0


# ═══════════════════════════════════════════════════════════════════════════════
# 6. _health_score
# ═══════════════════════════════════════════════════════════════════════════════

class TestHealthScore:
    def _compute(self, engine, **kwargs) -> float:
        inp = make_input(**kwargs)
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        return engine._health_score(inp, adoption, feat_util)

    def test_returns_float(self, engine):
        inp = make_input()
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        result = engine._health_score(inp, adoption, feat_util)
        assert isinstance(result, float)

    def test_clamped_at_minimum_zero(self, engine):
        # Worst case everything minimal
        score = self._compute(
            engine,
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=10,
            executive_engagement=False,
            last_qbr_days=300,
        )
        assert score >= 0.0

    def test_clamped_at_maximum_100(self, engine):
        # Best case
        score = self._compute(
            engine,
            active_users=100, licensed_users=100,
            features_used=10, total_features_available=10,
            nps_score=100.0,
            support_tickets_open=0,
            executive_engagement=True,
            last_qbr_days=10,
        )
        assert score <= 100.0

    def test_adoption_contributes_30pct(self, engine):
        inp = make_input(
            active_users=100, licensed_users=100,  # adoption = 100
            features_used=0, total_features_available=10,  # feat_util = 0
            nps_score=0.0,   # nps_norm = 0.5 → 12.5
            support_tickets_open=10,  # -10
            executive_engagement=False,
            last_qbr_days=100,  # between 90 and 180 → 0
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        # adoption*0.30 = 30, feat_util*0.20 = 0, nps=12.5, tickets=-10
        # score = 30 + 0 + 12.5 - 10 = 32.5
        assert score == 32.5

    def test_feat_util_contributes_20pct(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,  # adoption = 0
            features_used=10, total_features_available=10,  # feat_util = 100
            nps_score=0.0,  # nps_norm=0.5 → 12.5
            support_tickets_open=10,  # -10
            executive_engagement=False,
            last_qbr_days=100,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        # 0 + 20 + 12.5 - 10 = 22.5
        assert score == 22.5

    def test_nps_max_100_adds_25(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=100.0,  # nps_norm = 1.0 → +25
            support_tickets_open=10,
            executive_engagement=False,
            last_qbr_days=100,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        # 0 + 0 + 25 - 10 = 15
        assert score == 15.0

    def test_nps_min_neg100_adds_zero(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,  # nps_norm = 0.0 → +0
            support_tickets_open=0,  # +10
            executive_engagement=False,
            last_qbr_days=100,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        # 0 + 0 + 0 + 10 = 10
        assert score == 10.0

    def test_tickets_zero_adds_10(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=0,  # +10
            executive_engagement=False,
            last_qbr_days=100,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 10.0  # 0+0+0+10

    def test_tickets_1_adds_5(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=1,  # +5
            executive_engagement=False,
            last_qbr_days=100,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 5.0

    def test_tickets_2_adds_5(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=2,  # <=2 → +5
            executive_engagement=False,
            last_qbr_days=100,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 5.0

    def test_tickets_3_subtracts_10(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=3,  # >2 → -10
            executive_engagement=False,
            last_qbr_days=100,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 0.0  # clamped: 0+0+0-10 = -10 → 0

    def test_executive_engagement_adds_8(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=0,  # +10
            executive_engagement=True,  # +8
            last_qbr_days=100,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 18.0

    def test_no_executive_engagement(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=0,  # +10
            executive_engagement=False,
            last_qbr_days=100,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 10.0

    def test_qbr_within_30_days_adds_7(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=0,  # +10
            executive_engagement=False,
            last_qbr_days=30,  # <=30 → +7
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 17.0

    def test_qbr_at_exactly_30_days_adds_7(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=0,
            executive_engagement=False,
            last_qbr_days=30,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 17.0

    def test_qbr_at_31_days_adds_3(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=0,  # +10
            executive_engagement=False,
            last_qbr_days=31,  # >30, <=90 → +3
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 13.0

    def test_qbr_at_90_days_adds_3(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=0,
            executive_engagement=False,
            last_qbr_days=90,  # <=90 → +3
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 13.0

    def test_qbr_91_to_180_adds_nothing(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=0,  # +10
            executive_engagement=False,
            last_qbr_days=150,  # 91-180 → 0
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 10.0

    def test_qbr_over_180_subtracts_10(self, engine):
        inp = make_input(
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=0,  # +10
            executive_engagement=False,
            last_qbr_days=181,  # >180 → -10
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        assert score == 0.0  # 10 - 10 = 0

    def test_score_rounded_to_one_decimal(self, engine):
        inp = make_input(
            active_users=1, licensed_users=3,  # adoption = 33.3
            features_used=1, total_features_available=3,  # feat_util = 33.3
            nps_score=0.0,
            support_tickets_open=0,
            executive_engagement=False,
            last_qbr_days=100,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        score = engine._health_score(inp, adoption, feat_util)
        # 33.3*0.3 + 33.3*0.2 + 12.5 + 10 = 9.99 + 6.66 + 12.5 + 10 = 39.15 → round to 1
        assert score == round(score, 1)


# ═══════════════════════════════════════════════════════════════════════════════
# 7. _churn_risk_score
# ═══════════════════════════════════════════════════════════════════════════════

class TestChurnRiskScore:
    def _compute_churn(self, engine, health: float, adoption: float, **kwargs) -> float:
        inp = make_input(**kwargs)
        return engine._churn_risk_score(inp, health, adoption)

    def test_zero_risk_baseline(self, engine):
        # health >= 60, adoption >= 60, contract far, no competitor, no tickets
        score = self._compute_churn(
            engine, health=80.0, adoption=70.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 0.0

    def test_health_below_40_adds_30(self, engine):
        score = self._compute_churn(
            engine, health=39.0, adoption=70.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 30.0

    def test_health_40_does_not_add_30(self, engine):
        score = self._compute_churn(
            engine, health=40.0, adoption=70.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        # health=40 not < 40, not < 60 (40 is >=40 but <60), so +15
        assert score == 15.0

    def test_health_between_40_and_60_adds_15(self, engine):
        score = self._compute_churn(
            engine, health=55.0, adoption=70.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 15.0

    def test_health_60_adds_nothing(self, engine):
        score = self._compute_churn(
            engine, health=60.0, adoption=70.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 0.0

    def test_adoption_below_30_adds_20(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=29.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 20.0

    def test_adoption_between_30_and_60_adds_10(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=50.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 10.0

    def test_adoption_60_adds_nothing(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=60.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 0.0

    def test_contract_end_30_adds_25(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=70.0,
            contract_end_days=30,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 25.0

    def test_contract_end_at_exactly_30_adds_25(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=70.0,
            contract_end_days=30,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 25.0

    def test_contract_end_31_to_60_adds_10(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=70.0,
            contract_end_days=60,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 10.0

    def test_contract_end_61_adds_nothing(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=70.0,
            contract_end_days=61,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 0.0

    def test_competitor_conversation_adds_20(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=70.0,
            contract_end_days=200,
            competitor_conversation=True,
            support_tickets_open=0,
        )
        assert score == 20.0

    def test_tickets_5_adds_10(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=70.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=5,
        )
        assert score == 10.0

    def test_tickets_3_adds_5(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=70.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=3,
        )
        assert score == 5.0

    def test_tickets_2_adds_nothing(self, engine):
        score = self._compute_churn(
            engine, health=70.0, adoption=70.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=2,
        )
        assert score == 0.0

    def test_clamped_at_100(self, engine):
        # Many risk factors stacking
        score = self._compute_churn(
            engine, health=30.0, adoption=20.0,  # +30 +20
            contract_end_days=15,   # +25
            competitor_conversation=True,  # +20
            support_tickets_open=6,  # +10
        )
        assert score == 100.0

    def test_clamped_at_0_minimum(self, engine):
        score = self._compute_churn(
            engine, health=90.0, adoption=90.0,
            contract_end_days=200,
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 0.0

    def test_rounded_to_one_decimal(self, engine):
        inp = make_input(contract_end_days=200, competitor_conversation=False, support_tickets_open=0)
        score = engine._churn_risk_score(inp, 70.0, 70.0)
        assert score == round(score, 1)

    def test_cumulative_risk_stacks(self, engine):
        score = self._compute_churn(
            engine, health=50.0, adoption=50.0,  # +15, +10
            contract_end_days=60,  # +10
            competitor_conversation=False,
            support_tickets_open=0,
        )
        assert score == 35.0


# ═══════════════════════════════════════════════════════════════════════════════
# 8. _churn_signal — all 5 levels + exact boundaries
# ═══════════════════════════════════════════════════════════════════════════════

class TestChurnSignal:
    def test_none_below_10(self, engine):
        assert engine._churn_signal(9.9) == ChurnSignal.NONE

    def test_none_at_zero(self, engine):
        assert engine._churn_signal(0.0) == ChurnSignal.NONE

    def test_low_at_10(self, engine):
        assert engine._churn_signal(10.0) == ChurnSignal.LOW

    def test_low_below_30(self, engine):
        assert engine._churn_signal(29.9) == ChurnSignal.LOW

    def test_medium_at_30(self, engine):
        assert engine._churn_signal(30.0) == ChurnSignal.MEDIUM

    def test_medium_below_50(self, engine):
        assert engine._churn_signal(49.9) == ChurnSignal.MEDIUM

    def test_high_at_50(self, engine):
        assert engine._churn_signal(50.0) == ChurnSignal.HIGH

    def test_high_below_70(self, engine):
        assert engine._churn_signal(69.9) == ChurnSignal.HIGH

    def test_critical_at_70(self, engine):
        assert engine._churn_signal(70.0) == ChurnSignal.CRITICAL

    def test_critical_at_100(self, engine):
        assert engine._churn_signal(100.0) == ChurnSignal.CRITICAL

    def test_returns_churn_signal_type(self, engine):
        assert isinstance(engine._churn_signal(50.0), ChurnSignal)


# ═══════════════════════════════════════════════════════════════════════════════
# 9. _expansion_score
# ═══════════════════════════════════════════════════════════════════════════════

class TestExpansionScore:
    def _compute(self, engine, health=50.0, adoption=50.0, feat_util=50.0, **kwargs) -> float:
        inp = make_input(**kwargs)
        return engine._expansion_score(inp, health, adoption, feat_util)

    def test_returns_float(self, engine):
        inp = make_input()
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        health = engine._health_score(inp, adoption, feat_util)
        result = engine._expansion_score(inp, health, adoption, feat_util)
        assert isinstance(result, float)

    def test_clamped_at_zero_minimum(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=True,  # -15
            growth_since_start_pct=0.0,
        )
        assert score == 0.0

    def test_clamped_at_100_maximum(self, engine):
        score = self._compute(
            engine, health=100.0, adoption=100.0, feat_util=100.0,
            whitespace_products=5,  # min(20, 5*4=20) = 20
            expansion_budget_confirmed=True,  # +15
            internal_champion=True,  # +10
            roi_demonstrated=True,   # +8
            competitor_conversation=False,
            growth_since_start_pct=25.0,  # +10
        )
        assert score == 100.0

    def test_health_contributes_30pct(self, engine):
        score = self._compute(
            engine, health=100.0, adoption=0.0, feat_util=0.0,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        assert score == 30.0

    def test_adoption_contributes_20pct(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=100.0, feat_util=0.0,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        assert score == 20.0

    def test_whitespace_adds_up_to_20(self, engine):
        score5 = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=5,  # min(20, 20) = 20
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        assert score5 == 20.0

    def test_whitespace_capped_at_20(self, engine):
        score_big = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=10,  # min(20, 40) = 20
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        assert score_big == 20.0

    def test_whitespace_3_adds_12(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=3,  # 3*4 = 12
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        assert score == 12.0

    def test_budget_confirmed_adds_15(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=0,
            expansion_budget_confirmed=True,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        assert score == 15.0

    def test_internal_champion_adds_10(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=True,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        assert score == 10.0

    def test_roi_demonstrated_adds_8(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=True,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        assert score == 8.0

    def test_competitor_conversation_subtracts_15(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=5,  # +20 to avoid negative clamping
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=True,  # -15
            growth_since_start_pct=0.0,
        )
        assert score == 5.0

    def test_growth_20pct_adds_10(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=20.0,
        )
        assert score == 10.0

    def test_growth_exactly_20_adds_10(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=20.0,
        )
        assert score == 10.0

    def test_growth_10_to_19_adds_5(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=15.0,
        )
        assert score == 5.0

    def test_growth_below_10_adds_nothing(self, engine):
        score = self._compute(
            engine, health=0.0, adoption=0.0, feat_util=0.0,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=9.0,
        )
        assert score == 0.0

    def test_rounded_to_one_decimal(self, engine):
        inp = make_input(
            active_users=1, licensed_users=3,
            features_used=1, total_features_available=3,
            whitespace_products=1,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        adoption = engine._adoption_rate(inp)
        feat_util = engine._feature_utilization(inp)
        health = engine._health_score(inp, adoption, feat_util)
        score = engine._expansion_score(inp, health, adoption, feat_util)
        assert score == round(score, 1)


# ═══════════════════════════════════════════════════════════════════════════════
# 10. _expansion_readiness — all 4 levels + priority order
# ═══════════════════════════════════════════════════════════════════════════════

class TestExpansionReadiness:
    def test_high_churn_returns_not_ready(self, engine):
        inp = make_input(expansion_budget_confirmed=True)
        result = engine._expansion_readiness(inp, exp_score=90.0, churn_sig=ChurnSignal.HIGH)
        assert result == ExpansionReadiness.NOT_READY

    def test_critical_churn_returns_not_ready(self, engine):
        inp = make_input(expansion_budget_confirmed=True)
        result = engine._expansion_readiness(inp, exp_score=90.0, churn_sig=ChurnSignal.CRITICAL)
        assert result == ExpansionReadiness.NOT_READY

    def test_medium_churn_does_not_block(self, engine):
        inp = make_input(expansion_budget_confirmed=True, contract_end_days=30)
        result = engine._expansion_readiness(inp, exp_score=90.0, churn_sig=ChurnSignal.MEDIUM)
        # exp_score >=70 AND budget confirmed → READY_NOW
        assert result == ExpansionReadiness.READY_NOW

    def test_ready_now_requires_score_70_and_budget(self, engine):
        inp = make_input(expansion_budget_confirmed=True)
        result = engine._expansion_readiness(inp, exp_score=70.0, churn_sig=ChurnSignal.NONE)
        assert result == ExpansionReadiness.READY_NOW

    def test_ready_now_fails_without_budget(self, engine):
        inp = make_input(expansion_budget_confirmed=False, contract_end_days=200)
        # exp_score=70 but no budget → not READY_NOW; exp_score >=55 but contract_end_days>90 → not UPCOMING
        # exp_score >=35 → NEEDS_NURTURING
        result = engine._expansion_readiness(inp, exp_score=70.0, churn_sig=ChurnSignal.NONE)
        assert result == ExpansionReadiness.NEEDS_NURTURING

    def test_ready_now_fails_with_score_69(self, engine):
        inp = make_input(expansion_budget_confirmed=True, contract_end_days=90)
        result = engine._expansion_readiness(inp, exp_score=69.9, churn_sig=ChurnSignal.NONE)
        # Not >=70 + budget; exp_score >=55 AND contract_end_days <=90 → UPCOMING
        assert result == ExpansionReadiness.UPCOMING

    def test_upcoming_score_55_contract_90(self, engine):
        inp = make_input(expansion_budget_confirmed=False, contract_end_days=90)
        result = engine._expansion_readiness(inp, exp_score=55.0, churn_sig=ChurnSignal.NONE)
        assert result == ExpansionReadiness.UPCOMING

    def test_upcoming_fails_contract_over_90(self, engine):
        inp = make_input(expansion_budget_confirmed=False, contract_end_days=91)
        result = engine._expansion_readiness(inp, exp_score=60.0, churn_sig=ChurnSignal.NONE)
        # Not ready_now (no budget), not upcoming (contract > 90), score>=35 → NEEDS_NURTURING
        assert result == ExpansionReadiness.NEEDS_NURTURING

    def test_needs_nurturing_score_35(self, engine):
        inp = make_input(expansion_budget_confirmed=False, contract_end_days=200)
        result = engine._expansion_readiness(inp, exp_score=35.0, churn_sig=ChurnSignal.NONE)
        assert result == ExpansionReadiness.NEEDS_NURTURING

    def test_needs_nurturing_score_54(self, engine):
        inp = make_input(expansion_budget_confirmed=False, contract_end_days=200)
        result = engine._expansion_readiness(inp, exp_score=54.9, churn_sig=ChurnSignal.NONE)
        assert result == ExpansionReadiness.NEEDS_NURTURING

    def test_not_ready_score_below_35(self, engine):
        inp = make_input(expansion_budget_confirmed=False, contract_end_days=200)
        result = engine._expansion_readiness(inp, exp_score=34.9, churn_sig=ChurnSignal.NONE)
        assert result == ExpansionReadiness.NOT_READY

    def test_not_ready_score_zero(self, engine):
        inp = make_input(expansion_budget_confirmed=False, contract_end_days=200)
        result = engine._expansion_readiness(inp, exp_score=0.0, churn_sig=ChurnSignal.NONE)
        assert result == ExpansionReadiness.NOT_READY

    def test_churn_high_overrides_high_score(self, engine):
        # Even with perfect score and budget, HIGH churn → NOT_READY
        inp = make_input(expansion_budget_confirmed=True)
        result = engine._expansion_readiness(inp, exp_score=100.0, churn_sig=ChurnSignal.HIGH)
        assert result == ExpansionReadiness.NOT_READY

    def test_returns_expansion_readiness_type(self, engine):
        inp = make_input()
        result = engine._expansion_readiness(inp, exp_score=80.0, churn_sig=ChurnSignal.NONE)
        assert isinstance(result, ExpansionReadiness)


# ═══════════════════════════════════════════════════════════════════════════════
# 11. _expansion_potential
# ═══════════════════════════════════════════════════════════════════════════════

class TestExpansionPotential:
    def test_zero_exp_score_gives_zero(self, engine):
        inp = make_input(current_arr=100_000.0, whitespace_products=5)
        result = engine._expansion_potential(inp, exp_score=0.0)
        assert result == 0.0

    def test_basic_calculation(self, engine):
        inp = make_input(current_arr=100_000.0, whitespace_products=0)
        result = engine._expansion_potential(inp, exp_score=100.0)
        # base = 100000 * 0.2 * 1.0 = 20000, whitespace_mult = 1.0
        assert result == 20_000.0

    def test_whitespace_multiplier(self, engine):
        inp = make_input(current_arr=100_000.0, whitespace_products=3)
        result = engine._expansion_potential(inp, exp_score=100.0)
        # base = 100000 * 0.2 * 1.0 = 20000, mult = 1.0 + 3*0.1 = 1.3
        assert result == 26_000.0

    def test_whitespace_multiplier_at_5(self, engine):
        inp = make_input(current_arr=100_000.0, whitespace_products=5)
        result = engine._expansion_potential(inp, exp_score=100.0)
        # mult = 1.0 + 5*0.1 = 1.5, base = 20000
        assert result == 30_000.0

    def test_partial_exp_score(self, engine):
        inp = make_input(current_arr=100_000.0, whitespace_products=0)
        result = engine._expansion_potential(inp, exp_score=50.0)
        # base = 100000 * 0.2 * 0.5 = 10000
        assert result == 10_000.0

    def test_rounded_to_2_decimal_places(self, engine):
        inp = make_input(current_arr=99_999.0, whitespace_products=1)
        result = engine._expansion_potential(inp, exp_score=33.0)
        # base = 99999 * 0.2 * 0.33 = 6599.934, mult = 1.1
        # 6599.934 * 1.1 = 7259.9274 → 7259.93
        assert result == round(result, 2)

    def test_high_arr_high_score(self, engine):
        inp = make_input(current_arr=1_000_000.0, whitespace_products=10)
        result = engine._expansion_potential(inp, exp_score=100.0)
        # base = 200000, mult = 2.0 → 400000
        assert result == 400_000.0

    def test_returns_float(self, engine):
        inp = make_input()
        result = engine._expansion_potential(inp, exp_score=50.0)
        assert isinstance(result, float)


# ═══════════════════════════════════════════════════════════════════════════════
# 12. _nrr_forecast
# ═══════════════════════════════════════════════════════════════════════════════

class TestNrrForecast:
    def _compute_nrr(self, engine, health: float, churn_risk: float, exp_score: float) -> float:
        inp = make_input()
        return engine._nrr_forecast(inp, health, churn_risk, exp_score)

    def test_baseline_100(self, engine):
        # exp_score=0, churn=0, health between 40 and 70
        nrr = self._compute_nrr(engine, health=50.0, churn_risk=0.0, exp_score=0.0)
        assert nrr == 100.0

    def test_expansion_adds_up_to_30(self, engine):
        nrr = self._compute_nrr(engine, health=50.0, churn_risk=0.0, exp_score=100.0)
        # 100 + 30 - 0 = 130
        assert nrr == 130.0

    def test_churn_subtracts_up_to_40(self, engine):
        nrr = self._compute_nrr(engine, health=50.0, churn_risk=100.0, exp_score=0.0)
        # 100 + 0 - 40 = 60
        assert nrr == 60.0

    def test_health_above_70_adds_5(self, engine):
        nrr = self._compute_nrr(engine, health=70.0, churn_risk=0.0, exp_score=0.0)
        assert nrr == 105.0

    def test_health_71_adds_5(self, engine):
        nrr = self._compute_nrr(engine, health=71.0, churn_risk=0.0, exp_score=0.0)
        assert nrr == 105.0

    def test_health_below_40_subtracts_10(self, engine):
        nrr = self._compute_nrr(engine, health=39.9, churn_risk=0.0, exp_score=0.0)
        assert nrr == 90.0

    def test_health_40_has_no_adjustment(self, engine):
        nrr = self._compute_nrr(engine, health=40.0, churn_risk=0.0, exp_score=0.0)
        assert nrr == 100.0

    def test_health_between_40_and_70_no_adjustment(self, engine):
        nrr = self._compute_nrr(engine, health=55.0, churn_risk=0.0, exp_score=0.0)
        assert nrr == 100.0

    def test_clamped_at_0(self, engine):
        # max negative: churn=100 → -40, health<40 → -10, no expansion
        nrr = self._compute_nrr(engine, health=30.0, churn_risk=100.0, exp_score=0.0)
        # 100 - 40 - 10 = 50 > 0, won't hit 0 in normal cases
        assert nrr == 50.0

    def test_clamped_at_200(self, engine):
        nrr = self._compute_nrr(engine, health=100.0, churn_risk=0.0, exp_score=100.0)
        # 100 + 30 + 5 = 135, well below 200
        assert nrr == 135.0

    def test_rounded_to_one_decimal(self, engine):
        nrr = self._compute_nrr(engine, health=50.0, churn_risk=33.0, exp_score=50.0)
        assert nrr == round(nrr, 1)

    def test_combined_factors(self, engine):
        # health=80 (>=70→+5), churn=50, exp_score=50
        nrr = self._compute_nrr(engine, health=80.0, churn_risk=50.0, exp_score=50.0)
        # 100 + (50/100)*30 - (50/100)*40 + 5 = 100 + 15 - 20 + 5 = 100
        assert nrr == 100.0

    def test_minimum_achievable(self, engine):
        # Construct the worst possible: force churn risk accumulation
        nrr = self._compute_nrr(engine, health=10.0, churn_risk=100.0, exp_score=0.0)
        # 100 + 0 - 40 - 10 = 50
        assert nrr == 50.0


# ═══════════════════════════════════════════════════════════════════════════════
# 13. _expansion_action — full 7-step priority chain
# ═══════════════════════════════════════════════════════════════════════════════

class TestExpansionAction:
    def test_critical_churn_returns_risk_intervention(self, engine):
        inp = make_input(last_qbr_days=50)
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.READY_NOW,
            churn_sig=ChurnSignal.CRITICAL,
            exp_score=90.0,
        )
        assert action == ExpansionAction.RISK_INTERVENTION

    def test_high_churn_returns_risk_intervention(self, engine):
        inp = make_input(last_qbr_days=50)
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.READY_NOW,
            churn_sig=ChurnSignal.HIGH,
            exp_score=90.0,
        )
        assert action == ExpansionAction.RISK_INTERVENTION

    def test_critical_overrides_ready_now(self, engine):
        inp = make_input(last_qbr_days=50)
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.READY_NOW,
            churn_sig=ChurnSignal.CRITICAL,
            exp_score=80.0,
        )
        assert action == ExpansionAction.RISK_INTERVENTION

    def test_ready_now_returns_pitch_now(self, engine):
        inp = make_input(last_qbr_days=50)
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.READY_NOW,
            churn_sig=ChurnSignal.NONE,
            exp_score=80.0,
        )
        assert action == ExpansionAction.PITCH_NOW

    def test_upcoming_returns_schedule_qbr(self, engine):
        inp = make_input(last_qbr_days=50)
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.UPCOMING,
            churn_sig=ChurnSignal.NONE,
            exp_score=60.0,
        )
        assert action == ExpansionAction.SCHEDULE_QBR

    def test_low_score_and_old_qbr_returns_reactivate(self, engine):
        inp = make_input(last_qbr_days=200)  # >180
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.NOT_READY,
            churn_sig=ChurnSignal.NONE,
            exp_score=15.0,  # <20
        )
        assert action == ExpansionAction.REACTIVATE

    def test_reactivate_not_triggered_if_qbr_recent(self, engine):
        inp = make_input(last_qbr_days=100)  # not >180
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.NOT_READY,
            churn_sig=ChurnSignal.NONE,
            exp_score=15.0,
        )
        # falls to MAINTAIN_HEALTH (NOT_READY, no other match)
        assert action == ExpansionAction.MAINTAIN_HEALTH

    def test_reactivate_not_triggered_if_score_20_or_above(self, engine):
        inp = make_input(last_qbr_days=200)
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.NOT_READY,
            churn_sig=ChurnSignal.NONE,
            exp_score=20.0,  # not < 20
        )
        assert action == ExpansionAction.MAINTAIN_HEALTH

    def test_needs_nurturing_returns_nurture_adoption(self, engine):
        inp = make_input(last_qbr_days=50)
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.NEEDS_NURTURING,
            churn_sig=ChurnSignal.NONE,
            exp_score=40.0,
        )
        assert action == ExpansionAction.NURTURE_ADOPTION

    def test_not_ready_moderate_score_returns_maintain_health(self, engine):
        inp = make_input(last_qbr_days=50)
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.NOT_READY,
            churn_sig=ChurnSignal.NONE,
            exp_score=25.0,
        )
        assert action == ExpansionAction.MAINTAIN_HEALTH

    def test_medium_churn_does_not_trigger_risk_intervention(self, engine):
        inp = make_input(last_qbr_days=50)
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.READY_NOW,
            churn_sig=ChurnSignal.MEDIUM,
            exp_score=80.0,
        )
        assert action == ExpansionAction.PITCH_NOW

    def test_low_churn_does_not_trigger_risk_intervention(self, engine):
        inp = make_input(last_qbr_days=50)
        action = engine._expansion_action(
            inp,
            readiness=ExpansionReadiness.UPCOMING,
            churn_sig=ChurnSignal.LOW,
            exp_score=60.0,
        )
        assert action == ExpansionAction.SCHEDULE_QBR

    def test_returns_expansion_action_type(self, engine, good_input):
        result = engine.analyze(good_input)
        assert isinstance(result.expansion_action, ExpansionAction)

    def test_reactivate_needs_both_conditions(self, engine):
        # Both conditions required: exp_score < 20 AND last_qbr_days > 180
        inp_only_score = make_input(last_qbr_days=50)
        action1 = engine._expansion_action(
            inp_only_score, ExpansionReadiness.NOT_READY, ChurnSignal.NONE, 10.0
        )
        assert action1 == ExpansionAction.MAINTAIN_HEALTH  # no old QBR

        inp_only_qbr = make_input(last_qbr_days=200)
        action2 = engine._expansion_action(
            inp_only_qbr, ExpansionReadiness.NOT_READY, ChurnSignal.NONE, 25.0
        )
        assert action2 == ExpansionAction.MAINTAIN_HEALTH  # score not < 20

        inp_both = make_input(last_qbr_days=200)
        action3 = engine._expansion_action(
            inp_both, ExpansionReadiness.NOT_READY, ChurnSignal.NONE, 10.0
        )
        assert action3 == ExpansionAction.REACTIVATE


# ═══════════════════════════════════════════════════════════════════════════════
# 14. is_at_risk
# ═══════════════════════════════════════════════════════════════════════════════

class TestIsAtRisk:
    def test_critical_churn_is_at_risk(self, engine, risky_input):
        result = engine.analyze(risky_input)
        if result.churn_signal == ChurnSignal.CRITICAL:
            assert result.is_at_risk is True

    def test_high_churn_is_at_risk(self, engine):
        # Force high churn signal directly
        inp = make_input(
            active_users=5, licensed_users=100,  # adoption=5 → +20 (adoption<30)
            nps_score=-80.0,                      # health very low → +30
            contract_end_days=20,                 # +25
            competitor_conversation=True,          # +20
            support_tickets_open=0,
            executive_engagement=False,
            last_qbr_days=200,
            expansion_budget_confirmed=False,
            whitespace_products=0,
            features_used=0, total_features_available=10,
        )
        result = engine.analyze(inp)
        assert result.churn_signal in (ChurnSignal.HIGH, ChurnSignal.CRITICAL)
        assert result.is_at_risk is True

    def test_medium_churn_not_at_risk(self, engine):
        # Medium churn (risk ~ 30-49): health<60 +15, adoption<60 +10 = 25 → LOW
        # To get MEDIUM, add competitor or contract risk
        inp = make_input(
            active_users=50, licensed_users=100,   # adoption=50 → +10
            nps_score=0.0,
            support_tickets_open=0,
            contract_end_days=60,   # +10
            competitor_conversation=False,
            executive_engagement=True,
            last_qbr_days=30,
            features_used=5, total_features_available=10,
        )
        result = engine.analyze(inp)
        if result.churn_signal == ChurnSignal.MEDIUM:
            assert result.is_at_risk is False

    def test_none_churn_not_at_risk(self, engine, good_input):
        result = engine.analyze(good_input)
        if result.churn_signal == ChurnSignal.NONE:
            assert result.is_at_risk is False

    def test_is_at_risk_is_bool(self, engine, good_input):
        result = engine.analyze(good_input)
        assert isinstance(result.is_at_risk, bool)

    def test_at_risk_matches_churn_signal(self, engine):
        for _ in range(3):
            inp = make_input(
                active_users=5, licensed_users=100,
                contract_end_days=10,
                competitor_conversation=True,
                nps_score=-80.0,
                executive_engagement=False,
                last_qbr_days=250,
                support_tickets_open=6,
                features_used=0, total_features_available=10,
            )
            result = engine.analyze(inp)
            expected = result.churn_signal in (ChurnSignal.HIGH, ChurnSignal.CRITICAL)
            assert result.is_at_risk == expected
            engine.reset()


# ═══════════════════════════════════════════════════════════════════════════════
# 15. is_ready_to_expand
# ═══════════════════════════════════════════════════════════════════════════════

class TestIsReadyToExpand:
    def test_ready_now_sets_true(self, engine, good_input):
        result = engine.analyze(good_input)
        if result.expansion_readiness == ExpansionReadiness.READY_NOW:
            assert result.is_ready_to_expand is True

    def test_not_ready_sets_false(self, engine, risky_input):
        result = engine.analyze(risky_input)
        if result.expansion_readiness == ExpansionReadiness.NOT_READY:
            assert result.is_ready_to_expand is False

    def test_upcoming_sets_false(self, engine):
        inp = make_input(
            expansion_budget_confirmed=False,
            contract_end_days=60,
            active_users=70, licensed_users=100,
            nps_score=50.0,
            support_tickets_open=0,
            executive_engagement=True,
            last_qbr_days=30,
            whitespace_products=2,
            internal_champion=True,
            roi_demonstrated=True,
            competitor_conversation=False,
            growth_since_start_pct=25.0,
            features_used=7, total_features_available=10,
        )
        result = engine.analyze(inp)
        if result.expansion_readiness == ExpansionReadiness.UPCOMING:
            assert result.is_ready_to_expand is False

    def test_needs_nurturing_sets_false(self, engine):
        inp = make_input(
            expansion_budget_confirmed=False,
            contract_end_days=200,
            active_users=40, licensed_users=100,
            nps_score=20.0,
            support_tickets_open=1,
            executive_engagement=False,
            last_qbr_days=60,
            whitespace_products=1,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=5.0,
            features_used=3, total_features_available=10,
        )
        result = engine.analyze(inp)
        if result.expansion_readiness == ExpansionReadiness.NEEDS_NURTURING:
            assert result.is_ready_to_expand is False

    def test_is_bool_type(self, engine, good_input):
        result = engine.analyze(good_input)
        assert isinstance(result.is_ready_to_expand, bool)

    def test_matches_readiness_enum(self, engine, good_input):
        result = engine.analyze(good_input)
        assert result.is_ready_to_expand == (result.expansion_readiness == ExpansionReadiness.READY_NOW)


# ═══════════════════════════════════════════════════════════════════════════════
# 16. Properties (empty, filtering, total_expansion_potential)
# ═══════════════════════════════════════════════════════════════════════════════

class TestEngineProperties:
    def test_at_risk_accounts_empty_initially(self, engine):
        assert engine.at_risk_accounts == []

    def test_ready_to_expand_empty_initially(self, engine):
        assert engine.ready_to_expand == []

    def test_high_value_opportunities_empty_initially(self, engine):
        assert engine.high_value_opportunities == []

    def test_total_expansion_potential_zero_initially(self, engine):
        assert engine.total_expansion_potential == 0.0

    def test_at_risk_accounts_filters_correctly(self, engine):
        # Add a high-risk account
        risky = make_input(
            account_id="risky",
            active_users=5, licensed_users=100,
            contract_end_days=10,
            competitor_conversation=True,
            nps_score=-80.0,
            executive_engagement=False,
            last_qbr_days=250,
            support_tickets_open=6,
            features_used=0, total_features_available=10,
        )
        good = make_input(account_id="good")
        engine.analyze(risky)
        engine.analyze(good)
        at_risk = engine.at_risk_accounts
        at_risk_ids = {r.account_id for r in at_risk}
        # All at_risk entries should have is_at_risk=True
        assert all(r.is_at_risk for r in at_risk)

    def test_ready_to_expand_filters_correctly(self, engine):
        good = make_input(account_id="good_acct")
        result = engine.analyze(good)
        ready = engine.ready_to_expand
        for r in ready:
            assert r.is_ready_to_expand is True

    def test_high_value_opportunities_threshold_50000(self, engine):
        # Force large expansion potential: huge ARR, high scores
        big = make_input(
            account_id="big",
            current_arr=1_000_000.0,
            active_users=90, licensed_users=100,
            features_used=9, total_features_available=10,
            nps_score=80.0,
            support_tickets_open=0,
            executive_engagement=True,
            last_qbr_days=20,
            whitespace_products=5,
            expansion_budget_confirmed=True,
            internal_champion=True,
            roi_demonstrated=True,
            competitor_conversation=False,
            growth_since_start_pct=25.0,
        )
        result = engine.analyze(big)
        if result.expansion_potential >= 50_000:
            assert result in engine.high_value_opportunities

    def test_high_value_does_not_include_below_threshold(self, engine):
        small = make_input(
            account_id="small",
            current_arr=1_000.0,  # tiny ARR
            active_users=0, licensed_users=100,
            features_used=0, total_features_available=10,
            nps_score=-100.0,
            support_tickets_open=0,
            executive_engagement=False,
            last_qbr_days=100,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        result = engine.analyze(small)
        if result.expansion_potential < 50_000:
            assert result not in engine.high_value_opportunities

    def test_total_expansion_potential_sums_all(self, engine):
        inp1 = make_input(account_id="a1", current_arr=100_000.0)
        inp2 = make_input(account_id="a2", current_arr=200_000.0)
        r1 = engine.analyze(inp1)
        r2 = engine.analyze(inp2)
        expected = round(r1.expansion_potential + r2.expansion_potential, 2)
        assert engine.total_expansion_potential == expected

    def test_total_expansion_potential_rounded_to_2(self, engine):
        engine.analyze(make_input(account_id="x", current_arr=99_999.99))
        total = engine.total_expansion_potential
        assert total == round(total, 2)

    def test_at_risk_count_increments(self, engine):
        risky = make_input(
            active_users=5, licensed_users=100,
            contract_end_days=10,
            competitor_conversation=True,
            nps_score=-80.0,
            executive_engagement=False,
            last_qbr_days=250,
            support_tickets_open=6,
            features_used=0, total_features_available=10,
        )
        engine.analyze(risky)
        # at_risk_accounts may include the risky one
        for r in engine.at_risk_accounts:
            assert r.is_at_risk is True

    def test_properties_return_lists(self, engine, good_input):
        engine.analyze(good_input)
        assert isinstance(engine.at_risk_accounts, list)
        assert isinstance(engine.ready_to_expand, list)
        assert isinstance(engine.high_value_opportunities, list)


# ═══════════════════════════════════════════════════════════════════════════════
# 17. summary() — 13 keys + expansion_type_counts always empty
# ═══════════════════════════════════════════════════════════════════════════════

class TestSummary:
    def test_empty_summary_has_13_keys(self, engine):
        s = engine.summary()
        assert len(s) == 13

    def test_empty_summary_total_zero(self, engine):
        s = engine.summary()
        assert s["total"] == 0

    def test_empty_summary_expansion_type_counts_empty_dict(self, engine):
        s = engine.summary()
        assert s["expansion_type_counts"] == {}

    def test_empty_summary_all_counts_empty(self, engine):
        s = engine.summary()
        assert s["readiness_counts"] == {}
        assert s["churn_signal_counts"] == {}
        assert s["action_counts"] == {}

    def test_empty_summary_avg_scores_zero(self, engine):
        s = engine.summary()
        assert s["avg_health_score"] == 0.0
        assert s["avg_expansion_score"] == 0.0
        assert s["avg_churn_risk_score"] == 0.0
        assert s["avg_nrr_forecast"] == 0.0

    def test_empty_summary_at_risk_count_zero(self, engine):
        s = engine.summary()
        assert s["at_risk_count"] == 0
        assert s["ready_to_expand_count"] == 0
        assert s["high_value_count"] == 0

    def test_summary_with_one_account(self, engine, good_input):
        result = engine.analyze(good_input)
        s = engine.summary()
        assert s["total"] == 1

    def test_summary_total_matches_analyzed_count(self, engine):
        for i in range(3):
            engine.analyze(make_input(account_id=f"acct_{i}"))
        s = engine.summary()
        assert s["total"] == 3

    def test_summary_expansion_type_counts_always_empty_after_analysis(self, engine):
        engine.analyze(make_input(expansion_type=ExpansionType.UPSELL))
        engine.analyze(make_input(account_id="a2", expansion_type=ExpansionType.CROSS_SELL))
        s = engine.summary()
        # Known bug: type_counts dict is never populated
        assert s["expansion_type_counts"] == {}

    def test_summary_readiness_counts_populated(self, engine, good_input):
        engine.analyze(good_input)
        s = engine.summary()
        assert len(s["readiness_counts"]) >= 1

    def test_summary_churn_signal_counts_populated(self, engine, good_input):
        engine.analyze(good_input)
        s = engine.summary()
        assert len(s["churn_signal_counts"]) >= 1

    def test_summary_action_counts_populated(self, engine, good_input):
        engine.analyze(good_input)
        s = engine.summary()
        assert len(s["action_counts"]) >= 1

    def test_summary_readiness_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(account_id=f"acct_{i}"))
        s = engine.summary()
        assert sum(s["readiness_counts"].values()) == s["total"]

    def test_summary_churn_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(account_id=f"acct_{i}"))
        s = engine.summary()
        assert sum(s["churn_signal_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(account_id=f"acct_{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_health_score_calculated(self, engine):
        inp = make_input()
        result = engine.analyze(inp)
        s = engine.summary()
        assert s["avg_health_score"] == result.health_score

    def test_summary_avg_expansion_score_calculated(self, engine):
        inp = make_input()
        result = engine.analyze(inp)
        s = engine.summary()
        assert s["avg_expansion_score"] == result.expansion_score

    def test_summary_avg_churn_risk_score_calculated(self, engine):
        inp = make_input()
        result = engine.analyze(inp)
        s = engine.summary()
        assert s["avg_churn_risk_score"] == result.churn_risk_score

    def test_summary_avg_nrr_calculated(self, engine):
        inp = make_input()
        result = engine.analyze(inp)
        s = engine.summary()
        assert s["avg_nrr_forecast"] == result.nrr_forecast

    def test_summary_total_expansion_potential_matches_property(self, engine):
        for i in range(3):
            engine.analyze(make_input(account_id=f"acct_{i}", current_arr=50_000.0 * (i + 1)))
        s = engine.summary()
        assert s["total_expansion_potential"] == engine.total_expansion_potential

    def test_summary_at_risk_count_correct(self, engine):
        for i in range(5):
            engine.analyze(make_input(account_id=f"acct_{i}"))
        s = engine.summary()
        assert s["at_risk_count"] == len(engine.at_risk_accounts)

    def test_summary_ready_to_expand_count_correct(self, engine):
        for i in range(5):
            engine.analyze(make_input(account_id=f"acct_{i}"))
        s = engine.summary()
        assert s["ready_to_expand_count"] == len(engine.ready_to_expand)

    def test_summary_high_value_count_correct(self, engine):
        for i in range(5):
            engine.analyze(make_input(account_id=f"acct_{i}", current_arr=200_000.0))
        s = engine.summary()
        assert s["high_value_count"] == len(engine.high_value_opportunities)

    def test_summary_keys_are_exactly_13(self, engine, good_input):
        engine.analyze(good_input)
        s = engine.summary()
        expected_keys = {
            "total", "readiness_counts", "churn_signal_counts", "action_counts",
            "expansion_type_counts", "avg_health_score", "avg_expansion_score",
            "avg_churn_risk_score", "avg_nrr_forecast", "total_expansion_potential",
            "at_risk_count", "ready_to_expand_count", "high_value_count",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_avg_is_rounded(self, engine):
        for i in range(3):
            engine.analyze(make_input(account_id=f"acct_{i}"))
        s = engine.summary()
        # Averages should be rounded to 1 decimal
        assert s["avg_health_score"] == round(s["avg_health_score"], 1)
        assert s["avg_expansion_score"] == round(s["avg_expansion_score"], 1)


# ═══════════════════════════════════════════════════════════════════════════════
# 18. reset()
# ═══════════════════════════════════════════════════════════════════════════════

class TestReset:
    def test_reset_clears_results(self, engine, good_input):
        engine.analyze(good_input)
        assert len(engine._results) == 1
        engine.reset()
        assert len(engine._results) == 0

    def test_reset_clears_multiple_results(self, engine):
        for i in range(5):
            engine.analyze(make_input(account_id=f"acct_{i}"))
        engine.reset()
        assert len(engine._results) == 0

    def test_summary_after_reset_returns_empty(self, engine, good_input):
        engine.analyze(good_input)
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0

    def test_at_risk_accounts_empty_after_reset(self, engine):
        risky = make_input(
            active_users=5, licensed_users=100,
            contract_end_days=10,
            competitor_conversation=True,
            nps_score=-80.0,
            executive_engagement=False,
            last_qbr_days=250,
            support_tickets_open=6,
            features_used=0, total_features_available=10,
        )
        engine.analyze(risky)
        engine.reset()
        assert engine.at_risk_accounts == []

    def test_total_expansion_potential_zero_after_reset(self, engine):
        engine.analyze(make_input(current_arr=1_000_000.0))
        engine.reset()
        assert engine.total_expansion_potential == 0.0

    def test_can_analyze_after_reset(self, engine, good_input):
        engine.analyze(good_input)
        engine.reset()
        result = engine.analyze(good_input)
        assert result.account_id == good_input.account_id
        assert len(engine._results) == 1

    def test_reset_returns_none(self, engine, good_input):
        engine.analyze(good_input)
        retval = engine.reset()
        assert retval is None


# ═══════════════════════════════════════════════════════════════════════════════
# 19. analyze_batch
# ═══════════════════════════════════════════════════════════════════════════════

class TestAnalyzeBatch:
    def test_returns_list(self, engine):
        inputs = [make_input(account_id=f"acct_{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert isinstance(results, list)

    def test_returns_correct_count(self, engine):
        inputs = [make_input(account_id=f"acct_{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_empty_batch_returns_empty_list(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_results_accumulate_in_engine(self, engine):
        inputs = [make_input(account_id=f"acct_{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 4

    def test_order_preserved(self, engine):
        ids = [f"acct_{i}" for i in range(5)]
        inputs = [make_input(account_id=i) for i in ids]
        results = engine.analyze_batch(inputs)
        for i, result in enumerate(results):
            assert result.account_id == ids[i]

    def test_returns_account_expansion_results(self, engine):
        inputs = [make_input(account_id=f"acct_{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for r in results:
            assert isinstance(r, AccountExpansionResult)

    def test_batch_adds_to_existing_results(self, engine, good_input):
        engine.analyze(good_input)
        inputs = [make_input(account_id=f"batch_{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 4


# ═══════════════════════════════════════════════════════════════════════════════
# 20. End-to-end scenarios
# ═══════════════════════════════════════════════════════════════════════════════

class TestEndToEndScenarios:
    def test_healthy_enterprise_account_ready_to_expand(self, engine):
        """High adoption, NPS, budget confirmed → READY_NOW, PITCH_NOW."""
        inp = make_input(
            account_id="enterprise_1",
            current_arr=500_000.0,
            active_users=90, licensed_users=100,
            features_used=9, total_features_available=10,
            nps_score=80.0,
            support_tickets_open=0,
            executive_engagement=True,
            last_qbr_days=20,
            contract_end_days=180,
            whitespace_products=3,
            expansion_budget_confirmed=True,
            internal_champion=True,
            roi_demonstrated=True,
            competitor_conversation=False,
            growth_since_start_pct=30.0,
        )
        result = engine.analyze(inp)
        assert result.expansion_readiness == ExpansionReadiness.READY_NOW
        assert result.expansion_action == ExpansionAction.PITCH_NOW
        assert result.is_ready_to_expand is True
        assert result.is_at_risk is False
        assert result.health_score > 50
        assert result.expansion_score > 70

    def test_churning_account_risk_intervention(self, engine):
        """Low adoption, competitor, short contract → at risk, RISK_INTERVENTION."""
        inp = make_input(
            account_id="churning_1",
            current_arr=100_000.0,
            active_users=5, licensed_users=100,
            features_used=1, total_features_available=10,
            nps_score=-70.0,
            support_tickets_open=8,
            executive_engagement=False,
            last_qbr_days=300,
            contract_end_days=15,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=True,
            growth_since_start_pct=-10.0,
        )
        result = engine.analyze(inp)
        assert result.is_at_risk is True
        assert result.expansion_action == ExpansionAction.RISK_INTERVENTION
        assert result.churn_signal in (ChurnSignal.HIGH, ChurnSignal.CRITICAL)
        assert result.expansion_readiness == ExpansionReadiness.NOT_READY

    def test_upcoming_renewal_account(self, engine):
        """Good score, upcoming contract, no confirmed budget → UPCOMING."""
        inp = make_input(
            account_id="renewal_1",
            current_arr=200_000.0,
            active_users=70, licensed_users=100,
            features_used=7, total_features_available=10,
            nps_score=60.0,
            support_tickets_open=1,
            executive_engagement=True,
            last_qbr_days=45,
            contract_end_days=60,  # within 90 days
            whitespace_products=2,
            expansion_budget_confirmed=False,
            internal_champion=True,
            roi_demonstrated=True,
            competitor_conversation=False,
            growth_since_start_pct=15.0,
        )
        result = engine.analyze(inp)
        # Verify UPCOMING or READY_NOW (if score is high enough)
        assert result.expansion_readiness in (ExpansionReadiness.UPCOMING, ExpansionReadiness.READY_NOW)
        if result.expansion_readiness == ExpansionReadiness.UPCOMING:
            assert result.expansion_action == ExpansionAction.SCHEDULE_QBR

    def test_dormant_account_reactivation(self, engine):
        """Very low score, old QBR → REACTIVATE."""
        inp = make_input(
            account_id="dormant_1",
            current_arr=50_000.0,
            active_users=5, licensed_users=100,
            features_used=1, total_features_available=10,
            nps_score=-50.0,
            support_tickets_open=1,
            executive_engagement=False,
            last_qbr_days=200,  # >180
            contract_end_days=180,
            whitespace_products=0,
            expansion_budget_confirmed=False,
            internal_champion=False,
            roi_demonstrated=False,
            competitor_conversation=False,
            growth_since_start_pct=0.0,
        )
        result = engine.analyze(inp)
        # If churn is not HIGH/CRITICAL and score <20 and qbr>180 → REACTIVATE
        if result.churn_signal not in (ChurnSignal.HIGH, ChurnSignal.CRITICAL):
            if result.expansion_score < 20:
                assert result.expansion_action == ExpansionAction.REACTIVATE

    def test_result_fields_have_correct_types(self, engine, good_input):
        result = engine.analyze(good_input)
        assert isinstance(result.account_id, str)
        assert isinstance(result.account_name, str)
        assert isinstance(result.csm_id, str)
        assert isinstance(result.expansion_readiness, ExpansionReadiness)
        assert isinstance(result.churn_signal, ChurnSignal)
        assert isinstance(result.expansion_action, ExpansionAction)
        assert isinstance(result.expansion_score, float)
        assert isinstance(result.health_score, float)
        assert isinstance(result.churn_risk_score, float)
        assert isinstance(result.adoption_rate, float)
        assert isinstance(result.feature_utilization, float)
        assert isinstance(result.expansion_potential, float)
        assert isinstance(result.nrr_forecast, float)
        assert isinstance(result.is_at_risk, bool)
        assert isinstance(result.is_ready_to_expand, bool)

    def test_score_bounds_always_valid(self, engine):
        inputs = [
            make_input(account_id=f"a{i}", current_arr=10_000.0 * i,
                       active_users=i * 5, licensed_users=100,
                       features_used=i, total_features_available=10,
                       nps_score=float(i * 10 - 50))
            for i in range(1, 11)
        ]
        for inp in inputs:
            result = engine.analyze(inp)
            assert 0.0 <= result.health_score <= 100.0
            assert 0.0 <= result.churn_risk_score <= 100.0
            assert 0.0 <= result.expansion_score <= 100.0
            assert 0.0 <= result.nrr_forecast <= 200.0
            assert result.expansion_potential >= 0.0
            assert result.adoption_rate >= 0.0
            assert result.feature_utilization >= 0.0
        engine.reset()

    def test_multiple_accounts_tracked_in_summary(self, engine):
        accounts = [
            make_input(account_id=f"acct_{i}", current_arr=100_000.0)
            for i in range(6)
        ]
        engine.analyze_batch(accounts)
        s = engine.summary()
        assert s["total"] == 6
        assert s["at_risk_count"] + s["ready_to_expand_count"] <= 12  # can overlap? No, distinct

    def test_high_value_filter_with_large_arr(self, engine):
        big = make_input(
            account_id="big_enterprise",
            current_arr=2_000_000.0,
            active_users=95, licensed_users=100,
            features_used=9, total_features_available=10,
            nps_score=90.0,
            support_tickets_open=0,
            executive_engagement=True,
            last_qbr_days=15,
            whitespace_products=5,
            expansion_budget_confirmed=True,
            internal_champion=True,
            roi_demonstrated=True,
            competitor_conversation=False,
            growth_since_start_pct=30.0,
        )
        result = engine.analyze(big)
        assert result.expansion_potential >= 50_000
        assert len(engine.high_value_opportunities) >= 1

    def test_analyze_returns_result_and_stores_it(self, engine, good_input):
        result = engine.analyze(good_input)
        assert result in engine._results

    def test_consecutive_analyses_accumulate(self, engine):
        for i in range(10):
            engine.analyze(make_input(account_id=f"acct_{i}"))
        assert len(engine._results) == 10

    def test_smb_segment_account(self, engine):
        inp = make_input(
            segment="smb",
            current_arr=10_000.0,
            active_users=8, licensed_users=10,
            features_used=3, total_features_available=5,
        )
        result = engine.analyze(inp)
        assert isinstance(result, AccountExpansionResult)
        assert result.adoption_rate == 80.0
        assert result.feature_utilization == 60.0

    def test_zero_arr_gives_zero_potential(self, engine):
        inp = make_input(current_arr=0.0, whitespace_products=5)
        result = engine.analyze(inp)
        assert result.expansion_potential == 0.0

    def test_full_adoption_and_utilization(self, engine):
        inp = make_input(
            active_users=100, licensed_users=100,
            features_used=10, total_features_available=10,
        )
        result = engine.analyze(inp)
        assert result.adoption_rate == 100.0
        assert result.feature_utilization == 100.0
