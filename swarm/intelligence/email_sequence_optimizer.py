"""Email Sequence Optimizer — optimizes outreach sequence step timing and messaging."""

from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class SequenceStatus(str, Enum):
    EXCELLENT = "excellent"   # >=80
    GOOD = "good"             # >=60
    AVERAGE = "average"       # >=40
    POOR = "poor"             # >=20
    CRITICAL = "critical"     # <20


class StepType(str, Enum):
    EMAIL = "email"
    LINKEDIN = "linkedin"
    PHONE = "phone"
    VIDEO = "video"
    DIRECT_MAIL = "direct_mail"


class TouchpointStrategy(str, Enum):
    AGGRESSIVE = "aggressive"   # high frequency
    BALANCED = "balanced"       # standard cadence
    NURTURE = "nurture"         # slow burn
    REACTIVATION = "reactivation"  # re-engage cold leads


_OPTIMAL_GAPS_DAYS = {
    TouchpointStrategy.AGGRESSIVE: [0, 2, 4, 7, 10, 14],
    TouchpointStrategy.BALANCED:   [0, 3, 7, 14, 21, 28],
    TouchpointStrategy.NURTURE:    [0, 7, 14, 30, 45, 60],
    TouchpointStrategy.REACTIVATION: [0, 5, 12, 21, 35, 50],
}

_STEP_TYPE_OPEN_RATE = {
    StepType.EMAIL: 0.22,
    StepType.LINKEDIN: 0.45,
    StepType.PHONE: 0.30,
    StepType.VIDEO: 0.38,
    StepType.DIRECT_MAIL: 0.65,
}

_STEP_TYPE_REPLY_RATE = {
    StepType.EMAIL: 0.05,
    StepType.LINKEDIN: 0.12,
    StepType.PHONE: 0.18,
    StepType.VIDEO: 0.10,
    StepType.DIRECT_MAIL: 0.25,
}


@dataclass
class SequenceStep:
    step_number: int
    step_type: StepType
    day_offset: int          # days from sequence start
    subject_line: str
    body_preview: str        # first 100 chars
    open_rate_pct: float
    reply_rate_pct: float
    click_rate_pct: float
    unsubscribe_rate_pct: float
    sent_count: int


@dataclass
class SequenceInput:
    sequence_id: str
    sequence_name: str
    strategy: TouchpointStrategy
    steps: list[SequenceStep]
    target_industry: str
    target_persona: str   # e.g. "VP Sales", "CTO"
    avg_deal_size_eur: float
    total_prospects: int
    converted_prospects: int
    bounced_emails: int


@dataclass
class StepOptimization:
    step_number: int
    step_type: StepType
    current_day_offset: int
    recommended_day_offset: int
    timing_score: float
    performance_score: float
    issues: list[str]
    recommendations: list[str]


@dataclass
class SequenceResult:
    sequence_id: str
    sequence_name: str
    overall_score: float
    status: SequenceStatus
    strategy: TouchpointStrategy
    avg_open_rate_pct: float
    avg_reply_rate_pct: float
    conversion_rate_pct: float
    bounce_rate_pct: float
    step_optimizations: list[StepOptimization]
    sequence_signals: list[str]
    risk_signals: list[str]
    estimated_pipeline_eur: float
    recommended_strategy: TouchpointStrategy

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value
        d["strategy"] = self.strategy.value
        d["recommended_strategy"] = self.recommended_strategy.value
        for s in d["step_optimizations"]:
            s["step_type"] = StepType(s["step_type"]).value
        return d


def _timing_score(step: SequenceStep, strategy: TouchpointStrategy) -> float:
    """Score timing fit vs optimal gaps for this strategy."""
    optimal = _OPTIMAL_GAPS_DAYS.get(strategy, _OPTIMAL_GAPS_DAYS[TouchpointStrategy.BALANCED])
    idx = min(step.step_number - 1, len(optimal) - 1)
    optimal_day = optimal[idx]
    delta = abs(step.day_offset - optimal_day)
    return max(0, 100 - delta * 8)


def _performance_score(step: SequenceStep) -> float:
    """Score actual performance vs channel benchmarks."""
    benchmark_open = _STEP_TYPE_OPEN_RATE.get(step.step_type, 0.20) * 100
    benchmark_reply = _STEP_TYPE_REPLY_RATE.get(step.step_type, 0.05) * 100

    if step.sent_count == 0:
        return 50.0

    open_score = min(100, (step.open_rate_pct / benchmark_open) * 70) if benchmark_open > 0 else 50
    reply_score = min(100, (step.reply_rate_pct / benchmark_reply) * 100) if benchmark_reply > 0 else 50

    unsub_penalty = min(30, step.unsubscribe_rate_pct * 10)
    return max(0, open_score * 0.45 + reply_score * 0.55 - unsub_penalty)


