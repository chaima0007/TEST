from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DealOutcome(str, Enum):
    CLOSED_WON  = "closed_won"
    CLOSED_LOST = "closed_lost"
    NO_DECISION = "no_decision"
    CHURNED     = "churned"


class LossReason(str, Enum):
    PRICE           = "price"
    COMPETITOR      = "competitor"
    TIMING          = "timing"
    CHAMPION_LOSS   = "champion_loss"
    POOR_PROCESS    = "poor_process"
    NO_LOSS         = "no_loss"


class RepBehaviorPattern(str, Enum):
    EXEMPLARY       = "exemplary"
    SOLID           = "solid"
    IMPROVABLE      = "improvable"
    HIGH_RISK       = "high_risk"


class WinLossAction(str, Enum):
    REPLICATE       = "replicate"
    SHARE_AS_BEST_PRACTICE = "share_as_best_practice"
    COACH_AND_IMPROVE      = "coach_and_improve"
    URGENT_INTERVENTION    = "urgent_intervention"


@dataclass
class WinLossPatternInput:
    deal_id:                        str
    deal_name:                      str
    rep_id:                         str
    deal_outcome:                   str     # "closed_won"/"closed_lost"/"no_decision"/"churned"
    deal_size_usd:                  float
    sales_cycle_days:               int     # actual days from first contact to close
    expected_cycle_days:            int     # expected cycle for this segment
    discovery_calls_completed:      int     # # of discovery calls
    stakeholders_engaged:           int     # # unique stakeholders engaged
    exec_sponsor_engaged:           int     # 1 if exec sponsor was engaged
    champion_active_at_close:       int     # 1 if champion was still active at close
    proposal_revision_count:        int     # # of proposal revisions requested
    demo_count:                     int     # # of demos given
    mutual_action_plan_used:        int     # 1 if MAP was used
    competitive_deal:               int     # 1 if competitors were mentioned
    competitor_displacement:        int     # 1 if we displaced a competitor
    price_discount_pct:             float   # % discount applied (0-100)
    close_date_slips:               int     # # of close date slips
    objections_raised:              int     # total objections raised
    objections_resolved_pct:        float   # % of objections resolved (0-100)
    post_deal_survey_score:         float   # buyer feedback score 0-100 (-1 if no survey)
    rep_activity_score:             float   # rep activity quality 0-100


@dataclass
class WinLossPatternResult:
    deal_id:                str
    deal_name:              str
    deal_outcome:           DealOutcome
    loss_reason:            LossReason
    rep_behavior_pattern:   RepBehaviorPattern
    win_loss_action:        WinLossAction
    process_quality_score:  float   # 0-100
    execution_score:        float   # 0-100
    relationship_score:     float   # 0-100
    deal_health_score:      float   # 0-100
    win_loss_composite:     float   # 0-100
    win_probability_index:  float   # 0-100 (how "winnable" was this deal)
    replication_value:      float   # 0-100 (how valuable to replicate this rep's approach)
    is_best_practice:       bool
    needs_coaching:         bool

    def to_dict(self) -> dict:
        return {
            "deal_id":                  self.deal_id,
            "deal_name":                self.deal_name,
            "deal_outcome":             self.deal_outcome.value,
            "loss_reason":              self.loss_reason.value,
            "rep_behavior_pattern":     self.rep_behavior_pattern.value,
            "win_loss_action":          self.win_loss_action.value,
            "process_quality_score":    self.process_quality_score,
            "execution_score":          self.execution_score,
            "relationship_score":       self.relationship_score,
            "deal_health_score":        self.deal_health_score,
            "win_loss_composite":       self.win_loss_composite,
            "win_probability_index":    self.win_probability_index,
            "replication_value":        self.replication_value,
            "is_best_practice":         self.is_best_practice,
            "needs_coaching":           self.needs_coaching,
        }


