"""ICP Scorer — Ideal Customer Profile fit scoring engine."""

from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class ICPTier(str, Enum):
    PERFECT = "perfect"      # >=85
    STRONG = "strong"        # >=70
    MODERATE = "moderate"    # >=50
    WEAK = "weak"            # >=30
    DISQUALIFIED = "disqualified"  # <30


class CompanySize(str, Enum):
    STARTUP = "startup"          # 1-50
    SMB = "smb"                  # 51-250
    MID_MARKET = "mid_market"    # 251-1000
    ENTERPRISE = "enterprise"    # 1001-5000
    LARGE_ENTERPRISE = "large_enterprise"  # 5000+


class OutreachRecommendation(str, Enum):
    PRIORITIZE = "prioritize"    # PERFECT + STRONG
    QUALIFY = "qualify"          # MODERATE
    DEPRIORITIZE = "deprioritize"  # WEAK
    REJECT = "reject"            # DISQUALIFIED


_SIZE_IDEAL = {
    CompanySize.STARTUP: 30,
    CompanySize.SMB: 75,
    CompanySize.MID_MARKET: 100,
    CompanySize.ENTERPRISE: 90,
    CompanySize.LARGE_ENTERPRISE: 60,
}

_INDUSTRY_SCORES = {
    "saas": 100, "software": 95, "fintech": 90, "cybersecurity": 88,
    "martech": 85, "hrtech": 80, "proptech": 75, "legaltech": 75,
    "edtech": 70, "healthtech": 70, "ecommerce": 65, "retail": 55,
    "manufacturing": 50, "logistics": 50, "consulting": 60,
    "finance": 70, "insurance": 65, "healthcare": 65, "pharma": 60,
    "telecom": 55, "media": 50, "real_estate": 45, "construction": 40,
    "agriculture": 35, "government": 30, "non_profit": 25,
}

_GROWTH_SCORES = {
    "hyper_growth": 100,   # >50% YoY
    "fast_growth": 85,     # 20-50%
    "moderate_growth": 65, # 5-20%
    "stable": 45,          # 0-5%
    "declining": 15,       # <0%
}

_TECH_STACK_BONUS = {
    "salesforce": 15, "hubspot": 12, "marketo": 10, "outreach": 10,
    "salesloft": 10, "gong": 8, "chorus": 8, "linkedin_sales_nav": 8,
    "slack": 5, "notion": 5, "jira": 5, "zendesk": 8, "intercom": 8,
}


@dataclass
class ICPInput:
    company_id: str
    company_name: str
    industry: str                        # maps to _INDUSTRY_SCORES
    company_size: CompanySize
    employee_count: int
    annual_revenue_eur: float
    growth_stage: str                    # maps to _GROWTH_SCORES
    tech_stack: list[str] = field(default_factory=list)

    # Behavioural / intent signals
    has_dedicated_sales_team: bool = False
    uses_crm: bool = False
    has_marketing_budget: bool = False
    recently_raised_funding: bool = False
    active_hiring_sales: bool = False
    visited_website: bool = False
    engaged_with_content: bool = False
    attended_event: bool = False
    competitor_customer: bool = False
    inbound_lead: bool = False

    # Strategic fit
    decision_maker_accessible: bool = False
    multi_stakeholder_buying: bool = False
    has_pain_point_match: bool = False
    budget_confirmed: bool = False
    timeline_fit: bool = False           # decision <=6 months

    # Risk flags
    high_churn_industry: bool = False
    price_sensitive: bool = False
    long_sales_cycle: bool = False


@dataclass
class ICPResult:
    company_id: str
    company_name: str
    icp_score: float
    icp_tier: ICPTier
    firmographic_score: float
    intent_score: float
    strategic_score: float
    risk_penalty: float
    outreach_recommendation: OutreachRecommendation
    fit_signals: list[str]
    risk_signals: list[str]
    estimated_deal_size_eur: float
    priority_rank: int = 0

    def to_dict(self) -> dict:
        d = asdict(self)
        d["icp_tier"] = self.icp_tier.value
        d["outreach_recommendation"] = self.outreach_recommendation.value
        return d


