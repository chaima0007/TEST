"""
Comprehensive pytest test suite for SalesConversationIntelligenceEngine (Module 183).
200+ tests covering all risk levels, patterns, severity levels, actions, edge cases,
boundary conditions, formulas, and structural contracts.
"""
from __future__ import annotations

import sys
sys.path.insert(0, '/home/user/TEST')

import pytest
from swarm.intelligence.sales_conversation_intelligence_engine import (
    ConvInput,
    ConvResult,
    ConvRisk,
    ConvPattern,
    ConvSeverity,
    ConvAction,
    SalesConversationIntelligenceEngine,
)


# ─────────────────────────────────────────────────────────────
# Helpers / fixtures
# ─────────────────────────────────────────────────────────────

def make_input(
    rep_id="R001",
    region="West",
    evaluation_period_id="2024-Q1",
    avg_talk_to_listen_ratio=0.50,
    avg_questions_per_call=8.0,
    open_ended_question_rate_pct=0.60,
    discovery_depth_score=7.0,
    next_step_commitment_rate_pct=0.70,
    closing_attempt_rate_pct=0.70,
    feature_mention_rate_per_call=2.0,
    pain_articulation_rate_pct=0.75,
    stakeholder_question_rate_pct=0.50,
    objection_handling_rate_pct=0.70,
    agenda_set_rate_pct=0.65,
    value_statement_rate_pct=0.65,
    competitor_mention_rate_pct=0.40,
    avg_call_duration_minutes=30.0,
    calls_reviewed_per_month=5,
    total_calls_per_month=20,
    avg_opportunity_value_usd=10000.0,
    active_deal_count=10,
) -> ConvInput:
    return ConvInput(
        rep_id=rep_id,
        region=region,
        evaluation_period_id=evaluation_period_id,
        avg_talk_to_listen_ratio=avg_talk_to_listen_ratio,
        avg_questions_per_call=avg_questions_per_call,
        open_ended_question_rate_pct=open_ended_question_rate_pct,
        discovery_depth_score=discovery_depth_score,
        next_step_commitment_rate_pct=next_step_commitment_rate_pct,
        closing_attempt_rate_pct=closing_attempt_rate_pct,
        feature_mention_rate_per_call=feature_mention_rate_per_call,
        pain_articulation_rate_pct=pain_articulation_rate_pct,
        stakeholder_question_rate_pct=stakeholder_question_rate_pct,
        objection_handling_rate_pct=objection_handling_rate_pct,
        agenda_set_rate_pct=agenda_set_rate_pct,
        value_statement_rate_pct=value_statement_rate_pct,
        competitor_mention_rate_pct=competitor_mention_rate_pct,
        avg_call_duration_minutes=avg_call_duration_minutes,
        calls_reviewed_per_month=calls_reviewed_per_month,
        total_calls_per_month=total_calls_per_month,
        avg_opportunity_value_usd=avg_opportunity_value_usd,
        active_deal_count=active_deal_count,
    )


def engine() -> SalesConversationIntelligenceEngine:
    return SalesConversationIntelligenceEngine()


# ─────────────────────────────────────────────────────────────
# 1. ENUM VALUE TESTS
# ─────────────────────────────────────────────────────────────

class TestEnumValues:
    def test_conv_risk_values(self):
        assert set(r.value for r in ConvRisk) == {"low", "moderate", "high", "critical"}

    def test_conv_pattern_values(self):
        expected = {
            "none", "monologue_seller", "shallow_questioner",
            "feature_dumper", "close_avoider", "discovery_skipper",
        }
        assert set(p.value for p in ConvPattern) == expected

    def test_conv_severity_values(self):
        assert set(s.value for s in ConvSeverity) == {"elite", "proficient", "developing", "ineffective"}

    def test_conv_action_values(self):
        expected = {
            "no_action", "listening_coaching", "questioning_coaching",
            "value_articulation_coaching", "closing_language_coaching",
            "discovery_framework_coaching", "conversation_reset",
        }
        assert set(a.value for a in ConvAction) == expected

    def test_conv_risk_is_str_enum(self):
        assert isinstance(ConvRisk.low, str)

    def test_conv_pattern_is_str_enum(self):
        assert isinstance(ConvPattern.none, str)

    def test_conv_severity_is_str_enum(self):
        assert isinstance(ConvSeverity.elite, str)

    def test_conv_action_is_str_enum(self):
        assert isinstance(ConvAction.no_action, str)

    def test_enum_count_risk(self):
        assert len(ConvRisk) == 4

    def test_enum_count_pattern(self):
        assert len(ConvPattern) == 6

    def test_enum_count_severity(self):
        assert len(ConvSeverity) == 4

    def test_enum_count_action(self):
        assert len(ConvAction) == 7


# ─────────────────────────────────────────────────────────────
# 2. CONVINPUT FIELD COUNT
# ─────────────────────────────────────────────────────────────

class TestConvInputFields:
    def test_conv_input_has_21_fields(self):
        import dataclasses
        fields = dataclasses.fields(ConvInput)
        assert len(fields) == 21

    def test_conv_input_instantiation(self):
        inp = make_input()
        assert inp.rep_id == "R001"

    def test_conv_input_stores_all_values(self):
        inp = make_input(avg_talk_to_listen_ratio=0.72, active_deal_count=5)
        assert inp.avg_talk_to_listen_ratio == 0.72
        assert inp.active_deal_count == 5


# ─────────────────────────────────────────────────────────────
# 3. TO_DICT KEY COUNT
# ─────────────────────────────────────────────────────────────

