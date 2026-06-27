from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AttainmentOutcome(str, Enum):
    OVERACHIEVE = "overachieve"    # projected ≥110%
    ACHIEVE = "achieve"            # projected 90-109%
    SLIGHT_MISS = "slight_miss"    # projected 70-89%
    MISS = "miss"                  # projected 50-69%
    CRITICAL_MISS = "critical_miss"  # projected <50%


class AttainmentConfidence(str, Enum):
    HIGH = "high"       # strong pipeline + activity alignment
    MEDIUM = "medium"   # some signals uncertain
    LOW = "low"         # significant uncertainty
    VERY_LOW = "very_low"  # insufficient data or severe risk


class QuotaAction(str, Enum):
    MAINTAIN = "maintain"         # on track
    ACCELERATE = "accelerate"     # push harder to reach target
    INTERVENTION = "intervention"  # manager/coach engagement needed
    ESCALATE = "escalate"         # urgent leadership action


@dataclass
class AttainmentInput:
    rep_id: str
    rep_name: str
    region: str
    segment: str
    # Period
    quota_eur: float
    days_elapsed: int
    days_remaining: int
    # Closed
    closed_won_eur: float
    # Pipeline
    pipeline_stage3_eur: float     # negotiation/closing — highest probability
    pipeline_stage2_eur: float     # proposal/demo
    pipeline_stage1_eur: float     # discovery/qualification
    # Historical performance
    win_rate_pct: float            # historical win rate 0-100
    avg_deal_size_eur: float
    avg_sales_cycle_days: int
    historical_attainment_pcts: list[float]   # last 3-4 periods [0-100+]
    # Activity
    deals_created_30d: int
    meetings_30d: int
    proposals_sent_30d: int
    # Manager assessment
    rep_confidence_score: float    # manager's confidence 0-10


@dataclass
class AttainmentResult:
    rep_id: str
    rep_name: str
    region: str
    segment: str
    quota_eur: float
    current_attainment_pct: float
    projected_attainment_pct: float
    projected_closed_eur: float
    gap_to_quota_eur: float           # positive = still needed; negative = overachievement
    attainment_outcome: AttainmentOutcome
    confidence: AttainmentConfidence
    quota_action: QuotaAction
    run_rate_pct: float
    pipeline_coverage_ratio: float
    weighted_pipeline_eur: float
    historical_avg_attainment_pct: float
    prediction_drivers: list[str]
    prediction_risks: list[str]
    action_plan: list[str]

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "region": self.region,
            "segment": self.segment,
            "quota_eur": self.quota_eur,
            "current_attainment_pct": self.current_attainment_pct,
            "projected_attainment_pct": self.projected_attainment_pct,
            "projected_closed_eur": self.projected_closed_eur,
            "gap_to_quota_eur": self.gap_to_quota_eur,
            "attainment_outcome": self.attainment_outcome.value,
            "confidence": self.confidence.value,
            "quota_action": self.quota_action.value,
            "run_rate_pct": self.run_rate_pct,
            "pipeline_coverage_ratio": self.pipeline_coverage_ratio,
            "weighted_pipeline_eur": self.weighted_pipeline_eur,
            "historical_avg_attainment_pct": self.historical_avg_attainment_pct,
            "prediction_drivers": self.prediction_drivers,
            "prediction_risks": self.prediction_risks,
            "action_plan": self.action_plan,
        }


def _current_attainment_pct(inp: AttainmentInput) -> float:
    if inp.quota_eur <= 0:
        return 0.0
    return round((inp.closed_won_eur / inp.quota_eur) * 100.0, 1)


def _run_rate_pct(inp: AttainmentInput) -> float:
    total_days = inp.days_elapsed + inp.days_remaining
    if total_days <= 0 or inp.quota_eur <= 0 or inp.days_elapsed <= 0:
        return 0.0
    expected = inp.quota_eur * (inp.days_elapsed / total_days)
    if expected <= 0:
        return 0.0
    return round((inp.closed_won_eur / expected) * 100.0, 1)


def _weighted_pipeline_eur(inp: AttainmentInput) -> float:
    wr = inp.win_rate_pct / 100.0
    weighted = (
        inp.pipeline_stage3_eur * wr
        + inp.pipeline_stage2_eur * wr * 0.6
        + inp.pipeline_stage1_eur * wr * 0.3
    )
    return round(weighted, 0)


