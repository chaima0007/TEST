"""Comprehensive pytest tests for Module 34 — Competitive Win-Loss Analyzer."""
from __future__ import annotations

import pytest

from swarm.intelligence.competitive_win_loss_analyzer import (
    CompetitiveAction,
    CompetitivePosition,
    CompetitiveWinLossAnalyzer,
    CompetitorAnalysis,
    DealOutcome,
    DealRecord,
    LossReason,
    _battlecard_priorities,
    _competitive_action,
    _competitive_position,
    _loss_patterns,
    _top_loss_reasons,
    _win_patterns,
    _win_rate_pct,
)

# ---------------------------------------------------------------------------
# Helpers / Factories
# ---------------------------------------------------------------------------


def make_deal(
    deal_id: str = "D001",
    competitor: str = "Acme",
    outcome: DealOutcome = DealOutcome.WON,
    loss_reason: LossReason | None = None,
    deal_size_eur: float = 10_000.0,
    segment: str = "enterprise",
    region: str = "EMEA",
    sales_cycle_days: int = 60,
    rep_id: str = "REP01",
    price_objection: bool = False,
    product_gap_mentioned: bool = False,
    exec_sponsor_engaged: bool = True,
    proof_of_concept_done: bool = False,
    references_provided: bool = False,
) -> DealRecord:
    return DealRecord(
        deal_id=deal_id,
        competitor=competitor,
        outcome=outcome,
        loss_reason=loss_reason,
        deal_size_eur=deal_size_eur,
        segment=segment,
        region=region,
        sales_cycle_days=sales_cycle_days,
        rep_id=rep_id,
        price_objection=price_objection,
        product_gap_mentioned=product_gap_mentioned,
        exec_sponsor_engaged=exec_sponsor_engaged,
        proof_of_concept_done=proof_of_concept_done,
        references_provided=references_provided,
    )


def make_won(deal_id="W1", competitor="Acme", deal_size_eur=10_000.0, **kwargs) -> DealRecord:
    return make_deal(
        deal_id=deal_id,
        competitor=competitor,
        outcome=DealOutcome.WON,
        deal_size_eur=deal_size_eur,
        **kwargs,
    )


def make_lost(
    deal_id="L1",
    competitor="Acme",
    loss_reason=LossReason.PRICE,
    deal_size_eur=10_000.0,
    **kwargs,
) -> DealRecord:
    return make_deal(
        deal_id=deal_id,
        competitor=competitor,
        outcome=DealOutcome.LOST,
        loss_reason=loss_reason,
        deal_size_eur=deal_size_eur,
        **kwargs,
    )


def make_no_decision(deal_id="ND1", competitor="Acme", **kwargs) -> DealRecord:
    return make_deal(
        deal_id=deal_id,
        competitor=competitor,
        outcome=DealOutcome.NO_DECISION,
        **kwargs,
    )


