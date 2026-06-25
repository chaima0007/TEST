from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class VelocityStatus(str, Enum):
    ACCELERATING    = "accelerating"
    ON_PACE         = "on_pace"
    DECELERATING    = "decelerating"
    STALLED         = "stalled"


class SlipRisk(str, Enum):
    LOW         = "low"
    MODERATE    = "moderate"
    HIGH        = "high"
    CRITICAL    = "critical"


class DealMomentum(str, Enum):
    STRONG      = "strong"
    BUILDING    = "building"
    FADING      = "fading"
    LOST        = "lost"


class VelocityAction(str, Enum):
    ACCELERATE      = "accelerate"
    MAINTAIN        = "maintain"
    INJECT_URGENCY  = "inject_urgency"
    RESCUE          = "rescue"


@dataclass
class DealVelocityInput:
    deal_id:                        str
    deal_name:                      str
    rep_id:                         str
    days_in_current_stage:          int     # days stuck in current stage
    avg_days_per_stage_historical:  float   # historical avg days per stage for rep/segment
    total_stages_completed:         int     # number of stages completed so far
    total_stages_in_pipeline:       int     # total stages in the pipeline
    meetings_last_30d:              int     # meetings held in last 30 days
    meetings_prior_30d:             int     # meetings held in prior 30 days
    docs_shared_last_30d:           int     # documents shared in last 30 days (proposals, decks)
    docs_opened_last_30d:           int     # documents opened by buyer in last 30 days
    stakeholder_count_current:      int     # current number of stakeholders engaged
    stakeholder_count_30d_ago:      int     # stakeholders engaged 30 days ago
    new_action_items_last_7d:       int     # new action items created in last 7 days
    action_items_completed_rate:    float   # % of action items completed on time (0-100)
    days_to_target_close:           int     # remaining days to target close date
    close_date_push_count:          int     # times close date has been pushed
    last_stage_advance_days_ago:    int     # days since last stage advance
    pipeline_value:                 float   # deal pipeline value ($)
    exec_involved:                  int     # 1 if executive is involved (speeds deals)
    deal_created_days_ago:          int     # total age of the deal
    deal_value:                     float


@dataclass
class DealVelocityResult:
    deal_id:                str
    deal_name:              str
    velocity_status:        VelocityStatus
    slip_risk:              SlipRisk
    deal_momentum:          DealMomentum
    velocity_action:        VelocityAction
    stage_progress_score:   float   # 0-100
    activity_velocity_score: float  # 0-100
    stakeholder_growth_score: float # 0-100
    urgency_score:          float   # 0-100
    velocity_composite:     float   # 0-100
    predicted_close_days:   int     # predicted days to close at current velocity
    slip_probability:       float   # 0-100
    is_on_track:            bool
    needs_velocity_boost:   bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                  self.deal_id,
            "deal_name":                self.deal_name,
            "velocity_status":          self.velocity_status.value,
            "slip_risk":                self.slip_risk.value,
            "deal_momentum":            self.deal_momentum.value,
            "velocity_action":          self.velocity_action.value,
            "stage_progress_score":     self.stage_progress_score,
            "activity_velocity_score":  self.activity_velocity_score,
            "stakeholder_growth_score": self.stakeholder_growth_score,
            "urgency_score":            self.urgency_score,
            "velocity_composite":       self.velocity_composite,
            "predicted_close_days":     self.predicted_close_days,
            "slip_probability":         self.slip_probability,
            "is_on_track":              self.is_on_track,
            "needs_velocity_boost":     self.needs_velocity_boost,
        }


