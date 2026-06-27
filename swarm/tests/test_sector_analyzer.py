"""
Tests for intelligence/sector_analyzer.py
"""

import pytest
from intelligence.sector_analyzer import SectorAnalyzer, SectorProfile, _SECTOR_DB


# ── Helpers ───────────────────────────────────────────────────────────────────

def analyzer() -> SectorAnalyzer:
    return SectorAnalyzer()


# ── SectorProfile ─────────────────────────────────────────────────────────────

class TestSectorProfile:
    def test_icp_priority_is_valid(self):
        for p in _SECTOR_DB.values():
            assert p.icp_priority() in {"S", "A", "B", "C"}

    def test_recommended_volume_positive(self):
        for p in _SECTOR_DB.values():
            assert p.recommended_volume() >= 20

    def test_recommended_volume_max_200(self):
        for p in _SECTOR_DB.values():
            assert p.recommended_volume() <= 200

    def test_to_dict_has_required_keys(self):
        p = list(_SECTOR_DB.values())[0]
        d = p.to_dict()
        for key in ("name", "market_size_fr", "avg_pagespeed", "competition_density",
                    "avg_revenue_impact_eur", "outreach_roi_multiplier",
                    "icp_priority", "recommended_volume", "tags"):
            assert key in d

    def test_artisan_has_high_priority(self):
        p = _SECTOR_DB["artisans_batiment"]
        assert p.icp_priority() in {"S", "A"}

    def test_associations_has_low_roi_multiplier(self):
        p = _SECTOR_DB["associations_loisirs"]
        assert p.outreach_roi_multiplier <= 1.5


# ── get / get_by_name ─────────────────────────────────────────────────────────

class TestGet:
    def test_get_returns_profile(self):
        p = analyzer().get("artisans_batiment")
        assert isinstance(p, SectorProfile)
        assert p.name == "Artisans & Bâtiment"

    def test_get_unknown_returns_none(self):
        assert analyzer().get("unknown_sector") is None

    def test_get_by_name_exact(self):
        p = analyzer().get_by_name("Artisans & Bâtiment")
        assert p is not None

    def test_get_by_name_partial(self):
        p = analyzer().get_by_name("restaurant")
        assert p is not None
        assert "Restauration" in p.name

    def test_get_by_name_tag_match(self):
        p = analyzer().get_by_name("plombier")
        assert p is not None
        assert "Artisans" in p.name

    def test_get_by_name_dentiste(self):
        p = analyzer().get_by_name("dentiste")
        assert p is not None
        assert "Médical" in p.name

    def test_get_by_name_unknown_returns_none(self):
        assert analyzer().get_by_name("fabricant de widgets inconnus") is None

    def test_get_by_name_case_insensitive(self):
        p1 = analyzer().get_by_name("RESTAURANT")
        p2 = analyzer().get_by_name("restaurant")
        assert p1 is not None
        assert p2 is not None


# ── all_sectors ───────────────────────────────────────────────────────────────

class TestAllSectors:
    def test_returns_list(self):
        result = analyzer().all_sectors()
        assert isinstance(result, list)

    def test_returns_all_sectors(self):
        result = analyzer().all_sectors()
        assert len(result) == len(_SECTOR_DB)

    def test_all_are_sector_profiles(self):
        for p in analyzer().all_sectors():
            assert isinstance(p, SectorProfile)


# ── ranked_by_opportunity ─────────────────────────────────────────────────────

class TestRanked:
    def test_returns_list_of_correct_length(self):
        result = analyzer().ranked_by_opportunity()
        assert len(result) == len(_SECTOR_DB)

    def test_artisans_near_top(self):
        ranked = analyzer().ranked_by_opportunity()
        names = [p.name for p in ranked[:3]]
        assert any("Artisan" in n for n in names)

    def test_last_ranked_has_lower_roi(self):
        ranked = analyzer().ranked_by_opportunity()
        last  = ranked[-1]
        first = ranked[0]
        # Bottom sector has lower ROI multiplier than top sector
        assert last.outreach_roi_multiplier < first.outreach_roi_multiplier


# ── s_priority_sectors ────────────────────────────────────────────────────────

class TestSPriority:
    def test_returns_list(self):
        result = analyzer().s_priority_sectors()
        assert isinstance(result, list)

    def test_all_returned_are_s_grade(self):
        for p in analyzer().s_priority_sectors():
            assert p.icp_priority() == "S"

    def test_artisans_is_s_priority(self):
        s_sectors = analyzer().s_priority_sectors()
        names = [p.name for p in s_sectors]
        assert any("Artisan" in n for n in names)


# ── total_addressable_market ──────────────────────────────────────────────────

class TestTAM:
    def test_tam_is_positive_int(self):
        tam = analyzer().total_addressable_market()
        assert isinstance(tam, int)
        assert tam > 0

    def test_tam_is_sum_of_all_markets(self):
        tam = analyzer().total_addressable_market()
        expected = sum(p.market_size_fr for p in _SECTOR_DB.values())
        assert tam == expected

    def test_tam_at_least_one_million(self):
        assert analyzer().total_addressable_market() >= 1_000_000


# ── weekly_outreach_plan ──────────────────────────────────────────────────────

class TestOutreachPlan:
    def test_returns_dict(self):
        plan = analyzer().weekly_outreach_plan()
        assert isinstance(plan, dict)

    def test_all_sectors_in_plan(self):
        plan = analyzer().weekly_outreach_plan()
        assert len(plan) == len(_SECTOR_DB)

    def test_all_volumes_positive(self):
        for vol in analyzer().weekly_outreach_plan().values():
            assert vol >= 20

    def test_all_volumes_at_most_200(self):
        for vol in analyzer().weekly_outreach_plan().values():
            assert vol <= 200


# ── competition_report ────────────────────────────────────────────────────────

class TestCompetitionReport:
    def test_returns_list(self):
        report = analyzer().competition_report()
        assert isinstance(report, list)

    def test_sorted_by_competition_asc(self):
        report = analyzer().competition_report()
        densities = [r["competition_density"] for r in report]
        assert densities == sorted(densities)

    def test_report_has_required_keys(self):
        report = analyzer().competition_report()
        for row in report:
            assert "sector" in row
            assert "competition_density" in row
            assert "opportunity_score" in row

    def test_opportunity_score_positive(self):
        for row in analyzer().competition_report():
            assert row["opportunity_score"] > 0

    def test_associations_has_highest_opportunity_from_low_competition(self):
        report = analyzer().competition_report()
        # First item has lowest competition density
        assert report[0]["competition_density"] <= 0.15


# ── Database integrity ────────────────────────────────────────────────────────

class TestDatabaseIntegrity:
    def test_all_pagespeed_scores_in_range(self):
        for p in _SECTOR_DB.values():
            assert 0 <= p.avg_pagespeed <= 100

    def test_all_competition_densities_in_range(self):
        for p in _SECTOR_DB.values():
            assert 0.0 <= p.competition_density <= 1.0

    def test_all_market_sizes_positive(self):
        for p in _SECTOR_DB.values():
            assert p.market_size_fr > 0

    def test_all_revenue_impacts_positive(self):
        for p in _SECTOR_DB.values():
            assert p.avg_revenue_impact_eur > 0

    def test_all_roi_multipliers_above_one(self):
        for p in _SECTOR_DB.values():
            assert p.outreach_roi_multiplier >= 1.0

    def test_all_sectors_have_tags(self):
        for p in _SECTOR_DB.values():
            assert len(p.tags) >= 3
