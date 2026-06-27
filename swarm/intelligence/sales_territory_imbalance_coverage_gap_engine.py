from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class TerritoryRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class TerritoryPattern(str, Enum):
    none                = "none"
    overloaded_rep      = "overloaded_rep"
    starved_territory   = "starved_territory"
    whitespace_blind    = "whitespace_blind"
    coverage_ghost      = "coverage_ghost"
    renewal_neglect     = "renewal_neglect"


class TerritorySeverity(str, Enum):
    balanced     = "balanced"
    drifting     = "drifting"
    imbalanced   = "imbalanced"
    critical     = "critical"


class TerritoryAction(str, Enum):
    no_action                      = "no_action"
    territory_health_check         = "territory_health_check"
    account_redistribution_review  = "account_redistribution_review"
    whitespace_activation_plan     = "whitespace_activation_plan"
    coverage_model_reassignment    = "coverage_model_reassignment"
    renewal_coverage_remediation   = "renewal_coverage_remediation"
    territory_redesign_escalation  = "territory_redesign_escalation"


@dataclass
class TerritoryInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    accounts_per_rep_vs_benchmark:       float   # 0-∞ (1.0 = at benchmark)
    revenue_per_account_vs_benchmark:    float   # 0-∞ (1.0 = at benchmark)
    whitespace_accounts_untouched_pct:   float   # 0-1 % of TAM not contacted
    renewal_coverage_rate_pct:           float   # 0-1 % renewals with active coverage
    territory_quota_vs_capacity_ratio:   float   # 0-∞ (quota / sellable capacity; >1 = overloaded)
    active_accounts_pct:                 float   # 0-1 % of assigned accounts with activity
    avg_travel_time_per_call_hours:      float   # avg hours travel per customer call
    geographic_concentration_score:      float   # 0-1 (1 = all accounts in same city)
    icp_account_coverage_pct:            float   # 0-1 % ICP accounts covered
    new_logo_territory_penetration_pct:  float   # 0-1 % new logos opened in territory
    competitive_displacement_coverage:  float   # 0-1 % competitor accounts touched
    account_scoring_adoption_rate_pct:   float   # 0-1 % accounts with health scores
    stale_account_rate_pct:              float   # 0-1 % accounts untouched 90+ days
    multi_product_territory_pct:         float   # 0-1 % accounts with >1 product
    territory_nps_avg:                   float   # -1 to 1 avg NPS in territory
    expansion_opportunity_capture_pct:   float   # 0-1 % expansion opps actioned
    rep_tenure_territory_months:         float   # months rep has owned territory
    total_accounts_in_territory:         int
    avg_arr_per_account_usd:             float


@dataclass
class TerritoryResult:
    rep_id:                              str
    region:                              str
    territory_risk:                      TerritoryRisk
    territory_pattern:                   TerritoryPattern
    territory_severity:                  TerritorySeverity
    recommended_action:                  TerritoryAction
    load_score:                          float
    coverage_score:                      float
    penetration_score:                   float
    efficiency_score:                    float
    territory_composite:                 float
    has_territory_gap:                   bool
    requires_territory_intervention:     bool
    estimated_uncaptured_revenue_usd:    float
    territory_signal:                    str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                            self.rep_id,
            "region":                            self.region,
            "territory_risk":                    self.territory_risk.value,
            "territory_pattern":                 self.territory_pattern.value,
            "territory_severity":                self.territory_severity.value,
            "recommended_action":                self.recommended_action.value,
            "load_score":                        self.load_score,
            "coverage_score":                    self.coverage_score,
            "penetration_score":                 self.penetration_score,
            "efficiency_score":                  self.efficiency_score,
            "territory_composite":               self.territory_composite,
            "has_territory_gap":                 self.has_territory_gap,
            "requires_territory_intervention":   self.requires_territory_intervention,
            "estimated_uncaptured_revenue_usd":  self.estimated_uncaptured_revenue_usd,
            "territory_signal":                  self.territory_signal,
        }