class DealVelocityTracker:
    def __init__(self) -> None:
        self._results: list[DealVelocityResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def track(self, inp: DealVelocityInput) -> DealVelocityResult:
        stage_prog  = self._stage_progress_score(inp)
        activity    = self._activity_velocity_score(inp)
        stakeholder = self._stakeholder_growth_score(inp)
        urgency     = self._urgency_score(inp)
        composite   = self._composite(stage_prog, activity, stakeholder, urgency)
        status      = self._velocity_status(composite, inp)
        slip        = self._slip_risk(composite, inp)
        momentum    = self._deal_momentum(composite, inp)
        pred_close  = self._predicted_close_days(inp, composite)
        slip_prob   = self._slip_probability(inp, composite)
        is_on_track = composite >= 55.0 and inp.close_date_push_count <= 1
        needs_boost = composite < 40.0 or inp.days_in_current_stage > inp.avg_days_per_stage_historical * 2
        action      = self._velocity_action(status, needs_boost, composite)

        result = DealVelocityResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            velocity_status=status,
            slip_risk=slip,
            deal_momentum=momentum,
            velocity_action=action,
            stage_progress_score=stage_prog,
            activity_velocity_score=activity,
            stakeholder_growth_score=stakeholder,
            urgency_score=urgency,
            velocity_composite=composite,
            predicted_close_days=pred_close,
            slip_probability=slip_prob,
            is_on_track=is_on_track,
            needs_velocity_boost=needs_boost,
        )
        self._results.append(result)
        return result

    def track_batch(self, inputs: list[DealVelocityInput]) -> list[DealVelocityResult]:
        return [self.track(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def on_track_deals(self) -> list[DealVelocityResult]:
        return [r for r in self._results if r.is_on_track]

    @property
    def velocity_boost_queue(self) -> list[DealVelocityResult]:
        return [r for r in self._results if r.needs_velocity_boost]

    @property
    def avg_velocity_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.velocity_composite for r in self._results) / len(self._results), 1)

    @property
    def avg_slip_probability(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.slip_probability for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _stage_progress_score(self, inp: DealVelocityInput) -> float:
        score = 0.0
        # Pipeline completion %
        if inp.total_stages_in_pipeline > 0:
            pct = inp.total_stages_completed / inp.total_stages_in_pipeline
            score += pct * 40.0
        # Days in current stage vs historical
        if inp.avg_days_per_stage_historical > 0:
            stage_ratio = inp.days_in_current_stage / inp.avg_days_per_stage_historical
            if stage_ratio <= 0.5:
                score += 30.0  # moving faster than average
            elif stage_ratio <= 1.0:
                score += 20.0  # on pace
            elif stage_ratio <= 1.5:
                score += 5.0   # slightly slow
            # > 1.5x means stuck
        # Last stage advance
        adv = inp.last_stage_advance_days_ago
        if adv <= 7:
            score += 20.0
        elif adv <= 14:
            score += 12.0
        elif adv <= 30:
            score += 5.0
        # Close date stability
        if inp.close_date_push_count == 0:
            score += 10.0
        elif inp.close_date_push_count == 1:
            score += 5.0
        elif inp.close_date_push_count >= 3:
            score -= 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _activity_velocity_score(self, inp: DealVelocityInput) -> float:
        score = 0.0
        # Meeting velocity
        if inp.meetings_prior_30d > 0:
            mtg_ratio = inp.meetings_last_30d / inp.meetings_prior_30d
        else:
            mtg_ratio = 1.0 if inp.meetings_last_30d == 0 else 2.0
        if mtg_ratio >= 1.5:
            score += 25.0
        elif mtg_ratio >= 1.0:
            score += 15.0
        elif mtg_ratio >= 0.7:
            score += 8.0
        # Meeting count absolute
        if inp.meetings_last_30d >= 4:
            score += 20.0
        elif inp.meetings_last_30d >= 2:
            score += 12.0
        elif inp.meetings_last_30d >= 1:
            score += 5.0
        # Document activity
        if inp.docs_opened_last_30d >= 3:
            score += 20.0
        elif inp.docs_opened_last_30d >= 1:
            score += 10.0
        # Action item completion
        completion = inp.action_items_completed_rate
        if completion >= 80:
            score += 20.0
        elif completion >= 60:
            score += 12.0
        elif completion >= 40:
            score += 5.0
        # New action items = deal is active
        if inp.new_action_items_last_7d >= 3:
            score += 10.0
        elif inp.new_action_items_last_7d >= 1:
            score += 5.0
        return round(max(0.0, min(100.0, score)), 1)

    def _stakeholder_growth_score(self, inp: DealVelocityInput) -> float:
        score = 50.0  # neutral base
        # Stakeholder growth/shrinkage
        growth = inp.stakeholder_count_current - inp.stakeholder_count_30d_ago
        if growth >= 2:
            score += 30.0
        elif growth == 1:
            score += 15.0
        elif growth == -1:
            score -= 15.0
        elif growth <= -2:
            score -= 30.0
        # Absolute count
        if inp.stakeholder_count_current >= 5:
            score += 10.0
        elif inp.stakeholder_count_current >= 3:
            score += 5.0
        # Exec involvement
        if inp.exec_involved:
            score = min(100.0, score + 10.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _urgency_score(self, inp: DealVelocityInput) -> float:
        score = 0.0
        # Days to close (proximity = urgency)
        days_left = inp.days_to_target_close
        if days_left <= 7:
            score += 50.0
        elif days_left <= 14:
            score += 35.0
        elif days_left <= 30:
            score += 20.0
        elif days_left <= 60:
            score += 10.0
        # Deal value weight
        if inp.deal_value >= 500_000:
            score += 20.0
        elif inp.deal_value >= 200_000:
            score += 12.0
        elif inp.deal_value >= 100_000:
            score += 6.0
        # Exec involved accelerates urgency
        if inp.exec_involved:
            score = min(100.0, score + 15.0)
        # Push count signals inability to create urgency
        if inp.close_date_push_count >= 3:
            score -= 15.0
        elif inp.close_date_push_count >= 2:
            score -= 8.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        stage: float,
        activity: float,
        stakeholder: float,
        urgency: float,
    ) -> float:
        composite = stage * 0.30 + activity * 0.35 + stakeholder * 0.20 + urgency * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _velocity_status(self, composite: float, inp: DealVelocityInput) -> VelocityStatus:
        if composite >= 70 and inp.last_stage_advance_days_ago <= 7:
            return VelocityStatus.ACCELERATING
        if composite >= 50:
            return VelocityStatus.ON_PACE
        if composite >= 30:
            return VelocityStatus.DECELERATING
        return VelocityStatus.STALLED

    def _slip_risk(self, composite: float, inp: DealVelocityInput) -> SlipRisk:
        risk_score = 100.0 - composite
        if inp.close_date_push_count >= 2:
            risk_score = min(100.0, risk_score + 15.0)
        if inp.days_in_current_stage > inp.avg_days_per_stage_historical * 2:
            risk_score = min(100.0, risk_score + 10.0)
        if risk_score >= 70:
            return SlipRisk.CRITICAL
        if risk_score >= 50:
            return SlipRisk.HIGH
        if risk_score >= 30:
            return SlipRisk.MODERATE
        return SlipRisk.LOW

    def _deal_momentum(self, composite: float, inp: DealVelocityInput) -> DealMomentum:
        if composite >= 70:
            return DealMomentum.STRONG
        if composite >= 50:
            return DealMomentum.BUILDING
        if composite >= 30:
            return DealMomentum.FADING
        return DealMomentum.LOST

    def _predicted_close_days(self, inp: DealVelocityInput, composite: float) -> int:
        stages_remaining = max(0, inp.total_stages_in_pipeline - inp.total_stages_completed)
        if composite >= 70:
            days_per_stage = inp.avg_days_per_stage_historical * 0.7
        elif composite >= 50:
            days_per_stage = inp.avg_days_per_stage_historical
        elif composite >= 30:
            days_per_stage = inp.avg_days_per_stage_historical * 1.5
        else:
            days_per_stage = inp.avg_days_per_stage_historical * 2.0
        predicted = int(stages_remaining * days_per_stage)
        return max(1, predicted)

    def _slip_probability(self, inp: DealVelocityInput, composite: float) -> float:
        base = max(0.0, 100.0 - composite)
        # Each close date push adds risk
        base = min(100.0, base + inp.close_date_push_count * 8.0)
        # Stage stuck too long
        if inp.avg_days_per_stage_historical > 0:
            if inp.days_in_current_stage > inp.avg_days_per_stage_historical * 2:
                base = min(100.0, base + 15.0)
        # Exec involvement reduces slip risk
        if inp.exec_involved:
            base -= 10.0
        return round(max(0.0, min(100.0, base)), 1)

    def _velocity_action(
        self,
        status: VelocityStatus,
        needs_boost: bool,
        composite: float,
    ) -> VelocityAction:
        if needs_boost or status == VelocityStatus.STALLED:
            return VelocityAction.RESCUE
        if status == VelocityStatus.DECELERATING:
            return VelocityAction.INJECT_URGENCY
        if status == VelocityStatus.ON_PACE:
            return VelocityAction.MAINTAIN
        return VelocityAction.ACCELERATE

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "status_counts":                {},
                "slip_risk_counts":             {},
                "momentum_counts":              {},
                "action_counts":                {},
                "avg_velocity_composite":       0.0,
                "avg_slip_probability":         0.0,
                "on_track_count":               0,
                "velocity_boost_count":         0,
                "avg_stage_progress_score":     0.0,
                "avg_activity_velocity_score":  0.0,
                "avg_stakeholder_growth_score": 0.0,
                "avg_urgency_score":            0.0,
            }

        status_counts:    dict[str, int] = {}
        slip_risk_counts: dict[str, int] = {}
        momentum_counts:  dict[str, int] = {}
        action_counts:    dict[str, int] = {}
        total_comp  = 0.0
        total_slip  = 0.0
        total_stage = 0.0
        total_act   = 0.0
        total_stak  = 0.0
        total_urg   = 0.0

        for r in self._results:
            status_counts[r.velocity_status.value]      = status_counts.get(r.velocity_status.value, 0) + 1
            slip_risk_counts[r.slip_risk.value]          = slip_risk_counts.get(r.slip_risk.value, 0) + 1
            momentum_counts[r.deal_momentum.value]       = momentum_counts.get(r.deal_momentum.value, 0) + 1
            action_counts[r.velocity_action.value]       = action_counts.get(r.velocity_action.value, 0) + 1
            total_comp  += r.velocity_composite
            total_slip  += r.slip_probability
            total_stage += r.stage_progress_score
            total_act   += r.activity_velocity_score
            total_stak  += r.stakeholder_growth_score
            total_urg   += r.urgency_score

        return {
            "total":                        n,
            "status_counts":                status_counts,
            "slip_risk_counts":             slip_risk_counts,
            "momentum_counts":              momentum_counts,
            "action_counts":                action_counts,
            "avg_velocity_composite":       round(total_comp / n, 1),
            "avg_slip_probability":         round(total_slip / n, 1),
            "on_track_count":               len(self.on_track_deals),
            "velocity_boost_count":         len(self.velocity_boost_queue),
            "avg_stage_progress_score":     round(total_stage / n, 1),
            "avg_activity_velocity_score":  round(total_act / n, 1),
            "avg_stakeholder_growth_score": round(total_stak / n, 1),
            "avg_urgency_score":            round(total_urg / n, 1),
        }