def _pipeline_coverage_ratio(inp: AttainmentInput) -> float:
    remaining = max(0.0, inp.quota_eur - inp.closed_won_eur)
    if remaining <= 0:
        return 99.0
    total_pipeline = inp.pipeline_stage1_eur + inp.pipeline_stage2_eur + inp.pipeline_stage3_eur
    return round(total_pipeline / remaining, 2)


def _historical_avg_attainment(inp: AttainmentInput) -> float:
    if not inp.historical_attainment_pcts:
        return 80.0  # assume average if no history
    return round(sum(inp.historical_attainment_pcts) / len(inp.historical_attainment_pcts), 1)


def _projected_attainment(
    inp: AttainmentInput,
    weighted_pipeline: float,
    hist_avg: float,
    run_rate: float,
) -> float:
    # Model: closed + weighted pipeline (adjusted for time)
    total_days = inp.days_elapsed + inp.days_remaining
    time_factor = inp.days_remaining / total_days if total_days > 0 else 0.0
    # Adjust pipeline by time available vs average cycle
    if inp.avg_sales_cycle_days > 0:
        closeable_ratio = min(1.0, inp.days_remaining / inp.avg_sales_cycle_days)
    else:
        closeable_ratio = 1.0
    adjusted_pipeline = weighted_pipeline * closeable_ratio
    projected_close = inp.closed_won_eur + adjusted_pipeline
    if inp.quota_eur <= 0:
        return 0.0
    # Blend with historical performance (20% weight)
    model_pct = (projected_close / inp.quota_eur) * 100.0
    blended = model_pct * 0.8 + hist_avg * 0.2
    # Apply run-rate pressure if very behind
    if run_rate < 50 and inp.days_remaining < 30:
        blended = blended * 0.85
    return round(min(200.0, max(0.0, blended)), 1)


def _attainment_outcome(projected: float) -> AttainmentOutcome:
    if projected >= 110:
        return AttainmentOutcome.OVERACHIEVE
    if projected >= 90:
        return AttainmentOutcome.ACHIEVE
    if projected >= 70:
        return AttainmentOutcome.SLIGHT_MISS
    if projected >= 50:
        return AttainmentOutcome.MISS
    return AttainmentOutcome.CRITICAL_MISS


def _confidence(inp: AttainmentInput, coverage: float, hist_avg: float, run_rate: float) -> AttainmentConfidence:
    score = 0.0
    if coverage >= 3:
        score += 2.0
    elif coverage >= 2:
        score += 1.0
    if len(inp.historical_attainment_pcts) >= 3:
        score += 2.0
    elif len(inp.historical_attainment_pcts) >= 1:
        score += 1.0
    if run_rate >= 90:
        score += 2.0
    elif run_rate >= 70:
        score += 1.0
    if inp.rep_confidence_score >= 7:
        score += 2.0
    elif inp.rep_confidence_score >= 5:
        score += 1.0
    if inp.deals_created_30d >= 3:
        score += 1.0
    if score >= 7:
        return AttainmentConfidence.HIGH
    if score >= 5:
        return AttainmentConfidence.MEDIUM
    if score >= 3:
        return AttainmentConfidence.LOW
    return AttainmentConfidence.VERY_LOW


def _quota_action(outcome: AttainmentOutcome, days_remaining: int) -> QuotaAction:
    if outcome == AttainmentOutcome.CRITICAL_MISS:
        return QuotaAction.ESCALATE
    if outcome == AttainmentOutcome.MISS or (outcome == AttainmentOutcome.SLIGHT_MISS and days_remaining < 30):
        return QuotaAction.INTERVENTION
    if outcome in (AttainmentOutcome.SLIGHT_MISS, AttainmentOutcome.ACHIEVE) and days_remaining >= 30:
        return QuotaAction.ACCELERATE
    return QuotaAction.MAINTAIN


