from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional


class ConvRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ConvPattern(str, Enum):
    none                  = "none"
    monologue_seller      = "monologue_seller"
    shallow_questioner    = "shallow_questioner"
    feature_dumper        = "feature_dumper"
    close_avoider         = "close_avoider"
    discovery_skipper     = "discovery_skipper"


class ConvSeverity(str, Enum):
    elite      = "elite"
    proficient = "proficient"
    developing = "developing"
    ineffective = "ineffective"


class ConvAction(str, Enum):
    no_action                    = "no_action"
    listening_coaching           = "listening_coaching"
    questioning_coaching         = "questioning_coaching"
    value_articulation_coaching  = "value_articulation_coaching"
    closing_language_coaching    = "closing_language_coaching"
    discovery_framework_coaching = "discovery_framework_coaching"
    conversation_reset           = "conversation_reset"


@dataclass
class ConvInput:
    rep_id:                           str
    region:                           str
    evaluation_period_id:             str
    avg_talk_to_listen_ratio:         float   # rep talk time / total call time (0–1)
    avg_questions_per_call:           float   # avg number of questions asked
    open_ended_question_rate_pct:     float   # % of questions that are open-ended (0–1)
    discovery_depth_score:            float   # self-assessed or manager-scored 0–10
    next_step_commitment_rate_pct:    float   # % calls ending with clear next step (0–1)
    closing_attempt_rate_pct:         float   # % of closing-stage calls with explicit ask (0–1)
    feature_mention_rate_per_call:    float   # avg features mentioned per call
    pain_articulation_rate_pct:       float   # % calls where buyer pain clearly stated (0–1)
    stakeholder_question_rate_pct:    float   # % calls probing additional stakeholders (0–1)
    objection_handling_rate_pct:      float   # % objections properly addressed (0–1)
    agenda_set_rate_pct:              float   # % calls starting with clear agenda (0–1)
    value_statement_rate_pct:         float   # % calls with explicit value proposition (0–1)
    competitor_mention_rate_pct:      float   # % calls where competitor probed (0–1)
    avg_call_duration_minutes:        float   # average call length
    calls_reviewed_per_month:         int     # how many calls reviewed/coached per month
    total_calls_per_month:            int
    avg_opportunity_value_usd:        float
    active_deal_count:                int


@dataclass
class ConvResult:
    rep_id:                        str
    region:                        str
    conv_risk:                     ConvRisk
    conv_pattern:                  ConvPattern
    conv_severity:                 ConvSeverity
    recommended_action:            ConvAction
    listening_score:               float
    questioning_score:             float
    discovery_score:               float
    closing_effectiveness_score:   float
    conv_composite:                float
    has_conv_gap:                  bool
    requires_conv_coaching:        bool
    estimated_revenue_impact_usd:  float
    conv_signal:                   str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "conv_risk":                     self.conv_risk.value,
            "conv_pattern":                  self.conv_pattern.value,
            "conv_severity":                 self.conv_severity.value,
            "recommended_action":            self.recommended_action.value,
            "listening_score":               self.listening_score,
            "questioning_score":             self.questioning_score,
            "discovery_score":               self.discovery_score,
            "closing_effectiveness_score":   self.closing_effectiveness_score,
            "conv_composite":                self.conv_composite,
            "has_conv_gap":                  self.has_conv_gap,
            "requires_conv_coaching":        self.requires_conv_coaching,
            "estimated_revenue_impact_usd":  self.estimated_revenue_impact_usd,
            "conv_signal":                   self.conv_signal,
        }


