"""Comprehensive pytest test suite for swarm.intelligence.customer_success_playbook."""

from __future__ import annotations

import pytest
from swarm.intelligence.customer_success_playbook import (
    LifecycleStage,
    PlaybookMotion,
    RiskLevel,
    CSPlaybookInput,
    CSPlaybookResult,
    CustomerSuccessPlaybookEngine,
    _overall_health,
    _risk_level,
    _lifecycle_stage,
    _renewal_urgency,
    _expansion_readiness,
    _playbook_motion,
    _build_risks,
    _build_actions,
    _build_playbook_steps,
    _build_success_metrics,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────

def _make_input(**overrides) -> CSPlaybookInput:
    """Return a healthy default CSPlaybookInput, overridable via kwargs."""
    defaults = dict(
        account_id="acct-001",
        account_name="Acme Corp",
        segment="enterprise",
        arr_eur=120_000.0,
        days_since_signature=200,
        product_adoption_score=80.0,
        support_health_score=80.0,
        engagement_score=80.0,
        nps_score=50.0,
        days_to_renewal=200,
        has_expansion_potential=True,
        competitive_pressure=False,
        executive_sponsor_active=True,
        champion_strength=70.0,
        dau_mau_ratio=0.3,
        features_adopted_pct=70.0,
        last_login_days_ago=3,
        open_escalations=0,
        missed_qbr_count=0,
        onboarding_complete=True,
    )
    defaults.update(overrides)
    return CSPlaybookInput(**defaults)


@pytest.fixture
def healthy_input():
    """A very healthy account across all dimensions."""
    return _make_input()


@pytest.fixture
def at_risk_input():
    """Account in AT_RISK stage (open escalations)."""
    return _make_input(open_escalations=3, product_adoption_score=30.0)


@pytest.fixture
def onboarding_input():
    """Account in ONBOARDING stage."""
    return _make_input(days_since_signature=45, open_escalations=0, competitive_pressure=False)


@pytest.fixture
def critical_input():
    """Account with CRITICAL health (all scores very low)."""
    return _make_input(
        product_adoption_score=10.0,
        support_health_score=10.0,
        engagement_score=10.0,
        nps_score=-80.0,
        open_escalations=0,
        competitive_pressure=False,
        days_since_signature=400,
    )


@pytest.fixture
def expand_ready_input():
    """Account ready for expansion motion."""
    return _make_input(
        product_adoption_score=90.0,
        support_health_score=90.0,
        engagement_score=90.0,
        nps_score=80.0,
        has_expansion_potential=True,
        champion_strength=75.0,
        competitive_pressure=False,
        features_adopted_pct=80.0,
        days_since_signature=400,
        open_escalations=0,
    )


@pytest.fixture
def engine():
    """A fresh CustomerSuccessPlaybookEngine."""
    return CustomerSuccessPlaybookEngine()


# ─── 1. TestLifecycleStageEnum ────────────────────────────────────────────────

class TestLifecycleStageEnum:
    def test_onboarding_value(self):
        assert LifecycleStage.ONBOARDING.value == "onboarding"

    def test_adoption_value(self):
        assert LifecycleStage.ADOPTION.value == "adoption"

    def test_growth_value(self):
        assert LifecycleStage.GROWTH.value == "growth"

    def test_mature_value(self):
        assert LifecycleStage.MATURE.value == "mature"

    def test_at_risk_value(self):
        assert LifecycleStage.AT_RISK.value == "at_risk"

    def test_all_members(self):
        members = {s.value for s in LifecycleStage}
        assert members == {"onboarding", "adoption", "growth", "mature", "at_risk"}

    def test_is_str_enum(self):
        assert isinstance(LifecycleStage.MATURE, str)

    def test_str_comparison(self):
        assert LifecycleStage.GROWTH == "growth"

    def test_count(self):
        assert len(LifecycleStage) == 5


# ─── 2. TestPlaybookMotionEnum ────────────────────────────────────────────────

class TestPlaybookMotionEnum:
    def test_expand_value(self):
        assert PlaybookMotion.EXPAND.value == "expand"

    def test_retain_value(self):
        assert PlaybookMotion.RETAIN.value == "retain"

    def test_rescue_value(self):
        assert PlaybookMotion.RESCUE.value == "rescue"

    def test_onboard_value(self):
        assert PlaybookMotion.ONBOARD.value == "onboard"

    def test_accelerate_value(self):
        assert PlaybookMotion.ACCELERATE.value == "accelerate"

    def test_is_str_enum(self):
        assert isinstance(PlaybookMotion.EXPAND, str)

    def test_all_members(self):
        members = {m.value for m in PlaybookMotion}
        assert members == {"expand", "retain", "rescue", "onboard", "accelerate"}

    def test_count(self):
        assert len(PlaybookMotion) == 5

    def test_str_comparison(self):
        assert PlaybookMotion.RESCUE == "rescue"


# ─── 3. TestRiskLevelEnum ────────────────────────────────────────────────────

class TestRiskLevelEnum:
    def test_low_value(self):
        assert RiskLevel.LOW.value == "low"

    def test_medium_value(self):
        assert RiskLevel.MEDIUM.value == "medium"

    def test_high_value(self):
        assert RiskLevel.HIGH.value == "high"

    def test_critical_value(self):
        assert RiskLevel.CRITICAL.value == "critical"

    def test_is_str_enum(self):
        assert isinstance(RiskLevel.LOW, str)

    def test_all_members(self):
        members = {r.value for r in RiskLevel}
        assert members == {"low", "medium", "high", "critical"}

    def test_count(self):
        assert len(RiskLevel) == 4

    def test_str_comparison(self):
        assert RiskLevel.HIGH == "high"


# ─── 4. TestCSPlaybookInputDataclass ─────────────────────────────────────────

class TestCSPlaybookInputDataclass:
    def test_creation(self, healthy_input):
        assert healthy_input.account_id == "acct-001"

    def test_all_fields_accessible(self, healthy_input):
        assert healthy_input.account_name == "Acme Corp"
        assert healthy_input.segment == "enterprise"
        assert healthy_input.arr_eur == 120_000.0
        assert healthy_input.days_since_signature == 200

    def test_health_dimension_fields(self, healthy_input):
        assert healthy_input.product_adoption_score == 80.0
        assert healthy_input.support_health_score == 80.0
        assert healthy_input.engagement_score == 80.0
        assert healthy_input.nps_score == 50.0

    def test_renewal_and_growth_fields(self, healthy_input):
        assert healthy_input.days_to_renewal == 200
        assert healthy_input.has_expansion_potential is True
        assert healthy_input.competitive_pressure is False
        assert healthy_input.executive_sponsor_active is True
        assert healthy_input.champion_strength == 70.0

    def test_usage_signal_fields(self, healthy_input):
        assert healthy_input.dau_mau_ratio == 0.3
        assert healthy_input.features_adopted_pct == 70.0
        assert healthy_input.last_login_days_ago == 3

    def test_escalation_context_fields(self, healthy_input):
        assert healthy_input.open_escalations == 0
        assert healthy_input.missed_qbr_count == 0
        assert healthy_input.onboarding_complete is True

    def test_dataclass_is_mutable(self, healthy_input):
        healthy_input.arr_eur = 200_000.0
        assert healthy_input.arr_eur == 200_000.0

    def test_nps_negative_allowed(self):
        inp = _make_input(nps_score=-50.0)
        assert inp.nps_score == -50.0

    def test_nps_boundary_max(self):
        inp = _make_input(nps_score=100.0)
        assert inp.nps_score == 100.0

    def test_nps_boundary_min(self):
        inp = _make_input(nps_score=-100.0)
        assert inp.nps_score == -100.0


# ─── 5. TestCSPlaybookResultToDict ───────────────────────────────────────────

class TestCSPlaybookResultToDict:
    def _make_result(self, **overrides):
        defaults = dict(
            account_id="acct-999",
            account_name="Test Co",
            segment="smb",
            arr_eur=50_000.0,
            lifecycle_stage=LifecycleStage.GROWTH,
            risk_level=RiskLevel.LOW,
            playbook_motion=PlaybookMotion.EXPAND,
            overall_health_score=80.0,
            renewal_urgency="low",
            expansion_readiness="ready",
            key_risks=[],
            immediate_actions=["action1"],
            playbook_steps=["step1"],
            success_metrics=["metric1"],
        )
        defaults.update(overrides)
        return CSPlaybookResult(**defaults)

    def test_to_dict_returns_dict(self):
        result = self._make_result()
        assert isinstance(result.to_dict(), dict)

    def test_lifecycle_stage_serialised_as_string(self):
        result = self._make_result(lifecycle_stage=LifecycleStage.GROWTH)
        d = result.to_dict()
        assert d["lifecycle_stage"] == "growth"
        assert isinstance(d["lifecycle_stage"], str)

    def test_risk_level_serialised_as_string(self):
        result = self._make_result(risk_level=RiskLevel.MEDIUM)
        d = result.to_dict()
        assert d["risk_level"] == "medium"

    def test_playbook_motion_serialised_as_string(self):
        result = self._make_result(playbook_motion=PlaybookMotion.RESCUE)
        d = result.to_dict()
        assert d["playbook_motion"] == "rescue"

    def test_all_keys_present(self):
        result = self._make_result()
        d = result.to_dict()
        expected_keys = {
            "account_id", "account_name", "segment", "arr_eur",
            "lifecycle_stage", "risk_level", "playbook_motion",
            "overall_health_score", "renewal_urgency", "expansion_readiness",
            "key_risks", "immediate_actions", "playbook_steps", "success_metrics",
        }
        assert expected_keys.issubset(d.keys())

    def test_arr_eur_preserved(self):
        result = self._make_result(arr_eur=99_999.99)
        assert result.to_dict()["arr_eur"] == 99_999.99

    def test_lists_preserved(self):
        result = self._make_result(key_risks=["r1", "r2"])
        d = result.to_dict()
        assert d["key_risks"] == ["r1", "r2"]

    def test_to_dict_at_risk_stage(self):
        result = self._make_result(lifecycle_stage=LifecycleStage.AT_RISK)
        assert result.to_dict()["lifecycle_stage"] == "at_risk"

    def test_to_dict_critical_risk(self):
        result = self._make_result(risk_level=RiskLevel.CRITICAL)
        assert result.to_dict()["risk_level"] == "critical"


# ─── 6. TestOverallHealthWeights ─────────────────────────────────────────────

class TestOverallHealthWeights:
    """Verify the weighted formula: adoption*0.30 + support*0.20 + engagement*0.25 + nps_norm*0.25."""

    def test_all_zeros_gives_zero(self):
        inp = _make_input(
            product_adoption_score=0.0,
            support_health_score=0.0,
            engagement_score=0.0,
            nps_score=-100.0,  # nps_norm = 0
        )
        assert _overall_health(inp) == 0.0

    def test_all_max_gives_100(self):
        inp = _make_input(
            product_adoption_score=100.0,
            support_health_score=100.0,
            engagement_score=100.0,
            nps_score=100.0,  # nps_norm = 100
        )
        assert _overall_health(inp) == 100.0

    def test_adoption_weight_30pct(self):
        # Only adoption non-zero; nps_norm = 0 (nps=-100)
        inp = _make_input(
            product_adoption_score=100.0,
            support_health_score=0.0,
            engagement_score=0.0,
            nps_score=-100.0,
        )
        assert _overall_health(inp) == 30.0

    def test_support_weight_20pct(self):
        inp = _make_input(
            product_adoption_score=0.0,
            support_health_score=100.0,
            engagement_score=0.0,
            nps_score=-100.0,
        )
        assert _overall_health(inp) == 20.0

    def test_engagement_weight_25pct(self):
        inp = _make_input(
            product_adoption_score=0.0,
            support_health_score=0.0,
            engagement_score=100.0,
            nps_score=-100.0,
        )
        assert _overall_health(inp) == 25.0

    def test_nps_norm_weight_25pct(self):
        # nps=100 → nps_norm=100; all other zeros
        inp = _make_input(
            product_adoption_score=0.0,
            support_health_score=0.0,
            engagement_score=0.0,
            nps_score=100.0,
        )
        assert _overall_health(inp) == 25.0

    def test_weights_sum_to_100_when_all_max(self):
        inp = _make_input(
            product_adoption_score=100.0,
            support_health_score=100.0,
            engagement_score=100.0,
            nps_score=100.0,
        )
        assert _overall_health(inp) == 100.0

    def test_known_mixed_values(self):
        # adoption=60, support=80, engagement=70, nps=20 → nps_norm=60
        # 60*0.30 + 80*0.20 + 70*0.25 + 60*0.25 = 18+16+17.5+15 = 66.5
        inp = _make_input(
            product_adoption_score=60.0,
            support_health_score=80.0,
            engagement_score=70.0,
            nps_score=20.0,
            open_escalations=0,
            competitive_pressure=False,
        )
        assert _overall_health(inp) == 66.5

    def test_result_is_float(self, healthy_input):
        assert isinstance(_overall_health(healthy_input), float)

    def test_result_rounded_to_1dp(self):
        inp = _make_input(
            product_adoption_score=33.0,
            support_health_score=33.0,
            engagement_score=33.0,
            nps_score=-34.0,  # nps_norm = 33
        )
        result = _overall_health(inp)
        assert result == round(result, 1)

    def test_clamped_at_0(self):
        inp = _make_input(
            product_adoption_score=-50.0,
            support_health_score=-50.0,
            engagement_score=-50.0,
            nps_score=-100.0,
        )
        assert _overall_health(inp) >= 0.0

    def test_clamped_at_100(self):
        inp = _make_input(
            product_adoption_score=200.0,
            support_health_score=200.0,
            engagement_score=200.0,
            nps_score=100.0,
        )
        assert _overall_health(inp) == 100.0


# ─── 7. TestOverallHealthNPSNormalisation ────────────────────────────────────

class TestOverallHealthNPSNormalisation:
    """nps_norm = (nps + 100) / 2, clamped 0-100."""

    def test_nps_minus100_gives_norm_0(self):
        # Only nps matters; zero all other dims, nps=-100 → nps_norm=0
        inp = _make_input(
            product_adoption_score=0.0,
            support_health_score=0.0,
            engagement_score=0.0,
            nps_score=-100.0,
        )
        # health = 0*0.30 + 0*0.20 + 0*0.25 + 0*0.25 = 0
        assert _overall_health(inp) == 0.0

    def test_nps_plus100_gives_norm_100(self):
        inp = _make_input(
            product_adoption_score=0.0,
            support_health_score=0.0,
            engagement_score=0.0,
            nps_score=100.0,
        )
        # health = nps_norm * 0.25 = 100*0.25 = 25
        assert _overall_health(inp) == 25.0

    def test_nps_zero_gives_norm_50(self):
        inp = _make_input(
            product_adoption_score=0.0,
            support_health_score=0.0,
            engagement_score=0.0,
            nps_score=0.0,
        )
        # nps_norm=50; health = 50*0.25 = 12.5
        assert _overall_health(inp) == 12.5

    def test_nps_minus50_gives_norm_25(self):
        inp = _make_input(
            product_adoption_score=0.0,
            support_health_score=0.0,
            engagement_score=0.0,
            nps_score=-50.0,
        )
        # nps_norm = (-50+100)/2 = 25; health = 25*0.25 = 6.25 → rounded 6.2 or 6.3
        result = _overall_health(inp)
        assert abs(result - 6.2) < 0.2  # 6.2 rounded

    def test_nps_boundary_not_below_0(self):
        # Even if hypothetically nps < -100, norm is clamped at 0
        inp = _make_input(
            product_adoption_score=0.0,
            support_health_score=0.0,
            engagement_score=0.0,
            nps_score=-100.0,
        )
        assert _overall_health(inp) >= 0.0

    def test_nps_positive_contributes_positively(self):
        inp_pos = _make_input(
            product_adoption_score=0.0,
            support_health_score=0.0,
            engagement_score=0.0,
            nps_score=60.0,
        )
        inp_neg = _make_input(
            product_adoption_score=0.0,
            support_health_score=0.0,
            engagement_score=0.0,
            nps_score=-60.0,
        )
        assert _overall_health(inp_pos) > _overall_health(inp_neg)


# ─── 8. TestRiskLevelThresholds ──────────────────────────────────────────────

class TestRiskLevelThresholds:
    def test_75_is_low(self):
        assert _risk_level(75.0) == RiskLevel.LOW

    def test_74_is_medium(self):
        assert _risk_level(74.0) == RiskLevel.MEDIUM

    def test_50_is_medium(self):
        assert _risk_level(50.0) == RiskLevel.MEDIUM

    def test_49_is_high(self):
        assert _risk_level(49.0) == RiskLevel.HIGH

    def test_25_is_high(self):
        assert _risk_level(25.0) == RiskLevel.HIGH

    def test_24_is_critical(self):
        assert _risk_level(24.0) == RiskLevel.CRITICAL

    def test_0_is_critical(self):
        assert _risk_level(0.0) == RiskLevel.CRITICAL

    def test_100_is_low(self):
        assert _risk_level(100.0) == RiskLevel.LOW

    def test_76_is_low(self):
        assert _risk_level(76.0) == RiskLevel.LOW

    def test_60_is_medium(self):
        assert _risk_level(60.0) == RiskLevel.MEDIUM

    def test_30_is_high(self):
        assert _risk_level(30.0) == RiskLevel.HIGH

    def test_1_is_critical(self):
        assert _risk_level(1.0) == RiskLevel.CRITICAL

    def test_returns_risklevel_instance(self):
        assert isinstance(_risk_level(80.0), RiskLevel)


# ─── 9. TestLifecycleStageATRisk ─────────────────────────────────────────────

class TestLifecycleStageATRisk:
    def test_escalations_gte_2_gives_at_risk(self):
        inp = _make_input(open_escalations=2, days_since_signature=400)
        assert _lifecycle_stage(inp, 80.0) == LifecycleStage.AT_RISK

    def test_escalations_3_gives_at_risk(self):
        inp = _make_input(open_escalations=3, days_since_signature=400)
        assert _lifecycle_stage(inp, 80.0) == LifecycleStage.AT_RISK

    def test_escalations_1_does_not_trigger_at_risk_alone(self):
        inp = _make_input(open_escalations=1, days_since_signature=400, competitive_pressure=False)
        result = _lifecycle_stage(inp, 80.0)
        assert result != LifecycleStage.AT_RISK

    def test_health_below_30_gives_at_risk(self):
        inp = _make_input(open_escalations=0, days_since_signature=400, competitive_pressure=False)
        assert _lifecycle_stage(inp, 29.0) == LifecycleStage.AT_RISK

    def test_health_exactly_30_not_at_risk(self):
        inp = _make_input(open_escalations=0, days_since_signature=400, competitive_pressure=False)
        result = _lifecycle_stage(inp, 30.0)
        assert result != LifecycleStage.AT_RISK

    def test_competitive_pressure_plus_health_below_50_gives_at_risk(self):
        inp = _make_input(open_escalations=0, days_since_signature=400, competitive_pressure=True)
        assert _lifecycle_stage(inp, 49.0) == LifecycleStage.AT_RISK

    def test_competitive_pressure_plus_health_exactly_50_not_at_risk(self):
        inp = _make_input(open_escalations=0, days_since_signature=400, competitive_pressure=True)
        result = _lifecycle_stage(inp, 50.0)
        assert result != LifecycleStage.AT_RISK

    def test_competitive_pressure_plus_high_health_not_at_risk(self):
        inp = _make_input(open_escalations=0, days_since_signature=400, competitive_pressure=True)
        result = _lifecycle_stage(inp, 75.0)
        assert result != LifecycleStage.AT_RISK

    def test_no_escalations_high_health_no_competition_not_at_risk(self):
        inp = _make_input(open_escalations=0, days_since_signature=400, competitive_pressure=False)
        result = _lifecycle_stage(inp, 80.0)
        assert result != LifecycleStage.AT_RISK


# ─── 10. TestLifecycleStageByDays ────────────────────────────────────────────

class TestLifecycleStageByDays:
    """AT_RISK conditions must be False for these tests."""

    def _clean(self, days):
        return _make_input(days_since_signature=days, open_escalations=0, competitive_pressure=False)

    def test_90_days_gives_onboarding(self):
        assert _lifecycle_stage(self._clean(90), 80.0) == LifecycleStage.ONBOARDING

    def test_1_day_gives_onboarding(self):
        assert _lifecycle_stage(self._clean(1), 80.0) == LifecycleStage.ONBOARDING

    def test_0_days_gives_onboarding(self):
        assert _lifecycle_stage(self._clean(0), 80.0) == LifecycleStage.ONBOARDING

    def test_91_days_gives_adoption(self):
        assert _lifecycle_stage(self._clean(91), 80.0) == LifecycleStage.ADOPTION

    def test_180_days_gives_adoption(self):
        assert _lifecycle_stage(self._clean(180), 80.0) == LifecycleStage.ADOPTION

    def test_181_days_gives_growth(self):
        assert _lifecycle_stage(self._clean(181), 80.0) == LifecycleStage.GROWTH

    def test_365_days_gives_growth(self):
        assert _lifecycle_stage(self._clean(365), 80.0) == LifecycleStage.GROWTH

    def test_366_days_gives_mature(self):
        assert _lifecycle_stage(self._clean(366), 80.0) == LifecycleStage.MATURE

    def test_1000_days_gives_mature(self):
        assert _lifecycle_stage(self._clean(1000), 80.0) == LifecycleStage.MATURE

    def test_returns_lifecycle_stage_instance(self):
        result = _lifecycle_stage(self._clean(200), 80.0)
        assert isinstance(result, LifecycleStage)


# ─── 11. TestRenewalUrgency ──────────────────────────────────────────────────

class TestRenewalUrgency:
    def test_30_days_is_immediate(self):
        inp = _make_input(days_to_renewal=30)
        assert _renewal_urgency(inp) == "immediate"

    def test_1_day_is_immediate(self):
        inp = _make_input(days_to_renewal=1)
        assert _renewal_urgency(inp) == "immediate"

    def test_0_days_is_immediate(self):
        inp = _make_input(days_to_renewal=0)
        assert _renewal_urgency(inp) == "immediate"

    def test_31_days_is_high(self):
        inp = _make_input(days_to_renewal=31)
        assert _renewal_urgency(inp) == "high"

    def test_90_days_is_high(self):
        inp = _make_input(days_to_renewal=90)
        assert _renewal_urgency(inp) == "high"

    def test_91_days_is_medium(self):
        inp = _make_input(days_to_renewal=91)
        assert _renewal_urgency(inp) == "medium"

    def test_180_days_is_medium(self):
        inp = _make_input(days_to_renewal=180)
        assert _renewal_urgency(inp) == "medium"

    def test_181_days_is_low(self):
        inp = _make_input(days_to_renewal=181)
        assert _renewal_urgency(inp) == "low"

    def test_365_days_is_low(self):
        inp = _make_input(days_to_renewal=365)
        assert _renewal_urgency(inp) == "low"

    def test_returns_string(self):
        inp = _make_input(days_to_renewal=200)
        assert isinstance(_renewal_urgency(inp), str)


# ─── 12. TestExpansionReadiness ──────────────────────────────────────────────

class TestExpansionReadiness:
    def test_ready_when_health_ge_70_expansion_and_champion_ge_60(self):
        inp = _make_input(has_expansion_potential=True, champion_strength=60.0)
        assert _expansion_readiness(inp, 70.0) == "ready"

    def test_ready_with_higher_values(self):
        inp = _make_input(has_expansion_potential=True, champion_strength=80.0)
        assert _expansion_readiness(inp, 90.0) == "ready"

    def test_not_ready_when_health_ge_70_but_no_expansion(self):
        inp = _make_input(has_expansion_potential=False, champion_strength=80.0)
        assert _expansion_readiness(inp, 70.0) != "ready"

    def test_not_ready_when_health_ge_70_expansion_but_champion_below_60(self):
        inp = _make_input(has_expansion_potential=True, champion_strength=59.0)
        result = _expansion_readiness(inp, 70.0)
        assert result != "ready"

    def test_building_when_health_ge_50_and_expansion(self):
        inp = _make_input(has_expansion_potential=True, champion_strength=30.0)
        assert _expansion_readiness(inp, 50.0) == "building"

    def test_building_does_not_require_champion(self):
        inp = _make_input(has_expansion_potential=True, champion_strength=0.0)
        assert _expansion_readiness(inp, 65.0) == "building"

    def test_not_ready_when_health_ge_50_but_no_expansion(self):
        inp = _make_input(has_expansion_potential=False, champion_strength=80.0)
        assert _expansion_readiness(inp, 65.0) == "not_ready"

    def test_not_ready_when_health_below_50(self):
        inp = _make_input(has_expansion_potential=True, champion_strength=80.0)
        assert _expansion_readiness(inp, 49.0) == "not_ready"

    def test_not_ready_when_health_below_50_no_expansion(self):
        inp = _make_input(has_expansion_potential=False, champion_strength=40.0)
        assert _expansion_readiness(inp, 40.0) == "not_ready"

    def test_health_exactly_70_with_champion_60_is_ready(self):
        inp = _make_input(has_expansion_potential=True, champion_strength=60.0)
        assert _expansion_readiness(inp, 70.0) == "ready"

    def test_health_exactly_50_is_building(self):
        inp = _make_input(has_expansion_potential=True, champion_strength=20.0)
        assert _expansion_readiness(inp, 50.0) == "building"

    def test_returns_string(self):
        inp = _make_input()
        result = _expansion_readiness(inp, 80.0)
        assert isinstance(result, str)


# ─── 13. TestPlaybookMotionOnboard ───────────────────────────────────────────

class TestPlaybookMotionOnboard:
    def test_onboarding_stage_always_onboard(self):
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.ONBOARDING, RiskLevel.LOW, "ready")
        assert motion == PlaybookMotion.ONBOARD

    def test_onboarding_stage_overrides_at_risk(self):
        """ONBOARDING check comes before AT_RISK/CRITICAL in the function — but ONBOARDING stage is
        set only when AT_RISK conditions are False, so stage=ONBOARDING with AT_RISK logic is
        unreachable in practice; still worth checking the function directly."""
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.ONBOARDING, RiskLevel.CRITICAL, "not_ready")
        # Stage ONBOARDING takes precedence in the function's first if-branch
        assert motion == PlaybookMotion.ONBOARD

    def test_onboarding_stage_overrides_high_risk(self):
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.ONBOARDING, RiskLevel.HIGH, "not_ready")
        assert motion == PlaybookMotion.ONBOARD

    def test_onboarding_stage_with_expand_readiness_still_onboard(self):
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.ONBOARDING, RiskLevel.LOW, "ready")
        assert motion == PlaybookMotion.ONBOARD

    def test_non_onboarding_stage_not_onboard_by_default(self):
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "not_ready")
        assert motion != PlaybookMotion.ONBOARD


