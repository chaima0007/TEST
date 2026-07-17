from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class DecayRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class DecayPattern(str, Enum):
    none                          = "none"
    gradual_erosion               = "gradual_erosion"
    sharp_cliff_drop              = "sharp_cliff_drop"
    competitive_displacement      = "competitive_displacement"
    late_stage_collapse           = "late_stage_collapse"
    deal_size_inflation_trap      = "deal_size_inflation_trap"


class DecaySeverity(str, Enum):
    improving   = "improving"
    stable      = "stable"
    declining   = "declining"
    collapsing  = "collapsing"


class DecayAction(str, Enum):
    no_action                      = "no_action"
    win_loss_debrief_coaching      = "win_loss_debrief_coaching"
    competitive_positioning_review = "competitive_positioning_review"
    deal_quality_audit             = "deal_quality_audit"
    late_stage_process_coaching    = "late_stage_process_coaching"
    urgent_pipeline_intervention   = "urgent_pipeline_intervention"


@dataclass
class DecayInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    current_win_rate_pct: float
    win_rate_3m_ago_pct: float
    win_rate_6m_ago_pct: float
    win_rate_decline_velocity_pct: float
    late_stage_win_rate_pct: float
    early_stage_win_rate_pct: float
    competitive_win_rate_pct: float
    uncontested_win_rate_pct: float
    avg_deal_size_current_usd: float
    avg_deal_size_6m_ago_usd: float
    deals_lost_at_stage_4plus_pct: float
    no_decision_rate_pct: float
    discounting_frequency_pct: float
    avg_discount_depth_pct: float
    champion_presence_lost_deals_pct: float
    multi_stakeholder_win_rate_pct: float
    single_stakeholder_win_rate_pct: float
    total_deals_evaluated: int
    avg_opportunity_value_usd: float


@dataclass
class DecayResult:
    rep_id: str
    region: str
    decay_risk: DecayRisk
    decay_pattern: DecayPattern
    decay_severity: DecaySeverity
    recommended_action: DecayAction
    trajectory_score: float
    competitive_score: float
    deal_quality_score: float
    late_stage_score: float
    decay_composite: float
    has_decay_gap: bool
    requires_decay_coaching: bool
    estimated_revenue_decay_usd: float
    decay_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                         self.rep_id,
            "region":                         self.region,
            "decay_risk":                     self.decay_risk.value,
            "decay_pattern":                  self.decay_pattern.value,
            "decay_severity":                 self.decay_severity.value,
            "recommended_action":             self.recommended_action.value,
            "trajectory_score":               self.trajectory_score,
            "competitive_score":              self.competitive_score,
            "deal_quality_score":             self.deal_quality_score,
            "late_stage_score":               self.late_stage_score,
            "decay_composite":                self.decay_composite,
            "has_decay_gap":                  self.has_decay_gap,
            "requires_decay_coaching":        self.requires_decay_coaching,
            "estimated_revenue_decay_usd":    self.estimated_revenue_decay_usd,
            "decay_signal":                   self.decay_signal,
        }


class SalesWinRateDecayIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[DecayResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _trajectory_score(self, inp: DecayInput) -> float:
        """Risk from win-rate decline velocity and trend depth."""
        score = 0.0

        # Overall decline from 6 months ago
        decline_6m = inp.win_rate_6m_ago_pct - inp.current_win_rate_pct
        if decline_6m >= 0.20:
            score += 40.0
        elif decline_6m >= 0.10:
            score += 22.0
        elif decline_6m >= 0.05:
            score += 8.0

        # Recent velocity (3m decline)
        if inp.win_rate_decline_velocity_pct >= 0.15:
            score += 35.0
        elif inp.win_rate_decline_velocity_pct >= 0.08:
            score += 18.0

        # Absolute win rate floor
        if inp.current_win_rate_pct <= 0.20:
            score += 25.0
        elif inp.current_win_rate_pct <= 0.35:
            score += 12.0

        return min(score, 100.0)

    def _competitive_score(self, inp: DecayInput) -> float:
        """Risk from competitive win-rate erosion."""
        score = 0.0

        if inp.competitive_win_rate_pct <= 0.20:
            score += 40.0
        elif inp.competitive_win_rate_pct <= 0.35:
            score += 22.0
        elif inp.competitive_win_rate_pct <= 0.50:
            score += 8.0

        gap = inp.uncontested_win_rate_pct - inp.competitive_win_rate_pct
        if gap >= 0.40:
            score += 35.0
        elif gap >= 0.25:
            score += 18.0

        if inp.discounting_frequency_pct >= 0.70:
            score += 25.0
        elif inp.discounting_frequency_pct >= 0.45:
            score += 12.0

        return min(score, 100.0)

    def _deal_quality_score(self, inp: DecayInput) -> float:
        """Risk from deal size inflation and no-decision churn."""
        score = 0.0

        if inp.no_decision_rate_pct >= 0.40:
            score += 40.0
        elif inp.no_decision_rate_pct >= 0.25:
            score += 22.0
        elif inp.no_decision_rate_pct >= 0.15:
            score += 8.0

        # Deal size inflation = chasing deals too large for rep's current skill
        size_inflation = inp.avg_deal_size_current_usd / max(inp.avg_deal_size_6m_ago_usd, 1.0)
        if size_inflation >= 2.0:
            score += 35.0
        elif size_inflation >= 1.50:
            score += 18.0

        if inp.avg_discount_depth_pct >= 0.25:
            score += 25.0
        elif inp.avg_discount_depth_pct >= 0.15:
            score += 12.0

        return min(score, 100.0)

    def _late_stage_score(self, inp: DecayInput) -> float:
        """Risk from late-stage collapse patterns."""
        score = 0.0

        if inp.deals_lost_at_stage_4plus_pct >= 0.50:
            score += 45.0
        elif inp.deals_lost_at_stage_4plus_pct >= 0.30:
            score += 25.0
        elif inp.deals_lost_at_stage_4plus_pct >= 0.15:
            score += 10.0

        gap = inp.early_stage_win_rate_pct - inp.late_stage_win_rate_pct
        if gap >= 0.35:
            score += 30.0
        elif gap >= 0.20:
            score += 15.0

        if inp.champion_presence_lost_deals_pct <= 0.20:
            score += 25.0
        elif inp.champion_presence_lost_deals_pct <= 0.40:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: DecayInput,
                          trajectory: float, competitive: float,
                          deal_quality: float, late_stage: float) -> DecayPattern:
        # Deal size inflation trap: large deal-size jump + high no-decision rate
        size_inflation = inp.avg_deal_size_current_usd / max(inp.avg_deal_size_6m_ago_usd, 1.0)
        if size_inflation >= 1.80 and inp.no_decision_rate_pct >= 0.30:
            return DecayPattern.deal_size_inflation_trap

        # Late stage collapse: most losses happen deep in funnel
        if late_stage >= 35 and inp.deals_lost_at_stage_4plus_pct >= 0.40:
            return DecayPattern.late_stage_collapse

        # Competitive displacement: competitive win rate far below uncontested
        if competitive >= 35 and inp.competitive_win_rate_pct <= 0.25:
            return DecayPattern.competitive_displacement

        # Sharp cliff drop: rapid recent velocity + big 3m decline
        if trajectory >= 35 and inp.win_rate_decline_velocity_pct >= 0.12:
            return DecayPattern.sharp_cliff_drop

        # Gradual erosion: slow but sustained decline
        decline_6m = inp.win_rate_6m_ago_pct - inp.current_win_rate_pct
        if decline_6m >= 0.08 and trajectory >= 15:
            return DecayPattern.gradual_erosion

        return DecayPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> DecayRisk:
        if composite >= 60:
            return DecayRisk.critical
        if composite >= 40:
            return DecayRisk.high
        if composite >= 20:
            return DecayRisk.moderate
        return DecayRisk.low

    def _severity(self, composite: float) -> DecaySeverity:
        if composite >= 60:
            return DecaySeverity.collapsing
        if composite >= 40:
            return DecaySeverity.declining
        if composite >= 20:
            return DecaySeverity.stable
        return DecaySeverity.improving

    def _action(self, risk: DecayRisk, pattern: DecayPattern) -> DecayAction:
        if risk == DecayRisk.critical:
            if pattern == DecayPattern.late_stage_collapse:
                return DecayAction.late_stage_process_coaching
            if pattern == DecayPattern.competitive_displacement:
                return DecayAction.competitive_positioning_review
            return DecayAction.urgent_pipeline_intervention
        if risk == DecayRisk.high:
            if pattern == DecayPattern.deal_size_inflation_trap:
                return DecayAction.deal_quality_audit
            if pattern == DecayPattern.sharp_cliff_drop:
                return DecayAction.win_loss_debrief_coaching
            return DecayAction.win_loss_debrief_coaching
        if risk == DecayRisk.moderate:
            return DecayAction.win_loss_debrief_coaching
        return DecayAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_decay_gap(self, composite: float, inp: DecayInput) -> bool:
        decline_6m = inp.win_rate_6m_ago_pct - inp.current_win_rate_pct
        return (
            composite >= 40
            or decline_6m >= 0.15
            or inp.current_win_rate_pct <= 0.25
        )

    def _requires_decay_coaching(self, composite: float, inp: DecayInput) -> bool:
        return (
            composite >= 30
            or inp.win_rate_decline_velocity_pct >= 0.08
            or inp.no_decision_rate_pct >= 0.25
        )

    # ------------------------------------------------------------------
    # Revenue decay estimate
    # ------------------------------------------------------------------

    def _estimated_revenue_decay(self, inp: DecayInput, composite: float) -> float:
        win_rate_gap = max(0.0, inp.win_rate_6m_ago_pct - inp.current_win_rate_pct)
        return round(
            inp.total_deals_evaluated
            * inp.avg_opportunity_value_usd
            * win_rate_gap
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: DecayInput,
                 pattern: DecayPattern, composite: float) -> str:
        if pattern == DecayPattern.none and composite < 20:
            return "Win rate stable — trajectory, competitive positioning, and late-stage conversion within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.current_win_rate_pct * 100:.0f}% current win rate")
        decline_6m = inp.win_rate_6m_ago_pct - inp.current_win_rate_pct
        parts.append(f"{decline_6m * 100:.0f}pp decline over 6m")
        parts.append(f"{inp.competitive_win_rate_pct * 100:.0f}% competitive win rate")
        label = pattern.value.replace("_", " ") if pattern != DecayPattern.none else "Win rate decay"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: DecayInput) -> DecayResult:
        trajectory   = round(self._trajectory_score(inp), 1)
        competitive  = round(self._competitive_score(inp), 1)
        deal_quality = round(self._deal_quality_score(inp), 1)
        late_stage   = round(self._late_stage_score(inp), 1)

        composite = round(
            trajectory * 0.35 + competitive * 0.25 + deal_quality * 0.20 + late_stage * 0.20, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, trajectory, competitive, deal_quality, late_stage)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_decay_gap(composite, inp)
        coach  = self._requires_decay_coaching(composite, inp)
        loss   = self._estimated_revenue_decay(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = DecayResult(
            rep_id=inp.rep_id,
            region=inp.region,
            decay_risk=risk,
            decay_pattern=pattern,
            decay_severity=severity,
            recommended_action=action,
            trajectory_score=trajectory,
            competitive_score=competitive,
            deal_quality_score=deal_quality,
            late_stage_score=late_stage,
            decay_composite=composite,
            has_decay_gap=gap,
            requires_decay_coaching=coach,
            estimated_revenue_decay_usd=loss,
            decay_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[DecayInput]) -> list[DecayResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_decay_composite": 0.0,
                "decay_gap_count": 0,
                "coaching_count": 0,
                "avg_trajectory_score": 0.0,
                "avg_competitive_score": 0.0,
                "avg_deal_quality_score": 0.0,
                "avg_late_stage_score": 0.0,
                "total_estimated_revenue_decay_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_tra = total_com = total_dq = total_ls = total_loss = 0.0

        for r in self._results:
            risk_counts[r.decay_risk.value]       = risk_counts.get(r.decay_risk.value, 0) + 1
            pattern_counts[r.decay_pattern.value] = pattern_counts.get(r.decay_pattern.value, 0) + 1
            severity_counts[r.decay_severity.value] = severity_counts.get(r.decay_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.decay_composite
            total_tra  += r.trajectory_score
            total_com  += r.competitive_score
            total_dq   += r.deal_quality_score
            total_ls   += r.late_stage_score
            total_loss += r.estimated_revenue_decay_usd

        n = len(self._results)

        return {
            "total":                                   n,
            "risk_counts":                             risk_counts,
            "pattern_counts":                          pattern_counts,
            "severity_counts":                         severity_counts,
            "action_counts":                           action_counts,
            "avg_decay_composite":                     round(total_comp / n, 1),
            "decay_gap_count":                         sum(1 for r in self._results if r.has_decay_gap),
            "coaching_count":                          sum(1 for r in self._results if r.requires_decay_coaching),
            "avg_trajectory_score":                    round(total_tra / n, 1),
            "avg_competitive_score":                   round(total_com / n, 1),
            "avg_deal_quality_score":                  round(total_dq / n, 1),
            "avg_late_stage_score":                    round(total_ls / n, 1),
            "total_estimated_revenue_decay_usd":       round(total_loss, 2),
        }
