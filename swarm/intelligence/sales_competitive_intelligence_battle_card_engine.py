from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class CompetitiveRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CompetitivePattern(str, Enum):
    none                 = "none"
    unprepared_seller    = "unprepared_seller"
    feature_fighter      = "feature_fighter"
    price_surrenderer    = "price_surrenderer"
    late_discovery       = "late_discovery"
    single_thread_loser  = "single_thread_loser"


class CompetitiveSeverity(str, Enum):
    dominant    = "dominant"
    competing   = "competing"
    struggling  = "struggling"
    losing      = "losing"


class CompetitiveAction(str, Enum):
    no_action                      = "no_action"
    competitive_awareness_coaching = "competitive_awareness_coaching"
    battle_card_refresh_coaching   = "battle_card_refresh_coaching"
    value_differentiation_coaching = "value_differentiation_coaching"
    multi_thread_coaching          = "multi_thread_coaching"
    competitive_deal_review        = "competitive_deal_review"
    executive_competitive_escalation = "executive_competitive_escalation"


@dataclass
class CompetitiveInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    competitive_win_rate_pct:            float  # 0-1 win rate in competitive deals
    competitive_loss_rate_pct:           float  # 0-1 loss rate in competitive deals
    battle_card_usage_rate_pct:          float  # 0-1 % of competitive deals where battle card used
    competitive_mention_early_rate_pct:  float  # 0-1 % deals where competition surfaced early
    price_concession_vs_competitor_pct:  float  # 0-1 % deals where price cut due to comp pressure
    feature_comparison_loss_rate_pct:    float  # 0-1 % losses attributed to feature gaps
    competitive_deal_cycle_delta_days:   float  # extra days when competitor involved
    no_competitive_intel_rate_pct:       float  # 0-1 % deals with no competitor identified
    competitive_stakeholder_loss_pct:    float  # 0-1 % competitive losses at exec level
    single_competitor_thread_rate_pct:   float  # 0-1 % deals where only one contact engaged vs comp
    late_competitor_discovery_rate_pct:  float  # 0-1 % deals where comp identified late (after demo)
    displacement_win_rate_pct:           float  # 0-1 win rate on displacement deals (replacing incumbent)
    proof_of_concept_win_rate_pct:       float  # 0-1 win rate when POC/bakeoff involved
    reference_customer_usage_pct:        float  # 0-1 % deals with reference customer deployed
    total_competitive_deals:             int
    avg_deal_value_usd:                  float
    competitive_intensity_score:         float  # 0-1 how often top 3 competitors appear
    head_to_head_calls_per_deal:         float  # avg calls with competitive intelligence team per deal
    post_loss_debrief_rate_pct:          float  # 0-1 % competitive losses followed by debrief
    total_deals_evaluated:               int


@dataclass
class CompetitiveResult:
    rep_id:                          str
    region:                          str
    competitive_risk:                CompetitiveRisk
    competitive_pattern:             CompetitivePattern
    competitive_severity:            CompetitiveSeverity
    recommended_action:              CompetitiveAction
    preparedness_score:              float
    execution_score:                 float
    intelligence_score:              float
    positioning_score:               float
    competitive_composite:           float
    has_competitive_gap:             bool
    requires_competitive_coaching:   bool
    estimated_lost_revenue_usd:      float
    competitive_signal:              str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "competitive_risk":              self.competitive_risk.value,
            "competitive_pattern":           self.competitive_pattern.value,
            "competitive_severity":          self.competitive_severity.value,
            "recommended_action":            self.recommended_action.value,
            "preparedness_score":            self.preparedness_score,
            "execution_score":               self.execution_score,
            "intelligence_score":            self.intelligence_score,
            "positioning_score":             self.positioning_score,
            "competitive_composite":         self.competitive_composite,
            "has_competitive_gap":           self.has_competitive_gap,
            "requires_competitive_coaching": self.requires_competitive_coaching,
            "estimated_lost_revenue_usd":    self.estimated_lost_revenue_usd,
            "competitive_signal":            self.competitive_signal,
        }


