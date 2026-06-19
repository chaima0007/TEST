"""
Module 229 — Innovation Scout Engine
Detects missed-opportunity risk across domains by scanning technology adoption
lags, competitive disruption signals, market whitespace gaps, talent shifts
and regulatory tailwinds — then recommends the right innovation response.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class InnovationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class InnovationPattern(str, Enum):
    none                    = "none"
    emerging_technology     = "emerging_technology"
    competitive_disruption  = "competitive_disruption"
    market_whitespace       = "market_whitespace"
    talent_shift            = "talent_shift"
    regulatory_opportunity  = "regulatory_opportunity"


class InnovationSeverity(str, Enum):
    ahead        = "ahead"
    monitoring   = "monitoring"
    lagging      = "lagging"
    critical_gap = "critical_gap"


class InnovationAction(str, Enum):
    no_action                     = "no_action"
    trend_monitoring              = "trend_monitoring"
    technology_pilot              = "technology_pilot"
    competitive_response          = "competitive_response"
    market_entry_analysis         = "market_entry_analysis"
    talent_acquisition_strategy   = "talent_acquisition_strategy"
    regulatory_positioning        = "regulatory_positioning"
    innovation_sprint             = "innovation_sprint"
    executive_innovation_briefing = "executive_innovation_briefing"


@dataclass
class InnovationInput:
    signal_id: str
    domain: str
    region: str
    technology_adoption_lag_months: float        # months behind leading edge
    competitor_innovation_velocity_score: float  # 0-1
    patent_filing_trend_pct: float               # % change in patent filings
    market_whitespace_score: float               # 0-1 (1 = large gap)
    customer_demand_signal_score: float          # 0-1
    talent_availability_score: float             # 0-1 (1 = available)
    regulatory_tailwind_score: float             # 0-1 (1 = favorable)
    startup_activity_score: float                # 0-1
    vc_investment_growth_pct: float              # % growth in VC investment
    technology_readiness_level: int              # 1-9
    cross_industry_adoption_pct: float           # 0-1
    internal_capability_gap_score: float         # 0-1
    pilot_success_rate_pct: float                # 0-1
    time_to_market_advantage_months: float       # months of advantage possible
    first_mover_window_months: float             # months before window closes
    strategic_fit_score: float                   # 0-1
    disruption_probability_score: float          # 0-1


@dataclass
class InnovationResult:
    signal_id: str
    region: str
    innovation_risk: str
    innovation_pattern: str
    innovation_severity: str
    recommended_action: str
    opportunity_score: float
    market_score: float
    capability_score: float
    timing_score: float
    innovation_composite: float
    has_opportunity_signal: bool
    requires_executive_attention: bool
    estimated_opportunity_value_index: float
    innovation_signal: str

    def to_dict(self) -> Dict:
        return {
            "signal_id":                          self.signal_id,
            "region":                             self.region,
            "innovation_risk":                    self.innovation_risk,
            "innovation_pattern":                 self.innovation_pattern,
            "innovation_severity":                self.innovation_severity,
            "recommended_action":                 self.recommended_action,
            "opportunity_score":                  self.opportunity_score,
            "market_score":                       self.market_score,
            "capability_score":                   self.capability_score,
            "timing_score":                       self.timing_score,
            "innovation_composite":               self.innovation_composite,
            "has_opportunity_signal":             self.has_opportunity_signal,
            "requires_executive_attention":       self.requires_executive_attention,
            "estimated_opportunity_value_index":  self.estimated_opportunity_value_index,
            "innovation_signal":                  self.innovation_signal,
        }


class InnovationScoutEngine:
    def __init__(self) -> None:
        self._results: List[InnovationResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _opportunity_score(self, i: InnovationInput) -> float:
        s = 0
        if   i.market_whitespace_score >= 0.75: s += 40
        elif i.market_whitespace_score >= 0.50: s += 22
        elif i.market_whitespace_score >= 0.25: s += 8

        if   i.customer_demand_signal_score >= 0.75: s += 35
        elif i.customer_demand_signal_score >= 0.50: s += 18
        elif i.customer_demand_signal_score >= 0.25: s += 6

        if   i.disruption_probability_score >= 0.70: s += 25
        elif i.disruption_probability_score >= 0.45: s += 12
        return min(s, 100)

    def _market_score(self, i: InnovationInput) -> float:
        s = 0
        if   i.competitor_innovation_velocity_score >= 0.80: s += 40
        elif i.competitor_innovation_velocity_score >= 0.60: s += 22
        elif i.competitor_innovation_velocity_score >= 0.35: s += 8

        if   i.startup_activity_score >= 0.75: s += 35
        elif i.startup_activity_score >= 0.50: s += 18

        if   i.vc_investment_growth_pct >= 0.50: s += 25
        elif i.vc_investment_growth_pct >= 0.25: s += 12
        return min(s, 100)

    def _capability_score(self, i: InnovationInput) -> float:
        s = 0
        if   i.internal_capability_gap_score >= 0.70: s += 45
        elif i.internal_capability_gap_score >= 0.45: s += 25
        elif i.internal_capability_gap_score >= 0.20: s += 10

        if   i.technology_readiness_level <= 3: s += 30
        elif i.technology_readiness_level <= 5: s += 15

        if   i.talent_availability_score <= 0.35: s += 25
        elif i.talent_availability_score <= 0.60: s += 12
        return min(s, 100)

    def _timing_score(self, i: InnovationInput) -> float:
        s = 0
        if   i.first_mover_window_months <= 6:  s += 40
        elif i.first_mover_window_months <= 12: s += 22
        elif i.first_mover_window_months <= 24: s += 8

        if   i.technology_adoption_lag_months >= 18: s += 35
        elif i.technology_adoption_lag_months >= 9:  s += 18
        elif i.technology_adoption_lag_months >= 3:  s += 6

        if   i.time_to_market_advantage_months >= 12: s += 25
        elif i.time_to_market_advantage_months >= 6:  s += 12
        return min(s, 100)

    def _composite(self, opp: float, mkt: float, cap: float, tim: float) -> float:
        return min(round(opp * 0.30 + mkt * 0.25 + cap * 0.25 + tim * 0.20, 2), 100.0)

    def _risk(self, c: float) -> InnovationRisk:
        if c >= 60: return InnovationRisk.critical
        if c >= 40: return InnovationRisk.high
        if c >= 20: return InnovationRisk.moderate
        return InnovationRisk.low

    def _severity(self, c: float) -> InnovationSeverity:
        if c >= 60: return InnovationSeverity.critical_gap
        if c >= 40: return InnovationSeverity.lagging
        if c >= 20: return InnovationSeverity.monitoring
        return InnovationSeverity.ahead

    def _pattern(self, i: InnovationInput) -> InnovationPattern:
        if (i.technology_readiness_level <= 4
                and i.cross_industry_adoption_pct >= 0.30):
            return InnovationPattern.emerging_technology
        if (i.competitor_innovation_velocity_score >= 0.75
                and i.disruption_probability_score >= 0.60):
            return InnovationPattern.competitive_disruption
        if (i.market_whitespace_score >= 0.65
                and i.customer_demand_signal_score >= 0.60):
            return InnovationPattern.market_whitespace
        if (i.talent_availability_score <= 0.35
                and i.startup_activity_score >= 0.60):
            return InnovationPattern.talent_shift
        if (i.regulatory_tailwind_score >= 0.65
                and i.strategic_fit_score >= 0.60):
            return InnovationPattern.regulatory_opportunity
        return InnovationPattern.none

    def _action(
        self, risk: InnovationRisk, pat: InnovationPattern
    ) -> InnovationAction:
        if risk == InnovationRisk.critical:
            if pat in (InnovationPattern.emerging_technology,
                       InnovationPattern.competitive_disruption):
                return InnovationAction.innovation_sprint
            return InnovationAction.executive_innovation_briefing
        if risk == InnovationRisk.high:
            if pat == InnovationPattern.emerging_technology:
                return InnovationAction.technology_pilot
            if pat == InnovationPattern.competitive_disruption:
                return InnovationAction.competitive_response
            if pat == InnovationPattern.market_whitespace:
                return InnovationAction.market_entry_analysis
            if pat == InnovationPattern.talent_shift:
                return InnovationAction.talent_acquisition_strategy
            if pat == InnovationPattern.regulatory_opportunity:
                return InnovationAction.regulatory_positioning
            return InnovationAction.trend_monitoring
        if risk == InnovationRisk.moderate:
            return InnovationAction.trend_monitoring
        return InnovationAction.no_action

    def _signal(self, i: InnovationInput, pat: InnovationPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Innovation landscape stable — no critical gaps or missed "
                "opportunities identified"
            )
        labels = {
            InnovationPattern.emerging_technology:    "Emerging technology signal",
            InnovationPattern.competitive_disruption: "Competitive disruption detected",
            InnovationPattern.market_whitespace:      "Market whitespace opportunity",
            InnovationPattern.talent_shift:           "Talent shift underway",
            InnovationPattern.regulatory_opportunity: "Regulatory tailwind identified",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — "
            f"{round(i.market_whitespace_score * 100)}% market whitespace — "
            f"{round(i.disruption_probability_score * 100)}% disruption prob — "
            f"{round(i.first_mover_window_months)}mo window — "
            f"composite {round(comp)}"
        )

    def _has_opportunity_signal(self, i: InnovationInput, comp: float) -> bool:
        return (
            comp >= 40
            or i.market_whitespace_score >= 0.50
            or i.disruption_probability_score >= 0.45
        )

    def _requires_executive_attention(self, i: InnovationInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.competitor_innovation_velocity_score >= 0.65
            or i.first_mover_window_months <= 12
        )

    def _opportunity_value_index(self, i: InnovationInput, comp: float) -> float:
        return round(min(comp / 100 * i.strategic_fit_score * 10, 10.0), 2)

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, i: InnovationInput) -> InnovationResult:
        opp  = self._opportunity_score(i)
        mkt  = self._market_score(i)
        cap  = self._capability_score(i)
        tim  = self._timing_score(i)
        comp = self._composite(opp, mkt, cap, tim)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = InnovationResult(
            signal_id=i.signal_id,
            region=i.region,
            innovation_risk=risk.value,
            innovation_pattern=pat.value,
            innovation_severity=sev.value,
            recommended_action=act.value,
            opportunity_score=opp,
            market_score=mkt,
            capability_score=cap,
            timing_score=tim,
            innovation_composite=comp,
            has_opportunity_signal=self._has_opportunity_signal(i, comp),
            requires_executive_attention=self._requires_executive_attention(i, comp),
            estimated_opportunity_value_index=self._opportunity_value_index(i, comp),
            innovation_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[InnovationInput]) -> List[InnovationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_innovation_composite": 0.0,
                "opportunity_signal_count": 0,
                "executive_attention_count": 0,
                "avg_opportunity_score": 0.0,
                "avg_market_score": 0.0,
                "avg_capability_score": 0.0,
                "avg_timing_score": 0.0,
                "avg_estimated_opportunity_value_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        topp = tmkt = tcap = ttim = tcomp = tval = 0.0
        osc = eac = 0
        for r in self._results:
            rc[r.innovation_risk]      = rc.get(r.innovation_risk, 0)      + 1
            pc[r.innovation_pattern]   = pc.get(r.innovation_pattern, 0)   + 1
            sc[r.innovation_severity]  = sc.get(r.innovation_severity, 0)  + 1
            ac[r.recommended_action]   = ac.get(r.recommended_action, 0)   + 1
            topp  += r.opportunity_score
            tmkt  += r.market_score
            tcap  += r.capability_score
            ttim  += r.timing_score
            tcomp += r.innovation_composite
            tval  += r.estimated_opportunity_value_index
            if r.has_opportunity_signal:       osc += 1
            if r.requires_executive_attention: eac += 1
        return {
            "total":                                  n,
            "risk_counts":                            rc,
            "pattern_counts":                         pc,
            "severity_counts":                        sc,
            "action_counts":                          ac,
            "avg_innovation_composite":               round(tcomp / n, 1),
            "opportunity_signal_count":               osc,
            "executive_attention_count":              eac,
            "avg_opportunity_score":                  round(topp / n, 1),
            "avg_market_score":                       round(tmkt / n, 1),
            "avg_capability_score":                   round(tcap / n, 1),
            "avg_timing_score":                       round(ttim / n, 1),
            "avg_estimated_opportunity_value_index":  round(tval / n, 2),
        }
