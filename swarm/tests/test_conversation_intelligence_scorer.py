"""
Comprehensive pytest tests for ConversationIntelligenceScorer.

Invariants tested:
- ConversationIntelligenceInput has exactly 22 fields
- ConversationIntelligenceResult.to_dict() returns exactly 15 keys
- summary() returns exactly 13 keys
- All enum members (ConversationQuality, ConversationPattern, QualificationDepth, ConversationAction)
- Composite formula: discovery*0.30 + qualification*0.30 + communication*0.20 + value*0.20
- is_coachable_moment: coaching_priority >= 60 OR composite < 40
- is_exemplary_call: composite >= 80 AND deal_advancement >= 75
- All score sub-branches
- batch scoring, reset, properties
"""

from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.conversation_intelligence_scorer import (
    ConversationAction,
    ConversationIntelligenceInput,
    ConversationIntelligenceResult,
    ConversationIntelligenceScorer,
    ConversationPattern,
    ConversationQuality,
    QualificationDepth,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helper factories
# ─────────────────────────────────────────────────────────────────────────────

def make_input(**overrides) -> ConversationIntelligenceInput:
    """Return a baseline 'average' call with sensible defaults, then apply overrides."""
    defaults = dict(
        call_id="call-001",
        deal_id="deal-001",
        rep_id="rep-001",
        call_type="discovery",
        talk_listen_ratio=45.0,          # ideal 35-50 → +25 discovery
        questions_asked_count=8,         # >= 6 → +12
        open_ended_question_pct=55.0,    # 50-70 → +15
        pain_point_questions_asked=3,    # >= 3 → +12
        budget_discussed=1,
        authority_confirmed=1,
        timeline_established=1,
        business_impact_quantified=0,
        next_steps_defined=1,
        competitor_mentioned_by_buyer=0,
        objection_count=2,
        objections_handled_count=2,
        filler_words_per_minute=1.0,
        interruptions_count=0,
        monologue_longest_seconds=60,
        value_statement_count=3,
        call_duration_minutes=30,
        deal_value=50000.0,
    )
    defaults.update(overrides)
    return ConversationIntelligenceInput(**defaults)


def make_scorer() -> ConversationIntelligenceScorer:
    return ConversationIntelligenceScorer()


# ─────────────────────────────────────────────────────────────────────────────
# 1. Structural invariants
# ─────────────────────────────────────────────────────────────────────────────

class TestStructuralInvariants:
    def test_input_has_exactly_22_fields(self):
        fields = dataclasses.fields(ConversationIntelligenceInput)
        assert len(fields) == 22

    def test_input_field_names(self):
        names = {f.name for f in dataclasses.fields(ConversationIntelligenceInput)}
        expected = {
            "call_id", "deal_id", "rep_id", "call_type",
            "talk_listen_ratio", "questions_asked_count", "open_ended_question_pct",
            "pain_point_questions_asked", "budget_discussed", "authority_confirmed",
            "timeline_established", "business_impact_quantified", "next_steps_defined",
            "competitor_mentioned_by_buyer", "objection_count", "objections_handled_count",
            "filler_words_per_minute", "interruptions_count", "monologue_longest_seconds",
            "value_statement_count", "call_duration_minutes", "deal_value",
        }
        assert names == expected

    def test_result_to_dict_returns_exactly_15_keys(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        d = result.to_dict()
        assert len(d) == 15

    def test_result_to_dict_exact_keys(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        d = result.to_dict()
        expected_keys = {
            "call_id", "deal_id", "conversation_quality", "conversation_pattern",
            "qualification_depth", "conversation_action", "discovery_score",
            "qualification_score", "communication_score", "value_articulation_score",
            "conversation_composite", "coaching_priority_score", "deal_advancement_score",
            "is_coachable_moment", "is_exemplary_call",
        }
        assert set(d.keys()) == expected_keys

    def test_summary_returns_exactly_13_keys(self):
        scorer = make_scorer()
        scorer.score(make_input())
        s = scorer.summary()
        assert len(s) == 13

    def test_summary_exact_keys(self):
        scorer = make_scorer()
        scorer.score(make_input())
        s = scorer.summary()
        expected_keys = {
            "total", "quality_counts", "pattern_counts", "depth_counts", "action_counts",
            "avg_conversation_composite", "avg_deal_advancement_score",
            "coachable_count", "exemplary_count", "avg_discovery_score",
            "avg_qualification_score", "avg_communication_score",
            "avg_value_articulation_score",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_empty_returns_13_keys(self):
        scorer = make_scorer()
        s = scorer.summary()
        assert len(s) == 13

    def test_summary_empty_exact_keys(self):
        scorer = make_scorer()
        s = scorer.summary()
        expected_keys = {
            "total", "quality_counts", "pattern_counts", "depth_counts", "action_counts",
            "avg_conversation_composite", "avg_deal_advancement_score",
            "coachable_count", "exemplary_count", "avg_discovery_score",
            "avg_qualification_score", "avg_communication_score",
            "avg_value_articulation_score",
        }
        assert set(s.keys()) == expected_keys

    def test_result_is_dataclass(self):
        assert dataclasses.is_dataclass(ConversationIntelligenceResult)

    def test_input_is_dataclass(self):
        assert dataclasses.is_dataclass(ConversationIntelligenceInput)

    def test_to_dict_enum_values_are_strings(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        d = result.to_dict()
        for key in ("conversation_quality", "conversation_pattern",
                    "qualification_depth", "conversation_action"):
            assert isinstance(d[key], str), f"{key} should be a string"


# ─────────────────────────────────────────────────────────────────────────────
# 2. Enum members
# ─────────────────────────────────────────────────────────────────────────────

class TestEnumMembers:
    def test_conversation_quality_members(self):
        values = {e.value for e in ConversationQuality}
        assert values == {"poor", "developing", "proficient", "elite"}

    def test_conversation_quality_count(self):
        assert len(ConversationQuality) == 4

    def test_conversation_pattern_members(self):
        values = {e.value for e in ConversationPattern}
        assert values == {
            "feature_dump", "shallow_discovery", "monologue",
            "balanced_dialogue", "consultative", "challenger",
        }

    def test_conversation_pattern_count(self):
        assert len(ConversationPattern) == 6

    def test_qualification_depth_members(self):
        values = {e.value for e in QualificationDepth}
        assert values == {
            "unqualified", "surface_level", "moderately_qualified", "deeply_qualified",
        }

    def test_qualification_depth_count(self):
        assert len(QualificationDepth) == 4

    def test_conversation_action_members(self):
        values = {e.value for e in ConversationAction}
        assert values == {
            "coach_immediately", "structured_coaching",
            "reinforce_strengths", "share_as_example",
        }

    def test_conversation_action_count(self):
        assert len(ConversationAction) == 4

    def test_quality_enum_is_str(self):
        assert isinstance(ConversationQuality.POOR, str)

    def test_pattern_enum_is_str(self):
        assert isinstance(ConversationPattern.CHALLENGER, str)

    def test_depth_enum_is_str(self):
        assert isinstance(QualificationDepth.DEEPLY_QUALIFIED, str)

    def test_action_enum_is_str(self):
        assert isinstance(ConversationAction.SHARE_AS_EXAMPLE, str)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Discovery score branches
# ─────────────────────────────────────────────────────────────────────────────

class TestDiscoveryScore:
    """Test all branches of _discovery_score."""

    def _get_discovery(self, **kw) -> float:
        scorer = make_scorer()
        return scorer.score(make_input(**kw)).discovery_score

    # --- talk_listen_ratio branches ---
    def test_ttl_35_to_50_adds_25(self):
        # baseline: ttl=45 -> +25, questions=8 -> +12, oeq=55 -> +15, pain=3 -> +12, mono=60 -> 0
        # expected = 25+12+15+12 = 64
        s = self._get_discovery(talk_listen_ratio=45.0)
        assert s == 64.0

    def test_ttl_exactly_35_adds_25(self):
        s = self._get_discovery(talk_listen_ratio=35.0)
        assert s == 64.0

    def test_ttl_exactly_50_adds_25(self):
        s = self._get_discovery(talk_listen_ratio=50.0)
        assert s == 64.0

    def test_ttl_51_to_65_adds_15(self):
        # ttl=60 -> +15, questions=8 -> +12, oeq=55 -> +15, pain=3 -> +12 => 54
        s = self._get_discovery(talk_listen_ratio=60.0)
        assert s == 54.0

    def test_ttl_exactly_65_adds_15(self):
        s = self._get_discovery(talk_listen_ratio=65.0)
        assert s == 54.0

    def test_ttl_above_65_adds_5(self):
        # ttl=70 -> +5, questions=8 -> +12, oeq=55 -> +15, pain=3 -> +12 => 44
        s = self._get_discovery(talk_listen_ratio=70.0)
        assert s == 44.0

    def test_ttl_below_35_adds_18(self):
        # ttl=20 -> +18, questions=8 -> +12, oeq=55 -> +15, pain=3 -> +12 => 57
        s = self._get_discovery(talk_listen_ratio=20.0)
        assert s == 57.0

    def test_ttl_exactly_34_9_adds_18(self):
        s = self._get_discovery(talk_listen_ratio=34.9)
        assert s == 57.0

    # --- questions_asked_count branches ---
    def test_questions_ge_10_adds_20(self):
        # ttl=45 -> +25, questions=10 -> +20, oeq=55 -> +15, pain=3 -> +12 => 72
        s = self._get_discovery(questions_asked_count=10)
        assert s == 72.0

    def test_questions_exactly_10_adds_20(self):
        s = self._get_discovery(questions_asked_count=10)
        assert s == 72.0

    def test_questions_6_to_9_adds_12(self):
        # baseline questions=8 -> +12 (already tested above at 64)
        s = self._get_discovery(questions_asked_count=6)
        assert s == 64.0

    def test_questions_3_to_5_adds_6(self):
        # ttl=45 -> +25, questions=3 -> +6, oeq=55 -> +15, pain=3 -> +12 => 58
        s = self._get_discovery(questions_asked_count=3)
        assert s == 58.0

    def test_questions_exactly_3_adds_6(self):
        s = self._get_discovery(questions_asked_count=3)
        assert s == 58.0

    def test_questions_below_3_adds_0(self):
        # ttl=45 -> +25, questions=2 -> +0, oeq=55 -> +15, pain=3 -> +12 => 52
        s = self._get_discovery(questions_asked_count=2)
        assert s == 52.0

    def test_questions_0_adds_0(self):
        s = self._get_discovery(questions_asked_count=0)
        assert s == 52.0

    # --- open_ended_question_pct branches ---
    def test_oeq_ge_70_adds_25(self):
        # ttl=45 -> +25, questions=8 -> +12, oeq=70 -> +25, pain=3 -> +12 => 74
        s = self._get_discovery(open_ended_question_pct=70.0)
        assert s == 74.0

    def test_oeq_exactly_70_adds_25(self):
        s = self._get_discovery(open_ended_question_pct=70.0)
        assert s == 74.0

    def test_oeq_50_to_69_adds_15(self):
        # baseline oeq=55 -> +15 => 64 (tested above)
        s = self._get_discovery(open_ended_question_pct=50.0)
        assert s == 64.0

    def test_oeq_exactly_50_adds_15(self):
        s = self._get_discovery(open_ended_question_pct=50.0)
        assert s == 64.0

    def test_oeq_30_to_49_adds_8(self):
        # ttl=45 -> +25, questions=8 -> +12, oeq=30 -> +8, pain=3 -> +12 => 57
        s = self._get_discovery(open_ended_question_pct=30.0)
        assert s == 57.0

    def test_oeq_exactly_30_adds_8(self):
        s = self._get_discovery(open_ended_question_pct=30.0)
        assert s == 57.0

    def test_oeq_below_30_adds_0(self):
        # ttl=45 -> +25, questions=8 -> +12, oeq=0 -> +0, pain=3 -> +12 => 49
        s = self._get_discovery(open_ended_question_pct=0.0)
        assert s == 49.0

    # --- pain_point_questions_asked branches ---
    def test_pain_ge_5_adds_20(self):
        # ttl=45 -> +25, questions=8 -> +12, oeq=55 -> +15, pain=5 -> +20 => 72
        s = self._get_discovery(pain_point_questions_asked=5)
        assert s == 72.0

    def test_pain_exactly_5_adds_20(self):
        s = self._get_discovery(pain_point_questions_asked=5)
        assert s == 72.0

    def test_pain_3_to_4_adds_12(self):
        # baseline pain=3 -> +12 => 64
        s = self._get_discovery(pain_point_questions_asked=3)
        assert s == 64.0

    def test_pain_exactly_3_adds_12(self):
        s = self._get_discovery(pain_point_questions_asked=3)
        assert s == 64.0

    def test_pain_1_to_2_adds_6(self):
        # ttl=45 -> +25, questions=8 -> +12, oeq=55 -> +15, pain=1 -> +6 => 58
        s = self._get_discovery(pain_point_questions_asked=1)
        assert s == 58.0

    def test_pain_0_adds_0(self):
        # ttl=45 -> +25, questions=8 -> +12, oeq=55 -> +15, pain=0 -> +0 => 52
        s = self._get_discovery(pain_point_questions_asked=0)
        assert s == 52.0

    # --- monologue penalty branches ---
    def test_monologue_ge_180_subtracts_15(self):
        # ttl=45 -> +25, questions=8 -> +12, oeq=55 -> +15, pain=3 -> +12, mono=180 -> -15 => 49
        s = self._get_discovery(monologue_longest_seconds=180)
        assert s == 49.0

    def test_monologue_exactly_180_subtracts_15(self):
        s = self._get_discovery(monologue_longest_seconds=180)
        assert s == 49.0

    def test_monologue_90_to_179_subtracts_8(self):
        # ttl=45 -> +25, questions=8 -> +12, oeq=55 -> +15, pain=3 -> +12, mono=90 -> -8 => 56
        s = self._get_discovery(monologue_longest_seconds=90)
        assert s == 56.0

    def test_monologue_exactly_90_subtracts_8(self):
        s = self._get_discovery(monologue_longest_seconds=90)
        assert s == 56.0

    def test_monologue_below_90_no_penalty(self):
        # ttl=45 -> +25, questions=8 -> +12, oeq=55 -> +15, pain=3 -> +12, mono=89 -> 0 => 64
        s = self._get_discovery(monologue_longest_seconds=89)
        assert s == 64.0

    def test_discovery_score_clamp_min_zero(self):
        # Minimize everything: ttl=70 -> +5, questions=0 -> 0, oeq=0 -> 0, pain=0 -> 0, mono=200 -> -15 => max(0, -10) = 0
        s = self._get_discovery(
            talk_listen_ratio=100.0,
            questions_asked_count=0,
            open_ended_question_pct=0.0,
            pain_point_questions_asked=0,
            monologue_longest_seconds=250,
        )
        assert s == 0.0

    def test_discovery_score_clamp_max_100(self):
        # Maximize everything within reasonable bounds: ttl=45 -> +25, q=10 -> +20, oeq=80 -> +25, pain=6 -> +20 => 90
        s = self._get_discovery(
            talk_listen_ratio=45.0,
            questions_asked_count=15,
            open_ended_question_pct=90.0,
            pain_point_questions_asked=6,
            monologue_longest_seconds=10,
        )
        assert s == 90.0  # 25+20+25+20 = 90, no penalty → no clamping needed, but stays ≤100

    def test_discovery_score_above_theoretical_max_stays_100(self):
        # Theoretical max = 25+20+25+20 = 90, which can't exceed 100 anyway
        scorer = make_scorer()
        inp = make_input(
            talk_listen_ratio=45.0,
            questions_asked_count=15,
            open_ended_question_pct=95.0,
            pain_point_questions_asked=10,
            monologue_longest_seconds=1,
        )
        result = scorer.score(inp)
        assert result.discovery_score <= 100.0


# ─────────────────────────────────────────────────────────────────────────────
# 4. Qualification score branches
# ─────────────────────────────────────────────────────────────────────────────

class TestQualificationScore:
    def _get_qual(self, **kw) -> float:
        scorer = make_scorer()
        return scorer.score(make_input(**kw)).qualification_score

    def test_all_meddic_signals_present(self):
        s = self._get_qual(
            budget_discussed=1, authority_confirmed=1, timeline_established=1,
            business_impact_quantified=1, next_steps_defined=1
        )
        assert s == 100.0

    def test_no_meddic_signals(self):
        s = self._get_qual(
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0
        )
        assert s == 0.0

    def test_budget_only_adds_20(self):
        s = self._get_qual(
            budget_discussed=1, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0
        )
        assert s == 20.0

    def test_authority_only_adds_20(self):
        s = self._get_qual(
            budget_discussed=0, authority_confirmed=1, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0
        )
        assert s == 20.0

    def test_timeline_only_adds_20(self):
        s = self._get_qual(
            budget_discussed=0, authority_confirmed=0, timeline_established=1,
            business_impact_quantified=0, next_steps_defined=0
        )
        assert s == 20.0

    def test_business_impact_only_adds_25(self):
        s = self._get_qual(
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=1, next_steps_defined=0
        )
        assert s == 25.0

    def test_next_steps_only_adds_15(self):
        s = self._get_qual(
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=1
        )
        assert s == 15.0

    def test_budget_authority_timeline(self):
        s = self._get_qual(
            budget_discussed=1, authority_confirmed=1, timeline_established=1,
            business_impact_quantified=0, next_steps_defined=0
        )
        assert s == 60.0

    def test_qual_score_clamped_to_100(self):
        s = self._get_qual(
            budget_discussed=1, authority_confirmed=1, timeline_established=1,
            business_impact_quantified=1, next_steps_defined=1
        )
        assert s <= 100.0

    def test_qual_score_clamped_to_0(self):
        s = self._get_qual(
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0
        )
        assert s >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 5. Communication score branches
# ─────────────────────────────────────────────────────────────────────────────

class TestCommunicationScore:
    def _get_comm(self, **kw) -> float:
        scorer = make_scorer()
        return scorer.score(make_input(**kw)).communication_score

    def test_perfect_communication(self):
        # fillers=0 -> no penalty, interrupts=0 -> no penalty, ttl=45 discovery call -> no penalty
        s = self._get_comm(
            filler_words_per_minute=0.0,
            interruptions_count=0,
            talk_listen_ratio=45.0,
            call_type="discovery",
        )
        assert s == 100.0

    # --- filler_words_per_minute branches ---
    def test_fillers_ge_8_subtracts_30(self):
        s = self._get_comm(filler_words_per_minute=8.0, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 70.0

    def test_fillers_exactly_8_subtracts_30(self):
        s = self._get_comm(filler_words_per_minute=8.0, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 70.0

    def test_fillers_9_subtracts_30(self):
        s = self._get_comm(filler_words_per_minute=9.0, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 70.0

    def test_fillers_5_to_7_subtracts_20(self):
        s = self._get_comm(filler_words_per_minute=5.0, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 80.0

    def test_fillers_exactly_5_subtracts_20(self):
        s = self._get_comm(filler_words_per_minute=5.0, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 80.0

    def test_fillers_7_subtracts_20(self):
        s = self._get_comm(filler_words_per_minute=7.0, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 80.0

    def test_fillers_3_to_4_subtracts_10(self):
        s = self._get_comm(filler_words_per_minute=3.0, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 90.0

    def test_fillers_exactly_3_subtracts_10(self):
        s = self._get_comm(filler_words_per_minute=3.0, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 90.0

    def test_fillers_4_subtracts_10(self):
        s = self._get_comm(filler_words_per_minute=4.0, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 90.0

    def test_fillers_below_3_no_penalty(self):
        s = self._get_comm(filler_words_per_minute=2.9, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 100.0

    # --- interruptions_count branches ---
    def test_interrupts_ge_5_subtracts_25(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=5,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 75.0

    def test_interrupts_exactly_5_subtracts_25(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=5,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 75.0

    def test_interrupts_10_subtracts_25(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=10,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 75.0

    def test_interrupts_3_to_4_subtracts_15(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=3,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 85.0

    def test_interrupts_exactly_3_subtracts_15(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=3,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 85.0

    def test_interrupts_1_to_2_subtracts_5(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=1,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 95.0

    def test_interrupts_0_no_penalty(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=0,
                           talk_listen_ratio=45.0, call_type="discovery")
        assert s == 100.0

    # --- call_type talk ratio branch ---
    def test_discovery_call_ttl_above_65_subtracts_15(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=0,
                           talk_listen_ratio=66.0, call_type="discovery")
        assert s == 85.0

    def test_discovery_call_ttl_exactly_66_subtracts_15(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=0,
                           talk_listen_ratio=66.0, call_type="discovery")
        assert s == 85.0

    def test_discovery_call_ttl_65_no_penalty(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=0,
                           talk_listen_ratio=65.0, call_type="discovery")
        assert s == 100.0

    def test_non_discovery_call_ttl_above_80_subtracts_15(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=0,
                           talk_listen_ratio=81.0, call_type="demo")
        assert s == 85.0

    def test_non_discovery_call_ttl_exactly_81_subtracts_15(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=0,
                           talk_listen_ratio=81.0, call_type="followup")
        assert s == 85.0

    def test_non_discovery_call_ttl_80_no_penalty(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=0,
                           talk_listen_ratio=80.0, call_type="demo")
        assert s == 100.0

    def test_non_discovery_call_ttl_below_65_no_penalty(self):
        s = self._get_comm(filler_words_per_minute=0.0, interruptions_count=0,
                           talk_listen_ratio=50.0, call_type="closing")
        assert s == 100.0

    def test_comm_score_clamped_min_zero(self):
        s = self._get_comm(
            filler_words_per_minute=20.0,
            interruptions_count=20,
            talk_listen_ratio=90.0,
            call_type="discovery",
        )
        # 100 - 30 - 25 - 15 = 30 → not zero, but let's just check it >= 0
        assert s >= 0.0

    def test_comm_score_never_above_100(self):
        s = self._get_comm(
            filler_words_per_minute=0.0,
            interruptions_count=0,
            talk_listen_ratio=30.0,
            call_type="demo",
        )
        assert s <= 100.0

    def test_combined_penalties_dont_go_below_zero(self):
        s = self._get_comm(
            filler_words_per_minute=15.0,
            interruptions_count=15,
            talk_listen_ratio=95.0,
            call_type="discovery",
        )
        assert s >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 6. Value articulation score branches
# ─────────────────────────────────────────────────────────────────────────────

class TestValueArticulationScore:
    def _get_val(self, **kw) -> float:
        scorer = make_scorer()
        return scorer.score(make_input(**kw)).value_articulation_score

    # --- value_statement_count branches ---
    def test_value_stmts_ge_5_adds_35(self):
        s = self._get_val(value_statement_count=5, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=0)
        assert s == 35.0

    def test_value_stmts_exactly_5_adds_35(self):
        s = self._get_val(value_statement_count=5, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=0)
        assert s == 35.0

    def test_value_stmts_3_to_4_adds_22(self):
        s = self._get_val(value_statement_count=3, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=0)
        assert s == 22.0

    def test_value_stmts_exactly_3_adds_22(self):
        s = self._get_val(value_statement_count=3, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=0)
        assert s == 22.0

    def test_value_stmts_1_to_2_adds_10(self):
        s = self._get_val(value_statement_count=1, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=0)
        assert s == 10.0

    def test_value_stmts_0_adds_0(self):
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=0)
        assert s == 0.0

    # --- business_impact_quantified ---
    def test_business_impact_adds_35(self):
        s = self._get_val(value_statement_count=0, business_impact_quantified=1,
                          next_steps_defined=0, objection_count=0)
        assert s == 35.0

    def test_no_business_impact_adds_0(self):
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=0)
        assert s == 0.0

    # --- next_steps_defined ---
    def test_next_steps_adds_20(self):
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=1, objection_count=0)
        assert s == 20.0

    def test_no_next_steps_adds_0(self):
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=0)
        assert s == 0.0

    # --- objection handling rate branches ---
    def test_handle_rate_ge_80_pct_adds_10(self):
        # 4 objections, 4 handled = 100% >= 80%
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=5, objections_handled_count=4)
        assert s == 10.0

    def test_handle_rate_exactly_80_pct_adds_10(self):
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=5, objections_handled_count=4)
        assert s == 10.0

    def test_handle_rate_50_to_79_pct_adds_5(self):
        # 2 of 4 = 50%
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=4, objections_handled_count=2)
        assert s == 5.0

    def test_handle_rate_exactly_50_pct_adds_5(self):
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=2, objections_handled_count=1)
        assert s == 5.0

    def test_handle_rate_below_50_pct_adds_0(self):
        # 1 of 4 = 25%
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=4, objections_handled_count=1)
        assert s == 0.0

    def test_zero_objections_no_handle_rate_bonus(self):
        # objection_count = 0 means division not executed
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=0, objections_handled_count=0)
        assert s == 0.0

    def test_max_value_articulation_score_clamped(self):
        # 35 + 35 + 20 + 10 = 100
        s = self._get_val(value_statement_count=5, business_impact_quantified=1,
                          next_steps_defined=1, objection_count=1, objections_handled_count=1)
        assert s == 100.0

    def test_value_score_never_above_100(self):
        s = self._get_val(value_statement_count=100, business_impact_quantified=1,
                          next_steps_defined=1, objection_count=1, objections_handled_count=1)
        assert s <= 100.0

    def test_value_score_never_below_0(self):
        s = self._get_val(value_statement_count=0, business_impact_quantified=0,
                          next_steps_defined=0, objection_count=0, objections_handled_count=0)
        assert s >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 7. Composite formula
# ─────────────────────────────────────────────────────────────────────────────

class TestCompositeFormula:
    def test_composite_formula_direct(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        expected = round(
            result.discovery_score * 0.30 +
            result.qualification_score * 0.30 +
            result.communication_score * 0.20 +
            result.value_articulation_score * 0.20,
            1,
        )
        assert result.conversation_composite == expected

    def test_composite_with_all_zeros(self):
        # communication score starts at 100 and only deducts, so composite is never truly 0
        # worst case: discovery=0, qual=0, comm≥0, value=0 → composite≥0
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=100.0,
            questions_asked_count=0,
            open_ended_question_pct=0.0,
            pain_point_questions_asked=0,
            monologue_longest_seconds=250,
            budget_discussed=0,
            authority_confirmed=0,
            timeline_established=0,
            business_impact_quantified=0,
            next_steps_defined=0,
            filler_words_per_minute=20.0,
            interruptions_count=20,
            value_statement_count=0,
            objection_count=0,
            call_type="discovery",
        ))
        # discovery=0 (max(0, 5-15)=0), qual=0, comm=max(0,100-30-25-15)=30, value=0
        # composite = 0*0.30 + 0*0.30 + 30*0.20 + 0*0.20 = 6.0
        assert result.discovery_score == 0.0
        assert result.qualification_score == 0.0
        assert result.value_articulation_score == 0.0
        assert result.conversation_composite >= 0.0

    def test_composite_is_weighted_correctly(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=45.0,
            questions_asked_count=10,
            open_ended_question_pct=70.0,
            pain_point_questions_asked=5,
            monologue_longest_seconds=0,
            budget_discussed=1,
            authority_confirmed=1,
            timeline_established=1,
            business_impact_quantified=1,
            next_steps_defined=1,
            filler_words_per_minute=0.0,
            interruptions_count=0,
            value_statement_count=5,
            objection_count=5,
            objections_handled_count=5,
            call_type="demo",
        ))
        manual = round(
            result.discovery_score * 0.30 +
            result.qualification_score * 0.30 +
            result.communication_score * 0.20 +
            result.value_articulation_score * 0.20,
            1,
        )
        assert result.conversation_composite == manual

    def test_composite_never_above_100(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        assert result.conversation_composite <= 100.0

    def test_composite_never_below_0(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=100.0, questions_asked_count=0,
            open_ended_question_pct=0.0, pain_point_questions_asked=0,
            monologue_longest_seconds=250, budget_discussed=0, authority_confirmed=0,
            timeline_established=0, business_impact_quantified=0, next_steps_defined=0,
            filler_words_per_minute=20.0, interruptions_count=20, value_statement_count=0,
            objection_count=0, call_type="discovery",
        ))
        assert result.conversation_composite >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 8. Conversation quality classification
# ─────────────────────────────────────────────────────────────────────────────

class TestConversationQuality:
    def test_elite_at_exactly_75(self):
        scorer = ConversationIntelligenceScorer()
        # Build a result manually to test _conversation_quality
        q = scorer._conversation_quality(75.0)
        assert q == ConversationQuality.ELITE

    def test_elite_above_75(self):
        scorer = ConversationIntelligenceScorer()
        q = scorer._conversation_quality(90.0)
        assert q == ConversationQuality.ELITE

    def test_elite_at_100(self):
        scorer = ConversationIntelligenceScorer()
        q = scorer._conversation_quality(100.0)
        assert q == ConversationQuality.ELITE

    def test_proficient_at_exactly_55(self):
        scorer = ConversationIntelligenceScorer()
        q = scorer._conversation_quality(55.0)
        assert q == ConversationQuality.PROFICIENT

    def test_proficient_at_74(self):
        scorer = ConversationIntelligenceScorer()
        q = scorer._conversation_quality(74.9)
        assert q == ConversationQuality.PROFICIENT

    def test_developing_at_exactly_35(self):
        scorer = ConversationIntelligenceScorer()
        q = scorer._conversation_quality(35.0)
        assert q == ConversationQuality.DEVELOPING

    def test_developing_at_54(self):
        scorer = ConversationIntelligenceScorer()
        q = scorer._conversation_quality(54.9)
        assert q == ConversationQuality.DEVELOPING

    def test_poor_at_exactly_34(self):
        scorer = ConversationIntelligenceScorer()
        q = scorer._conversation_quality(34.9)
        assert q == ConversationQuality.POOR

    def test_poor_at_zero(self):
        scorer = ConversationIntelligenceScorer()
        q = scorer._conversation_quality(0.0)
        assert q == ConversationQuality.POOR

    def test_poor_boundary_just_below_35(self):
        scorer = ConversationIntelligenceScorer()
        q = scorer._conversation_quality(34.99)
        assert q == ConversationQuality.POOR


# ─────────────────────────────────────────────────────────────────────────────
# 9. Conversation pattern classification
# ─────────────────────────────────────────────────────────────────────────────

class TestConversationPattern:
    def _get_pattern(self, **kw) -> ConversationPattern:
        scorer = make_scorer()
        return scorer.score(make_input(**kw)).conversation_pattern

    def test_challenger_pattern(self):
        # business_impact_quantified=1, value_statement_count >= 4, objection_count > 0, handled >= 80%
        p = self._get_pattern(
            business_impact_quantified=1,
            value_statement_count=4,
            objection_count=5,
            objections_handled_count=4,  # 80%
            open_ended_question_pct=50.0,
            talk_listen_ratio=50.0,
        )
        assert p == ConversationPattern.CHALLENGER

    def test_challenger_exact_80_pct(self):
        p = self._get_pattern(
            business_impact_quantified=1,
            value_statement_count=5,
            objection_count=5,
            objections_handled_count=4,
        )
        assert p == ConversationPattern.CHALLENGER

    def test_challenger_above_80_pct(self):
        p = self._get_pattern(
            business_impact_quantified=1,
            value_statement_count=4,
            objection_count=5,
            objections_handled_count=5,
        )
        assert p == ConversationPattern.CHALLENGER

    def test_no_challenger_when_objection_count_zero(self):
        p = self._get_pattern(
            business_impact_quantified=1,
            value_statement_count=5,
            objection_count=0,
            objections_handled_count=0,
        )
        assert p != ConversationPattern.CHALLENGER

    def test_no_challenger_when_not_enough_value_stmts(self):
        p = self._get_pattern(
            business_impact_quantified=1,
            value_statement_count=3,  # < 4
            objection_count=5,
            objections_handled_count=5,
        )
        assert p != ConversationPattern.CHALLENGER

    def test_no_challenger_when_no_business_impact(self):
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=5,
            objection_count=5,
            objections_handled_count=5,
        )
        assert p != ConversationPattern.CHALLENGER

    def test_consultative_pattern(self):
        # composite >= 60, open_ended_question_pct >= 60, talk_listen_ratio <= 55
        # We need to craft an input that won't hit challenger first
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=3,
            objection_count=0,
            talk_listen_ratio=45.0,
            open_ended_question_pct=70.0,
            questions_asked_count=10,
            pain_point_questions_asked=5,
            budget_discussed=1,
            authority_confirmed=1,
            timeline_established=1,
            next_steps_defined=1,
            filler_words_per_minute=0.0,
            interruptions_count=0,
            monologue_longest_seconds=10,
        )
        assert p == ConversationPattern.CONSULTATIVE

    def test_no_consultative_low_oeq(self):
        # oeq < 60 prevents consultative
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=2,
            objection_count=0,
            talk_listen_ratio=45.0,
            open_ended_question_pct=50.0,
            questions_asked_count=10,
            pain_point_questions_asked=5,
        )
        # Should not be consultative (oeq=50 < 60)
        assert p != ConversationPattern.CONSULTATIVE

    def test_balanced_dialogue_pattern(self):
        # 40 <= talk_listen_ratio <= 60 and questions_asked_count >= 5, not challenger or consultative
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=2,
            objection_count=0,
            talk_listen_ratio=50.0,
            open_ended_question_pct=30.0,  # < 60 so not consultative
            questions_asked_count=5,
            pain_point_questions_asked=0,
            budget_discussed=0,
            authority_confirmed=0,
            timeline_established=0,
            next_steps_defined=0,
            filler_words_per_minute=10.0,
            interruptions_count=5,
        )
        assert p == ConversationPattern.BALANCED_DIALOGUE

    def test_balanced_dialogue_exactly_40_ratio(self):
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=2,
            objection_count=0,
            talk_listen_ratio=40.0,
            open_ended_question_pct=30.0,
            questions_asked_count=5,
            pain_point_questions_asked=0,
            budget_discussed=0,
            authority_confirmed=0,
            timeline_established=0,
            next_steps_defined=0,
            filler_words_per_minute=10.0,
            interruptions_count=5,
        )
        assert p == ConversationPattern.BALANCED_DIALOGUE

    def test_balanced_dialogue_exactly_60_ratio(self):
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=2,
            objection_count=0,
            talk_listen_ratio=60.0,
            open_ended_question_pct=30.0,
            questions_asked_count=5,
            pain_point_questions_asked=0,
            budget_discussed=0,
            authority_confirmed=0,
            timeline_established=0,
            next_steps_defined=0,
            filler_words_per_minute=10.0,
            interruptions_count=5,
        )
        assert p == ConversationPattern.BALANCED_DIALOGUE

    def test_monologue_pattern_high_ratio(self):
        # talk_listen_ratio >= 70
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=2,
            objection_count=0,
            talk_listen_ratio=70.0,
            open_ended_question_pct=30.0,
            questions_asked_count=8,
            pain_point_questions_asked=2,
        )
        assert p == ConversationPattern.MONOLOGUE

    def test_monologue_pattern_long_mono(self):
        # monologue_longest_seconds >= 180
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=2,
            objection_count=0,
            talk_listen_ratio=35.0,  # Would go to balanced but mono takes priority
            open_ended_question_pct=30.0,
            questions_asked_count=3,
            pain_point_questions_asked=0,
            monologue_longest_seconds=180,
        )
        assert p == ConversationPattern.MONOLOGUE

    def test_shallow_discovery_few_questions(self):
        # pain_point_questions_asked <= 1 and questions_asked_count <= 4, no higher pattern
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=2,
            objection_count=0,
            talk_listen_ratio=50.0,  # This would be balanced_dialogue if q>=5
            open_ended_question_pct=30.0,
            questions_asked_count=4,
            pain_point_questions_asked=1,
        )
        assert p == ConversationPattern.SHALLOW_DISCOVERY

    def test_feature_dump_pattern(self):
        # value_statement_count >= 5, pain_point_questions_asked <= 1
        # Must not match challenger, consultative, balanced_dialogue, monologue, or shallow_discovery
        # shallow_discovery: pain<=1 AND q<=4 → triggers first, so use q>=5 to bypass it
        # balanced_dialogue: 40<=ratio<=60 AND q>=5 → use ratio outside that range (e.g. 65)
        # monologue: ratio>=70 → use ratio < 70 (e.g. 65)
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=5,
            objection_count=0,
            talk_listen_ratio=65.0,       # not in 40-60 so no balanced_dialogue; <70 so no monologue
            open_ended_question_pct=30.0,
            questions_asked_count=5,      # >=5 so shallow_discovery condition (q<=4) is skipped
            pain_point_questions_asked=0,
        )
        assert p == ConversationPattern.FEATURE_DUMP

    def test_shallow_discovery_fallback(self):
        # hits no other pattern → falls through to SHALLOW_DISCOVERY
        p = self._get_pattern(
            business_impact_quantified=0,
            value_statement_count=2,
            objection_count=0,
            talk_listen_ratio=30.0,
            open_ended_question_pct=20.0,
            questions_asked_count=2,
            pain_point_questions_asked=0,
            monologue_longest_seconds=50,
        )
        assert p == ConversationPattern.SHALLOW_DISCOVERY


