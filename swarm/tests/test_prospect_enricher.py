"""
Tests for intelligence/prospect_enricher.py
"""

import pytest
from intelligence.prospect_enricher import ProspectEnricher, EnrichedProspect


# ── Fixtures ──────────────────────────────────────────────────────────────────

def make_fiche(
    company_id: str = "co_001",
    name: str = "Plomberie Martin SARL",
    sector: str = "plombier artisan",
    pagespeed_score: int = 22,
    load_time_ms: int = 5200,
) -> dict:
    return {
        "company_id": company_id,
        "name": name,
        "sector": sector,
        "website": "http://plomberie-martin.fr",
        "contact_email": "contact@plomberie-martin.fr",
        "pagespeed_score": pagespeed_score,
        "load_time_ms": load_time_ms,
    }


def enricher() -> ProspectEnricher:
    return ProspectEnricher()


# ── enrich: output structure ──────────────────────────────────────────────────

class TestEnrichOutput:
    def test_returns_enriched_prospect(self):
        result = enricher().enrich(make_fiche())
        assert isinstance(result, EnrichedProspect)

    def test_company_id_preserved(self):
        result = enricher().enrich(make_fiche(company_id="xyz_99"))
        assert result.company_id == "xyz_99"

    def test_sector_preserved(self):
        result = enricher().enrich(make_fiche(sector="restaurant"))
        assert result.sector == "restaurant"

    def test_priority_score_in_range(self):
        result = enricher().enrich(make_fiche())
        assert 0 <= result.priority_score <= 100

    def test_icp_fit_in_range(self):
        result = enricher().enrich(make_fiche())
        assert 0.0 <= result.icp_fit <= 1.0

    def test_urgency_in_range(self):
        result = enricher().enrich(make_fiche())
        assert 0.0 <= result.urgency <= 1.0

    def test_tier_is_valid(self):
        result = enricher().enrich(make_fiche())
        assert result.tier in {"A", "B", "C"}

    def test_urgency_label_is_valid(self):
        result = enricher().enrich(make_fiche())
        assert result.urgency_label in {"critique", "mauvais", "moyen", "acceptable", "bon"}

    def test_company_size_is_valid(self):
        result = enricher().enrich(make_fiche())
        assert result.company_size in {"TPE", "PME", "ETI"}

    def test_enrichment_notes_is_list(self):
        result = enricher().enrich(make_fiche())
        assert isinstance(result.enrichment_notes, list)

    def test_to_dict_works(self):
        result = enricher().enrich(make_fiche())
        d = result.to_dict()
        assert isinstance(d, dict)
        assert "priority_score" in d
        assert "tier" in d


# ── ICP fit scoring ───────────────────────────────────────────────────────────

class TestICPScoring:
    def test_plumber_has_high_icp(self):
        result = enricher().enrich(make_fiche(sector="plombier"))
        assert result.icp_fit >= 0.85

    def test_restaurant_has_high_icp(self):
        result = enricher().enrich(make_fiche(sector="restaurant gastronomique"))
        assert result.icp_fit >= 0.90

    def test_doctor_has_high_icp(self):
        result = enricher().enrich(make_fiche(sector="médecin généraliste"))
        assert result.icp_fit >= 0.80

    def test_web_agency_has_low_icp(self):
        result = enricher().enrich(make_fiche(sector="agence web digitale"))
        assert result.icp_fit <= 0.20

    def test_unknown_sector_gets_neutral_icp(self):
        result = enricher().enrich(make_fiche(sector="fabrique de widgets inconnus"))
        assert 0.3 <= result.icp_fit <= 0.6

    def test_case_insensitive_sector_match(self):
        result_lower = enricher().enrich(make_fiche(sector="plombier"))
        result_upper = enricher().enrich(make_fiche(sector="PLOMBIER"))
        assert result_lower.icp_fit == result_upper.icp_fit


# ── PageSpeed urgency ─────────────────────────────────────────────────────────

class TestPageSpeedUrgency:
    def test_score_below_30_is_critique(self):
        result = enricher().enrich(make_fiche(pagespeed_score=15))
        assert result.urgency_label == "critique"
        assert result.urgency == 1.0

    def test_score_30_49_is_mauvais(self):
        result = enricher().enrich(make_fiche(pagespeed_score=40))
        assert result.urgency_label == "mauvais"
        assert result.urgency == 0.85

    def test_score_50_69_is_moyen(self):
        result = enricher().enrich(make_fiche(pagespeed_score=60))
        assert result.urgency_label == "moyen"

    def test_score_70_89_is_acceptable(self):
        result = enricher().enrich(make_fiche(pagespeed_score=80))
        assert result.urgency_label == "acceptable"

    def test_score_90_100_is_bon(self):
        result = enricher().enrich(make_fiche(pagespeed_score=95))
        assert result.urgency_label == "bon"
        assert result.urgency <= 0.1

    def test_critique_score_gives_higher_priority(self):
        bad = enricher().enrich(make_fiche(pagespeed_score=10))
        good = enricher().enrich(make_fiche(pagespeed_score=90, sector="plombier"))
        # Same sector, very different pagespeed — bad should score higher
        assert bad.priority_score > good.priority_score


