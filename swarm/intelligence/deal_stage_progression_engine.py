"""Module 36 — Deal Stage Progression Engine

Analyses each deal's current pipeline stage, velocity through stages, and
predicts the probability of advancing to close within the quarter.  Flags
stuck deals, recommends next actions per stage, and gives managers an
escalation signal when a deal has stalled beyond its expected cycle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class DealStage(str, Enum):
    PROSPECTING    = "prospecting"     # Stage 1
    QUALIFICATION  = "qualification"   # Stage 2
    DEMO           = "demo"            # Stage 3
    PROPOSAL       = "proposal"        # Stage 4
    NEGOTIATION    = "negotiation"     # Stage 5
    CLOSING        = "closing"         # Stage 6


class ProgressionRisk(str, Enum):
    ON_TRACK  = "on_track"    # advancing as expected
    SLOWING   = "slowing"     # slower than benchmark
    STUCK     = "stuck"       # no movement in >1 benchmark cycle
    REGRESSED = "regressed"   # moved backward at least one stage


class ProgressionAction(str, Enum):
    MAINTAIN    = "maintain"     # healthy velocity — keep cadence
    ACCELERATE  = "accelerate"   # push to next stage within 7 days
    RESCUE      = "rescue"       # deal in danger — urgent intervention
    CLOSE_NOW   = "close_now"    # at closing/negotiation — drive signature
    REPRIORITISE = "reprioritise"  # low score + stuck — consider deprioritising


class CloseQuarterProbability(str, Enum):
    HIGH    = "high"     # ≥70 % chance to close this quarter
    MEDIUM  = "medium"   # 40–69 %
    LOW     = "low"      # 15–39 %
    VERY_LOW = "very_low"  # <15 %


# ─── Input dataclass ─────────────────────────────────────────────────────────

@dataclass
class DealInput:
    deal_id: str
    deal_name: str
    rep_id: str
    rep_name: str
    account_name: str
    current_stage: DealStage
    previous_stage: Optional[DealStage]          # None if deal just created
    days_in_current_stage: int                   # days without stage change
    days_since_created: int
    deal_size_eur: float
    close_date_days_remaining: int               # days until expected close
    # Stage benchmark durations (avg days reps spend in each stage)
    benchmark_days_prospecting: int              # e.g. 7
    benchmark_days_qualification: int            # e.g. 10
    benchmark_days_demo: int                     # e.g. 14
    benchmark_days_proposal: int                 # e.g. 14
    benchmark_days_negotiation: int              # e.g. 10
    benchmark_days_closing: int                  # e.g. 7
    # Activity signals
    last_activity_days_ago: int                  # days since any logged activity
    meetings_held: int                           # total meetings for this deal
    emails_sent: int
    proposals_sent: int
    exec_sponsor_engaged: bool
    # Qualification signals
    budget_confirmed: bool
    timeline_confirmed: bool
    decision_maker_identified: bool
    # Historical win rate for this rep at current stage
    rep_stage_win_rate_pct: float                # 0–100


# ─── Output dataclass ─────────────────────────────────────────────────────────

@dataclass
class DealProgressionResult:
    deal_id: str
    deal_name: str
    rep_id: str
    rep_name: str
    account_name: str
    current_stage: DealStage
    previous_stage: Optional[DealStage]
    deal_size_eur: float

    # Computed fields
    progression_risk: ProgressionRisk
    progression_action: ProgressionAction
    close_quarter_probability: CloseQuarterProbability
    progression_score: float          # 0–100, higher = healthier progression
    stage_velocity_ratio: float       # days_in_stage / benchmark; <1 fast, >1 slow
    days_over_benchmark: int          # max(0, days_in_stage - benchmark)
    estimated_stages_remaining: int
    estimated_days_to_close: int

    # Qualitative signals
    stall_reasons: list[str]
    next_actions: list[str]
    close_quarter_drivers: list[str]

    def to_dict(self) -> dict:
        return {
            "deal_id": self.deal_id,
            "deal_name": self.deal_name,
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "account_name": self.account_name,
            "current_stage": self.current_stage.value,
            "previous_stage": self.previous_stage.value if self.previous_stage else None,
            "deal_size_eur": self.deal_size_eur,
            "progression_risk": self.progression_risk.value,
            "progression_action": self.progression_action.value,
            "close_quarter_probability": self.close_quarter_probability.value,
            "progression_score": self.progression_score,
            "stage_velocity_ratio": self.stage_velocity_ratio,
            "days_over_benchmark": self.days_over_benchmark,
            "estimated_stages_remaining": self.estimated_stages_remaining,
            "estimated_days_to_close": self.estimated_days_to_close,
            "stall_reasons": self.stall_reasons,
            "next_actions": self.next_actions,
            "close_quarter_drivers": self.close_quarter_drivers,
        }


# ─── Engine ──────────────────────────────────────────────────────────────────

class DealStageProgressionEngine:

    _STAGE_ORDER = [
        DealStage.PROSPECTING,
        DealStage.QUALIFICATION,
        DealStage.DEMO,
        DealStage.PROPOSAL,
        DealStage.NEGOTIATION,
        DealStage.CLOSING,
    ]

    def __init__(self) -> None:
        self._results: list[DealProgressionResult] = []

    # ── private helpers ────────────────────────────────────────────────────

    def _benchmark_for_stage(self, stage: DealStage, inp: DealInput) -> int:
        mapping = {
            DealStage.PROSPECTING:   inp.benchmark_days_prospecting,
            DealStage.QUALIFICATION: inp.benchmark_days_qualification,
            DealStage.DEMO:          inp.benchmark_days_demo,
            DealStage.PROPOSAL:      inp.benchmark_days_proposal,
            DealStage.NEGOTIATION:   inp.benchmark_days_negotiation,
            DealStage.CLOSING:       inp.benchmark_days_closing,
        }
        return mapping[stage]

    def _stage_velocity_ratio(self, inp: DealInput) -> float:
        benchmark = self._benchmark_for_stage(inp.current_stage, inp)
        if benchmark <= 0:
            return 1.0
        return inp.days_in_current_stage / benchmark

    def _days_over_benchmark(self, inp: DealInput) -> int:
        benchmark = self._benchmark_for_stage(inp.current_stage, inp)
        return max(0, inp.days_in_current_stage - benchmark)

    def _stage_index(self, stage: DealStage) -> int:
        return self._STAGE_ORDER.index(stage)

    def _stages_remaining(self, inp: DealInput) -> int:
        idx = self._stage_index(inp.current_stage)
        return len(self._STAGE_ORDER) - 1 - idx

    def _avg_remaining_days(self, inp: DealInput) -> int:
        """Sum of benchmark days for stages not yet reached."""
        idx = self._stage_index(inp.current_stage)
        remaining_stages = self._STAGE_ORDER[idx:]  # includes current
        # For current stage count only remaining days (benchmark - elapsed, min 0)
        current_benchmark = self._benchmark_for_stage(inp.current_stage, inp)
        days_left_in_current = max(0, current_benchmark - inp.days_in_current_stage)
        future_stages = self._STAGE_ORDER[idx + 1:]
        future_days = sum(self._benchmark_for_stage(s, inp) for s in future_stages)
        return days_left_in_current + future_days

    def _progression_risk(self, inp: DealInput, velocity_ratio: float) -> ProgressionRisk:
        # Regression: previous stage is further along than current
        if inp.previous_stage is not None:
            prev_idx = self._stage_index(inp.previous_stage)
            curr_idx = self._stage_index(inp.current_stage)
            if curr_idx < prev_idx:
                return ProgressionRisk.REGRESSED

        # Stuck: > 2× benchmark with no recent activity
        if velocity_ratio >= 2.0 and inp.last_activity_days_ago > 7:
            return ProgressionRisk.STUCK

        # Slowing: >1.5× benchmark or no activity > 5 days
        if velocity_ratio >= 1.5 or inp.last_activity_days_ago > 5:
            return ProgressionRisk.SLOWING

        return ProgressionRisk.ON_TRACK

    def _progression_action(
        self,
        inp: DealInput,
        risk: ProgressionRisk,
        score: float,
    ) -> ProgressionAction:
        stage = inp.current_stage
        if stage in (DealStage.NEGOTIATION, DealStage.CLOSING):
            return ProgressionAction.CLOSE_NOW
        if risk in (ProgressionRisk.STUCK, ProgressionRisk.REGRESSED):
            if score < 35:
                return ProgressionAction.REPRIORITISE
            return ProgressionAction.RESCUE
        if risk == ProgressionRisk.SLOWING:
            return ProgressionAction.ACCELERATE
        return ProgressionAction.MAINTAIN

    def _close_quarter_probability(
        self, inp: DealInput, score: float, estimated_days: int
    ) -> CloseQuarterProbability:
        """Assess likelihood of closing within close_date_days_remaining."""
        days_avail = inp.close_date_days_remaining
        # If estimated time to close > available days with margin → lower probability
        time_feasible = estimated_days <= days_avail * 1.1

        if score >= 70 and time_feasible and inp.exec_sponsor_engaged:
            return CloseQuarterProbability.HIGH
        if score >= 50 and time_feasible:
            return CloseQuarterProbability.MEDIUM
        if score >= 30 or (time_feasible and score >= 20):
            return CloseQuarterProbability.LOW
        return CloseQuarterProbability.VERY_LOW

    def _progression_score(self, inp: DealInput, velocity_ratio: float) -> float:
        """
        0–100 composite score for deal progression health.
        Components:
          velocity   30 pts  (1.0→30, scales down with ratio)
          activity   25 pts  (last_activity, meetings, emails)
          qual sigs  20 pts  (budget/timeline/dm)
          win_rate   15 pts  (rep stage win rate)
          stage adv  10 pts  (bonus for being in later stages)
        """
        # Velocity component: perfect at ratio ≤ 1, zero at ratio ≥ 3
        vel_pts = max(0.0, 30.0 * (1.0 - (velocity_ratio - 1.0) / 2.0))
        vel_pts = min(30.0, vel_pts)

        # Activity component
        recency_pts = max(0.0, 10.0 - inp.last_activity_days_ago * 1.5)
        meeting_pts = min(8.0, inp.meetings_held * 2.0)
        email_pts   = min(7.0, inp.emails_sent * 0.5)
        act_pts = min(25.0, recency_pts + meeting_pts + email_pts)

        # Qualification signals
        qual_pts = (
            (7.0 if inp.budget_confirmed else 0.0)
            + (7.0 if inp.timeline_confirmed else 0.0)
            + (6.0 if inp.decision_maker_identified else 0.0)
        )

        # Rep stage win rate
        wr_pts = min(15.0, inp.rep_stage_win_rate_pct * 0.15)

        # Stage advancement bonus
        stage_bonus = self._stage_index(inp.current_stage) * (10.0 / 5.0)

        raw = vel_pts + act_pts + qual_pts + wr_pts + stage_bonus
        return round(min(100.0, max(0.0, raw)), 1)

    def _stall_reasons(self, inp: DealInput, velocity_ratio: float) -> list[str]:
        reasons: list[str] = []
        if velocity_ratio >= 2.0:
            bench = self._benchmark_for_stage(inp.current_stage, inp)
            reasons.append(
                f"Bloqué depuis {inp.days_in_current_stage}j (benchmark {bench}j) — "
                f"ratio {velocity_ratio:.1f}×"
            )
        if inp.last_activity_days_ago > 7:
            reasons.append(
                f"Aucune activité depuis {inp.last_activity_days_ago} jours"
            )
        if not inp.budget_confirmed:
            reasons.append("Budget non confirmé — risque de décrochage")
        if not inp.decision_maker_identified:
            reasons.append("Décideur non identifié — champion à sécuriser")
        if not inp.exec_sponsor_engaged and inp.current_stage in (
            DealStage.PROPOSAL, DealStage.NEGOTIATION, DealStage.CLOSING
        ):
            reasons.append("Sponsor exécutif absent — exposition au risque")
        if inp.previous_stage is not None:
            prev_idx = self._stage_index(inp.previous_stage)
            curr_idx = self._stage_index(inp.current_stage)
            if curr_idx < prev_idx:
                reasons.append(
                    f"Régression de {inp.previous_stage.value} → "
                    f"{inp.current_stage.value}"
                )
        return reasons

    def _next_actions(self, inp: DealInput, action: ProgressionAction) -> list[str]:
        stage = inp.current_stage
        base: list[str] = []

        if action == ProgressionAction.CLOSE_NOW:
            base = [
                "Envoyer la proposition finale dans les 24h",
                "Organiser un appel de closing avec le décideur",
                "Lever les dernières objections contractuelles",
                "Aligner sur la date de signature",
            ]
        elif action == ProgressionAction.RESCUE:
            base = [
                "Session de revue manager — analyse deal by deal",
                "Re-qualifier le champion et vérifier le budget",
                "Proposer une démo personnalisée ou POC pour relancer",
                "Demander un exec sponsor côté client",
            ]
        elif action == ProgressionAction.REPRIORITISE:
            base = [
                "Évaluer si le deal est encore viable",
                "Passer en mode nurture ou fermer le deal",
                "Réallouer le temps commercial sur des deals plus matures",
            ]
        elif action == ProgressionAction.ACCELERATE:
            base = [
                f"Relancer le contact dans les 48h — prochaine étape : {self._next_stage_name(stage)}",
                "Envoyer un contenu de valeur adapté au stade actuel",
                "Planifier la prochaine réunion avant la fin de semaine",
            ]
        else:  # MAINTAIN
            base = [
                "Maintenir la cadence d'activité actuelle",
                "Préparer les éléments pour l'étape suivante",
                "Reconfirmer le calendrier de décision avec le prospect",
            ]

        if inp.proposals_sent == 0 and stage in (
            DealStage.PROPOSAL, DealStage.NEGOTIATION
        ):
            base.insert(0, "Envoyer la proposition commerciale — non encore envoyée")

        return base

    def _next_stage_name(self, stage: DealStage) -> str:
        idx = self._stage_index(stage)
        if idx + 1 < len(self._STAGE_ORDER):
            return self._STAGE_ORDER[idx + 1].value
        return "closing"

    def _close_quarter_drivers(self, inp: DealInput, prob: CloseQuarterProbability) -> list[str]:
        drivers: list[str] = []
        if inp.exec_sponsor_engaged:
            drivers.append("Sponsor exécutif engagé — signal fort de closing")
        if inp.budget_confirmed:
            drivers.append("Budget confirmé — décision financière validée")
        if inp.timeline_confirmed:
            drivers.append("Timeline confirmée — urgence côté client identifiée")
        if inp.decision_maker_identified:
            drivers.append("Décideur identifié — accès direct au pouvoir de signature")
        if inp.proposals_sent >= 1:
            drivers.append(f"Proposition envoyée — {inp.proposals_sent} version(s)")
        if inp.meetings_held >= 3:
            drivers.append(f"{inp.meetings_held} réunions tenues — relation avancée")
        days_left = inp.close_date_days_remaining
        if days_left <= 30:
            drivers.append(f"Fin de période dans {days_left}j — pression calendaire")
        if not drivers:
            drivers.append("Peu de signaux positifs — investissement requis pour débloquer")
        return drivers

    # ── public API ─────────────────────────────────────────────────────────

    def analyze(self, inp: DealInput) -> DealProgressionResult:
        vel_ratio  = self._stage_velocity_ratio(inp)
        over_bench = self._days_over_benchmark(inp)
        score      = self._progression_score(inp, vel_ratio)
        risk       = self._progression_risk(inp, vel_ratio)
        action     = self._progression_action(inp, risk, score)
        est_days   = self._avg_remaining_days(inp)
        prob       = self._close_quarter_probability(inp, score, est_days)
        stalls     = self._stall_reasons(inp, vel_ratio)
        actions    = self._next_actions(inp, action)
        drivers    = self._close_quarter_drivers(inp, prob)

        result = DealProgressionResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            account_name=inp.account_name,
            current_stage=inp.current_stage,
            previous_stage=inp.previous_stage,
            deal_size_eur=inp.deal_size_eur,
            progression_risk=risk,
            progression_action=action,
            close_quarter_probability=prob,
            progression_score=score,
            stage_velocity_ratio=round(vel_ratio, 2),
            days_over_benchmark=over_bench,
            estimated_stages_remaining=self._stages_remaining(inp),
            estimated_days_to_close=est_days,
            stall_reasons=stalls,
            next_actions=actions,
            close_quarter_drivers=drivers,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[DealInput]) -> list[DealProgressionResult]:
        """Analyze multiple deals, sorted DESC by progression_score (best first)."""
        results = [self.analyze(inp) for inp in inputs]
        results.sort(key=lambda r: r.progression_score, reverse=True)
        return results

    # ── filter helpers ─────────────────────────────────────────────────────

    def all_deals(self) -> list[DealProgressionResult]:
        return list(self._results)

    def by_risk(self, risk: ProgressionRisk) -> list[DealProgressionResult]:
        return [r for r in self._results if r.progression_risk == risk]

    def by_action(self, action: ProgressionAction) -> list[DealProgressionResult]:
        return [r for r in self._results if r.progression_action == action]

    def by_probability(self, prob: CloseQuarterProbability) -> list[DealProgressionResult]:
        return [r for r in self._results if r.close_quarter_probability == prob]

    def by_stage(self, stage: DealStage) -> list[DealProgressionResult]:
        return [r for r in self._results if r.current_stage == stage]

    def stuck_deals(self) -> list[DealProgressionResult]:
        return self.by_risk(ProgressionRisk.STUCK)

    def regressed_deals(self) -> list[DealProgressionResult]:
        return self.by_risk(ProgressionRisk.REGRESSED)

    def needs_rescue(self) -> list[DealProgressionResult]:
        return [
            r for r in self._results
            if r.progression_action in (
                ProgressionAction.RESCUE, ProgressionAction.REPRIORITISE
            )
        ]

    def ready_to_close(self) -> list[DealProgressionResult]:
        return self.by_action(ProgressionAction.CLOSE_NOW)

    def high_probability_deals(self) -> list[DealProgressionResult]:
        return self.by_probability(CloseQuarterProbability.HIGH)

    # ── aggregates ─────────────────────────────────────────────────────────

    def total_pipeline_eur(self) -> float:
        return sum(r.deal_size_eur for r in self._results)

    def avg_progression_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.progression_score for r in self._results) / len(self._results), 1)

    def high_prob_pipeline_eur(self) -> float:
        return sum(r.deal_size_eur for r in self.high_probability_deals())

    def stuck_pipeline_eur(self) -> float:
        return sum(r.deal_size_eur for r in self.stuck_deals())

    def summary(self) -> dict:
        n = len(self._results)
        risk_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        prob_counts: dict[str, int] = {}
        for r in self._results:
            risk_counts[r.progression_risk.value]      = risk_counts.get(r.progression_risk.value, 0) + 1
            action_counts[r.progression_action.value]  = action_counts.get(r.progression_action.value, 0) + 1
            prob_counts[r.close_quarter_probability.value] = prob_counts.get(r.close_quarter_probability.value, 0) + 1
        return {
            "total_deals": n,
            "risk_counts": risk_counts,
            "action_counts": action_counts,
            "probability_counts": prob_counts,
            "avg_progression_score": self.avg_progression_score(),
            "total_pipeline_eur": self.total_pipeline_eur(),
            "high_prob_pipeline_eur": self.high_prob_pipeline_eur(),
            "stuck_pipeline_eur": self.stuck_pipeline_eur(),
            "stuck_count": len(self.stuck_deals()),
            "rescue_count": len(self.needs_rescue()),
        }

    def reset(self) -> None:
        self._results.clear()
