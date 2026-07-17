from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class DiscoveryRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class DiscoveryPattern(str, Enum):
    none                    = "none"
    surface_level_discovery = "surface_level_discovery"
    budget_avoidance        = "budget_avoidance"
    single_stakeholder_lock = "single_stakeholder_lock"
    pain_point_skipping     = "pain_point_skipping"
    premature_solutioning   = "premature_solutioning"


class DiscoverySeverity(str, Enum):
    thorough   = "thorough"
    adequate   = "adequate"
    shallow    = "shallow"
    negligent  = "negligent"


class DiscoveryAction(str, Enum):
    no_action                     = "no_action"
    discovery_framework_coaching  = "discovery_framework_coaching"
    budget_qualification_coaching = "budget_qualification_coaching"
    stakeholder_mapping_coaching  = "stakeholder_mapping_coaching"
    pain_discovery_coaching       = "pain_discovery_coaching"
    discovery_reset_intervention  = "discovery_reset_intervention"


@dataclass
class DiscoveryInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    avg_discovery_questions_per_call: float
    business_impact_quantified_pct: float
    pain_points_documented_per_deal: float
    budget_qualified_before_demo_pct: float
    decision_process_mapped_pct: float
    timeline_established_in_discovery_pct: float
    stakeholders_identified_in_discovery_avg: float
    economic_buyer_engaged_pre_proposal_pct: float
    technical_buyer_engaged_pre_proposal_pct: float
    solution_presented_before_discovery_pct: float
    demo_given_without_discovery_pct: float
    follow_up_discovery_call_rate_pct: float
    discovery_to_proposal_gap_days: float
    proposal_rework_rate_pct: float
    deals_lost_due_to_poor_fit_pct: float
    competitor_mentioned_in_discovery_pct: float
    success_criteria_defined_in_discovery_pct: float
    total_discovery_calls: int
    avg_opportunity_value_usd: float


@dataclass
class DiscoveryResult:
    rep_id: str
    region: str
    discovery_risk: DiscoveryRisk
    discovery_pattern: DiscoveryPattern
    discovery_severity: DiscoverySeverity
    recommended_action: DiscoveryAction
    depth_score: float
    qualification_score: float
    stakeholder_score: float
    fit_score: float
    discovery_composite: float
    has_discovery_gap: bool
    requires_discovery_coaching: bool
    estimated_wasted_pipeline_usd: float
    discovery_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                          self.rep_id,
            "region":                          self.region,
            "discovery_risk":                  self.discovery_risk.value,
            "discovery_pattern":               self.discovery_pattern.value,
            "discovery_severity":              self.discovery_severity.value,
            "recommended_action":              self.recommended_action.value,
            "depth_score":                     self.depth_score,
            "qualification_score":             self.qualification_score,
            "stakeholder_score":               self.stakeholder_score,
            "fit_score":                       self.fit_score,
            "discovery_composite":             self.discovery_composite,
            "has_discovery_gap":               self.has_discovery_gap,
            "requires_discovery_coaching":     self.requires_discovery_coaching,
            "estimated_wasted_pipeline_usd":   self.estimated_wasted_pipeline_usd,
            "discovery_signal":                self.discovery_signal,
        }


class SalesDiscoveryQualityIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[DiscoveryResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _depth_score(self, inp: DiscoveryInput) -> float:
        score = 0.0

        if inp.avg_discovery_questions_per_call <= 5.0:
            score += 40.0
        elif inp.avg_discovery_questions_per_call <= 10.0:
            score += 22.0
        elif inp.avg_discovery_questions_per_call <= 15.0:
            score += 8.0

        if inp.pain_points_documented_per_deal <= 1.0:
            score += 35.0
        elif inp.pain_points_documented_per_deal <= 2.5:
            score += 18.0

        if inp.business_impact_quantified_pct <= 0.25:
            score += 25.0
        elif inp.business_impact_quantified_pct <= 0.50:
            score += 12.0

        return min(score, 100.0)

    def _qualification_score(self, inp: DiscoveryInput) -> float:
        score = 0.0

        if inp.budget_qualified_before_demo_pct <= 0.30:
            score += 40.0
        elif inp.budget_qualified_before_demo_pct <= 0.55:
            score += 22.0
        elif inp.budget_qualified_before_demo_pct <= 0.75:
            score += 8.0

        if inp.decision_process_mapped_pct <= 0.30:
            score += 35.0
        elif inp.decision_process_mapped_pct <= 0.55:
            score += 18.0

        if inp.timeline_established_in_discovery_pct <= 0.35:
            score += 25.0
        elif inp.timeline_established_in_discovery_pct <= 0.60:
            score += 12.0

        return min(score, 100.0)

    def _stakeholder_score(self, inp: DiscoveryInput) -> float:
        score = 0.0

        if inp.stakeholders_identified_in_discovery_avg <= 1.5:
            score += 45.0
        elif inp.stakeholders_identified_in_discovery_avg <= 2.5:
            score += 25.0
        elif inp.stakeholders_identified_in_discovery_avg <= 3.5:
            score += 10.0

        if inp.economic_buyer_engaged_pre_proposal_pct <= 0.25:
            score += 30.0
        elif inp.economic_buyer_engaged_pre_proposal_pct <= 0.50:
            score += 15.0

        if inp.technical_buyer_engaged_pre_proposal_pct <= 0.20:
            score += 25.0
        elif inp.technical_buyer_engaged_pre_proposal_pct <= 0.45:
            score += 12.0

        return min(score, 100.0)

    def _fit_score(self, inp: DiscoveryInput) -> float:
        score = 0.0

        if inp.solution_presented_before_discovery_pct >= 0.40:
            score += 40.0
        elif inp.solution_presented_before_discovery_pct >= 0.20:
            score += 22.0
        elif inp.solution_presented_before_discovery_pct >= 0.10:
            score += 8.0

        if inp.deals_lost_due_to_poor_fit_pct >= 0.40:
            score += 35.0
        elif inp.deals_lost_due_to_poor_fit_pct >= 0.20:
            score += 18.0

        if inp.proposal_rework_rate_pct >= 0.50:
            score += 25.0
        elif inp.proposal_rework_rate_pct >= 0.25:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: DiscoveryInput,
                         depth: float, qualification: float,
                         stakeholder: float, fit: float) -> DiscoveryPattern:
        # Premature solutioning: pitching before understanding the problem
        if inp.solution_presented_before_discovery_pct >= 0.35 and inp.demo_given_without_discovery_pct >= 0.30:
            return DiscoveryPattern.premature_solutioning

        # Surface level discovery: too few questions, too shallow
        if depth >= 40 and inp.avg_discovery_questions_per_call <= 8.0:
            return DiscoveryPattern.surface_level_discovery

        # Budget avoidance: never qualifies budget before spending time
        if inp.budget_qualified_before_demo_pct <= 0.25 and qualification >= 35:
            return DiscoveryPattern.budget_avoidance

        # Single stakeholder lock: only talks to one person
        if inp.stakeholders_identified_in_discovery_avg <= 1.5 and stakeholder >= 30:
            return DiscoveryPattern.single_stakeholder_lock

        # Pain point skipping: doesn't document pain, loses on poor fit
        if inp.pain_points_documented_per_deal <= 1.5 and inp.deals_lost_due_to_poor_fit_pct >= 0.30:
            return DiscoveryPattern.pain_point_skipping

        return DiscoveryPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> DiscoveryRisk:
        if composite >= 60:
            return DiscoveryRisk.critical
        if composite >= 40:
            return DiscoveryRisk.high
        if composite >= 20:
            return DiscoveryRisk.moderate
        return DiscoveryRisk.low

    def _severity(self, composite: float) -> DiscoverySeverity:
        if composite >= 60:
            return DiscoverySeverity.negligent
        if composite >= 40:
            return DiscoverySeverity.shallow
        if composite >= 20:
            return DiscoverySeverity.adequate
        return DiscoverySeverity.thorough

    def _action(self, risk: DiscoveryRisk, pattern: DiscoveryPattern) -> DiscoveryAction:
        if risk == DiscoveryRisk.critical:
            if pattern == DiscoveryPattern.premature_solutioning:
                return DiscoveryAction.discovery_framework_coaching
            if pattern == DiscoveryPattern.surface_level_discovery:
                return DiscoveryAction.pain_discovery_coaching
            return DiscoveryAction.discovery_reset_intervention
        if risk == DiscoveryRisk.high:
            if pattern == DiscoveryPattern.budget_avoidance:
                return DiscoveryAction.budget_qualification_coaching
            if pattern == DiscoveryPattern.single_stakeholder_lock:
                return DiscoveryAction.stakeholder_mapping_coaching
            return DiscoveryAction.discovery_framework_coaching
        if risk == DiscoveryRisk.moderate:
            return DiscoveryAction.discovery_framework_coaching
        return DiscoveryAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_discovery_gap(self, composite: float, inp: DiscoveryInput) -> bool:
        return (
            composite >= 40
            or inp.budget_qualified_before_demo_pct <= 0.40
            or inp.deals_lost_due_to_poor_fit_pct >= 0.25
        )

    def _requires_discovery_coaching(self, composite: float, inp: DiscoveryInput) -> bool:
        return (
            composite >= 30
            or inp.avg_discovery_questions_per_call <= 10.0
            or inp.solution_presented_before_discovery_pct >= 0.20
        )

    # ------------------------------------------------------------------
    # Wasted pipeline estimate
    # ------------------------------------------------------------------

    def _estimated_wasted_pipeline(self, inp: DiscoveryInput, composite: float) -> float:
        return round(
            inp.total_discovery_calls
            * inp.avg_opportunity_value_usd
            * inp.deals_lost_due_to_poor_fit_pct
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: DiscoveryInput,
                 pattern: DiscoveryPattern, composite: float) -> str:
        if pattern == DiscoveryPattern.none and composite < 20:
            return "Discovery quality strong — depth of questioning, qualification, and stakeholder mapping within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.avg_discovery_questions_per_call:.0f} avg questions per call")
        parts.append(f"{inp.budget_qualified_before_demo_pct * 100:.0f}% budget qualified before demo")
        parts.append(f"{inp.deals_lost_due_to_poor_fit_pct * 100:.0f}% deals lost to poor fit")
        label = pattern.value.replace("_", " ") if pattern != DiscoveryPattern.none else "Discovery risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: DiscoveryInput) -> DiscoveryResult:
        depth         = round(self._depth_score(inp), 1)
        qualification = round(self._qualification_score(inp), 1)
        stakeholder   = round(self._stakeholder_score(inp), 1)
        fit           = round(self._fit_score(inp), 1)

        composite = round(
            depth * 0.30 + qualification * 0.30 + stakeholder * 0.25 + fit * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, depth, qualification, stakeholder, fit)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_discovery_gap(composite, inp)
        coach  = self._requires_discovery_coaching(composite, inp)
        loss   = self._estimated_wasted_pipeline(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = DiscoveryResult(
            rep_id=inp.rep_id,
            region=inp.region,
            discovery_risk=risk,
            discovery_pattern=pattern,
            discovery_severity=severity,
            recommended_action=action,
            depth_score=depth,
            qualification_score=qualification,
            stakeholder_score=stakeholder,
            fit_score=fit,
            discovery_composite=composite,
            has_discovery_gap=gap,
            requires_discovery_coaching=coach,
            estimated_wasted_pipeline_usd=loss,
            discovery_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[DiscoveryInput]) -> list[DiscoveryResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_discovery_composite": 0.0,
                "discovery_gap_count": 0,
                "coaching_count": 0,
                "avg_depth_score": 0.0,
                "avg_qualification_score": 0.0,
                "avg_stakeholder_score": 0.0,
                "avg_fit_score": 0.0,
                "total_estimated_wasted_pipeline_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_dep = total_qua = total_sta = total_fit = total_loss = 0.0

        for r in self._results:
            risk_counts[r.discovery_risk.value]         = risk_counts.get(r.discovery_risk.value, 0) + 1
            pattern_counts[r.discovery_pattern.value]   = pattern_counts.get(r.discovery_pattern.value, 0) + 1
            severity_counts[r.discovery_severity.value] = severity_counts.get(r.discovery_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.discovery_composite
            total_dep  += r.depth_score
            total_qua  += r.qualification_score
            total_sta  += r.stakeholder_score
            total_fit  += r.fit_score
            total_loss += r.estimated_wasted_pipeline_usd

        n = len(self._results)

        return {
            "total":                                   n,
            "risk_counts":                             risk_counts,
            "pattern_counts":                          pattern_counts,
            "severity_counts":                         severity_counts,
            "action_counts":                           action_counts,
            "avg_discovery_composite":                 round(total_comp / n, 1),
            "discovery_gap_count":                     sum(1 for r in self._results if r.has_discovery_gap),
            "coaching_count":                          sum(1 for r in self._results if r.requires_discovery_coaching),
            "avg_depth_score":                         round(total_dep / n, 1),
            "avg_qualification_score":                 round(total_qua / n, 1),
            "avg_stakeholder_score":                   round(total_sta / n, 1),
            "avg_fit_score":                           round(total_fit / n, 1),
            "total_estimated_wasted_pipeline_usd":     round(total_loss, 2),
        }
