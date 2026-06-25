"""
Sales Territory Coverage Intelligence Engine

Analyse la couverture territoriale d'un commercial ou d'une équipe :
densité de comptes, whitespace, prévention du churn géographique.
"""

from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields
from enum import Enum
from typing import Optional


class CoverageRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class CoveragePattern(str, Enum):
    none = "none"
    geographic_concentration = "geographic_concentration"
    account_desert = "account_desert"
    whitespace_neglect = "whitespace_neglect"
    churn_cluster = "churn_cluster"
    top_heavy_territory = "top_heavy_territory"
    underserved_segment = "underserved_segment"


class CoverageSeverity(str, Enum):
    optimal = "optimal"
    suboptimal = "suboptimal"
    degraded = "degraded"
    critical = "critical"


class CoverageAction(str, Enum):
    maintain = "maintain"
    expand_whitespace = "expand_whitespace"
    rebalance_territory = "rebalance_territory"
    churn_intervention = "churn_intervention"
    account_redistribution = "account_redistribution"
    segment_focus = "segment_focus"


@dataclass
class TerritoryCoverageInput:
    total_accounts: int = 100
    active_accounts: int = 60
    whitespace_accounts: int = 30
    churned_accounts_last_90d: int = 5
    top_account_revenue_pct: float = 40.0
    geographic_zones: int = 4
    zones_with_activity: int = 3
    avg_visits_per_account: float = 2.5
    accounts_no_contact_90d: int = 10
    new_accounts_added: int = 8
    accounts_at_risk: int = 12
    total_revenue: float = 500000.0
    top_3_accounts_revenue: float = 150000.0
    segment_a_coverage_pct: float = 75.0
    segment_b_coverage_pct: float = 55.0
    segment_c_coverage_pct: float = 35.0
    competitor_wins_in_territory: int = 3
    pipeline_coverage_ratio: float = 2.5
    territory_quota: float = 600000.0
    quota_attainment_pct: float = 83.0
    expansion_opportunities: int = 15
    account_health_score_avg: float = 68.0


@dataclass
class TerritoryCoverageResult:
    composite_score: float
    risk: CoverageRisk
    pattern: CoveragePattern
    severity: CoverageSeverity
    action: CoverageAction
    account_breadth_score: float
    account_prioritization_score: float
    whitespace_exploitation_score: float
    churn_prevention_score: float
    has_coverage_gap: bool
    requires_territory_rebalance: bool
    estimated_revenue_at_risk: float
    signal: str
    coverage_gap_pct: float
    whitespace_penetration_pct: float

    def to_dict(self) -> dict:
        return {
            "composite_score": self.composite_score,
            "risk": self.risk.value,
            "pattern": self.pattern.value,
            "severity": self.severity.value,
            "action": self.action.value,
            "account_breadth_score": self.account_breadth_score,
            "account_prioritization_score": self.account_prioritization_score,
            "whitespace_exploitation_score": self.whitespace_exploitation_score,
            "churn_prevention_score": self.churn_prevention_score,
            "has_coverage_gap": self.has_coverage_gap,
            "requires_territory_rebalance": self.requires_territory_rebalance,
            "estimated_revenue_at_risk": self.estimated_revenue_at_risk,
            "signal": self.signal,
            "coverage_gap_pct": self.coverage_gap_pct,
            "whitespace_penetration_pct": self.whitespace_penetration_pct,
        }


