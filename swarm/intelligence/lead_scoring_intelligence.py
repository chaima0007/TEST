"""Module 23 — Lead Scoring Intelligence Engine."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class LeadTier(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"
    DEAD = "dead"


class LeadAction(str, Enum):
    CALL_NOW = "call_now"
    NURTURE = "nurture"
    QUALIFY = "qualify"
    DISQUALIFY = "disqualify"
    ASSIGN_AE = "assign_ae"


class FitScore(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class IntentSignal(str, Enum):
    HIGH_INTENT = "high_intent"
    MEDIUM_INTENT = "medium_intent"
    LOW_INTENT = "low_intent"
    NO_INTENT = "no_intent"


@dataclass
class LeadProfile:
    lead_id: str
    company: str
    contact_name: str
    segment: str
    # ICP fit signals (0-100)
    icp_industry_match: bool
    icp_size_match: bool          # headcount in target range
    icp_revenue_match: bool       # revenue in target range
    icp_geography_match: bool
    tech_stack_match: bool        # uses compatible technologies
    # Engagement signals
    website_visits: int           # last 30 days
    email_opens: int              # last 30 days
    email_clicks: int             # last 30 days
    content_downloads: int        # whitepapers, case studies
    demo_requested: bool
    pricing_page_visits: int
    # Qualification signals
    budget_confirmed: bool
    authority_confirmed: bool     # DM or influencer reached
    need_confirmed: bool
    timeline_confirmed: bool      # active timeline <6 months
    # Negative signals
    competitor_customer: bool
    out_of_territory: bool
    unsubscribed: bool
    # Contextual
    days_in_funnel: int           # 0 = fresh lead
    lead_source: str              # inbound/outbound/referral/event/content


@dataclass
class LeadScoringResult:
    lead_id: str
    company: str
    contact_name: str
    segment: str
    lead_source: str
    lead_score: float            # 0-100
    fit_score_label: FitScore
    intent_signal: IntentSignal
    tier: LeadTier
    action: LeadAction
    fit_breakdown: dict          # icp/engagement/qualification breakdown
    strengths: list[str]
    weaknesses: list[str]
    recommended_steps: list[str]
    disqualification_reasons: list[str]

    def to_dict(self) -> dict:
        return {
            "lead_id": self.lead_id,
            "company": self.company,
            "contact_name": self.contact_name,
            "segment": self.segment,
            "lead_source": self.lead_source,
            "lead_score": self.lead_score,
            "fit_score_label": self.fit_score_label.value,
            "intent_signal": self.intent_signal.value,
            "tier": self.tier.value,
            "action": self.action.value,
            "fit_breakdown": self.fit_breakdown,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "recommended_steps": self.recommended_steps,
            "disqualification_reasons": self.disqualification_reasons,
        }


def _icp_score(lead: LeadProfile) -> float:
    """ICP fit contributes 35 points."""
    pts = 0.0
    if lead.icp_industry_match:
        pts += 10
    if lead.icp_size_match:
        pts += 8
    if lead.icp_revenue_match:
        pts += 8
    if lead.icp_geography_match:
        pts += 5
    if lead.tech_stack_match:
        pts += 4
    return pts


def _engagement_score(lead: LeadProfile) -> float:
    """Engagement contributes 35 points."""
    pts = 0.0
    # Website visits: up to 10 pts
    if lead.website_visits >= 10:
        pts += 10
    elif lead.website_visits >= 5:
        pts += 6
    elif lead.website_visits >= 2:
        pts += 3
    # Email engagement: up to 8 pts
    email_eng = lead.email_opens + lead.email_clicks * 2
    if email_eng >= 10:
        pts += 8
    elif email_eng >= 5:
        pts += 5
    elif email_eng >= 2:
        pts += 2
    # Content / demo: up to 10 pts
    if lead.demo_requested:
        pts += 6
    if lead.content_downloads >= 2:
        pts += 4
    elif lead.content_downloads == 1:
        pts += 2
    # Pricing page: up to 7 pts
    if lead.pricing_page_visits >= 3:
        pts += 7
    elif lead.pricing_page_visits >= 1:
        pts += 4
    return pts


def _qualification_score(lead: LeadProfile) -> float:
    """BANT qualification contributes 30 points."""
    pts = 0.0
    if lead.budget_confirmed:
        pts += 10
    if lead.authority_confirmed:
        pts += 8
    if lead.need_confirmed:
        pts += 8
    if lead.timeline_confirmed:
        pts += 4
    return pts


def _compute_lead_score(lead: LeadProfile) -> tuple[float, dict]:
    icp = _icp_score(lead)
    eng = _engagement_score(lead)
    qual = _qualification_score(lead)
    raw = icp + eng + qual
    # Negative deductions
    if lead.competitor_customer:
        raw -= 15
    if lead.out_of_territory:
        raw -= 20
    if lead.unsubscribed:
        raw -= 25
    # Stale lead penalty
    if lead.days_in_funnel > 180:
        raw -= 10
    elif lead.days_in_funnel > 90:
        raw -= 5
    score = max(0.0, min(100.0, round(raw, 1)))
    breakdown = {
        "icp": round(icp, 1),
        "engagement": round(eng, 1),
        "qualification": round(qual, 1),
    }
    return score, breakdown


def _fit_score_label(icp: float) -> FitScore:
    if icp >= 30:
        return FitScore.EXCELLENT
    if icp >= 20:
        return FitScore.GOOD
    if icp >= 10:
        return FitScore.FAIR
    return FitScore.POOR


def _intent_signal(eng: float, demo: bool, pricing: int) -> IntentSignal:
    if demo or pricing >= 3 or eng >= 25:
        return IntentSignal.HIGH_INTENT
    if pricing >= 1 or eng >= 12:
        return IntentSignal.MEDIUM_INTENT
    if eng >= 5:
        return IntentSignal.LOW_INTENT
    return IntentSignal.NO_INTENT


def _tier(score: float) -> LeadTier:
    if score >= 70:
        return LeadTier.HOT
    if score >= 45:
        return LeadTier.WARM
    if score >= 20:
        return LeadTier.COLD
    return LeadTier.DEAD


def _action(
    tier: LeadTier,
    lead: LeadProfile,
    intent: IntentSignal,
) -> LeadAction:
    # Hard disqualifiers
    if lead.out_of_territory or lead.unsubscribed:
        return LeadAction.DISQUALIFY
    if tier == LeadTier.DEAD:
        return LeadAction.DISQUALIFY
    if tier == LeadTier.HOT and intent == IntentSignal.HIGH_INTENT:
        return LeadAction.CALL_NOW
    if tier == LeadTier.HOT:
        return LeadAction.ASSIGN_AE
    if tier == LeadTier.WARM and lead.budget_confirmed and lead.authority_confirmed:
        return LeadAction.QUALIFY
    if tier == LeadTier.WARM:
        return LeadAction.NURTURE
    # COLD
    if intent in (IntentSignal.MEDIUM_INTENT, IntentSignal.HIGH_INTENT):
        return LeadAction.NURTURE
    return LeadAction.DISQUALIFY


def _strengths(lead: LeadProfile, breakdown: dict) -> list[str]:
    out: list[str] = []
    if lead.icp_industry_match:
        out.append("Industrie alignée avec l'ICP cible")
    if lead.icp_size_match and lead.icp_revenue_match:
        out.append("Taille et revenu dans la cible — fit entreprise fort")
    if lead.tech_stack_match:
        out.append("Stack technologique compatible — intégration facilitée")
    if lead.demo_requested:
        out.append("Demo demandée — intention d'achat manifeste")
    if lead.pricing_page_visits >= 3:
        out.append("Visites répétées page tarifs — evaluation active")
    if lead.budget_confirmed:
        out.append("Budget confirmé — deal qualifiable immédiatement")
    if lead.authority_confirmed:
        out.append("Décideur identifié et engagé")
    if lead.need_confirmed and lead.timeline_confirmed:
        out.append("Besoin + timeline confirmés — deal en cours de qualification")
    if lead.lead_source == "referral":
        out.append("Lead issu de recommandation — taux de conversion x2")
    return out


def _weaknesses(lead: LeadProfile, breakdown: dict) -> list[str]:
    out: list[str] = []
    if not lead.icp_industry_match:
        out.append("Industrie hors ICP — fit produit non confirmé")
    if not lead.icp_size_match or not lead.icp_revenue_match:
        out.append("Profil entreprise hors cible (taille/revenu)")
    if breakdown["engagement"] < 5:
        out.append("Engagement très faible — lead non activé")
    if not lead.budget_confirmed:
        out.append("Budget non confirmé — risque disqualification BANT")
    if not lead.authority_confirmed:
        out.append("Décideur non identifié — accès au sponsor requis")
    if lead.competitor_customer:
        out.append("Client concurrent — switching cost élevé")
    if lead.days_in_funnel > 90:
        out.append("Lead vieux (>90j) — risque d'attrition")
    if not lead.need_confirmed:
        out.append("Besoin non confirmé — qualification discovery nécessaire")
    return out


def _recommended_steps(lead: LeadProfile, action: LeadAction, tier: LeadTier) -> list[str]:
    if action == LeadAction.DISQUALIFY:
        return [
            "Archiver le lead — critères de disqualification atteints",
            "Notifier le BDR pour mise à jour CRM",
        ]
    if action == LeadAction.CALL_NOW:
        return [
            "Appel de qualification immédiat — profil HOT avec forte intention",
            "Préparer deck personnalisé ROI selon l'industrie",
            "Identifier et confirmer le sponsor exécutif",
            "Proposer une demo technique dans les 48h",
        ]
    if action == LeadAction.ASSIGN_AE:
        return [
            "Assigner à un AE senior — lead HOT qualifiable",
            "Transférer contexte complet et historique d'engagement",
            "Organiser une réunion de découverte approfondie",
            "Préparer une proposition commerciale sous 5 jours",
        ]
    if action == LeadAction.QUALIFY:
        return [
            "Appel de qualification BANT — valider budget et timeline",
            "Confirmer le besoin métier et les critères de succès",
            "Identifier les parties prenantes clés",
            "Envoyer étude de cas sectorielle pertinente",
        ]
    # NURTURE
    return [
        "Intégrer dans une séquence nurture ciblée",
        "Envoyer du contenu éducatif adapté au secteur",
        "Relancer dans 2 semaines avec un angle business",
        "Monitorer les signaux d'intention (visites site, emails)",
    ]


def _disqualification_reasons(lead: LeadProfile) -> list[str]:
    reasons: list[str] = []
    if lead.out_of_territory:
        reasons.append("Hors territoire de vente")
    if lead.unsubscribed:
        reasons.append("Désinscrit — contact bloqué")
    if lead.competitor_customer:
        reasons.append("Client concurrent actif")
    if not lead.icp_industry_match and not lead.icp_size_match:
        reasons.append("Profil entièrement hors ICP")
    return reasons


class LeadScoringIntelligenceEngine:
    """Scores and prioritises leads using ICP fit + engagement + BANT signals."""

    def __init__(self) -> None:
        self._leads: dict[str, LeadScoringResult] = {}

    def score(self, lead: LeadProfile) -> LeadScoringResult:
        lead_score, breakdown = _compute_lead_score(lead)
        icp = breakdown["icp"]
        eng = breakdown["engagement"]
        fit_label = _fit_score_label(icp)
        intent = _intent_signal(eng, lead.demo_requested, lead.pricing_page_visits)
        tier = _tier(lead_score)
        action = _action(tier, lead, intent)

        result = LeadScoringResult(
            lead_id=lead.lead_id,
            company=lead.company,
            contact_name=lead.contact_name,
            segment=lead.segment,
            lead_source=lead.lead_source,
            lead_score=lead_score,
            fit_score_label=fit_label,
            intent_signal=intent,
            tier=tier,
            action=action,
            fit_breakdown=breakdown,
            strengths=_strengths(lead, breakdown),
            weaknesses=_weaknesses(lead, breakdown),
            recommended_steps=_recommended_steps(lead, action, tier),
            disqualification_reasons=_disqualification_reasons(lead),
        )
        self._leads[lead.lead_id] = result
        return result

    def score_batch(self, leads: list[LeadProfile]) -> list[LeadScoringResult]:
        results = [self.score(l) for l in leads]
        return sorted(results, key=lambda r: r.lead_score, reverse=True)

    # ── Read helpers ─────────────────────────────────────────────────────────

    def all_leads(self) -> list[LeadScoringResult]:
        return sorted(self._leads.values(), key=lambda r: r.lead_score, reverse=True)

    def by_tier(self, tier: LeadTier) -> list[LeadScoringResult]:
        return [r for r in self.all_leads() if r.tier == tier]

    def by_action(self, action: LeadAction) -> list[LeadScoringResult]:
        return [r for r in self.all_leads() if r.action == action]

    def by_intent(self, intent: IntentSignal) -> list[LeadScoringResult]:
        return [r for r in self.all_leads() if r.intent_signal == intent]

    def hot_leads(self) -> list[LeadScoringResult]:
        return self.by_tier(LeadTier.HOT)

    def disqualified(self) -> list[LeadScoringResult]:
        return self.by_action(LeadAction.DISQUALIFY)

    def call_now(self) -> list[LeadScoringResult]:
        return self.by_action(LeadAction.CALL_NOW)

    def high_intent(self) -> list[LeadScoringResult]:
        return self.by_intent(IntentSignal.HIGH_INTENT)

    def avg_lead_score(self) -> float:
        leads = list(self._leads.values())
        if not leads:
            return 0.0
        return round(sum(r.lead_score for r in leads) / len(leads), 1)

    def hot_rate(self) -> float:
        leads = list(self._leads.values())
        if not leads:
            return 0.0
        return round(len(self.hot_leads()) / len(leads) * 100, 1)

    def summary(self) -> dict:
        leads = list(self._leads.values())
        n = len(leads)
        tier_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        intent_counts: dict[str, int] = {}
        fit_counts: dict[str, int] = {}
        for r in leads:
            tier_counts[r.tier.value] = tier_counts.get(r.tier.value, 0) + 1
            action_counts[r.action.value] = action_counts.get(r.action.value, 0) + 1
            intent_counts[r.intent_signal.value] = intent_counts.get(r.intent_signal.value, 0) + 1
            fit_counts[r.fit_score_label.value] = fit_counts.get(r.fit_score_label.value, 0) + 1
        return {
            "total": n,
            "tier_counts": tier_counts,
            "action_counts": action_counts,
            "intent_counts": intent_counts,
            "fit_counts": fit_counts,
            "avg_lead_score": self.avg_lead_score(),
            "hot_rate_pct": self.hot_rate(),
            "hot_count": len(self.hot_leads()),
            "call_now_count": len(self.call_now()),
            "disqualified_count": len(self.disqualified()),
        }

    def reset(self) -> None:
        self._leads.clear()
