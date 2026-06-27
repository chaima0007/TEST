from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class HygieneRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class HygienePattern(str, Enum):
    none                     = "none"
    stage_inflation_stager   = "stage_inflation_stager"
    phantom_pipeline         = "phantom_pipeline"
    data_black_hole          = "data_black_hole"
    vanity_metrics_builder   = "vanity_metrics_builder"
    forecast_fudger          = "forecast_fudger"


class HygieneSeverity(str, Enum):
    clean       = "clean"
    drifting    = "drifting"
    degraded    = "degraded"
    corrupted   = "corrupted"


class HygieneAction(str, Enum):
    no_action                     = "no_action"
    crm_hygiene_coaching          = "crm_hygiene_coaching"
    pipeline_review_checkpoint    = "pipeline_review_checkpoint"
    stage_criteria_enforcement    = "stage_criteria_enforcement"
    data_quality_intervention     = "data_quality_intervention"
    pipeline_purge_facilitation   = "pipeline_purge_facilitation"
    forecast_integrity_audit      = "forecast_integrity_audit"
    crm_accuracy_reset            = "crm_accuracy_reset"


@dataclass
class HygieneInput:
    rep_id:                                     str
    region:                                     str
    evaluation_period_id:                       str
    stage_advancement_without_exit_criteria_pct: float  # 0-1 (% deals advanced without meeting stage criteria)
    deal_regression_rate_pct:                   float   # 0-1 (% deals that move backward in stage)
    avg_days_in_current_stage:                  float   # avg days deals sit stagnant in current stage
    stage_3_to_close_conversion_rate_pct:       float   # 0-1 (% converting from late stage to close)
    closed_won_below_forecast_pct:              float   # 0-1 (% closes below forecasted amount)
    stage_skip_rate_pct:                        float   # 0-1 (% deals skipping stages without justification)
    crm_update_latency_days:                    float   # avg days between activity and CRM update
    verified_next_step_in_crm_rate_pct:         float   # 0-1 (% deals with verified next steps logged)
    competitive_status_missing_rate_pct:        float   # 0-1 (% deals missing competitive info)
    decision_criteria_captured_rate_pct:        float   # 0-1 (% deals with decision criteria logged)
    technical_validation_complete_rate_pct:     float   # 0-1 (% with technical validation complete)
    budget_verified_rate_pct:                   float   # 0-1 (% deals with budget confirmed)
    close_date_slip_rate_pct:                   float   # 0-1 (% deals where close date slipped >1 quarter)
    pipeline_creation_to_close_ratio:           float   # ratio of pipeline created vs actually closed
    opp_age_over_180_days_pct:                  float   # 0-1 (% deals older than 180 days without close)
    discovery_to_proposal_ratio:                float   # ratio (high = stuck in discovery)
    data_completeness_score:                    float   # 0-1 (overall CRM data quality)
    manual_close_date_push_rate_pct:            float   # 0-1 (% deals with manual close date pushed)
    win_rate_vs_forecast_accuracy_delta:        float   # 0-1 normalized (gap between forecast and actual win rate)
    total_pipeline_deals:                       int
    avg_deal_value_usd:                         float


@dataclass
class HygieneResult:
    rep_id:                        str
    region:                        str
    hygiene_risk:                  HygieneRisk
    hygiene_pattern:               HygienePattern
    hygiene_severity:              HygieneSeverity
    recommended_action:            HygieneAction
    accuracy_score:                float
    hygiene_score:                 float
    velocity_score:                float
    completeness_score:            float
    hygiene_composite:             float
    has_hygiene_gap:               bool
    requires_hygiene_coaching:     bool
    estimated_inflated_pipeline_usd: float
    hygiene_signal:                str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                          self.rep_id,
            "region":                          self.region,
            "hygiene_risk":                    self.hygiene_risk.value,
            "hygiene_pattern":                 self.hygiene_pattern.value,
            "hygiene_severity":                self.hygiene_severity.value,
            "recommended_action":              self.recommended_action.value,
            "accuracy_score":                  self.accuracy_score,
            "hygiene_score":                   self.hygiene_score,
            "velocity_score":                  self.velocity_score,
            "completeness_score":              self.completeness_score,
            "hygiene_composite":               self.hygiene_composite,
            "has_hygiene_gap":                 self.has_hygiene_gap,
            "requires_hygiene_coaching":       self.requires_hygiene_coaching,
            "estimated_inflated_pipeline_usd": self.estimated_inflated_pipeline_usd,
            "hygiene_signal":                  self.hygiene_signal,
        }