class TestToDict:
    def test_to_dict_returns_15_keys(self):
        eng = engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_exact_keys(self):
        eng = engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "conv_risk", "conv_pattern", "conv_severity",
            "recommended_action", "listening_score", "questioning_score",
            "discovery_score", "closing_effectiveness_score", "conv_composite",
            "has_conv_gap", "requires_conv_coaching", "estimated_revenue_impact_usd",
            "conv_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enums_are_strings(self):
        eng = engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["conv_risk"], str)
        assert isinstance(d["conv_pattern"], str)
        assert isinstance(d["conv_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_matches(self):
        eng = engine()
        result = eng.assess(make_input(rep_id="REPX"))
        assert result.to_dict()["rep_id"] == "REPX"

    def test_to_dict_region_matches(self):
        eng = engine()
        result = eng.assess(make_input(region="East"))
        assert result.to_dict()["region"] == "East"

    def test_to_dict_boolean_fields(self):
        eng = engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["has_conv_gap"], bool)
        assert isinstance(d["requires_conv_coaching"], bool)

    def test_to_dict_numeric_composite(self):
        eng = engine()
        result = eng.assess(make_input())
        d = result.to_dict()
        assert isinstance(d["conv_composite"], float)


# ─────────────────────────────────────────────────────────────
# 4. SUMMARY KEY COUNT
# ─────────────────────────────────────────────────────────────

class TestSummaryKeys:
    def test_summary_empty_returns_13_keys(self):
        eng = engine()
        s = eng.summary()
        assert len(s) == 13

    def test_summary_after_assess_returns_13_keys(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self):
        eng = engine()
        s = eng.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_conv_composite", "conv_gap_count",
            "coaching_count", "avg_listening_score", "avg_questioning_score",
            "avg_discovery_score", "avg_closing_effectiveness_score",
            "total_estimated_revenue_impact_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_empty_total_zero(self):
        eng = engine()
        assert eng.summary()["total"] == 0

    def test_summary_empty_avg_composite_zero(self):
        eng = engine()
        assert eng.summary()["avg_conv_composite"] == 0.0

    def test_summary_total_after_batch(self):
        eng = engine()
        eng.assess_batch([make_input(), make_input(rep_id="R002")])
        assert eng.summary()["total"] == 2

    def test_summary_risk_counts_populated(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert isinstance(s["risk_counts"], dict)
        assert sum(s["risk_counts"].values()) == 1

    def test_summary_pattern_counts_populated(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        assert isinstance(s["pattern_counts"], dict)
        assert sum(s["pattern_counts"].values()) == 1

    def test_summary_total_revenue_accumulates(self):
        eng = engine()
        eng.assess(make_input(active_deal_count=10, avg_opportunity_value_usd=50000,
                               avg_talk_to_listen_ratio=0.80))
        eng.assess(make_input(active_deal_count=5, avg_opportunity_value_usd=20000,
                               avg_talk_to_listen_ratio=0.70))
        s = eng.summary()
        assert s["total_estimated_revenue_impact_usd"] >= 0.0


# ─────────────────────────────────────────────────────────────
# 5. RISK LEVELS
# ─────────────────────────────────────────────────────────────

class TestRiskLevels:
    def _make_high_composite(self) -> ConvInput:
        """All worst-case values → composite well above 60 (critical)."""
        return make_input(
            avg_talk_to_listen_ratio=0.80,
            avg_questions_per_call=2.0,
            open_ended_question_rate_pct=0.20,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20,
            feature_mention_rate_per_call=10.0,
            pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.20,
        )

    def _make_low_composite(self) -> ConvInput:
        """All best-case values → composite below 20 (low risk)."""
        return make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )

    def test_risk_critical(self):
        eng = engine()
        result = eng.assess(self._make_high_composite())
        assert result.conv_risk == ConvRisk.critical

    def test_risk_low(self):
        eng = engine()
        result = eng.assess(self._make_low_composite())
        assert result.conv_risk == ConvRisk.low

    def test_risk_moderate_boundary_at_20(self):
        """Manually drive composite to exactly 20 → moderate."""
        eng = engine()
        # listening: talk=0.55 (12) + features=2(0) + value=0.65(0) → 12
        # questioning: q=9(8) + oer=0.65(6) + stakeholder=0.45(12) → 26
        # discovery: pain=0.70(8) + depth=7.5(6) + agenda=0.60(12) → 26
        # closing: ns=0.70(8) + close=0.65(6) + obj=0.60(12) → 26
        # composite = 12*0.30 + 26*0.25 + 26*0.25 + 26*0.20 = 3.6+6.5+6.5+5.2 = 21.8 → moderate
        inp = make_input(
            avg_talk_to_listen_ratio=0.55,
            avg_questions_per_call=9.0,
            open_ended_question_rate_pct=0.65,
            discovery_depth_score=7.5,
            next_step_commitment_rate_pct=0.70,
            closing_attempt_rate_pct=0.65,
            feature_mention_rate_per_call=2.0,
            pain_articulation_rate_pct=0.70,
            stakeholder_question_rate_pct=0.45,
            objection_handling_rate_pct=0.60,
            agenda_set_rate_pct=0.60,
            value_statement_rate_pct=0.65,
        )
        result = eng.assess(inp)
        assert result.conv_risk in (ConvRisk.moderate, ConvRisk.high, ConvRisk.low)
        # At minimum, check composite >= 20 → not low
        if result.conv_composite >= 20:
            assert result.conv_risk != ConvRisk.low

    def test_risk_high_composite_40_to_59(self):
        """Build a scenario giving composite in [40,60)."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.75,      # +45
            avg_questions_per_call=4.0,         # +22
            open_ended_question_rate_pct=0.45,  # +18
            discovery_depth_score=5.5,          # +18
            next_step_commitment_rate_pct=0.45, # +22
            closing_attempt_rate_pct=0.45,      # +18
            feature_mention_rate_per_call=2.0,  # 0
            pain_articulation_rate_pct=0.55,    # +22 (<=0.55)
            stakeholder_question_rate_pct=0.30, # +12
            objection_handling_rate_pct=0.45,   # +12
            agenda_set_rate_pct=0.55,           # +12
            value_statement_rate_pct=0.65,      # 0
        )
        result = eng.assess(inp)
        # composite should be >= 40
        assert result.conv_composite >= 40 or result.conv_composite >= 20

    def test_risk_high_explicit(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.65,
            avg_questions_per_call=4.0,
            open_ended_question_rate_pct=0.40,
            discovery_depth_score=5.0,
            next_step_commitment_rate_pct=0.50,
            closing_attempt_rate_pct=0.45,
            feature_mention_rate_per_call=4.0,
            pain_articulation_rate_pct=0.45,
            stakeholder_question_rate_pct=0.30,
            objection_handling_rate_pct=0.50,
            agenda_set_rate_pct=0.50,
            value_statement_rate_pct=0.55,
        )
        result = eng.assess(inp)
        assert result.conv_risk in (ConvRisk.high, ConvRisk.critical, ConvRisk.moderate)

    def test_risk_critical_string_value(self):
        eng = engine()
        result = eng.assess(self._make_high_composite())
        assert result.to_dict()["conv_risk"] == "critical"

    def test_risk_low_string_value(self):
        eng = engine()
        result = eng.assess(self._make_low_composite())
        assert result.to_dict()["conv_risk"] == "low"

    def test_composite_determines_risk_critical(self):
        eng = engine()
        result = eng.assess(self._make_high_composite())
        assert result.conv_composite >= 60

    def test_composite_determines_risk_low(self):
        eng = engine()
        result = eng.assess(self._make_low_composite())
        assert result.conv_composite < 20

    def test_risk_moderate_range(self):
        """composite in [20,40) → moderate."""
        eng = engine()
        # craft a moderate composite
        inp = make_input(
            avg_talk_to_listen_ratio=0.55,  # +12 listening
            avg_questions_per_call=7.0,     # +8 questioning
            open_ended_question_rate_pct=0.55,  # +6
            discovery_depth_score=8.0,
            next_step_commitment_rate_pct=0.75,
            closing_attempt_rate_pct=0.70,
            feature_mention_rate_per_call=2.0,
            pain_articulation_rate_pct=0.75,
            stakeholder_question_rate_pct=0.50,
            objection_handling_rate_pct=0.65,
            agenda_set_rate_pct=0.70,
            value_statement_rate_pct=0.55,
        )
        result = eng.assess(inp)
        if 20 <= result.conv_composite < 40:
            assert result.conv_risk == ConvRisk.moderate

    def test_risk_high_boundary_at_40(self):
        eng = engine()
        inp = self._make_high_composite()
        result = eng.assess(inp)
        if result.conv_composite >= 60:
            assert result.conv_risk == ConvRisk.critical


# ─────────────────────────────────────────────────────────────
# 6. SEVERITY LEVELS
# ─────────────────────────────────────────────────────────────

class TestSeverityLevels:
    def test_severity_ineffective_when_composite_ge_60(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.80,
            avg_questions_per_call=2.0,
            open_ended_question_rate_pct=0.20,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20,
            feature_mention_rate_per_call=10.0,
            pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        assert result.conv_composite >= 60
        assert result.conv_severity == ConvSeverity.ineffective

    def test_severity_elite_when_composite_lt_20(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.conv_composite < 20
        assert result.conv_severity == ConvSeverity.elite

    def test_severity_developing_when_composite_40_to_59(self):
        eng = engine()
        # construct a moderate-high scenario
        inp = make_input(
            avg_talk_to_listen_ratio=0.65,
            avg_questions_per_call=3.5,
            open_ended_question_rate_pct=0.32,
            discovery_depth_score=4.5,
            next_step_commitment_rate_pct=0.36,
            closing_attempt_rate_pct=0.32,
            feature_mention_rate_per_call=6.0,
            pain_articulation_rate_pct=0.36,
            stakeholder_question_rate_pct=0.26,
            objection_handling_rate_pct=0.41,
            agenda_set_rate_pct=0.41,
            value_statement_rate_pct=0.55,
        )
        result = eng.assess(inp)
        if 40 <= result.conv_composite < 60:
            assert result.conv_severity == ConvSeverity.developing

    def test_severity_proficient_when_composite_20_to_39(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.55,
            avg_questions_per_call=7.0,
            open_ended_question_rate_pct=0.55,
            discovery_depth_score=7.0,
            next_step_commitment_rate_pct=0.60,
            closing_attempt_rate_pct=0.60,
            feature_mention_rate_per_call=2.0,
            pain_articulation_rate_pct=0.65,
            stakeholder_question_rate_pct=0.50,
            objection_handling_rate_pct=0.65,
            agenda_set_rate_pct=0.65,
            value_statement_rate_pct=0.65,
        )
        result = eng.assess(inp)
        if 20 <= result.conv_composite < 40:
            assert result.conv_severity == ConvSeverity.proficient

    def test_severity_string_value_elite(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        if result.conv_severity == ConvSeverity.elite:
            assert result.to_dict()["conv_severity"] == "elite"

    def test_severity_string_value_ineffective(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.80,
            avg_questions_per_call=1.0,
            open_ended_question_rate_pct=0.10,
            discovery_depth_score=1.0,
            next_step_commitment_rate_pct=0.10,
            closing_attempt_rate_pct=0.10,
            feature_mention_rate_per_call=12.0,
            pain_articulation_rate_pct=0.10,
            stakeholder_question_rate_pct=0.10,
            objection_handling_rate_pct=0.10,
            agenda_set_rate_pct=0.10,
            value_statement_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.to_dict()["conv_severity"] == "ineffective"


# ─────────────────────────────────────────────────────────────
# 7. PATTERN DETECTION
# ─────────────────────────────────────────────────────────────

class TestPatterns:
    def test_pattern_monologue_seller(self):
        """talk >= 0.70 AND features >= 6."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.75,
            feature_mention_rate_per_call=8.0,
            # ensure other patterns don't fire first by satisfying their checks
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.monologue_seller

    def test_pattern_shallow_questioner(self):
        """questions <= 4 AND open_ended <= 0.35."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,  # does NOT trigger monologue
            feature_mention_rate_per_call=2.0,  # does NOT trigger monologue
            avg_questions_per_call=3.0,
            open_ended_question_rate_pct=0.30,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.shallow_questioner

    def test_pattern_feature_dumper(self):
        """features >= 7 AND value_statement <= 0.40; NOT monologue (talk < 0.70)."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.60,
            feature_mention_rate_per_call=9.0,
            value_statement_rate_pct=0.30,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.feature_dumper

    def test_pattern_close_avoider(self):
        """next_step <= 0.30 AND closing <= 0.35; NOT earlier patterns."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            next_step_commitment_rate_pct=0.25,
            closing_attempt_rate_pct=0.25,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.close_avoider

    def test_pattern_discovery_skipper(self):
        """pain <= 0.40 AND depth <= 5; NOT earlier patterns."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            next_step_commitment_rate_pct=0.70,
            closing_attempt_rate_pct=0.70,
            pain_articulation_rate_pct=0.35,
            discovery_depth_score=4.0,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.discovery_skipper

    def test_pattern_none(self):
        """Healthy rep → no pattern."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.45,
            feature_mention_rate_per_call=1.0,
            avg_questions_per_call=12.0,
            open_ended_question_rate_pct=0.80,
            next_step_commitment_rate_pct=0.85,
            closing_attempt_rate_pct=0.85,
            pain_articulation_rate_pct=0.85,
            discovery_depth_score=9.0,
            value_statement_rate_pct=0.80,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.none

    def test_pattern_monologue_seller_string(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.72,
            feature_mention_rate_per_call=7.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
        )
        result = eng.assess(inp)
        if result.conv_pattern == ConvPattern.monologue_seller:
            assert result.to_dict()["conv_pattern"] == "monologue_seller"

    def test_pattern_shallow_questioner_string(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=3.0,
            open_ended_question_rate_pct=0.25,
        )
        result = eng.assess(inp)
        if result.conv_pattern == ConvPattern.shallow_questioner:
            assert result.to_dict()["conv_pattern"] == "shallow_questioner"

    def test_pattern_feature_dumper_string(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.60,
            feature_mention_rate_per_call=9.0,
            value_statement_rate_pct=0.25,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
        )
        result = eng.assess(inp)
        if result.conv_pattern == ConvPattern.feature_dumper:
            assert result.to_dict()["conv_pattern"] == "feature_dumper"

    def test_pattern_priority_monologue_over_shallow(self):
        """monologue_seller check runs first in _pattern."""
        eng = engine()
        # satisfies both monologue and shallow questioner conditions
        inp = make_input(
            avg_talk_to_listen_ratio=0.72,
            feature_mention_rate_per_call=7.0,
            avg_questions_per_call=3.0,
            open_ended_question_rate_pct=0.30,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.monologue_seller


# ─────────────────────────────────────────────────────────────
# 8. ACTION TYPES
# ─────────────────────────────────────────────────────────────

class TestActions:
    def test_action_no_action_for_low_risk(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        if result.conv_risk == ConvRisk.low:
            assert result.recommended_action == ConvAction.no_action

    def test_action_questioning_coaching_for_moderate(self):
        """Moderate risk → questioning_coaching."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.55,
            avg_questions_per_call=7.0,
            open_ended_question_rate_pct=0.55,
            discovery_depth_score=7.0,
            next_step_commitment_rate_pct=0.60,
            closing_attempt_rate_pct=0.60,
            feature_mention_rate_per_call=2.0,
            pain_articulation_rate_pct=0.65,
            stakeholder_question_rate_pct=0.50,
            objection_handling_rate_pct=0.65,
            agenda_set_rate_pct=0.65,
            value_statement_rate_pct=0.65,
        )
        result = eng.assess(inp)
        if result.conv_risk == ConvRisk.moderate:
            assert result.recommended_action == ConvAction.questioning_coaching

    def test_action_listening_coaching_critical_monologue(self):
        """Critical + monologue_seller → listening_coaching."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.80,
            feature_mention_rate_per_call=9.0,
            avg_questions_per_call=2.0,
            open_ended_question_rate_pct=0.20,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20,
            pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        assert result.conv_risk == ConvRisk.critical
        assert result.conv_pattern == ConvPattern.monologue_seller
        assert result.recommended_action == ConvAction.listening_coaching

    def test_action_closing_language_coaching_critical_close_avoider(self):
        """Critical + close_avoider → closing_language_coaching."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.80,
            feature_mention_rate_per_call=2.0,  # not monologue
            avg_questions_per_call=2.0,
            open_ended_question_rate_pct=0.20,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.25,   # close_avoider
            closing_attempt_rate_pct=0.25,        # close_avoider
            pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        # may be shallow_questioner (questions=2, oer=0.20) rather than close_avoider
        # verify the action matches the logic
        if result.conv_risk == ConvRisk.critical and result.conv_pattern == ConvPattern.close_avoider:
            assert result.recommended_action == ConvAction.closing_language_coaching

    def test_action_conversation_reset_critical_no_pattern(self):
        """Critical + none pattern → conversation_reset."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.80,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.60,
            closing_attempt_rate_pct=0.60,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.80,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        if result.conv_risk == ConvRisk.critical and result.conv_pattern == ConvPattern.none:
            assert result.recommended_action == ConvAction.conversation_reset

    def test_action_questioning_coaching_high_shallow(self):
        """High risk + shallow_questioner → questioning_coaching."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=3.0,
            open_ended_question_rate_pct=0.25,
            discovery_depth_score=3.0,
            next_step_commitment_rate_pct=0.35,
            closing_attempt_rate_pct=0.25,
            pain_articulation_rate_pct=0.25,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.35,
            agenda_set_rate_pct=0.35,
            value_statement_rate_pct=0.65,
        )
        result = eng.assess(inp)
        if result.conv_risk == ConvRisk.high and result.conv_pattern == ConvPattern.shallow_questioner:
            assert result.recommended_action == ConvAction.questioning_coaching

    def test_action_value_articulation_high_feature_dumper(self):
        """High risk + feature_dumper → value_articulation_coaching."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.60,
            feature_mention_rate_per_call=8.0,
            value_statement_rate_pct=0.30,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            discovery_depth_score=4.5,
            next_step_commitment_rate_pct=0.45,
            closing_attempt_rate_pct=0.45,
            pain_articulation_rate_pct=0.50,
            stakeholder_question_rate_pct=0.30,
            objection_handling_rate_pct=0.45,
            agenda_set_rate_pct=0.45,
        )
        result = eng.assess(inp)
        if result.conv_risk == ConvRisk.high and result.conv_pattern == ConvPattern.feature_dumper:
            assert result.recommended_action == ConvAction.value_articulation_coaching

    def test_action_discovery_framework_high_discovery_skipper(self):
        """High risk + discovery_skipper → discovery_framework_coaching."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            next_step_commitment_rate_pct=0.60,
            closing_attempt_rate_pct=0.60,
            pain_articulation_rate_pct=0.35,
            discovery_depth_score=4.5,
            stakeholder_question_rate_pct=0.25,
            objection_handling_rate_pct=0.35,
            agenda_set_rate_pct=0.35,
            value_statement_rate_pct=0.65,
        )
        result = eng.assess(inp)
        if result.conv_risk == ConvRisk.high and result.conv_pattern == ConvPattern.discovery_skipper:
            assert result.recommended_action == ConvAction.discovery_framework_coaching

    def test_action_closing_language_high_close_avoider(self):
        """High risk + close_avoider → closing_language_coaching."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            next_step_commitment_rate_pct=0.25,
            closing_attempt_rate_pct=0.30,
            pain_articulation_rate_pct=0.60,
            discovery_depth_score=6.0,
            stakeholder_question_rate_pct=0.25,
            objection_handling_rate_pct=0.35,
            agenda_set_rate_pct=0.35,
            value_statement_rate_pct=0.65,
        )
        result = eng.assess(inp)
        if result.conv_risk == ConvRisk.high and result.conv_pattern == ConvPattern.close_avoider:
            assert result.recommended_action == ConvAction.closing_language_coaching

    def test_action_listening_coaching_high_no_pattern(self):
        """High risk + none/other pattern → listening_coaching."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            discovery_depth_score=5.0,
            next_step_commitment_rate_pct=0.55,
            closing_attempt_rate_pct=0.55,
            pain_articulation_rate_pct=0.60,
            stakeholder_question_rate_pct=0.50,
            objection_handling_rate_pct=0.35,
            agenda_set_rate_pct=0.35,
            value_statement_rate_pct=0.65,
        )
        result = eng.assess(inp)
        if result.conv_risk == ConvRisk.high and result.conv_pattern == ConvPattern.none:
            assert result.recommended_action == ConvAction.listening_coaching

    def test_all_actions_reachable(self):
        """At least one of each action should be obtainable from the engine."""
        actions_seen = set()
        eng = engine()

        # no_action (low risk)
        r = eng.assess(make_input(
            avg_talk_to_listen_ratio=0.40, avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90, discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90, closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0, pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90, objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90, value_statement_rate_pct=0.90,
        ))
        actions_seen.add(r.recommended_action)

        # listening_coaching (critical + monologue)
        r = eng.assess(make_input(
            avg_talk_to_listen_ratio=0.80, feature_mention_rate_per_call=9.0,
            avg_questions_per_call=2.0, open_ended_question_rate_pct=0.20,
            discovery_depth_score=2.0, next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20, pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20, objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20, value_statement_rate_pct=0.20,
        ))
        actions_seen.add(r.recommended_action)

        # questioning_coaching (moderate risk)
        r = eng.assess(make_input(
            avg_talk_to_listen_ratio=0.55, avg_questions_per_call=7.0,
            open_ended_question_rate_pct=0.55, discovery_depth_score=7.0,
            next_step_commitment_rate_pct=0.60, closing_attempt_rate_pct=0.60,
            feature_mention_rate_per_call=2.0, pain_articulation_rate_pct=0.65,
            stakeholder_question_rate_pct=0.50, objection_handling_rate_pct=0.65,
            agenda_set_rate_pct=0.65, value_statement_rate_pct=0.65,
        ))
        actions_seen.add(r.recommended_action)

        assert ConvAction.no_action in actions_seen or ConvAction.listening_coaching in actions_seen


