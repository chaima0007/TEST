"""Module 43 — Buyer Intent Intelligence Engine

Aggregates and scores digital, behavioural, and event-driven buying signals
to determine a prospect's intent level, readiness to engage, and recommended
outreach strategy.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class IntentLevel(str, Enum):
    HOT         = "hot"          # strong buying signals — immediate outreach
    WARM        = "warm"         # moderate intent — nurture with value content
    LUKEWARM    = "lukewarm"     # early interest — light touch cadence
    COLD        = "cold"         # low or no intent — awareness plays only
    UNKNOWN     = "unknown"      # insufficient data to score


class IntentCategory(str, Enum):
    PRODUCT_INTEREST   = "product_interest"   # researching specific product/feature
    COMPETITIVE_EVAL   = "competitive_eval"   # comparing vendors / RFP stage
    BUDGET_CYCLE       = "budget_cycle"       # triggered by budget planning activity
    PAIN_DRIVEN        = "pain_driven"        # reacting to a business pain or event
    RELATIONSHIP       = "relationship"       # engagement driven by existing relationship
    EVENT_TRIGGERED    = "event_triggered"    # triggered by external event (funding, M&A, etc.)


class IntentTrend(str, Enum):
    ACCELERATING = "accelerating"   # intent increasing week-over-week
    STABLE       = "stable"         # consistent level
    DECLINING    = "declining"      # intent dropping — urgency fading
    SPIKED       = "spiked"         # sudden large increase this week
    DORMANT      = "dormant"        # was active, now silent


class OutreachStrategy(str, Enum):
    IMMEDIATE_OUTREACH  = "immediate_outreach"   # reach out today — hot window
    EXECUTIVE_OUTREACH  = "executive_outreach"   # senior level contact needed
    VALUE_CONTENT       = "value_content"        # send targeted content
    NURTURE_SEQUENCE    = "nurture_sequence"     # enrol in nurture cadence
    EVENT_INVITE        = "event_invite"         # invite to webinar/event
    WAIT_AND_MONITOR    = "wait_and_monitor"     # not ready — monitor signals


# ─── Input ────────────────────────────────────────────────────────────────────

@dataclass
class IntentInput:
    prospect_id: str
    company_name: str
    rep_id: str
    rep_name: str
    # Digital signals
    website_visits_30d: int
    pricing_page_visits: int
    demo_page_visits: int
    case_study_downloads: int
    whitepaper_downloads: int
    product_video_views: int
    # Email engagement
    emails_opened_30d: int
    emails_clicked_30d: int
    emails_sent_30d: int
    # Event signals
    webinar_attended: bool
    trade_show_visited: bool
    free_trial_started: bool
    # Relationship signals
    linkedin_engaged: bool
    replied_to_outreach: bool
    requested_demo: bool
    contacted_support: bool
    # External triggers
    funding_round_announced: bool
    leadership_change: bool
    competitor_contract_expired: bool
    recent_job_posting_relevant: bool    # hiring roles related to our product
    # Historical
    previous_demo_taken: bool
    previous_trial_abandoned: bool
    days_since_last_engagement: int
    # ICP fit
    icp_score: float                     # 0–100


# ─── Output ───────────────────────────────────────────────────────────────────

@dataclass
class IntentResult:
    prospect_id: str
    company_name: str
    rep_id: str
    rep_name: str
    intent_level: str
    intent_category: str
    intent_trend: str
    outreach_strategy: str
    intent_score: float          # 0–100 composite
    digital_score: float         # 0–100 web + content signals
    engagement_score: float      # 0–100 email + event + relationship
    trigger_score: float         # 0–100 external trigger signals
    hot_signals: list[str]
    cold_signals: list[str]
    recommended_actions: list[str]

    def to_dict(self) -> dict:
        return {
            "prospect_id":         self.prospect_id,
            "company_name":        self.company_name,
            "rep_id":              self.rep_id,
            "rep_name":            self.rep_name,
            "intent_level":        self.intent_level,
            "intent_category":     self.intent_category,
            "intent_trend":        self.intent_trend,
            "outreach_strategy":   self.outreach_strategy,
            "intent_score":        self.intent_score,
            "digital_score":       self.digital_score,
            "engagement_score":    self.engagement_score,
            "trigger_score":       self.trigger_score,
            "hot_signals":         self.hot_signals,
            "cold_signals":        self.cold_signals,
            "recommended_actions": self.recommended_actions,
        }


# ─── Engine ───────────────────────────────────────────────────────────────────

class BuyerIntentEngine:

    def __init__(self) -> None:
        self._results: list[IntentResult] = []

    # ── Sub-scores ─────────────────────────────────────────────────────────────

    def _digital_score(self, inp: IntentInput) -> float:
        score = 0.0
        # High-intent pages
        score += min(25, inp.pricing_page_visits * 12)
        score += min(20, inp.demo_page_visits * 10)
        # Content engagement
        score += min(15, inp.case_study_downloads * 7)
        score += min(10, inp.whitepaper_downloads * 5)
        score += min(8,  inp.product_video_views * 2)
        # General web traffic (diminishing returns)
        score += min(12, inp.website_visits_30d * 0.5)
        # Free trial = very high signal
        if inp.free_trial_started: score += 20
        return min(100.0, score)

    def _engagement_score(self, inp: IntentInput) -> float:
        score = 0.0
        # Requested demo = strongest signal
        if inp.requested_demo:      score += 30
        if inp.replied_to_outreach: score += 20
        if inp.webinar_attended:    score += 15
        if inp.trade_show_visited:  score += 12
        if inp.linkedin_engaged:    score += 8
        if inp.contacted_support:   score += 5
        # Email engagement
        if inp.emails_sent_30d > 0:
            open_rate  = inp.emails_opened_30d / inp.emails_sent_30d
            click_rate = inp.emails_clicked_30d / inp.emails_sent_30d
            score += min(5, open_rate * 8)
            score += min(8, click_rate * 20)
        # Historical signals
        if inp.previous_demo_taken:      score += 8
        if inp.previous_trial_abandoned: score += 5
        # Recency penalty
        if inp.days_since_last_engagement > 30:  score -= 15
        elif inp.days_since_last_engagement > 14: score -= 5
        return max(0.0, min(100.0, score))

    def _trigger_score(self, inp: IntentInput) -> float:
        score = 0.0
        if inp.funding_round_announced:         score += 30
        if inp.competitor_contract_expired:     score += 25
        if inp.leadership_change:               score += 20
        if inp.recent_job_posting_relevant:     score += 15
        return min(100.0, score)

    def _intent_score(
        self, digital: float, engagement: float, trigger: float, inp: IntentInput
    ) -> float:
        base = digital * 0.35 + engagement * 0.45 + trigger * 0.20
        # ICP multiplier: high ICP amplifies all signals
        icp_boost = (inp.icp_score - 50) * 0.1   # +/- up to 5 pts per 10 ICP pts
        return max(0.0, min(100.0, round(base + icp_boost, 1)))

    # ── Classification ─────────────────────────────────────────────────────────

    def _intent_level(self, score: float) -> IntentLevel:
        if score >= 70:   return IntentLevel.HOT
        if score >= 45:   return IntentLevel.WARM
        if score >= 20:   return IntentLevel.LUKEWARM
        if score >= 5:    return IntentLevel.COLD
        return IntentLevel.UNKNOWN

    def _intent_category(self, inp: IntentInput) -> IntentCategory:
        if inp.requested_demo or inp.free_trial_started:
            return IntentCategory.PRODUCT_INTEREST
        if inp.pricing_page_visits >= 2 or inp.case_study_downloads >= 2:
            return IntentCategory.COMPETITIVE_EVAL
        if inp.funding_round_announced or inp.competitor_contract_expired:
            return IntentCategory.EVENT_TRIGGERED
        if inp.leadership_change or inp.recent_job_posting_relevant:
            return IntentCategory.PAIN_DRIVEN
        if inp.replied_to_outreach or inp.webinar_attended:
            return IntentCategory.RELATIONSHIP
        if inp.website_visits_30d >= 5:
            return IntentCategory.PRODUCT_INTEREST
        return IntentCategory.RELATIONSHIP

    def _intent_trend(self, inp: IntentInput) -> IntentTrend:
        # No engagement recently
        if inp.days_since_last_engagement > 60:
            return IntentTrend.DORMANT
        # Spike: high-intent action very recently
        if (inp.requested_demo or inp.free_trial_started or inp.funding_round_announced
                or inp.competitor_contract_expired) and inp.days_since_last_engagement <= 7:
            return IntentTrend.SPIKED
        # Strong recent engagement
        if inp.days_since_last_engagement <= 7 and (inp.website_visits_30d >= 3 or inp.emails_clicked_30d >= 1):
            return IntentTrend.ACCELERATING
        # Fading engagement
        if inp.days_since_last_engagement > 21:
            return IntentTrend.DECLINING
        return IntentTrend.STABLE

    def _outreach_strategy(
        self, level: IntentLevel, trend: IntentTrend, inp: IntentInput
    ) -> OutreachStrategy:
        if level == IntentLevel.HOT:
            if inp.funding_round_announced or inp.icp_score >= 80:
                return OutreachStrategy.EXECUTIVE_OUTREACH
            return OutreachStrategy.IMMEDIATE_OUTREACH
        if level == IntentLevel.WARM:
            if trend == IntentTrend.SPIKED:
                return OutreachStrategy.IMMEDIATE_OUTREACH
            return OutreachStrategy.VALUE_CONTENT
        if level == IntentLevel.LUKEWARM:
            if inp.webinar_attended or inp.trade_show_visited:
                return OutreachStrategy.EVENT_INVITE
            return OutreachStrategy.NURTURE_SEQUENCE
        return OutreachStrategy.WAIT_AND_MONITOR

    # ── Signal lists ───────────────────────────────────────────────────────────

    def _hot_signals(self, inp: IntentInput) -> list[str]:
        signals: list[str] = []
        if inp.requested_demo:
            signals.append("Démo demandée — signal d'achat très fort")
        if inp.free_trial_started:
            signals.append("Trial gratuit démarré — évaluation active du produit")
        if inp.funding_round_announced:
            signals.append("Levée de fonds annoncée — budget disponible, fenêtre d'opportunité ouverte")
        if inp.competitor_contract_expired:
            signals.append("Contrat concurrent expiré — prospect en recherche de solution")
        if inp.pricing_page_visits >= 2:
            signals.append(f"{inp.pricing_page_visits} visites page tarification — comparaison de prix active")
        if inp.demo_page_visits >= 2:
            signals.append(f"{inp.demo_page_visits} visites page démo — intérêt produit confirmé")
        if inp.case_study_downloads >= 1:
            signals.append(f"{inp.case_study_downloads} cas client(s) téléchargé(s) — validation par les pairs")
        if inp.leadership_change:
            signals.append("Changement de leadership — opportunité de repositionnement")
        if inp.recent_job_posting_relevant:
            signals.append("Offre d'emploi pertinente publiée — besoin business identifié")
        if inp.webinar_attended:
            signals.append("Webinaire suivi — engagement éducatif actif")
        if inp.replied_to_outreach:
            signals.append("Réponse à l'outreach — ouverture au dialogue commercial")
        return signals

    def _cold_signals(self, inp: IntentInput) -> list[str]:
        signals: list[str] = []
        if inp.days_since_last_engagement > 30:
            signals.append(f"Pas d'engagement depuis {inp.days_since_last_engagement} jours — intérêt en déclin")
        if inp.emails_opened_30d == 0 and inp.emails_sent_30d >= 3:
            signals.append("Emails non ouverts malgré plusieurs envois — désengagement email")
        if inp.icp_score < 40:
            signals.append(f"Score ICP faible ({inp.icp_score:.0f}/100) — adéquation produit-marché limitée")
        if inp.website_visits_30d == 0 and inp.emails_sent_30d > 0:
            signals.append("Aucune visite web récente — prospect non actif en recherche")
        return signals

    # ── Recommended actions ───────────────────────────────────────────────────

    def _recommended_actions(
        self, inp: IntentInput, strategy: OutreachStrategy
    ) -> list[str]:
        actions: list[str] = []
        if strategy == OutreachStrategy.IMMEDIATE_OUTREACH:
            actions.append("Appel de découverte aujourd'hui — fenêtre d'engagement optimale")
            actions.append(
                f"Personnaliser l'outreach autour de : {', '.join(self._hot_signals(inp)[:2]) if self._hot_signals(inp) else 'les signaux détectés'}"
            )
        elif strategy == OutreachStrategy.EXECUTIVE_OUTREACH:
            actions.append("Contact C-level direct — valeur stratégique à mettre en avant")
            actions.append("Préparer un executive brief personnalisé avec ROI chiffré")
        elif strategy == OutreachStrategy.VALUE_CONTENT:
            actions.append("Envoyer 1–2 cas clients ciblés sur le secteur/douleur identifiée")
            actions.append("Inviter à un prochain webinaire produit lié aux signaux détectés")
        elif strategy == OutreachStrategy.NURTURE_SEQUENCE:
            actions.append("Enrôler dans la séquence de nurture — cadence bimensuelle")
            actions.append("Partager du contenu éducatif aligné sur les besoins sectoriels")
        elif strategy == OutreachStrategy.EVENT_INVITE:
            actions.append("Inviter au prochain événement / webinaire en lien avec les besoins")
            actions.append("Personnaliser l'invitation avec les signaux d'engagement passés")
        else:
            actions.append("Surveiller les signaux — relancer si activité détectée")
            actions.append("Configurer une alerte sur les triggers externes (levée de fonds, recrutement)")
        return actions

    # ── Main analysis ──────────────────────────────────────────────────────────

    def analyze(self, inp: IntentInput) -> IntentResult:
        digital    = round(self._digital_score(inp), 1)
        engagement = round(self._engagement_score(inp), 1)
        trigger    = round(self._trigger_score(inp), 1)
        intent     = self._intent_score(digital, engagement, trigger, inp)

        level    = self._intent_level(intent)
        category = self._intent_category(inp)
        trend    = self._intent_trend(inp)
        strategy = self._outreach_strategy(level, trend, inp)

        result = IntentResult(
            prospect_id         = inp.prospect_id,
            company_name        = inp.company_name,
            rep_id              = inp.rep_id,
            rep_name            = inp.rep_name,
            intent_level        = level.value,
            intent_category     = category.value,
            intent_trend        = trend.value,
            outreach_strategy   = strategy.value,
            intent_score        = intent,
            digital_score       = digital,
            engagement_score    = engagement,
            trigger_score       = trigger,
            hot_signals         = self._hot_signals(inp),
            cold_signals        = self._cold_signals(inp),
            recommended_actions = self._recommended_actions(inp, strategy),
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[IntentInput]) -> list[IntentResult]:
        results = [self.analyze(inp) for inp in inputs]
        results.sort(key=lambda r: r.intent_score, reverse=True)
        return results

    # ── Helpers ────────────────────────────────────────────────────────────────

    def hot_prospects(self) -> list[IntentResult]:
        return [r for r in self._results if r.intent_level == IntentLevel.HOT.value]

    def spiked_this_week(self) -> list[IntentResult]:
        return [r for r in self._results if r.intent_trend == IntentTrend.SPIKED.value]

    def immediate_outreach_needed(self) -> list[IntentResult]:
        return [r for r in self._results if r.outreach_strategy in (
            OutreachStrategy.IMMEDIATE_OUTREACH.value,
            OutreachStrategy.EXECUTIVE_OUTREACH.value,
        )]

    def declining_prospects(self) -> list[IntentResult]:
        return [r for r in self._results if r.intent_trend in (
            IntentTrend.DECLINING.value, IntentTrend.DORMANT.value
        )]

    def event_triggered(self) -> list[IntentResult]:
        return [r for r in self._results if r.intent_category == IntentCategory.EVENT_TRIGGERED.value]

    def summary(self) -> dict:
        results = self._results
        n = len(results)
        if n == 0:
            return {
                "total": 0,
                "level_counts": {},
                "category_counts": {},
                "trend_counts": {},
                "strategy_counts": {},
                "avg_intent_score": 0.0,
                "avg_digital_score": 0.0,
                "avg_engagement_score": 0.0,
                "hot_count": 0,
                "immediate_outreach_count": 0,
            }
        level_counts:    dict[str, int] = {}
        category_counts: dict[str, int] = {}
        trend_counts:    dict[str, int] = {}
        strategy_counts: dict[str, int] = {}
        total_intent = total_digital = total_engagement = 0.0

        for r in results:
            level_counts[r.intent_level]       = level_counts.get(r.intent_level, 0) + 1
            category_counts[r.intent_category] = category_counts.get(r.intent_category, 0) + 1
            trend_counts[r.intent_trend]        = trend_counts.get(r.intent_trend, 0) + 1
            strategy_counts[r.outreach_strategy] = strategy_counts.get(r.outreach_strategy, 0) + 1
            total_intent    += r.intent_score
            total_digital   += r.digital_score
            total_engagement += r.engagement_score

        return {
            "total":                    n,
            "level_counts":             level_counts,
            "category_counts":          category_counts,
            "trend_counts":             trend_counts,
            "strategy_counts":          strategy_counts,
            "avg_intent_score":         round(total_intent / n, 1),
            "avg_digital_score":        round(total_digital / n, 1),
            "avg_engagement_score":     round(total_engagement / n, 1),
            "hot_count":                sum(1 for r in results if r.intent_level == IntentLevel.HOT.value),
            "immediate_outreach_count": sum(
                1 for r in results if r.outreach_strategy in (
                    OutreachStrategy.IMMEDIATE_OUTREACH.value,
                    OutreachStrategy.EXECUTIVE_OUTREACH.value,
                )
            ),
        }

    def reset(self) -> None:
        self._results = []
