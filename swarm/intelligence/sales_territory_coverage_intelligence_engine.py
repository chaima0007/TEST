from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class CoverageRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CoveragePattern(str, Enum):
    none                   = "none"
    account_neglect        = "account_neglect"
    high_value_underserved = "high_value_underserved"
    whitespace_ignored     = "whitespace_ignored"
    churn_risk_uncovered   = "churn_risk_uncovered"
    revenue_concentration  = "revenue_concentration"


class CoverageSeverity(str, Enum):
    optimized     = "optimized"
    gaps_detected = "gaps_detected"
    underserved   = "underserved"
    critical      = "critical"


class CoverageAction(str, Enum):
    no_action                = "no_action"
    account_outreach_blitz   = "account_outreach_blitz"
    high_value_focus         = "high_value_focus"
    whitespace_expansion     = "whitespace_expansion"
    churn_prevention_sprint  = "churn_prevention_sprint"
    territory_restructure    = "territory_restructure"


@dataclass
class TerritoryCoverageInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_accounts_in_territory: int
    accounts_active_count: int
    accounts_neglected_count: int
    high_value_accounts_total: int
    high_value_accounts_engaged_count: int
    new_logo_accounts_added: int
    new_logo_converted_count: int
    whitespace_accounts_identified: int
    whitespace_accounts_pursued: int
    churn_risk_accounts_total: int
    churn_risk_accounts_contacted: int
    top_account_revenue_concentration_pct: float
    avg_contacts_per_account: float
    expansion_signals_identified: int
    expansion_signals_acted_upon: int
    multi_product_penetration_pct: float
    territory_revenue_growth_pct: float
    avg_account_revenue_usd: float
    accounts_without_next_steps_pct: float


@dataclass
class TerritoryCoverageResult:
    rep_id: str
    region: str
    coverage_risk: CoverageRisk
    coverage_pattern: CoveragePattern
    coverage_severity: CoverageSeverity
    recommended_action: CoverageAction
    account_breadth_score: float
    account_prioritization_score: float
    whitespace_exploitation_score: float
    churn_prevention_score: float
    territory_coverage_composite: float
    has_coverage_gap: bool
    requires_territory_rebalance: bool
    estimated_revenue_at_risk_usd: float
    coverage_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                          self.rep_id,
            "region":                          self.region,
            "coverage_risk":                   self.coverage_risk.value,
            "coverage_pattern":                self.coverage_pattern.value,
            "coverage_severity":               self.coverage_severity.value,
            "recommended_action":              self.recommended_action.value,
            "account_breadth_score":           self.account_breadth_score,
            "account_prioritization_score":    self.account_prioritization_score,
            "whitespace_exploitation_score":   self.whitespace_exploitation_score,
            "churn_prevention_score":          self.churn_prevention_score,
            "territory_coverage_composite":    self.territory_coverage_composite,
            "has_coverage_gap":                self.has_coverage_gap,
            "requires_territory_rebalance":    self.requires_territory_rebalance,
            "estimated_revenue_at_risk_usd":   self.estimated_revenue_at_risk_usd,
            "coverage_signal":                 self.coverage_signal,
        }


class SalesTerritoryCoverageIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[TerritoryCoverageResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _account_breadth_score(self, inp: TerritoryCoverageInput) -> float:
        score = 0.0
        total = max(inp.total_accounts_in_territory, 1)

        neglect_ratio = inp.accounts_neglected_count / total
        if neglect_ratio >= 0.40:
            score += 40.0
        elif neglect_ratio >= 0.25:
            score += 25.0
        elif neglect_ratio >= 0.10:
            score += 10.0

        active_ratio = inp.accounts_active_count / total
        if active_ratio < 0.30:
            score += 25.0
        elif active_ratio < 0.50:
            score += 12.0

        if inp.accounts_without_next_steps_pct >= 0.60:
            score += 20.0
        elif inp.accounts_without_next_steps_pct >= 0.40:
            score += 10.0

        return min(score, 100.0)

    def _account_prioritization_score(self, inp: TerritoryCoverageInput) -> float:
        score = 0.0
        hv_total = max(inp.high_value_accounts_total, 1)
        hv_engaged_ratio = inp.high_value_accounts_engaged_count / hv_total

        if hv_engaged_ratio < 0.40:
            score += 40.0
        elif hv_engaged_ratio < 0.60:
            score += 25.0
        elif hv_engaged_ratio < 0.80:
            score += 10.0

        # Dangerous over-concentration in few accounts
        if inp.top_account_revenue_concentration_pct >= 0.80:
            score += 30.0
        elif inp.top_account_revenue_concentration_pct >= 0.60:
            score += 15.0

        if inp.avg_contacts_per_account < 1.0:
            score += 20.0
        elif inp.avg_contacts_per_account < 2.0:
            score += 10.0

        return min(score, 100.0)

    def _whitespace_exploitation_score(self, inp: TerritoryCoverageInput) -> float:
        score = 0.0
        exp_identified = max(inp.expansion_signals_identified, 1)
        ws_identified  = max(inp.whitespace_accounts_identified, 1)

        acted_ratio = inp.expansion_signals_acted_upon / exp_identified
        if acted_ratio < 0.20:
            score += 35.0
        elif acted_ratio < 0.40:
            score += 20.0
        elif acted_ratio < 0.60:
            score += 8.0

        ws_ratio = inp.whitespace_accounts_pursued / ws_identified
        if ws_ratio < 0.20:
            score += 30.0
        elif ws_ratio < 0.40:
            score += 15.0

        if inp.multi_product_penetration_pct < 0.20:
            score += 20.0
        elif inp.multi_product_penetration_pct < 0.35:
            score += 10.0

        new_logo_total = max(inp.new_logo_accounts_added, 1)
        if inp.new_logo_converted_count / new_logo_total < 0.20:
            score += 15.0

        return min(score, 100.0)

    def _churn_prevention_score(self, inp: TerritoryCoverageInput) -> float:
        score = 0.0
        churn_total = max(inp.churn_risk_accounts_total, 1)

        churn_coverage = inp.churn_risk_accounts_contacted / churn_total
        if churn_coverage < 0.40:
            score += 40.0
        elif churn_coverage < 0.60:
            score += 25.0
        elif churn_coverage < 0.80:
            score += 10.0

        if inp.territory_revenue_growth_pct < -0.10:
            score += 35.0
        elif inp.territory_revenue_growth_pct < 0:
            score += 15.0

        if inp.accounts_neglected_count >= 5:
            score += 15.0
        elif inp.accounts_neglected_count >= 3:
            score += 8.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: TerritoryCoverageInput,
                         breadth: float, prioritization: float,
                         whitespace: float, churn: float) -> CoveragePattern:
        # Priority: revenue_concentration > churn_risk_uncovered > high_value_underserved
        #           > whitespace_ignored > account_neglect > none
        if inp.top_account_revenue_concentration_pct >= 0.70 and prioritization >= 30:
            return CoveragePattern.revenue_concentration

        churn_total = max(inp.churn_risk_accounts_total, 1)
        churn_ratio = inp.churn_risk_accounts_contacted / churn_total
        if churn >= 30 and churn_ratio < 0.40:
            return CoveragePattern.churn_risk_uncovered

        hv_total  = max(inp.high_value_accounts_total, 1)
        hv_ratio  = inp.high_value_accounts_engaged_count / hv_total
        if prioritization >= 35 and hv_ratio < 0.60:
            return CoveragePattern.high_value_underserved

        exp_identified = max(inp.expansion_signals_identified, 1)
        acted_ratio    = inp.expansion_signals_acted_upon / exp_identified
        if whitespace >= 35 and acted_ratio < 0.20:
            return CoveragePattern.whitespace_ignored

        if breadth >= 30 and inp.accounts_neglected_count >= 5:
            return CoveragePattern.account_neglect

        return CoveragePattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

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

    def _action(self, risk: CoverageRisk, pattern: CoveragePattern) -> CoverageAction:
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
        if risk == CoverageRisk.moderate:
            if pattern == CoveragePattern.whitespace_ignored:
                return CoverageAction.whitespace_expansion
            return CoverageAction.account_outreach_blitz
        return CoverageAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_coverage_gap(self, composite: float, inp: TerritoryCoverageInput) -> bool:
        churn_total = max(inp.churn_risk_accounts_total, 1)
        return (
            composite >= 40
            or inp.accounts_neglected_count >= 5
            or (inp.churn_risk_accounts_total > 0
                and inp.churn_risk_accounts_contacted / churn_total < 0.40)
        )

    def _requires_territory_rebalance(self, composite: float,
                                       inp: TerritoryCoverageInput) -> bool:
        hv_total = max(inp.high_value_accounts_total, 1)
        return (
            composite >= 30
            or inp.top_account_revenue_concentration_pct >= 0.70
            or inp.high_value_accounts_engaged_count / hv_total < 0.40
        )

    # ------------------------------------------------------------------
    # Revenue at risk
    # ------------------------------------------------------------------

    def _estimated_revenue_at_risk(self, inp: TerritoryCoverageInput,
                                    composite: float) -> float:
        return round(
            inp.accounts_neglected_count * inp.avg_account_revenue_usd * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: TerritoryCoverageInput,
                pattern: CoveragePattern, composite: float) -> str:
        if pattern == CoveragePattern.none and composite < 20:
            return "Territory coverage optimized across all segments"
        parts: list[str] = []
        if inp.accounts_neglected_count >= 3:
            parts.append(f"{inp.accounts_neglected_count} accounts neglected")
        hv_total = max(inp.high_value_accounts_total, 1)
        hv_ratio = inp.high_value_accounts_engaged_count / hv_total
        if hv_ratio < 0.60:
            parts.append(f"{hv_ratio*100:.0f}% high-value coverage")
        exp_identified = max(inp.expansion_signals_identified, 1)
        acted_ratio    = inp.expansion_signals_acted_upon / exp_identified
        if acted_ratio < 0.40:
            parts.append(f"{inp.whitespace_accounts_identified - inp.whitespace_accounts_pursued} whitespace opportunities missed")
        churn_total = max(inp.churn_risk_accounts_total, 1)
        if inp.churn_risk_accounts_contacted / churn_total < 0.50:
            parts.append(f"{int((inp.churn_risk_accounts_contacted / churn_total)*100)}% churn risk contacts")
        label = pattern.value.replace("_", " ") if pattern != CoveragePattern.none else "Coverage risk"
        summary = " — ".join(parts) if parts else "territory coverage gaps detected"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: TerritoryCoverageInput) -> TerritoryCoverageResult:
        breadth        = round(self._account_breadth_score(inp), 1)
        prioritization = round(self._account_prioritization_score(inp), 1)
        whitespace     = round(self._whitespace_exploitation_score(inp), 1)
        churn          = round(self._churn_prevention_score(inp), 1)

        composite = round(breadth * 0.25 + prioritization * 0.30 + whitespace * 0.25 + churn * 0.20, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, breadth, prioritization, whitespace, churn)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_coverage_gap(composite, inp)
        rebal    = self._requires_territory_rebalance(composite, inp)
        revenue  = self._estimated_revenue_at_risk(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = TerritoryCoverageResult(
            rep_id=inp.rep_id,
            region=inp.region,
            coverage_risk=risk,
            coverage_pattern=pattern,
            coverage_severity=severity,
            recommended_action=action,
            account_breadth_score=breadth,
            account_prioritization_score=prioritization,
            whitespace_exploitation_score=whitespace,
            churn_prevention_score=churn,
            territory_coverage_composite=composite,
            has_coverage_gap=gap,
            requires_territory_rebalance=rebal,
            estimated_revenue_at_risk_usd=revenue,
            coverage_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[TerritoryCoverageInput]) -> list[TerritoryCoverageResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
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

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_br = total_pr = total_ws = total_ch = total_rev = 0.0

        for r in self._results:
            risk_counts[r.coverage_risk.value]       = risk_counts.get(r.coverage_risk.value, 0) + 1
            pattern_counts[r.coverage_pattern.value] = pattern_counts.get(r.coverage_pattern.value, 0) + 1
            severity_counts[r.coverage_severity.value] = severity_counts.get(r.coverage_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.territory_coverage_composite
            total_br   += r.account_breadth_score
            total_pr   += r.account_prioritization_score
            total_ws   += r.whitespace_exploitation_score
            total_ch   += r.churn_prevention_score
            total_rev  += r.estimated_revenue_at_risk_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_territory_coverage_composite":     round(total_comp / n, 1),
            "coverage_gap_count":                   sum(1 for r in self._results if r.has_coverage_gap),
            "rebalance_count":                      sum(1 for r in self._results if r.requires_territory_rebalance),
            "avg_account_breadth_score":            round(total_br / n, 1),
            "avg_account_prioritization_score":     round(total_pr / n, 1),
            "avg_whitespace_exploitation_score":    round(total_ws / n, 1),
            "avg_churn_prevention_score":           round(total_ch / n, 1),
            "total_estimated_revenue_at_risk_usd":  round(total_rev, 2),
        }
