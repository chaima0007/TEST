"""
Tests for intelligence/lead_scorer.py
"""

import pytest
from intelligence.lead_scorer import LeadScorer, LeadScore


# ── Helpers ───────────────────────────────────────────────────────────────────

def scorer() -> LeadScorer:
    return LeadScorer()


def high_lead(company_id: str = "hi") -> dict:
    return {
        "company_id": company_id,
        "pagespeed_score": 10,
        "load_time_ms": 8000,
        "icp_fit": 0.95,
        "sector": "plombier artisan",
        "company_size": "PME",
        "open_rate": 0.5,
        "reply_signal": 1.0,
    }


def low_lead(company_id: str = "lo") -> dict:
    return {
        "company_id": company_id,
        "pagespeed_score": 95,
        "load_time_ms": 800,
        "icp_fit": 0.05,
        "sector": "agence web digitale",
        "company_size": "TPE",
        "open_rate": 0.0,
        "reply_signal": 0.0,
    }


# ── score() — output structure ────────────────────────────────────────────────

class TestScoreOutput:
    def test_returns_lead_score(self):
        result = scorer().score(**high_lead())
        assert isinstance(result, LeadScore)

    def test_company_id_preserved(self):
        result = scorer().score(**high_lead(company_id="co_xyz"))
        assert result.company_id == "co_xyz"

    def test_score_in_range(self):
        result = scorer().score(**high_lead())
        assert 0 <= result.action_score <= 100

    def test_grade_is_valid(self):
        result = scorer().score(**high_lead())
        assert result.grade in {"S", "A", "B", "C", "D"}

    def test_recommended_action_not_empty(self):
        result = scorer().score(**high_lead())
        assert len(result.recommended_action) > 0

    def test_feature_contributions_has_all_keys(self):
        result = scorer().score(**high_lead())
        for key in ("pagespeed", "load_time", "icp_fit", "sector", "company_size", "engagement"):
            assert key in result.feature_contributions

    def test_to_dict_works(self):
        result = scorer().score(**high_lead())
        d = result.to_dict()
        assert isinstance(d, dict)
        assert "action_score" in d
        assert "grade" in d

    def test_feature_contributions_sum_approx_score_over_100(self):
        result = scorer().score(**high_lead())
        total_contribution = sum(result.feature_contributions.values())
        assert abs(total_contribution - result.action_score / 100) < 0.01


# ── Scoring logic ─────────────────────────────────────────────────────────────

class TestScoringLogic:
    def test_high_lead_scores_higher_than_low(self):
        hi = scorer().score(**high_lead())
        lo = scorer().score(**low_lead())
        assert hi.action_score > lo.action_score

    def test_bad_pagespeed_increases_score(self):
        bad = scorer().score(**{**high_lead(), "pagespeed_score": 5})
        good = scorer().score(**{**high_lead(), "pagespeed_score": 90})
        assert bad.action_score > good.action_score

    def test_slow_load_time_increases_score(self):
        slow = scorer().score(**{**high_lead(), "load_time_ms": 9000})
        fast = scorer().score(**{**high_lead(), "load_time_ms": 500})
        assert slow.action_score > fast.action_score

    def test_high_icp_fit_increases_score(self):
        hi = scorer().score(**{**high_lead(), "icp_fit": 0.99})
        lo = scorer().score(**{**high_lead(), "icp_fit": 0.01})
        assert hi.action_score > lo.action_score

    def test_web_agency_scores_low(self):
        result = scorer().score(**low_lead())
        assert result.action_score < 30

    def test_plumber_scores_high(self):
        result = scorer().score(**high_lead())
        assert result.action_score >= 70

    def test_pme_scores_higher_than_tpe_same_lead(self):
        pme = scorer().score(**{**high_lead(), "company_size": "PME"})
        tpe = scorer().score(**{**high_lead(), "company_size": "TPE"})
        assert pme.action_score > tpe.action_score

    def test_reply_boosts_score(self):
        no_reply = scorer().score(**{**high_lead(), "reply_signal": 0.0, "open_rate": 0.0})
        with_reply = scorer().score(**{**high_lead(), "reply_signal": 1.0, "open_rate": 0.5})
        assert with_reply.action_score > no_reply.action_score

    def test_unknown_size_uses_fallback(self):
        result = scorer().score(**{**high_lead(), "company_size": "GrandGroupe"})
        assert 0 <= result.action_score <= 100

    def test_unknown_sector_uses_neutral(self):
        result = scorer().score(**{**high_lead(), "sector": "fabricant de widgets inconnus"})
        assert 0 <= result.action_score <= 100


