"""Deal Ghosting Risk Engine — detects when prospects go dark on active deals,
predicting ghosting patterns before they kill pipeline opportunities and enabling
reps to take re-engagement action before deals become unrecoverable."""

from __future__ import annotations

import dataclasses
from enum import Enum


class GhostingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class GhostingPattern(str, Enum):
    none                   = "none"
    silence_after_demo     = "silence_after_demo"
    proposal_drop_off      = "proposal_drop_off"
    champion_unresponsive  = "champion_unresponsive"
    multi_stakeholder_fade = "multi_stakeholder_fade"
    end_of_cycle_ghost     = "end_of_cycle_ghost"


class GhostingSeverity(str, Enum):
    active    = "active"
    cooling   = "cooling"
    dark      = "dark"
    lost      = "lost"


class GhostingAction(str, Enum):
    no_action            = "no_action"
    follow_up_sequence   = "follow_up_sequence"
    manager_re_engage    = "manager_re_engage"
    exec_outreach        = "exec_outreach"
    deal_disqualification = "deal_disqualification"


@dataclasses.dataclass
class DealGhostingInput:
    deal_id:                          str
    rep_id:                           str
    evaluation_period_id:             str
    days_since_last_prospect_response: int
    days_since_last_rep_outreach:     int
    outreach_attempts_no_response:    int
    deal_stage:                       str
    days_in_current_stage:            int
    expected_days_in_stage:           int
    demo_completed:                   int
    days_since_demo:                  int
    proposal_sent:                    int
    days_since_proposal:              int
    stakeholder_count:                int
    responsive_stakeholders:          int
    champion_last_response_days:      int
    email_open_rate_last_30d:         float
    meeting_decline_count:            int
    meeting_accept_count:             int
    competitor_mentioned_last_contact: int
    deal_value_usd:                   float
    close_date_days_remaining:        int


