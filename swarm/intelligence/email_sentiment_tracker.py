from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ThreadSentiment(str, Enum):
    ENTHUSIASTIC    = "enthusiastic"
    POSITIVE        = "positive"
    NEUTRAL         = "neutral"
    COOLING         = "cooling"
    NEGATIVE        = "negative"


class SentimentTrajectory(str, Enum):
    IMPROVING       = "improving"
    STABLE          = "stable"
    DECLINING       = "declining"
    VOLATILE        = "volatile"
    FLATLINED       = "flatlined"


class BuyerEngagementSignal(str, Enum):
    HIGHLY_ENGAGED      = "highly_engaged"
    ENGAGED             = "engaged"
    PASSIVELY_ENGAGED   = "passively_engaged"
    DISENGAGING         = "disengaging"
    DISENGAGED          = "disengaged"


class EmailAction(str, Enum):
    KEEP_MOMENTUM   = "keep_momentum"
    REFRAME         = "reframe"
    PATTERN_BREAK   = "pattern_break"
    ESCALATE_SEND   = "escalate_send"


@dataclass
class EmailSentimentInput:
    thread_id:                      str
    deal_id:                        str
    rep_id:                         str
    total_emails_sent:              int     # total emails rep sent in thread
    total_replies_received:         int     # total buyer replies in thread
    avg_reply_length_words:         int     # avg word count per buyer reply
    avg_reply_length_prior_words:   int     # avg word count per reply earlier in thread
    positive_language_count:        int     # # of positive/affirming phrases detected
    negative_language_count:        int     # # of negative/skeptical phrases detected
    question_count_from_buyer:      int     # # of questions buyer asked (engagement signal)
    exclamation_count:              int     # # of exclamation marks (enthusiasm signal)
    hedge_phrase_count:             int     # # of hedging phrases ("we'll see", "maybe", "not sure")
    urgency_language_count:         int     # # of urgency/deadline signals in buyer replies
    reply_time_trend:               float   # ratio recent/prior avg reply time (>1=slowing down)
    opens_per_email_avg:            float   # avg opens per email sent (>1 means re-reads)
    cta_click_rate_pct:             float   # % of CTAs clicked across the thread (0-100)
    sentiment_score_recent:         float   # AI sentiment score recent emails (0-100, 50=neutral)
    sentiment_score_prior:          float   # AI sentiment score prior emails (0-100, 50=neutral)
    days_since_last_reply:          int     # days since buyer last replied
    thread_age_days:                int     # age of email thread in days
    forwarded_to_others:            int     # 1 if buyer forwarded email to others
    deal_value:                     float


@dataclass
class EmailSentimentResult:
    thread_id:                  str
    deal_id:                    str
    thread_sentiment:           ThreadSentiment
    sentiment_trajectory:       SentimentTrajectory
    buyer_engagement_signal:    BuyerEngagementSignal
    email_action:               EmailAction
    reply_quality_score:        float   # 0-100
    engagement_depth_score:     float   # 0-100
    sentiment_momentum_score:   float   # 0-100
    urgency_alignment_score:    float   # 0-100
    email_composite:            float   # 0-100
    predicted_open_probability: float   # 0-100, chance next email gets opened
    thread_health_index:        float   # 0-100, overall thread health
    is_thread_healthy:          bool
    needs_intervention:         bool

    def to_dict(self) -> dict:
        return {
            "thread_id":                    self.thread_id,
            "deal_id":                      self.deal_id,
            "thread_sentiment":             self.thread_sentiment.value,
            "sentiment_trajectory":         self.sentiment_trajectory.value,
            "buyer_engagement_signal":      self.buyer_engagement_signal.value,
            "email_action":                 self.email_action.value,
            "reply_quality_score":          self.reply_quality_score,
            "engagement_depth_score":       self.engagement_depth_score,
            "sentiment_momentum_score":     self.sentiment_momentum_score,
            "urgency_alignment_score":      self.urgency_alignment_score,
            "email_composite":              self.email_composite,
            "predicted_open_probability":   self.predicted_open_probability,
            "thread_health_index":          self.thread_health_index,
            "is_thread_healthy":            self.is_thread_healthy,
            "needs_intervention":           self.needs_intervention,
        }


