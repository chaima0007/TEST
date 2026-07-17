from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ObjectionType(str, Enum):
    PRICE           = "price"
    TIMING          = "timing"
    COMPETITOR      = "competitor"
    STATUS_QUO      = "status_quo"
    RISK            = "risk"
    NO_OBJECTION    = "no_objection"


class ObjectionSeverity(str, Enum):
    MINOR       = "minor"
    MODERATE    = "moderate"
    SERIOUS     = "serious"
    DEAL_BREAKER = "deal_breaker"


class HandlingReadiness(str, Enum):
    PREPARED    = "prepared"
    NEEDS_PREP  = "needs_prep"
    REACTIVE    = "reactive"
    UNPREPARED  = "unprepared"


class ObjectionAction(str, Enum):
    NONE_NEEDED     = "none_needed"
    REFRAME_VALUE   = "reframe_value"
    PROVIDE_PROOF   = "provide_proof"
    EXECUTIVE_CALL  = "executive_call"


@dataclass
class ObjectionPatternInput:
    deal_id:                        str
    deal_name:                      str
    rep_id:                         str
    price_objections_count:         int     # # of price objections raised
    timing_objections_count:        int     # # of timing/not-now objections
    competitor_objections_count:    int     # # of competitor preference objections
    status_quo_objections_count:    int     # # of "we're fine as-is" objections
    risk_objections_count:          int     # # of risk/security/compliance objections
    total_objections_raised:        int     # total objections raised in the deal
    objections_successfully_handled: int   # # objections that were resolved
    objection_reoccurrence_count:   int     # # times same objection came back after handling
    rep_used_battlecard:            int     # 1 if rep used objection battlecard
    rep_asked_discovery_question:   int     # 1 if rep asked clarifying question before answering
    social_proof_used:              int     # 1 if case study/testimonial was used
    roi_calculator_used:            int     # 1 if ROI/business case was provided
    deal_stage_numeric:             int     # 1-6
    deal_size_usd:                  float
    days_to_close:                  int
    objection_raised_in_late_stage: int     # 1 if any objection came up in stage 4+
    competitor_deal_lost_last_90d:  int     # 1 if rep lost a deal to competitor recently
    discovery_call_count:           int     # total discovery calls completed
    avg_objection_response_time_hrs: float  # avg hours to respond to an objection


@dataclass
class ObjectionPatternResult:
    deal_id:                    str
    deal_name:                  str
    primary_objection_type:     ObjectionType
    objection_severity:         ObjectionSeverity
    handling_readiness:         HandlingReadiness
    objection_action:           ObjectionAction
    handling_effectiveness_score: float  # 0-100
    objection_density_score:    float   # 0-100 (how many objections per stage)
    pattern_risk_score:         float   # 0-100 (recurrence + late-stage risk)
    rep_preparedness_score:     float   # 0-100
    objection_composite:        float   # 0-100
    handle_rate:                float   # % of objections handled
    late_stage_risk:            bool
    is_objection_contained:     bool
    needs_coaching:             bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                          self.deal_id,
            "deal_name":                        self.deal_name,
            "primary_objection_type":           self.primary_objection_type.value,
            "objection_severity":               self.objection_severity.value,
            "handling_readiness":               self.handling_readiness.value,
            "objection_action":                 self.objection_action.value,
            "handling_effectiveness_score":     self.handling_effectiveness_score,
            "objection_density_score":          self.objection_density_score,
            "pattern_risk_score":               self.pattern_risk_score,
            "rep_preparedness_score":           self.rep_preparedness_score,
            "objection_composite":              self.objection_composite,
            "handle_rate":                      self.handle_rate,
            "late_stage_risk":                  self.late_stage_risk,
            "is_objection_contained":           self.is_objection_contained,
            "needs_coaching":                   self.needs_coaching,
        }


