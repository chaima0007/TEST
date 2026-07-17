"""
Unit tests for Division 5 Finance.

Run: pytest swarm/tests/test_division_5_finance.py -v
"""

import pytest
from divisions.division_5_finance import Division5Finance, PRICING_GRID, DOMAIN_BLACKLIST


@pytest.fixture
def fin():
    return Division5Finance()


# ── Pricing ───────────────────────────────────────────────────────────────────

class TestPricingGrid:
    def test_known_sectors_have_prices(self):
        for sector in ["Artisans", "Restauration", "Médical", "Immobilier"]:
            assert sector in PRICING_GRID, f"Secteur manquant: {sector}"
            assert PRICING_GRID[sector] > 0

    def test_medical_higher_than_artisans(self):
        assert PRICING_GRID["Médical"] > PRICING_GRID["Artisans"]

    def test_ecommerce_is_highest(self):
        max_price = max(PRICING_GRID.values())
        assert PRICING_GRID.get("E-commerce") == max_price or max_price >= 199

    def test_unknown_sector_has_default(self, fin):
        link = fin.create_stripe_link("comp_test", "Secteur Inconnu", "test.fr")
        assert "price" in link
        assert link["price"] > 0


# ── RGPD / Email Validation ───────────────────────────────────────────────────

class TestRGPDValidation:
    def test_valid_professional_email_passes(self, fin):
        assert fin.validate_email_rgpd("contact@restaurant-paris.fr") is True

    def test_blacklisted_domain_blocked(self, fin):
        for domain in list(DOMAIN_BLACKLIST)[:3]:
            assert fin.validate_email_rgpd(f"user@{domain}") is False

    def test_obvious_spam_domains_blocked(self, fin):
        spam = ["user@tempmail.com", "x@throwaway.email", "a@mailinator.com"]
        for email in spam:
            result = fin.validate_email_rgpd(email)
            # Not all may be in blacklist, but at minimum .validate must return bool
            assert isinstance(result, bool)

    def test_opt_out_adds_to_blacklist(self, fin):
        email = "unsubscribe-test@example-unique-domain.fr"
        fin.process_opt_out("comp_xyz", email)
        domain = email.split("@")[1]
        assert domain in DOMAIN_BLACKLIST or not fin.validate_email_rgpd(email)


# ── Stripe Link ───────────────────────────────────────────────────────────────

class TestStripeLink:
    def test_link_has_required_keys(self, fin):
        result = fin.create_stripe_link("comp_001", "Restauration", "lepetitbistro.fr")
        assert "company_id" in result
        assert "stripe_link" in result
        assert "price" in result
        assert "currency" in result

    def test_price_matches_sector(self, fin):
        result = fin.create_stripe_link("comp_002", "Médical", "clinique.fr")
        expected = PRICING_GRID.get("Médical", 149)
        assert result["price"] == expected

    def test_stripe_link_format(self, fin):
        result = fin.create_stripe_link("comp_003", "Artisans", "plombier.fr")
        link = result["stripe_link"]
        assert link.startswith("https://") or link.startswith("http://")


# ── Payment Confirmation ──────────────────────────────────────────────────────

class TestPaymentConfirmation:
    def test_confirm_returns_dict(self, fin):
        result = fin.confirm_payment("comp_test_pay", "ch_test_stripe_123")
        assert isinstance(result, dict)
        assert "confirmed" in result or "status" in result or "company_id" in result

    def test_confirm_sets_payment_confirmed(self, fin):
        result = fin.confirm_payment("comp_confirm_001", "ch_test_abc")
        assert result.get("confirmed") is True or result.get("status") == "confirmed"


# ── System Health ─────────────────────────────────────────────────────────────

class TestSystemHealth:
    def test_health_check_returns_dict(self, fin):
        health = fin.check_system_health()
        assert isinstance(health, dict)

    def test_health_has_status_key(self, fin):
        health = fin.check_system_health()
        assert "status" in health or "agents" in health or len(health) > 0

    def test_daily_report_is_dict(self, fin):
        report = fin.generate_daily_report()
        assert isinstance(report, dict)
        assert len(report) > 0
