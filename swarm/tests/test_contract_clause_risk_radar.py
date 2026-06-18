"""
Comprehensive pytest tests for ContractClauseRiskRadar (Module 71).

Coverage:
- All enums (values, membership)
- Field counts: 22 input fields, 15 to_dict keys, 13 summary keys
- Each scoring function boundary cases
- Composite weight verification
- Risk level thresholds (exact boundaries)
- Pattern priority ordering
- Stance / action mapping
- is_high_risk / needs_legal conditions
- Negotiability formula
- Financial exposure (base and unlimited liability branch)
- analyze / analyze_batch / reset
- Properties: high_risk_contracts, legal_escalation_needed,
  total_financial_exposure, avg_negotiability_score
- End-to-end scenarios
- Edge cases and cross-validation
"""
from __future__ import annotations

import dataclasses
import math

import pytest

from swarm.intelligence.contract_clause_risk_radar import (
    ClauseRiskLevel,
    ContractAction,
    ContractClauseInput,
    ContractClauseRiskRadar,
    ContractClauseRiskResult,
    NegotiationStance,
    RiskyClausePattern,
)

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _base(**overrides) -> ContractClauseInput:
    """Return a minimal 'clean' contract; override any fields via kwargs."""
    defaults = dict(
        contract_id="C-001",
        deal_name="Test Deal",
        rep_id="REP-1",
        contract_value=100_000.0,
        contract_term_months=12,
        liability_cap_multiplier=1.0,
        unlimited_liability_clause=0,
        indemnification_scope=1,
        ip_ownership_assigned_to_vendor=0,
        ip_ownership_disputed=0,
        auto_renewal_days_notice=0,
        auto_renewal_price_increase_pct=0.0,
        termination_for_convenience=1,
        termination_notice_days=30,
        termination_fee_pct=0.0,
        data_portability_guaranteed=1,
        data_retention_on_exit_days=90,
        governing_law_unfavorable=0,
        unilateral_amendment_right=0,
        price_lock_guaranteed=1,
        sla_penalty_pct=0.0,
        audit_rights_included=1,
    )
    defaults.update(overrides)
    return ContractClauseInput(**defaults)


@pytest.fixture
def radar():
    return ContractClauseRiskRadar()


# ===========================================================================
# 1. ENUM TESTS
# ===========================================================================

class TestClauseRiskLevel:
    def test_low_value(self):
        assert ClauseRiskLevel.LOW.value == "low"

    def test_moderate_value(self):
        assert ClauseRiskLevel.MODERATE.value == "moderate"

    def test_high_value(self):
        assert ClauseRiskLevel.HIGH.value == "high"

    def test_critical_value(self):
        assert ClauseRiskLevel.CRITICAL.value == "critical"

    def test_count(self):
        assert len(ClauseRiskLevel) == 4

    def test_membership(self):
        for v in ("low", "moderate", "high", "critical"):
            assert ClauseRiskLevel(v) in ClauseRiskLevel

    def test_is_str(self):
        assert isinstance(ClauseRiskLevel.LOW, str)


class TestRiskyClausePattern:
    def test_clean_value(self):
        assert RiskyClausePattern.CLEAN.value == "clean"

    def test_liability_exposure_value(self):
        assert RiskyClausePattern.LIABILITY_EXPOSURE.value == "liability_exposure"

    def test_ip_conflict_value(self):
        assert RiskyClausePattern.IP_CONFLICT.value == "ip_conflict"

    def test_renewal_trap_value(self):
        assert RiskyClausePattern.RENEWAL_TRAP.value == "renewal_trap"

    def test_termination_risk_value(self):
        assert RiskyClausePattern.TERMINATION_RISK.value == "termination_risk"

    def test_multi_clause_risk_value(self):
        assert RiskyClausePattern.MULTI_CLAUSE_RISK.value == "multi_clause_risk"

    def test_count(self):
        assert len(RiskyClausePattern) == 6

    def test_is_str(self):
        assert isinstance(RiskyClausePattern.CLEAN, str)


class TestNegotiationStance:
    def test_accept_value(self):
        assert NegotiationStance.ACCEPT.value == "accept"

    def test_minor_revision_value(self):
        assert NegotiationStance.MINOR_REVISION.value == "minor_revision"

    def test_negotiate_hard_value(self):
        assert NegotiationStance.NEGOTIATE_HARD.value == "negotiate_hard"

    def test_escalate_legal_value(self):
        assert NegotiationStance.ESCALATE_LEGAL.value == "escalate_legal"

    def test_count(self):
        assert len(NegotiationStance) == 4

    def test_is_str(self):
        assert isinstance(NegotiationStance.ACCEPT, str)


class TestContractAction:
    def test_proceed_value(self):
        assert ContractAction.PROCEED.value == "proceed"

    def test_flag_for_review_value(self):
        assert ContractAction.FLAG_FOR_REVIEW.value == "flag_for_review"

    def test_redline_value(self):
        assert ContractAction.REDLINE.value == "redline"

    def test_block_signing_value(self):
        assert ContractAction.BLOCK_SIGNING.value == "block_signing"

    def test_count(self):
        assert len(ContractAction) == 4

    def test_is_str(self):
        assert isinstance(ContractAction.PROCEED, str)


# ===========================================================================
# 2. FIELD COUNT TESTS
# ===========================================================================

class TestFieldCounts:
    def test_input_has_22_fields(self):
        fields = dataclasses.fields(ContractClauseInput)
        assert len(fields) == 22

    def test_input_field_names(self):
        expected = {
            "contract_id", "deal_name", "rep_id", "contract_value",
            "contract_term_months", "liability_cap_multiplier",
            "unlimited_liability_clause", "indemnification_scope",
            "ip_ownership_assigned_to_vendor", "ip_ownership_disputed",
            "auto_renewal_days_notice", "auto_renewal_price_increase_pct",
            "termination_for_convenience", "termination_notice_days",
            "termination_fee_pct", "data_portability_guaranteed",
            "data_retention_on_exit_days", "governing_law_unfavorable",
            "unilateral_amendment_right", "price_lock_guaranteed",
            "sla_penalty_pct", "audit_rights_included",
        }
        actual = {f.name for f in dataclasses.fields(ContractClauseInput)}
        assert actual == expected

    def test_result_to_dict_has_15_keys(self, radar):
        result = radar.analyze(_base())
        d = result.to_dict()
        assert len(d) == 15

    def test_result_to_dict_key_names(self, radar):
        expected = {
            "contract_id", "deal_name", "clause_risk_level",
            "risky_clause_pattern", "negotiation_stance", "contract_action",
            "liability_risk_score", "ip_risk_score", "renewal_trap_score",
            "termination_risk_score", "clause_risk_composite",
            "estimated_financial_exposure", "clause_negotiability_score",
            "is_high_risk_contract", "needs_legal_escalation",
        }
        result = radar.analyze(_base())
        assert set(result.to_dict().keys()) == expected

    def test_summary_has_13_keys(self, radar):
        radar.analyze(_base())
        s = radar.summary()
        assert len(s) == 13

    def test_summary_key_names(self, radar):
        radar.analyze(_base())
        expected = {
            "total", "risk_counts", "pattern_counts", "stance_counts",
            "action_counts", "avg_clause_risk_composite",
            "total_financial_exposure", "high_risk_count",
            "legal_escalation_count", "avg_liability_risk_score",
            "avg_ip_risk_score", "avg_renewal_trap_score",
            "avg_negotiability_score",
        }
        assert set(radar.summary().keys()) == expected

    def test_empty_summary_has_13_keys(self, radar):
        s = radar.summary()
        assert len(s) == 13

    def test_result_has_15_dataclass_fields(self):
        fields = dataclasses.fields(ContractClauseRiskResult)
        assert len(fields) == 15


# ===========================================================================
# 3. LIABILITY RISK SCORE
# ===========================================================================

