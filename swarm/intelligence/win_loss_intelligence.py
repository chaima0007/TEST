"""Win/Loss Intelligence — analyzes completed deals to surface execution patterns and coaching insights."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class DealOutcome(str, Enum):
    WON = "won"
    LOST = "lost"
    NO_DECISION = "no_decision"


class ExecutionQuality(str, Enum):
    EXCELLENT = "excellent"  # score >= 80
    GOOD = "good"            # score >= 60
    FAIR = "fair"            # score >= 40
    POOR = "poor"            # score < 40


class WinLossAction(str, Enum):
    REPLICATE = "replicate"      # WON with good execution — document and scale this approach
    DEBRIEF = "debrief"          # LOST despite good execution — extract competitive learnings
    INVESTIGATE = "investigate"  # NO_DECISION — diagnose root cause
    COACH = "coach"              # Poor execution drove the outcome — training needed


@dataclass
class WinLossInput:
    deal_id: str
    deal_name: str
    account_name: str
    segment: str  # enterprise / mid_market / smb
    arr_eur: float
    outcome: DealOutcome

    # Execution quality signals
    had_champion: bool
    executive_engaged: bool
    poc_done: bool
    budget_confirmed: bool
    decision_maker_met: bool
    multi_thread_count: int      # distinct contacts engaged throughout the deal
    next_step_always_present: bool  # was there always a clear next step?

    # Timeline
    days_to_outcome: int
    expected_cycle_days: int     # target/benchmark for this segment

    # Outcome context
    discount_given_pct: float    # 0-100
    loss_reason: str             # price/competitor/timing/product_gap/relationship/no_champion/none
    competitor_lost_to: str      # "" if WON or unknown

    # Engagement depth
    num_meetings: int
    objections_handled: int
    references_provided: bool
    case_study_shared: bool


@dataclass
class WinLossResult:
    deal_id: str
    deal_name: str
    account_name: str
    segment: str
    arr_eur: float
    outcome: DealOutcome

    execution_quality: ExecutionQuality
    wl_action: WinLossAction
    execution_score: float       # 0-100 — how well the process was executed

    cycle_efficiency_pct: float  # (1 - actual/expected) * 100; + = faster than expected
    discount_pressure: str       # none / low / medium / high

    win_patterns: list[str]      # positive signals for WON deals
    loss_factors: list[str]      # what went wrong for LOST / NO_DECISION
    process_gaps: list[str]      # execution gaps regardless of outcome
    coaching_insights: list[str] # actionable coaching points

    def to_dict(self) -> dict:
        d = asdict(self)
        d["outcome"] = self.outcome.value
        d["execution_quality"] = self.execution_quality.value
        d["wl_action"] = self.wl_action.value
        return d


def _execution_score(inp: WinLossInput) -> float:
    score = 0.0
    if inp.had_champion:          score += 20.0
    if inp.executive_engaged:     score += 15.0
    if inp.poc_done:              score += 15.0
    if inp.budget_confirmed:      score += 15.0
    if inp.decision_maker_met:    score += 15.0
    if inp.multi_thread_count >= 3: score += 10.0
    elif inp.multi_thread_count >= 2: score += 5.0
    if inp.next_step_always_present: score += 10.0
    return round(max(0.0, min(100.0, score)), 2)


def _execution_quality(score: float) -> ExecutionQuality:
    if score >= 80:
        return ExecutionQuality.EXCELLENT
    if score >= 60:
        return ExecutionQuality.GOOD
    if score >= 40:
        return ExecutionQuality.FAIR
    return ExecutionQuality.POOR


def _cycle_efficiency(inp: WinLossInput) -> float:
    if inp.expected_cycle_days <= 0:
        return 0.0
    return round((1.0 - inp.days_to_outcome / inp.expected_cycle_days) * 100.0, 1)


def _discount_pressure(inp: WinLossInput) -> str:
    if inp.discount_given_pct == 0:
        return "none"
    if inp.discount_given_pct <= 10:
        return "low"
    if inp.discount_given_pct <= 25:
        return "medium"
    return "high"


def _wl_action(inp: WinLossInput, quality: ExecutionQuality) -> WinLossAction:
    if inp.outcome == DealOutcome.WON:
        if quality in (ExecutionQuality.EXCELLENT, ExecutionQuality.GOOD):
            return WinLossAction.REPLICATE
        return WinLossAction.COACH
    if inp.outcome == DealOutcome.NO_DECISION:
        return WinLossAction.INVESTIGATE
    # LOST
    if quality in (ExecutionQuality.EXCELLENT, ExecutionQuality.GOOD):
        return WinLossAction.DEBRIEF
    return WinLossAction.COACH


def _build_signals(
    inp: WinLossInput,
    quality: ExecutionQuality,
    efficiency: float,
    pressure: str,
) -> tuple[list[str], list[str], list[str], list[str]]:
    win_patterns: list[str] = []
    loss_factors: list[str] = []
    process_gaps: list[str] = []
    coaching: list[str] = []

    # Win patterns (only for WON)
    if inp.outcome == DealOutcome.WON:
        if inp.had_champion:
            win_patterns.append("Deal champion-led — champion interne a accéléré la décision")
        if inp.executive_engaged:
            win_patterns.append("Alignement exécutif — sponsor C-level a facilité la signature")
        if inp.poc_done:
            win_patterns.append("POC complété — preuve technique a converti les sceptiques")
        if inp.budget_confirmed and inp.decision_maker_met:
            win_patterns.append("Deal bien qualifié — budget et décideur confirmés dès le départ")
        if inp.num_meetings >= 5:
            win_patterns.append(f"Engagement soutenu — {inp.num_meetings} réunions, relation de confiance établie")
        if inp.discount_given_pct == 0:
            win_patterns.append("Victoire sans remise — valeur perçue excellente")
        elif inp.discount_given_pct <= 10:
            win_patterns.append(f"Faible pression prix — seulement {inp.discount_given_pct:.0f}% de remise accordée")
        if efficiency > 10:
            win_patterns.append(f"Cycle rapide — {efficiency:.0f}% plus court que prévu")
        if inp.multi_thread_count >= 3:
            win_patterns.append(f"Multi-threading efficace — {inp.multi_thread_count} contacts engagés")
        if inp.references_provided:
            win_patterns.append("Références clients décisives — peer validation convaincante")
        if inp.case_study_shared:
            win_patterns.append("Business case partagé — ROI démontré avant négociation")

    # Loss factors (for LOST / NO_DECISION)
    if inp.outcome in (DealOutcome.LOST, DealOutcome.NO_DECISION):
        if inp.loss_reason == "price":
            win_patterns_text = f"Perdu sur le prix — budget insuffisant ou concurrence moins chère"
            loss_factors.append("Perdu sur le prix — valeur perçue insuffisante par rapport au coût")
        elif inp.loss_reason == "competitor":
            rival = f" ({inp.competitor_lost_to})" if inp.competitor_lost_to else ""
            loss_factors.append(f"Perdu face à un concurrent{rival} — différenciation insuffisante")
        elif inp.loss_reason == "timing":
            loss_factors.append("Perdu par timing — priorité interne non alignée ou budget gelé")
        elif inp.loss_reason == "product_gap":
            loss_factors.append("Perdu pour gap produit — besoin non couvert par notre offre")
        elif inp.loss_reason == "relationship":
            loss_factors.append("Perdu sur la relation — confiance insuffisante ou concurrent mieux positionné")
        elif inp.loss_reason == "no_champion":
            loss_factors.append("Perdu faute de champion — pas d'avocat interne pour porter le projet")
        if inp.outcome == DealOutcome.NO_DECISION:
            loss_factors.append("Pas de décision prise — status quo maintenu ou projet annulé")
        if not inp.had_champion:
            loss_factors.append("Aucun champion identifié — manque de support interne critique")
        if not inp.executive_engaged:
            loss_factors.append("Pas d'engagement exécutif — décision bloquée au niveau opérationnel")
        if inp.discount_given_pct > 25:
            loss_factors.append(f"Forte pression prix ({inp.discount_given_pct:.0f}% remise) — positionnement valeur défaillant")
        if inp.multi_thread_count < 2:
            loss_factors.append("Trop peu de contacts engagés — single-threading risqué")
        if not inp.budget_confirmed:
            loss_factors.append("Budget jamais confirmé — qualification incomplète")

    # Process gaps (all outcomes)
    if not inp.had_champion:
        process_gaps.append("Pas de champion identifié — point de contact insuffisant pour influencer")
    if not inp.budget_confirmed:
        process_gaps.append("Budget non confirmé — deal insuffisamment qualifié")
    if not inp.decision_maker_met:
        process_gaps.append("Décideur jamais rencontré — risque de surprise en fin de cycle")
    if inp.multi_thread_count < 2:
        process_gaps.append("Single-threading détecté — trop dépendant d'un seul contact")
    if not inp.next_step_always_present:
        process_gaps.append("Prochaines étapes non systématiques — momentum fragile")
    if not inp.poc_done and inp.arr_eur >= 50000:
        process_gaps.append("POC non proposé sur un deal significatif — opportunité manquée")
    if inp.num_meetings < 3:
        process_gaps.append(f"Peu de réunions ({inp.num_meetings}) — engagement client insuffisant")

    # Coaching insights
    if not inp.had_champion:
        coaching.append("Identifier le champion dès la qualification — ne pas avancer sans")
    if not inp.budget_confirmed and inp.outcome != DealOutcome.WON:
        coaching.append("Confirmer le budget avant d'aller en proposition")
    if inp.discount_given_pct > 25:
        coaching.append(f"Travailler le ROI plus tôt — {inp.discount_given_pct:.0f}% de remise signale une valeur mal perçue")
    if not inp.executive_engaged and inp.outcome != DealOutcome.WON:
        coaching.append("Engager un sponsor exécutif dès le stade démo/proposition")
    if inp.loss_reason == "competitor" and inp.competitor_lost_to:
        coaching.append(f"Renforcer la battle card contre {inp.competitor_lost_to} — deal perdu sur différenciation")
    if inp.loss_reason == "product_gap":
        coaching.append("Remonter le gap produit à l'équipe produit — impact sur pipeline identique")
    if not inp.poc_done and inp.outcome == DealOutcome.LOST and inp.arr_eur >= 50000:
        coaching.append("Proposer systématiquement un POC sur les deals à fort enjeu")
    if inp.outcome == DealOutcome.WON and quality == ExecutionQuality.EXCELLENT:
        coaching.append("Documenter ce playbook — deal modèle à partager avec l'équipe")
    if inp.outcome == DealOutcome.WON and inp.discount_given_pct == 0:
        coaching.append("Capitaliser sur ce cas — deal sans remise à utiliser en formation pricing")
    if efficiency > 20 and inp.outcome == DealOutcome.WON:
        coaching.append(f"Analyser les facteurs de rapidité ({efficiency:.0f}% sous le cycle cible) — scalabiliser")
    if not inp.next_step_always_present:
        coaching.append("Systématiser les prochaines étapes en fin de chaque réunion")
    if inp.multi_thread_count < 2:
        coaching.append("Développer plusieurs contacts dès la qualification pour éviter le single-threading")

    return win_patterns, loss_factors, process_gaps, coaching


class WinLossIntelligenceEngine:
    """Analyzes completed deals to identify execution patterns and coaching opportunities."""

    def __init__(self) -> None:
        self._results: dict[str, WinLossResult] = {}

    def analyze(self, inp: WinLossInput) -> WinLossResult:
        score = _execution_score(inp)
        quality = _execution_quality(score)
        efficiency = _cycle_efficiency(inp)
        pressure = _discount_pressure(inp)
        action = _wl_action(inp, quality)
        win_p, loss_f, gaps, coaching = _build_signals(inp, quality, efficiency, pressure)

        result = WinLossResult(
            deal_id=inp.deal_id,
            deal_name=inp.deal_name,
            account_name=inp.account_name,
            segment=inp.segment,
            arr_eur=inp.arr_eur,
            outcome=inp.outcome,
            execution_quality=quality,
            wl_action=action,
            execution_score=score,
            cycle_efficiency_pct=efficiency,
            discount_pressure=pressure,
            win_patterns=win_p,
            loss_factors=loss_f,
            process_gaps=gaps,
            coaching_insights=coaching,
        )
        self._results[inp.deal_id] = result
        return result

    def analyze_batch(self, inputs: list[WinLossInput]) -> list[WinLossResult]:
        return sorted(
            [self.analyze(inp) for inp in inputs],
            key=lambda r: r.execution_score,
            reverse=True,
        )

    def get(self, deal_id: str) -> Optional[WinLossResult]:
        return self._results.get(deal_id)

    def all_deals(self) -> list[WinLossResult]:
        return sorted(self._results.values(), key=lambda r: r.execution_score, reverse=True)

    def by_outcome(self, outcome: DealOutcome) -> list[WinLossResult]:
        return [r for r in self.all_deals() if r.outcome == outcome]

    def won(self) -> list[WinLossResult]:
        return self.by_outcome(DealOutcome.WON)

    def lost(self) -> list[WinLossResult]:
        return self.by_outcome(DealOutcome.LOST)

    def no_decision(self) -> list[WinLossResult]:
        return self.by_outcome(DealOutcome.NO_DECISION)

    def by_quality(self, quality: ExecutionQuality) -> list[WinLossResult]:
        return [r for r in self.all_deals() if r.execution_quality == quality]

    def needs_coaching(self) -> list[WinLossResult]:
        return [r for r in self.all_deals() if r.wl_action == WinLossAction.COACH]

    def replicate_worthy(self) -> list[WinLossResult]:
        return [r for r in self.all_deals() if r.wl_action == WinLossAction.REPLICATE]

    def win_rate(self) -> float:
        all_r = list(self._results.values())
        if not all_r:
            return 0.0
        wins = sum(1 for r in all_r if r.outcome == DealOutcome.WON)
        return round(wins / len(all_r) * 100.0, 1)

    def avg_execution_score(self) -> float:
        deals = list(self._results.values())
        if not deals:
            return 0.0
        return round(sum(r.execution_score for r in deals) / len(deals), 1)

    def total_won_arr_eur(self) -> float:
        return round(sum(r.arr_eur for r in self.won()), 2)

    def total_lost_arr_eur(self) -> float:
        return round(sum(r.arr_eur for r in self.lost()), 2)

    def avg_discount_won(self) -> float:
        won = self.won()
        if not won:
            return 0.0
        total_arr = sum(r.arr_eur for r in won)
        if total_arr == 0:
            return 0.0
        return round(sum(r.arr_eur for r in won if r.discount_pressure == "none") / total_arr * 100.0, 1)

    def top_loss_reasons(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for r in self.lost():
            for factor in r.loss_factors[:1]:  # primary factor only
                counts[factor] = counts.get(factor, 0) + 1
        return counts

    def summary(self) -> dict:
        all_r = list(self._results.values())
        if not all_r:
            return {
                "total": 0,
                "outcome_counts": {},
                "quality_counts": {},
                "action_counts": {},
                "win_rate": 0.0,
                "avg_execution_score": 0.0,
                "total_won_arr_eur": 0.0,
                "total_lost_arr_eur": 0.0,
                "coaching_needed_count": 0,
                "replicate_count": 0,
            }
        outcome_counts: dict[str, int] = {}
        quality_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in all_r:
            outcome_counts[r.outcome.value] = outcome_counts.get(r.outcome.value, 0) + 1
            quality_counts[r.execution_quality.value] = quality_counts.get(r.execution_quality.value, 0) + 1
            action_counts[r.wl_action.value] = action_counts.get(r.wl_action.value, 0) + 1
        return {
            "total": len(all_r),
            "outcome_counts": outcome_counts,
            "quality_counts": quality_counts,
            "action_counts": action_counts,
            "win_rate": self.win_rate(),
            "avg_execution_score": self.avg_execution_score(),
            "total_won_arr_eur": self.total_won_arr_eur(),
            "total_lost_arr_eur": self.total_lost_arr_eur(),
            "coaching_needed_count": len(self.needs_coaching()),
            "replicate_count": len(self.replicate_worthy()),
        }

    def reset(self) -> None:
        self._results.clear()
