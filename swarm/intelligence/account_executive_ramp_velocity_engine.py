"""Account Executive Ramp Velocity Engine — measures new AE productivity ramp
speed and identifies which new hires are under-ramping, enabling early coaching
interventions before they miss their first full quota period and churn."""

from __future__ import annotations

import dataclasses
from enum import Enum


class RampRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class RampBlocker(str, Enum):
    none                  = "none"
    pipeline_deficit      = "pipeline_deficit"
    slow_conversion       = "slow_conversion"
    knowledge_gap         = "knowledge_gap"
    activity_shortfall    = "activity_shortfall"
    coaching_gap          = "coaching_gap"


class RampSeverity(str, Enum):
    on_track    = "on_track"
    behind      = "behind"
    at_risk     = "at_risk"
    failing     = "failing"


class RampAction(str, Enum):
    no_action           = "no_action"
    targeted_coaching   = "targeted_coaching"
    ramp_plan_adjustment = "ramp_plan_adjustment"
    pip_initiation      = "pip_initiation"
    separation_review   = "separation_review"


@dataclasses.dataclass
class AERampVelocityInput:
    rep_id:                            str
    region:                            str
    evaluation_period_id:              str
    tenure_days:                       int
    first_deal_closed_days:            int
    deals_closed_count:                int
    pipeline_created_usd:              float
    pipeline_target_usd:               float
    avg_deal_cycle_days:               float
    benchmark_avg_deal_cycle_days:     float
    quota_attainment_pct:              float
    ramp_quota_target_pct:             float
    training_completion_pct:           float
    manager_coaching_sessions_completed: int
    peer_collaboration_score:          float
    crm_data_quality_score:            float
    discovery_call_completion_rate:    float
    demo_to_proposal_conversion_rate:  float
    benchmark_demo_to_proposal_rate:   float
    product_certification_completed:   int
    expected_deals_at_this_tenure:     int
    first_90_day_pipeline_coverage:    float


