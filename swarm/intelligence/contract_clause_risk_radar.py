from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ClauseRiskLevel(str, Enum):
    LOW      = "low"
    MODERATE = "moderate"
    HIGH     = "high"
    CRITICAL = "critical"


class RiskyClausePattern(str, Enum):
    CLEAN               = "clean"
    LIABILITY_EXPOSURE  = "liability_exposure"
    IP_CONFLICT         = "ip_conflict"
    RENEWAL_TRAP        = "renewal_trap"
    TERMINATION_RISK    = "termination_risk"
    MULTI_CLAUSE_RISK   = "multi_clause_risk"


class NegotiationStance(str, Enum):
    ACCEPT          = "accept"
    MINOR_REVISION  = "minor_revision"
    NEGOTIATE_HARD  = "negotiate_hard"
    ESCALATE_LEGAL  = "escalate_legal"


class ContractAction(str, Enum):
    PROCEED         = "proceed"
    FLAG_FOR_REVIEW = "flag_for_review"
    REDLINE         = "redline"
    BLOCK_SIGNING   = "block_signing"


@dataclass
class ContractClauseInput:
    contract_id:                    str
    deal_name:                      str
    rep_id:                         str
    contract_value:                 float   # total contract value $
    contract_term_months:           int     # length of contract in months
    liability_cap_multiplier:       float   # cap as multiple of contract value (0=uncapped)
    unlimited_liability_clause:     int     # 1 if unlimited liability present
    indemnification_scope:          int     # 1=narrow, 2=standard, 3=broad, 4=unlimited
    ip_ownership_assigned_to_vendor: int    # 1 if all IP assigned to vendor (bad for customer)
    ip_ownership_disputed:          int     # 1 if IP ownership is unclear/disputed
    auto_renewal_days_notice:       int     # days notice to cancel before auto-renewal (0=no auto)
    auto_renewal_price_increase_pct: float  # price increase on auto-renewal (%)
    termination_for_convenience:    int     # 1 if customer can terminate anytime
    termination_notice_days:        int     # days notice required for termination
    termination_fee_pct:            float   # % of remaining contract value as termination fee
    data_portability_guaranteed:    int     # 1 if data export/portability guaranteed
    data_retention_on_exit_days:    int     # days data is retained after contract ends
    governing_law_unfavorable:      int     # 1 if governing law jurisdiction is unfavorable
    unilateral_amendment_right:     int     # 1 if vendor can change terms unilaterally
    price_lock_guaranteed:          int     # 1 if price is locked for contract term
    sla_penalty_pct:                float   # % credit for SLA breaches (0=no penalties)
    audit_rights_included:          int     # 1 if customer has audit rights


@dataclass
class ContractClauseRiskResult:
    contract_id:                str
    deal_name:                  str
    clause_risk_level:          ClauseRiskLevel
    risky_clause_pattern:       RiskyClausePattern
    negotiation_stance:         NegotiationStance
    contract_action:            ContractAction
    liability_risk_score:       float   # 0-100
    ip_risk_score:              float   # 0-100
    renewal_trap_score:         float   # 0-100
    termination_risk_score:     float   # 0-100
    clause_risk_composite:      float   # 0-100
    estimated_financial_exposure: float # $ financial exposure from clauses
    clause_negotiability_score: float   # 0-100, how negotiable the problematic clauses are
    is_high_risk_contract:      bool
    needs_legal_escalation:     bool

    def to_dict(self) -> dict:
        return {
            "contract_id":                self.contract_id,
            "deal_name":                  self.deal_name,
            "clause_risk_level":          self.clause_risk_level.value,
            "risky_clause_pattern":       self.risky_clause_pattern.value,
            "negotiation_stance":         self.negotiation_stance.value,
            "contract_action":            self.contract_action.value,
            "liability_risk_score":       self.liability_risk_score,
            "ip_risk_score":              self.ip_risk_score,
            "renewal_trap_score":         self.renewal_trap_score,
            "termination_risk_score":     self.termination_risk_score,
            "clause_risk_composite":      self.clause_risk_composite,
            "estimated_financial_exposure": self.estimated_financial_exposure,
            "clause_negotiability_score": self.clause_negotiability_score,
            "is_high_risk_contract":      self.is_high_risk_contract,
            "needs_legal_escalation":     self.needs_legal_escalation,
        }


