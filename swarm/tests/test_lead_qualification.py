"""Tests for LeadQualificationEngine."""

import pytest
from swarm.intelligence.lead_qualification import (
    AuthorityLevel,
    BANTScore,
    LeadQualificationEngine,
    QualificationTier,
    Timeline,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture()
def eng():
    return LeadQualificationEngine()


def _hot_kwargs():
    return dict(
        budget_eur=1200.0, budget_confirmed=True,
        authority_level=AuthorityLevel.OWNER,
        need_severity=5, need_articulated=True,
        timeline=Timeline.IMMEDIATE,
    )


def _cold_kwargs():
    return dict(
        budget_eur=0.0, budget_confirmed=False,
        authority_level=AuthorityLevel.UNKNOWN,
        need_severity=1, need_articulated=False,
        timeline=Timeline.UNKNOWN,
    )


# ── BANTScore unit tests ──────────────────────────────────────────────────────

class TestBANTScore:
    def test_budget_zero_scores_zero(self):
        b = BANTScore(budget_eur=0, budget_confirmed=False)
        assert b.budget_pts == 0

    def test_budget_confirmed_full(self):
        b = BANTScore(budget_eur=1200, budget_confirmed=True)
        assert b.budget_pts == 25

    def test_budget_unconfirmed_halved(self):
        b = BANTScore(budget_eur=1200, budget_confirmed=False)
        assert b.budget_pts < 25
        assert b.budget_pts >= 1

    def test_authority_unknown_low(self):
        b = BANTScore(authority_level=AuthorityLevel.UNKNOWN)
        assert b.authority_pts == 5

    def test_authority_owner_max(self):
        b = BANTScore(authority_level=AuthorityLevel.OWNER)
        assert b.authority_pts == 25

    def test_need_severity_clamped_min(self):
        b = BANTScore(need_severity=0)
        assert b.need_pts >= 4

    def test_need_severity_clamped_max(self):
        b = BANTScore(need_severity=10)
        b2 = BANTScore(need_severity=5)
        assert b.need_pts == b2.need_pts

    def test_need_articulated_adds_5(self):
        b_no = BANTScore(need_severity=3, need_articulated=False)
        b_yes = BANTScore(need_severity=3, need_articulated=True)
        assert b_yes.need_pts == b_no.need_pts + 5

    def test_need_max_capped_25(self):
        b = BANTScore(need_severity=5, need_articulated=True)
        assert b.need_pts <= 25

    def test_timeline_immediate_max(self):
        b = BANTScore(timeline=Timeline.IMMEDIATE)
        assert b.timeline_pts == 25

    def test_timeline_unknown_low(self):
        b = BANTScore(timeline=Timeline.UNKNOWN)
        assert b.timeline_pts == 5

    def test_total_sum(self):
        b = BANTScore(
            budget_eur=1200, budget_confirmed=True,
            authority_level=AuthorityLevel.OWNER,
            need_severity=5, need_articulated=True,
            timeline=Timeline.IMMEDIATE,
        )
        assert b.total == b.budget_pts + b.authority_pts + b.need_pts + b.timeline_pts

    def test_tier_hot(self):
        b = BANTScore(**{
            "budget_eur": 1200, "budget_confirmed": True,
            "authority_level": AuthorityLevel.OWNER,
            "need_severity": 5, "need_articulated": True,
            "timeline": Timeline.IMMEDIATE,
        })
        assert b.tier == QualificationTier.HOT

    def test_tier_cold_all_min(self):
        b = BANTScore()
        assert b.tier == QualificationTier.COLD

    def test_to_dict_keys(self):
        b = BANTScore()
        d = b.to_dict()
        for key in ["budget_eur", "budget_confirmed", "authority_level", "need_severity",
                    "need_articulated", "timeline", "budget_pts", "authority_pts",
                    "need_pts", "timeline_pts", "total", "tier"]:
            assert key in d


# ── qualify ───────────────────────────────────────────────────────────────────

class TestQualify:
    def test_qualify_creates_record(self, eng):
        rec = eng.qualify("p001", "ACME", "artisan")
        assert rec is not None
        assert rec.prospect_id == "p001"
        assert rec.company_name == "ACME"
        assert rec.sector == "artisan"

    def test_qualify_stores_contact(self, eng):
        rec = eng.qualify("p001", "ACME", contact_name="Jean Dupont", contact_role="Gérant")
        assert rec.contact_name == "Jean Dupont"
        assert rec.contact_role == "Gérant"

    def test_qualify_hot_prospect(self, eng):
        rec = eng.qualify("p001", "A", **_hot_kwargs())
        assert rec.tier == QualificationTier.HOT
        assert rec.score >= 75

    def test_qualify_cold_prospect(self, eng):
        rec = eng.qualify("p001", "A", **_cold_kwargs())
        assert rec.tier == QualificationTier.COLD

    def test_qualify_overrides_existing(self, eng):
        eng.qualify("p001", "A", **_cold_kwargs())
        eng.qualify("p001", "A", **_hot_kwargs())
        rec = eng.get("p001")
        assert rec.tier == QualificationTier.HOT

    def test_ids_unique(self, eng):
        r1 = eng.qualify("p001", "A")
        r2 = eng.qualify("p002", "B")
        assert r1.record_id != r2.record_id

    def test_notes_stored(self, eng):
        rec = eng.qualify("p001", "A", notes="Rappel demain")
        assert rec.notes == "Rappel demain"


# ── update ────────────────────────────────────────────────────────────────────

class TestUpdate:
    def test_update_budget(self, eng):
        eng.qualify("p001", "A")
        rec = eng.update("p001", budget_eur=1200, budget_confirmed=True)
        assert rec.bant.budget_eur == 1200
        assert rec.bant.budget_confirmed is True

    def test_update_authority(self, eng):
        eng.qualify("p001", "A")
        eng.update("p001", authority_level=AuthorityLevel.DIRECTOR)
        assert eng.get("p001").bant.authority_level == AuthorityLevel.DIRECTOR

    def test_update_timeline(self, eng):
        eng.qualify("p001", "A")
        eng.update("p001", timeline=Timeline.IMMEDIATE)
        assert eng.get("p001").bant.timeline == Timeline.IMMEDIATE

    def test_update_notes(self, eng):
        eng.qualify("p001", "A")
        eng.update("p001", notes="Nouveau note")
        assert eng.get("p001").notes == "Nouveau note"

    def test_update_missing_returns_none(self, eng):
        assert eng.update("p999") is None

    def test_update_need_severity_clamped(self, eng):
        eng.qualify("p001", "A")
        eng.update("p001", need_severity=10)
        assert eng.get("p001").bant.need_severity == 5

    def test_update_improves_score(self, eng):
        rec = eng.qualify("p001", "A", **_cold_kwargs())
        low = rec.score
        eng.update("p001", **_hot_kwargs())
        assert eng.get("p001").score > low


# ── get / all_records ─────────────────────────────────────────────────────────

class TestGet:
    def test_get_existing(self, eng):
        rec = eng.qualify("p001", "A")
        assert eng.get("p001") is rec

    def test_get_missing(self, eng):
        assert eng.get("p999") is None

    def test_get_or_qualify_existing(self, eng):
        rec = eng.qualify("p001", "A", **_hot_kwargs())
        rec2 = eng.get_or_qualify("p001", "A")
        assert rec2 is rec

    def test_get_or_qualify_new(self, eng):
        rec = eng.get_or_qualify("p001", "A", "artisan")
        assert rec is not None
        assert eng.get("p001") is rec

    def test_all_records(self, eng):
        eng.qualify("p001", "A")
        eng.qualify("p002", "B")
        assert len(eng.all_records()) == 2


# ── Queries ───────────────────────────────────────────────────────────────────

class TestQueries:
    def test_by_tier_hot(self, eng):
        r1 = eng.qualify("p001", "A", **_hot_kwargs())
        r2 = eng.qualify("p002", "B", **_cold_kwargs())
        hot = eng.hot()
        assert r1 in hot and r2 not in hot

    def test_by_tier_warm(self, eng):
        rec = eng.qualify("p001", "A",
            budget_eur=600, budget_confirmed=True,
            authority_level=AuthorityLevel.DIRECTOR,
            need_severity=3, need_articulated=True,
            timeline=Timeline.THIS_QUARTER,
        )
        assert rec.tier == QualificationTier.WARM
        assert rec in eng.warm()

    def test_by_sector(self, eng):
        eng.qualify("p001", "A", sector="artisan")
        eng.qualify("p002", "B", sector="juridique")
        eng.qualify("p003", "C", sector="artisan spécialisé")
        results = eng.by_sector("artisan")
        assert len(results) == 2

    def test_top_n(self, eng):
        eng.qualify("p001", "A", **_hot_kwargs())
        eng.qualify("p002", "B", **_cold_kwargs())
        top = eng.top_n(1)
        assert len(top) == 1
        assert top[0].prospect_id == "p001"

    def test_top_n_respects_limit(self, eng):
        for i in range(5):
            eng.qualify(f"p{i:03d}", f"C{i}")
        assert len(eng.top_n(3)) == 3


# ── Analytics ─────────────────────────────────────────────────────────────────

class TestAnalytics:
    def test_tier_distribution_all_zero(self, eng):
        dist = eng.tier_distribution()
        assert all(v == 0 for v in dist.values())

    def test_tier_distribution_counts(self, eng):
        eng.qualify("p001", "A", **_hot_kwargs())
        eng.qualify("p002", "B", **_cold_kwargs())
        dist = eng.tier_distribution()
        assert dist["hot"] == 1
        assert dist["cold"] == 1

    def test_average_score_zero_empty(self, eng):
        assert eng.average_score() == 0.0

    def test_average_score(self, eng):
        r1 = eng.qualify("p001", "A", **_hot_kwargs())
        r2 = eng.qualify("p002", "B", **_cold_kwargs())
        expected = round((r1.score + r2.score) / 2, 1)
        assert eng.average_score() == expected

    def test_average_score_by_sector(self, eng):
        eng.qualify("p001", "A", sector="artisan", **_hot_kwargs())
        eng.qualify("p002", "B", sector="artisan", **_cold_kwargs())
        result = eng.average_score_by_sector()
        assert "artisan" in result

    def test_weakest_dimension_returns_string(self, eng):
        eng.qualify("p001", "A", **_cold_kwargs())
        wd = eng.weakest_dimension()
        assert wd in ("budget", "authority", "need", "timeline")

    def test_weakest_dimension_unknown_when_empty(self, eng):
        assert eng.weakest_dimension() == "unknown"

    def test_dimension_averages_keys(self, eng):
        eng.qualify("p001", "A")
        avgs = eng.dimension_averages()
        assert set(avgs.keys()) == {"budget", "authority", "need", "timeline"}

    def test_dimension_averages_empty(self, eng):
        avgs = eng.dimension_averages()
        assert all(v == 0.0 for v in avgs.values())


# ── summary() ─────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary(self, eng):
        s = eng.summary()
        assert s["total"] == 0
        assert s["avg_score"] == 0.0

    def test_summary_keys(self, eng):
        s = eng.summary()
        for k in ["total", "tier_hot", "tier_warm", "tier_cool", "tier_cold",
                  "avg_score", "weakest_bant", "dimension_avgs"]:
            assert k in s

    def test_summary_counts(self, eng):
        eng.qualify("p001", "A", **_hot_kwargs())
        eng.qualify("p002", "B", **_cold_kwargs())
        s = eng.summary()
        assert s["total"] == 2
        assert s["tier_hot"] == 1
        assert s["tier_cold"] == 1


# ── to_dict ───────────────────────────────────────────────────────────────────

class TestToDict:
    def test_record_to_dict(self, eng):
        rec = eng.qualify("p001", "ACME", "tech",
            contact_name="Paul", contact_role="CEO",
            **_hot_kwargs(),
        )
        d = rec.to_dict()
        assert d["prospect_id"] == "p001"
        assert d["company_name"] == "ACME"
        assert d["contact_name"] == "Paul"
        assert "bant" in d
        assert d["bant"]["tier"] == "hot"


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears(self, eng):
        eng.qualify("p001", "A")
        eng.reset()
        assert len(eng.all_records()) == 0

    def test_reset_counter(self, eng):
        eng.qualify("p001", "A")
        eng.reset()
        rec = eng.qualify("p001", "A")
        assert rec.record_id == "qual_00001"
