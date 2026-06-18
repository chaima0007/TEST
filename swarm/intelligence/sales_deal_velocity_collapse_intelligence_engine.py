from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class VelocityRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class VelocityPattern(str, Enum):
    none               = "none"
    stalled_pipeline   = "stalled_pipeline"
    stage_regression   = "stage_regression"
    ghost_deal         = "ghost_deal"
    champion_gone_dark = "champion_gone_dark"
    multistage_drag    = "multistage_drag"


class VelocitySeverity(str, Enum):
    accelerating = "accelerating"
    on_track     = "on_track"
    slowing      = "slowing"
    collapsed    = "collapsed"


class VelocityAction(str, Enum):
    no_action                   = "no_action"
    velocity_monitoring         = "velocity_monitoring"
    deal_acceleration_coaching  = "deal_acceleration_coaching"
    champion_reactivation       = "champion_reactivation"
    executive_involvement       = "executive_involvement"
    pipeline_triage             = "pipeline_triage"
    deal_rescue_escalation      = "deal_rescue_escalation"


@dataclass
class VelocityInput:
    rep_id:                          str
    region:                          str
    evaluation_period_id:            str
    avg_days_in_current_stage:       float   # days stuck in current stage
    avg_cycle_length_days:           float   # typical full cycle days
    cycle_length_vs_benchmark_pct:   float   # positive = slower than benchmark
    stage_regression_count:          int     # times deal moved backward
    no_activity_streak_days:         int     # days since last meaningful activity
    champion_response_time_days:     float   # avg days to get champion response
    executive_sponsor_days_since_contact: float  # days since exec sponsor touched
    next_step_defined_rate_pct:      float   # 0-1 (deals with clear next step)
    mutual_action_plan_completion_pct: float # 0-1
    close_date_slip_count:           int     # how many times close date pushed
    close_date_slip_days_avg:        float   # avg days pushed
    proposal_sent_to_response_days:  float   # avg days after proposal
    poc_to_commercial_days:          float   # days from PoC to commercial conversation
    avg_stakeholder_response_rate_pct: float # 0-1
    multi_threaded_deal_rate_pct:    float   # 0-1 (% deals with >1 contact engaged)
    competitive_re_eval_trigger_pct: float   # 0-1 (deals reopened for competitor eval)
    late_stage_stall_rate_pct:       float   # 0-1 (% deals stalling in final stage)
    total_active_deals:              int
    avg_deal_value_usd:              float


@dataclass
class VelocityResult:
    rep_id:                         str
    region:                         str
    velocity_risk:                  VelocityRisk
    velocity_pattern:               VelocityPattern
    velocity_severity:              VelocitySeverity
    recommended_action:             VelocityAction
    stage_stall_score:              float
    engagement_decay_score:         float
    deal_hygiene_score:             float
    pipeline_risk_score:            float
    velocity_composite:             float
    has_velocity_gap:               bool
    requires_velocity_intervention: bool
    estimated_at_risk_pipeline_usd: float
    velocity_signal:                str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "velocity_risk":                    self.velocity_risk.value,
            "velocity_pattern":                 self.velocity_pattern.value,
            "velocity_severity":                self.velocity_severity.value,
            "recommended_action":               self.recommended_action.value,
            "stage_stall_score":                self.stage_stall_score,
            "engagement_decay_score":           self.engagement_decay_score,
            "deal_hygiene_score":               self.deal_hygiene_score,
            "pipeline_risk_score":              self.pipeline_risk_score,
            "velocity_composite":               self.velocity_composite,
            "has_velocity_gap":                 self.has_velocity_gap,
            "requires_velocity_intervention":   self.requires_velocity_intervention,
            "estimated_at_risk_pipeline_usd":   self.estimated_at_risk_pipeline_usd,
            "velocity_signal":                  self.velocity_signal,
        }


