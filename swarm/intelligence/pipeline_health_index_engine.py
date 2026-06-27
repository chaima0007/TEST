"""Module 42 — Pipeline Health Index Engine

Computes a composite Pipeline Health Index (PHI) for each pipeline entry,
aggregating velocity, deal quality, coverage, and risk factors to give
managers and reps a single actionable score and prioritised remediation plays.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class HealthGrade(str, Enum):
    EXCELLENT = "excellent"    # PHI ≥ 80 — pipeline firing on all cylinders
    GOOD      = "good"         # PHI ≥ 60 — strong with manageable gaps
    FAIR      = "fair"         # PHI ≥ 40 — notable weaknesses requiring attention
    POOR      = "poor"         # PHI ≥ 20 — significant risks — intervention needed
    CRITICAL  = "critical"     # PHI <  20 — pipeline in danger


class HealthDimension(str, Enum):
    VELOCITY    = "velocity"    # deals are moving fast enough
    QUALITY     = "quality"     # deal quality and qualification depth
    COVERAGE    = "coverage"    # pipeline coverage vs quota
    DIVERSITY   = "diversity"   # distribution across stages, reps, and regions
    ACTIVITY    = "activity"    # rep activity levels sustaining the pipeline


class PipelineRisk(str, Enum):
    LOW        = "low"         # minimal risk factors
    MODERATE   = "moderate"    # some risk factors present
    HIGH       = "high"        # multiple significant risk factors
    SEVERE     = "severe"      # pipeline at high risk of collapse


class HealthAction(str, Enum):
    ACCELERATE    = "accelerate"     # focus on closing velocity
    ADD_PIPELINE  = "add_pipeline"   # insufficient pipeline — generate more
    IMPROVE_QUAL  = "improve_qual"   # qualify deals better
    REBALANCE     = "rebalance"      # fix stage / rep / region concentration
    BOOST_ACTIVITY = "boost_activity" # rep activity too low
    MAINTAIN      = "maintain"       # sustain current performance


# ─── Input ────────────────────────────────────────────────────────────────────

@dataclass
class PipelineHealthInput:
    pipeline_id: str
    rep_id: str
    rep_name: str
    region: str
    # Pipeline volume
    total_deals: int
    total_pipeline_eur: float
    quota_eur: float
    # Stage distribution
    deals_early_stage: int        # discovery + qualification
    deals_mid_stage: int          # demo + proposal
    deals_late_stage: int         # negotiation + closing
    # Velocity
    avg_deal_age_days: float
    avg_cycle_length_benchmark_days: float
    deals_stale_30d: int          # deals with no activity in 30d
    # Quality signals
    avg_deal_health_score: float  # 0–100
    qualified_deals_pct: float    # % BANT-qualified or equivalent
    avg_next_step_adherence_pct: float   # % deals with next step defined
    # Activity
    calls_last_30d: int
    meetings_last_30d: int
    call_benchmark_30d: int
    meeting_benchmark_30d: int
    # Risk factors
    deals_single_threaded: int    # deals with only 1 stakeholder
    deals_no_exec_sponsor: int    # deals missing executive engagement
    deals_overdue_close_date: int # deals past original close date
    rep_win_rate_pct: float       # 0–100
    manager_reviewed_deals: int   # deals reviewed in last 30d
    forecast_accuracy_pct: float  # how accurate recent forecasts were 0–100


# ─── Output ───────────────────────────────────────────────────────────────────

@dataclass
class PipelineHealthResult:
    pipeline_id: str
    rep_id: str
    rep_name: str
    region: str
    health_grade: str
    pipeline_risk: str
    health_action: str
    phi_score: float            # 0–100 composite Pipeline Health Index
    velocity_score: float       # 0–100
    quality_score: float        # 0–100
    coverage_score: float       # 0–100
    activity_score: float       # 0–100
    coverage_ratio: float       # pipeline / quota
    stale_deal_pct: float       # % deals stale
    remediation_plays: list[str]
    risk_signals: list[str]
    manager_alerts: list[str]

    def to_dict(self) -> dict:
        return {
            "pipeline_id":       self.pipeline_id,
            "rep_id":            self.rep_id,
            "rep_name":          self.rep_name,
            "region":            self.region,
            "health_grade":      self.health_grade,
            "pipeline_risk":     self.pipeline_risk,
            "health_action":     self.health_action,
            "phi_score":         self.phi_score,
            "velocity_score":    self.velocity_score,
            "quality_score":     self.quality_score,
            "coverage_score":    self.coverage_score,
            "activity_score":    self.activity_score,
            "coverage_ratio":    self.coverage_ratio,
            "stale_deal_pct":    self.stale_deal_pct,
            "remediation_plays": self.remediation_plays,
            "risk_signals":      self.risk_signals,
            "manager_alerts":    self.manager_alerts,
        }


# ─── Engine ───────────────────────────────────────────────────────────────────

class PipelineHealthIndexEngine:

    def __init__(self) -> None:
        self._results: list[PipelineHealthResult] = []

    # ── Dimension scores ───────────────────────────────────────────────────────

    def _velocity_score(self, inp: PipelineHealthInput) -> float:
        if inp.avg_cycle_length_benchmark_days <= 0 or inp.total_deals == 0:
            return 50.0
        # Age ratio: how old vs benchmark
        age_ratio = inp.avg_deal_age_days / inp.avg_cycle_length_benchmark_days
        if age_ratio <= 0.5:    vel = 100.0
        elif age_ratio <= 0.8:  vel = 85.0
        elif age_ratio <= 1.0:  vel = 70.0
        elif age_ratio <= 1.3:  vel = 50.0
        elif age_ratio <= 1.6:  vel = 30.0
        else:                   vel = 10.0
        # Stale deal penalty
        stale_pct = inp.deals_stale_30d / inp.total_deals if inp.total_deals > 0 else 0
        vel -= min(30, stale_pct * 60)
        return max(0.0, min(100.0, vel))

    def _quality_score(self, inp: PipelineHealthInput) -> float:
        score = 0.0
        score += min(40, inp.avg_deal_health_score * 0.4)
        score += min(30, inp.qualified_deals_pct * 0.30)
        score += min(20, inp.avg_next_step_adherence_pct * 0.20)
        score += min(10, inp.rep_win_rate_pct * 0.10)
        return min(100.0, score)

    def _coverage_score(self, inp: PipelineHealthInput) -> float:
        if inp.quota_eur <= 0:
            return 80.0
        ratio = inp.total_pipeline_eur / inp.quota_eur
        if ratio >= 4.0:    cov = 100.0
        elif ratio >= 3.0:  cov = 85.0
        elif ratio >= 2.0:  cov = 70.0
        elif ratio >= 1.5:  cov = 55.0
        elif ratio >= 1.0:  cov = 40.0
        else:               cov = ratio * 40
        return min(100.0, cov)

    def _activity_score(self, inp: PipelineHealthInput) -> float:
        score = 0.0
        if inp.call_benchmark_30d > 0:
            call_ratio = inp.calls_last_30d / inp.call_benchmark_30d
            score += min(50, call_ratio * 50)
        else:
            score += 50
        if inp.meeting_benchmark_30d > 0:
            mtg_ratio = inp.meetings_last_30d / inp.meeting_benchmark_30d
            score += min(35, mtg_ratio * 35)
        else:
            score += 35
        # Manager review signal
        if inp.total_deals > 0:
            review_pct = inp.manager_reviewed_deals / inp.total_deals
            score += min(15, review_pct * 15)
        return min(100.0, score)

    def _phi_score(
        self,
        vel: float, qual: float, cov: float, act: float
    ) -> float:
        return round(vel * 0.25 + qual * 0.30 + cov * 0.25 + act * 0.20, 1)

    # ── Classification ─────────────────────────────────────────────────────────

    def _health_grade(self, phi: float) -> HealthGrade:
        if phi >= 80:   return HealthGrade.EXCELLENT
        if phi >= 60:   return HealthGrade.GOOD
        if phi >= 40:   return HealthGrade.FAIR
        if phi >= 20:   return HealthGrade.POOR
        return HealthGrade.CRITICAL

    def _pipeline_risk(self, inp: PipelineHealthInput, phi: float) -> PipelineRisk:
        risk_count = 0
        if inp.deals_single_threaded > inp.total_deals * 0.5:  risk_count += 1
        if inp.deals_overdue_close_date > inp.total_deals * 0.3: risk_count += 1
        if inp.deals_no_exec_sponsor > inp.total_deals * 0.4:  risk_count += 1
        if inp.deals_stale_30d > inp.total_deals * 0.3:        risk_count += 1
        if inp.rep_win_rate_pct < 25:                          risk_count += 1
        if phi < 30:                                           risk_count += 1
        if risk_count >= 4:    return PipelineRisk.SEVERE
        if risk_count >= 2:    return PipelineRisk.HIGH
        if risk_count >= 1:    return PipelineRisk.MODERATE
        return PipelineRisk.LOW

    def _health_action(
        self, phi: float, vel: float, qual: float, cov: float, act: float, inp: PipelineHealthInput
    ) -> HealthAction:
        # Coverage is the primary concern
        if cov < 40:
            return HealthAction.ADD_PIPELINE
        # Activity drives future pipeline
        if act < 40:
            return HealthAction.BOOST_ACTIVITY
        # Quality before velocity
        if qual < 40:
            return HealthAction.IMPROVE_QUAL
        # Late-stage concentration is fine; too many early deals with poor velocity
        if vel < 40:
            return HealthAction.ACCELERATE
        # All below average — balanced issue
        if phi < 50 and vel < 60 and qual < 60:
            return HealthAction.REBALANCE
        return HealthAction.MAINTAIN

    # ── Remediation plays ──────────────────────────────────────────────────────

    def _remediation_plays(
        self, inp: PipelineHealthInput, action: HealthAction
    ) -> list[str]:
        plays: list[str] = []
        if action == HealthAction.ADD_PIPELINE:
            plays.append(
                f"Pipeline insuffisant ({inp.total_pipeline_eur:,.0f}€ vs quota {inp.quota_eur:,.0f}€) — campagne de prospection intensive requise"
            )
            plays.append("Activer les referrals clients et les campagnes inbound pour régénérer la pipeline")
        if action == HealthAction.BOOST_ACTIVITY:
            plays.append(
                f"Activité faible ({inp.calls_last_30d} appels, {inp.meetings_last_30d} RDV) — fixer des objectifs journaliers avec le rep"
            )
        if action == HealthAction.IMPROVE_QUAL:
            plays.append(
                f"Qualification insuffisante ({inp.qualified_deals_pct:.0f}% BANT qualifiés) — session de coaching qualification avec manager"
            )
        if action == HealthAction.ACCELERATE:
            plays.append(
                f"Vélocité faible (âge moyen {inp.avg_deal_age_days:.0f}j vs benchmark {inp.avg_cycle_length_benchmark_days:.0f}j) — définir next steps impératifs sur tous les deals"
            )
        if inp.deals_stale_30d > 0:
            plays.append(
                f"{inp.deals_stale_30d} deal(s) sans activité en 30j — revue immédiate pour relancer ou disqualifier"
            )
        if inp.deals_single_threaded > 0:
            plays.append(
                f"{inp.deals_single_threaded} deal(s) en contact unique — plan de multi-threading à lancer sous 7j"
            )
        if inp.deals_overdue_close_date > 0:
            plays.append(
                f"{inp.deals_overdue_close_date} deal(s) dépassant la date de clôture prévue — revue du forecast obligatoire"
            )
        if not plays:
            plays.append(
                f"Pipeline sain (PHI: {self._phi_score(0, 0, 0, 0)}) — maintenir les bonnes pratiques en place"
            )
        return plays

    # ── Risk signals ───────────────────────────────────────────────────────────

    def _risk_signals(self, inp: PipelineHealthInput) -> list[str]:
        risks: list[str] = []
        if inp.total_pipeline_eur < inp.quota_eur:
            risks.append(
                f"Pipeline sous le quota: {inp.total_pipeline_eur:,.0f}€ vs {inp.quota_eur:,.0f}€ — manque de {inp.quota_eur - inp.total_pipeline_eur:,.0f}€"
            )
        if inp.deals_overdue_close_date > inp.total_deals * 0.3 and inp.total_deals > 0:
            pct = round(inp.deals_overdue_close_date / inp.total_deals * 100)
            risks.append(f"{pct}% des deals dépassent la date de clôture prévue — forecast peu fiable")
        if inp.deals_stale_30d > inp.total_deals * 0.25 and inp.total_deals > 0:
            risks.append(
                f"{inp.deals_stale_30d} deals sans activité récente — stagnation pipeline détectée"
            )
        if inp.rep_win_rate_pct < 25:
            risks.append(
                f"Taux de victoire faible ({inp.rep_win_rate_pct:.0f}%) — efficacité de closing en baisse"
            )
        if inp.forecast_accuracy_pct < 60:
            risks.append(
                f"Précision du forecast faible ({inp.forecast_accuracy_pct:.0f}%) — réviser les critères de qualification"
            )
        if inp.deals_no_exec_sponsor > inp.total_deals * 0.5 and inp.total_deals > 0:
            risks.append(
                f"{inp.deals_no_exec_sponsor} deals sans sponsor exécutif — risque de blocage décisionnel"
            )
        return risks

    # ── Manager alerts ─────────────────────────────────────────────────────────

    def _manager_alerts(
        self,
        inp: PipelineHealthInput,
        grade: HealthGrade,
        risk: PipelineRisk,
    ) -> list[str]:
        alerts: list[str] = []
        if grade == HealthGrade.CRITICAL:
            alerts.append(
                f"⚠ Pipeline CRITIQUE pour {inp.rep_name} ({inp.region}) — intervention manager immédiate requise"
            )
        if grade == HealthGrade.POOR:
            alerts.append(
                f"Pipeline dégradé pour {inp.rep_name} — planifier une revue pipeline complète cette semaine"
            )
        if risk == PipelineRisk.SEVERE:
            alerts.append(
                f"Risque SÉVÈRE détecté — {inp.rep_name} risque de manquer le quota de façon significative"
            )
        if inp.total_pipeline_eur < inp.quota_eur * 0.8:
            shortfall = inp.quota_eur - inp.total_pipeline_eur
            alerts.append(
                f"Pipeline sous-couvert: déficit de {shortfall:,.0f}€ — assistance génération pipeline requise"
            )
        return alerts

    # ── Main analysis ──────────────────────────────────────────────────────────

    def analyze(self, inp: PipelineHealthInput) -> PipelineHealthResult:
        vel  = round(self._velocity_score(inp), 1)
        qual = round(self._quality_score(inp), 1)
        cov  = round(self._coverage_score(inp), 1)
        act  = round(self._activity_score(inp), 1)
        phi  = self._phi_score(vel, qual, cov, act)

        coverage_ratio = round(inp.total_pipeline_eur / inp.quota_eur, 2) if inp.quota_eur > 0 else 0.0
        stale_pct = round(
            inp.deals_stale_30d / inp.total_deals * 100 if inp.total_deals > 0 else 0.0, 1
        )

        grade  = self._health_grade(phi)
        risk   = self._pipeline_risk(inp, phi)
        action = self._health_action(phi, vel, qual, cov, act, inp)

        result = PipelineHealthResult(
            pipeline_id       = inp.pipeline_id,
            rep_id            = inp.rep_id,
            rep_name          = inp.rep_name,
            region            = inp.region,
            health_grade      = grade.value,
            pipeline_risk     = risk.value,
            health_action     = action.value,
            phi_score         = phi,
            velocity_score    = vel,
            quality_score     = qual,
            coverage_score    = cov,
            activity_score    = act,
            coverage_ratio    = coverage_ratio,
            stale_deal_pct    = stale_pct,
            remediation_plays = self._remediation_plays(inp, action),
            risk_signals      = self._risk_signals(inp),
            manager_alerts    = self._manager_alerts(inp, grade, risk),
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[PipelineHealthInput]) -> list[PipelineHealthResult]:
        results = [self.analyze(inp) for inp in inputs]
        results.sort(key=lambda r: r.phi_score, reverse=True)
        return results

    # ── Helpers ────────────────────────────────────────────────────────────────

    def critical_pipelines(self) -> list[PipelineHealthResult]:
        return [r for r in self._results if r.health_grade == HealthGrade.CRITICAL.value]

    def severe_risk(self) -> list[PipelineHealthResult]:
        return [r for r in self._results if r.pipeline_risk == PipelineRisk.SEVERE.value]

    def needs_pipeline_add(self) -> list[PipelineHealthResult]:
        return [r for r in self._results if r.health_action == HealthAction.ADD_PIPELINE.value]

    def healthy_pipelines(self) -> list[PipelineHealthResult]:
        return [r for r in self._results if r.health_grade in (
            HealthGrade.EXCELLENT.value, HealthGrade.GOOD.value
        )]

    def at_risk_pipelines(self) -> list[PipelineHealthResult]:
        return [r for r in self._results if r.pipeline_risk in (
            PipelineRisk.HIGH.value, PipelineRisk.SEVERE.value
        )]

    def summary(self) -> dict:
        results = self._results
        n = len(results)
        if n == 0:
            return {
                "total": 0,
                "grade_counts": {},
                "risk_counts": {},
                "action_counts": {},
                "avg_phi_score": 0.0,
                "avg_velocity_score": 0.0,
                "avg_quality_score": 0.0,
                "avg_coverage_score": 0.0,
                "avg_activity_score": 0.0,
                "critical_count": 0,
                "severe_risk_count": 0,
            }
        grade_counts:  dict[str, int] = {}
        risk_counts:   dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_phi = total_vel = total_qual = total_cov = total_act = 0.0

        for r in results:
            grade_counts[r.health_grade]   = grade_counts.get(r.health_grade, 0) + 1
            risk_counts[r.pipeline_risk]   = risk_counts.get(r.pipeline_risk, 0) + 1
            action_counts[r.health_action] = action_counts.get(r.health_action, 0) + 1
            total_phi  += r.phi_score
            total_vel  += r.velocity_score
            total_qual += r.quality_score
            total_cov  += r.coverage_score
            total_act  += r.activity_score

        return {
            "total":               n,
            "grade_counts":        grade_counts,
            "risk_counts":         risk_counts,
            "action_counts":       action_counts,
            "avg_phi_score":       round(total_phi / n, 1),
            "avg_velocity_score":  round(total_vel / n, 1),
            "avg_quality_score":   round(total_qual / n, 1),
            "avg_coverage_score":  round(total_cov / n, 1),
            "avg_activity_score":  round(total_act / n, 1),
            "critical_count":      sum(1 for r in results if r.health_grade == HealthGrade.CRITICAL.value),
            "severe_risk_count":   sum(1 for r in results if r.pipeline_risk == PipelineRisk.SEVERE.value),
        }

    def reset(self) -> None:
        self._results = []