class SalesTerritoryImbalanceCoverageGapEngine:
    """Detects territory imbalance before it kills quota attainment across the team."""

    def __init__(self) -> None:
        self._results: List[TerritoryResult] = []

    # ── sub-scores ─────────────────────────────────────────────────────────────

    def _load_score(self, inp: TerritoryInput) -> float:
        s = 0.0
        if   inp.territory_quota_vs_capacity_ratio >= 1.60: s += 40
        elif inp.territory_quota_vs_capacity_ratio >= 1.30: s += 22
        elif inp.territory_quota_vs_capacity_ratio >= 1.10: s += 8
        if   inp.accounts_per_rep_vs_benchmark     >= 1.80: s += 35
        elif inp.accounts_per_rep_vs_benchmark     >= 1.40: s += 18
        if   inp.avg_travel_time_per_call_hours    >= 3.0:  s += 25
        elif inp.avg_travel_time_per_call_hours    >= 1.5:  s += 12
        return min(s, 100.0)

    def _coverage_score(self, inp: TerritoryInput) -> float:
        s = 0.0
        if   inp.active_accounts_pct           <= 0.30: s += 45
        elif inp.active_accounts_pct           <= 0.55: s += 25
        elif inp.active_accounts_pct           <= 0.75: s += 10
        if   inp.stale_account_rate_pct        >= 0.50: s += 30
        elif inp.stale_account_rate_pct        >= 0.28: s += 15
        if   inp.renewal_coverage_rate_pct     <= 0.50: s += 25
        elif inp.renewal_coverage_rate_pct     <= 0.75: s += 12
        return min(s, 100.0)

    def _penetration_score(self, inp: TerritoryInput) -> float:
        s = 0.0
        if   inp.whitespace_accounts_untouched_pct >= 0.65: s += 40
        elif inp.whitespace_accounts_untouched_pct >= 0.40: s += 22
        elif inp.whitespace_accounts_untouched_pct >= 0.20: s += 8
        if   inp.icp_account_coverage_pct          <= 0.25: s += 35
        elif inp.icp_account_coverage_pct          <= 0.50: s += 18
        if   inp.new_logo_territory_penetration_pct <= 0.10: s += 25
        elif inp.new_logo_territory_penetration_pct <= 0.20: s += 12
        return min(s, 100.0)

    def _efficiency_score(self, inp: TerritoryInput) -> float:
        s = 0.0
        if   inp.revenue_per_account_vs_benchmark   <= 0.40: s += 45
        elif inp.revenue_per_account_vs_benchmark   <= 0.70: s += 25
        elif inp.revenue_per_account_vs_benchmark   <= 0.90: s += 10
        if   inp.expansion_opportunity_capture_pct  <= 0.20: s += 30
        elif inp.expansion_opportunity_capture_pct  <= 0.45: s += 15
        if   inp.account_scoring_adoption_rate_pct  <= 0.20: s += 25
        elif inp.account_scoring_adoption_rate_pct  <= 0.50: s += 12
        return min(s, 100.0)

    # ── composite ──────────────────────────────────────────────────────────────

    def _composite(self, lo: float, co: float, pe: float, ef: float) -> float:
        return min(round(lo * 0.25 + co * 0.30 + pe * 0.25 + ef * 0.20, 2), 100.0)

    # ── pattern ────────────────────────────────────────────────────────────────

    def _pattern(self, inp: TerritoryInput) -> TerritoryPattern:
        if inp.territory_quota_vs_capacity_ratio >= 1.50 and inp.accounts_per_rep_vs_benchmark >= 1.60:
            return TerritoryPattern.overloaded_rep
        if inp.accounts_per_rep_vs_benchmark <= 0.50 and inp.whitespace_accounts_untouched_pct >= 0.60:
            return TerritoryPattern.starved_territory
        if inp.whitespace_accounts_untouched_pct >= 0.65 and inp.icp_account_coverage_pct <= 0.25:
            return TerritoryPattern.whitespace_blind
        if inp.active_accounts_pct <= 0.30 and inp.stale_account_rate_pct >= 0.50:
            return TerritoryPattern.coverage_ghost
        if inp.renewal_coverage_rate_pct <= 0.45 and inp.expansion_opportunity_capture_pct <= 0.20:
            return TerritoryPattern.renewal_neglect
        return TerritoryPattern.none

    # ── thresholds ─────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> TerritoryRisk:
        if   composite >= 60: return TerritoryRisk.critical
        elif composite >= 40: return TerritoryRisk.high
        elif composite >= 20: return TerritoryRisk.moderate
        return TerritoryRisk.low

    def _severity(self, composite: float) -> TerritorySeverity:
        if   composite >= 60: return TerritorySeverity.critical
        elif composite >= 40: return TerritorySeverity.imbalanced
        elif composite >= 20: return TerritorySeverity.drifting
        return TerritorySeverity.balanced

    def _action(self, risk: TerritoryRisk, pattern: TerritoryPattern) -> TerritoryAction:
        if risk == TerritoryRisk.critical:
            if pattern in (TerritoryPattern.overloaded_rep, TerritoryPattern.starved_territory):
                return TerritoryAction.territory_redesign_escalation
            return TerritoryAction.account_redistribution_review
        if risk == TerritoryRisk.high:
            if pattern == TerritoryPattern.overloaded_rep:
                return TerritoryAction.account_redistribution_review
            if pattern == TerritoryPattern.starved_territory:
                return TerritoryAction.coverage_model_reassignment
            if pattern == TerritoryPattern.whitespace_blind:
                return TerritoryAction.whitespace_activation_plan
            if pattern == TerritoryPattern.coverage_ghost:
                return TerritoryAction.account_redistribution_review
            if pattern == TerritoryPattern.renewal_neglect:
                return TerritoryAction.renewal_coverage_remediation
            return TerritoryAction.territory_health_check
        if risk == TerritoryRisk.moderate:
            return TerritoryAction.territory_health_check
        return TerritoryAction.no_action

    # ── flags ──────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: TerritoryInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.active_accounts_pct              <= 0.55
            or inp.whitespace_accounts_untouched_pct >= 0.40
        )

    def _requires_intervention(self, inp: TerritoryInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.renewal_coverage_rate_pct <= 0.75
            or inp.stale_account_rate_pct    >= 0.28
        )

    # ── uncaptured revenue ─────────────────────────────────────────────────────

    def _uncaptured_revenue(self, inp: TerritoryInput, composite: float) -> float:
        untouched_accounts = inp.total_accounts_in_territory * inp.whitespace_accounts_untouched_pct
        return round(untouched_accounts * inp.avg_arr_per_account_usd * (composite / 100), 2)

    # ── signal ─────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        TerritoryPattern.overloaded_rep:    "Overloaded rep",
        TerritoryPattern.starved_territory: "Starved territory",
        TerritoryPattern.whitespace_blind:  "Whitespace blind",
        TerritoryPattern.coverage_ghost:    "Coverage ghost",
        TerritoryPattern.renewal_neglect:   "Renewal neglect",
    }

    def _signal(self, inp: TerritoryInput, pattern: TerritoryPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Territory balance healthy — coverage, penetration, load, "
                "and efficiency within benchmark targets"
            )
        label     = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        act_pct   = round(inp.active_accounts_pct * 100)
        white_pct = round(inp.whitespace_accounts_untouched_pct * 100)
        renew_pct = round(inp.renewal_coverage_rate_pct * 100)
        comp_int  = round(composite)
        return (
            f"{label} — {act_pct}% accounts active — {white_pct}% whitespace untouched — "
            f"{renew_pct}% renewal coverage — composite {comp_int}"
        )

    # ── public API ─────────────────────────────────────────────────────────────

    def assess(self, inp: TerritoryInput) -> TerritoryResult:
        lo   = self._load_score(inp)
        co   = self._coverage_score(inp)
        pe   = self._penetration_score(inp)
        ef   = self._efficiency_score(inp)
        comp = self._composite(lo, co, pe, ef)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = TerritoryResult(
            rep_id                          = inp.rep_id,
            region                          = inp.region,
            territory_risk                  = risk,
            territory_pattern               = pattern,
            territory_severity              = severity,
            recommended_action              = action,
            load_score                      = lo,
            coverage_score                  = co,
            penetration_score               = pe,
            efficiency_score                = ef,
            territory_composite             = comp,
            has_territory_gap               = self._has_gap(inp, comp),
            requires_territory_intervention = self._requires_intervention(inp, comp),
            estimated_uncaptured_revenue_usd = self._uncaptured_revenue(inp, comp),
            territory_signal                = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[TerritoryInput]) -> List[TerritoryResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_territory_composite": 0.0,
                "territory_gap_count": 0,
                "intervention_count": 0,
                "avg_load_score": 0.0,
                "avg_coverage_score": 0.0,
                "avg_penetration_score": 0.0,
                "avg_efficiency_score": 0.0,
                "total_estimated_uncaptured_revenue_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_lo = total_co = total_pe = total_ef = total_ur = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.territory_risk.value]         = risk_counts.get(res.territory_risk.value, 0) + 1
            pattern_counts[res.territory_pattern.value]   = pattern_counts.get(res.territory_pattern.value, 0) + 1
            severity_counts[res.territory_severity.value] = severity_counts.get(res.territory_severity.value, 0) + 1
            action_counts[res.recommended_action.value]   = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.territory_composite
            total_lo   += res.load_score
            total_co   += res.coverage_score
            total_pe   += res.penetration_score
            total_ef   += res.efficiency_score
            total_ur   += res.estimated_uncaptured_revenue_usd
            if res.has_territory_gap:               gap_count          += 1
            if res.requires_territory_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_territory_composite":                  round(total_comp / n, 1),
            "territory_gap_count":                      gap_count,
            "intervention_count":                       intervention_count,
            "avg_load_score":                           round(total_lo / n, 1),
            "avg_coverage_score":                       round(total_co / n, 1),
            "avg_penetration_score":                    round(total_pe / n, 1),
            "avg_efficiency_score":                     round(total_ef / n, 1),
            "total_estimated_uncaptured_revenue_usd":   round(total_ur, 2),
        }