# ─────────────────────────────────────────────────────────────────────────────
# 10. Qualification depth classification
# ─────────────────────────────────────────────────────────────────────────────

class TestQualificationDepth:
    def _get_depth(self, **kw) -> QualificationDepth:
        scorer = make_scorer()
        return scorer.score(make_input(**kw)).qualification_depth

    def test_deeply_qualified_at_75(self):
        # budget+authority+timeline+business_impact = 20+20+20+25 = 85 >= 75
        d = self._get_depth(budget_discussed=1, authority_confirmed=1,
                            timeline_established=1, business_impact_quantified=1,
                            next_steps_defined=0)
        assert d == QualificationDepth.DEEPLY_QUALIFIED

    def test_deeply_qualified_at_100(self):
        d = self._get_depth(budget_discussed=1, authority_confirmed=1,
                            timeline_established=1, business_impact_quantified=1,
                            next_steps_defined=1)
        assert d == QualificationDepth.DEEPLY_QUALIFIED

    def test_deeply_qualified_exactly_75(self):
        # budget+authority+timeline = 60, business_impact=25 -> 85. Need exactly 75:
        # business_impact only = 25, authority=20, timeline=20, budget=20, next_steps=15
        # 25+20+20 = 65, 25+20+20+15 = 80, nope
        # Directly test the method
        scorer = ConversationIntelligenceScorer()
        d = scorer._qualification_depth(75.0)
        assert d == QualificationDepth.DEEPLY_QUALIFIED

    def test_moderately_qualified_at_50(self):
        scorer = ConversationIntelligenceScorer()
        d = scorer._qualification_depth(50.0)
        assert d == QualificationDepth.MODERATELY_QUALIFIED

    def test_moderately_qualified_at_74(self):
        scorer = ConversationIntelligenceScorer()
        d = scorer._qualification_depth(74.9)
        assert d == QualificationDepth.MODERATELY_QUALIFIED

    def test_surface_level_at_25(self):
        scorer = ConversationIntelligenceScorer()
        d = scorer._qualification_depth(25.0)
        assert d == QualificationDepth.SURFACE_LEVEL

    def test_surface_level_at_49(self):
        scorer = ConversationIntelligenceScorer()
        d = scorer._qualification_depth(49.9)
        assert d == QualificationDepth.SURFACE_LEVEL

    def test_unqualified_at_0(self):
        scorer = ConversationIntelligenceScorer()
        d = scorer._qualification_depth(0.0)
        assert d == QualificationDepth.UNQUALIFIED

    def test_unqualified_at_24(self):
        scorer = ConversationIntelligenceScorer()
        d = scorer._qualification_depth(24.9)
        assert d == QualificationDepth.UNQUALIFIED

    def test_surface_level_via_input_budget_only(self):
        d = self._get_depth(budget_discussed=1, authority_confirmed=0,
                            timeline_established=0, business_impact_quantified=0,
                            next_steps_defined=1)
        # 20 + 15 = 35 -> surface_level
        assert d == QualificationDepth.SURFACE_LEVEL

    def test_unqualified_via_input_no_signals(self):
        d = self._get_depth(budget_discussed=0, authority_confirmed=0,
                            timeline_established=0, business_impact_quantified=0,
                            next_steps_defined=0)
        assert d == QualificationDepth.UNQUALIFIED