class SalesTerritoryCoverageIntelligenceEngine:

    def _account_breadth_score(self, inp: TerritoryCoverageInput) -> float:
        if inp.total_accounts == 0:
            return 0.0
        active_ratio = inp.active_accounts / inp.total_accounts
        zone_coverage = inp.zones_with_activity / max(inp.geographic_zones, 1)
        no_contact_penalty = inp.accounts_no_contact_90d / max(inp.total_accounts, 1)
        raw = (active_ratio * 50) + (zone_coverage * 30) - (no_contact_penalty * 20)
        return min(max(round(raw, 1), 0.0), 100.0)

    def _account_prioritization_score(self, inp: TerritoryCoverageInput) -> float:
        seg_avg = (inp.segment_a_coverage_pct + inp.segment_b_coverage_pct + inp.segment_c_coverage_pct) / 3
        health_score = inp.account_health_score_avg
        pipeline_score = min(inp.pipeline_coverage_ratio / 3.0, 1.0) * 20
        raw = (seg_avg * 0.5) + (health_score * 0.3) + pipeline_score
        return min(max(round(raw, 1), 0.0), 100.0)

    def _whitespace_exploitation_score(self, inp: TerritoryCoverageInput) -> float:
        if inp.total_accounts == 0:
            return 0.0
        penetration_rate = (inp.total_accounts - inp.whitespace_accounts) / inp.total_accounts
        expansion_bonus = min(inp.expansion_opportunities / inp.total_accounts * 50, 20)
        new_account_bonus = min(inp.new_accounts_added / max(inp.total_accounts * 0.05, 1) * 10, 10)
        raw = penetration_rate * 100 + expansion_bonus + new_account_bonus
        return min(max(round(raw, 1), 0.0), 100.0)

    def _churn_prevention_score(self, inp: TerritoryCoverageInput) -> float:
        churn_rate = inp.churned_accounts_last_90d / max(inp.total_accounts, 1)
        at_risk_rate = inp.accounts_at_risk / max(inp.total_accounts, 1)
        competitor_impact = inp.competitor_wins_in_territory / max(inp.total_accounts * 0.1, 1)
        raw = 100 - (churn_rate * 200) - (at_risk_rate * 60) - min(competitor_impact * 10, 20)
        return min(max(round(raw, 1), 0.0), 100.0)

    def _composite(self, b: float, p: float, w: float, c: float) -> float:
        return min(round(b * 0.25 + p * 0.30 + w * 0.25 + c * 0.20, 1), 100.0)

    def _risk_level(self, score: float) -> CoverageRisk:
        if score >= 75:
            return CoverageRisk.low
        if score >= 55:
            return CoverageRisk.moderate
        if score >= 35:
            return CoverageRisk.high
        return CoverageRisk.critical

    def _severity(self, risk: CoverageRisk) -> CoverageSeverity:
        return {
            CoverageRisk.low: CoverageSeverity.optimal,
            CoverageRisk.moderate: CoverageSeverity.suboptimal,
            CoverageRisk.high: CoverageSeverity.degraded,
            CoverageRisk.critical: CoverageSeverity.critical,
        }[risk]

    def _detect_pattern(self, inp: TerritoryCoverageInput, b: float, p: float, w: float, c: float) -> CoveragePattern:
        if inp.total_accounts > 0 and inp.top_3_accounts_revenue / max(inp.total_revenue, 1) > 0.5:
            return CoveragePattern.top_heavy_territory
        if inp.zones_with_activity < inp.geographic_zones * 0.6:
            return CoveragePattern.geographic_concentration
        if w < 40:
            return CoveragePattern.whitespace_neglect
        if c < 40:
            return CoveragePattern.churn_cluster
        if inp.accounts_no_contact_90d / max(inp.total_accounts, 1) > 0.2:
            return CoveragePattern.account_desert
        if inp.segment_c_coverage_pct < 30:
            return CoveragePattern.underserved_segment
        return CoveragePattern.none

    def _action(self, pattern: CoveragePattern, risk: CoverageRisk) -> CoverageAction:
        mapping = {
            CoveragePattern.top_heavy_territory: CoverageAction.account_redistribution,
            CoveragePattern.geographic_concentration: CoverageAction.rebalance_territory,
            CoveragePattern.whitespace_neglect: CoverageAction.expand_whitespace,
            CoveragePattern.churn_cluster: CoverageAction.churn_intervention,
            CoveragePattern.account_desert: CoverageAction.rebalance_territory,
            CoveragePattern.underserved_segment: CoverageAction.segment_focus,
            CoveragePattern.none: CoverageAction.maintain,
        }
        return mapping[pattern]

    def _has_coverage_gap(self, inp: TerritoryCoverageInput) -> bool:
        if inp.total_accounts == 0:
            return False
        return (inp.accounts_no_contact_90d / inp.total_accounts > 0.15
                or inp.zones_with_activity < inp.geographic_zones)

    def _requires_territory_rebalance(self, inp: TerritoryCoverageInput) -> bool:
        top_heavy = inp.total_revenue > 0 and inp.top_3_accounts_revenue / inp.total_revenue > 0.5
        zone_imbalanced = inp.zones_with_activity < inp.geographic_zones * 0.75
        return top_heavy or zone_imbalanced

    def _estimated_revenue_at_risk(self, inp: TerritoryCoverageInput, score: float) -> float:
        base = inp.total_revenue * (inp.accounts_at_risk / max(inp.total_accounts, 1))
        adjusted = base * (1 - score / 100)
        return round(adjusted, 2)

    def _signal(self, risk: CoverageRisk, pattern: CoveragePattern) -> str:
        if risk == CoverageRisk.low and pattern == CoveragePattern.none:
            return "Territory coverage healthy — breadth, prioritization, whitespace and churn prevention within benchmarks"
        signals = {
            CoveragePattern.top_heavy_territory: "Top-3 accounts represent >50% revenue — dangerous concentration risk",
            CoveragePattern.geographic_concentration: "Activity concentrated in fewer zones than available — expand geographic reach",
            CoveragePattern.whitespace_neglect: "Significant whitespace untouched — expansion opportunity being missed",
            CoveragePattern.churn_cluster: "Churn rate and at-risk accounts elevated — retention intervention required",
            CoveragePattern.account_desert: "High proportion of accounts with no recent contact — reactivation needed",
            CoveragePattern.underserved_segment: "Segment C coverage critically low — realign prospection efforts",
            CoveragePattern.none: f"Territory coverage {risk.value} — monitor key metrics",
        }
        return signals.get(pattern, "Territory coverage requires attention")

    def assess(self, inp: TerritoryCoverageInput) -> TerritoryCoverageResult:
        b = self._account_breadth_score(inp)
        p = self._account_prioritization_score(inp)
        w = self._whitespace_exploitation_score(inp)
        c = self._churn_prevention_score(inp)
        composite = self._composite(b, p, w, c)
        risk = self._risk_level(composite)
        severity = self._severity(risk)
        pattern = self._detect_pattern(inp, b, p, w, c)
        action = self._action(pattern, risk)

        coverage_gap_pct = round(
            inp.accounts_no_contact_90d / max(inp.total_accounts, 1) * 100, 1
        )
        whitespace_pct = round(
            inp.whitespace_accounts / max(inp.total_accounts, 1) * 100, 1
        )

        return TerritoryCoverageResult(
            composite_score=composite,
            risk=risk,
            pattern=pattern,
            severity=severity,
            action=action,
            account_breadth_score=b,
            account_prioritization_score=p,
            whitespace_exploitation_score=w,
            churn_prevention_score=c,
            has_coverage_gap=self._has_coverage_gap(inp),
            requires_territory_rebalance=self._requires_territory_rebalance(inp),
            estimated_revenue_at_risk=self._estimated_revenue_at_risk(inp, composite),
            signal=self._signal(risk, pattern),
            coverage_gap_pct=coverage_gap_pct,
            whitespace_penetration_pct=whitespace_pct,
        )

    def batch(self, inputs: list[TerritoryCoverageInput]) -> list[TerritoryCoverageResult]:
        return [self.assess(inp) for inp in inputs]

    def summary(self, results: list[TerritoryCoverageResult]) -> dict:
        if not results:
            return {}
        scores = [r.composite_score for r in results]
        return {
            "total_territories": len(results),
            "avg_composite_score": round(sum(scores) / len(scores), 1),
            "critical_count": sum(1 for r in results if r.risk == CoverageRisk.critical),
            "high_risk_count": sum(1 for r in results if r.risk == CoverageRisk.high),
            "rebalance_required_count": sum(1 for r in results if r.requires_territory_rebalance),
            "coverage_gap_count": sum(1 for r in results if r.has_coverage_gap),
            "top_pattern": max(set(r.pattern.value for r in results), key=lambda p: sum(1 for r in results if r.pattern.value == p)),
            "total_revenue_at_risk": round(sum(r.estimated_revenue_at_risk for r in results), 2),
            "whitespace_avg_pct": round(sum(r.whitespace_penetration_pct for r in results) / len(results), 1),
            "min_score": min(scores),
            "max_score": max(scores),
            "low_risk_pct": round(sum(1 for r in results if r.risk == CoverageRisk.low) / len(results) * 100, 1),
            "expand_whitespace_count": sum(1 for r in results if r.action == CoverageAction.expand_whitespace),
        }


# Alias with original typo for backward compatibility
SalesTerritoryConverageIntelligenceEngine = SalesTerritoryCoverageIntelligenceEngine