class SalesPipelineStageInflationCrmHygieneEngine:
    """Detects pipeline stage inflation and CRM hygiene decay — deals advancing in CRM before real milestones are hit."""

    def __init__(self) -> None:
        self._results: List[HygieneResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _accuracy_score(self, inp: HygieneInput) -> float:
        s = 0.0
        if   inp.stage_advancement_without_exit_criteria_pct >= 0.55: s += 40
        elif inp.stage_advancement_without_exit_criteria_pct >= 0.30: s += 22
        elif inp.stage_advancement_without_exit_criteria_pct >= 0.15: s += 8
        if   inp.closed_won_below_forecast_pct              >= 0.45: s += 35
        elif inp.closed_won_below_forecast_pct              >= 0.25: s += 18
        if   inp.win_rate_vs_forecast_accuracy_delta        >= 0.30: s += 25
        elif inp.win_rate_vs_forecast_accuracy_delta        >= 0.15: s += 12
        return min(s, 100.0)

    def _hygiene_score(self, inp: HygieneInput) -> float:
        s = 0.0
        if   inp.crm_update_latency_days               >= 10.0: s += 45
        elif inp.crm_update_latency_days               >= 5.0:  s += 25
        elif inp.crm_update_latency_days               >= 2.5:  s += 10
        if   inp.verified_next_step_in_crm_rate_pct    <= 0.25: s += 30
        elif inp.verified_next_step_in_crm_rate_pct    <= 0.55: s += 15
        if   inp.data_completeness_score               <= 0.25: s += 25
        elif inp.data_completeness_score               <= 0.55: s += 12
        return min(s, 100.0)

    def _velocity_score(self, inp: HygieneInput) -> float:
        s = 0.0
        if   inp.close_date_slip_rate_pct          >= 0.60: s += 45
        elif inp.close_date_slip_rate_pct          >= 0.35: s += 25
        elif inp.close_date_slip_rate_pct          >= 0.18: s += 10
        if   inp.opp_age_over_180_days_pct         >= 0.40: s += 30
        elif inp.opp_age_over_180_days_pct         >= 0.20: s += 15
        if   inp.deal_regression_rate_pct          >= 0.35: s += 25
        elif inp.deal_regression_rate_pct          >= 0.18: s += 12
        return min(s, 100.0)

    def _completeness_score(self, inp: HygieneInput) -> float:
        s = 0.0
        if   inp.decision_criteria_captured_rate_pct    <= 0.20: s += 40
        elif inp.decision_criteria_captured_rate_pct    <= 0.45: s += 22
        elif inp.decision_criteria_captured_rate_pct    <= 0.65: s += 8
        if   inp.budget_verified_rate_pct               <= 0.25: s += 35
        elif inp.budget_verified_rate_pct               <= 0.50: s += 18
        if   inp.technical_validation_complete_rate_pct <= 0.20: s += 25
        elif inp.technical_validation_complete_rate_pct <= 0.45: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────────

    def _composite(self, ac: float, hy: float, ve: float, co: float) -> float:
        return min(round(ac * 0.30 + hy * 0.25 + ve * 0.25 + co * 0.20, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, inp: HygieneInput) -> HygienePattern:
        if inp.stage_advancement_without_exit_criteria_pct >= 0.50 and inp.deal_regression_rate_pct >= 0.30:
            return HygienePattern.stage_inflation_stager
        if inp.close_date_slip_rate_pct >= 0.55 and inp.opp_age_over_180_days_pct >= 0.35:
            return HygienePattern.phantom_pipeline
        if inp.data_completeness_score <= 0.30 and inp.crm_update_latency_days >= 7:
            return HygienePattern.data_black_hole
        if inp.stage_3_to_close_conversion_rate_pct <= 0.15 and inp.pipeline_creation_to_close_ratio >= 5.0:
            return HygienePattern.vanity_metrics_builder
        if inp.win_rate_vs_forecast_accuracy_delta >= 0.25 and inp.closed_won_below_forecast_pct >= 0.40:
            return HygienePattern.forecast_fudger
        return HygienePattern.none

    # ── thresholds ────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> HygieneRisk:
        if   composite >= 60: return HygieneRisk.critical
        elif composite >= 40: return HygieneRisk.high
        elif composite >= 20: return HygieneRisk.moderate
        return HygieneRisk.low

    def _severity(self, composite: float) -> HygieneSeverity:
        if   composite >= 60: return HygieneSeverity.corrupted
        elif composite >= 40: return HygieneSeverity.degraded
        elif composite >= 20: return HygieneSeverity.drifting
        return HygieneSeverity.clean

    def _action(self, risk: HygieneRisk, pattern: HygienePattern) -> HygieneAction:
        if risk == HygieneRisk.critical:
            if pattern in (HygienePattern.stage_inflation_stager, HygienePattern.forecast_fudger):
                return HygieneAction.crm_accuracy_reset
            return HygieneAction.forecast_integrity_audit
        if risk == HygieneRisk.high:
            if pattern == HygienePattern.stage_inflation_stager:
                return HygieneAction.stage_criteria_enforcement
            if pattern == HygienePattern.phantom_pipeline:
                return HygieneAction.pipeline_purge_facilitation
            if pattern == HygienePattern.data_black_hole:
                return HygieneAction.data_quality_intervention
            if pattern == HygienePattern.vanity_metrics_builder:
                return HygieneAction.pipeline_review_checkpoint
            if pattern == HygienePattern.forecast_fudger:
                return HygieneAction.forecast_integrity_audit
            return HygieneAction.crm_hygiene_coaching
        if risk == HygieneRisk.moderate:
            return HygieneAction.crm_hygiene_coaching
        return HygieneAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: HygieneInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.data_completeness_score <= 0.50
            or inp.stage_advancement_without_exit_criteria_pct >= 0.30
        )

    def _requires_coaching(self, inp: HygieneInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.crm_update_latency_days >= 5.0
            or inp.verified_next_step_in_crm_rate_pct <= 0.60
        )

    # ── inflated pipeline estimate ────────────────────────────────────────────

    def _inflated_pipeline(self, inp: HygieneInput, composite: float) -> float:
        return round(
            inp.total_pipeline_deals
            * inp.avg_deal_value_usd
            * inp.stage_advancement_without_exit_criteria_pct
            * (composite / 100),
            2
        )

    # ── signal ────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        HygienePattern.stage_inflation_stager: "Stage inflation stager",
        HygienePattern.phantom_pipeline:       "Phantom pipeline",
        HygienePattern.data_black_hole:        "Data black hole",
        HygienePattern.vanity_metrics_builder: "Vanity metrics builder",
        HygienePattern.forecast_fudger:        "Forecast fudger",
    }

    def _signal(self, inp: HygieneInput, pattern: HygienePattern, composite: float) -> str:
        if composite < 20:
            return (
                "Pipeline staging and CRM hygiene healthy — stage criteria met, "
                "data completeness, and forecast accuracy within benchmark targets"
            )
        label       = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        inflate_pct = round(inp.stage_advancement_without_exit_criteria_pct * 100)
        slip_pct    = round(inp.close_date_slip_rate_pct * 100)
        complete_pct = round(inp.data_completeness_score * 100)
        comp_int    = round(composite)
        return (
            f"{label} — {inflate_pct}% advanced without criteria — {slip_pct}% close dates slipped — "
            f"{complete_pct}% data completeness — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, inp: HygieneInput) -> HygieneResult:
        ac  = self._accuracy_score(inp)
        hy  = self._hygiene_score(inp)
        ve  = self._velocity_score(inp)
        co  = self._completeness_score(inp)
        comp = self._composite(ac, hy, ve, co)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = HygieneResult(
            rep_id                         = inp.rep_id,
            region                         = inp.region,
            hygiene_risk                   = risk,
            hygiene_pattern                = pattern,
            hygiene_severity               = severity,
            recommended_action             = action,
            accuracy_score                 = ac,
            hygiene_score                  = hy,
            velocity_score                 = ve,
            completeness_score             = co,
            hygiene_composite              = comp,
            has_hygiene_gap                = self._has_gap(inp, comp),
            requires_hygiene_coaching      = self._requires_coaching(inp, comp),
            estimated_inflated_pipeline_usd= self._inflated_pipeline(inp, comp),
            hygiene_signal                 = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[HygieneInput]) -> List[HygieneResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total":                                  0,
                "risk_counts":                            {},
                "pattern_counts":                         {},
                "severity_counts":                        {},
                "action_counts":                          {},
                "avg_hygiene_composite":                  0.0,
                "hygiene_gap_count":                      0,
                "coaching_count":                         0,
                "avg_accuracy_score":                     0.0,
                "avg_hygiene_score":                      0.0,
                "avg_velocity_score":                     0.0,
                "avg_completeness_score":                 0.0,
                "total_estimated_inflated_pipeline_usd":  0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_ac = total_hy = total_ve = total_co = total_ip = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.hygiene_risk.value]         = risk_counts.get(res.hygiene_risk.value, 0) + 1
            pattern_counts[res.hygiene_pattern.value]   = pattern_counts.get(res.hygiene_pattern.value, 0) + 1
            severity_counts[res.hygiene_severity.value] = severity_counts.get(res.hygiene_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.hygiene_composite
            total_ac   += res.accuracy_score
            total_hy   += res.hygiene_score
            total_ve   += res.velocity_score
            total_co   += res.completeness_score
            total_ip   += res.estimated_inflated_pipeline_usd
            if res.has_hygiene_gap:           gap_count      += 1
            if res.requires_hygiene_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                 n,
            "risk_counts":                           risk_counts,
            "pattern_counts":                        pattern_counts,
            "severity_counts":                       severity_counts,
            "action_counts":                         action_counts,
            "avg_hygiene_composite":                 round(total_comp / n, 1),
            "hygiene_gap_count":                     gap_count,
            "coaching_count":                        coaching_count,
            "avg_accuracy_score":                    round(total_ac / n, 1),
            "avg_hygiene_score":                     round(total_hy / n, 1),
            "avg_velocity_score":                    round(total_ve / n, 1),
            "avg_completeness_score":                round(total_co / n, 1),
            "total_estimated_inflated_pipeline_usd": round(total_ip, 2),
        }
