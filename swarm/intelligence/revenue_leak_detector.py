from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LeakSeverity(str, Enum):
    CONTAINED   = "contained"
    MODERATE    = "moderate"
    SIGNIFICANT = "significant"
    CRITICAL    = "critical"


class LeakPattern(str, Enum):
    HEALTHY              = "healthy"
    DISCOUNT_CREEP       = "discount_creep"
    RENEWAL_RISK         = "renewal_risk"
    EXPANSION_STALL      = "expansion_stall"
    CHAMPION_EROSION     = "champion_erosion"
    MULTI_LEAK           = "multi_leak"


class RetentionOutlook(str, Enum):
    SECURE      = "secure"
    WATCHLIST   = "watchlist"
    AT_RISK     = "at_risk"
    CRITICAL    = "critical"


class LeakAction(str, Enum):
    MONITOR             = "monitor"
    PROTECT_EXPANSION   = "protect_expansion"
    RETENTION_PLAY      = "retention_play"
    EXECUTIVE_SAVE      = "executive_save"


@dataclass
class RevenueLeakInput:
    account_id:                     str
    account_name:                   str
    csm_id:                         str
    current_arr:                    float   # current ARR from account ($)
    arr_at_contract_start:          float   # ARR when deal was first signed ($)
    contracted_arr:                 float   # contracted ARR for current term ($)
    discount_pct_current:           float   # current discount % applied
    discount_pct_original:          float   # discount % at original deal signing
    days_to_renewal:                int     # days until renewal date
    renewal_qualified:              int     # 1 if renewal has been formally qualified
    last_expansion_days_ago:        int     # days since last upsell/expansion
    expansion_attempts_failed:      int     # # of expansion conversations that stalled
    champion_active:                int     # 1 if champion is still active/responsive
    champion_changed_last_90d:      int     # 1 if champion was replaced in last 90 days
    exec_sponsor_engaged:           int     # 1 if exec sponsor is engaged
    support_ticket_volume_30d:      int     # # of support tickets opened in last 30 days
    nps_score:                      int     # last NPS score (-100 to 100, -1 if unknown)
    product_adoption_pct:           float   # % of purchased features actually used (0-100)
    seats_utilized_pct:             float   # % of purchased seats actively used (0-100)
    multi_year_contract:            int     # 1 if multi-year contract
    competitive_displacement_risk:  int     # 1 if competitor actively pitching this account
    deal_value:                     float   # original deal value (same as arr_at_contract_start typically)


@dataclass
class RevenueLeakResult:
    account_id:             str
    account_name:           str
    leak_severity:          LeakSeverity
    leak_pattern:           LeakPattern
    retention_outlook:      RetentionOutlook
    leak_action:            LeakAction
    discount_risk_score:    float   # 0-100
    renewal_risk_score:     float   # 0-100
    expansion_health_score: float   # 0-100 (inverse: high = not stalled)
    relationship_score:     float   # 0-100
    leak_composite:         float   # 0-100, higher = more leakage risk
    estimated_arr_at_risk:  float   # $ ARR that could be lost
    arr_expansion_potential: float  # $ possible expansion ARR
    is_leaking:             bool
    needs_executive_save:   bool

    def to_dict(self) -> dict:
        return {
            "account_id":               self.account_id,
            "account_name":             self.account_name,
            "leak_severity":            self.leak_severity.value,
            "leak_pattern":             self.leak_pattern.value,
            "retention_outlook":        self.retention_outlook.value,
            "leak_action":              self.leak_action.value,
            "discount_risk_score":      self.discount_risk_score,
            "renewal_risk_score":       self.renewal_risk_score,
            "expansion_health_score":   self.expansion_health_score,
            "relationship_score":       self.relationship_score,
            "leak_composite":           self.leak_composite,
            "estimated_arr_at_risk":    self.estimated_arr_at_risk,
            "arr_expansion_potential":  self.arr_expansion_potential,
            "is_leaking":               self.is_leaking,
            "needs_executive_save":     self.needs_executive_save,
        }