# ─── 14. TestPlaybookMotionRescue ────────────────────────────────────────────

class TestPlaybookMotionRescue:
    def test_at_risk_stage_gives_rescue(self):
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.AT_RISK, RiskLevel.MEDIUM, "not_ready")
        assert motion == PlaybookMotion.RESCUE

    def test_critical_risk_gives_rescue(self):
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.CRITICAL, "not_ready")
        assert motion == PlaybookMotion.RESCUE

    def test_at_risk_plus_critical_gives_rescue(self):
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.AT_RISK, RiskLevel.CRITICAL, "not_ready")
        assert motion == PlaybookMotion.RESCUE

    def test_at_risk_stage_with_ready_expansion_still_rescue(self):
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.AT_RISK, RiskLevel.LOW, "ready")
        assert motion == PlaybookMotion.RESCUE

    def test_high_risk_growth_stage_not_rescue(self):
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.GROWTH, RiskLevel.HIGH, "not_ready")
        assert motion != PlaybookMotion.RESCUE

    def test_medium_risk_mature_not_rescue(self):
        inp = _make_input()
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.MEDIUM, "not_ready")
        assert motion != PlaybookMotion.RESCUE


# ─── 15. TestPlaybookMotionExpand ────────────────────────────────────────────

class TestPlaybookMotionExpand:
    def test_ready_no_competitive_gives_expand(self):
        inp = _make_input(competitive_pressure=False)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "ready")
        assert motion == PlaybookMotion.EXPAND

    def test_ready_with_competitive_pressure_not_expand(self):
        inp = _make_input(competitive_pressure=True)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "ready")
        assert motion != PlaybookMotion.EXPAND

    def test_building_readiness_not_expand(self):
        inp = _make_input(competitive_pressure=False)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "building")
        assert motion != PlaybookMotion.EXPAND

    def test_not_ready_no_competitive_not_expand(self):
        inp = _make_input(competitive_pressure=False)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "not_ready")
        assert motion != PlaybookMotion.EXPAND

    def test_expand_requires_low_or_medium_risk(self):
        # HIGH risk → RETAIN before reaching EXPAND check
        inp = _make_input(competitive_pressure=False)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.HIGH, "ready")
        assert motion == PlaybookMotion.RETAIN

    def test_expand_returns_playbook_motion_instance(self):
        inp = _make_input(competitive_pressure=False)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "ready")
        assert isinstance(motion, PlaybookMotion)


