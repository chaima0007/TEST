from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ToneSentiment(str, Enum):
    POSITIVE   = "positive"
    NEUTRAL    = "neutral"
    CAUTIOUS   = "cautious"
    NEGATIVE   = "negative"


class DominantTone(str, Enum):
    ENTHUSIASTIC  = "enthusiastic"
    AUTHORITATIVE = "authoritative"
    HESITANT      = "hesitant"
    EVASIVE       = "evasive"
    RESISTANT     = "resistant"
    PANIC_SIGNAL  = "panic_signal"


class ConversationControl(str, Enum):
    REP_LED      = "rep_led"
    BALANCED     = "balanced"
    BUYER_LED    = "buyer_led"
    FRAGMENTED   = "fragmented"


class ToneAction(str, Enum):
    REINFORCE   = "reinforce"
    NURTURE     = "nurture"
    REFRAME     = "reframe"
    INTERVENE   = "intervene"


@dataclass
class CallToneInput:
    call_id:                        str
    deal_name:                      str
    rep_id:                         str
    call_duration_minutes:          int     # total call length
    talk_time_rep_pct:              float   # % of call rep was talking (0-100)
    filler_word_rate_per_min:       float   # "um", "uh", "like" per minute (hesitation signal)
    interruption_count_rep:         int     # how many times rep interrupted buyer
    interruption_count_buyer:       int     # how many times buyer interrupted rep
    questions_asked_rep:            int     # open-ended questions asked by rep
    questions_asked_buyer:          int     # questions buyer asked (interest signal)
    sentiment_score_positive:       float   # % of sentences with positive sentiment
    sentiment_score_negative:       float   # % of sentences with negative sentiment
    enthusiasm_keywords_count:      int     # "excited", "love", "great", "absolutely" count
    hesitation_keywords_count:      int     # "maybe", "not sure", "have to check", "concern" count
    objection_count:                int     # number of distinct objections raised
    objection_resolved_count:       int     # objections rep successfully addressed
    silence_events_long:            int     # silences > 5 seconds (awkward/thinking)
    price_mention_count:            int     # how many times price/budget was mentioned
    competitor_mention_count:       int     # competitor names dropped on call
    decision_timeline_mentioned:    int     # 1 if buyer mentioned a decision timeline
    next_steps_agreed:              int     # 1 if specific next steps were agreed on call
    call_ended_abruptly:            int     # 1 if call ended without clean close


@dataclass
class CallToneResult:
    call_id:                    str
    deal_name:                  str
    tone_sentiment:             ToneSentiment
    dominant_tone:              DominantTone
    conversation_control:       ConversationControl
    tone_action:                ToneAction
    rep_confidence_score:       float   # 0-100
    buyer_engagement_score:     float   # 0-100
    objection_handling_score:   float   # 0-100
    conversation_quality_score: float   # 0-100
    call_tone_composite:        float   # 0-100 (higher = better)
    deal_advancement_probability: float # 0-100
    call_coaching_priority:     float   # 0-100, how urgently rep needs coaching
    is_positive_call:           bool
    needs_immediate_coaching:   bool

    def to_dict(self) -> dict:
        return {
            "call_id":                    self.call_id,
            "deal_name":                  self.deal_name,
            "tone_sentiment":             self.tone_sentiment.value,
            "dominant_tone":              self.dominant_tone.value,
            "conversation_control":       self.conversation_control.value,
            "tone_action":                self.tone_action.value,
            "rep_confidence_score":       self.rep_confidence_score,
            "buyer_engagement_score":     self.buyer_engagement_score,
            "objection_handling_score":   self.objection_handling_score,
            "conversation_quality_score": self.conversation_quality_score,
            "call_tone_composite":        self.call_tone_composite,
            "deal_advancement_probability": self.deal_advancement_probability,
            "call_coaching_priority":     self.call_coaching_priority,
            "is_positive_call":           self.is_positive_call,
            "needs_immediate_coaching":   self.needs_immediate_coaching,
        }