class SalesCompetitiveIntelligenceBattleCardEngine:
    """Identifies reps losing competitive deals due to poor preparation, late discovery, or feature fixation."""

    def __init__(self) -> None:
        self._results: List[CompetitiveResult] = []

    # ── sub-scores ─────────────────────────────────────────────────────────────

    def _preparedness_score(self, inp: CompetitiveInput) -> float:
        s = 0.0
        if   inp.battle_card_usage_rate_pct    <= 0.25: s += 40
        elif inp.battle_card_usage_rate_pct    <= 0.50: s += 22
        elif inp.battle_card_usage_rate_pct    <= 0.70: s += 8
        if   inp.no_competitive_intel_rate_pct >= 0.40: s += 35
        elif inp.no_competitive_intel_rate_pct >= 0.22: s += 18
        if   inp.post_loss_debrief_rate_pct    <= 0.20: s += 25
        elif inp.post_loss_debrief_rate_pct    <= 0.45: s += 12
        return min(s, 100.0)

    def _execution_score(self, inp: CompetitiveInput) -> float:
        s = 0.0
        if   inp.competitive_win_rate_pct      <= 0.25: s += 45
        elif inp.competitive_win_rate_pct      <= 0.45: s += 25
        elif inp.competitive_win_rate_pct      <= 0.60: s += 10
        if   inp.price_concession_vs_competitor_pct >= 0.50: s += 30
        elif inp.price_concession_vs_competitor_pct >= 0.28: s += 15
        if   inp.competitive_deal_cycle_delta_days  >= 25: s += 25
        elif inp.competitive_deal_cycle_delta_days  >= 12: s += 12
        return min(s, 100.0)

    def _intelligence_score(self, inp: CompetitiveInput) -> float:
        s = 0.0
        if   inp.late_competitor_discovery_rate_pct >= 0.45: s += 40
        elif inp.late_competitor_discovery_rate_pct >= 0.25: s += 22
        elif inp.late_competitor_discovery_rate_pct >= 0.12: s += 8
        if   inp.competitive_mention_early_rate_pct <= 0.25: s += 35
        elif inp.competitive_mention_early_rate_pct <= 0.50: s += 18
        if   inp.head_to_head_calls_per_deal        <= 0.5: s += 25
        elif inp.head_to_head_calls_per_deal        <= 1.2: s += 12
        return min(s, 100.0)

    def _positioning_score(self, inp: CompetitiveInput) -> float:
        s = 0.0
        if   inp.feature_comparison_loss_rate_pct   >= 0.45: s += 40
        elif inp.feature_comparison_loss_rate_pct   >= 0.25: s += 22
        elif inp.feature_comparison_loss_rate_pct   >= 0.12: s += 8
        if   inp.single_competitor_thread_rate_pct  >= 0.60: s += 35
        elif inp.single_competitor_thread_rate_pct  >= 0.35: s += 18
        if   inp.reference_customer_usage_pct       <= 0.15: s += 25
        elif inp.reference_customer_usage_pct       <= 0.35: s += 12
        return min(s, 100.0)

    # ── composite ──────────────────────────────────────────────────────────────

    def _composite(self, pr: float, ex: float, in_: float, po: float) -> float:
        return min(round(pr * 0.25 + ex * 0.35 + in_ * 0.20 + po * 0.20, 2), 100.0)

    # ── pattern ────────────────────────────────────────────────────────────────

    def _pattern(self, inp: CompetitiveInput) -> CompetitivePattern:
        if inp.battle_card_usage_rate_pct <= 0.20 and inp.no_competitive_intel_rate_pct >= 0.40:
            return CompetitivePattern.unprepared_seller
        if inp.feature_comparison_loss_rate_pct >= 0.45 and inp.price_concession_vs_competitor_pct <= 0.20:
            return CompetitivePattern.feature_fighter
        if inp.price_concession_vs_competitor_pct >= 0.55 and inp.competitive_win_rate_pct <= 0.30:
            return CompetitivePattern.price_surrenderer
        if inp.late_competitor_discovery_rate_pct >= 0.45 and inp.competitive_mention_early_rate_pct <= 0.20:
            return CompetitivePattern.late_discovery
        if inp.single_competitor_thread_rate_pct >= 0.60 and inp.competitive_stakeholder_loss_pct >= 0.45:
            return CompetitivePattern.single_thread_loser
        return CompetitivePattern.none

    # ── thresholds ─────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> CompetitiveRisk:
        if   composite >= 60: return CompetitiveRisk.critical
        elif composite >= 40: return CompetitiveRisk.high
        elif composite >= 20: return CompetitiveRisk.moderate
        return CompetitiveRisk.low

    def _severity(self, composite: float) -> CompetitiveSeverity:
        if   composite >= 60: return CompetitiveSeverity.losing
        elif composite >= 40: return CompetitiveSeverity.struggling
        elif composite >= 20: return CompetitiveSeverity.competing
        return CompetitiveSeverity.dominant

    def _action(self, risk: CompetitiveRisk, pattern: CompetitivePattern) -> CompetitiveAction:
        if risk == CompetitiveRisk.critical:
            if pattern in (CompetitivePattern.unprepared_seller, CompetitivePattern.price_surrenderer):
                return CompetitiveAction.executive_competitive_escalation
            return CompetitiveAction.competitive_deal_review
        if risk == CompetitiveRisk.high:
            if pattern == CompetitivePattern.unprepared_seller:
                return CompetitiveAction.battle_card_refresh_coaching
            if pattern == CompetitivePattern.feature_fighter:
                return CompetitiveAction.value_differentiation_coaching
            if pattern == CompetitivePattern.price_surrenderer:
                return CompetitiveAction.value_differentiation_coaching
            if pattern == CompetitivePattern.late_discovery:
                return CompetitiveAction.competitive_awareness_coaching
            if pattern == CompetitivePattern.single_thread_loser:
                return CompetitiveAction.multi_thread_coaching
            return CompetitiveAction.battle_card_refresh_coaching
        if risk == CompetitiveRisk.moderate:
            return CompetitiveAction.competitive_awareness_coaching
        return CompetitiveAction.no_action

    # ── flags ──────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: CompetitiveInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.competitive_win_rate_pct      <= 0.40
            or inp.battle_card_usage_rate_pct    <= 0.50
        )

    def _requires_coaching(self, inp: CompetitiveInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.no_competitive_intel_rate_pct >= 0.30
            or inp.late_competitor_discovery_rate_pct >= 0.25
        )

    # ── lost revenue ───────────────────────────────────────────────────────────

    def _lost_revenue(self, inp: CompetitiveInput, composite: float) -> float:
        loss_rate = inp.competitive_loss_rate_pct * (composite / 100)
        return round(inp.total_competitive_deals * inp.avg_deal_value_usd * loss_rate, 2)

    # ── signal ─────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        CompetitivePattern.unprepared_seller:   "Unprepared seller",
        CompetitivePattern.feature_fighter:     "Feature fighter",
        CompetitivePattern.price_surrenderer:   "Price surrenderer",
        CompetitivePattern.late_discovery:      "Late discovery",
        CompetitivePattern.single_thread_loser: "Single-thread loser",
    }

    def _signal(self, inp: CompetitiveInput, pattern: CompetitivePattern, composite: float) -> str:
        if composite < 20:
            return (
                "Competitive execution healthy — win rate, battle card usage, "
                "and intel discovery within benchmarks"
            )
        label    = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        win_pct  = round(inp.competitive_win_rate_pct * 100)
        bc_pct   = round(inp.battle_card_usage_rate_pct * 100)
        late_pct = round(inp.late_competitor_discovery_rate_pct * 100)
        comp_int = round(composite)
        return (
            f"{label} — {win_pct}% comp win rate — {bc_pct}% battle card usage — "
            f"{late_pct}% late discovery — composite {comp_int}"
        )

    # ── public API ─────────────────────────────────────────────────────────────

    def assess(self, inp: CompetitiveInput) -> CompetitiveResult:
        pr   = self._preparedness_score(inp)
        ex   = self._execution_score(inp)
        in_  = self._intelligence_score(inp)
        po   = self._positioning_score(inp)
        comp = self._composite(pr, ex, in_, po)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = CompetitiveResult(
            rep_id                          = inp.rep_id,
            region                          = inp.region,
            competitive_risk                = risk,
            competitive_pattern             = pattern,
            competitive_severity            = severity,
            recommended_action              = action,
            preparedness_score              = pr,
            execution_score                 = ex,
            intelligence_score              = in_,
            positioning_score               = po,
            competitive_composite           = comp,
            has_competitive_gap             = self._has_gap(inp, comp),
            requires_competitive_coaching   = self._requires_coaching(inp, comp),
            estimated_lost_revenue_usd      = self._lost_revenue(inp, comp),
            competitive_signal              = self._signal(inp, pattern, comp),
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
                "avg_preparedness_score": 0.0,
                "avg_execution_score": 0.0,
                "avg_intelligence_score": 0.0,
                "avg_positioning_score": 0.0,
                "total_estimated_lost_revenue_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_pr = total_ex = total_in = total_po = total_lr = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.competitive_risk.value]         = risk_counts.get(res.competitive_risk.value, 0) + 1
            pattern_counts[res.competitive_pattern.value]   = pattern_counts.get(res.competitive_pattern.value, 0) + 1
            severity_counts[res.competitive_severity.value] = severity_counts.get(res.competitive_severity.value, 0) + 1
            action_counts[res.recommended_action.value]     = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.competitive_composite
            total_pr   += res.preparedness_score
            total_ex   += res.execution_score
            total_in   += res.intelligence_score
            total_po   += res.positioning_score
            total_lr   += res.estimated_lost_revenue_usd
            if res.has_competitive_gap:          gap_count      += 1
            if res.requires_competitive_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_competitive_composite":            round(total_comp / n, 1),
            "competitive_gap_count":                gap_count,
            "coaching_count":                       coaching_count,
            "avg_preparedness_score":               round(total_pr / n, 1),
            "avg_execution_score":                  round(total_ex / n, 1),
            "avg_intelligence_score":               round(total_in / n, 1),
            "avg_positioning_score":                round(total_po / n, 1),
            "total_estimated_lost_revenue_usd":     round(total_lr, 2),
        }