def _prediction_drivers(
    inp: AttainmentInput,
    weighted: float,
    coverage: float,
    run_rate: float,
    hist_avg: float,
) -> list[str]:
    drivers: list[str] = []
    if inp.closed_won_eur > 0:
        drivers.append(f"Closé YTD: {inp.closed_won_eur:,.0f}€ — base solide")
    if coverage >= 3:
        drivers.append(f"Couverture pipeline {coverage:.1f}x — réservoir suffisant")
    if run_rate >= 90:
        drivers.append(f"Run rate {run_rate:.0f}% — rythme en ligne avec l'objectif")
    if hist_avg >= 90:
        drivers.append(f"Historique d'atteinte fort — moyenne {hist_avg:.0f}%")
    if inp.pipeline_stage3_eur > 0:
        drivers.append(f"Deals closing stage: {inp.pipeline_stage3_eur:,.0f}€ — à signer")
    if inp.rep_confidence_score >= 7:
        drivers.append(f"Confiance rep élevée ({inp.rep_confidence_score}/10)")
    return drivers


def _prediction_risks(
    inp: AttainmentInput,
    coverage: float,
    run_rate: float,
    projected: float,
    hist_avg: float,
) -> list[str]:
    risks: list[str] = []
    if coverage < 2:
        risks.append(f"Couverture pipeline insuffisante ({coverage:.1f}x) — pipeline sous-alimenté")
    if run_rate < 70:
        risks.append(f"Run rate faible ({run_rate:.0f}%) — rythme de closing en retard")
    if inp.avg_sales_cycle_days > inp.days_remaining:
        risks.append(
            f"Cycle moyen ({inp.avg_sales_cycle_days}j) > jours restants ({inp.days_remaining}j) — deals hors fenêtre"
        )
    if inp.deals_created_30d < 2:
        risks.append(f"Génération de pipeline faible ({inp.deals_created_30d} deals/30j)")
    if inp.win_rate_pct < 15:
        risks.append(f"Taux de signature faible ({inp.win_rate_pct:.0f}%) — conversion à améliorer")
    if hist_avg < 70:
        risks.append(f"Historique d'atteinte fragile — moyenne {hist_avg:.0f}%")
    if projected < 70:
        risks.append("Projection en deçà des 70% — intervention nécessaire")
    if inp.rep_confidence_score < 4:
        risks.append(f"Confiance rep faible ({inp.rep_confidence_score}/10) — signal d'alerte")
    return risks


def _action_plan(
    action: QuotaAction,
    inp: AttainmentInput,
    gap: float,
    projected: float,
) -> list[str]:
    plan: list[str] = []
    if action == QuotaAction.ESCALATE:
        plan.append("Escalade manager immédiate — revue pipeline deal by deal")
        plan.append("Identifier les deals à impact rapide — closing sprint 30j")
        plan.append("Support commercial renforcé — coach deal, exec selling")
        plan.append("Revoir les objectifs de fin de période avec le management")
    elif action == QuotaAction.INTERVENTION:
        plan.append("Session de coaching hebdomadaire — focus deals closing stage")
        plan.append(f"Combler le gap de {gap:,.0f}€ — plan d'action deal par deal")
        plan.append("Accélérer les deals en stage 2 — propositions et démos urgentes")
        plan.append("Revue pipeline bi-mensuelle avec le manager")
    elif action == QuotaAction.ACCELERATE:
        plan.append("Accélérer le closing — réduire le cycle de vente de 20%")
        plan.append("Prioriser les deals à fort potentiel de closing rapide")
        plan.append("Maximiser les activités outbound pour alimenter la fin de période")
    else:
        plan.append("Maintenir la cadence — objectif quota sur la bonne trajectoire")
        plan.append("Anticiper le pipeline du trimestre suivant")
        plan.append("Chercher des opportunités d'expansion sur les comptes actifs")
    return plan


