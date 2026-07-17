"""Sales Competitive Win Rate Erosion Engine — detects when a rep's or team's win rate
against specific competitors is declining, identifying which battlecards need updating
and where competitive coaching can recover lost ground."""

from __future__ import annotations

import dataclasses
from enum import Enum


class WinRateRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ErosionPattern(str, Enum):
    none                  = "none"
    pricing_displacement  = "pricing_displacement"
    feature_regression    = "feature_regression"
    rep_skill_gap         = "rep_skill_gap"
    champion_poaching     = "champion_poaching"
    systematic_loss       = "systematic_loss"


class ErosionSeverity(str, Enum):
    stable    = "stable"
    declining = "declining"
    eroding   = "eroding"
    collapse  = "collapse"


class WinRateAction(str, Enum):
    no_action              = "no_action"
    battlecard_refresh     = "battlecard_refresh"
    competitive_coaching   = "competitive_coaching"
    pricing_strategy_review = "pricing_strategy_review"
    executive_competitive_review = "executive_competitive_review"


@dataclasses.dataclass
class CompetitiveWinRateInput:
    rep_id:                         str
    region:                         str
    evaluation_period_id:           str
    win_rate_current_pct:           float
    win_rate_prior_period_pct:      float
    win_rate_benchmark_pct:         float
    total_competitive_deals:        int
    wins_this_period:               int
    losses_this_period:             int
    losses_on_price_count:          int
    losses_on_features_count:       int
    losses_on_relationship_count:   int
    losses_on_timing_count:         int
    competitor_strength_score:      float
    battlecard_last_updated_days:   int
    battlecard_usage_pct:           float
    late_stage_loss_count:          int
    late_stage_total_count:         int
    champion_poached_count:         int
    consecutive_loss_streak:        int
    win_rate_trend_3_period_delta:  float
    avg_deal_size_won_usd:          float


