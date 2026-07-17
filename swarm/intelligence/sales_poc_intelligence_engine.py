from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class POCRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class POCPattern(str, Enum):
    none                          = "none"
    poc_stall                     = "poc_stall"
    success_criteria_gap          = "success_criteria_gap"
    scope_creep                   = "scope_creep"
    technical_validation_failure  = "technical_validation_failure"
    no_champion_during_poc        = "no_champion_during_poc"


class POCSeverity(str, Enum):
    structured   = "structured"
    developing   = "developing"
    uncontrolled = "uncontrolled"
    failing      = "failing"


class POCAction(str, Enum):
    no_action                       = "no_action"
    poc_structure_coaching          = "poc_structure_coaching"
    success_criteria_alignment      = "success_criteria_alignment"
    scope_control_training          = "scope_control_training"
    technical_escalation_support    = "technical_escalation_support"
    champion_engagement_during_poc  = "champion_engagement_during_poc"


@dataclass
class POCInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_pocs_conducted: int
    poc_to_close_conversion_rate_pct: float
    avg_poc_duration_days: float
    pocs_exceeding_timeline_pct: float
    pocs_with_no_success_criteria_pct: float
    avg_poc_scope_changes_count: float
    technical_validation_failure_rate_pct: float
    poc_champion_engaged_pct: float
    exec_sponsor_briefed_pct: float
    avg_days_to_poc_kickoff: float
    poc_extended_count: int
    mutual_success_plan_completion_pct: float
    se_escalation_required_pct: float
    poc_abandoned_pct: float
    post_poc_proposal_delay_days: float
    competitive_poc_displacement_rate_pct: float
    avg_stakeholders_in_poc_count: float
    avg_poc_resources_allocated_count: int
    avg_opportunity_value_usd: float


@dataclass
class POCResult:
    rep_id: str
    region: str
    poc_risk: POCRisk
    poc_pattern: POCPattern
    poc_severity: POCSeverity
    recommended_action: POCAction
    poc_structure_score: float
    poc_execution_score: float
    poc_stakeholder_score: float
    poc_conversion_score: float
    poc_composite: float
    has_poc_gap: bool
    requires_poc_coaching: bool
    estimated_pipeline_loss_usd: float
    poc_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "poc_risk":                         self.poc_risk.value,
            "poc_pattern":                      self.poc_pattern.value,
            "poc_severity":                     self.poc_severity.value,
            "recommended_action":               self.recommended_action.value,
            "poc_structure_score":              self.poc_structure_score,
            "poc_execution_score":              self.poc_execution_score,
            "poc_stakeholder_score":            self.poc_stakeholder_score,
            "poc_conversion_score":             self.poc_conversion_score,
            "poc_composite":                    self.poc_composite,
            "has_poc_gap":                      self.has_poc_gap,
            "requires_poc_coaching":            self.requires_poc_coaching,
            "estimated_pipeline_loss_usd":      self.estimated_pipeline_loss_usd,
            "poc_signal":                       self.poc_signal,
        }


class SalesPOCIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[POCResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _poc_structure_score(self, inp: POCInput) -> float:
        score = 0.0

        if inp.pocs_with_no_success_criteria_pct >= 0.60:
            score += 40.0
        elif inp.pocs_with_no_success_criteria_pct >= 0.30:
            score += 22.0
        elif inp.pocs_with_no_success_criteria_pct >= 0.15:
            score += 8.0

        if inp.mutual_success_plan_completion_pct <= 0.20:
            score += 35.0
        elif inp.mutual_success_plan_completion_pct <= 0.50:
            score += 18.0

        if inp.avg_days_to_poc_kickoff >= 21.0:
            score += 25.0
        elif inp.avg_days_to_poc_kickoff >= 10.0:
            score += 12.0

        return min(score, 100.0)

    def _poc_execution_score(self, inp: POCInput) -> float:
        score = 0.0

        if inp.pocs_exceeding_timeline_pct >= 0.60:
            score += 40.0
        elif inp.pocs_exceeding_timeline_pct >= 0.30:
            score += 22.0
        elif inp.pocs_exceeding_timeline_pct >= 0.15:
            score += 8.0

        if inp.avg_poc_scope_changes_count >= 3.0:
            score += 35.0
        elif inp.avg_poc_scope_changes_count >= 1.5:
            score += 18.0

        if inp.poc_abandoned_pct >= 0.30:
            score += 25.0
        elif inp.poc_abandoned_pct >= 0.15:
            score += 12.0

        return min(score, 100.0)

    def _poc_stakeholder_score(self, inp: POCInput) -> float:
        score = 0.0

        if inp.poc_champion_engaged_pct <= 0.30:
            score += 45.0
        elif inp.poc_champion_engaged_pct <= 0.60:
            score += 25.0
        elif inp.poc_champion_engaged_pct <= 0.80:
            score += 10.0

        if inp.exec_sponsor_briefed_pct <= 0.20:
            score += 30.0
        elif inp.exec_sponsor_briefed_pct <= 0.50:
            score += 15.0

        if inp.avg_stakeholders_in_poc_count <= 1.0:
            score += 25.0
        elif inp.avg_stakeholders_in_poc_count <= 2.0:
            score += 12.0

        return min(score, 100.0)

    def _poc_conversion_score(self, inp: POCInput) -> float:
        score = 0.0

        if inp.poc_to_close_conversion_rate_pct <= 0.20:
            score += 45.0
        elif inp.poc_to_close_conversion_rate_pct <= 0.40:
            score += 25.0
        elif inp.poc_to_close_conversion_rate_pct <= 0.60:
            score += 10.0

        if inp.technical_validation_failure_rate_pct >= 0.30:
            score += 30.0
        elif inp.technical_validation_failure_rate_pct >= 0.15:
            score += 15.0

        if inp.competitive_poc_displacement_rate_pct >= 0.30:
            score += 25.0
        elif inp.competitive_poc_displacement_rate_pct >= 0.15:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: POCInput,
                         structure: float, execution: float,
                         stakeholder: float, conversion: float) -> POCPattern:
        if execution >= 40 and inp.pocs_exceeding_timeline_pct >= 0.40:
            return POCPattern.poc_stall

        if structure >= 40 and inp.pocs_with_no_success_criteria_pct >= 0.40:
            return POCPattern.success_criteria_gap

        if execution >= 30 and inp.avg_poc_scope_changes_count >= 2.0:
            return POCPattern.scope_creep

        if conversion >= 30 and inp.technical_validation_failure_rate_pct >= 0.20:
            return POCPattern.technical_validation_failure

        if stakeholder >= 30 and inp.poc_champion_engaged_pct <= 0.40:
            return POCPattern.no_champion_during_poc

        return POCPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> POCRisk:
        if composite >= 60:
            return POCRisk.critical
        if composite >= 40:
            return POCRisk.high
        if composite >= 20:
            return POCRisk.moderate
        return POCRisk.low

    def _severity(self, composite: float) -> POCSeverity:
        if composite >= 60:
            return POCSeverity.failing
        if composite >= 40:
            return POCSeverity.uncontrolled
        if composite >= 20:
            return POCSeverity.developing
        return POCSeverity.structured

    def _action(self, risk: POCRisk, pattern: POCPattern) -> POCAction:
        if risk == POCRisk.critical:
            if pattern == POCPattern.technical_validation_failure:
                return POCAction.technical_escalation_support
            if pattern == POCPattern.no_champion_during_poc:
                return POCAction.champion_engagement_during_poc
            return POCAction.poc_structure_coaching
        if risk == POCRisk.high:
            if pattern == POCPattern.success_criteria_gap:
                return POCAction.success_criteria_alignment
            if pattern == POCPattern.scope_creep:
                return POCAction.scope_control_training
            return POCAction.poc_structure_coaching
        if risk == POCRisk.moderate:
            return POCAction.success_criteria_alignment
        return POCAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_poc_gap(self, composite: float, inp: POCInput) -> bool:
        return (
            composite >= 40
            or inp.poc_to_close_conversion_rate_pct <= 0.20
            or inp.poc_abandoned_pct >= 0.25
        )

    def _requires_poc_coaching(self, composite: float, inp: POCInput) -> bool:
        return (
            composite >= 30
            or inp.pocs_with_no_success_criteria_pct >= 0.35
            or inp.poc_champion_engaged_pct <= 0.40
        )

    # ------------------------------------------------------------------
    # Pipeline loss estimate
    # ------------------------------------------------------------------

    def _estimated_pipeline_loss(self, inp: POCInput, composite: float) -> float:
        abandoned = round(inp.total_pocs_conducted * inp.poc_abandoned_pct)
        return round(abandoned * inp.avg_opportunity_value_usd * (composite / 100.0) * 0.30, 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: POCInput, pattern: POCPattern, composite: float) -> str:
        if pattern == POCPattern.none and composite < 20:
            return "POC execution healthy — structure, conversion, and champion engagement within benchmarks"
        parts: list[str] = []
        if inp.poc_to_close_conversion_rate_pct < 1.0:
            parts.append(f"{inp.poc_to_close_conversion_rate_pct*100:.0f}% POC-to-close")
        if inp.pocs_exceeding_timeline_pct < 1.0:
            parts.append(f"{inp.pocs_exceeding_timeline_pct*100:.0f}% stalled POCs")
        parts.append(f"{inp.avg_poc_duration_days:.0f} avg POC days")
        label = pattern.value.replace("_", " ") if pattern != POCPattern.none else "POC risk"
        summary = " — ".join(parts) if parts else "POC dependency elevated"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: POCInput) -> POCResult:
        structure   = round(self._poc_structure_score(inp), 1)
        execution   = round(self._poc_execution_score(inp), 1)
        stakeholder = round(self._poc_stakeholder_score(inp), 1)
        conversion  = round(self._poc_conversion_score(inp), 1)

        composite = round(
            structure * 0.30 + execution * 0.30 + stakeholder * 0.25 + conversion * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, structure, execution, stakeholder, conversion)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_poc_gap(composite, inp)
        coach  = self._requires_poc_coaching(composite, inp)
        loss   = self._estimated_pipeline_loss(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = POCResult(
            rep_id=inp.rep_id,
            region=inp.region,
            poc_risk=risk,
            poc_pattern=pattern,
            poc_severity=severity,
            recommended_action=action,
            poc_structure_score=structure,
            poc_execution_score=execution,
            poc_stakeholder_score=stakeholder,
            poc_conversion_score=conversion,
            poc_composite=composite,
            has_poc_gap=gap,
            requires_poc_coaching=coach,
            estimated_pipeline_loss_usd=loss,
            poc_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[POCInput]) -> list[POCResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_poc_composite": 0.0,
                "poc_gap_count": 0,
                "coaching_count": 0,
                "avg_poc_structure_score": 0.0,
                "avg_poc_execution_score": 0.0,
                "avg_poc_stakeholder_score": 0.0,
                "avg_poc_conversion_score": 0.0,
                "total_estimated_pipeline_loss_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_str = total_exc = total_stk = total_cvt = total_loss = 0.0

        for r in self._results:
            risk_counts[r.poc_risk.value]       = risk_counts.get(r.poc_risk.value, 0) + 1
            pattern_counts[r.poc_pattern.value] = pattern_counts.get(r.poc_pattern.value, 0) + 1
            severity_counts[r.poc_severity.value] = severity_counts.get(r.poc_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.poc_composite
            total_str  += r.poc_structure_score
            total_exc  += r.poc_execution_score
            total_stk  += r.poc_stakeholder_score
            total_cvt  += r.poc_conversion_score
            total_loss += r.estimated_pipeline_loss_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_poc_composite":                    round(total_comp / n, 1),
            "poc_gap_count":                        sum(1 for r in self._results if r.has_poc_gap),
            "coaching_count":                       sum(1 for r in self._results if r.requires_poc_coaching),
            "avg_poc_structure_score":              round(total_str / n, 1),
            "avg_poc_execution_score":              round(total_exc / n, 1),
            "avg_poc_stakeholder_score":            round(total_stk / n, 1),
            "avg_poc_conversion_score":             round(total_cvt / n, 1),
            "total_estimated_pipeline_loss_usd":    round(total_loss, 2),
        }
