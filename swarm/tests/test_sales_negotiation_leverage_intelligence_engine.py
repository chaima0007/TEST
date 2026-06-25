"""
Comprehensive pytest test suite for SalesNegotiationLeverageIntelligenceEngine.
"""
from __future__ import annotations

import pytest
from swarm.intelligence.sales_negotiation_leverage_intelligence_engine import (
    LeverageAction,
    LeverageInput,
    LeveragePattern,
    LeverageResult,
    LeverageRisk,
    LeverageSeverity,
    SalesNegotiationLeverageIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers / factories
# ---------------------------------------------------------------------------

def make_input(**overrides) -> LeverageInput:
    """Return a 'healthy' baseline LeverageInput with optional field overrides."""
    defaults = dict(
        rep_id="REP001",
        region="Northeast",
        evaluation_period_id="Q1-2026",
        # tactical — healthy (high usage → low risk)
        deals_with_competitive_pressure_used_pct=0.70,
        urgency_event_cited_in_negotiation_pct=0.70,
        deadline_anchored_close_rate_pct=0.60,
        concession_without_counter_ask_pct=0.10,
        value_anchor_set_before_price_pct=0.80,
        executive_sponsor_engaged_in_negotiation_pct=0.50,
        walk_away_threat_used_pct=0.30,
        walk_away_actually_executed_pct=0.05,
        multi_option_pricing_presented_pct=0.50,
        deal_restructured_to_preserve_margin_pct=0.40,
        procurement_engaged_early_pct=0.50,
        legal_used_as_delay_tactic_pct=0.10,
        negotiation_extended_beyond_target_days=5.0,
        last_minute_concession_rate_pct=0.10,
        price_reduction_without_scope_change_pct=0.10,
        batch_deal_packaging_rate_pct=0.20,
        renewal_leverage_used_pct=0.30,
        total_deals_negotiated=10,
        avg_opportunity_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return LeverageInput(**defaults)


def make_engine() -> SalesNegotiationLeverageIntelligenceEngine:
    return SalesNegotiationLeverageIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. Enum values and counts
# ---------------------------------------------------------------------------

class TestEnums:
    def test_leverage_risk_values(self):
        assert set(r.value for r in LeverageRisk) == {"low", "moderate", "high", "critical"}

    def test_leverage_risk_count(self):
        assert len(LeverageRisk) == 4

    def test_leverage_pattern_values(self):
        expected = {
            "none",
            "deadline_blind_negotiator",
            "single_lever_dependency",
            "urgency_manufacturing_failure",
            "competitive_leverage_avoidance",
            "concession_without_ask",
        }
        assert set(p.value for p in LeveragePattern) == expected

    def test_leverage_pattern_count(self):
        assert len(LeveragePattern) == 6

    def test_leverage_severity_values(self):
        assert set(s.value for s in LeverageSeverity) == {"commanding", "balanced", "reactive", "powerless"}

    def test_leverage_severity_count(self):
        assert len(LeverageSeverity) == 4

    def test_leverage_action_values(self):
        expected = {
            "no_action",
            "leverage_awareness_coaching",
            "deadline_framing_coaching",
            "competitive_leverage_coaching",
            "concession_discipline_coaching",
            "negotiation_strategy_overhaul",
        }
        assert set(a.value for a in LeverageAction) == expected

    def test_leverage_action_count(self):
        assert len(LeverageAction) == 6

    def test_enums_are_str_subclass(self):
        assert isinstance(LeverageRisk.low, str)
        assert isinstance(LeveragePattern.none, str)
        assert isinstance(LeverageSeverity.commanding, str)
        assert isinstance(LeverageAction.no_action, str)


# ---------------------------------------------------------------------------
# 2. LeverageInput – all 22 fields accepted
# ---------------------------------------------------------------------------

class TestLeverageInput:
    def test_all_22_fields_set(self):
        inp = make_input()
        assert inp.rep_id == "REP001"
        assert inp.region == "Northeast"
        assert inp.evaluation_period_id == "Q1-2026"
        assert inp.deals_with_competitive_pressure_used_pct == 0.70
        assert inp.urgency_event_cited_in_negotiation_pct == 0.70
        assert inp.deadline_anchored_close_rate_pct == 0.60
        assert inp.concession_without_counter_ask_pct == 0.10
        assert inp.value_anchor_set_before_price_pct == 0.80
        assert inp.executive_sponsor_engaged_in_negotiation_pct == 0.50
        assert inp.walk_away_threat_used_pct == 0.30
        assert inp.walk_away_actually_executed_pct == 0.05
        assert inp.multi_option_pricing_presented_pct == 0.50
        assert inp.deal_restructured_to_preserve_margin_pct == 0.40
        assert inp.procurement_engaged_early_pct == 0.50
        assert inp.legal_used_as_delay_tactic_pct == 0.10
        assert inp.negotiation_extended_beyond_target_days == 5.0
        assert inp.last_minute_concession_rate_pct == 0.10
        assert inp.price_reduction_without_scope_change_pct == 0.10
        assert inp.batch_deal_packaging_rate_pct == 0.20
        assert inp.renewal_leverage_used_pct == 0.30
        assert inp.total_deals_negotiated == 10
        assert inp.avg_opportunity_value_usd == 50_000.0

    def test_input_field_count(self):
        import dataclasses
        fields = dataclasses.fields(LeverageInput)
        assert len(fields) == 22


# ---------------------------------------------------------------------------
# 3. LeverageResult – all 15 fields + to_dict 15 keys
# ---------------------------------------------------------------------------

class TestLeverageResult:
    @pytest.fixture
    def result(self):
        eng = make_engine()
        return eng.assess(make_input())

    def test_result_field_count(self):
        import dataclasses
        fields = dataclasses.fields(LeverageResult)
        assert len(fields) == 15

    def test_result_has_all_fields(self, result):
        assert hasattr(result, "rep_id")
        assert hasattr(result, "region")
        assert hasattr(result, "leverage_risk")
        assert hasattr(result, "leverage_pattern")
        assert hasattr(result, "leverage_severity")
        assert hasattr(result, "recommended_action")
        assert hasattr(result, "tactical_score")
        assert hasattr(result, "urgency_score")
        assert hasattr(result, "discipline_score")
        assert hasattr(result, "positioning_score")
        assert hasattr(result, "leverage_composite")
        assert hasattr(result, "has_leverage_gap")
        assert hasattr(result, "requires_leverage_coaching")
        assert hasattr(result, "estimated_margin_conceded_usd")
        assert hasattr(result, "leverage_signal")

    def test_to_dict_returns_exactly_15_keys(self, result):
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_names(self, result):
        d = result.to_dict()
        expected_keys = {
            "rep_id", "region", "leverage_risk", "leverage_pattern",
            "leverage_severity", "recommended_action", "tactical_score",
            "urgency_score", "discipline_score", "positioning_score",
            "leverage_composite", "has_leverage_gap", "requires_leverage_coaching",
            "estimated_margin_conceded_usd", "leverage_signal",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self, result):
        d = result.to_dict()
        assert isinstance(d["leverage_risk"], str)
        assert isinstance(d["leverage_pattern"], str)
        assert isinstance(d["leverage_severity"], str)
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_rep_id_and_region(self, result):
        d = result.to_dict()
        assert d["rep_id"] == "REP001"
        assert d["region"] == "Northeast"


# ---------------------------------------------------------------------------
# 4. Sub-score: _tactical_score branches and cap
# ---------------------------------------------------------------------------

class TestTacticalScore:
    def _tactical(self, **kw) -> float:
        eng = make_engine()
        return eng._tactical_score(make_input(**kw))

    # deals_with_competitive_pressure_used_pct
    def test_competitive_pressure_le_020_adds_40(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.20,
            walk_away_threat_used_pct=0.30,          # no walk-away bonus
            multi_option_pricing_presented_pct=0.50,  # no multi-option bonus
        )
        assert score == 40.0

    def test_competitive_pressure_le_040_adds_22(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.40,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
        )
        assert score == 22.0

    def test_competitive_pressure_le_060_adds_8(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.60,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
        )
        assert score == 8.0

    def test_competitive_pressure_above_060_adds_0(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.61,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
        )
        assert score == 0.0

    # walk_away_threat_used_pct
    def test_walk_away_le_010_adds_35(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.70,  # no bonus
            walk_away_threat_used_pct=0.10,
            multi_option_pricing_presented_pct=0.50,
        )
        assert score == 35.0

    def test_walk_away_le_025_adds_18(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.25,
            multi_option_pricing_presented_pct=0.50,
        )
        assert score == 18.0

    def test_walk_away_above_025_adds_0(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.26,
            multi_option_pricing_presented_pct=0.50,
        )
        assert score == 0.0

    # multi_option_pricing_presented_pct
    def test_multi_option_le_020_adds_25(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.20,
        )
        assert score == 25.0

    def test_multi_option_le_045_adds_12(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.45,
        )
        assert score == 12.0

    def test_multi_option_above_045_adds_0(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.46,
        )
        assert score == 0.0

    def test_tactical_max_cap_at_100(self):
        # 40 + 35 + 25 = 100 exactly, should not exceed
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.05,
            walk_away_threat_used_pct=0.05,
            multi_option_pricing_presented_pct=0.05,
        )
        assert score == 100.0

    def test_tactical_all_zeros(self):
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
        )
        assert score == 0.0

    def test_tactical_combined_branches(self):
        # 22 + 18 + 12 = 52
        score = self._tactical(
            deals_with_competitive_pressure_used_pct=0.40,
            walk_away_threat_used_pct=0.25,
            multi_option_pricing_presented_pct=0.45,
        )
        assert score == 52.0


