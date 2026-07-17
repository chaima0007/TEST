from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ConversationQuality(str, Enum):
    POOR        = "poor"
    DEVELOPING  = "developing"
    PROFICIENT  = "proficient"
    ELITE       = "elite"


class ConversationPattern(str, Enum):
    FEATURE_DUMP        = "feature_dump"
    SHALLOW_DISCOVERY   = "shallow_discovery"
    MONOLOGUE           = "monologue"
    BALANCED_DIALOGUE   = "balanced_dialogue"
    CONSULTATIVE        = "consultative"
    CHALLENGER          = "challenger"


class QualificationDepth(str, Enum):
    UNQUALIFIED     = "unqualified"
    SURFACE_LEVEL   = "surface_level"
    MODERATELY_QUALIFIED = "moderately_qualified"
    DEEPLY_QUALIFIED = "deeply_qualified"


class ConversationAction(str, Enum):
    COACH_IMMEDIATELY   = "coach_immediately"
    STRUCTURED_COACHING = "structured_coaching"
    REINFORCE_STRENGTHS = "reinforce_strengths"
    SHARE_AS_EXAMPLE    = "share_as_example"


@dataclass
class ConversationIntelligenceInput:
    call_id:                        str
    deal_id:                        str
    rep_id:                         str
    call_type:                      str     # discovery / demo / followup / negotiation / closing
    talk_listen_ratio:              float   # rep talk time % (lower is better for discovery)
    questions_asked_count:          int     # total questions rep asked
    open_ended_question_pct:        float   # % of questions that were open-ended (0-100)
    pain_point_questions_asked:     int     # questions that uncovered pain points
    budget_discussed:               int     # 1 if budget was discussed
    authority_confirmed:            int     # 1 if decision maker authority was confirmed
    timeline_established:           int     # 1 if timeline was established with buyer
    business_impact_quantified:     int     # 1 if business impact was put in $ terms
    next_steps_defined:             int     # 1 if concrete next steps were defined with dates
    competitor_mentioned_by_buyer:  int     # 1 if buyer mentioned a competitor
    objection_count:                int     # # of objections raised by buyer
    objections_handled_count:       int     # # of objections actually addressed/resolved
    filler_words_per_minute:        float   # um/uh/like rate
    interruptions_count:            int     # # of times rep interrupted buyer
    monologue_longest_seconds:      int     # longest single rep monologue in seconds
    value_statement_count:          int     # # of clear value statements made by rep
    call_duration_minutes:          int     # total call duration in minutes
    deal_value:                     float


@dataclass
class ConversationIntelligenceResult:
    call_id:                    str
    deal_id:                    str
    conversation_quality:       ConversationQuality
    conversation_pattern:       ConversationPattern
    qualification_depth:        QualificationDepth
    conversation_action:        ConversationAction
    discovery_score:            float   # 0-100, how well rep ran discovery
    qualification_score:        float   # 0-100, MEDDIC depth
    communication_score:        float   # 0-100, talk/listen, filler words, interruptions
    value_articulation_score:   float   # 0-100, how well value was communicated
    conversation_composite:     float   # 0-100, overall call quality
    coaching_priority_score:    float   # 0-100, urgency to coach this rep
    deal_advancement_score:     float   # 0-100, likelihood this call advanced the deal
    is_coachable_moment:        bool
    is_exemplary_call:          bool

    def to_dict(self) -> dict:
        return {
            "call_id":                    self.call_id,
            "deal_id":                    self.deal_id,
            "conversation_quality":       self.conversation_quality.value,
            "conversation_pattern":       self.conversation_pattern.value,
            "qualification_depth":        self.qualification_depth.value,
            "conversation_action":        self.conversation_action.value,
            "discovery_score":            self.discovery_score,
            "qualification_score":        self.qualification_score,
            "communication_score":        self.communication_score,
            "value_articulation_score":   self.value_articulation_score,
            "conversation_composite":     self.conversation_composite,
            "coaching_priority_score":    self.coaching_priority_score,
            "deal_advancement_score":     self.deal_advancement_score,
            "is_coachable_moment":        self.is_coachable_moment,
            "is_exemplary_call":          self.is_exemplary_call,
        }


