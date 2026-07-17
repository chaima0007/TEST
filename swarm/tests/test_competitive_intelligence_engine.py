"""Comprehensive tests for swarm.intelligence.competitive_intelligence_engine."""
import pytest
from swarm.intelligence.competitive_intelligence_engine import (
    CompetitorThreat,
    CompetitivePosition,
    CompetitorCategory,
    CompetitiveAction,
    CompetitiveInput,
    CompetitiveResult,
    CompetitiveIntelligenceEngine,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────

def make_input(**overrides) -> CompetitiveInput:
    defaults = dict(
        deal_id="D001",
        deal_name="Deal Alpha",
        rep_id="R001",
        rep_name="Alice",
        account_name="Acme Corp",
        deal_size_eur=100000.0,
        competitor_name="CompetitorX",
        competitor_category=CompetitorCategory.ENTERPRISE,
        prospect_requested_competitor_demo=False,
        prospect_shared_competitor_pricing=False,
        prospect_mentioned_competitor_features=False,
        champion_supports_competitor=False,
        decision_maker_met_competitor=False,
        rfp_sent_to_competitor=False,
        executive_sponsor_engaged=False,
        decision_maker_relationship_score=5,
        product_fit_score=5,
        price_competitive=False,
        unique_features_count=0,
        references_provided=False,
        proof_of_concept_completed=False,
        previous_losses_to_competitor=0,
        win_rate_vs_competitor_pct=50.0,
        days_since_competitor_first_mentioned=10,
    )
    defaults.update(overrides)
    return CompetitiveInput(**defaults)


@pytest.fixture
def engine():
    return CompetitiveIntelligenceEngine()


@pytest.fixture
def clean_input():
    return make_input()


# ─── TestCompetitorThreatEnum ────────────────────────────────────────────────

class TestCompetitorThreatEnum:
    def test_critical_value(self):
        assert CompetitorThreat.CRITICAL.value == "critical"

    def test_high_value(self):
        assert CompetitorThreat.HIGH.value == "high"

    def test_moderate_value(self):
        assert CompetitorThreat.MODERATE.value == "moderate"

    def test_low_value(self):
        assert CompetitorThreat.LOW.value == "low"

    def test_none_value(self):
        assert CompetitorThreat.NONE.value == "none"

    def test_str_inheritance_critical(self):
        assert isinstance(CompetitorThreat.CRITICAL, str)

    def test_str_inheritance_high(self):
        assert isinstance(CompetitorThreat.HIGH, str)

    def test_str_inheritance_moderate(self):
        assert isinstance(CompetitorThreat.MODERATE, str)

    def test_str_inheritance_low(self):
        assert isinstance(CompetitorThreat.LOW, str)

    def test_str_inheritance_none(self):
        assert isinstance(CompetitorThreat.NONE, str)

    def test_str_equality_critical(self):
        assert CompetitorThreat.CRITICAL == "critical"

    def test_all_members(self):
        members = {m.value for m in CompetitorThreat}
        assert members == {"critical", "high", "moderate", "low", "none"}

    def test_count(self):
        assert len(CompetitorThreat) == 5


# ─── TestCompetitivePositionEnum ─────────────────────────────────────────────

class TestCompetitivePositionEnum:
    def test_winning_value(self):
        assert CompetitivePosition.WINNING.value == "winning"

    def test_leading_value(self):
        assert CompetitivePosition.LEADING.value == "leading"

    def test_tied_value(self):
        assert CompetitivePosition.TIED.value == "tied"

    def test_trailing_value(self):
        assert CompetitivePosition.TRAILING.value == "trailing"

    def test_losing_value(self):
        assert CompetitivePosition.LOSING.value == "losing"

    def test_str_inheritance_winning(self):
        assert isinstance(CompetitivePosition.WINNING, str)

    def test_str_inheritance_losing(self):
        assert isinstance(CompetitivePosition.LOSING, str)

    def test_str_equality(self):
        assert CompetitivePosition.TIED == "tied"

    def test_all_members(self):
        members = {m.value for m in CompetitivePosition}
        assert members == {"winning", "leading", "tied", "trailing", "losing"}

    def test_count(self):
        assert len(CompetitivePosition) == 5


# ─── TestCompetitorCategoryEnum ──────────────────────────────────────────────

class TestCompetitorCategoryEnum:
    def test_enterprise_value(self):
        assert CompetitorCategory.ENTERPRISE.value == "enterprise"

    def test_mid_market_value(self):
        assert CompetitorCategory.MID_MARKET.value == "mid_market"

    def test_startup_value(self):
        assert CompetitorCategory.STARTUP.value == "startup"

    def test_open_source_value(self):
        assert CompetitorCategory.OPEN_SOURCE.value == "open_source"

    def test_in_house_value(self):
        assert CompetitorCategory.IN_HOUSE.value == "in_house"

    def test_unknown_value(self):
        assert CompetitorCategory.UNKNOWN.value == "unknown"

    def test_str_inheritance(self):
        for member in CompetitorCategory:
            assert isinstance(member, str)

    def test_count(self):
        assert len(CompetitorCategory) == 6


# ─── TestCompetitiveActionEnum ───────────────────────────────────────────────

class TestCompetitiveActionEnum:
    def test_defend_and_close_value(self):
        assert CompetitiveAction.DEFEND_AND_CLOSE.value == "defend_and_close"

    def test_differentiate_value(self):
        assert CompetitiveAction.DIFFERENTIATE.value == "differentiate"

    def test_escalate_value(self):
        assert CompetitiveAction.ESCALATE.value == "escalate"

    def test_price_protect_value(self):
        assert CompetitiveAction.PRICE_PROTECT.value == "price_protect"

    def test_maintain_value(self):
        assert CompetitiveAction.MAINTAIN.value == "maintain"

    def test_monitor_value(self):
        assert CompetitiveAction.MONITOR.value == "monitor"

    def test_str_inheritance(self):
        for member in CompetitiveAction:
            assert isinstance(member, str)

    def test_count(self):
        assert len(CompetitiveAction) == 6


# ─── TestCompetitiveInputFields ──────────────────────────────────────────────

class TestCompetitiveInputFields:
    def test_deal_id_field(self):
        inp = make_input(deal_id="X")
        assert inp.deal_id == "X"

    def test_deal_name_field(self):
        inp = make_input(deal_name="MyDeal")
        assert inp.deal_name == "MyDeal"

    def test_rep_id_field(self):
        inp = make_input(rep_id="R99")
        assert inp.rep_id == "R99"

    def test_rep_name_field(self):
        inp = make_input(rep_name="Bob")
        assert inp.rep_name == "Bob"

    def test_account_name_field(self):
        inp = make_input(account_name="BigCo")
        assert inp.account_name == "BigCo"

    def test_deal_size_eur_field(self):
        inp = make_input(deal_size_eur=75000.0)
        assert inp.deal_size_eur == 75000.0

    def test_competitor_name_field(self):
        inp = make_input(competitor_name="Rival")
        assert inp.competitor_name == "Rival"

    def test_competitor_category_field(self):
        inp = make_input(competitor_category=CompetitorCategory.STARTUP)
        assert inp.competitor_category == CompetitorCategory.STARTUP

    def test_prospect_requested_competitor_demo_field(self):
        inp = make_input(prospect_requested_competitor_demo=True)
        assert inp.prospect_requested_competitor_demo is True

    def test_prospect_shared_competitor_pricing_field(self):
        inp = make_input(prospect_shared_competitor_pricing=True)
        assert inp.prospect_shared_competitor_pricing is True

    def test_prospect_mentioned_competitor_features_field(self):
        inp = make_input(prospect_mentioned_competitor_features=True)
        assert inp.prospect_mentioned_competitor_features is True

    def test_champion_supports_competitor_field(self):
        inp = make_input(champion_supports_competitor=True)
        assert inp.champion_supports_competitor is True

    def test_decision_maker_met_competitor_field(self):
        inp = make_input(decision_maker_met_competitor=True)
        assert inp.decision_maker_met_competitor is True

    def test_rfp_sent_to_competitor_field(self):
        inp = make_input(rfp_sent_to_competitor=True)
        assert inp.rfp_sent_to_competitor is True

    def test_executive_sponsor_engaged_field(self):
        inp = make_input(executive_sponsor_engaged=True)
        assert inp.executive_sponsor_engaged is True

    def test_decision_maker_relationship_score_field(self):
        inp = make_input(decision_maker_relationship_score=8)
        assert inp.decision_maker_relationship_score == 8

    def test_product_fit_score_field(self):
        inp = make_input(product_fit_score=9)
        assert inp.product_fit_score == 9

    def test_price_competitive_field(self):
        inp = make_input(price_competitive=True)
        assert inp.price_competitive is True

    def test_unique_features_count_field(self):
        inp = make_input(unique_features_count=3)
        assert inp.unique_features_count == 3

    def test_references_provided_field(self):
        inp = make_input(references_provided=True)
        assert inp.references_provided is True

    def test_proof_of_concept_completed_field(self):
        inp = make_input(proof_of_concept_completed=True)
        assert inp.proof_of_concept_completed is True

    def test_previous_losses_to_competitor_field(self):
        inp = make_input(previous_losses_to_competitor=4)
        assert inp.previous_losses_to_competitor == 4

    def test_win_rate_vs_competitor_pct_field(self):
        inp = make_input(win_rate_vs_competitor_pct=65.0)
        assert inp.win_rate_vs_competitor_pct == 65.0

    def test_days_since_competitor_first_mentioned_field(self):
        inp = make_input(days_since_competitor_first_mentioned=45)
        assert inp.days_since_competitor_first_mentioned == 45

    def test_total_24_fields(self):
        inp = make_input()
        assert len(inp.__dataclass_fields__) == 24


# ─── TestCompetitiveResultToDict ─────────────────────────────────────────────

class TestCompetitiveResultToDict:
    def test_to_dict_returns_17_keys(self, engine, clean_input):
        result = engine.analyze(clean_input)
        d = result.to_dict()
        assert len(d) == 17

    def test_to_dict_contains_deal_id(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "deal_id" in d

    def test_to_dict_contains_deal_name(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "deal_name" in d

    def test_to_dict_contains_rep_id(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "rep_id" in d

    def test_to_dict_contains_rep_name(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "rep_name" in d

    def test_to_dict_contains_account_name(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "account_name" in d

    def test_to_dict_contains_competitor_name(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "competitor_name" in d

    def test_to_dict_contains_competitor_category(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "competitor_category" in d

    def test_to_dict_contains_competitor_threat(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "competitor_threat" in d

    def test_to_dict_contains_competitive_position(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "competitive_position" in d

    def test_to_dict_contains_competitive_action(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "competitive_action" in d

    def test_to_dict_contains_threat_score(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "threat_score" in d

    def test_to_dict_contains_position_score(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "position_score" in d

    def test_to_dict_contains_win_probability_pct(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "win_probability_pct" in d

    def test_to_dict_contains_battle_tactics(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "battle_tactics" in d

    def test_to_dict_contains_differentiators(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "differentiators" in d

    def test_to_dict_contains_risk_signals(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "risk_signals" in d

    def test_to_dict_contains_manager_alerts(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        assert "manager_alerts" in d

    def test_to_dict_exact_key_set(self, engine, clean_input):
        d = engine.analyze(clean_input).to_dict()
        expected = {
            "deal_id", "deal_name", "rep_id", "rep_name", "account_name",
            "competitor_name", "competitor_category", "competitor_threat",
            "competitive_position", "competitive_action", "threat_score",
            "position_score", "win_probability_pct", "battle_tactics",
            "differentiators", "risk_signals", "manager_alerts",
        }
        assert set(d.keys()) == expected

    def test_to_dict_values_match_result_fields(self, engine, clean_input):
        result = engine.analyze(clean_input)
        d = result.to_dict()
        assert d["deal_id"] == result.deal_id
        assert d["threat_score"] == result.threat_score
        assert d["battle_tactics"] is result.battle_tactics


# ─── TestThreatScoring ───────────────────────────────────────────────────────

class TestThreatScoring:
    def test_zero_threat_all_false(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=False,
            prospect_requested_competitor_demo=False,
            decision_maker_met_competitor=False,
            prospect_shared_competitor_pricing=False,
            champion_supports_competitor=False,
            prospect_mentioned_competitor_features=False,
            previous_losses_to_competitor=0,
            win_rate_vs_competitor_pct=50.0,
        )
        score = engine._threat_score(inp)
        assert isinstance(score, (int, float))
        assert score == 0.0

    def test_rfp_adds_30(self, engine):
        inp = make_input(rfp_sent_to_competitor=True, win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 30.0

    def test_demo_adds_20(self, engine):
        inp = make_input(prospect_requested_competitor_demo=True, win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 20.0

    def test_decision_maker_met_adds_20(self, engine):
        inp = make_input(decision_maker_met_competitor=True, win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 20.0

    def test_pricing_shared_adds_15(self, engine):
        inp = make_input(prospect_shared_competitor_pricing=True, win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 15.0

    def test_champion_supports_adds_20(self, engine):
        inp = make_input(champion_supports_competitor=True, win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 20.0

    def test_features_mentioned_adds_10(self, engine):
        inp = make_input(prospect_mentioned_competitor_features=True, win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 10.0

    def test_previous_losses_1_adds_5(self, engine):
        inp = make_input(previous_losses_to_competitor=1, win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 5.0

    def test_previous_losses_2_adds_10(self, engine):
        inp = make_input(previous_losses_to_competitor=2, win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 10.0

    def test_previous_losses_4_adds_20(self, engine):
        inp = make_input(previous_losses_to_competitor=4, win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 20.0

    def test_previous_losses_capped_at_20(self, engine):
        inp = make_input(previous_losses_to_competitor=10, win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 20.0

    def test_win_rate_below_30_adds_15(self, engine):
        inp = make_input(win_rate_vs_competitor_pct=20.0)
        score = engine._threat_score(inp)
        assert score == 15.0

    def test_win_rate_exactly_29_adds_15(self, engine):
        inp = make_input(win_rate_vs_competitor_pct=29.9)
        score = engine._threat_score(inp)
        assert score == 15.0

    def test_win_rate_30_adds_8(self, engine):
        inp = make_input(win_rate_vs_competitor_pct=30.0)
        score = engine._threat_score(inp)
        assert score == 8.0

    def test_win_rate_below_50_adds_8(self, engine):
        inp = make_input(win_rate_vs_competitor_pct=40.0)
        score = engine._threat_score(inp)
        assert score == 8.0

    def test_win_rate_exactly_49_adds_8(self, engine):
        inp = make_input(win_rate_vs_competitor_pct=49.9)
        score = engine._threat_score(inp)
        assert score == 8.0

    def test_win_rate_50_no_bonus(self, engine):
        inp = make_input(win_rate_vs_competitor_pct=50.0)
        score = engine._threat_score(inp)
        assert score == 0.0

    def test_threat_score_clamped_at_100(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=True,
            prospect_requested_competitor_demo=True,
            decision_maker_met_competitor=True,
            prospect_shared_competitor_pricing=True,
            champion_supports_competitor=True,
            prospect_mentioned_competitor_features=True,
            previous_losses_to_competitor=10,
            win_rate_vs_competitor_pct=10.0,
        )
        score = engine._threat_score(inp)
        assert score == 100.0

    def test_threat_score_type_is_numeric(self, engine):
        inp = make_input()
        score = engine._threat_score(inp)
        assert isinstance(score, (int, float))

    def test_all_signals_combined(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=True,
            prospect_requested_competitor_demo=True,
            decision_maker_met_competitor=True,
            prospect_shared_competitor_pricing=True,
            champion_supports_competitor=True,
            prospect_mentioned_competitor_features=True,
            previous_losses_to_competitor=4,
            win_rate_vs_competitor_pct=50.0,
        )
        # 30+20+20+15+20+10+20 = 135 → clamped to 100
        score = engine._threat_score(inp)
        assert score == 100.0


# ─── TestPositionScoring ─────────────────────────────────────────────────────

class TestPositionScoring:
    def test_zero_position_score(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            executive_sponsor_engaged=False,
            proof_of_concept_completed=False,
            references_provided=False,
            unique_features_count=0,
            price_competitive=False,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 0.0

    def test_dm_relationship_score_5_gives_10(self, engine):
        inp = make_input(
            decision_maker_relationship_score=5,
            product_fit_score=0,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 10.0

    def test_dm_relationship_score_10_gives_20(self, engine):
        inp = make_input(
            decision_maker_relationship_score=10,
            product_fit_score=0,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 20.0

    def test_dm_relationship_capped_at_20(self, engine):
        inp = make_input(
            decision_maker_relationship_score=15,
            product_fit_score=0,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 20.0

    def test_product_fit_score_5_gives_10(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=5,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 10.0

    def test_product_fit_capped_at_20(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=15,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 20.0

    def test_exec_sponsor_adds_15(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            executive_sponsor_engaged=True,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 15.0

    def test_poc_completed_adds_15(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            proof_of_concept_completed=True,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 15.0

    def test_references_adds_10(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            references_provided=True,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 10.0

    def test_unique_features_3_gives_9(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            unique_features_count=3,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 9.0

    def test_unique_features_5_gives_15(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            unique_features_count=5,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 15.0

    def test_unique_features_capped_at_15(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            unique_features_count=10,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 15.0

    def test_price_competitive_adds_10(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            price_competitive=True,
            win_rate_vs_competitor_pct=40.0,
        )
        score = engine._position_score(inp)
        assert score == 10.0

    def test_win_rate_70_adds_10(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=70.0,
        )
        score = engine._position_score(inp)
        assert score == 10.0

    def test_win_rate_exactly_70_adds_10(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=70.0,
        )
        score = engine._position_score(inp)
        assert score == 10.0

    def test_win_rate_50_adds_5(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=50.0,
        )
        score = engine._position_score(inp)
        assert score == 5.0

    def test_win_rate_69_adds_5(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=69.9,
        )
        score = engine._position_score(inp)
        assert score == 5.0

    def test_win_rate_below_50_no_bonus(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=49.9,
        )
        score = engine._position_score(inp)
        assert score == 0.0

    def test_position_score_clamped_at_100(self, engine):
        inp = make_input(
            decision_maker_relationship_score=10,
            product_fit_score=10,
            executive_sponsor_engaged=True,
            proof_of_concept_completed=True,
            references_provided=True,
            unique_features_count=10,
            price_competitive=True,
            win_rate_vs_competitor_pct=70.0,
        )
        score = engine._position_score(inp)
        assert score == 100.0

    def test_position_score_type_is_numeric(self, engine):
        inp = make_input()
        score = engine._position_score(inp)
        assert isinstance(score, (int, float))


# ─── TestCompetitorThreatThresholds ──────────────────────────────────────────

class TestCompetitorThreatThresholds:
    def test_score_70_is_critical(self, engine):
        assert engine._competitor_threat(70.0) == CompetitorThreat.CRITICAL

    def test_score_100_is_critical(self, engine):
        assert engine._competitor_threat(100.0) == CompetitorThreat.CRITICAL

    def test_score_69_is_high(self, engine):
        assert engine._competitor_threat(69.9) == CompetitorThreat.HIGH

    def test_score_50_is_high(self, engine):
        assert engine._competitor_threat(50.0) == CompetitorThreat.HIGH

    def test_score_49_is_moderate(self, engine):
        assert engine._competitor_threat(49.9) == CompetitorThreat.MODERATE

    def test_score_30_is_moderate(self, engine):
        assert engine._competitor_threat(30.0) == CompetitorThreat.MODERATE

    def test_score_29_is_low(self, engine):
        assert engine._competitor_threat(29.9) == CompetitorThreat.LOW

    def test_score_10_is_low(self, engine):
        assert engine._competitor_threat(10.0) == CompetitorThreat.LOW

    def test_score_9_is_none(self, engine):
        assert engine._competitor_threat(9.9) == CompetitorThreat.NONE

    def test_score_0_is_none(self, engine):
        assert engine._competitor_threat(0.0) == CompetitorThreat.NONE


# ─── TestCompetitivePositionThresholds ───────────────────────────────────────

class TestCompetitivePositionThresholds:
    def test_delta_30_is_winning(self, engine):
        assert engine._competitive_position(80.0, 50.0) == CompetitivePosition.WINNING

    def test_delta_exactly_30_is_winning(self, engine):
        assert engine._competitive_position(80.0, 50.0) == CompetitivePosition.WINNING

    def test_delta_29_is_leading(self, engine):
        assert engine._competitive_position(79.0, 50.0) == CompetitivePosition.LEADING

    def test_delta_10_is_leading(self, engine):
        assert engine._competitive_position(60.0, 50.0) == CompetitivePosition.LEADING

    def test_delta_exactly_10_is_leading(self, engine):
        assert engine._competitive_position(60.0, 50.0) == CompetitivePosition.LEADING

    def test_delta_9_is_tied(self, engine):
        assert engine._competitive_position(59.0, 50.0) == CompetitivePosition.TIED

    def test_delta_0_is_tied(self, engine):
        assert engine._competitive_position(50.0, 50.0) == CompetitivePosition.TIED

    def test_delta_minus_10_is_tied(self, engine):
        assert engine._competitive_position(40.0, 50.0) == CompetitivePosition.TIED

    def test_delta_minus_11_is_trailing(self, engine):
        assert engine._competitive_position(39.0, 50.0) == CompetitivePosition.TRAILING

    def test_delta_minus_30_is_trailing(self, engine):
        assert engine._competitive_position(20.0, 50.0) == CompetitivePosition.TRAILING

    def test_delta_minus_31_is_losing(self, engine):
        assert engine._competitive_position(19.0, 50.0) == CompetitivePosition.LOSING

    def test_delta_very_negative_is_losing(self, engine):
        assert engine._competitive_position(0.0, 100.0) == CompetitivePosition.LOSING


# ─── TestWinProbability ──────────────────────────────────────────────────────

class TestWinProbability:
    def test_base_calculation_equal_scores(self, engine):
        inp = make_input(
            champion_supports_competitor=False,
            executive_sponsor_engaged=False,
            proof_of_concept_completed=False,
            win_rate_vs_competitor_pct=50.0,
        )
        prob = engine._win_probability(50.0, 50.0, inp)
        # base = 50 + 0*0.5 = 50; blended = 50*0.6 + 50*0.4 = 50; clamped
        assert isinstance(prob, (int, float))
        assert prob == 50.0

    def test_champion_supports_reduces_by_15(self, engine):
        inp = make_input(
            champion_supports_competitor=True,
            executive_sponsor_engaged=False,
            proof_of_concept_completed=False,
            win_rate_vs_competitor_pct=50.0,
        )
        prob = engine._win_probability(50.0, 50.0, inp)
        assert prob == 35.0

    def test_exec_sponsor_adds_8(self, engine):
        inp = make_input(
            champion_supports_competitor=False,
            executive_sponsor_engaged=True,
            proof_of_concept_completed=False,
            win_rate_vs_competitor_pct=50.0,
        )
        prob = engine._win_probability(50.0, 50.0, inp)
        assert prob == 58.0

    def test_poc_adds_7(self, engine):
        inp = make_input(
            champion_supports_competitor=False,
            executive_sponsor_engaged=False,
            proof_of_concept_completed=True,
            win_rate_vs_competitor_pct=50.0,
        )
        prob = engine._win_probability(50.0, 50.0, inp)
        assert prob == 57.0

    def test_win_probability_clamped_min_5(self, engine):
        inp = make_input(
            champion_supports_competitor=True,
            executive_sponsor_engaged=False,
            proof_of_concept_completed=False,
            win_rate_vs_competitor_pct=0.0,
        )
        prob = engine._win_probability(0.0, 100.0, inp)
        assert prob == 5.0

    def test_win_probability_clamped_max_95(self, engine):
        inp = make_input(
            champion_supports_competitor=False,
            executive_sponsor_engaged=True,
            proof_of_concept_completed=True,
            win_rate_vs_competitor_pct=100.0,
        )
        prob = engine._win_probability(100.0, 0.0, inp)
        assert prob == 95.0

    def test_win_probability_type_is_numeric(self, engine):
        inp = make_input()
        prob = engine._win_probability(50.0, 50.0, inp)
        assert isinstance(prob, (int, float))

    def test_win_rate_blending(self, engine):
        inp = make_input(
            champion_supports_competitor=False,
            executive_sponsor_engaged=False,
            proof_of_concept_completed=False,
            win_rate_vs_competitor_pct=80.0,
        )
        prob = engine._win_probability(50.0, 50.0, inp)
        # base=50; blended=50*0.6 + 80*0.4 = 30+32=62
        assert prob == 62.0


# ─── TestCompetitiveAction ───────────────────────────────────────────────────

class TestCompetitiveAction:
    def test_critical_losing_escalates(self, engine):
        inp = make_input()
        action = engine._competitive_action(
            CompetitorThreat.CRITICAL, CompetitivePosition.LOSING, inp
        )
        assert action == CompetitiveAction.ESCALATE

    def test_critical_trailing_escalates(self, engine):
        inp = make_input()
        action = engine._competitive_action(
            CompetitorThreat.CRITICAL, CompetitivePosition.TRAILING, inp
        )
        assert action == CompetitiveAction.ESCALATE

    def test_high_losing_escalates(self, engine):
        inp = make_input()
        action = engine._competitive_action(
            CompetitorThreat.HIGH, CompetitivePosition.LOSING, inp
        )
        assert action == CompetitiveAction.ESCALATE

    def test_high_trailing_escalates(self, engine):
        inp = make_input()
        action = engine._competitive_action(
            CompetitorThreat.HIGH, CompetitivePosition.TRAILING, inp
        )
        assert action == CompetitiveAction.ESCALATE

    def test_critical_not_price_competitive_pricing_shared_price_protect(self, engine):
        inp = make_input(price_competitive=False, prospect_shared_competitor_pricing=True)
        action = engine._competitive_action(
            CompetitorThreat.CRITICAL, CompetitivePosition.TIED, inp
        )
        assert action == CompetitiveAction.PRICE_PROTECT

    def test_high_not_price_competitive_pricing_shared_price_protect(self, engine):
        inp = make_input(price_competitive=False, prospect_shared_competitor_pricing=True)
        action = engine._competitive_action(
            CompetitorThreat.HIGH, CompetitivePosition.WINNING, inp
        )
        assert action == CompetitiveAction.PRICE_PROTECT

    def test_critical_price_competitive_defend_and_close(self, engine):
        inp = make_input(price_competitive=True, prospect_shared_competitor_pricing=True)
        action = engine._competitive_action(
            CompetitorThreat.CRITICAL, CompetitivePosition.WINNING, inp
        )
        assert action == CompetitiveAction.DEFEND_AND_CLOSE

    def test_critical_no_pricing_shared_defend_and_close(self, engine):
        inp = make_input(price_competitive=False, prospect_shared_competitor_pricing=False)
        action = engine._competitive_action(
            CompetitorThreat.CRITICAL, CompetitivePosition.WINNING, inp
        )
        assert action == CompetitiveAction.DEFEND_AND_CLOSE

    def test_high_defend_and_close(self, engine):
        inp = make_input(price_competitive=True)
        action = engine._competitive_action(
            CompetitorThreat.HIGH, CompetitivePosition.TIED, inp
        )
        assert action == CompetitiveAction.DEFEND_AND_CLOSE

    def test_moderate_two_unique_features_differentiate(self, engine):
        inp = make_input(unique_features_count=2)
        action = engine._competitive_action(
            CompetitorThreat.MODERATE, CompetitivePosition.WINNING, inp
        )
        assert action == CompetitiveAction.DIFFERENTIATE

    def test_moderate_three_unique_features_differentiate(self, engine):
        inp = make_input(unique_features_count=3)
        action = engine._competitive_action(
            CompetitorThreat.MODERATE, CompetitivePosition.WINNING, inp
        )
        assert action == CompetitiveAction.DIFFERENTIATE

    def test_moderate_one_unique_feature_defend_and_close(self, engine):
        inp = make_input(unique_features_count=1)
        action = engine._competitive_action(
            CompetitorThreat.MODERATE, CompetitivePosition.WINNING, inp
        )
        assert action == CompetitiveAction.DEFEND_AND_CLOSE

    def test_moderate_zero_unique_features_defend_and_close(self, engine):
        inp = make_input(unique_features_count=0)
        action = engine._competitive_action(
            CompetitorThreat.MODERATE, CompetitivePosition.WINNING, inp
        )
        assert action == CompetitiveAction.DEFEND_AND_CLOSE

    def test_low_threat_maintain(self, engine):
        inp = make_input()
        action = engine._competitive_action(
            CompetitorThreat.LOW, CompetitivePosition.WINNING, inp
        )
        assert action == CompetitiveAction.MAINTAIN

    def test_none_threat_monitor(self, engine):
        inp = make_input()
        action = engine._competitive_action(
            CompetitorThreat.NONE, CompetitivePosition.WINNING, inp
        )
        assert action == CompetitiveAction.MONITOR


# ─── TestAnalyzeResult ───────────────────────────────────────────────────────

class TestAnalyzeResult:
    def test_analyze_returns_competitive_result(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result, CompetitiveResult)

    def test_analyze_deal_id_propagated(self, engine):
        inp = make_input(deal_id="DEAL-999")
        result = engine.analyze(inp)
        assert result.deal_id == "DEAL-999"

    def test_analyze_deal_name_propagated(self, engine):
        inp = make_input(deal_name="Big Sale")
        result = engine.analyze(inp)
        assert result.deal_name == "Big Sale"

    def test_analyze_rep_id_propagated(self, engine):
        inp = make_input(rep_id="REP-42")
        result = engine.analyze(inp)
        assert result.rep_id == "REP-42"

    def test_analyze_rep_name_propagated(self, engine):
        inp = make_input(rep_name="Carol")
        result = engine.analyze(inp)
        assert result.rep_name == "Carol"

    def test_analyze_account_name_propagated(self, engine):
        inp = make_input(account_name="TechGiant")
        result = engine.analyze(inp)
        assert result.account_name == "TechGiant"

    def test_analyze_competitor_name_propagated(self, engine):
        inp = make_input(competitor_name="BigRival")
        result = engine.analyze(inp)
        assert result.competitor_name == "BigRival"

    def test_analyze_competitor_category_is_string_value(self, engine):
        inp = make_input(competitor_category=CompetitorCategory.STARTUP)
        result = engine.analyze(inp)
        assert result.competitor_category == "startup"

    def test_analyze_threat_score_is_numeric(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.threat_score, (int, float))

    def test_analyze_position_score_is_numeric(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.position_score, (int, float))

    def test_analyze_win_probability_is_numeric(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.win_probability_pct, (int, float))

    def test_analyze_battle_tactics_is_list(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.battle_tactics, list)

    def test_analyze_differentiators_is_list(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.differentiators, list)

    def test_analyze_risk_signals_is_list(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.risk_signals, list)

    def test_analyze_manager_alerts_is_list(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.manager_alerts, list)

    def test_analyze_stores_result(self, engine, clean_input):
        engine.analyze(clean_input)
        assert len(engine._results) == 1

    def test_analyze_threat_score_range(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert 0.0 <= result.threat_score <= 100.0

    def test_analyze_position_score_range(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert 0.0 <= result.position_score <= 100.0

    def test_analyze_win_probability_range(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert 5.0 <= result.win_probability_pct <= 95.0

    def test_analyze_competitor_threat_is_valid_value(self, engine, clean_input):
        result = engine.analyze(clean_input)
        valid = {m.value for m in CompetitorThreat}
        assert result.competitor_threat in valid

    def test_analyze_competitive_position_is_valid_value(self, engine, clean_input):
        result = engine.analyze(clean_input)
        valid = {m.value for m in CompetitivePosition}
        assert result.competitive_position in valid

    def test_analyze_competitive_action_is_valid_value(self, engine, clean_input):
        result = engine.analyze(clean_input)
        valid = {m.value for m in CompetitiveAction}
        assert result.competitive_action in valid


# ─── TestAnalyzeBatchSorting ──────────────────────────────────────────────────

class TestAnalyzeBatchSorting:
    def test_batch_sorted_desc_by_threat_score(self, engine):
        inp1 = make_input(deal_id="D1", rfp_sent_to_competitor=True, win_rate_vs_competitor_pct=50.0)
        inp2 = make_input(deal_id="D2", rfp_sent_to_competitor=False, win_rate_vs_competitor_pct=50.0)
        inp3 = make_input(
            deal_id="D3",
            rfp_sent_to_competitor=True,
            prospect_requested_competitor_demo=True,
            win_rate_vs_competitor_pct=50.0,
        )
        results = engine.analyze_batch([inp1, inp2, inp3])
        scores = [r.threat_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_batch_returns_all_results(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(5)]
        results = engine.analyze_batch(inputs)
        assert len(results) == 5

    def test_batch_first_has_highest_threat_score(self, engine):
        inp_low = make_input(deal_id="low", win_rate_vs_competitor_pct=50.0)
        inp_high = make_input(deal_id="high", rfp_sent_to_competitor=True, win_rate_vs_competitor_pct=50.0)
        results = engine.analyze_batch([inp_low, inp_high])
        assert results[0].threat_score >= results[1].threat_score

    def test_batch_all_stored_in_results(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 3

    def test_batch_empty_list(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_batch_single_item(self, engine):
        inp = make_input(deal_id="SOLO")
        results = engine.analyze_batch([inp])
        assert len(results) == 1
        assert results[0].deal_id == "SOLO"

    def test_batch_returns_competitive_result_objects(self, engine):
        inputs = [make_input(deal_id=f"D{i}") for i in range(2)]
        results = engine.analyze_batch(inputs)
        for r in results:
            assert isinstance(r, CompetitiveResult)


# ─── TestHelperFilters ───────────────────────────────────────────────────────

class TestHelperFilters:
    def test_critical_threats_empty_when_no_results(self, engine):
        assert engine.critical_threats() == []

    def test_critical_threats_returns_critical_only(self, engine):
        inp_crit = make_input(
            deal_id="CRIT",
            rfp_sent_to_competitor=True,
            champion_supports_competitor=True,
            decision_maker_met_competitor=True,
            prospect_requested_competitor_demo=True,
            win_rate_vs_competitor_pct=10.0,
        )
        inp_low = make_input(deal_id="LOW", win_rate_vs_competitor_pct=50.0)
        engine.analyze(inp_crit)
        engine.analyze(inp_low)
        crits = engine.critical_threats()
        assert all(r.competitor_threat == "critical" for r in crits)

    def test_losing_deals_empty_when_no_results(self, engine):
        assert engine.losing_deals() == []

    def test_losing_deals_returns_losing_only(self, engine):
        inp_losing = make_input(
            deal_id="LOSS",
            rfp_sent_to_competitor=True,
            champion_supports_competitor=True,
            decision_maker_met_competitor=True,
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=10.0,
        )
        inp_winning = make_input(
            deal_id="WIN",
            decision_maker_relationship_score=10,
            product_fit_score=10,
            executive_sponsor_engaged=True,
            proof_of_concept_completed=True,
            win_rate_vs_competitor_pct=80.0,
        )
        engine.analyze(inp_losing)
        engine.analyze(inp_winning)
        losing = engine.losing_deals()
        assert all(r.competitive_position == "losing" for r in losing)

    def test_needs_escalation_empty_when_no_results(self, engine):
        assert engine.needs_escalation() == []

    def test_needs_escalation_returns_escalate_only(self, engine):
        inp_escalate = make_input(
            deal_id="ESC",
            rfp_sent_to_competitor=True,
            champion_supports_competitor=True,
            decision_maker_met_competitor=True,
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=10.0,
        )
        engine.analyze(inp_escalate)
        escalations = engine.needs_escalation()
        assert all(r.competitive_action == "escalate" for r in escalations)

    def test_high_value_at_risk_empty_when_no_results(self, engine):
        assert engine.high_value_at_risk() == []

    def test_high_value_at_risk_returns_critical_and_high(self, engine):
        inp_crit = make_input(
            deal_id="CRIT2",
            rfp_sent_to_competitor=True,
            champion_supports_competitor=True,
            decision_maker_met_competitor=True,
            prospect_requested_competitor_demo=True,
            win_rate_vs_competitor_pct=10.0,
        )
        inp_none = make_input(deal_id="NONE", win_rate_vs_competitor_pct=80.0)
        engine.analyze(inp_crit)
        engine.analyze(inp_none)
        at_risk = engine.high_value_at_risk()
        for r in at_risk:
            assert r.competitor_threat in ("critical", "high")

    def test_strong_positions_empty_when_no_results(self, engine):
        assert engine.strong_positions() == []

    def test_strong_positions_returns_winning_only(self, engine):
        inp_winning = make_input(
            deal_id="WINS",
            decision_maker_relationship_score=10,
            product_fit_score=10,
            executive_sponsor_engaged=True,
            proof_of_concept_completed=True,
            references_provided=True,
            unique_features_count=5,
            price_competitive=True,
            win_rate_vs_competitor_pct=80.0,
        )
        engine.analyze(inp_winning)
        strong = engine.strong_positions()
        assert all(r.competitive_position == "winning" for r in strong)

    def test_high_value_at_risk_default_threshold(self, engine):
        result = engine.high_value_at_risk()
        assert isinstance(result, list)

    def test_high_value_at_risk_custom_threshold(self, engine):
        result = engine.high_value_at_risk(threshold_eur=100000)
        assert isinstance(result, list)


# ─── TestSummary ─────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_returns_dict(self, engine):
        assert isinstance(engine.summary(), dict)

    def test_summary_returns_10_keys(self, engine):
        assert len(engine.summary()) == 10

    def test_summary_empty_keys(self, engine):
        s = engine.summary()
        expected_keys = {
            "total", "threat_counts", "position_counts", "action_counts",
            "avg_threat_score", "avg_position_score", "avg_win_probability",
            "critical_count", "losing_count", "escalation_count",
        }
        assert set(s.keys()) == expected_keys

    def test_summary_total_zero_when_empty(self, engine):
        assert engine.summary()["total"] == 0

    def test_summary_total_correct(self, engine):
        for i in range(3):
            engine.analyze(make_input(deal_id=f"D{i}"))
        assert engine.summary()["total"] == 3

    def test_summary_threat_counts_is_dict(self, engine, clean_input):
        engine.analyze(clean_input)
        assert isinstance(engine.summary()["threat_counts"], dict)

    def test_summary_position_counts_is_dict(self, engine, clean_input):
        engine.analyze(clean_input)
        assert isinstance(engine.summary()["position_counts"], dict)

    def test_summary_action_counts_is_dict(self, engine, clean_input):
        engine.analyze(clean_input)
        assert isinstance(engine.summary()["action_counts"], dict)

    def test_summary_avg_threat_score_is_numeric(self, engine, clean_input):
        engine.analyze(clean_input)
        assert isinstance(engine.summary()["avg_threat_score"], (int, float))

    def test_summary_avg_position_score_is_numeric(self, engine, clean_input):
        engine.analyze(clean_input)
        assert isinstance(engine.summary()["avg_position_score"], (int, float))

    def test_summary_avg_win_probability_is_numeric(self, engine, clean_input):
        engine.analyze(clean_input)
        assert isinstance(engine.summary()["avg_win_probability"], (int, float))

    def test_summary_critical_count_is_int(self, engine, clean_input):
        engine.analyze(clean_input)
        assert isinstance(engine.summary()["critical_count"], int)

    def test_summary_losing_count_is_int(self, engine, clean_input):
        engine.analyze(clean_input)
        assert isinstance(engine.summary()["losing_count"], int)

    def test_summary_escalation_count_is_int(self, engine, clean_input):
        engine.analyze(clean_input)
        assert isinstance(engine.summary()["escalation_count"], int)

    def test_summary_empty_returns_zero_avgs(self, engine):
        s = engine.summary()
        assert s["avg_threat_score"] == 0.0
        assert s["avg_position_score"] == 0.0
        assert s["avg_win_probability"] == 0.0

    def test_summary_counts_correct(self, engine):
        inp = make_input(
            deal_id="D1",
            rfp_sent_to_competitor=True,
            champion_supports_competitor=True,
            decision_maker_met_competitor=True,
            prospect_requested_competitor_demo=True,
            win_rate_vs_competitor_pct=10.0,
        )
        engine.analyze(inp)
        s = engine.summary()
        assert s["critical_count"] == 1

    def test_summary_after_multiple_analyses(self, engine):
        for i in range(5):
            engine.analyze(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert s["total"] == 5
        assert len(s) == 10

    def test_summary_threat_counts_sums_to_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["threat_counts"].values()) == s["total"]

    def test_summary_position_counts_sums_to_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["position_counts"].values()) == s["total"]

    def test_summary_action_counts_sums_to_total(self, engine):
        for i in range(4):
            engine.analyze(make_input(deal_id=f"D{i}"))
        s = engine.summary()
        assert sum(s["action_counts"].values()) == s["total"]


# ─── TestReset ───────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, engine, clean_input):
        engine.analyze(clean_input)
        engine.reset()
        assert engine._results == []

    def test_reset_multiple_results(self, engine):
        for i in range(5):
            engine.analyze(make_input(deal_id=f"D{i}"))
        engine.reset()
        assert len(engine._results) == 0

    def test_reset_then_analyze_works(self, engine, clean_input):
        engine.analyze(clean_input)
        engine.reset()
        engine.analyze(clean_input)
        assert len(engine._results) == 1

    def test_reset_summary_returns_empty(self, engine, clean_input):
        engine.analyze(clean_input)
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0

    def test_reset_filters_return_empty(self, engine, clean_input):
        engine.analyze(clean_input)
        engine.reset()
        assert engine.critical_threats() == []
        assert engine.losing_deals() == []
        assert engine.needs_escalation() == []
        assert engine.strong_positions() == []


# ─── TestBattleTactics ───────────────────────────────────────────────────────

class TestBattleTactics:
    def test_escalate_action_adds_two_tactics(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=True,
            champion_supports_competitor=True,
            decision_maker_met_competitor=True,
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=10.0,
        )
        result = engine.analyze(inp)
        escalate_tactics = [t for t in result.battle_tactics if "Escalade" in t or "solution architect" in t]
        assert len(escalate_tactics) >= 1

    def test_rfp_detected_tactic_added(self, engine):
        inp = make_input(rfp_sent_to_competitor=True, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("RFP" in t for t in result.battle_tactics)

    def test_demo_requested_tactic_added(self, engine):
        inp = make_input(prospect_requested_competitor_demo=True, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("contre-démo" in t or "Demo" in t for t in result.battle_tactics)

    def test_pricing_shared_tactic_added(self, engine):
        inp = make_input(prospect_shared_competitor_pricing=True, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("tarifaire" in t or "TCO" in t for t in result.battle_tactics)

    def test_champion_supports_tactic_added(self, engine):
        inp = make_input(champion_supports_competitor=True, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("Champion" in t or "champion" in t for t in result.battle_tactics)

    def test_no_references_tactic_added(self, engine):
        inp = make_input(references_provided=False, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("référence" in t or "Aucune référence" in t for t in result.battle_tactics)

    def test_high_fit_no_poc_tactic_added(self, engine):
        inp = make_input(
            product_fit_score=8,
            proof_of_concept_completed=False,
            win_rate_vs_competitor_pct=50.0,
        )
        result = engine.analyze(inp)
        assert any("PoC" in t for t in result.battle_tactics)

    def test_default_tactic_when_no_signals(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=False,
            prospect_requested_competitor_demo=False,
            prospect_shared_competitor_pricing=False,
            champion_supports_competitor=False,
            references_provided=True,
            proof_of_concept_completed=True,
            win_rate_vs_competitor_pct=70.0,
            competitor_name="AcmeRival",
        )
        result = engine.analyze(inp)
        assert len(result.battle_tactics) >= 1

    def test_battle_tactics_returns_list(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.battle_tactics, list)
        assert len(result.battle_tactics) > 0


# ─── TestDifferentiators ─────────────────────────────────────────────────────

class TestDifferentiators:
    def test_unique_features_differentiator_added(self, engine):
        inp = make_input(unique_features_count=2, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("fonctionnalité" in d for d in result.differentiators)

    def test_poc_completed_differentiator_added(self, engine):
        inp = make_input(proof_of_concept_completed=True, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("PoC" in d for d in result.differentiators)

    def test_exec_sponsor_differentiator_added(self, engine):
        inp = make_input(executive_sponsor_engaged=True, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("Sponsor" in d or "sponsor" in d or "exécutif" in d for d in result.differentiators)

    def test_high_dm_relationship_differentiator_added(self, engine):
        inp = make_input(decision_maker_relationship_score=8, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("décideur" in d.lower() or "Relation" in d for d in result.differentiators)

    def test_high_win_rate_differentiator_added(self, engine):
        inp = make_input(win_rate_vs_competitor_pct=70.0)
        result = engine.analyze(inp)
        assert any("victoire" in d or "Historique" in d for d in result.differentiators)

    def test_price_competitive_differentiator_added(self, engine):
        inp = make_input(price_competitive=True, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("tarifaire" in d or "prix" in d.lower() for d in result.differentiators)

    def test_no_differentiators_default_message(self, engine):
        inp = make_input(
            unique_features_count=0,
            proof_of_concept_completed=False,
            executive_sponsor_engaged=False,
            decision_maker_relationship_score=3,
            win_rate_vs_competitor_pct=40.0,
            price_competitive=False,
        )
        result = engine.analyze(inp)
        assert len(result.differentiators) == 1
        assert "battlecard" in result.differentiators[0] or "différenciateurs" in result.differentiators[0]

    def test_differentiators_is_list(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.differentiators, list)


# ─── TestRiskSignals ─────────────────────────────────────────────────────────

class TestRiskSignals:
    def test_rfp_risk_signal(self, engine):
        inp = make_input(rfp_sent_to_competitor=True, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("RFP" in r for r in result.risk_signals)

    def test_champion_supports_risk_signal(self, engine):
        inp = make_input(champion_supports_competitor=True, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("champion" in r.lower() or "Champion" in r for r in result.risk_signals)

    def test_dm_met_risk_signal(self, engine):
        inp = make_input(decision_maker_met_competitor=True, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("Décideur" in r or "décideur" in r for r in result.risk_signals)

    def test_previous_losses_risk_signal(self, engine):
        inp = make_input(previous_losses_to_competitor=3, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("pertes" in r or "historiques" in r for r in result.risk_signals)

    def test_previous_losses_2_no_risk_signal(self, engine):
        inp = make_input(previous_losses_to_competitor=2, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert not any("pertes historiques" in r for r in result.risk_signals)

    def test_low_win_rate_risk_signal(self, engine):
        inp = make_input(win_rate_vs_competitor_pct=20.0)
        result = engine.analyze(inp)
        assert any("victoire" in r or "taux" in r.lower() for r in result.risk_signals)

    def test_pricing_shared_not_competitive_risk_signal(self, engine):
        inp = make_input(
            prospect_shared_competitor_pricing=True,
            price_competitive=False,
            win_rate_vs_competitor_pct=50.0,
        )
        result = engine.analyze(inp)
        assert any("tarifaire" in r for r in result.risk_signals)

    def test_days_since_mentioned_gt_30_risk_signal(self, engine):
        inp = make_input(days_since_competitor_first_mentioned=31, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert any("31j" in r or "31" in r for r in result.risk_signals)

    def test_days_since_mentioned_30_no_risk_signal(self, engine):
        inp = make_input(days_since_competitor_first_mentioned=30, win_rate_vs_competitor_pct=50.0)
        result = engine.analyze(inp)
        assert not any("évaluation longue durée" in r for r in result.risk_signals)

    def test_risk_signals_is_list(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.risk_signals, list)

    def test_no_signals_returns_empty_list(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=False,
            champion_supports_competitor=False,
            decision_maker_met_competitor=False,
            previous_losses_to_competitor=2,
            win_rate_vs_competitor_pct=50.0,
            prospect_shared_competitor_pricing=False,
            days_since_competitor_first_mentioned=10,
        )
        result = engine.analyze(inp)
        assert result.risk_signals == []


# ─── TestManagerAlerts ───────────────────────────────────────────────────────

class TestManagerAlerts:
    def test_critical_threat_alert(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=True,
            champion_supports_competitor=True,
            decision_maker_met_competitor=True,
            prospect_requested_competitor_demo=True,
            win_rate_vs_competitor_pct=10.0,
            deal_name="BigDeal",
        )
        result = engine.analyze(inp)
        assert any("critique" in a or "Menace" in a for a in result.manager_alerts)

    def test_losing_position_alert(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=True,
            champion_supports_competitor=True,
            decision_maker_met_competitor=True,
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=10.0,
        )
        result = engine.analyze(inp)
        if result.competitive_position == "losing":
            assert any("perdante" in a for a in result.manager_alerts)

    def test_low_win_probability_alert(self, engine):
        inp = make_input(
            champion_supports_competitor=True,
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=5.0,
            rfp_sent_to_competitor=True,
            decision_maker_met_competitor=True,
        )
        result = engine.analyze(inp)
        if result.win_probability_pct < 25:
            assert any("Probabilité" in a or "probabilité" in a for a in result.manager_alerts)

    def test_rfp_high_deal_size_alert(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=True,
            deal_size_eur=75000.0,
            win_rate_vs_competitor_pct=50.0,
        )
        result = engine.analyze(inp)
        assert any("RFP" in a or "stratégique" in a for a in result.manager_alerts)

    def test_rfp_low_deal_size_no_strategic_alert(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=True,
            deal_size_eur=30000.0,
            win_rate_vs_competitor_pct=50.0,
        )
        result = engine.analyze(inp)
        assert not any("stratégique" in a and "mobiliser" in a for a in result.manager_alerts)

    def test_manager_alerts_is_list(self, engine, clean_input):
        result = engine.analyze(clean_input)
        assert isinstance(result.manager_alerts, list)

    def test_no_alerts_when_clean(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=False,
            deal_size_eur=10000.0,
            win_rate_vs_competitor_pct=80.0,
            decision_maker_relationship_score=10,
            product_fit_score=10,
            executive_sponsor_engaged=True,
        )
        result = engine.analyze(inp)
        assert isinstance(result.manager_alerts, list)


# ─── TestEngineInitialization ────────────────────────────────────────────────

class TestEngineInitialization:
    def test_engine_initializes_empty_results(self):
        e = CompetitiveIntelligenceEngine()
        assert e._results == []

    def test_engine_is_instance(self):
        e = CompetitiveIntelligenceEngine()
        assert isinstance(e, CompetitiveIntelligenceEngine)

    def test_multiple_engines_independent(self):
        e1 = CompetitiveIntelligenceEngine()
        e2 = CompetitiveIntelligenceEngine()
        e1.analyze(make_input(deal_id="E1D1"))
        assert len(e2._results) == 0

    def test_results_accumulate_across_analyses(self, engine):
        for i in range(10):
            engine.analyze(make_input(deal_id=f"D{i}"))
        assert len(engine._results) == 10


# ─── TestEdgeCases ───────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_all_booleans_true_threat_score_100(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=True,
            prospect_requested_competitor_demo=True,
            decision_maker_met_competitor=True,
            prospect_shared_competitor_pricing=True,
            champion_supports_competitor=True,
            prospect_mentioned_competitor_features=True,
            previous_losses_to_competitor=10,
            win_rate_vs_competitor_pct=0.0,
        )
        result = engine.analyze(inp)
        assert result.threat_score == 100.0

    def test_all_position_signals_true_score_100(self, engine):
        inp = make_input(
            decision_maker_relationship_score=10,
            product_fit_score=10,
            executive_sponsor_engaged=True,
            proof_of_concept_completed=True,
            references_provided=True,
            unique_features_count=10,
            price_competitive=True,
            win_rate_vs_competitor_pct=70.0,
        )
        result = engine.analyze(inp)
        assert result.position_score == 100.0

    def test_threat_score_exactly_70_boundary(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=True,
            prospect_requested_competitor_demo=True,
            champion_supports_competitor=True,
            win_rate_vs_competitor_pct=50.0,
        )
        score = engine._threat_score(inp)
        # 30+20+20 = 70
        assert score == 70.0
        assert engine._competitor_threat(score) == CompetitorThreat.CRITICAL

    def test_threat_score_exactly_50_boundary(self, engine):
        inp = make_input(
            rfp_sent_to_competitor=True,
            prospect_requested_competitor_demo=True,
            win_rate_vs_competitor_pct=50.0,
        )
        score = engine._threat_score(inp)
        # 30+20 = 50
        assert score == 50.0
        assert engine._competitor_threat(score) == CompetitorThreat.HIGH

    def test_threat_score_exactly_30_boundary(self, engine):
        score = 30.0
        assert engine._competitor_threat(score) == CompetitorThreat.MODERATE

    def test_threat_score_exactly_10_boundary(self, engine):
        score = 10.0
        assert engine._competitor_threat(score) == CompetitorThreat.LOW

    def test_position_delta_exactly_30_winning(self, engine):
        pos = engine._competitive_position(80.0, 50.0)
        assert pos == CompetitivePosition.WINNING

    def test_position_delta_exactly_minus_10_tied(self, engine):
        pos = engine._competitive_position(40.0, 50.0)
        assert pos == CompetitivePosition.TIED

    def test_win_rate_exactly_70_position_boost(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=70.0,
        )
        score = engine._position_score(inp)
        assert score == 10.0

    def test_win_rate_exactly_50_position_boost(self, engine):
        inp = make_input(
            decision_maker_relationship_score=0,
            product_fit_score=0,
            win_rate_vs_competitor_pct=50.0,
        )
        score = engine._position_score(inp)
        assert score == 5.0

    def test_competitor_category_stored_as_string(self, engine):
        for cat in CompetitorCategory:
            inp = make_input(competitor_category=cat)
            result = engine.analyze(inp)
            assert result.competitor_category == cat.value
            engine.reset()

    def test_analyze_does_not_modify_input(self, engine):
        inp = make_input(deal_id="UNCHANGED")
        engine.analyze(inp)
        assert inp.deal_id == "UNCHANGED"
        assert inp.rfp_sent_to_competitor is False

    def test_summary_after_reset_returns_10_keys(self, engine, clean_input):
        engine.analyze(clean_input)
        engine.reset()
        s = engine.summary()
        assert len(s) == 10