@dataclasses.dataclass
class DealGhostingResult:
    deal_id:                       str
    rep_id:                        str
    ghosting_risk:                 GhostingRisk
    ghosting_pattern:              GhostingPattern
    ghosting_severity:             GhostingSeverity
    recommended_action:            GhostingAction
    silence_score:                 float
    engagement_decay_score:        float
    stakeholder_coverage_score:    float
    deal_momentum_score:           float
    ghosting_composite:            float
    is_ghosted:                    bool
    requires_escalation:           bool
    estimated_deal_recovery_pct:   float
    ghosting_signal:               str

    def to_dict(self) -> dict:
        return {
            "deal_id":                       self.deal_id,
            "rep_id":                        self.rep_id,
            "ghosting_risk":                 self.ghosting_risk.value,
            "ghosting_pattern":              self.ghosting_pattern.value,
            "ghosting_severity":             self.ghosting_severity.value,
            "recommended_action":            self.recommended_action.value,
            "silence_score":                 round(self.silence_score, 1),
            "engagement_decay_score":        round(self.engagement_decay_score, 1),
            "stakeholder_coverage_score":    round(self.stakeholder_coverage_score, 1),
            "deal_momentum_score":           round(self.deal_momentum_score, 1),
            "ghosting_composite":            round(self.ghosting_composite, 1),
            "is_ghosted":                    self.is_ghosted,
            "requires_escalation":           self.requires_escalation,
            "estimated_deal_recovery_pct":   round(self.estimated_deal_recovery_pct, 1),
            "ghosting_signal":               self.ghosting_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class DealGhostingRiskEngine:
    """Predicts prospect ghosting risk to enable early re-engagement before deals die."""

    def __init__(self) -> None:
        self._results: list[DealGhostingResult] = []

    # ── sub-scores (HIGHER = more ghosting risk) ─────────────────────────────

    def _silence_score(self, inp: DealGhostingInput) -> float:
        score = 0.0
        # Days since prospect responded
        if inp.days_since_last_prospect_response >= 21:
            score += 45.0
        elif inp.days_since_last_prospect_response >= 14:
            score += 28.0
        elif inp.days_since_last_prospect_response >= 7:
            score += 14.0
        elif inp.days_since_last_prospect_response >= 3:
            score += 5.0
        # Unanswered outreach attempts
        if inp.outreach_attempts_no_response >= 6:
            score += 35.0
        elif inp.outreach_attempts_no_response >= 4:
            score += 22.0
        elif inp.outreach_attempts_no_response >= 2:
            score += 10.0
        elif inp.outreach_attempts_no_response >= 1:
            score += 5.0
        # Champion specifically unresponsive
        if inp.champion_last_response_days >= 21:
            score += 20.0
        elif inp.champion_last_response_days >= 14:
            score += 12.0
        elif inp.champion_last_response_days >= 7:
            score += 6.0
        return _clamp(score)

    def _engagement_decay_score(self, inp: DealGhostingInput) -> float:
        score = 0.0
        # Low email open rate
        if inp.email_open_rate_last_30d < 0.10:
            score += 35.0
        elif inp.email_open_rate_last_30d < 0.20:
            score += 20.0
        elif inp.email_open_rate_last_30d < 0.35:
            score += 10.0
        # Meeting declines
        if inp.meeting_decline_count >= 4:
            score += 35.0
        elif inp.meeting_decline_count >= 2:
            score += 20.0
        elif inp.meeting_decline_count >= 1:
            score += 10.0
        # Proposal sent but no follow-up response
        if inp.proposal_sent == 1 and inp.days_since_proposal >= 14:
            score += 30.0
        elif inp.proposal_sent == 1 and inp.days_since_proposal >= 7:
            score += 15.0
        return _clamp(score)

    def _stakeholder_coverage_score(self, inp: DealGhostingInput) -> float:
        score = 0.0
        # Responsive stakeholder ratio
        if inp.stakeholder_count > 0:
            responsive_ratio = inp.responsive_stakeholders / inp.stakeholder_count
            if responsive_ratio < 0.2:
                score += 50.0
            elif responsive_ratio < 0.4:
                score += 30.0
            elif responsive_ratio < 0.6:
                score += 15.0
        # Competitor mentioned in last contact (losing champion)
        if inp.competitor_mentioned_last_contact == 1:
            score += 30.0
        # Demo done but silence since
        if inp.demo_completed == 1 and inp.days_since_demo >= 21:
            score += 20.0
        elif inp.demo_completed == 1 and inp.days_since_demo >= 14:
            score += 10.0
        return _clamp(score)

    def _deal_momentum_score(self, inp: DealGhostingInput) -> float:
        score = 0.0
        # Stage stagnation vs expected
        if inp.expected_days_in_stage > 0:
            stage_ratio = inp.days_in_current_stage / inp.expected_days_in_stage
            if stage_ratio >= 3.0:
                score += 40.0
            elif stage_ratio >= 2.0:
                score += 25.0
            elif stage_ratio >= 1.5:
                score += 12.0
        # Close date urgency (approaching deadline with no activity)
        if inp.close_date_days_remaining <= 7 and inp.days_since_last_prospect_response >= 7:
            score += 35.0
        elif inp.close_date_days_remaining <= 14 and inp.days_since_last_prospect_response >= 10:
            score += 20.0
        # Low meeting acceptance
        total_meetings = inp.meeting_accept_count + inp.meeting_decline_count
        if total_meetings > 0:
            accept_ratio = inp.meeting_accept_count / total_meetings
            if accept_ratio < 0.25:
                score += 25.0
            elif accept_ratio < 0.5:
                score += 12.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> GhostingRisk:
        if composite < 20:
            return GhostingRisk.low
        if composite < 40:
            return GhostingRisk.moderate
        if composite < 60:
            return GhostingRisk.high
        return GhostingRisk.critical

    def _classify_severity(self, composite: float) -> GhostingSeverity:
        if composite < 20:
            return GhostingSeverity.active
        if composite < 40:
            return GhostingSeverity.cooling
        if composite < 60:
            return GhostingSeverity.dark
        return GhostingSeverity.lost

    def _classify_pattern(
        self,
        inp: DealGhostingInput,
        silence: float,
        engagement: float,
        stakeholder: float,
        momentum: float,
    ) -> GhostingPattern:
        # End-of-cycle ghost: close date near but no response
        if inp.close_date_days_remaining <= 14 and inp.days_since_last_prospect_response >= 10:
            return GhostingPattern.end_of_cycle_ghost
        # Multi-stakeholder fade: most stakeholders unresponsive
        if inp.stakeholder_count >= 3 and inp.responsive_stakeholders <= 1:
            return GhostingPattern.multi_stakeholder_fade
        # Champion unresponsive
        if inp.champion_last_response_days >= 14:
            return GhostingPattern.champion_unresponsive
        # Proposal drop-off
        if inp.proposal_sent == 1 and inp.days_since_proposal >= 14 and engagement >= 25:
            return GhostingPattern.proposal_drop_off
        # Silence after demo
        if inp.demo_completed == 1 and inp.days_since_demo >= 14 and silence >= 20:
            return GhostingPattern.silence_after_demo
        return GhostingPattern.none

    def _recommended_action(
        self, risk: GhostingRisk, composite: float
    ) -> GhostingAction:
        if composite >= 60:
            return GhostingAction.deal_disqualification
        if composite >= 50:
            return GhostingAction.exec_outreach
        if risk == GhostingRisk.high:
            return GhostingAction.manager_re_engage
        if risk == GhostingRisk.moderate:
            return GhostingAction.follow_up_sequence
        return GhostingAction.no_action

    def _signal(
        self,
        pattern: GhostingPattern,
        composite: float,
        inp: DealGhostingInput,
    ) -> str:
        if pattern == GhostingPattern.none:
            return "Deal engagement within healthy parameters"
        msgs = {
            GhostingPattern.end_of_cycle_ghost: (
                f"{inp.days_since_last_prospect_response}d silence — "
                f"{inp.close_date_days_remaining}d to close date"
            ),
            GhostingPattern.multi_stakeholder_fade: (
                f"{inp.responsive_stakeholders}/{inp.stakeholder_count} stakeholders responsive"
            ),
            GhostingPattern.champion_unresponsive: (
                f"Champion dark {inp.champion_last_response_days}d — "
                f"{inp.outreach_attempts_no_response} unanswered outreach"
            ),
            GhostingPattern.proposal_drop_off: (
                f"Proposal sent {inp.days_since_proposal}d ago — no response — "
                f"{inp.outreach_attempts_no_response} attempts"
            ),
            GhostingPattern.silence_after_demo: (
                f"Demo {inp.days_since_demo}d ago — {inp.days_since_last_prospect_response}d silence"
            ),
        }
        base = msgs.get(pattern, f"ghosting composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: DealGhostingInput) -> DealGhostingResult:
        silence    = self._silence_score(inp)
        engagement = self._engagement_decay_score(inp)
        stakeholder = self._stakeholder_coverage_score(inp)
        momentum   = self._deal_momentum_score(inp)

        composite = _clamp(
            silence     * 0.35
            + engagement * 0.25
            + stakeholder * 0.25
            + momentum   * 0.15
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp, silence, engagement, stakeholder, momentum)
        action   = self._recommended_action(risk, composite)

        is_ghosted = (
            composite >= 40
            or inp.outreach_attempts_no_response >= 5
            or inp.days_since_last_prospect_response >= 21
        )
        requires_escalation = (
            composite >= 30
            or inp.champion_last_response_days >= 14
            or (inp.close_date_days_remaining <= 7 and composite >= 20)
        )

        estimated_deal_recovery_pct = _clamp(100.0 - composite)

        result = DealGhostingResult(
            deal_id=inp.deal_id,
            rep_id=inp.rep_id,
            ghosting_risk=risk,
            ghosting_pattern=pattern,
            ghosting_severity=severity,
            recommended_action=action,
            silence_score=silence,
            engagement_decay_score=engagement,
            stakeholder_coverage_score=stakeholder,
            deal_momentum_score=momentum,
            ghosting_composite=composite,
            is_ghosted=is_ghosted,
            requires_escalation=requires_escalation,
            estimated_deal_recovery_pct=estimated_deal_recovery_pct,
            ghosting_signal=self._signal(pattern, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[DealGhostingInput]
    ) -> list[DealGhostingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                          0,
                "risk_counts":                    {},
                "pattern_counts":                 {},
                "severity_counts":                {},
                "action_counts":                  {},
                "avg_ghosting_composite":         0.0,
                "ghosted_count":                  0,
                "escalation_count":               0,
                "avg_silence_score":              0.0,
                "avg_engagement_decay_score":     0.0,
                "avg_stakeholder_coverage_score": 0.0,
                "avg_deal_momentum_score":        0.0,
                "avg_estimated_deal_recovery_pct": 0.0,
            }

        risk_counts:    dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:  dict[str, int] = {}
        total_comp = total_sil = total_eng = total_stk = total_mom = total_rec = 0.0
        ghosted = esc = 0

        for r in self._results:
            risk_counts[r.ghosting_risk.value]       = risk_counts.get(r.ghosting_risk.value, 0) + 1
            pattern_counts[r.ghosting_pattern.value] = pattern_counts.get(r.ghosting_pattern.value, 0) + 1
            severity_counts[r.ghosting_severity.value] = severity_counts.get(r.ghosting_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.ghosting_composite
            total_sil  += r.silence_score
            total_eng  += r.engagement_decay_score
            total_stk  += r.stakeholder_coverage_score
            total_mom  += r.deal_momentum_score
            total_rec  += r.estimated_deal_recovery_pct
            if r.is_ghosted:
                ghosted += 1
            if r.requires_escalation:
                esc += 1

        n = len(self._results)
        return {
            "total":                           n,
            "risk_counts":                     risk_counts,
            "pattern_counts":                  pattern_counts,
            "severity_counts":                 severity_counts,
            "action_counts":                   action_counts,
            "avg_ghosting_composite":          round(total_comp / n, 1),
            "ghosted_count":                   ghosted,
            "escalation_count":                esc,
            "avg_silence_score":               round(total_sil  / n, 1),
            "avg_engagement_decay_score":      round(total_eng  / n, 1),
            "avg_stakeholder_coverage_score":  round(total_stk  / n, 1),
            "avg_deal_momentum_score":         round(total_mom  / n, 1),
            "avg_estimated_deal_recovery_pct": round(total_rec  / n, 1),
        }