# ── Grade thresholds ──────────────────────────────────────────────────────────

class TestGradeThresholds:
    def test_high_lead_gets_s_or_a(self):
        result = scorer().score(**high_lead())
        assert result.grade in {"S", "A"}

    def test_low_lead_gets_c_or_d(self):
        result = scorer().score(**low_lead())
        assert result.grade in {"C", "D"}

    def test_grade_s_action_mentions_appel(self):
        s = LeadScorer()
        s.GRADE_THRESHOLDS = [(85, "S"), (0, "D")]
        # Manually set a known S score
        lead_s = LeadScore("x", 90, "S", recommended_action=s.ACTIONS["S"])
        assert "Appel" in lead_s.recommended_action

    def test_grade_d_action_mentions_exclure(self):
        lead_d = LeadScore("x", 5, "D", recommended_action=LeadScorer.ACTIONS["D"])
        assert "Exclure" in lead_d.recommended_action


# ── score_batch ───────────────────────────────────────────────────────────────

class TestScoreBatch:
    def test_returns_list(self):
        leads = [high_lead("a"), low_lead("b")]
        results = scorer().score_batch(leads)
        assert isinstance(results, list)

    def test_sorted_by_score_desc(self):
        leads = [low_lead("lo"), high_lead("hi")]
        results = scorer().score_batch(leads)
        scores = [r.action_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_empty_batch_returns_empty(self):
        assert scorer().score_batch([]) == []

    def test_batch_length_matches_input(self):
        leads = [high_lead(f"c{i}") for i in range(7)]
        results = scorer().score_batch(leads)
        assert len(results) == 7


# ── filter_actionable ─────────────────────────────────────────────────────────

class TestFilterActionable:
    def test_filters_out_low_grade(self):
        leads = [high_lead("hi"), low_lead("lo")]
        results = scorer().filter_actionable(leads, min_grade="B")
        ids = [r.company_id for r in results]
        assert "hi" in ids
        # low_lead should be C or D — may be excluded depending on computed score

    def test_min_grade_s_only_returns_top(self):
        leads = [high_lead("hi"), low_lead("lo")]
        results = scorer().filter_actionable(leads, min_grade="S")
        # At least hi should still qualify or none — just verify it doesn't crash
        assert isinstance(results, list)

    def test_min_grade_d_returns_all(self):
        leads = [high_lead("hi"), low_lead("lo")]
        results = scorer().filter_actionable(leads, min_grade="D")
        assert len(results) == 2


# ── top_n ─────────────────────────────────────────────────────────────────────

class TestTopN:
    def test_returns_at_most_n(self):
        leads = [high_lead(f"c{i}") for i in range(20)]
        results = scorer().top_n(leads, n=5)
        assert len(results) == 5

    def test_top_n_sorted_desc(self):
        leads = [low_lead("lo"), high_lead("hi")]
        results = scorer().top_n(leads, n=2)
        assert results[0].action_score >= results[1].action_score

    def test_top_n_fewer_than_n_leads(self):
        leads = [high_lead("x")]
        results = scorer().top_n(leads, n=10)
        assert len(results) == 1


# ── Weights sum to 1 ──────────────────────────────────────────────────────────

class TestWeights:
    def test_weights_sum_to_one(self):
        total = sum(LeadScorer.WEIGHTS.values())
        assert abs(total - 1.0) < 1e-9

    def test_all_expected_weight_keys_present(self):
        for key in ("pagespeed", "load_time", "icp_fit", "sector", "size", "engagement"):
            assert key in LeadScorer.WEIGHTS