class ConversationIntelligenceScorer:
    def __init__(self) -> None:
        self._results: list[ConversationIntelligenceResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def score(self, inp: ConversationIntelligenceInput) -> ConversationIntelligenceResult:
        discovery   = self._discovery_score(inp)
        qual        = self._qualification_score(inp)
        comm        = self._communication_score(inp)
        value_artic = self._value_articulation_score(inp)
        composite   = self._composite(discovery, qual, comm, value_artic)
        quality     = self._conversation_quality(composite)
        pattern     = self._conversation_pattern(inp, composite)
        qual_depth  = self._qualification_depth(qual)
        coaching    = self._coaching_priority_score(composite, inp)
        advancement = self._deal_advancement_score(inp, composite)
        is_coach    = coaching >= 60.0 or composite < 40.0
        is_exemplary = composite >= 80.0 and advancement >= 75.0
        action      = self._conversation_action(quality, is_exemplary, coaching)

        result = ConversationIntelligenceResult(
            call_id=inp.call_id,
            deal_id=inp.deal_id,
            conversation_quality=quality,
            conversation_pattern=pattern,
            qualification_depth=qual_depth,
            conversation_action=action,
            discovery_score=discovery,
            qualification_score=qual,
            communication_score=comm,
            value_articulation_score=value_artic,
            conversation_composite=composite,
            coaching_priority_score=coaching,
            deal_advancement_score=advancement,
            is_coachable_moment=is_coach,
            is_exemplary_call=is_exemplary,
        )
        self._results.append(result)
        return result

    def score_batch(self, inputs: list[ConversationIntelligenceInput]) -> list[ConversationIntelligenceResult]:
        return [self.score(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def coachable_calls(self) -> list[ConversationIntelligenceResult]:
        return [r for r in self._results if r.is_coachable_moment]

    @property
    def exemplary_calls(self) -> list[ConversationIntelligenceResult]:
        return [r for r in self._results if r.is_exemplary_call]

    @property
    def avg_conversation_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.conversation_composite for r in self._results) / len(self._results), 1)

    @property
    def avg_deal_advancement_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.deal_advancement_score for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _discovery_score(self, inp: ConversationIntelligenceInput) -> float:
        score = 0.0
        # Talk-listen ratio (ideal: rep talks 40-50% in discovery)
        ttl = inp.talk_listen_ratio
        if 35 <= ttl <= 50:
            score += 25.0
        elif 50 < ttl <= 65:
            score += 15.0
        elif ttl > 65:
            score += 5.0
        elif ttl < 35:
            score += 18.0  # buyer talking more isn't bad, just less controlled
        # Question quality
        if inp.questions_asked_count >= 10:
            score += 20.0
        elif inp.questions_asked_count >= 6:
            score += 12.0
        elif inp.questions_asked_count >= 3:
            score += 6.0
        # Open-ended question %
        oeq = inp.open_ended_question_pct
        if oeq >= 70:
            score += 25.0
        elif oeq >= 50:
            score += 15.0
        elif oeq >= 30:
            score += 8.0
        # Pain point questions
        pain = inp.pain_point_questions_asked
        if pain >= 5:
            score += 20.0
        elif pain >= 3:
            score += 12.0
        elif pain >= 1:
            score += 6.0
        # Long monologue = poor discovery
        if inp.monologue_longest_seconds >= 180:
            score -= 15.0
        elif inp.monologue_longest_seconds >= 90:
            score -= 8.0
        return round(max(0.0, min(100.0, score)), 1)

    def _qualification_score(self, inp: ConversationIntelligenceInput) -> float:
        score = 0.0
        # MEDDIC signals
        if inp.budget_discussed:
            score += 20.0
        if inp.authority_confirmed:
            score += 20.0
        if inp.timeline_established:
            score += 20.0
        if inp.business_impact_quantified:
            score += 25.0
        if inp.next_steps_defined:
            score += 15.0
        return round(max(0.0, min(100.0, score)), 1)

    def _communication_score(self, inp: ConversationIntelligenceInput) -> float:
        score = 100.0
        # Filler words penalty
        fillers = inp.filler_words_per_minute
        if fillers >= 8:
            score -= 30.0
        elif fillers >= 5:
            score -= 20.0
        elif fillers >= 3:
            score -= 10.0
        # Interruptions penalty
        interrupts = inp.interruptions_count
        if interrupts >= 5:
            score -= 25.0
        elif interrupts >= 3:
            score -= 15.0
        elif interrupts >= 1:
            score -= 5.0
        # Talk ratio (if demo/closing: higher rep talk ok; discovery: penalize)
        if inp.call_type == "discovery" and inp.talk_listen_ratio > 65:
            score -= 15.0
        elif inp.talk_listen_ratio > 80:
            score -= 15.0
        return round(max(0.0, min(100.0, score)), 1)

    def _value_articulation_score(self, inp: ConversationIntelligenceInput) -> float:
        score = 0.0
        # Value statements made
        value_stmts = inp.value_statement_count
        if value_stmts >= 5:
            score += 35.0
        elif value_stmts >= 3:
            score += 22.0
        elif value_stmts >= 1:
            score += 10.0
        # Business impact quantified = highest quality value articulation
        if inp.business_impact_quantified:
            score += 35.0
        # Next steps = rep closed the loop
        if inp.next_steps_defined:
            score += 20.0
        # Handled objections = shows value defense
        if inp.objection_count > 0:
            handle_rate = inp.objections_handled_count / inp.objection_count
            if handle_rate >= 0.8:
                score += 10.0
            elif handle_rate >= 0.5:
                score += 5.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        discovery: float,
        qual: float,
        comm: float,
        value: float,
    ) -> float:
        composite = discovery * 0.30 + qual * 0.30 + comm * 0.20 + value * 0.20
        return round(max(0.0, min(100.0, composite)), 1)

    def _conversation_quality(self, composite: float) -> ConversationQuality:
        if composite >= 75:
            return ConversationQuality.ELITE
        if composite >= 55:
            return ConversationQuality.PROFICIENT
        if composite >= 35:
            return ConversationQuality.DEVELOPING
        return ConversationQuality.POOR

    def _conversation_pattern(self, inp: ConversationIntelligenceInput, composite: float) -> ConversationPattern:
        # Challenger: high value + quantified impact + handles objections well
        if (inp.business_impact_quantified and inp.value_statement_count >= 4 and
                inp.objection_count > 0 and inp.objections_handled_count >= inp.objection_count * 0.8):
            return ConversationPattern.CHALLENGER
        # Consultative: good discovery + balanced dialogue
        if composite >= 60 and inp.open_ended_question_pct >= 60 and inp.talk_listen_ratio <= 55:
            return ConversationPattern.CONSULTATIVE
        # Balanced dialogue: decent ratio + questions
        if 40 <= inp.talk_listen_ratio <= 60 and inp.questions_asked_count >= 5:
            return ConversationPattern.BALANCED_DIALOGUE
        # Monologue: rep talks too much
        if inp.talk_listen_ratio >= 70 or inp.monologue_longest_seconds >= 180:
            return ConversationPattern.MONOLOGUE
        # Shallow discovery: few meaningful questions
        if inp.pain_point_questions_asked <= 1 and inp.questions_asked_count <= 4:
            return ConversationPattern.SHALLOW_DISCOVERY
        # Feature dump: many value statements but low discovery
        if inp.value_statement_count >= 5 and inp.pain_point_questions_asked <= 1:
            return ConversationPattern.FEATURE_DUMP
        return ConversationPattern.SHALLOW_DISCOVERY

    def _qualification_depth(self, qual: float) -> QualificationDepth:
        if qual >= 75:
            return QualificationDepth.DEEPLY_QUALIFIED
        if qual >= 50:
            return QualificationDepth.MODERATELY_QUALIFIED
        if qual >= 25:
            return QualificationDepth.SURFACE_LEVEL
        return QualificationDepth.UNQUALIFIED

    def _coaching_priority_score(self, composite: float, inp: ConversationIntelligenceInput) -> float:
        # Inverse of quality + severity signals
        base = max(0.0, 100.0 - composite)
        if inp.filler_words_per_minute >= 5:
            base = min(100.0, base + 10.0)
        if inp.interruptions_count >= 3:
            base = min(100.0, base + 10.0)
        if inp.monologue_longest_seconds >= 180:
            base = min(100.0, base + 10.0)
        if inp.next_steps_defined == 0:
            base = min(100.0, base + 8.0)
        return round(max(0.0, min(100.0, base)), 1)

    def _deal_advancement_score(self, inp: ConversationIntelligenceInput, composite: float) -> float:
        score = composite * 0.50
        if inp.next_steps_defined:
            score += 20.0
        if inp.budget_discussed:
            score += 10.0
        if inp.timeline_established:
            score += 10.0
        if inp.business_impact_quantified:
            score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _conversation_action(
        self,
        quality: ConversationQuality,
        is_exemplary: bool,
        coaching: float,
    ) -> ConversationAction:
        if is_exemplary:
            return ConversationAction.SHARE_AS_EXAMPLE
        if quality == ConversationQuality.ELITE:
            return ConversationAction.REINFORCE_STRENGTHS
        if quality == ConversationQuality.POOR or coaching >= 65:
            return ConversationAction.COACH_IMMEDIATELY
        return ConversationAction.STRUCTURED_COACHING

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "quality_counts":               {},
                "pattern_counts":               {},
                "depth_counts":                 {},
                "action_counts":                {},
                "avg_conversation_composite":   0.0,
                "avg_deal_advancement_score":   0.0,
                "coachable_count":              0,
                "exemplary_count":              0,
                "avg_discovery_score":          0.0,
                "avg_qualification_score":      0.0,
                "avg_communication_score":      0.0,
                "avg_value_articulation_score": 0.0,
            }

        quality_counts:  dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        depth_counts:    dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = 0.0
        total_adv  = 0.0
        total_disc = 0.0
        total_qual = 0.0
        total_comm = 0.0
        total_val  = 0.0

        for r in self._results:
            quality_counts[r.conversation_quality.value] = quality_counts.get(r.conversation_quality.value, 0) + 1
            pattern_counts[r.conversation_pattern.value] = pattern_counts.get(r.conversation_pattern.value, 0) + 1
            depth_counts[r.qualification_depth.value]    = depth_counts.get(r.qualification_depth.value, 0) + 1
            action_counts[r.conversation_action.value]   = action_counts.get(r.conversation_action.value, 0) + 1
            total_comp += r.conversation_composite
            total_adv  += r.deal_advancement_score
            total_disc += r.discovery_score
            total_qual += r.qualification_score
            total_comm += r.communication_score
            total_val  += r.value_articulation_score

        return {
            "total":                        n,
            "quality_counts":               quality_counts,
            "pattern_counts":               pattern_counts,
            "depth_counts":                 depth_counts,
            "action_counts":                action_counts,
            "avg_conversation_composite":   round(total_comp / n, 1),
            "avg_deal_advancement_score":   round(total_adv / n, 1),
            "coachable_count":              len(self.coachable_calls),
            "exemplary_count":              len(self.exemplary_calls),
            "avg_discovery_score":          round(total_disc / n, 1),
            "avg_qualification_score":      round(total_qual / n, 1),
            "avg_communication_score":      round(total_comm / n, 1),
            "avg_value_articulation_score": round(total_val / n, 1),
        }
