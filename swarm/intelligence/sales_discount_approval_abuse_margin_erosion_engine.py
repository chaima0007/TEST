"""
Module 215 — Sales Discount Approval Abuse & Margin Erosion Engine
Detects unauthorized discounting, deal desk bypass, and systematic
margin erosion patterns per rep before they compound into P&L risk.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class MarginRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class MarginPattern(str, Enum):
    none                  = "none"
    approval_bypasser     = "approval_bypasser"
    panic_discounter      = "panic_discounter"
    margin_creep_enabler  = "margin_creep_enabler"
    list_price_ignorer    = "list_price_ignorer"
    quarter_end_dumper    = "quarter_end_dumper"


class MarginSeverity(str, Enum):
    disciplined  = "disciplined"
    drifting     = "drifting"
    eroding      = "eroding"
    collapsing   = "collapsing"


class MarginAction(str, Enum):
    no_action                     = "no_action"
    margin_monitoring             = "margin_monitoring"
    discount_hygiene_coaching     = "discount_hygiene_coaching"
    deal_desk_enforcement         = "deal_desk_enforcement"
    value_selling_coaching        = "value_selling_coaching"
    approval_workflow_audit       = "approval_workflow_audit"
    pricing_strategy_reset        = "pricing_strategy_reset"
    margin_rescue_intervention    = "margin_rescue_intervention"
    executive_pricing_escalation  = "executive_pricing_escalation"


@dataclass
class MarginInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    # Discount behavior
    avg_discount_pct: float                     # average discount granted
    max_discount_pct: float                     # largest single discount granted
    deals_discounted_above_approval_pct: float  # % deals discounted beyond approval limit
    unauthorized_discount_rate_pct: float       # % deals discounted without approval
    # Approval process
    deal_desk_bypass_rate_pct: float            # % discounts bypassing deal desk
    approval_cycle_shortcut_rate_pct: float     # % using emergency approval shortcuts
    post_approval_discount_increase_rate_pct: float  # % deals discounted more after approval
    # Margin outcomes
    avg_gross_margin_pct: float                 # avg gross margin achieved
    deals_below_floor_margin_pct: float         # % deals closed below margin floor
    quarter_end_discount_spike_ratio: float     # ratio of Q-end vs mid-Q discount rates
    # Value discipline
    list_price_adherence_rate_pct: float        # % deals started at list price
    discount_justification_rate_pct: float      # % discounts with documented justification
    multi_year_discount_front_loading_pct: float  # % multi-year deals with Y1 subsidy
    # Deal composition
    bundled_discount_rate_pct: float            # % discounts via bundling vs price cut
    competitive_discount_rate_pct: float        # % discounts claimed as competitive
    # Volume / context
    total_deals_closed: int
    avg_deal_value_usd: float


@dataclass
class MarginResult:
    rep_id: str
    region: str
    margin_risk: str
    margin_pattern: str
    margin_severity: str
    recommended_action: str
    discipline_score: float
    process_score: float
    outcome_score: float
    value_score: float
    margin_composite: float
    has_margin_gap: bool
    requires_intervention: bool
    estimated_margin_erosion_usd: float
    margin_signal: str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                      self.rep_id,
            "region":                      self.region,
            "margin_risk":                 self.margin_risk,
            "margin_pattern":              self.margin_pattern,
            "margin_severity":             self.margin_severity,
            "recommended_action":          self.recommended_action,
            "discipline_score":            self.discipline_score,
            "process_score":               self.process_score,
            "outcome_score":               self.outcome_score,
            "value_score":                 self.value_score,
            "margin_composite":            self.margin_composite,
            "has_margin_gap":              self.has_margin_gap,
            "requires_intervention":       self.requires_intervention,
            "estimated_margin_erosion_usd": self.estimated_margin_erosion_usd,
            "margin_signal":               self.margin_signal,
        }


class SalesDiscountApprovalAbuseMarginErosionEngine:
    def __init__(self) -> None:
        self._results: List[MarginResult] = []

    # ── Sub-scores ────────────────────────────────────────────────────────────

    def _discipline_score(self, i: MarginInput) -> float:
        s = 0
        if   i.avg_discount_pct                   >= 0.30: s += 40
        elif i.avg_discount_pct                   >= 0.18: s += 22
        elif i.avg_discount_pct                   >= 0.10: s += 8

        if   i.max_discount_pct                   >= 0.50: s += 35
        elif i.max_discount_pct                   >= 0.35: s += 18

        if   i.deals_discounted_above_approval_pct >= 0.40: s += 25
        elif i.deals_discounted_above_approval_pct >= 0.22: s += 12
        return min(s, 100)

    def _process_score(self, i: MarginInput) -> float:
        s = 0
        if   i.deal_desk_bypass_rate_pct               >= 0.40: s += 45
        elif i.deal_desk_bypass_rate_pct               >= 0.22: s += 25
        elif i.deal_desk_bypass_rate_pct               >= 0.10: s += 10

        if   i.unauthorized_discount_rate_pct          >= 0.30: s += 30
        elif i.unauthorized_discount_rate_pct          >= 0.15: s += 15

        if   i.post_approval_discount_increase_rate_pct >= 0.25: s += 25
        elif i.post_approval_discount_increase_rate_pct >= 0.12: s += 12
        return min(s, 100)

    def _outcome_score(self, i: MarginInput) -> float:
        s = 0
        if   i.deals_below_floor_margin_pct       >= 0.30: s += 40
        elif i.deals_below_floor_margin_pct       >= 0.15: s += 22
        elif i.deals_below_floor_margin_pct       >= 0.07: s += 8

        if   i.avg_gross_margin_pct               <= 0.20: s += 35
        elif i.avg_gross_margin_pct               <= 0.35: s += 18

        if   i.quarter_end_discount_spike_ratio   >= 2.5:  s += 25
        elif i.quarter_end_discount_spike_ratio   >= 1.8:  s += 12
        return min(s, 100)

    def _value_score(self, i: MarginInput) -> float:
        s = 0
        if   i.list_price_adherence_rate_pct      <= 0.30: s += 45
        elif i.list_price_adherence_rate_pct      <= 0.55: s += 25
        elif i.list_price_adherence_rate_pct      <= 0.75: s += 10

        if   i.discount_justification_rate_pct    <= 0.35: s += 30
        elif i.discount_justification_rate_pct    <= 0.60: s += 15

        if   i.bundled_discount_rate_pct          <= 0.20: s += 25
        elif i.bundled_discount_rate_pct          <= 0.40: s += 12
        return min(s, 100)

    # ── Composite ─────────────────────────────────────────────────────────────

    def _composite(self, di: float, pr: float, ou: float, va: float) -> float:
        return min(round(di * 0.30 + pr * 0.25 + ou * 0.25 + va * 0.20, 2), 100.0)

    # ── Risk / Severity ───────────────────────────────────────────────────────

    def _risk(self, c: float) -> MarginRisk:
        if c >= 60: return MarginRisk.critical
        if c >= 40: return MarginRisk.high
        if c >= 20: return MarginRisk.moderate
        return MarginRisk.low

    def _severity(self, c: float) -> MarginSeverity:
        if c >= 60: return MarginSeverity.collapsing
        if c >= 40: return MarginSeverity.eroding
        if c >= 20: return MarginSeverity.drifting
        return MarginSeverity.disciplined

    # ── Pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, i: MarginInput) -> MarginPattern:
        if (i.deal_desk_bypass_rate_pct >= 0.35
                and i.unauthorized_discount_rate_pct >= 0.25):
            return MarginPattern.approval_bypasser
        if (i.avg_discount_pct >= 0.25
                and i.list_price_adherence_rate_pct <= 0.35):
            return MarginPattern.list_price_ignorer
        if (i.quarter_end_discount_spike_ratio >= 2.2
                and i.deals_below_floor_margin_pct >= 0.20):
            return MarginPattern.quarter_end_dumper
        if (i.max_discount_pct >= 0.45
                and i.competitive_discount_rate_pct >= 0.60):
            return MarginPattern.panic_discounter
        if (i.multi_year_discount_front_loading_pct >= 0.45
                and i.avg_gross_margin_pct <= 0.30):
            return MarginPattern.margin_creep_enabler
        return MarginPattern.none

    # ── Action ────────────────────────────────────────────────────────────────

    def _action(self, risk: MarginRisk, pat: MarginPattern) -> MarginAction:
        if risk == MarginRisk.critical:
            if pat in (MarginPattern.approval_bypasser, MarginPattern.list_price_ignorer):
                return MarginAction.executive_pricing_escalation
            return MarginAction.margin_rescue_intervention
        if risk == MarginRisk.high:
            if pat == MarginPattern.approval_bypasser:    return MarginAction.approval_workflow_audit
            if pat == MarginPattern.panic_discounter:     return MarginAction.value_selling_coaching
            if pat == MarginPattern.margin_creep_enabler: return MarginAction.pricing_strategy_reset
            if pat == MarginPattern.list_price_ignorer:   return MarginAction.deal_desk_enforcement
            if pat == MarginPattern.quarter_end_dumper:   return MarginAction.discount_hygiene_coaching
            return MarginAction.margin_monitoring
        if risk == MarginRisk.moderate:
            return MarginAction.margin_monitoring
        return MarginAction.no_action

    # ── Signal ────────────────────────────────────────────────────────────────

    def _signal(self, i: MarginInput, pat: MarginPattern, comp: float) -> str:
        if comp < 20:
            return "Discount discipline strong — approval compliance, margin outcomes, and value selling within benchmark targets"
        labels = {
            MarginPattern.approval_bypasser:    "Approval bypasser",
            MarginPattern.panic_discounter:     "Panic discounter",
            MarginPattern.margin_creep_enabler: "Margin creep enabler",
            MarginPattern.list_price_ignorer:   "List price ignorer",
            MarginPattern.quarter_end_dumper:   "Quarter-end dumper",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {round(i.avg_discount_pct*100)}% avg discount — "
            f"{round(i.deal_desk_bypass_rate_pct*100)}% deal desk bypass — "
            f"{round(i.deals_below_floor_margin_pct*100)}% below floor — "
            f"composite {round(comp)}"
        )

    # ── Flags ─────────────────────────────────────────────────────────────────

    def _has_margin_gap(self, i: MarginInput, comp: float) -> bool:
        return (comp >= 40
                or i.avg_gross_margin_pct <= 0.35
                or i.deals_below_floor_margin_pct >= 0.15)

    def _requires_intervention(self, i: MarginInput, comp: float) -> bool:
        return (comp >= 25
                or i.deal_desk_bypass_rate_pct >= 0.20
                or i.avg_discount_pct >= 0.15)

    # ── Margin erosion estimate ───────────────────────────────────────────────

    def _margin_erosion(self, i: MarginInput, comp: float) -> float:
        return round(
            i.total_deals_closed
            * i.avg_deal_value_usd
            * i.avg_discount_pct
            * (comp / 100),
            2,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def assess(self, i: MarginInput) -> MarginResult:
        di  = self._discipline_score(i)
        pr  = self._process_score(i)
        ou  = self._outcome_score(i)
        va  = self._value_score(i)
        comp = self._composite(di, pr, ou, va)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = MarginResult(
            rep_id=i.rep_id,
            region=i.region,
            margin_risk=risk.value,
            margin_pattern=pat.value,
            margin_severity=sev.value,
            recommended_action=act.value,
            discipline_score=di,
            process_score=pr,
            outcome_score=ou,
            value_score=va,
            margin_composite=comp,
            has_margin_gap=self._has_margin_gap(i, comp),
            requires_intervention=self._requires_intervention(i, comp),
            estimated_margin_erosion_usd=self._margin_erosion(i, comp),
            margin_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[MarginInput]) -> List[MarginResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_margin_composite": 0.0,
                "margin_gap_count": 0,
                "intervention_count": 0,
                "avg_discipline_score": 0.0,
                "avg_process_score": 0.0,
                "avg_outcome_score": 0.0,
                "avg_value_score": 0.0,
                "total_estimated_margin_erosion_usd": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tdi = tpr = tou = tva = tcomp = tme = 0.0
        gc = ic = 0
        for r in self._results:
            rc[r.margin_risk]      = rc.get(r.margin_risk, 0)      + 1
            pc[r.margin_pattern]   = pc.get(r.margin_pattern, 0)   + 1
            sc[r.margin_severity]  = sc.get(r.margin_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tdi  += r.discipline_score
            tpr  += r.process_score
            tou  += r.outcome_score
            tva  += r.value_score
            tcomp += r.margin_composite
            tme  += r.estimated_margin_erosion_usd
            if r.has_margin_gap:       gc += 1
            if r.requires_intervention: ic += 1
        return {
            "total":                              n,
            "risk_counts":                        rc,
            "pattern_counts":                     pc,
            "severity_counts":                    sc,
            "action_counts":                      ac,
            "avg_margin_composite":               round(tcomp / n, 1),
            "margin_gap_count":                   gc,
            "intervention_count":                 ic,
            "avg_discipline_score":               round(tdi / n, 1),
            "avg_process_score":                  round(tpr / n, 1),
            "avg_outcome_score":                  round(tou / n, 1),
            "avg_value_score":                    round(tva / n, 1),
            "total_estimated_margin_erosion_usd": round(tme, 2),
        }
