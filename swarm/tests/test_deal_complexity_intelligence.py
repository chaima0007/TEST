"""Comprehensive pytest test suite for DealComplexityIntelligence."""
from __future__ import annotations

import pytest

from swarm.intelligence.deal_complexity_intelligence import (
    ComplexityAction,
    ComplexityDimension,
    ComplexityRisk,
    ComplexityTier,
    DealComplexityInput,
    DealComplexityIntelligence,
    DealComplexityResult,
    _complexity_action,
    _complexity_risk,
    _complexity_summary,
    _complexity_tier,
    _composite,
    _legal_complexity_score,
    _people_complexity_score,
    _primary_dimension,
    _process_complexity_score,
    _technology_complexity_score,
    _win_probability_impact,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def enterprise_input() -> DealComplexityInput:
    return DealComplexityInput(
        deal_id="deal_001",
        rep_id="rep_001",
        deal_name="Acme Enterprise Suite",
        deal_value_usd=750000.0,
        stakeholder_count=8,
        department_count=4,
        legal_review_required=1,
        security_review_required=1,
        procurement_involvement=1,
        custom_contract_required=1,
        integration_complexity_score=85.0,
        multi_year_deal=1,
        competitive_deal=1,
        proof_of_concept_required=1,
        deal_stage=2,
        industry_regulatory_complexity=70.0,
        geographic_complexity=2,
        pricing_complexity_score=60.0,
        existing_tech_debt_score=55.0,
        executive_alignment_required=1,
        partner_involvement_required=1,
        estimated_implementation_months=12,
    )


@pytest.fixture
def simple_input() -> DealComplexityInput:
    """Minimal deal — all booleans off, all numeric scores zero."""
    return DealComplexityInput(
        deal_id="deal_simple",
        rep_id="rep_simple",
        deal_name="Simple Deal",
        deal_value_usd=10000.0,
        stakeholder_count=1,
        department_count=1,
        legal_review_required=0,
        security_review_required=0,
        procurement_involvement=0,
        custom_contract_required=0,
        integration_complexity_score=0.0,
        multi_year_deal=0,
        competitive_deal=0,
        proof_of_concept_required=0,
        deal_stage=1,
        industry_regulatory_complexity=0.0,
        geographic_complexity=0,
        pricing_complexity_score=0.0,
        existing_tech_debt_score=0.0,
        executive_alignment_required=0,
        partner_involvement_required=0,
        estimated_implementation_months=1,
    )


@pytest.fixture
def intel() -> DealComplexityIntelligence:
    return DealComplexityIntelligence()


# ---------------------------------------------------------------------------
# Enum value tests
# ---------------------------------------------------------------------------


class TestEnumValues:
    def test_complexity_tier_simple(self):
        assert ComplexityTier.SIMPLE.value == "simple"

    def test_complexity_tier_standard(self):
        assert ComplexityTier.STANDARD.value == "standard"

    def test_complexity_tier_complex(self):
        assert ComplexityTier.COMPLEX.value == "complex"

    def test_complexity_tier_enterprise(self):
        assert ComplexityTier.ENTERPRISE.value == "enterprise"

    def test_complexity_tier_members(self):
        members = {t.value for t in ComplexityTier}
        assert members == {"simple", "standard", "complex", "enterprise"}

    def test_complexity_risk_low(self):
        assert ComplexityRisk.LOW.value == "low"

    def test_complexity_risk_moderate(self):
        assert ComplexityRisk.MODERATE.value == "moderate"

    def test_complexity_risk_high(self):
        assert ComplexityRisk.HIGH.value == "high"

    def test_complexity_risk_critical(self):
        assert ComplexityRisk.CRITICAL.value == "critical"

    def test_complexity_risk_members(self):
        members = {r.value for r in ComplexityRisk}
        assert members == {"low", "moderate", "high", "critical"}

    def test_complexity_dimension_people(self):
        assert ComplexityDimension.PEOPLE.value == "people"

    def test_complexity_dimension_process(self):
        assert ComplexityDimension.PROCESS.value == "process"

    def test_complexity_dimension_technology(self):
        assert ComplexityDimension.TECHNOLOGY.value == "technology"

    def test_complexity_dimension_legal(self):
        assert ComplexityDimension.LEGAL.value == "legal"

    def test_complexity_dimension_members(self):
        members = {d.value for d in ComplexityDimension}
        assert members == {"people", "process", "technology", "legal"}

    def test_complexity_action_standard_process(self):
        assert ComplexityAction.STANDARD_PROCESS.value == "standard_process"

    def test_complexity_action_assign_solution_engineer(self):
        assert ComplexityAction.ASSIGN_SOLUTION_ENGINEER.value == "assign_solution_engineer"

    def test_complexity_action_executive_sponsor_required(self):
        assert ComplexityAction.EXECUTIVE_SPONSOR_REQUIRED.value == "executive_sponsor_required"

    def test_complexity_action_dedicated_deal_team(self):
        assert ComplexityAction.DEDICATED_DEAL_TEAM.value == "dedicated_deal_team"

    def test_complexity_action_members(self):
        members = {a.value for a in ComplexityAction}
        assert members == {
            "standard_process",
            "assign_solution_engineer",
            "executive_sponsor_required",
            "dedicated_deal_team",
        }

    def test_enums_are_str_subclass(self):
        assert isinstance(ComplexityTier.SIMPLE, str)
        assert isinstance(ComplexityRisk.LOW, str)
        assert isinstance(ComplexityDimension.PEOPLE, str)
        assert isinstance(ComplexityAction.STANDARD_PROCESS, str)


# ---------------------------------------------------------------------------
# DealComplexityInput field tests (22 fields)
# ---------------------------------------------------------------------------


class TestDealComplexityInputFields:
    def test_has_22_fields(self, enterprise_input):
        import dataclasses
        fields = dataclasses.fields(enterprise_input)
        assert len(fields) == 22

    def test_field_deal_id(self, enterprise_input):
        assert enterprise_input.deal_id == "deal_001"

    def test_field_rep_id(self, enterprise_input):
        assert enterprise_input.rep_id == "rep_001"

    def test_field_deal_name(self, enterprise_input):
        assert enterprise_input.deal_name == "Acme Enterprise Suite"

    def test_field_deal_value_usd(self, enterprise_input):
        assert enterprise_input.deal_value_usd == 750000.0

    def test_field_stakeholder_count(self, enterprise_input):
        assert enterprise_input.stakeholder_count == 8

    def test_field_department_count(self, enterprise_input):
        assert enterprise_input.department_count == 4

    def test_field_legal_review_required(self, enterprise_input):
        assert enterprise_input.legal_review_required == 1

    def test_field_security_review_required(self, enterprise_input):
        assert enterprise_input.security_review_required == 1

    def test_field_procurement_involvement(self, enterprise_input):
        assert enterprise_input.procurement_involvement == 1

    def test_field_custom_contract_required(self, enterprise_input):
        assert enterprise_input.custom_contract_required == 1

    def test_field_integration_complexity_score(self, enterprise_input):
        assert enterprise_input.integration_complexity_score == 85.0

    def test_field_multi_year_deal(self, enterprise_input):
        assert enterprise_input.multi_year_deal == 1

    def test_field_competitive_deal(self, enterprise_input):
        assert enterprise_input.competitive_deal == 1

    def test_field_proof_of_concept_required(self, enterprise_input):
        assert enterprise_input.proof_of_concept_required == 1

    def test_field_deal_stage(self, enterprise_input):
        assert enterprise_input.deal_stage == 2

    def test_field_industry_regulatory_complexity(self, enterprise_input):
        assert enterprise_input.industry_regulatory_complexity == 70.0

    def test_field_geographic_complexity(self, enterprise_input):
        assert enterprise_input.geographic_complexity == 2

    def test_field_pricing_complexity_score(self, enterprise_input):
        assert enterprise_input.pricing_complexity_score == 60.0

    def test_field_existing_tech_debt_score(self, enterprise_input):
        assert enterprise_input.existing_tech_debt_score == 55.0

    def test_field_executive_alignment_required(self, enterprise_input):
        assert enterprise_input.executive_alignment_required == 1

    def test_field_partner_involvement_required(self, enterprise_input):
        assert enterprise_input.partner_involvement_required == 1

    def test_field_estimated_implementation_months(self, enterprise_input):
        assert enterprise_input.estimated_implementation_months == 12

    def test_simple_input_all_zero_booleans(self, simple_input):
        assert simple_input.legal_review_required == 0
        assert simple_input.security_review_required == 0
        assert simple_input.procurement_involvement == 0
        assert simple_input.custom_contract_required == 0
        assert simple_input.multi_year_deal == 0
        assert simple_input.competitive_deal == 0
        assert simple_input.proof_of_concept_required == 0
        assert simple_input.executive_alignment_required == 0
        assert simple_input.partner_involvement_required == 0


# ---------------------------------------------------------------------------
# DealComplexityResult to_dict() — exactly 15 keys
# ---------------------------------------------------------------------------


class TestDealComplexityResultToDict:
    def test_to_dict_has_15_keys(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        d = result.to_dict()
        assert len(d) == 15

    def test_to_dict_key_deal_id(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "deal_id" in d

    def test_to_dict_key_rep_id(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "rep_id" in d

    def test_to_dict_key_complexity_tier(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "complexity_tier" in d

    def test_to_dict_key_complexity_risk(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "complexity_risk" in d

    def test_to_dict_key_primary_complexity_dimension(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "primary_complexity_dimension" in d

    def test_to_dict_key_complexity_action(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "complexity_action" in d

    def test_to_dict_key_people_complexity_score(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "people_complexity_score" in d

    def test_to_dict_key_process_complexity_score(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "process_complexity_score" in d

    def test_to_dict_key_technology_complexity_score(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "technology_complexity_score" in d

    def test_to_dict_key_legal_complexity_score(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "legal_complexity_score" in d

    def test_to_dict_key_complexity_composite(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "complexity_composite" in d

    def test_to_dict_key_requires_deal_desk(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "requires_deal_desk" in d

    def test_to_dict_key_needs_executive_sponsor(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "needs_executive_sponsor" in d

    def test_to_dict_key_estimated_win_probability_impact_pct(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "estimated_win_probability_impact_pct" in d

    def test_to_dict_key_complexity_summary(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert "complexity_summary" in d

    def test_to_dict_enum_values_are_strings(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert isinstance(d["complexity_tier"], str)
        assert isinstance(d["complexity_risk"], str)
        assert isinstance(d["primary_complexity_dimension"], str)
        assert isinstance(d["complexity_action"], str)

    def test_to_dict_deal_id_matches(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert d["deal_id"] == "deal_001"

    def test_to_dict_rep_id_matches(self, intel, enterprise_input):
        d = intel.assess(enterprise_input).to_dict()
        assert d["rep_id"] == "rep_001"

    def test_to_dict_exact_keys(self, intel, simple_input):
        d = intel.assess(simple_input).to_dict()
        expected = {
            "deal_id", "rep_id", "complexity_tier", "complexity_risk",
            "primary_complexity_dimension", "complexity_action",
            "people_complexity_score", "process_complexity_score",
            "technology_complexity_score", "legal_complexity_score",
            "complexity_composite", "requires_deal_desk",
            "needs_executive_sponsor", "estimated_win_probability_impact_pct",
            "complexity_summary",
        }
        assert set(d.keys()) == expected


# ---------------------------------------------------------------------------
# People complexity score
# ---------------------------------------------------------------------------


class TestPeopleComplexityScore:
    def _make(self, **kwargs) -> DealComplexityInput:
        base = dict(
            deal_id="x", rep_id="y", deal_name="N", deal_value_usd=0.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        base.update(kwargs)
        return DealComplexityInput(**base)

    def test_zero_score_minimum_inputs(self, simple_input):
        assert _people_complexity_score(simple_input) == 0.0

    def test_stakeholder_count_1_no_contribution(self):
        inp = self._make(stakeholder_count=1)
        assert _people_complexity_score(inp) == 0.0

    def test_stakeholder_count_2_adds_5(self):
        inp = self._make(stakeholder_count=2)
        assert _people_complexity_score(inp) == 5.0

    def test_stakeholder_count_3_adds_12(self):
        inp = self._make(stakeholder_count=3)
        assert _people_complexity_score(inp) == 12.0

    def test_stakeholder_count_5_adds_12(self):
        inp = self._make(stakeholder_count=5)
        assert _people_complexity_score(inp) == 12.0

    def test_stakeholder_count_6_adds_22(self):
        inp = self._make(stakeholder_count=6)
        assert _people_complexity_score(inp) == 22.0

    def test_stakeholder_count_9_adds_22(self):
        inp = self._make(stakeholder_count=9)
        assert _people_complexity_score(inp) == 22.0

    def test_stakeholder_count_10_adds_30(self):
        inp = self._make(stakeholder_count=10)
        assert _people_complexity_score(inp) == 30.0

    def test_stakeholder_count_15_adds_30(self):
        inp = self._make(stakeholder_count=15)
        assert _people_complexity_score(inp) == 30.0

    def test_department_count_1_no_contribution(self):
        inp = self._make(department_count=1)
        assert _people_complexity_score(inp) == 0.0

    def test_department_count_2_adds_8(self):
        inp = self._make(department_count=2)
        assert _people_complexity_score(inp) == 8.0

    def test_department_count_3_adds_17(self):
        inp = self._make(department_count=3)
        assert _people_complexity_score(inp) == 17.0

    def test_department_count_4_adds_17(self):
        inp = self._make(department_count=4)
        assert _people_complexity_score(inp) == 17.0

    def test_department_count_5_adds_25(self):
        inp = self._make(department_count=5)
        assert _people_complexity_score(inp) == 25.0

    def test_executive_alignment_adds_20(self):
        inp = self._make(executive_alignment_required=1)
        assert _people_complexity_score(inp) == 20.0

    def test_no_executive_alignment_no_contribution(self):
        inp = self._make(executive_alignment_required=0)
        assert _people_complexity_score(inp) == 0.0

    def test_geographic_complexity_0_no_contribution(self):
        inp = self._make(geographic_complexity=0)
        assert _people_complexity_score(inp) == 0.0

    def test_geographic_complexity_1_no_contribution(self):
        inp = self._make(geographic_complexity=1)
        assert _people_complexity_score(inp) == 0.0

    def test_geographic_complexity_2_adds_8(self):
        inp = self._make(geographic_complexity=2)
        assert _people_complexity_score(inp) == 8.0

    def test_geographic_complexity_3_adds_15(self):
        inp = self._make(geographic_complexity=3)
        assert _people_complexity_score(inp) == 15.0

    def test_geographic_complexity_4_adds_15(self):
        inp = self._make(geographic_complexity=4)
        assert _people_complexity_score(inp) == 15.0

    def test_competitive_deal_adds_10(self):
        inp = self._make(competitive_deal=1)
        assert _people_complexity_score(inp) == 10.0

    def test_no_competitive_deal_no_contribution(self):
        inp = self._make(competitive_deal=0)
        assert _people_complexity_score(inp) == 0.0

    def test_score_clamped_at_100(self):
        # stakeholder_count>=10 (30) + dept>=5 (25) + exec (20) + geo>=3 (15) + competitive (10) = 100
        inp = self._make(
            stakeholder_count=10, department_count=5,
            executive_alignment_required=1, geographic_complexity=3,
            competitive_deal=1,
        )
        assert _people_complexity_score(inp) == 100.0

    def test_score_non_negative(self, simple_input):
        assert _people_complexity_score(simple_input) >= 0.0

    def test_enterprise_people_score_positive(self, enterprise_input):
        assert _people_complexity_score(enterprise_input) > 0.0


# ---------------------------------------------------------------------------
# Process complexity score
# ---------------------------------------------------------------------------


class TestProcessComplexityScore:
    def _make(self, **kwargs) -> DealComplexityInput:
        base = dict(
            deal_id="x", rep_id="y", deal_name="N", deal_value_usd=0.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        base.update(kwargs)
        return DealComplexityInput(**base)

    def test_zero_score_minimum_inputs(self, simple_input):
        assert _process_complexity_score(simple_input) == 0.0

    def test_procurement_adds_25(self):
        inp = self._make(procurement_involvement=1)
        assert _process_complexity_score(inp) == 25.0

    def test_no_procurement_no_contribution(self):
        inp = self._make(procurement_involvement=0)
        assert _process_complexity_score(inp) == 0.0

    def test_multi_year_adds_20(self):
        inp = self._make(multi_year_deal=1)
        assert _process_complexity_score(inp) == 20.0

    def test_no_multi_year_no_contribution(self):
        inp = self._make(multi_year_deal=0)
        assert _process_complexity_score(inp) == 0.0

    def test_poc_required_adds_20(self):
        inp = self._make(proof_of_concept_required=1)
        assert _process_complexity_score(inp) == 20.0

    def test_no_poc_no_contribution(self):
        inp = self._make(proof_of_concept_required=0)
        assert _process_complexity_score(inp) == 0.0

    def test_implementation_1_month_no_contribution(self):
        inp = self._make(estimated_implementation_months=1)
        assert _process_complexity_score(inp) == 0.0

    def test_implementation_2_months_no_contribution(self):
        inp = self._make(estimated_implementation_months=2)
        assert _process_complexity_score(inp) == 0.0

    def test_implementation_3_months_adds_6(self):
        inp = self._make(estimated_implementation_months=3)
        assert _process_complexity_score(inp) == 6.0

    def test_implementation_5_months_adds_6(self):
        inp = self._make(estimated_implementation_months=5)
        assert _process_complexity_score(inp) == 6.0

    def test_implementation_6_months_adds_13(self):
        inp = self._make(estimated_implementation_months=6)
        assert _process_complexity_score(inp) == 13.0

    def test_implementation_11_months_adds_13(self):
        inp = self._make(estimated_implementation_months=11)
        assert _process_complexity_score(inp) == 13.0

    def test_implementation_12_months_adds_20(self):
        inp = self._make(estimated_implementation_months=12)
        assert _process_complexity_score(inp) == 20.0

    def test_implementation_18_months_adds_20(self):
        inp = self._make(estimated_implementation_months=18)
        assert _process_complexity_score(inp) == 20.0

    def test_partner_involvement_adds_15(self):
        inp = self._make(partner_involvement_required=1)
        assert _process_complexity_score(inp) == 15.0

    def test_no_partner_no_contribution(self):
        inp = self._make(partner_involvement_required=0)
        assert _process_complexity_score(inp) == 0.0

    def test_score_clamped_at_100(self):
        # procurement(25) + multi_year(20) + poc(20) + impl>=12(20) + partner(15) = 100
        inp = self._make(
            procurement_involvement=1, multi_year_deal=1,
            proof_of_concept_required=1, estimated_implementation_months=12,
            partner_involvement_required=1,
        )
        assert _process_complexity_score(inp) == 100.0

    def test_enterprise_process_score_positive(self, enterprise_input):
        assert _process_complexity_score(enterprise_input) > 0.0


# ---------------------------------------------------------------------------
# Technology complexity score
# ---------------------------------------------------------------------------


class TestTechnologyComplexityScore:
    def _make(self, **kwargs) -> DealComplexityInput:
        base = dict(
            deal_id="x", rep_id="y", deal_name="N", deal_value_usd=0.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        base.update(kwargs)
        return DealComplexityInput(**base)

    def test_zero_score_minimum_inputs(self, simple_input):
        assert _technology_complexity_score(simple_input) == 0.0

    def test_integration_score_weight_0_40(self):
        inp = self._make(integration_complexity_score=100.0)
        score = _technology_complexity_score(inp)
        assert score == pytest.approx(40.0, abs=0.2)

    def test_integration_score_partial(self):
        inp = self._make(integration_complexity_score=50.0)
        score = _technology_complexity_score(inp)
        assert score == pytest.approx(20.0, abs=0.2)

    def test_tech_debt_weight_0_30(self):
        inp = self._make(existing_tech_debt_score=100.0)
        score = _technology_complexity_score(inp)
        assert score == pytest.approx(30.0, abs=0.2)

    def test_tech_debt_partial(self):
        inp = self._make(existing_tech_debt_score=50.0)
        score = _technology_complexity_score(inp)
        assert score == pytest.approx(15.0, abs=0.2)

    def test_security_review_adds_20(self):
        inp = self._make(security_review_required=1)
        assert _technology_complexity_score(inp) == 20.0

    def test_no_security_review_no_contribution(self):
        inp = self._make(security_review_required=0)
        assert _technology_complexity_score(inp) == 0.0

    def test_pricing_complexity_weight_0_10(self):
        inp = self._make(pricing_complexity_score=100.0)
        score = _technology_complexity_score(inp)
        assert score == pytest.approx(10.0, abs=0.2)

    def test_pricing_complexity_partial(self):
        inp = self._make(pricing_complexity_score=50.0)
        score = _technology_complexity_score(inp)
        assert score == pytest.approx(5.0, abs=0.2)

    def test_score_clamped_at_100(self):
        # integration(100*0.4=40) + tech_debt(100*0.3=30) + security(20) + pricing(100*0.1=10) = 100
        inp = self._make(
            integration_complexity_score=100.0,
            existing_tech_debt_score=100.0,
            security_review_required=1,
            pricing_complexity_score=100.0,
        )
        assert _technology_complexity_score(inp) == 100.0

    def test_score_non_negative(self, simple_input):
        assert _technology_complexity_score(simple_input) >= 0.0

    def test_enterprise_technology_score_positive(self, enterprise_input):
        assert _technology_complexity_score(enterprise_input) > 0.0

    def test_combined_weights_sum_to_100(self):
        # All inputs at 100 with security gives max 100
        inp = self._make(
            integration_complexity_score=100.0,
            existing_tech_debt_score=100.0,
            security_review_required=1,
            pricing_complexity_score=100.0,
        )
        score = _technology_complexity_score(inp)
        assert 0.0 <= score <= 100.0


# ---------------------------------------------------------------------------
# Legal complexity score
# ---------------------------------------------------------------------------


class TestLegalComplexityScore:
    def _make(self, **kwargs) -> DealComplexityInput:
        base = dict(
            deal_id="x", rep_id="y", deal_name="N", deal_value_usd=0.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        base.update(kwargs)
        return DealComplexityInput(**base)

    def test_zero_score_minimum_inputs(self, simple_input):
        assert _legal_complexity_score(simple_input) == 0.0

    def test_legal_review_adds_30(self):
        inp = self._make(legal_review_required=1)
        assert _legal_complexity_score(inp) == 30.0

    def test_no_legal_review_no_contribution(self):
        inp = self._make(legal_review_required=0)
        assert _legal_complexity_score(inp) == 0.0

    def test_custom_contract_adds_25(self):
        inp = self._make(custom_contract_required=1)
        assert _legal_complexity_score(inp) == 25.0

    def test_no_custom_contract_no_contribution(self):
        inp = self._make(custom_contract_required=0)
        assert _legal_complexity_score(inp) == 0.0

    def test_industry_regulatory_weight_0_25(self):
        inp = self._make(industry_regulatory_complexity=100.0)
        score = _legal_complexity_score(inp)
        assert score == pytest.approx(25.0, abs=0.2)

    def test_industry_regulatory_partial(self):
        inp = self._make(industry_regulatory_complexity=40.0)
        score = _legal_complexity_score(inp)
        assert score == pytest.approx(10.0, abs=0.2)

    def test_security_and_legal_combo_bonus_10(self):
        inp = self._make(security_review_required=1, legal_review_required=1)
        # legal(30) + security+legal combo(10) = 40
        assert _legal_complexity_score(inp) == 40.0

    def test_security_only_no_combo_bonus(self):
        inp = self._make(security_review_required=1, legal_review_required=0)
        assert _legal_complexity_score(inp) == 0.0

    def test_geographic_complexity_0_no_geo_legal(self):
        inp = self._make(geographic_complexity=0)
        assert _legal_complexity_score(inp) == 0.0

    def test_geographic_complexity_1_no_geo_legal(self):
        inp = self._make(geographic_complexity=1)
        assert _legal_complexity_score(inp) == 0.0

    def test_geographic_complexity_2_adds_5(self):
        inp = self._make(geographic_complexity=2)
        assert _legal_complexity_score(inp) == 5.0

    def test_geographic_complexity_3_adds_10(self):
        inp = self._make(geographic_complexity=3)
        assert _legal_complexity_score(inp) == 10.0

    def test_geographic_complexity_5_adds_10(self):
        inp = self._make(geographic_complexity=5)
        assert _legal_complexity_score(inp) == 10.0

    def test_score_clamped_at_100(self):
        # legal(30) + custom(25) + regulatory(100*0.25=25) + combo(10) + geo>=3(10) = 100
        inp = self._make(
            legal_review_required=1, custom_contract_required=1,
            industry_regulatory_complexity=100.0,
            security_review_required=1, geographic_complexity=3,
        )
        assert _legal_complexity_score(inp) == 100.0

    def test_score_non_negative(self, simple_input):
        assert _legal_complexity_score(simple_input) >= 0.0

    def test_enterprise_legal_score_positive(self, enterprise_input):
        assert _legal_complexity_score(enterprise_input) > 0.0


# ---------------------------------------------------------------------------
# Composite formula — equal 0.25 weights
# ---------------------------------------------------------------------------


class TestCompositeFormula:
    def test_all_zeros(self):
        assert _composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_all_100(self):
        assert _composite(100.0, 100.0, 100.0, 100.0) == 100.0

    def test_equal_weights_people(self):
        # Only people non-zero: 100 * 0.25 = 25
        assert _composite(100.0, 0.0, 0.0, 0.0) == 25.0

    def test_equal_weights_process(self):
        assert _composite(0.0, 100.0, 0.0, 0.0) == 25.0

    def test_equal_weights_technology(self):
        assert _composite(0.0, 0.0, 100.0, 0.0) == 25.0

    def test_equal_weights_legal(self):
        assert _composite(0.0, 0.0, 0.0, 100.0) == 25.0

    def test_partial_scores_average(self):
        # 40 * 0.25 * 4 = 40
        assert _composite(40.0, 40.0, 40.0, 40.0) == 40.0

    def test_mixed_scores(self):
        # 60*0.25 + 80*0.25 + 40*0.25 + 20*0.25 = 50
        result = _composite(60.0, 80.0, 40.0, 20.0)
        assert result == pytest.approx(50.0, abs=0.1)

    def test_rounded_to_1_decimal(self):
        result = _composite(33.3, 33.3, 33.3, 33.3)
        # 33.3 * 4 * 0.25 = 33.3
        assert result == pytest.approx(33.3, abs=0.1)

    def test_weights_sum_to_one(self):
        # If each weight is 0.25 and all inputs are 1.0, composite = 1.0
        result = _composite(1.0, 1.0, 1.0, 1.0)
        assert result == pytest.approx(1.0, abs=0.01)

    def test_asymmetric_inputs(self):
        result = _composite(100.0, 0.0, 0.0, 0.0)
        assert result == 25.0

    def test_two_equal_non_zero(self):
        result = _composite(50.0, 50.0, 0.0, 0.0)
        assert result == 25.0


# ---------------------------------------------------------------------------
# Complexity tier thresholds
# ---------------------------------------------------------------------------


class TestComplexityTier:
    def test_composite_0_is_simple(self):
        assert _complexity_tier(0.0) == ComplexityTier.SIMPLE

    def test_composite_24_9_is_simple(self):
        assert _complexity_tier(24.9) == ComplexityTier.SIMPLE

    def test_composite_25_is_standard(self):
        assert _complexity_tier(25.0) == ComplexityTier.STANDARD

    def test_composite_49_9_is_standard(self):
        assert _complexity_tier(49.9) == ComplexityTier.STANDARD

    def test_composite_50_is_complex(self):
        assert _complexity_tier(50.0) == ComplexityTier.COMPLEX

    def test_composite_69_9_is_complex(self):
        assert _complexity_tier(69.9) == ComplexityTier.COMPLEX

    def test_composite_70_is_enterprise(self):
        assert _complexity_tier(70.0) == ComplexityTier.ENTERPRISE

    def test_composite_100_is_enterprise(self):
        assert _complexity_tier(100.0) == ComplexityTier.ENTERPRISE

    def test_boundary_exactly_25(self):
        assert _complexity_tier(25.0) == ComplexityTier.STANDARD

    def test_boundary_exactly_50(self):
        assert _complexity_tier(50.0) == ComplexityTier.COMPLEX

    def test_boundary_exactly_70(self):
        assert _complexity_tier(70.0) == ComplexityTier.ENTERPRISE


# ---------------------------------------------------------------------------
# Complexity risk
# ---------------------------------------------------------------------------


class TestComplexityRisk:
    def _make(self, **kwargs) -> DealComplexityInput:
        base = dict(
            deal_id="x", rep_id="y", deal_name="N", deal_value_usd=0.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        base.update(kwargs)
        return DealComplexityInput(**base)

    def test_composite_0_no_flags_is_low(self):
        inp = self._make()
        assert _complexity_risk(0.0, inp) == ComplexityRisk.LOW

    def test_composite_24_is_low(self):
        inp = self._make()
        assert _complexity_risk(24.0, inp) == ComplexityRisk.LOW

    def test_composite_25_is_moderate(self):
        inp = self._make()
        assert _complexity_risk(25.0, inp) == ComplexityRisk.MODERATE

    def test_composite_49_is_moderate(self):
        inp = self._make()
        assert _complexity_risk(49.0, inp) == ComplexityRisk.MODERATE

    def test_composite_50_is_high(self):
        inp = self._make()
        assert _complexity_risk(50.0, inp) == ComplexityRisk.HIGH

    def test_composite_69_is_high(self):
        inp = self._make()
        assert _complexity_risk(69.0, inp) == ComplexityRisk.HIGH

    def test_composite_70_is_critical(self):
        inp = self._make()
        assert _complexity_risk(70.0, inp) == ComplexityRisk.CRITICAL

    def test_composite_100_is_critical(self):
        inp = self._make()
        assert _complexity_risk(100.0, inp) == ComplexityRisk.CRITICAL

    def test_triple_flag_combo_low_composite_is_critical(self):
        # legal + security + custom_contract => CRITICAL even with low composite
        inp = self._make(legal_review_required=1, security_review_required=1, custom_contract_required=1)
        assert _complexity_risk(10.0, inp) == ComplexityRisk.CRITICAL

    def test_legal_and_security_without_custom_not_critical_at_low_composite(self):
        inp = self._make(legal_review_required=1, security_review_required=1, custom_contract_required=0)
        assert _complexity_risk(10.0, inp) != ComplexityRisk.CRITICAL

    def test_legal_and_custom_without_security_not_critical_at_low_composite(self):
        inp = self._make(legal_review_required=1, security_review_required=0, custom_contract_required=1)
        assert _complexity_risk(10.0, inp) != ComplexityRisk.CRITICAL

    def test_security_and_custom_without_legal_not_critical_at_low_composite(self):
        inp = self._make(legal_review_required=0, security_review_required=1, custom_contract_required=1)
        assert _complexity_risk(10.0, inp) != ComplexityRisk.CRITICAL


# ---------------------------------------------------------------------------
# Primary dimension
# ---------------------------------------------------------------------------


class TestPrimaryDimension:
    def test_people_highest(self):
        assert _primary_dimension(90.0, 70.0, 60.0, 50.0) == ComplexityDimension.PEOPLE

    def test_process_highest(self):
        assert _primary_dimension(10.0, 90.0, 20.0, 30.0) == ComplexityDimension.PROCESS

    def test_technology_highest(self):
        assert _primary_dimension(10.0, 20.0, 80.0, 30.0) == ComplexityDimension.TECHNOLOGY

    def test_legal_highest(self):
        assert _primary_dimension(10.0, 20.0, 30.0, 95.0) == ComplexityDimension.LEGAL

    def test_all_equal_deterministic(self):
        # When all equal, the result should be one of the four dimensions (deterministic)
        result = _primary_dimension(50.0, 50.0, 50.0, 50.0)
        assert result in list(ComplexityDimension)


# ---------------------------------------------------------------------------
# Complexity action
# ---------------------------------------------------------------------------


class TestComplexityAction:
    def _make(self, **kwargs) -> DealComplexityInput:
        base = dict(
            deal_id="x", rep_id="y", deal_name="N", deal_value_usd=0.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        base.update(kwargs)
        return DealComplexityInput(**base)

    def test_low_risk_standard_process(self):
        inp = self._make()
        assert _complexity_action(ComplexityRisk.LOW, inp) == ComplexityAction.STANDARD_PROCESS

    def test_moderate_risk_assign_solution_engineer(self):
        inp = self._make()
        assert _complexity_action(ComplexityRisk.MODERATE, inp) == ComplexityAction.ASSIGN_SOLUTION_ENGINEER

    def test_high_risk_executive_sponsor_required(self):
        inp = self._make()
        assert _complexity_action(ComplexityRisk.HIGH, inp) == ComplexityAction.EXECUTIVE_SPONSOR_REQUIRED

    def test_critical_risk_dedicated_deal_team(self):
        inp = self._make()
        assert _complexity_action(ComplexityRisk.CRITICAL, inp) == ComplexityAction.DEDICATED_DEAL_TEAM


# ---------------------------------------------------------------------------
# Win probability impact
# ---------------------------------------------------------------------------


class TestWinProbabilityImpact:
    def test_composite_0_returns_minus_5(self):
        assert _win_probability_impact(0.0) == -5.0

    def test_composite_24_returns_minus_5(self):
        assert _win_probability_impact(24.9) == -5.0

    def test_composite_25_returns_minus_12(self):
        assert _win_probability_impact(25.0) == -12.0

    def test_composite_49_returns_minus_12(self):
        assert _win_probability_impact(49.9) == -12.0

    def test_composite_50_returns_minus_20(self):
        assert _win_probability_impact(50.0) == -20.0

    def test_composite_69_returns_minus_20(self):
        assert _win_probability_impact(69.9) == -20.0

    def test_composite_70_returns_minus_30(self):
        assert _win_probability_impact(70.0) == -30.0

    def test_composite_100_returns_minus_30(self):
        assert _win_probability_impact(100.0) == -30.0

    def test_boundary_exactly_25(self):
        assert _win_probability_impact(25.0) == -12.0

    def test_boundary_exactly_50(self):
        assert _win_probability_impact(50.0) == -20.0

    def test_boundary_exactly_70(self):
        assert _win_probability_impact(70.0) == -30.0

    def test_all_impacts_are_negative(self):
        for composite in [0.0, 10.0, 25.0, 40.0, 50.0, 65.0, 70.0, 90.0, 100.0]:
            assert _win_probability_impact(composite) < 0.0


# ---------------------------------------------------------------------------
# assess() — core integration tests
# ---------------------------------------------------------------------------


class TestAssess:
    def test_returns_deal_complexity_result(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert isinstance(result, DealComplexityResult)

    def test_deal_id_preserved(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.deal_id == "deal_001"

    def test_rep_id_preserved(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.rep_id == "rep_001"

    def test_enterprise_tier_is_enterprise(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.complexity_tier == ComplexityTier.ENTERPRISE

    def test_enterprise_risk_is_critical(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.complexity_risk == ComplexityRisk.CRITICAL

    def test_enterprise_action_is_dedicated_deal_team(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.complexity_action == ComplexityAction.DEDICATED_DEAL_TEAM

    def test_enterprise_requires_deal_desk(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.requires_deal_desk

    def test_enterprise_needs_executive_sponsor(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.needs_executive_sponsor

    def test_enterprise_win_probability_impact_minus_30(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.estimated_win_probability_impact_pct == -30.0

    def test_enterprise_composite_above_70(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.complexity_composite >= 70.0

    def test_simple_tier_is_simple(self, intel, simple_input):
        result = intel.assess(simple_input)
        assert result.complexity_tier == ComplexityTier.SIMPLE

    def test_simple_risk_is_low(self, intel, simple_input):
        result = intel.assess(simple_input)
        assert result.complexity_risk == ComplexityRisk.LOW

    def test_simple_action_is_standard_process(self, intel, simple_input):
        result = intel.assess(simple_input)
        assert result.complexity_action == ComplexityAction.STANDARD_PROCESS

    def test_simple_not_requires_deal_desk(self, intel, simple_input):
        result = intel.assess(simple_input)
        assert not result.requires_deal_desk

    def test_simple_not_needs_executive_sponsor_due_to_value(self, intel, simple_input):
        # deal_value_usd=10000 < 500000, composite < 75
        result = intel.assess(simple_input)
        assert not result.needs_executive_sponsor

    def test_simple_win_probability_impact_minus_5(self, intel, simple_input):
        result = intel.assess(simple_input)
        assert result.estimated_win_probability_impact_pct == -5.0

    def test_stored_in_results(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        assert intel.get("deal_001") is not None

    def test_people_score_between_0_and_100(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert 0.0 <= result.people_complexity_score <= 100.0

    def test_process_score_between_0_and_100(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert 0.0 <= result.process_complexity_score <= 100.0

    def test_technology_score_between_0_and_100(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert 0.0 <= result.technology_complexity_score <= 100.0

    def test_legal_score_between_0_and_100(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert 0.0 <= result.legal_complexity_score <= 100.0

    def test_composite_between_0_and_100(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert 0.0 <= result.complexity_composite <= 100.0

    def test_composite_matches_formula(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        expected = round(
            result.people_complexity_score * 0.25
            + result.process_complexity_score * 0.25
            + result.technology_complexity_score * 0.25
            + result.legal_complexity_score * 0.25,
            1,
        )
        assert result.complexity_composite == expected

    def test_complexity_summary_is_string(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert isinstance(result.complexity_summary, str)

    def test_complexity_summary_nonempty(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert len(result.complexity_summary) > 0


# ---------------------------------------------------------------------------
# requires_deal_desk boolean logic
# ---------------------------------------------------------------------------


class TestRequiresDealDesk:
    def _make(self, **kwargs) -> DealComplexityInput:
        base = dict(
            deal_id="x", rep_id="y", deal_name="N", deal_value_usd=50000.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        base.update(kwargs)
        return DealComplexityInput(**base)

    def test_legal_and_custom_contract_triggers_deal_desk(self, intel):
        inp = self._make(legal_review_required=1, custom_contract_required=1)
        result = intel.assess(inp)
        assert result.requires_deal_desk

    def test_legal_only_no_deal_desk_at_low_composite(self, intel):
        inp = self._make(legal_review_required=1, custom_contract_required=0)
        result = intel.assess(inp)
        # composite will be low; legal alone doesn't trigger deal desk
        if result.complexity_composite < 60:
            assert not result.requires_deal_desk

    def test_custom_contract_only_no_deal_desk_at_low_composite(self, intel):
        inp = self._make(legal_review_required=0, custom_contract_required=1)
        result = intel.assess(inp)
        if result.complexity_composite < 60:
            assert not result.requires_deal_desk

    def test_high_composite_triggers_deal_desk(self, intel):
        # Build input that produces composite >= 60
        inp = self._make(
            stakeholder_count=10, department_count=5,
            executive_alignment_required=1, geographic_complexity=3,
            competitive_deal=1, procurement_involvement=1, multi_year_deal=1,
            proof_of_concept_required=1, estimated_implementation_months=12,
            partner_involvement_required=1,
            integration_complexity_score=100.0, existing_tech_debt_score=100.0,
            security_review_required=1, pricing_complexity_score=100.0,
            legal_review_required=1, custom_contract_required=1,
            industry_regulatory_complexity=100.0,
        )
        result = intel.assess(inp)
        assert result.requires_deal_desk

    def test_deal_desk_false_when_both_conditions_absent(self, intel, simple_input):
        result = intel.assess(simple_input)
        assert not result.requires_deal_desk


# ---------------------------------------------------------------------------
# needs_executive_sponsor boolean logic
# ---------------------------------------------------------------------------


class TestNeedsExecutiveSponsor:
    def _make(self, **kwargs) -> DealComplexityInput:
        base = dict(
            deal_id="x", rep_id="y", deal_name="N", deal_value_usd=50000.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        base.update(kwargs)
        return DealComplexityInput(**base)

    def test_deal_value_500000_triggers_exec_sponsor(self, intel):
        inp = self._make(deal_value_usd=500000.0)
        result = intel.assess(inp)
        assert result.needs_executive_sponsor

    def test_deal_value_above_500000_triggers_exec_sponsor(self, intel):
        inp = self._make(deal_value_usd=1000000.0)
        result = intel.assess(inp)
        assert result.needs_executive_sponsor

    def test_deal_value_below_500000_no_exec_sponsor_at_low_composite(self, intel):
        inp = self._make(deal_value_usd=499999.0)
        result = intel.assess(inp)
        if result.complexity_composite < 75:
            assert not result.needs_executive_sponsor

    def test_high_composite_75_triggers_exec_sponsor(self, intel):
        # Build deal with composite >= 75
        inp = self._make(
            deal_value_usd=10000.0,
            stakeholder_count=10, department_count=5,
            executive_alignment_required=1, geographic_complexity=3,
            competitive_deal=1, procurement_involvement=1, multi_year_deal=1,
            proof_of_concept_required=1, estimated_implementation_months=12,
            partner_involvement_required=1,
            integration_complexity_score=100.0, existing_tech_debt_score=100.0,
            security_review_required=1, pricing_complexity_score=100.0,
            legal_review_required=1, custom_contract_required=1,
            industry_regulatory_complexity=100.0,
        )
        result = intel.assess(inp)
        assert result.needs_executive_sponsor

    def test_exec_sponsor_false_low_value_low_composite(self, intel, simple_input):
        result = intel.assess(simple_input)
        assert not result.needs_executive_sponsor

    def test_enterprise_fixture_needs_exec_sponsor(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.needs_executive_sponsor


# ---------------------------------------------------------------------------
# assess_batch()
# ---------------------------------------------------------------------------


class TestAssessBatch:
    def test_returns_list(self, intel, enterprise_input, simple_input):
        results = intel.assess_batch([enterprise_input, simple_input])
        assert isinstance(results, list)

    def test_returns_correct_count(self, intel, enterprise_input, simple_input):
        results = intel.assess_batch([enterprise_input, simple_input])
        assert len(results) == 2

    def test_sorted_by_composite_descending(self, intel, enterprise_input, simple_input):
        results = intel.assess_batch([simple_input, enterprise_input])
        composites = [r.complexity_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_batch_with_three_deals_sorted(self, intel):
        inputs = [
            DealComplexityInput(
                deal_id=f"deal_{i}", rep_id="r", deal_name="X",
                deal_value_usd=float(i * 10000),
                stakeholder_count=i, department_count=1, legal_review_required=0,
                security_review_required=0, procurement_involvement=0,
                custom_contract_required=0, integration_complexity_score=float(i * 10),
                multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
                deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
                pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
                executive_alignment_required=0, partner_involvement_required=0,
                estimated_implementation_months=1,
            )
            for i in [1, 5, 9]
        ]
        results = intel.assess_batch(inputs)
        composites = [r.complexity_composite for r in results]
        assert composites == sorted(composites, reverse=True)

    def test_empty_batch_returns_empty_list(self, intel):
        assert intel.assess_batch([]) == []

    def test_single_item_batch(self, intel, enterprise_input):
        results = intel.assess_batch([enterprise_input])
        assert len(results) == 1

    def test_batch_stores_all_results(self, intel, enterprise_input, simple_input):
        intel.assess_batch([enterprise_input, simple_input])
        assert intel.get("deal_001") is not None
        assert intel.get("deal_simple") is not None


# ---------------------------------------------------------------------------
# reset()
# ---------------------------------------------------------------------------


class TestReset:
    def test_reset_clears_results(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        intel.reset()
        assert intel.get("deal_001") is None

    def test_reset_clears_deal_values(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        intel.reset()
        assert intel.high_complexity_pipeline_usd() == 0.0

    def test_reset_clears_all_results(self, intel, enterprise_input, simple_input):
        intel.assess_batch([enterprise_input, simple_input])
        intel.reset()
        assert len(intel.all_deals()) == 0

    def test_reset_allows_reassess(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        intel.reset()
        result = intel.assess(enterprise_input)
        assert result.deal_id == "deal_001"

    def test_reset_summary_returns_zero_total(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        intel.reset()
        s = intel.summary()
        assert s["total"] == 0

    def test_reset_on_empty_intel_no_error(self, intel):
        intel.reset()  # Should not raise


# ---------------------------------------------------------------------------
# by_tier()
# ---------------------------------------------------------------------------


class TestByTier:
    def test_by_tier_enterprise_returns_enterprise_deals(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        enterprise_deals = intel.by_tier(ComplexityTier.ENTERPRISE)
        assert all(r.complexity_tier == ComplexityTier.ENTERPRISE for r in enterprise_deals)

    def test_by_tier_simple_returns_simple_deals(self, intel, simple_input):
        intel.assess(simple_input)
        simple_deals = intel.by_tier(ComplexityTier.SIMPLE)
        assert all(r.complexity_tier == ComplexityTier.SIMPLE for r in simple_deals)

    def test_by_tier_empty_when_no_matching(self, intel, simple_input):
        intel.assess(simple_input)
        enterprise_deals = intel.by_tier(ComplexityTier.ENTERPRISE)
        assert enterprise_deals == []

    def test_by_tier_complex(self, intel):
        inp = DealComplexityInput(
            deal_id="d_complex", rep_id="r", deal_name="X",
            deal_value_usd=100000.0,
            stakeholder_count=6, department_count=3, legal_review_required=0,
            security_review_required=1, procurement_involvement=1,
            custom_contract_required=0, integration_complexity_score=80.0,
            multi_year_deal=1, competitive_deal=1, proof_of_concept_required=0,
            deal_stage=2, industry_regulatory_complexity=20.0, geographic_complexity=1,
            pricing_complexity_score=30.0, existing_tech_debt_score=40.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=6,
        )
        result = intel.assess(inp)
        tier = result.complexity_tier
        tier_results = intel.by_tier(tier)
        assert any(r.deal_id == "d_complex" for r in tier_results)

    def test_by_tier_standard(self, intel):
        inp = DealComplexityInput(
            deal_id="d_standard", rep_id="r", deal_name="X",
            deal_value_usd=20000.0,
            stakeholder_count=3, department_count=2, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=10.0,
            multi_year_deal=0, competitive_deal=1, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=1, partner_involvement_required=0,
            estimated_implementation_months=3,
        )
        result = intel.assess(inp)
        tier = result.complexity_tier
        tier_results = intel.by_tier(tier)
        assert any(r.deal_id == "d_standard" for r in tier_results)


# ---------------------------------------------------------------------------
# by_risk()
# ---------------------------------------------------------------------------


class TestByRisk:
    def test_by_risk_critical_returns_critical_deals(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        critical_deals = intel.by_risk(ComplexityRisk.CRITICAL)
        assert all(r.complexity_risk == ComplexityRisk.CRITICAL for r in critical_deals)

    def test_by_risk_low_returns_low_deals(self, intel, simple_input):
        intel.assess(simple_input)
        low_deals = intel.by_risk(ComplexityRisk.LOW)
        assert all(r.complexity_risk == ComplexityRisk.LOW for r in low_deals)

    def test_by_risk_empty_when_no_matching(self, intel, simple_input):
        intel.assess(simple_input)
        critical_deals = intel.by_risk(ComplexityRisk.CRITICAL)
        assert critical_deals == []

    def test_by_risk_high(self, intel):
        inp = DealComplexityInput(
            deal_id="d_high", rep_id="r", deal_name="X",
            deal_value_usd=200000.0,
            stakeholder_count=6, department_count=3, legal_review_required=0,
            security_review_required=1, procurement_involvement=1,
            custom_contract_required=0, integration_complexity_score=80.0,
            multi_year_deal=1, competitive_deal=1, proof_of_concept_required=0,
            deal_stage=2, industry_regulatory_complexity=20.0, geographic_complexity=1,
            pricing_complexity_score=30.0, existing_tech_debt_score=40.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=6,
        )
        result = intel.assess(inp)
        risk = result.complexity_risk
        risk_results = intel.by_risk(risk)
        assert any(r.deal_id == "d_high" for r in risk_results)


# ---------------------------------------------------------------------------
# deal_desk_queue()
# ---------------------------------------------------------------------------


class TestDealDeskQueue:
    def test_enterprise_in_deal_desk_queue(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        queue = intel.deal_desk_queue()
        assert any(r.deal_id == "deal_001" for r in queue)

    def test_simple_not_in_deal_desk_queue(self, intel, simple_input):
        intel.assess(simple_input)
        queue = intel.deal_desk_queue()
        assert not any(r.deal_id == "deal_simple" for r in queue)

    def test_all_in_queue_require_deal_desk(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        queue = intel.deal_desk_queue()
        assert all(r.requires_deal_desk for r in queue)

    def test_empty_queue_when_no_deal_desk_required(self, intel, simple_input):
        intel.assess(simple_input)
        queue = intel.deal_desk_queue()
        assert queue == []


# ---------------------------------------------------------------------------
# executive_sponsor_queue()
# ---------------------------------------------------------------------------


class TestExecutiveSponsorQueue:
    def test_enterprise_in_exec_sponsor_queue(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        queue = intel.executive_sponsor_queue()
        assert any(r.deal_id == "deal_001" for r in queue)

    def test_simple_not_in_exec_sponsor_queue(self, intel, simple_input):
        intel.assess(simple_input)
        queue = intel.executive_sponsor_queue()
        assert not any(r.deal_id == "deal_simple" for r in queue)

    def test_all_in_queue_need_exec_sponsor(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        queue = intel.executive_sponsor_queue()
        assert all(r.needs_executive_sponsor for r in queue)

    def test_high_value_deal_in_exec_sponsor_queue(self, intel):
        inp = DealComplexityInput(
            deal_id="high_val", rep_id="r", deal_name="X",
            deal_value_usd=600000.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        intel.assess(inp)
        queue = intel.executive_sponsor_queue()
        assert any(r.deal_id == "high_val" for r in queue)


# ---------------------------------------------------------------------------
# high_complexity_pipeline_usd()
# ---------------------------------------------------------------------------


class TestHighComplexityPipelineUsd:
    def test_zero_when_no_deals(self, intel):
        assert intel.high_complexity_pipeline_usd() == 0.0

    def test_enterprise_deal_included(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        pipeline = intel.high_complexity_pipeline_usd()
        # enterprise composite >= 50, so 750000 should be included
        assert pipeline > 0.0

    def test_simple_deal_excluded(self, intel, simple_input):
        intel.assess(simple_input)
        # composite < 50 for simple deal
        result = intel.get("deal_simple")
        if result and result.complexity_composite < 50:
            assert intel.high_complexity_pipeline_usd() == 0.0

    def test_sums_only_high_complexity_deals(self, intel, enterprise_input, simple_input):
        intel.assess_batch([enterprise_input, simple_input])
        pipeline = intel.high_complexity_pipeline_usd()
        # enterprise is >= 50, simple is < 50
        enterprise_result = intel.get("deal_001")
        simple_result = intel.get("deal_simple")
        expected = 0.0
        if enterprise_result and enterprise_result.complexity_composite >= 50:
            expected += 750000.0
        if simple_result and simple_result.complexity_composite >= 50:
            expected += 10000.0
        assert pipeline == pytest.approx(expected, abs=0.01)

    def test_pipeline_cleared_after_reset(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        intel.reset()
        assert intel.high_complexity_pipeline_usd() == 0.0

    def test_multiple_high_complexity_deals_summed(self, intel):
        for i in range(3):
            inp = DealComplexityInput(
                deal_id=f"hc_{i}", rep_id="r", deal_name="X",
                deal_value_usd=100000.0,
                stakeholder_count=10, department_count=5,
                legal_review_required=1, security_review_required=1,
                procurement_involvement=1, custom_contract_required=1,
                integration_complexity_score=100.0, multi_year_deal=1,
                competitive_deal=1, proof_of_concept_required=1,
                deal_stage=2, industry_regulatory_complexity=100.0,
                geographic_complexity=3, pricing_complexity_score=100.0,
                existing_tech_debt_score=100.0, executive_alignment_required=1,
                partner_involvement_required=1, estimated_implementation_months=12,
            )
            intel.assess(inp)
        pipeline = intel.high_complexity_pipeline_usd()
        assert pipeline == pytest.approx(300000.0, abs=0.01)


# ---------------------------------------------------------------------------
# summary() — exactly 13 keys
# ---------------------------------------------------------------------------


class TestSummary:
    def test_summary_has_13_keys(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert len(s) == 13

    def test_summary_key_total(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "total" in s

    def test_summary_key_tier_counts(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "tier_counts" in s

    def test_summary_key_risk_counts(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "risk_counts" in s

    def test_summary_key_dimension_counts(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "dimension_counts" in s

    def test_summary_key_action_counts(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "action_counts" in s

    def test_summary_key_avg_complexity_composite(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "avg_complexity_composite" in s

    def test_summary_key_deal_desk_required_count(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "deal_desk_required_count" in s

    def test_summary_key_executive_sponsor_needed_count(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "executive_sponsor_needed_count" in s

    def test_summary_key_avg_people_score(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "avg_people_score" in s

    def test_summary_key_avg_process_score(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "avg_process_score" in s

    def test_summary_key_avg_technology_score(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "avg_technology_score" in s

    def test_summary_key_avg_legal_score(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "avg_legal_score" in s

    def test_summary_key_high_complexity_pipeline_usd(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert "high_complexity_pipeline_usd" in s

    def test_summary_exact_keys(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        expected = {
            "total", "tier_counts", "risk_counts", "dimension_counts",
            "action_counts", "avg_complexity_composite", "deal_desk_required_count",
            "executive_sponsor_needed_count", "avg_people_score", "avg_process_score",
            "avg_technology_score", "avg_legal_score", "high_complexity_pipeline_usd",
        }
        assert set(s.keys()) == expected

    def test_summary_total_matches_assessed_count(self, intel, enterprise_input, simple_input):
        intel.assess_batch([enterprise_input, simple_input])
        s = intel.summary()
        assert s["total"] == 2

    def test_summary_total_one_deal(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert s["total"] == 1

    def test_summary_empty_intel(self, intel):
        s = intel.summary()
        assert s["total"] == 0

    def test_summary_avg_composite_matches_single_deal(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        s = intel.summary()
        assert s["avg_complexity_composite"] == pytest.approx(result.complexity_composite, abs=0.1)

    def test_summary_tier_counts_correct(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        tier_counts = s["tier_counts"]
        assert tier_counts.get("enterprise", 0) >= 1

    def test_summary_risk_counts_correct(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        risk_counts = s["risk_counts"]
        assert risk_counts.get("critical", 0) >= 1

    def test_summary_deal_desk_count_correct(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert s["deal_desk_required_count"] >= 1

    def test_summary_exec_sponsor_count_correct(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert s["executive_sponsor_needed_count"] >= 1

    def test_summary_avg_scores_non_negative(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert s["avg_people_score"] >= 0.0
        assert s["avg_process_score"] >= 0.0
        assert s["avg_technology_score"] >= 0.0
        assert s["avg_legal_score"] >= 0.0

    def test_summary_high_complexity_pipeline_positive_for_enterprise(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        s = intel.summary()
        assert s["high_complexity_pipeline_usd"] > 0.0


# ---------------------------------------------------------------------------
# Score clamping [0, 100]
# ---------------------------------------------------------------------------


class TestScoreClamping:
    def _make_maximal(self) -> DealComplexityInput:
        return DealComplexityInput(
            deal_id="max", rep_id="r", deal_name="X",
            deal_value_usd=1000000.0,
            stakeholder_count=100, department_count=100,
            legal_review_required=1, security_review_required=1,
            procurement_involvement=1, custom_contract_required=1,
            integration_complexity_score=1000.0,
            multi_year_deal=1, competitive_deal=1, proof_of_concept_required=1,
            deal_stage=5, industry_regulatory_complexity=1000.0,
            geographic_complexity=10, pricing_complexity_score=1000.0,
            existing_tech_debt_score=1000.0, executive_alignment_required=1,
            partner_involvement_required=1, estimated_implementation_months=100,
        )

    def test_people_score_clamped_at_100(self):
        inp = self._make_maximal()
        assert _people_complexity_score(inp) <= 100.0

    def test_process_score_clamped_at_100(self):
        inp = self._make_maximal()
        assert _process_complexity_score(inp) <= 100.0

    def test_technology_score_clamped_at_100(self):
        inp = self._make_maximal()
        assert _technology_complexity_score(inp) <= 100.0

    def test_legal_score_clamped_at_100(self):
        inp = self._make_maximal()
        assert _legal_complexity_score(inp) <= 100.0

    def test_all_scores_non_negative_for_negative_inputs(self):
        # Pass extreme low values to ensure min(0) clamping
        inp = DealComplexityInput(
            deal_id="neg", rep_id="r", deal_name="X",
            deal_value_usd=0.0,
            stakeholder_count=0, department_count=0,
            legal_review_required=0, security_review_required=0,
            procurement_involvement=0, custom_contract_required=0,
            integration_complexity_score=-100.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=0, industry_regulatory_complexity=-100.0,
            geographic_complexity=0, pricing_complexity_score=-100.0,
            existing_tech_debt_score=-100.0, executive_alignment_required=0,
            partner_involvement_required=0, estimated_implementation_months=0,
        )
        assert _people_complexity_score(inp) >= 0.0
        assert _process_complexity_score(inp) >= 0.0
        assert _technology_complexity_score(inp) >= 0.0
        assert _legal_complexity_score(inp) >= 0.0


# ---------------------------------------------------------------------------
# get() and all_deals()
# ---------------------------------------------------------------------------


class TestGetAndAllDeals:
    def test_get_returns_none_for_unknown_deal(self, intel):
        assert intel.get("unknown") is None

    def test_get_returns_result_after_assess(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        assert intel.get("deal_001") is not None

    def test_all_deals_empty_initially(self, intel):
        assert intel.all_deals() == []

    def test_all_deals_after_assess(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        deals = intel.all_deals()
        assert len(deals) == 1

    def test_all_deals_sorted_by_composite_descending(self, intel, enterprise_input, simple_input):
        intel.assess_batch([simple_input, enterprise_input])
        deals = intel.all_deals()
        composites = [d.complexity_composite for d in deals]
        assert composites == sorted(composites, reverse=True)

    def test_assess_overwrites_existing_deal_id(self, intel, enterprise_input):
        intel.assess(enterprise_input)
        modified = DealComplexityInput(
            deal_id="deal_001", rep_id="rep_002", deal_name="Updated",
            deal_value_usd=100.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        intel.assess(modified)
        result = intel.get("deal_001")
        assert result.rep_id == "rep_002"
        assert len(intel.all_deals()) == 1


# ---------------------------------------------------------------------------
# avg_complexity_composite()
# ---------------------------------------------------------------------------


class TestAvgComplexityComposite:
    def test_returns_zero_when_empty(self, intel):
        assert intel.avg_complexity_composite() == 0.0

    def test_returns_single_deal_composite(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert intel.avg_complexity_composite() == result.complexity_composite

    def test_returns_average_of_two_deals(self, intel, enterprise_input, simple_input):
        r1 = intel.assess(enterprise_input)
        r2 = intel.assess(simple_input)
        expected = round((r1.complexity_composite + r2.complexity_composite) / 2, 1)
        assert intel.avg_complexity_composite() == expected


# ---------------------------------------------------------------------------
# Complexity summary string tests
# ---------------------------------------------------------------------------


class TestComplexitySummary:
    def _make(self, **kwargs) -> DealComplexityInput:
        base = dict(
            deal_id="x", rep_id="y", deal_name="N", deal_value_usd=0.0,
            stakeholder_count=1, department_count=1, legal_review_required=0,
            security_review_required=0, procurement_involvement=0,
            custom_contract_required=0, integration_complexity_score=0.0,
            multi_year_deal=0, competitive_deal=0, proof_of_concept_required=0,
            deal_stage=1, industry_regulatory_complexity=0.0, geographic_complexity=0,
            pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
            executive_alignment_required=0, partner_involvement_required=0,
            estimated_implementation_months=1,
        )
        base.update(kwargs)
        return DealComplexityInput(**base)

    def test_summary_contains_primary_dimension(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        assert result.primary_complexity_dimension.value in result.complexity_summary

    def test_summary_custom_legal_factor(self):
        inp = self._make(legal_review_required=1, custom_contract_required=1)
        people = _people_complexity_score(inp)
        process = _process_complexity_score(inp)
        technology = _technology_complexity_score(inp)
        legal = _legal_complexity_score(inp)
        summary = _complexity_summary(inp, people, process, technology, legal)
        assert "custom legal" in summary

    def test_summary_security_review_factor(self):
        inp = self._make(security_review_required=1)
        people = _people_complexity_score(inp)
        process = _process_complexity_score(inp)
        technology = _technology_complexity_score(inp)
        legal = _legal_complexity_score(inp)
        summary = _complexity_summary(inp, people, process, technology, legal)
        assert "security review" in summary

    def test_summary_poc_factor(self):
        inp = self._make(proof_of_concept_required=1)
        people = _people_complexity_score(inp)
        process = _process_complexity_score(inp)
        technology = _technology_complexity_score(inp)
        legal = _legal_complexity_score(inp)
        summary = _complexity_summary(inp, people, process, technology, legal)
        assert "POC required" in summary

    def test_summary_long_implementation_factor(self):
        inp = self._make(estimated_implementation_months=12)
        people = _people_complexity_score(inp)
        process = _process_complexity_score(inp)
        technology = _technology_complexity_score(inp)
        legal = _legal_complexity_score(inp)
        summary = _complexity_summary(inp, people, process, technology, legal)
        assert "12-month implementation" in summary

    def test_summary_multiregion_factor(self):
        inp = self._make(geographic_complexity=2)
        people = _people_complexity_score(inp)
        process = _process_complexity_score(inp)
        technology = _technology_complexity_score(inp)
        legal = _legal_complexity_score(inp)
        summary = _complexity_summary(inp, people, process, technology, legal)
        assert "multi-region" in summary

    def test_summary_no_factors_fallback(self):
        inp = self._make()
        summary = _complexity_summary(inp, 0.0, 0.0, 0.0, 0.0)
        assert "primary complexity driver" in summary

    def test_summary_implementation_9_months_included(self):
        inp = self._make(estimated_implementation_months=9)
        people = _people_complexity_score(inp)
        process = _process_complexity_score(inp)
        technology = _technology_complexity_score(inp)
        legal = _legal_complexity_score(inp)
        summary = _complexity_summary(inp, people, process, technology, legal)
        assert "9-month implementation" in summary

    def test_summary_implementation_8_months_not_included(self):
        inp = self._make(estimated_implementation_months=8)
        people = _people_complexity_score(inp)
        process = _process_complexity_score(inp)
        technology = _technology_complexity_score(inp)
        legal = _legal_complexity_score(inp)
        summary = _complexity_summary(inp, people, process, technology, legal)
        assert "month implementation" not in summary


# ---------------------------------------------------------------------------
# End-to-end / integration tests
# ---------------------------------------------------------------------------


class TestEndToEnd:
    def test_full_pipeline_enterprise(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        s = intel.summary()
        assert s["total"] == 1
        assert s["deal_desk_required_count"] >= 1
        assert result.requires_deal_desk
        assert result.needs_executive_sponsor
        assert result.complexity_tier == ComplexityTier.ENTERPRISE

    def test_full_pipeline_mixed_batch(self, intel, enterprise_input, simple_input):
        results = intel.assess_batch([enterprise_input, simple_input])
        assert len(results) == 2
        s = intel.summary()
        assert s["total"] == 2

    def test_reset_and_reassess(self, intel, enterprise_input, simple_input):
        intel.assess_batch([enterprise_input, simple_input])
        intel.reset()
        assert intel.summary()["total"] == 0
        intel.assess(enterprise_input)
        assert intel.summary()["total"] == 1

    def test_to_dict_and_back_consistent(self, intel, enterprise_input):
        result = intel.assess(enterprise_input)
        d = result.to_dict()
        assert d["complexity_composite"] == result.complexity_composite
        assert d["requires_deal_desk"] == result.requires_deal_desk
        assert d["needs_executive_sponsor"] == result.needs_executive_sponsor

    def test_multiple_deals_different_tiers(self, intel):
        inputs = [
            # Simple: all zeros
            DealComplexityInput(
                deal_id="t_simple", rep_id="r", deal_name="X",
                deal_value_usd=5000.0, stakeholder_count=1, department_count=1,
                legal_review_required=0, security_review_required=0,
                procurement_involvement=0, custom_contract_required=0,
                integration_complexity_score=0.0, multi_year_deal=0,
                competitive_deal=0, proof_of_concept_required=0, deal_stage=1,
                industry_regulatory_complexity=0.0, geographic_complexity=0,
                pricing_complexity_score=0.0, existing_tech_debt_score=0.0,
                executive_alignment_required=0, partner_involvement_required=0,
                estimated_implementation_months=1,
            ),
            # Enterprise: all high
            DealComplexityInput(
                deal_id="t_enterprise", rep_id="r", deal_name="X",
                deal_value_usd=999999.0, stakeholder_count=10, department_count=5,
                legal_review_required=1, security_review_required=1,
                procurement_involvement=1, custom_contract_required=1,
                integration_complexity_score=100.0, multi_year_deal=1,
                competitive_deal=1, proof_of_concept_required=1, deal_stage=3,
                industry_regulatory_complexity=100.0, geographic_complexity=3,
                pricing_complexity_score=100.0, existing_tech_debt_score=100.0,
                executive_alignment_required=1, partner_involvement_required=1,
                estimated_implementation_months=18,
            ),
        ]
        results = intel.assess_batch(inputs)
        composites = [r.complexity_composite for r in results]
        assert composites[0] >= composites[1]  # sorted descending

    def test_deal_desk_queue_subset_of_all_deals(self, intel, enterprise_input, simple_input):
        intel.assess_batch([enterprise_input, simple_input])
        all_ids = {r.deal_id for r in intel.all_deals()}
        queue_ids = {r.deal_id for r in intel.deal_desk_queue()}
        assert queue_ids.issubset(all_ids)

    def test_exec_sponsor_queue_subset_of_all_deals(self, intel, enterprise_input, simple_input):
        intel.assess_batch([enterprise_input, simple_input])
        all_ids = {r.deal_id for r in intel.all_deals()}
        queue_ids = {r.deal_id for r in intel.executive_sponsor_queue()}
        assert queue_ids.issubset(all_ids)