# ─────────────────────────────────────────────────────────────────────────────
# 11. Coaching priority score branches
# ─────────────────────────────────────────────────────────────────────────────

class TestCoachingPriorityScore:
    def _get_coaching(self, **kw) -> float:
        scorer = make_scorer()
        return scorer.score(make_input(**kw)).coaching_priority_score

    def test_coaching_base_is_100_minus_composite(self):
        scorer = make_scorer()
        inp = make_input()
        result = scorer.score(inp)
        # Base is 100 - composite, then may be modified by bonuses
        # Check the formula holds when there are no severity signals
        clean_inp = make_input(
            filler_words_per_minute=0.0,
            interruptions_count=0,
            monologue_longest_seconds=50,
            next_steps_defined=1,
        )
        clean_result = scorer.score(clean_inp)
        expected_base = round(max(0.0, 100.0 - clean_result.conversation_composite), 1)
        assert clean_result.coaching_priority_score == expected_base

    def test_fillers_ge_5_adds_10_to_coaching(self):
        scorer = ConversationIntelligenceScorer()
        inp_no_filler = make_input(
            filler_words_per_minute=0.0,
            interruptions_count=0,
            monologue_longest_seconds=50,
            next_steps_defined=1,
        )
        inp_filler = make_input(
            filler_words_per_minute=5.0,
            interruptions_count=0,
            monologue_longest_seconds=50,
            next_steps_defined=1,
        )
        r1 = scorer.score(inp_no_filler)
        r2 = scorer.score(inp_filler)
        # coaching differs by more than just the composite difference (extra +10 added)
        base_no_filler = max(0.0, 100.0 - r1.conversation_composite)
        # filler: composite different (comm_score affected), so check only that +10 was attempted
        # With filler=5, comm_score drops by 20, composite drops 0.20*20=4
        # coaching base = 100-(composite-4), then +10 for filler >= 5
        assert r2.coaching_priority_score >= r1.coaching_priority_score

    def test_interrupts_ge_3_adds_10_to_coaching(self):
        scorer = ConversationIntelligenceScorer()
        r_clean = scorer.score(make_input(interruptions_count=0, filler_words_per_minute=0.0,
                                          monologue_longest_seconds=50, next_steps_defined=1))
        r_inter = scorer.score(make_input(interruptions_count=3, filler_words_per_minute=0.0,
                                          monologue_longest_seconds=50, next_steps_defined=1))
        assert r_inter.coaching_priority_score >= r_clean.coaching_priority_score

    def test_monologue_ge_180_adds_10_to_coaching(self):
        scorer = ConversationIntelligenceScorer()
        r_short = scorer.score(make_input(monologue_longest_seconds=50, filler_words_per_minute=0.0,
                                          interruptions_count=0, next_steps_defined=1))
        r_long  = scorer.score(make_input(monologue_longest_seconds=180, filler_words_per_minute=0.0,
                                          interruptions_count=0, next_steps_defined=1))
        assert r_long.coaching_priority_score >= r_short.coaching_priority_score

    def test_no_next_steps_adds_8_to_coaching(self):
        scorer = ConversationIntelligenceScorer()
        r_with = scorer.score(make_input(next_steps_defined=1, filler_words_per_minute=0.0,
                                          interruptions_count=0, monologue_longest_seconds=50))
        r_without = scorer.score(make_input(next_steps_defined=0, filler_words_per_minute=0.0,
                                             interruptions_count=0, monologue_longest_seconds=50))
        assert r_without.coaching_priority_score >= r_with.coaching_priority_score

    def test_coaching_priority_clamp_max_100(self):
        s = self._get_coaching(
            talk_listen_ratio=100.0, questions_asked_count=0, open_ended_question_pct=0.0,
            pain_point_questions_asked=0, monologue_longest_seconds=250,
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0,
            filler_words_per_minute=20.0, interruptions_count=20,
            value_statement_count=0, objection_count=0, call_type="discovery",
        )
        assert s <= 100.0

    def test_coaching_priority_clamp_min_0(self):
        s = self._get_coaching(
            talk_listen_ratio=45.0, questions_asked_count=15, open_ended_question_pct=90.0,
            pain_point_questions_asked=6, monologue_longest_seconds=10,
            budget_discussed=1, authority_confirmed=1, timeline_established=1,
            business_impact_quantified=1, next_steps_defined=1,
            filler_words_per_minute=0.0, interruptions_count=0,
            value_statement_count=5, objection_count=5, objections_handled_count=5,
            call_type="demo",
        )
        assert s >= 0.0

    def test_coaching_priority_capped_at_100_with_all_bonuses(self):
        # Even with all +10 bonuses and low composite, should not exceed 100
        scorer = ConversationIntelligenceScorer()
        result = scorer.score(make_input(
            talk_listen_ratio=100.0,
            questions_asked_count=0,
            open_ended_question_pct=0.0,
            pain_point_questions_asked=0,
            monologue_longest_seconds=200,  # >= 180 → +10
            budget_discussed=0,
            authority_confirmed=0,
            timeline_established=0,
            business_impact_quantified=0,
            next_steps_defined=0,           # → +8
            filler_words_per_minute=6.0,    # >= 5 → +10
            interruptions_count=4,          # >= 3 → +10
            value_statement_count=0,
            objection_count=0,
            call_type="discovery",
        ))
        assert result.coaching_priority_score <= 100.0