class QuotaAttainmentPredictor:
    def __init__(self) -> None:
        self._results: dict[str, AttainmentResult] = {}

    def predict(self, inp: AttainmentInput) -> AttainmentResult:
        current = _current_attainment_pct(inp)
        run_rate = _run_rate_pct(inp)
        weighted = _weighted_pipeline_eur(inp)
        coverage = _pipeline_coverage_ratio(inp)
        hist_avg = _historical_avg_attainment(inp)
        projected = _projected_attainment(inp, weighted, hist_avg, run_rate)
        outcome = _attainment_outcome(projected)
        confidence = _confidence(inp, coverage, hist_avg, run_rate)
        action = _quota_action(outcome, inp.days_remaining)
        gap = max(0.0, inp.quota_eur - inp.closed_won_eur - weighted)
        projected_closed = round(inp.closed_won_eur + weighted, 0)
        result = AttainmentResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            region=inp.region,
            segment=inp.segment,
            quota_eur=inp.quota_eur,
            current_attainment_pct=current,
            projected_attainment_pct=projected,
            projected_closed_eur=projected_closed,
            gap_to_quota_eur=round(gap, 0),
            attainment_outcome=outcome,
            confidence=confidence,
            quota_action=action,
            run_rate_pct=run_rate,
            pipeline_coverage_ratio=coverage,
            weighted_pipeline_eur=weighted,
            historical_avg_attainment_pct=hist_avg,
            prediction_drivers=_prediction_drivers(inp, weighted, coverage, run_rate, hist_avg),
            prediction_risks=_prediction_risks(inp, coverage, run_rate, projected, hist_avg),
            action_plan=_action_plan(action, inp, gap, projected),
        )
        self._results[inp.rep_id] = result
        return result

    def predict_batch(self, reps: list[AttainmentInput]) -> list[AttainmentResult]:
        results = [self.predict(r) for r in reps]
        return sorted(results, key=lambda r: r.projected_attainment_pct, reverse=True)

    def all_reps(self) -> list[AttainmentResult]:
        return sorted(self._results.values(), key=lambda r: r.projected_attainment_pct, reverse=True)

    def by_outcome(self, outcome: AttainmentOutcome) -> list[AttainmentResult]:
        return [r for r in self._results.values() if r.attainment_outcome == outcome]

    def by_action(self, action: QuotaAction) -> list[AttainmentResult]:
        return [r for r in self._results.values() if r.quota_action == action]

    def by_confidence(self, confidence: AttainmentConfidence) -> list[AttainmentResult]:
        return [r for r in self._results.values() if r.confidence == confidence]

    def at_risk_reps(self) -> list[AttainmentResult]:
        return [
            r for r in self._results.values()
            if r.attainment_outcome in (AttainmentOutcome.MISS, AttainmentOutcome.CRITICAL_MISS)
        ]

    def on_track_reps(self) -> list[AttainmentResult]:
        return [
            r for r in self._results.values()
            if r.attainment_outcome in (AttainmentOutcome.ACHIEVE, AttainmentOutcome.OVERACHIEVE)
        ]

    def overachievers(self) -> list[AttainmentResult]:
        return self.by_outcome(AttainmentOutcome.OVERACHIEVE)

    def critical_misses(self) -> list[AttainmentResult]:
        return self.by_outcome(AttainmentOutcome.CRITICAL_MISS)

    def needs_escalation(self) -> list[AttainmentResult]:
        return self.by_action(QuotaAction.ESCALATE)

    def avg_projected_attainment(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.projected_attainment_pct for r in self._results.values()) / len(self._results), 1)

    def total_projected_closed_eur(self) -> float:
        return sum(r.projected_closed_eur for r in self._results.values())

    def total_gap_eur(self) -> float:
        return sum(r.gap_to_quota_eur for r in self._results.values())

    def summary(self) -> dict:
        all_r = list(self._results.values())
        n = len(all_r)
        return {
            "total": n,
            "outcome_counts": {o.value: sum(1 for r in all_r if r.attainment_outcome == o) for o in AttainmentOutcome},
            "action_counts": {a.value: sum(1 for r in all_r if r.quota_action == a) for a in QuotaAction},
            "confidence_counts": {c.value: sum(1 for r in all_r if r.confidence == c) for c in AttainmentConfidence},
            "avg_projected_attainment_pct": self.avg_projected_attainment(),
            "total_projected_closed_eur": self.total_projected_closed_eur(),
            "total_gap_eur": self.total_gap_eur(),
            "critical_miss_count": len(self.critical_misses()),
            "escalation_count": len(self.needs_escalation()),
            "overachieve_count": len(self.overachievers()),
        }

    def reset(self) -> None:
        self._results.clear()