def make_churned(deal_id="C1", competitor="Acme", **kwargs) -> DealRecord:
    return make_deal(
        deal_id=deal_id,
        competitor=competitor,
        outcome=DealOutcome.CHURNED,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Class 1 — DealOutcome enum
# ---------------------------------------------------------------------------


class TestDealOutcomeEnum:
    def test_values(self):
        assert DealOutcome.WON.value == "won"
        assert DealOutcome.LOST.value == "lost"
        assert DealOutcome.NO_DECISION.value == "no_decision"
        assert DealOutcome.CHURNED.value == "churned"

    def test_membership(self):
        assert DealOutcome.WON in DealOutcome
        assert DealOutcome.LOST in DealOutcome
        assert DealOutcome.NO_DECISION in DealOutcome
        assert DealOutcome.CHURNED in DealOutcome

    def test_is_str(self):
        assert isinstance(DealOutcome.WON, str)
        assert DealOutcome.WON == "won"

    def test_count(self):
        assert len(DealOutcome) == 4


# ---------------------------------------------------------------------------
# Class 2 — LossReason enum
# ---------------------------------------------------------------------------


class TestLossReasonEnum:
    def test_values(self):
        assert LossReason.PRICE.value == "price"
        assert LossReason.PRODUCT.value == "product"
        assert LossReason.COMPETITOR.value == "competitor"
        assert LossReason.TIMING.value == "timing"
        assert LossReason.CHAMPION_LEFT.value == "champion_left"
        assert LossReason.INTERNAL_PRIORITY.value == "internal_priority"
        assert LossReason.RELATIONSHIP.value == "relationship"
        assert LossReason.UNKNOWN.value == "unknown"

    def test_count(self):
        assert len(LossReason) == 8

    def test_is_str(self):
        assert isinstance(LossReason.PRICE, str)


# ---------------------------------------------------------------------------
# Class 3 — CompetitivePosition enum
# ---------------------------------------------------------------------------


class TestCompetitivePositionEnum:
    def test_values(self):
        assert CompetitivePosition.DOMINANT.value == "dominant"
        assert CompetitivePosition.STRONG.value == "strong"
        assert CompetitivePosition.COMPETITIVE.value == "competitive"
        assert CompetitivePosition.WEAK.value == "weak"
        assert CompetitivePosition.UNKNOWN.value == "unknown"

    def test_count(self):
        assert len(CompetitivePosition) == 5


# ---------------------------------------------------------------------------
# Class 4 — CompetitiveAction enum
# ---------------------------------------------------------------------------


class TestCompetitiveActionEnum:
    def test_values(self):
        assert CompetitiveAction.REPLICATE.value == "replicate"
        assert CompetitiveAction.DEFEND.value == "defend"
        assert CompetitiveAction.DIFFERENTIATE.value == "differentiate"
        assert CompetitiveAction.BATTLECARD.value == "battlecard"

    def test_count(self):
        assert len(CompetitiveAction) == 4


# ---------------------------------------------------------------------------
# Class 5 — DealRecord dataclass
# ---------------------------------------------------------------------------


class TestDealRecordDataclass:
    def test_creation(self):
        d = make_deal()
        assert d.deal_id == "D001"
        assert d.competitor == "Acme"
        assert d.outcome == DealOutcome.WON
        assert d.loss_reason is None
        assert d.deal_size_eur == 10_000.0

    def test_all_fields(self):
        d = make_deal(
            deal_id="X",
            competitor="Beta",
            outcome=DealOutcome.LOST,
            loss_reason=LossReason.PRODUCT,
            deal_size_eur=5_000.0,
            segment="smb",
            region="APAC",
            sales_cycle_days=90,
            rep_id="REP99",
            price_objection=True,
            product_gap_mentioned=True,
            exec_sponsor_engaged=False,
            proof_of_concept_done=True,
            references_provided=True,
        )
        assert d.price_objection is True
        assert d.product_gap_mentioned is True
        assert d.exec_sponsor_engaged is False
        assert d.proof_of_concept_done is True
        assert d.references_provided is True
        assert d.segment == "smb"
        assert d.region == "APAC"
        assert d.sales_cycle_days == 90

    def test_loss_reason_none_for_won(self):
        d = make_won()
        assert d.loss_reason is None


# ---------------------------------------------------------------------------
# Class 6 — CompetitorAnalysis dataclass & to_dict
# ---------------------------------------------------------------------------


class TestCompetitorAnalysisToDict:
    def _make_analysis(self, **kwargs) -> CompetitorAnalysis:
        defaults = dict(
            competitor="TestCo",
            total_deals=10,
            wins=7,
            losses=3,
            no_decisions=0,
            win_rate_pct=70.0,
            avg_deal_size_eur=8000.0,
            avg_cycle_days=45.0,
            position=CompetitivePosition.DOMINANT,
            action=CompetitiveAction.REPLICATE,
            top_loss_reasons=["reason1"],
            win_patterns=["pattern1"],
            loss_patterns=["lpattern1"],
            battlecard_priorities=["prio1"],
            arr_won_eur=70_000.0,
            arr_lost_eur=30_000.0,
            net_arr_eur=40_000.0,
        )
        defaults.update(kwargs)
        return CompetitorAnalysis(**defaults)

    def test_to_dict_keys(self):
        d = self._make_analysis().to_dict()
        expected_keys = {
            "competitor",
            "total_deals",
            "wins",
            "losses",
            "no_decisions",
            "win_rate_pct",
            "avg_deal_size_eur",
            "avg_cycle_days",
            "position",
            "action",
            "top_loss_reasons",
            "win_patterns",
            "loss_patterns",
            "battlecard_priorities",
            "arr_won_eur",
            "arr_lost_eur",
            "net_arr_eur",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_position_is_str(self):
        d = self._make_analysis().to_dict()
        assert d["position"] == "dominant"
        assert isinstance(d["position"], str)

    def test_to_dict_action_is_str(self):
        d = self._make_analysis().to_dict()
        assert d["action"] == "replicate"
        assert isinstance(d["action"], str)

    def test_to_dict_values(self):
        analysis = self._make_analysis()
        d = analysis.to_dict()
        assert d["competitor"] == "TestCo"
        assert d["total_deals"] == 10
        assert d["wins"] == 7
        assert d["losses"] == 3
        assert d["win_rate_pct"] == 70.0
        assert d["arr_won_eur"] == 70_000.0
        assert d["arr_lost_eur"] == 30_000.0
        assert d["net_arr_eur"] == 40_000.0

    def test_to_dict_lists_preserved(self):
        analysis = self._make_analysis()
        d = analysis.to_dict()
        assert d["top_loss_reasons"] == ["reason1"]
        assert d["win_patterns"] == ["pattern1"]
        assert d["loss_patterns"] == ["lpattern1"]
        assert d["battlecard_priorities"] == ["prio1"]


# ---------------------------------------------------------------------------
# Class 7 — _win_rate_pct
# ---------------------------------------------------------------------------


class TestWinRatePct:
    def test_zero_total(self):
        assert _win_rate_pct(0, 0) == 0.0

    def test_negative_total(self):
        assert _win_rate_pct(0, -1) == 0.0

    def test_perfect_win_rate(self):
        assert _win_rate_pct(10, 10) == 100.0

    def test_zero_wins(self):
        assert _win_rate_pct(0, 5) == 0.0

    def test_half(self):
        assert _win_rate_pct(5, 10) == 50.0

    def test_rounded_to_one_decimal(self):
        result = _win_rate_pct(1, 3)
        assert result == 33.3

    def test_70_percent(self):
        assert _win_rate_pct(7, 10) == 70.0

    def test_single_win(self):
        assert _win_rate_pct(1, 1) == 100.0


# ---------------------------------------------------------------------------
# Class 8 — _competitive_position
# ---------------------------------------------------------------------------


class TestCompetitivePosition:
    def test_unknown_when_zero_deals(self):
        assert _competitive_position(100.0, 0) == CompetitivePosition.UNKNOWN

    def test_unknown_when_one_deal(self):
        assert _competitive_position(100.0, 1) == CompetitivePosition.UNKNOWN

    def test_unknown_when_two_deals(self):
        assert _competitive_position(100.0, 2) == CompetitivePosition.UNKNOWN

    def test_dominant_at_70(self):
        assert _competitive_position(70.0, 10) == CompetitivePosition.DOMINANT

    def test_dominant_above_70(self):
        assert _competitive_position(85.0, 10) == CompetitivePosition.DOMINANT

    def test_dominant_at_100(self):
        assert _competitive_position(100.0, 5) == CompetitivePosition.DOMINANT

    def test_strong_at_50(self):
        assert _competitive_position(50.0, 10) == CompetitivePosition.STRONG

    def test_strong_at_69(self):
        assert _competitive_position(69.9, 10) == CompetitivePosition.STRONG

    def test_competitive_at_30(self):
        assert _competitive_position(30.0, 10) == CompetitivePosition.COMPETITIVE

    def test_competitive_at_49(self):
        assert _competitive_position(49.9, 10) == CompetitivePosition.COMPETITIVE

    def test_weak_below_30(self):
        assert _competitive_position(29.9, 10) == CompetitivePosition.WEAK

    def test_weak_at_zero(self):
        assert _competitive_position(0.0, 10) == CompetitivePosition.WEAK

    def test_boundary_exactly_3_deals(self):
        # 3 deals is enough for a real position
        result = _competitive_position(70.0, 3)
        assert result == CompetitivePosition.DOMINANT


# ---------------------------------------------------------------------------
# Class 9 — _competitive_action
# ---------------------------------------------------------------------------


class TestCompetitiveAction:
    def test_dominant_gives_replicate(self):
        assert _competitive_action(CompetitivePosition.DOMINANT, 80.0) == CompetitiveAction.REPLICATE

    def test_strong_gives_defend(self):
        assert _competitive_action(CompetitivePosition.STRONG, 60.0) == CompetitiveAction.DEFEND

    def test_competitive_gives_differentiate(self):
        assert (
            _competitive_action(CompetitivePosition.COMPETITIVE, 40.0)
            == CompetitiveAction.DIFFERENTIATE
        )

    def test_unknown_gives_differentiate(self):
        assert (
            _competitive_action(CompetitivePosition.UNKNOWN, 0.0)
            == CompetitiveAction.DIFFERENTIATE
        )

    def test_weak_gives_battlecard(self):
        assert _competitive_action(CompetitivePosition.WEAK, 20.0) == CompetitiveAction.BATTLECARD


# ---------------------------------------------------------------------------
# Class 10 — _top_loss_reasons
# ---------------------------------------------------------------------------


class TestTopLossReasons:
    def test_empty_losses(self):
        assert _top_loss_reasons([]) == []

    def test_single_reason(self):
        losses = [make_lost(loss_reason=LossReason.PRICE)]
        result = _top_loss_reasons(losses)
        assert len(result) == 1
        assert "pricing" in result[0].lower() or "prix" in result[0].lower()
        assert "(1 deals)" in result[0]

    def test_top_3_limit(self):
        losses = [
            make_lost(deal_id="L1", loss_reason=LossReason.PRICE),
            make_lost(deal_id="L2", loss_reason=LossReason.PRICE),
            make_lost(deal_id="L3", loss_reason=LossReason.PRODUCT),
            make_lost(deal_id="L4", loss_reason=LossReason.COMPETITOR),
            make_lost(deal_id="L5", loss_reason=LossReason.TIMING),
            make_lost(deal_id="L6", loss_reason=LossReason.RELATIONSHIP),
        ]
        result = _top_loss_reasons(losses)
        assert len(result) == 3

    def test_sorted_by_count_desc(self):
        losses = [
            make_lost(deal_id="L1", loss_reason=LossReason.TIMING),
            make_lost(deal_id="L2", loss_reason=LossReason.PRICE),
            make_lost(deal_id="L3", loss_reason=LossReason.PRICE),
            make_lost(deal_id="L4", loss_reason=LossReason.PRICE),
            make_lost(deal_id="L5", loss_reason=LossReason.PRODUCT),
            make_lost(deal_id="L6", loss_reason=LossReason.PRODUCT),
        ]
        result = _top_loss_reasons(losses)
        # First item must have (3 deals) for PRICE
        assert "(3 deals)" in result[0]

    def test_none_loss_reason_treated_as_unknown(self):
        losses = [make_lost(deal_id="L1", loss_reason=None)]
        result = _top_loss_reasons(losses)
        assert len(result) == 1
        assert "(1 deals)" in result[0]

    def test_count_label_in_output(self):
        losses = [
            make_lost(deal_id="L1", loss_reason=LossReason.PRODUCT),
            make_lost(deal_id="L2", loss_reason=LossReason.PRODUCT),
        ]
        result = _top_loss_reasons(losses)
        assert "(2 deals)" in result[0]

    def test_all_known_reasons_have_labels(self):
        for reason in LossReason:
            losses = [make_lost(deal_id="L1", loss_reason=reason)]
            result = _top_loss_reasons(losses)
            assert len(result) == 1
            assert "(1 deals)" in result[0]


# ---------------------------------------------------------------------------
# Class 11 — _win_patterns
# ---------------------------------------------------------------------------


class TestWinPatterns:
    def test_empty_wins(self):
        assert _win_patterns([]) == []

    def test_avg_size_always_included(self):
        wins = [make_won(deal_size_eur=10_000.0)]
        result = _win_patterns(wins)
        assert any("10" in p and "€" in p for p in result)

    def test_poc_pattern_triggered_at_60_pct(self):
        wins = [
            make_won(deal_id="W1", proof_of_concept_done=True),
            make_won(deal_id="W2", proof_of_concept_done=True),
            make_won(deal_id="W3", proof_of_concept_done=True),
            make_won(deal_id="W4", proof_of_concept_done=False),
            make_won(deal_id="W5", proof_of_concept_done=False),
        ]
        result = _win_patterns(wins)
        poc_patterns = [p for p in result if "POC" in p]
        assert len(poc_patterns) == 1

    def test_poc_pattern_not_triggered_below_60_pct(self):
        wins = [
            make_won(deal_id="W1", proof_of_concept_done=True),
            make_won(deal_id="W2", proof_of_concept_done=False),
            make_won(deal_id="W3", proof_of_concept_done=False),
        ]
        result = _win_patterns(wins)
        poc_patterns = [p for p in result if "POC" in p]
        assert len(poc_patterns) == 0

    def test_reference_pattern_triggered_at_50_pct(self):
        wins = [
            make_won(deal_id="W1", references_provided=True),
            make_won(deal_id="W2", references_provided=True),
            make_won(deal_id="W3", references_provided=False),
            make_won(deal_id="W4", references_provided=False),
        ]
        result = _win_patterns(wins)
        ref_patterns = [p for p in result if "f" in p.lower() and "rence" in p.lower()]
        assert len(ref_patterns) == 1

    def test_reference_pattern_not_triggered_below_50_pct(self):
        wins = [
            make_won(deal_id="W1", references_provided=True),
            make_won(deal_id="W2", references_provided=False),
            make_won(deal_id="W3", references_provided=False),
        ]
        result = _win_patterns(wins)
        ref_patterns = [p for p in result if "f" in p.lower() and "rence" in p.lower()]
        assert len(ref_patterns) == 0

    def test_exec_pattern_triggered_at_70_pct(self):
        wins = [
            make_won(deal_id="W1", exec_sponsor_engaged=True),
            make_won(deal_id="W2", exec_sponsor_engaged=True),
            make_won(deal_id="W3", exec_sponsor_engaged=True),
            make_won(deal_id="W4", exec_sponsor_engaged=False),
        ]
        result = _win_patterns(wins)
        exec_patterns = [p for p in result if "C-level" in p or "sponsor" in p.lower()]
        assert len(exec_patterns) == 1

    def test_exec_pattern_not_triggered_below_70_pct(self):
        wins = [
            make_won(deal_id="W1", exec_sponsor_engaged=True),
            make_won(deal_id="W2", exec_sponsor_engaged=True),
            make_won(deal_id="W3", exec_sponsor_engaged=False),
            make_won(deal_id="W4", exec_sponsor_engaged=False),
        ]
        result = _win_patterns(wins)
        exec_patterns = [p for p in result if "C-level" in p or "sponsor" in p.lower()]
        assert len(exec_patterns) == 0

    def test_all_patterns_triggered(self):
        wins = [
            make_won(
                deal_id=f"W{i}",
                proof_of_concept_done=True,
                references_provided=True,
                exec_sponsor_engaged=True,
                deal_size_eur=10_000.0,
            )
            for i in range(5)
        ]
        result = _win_patterns(wins)
        # poc, ref, exec + avg size => 4 patterns
        assert len(result) == 4


# ---------------------------------------------------------------------------
# Class 12 — _loss_patterns
# ---------------------------------------------------------------------------


class TestLossPatterns:
    def test_empty_losses(self):
        assert _loss_patterns([]) == []

    def test_avg_cycle_always_included(self):
        losses = [make_lost(sales_cycle_days=90)]
        result = _loss_patterns(losses)
        assert any("90" in p for p in result)

    def test_price_pattern_triggered_at_50_pct(self):
        losses = [
            make_lost(deal_id="L1", price_objection=True),
            make_lost(deal_id="L2", price_objection=True),
            make_lost(deal_id="L3", price_objection=False),
            make_lost(deal_id="L4", price_objection=False),
        ]
        result = _loss_patterns(losses)
        price_patterns = [p for p in result if "prix" in p.lower() or "price" in p.lower() or "prix" in p.lower()]
        assert len(price_patterns) == 1

    def test_price_pattern_not_triggered_below_50_pct(self):
        losses = [
            make_lost(deal_id="L1", price_objection=True),
            make_lost(deal_id="L2", price_objection=False),
            make_lost(deal_id="L3", price_objection=False),
        ]
        result = _loss_patterns(losses)
        price_patterns = [p for p in result if "prix" in p.lower()]
        assert len(price_patterns) == 0

    def test_product_pattern_triggered_at_40_pct(self):
        losses = [
            make_lost(deal_id="L1", product_gap_mentioned=True),
            make_lost(deal_id="L2", product_gap_mentioned=True),
            make_lost(deal_id="L3", product_gap_mentioned=False),
            make_lost(deal_id="L4", product_gap_mentioned=False),
            make_lost(deal_id="L5", product_gap_mentioned=False),
        ]
        result = _loss_patterns(losses)
        prod_patterns = [p for p in result if "produit" in p.lower() or "gap" in p.lower()]
        assert len(prod_patterns) == 1

    def test_product_pattern_not_triggered_below_40_pct(self):
        losses = [
            make_lost(deal_id="L1", product_gap_mentioned=True),
            make_lost(deal_id="L2", product_gap_mentioned=False),
            make_lost(deal_id="L3", product_gap_mentioned=False),
            make_lost(deal_id="L4", product_gap_mentioned=False),
        ]
        result = _loss_patterns(losses)
        prod_patterns = [p for p in result if "produit" in p.lower() or "gap" in p.lower()]
        assert len(prod_patterns) == 0

    def test_exec_absent_pattern_triggered_at_60_pct(self):
        losses = [
            make_lost(deal_id="L1", exec_sponsor_engaged=False),
            make_lost(deal_id="L2", exec_sponsor_engaged=False),
            make_lost(deal_id="L3", exec_sponsor_engaged=False),
            make_lost(deal_id="L4", exec_sponsor_engaged=True),
            make_lost(deal_id="L5", exec_sponsor_engaged=True),
        ]
        result = _loss_patterns(losses)
        exec_patterns = [p for p in result if "exécutif" in p.lower() or "sponsor" in p.lower()]
        assert len(exec_patterns) == 1

    def test_exec_absent_pattern_not_triggered_below_60_pct(self):
        losses = [
            make_lost(deal_id="L1", exec_sponsor_engaged=False),
            make_lost(deal_id="L2", exec_sponsor_engaged=True),
            make_lost(deal_id="L3", exec_sponsor_engaged=True),
        ]
        result = _loss_patterns(losses)
        exec_patterns = [p for p in result if "exécutif" in p.lower() or "sponsor" in p.lower()]
        assert len(exec_patterns) == 0

    def test_avg_cycle_is_correct(self):
        losses = [
            make_lost(deal_id="L1", sales_cycle_days=60),
            make_lost(deal_id="L2", sales_cycle_days=120),
        ]
        result = _loss_patterns(losses)
        cycle_patterns = [p for p in result if "90" in p or "cycle" in p.lower()]
        assert len(cycle_patterns) >= 1


# ---------------------------------------------------------------------------
# Class 13 — _battlecard_priorities
# ---------------------------------------------------------------------------


class TestBattlecardPriorities:
    def test_price_losses_trigger_roi_priority(self):
        losses = [make_lost(deal_id="L1", price_objection=True)]
        result = _battlecard_priorities(losses, CompetitivePosition.COMPETITIVE, "Rival")
        assert any("ROI" in p or "Rival" in p for p in result)

    def test_product_losses_trigger_feature_priority(self):
        losses = [make_lost(deal_id="L1", product_gap_mentioned=True)]
        result = _battlecard_priorities(losses, CompetitivePosition.COMPETITIVE, "Rival")
        assert any("fonctionnalit" in p for p in result)

    def test_weak_position_adds_two_extra_priorities(self):
        losses = []
        result = _battlecard_priorities(losses, CompetitivePosition.WEAK, "Enemy")
        # Should have at least 2 weak-specific items
        weak_prios = [p for p in result if "Win story" in p or "terrain de jeu" in p]
        assert len(weak_prios) == 2

    def test_competitive_position_adds_two_extra_priorities(self):
        losses = []
        result = _battlecard_priorities(losses, CompetitivePosition.COMPETITIVE, "Enemy")
        comp_prios = [p for p in result if "discovery" in p or "références" in p.lower()]
        assert len(comp_prios) == 2

    def test_strong_position_adds_one_extra_priority(self):
        losses = []
        result = _battlecard_priorities(losses, CompetitivePosition.STRONG, "Enemy")
        strong_prios = [p for p in result if "Maintenir" in p or "avantage" in p.lower()]
        assert len(strong_prios) == 1

    def test_dominant_position_adds_playbook_priority(self):
        losses = []
        result = _battlecard_priorities(losses, CompetitivePosition.DOMINANT, "Enemy")
        playbook_prios = [p for p in result if "playbook" in p.lower()]
        assert len(playbook_prios) == 1

    def test_unknown_position_falls_through_to_else(self):
        losses = []
        result = _battlecard_priorities(losses, CompetitivePosition.UNKNOWN, "Enemy")
        # UNKNOWN is not WEAK, COMPETITIVE, or STRONG, so falls to else
        playbook_prios = [p for p in result if "playbook" in p.lower()]
        assert len(playbook_prios) == 1

    def test_competitor_name_in_output(self):
        losses = [make_lost(deal_id="L1", price_objection=True)]
        result = _battlecard_priorities(losses, CompetitivePosition.WEAK, "SpecialCorp")
        assert any("SpecialCorp" in p for p in result)

    def test_no_losses_no_price_product_priorities(self):
        result = _battlecard_priorities([], CompetitivePosition.DOMINANT, "Corp")
        # No price/product losses, only the else branch for dominant
        price_prios = [p for p in result if "ROI" in p]
        assert len(price_prios) == 0


# ---------------------------------------------------------------------------
# Class 14 — CompetitiveWinLossAnalyzer.add_deal / add_deals
# ---------------------------------------------------------------------------


class TestAnalyzerAddDeals:
    def test_add_single_deal(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_deal())
        assert analyzer.overall_win_rate() == 100.0

    def test_add_multiple_deals_via_add_deal(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1"))
        analyzer.add_deal(make_lost(deal_id="L1"))
        assert analyzer.overall_win_rate() == 50.0

    def test_add_deals_bulk(self):
        analyzer = CompetitiveWinLossAnalyzer()
        deals = [make_won(deal_id=f"W{i}") for i in range(5)]
        analyzer.add_deals(deals)
        assert analyzer.overall_win_rate() == 100.0

    def test_add_deal_invalidates_cache_for_competitor(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1", competitor="Acme"))
        first = analyzer.analyze("Acme")
        assert first.wins == 1
        analyzer.add_deal(make_won(deal_id="W2", competitor="Acme"))
        second = analyzer.analyze("Acme")
        assert second.wins == 2

    def test_add_deals_clears_all_caches(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1", competitor="Acme"))
        _ = analyzer.analyze("Acme")
        analyzer.add_deals([make_won(deal_id="W2", competitor="Acme")])
        fresh = analyzer.analyze("Acme")
        assert fresh.wins == 2

    def test_add_empty_list(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deals([])
        assert analyzer.overall_win_rate() == 0.0


# ---------------------------------------------------------------------------
# Class 15 — CompetitiveWinLossAnalyzer.analyze
# ---------------------------------------------------------------------------


class TestAnalyzerAnalyze:
    def _setup(self) -> CompetitiveWinLossAnalyzer:
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deals([
            make_won(deal_id="W1", competitor="Acme", deal_size_eur=10_000),
            make_won(deal_id="W2", competitor="Acme", deal_size_eur=20_000),
            make_lost(deal_id="L1", competitor="Acme", loss_reason=LossReason.PRICE,
                      deal_size_eur=5_000),
        ])
        return analyzer

    def test_returns_competitor_analysis(self):
        analyzer = self._setup()
        result = analyzer.analyze("Acme")
        assert isinstance(result, CompetitorAnalysis)
        assert result.competitor == "Acme"

    def test_total_deals_correct(self):
        result = self._setup().analyze("Acme")
        assert result.total_deals == 3

    def test_wins_count_correct(self):
        result = self._setup().analyze("Acme")
        assert result.wins == 2

    def test_losses_count_correct(self):
        result = self._setup().analyze("Acme")
        assert result.losses == 1

    def test_win_rate_correct(self):
        result = self._setup().analyze("Acme")
        assert result.win_rate_pct == pytest.approx(66.7, abs=0.1)

    def test_arr_won_correct(self):
        result = self._setup().analyze("Acme")
        assert result.arr_won_eur == 30_000.0

    def test_arr_lost_correct(self):
        result = self._setup().analyze("Acme")
        assert result.arr_lost_eur == 5_000.0

    def test_net_arr_correct(self):
        result = self._setup().analyze("Acme")
        assert result.net_arr_eur == 25_000.0

    def test_avg_deal_size(self):
        result = self._setup().analyze("Acme")
        expected = (10_000 + 20_000 + 5_000) / 3
        assert result.avg_deal_size_eur == pytest.approx(round(expected, 0), abs=1)

    def test_no_decisions_counted(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deals([
            make_won(deal_id="W1", competitor="Beta"),
            make_won(deal_id="W2", competitor="Beta"),
            make_no_decision(deal_id="ND1", competitor="Beta"),
        ])
        result = analyzer.analyze("Beta")
        assert result.no_decisions == 1

    def test_position_computed(self):
        result = self._setup().analyze("Acme")
        assert result.position in CompetitivePosition

    def test_action_computed(self):
        result = self._setup().analyze("Acme")
        assert result.action in CompetitiveAction


# ---------------------------------------------------------------------------
# Class 16 — CompetitiveWinLossAnalyzer.analyze_all
# ---------------------------------------------------------------------------


class TestAnalyzeAll:
    def _setup_multi_competitor(self) -> CompetitiveWinLossAnalyzer:
        analyzer = CompetitiveWinLossAnalyzer()
        # Acme: 3/4 wins => 75% => DOMINANT
        for i in range(3):
            analyzer.add_deal(make_won(deal_id=f"AW{i}", competitor="Acme"))
        analyzer.add_deal(make_lost(deal_id="AL1", competitor="Acme", loss_reason=LossReason.PRICE))

        # Beta: 1/4 wins => 25% => WEAK
        analyzer.add_deal(make_won(deal_id="BW1", competitor="Beta"))
        for i in range(3):
            analyzer.add_deal(make_lost(deal_id=f"BL{i}", competitor="Beta",
                                        loss_reason=LossReason.PRODUCT))
        return analyzer

    def test_returns_list(self):
        analyzer = self._setup_multi_competitor()
        result = analyzer.analyze_all()
        assert isinstance(result, list)

    def test_returns_all_competitors(self):
        analyzer = self._setup_multi_competitor()
        result = analyzer.analyze_all()
        competitors = {a.competitor for a in result}
        assert competitors == {"Acme", "Beta"}

    def test_sorted_desc_by_win_rate(self):
        analyzer = self._setup_multi_competitor()
        result = analyzer.analyze_all()
        win_rates = [a.win_rate_pct for a in result]
        assert win_rates == sorted(win_rates, reverse=True)

    def test_first_is_highest_win_rate(self):
        analyzer = self._setup_multi_competitor()
        result = analyzer.analyze_all()
        assert result[0].competitor == "Acme"

    def test_empty_analyzer(self):
        analyzer = CompetitiveWinLossAnalyzer()
        result = analyzer.analyze_all()
        assert result == []

    def test_single_competitor(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1", competitor="Solo"))
        result = analyzer.analyze_all()
        assert len(result) == 1
        assert result[0].competitor == "Solo"


# ---------------------------------------------------------------------------
# Class 17 — by_position / weakest_competitors / dominant_over
# ---------------------------------------------------------------------------


class TestPositionFilters:
    def _setup(self) -> CompetitiveWinLossAnalyzer:
        analyzer = CompetitiveWinLossAnalyzer()
        # Dominant: Acme 4/4 = 100%
        for i in range(4):
            analyzer.add_deal(make_won(deal_id=f"AW{i}", competitor="Acme"))
        # Weak: Beta 0/4 = 0%
        for i in range(4):
            analyzer.add_deal(make_lost(deal_id=f"BL{i}", competitor="Beta",
                                        loss_reason=LossReason.TIMING))
        return analyzer

    def test_by_position_dominant(self):
        analyzer = self._setup()
        result = analyzer.by_position(CompetitivePosition.DOMINANT)
        assert all(a.position == CompetitivePosition.DOMINANT for a in result)
        assert any(a.competitor == "Acme" for a in result)

    def test_by_position_weak(self):
        analyzer = self._setup()
        result = analyzer.by_position(CompetitivePosition.WEAK)
        assert all(a.position == CompetitivePosition.WEAK for a in result)
        assert any(a.competitor == "Beta" for a in result)

    def test_weakest_competitors(self):
        analyzer = self._setup()
        result = analyzer.weakest_competitors()
        assert all(a.position == CompetitivePosition.WEAK for a in result)

    def test_dominant_over(self):
        analyzer = self._setup()
        result = analyzer.dominant_over()
        assert all(a.position == CompetitivePosition.DOMINANT for a in result)

    def test_empty_position_returns_empty_list(self):
        analyzer = self._setup()
        result = analyzer.by_position(CompetitivePosition.STRONG)
        assert result == []

    def test_weakest_empty_when_none_weak(self):
        analyzer = CompetitiveWinLossAnalyzer()
        for i in range(4):
            analyzer.add_deal(make_won(deal_id=f"W{i}", competitor="Alpha"))
        result = analyzer.weakest_competitors()
        assert result == []


# ---------------------------------------------------------------------------
# Class 18 — needs_battlecard
# ---------------------------------------------------------------------------


class TestNeedsBattlecard:
    def test_weak_competitor_needs_battlecard(self):
        analyzer = CompetitiveWinLossAnalyzer()
        for i in range(4):
            analyzer.add_deal(make_lost(deal_id=f"L{i}", competitor="WeakCo",
                                        loss_reason=LossReason.PRICE))
        result = analyzer.needs_battlecard()
        assert any(a.competitor == "WeakCo" for a in result)

    def test_dominant_competitor_not_in_battlecard(self):
        analyzer = CompetitiveWinLossAnalyzer()
        for i in range(5):
            analyzer.add_deal(make_won(deal_id=f"W{i}", competitor="DomCo"))
        result = analyzer.needs_battlecard()
        assert not any(a.competitor == "DomCo" for a in result)

    def test_all_need_battlecard_have_correct_action(self):
        analyzer = CompetitiveWinLossAnalyzer()
        for i in range(4):
            analyzer.add_deal(make_lost(deal_id=f"L{i}", competitor="WkCo",
                                        loss_reason=LossReason.TIMING))
        result = analyzer.needs_battlecard()
        for a in result:
            assert a.action == CompetitiveAction.BATTLECARD

    def test_empty_analyzer_returns_empty(self):
        analyzer = CompetitiveWinLossAnalyzer()
        assert analyzer.needs_battlecard() == []


# ---------------------------------------------------------------------------
# Class 19 — overall_win_rate
# ---------------------------------------------------------------------------


class TestOverallWinRate:
    def test_empty_returns_zero(self):
        analyzer = CompetitiveWinLossAnalyzer()
        assert analyzer.overall_win_rate() == 0.0

    def test_all_won(self):
        analyzer = CompetitiveWinLossAnalyzer()
        for i in range(5):
            analyzer.add_deal(make_won(deal_id=f"W{i}"))
        assert analyzer.overall_win_rate() == 100.0

    def test_all_lost(self):
        analyzer = CompetitiveWinLossAnalyzer()
        for i in range(5):
            analyzer.add_deal(make_lost(deal_id=f"L{i}"))
        assert analyzer.overall_win_rate() == 0.0

    def test_half_won(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1"))
        analyzer.add_deal(make_lost(deal_id="L1"))
        assert analyzer.overall_win_rate() == 50.0

    def test_no_decision_counted_in_total(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1"))
        analyzer.add_deal(make_no_decision(deal_id="ND1"))
        # 1 win out of 2 total = 50%
        assert analyzer.overall_win_rate() == 50.0

    def test_across_competitors(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1", competitor="Acme"))
        analyzer.add_deal(make_won(deal_id="W2", competitor="Beta"))
        analyzer.add_deal(make_lost(deal_id="L1", competitor="Acme"))
        # 2/3 won
        assert analyzer.overall_win_rate() == pytest.approx(66.7, abs=0.1)


# ---------------------------------------------------------------------------
# Class 20 — total_arr_won_eur / total_arr_lost_eur
# ---------------------------------------------------------------------------


class TestArrTotals:
    def test_arr_won_empty(self):
        analyzer = CompetitiveWinLossAnalyzer()
        assert analyzer.total_arr_won_eur() == 0.0

    def test_arr_lost_empty(self):
        analyzer = CompetitiveWinLossAnalyzer()
        assert analyzer.total_arr_lost_eur() == 0.0

    def test_arr_won_sums_only_won(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1", deal_size_eur=10_000))
        analyzer.add_deal(make_won(deal_id="W2", deal_size_eur=20_000))
        analyzer.add_deal(make_lost(deal_id="L1", deal_size_eur=50_000))
        assert analyzer.total_arr_won_eur() == 30_000.0

    def test_arr_lost_sums_only_lost(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1", deal_size_eur=10_000))
        analyzer.add_deal(make_lost(deal_id="L1", deal_size_eur=5_000))
        analyzer.add_deal(make_lost(deal_id="L2", deal_size_eur=15_000))
        assert analyzer.total_arr_lost_eur() == 20_000.0

    def test_churned_not_in_won(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_churned(deal_id="C1", deal_size_eur=100_000))
        assert analyzer.total_arr_won_eur() == 0.0

    def test_no_decision_not_in_lost(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_no_decision(deal_id="ND1", deal_size_eur=50_000))
        assert analyzer.total_arr_lost_eur() == 0.0


# ---------------------------------------------------------------------------
# Class 21 — most_common_loss_reason
# ---------------------------------------------------------------------------


class TestMostCommonLossReason:
    def test_no_losses_returns_unknown(self):
        analyzer = CompetitiveWinLossAnalyzer()
        assert analyzer.most_common_loss_reason() == LossReason.UNKNOWN.value

    def test_single_loss(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_lost(deal_id="L1", loss_reason=LossReason.PRODUCT))
        assert analyzer.most_common_loss_reason() == "product"

    def test_most_frequent_reason(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_lost(deal_id="L1", loss_reason=LossReason.PRICE))
        analyzer.add_deal(make_lost(deal_id="L2", loss_reason=LossReason.PRICE))
        analyzer.add_deal(make_lost(deal_id="L3", loss_reason=LossReason.PRICE))
        analyzer.add_deal(make_lost(deal_id="L4", loss_reason=LossReason.PRODUCT))
        assert analyzer.most_common_loss_reason() == "price"

    def test_won_deals_not_counted(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1"))
        analyzer.add_deal(make_lost(deal_id="L1", loss_reason=LossReason.TIMING))
        assert analyzer.most_common_loss_reason() == "timing"

    def test_none_loss_reason_treated_as_unknown(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_lost(deal_id="L1", loss_reason=None))
        assert analyzer.most_common_loss_reason() == "unknown"

    def test_competitor_loss_reason(self):
        analyzer = CompetitiveWinLossAnalyzer()
        for i in range(3):
            analyzer.add_deal(make_lost(deal_id=f"L{i}", loss_reason=LossReason.COMPETITOR))
        analyzer.add_deal(make_lost(deal_id="L4", loss_reason=LossReason.RELATIONSHIP))
        assert analyzer.most_common_loss_reason() == "competitor"


# ---------------------------------------------------------------------------
# Class 22 — summary
# ---------------------------------------------------------------------------


class TestSummary:
    def _setup(self) -> CompetitiveWinLossAnalyzer:
        analyzer = CompetitiveWinLossAnalyzer()
        # Acme: 4 won, 1 lost
        for i in range(4):
            analyzer.add_deal(make_won(deal_id=f"AW{i}", competitor="Acme", deal_size_eur=10_000))
        analyzer.add_deal(make_lost(deal_id="AL1", competitor="Acme",
                                    loss_reason=LossReason.PRICE, deal_size_eur=5_000))
        # Beta: 1 won, 3 lost
        analyzer.add_deal(make_won(deal_id="BW1", competitor="Beta", deal_size_eur=8_000))
        for i in range(3):
            analyzer.add_deal(make_lost(deal_id=f"BL{i}", competitor="Beta",
                                        loss_reason=LossReason.PRODUCT, deal_size_eur=4_000))
        return analyzer

    def test_summary_keys(self):
        s = self._setup().summary()
        expected_keys = {
            "total_deals",
            "total_competitors",
            "overall_win_rate_pct",
            "total_arr_won_eur",
            "total_arr_lost_eur",
            "net_arr_eur",
            "position_counts",
            "action_counts",
            "most_common_loss_reason",
            "needs_battlecard_count",
        }
        assert set(s.keys()) == expected_keys

    def test_total_deals(self):
        s = self._setup().summary()
        assert s["total_deals"] == 9

    def test_total_competitors(self):
        s = self._setup().summary()
        assert s["total_competitors"] == 2

    def test_overall_win_rate_pct(self):
        s = self._setup().summary()
        # 5 wins out of 9
        assert s["overall_win_rate_pct"] == pytest.approx(55.6, abs=0.1)

    def test_arr_won(self):
        s = self._setup().summary()
        assert s["total_arr_won_eur"] == pytest.approx(48_000.0)

    def test_arr_lost(self):
        s = self._setup().summary()
        assert s["total_arr_lost_eur"] == pytest.approx(5_000 + 12_000)

    def test_net_arr(self):
        s = self._setup().summary()
        assert s["net_arr_eur"] == s["total_arr_won_eur"] - s["total_arr_lost_eur"]

    def test_position_counts_structure(self):
        s = self._setup().summary()
        assert "position_counts" in s
        counts = s["position_counts"]
        for pos in CompetitivePosition:
            assert pos.value in counts

    def test_action_counts_structure(self):
        s = self._setup().summary()
        counts = s["action_counts"]
        for act in CompetitiveAction:
            assert act.value in counts

    def test_most_common_loss_reason_in_summary(self):
        s = self._setup().summary()
        assert s["most_common_loss_reason"] in [r.value for r in LossReason]

    def test_needs_battlecard_count_is_int(self):
        s = self._setup().summary()
        assert isinstance(s["needs_battlecard_count"], int)
        assert s["needs_battlecard_count"] >= 0


# ---------------------------------------------------------------------------
# Class 23 — reset
# ---------------------------------------------------------------------------


class TestReset:
    def test_reset_clears_deals(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1"))
        analyzer.reset()
        assert analyzer.overall_win_rate() == 0.0

    def test_reset_clears_analyses_cache(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1", competitor="Acme"))
        _ = analyzer.analyze("Acme")
        analyzer.reset()
        # After reset, analyze_all should return empty
        assert analyzer.analyze_all() == []

    def test_reset_allows_reuse(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1"))
        analyzer.reset()
        analyzer.add_deal(make_lost(deal_id="L1", loss_reason=LossReason.PRICE))
        assert analyzer.overall_win_rate() == 0.0

    def test_double_reset_is_safe(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.reset()
        analyzer.reset()
        assert analyzer.overall_win_rate() == 0.0

    def test_reset_total_arr_won(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1", deal_size_eur=999_999))
        analyzer.reset()
        assert analyzer.total_arr_won_eur() == 0.0

    def test_reset_total_arr_lost(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_lost(deal_id="L1", deal_size_eur=999_999))
        analyzer.reset()
        assert analyzer.total_arr_lost_eur() == 0.0


# ---------------------------------------------------------------------------
# Class 24 — Integration / end-to-end scenarios
# ---------------------------------------------------------------------------


class TestIntegration:
    def test_full_pipeline(self):
        analyzer = CompetitiveWinLossAnalyzer()
        # Build a 10-deal scenario vs two competitors
        deals = [
            make_won(deal_id="W1", competitor="Alpha", deal_size_eur=15_000,
                     proof_of_concept_done=True, references_provided=True,
                     exec_sponsor_engaged=True),
            make_won(deal_id="W2", competitor="Alpha", deal_size_eur=20_000,
                     proof_of_concept_done=True, references_provided=True,
                     exec_sponsor_engaged=True),
            make_won(deal_id="W3", competitor="Alpha", deal_size_eur=10_000,
                     proof_of_concept_done=True, references_provided=False,
                     exec_sponsor_engaged=True),
            make_won(deal_id="W4", competitor="Alpha", deal_size_eur=8_000,
                     proof_of_concept_done=False, references_provided=False,
                     exec_sponsor_engaged=True),
            make_lost(deal_id="L1", competitor="Alpha", loss_reason=LossReason.PRICE,
                      deal_size_eur=5_000, price_objection=True),
            make_lost(deal_id="L2", competitor="Beta", loss_reason=LossReason.PRODUCT,
                      deal_size_eur=12_000, product_gap_mentioned=True),
            make_lost(deal_id="L3", competitor="Beta", loss_reason=LossReason.PRODUCT,
                      deal_size_eur=8_000, product_gap_mentioned=True),
            make_lost(deal_id="L4", competitor="Beta", loss_reason=LossReason.PRICE,
                      deal_size_eur=6_000, price_objection=True),
            make_won(deal_id="W5", competitor="Beta", deal_size_eur=9_000),
            make_no_decision(deal_id="ND1", competitor="Beta"),
        ]
        analyzer.add_deals(deals)

        all_results = analyzer.analyze_all()
        assert len(all_results) == 2

        alpha = analyzer.analyze("Alpha")
        assert alpha.total_deals == 5
        assert alpha.wins == 4
        assert alpha.losses == 1
        assert alpha.win_rate_pct == 80.0
        assert alpha.position == CompetitivePosition.DOMINANT
        assert alpha.action == CompetitiveAction.REPLICATE

        beta = analyzer.analyze("Beta")
        assert beta.total_deals == 5
        assert beta.wins == 1
        assert beta.losses == 3
        assert beta.no_decisions == 1
        assert beta.win_rate_pct == 20.0
        assert beta.position == CompetitivePosition.WEAK
        assert beta.action == CompetitiveAction.BATTLECARD

        # Overall: 5 wins out of 10 = 50%
        assert analyzer.overall_win_rate() == 50.0

        # Summary structure
        s = analyzer.summary()
        assert s["total_deals"] == 10
        assert s["total_competitors"] == 2

    def test_avg_cycle_days_in_loss_patterns(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deals([
            make_lost(deal_id="L1", competitor="Corp", sales_cycle_days=30,
                      loss_reason=LossReason.TIMING),
            make_lost(deal_id="L2", competitor="Corp", sales_cycle_days=90,
                      loss_reason=LossReason.TIMING),
            make_lost(deal_id="L3", competitor="Corp", sales_cycle_days=60,
                      loss_reason=LossReason.TIMING),
            make_won(deal_id="W1", competitor="Corp"),
        ])
        result = analyzer.analyze("Corp")
        # avg cycle = (30+90+60)/3 = 60
        cycle_patterns = [p for p in result.loss_patterns if "60" in p]
        assert len(cycle_patterns) >= 1

    def test_net_arr_is_negative_when_losing_more(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1", deal_size_eur=1_000))
        for i in range(3):
            analyzer.add_deal(make_lost(deal_id=f"L{i}", deal_size_eur=50_000))
        s = analyzer.summary()
        assert s["net_arr_eur"] < 0

    def test_churned_deals_not_in_wins_or_losses(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_churned(deal_id="C1", competitor="Corp", deal_size_eur=100_000))
        result = analyzer.analyze("Corp")
        assert result.wins == 0
        assert result.losses == 0
        assert result.total_deals == 1

    def test_unknown_position_with_two_deals(self):
        analyzer = CompetitiveWinLossAnalyzer()
        analyzer.add_deal(make_won(deal_id="W1", competitor="Solo"))
        analyzer.add_deal(make_lost(deal_id="L1", competitor="Solo",
                                    loss_reason=LossReason.PRICE))
        result = analyzer.analyze("Solo")
        assert result.position == CompetitivePosition.UNKNOWN
        assert result.action == CompetitiveAction.DIFFERENTIATE