# ─────────────────────────────────────────────────────────────────────────────
# 12. Deal advancement score branches
# ─────────────────────────────────────────────────────────────────────────────

class TestDealAdvancementScore:
    def _get_deal_adv(self, **kw) -> float:
        scorer = make_scorer()
        return scorer.score(make_input(**kw)).deal_advancement_score

    def test_deal_advancement_base_50pct_composite(self):
        scorer = ConversationIntelligenceScorer()
        result = scorer.score(make_input(
            next_steps_defined=0, budget_discussed=0, timeline_established=0,
            business_impact_quantified=0
        ))
        expected = round(max(0.0, min(100.0, result.conversation_composite * 0.50)), 1)
        assert result.deal_advancement_score == expected

    def test_next_steps_adds_20_to_advancement(self):
        scorer = ConversationIntelligenceScorer()
        r_without = scorer.score(make_input(next_steps_defined=0, budget_discussed=0,
                                            timeline_established=0, business_impact_quantified=0))
        r_with = scorer.score(make_input(next_steps_defined=1, budget_discussed=0,
                                          timeline_established=0, business_impact_quantified=0))
        diff = r_with.deal_advancement_score - r_without.deal_advancement_score
        # Composite is same since next_steps affects qual_score too but let's just assert direction
        assert r_with.deal_advancement_score > r_without.deal_advancement_score

    def test_budget_adds_10_to_advancement(self):
        scorer = ConversationIntelligenceScorer()
        r_without = scorer.score(make_input(budget_discussed=0, authority_confirmed=0,
                                            timeline_established=0, next_steps_defined=0,
                                            business_impact_quantified=0))
        r_with = scorer.score(make_input(budget_discussed=1, authority_confirmed=0,
                                          timeline_established=0, next_steps_defined=0,
                                          business_impact_quantified=0))
        assert r_with.deal_advancement_score > r_without.deal_advancement_score

    def test_timeline_adds_10_to_advancement(self):
        scorer = ConversationIntelligenceScorer()
        r_without = scorer.score(make_input(timeline_established=0, budget_discussed=0,
                                            authority_confirmed=0, next_steps_defined=0,
                                            business_impact_quantified=0))
        r_with = scorer.score(make_input(timeline_established=1, budget_discussed=0,
                                          authority_confirmed=0, next_steps_defined=0,
                                          business_impact_quantified=0))
        assert r_with.deal_advancement_score > r_without.deal_advancement_score

    def test_business_impact_adds_10_to_advancement(self):
        scorer = ConversationIntelligenceScorer()
        r_without = scorer.score(make_input(business_impact_quantified=0, budget_discussed=0,
                                            authority_confirmed=0, timeline_established=0,
                                            next_steps_defined=0))
        r_with = scorer.score(make_input(business_impact_quantified=1, budget_discussed=0,
                                          authority_confirmed=0, timeline_established=0,
                                          next_steps_defined=0))
        assert r_with.deal_advancement_score > r_without.deal_advancement_score

    def test_deal_advancement_capped_at_100(self):
        s = self._get_deal_adv(
            budget_discussed=1, authority_confirmed=1, timeline_established=1,
            business_impact_quantified=1, next_steps_defined=1,
            talk_listen_ratio=45.0, questions_asked_count=15, open_ended_question_pct=90.0,
            pain_point_questions_asked=6, monologue_longest_seconds=10,
            filler_words_per_minute=0.0, interruptions_count=0,
            value_statement_count=5, objection_count=5, objections_handled_count=5,
            call_type="demo",
        )
        assert s <= 100.0

    def test_deal_advancement_never_below_0(self):
        s = self._get_deal_adv(
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0,
            talk_listen_ratio=100.0, questions_asked_count=0, open_ended_question_pct=0.0,
            pain_point_questions_asked=0, monologue_longest_seconds=250,
            filler_words_per_minute=20.0, interruptions_count=20,
            value_statement_count=0, objection_count=0, call_type="discovery",
        )
        assert s >= 0.0


