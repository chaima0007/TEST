from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class TerritoryRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class TerritoryPattern(str, Enum):
    none                   = "none"
    coverage_avoidance     = "coverage_avoidance"
    contact_recycling      = "contact_recycling"
    expansion_neglect      = "expansion_neglect"
    competitive_blindspot  = "competitive_blindspot"
    vertical_concentration = "vertical_concentration"


class TerritorySeverity(str, Enum):
    optimal     = "optimal"
    acceptable  = "acceptable"
    concerning  = "concerning"
    stagnant    = "stagnant"


class TerritoryAction(str, Enum):
    no_action                        = "no_action"
    territory_planning_coaching      = "territory_planning_coaching"
    new_logo_coaching                = "new_logo_coaching"
    competitive_territory_coaching   = "competitive_territory_coaching"
    contact_diversification_coaching = "contact_diversification_coaching"
    territory_coverage_intervention  = "territory_coverage_intervention"
    territory_strategy_reset         = "territory_strategy_reset"


@dataclass
class TerritoryInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_accounts_in_territory: int
    accounts_with_active_opportunity_pct: float
    net_new_logos_acquired_pct: float
    territory_coverage_calls_per_week_avg: float
    icp_fit_accounts_engaged_pct: float
    dormant_account_reactivation_rate_pct: float
    competitive_account_attempted_pct: float
    competitive_displacement_win_rate_pct: float
    expansion_first_meeting_rate_pct: float
    new_logo_pipeline_pct: float
    whitespace_opportunity_identified_pct: float
    territory_growth_rate_pct: float
    same_contact_dependency_pct: float
    accounts_with_no_contact_90d_pct: float
    avg_accounts_worked_simultaneously: float
    vertical_concentration_pct: float
    cross_sell_opportunity_created_pct: float
    total_territory_icp_accounts: int
    avg_opportunity_value_usd: float


@dataclass
class TerritoryResult:
    rep_id: str
    region: str
    territory_risk: TerritoryRisk
    territory_pattern: TerritoryPattern
    territory_severity: TerritorySeverity
    recommended_action: TerritoryAction
    coverage_score: float
    penetration_score: float
    growth_score: float
    competitive_score: float
    territory_composite: float
    has_territory_gap: bool
    requires_territory_coaching: bool
    estimated_whitespace_opportunity_usd: float
    territory_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                              self.rep_id,
            "region":                              self.region,
            "territory_risk":                      self.territory_risk.value,
            "territory_pattern":                   self.territory_pattern.value,
            "territory_severity":                  self.territory_severity.value,
            "recommended_action":                  self.recommended_action.value,
            "coverage_score":                      self.coverage_score,
            "penetration_score":                   self.penetration_score,
            "growth_score":                        self.growth_score,
            "competitive_score":                   self.competitive_score,
            "territory_composite":                 self.territory_composite,
            "has_territory_gap":                   self.has_territory_gap,
            "requires_territory_coaching":         self.requires_territory_coaching,
            "estimated_whitespace_opportunity_usd": self.estimated_whitespace_opportunity_usd,
            "territory_signal":                    self.territory_signal,
        }


class SalesTerritoryWhitespaceIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[TerritoryResult] = []

    def _coverage_score(self, inp: TerritoryInput) -> float:
        score = 0.0
        if inp.icp_fit_accounts_engaged_pct <= 0.25:
            score += 40.0
        elif inp.icp_fit_accounts_engaged_pct <= 0.45:
            score += 22.0
        elif inp.icp_fit_accounts_engaged_pct <= 0.65:
            score += 8.0
        if inp.accounts_with_no_contact_90d_pct >= 0.50:
            score += 35.0
        elif inp.accounts_with_no_contact_90d_pct >= 0.30:
            score += 18.0
        if inp.territory_coverage_calls_per_week_avg <= 0.20:
            score += 25.0
        elif inp.territory_coverage_calls_per_week_avg <= 0.50:
            score += 12.0
        return min(score, 100.0)

    def _penetration_score(self, inp: TerritoryInput) -> float:
        score = 0.0
        if inp.whitespace_opportunity_identified_pct <= 0.15:
            score += 40.0
        elif inp.whitespace_opportunity_identified_pct <= 0.30:
            score += 22.0
        elif inp.whitespace_opportunity_identified_pct <= 0.50:
            score += 8.0
        if inp.same_contact_dependency_pct >= 0.70:
            score += 35.0
        elif inp.same_contact_dependency_pct >= 0.50:
            score += 18.0
        if inp.accounts_with_active_opportunity_pct <= 0.10:
            score += 25.0
        elif inp.accounts_with_active_opportunity_pct <= 0.25:
            score += 12.0
        return min(score, 100.0)

    def _growth_score(self, inp: TerritoryInput) -> float:
        score = 0.0
        if inp.net_new_logos_acquired_pct <= 0.05:
            score += 45.0
        elif inp.net_new_logos_acquired_pct <= 0.12:
            score += 25.0
        elif inp.net_new_logos_acquired_pct <= 0.20:
            score += 10.0
        if inp.new_logo_pipeline_pct <= 0.10:
            score += 30.0
        elif inp.new_logo_pipeline_pct <= 0.25:
            score += 15.0
        if inp.territory_growth_rate_pct <= 0.05:
            score += 25.0
        elif inp.territory_growth_rate_pct <= 0.15:
            score += 12.0
        return min(score, 100.0)

    def _competitive_score(self, inp: TerritoryInput) -> float:
        score = 0.0
        if inp.competitive_account_attempted_pct <= 0.15:
            score += 40.0
        elif inp.competitive_account_attempted_pct <= 0.35:
            score += 22.0
        elif inp.competitive_account_attempted_pct <= 0.55:
            score += 8.0
        if inp.competitive_displacement_win_rate_pct <= 0.10:
            score += 35.0
        elif inp.competitive_displacement_win_rate_pct <= 0.25:
            score += 18.0
        if inp.vertical_concentration_pct >= 0.80:
            score += 25.0
        elif inp.vertical_concentration_pct >= 0.65:
            score += 12.0
        return min(score, 100.0)

    def _detect_pattern(self, inp: TerritoryInput,
                         coverage: float, penetration: float,
                         growth: float, competitive: float) -> TerritoryPattern:
        if inp.accounts_with_no_contact_90d_pct >= 0.45 and coverage >= 35:
            return TerritoryPattern.coverage_avoidance
        if inp.same_contact_dependency_pct >= 0.65 and penetration >= 35:
            return TerritoryPattern.contact_recycling
        if inp.new_logo_pipeline_pct <= 0.15 and growth >= 35:
            return TerritoryPattern.expansion_neglect
        if inp.competitive_account_attempted_pct <= 0.20 and competitive >= 30:
            return TerritoryPattern.competitive_blindspot
        if inp.vertical_concentration_pct >= 0.75 and competitive >= 25:
            return TerritoryPattern.vertical_concentration
        return TerritoryPattern.none

    def _risk_level(self, composite: float) -> TerritoryRisk:
        if composite >= 60:
            return TerritoryRisk.critical
        if composite >= 40:
            return TerritoryRisk.high
        if composite >= 20:
            return TerritoryRisk.moderate
        return TerritoryRisk.low

    def _severity(self, composite: float) -> TerritorySeverity:
        if composite >= 60:
            return TerritorySeverity.stagnant
        if composite >= 40:
            return TerritorySeverity.concerning
        if composite >= 20:
            return TerritorySeverity.acceptable
        return TerritorySeverity.optimal

    def _action(self, risk: TerritoryRisk, pattern: TerritoryPattern) -> TerritoryAction:
        if risk == TerritoryRisk.critical:
            if pattern == TerritoryPattern.coverage_avoidance:
                return TerritoryAction.territory_coverage_intervention
            if pattern == TerritoryPattern.contact_recycling:
                return TerritoryAction.contact_diversification_coaching
            return TerritoryAction.territory_strategy_reset
        if risk == TerritoryRisk.high:
            if pattern == TerritoryPattern.expansion_neglect:
                return TerritoryAction.new_logo_coaching
            if pattern == TerritoryPattern.competitive_blindspot:
                return TerritoryAction.competitive_territory_coaching
            return TerritoryAction.territory_planning_coaching
        if risk == TerritoryRisk.moderate:
            return TerritoryAction.territory_planning_coaching
        return TerritoryAction.no_action

    def _has_territory_gap(self, composite: float, inp: TerritoryInput) -> bool:
        return (
            composite >= 40
            or inp.accounts_with_no_contact_90d_pct >= 0.35
            or inp.net_new_logos_acquired_pct <= 0.08
        )

    def _requires_territory_coaching(self, composite: float, inp: TerritoryInput) -> bool:
        return (
            composite >= 30
            or inp.icp_fit_accounts_engaged_pct <= 0.40
            or inp.same_contact_dependency_pct >= 0.50
        )

    def _estimated_whitespace_opportunity(self, inp: TerritoryInput, composite: float) -> float:
        uncovered = max(0.0, 1.0 - inp.icp_fit_accounts_engaged_pct)
        return round(
            inp.total_territory_icp_accounts
            * inp.avg_opportunity_value_usd
            * uncovered
            * (composite / 100.0),
            2,
        )

    def _signal(self, inp: TerritoryInput,
                pattern: TerritoryPattern, composite: float) -> str:
        if pattern == TerritoryPattern.none and composite < 20:
            return "Territory coverage strong — ICP engagement, new logo pursuit, and competitive displacement within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.icp_fit_accounts_engaged_pct * 100:.0f}% ICP accounts engaged")
        parts.append(f"{inp.net_new_logos_acquired_pct * 100:.0f}% new logos acquired")
        parts.append(f"{inp.accounts_with_no_contact_90d_pct * 100:.0f}% dormant 90d")
        label = pattern.value.replace("_", " ") if pattern != TerritoryPattern.none else "Territory risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    def assess(self, inp: TerritoryInput) -> TerritoryResult:
        coverage    = round(self._coverage_score(inp), 1)
        penetration = round(self._penetration_score(inp), 1)
        growth      = round(self._growth_score(inp), 1)
        competitive = round(self._competitive_score(inp), 1)
        composite   = round(
            coverage * 0.30 + penetration * 0.30 + growth * 0.25 + competitive * 0.15, 1
        )
        composite = min(composite, 100.0)
        pattern  = self._detect_pattern(inp, coverage, penetration, growth, competitive)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)
        gap      = self._has_territory_gap(composite, inp)
        coach    = self._requires_territory_coaching(composite, inp)
        opp      = self._estimated_whitespace_opportunity(inp, composite)
        signal   = self._signal(inp, pattern, composite)
        result = TerritoryResult(
            rep_id=inp.rep_id, region=inp.region,
            territory_risk=risk, territory_pattern=pattern,
            territory_severity=severity, recommended_action=action,
            coverage_score=coverage, penetration_score=penetration,
            growth_score=growth, competitive_score=competitive,
            territory_composite=composite,
            has_territory_gap=gap, requires_territory_coaching=coach,
            estimated_whitespace_opportunity_usd=opp,
            territory_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[TerritoryInput]) -> list[TerritoryResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0, "risk_counts": {}, "pattern_counts": {},
                "severity_counts": {}, "action_counts": {},
                "avg_territory_composite": 0.0, "territory_gap_count": 0, "coaching_count": 0,
                "avg_coverage_score": 0.0, "avg_penetration_score": 0.0,
                "avg_growth_score": 0.0, "avg_competitive_score": 0.0,
                "total_estimated_whitespace_opportunity_usd": 0.0,
            }
        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        tc = tcov = tpen = tgro = tcom = topp = 0.0
        for r in self._results:
            risk_counts[r.territory_risk.value]         = risk_counts.get(r.territory_risk.value, 0) + 1
            pattern_counts[r.territory_pattern.value]   = pattern_counts.get(r.territory_pattern.value, 0) + 1
            severity_counts[r.territory_severity.value] = severity_counts.get(r.territory_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            tc   += r.territory_composite
            tcov += r.coverage_score
            tpen += r.penetration_score
            tgro += r.growth_score
            tcom += r.competitive_score
            topp += r.estimated_whitespace_opportunity_usd
        n = len(self._results)
        return {
            "total":                                     n,
            "risk_counts":                               risk_counts,
            "pattern_counts":                            pattern_counts,
            "severity_counts":                           severity_counts,
            "action_counts":                             action_counts,
            "avg_territory_composite":                   round(tc / n, 1),
            "territory_gap_count":                       sum(1 for r in self._results if r.has_territory_gap),
            "coaching_count":                            sum(1 for r in self._results if r.requires_territory_coaching),
            "avg_coverage_score":                        round(tcov / n, 1),
            "avg_penetration_score":                     round(tpen / n, 1),
            "avg_growth_score":                          round(tgro / n, 1),
            "avg_competitive_score":                     round(tcom / n, 1),
            "total_estimated_whitespace_opportunity_usd": round(topp, 2),
        }
