"""Competitor Win/Loss Intelligence Engine — identifies patterns in competitive
deal outcomes to detect where competitors are systematically winning, where
intel gaps exist, and which competitive strategies are failing."""

from __future__ import annotations

import dataclasses
from enum import Enum


class CompetitiveRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CompetitivePattern(str, Enum):
    none               = "none"
    price_displacement = "price_displacement"
    feature_gap        = "feature_gap"
    relationship_loss  = "relationship_loss"
    intel_blindspot    = "intel_blindspot"
    systematic_loss    = "systematic_loss"


class CompetitiveSeverity(str, Enum):
    stable      = "stable"
    watch       = "watch"
    threatened  = "threatened"
    critical    = "critical"


class CompetitiveAction(str, Enum):
    no_action           = "no_action"
    monitor             = "monitor"
    battlecard_update   = "battlecard_update"
    sales_coaching      = "sales_coaching"
    executive_escalation = "executive_escalation"


@dataclasses.dataclass
class CompetitorWinLossInput:
    rep_id:                          str
    region:                          str
    evaluation_period_id:            str
    total_competitive_deals:         int
    wins_against_competitor:         int
    losses_to_competitor:            int
    avg_win_rate_pct:                float
    company_avg_win_rate_pct:        float
    deals_lost_on_price:             int
    deals_lost_on_features:          int
    deals_lost_on_relationship:      int
    deals_without_competitor_intel:  int
    avg_deal_value_won_usd:          float
    avg_deal_value_lost_usd:         float
    competitor_mentioned_in_deal_count: int
    battlecard_usage_count:          int
    late_stage_competitive_loss_count: int
    competitive_loss_streak:         int
    win_rate_trend_delta_pct:        float
    days_since_last_competitive_win: int
    rep_avg_competitive_win_rate_pct: float
    exec_sponsor_deals_won:          int


