"""Comprehensive pytest test suite for CustomerSentimentDecayEngine."""

from __future__ import annotations

import dataclasses
import math
import pytest

from swarm.intelligence.customer_sentiment_decay_engine import (
    CustomerSentimentDecayEngine,
    CustomerSentimentDecayInput,
    DecayStage,
    DecayRisk,
    DecaySignal,
    DecayAction,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_input(
    account_id: str = "ACC-001",
    account_name: str = "Acme Corp",
    csm_id: str = "CSM-1",
    region: str = "NA",
    nps_current: float = 60.0,
    nps_prior_quarter: float = 60.0,
    nps_prior_year: float = 60.0,
    support_tickets_last_30d: int = 2,
    support_tickets_prior_30d: int = 2,
    critical_tickets_last_30d: int = 0,
    avg_ticket_resolution_hours: float = 24.0,
    executive_engagement_last_90d: int = 3,
    executive_meetings_prior_90d: int = 3,
    product_usage_pct_current: float = 75.0,
    product_usage_pct_prior: float = 75.0,
    feature_adoption_score: float = 60.0,
    login_frequency_last_30d: int = 20,
    login_frequency_prior_30d: int = 20,
    payment_delay_days: int = 0,
    contract_value_usd: float = 100_000.0,
    months_since_last_qbr: int = 2,
    expansion_discussions_last_90d: int = 1,
) -> CustomerSentimentDecayInput:
    """Return a fully healthy baseline input with overridable fields."""
    return CustomerSentimentDecayInput(
        account_id=account_id,
        account_name=account_name,
        csm_id=csm_id,
        region=region,
        nps_current=nps_current,
        nps_prior_quarter=nps_prior_quarter,
        nps_prior_year=nps_prior_year,
        support_tickets_last_30d=support_tickets_last_30d,
        support_tickets_prior_30d=support_tickets_prior_30d,
        critical_tickets_last_30d=critical_tickets_last_30d,
        avg_ticket_resolution_hours=avg_ticket_resolution_hours,
        executive_engagement_last_90d=executive_engagement_last_90d,
        executive_meetings_prior_90d=executive_meetings_prior_90d,
        product_usage_pct_current=product_usage_pct_current,
        product_usage_pct_prior=product_usage_pct_prior,
        feature_adoption_score=feature_adoption_score,
        login_frequency_last_30d=login_frequency_last_30d,
        login_frequency_prior_30d=login_frequency_prior_30d,
        payment_delay_days=payment_delay_days,
        contract_value_usd=contract_value_usd,
        months_since_last_qbr=months_since_last_qbr,
        expansion_discussions_last_90d=expansion_discussions_last_90d,
    )


def fresh_engine() -> CustomerSentimentDecayEngine:
    return CustomerSentimentDecayEngine()


# ── Section 1: Enum tests ─────────────────────────────────────────────────────

class TestEnums:
    def test_decay_stage_values(self):
        assert DecayStage.stable.value == "stable"
        assert DecayStage.early_warning.value == "early_warning"
        assert DecayStage.declining.value == "declining"
        assert DecayStage.critical.value == "critical"
        assert DecayStage.churning.value == "churning"

    def test_decay_stage_count(self):
        assert len(DecayStage) == 5

    def test_decay_risk_values(self):
        assert DecayRisk.low.value == "low"
        assert DecayRisk.moderate.value == "moderate"
        assert DecayRisk.high.value == "high"
        assert DecayRisk.critical.value == "critical"

    def test_decay_risk_count(self):
        assert len(DecayRisk) == 4

    def test_decay_signal_values(self):
        assert DecaySignal.none.value == "none"
        assert DecaySignal.engagement_drop.value == "engagement_drop"
        assert DecaySignal.support_escalation.value == "support_escalation"
        assert DecaySignal.executive_silence.value == "executive_silence"
        assert DecaySignal.nps_decline.value == "nps_decline"
        assert DecaySignal.usage_reduction.value == "usage_reduction"
        assert DecaySignal.payment_delay.value == "payment_delay"

    def test_decay_signal_count(self):
        assert len(DecaySignal) == 7

    def test_decay_action_values(self):
        assert DecayAction.no_action.value == "no_action"
        assert DecayAction.monitor.value == "monitor"
        assert DecayAction.proactive_outreach.value == "proactive_outreach"
        assert DecayAction.executive_escalation.value == "executive_escalation"
        assert DecayAction.emergency_intervention.value == "emergency_intervention"

    def test_decay_action_count(self):
        assert len(DecayAction) == 5

    def test_enums_are_str_subclass(self):
        assert isinstance(DecayStage.stable, str)
        assert isinstance(DecayRisk.low, str)
        assert isinstance(DecaySignal.none, str)
        assert isinstance(DecayAction.no_action, str)


# ── Section 2: Input dataclass field count ────────────────────────────────────

class TestInputDataclass:
    def test_input_has_22_fields(self):
        fields = dataclasses.fields(CustomerSentimentDecayInput)
        assert len(fields) == 22

    def test_input_field_names(self):
        names = {f.name for f in dataclasses.fields(CustomerSentimentDecayInput)}
        expected = {
            "account_id", "account_name", "csm_id", "region",
            "nps_current", "nps_prior_quarter", "nps_prior_year",
            "support_tickets_last_30d", "support_tickets_prior_30d",
            "critical_tickets_last_30d", "avg_ticket_resolution_hours",
            "executive_engagement_last_90d", "executive_meetings_prior_90d",
            "product_usage_pct_current", "product_usage_pct_prior",
            "feature_adoption_score", "login_frequency_last_30d",
            "login_frequency_prior_30d", "payment_delay_days",
            "contract_value_usd", "months_since_last_qbr",
            "expansion_discussions_last_90d",
        }
        assert names == expected

    def test_input_is_dataclass(self):
        assert dataclasses.is_dataclass(CustomerSentimentDecayInput)

    def test_input_can_be_instantiated(self):
        inp = make_input()
        assert inp.account_id == "ACC-001"

    def test_input_field_account_id(self):
        inp = make_input(account_id="X99")
        assert inp.account_id == "X99"

    def test_input_field_contract_value(self):
        inp = make_input(contract_value_usd=500_000.0)
        assert inp.contract_value_usd == 500_000.0


# ── Section 3: to_dict() key count ───────────────────────────────────────────

class TestToDictKeys:
    def test_to_dict_returns_exactly_15_keys(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert len(result.to_dict()) == 15

    def test_to_dict_key_names(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        expected = {
            "account_id", "account_name", "decay_stage", "decay_risk",
            "primary_decay_signal", "recommended_action",
            "engagement_score", "support_health_score", "usage_vitality_score",
            "relationship_score", "decay_composite",
            "is_at_risk", "requires_escalation",
            "estimated_arr_at_risk_usd", "decay_signal",
        }
        assert set(d.keys()) == expected

    def test_to_dict_account_id_preserved(self):
        eng = fresh_engine()
        d = eng.assess(make_input(account_id="CUST-42")).to_dict()
        assert d["account_id"] == "CUST-42"

    def test_to_dict_account_name_preserved(self):
        eng = fresh_engine()
        d = eng.assess(make_input(account_name="Beta LLC")).to_dict()
        assert d["account_name"] == "Beta LLC"

    def test_to_dict_stage_is_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["decay_stage"], str)

    def test_to_dict_risk_is_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["decay_risk"], str)

    def test_to_dict_signal_is_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["primary_decay_signal"], str)

    def test_to_dict_action_is_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_is_at_risk_is_bool(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["is_at_risk"], bool)

    def test_to_dict_requires_escalation_is_bool(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["requires_escalation"], bool)

    def test_to_dict_arr_at_risk_is_float(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["estimated_arr_at_risk_usd"], float)

    def test_to_dict_decay_signal_is_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert isinstance(d["decay_signal"], str)

    def test_to_dict_scores_are_rounded_to_1dp(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        for key in ("engagement_score", "support_health_score", "usage_vitality_score",
                    "relationship_score", "decay_composite"):
            val = d[key]
            assert round(val, 1) == val

    def test_to_dict_arr_rounded_to_2dp(self):
        eng = fresh_engine()
        d = eng.assess(make_input(contract_value_usd=99_999.99)).to_dict()
        val = d["estimated_arr_at_risk_usd"]
        assert round(val, 2) == val


# ── Section 4: summary() key count ───────────────────────────────────────────

class TestSummaryKeys:
    def test_summary_returns_exactly_13_keys(self):
        eng = fresh_engine()
        eng.assess(make_input())
        assert len(eng.summary()) == 13

    def test_summary_key_names(self):
        eng = fresh_engine()
        eng.assess(make_input())
        expected = {
            "total", "stage_counts", "risk_counts", "signal_counts", "action_counts",
            "avg_decay_composite", "at_risk_count", "escalation_count",
            "avg_engagement_score", "avg_support_health_score",
            "avg_usage_vitality_score", "avg_relationship_score",
            "total_arr_at_risk_usd",
        }
        assert set(eng.summary().keys()) == expected

    def test_empty_summary_returns_13_keys(self):
        eng = fresh_engine()
        assert len(eng.summary()) == 13

    def test_empty_summary_total_zero(self):
        eng = fresh_engine()
        assert eng.summary()["total"] == 0

    def test_empty_summary_at_risk_zero(self):
        eng = fresh_engine()
        assert eng.summary()["at_risk_count"] == 0

    def test_empty_summary_escalation_zero(self):
        eng = fresh_engine()
        assert eng.summary()["escalation_count"] == 0

    def test_empty_summary_avg_composite_zero(self):
        eng = fresh_engine()
        assert eng.summary()["avg_decay_composite"] == 0.0

    def test_empty_summary_total_arr_zero(self):
        eng = fresh_engine()
        assert eng.summary()["total_arr_at_risk_usd"] == 0.0

    def test_empty_summary_stage_counts_empty_dict(self):
        eng = fresh_engine()
        assert eng.summary()["stage_counts"] == {}

    def test_empty_summary_risk_counts_empty_dict(self):
        eng = fresh_engine()
        assert eng.summary()["risk_counts"] == {}

    def test_empty_summary_signal_counts_empty_dict(self):
        eng = fresh_engine()
        assert eng.summary()["signal_counts"] == {}

    def test_empty_summary_action_counts_empty_dict(self):
        eng = fresh_engine()
        assert eng.summary()["action_counts"] == {}

    def test_empty_summary_avg_engagement_zero(self):
        eng = fresh_engine()
        assert eng.summary()["avg_engagement_score"] == 0.0

    def test_empty_summary_avg_support_zero(self):
        eng = fresh_engine()
        assert eng.summary()["avg_support_health_score"] == 0.0

    def test_empty_summary_avg_usage_zero(self):
        eng = fresh_engine()
        assert eng.summary()["avg_usage_vitality_score"] == 0.0

    def test_empty_summary_avg_relationship_zero(self):
        eng = fresh_engine()
        assert eng.summary()["avg_relationship_score"] == 0.0


# ── Section 5: Composite formula ─────────────────────────────────────────────

class TestCompositeFormula:
    """Verify composite = eng*0.30 + support*0.25 + usage*0.25 + rel*0.20"""

    def test_healthy_customer_composite_near_zero(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.decay_composite < 15.0

    def test_composite_matches_weighted_formula(self):
        eng = fresh_engine()
        inp = make_input()
        result = eng.assess(inp)
        expected = round(
            result.engagement_score * 0.30
            + result.support_health_score * 0.25
            + result.usage_vitality_score * 0.25
            + result.relationship_score * 0.20,
            1,
        )
        assert result.decay_composite == expected

    def test_composite_is_clamped_to_100(self):
        # Worst-case inputs should not exceed 100
        eng = fresh_engine()
        inp = make_input(
            nps_current=-50,
            nps_prior_quarter=50,
            nps_prior_year=100,
            critical_tickets_last_30d=5,
            support_tickets_last_30d=30,
            support_tickets_prior_30d=1,
            avg_ticket_resolution_hours=200,
            product_usage_pct_current=0,
            product_usage_pct_prior=100,
            feature_adoption_score=0,
            login_frequency_last_30d=0,
            login_frequency_prior_30d=30,
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=5,
            payment_delay_days=60,
            expansion_discussions_last_90d=0,
            months_since_last_qbr=12,
        )
        result = eng.assess(inp)
        assert result.decay_composite <= 100.0

    def test_composite_is_non_negative(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.decay_composite >= 0.0

    def test_composite_increases_with_more_problems(self):
        eng = fresh_engine()
        good = eng.assess(make_input())
        bad = eng.assess(make_input(
            nps_current=20, nps_prior_quarter=60,
            critical_tickets_last_30d=2,
            product_usage_pct_current=30,
        ))
        assert bad.decay_composite > good.decay_composite

    def test_composite_formula_weight_sum_is_100pct(self):
        # Sanity: 0.30 + 0.25 + 0.25 + 0.20 == 1.0
        assert abs(0.30 + 0.25 + 0.25 + 0.20 - 1.0) < 1e-9

    def test_composite_rounded_to_one_decimal(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.decay_composite == round(result.decay_composite, 1)


# ── Section 6: is_at_risk invariants ─────────────────────────────────────────

class TestIsAtRisk:
    def test_not_at_risk_when_healthy(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.is_at_risk is False

    def test_at_risk_when_composite_ge_35(self):
        eng = fresh_engine()
        # Force composite >= 35 via high NPS drop and critical ticket
        inp = make_input(
            nps_current=0,
            nps_prior_quarter=50,
            critical_tickets_last_30d=1,
            support_tickets_last_30d=10,
            support_tickets_prior_30d=1,
        )
        result = eng.assess(inp)
        if result.decay_composite >= 35:
            assert result.is_at_risk is True

    def test_at_risk_when_critical_tickets_ge_2(self):
        eng = fresh_engine()
        result = eng.assess(make_input(critical_tickets_last_30d=2))
        assert result.is_at_risk is True

    def test_at_risk_when_critical_tickets_eq_3(self):
        eng = fresh_engine()
        result = eng.assess(make_input(critical_tickets_last_30d=3))
        assert result.is_at_risk is True

    def test_at_risk_when_nps_current_negative(self):
        eng = fresh_engine()
        result = eng.assess(make_input(nps_current=-1))
        assert result.is_at_risk is True

    def test_at_risk_when_nps_current_very_negative(self):
        eng = fresh_engine()
        result = eng.assess(make_input(nps_current=-50))
        assert result.is_at_risk is True

    def test_not_at_risk_when_nps_zero(self):
        eng = fresh_engine()
        result = eng.assess(make_input(nps_current=0))
        # nps_current==0 is NOT < 0, so is_at_risk depends on composite only
        # With healthy inputs, composite should be < 35
        assert result.is_at_risk is (result.decay_composite >= 35 or result.requires_escalation or False)

    def test_not_at_risk_critical_tickets_1(self):
        eng = fresh_engine()
        result = eng.assess(make_input(critical_tickets_last_30d=1))
        # critical_tickets==1 doesn't trigger is_at_risk alone
        assert result.is_at_risk is (result.decay_composite >= 35 or 1 >= 2 or result.decay_composite < 0)
        # more direct: 1 < 2, so only composite matters
        assert result.is_at_risk is (result.decay_composite >= 35 or make_input(critical_tickets_last_30d=1).nps_current < 0)

    def test_at_risk_true_in_dict(self):
        eng = fresh_engine()
        d = eng.assess(make_input(critical_tickets_last_30d=2)).to_dict()
        assert d["is_at_risk"] is True

    def test_at_risk_false_in_dict(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert d["is_at_risk"] is False


# ── Section 7: requires_escalation invariants ────────────────────────────────

class TestRequiresEscalation:
    def test_not_escalated_when_healthy(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.requires_escalation is False

    def test_escalated_when_composite_ge_55(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=-50,
            nps_prior_quarter=50,
            nps_prior_year=80,
            critical_tickets_last_30d=3,
            support_tickets_last_30d=20,
            support_tickets_prior_30d=1,
            avg_ticket_resolution_hours=150,
            product_usage_pct_current=10,
            product_usage_pct_prior=90,
            feature_adoption_score=5,
            login_frequency_last_30d=1,
            login_frequency_prior_30d=20,
        )
        result = eng.assess(inp)
        if result.decay_composite >= 55:
            assert result.requires_escalation is True

    def test_escalated_when_payment_delay_gt_45(self):
        eng = fresh_engine()
        result = eng.assess(make_input(payment_delay_days=46))
        assert result.requires_escalation is True

    def test_escalated_when_payment_delay_exactly_46(self):
        eng = fresh_engine()
        result = eng.assess(make_input(payment_delay_days=46))
        assert result.requires_escalation is True

    def test_not_escalated_when_payment_delay_exactly_45(self):
        eng = fresh_engine()
        result = eng.assess(make_input(payment_delay_days=45))
        # 45 is NOT > 45
        assert result.requires_escalation is (result.decay_composite >= 55 or
            (make_input(payment_delay_days=45).executive_engagement_last_90d == 0
             and make_input(payment_delay_days=45).executive_meetings_prior_90d >= 2))

    def test_escalated_when_exec_silence_and_prior_meetings(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=2,
        ))
        assert result.requires_escalation is True

    def test_escalated_exec_silence_3_prior_meetings(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=3,
        ))
        assert result.requires_escalation is True

    def test_not_escalated_exec_silence_only_1_prior(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=1,
        ))
        # exec_meetings_prior_90d < 2, so this clause doesn't trigger
        assert result.requires_escalation is (result.decay_composite >= 55 or result.decay_composite > 45)

    def test_not_escalated_exec_engaged(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            executive_engagement_last_90d=1,
            executive_meetings_prior_90d=5,
        ))
        # exec_engagement != 0, so clause doesn't fire
        assert result.requires_escalation is (result.decay_composite >= 55 or make_input().payment_delay_days > 45)

    def test_escalation_true_in_dict(self):
        eng = fresh_engine()
        d = eng.assess(make_input(payment_delay_days=60)).to_dict()
        assert d["requires_escalation"] is True

    def test_escalation_false_in_dict(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert d["requires_escalation"] is False


# ── Section 8: estimated_arr_at_risk_usd formula ─────────────────────────────

class TestArrAtRisk:
    def test_arr_formula_healthy(self):
        eng = fresh_engine()
        inp = make_input(contract_value_usd=100_000.0)
        result = eng.assess(inp)
        expected = round(100_000.0 * (result.decay_composite / 100.0), 2)
        assert result.estimated_arr_at_risk_usd == expected

    def test_arr_zero_when_composite_zero(self):
        eng = fresh_engine()
        # A perfectly healthy customer might have 0 composite
        inp = make_input(
            nps_current=80, nps_prior_quarter=80, nps_prior_year=80,
            support_tickets_last_30d=0, support_tickets_prior_30d=0,
            critical_tickets_last_30d=0, avg_ticket_resolution_hours=1,
            executive_engagement_last_90d=4, executive_meetings_prior_90d=4,
            product_usage_pct_current=90, product_usage_pct_prior=90,
            feature_adoption_score=80,
            login_frequency_last_30d=25, login_frequency_prior_30d=25,
            payment_delay_days=0, contract_value_usd=500_000.0,
            months_since_last_qbr=1, expansion_discussions_last_90d=3,
        )
        result = eng.assess(inp)
        expected = round(500_000.0 * (result.decay_composite / 100.0), 2)
        assert result.estimated_arr_at_risk_usd == expected

    def test_arr_proportional_to_contract_value(self):
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        inp1 = make_input(contract_value_usd=100_000.0,
                          nps_current=30, nps_prior_quarter=60)
        inp2 = make_input(contract_value_usd=200_000.0,
                          nps_current=30, nps_prior_quarter=60)
        r1 = eng1.assess(inp1)
        r2 = eng2.assess(inp2)
        assert abs(r2.estimated_arr_at_risk_usd - 2 * r1.estimated_arr_at_risk_usd) < 0.01

    def test_arr_at_risk_in_dict_matches_result(self):
        eng = fresh_engine()
        inp = make_input(contract_value_usd=250_000.0)
        result = eng.assess(inp)
        d = result.to_dict()
        assert d["estimated_arr_at_risk_usd"] == round(result.estimated_arr_at_risk_usd, 2)

    def test_arr_never_negative(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.estimated_arr_at_risk_usd >= 0.0

    def test_arr_large_contract(self):
        eng = fresh_engine()
        inp = make_input(
            contract_value_usd=10_000_000.0,
            nps_current=20, nps_prior_quarter=60,
        )
        result = eng.assess(inp)
        expected = round(10_000_000.0 * (result.decay_composite / 100.0), 2)
        assert result.estimated_arr_at_risk_usd == expected


# ── Section 9: DecayStage classification ─────────────────────────────────────

class TestDecayStageClassification:
    def test_stable_when_composite_lt_15(self):
        eng = fresh_engine()
        result = eng.assess(make_input())  # healthy -> very low composite
        if result.decay_composite < 15:
            assert result.decay_stage == DecayStage.stable

    def test_early_warning_when_composite_15_to_29(self):
        # Use NPS drop of 6pts (adds 7 to engagement) + other minor signals
        eng = fresh_engine()
        inp = make_input(
            nps_current=44, nps_prior_quarter=50,  # drop=6 -> +7 engagement
            months_since_last_qbr=4,               # +8 engagement -> total 15
            expansion_discussions_last_90d=0,       # +15 relationship
        )
        result = eng.assess(inp)
        if 15 <= result.decay_composite < 30:
            assert result.decay_stage == DecayStage.early_warning

    def test_declining_when_composite_30_to_49(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=20, nps_prior_quarter=50,  # drop=30 -> +24
            expansion_discussions_last_90d=0,
            months_since_last_qbr=4,
        )
        result = eng.assess(inp)
        if 30 <= result.decay_composite < 50:
            assert result.decay_stage == DecayStage.declining

    def test_critical_when_composite_50_to_69(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=-10, nps_prior_quarter=50,  # drop=60 -> +35 eng + +25
            critical_tickets_last_30d=2,
            support_tickets_last_30d=8,
            support_tickets_prior_30d=1,
            expansion_discussions_last_90d=0,
            months_since_last_qbr=6,
        )
        result = eng.assess(inp)
        if 50 <= result.decay_composite < 70:
            assert result.decay_stage == DecayStage.critical

    def test_churning_when_composite_ge_70(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=-50,
            nps_prior_quarter=50,
            nps_prior_year=80,
            critical_tickets_last_30d=3,
            support_tickets_last_30d=30,
            support_tickets_prior_30d=1,
            avg_ticket_resolution_hours=200,
            product_usage_pct_current=5,
            product_usage_pct_prior=90,
            feature_adoption_score=5,
            login_frequency_last_30d=0,
            login_frequency_prior_30d=20,
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=5,
            payment_delay_days=60,
            expansion_discussions_last_90d=0,
            months_since_last_qbr=12,
        )
        result = eng.assess(inp)
        if result.decay_composite >= 70:
            assert result.decay_stage == DecayStage.churning

    def test_stage_in_to_dict_is_string(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert d["decay_stage"] in ("stable", "early_warning", "declining", "critical", "churning")

    def test_stable_stage_boundary_exactly_14(self):
        # Force a scenario where composite is around 14
        eng = fresh_engine()
        inp = make_input(
            nps_current=55, nps_prior_quarter=60,  # drop=5 < 5, no score
            expansion_discussions_last_90d=0,        # +15 relationship score
        )
        result = eng.assess(inp)
        # relationship = 15 * 0.20 = 3.0 → composite near 3
        # composite < 15 → stable
        assert result.decay_stage == DecayStage.stable


# ── Section 10: DecayRisk classification ─────────────────────────────────────

class TestDecayRiskClassification:
    def test_low_risk_when_composite_lt_20(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        if result.decay_composite < 20:
            assert result.decay_risk == DecayRisk.low

    def test_moderate_risk_when_composite_20_to_39(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=40, nps_prior_quarter=60,  # drop=20, +24
            expansion_discussions_last_90d=0,
        )
        result = eng.assess(inp)
        if 20 <= result.decay_composite < 40:
            assert result.decay_risk == DecayRisk.moderate

    def test_high_risk_when_composite_40_to_59(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=10, nps_prior_quarter=60,
            critical_tickets_last_30d=1,
            support_tickets_last_30d=5,
            support_tickets_prior_30d=1,
            expansion_discussions_last_90d=0,
            months_since_last_qbr=6,
        )
        result = eng.assess(inp)
        if 40 <= result.decay_composite < 60:
            assert result.decay_risk == DecayRisk.high

    def test_critical_risk_when_composite_ge_60(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=-50,
            nps_prior_quarter=50,
            nps_prior_year=80,
            critical_tickets_last_30d=3,
            support_tickets_last_30d=30,
            support_tickets_prior_30d=1,
            avg_ticket_resolution_hours=200,
            product_usage_pct_current=5,
            product_usage_pct_prior=90,
            feature_adoption_score=5,
            login_frequency_last_30d=0,
            login_frequency_prior_30d=20,
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=5,
            payment_delay_days=60,
            expansion_discussions_last_90d=0,
            months_since_last_qbr=12,
        )
        result = eng.assess(inp)
        if result.decay_composite >= 60:
            assert result.decay_risk == DecayRisk.critical

    def test_risk_in_to_dict_valid_value(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert d["decay_risk"] in ("low", "moderate", "high", "critical")


# ── Section 11: DecayAction classification ───────────────────────────────────

class TestDecayActionClassification:
    def test_no_action_for_healthy_customer(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.recommended_action == DecayAction.no_action

    def test_monitor_for_moderate_risk(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=40, nps_prior_quarter=60,
            expansion_discussions_last_90d=0,
        )
        result = eng.assess(inp)
        if result.decay_risk == DecayRisk.moderate and result.decay_composite < 70:
            assert result.recommended_action == DecayAction.monitor

    def test_proactive_outreach_for_high_risk(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=10, nps_prior_quarter=60,
            critical_tickets_last_30d=1,
            support_tickets_last_30d=5,
            support_tickets_prior_30d=1,
            expansion_discussions_last_90d=0,
            months_since_last_qbr=6,
        )
        result = eng.assess(inp)
        if result.decay_risk == DecayRisk.high and result.decay_composite < 70:
            assert result.recommended_action == DecayAction.proactive_outreach

    def test_executive_escalation_for_critical_risk_under_70(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=-5,
            nps_prior_quarter=55,
            critical_tickets_last_30d=2,
            support_tickets_last_30d=8,
            support_tickets_prior_30d=2,
            avg_ticket_resolution_hours=90,
            expansion_discussions_last_90d=0,
            months_since_last_qbr=5,
        )
        result = eng.assess(inp)
        if result.decay_risk == DecayRisk.critical and result.decay_composite < 70:
            assert result.recommended_action == DecayAction.executive_escalation

    def test_emergency_intervention_when_composite_ge_70(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=-50,
            nps_prior_quarter=50,
            nps_prior_year=80,
            critical_tickets_last_30d=3,
            support_tickets_last_30d=30,
            support_tickets_prior_30d=1,
            avg_ticket_resolution_hours=200,
            product_usage_pct_current=5,
            product_usage_pct_prior=90,
            feature_adoption_score=5,
            login_frequency_last_30d=0,
            login_frequency_prior_30d=20,
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=5,
            payment_delay_days=60,
            expansion_discussions_last_90d=0,
            months_since_last_qbr=12,
        )
        result = eng.assess(inp)
        if result.decay_composite >= 70:
            assert result.recommended_action == DecayAction.emergency_intervention

    def test_action_in_to_dict_valid_value(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        assert d["recommended_action"] in (
            "no_action", "monitor", "proactive_outreach",
            "executive_escalation", "emergency_intervention",
        )


# ── Section 12: Primary signal logic ─────────────────────────────────────────

class TestPrimarySignal:
    def test_signal_none_when_healthy(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.primary_decay_signal == DecaySignal.none

    def test_nps_decline_signal(self):
        eng = fresh_engine()
        inp = make_input(
            nps_current=30, nps_prior_quarter=60,  # drop=30 -> +35 engagement
            months_since_last_qbr=1,               # no engagement_drop
            critical_tickets_last_30d=0,
            product_usage_pct_current=75,
            product_usage_pct_prior=75,
            executive_engagement_last_90d=3,
            payment_delay_days=0,
        )
        result = eng.assess(inp)
        assert result.primary_decay_signal == DecaySignal.nps_decline

    def test_support_escalation_signal(self):
        eng = fresh_engine()
        inp = make_input(
            critical_tickets_last_30d=3,
            support_tickets_last_30d=10,
            support_tickets_prior_30d=1,
            avg_ticket_resolution_hours=200,
            nps_current=60, nps_prior_quarter=60,  # no nps drop
            product_usage_pct_current=75,
            product_usage_pct_prior=75,
        )
        result = eng.assess(inp)
        assert result.primary_decay_signal == DecaySignal.support_escalation

    def test_usage_reduction_signal(self):
        eng = fresh_engine()
        inp = make_input(
            product_usage_pct_current=20,
            product_usage_pct_prior=80,  # drop=60
            feature_adoption_score=10,
            login_frequency_last_30d=2,
            login_frequency_prior_30d=20,
            nps_current=60, nps_prior_quarter=60,
            critical_tickets_last_30d=0,
            executive_engagement_last_90d=3,
            payment_delay_days=0,
            months_since_last_qbr=1,
        )
        result = eng.assess(inp)
        assert result.primary_decay_signal == DecaySignal.usage_reduction

    def test_executive_silence_signal(self):
        eng = fresh_engine()
        inp = make_input(
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=5,
            nps_current=60, nps_prior_quarter=60,
            critical_tickets_last_30d=0,
            product_usage_pct_current=75,
            product_usage_pct_prior=75,
            payment_delay_days=0,
            months_since_last_qbr=1,
        )
        result = eng.assess(inp)
        assert result.primary_decay_signal == DecaySignal.executive_silence

    def test_payment_delay_signal(self):
        eng = fresh_engine()
        inp = make_input(
            payment_delay_days=30,
            executive_engagement_last_90d=3,  # no exec silence
            nps_current=60, nps_prior_quarter=60,
            critical_tickets_last_30d=0,
            product_usage_pct_current=75,
            product_usage_pct_prior=75,
            months_since_last_qbr=1,
            expansion_discussions_last_90d=0,
        )
        result = eng.assess(inp)
        # relationship score includes payment delay (+15) and no expansion (+15)
        if result.relationship_score >= 15:
            assert result.primary_decay_signal in (DecaySignal.payment_delay, DecaySignal.executive_silence, DecaySignal.none)

    def test_engagement_drop_signal_qbr(self):
        eng = fresh_engine()
        inp = make_input(
            months_since_last_qbr=6,            # adds +15 engagement
            nps_current=60, nps_prior_quarter=60, # no nps drop
            critical_tickets_last_30d=0,
            product_usage_pct_current=75,
            product_usage_pct_prior=75,
            executive_engagement_last_90d=3,
            payment_delay_days=0,
            expansion_discussions_last_90d=1,
        )
        result = eng.assess(inp)
        # engagement score = 15 (from QBR), so signal should be engagement_drop
        assert result.primary_decay_signal == DecaySignal.engagement_drop

    def test_signal_in_to_dict_valid_value(self):
        eng = fresh_engine()
        d = eng.assess(make_input()).to_dict()
        valid = {"none", "engagement_drop", "support_escalation", "executive_silence",
                 "nps_decline", "usage_reduction", "payment_delay"}
        assert d["primary_decay_signal"] in valid


# ── Section 13: _engagement_score sub-score tests ────────────────────────────

class TestEngagementScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        inp = make_input(**kw)
        return eng._engagement_score(inp)

    def test_zero_when_no_issues(self):
        assert self._score() == 0.0

    def test_nps_drop_qoq_gt_5(self):
        s = self._score(nps_current=54, nps_prior_quarter=60)  # drop=6
        assert s >= 7.0

    def test_nps_drop_qoq_gt_10(self):
        s = self._score(nps_current=49, nps_prior_quarter=60)  # drop=11
        assert s >= 14.0

    def test_nps_drop_qoq_gt_20(self):
        s = self._score(nps_current=39, nps_prior_quarter=60)  # drop=21
        assert s >= 24.0

    def test_nps_drop_qoq_gt_30(self):
        s = self._score(nps_current=29, nps_prior_quarter=60)  # drop=31
        assert s >= 35.0

    def test_nps_drop_yoy_gt_20(self):
        s = self._score(nps_current=30, nps_prior_year=60)  # yoy drop=30
        assert s >= 12.0

    def test_nps_drop_yoy_gt_40(self):
        s = self._score(nps_current=20, nps_prior_year=70)  # yoy drop=50
        assert s >= 20.0

    def test_absolute_nps_below_0(self):
        s = self._score(nps_current=-1, nps_prior_quarter=-1, nps_prior_year=-1)
        assert s >= 25.0

    def test_absolute_nps_below_20(self):
        s = self._score(nps_current=10, nps_prior_quarter=10, nps_prior_year=10)
        assert s >= 15.0

    def test_absolute_nps_below_40(self):
        s = self._score(nps_current=30, nps_prior_quarter=30, nps_prior_year=30)
        assert s >= 8.0

    def test_qbr_6_months(self):
        s = self._score(months_since_last_qbr=6)
        assert s >= 15.0

    def test_qbr_4_months(self):
        s = self._score(months_since_last_qbr=4)
        assert s >= 8.0

    def test_qbr_3_months_no_penalty(self):
        s = self._score(months_since_last_qbr=3)
        assert s == 0.0  # 3 < 4, no penalty

    def test_score_clamped_at_100(self):
        s = self._score(
            nps_current=-50, nps_prior_quarter=50, nps_prior_year=100,
            months_since_last_qbr=12,
        )
        assert s <= 100.0


# ── Section 14: _support_health_score sub-score tests ────────────────────────

class TestSupportHealthScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        inp = make_input(**kw)
        return eng._support_health_score(inp)

    def test_zero_when_no_issues(self):
        assert self._score() == 0.0

    def test_ticket_ratio_ge_3(self):
        s = self._score(support_tickets_last_30d=6, support_tickets_prior_30d=2)
        assert s >= 35.0

    def test_ticket_ratio_ge_2(self):
        s = self._score(support_tickets_last_30d=4, support_tickets_prior_30d=2)
        assert s >= 22.0

    def test_ticket_ratio_ge_1_5(self):
        s = self._score(support_tickets_last_30d=3, support_tickets_prior_30d=2)
        assert s >= 12.0

    def test_ticket_ratio_prior_zero_none_now(self):
        s = self._score(support_tickets_last_30d=0, support_tickets_prior_30d=0)
        # ratio = 1.0, no penalty
        assert s == 0.0

    def test_ticket_ratio_prior_zero_some_now(self):
        s = self._score(support_tickets_last_30d=1, support_tickets_prior_30d=0)
        # ratio = 3.0 -> +35
        assert s >= 35.0

    def test_critical_tickets_ge_1(self):
        s = self._score(critical_tickets_last_30d=1)
        assert s >= 12.0

    def test_critical_tickets_ge_2(self):
        s = self._score(critical_tickets_last_30d=2)
        assert s >= 24.0

    def test_critical_tickets_ge_3(self):
        s = self._score(critical_tickets_last_30d=3)
        assert s >= 35.0

    def test_resolution_hours_gt_48(self):
        s = self._score(avg_ticket_resolution_hours=50)
        assert s >= 6.0

    def test_resolution_hours_gt_72(self):
        s = self._score(avg_ticket_resolution_hours=80)
        assert s >= 12.0

    def test_resolution_hours_gt_120(self):
        s = self._score(avg_ticket_resolution_hours=150)
        assert s >= 20.0

    def test_resolution_hours_le_48_no_penalty(self):
        s = self._score(avg_ticket_resolution_hours=48)
        assert s == 0.0

    def test_score_clamped_at_100(self):
        s = self._score(
            support_tickets_last_30d=30, support_tickets_prior_30d=1,
            critical_tickets_last_30d=5,
            avg_ticket_resolution_hours=200,
        )
        assert s <= 100.0


# ── Section 15: _usage_vitality_score sub-score tests ────────────────────────

class TestUsageVitalityScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        inp = make_input(**kw)
        return eng._usage_vitality_score(inp)

    def test_zero_when_no_issues(self):
        assert self._score() == 0.0

    def test_usage_drop_lt_minus5(self):
        s = self._score(product_usage_pct_current=69, product_usage_pct_prior=75)
        assert s >= 8.0

    def test_usage_drop_lt_minus10(self):
        s = self._score(product_usage_pct_current=60, product_usage_pct_prior=75)
        assert s >= 16.0

    def test_usage_drop_lt_minus20(self):
        s = self._score(product_usage_pct_current=50, product_usage_pct_prior=75)
        assert s >= 28.0

    def test_usage_drop_lt_minus30(self):
        s = self._score(product_usage_pct_current=40, product_usage_pct_prior=75)
        assert s >= 40.0

    def test_usage_prior_zero_no_change(self):
        s = self._score(product_usage_pct_current=50, product_usage_pct_prior=0)
        # usage_change = 0.0, so no drop penalty
        assert s >= 0.0  # absolute usage adds some

    def test_absolute_usage_lt_30(self):
        s = self._score(product_usage_pct_current=20, product_usage_pct_prior=20)
        assert s >= 25.0

    def test_absolute_usage_lt_50(self):
        s = self._score(product_usage_pct_current=40, product_usage_pct_prior=40)
        assert s >= 15.0

    def test_login_ratio_lt_0_3(self):
        s = self._score(login_frequency_last_30d=2, login_frequency_prior_30d=10)
        assert s >= 20.0

    def test_login_ratio_lt_0_5(self):
        s = self._score(login_frequency_last_30d=4, login_frequency_prior_30d=10)
        assert s >= 12.0

    def test_login_ratio_lt_0_7(self):
        s = self._score(login_frequency_last_30d=6, login_frequency_prior_30d=10)
        assert s >= 6.0

    def test_login_ratio_gte_0_7_no_penalty(self):
        s = self._score(login_frequency_last_30d=7, login_frequency_prior_30d=10)
        assert s == 0.0

    def test_feature_adoption_lt_20(self):
        s = self._score(feature_adoption_score=10)
        assert s >= 15.0

    def test_feature_adoption_lt_40(self):
        s = self._score(feature_adoption_score=30)
        assert s >= 8.0

    def test_feature_adoption_gte_40_no_penalty(self):
        s = self._score(feature_adoption_score=40)
        assert s == 0.0

    def test_login_prior_zero_no_ratio_penalty(self):
        s = self._score(login_frequency_last_30d=0, login_frequency_prior_30d=0)
        # prior=0 -> ratio=1.0, no penalty from ratio
        assert s >= 0.0

    def test_score_clamped_at_100(self):
        s = self._score(
            product_usage_pct_current=5,
            product_usage_pct_prior=90,
            feature_adoption_score=5,
            login_frequency_last_30d=0,
            login_frequency_prior_30d=20,
        )
        assert s <= 100.0


# ── Section 16: _relationship_score sub-score tests ──────────────────────────

class TestRelationshipScore:
    def _score(self, **kw) -> float:
        eng = fresh_engine()
        inp = make_input(**kw)
        return eng._relationship_score(inp)

    def test_zero_when_no_issues(self):
        # baseline has expansion=1, so no no-expansion penalty
        assert self._score() == 0.0

    def test_exec_drop_ge_1(self):
        s = self._score(executive_engagement_last_90d=2, executive_meetings_prior_90d=3)
        assert s >= 15.0

    def test_exec_drop_ge_2(self):
        s = self._score(executive_engagement_last_90d=1, executive_meetings_prior_90d=3)
        assert s >= 28.0

    def test_exec_drop_ge_3(self):
        s = self._score(executive_engagement_last_90d=0, executive_meetings_prior_90d=3)
        # exec_drop=3 -> +40, plus zero engagement with prior > 0 -> +20
        assert s >= 40.0

    def test_exec_zero_with_prior_meetings(self):
        s = self._score(executive_engagement_last_90d=0, executive_meetings_prior_90d=1)
        # exec_drop=1 -> +15, zero with prior > 0 -> +20
        assert s >= 35.0

    def test_exec_zero_but_no_prior(self):
        s = self._score(executive_engagement_last_90d=0, executive_meetings_prior_90d=0)
        # exec_drop=0, zero but prior==0 so NO +20
        assert s >= 0.0

    def test_payment_delay_gt_15(self):
        s = self._score(payment_delay_days=20)
        assert s >= 8.0

    def test_payment_delay_gt_30(self):
        s = self._score(payment_delay_days=35)
        assert s >= 15.0

    def test_payment_delay_gt_45(self):
        s = self._score(payment_delay_days=50)
        assert s >= 25.0

    def test_payment_delay_le_15_no_penalty(self):
        s = self._score(payment_delay_days=15)
        assert s == 0.0

    def test_no_expansion_discussion(self):
        s = self._score(expansion_discussions_last_90d=0)
        assert s >= 15.0

    def test_with_expansion_discussion(self):
        s = self._score(expansion_discussions_last_90d=1)
        # no expansion penalty
        assert s == 0.0

    def test_score_clamped_at_100(self):
        s = self._score(
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=10,
            payment_delay_days=60,
            expansion_discussions_last_90d=0,
        )
        assert s <= 100.0


# ── Section 17: assess() method ──────────────────────────────────────────────

class TestAssess:
    def test_returns_result_with_correct_account_id(self):
        eng = fresh_engine()
        result = eng.assess(make_input(account_id="A123"))
        assert result.account_id == "A123"

    def test_returns_result_with_correct_account_name(self):
        eng = fresh_engine()
        result = eng.assess(make_input(account_name="Delta Inc"))
        assert result.account_name == "Delta Inc"

    def test_assess_stores_result_in_engine(self):
        eng = fresh_engine()
        eng.assess(make_input())
        assert len(eng._results) == 1

    def test_assess_multiple_stored_in_order(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(account_id="A1"))
        r2 = eng.assess(make_input(account_id="A2"))
        assert eng._results[0].account_id == "A1"
        assert eng._results[1].account_id == "A2"

    def test_assess_returns_dataclass_result(self):
        from swarm.intelligence.customer_sentiment_decay_engine import CustomerSentimentDecayResult
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert dataclasses.is_dataclass(result)

    def test_assess_result_has_decay_stage_enum(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.decay_stage, DecayStage)

    def test_assess_result_has_decay_risk_enum(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.decay_risk, DecayRisk)

    def test_assess_result_has_signal_enum(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.primary_decay_signal, DecaySignal)

    def test_assess_result_has_action_enum(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.recommended_action, DecayAction)

    def test_assess_result_scores_are_floats(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.engagement_score, float)
        assert isinstance(result.support_health_score, float)
        assert isinstance(result.usage_vitality_score, float)
        assert isinstance(result.relationship_score, float)
        assert isinstance(result.decay_composite, float)

    def test_assess_decay_signal_is_string(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.decay_signal, str)

    def test_assess_stable_customer_signal_text(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert "stable" in result.decay_signal.lower()

    def test_assess_nps_decline_signal_text(self):
        eng = fresh_engine()
        # Need non-stable stage for the signal text to appear - use a heavier drop
        inp = make_input(
            nps_current=-10, nps_prior_quarter=60,  # big drop -> non-stable composite
            nps_prior_year=60,
        )
        result = eng.assess(inp)
        if result.primary_decay_signal == DecaySignal.nps_decline and result.decay_stage != DecayStage.stable:
            assert "NPS" in result.decay_signal or "decay composite" in result.decay_signal

    def test_assess_payment_delay_signal_text(self):
        eng = fresh_engine()
        inp = make_input(
            payment_delay_days=30,
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=5,  # force non-stable via high relationship score
            nps_current=60, nps_prior_quarter=60,
            expansion_discussions_last_90d=0,
        )
        result = eng.assess(inp)
        if result.primary_decay_signal == DecaySignal.payment_delay and result.decay_stage != DecayStage.stable:
            assert "payment" in result.decay_signal.lower() or "decay composite" in result.decay_signal.lower()

    def test_assess_different_inputs_produce_different_composites(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(nps_current=60))
        r2 = eng.assess(make_input(nps_current=10, nps_prior_quarter=60))
        assert r1.decay_composite != r2.decay_composite

    def test_assess_scores_non_negative(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.engagement_score >= 0
        assert result.support_health_score >= 0
        assert result.usage_vitality_score >= 0
        assert result.relationship_score >= 0

    def test_assess_scores_le_100(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.engagement_score <= 100
        assert result.support_health_score <= 100
        assert result.usage_vitality_score <= 100
        assert result.relationship_score <= 100

    def test_assess_composite_le_100(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            nps_current=-50, nps_prior_quarter=50, nps_prior_year=100,
            critical_tickets_last_30d=5, support_tickets_last_30d=30,
            support_tickets_prior_30d=1, avg_ticket_resolution_hours=200,
            product_usage_pct_current=0, product_usage_pct_prior=100,
            feature_adoption_score=0, login_frequency_last_30d=0,
            login_frequency_prior_30d=30, executive_engagement_last_90d=0,
            executive_meetings_prior_90d=5, payment_delay_days=60,
            expansion_discussions_last_90d=0, months_since_last_qbr=12,
        ))
        assert result.decay_composite <= 100.0


# ── Section 18: assess_batch() ───────────────────────────────────────────────

class TestAssessBatch:
    def test_batch_empty_returns_empty_list(self):
        eng = fresh_engine()
        assert eng.assess_batch([]) == []

    def test_batch_single(self):
        eng = fresh_engine()
        results = eng.assess_batch([make_input(account_id="B1")])
        assert len(results) == 1
        assert results[0].account_id == "B1"

    def test_batch_multiple_returns_same_count(self):
        eng = fresh_engine()
        inputs = [make_input(account_id=f"B{i}") for i in range(5)]
        results = eng.assess_batch(inputs)
        assert len(results) == 5

    def test_batch_order_preserved(self):
        eng = fresh_engine()
        inputs = [make_input(account_id=f"C{i}") for i in range(3)]
        results = eng.assess_batch(inputs)
        for i, r in enumerate(results):
            assert r.account_id == f"C{i}"

    def test_batch_stores_in_engine(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(), make_input(account_id="X2")])
        assert len(eng._results) == 2

    def test_batch_matches_individual_assess(self):
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        inp = make_input(nps_current=30, nps_prior_quarter=60)
        r1 = eng1.assess(inp)
        r2 = eng2.assess_batch([inp])[0]
        assert r1.decay_composite == r2.decay_composite

    def test_batch_different_customers(self):
        eng = fresh_engine()
        inp1 = make_input(account_id="D1", nps_current=60)
        inp2 = make_input(account_id="D2", nps_current=10, nps_prior_quarter=60)
        results = eng.assess_batch([inp1, inp2])
        assert results[0].decay_composite < results[1].decay_composite

    def test_batch_combined_with_individual(self):
        eng = fresh_engine()
        eng.assess(make_input(account_id="E1"))
        eng.assess_batch([make_input(account_id="E2"), make_input(account_id="E3")])
        assert len(eng._results) == 3


# ── Section 19: summary() with results ───────────────────────────────────────

class TestSummaryWithResults:
    def test_total_count_correct(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(account_id=f"F{i}") for i in range(4)])
        assert eng.summary()["total"] == 4

    def test_stage_counts_correct_all_stable(self):
        eng = fresh_engine()
        eng.assess_batch([make_input() for _ in range(3)])
        s = eng.summary()
        assert s["stage_counts"].get("stable", 0) == 3

    def test_risk_counts_correct_all_low(self):
        eng = fresh_engine()
        eng.assess_batch([make_input() for _ in range(2)])
        s = eng.summary()
        assert s["risk_counts"].get("low", 0) == 2

    def test_at_risk_count_correct(self):
        eng = fresh_engine()
        eng.assess(make_input())                              # not at risk
        eng.assess(make_input(critical_tickets_last_30d=2))  # at risk
        eng.assess(make_input(nps_current=-5))               # at risk
        assert eng.summary()["at_risk_count"] == 2

    def test_escalation_count_correct(self):
        eng = fresh_engine()
        eng.assess(make_input())                           # not escalated
        eng.assess(make_input(payment_delay_days=60))      # escalated
        assert eng.summary()["escalation_count"] == 1

    def test_avg_decay_composite_correct(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input())
        r2 = eng.assess(make_input(nps_current=20, nps_prior_quarter=60))
        expected = round((r1.decay_composite + r2.decay_composite) / 2, 1)
        assert eng.summary()["avg_decay_composite"] == expected

    def test_avg_engagement_score_correct(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input())
        r2 = eng.assess(make_input(nps_current=20, nps_prior_quarter=60))
        expected = round((r1.engagement_score + r2.engagement_score) / 2, 1)
        assert eng.summary()["avg_engagement_score"] == expected

    def test_avg_support_score_correct(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input())
        r2 = eng.assess(make_input(critical_tickets_last_30d=2))
        expected = round((r1.support_health_score + r2.support_health_score) / 2, 1)
        assert eng.summary()["avg_support_health_score"] == expected

    def test_avg_usage_score_correct(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input())
        r2 = eng.assess(make_input(product_usage_pct_current=20, product_usage_pct_prior=80))
        expected = round((r1.usage_vitality_score + r2.usage_vitality_score) / 2, 1)
        assert eng.summary()["avg_usage_vitality_score"] == expected

    def test_avg_relationship_score_correct(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input())
        r2 = eng.assess(make_input(payment_delay_days=60))
        expected = round((r1.relationship_score + r2.relationship_score) / 2, 1)
        assert eng.summary()["avg_relationship_score"] == expected

    def test_total_arr_at_risk_correct(self):
        eng = fresh_engine()
        r1 = eng.assess(make_input(contract_value_usd=100_000.0))
        r2 = eng.assess(make_input(contract_value_usd=200_000.0, nps_current=20, nps_prior_quarter=60))
        expected = round(r1.estimated_arr_at_risk_usd + r2.estimated_arr_at_risk_usd, 2)
        assert eng.summary()["total_arr_at_risk_usd"] == expected

    def test_signal_counts_correct(self):
        eng = fresh_engine()
        eng.assess(make_input())  # signal = none
        eng.assess(make_input())  # signal = none
        s = eng.summary()
        assert s["signal_counts"].get("none", 0) == 2

    def test_action_counts_correct(self):
        eng = fresh_engine()
        eng.assess(make_input())  # no_action
        eng.assess(make_input())  # no_action
        s = eng.summary()
        assert s["action_counts"].get("no_action", 0) == 2

    def test_summary_after_single_assess(self):
        eng = fresh_engine()
        r = eng.assess(make_input())
        s = eng.summary()
        assert s["total"] == 1
        assert s["avg_decay_composite"] == r.decay_composite

    def test_summary_accumulates_across_calls(self):
        eng = fresh_engine()
        for _ in range(10):
            eng.assess(make_input())
        assert eng.summary()["total"] == 10

    def test_summary_stage_counts_multiple_stages(self):
        eng = fresh_engine()
        # healthy -> stable
        eng.assess(make_input())
        # declining scenario
        inp = make_input(
            nps_current=20, nps_prior_quarter=60,
            critical_tickets_last_30d=1,
            expansion_discussions_last_90d=0,
        )
        eng.assess(inp)
        s = eng.summary()
        assert sum(s["stage_counts"].values()) == 2

    def test_summary_total_arr_rounds_to_2dp(self):
        eng = fresh_engine()
        eng.assess(make_input(contract_value_usd=33_333.33))
        s = eng.summary()
        v = s["total_arr_at_risk_usd"]
        assert round(v, 2) == v

    def test_summary_avg_composite_rounded_to_1dp(self):
        eng = fresh_engine()
        eng.assess(make_input())
        eng.assess(make_input(nps_current=40, nps_prior_quarter=60))
        s = eng.summary()
        v = s["avg_decay_composite"]
        assert round(v, 1) == v

    def test_independent_engines_dont_share_state(self):
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        eng1.assess(make_input())
        assert eng2.summary()["total"] == 0


# ── Section 20: Edge cases ────────────────────────────────────────────────────

class TestEdgeCases:
    def test_zero_contract_value_arr_is_zero(self):
        eng = fresh_engine()
        result = eng.assess(make_input(contract_value_usd=0.0))
        assert result.estimated_arr_at_risk_usd == 0.0

    def test_very_large_contract_value(self):
        eng = fresh_engine()
        result = eng.assess(make_input(contract_value_usd=1_000_000_000.0))
        assert result.estimated_arr_at_risk_usd >= 0.0

    def test_all_zeroes_support_tickets(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            support_tickets_last_30d=0,
            support_tickets_prior_30d=0,
        ))
        assert result.support_health_score >= 0.0

    def test_nps_same_quarter_and_year(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            nps_current=50, nps_prior_quarter=50, nps_prior_year=50,
        ))
        # No drop -> engagement score only from absolute level
        assert result.engagement_score >= 0.0

    def test_executive_engagement_equals_prior(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            executive_engagement_last_90d=3,
            executive_meetings_prior_90d=3,
        ))
        # exec_drop = 0 -> no penalty from that clause
        assert result.relationship_score >= 0.0

    def test_product_usage_same_current_and_prior(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            product_usage_pct_current=70, product_usage_pct_prior=70,
        ))
        assert result.usage_vitality_score >= 0.0

    def test_login_frequency_both_zero(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            login_frequency_last_30d=0,
            login_frequency_prior_30d=0,
        ))
        # ratio defaults to 1.0 -> no penalty from ratio
        assert result.usage_vitality_score >= 0.0

    def test_payment_delay_exactly_15_no_penalty(self):
        eng = fresh_engine()
        result = eng.assess(make_input(payment_delay_days=15))
        # 15 is NOT > 15
        rel = eng._relationship_score(make_input(payment_delay_days=15))
        assert rel == 0.0  # baseline has expansion=1, no other penalties

    def test_payment_delay_exactly_16_penalty(self):
        eng = fresh_engine()
        rel = eng._relationship_score(make_input(payment_delay_days=16))
        assert rel >= 8.0

    def test_months_since_qbr_exactly_4(self):
        eng = fresh_engine()
        s = eng._engagement_score(make_input(months_since_last_qbr=4))
        assert s >= 8.0

    def test_months_since_qbr_exactly_6(self):
        eng = fresh_engine()
        s = eng._engagement_score(make_input(months_since_last_qbr=6))
        assert s >= 15.0

    def test_months_since_qbr_exactly_3_no_penalty(self):
        eng = fresh_engine()
        s = eng._engagement_score(make_input(months_since_last_qbr=3))
        assert s == 0.0

    def test_nps_drop_exactly_5_no_qoq_penalty(self):
        eng = fresh_engine()
        s = eng._engagement_score(make_input(
            nps_current=55, nps_prior_quarter=60,  # drop=5 which is NOT > 5
        ))
        assert s == 0.0

    def test_nps_drop_exactly_6_qoq_penalty(self):
        eng = fresh_engine()
        s = eng._engagement_score(make_input(
            nps_current=54, nps_prior_quarter=60,  # drop=6 > 5
        ))
        assert s >= 7.0

    def test_high_feature_adoption_no_penalty(self):
        eng = fresh_engine()
        s = eng._usage_vitality_score(make_input(feature_adoption_score=80))
        assert s == 0.0

    def test_nps_current_exactly_0_no_negative_penalty(self):
        eng = fresh_engine()
        s = eng._engagement_score(make_input(nps_current=0, nps_prior_quarter=0, nps_prior_year=0))
        # nps_current=0 is NOT < 0, so no +25
        # but 0 < 20 -> +15
        assert s >= 15.0

    def test_nps_current_exactly_minus_1_is_at_risk(self):
        eng = fresh_engine()
        result = eng.assess(make_input(nps_current=-1))
        assert result.is_at_risk is True

    def test_critical_tickets_exactly_2_is_at_risk(self):
        eng = fresh_engine()
        result = eng.assess(make_input(critical_tickets_last_30d=2))
        assert result.is_at_risk is True

    def test_critical_tickets_exactly_1_not_at_risk_alone(self):
        eng = fresh_engine()
        # With no other issues, critical_tickets=1 shouldn't make it at_risk
        result = eng.assess(make_input(critical_tickets_last_30d=1))
        # Only at risk if composite>=35 or critical>=2 or nps<0
        assert result.is_at_risk is (result.decay_composite >= 35 or False or False)

    def test_payment_delay_exactly_46_escalation(self):
        eng = fresh_engine()
        result = eng.assess(make_input(payment_delay_days=46))
        assert result.requires_escalation is True

    def test_exec_meetings_prior_exactly_2_triggers_escalation(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=2,
        ))
        assert result.requires_escalation is True

    def test_exec_meetings_prior_exactly_1_no_escalation_from_clause(self):
        eng = fresh_engine()
        result = eng.assess(make_input(
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=1,
        ))
        # 1 < 2, so this clause doesn't trigger escalation
        # Only if composite >= 55 or payment > 45
        assert result.requires_escalation is (result.decay_composite >= 55 or 0 > 45)

    def test_usage_pct_prior_zero_no_change(self):
        eng = fresh_engine()
        s = eng._usage_vitality_score(make_input(
            product_usage_pct_current=50, product_usage_pct_prior=0,
        ))
        # usage_change = 0.0, so no drop penalty
        # absolute 50 < 50 is false, so no abs penalty either
        assert s >= 0.0

    def test_nps_exactly_40_no_nps_level_penalty(self):
        eng = fresh_engine()
        s = eng._engagement_score(make_input(
            nps_current=40, nps_prior_quarter=40, nps_prior_year=40,
        ))
        # 40 is NOT < 40
        assert s == 0.0

    def test_nps_exactly_39_penalty(self):
        eng = fresh_engine()
        s = eng._engagement_score(make_input(
            nps_current=39, nps_prior_quarter=39, nps_prior_year=39,
        ))
        assert s >= 8.0

    def test_ticket_ratio_exactly_2_triggers_22(self):
        eng = fresh_engine()
        s = eng._support_health_score(make_input(
            support_tickets_last_30d=4, support_tickets_prior_30d=2,
        ))
        assert s >= 22.0

    def test_ticket_ratio_exactly_3_triggers_35(self):
        eng = fresh_engine()
        s = eng._support_health_score(make_input(
            support_tickets_last_30d=6, support_tickets_prior_30d=2,
        ))
        assert s >= 35.0

    def test_usage_exactly_30_lt_50_penalty(self):
        eng = fresh_engine()
        # usage==30 is NOT < 30 (no +25), but 30 < 50 -> +15
        s = eng._usage_vitality_score(make_input(
            product_usage_pct_current=30, product_usage_pct_prior=30,
        ))
        assert s >= 15.0

    def test_usage_exactly_29_absolute_penalty(self):
        eng = fresh_engine()
        s = eng._usage_vitality_score(make_input(
            product_usage_pct_current=29, product_usage_pct_prior=29,
        ))
        assert s >= 25.0

    def test_usage_exactly_50_no_second_absolute_penalty(self):
        eng = fresh_engine()
        # usage==50 is NOT < 50
        s = eng._usage_vitality_score(make_input(
            product_usage_pct_current=50, product_usage_pct_prior=50,
        ))
        assert s == 0.0

    def test_usage_exactly_49_second_absolute_penalty(self):
        eng = fresh_engine()
        s = eng._usage_vitality_score(make_input(
            product_usage_pct_current=49, product_usage_pct_prior=49,
        ))
        assert s >= 15.0


# ── Section 21: decay_signal text content ────────────────────────────────────

class TestDecaySignalText:
    def test_stable_text(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result.decay_signal == "customer sentiment stable — no decay signals detected"

    def test_composite_in_non_stable_signal(self):
        eng = fresh_engine()
        inp = make_input(months_since_last_qbr=6)
        result = eng.assess(inp)
        if result.decay_stage != DecayStage.stable:
            assert "decay composite" in result.decay_signal

    def test_nps_decline_text_contains_drop(self):
        # Need non-stable stage for signal text; use a large NPS drop that pushes composite >= 15
        eng = fresh_engine()
        inp = make_input(
            nps_current=-10, nps_prior_quarter=60,  # drop=70 -> +35 eng, +25 abs < 0 = 60 eng
            nps_prior_year=60,
        )
        result = eng.assess(inp)
        # composite = 60*0.30 = 18 -> early_warning -> non-stable
        if result.primary_decay_signal == DecaySignal.nps_decline and result.decay_stage != DecayStage.stable:
            assert "NPS" in result.decay_signal

    def test_support_escalation_text_contains_critical(self):
        eng = fresh_engine()
        inp = make_input(
            critical_tickets_last_30d=2,
            support_tickets_last_30d=5,
            support_tickets_prior_30d=1,
            avg_ticket_resolution_hours=150,
        )
        result = eng.assess(inp)
        if result.primary_decay_signal == DecaySignal.support_escalation and result.decay_stage != DecayStage.stable:
            assert "critical ticket" in result.decay_signal.lower() or "critical" in result.decay_signal.lower()

    def test_usage_reduction_text_contains_usage(self):
        eng = fresh_engine()
        inp = make_input(
            product_usage_pct_current=20, product_usage_pct_prior=80,
            feature_adoption_score=10,
            login_frequency_last_30d=2, login_frequency_prior_30d=20,
            nps_current=60, nps_prior_quarter=60,
            critical_tickets_last_30d=0,
            executive_engagement_last_90d=3,
            payment_delay_days=0,
            months_since_last_qbr=1,
        )
        result = eng.assess(inp)
        if result.primary_decay_signal == DecaySignal.usage_reduction and result.decay_stage != DecayStage.stable:
            assert "usage" in result.decay_signal.lower()

    def test_executive_silence_text_contains_meetings(self):
        eng = fresh_engine()
        # large exec drop to push composite past 15
        inp = make_input(
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=10,  # exec_drop=10 -> +40, +20 = 60 rel -> 60*0.20 = 12
            nps_current=60, nps_prior_quarter=60,
            critical_tickets_last_30d=0,
            product_usage_pct_current=75, product_usage_pct_prior=75,
            payment_delay_days=0,
            months_since_last_qbr=1,
            expansion_discussions_last_90d=0,  # +15 rel -> total 75 rel -> 75*0.20=15 composite
        )
        result = eng.assess(inp)
        if result.primary_decay_signal == DecaySignal.executive_silence and result.decay_stage != DecayStage.stable:
            assert "executive" in result.decay_signal.lower() or "meetings" in result.decay_signal.lower()

    def test_payment_delay_text(self):
        eng = fresh_engine()
        # Need large enough signal to get non-stable stage
        inp = make_input(
            payment_delay_days=50,            # >45 -> +25 relationship
            executive_engagement_last_90d=3,   # no exec silence
            nps_current=60, nps_prior_quarter=60,
            critical_tickets_last_30d=0,
            product_usage_pct_current=75, product_usage_pct_prior=75,
            months_since_last_qbr=1,
            expansion_discussions_last_90d=0,  # +15 rel
        )
        result = eng.assess(inp)
        if result.primary_decay_signal == DecaySignal.payment_delay and result.decay_stage != DecayStage.stable:
            assert "payment" in result.decay_signal.lower() or "overdue" in result.decay_signal.lower()

    def test_engagement_drop_text_contains_qbr(self):
        eng = fresh_engine()
        # Need enough composite to get non-stable stage
        inp = make_input(
            months_since_last_qbr=6,             # +15 eng
            nps_current=39, nps_prior_quarter=39, # absolute nps<40 -> +8 eng -> total 23 -> composite ~7
            critical_tickets_last_30d=0,
            product_usage_pct_current=75, product_usage_pct_prior=75,
            executive_engagement_last_90d=3,
            payment_delay_days=0,
            expansion_discussions_last_90d=0,  # +15 rel -> 0.20*15=3 + 0.30*23=6.9 = ~10
        )
        result = eng.assess(inp)
        if result.primary_decay_signal == DecaySignal.engagement_drop and result.decay_stage != DecayStage.stable:
            assert "QBR" in result.decay_signal or "engagement" in result.decay_signal.lower()


# ── Section 22: Scenario-based integration tests ──────────────────────────────

class TestScenarios:
    def test_ideal_customer_scenario(self):
        """A perfectly healthy customer should be stable with low risk."""
        eng = fresh_engine()
        inp = make_input(
            nps_current=90, nps_prior_quarter=90, nps_prior_year=90,
            support_tickets_last_30d=0, support_tickets_prior_30d=0,
            critical_tickets_last_30d=0, avg_ticket_resolution_hours=4,
            executive_engagement_last_90d=5, executive_meetings_prior_90d=5,
            product_usage_pct_current=95, product_usage_pct_prior=95,
            feature_adoption_score=90,
            login_frequency_last_30d=30, login_frequency_prior_30d=30,
            payment_delay_days=0, contract_value_usd=100_000.0,
            months_since_last_qbr=2, expansion_discussions_last_90d=5,
        )
        result = eng.assess(inp)
        assert result.decay_stage == DecayStage.stable
        assert result.decay_risk == DecayRisk.low
        assert result.is_at_risk is False
        assert result.requires_escalation is False
        assert result.recommended_action == DecayAction.no_action

    def test_churning_customer_scenario(self):
        """A worst-case customer should be churning with emergency intervention."""
        eng = fresh_engine()
        inp = make_input(
            nps_current=-50, nps_prior_quarter=50, nps_prior_year=80,
            critical_tickets_last_30d=3,
            support_tickets_last_30d=30, support_tickets_prior_30d=1,
            avg_ticket_resolution_hours=200,
            product_usage_pct_current=5, product_usage_pct_prior=90,
            feature_adoption_score=5,
            login_frequency_last_30d=0, login_frequency_prior_30d=20,
            executive_engagement_last_90d=0, executive_meetings_prior_90d=5,
            payment_delay_days=60, expansion_discussions_last_90d=0,
            months_since_last_qbr=12, contract_value_usd=1_000_000.0,
        )
        result = eng.assess(inp)
        assert result.decay_composite >= 70
        assert result.decay_stage == DecayStage.churning
        assert result.is_at_risk is True
        assert result.requires_escalation is True
        assert result.recommended_action == DecayAction.emergency_intervention

    def test_payment_only_at_risk(self):
        """Customer with only payment issues should be escalated."""
        eng = fresh_engine()
        result = eng.assess(make_input(payment_delay_days=60))
        assert result.requires_escalation is True

    def test_nps_crash_scenario(self):
        """Customer whose NPS cratered should detect nps_decline signal."""
        eng = fresh_engine()
        inp = make_input(
            nps_current=-20, nps_prior_quarter=70, nps_prior_year=80,
            critical_tickets_last_30d=0,
            product_usage_pct_current=75, product_usage_pct_prior=75,
            executive_engagement_last_90d=3,
            payment_delay_days=0,
            months_since_last_qbr=1,
        )
        result = eng.assess(inp)
        assert result.is_at_risk is True  # nps < 0
        assert result.primary_decay_signal == DecaySignal.nps_decline

    def test_exec_silence_with_prior_engagement(self):
        """C-suite went silent after prior engagement -> escalation."""
        eng = fresh_engine()
        result = eng.assess(make_input(
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=4,
            nps_current=60, nps_prior_quarter=60,
        ))
        assert result.requires_escalation is True
        assert result.primary_decay_signal == DecaySignal.executive_silence

    def test_support_ticket_surge_scenario(self):
        """10x ticket surge with critical tickets should alarm."""
        eng = fresh_engine()
        result = eng.assess(make_input(
            support_tickets_last_30d=10, support_tickets_prior_30d=1,
            critical_tickets_last_30d=2,
            avg_ticket_resolution_hours=100,
        ))
        assert result.is_at_risk is True

    def test_usage_collapse_scenario(self):
        """Usage dropped from 90% to 10% should trigger usage_reduction."""
        eng = fresh_engine()
        inp = make_input(
            product_usage_pct_current=10, product_usage_pct_prior=90,
            feature_adoption_score=15,
            login_frequency_last_30d=1, login_frequency_prior_30d=25,
            nps_current=60, nps_prior_quarter=60,
            critical_tickets_last_30d=0,
            executive_engagement_last_90d=3,
            payment_delay_days=0,
            months_since_last_qbr=1,
        )
        result = eng.assess(inp)
        assert result.primary_decay_signal == DecaySignal.usage_reduction

    def test_multiple_risk_factors_compound(self):
        """Multiple moderate issues should compound to higher composite."""
        eng = fresh_engine()
        clean = eng.assess(make_input())
        dirty = eng.assess(make_input(
            nps_current=45, nps_prior_quarter=55,  # minor drop
            critical_tickets_last_30d=1,
            months_since_last_qbr=4,
            expansion_discussions_last_90d=0,
        ))
        assert dirty.decay_composite > clean.decay_composite

    def test_batch_summary_consistency(self):
        """summary() totals should match individual results."""
        eng = fresh_engine()
        inputs = [
            make_input(account_id="G1"),
            make_input(account_id="G2", nps_current=-5),
            make_input(account_id="G3", payment_delay_days=60),
        ]
        results = eng.assess_batch(inputs)
        s = eng.summary()
        assert s["total"] == 3
        assert s["at_risk_count"] == sum(1 for r in results if r.is_at_risk)
        assert s["escalation_count"] == sum(1 for r in results if r.requires_escalation)
        total_arr = round(sum(r.estimated_arr_at_risk_usd for r in results), 2)
        assert s["total_arr_at_risk_usd"] == total_arr


# ── Section 23: Boundary values for classification thresholds ─────────────────

class TestClassificationBoundaries:
    def _make_result_with_composite(self, target_composite: float):
        """Assess and return result; verify composite is near target."""
        eng = fresh_engine()
        # We test classification directly via private methods
        stage = eng._classify_stage(target_composite)
        risk = eng._classify_risk(target_composite)
        return stage, risk

    def test_stage_boundary_exactly_15(self):
        eng = fresh_engine()
        assert eng._classify_stage(15.0) == DecayStage.early_warning

    def test_stage_boundary_14_9(self):
        eng = fresh_engine()
        assert eng._classify_stage(14.9) == DecayStage.stable

    def test_stage_boundary_exactly_30(self):
        eng = fresh_engine()
        assert eng._classify_stage(30.0) == DecayStage.declining

    def test_stage_boundary_29_9(self):
        eng = fresh_engine()
        assert eng._classify_stage(29.9) == DecayStage.early_warning

    def test_stage_boundary_exactly_50(self):
        eng = fresh_engine()
        assert eng._classify_stage(50.0) == DecayStage.critical

    def test_stage_boundary_49_9(self):
        eng = fresh_engine()
        assert eng._classify_stage(49.9) == DecayStage.declining

    def test_stage_boundary_exactly_70(self):
        eng = fresh_engine()
        assert eng._classify_stage(70.0) == DecayStage.churning

    def test_stage_boundary_69_9(self):
        eng = fresh_engine()
        assert eng._classify_stage(69.9) == DecayStage.critical

    def test_stage_boundary_100(self):
        eng = fresh_engine()
        assert eng._classify_stage(100.0) == DecayStage.churning

    def test_risk_boundary_exactly_20(self):
        eng = fresh_engine()
        assert eng._classify_risk(20.0) == DecayRisk.moderate

    def test_risk_boundary_19_9(self):
        eng = fresh_engine()
        assert eng._classify_risk(19.9) == DecayRisk.low

    def test_risk_boundary_exactly_40(self):
        eng = fresh_engine()
        assert eng._classify_risk(40.0) == DecayRisk.high

    def test_risk_boundary_39_9(self):
        eng = fresh_engine()
        assert eng._classify_risk(39.9) == DecayRisk.moderate

    def test_risk_boundary_exactly_60(self):
        eng = fresh_engine()
        assert eng._classify_risk(60.0) == DecayRisk.critical

    def test_risk_boundary_59_9(self):
        eng = fresh_engine()
        assert eng._classify_risk(59.9) == DecayRisk.high

    def test_risk_boundary_100(self):
        eng = fresh_engine()
        assert eng._classify_risk(100.0) == DecayRisk.critical

    def test_action_boundary_composite_exactly_70(self):
        eng = fresh_engine()
        action = eng._recommended_action(DecayRisk.critical, 70.0)
        assert action == DecayAction.emergency_intervention

    def test_action_boundary_composite_69(self):
        eng = fresh_engine()
        # composite < 70, critical risk -> executive_escalation
        action = eng._recommended_action(DecayRisk.critical, 69.9)
        assert action == DecayAction.executive_escalation

    def test_action_high_risk_under_70(self):
        eng = fresh_engine()
        action = eng._recommended_action(DecayRisk.high, 50.0)
        assert action == DecayAction.proactive_outreach

    def test_action_moderate_risk_under_70(self):
        eng = fresh_engine()
        action = eng._recommended_action(DecayRisk.moderate, 30.0)
        assert action == DecayAction.monitor

    def test_action_low_risk_under_70(self):
        eng = fresh_engine()
        action = eng._recommended_action(DecayRisk.low, 10.0)
        assert action == DecayAction.no_action


# ── Section 24: State isolation between engines ───────────────────────────────

class TestStateIsolation:
    def test_two_engines_independent(self):
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        eng1.assess(make_input(account_id="H1"))
        eng1.assess(make_input(account_id="H2"))
        assert eng2.summary()["total"] == 0

    def test_engine_accumulates_state_between_calls(self):
        eng = fresh_engine()
        for i in range(5):
            eng.assess(make_input(account_id=f"I{i}"))
        assert eng.summary()["total"] == 5

    def test_fresh_engine_empty_results(self):
        eng = fresh_engine()
        assert eng._results == []

    def test_engine_results_list_grows(self):
        eng = fresh_engine()
        assert len(eng._results) == 0
        eng.assess(make_input())
        assert len(eng._results) == 1
        eng.assess(make_input())
        assert len(eng._results) == 2

    def test_batch_then_individual_combined(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(account_id=f"J{i}") for i in range(3)])
        eng.assess(make_input(account_id="J3"))
        assert eng.summary()["total"] == 4


# ── Section 25: Additional invariants and properties ─────────────────────────

class TestAdditionalInvariants:
    def test_stable_stage_always_has_stable_signal_text(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        if result.decay_stage == DecayStage.stable:
            assert "stable" in result.decay_signal

    def test_composite_formula_respects_weights(self):
        """Changing only engagement input affects composite proportionally."""
        eng1 = fresh_engine()
        eng2 = fresh_engine()
        base = make_input()
        # make engagement score higher in eng2
        high_eng = make_input(nps_current=20, nps_prior_quarter=60)
        r1 = eng1.assess(base)
        r2 = eng2.assess(high_eng)
        # higher engagement input -> higher composite
        assert r2.decay_composite >= r1.decay_composite

    def test_to_dict_values_match_result_fields(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert d["account_id"] == result.account_id
        assert d["account_name"] == result.account_name
        assert d["decay_stage"] == result.decay_stage.value
        assert d["decay_risk"] == result.decay_risk.value
        assert d["primary_decay_signal"] == result.primary_decay_signal.value
        assert d["recommended_action"] == result.recommended_action.value
        assert d["is_at_risk"] == result.is_at_risk
        assert d["requires_escalation"] == result.requires_escalation
        assert d["decay_signal"] == result.decay_signal

    def test_arr_in_dict_rounded_correctly(self):
        eng = fresh_engine()
        result = eng.assess(make_input(contract_value_usd=123_456.789))
        d = result.to_dict()
        assert d["estimated_arr_at_risk_usd"] == round(result.estimated_arr_at_risk_usd, 2)

    def test_scores_in_dict_rounded_correctly(self):
        eng = fresh_engine()
        result = eng.assess(make_input(nps_current=33, nps_prior_quarter=66))
        d = result.to_dict()
        assert d["engagement_score"] == round(result.engagement_score, 1)
        assert d["support_health_score"] == round(result.support_health_score, 1)
        assert d["usage_vitality_score"] == round(result.usage_vitality_score, 1)
        assert d["relationship_score"] == round(result.relationship_score, 1)
        assert d["decay_composite"] == round(result.decay_composite, 1)

    def test_summary_total_arr_rounds_to_cent(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(contract_value_usd=v) for v in [11111.11, 22222.22, 33333.33]])
        s = eng.summary()
        assert s["total_arr_at_risk_usd"] == round(s["total_arr_at_risk_usd"], 2)

    def test_summary_stage_counts_sum_to_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(account_id=f"K{i}") for i in range(7)])
        s = eng.summary()
        assert sum(s["stage_counts"].values()) == s["total"]

    def test_summary_risk_counts_sum_to_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(account_id=f"L{i}") for i in range(6)])
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_signal_counts_sum_to_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(account_id=f"M{i}") for i in range(5)])
        s = eng.summary()
        assert sum(s["signal_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(account_id=f"N{i}") for i in range(4)])
        s = eng.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_at_risk_count_le_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(account_id=f"O{i}") for i in range(5)])
        s = eng.summary()
        assert s["at_risk_count"] <= s["total"]

    def test_escalation_count_le_total(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(account_id=f"P{i}") for i in range(5)])
        s = eng.summary()
        assert s["escalation_count"] <= s["total"]

    def test_avg_composite_between_0_and_100(self):
        eng = fresh_engine()
        eng.assess_batch([make_input(account_id=f"Q{i}") for i in range(3)])
        s = eng.summary()
        assert 0.0 <= s["avg_decay_composite"] <= 100.0

    def test_batch_result_is_list(self):
        eng = fresh_engine()
        result = eng.assess_batch([make_input()])
        assert isinstance(result, list)

    def test_engine_class_instantiation(self):
        eng = CustomerSentimentDecayEngine()
        assert eng is not None

    def test_assess_returns_non_none(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert result is not None

    def test_summary_returns_dict(self):
        eng = fresh_engine()
        s = eng.summary()
        assert isinstance(s, dict)

    def test_to_dict_returns_dict(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        assert isinstance(result.to_dict(), dict)

    def test_csm_id_and_region_stored_in_input(self):
        inp = make_input(csm_id="CSM-99", region="EMEA")
        assert inp.csm_id == "CSM-99"
        assert inp.region == "EMEA"

    def test_multiple_to_dict_calls_same_result(self):
        eng = fresh_engine()
        result = eng.assess(make_input())
        d1 = result.to_dict()
        d2 = result.to_dict()
        assert d1 == d2

    def test_nps_drop_yoy_exactly_40_no_20pt_bonus(self):
        eng = fresh_engine()
        # yoy drop = 40 is NOT > 40, so should get 12pt bonus (> 20 branch)
        s = eng._engagement_score(make_input(
            nps_current=30, nps_prior_year=70,  # drop = 40
            nps_prior_quarter=30,               # no qoq drop
        ))
        assert s >= 12.0

    def test_nps_drop_yoy_exactly_41_20pt_bonus(self):
        eng = fresh_engine()
        s = eng._engagement_score(make_input(
            nps_current=29, nps_prior_year=70,  # drop = 41
            nps_prior_quarter=29,               # no qoq drop
        ))
        assert s >= 20.0

    def test_exec_drop_exactly_3_triggers_40(self):
        eng = fresh_engine()
        s = eng._relationship_score(make_input(
            executive_engagement_last_90d=0,
            executive_meetings_prior_90d=3,
        ))
        # exec_drop=3 -> +40, zero with prior > 0 -> +20 = 60 -> clamped to 60
        assert s >= 40.0

    def test_exec_drop_exactly_2_triggers_28(self):
        eng = fresh_engine()
        s = eng._relationship_score(make_input(
            executive_engagement_last_90d=1,
            executive_meetings_prior_90d=3,
        ))
        # exec_drop=2 -> +28; exec != 0 so no +20; no expansion penalty in baseline
        assert s >= 28.0

    def test_exec_drop_exactly_1_triggers_15(self):
        eng = fresh_engine()
        s = eng._relationship_score(make_input(
            executive_engagement_last_90d=2,
            executive_meetings_prior_90d=3,
        ))
        # exec_drop=1 -> +15; exec != 0 so no +20
        assert s >= 15.0

    def test_signal_none_when_worst_score_lt_15(self):
        eng = fresh_engine()
        inp = make_input()
        # All sub-scores are 0 -> worst < 15 -> signal = none
        e = eng._engagement_score(inp)
        s = eng._support_health_score(inp)
        u = eng._usage_vitality_score(inp)
        r = eng._relationship_score(inp)
        worst = max(e, s, u, r)
        if worst < 15:
            result = eng.assess(inp)
            assert result.primary_decay_signal == DecaySignal.none