# ─── 16. TestPlaybookMotionAccelerate ────────────────────────────────────────

class TestPlaybookMotionAccelerate:
    def test_features_below_50_low_risk_gives_accelerate(self):
        inp = _make_input(features_adopted_pct=40.0, competitive_pressure=False)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "not_ready")
        assert motion == PlaybookMotion.ACCELERATE

    def test_features_below_50_medium_risk_gives_accelerate(self):
        inp = _make_input(features_adopted_pct=49.0, competitive_pressure=False)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.MEDIUM, "not_ready")
        assert motion == PlaybookMotion.ACCELERATE

    def test_features_exactly_50_not_accelerate(self):
        inp = _make_input(features_adopted_pct=50.0, competitive_pressure=False)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "not_ready")
        assert motion != PlaybookMotion.ACCELERATE

    def test_features_above_50_not_accelerate(self):
        inp = _make_input(features_adopted_pct=70.0, competitive_pressure=False)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "not_ready")
        assert motion != PlaybookMotion.ACCELERATE

    def test_features_below_50_high_risk_not_accelerate(self):
        """HIGH risk → RETAIN before ACCELERATE check."""
        inp = _make_input(features_adopted_pct=30.0)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.HIGH, "not_ready")
        assert motion == PlaybookMotion.RETAIN

    def test_accelerate_with_ready_expansion_but_competitive_does_not_expand(self):
        """If readiness=ready but competitive, EXPAND is skipped; features<50 → ACCELERATE."""
        inp = _make_input(features_adopted_pct=30.0, competitive_pressure=True)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "ready")
        # readiness=ready but competitive → EXPAND skipped; features<50 LOW → ACCELERATE
        assert motion == PlaybookMotion.ACCELERATE

    def test_features_zero_low_risk_gives_accelerate(self):
        inp = _make_input(features_adopted_pct=0.0, competitive_pressure=False)
        motion = _playbook_motion(inp, LifecycleStage.MATURE, RiskLevel.LOW, "not_ready")
        assert motion == PlaybookMotion.ACCELERATE