class EmailSentimentTracker:
    def __init__(self) -> None:
        self._results: list[EmailSentimentResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: EmailSentimentInput) -> EmailSentimentResult:
        reply_q     = self._reply_quality_score(inp)
        depth       = self._engagement_depth_score(inp)
        momentum    = self._sentiment_momentum_score(inp)
        urgency     = self._urgency_alignment_score(inp)
        composite   = self._composite(reply_q, depth, momentum, urgency)
        sentiment   = self._thread_sentiment(inp, composite)
        trajectory  = self._sentiment_trajectory(inp)
        engagement  = self._buyer_engagement_signal(composite, inp)
        open_prob   = self._predicted_open_probability(inp, composite)
        health_idx  = self._thread_health_index(inp, composite)
        is_healthy  = composite >= 55.0 and inp.days_since_last_reply <= 7
        needs_int   = composite < 35.0 or inp.days_since_last_reply >= 14
        action      = self._email_action(trajectory, needs_int, composite)

        result = EmailSentimentResult(
            thread_id=inp.thread_id,
            deal_id=inp.deal_id,
            thread_sentiment=sentiment,
            sentiment_trajectory=trajectory,
            buyer_engagement_signal=engagement,
            email_action=action,
            reply_quality_score=reply_q,
            engagement_depth_score=depth,
            sentiment_momentum_score=momentum,
            urgency_alignment_score=urgency,
            email_composite=composite,
            predicted_open_probability=open_prob,
            thread_health_index=health_idx,
            is_thread_healthy=is_healthy,
            needs_intervention=needs_int,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[EmailSentimentInput]) -> list[EmailSentimentResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def healthy_threads(self) -> list[EmailSentimentResult]:
        return [r for r in self._results if r.is_thread_healthy]

    @property
    def intervention_queue(self) -> list[EmailSentimentResult]:
        return [r for r in self._results if r.needs_intervention]

    @property
    def avg_email_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.email_composite for r in self._results) / len(self._results), 1)

    @property
    def avg_thread_health_index(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.thread_health_index for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _reply_quality_score(self, inp: EmailSentimentInput) -> float:
        score = 0.0
        # Reply rate
        if inp.total_emails_sent > 0:
            reply_rate = inp.total_replies_received / inp.total_emails_sent
            if reply_rate >= 0.7:
                score += 30.0
            elif reply_rate >= 0.5:
                score += 20.0
            elif reply_rate >= 0.3:
                score += 10.0
        # Reply length (longer = more engaged)
        if inp.avg_reply_length_words >= 80:
            score += 30.0
        elif inp.avg_reply_length_words >= 40:
            score += 18.0
        elif inp.avg_reply_length_words >= 15:
            score += 8.0
        # Reply length trend (shrinking = disengaging)
        if inp.avg_reply_length_prior_words > 0:
            length_ratio = inp.avg_reply_length_words / inp.avg_reply_length_prior_words
            if length_ratio >= 1.2:
                score += 20.0
            elif length_ratio <= 0.5:
                score -= 15.0
            elif length_ratio <= 0.7:
                score -= 8.0
        # Reply time trend (slowing = disengaging)
        if inp.reply_time_trend <= 0.8:
            score += 10.0
        elif inp.reply_time_trend >= 2.0:
            score -= 10.0
        elif inp.reply_time_trend >= 1.5:
            score -= 5.0
        # Days since last reply
        if inp.days_since_last_reply >= 14:
            score -= 20.0
        elif inp.days_since_last_reply >= 7:
            score -= 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _engagement_depth_score(self, inp: EmailSentimentInput) -> float:
        score = 0.0
        # Buyer questions = high engagement
        questions = inp.question_count_from_buyer
        if questions >= 5:
            score += 30.0
        elif questions >= 3:
            score += 20.0
        elif questions >= 1:
            score += 10.0
        # CTA click rate
        cta = inp.cta_click_rate_pct
        if cta >= 60:
            score += 25.0
        elif cta >= 30:
            score += 15.0
        elif cta >= 10:
            score += 8.0
        # Multi-open signal
        if inp.opens_per_email_avg >= 2.0:
            score += 20.0
        elif inp.opens_per_email_avg >= 1.3:
            score += 10.0
        # Forwarded to others = high commitment signal
        if inp.forwarded_to_others:
            score += 20.0
        # Exclamation marks = enthusiasm
        if inp.exclamation_count >= 5:
            score += 5.0
        elif inp.exclamation_count >= 2:
            score += 3.0
        return round(max(0.0, min(100.0, score)), 1)

    def _sentiment_momentum_score(self, inp: EmailSentimentInput) -> float:
        # Based on language signals and AI sentiment
        score = 50.0  # neutral base
        # Positive vs negative language
        net_language = inp.positive_language_count - inp.negative_language_count
        if net_language >= 5:
            score += 25.0
        elif net_language >= 2:
            score += 15.0
        elif net_language >= 0:
            score += 5.0
        elif net_language >= -2:
            score -= 10.0
        else:
            score -= 20.0
        # Hedge phrases = uncertainty
        if inp.hedge_phrase_count >= 5:
            score -= 20.0
        elif inp.hedge_phrase_count >= 3:
            score -= 12.0
        elif inp.hedge_phrase_count >= 1:
            score -= 5.0
        # Sentiment trend
        sent_delta = inp.sentiment_score_recent - inp.sentiment_score_prior
        if sent_delta >= 10:
            score += 15.0
        elif sent_delta >= 5:
            score += 8.0
        elif sent_delta <= -10:
            score -= 15.0
        elif sent_delta <= -5:
            score -= 8.0
        return round(max(0.0, min(100.0, score)), 1)

    def _urgency_alignment_score(self, inp: EmailSentimentInput) -> float:
        score = 0.0
        # Buyer urgency language = deal heat
        if inp.urgency_language_count >= 4:
            score += 40.0
        elif inp.urgency_language_count >= 2:
            score += 25.0
        elif inp.urgency_language_count >= 1:
            score += 12.0
        # Recent high sentiment = urgency aligned
        if inp.sentiment_score_recent >= 70:
            score += 30.0
        elif inp.sentiment_score_recent >= 55:
            score += 18.0
        # CTA engagement
        if inp.cta_click_rate_pct >= 50:
            score += 20.0
        elif inp.cta_click_rate_pct >= 25:
            score += 10.0
        # Forwarding = urgency signal
        if inp.forwarded_to_others:
            score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        reply_q: float,
        depth: float,
        momentum: float,
        urgency: float,
    ) -> float:
        composite = reply_q * 0.30 + depth * 0.30 + momentum * 0.25 + urgency * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _thread_sentiment(self, inp: EmailSentimentInput, composite: float) -> ThreadSentiment:
        sent = inp.sentiment_score_recent
        if sent >= 75 and composite >= 60:
            return ThreadSentiment.ENTHUSIASTIC
        if sent >= 60 or composite >= 55:
            return ThreadSentiment.POSITIVE
        if sent >= 45:
            return ThreadSentiment.NEUTRAL
        if sent >= 30:
            return ThreadSentiment.COOLING
        return ThreadSentiment.NEGATIVE

    def _sentiment_trajectory(self, inp: EmailSentimentInput) -> SentimentTrajectory:
        sent_delta = inp.sentiment_score_recent - inp.sentiment_score_prior
        length_ratio = (
            inp.avg_reply_length_words / inp.avg_reply_length_prior_words
            if inp.avg_reply_length_prior_words > 0
            else 1.0
        )
        if inp.days_since_last_reply >= 14:
            return SentimentTrajectory.FLATLINED
        if abs(sent_delta) >= 20 and length_ratio >= 1.5:
            return SentimentTrajectory.VOLATILE
        if sent_delta >= 8 and length_ratio >= 0.9:
            return SentimentTrajectory.IMPROVING
        if sent_delta <= -8 or length_ratio <= 0.6:
            return SentimentTrajectory.DECLINING
        return SentimentTrajectory.STABLE

    def _buyer_engagement_signal(self, composite: float, inp: EmailSentimentInput) -> BuyerEngagementSignal:
        if composite >= 75 and inp.question_count_from_buyer >= 3:
            return BuyerEngagementSignal.HIGHLY_ENGAGED
        if composite >= 55:
            return BuyerEngagementSignal.ENGAGED
        if composite >= 40:
            return BuyerEngagementSignal.PASSIVELY_ENGAGED
        if composite >= 25 or inp.days_since_last_reply >= 7:
            return BuyerEngagementSignal.DISENGAGING
        return BuyerEngagementSignal.DISENGAGED

    def _predicted_open_probability(self, inp: EmailSentimentInput, composite: float) -> float:
        base = composite * 0.6
        if inp.opens_per_email_avg >= 1.5:
            base = min(100.0, base + 20.0)
        if inp.sentiment_score_recent >= 65:
            base = min(100.0, base + 15.0)
        if inp.days_since_last_reply >= 14:
            base -= 20.0
        return round(max(0.0, min(100.0, base)), 1)

    def _thread_health_index(self, inp: EmailSentimentInput, composite: float) -> float:
        base = composite
        if inp.total_replies_received >= 3:
            base = min(100.0, base + 5.0)
        if inp.days_since_last_reply <= 3:
            base = min(100.0, base + 8.0)
        return round(max(0.0, min(100.0, base)), 1)

    def _email_action(
        self,
        trajectory: SentimentTrajectory,
        needs_int: bool,
        composite: float,
    ) -> EmailAction:
        if trajectory == SentimentTrajectory.FLATLINED or composite < 20:
            return EmailAction.ESCALATE_SEND
        if needs_int or trajectory == SentimentTrajectory.DECLINING:
            return EmailAction.PATTERN_BREAK
        if trajectory in (SentimentTrajectory.VOLATILE, SentimentTrajectory.STABLE) and composite < 55:
            return EmailAction.REFRAME
        return EmailAction.KEEP_MOMENTUM

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                            0,
                "sentiment_counts":                 {},
                "trajectory_counts":                {},
                "engagement_counts":                {},
                "action_counts":                    {},
                "avg_email_composite":              0.0,
                "avg_thread_health_index":          0.0,
                "healthy_count":                    0,
                "intervention_count":               0,
                "avg_reply_quality_score":          0.0,
                "avg_engagement_depth_score":       0.0,
                "avg_sentiment_momentum_score":     0.0,
                "avg_urgency_alignment_score":      0.0,
            }

        sentiment_counts:  dict[str, int] = {}
        trajectory_counts: dict[str, int] = {}
        engagement_counts: dict[str, int] = {}
        action_counts:     dict[str, int] = {}
        total_comp = 0.0
        total_health = 0.0
        total_reply = 0.0
        total_depth = 0.0
        total_mom   = 0.0
        total_urg   = 0.0

        for r in self._results:
            sentiment_counts[r.thread_sentiment.value]        = sentiment_counts.get(r.thread_sentiment.value, 0) + 1
            trajectory_counts[r.sentiment_trajectory.value]   = trajectory_counts.get(r.sentiment_trajectory.value, 0) + 1
            engagement_counts[r.buyer_engagement_signal.value] = engagement_counts.get(r.buyer_engagement_signal.value, 0) + 1
            action_counts[r.email_action.value]               = action_counts.get(r.email_action.value, 0) + 1
            total_comp   += r.email_composite
            total_health += r.thread_health_index
            total_reply  += r.reply_quality_score
            total_depth  += r.engagement_depth_score
            total_mom    += r.sentiment_momentum_score
            total_urg    += r.urgency_alignment_score

        return {
            "total":                            n,
            "sentiment_counts":                 sentiment_counts,
            "trajectory_counts":                trajectory_counts,
            "engagement_counts":                engagement_counts,
            "action_counts":                    action_counts,
            "avg_email_composite":              round(total_comp / n, 1),
            "avg_thread_health_index":          round(total_health / n, 1),
            "healthy_count":                    len(self.healthy_threads),
            "intervention_count":               len(self.intervention_queue),
            "avg_reply_quality_score":          round(total_reply / n, 1),
            "avg_engagement_depth_score":       round(total_depth / n, 1),
            "avg_sentiment_momentum_score":     round(total_mom / n, 1),
            "avg_urgency_alignment_score":      round(total_urg / n, 1),
        }
