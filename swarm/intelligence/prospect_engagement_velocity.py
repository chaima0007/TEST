from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class EngagementVelocity(str, Enum):
    ACCELERATING = "accelerating"
    STEADY       = "steady"
    DECELERATING = "decelerating"
    STALLED      = "stalled"
    COLD         = "cold"


class IntentLevel(str, Enum):
    HOT      = "hot"
    WARM     = "warm"
    LUKEWARM = "lukewarm"
    COLD     = "cold"


class EngagementRisk(str, Enum):
    LOW      = "low"
    MODERATE = "moderate"
    HIGH     = "high"
    CRITICAL = "critical"


class EngagementAction(str, Enum):
    NURTURE     = "nurture"
    ADVANCE     = "advance"
    REACTIVATE  = "reactivate"
    DISQUALIFY  = "disqualify"


@dataclass
class ProspectEngagementInput:
    prospect_id: str
    prospect_name: str
    company_name: str
    rep_id: str
    emails_sent_last_30d: int
    emails_opened_last_30d: int
    emails_replied_last_30d: int
    avg_reply_time_hours: float
    meetings_requested_last_30d: int
    meetings_accepted_last_30d: int
    meetings_rescheduled_count: int
    meetings_ghosted_count: int
    content_viewed_last_30d: int
    demo_request_submitted: int
    pricing_page_visited_count: int
    linkedin_engagement_count: int
    days_since_last_engagement: int
    days_since_first_contact: int
    champion_internal_sharing: int
    decision_maker_cc_count: int
    prior_30d_engagement_score: float
    deal_stage: int


@dataclass
class ProspectEngagementResult:
    prospect_id: str
    prospect_name: str
    engagement_velocity: EngagementVelocity
    intent_level: IntentLevel
    engagement_risk: EngagementRisk
    engagement_action: EngagementAction
    email_engagement_score: float
    meeting_engagement_score: float
    digital_engagement_score: float
    velocity_trend_score: float
    engagement_composite: float
    days_to_re_engage: int
    is_high_intent: bool
    needs_reactivation: bool
    primary_signal: str

    def to_dict(self) -> dict:
        return {
            "prospect_id": self.prospect_id,
            "prospect_name": self.prospect_name,
            "engagement_velocity": self.engagement_velocity.value,
            "intent_level": self.intent_level.value,
            "engagement_risk": self.engagement_risk.value,
            "engagement_action": self.engagement_action.value,
            "email_engagement_score": self.email_engagement_score,
            "meeting_engagement_score": self.meeting_engagement_score,
            "digital_engagement_score": self.digital_engagement_score,
            "velocity_trend_score": self.velocity_trend_score,
            "engagement_composite": self.engagement_composite,
            "days_to_re_engage": self.days_to_re_engage,
            "is_high_intent": self.is_high_intent,
            "needs_reactivation": self.needs_reactivation,
            "primary_signal": self.primary_signal,
        }


def _email_engagement_score(inp: ProspectEngagementInput) -> float:
    score = 0.0
    # Open rate (0-25)
    if inp.emails_sent_last_30d > 0:
        open_rate = inp.emails_opened_last_30d / inp.emails_sent_last_30d
        if open_rate >= 0.8:
            score += 25.0
        elif open_rate >= 0.6:
            score += 18.0
        elif open_rate >= 0.4:
            score += 11.0
        elif open_rate >= 0.2:
            score += 5.0
    # Reply rate (0-35)
    if inp.emails_sent_last_30d > 0:
        reply_rate = inp.emails_replied_last_30d / inp.emails_sent_last_30d
        if reply_rate >= 0.5:
            score += 35.0
        elif reply_rate >= 0.3:
            score += 25.0
        elif reply_rate >= 0.15:
            score += 15.0
        elif reply_rate >= 0.05:
            score += 7.0
    # Reply speed (0-25)
    if inp.avg_reply_time_hours > 0:
        if inp.avg_reply_time_hours <= 2:
            score += 25.0
        elif inp.avg_reply_time_hours <= 6:
            score += 18.0
        elif inp.avg_reply_time_hours <= 24:
            score += 10.0
        elif inp.avg_reply_time_hours <= 72:
            score += 4.0
    # Recency penalty (0-15, reversed)
    if inp.days_since_last_engagement <= 3:
        score += 15.0
    elif inp.days_since_last_engagement <= 7:
        score += 10.0
    elif inp.days_since_last_engagement <= 14:
        score += 5.0
    return max(0.0, min(100.0, round(score, 1)))


