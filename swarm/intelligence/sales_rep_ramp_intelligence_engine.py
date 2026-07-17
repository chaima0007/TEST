from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict


class RampRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class RampPattern(str, Enum):
    none                = "none"
    slow_activator      = "slow_activator"
    quota_plateau       = "quota_plateau"
    pipeline_builder_gap = "pipeline_builder_gap"
    knowledge_laggard   = "knowledge_laggard"
    coaching_resistant  = "coaching_resistant"


class RampSeverity(str, Enum):
    on_track   = "on_track"
    watch      = "watch"
    at_risk    = "at_risk"
    stalled    = "stalled"


class RampAction(str, Enum):
    no_action                      = "no_action"
    accelerated_onboarding         = "accelerated_onboarding"
    pipeline_building_coaching     = "pipeline_building_coaching"
    product_knowledge_coaching     = "product_knowledge_coaching"
    quota_expectation_reset        = "quota_expectation_reset"
    manager_escalation             = "manager_escalation"
    ramp_extension_review          = "ramp_extension_review"


@dataclass
class RampInput:
    rep_id:                          str
    region:                          str
    evaluation_period_id:            str
    months_in_role:                  int      # 1–24
    ramp_period_months:              int      # agreed ramp period (typ 3–9)
    quota_attainment_pct:            float    # % of quota attained so far (0–1+)
    pipeline_coverage_ratio:         float    # pipe / quota
    first_deal_days:                 int      # days until first deal closed
    certification_completion_pct:    float    # % of onboarding certs done (0–1)
    manager_check_in_per_month:      int      # coaching sessions per month
    peer_shadowing_calls:            int      # number of shadow calls done
    crm_data_quality_score:          float    # 0–10
    call_volume_vs_target_pct:       float    # actual / target call volume (0–1+)
    avg_deal_size_vs_team_pct:       float    # new rep deal size / team avg (0–1+)
    lost_deal_pct:                   float    # % of closed deals lost (0–1)
    product_quiz_score:              float    # knowledge assessment 0–100
    days_to_first_meeting:           int
    avg_time_to_close_days:          int      # new rep avg vs target
    target_time_to_close_days:       int
    total_expected_quota_usd:        float
    avg_opportunity_value_usd:       float
    pipeline_deal_count:             int


@dataclass
class RampResult:
    rep_id:                     str
    region:                     str
    ramp_risk:                  RampRisk
    ramp_pattern:               RampPattern
    ramp_severity:              RampSeverity
    recommended_action:         RampAction
    activation_score:           float
    pipeline_health_score:      float
    knowledge_score:            float
    productivity_score:         float
    ramp_composite:             float
    has_ramp_gap:               bool
    requires_ramp_coaching:     bool
    estimated_ramp_cost_usd:    float
    ramp_signal:                str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                     self.rep_id,
            "region":                     self.region,
            "ramp_risk":                  self.ramp_risk.value,
            "ramp_pattern":               self.ramp_pattern.value,
            "ramp_severity":              self.ramp_severity.value,
            "recommended_action":         self.recommended_action.value,
            "activation_score":           self.activation_score,
            "pipeline_health_score":      self.pipeline_health_score,
            "knowledge_score":            self.knowledge_score,
            "productivity_score":         self.productivity_score,
            "ramp_composite":             self.ramp_composite,
            "has_ramp_gap":               self.has_ramp_gap,
            "requires_ramp_coaching":     self.requires_ramp_coaching,
            "estimated_ramp_cost_usd":    self.estimated_ramp_cost_usd,
            "ramp_signal":                self.ramp_signal,
        }