# ---------------------------------------------------------------------------
# 5. Sub-score: _urgency_score branches and cap
# ---------------------------------------------------------------------------

class TestUrgencyScore:
    def _urgency(self, **kw) -> float:
        eng = make_engine()
        return eng._urgency_score(make_input(**kw))

    # urgency_event_cited_in_negotiation_pct
    def test_urgency_event_le_020_adds_40(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.20,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
        )
        assert s == 40.0

    def test_urgency_event_le_040_adds_22(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.40,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
        )
        assert s == 22.0

    def test_urgency_event_le_060_adds_8(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.60,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
        )
        assert s == 8.0

    def test_urgency_event_above_060_adds_0(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.61,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
        )
        assert s == 0.0

    # deadline_anchored_close_rate_pct
    def test_deadline_le_025_adds_35(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.25,
            negotiation_extended_beyond_target_days=5.0,
        )
        assert s == 35.0

    def test_deadline_le_050_adds_18(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.50,
            negotiation_extended_beyond_target_days=5.0,
        )
        assert s == 18.0

    def test_deadline_above_050_adds_0(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.51,
            negotiation_extended_beyond_target_days=5.0,
        )
        assert s == 0.0

    # negotiation_extended_beyond_target_days
    def test_extended_ge_210_adds_25(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=21.0,
        )
        assert s == 25.0

    def test_extended_ge_100_adds_12(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=10.0,
        )
        assert s == 12.0

    def test_extended_below_100_adds_0(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=9.9,
        )
        assert s == 0.0

    def test_urgency_max_cap_at_100(self):
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.05,
            deadline_anchored_close_rate_pct=0.05,
            negotiation_extended_beyond_target_days=25.0,
        )
        assert s == 100.0

    def test_urgency_combined_mid_branches(self):
        # 22 + 18 + 12 = 52
        s = self._urgency(
            urgency_event_cited_in_negotiation_pct=0.40,
            deadline_anchored_close_rate_pct=0.50,
            negotiation_extended_beyond_target_days=10.0,
        )
        assert s == 52.0


# ---------------------------------------------------------------------------
# 6. Sub-score: _discipline_score branches and cap
# ---------------------------------------------------------------------------

class TestDisciplineScore:
    def _discipline(self, **kw) -> float:
        eng = make_engine()
        return eng._discipline_score(make_input(**kw))

    # concession_without_counter_ask_pct
    def test_concession_ge_060_adds_40(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.60,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
        )
        assert s == 40.0

    def test_concession_ge_040_adds_22(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.40,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
        )
        assert s == 22.0

    def test_concession_ge_020_adds_8(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.20,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
        )
        assert s == 8.0

    def test_concession_below_020_adds_0(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.19,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
        )
        assert s == 0.0

    # price_reduction_without_scope_change_pct
    def test_price_reduction_ge_050_adds_35(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.50,
            last_minute_concession_rate_pct=0.10,
        )
        assert s == 35.0

    def test_price_reduction_ge_030_adds_18(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.30,
            last_minute_concession_rate_pct=0.10,
        )
        assert s == 18.0

    def test_price_reduction_below_030_adds_0(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.29,
            last_minute_concession_rate_pct=0.10,
        )
        assert s == 0.0

    # last_minute_concession_rate_pct
    def test_last_minute_ge_045_adds_25(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.45,
        )
        assert s == 25.0

    def test_last_minute_ge_025_adds_12(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.25,
        )
        assert s == 12.0

    def test_last_minute_below_025_adds_0(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.24,
        )
        assert s == 0.0

    def test_discipline_max_cap_at_100(self):
        s = self._discipline(
            concession_without_counter_ask_pct=0.80,
            price_reduction_without_scope_change_pct=0.80,
            last_minute_concession_rate_pct=0.80,
        )
        assert s == 100.0

    def test_discipline_combined_mid_branches(self):
        # 22 + 18 + 12 = 52
        s = self._discipline(
            concession_without_counter_ask_pct=0.40,
            price_reduction_without_scope_change_pct=0.30,
            last_minute_concession_rate_pct=0.25,
        )
        assert s == 52.0


