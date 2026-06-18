from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class CRMAdoptionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CRMAdoptionPattern(str, Enum):
    none                        = "none"
    stale_data                  = "stale_data"
    incomplete_records          = "incomplete_records"
    activity_logging_gap        = "activity_logging_gap"
    forecast_data_unreliable    = "forecast_data_unreliable"
    lazy_entry                  = "lazy_entry"


class CRMAdoptionSeverity(str, Enum):
    compliant   = "compliant"
    developing  = "developing"
    neglected   = "neglected"
    abandoned   = "abandoned"


class CRMAdoptionAction(str, Enum):
    no_action                   = "no_action"
    crm_coaching                = "crm_coaching"
    data_cleanup_session        = "data_cleanup_session"
    activity_logging_training   = "activity_logging_training"
    forecast_accuracy_review    = "forecast_accuracy_review"
    crm_adoption_program        = "crm_adoption_program"


@dataclass
class CRMAdoptionInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_deals_managed: int
    avg_days_since_last_crm_update: float
    deals_not_updated_7d_pct: float
    required_fields_completion_pct: float
    activity_logs_per_deal_per_week: float
    call_logs_per_week: float
    email_logs_per_week: float
    meeting_logs_per_week: float
    next_action_field_completion_pct: float
    close_date_accuracy_score: float
    deal_stage_accuracy_pct: float
    note_quality_score: float
    opportunity_value_update_frequency: float
    custom_fields_completion_pct: float
    contact_role_mapping_pct: float
    duplicate_records_rate_pct: float
    data_entry_lag_hours: float
    deal_age_vs_stage_consistency_score: float
    avg_opportunity_value_usd: float


@dataclass
class CRMAdoptionResult:
    rep_id: str
    region: str
    crm_adoption_risk: CRMAdoptionRisk
    crm_adoption_pattern: CRMAdoptionPattern
    crm_adoption_severity: CRMAdoptionSeverity
    recommended_action: CRMAdoptionAction
    data_freshness_score: float
    data_completeness_score: float
    activity_logging_score: float
    forecast_data_quality_score: float
    crm_adoption_composite: float
    has_crm_gap: bool
    requires_crm_coaching: bool
    estimated_forecast_risk_usd: float
    crm_adoption_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "crm_adoption_risk":                self.crm_adoption_risk.value,
            "crm_adoption_pattern":             self.crm_adoption_pattern.value,
            "crm_adoption_severity":            self.crm_adoption_severity.value,
            "recommended_action":               self.recommended_action.value,
            "data_freshness_score":             self.data_freshness_score,
            "data_completeness_score":          self.data_completeness_score,
            "activity_logging_score":           self.activity_logging_score,
            "forecast_data_quality_score":      self.forecast_data_quality_score,
            "crm_adoption_composite":           self.crm_adoption_composite,
            "has_crm_gap":                      self.has_crm_gap,
            "requires_crm_coaching":            self.requires_crm_coaching,
            "estimated_forecast_risk_usd":      self.estimated_forecast_risk_usd,
            "crm_adoption_signal":              self.crm_adoption_signal,
        }


class SalesCRMAdoptionIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[CRMAdoptionResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _data_freshness_score(self, inp: CRMAdoptionInput) -> float:
        score = 0.0

        if inp.avg_days_since_last_crm_update >= 14.0:
            score += 45.0
        elif inp.avg_days_since_last_crm_update >= 7.0:
            score += 25.0
        elif inp.avg_days_since_last_crm_update >= 3.0:
            score += 8.0

        if inp.deals_not_updated_7d_pct >= 0.60:
            score += 35.0
        elif inp.deals_not_updated_7d_pct >= 0.40:
            score += 18.0
        elif inp.deals_not_updated_7d_pct >= 0.20:
            score += 7.0

        if inp.data_entry_lag_hours >= 48.0:
            score += 20.0
        elif inp.data_entry_lag_hours >= 24.0:
            score += 10.0

        return min(score, 100.0)

    def _data_completeness_score(self, inp: CRMAdoptionInput) -> float:
        score = 0.0

        if inp.required_fields_completion_pct < 0.50:
            score += 40.0
        elif inp.required_fields_completion_pct < 0.70:
            score += 22.0
        elif inp.required_fields_completion_pct < 0.85:
            score += 8.0

        if inp.contact_role_mapping_pct < 0.30:
            score += 35.0
        elif inp.contact_role_mapping_pct < 0.55:
            score += 18.0

        if inp.custom_fields_completion_pct < 0.40:
            score += 25.0
        elif inp.custom_fields_completion_pct < 0.65:
            score += 12.0

        return min(score, 100.0)

    def _activity_logging_score(self, inp: CRMAdoptionInput) -> float:
        score = 0.0

        if inp.activity_logs_per_deal_per_week < 1.0:
            score += 40.0
        elif inp.activity_logs_per_deal_per_week < 2.0:
            score += 20.0
        elif inp.activity_logs_per_deal_per_week < 3.0:
            score += 8.0

        if inp.next_action_field_completion_pct < 0.40:
            score += 35.0
        elif inp.next_action_field_completion_pct < 0.65:
            score += 18.0

        if inp.note_quality_score < 0.30:
            score += 25.0
        elif inp.note_quality_score < 0.55:
            score += 12.0

        return min(score, 100.0)

    def _forecast_data_quality_score(self, inp: CRMAdoptionInput) -> float:
        score = 0.0

        if inp.close_date_accuracy_score < 0.40:
            score += 40.0
        elif inp.close_date_accuracy_score < 0.60:
            score += 22.0
        elif inp.close_date_accuracy_score < 0.80:
            score += 8.0

        if inp.deal_stage_accuracy_pct < 0.50:
            score += 35.0
        elif inp.deal_stage_accuracy_pct < 0.70:
            score += 18.0

        if inp.duplicate_records_rate_pct >= 0.15:
            score += 25.0
        elif inp.duplicate_records_rate_pct >= 0.07:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: CRMAdoptionInput,
                          freshness: float, completeness: float,
                          activity: float, forecast: float) -> CRMAdoptionPattern:
        if freshness >= 40 and inp.avg_days_since_last_crm_update >= 10.0:
            return CRMAdoptionPattern.stale_data

        if completeness >= 35 and inp.required_fields_completion_pct < 0.60:
            return CRMAdoptionPattern.incomplete_records

        if activity >= 35 and inp.activity_logs_per_deal_per_week < 1.5:
            return CRMAdoptionPattern.activity_logging_gap

        if forecast >= 30 and inp.deal_stage_accuracy_pct < 0.60:
            return CRMAdoptionPattern.forecast_data_unreliable

        if freshness >= 20 and inp.data_entry_lag_hours >= 36.0:
            return CRMAdoptionPattern.lazy_entry

        return CRMAdoptionPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> CRMAdoptionRisk:
        if composite >= 60:
            return CRMAdoptionRisk.critical
        if composite >= 40:
            return CRMAdoptionRisk.high
        if composite >= 20:
            return CRMAdoptionRisk.moderate
        return CRMAdoptionRisk.low

    def _severity(self, composite: float) -> CRMAdoptionSeverity:
        if composite >= 60:
            return CRMAdoptionSeverity.abandoned
        if composite >= 40:
            return CRMAdoptionSeverity.neglected
        if composite >= 20:
            return CRMAdoptionSeverity.developing
        return CRMAdoptionSeverity.compliant

    def _action(self, risk: CRMAdoptionRisk,
                 pattern: CRMAdoptionPattern) -> CRMAdoptionAction:
        if risk == CRMAdoptionRisk.critical:
            if pattern == CRMAdoptionPattern.stale_data:
                return CRMAdoptionAction.data_cleanup_session
            if pattern == CRMAdoptionPattern.activity_logging_gap:
                return CRMAdoptionAction.activity_logging_training
            return CRMAdoptionAction.crm_adoption_program
        if risk == CRMAdoptionRisk.high:
            if pattern == CRMAdoptionPattern.forecast_data_unreliable:
                return CRMAdoptionAction.forecast_accuracy_review
            if pattern == CRMAdoptionPattern.incomplete_records:
                return CRMAdoptionAction.data_cleanup_session
            return CRMAdoptionAction.crm_coaching
        if risk == CRMAdoptionRisk.moderate:
            return CRMAdoptionAction.crm_coaching
        return CRMAdoptionAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_crm_gap(self, composite: float,
                      inp: CRMAdoptionInput) -> bool:
        return (
            composite >= 40
            or inp.deals_not_updated_7d_pct >= 0.50
            or inp.required_fields_completion_pct < 0.50
        )

    def _requires_crm_coaching(self, composite: float,
                                inp: CRMAdoptionInput) -> bool:
        return (
            composite >= 30
            or inp.activity_logs_per_deal_per_week < 1.0
            or inp.next_action_field_completion_pct < 0.40
        )

    # ------------------------------------------------------------------
    # Forecast risk estimate
    # ------------------------------------------------------------------

    def _estimated_forecast_risk(self, inp: CRMAdoptionInput,
                                  composite: float) -> float:
        stale_deals = round(inp.total_deals_managed * inp.deals_not_updated_7d_pct)
        return round(stale_deals * inp.avg_opportunity_value_usd * (composite / 100.0) * 0.15, 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: CRMAdoptionInput,
                 pattern: CRMAdoptionPattern, composite: float) -> str:
        if pattern == CRMAdoptionPattern.none and composite < 20:
            return "CRM adoption healthy — data freshness, completeness, and activity logging within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.avg_days_since_last_crm_update:.1f}d avg update lag")
        parts.append(f"{inp.required_fields_completion_pct*100:.0f}% fields complete")
        parts.append(f"{inp.activity_logs_per_deal_per_week:.1f} logs/deal/wk")
        label = pattern.value.replace("_", " ") if pattern != CRMAdoptionPattern.none else "CRM adoption risk"
        summary = " — ".join(parts)
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: CRMAdoptionInput) -> CRMAdoptionResult:
        freshness    = round(self._data_freshness_score(inp), 1)
        completeness = round(self._data_completeness_score(inp), 1)
        activity     = round(self._activity_logging_score(inp), 1)
        forecast     = round(self._forecast_data_quality_score(inp), 1)

        composite = round(
            freshness * 0.30 + completeness * 0.30 + activity * 0.25 + forecast * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, freshness, completeness, activity, forecast)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_crm_gap(composite, inp)
        coach  = self._requires_crm_coaching(composite, inp)
        impact = self._estimated_forecast_risk(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = CRMAdoptionResult(
            rep_id=inp.rep_id,
            region=inp.region,
            crm_adoption_risk=risk,
            crm_adoption_pattern=pattern,
            crm_adoption_severity=severity,
            recommended_action=action,
            data_freshness_score=freshness,
            data_completeness_score=completeness,
            activity_logging_score=activity,
            forecast_data_quality_score=forecast,
            crm_adoption_composite=composite,
            has_crm_gap=gap,
            requires_crm_coaching=coach,
            estimated_forecast_risk_usd=impact,
            crm_adoption_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[CRMAdoptionInput]) -> list[CRMAdoptionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_crm_adoption_composite": 0.0,
                "crm_gap_count": 0,
                "coaching_count": 0,
                "avg_data_freshness_score": 0.0,
                "avg_data_completeness_score": 0.0,
                "avg_activity_logging_score": 0.0,
                "avg_forecast_data_quality_score": 0.0,
                "total_estimated_forecast_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_fr = total_co = total_ac = total_fo = total_impact = 0.0

        for r in self._results:
            risk_counts[r.crm_adoption_risk.value]       = risk_counts.get(r.crm_adoption_risk.value, 0) + 1
            pattern_counts[r.crm_adoption_pattern.value] = pattern_counts.get(r.crm_adoption_pattern.value, 0) + 1
            severity_counts[r.crm_adoption_severity.value] = severity_counts.get(r.crm_adoption_severity.value, 0) + 1
            action_counts[r.recommended_action.value]    = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp   += r.crm_adoption_composite
            total_fr     += r.data_freshness_score
            total_co     += r.data_completeness_score
            total_ac     += r.activity_logging_score
            total_fo     += r.forecast_data_quality_score
            total_impact += r.estimated_forecast_risk_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_crm_adoption_composite":               round(total_comp / n, 1),
            "crm_gap_count":                            sum(1 for r in self._results if r.has_crm_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_crm_coaching),
            "avg_data_freshness_score":                 round(total_fr / n, 1),
            "avg_data_completeness_score":              round(total_co / n, 1),
            "avg_activity_logging_score":               round(total_ac / n, 1),
            "avg_forecast_data_quality_score":          round(total_fo / n, 1),
            "total_estimated_forecast_risk_usd":        round(total_impact, 2),
        }