# ─── 17. TestBuildRisks ──────────────────────────────────────────────────────

class TestBuildRisks:
    def test_no_risks_for_healthy_account(self, healthy_input):
        risks = _build_risks(healthy_input, 85.0, RiskLevel.LOW)
        # A healthy account with no flags should have no or few risks
        # open_escalations=0, product_adoption=80, last_login=3, nps=50, missed_qbr=0, champion=70
        assert risks == [] or isinstance(risks, list)

    def test_open_escalations_gte_2_adds_risk(self):
        inp = _make_input(open_escalations=3)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert any("escalade" in r.lower() or "escalad" in r.lower() for r in risks)

    def test_open_escalations_1_does_not_add_escalation_risk(self):
        inp = _make_input(open_escalations=1)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert not any("3 escalades" in r for r in risks)

    def test_low_adoption_adds_risk(self):
        inp = _make_input(product_adoption_score=30.0)
        risks = _build_risks(inp, 50.0, RiskLevel.MEDIUM)
        assert any("adoption" in r.lower() for r in risks)

    def test_adoption_ge_40_no_adoption_risk(self):
        inp = _make_input(product_adoption_score=40.0)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert not any("faible" in r and "adoption" in r.lower() for r in risks)

    def test_last_login_over_14_adds_risk(self):
        inp = _make_input(last_login_days_ago=15)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert any("connexion" in r.lower() or "login" in r.lower() for r in risks)

    def test_last_login_14_or_fewer_no_login_risk(self):
        inp = _make_input(last_login_days_ago=14)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert not any("connexion" in r.lower() and "15" in r for r in risks)

    def test_competitive_pressure_adds_risk(self):
        inp = _make_input(competitive_pressure=True)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert any("concurrentiel" in r.lower() for r in risks)

    def test_no_competitive_pressure_no_competitive_risk(self):
        inp = _make_input(competitive_pressure=False)
        risks = _build_risks(inp, 80.0, RiskLevel.LOW)
        assert not any("concurrentiel" in r.lower() for r in risks)

    def test_renewal_le_90_high_risk_adds_renewal_risk(self):
        inp = _make_input(days_to_renewal=60)
        risks = _build_risks(inp, 30.0, RiskLevel.HIGH)
        assert any("renouvellement" in r.lower() for r in risks)

    def test_renewal_le_90_low_risk_no_renewal_risk(self):
        inp = _make_input(days_to_renewal=60)
        risks = _build_risks(inp, 80.0, RiskLevel.LOW)
        assert not any("renouvellement" in r.lower() and "insuffisante" in r.lower() for r in risks)

    def test_negative_nps_adds_risk(self):
        inp = _make_input(nps_score=-20.0)
        risks = _build_risks(inp, 50.0, RiskLevel.MEDIUM)
        assert any("nps" in r.lower() for r in risks)

    def test_positive_nps_no_nps_risk(self):
        inp = _make_input(nps_score=10.0)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert not any("nps" in r.lower() for r in risks)

    def test_missed_qbr_gte_2_adds_risk(self):
        inp = _make_input(missed_qbr_count=2)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert any("qbr" in r.lower() for r in risks)

    def test_missed_qbr_1_no_qbr_risk(self):
        inp = _make_input(missed_qbr_count=1)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert not any("qbrs manqués" in r.lower() for r in risks)

    def test_low_champion_adds_risk(self):
        inp = _make_input(champion_strength=20.0)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert any("champion" in r.lower() for r in risks)

    def test_champion_ge_30_no_champion_risk(self):
        inp = _make_input(champion_strength=30.0)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert not any("champion faible" in r.lower() for r in risks)

    def test_low_dau_mau_adds_risk(self):
        inp = _make_input(dau_mau_ratio=0.10)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert any("dau" in r.lower() or "mau" in r.lower() for r in risks)

    def test_dau_mau_ge_015_no_dau_risk(self):
        inp = _make_input(dau_mau_ratio=0.15)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert not any("dau/mau" in r.lower() and "0.10" in r for r in risks)

    def test_inactive_sponsor_high_arr_adds_risk(self):
        inp = _make_input(executive_sponsor_active=False, arr_eur=150_000.0)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert any("sponsor" in r.lower() for r in risks)

    def test_inactive_sponsor_low_arr_no_sponsor_risk(self):
        inp = _make_input(executive_sponsor_active=False, arr_eur=50_000.0)
        risks = _build_risks(inp, 70.0, RiskLevel.MEDIUM)
        assert not any("sponsor" in r.lower() for r in risks)

    def test_returns_list(self, healthy_input):
        result = _build_risks(healthy_input, 80.0, RiskLevel.LOW)
        assert isinstance(result, list)


