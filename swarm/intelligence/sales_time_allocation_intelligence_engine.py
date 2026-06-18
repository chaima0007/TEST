from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class TimeRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class TimePattern(str, Enum):
    none                   = "none"
    high_priority_neglect  = "high_priority_neglect"
    admin_overload         = "admin_overload"
    reactive_time_sink     = "reactive_time_sink"
    wrong_size_focus       = "wrong_size_focus"
    renewal_hover          = "renewal_hover"


class TimeSeverity(str, Enum):
    optimized  = "optimized"
    balanced   = "balanced"
    misaligned = "misaligned"
    scattered  = "scattered"


class TimeAction(str, Enum):
    no_action                       = "no_action"
    account_prioritization_coaching = "account_prioritization_coaching"
    admin_reduction_coaching        = "admin_reduction_coaching"
    pipeline_focus_coaching         = "pipeline_focus_coaching"
    time_reallocation_coaching      = "time_reallocation_coaching"
    time_reallocation_intervention  = "time_reallocation_intervention"
    time_strategy_reset             = "time_strategy_reset"


@dataclass
class TimeInput:
    rep_id:                          str
    region:                          str
    evaluation_period_id:            str
    time_on_high_priority_accts_pct: float   # 0-1
    time_on_low_priority_accts_pct:  float   # 0-1
    time_on_admin_tasks_pct:         float   # 0-1
    time_on_pipeline_building_pct:   float   # 0-1
    time_on_existing_customers_pct:  float   # 0-1
    time_on_new_logo_pursuit_pct:    float   # 0-1
    reactive_time_pct:               float   # 0-1
    meeting_prep_time_pct:           float   # 0-1
    crm_update_hrs_per_week_avg:     float   # hours
    avg_selling_hours_per_week:      float   # hours
    accounts_touched_per_week_avg:   float   # count
    high_value_deal_time_ratio:      float   # 0-1
    quota_mapped_time_pct:           float   # 0-1
    strategy_vs_tactical_ratio:      float   # 0-1 (1.0 = all strategic)
    early_stage_deal_time_pct:       float   # 0-1
    late_stage_deal_time_pct:        float   # 0-1
    lost_deal_time_pct:              float   # 0-1
    total_managed_accounts:          int
    avg_opportunity_value_usd:       float


@dataclass
class TimeResult:
    rep_id:                          str
    region:                          str
    time_risk:                       TimeRisk
    time_pattern:                    TimePattern
    time_severity:                   TimeSeverity
    recommended_action:              TimeAction
    priority_allocation_score:       float
    balance_score:                   float
    pipeline_focus_score:            float
    selling_effectiveness_score:     float
    time_composite:                  float
    has_time_gap:                    bool
    requires_time_coaching:          bool
    estimated_quota_risk_usd:        float
    time_signal:                     str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "time_risk":                     self.time_risk.value,
            "time_pattern":                  self.time_pattern.value,
            "time_severity":                 self.time_severity.value,
            "recommended_action":            self.recommended_action.value,
            "priority_allocation_score":     self.priority_allocation_score,
            "balance_score":                 self.balance_score,
            "pipeline_focus_score":          self.pipeline_focus_score,
            "selling_effectiveness_score":   self.selling_effectiveness_score,
            "time_composite":                self.time_composite,
            "has_time_gap":                  self.has_time_gap,
            "requires_time_coaching":        self.requires_time_coaching,
            "estimated_quota_risk_usd":      self.estimated_quota_risk_usd,
            "time_signal":                   self.time_signal,
        }


