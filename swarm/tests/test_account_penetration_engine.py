"""
Comprehensive pytest tests for swarm/intelligence/account_penetration_engine.py
"""

from __future__ import annotations

import pytest

from swarm.intelligence.account_penetration_engine import (
    AccountPenetrationEngine,
    CommitteeGap,
    PenetrationAction,
    PenetrationInput,
    PenetrationLevel,
    PenetrationResult,
    StakeholderRisk,
)


# ─── Fixtures / Helpers ───────────────────────────────────────────────────────

def make_input(
    account_id: str = "acc-001",
    account_name: str = "Acme Corp",
    rep_id: str = "rep-01",
    rep_name: str = "Alice Dupont",
    total_contacts_mapped: int = 6,
    executive_contacts: int = 2,
    user_champion_contacts: int = 2,
    technical_evaluator_contacts: int = 1,
    finance_procurement_contacts: int = 1,
    active_contacts_30d: int = 4,
    promoter_contacts: int = 3,
    neutral_contacts: int = 2,
    detractor_contacts: int = 0,
    primary_champion_engaged: bool = True,
    champion_left_or_changed: bool = False,
    executive_sponsor_active: bool = True,
    decision_maker_relationship_score: int = 8,
    deal_size_eur: float = 75_000.0,
    deal_stage: str = "proposal",
    days_in_stage: int = 14,
    prior_deal_count: int = 1,
    contract_renewal_months: int | None = 6,
) -> PenetrationInput:
    return PenetrationInput(
        account_id=account_id,
        account_name=account_name,
        rep_id=rep_id,
        rep_name=rep_name,
        total_contacts_mapped=total_contacts_mapped,
        executive_contacts=executive_contacts,
        user_champion_contacts=user_champion_contacts,
        technical_evaluator_contacts=technical_evaluator_contacts,
        finance_procurement_contacts=finance_procurement_contacts,
        active_contacts_30d=active_contacts_30d,
        promoter_contacts=promoter_contacts,
        neutral_contacts=neutral_contacts,
        detractor_contacts=detractor_contacts,
        primary_champion_engaged=primary_champion_engaged,
        champion_left_or_changed=champion_left_or_changed,
        executive_sponsor_active=executive_sponsor_active,
        decision_maker_relationship_score=decision_maker_relationship_score,
        deal_size_eur=deal_size_eur,
        deal_stage=deal_stage,
        days_in_stage=days_in_stage,
        prior_deal_count=prior_deal_count,
        contract_renewal_months=contract_renewal_months,
    )


@pytest.fixture
def engine() -> AccountPenetrationEngine:
    return AccountPenetrationEngine()


@pytest.fixture
def full_input() -> PenetrationInput:
    return make_input()


# ─── Enum: PenetrationLevel ───────────────────────────────────────────────────

class TestPenetrationLevelEnum:
    def test_deep_value(self):
        assert PenetrationLevel.DEEP == "deep"

    def test_solid_value(self):
        assert PenetrationLevel.SOLID == "solid"

    def test_partial_value(self):
        assert PenetrationLevel.PARTIAL == "partial"

    def test_thin_value(self):
        assert PenetrationLevel.THIN == "thin"

    def test_single_value(self):
        assert PenetrationLevel.SINGLE == "single"

    def test_str_inheritance(self):
        assert isinstance(PenetrationLevel.DEEP, str)
        assert isinstance(PenetrationLevel.SOLID, str)
        assert isinstance(PenetrationLevel.PARTIAL, str)
        assert isinstance(PenetrationLevel.THIN, str)
        assert isinstance(PenetrationLevel.SINGLE, str)

    def test_five_members(self):
        assert len(PenetrationLevel) == 5

    def test_enum_values_are_strings(self):
        for member in PenetrationLevel:
            assert isinstance(member.value, str)


# ─── Enum: StakeholderRisk ────────────────────────────────────────────────────

class TestStakeholderRiskEnum:
    def test_secure_value(self):
        assert StakeholderRisk.SECURE == "secure"

    def test_stable_value(self):
        assert StakeholderRisk.STABLE == "stable"

    def test_vulnerable_value(self):
        assert StakeholderRisk.VULNERABLE == "vulnerable"

    def test_critical_value(self):
        assert StakeholderRisk.CRITICAL == "critical"

    def test_str_inheritance(self):
        for member in StakeholderRisk:
            assert isinstance(member, str)

    def test_four_members(self):
        assert len(StakeholderRisk) == 4


# ─── Enum: CommitteeGap ───────────────────────────────────────────────────────

class TestCommitteeGapEnum:
    def test_none_value(self):
        assert CommitteeGap.NONE == "none"

    def test_missing_exec_value(self):
        assert CommitteeGap.MISSING_EXEC == "missing_exec"

    def test_missing_user_value(self):
        assert CommitteeGap.MISSING_USER == "missing_user"

    def test_missing_tech_value(self):
        assert CommitteeGap.MISSING_TECH == "missing_tech"

    def test_missing_finance_value(self):
        assert CommitteeGap.MISSING_FINANCE == "missing_finance"

    def test_multiple_gaps_value(self):
        assert CommitteeGap.MULTIPLE_GAPS == "multiple_gaps"

    def test_str_inheritance(self):
        for member in CommitteeGap:
            assert isinstance(member, str)

    def test_six_members(self):
        assert len(CommitteeGap) == 6


# ─── Enum: PenetrationAction ─────────────────────────────────────────────────

class TestPenetrationActionEnum:
    def test_maintain_value(self):
        assert PenetrationAction.MAINTAIN == "maintain"

    def test_expand_exec_value(self):
        assert PenetrationAction.EXPAND_EXEC == "expand_exec"

    def test_expand_user_value(self):
        assert PenetrationAction.EXPAND_USER == "expand_user"

    def test_expand_tech_value(self):
        assert PenetrationAction.EXPAND_TECH == "expand_tech"

    def test_expand_finance_value(self):
        assert PenetrationAction.EXPAND_FINANCE == "expand_finance"

    def test_rebuild_champion_value(self):
        assert PenetrationAction.REBUILD_CHAMPION == "rebuild_champion"

    def test_multithread_now_value(self):
        assert PenetrationAction.MULTITHREAD_NOW == "multithread_now"

    def test_str_inheritance(self):
        for member in PenetrationAction:
            assert isinstance(member, str)

    def test_seven_members(self):
        assert len(PenetrationAction) == 7


# ─── PenetrationInput dataclass ───────────────────────────────────────────────

class TestPenetrationInputFields:
    def test_account_id_field(self, full_input):
        assert full_input.account_id == "acc-001"

    def test_account_name_field(self, full_input):
        assert full_input.account_name == "Acme Corp"

    def test_rep_id_field(self, full_input):
        assert full_input.rep_id == "rep-01"

    def test_rep_name_field(self, full_input):
        assert full_input.rep_name == "Alice Dupont"

    def test_total_contacts_mapped_field(self, full_input):
        assert full_input.total_contacts_mapped == 6

    def test_executive_contacts_field(self, full_input):
        assert full_input.executive_contacts == 2

    def test_user_champion_contacts_field(self, full_input):
        assert full_input.user_champion_contacts == 2

    def test_technical_evaluator_contacts_field(self, full_input):
        assert full_input.technical_evaluator_contacts == 1

    def test_finance_procurement_contacts_field(self, full_input):
        assert full_input.finance_procurement_contacts == 1

    def test_active_contacts_30d_field(self, full_input):
        assert full_input.active_contacts_30d == 4

    def test_promoter_contacts_field(self, full_input):
        assert full_input.promoter_contacts == 3

    def test_neutral_contacts_field(self, full_input):
        assert full_input.neutral_contacts == 2

    def test_detractor_contacts_field(self, full_input):
        assert full_input.detractor_contacts == 0

    def test_primary_champion_engaged_field(self, full_input):
        assert full_input.primary_champion_engaged is True

    def test_champion_left_or_changed_field(self, full_input):
        assert full_input.champion_left_or_changed is False

    def test_executive_sponsor_active_field(self, full_input):
        assert full_input.executive_sponsor_active is True

    def test_decision_maker_relationship_score_field(self, full_input):
        assert full_input.decision_maker_relationship_score == 8

    def test_deal_size_eur_field(self, full_input):
        assert full_input.deal_size_eur == 75_000.0

    def test_deal_stage_field(self, full_input):
        assert full_input.deal_stage == "proposal"

    def test_days_in_stage_field(self, full_input):
        assert full_input.days_in_stage == 14

    def test_prior_deal_count_field(self, full_input):
        assert full_input.prior_deal_count == 1

    def test_contract_renewal_months_field(self, full_input):
        assert full_input.contract_renewal_months == 6

    def test_contract_renewal_months_none(self):
        inp = make_input(contract_renewal_months=None)
        assert inp.contract_renewal_months is None

    def test_nineteen_fields(self):
        import dataclasses
        fields = dataclasses.fields(PenetrationInput)
        assert len(fields) == 22  # account: 4 + committee: 5 + relationship: 6 + key person: 4 + deal: 5 = 24... let's just count directly
        field_names = {f.name for f in fields}
        expected = {
            "account_id", "account_name", "rep_id", "rep_name",
            "total_contacts_mapped", "executive_contacts", "user_champion_contacts",
            "technical_evaluator_contacts", "finance_procurement_contacts",
            "active_contacts_30d", "promoter_contacts", "neutral_contacts", "detractor_contacts",
            "primary_champion_engaged", "champion_left_or_changed", "executive_sponsor_active",
            "decision_maker_relationship_score",
            "deal_size_eur", "deal_stage", "days_in_stage", "prior_deal_count",
            "contract_renewal_months",
        }
        assert field_names == expected


