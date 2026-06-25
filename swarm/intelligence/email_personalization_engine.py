from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PersonalizationLevel(str, Enum):
    HYPER_PERSONALIZED = "hyper_personalized"
    HIGHLY_PERSONALIZED = "highly_personalized"
    MODERATELY_PERSONALIZED = "moderately_personalized"
    GENERIC = "generic"
    TEMPLATE = "template"


class EmailTone(str, Enum):
    EXECUTIVE = "executive"
    CONSULTATIVE = "consultative"
    CHALLENGER = "challenger"
    EDUCATIONAL = "educational"
    URGENCY = "urgency"


class SendTiming(str, Enum):
    IMMEDIATE = "immediate"
    MORNING = "morning"
    MIDDAY = "midday"
    AFTERNOON = "afternoon"
    NEXT_BUSINESS_DAY = "next_business_day"
    HOLD = "hold"


class PersonalizationAction(str, Enum):
    SEND_NOW = "send_now"
    REFINE_AND_SEND = "refine_and_send"
    REVIEW_BEFORE_SEND = "review_before_send"
    REWRITE_REQUIRED = "rewrite_required"
    HOLD = "hold"


@dataclass
class EmailPersonalizationInput:
    prospect_id: str
    campaign_id: str
    rep_id: str
    icp_score: float              # 0–100 ICP fit score
    lead_score: float             # 0–100 lead score
    buyer_intent_score: float     # 0–100 intent signal score
    seniority_level: int          # 1–5
    industry: str                 # e.g. "saas", "finance", "retail"
    company_size: str             # "smb", "mid_market", "enterprise"
    prior_emails_sent: int
    prior_open_rate: float        # 0–1
    prior_reply_rate: float       # 0–1
    prior_click_rate: float       # 0–1
    days_since_last_email: int
    has_trigger_event: bool       # funding, hiring surge, product launch, etc.
    trigger_event_type: str       # "funding", "hiring", "expansion", "none"
    persona_pain_points: int      # number of known pain points (0–5)
    personalization_tokens: int   # number of available personalization data points
    subject_line_score: float     # 0–100 predicted open score for drafted subject
    body_relevance_score: float   # 0–100 predicted relevance score for body
    sequence_position: int        # 1=first touch, 2=follow-up, etc.
    is_warm_lead: bool
    opted_out: bool


@dataclass
class EmailPersonalizationResult:
    prospect_id: str
    campaign_id: str
    rep_id: str
    personalization_score: float
    personalization_level: PersonalizationLevel
    email_tone: EmailTone
    send_timing: SendTiming
    recommended_action: PersonalizationAction
    predicted_open_rate: float
    predicted_reply_rate: float
    send_score: float
    is_ready_to_send: bool
    personalization_tips: list[str]
    subject_suggestions: list[str]
    risk_flags: list[str]
    optimization_score: float

    def to_dict(self) -> dict:
        return {
            "prospect_id":            self.prospect_id,
            "campaign_id":            self.campaign_id,
            "personalization_score":  self.personalization_score,
            "personalization_level":  self.personalization_level.value,
            "email_tone":             self.email_tone.value,
            "send_timing":            self.send_timing.value,
            "recommended_action":     self.recommended_action.value,
            "predicted_open_rate":    self.predicted_open_rate,
            "predicted_reply_rate":   self.predicted_reply_rate,
            "send_score":             self.send_score,
            "is_ready_to_send":       self.is_ready_to_send,
            "personalization_tips":   self.personalization_tips,
            "subject_suggestions":    self.subject_suggestions,
            "risk_flags":             self.risk_flags,
            "optimization_score":     self.optimization_score,
        }