class WinLossPatternEngine:
    def __init__(self) -> None:
        self._results: list[WinLossPatternResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: WinLossPatternInput) -> WinLossPatternResult:
        process     = self._process_quality_score(inp)
        execution   = self._execution_score(inp)
        relationship = self._relationship_score(inp)
        health      = self._deal_health_score(inp)
        composite   = self._composite(process, execution, relationship, health)
        outcome     = self._parse_outcome(inp.deal_outcome)
        loss_reason = self._loss_reason(inp, outcome)
        behavior    = self._rep_behavior_pattern(composite, inp, outcome)
        win_prob    = self._win_probability_index(inp)
        repl_value  = self._replication_value(composite, inp, outcome)
        is_bp       = outcome == DealOutcome.CLOSED_WON and composite >= 75
        needs_coach = composite < 45 or (outcome == DealOutcome.CLOSED_LOST and process < 50)
        action      = self._win_loss_action(behavior, is_bp, needs_coach)

        result = WinLossPatternResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            deal_outcome=outcome,
            loss_reason=loss_reason,
            rep_behavior_pattern=behavior,
            win_loss_action=action,
            process_quality_score=process,
            execution_score=execution,
            relationship_score=relationship,
            deal_health_score=health,
            win_loss_composite=composite,
            win_probability_index=win_prob,
            replication_value=repl_value,
            is_best_practice=is_bp,
            needs_coaching=needs_coach,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[WinLossPatternInput]) -> list[WinLossPatternResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def best_practice_deals(self) -> list[WinLossPatternResult]:
        return [r for r in self._results if r.is_best_practice]

    @property
    def coaching_queue(self) -> list[WinLossPatternResult]:
        return [r for r in self._results if r.needs_coaching]

    @property
    def avg_win_loss_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.win_loss_composite for r in self._results) / len(self._results), 1)

    @property
    def win_rate(self) -> float:
        if not self._results:
            return 0.0
        won = sum(1 for r in self._results if r.deal_outcome == DealOutcome.CLOSED_WON)
        return round(won / len(self._results) * 100, 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _process_quality_score(self, inp: WinLossPatternInput) -> float:
        score = 0.0
        # Discovery calls (25 pts)
        if inp.discovery_calls_completed >= 3:
            score += 25.0
        elif inp.discovery_calls_completed >= 2:
            score += 16.0
        elif inp.discovery_calls_completed >= 1:
            score += 8.0
        # MAP usage (20 pts)
        if inp.mutual_action_plan_used:
            score += 20.0
        # Objection resolution rate (30 pts)
        orr = inp.objections_resolved_pct
        if orr >= 80:
            score += 30.0
        elif orr >= 60:
            score += 20.0
        elif orr >= 40:
            score += 10.0
        # Close date discipline (penalty)
        if inp.close_date_slips == 0:
            score += 15.0
        elif inp.close_date_slips == 1:
            score += 7.0
        elif inp.close_date_slips >= 3:
            score -= 10.0
        # Proposal revisions penalty
        if inp.proposal_revision_count >= 4:
            score -= 10.0
        elif inp.proposal_revision_count >= 2:
            score -= 5.0
        return round(max(0.0, min(100.0, score)), 1)

    def _execution_score(self, inp: WinLossPatternInput) -> float:
        score = 0.0
        # Sales cycle efficiency
        if inp.expected_cycle_days > 0:
            cycle_ratio = inp.sales_cycle_days / inp.expected_cycle_days
            if cycle_ratio <= 0.8:
                score += 35.0
            elif cycle_ratio <= 1.0:
                score += 25.0
            elif cycle_ratio <= 1.3:
                score += 12.0
            elif cycle_ratio <= 1.7:
                score += 5.0
        # Activity score
        act = inp.rep_activity_score
        if act >= 80:
            score += 35.0
        elif act >= 60:
            score += 22.0
        elif act >= 40:
            score += 10.0
        # Demo count (2-3 is optimal)
        if 2 <= inp.demo_count <= 3:
            score += 20.0
        elif inp.demo_count == 1 or inp.demo_count == 4:
            score += 10.0
        # Competitor displacement bonus
        if inp.competitor_displacement:
            score = min(100.0, score + 10.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _relationship_score(self, inp: WinLossPatternInput) -> float:
        score = 0.0
        # Stakeholder breadth (30 pts)
        se = inp.stakeholders_engaged
        if se >= 6:
            score += 30.0
        elif se >= 4:
            score += 20.0
        elif se >= 2:
            score += 10.0
        # Exec sponsor (25 pts)
        if inp.exec_sponsor_engaged:
            score += 25.0
        # Champion active at close (30 pts)
        if inp.champion_active_at_close:
            score += 30.0
        # Buyer feedback bonus
        if inp.post_deal_survey_score >= 80:
            score = min(100.0, score + 15.0)
        elif inp.post_deal_survey_score >= 60:
            score = min(100.0, score + 8.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _deal_health_score(self, inp: WinLossPatternInput) -> float:
        score = 0.0
        # Discount discipline (less is better)
        disc = inp.price_discount_pct
        if disc == 0:
            score += 30.0
        elif disc <= 5:
            score += 22.0
        elif disc <= 15:
            score += 12.0
        elif disc <= 25:
            score += 4.0
        # Deal size factor (larger deals = more strategic)
        if inp.deal_size_usd >= 200_000:
            score += 25.0
        elif inp.deal_size_usd >= 75_000:
            score += 15.0
        elif inp.deal_size_usd >= 25_000:
            score += 8.0
        # Won bonus
        if inp.deal_outcome == "closed_won":
            score = min(100.0, score + 35.0)
        elif inp.deal_outcome == "no_decision":
            score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        process: float,
        execution: float,
        relationship: float,
        health: float,
    ) -> float:
        composite = process * 0.30 + execution * 0.30 + relationship * 0.25 + health * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _parse_outcome(self, outcome_str: str) -> DealOutcome:
        try:
            return DealOutcome(outcome_str)
        except ValueError:
            return DealOutcome.CLOSED_LOST

    def _loss_reason(self, inp: WinLossPatternInput, outcome: DealOutcome) -> LossReason:
        if outcome == DealOutcome.CLOSED_WON:
            return LossReason.NO_LOSS
        # Determine primary loss reason
        if not inp.champion_active_at_close and outcome != DealOutcome.NO_DECISION:
            return LossReason.CHAMPION_LOSS
        if inp.competitive_deal and not inp.competitor_displacement:
            return LossReason.COMPETITOR
        if inp.price_discount_pct >= 20:
            return LossReason.PRICE
        if inp.close_date_slips >= 3:
            return LossReason.TIMING
        if inp.discovery_calls_completed <= 1 or inp.objections_resolved_pct < 40:
            return LossReason.POOR_PROCESS
        return LossReason.TIMING

    def _rep_behavior_pattern(
        self, composite: float, inp: WinLossPatternInput, outcome: DealOutcome
    ) -> RepBehaviorPattern:
        if composite >= 75 and outcome == DealOutcome.CLOSED_WON:
            return RepBehaviorPattern.EXEMPLARY
        if composite >= 60:
            return RepBehaviorPattern.SOLID
        if composite >= 40:
            return RepBehaviorPattern.IMPROVABLE
        return RepBehaviorPattern.HIGH_RISK

    def _win_probability_index(self, inp: WinLossPatternInput) -> float:
        # How "winnable" was this deal regardless of outcome
        score = 50.0
        if inp.exec_sponsor_engaged:
            score += 15.0
        if inp.champion_active_at_close:
            score += 15.0
        if inp.mutual_action_plan_used:
            score += 10.0
        if inp.objections_resolved_pct >= 80:
            score += 10.0
        if inp.close_date_slips >= 3:
            score -= 15.0
        if inp.price_discount_pct >= 20:
            score -= 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _replication_value(
        self, composite: float, inp: WinLossPatternInput, outcome: DealOutcome
    ) -> float:
        # How valuable is it to have other reps replicate this approach
        if outcome != DealOutcome.CLOSED_WON:
            return max(0.0, round(composite * 0.4, 1))  # lost = low replication value
        return round(min(100.0, composite * 1.1), 1)

    def _win_loss_action(
        self,
        behavior: RepBehaviorPattern,
        is_bp: bool,
        needs_coaching: bool,
    ) -> WinLossAction:
        if is_bp and behavior == RepBehaviorPattern.EXEMPLARY:
            return WinLossAction.SHARE_AS_BEST_PRACTICE
        if behavior == RepBehaviorPattern.HIGH_RISK or needs_coaching:
            return WinLossAction.URGENT_INTERVENTION
        if needs_coaching or behavior == RepBehaviorPattern.IMPROVABLE:
            return WinLossAction.COACH_AND_IMPROVE
        return WinLossAction.REPLICATE

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "outcome_counts":               {},
                "loss_reason_counts":           {},
                "behavior_counts":              {},
                "action_counts":                {},
                "avg_win_loss_composite":       0.0,
                "win_rate":                     0.0,
                "best_practice_count":          0,
                "coaching_count":               0,
                "avg_process_quality_score":    0.0,
                "avg_execution_score":          0.0,
                "avg_relationship_score":       0.0,
                "avg_replication_value":        0.0,
            }

        outcome_counts:     dict[str, int] = {}
        loss_counts:        dict[str, int] = {}
        behavior_counts:    dict[str, int] = {}
        action_counts:      dict[str, int] = {}
        total_comp = 0.0; total_proc = 0.0; total_exec = 0.0
        total_rel  = 0.0; total_repl = 0.0

        for r in self._results:
            outcome_counts[r.deal_outcome.value]            = outcome_counts.get(r.deal_outcome.value, 0) + 1
            loss_counts[r.loss_reason.value]                = loss_counts.get(r.loss_reason.value, 0) + 1
            behavior_counts[r.rep_behavior_pattern.value]   = behavior_counts.get(r.rep_behavior_pattern.value, 0) + 1
            action_counts[r.win_loss_action.value]          = action_counts.get(r.win_loss_action.value, 0) + 1
            total_comp += r.win_loss_composite
            total_proc += r.process_quality_score
            total_exec += r.execution_score
            total_rel  += r.relationship_score
            total_repl += r.replication_value

        return {
            "total":                        n,
            "outcome_counts":               outcome_counts,
            "loss_reason_counts":           loss_counts,
            "behavior_counts":              behavior_counts,
            "action_counts":                action_counts,
            "avg_win_loss_composite":       round(total_comp / n, 1),
            "win_rate":                     self.win_rate,
            "best_practice_count":          len(self.best_practice_deals),
            "coaching_count":               len(self.coaching_queue),
            "avg_process_quality_score":    round(total_proc / n, 1),
            "avg_execution_score":          round(total_exec / n, 1),
            "avg_relationship_score":       round(total_rel / n, 1),
            "avg_replication_value":        round(total_repl / n, 1),
        }