# ── Company size detection ────────────────────────────────────────────────────

class TestCompanySize:
    def test_sarl_detected_as_pme(self):
        result = enricher().enrich(make_fiche(name="Martin SARL"))
        assert result.company_size == "PME"

    def test_eurl_detected_as_tpe(self):
        result = enricher().enrich(make_fiche(name="Durand EURL"))
        assert result.company_size == "TPE"

    def test_groupe_detected_as_eti(self):
        result = enricher().enrich(make_fiche(name="Groupe Bouygues"))
        assert result.company_size == "ETI"

    def test_unknown_defaults_to_pme(self):
        result = enricher().enrich(make_fiche(name="Boulangerie du Coin"))
        assert result.company_size == "PME"


# ── Tier assignment ───────────────────────────────────────────────────────────

class TestTierAssignment:
    def test_high_priority_is_tier_a(self):
        # Plumber + critical pagespeed → should be tier A
        result = enricher().enrich(make_fiche(sector="plombier", pagespeed_score=10))
        assert result.tier == "A"

    def test_very_low_priority_is_tier_c(self):
        result = enricher().enrich(make_fiche(sector="agence web", pagespeed_score=95))
        assert result.tier == "C"


# ── Revenue impact ────────────────────────────────────────────────────────────

class TestRevenueImpact:
    def test_slow_site_has_positive_impact(self):
        result = enricher().enrich(make_fiche(load_time_ms=6000))
        assert result.estimated_revenue_impact_eur > 0

    def test_fast_site_has_low_impact(self):
        fast = enricher().enrich(make_fiche(load_time_ms=800))
        slow = enricher().enrich(make_fiche(load_time_ms=8000))
        assert fast.estimated_revenue_impact_eur < slow.estimated_revenue_impact_eur


# ── enrich_batch ──────────────────────────────────────────────────────────────

class TestEnrichBatch:
    def test_returns_list(self):
        fiches = [make_fiche(company_id=f"c{i}") for i in range(5)]
        results = enricher().enrich_batch(fiches)
        assert isinstance(results, list)
        assert len(results) == 5

    def test_sorted_by_priority_desc(self):
        fiches = [
            make_fiche("hi", sector="plombier", pagespeed_score=10),
            make_fiche("lo", sector="agence web", pagespeed_score=90),
            make_fiche("mid", sector="restaurant", pagespeed_score=45),
        ]
        results = enricher().enrich_batch(fiches)
        scores = [r.priority_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_empty_batch_returns_empty(self):
        assert enricher().enrich_batch([]) == []


# ── filter_priority ───────────────────────────────────────────────────────────

class TestFilterPriority:
    def test_filters_below_threshold(self):
        fiches = [
            make_fiche("hi", sector="plombier", pagespeed_score=10),
            make_fiche("lo", sector="agence web", pagespeed_score=90),
        ]
        results = ProspectEnricher(min_priority_threshold=50).filter_priority(fiches)
        # Only the high-priority plumber should pass
        ids = [r.company_id for r in results]
        assert "hi" in ids
        assert "lo" not in ids

    def test_custom_threshold(self):
        fiches = [make_fiche(company_id=f"c{i}", pagespeed_score=20 + i * 10) for i in range(5)]
        # Low threshold should pass all
        results = enricher().filter_priority(fiches, min_score=0)
        assert len(results) == 5


# ── get_tier_a ────────────────────────────────────────────────────────────────

class TestGetTierA:
    def test_returns_only_tier_a(self):
        fiches = [
            make_fiche("a1", sector="plombier", pagespeed_score=10),
            make_fiche("c1", sector="agence web", pagespeed_score=90),
        ]
        results = enricher().get_tier_a(fiches)
        assert all(r.tier == "A" for r in results)

    def test_empty_when_no_tier_a(self):
        fiches = [make_fiche(sector="agence web", pagespeed_score=90)]
        results = enricher().get_tier_a(fiches)
        assert results == []


# ── Dataclass input ───────────────────────────────────────────────────────────

class TestDataclassInput:
    def test_accepts_dict_prospect(self):
        fiche = {
            "company_id": "dc_001",
            "name": "Test Company",
            "sector": "restaurant",
            "website": "http://test.fr",
            "pagespeed_score": 35,
            "mobile_responsive": False,
            "load_time_ms": 4000,
            "contact_email": "test@test.fr",
            "contact_name": "Le Directeur",
            "agent_source": "1.1",
            "detected_issues": [],
        }
        result = enricher().enrich(fiche)
        assert result.company_id == "dc_001"
        assert result.icp_fit >= 0.90