class SalesTimeAllocationIntelligenceEngine:
    """Detects per-rep time misallocation — priority neglect, admin overload, reactive traps, and pipeline gaps."""

    def __init__(self) -> None:
        self._results: List[TimeResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _priority_allocation_score(self, inp: TimeInput) -> float:
        s = 0.0
        if   inp.time_on_high_priority_accts_pct <= 0.30: s += 40
        elif inp.time_on_high_priority_accts_pct <= 0.50: s += 22
        elif inp.time_on_high_priority_accts_pct <= 0.65: s += 8
        if   inp.high_value_deal_time_ratio      <= 0.30: s += 35
        elif inp.high_value_deal_time_ratio      <= 0.50: s += 18
        if   inp.quota_mapped_time_pct           <= 0.40: s += 25
        elif inp.quota_mapped_time_pct           <= 0.60: s += 12
        return min(s, 100.0)

    def _balance_score(self, inp: TimeInput) -> float:
        s = 0.0
        if   inp.time_on_admin_tasks_pct >= 0.30: s += 40
        elif inp.time_on_admin_tasks_pct >= 0.20: s += 22
        elif inp.time_on_admin_tasks_pct >= 0.12: s += 8
        if   inp.reactive_time_pct       >= 0.60: s += 35
        elif inp.reactive_time_pct       >= 0.40: s += 18
        if   inp.lost_deal_time_pct      >= 0.20: s += 25
        elif inp.lost_deal_time_pct      >= 0.10: s += 12
        return min(s, 100.0)

    def _pipeline_focus_score(self, inp: TimeInput) -> float:
        s = 0.0
        if   inp.time_on_pipeline_building_pct  <= 0.20: s += 45
        elif inp.time_on_pipeline_building_pct  <= 0.35: s += 25
        elif inp.time_on_pipeline_building_pct  <= 0.50: s += 10
        if   inp.time_on_new_logo_pursuit_pct   <= 0.10: s += 30
        elif inp.time_on_new_logo_pursuit_pct   <= 0.25: s += 15
        if   inp.early_stage_deal_time_pct      <= 0.15: s += 25
        elif inp.early_stage_deal_time_pct      <= 0.30: s += 12
        return min(s, 100.0)

    def _selling_effectiveness_score(self, inp: TimeInput) -> float:
        s = 0.0
        if   inp.avg_selling_hours_per_week  <= 25: s += 40
        elif inp.avg_selling_hours_per_week  <= 32: s += 22
        elif inp.avg_selling_hours_per_week  <= 38: s += 8
        if   inp.strategy_vs_tactical_ratio  <= 0.25: s += 35
        elif inp.strategy_vs_tactical_ratio  <= 0.45: s += 18
        if   inp.meeting_prep_time_pct       <= 0.05: s += 25
        elif inp.meeting_prep_time_pct       <= 0.10: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, pa: float, ba: float, pf: float, se: float) -> float:
        return min(round(pa * 0.35 + ba * 0.30 + pf * 0.20 + se * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: TimeInput) -> TimePattern:
        if inp.time_on_high_priority_accts_pct <= 0.25 and inp.high_value_deal_time_ratio <= 0.25:
            return TimePattern.high_priority_neglect
        if inp.time_on_admin_tasks_pct >= 0.35 and inp.avg_selling_hours_per_week <= 28:
            return TimePattern.admin_overload
        if inp.reactive_time_pct >= 0.65 and inp.time_on_pipeline_building_pct <= 0.15:
            return TimePattern.reactive_time_sink
        if inp.time_on_low_priority_accts_pct >= 0.50 and inp.high_value_deal_time_ratio <= 0.30:
            return TimePattern.wrong_size_focus
        if inp.time_on_existing_customers_pct >= 0.65 and inp.time_on_new_logo_pursuit_pct <= 0.15:
            return TimePattern.renewal_hover
        return TimePattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> TimeRisk:
        if   composite >= 60: return TimeRisk.critical
        elif composite >= 40: return TimeRisk.high
        elif composite >= 20: return TimeRisk.moderate
        return TimeRisk.low

    def _severity(self, composite: float) -> TimeSeverity:
        if   composite >= 60: return TimeSeverity.scattered
        elif composite >= 40: return TimeSeverity.misaligned
        elif composite >= 20: return TimeSeverity.balanced
        return TimeSeverity.optimized

    def _action(self, risk: TimeRisk, pattern: TimePattern) -> TimeAction:
        if risk == TimeRisk.critical:
            if pattern == TimePattern.high_priority_neglect:
                return TimeAction.time_strategy_reset
            if pattern == TimePattern.admin_overload:
                return TimeAction.time_reallocation_intervention
            return TimeAction.time_strategy_reset
        if risk == TimeRisk.high:
            if pattern == TimePattern.admin_overload:
                return TimeAction.admin_reduction_coaching
            if pattern == TimePattern.reactive_time_sink:
                return TimeAction.pipeline_focus_coaching
            if pattern == TimePattern.wrong_size_focus:
                return TimeAction.account_prioritization_coaching
            if pattern == TimePattern.renewal_hover:
                return TimeAction.pipeline_focus_coaching
            return TimeAction.time_reallocation_coaching
        if risk == TimeRisk.moderate:
            return TimeAction.account_prioritization_coaching
        return TimeAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: TimeInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.time_on_admin_tasks_pct           >= 0.25
            or inp.time_on_high_priority_accts_pct   <= 0.40
        )

    def _requires_coaching(self, inp: TimeInput, composite: float) -> bool:
        return (
            composite >= 30
            or inp.reactive_time_pct                 >= 0.45
            or inp.high_value_deal_time_ratio        <= 0.40
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _quota_risk(self, inp: TimeInput, composite: float) -> float:
        misalignment = max(0.0, 0.65 - inp.time_on_high_priority_accts_pct)
        return round(
            inp.total_managed_accounts
            * inp.avg_opportunity_value_usd
            * misalignment
            * (composite / 100),
            2,
        )

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        TimePattern.high_priority_neglect: "High-priority neglect",
        TimePattern.admin_overload:        "Admin overload",
        TimePattern.reactive_time_sink:    "Reactive time sink",
        TimePattern.wrong_size_focus:      "Wrong-size focus",
        TimePattern.renewal_hover:         "Renewal hover",
    }

    def _signal(self, inp: TimeInput, pattern: TimePattern, composite: float) -> str:
        if composite < 20:
            return (
                "Time allocation optimized — priority accounts, pipeline building, "
                "and selling hours within benchmarks"
            )
        label      = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        hi_pct     = round(inp.time_on_high_priority_accts_pct * 100)
        admin_pct  = round(inp.time_on_admin_tasks_pct * 100)
        react_pct  = round(inp.reactive_time_pct * 100)
        comp_int   = round(composite)
        return (
            f"{label} — {hi_pct}% time on high-priority accounts — "
            f"{admin_pct}% on admin — "
            f"{react_pct}% reactive — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: TimeInput) -> TimeResult:
        pa  = self._priority_allocation_score(inp)
        ba  = self._balance_score(inp)
        pf  = self._pipeline_focus_score(inp)
        se  = self._selling_effectiveness_score(inp)
        comp = self._composite(pa, ba, pf, se)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = TimeResult(
            rep_id                      = inp.rep_id,
            region                      = inp.region,
            time_risk                   = risk,
            time_pattern                = pattern,
            time_severity               = severity,
            recommended_action          = action,
            priority_allocation_score   = pa,
            balance_score               = ba,
            pipeline_focus_score        = pf,
            selling_effectiveness_score = se,
            time_composite              = comp,
            has_time_gap                = self._has_gap(inp, comp),
            requires_time_coaching      = self._requires_coaching(inp, comp),
            estimated_quota_risk_usd    = self._quota_risk(inp, comp),
            time_signal                 = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[TimeInput]) -> List[TimeResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_time_composite": 0.0,
                "time_gap_count": 0,
                "coaching_count": 0,
                "avg_priority_allocation_score": 0.0,
                "avg_balance_score": 0.0,
                "avg_pipeline_focus_score": 0.0,
                "avg_selling_effectiveness_score": 0.0,
                "total_estimated_quota_risk_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_pa = total_ba = total_pf = total_se = total_qr = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.time_risk.value]       = risk_counts.get(res.time_risk.value, 0) + 1
            pattern_counts[res.time_pattern.value] = pattern_counts.get(res.time_pattern.value, 0) + 1
            severity_counts[res.time_severity.value] = severity_counts.get(res.time_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.time_composite
            total_pa   += res.priority_allocation_score
            total_ba   += res.balance_score
            total_pf   += res.pipeline_focus_score
            total_se   += res.selling_effectiveness_score
            total_qr   += res.estimated_quota_risk_usd
            if res.has_time_gap:         gap_count      += 1
            if res.requires_time_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                              n,
            "risk_counts":                        risk_counts,
            "pattern_counts":                     pattern_counts,
            "severity_counts":                    severity_counts,
            "action_counts":                      action_counts,
            "avg_time_composite":                 round(total_comp / n, 1),
            "time_gap_count":                     gap_count,
            "coaching_count":                     coaching_count,
            "avg_priority_allocation_score":      round(total_pa / n, 1),
            "avg_balance_score":                  round(total_ba / n, 1),
            "avg_pipeline_focus_score":           round(total_pf / n, 1),
            "avg_selling_effectiveness_score":    round(total_se / n, 1),
            "total_estimated_quota_risk_usd":     round(total_qr, 2),
        }
