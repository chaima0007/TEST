from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ExpansionLeakRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class LeakPattern(str, Enum):
    none                      = "none"
    upsell_neglect            = "upsell_neglect"
    cross_sell_gap            = "cross_sell_gap"
    renewal_underpricing      = "renewal_underpricing"
    champion_not_leveraged    = "champion_not_leveraged"
    expansion_stall           = "expansion_stall"


class LeakSeverity(str, Enum):
    captured   = "captured"
    watch      = "watch"
    leaking    = "leaking"
    critical   = "critical"


class LeakAction(str, Enum):
    no_action              = "no_action"
    expansion_outreach     = "expansion_outreach"
    qbr_scheduling         = "qbr_scheduling"
    pricing_renegotiation  = "pricing_renegotiation"
    executive_alignment    = "executive_alignment"


@dataclass
class ExpansionLeakInput:
    account_id: str
    region: str
    csm_id: str
    contract_arr_usd: float
    expansion_potential_usd: float
    upsell_attempts_last_90d: int
    upsell_wins_last_90d: int
    cross_sell_products_available: int
    cross_sell_products_adopted: int
    renewal_price_increase_pct: float
    market_price_increase_benchmark_pct: float
    days_since_last_expansion_discussion: int
    champion_engagement_score: float
    champion_intro_to_new_stakeholders: int
    qbr_held_last_180d: int
    product_usage_growth_pct: float
    license_utilization_pct: float
    nps_score: float
    account_health_score: float
    open_expansion_opportunities: int
    expansion_opportunities_aged_90d_plus: int
    competitive_displacement_risk_score: float


@dataclass
class ExpansionLeakResult:
    account_id: str
    region: str
    expansion_leak_risk: ExpansionLeakRisk
    leak_pattern: LeakPattern
    leak_severity: LeakSeverity
    recommended_action: LeakAction
    upsell_neglect_score: float
    cross_sell_gap_score: float
    renewal_pricing_score: float
    champion_leverage_score: float
    expansion_leak_composite: float
    is_revenue_leaking: bool
    requires_immediate_action: bool
    estimated_leaked_revenue_usd: float
    leak_signal: str

    def to_dict(self) -> dict:
        return {
            "account_id":                    self.account_id,
            "region":                        self.region,
            "expansion_leak_risk":           self.expansion_leak_risk.value,
            "leak_pattern":                  self.leak_pattern.value,
            "leak_severity":                 self.leak_severity.value,
            "recommended_action":            self.recommended_action.value,
            "upsell_neglect_score":          self.upsell_neglect_score,
            "cross_sell_gap_score":          self.cross_sell_gap_score,
            "renewal_pricing_score":         self.renewal_pricing_score,
            "champion_leverage_score":       self.champion_leverage_score,
            "expansion_leak_composite":      self.expansion_leak_composite,
            "is_revenue_leaking":            self.is_revenue_leaking,
            "requires_immediate_action":     self.requires_immediate_action,
            "estimated_leaked_revenue_usd":  self.estimated_leaked_revenue_usd,
            "leak_signal":                   self.leak_signal,
        }