class SalesRepRampIntelligenceEngine:

    def __init__(self) -> None:
        self._results: List[RampResult] = []

    def _activation_score(self, inp: RampInput) -> float:
        s = 0.0
        # quota attainment vs expected for months in role
        expected_attain = min(1.0, inp.months_in_role / inp.ramp_period_months)
        gap = expected_attain - inp.quota_attainment_pct
        if gap >= 0.50:
            s += 45
        elif gap >= 0.30:
            s += 28
        elif gap >= 0.15:
            s += 12
        # first deal
        if inp.first_deal_days > inp.ramp_period_months * 30:
            s += 35
        elif inp.first_deal_days > inp.ramp_period_months * 20:
            s += 18
        elif inp.first_deal_days > inp.ramp_period_months * 12:
            s += 6
        # deal size vs team
        if inp.avg_deal_size_vs_team_pct < 0.60:
            s += 20
        elif inp.avg_deal_size_vs_team_pct < 0.80:
            s += 10
        return min(s, 100.0)

    def _pipeline_health_score(self, inp: RampInput) -> float:
        s = 0.0
        if inp.pipeline_coverage_ratio < 1.0:
            s += 45
        elif inp.pipeline_coverage_ratio < 2.0:
            s += 25
        elif inp.pipeline_coverage_ratio < 3.0:
            s += 8
        if inp.call_volume_vs_target_pct < 0.60:
            s += 35
        elif inp.call_volume_vs_target_pct < 0.80:
            s += 18
        elif inp.call_volume_vs_target_pct < 0.90:
            s += 6
        if inp.lost_deal_pct > 0.70:
            s += 20
        elif inp.lost_deal_pct > 0.55:
            s += 10
        return min(s, 100.0)

    def _knowledge_score(self, inp: RampInput) -> float:
        s = 0.0
        if inp.certification_completion_pct < 0.50:
            s += 40
        elif inp.certification_completion_pct < 0.75:
            s += 22
        elif inp.certification_completion_pct < 0.90:
            s += 8
        if inp.product_quiz_score < 60:
            s += 35
        elif inp.product_quiz_score < 75:
            s += 18
        elif inp.product_quiz_score < 85:
            s += 6
        if inp.peer_shadowing_calls < 3:
            s += 25
        elif inp.peer_shadowing_calls < 6:
            s += 12
        return min(s, 100.0)

    def _productivity_score(self, inp: RampInput) -> float:
        s = 0.0
        cycle_ratio = inp.avg_time_to_close_days / max(1, inp.target_time_to_close_days)
        if cycle_ratio > 1.50:
            s += 40
        elif cycle_ratio > 1.25:
            s += 22
        elif cycle_ratio > 1.10:
            s += 8
        if inp.crm_data_quality_score < 5:
            s += 35
        elif inp.crm_data_quality_score < 7:
            s += 18
        elif inp.crm_data_quality_score < 8.5:
            s += 6
        if inp.manager_check_in_per_month < 2:
            s += 25
        elif inp.manager_check_in_per_month < 4:
            s += 12
        return min(s, 100.0)

    def _composite(self, a: float, p: float, k: float, pr: float) -> float:
        return round(a * 0.35 + p * 0.30 + k * 0.20 + pr * 0.15, 2)

    def _pattern(self, inp: RampInput) -> RampPattern:
        expected = min(1.0, inp.months_in_role / inp.ramp_period_months)
        if inp.quota_attainment_pct < expected * 0.50 and inp.first_deal_days > inp.ramp_period_months * 25:
            return RampPattern.slow_activator
        if inp.months_in_role > inp.ramp_period_months and inp.quota_attainment_pct < 0.70:
            return RampPattern.quota_plateau
        if inp.pipeline_coverage_ratio < 1.5 and inp.call_volume_vs_target_pct < 0.70:
            return RampPattern.pipeline_builder_gap
        if inp.product_quiz_score < 65 and inp.certification_completion_pct < 0.60:
            return RampPattern.knowledge_laggard
        if inp.manager_check_in_per_month < 2 and inp.peer_shadowing_calls < 3:
            return RampPattern.coaching_resistant
        return RampPattern.none

    def _risk(self, composite: float) -> RampRisk:
        if composite >= 60: return RampRisk.critical
        if composite >= 40: return RampRisk.high
        if composite >= 20: return RampRisk.moderate
        return RampRisk.low

    def _severity(self, composite: float) -> RampSeverity:
        if composite >= 60: return RampSeverity.stalled
        if composite >= 40: return RampSeverity.at_risk
        if composite >= 20: return RampSeverity.watch
        return RampSeverity.on_track

    def _action(self, risk: RampRisk, pattern: RampPattern) -> RampAction:
        if risk == RampRisk.critical:
            if pattern == RampPattern.quota_plateau:
                return RampAction.quota_expectation_reset
            return RampAction.ramp_extension_review
        if risk == RampRisk.high:
            if pattern == RampPattern.slow_activator:
                return RampAction.manager_escalation
            if pattern == RampPattern.pipeline_builder_gap:
                return RampAction.pipeline_building_coaching
            if pattern == RampPattern.knowledge_laggard:
                return RampAction.product_knowledge_coaching
            if pattern == RampPattern.coaching_resistant:
                return RampAction.manager_escalation
            return RampAction.accelerated_onboarding
        if risk == RampRisk.moderate:
            return RampAction.accelerated_onboarding
        return RampAction.no_action

    def _has_gap(self, inp: RampInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.quota_attainment_pct < 0.50
            or inp.pipeline_coverage_ratio < 2.0
        )

    def _requires_coaching(self, inp: RampInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.certification_completion_pct < 0.80
            or inp.manager_check_in_per_month < 3
        )

    def _ramp_cost(self, inp: RampInput, composite: float) -> float:
        expected = min(1.0, inp.months_in_role / inp.ramp_period_months)
        shortfall = max(0.0, expected - inp.quota_attainment_pct)
        return round(inp.total_expected_quota_usd * shortfall * (composite / 100.0), 2)

    def _signal(self, inp: RampInput, pattern: RampPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Rep ramp on track — quota activation, pipeline build, "
                "and knowledge acquisition within benchmarks"
            )
        labels = {
            RampPattern.slow_activator:       "Slow activator",
            RampPattern.quota_plateau:        "Quota plateau",
            RampPattern.pipeline_builder_gap: "Pipeline builder gap",
            RampPattern.knowledge_laggard:    "Knowledge laggard",
            RampPattern.coaching_resistant:   "Coaching resistant",
        }
        label    = labels.get(pattern, "Ramp gap detected")
        attain   = round(inp.quota_attainment_pct * 100)
        pipe     = round(inp.pipeline_coverage_ratio, 1)
        cert     = round(inp.certification_completion_pct * 100)
        comp_int = round(composite)
        return (
            f"{label} — {attain}% quota attained — "
            f"{pipe}x pipeline coverage — "
            f"{cert}% certs complete — composite {comp_int}"
        )

    def assess(self, inp: RampInput) -> RampResult:
        a  = self._activation_score(inp)
        p  = self._pipeline_health_score(inp)
        k  = self._knowledge_score(inp)
        pr = self._productivity_score(inp)
        comp    = self._composite(a, p, k, pr)
        pattern = self._pattern(inp)
        risk    = self._risk(comp)
        sev     = self._severity(comp)
        action  = self._action(risk, pattern)
        result  = RampResult(
            rep_id               = inp.rep_id,
            region               = inp.region,
            ramp_risk            = risk,
            ramp_pattern         = pattern,
            ramp_severity        = sev,
            recommended_action   = action,
            activation_score     = round(a, 2),
            pipeline_health_score= round(p, 2),
            knowledge_score      = round(k, 2),
            productivity_score   = round(pr, 2),
            ramp_composite       = comp,
            has_ramp_gap         = self._has_gap(inp, comp),
            requires_ramp_coaching = self._requires_coaching(inp, comp),
            estimated_ramp_cost_usd = self._ramp_cost(inp, comp),
            ramp_signal          = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[RampInput]) -> List[RampResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        rr = self._results
        if not rr:
            return {
                "total": 0, "risk_counts": {}, "pattern_counts": {},
                "severity_counts": {}, "action_counts": {},
                "avg_ramp_composite": 0.0, "ramp_gap_count": 0,
                "coaching_count": 0, "avg_activation_score": 0.0,
                "avg_pipeline_health_score": 0.0, "avg_knowledge_score": 0.0,
                "avg_productivity_score": 0.0,
                "total_estimated_ramp_cost_usd": 0.0,
            }
        n = len(rr)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        ta = tp = tk = tpr = trev = 0.0
        gc = cc = 0
        for r in rr:
            rc[r.ramp_risk.value]          = rc.get(r.ramp_risk.value, 0) + 1
            pc[r.ramp_pattern.value]       = pc.get(r.ramp_pattern.value, 0) + 1
            sc[r.ramp_severity.value]      = sc.get(r.ramp_severity.value, 0) + 1
            ac[r.recommended_action.value] = ac.get(r.recommended_action.value, 0) + 1
            ta   += r.activation_score
            tp   += r.pipeline_health_score
            tk   += r.knowledge_score
            tpr  += r.productivity_score
            trev += r.estimated_ramp_cost_usd
            gc   += r.has_ramp_gap
            cc   += r.requires_ramp_coaching
        return {
            "total":                           n,
            "risk_counts":                     rc,
            "pattern_counts":                  pc,
            "severity_counts":                 sc,
            "action_counts":                   ac,
            "avg_ramp_composite":              round(sum(r.ramp_composite for r in rr) / n, 1),
            "ramp_gap_count":                  gc,
            "coaching_count":                  cc,
            "avg_activation_score":            round(ta / n, 1),
            "avg_pipeline_health_score":       round(tp / n, 1),
            "avg_knowledge_score":             round(tk / n, 1),
            "avg_productivity_score":          round(tpr / n, 1),
            "total_estimated_ramp_cost_usd":   round(trev, 2),
        }