class TestLiabilityRiskScore:
    def _score(self, **kw):
        r = ContractClauseRiskRadar()
        return r._liability_risk_score(_base(**kw))

    # unlimited liability clause branch
    def test_unlimited_liability_adds_40(self):
        s = self._score(unlimited_liability_clause=1, indemnification_scope=1,
                        governing_law_unfavorable=0, unilateral_amendment_right=0)
        assert s == 40.0

    def test_unlimited_liability_with_scope4(self):
        s = self._score(unlimited_liability_clause=1, indemnification_scope=4,
                        governing_law_unfavorable=0, unilateral_amendment_right=0)
        assert s == 75.0  # 40 + 35

    def test_unlimited_liability_with_all_extras(self):
        s = self._score(unlimited_liability_clause=1, indemnification_scope=4,
                        governing_law_unfavorable=1, unilateral_amendment_right=1)
        assert s == 100.0  # 40+35+15+10 = 100 => cap

    # cap_multiplier == 0 branch (no explicit clause)
    def test_cap_mult_zero_adds_30(self):
        s = self._score(unlimited_liability_clause=0, liability_cap_multiplier=0.0,
                        indemnification_scope=1, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 30.0

    # cap_multiplier > 5.0 adds 20
    def test_cap_mult_gt5_adds_20(self):
        s = self._score(unlimited_liability_clause=0, liability_cap_multiplier=5.1,
                        indemnification_scope=1, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 20.0

    def test_cap_mult_exactly_5_not_gt5(self):
        # 5.0 is not > 5.0 and not > 3.0 via elif chain (no, 5.0 > 3.0)
        s = self._score(unlimited_liability_clause=0, liability_cap_multiplier=5.0,
                        indemnification_scope=1, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 10.0  # 5.0 > 3.0 → +10

    def test_cap_mult_gt3_adds_10(self):
        s = self._score(unlimited_liability_clause=0, liability_cap_multiplier=3.1,
                        indemnification_scope=1, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 10.0

    def test_cap_mult_exactly_3_adds_nothing(self):
        s = self._score(unlimited_liability_clause=0, liability_cap_multiplier=3.0,
                        indemnification_scope=1, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 0.0

    def test_cap_mult_1_adds_nothing(self):
        s = self._score(unlimited_liability_clause=0, liability_cap_multiplier=1.0,
                        indemnification_scope=1, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 0.0

    # indemnification_scope branches
    def test_scope_1_adds_0(self):
        s = self._score(indemnification_scope=1, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 0.0

    def test_scope_2_adds_5(self):
        s = self._score(indemnification_scope=2, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 5.0

    def test_scope_3_adds_25(self):
        s = self._score(indemnification_scope=3, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 25.0

    def test_scope_4_adds_35(self):
        s = self._score(indemnification_scope=4, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 35.0

    def test_unknown_scope_adds_0(self):
        s = self._score(indemnification_scope=99, governing_law_unfavorable=0,
                        unilateral_amendment_right=0)
        assert s == 0.0

    # governing_law_unfavorable
    def test_governing_law_unfavorable_adds_15(self):
        s = self._score(governing_law_unfavorable=1, unilateral_amendment_right=0,
                        indemnification_scope=1)
        assert s == 15.0

    def test_governing_law_favorable_adds_0(self):
        s = self._score(governing_law_unfavorable=0, unilateral_amendment_right=0,
                        indemnification_scope=1)
        assert s == 0.0

    # unilateral_amendment_right
    def test_unilateral_amendment_adds_10(self):
        s = self._score(unilateral_amendment_right=1, governing_law_unfavorable=0,
                        indemnification_scope=1)
        assert s == 10.0

    def test_no_unilateral_amendment_adds_0(self):
        s = self._score(unilateral_amendment_right=0, governing_law_unfavorable=0,
                        indemnification_scope=1)
        assert s == 0.0

    # cap
    def test_score_capped_at_100(self):
        s = self._score(unlimited_liability_clause=1, indemnification_scope=4,
                        governing_law_unfavorable=1, unilateral_amendment_right=1)
        assert s == 100.0

    def test_score_not_negative(self):
        s = self._score()
        assert s >= 0.0

    # combination
    def test_cap_mult_zero_plus_scope4_plus_governing_plus_unilateral(self):
        # 30 + 35 + 15 + 10 = 90
        s = self._score(unlimited_liability_clause=0, liability_cap_multiplier=0.0,
                        indemnification_scope=4, governing_law_unfavorable=1,
                        unilateral_amendment_right=1)
        assert s == 90.0


# ===========================================================================
# 4. IP RISK SCORE
# ===========================================================================

class TestIpRiskScore:
    def _score(self, **kw):
        r = ContractClauseRiskRadar()
        return r._ip_risk_score(_base(**kw))

    def test_clean_no_audit_rights(self):
        s = self._score(ip_ownership_assigned_to_vendor=0, ip_ownership_disputed=0,
                        audit_rights_included=0)
        assert s == 15.0

    def test_clean_with_audit_rights(self):
        s = self._score(ip_ownership_assigned_to_vendor=0, ip_ownership_disputed=0,
                        audit_rights_included=1)
        assert s == 0.0

    def test_ip_assigned_adds_50(self):
        s = self._score(ip_ownership_assigned_to_vendor=1, ip_ownership_disputed=0,
                        audit_rights_included=1)
        assert s == 50.0

    def test_ip_disputed_adds_35(self):
        s = self._score(ip_ownership_assigned_to_vendor=0, ip_ownership_disputed=1,
                        audit_rights_included=1)
        assert s == 35.0

    def test_no_audit_rights_adds_15(self):
        s = self._score(ip_ownership_assigned_to_vendor=0, ip_ownership_disputed=0,
                        audit_rights_included=0)
        assert s == 15.0

    def test_all_three_signals(self):
        # 50 + 35 + 15 = 100
        s = self._score(ip_ownership_assigned_to_vendor=1, ip_ownership_disputed=1,
                        audit_rights_included=0)
        assert s == 100.0

    def test_assigned_and_disputed(self):
        # 50 + 35 = 85
        s = self._score(ip_ownership_assigned_to_vendor=1, ip_ownership_disputed=1,
                        audit_rights_included=1)
        assert s == 85.0

    def test_capped_at_100(self):
        s = self._score(ip_ownership_assigned_to_vendor=1, ip_ownership_disputed=1,
                        audit_rights_included=0)
        assert s <= 100.0

    def test_not_negative(self):
        s = self._score()
        assert s >= 0.0


# ===========================================================================
# 5. RENEWAL TRAP SCORE
# ===========================================================================

class TestRenewalTrapScore:
    def _score(self, **kw):
        r = ContractClauseRiskRadar()
        return r._renewal_trap_score(_base(**kw))

    def test_no_auto_renewal_is_zero(self):
        s = self._score(auto_renewal_days_notice=0, auto_renewal_price_increase_pct=0.0,
                        price_lock_guaranteed=1)
        assert s == 0.0

    def test_auto_renewal_notice_30_adds_40(self):
        s = self._score(auto_renewal_days_notice=30, auto_renewal_price_increase_pct=0.0,
                        price_lock_guaranteed=1)
        assert s == 40.0

    def test_auto_renewal_notice_31_adds_25(self):
        s = self._score(auto_renewal_days_notice=31, auto_renewal_price_increase_pct=0.0,
                        price_lock_guaranteed=1)
        assert s == 25.0

    def test_auto_renewal_notice_60_adds_25(self):
        s = self._score(auto_renewal_days_notice=60, auto_renewal_price_increase_pct=0.0,
                        price_lock_guaranteed=1)
        assert s == 25.0

    def test_auto_renewal_notice_61_adds_10(self):
        s = self._score(auto_renewal_days_notice=61, auto_renewal_price_increase_pct=0.0,
                        price_lock_guaranteed=1)
        assert s == 10.0

    def test_auto_renewal_notice_90_adds_10(self):
        s = self._score(auto_renewal_days_notice=90, auto_renewal_price_increase_pct=0.0,
                        price_lock_guaranteed=1)
        assert s == 10.0

    def test_auto_renewal_notice_91_adds_0_notice(self):
        # >90 adds nothing for notice; just price_lock bonus
        s = self._score(auto_renewal_days_notice=91, auto_renewal_price_increase_pct=0.0,
                        price_lock_guaranteed=1)
        assert s == 0.0

    # price increase branches
    def test_price_increase_15_adds_40(self):
        s = self._score(auto_renewal_days_notice=91, auto_renewal_price_increase_pct=15.0,
                        price_lock_guaranteed=1)
        assert s == 40.0

    def test_price_increase_10_adds_25(self):
        s = self._score(auto_renewal_days_notice=91, auto_renewal_price_increase_pct=10.0,
                        price_lock_guaranteed=1)
        assert s == 25.0

    def test_price_increase_5_adds_10(self):
        s = self._score(auto_renewal_days_notice=91, auto_renewal_price_increase_pct=5.0,
                        price_lock_guaranteed=1)
        assert s == 10.0

    def test_price_increase_below_5_adds_0(self):
        s = self._score(auto_renewal_days_notice=91, auto_renewal_price_increase_pct=4.9,
                        price_lock_guaranteed=1)
        assert s == 0.0

    # price_lock_guaranteed = 0 adds 10
    def test_no_price_lock_adds_10(self):
        s = self._score(auto_renewal_days_notice=91, auto_renewal_price_increase_pct=0.0,
                        price_lock_guaranteed=0)
        assert s == 10.0

    def test_price_lock_guaranteed_adds_0_extra(self):
        s = self._score(auto_renewal_days_notice=91, auto_renewal_price_increase_pct=0.0,
                        price_lock_guaranteed=1)
        assert s == 0.0

    # combinations
    def test_worst_case_short_notice_high_increase_no_lock(self):
        # 40 + 40 + 10 = 90
        s = self._score(auto_renewal_days_notice=30, auto_renewal_price_increase_pct=15.0,
                        price_lock_guaranteed=0)
        assert s == 90.0

    def test_capped_at_100(self):
        s = self._score(auto_renewal_days_notice=1, auto_renewal_price_increase_pct=20.0,
                        price_lock_guaranteed=0)
        assert s <= 100.0

    def test_not_negative(self):
        s = self._score()
        assert s >= 0.0


# ===========================================================================
# 6. TERMINATION RISK SCORE
# ===========================================================================

class TestTerminationRiskScore:
    def _score(self, **kw):
        r = ContractClauseRiskRadar()
        return r._termination_risk_score(_base(**kw))

    def test_clean_contract_is_zero(self):
        # termination_for_convenience=1, low notice, no fee, data ok
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=0.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 0.0

    def test_no_termination_for_convenience_adds_35(self):
        s = self._score(termination_for_convenience=0, termination_notice_days=30,
                        termination_fee_pct=0.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 35.0

    # notice days
    def test_notice_180_adds_30(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=180,
                        termination_fee_pct=0.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 30.0

    def test_notice_181_adds_30(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=181,
                        termination_fee_pct=0.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 30.0

    def test_notice_90_adds_15(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=90,
                        termination_fee_pct=0.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 15.0

    def test_notice_179_adds_15(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=179,
                        termination_fee_pct=0.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 15.0

    def test_notice_89_adds_0(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=89,
                        termination_fee_pct=0.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 0.0

    # termination fee
    def test_fee_50_adds_25(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=50.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 25.0

    def test_fee_100_adds_25(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=100.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 25.0

    def test_fee_25_adds_15(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=25.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 15.0

    def test_fee_49_adds_15(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=49.9, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 15.0

    def test_fee_10_adds_5(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=10.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 5.0

    def test_fee_9_adds_0(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=9.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=90)
        assert s == 0.0

    # data portability
    def test_no_data_portability_adds_8(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=0.0, data_portability_guaranteed=0,
                        data_retention_on_exit_days=90)
        assert s == 8.0

    # data retention <= 30 days adds 6
    def test_retention_30_adds_6(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=0.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=30)
        assert s == 6.0

    def test_retention_29_adds_6(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=0.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=29)
        assert s == 6.0

    def test_retention_31_adds_0(self):
        s = self._score(termination_for_convenience=1, termination_notice_days=30,
                        termination_fee_pct=0.0, data_portability_guaranteed=1,
                        data_retention_on_exit_days=31)
        assert s == 0.0

    def test_worst_case_combination(self):
        # 35+30+25+8+6 = 104 → capped at 100
        s = self._score(termination_for_convenience=0, termination_notice_days=180,
                        termination_fee_pct=50.0, data_portability_guaranteed=0,
                        data_retention_on_exit_days=30)
        assert s == 100.0

    def test_not_negative(self):
        s = self._score()
        assert s >= 0.0


# ===========================================================================
# 7. COMPOSITE SCORE
# ===========================================================================

class TestCompositeScore:
    def _composite(self, liab=0.0, ip=0.0, renewal=0.0, term=0.0):
        r = ContractClauseRiskRadar()
        return r._composite(liab, ip, renewal, term)

    def test_all_zero(self):
        assert self._composite() == 0.0

    def test_all_100(self):
        assert self._composite(100, 100, 100, 100) == 100.0

    def test_liability_weight_0_35(self):
        # Only liab=100 → 100*0.35 = 35
        assert self._composite(liab=100.0) == 35.0

    def test_ip_weight_0_25(self):
        assert self._composite(ip=100.0) == 25.0

    def test_renewal_weight_0_20(self):
        assert self._composite(renewal=100.0) == 20.0

    def test_termination_weight_0_20(self):
        assert self._composite(term=100.0) == 20.0

    def test_weights_sum_to_1(self):
        c = self._composite(100, 100, 100, 100)
        assert c == 100.0

    def test_composite_example(self):
        # 40*0.35 + 60*0.25 + 50*0.20 + 30*0.20 = 14+15+10+6 = 45
        c = self._composite(40, 60, 50, 30)
        assert c == pytest.approx(45.0, abs=0.2)

    def test_capped_at_100(self):
        c = self._composite(200, 200, 200, 200)
        assert c == 100.0

    def test_not_negative(self):
        c = self._composite(-10, -10, -10, -10)
        assert c == 0.0

    def test_rounding(self):
        # Should be rounded to 1 decimal
        c = self._composite(33, 33, 33, 33)
        assert c == round(c, 1)


# ===========================================================================
# 8. RISK LEVEL THRESHOLDS
# ===========================================================================

class TestRiskLevelThresholds:
    def _level(self, composite):
        r = ContractClauseRiskRadar()
        return r._clause_risk_level(composite)

    def test_zero_is_low(self):
        assert self._level(0.0) == ClauseRiskLevel.LOW

    def test_24_9_is_low(self):
        assert self._level(24.9) == ClauseRiskLevel.LOW

    def test_25_is_moderate(self):
        assert self._level(25.0) == ClauseRiskLevel.MODERATE

    def test_44_9_is_moderate(self):
        assert self._level(44.9) == ClauseRiskLevel.MODERATE

    def test_45_is_high(self):
        assert self._level(45.0) == ClauseRiskLevel.HIGH

    def test_64_9_is_high(self):
        assert self._level(64.9) == ClauseRiskLevel.HIGH

    def test_65_is_critical(self):
        assert self._level(65.0) == ClauseRiskLevel.CRITICAL

    def test_100_is_critical(self):
        assert self._level(100.0) == ClauseRiskLevel.CRITICAL


# ===========================================================================
# 9. RISKY CLAUSE PATTERN PRIORITY
# ===========================================================================

class TestRiskyClausePattern:
    def _pattern(self, liab=0.0, ip=0.0, renewal=0.0, term=0.0):
        r = ContractClauseRiskRadar()
        return r._risky_clause_pattern(liab, ip, renewal, term)

    def test_all_zero_is_clean(self):
        assert self._pattern() == RiskyClausePattern.CLEAN

    def test_all_below_50_is_clean(self):
        assert self._pattern(49, 49, 49, 49) == RiskyClausePattern.CLEAN

    # single signals
    def test_liab_50_is_liability_exposure(self):
        assert self._pattern(liab=50.0) == RiskyClausePattern.LIABILITY_EXPOSURE

    def test_liab_100_is_liability_exposure(self):
        assert self._pattern(liab=100.0) == RiskyClausePattern.LIABILITY_EXPOSURE

    def test_ip_50_is_ip_conflict(self):
        assert self._pattern(ip=50.0) == RiskyClausePattern.IP_CONFLICT

    def test_renewal_50_is_renewal_trap(self):
        assert self._pattern(renewal=50.0) == RiskyClausePattern.RENEWAL_TRAP

    def test_term_50_is_termination_risk(self):
        assert self._pattern(term=50.0) == RiskyClausePattern.TERMINATION_RISK

    # multi signals (>= 2)
    def test_liab_and_ip_is_multi(self):
        assert self._pattern(liab=50, ip=50) == RiskyClausePattern.MULTI_CLAUSE_RISK

    def test_liab_and_renewal_is_multi(self):
        assert self._pattern(liab=50, renewal=50) == RiskyClausePattern.MULTI_CLAUSE_RISK

    def test_liab_and_term_is_multi(self):
        assert self._pattern(liab=50, term=50) == RiskyClausePattern.MULTI_CLAUSE_RISK

    def test_ip_and_renewal_is_multi(self):
        assert self._pattern(ip=50, renewal=50) == RiskyClausePattern.MULTI_CLAUSE_RISK

    def test_ip_and_term_is_multi(self):
        assert self._pattern(ip=50, term=50) == RiskyClausePattern.MULTI_CLAUSE_RISK

    def test_renewal_and_term_is_multi(self):
        assert self._pattern(renewal=50, term=50) == RiskyClausePattern.MULTI_CLAUSE_RISK

    def test_all_four_is_multi(self):
        assert self._pattern(50, 50, 50, 50) == RiskyClausePattern.MULTI_CLAUSE_RISK

    # priority: multi beats single
    def test_multi_beats_single_liab(self):
        p = self._pattern(liab=100, ip=100)
        assert p == RiskyClausePattern.MULTI_CLAUSE_RISK

    # priority: liab before ip when only liab is >=50
    def test_liab_priority_over_ip(self):
        # Only liab >=50
        p = self._pattern(liab=50, ip=30)
        assert p == RiskyClausePattern.LIABILITY_EXPOSURE

    def test_ip_priority_over_renewal(self):
        p = self._pattern(ip=50, renewal=30)
        assert p == RiskyClausePattern.IP_CONFLICT

    def test_renewal_priority_over_term(self):
        p = self._pattern(renewal=50, term=30)
        assert p == RiskyClausePattern.RENEWAL_TRAP

    def test_exactly_49_each_is_clean(self):
        assert self._pattern(49.9, 49.9, 49.9, 49.9) == RiskyClausePattern.CLEAN


# ===========================================================================
# 10. NEGOTIATION STANCE MAPPING
# ===========================================================================

class TestNegotiationStanceMapping:
    def _stance(self, risk_level):
        r = ContractClauseRiskRadar()
        return r._negotiation_stance(risk_level)

    def test_critical_escalates_legal(self):
        assert self._stance(ClauseRiskLevel.CRITICAL) == NegotiationStance.ESCALATE_LEGAL

    def test_high_negotiate_hard(self):
        assert self._stance(ClauseRiskLevel.HIGH) == NegotiationStance.NEGOTIATE_HARD

    def test_moderate_minor_revision(self):
        assert self._stance(ClauseRiskLevel.MODERATE) == NegotiationStance.MINOR_REVISION

    def test_low_accept(self):
        assert self._stance(ClauseRiskLevel.LOW) == NegotiationStance.ACCEPT


# ===========================================================================
# 11. CONTRACT ACTION MAPPING
# ===========================================================================

class TestContractActionMapping:
    def _action(self, risk_level):
        r = ContractClauseRiskRadar()
        return r._contract_action(risk_level, 0.0)

    def test_critical_blocks_signing(self):
        assert self._action(ClauseRiskLevel.CRITICAL) == ContractAction.BLOCK_SIGNING

    def test_high_redline(self):
        assert self._action(ClauseRiskLevel.HIGH) == ContractAction.REDLINE

    def test_moderate_flag_for_review(self):
        assert self._action(ClauseRiskLevel.MODERATE) == ContractAction.FLAG_FOR_REVIEW

    def test_low_proceed(self):
        assert self._action(ClauseRiskLevel.LOW) == ContractAction.PROCEED


# ===========================================================================
# 12. IS_HIGH_RISK CONDITIONS
# ===========================================================================

class TestIsHighRisk:
    def test_composite_55_is_high_risk(self, radar):
        # Build a contract that produces composite >= 55
        inp = _base(unlimited_liability_clause=1, indemnification_scope=4)
        result = radar.analyze(inp)
        assert result.is_high_risk_contract is True

    def test_unlimited_liability_is_always_high_risk(self, radar):
        inp = _base(unlimited_liability_clause=1)
        result = radar.analyze(inp)
        assert result.is_high_risk_contract is True

    def test_clean_contract_is_not_high_risk(self, radar):
        result = radar.analyze(_base())
        assert result.is_high_risk_contract is False

    def test_composite_below_55_without_unlimited_not_high_risk(self, radar):
        # Force composite < 55 manually; use moderate risk input
        inp = _base(indemnification_scope=3, governing_law_unfavorable=1)
        result = radar.analyze(inp)
        # liab = 25+15 = 40; composite = 40*0.35 = 14 → not high risk
        assert not result.is_high_risk_contract

    def test_high_risk_flag_in_to_dict(self, radar):
        inp = _base(unlimited_liability_clause=1)
        result = radar.analyze(inp)
        assert result.to_dict()["is_high_risk_contract"] is True


# ===========================================================================
# 13. NEEDS_LEGAL_ESCALATION CONDITIONS
# ===========================================================================

class TestNeedsLegalEscalation:
    def test_composite_65_triggers_legal(self, radar):
        inp = _base(unlimited_liability_clause=1, indemnification_scope=4,
                    governing_law_unfavorable=1, unilateral_amendment_right=1,
                    ip_ownership_assigned_to_vendor=1,
                    auto_renewal_days_notice=30, auto_renewal_price_increase_pct=15.0,
                    price_lock_guaranteed=0,
                    termination_for_convenience=0, termination_notice_days=180,
                    termination_fee_pct=50.0, data_portability_guaranteed=0,
                    data_retention_on_exit_days=30)
        result = radar.analyze(inp)
        assert result.needs_legal_escalation is True

    def test_unlimited_liability_triggers_legal(self, radar):
        inp = _base(unlimited_liability_clause=1)
        result = radar.analyze(inp)
        assert result.needs_legal_escalation is True

    def test_ip_disputed_triggers_legal(self, radar):
        inp = _base(ip_ownership_disputed=1)
        result = radar.analyze(inp)
        assert result.needs_legal_escalation is True

    def test_clean_does_not_trigger_legal(self, radar):
        result = radar.analyze(_base())
        assert result.needs_legal_escalation is False

    def test_needs_legal_in_to_dict(self, radar):
        inp = _base(ip_ownership_disputed=1)
        result = radar.analyze(inp)
        assert result.to_dict()["needs_legal_escalation"] is True


# ===========================================================================
# 14. NEGOTIABILITY SCORE
# ===========================================================================

class TestNegotiabilityScore:
    def _negot(self, **kw):
        r = ContractClauseRiskRadar()
        return r._clause_negotiability_score(_base(**kw))

    def test_base_is_50(self):
        # All neutral (no bonuses, no penalties)
        s = self._negot(termination_for_convenience=0, price_lock_guaranteed=0,
                        data_portability_guaranteed=0, audit_rights_included=0,
                        sla_penalty_pct=0.0, unlimited_liability_clause=0,
                        unilateral_amendment_right=0, ip_ownership_assigned_to_vendor=0)
        assert s == 50.0

    def test_termination_for_convenience_adds_15(self):
        s = self._negot(termination_for_convenience=1, price_lock_guaranteed=0,
                        data_portability_guaranteed=0, audit_rights_included=0,
                        sla_penalty_pct=0.0)
        assert s == 65.0

    def test_price_lock_adds_10(self):
        s = self._negot(termination_for_convenience=0, price_lock_guaranteed=1,
                        data_portability_guaranteed=0, audit_rights_included=0,
                        sla_penalty_pct=0.0)
        assert s == 60.0

    def test_data_portability_adds_10(self):
        s = self._negot(termination_for_convenience=0, price_lock_guaranteed=0,
                        data_portability_guaranteed=1, audit_rights_included=0,
                        sla_penalty_pct=0.0)
        assert s == 60.0

    def test_audit_rights_adds_8(self):
        s = self._negot(termination_for_convenience=0, price_lock_guaranteed=0,
                        data_portability_guaranteed=0, audit_rights_included=1,
                        sla_penalty_pct=0.0)
        assert s == 58.0

    def test_sla_penalty_capped_at_7(self):
        s = self._negot(termination_for_convenience=0, price_lock_guaranteed=0,
                        data_portability_guaranteed=0, audit_rights_included=0,
                        sla_penalty_pct=20.0)  # 20*0.5=10 → capped at 7
        assert s == 57.0

    def test_sla_penalty_2_pct_adds_1(self):
        s = self._negot(termination_for_convenience=0, price_lock_guaranteed=0,
                        data_portability_guaranteed=0, audit_rights_included=0,
                        sla_penalty_pct=2.0)  # 2*0.5=1
        assert s == 51.0

    def test_sla_penalty_14_adds_7_exactly(self):
        s = self._negot(termination_for_convenience=0, price_lock_guaranteed=0,
                        data_portability_guaranteed=0, audit_rights_included=0,
                        sla_penalty_pct=14.0)  # 14*0.5=7 → min(7,7)=7
        assert s == 57.0

    def test_unlimited_liability_subtracts_30(self):
        s = self._negot(termination_for_convenience=0, price_lock_guaranteed=0,
                        data_portability_guaranteed=0, audit_rights_included=0,
                        sla_penalty_pct=0.0, unlimited_liability_clause=1)
        assert s == 20.0

    def test_unilateral_amendment_subtracts_20(self):
        s = self._negot(termination_for_convenience=0, price_lock_guaranteed=0,
                        data_portability_guaranteed=0, audit_rights_included=0,
                        sla_penalty_pct=0.0, unilateral_amendment_right=1)
        assert s == 30.0

    def test_ip_assigned_subtracts_20(self):
        s = self._negot(termination_for_convenience=0, price_lock_guaranteed=0,
                        data_portability_guaranteed=0, audit_rights_included=0,
                        sla_penalty_pct=0.0, ip_ownership_assigned_to_vendor=1)
        assert s == 30.0

    def test_all_penalties_clamped_to_0(self):
        s = self._negot(unlimited_liability_clause=1, unilateral_amendment_right=1,
                        ip_ownership_assigned_to_vendor=1, termination_for_convenience=0,
                        price_lock_guaranteed=0, data_portability_guaranteed=0,
                        audit_rights_included=0, sla_penalty_pct=0.0)
        # 50 - 30 - 20 - 20 = -20 → clamped to 0
        assert s == 0.0

    def test_all_bonuses_max_100(self):
        # 50 + 15 + 10 + 10 + 8 + 7 = 100
        s = self._negot(termination_for_convenience=1, price_lock_guaranteed=1,
                        data_portability_guaranteed=1, audit_rights_included=1,
                        sla_penalty_pct=14.0, unlimited_liability_clause=0,
                        unilateral_amendment_right=0, ip_ownership_assigned_to_vendor=0)
        assert s == 100.0

    def test_clamped_at_100(self):
        s = self._negot(termination_for_convenience=1, price_lock_guaranteed=1,
                        data_portability_guaranteed=1, audit_rights_included=1,
                        sla_penalty_pct=100.0)
        assert s <= 100.0

    def test_not_negative(self):
        s = self._negot(unlimited_liability_clause=1, unilateral_amendment_right=1,
                        ip_ownership_assigned_to_vendor=1)
        assert s >= 0.0


# ===========================================================================
# 15. FINANCIAL EXPOSURE
# ===========================================================================

class TestFinancialExposure:
    def _exposure(self, **kw):
        r = ContractClauseRiskRadar()
        inp = _base(**kw)
        composite = r._composite(
            r._liability_risk_score(inp),
            r._ip_risk_score(inp),
            r._renewal_trap_score(inp),
            r._termination_risk_score(inp),
        )
        return r._financial_exposure(inp, composite)

    def test_zero_composite_zero_exposure(self):
        e = self._exposure()
        # composite near 0, so exposure ~ 0 (could be nonzero if base scores not 0)
        assert e >= 0.0

    def test_exposure_formula(self, radar):
        inp = _base(contract_value=100_000.0, indemnification_scope=4,
                    governing_law_unfavorable=1)
        # liab = 35+15 = 50, ip=0 (audit), renewal=0, term=0
        # Actually audit_rights=1 in _base, so ip=0; renewal=0; term=0
        # composite = 50*0.35 = 17.5
        result = radar.analyze(inp)
        expected = round(100_000.0 * (result.clause_risk_composite / 100.0), 2)
        assert result.estimated_financial_exposure == pytest.approx(expected, abs=0.01)

    def test_unlimited_liability_doubles_contract_value_min(self, radar):
        inp = _base(contract_value=50_000.0, unlimited_liability_clause=1)
        result = radar.analyze(inp)
        # With unlimited: max(base, 50000*2) = max(base, 100000)
        assert result.estimated_financial_exposure >= 50_000.0 * 2.0

    def test_unlimited_liability_branch_triggered(self, radar):
        # composite may be < 200 so base < contract*2
        inp = _base(contract_value=100_000.0, unlimited_liability_clause=1)
        result = radar.analyze(inp)
        assert result.estimated_financial_exposure >= 200_000.0

    def test_exposure_rounded_to_2_decimals(self, radar):
        inp = _base(contract_value=333.33)
        result = radar.analyze(inp)
        exposure = result.estimated_financial_exposure
        assert round(exposure, 2) == exposure

    def test_large_contract_value(self, radar):
        inp = _base(contract_value=10_000_000.0, unlimited_liability_clause=1)
        result = radar.analyze(inp)
        assert result.estimated_financial_exposure >= 20_000_000.0

    def test_zero_contract_value(self, radar):
        inp = _base(contract_value=0.0, unlimited_liability_clause=1)
        result = radar.analyze(inp)
        assert result.estimated_financial_exposure == 0.0


# ===========================================================================
# 16. ANALYZE METHOD
# ===========================================================================

class TestAnalyzeMethod:
    def test_returns_result_type(self, radar):
        result = radar.analyze(_base())
        assert isinstance(result, ContractClauseRiskResult)

    def test_result_stored_in_results(self, radar):
        radar.analyze(_base())
        assert len(radar._results) == 1

    def test_multiple_analyses_accumulate(self, radar):
        for i in range(5):
            radar.analyze(_base(contract_id=f"C-{i}"))
        assert len(radar._results) == 5

    def test_contract_id_preserved(self, radar):
        result = radar.analyze(_base(contract_id="MYID-42"))
        assert result.contract_id == "MYID-42"

    def test_deal_name_preserved(self, radar):
        result = radar.analyze(_base(deal_name="My Big Deal"))
        assert result.deal_name == "My Big Deal"

    def test_all_score_fields_present(self, radar):
        result = radar.analyze(_base())
        assert hasattr(result, "liability_risk_score")
        assert hasattr(result, "ip_risk_score")
        assert hasattr(result, "renewal_trap_score")
        assert hasattr(result, "termination_risk_score")
        assert hasattr(result, "clause_risk_composite")

    def test_scores_in_valid_range(self, radar):
        inp = _base(unlimited_liability_clause=1, ip_ownership_assigned_to_vendor=1,
                    ip_ownership_disputed=1, auto_renewal_days_notice=30,
                    auto_renewal_price_increase_pct=20.0, termination_for_convenience=0,
                    termination_notice_days=200, termination_fee_pct=60.0)
        result = radar.analyze(inp)
        for score in (result.liability_risk_score, result.ip_risk_score,
                      result.renewal_trap_score, result.termination_risk_score,
                      result.clause_risk_composite):
            assert 0.0 <= score <= 100.0


# ===========================================================================
# 17. ANALYZE_BATCH METHOD
# ===========================================================================

class TestAnalyzeBatch:
    def test_returns_list(self, radar):
        results = radar.analyze_batch([_base(), _base(contract_id="C-2")])
        assert isinstance(results, list)

    def test_returns_correct_count(self, radar):
        inputs = [_base(contract_id=f"C-{i}") for i in range(7)]
        results = radar.analyze_batch(inputs)
        assert len(results) == 7

    def test_empty_batch_returns_empty(self, radar):
        results = radar.analyze_batch([])
        assert results == []

    def test_batch_accumulates_in_results(self, radar):
        radar.analyze_batch([_base(contract_id=f"C-{i}") for i in range(4)])
        assert len(radar._results) == 4

    def test_batch_order_preserved(self, radar):
        ids = [f"C-{i}" for i in range(5)]
        results = radar.analyze_batch([_base(contract_id=cid) for cid in ids])
        assert [r.contract_id for r in results] == ids

    def test_batch_plus_single_accumulate(self, radar):
        radar.analyze_batch([_base(), _base(contract_id="C-2")])
        radar.analyze(_base(contract_id="C-3"))
        assert len(radar._results) == 3


# ===========================================================================
# 18. RESET METHOD
# ===========================================================================

class TestResetMethod:
    def test_reset_clears_results(self, radar):
        radar.analyze(_base())
        radar.reset()
        assert len(radar._results) == 0

    def test_reset_empty_is_ok(self, radar):
        radar.reset()
        assert len(radar._results) == 0

    def test_reset_resets_properties(self, radar):
        radar.analyze(_base(unlimited_liability_clause=1))
        radar.reset()
        assert radar.high_risk_contracts == []

    def test_can_analyze_after_reset(self, radar):
        radar.analyze(_base())
        radar.reset()
        result = radar.analyze(_base(contract_id="NEW"))
        assert result.contract_id == "NEW"
        assert len(radar._results) == 1

    def test_reset_total_financial_exposure_zero(self, radar):
        radar.analyze(_base(contract_value=100_000.0, unlimited_liability_clause=1))
        radar.reset()
        assert radar.total_financial_exposure == 0.0


# ===========================================================================
# 19. PROPERTIES
# ===========================================================================

class TestProperties:
    def test_high_risk_contracts_empty_initially(self, radar):
        assert radar.high_risk_contracts == []

    def test_high_risk_contracts_includes_unlimited_liability(self, radar):
        radar.analyze(_base(unlimited_liability_clause=1))
        assert len(radar.high_risk_contracts) == 1

    def test_high_risk_contracts_excludes_clean(self, radar):
        radar.analyze(_base())
        assert radar.high_risk_contracts == []

    def test_high_risk_contracts_mixed(self, radar):
        radar.analyze(_base(contract_id="C-1"))  # clean
        radar.analyze(_base(contract_id="C-2", unlimited_liability_clause=1))
        assert len(radar.high_risk_contracts) == 1
        assert radar.high_risk_contracts[0].contract_id == "C-2"

    def test_legal_escalation_needed_empty_initially(self, radar):
        assert radar.legal_escalation_needed == []

    def test_legal_escalation_needed_ip_disputed(self, radar):
        radar.analyze(_base(ip_ownership_disputed=1))
        assert len(radar.legal_escalation_needed) == 1

    def test_legal_escalation_excludes_clean(self, radar):
        radar.analyze(_base())
        assert radar.legal_escalation_needed == []

    def test_total_financial_exposure_zero_initially(self, radar):
        assert radar.total_financial_exposure == 0.0

    def test_total_financial_exposure_sum(self, radar):
        r1 = radar.analyze(_base(contract_id="C-1", contract_value=100_000.0))
        r2 = radar.analyze(_base(contract_id="C-2", contract_value=200_000.0))
        expected = round(r1.estimated_financial_exposure + r2.estimated_financial_exposure, 2)
        assert radar.total_financial_exposure == expected

    def test_avg_negotiability_score_zero_initially(self, radar):
        assert radar.avg_negotiability_score == 0.0

    def test_avg_negotiability_score_single(self, radar):
        result = radar.analyze(_base())
        assert radar.avg_negotiability_score == round(result.clause_negotiability_score, 1)

    def test_avg_negotiability_score_multiple(self, radar):
        r1 = radar.analyze(_base(contract_id="C-1"))
        r2 = radar.analyze(_base(contract_id="C-2", unlimited_liability_clause=1))
        expected = round((r1.clause_negotiability_score + r2.clause_negotiability_score) / 2, 1)
        assert radar.avg_negotiability_score == expected

    def test_total_financial_exposure_rounded(self, radar):
        radar.analyze(_base(contract_value=333.33))
        exp = radar.total_financial_exposure
        assert round(exp, 2) == exp


# ===========================================================================
# 20. SUMMARY
# ===========================================================================

class TestSummary:
    def test_empty_summary_total_zero(self, radar):
        s = radar.summary()
        assert s["total"] == 0

    def test_empty_summary_all_zero(self, radar):
        s = radar.summary()
        assert s["avg_clause_risk_composite"] == 0.0
        assert s["total_financial_exposure"] == 0.0
        assert s["high_risk_count"] == 0
        assert s["legal_escalation_count"] == 0
        assert s["avg_liability_risk_score"] == 0.0
        assert s["avg_ip_risk_score"] == 0.0
        assert s["avg_renewal_trap_score"] == 0.0
        assert s["avg_negotiability_score"] == 0.0

    def test_empty_summary_dicts_empty(self, radar):
        s = radar.summary()
        assert s["risk_counts"] == {}
        assert s["pattern_counts"] == {}
        assert s["stance_counts"] == {}
        assert s["action_counts"] == {}

    def test_summary_total_count(self, radar):
        for i in range(3):
            radar.analyze(_base(contract_id=f"C-{i}"))
        assert radar.summary()["total"] == 3

    def test_summary_risk_counts_keys_are_strings(self, radar):
        radar.analyze(_base())
        s = radar.summary()
        for k in s["risk_counts"]:
            assert isinstance(k, str)

    def test_summary_risk_counts_correct(self, radar):
        radar.analyze(_base())  # low risk
        radar.analyze(_base(unlimited_liability_clause=1))  # higher risk
        s = radar.summary()
        total_in_counts = sum(s["risk_counts"].values())
        assert total_in_counts == 2

    def test_summary_pattern_counts_sum(self, radar):
        for i in range(4):
            radar.analyze(_base(contract_id=f"C-{i}"))
        s = radar.summary()
        assert sum(s["pattern_counts"].values()) == 4

    def test_summary_stance_counts_sum(self, radar):
        for i in range(3):
            radar.analyze(_base(contract_id=f"C-{i}"))
        s = radar.summary()
        assert sum(s["stance_counts"].values()) == 3

    def test_summary_action_counts_sum(self, radar):
        for i in range(5):
            radar.analyze(_base(contract_id=f"C-{i}"))
        s = radar.summary()
        assert sum(s["action_counts"].values()) == 5

    def test_summary_high_risk_count(self, radar):
        radar.analyze(_base())
        radar.analyze(_base(contract_id="C-2", unlimited_liability_clause=1))
        s = radar.summary()
        assert s["high_risk_count"] == 1

    def test_summary_legal_escalation_count(self, radar):
        radar.analyze(_base(ip_ownership_disputed=1, contract_id="C-1"))
        radar.analyze(_base(contract_id="C-2"))
        s = radar.summary()
        assert s["legal_escalation_count"] == 1

    def test_summary_avg_composite(self, radar):
        r1 = radar.analyze(_base(contract_id="C-1"))
        r2 = radar.analyze(_base(contract_id="C-2", unlimited_liability_clause=1))
        expected = round((r1.clause_risk_composite + r2.clause_risk_composite) / 2, 1)
        assert radar.summary()["avg_clause_risk_composite"] == expected

    def test_summary_avg_negotiability(self, radar):
        r1 = radar.analyze(_base(contract_id="C-1"))
        r2 = radar.analyze(_base(contract_id="C-2", unlimited_liability_clause=1))
        expected = round((r1.clause_negotiability_score + r2.clause_negotiability_score) / 2, 1)
        assert radar.summary()["avg_negotiability_score"] == expected

    def test_summary_total_financial_exposure_matches_property(self, radar):
        radar.analyze(_base(contract_value=50_000.0))
        radar.analyze(_base(contract_id="C-2", contract_value=75_000.0,
                            unlimited_liability_clause=1))
        s = radar.summary()
        assert s["total_financial_exposure"] == radar.total_financial_exposure


# ===========================================================================
# 21. TO_DICT CONTENT
# ===========================================================================

class TestToDict:
    def test_contract_id_in_dict(self, radar):
        r = radar.analyze(_base(contract_id="XYZ"))
        assert r.to_dict()["contract_id"] == "XYZ"

    def test_deal_name_in_dict(self, radar):
        r = radar.analyze(_base(deal_name="BigDeal"))
        assert r.to_dict()["deal_name"] == "BigDeal"

    def test_risk_level_is_string(self, radar):
        r = radar.analyze(_base())
        assert isinstance(r.to_dict()["clause_risk_level"], str)

    def test_pattern_is_string(self, radar):
        r = radar.analyze(_base())
        assert isinstance(r.to_dict()["risky_clause_pattern"], str)

    def test_stance_is_string(self, radar):
        r = radar.analyze(_base())
        assert isinstance(r.to_dict()["negotiation_stance"], str)

    def test_action_is_string(self, radar):
        r = radar.analyze(_base())
        assert isinstance(r.to_dict()["contract_action"], str)

    def test_risk_level_values_valid(self, radar):
        valid = {"low", "moderate", "high", "critical"}
        r = radar.analyze(_base())
        assert r.to_dict()["clause_risk_level"] in valid

    def test_pattern_values_valid(self, radar):
        valid = {"clean", "liability_exposure", "ip_conflict",
                 "renewal_trap", "termination_risk", "multi_clause_risk"}
        r = radar.analyze(_base())
        assert r.to_dict()["risky_clause_pattern"] in valid

    def test_bool_fields_are_bool(self, radar):
        r = radar.analyze(_base())
        d = r.to_dict()
        assert isinstance(d["is_high_risk_contract"], bool)
        assert isinstance(d["needs_legal_escalation"], bool)

    def test_numeric_fields_are_numeric(self, radar):
        r = radar.analyze(_base())
        d = r.to_dict()
        for key in ("liability_risk_score", "ip_risk_score", "renewal_trap_score",
                    "termination_risk_score", "clause_risk_composite",
                    "estimated_financial_exposure", "clause_negotiability_score"):
            assert isinstance(d[key], (int, float))


# ===========================================================================
# 22. END-TO-END SCENARIOS
# ===========================================================================

class TestEndToEndScenarios:
    def test_perfectly_clean_contract(self, radar):
        inp = _base(
            unlimited_liability_clause=0, liability_cap_multiplier=1.0,
            indemnification_scope=1, governing_law_unfavorable=0,
            unilateral_amendment_right=0, ip_ownership_assigned_to_vendor=0,
            ip_ownership_disputed=0, audit_rights_included=1,
            auto_renewal_days_notice=0, price_lock_guaranteed=1,
            termination_for_convenience=1, termination_notice_days=30,
            termination_fee_pct=0.0, data_portability_guaranteed=1,
            data_retention_on_exit_days=90,
        )
        result = radar.analyze(inp)
        assert result.clause_risk_level == ClauseRiskLevel.LOW
        assert result.risky_clause_pattern == RiskyClausePattern.CLEAN
        assert result.negotiation_stance == NegotiationStance.ACCEPT
        assert result.contract_action == ContractAction.PROCEED
        assert not result.is_high_risk_contract
        assert not result.needs_legal_escalation

    def test_nightmare_contract_all_bad(self, radar):
        inp = _base(
            unlimited_liability_clause=1, liability_cap_multiplier=10.0,
            indemnification_scope=4, governing_law_unfavorable=1,
            unilateral_amendment_right=1, ip_ownership_assigned_to_vendor=1,
            ip_ownership_disputed=1, audit_rights_included=0,
            auto_renewal_days_notice=15, auto_renewal_price_increase_pct=20.0,
            price_lock_guaranteed=0, termination_for_convenience=0,
            termination_notice_days=365, termination_fee_pct=75.0,
            data_portability_guaranteed=0, data_retention_on_exit_days=7,
        )
        result = radar.analyze(inp)
        assert result.clause_risk_level == ClauseRiskLevel.CRITICAL
        assert result.risky_clause_pattern == RiskyClausePattern.MULTI_CLAUSE_RISK
        assert result.negotiation_stance == NegotiationStance.ESCALATE_LEGAL
        assert result.contract_action == ContractAction.BLOCK_SIGNING
        assert result.is_high_risk_contract
        assert result.needs_legal_escalation
        assert result.clause_risk_composite >= 65.0

    def test_ip_only_conflict_scenario(self, radar):
        inp = _base(
            ip_ownership_assigned_to_vendor=1, ip_ownership_disputed=0,
            audit_rights_included=1,
        )
        result = radar.analyze(inp)
        assert result.ip_risk_score == 50.0
        assert result.risky_clause_pattern == RiskyClausePattern.IP_CONFLICT

    def test_renewal_trap_scenario(self, radar):
        inp = _base(
            auto_renewal_days_notice=15, auto_renewal_price_increase_pct=20.0,
            price_lock_guaranteed=0,
        )
        result = radar.analyze(inp)
        assert result.renewal_trap_score == 90.0
        assert result.risky_clause_pattern == RiskyClausePattern.RENEWAL_TRAP

    def test_termination_risk_scenario(self, radar):
        inp = _base(
            termination_for_convenience=0, termination_notice_days=180,
            termination_fee_pct=50.0, data_portability_guaranteed=0,
            data_retention_on_exit_days=30,
        )
        result = radar.analyze(inp)
        assert result.termination_risk_score == 100.0
        assert result.risky_clause_pattern == RiskyClausePattern.TERMINATION_RISK

    def test_liability_only_scenario(self, radar):
        inp = _base(
            unlimited_liability_clause=1, indemnification_scope=1,
            governing_law_unfavorable=0, unilateral_amendment_right=0,
        )
        result = radar.analyze(inp)
        assert result.liability_risk_score == 40.0
        # only liab >=50? No: 40 < 50. Pattern should be clean
        assert result.risky_clause_pattern == RiskyClausePattern.CLEAN

    def test_batch_mixed_contracts(self, radar):
        inputs = [
            _base(contract_id="clean"),
            _base(contract_id="risky", unlimited_liability_clause=1,
                  ip_ownership_disputed=1),
        ]
        results = radar.analyze_batch(inputs)
        clean_r = next(r for r in results if r.contract_id == "clean")
        risky_r = next(r for r in results if r.contract_id == "risky")
        assert clean_r.clause_risk_level == ClauseRiskLevel.LOW
        assert risky_r.needs_legal_escalation is True

    def test_moderate_risk_contract(self, radar):
        # Design a moderate contract: composite 25-44
        # liab: scope=3 → 25; composite = 25*0.35 = 8.75 → low actually
        # Need higher: cap_mult>5 (20) + scope=3 (25) = 45 → high
        # Let's try scope=2 (5) + governing (15) = 20 → composite = 20*0.35 = 7 → low
        # Use scope=3 (25) + governing(15) = 40 → composite = 40*0.35 = 14 → low
        # Need composite in [25,44]: set liab=70 from scope4+governing+unilateral = 35+15+10=60,
        # plus cap_mult>5 but since no unlimited that doesn't double; 60*0.35=21 →low still
        # Actually with cap_mult=0 no unlimited: 30+35+15+10=90; 90*0.35=31.5 → moderate!
        inp = _base(
            unlimited_liability_clause=0, liability_cap_multiplier=0.0,
            indemnification_scope=4, governing_law_unfavorable=1,
            unilateral_amendment_right=1,
        )
        result = radar.analyze(inp)
        assert result.clause_risk_level == ClauseRiskLevel.MODERATE
        assert result.negotiation_stance == NegotiationStance.MINOR_REVISION
        assert result.contract_action == ContractAction.FLAG_FOR_REVIEW

    def test_high_risk_contract(self, radar):
        # composite in [45,64]: liab=100*0.35=35 + ip=100*0.25=25 = 60 → high
        inp = _base(
            unlimited_liability_clause=1, indemnification_scope=4,
            governing_law_unfavorable=1, unilateral_amendment_right=1,
            ip_ownership_assigned_to_vendor=1, ip_ownership_disputed=1,
            audit_rights_included=0,
        )
        result = radar.analyze(inp)
        assert result.clause_risk_composite >= 45.0
        # Could be critical if >= 65
        assert result.clause_risk_level in (ClauseRiskLevel.HIGH, ClauseRiskLevel.CRITICAL)


# ===========================================================================
# 23. EDGE CASES
# ===========================================================================

class TestEdgeCases:
    def test_zero_contract_value_no_exposure(self, radar):
        inp = _base(contract_value=0.0)
        result = radar.analyze(inp)
        assert result.estimated_financial_exposure == 0.0

    def test_very_large_contract_value(self, radar):
        inp = _base(contract_value=1_000_000_000.0, unlimited_liability_clause=1)
        result = radar.analyze(inp)
        assert result.estimated_financial_exposure >= 2_000_000_000.0

    def test_sla_penalty_zero(self, radar):
        inp = _base(sla_penalty_pct=0.0)
        result = radar.analyze(inp)
        assert result.clause_negotiability_score >= 0.0

    def test_sla_penalty_fractional(self, radar):
        r = ContractClauseRiskRadar()
        inp = _base(sla_penalty_pct=1.0, termination_for_convenience=0,
                    price_lock_guaranteed=0, data_portability_guaranteed=0,
                    audit_rights_included=0)
        s = r._clause_negotiability_score(inp)
        assert s == pytest.approx(50.5, abs=0.1)

    def test_all_zeros_input_does_not_crash(self, radar):
        inp = ContractClauseInput(
            contract_id="Z", deal_name="Zero", rep_id="R0",
            contract_value=0.0, contract_term_months=0,
            liability_cap_multiplier=0.0, unlimited_liability_clause=0,
            indemnification_scope=1, ip_ownership_assigned_to_vendor=0,
            ip_ownership_disputed=0, auto_renewal_days_notice=0,
            auto_renewal_price_increase_pct=0.0, termination_for_convenience=0,
            termination_notice_days=0, termination_fee_pct=0.0,
            data_portability_guaranteed=0, data_retention_on_exit_days=0,
            governing_law_unfavorable=0, unilateral_amendment_right=0,
            price_lock_guaranteed=0, sla_penalty_pct=0.0,
            audit_rights_included=0,
        )
        result = radar.analyze(inp)
        assert isinstance(result, ContractClauseRiskResult)

    def test_reset_then_summary_shows_zeros(self, radar):
        radar.analyze(_base())
        radar.reset()
        s = radar.summary()
        assert s["total"] == 0

    def test_auto_renewal_notice_exactly_1(self, radar):
        r = ContractClauseRiskRadar()
        s = r._renewal_trap_score(_base(auto_renewal_days_notice=1,
                                        auto_renewal_price_increase_pct=0.0,
                                        price_lock_guaranteed=1))
        assert s == 40.0  # <= 30

    def test_data_retention_exactly_30_adds_6(self, radar):
        r = ContractClauseRiskRadar()
        s = r._termination_risk_score(_base(
            termination_for_convenience=1, termination_notice_days=30,
            termination_fee_pct=0.0, data_portability_guaranteed=1,
            data_retention_on_exit_days=30,
        ))
        assert s == 6.0

    def test_scope_value_0_default(self):
        r = ContractClauseRiskRadar()
        # scope=0 not in dict → 0 points
        s = r._liability_risk_score(_base(indemnification_scope=0))
        assert s == 0.0

    def test_liability_cap_exactly_5_point_0(self):
        r = ContractClauseRiskRadar()
        # 5.0 is not > 5.0, but 5.0 > 3.0 → +10
        s = r._liability_risk_score(_base(liability_cap_multiplier=5.0,
                                          unlimited_liability_clause=0,
                                          indemnification_scope=1,
                                          governing_law_unfavorable=0,
                                          unilateral_amendment_right=0))
        assert s == 10.0

    def test_price_increase_exactly_15(self):
        r = ContractClauseRiskRadar()
        s = r._renewal_trap_score(_base(auto_renewal_days_notice=91,
                                        auto_renewal_price_increase_pct=15.0,
                                        price_lock_guaranteed=1))
        assert s == 40.0

    def test_price_increase_exactly_10(self):
        r = ContractClauseRiskRadar()
        s = r._renewal_trap_score(_base(auto_renewal_days_notice=91,
                                        auto_renewal_price_increase_pct=10.0,
                                        price_lock_guaranteed=1))
        assert s == 25.0

    def test_price_increase_exactly_5(self):
        r = ContractClauseRiskRadar()
        s = r._renewal_trap_score(_base(auto_renewal_days_notice=91,
                                        auto_renewal_price_increase_pct=5.0,
                                        price_lock_guaranteed=1))
        assert s == 10.0

    def test_termination_notice_exactly_90_is_15(self):
        r = ContractClauseRiskRadar()
        s = r._termination_risk_score(_base(termination_for_convenience=1,
                                            termination_notice_days=90,
                                            termination_fee_pct=0.0,
                                            data_portability_guaranteed=1,
                                            data_retention_on_exit_days=90))
        assert s == 15.0

    def test_termination_notice_exactly_180_is_30(self):
        r = ContractClauseRiskRadar()
        s = r._termination_risk_score(_base(termination_for_convenience=1,
                                            termination_notice_days=180,
                                            termination_fee_pct=0.0,
                                            data_portability_guaranteed=1,
                                            data_retention_on_exit_days=90))
        assert s == 30.0


# ===========================================================================
# 24. CROSS-VALIDATION
# ===========================================================================

class TestCrossValidation:
    def test_risk_level_consistent_with_composite(self, radar):
        inputs = [
            _base(contract_id=f"C-{i}",
                  unlimited_liability_clause=i % 2,
                  indemnification_scope=(i % 4) + 1)
            for i in range(10)
        ]
        for inp in inputs:
            r = radar.analyze(inp)
            composite = r.clause_risk_composite
            if composite >= 65:
                assert r.clause_risk_level == ClauseRiskLevel.CRITICAL
            elif composite >= 45:
                assert r.clause_risk_level == ClauseRiskLevel.HIGH
            elif composite >= 25:
                assert r.clause_risk_level == ClauseRiskLevel.MODERATE
            else:
                assert r.clause_risk_level == ClauseRiskLevel.LOW

    def test_stance_consistent_with_risk_level(self, radar):
        mapping = {
            ClauseRiskLevel.LOW: NegotiationStance.ACCEPT,
            ClauseRiskLevel.MODERATE: NegotiationStance.MINOR_REVISION,
            ClauseRiskLevel.HIGH: NegotiationStance.NEGOTIATE_HARD,
            ClauseRiskLevel.CRITICAL: NegotiationStance.ESCALATE_LEGAL,
        }
        inputs = [
            _base(contract_id=f"C-{i}", unlimited_liability_clause=i % 2,
                  ip_ownership_assigned_to_vendor=i % 2)
            for i in range(6)
        ]
        for inp in inputs:
            r = radar.analyze(inp)
            assert r.negotiation_stance == mapping[r.clause_risk_level]

    def test_action_consistent_with_risk_level(self, radar):
        mapping = {
            ClauseRiskLevel.LOW: ContractAction.PROCEED,
            ClauseRiskLevel.MODERATE: ContractAction.FLAG_FOR_REVIEW,
            ClauseRiskLevel.HIGH: ContractAction.REDLINE,
            ClauseRiskLevel.CRITICAL: ContractAction.BLOCK_SIGNING,
        }
        inputs = [
            _base(contract_id=f"C-{i}", unlimited_liability_clause=i % 2,
                  ip_ownership_assigned_to_vendor=i % 2)
            for i in range(6)
        ]
        for inp in inputs:
            r = radar.analyze(inp)
            assert r.contract_action == mapping[r.clause_risk_level]

    def test_high_risk_consistent_with_definition(self, radar):
        for i in range(5):
            inp = _base(contract_id=f"C-{i}", unlimited_liability_clause=i % 2)
            r = radar.analyze(inp)
            expected = r.clause_risk_composite >= 55.0 or inp.unlimited_liability_clause == 1
            assert r.is_high_risk_contract == expected

    def test_needs_legal_consistent_with_definition(self, radar):
        for i in range(5):
            inp = _base(contract_id=f"C-{i}",
                        unlimited_liability_clause=i % 2,
                        ip_ownership_disputed=i % 2)
            r = radar.analyze(inp)
            expected = (r.clause_risk_composite >= 65.0
                        or inp.unlimited_liability_clause == 1
                        or inp.ip_ownership_disputed == 1)
            assert r.needs_legal_escalation == expected

    def test_composite_is_weighted_sum_of_components(self, radar):
        inp = _base(
            unlimited_liability_clause=1, indemnification_scope=3,
            governing_law_unfavorable=1, unilateral_amendment_right=1,
            ip_ownership_assigned_to_vendor=1, audit_rights_included=1,
            auto_renewal_days_notice=30, auto_renewal_price_increase_pct=10.0,
            price_lock_guaranteed=0,
            termination_for_convenience=0, termination_notice_days=90,
            termination_fee_pct=25.0, data_portability_guaranteed=1,
            data_retention_on_exit_days=60,
        )
        r = ContractClauseRiskRadar()
        liab = r._liability_risk_score(inp)
        ip = r._ip_risk_score(inp)
        renewal = r._renewal_trap_score(inp)
        term = r._termination_risk_score(inp)
        composite = r._composite(liab, ip, renewal, term)
        result = r.analyze(inp)
        assert result.clause_risk_composite == composite
        expected = round(min(100.0, max(0.0, liab*0.35 + ip*0.25 + renewal*0.20 + term*0.20)), 1)
        assert result.clause_risk_composite == expected

    def test_pattern_consistent_with_score_signals(self, radar):
        inputs = [
            _base(contract_id="c1"),
            _base(contract_id="c2", unlimited_liability_clause=1, indemnification_scope=4),
            _base(contract_id="c3", ip_ownership_assigned_to_vendor=1),
            _base(contract_id="c4", auto_renewal_days_notice=15,
                  auto_renewal_price_increase_pct=15.0, price_lock_guaranteed=0),
        ]
        for inp in inputs:
            r = ContractClauseRiskRadar()
            result = r.analyze(inp)
            liab = result.liability_risk_score
            ip = result.ip_risk_score
            renewal = result.renewal_trap_score
            term = result.termination_risk_score
            signals = sum([liab >= 50, ip >= 50, renewal >= 50, term >= 50])
            if signals >= 2:
                assert result.risky_clause_pattern == RiskyClausePattern.MULTI_CLAUSE_RISK
            elif liab >= 50:
                assert result.risky_clause_pattern == RiskyClausePattern.LIABILITY_EXPOSURE
            elif ip >= 50:
                assert result.risky_clause_pattern == RiskyClausePattern.IP_CONFLICT
            elif renewal >= 50:
                assert result.risky_clause_pattern == RiskyClausePattern.RENEWAL_TRAP
            elif term >= 50:
                assert result.risky_clause_pattern == RiskyClausePattern.TERMINATION_RISK
            else:
                assert result.risky_clause_pattern == RiskyClausePattern.CLEAN

    def test_financial_exposure_unlimited_branch(self, radar):
        inp = _base(contract_value=100_000.0, unlimited_liability_clause=1)
        result = radar.analyze(inp)
        base = inp.contract_value * (result.clause_risk_composite / 100.0)
        min_exposure = max(base, inp.contract_value * 2.0)
        assert result.estimated_financial_exposure == round(min_exposure, 2)

    def test_financial_exposure_normal_branch(self, radar):
        inp = _base(contract_value=100_000.0, unlimited_liability_clause=0)
        result = radar.analyze(inp)
        expected = round(100_000.0 * (result.clause_risk_composite / 100.0), 2)
        assert result.estimated_financial_exposure == expected

    def test_summary_avg_scores_match_manual_calc(self, radar):
        r1 = radar.analyze(_base(contract_id="C-1"))
        r2 = radar.analyze(_base(contract_id="C-2", unlimited_liability_clause=1))
        r3 = radar.analyze(_base(contract_id="C-3", ip_ownership_disputed=1))
        s = radar.summary()
        expected_liab = round((r1.liability_risk_score + r2.liability_risk_score +
                                r3.liability_risk_score) / 3, 1)
        expected_ip = round((r1.ip_risk_score + r2.ip_risk_score +
                              r3.ip_risk_score) / 3, 1)
        assert s["avg_liability_risk_score"] == expected_liab
        assert s["avg_ip_risk_score"] == expected_ip
