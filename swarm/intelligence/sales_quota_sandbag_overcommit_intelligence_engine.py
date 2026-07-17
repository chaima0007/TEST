from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class QuotaPatternRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class QuotaPattern(str, Enum):
    none              = "none"
    sandbagging       = "sandbagging"
    overcommitting    = "overcommitting"
    volatile_committor = "volatile_committor"
    late_surge        = "late_surge"
    forecast_manipulator = "forecast_manipulator"


class QuotaSeverity(str, Enum):
    calibrated   = "calibrated"
    drifting     = "drifting"
    distorted    = "distorted"
    manipulated  = "manipulated"


class QuotaAction(str, Enum):
    no_action                     = "no_action"
    quota_check_in                = "quota_check_in"
    forecast_calibration_coaching = "forecast_calibration_coaching"
    commit_accuracy_coaching      = "commit_accuracy_coaching"
    manager_quota_review          = "manager_quota_review"
    quota_reset_intervention      = "quota_reset_intervention"
    executive_quota_escalation    = "executive_quota_escalation"


@dataclass
class QuotaInput:
    rep_id:                         str
    region:                         str
    evaluation_period_id:           str
    quota_attainment_pct:           float   # 0-2+ (>1 = over quota)
    forecast_accuracy_pct:          float   # 0-1 (how accurate commits were)
    commit_vs_actual_ratio:         float   # actual/committed (>1 overcommit, <1 sandbag)
    sandbagging_index:              float   # 0-1 (proprietary: late surge + low commit pattern)
    overcommit_frequency_pct:       float   # 0-1 (how often rep commits above actual)
    late_quarter_close_rate_pct:    float   # 0-1 (deals closing in last 2 weeks)
    pipeline_to_quota_ratio:        float   # pipeline coverage vs quota
    early_commit_accuracy_pct:      float   # 0-1 (commits made >45 days out)
    mid_commit_accuracy_pct:        float   # 0-1 (commits 15-45 days out)
    late_commit_accuracy_pct:       float   # 0-1 (commits <15 days out)
    upside_conversion_rate_pct:     float   # 0-1 (how often upside becomes commit/close)
    commit_revision_frequency:      int     # times commit changed in a quarter
    pulled_in_deal_rate_pct:        float   # 0-1 (deals pulled forward to hit number)
    pushed_out_deal_rate_pct:       float   # 0-1 (deals pushed to next quarter)
    quota_to_territory_fit_score:   float   # 0-1 (is quota fair vs territory)
    mgr_trust_in_forecast_score:    float   # 0-1 (manager confidence in rep's commits)
    peer_comparison_delta_pct:      float   # rep attainment vs peer average (-1 to 1)
    consecutive_miss_streak:        int     # consecutive periods missing commit
    voluntary_quota_increase_pct:   float   # 0-1 (rep accepted quota increase)


@dataclass
class QuotaResult:
    rep_id:                         str
    region:                         str
    quota_risk:                     QuotaPatternRisk
    quota_pattern:                  QuotaPattern
    quota_severity:                 QuotaSeverity
    recommended_action:             QuotaAction
    sandbagging_score:              float
    overcommit_score:               float
    calibration_score:              float
    volatility_score:               float
    quota_composite:                float
    has_quota_gap:                  bool
    requires_quota_intervention:    bool
    estimated_quota_distortion_usd: float
    quota_signal:                   str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "quota_risk":                       self.quota_risk.value,
            "quota_pattern":                    self.quota_pattern.value,
            "quota_severity":                   self.quota_severity.value,
            "recommended_action":               self.recommended_action.value,
            "sandbagging_score":                self.sandbagging_score,
            "overcommit_score":                 self.overcommit_score,
            "calibration_score":                self.calibration_score,
            "volatility_score":                 self.volatility_score,
            "quota_composite":                  self.quota_composite,
            "has_quota_gap":                    self.has_quota_gap,
            "requires_quota_intervention":      self.requires_quota_intervention,
            "estimated_quota_distortion_usd":   self.estimated_quota_distortion_usd,
            "quota_signal":                     self.quota_signal,
        }