class CustomerExpansionRevenueLeakDetector:

    def __init__(self) -> None:
        self._results: list[ExpansionLeakResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100)
    # ------------------------------------------------------------------

    def _upsell_neglect_score(self, inp: ExpansionLeakInput) -> float:
        score = 0.0

        # Upsell conversion rate
        if inp.upsell_attempts_last_90d > 0:
            conversion = inp.upsell_wins_last_90d / inp.upsell_attempts_last_90d
            if conversion < 0.10:
                score += 30.0
            elif conversion < 0.25:
                score += 15.0
        elif inp.expansion_potential_usd > 0:
            # No attempts despite potential = neglect
            score += 35.0

        # Days since last expansion discussion
        if inp.days_since_last_expansion_discussion >= 90:
            score += 35.0
        elif inp.days_since_last_expansion_discussion >= 60:
            score += 20.0
        elif inp.days_since_last_expansion_discussion >= 30:
            score += 8.0

        # Aged open opportunities
        if inp.expansion_opportunities_aged_90d_plus >= 3:
            score += 20.0
        elif inp.expansion_opportunities_aged_90d_plus >= 1:
            score += 10.0

        # High usage but no upsell = missed signal
        if inp.license_utilization_pct >= 0.90 and inp.upsell_attempts_last_90d == 0:
            score += 15.0

        return min(score, 100.0)

    def _cross_sell_gap_score(self, inp: ExpansionLeakInput) -> float:
        score = 0.0

        # Product adoption gap
        if inp.cross_sell_products_available > 0:
            adoption = inp.cross_sell_products_adopted / inp.cross_sell_products_available
            if adoption < 0.20:
                score += 45.0
            elif adoption < 0.40:
                score += 25.0
            elif adoption < 0.60:
                score += 10.0

        # High health + low adoption = opportunity gap
        if inp.account_health_score >= 70.0 and inp.cross_sell_products_available > 0:
            adoption = inp.cross_sell_products_adopted / inp.cross_sell_products_available
            if adoption < 0.30:
                score += 20.0

        # Growing usage with low cross-sell = whitespace
        if inp.product_usage_growth_pct >= 20.0 and inp.cross_sell_products_adopted == 0:
            score += 20.0
        elif inp.product_usage_growth_pct >= 10.0 and inp.cross_sell_products_adopted == 0:
            score += 10.0

        # Open expansion opps not acted on
        if inp.open_expansion_opportunities >= 4:
            score += 15.0
        elif inp.open_expansion_opportunities >= 2:
            score += 7.0

        return min(score, 100.0)

    def _renewal_pricing_score(self, inp: ExpansionLeakInput) -> float:
        score = 0.0

        # Underpricing vs market benchmark
        delta = inp.market_price_increase_benchmark_pct - inp.renewal_price_increase_pct
        if delta >= 10.0:
            score += 45.0
        elif delta >= 5.0:
            score += 25.0
        elif delta >= 2.0:
            score += 10.0

        # High NPS but low price increase = missed leverage
        if inp.nps_score >= 70.0 and inp.renewal_price_increase_pct < inp.market_price_increase_benchmark_pct * 0.5:
            score += 25.0

        # High health score but no price increase
        if inp.account_health_score >= 75.0 and inp.renewal_price_increase_pct < 3.0:
            score += 20.0

        # Competitive risk reducing negotiating power
        if inp.competitive_displacement_risk_score >= 60.0:
            score += 10.0

        return min(score, 100.0)

    def _champion_leverage_score(self, inp: ExpansionLeakInput) -> float:
        score = 0.0

        # Low champion engagement
        if inp.champion_engagement_score < 30.0:
            score += 40.0
        elif inp.champion_engagement_score < 50.0:
            score += 20.0
        elif inp.champion_engagement_score < 65.0:
            score += 8.0

        # No stakeholder introductions (champion not leveraged)
        if inp.champion_intro_to_new_stakeholders == 0 and inp.account_health_score >= 60.0:
            score += 30.0
        elif inp.champion_intro_to_new_stakeholders == 0:
            score += 15.0

        # No QBR held
        if inp.qbr_held_last_180d == 0:
            score += 20.0
        elif inp.qbr_held_last_180d == 1:
            score += 5.0

        # Low NPS but no retention-led expansion
        if inp.nps_score < 40.0 and inp.expansion_potential_usd > 0:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ExpansionLeakInput,
                         upsell: float, cross: float,
                         pricing: float, champion: float) -> LeakPattern:
        # Priority: expansion_stall > champion_not_leveraged > renewal_underpricing
        #           > cross_sell_gap > upsell_neglect > none
        if upsell >= 30 and cross >= 30 and inp.expansion_opportunities_aged_90d_plus >= 2:
            return LeakPattern.expansion_stall
        if champion >= 30 and inp.champion_intro_to_new_stakeholders == 0 and inp.qbr_held_last_180d == 0:
            return LeakPattern.champion_not_leveraged
        if pricing >= 25 and (inp.market_price_increase_benchmark_pct - inp.renewal_price_increase_pct) >= 5.0:
            return LeakPattern.renewal_underpricing
        if cross >= 25 and inp.cross_sell_products_available > 0:
            adoption = inp.cross_sell_products_adopted / inp.cross_sell_products_available
            if adoption < 0.40:
                return LeakPattern.cross_sell_gap
        if upsell >= 20 and inp.days_since_last_expansion_discussion >= 45:
            return LeakPattern.upsell_neglect
        return LeakPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ExpansionLeakRisk:
        if composite >= 60:
            return ExpansionLeakRisk.critical
        if composite >= 40:
            return ExpansionLeakRisk.high
        if composite >= 20:
            return ExpansionLeakRisk.moderate
        return ExpansionLeakRisk.low

    def _severity(self, composite: float) -> LeakSeverity:
        if composite >= 60:
            return LeakSeverity.critical
        if composite >= 40:
            return LeakSeverity.leaking
        if composite >= 20:
            return LeakSeverity.watch
        return LeakSeverity.captured

    def _action(self, risk: ExpansionLeakRisk, pattern: LeakPattern) -> LeakAction:
        if risk == ExpansionLeakRisk.critical:
            if pattern == LeakPattern.champion_not_leveraged:
                return LeakAction.executive_alignment
            return LeakAction.qbr_scheduling
        if risk == ExpansionLeakRisk.high:
            if pattern == LeakPattern.renewal_underpricing:
                return LeakAction.pricing_renegotiation
            return LeakAction.expansion_outreach
        if risk == ExpansionLeakRisk.moderate:
            return LeakAction.expansion_outreach
        return LeakAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _is_revenue_leaking(self, composite: float, inp: ExpansionLeakInput) -> bool:
        return (
            composite >= 40
            or inp.expansion_opportunities_aged_90d_plus >= 3
            or (inp.license_utilization_pct >= 0.95 and inp.upsell_attempts_last_90d == 0)
        )

    def _requires_immediate_action(self, composite: float, inp: ExpansionLeakInput) -> bool:
        return (
            composite >= 30
            or inp.days_since_last_expansion_discussion >= 90
            or inp.qbr_held_last_180d == 0
        )

    # ------------------------------------------------------------------
    # Leaked revenue estimate
    # ------------------------------------------------------------------

    def _leaked_revenue(self, inp: ExpansionLeakInput, composite: float) -> float:
        return round(inp.expansion_potential_usd * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ExpansionLeakInput, pattern: LeakPattern,
                composite: float) -> str:
        if composite < 5 and pattern == LeakPattern.none:
            return "Expansion motion healthy — all revenue opportunities being actively pursued"
        parts: list[str] = []
        if inp.days_since_last_expansion_discussion >= 60:
            parts.append(f"{inp.days_since_last_expansion_discussion}d since expansion discussion")
        if inp.cross_sell_products_available > 0:
            adoption = inp.cross_sell_products_adopted / inp.cross_sell_products_available
            if adoption < 0.40:
                parts.append(f"{adoption*100:.0f}% cross-sell adoption")
        if inp.expansion_opportunities_aged_90d_plus >= 1:
            parts.append(f"{inp.expansion_opportunities_aged_90d_plus} aged opps 90d+")
        if inp.qbr_held_last_180d == 0:
            parts.append("no QBR in 180d")
        if inp.license_utilization_pct >= 0.90 and inp.upsell_attempts_last_90d == 0:
            parts.append(f"{inp.license_utilization_pct*100:.0f}% utilization with no upsell attempt")
        label = pattern.value.replace("_", " ")
        summary = " — ".join(parts) if parts else "expansion signals detected"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ExpansionLeakInput) -> ExpansionLeakResult:
        u = round(self._upsell_neglect_score(inp), 1)
        c = round(self._cross_sell_gap_score(inp), 1)
        r = round(self._renewal_pricing_score(inp), 1)
        h = round(self._champion_leverage_score(inp), 1)

        composite = round(u * 0.30 + c * 0.30 + r * 0.25 + h * 0.15, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, u, c, r, h)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        is_rl = self._is_revenue_leaking(composite, inp)
        is_ri = self._requires_immediate_action(composite, inp)
        leaked= self._leaked_revenue(inp, composite)
        signal= self._signal(inp, pattern, composite)

        result = ExpansionLeakResult(
            account_id=inp.account_id,
            region=inp.region,
            expansion_leak_risk=risk,
            leak_pattern=pattern,
            leak_severity=severity,
            recommended_action=action,
            upsell_neglect_score=u,
            cross_sell_gap_score=c,
            renewal_pricing_score=r,
            champion_leverage_score=h,
            expansion_leak_composite=composite,
            is_revenue_leaking=is_rl,
            requires_immediate_action=is_ri,
            estimated_leaked_revenue_usd=leaked,
            leak_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ExpansionLeakInput]) -> list[ExpansionLeakResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_expansion_leak_composite": 0.0,
                "leaking_count": 0,
                "immediate_action_count": 0,
                "avg_upsell_neglect_score": 0.0,
                "avg_cross_sell_gap_score": 0.0,
                "avg_renewal_pricing_score": 0.0,
                "avg_champion_leverage_score": 0.0,
                "total_estimated_leaked_revenue_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_u = total_c = total_r = total_h = total_rev = 0.0

        for res in self._results:
            risk_counts[res.expansion_leak_risk.value]   = risk_counts.get(res.expansion_leak_risk.value, 0) + 1
            pattern_counts[res.leak_pattern.value]       = pattern_counts.get(res.leak_pattern.value, 0) + 1
            severity_counts[res.leak_severity.value]     = severity_counts.get(res.leak_severity.value, 0) + 1
            action_counts[res.recommended_action.value]  = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.expansion_leak_composite
            total_u    += res.upsell_neglect_score
            total_c    += res.cross_sell_gap_score
            total_r    += res.renewal_pricing_score
            total_h    += res.champion_leverage_score
            total_rev  += res.estimated_leaked_revenue_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_expansion_leak_composite":         round(total_comp / n, 1),
            "leaking_count":                        sum(1 for r in self._results if r.is_revenue_leaking),
            "immediate_action_count":               sum(1 for r in self._results if r.requires_immediate_action),
            "avg_upsell_neglect_score":             round(total_u / n, 1),
            "avg_cross_sell_gap_score":             round(total_c / n, 1),
            "avg_renewal_pricing_score":            round(total_r / n, 1),
            "avg_champion_leverage_score":          round(total_h / n, 1),
            "total_estimated_leaked_revenue_usd":   round(total_rev, 2),
        }