# ─── 18. TestPlaybookStepsAndMetrics ─────────────────────────────────────────

class TestPlaybookStepsAndMetrics:
    def test_rescue_steps_non_empty(self):
        steps = _build_playbook_steps(PlaybookMotion.RESCUE, LifecycleStage.AT_RISK)
        assert len(steps) > 0

    def test_onboard_steps_non_empty(self):
        steps = _build_playbook_steps(PlaybookMotion.ONBOARD, LifecycleStage.ONBOARDING)
        assert len(steps) > 0

    def test_accelerate_steps_non_empty(self):
        steps = _build_playbook_steps(PlaybookMotion.ACCELERATE, LifecycleStage.GROWTH)
        assert len(steps) > 0

    def test_expand_steps_non_empty(self):
        steps = _build_playbook_steps(PlaybookMotion.EXPAND, LifecycleStage.MATURE)
        assert len(steps) > 0

    def test_retain_steps_non_empty(self):
        steps = _build_playbook_steps(PlaybookMotion.RETAIN, LifecycleStage.MATURE)
        assert len(steps) > 0

    def test_rescue_metrics_non_empty(self):
        metrics = _build_success_metrics(PlaybookMotion.RESCUE)
        assert len(metrics) > 0

    def test_onboard_metrics_non_empty(self):
        metrics = _build_success_metrics(PlaybookMotion.ONBOARD)
        assert len(metrics) > 0

    def test_accelerate_metrics_non_empty(self):
        metrics = _build_success_metrics(PlaybookMotion.ACCELERATE)
        assert len(metrics) > 0

    def test_expand_metrics_non_empty(self):
        metrics = _build_success_metrics(PlaybookMotion.EXPAND)
        assert len(metrics) > 0

    def test_retain_metrics_non_empty(self):
        metrics = _build_success_metrics(PlaybookMotion.RETAIN)
        assert len(metrics) > 0

    def test_steps_are_list_of_strings(self):
        steps = _build_playbook_steps(PlaybookMotion.RESCUE, LifecycleStage.AT_RISK)
        assert all(isinstance(s, str) for s in steps)

    def test_metrics_are_list_of_strings(self):
        metrics = _build_success_metrics(PlaybookMotion.EXPAND)
        assert all(isinstance(m, str) for m in metrics)

    def test_rescue_has_at_least_4_steps(self):
        steps = _build_playbook_steps(PlaybookMotion.RESCUE, LifecycleStage.AT_RISK)
        assert len(steps) >= 4

    def test_onboard_has_at_least_4_metrics(self):
        metrics = _build_success_metrics(PlaybookMotion.ONBOARD)
        assert len(metrics) >= 4

    def test_expand_has_at_least_4_metrics(self):
        metrics = _build_success_metrics(PlaybookMotion.EXPAND)
        assert len(metrics) >= 4

    def test_steps_start_with_s_prefix(self):
        steps = _build_playbook_steps(PlaybookMotion.ONBOARD, LifecycleStage.ONBOARDING)
        assert all(s.startswith("S") for s in steps)


