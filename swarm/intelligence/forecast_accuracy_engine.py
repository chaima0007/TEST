from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ForecastAccuracy(str, Enum):
    EXCELLENT = "excellent"   # ≥90 %
    GOOD = "good"             # ≥75 %
    FAIR = "fair"             # ≥55 %
    POOR = "poor"             # < 55 %


class ForecastBias(str, Enum):
    OPTIMISTIC = "optimistic"   # forecast > actual by > 10 %
    NEUTRAL = "neutral"         # within ± 10 %
    PESSIMISTIC = "pessimistic" # forecast < actual by > 10 %


class ForecastAction(str, Enum):
    CELEBRATE = "celebrate"     # excellent accuracy
    CALIBRATE = "calibrate"     # good but tuning needed
    IMPROVE = "improve"         # fair — significant gaps
    OVERHAUL = "overhaul"       # poor — systemic issues


class RepTier(str, Enum):
    TOP = "top"
    SOLID = "solid"
    DEVELOPING = "developing"
    STRUGGLING = "struggling"


@dataclass
class ForecastInput:
    rep_id: str
    rep_name: str
    region: str
    segment: str          # enterprise / mid_market / smb
    # Historical periods (last N quarters)
    periods: int          # number of periods evaluated (1-8)
    total_committed_eur: float   # sum of committed forecast across periods
    total_actual_eur: float      # sum of actual closed across periods
    # CRM data quality
    crm_update_lag_days: float   # avg days between activity and CRM update
    pipeline_coverage_ratio: float  # pipeline / quota (e.g., 3.2)
    # Behavioural signals
    late_stage_pull_ins: int    # deals moved in last minute to hit number
    sandbagging_events: int     # deals held back then over-achieved
    avg_deal_slip_days: float   # avg days deals slip from original close date
    quota_eur: float            # total quota for evaluated periods


@dataclass
class ForecastResult:
    rep_id: str
    rep_name: str
    region: str
    segment: str
    accuracy_pct: float
    accuracy_tier: ForecastAccuracy
    bias: ForecastBias
    forecast_action: ForecastAction
    rep_tier: RepTier
    attainment_pct: float
    variance_eur: float          # actual - committed (positive = beat)
    accuracy_drivers: list[str]
    accuracy_gaps: list[str]
    coaching_recommendations: list[str]
    reliability_score: float     # 0-100, composite

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "region": self.region,
            "segment": self.segment,
            "accuracy_pct": self.accuracy_pct,
            "accuracy_tier": self.accuracy_tier.value,
            "bias": self.bias.value,
            "forecast_action": self.forecast_action.value,
            "rep_tier": self.rep_tier.value,
            "attainment_pct": self.attainment_pct,
            "variance_eur": self.variance_eur,
            "accuracy_drivers": self.accuracy_drivers,
            "accuracy_gaps": self.accuracy_gaps,
            "coaching_recommendations": self.coaching_recommendations,
            "reliability_score": self.reliability_score,
        }


def _accuracy_pct(inp: ForecastInput) -> float:
    if inp.total_committed_eur <= 0:
        return 0.0
    raw = 1.0 - abs(inp.total_actual_eur - inp.total_committed_eur) / inp.total_committed_eur
    return round(max(0.0, min(100.0, raw * 100.0)), 1)


def _attainment_pct(inp: ForecastInput) -> float:
    if inp.quota_eur <= 0:
        return 0.0
    return round((inp.total_actual_eur / inp.quota_eur) * 100.0, 1)


def _variance_eur(inp: ForecastInput) -> float:
    return round(inp.total_actual_eur - inp.total_committed_eur, 0)


def _accuracy_tier(accuracy: float) -> ForecastAccuracy:
    if accuracy >= 90:
        return ForecastAccuracy.EXCELLENT
    if accuracy >= 75:
        return ForecastAccuracy.GOOD
    if accuracy >= 55:
        return ForecastAccuracy.FAIR
    return ForecastAccuracy.POOR


def _bias(inp: ForecastInput) -> ForecastBias:
    if inp.total_committed_eur <= 0:
        return ForecastBias.NEUTRAL
    diff_pct = (inp.total_actual_eur - inp.total_committed_eur) / inp.total_committed_eur * 100.0
    if diff_pct > 10:
        return ForecastBias.PESSIMISTIC
    if diff_pct < -10:
        return ForecastBias.OPTIMISTIC
    return ForecastBias.NEUTRAL


def _forecast_action(tier: ForecastAccuracy) -> ForecastAction:
    if tier == ForecastAccuracy.EXCELLENT:
        return ForecastAction.CELEBRATE
    if tier == ForecastAccuracy.GOOD:
        return ForecastAction.CALIBRATE
    if tier == ForecastAccuracy.FAIR:
        return ForecastAction.IMPROVE
    return ForecastAction.OVERHAUL


def _rep_tier(attainment: float, accuracy: float) -> RepTier:
    if attainment >= 100 and accuracy >= 80:
        return RepTier.TOP
    if attainment >= 80 and accuracy >= 65:
        return RepTier.SOLID
    if attainment >= 60 or accuracy >= 55:
        return RepTier.DEVELOPING
    return RepTier.STRUGGLING