@dataclasses.dataclass
class CompetitiveWinRateResult:
    rep_id:                      str
    region:                      str
    win_rate_risk:               WinRateRisk
    erosion_pattern:             ErosionPattern
    erosion_severity:            ErosionSeverity
    recommended_action:          WinRateAction
    win_rate_decline_score:      float
    deal_quality_score:          float
    competitive_readiness_score: float
    pattern_intensity_score:     float
    win_rate_composite:          float
    is_win_rate_eroding:         bool
    requires_coaching:           bool
    estimated_lost_revenue_usd:  float
    erosion_signal:              str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "win_rate_risk":                self.win_rate_risk.value,
            "erosion_pattern":              self.erosion_pattern.value,
            "erosion_severity":             self.erosion_severity.value,
            "recommended_action":           self.recommended_action.value,
            "win_rate_decline_score":       round(self.win_rate_decline_score, 1),
            "deal_quality_score":           round(self.deal_quality_score, 1),
            "competitive_readiness_score":  round(self.competitive_readiness_score, 1),
            "pattern_intensity_score":      round(self.pattern_intensity_score, 1),
            "win_rate_composite":           round(self.win_rate_composite, 1),
            "is_win_rate_eroding":          self.is_win_rate_eroding,
            "requires_coaching":            self.requires_coaching,
            "estimated_lost_revenue_usd":   round(self.estimated_lost_revenue_usd, 2),
            "erosion_signal":               self.erosion_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesCompetitiveWinRateErosionEngine:
    """Detects win rate erosion against competitors to enable targeted competitive improvement."""

    def __init__(self) -> None:
        self._results: list[CompetitiveWinRateResult] = []

    # ── sub-scores (HIGHER = more erosion) ──────────────────────────────────

    def _win_rate_decline_score(self, inp: CompetitiveWinRateInput) -> float:
        score = 0.0
        # Win rate vs benchmark
        benchmark_gap = inp.win_rate_benchmark_pct - inp.win_rate_current_pct
        if benchmark_gap >= 25:
            score += 45.0
        elif benchmark_gap >= 15:
            score += 28.0
        elif benchmark_gap >= 8:
            score += 14.0
        elif benchmark_gap >= 3:
            score += 6.0
        # Period over period decline
        period_decline = inp.win_rate_prior_period_pct - inp.win_rate_current_pct
        if period_decline >= 20:
            score += 35.0
        elif period_decline >= 12:
            score += 22.0
        elif period_decline >= 6:
            score += 10.0
        # 3-period trend
        if inp.win_rate_trend_3_period_delta <= -20:
            score += 20.0
        elif inp.win_rate_trend_3_period_delta <= -12:
            score += 12.0
        elif inp.win_rate_trend_3_period_delta <= -5:
            score += 5.0
        return _clamp(score)

    def _deal_quality_score(self, inp: CompetitiveWinRateInput) -> float:
        score = 0.0
        if inp.late_stage_total_count > 0:
            # Late-stage loss rate (losing when close to winning = bad)
            late_loss_rate = inp.late_stage_loss_count / inp.late_stage_total_count
            if late_loss_rate >= 0.60:
                score += 45.0
            elif late_loss_rate >= 0.40:
                score += 28.0
            elif late_loss_rate >= 0.25:
                score += 14.0
        # Consecutive loss streak
        if inp.consecutive_loss_streak >= 5:
            score += 35.0
        elif inp.consecutive_loss_streak >= 3:
            score += 20.0
        elif inp.consecutive_loss_streak >= 1:
            score += 8.0
        # Champion poaching
        if inp.champion_poached_count >= 3:
            score += 20.0
        elif inp.champion_poached_count >= 1:
            score += 10.0
        return _clamp(score)

    def _competitive_readiness_score(self, inp: CompetitiveWinRateInput) -> float:
        score = 0.0
        # Stale battlecard
        if inp.battlecard_last_updated_days >= 180:
            score += 40.0
        elif inp.battlecard_last_updated_days >= 90:
            score += 24.0
        elif inp.battlecard_last_updated_days >= 45:
            score += 10.0
        # Low battlecard usage
        if inp.battlecard_usage_pct < 0.20:
            score += 35.0
        elif inp.battlecard_usage_pct < 0.40:
            score += 20.0
        elif inp.battlecard_usage_pct < 0.60:
            score += 8.0
        # Competitor strength
        if inp.competitor_strength_score >= 80:
            score += 25.0
        elif inp.competitor_strength_score >= 60:
            score += 14.0
        elif inp.competitor_strength_score >= 40:
            score += 6.0
        return _clamp(score)

    def _pattern_intensity_score(self, inp: CompetitiveWinRateInput) -> float:
        score = 0.0
        if inp.losses_this_period > 0:
            # Price-dominated losses
            price_ratio = inp.losses_on_price_count / inp.losses_this_period
            if price_ratio >= 0.60:
                score += 40.0
            elif price_ratio >= 0.40:
                score += 24.0
            elif price_ratio >= 0.20:
                score += 10.0
            # Feature-dominated losses
            feature_ratio = inp.losses_on_features_count / inp.losses_this_period
            if feature_ratio >= 0.50:
                score += 35.0
            elif feature_ratio >= 0.30:
                score += 20.0
            elif feature_ratio >= 0.15:
                score += 8.0
            # Relationship-dominated losses (hardest to fix)
            rel_ratio = inp.losses_on_relationship_count / inp.losses_this_period
            if rel_ratio >= 0.50:
                score += 25.0
            elif rel_ratio >= 0.30:
                score += 14.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> WinRateRisk:
        if composite < 20:
            return WinRateRisk.low
        if composite < 40:
            return WinRateRisk.moderate
        if composite < 60:
            return WinRateRisk.high
        return WinRateRisk.critical

    def _classify_severity(self, composite: float) -> ErosionSeverity:
        if composite < 20:
            return ErosionSeverity.stable
        if composite < 40:
            return ErosionSeverity.declining
        if composite < 60:
            return ErosionSeverity.eroding
        return ErosionSeverity.collapse

    def _classify_pattern(
        self,
        inp: CompetitiveWinRateInput,
        decline: float,
        deal: float,
        readiness: float,
        intensity: float,
    ) -> ErosionPattern:
        if inp.losses_this_period == 0:
            return ErosionPattern.none
        # Systematic loss: declining across all metrics
        if inp.consecutive_loss_streak >= 4 and decline >= 25:
            return ErosionPattern.systematic_loss
        # Champion poaching: relationship attacks
        if inp.champion_poached_count >= 2:
            return ErosionPattern.champion_poaching
        # Feature regression: most losses are feature-based
        feature_ratio = inp.losses_on_features_count / inp.losses_this_period
        if feature_ratio >= 0.40 and readiness >= 20:
            return ErosionPattern.feature_regression
        # Pricing displacement: most losses are price-based
        price_ratio = inp.losses_on_price_count / inp.losses_this_period
        if price_ratio >= 0.40:
            return ErosionPattern.pricing_displacement
        # Rep skill gap: late-stage losses dominate
        if inp.late_stage_total_count > 0:
            late_rate = inp.late_stage_loss_count / inp.late_stage_total_count
            if late_rate >= 0.40 and deal >= 20:
                return ErosionPattern.rep_skill_gap
        return ErosionPattern.none

    def _recommended_action(
        self, risk: WinRateRisk, composite: float
    ) -> WinRateAction:
        if composite >= 60:
            return WinRateAction.executive_competitive_review
        if composite >= 50:
            return WinRateAction.pricing_strategy_review
        if risk == WinRateRisk.high:
            return WinRateAction.competitive_coaching
        if risk == WinRateRisk.moderate:
            return WinRateAction.battlecard_refresh
        return WinRateAction.no_action

    def _signal(
        self,
        pattern: ErosionPattern,
        composite: float,
        inp: CompetitiveWinRateInput,
    ) -> str:
        if pattern == ErosionPattern.none:
            return "Competitive win rate within healthy range"
        msgs = {
            ErosionPattern.systematic_loss: (
                f"{inp.consecutive_loss_streak} consecutive losses — "
                f"win rate {inp.win_rate_current_pct:.0f}% vs {inp.win_rate_prior_period_pct:.0f}% prior"
            ),
            ErosionPattern.champion_poaching: (
                f"{inp.champion_poached_count} champions poached — "
                f"{inp.losses_on_relationship_count} relationship losses"
            ),
            ErosionPattern.feature_regression: (
                f"{inp.losses_on_features_count}/{inp.losses_this_period} losses on features — "
                f"battlecard {inp.battlecard_last_updated_days}d old"
            ),
            ErosionPattern.pricing_displacement: (
                f"{inp.losses_on_price_count}/{inp.losses_this_period} losses on price — "
                f"win rate {inp.win_rate_current_pct:.0f}% vs {inp.win_rate_benchmark_pct:.0f}% benchmark"
            ),
            ErosionPattern.rep_skill_gap: (
                f"{inp.late_stage_loss_count}/{inp.late_stage_total_count} late-stage losses — "
                f"{inp.consecutive_loss_streak} loss streak"
            ),
        }
        base = msgs.get(pattern, f"win rate erosion composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: CompetitiveWinRateInput) -> CompetitiveWinRateResult:
        decline   = self._win_rate_decline_score(inp)
        deal      = self._deal_quality_score(inp)
        readiness = self._competitive_readiness_score(inp)
        intensity = self._pattern_intensity_score(inp)

        composite = _clamp(
            decline   * 0.35
            + deal     * 0.25
            + readiness * 0.25
            + intensity * 0.15
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp, decline, deal, readiness, intensity)
        action   = self._recommended_action(risk, composite)

        is_win_rate_eroding = (
            composite >= 40
            or inp.consecutive_loss_streak >= 4
            or inp.win_rate_trend_3_period_delta <= -15
        )
        requires_coaching = (
            composite >= 30
            or inp.late_stage_loss_count >= 3
            or inp.battlecard_last_updated_days >= 90
        )

        estimated_lost_revenue_usd = (
            inp.losses_this_period * inp.avg_deal_size_won_usd * (composite / 100.0)
        )

        result = CompetitiveWinRateResult(
            rep_id=inp.rep_id,
            region=inp.region,
            win_rate_risk=risk,
            erosion_pattern=pattern,
            erosion_severity=severity,
            recommended_action=action,
            win_rate_decline_score=decline,
            deal_quality_score=deal,
            competitive_readiness_score=readiness,
            pattern_intensity_score=intensity,
            win_rate_composite=composite,
            is_win_rate_eroding=is_win_rate_eroding,
            requires_coaching=requires_coaching,
            estimated_lost_revenue_usd=estimated_lost_revenue_usd,
            erosion_signal=self._signal(pattern, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[CompetitiveWinRateInput]
    ) -> list[CompetitiveWinRateResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                            0,
                "risk_counts":                      {},
                "pattern_counts":                   {},
                "severity_counts":                  {},
                "action_counts":                    {},
                "avg_win_rate_composite":           0.0,
                "eroding_count":                    0,
                "coaching_count":                   0,
                "avg_win_rate_decline_score":       0.0,
                "avg_deal_quality_score":           0.0,
                "avg_competitive_readiness_score":  0.0,
                "avg_pattern_intensity_score":      0.0,
                "total_estimated_lost_revenue_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_dec = total_deal = total_read = total_int = 0.0
        eroding = coaching = 0
        total_lost = 0.0

        for r in self._results:
            risk_counts[r.win_rate_risk.value]       = risk_counts.get(r.win_rate_risk.value, 0) + 1
            pattern_counts[r.erosion_pattern.value]  = pattern_counts.get(r.erosion_pattern.value, 0) + 1
            severity_counts[r.erosion_severity.value] = severity_counts.get(r.erosion_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.win_rate_composite
            total_dec   += r.win_rate_decline_score
            total_deal  += r.deal_quality_score
            total_read  += r.competitive_readiness_score
            total_int   += r.pattern_intensity_score
            total_lost  += r.estimated_lost_revenue_usd
            if r.is_win_rate_eroding:
                eroding += 1
            if r.requires_coaching:
                coaching += 1

        n = len(self._results)
        return {
            "total":                            n,
            "risk_counts":                      risk_counts,
            "pattern_counts":                   pattern_counts,
            "severity_counts":                  severity_counts,
            "action_counts":                    action_counts,
            "avg_win_rate_composite":           round(total_comp / n, 1),
            "eroding_count":                    eroding,
            "coaching_count":                   coaching,
            "avg_win_rate_decline_score":       round(total_dec  / n, 1),
            "avg_deal_quality_score":           round(total_deal / n, 1),
            "avg_competitive_readiness_score":  round(total_read / n, 1),
            "avg_pattern_intensity_score":      round(total_int  / n, 1),
            "total_estimated_lost_revenue_usd": round(total_lost, 2),
        }