def _step_issues_and_recs(
    step: SequenceStep, timing: float, perf: float, strategy: TouchpointStrategy
) -> tuple[list[str], list[str]]:
    issues: list[str] = []
    recs: list[str] = []

    benchmark_open = _STEP_TYPE_OPEN_RATE.get(step.step_type, 0.20) * 100
    benchmark_reply = _STEP_TYPE_REPLY_RATE.get(step.step_type, 0.05) * 100

    if timing < 50:
        issues.append(f"Timing hors norme pour la stratégie {strategy.value}")
        recs.append("Réajuster le délai selon le calendrier optimal de la stratégie")
    if step.sent_count > 0 and step.open_rate_pct < benchmark_open * 0.6:
        issues.append(f"Taux d'ouverture faible ({step.open_rate_pct:.1f}% vs {benchmark_open:.0f}% benchmark)")
        recs.append("Tester un nouvel objet d'email — A/B test sur la ligne de sujet")
    if step.sent_count > 0 and step.reply_rate_pct < benchmark_reply * 0.5:
        issues.append(f"Taux de réponse faible ({step.reply_rate_pct:.1f}% vs {benchmark_reply:.0f}% benchmark)")
        recs.append("Raccourcir le message et ajouter un CTA plus direct")
    if step.unsubscribe_rate_pct > 2.0:
        issues.append(f"Taux de désabonnement élevé ({step.unsubscribe_rate_pct:.1f}%)")
        recs.append("Réduire la fréquence ou requalifier la liste de prospects")
    if step.sent_count > 0 and step.click_rate_pct < 1.0 and step.step_type == StepType.EMAIL:
        recs.append("Ajouter un lien CTA clair (case study, démo, calendly)")

    return issues, recs


def _overall_score(inp: SequenceInput, steps_scores: list[tuple[float, float]]) -> float:
    """Weighted: avg_timing(30%) + avg_performance(40%) + conversion(20%) + bounce_penalty(10%)."""
    if not steps_scores:
        return 0.0
    avg_timing = sum(t for t, _ in steps_scores) / len(steps_scores)
    avg_perf = sum(p for _, p in steps_scores) / len(steps_scores)

    conv_rate = (inp.converted_prospects / max(1, inp.total_prospects)) * 100
    conv_score = min(100, conv_rate * 10)  # 10% conversion = 100 score

    bounce_rate = (inp.bounced_emails / max(1, inp.total_prospects)) * 100
    bounce_penalty = min(30, bounce_rate * 3)

    raw = avg_timing * 0.30 + avg_perf * 0.40 + conv_score * 0.20 - bounce_penalty * 0.10
    return round(max(0, min(100, raw)), 2)


def _status(score: float) -> SequenceStatus:
    if score >= 80:
        return SequenceStatus.EXCELLENT
    if score >= 60:
        return SequenceStatus.GOOD
    if score >= 40:
        return SequenceStatus.AVERAGE
    if score >= 20:
        return SequenceStatus.POOR
    return SequenceStatus.CRITICAL


def _recommended_strategy(inp: SequenceInput, score: float) -> TouchpointStrategy:
    conv_rate = inp.converted_prospects / max(1, inp.total_prospects)
    if conv_rate >= 0.10:
        return TouchpointStrategy.AGGRESSIVE
    if conv_rate >= 0.05:
        return inp.strategy  # keep current
    if inp.total_prospects > 0 and inp.converted_prospects == 0:
        return TouchpointStrategy.REACTIVATION
    return TouchpointStrategy.NURTURE


def _build_signals(
    inp: SequenceInput, score: float, status: SequenceStatus
) -> tuple[list[str], list[str]]:
    signals: list[str] = []
    risks: list[str] = []

    conv_rate = (inp.converted_prospects / max(1, inp.total_prospects)) * 100
    bounce_rate = (inp.bounced_emails / max(1, inp.total_prospects)) * 100

    if status in (SequenceStatus.EXCELLENT, SequenceStatus.GOOD):
        signals.append(f"Séquence performante — score {score:.0f}/100")
    if conv_rate >= 8:
        signals.append(f"Taux de conversion excellent ({conv_rate:.1f}%) — séquence à dupliquer")
    if conv_rate >= 3:
        signals.append(f"Conversion positive ({conv_rate:.1f}%) — optimisation marginale possible")
    if bounce_rate < 2:
        signals.append("Liste propre — faible taux de bounce")
    if len(inp.steps) >= 5:
        signals.append("Séquence complète — bonne couverture du cycle de décision")

    if bounce_rate >= 5:
        risks.append(f"Taux de bounce élevé ({bounce_rate:.1f}%) — nettoyer la liste")
    if conv_rate < 2 and inp.total_prospects > 50:
        risks.append(f"Conversion faible ({conv_rate:.1f}%) — revoir le ciblage et le message")
    if status in (SequenceStatus.POOR, SequenceStatus.CRITICAL):
        risks.append("Séquence sous-performante — révision complète recommandée")
    if len(inp.steps) < 4:
        risks.append("Trop peu d'étapes — les prospects abandonnent avant la décision")

    return signals, risks


def _estimate_pipeline(inp: SequenceInput, score: float) -> float:
    conv_rate = inp.converted_prospects / max(1, inp.total_prospects)
    projected_conv = inp.total_prospects * conv_rate * (1 + score / 200)
    return round(projected_conv * inp.avg_deal_size_eur, -2)