def _meeting_engagement_score(inp: ProspectEngagementInput) -> float:
    score = 0.0
    # Acceptance rate (0-40)
    if inp.meetings_requested_last_30d > 0:
        acc_rate = inp.meetings_accepted_last_30d / inp.meetings_requested_last_30d
        if acc_rate >= 0.8:
            score += 40.0
        elif acc_rate >= 0.6:
            score += 28.0
        elif acc_rate >= 0.4:
            score += 18.0
        elif acc_rate >= 0.2:
            score += 8.0
    # Ghosting penalty (0-30, reversed)
    if inp.meetings_ghosted_count == 0:
        score += 30.0
    elif inp.meetings_ghosted_count == 1:
        score += 18.0
    elif inp.meetings_ghosted_count == 2:
        score += 8.0
    # Rescheduling mild penalty (0-15, reversed)
    if inp.meetings_rescheduled_count == 0:
        score += 15.0
    elif inp.meetings_rescheduled_count <= 1:
        score += 10.0
    elif inp.meetings_rescheduled_count <= 2:
        score += 4.0
    # Internal champion sharing bonus (0-15)
    if inp.champion_internal_sharing:
        score += 10.0
    if inp.decision_maker_cc_count >= 2:
        score += 5.0
    elif inp.decision_maker_cc_count >= 1:
        score += 3.0
    return max(0.0, min(100.0, round(score, 1)))


def _digital_engagement_score(inp: ProspectEngagementInput) -> float:
    score = 0.0
    # Content viewed (0-25)
    if inp.content_viewed_last_30d >= 5:
        score += 25.0
    elif inp.content_viewed_last_30d >= 3:
        score += 16.0
    elif inp.content_viewed_last_30d >= 1:
        score += 8.0
    # Demo request (0-30)
    if inp.demo_request_submitted:
        score += 30.0
    # Pricing page visits (0-25) — strong buying signal
    if inp.pricing_page_visited_count >= 3:
        score += 25.0
    elif inp.pricing_page_visited_count >= 1:
        score += 15.0
    # LinkedIn engagement (0-20)
    if inp.linkedin_engagement_count >= 5:
        score += 20.0
    elif inp.linkedin_engagement_count >= 3:
        score += 13.0
    elif inp.linkedin_engagement_count >= 1:
        score += 6.0
    return max(0.0, min(100.0, round(score, 1)))


def _velocity_trend_score(inp: ProspectEngagementInput) -> float:
    # Compare current vs prior engagement score
    current = (
        _email_engagement_score(inp) * 0.35
        + _meeting_engagement_score(inp) * 0.35
        + _digital_engagement_score(inp) * 0.30
    )
    prior = max(0.0, min(100.0, inp.prior_30d_engagement_score))
    if prior <= 0:
        return 50.0  # no prior baseline
    ratio = current / prior
    if ratio >= 1.3:
        score = 95.0
    elif ratio >= 1.1:
        score = 80.0
    elif ratio >= 0.9:
        score = 60.0
    elif ratio >= 0.7:
        score = 35.0
    elif ratio >= 0.5:
        score = 15.0
    else:
        score = 5.0
    return round(score, 1)


def _composite(email: float, meeting: float, digital: float, velocity: float) -> float:
    raw = email * 0.30 + meeting * 0.30 + digital * 0.20 + velocity * 0.20
    return round(raw, 1)


def _engagement_velocity(composite: float, velocity_trend: float,
                         days_since: int) -> EngagementVelocity:
    if days_since >= 21:
        return EngagementVelocity.COLD
    if days_since >= 14 or composite < 20:
        return EngagementVelocity.STALLED
    if velocity_trend >= 75:
        return EngagementVelocity.ACCELERATING
    if velocity_trend >= 55:
        return EngagementVelocity.STEADY
    if velocity_trend >= 35:
        return EngagementVelocity.DECELERATING
    return EngagementVelocity.STALLED


def _intent_level(composite: float, inp: ProspectEngagementInput) -> IntentLevel:
    if composite >= 70 and inp.days_since_last_engagement <= 7:
        return IntentLevel.HOT
    if composite >= 50:
        return IntentLevel.WARM
    if composite >= 30:
        return IntentLevel.LUKEWARM
    return IntentLevel.COLD


def _engagement_risk(composite: float, days_since: int) -> EngagementRisk:
    if composite < 20 or days_since >= 21:
        return EngagementRisk.CRITICAL
    if composite < 35 or days_since >= 14:
        return EngagementRisk.HIGH
    if composite < 55 or days_since >= 7:
        return EngagementRisk.MODERATE
    return EngagementRisk.LOW


def _engagement_action(risk: EngagementRisk, composite: float,
                       days_since: int) -> EngagementAction:
    if composite >= 70 and risk == EngagementRisk.LOW:
        return EngagementAction.ADVANCE
    if days_since >= 14 or composite < 30:
        if composite < 15 or days_since >= 28:
            return EngagementAction.DISQUALIFY
        return EngagementAction.REACTIVATE
    if risk in (EngagementRisk.MODERATE,):
        return EngagementAction.NURTURE
    return EngagementAction.ADVANCE


def _days_to_re_engage(composite: float, days_since: int) -> int:
    if composite >= 70:
        return 1
    if composite >= 50:
        return 2
    if composite >= 35:
        return 3
    if days_since >= 14:
        return 5
    return 4