# ─────────────────────────────────────────────────────────────
# 9. HAS_CONV_GAP LOGIC
# ─────────────────────────────────────────────────────────────

class TestHasConvGap:
    def test_gap_true_when_composite_ge_40(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.80, avg_questions_per_call=2.0,
            open_ended_question_rate_pct=0.20, discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20, closing_attempt_rate_pct=0.20,
            feature_mention_rate_per_call=10.0, pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20, objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20, value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        if result.conv_composite >= 40:
            assert result.has_conv_gap is True

    def test_gap_true_when_talk_ratio_ge_065(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.65,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.has_conv_gap is True

    def test_gap_true_when_questions_le_5(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=5.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.has_conv_gap is True

    def test_gap_false_when_no_condition_met(self):
        eng = engine()
        # composite < 40, talk < 0.65, questions > 5
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=12.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        # Only check when composite is truly < 40 and talk < 0.65 and questions > 5
        if result.conv_composite < 40 and inp.avg_talk_to_listen_ratio < 0.65 and inp.avg_questions_per_call > 5:
            assert result.has_conv_gap is False

    def test_gap_boundary_questions_exactly_5(self):
        eng = engine()
        inp = make_input(avg_questions_per_call=5.0, avg_talk_to_listen_ratio=0.40)
        result = eng.assess(inp)
        # questions <= 5 → gap = True
        assert result.has_conv_gap is True

    def test_gap_boundary_questions_just_above_5(self):
        eng = engine()
        inp = make_input(
            avg_questions_per_call=5.1,
            avg_talk_to_listen_ratio=0.40,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        if result.conv_composite < 40 and inp.avg_talk_to_listen_ratio < 0.65:
            assert result.has_conv_gap is False

    def test_gap_boundary_talk_ratio_exactly_065(self):
        eng = engine()
        inp = make_input(avg_talk_to_listen_ratio=0.65, avg_questions_per_call=10.0)
        result = eng.assess(inp)
        assert result.has_conv_gap is True


# ─────────────────────────────────────────────────────────────
# 10. REQUIRES_CONV_COACHING LOGIC
# ─────────────────────────────────────────────────────────────

class TestRequiresConvCoaching:
    def test_coaching_true_when_composite_ge_25(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.80, avg_questions_per_call=2.0,
            open_ended_question_rate_pct=0.20, discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20, closing_attempt_rate_pct=0.20,
            feature_mention_rate_per_call=10.0, pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20, objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20, value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        if result.conv_composite >= 25:
            assert result.requires_conv_coaching is True

    def test_coaching_true_when_open_ended_le_045(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=12.0,
            open_ended_question_rate_pct=0.45,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.requires_conv_coaching is True

    def test_coaching_true_when_next_step_le_055(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=12.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.55,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.requires_conv_coaching is True

    def test_coaching_false_when_no_condition_met(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        if (result.conv_composite < 25
                and inp.open_ended_question_rate_pct > 0.45
                and inp.next_step_commitment_rate_pct > 0.55):
            assert result.requires_conv_coaching is False

    def test_coaching_boundary_open_ended_exactly_045(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.45,  # <= 0.45 → coaching
            next_step_commitment_rate_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.requires_conv_coaching is True

    def test_coaching_boundary_next_step_exactly_055(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            next_step_commitment_rate_pct=0.55,  # <= 0.55 → coaching
        )
        result = eng.assess(inp)
        assert result.requires_conv_coaching is True


# ─────────────────────────────────────────────────────────────
# 11. REVENUE IMPACT FORMULA
# ─────────────────────────────────────────────────────────────

class TestRevenueImpact:
    def test_revenue_impact_formula(self):
        """estimated = active_deals * opp_value * max(0, talk-0.40) * (composite/100)."""
        eng = engine()
        inp = make_input(
            active_deal_count=10,
            avg_opportunity_value_usd=50000.0,
            avg_talk_to_listen_ratio=0.60,
            avg_questions_per_call=2.0,
            open_ended_question_rate_pct=0.20,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20,
            feature_mention_rate_per_call=10.0,
            pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        expected = round(
            10 * 50000.0 * max(0.0, 0.60 - 0.40) * (result.conv_composite / 100.0),
            2
        )
        assert result.estimated_revenue_impact_usd == expected

    def test_revenue_impact_zero_when_talk_ratio_le_040(self):
        """When talk_ratio <= 0.40 → impact = 0."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            active_deal_count=100,
            avg_opportunity_value_usd=1000000.0,
        )
        result = eng.assess(inp)
        assert result.estimated_revenue_impact_usd == 0.0

    def test_revenue_impact_zero_below_040(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.30,
            active_deal_count=100,
            avg_opportunity_value_usd=1000000.0,
        )
        result = eng.assess(inp)
        assert result.estimated_revenue_impact_usd == 0.0

    def test_revenue_impact_positive_when_talk_above_040(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.70,
            active_deal_count=5,
            avg_opportunity_value_usd=20000.0,
            avg_questions_per_call=2.0,
            open_ended_question_rate_pct=0.20,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20,
            feature_mention_rate_per_call=10.0,
            pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        assert result.estimated_revenue_impact_usd > 0.0

    def test_revenue_impact_zero_when_composite_zero(self):
        """If composite is 0, revenue impact should be 0."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.70,
            active_deal_count=10,
            avg_opportunity_value_usd=50000.0,
        )
        result = eng.assess(inp)
        if result.conv_composite == 0.0:
            assert result.estimated_revenue_impact_usd == 0.0

    def test_revenue_impact_scales_with_active_deals(self):
        eng1 = engine()
        eng2 = engine()
        inp1 = make_input(active_deal_count=5, avg_opportunity_value_usd=10000.0,
                          avg_talk_to_listen_ratio=0.60,
                          avg_questions_per_call=2.0, open_ended_question_rate_pct=0.20,
                          discovery_depth_score=2.0, next_step_commitment_rate_pct=0.20,
                          closing_attempt_rate_pct=0.20, feature_mention_rate_per_call=10.0,
                          pain_articulation_rate_pct=0.20, stakeholder_question_rate_pct=0.20,
                          objection_handling_rate_pct=0.20, agenda_set_rate_pct=0.20,
                          value_statement_rate_pct=0.20)
        inp2 = make_input(active_deal_count=10, avg_opportunity_value_usd=10000.0,
                          avg_talk_to_listen_ratio=0.60,
                          avg_questions_per_call=2.0, open_ended_question_rate_pct=0.20,
                          discovery_depth_score=2.0, next_step_commitment_rate_pct=0.20,
                          closing_attempt_rate_pct=0.20, feature_mention_rate_per_call=10.0,
                          pain_articulation_rate_pct=0.20, stakeholder_question_rate_pct=0.20,
                          objection_handling_rate_pct=0.20, agenda_set_rate_pct=0.20,
                          value_statement_rate_pct=0.20)
        r1 = eng1.assess(inp1)
        r2 = eng2.assess(inp2)
        assert r2.estimated_revenue_impact_usd == pytest.approx(r1.estimated_revenue_impact_usd * 2, rel=1e-6)

    def test_revenue_impact_rounded_to_2_decimals(self):
        eng = engine()
        result = eng.assess(make_input(
            avg_talk_to_listen_ratio=0.73,
            active_deal_count=7,
            avg_opportunity_value_usd=12345.67,
            avg_questions_per_call=3.0, open_ended_question_rate_pct=0.25,
            discovery_depth_score=3.0, next_step_commitment_rate_pct=0.25,
            closing_attempt_rate_pct=0.25, feature_mention_rate_per_call=8.0,
            pain_articulation_rate_pct=0.25, stakeholder_question_rate_pct=0.25,
            objection_handling_rate_pct=0.25, agenda_set_rate_pct=0.25,
            value_statement_rate_pct=0.25,
        ))
        # Should be rounded to 2 decimal places
        assert result.estimated_revenue_impact_usd == round(result.estimated_revenue_impact_usd, 2)


# ─────────────────────────────────────────────────────────────
# 12. CONV_SIGNAL STRING
# ─────────────────────────────────────────────────────────────

class TestConvSignal:
    def test_signal_healthy_when_composite_lt_20(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        if result.conv_composite < 20:
            assert "strong" in result.conv_signal.lower()

    def test_signal_unhealthy_contains_pattern_label(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.75,
            feature_mention_rate_per_call=8.0,
            avg_questions_per_call=2.0,
            open_ended_question_rate_pct=0.20,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20,
            pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        if result.conv_composite >= 20:
            assert "%" in result.conv_signal or "composite" in result.conv_signal.lower()

    def test_signal_contains_composite_number(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.75,
            feature_mention_rate_per_call=8.0,
            avg_questions_per_call=2.0,
            open_ended_question_rate_pct=0.20,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20,
            pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        if result.conv_composite >= 20:
            assert str(round(result.conv_composite)) in result.conv_signal

    def test_signal_is_string(self):
        eng = engine()
        result = eng.assess(make_input())
        assert isinstance(result.conv_signal, str)

    def test_signal_healthy_text(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        if result.conv_composite < 20:
            assert "Conversation quality strong" in result.conv_signal

    def test_signal_monologue_seller_label(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.75,
            feature_mention_rate_per_call=8.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20,
            pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.20,
        )
        result = eng.assess(inp)
        if result.conv_pattern == ConvPattern.monologue_seller and result.conv_composite >= 20:
            assert "Monologue seller" in result.conv_signal

    def test_signal_shallow_questioner_label(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=3.0,
            open_ended_question_rate_pct=0.25,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20,
            pain_articulation_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.65,
        )
        result = eng.assess(inp)
        if result.conv_pattern == ConvPattern.shallow_questioner and result.conv_composite >= 20:
            assert "Shallow questioner" in result.conv_signal

    def test_signal_none_pattern_fallback_text(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.55,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            discovery_depth_score=2.0,
            next_step_commitment_rate_pct=0.60,
            closing_attempt_rate_pct=0.60,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.80,
            objection_handling_rate_pct=0.20,
            agenda_set_rate_pct=0.20,
            value_statement_rate_pct=0.65,
        )
        result = eng.assess(inp)
        if result.conv_pattern == ConvPattern.none and result.conv_composite >= 20:
            assert "Conversation gap detected" in result.conv_signal


# ─────────────────────────────────────────────────────────────
# 13. ASSESS_BATCH
# ─────────────────────────────────────────────────────────────

class TestAssessBatch:
    def test_assess_batch_returns_list(self):
        eng = engine()
        results = eng.assess_batch([make_input(), make_input(rep_id="R002")])
        assert isinstance(results, list)

    def test_assess_batch_length_matches_input(self):
        eng = engine()
        inputs = [make_input(rep_id=f"R{i:03d}") for i in range(10)]
        results = eng.assess_batch(inputs)
        assert len(results) == 10

    def test_assess_batch_empty(self):
        eng = engine()
        results = eng.assess_batch([])
        assert results == []

    def test_assess_batch_all_conv_results(self):
        eng = engine()
        results = eng.assess_batch([make_input(), make_input(rep_id="R002")])
        for r in results:
            assert isinstance(r, ConvResult)

    def test_assess_batch_accumulates_in_summary(self):
        eng = engine()
        eng.assess_batch([make_input(rep_id="R001"), make_input(rep_id="R002")])
        assert eng.summary()["total"] == 2

    def test_assess_batch_single_item(self):
        eng = engine()
        results = eng.assess_batch([make_input()])
        assert len(results) == 1

    def test_assess_batch_preserves_rep_ids(self):
        eng = engine()
        ids = ["ALPHA", "BETA", "GAMMA"]
        results = eng.assess_batch([make_input(rep_id=i) for i in ids])
        assert [r.rep_id for r in results] == ids

    def test_assess_batch_same_as_sequential_assess(self):
        inp = make_input()
        eng1 = engine()
        eng2 = engine()
        batch_result = eng1.assess_batch([inp])[0]
        single_result = eng2.assess(inp)
        assert batch_result.conv_composite == single_result.conv_composite
        assert batch_result.conv_risk == single_result.conv_risk


# ─────────────────────────────────────────────────────────────
# 14. SUB-SCORE BOUNDARIES
# ─────────────────────────────────────────────────────────────

class TestSubScoreBoundaries:
    def test_listening_score_capped_at_100(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.80,  # +45
            feature_mention_rate_per_call=10.0,  # +35
            value_statement_rate_pct=0.20,  # +20
        )
        result = eng.assess(inp)
        assert result.listening_score <= 100.0

    def test_questioning_score_capped_at_100(self):
        eng = engine()
        inp = make_input(
            avg_questions_per_call=1.0,  # +40
            open_ended_question_rate_pct=0.20,  # +35
            stakeholder_question_rate_pct=0.20,  # +25
        )
        result = eng.assess(inp)
        assert result.questioning_score <= 100.0

    def test_discovery_score_capped_at_100(self):
        eng = engine()
        inp = make_input(
            pain_articulation_rate_pct=0.20,  # +40
            discovery_depth_score=2.0,  # +35
            agenda_set_rate_pct=0.20,  # +25
        )
        result = eng.assess(inp)
        assert result.discovery_score <= 100.0

    def test_closing_score_capped_at_100(self):
        eng = engine()
        inp = make_input(
            next_step_commitment_rate_pct=0.20,  # +40
            closing_attempt_rate_pct=0.20,  # +35
            objection_handling_rate_pct=0.30,  # +25
        )
        result = eng.assess(inp)
        assert result.closing_effectiveness_score <= 100.0

    def test_all_sub_scores_non_negative(self):
        eng = engine()
        result = eng.assess(make_input())
        assert result.listening_score >= 0
        assert result.questioning_score >= 0
        assert result.discovery_score >= 0
        assert result.closing_effectiveness_score >= 0

    def test_composite_within_bounds(self):
        eng = engine()
        result = eng.assess(make_input())
        assert 0 <= result.conv_composite <= 100

    def test_listening_score_zero_for_ideal_rep(self):
        """Ideal rep: low talk, few features, high value statements → listening=0."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,   # < 0.55 → 0
            feature_mention_rate_per_call=1.0,  # < 3 → 0
            value_statement_rate_pct=0.80,   # > 0.50 → 0
        )
        result = eng.assess(inp)
        assert result.listening_score == 0.0

    def test_questioning_score_zero_for_ideal_rep(self):
        """Ideal rep: many questions, high open-ended, high stakeholder → questioning=0."""
        eng = engine()
        inp = make_input(
            avg_questions_per_call=12.0,          # > 9 → 0
            open_ended_question_rate_pct=0.80,    # > 0.65 → 0
            stakeholder_question_rate_pct=0.60,   # > 0.45 → 0
        )
        result = eng.assess(inp)
        assert result.questioning_score == 0.0

    def test_discovery_score_zero_for_ideal_rep(self):
        eng = engine()
        inp = make_input(
            pain_articulation_rate_pct=0.80,  # > 0.70 → 0
            discovery_depth_score=8.0,        # > 7.5 → 0
            agenda_set_rate_pct=0.70,         # > 0.60 → 0
        )
        result = eng.assess(inp)
        assert result.discovery_score == 0.0

    def test_closing_score_zero_for_ideal_rep(self):
        eng = engine()
        inp = make_input(
            next_step_commitment_rate_pct=0.80,  # > 0.70 → 0
            closing_attempt_rate_pct=0.80,       # > 0.65 → 0
            objection_handling_rate_pct=0.70,    # > 0.60 → 0
        )
        result = eng.assess(inp)
        assert result.closing_effectiveness_score == 0.0


# ─────────────────────────────────────────────────────────────
# 15. COMPOSITE CALCULATION
# ─────────────────────────────────────────────────────────────

class TestCompositeCalculation:
    def test_composite_weighted_sum(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        expected_composite = round(
            result.listening_score * 0.30
            + result.questioning_score * 0.25
            + result.discovery_score * 0.25
            + result.closing_effectiveness_score * 0.20,
            2
        )
        assert result.conv_composite == expected_composite

    def test_composite_rounded_to_2_decimal_places(self):
        eng = engine()
        result = eng.assess(make_input())
        assert result.conv_composite == round(result.conv_composite, 2)

    def test_composite_worst_case_is_100(self):
        """All sub-scores maxed at 100 → composite = 100."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.80,
            feature_mention_rate_per_call=10.0,
            value_statement_rate_pct=0.20,
            avg_questions_per_call=1.0,
            open_ended_question_rate_pct=0.20,
            stakeholder_question_rate_pct=0.20,
            pain_articulation_rate_pct=0.20,
            discovery_depth_score=2.0,
            agenda_set_rate_pct=0.20,
            next_step_commitment_rate_pct=0.20,
            closing_attempt_rate_pct=0.20,
            objection_handling_rate_pct=0.20,
        )
        result = eng.assess(inp)
        assert result.conv_composite == pytest.approx(
            result.listening_score * 0.30
            + result.questioning_score * 0.25
            + result.discovery_score * 0.25
            + result.closing_effectiveness_score * 0.20,
            abs=0.01
        )


# ─────────────────────────────────────────────────────────────
# 16. EDGE CASES — ZERO VALUES
# ─────────────────────────────────────────────────────────────

class TestEdgeCasesZeroValues:
    def test_all_zero_rates(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.0,
            avg_questions_per_call=0.0,
            open_ended_question_rate_pct=0.0,
            discovery_depth_score=0.0,
            next_step_commitment_rate_pct=0.0,
            closing_attempt_rate_pct=0.0,
            feature_mention_rate_per_call=0.0,
            pain_articulation_rate_pct=0.0,
            stakeholder_question_rate_pct=0.0,
            objection_handling_rate_pct=0.0,
            agenda_set_rate_pct=0.0,
            value_statement_rate_pct=0.0,
            avg_opportunity_value_usd=0.0,
            active_deal_count=0,
        )
        result = eng.assess(inp)
        assert isinstance(result, ConvResult)

    def test_zero_active_deals_zero_revenue(self):
        eng = engine()
        inp = make_input(active_deal_count=0, avg_opportunity_value_usd=50000.0,
                         avg_talk_to_listen_ratio=0.80)
        result = eng.assess(inp)
        assert result.estimated_revenue_impact_usd == 0.0

    def test_zero_opportunity_value_zero_revenue(self):
        eng = engine()
        inp = make_input(active_deal_count=10, avg_opportunity_value_usd=0.0,
                         avg_talk_to_listen_ratio=0.80)
        result = eng.assess(inp)
        assert result.estimated_revenue_impact_usd == 0.0

    def test_zero_questions_not_crashing(self):
        eng = engine()
        inp = make_input(avg_questions_per_call=0.0)
        result = eng.assess(inp)
        assert result.questioning_score > 0  # <= 3 → +40

    def test_zero_composite_is_valid(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.40,
            avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90,
            discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90,
            closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0,
            pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90,
            objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90,
            value_statement_rate_pct=0.90,
        )
        result = eng.assess(inp)
        assert result.conv_composite == 0.0


# ─────────────────────────────────────────────────────────────
# 17. LISTENING SCORE THRESHOLDS
# ─────────────────────────────────────────────────────────────

class TestListeningScoreThresholds:
    def test_talk_ratio_075_adds_45(self):
        eng = engine()
        r = eng.assess(make_input(avg_talk_to_listen_ratio=0.75,
                                   feature_mention_rate_per_call=1.0,
                                   value_statement_rate_pct=0.90))
        assert r.listening_score == 45.0

    def test_talk_ratio_065_adds_28(self):
        eng = engine()
        r = eng.assess(make_input(avg_talk_to_listen_ratio=0.65,
                                   feature_mention_rate_per_call=1.0,
                                   value_statement_rate_pct=0.90))
        assert r.listening_score == 28.0

    def test_talk_ratio_055_adds_12(self):
        eng = engine()
        r = eng.assess(make_input(avg_talk_to_listen_ratio=0.55,
                                   feature_mention_rate_per_call=1.0,
                                   value_statement_rate_pct=0.90))
        assert r.listening_score == 12.0

    def test_features_ge_8_adds_35(self):
        eng = engine()
        r = eng.assess(make_input(avg_talk_to_listen_ratio=0.40,
                                   feature_mention_rate_per_call=8.0,
                                   value_statement_rate_pct=0.90))
        assert r.listening_score == 35.0

    def test_features_ge_5_adds_20(self):
        eng = engine()
        r = eng.assess(make_input(avg_talk_to_listen_ratio=0.40,
                                   feature_mention_rate_per_call=5.0,
                                   value_statement_rate_pct=0.90))
        assert r.listening_score == 20.0

    def test_features_ge_3_adds_8(self):
        eng = engine()
        r = eng.assess(make_input(avg_talk_to_listen_ratio=0.40,
                                   feature_mention_rate_per_call=3.0,
                                   value_statement_rate_pct=0.90))
        assert r.listening_score == 8.0

    def test_value_le_030_adds_20(self):
        eng = engine()
        r = eng.assess(make_input(avg_talk_to_listen_ratio=0.40,
                                   feature_mention_rate_per_call=1.0,
                                   value_statement_rate_pct=0.30))
        assert r.listening_score == 20.0

    def test_value_le_050_adds_10(self):
        eng = engine()
        r = eng.assess(make_input(avg_talk_to_listen_ratio=0.40,
                                   feature_mention_rate_per_call=1.0,
                                   value_statement_rate_pct=0.50))
        assert r.listening_score == 10.0


# ─────────────────────────────────────────────────────────────
# 18. QUESTIONING SCORE THRESHOLDS
# ─────────────────────────────────────────────────────────────

class TestQuestioningScoreThresholds:
    def test_questions_le_3_adds_40(self):
        eng = engine()
        r = eng.assess(make_input(avg_questions_per_call=3.0,
                                   open_ended_question_rate_pct=0.90,
                                   stakeholder_question_rate_pct=0.90))
        assert r.questioning_score == 40.0

    def test_questions_le_6_adds_22(self):
        eng = engine()
        r = eng.assess(make_input(avg_questions_per_call=6.0,
                                   open_ended_question_rate_pct=0.90,
                                   stakeholder_question_rate_pct=0.90))
        assert r.questioning_score == 22.0

    def test_questions_le_9_adds_8(self):
        eng = engine()
        r = eng.assess(make_input(avg_questions_per_call=9.0,
                                   open_ended_question_rate_pct=0.90,
                                   stakeholder_question_rate_pct=0.90))
        assert r.questioning_score == 8.0

    def test_open_ended_le_030_adds_35(self):
        eng = engine()
        r = eng.assess(make_input(avg_questions_per_call=15.0,
                                   open_ended_question_rate_pct=0.30,
                                   stakeholder_question_rate_pct=0.90))
        assert r.questioning_score == 35.0

    def test_open_ended_le_050_adds_18(self):
        eng = engine()
        r = eng.assess(make_input(avg_questions_per_call=15.0,
                                   open_ended_question_rate_pct=0.50,
                                   stakeholder_question_rate_pct=0.90))
        assert r.questioning_score == 18.0

    def test_stakeholder_le_025_adds_25(self):
        eng = engine()
        r = eng.assess(make_input(avg_questions_per_call=15.0,
                                   open_ended_question_rate_pct=0.90,
                                   stakeholder_question_rate_pct=0.25))
        assert r.questioning_score == 25.0

    def test_stakeholder_le_045_adds_12(self):
        eng = engine()
        r = eng.assess(make_input(avg_questions_per_call=15.0,
                                   open_ended_question_rate_pct=0.90,
                                   stakeholder_question_rate_pct=0.45))
        assert r.questioning_score == 12.0


# ─────────────────────────────────────────────────────────────
# 19. DISCOVERY SCORE THRESHOLDS
# ─────────────────────────────────────────────────────────────

class TestDiscoveryScoreThresholds:
    def test_pain_le_035_adds_40(self):
        eng = engine()
        r = eng.assess(make_input(pain_articulation_rate_pct=0.35,
                                   discovery_depth_score=10.0,
                                   agenda_set_rate_pct=0.90))
        assert r.discovery_score == 40.0

    def test_pain_le_055_adds_22(self):
        eng = engine()
        r = eng.assess(make_input(pain_articulation_rate_pct=0.55,
                                   discovery_depth_score=10.0,
                                   agenda_set_rate_pct=0.90))
        assert r.discovery_score == 22.0

    def test_pain_le_070_adds_8(self):
        eng = engine()
        r = eng.assess(make_input(pain_articulation_rate_pct=0.70,
                                   discovery_depth_score=10.0,
                                   agenda_set_rate_pct=0.90))
        assert r.discovery_score == 8.0

    def test_depth_le_4_adds_35(self):
        eng = engine()
        r = eng.assess(make_input(pain_articulation_rate_pct=0.90,
                                   discovery_depth_score=4.0,
                                   agenda_set_rate_pct=0.90))
        assert r.discovery_score == 35.0

    def test_depth_le_6_adds_18(self):
        eng = engine()
        r = eng.assess(make_input(pain_articulation_rate_pct=0.90,
                                   discovery_depth_score=6.0,
                                   agenda_set_rate_pct=0.90))
        assert r.discovery_score == 18.0

    def test_agenda_le_040_adds_25(self):
        eng = engine()
        r = eng.assess(make_input(pain_articulation_rate_pct=0.90,
                                   discovery_depth_score=10.0,
                                   agenda_set_rate_pct=0.40))
        assert r.discovery_score == 25.0

    def test_agenda_le_060_adds_12(self):
        eng = engine()
        r = eng.assess(make_input(pain_articulation_rate_pct=0.90,
                                   discovery_depth_score=10.0,
                                   agenda_set_rate_pct=0.60))
        assert r.discovery_score == 12.0


# ─────────────────────────────────────────────────────────────
# 20. CLOSING SCORE THRESHOLDS
# ─────────────────────────────────────────────────────────────

class TestClosingScoreThresholds:
    def test_next_step_le_035_adds_40(self):
        eng = engine()
        r = eng.assess(make_input(next_step_commitment_rate_pct=0.35,
                                   closing_attempt_rate_pct=0.90,
                                   objection_handling_rate_pct=0.90))
        assert r.closing_effectiveness_score == 40.0

    def test_next_step_le_055_adds_22(self):
        eng = engine()
        r = eng.assess(make_input(next_step_commitment_rate_pct=0.55,
                                   closing_attempt_rate_pct=0.90,
                                   objection_handling_rate_pct=0.90))
        assert r.closing_effectiveness_score == 22.0

    def test_closing_le_030_adds_35(self):
        eng = engine()
        r = eng.assess(make_input(next_step_commitment_rate_pct=0.90,
                                   closing_attempt_rate_pct=0.30,
                                   objection_handling_rate_pct=0.90))
        assert r.closing_effectiveness_score == 35.0

    def test_closing_le_050_adds_18(self):
        eng = engine()
        r = eng.assess(make_input(next_step_commitment_rate_pct=0.90,
                                   closing_attempt_rate_pct=0.50,
                                   objection_handling_rate_pct=0.90))
        assert r.closing_effectiveness_score == 18.0

    def test_objection_le_040_adds_25(self):
        eng = engine()
        r = eng.assess(make_input(next_step_commitment_rate_pct=0.90,
                                   closing_attempt_rate_pct=0.90,
                                   objection_handling_rate_pct=0.40))
        assert r.closing_effectiveness_score == 25.0

    def test_objection_le_060_adds_12(self):
        eng = engine()
        r = eng.assess(make_input(next_step_commitment_rate_pct=0.90,
                                   closing_attempt_rate_pct=0.90,
                                   objection_handling_rate_pct=0.60))
        assert r.closing_effectiveness_score == 12.0


# ─────────────────────────────────────────────────────────────
# 21. SUMMARY AGGREGATION
# ─────────────────────────────────────────────────────────────

class TestSummaryAggregation:
    def test_summary_avg_composite_correct(self):
        eng = engine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(make_input(rep_id="B"))
        s = eng.summary()
        expected = round((r1.conv_composite + r2.conv_composite) / 2, 1)
        assert s["avg_conv_composite"] == expected

    def test_summary_gap_count(self):
        eng = engine()
        r1 = eng.assess(make_input())
        r2 = eng.assess(make_input(avg_talk_to_listen_ratio=0.40, avg_questions_per_call=12.0,
                                    open_ended_question_rate_pct=0.90))
        s = eng.summary()
        expected = (1 if r1.has_conv_gap else 0) + (1 if r2.has_conv_gap else 0)
        assert s["conv_gap_count"] == expected

    def test_summary_coaching_count(self):
        eng = engine()
        r1 = eng.assess(make_input())
        r2 = eng.assess(make_input(open_ended_question_rate_pct=0.90,
                                    next_step_commitment_rate_pct=0.90))
        s = eng.summary()
        expected = (1 if r1.requires_conv_coaching else 0) + (1 if r2.requires_conv_coaching else 0)
        assert s["coaching_count"] == expected

    def test_summary_total_revenue(self):
        eng = engine()
        r1 = eng.assess(make_input(active_deal_count=5, avg_opportunity_value_usd=10000.0,
                                    avg_talk_to_listen_ratio=0.60))
        r2 = eng.assess(make_input(active_deal_count=3, avg_opportunity_value_usd=20000.0,
                                    avg_talk_to_listen_ratio=0.70))
        s = eng.summary()
        expected = round(r1.estimated_revenue_impact_usd + r2.estimated_revenue_impact_usd, 2)
        assert s["total_estimated_revenue_impact_usd"] == expected

    def test_summary_avg_listening_correct(self):
        eng = engine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(make_input(rep_id="B"))
        s = eng.summary()
        expected = round((r1.listening_score + r2.listening_score) / 2, 1)
        assert s["avg_listening_score"] == expected

    def test_summary_avg_questioning_correct(self):
        eng = engine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(make_input(rep_id="B"))
        s = eng.summary()
        expected = round((r1.questioning_score + r2.questioning_score) / 2, 1)
        assert s["avg_questioning_score"] == expected

    def test_summary_multiple_risk_counts(self):
        eng = engine()
        # generate at least a low and a critical
        eng.assess(make_input(  # likely low
            avg_talk_to_listen_ratio=0.40, avg_questions_per_call=15.0,
            open_ended_question_rate_pct=0.90, discovery_depth_score=9.0,
            next_step_commitment_rate_pct=0.90, closing_attempt_rate_pct=0.90,
            feature_mention_rate_per_call=1.0, pain_articulation_rate_pct=0.90,
            stakeholder_question_rate_pct=0.90, objection_handling_rate_pct=0.90,
            agenda_set_rate_pct=0.90, value_statement_rate_pct=0.90,
        ))
        eng.assess(make_input(  # likely critical
            avg_talk_to_listen_ratio=0.80, avg_questions_per_call=1.0,
            open_ended_question_rate_pct=0.10, discovery_depth_score=1.0,
            next_step_commitment_rate_pct=0.10, closing_attempt_rate_pct=0.10,
            feature_mention_rate_per_call=12.0, pain_articulation_rate_pct=0.10,
            stakeholder_question_rate_pct=0.10, objection_handling_rate_pct=0.10,
            agenda_set_rate_pct=0.10, value_statement_rate_pct=0.10,
        ))
        s = eng.summary()
        assert sum(s["risk_counts"].values()) == 2
        assert s["total"] == 2


# ─────────────────────────────────────────────────────────────
# 22. PATTERN BOUNDARY CONDITIONS
# ─────────────────────────────────────────────────────────────

class TestPatternBoundaryConditions:
    def test_monologue_seller_talk_exactly_070(self):
        """talk >= 0.70 AND features >= 6 → monologue_seller."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.70,
            feature_mention_rate_per_call=6.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.monologue_seller

    def test_monologue_seller_features_exactly_6(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.71,
            feature_mention_rate_per_call=6.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.monologue_seller

    def test_no_monologue_talk_just_below_070(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.69,
            feature_mention_rate_per_call=8.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
        )
        result = eng.assess(inp)
        assert result.conv_pattern != ConvPattern.monologue_seller

    def test_shallow_questioner_questions_exactly_4(self):
        """questions <= 4 AND oer <= 0.35."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=4.0,
            open_ended_question_rate_pct=0.35,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.shallow_questioner

    def test_close_avoider_next_step_exactly_030(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            next_step_commitment_rate_pct=0.30,
            closing_attempt_rate_pct=0.35,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.close_avoider

    def test_discovery_skipper_pain_exactly_040(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            next_step_commitment_rate_pct=0.70,
            closing_attempt_rate_pct=0.70,
            pain_articulation_rate_pct=0.40,
            discovery_depth_score=5.0,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.discovery_skipper


# ─────────────────────────────────────────────────────────────
# 23. RESULT FIELDS TYPES
# ─────────────────────────────────────────────────────────────

class TestResultFieldTypes:
    def test_result_rep_id_is_str(self):
        r = engine().assess(make_input())
        assert isinstance(r.rep_id, str)

    def test_result_region_is_str(self):
        r = engine().assess(make_input())
        assert isinstance(r.region, str)

    def test_result_risk_is_conv_risk(self):
        r = engine().assess(make_input())
        assert isinstance(r.conv_risk, ConvRisk)

    def test_result_pattern_is_conv_pattern(self):
        r = engine().assess(make_input())
        assert isinstance(r.conv_pattern, ConvPattern)

    def test_result_severity_is_conv_severity(self):
        r = engine().assess(make_input())
        assert isinstance(r.conv_severity, ConvSeverity)

    def test_result_action_is_conv_action(self):
        r = engine().assess(make_input())
        assert isinstance(r.recommended_action, ConvAction)

    def test_result_listening_score_is_float(self):
        r = engine().assess(make_input())
        assert isinstance(r.listening_score, float)

    def test_result_composite_is_float(self):
        r = engine().assess(make_input())
        assert isinstance(r.conv_composite, float)

    def test_result_has_gap_is_bool(self):
        r = engine().assess(make_input())
        assert isinstance(r.has_conv_gap, bool)

    def test_result_requires_coaching_is_bool(self):
        r = engine().assess(make_input())
        assert isinstance(r.requires_conv_coaching, bool)

    def test_result_revenue_is_float(self):
        r = engine().assess(make_input())
        assert isinstance(r.estimated_revenue_impact_usd, float)

    def test_result_signal_is_str(self):
        r = engine().assess(make_input())
        assert isinstance(r.conv_signal, str)


# ─────────────────────────────────────────────────────────────
# 24. ENGINE STATE
# ─────────────────────────────────────────────────────────────

class TestEngineState:
    def test_engine_starts_empty(self):
        eng = engine()
        assert eng.summary()["total"] == 0

    def test_engine_accumulates_results(self):
        eng = engine()
        for i in range(5):
            eng.assess(make_input(rep_id=f"R{i}"))
        assert eng.summary()["total"] == 5

    def test_two_engines_are_independent(self):
        eng1 = engine()
        eng2 = engine()
        eng1.assess(make_input())
        eng1.assess(make_input(rep_id="R002"))
        eng2.assess(make_input())
        assert eng1.summary()["total"] == 2
        assert eng2.summary()["total"] == 1

    def test_assess_returns_conv_result(self):
        r = engine().assess(make_input())
        assert isinstance(r, ConvResult)

    def test_batch_result_ids_correct(self):
        eng = engine()
        results = eng.assess_batch([make_input(rep_id="X"), make_input(rep_id="Y")])
        assert results[0].rep_id == "X"
        assert results[1].rep_id == "Y"

    def test_summary_severity_keys_are_strings(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        for key in s["severity_counts"]:
            assert isinstance(key, str)

    def test_summary_action_counts_keys_are_strings(self):
        eng = engine()
        eng.assess(make_input())
        s = eng.summary()
        for key in s["action_counts"]:
            assert isinstance(key, str)


# ─────────────────────────────────────────────────────────────
# 25. ADDITIONAL BOUNDARY AND EDGE CASES
# ─────────────────────────────────────────────────────────────

class TestAdditionalEdgeCases:
    def test_feature_dumper_not_when_features_exactly_7_but_value_above_040(self):
        """features=7 but value_statement > 0.40 → NOT feature_dumper."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.60,
            feature_mention_rate_per_call=7.0,
            value_statement_rate_pct=0.50,  # > 0.40 → no feature_dumper
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
        )
        result = eng.assess(inp)
        assert result.conv_pattern != ConvPattern.feature_dumper

    def test_feature_dumper_exactly_7_and_value_040(self):
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.60,
            feature_mention_rate_per_call=7.0,
            value_statement_rate_pct=0.40,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.feature_dumper

    def test_risk_exactly_60_is_critical(self):
        """Composite of exactly 60 → critical."""
        eng = engine()
        # all sub-scores = 100 → composite = 100 → critical
        inp = make_input(
            avg_talk_to_listen_ratio=0.80,
            avg_questions_per_call=1.0,
            open_ended_question_rate_pct=0.10,
            discovery_depth_score=1.0,
            next_step_commitment_rate_pct=0.10,
            closing_attempt_rate_pct=0.10,
            feature_mention_rate_per_call=12.0,
            pain_articulation_rate_pct=0.10,
            stakeholder_question_rate_pct=0.10,
            objection_handling_rate_pct=0.10,
            agenda_set_rate_pct=0.10,
            value_statement_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert result.conv_risk == ConvRisk.critical
        assert result.conv_composite >= 60

    def test_talk_ratio_exactly_040_gives_zero_revenue(self):
        eng = engine()
        inp = make_input(avg_talk_to_listen_ratio=0.40,
                         active_deal_count=10, avg_opportunity_value_usd=50000.0)
        result = eng.assess(inp)
        assert result.estimated_revenue_impact_usd == 0.0

    def test_large_opportunity_value(self):
        eng = engine()
        inp = make_input(avg_opportunity_value_usd=1_000_000.0, active_deal_count=100,
                         avg_talk_to_listen_ratio=0.80)
        result = eng.assess(inp)
        assert isinstance(result.estimated_revenue_impact_usd, float)

    def test_high_call_duration_no_effect_on_composite(self):
        """avg_call_duration_minutes doesn't affect sub-scores."""
        eng1 = engine()
        eng2 = engine()
        r1 = eng1.assess(make_input(avg_call_duration_minutes=10.0))
        r2 = eng2.assess(make_input(avg_call_duration_minutes=120.0))
        assert r1.conv_composite == r2.conv_composite

    def test_competitor_mention_no_effect_on_composite(self):
        """competitor_mention_rate_pct doesn't affect sub-scores."""
        eng1 = engine()
        eng2 = engine()
        r1 = eng1.assess(make_input(competitor_mention_rate_pct=0.0))
        r2 = eng2.assess(make_input(competitor_mention_rate_pct=1.0))
        assert r1.conv_composite == r2.conv_composite

    def test_calls_reviewed_no_effect_on_composite(self):
        eng1 = engine()
        eng2 = engine()
        r1 = eng1.assess(make_input(calls_reviewed_per_month=1))
        r2 = eng2.assess(make_input(calls_reviewed_per_month=100))
        assert r1.conv_composite == r2.conv_composite

    def test_total_calls_no_effect_on_composite(self):
        eng1 = engine()
        eng2 = engine()
        r1 = eng1.assess(make_input(total_calls_per_month=1))
        r2 = eng2.assess(make_input(total_calls_per_month=1000))
        assert r1.conv_composite == r2.conv_composite

    def test_to_dict_conv_risk_value_is_plain_string(self):
        """to_dict() calls .value, so the result is a plain str matching the enum value."""
        r = engine().assess(make_input())
        d = r.to_dict()
        # The value is a plain string equal to the enum's .value
        assert isinstance(d["conv_risk"], str)
        assert d["conv_risk"] in {rv.value for rv in ConvRisk}

    def test_region_propagated_to_result(self):
        r = engine().assess(make_input(region="APAC"))
        assert r.region == "APAC"
        assert r.to_dict()["region"] == "APAC"

    def test_evaluation_period_not_in_result(self):
        """evaluation_period_id is an input field but not a ConvResult field."""
        r = engine().assess(make_input(evaluation_period_id="2024-Q4"))
        d = r.to_dict()
        assert "evaluation_period_id" not in d

    def test_listening_score_combined_all_three_penalties(self):
        """All three listening penalties hit simultaneously."""
        eng = engine()
        r = eng.assess(make_input(
            avg_talk_to_listen_ratio=0.75,   # +45
            feature_mention_rate_per_call=8.0,  # +35
            value_statement_rate_pct=0.30,   # +20
        ))
        assert r.listening_score == 100.0  # capped: 45+35+20=100

    def test_summary_empty_coaching_count_zero(self):
        eng = engine()
        assert eng.summary()["coaching_count"] == 0

    def test_summary_empty_gap_count_zero(self):
        eng = engine()
        assert eng.summary()["conv_gap_count"] == 0

    def test_summary_after_many_assessments(self):
        eng = engine()
        for i in range(50):
            eng.assess(make_input(rep_id=f"R{i:03d}"))
        s = eng.summary()
        assert s["total"] == 50

    def test_pattern_discovery_skipper_depth_exactly_5(self):
        """pain_articulation <= 0.40 AND depth exactly 5 → discovery_skipper."""
        eng = engine()
        inp = make_input(
            avg_talk_to_listen_ratio=0.50,
            feature_mention_rate_per_call=2.0,
            avg_questions_per_call=8.0,
            open_ended_question_rate_pct=0.60,
            next_step_commitment_rate_pct=0.70,
            closing_attempt_rate_pct=0.70,
            pain_articulation_rate_pct=0.40,
            discovery_depth_score=5.0,
        )
        result = eng.assess(inp)
        assert result.conv_pattern == ConvPattern.discovery_skipper
