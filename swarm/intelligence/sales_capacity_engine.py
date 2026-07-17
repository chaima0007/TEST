from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CapacityStatus(str, Enum):
    OVER_CAPACITY      = "over_capacity"
    AT_CAPACITY        = "at_capacity"
    UNDER_CAPACITY     = "under_capacity"
    CRITICAL_SHORTAGE  = "critical_shortage"


class HiringUrgency(str, Enum):
    IMMEDIATE  = "immediate"
    NEAR_TERM  = "near_term"
    PLANNED    = "planned"
    MONITOR    = "monitor"


class CapacityHealth(str, Enum):
    HEALTHY      = "healthy"
    AT_RISK      = "at_risk"
    CONSTRAINED  = "constrained"
    CRITICAL     = "critical"


class CapacityAction(str, Enum):
    HIRE_IMMEDIATELY   = "hire_immediately"
    ACCELERATE_RAMP    = "accelerate_ramp"
    REDISTRIBUTE_QUOTA = "redistribute_quota"
    FOCUS_PRODUCTIVITY = "focus_productivity"
    MAINTAIN_CAPACITY  = "maintain_capacity"
    STRATEGIC_REVIEW   = "strategic_review"


@dataclass
class SalesCapacityInput:
    team_id:                  str
    region:                   str
    segment:                  str              # smb / mid_market / enterprise
    manager_id:               str
    current_reps:             int
    target_reps:              int
    quota_per_rep:            float
    total_team_quota:         float
    avg_attainment_pct:       float            # 0–100 historical average
    new_hires_qtd:            int              # new hires this quarter
    attrition_qtd:            int              # departures this quarter
    avg_ramp_months:          int              # months to full productivity
    ramping_reps:             int              # currently ramping
    pipeline_coverage_ratio:  float            # pipeline / quota
    avg_deal_size:            float
    avg_sales_cycle_days:     int
    historical_win_rate:      float            # 0–1
    target_growth_pct:        float            # revenue growth target %
    days_remaining_period:    int              # days left in period
    productivity_score:       float            # 0–100 current team effectiveness
    open_headcount:           int              # approved unfilled positions
    voluntary_attrition_risk: int              # reps with flight-risk signals


@dataclass
class SalesCapacityResult:
    team_id:                  str
    region:                   str
    capacity_status:          CapacityStatus
    hiring_urgency:           HiringUrgency
    capacity_health:          CapacityHealth
    capacity_action:          CapacityAction
    effective_capacity_pct:   float    # 0–100
    headcount_gap:            int      # target - current (positive = under)
    quota_at_risk:            float    # unprotected quota $
    pipeline_per_rep:         float    # total pipeline / current reps
    required_attainment:      float    # attainment % needed to hit quota
    ramp_impact:              float    # % of team currently ramping
    productivity_index:       float    # 0–100 composite
    is_capacity_constrained:  bool
    needs_immediate_hire:     bool

    def to_dict(self) -> dict:
        return {
            "team_id":                  self.team_id,
            "region":                   self.region,
            "capacity_status":          self.capacity_status.value,
            "hiring_urgency":           self.hiring_urgency.value,
            "capacity_health":          self.capacity_health.value,
            "capacity_action":          self.capacity_action.value,
            "effective_capacity_pct":   self.effective_capacity_pct,
            "headcount_gap":            self.headcount_gap,
            "quota_at_risk":            self.quota_at_risk,
            "pipeline_per_rep":         self.pipeline_per_rep,
            "required_attainment":      self.required_attainment,
            "ramp_impact":              self.ramp_impact,
            "productivity_index":       self.productivity_index,
            "is_capacity_constrained":  self.is_capacity_constrained,
            "needs_immediate_hire":     self.needs_immediate_hire,
        }