def _firmographic_score(inp: ICPInput) -> float:
    """Size fit (35%) + industry fit (35%) + growth stage (30%)."""
    size_score = _SIZE_IDEAL.get(inp.company_size, 50)
    industry_score = _INDUSTRY_SCORES.get(inp.industry.lower(), 40)
    growth_score = _GROWTH_SCORES.get(inp.growth_stage.lower(), 30)

    # Revenue fit bonus (normalized to 0-20 bonus on top of industry)
    rev_bonus = min(15, math.log10(max(1, inp.annual_revenue_eur / 100_000)) * 5)

    raw = size_score * 0.35 + industry_score * 0.35 + growth_score * 0.30
    return min(100, raw + rev_bonus * 0.10)


def _intent_score(inp: ICPInput) -> float:
    """Behavioural / intent signals — weighted sum capped at 100."""
    score = 0.0
    if inp.inbound_lead:
        score += 30
    if inp.has_pain_point_match:
        score += 25
    if inp.visited_website:
        score += 10
    if inp.engaged_with_content:
        score += 10
    if inp.attended_event:
        score += 8
    if inp.active_hiring_sales:
        score += 7
    if inp.recently_raised_funding:
        score += 7
    if inp.competitor_customer:
        score += 5
    if inp.uses_crm:
        score += 5
    if inp.has_dedicated_sales_team:
        score += 5
    if inp.has_marketing_budget:
        score += 5

    # Tech stack bonus (up to +15)
    tech_bonus = min(15, sum(_TECH_STACK_BONUS.get(t.lower(), 0) for t in inp.tech_stack))
    score += tech_bonus

    return min(100, score)


def _strategic_score(inp: ICPInput) -> float:
    """Strategic fit — buying signals."""
    score = 0.0
    if inp.decision_maker_accessible:
        score += 35
    if inp.has_pain_point_match:
        score += 25
    if inp.budget_confirmed:
        score += 20
    if inp.timeline_fit:
        score += 15
    if inp.multi_stakeholder_buying:
        score += 5
    return min(100, score)


def _risk_penalty(inp: ICPInput) -> float:
    """Risk deductions (returned as positive number — will subtract)."""
    penalty = 0.0
    if inp.high_churn_industry:
        penalty += 15
    if inp.price_sensitive:
        penalty += 10
    if inp.long_sales_cycle:
        penalty += 8
    return min(30, penalty)


def _estimate_deal_size(inp: ICPInput, icp_score: float) -> float:
    """Estimate deal size based on ARR, employee count, and ICP score."""
    base = inp.annual_revenue_eur * 0.008  # 0.8% of ARR as license
    employee_factor = math.log10(max(1, inp.employee_count)) * 500
    score_multiplier = 0.5 + (icp_score / 100) * 1.5
    return round(max(500, (base + employee_factor) * score_multiplier), -2)


def _build_signals(inp: ICPInput, result_tier: ICPTier) -> tuple[list[str], list[str]]:
    fit: list[str] = []
    risk: list[str] = []

    if inp.inbound_lead:
        fit.append("Lead entrant — forte intention d'achat")
    if inp.has_pain_point_match:
        fit.append("Point de douleur aligné avec notre proposition de valeur")
    if inp.budget_confirmed:
        fit.append("Budget confirmé — décision d'achat imminente")
    if inp.decision_maker_accessible:
        fit.append("Décideur accessible — cycle de vente raccourci")
    if inp.timeline_fit:
        fit.append("Timeline de décision favorable (<6 mois)")
    if inp.recently_raised_funding:
        fit.append("Financement récent — budget disponible")
    if inp.active_hiring_sales:
        fit.append("Recrutement commercial actif — en croissance")
    if inp.competitor_customer:
        fit.append("Client concurrent — opportunité de switcher")
    if inp.attended_event:
        fit.append("Participant à un événement — engagement prouvé")
    if inp.uses_crm:
        fit.append("Utilise un CRM — culture data-driven")
    if inp.engaged_with_content:
        fit.append("Engagement avec notre contenu — intérêt démontré")

    if inp.high_churn_industry:
        risk.append("Industrie à fort taux de churn — risque de non-renouvellement")
    if inp.price_sensitive:
        risk.append("Sensibilité prix élevée — négociation complexe")
    if inp.long_sales_cycle:
        risk.append("Cycle de vente long — effort commercial important")
    if result_tier == ICPTier.DISQUALIFIED:
        risk.append("Profil hors ICP — ne pas prioriser les ressources")

    return fit, risk


