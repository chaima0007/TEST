"""
Sales Forecast Accuracy Intelligence Engine.

Évalue la fiabilité des prévisions d'un commercial (précision vs réel,
discipline de commit, exactitude des étapes, fiabilité du commit) et produit
un score composite avec pattern, sévérité, action, flags, revenue-at-risk et
un signal lisible.

Sous-scores : plus le score est élevé, plus le risque est élevé.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


# ===========================================================================
# Enums
# ===========================================================================

class ForecastRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class ForecastPattern(str, Enum):
    none = "none"
    chronic_over_forecasting = "chronic_over_forecasting"
    chronic_under_forecasting = "chronic_under_forecasting"
    end_of_quarter_cliff = "end_of_quarter_cliff"
    recency_bias_sandbagging = "recency_bias_sandbagging"
    stage_inflation_blindspot = "stage_inflation_blindspot"


class ForecastSeverity(str, Enum):
    precise = "precise"
    calibrating = "calibrating"
    drifting = "drifting"
    unreliable = "unreliable"


class ForecastAction(str, Enum):
    no_action = "no_action"
    forecast_calibration_coaching = "forecast_calibration_coaching"
    pipeline_inspection_coaching = "pipeline_inspection_coaching"
    stage_criteria_coaching = "stage_criteria_coaching"
    commit_discipline_coaching = "commit_discipline_coaching"
    forecast_reset_intervention = "forecast_reset_intervention"


# ===========================================================================
# Dataclasses
# ===========================================================================

@dataclass
class ForecastInput:
    rep_id: str = ""
    region: str = ""
    evaluation_period_id: str = ""
    forecast_vs_actual_variance_pct: float = 0.0
    over_forecast_frequency_pct: float = 0.0
    under_forecast_frequency_pct: float = 0.0
    commit_to_close_rate_pct: float = 1.0
    best_case_to_close_rate_pct: float = 0.0
    pipeline_to_quota_ratio: float = 0.0
    late_add_to_forecast_pct: float = 0.0
    deals_pulled_from_forecast_pct: float = 0.0
    avg_deal_slip_days: float = 0.0
    stage_advancement_accuracy_pct: float = 1.0
    close_date_accuracy_within_week_pct: float = 1.0
    forecast_change_frequency_per_qtr: float = 0.0
    upside_deals_closed_pct: float = 0.0
    commit_deals_lost_pct: float = 0.0
    sandbag_conversion_rate_pct: float = 0.0
    multi_quarter_slip_rate_pct: float = 0.0
    forecast_submitted_on_time_pct: float = 1.0
    total_deals_forecasted: int = 0
    avg_opportunity_value_usd: float = 0.0


@dataclass
class ForecastResult:
    rep_id: str
    region: str
    forecast_risk: ForecastRisk
    forecast_pattern: ForecastPattern
    forecast_severity: ForecastSeverity
    recommended_action: ForecastAction
    accuracy_score: float
    discipline_score: float
    stage_score: float
    commit_score: float
    forecast_composite: float
    has_forecast_gap: bool
    requires_forecast_coaching: bool
    estimated_revenue_at_risk_usd: float
    forecast_signal: str

    def to_dict(self) -> Dict:
        return {
            "rep_id": self.rep_id,
            "region": self.region,
            "forecast_risk": self.forecast_risk.value,
            "forecast_pattern": self.forecast_pattern.value,
            "forecast_severity": self.forecast_severity.value,
            "recommended_action": self.recommended_action.value,
            "accuracy_score": self.accuracy_score,
            "discipline_score": self.discipline_score,
            "stage_score": self.stage_score,
            "commit_score": self.commit_score,
            "forecast_composite": self.forecast_composite,
            "has_forecast_gap": self.has_forecast_gap,
            "requires_forecast_coaching": self.requires_forecast_coaching,
            "estimated_revenue_at_risk_usd": self.estimated_revenue_at_risk_usd,
            "forecast_signal": self.forecast_signal,
        }


# ===========================================================================
# Engine
# ===========================================================================

class SalesForecastAccuracyIntelligenceEngine:
    def __init__(self) -> None:
        self._results: List[ForecastResult] = []

    # ---- Sous-scores ------------------------------------------------------

    def _accuracy_score(self, inp: ForecastInput) -> float:
        score = 0.0
        v = inp.forecast_vs_actual_variance_pct
        if v >= 0.40:
            score += 40
        elif v >= 0.20:
            score += 22
        elif v >= 0.10:
            score += 8

        cl = inp.commit_deals_lost_pct
        if cl >= 0.40:
            score += 35
        elif cl >= 0.20:
            score += 18

        cd = inp.close_date_accuracy_within_week_pct
        if cd <= 0.30:
            score += 25
        elif cd <= 0.55:
            score += 12

        return float(min(score, 100.0))

    def _discipline_score(self, inp: ForecastInput) -> float:
        score = 0.0
        cf = inp.forecast_change_frequency_per_qtr
        if cf >= 5.0:
            score += 40
        elif cf >= 3.0:
            score += 22
        elif cf >= 1.5:
            score += 8

        la = inp.late_add_to_forecast_pct
        if la >= 0.40:
            score += 35
        elif la >= 0.20:
            score += 18

        sl = inp.multi_quarter_slip_rate_pct
        if sl >= 0.35:
            score += 25
        elif sl >= 0.15:
            score += 12

        return float(min(score, 100.0))

    def _stage_score(self, inp: ForecastInput) -> float:
        score = 0.0
        sa = inp.stage_advancement_accuracy_pct
        if sa <= 0.40:
            score += 40
        elif sa <= 0.60:
            score += 22
        elif sa <= 0.75:
            score += 8

        dp = inp.deals_pulled_from_forecast_pct
        if dp >= 0.35:
            score += 35
        elif dp >= 0.20:
            score += 18

        sd = inp.avg_deal_slip_days
        if sd >= 30:
            score += 25
        elif sd >= 14:
            score += 12

        return float(min(score, 100.0))

    def _commit_score(self, inp: ForecastInput) -> float:
        score = 0.0
        cc = inp.commit_to_close_rate_pct
        if cc <= 0.40:
            score += 45
        elif cc <= 0.60:
            score += 25
        elif cc <= 0.75:
            score += 10

        of = inp.over_forecast_frequency_pct
        if of >= 0.60:
            score += 30
        elif of >= 0.40:
            score += 15

        uf = inp.under_forecast_frequency_pct
        if uf >= 0.50:
            score += 25
        elif uf >= 0.30:
            score += 12

        return float(min(score, 100.0))

    # ---- Composite, niveaux, pattern, action ------------------------------

    def _composite(self, accuracy: float, discipline: float, stage: float, commit: float) -> float:
        weighted = accuracy * 0.35 + discipline * 0.25 + stage * 0.25 + commit * 0.15
        return float(min(round(weighted, 1), 100.0))

    def _risk_level(self, composite: float) -> ForecastRisk:
        if composite >= 60:
            return ForecastRisk.critical
        if composite >= 40:
            return ForecastRisk.high
        if composite >= 20:
            return ForecastRisk.moderate
        return ForecastRisk.low

    def _severity(self, composite: float) -> ForecastSeverity:
        if composite >= 60:
            return ForecastSeverity.unreliable
        if composite >= 40:
            return ForecastSeverity.drifting
        if composite >= 20:
            return ForecastSeverity.calibrating
        return ForecastSeverity.precise

    def _detect_pattern(
        self,
        inp: ForecastInput,
        accuracy: float,
        discipline: float,
        stage: float,
        commit: float,
    ) -> ForecastPattern:
        if inp.stage_advancement_accuracy_pct <= 0.35 and inp.deals_pulled_from_forecast_pct >= 0.30:
            return ForecastPattern.stage_inflation_blindspot
        if inp.over_forecast_frequency_pct >= 0.55 and inp.commit_deals_lost_pct >= 0.30:
            return ForecastPattern.chronic_over_forecasting
        if discipline >= 35 and inp.multi_quarter_slip_rate_pct >= 0.25:
            return ForecastPattern.end_of_quarter_cliff
        if inp.sandbag_conversion_rate_pct >= 0.50 and inp.late_add_to_forecast_pct >= 0.30:
            return ForecastPattern.recency_bias_sandbagging
        if inp.under_forecast_frequency_pct >= 0.45 and commit >= 30:
            return ForecastPattern.chronic_under_forecasting
        return ForecastPattern.none

    def _action(self, risk: ForecastRisk, pattern: ForecastPattern) -> ForecastAction:
        if risk == ForecastRisk.low:
            return ForecastAction.no_action
        if risk == ForecastRisk.moderate:
            return ForecastAction.forecast_calibration_coaching
        if risk == ForecastRisk.high:
            if pattern == ForecastPattern.end_of_quarter_cliff:
                return ForecastAction.pipeline_inspection_coaching
            if pattern == ForecastPattern.recency_bias_sandbagging:
                return ForecastAction.forecast_calibration_coaching
            return ForecastAction.commit_discipline_coaching
        # critical
        if pattern == ForecastPattern.stage_inflation_blindspot:
            return ForecastAction.stage_criteria_coaching
        if pattern == ForecastPattern.chronic_over_forecasting:
            return ForecastAction.commit_discipline_coaching
        return ForecastAction.forecast_reset_intervention

    # ---- Flags, revenue, signal -------------------------------------------

    def _has_forecast_gap(self, composite: float, inp: ForecastInput) -> bool:
        if composite >= 40:
            return True
        if inp.commit_deals_lost_pct >= 0.30:
            return True
        if inp.commit_to_close_rate_pct <= 0.50:
            return True
        return False

    def _requires_forecast_coaching(self, composite: float, inp: ForecastInput) -> bool:
        if composite >= 30:
            return True
        if inp.forecast_vs_actual_variance_pct >= 0.15:
            return True
        if inp.stage_advancement_accuracy_pct <= 0.60:
            return True
        return False

    def _estimated_revenue_at_risk(self, inp: ForecastInput, composite: float) -> float:
        return round(
            inp.total_deals_forecasted
            * inp.avg_opportunity_value_usd
            * inp.commit_deals_lost_pct
            * (composite / 100.0),
            2,
        )

    def _signal(self, inp: ForecastInput, pattern: ForecastPattern, composite: float) -> str:
        if pattern == ForecastPattern.none and composite < 20:
            return (
                "Forecast accuracy healthy — variance, commit discipline, "
                "and stage accuracy within benchmarks"
            )

        parts: List[str] = []
        if inp.forecast_vs_actual_variance_pct >= 0.10:
            parts.append(f"{inp.forecast_vs_actual_variance_pct * 100:.0f}% forecast variance")
        if inp.commit_to_close_rate_pct <= 0.75:
            parts.append(f"commit-to-close rate {inp.commit_to_close_rate_pct * 100:.0f}%")
        if inp.commit_deals_lost_pct >= 0.20:
            parts.append(f"{inp.commit_deals_lost_pct * 100:.0f}% committed deals lost")

        if pattern == ForecastPattern.none:
            prefix = "Forecast risk"
        else:
            prefix = pattern.value.replace("_", " ").capitalize()

        if not parts:
            parts.append("forecast accuracy degrading")

        return f"{prefix}: {'; '.join(parts)} (composite {composite:.0f})"

    # ---- Assess / batch / summary -----------------------------------------

    def assess(self, inp: ForecastInput) -> ForecastResult:
        accuracy = self._accuracy_score(inp)
        discipline = self._discipline_score(inp)
        stage = self._stage_score(inp)
        commit = self._commit_score(inp)
        composite = self._composite(accuracy, discipline, stage, commit)
        risk = self._risk_level(composite)
        pattern = self._detect_pattern(inp, accuracy, discipline, stage, commit)
        severity = self._severity(composite)
        action = self._action(risk, pattern)

        result = ForecastResult(
            rep_id=inp.rep_id,
            region=inp.region,
            forecast_risk=risk,
            forecast_pattern=pattern,
            forecast_severity=severity,
            recommended_action=action,
            accuracy_score=accuracy,
            discipline_score=discipline,
            stage_score=stage,
            commit_score=commit,
            forecast_composite=composite,
            has_forecast_gap=self._has_forecast_gap(composite, inp),
            requires_forecast_coaching=self._requires_forecast_coaching(composite, inp),
            estimated_revenue_at_risk_usd=self._estimated_revenue_at_risk(inp, composite),
            forecast_signal=self._signal(inp, pattern, composite),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ForecastInput]) -> List[ForecastResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        n = len(self._results)
        if n == 0:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_forecast_composite": 0.0,
                "forecast_gap_count": 0,
                "coaching_count": 0,
                "avg_accuracy_score": 0.0,
                "avg_discipline_score": 0.0,
                "avg_stage_score": 0.0,
                "avg_commit_score": 0.0,
                "total_estimated_revenue_at_risk_usd": 0.0,
            }

        def counts(attr: str) -> Dict[str, int]:
            out: Dict[str, int] = {}
            for r in self._results:
                key = getattr(r, attr).value
                out[key] = out.get(key, 0) + 1
            return out

        def avg(attr: str) -> float:
            return round(sum(getattr(r, attr) for r in self._results) / n, 1)

        return {
            "total": n,
            "risk_counts": counts("forecast_risk"),
            "pattern_counts": counts("forecast_pattern"),
            "severity_counts": counts("forecast_severity"),
            "action_counts": counts("recommended_action"),
            "avg_forecast_composite": avg("forecast_composite"),
            "forecast_gap_count": sum(1 for r in self._results if r.has_forecast_gap),
            "coaching_count": sum(1 for r in self._results if r.requires_forecast_coaching),
            "avg_accuracy_score": avg("accuracy_score"),
            "avg_discipline_score": avg("discipline_score"),
            "avg_stage_score": avg("stage_score"),
            "avg_commit_score": avg("commit_score"),
            "total_estimated_revenue_at_risk_usd": round(
                sum(r.estimated_revenue_at_risk_usd for r in self._results), 2
            ),
        }
