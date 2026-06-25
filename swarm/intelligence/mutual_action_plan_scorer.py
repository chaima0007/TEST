from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MAPHealth(str, Enum):
    ON_TRACK   = "on_track"
    SLIPPING   = "slipping"
    AT_RISK    = "at_risk"
    BROKEN     = "broken"


class AdherencePattern(str, Enum):
    BOTH_COMMITTED     = "both_committed"
    REP_ONLY           = "rep_only"
    BUYER_LEADING      = "buyer_leading"
    BUYER_GHOSTING     = "buyer_ghosting"
    MUTUAL_DRIFT       = "mutual_drift"
    COMPLETE_BREAKDOWN = "complete_breakdown"


class CommitmentSignal(str, Enum):
    STRONG   = "strong"
    MODERATE = "moderate"
    WEAK     = "weak"
    ABSENT   = "absent"


class MAPAction(str, Enum):
    ACCELERATE  = "accelerate"
    REAFFIRM    = "reaffirm"
    RESET_MAP   = "reset_map"
    ESCALATE    = "escalate"


@dataclass
class MutualActionPlanInput:
    deal_id:                        str
    deal_name:                      str
    rep_id:                         str
    map_start_date_days_ago:        int     # how many days since MAP was agreed
    total_milestones:               int     # total milestones defined in MAP
    rep_milestones_completed:       int     # milestones rep completed on time
    rep_milestones_missed:          int     # milestones rep missed/late
    buyer_milestones_completed:     int     # milestones buyer completed on time
    buyer_milestones_missed:        int     # milestones buyer missed/late
    buyer_response_time_avg_hours:  float   # average hours buyer takes to respond to rep actions
    map_last_reviewed_days_ago:     int     # days since MAP was last reviewed with buyer
    close_date_agreed_in_map:       int     # 1 if close date was explicitly agreed in MAP
    close_date_changes_since_map:   int     # number of close date changes after MAP signed
    legal_milestone_in_map:         int     # 1 if legal/procurement milestone included
    legal_milestone_completed:      int     # 1 if legal milestone was completed on time
    technical_milestone_in_map:     int     # 1 if technical validation milestone included
    technical_milestone_completed:  int     # 1 if technical milestone was completed
    executive_sign_off_milestone:   int     # 1 if exec sign-off milestone is in MAP
    executive_sign_off_done:        int     # 1 if exec sign-off milestone completed
    mutual_success_criteria_defined: int    # 1 if success criteria were written and agreed
    buyer_shared_map_internally:    int     # 1 if buyer shared MAP internally (strong signal)
    deal_value:                     float


@dataclass
class MAPAdherenceResult:
    deal_id:                    str
    deal_name:                  str
    map_health:                 MAPHealth
    adherence_pattern:          AdherencePattern
    commitment_signal:          CommitmentSignal
    map_action:                 MAPAction
    rep_adherence_score:        float   # 0-100
    buyer_adherence_score:      float   # 0-100
    milestone_progress_score:   float   # 0-100
    map_quality_score:          float   # 0-100
    map_adherence_composite:    float   # 0-100
    estimated_close_confidence: float   # 0-100
    days_to_close_risk:         int     # estimated slippage days if current trend continues
    is_healthy_map:             bool
    needs_map_reset:            bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                    self.deal_id,
            "deal_name":                  self.deal_name,
            "map_health":                 self.map_health.value,
            "adherence_pattern":          self.adherence_pattern.value,
            "commitment_signal":          self.commitment_signal.value,
            "map_action":                 self.map_action.value,
            "rep_adherence_score":        self.rep_adherence_score,
            "buyer_adherence_score":      self.buyer_adherence_score,
            "milestone_progress_score":   self.milestone_progress_score,
            "map_quality_score":          self.map_quality_score,
            "map_adherence_composite":    self.map_adherence_composite,
            "estimated_close_confidence": self.estimated_close_confidence,
            "days_to_close_risk":         self.days_to_close_risk,
            "is_healthy_map":             self.is_healthy_map,
            "needs_map_reset":            self.needs_map_reset,
        }