def _tier_from_score(score: float) -> ICPTier:
    if score >= 85:
        return ICPTier.PERFECT
    if score >= 70:
        return ICPTier.STRONG
    if score >= 50:
        return ICPTier.MODERATE
    if score >= 30:
        return ICPTier.WEAK
    return ICPTier.DISQUALIFIED


def _recommendation(tier: ICPTier) -> OutreachRecommendation:
    if tier in (ICPTier.PERFECT, ICPTier.STRONG):
        return OutreachRecommendation.PRIORITIZE
    if tier == ICPTier.MODERATE:
        return OutreachRecommendation.QUALIFY
    if tier == ICPTier.WEAK:
        return OutreachRecommendation.DEPRIORITIZE
    return OutreachRecommendation.REJECT


class ICPScorer:
    """Scores companies against Ideal Customer Profile criteria."""

    def __init__(self) -> None:
        self._results: dict[str, ICPResult] = {}

    def score(self, inp: ICPInput) -> ICPResult:
        firm = _firmographic_score(inp)
        intent = _intent_score(inp)
        strategic = _strategic_score(inp)
        penalty = _risk_penalty(inp)

        raw = firm * 0.40 + intent * 0.35 + strategic * 0.25 - penalty
        icp_score = round(max(0, min(100, raw)), 2)

        tier = _tier_from_score(icp_score)
        recommendation = _recommendation(tier)
        fit_signals, risk_signals = _build_signals(inp, tier)
        deal_size = _estimate_deal_size(inp, icp_score)

        result = ICPResult(
            company_id=inp.company_id,
            company_name=inp.company_name,
            icp_score=icp_score,
            icp_tier=tier,
            firmographic_score=round(firm, 2),
            intent_score=round(intent, 2),
            strategic_score=round(strategic, 2),
            risk_penalty=round(penalty, 2),
            outreach_recommendation=recommendation,
            fit_signals=fit_signals,
            risk_signals=risk_signals,
            estimated_deal_size_eur=deal_size,
        )
        self._results[inp.company_id] = result
        return result

    def score_batch(self, inputs: list[ICPInput]) -> list[ICPResult]:
        results = [self.score(inp) for inp in inputs]
        sorted_results = sorted(results, key=lambda r: r.icp_score, reverse=True)
        for rank, r in enumerate(sorted_results, 1):
            r.priority_rank = rank
        return sorted_results

    def get(self, company_id: str) -> Optional[ICPResult]:
        return self._results.get(company_id)

    def all_companies(self) -> list[ICPResult]:
        return sorted(self._results.values(), key=lambda r: r.icp_score, reverse=True)

    def by_tier(self, tier: ICPTier) -> list[ICPResult]:
        return [r for r in self.all_companies() if r.icp_tier == tier]

    def perfect_fit(self) -> list[ICPResult]:
        return self.by_tier(ICPTier.PERFECT)

    def strong_fit(self) -> list[ICPResult]:
        return self.by_tier(ICPTier.STRONG)

    def prioritize(self) -> list[ICPResult]:
        return [
            r for r in self.all_companies()
            if r.outreach_recommendation == OutreachRecommendation.PRIORITIZE
        ]

    def disqualified(self) -> list[ICPResult]:
        return self.by_tier(ICPTier.DISQUALIFIED)

    def top_n(self, n: int = 10) -> list[ICPResult]:
        return self.all_companies()[:n]

    def total_pipeline_eur(self) -> float:
        return round(sum(r.estimated_deal_size_eur for r in self.prioritize()), 2)

    def summary(self) -> dict:
        all_r = self.all_companies()
        if not all_r:
            return {
                "total": 0,
                "tier_counts": {},
                "avg_icp_score": 0.0,
                "total_pipeline_eur": 0.0,
            }
        tier_counts: dict[str, int] = {}
        total_score = 0.0
        for r in all_r:
            tier_counts[r.icp_tier.value] = tier_counts.get(r.icp_tier.value, 0) + 1
            total_score += r.icp_score
        return {
            "total": len(all_r),
            "tier_counts": tier_counts,
            "avg_icp_score": round(total_score / len(all_r), 1),
            "total_pipeline_eur": self.total_pipeline_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
