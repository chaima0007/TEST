from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class VelocityTrend(str, Enum):
    ACCELERATING  = "accelerating"
    STABLE        = "stable"
    DECELERATING  = "decelerating"
    STALLED       = "stalled"


class StageHealth(str, Enum):
    HEALTHY  = "healthy"
    SLOW     = "slow"
    STUCK    = "stuck"
    CRITICAL = "critical"


class DealOutcome(str, Enum):
    LIKELY_CLOSE = "likely_close"
    ON_TRACK     = "on_track"
    AT_RISK      = "at_risk"
    LIKELY_SLIP  = "likely_slip"
    LIKELY_LOSE  = "likely_lose"


class VelocityAction(str, Enum):
    STANDARD_FOLLOW_UP   = "standard_follow_up"
    PRIORITIZE           = "prioritize"
    ACCELERATE           = "accelerate"
    ENGAGE_EXECUTIVE     = "engage_executive"
    REASSIGN             = "reassign"
    CLOSE_LOST           = "close_lost"


@dataclass
class DealVelocityInput:
    deal_id:                   str
    deal_name:                 str
    rep_id:                    str
    account_id:                str
    stage_number:              int      # 1–5
    deal_value:                float
    probability_pct:           float    # 0–100
    expected_close_days:       int      # days until expected close
    created_days_ago:          int      # deal age in days
    days_in_current_stage:     int
    avg_days_per_stage:        float    # historical avg per stage
    last_activity_days_ago:    int
    num_stakeholders_engaged:  int
    decision_maker_engaged:    bool
    champion_identified:       bool
    competitor_present:        bool
    pricing_discussed:         bool
    legal_review_started:      bool
    close_date_changes:        int      # # times close date pushed out
    win_rate_similar_deals:    float    # historical win rate 0–100
    nrr_expansion_potential:   float    # upsell/expansion value if closed


@dataclass
class DealVelocityResult:
    deal_id:               str
    deal_name:             str
    rep_id:                str
    velocity_trend:        VelocityTrend
    stage_health:          StageHealth
    deal_outcome:          DealOutcome
    velocity_action:       VelocityAction
    velocity_score:        float    # 0–100
    stage_progression_rate: float   # ratio: avg/actual (>1 = faster than avg)
    close_date_risk:       float    # 0–100
    engagement_score:      float    # 0–100
    momentum_score:        float    # 0–100
    deal_health_index:     float    # 0–100 composite
    is_at_risk:            bool
    needs_escalation:      bool

    def to_dict(self) -> dict:
        return {
            "deal_id":               self.deal_id,
            "deal_name":             self.deal_name,
            "rep_id":                self.rep_id,
            "velocity_trend":        self.velocity_trend.value,
            "stage_health":          self.stage_health.value,
            "deal_outcome":          self.deal_outcome.value,
            "velocity_action":       self.velocity_action.value,
            "velocity_score":        self.velocity_score,
            "stage_progression_rate": self.stage_progression_rate,
            "close_date_risk":       self.close_date_risk,
            "engagement_score":      self.engagement_score,
            "momentum_score":        self.momentum_score,
            "deal_health_index":     self.deal_health_index,
            "is_at_risk":            self.is_at_risk,
            "needs_escalation":      self.needs_escalation,
        }


