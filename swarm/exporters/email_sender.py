"""
SMTP Email Sender with RGPD compliance and retry logic.

Handles outbound cold-email delivery for Division 2 outreach records.
Rate-limited, opt-out checked, throttled to respect ISP limits.

Usage:
    from exporters.email_sender import EmailSender
    sender = EmailSender()
    result = sender.send(record)
    print(result.success, result.message_id)
"""

from __future__ import annotations

import logging
import os
import smtplib
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

logger = logging.getLogger("swarm.email_sender")

# ── RGPD / opt-out blacklist (loaded from env or Division 5) ──────────────────

_BLACKLISTED_DOMAINS: set[str] = set(
    os.getenv("EMAIL_BLACKLIST_DOMAINS", "").split(",")
) - {""}

# Domains that are always blocked (generic/shared mailboxes)
_ALWAYS_BLOCKED = {
    "gmail.com", "hotmail.com", "yahoo.fr", "yahoo.com",
    "orange.fr", "free.fr", "sfr.fr", "laposte.net",
    "wanadoo.fr", "outlook.com", "live.fr",
}

# ── Send result ───────────────────────────────────────────────────────────────


@dataclass
class SendResult:
    success: bool
    recipient: str
    message_id: str
    sent_at: str
    error: Optional[str] = None
    retries: int = 0

    def to_dict(self) -> dict:
        return self.__dict__.copy()


# ── EmailSender ───────────────────────────────────────────────────────────────