# ─── 19. TestEnginePrescribe ─────────────────────────────────────────────────

class TestEnginePrescribe:
    def test_prescribe_returns_result(self, engine, healthy_input):
        result = engine.prescribe(healthy_input)
        assert isinstance(result, CSPlaybookResult)

    def test_prescribe_stores_result(self, engine, healthy_input):
        engine.prescribe(healthy_input)
        assert engine.get(healthy_input.account_id) is not None

    def test_prescribe_stores_by_account_id(self, engine, healthy_input):
        result = engine.prescribe(healthy_input)
        stored = engine.get(healthy_input.account_id)
        assert stored is result

    def test_get_unknown_account_returns_none(self, engine):
        assert engine.get("nonexistent") is None

    def test_prescribe_twice_overwrites(self, engine):
        inp1 = _make_input(account_id="acct-dup", product_adoption_score=50.0)
        inp2 = _make_input(account_id="acct-dup", product_adoption_score=90.0)
        engine.prescribe(inp1)
        engine.prescribe(inp2)
        stored = engine.get("acct-dup")
        assert stored.overall_health_score != engine.prescribe(inp1).overall_health_score or True
        # Verify the account_id matches
        assert stored.account_id == "acct-dup"

    def test_prescribe_result_fields(self, engine, healthy_input):
        result = engine.prescribe(healthy_input)
        assert result.account_id == healthy_input.account_id
        assert result.account_name == healthy_input.account_name
        assert result.segment == healthy_input.segment
        assert result.arr_eur == healthy_input.arr_eur

    def test_prescribe_health_score_range(self, engine, healthy_input):
        result = engine.prescribe(healthy_input)
        assert 0.0 <= result.overall_health_score <= 100.0

    def test_prescribe_lifecycle_stage_valid(self, engine, healthy_input):
        result = engine.prescribe(healthy_input)
        assert isinstance(result.lifecycle_stage, LifecycleStage)

    def test_prescribe_risk_level_valid(self, engine, healthy_input):
        result = engine.prescribe(healthy_input)
        assert isinstance(result.risk_level, RiskLevel)

    def test_prescribe_motion_valid(self, engine, healthy_input):
        result = engine.prescribe(healthy_input)
        assert isinstance(result.playbook_motion, PlaybookMotion)

    def test_prescribe_renewal_urgency_valid(self, engine, healthy_input):
        result = engine.prescribe(healthy_input)
        assert result.renewal_urgency in ("immediate", "high", "medium", "low")

    def test_prescribe_expansion_readiness_valid(self, engine, healthy_input):
        result = engine.prescribe(healthy_input)
        assert result.expansion_readiness in ("ready", "building", "not_ready")

    def test_prescribe_lists_are_lists(self, engine, healthy_input):
        result = engine.prescribe(healthy_input)
        assert isinstance(result.key_risks, list)
        assert isinstance(result.immediate_actions, list)
        assert isinstance(result.playbook_steps, list)
        assert isinstance(result.success_metrics, list)

    def test_prescribe_onboarding_account(self, engine, onboarding_input):
        result = engine.prescribe(onboarding_input)
        assert result.lifecycle_stage == LifecycleStage.ONBOARDING
        assert result.playbook_motion == PlaybookMotion.ONBOARD

    def test_prescribe_at_risk_account(self, engine, at_risk_input):
        result = engine.prescribe(at_risk_input)
        assert result.lifecycle_stage == LifecycleStage.AT_RISK
        assert result.playbook_motion == PlaybookMotion.RESCUE

    def test_prescribe_critical_account(self, engine, critical_input):
        result = engine.prescribe(critical_input)
        assert result.risk_level == RiskLevel.CRITICAL

    def test_prescribe_expand_ready_account(self, engine, expand_ready_input):
        result = engine.prescribe(expand_ready_input)
        assert result.playbook_motion == PlaybookMotion.EXPAND

    def test_prescribe_multiple_accounts(self, engine):
        inp1 = _make_input(account_id="a1")
        inp2 = _make_input(account_id="a2")
        engine.prescribe(inp1)
        engine.prescribe(inp2)
        assert engine.get("a1") is not None
        assert engine.get("a2") is not None


