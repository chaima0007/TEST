"""Lead Enrichment Engine — validates and enriches lead data quality for outreach."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
import math


class DataQuality(str, Enum):
    EXCELLENT = "excellent"  # >=85
    GOOD = "good"            # >=65
    FAIR = "fair"            # >=45
    POOR = "poor"            # >=25
    INCOMPLETE = "incomplete"  # <25


class EnrichmentPriority(str, Enum):
    IMMEDIATE = "immediate"    # data so poor it blocks outreach
    HIGH = "high"              # major gaps, enrichment needed before contact
    MEDIUM = "medium"          # some gaps, enrichment beneficial
    LOW = "low"                # minor gaps, can reach out now
    NONE = "none"              # data complete, proceed


class LeadSource(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    REFERRAL = "referral"
    EVENT = "event"
    CONTENT = "content"
    PAID = "paid"


_FIELD_WEIGHTS = {
    # Contact fields (40%)
    "has_email": 12,
    "has_phone": 8,
    "has_linkedin": 10,
    "has_job_title": 10,
    # Company fields (35%)
    "has_company_name": 8,
    "has_industry": 8,
    "has_company_size": 7,
    "has_annual_revenue": 7,
    "has_website": 5,
    # Intent signals (25%)
    "has_pain_point": 8,
    "has_use_case": 7,
    "has_budget_signal": 5,
    "has_timeline": 5,
}


@dataclass
class LeadInput:
    lead_id: str
    lead_name: str
    source: LeadSource

    # Contact fields
    email: str = ""
    phone: str = ""
    linkedin_url: str = ""
    job_title: str = ""

    # Company fields
    company_name: str = ""
    industry: str = ""
    company_size_employees: int = 0   # 0 = unknown
    annual_revenue_eur: float = 0.0   # 0 = unknown
    website: str = ""

    # Intent signals
    pain_point_identified: str = ""
    use_case_identified: str = ""
    budget_signal: str = ""           # e.g. "confirmed", "hinted", ""
    timeline_identified: str = ""     # e.g. "Q1 2026", ""

    # Engagement
    email_opens: int = 0
    website_visits: int = 0
    content_downloads: int = 0
    events_attended: int = 0

    # Quality flags
    is_verified_email: bool = False
    is_duplicate: bool = False
    is_unsubscribed: bool = False
    bounce_history: int = 0           # previous bounces

    # Firmographic validation
    domain_match: bool = True         # email domain matches company
    seniority_level: str = ""         # c_suite / vp / director / manager / individual


@dataclass
class EnrichmentGap:
    field: str
    description: str
    impact_score: int                 # how much this gap costs in data quality


@dataclass
class LeadResult:
    lead_id: str
    lead_name: str
    source: LeadSource
    data_quality: DataQuality
    quality_score: float
    contact_score: float
    company_score: float
    intent_score: float
    engagement_score: float
    enrichment_priority: EnrichmentPriority
    gaps: list[EnrichmentGap]
    outreach_ready: bool
    quality_signals: list[str]
    risk_flags: list[str]
    suggested_enrichment_sources: list[str]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["data_quality"] = self.data_quality.value
        d["enrichment_priority"] = self.enrichment_priority.value
        d["source"] = self.source.value
        return d


def _has(val: str | float | int) -> bool:
    if isinstance(val, str):
        return bool(val.strip())
    if isinstance(val, (int, float)):
        return val > 0
    return bool(val)


def _contact_score(inp: LeadInput) -> tuple[float, list[EnrichmentGap]]:
    gaps: list[EnrichmentGap] = []
    score = 0.0
    checks = [
        ("has_email", _has(inp.email), "Email manquant — impossible de contacter", 12),
        ("has_phone", _has(inp.phone), "Téléphone manquant — canal de contact limité", 8),
        ("has_linkedin", _has(inp.linkedin_url), "LinkedIn manquant — social selling impossible", 10),
        ("has_job_title", _has(inp.job_title), "Titre manquant — personnalisation impossible", 10),
    ]
    for key, present, desc, weight in checks:
        if present:
            score += weight
        else:
            gaps.append(EnrichmentGap(field=key, description=desc, impact_score=weight))

    total_weight = sum(w for _, _, _, w in checks)
    return round(score / total_weight * 100, 2), gaps


def _company_score(inp: LeadInput) -> tuple[float, list[EnrichmentGap]]:
    gaps: list[EnrichmentGap] = []
    score = 0.0
    checks = [
        ("has_company_name", _has(inp.company_name), "Entreprise manquante — contexte inconnu", 8),
        ("has_industry", _has(inp.industry), "Secteur manquant — segmentation impossible", 8),
        ("has_company_size", inp.company_size_employees > 0, "Taille entreprise manquante — ICP inconnu", 7),
        ("has_annual_revenue", inp.annual_revenue_eur > 0, "CA annuel manquant — potentiel deal inconnu", 7),
        ("has_website", _has(inp.website), "Site web manquant — impossible de valider l'entreprise", 5),
    ]
    for key, present, desc, weight in checks:
        if present:
            score += weight
        else:
            gaps.append(EnrichmentGap(field=key, description=desc, impact_score=weight))

    total_weight = sum(w for _, _, _, w in checks)
    return round(score / total_weight * 100, 2), gaps


def _intent_score_fn(inp: LeadInput) -> tuple[float, list[EnrichmentGap]]:
    gaps: list[EnrichmentGap] = []
    score = 0.0
    checks = [
        ("has_pain_point", _has(inp.pain_point_identified), "Point de douleur non identifié", 8),
        ("has_use_case", _has(inp.use_case_identified), "Cas d'usage non identifié", 7),
        ("has_budget_signal", _has(inp.budget_signal), "Signal budget absent", 5),
        ("has_timeline", _has(inp.timeline_identified), "Timeline non identifiée", 5),
    ]
    for key, present, desc, weight in checks:
        if present:
            score += weight
        else:
            gaps.append(EnrichmentGap(field=key, description=desc, impact_score=weight))

    total_weight = sum(w for _, _, _, w in checks)
    return round(score / total_weight * 100, 2), gaps


def _engagement_score(inp: LeadInput) -> float:
    score = 0.0
    score += min(30, inp.email_opens * 6)
    score += min(25, inp.website_visits * 5)
    score += min(25, inp.content_downloads * 12)
    score += min(20, inp.events_attended * 20)
    return round(min(100, score), 2)


def _quality_score(contact: float, company: float, intent: float, engagement: float) -> float:
    return round(contact * 0.35 + company * 0.30 + intent * 0.20 + engagement * 0.15, 2)


def _data_quality(score: float) -> DataQuality:
    if score >= 85:
        return DataQuality.EXCELLENT
    if score >= 65:
        return DataQuality.GOOD
    if score >= 45:
        return DataQuality.FAIR
    if score >= 25:
        return DataQuality.POOR
    return DataQuality.INCOMPLETE


def _enrichment_priority(quality: DataQuality, has_email: bool, is_unsubscribed: bool) -> EnrichmentPriority:
    if is_unsubscribed:
        return EnrichmentPriority.NONE  # don't enrich — don't contact
    if not has_email and quality in (DataQuality.INCOMPLETE, DataQuality.POOR):
        return EnrichmentPriority.IMMEDIATE
    if quality == DataQuality.INCOMPLETE:
        return EnrichmentPriority.IMMEDIATE
    if quality == DataQuality.POOR:
        return EnrichmentPriority.HIGH
    if quality == DataQuality.FAIR:
        return EnrichmentPriority.MEDIUM
    if quality == DataQuality.GOOD:
        return EnrichmentPriority.LOW
    return EnrichmentPriority.NONE


def _outreach_ready(inp: LeadInput, quality: DataQuality) -> bool:
    if inp.is_unsubscribed or inp.is_duplicate:
        return False
    if not _has(inp.email) and not _has(inp.linkedin_url):
        return False
    if quality == DataQuality.INCOMPLETE:
        return False
    return True


def _build_signals(inp: LeadInput, quality: DataQuality, engagement: float) -> tuple[list[str], list[str]]:
    signals: list[str] = []
    risks: list[str] = []

    if inp.is_verified_email:
        signals.append("Email vérifié — délivrabilité garantie")
    if inp.source == LeadSource.REFERRAL:
        signals.append("Lead par recommandation — taux de conversion 3x supérieur")
    if inp.source == LeadSource.INBOUND:
        signals.append("Lead entrant — forte intention d'achat")
    if engagement >= 70:
        signals.append(f"Très haut engagement — {inp.email_opens} ouvertures, {inp.website_visits} visites")
    elif engagement >= 40:
        signals.append("Engagement modéré — lead tiède, à relancer")
    if _has(inp.pain_point_identified):
        signals.append(f"Point de douleur identifié : {inp.pain_point_identified[:50]}")
    if _has(inp.budget_signal):
        signals.append("Signal budget capté — décision proche")
    if inp.seniority_level in ("c_suite", "vp"):
        signals.append(f"Décideur de haut niveau identifié ({inp.seniority_level})")
    if inp.content_downloads >= 2:
        signals.append(f"{inp.content_downloads} téléchargements de contenu — intérêt prouvé")

    if inp.is_duplicate:
        risks.append("Lead dupliqué — déprioritiser, déjà dans le CRM")
    if inp.is_unsubscribed:
        risks.append("Désabonné — ne pas contacter (RGPD / CAN-SPAM)")
    if inp.bounce_history >= 2:
        risks.append(f"{inp.bounce_history} bounces antérieurs — vérifier l'email")
    if not inp.domain_match and _has(inp.email) and _has(inp.company_name):
        risks.append("Domaine email ne correspond pas à l'entreprise — valider l'identité")
    if not inp.is_verified_email and _has(inp.email):
        risks.append("Email non vérifié — risque de bounce")
    if quality in (DataQuality.POOR, DataQuality.INCOMPLETE):
        risks.append("Données insuffisantes — enrichissement obligatoire avant contact")

    return signals, risks


def _enrichment_sources(gaps: list[EnrichmentGap]) -> list[str]:
    sources: list[str] = []
    gap_fields = {g.field for g in gaps}

    if "has_linkedin" in gap_fields or "has_job_title" in gap_fields:
        sources.append("LinkedIn Sales Navigator — trouver profil et titre")
    if "has_email" in gap_fields:
        sources.append("Hunter.io / Apollo.io — trouver email professionnel")
    if "has_phone" in gap_fields:
        sources.append("Lusha / ZoomInfo — trouver numéro direct")
    if "has_company_size" in gap_fields or "has_annual_revenue" in gap_fields:
        sources.append("Clearbit / Apollo — enrichissement firmographique")
    if "has_industry" in gap_fields or "has_website" in gap_fields:
        sources.append("Crunchbase / LinkedIn Company — valider secteur")
    if "has_pain_point" in gap_fields or "has_use_case" in gap_fields:
        sources.append("Gong / Chorus — analyser les appels de découverte précédents")

    return list(dict.fromkeys(sources))  # deduplicate while preserving order


class LeadEnrichmentEngine:
    """Validates and scores lead data quality, identifies gaps, and recommends enrichment."""

    def __init__(self) -> None:
        self._results: dict[str, LeadResult] = {}

    def enrich(self, inp: LeadInput) -> LeadResult:
        contact, contact_gaps = _contact_score(inp)
        company, company_gaps = _company_score(inp)
        intent, intent_gaps = _intent_score_fn(inp)
        engagement = _engagement_score(inp)
        quality_score = _quality_score(contact, company, intent, engagement)
        quality = _data_quality(quality_score)
        priority = _enrichment_priority(quality, _has(inp.email), inp.is_unsubscribed)
        ready = _outreach_ready(inp, quality)
        signals, risks = _build_signals(inp, quality, engagement)
        all_gaps = contact_gaps + company_gaps + intent_gaps
        sources = _enrichment_sources(all_gaps)

        result = LeadResult(
            lead_id=inp.lead_id,
            lead_name=inp.lead_name,
            source=inp.source,
            data_quality=quality,
            quality_score=round(quality_score, 2),
            contact_score=contact,
            company_score=company,
            intent_score=intent,
            engagement_score=engagement,
            enrichment_priority=priority,
            gaps=all_gaps,
            outreach_ready=ready,
            quality_signals=signals,
            risk_flags=risks,
            suggested_enrichment_sources=sources,
        )
        self._results[inp.lead_id] = result
        return result

    def enrich_batch(self, inputs: list[LeadInput]) -> list[LeadResult]:
        return sorted([self.enrich(inp) for inp in inputs], key=lambda r: r.quality_score, reverse=True)

    def get(self, lead_id: str) -> Optional[LeadResult]:
        return self._results.get(lead_id)

    def all_leads(self) -> list[LeadResult]:
        return sorted(self._results.values(), key=lambda r: r.quality_score, reverse=True)

    def by_quality(self, quality: DataQuality) -> list[LeadResult]:
        return [r for r in self.all_leads() if r.data_quality == quality]

    def outreach_ready(self) -> list[LeadResult]:
        return [r for r in self.all_leads() if r.outreach_ready]

    def needs_enrichment(self) -> list[LeadResult]:
        return [
            r for r in self.all_leads()
            if r.enrichment_priority in (EnrichmentPriority.IMMEDIATE, EnrichmentPriority.HIGH)
        ]

    def excellent_leads(self) -> list[LeadResult]:
        return self.by_quality(DataQuality.EXCELLENT)

    def incomplete_leads(self) -> list[LeadResult]:
        return self.by_quality(DataQuality.INCOMPLETE)

    def top_n(self, n: int = 10) -> list[LeadResult]:
        return self.all_leads()[:n]

    def summary(self) -> dict:
        all_r = self.all_leads()
        if not all_r:
            return {
                "total": 0,
                "quality_counts": {},
                "priority_counts": {},
                "avg_quality_score": 0.0,
                "outreach_ready_count": 0,
                "needs_enrichment_count": 0,
            }
        quality_counts: dict[str, int] = {}
        priority_counts: dict[str, int] = {}
        total_score = 0.0
        for r in all_r:
            quality_counts[r.data_quality.value] = quality_counts.get(r.data_quality.value, 0) + 1
            priority_counts[r.enrichment_priority.value] = priority_counts.get(r.enrichment_priority.value, 0) + 1
            total_score += r.quality_score
        return {
            "total": len(all_r),
            "quality_counts": quality_counts,
            "priority_counts": priority_counts,
            "avg_quality_score": round(total_score / len(all_r), 1),
            "outreach_ready_count": len(self.outreach_ready()),
            "needs_enrichment_count": len(self.needs_enrichment()),
        }

    def reset(self) -> None:
        self._results.clear()