class EmailSequenceOptimizer:
    """Analyzes and optimizes outreach email sequences."""

    def __init__(self) -> None:
        self._results: dict[str, SequenceResult] = {}

    def optimize(self, inp: SequenceInput) -> SequenceResult:
        step_opts: list[StepOptimization] = []
        scores: list[tuple[float, float]] = []

        for step in inp.steps:
            t_score = _timing_score(step, inp.strategy)
            p_score = _performance_score(step)
            issues, recs = _step_issues_and_recs(step, t_score, p_score, inp.strategy)

            optimal = _OPTIMAL_GAPS_DAYS.get(inp.strategy, _OPTIMAL_GAPS_DAYS[TouchpointStrategy.BALANCED])
            rec_day = optimal[min(step.step_number - 1, len(optimal) - 1)]

            step_opts.append(StepOptimization(
                step_number=step.step_number,
                step_type=step.step_type,
                current_day_offset=step.day_offset,
                recommended_day_offset=rec_day,
                timing_score=round(t_score, 2),
                performance_score=round(p_score, 2),
                issues=issues,
                recommendations=recs,
            ))
            scores.append((t_score, p_score))

        overall = _overall_score(inp, scores)
        status = _status(overall)
        rec_strategy = _recommended_strategy(inp, overall)
        signals, risks = _build_signals(inp, overall, status)
        pipeline = _estimate_pipeline(inp, overall)

        total_sent = sum(s.sent_count for s in inp.steps)
        if total_sent > 0:
            avg_open = sum(s.open_rate_pct * s.sent_count for s in inp.steps) / total_sent
            avg_reply = sum(s.reply_rate_pct * s.sent_count for s in inp.steps) / total_sent
        else:
            avg_open = sum(s.open_rate_pct for s in inp.steps) / max(1, len(inp.steps))
            avg_reply = sum(s.reply_rate_pct for s in inp.steps) / max(1, len(inp.steps))

        conv_rate = (inp.converted_prospects / max(1, inp.total_prospects)) * 100
        bounce_rate = (inp.bounced_emails / max(1, inp.total_prospects)) * 100

        result = SequenceResult(
            sequence_id=inp.sequence_id,
            sequence_name=inp.sequence_name,
            overall_score=overall,
            status=status,
            strategy=inp.strategy,
            avg_open_rate_pct=round(avg_open, 2),
            avg_reply_rate_pct=round(avg_reply, 2),
            conversion_rate_pct=round(conv_rate, 2),
            bounce_rate_pct=round(bounce_rate, 2),
            step_optimizations=step_opts,
            sequence_signals=signals,
            risk_signals=risks,
            estimated_pipeline_eur=pipeline,
            recommended_strategy=rec_strategy,
        )
        self._results[inp.sequence_id] = result
        return result

    def optimize_batch(self, inputs: list[SequenceInput]) -> list[SequenceResult]:
        return sorted([self.optimize(inp) for inp in inputs], key=lambda r: r.overall_score, reverse=True)

    def get(self, sequence_id: str) -> Optional[SequenceResult]:
        return self._results.get(sequence_id)

    def all_sequences(self) -> list[SequenceResult]:
        return sorted(self._results.values(), key=lambda r: r.overall_score, reverse=True)

    def by_status(self, status: SequenceStatus) -> list[SequenceResult]:
        return [r for r in self.all_sequences() if r.status == status]

    def excellent_sequences(self) -> list[SequenceResult]:
        return self.by_status(SequenceStatus.EXCELLENT)

    def critical_sequences(self) -> list[SequenceResult]:
        return self.by_status(SequenceStatus.CRITICAL)

    def needs_attention(self) -> list[SequenceResult]:
        return [
            r for r in self.all_sequences()
            if r.status in (SequenceStatus.POOR, SequenceStatus.CRITICAL)
        ]

    def top_pipeline(self, n: int = 5) -> list[SequenceResult]:
        return sorted(self.all_sequences(), key=lambda r: r.estimated_pipeline_eur, reverse=True)[:n]

    def total_pipeline_eur(self) -> float:
        return round(sum(r.estimated_pipeline_eur for r in self.all_sequences()), 2)

    def summary(self) -> dict:
        all_r = self.all_sequences()
        if not all_r:
            return {
                "total": 0,
                "status_counts": {},
                "avg_score": 0.0,
                "avg_conversion_rate_pct": 0.0,
                "total_pipeline_eur": 0.0,
            }
        status_counts: dict[str, int] = {}
        total_score = 0.0
        total_conv = 0.0
        for r in all_r:
            status_counts[r.status.value] = status_counts.get(r.status.value, 0) + 1
            total_score += r.overall_score
            total_conv += r.conversion_rate_pct
        n = len(all_r)
        return {
            "total": n,
            "status_counts": status_counts,
            "avg_score": round(total_score / n, 1),
            "avg_conversion_rate_pct": round(total_conv / n, 2),
            "total_pipeline_eur": self.total_pipeline_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