class DealVelocityEngine:
    def __init__(self) -> None:
        self._results: list[DealVelocityResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: DealVelocityInput) -> DealVelocityResult:
        progression   = self._stage_progression_rate(inp)
        engagement    = self._engagement_score(inp)
        velocity      = self._velocity_score(inp, progression)
        close_risk    = self._close_date_risk(inp, progression)
        momentum      = self._momentum_score(inp, progression, engagement)
        health        = self._deal_health_index(velocity, engagement, momentum)
        trend         = self._velocity_trend(inp, progression)
        stage_hlth    = self._stage_health(inp, progression)
        outcome       = self._deal_outcome(inp, health, close_risk)
        action        = self._velocity_action(inp, outcome, stage_hlth, health)
        at_risk       = health < 40.0 or close_risk > 70.0
        escalation    = stage_hlth == StageHealth.CRITICAL or outcome == DealOutcome.LIKELY_LOSE

        result = DealVelocityResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            rep_id=inp.rep_id,
            velocity_trend=trend,
            stage_health=stage_hlth,
            deal_outcome=outcome,
            velocity_action=action,
            velocity_score=velocity,
            stage_progression_rate=progression,
            close_date_risk=close_risk,
            engagement_score=engagement,
            momentum_score=momentum,
            deal_health_index=health,
            is_at_risk=at_risk,
            needs_escalation=escalation,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[DealVelocityInput]
    ) -> list[DealVelocityResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def at_risk_deals(self) -> list[DealVelocityResult]:
        return [r for r in self._results if r.is_at_risk]

    @property
    def escalation_deals(self) -> list[DealVelocityResult]:
        return [r for r in self._results if r.needs_escalation]

    @property
    def healthy_deals(self) -> list[DealVelocityResult]:
        return [r for r in self._results if r.deal_health_index >= 65.0]

    @property
    def total_pipeline_value(self) -> float:
        return round(sum(r.deal_health_index for r in self._results), 2)

    @property
    def avg_deal_health(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.deal_health_index for r in self._results) / len(self._results), 1)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _stage_progression_rate(self, inp: DealVelocityInput) -> float:
        if inp.days_in_current_stage <= 0 or inp.avg_days_per_stage <= 0:
            return 1.0
        rate = inp.avg_days_per_stage / inp.days_in_current_stage
        return round(max(0.1, min(5.0, rate)), 2)

    def _engagement_score(self, inp: DealVelocityInput) -> float:
        score = 0.0
        # Stakeholder breadth (up to 30)
        score += min(30.0, inp.num_stakeholders_engaged * 10.0)
        # Key role presence (up to 40)
        if inp.decision_maker_engaged:
            score += 20.0
        if inp.champion_identified:
            score += 20.0
        # Deal progression signals (up to 30)
        if inp.pricing_discussed:
            score += 15.0
        if inp.legal_review_started:
            score += 15.0
        return round(max(0.0, min(100.0, score)), 1)

    def _velocity_score(self, inp: DealVelocityInput, progression: float) -> float:
        score = 0.0
        # Progression speed (up to 40)
        score += min(40.0, progression * 20.0)
        # Activity recency (up to 35)
        if inp.last_activity_days_ago == 0:
            score += 35.0
        elif inp.last_activity_days_ago <= 3:
            score += 30.0
        elif inp.last_activity_days_ago <= 7:
            score += 20.0
        elif inp.last_activity_days_ago <= 14:
            score += 10.0
        else:
            score += max(0.0, 10.0 - (inp.last_activity_days_ago - 14) * 0.5)
        # Close date stability (up to 25)
        slip_penalty = min(25.0, inp.close_date_changes * 8.0)
        score += max(0.0, 25.0 - slip_penalty)
        return round(max(0.0, min(100.0, score)), 1)

    def _close_date_risk(self, inp: DealVelocityInput, progression: float) -> float:
        risk = 0.0
        # Slow progression increases risk (up to 40)
        if progression < 0.5:
            risk += 40.0
        elif progression < 0.8:
            risk += 25.0
        elif progression < 1.0:
            risk += 10.0
        # Prior slippage history (up to 30)
        risk += min(30.0, inp.close_date_changes * 10.0)
        # Urgency based on expected close (up to 20)
        if inp.expected_close_days < 0:
            risk += 20.0
        elif inp.expected_close_days <= 7:
            risk += 10.0
        # Competitive risk (up to 10)
        if inp.competitor_present and not inp.decision_maker_engaged:
            risk += 10.0
        return round(max(0.0, min(100.0, risk)), 1)

    def _momentum_score(
        self, inp: DealVelocityInput, progression: float, engagement: float
    ) -> float:
        # Weighted blend of progression, engagement, activity freshness
        prog_component = min(40.0, progression * 20.0)
        eng_component  = engagement * 0.35
        activity_score = max(0.0, 25.0 - inp.last_activity_days_ago * 1.5)
        base = prog_component + eng_component + activity_score
        # Win rate boost/penalty
        win_factor = (inp.win_rate_similar_deals - 50.0) / 50.0 * 10.0
        return round(max(0.0, min(100.0, base + win_factor)), 1)

    def _deal_health_index(
        self, velocity: float, engagement: float, momentum: float
    ) -> float:
        health = velocity * 0.35 + engagement * 0.30 + momentum * 0.35
        return round(max(0.0, min(100.0, health)), 1)

    def _velocity_trend(
        self, inp: DealVelocityInput, progression: float
    ) -> VelocityTrend:
        if progression >= 1.5 and inp.last_activity_days_ago <= 3:
            return VelocityTrend.ACCELERATING
        if inp.last_activity_days_ago > 21 or progression < 0.3:
            return VelocityTrend.STALLED
        if progression < 0.7 or inp.last_activity_days_ago > 10:
            return VelocityTrend.DECELERATING
        return VelocityTrend.STABLE

    def _stage_health(
        self, inp: DealVelocityInput, progression: float
    ) -> StageHealth:
        if progression >= 1.2:
            return StageHealth.HEALTHY
        if progression >= 0.8:
            return StageHealth.SLOW
        if inp.days_in_current_stage > inp.avg_days_per_stage * 2.5:
            return StageHealth.CRITICAL
        return StageHealth.STUCK

    def _deal_outcome(
        self, inp: DealVelocityInput, health: float, close_risk: float
    ) -> DealOutcome:
        if health >= 70.0 and close_risk <= 20.0 and inp.probability_pct >= 70.0:
            return DealOutcome.LIKELY_CLOSE
        if health < 25.0 or (inp.competitor_present and not inp.champion_identified and inp.probability_pct < 30.0):
            return DealOutcome.LIKELY_LOSE
        if close_risk >= 60.0 or (inp.close_date_changes >= 3 and health < 50.0):
            return DealOutcome.LIKELY_SLIP
        if health >= 50.0 and close_risk <= 40.0:
            return DealOutcome.ON_TRACK
        return DealOutcome.AT_RISK

    def _velocity_action(
        self,
        inp: DealVelocityInput,
        outcome: DealOutcome,
        stage_health: StageHealth,
        health: float,
    ) -> VelocityAction:
        if outcome == DealOutcome.LIKELY_LOSE and health < 20.0:
            return VelocityAction.CLOSE_LOST
        if stage_health == StageHealth.CRITICAL or outcome == DealOutcome.LIKELY_LOSE:
            return VelocityAction.ENGAGE_EXECUTIVE
        if outcome == DealOutcome.LIKELY_SLIP:
            return VelocityAction.REASSIGN if health < 35.0 else VelocityAction.ACCELERATE
        if outcome == DealOutcome.AT_RISK:
            return VelocityAction.PRIORITIZE
        if outcome == DealOutcome.LIKELY_CLOSE:
            return VelocityAction.ACCELERATE
        return VelocityAction.STANDARD_FOLLOW_UP

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                 0,
                "trend_counts":          {},
                "health_counts":         {},
                "outcome_counts":        {},
                "action_counts":         {},
                "avg_velocity_score":    0.0,
                "avg_deal_health_index": 0.0,
                "avg_close_date_risk":   0.0,
                "at_risk_count":         0,
                "escalation_count":      0,
                "avg_engagement_score":  0.0,
                "avg_momentum_score":    0.0,
                "healthy_deal_count":    0,
            }

        trend_counts:   dict[str, int] = {}
        health_counts:  dict[str, int] = {}
        outcome_counts: dict[str, int] = {}
        action_counts:  dict[str, int] = {}
        total_velocity   = 0.0
        total_health_idx = 0.0
        total_close_risk = 0.0
        total_engagement = 0.0
        total_momentum   = 0.0

        for r in self._results:
            trend_counts[r.velocity_trend.value]   = trend_counts.get(r.velocity_trend.value, 0) + 1
            health_counts[r.stage_health.value]    = health_counts.get(r.stage_health.value, 0) + 1
            outcome_counts[r.deal_outcome.value]   = outcome_counts.get(r.deal_outcome.value, 0) + 1
            action_counts[r.velocity_action.value] = action_counts.get(r.velocity_action.value, 0) + 1
            total_velocity   += r.velocity_score
            total_health_idx += r.deal_health_index
            total_close_risk += r.close_date_risk
            total_engagement += r.engagement_score
            total_momentum   += r.momentum_score

        return {
            "total":                 n,
            "trend_counts":          trend_counts,
            "health_counts":         health_counts,
            "outcome_counts":        outcome_counts,
            "action_counts":         action_counts,
            "avg_velocity_score":    round(total_velocity / n, 1),
            "avg_deal_health_index": round(total_health_idx / n, 1),
            "avg_close_date_risk":   round(total_close_risk / n, 1),
            "at_risk_count":         len(self.at_risk_deals),
            "escalation_count":      len(self.escalation_deals),
            "avg_engagement_score":  round(total_engagement / n, 1),
            "avg_momentum_score":    round(total_momentum / n, 1),
            "healthy_deal_count":    len(self.healthy_deals),
        }
