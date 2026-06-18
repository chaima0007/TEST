from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ProposalRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ProposalPattern(str, Enum):
    none                   = "none"
    poor_win_rate          = "poor_win_rate"
    proposal_staleness     = "proposal_staleness"
    value_misalignment     = "value_misalignment"
    competitive_loss       = "competitive_loss"
    budget_friction        = "budget_friction"


class ProposalSeverity(str, Enum):
    healthy   = "healthy"
    declining = "declining"
    stalled   = "stalled"
    critical  = "critical"


class ProposalAction(str, Enum):
    no_action                   = "no_action"
    proposal_coaching           = "proposal_coaching"
    value_messaging_update      = "value_messaging_update"
    competitive_repositioning   = "competitive_repositioning"
    pricing_optimization        = "pricing_optimization"
    executive_escalation        = "executive_escalation"


@dataclass
class ProposalConversionInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    proposals_sent_count: int
    proposals_won_count: int
    proposals_lost_count: int
    proposals_pending_count: int
    avg_proposal_size_usd: float
    avg_days_proposal_to_decision: float
    proposals_stale_count: int
    proposal_revision_avg_count: float
    proposals_lost_to_price_count: int
    proposals_lost_to_competitor_count: int
    proposals_lost_no_decision_count: int
    executive_sponsor_rate_pct: float
    value_prop_alignment_score: float
    avg_discount_pct: float
    discount_applied_count: int
    competitive_deals_pct: float
    prior_period_win_rate_pct: float
    current_period_win_rate_pct: float
    multi_stakeholder_proposals_pct: float


@dataclass
class ProposalConversionResult:
    rep_id: str
    region: str
    proposal_risk: ProposalRisk
    proposal_pattern: ProposalPattern
    proposal_severity: ProposalSeverity
    recommended_action: ProposalAction
    proposal_win_rate_score: float
    proposal_velocity_score: float
    value_alignment_score: float
    competitive_exposure_score: float
    proposal_effectiveness_composite: float
    is_win_rate_declining: bool
    requires_proposal_redesign: bool
    estimated_lost_revenue_usd: float
    proposal_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "proposal_risk":                    self.proposal_risk.value,
            "proposal_pattern":                 self.proposal_pattern.value,
            "proposal_severity":                self.proposal_severity.value,
            "recommended_action":               self.recommended_action.value,
            "proposal_win_rate_score":          self.proposal_win_rate_score,
            "proposal_velocity_score":          self.proposal_velocity_score,
            "value_alignment_score":            self.value_alignment_score,
            "competitive_exposure_score":       self.competitive_exposure_score,
            "proposal_effectiveness_composite": self.proposal_effectiveness_composite,
            "is_win_rate_declining":            self.is_win_rate_declining,
            "requires_proposal_redesign":       self.requires_proposal_redesign,
            "estimated_lost_revenue_usd":       self.estimated_lost_revenue_usd,
            "proposal_signal":                  self.proposal_signal,
        }


class SalesProposalConversionIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ProposalConversionResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _proposal_win_rate_score(self, inp: ProposalConversionInput) -> float:
        score = 0.0
        decided = inp.proposals_won_count + inp.proposals_lost_count
        current_win_rate = inp.proposals_won_count / max(decided, 1)

        if current_win_rate < 0.15:
            score += 40.0
        elif current_win_rate < 0.25:
            score += 25.0
        elif current_win_rate < 0.40:
            score += 10.0

        win_rate_delta = inp.current_period_win_rate_pct - inp.prior_period_win_rate_pct
        if win_rate_delta < -0.10:
            score += 30.0
        elif win_rate_delta < -0.05:
            score += 15.0
        elif win_rate_delta < 0:
            score += 8.0

        if inp.proposals_lost_no_decision_count >= 3:
            score += 20.0
        elif inp.proposals_lost_no_decision_count >= 2:
            score += 10.0
        elif inp.proposals_lost_no_decision_count >= 1:
            score += 5.0

        return min(score, 100.0)

    def _proposal_velocity_score(self, inp: ProposalConversionInput) -> float:
        score = 0.0

        if inp.avg_days_proposal_to_decision >= 90.0:
            score += 35.0
        elif inp.avg_days_proposal_to_decision >= 60.0:
            score += 20.0
        elif inp.avg_days_proposal_to_decision >= 30.0:
            score += 8.0

        if inp.proposals_stale_count >= 4:
            score += 30.0
        elif inp.proposals_stale_count >= 2:
            score += 18.0
        elif inp.proposals_stale_count >= 1:
            score += 8.0

        if inp.proposal_revision_avg_count >= 4.0:
            score += 20.0
        elif inp.proposal_revision_avg_count >= 2.5:
            score += 10.0
        elif inp.proposal_revision_avg_count >= 1.5:
            score += 5.0

        return min(score, 100.0)

    def _value_alignment_score(self, inp: ProposalConversionInput) -> float:
        score = 0.0

        if inp.value_prop_alignment_score < 0.35:
            score += 40.0
        elif inp.value_prop_alignment_score < 0.55:
            score += 25.0
        elif inp.value_prop_alignment_score < 0.70:
            score += 10.0

        if inp.executive_sponsor_rate_pct < 0.25:
            score += 30.0
        elif inp.executive_sponsor_rate_pct < 0.45:
            score += 15.0

        if inp.multi_stakeholder_proposals_pct < 0.30:
            score += 20.0
        elif inp.multi_stakeholder_proposals_pct < 0.50:
            score += 10.0

        # Heavy discounting signals value is not landing with buyer
        if inp.avg_discount_pct >= 25.0:
            score += 15.0
        elif inp.avg_discount_pct >= 15.0:
            score += 8.0

        return min(score, 100.0)

    def _competitive_exposure_score(self, inp: ProposalConversionInput) -> float:
        score = 0.0

        if inp.competitive_deals_pct >= 0.60:
            score += 35.0
        elif inp.competitive_deals_pct >= 0.40:
            score += 20.0
        elif inp.competitive_deals_pct >= 0.20:
            score += 8.0

        if inp.proposals_lost_to_competitor_count >= 4:
            score += 35.0
        elif inp.proposals_lost_to_competitor_count >= 2:
            score += 20.0
        elif inp.proposals_lost_to_competitor_count >= 1:
            score += 10.0

        # Competitor loss rate among all losses
        if inp.proposals_lost_count > 0:
            comp_loss_rate = inp.proposals_lost_to_competitor_count / inp.proposals_lost_count
            if comp_loss_rate >= 0.60:
                score += 20.0
            elif comp_loss_rate >= 0.40:
                score += 10.0

        # Defensive discounting to compete
        if inp.discount_applied_count >= 5:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ProposalConversionInput,
                         win_rate: float, velocity: float,
                         value: float, competitive: float) -> ProposalPattern:
        # Priority: competitive_loss > poor_win_rate > proposal_staleness
        #           > value_misalignment > budget_friction > none
        if competitive >= 35 and inp.proposals_lost_to_competitor_count >= 2:
            return ProposalPattern.competitive_loss
        if win_rate >= 35 and inp.current_period_win_rate_pct < 0.30:
            return ProposalPattern.poor_win_rate
        if velocity >= 30 and inp.proposals_stale_count >= 2:
            return ProposalPattern.proposal_staleness
        if value >= 30 and inp.value_prop_alignment_score < 0.50:
            return ProposalPattern.value_misalignment
        if inp.avg_discount_pct >= 15.0 and inp.proposals_lost_to_price_count >= 2:
            return ProposalPattern.budget_friction
        return ProposalPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ProposalRisk:
        if composite >= 60:
            return ProposalRisk.critical
        if composite >= 40:
            return ProposalRisk.high
        if composite >= 20:
            return ProposalRisk.moderate
        return ProposalRisk.low

    def _severity(self, composite: float) -> ProposalSeverity:
        if composite >= 60:
            return ProposalSeverity.critical
        if composite >= 40:
            return ProposalSeverity.stalled
        if composite >= 20:
            return ProposalSeverity.declining
        return ProposalSeverity.healthy

    def _action(self, risk: ProposalRisk, pattern: ProposalPattern) -> ProposalAction:
        if risk == ProposalRisk.critical:
            if pattern == ProposalPattern.competitive_loss:
                return ProposalAction.competitive_repositioning
            return ProposalAction.executive_escalation
        if risk == ProposalRisk.high:
            if pattern == ProposalPattern.competitive_loss:
                return ProposalAction.competitive_repositioning
            if pattern == ProposalPattern.value_misalignment:
                return ProposalAction.value_messaging_update
            return ProposalAction.proposal_coaching
        if risk == ProposalRisk.moderate:
            if pattern == ProposalPattern.budget_friction:
                return ProposalAction.pricing_optimization
            return ProposalAction.proposal_coaching
        return ProposalAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_win_rate_declining(self, inp: ProposalConversionInput,
                                win_rate_score: float) -> bool:
        return (
            inp.current_period_win_rate_pct < inp.prior_period_win_rate_pct - 0.05
            or win_rate_score >= 40
        )

    def _requires_proposal_redesign(self, composite: float,
                                     inp: ProposalConversionInput) -> bool:
        return (
            composite >= 30
            or inp.value_prop_alignment_score < 0.35
            or (inp.proposals_stale_count >= 3 and composite >= 25)
        )

    # ------------------------------------------------------------------
    # Revenue impact
    # ------------------------------------------------------------------

    def _estimated_lost_revenue(self, inp: ProposalConversionInput,
                                  composite: float) -> float:
        return round(inp.proposals_lost_count * inp.avg_proposal_size_usd * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ProposalConversionInput,
                pattern: ProposalPattern, composite: float) -> str:
        if pattern == ProposalPattern.none and composite < 20:
            return "Proposal conversion rate within benchmarks"
        parts: list[str] = []
        if inp.current_period_win_rate_pct * 100 < 30:
            parts.append(f"{inp.current_period_win_rate_pct*100:.0f}% win rate")
        if inp.proposals_stale_count >= 2:
            parts.append(f"{inp.proposals_stale_count} stale proposals")
        if inp.value_prop_alignment_score < 0.50:
            parts.append(f"{inp.value_prop_alignment_score*100:.0f}% value alignment")
        if inp.proposals_lost_to_competitor_count >= 2:
            parts.append(f"{inp.proposals_lost_to_competitor_count} lost to competition")
        label = pattern.value.replace("_", " ") if pattern != ProposalPattern.none else "Proposal risk"
        summary = " — ".join(parts) if parts else "conversion efficiency degraded"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ProposalConversionInput) -> ProposalConversionResult:
        win_rate    = round(self._proposal_win_rate_score(inp), 1)
        velocity    = round(self._proposal_velocity_score(inp), 1)
        value       = round(self._value_alignment_score(inp), 1)
        competitive = round(self._competitive_exposure_score(inp), 1)

        composite = round(win_rate * 0.30 + velocity * 0.20 + value * 0.25 + competitive * 0.25, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, win_rate, velocity, value, competitive)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        declining = self._is_win_rate_declining(inp, win_rate)
        redesign  = self._requires_proposal_redesign(composite, inp)
        revenue   = self._estimated_lost_revenue(inp, composite)
        signal    = self._signal(inp, pattern, composite)

        result = ProposalConversionResult(
            rep_id=inp.rep_id,
            region=inp.region,
            proposal_risk=risk,
            proposal_pattern=pattern,
            proposal_severity=severity,
            recommended_action=action,
            proposal_win_rate_score=win_rate,
            proposal_velocity_score=velocity,
            value_alignment_score=value,
            competitive_exposure_score=competitive,
            proposal_effectiveness_composite=composite,
            is_win_rate_declining=declining,
            requires_proposal_redesign=redesign,
            estimated_lost_revenue_usd=revenue,
            proposal_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ProposalConversionInput]) -> list[ProposalConversionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_proposal_effectiveness_composite": 0.0,
                "declining_win_rate_count": 0,
                "proposal_redesign_count": 0,
                "avg_proposal_win_rate_score": 0.0,
                "avg_proposal_velocity_score": 0.0,
                "avg_value_alignment_score": 0.0,
                "avg_competitive_exposure_score": 0.0,
                "total_estimated_lost_revenue_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_wr = total_vel = total_val = total_ce = total_rev = 0.0

        for r in self._results:
            risk_counts[r.proposal_risk.value]       = risk_counts.get(r.proposal_risk.value, 0) + 1
            pattern_counts[r.proposal_pattern.value] = pattern_counts.get(r.proposal_pattern.value, 0) + 1
            severity_counts[r.proposal_severity.value] = severity_counts.get(r.proposal_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.proposal_effectiveness_composite
            total_wr   += r.proposal_win_rate_score
            total_vel  += r.proposal_velocity_score
            total_val  += r.value_alignment_score
            total_ce   += r.competitive_exposure_score
            total_rev  += r.estimated_lost_revenue_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_proposal_effectiveness_composite": round(total_comp / n, 1),
            "declining_win_rate_count":             sum(1 for r in self._results if r.is_win_rate_declining),
            "proposal_redesign_count":              sum(1 for r in self._results if r.requires_proposal_redesign),
            "avg_proposal_win_rate_score":          round(total_wr / n, 1),
            "avg_proposal_velocity_score":          round(total_vel / n, 1),
            "avg_value_alignment_score":            round(total_val / n, 1),
            "avg_competitive_exposure_score":       round(total_ce / n, 1),
            "total_estimated_lost_revenue_usd":     round(total_rev, 2),
        }
