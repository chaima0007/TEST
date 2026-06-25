from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GapSeverity(str, Enum):
    NONE = "none"
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class PipelineAction(str, Enum):
    MAINTAIN = "maintain"
    BUILD = "build"          # proactive pipeline building
    ACCELERATE = "accelerate"  # push existing deals through
    EMERGENCY = "emergency"    # immediate corrective action


class QuotaRisk(str, Enum):
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BEHIND = "behind"
    CRITICAL = "critical"


class CoverageHealth(str, Enum):
    HEALTHY = "healthy"     # ≥4x coverage
    ADEQUATE = "adequate"   # ≥3x
    THIN = "thin"           # ≥2x
    INSUFFICIENT = "insufficient"  # < 2x


@dataclass
class PipelineInput:
    rep_id: str
    rep_name: str
    region: str
    segment: str
    # Quota & attainment
    quota_eur: float
    closed_won_eur: float        # MTD or QTD closed
    days_elapsed: int            # days into period
    days_remaining: int          # days left in period
    # Pipeline composition
    pipeline_total_eur: float    # total open pipeline
    stage_1_eur: float           # discovery/qualification
    stage_2_eur: float           # proposal/demo
    stage_3_eur: float           # negotiation/closing
    # Pipeline quality
    avg_deal_size_eur: float
    avg_sales_cycle_days: int
    win_rate_pct: float          # historical win rate 0-100
    # Activity signals
    new_opps_created_30d: int
    demos_completed_30d: int
    proposals_sent_30d: int
    follow_up_rate_pct: float    # 0-100


@dataclass
class PipelineGapResult:
    rep_id: str
    rep_name: str
    region: str
    segment: str
    quota_eur: float
    gap_eur: float                  # quota remaining - expected from pipeline
    gap_severity: GapSeverity
    pipeline_action: PipelineAction
    quota_risk: QuotaRisk
    coverage_health: CoverageHealth
    coverage_ratio: float           # pipeline / quota_remaining
    expected_close_eur: float       # pipeline * win_rate adjusted
    quota_remaining_eur: float
    attainment_pct: float
    run_rate_pct: float             # pace vs. quota based on time elapsed
    gap_drivers: list[str]
    gap_closers: list[str]          # actions to close the gap
    pipeline_score: float           # 0-100

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "region": self.region,
            "segment": self.segment,
            "quota_eur": self.quota_eur,
            "gap_eur": self.gap_eur,
            "gap_severity": self.gap_severity.value,
            "pipeline_action": self.pipeline_action.value,
            "quota_risk": self.quota_risk.value,
            "coverage_health": self.coverage_health.value,
            "coverage_ratio": self.coverage_ratio,
            "expected_close_eur": self.expected_close_eur,
            "quota_remaining_eur": self.quota_remaining_eur,
            "attainment_pct": self.attainment_pct,
            "run_rate_pct": self.run_rate_pct,
            "gap_drivers": self.gap_drivers,
            "gap_closers": self.gap_closers,
            "pipeline_score": self.pipeline_score,
        }


def _quota_remaining(inp: PipelineInput) -> float:
    return max(0.0, inp.quota_eur - inp.closed_won_eur)


def _attainment_pct(inp: PipelineInput) -> float:
    if inp.quota_eur <= 0:
        return 0.0
    return round((inp.closed_won_eur / inp.quota_eur) * 100.0, 1)


def _run_rate_pct(inp: PipelineInput) -> float:
    total_days = inp.days_elapsed + inp.days_remaining
    if total_days <= 0 or inp.quota_eur <= 0:
        return 0.0
    expected_at_pace = inp.quota_eur * (inp.days_elapsed / total_days)
    return round((inp.closed_won_eur / expected_at_pace) * 100.0, 1) if expected_at_pace > 0 else 0.0


def _expected_close_eur(inp: PipelineInput) -> float:
    wr = inp.win_rate_pct / 100.0
    # Weight later stages higher (stage_3 at full rate, stage_2 at 60%, stage_1 at 30%)
    weighted = (
        inp.stage_3_eur * wr
        + inp.stage_2_eur * wr * 0.6
        + inp.stage_1_eur * wr * 0.3
    )
    return round(weighted, 0)


def _coverage_ratio(inp: PipelineInput) -> float:
    remaining = _quota_remaining(inp)
    if remaining <= 0:
        return 99.0
    return round(inp.pipeline_total_eur / remaining, 2)


def _coverage_health(ratio: float) -> CoverageHealth:
    if ratio >= 4:
        return CoverageHealth.HEALTHY
    if ratio >= 3:
        return CoverageHealth.ADEQUATE
    if ratio >= 2:
        return CoverageHealth.THIN
    return CoverageHealth.INSUFFICIENT


def _gap_eur(inp: PipelineInput, expected: float) -> float:
    remaining = _quota_remaining(inp)
    return round(max(0.0, remaining - expected), 0)