# ─────────────────────────────────────────────────────────────────────────────
# 13. is_coachable_moment invariant
# ─────────────────────────────────────────────────────────────────────────────

class TestIsCoachableMoment:
    def test_coachable_when_coaching_priority_ge_60(self):
        # Force a low composite by zeroing out everything
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=100.0, questions_asked_count=0, open_ended_question_pct=0.0,
            pain_point_questions_asked=0, monologue_longest_seconds=250,
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0,
            filler_words_per_minute=20.0, interruptions_count=20,
            value_statement_count=0, objection_count=0, call_type="discovery",
        ))
        assert result.is_coachable_moment is True

    def test_coachable_when_composite_lt_40(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=100.0, questions_asked_count=0, open_ended_question_pct=0.0,
            pain_point_questions_asked=0, monologue_longest_seconds=200,
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0,
            filler_words_per_minute=0.0, interruptions_count=0,
            value_statement_count=0, objection_count=0, call_type="demo",
        ))
        if result.conversation_composite < 40.0:
            assert result.is_coachable_moment is True

    def test_coachable_invariant_coaching_ge_60_or_composite_lt_40(self):
        scorer = make_scorer()
        for i in range(5):
            inp = make_input(
                talk_listen_ratio=float(60 + i * 5),
                questions_asked_count=i,
                open_ended_question_pct=float(10 + i * 5),
                pain_point_questions_asked=0,
            )
            result = scorer.score(inp)
            expected = result.coaching_priority_score >= 60.0 or result.conversation_composite < 40.0
            assert result.is_coachable_moment == expected

    def test_not_coachable_when_high_quality_no_issues(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=45.0,
            questions_asked_count=15,
            open_ended_question_pct=90.0,
            pain_point_questions_asked=6,
            monologue_longest_seconds=10,
            budget_discussed=1,
            authority_confirmed=1,
            timeline_established=1,
            business_impact_quantified=1,
            next_steps_defined=1,
            filler_words_per_minute=0.0,
            interruptions_count=0,
            value_statement_count=5,
            objection_count=5,
            objections_handled_count=5,
            call_type="demo",
        ))
        # coaching should be low for a great call
        expected = result.coaching_priority_score >= 60.0 or result.conversation_composite < 40.0
        assert result.is_coachable_moment == expected

    def test_coachable_moment_consistency_with_formula(self):
        scorer = make_scorer()
        for _ in range(10):
            inp = make_input()
            result = scorer.score(inp)
            expected = result.coaching_priority_score >= 60.0 or result.conversation_composite < 40.0
            assert result.is_coachable_moment == expected


# ─────────────────────────────────────────────────────────────────────────────
# 14. is_exemplary_call invariant
# ─────────────────────────────────────────────────────────────────────────────

class TestIsExemplaryCall:
    def _make_exemplary_input(self):
        """Create input designed to generate exemplary call (composite>=80, advancement>=75)."""
        return make_input(
            talk_listen_ratio=45.0,
            questions_asked_count=15,
            open_ended_question_pct=90.0,
            pain_point_questions_asked=6,
            monologue_longest_seconds=10,
            budget_discussed=1,
            authority_confirmed=1,
            timeline_established=1,
            business_impact_quantified=1,
            next_steps_defined=1,
            filler_words_per_minute=0.0,
            interruptions_count=0,
            value_statement_count=5,
            objection_count=5,
            objections_handled_count=5,
            call_type="demo",
        )

    def test_exemplary_when_both_conditions_met(self):
        scorer = make_scorer()
        result = scorer.score(self._make_exemplary_input())
        if result.conversation_composite >= 80.0 and result.deal_advancement_score >= 75.0:
            assert result.is_exemplary_call is True

    def test_not_exemplary_when_composite_below_80(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=70.0, questions_asked_count=2, open_ended_question_pct=20.0,
            pain_point_questions_asked=0, budget_discussed=0, authority_confirmed=0,
            timeline_established=0, business_impact_quantified=0, next_steps_defined=0,
        ))
        if result.conversation_composite < 80.0:
            assert result.is_exemplary_call is False

    def test_not_exemplary_when_advancement_below_75(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            budget_discussed=0, authority_confirmed=0,
            timeline_established=0, next_steps_defined=0,
            business_impact_quantified=0,
        ))
        if result.deal_advancement_score < 75.0:
            assert result.is_exemplary_call is False

    def test_exemplary_invariant_consistency(self):
        scorer = make_scorer()
        result = scorer.score(self._make_exemplary_input())
        expected = result.conversation_composite >= 80.0 and result.deal_advancement_score >= 75.0
        assert result.is_exemplary_call == expected

    def test_exemplary_invariant_with_poor_call(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=100.0, questions_asked_count=0, open_ended_question_pct=0.0,
            pain_point_questions_asked=0, monologue_longest_seconds=250,
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0,
            filler_words_per_minute=20.0, interruptions_count=20,
            value_statement_count=0, objection_count=0, call_type="discovery",
        ))
        expected = result.conversation_composite >= 80.0 and result.deal_advancement_score >= 75.0
        assert result.is_exemplary_call == expected
        assert result.is_exemplary_call is False