class EmailPersonalizationEngine:
    def __init__(self) -> None:
        self._results: list[EmailPersonalizationResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: EmailPersonalizationInput) -> EmailPersonalizationResult:
        if inp.opted_out:
            result = EmailPersonalizationResult(
                prospect_id=inp.prospect_id,
                campaign_id=inp.campaign_id,
                rep_id=inp.rep_id,
                personalization_score=0.0,
                personalization_level=PersonalizationLevel.TEMPLATE,
                email_tone=EmailTone.EDUCATIONAL,
                send_timing=SendTiming.HOLD,
                recommended_action=PersonalizationAction.HOLD,
                predicted_open_rate=0.0,
                predicted_reply_rate=0.0,
                send_score=0.0,
                is_ready_to_send=False,
                personalization_tips=[],
                subject_suggestions=[],
                risk_flags=["Prospect opt-out — ne pas contacter"],
                optimization_score=0.0,
            )
            self._results.append(result)
            return result

        p_score  = self._personalization_score(inp)
        level    = self._personalization_level(p_score, inp)
        tone     = self._email_tone(inp)
        timing   = self._send_timing(inp)
        open_r   = self._predicted_open_rate(inp, p_score)
        reply_r  = self._predicted_reply_rate(inp, p_score)
        s_score  = self._send_score(inp, p_score, open_r, reply_r)
        action   = self._recommended_action(inp, s_score, p_score)
        opt_score = self._optimization_score(p_score, s_score)
        ready    = action in (PersonalizationAction.SEND_NOW, PersonalizationAction.REFINE_AND_SEND)
        tips     = self._personalization_tips(inp, p_score, level)
        subjects = self._subject_suggestions(inp, tone, level)
        risks    = self._risk_flags(inp, s_score, p_score)

        result = EmailPersonalizationResult(
            prospect_id=inp.prospect_id,
            campaign_id=inp.campaign_id,
            rep_id=inp.rep_id,
            personalization_score=p_score,
            personalization_level=level,
            email_tone=tone,
            send_timing=timing,
            recommended_action=action,
            predicted_open_rate=open_r,
            predicted_reply_rate=reply_r,
            send_score=s_score,
            is_ready_to_send=ready,
            personalization_tips=tips,
            subject_suggestions=subjects,
            risk_flags=risks,
            optimization_score=opt_score,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[EmailPersonalizationInput]
    ) -> list[EmailPersonalizationResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def ready_to_send(self) -> list[EmailPersonalizationResult]:
        return [r for r in self._results if r.is_ready_to_send]

    @property
    def needs_review(self) -> list[EmailPersonalizationResult]:
        return [r for r in self._results
                if r.recommended_action == PersonalizationAction.REVIEW_BEFORE_SEND]

    @property
    def held_emails(self) -> list[EmailPersonalizationResult]:
        return [r for r in self._results
                if r.recommended_action == PersonalizationAction.HOLD]

    @property
    def high_personalization(self) -> list[EmailPersonalizationResult]:
        return [r for r in self._results
                if r.personalization_level in (
                    PersonalizationLevel.HYPER_PERSONALIZED,
                    PersonalizationLevel.HIGHLY_PERSONALIZED,
                )]

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _personalization_score(self, inp: EmailPersonalizationInput) -> float:
        score = 0.0
        # Data richness
        score += min(25.0, inp.personalization_tokens * 5.0)
        # Pain points known
        score += min(15.0, inp.persona_pain_points * 3.0)
        # Intent signals
        score += inp.buyer_intent_score * 0.20
        # ICP fit
        score += inp.icp_score * 0.15
        # Trigger event
        if inp.has_trigger_event and inp.trigger_event_type != "none":
            score += 15.0
        # Prior engagement data
        if inp.prior_emails_sent > 0:
            score += min(10.0, inp.prior_open_rate * 10.0 + inp.prior_reply_rate * 10.0)
        # Warm lead boost
        if inp.is_warm_lead:
            score += 5.0
        return round(max(0.0, min(100.0, score)), 1)

    def _personalization_level(
        self, score: float, inp: EmailPersonalizationInput
    ) -> PersonalizationLevel:
        if score >= 80 and inp.personalization_tokens >= 4:
            return PersonalizationLevel.HYPER_PERSONALIZED
        if score >= 65:
            return PersonalizationLevel.HIGHLY_PERSONALIZED
        if score >= 45:
            return PersonalizationLevel.MODERATELY_PERSONALIZED
        if score >= 25:
            return PersonalizationLevel.GENERIC
        return PersonalizationLevel.TEMPLATE

    def _email_tone(self, inp: EmailPersonalizationInput) -> EmailTone:
        if inp.seniority_level >= 4:
            return EmailTone.EXECUTIVE
        if inp.buyer_intent_score >= 70:
            return EmailTone.URGENCY
        if inp.has_trigger_event:
            return EmailTone.CHALLENGER
        if inp.lead_score >= 60:
            return EmailTone.CONSULTATIVE
        return EmailTone.EDUCATIONAL

    def _send_timing(self, inp: EmailPersonalizationInput) -> SendTiming:
        if inp.opted_out:
            return SendTiming.HOLD
        if inp.has_trigger_event and inp.buyer_intent_score >= 60:
            return SendTiming.IMMEDIATE
        if inp.seniority_level >= 4:
            return SendTiming.MORNING
        if inp.sequence_position == 1:
            return SendTiming.MORNING
        if inp.days_since_last_email < 2:
            return SendTiming.NEXT_BUSINESS_DAY
        return SendTiming.MIDDAY

    def _predicted_open_rate(self, inp: EmailPersonalizationInput, p_score: float) -> float:
        base = 0.20
        base += p_score * 0.003
        if inp.subject_line_score >= 70:
            base += 0.10
        elif inp.subject_line_score >= 50:
            base += 0.05
        if inp.has_trigger_event:
            base += 0.08
        if inp.is_warm_lead:
            base += 0.07
        if inp.seniority_level >= 4:
            base -= 0.05
        if inp.prior_emails_sent > 3 and inp.prior_open_rate < 0.15:
            base -= 0.08
        return round(max(0.0, min(1.0, base)), 3)

    def _predicted_reply_rate(self, inp: EmailPersonalizationInput, p_score: float) -> float:
        base = 0.03
        base += p_score * 0.002
        if inp.body_relevance_score >= 70:
            base += 0.05
        elif inp.body_relevance_score >= 50:
            base += 0.02
        if inp.buyer_intent_score >= 70:
            base += 0.06
        if inp.is_warm_lead:
            base += 0.04
        if inp.persona_pain_points >= 3:
            base += 0.03
        if inp.sequence_position > 3:
            base -= 0.02
        if inp.prior_reply_rate > 0:
            base += inp.prior_reply_rate * 0.20
        return round(max(0.0, min(1.0, base)), 3)

    def _send_score(
        self,
        inp: EmailPersonalizationInput,
        p_score: float,
        open_r: float,
        reply_r: float,
    ) -> float:
        score = p_score * 0.40
        score += open_r  * 100 * 0.30
        score += reply_r * 100 * 0.30
        if inp.has_trigger_event:
            score += 5
        if inp.days_since_last_email < 1:
            score -= 15
        if inp.prior_emails_sent > 5 and inp.prior_reply_rate < 0.02:
            score -= 10
        return round(max(0.0, min(100.0, score)), 1)

    def _recommended_action(
        self, inp: EmailPersonalizationInput, s_score: float, p_score: float
    ) -> PersonalizationAction:
        if inp.opted_out:
            return PersonalizationAction.HOLD
        if inp.days_since_last_email < 1:
            return PersonalizationAction.HOLD
        if s_score >= 70 and p_score >= 65:
            return PersonalizationAction.SEND_NOW
        if s_score >= 55:
            return PersonalizationAction.REFINE_AND_SEND
        if s_score >= 35:
            return PersonalizationAction.REVIEW_BEFORE_SEND
        if p_score < 25:
            return PersonalizationAction.REWRITE_REQUIRED
        return PersonalizationAction.REVIEW_BEFORE_SEND

    def _optimization_score(self, p_score: float, s_score: float) -> float:
        return round((p_score * 0.50 + s_score * 0.50), 1)

    def _personalization_tips(
        self, inp: EmailPersonalizationInput, p_score: float, level: PersonalizationLevel
    ) -> list[str]:
        tips: list[str] = []
        if inp.personalization_tokens < 3:
            tips.append("Enrichir le profil — ajouter plus de données de personnalisation")
        if inp.persona_pain_points < 2:
            tips.append("Identifier les points de douleur spécifiques au persona")
        if not inp.has_trigger_event:
            tips.append("Rechercher un trigger event récent (levée de fonds, recrutement, expansion)")
        if inp.subject_line_score < 60:
            tips.append("Améliorer la ligne d'objet — viser un score supérieur à 60")
        if inp.body_relevance_score < 60:
            tips.append("Renforcer la pertinence du corps — aligner sur le secteur et le persona")
        if inp.buyer_intent_score < 40 and inp.lead_score >= 60:
            tips.append("Activer les signaux d'intention — surveiller les visites et recherches")
        if level == PersonalizationLevel.TEMPLATE:
            tips.append("Personnaliser au minimum 3 éléments avant d'envoyer")
        return tips

    def _subject_suggestions(
        self, inp: EmailPersonalizationInput, tone: EmailTone, level: PersonalizationLevel
    ) -> list[str]:
        suggestions: list[str] = []
        industry_context = {
            "saas": "croissance SaaS",
            "finance": "performance financière",
            "retail": "expérience client retail",
        }.get(inp.industry, "votre secteur")

        if inp.has_trigger_event and inp.trigger_event_type == "funding":
            suggestions.append(
                f"Félicitations pour votre levée — comment accélérer la {industry_context}"
            )
        if tone == EmailTone.EXECUTIVE:
            suggestions.append(f"3 leviers pour améliorer la {industry_context} en Q3")
        if tone == EmailTone.URGENCY:
            suggestions.append("Action requise avant la fin du trimestre")
        if inp.is_warm_lead:
            suggestions.append("Suite à votre intérêt — prochaine étape concrète")
        if inp.sequence_position == 1:
            suggestions.append(f"Idée rapide pour la {industry_context}")
        if inp.sequence_position > 1:
            suggestions.append("Question courte — 2 minutes de votre temps ?")
        return suggestions[:3]

    def _risk_flags(
        self, inp: EmailPersonalizationInput, s_score: float, p_score: float
    ) -> list[str]:
        flags: list[str] = []
        if inp.opted_out:
            flags.append("Prospect opt-out — ne pas contacter")
        if inp.days_since_last_email < 1:
            flags.append("Email envoyé il y a moins de 24h — risque de spam")
        if inp.prior_emails_sent > 5 and inp.prior_open_rate < 0.10:
            flags.append(
                f"Faible taux d'ouverture historique ({inp.prior_open_rate:.0%}) — revoir l'approche"
            )
        if inp.prior_emails_sent > 3 and inp.prior_reply_rate < 0.02:
            flags.append("Aucune réponse après plusieurs relances — envisager un autre canal")
        if p_score < 30:
            flags.append("Personnalisation insuffisante — risque d'atterrir en spam")
        if s_score < 30:
            flags.append("Score d'envoi critique — ne pas envoyer sans optimisation")
        return flags

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total": 0,
                "level_counts": {},
                "tone_counts": {},
                "timing_counts": {},
                "action_counts": {},
                "avg_personalization_score": 0.0,
                "avg_send_score": 0.0,
                "avg_predicted_open_rate": 0.0,
                "avg_predicted_reply_rate": 0.0,
                "ready_to_send_count": 0,
                "needs_review_count": 0,
                "held_count": 0,
                "high_personalization_count": 0,
            }

        level_counts:  dict[str, int] = {}
        tone_counts:   dict[str, int] = {}
        timing_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_p = 0.0
        total_s = 0.0
        total_o = 0.0
        total_r = 0.0

        for res in self._results:
            level_counts[res.personalization_level.value] = level_counts.get(res.personalization_level.value, 0) + 1
            tone_counts[res.email_tone.value]             = tone_counts.get(res.email_tone.value, 0) + 1
            timing_counts[res.send_timing.value]          = timing_counts.get(res.send_timing.value, 0) + 1
            action_counts[res.recommended_action.value]   = action_counts.get(res.recommended_action.value, 0) + 1
            total_p += res.personalization_score
            total_s += res.send_score
            total_o += res.predicted_open_rate
            total_r += res.predicted_reply_rate

        return {
            "total":                       n,
            "level_counts":                level_counts,
            "tone_counts":                 tone_counts,
            "timing_counts":               timing_counts,
            "action_counts":               action_counts,
            "avg_personalization_score":   round(total_p / n, 1),
            "avg_send_score":              round(total_s / n, 1),
            "avg_predicted_open_rate":     round(total_o / n, 3),
            "avg_predicted_reply_rate":    round(total_r / n, 3),
            "ready_to_send_count":         len(self.ready_to_send),
            "needs_review_count":          len(self.needs_review),
            "held_count":                  len(self.held_emails),
            "high_personalization_count":  len(self.high_personalization),
        }
