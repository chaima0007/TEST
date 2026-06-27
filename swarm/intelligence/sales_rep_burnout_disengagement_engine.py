"""Sales Rep Burnout & Disengagement Risk Engine — detects declining activity,
performance decay, and disengagement patterns signaling rep burnout or
flight risk before they damage pipeline and customer relationships."""

from __future__ import annotations

import dataclasses
from enum import Enum


class BurnoutRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class BurnoutIndicator(str, Enum):
    none                = "none"
    activity_decline    = "activity_decline"
    velocity_slowdown   = "velocity_slowdown"
    quality_degradation = "quality_degradation"
    disengagement       = "disengagement"
    flight_risk         = "flight_risk"


class BurnoutSeverity(str, Enum):
    stable      = "stable"
    watch       = "watch"
    concerning  = "concerning"
    crisis      = "crisis"


class BurnoutAction(str, Enum):
    no_action             = "no_action"
    manager_checkin       = "manager_checkin"
    hr_review             = "hr_review"
    performance_pip       = "performance_pip"
    retention_intervention = "retention_intervention"


@dataclasses.dataclass
class SalesRepBurnoutInput:
    rep_id:                           str
    region:                           str
    evaluation_period_id:             str
    calls_last_30d:                   int
    calls_prior_30d:                  int
    emails_last_30d:                  int
    emails_prior_30d:                 int
    meetings_last_30d:                int
    meetings_prior_30d:               int
    quota_attainment_pct_last_90d:    float
    quota_attainment_pct_prior_90d:   float
    avg_deal_cycle_days_last_30d:     float
    avg_deal_cycle_days_prior_30d:    float
    pipeline_created_last_30d_usd:    float
    pipeline_created_prior_30d_usd:   float
    crm_update_frequency_last_30d:    int
    crm_update_frequency_prior_30d:   int
    pto_days_taken_last_90d:          int
    late_submissions_count:           int
    manager_escalations_count:        int
    peer_collaboration_score:         float
    rep_tenure_months:                int