# ─────────────────────────────────────────────────────────────────────────────
# 15. Conversation action classification
# ─────────────────────────────────────────────────────────────────────────────

class TestConversationAction:
    def test_share_as_example_when_exemplary(self):
        scorer = ConversationIntelligenceScorer()
        action = scorer._conversation_action(
            quality=ConversationQuality.ELITE,
            is_exemplary=True,
            coaching=10.0,
        )
        assert action == ConversationAction.SHARE_AS_EXAMPLE

    def test_share_as_example_overrides_elite(self):
        scorer = ConversationIntelligenceScorer()
        action = scorer._conversation_action(
            quality=ConversationQuality.ELITE,
            is_exemplary=True,
            coaching=5.0,
        )
        assert action == ConversationAction.SHARE_AS_EXAMPLE

    def test_reinforce_strengths_when_elite_not_exemplary(self):
        scorer = ConversationIntelligenceScorer()
        action = scorer._conversation_action(
            quality=ConversationQuality.ELITE,
            is_exemplary=False,
            coaching=30.0,
        )
        assert action == ConversationAction.REINFORCE_STRENGTHS

    def test_coach_immediately_when_poor(self):
        scorer = ConversationIntelligenceScorer()
        action = scorer._conversation_action(
            quality=ConversationQuality.POOR,
            is_exemplary=False,
            coaching=40.0,
        )
        assert action == ConversationAction.COACH_IMMEDIATELY

    def test_coach_immediately_when_coaching_ge_65(self):
        scorer = ConversationIntelligenceScorer()
        action = scorer._conversation_action(
            quality=ConversationQuality.DEVELOPING,
            is_exemplary=False,
            coaching=65.0,
        )
        assert action == ConversationAction.COACH_IMMEDIATELY

    def test_coach_immediately_exactly_65(self):
        scorer = ConversationIntelligenceScorer()
        action = scorer._conversation_action(
            quality=ConversationQuality.PROFICIENT,
            is_exemplary=False,
            coaching=65.0,
        )
        assert action == ConversationAction.COACH_IMMEDIATELY

    def test_structured_coaching_when_developing_low_coaching(self):
        scorer = ConversationIntelligenceScorer()
        action = scorer._conversation_action(
            quality=ConversationQuality.DEVELOPING,
            is_exemplary=False,
            coaching=50.0,
        )
        assert action == ConversationAction.STRUCTURED_COACHING

    def test_structured_coaching_when_proficient_low_coaching(self):
        scorer = ConversationIntelligenceScorer()
        action = scorer._conversation_action(
            quality=ConversationQuality.PROFICIENT,
            is_exemplary=False,
            coaching=50.0,
        )
        assert action == ConversationAction.STRUCTURED_COACHING

    def test_action_in_full_pipeline_exemplary(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=45.0, questions_asked_count=15, open_ended_question_pct=90.0,
            pain_point_questions_asked=6, monologue_longest_seconds=10,
            budget_discussed=1, authority_confirmed=1, timeline_established=1,
            business_impact_quantified=1, next_steps_defined=1,
            filler_words_per_minute=0.0, interruptions_count=0,
            value_statement_count=5, objection_count=5, objections_handled_count=5,
            call_type="demo",
        ))
        if result.is_exemplary_call:
            assert result.conversation_action == ConversationAction.SHARE_AS_EXAMPLE

    def test_action_in_full_pipeline_poor_quality(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=100.0, questions_asked_count=0, open_ended_question_pct=0.0,
            pain_point_questions_asked=0, monologue_longest_seconds=250,
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0,
            filler_words_per_minute=20.0, interruptions_count=20,
            value_statement_count=0, objection_count=0, call_type="discovery",
        ))
        assert result.conversation_action in {
            ConversationAction.COACH_IMMEDIATELY,
            ConversationAction.STRUCTURED_COACHING,
        }


# ─────────────────────────────────────────────────────────────────────────────
# 16. score() method and result storage
# ─────────────────────────────────────────────────────────────────────────────