def _gap_severity(gap: float, quota: float) -> GapSeverity:
    if quota <= 0:
        return GapSeverity.NONE
    pct = gap / quota * 100
    if pct >= 40:
        return GapSeverity.CRITICAL
    if pct >= 25:
        return GapSeverity.SEVERE
    if pct >= 15:
        return GapSeverity.MODERATE
    if pct >= 5:
        return GapSeverity.MINOR
    return GapSeverity.NONE


def _quota_risk(attainment: float, run_rate: float, gap_severity: GapSeverity) -> QuotaRisk:
    if gap_severity == GapSeverity.CRITICAL or (run_rate < 60 and attainment < 40):
        return QuotaRisk.CRITICAL
    if gap_severity == GapSeverity.SEVERE or run_rate < 75:
        return QuotaRisk.BEHIND
    if gap_severity in (GapSeverity.MODERATE, GapSeverity.MINOR) or run_rate < 90:
        return QuotaRisk.AT_RISK
    return QuotaRisk.ON_TRACK


def _pipeline_action(risk: QuotaRisk, coverage: CoverageHealth) -> PipelineAction:
    if risk == QuotaRisk.CRITICAL or coverage == CoverageHealth.INSUFFICIENT:
        return PipelineAction.EMERGENCY
    if risk == QuotaRisk.BEHIND or coverage == CoverageHealth.THIN:
        return PipelineAction.BUILD
    if risk == QuotaRisk.AT_RISK:
        return PipelineAction.ACCELERATE
    return PipelineAction.MAINTAIN


def _pipeline_score(inp: PipelineInput, coverage: float, run_rate: float) -> float:
    score = 0.0
    # Coverage (30 pts)
    if coverage >= 4:
        score += 30.0
    elif coverage >= 3:
        score += 22.0
    elif coverage >= 2:
        score += 12.0
    elif coverage >= 1:
        score += 5.0
    # Run rate (25 pts)
    score += min(25.0, run_rate * 0.25)
    # Activity signals (25 pts)
    score += min(10.0, inp.new_opps_created_30d * 2.0)
    score += min(8.0, inp.demos_completed_30d * 2.0)
    score += min(7.0, inp.proposals_sent_30d * 2.0)
    # Pipeline quality (20 pts)
    stage_3_ratio = inp.stage_3_eur / inp.pipeline_total_eur if inp.pipeline_total_eur > 0 else 0
    score += min(10.0, stage_3_ratio * 20.0)
    if inp.win_rate_pct >= 25:
        score += 6.0
    elif inp.win_rate_pct >= 15:
        score += 3.0
    if inp.follow_up_rate_pct >= 80:
        score += 4.0
    elif inp.follow_up_rate_pct >= 60:
        score += 2.0
    return round(min(100.0, max(0.0, score)), 1)


def _gap_drivers(inp: PipelineInput, gap: float, coverage: CoverageHealth, run_rate: float) -> list[str]:
    drivers: list[str] = []
    if coverage == CoverageHealth.INSUFFICIENT:
        drivers.append(f"Couverture pipeline insuffisante — {inp.pipeline_total_eur / max(1, _quota_remaining(inp)):.1f}x (seuil: 3x)")
    if coverage == CoverageHealth.THIN:
        drivers.append(f"Pipeline mince — couverture {inp.pipeline_total_eur / max(1, _quota_remaining(inp)):.1f}x seulement")
    if run_rate < 75:
        drivers.append(f"Rythme de vente insuffisant — pace à {run_rate:.0f}% vs. objectif")
    if inp.new_opps_created_30d < 3:
        drivers.append(f"Génération de pipeline faible — seulement {inp.new_opps_created_30d} nouvelles opportunités sur 30j")
    if inp.stage_1_eur > inp.stage_2_eur + inp.stage_3_eur:
        drivers.append("Entonnoir déséquilibré — trop de pipeline en early stage")
    if inp.win_rate_pct < 15:
        drivers.append(f"Taux de signature faible ({inp.win_rate_pct:.0f}%) — qualification à améliorer")
    if inp.avg_sales_cycle_days > 90 and inp.days_remaining < inp.avg_sales_cycle_days:
        drivers.append(f"Cycle de vente moyen ({inp.avg_sales_cycle_days}j) > jours restants ({inp.days_remaining}j)")
    if inp.follow_up_rate_pct < 50:
        drivers.append(f"Suivi insuffisant — {inp.follow_up_rate_pct:.0f}% de taux de follow-up")
    return drivers


