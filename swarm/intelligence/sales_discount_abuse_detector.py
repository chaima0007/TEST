"""Sales Discount Abuse Detector — identifies reps who systematically over-discount
to close deals at the expense of margin, training customers to expect concessions
and distorting revenue quality metrics."""

from __future__ import annotations

import dataclasses
from enum import Enum


class DiscountRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class DiscountPattern(str, Enum):
    none                = "none"
    policy_breach       = "policy_breach"
    habitual_discounting = "habitual_discounting"
    dependency_pattern  = "dependency_pattern"
    unauthorized        = "unauthorized"
    margin_destruction  = "margin_destruction"


class DiscountSeverity(str, Enum):
    clean      = "clean"
    watch      = "watch"
    concerning = "concerning"
    abusive    = "abusive"


class DiscountAction(str, Enum):
    no_action          = "no_action"
    flag_for_review    = "flag_for_review"
    manager_approval   = "manager_approval"
    discount_freeze    = "discount_freeze"
    compensation_review = "compensation_review"


@dataclasses.dataclass
class SalesDiscountAbuseInput:
    rep_id:                             str
    region:                             str
    period_id:                          str
    deals_closed_count:                 int
    avg_discount_pct:                   float
    company_avg_discount_pct:           float
    deals_above_policy_count:           int
    max_discount_pct:                   float
    policy_max_discount_pct:            float
    discount_requested_by_rep_count:    int
    deal_value_usd_total:               float
    revenue_at_risk_from_discount_usd:  float
    competitive_pressure_deals_count:   int
    manager_approved_exceptions_count:  int
    unauthorized_discount_count:        int
    discount_trend_delta_pct:           float
    avg_deal_cycle_days:                float
    company_avg_deal_cycle_days:        float
    win_rate_with_discount_pct:         float
    win_rate_without_discount_pct:      float
    rep_quota_attainment_pct:           float
    repeat_discount_customer_count:     int