class EmailSender:
    """
    SMTP-backed sender with:
    - RGPD opt-out check (domain + address blacklist)
    - Exponential back-off retry (up to max_retries)
    - Configurable rate limit (emails per minute)
    - Unsubscribe header (RFC 8058) on every email
    - Dry-run mode when SMTP_HOST is not set
    """

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: int = 587,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None,
        from_email: Optional[str] = None,
        from_name: str = "CompeteIQ Outreach",
        max_retries: int = 3,
        rate_limit_per_minute: int = 30,
    ):
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", smtp_port))
        self.smtp_user = smtp_user or os.getenv("SMTP_USER")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD")
        self.from_email = from_email or os.getenv("SMTP_FROM", "noreply@competeiq.fr")
        self.from_name = from_name
        self.max_retries = max_retries
        self._min_interval = 60.0 / max(rate_limit_per_minute, 1)
        self._last_sent_at: float = 0.0
        self._sent_count = 0
        self._failed_count = 0
        dry = not self.smtp_host
        logger.info(
            "EmailSender init — host=%s port=%d from=%s dry_run=%s",
            self.smtp_host or "NONE", self.smtp_port, self.from_email, dry,
        )

    # ── RGPD checks ───────────────────────────────────────────────────────────

    def is_rgpd_blocked(self, email: str) -> tuple[bool, str]:
        """Returns (blocked, reason)."""
        if not email or "@" not in email:
            return True, "Invalid email format"
        domain = email.split("@", 1)[1].lower()
        if domain in _ALWAYS_BLOCKED:
            return True, f"Personal mailbox blocked: {domain}"
        if domain in _BLACKLISTED_DOMAINS:
            return True, f"Domain on opt-out list: {domain}"
        if email.lower() in _BLACKLISTED_DOMAINS:
            return True, "Address on opt-out list"
        return False, ""

    def add_to_blacklist(self, email_or_domain: str) -> None:
        """Dynamically add an address or domain to the RGPD blacklist."""
        _BLACKLISTED_DOMAINS.add(email_or_domain.lower())
        logger.info("RGPD blacklist updated: +%s", email_or_domain)

    # ── Email construction ────────────────────────────────────────────────────

    def _build_message(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        unsubscribe_url: Optional[str] = None,
    ) -> MIMEMultipart:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"{self.from_name} <{self.from_email}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg["Message-ID"] = f"<{uuid.uuid4().hex}@competeiq.fr>"
        msg["X-Mailer"] = "CompeteIQ-Swarm/1.0"

        if unsubscribe_url:
            msg["List-Unsubscribe"] = f"<{unsubscribe_url}>, <mailto:{self.from_email}?subject=STOP>"
            msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"

        # Plain text with unsubscribe footer
        footer = (
            f"\n\n---\nVous recevez cet e-mail car votre site a été analysé automatiquement. "
            f"Pour ne plus recevoir nos messages : {unsubscribe_url or self.from_email}"
        )
        plain_body = body_text + footer
        msg.attach(MIMEText(plain_body, "plain", "utf-8"))
        return msg

    # ── SMTP send ─────────────────────────────────────────────────────────────

    def _smtp_send(self, msg: MIMEMultipart, to_email: str) -> None:
        """Open an SMTP connection, send, and close. Raises on failure."""
        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.from_email, [to_email], msg.as_string())

    # ── Public API ────────────────────────────────────────────────────────────

    def send(
        self,
        to_email: str,
        subject: str,
        body: str,
        unsubscribe_url: Optional[str] = None,
    ) -> SendResult:
        """
        Send a single email. Handles RGPD check, rate-limiting, retries.
        Returns a SendResult regardless of outcome.
        """
        blocked, reason = self.is_rgpd_blocked(to_email)
        if blocked:
            logger.warning("RGPD block — skipping %s: %s", to_email, reason)
            return SendResult(
                success=False,
                recipient=to_email,
                message_id="",
                sent_at=datetime.utcnow().isoformat(),
                error=f"RGPD: {reason}",
            )

        # Rate limiting
        elapsed = time.monotonic() - self._last_sent_at
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)

        msg = self._build_message(to_email, subject, body, unsubscribe_url)
        message_id = msg["Message-ID"]

        if not self.smtp_host:
            # Dry-run: log and succeed without sending
            logger.info("[DRY-RUN] Would send to %s — subject: %s", to_email, subject)
            self._sent_count += 1
            self._last_sent_at = time.monotonic()
            return SendResult(
                success=True,
                recipient=to_email,
                message_id=message_id,
                sent_at=datetime.utcnow().isoformat(),
            )

        for attempt in range(1, self.max_retries + 1):
            try:
                self._smtp_send(msg, to_email)
                self._sent_count += 1
                self._last_sent_at = time.monotonic()
                logger.info("Email sent → %s (attempt %d)", to_email, attempt)
                return SendResult(
                    success=True,
                    recipient=to_email,
                    message_id=message_id,
                    sent_at=datetime.utcnow().isoformat(),
                    retries=attempt - 1,
                )
            except smtplib.SMTPRecipientsRefused as e:
                # Hard bounce — add to blacklist
                self.add_to_blacklist(to_email)
                self._failed_count += 1
                return SendResult(
                    success=False,
                    recipient=to_email,
                    message_id=message_id,
                    sent_at=datetime.utcnow().isoformat(),
                    error=f"Hard bounce: {e}",
                    retries=attempt - 1,
                )
            except (smtplib.SMTPException, OSError) as e:
                wait = 2 ** attempt
                logger.warning(
                    "SMTP error on attempt %d/%d for %s — retrying in %ds: %s",
                    attempt, self.max_retries, to_email, wait, e,
                )
                if attempt < self.max_retries:
                    time.sleep(wait)
                else:
                    self._failed_count += 1
                    return SendResult(
                        success=False,
                        recipient=to_email,
                        message_id=message_id,
                        sent_at=datetime.utcnow().isoformat(),
                        error=str(e),
                        retries=attempt - 1,
                    )

        # Should not reach here
        self._failed_count += 1
        return SendResult(
            success=False,
            recipient=to_email,
            message_id=message_id,
            sent_at=datetime.utcnow().isoformat(),
            error="Max retries exceeded",
            retries=self.max_retries,
        )

    def send_batch(
        self,
        emails: List[tuple[str, str, str]],  # (to, subject, body)
        unsubscribe_base_url: Optional[str] = None,
    ) -> List[SendResult]:
        """Send a batch of emails. Returns list of SendResult in same order."""
        results = []
        for to_email, subject, body in emails:
            url = f"{unsubscribe_base_url}?email={to_email}" if unsubscribe_base_url else None
            results.append(self.send(to_email, subject, body, url))
        return results

    def get_stats(self) -> dict:
        return {
            "sent": self._sent_count,
            "failed": self._failed_count,
            "total": self._sent_count + self._failed_count,
            "success_rate": (
                round(self._sent_count / (self._sent_count + self._failed_count) * 100, 1)
                if self._sent_count + self._failed_count > 0 else 0.0
            ),
            "blacklisted_domains": len(_BLACKLISTED_DOMAINS),
        }