def _gap_closers(
    inp: PipelineInput, action: PipelineAction, gap: float, coverage: CoverageHealth
) -> list[str]:
    closers: list[str] = []
    if action == PipelineAction.EMERGENCY:
        closers.append("Prospection intensive immédiate — 10 nouveaux comptes ciblés cette semaine")
        closers.append("Réactiver les deals dormants — relancer les opportunités stagnantes")
        closers.append("Demander des introductions client — activer le réseau et les références")
        if inp.stage_3_eur > 0:
            closers.append("Concentrer 80% du temps sur les deals closing stage — maximiser la signature")
    elif action == PipelineAction.BUILD:
        closers.append("Intensifier la génération de pipeline — 5 nouveaux comptes par semaine")
        closers.append("Maximiser les activités outbound — emails, appels, LinkedIn")
        closers.append("Cibler les comptes ICP non prospectés — liste ABM à activer")
    elif action == PipelineAction.ACCELERATE:
        closers.append("Accélérer les deals en stage 2 et 3 — réduire le cycle de décision")
        closers.append("Qualifier et éliminer les deals fantômes — nettoyer le CRM")
        closers.append("Préparer les propositions en attente — débloquer les deals stagnants")
    else:
        closers.append("Maintenir la cadence d'activité — objectifs de pipeline respectés")
        closers.append("Chercher des opportunités d'expansion sur les comptes existants")
        closers.append("Anticiper le pipeline du prochain trimestre")
    return closers


class PipelineGapAnalyzerEngine:
    def __init__(self) -> None:
        self._results: dict[str, PipelineGapResult] = {}

    def analyze(self, inp: PipelineInput) -> PipelineGapResult:
        remaining = _quota_remaining(inp)
        attainment = _attainment_pct(inp)
        run_rate = _run_rate_pct(inp)
        expected = _expected_close_eur(inp)
        ratio = _coverage_ratio(inp)
        coverage = _coverage_health(ratio)
        gap = _gap_eur(inp, expected)
        severity = _gap_severity(gap, inp.quota_eur)
        risk = _quota_risk(attainment, run_rate, severity)
        action = _pipeline_action(risk, coverage)
        score = _pipeline_score(inp, ratio, run_rate)
        result = PipelineGapResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            region=inp.region,
            segment=inp.segment,
            quota_eur=inp.quota_eur,
            gap_eur=gap,
            gap_severity=severity,
            pipeline_action=action,
            quota_risk=risk,
            coverage_health=coverage,
            coverage_ratio=ratio,
            expected_close_eur=expected,
            quota_remaining_eur=remaining,
            attainment_pct=attainment,
            run_rate_pct=run_rate,
            gap_drivers=_gap_drivers(inp, gap, coverage, run_rate),
            gap_closers=_gap_closers(inp, action, gap, coverage),
            pipeline_score=score,
        )
        self._results[inp.rep_id] = result
        return result

    def analyze_batch(self, reps: list[PipelineInput]) -> list[PipelineGapResult]:
        results = [self.analyze(r) for r in reps]
        return sorted(results, key=lambda r: r.gap_eur, reverse=True)

    def all_reps(self) -> list[PipelineGapResult]:
        return sorted(self._results.values(), key=lambda r: r.gap_eur, reverse=True)

    def by_severity(self, severity: GapSeverity) -> list[PipelineGapResult]:
        return [r for r in self._results.values() if r.gap_severity == severity]

    def by_action(self, action: PipelineAction) -> list[PipelineGapResult]:
        return [r for r in self._results.values() if r.pipeline_action == action]

    def by_quota_risk(self, risk: QuotaRisk) -> list[PipelineGapResult]:
        return [r for r in self._results.values() if r.quota_risk == risk]

    def critical_gaps(self) -> list[PipelineGapResult]:
        return self.by_severity(GapSeverity.CRITICAL)

    def needs_emergency(self) -> list[PipelineGapResult]:
        return self.by_action(PipelineAction.EMERGENCY)

    def at_risk_reps(self) -> list[PipelineGapResult]:
        return [
            r for r in self._results.values()
            if r.quota_risk in (QuotaRisk.BEHIND, QuotaRisk.CRITICAL)
        ]

    def on_track_reps(self) -> list[PipelineGapResult]:
        return self.by_quota_risk(QuotaRisk.ON_TRACK)

    def avg_coverage_ratio(self) -> float:
        if not self._results:
            return 0.0
        ratios = [r.coverage_ratio for r in self._results.values() if r.coverage_ratio < 99]
        if not ratios:
            return 0.0
        return round(sum(ratios) / len(ratios), 2)

    def avg_pipeline_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.pipeline_score for r in self._results.values()) / len(self._results), 1)

    def total_gap_eur(self) -> float:
        return sum(r.gap_eur for r in self._results.values())

    def total_pipeline_eur(self) -> float:
        return sum(r.quota_eur for r in self._results.values())

    def summary(self) -> dict:
        all_r = list(self._results.values())
        n = len(all_r)
        return {
            "total": n,
            "severity_counts": {s.value: sum(1 for r in all_r if r.gap_severity == s) for s in GapSeverity},
            "action_counts": {a.value: sum(1 for r in all_r if r.pipeline_action == a) for a in PipelineAction},
            "risk_counts": {r.value: sum(1 for x in all_r if x.quota_risk == r) for r in QuotaRisk},
            "avg_pipeline_score": self.avg_pipeline_score(),
            "avg_coverage_ratio": self.avg_coverage_ratio(),
            "critical_count": len(self.critical_gaps()),
            "emergency_count": len(self.needs_emergency()),
            "total_gap_eur": self.total_gap_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
