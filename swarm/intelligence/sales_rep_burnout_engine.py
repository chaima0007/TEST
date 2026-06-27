from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BurnoutRisk(str, Enum):
    MINIMAL  = "minimal"
    BUILDING = "building"
    HIGH     = "high"
    CRITICAL = "critical"


class BurnoutCategory(str, Enum):
    HEALTHY     = "healthy"
    STRESSED    = "stressed"
    OVERLOADED  = "overloaded"
    BURNED_OUT  = "burned_out"


class BurnoutPattern(str, Enum):
    STABLE      = "stable"
    OVERWORKING = "overworking"
    DISENGAGING = "disengaging"
    DECLINING   = "declining"


class BurnoutAction(str, Enum):
    MONITOR                = "monitor"
    WORKLOAD_REVIEW        = "workload_review"
    COACHING               = "coaching"
    IMMEDIATE_INTERVENTION = "immediate_intervention"


@dataclass
class SalesRepBurnoutInput:
    rep_id:                    str
    rep_name:                  str
    manager_id:                str
    region:                    str
    activities_per_day_current:  float    # avg daily activities this month
    activities_per_day_prev:     float    # avg daily activities last month
    activities_per_day_avg:      float    # 12-month baseline average
    deals_closed_this_quarter:   int      # deals closed current quarter
    deals_closed_last_quarter:   int      # deals closed last quarter
    deals_stalled_pct:           float    # % of pipeline currently stalled (0–100)
    new_deals_added_mtd:         int      # new opportunities added this month
    new_deals_prev_month:        int      # new opportunities added last month
    win_rate_current:            float    # current quarter win rate (0–100)
    win_rate_prev_quarter:       float    # previous quarter win rate (0–100)
    avg_response_time_hours:     float    # avg email/call response time in hours
    meetings_attended_this_week: int      # meetings attended this week
    meetings_attended_avg_week:  float    # average meetings per week (12-month)
    pto_days_taken_qtd:          int      # PTO days taken this quarter
    pto_days_remaining:          int      # remaining PTO days
    sick_days_this_quarter:      int      # sick days this quarter
    late_submissions:            int      # CRM/admin submissions made late this month
    coaching_sessions_declined:  int      # coaching sessions declined or rescheduled


@dataclass
class SalesRepBurnoutResult:
    rep_id:                       str
    rep_name:                     str
    burnout_risk:                 BurnoutRisk
    burnout_category:             BurnoutCategory
    burnout_pattern:              BurnoutPattern
    burnout_action:               BurnoutAction
    overwork_score:               float    # 0–100, higher = more overworked
    disengagement_score:          float    # 0–100, higher = more disengaged
    performance_decline_score:    float    # 0–100, higher = more declining
    wellbeing_score:              float    # 0–100, higher = better wellbeing
    burnout_composite_score:      float    # 0–100, higher = more at risk
    predicted_turnover_probability: float  # 0–100
    intervention_urgency_score:   float    # 0–100
    is_at_risk:                   bool
    needs_immediate_action:       bool

    def to_dict(self) -> dict:
        return {
            "rep_id":                         self.rep_id,
            "rep_name":                       self.rep_name,
            "burnout_risk":                   self.burnout_risk.value,
            "burnout_category":               self.burnout_category.value,
            "burnout_pattern":                self.burnout_pattern.value,
            "burnout_action":                 self.burnout_action.value,
            "overwork_score":                 self.overwork_score,
            "disengagement_score":            self.disengagement_score,
            "performance_decline_score":      self.performance_decline_score,
            "wellbeing_score":                self.wellbeing_score,
            "burnout_composite_score":        self.burnout_composite_score,
            "predicted_turnover_probability": self.predicted_turnover_probability,
            "intervention_urgency_score":     self.intervention_urgency_score,
            "is_at_risk":                     self.is_at_risk,
            "needs_immediate_action":         self.needs_immediate_action,
        }


