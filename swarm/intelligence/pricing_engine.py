"""
Pricing Engine — computes dynamic quote prices based on prospect diagnostics,
sector ROI multipliers, and tiered service packages.

Packages:
  - Starter (99€):  basic PageSpeed fix + mobile optimisation
  - Standard (249€): Starter + SEO report + contact form fix
  - Premium (449€): Standard + full redesign mockup + 30-day follow-up
  - Enterprise (799€+): custom, per-audit negotiation
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ── Package catalogue ─────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Package:
    code: str
    name: str
    base_price_eur: float
    deliverables: List[str]
    description: str

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "base_price_eur": self.base_price_eur,
            "deliverables": list(self.deliverables),
            "description": self.description,
        }


PACKAGES: Dict[str, Package] = {
    "starter": Package(
        code="starter",
        name="Starter",
        base_price_eur=99.0,
        deliverables=["pagespeed_fix.zip", "mobile_css.zip"],
        description="Optimisation PageSpeed et responsive mobile",
    ),
    "standard": Package(
        code="standard",
        name="Standard",
        base_price_eur=249.0,
        deliverables=["pagespeed_fix.zip", "mobile_css.zip", "seo_report.pdf", "contact_form_fix.zip"],
        description="Standard + rapport SEO + correction formulaire de contact",
    ),
    "premium": Package(
        code="premium",
        name="Premium",
        base_price_eur=449.0,
        deliverables=["pagespeed_fix.zip", "mobile_css.zip", "seo_report.pdf",
                      "contact_form_fix.zip", "redesign_mockup.figma", "followup_30j.pdf"],
        description="Premium + maquette redesign + suivi 30 jours",
    ),
    "enterprise": Package(
        code="enterprise",
        name="Enterprise",
        base_price_eur=799.0,
        deliverables=["audit_complet.pdf", "pagespeed_fix.zip", "mobile_css.zip",
                      "seo_report.pdf", "contact_form_fix.zip", "redesign_mockup.figma",
                      "followup_30j.pdf", "formation_equipe.pdf"],
        description="Audit complet + tout Premium + formation équipe",
    ),
}

# Sector-specific ROI multipliers (premium sectors pay more)
_SECTOR_MULTIPLIERS: Dict[str, float] = {
    "médical":     1.30,
    "juridique":   1.25,
    "immobilier":  1.20,
    "formation":   1.15,
    "restaurant":  1.10,
    "artisan":     1.05,
    "garage":      1.05,
    "beauté":      1.00,
    "association": 0.85,   # public/charitable — discounted
}

TVA_RATE = 0.20


# ── Quote models ──────────────────────────────────────────────────────────────

@dataclass
class QuoteLineItem:
    label: str
    amount_eur: float
    quantity: int = 1

    @property
    def total_eur(self) -> float:
        return self.amount_eur * self.quantity

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "amount_eur": round(self.amount_eur, 2),
            "quantity": self.quantity,
            "total_eur": round(self.total_eur, 2),
        }


@dataclass
class Quote:
    prospect_id: str
    company_name: str
    sector: str
    package: Package
    line_items: List[QuoteLineItem] = field(default_factory=list)
    discount_pct: float = 0.0           # 0–1
    sector_multiplier: float = 1.0
    urgency_bonus: float = 0.0          # flat EUR bump for urgent repairs

    @property
    def subtotal_eur(self) -> float:
        return sum(item.total_eur for item in self.line_items)

    @property
    def discount_amount_eur(self) -> float:
        return self.subtotal_eur * self.discount_pct

    @property
    def total_ht_eur(self) -> float:
        return max(0.0, self.subtotal_eur - self.discount_amount_eur + self.urgency_bonus)

    @property
    def tva_eur(self) -> float:
        return self.total_ht_eur * TVA_RATE

    @property
    def total_ttc_eur(self) -> float:
        return self.total_ht_eur + self.tva_eur

    def to_dict(self) -> dict:
        return {
            "prospect_id": self.prospect_id,
            "company_name": self.company_name,
            "sector": self.sector,
            "package": self.package.to_dict(),
            "line_items": [li.to_dict() for li in self.line_items],
            "discount_pct": round(self.discount_pct * 100, 1),
            "discount_amount_eur": round(self.discount_amount_eur, 2),
            "urgency_bonus_eur": round(self.urgency_bonus, 2),
            "subtotal_eur": round(self.subtotal_eur, 2),
            "total_ht_eur": round(self.total_ht_eur, 2),
            "tva_eur": round(self.tva_eur, 2),
            "total_ttc_eur": round(self.total_ttc_eur, 2),
            "sector_multiplier": self.sector_multiplier,
        }

    def summary_line(self) -> str:
        return (
            f"{self.company_name} ({self.sector}) | "
            f"{self.package.name} | "
            f"HT: {self.total_ht_eur:.0f}€ | "
            f"TTC: {self.total_ttc_eur:.0f}€"
        )


# ── Engine ────────────────────────────────────────────────────────────────────

class PricingEngine:
    """
    Computes dynamic quotes for prospects based on:
    - Diagnostic severity (PageSpeed score, load time, mobile issues)
    - Sector ROI multiplier
    - Tier-based package recommendation
    - Optional discounts and urgency bonuses
    """

    def __init__(self, tva_rate: float = TVA_RATE):
        self.tva_rate = tva_rate
        self._quotes: Dict[str, Quote] = {}

    # ── Package selection ─────────────────────────────────────────────────────

    def recommend_package(
        self,
        pagespeed_score: int,
        load_time_ms: int,
        mobile_responsive: bool,
        issue_count: int = 0,
    ) -> Package:
        """Select the best-fit package based on diagnostic severity."""
        severity = self._severity_score(pagespeed_score, load_time_ms, mobile_responsive, issue_count)
        if severity >= 0.75:
            return PACKAGES["enterprise"]
        if severity >= 0.55:
            return PACKAGES["premium"]
        if severity >= 0.30:
            return PACKAGES["standard"]
        return PACKAGES["starter"]

    @staticmethod
    def _severity_score(
        pagespeed_score: int,
        load_time_ms: int,
        mobile_responsive: bool,
        issue_count: int,
    ) -> float:
        """0.0 (no problems) → 1.0 (critical state)."""
        ps_component  = max(0.0, (100 - pagespeed_score) / 100) * 0.40
        lt_component  = min(1.0, max(0.0, (load_time_ms - 1000) / 9000)) * 0.30
        mob_component = (0.0 if mobile_responsive else 0.20)
        iss_component = min(1.0, issue_count / 10) * 0.10
        return ps_component + lt_component + mob_component + iss_component

    # ── Sector multiplier ─────────────────────────────────────────────────────

    @staticmethod
    def sector_multiplier(sector: str) -> float:
        sector_lower = sector.lower()
        for key, mult in _SECTOR_MULTIPLIERS.items():
            if key in sector_lower:
                return mult
        return 1.0

    # ── Quote generation ──────────────────────────────────────────────────────

    def generate_quote(
        self,
        prospect_id: str,
        company_name: str,
        sector: str,
        pagespeed_score: int,
        load_time_ms: int,
        mobile_responsive: bool,
        issue_count: int = 0,
        force_package: Optional[str] = None,
        discount_pct: float = 0.0,
        urgency: bool = False,
    ) -> Quote:
        """
        Build a full Quote for a prospect.
        `force_package` overrides automatic package selection.
        """
        pkg = PACKAGES.get(force_package or "") or self.recommend_package(
            pagespeed_score, load_time_ms, mobile_responsive, issue_count
        )
        mult = self.sector_multiplier(sector)
        adjusted_base = round(pkg.base_price_eur * mult, 2)

        line_items = [QuoteLineItem(label=pkg.name, amount_eur=adjusted_base)]

        urgency_bonus = 0.0
        if urgency:
            urgency_bonus = round(adjusted_base * 0.10, 2)

        quote = Quote(
            prospect_id=prospect_id,
            company_name=company_name,
            sector=sector,
            package=pkg,
            line_items=line_items,
            discount_pct=max(0.0, min(1.0, discount_pct)),
            sector_multiplier=mult,
            urgency_bonus=urgency_bonus,
        )
        self._quotes[prospect_id] = quote
        return quote

    # ── Batch pricing ─────────────────────────────────────────────────────────

    def price_batch(
        self,
        prospects: List[dict],
        default_discount_pct: float = 0.0,
    ) -> List[Quote]:
        """Price a list of prospect dicts. Each must have the required fields."""
        quotes = []
        for p in prospects:
            q = self.generate_quote(
                prospect_id=p.get("company_id", p.get("prospect_id", "")),
                company_name=p.get("company_name", p.get("name", "")),
                sector=p.get("sector", ""),
                pagespeed_score=p.get("pagespeed_score", 50),
                load_time_ms=p.get("load_time_ms", 2000),
                mobile_responsive=p.get("mobile_responsive", True),
                issue_count=len(p.get("detected_issues", [])),
                discount_pct=default_discount_pct,
            )
            quotes.append(q)
        return quotes

    # ── Queries ───────────────────────────────────────────────────────────────

    def get_quote(self, prospect_id: str) -> Optional[Quote]:
        return self._quotes.get(prospect_id)

    def all_quotes(self) -> List[Quote]:
        return list(self._quotes.values())

    def total_pipeline_eur(self) -> float:
        return sum(q.total_ttc_eur for q in self._quotes.values())

    def average_quote_eur(self) -> float:
        quotes = list(self._quotes.values())
        return sum(q.total_ttc_eur for q in quotes) / len(quotes) if quotes else 0.0

    def quotes_by_package(self) -> Dict[str, int]:
        result: Dict[str, int] = {}
        for q in self._quotes.values():
            result[q.package.code] = result.get(q.package.code, 0) + 1
        return result

    def top_quotes(self, n: int = 10) -> List[Quote]:
        return sorted(self._quotes.values(), key=lambda q: q.total_ttc_eur, reverse=True)[:n]

    # ── Summary ───────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        quotes = list(self._quotes.values())
        if not quotes:
            return {
                "total_quotes": 0,
                "total_pipeline_eur": 0.0,
                "average_quote_eur": 0.0,
                "by_package": {},
            }
        return {
            "total_quotes": len(quotes),
            "total_pipeline_eur": round(self.total_pipeline_eur(), 2),
            "average_quote_eur": round(self.average_quote_eur(), 2),
            "by_package": self.quotes_by_package(),
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._quotes.clear()