def _primary_signal(inp: ProspectEngagementInput,
                    email: float, meeting: float, digital: float) -> str:
    if inp.pricing_page_visited_count >= 2:
        return "pricing page visited — high buying intent"
    if inp.demo_request_submitted:
        return "demo requested — strong interest"
    if inp.champion_internal_sharing:
        return "champion sharing content internally"
    if inp.decision_maker_cc_count >= 1:
        return "decision maker engaged via CC"
    if inp.meetings_ghosted_count >= 2:
        return "multiple meetings ghosted — low engagement"
    if inp.days_since_last_engagement >= 14:
        return "gone dark — reactivation required"
    scores = {"email": email, "meeting": meeting, "digital": digital}
    best = max(scores, key=lambda k: scores[k])
    return f"strongest signal: {best} engagement"


class ProspectEngagementVelocityTracker:
    def __init__(self) -> None:
        self._results: dict[str, ProspectEngagementResult] = {}

    def track(self, inp: ProspectEngagementInput) -> ProspectEngagementResult:
        email   = _email_engagement_score(inp)
        meeting = _meeting_engagement_score(inp)
        digital = _digital_engagement_score(inp)
        velocity_trend = _velocity_trend_score(inp)
        composite = _composite(email, meeting, digital, velocity_trend)

        velocity = _engagement_velocity(composite, velocity_trend, inp.days_since_last_engagement)
        intent   = _intent_level(composite, inp)
        risk     = _engagement_risk(composite, inp.days_since_last_engagement)
        action   = _engagement_action(risk, composite, inp.days_since_last_engagement)
        d2r      = _days_to_re_engage(composite, inp.days_since_last_engagement)
        signal   = _primary_signal(inp, email, meeting, digital)

        is_high_intent    = composite >= 70.0 and inp.days_since_last_engagement <= 7
        needs_reactivation = (inp.days_since_last_engagement >= 14 or composite < 30.0)

        result = ProspectEngagementResult(
            prospect_id=inp.prospect_id,
            prospect_name=inp.prospect_name,
            engagement_velocity=velocity,
            intent_level=intent,
            engagement_risk=risk,
            engagement_action=action,
            email_engagement_score=email,
            meeting_engagement_score=meeting,
            digital_engagement_score=digital,
            velocity_trend_score=velocity_trend,
            engagement_composite=composite,
            days_to_re_engage=d2r,
            is_high_intent=is_high_intent,
            needs_reactivation=needs_reactivation,
            primary_signal=signal,
        )
        self._results[inp.prospect_id] = result
        return result

    def track_batch(self, inputs: List[ProspectEngagementInput]) -> List[ProspectEngagementResult]:
        results = [self.track(inp) for inp in inputs]
        results.sort(key=lambda r: r.engagement_composite, reverse=True)
        return results

    def get(self, prospect_id: str) -> ProspectEngagementResult | None:
        return self._results.get(prospect_id)

    def all_prospects(self) -> List[ProspectEngagementResult]:
        return sorted(self._results.values(), key=lambda r: r.engagement_composite, reverse=True)

    def high_intent_prospects(self) -> List[ProspectEngagementResult]:
        return [r for r in self._results.values() if r.is_high_intent]

    def reactivation_list(self) -> List[ProspectEngagementResult]:
        return [r for r in self._results.values() if r.needs_reactivation]

    def by_velocity(self, velocity: EngagementVelocity) -> List[ProspectEngagementResult]:
        return [r for r in self._results.values() if r.engagement_velocity == velocity]

    def by_intent(self, intent: IntentLevel) -> List[ProspectEngagementResult]:
        return [r for r in self._results.values() if r.intent_level == intent]

    def avg_engagement_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.engagement_composite for r in self._results.values()) / len(self._results), 1)

    def reset(self) -> None:
        self._results.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        velocity_counts: dict[str, int] = {}
        intent_counts:   dict[str, int] = {}
        risk_counts:     dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        for r in results:
            velocity_counts[r.engagement_velocity.value] = velocity_counts.get(r.engagement_velocity.value, 0) + 1
            intent_counts[r.intent_level.value]           = intent_counts.get(r.intent_level.value, 0) + 1
            risk_counts[r.engagement_risk.value]          = risk_counts.get(r.engagement_risk.value, 0) + 1
            action_counts[r.engagement_action.value]      = action_counts.get(r.engagement_action.value, 0) + 1
        return {
            "total": n,
            "velocity_counts":                velocity_counts,
            "intent_counts":                   intent_counts,
            "risk_counts":                     risk_counts,
            "action_counts":                   action_counts,
            "avg_engagement_composite":        self.avg_engagement_composite(),
            "high_intent_count":               len(self.high_intent_prospects()),
            "reactivation_count":              len(self.reactivation_list()),
            "avg_email_engagement_score":      round(sum(r.email_engagement_score for r in results) / n, 1) if n else 0.0,
            "avg_meeting_engagement_score":    round(sum(r.meeting_engagement_score for r in results) / n, 1) if n else 0.0,
            "avg_digital_engagement_score":    round(sum(r.digital_engagement_score for r in results) / n, 1) if n else 0.0,
            "avg_velocity_trend_score":        round(sum(r.velocity_trend_score for r in results) / n, 1) if n else 0.0,
            "avg_days_to_re_engage":           round(sum(r.days_to_re_engage for r in results) / n, 1) if n else 0.0,
        }
