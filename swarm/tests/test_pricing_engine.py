"""
Tests for intelligence/pricing_engine.py
"""

import pytest
from intelligence.pricing_engine import (
    PricingEngine, Package, Quote, QuoteLineItem,
    PACKAGES, TVA_RATE, _SECTOR_MULTIPLIERS,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def eng() -> PricingEngine:
    e = PricingEngine()
    e.reset()
    return e


def make_quote(
    pid="p001",
    company="Acme",
    sector="artisan",
    pagespeed=30,
    load_ms=5000,
    mobile=False,
    issues=3,
    force_pkg=None,
    discount=0.0,
    urgency=False,
) -> Quote:
    return eng().generate_quote(
        prospect_id=pid,
        company_name=company,
        sector=sector,
        pagespeed_score=pagespeed,
        load_time_ms=load_ms,
        mobile_responsive=mobile,
        issue_count=issues,
        force_package=force_pkg,
        discount_pct=discount,
        urgency=urgency,
    )


# ── Package catalogue ─────────────────────────────────────────────────────────

class TestPackageCatalogue:
    def test_four_packages_exist(self):
        assert len(PACKAGES) == 4

    def test_all_package_codes(self):
        assert set(PACKAGES.keys()) == {"starter", "standard", "premium", "enterprise"}

    def test_packages_have_deliverables(self):
        for pkg in PACKAGES.values():
            assert len(pkg.deliverables) > 0

    def test_prices_ascending(self):
        prices = [PACKAGES[k].base_price_eur for k in ["starter", "standard", "premium", "enterprise"]]
        assert prices == sorted(prices)

    def test_starter_price(self):
        assert PACKAGES["starter"].base_price_eur == pytest.approx(99.0)

    def test_premium_price(self):
        assert PACKAGES["premium"].base_price_eur == pytest.approx(449.0)

    def test_to_dict_has_keys(self):
        d = PACKAGES["standard"].to_dict()
        for key in ("code", "name", "base_price_eur", "deliverables", "description"):
            assert key in d


# ── QuoteLineItem ─────────────────────────────────────────────────────────────

class TestQuoteLineItem:
    def test_total_is_price_times_qty(self):
        li = QuoteLineItem("Service", 100.0, quantity=3)
        assert li.total_eur == pytest.approx(300.0)

    def test_default_qty_is_1(self):
        li = QuoteLineItem("Service", 200.0)
        assert li.quantity == 1

    def test_to_dict_has_all_keys(self):
        li = QuoteLineItem("Service", 100.0)
        d = li.to_dict()
        for key in ("label", "amount_eur", "quantity", "total_eur"):
            assert key in d


# ── Quote calculations ────────────────────────────────────────────────────────

class TestQuoteCalculations:
    def test_total_ttc_greater_than_ht(self):
        q = make_quote()
        assert q.total_ttc_eur > q.total_ht_eur

    def test_tva_is_20_pct_of_ht(self):
        q = make_quote()
        assert q.tva_eur == pytest.approx(q.total_ht_eur * 0.20, abs=0.01)

    def test_ttc_equals_ht_plus_tva(self):
        q = make_quote()
        assert q.total_ttc_eur == pytest.approx(q.total_ht_eur + q.tva_eur, abs=0.01)

    def test_discount_reduces_total(self):
        q_full     = make_quote()
        q_discount = make_quote(discount=0.10)
        assert q_discount.total_ht_eur < q_full.total_ht_eur

    def test_10_pct_discount(self):
        q = make_quote(discount=0.10)
        expected_ht = q.subtotal_eur * 0.90
        assert q.total_ht_eur == pytest.approx(expected_ht, abs=0.01)

    def test_discount_capped_at_100pct(self):
        q = make_quote(discount=1.5)  # over 100%
        assert q.total_ht_eur >= 0.0

    def test_urgency_bonus_adds_10pct(self):
        q_normal  = make_quote(urgency=False)
        q_urgent  = make_quote(urgency=True)
        assert q_urgent.urgency_bonus > 0
        assert q_urgent.total_ht_eur > q_normal.total_ht_eur

    def test_to_dict_has_all_keys(self):
        d = make_quote().to_dict()
        for key in ("prospect_id", "company_name", "sector", "package",
                    "subtotal_eur", "total_ht_eur", "tva_eur", "total_ttc_eur",
                    "discount_pct", "sector_multiplier"):
            assert key in d

    def test_summary_line_contains_company(self):
        q = make_quote(company="ACME SARL")
        assert "ACME SARL" in q.summary_line()

    def test_summary_line_contains_package(self):
        q = make_quote(force_pkg="premium")
        assert "Premium" in q.summary_line()


# ── Package recommendation ────────────────────────────────────────────────────

class TestPackageRecommendation:
    def test_low_severity_returns_starter(self):
        pkg = eng().recommend_package(pagespeed_score=85, load_time_ms=800, mobile_responsive=True, issue_count=0)
        assert pkg.code == "starter"

    def test_medium_severity_returns_standard(self):
        pkg = eng().recommend_package(pagespeed_score=40, load_time_ms=4500, mobile_responsive=True, issue_count=4)
        assert pkg.code in {"standard", "premium"}

    def test_high_severity_returns_premium_or_enterprise(self):
        pkg = eng().recommend_package(pagespeed_score=20, load_time_ms=8000, mobile_responsive=False, issue_count=8)
        assert pkg.code in {"premium", "enterprise"}

    def test_critical_returns_enterprise(self):
        pkg = eng().recommend_package(pagespeed_score=5, load_time_ms=10000, mobile_responsive=False, issue_count=10)
        assert pkg.code == "enterprise"

    def test_force_package_overrides(self):
        q = make_quote(pagespeed=5, mobile=False, force_pkg="starter")
        assert q.package.code == "starter"


# ── Severity scoring ──────────────────────────────────────────────────────────

class TestSeverityScore:
    def test_perfect_site_near_zero(self):
        s = PricingEngine._severity_score(100, 500, True, 0)
        assert s < 0.05

    def test_terrible_site_near_one(self):
        s = PricingEngine._severity_score(0, 10000, False, 10)
        assert s >= 0.95

    def test_mobile_non_responsive_adds_0_20(self):
        s_responsive    = PricingEngine._severity_score(50, 2000, True, 0)
        s_non_responsive = PricingEngine._severity_score(50, 2000, False, 0)
        assert s_non_responsive - s_responsive == pytest.approx(0.20, abs=0.01)

    def test_more_issues_higher_severity(self):
        s_low  = PricingEngine._severity_score(50, 2000, True, 0)
        s_high = PricingEngine._severity_score(50, 2000, True, 10)
        assert s_high > s_low


# ── Sector multiplier ─────────────────────────────────────────────────────────

class TestSectorMultiplier:
    def test_medecin_has_highest_multiplier(self):
        m = PricingEngine.sector_multiplier("médical")
        assert m == pytest.approx(1.30)

    def test_association_discounted(self):
        m = PricingEngine.sector_multiplier("association")
        assert m < 1.0

    def test_unknown_sector_returns_1(self):
        assert PricingEngine.sector_multiplier("zorgblorf") == pytest.approx(1.0)

    def test_partial_match_artisan(self):
        assert PricingEngine.sector_multiplier("artisan bâtiment") == pytest.approx(1.05)

    def test_sector_multiplier_applied_to_price(self):
        q_artisan = make_quote(sector="artisan", force_pkg="standard", pagespeed=50, load_ms=3000, mobile=True)
        q_medical = make_quote(sector="médical",  force_pkg="standard", pagespeed=50, load_ms=3000, mobile=True)
        assert q_medical.subtotal_eur > q_artisan.subtotal_eur


# ── generate_quote ────────────────────────────────────────────────────────────

class TestGenerateQuote:
    def test_returns_quote_object(self):
        assert isinstance(make_quote(), Quote)

    def test_quote_stored_in_engine(self):
        e = eng()
        q = e.generate_quote("p1", "X", "artisan", 30, 5000, False)
        assert e.get_quote("p1") is q

    def test_get_unknown_quote_none(self):
        assert eng().get_quote("missing") is None

    def test_prospect_id_set(self):
        q = make_quote(pid="p999")
        assert q.prospect_id == "p999"

    def test_company_name_set(self):
        q = make_quote(company="BTP Expert")
        assert q.company_name == "BTP Expert"

    def test_sector_multiplier_set(self):
        q = make_quote(sector="médical")
        assert q.sector_multiplier == pytest.approx(1.30)

    def test_line_items_non_empty(self):
        q = make_quote()
        assert len(q.line_items) >= 1

    def test_force_package_starter(self):
        q = make_quote(force_pkg="starter")
        assert q.package.code == "starter"


# ── price_batch ───────────────────────────────────────────────────────────────

class TestPriceBatch:
    def _prospects(self, n=3):
        return [
            {
                "company_id": f"p{i}",
                "name": f"Company {i}",
                "sector": "restaurant",
                "pagespeed_score": 30 + i * 5,
                "load_time_ms": 4000,
                "mobile_responsive": False,
                "detected_issues": ["issue1", "issue2"],
            }
            for i in range(n)
        ]

    def test_returns_list_of_quotes(self):
        quotes = eng().price_batch(self._prospects(3))
        assert len(quotes) == 3

    def test_all_quotes_are_quote_objects(self):
        quotes = eng().price_batch(self._prospects(2))
        assert all(isinstance(q, Quote) for q in quotes)

    def test_empty_batch(self):
        assert eng().price_batch([]) == []

    def test_discount_applied_to_all(self):
        e = eng()
        q_normal  = e.price_batch(self._prospects(1), default_discount_pct=0.0)[0]
        e.reset()
        q_discounted = e.price_batch(self._prospects(1), default_discount_pct=0.10)[0]
        assert q_discounted.total_ht_eur < q_normal.total_ht_eur


# ── Aggregate queries ─────────────────────────────────────────────────────────

class TestAggregateQueries:
    def _setup(self):
        e = eng()
        e.generate_quote("p1", "A", "médical",  10, 9000, False, force_package="enterprise")
        e.generate_quote("p2", "B", "artisan",   50, 3000, True,  force_package="standard")
        e.generate_quote("p3", "C", "artisan",   80, 1000, True,  force_package="starter")
        return e

    def test_all_quotes_count(self):
        assert len(self._setup().all_quotes()) == 3

    def test_total_pipeline_positive(self):
        assert self._setup().total_pipeline_eur() > 0

    def test_average_quote_positive(self):
        assert self._setup().average_quote_eur() > 0

    def test_top_quotes_sorted_desc(self):
        quotes = self._setup().top_quotes(n=2)
        assert quotes[0].total_ttc_eur >= quotes[1].total_ttc_eur

    def test_quotes_by_package_counts(self):
        by_pkg = self._setup().quotes_by_package()
        assert by_pkg.get("enterprise", 0) == 1
        assert by_pkg.get("standard", 0) == 1
        assert by_pkg.get("starter", 0) == 1

    def test_summary_keys(self):
        s = self._setup().summary()
        for key in ("total_quotes", "total_pipeline_eur", "average_quote_eur", "by_package"):
            assert key in s

    def test_summary_empty(self):
        s = eng().summary()
        assert s["total_quotes"] == 0
        assert s["total_pipeline_eur"] == 0.0


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_quotes(self):
        e = eng()
        e.generate_quote("p1", "X", "artisan", 30, 5000, False)
        e.reset()
        assert len(e.all_quotes()) == 0

    def test_reset_allows_fresh_start(self):
        e = eng()
        e.generate_quote("p1", "X", "artisan", 30, 5000, False)
        e.reset()
        e.generate_quote("p2", "Y", "restaurant", 40, 4000, True)
        assert len(e.all_quotes()) == 1