class ContractClauseRiskRadar:
    def __init__(self) -> None:
        self._results: list[ContractClauseRiskResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, inp: ContractClauseInput) -> ContractClauseRiskResult:
        liab    = self._liability_risk_score(inp)
        ip      = self._ip_risk_score(inp)
        renewal = self._renewal_trap_score(inp)
        term    = self._termination_risk_score(inp)
        composite = self._composite(liab, ip, renewal, term)
        risk    = self._clause_risk_level(composite)
        pattern = self._risky_clause_pattern(liab, ip, renewal, term)
        stance  = self._negotiation_stance(risk)
        action  = self._contract_action(risk, composite)
        negot   = self._clause_negotiability_score(inp)
        exposure = self._financial_exposure(inp, composite)
        is_high = composite >= 55.0 or inp.unlimited_liability_clause == 1
        needs_legal = composite >= 65.0 or inp.unlimited_liability_clause == 1 or inp.ip_ownership_disputed == 1

        result = ContractClauseRiskResult(
            contract_id=inp.contract_id,
            deal_name=inp.deal_name,
            clause_risk_level=risk,
            risky_clause_pattern=pattern,
            negotiation_stance=stance,
            contract_action=action,
            liability_risk_score=liab,
            ip_risk_score=ip,
            renewal_trap_score=renewal,
            termination_risk_score=term,
            clause_risk_composite=composite,
            estimated_financial_exposure=exposure,
            clause_negotiability_score=negot,
            is_high_risk_contract=is_high,
            needs_legal_escalation=needs_legal,
        )
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[ContractClauseInput]) -> list[ContractClauseRiskResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def high_risk_contracts(self) -> list[ContractClauseRiskResult]:
        return [r for r in self._results if r.is_high_risk_contract]

    @property
    def legal_escalation_needed(self) -> list[ContractClauseRiskResult]:
        return [r for r in self._results if r.needs_legal_escalation]

    @property
    def total_financial_exposure(self) -> float:
        return round(sum(r.estimated_financial_exposure for r in self._results), 2)

    @property
    def avg_negotiability_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.clause_negotiability_score for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _liability_risk_score(self, inp: ContractClauseInput) -> float:
        score = 0.0
        # Unlimited liability is the worst (40 pts)
        if inp.unlimited_liability_clause:
            score += 40.0
        else:
            # Low multiplier cap means high exposure too
            if inp.liability_cap_multiplier == 0:
                score += 30.0  # uncapped but no explicit clause
            elif inp.liability_cap_multiplier > 5.0:
                score += 20.0
            elif inp.liability_cap_multiplier > 3.0:
                score += 10.0
        # Broad indemnification scope (up to 35)
        scope_scores = {1: 0.0, 2: 5.0, 3: 25.0, 4: 35.0}
        score += scope_scores.get(inp.indemnification_scope, 0.0)
        # Governing law in unfavorable jurisdiction (up to 15)
        if inp.governing_law_unfavorable:
            score += 15.0
        # Unilateral amendment right (up to 10)
        if inp.unilateral_amendment_right:
            score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _ip_risk_score(self, inp: ContractClauseInput) -> float:
        score = 0.0
        # IP fully assigned to vendor (up to 50)
        if inp.ip_ownership_assigned_to_vendor:
            score += 50.0
        # IP ownership disputed (up to 35)
        if inp.ip_ownership_disputed:
            score += 35.0
        # No audit rights (up to 15)
        if not inp.audit_rights_included:
            score += 15.0
        return round(max(0.0, min(100.0, score)), 1)

    def _renewal_trap_score(self, inp: ContractClauseInput) -> float:
        score = 0.0
        if inp.auto_renewal_days_notice > 0:
            # Very short notice window means trap
            if inp.auto_renewal_days_notice <= 30:
                score += 40.0
            elif inp.auto_renewal_days_notice <= 60:
                score += 25.0
            elif inp.auto_renewal_days_notice <= 90:
                score += 10.0
            # Price increase on renewal
            pct = inp.auto_renewal_price_increase_pct
            if pct >= 15.0:
                score += 40.0
            elif pct >= 10.0:
                score += 25.0
            elif pct >= 5.0:
                score += 10.0
            # Price lock not guaranteed amplifies renewal risk
            if not inp.price_lock_guaranteed:
                score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _termination_risk_score(self, inp: ContractClauseInput) -> float:
        score = 0.0
        # No termination for convenience (customer stuck)
        if not inp.termination_for_convenience:
            score += 35.0
        # Long notice period
        if inp.termination_notice_days >= 180:
            score += 30.0
        elif inp.termination_notice_days >= 90:
            score += 15.0
        # High termination fee
        fee = inp.termination_fee_pct
        if fee >= 50.0:
            score += 25.0
        elif fee >= 25.0:
            score += 15.0
        elif fee >= 10.0:
            score += 5.0
        # Poor data portability / retention
        if not inp.data_portability_guaranteed:
            score += 8.0
        if inp.data_retention_on_exit_days <= 30:
            score += 6.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(self, liab: float, ip: float, renewal: float, term: float) -> float:
        composite = liab * 0.35 + ip * 0.25 + renewal * 0.20 + term * 0.20
        return round(max(0.0, min(100.0, composite)), 1)

    def _clause_risk_level(self, composite: float) -> ClauseRiskLevel:
        if composite >= 65:
            return ClauseRiskLevel.CRITICAL
        if composite >= 45:
            return ClauseRiskLevel.HIGH
        if composite >= 25:
            return ClauseRiskLevel.MODERATE
        return ClauseRiskLevel.LOW

    def _risky_clause_pattern(
        self,
        liab: float,
        ip: float,
        renewal: float,
        term: float,
    ) -> RiskyClausePattern:
        signals = sum([liab >= 50, ip >= 50, renewal >= 50, term >= 50])
        if signals >= 2:
            return RiskyClausePattern.MULTI_CLAUSE_RISK
        if liab >= 50:
            return RiskyClausePattern.LIABILITY_EXPOSURE
        if ip >= 50:
            return RiskyClausePattern.IP_CONFLICT
        if renewal >= 50:
            return RiskyClausePattern.RENEWAL_TRAP
        if term >= 50:
            return RiskyClausePattern.TERMINATION_RISK
        return RiskyClausePattern.CLEAN

    def _negotiation_stance(self, risk: ClauseRiskLevel) -> NegotiationStance:
        if risk == ClauseRiskLevel.CRITICAL:
            return NegotiationStance.ESCALATE_LEGAL
        if risk == ClauseRiskLevel.HIGH:
            return NegotiationStance.NEGOTIATE_HARD
        if risk == ClauseRiskLevel.MODERATE:
            return NegotiationStance.MINOR_REVISION
        return NegotiationStance.ACCEPT

    def _contract_action(self, risk: ClauseRiskLevel, composite: float) -> ContractAction:
        if risk == ClauseRiskLevel.CRITICAL:
            return ContractAction.BLOCK_SIGNING
        if risk == ClauseRiskLevel.HIGH:
            return ContractAction.REDLINE
        if risk == ClauseRiskLevel.MODERATE:
            return ContractAction.FLAG_FOR_REVIEW
        return ContractAction.PROCEED

    def _clause_negotiability_score(self, inp: ContractClauseInput) -> float:
        # Higher score = more negotiable (better for customer)
        score = 50.0
        if inp.termination_for_convenience:
            score += 15.0
        if inp.price_lock_guaranteed:
            score += 10.0
        if inp.data_portability_guaranteed:
            score += 10.0
        if inp.audit_rights_included:
            score += 8.0
        if inp.sla_penalty_pct > 0:
            score += min(7.0, inp.sla_penalty_pct * 0.5)
        # Penalties for non-negotiable risks
        if inp.unlimited_liability_clause:
            score -= 30.0
        if inp.unilateral_amendment_right:
            score -= 20.0
        if inp.ip_ownership_assigned_to_vendor:
            score -= 20.0
        return round(max(0.0, min(100.0, score)), 1)

    def _financial_exposure(self, inp: ContractClauseInput, composite: float) -> float:
        base_exposure = inp.contract_value * (composite / 100.0)
        # Unlimited liability can multiply beyond contract value
        if inp.unlimited_liability_clause:
            base_exposure = max(base_exposure, inp.contract_value * 2.0)
        return round(base_exposure, 2)

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "risk_counts":                  {},
                "pattern_counts":               {},
                "stance_counts":                {},
                "action_counts":                {},
                "avg_clause_risk_composite":    0.0,
                "total_financial_exposure":     0.0,
                "high_risk_count":              0,
                "legal_escalation_count":       0,
                "avg_liability_risk_score":     0.0,
                "avg_ip_risk_score":            0.0,
                "avg_renewal_trap_score":       0.0,
                "avg_negotiability_score":      0.0,
            }

        risk_counts:    dict[str, int] = {}
        pattern_counts: dict[str, int] = {}
        stance_counts:  dict[str, int] = {}
        action_counts:  dict[str, int] = {}
        total_comp  = 0.0
        total_liab  = 0.0
        total_ip    = 0.0
        total_ren   = 0.0
        total_neg   = 0.0

        for r in self._results:
            risk_counts[r.clause_risk_level.value]      = risk_counts.get(r.clause_risk_level.value, 0) + 1
            pattern_counts[r.risky_clause_pattern.value] = pattern_counts.get(r.risky_clause_pattern.value, 0) + 1
            stance_counts[r.negotiation_stance.value]   = stance_counts.get(r.negotiation_stance.value, 0) + 1
            action_counts[r.contract_action.value]      = action_counts.get(r.contract_action.value, 0) + 1
            total_comp += r.clause_risk_composite
            total_liab += r.liability_risk_score
            total_ip   += r.ip_risk_score
            total_ren  += r.renewal_trap_score
            total_neg  += r.clause_negotiability_score

        return {
            "total":                        n,
            "risk_counts":                  risk_counts,
            "pattern_counts":               pattern_counts,
            "stance_counts":                stance_counts,
            "action_counts":                action_counts,
            "avg_clause_risk_composite":    round(total_comp / n, 1),
            "total_financial_exposure":     self.total_financial_exposure,
            "high_risk_count":              len(self.high_risk_contracts),
            "legal_escalation_count":       len(self.legal_escalation_needed),
            "avg_liability_risk_score":     round(total_liab / n, 1),
            "avg_ip_risk_score":            round(total_ip / n, 1),
            "avg_renewal_trap_score":       round(total_ren / n, 1),
            "avg_negotiability_score":      round(total_neg / n, 1),
        }
