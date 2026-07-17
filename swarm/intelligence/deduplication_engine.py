"""
Deduplication Engine — prevents the swarm from contacting the same prospect twice.

Tracks:
  - Contacted domains/emails with cooldown periods
  - Duplicate detection across sectors and agents
  - Suppression list management (opt-outs, bounces, unreachable)
  - Merge of near-duplicate prospect records
"""

from __future__ import annotations

import datetime
import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


# ── Enums ──────────────────────────────────────────────────────────────────────

class SuppressionReason(str, Enum):
    OPT_OUT      = "opt_out"
    BOUNCE       = "bounce"
    SPAM         = "spam"
    UNREACHABLE  = "unreachable"
    COMPETITOR   = "competitor"
    CLIENT       = "client"       # already a paying client — do not contact
    MANUAL       = "manual"


# ── Cooldown defaults (days) ──────────────────────────────────────────────────

_DEFAULT_COOLDOWNS: Dict[str, int] = {
    "email":    30,   # same email address
    "domain":   14,   # same company domain
    "phone":    21,
}


# ── Models ────────────────────────────────────────────────────────────────────

@dataclass
class ContactRecord:
    """Tracks the last outreach attempt for a unique key."""
    key: str                      # normalised email / domain / phone
    key_type: str                 # "email" | "domain" | "phone"
    last_contacted: datetime.datetime
    contact_count: int = 1
    agent_id: str = ""
    sector: str = ""

    def is_in_cooldown(self, cooldown_days: int, as_of: Optional[datetime.datetime] = None) -> bool:
        as_of = as_of or datetime.datetime.utcnow()
        elapsed = (as_of - self.last_contacted).total_seconds() / 86400
        return elapsed < cooldown_days

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "key_type": self.key_type,
            "last_contacted": self.last_contacted.isoformat(),
            "contact_count": self.contact_count,
            "agent_id": self.agent_id,
            "sector": self.sector,
        }


@dataclass
class SuppressionEntry:
    """Permanently suppressed contact — never re-contact."""
    key: str
    key_type: str
    reason: SuppressionReason
    added_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "key_type": self.key_type,
            "reason": self.reason.value,
            "added_at": self.added_at.isoformat(),
            "note": self.note,
        }


@dataclass
class DeduplicationResult:
    """Result of a deduplication check for a single prospect."""
    allowed: bool
    reason: str                        # "ok" | "cooldown" | "suppressed" | "duplicate"
    matching_key: str = ""
    cooldown_remaining_days: float = 0.0

    def to_dict(self) -> dict:
        return {
            "allowed": self.allowed,
            "reason": self.reason,
            "matching_key": self.matching_key,
            "cooldown_remaining_days": round(self.cooldown_remaining_days, 1),
        }


# ── Engine ────────────────────────────────────────────────────────────────────

