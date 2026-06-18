from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ExpansionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ExpansionPattern(str, Enum):
    none               = "none"
    stagnant_portfolio = "stagnant_portfolio"
    cross_sell_neglect = "cross_sell_neglect"
    renewal_risk       = "renewal_risk"
    low_penetration    = "low_penetration"
    executive_gap      = "executive_gap"


class ExpansionSeverity(str, Enum):
    growing   = "growing"
    steady    = "steady"
    declining = "declining"
    stagnant  = "stagnant"


class ExpansionAction(str, Enum):
    no_action              = "no_action"
    expansion_outreach     = "expansion_outreach"
    cross_sell_campaign    = "cross_sell_campaign"
    renewal_acceleration   = "renewal_acceleration"
    penetration_deepening  = "penetration_deepening"
    executive_alignment    = "executive_alignment"


@dataclass
class AccountExpansionInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_accounts: int
    expansion_ready_accounts: int
    expansion_conversations_initiated: int
    expansion_proposals_sent: int
    expansion_deals_closed: int
    cross_sell_opportunities_identified: int
    cross_sell_opportunities_pursued: int
    upsell_revenue_last_period_usd: float
    avg_account_product_penetration_pct: float
    accounts_at_contract_renewal_90d: int
    renewal_expansions_secured_count: int
    net_revenue_retention_pct: float
    avg_account_lifetime_months: float
    multi_product_accounts_count: int
    single_product_accounts_count: int
    executive_sponsor_coverage_pct: float
    account_health_avg_score: float
    avg_contract_value_usd: float
    churn_prevented_revenue_usd: float


@dataclass
class AccountExpansionResult:
    rep_id: str
    region: str
    expansion_risk: ExpansionRisk
    expansion_pattern: ExpansionPattern
    expansion_severity: ExpansionSeverity
    recommended_action: ExpansionAction
    expansion_capture_score: float
    portfolio_penetration_score: float
    renewal_health_score: float
    executive_coverage_score: float
    account_expansion_composite: float
    has_expansion_gap: bool
    requires_account_review: bool
    estimated_expansion_revenue_upside_usd: float
    expansion_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                                   self.rep_id,
            "region":                                   self.region,
            "expansion_risk":                           self.expansion_risk.value,
            "expansion_pattern":                        self.expansion_pattern.value,
            "expansion_severity":                       self.expansion_severity.value,
            "recommended_action":                       self.recommended_action.value,
            "expansion_capture_score":                  self.expansion_capture_score,
            "portfolio_penetration_score":              self.portfolio_penetration_score,
            "renewal_health_score":                     self.renewal_health_score,
            "executive_coverage_score":                 self.executive_coverage_score,
            "account_expansion_composite":              self.account_expansion_composite,
            "has_expansion_gap":                        self.has_expansion_gap,
            "requires_account_review":                  self.requires_account_review,
            "estimated_expansion_revenue_upside_usd":   self.estimated_expansion_revenue_upside_usd,
            "expansion_signal":                         self.expansion_signal,
        }


class SalesAccountExpansionIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[AccountExpansionResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk / missed opportunity)
    # ------------------------------------------------------------------

    def _expansion_capture_score(self, inp: AccountExpansionInput) -> float:
        score = 0.0
        ready = max(inp.expansion_ready_accounts, 1)

        engage_rate = inp.expansion_conversations_initiated / ready
        if engage_rate < 0.30:
            score += 35.0
        elif engage_rate < 0.50:
            score += 20.0
        elif engage_rate < 0.70:
            score += 8.0

        if inp.expansion_proposals_sent == 0 and inp.expansion_ready_accounts >= 3:
            score += 25.0
        elif inp.expansion_proposals_sent <= 1 and inp.expansion_ready_accounts >= 5:
            score += 12.0

        xsell_denom = max(inp.cross_sell_opportunities_identified, 1)
        xsell_rate = inp.cross_sell_opportunities_pursued / xsell_denom
        if xsell_rate < 0.25:
            score += 25.0
        elif xsell_rate < 0.50:
            score += 12.0

        proposals_denom = max(inp.expansion_proposals_sent, 1)
        close_rate = inp.expansion_deals_closed / proposals_denom
        if inp.expansion_proposals_sent > 0 and close_rate < 0.20:
            score += 15.0
        elif inp.expansion_proposals_sent > 0 and close_rate < 0.40:
            score += 8.0

        return min(score, 100.0)

    def _portfolio_penetration_score(self, inp: AccountExpansionInput) -> float:
        score = 0.0

        if inp.avg_account_product_penetration_pct < 0.25:
            score += 35.0
        elif inp.avg_account_product_penetration_pct < 0.45:
            score += 20.0
        elif inp.avg_account_product_penetration_pct < 0.60:
            score += 8.0

        total_accounts = inp.multi_product_accounts_count + inp.single_product_accounts_count
        single_ratio = inp.single_product_accounts_count / max(total_accounts, 1)
        if single_ratio >= 0.70:
            score += 30.0
        elif single_ratio >= 0.50:
            score += 15.0
        elif single_ratio >= 0.35:
            score += 8.0

        if inp.net_revenue_retention_pct < 0.90:
            score += 25.0
        elif inp.net_revenue_retention_pct < 1.00:
            score += 12.0
        elif inp.net_revenue_retention_pct < 1.05:
            score += 5.0

        return min(score, 100.0)

    def _renewal_health_score(self, inp: AccountExpansionInput) -> float:
        score = 0.0

        renewal_denom = max(inp.accounts_at_contract_renewal_90d, 1)
        secured_rate = inp.renewal_expansions_secured_count / renewal_denom
        if inp.accounts_at_contract_renewal_90d > 0 and secured_rate < 0.30:
            score += 40.0
        elif inp.accounts_at_contract_renewal_90d > 0 and secured_rate < 0.60:
            score += 20.0

        if inp.account_health_avg_score < 5.0:
            score += 30.0
        elif inp.account_health_avg_score < 7.0:
            score += 15.0

        if inp.avg_account_lifetime_months < 12:
            score += 20.0
        elif inp.avg_account_lifetime_months < 24:
            score += 10.0

        return min(score, 100.0)

    def _executive_coverage_score(self, inp: AccountExpansionInput) -> float:
        score = 0.0

        if inp.executive_sponsor_coverage_pct < 0.25:
            score += 45.0
        elif inp.executive_sponsor_coverage_pct < 0.50:
            score += 25.0
        elif inp.executive_sponsor_coverage_pct < 0.70:
            score += 10.0

        total = max(inp.total_accounts, 1)
        expansion_density = inp.expansion_deals_closed / total
        if expansion_density < 0.05:
            score += 30.0
        elif expansion_density < 0.10:
            score += 15.0

        if inp.upsell_revenue_last_period_usd == 0.0:
            score += 25.0
        elif inp.upsell_revenue_last_period_usd < inp.avg_contract_value_usd * 0.10:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: AccountExpansionInput,
                         capture: float, penetration: float,
                         renewal: float, executive: float) -> ExpansionPattern:
        # Priority: stagnant_portfolio > cross_sell_neglect > renewal_risk
        #           > low_penetration > executive_gap > none
        if capture >= 40 and inp.expansion_deals_closed == 0 and inp.expansion_ready_accounts >= 3:
            return ExpansionPattern.stagnant_portfolio

        xsell_denom = max(inp.cross_sell_opportunities_identified, 1)
        xsell_rate = inp.cross_sell_opportunities_pursued / xsell_denom
        if capture >= 30 and inp.cross_sell_opportunities_identified >= 3 and xsell_rate < 0.30:
            return ExpansionPattern.cross_sell_neglect

        if renewal >= 35 and inp.accounts_at_contract_renewal_90d >= 2:
            return ExpansionPattern.renewal_risk

        if penetration >= 30 and inp.avg_account_product_penetration_pct < 0.40:
            return ExpansionPattern.low_penetration

        if executive >= 30 and inp.executive_sponsor_coverage_pct < 0.40:
            return ExpansionPattern.executive_gap

        return ExpansionPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ExpansionRisk:
        if composite >= 60:
            return ExpansionRisk.critical
        if composite >= 40:
            return ExpansionRisk.high
        if composite >= 20:
            return ExpansionRisk.moderate
        return ExpansionRisk.low

    def _severity(self, composite: float) -> ExpansionSeverity:
        if composite >= 60:
            return ExpansionSeverity.stagnant
        if composite >= 40:
            return ExpansionSeverity.declining
        if composite >= 20:
            return ExpansionSeverity.steady
        return ExpansionSeverity.growing

    def _action(self, risk: ExpansionRisk, pattern: ExpansionPattern) -> ExpansionAction:
        if risk == ExpansionRisk.critical:
            if pattern == ExpansionPattern.renewal_risk:
                return ExpansionAction.renewal_acceleration
            if pattern == ExpansionPattern.executive_gap:
                return ExpansionAction.executive_alignment
            return ExpansionAction.expansion_outreach
        if risk == ExpansionRisk.high:
            if pattern == ExpansionPattern.cross_sell_neglect:
                return ExpansionAction.cross_sell_campaign
            if pattern == ExpansionPattern.low_penetration:
                return ExpansionAction.penetration_deepening
            return ExpansionAction.expansion_outreach
        if risk == ExpansionRisk.moderate:
            return ExpansionAction.expansion_outreach
        return ExpansionAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_expansion_gap(self, composite: float,
                            inp: AccountExpansionInput) -> bool:
        return (
            composite >= 40
            or (inp.expansion_ready_accounts >= 3 and inp.expansion_deals_closed == 0)
            or inp.net_revenue_retention_pct < 0.90
        )

    def _requires_account_review(self, composite: float,
                                  inp: AccountExpansionInput) -> bool:
        return (
            composite >= 30
            or inp.account_health_avg_score < 6.0
            or inp.accounts_at_contract_renewal_90d >= 3
        )

    # ------------------------------------------------------------------
    # Revenue upside
    # ------------------------------------------------------------------

    def _estimated_revenue_upside(self, inp: AccountExpansionInput,
                                   composite: float) -> float:
        return round(
            (inp.expansion_ready_accounts - inp.expansion_deals_closed)
            * inp.avg_contract_value_usd
            * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: AccountExpansionInput,
                 pattern: ExpansionPattern, composite: float) -> str:
        if pattern == ExpansionPattern.none and composite < 20:
            return "Account expansion momentum strong across portfolio"
        parts: list[str] = []
        if inp.expansion_ready_accounts > inp.expansion_deals_closed:
            missed = inp.expansion_ready_accounts - inp.expansion_deals_closed
            parts.append(f"{missed} untapped expansion accounts")
        if inp.cross_sell_opportunities_identified > inp.cross_sell_opportunities_pursued:
            missed_x = inp.cross_sell_opportunities_identified - inp.cross_sell_opportunities_pursued
            parts.append(f"{missed_x} cross-sell opportunities ignored")
        if inp.accounts_at_contract_renewal_90d > inp.renewal_expansions_secured_count:
            at_risk = inp.accounts_at_contract_renewal_90d - inp.renewal_expansions_secured_count
            parts.append(f"{at_risk} renewals unsecured")
        label = pattern.value.replace("_", " ") if pattern != ExpansionPattern.none else "Expansion risk"
        summary = " — ".join(parts) if parts else "expansion momentum slowing"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: AccountExpansionInput) -> AccountExpansionResult:
        capture     = round(self._expansion_capture_score(inp), 1)
        penetration = round(self._portfolio_penetration_score(inp), 1)
        renewal     = round(self._renewal_health_score(inp), 1)
        executive   = round(self._executive_coverage_score(inp), 1)

        composite = round(capture * 0.30 + penetration * 0.25 + renewal * 0.25 + executive * 0.20, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, capture, penetration, renewal, executive)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_expansion_gap(composite, inp)
        review   = self._requires_account_review(composite, inp)
        upside   = self._estimated_revenue_upside(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = AccountExpansionResult(
            rep_id=inp.rep_id,
            region=inp.region,
            expansion_risk=risk,
            expansion_pattern=pattern,
            expansion_severity=severity,
            recommended_action=action,
            expansion_capture_score=capture,
            portfolio_penetration_score=penetration,
            renewal_health_score=renewal,
            executive_coverage_score=executive,
            account_expansion_composite=composite,
            has_expansion_gap=gap,
            requires_account_review=review,
            estimated_expansion_revenue_upside_usd=upside,
            expansion_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[AccountExpansionInput]) -> list[AccountExpansionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_account_expansion_composite": 0.0,
                "expansion_gap_count": 0,
                "account_review_count": 0,
                "avg_expansion_capture_score": 0.0,
                "avg_portfolio_penetration_score": 0.0,
                "avg_renewal_health_score": 0.0,
                "avg_executive_coverage_score": 0.0,
                "total_estimated_expansion_revenue_upside_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_cap = total_pen = total_ren = total_exe = total_ups = 0.0

        for r in self._results:
            risk_counts[r.expansion_risk.value]       = risk_counts.get(r.expansion_risk.value, 0) + 1
            pattern_counts[r.expansion_pattern.value] = pattern_counts.get(r.expansion_pattern.value, 0) + 1
            severity_counts[r.expansion_severity.value] = severity_counts.get(r.expansion_severity.value, 0) + 1
            action_counts[r.recommended_action.value]   = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.account_expansion_composite
            total_cap  += r.expansion_capture_score
            total_pen  += r.portfolio_penetration_score
            total_ren  += r.renewal_health_score
            total_exe  += r.executive_coverage_score
            total_ups  += r.estimated_expansion_revenue_upside_usd

        n = len(self._results)

        return {
            "total":                                        n,
            "risk_counts":                                  risk_counts,
            "pattern_counts":                               pattern_counts,
            "severity_counts":                              severity_counts,
            "action_counts":                                action_counts,
            "avg_account_expansion_composite":              round(total_comp / n, 1),
            "expansion_gap_count":                          sum(1 for r in self._results if r.has_expansion_gap),
            "account_review_count":                         sum(1 for r in self._results if r.requires_account_review),
            "avg_expansion_capture_score":                  round(total_cap / n, 1),
            "avg_portfolio_penetration_score":              round(total_pen / n, 1),
            "avg_renewal_health_score":                     round(total_ren / n, 1),
            "avg_executive_coverage_score":                 round(total_exe / n, 1),
            "total_estimated_expansion_revenue_upside_usd": round(total_ups, 2),
        }
