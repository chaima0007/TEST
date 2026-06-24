"""
Sales Territory Coverage Intelligence Engine.

Évalue la couverture d'un territoire de vente (comptes actifs/négligés, comptes
à forte valeur, whitespace/expansion, prévention du churn) et produit un score
de risque composite avec pattern, sévérité et action recommandée.

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
    evaluation_period_id: str
    account_breadth_score: float
    account_prioritization_score: float
    whitespace_exploitation_score: float
    churn_prevention_score: float
    composite_score: float
    risk: CoverageRisk
    pattern: CoveragePattern
    severity: CoverageSeverity
    action: CoverageAction
    flags: List[str] = field(default_factory=list)
    revenue_at_risk_usd: float = 0.0
    signals: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "rep_id": self.rep_id,
            "region": self.region,
            "evaluation_period_id": self.evaluation_period_id,
            "account_breadth_score": self.account_breadth_score,
            "account_prioritization_score": self.account_prioritization_score,
            "whitespace_exploitation_score": self.whitespace_exploitation_score,
            "churn_prevention_score": self.churn_prevention_score,
            "composite_score": self.composite_score,
            "risk": self.risk.value,
            "pattern": self.pattern.value,
            "severity": self.severity.value,
            "action": self.action.value,
            "flags": list(self.flags),
            "revenue_at_risk_usd": self.revenue_at_risk_usd,
            "signals": list(self.signals),
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

    # ---- Composite & évaluation (base ; affinage ultérieur) ---------------

    def _composite(self, b: float, p: float, w: float, c: float) -> float:
        return round((b + p + w + c) / 4.0, 1)

    def _risk(self, composite: float) -> CoverageRisk:
        if composite >= 60:
            return CoverageRisk.critical
        if composite >= 40:
            return CoverageRisk.high
        if composite >= 20:
            return CoverageRisk.moderate
        return CoverageRisk.low

    def assess(self, inp: TerritoryCoverageInput) -> TerritoryCoverageResult:
        b = self._account_breadth_score(inp)
        p = self._account_prioritization_score(inp)
        w = self._whitespace_exploitation_score(inp)
        c = self._churn_prevention_score(inp)
        composite = self._composite(b, p, w, c)
        risk = self._risk(composite)

        result = TerritoryCoverageResult(
            rep_id=inp.rep_id,
            region=inp.region,
            evaluation_period_id=inp.evaluation_period_id,
            account_breadth_score=b,
            account_prioritization_score=p,
            whitespace_exploitation_score=w,
            churn_prevention_score=c,
            composite_score=composite,
            risk=risk,
            pattern=CoveragePattern.none,
            severity=CoverageSeverity.optimized,
            action=CoverageAction.no_action,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[TerritoryCoverageInput]) -> List[TerritoryCoverageResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        n = len(self._results)
        if n == 0:
            return {"count": 0}
        return {
            "count": n,
            "avg_composite": round(sum(r.composite_score for r in self._results) / n, 1),
        }


# Alias de compatibilité (ancien nom mal orthographié)
SalesTerritoryConverageIntelligenceEngine = SalesTerritoryCoverageIntelligenceEngine
