from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class CalibrationRating(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class CalibrationRisk(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class BiasType(str, Enum):
    ACCURATE = "accurate"
    SANDBAGGING = "sandbagging"
    OVER_OPTIMISTIC = "over_optimistic"
    INCONSISTENT = "inconsistent"


class CalibrationAction(str, Enum):
    NO_ACTION = "no_action"
    COACHING_REQUIRED = "coaching_required"
    FORECAST_ADJUSTMENT = "forecast_adjustment"
    SYSTEM_OVERRIDE = "system_override"


@dataclass
class ForecastCalibrationInput:
    rep_id: str
    rep_name: str
    region: str
    quarter: str
    forecast_category: str
    forecasted_amount_usd: float
    closed_won_amount_usd: float
    deals_forecasted_count: int
    deals_closed_count: int
    avg_forecast_accuracy_last_4q_pct: float
    sandbagging_score: float
    optimism_bias_score: float
    stage_lag_days: float
    close_date_push_count: int
    late_stage_slippage_rate_pct: float
    commit_accuracy_pct: float
    best_case_accuracy_pct: float
    pipeline_coverage_ratio: float
    win_rate_trend: float
    forecast_change_frequency: int
    manager_override_count: int
    data_entry_lag_days: float


@dataclass
class ForecastCalibrationResult:
    rep_id: str
    rep_name: str
    calibration_rating: CalibrationRating
    calibration_risk: CalibrationRisk
    bias_type: BiasType
    calibration_action: CalibrationAction
    accuracy_score: float
    bias_score: float
    consistency_score: float
    data_quality_score: float
    calibration_composite: float
    is_sandbagging: bool
    is_over_optimistic: bool
    estimated_forecast_error_usd: float
    calibration_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id": self.rep_id,
            "rep_name": self.rep_name,
            "calibration_rating": self.calibration_rating.value,
            "calibration_risk": self.calibration_risk.value,
            "bias_type": self.bias_type.value,
            "calibration_action": self.calibration_action.value,
            "accuracy_score": self.accuracy_score,
            "bias_score": self.bias_score,
            "consistency_score": self.consistency_score,
            "data_quality_score": self.data_quality_score,
            "calibration_composite": self.calibration_composite,
            "is_sandbagging": self.is_sandbagging,
            "is_over_optimistic": self.is_over_optimistic,
            "estimated_forecast_error_usd": self.estimated_forecast_error_usd,
            "calibration_signal": self.calibration_signal,
        }


def _accuracy_score(inp: ForecastCalibrationInput) -> float:
    score = 0.0
    # Current quarter accuracy (0-40)
    if inp.forecasted_amount_usd > 0:
        actual_ratio = inp.closed_won_amount_usd / inp.forecasted_amount_usd
        pct_error = abs(1.0 - actual_ratio) * 100.0
    else:
        pct_error = 100.0
    if pct_error <= 5:
        score += 40.0
    elif pct_error <= 10:
        score += 32.0
    elif pct_error <= 20:
        score += 20.0
    elif pct_error <= 35:
        score += 10.0
    # Historical accuracy (0-30)
    hist = inp.avg_forecast_accuracy_last_4q_pct
    if hist >= 90:
        score += 30.0
    elif hist >= 80:
        score += 22.0
    elif hist >= 70:
        score += 14.0
    elif hist >= 55:
        score += 6.0
    # Commit accuracy (0-20)
    commit = inp.commit_accuracy_pct
    if commit >= 85:
        score += 20.0
    elif commit >= 75:
        score += 14.0
    elif commit >= 60:
        score += 7.0
    # Deal count accuracy (0-10)
    if inp.deals_forecasted_count > 0:
        deal_ratio = abs(inp.deals_closed_count / inp.deals_forecasted_count - 1.0)
        if deal_ratio <= 0.10:
            score += 10.0
        elif deal_ratio <= 0.25:
            score += 6.0
        elif deal_ratio <= 0.50:
            score += 2.0
    return max(0.0, min(100.0, round(score, 1)))


def _bias_score(inp: ForecastCalibrationInput) -> float:
    # Higher score = more biased (bad)
    score = 0.0
    # Sandbagging indicator (0-30)
    score += min(30.0, inp.sandbagging_score * 0.30)
    # Over-optimism indicator (0-30)
    score += min(30.0, inp.optimism_bias_score * 0.30)
    # Close date push frequency (0-20)
    if inp.close_date_push_count >= 5:
        score += 20.0
    elif inp.close_date_push_count >= 3:
        score += 14.0
    elif inp.close_date_push_count >= 2:
        score += 8.0
    elif inp.close_date_push_count >= 1:
        score += 3.0
    # Stage lag (0-20): deals lingering past benchmarks
    if inp.stage_lag_days >= 30:
        score += 20.0
    elif inp.stage_lag_days >= 20:
        score += 14.0
    elif inp.stage_lag_days >= 10:
        score += 7.0
    return max(0.0, min(100.0, round(score, 1)))


def _consistency_score(inp: ForecastCalibrationInput) -> float:
    score = 0.0
    # Low forecast change frequency (0-35): thrash = poor forecast discipline
    if inp.forecast_change_frequency <= 2:
        score += 35.0
    elif inp.forecast_change_frequency <= 4:
        score += 25.0
    elif inp.forecast_change_frequency <= 7:
        score += 12.0
    # Manager override rate (0-30): high overrides = rep forecasts untrustworthy
    if inp.manager_override_count == 0:
        score += 30.0
    elif inp.manager_override_count == 1:
        score += 20.0
    elif inp.manager_override_count == 2:
        score += 10.0
    # Late stage slippage rate (0-20)
    if inp.late_stage_slippage_rate_pct <= 10:
        score += 20.0
    elif inp.late_stage_slippage_rate_pct <= 20:
        score += 14.0
    elif inp.late_stage_slippage_rate_pct <= 35:
        score += 6.0
    # Pipeline coverage ratio health (0-15)
    if 3.0 <= inp.pipeline_coverage_ratio <= 5.0:
        score += 15.0
    elif 2.0 <= inp.pipeline_coverage_ratio < 3.0:
        score += 10.0
    elif 5.0 < inp.pipeline_coverage_ratio <= 7.0:
        score += 8.0
    return max(0.0, min(100.0, round(score, 1)))


def _data_quality_score(inp: ForecastCalibrationInput) -> float:
    score = 0.0
    # CRM entry lag (0-40): fast updates = high quality
    if inp.data_entry_lag_days <= 1:
        score += 40.0
    elif inp.data_entry_lag_days <= 2:
        score += 30.0
    elif inp.data_entry_lag_days <= 5:
        score += 18.0
    elif inp.data_entry_lag_days <= 10:
        score += 8.0
    # Best case accuracy (0-30)
    if inp.best_case_accuracy_pct >= 80:
        score += 30.0
    elif inp.best_case_accuracy_pct >= 65:
        score += 20.0
    elif inp.best_case_accuracy_pct >= 50:
        score += 10.0
    # Win rate trend (0-30): positive trend indicates healthy pipeline mgmt
    if inp.win_rate_trend >= 0.5:
        score += 30.0
    elif inp.win_rate_trend >= 0:
        score += 20.0
    elif inp.win_rate_trend >= -0.5:
        score += 10.0
    return max(0.0, min(100.0, round(score, 1)))


def _composite(accuracy: float, bias: float, consistency: float, data_quality: float) -> float:
    # For calibration: accuracy and consistency are good, bias is bad
    # Composite = HIGHER is BETTER calibrated
    # Invert bias: (100 - bias)
    raw = accuracy * 0.35 + (100.0 - bias) * 0.25 + consistency * 0.25 + data_quality * 0.15
    return round(raw, 1)


def _calibration_rating(composite: float) -> CalibrationRating:
    if composite >= 75:
        return CalibrationRating.EXCELLENT
    if composite >= 55:
        return CalibrationRating.GOOD
    if composite >= 35:
        return CalibrationRating.FAIR
    return CalibrationRating.POOR


def _calibration_risk(composite: float) -> CalibrationRisk:
    if composite < 25:
        return CalibrationRisk.CRITICAL
    if composite < 40:
        return CalibrationRisk.HIGH
    if composite < 60:
        return CalibrationRisk.MODERATE
    return CalibrationRisk.LOW


def _bias_type(inp: ForecastCalibrationInput) -> BiasType:
    if inp.sandbagging_score > 60 and inp.optimism_bias_score < 30:
        return BiasType.SANDBAGGING
    if inp.optimism_bias_score > 60 and inp.sandbagging_score < 30:
        return BiasType.OVER_OPTIMISTIC
    if inp.sandbagging_score > 40 and inp.optimism_bias_score > 40:
        return BiasType.INCONSISTENT
    # Also detect from actual data: consistently under-forecasting
    if inp.forecasted_amount_usd > 0:
        ratio = inp.closed_won_amount_usd / inp.forecasted_amount_usd
        if ratio > 1.25:
            return BiasType.SANDBAGGING
        if ratio < 0.70:
            return BiasType.OVER_OPTIMISTIC
    return BiasType.ACCURATE


def _calibration_action(risk: CalibrationRisk, bias: BiasType) -> CalibrationAction:
    if risk == CalibrationRisk.CRITICAL:
        return CalibrationAction.SYSTEM_OVERRIDE
    if risk == CalibrationRisk.HIGH:
        if bias in (BiasType.SANDBAGGING, BiasType.OVER_OPTIMISTIC):
            return CalibrationAction.FORECAST_ADJUSTMENT
        return CalibrationAction.COACHING_REQUIRED
    if risk == CalibrationRisk.MODERATE:
        return CalibrationAction.COACHING_REQUIRED
    return CalibrationAction.NO_ACTION


def _estimated_forecast_error_usd(inp: ForecastCalibrationInput, composite: float) -> float:
    error_rate = (100.0 - composite) / 100.0
    return round(inp.forecasted_amount_usd * error_rate, 2)


def _calibration_signal(inp: ForecastCalibrationInput, bias: BiasType) -> str:
    if bias == BiasType.SANDBAGGING:
        ratio = inp.closed_won_amount_usd / max(1, inp.forecasted_amount_usd)
        return f"sandbagging detected — closed {ratio:.0%} of forecast; quota pressure likely"
    if bias == BiasType.OVER_OPTIMISTIC:
        if inp.forecasted_amount_usd > 0:
            gap = inp.forecasted_amount_usd - inp.closed_won_amount_usd
            return f"over-optimistic — missed forecast by ${gap:,.0f}; close date pushes: {inp.close_date_push_count}"
    if inp.data_entry_lag_days > 5:
        return f"CRM data lag {inp.data_entry_lag_days:.0f} days — forecast accuracy compromised by stale data"
    if inp.manager_override_count >= 3:
        return f"manager overrode forecast {inp.manager_override_count}x this quarter — rep forecasting untrusted"
    if inp.late_stage_slippage_rate_pct >= 30:
        return f"late stage slippage {inp.late_stage_slippage_rate_pct:.0f}% — deals not closing as forecasted"
    return f"forecast accuracy {inp.avg_forecast_accuracy_last_4q_pct:.0f}% (4Q avg)"


class ForecastCalibrationEngine:
    def __init__(self) -> None:
        self._results: dict[str, ForecastCalibrationResult] = {}
        self._forecast_values: dict[str, float] = {}

    def assess(self, inp: ForecastCalibrationInput) -> ForecastCalibrationResult:
        accuracy = _accuracy_score(inp)
        bias = _bias_score(inp)
        consistency = _consistency_score(inp)
        data_quality = _data_quality_score(inp)
        composite = _composite(accuracy, bias, consistency, data_quality)

        rating = _calibration_rating(composite)
        risk = _calibration_risk(composite)
        bias_type = _bias_type(inp)
        action = _calibration_action(risk, bias_type)

        is_sandbagging = bias_type == BiasType.SANDBAGGING
        is_over_optimistic = bias_type == BiasType.OVER_OPTIMISTIC
        err_usd = _estimated_forecast_error_usd(inp, composite)
        signal = _calibration_signal(inp, bias_type)

        result = ForecastCalibrationResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            calibration_rating=rating,
            calibration_risk=risk,
            bias_type=bias_type,
            calibration_action=action,
            accuracy_score=accuracy,
            bias_score=bias,
            consistency_score=consistency,
            data_quality_score=data_quality,
            calibration_composite=composite,
            is_sandbagging=is_sandbagging,
            is_over_optimistic=is_over_optimistic,
            estimated_forecast_error_usd=err_usd,
            calibration_signal=signal,
        )
        self._results[inp.rep_id] = result
        self._forecast_values[inp.rep_id] = inp.forecasted_amount_usd
        return result

    def assess_batch(self, inputs: List[ForecastCalibrationInput]) -> List[ForecastCalibrationResult]:
        results = [self.assess(inp) for inp in inputs]
        results.sort(key=lambda r: r.calibration_composite, reverse=True)
        return results

    def get(self, rep_id: str) -> ForecastCalibrationResult | None:
        return self._results.get(rep_id)

    def all_reps(self) -> List[ForecastCalibrationResult]:
        return sorted(self._results.values(), key=lambda r: r.calibration_composite, reverse=True)

    def sandbagging_reps(self) -> List[ForecastCalibrationResult]:
        return [r for r in self._results.values() if r.is_sandbagging]

    def over_optimistic_reps(self) -> List[ForecastCalibrationResult]:
        return [r for r in self._results.values() if r.is_over_optimistic]

    def by_rating(self, rating: CalibrationRating) -> List[ForecastCalibrationResult]:
        return [r for r in self._results.values() if r.calibration_rating == rating]

    def by_risk(self, risk: CalibrationRisk) -> List[ForecastCalibrationResult]:
        return [r for r in self._results.values() if r.calibration_risk == risk]

    def avg_calibration_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.calibration_composite for r in self._results.values()) / len(self._results), 1)

    def total_forecast_error_exposure_usd(self) -> float:
        return round(sum(r.estimated_forecast_error_usd for r in self._results.values()), 2)

    def reset(self) -> None:
        self._results.clear()
        self._forecast_values.clear()

    def summary(self) -> dict:
        results = list(self._results.values())
        n = len(results)
        calibration_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        bias_type_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        for r in results:
            calibration_counts[r.calibration_rating.value] = calibration_counts.get(r.calibration_rating.value, 0) + 1
            risk_counts[r.calibration_risk.value] = risk_counts.get(r.calibration_risk.value, 0) + 1
            bias_type_counts[r.bias_type.value] = bias_type_counts.get(r.bias_type.value, 0) + 1
            action_counts[r.calibration_action.value] = action_counts.get(r.calibration_action.value, 0) + 1
        return {
            "total": n,
            "calibration_counts": calibration_counts,
            "risk_counts": risk_counts,
            "bias_type_counts": bias_type_counts,
            "action_counts": action_counts,
            "avg_calibration_composite": self.avg_calibration_composite(),
            "sandbagging_count": len(self.sandbagging_reps()),
            "over_optimistic_count": len(self.over_optimistic_reps()),
            "avg_accuracy_score": round(sum(r.accuracy_score for r in results) / n, 1) if n else 0.0,
            "avg_bias_score": round(sum(r.bias_score for r in results) / n, 1) if n else 0.0,
            "avg_consistency_score": round(sum(r.consistency_score for r in results) / n, 1) if n else 0.0,
            "avg_data_quality_score": round(sum(r.data_quality_score for r in results) / n, 1) if n else 0.0,
            "total_forecast_error_exposure_usd": self.total_forecast_error_exposure_usd(),
        }