class SalesCapacityEngine:
    def __init__(self) -> None:
        self._results: list[SalesCapacityResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: SalesCapacityInput) -> SalesCapacityResult:
        eff_cap       = self._effective_capacity_pct(inp)
        hc_gap        = self._headcount_gap(inp)
        quota_risk    = self._quota_at_risk(inp, eff_cap)
        pipe_per_rep  = self._pipeline_per_rep(inp)
        req_attain    = self._required_attainment(inp)
        ramp_imp      = self._ramp_impact(inp)
        prod_idx      = self._productivity_index(inp, ramp_imp)
        status        = self._capacity_status(eff_cap)
        urgency       = self._hiring_urgency(status, hc_gap)
        health        = self._capacity_health(inp, status, req_attain)
        action        = self._capacity_action(inp, status, urgency, ramp_imp, prod_idx)
        constrained   = status in (CapacityStatus.UNDER_CAPACITY, CapacityStatus.CRITICAL_SHORTAGE)
        immediate     = urgency == HiringUrgency.IMMEDIATE

        result = SalesCapacityResult(
            team_id=inp.team_id,
            region=inp.region,
            capacity_status=status,
            hiring_urgency=urgency,
            capacity_health=health,
            capacity_action=action,
            effective_capacity_pct=eff_cap,
            headcount_gap=hc_gap,
            quota_at_risk=quota_risk,
            pipeline_per_rep=pipe_per_rep,
            required_attainment=req_attain,
            ramp_impact=ramp_imp,
            productivity_index=prod_idx,
            is_capacity_constrained=constrained,
            needs_immediate_hire=immediate,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[SalesCapacityInput]
    ) -> list[SalesCapacityResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def constrained_teams(self) -> list[SalesCapacityResult]:
        return [r for r in self._results if r.is_capacity_constrained]

    @property
    def immediate_hire_teams(self) -> list[SalesCapacityResult]:
        return [r for r in self._results if r.needs_immediate_hire]

    @property
    def critical_teams(self) -> list[SalesCapacityResult]:
        return [r for r in self._results if r.capacity_health == CapacityHealth.CRITICAL]

    @property
    def total_quota_at_risk(self) -> float:
        return round(sum(r.quota_at_risk for r in self._results), 2)

    @property
    def total_headcount_gap(self) -> int:
        return sum(r.headcount_gap for r in self._results)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _effective_capacity_pct(self, inp: SalesCapacityInput) -> float:
        if inp.target_reps <= 0:
            return 0.0
        # Ramping reps count at 40% capacity
        effective_reps = max(0.0, inp.current_reps - inp.ramping_reps * 0.6)
        pct = (effective_reps / inp.target_reps) * inp.avg_attainment_pct
        return round(max(0.0, min(150.0, pct)), 1)

    def _headcount_gap(self, inp: SalesCapacityInput) -> int:
        return max(0, inp.target_reps - inp.current_reps)

    def _quota_at_risk(self, inp: SalesCapacityInput, eff_cap: float) -> float:
        shortfall = max(0.0, 1.0 - eff_cap / 100.0)
        return round(inp.total_team_quota * shortfall, 2)

    def _pipeline_per_rep(self, inp: SalesCapacityInput) -> float:
        reps = max(1, inp.current_reps)
        total_pipeline = inp.total_team_quota * inp.pipeline_coverage_ratio
        return round(total_pipeline / reps, 2)

    def _required_attainment(self, inp: SalesCapacityInput) -> float:
        if inp.current_reps <= 0 or inp.quota_per_rep <= 0:
            return 200.0
        needed = inp.total_team_quota / (inp.current_reps * inp.quota_per_rep) * 100
        return round(min(200.0, needed), 1)

    def _ramp_impact(self, inp: SalesCapacityInput) -> float:
        if inp.current_reps <= 0:
            return 0.0
        return round(min(100.0, (inp.ramping_reps / inp.current_reps) * 100), 1)

    def _productivity_index(self, inp: SalesCapacityInput, ramp_impact: float) -> float:
        # Penalize productivity by proportion of team still ramping
        ramp_penalty = ramp_impact / 200.0  # max 50% penalty
        idx = inp.productivity_score * (1.0 - ramp_penalty)
        # Voluntary attrition risk degrades productivity
        if inp.current_reps > 0:
            idx -= (inp.voluntary_attrition_risk / inp.current_reps) * 10
        return round(max(0.0, min(100.0, idx)), 1)

    def _capacity_status(self, eff_cap: float) -> CapacityStatus:
        if eff_cap >= 100: return CapacityStatus.OVER_CAPACITY
        if eff_cap >= 80:  return CapacityStatus.AT_CAPACITY
        if eff_cap >= 60:  return CapacityStatus.UNDER_CAPACITY
        return CapacityStatus.CRITICAL_SHORTAGE

    def _hiring_urgency(
        self, status: CapacityStatus, hc_gap: int
    ) -> HiringUrgency:
        if status == CapacityStatus.CRITICAL_SHORTAGE:
            return HiringUrgency.IMMEDIATE
        if hc_gap >= 3:
            return HiringUrgency.NEAR_TERM
        if hc_gap >= 1:
            return HiringUrgency.PLANNED
        return HiringUrgency.MONITOR

    def _capacity_health(
        self,
        inp: SalesCapacityInput,
        status: CapacityStatus,
        req_attain: float,
    ) -> CapacityHealth:
        if status == CapacityStatus.CRITICAL_SHORTAGE or req_attain > 130:
            return CapacityHealth.CRITICAL
        if status == CapacityStatus.UNDER_CAPACITY or req_attain > 110:
            return CapacityHealth.CONSTRAINED
        if inp.attrition_qtd > 0 or inp.voluntary_attrition_risk > 0:
            return CapacityHealth.AT_RISK
        return CapacityHealth.HEALTHY

    def _capacity_action(
        self,
        inp: SalesCapacityInput,
        status: CapacityStatus,
        urgency: HiringUrgency,
        ramp_impact: float,
        prod_idx: float,
    ) -> CapacityAction:
        if status == CapacityStatus.CRITICAL_SHORTAGE:
            return CapacityAction.HIRE_IMMEDIATELY
        if ramp_impact > 50:
            return CapacityAction.ACCELERATE_RAMP
        if urgency == HiringUrgency.NEAR_TERM and inp.pipeline_coverage_ratio < 2.0:
            return CapacityAction.REDISTRIBUTE_QUOTA
        if status == CapacityStatus.AT_CAPACITY and prod_idx < 70:
            return CapacityAction.FOCUS_PRODUCTIVITY
        if status in (CapacityStatus.AT_CAPACITY, CapacityStatus.OVER_CAPACITY):
            return CapacityAction.MAINTAIN_CAPACITY
        return CapacityAction.STRATEGIC_REVIEW

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                   0,
                "status_counts":           {},
                "urgency_counts":          {},
                "health_counts":           {},
                "action_counts":           {},
                "avg_effective_capacity":  0.0,
                "avg_required_attainment": 0.0,
                "total_quota_at_risk":     0.0,
                "constrained_count":       0,
                "immediate_hire_count":    0,
                "critical_count":          0,
                "avg_productivity_index":  0.0,
                "total_headcount_gap":     0,
            }

        status_counts:  dict[str, int] = {}
        urgency_counts: dict[str, int] = {}
        health_counts:  dict[str, int] = {}
        action_counts:  dict[str, int] = {}
        total_cap   = 0.0
        total_req   = 0.0
        total_prod  = 0.0

        for r in self._results:
            status_counts[r.capacity_status.value]  = status_counts.get(r.capacity_status.value, 0) + 1
            urgency_counts[r.hiring_urgency.value]  = urgency_counts.get(r.hiring_urgency.value, 0) + 1
            health_counts[r.capacity_health.value]  = health_counts.get(r.capacity_health.value, 0) + 1
            action_counts[r.capacity_action.value]  = action_counts.get(r.capacity_action.value, 0) + 1
            total_cap  += r.effective_capacity_pct
            total_req  += r.required_attainment
            total_prod += r.productivity_index

        return {
            "total":                   n,
            "status_counts":           status_counts,
            "urgency_counts":          urgency_counts,
            "health_counts":           health_counts,
            "action_counts":           action_counts,
            "avg_effective_capacity":  round(total_cap / n, 1),
            "avg_required_attainment": round(total_req / n, 1),
            "total_quota_at_risk":     self.total_quota_at_risk,
            "constrained_count":       len(self.constrained_teams),
            "immediate_hire_count":    len(self.immediate_hire_teams),
            "critical_count":          len(self.critical_teams),
            "avg_productivity_index":  round(total_prod / n, 1),
            "total_headcount_gap":     self.total_headcount_gap,
        }