def _reliability_score(inp: ForecastInput, accuracy: float, attainment: float) -> float:
    score = 0.0
    # Accuracy component: 40 pts
    score += accuracy * 0.40
    # Attainment component: 20 pts
    score += min(20.0, attainment * 0.20)
    # CRM hygiene: lag ≤1d→10, ≤3d→7, ≤7d→4, else 0
    if inp.crm_update_lag_days <= 1:
        score += 10.0
    elif inp.crm_update_lag_days <= 3:
        score += 7.0
    elif inp.crm_update_lag_days <= 7:
        score += 4.0
    # Pipeline coverage: ≥4→10, ≥3→7, ≥2→4, else 0
    if inp.pipeline_coverage_ratio >= 4:
        score += 10.0
    elif inp.pipeline_coverage_ratio >= 3:
        score += 7.0
    elif inp.pipeline_coverage_ratio >= 2:
        score += 4.0
    # Deal discipline: pull-ins and sandbagging (up to -10 each)
    score -= min(10.0, inp.late_stage_pull_ins * 2.0)
    score -= min(5.0, inp.sandbagging_events * 1.5)
    # Slip penalty: avg slip > 14d→-5, > 7d→-3
    if inp.avg_deal_slip_days > 14:
        score -= 5.0
    elif inp.avg_deal_slip_days > 7:
        score -= 3.0
    return round(max(0.0, min(100.0, score)), 1)


def _accuracy_drivers(inp: ForecastInput, accuracy: float, attainment: float) -> list[str]:
    drivers: list[str] = []
    if accuracy >= 85:
        drivers.append(f"Précision forecast excellente ({accuracy:.0f}%) — prévisions très fiables")
    if attainment >= 100:
        drivers.append(f"Quota atteint à {attainment:.0f}% — performance commerciale solide")
    if inp.crm_update_lag_days <= 2:
        drivers.append(f"Hygiène CRM irréprochable — données à jour (lag {inp.crm_update_lag_days:.0f}j)")
    if inp.pipeline_coverage_ratio >= 3.5:
        drivers.append(f"Couverture pipeline élevée ({inp.pipeline_coverage_ratio:.1f}x) — visibilité long terme")
    if inp.sandbagging_events == 0 and inp.late_stage_pull_ins == 0:
        drivers.append("Comportement forecast propre — aucun sandbagging ni pull-in détecté")
    if inp.avg_deal_slip_days <= 5:
        drivers.append(f"Deals peu glissants ({inp.avg_deal_slip_days:.0f}j avg) — prévisions temporellement fiables")
    if inp.periods >= 4:
        drivers.append(f"Évaluée sur {inp.periods} trimestres — historique solide")
    return drivers


def _accuracy_gaps(inp: ForecastInput, accuracy: float, attainment: float, bias: ForecastBias) -> list[str]:
    gaps: list[str] = []
    if accuracy < 75:
        gaps.append(f"Précision insuffisante ({accuracy:.0f}%) — écart forecast/réel trop important")
    if bias == ForecastBias.OPTIMISTIC:
        gaps.append("Biais optimiste — forecast régulièrement > réalisé (sur-déclaration)")
    elif bias == ForecastBias.PESSIMISTIC:
        gaps.append("Biais pessimiste — forecast régulièrement < réalisé (sandbagging)")
    if inp.crm_update_lag_days > 7:
        gaps.append(f"Hygiène CRM insuffisante — lag moyen de {inp.crm_update_lag_days:.0f}j")
    if inp.pipeline_coverage_ratio < 2.5:
        gaps.append(f"Pipeline sous-alimenté ({inp.pipeline_coverage_ratio:.1f}x) — visibilité réduite")
    if inp.late_stage_pull_ins >= 3:
        gaps.append(f"{inp.late_stage_pull_ins} pull-ins last minute — distortion des prévisions")
    if inp.sandbagging_events >= 2:
        gaps.append(f"{inp.sandbagging_events} événements sandbagging — manque de transparence")
    if inp.avg_deal_slip_days > 14:
        gaps.append(f"Deals glissants en moyenne {inp.avg_deal_slip_days:.0f}j — prévisions de date non fiables")
    if attainment < 70:
        gaps.append(f"Attainment à {attainment:.0f}% — performance commerciale à améliorer")
    return gaps


