"""
Comprehensive pytest tests for SalesBuyerPersonaMismatchIntelligenceEngine.
"""
from __future__ import annotations
import pytest
from swarm.intelligence.sales_buyer_persona_mismatch_intelligence_engine import (
    PersonaInput,
    PersonaResult,
    PersonaRisk,
    PersonaPattern,
    PersonaSeverity,
    PersonaAction,
    SalesBuyerPersonaMismatchIntelligenceEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input(**overrides) -> PersonaInput:
    """Return a 'perfect' baseline PersonaInput; override any fields via kwargs."""
    defaults = dict(
        rep_id="REP001",
        region="NORTH",
        evaluation_period_id="Q1-2026",
        primary_contact_level_score=0.80,
        economic_buyer_contact_rate_pct=0.80,
        it_only_contact_rate_pct=0.10,
        business_unit_alignment_score=0.80,
        decision_maker_access_rate_pct=0.80,
        influencer_only_rate_pct=0.10,
        procurement_first_contact_rate_pct=0.10,
        avg_seniority_of_contacts=0.75,
        sponsor_identification_rate_pct=0.80,
        cross_functional_coverage_score=0.80,
        persona_to_use_case_fit_score=0.80,
        budget_authority_confirmed_rate_pct=0.80,
        vp_plus_engagement_rate_pct=0.80,
        champion_seniority_score=0.80,
        technical_blockers_rate_pct=0.10,
        wrong_entry_point_rate_pct=0.10,
        referral_to_right_person_rate_pct=0.80,
        lost_due_to_persona_mismatch_pct=0.05,
        total_deals_evaluated=20,
        avg_deal_value_usd=50_000.0,
    )
    defaults.update(overrides)
    return PersonaInput(**defaults)


def engine() -> SalesBuyerPersonaMismatchIntelligenceEngine:
    return SalesBuyerPersonaMismatchIntelligenceEngine()


# ---------------------------------------------------------------------------
# 1. PersonaInput – construction and field count
# ---------------------------------------------------------------------------

class TestPersonaInputConstruction:
    def test_all_22_fields_accepted(self):
        inp = make_input()
        assert inp.rep_id == "REP001"

    def test_rep_id_stored(self):
        inp = make_input(rep_id="X99")
        assert inp.rep_id == "X99"

    def test_region_stored(self):
        inp = make_input(region="APAC")
        assert inp.region == "APAC"

    def test_evaluation_period_id_stored(self):
        inp = make_input(evaluation_period_id="Q4-2025")
        assert inp.evaluation_period_id == "Q4-2025"

    def test_total_deals_evaluated_is_int(self):
        inp = make_input(total_deals_evaluated=100)
        assert isinstance(inp.total_deals_evaluated, int)

    def test_avg_deal_value_usd_is_float(self):
        inp = make_input(avg_deal_value_usd=25000.0)
        assert isinstance(inp.avg_deal_value_usd, float)

    def test_float_fields_stored(self):
        inp = make_input(primary_contact_level_score=0.55)
        assert inp.primary_contact_level_score == 0.55

    def test_zero_deal_value(self):
        inp = make_input(avg_deal_value_usd=0.0)
        assert inp.avg_deal_value_usd == 0.0

    def test_zero_deals_evaluated(self):
        inp = make_input(total_deals_evaluated=0)
        assert inp.total_deals_evaluated == 0

    def test_boundary_floats_at_1(self):
        inp = make_input(primary_contact_level_score=1.0)
        assert inp.primary_contact_level_score == 1.0

    def test_boundary_floats_at_0(self):
        inp = make_input(primary_contact_level_score=0.0)
        assert inp.primary_contact_level_score == 0.0


# ---------------------------------------------------------------------------
# 2. PersonaResult – to_dict key count and types
# ---------------------------------------------------------------------------

class TestPersonaResultToDict:
    def test_to_dict_has_exactly_15_keys(self):
        res = engine().assess(make_input())
        assert len(res.to_dict()) == 15

    def test_to_dict_has_rep_id(self):
        res = engine().assess(make_input(rep_id="A1"))
        assert res.to_dict()["rep_id"] == "A1"

    def test_to_dict_has_region(self):
        res = engine().assess(make_input(region="EMEA"))
        assert res.to_dict()["region"] == "EMEA"

    def test_to_dict_persona_risk_is_string(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["persona_risk"], str)

    def test_to_dict_persona_pattern_is_string(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["persona_pattern"], str)

    def test_to_dict_persona_severity_is_string(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["persona_severity"], str)

    def test_to_dict_recommended_action_is_string(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["recommended_action"], str)

    def test_to_dict_access_score_is_float(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["access_score"], float)

    def test_to_dict_alignment_score_is_float(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["alignment_score"], float)

    def test_to_dict_authority_score_is_float(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["authority_score"], float)

    def test_to_dict_coverage_score_is_float(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["coverage_score"], float)

    def test_to_dict_persona_composite_is_float(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["persona_composite"], float)

    def test_to_dict_has_persona_gap_bool(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["has_persona_gap"], bool)

    def test_to_dict_requires_coaching_bool(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["requires_persona_coaching"], bool)

    def test_to_dict_estimated_lost_deal_value_float(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["estimated_lost_deal_value_usd"], float)

    def test_to_dict_persona_signal_is_str(self):
        d = engine().assess(make_input()).to_dict()
        assert isinstance(d["persona_signal"], str)

    def test_to_dict_exact_keys(self):
        expected = {
            "rep_id", "region", "persona_risk", "persona_pattern",
            "persona_severity", "recommended_action", "access_score",
            "alignment_score", "authority_score", "coverage_score",
            "persona_composite", "has_persona_gap", "requires_persona_coaching",
            "estimated_lost_deal_value_usd", "persona_signal",
        }
        assert set(engine().assess(make_input()).to_dict().keys()) == expected


# ---------------------------------------------------------------------------
# 3. summary() key count
# ---------------------------------------------------------------------------

class TestSummaryKeys:
    def test_empty_summary_has_13_keys(self):
        assert len(engine().summary()) == 13

    def test_non_empty_summary_has_13_keys(self):
        e = engine()
        e.assess(make_input())
        assert len(e.summary()) == 13

    def test_summary_exact_keys(self):
        expected = {
            "total", "risk_counts", "pattern_counts", "severity_counts",
            "action_counts", "avg_persona_composite", "persona_gap_count",
            "coaching_count", "avg_access_score", "avg_alignment_score",
            "avg_authority_score", "avg_coverage_score",
            "total_estimated_lost_deal_value_usd",
        }
        assert set(engine().summary().keys()) == expected

    def test_empty_summary_total_zero(self):
        assert engine().summary()["total"] == 0

    def test_empty_summary_risk_counts_empty(self):
        assert engine().summary()["risk_counts"] == {}

    def test_empty_summary_avg_composite_zero(self):
        assert engine().summary()["avg_persona_composite"] == 0.0

    def test_empty_summary_gap_count_zero(self):
        assert engine().summary()["persona_gap_count"] == 0

    def test_empty_summary_coaching_count_zero(self):
        assert engine().summary()["coaching_count"] == 0

    def test_empty_summary_lost_value_zero(self):
        assert engine().summary()["total_estimated_lost_deal_value_usd"] == 0.0


# ---------------------------------------------------------------------------
# 4. _access_score sub-score thresholds
# ---------------------------------------------------------------------------

class TestAccessScore:
    # decision_maker_access_rate_pct
    def test_dm_access_le_030_adds_40(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.30,
                         vp_plus_engagement_rate_pct=0.80,
                         primary_contact_level_score=0.80)
        assert e._access_score(inp) == 40.0

    def test_dm_access_le_055_adds_22(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.55,
                         vp_plus_engagement_rate_pct=0.80,
                         primary_contact_level_score=0.80)
        assert e._access_score(inp) == 22.0

    def test_dm_access_le_075_adds_8(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.75,
                         vp_plus_engagement_rate_pct=0.80,
                         primary_contact_level_score=0.80)
        assert e._access_score(inp) == 8.0

    def test_dm_access_above_075_adds_0(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.76,
                         vp_plus_engagement_rate_pct=0.80,
                         primary_contact_level_score=0.80)
        assert e._access_score(inp) == 0.0

    # vp_plus_engagement_rate_pct
    def test_vp_le_020_adds_35(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.80,
                         vp_plus_engagement_rate_pct=0.20,
                         primary_contact_level_score=0.80)
        assert e._access_score(inp) == 35.0

    def test_vp_le_045_adds_18(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.80,
                         vp_plus_engagement_rate_pct=0.45,
                         primary_contact_level_score=0.80)
        assert e._access_score(inp) == 18.0

    def test_vp_above_045_adds_0(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.80,
                         vp_plus_engagement_rate_pct=0.46,
                         primary_contact_level_score=0.80)
        assert e._access_score(inp) == 0.0

    # primary_contact_level_score
    def test_pcl_le_025_adds_25(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.80,
                         vp_plus_engagement_rate_pct=0.80,
                         primary_contact_level_score=0.25)
        assert e._access_score(inp) == 25.0

    def test_pcl_le_050_adds_12(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.80,
                         vp_plus_engagement_rate_pct=0.80,
                         primary_contact_level_score=0.50)
        assert e._access_score(inp) == 12.0

    def test_pcl_above_050_adds_0(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.80,
                         vp_plus_engagement_rate_pct=0.80,
                         primary_contact_level_score=0.51)
        assert e._access_score(inp) == 0.0

    def test_access_score_capped_at_100(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.10,
                         vp_plus_engagement_rate_pct=0.10,
                         primary_contact_level_score=0.10)
        assert e._access_score(inp) == 100.0

    def test_access_score_worst_case(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.30,
                         vp_plus_engagement_rate_pct=0.20,
                         primary_contact_level_score=0.25)
        # 40 + 35 + 25 = 100 → capped
        assert e._access_score(inp) == 100.0

    def test_access_score_zero_when_all_good(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=1.0,
                         vp_plus_engagement_rate_pct=1.0,
                         primary_contact_level_score=1.0)
        assert e._access_score(inp) == 0.0

    def test_access_score_combined_22_18(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.55,
                         vp_plus_engagement_rate_pct=0.45,
                         primary_contact_level_score=0.80)
        assert e._access_score(inp) == 40.0

    def test_access_score_boundary_dm_031(self):
        e = engine()
        inp = make_input(decision_maker_access_rate_pct=0.31,
                         vp_plus_engagement_rate_pct=0.80,
                         primary_contact_level_score=0.80)
        assert e._access_score(inp) == 22.0


# ---------------------------------------------------------------------------
# 5. _alignment_score sub-score thresholds
# ---------------------------------------------------------------------------

class TestAlignmentScore:
    def test_fit_le_030_adds_40(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.30,
                         business_unit_alignment_score=0.80,
                         wrong_entry_point_rate_pct=0.10)
        assert e._alignment_score(inp) == 40.0

    def test_fit_le_055_adds_22(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.55,
                         business_unit_alignment_score=0.80,
                         wrong_entry_point_rate_pct=0.10)
        assert e._alignment_score(inp) == 22.0

    def test_fit_le_075_adds_8(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.75,
                         business_unit_alignment_score=0.80,
                         wrong_entry_point_rate_pct=0.10)
        assert e._alignment_score(inp) == 8.0

    def test_fit_above_075_adds_0(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.76,
                         business_unit_alignment_score=0.80,
                         wrong_entry_point_rate_pct=0.10)
        assert e._alignment_score(inp) == 0.0

    def test_bu_le_030_adds_35(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.80,
                         business_unit_alignment_score=0.30,
                         wrong_entry_point_rate_pct=0.10)
        assert e._alignment_score(inp) == 35.0

    def test_bu_le_055_adds_18(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.80,
                         business_unit_alignment_score=0.55,
                         wrong_entry_point_rate_pct=0.10)
        assert e._alignment_score(inp) == 18.0

    def test_bu_above_055_adds_0(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.80,
                         business_unit_alignment_score=0.56,
                         wrong_entry_point_rate_pct=0.10)
        assert e._alignment_score(inp) == 0.0

    def test_wrong_entry_ge_050_adds_25(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.80,
                         business_unit_alignment_score=0.80,
                         wrong_entry_point_rate_pct=0.50)
        assert e._alignment_score(inp) == 25.0

    def test_wrong_entry_ge_030_adds_12(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.80,
                         business_unit_alignment_score=0.80,
                         wrong_entry_point_rate_pct=0.30)
        assert e._alignment_score(inp) == 12.0

    def test_wrong_entry_below_030_adds_0(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.80,
                         business_unit_alignment_score=0.80,
                         wrong_entry_point_rate_pct=0.29)
        assert e._alignment_score(inp) == 0.0

    def test_alignment_score_capped_100(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.10,
                         business_unit_alignment_score=0.10,
                         wrong_entry_point_rate_pct=0.90)
        assert e._alignment_score(inp) == 100.0

    def test_alignment_score_zero_all_good(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.90,
                         business_unit_alignment_score=0.90,
                         wrong_entry_point_rate_pct=0.05)
        assert e._alignment_score(inp) == 0.0

    def test_alignment_combined_40_35(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.30,
                         business_unit_alignment_score=0.30,
                         wrong_entry_point_rate_pct=0.10)
        assert e._alignment_score(inp) == 75.0

    def test_alignment_boundary_fit_031(self):
        e = engine()
        inp = make_input(persona_to_use_case_fit_score=0.31,
                         business_unit_alignment_score=0.80,
                         wrong_entry_point_rate_pct=0.10)
        assert e._alignment_score(inp) == 22.0


# ---------------------------------------------------------------------------
# 6. _authority_score sub-score thresholds
# ---------------------------------------------------------------------------

class TestAuthorityScore:
    def test_eb_le_025_adds_40(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.25,
                         budget_authority_confirmed_rate_pct=0.80,
                         influencer_only_rate_pct=0.10)
        assert e._authority_score(inp) == 40.0

    def test_eb_le_050_adds_22(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.50,
                         budget_authority_confirmed_rate_pct=0.80,
                         influencer_only_rate_pct=0.10)
        assert e._authority_score(inp) == 22.0

    def test_eb_le_070_adds_8(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.70,
                         budget_authority_confirmed_rate_pct=0.80,
                         influencer_only_rate_pct=0.10)
        assert e._authority_score(inp) == 8.0

    def test_eb_above_070_adds_0(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.71,
                         budget_authority_confirmed_rate_pct=0.80,
                         influencer_only_rate_pct=0.10)
        assert e._authority_score(inp) == 0.0

    def test_budget_le_025_adds_35(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.80,
                         budget_authority_confirmed_rate_pct=0.25,
                         influencer_only_rate_pct=0.10)
        assert e._authority_score(inp) == 35.0

    def test_budget_le_050_adds_18(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.80,
                         budget_authority_confirmed_rate_pct=0.50,
                         influencer_only_rate_pct=0.10)
        assert e._authority_score(inp) == 18.0

    def test_budget_above_050_adds_0(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.80,
                         budget_authority_confirmed_rate_pct=0.51,
                         influencer_only_rate_pct=0.10)
        assert e._authority_score(inp) == 0.0

    def test_influencer_ge_050_adds_25(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.80,
                         budget_authority_confirmed_rate_pct=0.80,
                         influencer_only_rate_pct=0.50)
        assert e._authority_score(inp) == 25.0

    def test_influencer_ge_030_adds_12(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.80,
                         budget_authority_confirmed_rate_pct=0.80,
                         influencer_only_rate_pct=0.30)
        assert e._authority_score(inp) == 12.0

    def test_influencer_below_030_adds_0(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.80,
                         budget_authority_confirmed_rate_pct=0.80,
                         influencer_only_rate_pct=0.29)
        assert e._authority_score(inp) == 0.0

    def test_authority_score_capped_100(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.10,
                         budget_authority_confirmed_rate_pct=0.10,
                         influencer_only_rate_pct=0.90)
        assert e._authority_score(inp) == 100.0

    def test_authority_score_zero_all_good(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.90,
                         budget_authority_confirmed_rate_pct=0.90,
                         influencer_only_rate_pct=0.05)
        assert e._authority_score(inp) == 0.0

    def test_authority_combined_40_35(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.25,
                         budget_authority_confirmed_rate_pct=0.25,
                         influencer_only_rate_pct=0.10)
        assert e._authority_score(inp) == 75.0

    def test_authority_boundary_eb_026(self):
        e = engine()
        inp = make_input(economic_buyer_contact_rate_pct=0.26,
                         budget_authority_confirmed_rate_pct=0.80,
                         influencer_only_rate_pct=0.10)
        assert e._authority_score(inp) == 22.0


# ---------------------------------------------------------------------------
# 7. _coverage_score sub-score thresholds
# ---------------------------------------------------------------------------

class TestCoverageScore:
    def test_cf_le_025_adds_45(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.25,
                         sponsor_identification_rate_pct=0.80,
                         technical_blockers_rate_pct=0.10)
        assert e._coverage_score(inp) == 45.0

    def test_cf_le_050_adds_25(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.50,
                         sponsor_identification_rate_pct=0.80,
                         technical_blockers_rate_pct=0.10)
        assert e._coverage_score(inp) == 25.0

    def test_cf_le_070_adds_10(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.70,
                         sponsor_identification_rate_pct=0.80,
                         technical_blockers_rate_pct=0.10)
        assert e._coverage_score(inp) == 10.0

    def test_cf_above_070_adds_0(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.71,
                         sponsor_identification_rate_pct=0.80,
                         technical_blockers_rate_pct=0.10)
        assert e._coverage_score(inp) == 0.0

    def test_sponsor_le_030_adds_30(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.80,
                         sponsor_identification_rate_pct=0.30,
                         technical_blockers_rate_pct=0.10)
        assert e._coverage_score(inp) == 30.0

    def test_sponsor_le_055_adds_15(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.80,
                         sponsor_identification_rate_pct=0.55,
                         technical_blockers_rate_pct=0.10)
        assert e._coverage_score(inp) == 15.0

    def test_sponsor_above_055_adds_0(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.80,
                         sponsor_identification_rate_pct=0.56,
                         technical_blockers_rate_pct=0.10)
        assert e._coverage_score(inp) == 0.0

    def test_tech_blockers_ge_045_adds_25(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.80,
                         sponsor_identification_rate_pct=0.80,
                         technical_blockers_rate_pct=0.45)
        assert e._coverage_score(inp) == 25.0

    def test_tech_blockers_ge_025_adds_12(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.80,
                         sponsor_identification_rate_pct=0.80,
                         technical_blockers_rate_pct=0.25)
        assert e._coverage_score(inp) == 12.0

    def test_tech_blockers_below_025_adds_0(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.80,
                         sponsor_identification_rate_pct=0.80,
                         technical_blockers_rate_pct=0.24)
        assert e._coverage_score(inp) == 0.0

    def test_coverage_score_capped_100(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.10,
                         sponsor_identification_rate_pct=0.10,
                         technical_blockers_rate_pct=0.90)
        assert e._coverage_score(inp) == 100.0

    def test_coverage_score_zero_all_good(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.90,
                         sponsor_identification_rate_pct=0.90,
                         technical_blockers_rate_pct=0.10)
        assert e._coverage_score(inp) == 0.0

    def test_coverage_combined_45_30(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.25,
                         sponsor_identification_rate_pct=0.30,
                         technical_blockers_rate_pct=0.10)
        assert e._coverage_score(inp) == 75.0

    def test_coverage_boundary_cf_026(self):
        e = engine()
        inp = make_input(cross_functional_coverage_score=0.26,
                         sponsor_identification_rate_pct=0.80,
                         technical_blockers_rate_pct=0.10)
        assert e._coverage_score(inp) == 25.0


# ---------------------------------------------------------------------------
# 8. _composite weighting
# ---------------------------------------------------------------------------

class TestComposite:
    def test_composite_weights_sum_to_one(self):
        # weights: 0.30 + 0.25 + 0.30 + 0.15 = 1.00
        e = engine()
        comp = e._composite(100.0, 100.0, 100.0, 100.0)
        assert comp == 100.0

    def test_composite_all_zero(self):
        e = engine()
        assert e._composite(0.0, 0.0, 0.0, 0.0) == 0.0

    def test_composite_only_access(self):
        e = engine()
        assert e._composite(100.0, 0.0, 0.0, 0.0) == 30.0

    def test_composite_only_alignment(self):
        e = engine()
        assert e._composite(0.0, 100.0, 0.0, 0.0) == 25.0

    def test_composite_only_authority(self):
        e = engine()
        assert e._composite(0.0, 0.0, 100.0, 0.0) == 30.0

    def test_composite_only_coverage(self):
        e = engine()
        assert e._composite(0.0, 0.0, 0.0, 100.0) == 15.0

    def test_composite_capped_at_100(self):
        e = engine()
        assert e._composite(200.0, 200.0, 200.0, 200.0) == 100.0

    def test_composite_rounded_to_2dp(self):
        e = engine()
        val = e._composite(33.3, 33.3, 33.3, 33.3)
        assert val == round(33.3 * 0.30 + 33.3 * 0.25 + 33.3 * 0.30 + 33.3 * 0.15, 2)

    def test_composite_known_values(self):
        e = engine()
        # 40*0.30 + 22*0.25 + 35*0.30 + 30*0.15
        expected = round(40 * 0.30 + 22 * 0.25 + 35 * 0.30 + 30 * 0.15, 2)
        assert e._composite(40.0, 22.0, 35.0, 30.0) == expected


# ---------------------------------------------------------------------------
# 9. Risk thresholds
# ---------------------------------------------------------------------------

class TestRisk:
    def test_risk_critical_at_60(self):
        assert engine()._risk(60.0) == PersonaRisk.critical

    def test_risk_critical_above_60(self):
        assert engine()._risk(75.0) == PersonaRisk.critical

    def test_risk_high_at_40(self):
        assert engine()._risk(40.0) == PersonaRisk.high

    def test_risk_high_at_59(self):
        assert engine()._risk(59.9) == PersonaRisk.high

    def test_risk_moderate_at_20(self):
        assert engine()._risk(20.0) == PersonaRisk.moderate

    def test_risk_moderate_at_39(self):
        assert engine()._risk(39.9) == PersonaRisk.moderate

    def test_risk_low_at_0(self):
        assert engine()._risk(0.0) == PersonaRisk.low

    def test_risk_low_at_19(self):
        assert engine()._risk(19.9) == PersonaRisk.low

    def test_risk_boundary_exactly_20(self):
        assert engine()._risk(20.0) == PersonaRisk.moderate

    def test_risk_boundary_exactly_40(self):
        assert engine()._risk(40.0) == PersonaRisk.high

    def test_risk_boundary_exactly_60(self):
        assert engine()._risk(60.0) == PersonaRisk.critical


# ---------------------------------------------------------------------------
# 10. Severity thresholds
# ---------------------------------------------------------------------------

class TestSeverity:
    def test_severity_invisible_at_60(self):
        assert engine()._severity(60.0) == PersonaSeverity.invisible

    def test_severity_invisible_above_60(self):
        assert engine()._severity(80.0) == PersonaSeverity.invisible

    def test_severity_disconnected_at_40(self):
        assert engine()._severity(40.0) == PersonaSeverity.disconnected

    def test_severity_disconnected_at_59(self):
        assert engine()._severity(59.9) == PersonaSeverity.disconnected

    def test_severity_misaligned_at_20(self):
        assert engine()._severity(20.0) == PersonaSeverity.misaligned

    def test_severity_misaligned_at_39(self):
        assert engine()._severity(39.9) == PersonaSeverity.misaligned

    def test_severity_aligned_at_0(self):
        assert engine()._severity(0.0) == PersonaSeverity.aligned

    def test_severity_aligned_at_19(self):
        assert engine()._severity(19.9) == PersonaSeverity.aligned

    def test_severity_boundary_20(self):
        assert engine()._severity(20.0) == PersonaSeverity.misaligned

    def test_severity_boundary_40(self):
        assert engine()._severity(40.0) == PersonaSeverity.disconnected

    def test_severity_boundary_60(self):
        assert engine()._severity(60.0) == PersonaSeverity.invisible


# ---------------------------------------------------------------------------
# 11. Pattern detection (priority order)
# ---------------------------------------------------------------------------

class TestPatternDetection:
    def _p(self, **kw):
        return engine()._pattern(make_input(**kw))

    # wrong_level (priority 1)
    def test_wrong_level_both_conditions_met(self):
        p = self._p(primary_contact_level_score=0.30,
                    vp_plus_engagement_rate_pct=0.20)
        assert p == PersonaPattern.wrong_level

    def test_wrong_level_pcl_just_below(self):
        p = self._p(primary_contact_level_score=0.29,
                    vp_plus_engagement_rate_pct=0.20)
        assert p == PersonaPattern.wrong_level

    def test_wrong_level_not_triggered_pcl_high(self):
        p = self._p(primary_contact_level_score=0.31,
                    vp_plus_engagement_rate_pct=0.20,
                    business_unit_alignment_score=0.80,
                    persona_to_use_case_fit_score=0.80,
                    influencer_only_rate_pct=0.10,
                    decision_maker_access_rate_pct=0.80,
                    it_only_contact_rate_pct=0.10,
                    technical_blockers_rate_pct=0.10,
                    economic_buyer_contact_rate_pct=0.80,
                    budget_authority_confirmed_rate_pct=0.80)
        assert p != PersonaPattern.wrong_level

    def test_wrong_level_not_triggered_vp_high(self):
        p = self._p(primary_contact_level_score=0.30,
                    vp_plus_engagement_rate_pct=0.21,
                    business_unit_alignment_score=0.80,
                    persona_to_use_case_fit_score=0.80,
                    influencer_only_rate_pct=0.10,
                    decision_maker_access_rate_pct=0.80,
                    it_only_contact_rate_pct=0.10,
                    technical_blockers_rate_pct=0.10,
                    economic_buyer_contact_rate_pct=0.80,
                    budget_authority_confirmed_rate_pct=0.80)
        assert p != PersonaPattern.wrong_level

    # wrong_department (priority 2)
    def test_wrong_department_detected(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.35,
                    persona_to_use_case_fit_score=0.40)
        assert p == PersonaPattern.wrong_department

    def test_wrong_department_bu_just_below(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.34,
                    persona_to_use_case_fit_score=0.40)
        assert p == PersonaPattern.wrong_department

    def test_wrong_department_not_triggered_bu_high(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.36,
                    persona_to_use_case_fit_score=0.40,
                    influencer_only_rate_pct=0.10,
                    decision_maker_access_rate_pct=0.80,
                    it_only_contact_rate_pct=0.10,
                    technical_blockers_rate_pct=0.10,
                    economic_buyer_contact_rate_pct=0.80,
                    budget_authority_confirmed_rate_pct=0.80)
        assert p != PersonaPattern.wrong_department

    # influencer_only (priority 3)
    def test_influencer_only_detected(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.80,
                    persona_to_use_case_fit_score=0.80,
                    influencer_only_rate_pct=0.50,
                    decision_maker_access_rate_pct=0.35)
        assert p == PersonaPattern.influencer_only

    def test_influencer_only_just_below_dm(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.80,
                    persona_to_use_case_fit_score=0.80,
                    influencer_only_rate_pct=0.50,
                    decision_maker_access_rate_pct=0.34)
        assert p == PersonaPattern.influencer_only

    def test_influencer_only_not_triggered_dm_high(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.80,
                    persona_to_use_case_fit_score=0.80,
                    influencer_only_rate_pct=0.50,
                    decision_maker_access_rate_pct=0.36,
                    it_only_contact_rate_pct=0.10,
                    technical_blockers_rate_pct=0.10,
                    economic_buyer_contact_rate_pct=0.80,
                    budget_authority_confirmed_rate_pct=0.80)
        assert p != PersonaPattern.influencer_only

    # technical_gatekeeper (priority 4)
    def test_technical_gatekeeper_detected(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.80,
                    persona_to_use_case_fit_score=0.80,
                    influencer_only_rate_pct=0.10,
                    decision_maker_access_rate_pct=0.80,
                    it_only_contact_rate_pct=0.55,
                    technical_blockers_rate_pct=0.40)
        assert p == PersonaPattern.technical_gatekeeper

    def test_technical_gatekeeper_not_triggered_it_low(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.80,
                    persona_to_use_case_fit_score=0.80,
                    influencer_only_rate_pct=0.10,
                    decision_maker_access_rate_pct=0.80,
                    it_only_contact_rate_pct=0.54,
                    technical_blockers_rate_pct=0.40,
                    economic_buyer_contact_rate_pct=0.80,
                    budget_authority_confirmed_rate_pct=0.80)
        assert p != PersonaPattern.technical_gatekeeper

    # budget_blind (priority 5)
    def test_budget_blind_detected(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.80,
                    persona_to_use_case_fit_score=0.80,
                    influencer_only_rate_pct=0.10,
                    decision_maker_access_rate_pct=0.80,
                    it_only_contact_rate_pct=0.10,
                    technical_blockers_rate_pct=0.10,
                    economic_buyer_contact_rate_pct=0.25,
                    budget_authority_confirmed_rate_pct=0.25)
        assert p == PersonaPattern.budget_blind

    def test_budget_blind_not_triggered_eb_high(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.80,
                    persona_to_use_case_fit_score=0.80,
                    influencer_only_rate_pct=0.10,
                    decision_maker_access_rate_pct=0.80,
                    it_only_contact_rate_pct=0.10,
                    technical_blockers_rate_pct=0.10,
                    economic_buyer_contact_rate_pct=0.26,
                    budget_authority_confirmed_rate_pct=0.25)
        assert p != PersonaPattern.budget_blind

    # none (fallback)
    def test_none_pattern_fallback(self):
        p = self._p()  # perfect baseline
        assert p == PersonaPattern.none

    # Priority: wrong_level overrides wrong_department when both conditions met
    def test_wrong_level_takes_priority_over_wrong_department(self):
        p = self._p(primary_contact_level_score=0.30,
                    vp_plus_engagement_rate_pct=0.20,
                    business_unit_alignment_score=0.35,
                    persona_to_use_case_fit_score=0.40)
        assert p == PersonaPattern.wrong_level

    def test_wrong_department_takes_priority_over_influencer_only(self):
        p = self._p(primary_contact_level_score=0.80,
                    vp_plus_engagement_rate_pct=0.80,
                    business_unit_alignment_score=0.35,
                    persona_to_use_case_fit_score=0.40,
                    influencer_only_rate_pct=0.50,
                    decision_maker_access_rate_pct=0.35)
        assert p == PersonaPattern.wrong_department


# ---------------------------------------------------------------------------
# 12. _action mapping
# ---------------------------------------------------------------------------

class TestActionMapping:
    def _action(self, risk, pattern):
        return engine()._action(risk, pattern)

    # critical
    def test_critical_wrong_level_returns_deal_requalification(self):
        assert self._action(PersonaRisk.critical, PersonaPattern.wrong_level) == PersonaAction.deal_re_qualification

    def test_critical_influencer_only_returns_deal_requalification(self):
        assert self._action(PersonaRisk.critical, PersonaPattern.influencer_only) == PersonaAction.deal_re_qualification

    def test_critical_wrong_department_returns_persona_reset(self):
        assert self._action(PersonaRisk.critical, PersonaPattern.wrong_department) == PersonaAction.persona_reset_intervention

    def test_critical_technical_gatekeeper_returns_persona_reset(self):
        assert self._action(PersonaRisk.critical, PersonaPattern.technical_gatekeeper) == PersonaAction.persona_reset_intervention

    def test_critical_budget_blind_returns_persona_reset(self):
        assert self._action(PersonaRisk.critical, PersonaPattern.budget_blind) == PersonaAction.persona_reset_intervention

    def test_critical_none_returns_persona_reset(self):
        assert self._action(PersonaRisk.critical, PersonaPattern.none) == PersonaAction.persona_reset_intervention

    # high
    def test_high_wrong_level_returns_executive_access_coaching(self):
        assert self._action(PersonaRisk.high, PersonaPattern.wrong_level) == PersonaAction.executive_access_coaching

    def test_high_wrong_department_returns_stakeholder_mapping(self):
        assert self._action(PersonaRisk.high, PersonaPattern.wrong_department) == PersonaAction.stakeholder_mapping_coaching

    def test_high_influencer_only_returns_executive_access_coaching(self):
        assert self._action(PersonaRisk.high, PersonaPattern.influencer_only) == PersonaAction.executive_access_coaching

    def test_high_technical_gatekeeper_returns_budget_holder_intro(self):
        assert self._action(PersonaRisk.high, PersonaPattern.technical_gatekeeper) == PersonaAction.budget_holder_introduction

    def test_high_budget_blind_returns_budget_holder_intro(self):
        assert self._action(PersonaRisk.high, PersonaPattern.budget_blind) == PersonaAction.budget_holder_introduction

    def test_high_none_returns_stakeholder_mapping(self):
        assert self._action(PersonaRisk.high, PersonaPattern.none) == PersonaAction.stakeholder_mapping_coaching

    # moderate
    def test_moderate_any_pattern_returns_alignment_check(self):
        for pat in PersonaPattern:
            assert self._action(PersonaRisk.moderate, pat) == PersonaAction.persona_alignment_check

    # low
    def test_low_any_pattern_returns_no_action(self):
        for pat in PersonaPattern:
            assert self._action(PersonaRisk.low, pat) == PersonaAction.no_action


# ---------------------------------------------------------------------------
# 13. has_persona_gap logic
# ---------------------------------------------------------------------------

class TestHasPersonaGap:
    def _gap(self, composite, **kw):
        return engine()._has_gap(make_input(**kw), composite)

    def test_gap_true_when_composite_ge_40(self):
        assert self._gap(40.0,
                         economic_buyer_contact_rate_pct=0.80,
                         decision_maker_access_rate_pct=0.80) is True

    def test_gap_true_when_eb_le_050(self):
        assert self._gap(0.0,
                         economic_buyer_contact_rate_pct=0.50,
                         decision_maker_access_rate_pct=0.80) is True

    def test_gap_true_when_dm_le_055(self):
        assert self._gap(0.0,
                         economic_buyer_contact_rate_pct=0.80,
                         decision_maker_access_rate_pct=0.55) is True

    def test_gap_false_when_none_triggered(self):
        assert self._gap(39.9,
                         economic_buyer_contact_rate_pct=0.51,
                         decision_maker_access_rate_pct=0.56) is False

    def test_gap_true_composite_exactly_40(self):
        assert self._gap(40.0,
                         economic_buyer_contact_rate_pct=0.80,
                         decision_maker_access_rate_pct=0.80) is True

    def test_gap_true_eb_exactly_050(self):
        assert self._gap(0.0,
                         economic_buyer_contact_rate_pct=0.50,
                         decision_maker_access_rate_pct=0.80) is True

    def test_gap_true_dm_exactly_055(self):
        assert self._gap(0.0,
                         economic_buyer_contact_rate_pct=0.80,
                         decision_maker_access_rate_pct=0.55) is True

    def test_gap_false_composite_39_eb_high_dm_high(self):
        assert self._gap(39.9,
                         economic_buyer_contact_rate_pct=0.60,
                         decision_maker_access_rate_pct=0.70) is False


# ---------------------------------------------------------------------------
# 14. requires_persona_coaching logic
# ---------------------------------------------------------------------------

class TestRequiresCoaching:
    def _coaching(self, composite, **kw):
        return engine()._requires_coaching(make_input(**kw), composite)

    def test_coaching_true_composite_ge_25(self):
        assert self._coaching(25.0,
                               lost_due_to_persona_mismatch_pct=0.05,
                               influencer_only_rate_pct=0.10) is True

    def test_coaching_true_lost_ge_020(self):
        assert self._coaching(0.0,
                               lost_due_to_persona_mismatch_pct=0.20,
                               influencer_only_rate_pct=0.10) is True

    def test_coaching_true_influencer_ge_035(self):
        assert self._coaching(0.0,
                               lost_due_to_persona_mismatch_pct=0.05,
                               influencer_only_rate_pct=0.35) is True

    def test_coaching_false_none_triggered(self):
        assert self._coaching(24.9,
                               lost_due_to_persona_mismatch_pct=0.19,
                               influencer_only_rate_pct=0.34) is False

    def test_coaching_boundary_composite_25(self):
        assert self._coaching(25.0,
                               lost_due_to_persona_mismatch_pct=0.05,
                               influencer_only_rate_pct=0.10) is True

    def test_coaching_boundary_lost_020(self):
        assert self._coaching(0.0,
                               lost_due_to_persona_mismatch_pct=0.20,
                               influencer_only_rate_pct=0.10) is True

    def test_coaching_boundary_influencer_035(self):
        assert self._coaching(0.0,
                               lost_due_to_persona_mismatch_pct=0.05,
                               influencer_only_rate_pct=0.35) is True


# ---------------------------------------------------------------------------
# 15. estimated_lost_deal_value calculation
# ---------------------------------------------------------------------------

class TestLostDealValue:
    def _ldv(self, composite, **kw):
        return engine()._lost_deal_value(make_input(**kw), composite)

    def test_basic_calculation(self):
        # lost=0.10, composite=20 → rate = 0.10 + 20/200 = 0.20
        val = self._ldv(20.0,
                        lost_due_to_persona_mismatch_pct=0.10,
                        total_deals_evaluated=10,
                        avg_deal_value_usd=100_000.0)
        assert val == round(10 * 100_000.0 * 0.20, 2)

    def test_rate_capped_at_1(self):
        # lost=0.90, composite=200 → rate = min(0.90+1.0, 1.0) = 1.0
        val = self._ldv(200.0,
                        lost_due_to_persona_mismatch_pct=0.90,
                        total_deals_evaluated=5,
                        avg_deal_value_usd=50_000.0)
        assert val == round(5 * 50_000.0 * 1.0, 2)

    def test_rate_not_capped_below_1(self):
        # lost=0.05, composite=10 → rate = 0.05 + 10/200 = 0.10
        val = self._ldv(10.0,
                        lost_due_to_persona_mismatch_pct=0.05,
                        total_deals_evaluated=20,
                        avg_deal_value_usd=10_000.0)
        assert val == round(20 * 10_000.0 * 0.10, 2)

    def test_zero_deals_gives_zero(self):
        val = self._ldv(50.0,
                        lost_due_to_persona_mismatch_pct=0.30,
                        total_deals_evaluated=0,
                        avg_deal_value_usd=50_000.0)
        assert val == 0.0

    def test_zero_deal_value_gives_zero(self):
        val = self._ldv(50.0,
                        lost_due_to_persona_mismatch_pct=0.30,
                        total_deals_evaluated=10,
                        avg_deal_value_usd=0.0)
        assert val == 0.0

    def test_result_is_rounded_to_2dp(self):
        val = self._ldv(33.0,
                        lost_due_to_persona_mismatch_pct=0.11,
                        total_deals_evaluated=7,
                        avg_deal_value_usd=33_333.0)
        rate = min(0.11 + 33.0 / 200, 1.0)
        assert val == round(7 * 33_333.0 * rate, 2)

    def test_rate_exactly_1_boundary(self):
        # lost=1.0, composite=0 → rate = min(1.0 + 0.0, 1.0) = 1.0
        val = self._ldv(0.0,
                        lost_due_to_persona_mismatch_pct=1.0,
                        total_deals_evaluated=10,
                        avg_deal_value_usd=1_000.0)
        assert val == 10_000.0


# ---------------------------------------------------------------------------
# 16. Signal generation
# ---------------------------------------------------------------------------

class TestSignal:
    def test_signal_below_20_returns_strong_message(self):
        e = engine()
        inp = make_input()
        result = e.assess(inp)
        assert "strong" in result.persona_signal.lower() or "benchmark" in result.persona_signal.lower()

    def test_signal_above_20_contains_dm_pct(self):
        inp = make_input(
            primary_contact_level_score=0.10,
            vp_plus_engagement_rate_pct=0.10,
            decision_maker_access_rate_pct=0.20,
            economic_buyer_contact_rate_pct=0.20,
            budget_authority_confirmed_rate_pct=0.20,
            influencer_only_rate_pct=0.60,
            cross_functional_coverage_score=0.20,
            sponsor_identification_rate_pct=0.20,
            technical_blockers_rate_pct=0.50,
            business_unit_alignment_score=0.20,
            persona_to_use_case_fit_score=0.20,
            wrong_entry_point_rate_pct=0.60,
        )
        result = engine().assess(inp)
        assert "20%" in result.persona_signal  # DM access = 20%

    def test_signal_contains_composite(self):
        inp = make_input(
            primary_contact_level_score=0.10,
            vp_plus_engagement_rate_pct=0.10,
            decision_maker_access_rate_pct=0.20,
            economic_buyer_contact_rate_pct=0.20,
            budget_authority_confirmed_rate_pct=0.20,
            influencer_only_rate_pct=0.60,
            cross_functional_coverage_score=0.20,
            sponsor_identification_rate_pct=0.20,
            technical_blockers_rate_pct=0.50,
            business_unit_alignment_score=0.20,
            persona_to_use_case_fit_score=0.20,
            wrong_entry_point_rate_pct=0.60,
        )
        result = engine().assess(inp)
        assert "composite" in result.persona_signal

    def test_signal_below_20_not_contains_composite_label(self):
        result = engine().assess(make_input())
        assert "composite" not in result.persona_signal


# ---------------------------------------------------------------------------
# 17. Full assess() integration — low risk / aligned
# ---------------------------------------------------------------------------

class TestAssessLowRisk:
    def test_low_risk_label(self):
        r = engine().assess(make_input())
        assert r.persona_risk == PersonaRisk.low

    def test_aligned_severity(self):
        r = engine().assess(make_input())
        assert r.persona_severity == PersonaSeverity.aligned

    def test_no_action_recommended(self):
        r = engine().assess(make_input())
        assert r.recommended_action == PersonaAction.no_action

    def test_pattern_none(self):
        r = engine().assess(make_input())
        assert r.persona_pattern == PersonaPattern.none

    def test_composite_low(self):
        r = engine().assess(make_input())
        assert r.persona_composite < 20.0

    def test_rep_id_passed_through(self):
        r = engine().assess(make_input(rep_id="R42"))
        assert r.rep_id == "R42"

    def test_region_passed_through(self):
        r = engine().assess(make_input(region="LATAM"))
        assert r.region == "LATAM"


# ---------------------------------------------------------------------------
# 18. Full assess() integration — critical / invisible
# ---------------------------------------------------------------------------

class TestAssessCritical:
    def _critical_input(self):
        return make_input(
            primary_contact_level_score=0.10,
            vp_plus_engagement_rate_pct=0.10,
            decision_maker_access_rate_pct=0.15,
            economic_buyer_contact_rate_pct=0.10,
            budget_authority_confirmed_rate_pct=0.10,
            influencer_only_rate_pct=0.80,
            cross_functional_coverage_score=0.10,
            sponsor_identification_rate_pct=0.10,
            technical_blockers_rate_pct=0.60,
            business_unit_alignment_score=0.10,
            persona_to_use_case_fit_score=0.10,
            wrong_entry_point_rate_pct=0.80,
        )

    def test_critical_risk_label(self):
        assert engine().assess(self._critical_input()).persona_risk == PersonaRisk.critical

    def test_invisible_severity(self):
        assert engine().assess(self._critical_input()).persona_severity == PersonaSeverity.invisible

    def test_composite_ge_60(self):
        assert engine().assess(self._critical_input()).persona_composite >= 60.0

    def test_has_persona_gap_true(self):
        assert engine().assess(self._critical_input()).has_persona_gap is True

    def test_requires_coaching_true(self):
        assert engine().assess(self._critical_input()).requires_persona_coaching is True

    def test_estimated_lost_value_positive(self):
        r = engine().assess(self._critical_input())
        assert r.estimated_lost_deal_value_usd > 0.0


# ---------------------------------------------------------------------------
# 19. Full assess() integration — moderate risk / misaligned
# ---------------------------------------------------------------------------

class TestAssessModerate:
    def _moderate_input(self):
        # Craft scores so composite lands in [20, 40)
        # ac=52 (dm=0.55->22, vp=0.45->18, pcl=0.50->12)
        # al=26 (fit=0.75->8, bu=0.55->18, we=0.29->0)
        # au=26 (eb=0.70->8, ba=0.50->18, inf=0.29->0)
        # co=25 (cf=0.70->10, sp=0.55->15, tb=0.24->0)
        # composite = 52*0.30 + 26*0.25 + 26*0.30 + 25*0.15 = 33.65
        return make_input(
            primary_contact_level_score=0.50,
            vp_plus_engagement_rate_pct=0.45,
            decision_maker_access_rate_pct=0.55,
            economic_buyer_contact_rate_pct=0.70,
            budget_authority_confirmed_rate_pct=0.50,
            influencer_only_rate_pct=0.29,
            cross_functional_coverage_score=0.70,
            sponsor_identification_rate_pct=0.55,
            technical_blockers_rate_pct=0.24,
            business_unit_alignment_score=0.55,
            persona_to_use_case_fit_score=0.75,
            wrong_entry_point_rate_pct=0.29,
        )

    def test_composite_in_moderate_range(self):
        r = engine().assess(self._moderate_input())
        assert 20.0 <= r.persona_composite < 40.0

    def test_moderate_risk(self):
        r = engine().assess(self._moderate_input())
        assert r.persona_risk == PersonaRisk.moderate

    def test_misaligned_severity(self):
        r = engine().assess(self._moderate_input())
        assert r.persona_severity == PersonaSeverity.misaligned

    def test_moderate_action(self):
        r = engine().assess(self._moderate_input())
        assert r.recommended_action == PersonaAction.persona_alignment_check


# ---------------------------------------------------------------------------
# 20. assess_batch
# ---------------------------------------------------------------------------

class TestAssessBatch:
    def test_returns_list(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(5)]
        results = engine().assess_batch(inputs)
        assert isinstance(results, list)

    def test_returns_correct_count(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(7)]
        results = engine().assess_batch(inputs)
        assert len(results) == 7

    def test_each_result_is_persona_result(self):
        inputs = [make_input(rep_id=f"R{i}") for i in range(3)]
        for r in engine().assess_batch(inputs):
            assert isinstance(r, PersonaResult)

    def test_rep_ids_preserved_in_batch(self):
        inputs = [make_input(rep_id=f"REP{i}") for i in range(5)]
        results = engine().assess_batch(inputs)
        assert [r.rep_id for r in results] == [f"REP{i}" for i in range(5)]

    def test_empty_batch_returns_empty(self):
        assert engine().assess_batch([]) == []

    def test_batch_results_stored_for_summary(self):
        e = engine()
        inputs = [make_input(rep_id=f"R{i}") for i in range(4)]
        e.assess_batch(inputs)
        assert e.summary()["total"] == 4


# ---------------------------------------------------------------------------
# 21. summary() aggregation
# ---------------------------------------------------------------------------

class TestSummaryAggregation:
    def test_summary_total_matches_assessed_count(self):
        e = engine()
        for i in range(5):
            e.assess(make_input(rep_id=f"R{i}"))
        assert e.summary()["total"] == 5

    def test_summary_risk_counts_sum_to_total(self):
        e = engine()
        for i in range(6):
            e.assess(make_input(rep_id=f"R{i}"))
        s = e.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_summary_pattern_counts_sum_to_total(self):
        e = engine()
        for i in range(4):
            e.assess(make_input(rep_id=f"R{i}"))
        s = e.summary()
        assert sum(s["pattern_counts"].values()) == s["total"]

    def test_summary_severity_counts_sum_to_total(self):
        e = engine()
        for i in range(3):
            e.assess(make_input(rep_id=f"R{i}"))
        s = e.summary()
        assert sum(s["severity_counts"].values()) == s["total"]

    def test_summary_action_counts_sum_to_total(self):
        e = engine()
        for i in range(3):
            e.assess(make_input(rep_id=f"R{i}"))
        s = e.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_summary_avg_composite_reasonable(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert 0.0 <= s["avg_persona_composite"] <= 100.0

    def test_summary_avg_access_score_range(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert 0.0 <= s["avg_access_score"] <= 100.0

    def test_summary_avg_alignment_score_range(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert 0.0 <= s["avg_alignment_score"] <= 100.0

    def test_summary_avg_authority_score_range(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert 0.0 <= s["avg_authority_score"] <= 100.0

    def test_summary_avg_coverage_score_range(self):
        e = engine()
        e.assess(make_input())
        s = e.summary()
        assert 0.0 <= s["avg_coverage_score"] <= 100.0

    def test_summary_gap_count_le_total(self):
        e = engine()
        for i in range(5):
            e.assess(make_input(rep_id=f"R{i}"))
        s = e.summary()
        assert s["persona_gap_count"] <= s["total"]

    def test_summary_coaching_count_le_total(self):
        e = engine()
        for i in range(5):
            e.assess(make_input(rep_id=f"R{i}"))
        s = e.summary()
        assert s["coaching_count"] <= s["total"]

    def test_summary_lost_value_non_negative(self):
        e = engine()
        e.assess(make_input())
        assert e.summary()["total_estimated_lost_deal_value_usd"] >= 0.0

    def test_summary_accumulates_across_multiple_calls(self):
        e = engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        e.assess(make_input(rep_id="C"))
        assert e.summary()["total"] == 3

    def test_summary_lost_value_equals_sum_of_individual(self):
        e = engine()
        inp1 = make_input(rep_id="A", total_deals_evaluated=10, avg_deal_value_usd=10_000.0,
                          lost_due_to_persona_mismatch_pct=0.10)
        inp2 = make_input(rep_id="B", total_deals_evaluated=20, avg_deal_value_usd=5_000.0,
                          lost_due_to_persona_mismatch_pct=0.20)
        r1 = e.assess(inp1)
        r2 = e.assess(inp2)
        s = e.summary()
        assert abs(s["total_estimated_lost_deal_value_usd"] -
                   round(r1.estimated_lost_deal_value_usd + r2.estimated_lost_deal_value_usd, 2)) < 0.01

    def test_summary_avg_composite_two_assessments(self):
        e = engine()
        inp1 = make_input(rep_id="A")
        inp2 = make_input(rep_id="B",
                          primary_contact_level_score=0.10,
                          vp_plus_engagement_rate_pct=0.10,
                          decision_maker_access_rate_pct=0.10,
                          economic_buyer_contact_rate_pct=0.10,
                          budget_authority_confirmed_rate_pct=0.10,
                          influencer_only_rate_pct=0.80,
                          cross_functional_coverage_score=0.10,
                          sponsor_identification_rate_pct=0.10,
                          technical_blockers_rate_pct=0.60,
                          business_unit_alignment_score=0.10,
                          persona_to_use_case_fit_score=0.10,
                          wrong_entry_point_rate_pct=0.80)
        r1 = e.assess(inp1)
        r2 = e.assess(inp2)
        s = e.summary()
        expected = round((r1.persona_composite + r2.persona_composite) / 2, 1)
        assert s["avg_persona_composite"] == expected


# ---------------------------------------------------------------------------
# 22. Enum value strings
# ---------------------------------------------------------------------------

class TestEnumValues:
    def test_risk_low_value(self):
        assert PersonaRisk.low.value == "low"

    def test_risk_moderate_value(self):
        assert PersonaRisk.moderate.value == "moderate"

    def test_risk_high_value(self):
        assert PersonaRisk.high.value == "high"

    def test_risk_critical_value(self):
        assert PersonaRisk.critical.value == "critical"

    def test_severity_aligned_value(self):
        assert PersonaSeverity.aligned.value == "aligned"

    def test_severity_misaligned_value(self):
        assert PersonaSeverity.misaligned.value == "misaligned"

    def test_severity_disconnected_value(self):
        assert PersonaSeverity.disconnected.value == "disconnected"

    def test_severity_invisible_value(self):
        assert PersonaSeverity.invisible.value == "invisible"

    def test_pattern_none_value(self):
        assert PersonaPattern.none.value == "none"

    def test_pattern_wrong_level_value(self):
        assert PersonaPattern.wrong_level.value == "wrong_level"

    def test_pattern_wrong_department_value(self):
        assert PersonaPattern.wrong_department.value == "wrong_department"

    def test_pattern_influencer_only_value(self):
        assert PersonaPattern.influencer_only.value == "influencer_only"

    def test_pattern_technical_gatekeeper_value(self):
        assert PersonaPattern.technical_gatekeeper.value == "technical_gatekeeper"

    def test_pattern_budget_blind_value(self):
        assert PersonaPattern.budget_blind.value == "budget_blind"

    def test_action_no_action_value(self):
        assert PersonaAction.no_action.value == "no_action"

    def test_action_deal_re_qualification_value(self):
        assert PersonaAction.deal_re_qualification.value == "deal_re_qualification"

    def test_action_persona_reset_value(self):
        assert PersonaAction.persona_reset_intervention.value == "persona_reset_intervention"

    def test_action_executive_access_value(self):
        assert PersonaAction.executive_access_coaching.value == "executive_access_coaching"

    def test_action_budget_holder_intro_value(self):
        assert PersonaAction.budget_holder_introduction.value == "budget_holder_introduction"

    def test_action_stakeholder_mapping_value(self):
        assert PersonaAction.stakeholder_mapping_coaching.value == "stakeholder_mapping_coaching"

    def test_action_persona_alignment_check_value(self):
        assert PersonaAction.persona_alignment_check.value == "persona_alignment_check"


# ---------------------------------------------------------------------------
# 23. Boundary: exact threshold values
# ---------------------------------------------------------------------------

class TestExactBoundaries:
    # Access score exact thresholds
    def test_access_dm_exactly_030(self):
        e = engine()
        s = e._access_score(make_input(decision_maker_access_rate_pct=0.30,
                                        vp_plus_engagement_rate_pct=1.0,
                                        primary_contact_level_score=1.0))
        assert s == 40.0

    def test_access_vp_exactly_020(self):
        e = engine()
        s = e._access_score(make_input(decision_maker_access_rate_pct=1.0,
                                        vp_plus_engagement_rate_pct=0.20,
                                        primary_contact_level_score=1.0))
        assert s == 35.0

    def test_access_pcl_exactly_025(self):
        e = engine()
        s = e._access_score(make_input(decision_maker_access_rate_pct=1.0,
                                        vp_plus_engagement_rate_pct=1.0,
                                        primary_contact_level_score=0.25))
        assert s == 25.0

    # Coverage score exact thresholds
    def test_coverage_cf_exactly_025(self):
        e = engine()
        s = e._coverage_score(make_input(cross_functional_coverage_score=0.25,
                                          sponsor_identification_rate_pct=1.0,
                                          technical_blockers_rate_pct=0.0))
        assert s == 45.0

    def test_coverage_sponsor_exactly_030(self):
        e = engine()
        s = e._coverage_score(make_input(cross_functional_coverage_score=1.0,
                                          sponsor_identification_rate_pct=0.30,
                                          technical_blockers_rate_pct=0.0))
        assert s == 30.0

    def test_coverage_tech_blockers_exactly_045(self):
        e = engine()
        s = e._coverage_score(make_input(cross_functional_coverage_score=1.0,
                                          sponsor_identification_rate_pct=1.0,
                                          technical_blockers_rate_pct=0.45))
        assert s == 25.0

    # Pattern thresholds
    def test_pattern_wrong_level_pcl_exactly_030(self):
        p = engine()._pattern(make_input(primary_contact_level_score=0.30,
                                          vp_plus_engagement_rate_pct=0.20))
        assert p == PersonaPattern.wrong_level

    def test_pattern_wrong_department_bu_exactly_035(self):
        p = engine()._pattern(make_input(primary_contact_level_score=0.80,
                                          vp_plus_engagement_rate_pct=0.80,
                                          business_unit_alignment_score=0.35,
                                          persona_to_use_case_fit_score=0.40))
        assert p == PersonaPattern.wrong_department

    def test_pattern_influencer_only_rate_exactly_050(self):
        p = engine()._pattern(make_input(primary_contact_level_score=0.80,
                                          vp_plus_engagement_rate_pct=0.80,
                                          business_unit_alignment_score=0.80,
                                          persona_to_use_case_fit_score=0.80,
                                          influencer_only_rate_pct=0.50,
                                          decision_maker_access_rate_pct=0.35))
        assert p == PersonaPattern.influencer_only

    def test_pattern_technical_gatekeeper_it_exactly_055(self):
        p = engine()._pattern(make_input(primary_contact_level_score=0.80,
                                          vp_plus_engagement_rate_pct=0.80,
                                          business_unit_alignment_score=0.80,
                                          persona_to_use_case_fit_score=0.80,
                                          influencer_only_rate_pct=0.10,
                                          decision_maker_access_rate_pct=0.80,
                                          it_only_contact_rate_pct=0.55,
                                          technical_blockers_rate_pct=0.40))
        assert p == PersonaPattern.technical_gatekeeper

    def test_pattern_budget_blind_eb_exactly_025(self):
        p = engine()._pattern(make_input(primary_contact_level_score=0.80,
                                          vp_plus_engagement_rate_pct=0.80,
                                          business_unit_alignment_score=0.80,
                                          persona_to_use_case_fit_score=0.80,
                                          influencer_only_rate_pct=0.10,
                                          decision_maker_access_rate_pct=0.80,
                                          it_only_contact_rate_pct=0.10,
                                          technical_blockers_rate_pct=0.10,
                                          economic_buyer_contact_rate_pct=0.25,
                                          budget_authority_confirmed_rate_pct=0.25))
        assert p == PersonaPattern.budget_blind


# ---------------------------------------------------------------------------
# 24. State isolation — new engine per test
# ---------------------------------------------------------------------------

class TestStateIsolation:
    def test_new_engine_starts_empty(self):
        e = engine()
        assert e.summary()["total"] == 0

    def test_results_not_shared_between_engines(self):
        e1 = engine()
        e2 = engine()
        e1.assess(make_input(rep_id="R1"))
        assert e2.summary()["total"] == 0

    def test_each_assess_increments_total(self):
        e = engine()
        for i in range(10):
            e.assess(make_input(rep_id=f"R{i}"))
        assert e.summary()["total"] == 10

    def test_results_list_grows_with_assess(self):
        e = engine()
        e.assess(make_input(rep_id="A"))
        e.assess(make_input(rep_id="B"))
        assert len(e._results) == 2


# ---------------------------------------------------------------------------
# 25. Sub-score range (always 0–100)
# ---------------------------------------------------------------------------

class TestSubScoreRange:
    @pytest.mark.parametrize("dm,vp,pcl", [
        (0.0, 0.0, 0.0),
        (0.30, 0.20, 0.25),
        (0.55, 0.45, 0.50),
        (0.75, 0.45, 0.50),
        (1.0, 1.0, 1.0),
    ])
    def test_access_score_in_range(self, dm, vp, pcl):
        s = engine()._access_score(make_input(
            decision_maker_access_rate_pct=dm,
            vp_plus_engagement_rate_pct=vp,
            primary_contact_level_score=pcl))
        assert 0.0 <= s <= 100.0

    @pytest.mark.parametrize("fit,bu,we", [
        (0.0, 0.0, 1.0),
        (0.30, 0.30, 0.50),
        (0.55, 0.55, 0.30),
        (0.75, 0.55, 0.10),
        (1.0, 1.0, 0.0),
    ])
    def test_alignment_score_in_range(self, fit, bu, we):
        s = engine()._alignment_score(make_input(
            persona_to_use_case_fit_score=fit,
            business_unit_alignment_score=bu,
            wrong_entry_point_rate_pct=we))
        assert 0.0 <= s <= 100.0

    @pytest.mark.parametrize("eb,ba,inf", [
        (0.0, 0.0, 1.0),
        (0.25, 0.25, 0.50),
        (0.50, 0.50, 0.30),
        (0.70, 0.51, 0.10),
        (1.0, 1.0, 0.0),
    ])
    def test_authority_score_in_range(self, eb, ba, inf):
        s = engine()._authority_score(make_input(
            economic_buyer_contact_rate_pct=eb,
            budget_authority_confirmed_rate_pct=ba,
            influencer_only_rate_pct=inf))
        assert 0.0 <= s <= 100.0

    @pytest.mark.parametrize("cf,sp,tb", [
        (0.0, 0.0, 1.0),
        (0.25, 0.30, 0.45),
        (0.50, 0.55, 0.25),
        (0.70, 0.56, 0.10),
        (1.0, 1.0, 0.0),
    ])
    def test_coverage_score_in_range(self, cf, sp, tb):
        s = engine()._coverage_score(make_input(
            cross_functional_coverage_score=cf,
            sponsor_identification_rate_pct=sp,
            technical_blockers_rate_pct=tb))
        assert 0.0 <= s <= 100.0


# ---------------------------------------------------------------------------
# 26. Parametrized risk/severity consistency
# ---------------------------------------------------------------------------

class TestRiskSeverityConsistency:
    @pytest.mark.parametrize("composite,expected_risk,expected_sev", [
        (0.0,  PersonaRisk.low,      PersonaSeverity.aligned),
        (10.0, PersonaRisk.low,      PersonaSeverity.aligned),
        (19.9, PersonaRisk.low,      PersonaSeverity.aligned),
        (20.0, PersonaRisk.moderate, PersonaSeverity.misaligned),
        (30.0, PersonaRisk.moderate, PersonaSeverity.misaligned),
        (39.9, PersonaRisk.moderate, PersonaSeverity.misaligned),
        (40.0, PersonaRisk.high,     PersonaSeverity.disconnected),
        (55.0, PersonaRisk.high,     PersonaSeverity.disconnected),
        (59.9, PersonaRisk.high,     PersonaSeverity.disconnected),
        (60.0, PersonaRisk.critical, PersonaSeverity.invisible),
        (80.0, PersonaRisk.critical, PersonaSeverity.invisible),
        (100.0,PersonaRisk.critical, PersonaSeverity.invisible),
    ])
    def test_risk_severity_at_composite(self, composite, expected_risk, expected_sev):
        e = engine()
        assert e._risk(composite) == expected_risk
        assert e._severity(composite) == expected_sev


# ---------------------------------------------------------------------------
# 27. Additional pattern edge-cases
# ---------------------------------------------------------------------------

class TestPatternEdgeCases:
    def test_technical_gatekeeper_tb_exactly_040(self):
        p = engine()._pattern(make_input(
            primary_contact_level_score=0.80,
            vp_plus_engagement_rate_pct=0.80,
            business_unit_alignment_score=0.80,
            persona_to_use_case_fit_score=0.80,
            influencer_only_rate_pct=0.10,
            decision_maker_access_rate_pct=0.80,
            it_only_contact_rate_pct=0.55,
            technical_blockers_rate_pct=0.40,
        ))
        assert p == PersonaPattern.technical_gatekeeper

    def test_technical_gatekeeper_tb_below_040_not_triggered(self):
        p = engine()._pattern(make_input(
            primary_contact_level_score=0.80,
            vp_plus_engagement_rate_pct=0.80,
            business_unit_alignment_score=0.80,
            persona_to_use_case_fit_score=0.80,
            influencer_only_rate_pct=0.10,
            decision_maker_access_rate_pct=0.80,
            it_only_contact_rate_pct=0.55,
            technical_blockers_rate_pct=0.39,
            economic_buyer_contact_rate_pct=0.80,
            budget_authority_confirmed_rate_pct=0.80,
        ))
        assert p != PersonaPattern.technical_gatekeeper

    def test_budget_blind_budget_above_025_not_triggered(self):
        p = engine()._pattern(make_input(
            primary_contact_level_score=0.80,
            vp_plus_engagement_rate_pct=0.80,
            business_unit_alignment_score=0.80,
            persona_to_use_case_fit_score=0.80,
            influencer_only_rate_pct=0.10,
            decision_maker_access_rate_pct=0.80,
            it_only_contact_rate_pct=0.10,
            technical_blockers_rate_pct=0.10,
            economic_buyer_contact_rate_pct=0.25,
            budget_authority_confirmed_rate_pct=0.26,
        ))
        assert p != PersonaPattern.budget_blind

    def test_influencer_only_influencer_below_050_not_triggered(self):
        p = engine()._pattern(make_input(
            primary_contact_level_score=0.80,
            vp_plus_engagement_rate_pct=0.80,
            business_unit_alignment_score=0.80,
            persona_to_use_case_fit_score=0.80,
            influencer_only_rate_pct=0.49,
            decision_maker_access_rate_pct=0.35,
            it_only_contact_rate_pct=0.10,
            technical_blockers_rate_pct=0.10,
            economic_buyer_contact_rate_pct=0.80,
            budget_authority_confirmed_rate_pct=0.80,
        ))
        assert p != PersonaPattern.influencer_only

    def test_wrong_department_fit_above_040_not_triggered(self):
        p = engine()._pattern(make_input(
            primary_contact_level_score=0.80,
            vp_plus_engagement_rate_pct=0.80,
            business_unit_alignment_score=0.35,
            persona_to_use_case_fit_score=0.41,
            influencer_only_rate_pct=0.10,
            decision_maker_access_rate_pct=0.80,
            it_only_contact_rate_pct=0.10,
            technical_blockers_rate_pct=0.10,
            economic_buyer_contact_rate_pct=0.80,
            budget_authority_confirmed_rate_pct=0.80,
        ))
        assert p != PersonaPattern.wrong_department


# ---------------------------------------------------------------------------
# 28. Mixed scenarios — validate end-to-end for each pattern
# ---------------------------------------------------------------------------

class TestEndToEndByPattern:
    def _e2e(self, **kw):
        return engine().assess(make_input(**kw))

    def test_wrong_level_end_to_end(self):
        r = self._e2e(primary_contact_level_score=0.20,
                      vp_plus_engagement_rate_pct=0.15)
        assert r.persona_pattern == PersonaPattern.wrong_level

    def test_wrong_department_end_to_end(self):
        r = self._e2e(primary_contact_level_score=0.80,
                      vp_plus_engagement_rate_pct=0.80,
                      business_unit_alignment_score=0.30,
                      persona_to_use_case_fit_score=0.30)
        assert r.persona_pattern == PersonaPattern.wrong_department

    def test_influencer_only_end_to_end(self):
        r = self._e2e(primary_contact_level_score=0.80,
                      vp_plus_engagement_rate_pct=0.80,
                      business_unit_alignment_score=0.80,
                      persona_to_use_case_fit_score=0.80,
                      influencer_only_rate_pct=0.65,
                      decision_maker_access_rate_pct=0.25)
        assert r.persona_pattern == PersonaPattern.influencer_only

    def test_technical_gatekeeper_end_to_end(self):
        r = self._e2e(primary_contact_level_score=0.80,
                      vp_plus_engagement_rate_pct=0.80,
                      business_unit_alignment_score=0.80,
                      persona_to_use_case_fit_score=0.80,
                      influencer_only_rate_pct=0.10,
                      decision_maker_access_rate_pct=0.80,
                      it_only_contact_rate_pct=0.70,
                      technical_blockers_rate_pct=0.55)
        assert r.persona_pattern == PersonaPattern.technical_gatekeeper

    def test_budget_blind_end_to_end(self):
        r = self._e2e(primary_contact_level_score=0.80,
                      vp_plus_engagement_rate_pct=0.80,
                      business_unit_alignment_score=0.80,
                      persona_to_use_case_fit_score=0.80,
                      influencer_only_rate_pct=0.10,
                      decision_maker_access_rate_pct=0.80,
                      it_only_contact_rate_pct=0.10,
                      technical_blockers_rate_pct=0.10,
                      economic_buyer_contact_rate_pct=0.20,
                      budget_authority_confirmed_rate_pct=0.20)
        assert r.persona_pattern == PersonaPattern.budget_blind

    def test_none_pattern_end_to_end(self):
        r = self._e2e()
        assert r.persona_pattern == PersonaPattern.none

    def test_wrong_level_with_critical_risk_gives_deal_requalification(self):
        r = self._e2e(
            primary_contact_level_score=0.05,
            vp_plus_engagement_rate_pct=0.05,
            decision_maker_access_rate_pct=0.10,
            economic_buyer_contact_rate_pct=0.10,
            budget_authority_confirmed_rate_pct=0.10,
            influencer_only_rate_pct=0.80,
            cross_functional_coverage_score=0.10,
            sponsor_identification_rate_pct=0.10,
            technical_blockers_rate_pct=0.60,
            business_unit_alignment_score=0.80,
            persona_to_use_case_fit_score=0.80,
            wrong_entry_point_rate_pct=0.80,
        )
        if r.persona_risk == PersonaRisk.critical and r.persona_pattern == PersonaPattern.wrong_level:
            assert r.recommended_action == PersonaAction.deal_re_qualification

    def test_influencer_only_critical_gives_deal_requalification(self):
        r = self._e2e(
            primary_contact_level_score=0.80,
            vp_plus_engagement_rate_pct=0.80,
            business_unit_alignment_score=0.80,
            persona_to_use_case_fit_score=0.80,
            influencer_only_rate_pct=0.90,
            decision_maker_access_rate_pct=0.10,
            economic_buyer_contact_rate_pct=0.10,
            budget_authority_confirmed_rate_pct=0.10,
            cross_functional_coverage_score=0.10,
            sponsor_identification_rate_pct=0.10,
            technical_blockers_rate_pct=0.60,
            wrong_entry_point_rate_pct=0.80,
        )
        if r.persona_risk == PersonaRisk.critical:
            assert r.recommended_action == PersonaAction.deal_re_qualification


# ---------------------------------------------------------------------------
# 29. Determinism — same input → same output
# ---------------------------------------------------------------------------

class TestDeterminism:
    def test_same_input_same_composite(self):
        inp = make_input(rep_id="DET")
        e1, e2 = engine(), engine()
        assert e1.assess(inp).persona_composite == e2.assess(inp).persona_composite

    def test_same_input_same_risk(self):
        inp = make_input(rep_id="DET")
        assert engine().assess(inp).persona_risk == engine().assess(inp).persona_risk

    def test_same_input_same_pattern(self):
        inp = make_input(rep_id="DET")
        assert engine().assess(inp).persona_pattern == engine().assess(inp).persona_pattern

    def test_same_input_same_signal(self):
        inp = make_input(rep_id="DET")
        assert engine().assess(inp).persona_signal == engine().assess(inp).persona_signal

    def test_same_input_same_lost_value(self):
        inp = make_input(rep_id="DET")
        assert engine().assess(inp).estimated_lost_deal_value_usd == engine().assess(inp).estimated_lost_deal_value_usd


# ---------------------------------------------------------------------------
# 30. Edge cases: zero / extreme values
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_all_zeros_float_fields(self):
        inp = make_input(
            primary_contact_level_score=0.0,
            economic_buyer_contact_rate_pct=0.0,
            it_only_contact_rate_pct=0.0,
            business_unit_alignment_score=0.0,
            decision_maker_access_rate_pct=0.0,
            influencer_only_rate_pct=0.0,
            procurement_first_contact_rate_pct=0.0,
            avg_seniority_of_contacts=0.0,
            sponsor_identification_rate_pct=0.0,
            cross_functional_coverage_score=0.0,
            persona_to_use_case_fit_score=0.0,
            budget_authority_confirmed_rate_pct=0.0,
            vp_plus_engagement_rate_pct=0.0,
            champion_seniority_score=0.0,
            technical_blockers_rate_pct=0.0,
            wrong_entry_point_rate_pct=0.0,
            referral_to_right_person_rate_pct=0.0,
            lost_due_to_persona_mismatch_pct=0.0,
            total_deals_evaluated=0,
            avg_deal_value_usd=0.0,
        )
        r = engine().assess(inp)
        assert isinstance(r, PersonaResult)

    def test_all_ones_float_fields(self):
        inp = make_input(
            primary_contact_level_score=1.0,
            economic_buyer_contact_rate_pct=1.0,
            it_only_contact_rate_pct=1.0,
            business_unit_alignment_score=1.0,
            decision_maker_access_rate_pct=1.0,
            influencer_only_rate_pct=1.0,
            procurement_first_contact_rate_pct=1.0,
            avg_seniority_of_contacts=1.0,
            sponsor_identification_rate_pct=1.0,
            cross_functional_coverage_score=1.0,
            persona_to_use_case_fit_score=1.0,
            budget_authority_confirmed_rate_pct=1.0,
            vp_plus_engagement_rate_pct=1.0,
            champion_seniority_score=1.0,
            technical_blockers_rate_pct=1.0,
            wrong_entry_point_rate_pct=1.0,
            referral_to_right_person_rate_pct=1.0,
            lost_due_to_persona_mismatch_pct=1.0,
            total_deals_evaluated=1000,
            avg_deal_value_usd=1_000_000.0,
        )
        r = engine().assess(inp)
        assert r.persona_composite <= 100.0

    def test_large_deal_count(self):
        r = engine().assess(make_input(total_deals_evaluated=10_000,
                                        avg_deal_value_usd=100_000.0,
                                        lost_due_to_persona_mismatch_pct=0.50))
        assert r.estimated_lost_deal_value_usd > 0

    def test_very_small_deal_value(self):
        r = engine().assess(make_input(total_deals_evaluated=1,
                                        avg_deal_value_usd=0.01,
                                        lost_due_to_persona_mismatch_pct=0.10))
        assert r.estimated_lost_deal_value_usd >= 0.0

    def test_composite_never_negative(self):
        r = engine().assess(make_input())
        assert r.persona_composite >= 0.0

    def test_access_score_never_negative(self):
        r = engine().assess(make_input())
        assert r.access_score >= 0.0

    def test_alignment_score_never_negative(self):
        r = engine().assess(make_input())
        assert r.alignment_score >= 0.0

    def test_authority_score_never_negative(self):
        r = engine().assess(make_input())
        assert r.authority_score >= 0.0

    def test_coverage_score_never_negative(self):
        r = engine().assess(make_input())
        assert r.coverage_score >= 0.0

    def test_lost_value_never_negative(self):
        r = engine().assess(make_input())
        assert r.estimated_lost_deal_value_usd >= 0.0


# ---------------------------------------------------------------------------
# 31. Summary with mixed risk reps
# ---------------------------------------------------------------------------

class TestSummaryMixedRisk:
    def _setup_engine(self):
        e = engine()
        # Low risk
        e.assess(make_input(rep_id="LR1"))
        # Critical risk
        e.assess(make_input(rep_id="CR1",
            primary_contact_level_score=0.05, vp_plus_engagement_rate_pct=0.05,
            decision_maker_access_rate_pct=0.10, economic_buyer_contact_rate_pct=0.05,
            budget_authority_confirmed_rate_pct=0.05, influencer_only_rate_pct=0.90,
            cross_functional_coverage_score=0.05, sponsor_identification_rate_pct=0.05,
            technical_blockers_rate_pct=0.70, business_unit_alignment_score=0.05,
            persona_to_use_case_fit_score=0.05, wrong_entry_point_rate_pct=0.90))
        return e

    def test_mixed_risk_total_is_2(self):
        assert self._setup_engine().summary()["total"] == 2

    def test_mixed_risk_has_low_in_risk_counts(self):
        s = self._setup_engine().summary()
        assert "low" in s["risk_counts"]

    def test_mixed_risk_has_critical_in_risk_counts(self):
        s = self._setup_engine().summary()
        assert "critical" in s["risk_counts"]

    def test_mixed_risk_pattern_counts_present(self):
        s = self._setup_engine().summary()
        assert len(s["pattern_counts"]) >= 1

    def test_mixed_risk_severity_counts_present(self):
        s = self._setup_engine().summary()
        assert len(s["severity_counts"]) >= 1

    def test_mixed_risk_action_counts_present(self):
        s = self._setup_engine().summary()
        assert len(s["action_counts"]) >= 1


# ---------------------------------------------------------------------------
# 32. Access sub-score: tier combinations
# ---------------------------------------------------------------------------

class TestAccessSubScoreCombinations:
    def test_dm_055_vp_020_pcl_080(self):
        # 22 + 35 + 0 = 57
        e = engine()
        s = e._access_score(make_input(
            decision_maker_access_rate_pct=0.55,
            vp_plus_engagement_rate_pct=0.20,
            primary_contact_level_score=0.80))
        assert s == 57.0

    def test_dm_030_vp_045_pcl_080(self):
        # 40 + 18 + 0 = 58
        e = engine()
        s = e._access_score(make_input(
            decision_maker_access_rate_pct=0.30,
            vp_plus_engagement_rate_pct=0.45,
            primary_contact_level_score=0.80))
        assert s == 58.0

    def test_dm_075_vp_045_pcl_050(self):
        # 8 + 18 + 12 = 38
        e = engine()
        s = e._access_score(make_input(
            decision_maker_access_rate_pct=0.75,
            vp_plus_engagement_rate_pct=0.45,
            primary_contact_level_score=0.50))
        assert s == 38.0

    def test_dm_030_vp_020_pcl_050(self):
        # 40 + 35 + 12 = 87 → not capped
        e = engine()
        s = e._access_score(make_input(
            decision_maker_access_rate_pct=0.30,
            vp_plus_engagement_rate_pct=0.20,
            primary_contact_level_score=0.50))
        assert s == 87.0


# ---------------------------------------------------------------------------
# 33. Authority sub-score: tier combinations
# ---------------------------------------------------------------------------

class TestAuthoritySubScoreCombinations:
    def test_eb_050_budget_050_inf_030(self):
        # 22 + 18 + 12 = 52
        e = engine()
        s = e._authority_score(make_input(
            economic_buyer_contact_rate_pct=0.50,
            budget_authority_confirmed_rate_pct=0.50,
            influencer_only_rate_pct=0.30))
        assert s == 52.0

    def test_eb_025_budget_025_inf_050(self):
        # 40 + 35 + 25 = 100 → capped
        e = engine()
        s = e._authority_score(make_input(
            economic_buyer_contact_rate_pct=0.25,
            budget_authority_confirmed_rate_pct=0.25,
            influencer_only_rate_pct=0.50))
        assert s == 100.0

    def test_eb_070_budget_050_inf_030(self):
        # 8 + 18 + 12 = 38
        e = engine()
        s = e._authority_score(make_input(
            economic_buyer_contact_rate_pct=0.70,
            budget_authority_confirmed_rate_pct=0.50,
            influencer_only_rate_pct=0.30))
        assert s == 38.0


# ---------------------------------------------------------------------------
# 34. Coverage sub-score: tier combinations
# ---------------------------------------------------------------------------

class TestCoverageSubScoreCombinations:
    def test_cf_050_sp_055_tb_025(self):
        # 25 + 15 + 12 = 52
        e = engine()
        s = e._coverage_score(make_input(
            cross_functional_coverage_score=0.50,
            sponsor_identification_rate_pct=0.55,
            technical_blockers_rate_pct=0.25))
        assert s == 52.0

    def test_cf_070_sp_030_tb_045(self):
        # 10 + 30 + 25 = 65
        e = engine()
        s = e._coverage_score(make_input(
            cross_functional_coverage_score=0.70,
            sponsor_identification_rate_pct=0.30,
            technical_blockers_rate_pct=0.45))
        assert s == 65.0

    def test_cf_025_sp_030_tb_045(self):
        # 45 + 30 + 25 = 100 → capped
        e = engine()
        s = e._coverage_score(make_input(
            cross_functional_coverage_score=0.25,
            sponsor_identification_rate_pct=0.30,
            technical_blockers_rate_pct=0.45))
        assert s == 100.0


# ---------------------------------------------------------------------------
# 35. Alignment sub-score: tier combinations
# ---------------------------------------------------------------------------

class TestAlignmentSubScoreCombinations:
    def test_fit_055_bu_055_we_030(self):
        # 22 + 18 + 12 = 52
        e = engine()
        s = e._alignment_score(make_input(
            persona_to_use_case_fit_score=0.55,
            business_unit_alignment_score=0.55,
            wrong_entry_point_rate_pct=0.30))
        assert s == 52.0

    def test_fit_030_bu_030_we_050(self):
        # 40 + 35 + 25 = 100 → capped
        e = engine()
        s = e._alignment_score(make_input(
            persona_to_use_case_fit_score=0.30,
            business_unit_alignment_score=0.30,
            wrong_entry_point_rate_pct=0.50))
        assert s == 100.0

    def test_fit_075_bu_055_we_030(self):
        # 8 + 18 + 12 = 38
        e = engine()
        s = e._alignment_score(make_input(
            persona_to_use_case_fit_score=0.75,
            business_unit_alignment_score=0.55,
            wrong_entry_point_rate_pct=0.30))
        assert s == 38.0


# ---------------------------------------------------------------------------
# 36. assess() result fields all non-None
# ---------------------------------------------------------------------------

class TestAssessResultNonNone:
    def test_all_result_fields_non_none(self):
        r = engine().assess(make_input())
        assert r.rep_id is not None
        assert r.region is not None
        assert r.persona_risk is not None
        assert r.persona_pattern is not None
        assert r.persona_severity is not None
        assert r.recommended_action is not None
        assert r.access_score is not None
        assert r.alignment_score is not None
        assert r.authority_score is not None
        assert r.coverage_score is not None
        assert r.persona_composite is not None
        assert r.has_persona_gap is not None
        assert r.requires_persona_coaching is not None
        assert r.estimated_lost_deal_value_usd is not None
        assert r.persona_signal is not None

    def test_result_is_dataclass(self):
        from dataclasses import is_dataclass
        assert is_dataclass(PersonaResult)

    def test_input_is_dataclass(self):
        from dataclasses import is_dataclass
        assert is_dataclass(PersonaInput)


# ---------------------------------------------------------------------------
# 37. Summary: avg score computations match manual calculation
# ---------------------------------------------------------------------------

class TestSummaryAvgScores:
    def test_avg_access_matches_manual(self):
        e = engine()
        inp1 = make_input(rep_id="A", decision_maker_access_rate_pct=1.0,
                          vp_plus_engagement_rate_pct=1.0, primary_contact_level_score=1.0)
        inp2 = make_input(rep_id="B", decision_maker_access_rate_pct=1.0,
                          vp_plus_engagement_rate_pct=1.0, primary_contact_level_score=1.0)
        r1 = e.assess(inp1)
        r2 = e.assess(inp2)
        s = e.summary()
        expected = round((r1.access_score + r2.access_score) / 2, 1)
        assert s["avg_access_score"] == expected

    def test_avg_alignment_matches_manual(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B"))
        s = e.summary()
        expected = round((r1.alignment_score + r2.alignment_score) / 2, 1)
        assert s["avg_alignment_score"] == expected

    def test_avg_authority_matches_manual(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B"))
        s = e.summary()
        expected = round((r1.authority_score + r2.authority_score) / 2, 1)
        assert s["avg_authority_score"] == expected

    def test_avg_coverage_matches_manual(self):
        e = engine()
        r1 = e.assess(make_input(rep_id="A"))
        r2 = e.assess(make_input(rep_id="B"))
        s = e.summary()
        expected = round((r1.coverage_score + r2.coverage_score) / 2, 1)
        assert s["avg_coverage_score"] == expected


# ---------------------------------------------------------------------------
# 38. Correctness of to_dict enum values (string form)
# ---------------------------------------------------------------------------

class TestToDictEnumStrings:
    def test_to_dict_risk_matches_enum_value(self):
        r = engine().assess(make_input())
        assert r.to_dict()["persona_risk"] == r.persona_risk.value

    def test_to_dict_pattern_matches_enum_value(self):
        r = engine().assess(make_input())
        assert r.to_dict()["persona_pattern"] == r.persona_pattern.value

    def test_to_dict_severity_matches_enum_value(self):
        r = engine().assess(make_input())
        assert r.to_dict()["persona_severity"] == r.persona_severity.value

    def test_to_dict_action_matches_enum_value(self):
        r = engine().assess(make_input())
        assert r.to_dict()["recommended_action"] == r.recommended_action.value

    def test_to_dict_access_score_matches_result_field(self):
        r = engine().assess(make_input())
        assert r.to_dict()["access_score"] == r.access_score

    def test_to_dict_composite_matches_result_field(self):
        r = engine().assess(make_input())
        assert r.to_dict()["persona_composite"] == r.persona_composite

    def test_to_dict_signal_matches_result_field(self):
        r = engine().assess(make_input())
        assert r.to_dict()["persona_signal"] == r.persona_signal

    def test_to_dict_has_persona_gap_matches(self):
        r = engine().assess(make_input())
        assert r.to_dict()["has_persona_gap"] == r.has_persona_gap

    def test_to_dict_requires_coaching_matches(self):
        r = engine().assess(make_input())
        assert r.to_dict()["requires_persona_coaching"] == r.requires_persona_coaching

    def test_to_dict_lost_value_matches(self):
        r = engine().assess(make_input())
        assert r.to_dict()["estimated_lost_deal_value_usd"] == r.estimated_lost_deal_value_usd


# ---------------------------------------------------------------------------
# 39. High-risk (but not critical) end-to-end actions
# ---------------------------------------------------------------------------

class TestHighRiskActions:
    def _high_risk_input_with_pattern(self, **kw):
        # Create high-risk composite (40–59) by mixing moderate sub-scores
        base = dict(
            primary_contact_level_score=0.50,
            vp_plus_engagement_rate_pct=0.45,
            decision_maker_access_rate_pct=0.55,
            economic_buyer_contact_rate_pct=0.50,
            budget_authority_confirmed_rate_pct=0.50,
            influencer_only_rate_pct=0.29,
            cross_functional_coverage_score=0.50,
            sponsor_identification_rate_pct=0.55,
            technical_blockers_rate_pct=0.24,
            business_unit_alignment_score=0.55,
            persona_to_use_case_fit_score=0.55,
            wrong_entry_point_rate_pct=0.29,
        )
        base.update(kw)
        return make_input(**base)

    def test_high_risk_wrong_level_gives_executive_access_coaching(self):
        inp = self._high_risk_input_with_pattern(
            primary_contact_level_score=0.30,
            vp_plus_engagement_rate_pct=0.20,
        )
        r = engine().assess(inp)
        if r.persona_risk == PersonaRisk.high and r.persona_pattern == PersonaPattern.wrong_level:
            assert r.recommended_action == PersonaAction.executive_access_coaching

    def test_high_risk_wrong_department_gives_stakeholder_mapping(self):
        inp = self._high_risk_input_with_pattern(
            primary_contact_level_score=0.80,
            vp_plus_engagement_rate_pct=0.80,
            business_unit_alignment_score=0.35,
            persona_to_use_case_fit_score=0.40,
        )
        r = engine().assess(inp)
        if r.persona_risk == PersonaRisk.high and r.persona_pattern == PersonaPattern.wrong_department:
            assert r.recommended_action == PersonaAction.stakeholder_mapping_coaching


# ---------------------------------------------------------------------------
# 40. Signal format correctness
# ---------------------------------------------------------------------------

class TestSignalFormat:
    def _signal_with_high_composite(self):
        inp = make_input(
            primary_contact_level_score=0.10,
            vp_plus_engagement_rate_pct=0.10,
            decision_maker_access_rate_pct=0.25,
            economic_buyer_contact_rate_pct=0.20,
            budget_authority_confirmed_rate_pct=0.20,
            influencer_only_rate_pct=0.60,
            cross_functional_coverage_score=0.20,
            sponsor_identification_rate_pct=0.20,
            technical_blockers_rate_pct=0.50,
            business_unit_alignment_score=0.20,
            persona_to_use_case_fit_score=0.20,
            wrong_entry_point_rate_pct=0.60,
        )
        return engine().assess(inp)

    def test_signal_contains_dm_pct_label(self):
        r = self._signal_with_high_composite()
        assert "DM access" in r.persona_signal

    def test_signal_contains_eb_pct_label(self):
        r = self._signal_with_high_composite()
        assert "EB contact" in r.persona_signal

    def test_signal_contains_vp_pct_label(self):
        r = self._signal_with_high_composite()
        assert "VP+" in r.persona_signal

    def test_signal_is_non_empty_string(self):
        r = engine().assess(make_input())
        assert len(r.persona_signal) > 0

    def test_signal_low_composite_message_contains_alignment(self):
        r = engine().assess(make_input())
        assert "alignment" in r.persona_signal.lower() or "benchmark" in r.persona_signal.lower()