class ObjectionPatternAnalyzer:
    def __init__(self) -> None:
        self._results: list[ObjectionPatternResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: ObjectionPatternInput) -> ObjectionPatternResult:
        handling    = self._handling_effectiveness_score(inp)
        density     = self._objection_density_score(inp)
        pat_risk    = self._pattern_risk_score(inp)
        prep        = self._rep_preparedness_score(inp)
        composite   = self._composite(handling, density, pat_risk, prep)
        primary     = self._primary_objection_type(inp)
        severity    = self._objection_severity(inp)
        readiness   = self._handling_readiness(prep, inp)
        handle_rate = (
            inp.objections_successfully_handled / inp.total_objections_raised * 100
            if inp.total_objections_raised > 0 else 100.0
        )
        late_risk   = bool(inp.objection_raised_in_late_stage)
        is_contained = composite >= 60 and inp.objection_reoccurrence_count <= 1
        needs_coaching = prep < 40 or inp.objection_reoccurrence_count >= 3 or composite < 40
        action = self._objection_action(severity, needs_coaching, inp)

        result = ObjectionPatternResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            primary_objection_type=primary,
            objection_severity=severity,
            handling_readiness=readiness,
            objection_action=action,
            handling_effectiveness_score=handling,
            objection_density_score=density,
            pattern_risk_score=pat_risk,
            rep_preparedness_score=prep,
            objection_composite=composite,
            handle_rate=round(handle_rate, 1),
            late_stage_risk=late_risk,
            is_objection_contained=is_contained,
            needs_coaching=needs_coaching,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[ObjectionPatternInput]) -> list[ObjectionPatternResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def contained_deals(self) -> list[ObjectionPatternResult]:
        return [r for r in self._results if r.is_objection_contained]

    @property
    def coaching_queue(self) -> list[ObjectionPatternResult]:
        return [r for r in self._results if r.needs_coaching]

    @property
    def avg_objection_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.objection_composite for r in self._results) / len(self._results), 1)

    @property
    def avg_handle_rate(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.handle_rate for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _handling_effectiveness_score(self, inp: ObjectionPatternInput) -> float:
        if inp.total_objections_raised == 0:
            return 85.0  # no objections = easy deal
        score = 0.0
        # Handle rate (weight 50 pts)
        hr = inp.objections_successfully_handled / inp.total_objections_raised
        if hr >= 0.9:
            score += 50.0
        elif hr >= 0.7:
            score += 35.0
        elif hr >= 0.5:
            score += 20.0
        elif hr >= 0.3:
            score += 10.0
        # Reoccurrence penalty
        if inp.objection_reoccurrence_count == 0:
            score += 25.0
        elif inp.objection_reoccurrence_count == 1:
            score += 12.0
        elif inp.objection_reoccurrence_count >= 3:
            score -= 10.0
        # Late-stage objection penalty
        if inp.objection_raised_in_late_stage:
            score -= 15.0
        # Response time
        if inp.avg_objection_response_time_hrs <= 4:
            score += 15.0
        elif inp.avg_objection_response_time_hrs <= 24:
            score += 8.0
        elif inp.avg_objection_response_time_hrs >= 72:
            score -= 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _objection_density_score(self, inp: ObjectionPatternInput) -> float:
        # Fewer objections vs stage = better score (inverted density)
        total = inp.total_objections_raised
        stage = max(1, inp.deal_stage_numeric)
        density = total / stage
        if density == 0:
            score = 90.0
        elif density <= 0.5:
            score = 75.0
        elif density <= 1.0:
            score = 55.0
        elif density <= 2.0:
            score = 35.0
        else:
            score = 15.0
        # Competitor + status-quo combo = high density risk
        if inp.competitor_objections_count >= 2 and inp.status_quo_objections_count >= 2:
            score -= 15.0
        return round(max(0.0, min(100.0, score)), 1)

    def _pattern_risk_score(self, inp: ObjectionPatternInput) -> float:
        # High score = HIGH RISK (inverted for composite)
        risk = 0.0
        if inp.objection_reoccurrence_count >= 3:
            risk += 40.0
        elif inp.objection_reoccurrence_count >= 2:
            risk += 25.0
        elif inp.objection_reoccurrence_count >= 1:
            risk += 10.0
        if inp.objection_raised_in_late_stage:
            risk += 30.0
        if inp.competitor_deal_lost_last_90d:
            risk += 15.0
        if inp.total_objections_raised >= 8:
            risk += 15.0
        elif inp.total_objections_raised >= 5:
            risk += 8.0
        # Invert: high risk = low score for composite
        return round(max(0.0, min(100.0, 100.0 - risk)), 1)

    def _rep_preparedness_score(self, inp: ObjectionPatternInput) -> float:
        score = 0.0
        # Battlecard use (35 pts)
        if inp.rep_used_battlecard:
            score += 35.0
        # Discovery question before answering (25 pts)
        if inp.rep_asked_discovery_question:
            score += 25.0
        # Social proof (20 pts)
        if inp.social_proof_used:
            score += 20.0
        # ROI calculator (15 pts)
        if inp.roi_calculator_used:
            score += 15.0
        # Discovery calls (bonus 5 pts)
        if inp.discovery_call_count >= 3:
            score = min(100.0, score + 5.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        handling: float,
        density: float,
        pat_risk: float,
        prep: float,
    ) -> float:
        composite = handling * 0.35 + density * 0.25 + pat_risk * 0.25 + prep * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _primary_objection_type(self, inp: ObjectionPatternInput) -> ObjectionType:
        if inp.total_objections_raised == 0:
            return ObjectionType.NO_OBJECTION
        counts = {
            ObjectionType.PRICE:        inp.price_objections_count,
            ObjectionType.TIMING:       inp.timing_objections_count,
            ObjectionType.COMPETITOR:   inp.competitor_objections_count,
            ObjectionType.STATUS_QUO:   inp.status_quo_objections_count,
            ObjectionType.RISK:         inp.risk_objections_count,
        }
        return max(counts, key=lambda k: counts[k])

    def _objection_severity(self, inp: ObjectionPatternInput) -> ObjectionSeverity:
        total = inp.total_objections_raised
        if total == 0:
            return ObjectionSeverity.MINOR
        hr = inp.objections_successfully_handled / total
        if inp.objection_raised_in_late_stage and hr < 0.5:
            return ObjectionSeverity.DEAL_BREAKER
        if inp.objection_reoccurrence_count >= 3 or (total >= 6 and hr < 0.6):
            return ObjectionSeverity.SERIOUS
        if inp.objection_reoccurrence_count >= 2 or total >= 4:
            return ObjectionSeverity.MODERATE
        return ObjectionSeverity.MINOR

    def _handling_readiness(self, prep: float, inp: ObjectionPatternInput) -> HandlingReadiness:
        if prep >= 70:
            return HandlingReadiness.PREPARED
        if prep >= 45:
            return HandlingReadiness.NEEDS_PREP
        if prep >= 20:
            return HandlingReadiness.REACTIVE
        return HandlingReadiness.UNPREPARED

    def _objection_action(
        self,
        severity: ObjectionSeverity,
        needs_coaching: bool,
        inp: ObjectionPatternInput,
    ) -> ObjectionAction:
        if severity == ObjectionSeverity.DEAL_BREAKER:
            return ObjectionAction.EXECUTIVE_CALL
        if inp.competitor_objections_count >= 2:
            return ObjectionAction.PROVIDE_PROOF
        if needs_coaching or severity == ObjectionSeverity.SERIOUS:
            return ObjectionAction.REFRAME_VALUE
        return ObjectionAction.NONE_NEEDED

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                            0,
                "objection_type_counts":            {},
                "severity_counts":                  {},
                "readiness_counts":                 {},
                "action_counts":                    {},
                "avg_objection_composite":          0.0,
                "avg_handle_rate":                  0.0,
                "contained_count":                  0,
                "coaching_count":                   0,
                "avg_handling_effectiveness_score": 0.0,
                "avg_pattern_risk_score":           0.0,
                "avg_rep_preparedness_score":       0.0,
                "avg_objection_density_score":      0.0,
            }

        type_counts:     dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        readiness_counts:dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = 0.0; total_hr   = 0.0; total_hdl = 0.0
        total_risk = 0.0; total_prep = 0.0; total_dens = 0.0

        for r in self._results:
            type_counts[r.primary_objection_type.value]  = type_counts.get(r.primary_objection_type.value, 0) + 1
            severity_counts[r.objection_severity.value]  = severity_counts.get(r.objection_severity.value, 0) + 1
            readiness_counts[r.handling_readiness.value] = readiness_counts.get(r.handling_readiness.value, 0) + 1
            action_counts[r.objection_action.value]      = action_counts.get(r.objection_action.value, 0) + 1
            total_comp += r.objection_composite
            total_hr   += r.handle_rate
            total_hdl  += r.handling_effectiveness_score
            total_risk += r.pattern_risk_score
            total_prep += r.rep_preparedness_score
            total_dens += r.objection_density_score

        return {
            "total":                            n,
            "objection_type_counts":            type_counts,
            "severity_counts":                  severity_counts,
            "readiness_counts":                 readiness_counts,
            "action_counts":                    action_counts,
            "avg_objection_composite":          round(total_comp / n, 1),
            "avg_handle_rate":                  round(total_hr / n, 1),
            "contained_count":                  len(self.contained_deals),
            "coaching_count":                   len(self.coaching_queue),
            "avg_handling_effectiveness_score": round(total_hdl / n, 1),
            "avg_pattern_risk_score":           round(total_risk / n, 1),
            "avg_rep_preparedness_score":       round(total_prep / n, 1),
            "avg_objection_density_score":      round(total_dens / n, 1),
        }
