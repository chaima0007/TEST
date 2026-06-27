from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ReferenceRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ReferencePattern(str, Enum):
    none                      = "none"
    reference_avoidance       = "reference_avoidance"
    reference_fatigue         = "reference_fatigue"
    single_reference_overuse  = "single_reference_overuse"
    no_case_study_usage       = "no_case_study_usage"
    late_stage_evidence_gap   = "late_stage_evidence_gap"


class ReferenceSeverity(str, Enum):
    evidence_led  = "evidence_led"
    developing    = "developing"
    anecdotal     = "anecdotal"
    blind         = "blind"


class ReferenceAction(str, Enum):
    no_action                    = "no_action"
    reference_program_onboarding = "reference_program_onboarding"
    evidence_library_training    = "evidence_library_training"
    reference_rotation_coaching  = "reference_rotation_coaching"
    case_study_deployment_plan   = "case_study_deployment_plan"
    late_stage_evidence_sprint   = "late_stage_evidence_sprint"


@dataclass
class ReferenceInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_deals_active: int
    deals_with_reference_deployed_pct: float
    avg_references_per_deal: float
    unique_references_used_count: int
    reference_call_conversion_lift_pct: float
    avg_days_to_first_reference: float
    late_stage_reference_rate_pct: float
    deals_with_no_evidence_pct: float
    case_study_deployment_rate_pct: float
    roi_document_shared_pct: float
    testimonial_used_pct: float
    peer_review_site_share_rate_pct: float
    reference_repeat_use_count: int
    reference_burnout_signals_count: int
    analyst_report_leveraged_pct: float
    competitive_displacement_story_used_pct: float
    win_stories_shared_in_pipeline_pct: float
    avg_evidence_assets_per_deal: float
    avg_opportunity_value_usd: float


@dataclass
class ReferenceResult:
    rep_id: str
    region: str
    reference_risk: ReferenceRisk
    reference_pattern: ReferencePattern
    reference_severity: ReferenceSeverity
    recommended_action: ReferenceAction
    reference_utilization_score: float
    evidence_diversity_score: float
    reference_timing_score: float
    evidence_depth_score: float
    reference_composite: float
    has_reference_gap: bool
    requires_reference_coaching: bool
    estimated_win_rate_impact_usd: float
    reference_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "reference_risk":                   self.reference_risk.value,
            "reference_pattern":                self.reference_pattern.value,
            "reference_severity":               self.reference_severity.value,
            "recommended_action":               self.recommended_action.value,
            "reference_utilization_score":      self.reference_utilization_score,
            "evidence_diversity_score":         self.evidence_diversity_score,
            "reference_timing_score":           self.reference_timing_score,
            "evidence_depth_score":             self.evidence_depth_score,
            "reference_composite":              self.reference_composite,
            "has_reference_gap":                self.has_reference_gap,
            "requires_reference_coaching":      self.requires_reference_coaching,
            "estimated_win_rate_impact_usd":    self.estimated_win_rate_impact_usd,
            "reference_signal":                 self.reference_signal,
        }


class SalesReferenceIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ReferenceResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _reference_utilization_score(self, inp: ReferenceInput) -> float:
        score = 0.0

        if inp.deals_with_reference_deployed_pct <= 0.20:
            score += 40.0
        elif inp.deals_with_reference_deployed_pct <= 0.50:
            score += 22.0
        elif inp.deals_with_reference_deployed_pct <= 0.70:
            score += 8.0

        if inp.avg_references_per_deal <= 0.5:
            score += 35.0
        elif inp.avg_references_per_deal <= 1.0:
            score += 18.0

        if inp.deals_with_no_evidence_pct >= 0.50:
            score += 25.0
        elif inp.deals_with_no_evidence_pct >= 0.25:
            score += 12.0

        return min(score, 100.0)

    def _evidence_diversity_score(self, inp: ReferenceInput) -> float:
        score = 0.0

        if inp.unique_references_used_count <= 1:
            score += 40.0
        elif inp.unique_references_used_count <= 3:
            score += 22.0
        elif inp.unique_references_used_count <= 5:
            score += 8.0

        if inp.case_study_deployment_rate_pct <= 0.20:
            score += 35.0
        elif inp.case_study_deployment_rate_pct <= 0.50:
            score += 18.0

        if inp.avg_evidence_assets_per_deal <= 1.0:
            score += 25.0
        elif inp.avg_evidence_assets_per_deal <= 2.0:
            score += 12.0

        return min(score, 100.0)

    def _reference_timing_score(self, inp: ReferenceInput) -> float:
        score = 0.0

        if inp.avg_days_to_first_reference >= 60.0:
            score += 40.0
        elif inp.avg_days_to_first_reference >= 30.0:
            score += 22.0
        elif inp.avg_days_to_first_reference >= 14.0:
            score += 8.0

        if inp.late_stage_reference_rate_pct >= 0.60:
            score += 35.0
        elif inp.late_stage_reference_rate_pct >= 0.40:
            score += 18.0

        if inp.reference_repeat_use_count >= 6:
            score += 25.0
        elif inp.reference_repeat_use_count >= 3:
            score += 12.0

        return min(score, 100.0)

    def _evidence_depth_score(self, inp: ReferenceInput) -> float:
        score = 0.0

        if inp.roi_document_shared_pct <= 0.15:
            score += 45.0
        elif inp.roi_document_shared_pct <= 0.40:
            score += 25.0
        elif inp.roi_document_shared_pct <= 0.65:
            score += 10.0

        if inp.analyst_report_leveraged_pct <= 0.10:
            score += 30.0
        elif inp.analyst_report_leveraged_pct <= 0.30:
            score += 15.0

        if inp.competitive_displacement_story_used_pct <= 0.15:
            score += 25.0
        elif inp.competitive_displacement_story_used_pct <= 0.35:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ReferenceInput,
                         utilization: float, diversity: float,
                         timing: float, depth: float) -> ReferencePattern:
        if utilization >= 40 and inp.deals_with_reference_deployed_pct <= 0.20:
            return ReferencePattern.reference_avoidance

        if timing >= 30 and inp.reference_repeat_use_count >= 4:
            return ReferencePattern.reference_fatigue

        if diversity >= 30 and inp.unique_references_used_count <= 2:
            return ReferencePattern.single_reference_overuse

        if depth >= 30 and inp.case_study_deployment_rate_pct <= 0.20:
            return ReferencePattern.no_case_study_usage

        if timing >= 20 and inp.late_stage_reference_rate_pct >= 0.50:
            return ReferencePattern.late_stage_evidence_gap

        return ReferencePattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ReferenceRisk:
        if composite >= 60:
            return ReferenceRisk.critical
        if composite >= 40:
            return ReferenceRisk.high
        if composite >= 20:
            return ReferenceRisk.moderate
        return ReferenceRisk.low

    def _severity(self, composite: float) -> ReferenceSeverity:
        if composite >= 60:
            return ReferenceSeverity.blind
        if composite >= 40:
            return ReferenceSeverity.anecdotal
        if composite >= 20:
            return ReferenceSeverity.developing
        return ReferenceSeverity.evidence_led

    def _action(self, risk: ReferenceRisk, pattern: ReferencePattern) -> ReferenceAction:
        if risk == ReferenceRisk.critical:
            if pattern == ReferencePattern.reference_fatigue:
                return ReferenceAction.reference_rotation_coaching
            if pattern == ReferencePattern.no_case_study_usage:
                return ReferenceAction.case_study_deployment_plan
            return ReferenceAction.reference_program_onboarding
        if risk == ReferenceRisk.high:
            if pattern == ReferencePattern.late_stage_evidence_gap:
                return ReferenceAction.late_stage_evidence_sprint
            if pattern == ReferencePattern.single_reference_overuse:
                return ReferenceAction.reference_rotation_coaching
            return ReferenceAction.evidence_library_training
        if risk == ReferenceRisk.moderate:
            return ReferenceAction.evidence_library_training
        return ReferenceAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_reference_gap(self, composite: float, inp: ReferenceInput) -> bool:
        return (
            composite >= 40
            or inp.deals_with_reference_deployed_pct <= 0.20
            or inp.deals_with_no_evidence_pct >= 0.40
        )

    def _requires_reference_coaching(self, composite: float, inp: ReferenceInput) -> bool:
        return (
            composite >= 30
            or inp.case_study_deployment_rate_pct <= 0.25
            or inp.unique_references_used_count <= 2
        )

    # ------------------------------------------------------------------
    # Win-rate impact estimate
    # ------------------------------------------------------------------

    def _estimated_win_rate_impact(self, inp: ReferenceInput, composite: float) -> float:
        evidence_free_deals = round(inp.total_deals_active * inp.deals_with_no_evidence_pct)
        lift_gap = max(0.0, inp.reference_call_conversion_lift_pct)
        return round(evidence_free_deals * inp.avg_opportunity_value_usd * lift_gap * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ReferenceInput,
                 pattern: ReferencePattern, composite: float) -> str:
        if pattern == ReferencePattern.none and composite < 20:
            return "Reference usage healthy — customer evidence, case studies, and ROI assets deployed within benchmarks"
        parts: list[str] = []
        if inp.deals_with_reference_deployed_pct < 1.0:
            parts.append(f"{inp.deals_with_reference_deployed_pct*100:.0f}% deals with reference")
        if inp.deals_with_no_evidence_pct < 1.0:
            parts.append(f"{inp.deals_with_no_evidence_pct*100:.0f}% deals without evidence")
        parts.append(f"{inp.unique_references_used_count} unique refs")
        label = pattern.value.replace("_", " ") if pattern != ReferencePattern.none else "Reference gap"
        summary = " — ".join(parts) if parts else "evidence gap elevated"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ReferenceInput) -> ReferenceResult:
        utilization = round(self._reference_utilization_score(inp), 1)
        diversity   = round(self._evidence_diversity_score(inp), 1)
        timing      = round(self._reference_timing_score(inp), 1)
        depth       = round(self._evidence_depth_score(inp), 1)

        composite = round(
            utilization * 0.30 + diversity * 0.30 + timing * 0.25 + depth * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, utilization, diversity, timing, depth)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_reference_gap(composite, inp)
        coach  = self._requires_reference_coaching(composite, inp)
        impact = self._estimated_win_rate_impact(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = ReferenceResult(
            rep_id=inp.rep_id,
            region=inp.region,
            reference_risk=risk,
            reference_pattern=pattern,
            reference_severity=severity,
            recommended_action=action,
            reference_utilization_score=utilization,
            evidence_diversity_score=diversity,
            reference_timing_score=timing,
            evidence_depth_score=depth,
            reference_composite=composite,
            has_reference_gap=gap,
            requires_reference_coaching=coach,
            estimated_win_rate_impact_usd=impact,
            reference_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ReferenceInput]) -> list[ReferenceResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_reference_composite": 0.0,
                "reference_gap_count": 0,
                "coaching_count": 0,
                "avg_reference_utilization_score": 0.0,
                "avg_evidence_diversity_score": 0.0,
                "avg_reference_timing_score": 0.0,
                "avg_evidence_depth_score": 0.0,
                "total_estimated_win_rate_impact_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_uti = total_div = total_tim = total_dep = total_impact = 0.0

        for r in self._results:
            risk_counts[r.reference_risk.value]       = risk_counts.get(r.reference_risk.value, 0) + 1
            pattern_counts[r.reference_pattern.value] = pattern_counts.get(r.reference_pattern.value, 0) + 1
            severity_counts[r.reference_severity.value] = severity_counts.get(r.reference_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp   += r.reference_composite
            total_uti    += r.reference_utilization_score
            total_div    += r.evidence_diversity_score
            total_tim    += r.reference_timing_score
            total_dep    += r.evidence_depth_score
            total_impact += r.estimated_win_rate_impact_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_reference_composite":                  round(total_comp / n, 1),
            "reference_gap_count":                      sum(1 for r in self._results if r.has_reference_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_reference_coaching),
            "avg_reference_utilization_score":          round(total_uti / n, 1),
            "avg_evidence_diversity_score":             round(total_div / n, 1),
            "avg_reference_timing_score":               round(total_tim / n, 1),
            "avg_evidence_depth_score":                 round(total_dep / n, 1),
            "total_estimated_win_rate_impact_usd":      round(total_impact, 2),
        }
