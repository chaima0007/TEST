"""
Negotiation State Manager — tracks offer/counter-offer cycles,
deal terms, negotiation stages, and outcomes for each prospect.

Negotiation lifecycle:
  OPENED → IN_PROGRESS (offers exchanged) → AGREED / FAILED / ABANDONED

Each negotiation can have multiple rounds of offers. The manager
records who proposed each change (us vs prospect), computes
the concession delta, and surfaces deal quality metrics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ── Enums ─────────────────────────────────────────────────────────────────────

class NegotiationStatus(str, Enum):
    OPENED      = "opened"
    IN_PROGRESS = "in_progress"
    AGREED      = "agreed"
    FAILED      = "failed"
    ABANDONED   = "abandoned"


class OfferParty(str, Enum):
    US       = "us"
    PROSPECT = "prospect"


class ConcessionType(str, Enum):
    PRICE    = "price"
    SCOPE    = "scope"
    TIMELINE = "timeline"
    PAYMENT  = "payment"
    OTHER    = "other"


# ── Offer record ──────────────────────────────────────────────────────────────

@dataclass
class Offer:
    round_number:     int
    party:            OfferParty
    amount:           float            # TTC EUR
    concession_type:  ConcessionType
    note:             str = ""
    proposed_at:      datetime = field(default_factory=datetime.utcnow)

    @property
    def concession_delta(self) -> float:
        return 0.0  # computed externally vs previous offer

    def to_dict(self) -> dict:
        return {
            "round_number":    self.round_number,
            "party":           self.party.value,
            "amount":          self.amount,
            "concession_type": self.concession_type.value,
            "note":            self.note,
            "proposed_at":     self.proposed_at.isoformat(),
        }


# ── Negotiation record ────────────────────────────────────────────────────────

@dataclass
class Negotiation:
    negotiation_id:  str
    prospect_id:     str
    company_name:    str
    sector:          str
    asking_price:    float            # our initial price (TTC EUR)
    status:          NegotiationStatus = NegotiationStatus.OPENED
    offers:          List[Offer] = field(default_factory=list)
    opened_at:       datetime = field(default_factory=datetime.utcnow)
    closed_at:       Optional[datetime] = None
    failure_reason:  str = ""

    # ── Offer management ──────────────────────────────────────────────────────

    def add_offer(
        self,
        party: OfferParty,
        amount: float,
        concession_type: ConcessionType = ConcessionType.PRICE,
        note: str = "",
        ts: Optional[datetime] = None,
    ) -> Offer:
        offer = Offer(
            round_number=len(self.offers) + 1,
            party=party,
            amount=amount,
            concession_type=concession_type,
            note=note,
            proposed_at=ts or datetime.utcnow(),
        )
        self.offers.append(offer)
        if self.status == NegotiationStatus.OPENED:
            self.status = NegotiationStatus.IN_PROGRESS
        return offer

    def agree(self, ts: Optional[datetime] = None) -> bool:
        if self.status in (NegotiationStatus.AGREED, NegotiationStatus.FAILED, NegotiationStatus.ABANDONED):
            return False
        self.status = NegotiationStatus.AGREED
        self.closed_at = ts or datetime.utcnow()
        return True

    def fail(self, reason: str = "", ts: Optional[datetime] = None) -> bool:
        if self.status in (NegotiationStatus.AGREED, NegotiationStatus.FAILED, NegotiationStatus.ABANDONED):
            return False
        self.status = NegotiationStatus.FAILED
        self.failure_reason = reason
        self.closed_at = ts or datetime.utcnow()
        return True

    def abandon(self, ts: Optional[datetime] = None) -> bool:
        if self.status in (NegotiationStatus.AGREED, NegotiationStatus.FAILED, NegotiationStatus.ABANDONED):
            return False
        self.status = NegotiationStatus.ABANDONED
        self.closed_at = ts or datetime.utcnow()
        return True

    # ── Analytics ─────────────────────────────────────────────────────────────

    @property
    def current_amount(self) -> float:
        """Latest offer amount, or asking_price if no offers yet."""
        return self.offers[-1].amount if self.offers else self.asking_price

    @property
    def final_amount(self) -> Optional[float]:
        """Amount only when AGREED."""
        return self.current_amount if self.status == NegotiationStatus.AGREED else None

    @property
    def discount_pct(self) -> float:
        """How much we gave away relative to asking price (0–100)."""
        if self.asking_price == 0:
            return 0.0
        return max(0.0, round((self.asking_price - self.current_amount) / self.asking_price * 100, 1))

    @property
    def rounds(self) -> int:
        return len(self.offers)

    @property
    def duration_days(self) -> float:
        end = self.closed_at or datetime.utcnow()
        return round((end - self.opened_at).total_seconds() / 86400, 1)

    @property
    def our_last_offer(self) -> Optional[Offer]:
        for o in reversed(self.offers):
            if o.party == OfferParty.US:
                return o
        return None

    @property
    def prospect_last_offer(self) -> Optional[Offer]:
        for o in reversed(self.offers):
            if o.party == OfferParty.PROSPECT:
                return o
        return None

    @property
    def total_concession_eur(self) -> float:
        """Total EUR we dropped from asking price to current."""
        return max(0.0, round(self.asking_price - self.current_amount, 2))

    def round_deltas(self) -> List[dict]:
        """Per-round amount and delta vs previous."""
        result = []
        prev = self.asking_price
        for o in self.offers:
            delta = o.amount - prev
            result.append({
                "round":  o.round_number,
                "party":  o.party.value,
                "amount": o.amount,
                "delta":  round(delta, 2),
            })
            prev = o.amount
        return result

    def to_dict(self) -> dict:
        return {
            "negotiation_id":      self.negotiation_id,
            "prospect_id":         self.prospect_id,
            "company_name":        self.company_name,
            "sector":              self.sector,
            "asking_price":        self.asking_price,
            "current_amount":      self.current_amount,
            "final_amount":        self.final_amount,
            "discount_pct":        self.discount_pct,
            "total_concession_eur": self.total_concession_eur,
            "status":              self.status.value,
            "rounds":              self.rounds,
            "duration_days":       self.duration_days,
            "failure_reason":      self.failure_reason,
            "opened_at":           self.opened_at.isoformat(),
            "closed_at":           self.closed_at.isoformat() if self.closed_at else None,
            "offers":              [o.to_dict() for o in self.offers],
        }


# ── Manager ───────────────────────────────────────────────────────────────────

class NegotiationManager:
    """
    Manages all negotiations across all prospects.

    Usage::
        mgr = NegotiationManager()
        neg = mgr.open("p001", "Plomberie Martin", "artisan", asking_price=598.80)
        mgr.add_offer(neg.negotiation_id, OfferParty.PROSPECT, 520.0, note="Trop cher")
        mgr.add_offer(neg.negotiation_id, OfferParty.US, 549.0, note="Effort max")
        mgr.agree(neg.negotiation_id)
        report = mgr.summary()
    """

    def __init__(self) -> None:
        self._records: Dict[str, Negotiation] = {}
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"neg_{self._counter:05d}"

    # ── Open / manage ─────────────────────────────────────────────────────────

    def open(
        self,
        prospect_id: str,
        company_name: str,
        sector: str = "",
        asking_price: float = 0.0,
        ts: Optional[datetime] = None,
    ) -> Negotiation:
        neg_id = self._next_id()
        neg = Negotiation(
            negotiation_id=neg_id,
            prospect_id=prospect_id,
            company_name=company_name,
            sector=sector,
            asking_price=asking_price,
            opened_at=ts or datetime.utcnow(),
        )
        self._records[neg_id] = neg
        return neg

    def get(self, negotiation_id: str) -> Optional[Negotiation]:
        return self._records.get(negotiation_id)

    def get_by_prospect(self, prospect_id: str) -> List[Negotiation]:
        return [n for n in self._records.values() if n.prospect_id == prospect_id]

    def all_negotiations(self) -> List[Negotiation]:
        return list(self._records.values())

    # ── Offer lifecycle ───────────────────────────────────────────────────────

    def add_offer(
        self,
        negotiation_id: str,
        party: OfferParty,
        amount: float,
        concession_type: ConcessionType = ConcessionType.PRICE,
        note: str = "",
        ts: Optional[datetime] = None,
    ) -> Optional[Offer]:
        neg = self._records.get(negotiation_id)
        if not neg:
            return None
        return neg.add_offer(party, amount, concession_type, note, ts)

    def agree(self, negotiation_id: str, ts: Optional[datetime] = None) -> bool:
        neg = self._records.get(negotiation_id)
        return neg.agree(ts) if neg else False

    def fail(self, negotiation_id: str, reason: str = "", ts: Optional[datetime] = None) -> bool:
        neg = self._records.get(negotiation_id)
        return neg.fail(reason, ts) if neg else False

    def abandon(self, negotiation_id: str, ts: Optional[datetime] = None) -> bool:
        neg = self._records.get(negotiation_id)
        return neg.abandon(ts) if neg else False

    # ── Queries ───────────────────────────────────────────────────────────────

    def by_status(self, status: NegotiationStatus) -> List[Negotiation]:
        return [n for n in self._records.values() if n.status == status]

    def active(self) -> List[Negotiation]:
        return [n for n in self._records.values() if n.status in (NegotiationStatus.OPENED, NegotiationStatus.IN_PROGRESS)]

    def agreed(self) -> List[Negotiation]:
        return self.by_status(NegotiationStatus.AGREED)

    def failed_or_abandoned(self) -> List[Negotiation]:
        return [n for n in self._records.values() if n.status in (NegotiationStatus.FAILED, NegotiationStatus.ABANDONED)]

    def by_sector(self, sector: str) -> List[Negotiation]:
        return [n for n in self._records.values() if sector.lower() in n.sector.lower()]

    # ── Analytics ─────────────────────────────────────────────────────────────

    def win_rate(self) -> float:
        closed = [n for n in self._records.values() if n.status in (NegotiationStatus.AGREED, NegotiationStatus.FAILED, NegotiationStatus.ABANDONED)]
        if not closed:
            return 0.0
        won = sum(1 for n in closed if n.status == NegotiationStatus.AGREED)
        return round(won / len(closed) * 100, 1)

    def average_discount_pct(self) -> float:
        agreed = self.agreed()
        if not agreed:
            return 0.0
        return round(sum(n.discount_pct for n in agreed) / len(agreed), 1)

    def average_rounds(self) -> float:
        if not self._records:
            return 0.0
        return round(sum(n.rounds for n in self._records.values()) / len(self._records), 1)

    def total_agreed_revenue(self) -> float:
        return round(sum(n.current_amount for n in self.agreed()), 2)

    def total_conceded_eur(self) -> float:
        return round(sum(n.total_concession_eur for n in self.agreed()), 2)

    def average_duration_days(self) -> float:
        closed = [n for n in self._records.values() if n.closed_at]
        if not closed:
            return 0.0
        return round(sum(n.duration_days for n in closed) / len(closed), 1)

    def sector_summary(self) -> Dict[str, dict]:
        result: Dict[str, dict] = {}
        for n in self._records.values():
            s = n.sector or "unknown"
            if s not in result:
                result[s] = {"count": 0, "agreed": 0, "revenue": 0.0, "avg_discount_pct": []}
            result[s]["count"] += 1
            if n.status == NegotiationStatus.AGREED:
                result[s]["agreed"] += 1
                result[s]["revenue"] += n.current_amount
                result[s]["avg_discount_pct"].append(n.discount_pct)
        # Flatten avg
        for s, d in result.items():
            discounts = d.pop("avg_discount_pct")
            d["avg_discount_pct"] = round(sum(discounts) / len(discounts), 1) if discounts else 0.0
            d["revenue"] = round(d["revenue"], 2)
        return result

    def failure_reason_summary(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for n in self.failed_or_abandoned():
            r = n.failure_reason or "unspecified"
            counts[r] = counts.get(r, 0) + 1
        return counts

    def summary(self) -> dict:
        total = len(self._records)
        active_n = self.active()
        agreed_n = self.agreed()
        failed_n = self.failed_or_abandoned()
        return {
            "total":               total,
            "active":              len(active_n),
            "agreed":              len(agreed_n),
            "failed_or_abandoned": len(failed_n),
            "win_rate_pct":        self.win_rate(),
            "avg_discount_pct":    self.average_discount_pct(),
            "avg_rounds":          self.average_rounds(),
            "avg_duration_days":   self.average_duration_days(),
            "total_agreed_eur":    self.total_agreed_revenue(),
            "total_conceded_eur":  self.total_conceded_eur(),
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._records.clear()
        self._counter = 0