def _coaching_recommendations(
    inp: ForecastInput, accuracy: float, attainment: float,
    bias: ForecastBias, action: ForecastAction
) -> list[str]:
    recs: list[str] = []
    if action == ForecastAction.CELEBRATE:
        recs.append("Partager les bonnes pratiques de forecast avec l'équipe")
        recs.append("Documenter la méthode de qualification pour en faire un standard")
        return recs
    if bias == ForecastBias.OPTIMISTIC:
        recs.append("Revoir les critères de commit — n'engager que les deals validés MEDDIC")
        recs.append("Instaurer un review hebdomadaire avec le manager avant le commit")
    elif bias == ForecastBias.PESSIMISTIC:
        recs.append("Corriger le sandbagging — aligner le forecast sur la réalité du pipeline")
        recs.append("Session 1:1 de calibration — analyser les deals sous-déclarés")
    if inp.crm_update_lag_days > 5:
        recs.append(f"Améliorer la cadence CRM — viser un lag < 24h (actuel: {inp.crm_update_lag_days:.0f}j)")
    if inp.pipeline_coverage_ratio < 2.5:
        recs.append("Intensifier la génération de pipeline — viser un coverage ≥ 3x quota")
    if inp.late_stage_pull_ins >= 3:
        recs.append("Éliminer les pull-ins late stage — qualifier le close date dès le début")
    if inp.avg_deal_slip_days > 14:
        recs.append("Améliorer la qualification des close dates — utiliser les jalons MEDDIC")
    if attainment < 80:
        recs.append("Plan d'amélioration 90j — objectifs hebdomadaires et coaching intensif")
    if action == ForecastAction.OVERHAUL:
        recs.append("Révision complète du processus de forecast — atelier avec l'équipe RevOps")
    return recs


class ForecastAccuracyEngine:
    def __init__(self) -> None:
        self._results: dict[str, ForecastResult] = {}

    def analyze(self, inp: ForecastInput) -> ForecastResult:
        accuracy = _accuracy_pct(inp)
        attainment = _attainment_pct(inp)
        variance = _variance_eur(inp)
        tier = _accuracy_tier(accuracy)
        bias = _bias(inp)
        action = _forecast_action(tier)
        rep_tier = _rep_tier(attainment, accuracy)
        reliability = _reliability_score(inp, accuracy, attainment)
        result = ForecastResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            region=inp.region,
            segment=inp.segment,
            accuracy_pct=accuracy,
            accuracy_tier=tier,
            bias=bias,
            forecast_action=action,
            rep_tier=rep_tier,
            attainment_pct=attainment,
            variance_eur=variance,
            accuracy_drivers=_accuracy_drivers(inp, accuracy, attainment),
            accuracy_gaps=_accuracy_gaps(inp, accuracy, attainment, bias),
            coaching_recommendations=_coaching_recommendations(inp, accuracy, attainment, bias, action),
            reliability_score=reliability,
        )
        self._results[inp.rep_id] = result
        return result

    def analyze_batch(self, reps: list[ForecastInput]) -> list[ForecastResult]:
        results = [self.analyze(r) for r in reps]
        return sorted(results, key=lambda r: r.accuracy_pct, reverse=True)

    def all_reps(self) -> list[ForecastResult]:
        return sorted(self._results.values(), key=lambda r: r.accuracy_pct, reverse=True)

    def by_accuracy(self, tier: ForecastAccuracy) -> list[ForecastResult]:
        return [r for r in self._results.values() if r.accuracy_tier == tier]

    def by_action(self, action: ForecastAction) -> list[ForecastResult]:
        return [r for r in self._results.values() if r.forecast_action == action]

    def by_bias(self, bias: ForecastBias) -> list[ForecastResult]:
        return [r for r in self._results.values() if r.bias == bias]

    def by_rep_tier(self, tier: RepTier) -> list[ForecastResult]:
        return [r for r in self._results.values() if r.rep_tier == tier]

    def excellent_forecasters(self) -> list[ForecastResult]:
        return self.by_accuracy(ForecastAccuracy.EXCELLENT)

    def needs_overhaul(self) -> list[ForecastResult]:
        return self.by_action(ForecastAction.OVERHAUL)

    def optimistic_reps(self) -> list[ForecastResult]:
        return self.by_bias(ForecastBias.OPTIMISTIC)

    def sandbagging_reps(self) -> list[ForecastResult]:
        return self.by_bias(ForecastBias.PESSIMISTIC)

    def top_performers(self) -> list[ForecastResult]:
        return self.by_rep_tier(RepTier.TOP)

    def avg_accuracy(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.accuracy_pct for r in self._results.values()) / len(self._results), 1)

    def avg_attainment(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.attainment_pct for r in self._results.values()) / len(self._results), 1)

    def avg_reliability(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.reliability_score for r in self._results.values()) / len(self._results), 1)

    def total_variance_eur(self) -> float:
        return sum(r.variance_eur for r in self._results.values())

    def summary(self) -> dict:
        all_r = list(self._results.values())
        n = len(all_r)
        return {
            "total": n,
            "accuracy_counts": {t.value: sum(1 for r in all_r if r.accuracy_tier == t) for t in ForecastAccuracy},
            "action_counts": {a.value: sum(1 for r in all_r if r.forecast_action == a) for a in ForecastAction},
            "bias_counts": {b.value: sum(1 for r in all_r if r.bias == b) for b in ForecastBias},
            "avg_accuracy_pct": self.avg_accuracy(),
            "avg_attainment_pct": self.avg_attainment(),
            "avg_reliability_score": self.avg_reliability(),
            "excellent_count": len(self.excellent_forecasters()),
            "overhaul_count": len(self.needs_overhaul()),
            "total_variance_eur": self.total_variance_eur(),
        }

    def reset(self) -> None:
        self._results.clear()