class SalesQuotaSandbagOvercommitIntelligenceEngine:
    """Detects quota gaming — sandbagging, overcommitting, volatile commitments, late-surge patterns."""

    def __init__(self) -> None:
        self._results: List[QuotaResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _sandbagging_score(self, inp: QuotaInput) -> float:
        s = 0.0
        if   inp.sandbagging_index         >= 0.65: s += 40
        elif inp.sandbagging_index         >= 0.45: s += 22
        elif inp.sandbagging_index         >= 0.25: s += 8
        if   inp.late_quarter_close_rate_pct >= 0.60: s += 35
        elif inp.late_quarter_close_rate_pct >= 0.40: s += 18
        if   inp.commit_vs_actual_ratio     <= 0.70: s += 25
        elif inp.commit_vs_actual_ratio     <= 0.85: s += 12
        return min(s, 100.0)

    def _overcommit_score(self, inp: QuotaInput) -> float:
        s = 0.0
        if   inp.overcommit_frequency_pct  >= 0.55: s += 40
        elif inp.overcommit_frequency_pct  >= 0.35: s += 22
        elif inp.overcommit_frequency_pct  >= 0.20: s += 8
        if   inp.consecutive_miss_streak   >= 3:    s += 35
        elif inp.consecutive_miss_streak   >= 2:    s += 18
        if   inp.mgr_trust_in_forecast_score <= 0.35: s += 25
        elif inp.mgr_trust_in_forecast_score <= 0.55: s += 12
        return min(s, 100.0)

    def _calibration_score(self, inp: QuotaInput) -> float:
        s = 0.0
        if   inp.forecast_accuracy_pct     <= 0.40: s += 40
        elif inp.forecast_accuracy_pct     <= 0.60: s += 22
        elif inp.forecast_accuracy_pct     <= 0.75: s += 8
        if   inp.early_commit_accuracy_pct <= 0.35: s += 30
        elif inp.early_commit_accuracy_pct <= 0.55: s += 15
        if   inp.mid_commit_accuracy_pct   <= 0.50: s += 20
        elif inp.mid_commit_accuracy_pct   <= 0.70: s += 10
        if   inp.late_commit_accuracy_pct  <= 0.65: s += 10
        return min(s, 100.0)

    def _volatility_score(self, inp: QuotaInput) -> float:
        s = 0.0
        if   inp.commit_revision_frequency >= 5:    s += 40
        elif inp.commit_revision_frequency >= 3:    s += 22
        elif inp.commit_revision_frequency >= 2:    s += 8
        if   inp.pulled_in_deal_rate_pct   >= 0.35: s += 35
        elif inp.pulled_in_deal_rate_pct   >= 0.20: s += 18
        if   inp.pushed_out_deal_rate_pct  >= 0.30: s += 25
        elif inp.pushed_out_deal_rate_pct  >= 0.15: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, sb: float, oc: float, cal: float, vol: float) -> float:
        return min(round(sb * 0.30 + oc * 0.25 + cal * 0.30 + vol * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: QuotaInput) -> QuotaPattern:
        if inp.sandbagging_index >= 0.50 and inp.late_quarter_close_rate_pct >= 0.45:
            return QuotaPattern.sandbagging
        if inp.overcommit_frequency_pct >= 0.50 and inp.consecutive_miss_streak >= 2:
            return QuotaPattern.overcommitting
        if inp.commit_revision_frequency >= 4 and inp.forecast_accuracy_pct <= 0.55:
            return QuotaPattern.volatile_committor
        if inp.late_quarter_close_rate_pct >= 0.55 and inp.early_commit_accuracy_pct <= 0.40:
            return QuotaPattern.late_surge
        if inp.pulled_in_deal_rate_pct >= 0.30 and inp.pushed_out_deal_rate_pct >= 0.25:
            return QuotaPattern.forecast_manipulator
        return QuotaPattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> QuotaPatternRisk:
        if   composite >= 60: return QuotaPatternRisk.critical
        elif composite >= 40: return QuotaPatternRisk.high
        elif composite >= 20: return QuotaPatternRisk.moderate
        return QuotaPatternRisk.low

    def _severity(self, composite: float) -> QuotaSeverity:
        if   composite >= 60: return QuotaSeverity.manipulated
        elif composite >= 40: return QuotaSeverity.distorted
        elif composite >= 20: return QuotaSeverity.drifting
        return QuotaSeverity.calibrated

    def _action(self, risk: QuotaPatternRisk, pattern: QuotaPattern) -> QuotaAction:
        if risk == QuotaPatternRisk.critical:
            if pattern in (QuotaPattern.sandbagging, QuotaPattern.forecast_manipulator):
                return QuotaAction.executive_quota_escalation
            return QuotaAction.quota_reset_intervention
        if risk == QuotaPatternRisk.high:
            if pattern == QuotaPattern.sandbagging:
                return QuotaAction.manager_quota_review
            if pattern == QuotaPattern.overcommitting:
                return QuotaAction.commit_accuracy_coaching
            if pattern == QuotaPattern.volatile_committor:
                return QuotaAction.forecast_calibration_coaching
            if pattern == QuotaPattern.late_surge:
                return QuotaAction.manager_quota_review
            if pattern == QuotaPattern.forecast_manipulator:
                return QuotaAction.manager_quota_review
            return QuotaAction.commit_accuracy_coaching
        if risk == QuotaPatternRisk.moderate:
            return QuotaAction.quota_check_in
        return QuotaAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: QuotaInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.forecast_accuracy_pct     <= 0.60
            or inp.consecutive_miss_streak   >= 2
        )

    def _requires_intervention(self, inp: QuotaInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.sandbagging_index         >= 0.40
            or inp.mgr_trust_in_forecast_score <= 0.50
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _distortion_usd(self, inp: QuotaInput, composite: float) -> float:
        base = inp.pipeline_to_quota_ratio * 100_000
        distortion = (composite / 100) * abs(1.0 - inp.commit_vs_actual_ratio)
        return round(base * distortion, 2)

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        QuotaPattern.sandbagging:          "Sandbagging",
        QuotaPattern.overcommitting:       "Overcommitting",
        QuotaPattern.volatile_committor:   "Volatile committor",
        QuotaPattern.late_surge:           "Late surge",
        QuotaPattern.forecast_manipulator: "Forecast manipulator",
    }

    def _signal(self, inp: QuotaInput, pattern: QuotaPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Quota commitment calibrated — forecast accuracy, commit consistency, "
                "and attainment pattern within benchmarks"
            )
        label    = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        acc_pct  = round(inp.forecast_accuracy_pct * 100)
        late_pct = round(inp.late_quarter_close_rate_pct * 100)
        miss     = inp.consecutive_miss_streak
        comp_int = round(composite)
        return (
            f"{label} — {acc_pct}% forecast accuracy — "
            f"{late_pct}% late-quarter closes — "
            f"{miss} consecutive miss streak — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: QuotaInput) -> QuotaResult:
        sb  = self._sandbagging_score(inp)
        oc  = self._overcommit_score(inp)
        cal = self._calibration_score(inp)
        vol = self._volatility_score(inp)
        comp = self._composite(sb, oc, cal, vol)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = QuotaResult(
            rep_id                      = inp.rep_id,
            region                      = inp.region,
            quota_risk                  = risk,
            quota_pattern               = pattern,
            quota_severity              = severity,
            recommended_action          = action,
            sandbagging_score           = sb,
            overcommit_score            = oc,
            calibration_score           = cal,
            volatility_score            = vol,
            quota_composite             = comp,
            has_quota_gap               = self._has_gap(inp, comp),
            requires_quota_intervention = self._requires_intervention(inp, comp),
            estimated_quota_distortion_usd = self._distortion_usd(inp, comp),
            quota_signal                = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[QuotaInput]) -> List[QuotaResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_quota_composite": 0.0,
                "quota_gap_count": 0,
                "intervention_count": 0,
                "avg_sandbagging_score": 0.0,
                "avg_overcommit_score": 0.0,
                "avg_calibration_score": 0.0,
                "avg_volatility_score": 0.0,
                "total_estimated_quota_distortion_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_sb = total_oc = total_cal = total_vol = total_dist = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.quota_risk.value]          = risk_counts.get(res.quota_risk.value, 0) + 1
            pattern_counts[res.quota_pattern.value]    = pattern_counts.get(res.quota_pattern.value, 0) + 1
            severity_counts[res.quota_severity.value]  = severity_counts.get(res.quota_severity.value, 0) + 1
            action_counts[res.recommended_action.value]= action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.quota_composite
            total_sb   += res.sandbagging_score
            total_oc   += res.overcommit_score
            total_cal  += res.calibration_score
            total_vol  += res.volatility_score
            total_dist += res.estimated_quota_distortion_usd
            if res.has_quota_gap:               gap_count          += 1
            if res.requires_quota_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_quota_composite":                      round(total_comp / n, 1),
            "quota_gap_count":                          gap_count,
            "intervention_count":                       intervention_count,
            "avg_sandbagging_score":                    round(total_sb / n, 1),
            "avg_overcommit_score":                     round(total_oc / n, 1),
            "avg_calibration_score":                    round(total_cal / n, 1),
            "avg_volatility_score":                     round(total_vol / n, 1),
            "total_estimated_quota_distortion_usd":     round(total_dist, 2),
        }