class MutualActionPlanScorer:
    def __init__(self) -> None:
        self._results: list[MAPAdherenceResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def score(self, inp: MutualActionPlanInput) -> MAPAdherenceResult:
        rep_adh  = self._rep_adherence_score(inp)
        buyer_adh = self._buyer_adherence_score(inp)
        milestone = self._milestone_progress_score(inp)
        quality  = self._map_quality_score(inp)
        composite = self._composite(rep_adh, buyer_adh, milestone, quality)
        health   = self._map_health(composite)
        pattern  = self._adherence_pattern(rep_adh, buyer_adh, inp)
        signal   = self._commitment_signal(buyer_adh, composite, inp)
        close_conf = self._estimated_close_confidence(inp, composite)
        days_risk  = self._days_to_close_risk(inp, composite)
        is_healthy = composite >= 65.0
        needs_reset = composite < 35.0 or inp.buyer_milestones_missed >= 3
        action   = self._map_action(health, needs_reset, composite)

        result = MAPAdherenceResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            map_health=health,
            adherence_pattern=pattern,
            commitment_signal=signal,
            map_action=action,
            rep_adherence_score=rep_adh,
            buyer_adherence_score=buyer_adh,
            milestone_progress_score=milestone,
            map_quality_score=quality,
            map_adherence_composite=composite,
            estimated_close_confidence=close_conf,
            days_to_close_risk=days_risk,
            is_healthy_map=is_healthy,
            needs_map_reset=needs_reset,
        )
        self._results.append(result)
        return result

    def score_batch(self, inputs: list[MutualActionPlanInput]) -> list[MAPAdherenceResult]:
        return [self.score(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def healthy_maps(self) -> list[MAPAdherenceResult]:
        return [r for r in self._results if r.is_healthy_map]

    @property
    def maps_needing_reset(self) -> list[MAPAdherenceResult]:
        return [r for r in self._results if r.needs_map_reset]

    @property
    def avg_close_confidence(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.estimated_close_confidence for r in self._results) / len(self._results), 1)

    @property
    def avg_map_adherence_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.map_adherence_composite for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _rep_adherence_score(self, inp: MutualActionPlanInput) -> float:
        total = inp.rep_milestones_completed + inp.rep_milestones_missed
        if total == 0:
            return 50.0  # no data yet
        completion_rate = inp.rep_milestones_completed / total
        score = completion_rate * 80.0
        # Bonus for perfect completion
        if inp.rep_milestones_missed == 0 and inp.rep_milestones_completed >= 2:
            score += 20.0
        # MAP reviewed recently
        if inp.map_last_reviewed_days_ago <= 7:
            score = min(100.0, score + 10.0)
        elif inp.map_last_reviewed_days_ago >= 30:
            score -= 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _buyer_adherence_score(self, inp: MutualActionPlanInput) -> float:
        total = inp.buyer_milestones_completed + inp.buyer_milestones_missed
        if total == 0:
            return 40.0  # assume below neutral if buyer hasn't engaged milestones
        completion_rate = inp.buyer_milestones_completed / total
        score = completion_rate * 70.0
        # Buyer shared MAP internally = huge commitment signal
        if inp.buyer_shared_map_internally:
            score += 20.0
        # Fast response time = engaged buyer
        resp = inp.buyer_response_time_avg_hours
        if resp <= 4:
            score = min(100.0, score + 10.0)
        elif resp >= 48:
            score -= 15.0
        elif resp >= 24:
            score -= 8.0
        return round(max(0.0, min(100.0, score)), 1)

    def _milestone_progress_score(self, inp: MutualActionPlanInput) -> float:
        if inp.total_milestones == 0:
            return 20.0
        total_completed = inp.rep_milestones_completed + inp.buyer_milestones_completed
        total_milestones = inp.total_milestones
        completion_pct = min(1.0, total_completed / total_milestones)
        score = completion_pct * 60.0
        # Critical milestones bonus
        if inp.legal_milestone_in_map and inp.legal_milestone_completed:
            score += 15.0
        elif inp.legal_milestone_in_map and not inp.legal_milestone_completed:
            score -= 5.0
        if inp.technical_milestone_in_map and inp.technical_milestone_completed:
            score += 12.0
        if inp.executive_sign_off_milestone and inp.executive_sign_off_done:
            score += 13.0
        # Close date changes = milestone drift
        score -= min(20.0, inp.close_date_changes_since_map * 7.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _map_quality_score(self, inp: MutualActionPlanInput) -> float:
        score = 30.0
        if inp.close_date_agreed_in_map:
            score += 20.0
        if inp.mutual_success_criteria_defined:
            score += 20.0
        if inp.legal_milestone_in_map:
            score += 10.0
        if inp.technical_milestone_in_map:
            score += 10.0
        if inp.executive_sign_off_milestone:
            score += 10.0
        # MAP stale penalty
        if inp.map_last_reviewed_days_ago >= 21:
            score -= 15.0
        elif inp.map_last_reviewed_days_ago >= 14:
            score -= 7.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        rep: float,
        buyer: float,
        milestone: float,
        quality: float,
    ) -> float:
        composite = rep * 0.25 + buyer * 0.35 + milestone * 0.25 + quality * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _map_health(self, composite: float) -> MAPHealth:
        if composite >= 65:
            return MAPHealth.ON_TRACK
        if composite >= 45:
            return MAPHealth.SLIPPING
        if composite >= 25:
            return MAPHealth.AT_RISK
        return MAPHealth.BROKEN

    def _adherence_pattern(
        self,
        rep: float,
        buyer: float,
        inp: MutualActionPlanInput,
    ) -> AdherencePattern:
        if inp.buyer_milestones_missed >= 3 and rep >= 70:
            return AdherencePattern.BUYER_GHOSTING
        if rep < 30 and buyer < 30:
            return AdherencePattern.COMPLETE_BREAKDOWN
        if rep < 40 and buyer < 40:
            return AdherencePattern.MUTUAL_DRIFT
        if buyer >= 70 and rep < 50:
            return AdherencePattern.BUYER_LEADING
        if rep >= 70 and buyer < 50:
            return AdherencePattern.REP_ONLY
        if rep >= 65 and buyer >= 65:
            return AdherencePattern.BOTH_COMMITTED
        return AdherencePattern.MUTUAL_DRIFT

    def _commitment_signal(
        self,
        buyer: float,
        composite: float,
        inp: MutualActionPlanInput,
    ) -> CommitmentSignal:
        if buyer >= 70 and inp.buyer_shared_map_internally:
            return CommitmentSignal.STRONG
        if buyer >= 55 and composite >= 55:
            return CommitmentSignal.MODERATE
        if buyer >= 40:
            return CommitmentSignal.WEAK
        return CommitmentSignal.ABSENT

    def _estimated_close_confidence(self, inp: MutualActionPlanInput, composite: float) -> float:
        base = composite
        if inp.close_date_agreed_in_map:
            base = min(100.0, base + 10.0)
        if inp.buyer_shared_map_internally:
            base = min(100.0, base + 12.0)
        if inp.mutual_success_criteria_defined:
            base = min(100.0, base + 8.0)
        base -= inp.close_date_changes_since_map * 8.0
        return round(max(0.0, min(100.0, base)), 1)

    def _days_to_close_risk(self, inp: MutualActionPlanInput, composite: float) -> int:
        if composite >= 75:
            return 0
        if composite >= 55:
            return inp.close_date_changes_since_map * 14
        if composite >= 35:
            return inp.close_date_changes_since_map * 21 + 14
        return inp.close_date_changes_since_map * 30 + 30

    def _map_action(
        self,
        health: MAPHealth,
        needs_reset: bool,
        composite: float,
    ) -> MAPAction:
        if needs_reset or health == MAPHealth.BROKEN:
            return MAPAction.ESCALATE
        if health == MAPHealth.AT_RISK:
            return MAPAction.RESET_MAP
        if health == MAPHealth.SLIPPING:
            return MAPAction.REAFFIRM
        return MAPAction.ACCELERATE

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "health_counts":                {},
                "pattern_counts":               {},
                "signal_counts":                {},
                "action_counts":                {},
                "avg_map_adherence_composite":  0.0,
                "avg_close_confidence":         0.0,
                "healthy_map_count":            0,
                "reset_needed_count":           0,
                "avg_rep_adherence_score":      0.0,
                "avg_buyer_adherence_score":    0.0,
                "avg_milestone_progress_score": 0.0,
                "avg_map_quality_score":        0.0,
            }

        health_counts:  dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        signal_counts:  dict[str, int] = {}
        action_counts:  dict[str, int] = {}
        total_comp = 0.0
        total_conf = 0.0
        total_rep  = 0.0
        total_buy  = 0.0
        total_mile = 0.0
        total_qual = 0.0

        for r in self._results:
            health_counts[r.map_health.value]       = health_counts.get(r.map_health.value, 0) + 1
            pattern_counts[r.adherence_pattern.value] = pattern_counts.get(r.adherence_pattern.value, 0) + 1
            signal_counts[r.commitment_signal.value] = signal_counts.get(r.commitment_signal.value, 0) + 1
            action_counts[r.map_action.value]        = action_counts.get(r.map_action.value, 0) + 1
            total_comp += r.map_adherence_composite
            total_conf += r.estimated_close_confidence
            total_rep  += r.rep_adherence_score
            total_buy  += r.buyer_adherence_score
            total_mile += r.milestone_progress_score
            total_qual += r.map_quality_score

        return {
            "total":                        n,
            "health_counts":                health_counts,
            "pattern_counts":               pattern_counts,
            "signal_counts":                signal_counts,
            "action_counts":                action_counts,
            "avg_map_adherence_composite":  round(total_comp / n, 1),
            "avg_close_confidence":         round(total_conf / n, 1),
            "healthy_map_count":            len(self.healthy_maps),
            "reset_needed_count":           len(self.maps_needing_reset),
            "avg_rep_adherence_score":      round(total_rep / n, 1),
            "avg_buyer_adherence_score":    round(total_buy / n, 1),
            "avg_milestone_progress_score": round(total_mile / n, 1),
            "avg_map_quality_score":        round(total_qual / n, 1),
        }