@dataclasses.dataclass
class AERampVelocityResult:
    rep_id:                            str
    region:                            str
    ramp_risk:                         RampRisk
    ramp_blocker:                      RampBlocker
    ramp_severity:                     RampSeverity
    recommended_action:                RampAction
    pipeline_gap_score:                float
    conversion_velocity_score:         float
    knowledge_readiness_score:         float
    activity_quality_score:            float
    ramp_composite:                    float
    is_under_ramping:                  bool
    requires_intervention:             bool
    estimated_quota_attainment_pct:    float
    ramp_signal:                       str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "ramp_risk":                        self.ramp_risk.value,
            "ramp_blocker":                     self.ramp_blocker.value,
            "ramp_severity":                    self.ramp_severity.value,
            "recommended_action":               self.recommended_action.value,
            "pipeline_gap_score":               round(self.pipeline_gap_score, 1),
            "conversion_velocity_score":        round(self.conversion_velocity_score, 1),
            "knowledge_readiness_score":        round(self.knowledge_readiness_score, 1),
            "activity_quality_score":           round(self.activity_quality_score, 1),
            "ramp_composite":                   round(self.ramp_composite, 1),
            "is_under_ramping":                 self.is_under_ramping,
            "requires_intervention":            self.requires_intervention,
            "estimated_quota_attainment_pct":   round(self.estimated_quota_attainment_pct, 1),
            "ramp_signal":                      self.ramp_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class AccountExecutiveRampVelocityEngine:
    """Identifies under-ramping AEs early to enable coaching before first quota period."""

    def __init__(self) -> None:
        self._results: list[AERampVelocityResult] = []

    # ── sub-scores (HIGHER = worse ramp performance) ─────────────────────────

    def _pipeline_gap_score(self, inp: AERampVelocityInput) -> float:
        score = 0.0
        # Pipeline vs target
        if inp.pipeline_target_usd > 0:
            coverage = inp.pipeline_created_usd / inp.pipeline_target_usd
            if coverage < 0.3:
                score += 50.0
            elif coverage < 0.5:
                score += 35.0
            elif coverage < 0.7:
                score += 20.0
            elif coverage < 0.85:
                score += 8.0
        # First 90-day pipeline coverage
        if inp.first_90_day_pipeline_coverage < 1.5:
            score += 30.0
        elif inp.first_90_day_pipeline_coverage < 2.5:
            score += 15.0
        elif inp.first_90_day_pipeline_coverage < 3.0:
            score += 5.0
        # Deals vs expected for tenure
        if inp.expected_deals_at_this_tenure > 0:
            deal_ratio = inp.deals_closed_count / inp.expected_deals_at_this_tenure
            if deal_ratio < 0.2:
                score += 20.0
            elif deal_ratio < 0.5:
                score += 10.0
            elif deal_ratio < 0.75:
                score += 5.0
        return _clamp(score)

    def _conversion_velocity_score(self, inp: AERampVelocityInput) -> float:
        score = 0.0
        # Demo-to-proposal conversion vs benchmark
        if inp.benchmark_demo_to_proposal_rate > 0:
            conv_gap = inp.benchmark_demo_to_proposal_rate - inp.demo_to_proposal_conversion_rate
            if conv_gap >= 0.4:
                score += 40.0
            elif conv_gap >= 0.25:
                score += 25.0
            elif conv_gap >= 0.15:
                score += 12.0
        # Deal cycle length vs benchmark
        if inp.benchmark_avg_deal_cycle_days > 0:
            cycle_ratio = inp.avg_deal_cycle_days / inp.benchmark_avg_deal_cycle_days
            if cycle_ratio >= 2.0:
                score += 30.0
            elif cycle_ratio >= 1.5:
                score += 18.0
            elif cycle_ratio >= 1.25:
                score += 8.0
        # First deal closed timeline
        if inp.tenure_days >= 90 and inp.first_deal_closed_days == 0:
            score += 30.0
        elif inp.first_deal_closed_days >= 120:
            score += 20.0
        elif inp.first_deal_closed_days >= 90:
            score += 10.0
        return _clamp(score)

    def _knowledge_readiness_score(self, inp: AERampVelocityInput) -> float:
        score = 0.0
        # Training completion
        if inp.training_completion_pct < 40:
            score += 40.0
        elif inp.training_completion_pct < 60:
            score += 25.0
        elif inp.training_completion_pct < 80:
            score += 12.0
        # Product certification
        if inp.tenure_days >= 60 and inp.product_certification_completed == 0:
            score += 30.0
        # CRM data quality (proxy for process knowledge)
        if inp.crm_data_quality_score < 40:
            score += 20.0
        elif inp.crm_data_quality_score < 60:
            score += 10.0
        elif inp.crm_data_quality_score < 75:
            score += 5.0
        # Coaching sessions completed
        if inp.tenure_days >= 30 and inp.manager_coaching_sessions_completed == 0:
            score += 10.0
        elif inp.manager_coaching_sessions_completed <= 1 and inp.tenure_days >= 60:
            score += 5.0
        return _clamp(score)

    def _activity_quality_score(self, inp: AERampVelocityInput) -> float:
        score = 0.0
        # Discovery call completion (quality prospecting)
        if inp.discovery_call_completion_rate < 0.20:
            score += 40.0
        elif inp.discovery_call_completion_rate < 0.35:
            score += 25.0
        elif inp.discovery_call_completion_rate < 0.50:
            score += 12.0
        # Quota attainment vs ramp target
        attainment_vs_target = inp.quota_attainment_pct - inp.ramp_quota_target_pct
        if attainment_vs_target <= -50:
            score += 40.0
        elif attainment_vs_target <= -30:
            score += 25.0
        elif attainment_vs_target <= -15:
            score += 12.0
        # Low peer collaboration (not leveraging team)
        if inp.peer_collaboration_score < 30:
            score += 20.0
        elif inp.peer_collaboration_score < 50:
            score += 10.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> RampRisk:
        if composite < 20:
            return RampRisk.low
        if composite < 40:
            return RampRisk.moderate
        if composite < 60:
            return RampRisk.high
        return RampRisk.critical

    def _classify_severity(self, composite: float) -> RampSeverity:
        if composite < 20:
            return RampSeverity.on_track
        if composite < 40:
            return RampSeverity.behind
        if composite < 60:
            return RampSeverity.at_risk
        return RampSeverity.failing

    def _classify_blocker(
        self,
        inp: AERampVelocityInput,
        pipeline: float,
        conversion: float,
        knowledge: float,
        activity: float,
    ) -> RampBlocker:
        # Knowledge gap dominates
        if knowledge >= 35 and inp.training_completion_pct < 60:
            return RampBlocker.knowledge_gap
        # Coaching gap
        if inp.manager_coaching_sessions_completed == 0 and inp.tenure_days >= 45:
            return RampBlocker.coaching_gap
        # Pipeline deficit
        if pipeline >= 35:
            return RampBlocker.pipeline_deficit
        # Slow conversion
        if conversion >= 30:
            return RampBlocker.slow_conversion
        # Activity shortfall
        if activity >= 25:
            return RampBlocker.activity_shortfall
        return RampBlocker.none

    def _recommended_action(
        self, risk: RampRisk, composite: float
    ) -> RampAction:
        if composite >= 70:
            return RampAction.separation_review
        if composite >= 55:
            return RampAction.pip_initiation
        if risk == RampRisk.high:
            return RampAction.ramp_plan_adjustment
        if risk == RampRisk.moderate:
            return RampAction.targeted_coaching
        return RampAction.no_action

    def _signal(
        self,
        blocker: RampBlocker,
        composite: float,
        inp: AERampVelocityInput,
    ) -> str:
        if blocker == RampBlocker.none:
            return "AE ramp velocity within expected parameters"
        msgs = {
            RampBlocker.knowledge_gap: (
                f"Training {inp.training_completion_pct:.0f}% complete — "
                f"certification {'done' if inp.product_certification_completed else 'pending'}"
            ),
            RampBlocker.coaching_gap: (
                f"{inp.manager_coaching_sessions_completed} coaching session(s) in "
                f"{inp.tenure_days}d tenure"
            ),
            RampBlocker.pipeline_deficit: (
                f"Pipeline ${inp.pipeline_created_usd:,.0f} vs "
                f"${inp.pipeline_target_usd:,.0f} target — "
                f"coverage {inp.pipeline_created_usd / inp.pipeline_target_usd * 100:.0f}%"
                if inp.pipeline_target_usd > 0 else
                f"Pipeline ${inp.pipeline_created_usd:,.0f}"
            ),
            RampBlocker.slow_conversion: (
                f"Demo-to-proposal {inp.demo_to_proposal_conversion_rate:.0%} vs "
                f"{inp.benchmark_demo_to_proposal_rate:.0%} benchmark"
            ),
            RampBlocker.activity_shortfall: (
                f"Discovery rate {inp.discovery_call_completion_rate:.0%} — "
                f"attainment {inp.quota_attainment_pct:.0f}% vs "
                f"{inp.ramp_quota_target_pct:.0f}% ramp target"
            ),
        }
        base = msgs.get(blocker, f"ramp composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: AERampVelocityInput) -> AERampVelocityResult:
        pipeline   = self._pipeline_gap_score(inp)
        conversion = self._conversion_velocity_score(inp)
        knowledge  = self._knowledge_readiness_score(inp)
        activity   = self._activity_quality_score(inp)

        composite = _clamp(
            pipeline   * 0.30
            + conversion * 0.30
            + knowledge  * 0.25
            + activity   * 0.15
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        blocker  = self._classify_blocker(inp, pipeline, conversion, knowledge, activity)
        action   = self._recommended_action(risk, composite)

        is_under_ramping = (
            composite >= 40
            or (inp.tenure_days >= 90 and inp.deals_closed_count == 0)
            or inp.quota_attainment_pct < inp.ramp_quota_target_pct * 0.4
        )
        requires_intervention = (
            composite >= 30
            or inp.training_completion_pct < 50
            or inp.manager_coaching_sessions_completed == 0 and inp.tenure_days >= 60
        )

        estimated_quota_attainment_pct = _clamp(
            inp.quota_attainment_pct * (1 - composite / 200.0)
        )

        result = AERampVelocityResult(
            rep_id=inp.rep_id,
            region=inp.region,
            ramp_risk=risk,
            ramp_blocker=blocker,
            ramp_severity=severity,
            recommended_action=action,
            pipeline_gap_score=pipeline,
            conversion_velocity_score=conversion,
            knowledge_readiness_score=knowledge,
            activity_quality_score=activity,
            ramp_composite=composite,
            is_under_ramping=is_under_ramping,
            requires_intervention=requires_intervention,
            estimated_quota_attainment_pct=estimated_quota_attainment_pct,
            ramp_signal=self._signal(blocker, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[AERampVelocityInput]
    ) -> list[AERampVelocityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                              0,
                "risk_counts":                        {},
                "blocker_counts":                     {},
                "severity_counts":                    {},
                "action_counts":                      {},
                "avg_ramp_composite":                 0.0,
                "under_ramping_count":                0,
                "intervention_count":                 0,
                "avg_pipeline_gap_score":             0.0,
                "avg_conversion_velocity_score":      0.0,
                "avg_knowledge_readiness_score":      0.0,
                "avg_activity_quality_score":         0.0,
                "avg_estimated_quota_attainment_pct": 0.0,
            }

        risk_counts:    dict[str, int] = {}
        blocker_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:  dict[str, int] = {}
        total_comp = total_pipe = total_conv = total_know = total_act = total_att = 0.0
        under = intervene = 0

        for r in self._results:
            risk_counts[r.ramp_risk.value]       = risk_counts.get(r.ramp_risk.value, 0) + 1
            blocker_counts[r.ramp_blocker.value] = blocker_counts.get(r.ramp_blocker.value, 0) + 1
            severity_counts[r.ramp_severity.value] = severity_counts.get(r.ramp_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.ramp_composite
            total_pipe += r.pipeline_gap_score
            total_conv += r.conversion_velocity_score
            total_know += r.knowledge_readiness_score
            total_act  += r.activity_quality_score
            total_att  += r.estimated_quota_attainment_pct
            if r.is_under_ramping:
                under += 1
            if r.requires_intervention:
                intervene += 1

        n = len(self._results)
        return {
            "total":                               n,
            "risk_counts":                         risk_counts,
            "blocker_counts":                      blocker_counts,
            "severity_counts":                     severity_counts,
            "action_counts":                       action_counts,
            "avg_ramp_composite":                  round(total_comp / n, 1),
            "under_ramping_count":                 under,
            "intervention_count":                  intervene,
            "avg_pipeline_gap_score":              round(total_pipe / n, 1),
            "avg_conversion_velocity_score":       round(total_conv / n, 1),
            "avg_knowledge_readiness_score":       round(total_know / n, 1),
            "avg_activity_quality_score":          round(total_act  / n, 1),
            "avg_estimated_quota_attainment_pct":  round(total_att  / n, 1),
        }
