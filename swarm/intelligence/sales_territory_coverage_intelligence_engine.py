from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class CoverageRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CoveragePattern(str, Enum):
    none                = "none"
    whitespace_neglect  = "whitespace_neglect"
    density_imbalance   = "density_imbalance"
    travel_inefficiency = "travel_inefficiency"
    vertical_blind_spot = "vertical_blind_spot"
    renewal_anchoring   = "renewal_anchoring"


class CoverageSeverity(str, Enum):
    optimal    = "optimal"
    adequate   = "adequate"
    underserved = "underserved"
    neglected  = "neglected"


class CoverageAction(str, Enum):
    no_action                       = "no_action"
    territory_monitoring            = "territory_monitoring"
    whitespace_prospecting_coaching = "whitespace_prospecting_coaching"
    route_optimization_coaching     = "route_optimization_coaching"
    vertical_expansion_coaching     = "vertical_expansion_coaching"
    territory_rebalancing           = "territory_rebalancing"
    territory_strategy_reset        = "territory_strategy_reset"


@dataclass
class TerritoryCoverageInput:
    rep_id:                         str
    region:                         str
    evaluation_period_id:           str
    accounts_touched_pct:           float   # 0-1 (pct of assigned accounts touched)
    whitespace_accounts_touched_pct:float   # 0-1
    new_logo_attempts_per_month:    float   # count
    avg_accounts_per_week:          float   # unique accounts touched
    vertical_coverage_pct:          float   # 0-1 (industries covered vs available)
    geographic_concentration_pct:   float   # 0-1 (1.0 = all activity one city)
    travel_time_pct_of_selling:     float   # 0-1
    repeat_visit_rate_pct:          float   # 0-1
    inactive_account_pct:           float   # 0-1 (accounts not touched in 60d)
    expansion_account_pct:          float   # 0-1
    at_risk_account_pct:            float   # 0-1 (by health score)
    high_potential_untouched_pct:   float   # 0-1
    avg_touch_frequency_days:       float   # days between touches per account
    segmentation_adherence_pct:     float   # 0-1
    icp_alignment_pct:              float   # 0-1
    conquest_account_coverage_pct:  float   # 0-1
    total_assigned_accounts:        int
    total_territory_arr_usd:        float
    avg_account_arr_usd:            float


@dataclass
class TerritoryCoverageResult:
    rep_id:                         str
    region:                         str
    territory_risk:                 CoverageRisk
    territory_pattern:              CoveragePattern
    territory_severity:             CoverageSeverity
    recommended_action:             CoverageAction
    coverage_score:                 float
    prospecting_score:              float
    efficiency_score:               float
    segmentation_score:             float
    territory_composite:            float
    has_territory_gap:              bool
    requires_territory_coaching:    bool
    estimated_missed_revenue_usd:   float
    territory_signal:               str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "territory_risk":                   self.territory_risk.value,
            "territory_pattern":                self.territory_pattern.value,
            "territory_severity":               self.territory_severity.value,
            "recommended_action":               self.recommended_action.value,
            "coverage_score":                   self.coverage_score,
            "prospecting_score":                self.prospecting_score,
            "efficiency_score":                 self.efficiency_score,
            "segmentation_score":               self.segmentation_score,
            "territory_composite":              self.territory_composite,
            "has_territory_gap":                self.has_territory_gap,
            "requires_territory_coaching":      self.requires_territory_coaching,
            "estimated_missed_revenue_usd":     self.estimated_missed_revenue_usd,
            "territory_signal":                 self.territory_signal,
        }


