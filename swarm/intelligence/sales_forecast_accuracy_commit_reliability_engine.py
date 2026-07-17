"""
Module 217 — Sales Forecast Accuracy & Commit Reliability Engine
Measures how accurately reps forecast their commits vs actual close rates,
detects sandbagging, overcommitting, and chronic forecast drift patterns.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ForecastRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ForecastPattern(str, Enum):
    none                = "none"
    chronic_overcommit  = "chronic_overcommit"
    sandbagger          = "sandbagger"
    commit_drifter      = "commit_drifter"
    late_push_abuser    = "late_push_abuser"
    category_manipulator = "category_manipulator"


class ForecastSeverity(str, Enum):
    accurate    = "accurate"
    drifting    = "drifting"
    unreliable  = "unreliable"
    blind_spot  = "blind_spot"


class ForecastAction(str, Enum):
    no_action                        = "no_action"
    forecast_monitoring              = "forecast_monitoring"
    commit_cadence_coaching          = "commit_cadence_coaching"
    pipeline_review_increase         = "pipeline_review_increase"
    forecast_hygiene_training        = "forecast_hygiene_training"
    manager_forecast_alignment       = "manager_forecast_alignment"
    deal_by_deal_review              = "deal_by_deal_review"
    forecast_process_reset           = "forecast_process_reset"
    executive_forecast_audit         = "executive_forecast_audit"


@dataclass
class ForecastInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    # Commit accuracy
    commit_vs_actual_variance_pct: float        # avg % variance between commit and close
    overcommit_frequency_pct: float             # % periods rep commits more than closes
    undercommit_frequency_pct: float            # % periods rep commits less than closes (sandbagging)
    forecast_miss_rate_pct: float               # % quarters forecast missed by >15%
    # Category discipline
    commit_category_accuracy_pct: float         # % deals forecast in right category (commit/best-case/pipeline)
    best_case_to_close_conversion_pct: float    # % best-case deals that actually close
    pipeline_to_commit_escalation_rate_pct: float  # % pipeline deals pushed to commit <14 days before close
    category_downgrade_rate_pct: float          # % deals moved from commit to pipeline
    # Timing patterns
    last_week_close_rate_pct: float             # % of deals closed in final week of period
    pull_in_frequency_pct: float                # % of closes pulled in from future periods
    push_out_frequency_pct: float               # % of commits pushed to next period
    avg_days_in_commit_before_close: float      # avg days a deal stays in commit before closing
    # Data quality
    crm_forecast_update_frequency_days: float   # avg days between CRM forecast updates
    deal_stage_accuracy_at_commit_pct: float    # % of commit deals in correct CRM stage
    close_date_change_frequency: float          # avg number of close date changes per deal
    # Historical reliability
    rolling_3q_forecast_accuracy_pct: float     # 3-quarter rolling forecast accuracy
    upside_capture_rate_pct: float              # % of upside deals actually captured
    # Volume context
    total_commit_deals: int
    avg_deal_value_usd: float
    quota_attainment_pct: float


@dataclass
class ForecastResult:
    rep_id: str
    region: str
    forecast_risk: str
    forecast_pattern: str
    forecast_severity: str
    recommended_action: str
    accuracy_score: float
    discipline_score: float
    timing_score: float
    reliability_score: float
    forecast_composite: float
    has_forecast_gap: bool
    requires_manager_review: bool
    estimated_forecast_error_usd: float
    forecast_signal: str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                      self.rep_id,
            "region":                      self.region,
            "forecast_risk":               self.forecast_risk,
            "forecast_pattern":            self.forecast_pattern,
            "forecast_severity":           self.forecast_severity,
            "recommended_action":          self.recommended_action,
            "accuracy_score":              self.accuracy_score,
            "discipline_score":            self.discipline_score,
            "timing_score":                self.timing_score,
            "reliability_score":           self.reliability_score,
            "forecast_composite":          self.forecast_composite,
            "has_forecast_gap":            self.has_forecast_gap,
            "requires_manager_review":     self.requires_manager_review,
            "estimated_forecast_error_usd": self.estimated_forecast_error_usd,
            "forecast_signal":             self.forecast_signal,
        }


class SalesForecastAccuracyCommitReliabilityEngine:
    def __init__(self) -> None:
        self._results: List[ForecastResult] = []

    # ── Sub-scores ────────────────────────────────────────────────────────────

    def _accuracy_score(self, i: ForecastInput) -> float:
        s = 0
        if   i.commit_vs_actual_variance_pct   >= 0.40: s += 40
        elif i.commit_vs_actual_variance_pct   >= 0.22: s += 22
        elif i.commit_vs_actual_variance_pct   >= 0.10: s += 8

        if   i.forecast_miss_rate_pct          >= 0.60: s += 35
        elif i.forecast_miss_rate_pct          >= 0.40: s += 18
        elif i.forecast_miss_rate_pct          >= 0.20: s += 6

        if   i.rolling_3q_forecast_accuracy_pct <= 0.55: s += 25
        elif i.rolling_3q_forecast_accuracy_pct <= 0.70: s += 12
        return min(s, 100)

    def _discipline_score(self, i: ForecastInput) -> float:
        s = 0
        if   i.commit_category_accuracy_pct    <= 0.40: s += 45
        elif i.commit_category_accuracy_pct    <= 0.60: s += 25
        elif i.commit_category_accuracy_pct    <= 0.75: s += 10

        if   i.category_downgrade_rate_pct     >= 0.35: s += 30
        elif i.category_downgrade_rate_pct     >= 0.20: s += 15

        if   i.close_date_change_frequency     >= 3.0:  s += 25
        elif i.close_date_change_frequency     >= 2.0:  s += 12
        return min(s, 100)

    def _timing_score(self, i: ForecastInput) -> float:
        s = 0
        if   i.last_week_close_rate_pct        >= 0.55: s += 40
        elif i.last_week_close_rate_pct        >= 0.35: s += 22
        elif i.last_week_close_rate_pct        >= 0.20: s += 8

        if   i.pipeline_to_commit_escalation_rate_pct >= 0.40: s += 35
        elif i.pipeline_to_commit_escalation_rate_pct >= 0.25: s += 18

        if   i.push_out_frequency_pct          >= 0.45: s += 25
        elif i.push_out_frequency_pct          >= 0.28: s += 12
        return min(s, 100)

    def _reliability_score(self, i: ForecastInput) -> float:
        s = 0
        if   i.overcommit_frequency_pct        >= 0.60: s += 40
        elif i.overcommit_frequency_pct        >= 0.40: s += 22
        elif i.overcommit_frequency_pct        >= 0.22: s += 8

        if   i.undercommit_frequency_pct       >= 0.55: s += 35
        elif i.undercommit_frequency_pct       >= 0.35: s += 18

        if   i.crm_forecast_update_frequency_days >= 7.0: s += 25
        elif i.crm_forecast_update_frequency_days >= 4.0: s += 12
        return min(s, 100)

    # ── Composite ─────────────────────────────────────────────────────────────

    def _composite(self, ac: float, di: float, ti: float, re: float) -> float:
        return min(round(ac * 0.30 + di * 0.25 + ti * 0.25 + re * 0.20, 2), 100.0)

    # ── Risk / Severity ───────────────────────────────────────────────────────

    def _risk(self, c: float) -> ForecastRisk:
        if c >= 60: return ForecastRisk.critical
        if c >= 40: return ForecastRisk.high
        if c >= 20: return ForecastRisk.moderate
        return ForecastRisk.low

    def _severity(self, c: float) -> ForecastSeverity:
        if c >= 60: return ForecastSeverity.blind_spot
        if c >= 40: return ForecastSeverity.unreliable
        if c >= 20: return ForecastSeverity.drifting
        return ForecastSeverity.accurate

    # ── Pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, i: ForecastInput) -> ForecastPattern:
        if (i.overcommit_frequency_pct >= 0.55
                and i.commit_vs_actual_variance_pct >= 0.30):
            return ForecastPattern.chronic_overcommit
        if (i.undercommit_frequency_pct >= 0.50
                and i.rolling_3q_forecast_accuracy_pct >= 0.80):
            return ForecastPattern.sandbagger
        if (i.push_out_frequency_pct >= 0.40
                and i.close_date_change_frequency >= 2.5):
            return ForecastPattern.commit_drifter
        if (i.last_week_close_rate_pct >= 0.50
                and i.pipeline_to_commit_escalation_rate_pct >= 0.35):
            return ForecastPattern.late_push_abuser
        if (i.category_downgrade_rate_pct >= 0.30
                and i.commit_category_accuracy_pct <= 0.55):
            return ForecastPattern.category_manipulator
        return ForecastPattern.none

    # ── Action ────────────────────────────────────────────────────────────────

    def _action(self, risk: ForecastRisk, pat: ForecastPattern) -> ForecastAction:
        if risk == ForecastRisk.critical:
            if pat in (ForecastPattern.chronic_overcommit, ForecastPattern.sandbagger):
                return ForecastAction.executive_forecast_audit
            return ForecastAction.forecast_process_reset
        if risk == ForecastRisk.high:
            if pat == ForecastPattern.chronic_overcommit:    return ForecastAction.deal_by_deal_review
            if pat == ForecastPattern.sandbagger:            return ForecastAction.manager_forecast_alignment
            if pat == ForecastPattern.commit_drifter:        return ForecastAction.commit_cadence_coaching
            if pat == ForecastPattern.late_push_abuser:      return ForecastAction.pipeline_review_increase
            if pat == ForecastPattern.category_manipulator:  return ForecastAction.forecast_hygiene_training
            return ForecastAction.forecast_monitoring
        if risk == ForecastRisk.moderate:
            return ForecastAction.forecast_monitoring
        return ForecastAction.no_action

    # ── Signal ────────────────────────────────────────────────────────────────

    def _signal(self, i: ForecastInput, pat: ForecastPattern, comp: float) -> str:
        if comp < 20:
            return "Forecast reliability strong — commit accuracy, category discipline, and timing patterns within benchmark targets"
        labels = {
            ForecastPattern.chronic_overcommit:   "Chronic overcommit",
            ForecastPattern.sandbagger:           "Sandbagger",
            ForecastPattern.commit_drifter:       "Commit drifter",
            ForecastPattern.late_push_abuser:     "Late push abuser",
            ForecastPattern.category_manipulator: "Category manipulator",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {round(i.commit_vs_actual_variance_pct*100)}% commit variance — "
            f"{round(i.forecast_miss_rate_pct*100)}% miss rate — "
            f"{round(i.rolling_3q_forecast_accuracy_pct*100)}% 3Q accuracy — "
            f"composite {round(comp)}"
        )

    # ── Flags ─────────────────────────────────────────────────────────────────

    def _has_forecast_gap(self, i: ForecastInput, comp: float) -> bool:
        return (comp >= 40
                or i.forecast_miss_rate_pct >= 0.40
                or i.rolling_3q_forecast_accuracy_pct <= 0.65)

    def _requires_manager_review(self, i: ForecastInput, comp: float) -> bool:
        return (comp >= 25
                or i.commit_vs_actual_variance_pct >= 0.20
                or i.push_out_frequency_pct >= 0.30)

    # ── Forecast error estimate ───────────────────────────────────────────────

    def _forecast_error(self, i: ForecastInput, comp: float) -> float:
        return round(
            i.total_commit_deals
            * i.avg_deal_value_usd
            * i.commit_vs_actual_variance_pct
            * (comp / 100),
            2,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def assess(self, i: ForecastInput) -> ForecastResult:
        ac  = self._accuracy_score(i)
        di  = self._discipline_score(i)
        ti  = self._timing_score(i)
        re  = self._reliability_score(i)
        comp = self._composite(ac, di, ti, re)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = ForecastResult(
            rep_id=i.rep_id,
            region=i.region,
            forecast_risk=risk.value,
            forecast_pattern=pat.value,
            forecast_severity=sev.value,
            recommended_action=act.value,
            accuracy_score=ac,
            discipline_score=di,
            timing_score=ti,
            reliability_score=re,
            forecast_composite=comp,
            has_forecast_gap=self._has_forecast_gap(i, comp),
            requires_manager_review=self._requires_manager_review(i, comp),
            estimated_forecast_error_usd=self._forecast_error(i, comp),
            forecast_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ForecastInput]) -> List[ForecastResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_forecast_composite": 0.0,
                "forecast_gap_count": 0,
                "manager_review_count": 0,
                "avg_accuracy_score": 0.0,
                "avg_discipline_score": 0.0,
                "avg_timing_score": 0.0,
                "avg_reliability_score": 0.0,
                "total_estimated_forecast_error_usd": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tac = tdi = tti = tre = tcomp = tfe = 0.0
        gc = mc = 0
        for r in self._results:
            rc[r.forecast_risk]      = rc.get(r.forecast_risk, 0)      + 1
            pc[r.forecast_pattern]   = pc.get(r.forecast_pattern, 0)   + 1
            sc[r.forecast_severity]  = sc.get(r.forecast_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tac  += r.accuracy_score
            tdi  += r.discipline_score
            tti  += r.timing_score
            tre  += r.reliability_score
            tcomp += r.forecast_composite
            tfe  += r.estimated_forecast_error_usd
            if r.has_forecast_gap:        gc += 1
            if r.requires_manager_review: mc += 1
        return {
            "total":                                n,
            "risk_counts":                          rc,
            "pattern_counts":                       pc,
            "severity_counts":                      sc,
            "action_counts":                        ac,
            "avg_forecast_composite":               round(tcomp / n, 1),
            "forecast_gap_count":                   gc,
            "manager_review_count":                 mc,
            "avg_accuracy_score":                   round(tac / n, 1),
            "avg_discipline_score":                 round(tdi / n, 1),
            "avg_timing_score":                     round(tti / n, 1),
            "avg_reliability_score":                round(tre / n, 1),
            "total_estimated_forecast_error_usd":   round(tfe, 2),
        }
