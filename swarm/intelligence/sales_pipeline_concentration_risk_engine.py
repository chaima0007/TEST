"""Sales Pipeline Concentration Risk Engine — detects when pipeline is concentrated
in too few deals, reps, accounts, or product lines, creating fragile forecasts and
single-point-of-failure exposure that inflates committed revenue risk."""

from __future__ import annotations

import dataclasses
from enum import Enum


class ConcentrationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ConcentrationPattern(str, Enum):
    none                   = "none"
    whale_dependency       = "whale_dependency"
    rep_single_point       = "rep_single_point"
    account_overexposure   = "account_overexposure"
    product_concentration  = "product_concentration"
    stage_bottleneck       = "stage_bottleneck"


class ConcentrationSeverity(str, Enum):
    diversified = "diversified"
    watch       = "watch"
    concentrated = "concentrated"
    critical     = "critical"


class ConcentrationAction(str, Enum):
    no_action              = "no_action"
    pipeline_diversification = "pipeline_diversification"
    rep_rebalancing        = "rep_rebalancing"
    forecast_risk_flag     = "forecast_risk_flag"
    executive_review       = "executive_review"


@dataclasses.dataclass
class PipelineConcentrationInput:
    rep_id:                          str
    region:                          str
    evaluation_period_id:            str
    total_pipeline_usd:              float
    top_deal_value_usd:              float
    top_3_deals_value_usd:           float
    deal_count:                      int
    unique_accounts_in_pipeline:     int
    top_account_pipeline_usd:        float
    product_lines_represented:       int
    total_product_lines:             int
    top_product_line_pipeline_pct:   float
    deals_in_late_stage_pct:         float
    deals_in_single_stage_pct:       float
    avg_deal_value_usd:              float
    median_deal_value_usd:           float
    pipeline_created_last_30d_usd:   float
    pipeline_created_prior_30d_usd:  float
    single_rep_pipeline_pct:         float
    stale_deals_pct:                 float
    committed_forecast_usd:          float
    sandbagged_deals_count:          int