class SalesDealVelocityCollapseIntelligenceEngine:
    """Detects deal cycle expansion and velocity collapse — catches stuck deals before they ghost."""

    def __init__(self) -> None:
        self._results: List[VelocityResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _stage_stall_score(self, inp: VelocityInput) -> float:
        s = 0.0
        if   inp.avg_days_in_current_stage      >= 30: s += 40
        elif inp.avg_days_in_current_stage      >= 18: s += 22
        elif inp.avg_days_in_current_stage      >= 10: s += 8
        if   inp.cycle_length_vs_benchmark_pct  >= 0.50: s += 35
        elif inp.cycle_length_vs_benchmark_pct  >= 0.25: s += 18
        elif inp.cycle_length_vs_benchmark_pct  >= 0.10: s += 6
        if   inp.stage_regression_count         >= 3: s += 25
        elif inp.stage_regression_count         >= 2: s += 12
        return min(s, 100.0)

    def _engagement_decay_score(self, inp: VelocityInput) -> float:
        s = 0.0
        if   inp.no_activity_streak_days                  >= 14: s += 40
        elif inp.no_activity_streak_days                  >= 7:  s += 22
        elif inp.no_activity_streak_days                  >= 3:  s += 8
        if   inp.champion_response_time_days              >= 10: s += 35
        elif inp.champion_response_time_days              >= 5:  s += 18
        if   inp.avg_stakeholder_response_rate_pct        <= 0.25: s += 25
        elif inp.avg_stakeholder_response_rate_pct        <= 0.50: s += 12
        return min(s, 100.0)

    def _deal_hygiene_score(self, inp: VelocityInput) -> float:
        s = 0.0
        if   inp.next_step_defined_rate_pct      <= 0.30: s += 40
        elif inp.next_step_defined_rate_pct      <= 0.55: s += 22
        elif inp.next_step_defined_rate_pct      <= 0.75: s += 8
        if   inp.mutual_action_plan_completion_pct <= 0.25: s += 35
        elif inp.mutual_action_plan_completion_pct <= 0.50: s += 18
        if   inp.close_date_slip_count            >= 3: s += 25
        elif inp.close_date_slip_count            >= 2: s += 12
        return min(s, 100.0)

    def _pipeline_risk_score(self, inp: VelocityInput) -> float:
        s = 0.0
        if   inp.late_stage_stall_rate_pct       >= 0.45: s += 45
        elif inp.late_stage_stall_rate_pct       >= 0.25: s += 25
        elif inp.late_stage_stall_rate_pct       >= 0.12: s += 10
        if   inp.competitive_re_eval_trigger_pct >= 0.35: s += 30
        elif inp.competitive_re_eval_trigger_pct >= 0.20: s += 15
        if   inp.multi_threaded_deal_rate_pct    <= 0.25: s += 25
        elif inp.multi_threaded_deal_rate_pct    <= 0.50: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────────

    def _composite(self, st: float, eng: float, hy: float, pip: float) -> float:
        return min(round(st * 0.30 + eng * 0.30 + hy * 0.25 + pip * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, inp: VelocityInput) -> VelocityPattern:
        if inp.no_activity_streak_days >= 10 and inp.avg_days_in_current_stage >= 20:
            return VelocityPattern.stalled_pipeline
        if inp.stage_regression_count >= 2 and inp.close_date_slip_count >= 2:
            return VelocityPattern.stage_regression
        if inp.no_activity_streak_days >= 14 and inp.champion_response_time_days >= 8:
            return VelocityPattern.ghost_deal
        if inp.champion_response_time_days >= 7 and inp.executive_sponsor_days_since_contact >= 30:
            return VelocityPattern.champion_gone_dark
        if inp.avg_cycle_length_days >= 120 and inp.late_stage_stall_rate_pct >= 0.30:
            return VelocityPattern.multistage_drag
        return VelocityPattern.none

    # ── thresholds ────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> VelocityRisk:
        if   composite >= 60: return VelocityRisk.critical
        elif composite >= 40: return VelocityRisk.high
        elif composite >= 20: return VelocityRisk.moderate
        return VelocityRisk.low

    def _severity(self, composite: float) -> VelocitySeverity:
        if   composite >= 60: return VelocitySeverity.collapsed
        elif composite >= 40: return VelocitySeverity.slowing
        elif composite >= 20: return VelocitySeverity.on_track
        return VelocitySeverity.accelerating

    def _action(self, risk: VelocityRisk, pattern: VelocityPattern) -> VelocityAction:
        if risk == VelocityRisk.critical:
            if pattern in (VelocityPattern.ghost_deal, VelocityPattern.champion_gone_dark):
                return VelocityAction.deal_rescue_escalation
            return VelocityAction.pipeline_triage
        if risk == VelocityRisk.high:
            if pattern == VelocityPattern.stalled_pipeline:
                return VelocityAction.deal_acceleration_coaching
            if pattern == VelocityPattern.stage_regression:
                return VelocityAction.deal_acceleration_coaching
            if pattern == VelocityPattern.ghost_deal:
                return VelocityAction.champion_reactivation
            if pattern == VelocityPattern.champion_gone_dark:
                return VelocityAction.executive_involvement
            if pattern == VelocityPattern.multistage_drag:
                return VelocityAction.executive_involvement
            return VelocityAction.deal_acceleration_coaching
        if risk == VelocityRisk.moderate:
            return VelocityAction.velocity_monitoring
        return VelocityAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: VelocityInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.close_date_slip_count >= 2
            or inp.no_activity_streak_days >= 10
        )

    def _requires_intervention(self, inp: VelocityInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.late_stage_stall_rate_pct >= 0.30
            or inp.stage_regression_count >= 2
        )

    # ── pipeline at risk ──────────────────────────────────────────────────────

    def _at_risk_pipeline(self, inp: VelocityInput, composite: float) -> float:
        stall_rate = inp.late_stage_stall_rate_pct + (inp.close_date_slip_count / 10)
        return round(inp.total_active_deals * inp.avg_deal_value_usd * min(stall_rate, 1.0) * (composite / 100), 2)

    # ── signal ────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        VelocityPattern.stalled_pipeline:   "Stalled pipeline",
        VelocityPattern.stage_regression:   "Stage regression",
        VelocityPattern.ghost_deal:         "Ghost deal",
        VelocityPattern.champion_gone_dark: "Champion gone dark",
        VelocityPattern.multistage_drag:    "Multistage drag",
    }

    def _signal(self, inp: VelocityInput, pattern: VelocityPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Deal velocity healthy — stage progression, engagement cadence, "
                "and pipeline hygiene within benchmarks"
            )
        label         = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        stall_days    = round(inp.avg_days_in_current_stage)
        no_act_days   = inp.no_activity_streak_days
        slip_count    = inp.close_date_slip_count
        comp_int      = round(composite)
        return (
            f"{label} — {stall_days}d in current stage — "
            f"{no_act_days}d no activity — "
            f"{slip_count} close-date slips — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, inp: VelocityInput) -> VelocityResult:
        st   = self._stage_stall_score(inp)
        eng  = self._engagement_decay_score(inp)
        hy   = self._deal_hygiene_score(inp)
        pip  = self._pipeline_risk_score(inp)
        comp = self._composite(st, eng, hy, pip)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = VelocityResult(
            rep_id                          = inp.rep_id,
            region                          = inp.region,
            velocity_risk                   = risk,
            velocity_pattern                = pattern,
            velocity_severity               = severity,
            recommended_action              = action,
            stage_stall_score               = st,
            engagement_decay_score          = eng,
            deal_hygiene_score              = hy,
            pipeline_risk_score             = pip,
            velocity_composite              = comp,
            has_velocity_gap                = self._has_gap(inp, comp),
            requires_velocity_intervention  = self._requires_intervention(inp, comp),
            estimated_at_risk_pipeline_usd  = self._at_risk_pipeline(inp, comp),
            velocity_signal                 = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[VelocityInput]) -> List[VelocityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_velocity_composite": 0.0,
                "velocity_gap_count": 0,
                "intervention_count": 0,
                "avg_stage_stall_score": 0.0,
                "avg_engagement_decay_score": 0.0,
                "avg_deal_hygiene_score": 0.0,
                "avg_pipeline_risk_score": 0.0,
                "total_estimated_at_risk_pipeline_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_st = total_eng = total_hy = total_pip = total_ar = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.velocity_risk.value]         = risk_counts.get(res.velocity_risk.value, 0) + 1
            pattern_counts[res.velocity_pattern.value]   = pattern_counts.get(res.velocity_pattern.value, 0) + 1
            severity_counts[res.velocity_severity.value] = severity_counts.get(res.velocity_severity.value, 0) + 1
            action_counts[res.recommended_action.value]  = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.velocity_composite
            total_st   += res.stage_stall_score
            total_eng  += res.engagement_decay_score
            total_hy   += res.deal_hygiene_score
            total_pip  += res.pipeline_risk_score
            total_ar   += res.estimated_at_risk_pipeline_usd
            if res.has_velocity_gap:               gap_count          += 1
            if res.requires_velocity_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_velocity_composite":               round(total_comp / n, 1),
            "velocity_gap_count":                   gap_count,
            "intervention_count":                   intervention_count,
            "avg_stage_stall_score":                round(total_st / n, 1),
            "avg_engagement_decay_score":           round(total_eng / n, 1),
            "avg_deal_hygiene_score":               round(total_hy / n, 1),
            "avg_pipeline_risk_score":              round(total_pip / n, 1),
            "total_estimated_at_risk_pipeline_usd": round(total_ar, 2),
        }
