"""
Module 212 — Sales Competitive Win/Loss Pattern Intelligence Engine
Detects patterns in competitive losses and win blind spots by rep.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class CompetitiveRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CompetitivePattern(str, Enum):
    none                     = "none"
    single_competitor_loser  = "single_competitor_loser"
    price_only_battle        = "price_only_battle"
    feature_gap_surrender    = "feature_gap_surrender"
    late_to_discover_comp    = "late_to_discover_comp"
    displacement_target      = "displacement_target"


class CompetitiveSeverity(str, Enum):
    dominant   = "dominant"
    competing  = "competing"
    slipping   = "slipping"
    losing     = "losing"


class CompetitiveAction(str, Enum):
    no_action                      = "no_action"
    competitive_monitoring         = "competitive_monitoring"
    differentiation_coaching       = "differentiation_coaching"
    battle_card_enforcement        = "battle_card_enforcement"
    discovery_depth_coaching       = "discovery_depth_coaching"
    pricing_strategy_coaching      = "pricing_strategy_coaching"
    competitive_deal_desk_support  = "competitive_deal_desk_support"
    win_loss_review_intervention   = "win_loss_review_intervention"
    competitive_strategy_reset     = "competitive_strategy_reset"


@dataclass
class CompetitiveInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    # Competitive exposure metrics
    competitive_deal_rate_pct: float          # % of deals with known competitor
    competitive_win_rate_pct: float           # win rate in competitive deals
    competitive_loss_rate_pct: float          # loss rate in competitive deals
    single_competitor_loss_concentration_pct: float  # % losses to one specific competitor
    # Discovery quality
    competitor_identified_late_rate_pct: float       # competitor discovered late in cycle
    battle_card_usage_rate_pct: float                # % competitive deals using battle cards
    competitive_discovery_score: float               # 0-1 quality of comp discovery
    # Positioning quality
    price_cited_as_loss_reason_pct: float            # % losses where price was cited
    feature_gap_cited_as_loss_reason_pct: float      # % losses citing feature gaps
    value_differentiation_score: float               # 0-1 rep's ability to differentiate
    # Deal conversion in comp context
    competitive_pipeline_conversion_rate_pct: float  # pipeline→close in competitive deals
    displacement_deal_win_rate_pct: float            # win rate when displacing incumbent
    incumbent_defense_win_rate_pct: float            # win rate when defending vs challenger
    multi_competitor_deal_rate_pct: float            # % deals with 3+ competitors
    # Intelligence and preparation
    competitive_intelligence_recency_score: float    # 0-1 how fresh comp intel is
    proof_of_concept_win_rate_pct: float             # win rate after POC/pilot
    executive_alignment_in_comp_deals_pct: float     # exec alignment in competitive deals
    # Volume
    total_competitive_deals: int
    avg_deal_value_usd: float


@dataclass
class CompetitiveResult:
    rep_id: str
    region: str
    competitive_risk: str
    competitive_pattern: str
    competitive_severity: str
    recommended_action: str
    exposure_score: float
    positioning_score: float
    intelligence_score: float
    conversion_score: float
    competitive_composite: float
    has_competitive_gap: bool
    requires_competitive_coaching: bool
    estimated_lost_revenue_usd: float
    competitive_signal: str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                     self.rep_id,
            "region":                     self.region,
            "competitive_risk":           self.competitive_risk,
            "competitive_pattern":        self.competitive_pattern,
            "competitive_severity":       self.competitive_severity,
            "recommended_action":         self.recommended_action,
            "exposure_score":             self.exposure_score,
            "positioning_score":          self.positioning_score,
            "intelligence_score":         self.intelligence_score,
            "conversion_score":           self.conversion_score,
            "competitive_composite":      self.competitive_composite,
            "has_competitive_gap":        self.has_competitive_gap,
            "requires_competitive_coaching": self.requires_competitive_coaching,
            "estimated_lost_revenue_usd": self.estimated_lost_revenue_usd,
            "competitive_signal":         self.competitive_signal,
        }


class SalesCompetitiveWinLossPatternEngine:
    def __init__(self) -> None:
        self._results: List[CompetitiveResult] = []

    # ── Sub-scores ────────────────────────────────────────────────────────────

    def _exposure_score(self, i: CompetitiveInput) -> float:
        """High exposure + concentrated losses = risk."""
        s = 0
        if   i.single_competitor_loss_concentration_pct >= 0.60: s += 40
        elif i.single_competitor_loss_concentration_pct >= 0.40: s += 22
        elif i.single_competitor_loss_concentration_pct >= 0.25: s += 8

        if   i.competitive_loss_rate_pct >= 0.65: s += 35
        elif i.competitive_loss_rate_pct >= 0.45: s += 18
        elif i.competitive_loss_rate_pct >= 0.30: s += 8

        if   i.multi_competitor_deal_rate_pct >= 0.50: s += 25
        elif i.multi_competitor_deal_rate_pct >= 0.30: s += 12
        return min(s, 100)

    def _positioning_score(self, i: CompetitiveInput) -> float:
        """Poor differentiation and feature gap reliance = risk."""
        s = 0
        if   i.value_differentiation_score    <= 0.20: s += 45
        elif i.value_differentiation_score    <= 0.45: s += 25
        elif i.value_differentiation_score    <= 0.65: s += 10

        if   i.price_cited_as_loss_reason_pct >= 0.55: s += 30
        elif i.price_cited_as_loss_reason_pct >= 0.35: s += 15

        if   i.feature_gap_cited_as_loss_reason_pct >= 0.45: s += 25
        elif i.feature_gap_cited_as_loss_reason_pct >= 0.28: s += 12
        return min(s, 100)

    def _intelligence_score(self, i: CompetitiveInput) -> float:
        """Late discovery, stale intel, low battle card use = risk."""
        s = 0
        if   i.competitor_identified_late_rate_pct >= 0.55: s += 40
        elif i.competitor_identified_late_rate_pct >= 0.35: s += 22
        elif i.competitor_identified_late_rate_pct >= 0.20: s += 8

        if   i.competitive_intelligence_recency_score <= 0.20: s += 35
        elif i.competitive_intelligence_recency_score <= 0.45: s += 18

        if   i.battle_card_usage_rate_pct <= 0.25: s += 25
        elif i.battle_card_usage_rate_pct <= 0.55: s += 12
        return min(s, 100)

    def _conversion_score(self, i: CompetitiveInput) -> float:
        """Low conversion and poor displacement rate = risk."""
        s = 0
        if   i.competitive_pipeline_conversion_rate_pct <= 0.15: s += 45
        elif i.competitive_pipeline_conversion_rate_pct <= 0.30: s += 25
        elif i.competitive_pipeline_conversion_rate_pct <= 0.45: s += 10

        if   i.displacement_deal_win_rate_pct <= 0.20: s += 30
        elif i.displacement_deal_win_rate_pct <= 0.40: s += 15

        if   i.executive_alignment_in_comp_deals_pct <= 0.25: s += 25
        elif i.executive_alignment_in_comp_deals_pct <= 0.50: s += 12
        return min(s, 100)

    # ── Composite ─────────────────────────────────────────────────────────────

    def _composite(self, ex: float, po: float, in_: float, co: float) -> float:
        return min(round(ex * 0.30 + po * 0.25 + in_ * 0.25 + co * 0.20, 2), 100.0)

    # ── Risk / Severity ───────────────────────────────────────────────────────

    def _risk(self, c: float) -> CompetitiveRisk:
        if c >= 60: return CompetitiveRisk.critical
        if c >= 40: return CompetitiveRisk.high
        if c >= 20: return CompetitiveRisk.moderate
        return CompetitiveRisk.low

    def _severity(self, c: float) -> CompetitiveSeverity:
        if c >= 60: return CompetitiveSeverity.losing
        if c >= 40: return CompetitiveSeverity.slipping
        if c >= 20: return CompetitiveSeverity.competing
        return CompetitiveSeverity.dominant

    # ── Pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, i: CompetitiveInput) -> CompetitivePattern:
        if (i.single_competitor_loss_concentration_pct >= 0.55
                and i.competitive_win_rate_pct <= 0.30):
            return CompetitivePattern.single_competitor_loser
        if (i.price_cited_as_loss_reason_pct >= 0.50
                and i.value_differentiation_score <= 0.30):
            return CompetitivePattern.price_only_battle
        if (i.feature_gap_cited_as_loss_reason_pct >= 0.40
                and i.competitive_discovery_score <= 0.40):
            return CompetitivePattern.feature_gap_surrender
        if (i.competitor_identified_late_rate_pct >= 0.50
                and i.battle_card_usage_rate_pct <= 0.30):
            return CompetitivePattern.late_to_discover_comp
        if (i.displacement_deal_win_rate_pct <= 0.15
                and i.incumbent_defense_win_rate_pct >= 0.65):
            return CompetitivePattern.displacement_target
        return CompetitivePattern.none

    # ── Action ────────────────────────────────────────────────────────────────

    def _action(self, risk: CompetitiveRisk, pat: CompetitivePattern) -> CompetitiveAction:
        if risk == CompetitiveRisk.critical:
            if pat in (CompetitivePattern.single_competitor_loser, CompetitivePattern.price_only_battle):
                return CompetitiveAction.competitive_strategy_reset
            return CompetitiveAction.win_loss_review_intervention
        if risk == CompetitiveRisk.high:
            if pat == CompetitivePattern.single_competitor_loser: return CompetitiveAction.battle_card_enforcement
            if pat == CompetitivePattern.price_only_battle:       return CompetitiveAction.pricing_strategy_coaching
            if pat == CompetitivePattern.feature_gap_surrender:   return CompetitiveAction.differentiation_coaching
            if pat == CompetitivePattern.late_to_discover_comp:   return CompetitiveAction.discovery_depth_coaching
            if pat == CompetitivePattern.displacement_target:     return CompetitiveAction.competitive_deal_desk_support
            return CompetitiveAction.competitive_monitoring
        if risk == CompetitiveRisk.moderate:
            return CompetitiveAction.competitive_monitoring
        return CompetitiveAction.no_action

    # ── Signal ────────────────────────────────────────────────────────────────

    def _signal(self, i: CompetitiveInput, pat: CompetitivePattern, comp: float) -> str:
        if comp < 20:
            return "Competitive performance strong — win rates, differentiation, and intel freshness within benchmark targets"
        labels = {
            CompetitivePattern.single_competitor_loser: "Single competitor loser",
            CompetitivePattern.price_only_battle:       "Price-only battle",
            CompetitivePattern.feature_gap_surrender:   "Feature gap surrender",
            CompetitivePattern.late_to_discover_comp:   "Late to discover competitor",
            CompetitivePattern.displacement_target:     "Displacement target",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {round(i.competitive_win_rate_pct*100)}% comp win rate — "
            f"{round(i.price_cited_as_loss_reason_pct*100)}% price cited as loss — "
            f"{round(i.competitor_identified_late_rate_pct*100)}% late discovery — "
            f"composite {round(comp)}"
        )

    # ── Flags ─────────────────────────────────────────────────────────────────

    def _has_competitive_gap(self, i: CompetitiveInput, comp: float) -> bool:
        return (comp >= 40
                or i.competitive_win_rate_pct <= 0.35
                or i.single_competitor_loss_concentration_pct >= 0.40)

    def _requires_coaching(self, i: CompetitiveInput, comp: float) -> bool:
        return (comp >= 25
                or i.battle_card_usage_rate_pct <= 0.40
                or i.value_differentiation_score <= 0.50)

    # ── Revenue at risk ───────────────────────────────────────────────────────

    def _lost_revenue(self, i: CompetitiveInput, comp: float) -> float:
        return round(
            i.total_competitive_deals
            * i.avg_deal_value_usd
            * i.competitive_loss_rate_pct
            * (comp / 100),
            2,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def assess(self, i: CompetitiveInput) -> CompetitiveResult:
        ex  = self._exposure_score(i)
        po  = self._positioning_score(i)
        in_ = self._intelligence_score(i)
        co  = self._conversion_score(i)
        comp = self._composite(ex, po, in_, co)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = CompetitiveResult(
            rep_id=i.rep_id,
            region=i.region,
            competitive_risk=risk.value,
            competitive_pattern=pat.value,
            competitive_severity=sev.value,
            recommended_action=act.value,
            exposure_score=ex,
            positioning_score=po,
            intelligence_score=in_,
            conversion_score=co,
            competitive_composite=comp,
            has_competitive_gap=self._has_competitive_gap(i, comp),
            requires_competitive_coaching=self._requires_coaching(i, comp),
            estimated_lost_revenue_usd=self._lost_revenue(i, comp),
            competitive_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[CompetitiveInput]) -> List[CompetitiveResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_competitive_composite": 0.0,
                "competitive_gap_count": 0,
                "coaching_count": 0,
                "avg_exposure_score": 0.0,
                "avg_positioning_score": 0.0,
                "avg_intelligence_score": 0.0,
                "avg_conversion_score": 0.0,
                "total_estimated_lost_revenue_usd": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tex = tpo = tin = tco = tcomp = tlr = 0.0
        gc = cc = 0
        for r in self._results:
            rc[r.competitive_risk]    = rc.get(r.competitive_risk, 0)    + 1
            pc[r.competitive_pattern] = pc.get(r.competitive_pattern, 0) + 1
            sc[r.competitive_severity]= sc.get(r.competitive_severity, 0)+ 1
            ac[r.recommended_action]  = ac.get(r.recommended_action, 0)  + 1
            tex  += r.exposure_score
            tpo  += r.positioning_score
            tin  += r.intelligence_score
            tco  += r.conversion_score
            tcomp += r.competitive_composite
            tlr  += r.estimated_lost_revenue_usd
            if r.has_competitive_gap:        gc += 1
            if r.requires_competitive_coaching: cc += 1
        return {
            "total":                           n,
            "risk_counts":                     rc,
            "pattern_counts":                  pc,
            "severity_counts":                 sc,
            "action_counts":                   ac,
            "avg_competitive_composite":       round(tcomp / n, 1),
            "competitive_gap_count":           gc,
            "coaching_count":                  cc,
            "avg_exposure_score":              round(tex / n, 1),
            "avg_positioning_score":           round(tpo / n, 1),
            "avg_intelligence_score":          round(tin / n, 1),
            "avg_conversion_score":            round(tco / n, 1),
            "total_estimated_lost_revenue_usd": round(tlr, 2),
        }