@dataclasses.dataclass
class PipelineConcentrationResult:
    rep_id:                       str
    region:                       str
    concentration_risk:           ConcentrationRisk
    concentration_pattern:        ConcentrationPattern
    concentration_severity:       ConcentrationSeverity
    recommended_action:           ConcentrationAction
    deal_concentration_score:     float
    account_concentration_score:  float
    product_concentration_score:  float
    stage_concentration_score:    float
    concentration_composite:      float
    is_fragile_pipeline:          bool
    requires_rebalancing:         bool
    estimated_at_risk_revenue_usd: float
    concentration_signal:         str

    def to_dict(self) -> dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "concentration_risk":            self.concentration_risk.value,
            "concentration_pattern":         self.concentration_pattern.value,
            "concentration_severity":        self.concentration_severity.value,
            "recommended_action":            self.recommended_action.value,
            "deal_concentration_score":      round(self.deal_concentration_score, 1),
            "account_concentration_score":   round(self.account_concentration_score, 1),
            "product_concentration_score":   round(self.product_concentration_score, 1),
            "stage_concentration_score":     round(self.stage_concentration_score, 1),
            "concentration_composite":       round(self.concentration_composite, 1),
            "is_fragile_pipeline":           self.is_fragile_pipeline,
            "requires_rebalancing":          self.requires_rebalancing,
            "estimated_at_risk_revenue_usd": round(self.estimated_at_risk_revenue_usd, 2),
            "concentration_signal":          self.concentration_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesPipelineConcentrationRiskEngine:
    """Detects pipeline concentration to protect forecast integrity."""

    def __init__(self) -> None:
        self._results: list[PipelineConcentrationResult] = []

    # ── sub-scores (HIGHER = more concentration risk) ────────────────────────

    def _deal_concentration_score(self, inp: PipelineConcentrationInput) -> float:
        score = 0.0
        if inp.total_pipeline_usd > 0:
            # Top deal as % of total pipeline
            top_deal_pct = inp.top_deal_value_usd / inp.total_pipeline_usd
            if top_deal_pct >= 0.60:
                score += 50.0
            elif top_deal_pct >= 0.40:
                score += 32.0
            elif top_deal_pct >= 0.25:
                score += 18.0
            elif top_deal_pct >= 0.15:
                score += 8.0
            # Top 3 deals as % of total
            top3_pct = inp.top_3_deals_value_usd / inp.total_pipeline_usd
            if top3_pct >= 0.85:
                score += 30.0
            elif top3_pct >= 0.70:
                score += 18.0
            elif top3_pct >= 0.55:
                score += 9.0
        # Very few deals
        if inp.deal_count <= 2:
            score += 20.0
        elif inp.deal_count <= 4:
            score += 10.0
        return _clamp(score)

    def _account_concentration_score(self, inp: PipelineConcentrationInput) -> float:
        score = 0.0
        if inp.total_pipeline_usd > 0:
            # Top account as % of total pipeline
            top_acct_pct = inp.top_account_pipeline_usd / inp.total_pipeline_usd
            if top_acct_pct >= 0.60:
                score += 45.0
            elif top_acct_pct >= 0.40:
                score += 28.0
            elif top_acct_pct >= 0.25:
                score += 15.0
            elif top_acct_pct >= 0.10:
                score += 6.0
        # Few unique accounts
        if inp.unique_accounts_in_pipeline <= 2:
            score += 30.0
        elif inp.unique_accounts_in_pipeline <= 4:
            score += 15.0
        elif inp.unique_accounts_in_pipeline <= 6:
            score += 6.0
        # Single rep pipeline concentration
        if inp.single_rep_pipeline_pct >= 0.90:
            score += 25.0
        elif inp.single_rep_pipeline_pct >= 0.70:
            score += 12.0
        return _clamp(score)

    def _product_concentration_score(self, inp: PipelineConcentrationInput) -> float:
        score = 0.0
        # Top product line concentration
        if inp.top_product_line_pipeline_pct >= 90:
            score += 40.0
        elif inp.top_product_line_pipeline_pct >= 75:
            score += 24.0
        elif inp.top_product_line_pipeline_pct >= 60:
            score += 12.0
        # Product line coverage ratio
        if inp.total_product_lines > 0:
            coverage = inp.product_lines_represented / inp.total_product_lines
            if coverage <= 0.20:
                score += 35.0
            elif coverage <= 0.40:
                score += 20.0
            elif coverage <= 0.60:
                score += 10.0
        # Pipeline creation slowdown
        if inp.pipeline_created_prior_30d_usd > 0:
            creation_ratio = inp.pipeline_created_last_30d_usd / inp.pipeline_created_prior_30d_usd
            if creation_ratio <= 0.25:
                score += 25.0
            elif creation_ratio <= 0.50:
                score += 14.0
            elif creation_ratio <= 0.75:
                score += 6.0
        return _clamp(score)

    def _stage_concentration_score(self, inp: PipelineConcentrationInput) -> float:
        score = 0.0
        # Deals clustered in late stage (no early pipeline)
        if inp.deals_in_late_stage_pct >= 0.80:
            score += 40.0
        elif inp.deals_in_late_stage_pct >= 0.60:
            score += 24.0
        elif inp.deals_in_late_stage_pct >= 0.40:
            score += 10.0
        # Deals clustered in a single stage
        if inp.deals_in_single_stage_pct >= 0.80:
            score += 35.0
        elif inp.deals_in_single_stage_pct >= 0.60:
            score += 20.0
        elif inp.deals_in_single_stage_pct >= 0.40:
            score += 10.0
        # Stale pipeline
        if inp.stale_deals_pct >= 0.50:
            score += 25.0
        elif inp.stale_deals_pct >= 0.30:
            score += 14.0
        elif inp.stale_deals_pct >= 0.15:
            score += 6.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> ConcentrationRisk:
        if composite < 20:
            return ConcentrationRisk.low
        if composite < 40:
            return ConcentrationRisk.moderate
        if composite < 60:
            return ConcentrationRisk.high
        return ConcentrationRisk.critical

    def _classify_severity(self, composite: float) -> ConcentrationSeverity:
        if composite < 20:
            return ConcentrationSeverity.diversified
        if composite < 40:
            return ConcentrationSeverity.watch
        if composite < 60:
            return ConcentrationSeverity.concentrated
        return ConcentrationSeverity.critical

    def _classify_pattern(
        self,
        inp: PipelineConcentrationInput,
        deal: float,
        account: float,
        product: float,
        stage: float,
    ) -> ConcentrationPattern:
        # Stage bottleneck: pipeline stuck in one stage
        if inp.deals_in_single_stage_pct >= 0.70 and stage >= 30:
            return ConcentrationPattern.stage_bottleneck
        # Whale dependency: single deal dominates
        if inp.total_pipeline_usd > 0 and inp.top_deal_value_usd / inp.total_pipeline_usd >= 0.45:
            return ConcentrationPattern.whale_dependency
        # Rep single point: one rep holds all pipeline
        if inp.single_rep_pipeline_pct >= 0.85:
            return ConcentrationPattern.rep_single_point
        # Account overexposure: one account dominates
        if inp.total_pipeline_usd > 0 and inp.top_account_pipeline_usd / inp.total_pipeline_usd >= 0.40:
            return ConcentrationPattern.account_overexposure
        # Product concentration: one product line
        if inp.top_product_line_pipeline_pct >= 75 and product >= 20:
            return ConcentrationPattern.product_concentration
        return ConcentrationPattern.none

    def _recommended_action(
        self, risk: ConcentrationRisk, composite: float
    ) -> ConcentrationAction:
        if composite >= 60:
            return ConcentrationAction.executive_review
        if composite >= 50:
            return ConcentrationAction.forecast_risk_flag
        if risk == ConcentrationRisk.high:
            return ConcentrationAction.rep_rebalancing
        if risk == ConcentrationRisk.moderate:
            return ConcentrationAction.pipeline_diversification
        return ConcentrationAction.no_action

    def _signal(
        self,
        pattern: ConcentrationPattern,
        composite: float,
        inp: PipelineConcentrationInput,
    ) -> str:
        if pattern == ConcentrationPattern.none:
            return "Pipeline well-diversified across deals, accounts, and stages"
        msgs = {
            ConcentrationPattern.stage_bottleneck: (
                f"{inp.deals_in_single_stage_pct*100:.0f}% of deals in single stage — "
                f"{inp.stale_deals_pct*100:.0f}% stale"
            ),
            ConcentrationPattern.whale_dependency: (
                f"Top deal ${inp.top_deal_value_usd:,.0f} — "
                f"{(inp.top_deal_value_usd/inp.total_pipeline_usd*100) if inp.total_pipeline_usd > 0 else 0:.0f}% of pipeline"
            ),
            ConcentrationPattern.rep_single_point: (
                f"{inp.single_rep_pipeline_pct*100:.0f}% pipeline held by single rep — "
                f"{inp.deal_count} deals"
            ),
            ConcentrationPattern.account_overexposure: (
                f"Top account ${inp.top_account_pipeline_usd:,.0f} — "
                f"{inp.unique_accounts_in_pipeline} unique accounts total"
            ),
            ConcentrationPattern.product_concentration: (
                f"Top product line {inp.top_product_line_pipeline_pct:.0f}% of pipeline — "
                f"{inp.product_lines_represented}/{inp.total_product_lines} lines"
            ),
        }
        base = msgs.get(pattern, f"concentration composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: PipelineConcentrationInput) -> PipelineConcentrationResult:
        deal    = self._deal_concentration_score(inp)
        account = self._account_concentration_score(inp)
        product = self._product_concentration_score(inp)
        stage   = self._stage_concentration_score(inp)

        composite = _clamp(
            deal    * 0.35
            + account * 0.30
            + product * 0.20
            + stage   * 0.15
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp, deal, account, product, stage)
        action   = self._recommended_action(risk, composite)

        is_fragile_pipeline = (
            composite >= 40
            or inp.deal_count <= 2
            or (inp.total_pipeline_usd > 0 and inp.top_deal_value_usd / inp.total_pipeline_usd >= 0.60)
        )
        requires_rebalancing = (
            composite >= 30
            or inp.unique_accounts_in_pipeline <= 3
            or inp.sandbagged_deals_count >= 2
        )

        estimated_at_risk_revenue_usd = inp.committed_forecast_usd * (composite / 100.0)

        result = PipelineConcentrationResult(
            rep_id=inp.rep_id,
            region=inp.region,
            concentration_risk=risk,
            concentration_pattern=pattern,
            concentration_severity=severity,
            recommended_action=action,
            deal_concentration_score=deal,
            account_concentration_score=account,
            product_concentration_score=product,
            stage_concentration_score=stage,
            concentration_composite=composite,
            is_fragile_pipeline=is_fragile_pipeline,
            requires_rebalancing=requires_rebalancing,
            estimated_at_risk_revenue_usd=estimated_at_risk_revenue_usd,
            concentration_signal=self._signal(pattern, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[PipelineConcentrationInput]
    ) -> list[PipelineConcentrationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                              0,
                "risk_counts":                        {},
                "pattern_counts":                     {},
                "severity_counts":                    {},
                "action_counts":                      {},
                "avg_concentration_composite":        0.0,
                "fragile_pipeline_count":             0,
                "rebalancing_count":                  0,
                "avg_deal_concentration_score":       0.0,
                "avg_account_concentration_score":    0.0,
                "avg_product_concentration_score":    0.0,
                "avg_stage_concentration_score":      0.0,
                "total_estimated_at_risk_revenue_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_deal = total_acc = total_prod = total_stg = 0.0
        fragile = rebal = 0
        total_rev = 0.0

        for r in self._results:
            risk_counts[r.concentration_risk.value]       = risk_counts.get(r.concentration_risk.value, 0) + 1
            pattern_counts[r.concentration_pattern.value] = pattern_counts.get(r.concentration_pattern.value, 0) + 1
            severity_counts[r.concentration_severity.value] = severity_counts.get(r.concentration_severity.value, 0) + 1
            action_counts[r.recommended_action.value]       = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp  += r.concentration_composite
            total_deal  += r.deal_concentration_score
            total_acc   += r.account_concentration_score
            total_prod  += r.product_concentration_score
            total_stg   += r.stage_concentration_score
            total_rev   += r.estimated_at_risk_revenue_usd
            if r.is_fragile_pipeline:
                fragile += 1
            if r.requires_rebalancing:
                rebal += 1

        n = len(self._results)
        return {
            "total":                               n,
            "risk_counts":                         risk_counts,
            "pattern_counts":                      pattern_counts,
            "severity_counts":                     severity_counts,
            "action_counts":                       action_counts,
            "avg_concentration_composite":         round(total_comp / n, 1),
            "fragile_pipeline_count":              fragile,
            "rebalancing_count":                   rebal,
            "avg_deal_concentration_score":        round(total_deal / n, 1),
            "avg_account_concentration_score":     round(total_acc  / n, 1),
            "avg_product_concentration_score":     round(total_prod / n, 1),
            "avg_stage_concentration_score":       round(total_stg  / n, 1),
            "total_estimated_at_risk_revenue_usd": round(total_rev, 2),
        }
