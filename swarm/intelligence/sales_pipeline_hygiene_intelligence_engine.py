from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class HygieneRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class HygienePattern(str, Enum):
    none                       = "none"
    data_neglect               = "data_neglect"
    zombie_pipeline            = "zombie_pipeline"
    forecast_distortion        = "forecast_distortion"
    stale_activity             = "stale_activity"
    incomplete_qualification   = "incomplete_qualification"


class HygieneSeverity(str, Enum):
    clean      = "clean"
    developing = "developing"
    dirty      = "dirty"
    toxic      = "toxic"


class HygieneAction(str, Enum):
    no_action               = "no_action"
    crm_coaching            = "crm_coaching"
    pipeline_audit          = "pipeline_audit"
    data_cleanup_sprint     = "data_cleanup_sprint"
    forecast_recalibration  = "forecast_recalibration"
    pipeline_purge          = "pipeline_purge"


@dataclass
class PipelineHygieneInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_open_deals: int
    deals_missing_close_date_count: int
    deals_missing_next_step_count: int
    deals_stale_notes_30d_count: int
    deals_stale_notes_60d_count: int
    deals_never_contacted_count: int
    deals_close_date_in_past_count: int
    deals_missing_contact_count: int
    deals_missing_value_count: int
    crm_field_completion_pct: float
    avg_days_since_last_crm_update: float
    duplicate_deal_count: int
    deals_wrong_stage_count: int
    manual_forecast_override_count: int
    deals_no_activity_60d_count: int
    overdue_tasks_count: int
    avg_open_deal_value_usd: float
    avg_deal_age_days: float
    zombie_deal_count: int


@dataclass
class PipelineHygieneResult:
    rep_id: str
    region: str
    hygiene_risk: HygieneRisk
    hygiene_pattern: HygienePattern
    hygiene_severity: HygieneSeverity
    recommended_action: HygieneAction
    data_completeness_score: float
    pipeline_freshness_score: float
    deal_quality_score: float
    forecast_reliability_score: float
    pipeline_hygiene_composite: float
    has_hygiene_gap: bool
    requires_hygiene_coaching: bool
    estimated_forecast_error_usd: float
    hygiene_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "hygiene_risk":                 self.hygiene_risk.value,
            "hygiene_pattern":              self.hygiene_pattern.value,
            "hygiene_severity":             self.hygiene_severity.value,
            "recommended_action":           self.recommended_action.value,
            "data_completeness_score":      self.data_completeness_score,
            "pipeline_freshness_score":     self.pipeline_freshness_score,
            "deal_quality_score":           self.deal_quality_score,
            "forecast_reliability_score":   self.forecast_reliability_score,
            "pipeline_hygiene_composite":   self.pipeline_hygiene_composite,
            "has_hygiene_gap":              self.has_hygiene_gap,
            "requires_hygiene_coaching":    self.requires_hygiene_coaching,
            "estimated_forecast_error_usd": self.estimated_forecast_error_usd,
            "hygiene_signal":               self.hygiene_signal,
        }


class SalesPipelineHygieneIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[PipelineHygieneResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = worse hygiene = more risk)
    # ------------------------------------------------------------------

    def _data_completeness_score(self, inp: PipelineHygieneInput) -> float:
        score = 0.0
        total = max(inp.total_open_deals, 1)

        if inp.crm_field_completion_pct < 0.50:
            score += 40.0
        elif inp.crm_field_completion_pct < 0.70:
            score += 20.0
        elif inp.crm_field_completion_pct < 0.85:
            score += 8.0

        close_date_missing_rate = inp.deals_missing_close_date_count / total
        if close_date_missing_rate >= 0.30:
            score += 30.0
        elif close_date_missing_rate >= 0.15:
            score += 15.0
        elif close_date_missing_rate >= 0.05:
            score += 7.0

        next_step_missing_rate = inp.deals_missing_next_step_count / total
        if next_step_missing_rate >= 0.40:
            score += 25.0
        elif next_step_missing_rate >= 0.20:
            score += 12.0

        return min(score, 100.0)

    def _pipeline_freshness_score(self, inp: PipelineHygieneInput) -> float:
        score = 0.0
        total = max(inp.total_open_deals, 1)

        if inp.avg_days_since_last_crm_update >= 14.0:
            score += 45.0
        elif inp.avg_days_since_last_crm_update >= 7.0:
            score += 25.0
        elif inp.avg_days_since_last_crm_update >= 3.0:
            score += 8.0

        stale_30d_rate = inp.deals_stale_notes_30d_count / total
        if stale_30d_rate >= 0.40:
            score += 35.0
        elif stale_30d_rate >= 0.25:
            score += 18.0
        elif stale_30d_rate >= 0.10:
            score += 7.0

        no_activity_60d_rate = inp.deals_no_activity_60d_count / total
        if no_activity_60d_rate >= 0.30:
            score += 20.0
        elif no_activity_60d_rate >= 0.15:
            score += 10.0

        return min(score, 100.0)

    def _deal_quality_score(self, inp: PipelineHygieneInput) -> float:
        score = 0.0
        total = max(inp.total_open_deals, 1)

        zombie_rate = inp.zombie_deal_count / total
        if zombie_rate >= 0.20:
            score += 40.0
        elif zombie_rate >= 0.10:
            score += 20.0
        elif zombie_rate >= 0.05:
            score += 8.0

        never_contacted_rate = inp.deals_never_contacted_count / total
        if never_contacted_rate >= 0.10:
            score += 30.0
        elif never_contacted_rate >= 0.05:
            score += 15.0

        missing_contact_rate = inp.deals_missing_contact_count / total
        if missing_contact_rate >= 0.25:
            score += 25.0
        elif missing_contact_rate >= 0.10:
            score += 12.0

        return min(score, 100.0)

    def _forecast_reliability_score(self, inp: PipelineHygieneInput) -> float:
        score = 0.0
        total = max(inp.total_open_deals, 1)

        past_close_rate = inp.deals_close_date_in_past_count / total
        if past_close_rate >= 0.20:
            score += 40.0
        elif past_close_rate >= 0.10:
            score += 20.0
        elif past_close_rate >= 0.05:
            score += 8.0

        if inp.manual_forecast_override_count >= 5:
            score += 30.0
        elif inp.manual_forecast_override_count >= 3:
            score += 15.0
        elif inp.manual_forecast_override_count >= 1:
            score += 7.0

        if inp.duplicate_deal_count >= 3:
            score += 25.0
        elif inp.duplicate_deal_count >= 1:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: PipelineHygieneInput,
                          completeness: float, freshness: float,
                          quality: float, reliability: float) -> HygienePattern:
        if completeness >= 35 and inp.crm_field_completion_pct < 0.60:
            return HygienePattern.data_neglect

        total = max(inp.total_open_deals, 1)
        zombie_rate = inp.zombie_deal_count / total
        if quality >= 35 and zombie_rate >= 0.15:
            return HygienePattern.zombie_pipeline

        past_close_rate = inp.deals_close_date_in_past_count / total
        if reliability >= 35 and (past_close_rate >= 0.15 or inp.manual_forecast_override_count >= 3):
            return HygienePattern.forecast_distortion

        if freshness >= 35 and inp.avg_days_since_last_crm_update >= 10.0:
            return HygienePattern.stale_activity

        never_rate = inp.deals_never_contacted_count / total
        if quality >= 25 and never_rate >= 0.08:
            return HygienePattern.incomplete_qualification

        return HygienePattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> HygieneRisk:
        if composite >= 60:
            return HygieneRisk.critical
        if composite >= 40:
            return HygieneRisk.high
        if composite >= 20:
            return HygieneRisk.moderate
        return HygieneRisk.low

    def _severity(self, composite: float) -> HygieneSeverity:
        if composite >= 60:
            return HygieneSeverity.toxic
        if composite >= 40:
            return HygieneSeverity.dirty
        if composite >= 20:
            return HygieneSeverity.developing
        return HygieneSeverity.clean

    def _action(self, risk: HygieneRisk,
                 pattern: HygienePattern) -> HygieneAction:
        if risk == HygieneRisk.critical:
            if pattern == HygienePattern.data_neglect:
                return HygieneAction.data_cleanup_sprint
            if pattern == HygienePattern.zombie_pipeline:
                return HygieneAction.pipeline_purge
            return HygieneAction.pipeline_audit
        if risk == HygieneRisk.high:
            if pattern == HygienePattern.forecast_distortion:
                return HygieneAction.forecast_recalibration
            if pattern == HygienePattern.stale_activity:
                return HygieneAction.crm_coaching
            return HygieneAction.pipeline_audit
        if risk == HygieneRisk.moderate:
            return HygieneAction.crm_coaching
        return HygieneAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_hygiene_gap(self, composite: float,
                          inp: PipelineHygieneInput) -> bool:
        return (
            composite >= 40
            or inp.zombie_deal_count >= 3
            or inp.crm_field_completion_pct < 0.50
        )

    def _requires_hygiene_coaching(self, composite: float,
                                    inp: PipelineHygieneInput) -> bool:
        return (
            composite >= 30
            or inp.avg_days_since_last_crm_update >= 10.0
            or inp.deals_close_date_in_past_count >= 3
        )

    # ------------------------------------------------------------------
    # Forecast error estimate
    # ------------------------------------------------------------------

    def _estimated_forecast_error(self, inp: PipelineHygieneInput,
                                   composite: float) -> float:
        exposed_deals = inp.zombie_deal_count + inp.deals_close_date_in_past_count
        return round(exposed_deals * inp.avg_open_deal_value_usd * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: PipelineHygieneInput,
                 pattern: HygienePattern, composite: float) -> str:
        if pattern == HygienePattern.none and composite < 20:
            return "Pipeline hygiene and CRM data quality within healthy benchmarks"
        parts: list[str] = []
        if inp.crm_field_completion_pct < 0.70:
            parts.append(f"{inp.crm_field_completion_pct*100:.0f}% CRM complete")
        if inp.zombie_deal_count >= 1:
            parts.append(f"{inp.zombie_deal_count} zombie deals")
        if inp.deals_close_date_in_past_count >= 1:
            parts.append(f"{inp.deals_close_date_in_past_count} overdue close dates")
        label = pattern.value.replace("_", " ") if pattern != HygienePattern.none else "Hygiene risk"
        summary = " — ".join(parts) if parts else "pipeline data quality degraded"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: PipelineHygieneInput) -> PipelineHygieneResult:
        completeness = round(self._data_completeness_score(inp), 1)
        freshness    = round(self._pipeline_freshness_score(inp), 1)
        quality      = round(self._deal_quality_score(inp), 1)
        reliability  = round(self._forecast_reliability_score(inp), 1)

        composite = round(
            completeness * 0.30 + freshness * 0.30 + quality * 0.25 + reliability * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, completeness, freshness, quality, reliability)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_hygiene_gap(composite, inp)
        coaching = self._requires_hygiene_coaching(composite, inp)
        error    = self._estimated_forecast_error(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = PipelineHygieneResult(
            rep_id=inp.rep_id,
            region=inp.region,
            hygiene_risk=risk,
            hygiene_pattern=pattern,
            hygiene_severity=severity,
            recommended_action=action,
            data_completeness_score=completeness,
            pipeline_freshness_score=freshness,
            deal_quality_score=quality,
            forecast_reliability_score=reliability,
            pipeline_hygiene_composite=composite,
            has_hygiene_gap=gap,
            requires_hygiene_coaching=coaching,
            estimated_forecast_error_usd=error,
            hygiene_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[PipelineHygieneInput]) -> list[PipelineHygieneResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_pipeline_hygiene_composite": 0.0,
                "hygiene_gap_count": 0,
                "hygiene_coaching_count": 0,
                "avg_data_completeness_score": 0.0,
                "avg_pipeline_freshness_score": 0.0,
                "avg_deal_quality_score": 0.0,
                "avg_forecast_reliability_score": 0.0,
                "total_estimated_forecast_error_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_cmp = total_frsh = total_qua = total_rel = total_err = 0.0

        for r in self._results:
            risk_counts[r.hygiene_risk.value]       = risk_counts.get(r.hygiene_risk.value, 0) + 1
            pattern_counts[r.hygiene_pattern.value] = pattern_counts.get(r.hygiene_pattern.value, 0) + 1
            severity_counts[r.hygiene_severity.value] = severity_counts.get(r.hygiene_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.pipeline_hygiene_composite
            total_cmp  += r.data_completeness_score
            total_frsh += r.pipeline_freshness_score
            total_qua  += r.deal_quality_score
            total_rel  += r.forecast_reliability_score
            total_err  += r.estimated_forecast_error_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_pipeline_hygiene_composite":       round(total_comp / n, 1),
            "hygiene_gap_count":                    sum(1 for r in self._results if r.has_hygiene_gap),
            "hygiene_coaching_count":               sum(1 for r in self._results if r.requires_hygiene_coaching),
            "avg_data_completeness_score":          round(total_cmp / n, 1),
            "avg_pipeline_freshness_score":         round(total_frsh / n, 1),
            "avg_deal_quality_score":               round(total_qua / n, 1),
            "avg_forecast_reliability_score":       round(total_rel / n, 1),
            "total_estimated_forecast_error_usd":   round(total_err, 2),
        }