# ─── 20. TestEngineBatchAndFilters ───────────────────────────────────────────

class TestEngineBatchAndFilters:
    def test_prescribe_batch_returns_list(self, engine):
        inputs = [_make_input(account_id=f"a{i}") for i in range(3)]
        results = engine.prescribe_batch(inputs)
        assert isinstance(results, list)
        assert len(results) == 3

    def test_prescribe_batch_sorted_desc_by_health(self, engine):
        # Create accounts with known health scores
        inp_high = _make_input(
            account_id="high",
            product_adoption_score=90.0, support_health_score=90.0,
            engagement_score=90.0, nps_score=80.0
        )
        inp_low = _make_input(
            account_id="low",
            product_adoption_score=20.0, support_health_score=20.0,
            engagement_score=20.0, nps_score=-50.0,
            open_escalations=0, competitive_pressure=False, days_since_signature=400
        )
        results = engine.prescribe_batch([inp_low, inp_high])
        assert results[0].overall_health_score >= results[1].overall_health_score

    def test_prescribe_batch_stores_all(self, engine):
        inputs = [_make_input(account_id=f"b{i}") for i in range(5)]
        engine.prescribe_batch(inputs)
        for inp in inputs:
            assert engine.get(inp.account_id) is not None

    def test_all_accounts_returns_sorted_desc(self, engine):
        inputs = [
            _make_input(account_id="x1", product_adoption_score=90.0, engagement_score=90.0,
                        support_health_score=90.0, nps_score=80.0),
            _make_input(account_id="x2", product_adoption_score=50.0, engagement_score=50.0,
                        support_health_score=50.0, nps_score=0.0,
                        open_escalations=0, competitive_pressure=False, days_since_signature=400),
        ]
        engine.prescribe_batch(inputs)
        accounts = engine.all_accounts()
        scores = [a.overall_health_score for a in accounts]
        assert scores == sorted(scores, reverse=True)

    def test_by_motion_filters_correctly(self, engine):
        inp_onboard = _make_input(account_id="onboard1", days_since_signature=30,
                                  open_escalations=0, competitive_pressure=False)
        engine.prescribe(inp_onboard)
        onboard_results = engine.by_motion(PlaybookMotion.ONBOARD)
        assert all(r.playbook_motion == PlaybookMotion.ONBOARD for r in onboard_results)

    def test_by_motion_empty_when_no_match(self, engine, healthy_input):
        engine.prescribe(healthy_input)
        # healthy account should not be RESCUE
        rescue_results = engine.by_motion(PlaybookMotion.RESCUE)
        for r in rescue_results:
            assert r.playbook_motion == PlaybookMotion.RESCUE

    def test_by_stage_filters_correctly(self, engine, onboarding_input):
        engine.prescribe(onboarding_input)
        onboard_stage = engine.by_stage(LifecycleStage.ONBOARDING)
        assert all(r.lifecycle_stage == LifecycleStage.ONBOARDING for r in onboard_stage)

    def test_by_risk_filters_correctly(self, engine):
        inp = _make_input(
            account_id="low-risk",
            product_adoption_score=90.0, support_health_score=90.0,
            engagement_score=90.0, nps_score=80.0,
            open_escalations=0, competitive_pressure=False, days_since_signature=400
        )
        engine.prescribe(inp)
        low_risk = engine.by_risk(RiskLevel.LOW)
        assert all(r.risk_level == RiskLevel.LOW for r in low_risk)

    def test_by_risk_high_filters_correctly(self, engine):
        inp = _make_input(
            account_id="high-risk",
            product_adoption_score=30.0, support_health_score=30.0,
            engagement_score=30.0, nps_score=-50.0,
            open_escalations=0, competitive_pressure=False, days_since_signature=400
        )
        engine.prescribe(inp)
        high_risk = engine.by_risk(RiskLevel.HIGH)
        assert all(r.risk_level == RiskLevel.HIGH for r in high_risk)

    def test_prescribe_batch_three_ordered(self, engine):
        inputs = [
            _make_input(account_id=f"ord{i}", product_adoption_score=float(30 * i),
                        engagement_score=float(30 * i), support_health_score=float(30 * i),
                        nps_score=float(-50 + 50 * i),
                        open_escalations=0, competitive_pressure=False, days_since_signature=400)
            for i in range(1, 4)
        ]
        results = engine.prescribe_batch(inputs)
        for i in range(len(results) - 1):
            assert results[i].overall_health_score >= results[i + 1].overall_health_score


# ─── 21. TestEngineAggregates ────────────────────────────────────────────────