@dataclasses.dataclass
class SalesRepBurnoutResult:
    rep_id:                         str
    region:                         str
    burnout_risk:                   BurnoutRisk
    burnout_indicator:              BurnoutIndicator
    burnout_severity:               BurnoutSeverity
    recommended_action:             BurnoutAction
    activity_decline_score:         float
    performance_decay_score:        float
    engagement_score:               float
    pipeline_health_score:          float
    burnout_composite:              float
    is_burnout_risk:                bool
    requires_hr_review:             bool
    estimated_productivity_loss_pct: float
    burnout_signal:                 str

    def to_dict(self) -> dict:
        return {
            "rep_id":                          self.rep_id,
            "region":                          self.region,
            "burnout_risk":                    self.burnout_risk.value,
            "burnout_indicator":               self.burnout_indicator.value,
            "burnout_severity":                self.burnout_severity.value,
            "recommended_action":              self.recommended_action.value,
            "activity_decline_score":          round(self.activity_decline_score, 1),
            "performance_decay_score":         round(self.performance_decay_score, 1),
            "engagement_score":                round(self.engagement_score, 1),
            "pipeline_health_score":           round(self.pipeline_health_score, 1),
            "burnout_composite":               round(self.burnout_composite, 1),
            "is_burnout_risk":                 self.is_burnout_risk,
            "requires_hr_review":              self.requires_hr_review,
            "estimated_productivity_loss_pct": round(self.estimated_productivity_loss_pct, 1),
            "burnout_signal":                  self.burnout_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


def _pct_decline(current: float, prior: float) -> float:
    """Returns decline as a 0-100 score. Positive = decline, 0 = no decline."""
    if prior <= 0:
        return 0.0
    delta = (prior - current) / prior
    return _clamp(delta * 100.0)


class SalesRepBurnoutDisengagementEngine:
    """Detects burnout and disengagement signals in sales rep activity and performance."""

    def __init__(self) -> None:
        self._results: list[SalesRepBurnoutResult] = []

    # ── sub-scores (HIGHER = more burnout risk) ──────────────────────────────

    def _activity_decline_score(self, inp: SalesRepBurnoutInput) -> float:
        score = 0.0
        # Call volume drop
        call_decline = _pct_decline(inp.calls_last_30d, inp.calls_prior_30d)
        if call_decline >= 50:
            score += 35.0
        elif call_decline >= 30:
            score += 22.0
        elif call_decline >= 15:
            score += 10.0
        # Email volume drop
        email_decline = _pct_decline(inp.emails_last_30d, inp.emails_prior_30d)
        if email_decline >= 50:
            score += 25.0
        elif email_decline >= 30:
            score += 15.0
        elif email_decline >= 15:
            score += 7.0
        # Meeting decline
        meeting_decline = _pct_decline(inp.meetings_last_30d, inp.meetings_prior_30d)
        if meeting_decline >= 50:
            score += 25.0
        elif meeting_decline >= 30:
            score += 15.0
        elif meeting_decline >= 15:
            score += 7.0
        # CRM update frequency drop
        crm_decline = _pct_decline(
            inp.crm_update_frequency_last_30d, inp.crm_update_frequency_prior_30d
        )
        if crm_decline >= 60:
            score += 15.0
        elif crm_decline >= 35:
            score += 8.0
        return _clamp(score)

    def _performance_decay_score(self, inp: SalesRepBurnoutInput) -> float:
        score = 0.0
        # Quota attainment decline
        quota_delta = inp.quota_attainment_pct_prior_90d - inp.quota_attainment_pct_last_90d
        if quota_delta >= 40:
            score += 40.0
        elif quota_delta >= 25:
            score += 28.0
        elif quota_delta >= 15:
            score += 16.0
        elif quota_delta >= 8:
            score += 8.0
        # Deal cycle lengthening (slower closings = disengagement)
        if inp.avg_deal_cycle_days_prior_30d > 0:
            cycle_growth = (
                (inp.avg_deal_cycle_days_last_30d - inp.avg_deal_cycle_days_prior_30d)
                / inp.avg_deal_cycle_days_prior_30d
            )
            if cycle_growth >= 0.5:
                score += 30.0
            elif cycle_growth >= 0.3:
                score += 18.0
            elif cycle_growth >= 0.15:
                score += 8.0
        # Absolute low attainment
        if inp.quota_attainment_pct_last_90d < 50:
            score += 30.0
        elif inp.quota_attainment_pct_last_90d < 70:
            score += 15.0
        return _clamp(score)

    def _engagement_score(self, inp: SalesRepBurnoutInput) -> float:
        score = 0.0
        # Late submissions signal disengagement
        if inp.late_submissions_count >= 5:
            score += 30.0
        elif inp.late_submissions_count >= 3:
            score += 18.0
        elif inp.late_submissions_count >= 1:
            score += 8.0
        # Manager escalations (conflict signal)
        if inp.manager_escalations_count >= 4:
            score += 25.0
        elif inp.manager_escalations_count >= 2:
            score += 15.0
        elif inp.manager_escalations_count >= 1:
            score += 7.0
        # Low peer collaboration
        if inp.peer_collaboration_score < 30:
            score += 30.0
        elif inp.peer_collaboration_score < 50:
            score += 18.0
        elif inp.peer_collaboration_score < 65:
            score += 8.0
        # Excessive PTO (checked out)
        if inp.pto_days_taken_last_90d >= 20:
            score += 15.0
        elif inp.pto_days_taken_last_90d >= 12:
            score += 8.0
        return _clamp(score)

    def _pipeline_health_score(self, inp: SalesRepBurnoutInput) -> float:
        score = 0.0
        # Pipeline creation collapse
        pipe_decline = _pct_decline(
            inp.pipeline_created_last_30d_usd, inp.pipeline_created_prior_30d_usd
        )
        if pipe_decline >= 60:
            score += 55.0
        elif pipe_decline >= 40:
            score += 38.0
        elif pipe_decline >= 20:
            score += 20.0
        elif pipe_decline >= 10:
            score += 8.0
        # Absolute pipeline drought
        if inp.pipeline_created_last_30d_usd == 0:
            score += 45.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> BurnoutRisk:
        if composite < 20:
            return BurnoutRisk.low
        if composite < 40:
            return BurnoutRisk.moderate
        if composite < 60:
            return BurnoutRisk.high
        return BurnoutRisk.critical

    def _classify_severity(self, composite: float) -> BurnoutSeverity:
        if composite < 20:
            return BurnoutSeverity.stable
        if composite < 40:
            return BurnoutSeverity.watch
        if composite < 60:
            return BurnoutSeverity.concerning
        return BurnoutSeverity.crisis

    def _classify_indicator(
        self,
        inp: SalesRepBurnoutInput,
        activity: float,
        performance: float,
        engagement: float,
        pipeline: float,
    ) -> BurnoutIndicator:
        # Flight risk: high escalations + low collaboration + high pto
        if inp.manager_escalations_count >= 3 and inp.peer_collaboration_score < 40:
            return BurnoutIndicator.flight_risk
        # Disengagement: all scores elevated
        if activity >= 30 and engagement >= 30 and pipeline >= 30:
            return BurnoutIndicator.disengagement
        # Quality degradation: performance decay dominates
        if performance >= 40:
            return BurnoutIndicator.quality_degradation
        # Velocity slowdown: deal cycles lengthening
        if inp.avg_deal_cycle_days_prior_30d > 0:
            cycle_growth = (
                (inp.avg_deal_cycle_days_last_30d - inp.avg_deal_cycle_days_prior_30d)
                / inp.avg_deal_cycle_days_prior_30d
            )
            if cycle_growth >= 0.3:
                return BurnoutIndicator.velocity_slowdown
        # Activity decline
        if activity >= 25:
            return BurnoutIndicator.activity_decline
        return BurnoutIndicator.none

    def _recommended_action(
        self, risk: BurnoutRisk, composite: float, indicator: BurnoutIndicator
    ) -> BurnoutAction:
        if composite >= 60 or indicator == BurnoutIndicator.flight_risk:
            return BurnoutAction.retention_intervention
        if composite >= 50:
            return BurnoutAction.performance_pip
        if risk == BurnoutRisk.high:
            return BurnoutAction.hr_review
        if risk == BurnoutRisk.moderate:
            return BurnoutAction.manager_checkin
        return BurnoutAction.no_action

    def _signal(
        self,
        indicator: BurnoutIndicator,
        composite: float,
        inp: SalesRepBurnoutInput,
    ) -> str:
        if indicator == BurnoutIndicator.none:
            return "Rep engagement and activity within healthy parameters"
        call_decline = _pct_decline(inp.calls_last_30d, inp.calls_prior_30d)
        msgs = {
            BurnoutIndicator.flight_risk: (
                f"{inp.manager_escalations_count} escalations — "
                f"peer collaboration {inp.peer_collaboration_score:.0f}/100"
            ),
            BurnoutIndicator.disengagement: (
                f"Broad disengagement — calls down {call_decline:.0f}% — "
                f"pipeline down {_pct_decline(inp.pipeline_created_last_30d_usd, inp.pipeline_created_prior_30d_usd):.0f}%"
            ),
            BurnoutIndicator.quality_degradation: (
                f"Attainment dropped {inp.quota_attainment_pct_prior_90d - inp.quota_attainment_pct_last_90d:.0f}pts — "
                f"now {inp.quota_attainment_pct_last_90d:.0f}%"
            ),
            BurnoutIndicator.velocity_slowdown: (
                f"Deal cycle grew from {inp.avg_deal_cycle_days_prior_30d:.0f}d to "
                f"{inp.avg_deal_cycle_days_last_30d:.0f}d"
            ),
            BurnoutIndicator.activity_decline: (
                f"Activity down {call_decline:.0f}% — "
                f"{inp.calls_last_30d} calls vs {inp.calls_prior_30d} prior"
            ),
        }
        base = msgs.get(indicator, f"burnout composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: SalesRepBurnoutInput) -> SalesRepBurnoutResult:
        activity    = self._activity_decline_score(inp)
        performance = self._performance_decay_score(inp)
        engagement  = self._engagement_score(inp)
        pipeline    = self._pipeline_health_score(inp)

        composite = _clamp(
            activity    * 0.30
            + performance * 0.30
            + engagement  * 0.25
            + pipeline    * 0.15
        )
        composite = round(composite, 1)

        risk      = self._classify_risk(composite)
        severity  = self._classify_severity(composite)
        indicator = self._classify_indicator(inp, activity, performance, engagement, pipeline)
        action    = self._recommended_action(risk, composite, indicator)

        is_burnout_risk = (
            composite >= 40
            or inp.quota_attainment_pct_last_90d < 50
            or (inp.calls_last_30d == 0 and inp.emails_last_30d == 0)
        )
        requires_hr_review = (
            composite >= 30
            or inp.manager_escalations_count >= 3
            or indicator == BurnoutIndicator.flight_risk
        )

        estimated_productivity_loss_pct = _clamp(composite * 0.75)

        result = SalesRepBurnoutResult(
            rep_id=inp.rep_id,
            region=inp.region,
            burnout_risk=risk,
            burnout_indicator=indicator,
            burnout_severity=severity,
            recommended_action=action,
            activity_decline_score=activity,
            performance_decay_score=performance,
            engagement_score=engagement,
            pipeline_health_score=pipeline,
            burnout_composite=composite,
            is_burnout_risk=is_burnout_risk,
            requires_hr_review=requires_hr_review,
            estimated_productivity_loss_pct=estimated_productivity_loss_pct,
            burnout_signal=self._signal(indicator, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[SalesRepBurnoutInput]
    ) -> list[SalesRepBurnoutResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                              0,
                "risk_counts":                        {},
                "indicator_counts":                   {},
                "severity_counts":                    {},
                "action_counts":                      {},
                "avg_burnout_composite":              0.0,
                "burnout_risk_count":                 0,
                "hr_review_count":                    0,
                "avg_activity_decline_score":         0.0,
                "avg_performance_decay_score":        0.0,
                "avg_engagement_score":               0.0,
                "avg_pipeline_health_score":          0.0,
                "avg_estimated_productivity_loss_pct": 0.0,
            }

        risk_counts:      dict[str, int] = {}
        indicator_counts: dict[str, int] = {}
        severity_counts:  dict[str, int] = {}
        action_counts:    dict[str, int] = {}
        total_comp = total_act = total_perf = total_eng = total_pipe = total_loss = 0.0
        burnout = hr = 0

        for r in self._results:
            risk_counts[r.burnout_risk.value]       = risk_counts.get(r.burnout_risk.value, 0) + 1
            indicator_counts[r.burnout_indicator.value] = indicator_counts.get(r.burnout_indicator.value, 0) + 1
            severity_counts[r.burnout_severity.value]   = severity_counts.get(r.burnout_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.burnout_composite
            total_act  += r.activity_decline_score
            total_perf += r.performance_decay_score
            total_eng  += r.engagement_score
            total_pipe += r.pipeline_health_score
            total_loss += r.estimated_productivity_loss_pct
            if r.is_burnout_risk:
                burnout += 1
            if r.requires_hr_review:
                hr += 1

        n = len(self._results)
        return {
            "total":                               n,
            "risk_counts":                         risk_counts,
            "indicator_counts":                    indicator_counts,
            "severity_counts":                     severity_counts,
            "action_counts":                       action_counts,
            "avg_burnout_composite":               round(total_comp / n, 1),
            "burnout_risk_count":                  burnout,
            "hr_review_count":                     hr,
            "avg_activity_decline_score":          round(total_act  / n, 1),
            "avg_performance_decay_score":         round(total_perf / n, 1),
            "avg_engagement_score":                round(total_eng  / n, 1),
            "avg_pipeline_health_score":           round(total_pipe / n, 1),
            "avg_estimated_productivity_loss_pct": round(total_loss / n, 1),
        }