class SalesRepBurnoutEngine:
    def __init__(self) -> None:
        self._results: list[SalesRepBurnoutResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: SalesRepBurnoutInput) -> SalesRepBurnoutResult:
        overwork    = self._overwork_score(inp)
        disengage   = self._disengagement_score(inp)
        perf_dec    = self._performance_decline_score(inp)
        wellbeing   = self._wellbeing_score(inp)
        composite   = self._burnout_composite(overwork, disengage, perf_dec, wellbeing)
        turnover    = self._predicted_turnover_probability(inp, composite)
        urgency     = self._intervention_urgency(inp, composite, turnover)
        risk        = self._burnout_risk(composite)
        category    = self._burnout_category(composite, overwork, disengage)
        pattern     = self._burnout_pattern(overwork, disengage, perf_dec)
        is_at_risk  = composite >= 55.0 or risk in (BurnoutRisk.HIGH, BurnoutRisk.CRITICAL)
        needs_imm   = composite >= 70.0 or turnover >= 65.0 or urgency >= 75.0
        action      = self._burnout_action(risk, pattern, composite, needs_imm)

        result = SalesRepBurnoutResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            burnout_risk=risk,
            burnout_category=category,
            burnout_pattern=pattern,
            burnout_action=action,
            overwork_score=overwork,
            disengagement_score=disengage,
            performance_decline_score=perf_dec,
            wellbeing_score=wellbeing,
            burnout_composite_score=composite,
            predicted_turnover_probability=turnover,
            intervention_urgency_score=urgency,
            is_at_risk=is_at_risk,
            needs_immediate_action=needs_imm,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[SalesRepBurnoutInput]
    ) -> list[SalesRepBurnoutResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_reps(self) -> list[SalesRepBurnoutResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def immediate_action_reps(self) -> list[SalesRepBurnoutResult]:
        return [r for r in self._results if r.needs_immediate_action]

    @property
    def healthy_reps(self) -> list[SalesRepBurnoutResult]:
        return [r for r in self._results if r.burnout_category == BurnoutCategory.HEALTHY]

    @property
    def avg_burnout_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.burnout_composite_score for r in self._results) / len(self._results), 1)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _overwork_score(self, inp: SalesRepBurnoutInput) -> float:
        score = 0.0
        # Activity vs baseline (up to 40) — high overwork = activities far above avg
        if inp.activities_per_day_avg > 0:
            activity_ratio = inp.activities_per_day_current / inp.activities_per_day_avg
            if activity_ratio > 1.3:
                score += min(40.0, (activity_ratio - 1.0) * 50.0)
        # Meeting overload vs avg (up to 30)
        if inp.meetings_attended_avg_week > 0:
            meeting_ratio = inp.meetings_attended_this_week / inp.meetings_attended_avg_week
            if meeting_ratio > 1.2:
                score += min(30.0, (meeting_ratio - 1.0) * 40.0)
        # Response time pressure (up to 30) — very fast response as overwork signal
        if inp.avg_response_time_hours <= 0.5:
            score += 25.0
        elif inp.avg_response_time_hours <= 1.0:
            score += 15.0
        elif inp.avg_response_time_hours <= 2.0:
            score += 5.0
        return round(max(0.0, min(100.0, score)), 1)

    def _disengagement_score(self, inp: SalesRepBurnoutInput) -> float:
        score = 0.0
        # Activity drop vs prev month (up to 35)
        if inp.activities_per_day_prev > 0:
            activity_drop = (inp.activities_per_day_prev - inp.activities_per_day_current) / inp.activities_per_day_prev
            if activity_drop > 0:
                score += min(35.0, activity_drop * 70.0)
        # New deal creation drop (up to 30)
        if inp.new_deals_prev_month > 0:
            deal_drop = (inp.new_deals_prev_month - inp.new_deals_added_mtd) / inp.new_deals_prev_month
            if deal_drop > 0:
                score += min(30.0, deal_drop * 50.0)
        # Late CRM submissions (up to 20)
        score += min(20.0, inp.late_submissions * 4.0)
        # Coaching sessions declined (up to 15)
        score += min(15.0, inp.coaching_sessions_declined * 5.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _performance_decline_score(self, inp: SalesRepBurnoutInput) -> float:
        score = 0.0
        # Win rate decline (up to 40)
        win_rate_drop = inp.win_rate_prev_quarter - inp.win_rate_current
        if win_rate_drop > 0:
            score += min(40.0, win_rate_drop * 1.2)
        # Closed deals decline quarter-over-quarter (up to 35)
        if inp.deals_closed_last_quarter > 0:
            closed_drop = (inp.deals_closed_last_quarter - inp.deals_closed_this_quarter) / inp.deals_closed_last_quarter
            if closed_drop > 0:
                score += min(35.0, closed_drop * 60.0)
        # Pipeline stall rate (up to 25)
        score += min(25.0, inp.deals_stalled_pct * 0.4)
        return round(max(0.0, min(100.0, score)), 1)

    def _wellbeing_score(self, inp: SalesRepBurnoutInput) -> float:
        score = 50.0  # neutral baseline
        # PTO usage positive (rep is taking breaks)
        if inp.pto_days_taken_qtd >= 3:
            score += 15.0
        elif inp.pto_days_taken_qtd >= 1:
            score += 7.0
        # Sick days signal exhaustion
        score -= min(25.0, inp.sick_days_this_quarter * 8.0)
        # PTO not taken (hoarding PTO = potential burnout)
        if inp.pto_days_remaining > 15:
            score -= 10.0
        elif inp.pto_days_remaining > 10:
            score -= 5.0
        # Reasonable response time = not hypervigilant
        if 2.0 <= inp.avg_response_time_hours <= 8.0:
            score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _burnout_composite(
        self,
        overwork: float,
        disengage: float,
        perf_dec: float,
        wellbeing: float,
    ) -> float:
        # Wellbeing is inverse (high wellbeing = low burnout risk)
        wellbeing_risk = 100.0 - wellbeing
        score = (
            overwork      * 0.30 +
            disengage     * 0.30 +
            perf_dec      * 0.25 +
            wellbeing_risk * 0.15
        )
        return round(max(0.0, min(100.0, score)), 1)

    def _predicted_turnover_probability(
        self, inp: SalesRepBurnoutInput, composite: float
    ) -> float:
        base = composite * 0.75
        # Boost if high sick days + no PTO taken
        if inp.sick_days_this_quarter >= 3 and inp.pto_days_remaining > 10:
            base = min(100.0, base + 15.0)
        # Boost if coaching consistently declined
        if inp.coaching_sessions_declined >= 3:
            base = min(100.0, base + 10.0)
        # Boost if performance declining alongside high stall
        if inp.deals_stalled_pct >= 50 and inp.win_rate_current < inp.win_rate_prev_quarter:
            base = min(100.0, base + 8.0)
        return round(max(0.0, min(100.0, base)), 1)

    def _intervention_urgency(
        self, inp: SalesRepBurnoutInput, composite: float, turnover: float
    ) -> float:
        urgency = (composite * 0.6 + turnover * 0.4)
        # Recency boost if recently declining
        if inp.activities_per_day_current < inp.activities_per_day_prev * 0.7:
            urgency = min(100.0, urgency + 10.0)
        return round(max(0.0, min(100.0, urgency)), 1)

    def _burnout_risk(self, composite: float) -> BurnoutRisk:
        if composite >= 70:
            return BurnoutRisk.CRITICAL
        if composite >= 50:
            return BurnoutRisk.HIGH
        if composite >= 30:
            return BurnoutRisk.BUILDING
        return BurnoutRisk.MINIMAL

    def _burnout_category(
        self, composite: float, overwork: float, disengage: float
    ) -> BurnoutCategory:
        if composite >= 70:
            return BurnoutCategory.BURNED_OUT
        if overwork >= 50:
            return BurnoutCategory.OVERLOADED
        if disengage >= 50 or composite >= 40:
            return BurnoutCategory.STRESSED
        return BurnoutCategory.HEALTHY

    def _burnout_pattern(
        self, overwork: float, disengage: float, perf_dec: float
    ) -> BurnoutPattern:
        if perf_dec >= 50:
            return BurnoutPattern.DECLINING
        if overwork >= 45:
            return BurnoutPattern.OVERWORKING
        if disengage >= 45:
            return BurnoutPattern.DISENGAGING
        return BurnoutPattern.STABLE

    def _burnout_action(
        self,
        risk: BurnoutRisk,
        pattern: BurnoutPattern,
        composite: float,
        needs_imm: bool,
    ) -> BurnoutAction:
        if needs_imm or risk == BurnoutRisk.CRITICAL:
            return BurnoutAction.IMMEDIATE_INTERVENTION
        if risk == BurnoutRisk.HIGH:
            return BurnoutAction.COACHING
        if pattern == BurnoutPattern.OVERWORKING:
            return BurnoutAction.WORKLOAD_REVIEW
        if composite >= 30:
            return BurnoutAction.COACHING
        return BurnoutAction.MONITOR

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                          0,
                "risk_counts":                    {},
                "category_counts":                {},
                "pattern_counts":                 {},
                "action_counts":                  {},
                "avg_burnout_composite_score":    0.0,
                "avg_predicted_turnover_probability": 0.0,
                "at_risk_count":                  0,
                "immediate_action_count":         0,
                "avg_overwork_score":             0.0,
                "avg_disengagement_score":        0.0,
                "avg_performance_decline_score":  0.0,
                "avg_wellbeing_score":            0.0,
            }

        risk_counts:     dict[str, int] = {}
        category_counts: dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_composite  = 0.0
        total_turnover   = 0.0
        total_overwork   = 0.0
        total_disengage  = 0.0
        total_perf_dec   = 0.0
        total_wellbeing  = 0.0

        for r in self._results:
            risk_counts[r.burnout_risk.value]         = risk_counts.get(r.burnout_risk.value, 0) + 1
            category_counts[r.burnout_category.value] = category_counts.get(r.burnout_category.value, 0) + 1
            pattern_counts[r.burnout_pattern.value]   = pattern_counts.get(r.burnout_pattern.value, 0) + 1
            action_counts[r.burnout_action.value]     = action_counts.get(r.burnout_action.value, 0) + 1
            total_composite += r.burnout_composite_score
            total_turnover  += r.predicted_turnover_probability
            total_overwork  += r.overwork_score
            total_disengage += r.disengagement_score
            total_perf_dec  += r.performance_decline_score
            total_wellbeing += r.wellbeing_score

        return {
            "total":                              n,
            "risk_counts":                        risk_counts,
            "category_counts":                    category_counts,
            "pattern_counts":                     pattern_counts,
            "action_counts":                      action_counts,
            "avg_burnout_composite_score":        round(total_composite / n, 1),
            "avg_predicted_turnover_probability": round(total_turnover / n, 1),
            "at_risk_count":                      len(self.at_risk_reps),
            "immediate_action_count":             len(self.immediate_action_reps),
            "avg_overwork_score":                 round(total_overwork / n, 1),
            "avg_disengagement_score":            round(total_disengage / n, 1),
            "avg_performance_decline_score":      round(total_perf_dec / n, 1),
            "avg_wellbeing_score":                round(total_wellbeing / n, 1),
        }