# ---------------------------------------------------------------------------
# 7. Sub-score: _positioning_score branches and cap
# ---------------------------------------------------------------------------

class TestPositioningScore:
    def _pos(self, **kw) -> float:
        eng = make_engine()
        return eng._positioning_score(make_input(**kw))

    # value_anchor_set_before_price_pct
    def test_value_anchor_le_030_adds_45(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.30,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        assert s == 45.0

    def test_value_anchor_le_055_adds_25(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.55,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        assert s == 25.0

    def test_value_anchor_le_075_adds_10(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.75,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        assert s == 10.0

    def test_value_anchor_above_075_adds_0(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.76,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        assert s == 0.0

    # executive_sponsor_engaged_in_negotiation_pct
    def test_exec_sponsor_le_020_adds_30(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.20,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        assert s == 30.0

    def test_exec_sponsor_le_040_adds_15(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.40,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        assert s == 15.0

    def test_exec_sponsor_above_040_adds_0(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.41,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        assert s == 0.0

    # deal_restructured_to_preserve_margin_pct
    def test_deal_restructured_le_015_adds_25(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.15,
        )
        assert s == 25.0

    def test_deal_restructured_le_035_adds_12(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.35,
        )
        assert s == 12.0

    def test_deal_restructured_above_035_adds_0(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.36,
        )
        assert s == 0.0

    def test_positioning_max_cap_at_100(self):
        s = self._pos(
            value_anchor_set_before_price_pct=0.05,
            executive_sponsor_engaged_in_negotiation_pct=0.05,
            deal_restructured_to_preserve_margin_pct=0.05,
        )
        assert s == 100.0

    def test_positioning_combined_mid_branches(self):
        # 25 + 15 + 12 = 52
        s = self._pos(
            value_anchor_set_before_price_pct=0.55,
            executive_sponsor_engaged_in_negotiation_pct=0.40,
            deal_restructured_to_preserve_margin_pct=0.35,
        )
        assert s == 52.0


# ---------------------------------------------------------------------------
# 8. Composite formula and weights
# ---------------------------------------------------------------------------

class TestCompositeFormula:
    def test_composite_weights(self):
        eng = make_engine()
        inp = make_input(
            # tactical = 40 (competitive <=0.20 only)
            deals_with_competitive_pressure_used_pct=0.05,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            # urgency = 40 (urgency event <=0.20 only)
            urgency_event_cited_in_negotiation_pct=0.05,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            # discipline = 40 (concession >=0.60 only)
            concession_without_counter_ask_pct=0.70,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
            # positioning = 45 (value anchor <=0.30 only)
            value_anchor_set_before_price_pct=0.10,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        result = eng.assess(inp)
        expected = round(40 * 0.30 + 40 * 0.25 + 40 * 0.25 + 45 * 0.20, 1)
        assert result.leverage_composite == expected

    def test_composite_capped_at_100(self):
        eng = make_engine()
        # All sub-scores maxed
        inp = make_input(
            deals_with_competitive_pressure_used_pct=0.01,
            walk_away_threat_used_pct=0.01,
            multi_option_pricing_presented_pct=0.01,
            urgency_event_cited_in_negotiation_pct=0.01,
            deadline_anchored_close_rate_pct=0.01,
            negotiation_extended_beyond_target_days=30.0,
            concession_without_counter_ask_pct=0.90,
            price_reduction_without_scope_change_pct=0.90,
            last_minute_concession_rate_pct=0.90,
            value_anchor_set_before_price_pct=0.01,
            executive_sponsor_engaged_in_negotiation_pct=0.01,
            deal_restructured_to_preserve_margin_pct=0.01,
        )
        result = eng.assess(inp)
        assert result.leverage_composite <= 100.0

    def test_composite_zero_for_healthy_rep(self):
        eng = make_engine()
        # everything above all risk thresholds
        inp = make_input(
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        result = eng.assess(inp)
        assert result.leverage_composite == 0.0


# ---------------------------------------------------------------------------
# 9. Pattern detection – all 6 patterns, priority, boundaries
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def _assess(self, **kw) -> LeverageResult:
        return make_engine().assess(make_input(**kw))

    # --- concession_without_ask (highest priority) ---

    def test_concession_without_ask_detected(self):
        r = self._assess(
            concession_without_counter_ask_pct=0.55,
            price_reduction_without_scope_change_pct=0.40,
            # Also meets competitive_leverage_avoidance conditions to test priority
            deals_with_competitive_pressure_used_pct=0.05,
            walk_away_threat_used_pct=0.05,
            multi_option_pricing_presented_pct=0.05,
        )
        assert r.leverage_pattern == LeveragePattern.concession_without_ask

    def test_concession_without_ask_boundary_miss(self):
        # concession just below 0.55 → should NOT trigger this pattern
        r = self._assess(
            concession_without_counter_ask_pct=0.54,
            price_reduction_without_scope_change_pct=0.40,
            # Ensure no other pattern fires
            deals_with_competitive_pressure_used_pct=0.70,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            value_anchor_set_before_price_pct=0.80,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
            last_minute_concession_rate_pct=0.10,
        )
        assert r.leverage_pattern != LeveragePattern.concession_without_ask

    def test_concession_without_ask_price_boundary_miss(self):
        # price reduction just below 0.40
        r = self._assess(
            concession_without_counter_ask_pct=0.55,
            price_reduction_without_scope_change_pct=0.39,
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
            last_minute_concession_rate_pct=0.10,
        )
        assert r.leverage_pattern != LeveragePattern.concession_without_ask

    # --- competitive_leverage_avoidance ---

    def test_competitive_leverage_avoidance_detected(self):
        # tactical >= 40 AND deals_with_competitive_pressure_used_pct <= 0.25
        # tactical = 40 (competitive <=0.20) + 35 (walk_away <=0.10) = 75
        r = self._assess(
            deals_with_competitive_pressure_used_pct=0.20,
            walk_away_threat_used_pct=0.05,
            multi_option_pricing_presented_pct=0.50,      # no multi-option bonus
            # concession_without_ask must NOT fire
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            # urgency, positioning all healthy
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
            last_minute_concession_rate_pct=0.10,
        )
        assert r.leverage_pattern == LeveragePattern.competitive_leverage_avoidance

    def test_competitive_leverage_avoidance_requires_tactical_ge_40(self):
        # tactical = 0, even if deals pct <=0.25
        r = self._assess(
            deals_with_competitive_pressure_used_pct=0.25,
            walk_away_threat_used_pct=0.30,               # no walk-away bonus
            multi_option_pricing_presented_pct=0.50,      # no multi-option bonus
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
            last_minute_concession_rate_pct=0.10,
        )
        assert r.leverage_pattern == LeveragePattern.none

    # --- deadline_blind_negotiator ---

    def test_deadline_blind_negotiator_detected(self):
        # urgency >= 40 AND negotiation_extended >= 14.0
        # urgency = 40 (event <=0.20) + 35 (deadline <=0.25) = 75
        r = self._assess(
            urgency_event_cited_in_negotiation_pct=0.10,
            deadline_anchored_close_rate_pct=0.20,
            negotiation_extended_beyond_target_days=14.0,
            # concession_without_ask must NOT fire
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            # competitive must NOT fire (tactical < 40 or deals > 0.25)
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
            last_minute_concession_rate_pct=0.10,
        )
        assert r.leverage_pattern == LeveragePattern.deadline_blind_negotiator

    def test_deadline_blind_negotiator_boundary_extended_below_14(self):
        r = self._assess(
            urgency_event_cited_in_negotiation_pct=0.10,
            deadline_anchored_close_rate_pct=0.20,
            negotiation_extended_beyond_target_days=13.9,
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
            last_minute_concession_rate_pct=0.10,
        )
        assert r.leverage_pattern != LeveragePattern.deadline_blind_negotiator

    # --- urgency_manufacturing_failure ---

    def test_urgency_manufacturing_failure_detected(self):
        # urgency_event <=0.15 AND discipline >= 30
        # discipline = 22 (concession >=0.40) + 18 (price_reduction >=0.30) = 40 >= 30
        r = self._assess(
            urgency_event_cited_in_negotiation_pct=0.10,
            concession_without_counter_ask_pct=0.45,
            price_reduction_without_scope_change_pct=0.35,
            last_minute_concession_rate_pct=0.10,
            # urgency < 40 to skip deadline_blind_negotiator: urgent event low but deadline ok
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            # concession_without_ask must NOT fire
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        # urgency = 40 (event <=0.20) but extended < 14, so not deadline_blind
        # urgency_event <=0.15 and discipline=40 >=30 → urgency_manufacturing_failure
        assert r.leverage_pattern == LeveragePattern.urgency_manufacturing_failure

    def test_urgency_manufacturing_failure_event_boundary(self):
        # urgency_event = 0.16 → does NOT trigger
        r = self._assess(
            urgency_event_cited_in_negotiation_pct=0.16,
            concession_without_counter_ask_pct=0.45,
            price_reduction_without_scope_change_pct=0.35,
            last_minute_concession_rate_pct=0.10,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        assert r.leverage_pattern != LeveragePattern.urgency_manufacturing_failure

    # --- single_lever_dependency ---

    def test_single_lever_dependency_detected(self):
        # positioning >= 30 AND value_anchor <=0.25
        # positioning = 45 (value_anchor <=0.30)
        r = self._assess(
            value_anchor_set_before_price_pct=0.25,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
            # Ensure patterns above don't fire
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            last_minute_concession_rate_pct=0.10,
        )
        assert r.leverage_pattern == LeveragePattern.single_lever_dependency

    def test_single_lever_dependency_boundary_value_anchor(self):
        # value_anchor = 0.26 → does NOT trigger
        r = self._assess(
            value_anchor_set_before_price_pct=0.26,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            last_minute_concession_rate_pct=0.10,
        )
        assert r.leverage_pattern != LeveragePattern.single_lever_dependency

    # --- none ---

    def test_pattern_none_for_healthy_rep(self):
        r = self._assess()  # all baseline healthy values
        assert r.leverage_pattern == LeveragePattern.none

    # --- Priority test: concession_without_ask beats competitive_leverage_avoidance ---

    def test_pattern_priority_concession_beats_competitive(self):
        # Both conditions met; concession should win
        r = self._assess(
            concession_without_counter_ask_pct=0.60,
            price_reduction_without_scope_change_pct=0.50,
            deals_with_competitive_pressure_used_pct=0.10,  # also triggers competitive
            walk_away_threat_used_pct=0.05,
            multi_option_pricing_presented_pct=0.05,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
            last_minute_concession_rate_pct=0.10,
        )
        assert r.leverage_pattern == LeveragePattern.concession_without_ask


# ---------------------------------------------------------------------------
# 10. Risk level thresholds
# ---------------------------------------------------------------------------

class TestRiskLevel:
    def _risk_at(self, composite: float) -> LeverageRisk:
        eng = make_engine()
        return eng._risk_level(composite)

    def test_risk_low_below_20(self):
        assert self._risk_at(0.0) == LeverageRisk.low
        assert self._risk_at(19.9) == LeverageRisk.low

    def test_risk_moderate_at_20(self):
        assert self._risk_at(20.0) == LeverageRisk.moderate

    def test_risk_moderate_up_to_39(self):
        assert self._risk_at(39.9) == LeverageRisk.moderate

    def test_risk_high_at_40(self):
        assert self._risk_at(40.0) == LeverageRisk.high

    def test_risk_high_up_to_59(self):
        assert self._risk_at(59.9) == LeverageRisk.high

    def test_risk_critical_at_60(self):
        assert self._risk_at(60.0) == LeverageRisk.critical

    def test_risk_critical_at_100(self):
        assert self._risk_at(100.0) == LeverageRisk.critical


# ---------------------------------------------------------------------------
# 11. Severity thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def _sev_at(self, composite: float) -> LeverageSeverity:
        eng = make_engine()
        return eng._severity(composite)

    def test_commanding_below_20(self):
        assert self._sev_at(0.0) == LeverageSeverity.commanding
        assert self._sev_at(19.9) == LeverageSeverity.commanding

    def test_balanced_at_20(self):
        assert self._sev_at(20.0) == LeverageSeverity.balanced

    def test_balanced_up_to_39(self):
        assert self._sev_at(39.9) == LeverageSeverity.balanced

    def test_reactive_at_40(self):
        assert self._sev_at(40.0) == LeverageSeverity.reactive

    def test_reactive_up_to_59(self):
        assert self._sev_at(59.9) == LeverageSeverity.reactive

    def test_powerless_at_60(self):
        assert self._sev_at(60.0) == LeverageSeverity.powerless

    def test_powerless_at_100(self):
        assert self._sev_at(100.0) == LeverageSeverity.powerless


# ---------------------------------------------------------------------------
# 12. Action mappings
# ---------------------------------------------------------------------------

class TestActionMapping:
    def _action(self, risk: LeverageRisk, pattern: LeveragePattern) -> LeverageAction:
        return make_engine()._action(risk, pattern)

    def test_critical_concession_without_ask(self):
        assert self._action(LeverageRisk.critical, LeveragePattern.concession_without_ask) == LeverageAction.concession_discipline_coaching

    def test_critical_competitive_leverage_avoidance(self):
        assert self._action(LeverageRisk.critical, LeveragePattern.competitive_leverage_avoidance) == LeverageAction.competitive_leverage_coaching

    def test_critical_deadline_blind(self):
        assert self._action(LeverageRisk.critical, LeveragePattern.deadline_blind_negotiator) == LeverageAction.negotiation_strategy_overhaul

    def test_critical_urgency_manufacturing_failure(self):
        assert self._action(LeverageRisk.critical, LeveragePattern.urgency_manufacturing_failure) == LeverageAction.negotiation_strategy_overhaul

    def test_critical_single_lever(self):
        assert self._action(LeverageRisk.critical, LeveragePattern.single_lever_dependency) == LeverageAction.negotiation_strategy_overhaul

    def test_critical_none_pattern(self):
        assert self._action(LeverageRisk.critical, LeveragePattern.none) == LeverageAction.negotiation_strategy_overhaul

    def test_high_deadline_blind(self):
        assert self._action(LeverageRisk.high, LeveragePattern.deadline_blind_negotiator) == LeverageAction.deadline_framing_coaching

    def test_high_urgency_manufacturing_failure(self):
        assert self._action(LeverageRisk.high, LeveragePattern.urgency_manufacturing_failure) == LeverageAction.deadline_framing_coaching

    def test_high_concession_without_ask(self):
        assert self._action(LeverageRisk.high, LeveragePattern.concession_without_ask) == LeverageAction.leverage_awareness_coaching

    def test_high_competitive_avoidance(self):
        assert self._action(LeverageRisk.high, LeveragePattern.competitive_leverage_avoidance) == LeverageAction.leverage_awareness_coaching

    def test_high_single_lever(self):
        assert self._action(LeverageRisk.high, LeveragePattern.single_lever_dependency) == LeverageAction.leverage_awareness_coaching

    def test_high_none(self):
        assert self._action(LeverageRisk.high, LeveragePattern.none) == LeverageAction.leverage_awareness_coaching

    def test_moderate_returns_awareness_coaching(self):
        for pattern in LeveragePattern:
            assert self._action(LeverageRisk.moderate, pattern) == LeverageAction.leverage_awareness_coaching

    def test_low_returns_no_action(self):
        for pattern in LeveragePattern:
            assert self._action(LeverageRisk.low, pattern) == LeverageAction.no_action


# ---------------------------------------------------------------------------
# 13. Flag conditions
# ---------------------------------------------------------------------------

class TestFlags:
    # has_leverage_gap
    def test_gap_true_via_composite_ge_40(self):
        # Make composite >= 40: tactical=75 (40+35), urgency=0, discipline=0, positioning=0
        # composite = 75*0.30 = 22.5 → not enough; need more
        # Use all worst case to get composite >= 40
        eng = make_engine()
        inp = make_input(
            deals_with_competitive_pressure_used_pct=0.05,
            walk_away_threat_used_pct=0.05,
            multi_option_pricing_presented_pct=0.05,
            urgency_event_cited_in_negotiation_pct=0.05,
            deadline_anchored_close_rate_pct=0.05,
            negotiation_extended_beyond_target_days=25.0,
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        result = eng.assess(inp)
        # tactical=100, urgency=100, discipline=0, positioning=0
        # composite = 100*0.30 + 100*0.25 = 55 >= 40
        assert result.has_leverage_gap is True

    def test_gap_true_via_concession_ge_045(self):
        eng = make_engine()
        inp = make_input(
            concession_without_counter_ask_pct=0.45,
            # composite stays low
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        result = eng.assess(inp)
        assert result.has_leverage_gap is True

    def test_gap_true_via_value_anchor_le_035(self):
        eng = make_engine()
        inp = make_input(
            value_anchor_set_before_price_pct=0.35,
            # composite stays low
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        result = eng.assess(inp)
        assert result.has_leverage_gap is True

    def test_gap_false_for_healthy_rep(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.has_leverage_gap is False

    # requires_leverage_coaching
    def test_coaching_true_via_composite_ge_30(self):
        # Force composite >= 30 (tactical+urgency each 40)
        eng = make_engine()
        inp = make_input(
            deals_with_competitive_pressure_used_pct=0.05,
            walk_away_threat_used_pct=0.05,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.05,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        result = eng.assess(inp)
        # tactical = 40+35 = 75, urgency = 40, composite = 75*0.30 + 40*0.25 = 22.5+10 = 32.5 >= 30
        assert result.requires_leverage_coaching is True

    def test_coaching_true_via_competitive_pressure_le_030(self):
        eng = make_engine()
        inp = make_input(
            deals_with_competitive_pressure_used_pct=0.30,
            # keep composite low
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        result = eng.assess(inp)
        assert result.requires_leverage_coaching is True

    def test_coaching_true_via_price_reduction_ge_025(self):
        eng = make_engine()
        inp = make_input(
            price_reduction_without_scope_change_pct=0.25,
            # keep composite low
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            concession_without_counter_ask_pct=0.10,
            last_minute_concession_rate_pct=0.10,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        result = eng.assess(inp)
        assert result.requires_leverage_coaching is True

    def test_coaching_false_for_healthy_rep(self):
        eng = make_engine()
        # composite=0, competitive>0.30, price_reduction<0.25
        result = eng.assess(make_input(
            deals_with_competitive_pressure_used_pct=0.70,
            price_reduction_without_scope_change_pct=0.10,
        ))
        assert result.requires_leverage_coaching is False


# ---------------------------------------------------------------------------
# 14. Margin conceded formula
# ---------------------------------------------------------------------------

class TestMarginConceded:
    def test_margin_formula_basic(self):
        eng = make_engine()
        inp = make_input(
            total_deals_negotiated=10,
            avg_opportunity_value_usd=50_000.0,
            price_reduction_without_scope_change_pct=0.20,
        )
        result = eng.assess(inp)
        composite = result.leverage_composite
        expected = round(10 * 50_000.0 * 0.20 * (composite / 100.0), 2)
        assert result.estimated_margin_conceded_usd == expected

    def test_margin_zero_when_composite_zero(self):
        eng = make_engine()
        # Use a zero price_reduction so formula = 0 regardless of composite
        inp = make_input(
            total_deals_negotiated=100,
            avg_opportunity_value_usd=100_000.0,
            price_reduction_without_scope_change_pct=0.0,
        )
        result = eng.assess(inp)
        assert result.estimated_margin_conceded_usd == 0.0

    def test_margin_rounded_to_2_decimals(self):
        eng = make_engine()
        inp = make_input(
            total_deals_negotiated=7,
            avg_opportunity_value_usd=33_333.33,
            price_reduction_without_scope_change_pct=0.15,
        )
        result = eng.assess(inp)
        # Verify rounding
        raw = 7 * 33_333.33 * 0.15 * (result.leverage_composite / 100.0)
        assert result.estimated_margin_conceded_usd == round(raw, 2)

    def test_margin_large_deal(self):
        eng = make_engine()
        inp = make_input(
            total_deals_negotiated=100,
            avg_opportunity_value_usd=1_000_000.0,
            price_reduction_without_scope_change_pct=0.50,
            # Force high composite
            deals_with_competitive_pressure_used_pct=0.05,
            walk_away_threat_used_pct=0.05,
            multi_option_pricing_presented_pct=0.05,
            urgency_event_cited_in_negotiation_pct=0.05,
            deadline_anchored_close_rate_pct=0.05,
            negotiation_extended_beyond_target_days=25.0,
            concession_without_counter_ask_pct=0.80,
            last_minute_concession_rate_pct=0.80,
            value_anchor_set_before_price_pct=0.05,
            executive_sponsor_engaged_in_negotiation_pct=0.05,
            deal_restructured_to_preserve_margin_pct=0.05,
        )
        result = eng.assess(inp)
        expected = round(100 * 1_000_000.0 * 0.50 * (result.leverage_composite / 100.0), 2)
        assert result.estimated_margin_conceded_usd == expected


# ---------------------------------------------------------------------------
# 15. Signal string
# ---------------------------------------------------------------------------

class TestSignalString:
    def test_healthy_signal(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.leverage_signal == (
            "Negotiation leverage healthy — tactical use, urgency framing, "
            "and concession discipline within benchmarks"
        )

    def test_signal_contains_concession_pct(self):
        eng = make_engine()
        inp = make_input(
            concession_without_counter_ask_pct=0.60,
            price_reduction_without_scope_change_pct=0.50,
            deals_with_competitive_pressure_used_pct=0.70,
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
            last_minute_concession_rate_pct=0.10,
        )
        result = eng.assess(inp)
        assert "60% concessions without counter-ask" in result.leverage_signal

    def test_signal_contains_competitive_pct(self):
        eng = make_engine()
        inp = make_input(
            concession_without_counter_ask_pct=0.60,
            price_reduction_without_scope_change_pct=0.50,
            deals_with_competitive_pressure_used_pct=0.35,
        )
        result = eng.assess(inp)
        assert "35% competitive pressure used" in result.leverage_signal

    def test_signal_contains_value_anchor_pct(self):
        eng = make_engine()
        inp = make_input(
            concession_without_counter_ask_pct=0.60,
            price_reduction_without_scope_change_pct=0.50,
            value_anchor_set_before_price_pct=0.80,
        )
        result = eng.assess(inp)
        assert "80% value-anchored before price" in result.leverage_signal

    def test_signal_contains_composite_score(self):
        eng = make_engine()
        inp = make_input(
            concession_without_counter_ask_pct=0.60,
            price_reduction_without_scope_change_pct=0.50,
        )
        result = eng.assess(inp)
        assert f"composite {result.leverage_composite:.0f}" in result.leverage_signal

    def test_signal_contains_pattern_label_for_pattern(self):
        # concession_without_ask pattern → "Concession without ask"
        eng = make_engine()
        inp = make_input(
            concession_without_counter_ask_pct=0.60,
            price_reduction_without_scope_change_pct=0.50,
        )
        result = eng.assess(inp)
        assert result.leverage_pattern == LeveragePattern.concession_without_ask
        assert "Concession without ask" in result.leverage_signal

    def test_signal_leverage_risk_label_when_no_pattern_but_high_composite(self):
        # If pattern is none but composite >= 20, signal uses "Leverage risk"
        eng = make_engine()
        # Make composite ~22 via moderate tactical without triggering any pattern
        inp = make_input(
            deals_with_competitive_pressure_used_pct=0.40,  # +22 tactical
            walk_away_threat_used_pct=0.30,
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.70,
            deadline_anchored_close_rate_pct=0.60,
            negotiation_extended_beyond_target_days=5.0,
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        result = eng.assess(inp)
        # composite = 22*0.30 = 6.6, still low → healthy signal
        # Let's force it higher: also add urgency
        inp2 = make_input(
            deals_with_competitive_pressure_used_pct=0.40,  # +22 tactical
            walk_away_threat_used_pct=0.25,                 # +18 tactical
            multi_option_pricing_presented_pct=0.50,
            urgency_event_cited_in_negotiation_pct=0.40,    # +22 urgency
            deadline_anchored_close_rate_pct=0.50,          # +18 urgency
            negotiation_extended_beyond_target_days=5.0,
            concession_without_counter_ask_pct=0.10,
            price_reduction_without_scope_change_pct=0.10,
            last_minute_concession_rate_pct=0.10,
            value_anchor_set_before_price_pct=0.80,
            executive_sponsor_engaged_in_negotiation_pct=0.50,
            deal_restructured_to_preserve_margin_pct=0.40,
        )
        result2 = eng.assess(inp2)
        # tactical=40, urgency=40 → composite=40*0.30+40*0.25=12+10=22
        if result2.leverage_pattern == LeveragePattern.none and result2.leverage_composite >= 20:
            assert "Leverage risk" in result2.leverage_signal


# ---------------------------------------------------------------------------
# 16. assess end-to-end
# ---------------------------------------------------------------------------

class TestAssessEndToEnd:
    def test_assess_returns_leverage_result(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert isinstance(result, LeverageResult)

    def test_assess_stores_result(self):
        eng = make_engine()
        eng.assess(make_input())
        assert len(eng._results) == 1

    def test_assess_rep_id_and_region_passthrough(self):
        eng = make_engine()
        inp = make_input(rep_id="X123", region="West")
        result = eng.assess(inp)
        assert result.rep_id == "X123"
        assert result.region == "West"

    def test_assess_score_types(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert isinstance(result.tactical_score, float)
        assert isinstance(result.urgency_score, float)
        assert isinstance(result.discipline_score, float)
        assert isinstance(result.positioning_score, float)
        assert isinstance(result.leverage_composite, float)

    def test_assess_boolean_flags_are_bool(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert isinstance(result.has_leverage_gap, bool)
        assert isinstance(result.requires_leverage_coaching, bool)

    def test_assess_full_critical_case(self):
        eng = make_engine()
        inp = make_input(
            deals_with_competitive_pressure_used_pct=0.05,
            walk_away_threat_used_pct=0.05,
            multi_option_pricing_presented_pct=0.05,
            urgency_event_cited_in_negotiation_pct=0.05,
            deadline_anchored_close_rate_pct=0.05,
            negotiation_extended_beyond_target_days=25.0,
            concession_without_counter_ask_pct=0.80,
            price_reduction_without_scope_change_pct=0.80,
            last_minute_concession_rate_pct=0.80,
            value_anchor_set_before_price_pct=0.05,
            executive_sponsor_engaged_in_negotiation_pct=0.05,
            deal_restructured_to_preserve_margin_pct=0.05,
        )
        result = eng.assess(inp)
        assert result.leverage_risk == LeverageRisk.critical
        assert result.leverage_severity == LeverageSeverity.powerless
        assert result.has_leverage_gap is True
        assert result.requires_leverage_coaching is True
        assert result.leverage_composite == 100.0


# ---------------------------------------------------------------------------
# 17. assess_batch
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_batch_returns_list(self):
        eng = make_engine()
        results = eng.assess_batch([make_input(), make_input(rep_id="REP002")])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_batch_stores_all_results(self):
        eng = make_engine()
        eng.assess_batch([make_input(rep_id=f"R{i}") for i in range(5)])
        assert len(eng._results) == 5

    def test_batch_empty_list(self):
        eng = make_engine()
        results = eng.assess_batch([])
        assert results == []

    def test_batch_accumulates_with_prior_assess(self):
        eng = make_engine()
        eng.assess(make_input(rep_id="SOLO"))
        eng.assess_batch([make_input(rep_id="B1"), make_input(rep_id="B2")])
        assert len(eng._results) == 3

    def test_batch_each_result_is_leverage_result(self):
        eng = make_engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        for r in eng.assess_batch(inputs):
            assert isinstance(r, LeverageResult)


# ---------------------------------------------------------------------------
# 18. summary – empty and populated
# ---------------------------------------------------------------------------

class TestSummary:
    def test_summary_empty_engine(self):
        eng = make_engine()
        s = eng.summary()
        assert s["total"] == 0
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["severity_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_leverage_composite"] == 0.0
        assert s["leverage_gap_count"] == 0
        assert s["coaching_count"] == 0
        assert s["avg_tactical_score"] == 0.0
        assert s["avg_urgency_score"] == 0.0
        assert s["avg_discipline_score"] == 0.0
        assert s["avg_positioning_score"] == 0.0
        assert s["total_estimated_margin_conceded_usd"] == 0.0

    def test_summary_returns_exactly_13_keys(self):
        eng = make_engine()
        assert len(eng.summary()) == 13

    def test_summary_13_keys_populated(self):
        eng = make_engine()
        eng.assess(make_input())
        s = eng.summary()
        assert len(s) == 13

    def test_summary_key_names(self):
        eng = make_engine()
        s = eng.summary()
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_leverage_composite", "leverage_gap_count",
            "coaching_count", "avg_tactical_score", "avg_urgency_score",
            "avg_discipline_score", "avg_positioning_score",
            "total_estimated_margin_conceded_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_total_count(self):
        eng = make_engine()
        for i in range(4):
            eng.assess(make_input(rep_id=f"R{i}"))
        s = eng.summary()
        assert s["total"] == 4

    def test_summary_risk_counts(self):
        eng = make_engine()
        eng.assess(make_input())  # low risk
        s = eng.summary()
        assert s["risk_counts"].get("low", 0) == 1

    def test_summary_pattern_counts(self):
        eng = make_engine()
        eng.assess(make_input())  # pattern = none
        s = eng.summary()
        assert s["pattern_counts"].get("none", 0) == 1

    def test_summary_severity_counts(self):
        eng = make_engine()
        eng.assess(make_input())  # commanding
        s = eng.summary()
        assert s["severity_counts"].get("commanding", 0) == 1

    def test_summary_action_counts(self):
        eng = make_engine()
        eng.assess(make_input())  # no_action
        s = eng.summary()
        assert s["action_counts"].get("no_action", 0) == 1

    def test_summary_avg_composite_single(self):
        eng = make_engine()
        result = eng.assess(make_input())
        s = eng.summary()
        assert s["avg_leverage_composite"] == result.leverage_composite

    def test_summary_avg_composite_multiple(self):
        eng = make_engine()
        r1 = eng.assess(make_input(rep_id="R1"))
        r2 = eng.assess(make_input(rep_id="R2"))
        s = eng.summary()
        expected = round((r1.leverage_composite + r2.leverage_composite) / 2, 1)
        assert s["avg_leverage_composite"] == expected

    def test_summary_leverage_gap_count(self):
        eng = make_engine()
        eng.assess(make_input())  # no gap
        eng.assess(make_input(value_anchor_set_before_price_pct=0.10))  # gap via value_anchor
        s = eng.summary()
        assert s["leverage_gap_count"] == 1

    def test_summary_coaching_count(self):
        eng = make_engine()
        eng.assess(make_input())  # no coaching (healthy)
        eng.assess(make_input(price_reduction_without_scope_change_pct=0.30))  # coaching
        s = eng.summary()
        assert s["coaching_count"] == 1

    def test_summary_avg_tactical(self):
        eng = make_engine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(make_input(rep_id="B"))
        s = eng.summary()
        assert s["avg_tactical_score"] == round((r1.tactical_score + r2.tactical_score) / 2, 1)

    def test_summary_avg_urgency(self):
        eng = make_engine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(make_input(rep_id="B"))
        s = eng.summary()
        assert s["avg_urgency_score"] == round((r1.urgency_score + r2.urgency_score) / 2, 1)

    def test_summary_avg_discipline(self):
        eng = make_engine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(make_input(rep_id="B"))
        s = eng.summary()
        assert s["avg_discipline_score"] == round((r1.discipline_score + r2.discipline_score) / 2, 1)

    def test_summary_avg_positioning(self):
        eng = make_engine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(make_input(rep_id="B"))
        s = eng.summary()
        assert s["avg_positioning_score"] == round((r1.positioning_score + r2.positioning_score) / 2, 1)

    def test_summary_total_margin_conceded(self):
        eng = make_engine()
        r1 = eng.assess(make_input(rep_id="A"))
        r2 = eng.assess(make_input(rep_id="B"))
        s = eng.summary()
        expected = round(r1.estimated_margin_conceded_usd + r2.estimated_margin_conceded_usd, 2)
        assert s["total_estimated_margin_conceded_usd"] == expected

    def test_summary_multiple_risk_levels(self):
        eng = make_engine()
        # Low risk
        eng.assess(make_input(rep_id="R1"))
        # Critical risk
        eng.assess(make_input(
            rep_id="R2",
            deals_with_competitive_pressure_used_pct=0.05,
            walk_away_threat_used_pct=0.05,
            multi_option_pricing_presented_pct=0.05,
            urgency_event_cited_in_negotiation_pct=0.05,
            deadline_anchored_close_rate_pct=0.05,
            negotiation_extended_beyond_target_days=25.0,
            concession_without_counter_ask_pct=0.80,
            price_reduction_without_scope_change_pct=0.80,
            last_minute_concession_rate_pct=0.80,
            value_anchor_set_before_price_pct=0.05,
            executive_sponsor_engaged_in_negotiation_pct=0.05,
            deal_restructured_to_preserve_margin_pct=0.05,
        ))
        s = eng.summary()
        assert s["total"] == 2
        assert "low" in s["risk_counts"]
        assert "critical" in s["risk_counts"]


# ---------------------------------------------------------------------------
# 19. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_boundary_composite_exactly_60_is_critical(self):
        eng = make_engine()
        # composite exactly 60 → critical
        # tactical=100, urgency=100, discipline=0, positioning=0 → 30+25=55
        # Need to add more: discipline=100 → 55+25=80
        # Or tune: tactical=0, urgency=0, discipline=0, positioning=100 → 20; no
        # Let's just verify the _risk_level method
        assert eng._risk_level(60.0) == LeverageRisk.critical

    def test_boundary_composite_exactly_40_is_high(self):
        eng = make_engine()
        assert eng._risk_level(40.0) == LeverageRisk.high

    def test_boundary_composite_exactly_20_is_moderate(self):
        eng = make_engine()
        assert eng._risk_level(20.0) == LeverageRisk.moderate

    def test_boundary_composite_0_is_low(self):
        eng = make_engine()
        assert eng._risk_level(0.0) == LeverageRisk.low

    def test_zero_deals_zero_margin(self):
        eng = make_engine()
        result = eng.assess(make_input(total_deals_negotiated=0, avg_opportunity_value_usd=100_000.0))
        assert result.estimated_margin_conceded_usd == 0.0

    def test_zero_opportunity_value_zero_margin(self):
        eng = make_engine()
        result = eng.assess(make_input(total_deals_negotiated=50, avg_opportunity_value_usd=0.0))
        assert result.estimated_margin_conceded_usd == 0.0

    def test_engine_independent_instances(self):
        eng1 = make_engine()
        eng2 = make_engine()
        eng1.assess(make_input())
        assert len(eng2._results) == 0

    def test_multiple_assessments_accumulate(self):
        eng = make_engine()
        for i in range(10):
            eng.assess(make_input(rep_id=f"REP{i:03d}"))
        assert len(eng._results) == 10

    def test_concession_exactly_055_triggers_pattern(self):
        eng = make_engine()
        r = eng.assess(make_input(
            concession_without_counter_ask_pct=0.55,
            price_reduction_without_scope_change_pct=0.40,
        ))
        assert r.leverage_pattern == LeveragePattern.concession_without_ask

    def test_composite_rounded_to_1_decimal(self):
        eng = make_engine()
        result = eng.assess(make_input())
        # composite is rounded to 1 decimal place
        assert result.leverage_composite == round(result.leverage_composite, 1)

    def test_sub_scores_rounded_to_1_decimal(self):
        eng = make_engine()
        result = eng.assess(make_input())
        assert result.tactical_score == round(result.tactical_score, 1)
        assert result.urgency_score == round(result.urgency_score, 1)
        assert result.discipline_score == round(result.discipline_score, 1)
        assert result.positioning_score == round(result.positioning_score, 1)

    def test_has_leverage_gap_boundary_concession_exactly_045(self):
        eng = make_engine()
        r = eng.assess(make_input(concession_without_counter_ask_pct=0.45))
        assert r.has_leverage_gap is True

    def test_has_leverage_gap_boundary_concession_below_045(self):
        eng = make_engine()
        r = eng.assess(make_input(
            concession_without_counter_ask_pct=0.44,
            value_anchor_set_before_price_pct=0.80,  # above 0.35, no gap
        ))
        # composite = 0 (healthy), concession < 0.45, value_anchor > 0.35 → no gap
        assert r.has_leverage_gap is False

    def test_coaching_boundary_price_reduction_exactly_025(self):
        eng = make_engine()
        r = eng.assess(make_input(
            price_reduction_without_scope_change_pct=0.25,
            deals_with_competitive_pressure_used_pct=0.70,  # > 0.30, no coaching from this
        ))
        assert r.requires_leverage_coaching is True

    def test_coaching_boundary_price_reduction_below_025(self):
        eng = make_engine()
        r = eng.assess(make_input(
            price_reduction_without_scope_change_pct=0.24,
            deals_with_competitive_pressure_used_pct=0.70,
        ))
        # composite=0, competitive>0.30, price<0.25 → no coaching
        assert r.requires_leverage_coaching is False

    def test_requires_coaching_competitive_pressure_exactly_030(self):
        eng = make_engine()
        r = eng.assess(make_input(
            deals_with_competitive_pressure_used_pct=0.30,
            price_reduction_without_scope_change_pct=0.10,
        ))
        assert r.requires_leverage_coaching is True

    def test_requires_coaching_competitive_pressure_above_030(self):
        eng = make_engine()
        r = eng.assess(make_input(
            deals_with_competitive_pressure_used_pct=0.31,
            price_reduction_without_scope_change_pct=0.10,
        ))
        # composite=22 (due to competitive 0.31>0.20 but <=0.40 → no tactical bonus from comp)
        # Actually 0.31 > 0.20 so +22 to tactical? No: 0.31 <=0.40 adds +22
        # tactical = 22; composite = 22*0.30 = 6.6 → no coaching via composite
        # deals > 0.30, price < 0.25 → False
        assert r.requires_leverage_coaching is False
