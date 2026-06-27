"""
Comprehensive pytest tests for swarm/intelligence/proposal_scorer.py
"""

import pytest
from swarm.intelligence.proposal_scorer import (
    ProposalTier,
    ProposalSignals,
    ScoredProposal,
    ProposalScorer,
    _value_alignment,
    _competitive_position,
    _relationship_strength,
    _timing_fit,
    _proposal_quality,
    _compute_win_probability,
    _classify_tier,
    _WEIGHTS,
    _BASELINE_WIN_RATE,
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def make_proposal(**overrides) -> ProposalSignals:
    """Return a neutral baseline proposal, easily overridden per test."""
    defaults = dict(
        proposal_id="P001",
        client_name="Acme Corp",
        sector="Tech",
        deal_value_eur=50_000.0,
        client_budget_eur=0.0,          # unknown → value_alignment = 60
        competitor_count=0,
        has_incumbent=False,
        meetings_held=1,
        decision_maker_reached=True,
        days_to_deadline=20,            # 15–30 band → timing 90
        has_roi_model=True,
        has_case_study=True,
        has_personalization=True,
        relationship_score=50.0,
        previous_deals_won=0,
        proposal_page_count=10,         # optimal → page_score 100
        our_price_vs_market=1.0,
    )
    defaults.update(overrides)
    return ProposalSignals(**defaults)


# ─── 1. Enum values ───────────────────────────────────────────────────────────

class TestProposalTierEnum:
    def test_weak_value(self):
        assert ProposalTier.WEAK.value == "weak"

    def test_fair_value(self):
        assert ProposalTier.FAIR.value == "fair"

    def test_good_value(self):
        assert ProposalTier.GOOD.value == "good"

    def test_strong_value(self):
        assert ProposalTier.STRONG.value == "strong"

    def test_tier_is_str(self):
        # ProposalTier(str, Enum) should compare equal to its string value
        assert ProposalTier.WEAK == "weak"
        assert ProposalTier.STRONG == "strong"

    def test_four_members(self):
        assert len(ProposalTier) == 4


# ─── 2. value_alignment ───────────────────────────────────────────────────────

class TestValueAlignment:
    def test_unknown_budget_base_score(self):
        """budget <= 0 → base 60; with roi_model → stays 60."""
        p = make_proposal(client_budget_eur=0, has_roi_model=True)
        score, tips, strengths = _value_alignment(p)
        assert score == 60.0

    def test_unknown_budget_no_roi(self):
        """budget=0, no roi_model → 60-15=45."""
        p = make_proposal(client_budget_eur=0, has_roi_model=False)
        score, tips, strengths = _value_alignment(p)
        assert score == 45.0
        assert "no_roi_quantified" in tips

    def test_ratio_below_080_strength(self):
        """deal < 80 % of budget → score 100 + strength."""
        p = make_proposal(deal_value_eur=70_000, client_budget_eur=100_000, has_roi_model=True)
        score, tips, strengths = _value_alignment(p)
        assert score == 100.0
        assert "Proposition sous le budget client" in strengths

    def test_ratio_at_080_boundary(self):
        """ratio exactly 0.80 → <=0.80 branch → 100."""
        p = make_proposal(deal_value_eur=80_000, client_budget_eur=100_000, has_roi_model=True)
        score, tips, strengths = _value_alignment(p)
        assert score == 100.0

    def test_ratio_between_080_and_110(self):
        """ratio = 1.00 → 85 (no tips)."""
        p = make_proposal(deal_value_eur=100_000, client_budget_eur=100_000, has_roi_model=True)
        score, tips, strengths = _value_alignment(p)
        assert score == 85.0
        assert tips == []

    def test_ratio_between_110_and_130(self):
        """ratio = 1.20 → 60 + budget_mismatch tip."""
        p = make_proposal(deal_value_eur=120_000, client_budget_eur=100_000, has_roi_model=True)
        score, tips, strengths = _value_alignment(p)
        assert score == 60.0
        assert "budget_mismatch" in tips

    def test_ratio_above_130(self):
        """ratio = 2.0 → max(0, 100-(2-1)*80)=20."""
        p = make_proposal(deal_value_eur=200_000, client_budget_eur=100_000, has_roi_model=True)
        score, tips, strengths = _value_alignment(p)
        assert score == 20.0
        assert "budget_mismatch" in tips

    def test_ratio_very_high_clamped_to_zero(self):
        """ratio = 3.0 → max(0, 100-2*80) = 0."""
        p = make_proposal(deal_value_eur=300_000, client_budget_eur=100_000, has_roi_model=True)
        score, tips, strengths = _value_alignment(p)
        assert score == 0.0

    def test_roi_model_adds_strength(self):
        p = make_proposal(client_budget_eur=0, has_roi_model=True)
        _, _, strengths = _value_alignment(p)
        assert "ROI quantifié inclus" in strengths

    def test_no_roi_model_subtracts_15(self):
        """ratio=0.80 → 100, then -15 = 85."""
        p = make_proposal(deal_value_eur=80_000, client_budget_eur=100_000, has_roi_model=False)
        score, tips, strengths = _value_alignment(p)
        assert score == 85.0
        assert "no_roi_quantified" in tips
        assert "ROI quantifié inclus" not in strengths

    def test_score_not_below_zero_when_high_ratio_and_no_roi(self):
        """Extremely over-budget without ROI must not go below 0."""
        p = make_proposal(deal_value_eur=1_000_000, client_budget_eur=100_000, has_roi_model=False)
        score, _, _ = _value_alignment(p)
        assert score >= 0.0


# ─── 3. competitive_position ──────────────────────────────────────────────────

class TestCompetitivePosition:
    def test_no_competitors_no_incumbent_base(self):
        """base = 100-0*15-0 = 100; price=1.0 (neutral); has_case_study → +strength."""
        p = make_proposal(competitor_count=0, has_incumbent=False,
                          our_price_vs_market=1.0, has_case_study=True,
                          previous_deals_won=0)
        score, tips, strengths = _competitive_position(p)
        assert score == 100.0
        assert "Étude de cas incluse" in strengths

    def test_competitors_reduce_base(self):
        """3 competitors → 100-45=55."""
        p = make_proposal(competitor_count=3, has_incumbent=False,
                          our_price_vs_market=1.0, has_case_study=True,
                          previous_deals_won=0)
        score, tips, strengths = _competitive_position(p)
        assert score == 55.0

    def test_incumbent_reduces_base(self):
        """0 competitors + incumbent → 100-20=80."""
        p = make_proposal(competitor_count=0, has_incumbent=True,
                          our_price_vs_market=1.0, has_case_study=True,
                          previous_deals_won=0)
        score, tips, strengths = _competitive_position(p)
        assert score == 80.0

    def test_base_clamped_to_zero(self):
        """7 competitors + incumbent → 100-105-20 → clamped at 0."""
        p = make_proposal(competitor_count=7, has_incumbent=True,
                          our_price_vs_market=1.0, has_case_study=True,
                          previous_deals_won=0)
        score, tips, strengths = _competitive_position(p)
        assert score == 0.0

    def test_cheap_price_adds_15_and_strength(self):
        """price=0.85 → base+15; strength added."""
        p = make_proposal(competitor_count=0, has_incumbent=False,
                          our_price_vs_market=0.85, has_case_study=True,
                          previous_deals_won=0)
        score, tips, strengths = _competitive_position(p)
        assert score == 100.0          # min(100, 100+15)
        assert "Prix compétitif vs marché" in strengths

    def test_cheap_price_exactly_090_boundary(self):
        p = make_proposal(competitor_count=0, has_incumbent=False,
                          our_price_vs_market=0.90, has_case_study=True,
                          previous_deals_won=0)
        score, _, strengths = _competitive_position(p)
        assert "Prix compétitif vs marché" in strengths

    def test_premium_price_subtracts_20(self):
        """price=1.40 → base-20; tip added."""
        p = make_proposal(competitor_count=0, has_incumbent=False,
                          our_price_vs_market=1.40, has_case_study=True,
                          previous_deals_won=0)
        score, tips, strengths = _competitive_position(p)
        assert score == 80.0
        assert "weak_competitive" in tips

    def test_no_case_study_subtracts_10_and_tip(self):
        p = make_proposal(competitor_count=0, has_incumbent=False,
                          our_price_vs_market=1.0, has_case_study=False,
                          previous_deals_won=0)
        score, tips, strengths = _competitive_position(p)
        assert score == 90.0
        assert "no_references" in tips

    def test_previous_deals_boost(self):
        """2 previous wins → base + 2*10 = 120 → clamped 100."""
        p = make_proposal(competitor_count=0, has_incumbent=False,
                          our_price_vs_market=1.0, has_case_study=True,
                          previous_deals_won=2)
        score, tips, strengths = _competitive_position(p)
        assert score == 100.0
        assert "2 deal(s) précédent(s) remporté(s)" in strengths

    def test_previous_deals_strength_label(self):
        p = make_proposal(competitor_count=2, has_incumbent=False,
                          our_price_vs_market=1.0, has_case_study=True,
                          previous_deals_won=1)
        _, _, strengths = _competitive_position(p)
        assert "1 deal(s) précédent(s) remporté(s)" in strengths


# ─── 4. relationship_strength ─────────────────────────────────────────────────

class TestRelationshipStrength:
    def test_decision_maker_reached_strength(self):
        p = make_proposal(decision_maker_reached=True, relationship_score=50.0,
                          meetings_held=0)
        score, tips, strengths = _relationship_strength(p)
        assert "Décideur contacté" in strengths
        assert "low_relationship" not in tips

    def test_no_decision_maker_reduces_score(self):
        """50 - 25 = 25, meetings=0 → no bonus."""
        p = make_proposal(decision_maker_reached=False, relationship_score=50.0,
                          meetings_held=0)
        score, tips, strengths = _relationship_strength(p)
        assert score == 25.0
        assert "low_relationship" in tips

    def test_meetings_bonus_capped_at_30(self):
        """5 meetings → min(30, 5*7.5)=30."""
        p = make_proposal(decision_maker_reached=True, relationship_score=60.0,
                          meetings_held=5)
        score, tips, strengths = _relationship_strength(p)
        assert score == min(100.0, 60.0 + 30.0)

    def test_meetings_bonus_partial(self):
        """2 meetings → bonus 15."""
        p = make_proposal(decision_maker_reached=True, relationship_score=50.0,
                          meetings_held=2)
        score, tips, _ = _relationship_strength(p)
        assert score == 65.0

    def test_three_plus_meetings_strength(self):
        p = make_proposal(decision_maker_reached=True, relationship_score=50.0,
                          meetings_held=3)
        _, _, strengths = _relationship_strength(p)
        assert "3 réunions tenues" in strengths

    def test_zero_meetings_tip(self):
        p = make_proposal(decision_maker_reached=True, relationship_score=50.0,
                          meetings_held=0)
        _, tips, _ = _relationship_strength(p)
        assert "single_contact" in tips

    def test_score_clamped_at_100(self):
        p = make_proposal(decision_maker_reached=True, relationship_score=90.0,
                          meetings_held=4)
        score, _, _ = _relationship_strength(p)
        assert score == 100.0

    def test_score_not_below_zero(self):
        p = make_proposal(decision_maker_reached=False, relationship_score=0.0,
                          meetings_held=0)
        score, _, _ = _relationship_strength(p)
        assert score == 0.0


# ─── 5. timing_fit ────────────────────────────────────────────────────────────

class TestTimingFit:
    def test_past_deadline_returns_zero(self):
        p = make_proposal(days_to_deadline=0, has_incumbent=False)
        score, tips, strengths = _timing_fit(p)
        assert score == 0.0
        assert "deadline_pressure" in tips

    def test_negative_deadline_returns_zero(self):
        p = make_proposal(days_to_deadline=-5, has_incumbent=False)
        score, tips, _ = _timing_fit(p)
        assert score == 0.0
        assert "deadline_pressure" in tips

    def test_1_to_7_days(self):
        p = make_proposal(days_to_deadline=5, has_incumbent=False)
        score, tips, _ = _timing_fit(p)
        assert score == 30.0
        assert "deadline_pressure" in tips

    def test_8_to_14_days(self):
        p = make_proposal(days_to_deadline=10, has_incumbent=False)
        score, tips, strengths = _timing_fit(p)
        assert score == 60.0
        assert "deadline_pressure" not in tips

    def test_15_to_30_days(self):
        p = make_proposal(days_to_deadline=20, has_incumbent=False)
        score, _, strengths = _timing_fit(p)
        assert score == 90.0
        assert "Délai favorable pour préparer la réponse" in strengths

    def test_31_to_60_days(self):
        p = make_proposal(days_to_deadline=45, has_incumbent=False)
        score, _, strengths = _timing_fit(p)
        assert score == 100.0
        assert "Timing excellent" in strengths

    def test_beyond_60_days_decay(self):
        """days=80 → max(60, 100-(80-60)*0.5) = max(60, 90) = 90."""
        p = make_proposal(days_to_deadline=80, has_incumbent=False)
        score, _, _ = _timing_fit(p)
        assert score == 90.0

    def test_beyond_60_days_decay_floor_at_60(self):
        """days=160 → max(60, 100-100*0.5) = max(60, 50) = 60."""
        p = make_proposal(days_to_deadline=160, has_incumbent=False)
        score, _, _ = _timing_fit(p)
        assert score == 60.0

    def test_incumbent_and_short_deadline_penalty(self):
        """days=10, incumbent → 60 - 15 = 45."""
        p = make_proposal(days_to_deadline=10, has_incumbent=True)
        score, tips, _ = _timing_fit(p)
        assert score == 45.0
        assert "poor_timing" in tips

    def test_incumbent_long_deadline_no_penalty(self):
        """Incumbent but >14 days → no poor_timing."""
        p = make_proposal(days_to_deadline=20, has_incumbent=True)
        score, tips, _ = _timing_fit(p)
        assert "poor_timing" not in tips

    def test_exactly_14_days_with_incumbent(self):
        """Boundary: days=14, has_incumbent → 60-15=45."""
        p = make_proposal(days_to_deadline=14, has_incumbent=True)
        score, tips, _ = _timing_fit(p)
        assert score == 45.0
        assert "poor_timing" in tips


# ─── 6. proposal_quality ──────────────────────────────────────────────────────

class TestProposalQuality:
    def _quality(self, pages, personalized, case_study):
        p = make_proposal(proposal_page_count=pages,
                          has_personalization=personalized,
                          has_case_study=case_study)
        return _proposal_quality(p)

    def test_pages_below_5(self):
        """page_score=40."""
        score, _, _ = self._quality(3, True, True)
        expected = 40 * 0.3 + 100 * 0.4 + 100 * 0.3
        assert abs(score - expected) < 1e-9

    def test_pages_5_to_20_optimal(self):
        """page_score=100; strength added."""
        score, _, strengths = self._quality(10, True, True)
        expected = 100 * 0.3 + 100 * 0.4 + 100 * 0.3
        assert score == expected
        assert "Longueur de proposition optimale" in strengths

    def test_pages_21_to_40(self):
        """page_score=75."""
        score, _, _ = self._quality(30, True, True)
        expected = 75 * 0.3 + 100 * 0.4 + 100 * 0.3
        assert abs(score - expected) < 1e-9

    def test_pages_above_40_decay(self):
        """pages=50 → max(40, 75-(50-40)*1.5) = max(40, 60) = 60."""
        score, _, _ = self._quality(50, True, True)
        page_score = max(40.0, 75.0 - (50 - 40) * 1.5)
        expected = page_score * 0.3 + 100 * 0.4 + 100 * 0.3
        assert abs(score - expected) < 1e-9

    def test_pages_above_40_floor_at_40(self):
        """pages=80 → max(40, 75-60*1.5) = max(40, -15) = 40."""
        score, _, _ = self._quality(80, True, True)
        page_score = 40.0
        expected = page_score * 0.3 + 100 * 0.4 + 100 * 0.3
        assert abs(score - expected) < 1e-9

    def test_no_personalization_tip(self):
        _, tips, _ = self._quality(10, False, True)
        assert "no_personalization" in tips

    def test_personalization_strength(self):
        _, _, strengths = self._quality(10, True, True)
        assert "Proposition personnalisée" in strengths

    def test_no_case_study_tip(self):
        _, tips, _ = self._quality(10, True, False)
        assert "missing_case_study" in tips

    def test_no_personalization_uses_score_50(self):
        score, _, _ = self._quality(10, False, True)
        expected = 100 * 0.3 + 50 * 0.4 + 100 * 0.3
        assert abs(score - expected) < 1e-9

    def test_no_case_study_uses_score_60(self):
        score, _, _ = self._quality(10, True, False)
        expected = 100 * 0.3 + 100 * 0.4 + 60 * 0.3
        assert abs(score - expected) < 1e-9

    def test_all_negative_minimum(self):
        """pages=3, no personalization, no case study → lowest score."""
        score, _, _ = self._quality(3, False, False)
        expected = 40 * 0.3 + 50 * 0.4 + 60 * 0.3
        assert abs(score - expected) < 1e-9


# ─── 7. win_probability formula ───────────────────────────────────────────────

class TestWinProbabilityFormula:
    def test_all_100_dimension_scores(self):
        """composite=100 → prob = 0.20 + 1.0*0.60 = 0.80."""
        dims = {k: 100.0 for k in _WEIGHTS}
        prob = _compute_win_probability(dims)
        assert prob == pytest.approx(0.80, abs=1e-4)

    def test_all_zero_dimension_scores(self):
        """composite=0 → prob = 0.20."""
        dims = {k: 0.0 for k in _WEIGHTS}
        prob = _compute_win_probability(dims)
        assert prob == pytest.approx(0.20, abs=1e-4)

    def test_all_50_dimension_scores(self):
        """composite=50 → prob = 0.20 + 0.5*0.60 = 0.50."""
        dims = {k: 50.0 for k in _WEIGHTS}
        prob = _compute_win_probability(dims)
        assert prob == pytest.approx(0.50, abs=1e-4)

    def test_baseline_win_rate(self):
        assert _BASELINE_WIN_RATE == 0.20

    def test_weights_sum_to_one(self):
        assert sum(_WEIGHTS.values()) == pytest.approx(1.0, abs=1e-9)

    def test_specific_composite(self):
        """Manually compute a mixed score."""
        dims = {
            "value_alignment": 80.0,
            "competitive_position": 60.0,
            "relationship_strength": 70.0,
            "timing_fit": 90.0,
            "proposal_quality": 50.0,
        }
        composite = (
            80.0 * 0.20
            + 60.0 * 0.25
            + 70.0 * 0.20
            + 90.0 * 0.15
            + 50.0 * 0.20
        )
        expected = 0.20 + (composite / 100.0) * 0.60
        assert _compute_win_probability(dims) == pytest.approx(expected, abs=1e-4)

    def test_result_clamped_between_0_and_1(self):
        dims = {k: 0.0 for k in _WEIGHTS}
        prob = _compute_win_probability(dims)
        assert 0.0 <= prob <= 1.0


# ─── 8. Tier classification boundaries ───────────────────────────────────────

class TestTierClassification:
    def test_strong_at_exactly_065(self):
        assert _classify_tier(0.65) == ProposalTier.STRONG

    def test_strong_above_065(self):
        assert _classify_tier(0.80) == ProposalTier.STRONG

    def test_good_at_exactly_050(self):
        assert _classify_tier(0.50) == ProposalTier.GOOD

    def test_good_below_065(self):
        assert _classify_tier(0.64) == ProposalTier.GOOD

    def test_fair_at_exactly_035(self):
        assert _classify_tier(0.35) == ProposalTier.FAIR

    def test_fair_below_050(self):
        assert _classify_tier(0.49) == ProposalTier.FAIR

    def test_weak_below_035(self):
        assert _classify_tier(0.34) == ProposalTier.WEAK

    def test_weak_at_zero(self):
        assert _classify_tier(0.0) == ProposalTier.WEAK

    def test_strong_at_one(self):
        assert _classify_tier(1.0) == ProposalTier.STRONG


# ─── 9. ProposalScorer CRUD & queries ────────────────────────────────────────

class TestProposalScorerCRUD:
    def setup_method(self):
        self.scorer = ProposalScorer()

    def test_score_returns_scored_proposal(self):
        p = make_proposal()
        result = self.scorer.score(p)
        assert isinstance(result, ScoredProposal)

    def test_score_stores_result(self):
        p = make_proposal(proposal_id="X1")
        self.scorer.score(p)
        assert self.scorer.get("X1") is not None

    def test_get_missing_returns_none(self):
        assert self.scorer.get("nonexistent") is None

    def test_get_returns_correct_proposal(self):
        p = make_proposal(proposal_id="ABC")
        scored = self.scorer.score(p)
        retrieved = self.scorer.get("ABC")
        assert retrieved is scored

    def test_score_overwrites_same_id(self):
        p1 = make_proposal(proposal_id="DUP", deal_value_eur=10_000)
        p2 = make_proposal(proposal_id="DUP", deal_value_eur=99_000)
        self.scorer.score(p1)
        self.scorer.score(p2)
        retrieved = self.scorer.get("DUP")
        assert retrieved.proposal.deal_value_eur == 99_000

    def test_all_scored_returns_all(self):
        for i in range(3):
            self.scorer.score(make_proposal(proposal_id=f"P{i}"))
        assert len(self.scorer.all_scored()) == 3

    def test_all_scored_sorted_descending(self):
        """Proposals inserted in no particular order should come back sorted."""
        self.scorer.score(make_proposal(proposal_id="A", relationship_score=10.0,
                                        meetings_held=0, decision_maker_reached=False))
        self.scorer.score(make_proposal(proposal_id="B", relationship_score=90.0,
                                        meetings_held=4, decision_maker_reached=True))
        self.scorer.score(make_proposal(proposal_id="C", relationship_score=50.0,
                                        meetings_held=2, decision_maker_reached=True))
        results = self.scorer.all_scored()
        probs = [r.win_probability for r in results]
        assert probs == sorted(probs, reverse=True)

    def test_score_batch_returns_list(self):
        proposals = [make_proposal(proposal_id=f"B{i}") for i in range(4)]
        results = self.scorer.score_batch(proposals)
        assert len(results) == 4
        assert all(isinstance(r, ScoredProposal) for r in results)

    def test_score_batch_stores_all(self):
        proposals = [make_proposal(proposal_id=f"C{i}") for i in range(3)]
        self.scorer.score_batch(proposals)
        assert len(self.scorer.all_scored()) == 3


# ─── 10. top_prospects ───────────────────────────────────────────────────────

class TestTopProspects:
    def setup_method(self):
        self.scorer = ProposalScorer()

    def test_top_prospects_default_n5(self):
        for i in range(10):
            self.scorer.score(make_proposal(proposal_id=f"T{i}"))
        assert len(self.scorer.top_prospects()) == 5

    def test_top_prospects_custom_n(self):
        for i in range(10):
            self.scorer.score(make_proposal(proposal_id=f"U{i}"))
        assert len(self.scorer.top_prospects(3)) == 3

    def test_top_prospects_ordered_best_first(self):
        self.scorer.score(make_proposal(proposal_id="LOW", relationship_score=5.0,
                                        meetings_held=0, decision_maker_reached=False))
        self.scorer.score(make_proposal(proposal_id="HIGH", relationship_score=90.0,
                                        meetings_held=4, decision_maker_reached=True))
        top = self.scorer.top_prospects(1)
        assert top[0].proposal.proposal_id == "HIGH"

    def test_top_prospects_fewer_than_n(self):
        self.scorer.score(make_proposal(proposal_id="ONLY"))
        assert len(self.scorer.top_prospects(10)) == 1


# ─── 11. by_tier & at_risk ───────────────────────────────────────────────────

class TestFilters:
    def setup_method(self):
        self.scorer = ProposalScorer()

    def _force_tier(self, proposal_id: str, tier: ProposalTier) -> ScoredProposal:
        """
        Score a proposal and patch its tier for filter testing,
        or craft a proposal that naturally produces that tier.
        We directly inject into the store for isolation.
        """
        p = make_proposal(proposal_id=proposal_id)
        sp = self.scorer.score(p)
        # Patch in-place so we can test filter logic independently of scorer math
        object.__setattr__(sp, "proposal_tier", tier)
        self.scorer._store[proposal_id] = sp
        return sp

    def test_by_tier_strong(self):
        self._force_tier("S1", ProposalTier.STRONG)
        self._force_tier("W1", ProposalTier.WEAK)
        strong = self.scorer.by_tier(ProposalTier.STRONG)
        assert len(strong) == 1
        assert strong[0].proposal.proposal_id == "S1"

    def test_by_tier_empty(self):
        self._force_tier("F1", ProposalTier.FAIR)
        good = self.scorer.by_tier(ProposalTier.GOOD)
        assert good == []

    def test_at_risk_returns_only_weak(self):
        self._force_tier("W2", ProposalTier.WEAK)
        self._force_tier("G1", ProposalTier.GOOD)
        at_risk = self.scorer.at_risk()
        assert len(at_risk) == 1
        assert at_risk[0].proposal.proposal_id == "W2"

    def test_at_risk_empty_when_no_weak(self):
        self._force_tier("S2", ProposalTier.STRONG)
        assert self.scorer.at_risk() == []

    def test_by_tier_multiple_results(self):
        self._force_tier("F2", ProposalTier.FAIR)
        self._force_tier("F3", ProposalTier.FAIR)
        fairs = self.scorer.by_tier(ProposalTier.FAIR)
        assert len(fairs) == 2


# ─── 12. summary() ───────────────────────────────────────────────────────────

class TestSummary:
    def setup_method(self):
        self.scorer = ProposalScorer()

    def test_summary_empty_returns_zeros(self):
        s = self.scorer.summary()
        assert s["total"] == 0
        assert s["avg_win_probability"] == 0.0
        assert s["best_win_probability"] == 0.0
        assert s["total_pipeline_eur"] == 0.0
        assert s["expected_won_eur"] == 0.0

    def test_summary_empty_tier_counts_all_zero(self):
        s = self.scorer.summary()
        assert all(v == 0 for v in s["tier_counts"].values())
        assert set(s["tier_counts"].keys()) == {"weak", "fair", "good", "strong"}

    def test_summary_total_count(self):
        for i in range(3):
            self.scorer.score(make_proposal(proposal_id=f"P{i}"))
        assert self.scorer.summary()["total"] == 3

    def test_summary_total_pipeline(self):
        self.scorer.score(make_proposal(proposal_id="PA", deal_value_eur=10_000))
        self.scorer.score(make_proposal(proposal_id="PB", deal_value_eur=40_000))
        s = self.scorer.summary()
        assert s["total_pipeline_eur"] == pytest.approx(50_000, abs=0.01)

    def test_summary_expected_won(self):
        p1 = make_proposal(proposal_id="E1", deal_value_eur=100_000)
        p2 = make_proposal(proposal_id="E2", deal_value_eur=200_000)
        r1 = self.scorer.score(p1)
        r2 = self.scorer.score(p2)
        s = self.scorer.summary()
        expected = r1.win_probability * 100_000 + r2.win_probability * 200_000
        assert s["expected_won_eur"] == pytest.approx(expected, abs=0.01)

    def test_summary_avg_win_probability(self):
        p1 = make_proposal(proposal_id="AV1")
        p2 = make_proposal(proposal_id="AV2")
        r1 = self.scorer.score(p1)
        r2 = self.scorer.score(p2)
        s = self.scorer.summary()
        expected_avg = (r1.win_probability + r2.win_probability) / 2
        assert s["avg_win_probability"] == pytest.approx(expected_avg, abs=1e-4)

    def test_summary_best_win_probability(self):
        r_low = self.scorer.score(make_proposal(
            proposal_id="BL", relationship_score=5.0, meetings_held=0,
            decision_maker_reached=False))
        r_high = self.scorer.score(make_proposal(
            proposal_id="BH", relationship_score=90.0, meetings_held=4,
            decision_maker_reached=True))
        s = self.scorer.summary()
        assert s["best_win_probability"] == max(r_low.win_probability, r_high.win_probability)

    def test_summary_tier_counts_correct(self):
        """Patch tiers directly and check tier_counts."""
        sp = self.scorer.score(make_proposal(proposal_id="TC1"))
        object.__setattr__(sp, "proposal_tier", ProposalTier.STRONG)
        self.scorer._store["TC1"] = sp
        s = self.scorer.summary()
        assert s["tier_counts"]["strong"] == 1


# ─── 13. reset() ─────────────────────────────────────────────────────────────

class TestReset:
    def setup_method(self):
        self.scorer = ProposalScorer()

    def test_reset_clears_store(self):
        for i in range(5):
            self.scorer.score(make_proposal(proposal_id=f"R{i}"))
        self.scorer.reset()
        assert self.scorer.all_scored() == []

    def test_reset_get_returns_none(self):
        self.scorer.score(make_proposal(proposal_id="RG1"))
        self.scorer.reset()
        assert self.scorer.get("RG1") is None

    def test_reset_summary_zeroed(self):
        self.scorer.score(make_proposal(proposal_id="RS1"))
        self.scorer.reset()
        assert self.scorer.summary()["total"] == 0

    def test_reset_then_score_works(self):
        self.scorer.score(make_proposal(proposal_id="RT1"))
        self.scorer.reset()
        self.scorer.score(make_proposal(proposal_id="RT2"))
        assert len(self.scorer.all_scored()) == 1


# ─── 14. to_dict() ───────────────────────────────────────────────────────────

class TestToDict:
    def setup_method(self):
        self.scorer = ProposalScorer()
        self.sp = self.scorer.score(make_proposal(proposal_id="D1"))

    def test_scored_proposal_to_dict_keys(self):
        d = self.sp.to_dict()
        assert set(d.keys()) == {
            "proposal", "win_probability", "proposal_tier",
            "dimension_scores", "recommendations", "strengths"
        }

    def test_proposal_tier_is_string(self):
        d = self.sp.to_dict()
        assert isinstance(d["proposal_tier"], str)

    def test_dimension_scores_keys(self):
        d = self.sp.to_dict()
        assert set(d["dimension_scores"].keys()) == {
            "value_alignment", "competitive_position",
            "relationship_strength", "timing_fit", "proposal_quality"
        }

    def test_proposal_dict_has_proposal_id(self):
        d = self.sp.to_dict()
        assert d["proposal"]["proposal_id"] == "D1"

    def test_proposal_signals_to_dict(self):
        p = make_proposal(proposal_id="SIG1")
        d = p.to_dict()
        assert "proposal_id" in d
        assert "client_name" in d
        assert "deal_value_eur" in d

    def test_recommendations_is_list(self):
        d = self.sp.to_dict()
        assert isinstance(d["recommendations"], list)

    def test_strengths_is_list(self):
        d = self.sp.to_dict()
        assert isinstance(d["strengths"], list)

    def test_win_probability_is_float(self):
        d = self.sp.to_dict()
        assert isinstance(d["win_probability"], float)


# ─── 15. Integration / end-to-end ────────────────────────────────────────────

class TestIntegration:
    def setup_method(self):
        self.scorer = ProposalScorer()

    def test_full_score_pipeline(self):
        """Smoke test: score a proposal and verify all output fields are populated."""
        p = make_proposal(
            proposal_id="INT1",
            deal_value_eur=80_000,
            client_budget_eur=100_000,
            competitor_count=2,
            has_incumbent=False,
            meetings_held=3,
            decision_maker_reached=True,
            days_to_deadline=25,
            has_roi_model=True,
            has_case_study=True,
            has_personalization=True,
            relationship_score=60.0,
            previous_deals_won=1,
            proposal_page_count=15,
            our_price_vs_market=0.95,
        )
        result = self.scorer.score(p)
        assert isinstance(result.win_probability, float)
        assert 0.0 <= result.win_probability <= 1.0
        assert isinstance(result.proposal_tier, ProposalTier)
        assert len(result.dimension_scores) == 5
        assert result.proposal is p

    def test_strong_proposal_characteristics(self):
        """Ideal proposal should achieve STRONG tier."""
        p = make_proposal(
            proposal_id="STRONG",
            deal_value_eur=80_000,
            client_budget_eur=100_000,   # ratio 0.8 → 100
            competitor_count=0,
            has_incumbent=False,
            meetings_held=4,
            decision_maker_reached=True,
            days_to_deadline=45,         # timing = 100
            has_roi_model=True,
            has_case_study=True,
            has_personalization=True,
            relationship_score=80.0,
            previous_deals_won=2,
            proposal_page_count=15,
            our_price_vs_market=0.85,    # competitive price
        )
        result = self.scorer.score(p)
        assert result.proposal_tier == ProposalTier.STRONG

    def test_weak_proposal_characteristics(self):
        """Worst-case proposal should be WEAK."""
        p = make_proposal(
            proposal_id="WEAK",
            deal_value_eur=300_000,
            client_budget_eur=100_000,   # ratio=3 → score 0
            competitor_count=5,
            has_incumbent=True,
            meetings_held=0,
            decision_maker_reached=False,
            days_to_deadline=0,          # past deadline → 0
            has_roi_model=False,
            has_case_study=False,
            has_personalization=False,
            relationship_score=10.0,
            previous_deals_won=0,
            proposal_page_count=2,
            our_price_vs_market=1.50,
        )
        result = self.scorer.score(p)
        assert result.proposal_tier == ProposalTier.WEAK

    def test_recommendations_are_full_strings_not_keys(self):
        """The recommendations list should contain translated strings, not raw keys."""
        p = make_proposal(
            proposal_id="REC",
            has_roi_model=False,          # triggers no_roi_quantified
            client_budget_eur=0,
        )
        result = self.scorer.score(p)
        assert all(not r.startswith("no_") for r in result.recommendations)
        assert any("ROI" in r for r in result.recommendations)

    def test_duplicate_tips_deduplicated(self):
        """A tip that would fire in multiple dimensions only appears once."""
        # no_references can appear in competitive_position only,
        # but we can ensure recommendations list has no duplicates.
        p = make_proposal(
            proposal_id="DED",
            has_case_study=False,
            has_personalization=False,
            has_roi_model=False,
            client_budget_eur=0,
        )
        result = self.scorer.score(p)
        assert len(result.recommendations) == len(set(result.recommendations))

    def test_score_batch_same_as_individual(self):
        proposals = [make_proposal(proposal_id=f"BS{i}") for i in range(3)]
        scorer_batch = ProposalScorer()
        scorer_single = ProposalScorer()
        batch_results = scorer_batch.score_batch(proposals)
        single_results = [scorer_single.score(p) for p in proposals]
        for br, sr in zip(batch_results, single_results):
            assert br.win_probability == sr.win_probability
            assert br.proposal_tier == sr.proposal_tier