@dataclasses.dataclass
class SalesDiscountAbuseResult:
    rep_id:                   str
    region:                   str
    discount_risk:            DiscountRisk
    discount_pattern:         DiscountPattern
    discount_severity:        DiscountSeverity
    recommended_action:       DiscountAction
    policy_violation_score:   float
    revenue_impact_score:     float
    behavioral_pattern_score: float
    dependency_score:         float
    discount_composite:       float
    is_abusing_discounts:     bool
    requires_manager_review:  bool
    estimated_margin_loss_usd: float
    discount_signal:          str

    def to_dict(self) -> dict:
        return {
            "rep_id":                    self.rep_id,
            "region":                    self.region,
            "discount_risk":             self.discount_risk.value,
            "discount_pattern":          self.discount_pattern.value,
            "discount_severity":         self.discount_severity.value,
            "recommended_action":        self.recommended_action.value,
            "policy_violation_score":    round(self.policy_violation_score, 1),
            "revenue_impact_score":      round(self.revenue_impact_score, 1),
            "behavioral_pattern_score":  round(self.behavioral_pattern_score, 1),
            "dependency_score":          round(self.dependency_score, 1),
            "discount_composite":        round(self.discount_composite, 1),
            "is_abusing_discounts":      self.is_abusing_discounts,
            "requires_manager_review":   self.requires_manager_review,
            "estimated_margin_loss_usd": round(self.estimated_margin_loss_usd, 2),
            "discount_signal":           self.discount_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesDiscountAbuseDetector:
    """Detects systematic discount abuse in sales rep behavior."""

    def __init__(self) -> None:
        self._results: list[SalesDiscountAbuseResult] = []

    # ── sub-scores (HIGHER = more abuse) ────────────────────────────────────

    def _policy_violation_score(self, inp: SalesDiscountAbuseInput) -> float:
        score = 0.0
        # Unauthorized discounts
        if inp.unauthorized_discount_count >= 5:
            score += 50.0
        elif inp.unauthorized_discount_count >= 3:
            score += 35.0
        elif inp.unauthorized_discount_count >= 1:
            score += 18.0
        # Deals above policy threshold
        if inp.deals_closed_count > 0:
            above_policy_ratio = inp.deals_above_policy_count / inp.deals_closed_count
            if above_policy_ratio >= 0.6:
                score += 30.0
            elif above_policy_ratio >= 0.4:
                score += 18.0
            elif above_policy_ratio >= 0.2:
                score += 8.0
        # Max discount vs policy ceiling
        if inp.policy_max_discount_pct > 0:
            max_excess = inp.max_discount_pct - inp.policy_max_discount_pct
            if max_excess >= 20:
                score += 20.0
            elif max_excess >= 10:
                score += 12.0
            elif max_excess >= 5:
                score += 5.0
        return _clamp(score)

    def _revenue_impact_score(self, inp: SalesDiscountAbuseInput) -> float:
        score = 0.0
        # Avg discount vs company avg
        excess_avg = inp.avg_discount_pct - inp.company_avg_discount_pct
        if excess_avg >= 15:
            score += 40.0
        elif excess_avg >= 10:
            score += 25.0
        elif excess_avg >= 5:
            score += 12.0
        # Revenue at risk as pct of total deal value
        if inp.deal_value_usd_total > 0:
            risk_ratio = inp.revenue_at_risk_from_discount_usd / inp.deal_value_usd_total
            if risk_ratio >= 0.25:
                score += 30.0
            elif risk_ratio >= 0.15:
                score += 18.0
            elif risk_ratio >= 0.08:
                score += 8.0
        # Worsening discount trend
        if inp.discount_trend_delta_pct >= 10:
            score += 20.0
        elif inp.discount_trend_delta_pct >= 5:
            score += 10.0
        return _clamp(score)

    def _behavioral_pattern_score(self, inp: SalesDiscountAbuseInput) -> float:
        score = 0.0
        # Rep initiates discounts vs customer requests
        if inp.deals_closed_count > 0 and inp.discount_requested_by_rep_count > 0:
            rep_initiation_ratio = inp.discount_requested_by_rep_count / inp.deals_closed_count
            if rep_initiation_ratio >= 0.7:
                score += 35.0
            elif rep_initiation_ratio >= 0.5:
                score += 22.0
            elif rep_initiation_ratio >= 0.3:
                score += 10.0
        # Discounting much faster than avg (using discount as shortcut)
        if inp.company_avg_deal_cycle_days > 0:
            speed_ratio = inp.avg_deal_cycle_days / inp.company_avg_deal_cycle_days
            if speed_ratio < 0.5 and inp.avg_discount_pct > inp.company_avg_discount_pct + 5:
                score += 25.0
            elif speed_ratio < 0.7 and inp.avg_discount_pct > inp.company_avg_discount_pct + 3:
                score += 12.0
        # Manager exceptions used as cover
        if inp.manager_approved_exceptions_count >= 5:
            score += 20.0
        elif inp.manager_approved_exceptions_count >= 3:
            score += 12.0
        elif inp.manager_approved_exceptions_count >= 1:
            score += 5.0
        return _clamp(score)

    def _dependency_score(self, inp: SalesDiscountAbuseInput) -> float:
        score = 0.0
        # Win rate gap: much higher with discount (trained customers to expect it)
        win_gap = inp.win_rate_with_discount_pct - inp.win_rate_without_discount_pct
        if win_gap >= 40:
            score += 40.0
        elif win_gap >= 25:
            score += 25.0
        elif win_gap >= 15:
            score += 12.0
        # Repeat discount customers (stickiness to concessions)
        if inp.repeat_discount_customer_count >= 5:
            score += 30.0
        elif inp.repeat_discount_customer_count >= 3:
            score += 18.0
        elif inp.repeat_discount_customer_count >= 1:
            score += 8.0
        # High quota attainment driven by discounting
        if inp.rep_quota_attainment_pct >= 140 and inp.avg_discount_pct > inp.company_avg_discount_pct + 8:
            score += 20.0
        elif inp.rep_quota_attainment_pct >= 120 and inp.avg_discount_pct > inp.company_avg_discount_pct + 5:
            score += 10.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> DiscountRisk:
        if composite < 20:
            return DiscountRisk.low
        if composite < 40:
            return DiscountRisk.moderate
        if composite < 60:
            return DiscountRisk.high
        return DiscountRisk.critical

    def _classify_severity(self, composite: float) -> DiscountSeverity:
        if composite < 20:
            return DiscountSeverity.clean
        if composite < 40:
            return DiscountSeverity.watch
        if composite < 60:
            return DiscountSeverity.concerning
        return DiscountSeverity.abusive

    def _classify_pattern(
        self,
        inp: SalesDiscountAbuseInput,
        policy: float,
        revenue: float,
        behavioral: float,
        dependency: float,
    ) -> DiscountPattern:
        if inp.unauthorized_discount_count >= 3:
            return DiscountPattern.unauthorized
        if revenue >= 50 and inp.avg_discount_pct > inp.company_avg_discount_pct + 12:
            return DiscountPattern.margin_destruction
        if inp.deals_above_policy_count >= 5:
            return DiscountPattern.policy_breach
        win_gap = inp.win_rate_with_discount_pct - inp.win_rate_without_discount_pct
        if win_gap >= 30 and inp.repeat_discount_customer_count >= 3:
            return DiscountPattern.dependency_pattern
        if inp.discount_requested_by_rep_count > 0 and inp.deals_closed_count > 0:
            if inp.discount_requested_by_rep_count / inp.deals_closed_count >= 0.5:
                return DiscountPattern.habitual_discounting
        return DiscountPattern.none

    def _recommended_action(
        self, risk: DiscountRisk, composite: float
    ) -> DiscountAction:
        if composite >= 60:
            return DiscountAction.compensation_review
        if risk == DiscountRisk.high:
            return DiscountAction.discount_freeze
        if risk == DiscountRisk.moderate:
            return DiscountAction.manager_approval
        if composite >= 10:
            return DiscountAction.flag_for_review
        return DiscountAction.no_action

    def _signal(
        self,
        pattern: DiscountPattern,
        composite: float,
        inp: SalesDiscountAbuseInput,
    ) -> str:
        if pattern == DiscountPattern.none:
            return "discount behavior within policy norms"
        msgs = {
            DiscountPattern.policy_breach: (
                f"{inp.deals_above_policy_count}/{inp.deals_closed_count} deals above policy threshold"
            ),
            DiscountPattern.habitual_discounting: (
                f"rep initiated discounts in {inp.discount_requested_by_rep_count}/{inp.deals_closed_count} deals"
            ),
            DiscountPattern.dependency_pattern: (
                f"win rate gap {inp.win_rate_with_discount_pct:.0f}% vs "
                f"{inp.win_rate_without_discount_pct:.0f}% — {inp.repeat_discount_customer_count} repeat discount customers"
            ),
            DiscountPattern.unauthorized: (
                f"{inp.unauthorized_discount_count} unauthorized discount(s) — "
                f"avg {inp.avg_discount_pct:.1f}% vs policy {inp.policy_max_discount_pct:.1f}%"
            ),
            DiscountPattern.margin_destruction: (
                f"avg discount {inp.avg_discount_pct:.1f}% vs company avg {inp.company_avg_discount_pct:.1f}% "
                f"(+{inp.avg_discount_pct - inp.company_avg_discount_pct:.1f}pts)"
            ),
        }
        base = msgs.get(pattern, f"discount abuse composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: SalesDiscountAbuseInput) -> SalesDiscountAbuseResult:
        policy     = self._policy_violation_score(inp)
        revenue    = self._revenue_impact_score(inp)
        behavioral = self._behavioral_pattern_score(inp)
        dependency = self._dependency_score(inp)

        composite = _clamp(
            policy     * 0.35
            + revenue    * 0.30
            + behavioral * 0.20
            + dependency * 0.15
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp, policy, revenue, behavioral, dependency)
        action   = self._recommended_action(risk, composite)

        is_abusing_discounts = (
            composite >= 40
            or inp.unauthorized_discount_count >= 3
            or (inp.policy_max_discount_pct > 0 and inp.avg_discount_pct > inp.policy_max_discount_pct * 1.5)
        )
        requires_manager_review = (
            composite >= 30
            or inp.unauthorized_discount_count >= 2
            or inp.deals_above_policy_count >= 5
        )

        estimated_margin_loss_usd = inp.revenue_at_risk_from_discount_usd * (composite / 100.0)

        result = SalesDiscountAbuseResult(
            rep_id=inp.rep_id,
            region=inp.region,
            discount_risk=risk,
            discount_pattern=pattern,
            discount_severity=severity,
            recommended_action=action,
            policy_violation_score=policy,
            revenue_impact_score=revenue,
            behavioral_pattern_score=behavioral,
            dependency_score=dependency,
            discount_composite=composite,
            is_abusing_discounts=is_abusing_discounts,
            requires_manager_review=requires_manager_review,
            estimated_margin_loss_usd=estimated_margin_loss_usd,
            discount_signal=self._signal(pattern, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[SalesDiscountAbuseInput]
    ) -> list[SalesDiscountAbuseResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                         0,
                "risk_counts":                   {},
                "pattern_counts":                {},
                "severity_counts":               {},
                "action_counts":                 {},
                "avg_discount_composite":        0.0,
                "abusing_count":                 0,
                "review_required_count":         0,
                "avg_policy_violation_score":    0.0,
                "avg_revenue_impact_score":      0.0,
                "avg_behavioral_pattern_score":  0.0,
                "avg_dependency_score":          0.0,
                "total_estimated_margin_loss_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_pol = total_rev = total_beh = total_dep = total_loss = 0.0
        abusing = review = 0

        for r in self._results:
            risk_counts[r.discount_risk.value]       = risk_counts.get(r.discount_risk.value, 0) + 1
            pattern_counts[r.discount_pattern.value] = pattern_counts.get(r.discount_pattern.value, 0) + 1
            severity_counts[r.discount_severity.value] = severity_counts.get(r.discount_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.discount_composite
            total_pol  += r.policy_violation_score
            total_rev  += r.revenue_impact_score
            total_beh  += r.behavioral_pattern_score
            total_dep  += r.dependency_score
            total_loss += r.estimated_margin_loss_usd
            if r.is_abusing_discounts:
                abusing += 1
            if r.requires_manager_review:
                review += 1

        n = len(self._results)
        return {
            "total":                           n,
            "risk_counts":                     risk_counts,
            "pattern_counts":                  pattern_counts,
            "severity_counts":                 severity_counts,
            "action_counts":                   action_counts,
            "avg_discount_composite":          round(total_comp / n, 1),
            "abusing_count":                   abusing,
            "review_required_count":           review,
            "avg_policy_violation_score":      round(total_pol  / n, 1),
            "avg_revenue_impact_score":        round(total_rev  / n, 1),
            "avg_behavioral_pattern_score":    round(total_beh  / n, 1),
            "avg_dependency_score":            round(total_dep  / n, 1),
            "total_estimated_margin_loss_usd": round(total_loss, 2),
        }