class SalesTerritoryCoverageIntelligenceEngine:
    """Detects territory gaps — whitespace neglect, density imbalance, travel inefficiency, vertical blind spots."""

    def __init__(self) -> None:
        self._results: List[TerritoryCoverageResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _coverage_score(self, inp: TerritoryCoverageInput) -> float:
        s = 0.0
        if   inp.accounts_touched_pct        <= 0.40: s += 40
        elif inp.accounts_touched_pct        <= 0.60: s += 22
        elif inp.accounts_touched_pct        <= 0.75: s += 8
        if   inp.inactive_account_pct        >= 0.40: s += 35
        elif inp.inactive_account_pct        >= 0.25: s += 18
        if   inp.high_potential_untouched_pct >= 0.40: s += 25
        elif inp.high_potential_untouched_pct >= 0.25: s += 12
        return min(s, 100.0)

    def _prospecting_score(self, inp: TerritoryCoverageInput) -> float:
        s = 0.0
        if   inp.whitespace_accounts_touched_pct <= 0.15: s += 40
        elif inp.whitespace_accounts_touched_pct <= 0.35: s += 22
        elif inp.whitespace_accounts_touched_pct <= 0.55: s += 8
        if   inp.new_logo_attempts_per_month     <= 3:    s += 35
        elif inp.new_logo_attempts_per_month     <= 6:    s += 18
        if   inp.conquest_account_coverage_pct   <= 0.20: s += 25
        elif inp.conquest_account_coverage_pct   <= 0.40: s += 12
        return min(s, 100.0)

    def _efficiency_score(self, inp: TerritoryCoverageInput) -> float:
        s = 0.0
        if   inp.travel_time_pct_of_selling  >= 0.35: s += 40
        elif inp.travel_time_pct_of_selling  >= 0.25: s += 22
        elif inp.travel_time_pct_of_selling  >= 0.15: s += 8
        if   inp.repeat_visit_rate_pct       >= 0.60: s += 35
        elif inp.repeat_visit_rate_pct       >= 0.45: s += 18
        if   inp.geographic_concentration_pct >= 0.70: s += 25
        elif inp.geographic_concentration_pct >= 0.55: s += 12
        return min(s, 100.0)

    def _segmentation_score(self, inp: TerritoryCoverageInput) -> float:
        s = 0.0
        if   inp.segmentation_adherence_pct  <= 0.40: s += 45
        elif inp.segmentation_adherence_pct  <= 0.60: s += 25
        elif inp.segmentation_adherence_pct  <= 0.75: s += 10
        if   inp.icp_alignment_pct           <= 0.40: s += 30
        elif inp.icp_alignment_pct           <= 0.65: s += 15
        if   inp.vertical_coverage_pct       <= 0.30: s += 25
        elif inp.vertical_coverage_pct       <= 0.55: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, co: float, pr: float, ef: float, se: float) -> float:
        return min(round(co * 0.35 + pr * 0.25 + ef * 0.20 + se * 0.20, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: TerritoryCoverageInput) -> CoveragePattern:
        if inp.whitespace_accounts_touched_pct <= 0.15 and inp.high_potential_untouched_pct >= 0.35:
            return CoveragePattern.whitespace_neglect
        if inp.geographic_concentration_pct >= 0.65 and inp.inactive_account_pct >= 0.35:
            return CoveragePattern.density_imbalance
        if inp.travel_time_pct_of_selling >= 0.30 and inp.repeat_visit_rate_pct >= 0.55:
            return CoveragePattern.travel_inefficiency
        if inp.vertical_coverage_pct <= 0.30 and inp.icp_alignment_pct <= 0.50:
            return CoveragePattern.vertical_blind_spot
        if inp.repeat_visit_rate_pct >= 0.60 and inp.new_logo_attempts_per_month <= 3:
            return CoveragePattern.renewal_anchoring
        return CoveragePattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> CoverageRisk:
        if   composite >= 60: return CoverageRisk.critical
        elif composite >= 40: return CoverageRisk.high
        elif composite >= 20: return CoverageRisk.moderate
        return CoverageRisk.low

    def _severity(self, composite: float) -> CoverageSeverity:
        if   composite >= 60: return CoverageSeverity.neglected
        elif composite >= 40: return CoverageSeverity.underserved
        elif composite >= 20: return CoverageSeverity.adequate
        return CoverageSeverity.optimal

    def _action(self, risk: CoverageRisk, pattern: CoveragePattern) -> CoverageAction:
        if risk == CoverageRisk.critical:
            if pattern == CoveragePattern.whitespace_neglect:
                return CoverageAction.territory_strategy_reset
            return CoverageAction.territory_rebalancing
        if risk == CoverageRisk.high:
            if pattern == CoveragePattern.whitespace_neglect:
                return CoverageAction.whitespace_prospecting_coaching
            if pattern == CoveragePattern.density_imbalance:
                return CoverageAction.territory_rebalancing
            if pattern == CoveragePattern.travel_inefficiency:
                return CoverageAction.route_optimization_coaching
            if pattern == CoveragePattern.vertical_blind_spot:
                return CoverageAction.vertical_expansion_coaching
            if pattern == CoveragePattern.renewal_anchoring:
                return CoverageAction.whitespace_prospecting_coaching
            return CoverageAction.territory_rebalancing
        if risk == CoverageRisk.moderate:
            return CoverageAction.territory_monitoring
        return CoverageAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: TerritoryCoverageInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.accounts_touched_pct          <= 0.60
            or inp.high_potential_untouched_pct  >= 0.30
        )

    def _requires_coaching(self, inp: TerritoryCoverageInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.whitespace_accounts_touched_pct <= 0.40
            or inp.segmentation_adherence_pct      <= 0.60
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _missed_revenue(self, inp: TerritoryCoverageInput, composite: float) -> float:
        untouched_pct = max(0.0, 1.0 - inp.accounts_touched_pct)
        return round(
            inp.total_territory_arr_usd
            * untouched_pct
            * (composite / 100),
            2,
        )

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        CoveragePattern.whitespace_neglect:  "Whitespace neglect",
        CoveragePattern.density_imbalance:   "Density imbalance",
        CoveragePattern.travel_inefficiency: "Travel inefficiency",
        CoveragePattern.vertical_blind_spot: "Vertical blind spot",
        CoveragePattern.renewal_anchoring:   "Renewal anchoring",
    }

    def _signal(self, inp: TerritoryCoverageInput, pattern: CoveragePattern, composite: float) -> str:
        if composite < 20:
            return (
                "Territory coverage optimal — accounts touched, whitespace prospecting, "
                "travel efficiency, and segmentation within benchmarks"
            )
        label       = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        touch_pct   = round(inp.accounts_touched_pct * 100)
        ws_pct      = round(inp.whitespace_accounts_touched_pct * 100)
        inact_pct   = round(inp.inactive_account_pct * 100)
        comp_int    = round(composite)
        return (
            f"{label} — {touch_pct}% accounts touched — "
            f"{ws_pct}% whitespace coverage — "
            f"{inact_pct}% inactive accounts — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: TerritoryCoverageInput) -> TerritoryCoverageResult:
        co  = self._coverage_score(inp)
        pr  = self._prospecting_score(inp)
        ef  = self._efficiency_score(inp)
        se  = self._segmentation_score(inp)
        comp = self._composite(co, pr, ef, se)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = TerritoryCoverageResult(
            rep_id                      = inp.rep_id,
            region                      = inp.region,
            territory_risk              = risk,
            territory_pattern           = pattern,
            territory_severity          = severity,
            recommended_action          = action,
            coverage_score              = co,
            prospecting_score           = pr,
            efficiency_score            = ef,
            segmentation_score          = se,
            territory_composite         = comp,
            has_territory_gap           = self._has_gap(inp, comp),
            requires_territory_coaching = self._requires_coaching(inp, comp),
            estimated_missed_revenue_usd= self._missed_revenue(inp, comp),
            territory_signal            = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[TerritoryCoverageInput]) -> List[TerritoryCoverageResult]:
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
                "coaching_count": 0,
                "avg_coverage_score": 0.0,
                "avg_prospecting_score": 0.0,
                "avg_efficiency_score": 0.0,
                "avg_segmentation_score": 0.0,
                "total_estimated_missed_revenue_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_co = total_pr = total_ef = total_se = total_mr = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.territory_risk.value]       = risk_counts.get(res.territory_risk.value, 0) + 1
            pattern_counts[res.territory_pattern.value] = pattern_counts.get(res.territory_pattern.value, 0) + 1
            severity_counts[res.territory_severity.value] = severity_counts.get(res.territory_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.territory_composite
            total_co   += res.coverage_score
            total_pr   += res.prospecting_score
            total_ef   += res.efficiency_score
            total_se   += res.segmentation_score
            total_mr   += res.estimated_missed_revenue_usd
            if res.has_territory_gap:          gap_count      += 1
            if res.requires_territory_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_territory_composite":              round(total_comp / n, 1),
            "territory_gap_count":                  gap_count,
            "coaching_count":                       coaching_count,
            "avg_coverage_score":                   round(total_co / n, 1),
            "avg_prospecting_score":                round(total_pr / n, 1),
            "avg_efficiency_score":                 round(total_ef / n, 1),
            "avg_segmentation_score":               round(total_se / n, 1),
            "total_estimated_missed_revenue_usd":   round(total_mr, 2),
        }