@dataclasses.dataclass
class CompetitorWinLossResult:
    rep_id:                         str
    region:                         str
    competitive_risk:               CompetitiveRisk
    competitive_pattern:            CompetitivePattern
    competitive_severity:           CompetitiveSeverity
    recommended_action:             CompetitiveAction
    price_vulnerability_score:      float
    feature_gap_score:              float
    intel_coverage_score:           float
    execution_quality_score:        float
    competitive_composite:          float
    is_competitive_risk:            bool
    requires_battlecard_update:     bool
    estimated_revenue_at_risk_usd:  float
    competitive_signal:             str

    def to_dict(self) -> dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "competitive_risk":              self.competitive_risk.value,
            "competitive_pattern":           self.competitive_pattern.value,
            "competitive_severity":          self.competitive_severity.value,
            "recommended_action":            self.recommended_action.value,
            "price_vulnerability_score":     round(self.price_vulnerability_score, 1),
            "feature_gap_score":             round(self.feature_gap_score, 1),
            "intel_coverage_score":          round(self.intel_coverage_score, 1),
            "execution_quality_score":       round(self.execution_quality_score, 1),
            "competitive_composite":         round(self.competitive_composite, 1),
            "is_competitive_risk":           self.is_competitive_risk,
            "requires_battlecard_update":    self.requires_battlecard_update,
            "estimated_revenue_at_risk_usd": round(self.estimated_revenue_at_risk_usd, 2),
            "competitive_signal":            self.competitive_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class CompetitorWinLossIntelligenceEngine:
    """Identifies competitive weakness patterns from win/loss data across sales reps."""

    def __init__(self) -> None:
        self._results: list[CompetitorWinLossResult] = []

    # ── sub-scores (HIGHER = more competitive risk) ──────────────────────────

    def _price_vulnerability_score(self, inp: CompetitorWinLossInput) -> float:
        score = 0.0
        if inp.total_competitive_deals > 0:
            price_loss_ratio = inp.deals_lost_on_price / inp.total_competitive_deals
            if price_loss_ratio >= 0.5:
                score += 45.0
            elif price_loss_ratio >= 0.35:
                score += 30.0
            elif price_loss_ratio >= 0.2:
                score += 15.0
        # Win rate vs company average
        win_rate_gap = inp.company_avg_win_rate_pct - inp.avg_win_rate_pct
        if win_rate_gap >= 30:
            score += 35.0
        elif win_rate_gap >= 20:
            score += 22.0
        elif win_rate_gap >= 10:
            score += 10.0
        # Deal value compression (losing bigger deals)
        if inp.avg_deal_value_won_usd > 0 and inp.avg_deal_value_lost_usd > inp.avg_deal_value_won_usd:
            value_gap_ratio = (inp.avg_deal_value_lost_usd - inp.avg_deal_value_won_usd) / inp.avg_deal_value_lost_usd
            if value_gap_ratio >= 0.5:
                score += 20.0
            elif value_gap_ratio >= 0.3:
                score += 10.0
        return _clamp(score)

    def _feature_gap_score(self, inp: CompetitorWinLossInput) -> float:
        score = 0.0
        if inp.total_competitive_deals > 0:
            feature_loss_ratio = inp.deals_lost_on_features / inp.total_competitive_deals
            if feature_loss_ratio >= 0.4:
                score += 45.0
            elif feature_loss_ratio >= 0.25:
                score += 28.0
            elif feature_loss_ratio >= 0.12:
                score += 14.0
        # Late-stage losses signal inability to defend on value/features
        if inp.late_stage_competitive_loss_count >= 5:
            score += 35.0
        elif inp.late_stage_competitive_loss_count >= 3:
            score += 22.0
        elif inp.late_stage_competitive_loss_count >= 1:
            score += 10.0
        # Win rate trend deterioration
        if inp.win_rate_trend_delta_pct <= -20:
            score += 20.0
        elif inp.win_rate_trend_delta_pct <= -10:
            score += 10.0
        return _clamp(score)

    def _intel_coverage_score(self, inp: CompetitorWinLossInput) -> float:
        score = 0.0
        # Deals without competitive intel
        if inp.total_competitive_deals > 0:
            blind_ratio = inp.deals_without_competitor_intel / inp.total_competitive_deals
            if blind_ratio >= 0.6:
                score += 45.0
            elif blind_ratio >= 0.4:
                score += 30.0
            elif blind_ratio >= 0.2:
                score += 15.0
        # Low battlecard usage
        if inp.competitor_mentioned_in_deal_count > 0:
            card_ratio = inp.battlecard_usage_count / inp.competitor_mentioned_in_deal_count
            if card_ratio < 0.2:
                score += 30.0
            elif card_ratio < 0.4:
                score += 18.0
            elif card_ratio < 0.6:
                score += 8.0
        # Losing streak without adjustment
        if inp.competitive_loss_streak >= 6:
            score += 25.0
        elif inp.competitive_loss_streak >= 4:
            score += 15.0
        elif inp.competitive_loss_streak >= 2:
            score += 7.0
        return _clamp(score)

    def _execution_quality_score(self, inp: CompetitorWinLossInput) -> float:
        score = 0.0
        # Relationship/champion losses
        if inp.total_competitive_deals > 0:
            rel_loss_ratio = inp.deals_lost_on_relationship / inp.total_competitive_deals
            if rel_loss_ratio >= 0.4:
                score += 40.0
            elif rel_loss_ratio >= 0.25:
                score += 25.0
            elif rel_loss_ratio >= 0.1:
                score += 12.0
        # Days since last competitive win (momentum)
        if inp.days_since_last_competitive_win >= 90:
            score += 30.0
        elif inp.days_since_last_competitive_win >= 60:
            score += 18.0
        elif inp.days_since_last_competitive_win >= 30:
            score += 8.0
        # Low exec sponsor engagement on won deals
        if inp.wins_against_competitor > 0:
            exec_win_ratio = inp.exec_sponsor_deals_won / inp.wins_against_competitor
            if exec_win_ratio < 0.15:
                score += 20.0
            elif exec_win_ratio < 0.30:
                score += 10.0
        elif inp.wins_against_competitor == 0 and inp.losses_to_competitor >= 3:
            score += 20.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> CompetitiveRisk:
        if composite < 20:
            return CompetitiveRisk.low
        if composite < 40:
            return CompetitiveRisk.moderate
        if composite < 60:
            return CompetitiveRisk.high
        return CompetitiveRisk.critical

    def _classify_severity(self, composite: float) -> CompetitiveSeverity:
        if composite < 20:
            return CompetitiveSeverity.stable
        if composite < 40:
            return CompetitiveSeverity.watch
        if composite < 60:
            return CompetitiveSeverity.threatened
        return CompetitiveSeverity.critical

    def _classify_pattern(
        self,
        inp: CompetitorWinLossInput,
        price: float,
        feature: float,
        intel: float,
        execution: float,
    ) -> CompetitivePattern:
        if inp.competitive_loss_streak >= 5 and inp.wins_against_competitor == 0:
            return CompetitivePattern.systematic_loss
        if intel >= 35:
            return CompetitivePattern.intel_blindspot
        if price >= 35:
            return CompetitivePattern.price_displacement
        if feature >= 35:
            return CompetitivePattern.feature_gap
        if execution >= 30 and inp.deals_lost_on_relationship >= 2:
            return CompetitivePattern.relationship_loss
        return CompetitivePattern.none

    def _recommended_action(
        self, risk: CompetitiveRisk, composite: float
    ) -> CompetitiveAction:
        if composite >= 60:
            return CompetitiveAction.executive_escalation
        if risk == CompetitiveRisk.high:
            return CompetitiveAction.sales_coaching
        if risk == CompetitiveRisk.moderate:
            return CompetitiveAction.battlecard_update
        if composite >= 10:
            return CompetitiveAction.monitor
        return CompetitiveAction.no_action

    def _signal(
        self,
        pattern: CompetitivePattern,
        composite: float,
        inp: CompetitorWinLossInput,
    ) -> str:
        if pattern == CompetitivePattern.none:
            return "Competitive win/loss within healthy parameters"
        loss_rate = (
            round(inp.losses_to_competitor / inp.total_competitive_deals * 100)
            if inp.total_competitive_deals > 0 else 0
        )
        msgs = {
            CompetitivePattern.systematic_loss: (
                f"Loss streak {inp.competitive_loss_streak} — "
                f"{inp.wins_against_competitor} wins vs {inp.losses_to_competitor} losses"
            ),
            CompetitivePattern.intel_blindspot: (
                f"{inp.deals_without_competitor_intel} deals without intel — "
                f"battlecard usage {inp.battlecard_usage_count}/{inp.competitor_mentioned_in_deal_count}"
            ),
            CompetitivePattern.price_displacement: (
                f"{inp.deals_lost_on_price} deals lost on price — {loss_rate}% loss rate"
            ),
            CompetitivePattern.feature_gap: (
                f"{inp.deals_lost_on_features} deals lost on features — "
                f"{inp.late_stage_competitive_loss_count} late-stage losses"
            ),
            CompetitivePattern.relationship_loss: (
                f"{inp.deals_lost_on_relationship} relationship losses — "
                f"{inp.days_since_last_competitive_win}d since last win"
            ),
        }
        base = msgs.get(pattern, f"competitive composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: CompetitorWinLossInput) -> CompetitorWinLossResult:
        price    = self._price_vulnerability_score(inp)
        feature  = self._feature_gap_score(inp)
        intel    = self._intel_coverage_score(inp)
        execution = self._execution_quality_score(inp)

        composite = _clamp(
            price     * 0.30
            + feature * 0.25
            + intel   * 0.25
            + execution * 0.20
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp, price, feature, intel, execution)
        action   = self._recommended_action(risk, composite)

        is_competitive_risk = (
            composite >= 40
            or inp.competitive_loss_streak >= 4
            or inp.avg_win_rate_pct < 20
        )
        requires_battlecard_update = (
            composite >= 30
            or inp.deals_without_competitor_intel >= 3
            or inp.win_rate_trend_delta_pct <= -15
        )

        estimated_revenue_at_risk_usd = inp.avg_deal_value_lost_usd * inp.losses_to_competitor * (composite / 100.0)

        result = CompetitorWinLossResult(
            rep_id=inp.rep_id,
            region=inp.region,
            competitive_risk=risk,
            competitive_pattern=pattern,
            competitive_severity=severity,
            recommended_action=action,
            price_vulnerability_score=price,
            feature_gap_score=feature,
            intel_coverage_score=intel,
            execution_quality_score=execution,
            competitive_composite=composite,
            is_competitive_risk=is_competitive_risk,
            requires_battlecard_update=requires_battlecard_update,
            estimated_revenue_at_risk_usd=estimated_revenue_at_risk_usd,
            competitive_signal=self._signal(pattern, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[CompetitorWinLossInput]
    ) -> list[CompetitorWinLossResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                            0,
                "risk_counts":                      {},
                "pattern_counts":                   {},
                "severity_counts":                  {},
                "action_counts":                    {},
                "avg_competitive_composite":        0.0,
                "competitive_risk_count":           0,
                "battlecard_update_count":          0,
                "avg_price_vulnerability_score":    0.0,
                "avg_feature_gap_score":            0.0,
                "avg_intel_coverage_score":         0.0,
                "avg_execution_quality_score":      0.0,
                "total_estimated_revenue_at_risk_usd": 0.0,
            }

        risk_counts:    dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:  dict[str, int] = {}
        total_comp = total_price = total_feat = total_intel = total_exec = 0.0
        total_rev = 0.0
        comp_risk = battlecard = 0

        for r in self._results:
            risk_counts[r.competitive_risk.value]       = risk_counts.get(r.competitive_risk.value, 0) + 1
            pattern_counts[r.competitive_pattern.value] = pattern_counts.get(r.competitive_pattern.value, 0) + 1
            severity_counts[r.competitive_severity.value] = severity_counts.get(r.competitive_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.competitive_composite
            total_price += r.price_vulnerability_score
            total_feat  += r.feature_gap_score
            total_intel += r.intel_coverage_score
            total_exec  += r.execution_quality_score
            total_rev   += r.estimated_revenue_at_risk_usd
            if r.is_competitive_risk:
                comp_risk += 1
            if r.requires_battlecard_update:
                battlecard += 1

        n = len(self._results)
        return {
            "total":                               n,
            "risk_counts":                         risk_counts,
            "pattern_counts":                      pattern_counts,
            "severity_counts":                     severity_counts,
            "action_counts":                       action_counts,
            "avg_competitive_composite":           round(total_comp  / n, 1),
            "competitive_risk_count":              comp_risk,
            "battlecard_update_count":             battlecard,
            "avg_price_vulnerability_score":       round(total_price / n, 1),
            "avg_feature_gap_score":               round(total_feat  / n, 1),
            "avg_intel_coverage_score":            round(total_intel / n, 1),
            "avg_execution_quality_score":         round(total_exec  / n, 1),
            "total_estimated_revenue_at_risk_usd": round(total_rev, 2),
        }