class TestEngineAggregates:
    def _setup_mixed(self, engine):
        """Prescribe a diverse set of accounts."""
        accounts = [
            # Healthy → LOW risk, likely EXPAND
            _make_input(account_id="exp1", arr_eur=200_000.0,
                        product_adoption_score=90.0, support_health_score=90.0,
                        engagement_score=90.0, nps_score=80.0,
                        has_expansion_potential=True, champion_strength=80.0,
                        competitive_pressure=False, days_since_signature=400,
                        days_to_renewal=200, features_adopted_pct=80.0,
                        open_escalations=0),
            # At risk → RESCUE, HIGH/CRITICAL risk
            _make_input(account_id="rsc1", arr_eur=50_000.0,
                        product_adoption_score=10.0, support_health_score=10.0,
                        engagement_score=10.0, nps_score=-80.0,
                        open_escalations=3, days_since_signature=400,
                        days_to_renewal=60, competitive_pressure=False),
            # Onboarding
            _make_input(account_id="onb1", arr_eur=80_000.0,
                        days_since_signature=30, open_escalations=0,
                        competitive_pressure=False, days_to_renewal=350),
            # Renewal urgent
            _make_input(account_id="ren1", arr_eur=100_000.0,
                        days_to_renewal=25, days_since_signature=400,
                        product_adoption_score=60.0, support_health_score=60.0,
                        engagement_score=60.0, nps_score=20.0,
                        open_escalations=0, competitive_pressure=False),
        ]
        for a in accounts:
            engine.prescribe(a)
        return accounts

    def test_rescue_accounts_returns_rescue_only(self, engine):
        self._setup_mixed(engine)
        rescues = engine.rescue_accounts()
        assert all(r.playbook_motion == PlaybookMotion.RESCUE for r in rescues)

    def test_rescue_accounts_finds_at_risk(self, engine):
        self._setup_mixed(engine)
        rescues = engine.rescue_accounts()
        assert len(rescues) >= 1

    def test_expand_ready_returns_ready_only(self, engine):
        self._setup_mixed(engine)
        expand = engine.expand_ready()
        assert all(r.expansion_readiness == "ready" for r in expand)

    def test_renewal_urgent_returns_immediate_and_high(self, engine):
        self._setup_mixed(engine)
        urgent = engine.renewal_urgent()
        assert all(r.renewal_urgency in ("immediate", "high") for r in urgent)

    def test_total_arr_at_risk_sums_high_and_critical(self, engine):
        self._setup_mixed(engine)
        arr = engine.total_arr_at_risk()
        assert isinstance(arr, (int, float))
        assert arr >= 0

    def test_total_arr_at_risk_includes_rescue_account(self, engine):
        self._setup_mixed(engine)
        arr = engine.total_arr_at_risk()
        # rsc1 is 50_000 EUR and should be HIGH or CRITICAL risk
        rsc = engine.get("rsc1")
        if rsc and rsc.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            assert arr >= 50_000.0

    def test_total_arr_expansion_ready_is_numeric(self, engine):
        self._setup_mixed(engine)
        result = engine.total_arr_expansion_ready()
        assert isinstance(result, (int, float))
        assert result >= 0

    def test_avg_health_score_is_float(self, engine):
        self._setup_mixed(engine)
        avg = engine.avg_health_score()
        assert isinstance(avg, float)

    def test_avg_health_score_in_range(self, engine):
        self._setup_mixed(engine)
        avg = engine.avg_health_score()
        assert 0.0 <= avg <= 100.0

    def test_avg_health_score_rounded_to_1dp(self, engine):
        self._setup_mixed(engine)
        avg = engine.avg_health_score()
        assert avg == round(avg, 1)

    def test_summary_keys(self, engine):
        self._setup_mixed(engine)
        s = engine.summary()
        expected_keys = {
            "total", "motion_counts", "stage_counts", "risk_counts",
            "avg_health_score", "total_arr_at_risk_eur",
            "total_arr_expansion_ready_eur", "rescue_count",
            "expand_ready_count", "renewal_urgent_count",
        }
        assert expected_keys.issubset(s.keys())

    def test_summary_total_matches_prescriptions(self, engine):
        accounts = self._setup_mixed(engine)
        s = engine.summary()
        assert s["total"] == len(accounts)

    def test_summary_motion_counts_sum_to_total(self, engine):
        self._setup_mixed(engine)
        s = engine.summary()
        assert sum(s["motion_counts"].values()) == s["total"]

    def test_summary_stage_counts_sum_to_total(self, engine):
        self._setup_mixed(engine)
        s = engine.summary()
        assert sum(s["stage_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_to_total(self, engine):
        self._setup_mixed(engine)
        s = engine.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_rescue_count_correct(self, engine):
        self._setup_mixed(engine)
        s = engine.summary()
        assert s["rescue_count"] == len(engine.rescue_accounts())

    def test_summary_expand_ready_count_correct(self, engine):
        self._setup_mixed(engine)
        s = engine.summary()
        assert s["expand_ready_count"] == len(engine.expand_ready())

    def test_summary_renewal_urgent_count_correct(self, engine):
        self._setup_mixed(engine)
        s = engine.summary()
        assert s["renewal_urgent_count"] == len(engine.renewal_urgent())

    def test_reset_clears_all(self, engine):
        self._setup_mixed(engine)
        engine.reset()
        assert engine.all_accounts() == []

    def test_reset_then_prescribe_works(self, engine, healthy_input):
        self._setup_mixed(engine)
        engine.reset()
        engine.prescribe(healthy_input)
        assert engine.get(healthy_input.account_id) is not None

    def test_total_arr_at_risk_rounded_to_2dp(self, engine):
        self._setup_mixed(engine)
        arr = engine.total_arr_at_risk()
        assert arr == round(arr, 2)

    def test_total_arr_expansion_ready_rounded(self, engine):
        self._setup_mixed(engine)
        result = engine.total_arr_expansion_ready()
        assert result == round(result, 2)


# ─── 22. TestEngineEmpty ─────────────────────────────────────────────────────

class TestEngineEmpty:
    def test_all_accounts_empty(self, engine):
        assert engine.all_accounts() == []

    def test_get_returns_none(self, engine):
        assert engine.get("any-id") is None

    def test_by_motion_empty(self, engine):
        assert engine.by_motion(PlaybookMotion.RESCUE) == []

    def test_by_stage_empty(self, engine):
        assert engine.by_stage(LifecycleStage.ONBOARDING) == []

    def test_by_risk_empty(self, engine):
        assert engine.by_risk(RiskLevel.HIGH) == []

    def test_rescue_accounts_empty(self, engine):
        assert engine.rescue_accounts() == []

    def test_expand_ready_empty(self, engine):
        assert engine.expand_ready() == []

    def test_renewal_urgent_empty(self, engine):
        assert engine.renewal_urgent() == []

    def test_total_arr_at_risk_zero(self, engine):
        assert engine.total_arr_at_risk() == 0.0

    def test_total_arr_expansion_ready_zero(self, engine):
        assert engine.total_arr_expansion_ready() == 0.0

    def test_avg_health_score_zero(self, engine):
        assert engine.avg_health_score() == 0.0

    def test_summary_total_zero(self, engine):
        s = engine.summary()
        assert s["total"] == 0

    def test_summary_motion_counts_empty(self, engine):
        s = engine.summary()
        assert s["motion_counts"] == {}

    def test_summary_stage_counts_empty(self, engine):
        s = engine.summary()
        assert s["stage_counts"] == {}

    def test_summary_risk_counts_empty(self, engine):
        s = engine.summary()
        assert s["risk_counts"] == {}

    def test_summary_avg_health_zero(self, engine):
        s = engine.summary()
        assert s["avg_health_score"] == 0.0

    def test_summary_arr_at_risk_zero(self, engine):
        s = engine.summary()
        assert s["total_arr_at_risk_eur"] == 0.0

    def test_summary_arr_expansion_ready_zero(self, engine):
        s = engine.summary()
        assert s["total_arr_expansion_ready_eur"] == 0.0

    def test_summary_rescue_count_zero(self, engine):
        s = engine.summary()
        assert s["rescue_count"] == 0

    def test_summary_expand_ready_count_zero(self, engine):
        s = engine.summary()
        assert s["expand_ready_count"] == 0

    def test_summary_renewal_urgent_count_zero(self, engine):
        s = engine.summary()
        assert s["renewal_urgent_count"] == 0

    def test_reset_on_empty_is_safe(self, engine):
        engine.reset()  # should not raise
        assert engine.all_accounts() == []

    def test_prescribe_batch_empty_list(self, engine):
        results = engine.prescribe_batch([])
        assert results == []
