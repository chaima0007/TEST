"""
Sales Territory Coverage Intelligence Engine.

Évalue la couverture d'un territoire de vente (comptes actifs/négligés, comptes
à forte valeur, whitespace/expansion, prévention du churn) et produit un score
de risque composite avec pattern, sévérité, action, flags, revenue-at-risk et
un signal lisible.

Sous-scores : plus le score est élevé, plus le risque est élevé.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


# ===========================================================================
# Enums
# ===========================================================================

class CoverageRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class CoveragePattern(str, Enum):
    none = "none"
    account_neglect = "account_neglect"
    high_value_underserved = "high_value_underserved"
    whitespace_ignored = "whitespace_ignored"
    churn_risk_uncovered = "churn_risk_uncovered"
    revenue_concentration = "revenue_concentration"


class CoverageSeverity(str, Enum):
    optimized = "optimized"
    gaps_detected = "gaps_detected"
    underserved = "underserved"
    critical = "critical"


class CoverageAction(str, Enum):
    no_action = "no_action"
    account_outreach_blitz = "account_outreach_blitz"
    high_value_focus = "high_value_focus"
    whitespace_expansion = "whitespace_expansion"
    churn_prevention_sprint = "churn_prevention_sprint"
    territory_restructure = "territory_restructure"


# ===========================================================================
# Dataclasses
# ===========================================================================

@dataclass
class TerritoryCoverageInput:
    rep_id: str = ""
    region: str = ""
    evaluation_period_id: str = ""
    total_accounts_in_territory: int = 0
    accounts_active_count: int = 0
    accounts_neglected_count: int = 0
    high_value_accounts_total: int = 0
    high_value_accounts_engaged_count: int = 0
    new_logo_accounts_added: int = 0
    new_logo_converted_count: int = 0
    whitespace_accounts_identified: int = 0
    whitespace_accounts_pursued: int = 0
    churn_risk_accounts_total: int = 0
    churn_risk_accounts_contacted: int = 0
    top_account_revenue_concentration_pct: float = 0.0
    avg_contacts_per_account: float = 0.0
    expansion_signals_identified: int = 0
    expansion_signals_acted_upon: int = 0
    multi_product_penetration_pct: float = 0.0
    territory_revenue_growth_pct: float = 0.0
    avg_account_revenue_usd: float = 0.0
    accounts_without_next_steps_pct: float = 0.0


@dataclass
class TerritoryCoverageResult:
    rep_id: str
    region: str
    account_breadth_score: float
    account_prioritization_score: float
    whitespace_exploitation_score: float
    churn_prevention_score: float
    territory_coverage_composite: float
    coverage_risk: CoverageRisk
    coverage_pattern: CoveragePattern
    coverage_severity: CoverageSeverity
    recommended_action: CoverageAction
    has_coverage_gap: bool
    requires_territory_rebalance: bool
    estimated_revenue_at_risk_usd: float
    coverage_signal: str
    evaluation_period_id: str = ""

    def to_dict(self) -> Dict:
        return {
            "rep_id": self.rep_id,
            "region": self.region,
            "coverage_risk": self.coverage_risk.value,
            "coverage_pattern": self.coverage_pattern.value,
            "coverage_severity": self.coverage_severity.value,
            "recommended_action": self.recommended_action.value,
            "account_breadth_score": self.account_breadth_score,
            "account_prioritization_score": self.account_prioritization_score,
            "whitespace_exploitation_score": self.whitespace_exploitation_score,
            "churn_prevention_score": self.churn_prevention_score,
            "territory_coverage_composite": self.territory_coverage_composite,
            "has_coverage_gap": self.has_coverage_gap,
            "requires_territory_rebalance": self.requires_territory_rebalance,
            "estimated_revenue_at_risk_usd": self.estimated_revenue_at_risk_usd,
            "coverage_signal": self.coverage_signal,
        }


# ===========================================================================
# Engine
# ===========================================================================

class SalesTerritoryCoverageIntelligenceEngine:
    def __init__(self) -> None:
        self._results: List[TerritoryCoverageResult] = []

    # ---- Sous-scores (plus haut = plus de risque) -------------------------

    def _account_breadth_score(self, inp: TerritoryCoverageInput) -> float:
        denom = max(inp.total_accounts_in_territory, 1)
        score = 0.0

        neglect_ratio = inp.accounts_neglected_count / denom
        if neglect_ratio >= 0.40:
            score += 40
        elif neglect_ratio >= 0.25:
            score += 25
        elif neglect_ratio >= 0.10:
            score += 10

        active_ratio = inp.accounts_active_count / denom
        if active_ratio < 0.30:
            score += 25
        elif active_ratio < 0.50:
            score += 12

        ns = inp.accounts_without_next_steps_pct
        if ns >= 0.60:
            score += 20
        elif ns >= 0.40:
            score += 10

        return float(min(score, 100.0))

    def _account_prioritization_score(self, inp: TerritoryCoverageInput) -> float:
        score = 0.0

        hv_ratio = inp.high_value_accounts_engaged_count / max(inp.high_value_accounts_total, 1)
        if hv_ratio < 0.40:
            score += 40
        elif hv_ratio < 0.60:
            score += 25
        elif hv_ratio < 0.80:
            score += 10

        conc = inp.top_account_revenue_concentration_pct
        if conc >= 0.80:
            score += 30
        elif conc >= 0.60:
            score += 15

        contacts = inp.avg_contacts_per_account
        if contacts < 1.0:
            score += 20
        elif contacts < 2.0:
            score += 10

        return float(min(score, 100.0))

    def _whitespace_exploitation_score(self, inp: TerritoryCoverageInput) -> float:
        score = 0.0

        acted_ratio = inp.expansion_signals_acted_upon / max(inp.expansion_signals_identified, 1)
        if acted_ratio < 0.20:
            score += 35
        elif acted_ratio < 0.40:
            score += 20
        elif acted_ratio < 0.60:
            score += 8

        ws_ratio = inp.whitespace_accounts_pursued / max(inp.whitespace_accounts_identified, 1)
        if ws_ratio < 0.20:
            score += 30
        elif ws_ratio < 0.40:
            score += 15

        mp = inp.multi_product_penetration_pct
        if mp < 0.20:
            score += 20
        elif mp < 0.35:
            score += 10

        logo_ratio = inp.new_logo_converted_count / max(inp.new_logo_accounts_added, 1)
        if logo_ratio < 0.20:
            score += 15

        return float(min(score, 100.0))

    def _churn_prevention_score(self, inp: TerritoryCoverageInput) -> float:
        score = 0.0

        coverage = inp.churn_risk_accounts_contacted / max(inp.churn_risk_accounts_total, 1)
        if coverage < 0.40:
            score += 40
        elif coverage < 0.60:
            score += 25
        elif coverage < 0.80:
            score += 10

        growth = inp.territory_revenue_growth_pct
        if growth < -0.10:
            score += 35
        elif growth < 0:
            score += 15

        neglected = inp.accounts_neglected_count
        if neglected >= 5:
            score += 15
        elif neglected >= 3:
            score += 8

        return float(min(score, 100.0))

    # ---- Composite, niveaux, pattern, action, flags -----------------------

    def _composite(self, b: float, p: float, w: float, c: float) -> float:
        weighted = b * 0.25 + p * 0.30 + w * 0.25 + c * 0.20
        return float(min(round(weighted, 1), 100.0))

    def _risk_level(self, composite: float) -> CoverageRisk:
        if composite >= 60:
            return CoverageRisk.critical
        if composite >= 40:
            return CoverageRisk.high
        if composite >= 20:
            return CoverageRisk.moderate
        return CoverageRisk.low

    def _severity(self, composite: float) -> CoverageSeverity:
        if composite >= 60:
            return CoverageSeverity.critical
        if composite >= 40:
            return CoverageSeverity.underserved
        if composite >= 20:
            return CoverageSeverity.gaps_detected
        return CoverageSeverity.optimized

    def _detect_pattern(
        self,
        inp: TerritoryCoverageInput,
        breadth: float,
        prioritization: float,
        whitespace: float,
        churn: float,
    ) -> CoveragePattern:
        churn_ratio = inp.churn_risk_accounts_contacted / max(inp.churn_risk_accounts_total, 1)
        hv_ratio = inp.high_value_accounts_engaged_count / max(inp.high_value_accounts_total, 1)
        acted_ratio = inp.expansion_signals_acted_upon / max(inp.expansion_signals_identified, 1)

        if inp.top_account_revenue_concentration_pct >= 0.70 and prioritization >= 30:
            return CoveragePattern.revenue_concentration
        if churn >= 30 and churn_ratio < 0.40:
            return CoveragePattern.churn_risk_uncovered
        if prioritization >= 35 and hv_ratio < 0.60:
            return CoveragePattern.high_value_underserved
        if whitespace >= 35 and acted_ratio < 0.20:
            return CoveragePattern.whitespace_ignored
        if breadth >= 30 and inp.accounts_neglected_count >= 5:
            return CoveragePattern.account_neglect
        return CoveragePattern.none

    def _action(self, risk: CoverageRisk, pattern: CoveragePattern) -> CoverageAction:
        if risk == CoverageRisk.low:
            return CoverageAction.no_action
        if risk == CoverageRisk.critical:
            if pattern == CoveragePattern.churn_risk_uncovered:
                return CoverageAction.churn_prevention_sprint
            return CoverageAction.territory_restructure
        if risk == CoverageRisk.high:
            if pattern == CoveragePattern.churn_risk_uncovered:
                return CoverageAction.churn_prevention_sprint
            if pattern == CoveragePattern.whitespace_ignored:
                return CoverageAction.whitespace_expansion
            if pattern == CoveragePattern.high_value_underserved:
                return CoverageAction.high_value_focus
            return CoverageAction.account_outreach_blitz
        # moderate
        if pattern == CoveragePattern.whitespace_ignored:
            return CoverageAction.whitespace_expansion
        return CoverageAction.account_outreach_blitz

    def _has_coverage_gap(self, composite: float, inp: TerritoryCoverageInput) -> bool:
        if composite >= 40:
            return True
        if inp.accounts_neglected_count >= 5:
            return True
        if inp.churn_risk_accounts_total > 0:
            ratio = inp.churn_risk_accounts_contacted / inp.churn_risk_accounts_total
            if ratio < 0.40:
                return True
        return False

    def _requires_territory_rebalance(self, composite: float, inp: TerritoryCoverageInput) -> bool:
        if composite >= 30:
            return True
        if inp.top_account_revenue_concentration_pct >= 0.70:
            return True
        hv_ratio = inp.high_value_accounts_engaged_count / max(inp.high_value_accounts_total, 1)
        if hv_ratio < 0.40:
            return True
        return False

    def _estimated_revenue_at_risk(self, inp: TerritoryCoverageInput, composite: float) -> float:
        return round(inp.accounts_neglected_count * inp.avg_account_revenue_usd * (composite / 100.0), 2)

    def _signal(self, inp: TerritoryCoverageInput, pattern: CoveragePattern, composite: float) -> str:
        if pattern == CoveragePattern.none and composite < 20:
            return "Territory coverage optimized across all segments"

        parts: List[str] = []
        if inp.accounts_neglected_count >= 3:
            parts.append(f"{inp.accounts_neglected_count} accounts neglected")

        hv_ratio = inp.high_value_accounts_engaged_count / max(inp.high_value_accounts_total, 1)
        if hv_ratio < 0.60:
            parts.append(f"high-value coverage at {hv_ratio * 100:.0f}%")

        acted_ratio = inp.expansion_signals_acted_upon / max(inp.expansion_signals_identified, 1)
        if acted_ratio < 0.40:
            parts.append("whitespace opportunities missed")

        churn_ratio = inp.churn_risk_accounts_contacted / max(inp.churn_risk_accounts_total, 1)
        if churn_ratio < 0.50:
            parts.append(f"churn risk contacts at {churn_ratio * 100:.0f}%")

        if pattern == CoveragePattern.none:
            prefix = "Coverage risk"
        else:
            prefix = pattern.value.replace("_", " ").capitalize()

        if not parts:
            parts.append("territory coverage gaps detected")

        return f"{prefix}: {'; '.join(parts)} (composite {composite:.0f})"

    # ---- Assess / batch / summary -----------------------------------------

    def assess(self, inp: TerritoryCoverageInput) -> TerritoryCoverageResult:
        b = self._account_breadth_score(inp)
        p = self._account_prioritization_score(inp)
        w = self._whitespace_exploitation_score(inp)
        c = self._churn_prevention_score(inp)
        composite = self._composite(b, p, w, c)
        risk = self._risk_level(composite)
        pattern = self._detect_pattern(inp, b, p, w, c)
        severity = self._severity(composite)
        action = self._action(risk, pattern)

        result = TerritoryCoverageResult(
            rep_id=inp.rep_id,
            region=inp.region,
            evaluation_period_id=inp.evaluation_period_id,
            account_breadth_score=b,
            account_prioritization_score=p,
            whitespace_exploitation_score=w,
            churn_prevention_score=c,
            territory_coverage_composite=composite,
            coverage_risk=risk,
            coverage_pattern=pattern,
            coverage_severity=severity,
            recommended_action=action,
            has_coverage_gap=self._has_coverage_gap(composite, inp),
            requires_territory_rebalance=self._requires_territory_rebalance(composite, inp),
            estimated_revenue_at_risk_usd=self._estimated_revenue_at_risk(inp, composite),
            coverage_signal=self._signal(inp, pattern, composite),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[TerritoryCoverageInput]) -> List[TerritoryCoverageResult]:
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
                "avg_territory_coverage_composite": 0.0,
                "coverage_gap_count": 0,
                "rebalance_count": 0,
                "avg_account_breadth_score": 0.0,
                "avg_account_prioritization_score": 0.0,
                "avg_whitespace_exploitation_score": 0.0,
                "avg_churn_prevention_score": 0.0,
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
            "risk_counts": counts("coverage_risk"),
            "pattern_counts": counts("coverage_pattern"),
            "severity_counts": counts("coverage_severity"),
            "action_counts": counts("recommended_action"),
            "avg_territory_coverage_composite": avg("territory_coverage_composite"),
            "coverage_gap_count": sum(1 for r in self._results if r.has_coverage_gap),
            "rebalance_count": sum(1 for r in self._results if r.requires_territory_rebalance),
            "avg_account_breadth_score": avg("account_breadth_score"),
            "avg_account_prioritization_score": avg("account_prioritization_score"),
            "avg_whitespace_exploitation_score": avg("whitespace_exploitation_score"),
            "avg_churn_prevention_score": avg("churn_prevention_score"),
            "total_estimated_revenue_at_risk_usd": round(
                sum(r.estimated_revenue_at_risk_usd for r in self._results), 2
            ),
        }


# Alias de compatibilité (ancien nom mal orthographié)
SalesTerritoryConverageIntelligenceEngine = SalesTerritoryCoverageIntelligenceEngine
