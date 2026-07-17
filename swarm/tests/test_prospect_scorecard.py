"""Tests for ProspectScorecard."""

import pytest
from intelligence.prospect_scorecard import (
    BANTDimension,
    BehavioralDimension,
    MarketFitDimension,
    ProspectScorecard,
    Scorecard,
    ScorecardTier,
    TemporalDimension,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture()
def engine():
    return ProspectScorecard()


def _bant(b=80, a=70, n=80, t=60) -> BANTDimension:
    return BANTDimension(budget_score=b, authority_score=a, need_score=n, timeline_score=t)


def _behav(**kwargs) -> BehavioralDimension:
    return BehavioralDimension(**kwargs)


def _temp(days=3.0, resp_h=4.0, freq=5.0) -> TemporalDimension:
    return TemporalDimension(days_since_contact=days, response_time_hours=resp_h, contact_frequency=freq)


def _fit(sector=True, web=True, age=5.0, emp=5) -> MarketFitDimension:
    return MarketFitDimension(sector_match=sector, has_website=web, company_age_years=age, employee_count=emp)


def _score(engine, pid="p001", **kwargs):
    defaults = dict(
        company_name="Test Co",
        sector="artisan",
        bant=_bant(),
        behavioral=_behav(replied_email=True),
        temporal=_temp(),
        market_fit=_fit(),
    )
    defaults.update(kwargs)
    return engine.score(pid, **defaults)


# ── BANTDimension ─────────────────────────────────────────────────────────────

class TestBANTDimension:
    def test_composite_in_range(self):
        b = _bant(100, 100, 100, 100)
        assert 0 <= b.composite <= 40

    def test_zero_bant_gives_zero(self):
        b = _bant(0, 0, 0, 0)
        assert b.composite == 0

    def test_high_bant_gives_high_score(self):
        b = _bant(100, 100, 100, 100)
        assert b.composite >= 35

    def test_budget_weighted_highest(self):
        high_budget = _bant(100, 0, 0, 0).composite
        high_authority = _bant(0, 100, 0, 0).composite
        assert high_budget > high_authority


# ── BehavioralDimension ───────────────────────────────────────────────────────

class TestBehavioralDimension:
    def test_no_engagement_zero(self):
        assert BehavioralDimension().composite == 0

    def test_all_engaged_max_30(self):
        b = BehavioralDimension(
            opened_email=True, replied_email=True, clicked_link=True,
            attended_demo=True, visited_website=True, requested_quote=True,
        )
        assert b.composite <= 30

    def test_replied_adds_points(self):
        no_reply = BehavioralDimension(opened_email=True).composite
        with_reply = BehavioralDimension(opened_email=True, replied_email=True).composite
        assert with_reply > no_reply

    def test_attended_demo_adds_points(self):
        without = BehavioralDimension(replied_email=True).composite
        with_demo = BehavioralDimension(replied_email=True, attended_demo=True).composite
        assert with_demo > without

    def test_composite_capped_at_30(self):
        b = BehavioralDimension(True, True, True, True, True, True)
        assert b.composite <= 30


# ── TemporalDimension ─────────────────────────────────────────────────────────

class TestTemporalDimension:
    def test_zero_days_max_recency(self):
        t = TemporalDimension(days_since_contact=0)
        assert t.recency_score == 10

    def test_old_contact_low_recency(self):
        t = TemporalDimension(days_since_contact=30)
        assert t.recency_score == 0

    def test_fast_response_adds_score(self):
        slow = TemporalDimension(response_time_hours=100).response_speed_score
        fast = TemporalDimension(response_time_hours=1).response_speed_score
        assert fast > slow

    def test_no_response_time_zero(self):
        t = TemporalDimension(response_time_hours=None)
        assert t.response_speed_score == 0

    def test_composite_in_range(self):
        t = _temp(days=0, resp_h=0.5, freq=2.0)
        assert 0 <= t.composite <= 20


# ── MarketFitDimension ────────────────────────────────────────────────────────

class TestMarketFitDimension:
    def test_zero_fit(self):
        m = MarketFitDimension()
        assert m.composite == 0

    def test_full_fit(self):
        m = _fit(sector=True, web=True, age=10, emp=10)
        assert m.composite == 10

    def test_sector_match_adds_most(self):
        no_sector = MarketFitDimension(sector_match=False, has_website=True).composite
        with_sector = MarketFitDimension(sector_match=True, has_website=True).composite
        assert with_sector > no_sector

    def test_young_company_lower_score(self):
        young = MarketFitDimension(sector_match=True, company_age_years=0.5).composite
        old = MarketFitDimension(sector_match=True, company_age_years=10).composite
        assert old > young


# ── Scorecard ─────────────────────────────────────────────────────────────────

class TestScorecard:
    def test_total_score_in_range(self, engine):
        card = _score(engine)
        assert 0 <= card.total_score <= 100

    def test_tier_is_valid(self, engine):
        card = _score(engine)
        assert card.tier in list(ScorecardTier)

    def test_high_score_tier_a(self, engine):
        card = engine.score(
            "p001", "Top Co", "artisan",
            bant=_bant(100, 100, 100, 100),
            behavioral=BehavioralDimension(True, True, True, True, True, True),
            temporal=TemporalDimension(0, 0.5, 2.0),
            market_fit=_fit(),
        )
        assert card.total_score >= 80
        assert card.tier == ScorecardTier.A

    def test_zero_score_tier_d(self, engine):
        card = engine.score(
            "p001", "Cold Co", "unknown",
            bant=_bant(0, 0, 0, 0),
            behavioral=BehavioralDimension(),
            temporal=TemporalDimension(days_since_contact=60),
            market_fit=MarketFitDimension(),
        )
        assert card.tier == ScorecardTier.D

    def test_dimension_breakdown_sums_to_total(self, engine):
        card = _score(engine)
        breakdown = card.dimension_breakdown
        assert sum(breakdown.values()) == card.total_score

    def test_to_dict_has_all_keys(self, engine):
        card = _score(engine)
        d = card.to_dict()
        for k in ["prospect_id", "company_name", "sector", "total_score", "tier",
                  "bant_score", "behavioral_score", "temporal_score", "market_fit_score",
                  "dimension_breakdown", "notes", "created_at", "updated_at"]:
            assert k in d

    def test_tier_value_is_string(self, engine):
        card = _score(engine)
        assert card.to_dict()["tier"] in ["A", "B", "C", "D"]


# ── Tier thresholds ───────────────────────────────────────────────────────────

class TestTierThresholds:
    def test_tier_a_gte_80(self, engine):
        card = _score(engine)
        if card.total_score >= 80:
            assert card.tier == ScorecardTier.A

    def test_tier_b_60_to_79(self, engine):
        card = _score(engine)
        if 60 <= card.total_score < 80:
            assert card.tier == ScorecardTier.B

    def test_tier_c_40_to_59(self, engine):
        card = _score(engine)
        if 40 <= card.total_score < 60:
            assert card.tier == ScorecardTier.C

    def test_tier_d_below_40(self, engine):
        card = engine.score("p001", "Cold", sector="unknown",
                            bant=_bant(0, 0, 0, 0), behavioral=BehavioralDimension(),
                            temporal=TemporalDimension(60), market_fit=MarketFitDimension())
        assert card.tier == ScorecardTier.D


# ── update ────────────────────────────────────────────────────────────────────

class TestUpdate:
    def test_update_behavioral(self, engine):
        _score(engine)
        engine.update("p001", behavioral=BehavioralDimension(True, True, True, True, True, True))
        assert engine.get("p001").behavioral_score == 30

    def test_update_notes(self, engine):
        _score(engine)
        engine.update("p001", notes="Updated note")
        assert engine.get("p001").notes == "Updated note"

    def test_update_missing_returns_none(self, engine):
        assert engine.update("p999") is None

    def test_update_preserves_other_dims(self, engine):
        card = _score(engine)
        original_bant = card.bant_score
        engine.update("p001", behavioral=BehavioralDimension(replied_email=True))
        assert engine.get("p001").bant_score == original_bant


# ── Queries ───────────────────────────────────────────────────────────────────

class TestQueries:
    def test_get_existing(self, engine):
        card = _score(engine)
        assert engine.get("p001") is card

    def test_get_missing(self, engine):
        assert engine.get("p999") is None

    def test_all_scorecards_sorted(self, engine):
        _score(engine, "p001", bant=_bant(100, 100, 100, 100))
        _score(engine, "p002", bant=_bant(0, 0, 0, 0))
        cards = engine.all_scorecards()
        assert cards[0].total_score >= cards[-1].total_score

    def test_all_scorecards_limit(self, engine):
        for i in range(6):
            _score(engine, f"p{i:03d}")
        assert len(engine.all_scorecards(limit=3)) == 3

    def test_by_tier(self, engine):
        engine.score("p001", "Top", bant=_bant(100, 100, 100, 100),
                     behavioral=BehavioralDimension(True, True, True, True, True, True),
                     temporal=TemporalDimension(0, 0.5, 2.0),
                     market_fit=_fit())
        tier_a = engine.by_tier(ScorecardTier.A)
        assert all(c.tier == ScorecardTier.A for c in tier_a)

    def test_top_n(self, engine):
        for i in range(8):
            _score(engine, f"p{i:03d}")
        top = engine.top_n(3)
        assert len(top) == 3
        assert top[0].total_score >= top[1].total_score


# ── Analytics ─────────────────────────────────────────────────────────────────

class TestAnalytics:
    def test_average_score_empty(self, engine):
        assert engine.average_score() == 0.0

    def test_average_score(self, engine):
        c1 = _score(engine, "p001")
        c2 = _score(engine, "p002")
        expected = round((c1.total_score + c2.total_score) / 2, 1)
        assert engine.average_score() == expected

    def test_tier_distribution(self, engine):
        _score(engine, "p001")
        dist = engine.tier_distribution()
        for t in ["A", "B", "C", "D"]:
            assert t in dist

    def test_dimension_averages_keys(self, engine):
        _score(engine)
        avgs = engine.dimension_averages()
        assert set(avgs.keys()) == {"bant", "behavioral", "temporal", "market_fit"}

    def test_weakest_dimension(self, engine):
        engine.score("p001", "X", bant=_bant(0, 0, 0, 0),
                     behavioral=BehavioralDimension(True, True, True),
                     temporal=_temp(0),
                     market_fit=_fit())
        weak = engine.weakest_dimension()
        assert weak == "bant"

    def test_sector_breakdown(self, engine):
        _score(engine, "p001", sector="artisan")
        _score(engine, "p002", sector="artisan")
        _score(engine, "p003", sector="PME")
        breakdown = engine.sector_breakdown()
        assert breakdown["artisan"]["count"] == 2
        assert breakdown["PME"]["count"] == 1

    def test_summary_keys(self, engine):
        _score(engine)
        s = engine.summary()
        for k in ["total", "tier_A", "tier_B", "tier_C", "tier_D",
                  "avg_score", "weakest_dimension", "dimension_averages", "sector_breakdown"]:
            assert k in s


# ── Reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears(self, engine):
        _score(engine)
        engine.reset()
        assert len(engine.all_scorecards()) == 0

    def test_can_score_after_reset(self, engine):
        _score(engine)
        engine.reset()
        card = _score(engine)
        assert card is not None
