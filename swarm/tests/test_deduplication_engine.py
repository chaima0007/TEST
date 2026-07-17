"""
Tests for intelligence/deduplication_engine.py
"""

import datetime
import pytest
from intelligence.deduplication_engine import (
    DeduplicationEngine, ContactRecord, SuppressionEntry,
    DeduplicationResult, SuppressionReason,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def eng() -> DeduplicationEngine:
    e = DeduplicationEngine()
    e.reset()
    return e


NOW = datetime.datetime(2026, 1, 10, 10, 0, 0)
PAST_30 = NOW - datetime.timedelta(days=30)
PAST_10 = NOW - datetime.timedelta(days=10)
PAST_5  = NOW - datetime.timedelta(days=5)


# ── Normalisation helpers ─────────────────────────────────────────────────────

class TestNormalisation:
    def test_normalize_email_lowercases(self):
        assert DeduplicationEngine._normalize_email("Test@Example.COM") == "test@example.com"

    def test_normalize_email_strips_spaces(self):
        assert DeduplicationEngine._normalize_email("  foo@bar.fr  ") == "foo@bar.fr"

    def test_extract_domain(self):
        assert DeduplicationEngine._extract_domain("user@acme.fr") == "acme.fr"

    def test_extract_domain_no_at(self):
        assert DeduplicationEngine._extract_domain("acme.fr") == "acme.fr"

    def test_normalize_phone_strips_non_digits(self):
        phone = DeduplicationEngine._normalize_phone("+33 6 12 34 56 78")
        assert phone.isdigit()

    def test_normalize_phone_french_33_prefix(self):
        phone = DeduplicationEngine._normalize_phone("33612345678")
        assert phone.startswith("06")

    def test_fingerprint_is_deterministic(self):
        a = DeduplicationEngine._fingerprint("Acme SARL", "Paris")
        b = DeduplicationEngine._fingerprint("Acme SARL", "Paris")
        assert a == b

    def test_fingerprint_case_insensitive(self):
        a = DeduplicationEngine._fingerprint("ACME SARL", "PARIS")
        b = DeduplicationEngine._fingerprint("acme sarl", "paris")
        assert a == b

    def test_fingerprint_different_companies(self):
        a = DeduplicationEngine._fingerprint("Acme", "Paris")
        b = DeduplicationEngine._fingerprint("Beta Corp", "Lyon")
        assert a != b


# ── ContactRecord ─────────────────────────────────────────────────────────────

class TestContactRecord:
    def test_in_cooldown_when_recent(self):
        rec = ContactRecord("x@x.fr", "email", PAST_5)
        assert rec.is_in_cooldown(30, NOW) is True

    def test_not_in_cooldown_when_expired(self):
        rec = ContactRecord("x@x.fr", "email", PAST_30)
        assert rec.is_in_cooldown(30, NOW) is False

    def test_to_dict_has_all_keys(self):
        rec = ContactRecord("x@x.fr", "email", NOW, contact_count=3)
        d = rec.to_dict()
        for key in ("key", "key_type", "last_contacted", "contact_count", "agent_id", "sector"):
            assert key in d


# ── SuppressionEntry ──────────────────────────────────────────────────────────

class TestSuppressionEntry:
    def test_to_dict_has_required_keys(self):
        e = SuppressionEntry("x@x.fr", "email", SuppressionReason.OPT_OUT)
        d = e.to_dict()
        for key in ("key", "key_type", "reason", "added_at"):
            assert key in d

    def test_reason_value_is_string(self):
        e = SuppressionEntry("x@x.fr", "email", SuppressionReason.BOUNCE)
        assert e.to_dict()["reason"] == "bounce"


# ── DeduplicationResult ───────────────────────────────────────────────────────

class TestDeduplicationResult:
    def test_to_dict_keys(self):
        r = DeduplicationResult(True, "ok")
        d = r.to_dict()
        for key in ("allowed", "reason", "matching_key", "cooldown_remaining_days"):
            assert key in d

    def test_allowed_true(self):
        assert DeduplicationResult(True, "ok").allowed is True

    def test_allowed_false_suppressed(self):
        assert DeduplicationResult(False, "suppressed", "x@x.fr").allowed is False


# ── check() — new contact allowed ────────────────────────────────────────────

class TestCheckAllowed:
    def test_new_email_allowed(self):
        result = eng().check("new@prospect.fr", as_of=NOW)
        assert result.allowed is True

    def test_reason_ok_when_allowed(self):
        result = eng().check("new@prospect.fr", as_of=NOW)
        assert result.reason == "ok"

    def test_after_cooldown_expired_allowed(self):
        e = eng()
        e.record_contact("old@prospect.fr", as_of=PAST_30)
        result = e.check("old@prospect.fr", as_of=NOW)
        assert result.allowed is True


# ── check() — cooldown ────────────────────────────────────────────────────────

class TestCheckCooldown:
    def test_recently_contacted_email_blocked(self):
        e = eng()
        e.record_contact("recent@prospect.fr", as_of=PAST_5)
        result = e.check("recent@prospect.fr", as_of=NOW)
        assert result.allowed is False
        assert result.reason == "cooldown"

    def test_cooldown_matching_key_is_email(self):
        e = eng()
        e.record_contact("recent@prospect.fr", as_of=PAST_5)
        result = e.check("recent@prospect.fr", as_of=NOW)
        assert result.matching_key == "recent@prospect.fr"

    def test_cooldown_remaining_positive(self):
        e = eng()
        e.record_contact("recent@prospect.fr", as_of=PAST_5)
        result = e.check("recent@prospect.fr", as_of=NOW)
        assert result.cooldown_remaining_days > 0

    def test_domain_cooldown_blocks_different_email(self):
        e = eng()
        e.record_contact("alice@acme.fr", as_of=PAST_5)
        result = e.check("bob@acme.fr", as_of=NOW)
        assert result.allowed is False
        assert result.reason == "cooldown"

    def test_domain_cooldown_uses_domain_window(self):
        # domain cooldown = 14 days; contact was 10 days ago → blocked
        e = eng()
        e.record_contact("alice@acme.fr", as_of=PAST_10)
        result = e.check("bob@acme.fr", as_of=NOW)
        assert result.allowed is False

    def test_domain_expired_after_14_days(self):
        # domain cooldown = 14 days; contact was 15 days ago → allowed
        e = eng()
        past_15 = NOW - datetime.timedelta(days=15)
        e.record_contact("alice@acme.fr", as_of=past_15)
        result = e.check("bob@acme.fr", as_of=NOW)
        assert result.allowed is True

    def test_custom_cooldown_respected(self):
        e = DeduplicationEngine(cooldown_days={"email": 60})
        e.record_contact("x@x.fr", as_of=PAST_30)
        result = e.check("x@x.fr", as_of=NOW)
        assert result.allowed is False  # 30 days < 60 day cooldown


# ── check() — suppression ─────────────────────────────────────────────────────

class TestCheckSuppression:
    def test_suppressed_email_blocked(self):
        e = eng()
        e.suppress("opt@out.fr", key_type="email", reason=SuppressionReason.OPT_OUT)
        result = e.check("opt@out.fr", as_of=NOW)
        assert result.allowed is False
        assert result.reason == "suppressed"

    def test_suppressed_domain_blocks_all(self):
        e = eng()
        e.suppress("spammy.fr", key_type="domain", reason=SuppressionReason.SPAM)
        result = e.check("any@spammy.fr", as_of=NOW)
        assert result.allowed is False

    def test_suppression_overrides_expired_cooldown(self):
        e = eng()
        e.record_contact("old@acme.fr", as_of=PAST_30)
        e.suppress("old@acme.fr", key_type="email", reason=SuppressionReason.OPT_OUT)
        result = e.check("old@acme.fr", as_of=NOW)
        assert result.allowed is False
        assert result.reason == "suppressed"


# ── check() — duplicate fingerprint ──────────────────────────────────────────

class TestCheckDuplicate:
    def test_same_company_city_blocked_after_contact(self):
        e = eng()
        e.record_contact("contact@acme.fr", company_name="Acme SARL", city="Paris", as_of=PAST_30)
        # Cooldown expired but fingerprint still registered
        result = e.check("autre@acme.fr", company_name="Acme SARL", city="Paris", as_of=NOW)
        assert result.reason == "duplicate"

    def test_different_company_same_city_allowed(self):
        e = eng()
        e.record_contact("a@x.fr", company_name="Acme", city="Paris", as_of=PAST_30)
        result = e.check("b@y.fr", company_name="Beta Corp", city="Paris", as_of=NOW)
        assert result.allowed is True


# ── record_contact ────────────────────────────────────────────────────────────

class TestRecordContact:
    def test_contact_logged(self):
        e = eng()
        e.record_contact("x@x.fr", as_of=NOW)
        assert e.get_contact("x@x.fr") is not None

    def test_contact_count_increments(self):
        e = eng()
        e.record_contact("x@x.fr", as_of=PAST_5)
        e.record_contact("x@x.fr", as_of=NOW)
        rec = e.get_contact("x@x.fr")
        assert rec.contact_count == 2

    def test_last_contacted_updated(self):
        e = eng()
        e.record_contact("x@x.fr", as_of=PAST_5)
        e.record_contact("x@x.fr", as_of=NOW)
        rec = e.get_contact("x@x.fr")
        assert rec.last_contacted == NOW

    def test_domain_also_recorded(self):
        e = eng()
        e.record_contact("user@acme.fr", as_of=NOW)
        assert "acme.fr" in e._contacts

    def test_fingerprint_recorded(self):
        e = eng()
        e.record_contact("x@x.fr", company_name="Acme", city="Lyon", as_of=NOW)
        fp = DeduplicationEngine._fingerprint("Acme", "Lyon")
        assert fp in e._fingerprints

    def test_phone_recorded(self):
        e = eng()
        e.record_contact("x@x.fr", phone="0612345678", as_of=NOW)
        assert "0612345678" in e._contacts


# ── suppress / unsuppress / is_suppressed ────────────────────────────────────

class TestSuppression:
    def test_suppress_adds_to_list(self):
        e = eng()
        e.suppress("bad@mail.fr")
        assert e.is_suppressed("bad@mail.fr")

    def test_unsuppress_removes(self):
        e = eng()
        e.suppress("bad@mail.fr")
        result = e.unsuppress("bad@mail.fr")
        assert result is True
        assert not e.is_suppressed("bad@mail.fr")

    def test_unsuppress_unknown_returns_false(self):
        assert eng().unsuppress("unknown@key.fr") is False

    def test_suppression_reason_stored(self):
        e = eng()
        e.suppress("b@b.fr", reason=SuppressionReason.BOUNCE)
        entry = e._suppressed["b@b.fr"]
        assert entry.reason == SuppressionReason.BOUNCE

    def test_suppress_domain(self):
        e = eng()
        e.suppress("competitor.fr", key_type="domain", reason=SuppressionReason.COMPETITOR)
        assert e.is_suppressed("competitor.fr")

    def test_suppression_count(self):
        e = eng()
        e.suppress("a@a.fr")
        e.suppress("b@b.fr")
        assert e.suppression_count() == 2

    def test_list_suppressed(self):
        e = eng()
        e.suppress("a@a.fr")
        entries = e.list_suppressed()
        assert len(entries) == 1
        assert isinstance(entries[0], SuppressionEntry)


# ── filter_batch ──────────────────────────────────────────────────────────────

class TestFilterBatch:
    def _prospects(self, n=3):
        return [
            {"email": f"contact{i}@company{i}.fr", "company_name": f"Company {i}", "city": "Paris"}
            for i in range(n)
        ]

    def test_all_new_prospects_allowed(self):
        e = eng()
        allowed, blocked = e.filter_batch(self._prospects(3), as_of=NOW)
        assert len(allowed) == 3
        assert len(blocked) == 0

    def test_suppressed_prospect_blocked(self):
        e = eng()
        e.suppress("contact0@company0.fr")
        allowed, blocked = e.filter_batch(self._prospects(3), as_of=NOW)
        assert len(allowed) == 2
        assert len(blocked) == 1

    def test_cooled_down_prospect_blocked(self):
        e = eng()
        e.record_contact("contact0@company0.fr", as_of=PAST_5)
        allowed, blocked = e.filter_batch(self._prospects(3), as_of=NOW)
        assert len(allowed) == 2
        assert len(blocked) == 1

    def test_block_reason_in_blocked(self):
        e = eng()
        e.suppress("contact0@company0.fr")
        _, blocked = e.filter_batch(self._prospects(3), as_of=NOW)
        assert "_block_reason" in blocked[0]

    def test_intra_batch_duplicate_blocked(self):
        e = eng()
        prospects = [
            {"email": "a@acme.fr",  "company_name": "Acme", "city": "Paris"},
            {"email": "b@acme2.fr", "company_name": "Acme", "city": "Paris"},  # same company
        ]
        allowed, blocked = e.filter_batch(prospects, as_of=NOW)
        assert len(allowed) == 1
        assert len(blocked) == 1
        assert blocked[0]["_block_reason"] == "duplicate"

    def test_empty_batch(self):
        allowed, blocked = eng().filter_batch([], as_of=NOW)
        assert allowed == []
        assert blocked == []


# ── export / import suppression ───────────────────────────────────────────────

class TestExportImport:
    def test_export_returns_list_of_dicts(self):
        e = eng()
        e.suppress("a@a.fr")
        data = e.export_suppression_list()
        assert isinstance(data, list)
        assert len(data) == 1
        assert isinstance(data[0], dict)

    def test_import_populates_suppressed(self):
        e = eng()
        entries = [{"key": "x@x.fr", "key_type": "email", "reason": "opt_out", "note": ""}]
        count = e.import_suppression_list(entries)
        assert count == 1
        assert e.is_suppressed("x@x.fr")

    def test_import_unknown_reason_defaults_to_manual(self):
        e = eng()
        entries = [{"key": "y@y.fr", "key_type": "email", "reason": "alien_invasion"}]
        e.import_suppression_list(entries)
        assert e.is_suppressed("y@y.fr")

    def test_round_trip_export_import(self):
        e1 = eng()
        e1.suppress("a@a.fr", reason=SuppressionReason.BOUNCE)
        e1.suppress("b.fr", key_type="domain", reason=SuppressionReason.SPAM)
        data = e1.export_suppression_list()

        e2 = eng()
        e2.import_suppression_list(data)
        assert e2.is_suppressed("a@a.fr")
        assert e2.is_suppressed("b.fr")


# ── summary ───────────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_keys(self):
        s = eng().summary()
        for key in ("unique_emails_contacted", "unique_domains_contacted",
                    "suppression_list_size", "fingerprints_seen", "total_contact_events"):
            assert key in s

    def test_summary_empty(self):
        s = eng().summary()
        assert s["unique_emails_contacted"] == 0
        assert s["suppression_list_size"] == 0

    def test_summary_after_contacts(self):
        e = eng()
        e.record_contact("a@x.fr", as_of=NOW)
        e.record_contact("b@y.fr", as_of=NOW)
        s = e.summary()
        assert s["unique_emails_contacted"] == 2
        assert s["unique_domains_contacted"] == 2

    def test_summary_suppression_count(self):
        e = eng()
        e.suppress("z@z.fr")
        assert e.summary()["suppression_list_size"] == 1


# ── reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_contacts(self):
        e = eng()
        e.record_contact("a@a.fr", as_of=NOW)
        e.reset()
        assert e.contact_count() == 0

    def test_reset_clears_suppressed_by_default(self):
        e = eng()
        e.suppress("a@a.fr")
        e.reset()
        assert not e.is_suppressed("a@a.fr")

    def test_reset_keep_suppressed(self):
        e = eng()
        e.suppress("a@a.fr")
        e.reset(keep_suppressed=True)
        assert e.is_suppressed("a@a.fr")

    def test_reset_clears_fingerprints(self):
        e = eng()
        e.record_contact("x@x.fr", company_name="Acme", city="Paris", as_of=NOW)
        e.reset()
        assert len(e._fingerprints) == 0