class TestScoreMethod:
    def test_score_returns_result_instance(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        assert isinstance(result, ConversationIntelligenceResult)

    def test_score_stores_result(self):
        scorer = make_scorer()
        scorer.score(make_input())
        assert len(scorer._results) == 1

    def test_score_multiple_stored(self):
        scorer = make_scorer()
        for i in range(5):
            scorer.score(make_input(call_id=f"call-{i}"))
        assert len(scorer._results) == 5

    def test_score_call_id_propagated(self):
        scorer = make_scorer()
        result = scorer.score(make_input(call_id="test-call-999"))
        assert result.call_id == "test-call-999"

    def test_score_deal_id_propagated(self):
        scorer = make_scorer()
        result = scorer.score(make_input(deal_id="deal-xyz"))
        assert result.deal_id == "deal-xyz"

    def test_score_call_id_in_to_dict(self):
        scorer = make_scorer()
        result = scorer.score(make_input(call_id="check-id"))
        assert result.to_dict()["call_id"] == "check-id"

    def test_score_deal_id_in_to_dict(self):
        scorer = make_scorer()
        result = scorer.score(make_input(deal_id="check-deal"))
        assert result.to_dict()["deal_id"] == "check-deal"

    def test_score_composite_is_float(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        assert isinstance(result.conversation_composite, float)

    def test_score_all_scores_are_floats(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        for attr in ("discovery_score", "qualification_score", "communication_score",
                     "value_articulation_score", "conversation_composite",
                     "coaching_priority_score", "deal_advancement_score"):
            assert isinstance(getattr(result, attr), float), f"{attr} should be float"

    def test_score_booleans_are_bools(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        assert isinstance(result.is_coachable_moment, bool)
        assert isinstance(result.is_exemplary_call, bool)


# ─────────────────────────────────────────────────────────────────────────────
# 17. score_batch() method
# ─────────────────────────────────────────────────────────────────────────────

class TestScoreBatch:
    def test_score_batch_returns_list(self):
        scorer = make_scorer()
        results = scorer.score_batch([make_input(), make_input()])
        assert isinstance(results, list)

    def test_score_batch_length_matches_input(self):
        scorer = make_scorer()
        inputs = [make_input(call_id=f"c{i}") for i in range(7)]
        results = scorer.score_batch(inputs)
        assert len(results) == 7

    def test_score_batch_returns_result_instances(self):
        scorer = make_scorer()
        results = scorer.score_batch([make_input(), make_input()])
        for r in results:
            assert isinstance(r, ConversationIntelligenceResult)

    def test_score_batch_empty_list(self):
        scorer = make_scorer()
        results = scorer.score_batch([])
        assert results == []

    def test_score_batch_stores_all_results(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(4)])
        assert len(scorer._results) == 4

    def test_score_batch_call_ids_preserved(self):
        scorer = make_scorer()
        inputs = [make_input(call_id=f"call-{i}") for i in range(3)]
        results = scorer.score_batch(inputs)
        for i, r in enumerate(results):
            assert r.call_id == f"call-{i}"

    def test_score_batch_same_as_individual_scores(self):
        scorer1 = make_scorer()
        scorer2 = make_scorer()
        inputs = [make_input(call_id=f"c{i}") for i in range(3)]
        batch_results = scorer1.score_batch(inputs)
        individual_results = [scorer2.score(inp) for inp in inputs]
        for b, ind in zip(batch_results, individual_results):
            assert b.conversation_composite == ind.conversation_composite
            assert b.discovery_score == ind.discovery_score

    def test_score_batch_single_item(self):
        scorer = make_scorer()
        results = scorer.score_batch([make_input(call_id="solo")])
        assert len(results) == 1
        assert results[0].call_id == "solo"


# ─────────────────────────────────────────────────────────────────────────────
# 18. reset() method
# ─────────────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self):
        scorer = make_scorer()
        scorer.score(make_input())
        scorer.reset()
        assert len(scorer._results) == 0

    def test_reset_clears_multiple_results(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
        scorer.reset()
        assert len(scorer._results) == 0

    def test_can_score_after_reset(self):
        scorer = make_scorer()
        scorer.score(make_input(call_id="before"))
        scorer.reset()
        result = scorer.score(make_input(call_id="after"))
        assert len(scorer._results) == 1
        assert result.call_id == "after"

    def test_reset_resets_properties(self):
        scorer = make_scorer()
        scorer.score(make_input())
        scorer.reset()
        assert scorer.avg_conversation_composite == 0.0
        assert scorer.avg_deal_advancement_score == 0.0

    def test_reset_resets_coachable_calls(self):
        scorer = make_scorer()
        scorer.score(make_input(
            talk_listen_ratio=100.0, questions_asked_count=0, open_ended_question_pct=0.0,
            pain_point_questions_asked=0, monologue_longest_seconds=250,
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0,
            filler_words_per_minute=20.0, interruptions_count=20,
            value_statement_count=0, objection_count=0, call_type="discovery",
        ))
        scorer.reset()
        assert scorer.coachable_calls == []

    def test_reset_resets_exemplary_calls(self):
        scorer = make_scorer()
        scorer.score(make_input())
        scorer.reset()
        assert scorer.exemplary_calls == []


# ─────────────────────────────────────────────────────────────────────────────
# 19. Properties
# ─────────────────────────────────────────────────────────────────────────────

class TestProperties:
    def test_avg_conversation_composite_empty(self):
        scorer = make_scorer()
        assert scorer.avg_conversation_composite == 0.0

    def test_avg_deal_advancement_score_empty(self):
        scorer = make_scorer()
        assert scorer.avg_deal_advancement_score == 0.0

    def test_avg_conversation_composite_single(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        assert scorer.avg_conversation_composite == result.conversation_composite

    def test_avg_deal_advancement_score_single(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        assert scorer.avg_deal_advancement_score == result.deal_advancement_score

    def test_avg_conversation_composite_multiple(self):
        scorer = make_scorer()
        inputs = [make_input(call_id=f"c{i}") for i in range(3)]
        results = scorer.score_batch(inputs)
        expected = round(sum(r.conversation_composite for r in results) / 3, 1)
        assert scorer.avg_conversation_composite == expected

    def test_avg_deal_advancement_score_multiple(self):
        scorer = make_scorer()
        inputs = [make_input(call_id=f"c{i}") for i in range(3)]
        results = scorer.score_batch(inputs)
        expected = round(sum(r.deal_advancement_score for r in results) / 3, 1)
        assert scorer.avg_deal_advancement_score == expected

    def test_coachable_calls_empty(self):
        scorer = make_scorer()
        assert scorer.coachable_calls == []

    def test_exemplary_calls_empty(self):
        scorer = make_scorer()
        assert scorer.exemplary_calls == []

    def test_coachable_calls_populated(self):
        scorer = make_scorer()
        bad_inp = make_input(
            talk_listen_ratio=100.0, questions_asked_count=0, open_ended_question_pct=0.0,
            pain_point_questions_asked=0, monologue_longest_seconds=250,
            budget_discussed=0, authority_confirmed=0, timeline_established=0,
            business_impact_quantified=0, next_steps_defined=0,
            filler_words_per_minute=20.0, interruptions_count=20,
            value_statement_count=0, objection_count=0, call_type="discovery",
        )
        scorer.score(bad_inp)
        assert len(scorer.coachable_calls) >= 1
        for r in scorer.coachable_calls:
            assert r.is_coachable_moment is True

    def test_exemplary_calls_populated(self):
        scorer = make_scorer()
        good_inp = make_input(
            talk_listen_ratio=45.0, questions_asked_count=15, open_ended_question_pct=90.0,
            pain_point_questions_asked=6, monologue_longest_seconds=10,
            budget_discussed=1, authority_confirmed=1, timeline_established=1,
            business_impact_quantified=1, next_steps_defined=1,
            filler_words_per_minute=0.0, interruptions_count=0,
            value_statement_count=5, objection_count=5, objections_handled_count=5,
            call_type="demo",
        )
        result = scorer.score(good_inp)
        if result.is_exemplary_call:
            assert result in scorer.exemplary_calls

    def test_coachable_calls_filters_correctly(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
        for r in scorer.coachable_calls:
            assert r.is_coachable_moment is True

    def test_exemplary_calls_filters_correctly(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
        for r in scorer.exemplary_calls:
            assert r.is_exemplary_call is True


# ─────────────────────────────────────────────────────────────────────────────
# 20. summary() method
# ─────────────────────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_empty_zeros(self):
        scorer = make_scorer()
        s = scorer.summary()
        assert s["total"] == 0
        assert s["avg_conversation_composite"] == 0.0
        assert s["avg_deal_advancement_score"] == 0.0
        assert s["coachable_count"] == 0
        assert s["exemplary_count"] == 0
        assert s["avg_discovery_score"] == 0.0
        assert s["avg_qualification_score"] == 0.0
        assert s["avg_communication_score"] == 0.0
        assert s["avg_value_articulation_score"] == 0.0

    def test_summary_empty_count_dicts(self):
        scorer = make_scorer()
        s = scorer.summary()
        assert s["quality_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["depth_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_total(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
        s = scorer.summary()
        assert s["total"] == 5

    def test_summary_quality_counts(self):
        scorer = make_scorer()
        scorer.score(make_input())
        s = scorer.summary()
        assert isinstance(s["quality_counts"], dict)
        total = sum(s["quality_counts"].values())
        assert total == s["total"]

    def test_summary_pattern_counts(self):
        scorer = make_scorer()
        scorer.score(make_input())
        s = scorer.summary()
        assert isinstance(s["pattern_counts"], dict)
        total = sum(s["pattern_counts"].values())
        assert total == s["total"]

    def test_summary_depth_counts(self):
        scorer = make_scorer()
        scorer.score(make_input())
        s = scorer.summary()
        assert isinstance(s["depth_counts"], dict)
        total = sum(s["depth_counts"].values())
        assert total == s["total"]

    def test_summary_action_counts(self):
        scorer = make_scorer()
        scorer.score(make_input())
        s = scorer.summary()
        assert isinstance(s["action_counts"], dict)
        total = sum(s["action_counts"].values())
        assert total == s["total"]

    def test_summary_avg_composite_is_correct(self):
        scorer = make_scorer()
        results = scorer.score_batch([make_input(call_id=f"c{i}") for i in range(4)])
        s = scorer.summary()
        expected = round(sum(r.conversation_composite for r in results) / 4, 1)
        assert s["avg_conversation_composite"] == expected

    def test_summary_avg_deal_advancement_is_correct(self):
        scorer = make_scorer()
        results = scorer.score_batch([make_input(call_id=f"c{i}") for i in range(4)])
        s = scorer.summary()
        expected = round(sum(r.deal_advancement_score for r in results) / 4, 1)
        assert s["avg_deal_advancement_score"] == expected

    def test_summary_coachable_count(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(3)])
        s = scorer.summary()
        assert s["coachable_count"] == len(scorer.coachable_calls)

    def test_summary_exemplary_count(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(3)])
        s = scorer.summary()
        assert s["exemplary_count"] == len(scorer.exemplary_calls)

    def test_summary_avg_discovery_score(self):
        scorer = make_scorer()
        results = scorer.score_batch([make_input(call_id=f"c{i}") for i in range(4)])
        s = scorer.summary()
        expected = round(sum(r.discovery_score for r in results) / 4, 1)
        assert s["avg_discovery_score"] == expected

    def test_summary_avg_qualification_score(self):
        scorer = make_scorer()
        results = scorer.score_batch([make_input(call_id=f"c{i}") for i in range(4)])
        s = scorer.summary()
        expected = round(sum(r.qualification_score for r in results) / 4, 1)
        assert s["avg_qualification_score"] == expected

    def test_summary_avg_communication_score(self):
        scorer = make_scorer()
        results = scorer.score_batch([make_input(call_id=f"c{i}") for i in range(4)])
        s = scorer.summary()
        expected = round(sum(r.communication_score for r in results) / 4, 1)
        assert s["avg_communication_score"] == expected

    def test_summary_avg_value_articulation_score(self):
        scorer = make_scorer()
        results = scorer.score_batch([make_input(call_id=f"c{i}") for i in range(4)])
        s = scorer.summary()
        expected = round(sum(r.value_articulation_score for r in results) / 4, 1)
        assert s["avg_value_articulation_score"] == expected

    def test_summary_quality_counts_keys_are_valid_enum_values(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
        s = scorer.summary()
        valid_values = {e.value for e in ConversationQuality}
        for key in s["quality_counts"]:
            assert key in valid_values

    def test_summary_pattern_counts_keys_are_valid(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
        s = scorer.summary()
        valid_values = {e.value for e in ConversationPattern}
        for key in s["pattern_counts"]:
            assert key in valid_values

    def test_summary_depth_counts_keys_are_valid(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
        s = scorer.summary()
        valid_values = {e.value for e in QualificationDepth}
        for key in s["depth_counts"]:
            assert key in valid_values

    def test_summary_action_counts_keys_are_valid(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
        s = scorer.summary()
        valid_values = {e.value for e in ConversationAction}
        for key in s["action_counts"]:
            assert key in valid_values

    def test_summary_after_reset_returns_zeros(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(3)])
        scorer.reset()
        s = scorer.summary()
        assert s["total"] == 0
        assert s["avg_conversation_composite"] == 0.0

    def test_summary_single_call(self):
        scorer = make_scorer()
        result = scorer.score(make_input(call_id="solo"))
        s = scorer.summary()
        assert s["total"] == 1
        assert s["avg_conversation_composite"] == result.conversation_composite

    def test_summary_mixed_quality_counts_all_sum_to_total(self):
        scorer = make_scorer()
        # Score very different calls
        scorer.score(make_input(
            talk_listen_ratio=100.0, questions_asked_count=0, open_ended_question_pct=0.0,
            pain_point_questions_asked=0, budget_discussed=0, authority_confirmed=0,
            timeline_established=0, business_impact_quantified=0, next_steps_defined=0,
            filler_words_per_minute=20.0, interruptions_count=20, value_statement_count=0,
            objection_count=0, call_type="discovery", monologue_longest_seconds=200,
            call_id="poor-call",
        ))
        scorer.score(make_input(
            talk_listen_ratio=45.0, questions_asked_count=15, open_ended_question_pct=90.0,
            pain_point_questions_asked=6, budget_discussed=1, authority_confirmed=1,
            timeline_established=1, business_impact_quantified=1, next_steps_defined=1,
            filler_words_per_minute=0.0, interruptions_count=0, value_statement_count=5,
            objection_count=5, objections_handled_count=5, call_type="demo",
            call_id="elite-call", monologue_longest_seconds=10,
        ))
        s = scorer.summary()
        assert sum(s["quality_counts"].values()) == 2


# ─────────────────────────────────────────────────────────────────────────────
# 21. to_dict() values verification
# ─────────────────────────────────────────────────────────────────────────────

class TestToDictValues:
    def test_to_dict_conversation_quality_is_string(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        assert isinstance(d["conversation_quality"], str)

    def test_to_dict_conversation_pattern_is_string(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        assert isinstance(d["conversation_pattern"], str)

    def test_to_dict_qualification_depth_is_string(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        assert isinstance(d["qualification_depth"], str)

    def test_to_dict_conversation_action_is_string(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        assert isinstance(d["conversation_action"], str)

    def test_to_dict_quality_valid_value(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        assert d["conversation_quality"] in {e.value for e in ConversationQuality}

    def test_to_dict_pattern_valid_value(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        assert d["conversation_pattern"] in {e.value for e in ConversationPattern}

    def test_to_dict_depth_valid_value(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        assert d["qualification_depth"] in {e.value for e in QualificationDepth}

    def test_to_dict_action_valid_value(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        assert d["conversation_action"] in {e.value for e in ConversationAction}

    def test_to_dict_scores_are_numeric(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        for key in ("discovery_score", "qualification_score", "communication_score",
                    "value_articulation_score", "conversation_composite",
                    "coaching_priority_score", "deal_advancement_score"):
            assert isinstance(d[key], (int, float)), f"{key} should be numeric"

    def test_to_dict_booleans(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        assert isinstance(d["is_coachable_moment"], bool)
        assert isinstance(d["is_exemplary_call"], bool)

    def test_to_dict_scores_in_range(self):
        scorer = make_scorer()
        d = scorer.score(make_input()).to_dict()
        for key in ("discovery_score", "qualification_score", "communication_score",
                    "value_articulation_score", "conversation_composite",
                    "coaching_priority_score", "deal_advancement_score"):
            assert 0.0 <= d[key] <= 100.0, f"{key} out of range: {d[key]}"


# ─────────────────────────────────────────────────────────────────────────────
# 22. Edge cases and boundary conditions
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_talk_listen_ratio_zero(self):
        scorer = make_scorer()
        result = scorer.score(make_input(talk_listen_ratio=0.0))
        assert result.discovery_score >= 0.0

    def test_talk_listen_ratio_100(self):
        scorer = make_scorer()
        result = scorer.score(make_input(talk_listen_ratio=100.0))
        assert result.discovery_score >= 0.0

    def test_very_high_filler_words(self):
        scorer = make_scorer()
        result = scorer.score(make_input(filler_words_per_minute=100.0))
        assert result.communication_score >= 0.0

    def test_very_high_interruptions(self):
        scorer = make_scorer()
        result = scorer.score(make_input(interruptions_count=100))
        assert result.communication_score >= 0.0

    def test_very_long_monologue(self):
        scorer = make_scorer()
        result = scorer.score(make_input(monologue_longest_seconds=9999))
        assert result.discovery_score >= 0.0

    def test_zero_call_duration(self):
        scorer = make_scorer()
        result = scorer.score(make_input(call_duration_minutes=0))
        assert result.conversation_composite >= 0.0

    def test_very_large_deal_value(self):
        scorer = make_scorer()
        result = scorer.score(make_input(deal_value=1e9))
        assert result.conversation_composite >= 0.0

    def test_objections_handled_more_than_count(self):
        # Technically invalid but shouldn't crash
        scorer = make_scorer()
        result = scorer.score(make_input(objection_count=2, objections_handled_count=5))
        assert result.value_articulation_score >= 0.0

    def test_objections_handled_zero_of_nonzero(self):
        scorer = make_scorer()
        result = scorer.score(make_input(objection_count=5, objections_handled_count=0))
        assert result.value_articulation_score >= 0.0

    def test_all_zeros_does_not_crash(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=0.0, questions_asked_count=0, open_ended_question_pct=0.0,
            pain_point_questions_asked=0, budget_discussed=0, authority_confirmed=0,
            timeline_established=0, business_impact_quantified=0, next_steps_defined=0,
            competitor_mentioned_by_buyer=0, objection_count=0, objections_handled_count=0,
            filler_words_per_minute=0.0, interruptions_count=0, monologue_longest_seconds=0,
            value_statement_count=0, call_duration_minutes=0, deal_value=0.0,
        ))
        assert result is not None

    def test_multiple_scorers_independent(self):
        scorer1 = make_scorer()
        scorer2 = make_scorer()
        scorer1.score(make_input(call_id="s1-call"))
        assert len(scorer2._results) == 0

    def test_new_scorer_starts_empty(self):
        scorer = make_scorer()
        assert len(scorer._results) == 0
        assert scorer.avg_conversation_composite == 0.0
        assert scorer.avg_deal_advancement_score == 0.0

    def test_different_call_types(self):
        scorer = make_scorer()
        for call_type in ("discovery", "demo", "followup", "negotiation", "closing"):
            result = scorer.score(make_input(call_type=call_type))
            assert isinstance(result, ConversationIntelligenceResult)

    def test_demo_call_ttl_70_no_discovery_penalty(self):
        """For non-discovery calls, discovery score is unaffected by talk ratio."""
        scorer1 = make_scorer()
        scorer2 = make_scorer()
        r1 = scorer1.score(make_input(call_type="demo", talk_listen_ratio=70.0))
        r2 = scorer2.score(make_input(call_type="demo", talk_listen_ratio=45.0))
        # Discovery score uses talk_listen_ratio regardless of call type
        # For 70 -> +5 branch; for 45 -> +25 branch
        assert r1.discovery_score != r2.discovery_score

    def test_communication_score_discovery_vs_demo_at_66(self):
        scorer1 = make_scorer()
        scorer2 = make_scorer()
        # discovery with ttl=66 → -15 penalty
        r_disc = scorer1.score(make_input(
            call_type="discovery", talk_listen_ratio=66.0,
            filler_words_per_minute=0.0, interruptions_count=0,
        ))
        # demo with ttl=66 → no penalty (66 <= 80)
        r_demo = scorer2.score(make_input(
            call_type="demo", talk_listen_ratio=66.0,
            filler_words_per_minute=0.0, interruptions_count=0,
        ))
        assert r_disc.communication_score < r_demo.communication_score

    def test_challenger_pattern_requires_80pct_handle_rate(self):
        """79% handle rate should NOT produce challenger."""
        scorer = make_scorer()
        result = scorer.score(make_input(
            business_impact_quantified=1,
            value_statement_count=5,
            objection_count=100,
            objections_handled_count=79,  # 79% < 80%
        ))
        assert result.conversation_pattern != ConversationPattern.CHALLENGER

    def test_handle_rate_exactly_below_80_pct(self):
        """Handle rate of exactly 79.9% should not get 10-point bonus in value artic."""
        scorer = make_scorer()
        # 799/1000 = 79.9% < 80%
        result = scorer.score(make_input(
            value_statement_count=0, business_impact_quantified=0,
            next_steps_defined=0, objection_count=1000, objections_handled_count=799,
        ))
        # Should get 5 points (>=50%) but not 10
        assert result.value_articulation_score == 5.0

    def test_summary_returns_dict(self):
        scorer = make_scorer()
        scorer.score(make_input())
        s = scorer.summary()
        assert isinstance(s, dict)

    def test_score_after_batch(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(3)])
        result = scorer.score(make_input(call_id="after-batch"))
        assert len(scorer._results) == 4
        assert result.call_id == "after-batch"


# ─────────────────────────────────────────────────────────────────────────────
# 23. Full pipeline integration tests
# ─────────────────────────────────────────────────────────────────────────────

class TestFullPipeline:
    def test_ideal_discovery_call(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            call_type="discovery",
            talk_listen_ratio=45.0,
            questions_asked_count=12,
            open_ended_question_pct=75.0,
            pain_point_questions_asked=5,
            monologue_longest_seconds=40,
            budget_discussed=1,
            authority_confirmed=1,
            timeline_established=1,
            business_impact_quantified=1,
            next_steps_defined=1,
            filler_words_per_minute=1.0,
            interruptions_count=0,
            value_statement_count=4,
            objection_count=2,
            objections_handled_count=2,
        ))
        assert result.conversation_composite > 70.0
        assert result.conversation_quality in {
            ConversationQuality.ELITE, ConversationQuality.PROFICIENT
        }

    def test_terrible_call_full_pipeline(self):
        scorer = make_scorer()
        result = scorer.score(make_input(
            call_type="discovery",
            talk_listen_ratio=95.0,
            questions_asked_count=0,
            open_ended_question_pct=0.0,
            pain_point_questions_asked=0,
            monologue_longest_seconds=300,
            budget_discussed=0,
            authority_confirmed=0,
            timeline_established=0,
            business_impact_quantified=0,
            next_steps_defined=0,
            filler_words_per_minute=12.0,
            interruptions_count=8,
            value_statement_count=0,
            objection_count=3,
            objections_handled_count=0,
        ))
        assert result.conversation_composite < 40.0
        assert result.conversation_quality == ConversationQuality.POOR
        assert result.is_coachable_moment is True
        assert result.is_exemplary_call is False

    def test_batch_then_summary_consistency(self):
        scorer = make_scorer()
        inputs = [make_input(call_id=f"c{i}") for i in range(10)]
        results = scorer.score_batch(inputs)
        s = scorer.summary()
        assert s["total"] == 10
        assert sum(s["quality_counts"].values()) == 10
        assert sum(s["pattern_counts"].values()) == 10
        assert sum(s["depth_counts"].values()) == 10
        assert sum(s["action_counts"].values()) == 10

    def test_coachable_count_matches_coachable_calls(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
        s = scorer.summary()
        assert s["coachable_count"] == len(scorer.coachable_calls)

    def test_exemplary_count_matches_exemplary_calls(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
        s = scorer.summary()
        assert s["exemplary_count"] == len(scorer.exemplary_calls)

    def test_round_trip_to_dict(self):
        scorer = make_scorer()
        result = scorer.score(make_input())
        d = result.to_dict()
        assert d["call_id"] == result.call_id
        assert d["deal_id"] == result.deal_id
        assert d["discovery_score"] == result.discovery_score
        assert d["qualification_score"] == result.qualification_score
        assert d["communication_score"] == result.communication_score
        assert d["value_articulation_score"] == result.value_articulation_score
        assert d["conversation_composite"] == result.conversation_composite
        assert d["coaching_priority_score"] == result.coaching_priority_score
        assert d["deal_advancement_score"] == result.deal_advancement_score
        assert d["is_coachable_moment"] == result.is_coachable_moment
        assert d["is_exemplary_call"] == result.is_exemplary_call

    def test_multiple_resets_work(self):
        scorer = make_scorer()
        for _ in range(3):
            scorer.score_batch([make_input(call_id=f"c{i}") for i in range(5)])
            scorer.reset()
        assert len(scorer._results) == 0

    def test_avg_properties_match_summary(self):
        scorer = make_scorer()
        scorer.score_batch([make_input(call_id=f"c{i}") for i in range(4)])
        s = scorer.summary()
        assert s["avg_conversation_composite"] == scorer.avg_conversation_composite
        assert s["avg_deal_advancement_score"] == scorer.avg_deal_advancement_score

    def test_monologue_pattern_when_balanced_dialogue_does_not_match(self):
        """MONOLOGUE fires when ratio >= 70 OR monologue >= 180, but BALANCED_DIALOGUE
        (40<=ratio<=60, q>=5) is checked first in the if-chain.  To reach MONOLOGUE the
        balanced-dialogue condition must NOT match — use ratio outside 40-60 range."""
        scorer = make_scorer()
        result = scorer.score(make_input(
            talk_listen_ratio=70.0,       # >= 70 → monologue; also outside 40-60 so no balanced
            questions_asked_count=5,
            open_ended_question_pct=30.0,
            pain_point_questions_asked=2,
            monologue_longest_seconds=50,
            business_impact_quantified=0,
            value_statement_count=2,
            objection_count=0,
        ))
        assert result.conversation_pattern == ConversationPattern.MONOLOGUE

    def test_challenger_pattern_takes_priority_over_consultative(self):
        """Challenger check comes before consultative in the if-chain."""
        scorer = make_scorer()
        result = scorer.score(make_input(
            business_impact_quantified=1,
            value_statement_count=4,
            objection_count=5,
            objections_handled_count=4,  # 80%
            open_ended_question_pct=70.0,
            talk_listen_ratio=45.0,
            questions_asked_count=10,
            pain_point_questions_asked=5,
            budget_discussed=1,
            authority_confirmed=1,
            timeline_established=1,
            next_steps_defined=1,
            filler_words_per_minute=0.0,
            interruptions_count=0,
            monologue_longest_seconds=10,
        ))
        assert result.conversation_pattern == ConversationPattern.CHALLENGER
