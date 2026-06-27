"""
Tests for exporters/email_sender.py — RGPD compliance and send logic.
"""

import pytest
from unittest.mock import patch, MagicMock, call
from exporters.email_sender import EmailSender, SendResult, _ALWAYS_BLOCKED


# ── Fixtures ──────────────────────────────────────────────────────────────────

def make_sender(**kwargs) -> EmailSender:
    """Create a dry-run (no SMTP_HOST) sender by default."""
    return EmailSender(rate_limit_per_minute=600, **kwargs)


# ── RGPD / blacklist ──────────────────────────────────────────────────────────

class TestRGPDCheck:
    def test_professional_email_is_allowed(self):
        s = make_sender()
        blocked, _ = s.is_rgpd_blocked("contact@plomberie-martin.fr")
        assert not blocked

    def test_gmail_is_always_blocked(self):
        s = make_sender()
        blocked, reason = s.is_rgpd_blocked("john.doe@gmail.com")
        assert blocked
        assert "gmail.com" in reason

    def test_hotmail_is_always_blocked(self):
        s = make_sender()
        blocked, _ = s.is_rgpd_blocked("user@hotmail.com")
        assert blocked

    def test_orange_fr_is_always_blocked(self):
        s = make_sender()
        blocked, _ = s.is_rgpd_blocked("client@orange.fr")
        assert blocked

    def test_invalid_email_no_at_sign(self):
        s = make_sender()
        blocked, reason = s.is_rgpd_blocked("notanemail")
        assert blocked
        assert "Invalid" in reason

    def test_empty_email_is_blocked(self):
        s = make_sender()
        blocked, _ = s.is_rgpd_blocked("")
        assert blocked

    def test_dynamic_blacklist_addition(self):
        s = make_sender()
        s.add_to_blacklist("spammer.com")
        blocked, _ = s.is_rgpd_blocked("user@spammer.com")
        assert blocked

    def test_dynamic_address_blacklist(self):
        s = make_sender()
        s.add_to_blacklist("opted-out@example.com")
        blocked, _ = s.is_rgpd_blocked("opted-out@example.com")
        assert blocked

    def test_blacklisted_domain_does_not_affect_others(self):
        s = make_sender()
        s.add_to_blacklist("bad.com")
        blocked, _ = s.is_rgpd_blocked("user@good.com")
        assert not blocked


# ── Dry-run sends ─────────────────────────────────────────────────────────────

class TestDryRunSend:
    def test_dry_run_succeeds(self):
        s = make_sender()
        result = s.send("contact@enterprise.fr", "Objet test", "Corps du message")
        assert result.success is True

    def test_dry_run_returns_send_result(self):
        s = make_sender()
        result = s.send("contact@enterprise.fr", "Objet", "Corps")
        assert isinstance(result, SendResult)

    def test_dry_run_has_message_id(self):
        s = make_sender()
        result = s.send("contact@enterprise.fr", "Objet", "Corps")
        assert result.message_id and "@competeiq.fr" in result.message_id

    def test_dry_run_has_recipient(self):
        s = make_sender()
        result = s.send("contact@enterprise.fr", "Objet", "Corps")
        assert result.recipient == "contact@enterprise.fr"

    def test_dry_run_increments_sent_count(self):
        s = make_sender()
        s.send("a@company.fr", "S", "B")
        s.send("b@company.fr", "S", "B")
        assert s.get_stats()["sent"] == 2

    def test_rgpd_block_returns_failure(self):
        s = make_sender()
        result = s.send("user@gmail.com", "Objet", "Corps")
        assert result.success is False
        assert "RGPD" in result.error

    def test_rgpd_block_does_not_increment_sent(self):
        s = make_sender()
        s.send("user@gmail.com", "Objet", "Corps")
        assert s.get_stats()["sent"] == 0


# ── SMTP send (mocked) ────────────────────────────────────────────────────────

class TestSMTPSend:
    def test_successful_smtp_send(self):
        s = make_sender(smtp_host="smtp.example.com", smtp_user="u", smtp_password="p")
        with patch("smtplib.SMTP") as mock_smtp:
            instance = mock_smtp.return_value.__enter__.return_value
            result = s.send("contact@enterprise.fr", "Objet", "Corps")
        assert result.success is True
        assert result.retries == 0

    def test_smtp_retries_on_error(self):
        s = make_sender(smtp_host="smtp.example.com", max_retries=3)
        import smtplib
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise smtplib.SMTPException("Transient error")
            return MagicMock()

        with patch("smtplib.SMTP", side_effect=side_effect):
            with patch("time.sleep"):  # don't actually sleep
                result = s.send("contact@enterprise.fr", "Objet", "Corps")

        assert result.success is True
        assert result.retries >= 1

    def test_hard_bounce_blacklists_address(self):
        import smtplib
        s = make_sender(smtp_host="smtp.example.com")

        with patch("smtplib.SMTP") as mock_smtp:
            instance = mock_smtp.return_value.__enter__.return_value
            instance.sendmail.side_effect = smtplib.SMTPRecipientsRefused({})
            result = s.send("bounce@example.com", "Objet", "Corps")

        assert result.success is False
        blocked, _ = s.is_rgpd_blocked("bounce@example.com")
        assert blocked

    def test_all_retries_exhausted_returns_failure(self):
        import smtplib
        s = make_sender(smtp_host="smtp.example.com", max_retries=2)

        with patch("smtplib.SMTP") as mock_smtp:
            instance = mock_smtp.return_value.__enter__.return_value
            instance.sendmail.side_effect = smtplib.SMTPException("Persistent error")
            with patch("time.sleep"):
                result = s.send("contact@company.fr", "Objet", "Corps")

        assert result.success is False
        assert result.error is not None


# ── Batch send ────────────────────────────────────────────────────────────────

class TestBatchSend:
    def test_batch_returns_one_result_per_email(self):
        s = make_sender()
        emails = [
            ("a@company.fr", "S", "B"),
            ("b@firm.fr", "S", "B"),
            ("c@shop.fr", "S", "B"),
        ]
        results = s.send_batch(emails)
        assert len(results) == 3

    def test_batch_with_mixed_rgpd(self):
        s = make_sender()
        emails = [
            ("a@company.fr", "S", "B"),
            ("user@gmail.com", "S", "B"),  # blocked
            ("b@firm.fr", "S", "B"),
        ]
        results = s.send_batch(emails)
        assert results[0].success is True
        assert results[1].success is False
        assert results[2].success is True

    def test_batch_counts_correctly(self):
        s = make_sender()
        emails = [(f"contact{i}@company.fr", "S", "B") for i in range(5)]
        results = s.send_batch(emails)
        assert s.get_stats()["sent"] == 5


# ── Stats ─────────────────────────────────────────────────────────────────────

class TestStats:
    def test_initial_stats_are_zero(self):
        s = make_sender()
        stats = s.get_stats()
        assert stats["sent"] == 0
        assert stats["failed"] == 0
        assert stats["total"] == 0
        assert stats["success_rate"] == 0.0

    def test_success_rate_calculation(self):
        s = make_sender()
        s.send("a@company.fr", "S", "B")
        s.send("b@company.fr", "S", "B")
        # Force one failure via RGPD
        s.send("user@gmail.com", "S", "B")
        stats = s.get_stats()
        # 2 sent successes, 0 failures (RGPD blocks don't count as failures)
        assert stats["sent"] == 2

    def test_stats_has_blacklisted_domains_count(self):
        s = make_sender()
        s.add_to_blacklist("spammer.com")
        stats = s.get_stats()
        assert stats["blacklisted_domains"] >= 1
