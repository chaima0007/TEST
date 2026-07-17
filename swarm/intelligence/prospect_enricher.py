"""
Prospect Enricher — adds company intelligence to raw ProspectFiche data.

Combines multiple heuristics (sector scoring, urgency signals, company size
estimation, ICP fit score) to prioritise the best prospects for outreach.

Usage:
    from intelligence.prospect_enricher import ProspectEnricher
    enricher = ProspectEnricher()
    enriched = enricher.enrich(fiche)
    priority = enriched.priority_score  # 0–100
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger("swarm.enricher")

# ── Sector ICP weights ────────────────────────────────────────────────────────
# Sectors where mobile PageSpeed problems translate to the most lost revenue

_SECTOR_ICP: dict[str, float] = {
    # High-value sectors (eager buyers, high LTV)
    "restaurant": 0.95,
    "hôtel": 0.95,
    "plombier": 0.90,
    "électricien": 0.90,
    "artisan": 0.88,
    "médecin": 0.85,
    "dentiste": 0.85,
    "avocat": 0.82,
    "comptable": 0.80,
    "notaire": 0.80,
    "architecte": 0.78,
    "immobilier": 0.75,
    "coiffeur": 0.72,
    "auto": 0.70,
    "garage": 0.70,
    "fleuriste": 0.65,
    "boulanger": 0.60,
    # Lower priority (price-sensitive or already tech-savvy)
    "logiciel": 0.30,
    "saas": 0.25,
    "startup": 0.25,
    "agence web": 0.10,
}

# PageSpeed score thresholds: higher urgency = lower score
_PAGESPEED_URGENCY: dict[str, tuple[int, int, float]] = {
    # (min_score, max_score, urgency_multiplier)
    "critique":  (0,  29, 1.0),
    "mauvais":   (30, 49, 0.85),
    "moyen":     (50, 69, 0.60),
    "acceptable":(70, 89, 0.30),
    "bon":       (90, 100, 0.05),
}

# Company size signals from common French business terms/employee counts
_SIZE_SIGNALS = {
    "sarl": "PME",
    "sas": "PME",
    "eurl": "TPE",
    "ei": "TPE",
    "auto-entrepreneur": "TPE",
    "micro-entreprise": "TPE",
    "sa ": "ETI",
    "groupe": "ETI",
    "holding": "ETI",
}


@dataclass
class EnrichedProspect:
    company_id: str
    name: str
    sector: str
    website: str
    contact_email: str
    pagespeed_score: int
    load_time_ms: int

    # Enrichment fields
    icp_fit: float = 0.0       # 0.0–1.0 ideal customer profile fit
    urgency: float = 0.0       # 0.0–1.0 (based on PageSpeed)
    company_size: str = "PME"  # TPE | PME | ETI
    priority_score: int = 0    # 0–100 composite score
    tier: str = "C"            # A | B | C tier
    sector_score: float = 0.0
    urgency_label: str = "moyen"
    estimated_revenue_impact_eur: float = 0.0
    enrichment_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return self.__dict__.copy()


class ProspectEnricher:
    """
    Enriches ProspectFiche objects with scoring signals for prioritisation.
    Fully offline — no external API calls required.
    """

    def __init__(self, min_priority_threshold: int = 20):
        self.min_priority_threshold = min_priority_threshold
        logger.info("ProspectEnricher init — ICP sectors: %d", len(_SECTOR_ICP))

    # ── ICP fit scoring ───────────────────────────────────────────────────────

    def _score_icp(self, sector: str) -> float:
        s = sector.lower()
        # Direct match first
        for key, score in _SECTOR_ICP.items():
            if key in s:
                return score
        return 0.45  # neutral default for unrecognised sectors

    # ── PageSpeed urgency ──────────────────────────────────────────────────────

    def _score_urgency(self, pagespeed: int) -> tuple[float, str]:
        for label, (lo, hi, mult) in _PAGESPEED_URGENCY.items():
            if lo <= pagespeed <= hi:
                return mult, label
        return 0.1, "bon"

    # ── Company size detection ─────────────────────────────────────────────────

    def _detect_size(self, name: str, website: str) -> str:
        combined = (name + " " + website).lower()
        for signal, size in _SIZE_SIGNALS.items():
            if signal in combined:
                return size
        return "PME"

    # ── Revenue impact estimation ──────────────────────────────────────────────

    def _estimate_revenue_impact(self, load_time_ms: int, sector: str, size: str) -> float:
        """
        Rough estimate of annual revenue lost to slow mobile site.
        Based on industry benchmark: +1s load time → -7% conversion.
        """
        size_base = {"TPE": 80_000, "PME": 400_000, "ETI": 2_000_000}
        sector_online_share = 0.15  # assume 15% of revenue touched by website
        base = size_base.get(size, 400_000) * sector_online_share
        extra_seconds = max(0, (load_time_ms - 1000) / 1000)
        loss_rate = min(0.7, extra_seconds * 0.07)
        return round(base * loss_rate, -2)  # round to nearest 100€

    # ── Priority composite ────────────────────────────────────────────────────

    def _compute_priority(self, icp: float, urgency: float) -> int:
        raw = (icp * 0.55 + urgency * 0.45) * 100
        return max(0, min(100, round(raw)))

    def _assign_tier(self, score: int) -> str:
        if score >= 70:
            return "A"
        if score >= 45:
            return "B"
        return "C"

    # ── Public API ────────────────────────────────────────────────────────────

    def enrich(self, fiche) -> EnrichedProspect:
        """
        Enrich a ProspectFiche (or dict-like) and return an EnrichedProspect.
        Accepts both dataclass instances (with .company_id) and dicts.
        """
        # Support both dataclass and dict inputs
        if hasattr(fiche, "__dict__"):
            data = fiche.__dict__
        elif isinstance(fiche, dict):
            data = fiche
        else:
            raise TypeError(f"Unsupported fiche type: {type(fiche)}")

        company_id = data.get("company_id", "unknown")
        name = data.get("name", "")
        sector = data.get("sector", "")
        website = data.get("website", "")
        email = data.get("contact_email", "")
        pagespeed = int(data.get("pagespeed_score", 50))
        load_time = int(data.get("load_time_ms", 3000))

        icp = self._score_icp(sector)
        urgency, urgency_label = self._score_urgency(pagespeed)
        size = self._detect_size(name, website)
        priority = self._compute_priority(icp, urgency)
        tier = self._assign_tier(priority)
        rev_impact = self._estimate_revenue_impact(load_time, sector, size)

        notes = []
        if pagespeed < 30:
            notes.append("PageSpeed critique — contact urgent recommandé")
        if icp >= 0.85:
            notes.append(f"Secteur à forte valeur ICP ({sector})")
        if rev_impact > 10_000:
            notes.append(f"Impact revenu estimé : {rev_impact:,.0f}€/an")
        if priority >= 70:
            notes.append("Priorité A — traitement immédiat")

        enriched = EnrichedProspect(
            company_id=company_id,
            name=name,
            sector=sector,
            website=website,
            contact_email=email,
            pagespeed_score=pagespeed,
            load_time_ms=load_time,
            icp_fit=round(icp, 3),
            urgency=round(urgency, 3),
            company_size=size,
            priority_score=priority,
            tier=tier,
            sector_score=icp,
            urgency_label=urgency_label,
            estimated_revenue_impact_eur=rev_impact,
            enrichment_notes=notes,
        )

        logger.debug(
            "Enriched %s — tier=%s score=%d icp=%.2f urgency=%s",
            company_id, tier, priority, icp, urgency_label,
        )
        return enriched

    def enrich_batch(self, fiches: list) -> list[EnrichedProspect]:
        """Enrich a list of prospects, sorted by priority (highest first)."""
        results = [self.enrich(f) for f in fiches]
        return sorted(results, key=lambda e: e.priority_score, reverse=True)

    def filter_priority(self, fiches: list, min_score: Optional[int] = None) -> list[EnrichedProspect]:
        """Enrich and return only prospects above the priority threshold."""
        threshold = min_score if min_score is not None else self.min_priority_threshold
        return [e for e in self.enrich_batch(fiches) if e.priority_score >= threshold]

    def get_tier_a(self, fiches: list) -> list[EnrichedProspect]:
        """Return only Tier A prospects (score ≥ 70)."""
        return [e for e in self.enrich_batch(fiches) if e.tier == "A"]