class DeduplicationEngine:
    """
    Central registry that prevents duplicate outreach.

    - `check()` verifies if a prospect can be contacted now.
    - `record_contact()` logs a successful send.
    - `suppress()` permanently blocks a contact.
    - `filter_batch()` splits a list into (allowed, blocked) sublists.
    """

    def __init__(
        self,
        cooldown_days: Optional[Dict[str, int]] = None,
    ):
        self._cooldowns: Dict[str, int] = {**_DEFAULT_COOLDOWNS, **(cooldown_days or {})}
        self._contacts: Dict[str, ContactRecord] = {}   # key → record
        self._suppressed: Dict[str, SuppressionEntry] = {}
        self._fingerprints: Set[str] = set()            # content-hash dedup

    # ── Normalisation ─────────────────────────────────────────────────────────

    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.strip().lower()

    @staticmethod
    def _extract_domain(email: str) -> str:
        email = email.strip().lower()
        if "@" in email:
            return email.split("@", 1)[1]
        return email

    @staticmethod
    def _normalize_phone(phone: str) -> str:
        digits = re.sub(r"\D", "", phone)
        if digits.startswith("33") and len(digits) == 11:
            digits = "0" + digits[2:]
        return digits

    @staticmethod
    def _fingerprint(company_name: str, city: str) -> str:
        raw = re.sub(r"\s+", " ", f"{company_name.lower().strip()} {city.lower().strip()}")
        return hashlib.md5(raw.encode()).hexdigest()

    # ── Core check ────────────────────────────────────────────────────────────

    def check(
        self,
        email: str,
        company_name: str = "",
        city: str = "",
        phone: str = "",
        as_of: Optional[datetime.datetime] = None,
    ) -> DeduplicationResult:
        """Return whether this prospect can be contacted now."""
        as_of = as_of or datetime.datetime.utcnow()

        norm_email = self._normalize_email(email)
        domain = self._extract_domain(email)

        # 1. Suppression check — email
        if norm_email in self._suppressed:
            entry = self._suppressed[norm_email]
            return DeduplicationResult(False, "suppressed", norm_email)

        # 2. Suppression check — domain
        if domain in self._suppressed:
            return DeduplicationResult(False, "suppressed", domain)

        # 3. Suppression check — phone
        if phone:
            norm_phone = self._normalize_phone(phone)
            if norm_phone in self._suppressed:
                return DeduplicationResult(False, "suppressed", norm_phone)

        # 4. Content fingerprint dedup (same company+city already in batch)
        if company_name:
            fp = self._fingerprint(company_name, city)
            if fp in self._fingerprints:
                return DeduplicationResult(False, "duplicate", fp)

        # 5. Cooldown — email
        if norm_email in self._contacts:
            rec = self._contacts[norm_email]
            cd = self._cooldowns.get("email", 30)
            if rec.is_in_cooldown(cd, as_of):
                remaining = cd - (as_of - rec.last_contacted).total_seconds() / 86400
                return DeduplicationResult(False, "cooldown", norm_email, remaining)

        # 6. Cooldown — domain
        if domain in self._contacts:
            rec = self._contacts[domain]
            cd = self._cooldowns.get("domain", 14)
            if rec.is_in_cooldown(cd, as_of):
                remaining = cd - (as_of - rec.last_contacted).total_seconds() / 86400
                return DeduplicationResult(False, "cooldown", domain, remaining)

        return DeduplicationResult(True, "ok")

    # ── Record contact ────────────────────────────────────────────────────────

    def record_contact(
        self,
        email: str,
        company_name: str = "",
        city: str = "",
        phone: str = "",
        agent_id: str = "",
        sector: str = "",
        as_of: Optional[datetime.datetime] = None,
    ) -> None:
        """Log that a prospect was contacted right now."""
        as_of = as_of or datetime.datetime.utcnow()
        norm_email = self._normalize_email(email)
        domain = self._extract_domain(email)

        for key, key_type in [(norm_email, "email"), (domain, "domain")]:
            if key in self._contacts:
                rec = self._contacts[key]
                rec.last_contacted = as_of
                rec.contact_count += 1
            else:
                self._contacts[key] = ContactRecord(
                    key=key, key_type=key_type,
                    last_contacted=as_of, contact_count=1,
                    agent_id=agent_id, sector=sector,
                )

        if phone:
            norm_phone = self._normalize_phone(phone)
            if norm_phone in self._contacts:
                self._contacts[norm_phone].last_contacted = as_of
                self._contacts[norm_phone].contact_count += 1
            else:
                self._contacts[norm_phone] = ContactRecord(
                    key=norm_phone, key_type="phone",
                    last_contacted=as_of, contact_count=1,
                    agent_id=agent_id, sector=sector,
                )

        if company_name:
            self._fingerprints.add(self._fingerprint(company_name, city))

    # ── Suppression list ──────────────────────────────────────────────────────

    def suppress(
        self,
        key: str,
        key_type: str = "email",
        reason: SuppressionReason = SuppressionReason.OPT_OUT,
        note: str = "",
    ) -> None:
        """Permanently block a key from receiving outreach."""
        normalized = (
            self._normalize_email(key) if key_type == "email"
            else self._normalize_phone(key) if key_type == "phone"
            else key.strip().lower()
        )
        self._suppressed[normalized] = SuppressionEntry(
            key=normalized, key_type=key_type,
            reason=reason, note=note,
        )

    def unsuppress(self, key: str) -> bool:
        """Remove a key from the suppression list."""
        normalized = key.strip().lower()
        if normalized in self._suppressed:
            del self._suppressed[normalized]
            return True
        return False

    def is_suppressed(self, key: str) -> bool:
        return key.strip().lower() in self._suppressed

    # ── Batch filter ─────────────────────────────────────────────────────────

    def filter_batch(
        self,
        prospects: List[dict],
        email_field: str = "email",
        company_field: str = "company_name",
        city_field: str = "city",
        phone_field: str = "phone",
        as_of: Optional[datetime.datetime] = None,
    ) -> Tuple[List[dict], List[dict]]:
        """
        Split a list of prospect dicts into (allowed, blocked).
        Also registers fingerprints as it goes to catch intra-batch duplicates.
        """
        as_of = as_of or datetime.datetime.utcnow()
        allowed: List[dict] = []
        blocked: List[dict] = []
        batch_fingerprints: Set[str] = set()

        for p in prospects:
            email = p.get(email_field, "")
            company = p.get(company_field, "")
            city = p.get(city_field, "")
            phone = p.get(phone_field, "")

            # Intra-batch duplicate check
            if company:
                fp = self._fingerprint(company, city)
                if fp in batch_fingerprints or fp in self._fingerprints:
                    blocked.append({**p, "_block_reason": "duplicate"})
                    continue
                batch_fingerprints.add(fp)

            result = self.check(email, company, city, phone, as_of)
            if result.allowed:
                allowed.append(p)
            else:
                blocked.append({**p, "_block_reason": result.reason})

        return allowed, blocked

    # ── Queries ───────────────────────────────────────────────────────────────

    def get_contact(self, key: str) -> Optional[ContactRecord]:
        return self._contacts.get(self._normalize_email(key)) or self._contacts.get(key.strip().lower())

    def list_suppressed(self) -> List[SuppressionEntry]:
        return list(self._suppressed.values())

    def suppression_count(self) -> int:
        return len(self._suppressed)

    def contact_count(self) -> int:
        return len({k for k, v in self._contacts.items() if v.key_type == "email"})

    # ── Export / import ───────────────────────────────────────────────────────

    def export_suppression_list(self) -> List[dict]:
        return [e.to_dict() for e in self._suppressed.values()]

    def import_suppression_list(self, entries: List[dict]) -> int:
        imported = 0
        for e in entries:
            try:
                reason = SuppressionReason(e.get("reason", "manual"))
            except ValueError:
                reason = SuppressionReason.MANUAL
            self.suppress(
                key=e["key"],
                key_type=e.get("key_type", "email"),
                reason=reason,
                note=e.get("note", ""),
            )
            imported += 1
        return imported

    # ── Summary ───────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        email_records = [r for r in self._contacts.values() if r.key_type == "email"]
        domain_records = [r for r in self._contacts.values() if r.key_type == "domain"]
        return {
            "unique_emails_contacted": len(email_records),
            "unique_domains_contacted": len(domain_records),
            "suppression_list_size": len(self._suppressed),
            "fingerprints_seen": len(self._fingerprints),
            "total_contact_events": sum(r.contact_count for r in email_records),
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset(self, keep_suppressed: bool = False) -> None:
        """Clear contact history. Optionally preserve the suppression list."""
        self._contacts.clear()
        self._fingerprints.clear()
        if not keep_suppressed:
            self._suppressed.clear()
