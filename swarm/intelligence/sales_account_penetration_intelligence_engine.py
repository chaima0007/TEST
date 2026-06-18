from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class PenetrationRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class PenetrationPattern(str, Enum):
    none                       = "none"
    whitespace_neglect         = "whitespace_neglect"
    shallow_coverage           = "shallow_coverage"
    cherry_picking             = "cherry_picking"
    churn_risk_blindness       = "churn_risk_blindness"
    expansion_stagnation       = "expansion_stagnation"


class PenetrationSeverity(str, Enum):
    optimal    = "optimal"
    developing = "developing"
    shallow    = "shallow"
    stagnant   = "stagnant"


class PenetrationAction(str, Enum):
    no_action                      = "no_action"
    territory_coverage_coaching    = "territory_coverage_coaching"
    account_prioritization_review  = "account_prioritization_review"
    strategic_account_planning     = "strategic_account_planning"
    expansion_pipeline_build       = "expansion_pipeline_build"
    executive_engagement_program   = "executive_engagement_program"


@dataclass
class AccountPenetrationInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_target_accounts: int
    accounts_with_active_opportunity_count: int
    accounts_with_multiple_contacts_count: int
    accounts_with_single_contact_count: int
    avg_contacts_per_target_account: float
    large_account_engagement_count: int
    large_account_ignored_count: int
    account_activity_days_avg: float
    accounts_with_no_activity_90d_count: int
    avg_deal_size_per_account_usd: float
    total_addressable_revenue_usd: float
    captured_revenue_pct: float
    whitespace_accounts_count: int
    expansion_attempts_count: int
    expansion_success_count: int
    account_renewal_at_risk_count: int
    competitive_accounts_touched_count: int
    executive_level_engagement_count: int
    avg_account_health_score: float


@dataclass
class AccountPenetrationResult:
    rep_id: str
    region: str
    penetration_risk: PenetrationRisk
    penetration_pattern: PenetrationPattern
    penetration_severity: PenetrationSeverity
    recommended_action: PenetrationAction
    account_coverage_score: float
    account_depth_score: float
    strategic_focus_score: float
    expansion_momentum_score: float
    account_penetration_composite: float
    has_penetration_gap: bool
    requires_account_coaching: bool
    estimated_untapped_revenue_usd: float
    penetration_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "penetration_risk":                 self.penetration_risk.value,
            "penetration_pattern":              self.penetration_pattern.value,
            "penetration_severity":             self.penetration_severity.value,
            "recommended_action":               self.recommended_action.value,
            "account_coverage_score":           self.account_coverage_score,
            "account_depth_score":              self.account_depth_score,
            "strategic_focus_score":            self.strategic_focus_score,
            "expansion_momentum_score":         self.expansion_momentum_score,
            "account_penetration_composite":    self.account_penetration_composite,
            "has_penetration_gap":              self.has_penetration_gap,
            "requires_account_coaching":        self.requires_account_coaching,
            "estimated_untapped_revenue_usd":   self.estimated_untapped_revenue_usd,
            "penetration_signal":               self.penetration_signal,
        }


class SalesAccountPenetrationIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[AccountPenetrationResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _account_coverage_score(self, inp: AccountPenetrationInput) -> float:
        score = 0.0
        total = max(inp.total_target_accounts, 1)

        pen_rate = inp.accounts_with_active_opportunity_count / total
        if pen_rate < 0.20:
            score += 40.0
        elif pen_rate < 0.35:
            score += 20.0
        elif pen_rate < 0.50:
            score += 8.0

        inactive_rate = inp.accounts_with_no_activity_90d_count / total
        if inactive_rate >= 0.50:
            score += 35.0
        elif inactive_rate >= 0.30:
            score += 18.0
        elif inactive_rate >= 0.15:
            score += 7.0

        if inp.account_activity_days_avg >= 60:
            score += 15.0
        elif inp.account_activity_days_avg >= 30:
            score += 7.0

        return min(score, 100.0)

    def _account_depth_score(self, inp: AccountPenetrationInput) -> float:
        score = 0.0
        active = max(inp.accounts_with_active_opportunity_count, 1)

        single_rate = inp.accounts_with_single_contact_count / active
        if single_rate >= 0.60:
            score += 40.0
        elif single_rate >= 0.40:
            score += 20.0
        elif single_rate >= 0.25:
            score += 8.0

        if inp.avg_contacts_per_target_account < 1.0:
            score += 30.0
        elif inp.avg_contacts_per_target_account < 1.5:
            score += 15.0
        elif inp.avg_contacts_per_target_account < 2.0:
            score += 7.0

        total = max(inp.total_target_accounts, 1)
        exec_rate = inp.executive_level_engagement_count / total
        if exec_rate < 0.10:
            score += 20.0
        elif exec_rate < 0.25:
            score += 10.0

        return min(score, 100.0)

    def _strategic_focus_score(self, inp: AccountPenetrationInput) -> float:
        score = 0.0

        large_total = max(inp.large_account_engagement_count + inp.large_account_ignored_count, 1)
        neglect_rate = inp.large_account_ignored_count / large_total
        if neglect_rate >= 0.50:
            score += 40.0
        elif neglect_rate >= 0.30:
            score += 20.0
        elif neglect_rate >= 0.15:
            score += 8.0

        if inp.captured_revenue_pct < 0.10:
            score += 35.0
        elif inp.captured_revenue_pct < 0.20:
            score += 18.0
        elif inp.captured_revenue_pct < 0.35:
            score += 7.0

        if inp.avg_account_health_score < 4.0:
            score += 20.0
        elif inp.avg_account_health_score < 6.0:
            score += 10.0

        return min(score, 100.0)

    def _expansion_momentum_score(self, inp: AccountPenetrationInput) -> float:
        score = 0.0

        if inp.expansion_attempts_count == 0:
            score += 30.0
        else:
            exp_rate = inp.expansion_success_count / inp.expansion_attempts_count
            if exp_rate < 0.20:
                score += 30.0
            elif exp_rate < 0.40:
                score += 15.0

        if inp.account_renewal_at_risk_count >= 3:
            score += 35.0
        elif inp.account_renewal_at_risk_count >= 1:
            score += 18.0

        total = max(inp.total_target_accounts, 1)
        comp_rate = inp.competitive_accounts_touched_count / total
        if comp_rate < 0.10:
            score += 25.0
        elif comp_rate < 0.20:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: AccountPenetrationInput,
                         coverage: float, depth: float,
                         strategic: float, expansion: float) -> PenetrationPattern:
        total = max(inp.total_target_accounts, 1)
        whitespace_rate = inp.whitespace_accounts_count / total
        if coverage >= 35 and whitespace_rate >= 0.50:
            return PenetrationPattern.whitespace_neglect

        if depth >= 35 and inp.avg_contacts_per_target_account < 1.5:
            return PenetrationPattern.shallow_coverage

        large_total = max(inp.large_account_engagement_count + inp.large_account_ignored_count, 1)
        neglect_rate = inp.large_account_ignored_count / large_total
        if strategic >= 35 and neglect_rate >= 0.40:
            return PenetrationPattern.cherry_picking

        if expansion >= 35 and inp.account_renewal_at_risk_count >= 2:
            return PenetrationPattern.churn_risk_blindness

        if expansion >= 25 and inp.expansion_attempts_count < 3:
            return PenetrationPattern.expansion_stagnation

        return PenetrationPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> PenetrationRisk:
        if composite >= 60:
            return PenetrationRisk.critical
        if composite >= 40:
            return PenetrationRisk.high
        if composite >= 20:
            return PenetrationRisk.moderate
        return PenetrationRisk.low

    def _severity(self, composite: float) -> PenetrationSeverity:
        if composite >= 60:
            return PenetrationSeverity.stagnant
        if composite >= 40:
            return PenetrationSeverity.shallow
        if composite >= 20:
            return PenetrationSeverity.developing
        return PenetrationSeverity.optimal

    def _action(self, risk: PenetrationRisk,
                 pattern: PenetrationPattern) -> PenetrationAction:
        if risk == PenetrationRisk.critical:
            if pattern == PenetrationPattern.whitespace_neglect:
                return PenetrationAction.executive_engagement_program
            if pattern == PenetrationPattern.cherry_picking:
                return PenetrationAction.strategic_account_planning
            return PenetrationAction.territory_coverage_coaching
        if risk == PenetrationRisk.high:
            if pattern == PenetrationPattern.churn_risk_blindness:
                return PenetrationAction.expansion_pipeline_build
            if pattern == PenetrationPattern.shallow_coverage:
                return PenetrationAction.account_prioritization_review
            return PenetrationAction.territory_coverage_coaching
        if risk == PenetrationRisk.moderate:
            return PenetrationAction.account_prioritization_review
        return PenetrationAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_penetration_gap(self, composite: float,
                              inp: AccountPenetrationInput) -> bool:
        return (
            composite >= 40
            or inp.large_account_ignored_count >= 3
            or inp.captured_revenue_pct < 0.10
        )

    def _requires_account_coaching(self, composite: float,
                                    inp: AccountPenetrationInput) -> bool:
        return (
            composite >= 30
            or inp.accounts_with_no_activity_90d_count >= 5
            or inp.avg_contacts_per_target_account < 1.0
        )

    # ------------------------------------------------------------------
    # Revenue untapped
    # ------------------------------------------------------------------

    def _estimated_untapped_revenue(self, inp: AccountPenetrationInput,
                                     composite: float) -> float:
        return round(
            inp.whitespace_accounts_count * inp.avg_deal_size_per_account_usd * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: AccountPenetrationInput,
                 pattern: PenetrationPattern, composite: float) -> str:
        if pattern == PenetrationPattern.none and composite < 20:
            return "Account penetration and territory coverage within healthy benchmarks"
        parts: list[str] = []
        total = max(inp.total_target_accounts, 1)
        pen_rate = inp.accounts_with_active_opportunity_count / total
        if pen_rate < 0.40:
            parts.append(f"{inp.accounts_with_no_activity_90d_count} inactive accounts")
        if inp.whitespace_accounts_count >= 1:
            parts.append(f"{inp.whitespace_accounts_count} whitespace accounts")
        if inp.large_account_ignored_count >= 1:
            parts.append(f"{inp.large_account_ignored_count} large accounts ignored")
        label = pattern.value.replace("_", " ") if pattern != PenetrationPattern.none else "Penetration risk"
        summary = " — ".join(parts) if parts else "territory coverage needs attention"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: AccountPenetrationInput) -> AccountPenetrationResult:
        coverage  = round(self._account_coverage_score(inp), 1)
        depth     = round(self._account_depth_score(inp), 1)
        strategic = round(self._strategic_focus_score(inp), 1)
        expansion = round(self._expansion_momentum_score(inp), 1)

        composite = round(
            coverage * 0.30 + depth * 0.30 + strategic * 0.25 + expansion * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, coverage, depth, strategic, expansion)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_penetration_gap(composite, inp)
        coaching = self._requires_account_coaching(composite, inp)
        untapped = self._estimated_untapped_revenue(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = AccountPenetrationResult(
            rep_id=inp.rep_id,
            region=inp.region,
            penetration_risk=risk,
            penetration_pattern=pattern,
            penetration_severity=severity,
            recommended_action=action,
            account_coverage_score=coverage,
            account_depth_score=depth,
            strategic_focus_score=strategic,
            expansion_momentum_score=expansion,
            account_penetration_composite=composite,
            has_penetration_gap=gap,
            requires_account_coaching=coaching,
            estimated_untapped_revenue_usd=untapped,
            penetration_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[AccountPenetrationInput]) -> list[AccountPenetrationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_account_penetration_composite": 0.0,
                "penetration_gap_count": 0,
                "account_coaching_count": 0,
                "avg_account_coverage_score": 0.0,
                "avg_account_depth_score": 0.0,
                "avg_strategic_focus_score": 0.0,
                "avg_expansion_momentum_score": 0.0,
                "total_estimated_untapped_revenue_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_cov = total_dep = total_str = total_exp = total_unt = 0.0

        for r in self._results:
            risk_counts[r.penetration_risk.value]       = risk_counts.get(r.penetration_risk.value, 0) + 1
            pattern_counts[r.penetration_pattern.value] = pattern_counts.get(r.penetration_pattern.value, 0) + 1
            severity_counts[r.penetration_severity.value] = severity_counts.get(r.penetration_severity.value, 0) + 1
            action_counts[r.recommended_action.value]     = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.account_penetration_composite
            total_cov  += r.account_coverage_score
            total_dep  += r.account_depth_score
            total_str  += r.strategic_focus_score
            total_exp  += r.expansion_momentum_score
            total_unt  += r.estimated_untapped_revenue_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_account_penetration_composite":    round(total_comp / n, 1),
            "penetration_gap_count":                sum(1 for r in self._results if r.has_penetration_gap),
            "account_coaching_count":               sum(1 for r in self._results if r.requires_account_coaching),
            "avg_account_coverage_score":           round(total_cov / n, 1),
            "avg_account_depth_score":              round(total_dep / n, 1),
            "avg_strategic_focus_score":            round(total_str / n, 1),
            "avg_expansion_momentum_score":         round(total_exp / n, 1),
            "total_estimated_untapped_revenue_usd": round(total_unt, 2),
        }
