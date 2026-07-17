from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class EngagementRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class EngagementPattern(str, Enum):
    none                        = "none"
    buyer_ghosting_cycle        = "buyer_ghosting_cycle"
    single_contact_dependency   = "single_contact_dependency"
    response_lag_accumulation   = "response_lag_accumulation"
    momentum_reversal           = "momentum_reversal"
    executive_access_deficit    = "executive_access_deficit"


class EngagementSeverity(str, Enum):
    accelerating = "accelerating"
    engaged      = "engaged"
    slowing      = "slowing"
    stalled      = "stalled"


class EngagementAction(str, Enum):
    no_action                       = "no_action"
    re_engagement_sequence_coaching = "re_engagement_sequence_coaching"
    multithreading_coaching         = "multithreading_coaching"
    executive_outreach_coaching     = "executive_outreach_coaching"
    deal_velocity_coaching          = "deal_velocity_coaching"
    deal_rescue_intervention        = "deal_rescue_intervention"


@dataclass
class EngagementInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    avg_buyer_response_time_days: float
    response_time_trend_days: float
    ghosting_episodes_per_deal: float
    buyer_initiated_contact_pct: float
    stakeholder_breadth_avg: float
    executive_engagement_rate_pct: float
    meeting_acceptance_rate_pct: float
    content_open_rate_pct: float
    follow_up_required_before_response_pct: float
    multi_stakeholder_deals_pct: float
    engagement_drop_after_proposal_pct: float
    champion_response_time_days: float
    mutual_action_plan_completion_pct: float
    next_step_set_rate_pct: float
    deal_re_engaged_after_silence_pct: float
    avg_days_between_meaningful_touches: float
    late_stage_dark_period_pct: float
    total_active_deals: int
    avg_opportunity_value_usd: float


@dataclass
class EngagementResult:
    rep_id: str
    region: str
    engagement_risk: EngagementRisk
    engagement_pattern: EngagementPattern
    engagement_severity: EngagementSeverity
    recommended_action: EngagementAction
    velocity_score: float
    breadth_score: float
    responsiveness_score: float
    momentum_score: float
    engagement_composite: float
    has_engagement_gap: bool
    requires_engagement_coaching: bool
    estimated_pipeline_at_risk_usd: float
    engagement_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                         self.rep_id,
            "region":                         self.region,
            "engagement_risk":                self.engagement_risk.value,
            "engagement_pattern":             self.engagement_pattern.value,
            "engagement_severity":            self.engagement_severity.value,
            "recommended_action":             self.recommended_action.value,
            "velocity_score":                 self.velocity_score,
            "breadth_score":                  self.breadth_score,
            "responsiveness_score":           self.responsiveness_score,
            "momentum_score":                 self.momentum_score,
            "engagement_composite":           self.engagement_composite,
            "has_engagement_gap":             self.has_engagement_gap,
            "requires_engagement_coaching":   self.requires_engagement_coaching,
            "estimated_pipeline_at_risk_usd": self.estimated_pipeline_at_risk_usd,
            "engagement_signal":              self.engagement_signal,
        }


class SalesBuyerEngagementVelocityIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[EngagementResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _velocity_score(self, inp: EngagementInput) -> float:
        score = 0.0

        if inp.avg_buyer_response_time_days >= 5.0:
            score += 40.0
        elif inp.avg_buyer_response_time_days >= 3.0:
            score += 22.0
        elif inp.avg_buyer_response_time_days >= 1.5:
            score += 8.0

        if inp.avg_days_between_meaningful_touches >= 14.0:
            score += 35.0
        elif inp.avg_days_between_meaningful_touches >= 7.0:
            score += 18.0

        if inp.next_step_set_rate_pct <= 0.40:
            score += 25.0
        elif inp.next_step_set_rate_pct <= 0.65:
            score += 12.0

        return min(score, 100.0)

    def _breadth_score(self, inp: EngagementInput) -> float:
        score = 0.0

        if inp.stakeholder_breadth_avg <= 1.5:
            score += 40.0
        elif inp.stakeholder_breadth_avg <= 2.5:
            score += 22.0
        elif inp.stakeholder_breadth_avg <= 3.5:
            score += 8.0

        if inp.executive_engagement_rate_pct <= 0.20:
            score += 35.0
        elif inp.executive_engagement_rate_pct <= 0.40:
            score += 18.0

        if inp.multi_stakeholder_deals_pct <= 0.30:
            score += 25.0
        elif inp.multi_stakeholder_deals_pct <= 0.55:
            score += 12.0

        return min(score, 100.0)

    def _responsiveness_score(self, inp: EngagementInput) -> float:
        score = 0.0

        if inp.follow_up_required_before_response_pct >= 0.70:
            score += 40.0
        elif inp.follow_up_required_before_response_pct >= 0.45:
            score += 22.0
        elif inp.follow_up_required_before_response_pct >= 0.25:
            score += 8.0

        if inp.buyer_initiated_contact_pct <= 0.15:
            score += 35.0
        elif inp.buyer_initiated_contact_pct <= 0.30:
            score += 18.0

        if inp.content_open_rate_pct <= 0.25:
            score += 25.0
        elif inp.content_open_rate_pct <= 0.50:
            score += 12.0

        return min(score, 100.0)

    def _momentum_score(self, inp: EngagementInput) -> float:
        score = 0.0

        if inp.ghosting_episodes_per_deal >= 3.0:
            score += 45.0
        elif inp.ghosting_episodes_per_deal >= 1.5:
            score += 25.0
        elif inp.ghosting_episodes_per_deal >= 0.5:
            score += 10.0

        if inp.engagement_drop_after_proposal_pct >= 0.55:
            score += 30.0
        elif inp.engagement_drop_after_proposal_pct >= 0.30:
            score += 15.0

        if inp.late_stage_dark_period_pct >= 0.40:
            score += 25.0
        elif inp.late_stage_dark_period_pct >= 0.20:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: EngagementInput,
                          velocity: float, breadth: float,
                          responsiveness: float, momentum: float) -> EngagementPattern:
        # Executive access deficit: no senior stakeholders involved
        if inp.executive_engagement_rate_pct <= 0.15 and inp.stakeholder_breadth_avg <= 2.0:
            return EngagementPattern.executive_access_deficit

        # Buyer ghosting cycle: repeated disappearance across the funnel
        if inp.ghosting_episodes_per_deal >= 2.5 and inp.late_stage_dark_period_pct >= 0.35:
            return EngagementPattern.buyer_ghosting_cycle

        # Single contact dependency: relying on one person in the buying group
        if breadth >= 35 and inp.stakeholder_breadth_avg <= 2.0:
            return EngagementPattern.single_contact_dependency

        # Response lag accumulation: buyer takes longer and longer to respond
        if velocity >= 35 and inp.response_time_trend_days >= 1.5:
            return EngagementPattern.response_lag_accumulation

        # Momentum reversal: engagement drops sharply after proposal/demo
        if inp.engagement_drop_after_proposal_pct >= 0.45 and momentum >= 30:
            return EngagementPattern.momentum_reversal

        return EngagementPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> EngagementRisk:
        if composite >= 60:
            return EngagementRisk.critical
        if composite >= 40:
            return EngagementRisk.high
        if composite >= 20:
            return EngagementRisk.moderate
        return EngagementRisk.low

    def _severity(self, composite: float) -> EngagementSeverity:
        if composite >= 60:
            return EngagementSeverity.stalled
        if composite >= 40:
            return EngagementSeverity.slowing
        if composite >= 20:
            return EngagementSeverity.engaged
        return EngagementSeverity.accelerating

    def _action(self, risk: EngagementRisk, pattern: EngagementPattern) -> EngagementAction:
        if risk == EngagementRisk.critical:
            if pattern == EngagementPattern.buyer_ghosting_cycle:
                return EngagementAction.re_engagement_sequence_coaching
            if pattern == EngagementPattern.executive_access_deficit:
                return EngagementAction.executive_outreach_coaching
            return EngagementAction.deal_rescue_intervention
        if risk == EngagementRisk.high:
            if pattern == EngagementPattern.single_contact_dependency:
                return EngagementAction.multithreading_coaching
            if pattern == EngagementPattern.response_lag_accumulation:
                return EngagementAction.deal_velocity_coaching
            return EngagementAction.deal_velocity_coaching
        if risk == EngagementRisk.moderate:
            return EngagementAction.re_engagement_sequence_coaching
        return EngagementAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_engagement_gap(self, composite: float, inp: EngagementInput) -> bool:
        return (
            composite >= 40
            or inp.ghosting_episodes_per_deal >= 2.0
            or inp.executive_engagement_rate_pct <= 0.25
        )

    def _requires_engagement_coaching(self, composite: float, inp: EngagementInput) -> bool:
        return (
            composite >= 30
            or inp.avg_buyer_response_time_days >= 4.0
            or inp.next_step_set_rate_pct <= 0.55
        )

    # ------------------------------------------------------------------
    # Pipeline at risk estimate
    # ------------------------------------------------------------------

    def _estimated_pipeline_at_risk(self, inp: EngagementInput, composite: float) -> float:
        return round(
            inp.total_active_deals
            * inp.avg_opportunity_value_usd
            * inp.late_stage_dark_period_pct
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: EngagementInput,
                 pattern: EngagementPattern, composite: float) -> str:
        if pattern == EngagementPattern.none and composite < 20:
            return "Buyer engagement healthy — response velocity, stakeholder breadth, and deal momentum within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.avg_buyer_response_time_days:.1f}d avg buyer response time")
        parts.append(f"{inp.stakeholder_breadth_avg:.1f} avg stakeholders")
        parts.append(f"{inp.ghosting_episodes_per_deal:.1f} ghosting episodes/deal")
        label = pattern.value.replace("_", " ") if pattern != EngagementPattern.none else "Engagement risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: EngagementInput) -> EngagementResult:
        velocity        = round(self._velocity_score(inp), 1)
        breadth         = round(self._breadth_score(inp), 1)
        responsiveness  = round(self._responsiveness_score(inp), 1)
        momentum        = round(self._momentum_score(inp), 1)

        composite = round(
            velocity * 0.30 + breadth * 0.25 + responsiveness * 0.25 + momentum * 0.20, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, velocity, breadth, responsiveness, momentum)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_engagement_gap(composite, inp)
        coach  = self._requires_engagement_coaching(composite, inp)
        loss   = self._estimated_pipeline_at_risk(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = EngagementResult(
            rep_id=inp.rep_id,
            region=inp.region,
            engagement_risk=risk,
            engagement_pattern=pattern,
            engagement_severity=severity,
            recommended_action=action,
            velocity_score=velocity,
            breadth_score=breadth,
            responsiveness_score=responsiveness,
            momentum_score=momentum,
            engagement_composite=composite,
            has_engagement_gap=gap,
            requires_engagement_coaching=coach,
            estimated_pipeline_at_risk_usd=loss,
            engagement_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[EngagementInput]) -> list[EngagementResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_engagement_composite": 0.0,
                "engagement_gap_count": 0,
                "coaching_count": 0,
                "avg_velocity_score": 0.0,
                "avg_breadth_score": 0.0,
                "avg_responsiveness_score": 0.0,
                "avg_momentum_score": 0.0,
                "total_estimated_pipeline_at_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_vel = total_bre = total_res = total_mom = total_loss = 0.0

        for r in self._results:
            risk_counts[r.engagement_risk.value]         = risk_counts.get(r.engagement_risk.value, 0) + 1
            pattern_counts[r.engagement_pattern.value]   = pattern_counts.get(r.engagement_pattern.value, 0) + 1
            severity_counts[r.engagement_severity.value] = severity_counts.get(r.engagement_severity.value, 0) + 1
            action_counts[r.recommended_action.value]    = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.engagement_composite
            total_vel  += r.velocity_score
            total_bre  += r.breadth_score
            total_res  += r.responsiveness_score
            total_mom  += r.momentum_score
            total_loss += r.estimated_pipeline_at_risk_usd

        n = len(self._results)

        return {
            "total":                                       n,
            "risk_counts":                                 risk_counts,
            "pattern_counts":                              pattern_counts,
            "severity_counts":                             severity_counts,
            "action_counts":                               action_counts,
            "avg_engagement_composite":                    round(total_comp / n, 1),
            "engagement_gap_count":                        sum(1 for r in self._results if r.has_engagement_gap),
            "coaching_count":                              sum(1 for r in self._results if r.requires_engagement_coaching),
            "avg_velocity_score":                          round(total_vel / n, 1),
            "avg_breadth_score":                           round(total_bre / n, 1),
            "avg_responsiveness_score":                    round(total_res / n, 1),
            "avg_momentum_score":                          round(total_mom / n, 1),
            "total_estimated_pipeline_at_risk_usd":        round(total_loss, 2),
        }