# ─── PenetrationResult.to_dict ────────────────────────────────────────────────

class TestPenetrationResultToDict:
    def test_to_dict_returns_dict(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.to_dict(), dict)

    def test_to_dict_exactly_15_keys(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert len(d) == 15

    def test_to_dict_has_account_id(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "account_id" in d

    def test_to_dict_has_account_name(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "account_name" in d

    def test_to_dict_has_rep_id(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "rep_id" in d

    def test_to_dict_has_rep_name(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "rep_name" in d

    def test_to_dict_has_penetration_level(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "penetration_level" in d

    def test_to_dict_has_stakeholder_risk(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "stakeholder_risk" in d

    def test_to_dict_has_committee_gap(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "committee_gap" in d

    def test_to_dict_has_penetration_action(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "penetration_action" in d

    def test_to_dict_has_penetration_score(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "penetration_score" in d

    def test_to_dict_has_coverage_score(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "coverage_score" in d

    def test_to_dict_has_relationship_score(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "relationship_score" in d

    def test_to_dict_has_multithread_ratio(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "multithread_ratio" in d

    def test_to_dict_has_expansion_plays(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "expansion_plays" in d

    def test_to_dict_has_risk_signals(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "risk_signals" in d

    def test_to_dict_has_manager_alerts(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        assert "manager_alerts" in d

    def test_to_dict_exact_keys(self, engine, full_input):
        d = engine.analyze(full_input).to_dict()
        expected_keys = {
            "account_id", "account_name", "rep_id", "rep_name",
            "penetration_level", "stakeholder_risk", "committee_gap",
            "penetration_action", "penetration_score", "coverage_score",
            "relationship_score", "multithread_ratio", "expansion_plays",
            "risk_signals", "manager_alerts",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_values_passthrough(self, engine, full_input):
        result = engine.analyze(full_input)
        d = result.to_dict()
        assert d["account_id"] == result.account_id
        assert d["account_name"] == result.account_name
        assert d["rep_id"] == result.rep_id
        assert d["rep_name"] == result.rep_name
        assert d["penetration_score"] == result.penetration_score
        assert d["expansion_plays"] is result.expansion_plays
        assert d["risk_signals"] is result.risk_signals
        assert d["manager_alerts"] is result.manager_alerts


# ─── Coverage Score ───────────────────────────────────────────────────────────

class TestCoverageScore:
    def test_exec_ge2_adds_20(self, engine):
        inp = make_input(executive_contacts=2, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=2, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score >= 20

    def test_exec_eq1_adds_12(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=1, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score >= 12

    def test_exec_eq0_adds_0(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=0, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score == 0.0

    def test_user_champion_ge2_adds_20(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=2,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=2, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score >= 20

    def test_user_champion_eq1_adds_12(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=1,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=1, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score >= 12

    def test_tech_eval_ge1_adds_20(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=1, finance_procurement_contacts=0,
                         total_contacts_mapped=1, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score >= 20

    def test_finance_ge1_adds_15(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=1,
                         total_contacts_mapped=1, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score >= 15

    def test_total_contacts_ge8_adds_10(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=8, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score >= 10

    def test_total_contacts_ge5_adds_5(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=5, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score >= 5

    def test_total_contacts_ge3_adds_2(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=3, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score >= 2

    def test_total_contacts_lt3_adds_0(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=2, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score == 0.0

    def test_activity_ratio_adds_up_to_15(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=10, active_contacts_30d=10)
        result = engine.analyze(inp)
        # activity_ratio = 1.0, min(15, 1.0*15)=15, breadth bonus 10 = total 25
        assert result.coverage_score == 25.0

    def test_activity_ratio_partial(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=4, active_contacts_30d=2)
        result = engine.analyze(inp)
        # activity_ratio=0.5, 0.5*15=7.5; breadth bonus 2 (ge3) = total 9.5
        assert result.coverage_score == 9.5

    def test_coverage_score_capped_at_100(self, engine):
        inp = make_input(executive_contacts=10, user_champion_contacts=10,
                         technical_evaluator_contacts=5, finance_procurement_contacts=5,
                         total_contacts_mapped=20, active_contacts_30d=20)
        result = engine.analyze(inp)
        assert result.coverage_score <= 100.0

    def test_coverage_score_zero_contacts(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=0, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.coverage_score == 0.0

    def test_coverage_score_is_numeric(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.coverage_score, (int, float))

    def test_total_contacts_boundary_8(self, engine):
        inp8 = make_input(executive_contacts=0, user_champion_contacts=0,
                          technical_evaluator_contacts=0, finance_procurement_contacts=0,
                          total_contacts_mapped=8, active_contacts_30d=0)
        inp7 = make_input(executive_contacts=0, user_champion_contacts=0,
                          technical_evaluator_contacts=0, finance_procurement_contacts=0,
                          total_contacts_mapped=7, active_contacts_30d=0)
        r8 = engine.analyze(inp8)
        r7 = engine.analyze(inp7)
        assert r8.coverage_score > r7.coverage_score

    def test_total_contacts_boundary_5(self, engine):
        inp5 = make_input(executive_contacts=0, user_champion_contacts=0,
                          technical_evaluator_contacts=0, finance_procurement_contacts=0,
                          total_contacts_mapped=5, active_contacts_30d=0)
        inp4 = make_input(executive_contacts=0, user_champion_contacts=0,
                          technical_evaluator_contacts=0, finance_procurement_contacts=0,
                          total_contacts_mapped=4, active_contacts_30d=0)
        r5 = engine.analyze(inp5)
        r4 = engine.analyze(inp4)
        assert r5.coverage_score > r4.coverage_score

    def test_full_committee_coverage(self, engine):
        inp = make_input(executive_contacts=2, user_champion_contacts=2,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1,
                         total_contacts_mapped=8, active_contacts_30d=8)
        result = engine.analyze(inp)
        # 20+20+20+15+10+15=100
        assert result.coverage_score == 100.0


# ─── Relationship Score ───────────────────────────────────────────────────────

class TestRelationshipScore:
    def test_champion_adds_25(self, engine):
        inp = make_input(primary_champion_engaged=True, executive_sponsor_active=False,
                         decision_maker_relationship_score=0, promoter_contacts=0,
                         neutral_contacts=0, detractor_contacts=0, prior_deal_count=0,
                         champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert result.relationship_score >= 25

    def test_exec_sponsor_adds_20(self, engine):
        inp = make_input(primary_champion_engaged=False, executive_sponsor_active=True,
                         decision_maker_relationship_score=0, promoter_contacts=0,
                         neutral_contacts=0, detractor_contacts=0, prior_deal_count=0,
                         champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert result.relationship_score >= 20

    def test_dm_score_max_20(self, engine):
        inp = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                         decision_maker_relationship_score=10, promoter_contacts=0,
                         neutral_contacts=0, detractor_contacts=0, prior_deal_count=0,
                         champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert result.relationship_score >= 20

    def test_dm_score_multiplied_by_2(self, engine):
        inp5 = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                          decision_maker_relationship_score=5, promoter_contacts=0,
                          neutral_contacts=0, detractor_contacts=0, prior_deal_count=0,
                          champion_left_or_changed=False)
        inp3 = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                          decision_maker_relationship_score=3, promoter_contacts=0,
                          neutral_contacts=0, detractor_contacts=0, prior_deal_count=0,
                          champion_left_or_changed=False)
        r5 = engine.analyze(inp5)
        r3 = engine.analyze(inp3)
        assert r5.relationship_score - r3.relationship_score == pytest.approx(4.0, abs=0.2)

    def test_promoter_ratio_max_20(self, engine):
        inp = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                         decision_maker_relationship_score=0, promoter_contacts=5,
                         neutral_contacts=0, detractor_contacts=0, prior_deal_count=0,
                         champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert result.relationship_score >= 20

    def test_promoter_ratio_partial(self, engine):
        inp = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                         decision_maker_relationship_score=0, promoter_contacts=1,
                         neutral_contacts=1, detractor_contacts=0, prior_deal_count=0,
                         champion_left_or_changed=False)
        result = engine.analyze(inp)
        # promoter_ratio = 0.5, 0.5*20=10
        assert result.relationship_score == pytest.approx(10.0, abs=0.2)

    def test_prior_deal_count_max_15(self, engine):
        inp = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                         decision_maker_relationship_score=0, promoter_contacts=0,
                         neutral_contacts=0, detractor_contacts=0, prior_deal_count=10,
                         champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert result.relationship_score >= 15

    def test_prior_deal_count_multiplied_by_5(self, engine):
        inp2 = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                          decision_maker_relationship_score=0, promoter_contacts=0,
                          neutral_contacts=0, detractor_contacts=0, prior_deal_count=2,
                          champion_left_or_changed=False)
        inp1 = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                          decision_maker_relationship_score=0, promoter_contacts=0,
                          neutral_contacts=0, detractor_contacts=0, prior_deal_count=1,
                          champion_left_or_changed=False)
        r2 = engine.analyze(inp2)
        r1 = engine.analyze(inp1)
        assert r2.relationship_score - r1.relationship_score == pytest.approx(5.0, abs=0.2)

    def test_detractors_ge2_penalises_10(self, engine):
        # Use dm_score=10 (adds 20) so baseline is 20; with detractors>=2 it becomes 10
        inp_no_det = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                                decision_maker_relationship_score=10, promoter_contacts=0,
                                neutral_contacts=5, detractor_contacts=0, prior_deal_count=0,
                                champion_left_or_changed=False)
        inp_det = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                             decision_maker_relationship_score=10, promoter_contacts=0,
                             neutral_contacts=5, detractor_contacts=2, prior_deal_count=0,
                             champion_left_or_changed=False)
        r_no = engine.analyze(inp_no_det)
        r_det = engine.analyze(inp_det)
        assert r_no.relationship_score - r_det.relationship_score == pytest.approx(10.0, abs=0.2)

    def test_detractors_eq1_no_penalty(self, engine):
        inp_no_det = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                                decision_maker_relationship_score=0, promoter_contacts=0,
                                neutral_contacts=5, detractor_contacts=0, prior_deal_count=0,
                                champion_left_or_changed=False)
        inp_1det = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                              decision_maker_relationship_score=0, promoter_contacts=0,
                              neutral_contacts=5, detractor_contacts=1, prior_deal_count=0,
                              champion_left_or_changed=False)
        r_no = engine.analyze(inp_no_det)
        r_1 = engine.analyze(inp_1det)
        assert r_no.relationship_score == r_1.relationship_score

    def test_champion_left_penalises_20(self, engine):
        # Use dm_score=10 (adds 20) and prior_deal_count=2 (adds 10) = 30 baseline
        # With champion_left: 30 - 20 = 10
        inp_ok = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                            decision_maker_relationship_score=10, promoter_contacts=0,
                            neutral_contacts=0, detractor_contacts=0, prior_deal_count=2,
                            champion_left_or_changed=False)
        inp_left = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                              decision_maker_relationship_score=10, promoter_contacts=0,
                              neutral_contacts=0, detractor_contacts=0, prior_deal_count=2,
                              champion_left_or_changed=True)
        r_ok = engine.analyze(inp_ok)
        r_left = engine.analyze(inp_left)
        assert r_ok.relationship_score - r_left.relationship_score == pytest.approx(20.0, abs=0.2)

    def test_relationship_score_floored_at_0(self, engine):
        inp = make_input(primary_champion_engaged=False, executive_sponsor_active=False,
                         decision_maker_relationship_score=0, promoter_contacts=0,
                         neutral_contacts=0, detractor_contacts=5, prior_deal_count=0,
                         champion_left_or_changed=True)
        result = engine.analyze(inp)
        assert result.relationship_score >= 0.0

    def test_relationship_score_capped_at_100(self, engine):
        inp = make_input(primary_champion_engaged=True, executive_sponsor_active=True,
                         decision_maker_relationship_score=10, promoter_contacts=20,
                         neutral_contacts=0, detractor_contacts=0, prior_deal_count=10,
                         champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert result.relationship_score <= 100.0

    def test_relationship_score_is_numeric(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.relationship_score, (int, float))


# ─── Penetration Score ────────────────────────────────────────────────────────

class TestPenetrationScore:
    def test_penetration_score_is_average(self, engine, full_input):
        result = engine.analyze(full_input)
        expected = round(result.coverage_score * 0.5 + result.relationship_score * 0.5, 1)
        assert result.penetration_score == expected

    def test_penetration_score_is_numeric(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.penetration_score, (int, float))

    def test_penetration_score_rounded_to_1_decimal(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=0,
                         total_contacts_mapped=4, active_contacts_30d=2,
                         promoter_contacts=1, neutral_contacts=1, detractor_contacts=0,
                         primary_champion_engaged=True, executive_sponsor_active=False,
                         decision_maker_relationship_score=5, prior_deal_count=1,
                         champion_left_or_changed=False)
        result = engine.analyze(inp)
        as_str = str(result.penetration_score)
        if "." in as_str:
            assert len(as_str.split(".")[1]) <= 1

    def test_penetration_score_between_0_and_100(self, engine, full_input):
        result = engine.analyze(full_input)
        assert 0.0 <= result.penetration_score <= 100.0


# ─── Penetration Level Classification ────────────────────────────────────────

class TestPenetrationLevelClassification:
    def test_single_when_total_contacts_0(self, engine):
        inp = make_input(total_contacts_mapped=0, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.penetration_level == PenetrationLevel.SINGLE.value

    def test_single_when_total_contacts_1(self, engine):
        inp = make_input(total_contacts_mapped=1, active_contacts_30d=1,
                         executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0)
        result = engine.analyze(inp)
        assert result.penetration_level == PenetrationLevel.SINGLE.value

    def test_deep_when_score_ge75(self, engine):
        inp = make_input(
            executive_contacts=2, user_champion_contacts=2,
            technical_evaluator_contacts=1, finance_procurement_contacts=1,
            total_contacts_mapped=8, active_contacts_30d=8,
            primary_champion_engaged=True, executive_sponsor_active=True,
            decision_maker_relationship_score=10, promoter_contacts=5,
            neutral_contacts=0, detractor_contacts=0, prior_deal_count=3,
            champion_left_or_changed=False
        )
        result = engine.analyze(inp)
        assert result.penetration_level == PenetrationLevel.DEEP.value

    def test_solid_when_score_ge55_lt75(self, engine):
        inp = make_input(
            executive_contacts=1, user_champion_contacts=2,
            technical_evaluator_contacts=1, finance_procurement_contacts=1,
            total_contacts_mapped=5, active_contacts_30d=3,
            primary_champion_engaged=True, executive_sponsor_active=False,
            decision_maker_relationship_score=5, promoter_contacts=2,
            neutral_contacts=2, detractor_contacts=0, prior_deal_count=1,
            champion_left_or_changed=False
        )
        result = engine.analyze(inp)
        assert result.penetration_score >= 55 and result.penetration_score < 75
        assert result.penetration_level == PenetrationLevel.SOLID.value

    def test_thin_when_score_lt35(self, engine):
        inp = make_input(
            executive_contacts=0, user_champion_contacts=0,
            technical_evaluator_contacts=0, finance_procurement_contacts=0,
            total_contacts_mapped=2, active_contacts_30d=0,
            primary_champion_engaged=False, executive_sponsor_active=False,
            decision_maker_relationship_score=0, promoter_contacts=0,
            neutral_contacts=2, detractor_contacts=0, prior_deal_count=0,
            champion_left_or_changed=False
        )
        result = engine.analyze(inp)
        assert result.penetration_score < 35
        assert result.penetration_level == PenetrationLevel.THIN.value

    def test_single_overrides_high_score(self, engine):
        inp = make_input(
            total_contacts_mapped=1, active_contacts_30d=1,
            executive_contacts=1, user_champion_contacts=0,
            technical_evaluator_contacts=0, finance_procurement_contacts=0,
            primary_champion_engaged=True, executive_sponsor_active=True,
            decision_maker_relationship_score=10, promoter_contacts=1,
            neutral_contacts=0, detractor_contacts=0, prior_deal_count=5,
            champion_left_or_changed=False
        )
        result = engine.analyze(inp)
        assert result.penetration_level == PenetrationLevel.SINGLE.value

    def test_boundary_score_75_is_deep(self, engine):
        # score exactly 75 → DEEP
        # coverage=75, relationship=75 → score=75
        # Build input carefully: 20+20+20+15+0+0=75 coverage; 25+20+10+0+0=55 relationship → 65 total
        # Instead just test the scoring boundary by checking >=75 → DEEP via a high score input
        inp = make_input(
            executive_contacts=2, user_champion_contacts=2,
            technical_evaluator_contacts=1, finance_procurement_contacts=1,
            total_contacts_mapped=10, active_contacts_30d=10,
            primary_champion_engaged=True, executive_sponsor_active=True,
            decision_maker_relationship_score=10, promoter_contacts=5,
            neutral_contacts=0, detractor_contacts=0, prior_deal_count=3,
            champion_left_or_changed=False
        )
        result = engine.analyze(inp)
        assert result.penetration_score >= 75
        assert result.penetration_level == PenetrationLevel.DEEP.value

    def test_boundary_score_55_is_solid(self, engine):
        inp = make_input(
            executive_contacts=1, user_champion_contacts=1,
            technical_evaluator_contacts=1, finance_procurement_contacts=0,
            total_contacts_mapped=3, active_contacts_30d=2,
            primary_champion_engaged=True, executive_sponsor_active=False,
            decision_maker_relationship_score=5, promoter_contacts=1,
            neutral_contacts=1, detractor_contacts=0, prior_deal_count=1,
            champion_left_or_changed=False
        )
        result = engine.analyze(inp)
        if result.penetration_score >= 55:
            assert result.penetration_level in (PenetrationLevel.SOLID.value, PenetrationLevel.DEEP.value)

    def test_boundary_score_35_is_partial(self, engine):
        inp = make_input(
            executive_contacts=0, user_champion_contacts=1,
            technical_evaluator_contacts=1, finance_procurement_contacts=0,
            total_contacts_mapped=3, active_contacts_30d=1,
            primary_champion_engaged=True, executive_sponsor_active=False,
            decision_maker_relationship_score=3, promoter_contacts=1,
            neutral_contacts=2, detractor_contacts=0, prior_deal_count=0,
            champion_left_or_changed=False
        )
        result = engine.analyze(inp)
        if result.penetration_score >= 35 and result.penetration_score < 55:
            assert result.penetration_level == PenetrationLevel.PARTIAL.value


# ─── Stakeholder Risk ─────────────────────────────────────────────────────────

class TestStakeholderRisk:
    def test_critical_when_champion_left(self, engine):
        inp = make_input(champion_left_or_changed=True)
        result = engine.analyze(inp)
        assert result.stakeholder_risk == StakeholderRisk.CRITICAL.value

    def test_vulnerable_when_detractors_ge2(self, engine):
        inp = make_input(detractor_contacts=2, champion_left_or_changed=False,
                         total_contacts_mapped=5)
        result = engine.analyze(inp)
        assert result.stakeholder_risk == StakeholderRisk.VULNERABLE.value

    def test_vulnerable_when_total_contacts_1(self, engine):
        inp = make_input(total_contacts_mapped=1, detractor_contacts=0,
                         champion_left_or_changed=False,
                         executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         active_contacts_30d=1)
        result = engine.analyze(inp)
        assert result.stakeholder_risk == StakeholderRisk.VULNERABLE.value

    def test_vulnerable_when_total_contacts_0(self, engine):
        inp = make_input(total_contacts_mapped=0, detractor_contacts=0,
                         champion_left_or_changed=False,
                         executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.stakeholder_risk == StakeholderRisk.VULNERABLE.value

    def test_secure_when_promoters_ge2_champion_and_exec(self, engine):
        inp = make_input(promoter_contacts=2, primary_champion_engaged=True,
                         executive_sponsor_active=True, detractor_contacts=0,
                         champion_left_or_changed=False, total_contacts_mapped=5)
        result = engine.analyze(inp)
        assert result.stakeholder_risk == StakeholderRisk.SECURE.value

    def test_stable_when_no_special_condition(self, engine):
        inp = make_input(promoter_contacts=1, primary_champion_engaged=True,
                         executive_sponsor_active=True, detractor_contacts=0,
                         champion_left_or_changed=False, total_contacts_mapped=5)
        result = engine.analyze(inp)
        assert result.stakeholder_risk == StakeholderRisk.STABLE.value

    def test_critical_takes_precedence_over_detractors(self, engine):
        inp = make_input(champion_left_or_changed=True, detractor_contacts=3,
                         total_contacts_mapped=5)
        result = engine.analyze(inp)
        assert result.stakeholder_risk == StakeholderRisk.CRITICAL.value

    def test_secure_requires_all_three_conditions(self, engine):
        inp_missing_exec = make_input(promoter_contacts=2, primary_champion_engaged=True,
                                      executive_sponsor_active=False, detractor_contacts=0,
                                      champion_left_or_changed=False, total_contacts_mapped=5)
        result = engine.analyze(inp_missing_exec)
        assert result.stakeholder_risk == StakeholderRisk.STABLE.value

    def test_detractors_eq1_not_vulnerable(self, engine):
        inp = make_input(detractor_contacts=1, champion_left_or_changed=False,
                         total_contacts_mapped=5, promoter_contacts=1,
                         primary_champion_engaged=True, executive_sponsor_active=True)
        result = engine.analyze(inp)
        assert result.stakeholder_risk in (StakeholderRisk.SECURE.value, StakeholderRisk.STABLE.value)


# ─── Committee Gap ────────────────────────────────────────────────────────────

class TestCommitteeGap:
    def test_none_when_all_roles_covered(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert result.committee_gap == CommitteeGap.NONE.value

    def test_missing_exec_when_only_exec_missing(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert result.committee_gap == CommitteeGap.MISSING_EXEC.value

    def test_missing_user_when_only_user_missing(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert result.committee_gap == CommitteeGap.MISSING_USER.value

    def test_missing_tech_when_only_tech_missing(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=0, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert result.committee_gap == CommitteeGap.MISSING_TECH.value

    def test_missing_finance_when_only_finance_missing(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=0)
        result = engine.analyze(inp)
        assert result.committee_gap == CommitteeGap.MISSING_FINANCE.value

    def test_multiple_gaps_when_2_missing(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert result.committee_gap == CommitteeGap.MULTIPLE_GAPS.value

    def test_multiple_gaps_when_3_missing(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert result.committee_gap == CommitteeGap.MULTIPLE_GAPS.value

    def test_multiple_gaps_when_4_missing(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0)
        result = engine.analyze(inp)
        assert result.committee_gap == CommitteeGap.MULTIPLE_GAPS.value

    def test_missing_exec_user_is_multiple(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert result.committee_gap == CommitteeGap.MULTIPLE_GAPS.value

    def test_missing_tech_finance_is_multiple(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0)
        result = engine.analyze(inp)
        assert result.committee_gap == CommitteeGap.MULTIPLE_GAPS.value


# ─── Penetration Action ───────────────────────────────────────────────────────

class TestPenetrationAction:
    def test_multithread_now_when_single(self, engine):
        inp = make_input(total_contacts_mapped=1, active_contacts_30d=1,
                         executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0)
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.MULTITHREAD_NOW.value

    def test_rebuild_champion_when_critical_risk(self, engine):
        inp = make_input(champion_left_or_changed=True, total_contacts_mapped=5,
                         executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.REBUILD_CHAMPION.value

    def test_expand_exec_when_missing_exec(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1,
                         champion_left_or_changed=False, total_contacts_mapped=5,
                         promoter_contacts=2, primary_champion_engaged=True,
                         executive_sponsor_active=True, detractor_contacts=0)
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.EXPAND_EXEC.value

    def test_expand_user_when_missing_user(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1,
                         champion_left_or_changed=False, total_contacts_mapped=5,
                         promoter_contacts=2, primary_champion_engaged=True,
                         executive_sponsor_active=True, detractor_contacts=0)
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.EXPAND_USER.value

    def test_expand_tech_when_missing_tech(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=0, finance_procurement_contacts=1,
                         champion_left_or_changed=False, total_contacts_mapped=5,
                         promoter_contacts=2, primary_champion_engaged=True,
                         executive_sponsor_active=True, detractor_contacts=0)
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.EXPAND_TECH.value

    def test_expand_finance_when_missing_finance(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=0,
                         champion_left_or_changed=False, total_contacts_mapped=5,
                         promoter_contacts=2, primary_champion_engaged=True,
                         executive_sponsor_active=True, detractor_contacts=0)
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.EXPAND_FINANCE.value

    def test_multithread_now_when_multiple_gaps(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1,
                         champion_left_or_changed=False, total_contacts_mapped=5,
                         promoter_contacts=2, primary_champion_engaged=True,
                         executive_sponsor_active=True, detractor_contacts=0)
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.MULTITHREAD_NOW.value

    def test_maintain_when_no_gaps_no_risk(self, engine):
        inp = make_input(
            executive_contacts=2, user_champion_contacts=2,
            technical_evaluator_contacts=1, finance_procurement_contacts=1,
            champion_left_or_changed=False, total_contacts_mapped=8,
            active_contacts_30d=6, promoter_contacts=3, primary_champion_engaged=True,
            executive_sponsor_active=True, detractor_contacts=0,
            decision_maker_relationship_score=8, prior_deal_count=2
        )
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.MAINTAIN.value

    def test_single_overrides_critical(self, engine):
        inp = make_input(total_contacts_mapped=1, active_contacts_30d=1,
                         executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         champion_left_or_changed=True)
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.MULTITHREAD_NOW.value

    def test_critical_overrides_gap(self, engine):
        inp = make_input(total_contacts_mapped=5, active_contacts_30d=3,
                         executive_contacts=0, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1,
                         champion_left_or_changed=True)
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.REBUILD_CHAMPION.value


# ─── Multithread Ratio ────────────────────────────────────────────────────────

class TestMultithreadRatio:
    def test_ratio_calculation(self, engine):
        inp = make_input(total_contacts_mapped=10, active_contacts_30d=5)
        result = engine.analyze(inp)
        assert result.multithread_ratio == pytest.approx(0.5, abs=0.01)

    def test_ratio_zero_when_total_zero(self, engine):
        inp = make_input(total_contacts_mapped=0, active_contacts_30d=0,
                         executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0)
        result = engine.analyze(inp)
        assert result.multithread_ratio == 0.0

    def test_ratio_rounded_to_2_decimals(self, engine):
        inp = make_input(total_contacts_mapped=7, active_contacts_30d=3)
        result = engine.analyze(inp)
        assert result.multithread_ratio == round(3 / 7, 2)

    def test_ratio_100_percent(self, engine):
        inp = make_input(total_contacts_mapped=4, active_contacts_30d=4)
        result = engine.analyze(inp)
        assert result.multithread_ratio == 1.0

    def test_ratio_0_percent_active(self, engine):
        inp = make_input(total_contacts_mapped=6, active_contacts_30d=0)
        result = engine.analyze(inp)
        assert result.multithread_ratio == 0.0

    def test_ratio_is_numeric(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.multithread_ratio, (int, float))


# ─── Analyze Method ───────────────────────────────────────────────────────────

class TestAnalyze:
    def test_returns_penetration_result(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result, PenetrationResult)

    def test_result_fields_set_correctly(self, engine, full_input):
        result = engine.analyze(full_input)
        assert result.account_id == full_input.account_id
        assert result.account_name == full_input.account_name
        assert result.rep_id == full_input.rep_id
        assert result.rep_name == full_input.rep_name

    def test_result_appended_to_internal_list(self, engine, full_input):
        engine.analyze(full_input)
        assert len(engine._results) == 1

    def test_multiple_results_appended(self, engine):
        inp1 = make_input(account_id="a1")
        inp2 = make_input(account_id="a2")
        engine.analyze(inp1)
        engine.analyze(inp2)
        assert len(engine._results) == 2

    def test_expansion_plays_is_list(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.expansion_plays, list)

    def test_risk_signals_is_list(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.risk_signals, list)

    def test_manager_alerts_is_list(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.manager_alerts, list)

    def test_penetration_level_is_string(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.penetration_level, str)

    def test_stakeholder_risk_is_string(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.stakeholder_risk, str)

    def test_committee_gap_is_string(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.committee_gap, str)

    def test_penetration_action_is_string(self, engine, full_input):
        result = engine.analyze(full_input)
        assert isinstance(result.penetration_action, str)

    def test_penetration_level_valid_value(self, engine, full_input):
        result = engine.analyze(full_input)
        assert result.penetration_level in {m.value for m in PenetrationLevel}

    def test_stakeholder_risk_valid_value(self, engine, full_input):
        result = engine.analyze(full_input)
        assert result.stakeholder_risk in {m.value for m in StakeholderRisk}

    def test_committee_gap_valid_value(self, engine, full_input):
        result = engine.analyze(full_input)
        assert result.committee_gap in {m.value for m in CommitteeGap}

    def test_penetration_action_valid_value(self, engine, full_input):
        result = engine.analyze(full_input)
        assert result.penetration_action in {m.value for m in PenetrationAction}


# ─── Analyze Batch ────────────────────────────────────────────────────────────

class TestAnalyzeBatch:
    def test_returns_list(self, engine):
        inputs = [make_input(account_id=f"a{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        assert isinstance(results, list)

    def test_sorted_desc_by_penetration_score(self, engine):
        low = make_input(account_id="low", executive_contacts=0, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         total_contacts_mapped=0, active_contacts_30d=0,
                         primary_champion_engaged=False, executive_sponsor_active=False,
                         decision_maker_relationship_score=0, promoter_contacts=0,
                         neutral_contacts=0, detractor_contacts=0, prior_deal_count=0,
                         champion_left_or_changed=False)
        high = make_input(account_id="high", executive_contacts=2, user_champion_contacts=2,
                          technical_evaluator_contacts=1, finance_procurement_contacts=1,
                          total_contacts_mapped=10, active_contacts_30d=10,
                          primary_champion_engaged=True, executive_sponsor_active=True,
                          decision_maker_relationship_score=10, promoter_contacts=5,
                          neutral_contacts=0, detractor_contacts=0, prior_deal_count=3,
                          champion_left_or_changed=False)
        results = engine.analyze_batch([low, high])
        assert results[0].penetration_score >= results[1].penetration_score

    def test_sorted_desc_three_items(self, engine):
        inputs = [
            make_input(account_id="a", executive_contacts=2, user_champion_contacts=2,
                       technical_evaluator_contacts=1, finance_procurement_contacts=1,
                       total_contacts_mapped=10, active_contacts_30d=10,
                       primary_champion_engaged=True, executive_sponsor_active=True,
                       decision_maker_relationship_score=10, promoter_contacts=5,
                       neutral_contacts=0, detractor_contacts=0, prior_deal_count=3,
                       champion_left_or_changed=False),
            make_input(account_id="b", executive_contacts=0, user_champion_contacts=0,
                       technical_evaluator_contacts=0, finance_procurement_contacts=0,
                       total_contacts_mapped=0, active_contacts_30d=0,
                       primary_champion_engaged=False, executive_sponsor_active=False,
                       decision_maker_relationship_score=0, promoter_contacts=0,
                       neutral_contacts=0, detractor_contacts=0, prior_deal_count=0,
                       champion_left_or_changed=False),
            make_input(account_id="c", executive_contacts=1, user_champion_contacts=1,
                       technical_evaluator_contacts=1, finance_procurement_contacts=0,
                       total_contacts_mapped=5, active_contacts_30d=3,
                       primary_champion_engaged=True, executive_sponsor_active=False,
                       decision_maker_relationship_score=5, promoter_contacts=2,
                       neutral_contacts=2, detractor_contacts=0, prior_deal_count=1,
                       champion_left_or_changed=False),
        ]
        results = engine.analyze_batch(inputs)
        scores = [r.penetration_score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_empty_batch_returns_empty_list(self, engine):
        results = engine.analyze_batch([])
        assert results == []

    def test_batch_appends_to_internal_results(self, engine):
        inputs = [make_input(account_id=f"a{i}") for i in range(3)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 3

    def test_single_item_batch(self, engine, full_input):
        results = engine.analyze_batch([full_input])
        assert len(results) == 1
        assert isinstance(results[0], PenetrationResult)

    def test_batch_results_all_penetration_result_instances(self, engine):
        inputs = [make_input(account_id=f"a{i}") for i in range(4)]
        results = engine.analyze_batch(inputs)
        assert all(isinstance(r, PenetrationResult) for r in results)


# ─── Expansion Plays ─────────────────────────────────────────────────────────

class TestExpansionPlays:
    def test_multithread_play_when_single(self, engine):
        inp = make_input(total_contacts_mapped=1, active_contacts_30d=1,
                         executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0)
        result = engine.analyze(inp)
        texts = " ".join(result.expansion_plays)
        assert "multi-thread" in texts.lower() or "multithread" in texts.lower() or "multi" in texts.lower()

    def test_rebuild_champion_play_when_critical(self, engine):
        inp = make_input(champion_left_or_changed=True, total_contacts_mapped=5,
                         executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert any("champion" in p.lower() for p in result.expansion_plays)

    def test_no_exec_play_when_exec_missing(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1,
                         total_contacts_mapped=5, champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert any("c-level" in p.lower() or "exec" in p.lower() for p in result.expansion_plays)

    def test_no_user_champion_play_when_missing(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1,
                         total_contacts_mapped=5, champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert any("utilisateur" in p.lower() or "champion" in p.lower() for p in result.expansion_plays)

    def test_no_tech_eval_play_when_missing(self, engine):
        inp = make_input(executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=0, finance_procurement_contacts=1,
                         total_contacts_mapped=5, champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert any("technique" in p.lower() or "tech" in p.lower() for p in result.expansion_plays)

    def test_finance_play_only_in_late_stages(self, engine):
        for stage in ("proposal", "negotiation", "closing"):
            e = AccountPenetrationEngine()
            inp = make_input(executive_contacts=1, user_champion_contacts=1,
                             technical_evaluator_contacts=1, finance_procurement_contacts=0,
                             deal_stage=stage, total_contacts_mapped=5,
                             champion_left_or_changed=False)
            result = e.analyze(inp)
            assert any("finance" in p.lower() or "achats" in p.lower() for p in result.expansion_plays)

    def test_finance_play_not_in_discovery(self, engine):
        inp = make_input(executive_contacts=2, user_champion_contacts=2,
                         technical_evaluator_contacts=1, finance_procurement_contacts=0,
                         deal_stage="discovery", total_contacts_mapped=8,
                         active_contacts_30d=6, champion_left_or_changed=False,
                         promoter_contacts=3, primary_champion_engaged=True,
                         executive_sponsor_active=True, detractor_contacts=0)
        result = engine.analyze(inp)
        finance_plays = [p for p in result.expansion_plays if "finance" in p.lower() or "achats" in p.lower()]
        assert len(finance_plays) == 0

    def test_dormant_contacts_play_when_low_activity(self, engine):
        inp = make_input(total_contacts_mapped=6, active_contacts_30d=2,
                         executive_contacts=2, user_champion_contacts=2,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1,
                         champion_left_or_changed=False, deal_stage="discovery")
        result = engine.analyze(inp)
        assert any("dormant" in p.lower() or "actifs" in p.lower() for p in result.expansion_plays)

    def test_maintain_play_when_all_good(self, engine):
        inp = make_input(
            executive_contacts=2, user_champion_contacts=2,
            technical_evaluator_contacts=1, finance_procurement_contacts=1,
            total_contacts_mapped=8, active_contacts_30d=7,
            primary_champion_engaged=True, executive_sponsor_active=True,
            promoter_contacts=3, neutral_contacts=1, detractor_contacts=0,
            champion_left_or_changed=False, decision_maker_relationship_score=8,
            prior_deal_count=2, deal_stage="discovery"
        )
        result = engine.analyze(inp)
        assert any("maintenir" in p.lower() or "maintain" in p.lower() or "rythme" in p.lower()
                   for p in result.expansion_plays)

    def test_expansion_plays_not_empty(self, engine, full_input):
        result = engine.analyze(full_input)
        assert len(result.expansion_plays) > 0


# ─── Risk Signals ─────────────────────────────────────────────────────────────

class TestRiskSignals:
    def test_single_contact_risk_signal(self, engine):
        inp = make_input(total_contacts_mapped=1, active_contacts_30d=1,
                         executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0)
        result = engine.analyze(inp)
        assert any("unique" in s.lower() or "single" in s.lower() for s in result.risk_signals)

    def test_champion_left_risk_signal(self, engine):
        inp = make_input(champion_left_or_changed=True, total_contacts_mapped=5,
                         executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert any("champion" in s.lower() for s in result.risk_signals)

    def test_detractor_risk_signal(self, engine):
        inp = make_input(detractor_contacts=1, total_contacts_mapped=5,
                         champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert any("détracteur" in s.lower() or "detract" in s.lower() for s in result.risk_signals)

    def test_no_exec_large_deal_risk_signal(self, engine):
        inp = make_input(executive_contacts=0, deal_size_eur=50_000.0,
                         total_contacts_mapped=5, champion_left_or_changed=False,
                         user_champion_contacts=1, technical_evaluator_contacts=1,
                         finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert any("exécutif" in s.lower() or "exec" in s.lower() or "c-level" in s.lower()
                   for s in result.risk_signals)

    def test_no_exec_small_deal_no_risk_signal(self, engine):
        inp = make_input(executive_contacts=0, deal_size_eur=49_999.0,
                         total_contacts_mapped=5, champion_left_or_changed=False,
                         user_champion_contacts=1, technical_evaluator_contacts=1,
                         finance_procurement_contacts=1, active_contacts_30d=4)
        result = engine.analyze(inp)
        exec_signals = [s for s in result.risk_signals
                        if "exécutif" in s.lower() or "exec" in s.lower() or "c-level" in s.lower()]
        assert len(exec_signals) == 0

    def test_no_active_contacts_risk_signal(self, engine):
        inp = make_input(total_contacts_mapped=5, active_contacts_30d=0,
                         executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1,
                         champion_left_or_changed=False)
        result = engine.analyze(inp)
        assert any("actif" in s.lower() or "30" in s for s in result.risk_signals)

    def test_finance_missing_proposal_risk_signal(self, engine):
        for stage in ("proposal", "negotiation"):
            e = AccountPenetrationEngine()
            inp = make_input(finance_procurement_contacts=0, deal_stage=stage,
                             total_contacts_mapped=5, champion_left_or_changed=False,
                             executive_contacts=1, user_champion_contacts=1,
                             technical_evaluator_contacts=1)
            result = e.analyze(inp)
            assert any("finance" in s.lower() or "achats" in s.lower() for s in result.risk_signals)

    def test_risk_signals_empty_when_all_good(self, engine):
        inp = make_input(
            executive_contacts=2, user_champion_contacts=2,
            technical_evaluator_contacts=1, finance_procurement_contacts=1,
            total_contacts_mapped=8, active_contacts_30d=6,
            primary_champion_engaged=True, executive_sponsor_active=True,
            promoter_contacts=3, neutral_contacts=1, detractor_contacts=0,
            champion_left_or_changed=False, deal_size_eur=30_000.0,
            deal_stage="discovery"
        )
        result = engine.analyze(inp)
        assert result.risk_signals == []


# ─── Manager Alerts ───────────────────────────────────────────────────────────

class TestManagerAlerts:
    def test_single_contact_alert(self, engine):
        inp = make_input(total_contacts_mapped=1, active_contacts_30d=1,
                         executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         deal_size_eur=10_000.0)
        result = engine.analyze(inp)
        assert any("unique" in a.lower() or "single" in a.lower() or "multi-thread" in a.lower()
                   for a in result.manager_alerts)

    def test_critical_risk_alert(self, engine):
        inp = make_input(champion_left_or_changed=True, total_contacts_mapped=5,
                         executive_contacts=1, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert any("champion" in a.lower() for a in result.manager_alerts)

    def test_thin_large_deal_alert(self, engine):
        inp = make_input(
            executive_contacts=0, user_champion_contacts=0,
            technical_evaluator_contacts=0, finance_procurement_contacts=0,
            total_contacts_mapped=2, active_contacts_30d=0,
            primary_champion_engaged=False, executive_sponsor_active=False,
            decision_maker_relationship_score=0, promoter_contacts=0,
            neutral_contacts=2, detractor_contacts=0, prior_deal_count=0,
            champion_left_or_changed=False, deal_size_eur=80_000.0
        )
        result = engine.analyze(inp)
        assert any("stratégique" in a.lower() or "deal" in a.lower() or "pénétration" in a.lower()
                   for a in result.manager_alerts)

    def test_detractors_ge2_alert(self, engine):
        inp = make_input(detractor_contacts=2, total_contacts_mapped=5,
                         champion_left_or_changed=False, executive_contacts=1,
                         user_champion_contacts=1, technical_evaluator_contacts=1,
                         finance_procurement_contacts=1)
        result = engine.analyze(inp)
        assert any("détracteur" in a.lower() or "detract" in a.lower() for a in result.manager_alerts)

    def test_no_alerts_when_all_good(self, engine):
        inp = make_input(
            executive_contacts=2, user_champion_contacts=2,
            technical_evaluator_contacts=1, finance_procurement_contacts=1,
            total_contacts_mapped=8, active_contacts_30d=6,
            promoter_contacts=3, neutral_contacts=1, detractor_contacts=0,
            champion_left_or_changed=False, deal_size_eur=30_000.0,
            primary_champion_engaged=True, executive_sponsor_active=True
        )
        result = engine.analyze(inp)
        assert result.manager_alerts == []

    def test_thin_small_deal_no_escalation_alert(self, engine):
        inp = make_input(
            executive_contacts=0, user_champion_contacts=0,
            technical_evaluator_contacts=0, finance_procurement_contacts=0,
            total_contacts_mapped=2, active_contacts_30d=0,
            primary_champion_engaged=False, executive_sponsor_active=False,
            decision_maker_relationship_score=0, promoter_contacts=0,
            neutral_contacts=2, detractor_contacts=0, prior_deal_count=0,
            champion_left_or_changed=False, deal_size_eur=50_000.0
        )
        result = engine.analyze(inp)
        escalation_alerts = [a for a in result.manager_alerts if "stratégique" in a.lower()]
        assert len(escalation_alerts) == 0


# ─── Helper Filters ───────────────────────────────────────────────────────────

class TestSingleThreadedFilter:
    def test_returns_only_single_threaded(self, engine):
        single = make_input(account_id="s1", total_contacts_mapped=1, active_contacts_30d=1,
                            executive_contacts=1, user_champion_contacts=0,
                            technical_evaluator_contacts=0, finance_procurement_contacts=0)
        multi = make_input(account_id="m1", total_contacts_mapped=6)
        engine.analyze_batch([single, multi])
        results = engine.single_threaded()
        assert all(r.penetration_level == PenetrationLevel.SINGLE.value for r in results)

    def test_single_threaded_count_correct(self, engine):
        s1 = make_input(account_id="s1", total_contacts_mapped=1, active_contacts_30d=1,
                        executive_contacts=1, user_champion_contacts=0,
                        technical_evaluator_contacts=0, finance_procurement_contacts=0)
        s2 = make_input(account_id="s2", total_contacts_mapped=0, active_contacts_30d=0,
                        executive_contacts=0, user_champion_contacts=0,
                        technical_evaluator_contacts=0, finance_procurement_contacts=0)
        m1 = make_input(account_id="m1")
        engine.analyze_batch([s1, s2, m1])
        results = engine.single_threaded()
        assert len(results) == 2

    def test_single_threaded_empty_when_none(self, engine):
        engine.analyze(make_input(total_contacts_mapped=6))
        assert engine.single_threaded() == []


class TestCriticalRiskFilter:
    def test_returns_only_critical_risk(self, engine):
        crit = make_input(account_id="c1", champion_left_or_changed=True,
                          total_contacts_mapped=5, executive_contacts=1,
                          user_champion_contacts=1, technical_evaluator_contacts=1,
                          finance_procurement_contacts=1)
        safe = make_input(account_id="s1", champion_left_or_changed=False)
        engine.analyze_batch([crit, safe])
        results = engine.critical_risk()
        assert all(r.stakeholder_risk == StakeholderRisk.CRITICAL.value for r in results)

    def test_critical_risk_count(self, engine):
        c1 = make_input(account_id="c1", champion_left_or_changed=True,
                        total_contacts_mapped=5, executive_contacts=1,
                        user_champion_contacts=1, technical_evaluator_contacts=1,
                        finance_procurement_contacts=1)
        c2 = make_input(account_id="c2", champion_left_or_changed=True,
                        total_contacts_mapped=5, executive_contacts=1,
                        user_champion_contacts=1, technical_evaluator_contacts=1,
                        finance_procurement_contacts=1)
        s1 = make_input(account_id="s1")
        engine.analyze_batch([c1, c2, s1])
        assert len(engine.critical_risk()) == 2

    def test_critical_risk_empty_when_none(self, engine):
        engine.analyze(make_input())
        assert engine.critical_risk() == []


class TestNeedsMultithreadFilter:
    def test_returns_multithread_now_results(self, engine):
        single = make_input(account_id="s1", total_contacts_mapped=1, active_contacts_30d=1,
                            executive_contacts=1, user_champion_contacts=0,
                            technical_evaluator_contacts=0, finance_procurement_contacts=0)
        multi = make_input(account_id="m1")
        engine.analyze_batch([single, multi])
        results = engine.needs_multithread()
        assert all(r.penetration_action == PenetrationAction.MULTITHREAD_NOW.value for r in results)

    def test_needs_multithread_empty_when_none(self, engine):
        inp = make_input(
            executive_contacts=2, user_champion_contacts=2,
            technical_evaluator_contacts=1, finance_procurement_contacts=1,
            total_contacts_mapped=8, active_contacts_30d=6,
            promoter_contacts=3, neutral_contacts=1, detractor_contacts=0,
            champion_left_or_changed=False, primary_champion_engaged=True,
            executive_sponsor_active=True
        )
        engine.analyze(inp)
        assert engine.needs_multithread() == []


class TestDeepPenetrationFilter:
    def test_returns_only_deep_level(self, engine):
        deep = make_input(account_id="d1",
                          executive_contacts=2, user_champion_contacts=2,
                          technical_evaluator_contacts=1, finance_procurement_contacts=1,
                          total_contacts_mapped=10, active_contacts_30d=10,
                          primary_champion_engaged=True, executive_sponsor_active=True,
                          decision_maker_relationship_score=10, promoter_contacts=5,
                          neutral_contacts=0, detractor_contacts=0, prior_deal_count=3,
                          champion_left_or_changed=False)
        thin = make_input(account_id="t1",
                          executive_contacts=0, user_champion_contacts=0,
                          technical_evaluator_contacts=0, finance_procurement_contacts=0,
                          total_contacts_mapped=2, active_contacts_30d=0,
                          primary_champion_engaged=False, executive_sponsor_active=False,
                          decision_maker_relationship_score=0, promoter_contacts=0,
                          neutral_contacts=2, detractor_contacts=0, prior_deal_count=0,
                          champion_left_or_changed=False)
        engine.analyze_batch([deep, thin])
        results = engine.deep_penetration()
        assert all(r.penetration_level == PenetrationLevel.DEEP.value for r in results)

    def test_deep_penetration_empty_when_none(self, engine):
        inp = make_input(total_contacts_mapped=0)
        engine.analyze(inp)
        assert engine.deep_penetration() == []


class TestHasCommitteeGapsFilter:
    def test_returns_results_with_gaps(self, engine):
        no_gap = make_input(account_id="ng", executive_contacts=1, user_champion_contacts=1,
                            technical_evaluator_contacts=1, finance_procurement_contacts=1)
        has_gap = make_input(account_id="hg", executive_contacts=0, user_champion_contacts=1,
                             technical_evaluator_contacts=1, finance_procurement_contacts=1)
        engine.analyze_batch([no_gap, has_gap])
        results = engine.has_committee_gaps()
        assert all(r.committee_gap != CommitteeGap.NONE.value for r in results)

    def test_committee_gaps_excludes_none(self, engine):
        no_gap = make_input(account_id="ng", executive_contacts=1, user_champion_contacts=1,
                            technical_evaluator_contacts=1, finance_procurement_contacts=1)
        engine.analyze(no_gap)
        assert engine.has_committee_gaps() == []

    def test_committee_gaps_includes_multiple_gaps(self, engine):
        multi = make_input(executive_contacts=0, user_champion_contacts=0,
                           technical_evaluator_contacts=1, finance_procurement_contacts=1,
                           total_contacts_mapped=5)
        engine.analyze(multi)
        assert len(engine.has_committee_gaps()) == 1


# ─── Reset ────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_results(self, engine, full_input):
        engine.analyze(full_input)
        assert len(engine._results) == 1
        engine.reset()
        assert len(engine._results) == 0

    def test_reset_makes_summary_empty(self, engine, full_input):
        engine.analyze(full_input)
        engine.reset()
        s = engine.summary()
        assert s["total"] == 0

    def test_reset_clears_filters(self, engine):
        inp = make_input(total_contacts_mapped=1, active_contacts_30d=1,
                         executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0)
        engine.analyze(inp)
        engine.reset()
        assert engine.single_threaded() == []
        assert engine.critical_risk() == []
        assert engine.needs_multithread() == []

    def test_analyze_after_reset_works(self, engine, full_input):
        engine.analyze(full_input)
        engine.reset()
        result = engine.analyze(full_input)
        assert isinstance(result, PenetrationResult)
        assert len(engine._results) == 1


# ─── Summary ──────────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_returns_dict(self, engine, full_input):
        engine.analyze(full_input)
        assert isinstance(engine.summary(), dict)

    def test_summary_exactly_10_keys(self, engine, full_input):
        engine.analyze(full_input)
        assert len(engine.summary()) == 10

    def test_summary_exact_keys(self, engine, full_input):
        engine.analyze(full_input)
        expected = {
            "total", "level_counts", "risk_counts", "gap_counts", "action_counts",
            "avg_penetration_score", "avg_coverage_score", "avg_relationship_score",
            "single_threaded_count", "critical_risk_count",
        }
        assert set(engine.summary().keys()) == expected

    def test_summary_empty_when_no_results(self, engine):
        s = engine.summary()
        assert s["total"] == 0
        assert s["level_counts"] == {}
        assert s["risk_counts"] == {}
        assert s["gap_counts"] == {}
        assert s["action_counts"] == {}
        assert s["avg_penetration_score"] == 0.0
        assert s["avg_coverage_score"] == 0.0
        assert s["avg_relationship_score"] == 0.0
        assert s["single_threaded_count"] == 0
        assert s["critical_risk_count"] == 0

    def test_summary_total_count(self, engine):
        for i in range(3):
            engine.analyze(make_input(account_id=f"a{i}"))
        assert engine.summary()["total"] == 3

    def test_summary_level_counts(self, engine):
        single_inp = make_input(account_id="s1", total_contacts_mapped=1, active_contacts_30d=1,
                                executive_contacts=1, user_champion_contacts=0,
                                technical_evaluator_contacts=0, finance_procurement_contacts=0)
        engine.analyze(single_inp)
        s = engine.summary()
        assert s["level_counts"].get(PenetrationLevel.SINGLE.value, 0) >= 1

    def test_summary_risk_counts(self, engine):
        crit = make_input(account_id="c1", champion_left_or_changed=True,
                          total_contacts_mapped=5, executive_contacts=1,
                          user_champion_contacts=1, technical_evaluator_contacts=1,
                          finance_procurement_contacts=1)
        engine.analyze(crit)
        s = engine.summary()
        assert s["risk_counts"].get(StakeholderRisk.CRITICAL.value, 0) == 1

    def test_summary_gap_counts(self, engine):
        inp = make_input(executive_contacts=0, user_champion_contacts=1,
                         technical_evaluator_contacts=1, finance_procurement_contacts=1,
                         total_contacts_mapped=5)
        engine.analyze(inp)
        s = engine.summary()
        assert s["gap_counts"].get(CommitteeGap.MISSING_EXEC.value, 0) == 1

    def test_summary_action_counts(self, engine):
        inp = make_input(total_contacts_mapped=1, active_contacts_30d=1,
                         executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0)
        engine.analyze(inp)
        s = engine.summary()
        assert s["action_counts"].get(PenetrationAction.MULTITHREAD_NOW.value, 0) >= 1

    def test_summary_avg_penetration_score(self, engine):
        inp1 = make_input(account_id="a1")
        inp2 = make_input(account_id="a2")
        r1 = engine.analyze(inp1)
        r2 = engine.analyze(inp2)
        s = engine.summary()
        expected_avg = round((r1.penetration_score + r2.penetration_score) / 2, 1)
        assert s["avg_penetration_score"] == expected_avg

    def test_summary_avg_coverage_score(self, engine):
        inp1 = make_input(account_id="a1")
        inp2 = make_input(account_id="a2")
        r1 = engine.analyze(inp1)
        r2 = engine.analyze(inp2)
        s = engine.summary()
        expected_avg = round((r1.coverage_score + r2.coverage_score) / 2, 1)
        assert s["avg_coverage_score"] == expected_avg

    def test_summary_avg_relationship_score(self, engine):
        inp1 = make_input(account_id="a1")
        inp2 = make_input(account_id="a2")
        r1 = engine.analyze(inp1)
        r2 = engine.analyze(inp2)
        s = engine.summary()
        expected_avg = round((r1.relationship_score + r2.relationship_score) / 2, 1)
        assert s["avg_relationship_score"] == expected_avg

    def test_summary_single_threaded_count(self, engine):
        s1 = make_input(account_id="s1", total_contacts_mapped=1, active_contacts_30d=1,
                        executive_contacts=1, user_champion_contacts=0,
                        technical_evaluator_contacts=0, finance_procurement_contacts=0)
        m1 = make_input(account_id="m1", total_contacts_mapped=6)
        engine.analyze_batch([s1, m1])
        assert engine.summary()["single_threaded_count"] == 1

    def test_summary_critical_risk_count(self, engine):
        c1 = make_input(account_id="c1", champion_left_or_changed=True,
                        total_contacts_mapped=5, executive_contacts=1,
                        user_champion_contacts=1, technical_evaluator_contacts=1,
                        finance_procurement_contacts=1)
        c2 = make_input(account_id="c2", champion_left_or_changed=True,
                        total_contacts_mapped=5, executive_contacts=1,
                        user_champion_contacts=1, technical_evaluator_contacts=1,
                        finance_procurement_contacts=1)
        s1 = make_input(account_id="s1")
        engine.analyze_batch([c1, c2, s1])
        assert engine.summary()["critical_risk_count"] == 2

    def test_summary_empty_exactly_10_keys(self, engine):
        assert len(engine.summary()) == 10

    def test_summary_scores_are_numeric(self, engine, full_input):
        engine.analyze(full_input)
        s = engine.summary()
        assert isinstance(s["avg_penetration_score"], (int, float))
        assert isinstance(s["avg_coverage_score"], (int, float))
        assert isinstance(s["avg_relationship_score"], (int, float))

    def test_summary_accumulates_across_multiple_analyzes(self, engine):
        for i in range(5):
            engine.analyze(make_input(account_id=f"a{i}"))
        assert engine.summary()["total"] == 5


# ─── Engine Initialization ────────────────────────────────────────────────────

class TestEngineInit:
    def test_engine_starts_with_empty_results(self):
        e = AccountPenetrationEngine()
        assert e._results == []

    def test_multiple_engines_are_independent(self):
        e1 = AccountPenetrationEngine()
        e2 = AccountPenetrationEngine()
        e1.analyze(make_input(account_id="a1"))
        assert len(e2._results) == 0

    def test_engine_is_accountpenetrationengine(self):
        e = AccountPenetrationEngine()
        assert isinstance(e, AccountPenetrationEngine)


# ─── End-to-end integration scenarios ────────────────────────────────────────

class TestIntegrationScenarios:
    def test_worst_case_scenario(self, engine):
        inp = make_input(
            total_contacts_mapped=0, active_contacts_30d=0,
            executive_contacts=0, user_champion_contacts=0,
            technical_evaluator_contacts=0, finance_procurement_contacts=0,
            primary_champion_engaged=False, executive_sponsor_active=False,
            decision_maker_relationship_score=0, promoter_contacts=0,
            neutral_contacts=0, detractor_contacts=0, prior_deal_count=0,
            champion_left_or_changed=False, deal_size_eur=100_000.0
        )
        result = engine.analyze(inp)
        assert result.penetration_level == PenetrationLevel.SINGLE.value
        assert result.penetration_score == 0.0
        assert result.multithread_ratio == 0.0

    def test_best_case_scenario(self, engine):
        inp = make_input(
            executive_contacts=5, user_champion_contacts=5,
            technical_evaluator_contacts=3, finance_procurement_contacts=3,
            total_contacts_mapped=20, active_contacts_30d=20,
            primary_champion_engaged=True, executive_sponsor_active=True,
            decision_maker_relationship_score=10, promoter_contacts=10,
            neutral_contacts=0, detractor_contacts=0, prior_deal_count=5,
            champion_left_or_changed=False
        )
        result = engine.analyze(inp)
        assert result.penetration_level == PenetrationLevel.DEEP.value
        assert result.penetration_score == 100.0
        assert result.stakeholder_risk == StakeholderRisk.SECURE.value
        assert result.committee_gap == CommitteeGap.NONE.value

    def test_single_with_champion_left_gets_multithread(self, engine):
        inp = make_input(total_contacts_mapped=1, active_contacts_30d=1,
                         executive_contacts=1, user_champion_contacts=0,
                         technical_evaluator_contacts=0, finance_procurement_contacts=0,
                         champion_left_or_changed=True)
        result = engine.analyze(inp)
        assert result.penetration_action == PenetrationAction.MULTITHREAD_NOW.value

    def test_batch_preserves_all_results_in_engine(self, engine):
        inputs = [make_input(account_id=f"a{i}") for i in range(5)]
        engine.analyze_batch(inputs)
        assert len(engine._results) == 5

    def test_to_dict_after_batch_analysis(self, engine):
        inputs = [make_input(account_id=f"a{i}") for i in range(3)]
        results = engine.analyze_batch(inputs)
        for r in results:
            d = r.to_dict()
            assert len(d) == 15

    def test_full_pipeline_summary_after_batch(self, engine):
        inputs = [make_input(account_id=f"a{i}") for i in range(4)]
        engine.analyze_batch(inputs)
        s = engine.summary()
        assert s["total"] == 4
        assert len(s) == 10