class SalesConversationIntelligenceEngine:

    def __init__(self) -> None:
        self._results: List[ConvResult] = []

    # ── sub-scores ──────────────────────────────────────────────────────────

    def _listening_score(self, inp: ConvInput) -> float:
        s = 0.0
        # talk ratio > 0.70 is too much talking
        if inp.avg_talk_to_listen_ratio >= 0.75:
            s += 45
        elif inp.avg_talk_to_listen_ratio >= 0.65:
            s += 28
        elif inp.avg_talk_to_listen_ratio >= 0.55:
            s += 12
        # feature dumping
        if inp.feature_mention_rate_per_call >= 8:
            s += 35
        elif inp.feature_mention_rate_per_call >= 5:
            s += 20
        elif inp.feature_mention_rate_per_call >= 3:
            s += 8
        # value statements help — lack hurts
        if inp.value_statement_rate_pct <= 0.30:
            s += 20
        elif inp.value_statement_rate_pct <= 0.50:
            s += 10
        return min(s, 100.0)

    def _questioning_score(self, inp: ConvInput) -> float:
        s = 0.0
        if inp.avg_questions_per_call <= 3:
            s += 40
        elif inp.avg_questions_per_call <= 6:
            s += 22
        elif inp.avg_questions_per_call <= 9:
            s += 8
        if inp.open_ended_question_rate_pct <= 0.30:
            s += 35
        elif inp.open_ended_question_rate_pct <= 0.50:
            s += 18
        elif inp.open_ended_question_rate_pct <= 0.65:
            s += 6
        if inp.stakeholder_question_rate_pct <= 0.25:
            s += 25
        elif inp.stakeholder_question_rate_pct <= 0.45:
            s += 12
        return min(s, 100.0)

    def _discovery_score(self, inp: ConvInput) -> float:
        s = 0.0
        # pain articulation
        if inp.pain_articulation_rate_pct <= 0.35:
            s += 40
        elif inp.pain_articulation_rate_pct <= 0.55:
            s += 22
        elif inp.pain_articulation_rate_pct <= 0.70:
            s += 8
        # discovery depth (0–10, lower is worse)
        if inp.discovery_depth_score <= 4:
            s += 35
        elif inp.discovery_depth_score <= 6:
            s += 18
        elif inp.discovery_depth_score <= 7.5:
            s += 6
        # agenda setting
        if inp.agenda_set_rate_pct <= 0.40:
            s += 25
        elif inp.agenda_set_rate_pct <= 0.60:
            s += 12
        return min(s, 100.0)

    def _closing_effectiveness_score(self, inp: ConvInput) -> float:
        s = 0.0
        if inp.next_step_commitment_rate_pct <= 0.35:
            s += 40
        elif inp.next_step_commitment_rate_pct <= 0.55:
            s += 22
        elif inp.next_step_commitment_rate_pct <= 0.70:
            s += 8
        if inp.closing_attempt_rate_pct <= 0.30:
            s += 35
        elif inp.closing_attempt_rate_pct <= 0.50:
            s += 18
        elif inp.closing_attempt_rate_pct <= 0.65:
            s += 6
        if inp.objection_handling_rate_pct <= 0.40:
            s += 25
        elif inp.objection_handling_rate_pct <= 0.60:
            s += 12
        return min(s, 100.0)

    def _composite(self, ls: float, qs: float, ds: float, cs: float) -> float:
        return round(ls * 0.30 + qs * 0.25 + ds * 0.25 + cs * 0.20, 2)

    def _pattern(self, inp: ConvInput) -> ConvPattern:
        if inp.avg_talk_to_listen_ratio >= 0.70 and inp.feature_mention_rate_per_call >= 6:
            return ConvPattern.monologue_seller
        if inp.avg_questions_per_call <= 4 and inp.open_ended_question_rate_pct <= 0.35:
            return ConvPattern.shallow_questioner
        if inp.feature_mention_rate_per_call >= 7 and inp.value_statement_rate_pct <= 0.40:
            return ConvPattern.feature_dumper
        if inp.next_step_commitment_rate_pct <= 0.30 and inp.closing_attempt_rate_pct <= 0.35:
            return ConvPattern.close_avoider
        if inp.pain_articulation_rate_pct <= 0.40 and inp.discovery_depth_score <= 5:
            return ConvPattern.discovery_skipper
        return ConvPattern.none

    def _risk(self, composite: float) -> ConvRisk:
        if composite >= 60:
            return ConvRisk.critical
        if composite >= 40:
            return ConvRisk.high
        if composite >= 20:
            return ConvRisk.moderate
        return ConvRisk.low

    def _severity(self, composite: float) -> ConvSeverity:
        if composite >= 60:
            return ConvSeverity.ineffective
        if composite >= 40:
            return ConvSeverity.developing
        if composite >= 20:
            return ConvSeverity.proficient
        return ConvSeverity.elite

    def _action(self, risk: ConvRisk, pattern: ConvPattern) -> ConvAction:
        if risk == ConvRisk.critical:
            if pattern == ConvPattern.monologue_seller:
                return ConvAction.listening_coaching
            if pattern == ConvPattern.close_avoider:
                return ConvAction.closing_language_coaching
            return ConvAction.conversation_reset
        if risk == ConvRisk.high:
            if pattern == ConvPattern.shallow_questioner:
                return ConvAction.questioning_coaching
            if pattern == ConvPattern.feature_dumper:
                return ConvAction.value_articulation_coaching
            if pattern == ConvPattern.discovery_skipper:
                return ConvAction.discovery_framework_coaching
            if pattern == ConvPattern.close_avoider:
                return ConvAction.closing_language_coaching
            return ConvAction.listening_coaching
        if risk == ConvRisk.moderate:
            return ConvAction.questioning_coaching
        return ConvAction.no_action

    def _has_gap(self, inp: ConvInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.avg_talk_to_listen_ratio >= 0.65
            or inp.avg_questions_per_call <= 5
        )

    def _requires_coaching(self, inp: ConvInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.open_ended_question_rate_pct <= 0.45
            or inp.next_step_commitment_rate_pct <= 0.55
        )

    def _revenue_impact(self, inp: ConvInput, composite: float) -> float:
        return round(
            inp.active_deal_count
            * inp.avg_opportunity_value_usd
            * max(0.0, inp.avg_talk_to_listen_ratio - 0.40)
            * (composite / 100.0),
            2,
        )

    def _signal(self, inp: ConvInput, pattern: ConvPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Conversation quality strong — listening ratio, questioning depth, "
                "and closing effectiveness within benchmarks"
            )
        labels = {
            ConvPattern.monologue_seller:   "Monologue seller",
            ConvPattern.shallow_questioner: "Shallow questioner",
            ConvPattern.feature_dumper:     "Feature dumper",
            ConvPattern.close_avoider:      "Close avoider",
            ConvPattern.discovery_skipper:  "Discovery skipper",
        }
        label = labels.get(pattern, "Conversation gap detected")
        talk_pct  = round(inp.avg_talk_to_listen_ratio * 100)
        q_per_call = round(inp.avg_questions_per_call, 1)
        ns_pct    = round(inp.next_step_commitment_rate_pct * 100)
        comp_int  = round(composite)
        return (
            f"{label} — {talk_pct}% rep talk time — "
            f"{q_per_call} questions/call — "
            f"{ns_pct}% calls with next step — composite {comp_int}"
        )

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: ConvInput) -> ConvResult:
        ls = self._listening_score(inp)
        qs = self._questioning_score(inp)
        ds = self._discovery_score(inp)
        cs = self._closing_effectiveness_score(inp)
        comp = self._composite(ls, qs, ds, cs)
        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)
        result = ConvResult(
            rep_id                       = inp.rep_id,
            region                       = inp.region,
            conv_risk                    = risk,
            conv_pattern                 = pattern,
            conv_severity                = severity,
            recommended_action           = action,
            listening_score              = round(ls, 2),
            questioning_score            = round(qs, 2),
            discovery_score              = round(ds, 2),
            closing_effectiveness_score  = round(cs, 2),
            conv_composite               = comp,
            has_conv_gap                 = self._has_gap(inp, comp),
            requires_conv_coaching       = self._requires_coaching(inp, comp),
            estimated_revenue_impact_usd = self._revenue_impact(inp, comp),
            conv_signal                  = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ConvInput]) -> List[ConvResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        rr = self._results
        if not rr:
            return {
                "total": 0, "risk_counts": {}, "pattern_counts": {},
                "severity_counts": {}, "action_counts": {},
                "avg_conv_composite": 0.0, "conv_gap_count": 0,
                "coaching_count": 0, "avg_listening_score": 0.0,
                "avg_questioning_score": 0.0, "avg_discovery_score": 0.0,
                "avg_closing_effectiveness_score": 0.0,
                "total_estimated_revenue_impact_usd": 0.0,
            }
        n = len(rr)
        risk_c: Dict[str, int] = {}
        pat_c:  Dict[str, int] = {}
        sev_c:  Dict[str, int] = {}
        act_c:  Dict[str, int] = {}
        tl = ts = td = tc = trev = 0.0
        gap_c = coach_c = 0
        for r in rr:
            risk_c[r.conv_risk.value]        = risk_c.get(r.conv_risk.value, 0) + 1
            pat_c[r.conv_pattern.value]      = pat_c.get(r.conv_pattern.value, 0) + 1
            sev_c[r.conv_severity.value]     = sev_c.get(r.conv_severity.value, 0) + 1
            act_c[r.recommended_action.value]= act_c.get(r.recommended_action.value, 0) + 1
            tl   += r.listening_score
            ts   += r.questioning_score
            td   += r.discovery_score
            tc   += r.closing_effectiveness_score
            trev += r.estimated_revenue_impact_usd
            gap_c   += r.has_conv_gap
            coach_c += r.requires_conv_coaching
        return {
            "total":                               n,
            "risk_counts":                         risk_c,
            "pattern_counts":                      pat_c,
            "severity_counts":                     sev_c,
            "action_counts":                       act_c,
            "avg_conv_composite":                  round(sum(r.conv_composite for r in rr) / n, 1),
            "conv_gap_count":                      gap_c,
            "coaching_count":                      coach_c,
            "avg_listening_score":                 round(tl / n, 1),
            "avg_questioning_score":               round(ts / n, 1),
            "avg_discovery_score":                 round(td / n, 1),
            "avg_closing_effectiveness_score":     round(tc / n, 1),
            "total_estimated_revenue_impact_usd":  round(trev, 2),
        }
