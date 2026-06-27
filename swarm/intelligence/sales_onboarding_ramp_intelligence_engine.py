from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class RampRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class RampPattern(str, Enum):
    none                  = "none"
    slow_starter          = "slow_starter"
    knowledge_gap_blocker = "knowledge_gap_blocker"
    pipeline_builder_fail = "pipeline_builder_fail"
    manager_orphan        = "manager_orphan"
    confidence_collapse   = "confidence_collapse"


class RampSeverity(str, Enum):
    on_track   = "on_track"
    at_risk    = "at_risk"
    behind     = "behind"
    critical   = "critical"


class RampAction(str, Enum):
    no_action                    = "no_action"
    ramp_check_in                = "ramp_check_in"
    product_knowledge_coaching   = "product_knowledge_coaching"
    pipeline_building_coaching   = "pipeline_building_coaching"
    manager_engagement_review    = "manager_engagement_review"
    structured_ramp_acceleration = "structured_ramp_acceleration"
    ramp_extension_or_reset      = "ramp_extension_or_reset"


@dataclass
class RampInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    weeks_since_start:                   int     # tenure in weeks
    quota_attainment_vs_ramp_plan_pct:   float   # 0-1 actual vs expected ramp quota
    first_meeting_booked_days:           float   # days to book first meeting
    first_opportunity_created_days:      float   # days to create first opportunity
    product_certification_completion_pct: float  # 0-1 % of certs completed
    training_module_completion_pct:      float   # 0-1
    call_shadowing_sessions_completed:   int
    manager_1on1_frequency_per_month:    float   # avg per month
    pipeline_coverage_ratio:             float   # pipeline vs ramp quota
    avg_deal_size_vs_team_avg_pct:       float   # 0-1 (1.0 = at team avg)
    outbound_activity_vs_plan_pct:       float   # 0-1 vs expected activity
    discovery_call_pass_rate_pct:        float   # 0-1 % calls meeting discovery bar
    demo_to_next_step_rate_pct:          float   # 0-1
    competitive_win_rate_ramp_pct:       float   # 0-1 during ramp period
    peer_buddy_engagement_score:         float   # 0-1 engagement with buddy program
    onboarding_satisfaction_score:       float   # 0-1 self-reported
    net_promoter_internal_score:         float   # 0-1 (would recommend joining)
    tool_adoption_rate_pct:              float   # 0-1 CRM/tools adoption
    avg_deal_value_usd:                  float


@dataclass
class RampResult:
    rep_id:                          str
    region:                          str
    ramp_risk:                       RampRisk
    ramp_pattern:                    RampPattern
    ramp_severity:                   RampSeverity
    recommended_action:              RampAction
    readiness_score:                 float
    activity_score:                  float
    pipeline_score:                  float
    manager_support_score:           float
    ramp_composite:                  float
    has_ramp_gap:                    bool
    requires_ramp_intervention:      bool
    estimated_ramp_revenue_risk_usd: float
    ramp_signal:                     str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                            self.rep_id,
            "region":                            self.region,
            "ramp_risk":                         self.ramp_risk.value,
            "ramp_pattern":                      self.ramp_pattern.value,
            "ramp_severity":                     self.ramp_severity.value,
            "recommended_action":                self.recommended_action.value,
            "readiness_score":                   self.readiness_score,
            "activity_score":                    self.activity_score,
            "pipeline_score":                    self.pipeline_score,
            "manager_support_score":             self.manager_support_score,
            "ramp_composite":                    self.ramp_composite,
            "has_ramp_gap":                      self.has_ramp_gap,
            "requires_ramp_intervention":        self.requires_ramp_intervention,
            "estimated_ramp_revenue_risk_usd":   self.estimated_ramp_revenue_risk_usd,
            "ramp_signal":                       self.ramp_signal,
        }