class CallToneAnalyzer:
    def __init__(self) -> None:
        self._results: list[CallToneResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: CallToneInput) -> CallToneResult:
        conf    = self._rep_confidence_score(inp)
        engage  = self._buyer_engagement_score(inp)
        obj_hdl = self._objection_handling_score(inp)
        quality = self._conversation_quality_score(inp)
        composite = self._composite(conf, engage, obj_hdl, quality)
        sentiment = self._tone_sentiment(inp, composite)
        tone    = self._dominant_tone(inp, conf, engage)
        control = self._conversation_control(inp)
        adv_prob = self._deal_advancement_probability(inp, composite)
        coaching = self._coaching_priority(conf, obj_hdl, composite)
        is_pos  = composite >= 55.0 and inp.next_steps_agreed == 1
        needs_c = coaching >= 65.0 or (inp.filler_word_rate_per_min >= 5.0 and conf < 40.0)
        action  = self._tone_action(sentiment, is_pos, needs_c)

        result = CallToneResult(
            call_id=inp.call_id,
            deal_name=inp.deal_name,
            tone_sentiment=sentiment,
            dominant_tone=tone,
            conversation_control=control,
            tone_action=action,
            rep_confidence_score=conf,
            buyer_engagement_score=engage,
            objection_handling_score=obj_hdl,
            conversation_quality_score=quality,
            call_tone_composite=composite,
            deal_advancement_probability=adv_prob,
            call_coaching_priority=coaching,
            is_positive_call=is_pos,
            needs_immediate_coaching=needs_c,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[CallToneInput]) -> list[CallToneResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def positive_calls(self) -> list[CallToneResult]:
        return [r for r in self._results if r.is_positive_call]

    @property
    def coaching_needed(self) -> list[CallToneResult]:
        return [r for r in self._results if r.needs_immediate_coaching]

    @property
    def avg_call_tone_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.call_tone_composite for r in self._results) / len(self._results), 1)

    @property
    def avg_deal_advancement_probability(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.deal_advancement_probability for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _rep_confidence_score(self, inp: CallToneInput) -> float:
        score = 50.0  # baseline
        # Filler word rate penalty (high fillers = low confidence)
        rate = inp.filler_word_rate_per_min
        if rate >= 5.0:
            score -= 30.0
        elif rate >= 3.0:
            score -= 18.0
        elif rate >= 1.5:
            score -= 8.0
        # Enthusiasm keywords boost
        score += min(20.0, inp.enthusiasm_keywords_count * 3.0)
        # Rep interrupting buyer too much = low control, but some ok
        if inp.interruption_count_rep > 5:
            score -= 15.0
        elif inp.interruption_count_rep > 2:
            score -= 5.0
        # Good talk ratio = 40-60%
        talk_ratio = inp.talk_time_rep_pct
        if 40.0 <= talk_ratio <= 60.0:
            score += 10.0
        elif talk_ratio > 80.0 or talk_ratio < 20.0:
            score -= 15.0
        # Abrupt ending
        if inp.call_ended_abruptly:
            score -= 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _buyer_engagement_score(self, inp: CallToneInput) -> float:
        score = 30.0  # baseline
        # Buyer questions = strong engagement signal
        score += min(30.0, inp.questions_asked_buyer * 5.0)
        # Buyer interruptions (positively correlated with engagement)
        score += min(15.0, inp.interruption_count_buyer * 3.0)
        # Positive sentiment
        score += min(15.0, inp.sentiment_score_positive * 0.3)
        # Decision timeline mentioned
        if inp.decision_timeline_mentioned:
            score += 10.0
        # Next steps agreed
        if inp.next_steps_agreed:
            score += 10.0
        # Negative sentiment penalty
        score -= min(20.0, inp.sentiment_score_negative * 0.4)
        return round(max(0.0, min(100.0, score)), 1)

    def _objection_handling_score(self, inp: CallToneInput) -> float:
        if inp.objection_count == 0:
            return 70.0  # no objections = decent default
        resolution_rate = inp.objection_resolved_count / inp.objection_count
        score = resolution_rate * 80.0
        # Bonus for resolving all objections
        if inp.objection_resolved_count >= inp.objection_count:
            score += 20.0
        # Penalty for high objection count with low resolution
        if inp.objection_count >= 5 and resolution_rate < 0.5:
            score -= 15.0
        # Hesitation keywords suggest unresolved tension
        score -= min(20.0, inp.hesitation_keywords_count * 2.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _conversation_quality_score(self, inp: CallToneInput) -> float:
        score = 40.0
        # Good question ratio by rep
        score += min(20.0, inp.questions_asked_rep * 3.0)
        # Long silences = awkward
        score -= min(20.0, inp.silence_events_long * 4.0)
        # Price pressure from multiple mentions
        if inp.price_mention_count >= 4:
            score -= 15.0
        elif inp.price_mention_count >= 2:
            score -= 5.0
        # Competitor mentions = risk
        score -= min(15.0, inp.competitor_mention_count * 5.0)
        # Next steps = quality indicator
        if inp.next_steps_agreed:
            score += 15.0
        # Duration too short or extremely long
        dur = inp.call_duration_minutes
        if dur < 15:
            score -= 10.0
        elif 30 <= dur <= 60:
            score += 5.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(self, conf: float, engage: float, obj: float, quality: float) -> float:
        composite = conf * 0.30 + engage * 0.30 + obj * 0.25 + quality * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _tone_sentiment(self, inp: CallToneInput, composite: float) -> ToneSentiment:
        if composite >= 65 and inp.sentiment_score_positive > 40:
            return ToneSentiment.POSITIVE
        if composite >= 45:
            return ToneSentiment.NEUTRAL
        if composite >= 30 or inp.sentiment_score_negative > 30:
            return ToneSentiment.CAUTIOUS
        return ToneSentiment.NEGATIVE

    def _dominant_tone(self, inp: CallToneInput, conf: float, engage: float) -> DominantTone:
        if inp.call_ended_abruptly and inp.objection_count > 3:
            return DominantTone.PANIC_SIGNAL
        if engage < 30 and inp.hesitation_keywords_count > 5:
            return DominantTone.EVASIVE
        if inp.objection_count > 4 and inp.sentiment_score_negative > 25:
            return DominantTone.RESISTANT
        if inp.filler_word_rate_per_min >= 3.0 or conf < 40:
            return DominantTone.HESITANT
        if conf >= 70 and inp.talk_time_rep_pct >= 50:
            return DominantTone.AUTHORITATIVE
        if engage >= 65 and inp.enthusiasm_keywords_count >= 5:
            return DominantTone.ENTHUSIASTIC
        return DominantTone.AUTHORITATIVE

    def _conversation_control(self, inp: CallToneInput) -> ConversationControl:
        talk = inp.talk_time_rep_pct
        if inp.call_ended_abruptly and inp.silence_events_long >= 3:
            return ConversationControl.FRAGMENTED
        if talk >= 70:
            return ConversationControl.REP_LED
        if talk <= 30:
            return ConversationControl.BUYER_LED
        return ConversationControl.BALANCED

    def _deal_advancement_probability(self, inp: CallToneInput, composite: float) -> float:
        base = composite
        if inp.next_steps_agreed:
            base = min(100.0, base + 15.0)
        if inp.decision_timeline_mentioned:
            base = min(100.0, base + 10.0)
        if inp.call_ended_abruptly:
            base -= 20.0
        if inp.objection_count > 0:
            resolution_rate = inp.objection_resolved_count / inp.objection_count
            if resolution_rate < 0.5:
                base -= 10.0
        return round(max(0.0, min(100.0, base)), 1)

    def _coaching_priority(self, conf: float, obj_hdl: float, composite: float) -> float:
        score = max(0.0, 100.0 - composite)
        if conf < 40:
            score = min(100.0, score + 20.0)
        if obj_hdl < 40:
            score = min(100.0, score + 15.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _tone_action(
        self,
        sentiment: ToneSentiment,
        is_pos: bool,
        needs_coaching: bool,
    ) -> ToneAction:
        if needs_coaching or sentiment == ToneSentiment.NEGATIVE:
            return ToneAction.INTERVENE
        if sentiment == ToneSentiment.CAUTIOUS:
            return ToneAction.REFRAME
        if sentiment == ToneSentiment.NEUTRAL:
            return ToneAction.NURTURE
        return ToneAction.REINFORCE

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                          0,
                "sentiment_counts":               {},
                "tone_counts":                    {},
                "control_counts":                 {},
                "action_counts":                  {},
                "avg_call_tone_composite":        0.0,
                "positive_call_count":            0,
                "coaching_needed_count":          0,
                "avg_rep_confidence_score":       0.0,
                "avg_buyer_engagement_score":     0.0,
                "avg_objection_handling_score":   0.0,
                "avg_deal_advancement_probability": 0.0,
                "avg_coaching_priority":          0.0,
            }

        sentiment_counts: dict[str, int] = {}
        tone_counts:      dict[str, int] = {}
        control_counts:   dict[str, int] = {}
        action_counts:    dict[str, int] = {}
        total_comp  = 0.0
        total_conf  = 0.0
        total_eng   = 0.0
        total_obj   = 0.0
        total_adv   = 0.0
        total_coach = 0.0

        for r in self._results:
            sentiment_counts[r.tone_sentiment.value]     = sentiment_counts.get(r.tone_sentiment.value, 0) + 1
            tone_counts[r.dominant_tone.value]           = tone_counts.get(r.dominant_tone.value, 0) + 1
            control_counts[r.conversation_control.value] = control_counts.get(r.conversation_control.value, 0) + 1
            action_counts[r.tone_action.value]           = action_counts.get(r.tone_action.value, 0) + 1
            total_comp  += r.call_tone_composite
            total_conf  += r.rep_confidence_score
            total_eng   += r.buyer_engagement_score
            total_obj   += r.objection_handling_score
            total_adv   += r.deal_advancement_probability
            total_coach += r.call_coaching_priority

        return {
            "total":                          n,
            "sentiment_counts":               sentiment_counts,
            "tone_counts":                    tone_counts,
            "control_counts":                 control_counts,
            "action_counts":                  action_counts,
            "avg_call_tone_composite":        round(total_comp / n, 1),
            "positive_call_count":            len(self.positive_calls),
            "coaching_needed_count":          len(self.coaching_needed),
            "avg_rep_confidence_score":       round(total_conf / n, 1),
            "avg_buyer_engagement_score":     round(total_eng / n, 1),
            "avg_objection_handling_score":   round(total_obj / n, 1),
            "avg_deal_advancement_probability": round(total_adv / n, 1),
            "avg_coaching_priority":          round(total_coach / n, 1),
        }