class RevenueLeakDetector:
    def __init__(self) -> None:
        self._results: list[RevenueLeakResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def detect(self, inp: RevenueLeakInput) -> RevenueLeakResult:
        disc_risk   = self._discount_risk_score(inp)
        renew_risk  = self._renewal_risk_score(inp)
        exp_health  = self._expansion_health_score(inp)
        rel_score   = self._relationship_score(inp)
        composite   = self._composite(disc_risk, renew_risk, exp_health, rel_score)
        severity    = self._leak_severity(composite)
        pattern     = self._leak_pattern(disc_risk, renew_risk, exp_health, rel_score, inp)
        outlook     = self._retention_outlook(renew_risk, composite, inp)
        arr_at_risk = self._estimated_arr_at_risk(inp, composite)
        exp_potential = self._arr_expansion_potential(inp)
        is_leak     = composite >= 45.0 or inp.days_to_renewal <= 60 and renew_risk >= 50
        needs_exec  = composite >= 65.0 or (inp.champion_changed_last_90d and inp.current_arr >= 100_000)
        action      = self._leak_action(severity, needs_exec, composite)

        result = RevenueLeakResult(
            account_id=inp.account_id,
            account_name=inp.account_name,
            leak_severity=severity,
            leak_pattern=pattern,
            retention_outlook=outlook,
            leak_action=action,
            discount_risk_score=disc_risk,
            renewal_risk_score=renew_risk,
            expansion_health_score=exp_health,
            relationship_score=rel_score,
            leak_composite=composite,
            estimated_arr_at_risk=arr_at_risk,
            arr_expansion_potential=exp_potential,
            is_leaking=is_leak,
            needs_executive_save=needs_exec,
        )
        self._results.append(result)
        return result

    def detect_batch(self, inputs: list[RevenueLeakInput]) -> list[RevenueLeakResult]:
        return [self.detect(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def leaking_accounts(self) -> list[RevenueLeakResult]:
        return [r for r in self._results if r.is_leaking]

    @property
    def executive_save_queue(self) -> list[RevenueLeakResult]:
        return [r for r in self._results if r.needs_executive_save]

    @property
    def total_arr_at_risk(self) -> float:
        return round(sum(r.estimated_arr_at_risk for r in self._results), 2)

    @property
    def total_expansion_potential(self) -> float:
        return round(sum(r.arr_expansion_potential for r in self._results), 2)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _discount_risk_score(self, inp: RevenueLeakInput) -> float:
        score = 0.0
        # Discount creep: current > original
        disc_creep = inp.discount_pct_current - inp.discount_pct_original
        if disc_creep >= 20:
            score += 40.0
        elif disc_creep >= 10:
            score += 25.0
        elif disc_creep >= 5:
            score += 12.0
        # ARR compression from contract start
        if inp.arr_at_contract_start > 0:
            arr_change = (inp.current_arr - inp.arr_at_contract_start) / inp.arr_at_contract_start * 100
            if arr_change <= -20:
                score += 40.0
            elif arr_change <= -10:
                score += 25.0
            elif arr_change <= -5:
                score += 10.0
        # High absolute discount (>30% is a leaky deal by nature)
        if inp.discount_pct_current >= 40:
            score += 20.0
        elif inp.discount_pct_current >= 30:
            score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _renewal_risk_score(self, inp: RevenueLeakInput) -> float:
        score = 0.0
        # Proximity to renewal
        days = inp.days_to_renewal
        if days <= 30:
            score += 40.0
        elif days <= 60:
            score += 25.0
        elif days <= 90:
            score += 12.0
        # Not yet qualified
        if not inp.renewal_qualified and days <= 90:
            score += 20.0
        # Low product adoption
        adoption = inp.product_adoption_pct
        if adoption < 30:
            score += 20.0
        elif adoption < 50:
            score += 12.0
        # Low seat utilization
        util = inp.seats_utilized_pct
        if util < 30:
            score += 15.0
        elif util < 50:
            score += 8.0
        # NPS penalty
        nps = inp.nps_score
        if nps != -1:
            if nps <= -30:
                score += 15.0
            elif nps <= 0:
                score += 8.0
        return round(max(0.0, min(100.0, score)), 1)

    def _expansion_health_score(self, inp: RevenueLeakInput) -> float:
        # High = healthy expansion, Low = stalled/leaking expansion
        score = 100.0
        # Days since last expansion (stall signal)
        exp_days = inp.last_expansion_days_ago
        if exp_days >= 365:
            score -= 35.0
        elif exp_days >= 180:
            score -= 20.0
        elif exp_days >= 90:
            score -= 10.0
        # Failed expansion attempts
        failed = inp.expansion_attempts_failed
        if failed >= 3:
            score -= 30.0
        elif failed >= 2:
            score -= 20.0
        elif failed >= 1:
            score -= 10.0
        # Seat utilization < 70% = no room to expand
        if inp.seats_utilized_pct < 50:
            score -= 20.0
        elif inp.seats_utilized_pct < 70:
            score -= 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _relationship_score(self, inp: RevenueLeakInput) -> float:
        # High = healthy relationships, low = eroding
        score = 100.0
        if not inp.champion_active:
            score -= 30.0
        if inp.champion_changed_last_90d:
            score -= 25.0
        if not inp.exec_sponsor_engaged:
            score -= 20.0
        # Support ticket surge
        tickets = inp.support_ticket_volume_30d
        if tickets >= 10:
            score -= 20.0
        elif tickets >= 5:
            score -= 10.0
        # Competitive displacement risk
        if inp.competitive_displacement_risk:
            score -= 15.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        disc: float,
        renew: float,
        exp_health: float,
        rel: float,
    ) -> float:
        # exp_health and rel are inverted: high means healthy, so (100-score) = risk
        exp_risk = 100.0 - exp_health
        rel_risk = 100.0 - rel
        composite = disc * 0.25 + renew * 0.35 + exp_risk * 0.20 + rel_risk * 0.20
        return round(max(0.0, min(100.0, composite)), 1)

    def _leak_severity(self, composite: float) -> LeakSeverity:
        if composite >= 65:
            return LeakSeverity.CRITICAL
        if composite >= 45:
            return LeakSeverity.SIGNIFICANT
        if composite >= 25:
            return LeakSeverity.MODERATE
        return LeakSeverity.CONTAINED

    def _leak_pattern(
        self,
        disc: float,
        renew: float,
        exp_health: float,
        rel: float,
        inp: RevenueLeakInput,
    ) -> LeakPattern:
        exp_risk = 100.0 - exp_health
        rel_risk = 100.0 - rel
        signals = sum([
            disc >= 40,
            renew >= 50,
            exp_risk >= 50,
            rel_risk >= 50,
        ])
        if signals >= 3:
            return LeakPattern.MULTI_LEAK
        if rel_risk >= 60 and (inp.champion_changed_last_90d or not inp.champion_active):
            return LeakPattern.CHAMPION_EROSION
        if renew >= 55:
            return LeakPattern.RENEWAL_RISK
        if disc >= 45:
            return LeakPattern.DISCOUNT_CREEP
        if exp_risk >= 55:
            return LeakPattern.EXPANSION_STALL
        return LeakPattern.HEALTHY

    def _retention_outlook(
        self,
        renew: float,
        composite: float,
        inp: RevenueLeakInput,
    ) -> RetentionOutlook:
        if composite >= 60 or (renew >= 60 and inp.days_to_renewal <= 60):
            return RetentionOutlook.CRITICAL
        if composite >= 40 or renew >= 45:
            return RetentionOutlook.AT_RISK
        if composite >= 20:
            return RetentionOutlook.WATCHLIST
        return RetentionOutlook.SECURE

    def _estimated_arr_at_risk(self, inp: RevenueLeakInput, composite: float) -> float:
        risk_pct = composite / 100.0
        base_risk = inp.current_arr * risk_pct
        # Multi-year gives partial protection
        if inp.multi_year_contract and inp.days_to_renewal > 365:
            base_risk *= 0.3
        return round(base_risk, 2)

    def _arr_expansion_potential(self, inp: RevenueLeakInput) -> float:
        # Potential based on unused seats and adoption headroom
        seat_headroom = max(0.0, 100.0 - inp.seats_utilized_pct) / 100.0
        adoption_headroom = max(0.0, 100.0 - inp.product_adoption_pct) / 100.0
        # Simple model: headroom * current ARR * 0.5 weight
        expansion = inp.current_arr * (seat_headroom * 0.4 + adoption_headroom * 0.3)
        return round(expansion, 2)

    def _leak_action(
        self,
        severity: LeakSeverity,
        needs_exec: bool,
        composite: float,
    ) -> LeakAction:
        if needs_exec or severity == LeakSeverity.CRITICAL:
            return LeakAction.EXECUTIVE_SAVE
        if severity == LeakSeverity.SIGNIFICANT:
            return LeakAction.RETENTION_PLAY
        if severity == LeakSeverity.MODERATE:
            return LeakAction.PROTECT_EXPANSION
        return LeakAction.MONITOR

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "severity_counts":              {},
                "pattern_counts":               {},
                "outlook_counts":               {},
                "action_counts":                {},
                "avg_leak_composite":           0.0,
                "total_arr_at_risk":            0.0,
                "leaking_count":                0,
                "executive_save_count":         0,
                "avg_discount_risk_score":      0.0,
                "avg_renewal_risk_score":       0.0,
                "avg_expansion_health_score":   0.0,
                "avg_relationship_score":       0.0,
            }

        severity_counts: dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        outlook_counts:  dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = 0.0
        total_disc = 0.0
        total_renew = 0.0
        total_exp  = 0.0
        total_rel  = 0.0

        for r in self._results:
            severity_counts[r.leak_severity.value]  = severity_counts.get(r.leak_severity.value, 0) + 1
            pattern_counts[r.leak_pattern.value]    = pattern_counts.get(r.leak_pattern.value, 0) + 1
            outlook_counts[r.retention_outlook.value] = outlook_counts.get(r.retention_outlook.value, 0) + 1
            action_counts[r.leak_action.value]      = action_counts.get(r.leak_action.value, 0) + 1
            total_comp  += r.leak_composite
            total_disc  += r.discount_risk_score
            total_renew += r.renewal_risk_score
            total_exp   += r.expansion_health_score
            total_rel   += r.relationship_score

        return {
            "total":                        n,
            "severity_counts":              severity_counts,
            "pattern_counts":               pattern_counts,
            "outlook_counts":               outlook_counts,
            "action_counts":                action_counts,
            "avg_leak_composite":           round(total_comp / n, 1),
            "total_arr_at_risk":            self.total_arr_at_risk,
            "leaking_count":                len(self.leaking_accounts),
            "executive_save_count":         len(self.executive_save_queue),
            "avg_discount_risk_score":      round(total_disc / n, 1),
            "avg_renewal_risk_score":       round(total_renew / n, 1),
            "avg_expansion_health_score":   round(total_exp / n, 1),
            "avg_relationship_score":       round(total_rel / n, 1),
        }