class SalesOnboardingRampIntelligenceEngine:
    """Detects new rep ramp failures before they miss first-year quota targets."""

    def __init__(self) -> None:
        self._results: List[RampResult] = []

    # ── sub-scores ─────────────────────────────────────────────────────────────

    def _readiness_score(self, inp: RampInput) -> float:
        s = 0.0
        if   inp.product_certification_completion_pct <= 0.30: s += 40
        elif inp.product_certification_completion_pct <= 0.60: s += 22
        elif inp.product_certification_completion_pct <= 0.80: s += 8
        if   inp.training_module_completion_pct       <= 0.30: s += 35
        elif inp.training_module_completion_pct       <= 0.60: s += 18
        if   inp.tool_adoption_rate_pct               <= 0.30: s += 25
        elif inp.tool_adoption_rate_pct               <= 0.60: s += 12
        return min(s, 100.0)

    def _activity_score(self, inp: RampInput) -> float:
        s = 0.0
        if   inp.outbound_activity_vs_plan_pct        <= 0.40: s += 45
        elif inp.outbound_activity_vs_plan_pct        <= 0.65: s += 25
        elif inp.outbound_activity_vs_plan_pct        <= 0.85: s += 10
        if   inp.first_meeting_booked_days            >= 21:   s += 30
        elif inp.first_meeting_booked_days            >= 12:   s += 15
        if   inp.discovery_call_pass_rate_pct         <= 0.25: s += 25
        elif inp.discovery_call_pass_rate_pct         <= 0.50: s += 12
        return min(s, 100.0)

    def _pipeline_score(self, inp: RampInput) -> float:
        s = 0.0
        if   inp.quota_attainment_vs_ramp_plan_pct    <= 0.30: s += 40
        elif inp.quota_attainment_vs_ramp_plan_pct    <= 0.60: s += 22
        elif inp.quota_attainment_vs_ramp_plan_pct    <= 0.85: s += 8
        if   inp.pipeline_coverage_ratio              <= 1.0:  s += 35
        elif inp.pipeline_coverage_ratio              <= 2.0:  s += 18
        if   inp.first_opportunity_created_days       >= 30:   s += 25
        elif inp.first_opportunity_created_days       >= 18:   s += 12
        return min(s, 100.0)

    def _manager_support_score(self, inp: RampInput) -> float:
        s = 0.0
        if   inp.manager_1on1_frequency_per_month     <= 1.0:  s += 45
        elif inp.manager_1on1_frequency_per_month     <= 2.0:  s += 25
        elif inp.manager_1on1_frequency_per_month     <= 3.0:  s += 10
        if   inp.call_shadowing_sessions_completed    <= 1:    s += 30
        elif inp.call_shadowing_sessions_completed    <= 3:    s += 15
        if   inp.peer_buddy_engagement_score          <= 0.20: s += 25
        elif inp.peer_buddy_engagement_score          <= 0.50: s += 12
        return min(s, 100.0)

    # ── composite ──────────────────────────────────────────────────────────────

    def _composite(self, re: float, ac: float, pi: float, ms: float) -> float:
        return min(round(re * 0.25 + ac * 0.30 + pi * 0.30 + ms * 0.15, 2), 100.0)

    # ── pattern ────────────────────────────────────────────────────────────────

    def _pattern(self, inp: RampInput) -> RampPattern:
        if inp.outbound_activity_vs_plan_pct <= 0.40 and inp.first_meeting_booked_days >= 21:
            return RampPattern.slow_starter
        if inp.product_certification_completion_pct <= 0.40 and inp.training_module_completion_pct <= 0.40:
            return RampPattern.knowledge_gap_blocker
        if inp.pipeline_coverage_ratio <= 1.0 and inp.quota_attainment_vs_ramp_plan_pct <= 0.40:
            return RampPattern.pipeline_builder_fail
        if inp.manager_1on1_frequency_per_month <= 1.0 and inp.call_shadowing_sessions_completed <= 2:
            return RampPattern.manager_orphan
        if inp.onboarding_satisfaction_score <= 0.35 and inp.net_promoter_internal_score <= 0.35:
            return RampPattern.confidence_collapse
        return RampPattern.none

    # ── thresholds ─────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> RampRisk:
        if   composite >= 60: return RampRisk.critical
        elif composite >= 40: return RampRisk.high
        elif composite >= 20: return RampRisk.moderate
        return RampRisk.low

    def _severity(self, composite: float) -> RampSeverity:
        if   composite >= 60: return RampSeverity.critical
        elif composite >= 40: return RampSeverity.behind
        elif composite >= 20: return RampSeverity.at_risk
        return RampSeverity.on_track

    def _action(self, risk: RampRisk, pattern: RampPattern) -> RampAction:
        if risk == RampRisk.critical:
            if pattern in (RampPattern.pipeline_builder_fail, RampPattern.slow_starter):
                return RampAction.ramp_extension_or_reset
            return RampAction.structured_ramp_acceleration
        if risk == RampRisk.high:
            if pattern == RampPattern.slow_starter:
                return RampAction.pipeline_building_coaching
            if pattern == RampPattern.knowledge_gap_blocker:
                return RampAction.product_knowledge_coaching
            if pattern == RampPattern.pipeline_builder_fail:
                return RampAction.pipeline_building_coaching
            if pattern == RampPattern.manager_orphan:
                return RampAction.manager_engagement_review
            if pattern == RampPattern.confidence_collapse:
                return RampAction.structured_ramp_acceleration
            return RampAction.pipeline_building_coaching
        if risk == RampRisk.moderate:
            return RampAction.ramp_check_in
        return RampAction.no_action

    # ── flags ──────────────────────────────────────────────────────────────────

    def _has_ramp_gap(self, inp: RampInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.quota_attainment_vs_ramp_plan_pct <= 0.60
            or inp.pipeline_coverage_ratio           <= 2.0
        )

    def _requires_intervention(self, inp: RampInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.outbound_activity_vs_plan_pct        <= 0.65
            or inp.product_certification_completion_pct <= 0.60
        )

    # ── revenue risk ───────────────────────────────────────────────────────────

    def _ramp_revenue_risk(self, inp: RampInput, composite: float) -> float:
        ramp_quota_usd = inp.avg_deal_value_usd * 4  # approximate 4-deal ramp target
        shortfall_rate = max(0.0, 1.0 - inp.quota_attainment_vs_ramp_plan_pct)
        return round(ramp_quota_usd * shortfall_rate * (composite / 100), 2)

    # ── signal ─────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        RampPattern.slow_starter:          "Slow starter",
        RampPattern.knowledge_gap_blocker: "Knowledge-gap blocker",
        RampPattern.pipeline_builder_fail: "Pipeline-builder fail",
        RampPattern.manager_orphan:        "Manager orphan",
        RampPattern.confidence_collapse:   "Confidence collapse",
    }

    def _signal(self, inp: RampInput, pattern: RampPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Ramp trajectory healthy — activity, pipeline coverage, "
                "and product readiness within plan benchmarks"
            )
        label     = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        att_pct   = round(inp.quota_attainment_vs_ramp_plan_pct * 100)
        act_pct   = round(inp.outbound_activity_vs_plan_pct * 100)
        cert_pct  = round(inp.product_certification_completion_pct * 100)
        comp_int  = round(composite)
        return (
            f"{label} — {att_pct}% ramp attainment — {act_pct}% activity vs plan — "
            f"{cert_pct}% certs complete — composite {comp_int}"
        )

    # ── public API ─────────────────────────────────────────────────────────────

    def assess(self, inp: RampInput) -> RampResult:
        re   = self._readiness_score(inp)
        ac   = self._activity_score(inp)
        pi   = self._pipeline_score(inp)
        ms   = self._manager_support_score(inp)
        comp = self._composite(re, ac, pi, ms)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = RampResult(
            rep_id                          = inp.rep_id,
            region                          = inp.region,
            ramp_risk                       = risk,
            ramp_pattern                    = pattern,
            ramp_severity                   = severity,
            recommended_action              = action,
            readiness_score                 = re,
            activity_score                  = ac,
            pipeline_score                  = pi,
            manager_support_score           = ms,
            ramp_composite                  = comp,
            has_ramp_gap                    = self._has_ramp_gap(inp, comp),
            requires_ramp_intervention      = self._requires_intervention(inp, comp),
            estimated_ramp_revenue_risk_usd = self._ramp_revenue_risk(inp, comp),
            ramp_signal                     = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[RampInput]) -> List[RampResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_ramp_composite": 0.0,
                "ramp_gap_count": 0,
                "intervention_count": 0,
                "avg_readiness_score": 0.0,
                "avg_activity_score": 0.0,
                "avg_pipeline_score": 0.0,
                "avg_manager_support_score": 0.0,
                "total_estimated_ramp_revenue_risk_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_re = total_ac = total_pi = total_ms = total_rv = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.ramp_risk.value]         = risk_counts.get(res.ramp_risk.value, 0) + 1
            pattern_counts[res.ramp_pattern.value]   = pattern_counts.get(res.ramp_pattern.value, 0) + 1
            severity_counts[res.ramp_severity.value] = severity_counts.get(res.ramp_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.ramp_composite
            total_re   += res.readiness_score
            total_ac   += res.activity_score
            total_pi   += res.pipeline_score
            total_ms   += res.manager_support_score
            total_rv   += res.estimated_ramp_revenue_risk_usd
            if res.has_ramp_gap:           gap_count          += 1
            if res.requires_ramp_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_ramp_composite":                       round(total_comp / n, 1),
            "ramp_gap_count":                           gap_count,
            "intervention_count":                       intervention_count,
            "avg_readiness_score":                      round(total_re / n, 1),
            "avg_activity_score":                       round(total_ac / n, 1),
            "avg_pipeline_score":                       round(total_pi / n, 1),
            "avg_manager_support_score":                round(total_ms / n, 1),
            "total_estimated_ramp_revenue_risk_usd":    round(total_rv, 2),
        }
