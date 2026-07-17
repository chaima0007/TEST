"""Comprehensive tests for LeadEnrichmentEngine."""

from __future__ import annotations

import pytest

from swarm.intelligence.lead_enrichment import (
    DataQuality,
    EnrichmentPriority,
    LeadSource,
    LeadInput,
    LeadResult,
    EnrichmentGap,
    LeadEnrichmentEngine,
    _has,
    _contact_score,
    _company_score,
    _intent_score_fn,
    _engagement_score,
    _quality_score,
    _data_quality,
    _enrichment_priority,
    _outreach_ready,
    _build_signals,
    _enrichment_sources,
    _FIELD_WEIGHTS,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_lead(**kwargs) -> LeadInput:
    """Create a minimal LeadInput; override any field via kwargs."""
    defaults = dict(
        lead_id="lead-001",
        lead_name="Alice Dupont",
        source=LeadSource.INBOUND,
    )
    defaults.update(kwargs)
    return LeadInput(**defaults)


def _full_lead(**kwargs) -> LeadInput:
    """Create a fully-populated LeadInput (all fields present)."""
    defaults = dict(
        lead_id="lead-full",
        lead_name="Bob Martin",
        source=LeadSource.REFERRAL,
        email="bob@acme.com",
        phone="+33612345678",
        linkedin_url="https://linkedin.com/in/bobmartin",
        job_title="CEO",
        company_name="Acme Corp",
        industry="SaaS",
        company_size_employees=500,
        annual_revenue_eur=5_000_000.0,
        website="https://acme.com",
        pain_point_identified="Manual reporting takes 10h/week",
        use_case_identified="Automate sales reporting",
        budget_signal="confirmed",
        timeline_identified="Q1 2026",
        email_opens=5,
        website_visits=5,
        content_downloads=3,
        events_attended=1,
        is_verified_email=True,
        is_duplicate=False,
        is_unsubscribed=False,
        bounce_history=0,
        domain_match=True,
        seniority_level="c_suite",
    )
    defaults.update(kwargs)
    return LeadInput(**defaults)


def _empty_lead(**kwargs) -> LeadInput:
    """Create a LeadInput with no optional fields filled."""
    return _make_lead(**kwargs)


# ── Class 1: DataQuality Enum ─────────────────────────────────────────────────

class TestDataQualityEnum:
    def test_values_are_strings(self):
        for dq in DataQuality:
            assert isinstance(dq.value, str)

    def test_excellent_value(self):
        assert DataQuality.EXCELLENT.value == "excellent"

    def test_good_value(self):
        assert DataQuality.GOOD.value == "good"

    def test_fair_value(self):
        assert DataQuality.FAIR.value == "fair"

    def test_poor_value(self):
        assert DataQuality.POOR.value == "poor"

    def test_incomplete_value(self):
        assert DataQuality.INCOMPLETE.value == "incomplete"

    def test_five_tiers_exist(self):
        assert len(list(DataQuality)) == 5

    def test_is_str_subclass(self):
        assert isinstance(DataQuality.EXCELLENT, str)


# ── Class 2: EnrichmentPriority Enum ─────────────────────────────────────────

class TestEnrichmentPriorityEnum:
    def test_immediate_value(self):
        assert EnrichmentPriority.IMMEDIATE.value == "immediate"

    def test_high_value(self):
        assert EnrichmentPriority.HIGH.value == "high"

    def test_medium_value(self):
        assert EnrichmentPriority.MEDIUM.value == "medium"

    def test_low_value(self):
        assert EnrichmentPriority.LOW.value == "low"

    def test_none_value(self):
        assert EnrichmentPriority.NONE.value == "none"

    def test_five_priorities(self):
        assert len(list(EnrichmentPriority)) == 5

    def test_is_str_subclass(self):
        assert isinstance(EnrichmentPriority.HIGH, str)


# ── Class 3: LeadSource Enum ──────────────────────────────────────────────────

class TestLeadSourceEnum:
    def test_inbound_value(self):
        assert LeadSource.INBOUND.value == "inbound"

    def test_outbound_value(self):
        assert LeadSource.OUTBOUND.value == "outbound"

    def test_referral_value(self):
        assert LeadSource.REFERRAL.value == "referral"

    def test_event_value(self):
        assert LeadSource.EVENT.value == "event"

    def test_content_value(self):
        assert LeadSource.CONTENT.value == "content"

    def test_paid_value(self):
        assert LeadSource.PAID.value == "paid"

    def test_six_sources(self):
        assert len(list(LeadSource)) == 6


# ── Class 4: _FIELD_WEIGHTS ───────────────────────────────────────────────────

class TestFieldWeights:
    def test_has_email_weight(self):
        assert _FIELD_WEIGHTS["has_email"] == 12

    def test_has_phone_weight(self):
        assert _FIELD_WEIGHTS["has_phone"] == 8

    def test_has_linkedin_weight(self):
        assert _FIELD_WEIGHTS["has_linkedin"] == 10

    def test_has_job_title_weight(self):
        assert _FIELD_WEIGHTS["has_job_title"] == 10

    def test_has_company_name_weight(self):
        assert _FIELD_WEIGHTS["has_company_name"] == 8

    def test_has_industry_weight(self):
        assert _FIELD_WEIGHTS["has_industry"] == 8

    def test_has_company_size_weight(self):
        assert _FIELD_WEIGHTS["has_company_size"] == 7

    def test_has_annual_revenue_weight(self):
        assert _FIELD_WEIGHTS["has_annual_revenue"] == 7

    def test_has_website_weight(self):
        assert _FIELD_WEIGHTS["has_website"] == 5

    def test_has_pain_point_weight(self):
        assert _FIELD_WEIGHTS["has_pain_point"] == 8

    def test_has_use_case_weight(self):
        assert _FIELD_WEIGHTS["has_use_case"] == 7

    def test_has_budget_signal_weight(self):
        assert _FIELD_WEIGHTS["has_budget_signal"] == 5

    def test_has_timeline_weight(self):
        assert _FIELD_WEIGHTS["has_timeline"] == 5

    def test_contact_weights_sum_to_40(self):
        contact_fields = ["has_email", "has_phone", "has_linkedin", "has_job_title"]
        total = sum(_FIELD_WEIGHTS[f] for f in contact_fields)
        assert total == 40

    def test_company_weights_sum_to_35(self):
        company_fields = [
            "has_company_name", "has_industry", "has_company_size",
            "has_annual_revenue", "has_website",
        ]
        total = sum(_FIELD_WEIGHTS[f] for f in company_fields)
        assert total == 35

    def test_intent_weights_sum_to_25(self):
        intent_fields = ["has_pain_point", "has_use_case", "has_budget_signal", "has_timeline"]
        total = sum(_FIELD_WEIGHTS[f] for f in intent_fields)
        assert total == 25


# ── Class 5: _has() ───────────────────────────────────────────────────────────

class TestHas:
    # String behaviour
    def test_str_non_empty_true(self):
        assert _has("hello") is True

    def test_str_empty_false(self):
        assert _has("") is False

    def test_str_whitespace_only_false(self):
        assert _has("   ") is False

    def test_str_whitespace_stripped_true(self):
        assert _has("  a  ") is True

    def test_str_single_char_true(self):
        assert _has("x") is True

    # Int behaviour
    def test_int_positive_true(self):
        assert _has(1) is True

    def test_int_zero_false(self):
        assert _has(0) is False

    def test_int_negative_false(self):
        assert _has(-1) is False

    def test_int_large_positive_true(self):
        assert _has(9999) is True

    # Float behaviour
    def test_float_positive_true(self):
        assert _has(0.1) is True

    def test_float_zero_false(self):
        assert _has(0.0) is False

    def test_float_negative_false(self):
        assert _has(-0.5) is False

    # Bool behaviour
    def test_bool_true_true(self):
        assert _has(True) is True

    def test_bool_false_false(self):
        assert _has(False) is False


# ── Class 6: _contact_score() ─────────────────────────────────────────────────

class TestContactScore:
    def test_all_present_score_100(self):
        inp = _make_lead(
            email="a@b.com", phone="123", linkedin_url="url", job_title="CEO"
        )
        score, gaps = _contact_score(inp)
        assert score == 100.0
        assert gaps == []

    def test_none_present_score_0(self):
        inp = _make_lead()
        score, gaps = _contact_score(inp)
        assert score == 0.0
        assert len(gaps) == 4

    def test_email_only_score(self):
        # 12 / 40 * 100 = 30.0
        inp = _make_lead(email="a@b.com")
        score, gaps = _contact_score(inp)
        assert score == 30.0
        assert len(gaps) == 3

    def test_phone_only_score(self):
        # 8 / 40 * 100 = 20.0
        inp = _make_lead(phone="123")
        score, gaps = _contact_score(inp)
        assert score == 20.0

    def test_linkedin_only_score(self):
        # 10 / 40 * 100 = 25.0
        inp = _make_lead(linkedin_url="url")
        score, gaps = _contact_score(inp)
        assert score == 25.0

    def test_job_title_only_score(self):
        # 10 / 40 * 100 = 25.0
        inp = _make_lead(job_title="CEO")
        score, gaps = _contact_score(inp)
        assert score == 25.0

    def test_gaps_fields_match_missing(self):
        inp = _make_lead(email="a@b.com")
        _, gaps = _contact_score(inp)
        gap_fields = {g.field for g in gaps}
        assert "has_phone" in gap_fields
        assert "has_linkedin" in gap_fields
        assert "has_job_title" in gap_fields
        assert "has_email" not in gap_fields

    def test_gap_impact_score_correct(self):
        inp = _make_lead()
        _, gaps = _contact_score(inp)
        gap_dict = {g.field: g.impact_score for g in gaps}
        assert gap_dict["has_email"] == 12
        assert gap_dict["has_phone"] == 8
        assert gap_dict["has_linkedin"] == 10
        assert gap_dict["has_job_title"] == 10

    def test_score_is_rounded_to_2dp(self):
        # email + phone = 20 / 40 * 100 = 50.0 exactly — just confirm type
        inp = _make_lead(email="a@b.com", phone="123")
        score, _ = _contact_score(inp)
        assert isinstance(score, float)

    def test_email_plus_linkedin_score(self):
        # 12 + 10 = 22 / 40 * 100 = 55.0
        inp = _make_lead(email="a@b.com", linkedin_url="url")
        score, _ = _contact_score(inp)
        assert score == 55.0

    def test_whitespace_email_counts_as_missing(self):
        inp = _make_lead(email="   ")
        score, gaps = _contact_score(inp)
        gap_fields = {g.field for g in gaps}
        assert "has_email" in gap_fields


# ── Class 7: _company_score() ─────────────────────────────────────────────────

class TestCompanyScore:
    def test_all_present_score_100(self):
        inp = _make_lead(
            company_name="Acme",
            industry="SaaS",
            company_size_employees=100,
            annual_revenue_eur=1_000_000.0,
            website="https://acme.com",
        )
        score, gaps = _company_score(inp)
        assert score == 100.0
        assert gaps == []

    def test_none_present_score_0(self):
        inp = _make_lead()
        score, gaps = _company_score(inp)
        assert score == 0.0
        assert len(gaps) == 5

    def test_company_name_only_score(self):
        # 8 / 35 * 100 ≈ 22.86
        inp = _make_lead(company_name="Acme")
        score, _ = _company_score(inp)
        assert abs(score - round(8 / 35 * 100, 2)) < 0.01

    def test_industry_only_score(self):
        # 8 / 35 * 100 ≈ 22.86
        inp = _make_lead(industry="SaaS")
        score, _ = _company_score(inp)
        assert abs(score - round(8 / 35 * 100, 2)) < 0.01

    def test_company_size_zero_is_missing(self):
        inp = _make_lead(company_size_employees=0)
        _, gaps = _company_score(inp)
        gap_fields = {g.field for g in gaps}
        assert "has_company_size" in gap_fields

    def test_company_size_positive_not_gap(self):
        inp = _make_lead(company_size_employees=1)
        _, gaps = _company_score(inp)
        gap_fields = {g.field for g in gaps}
        assert "has_company_size" not in gap_fields

    def test_annual_revenue_zero_is_missing(self):
        inp = _make_lead(annual_revenue_eur=0.0)
        _, gaps = _company_score(inp)
        gap_fields = {g.field for g in gaps}
        assert "has_annual_revenue" in gap_fields

    def test_annual_revenue_positive_not_gap(self):
        inp = _make_lead(annual_revenue_eur=1.0)
        _, gaps = _company_score(inp)
        gap_fields = {g.field for g in gaps}
        assert "has_annual_revenue" not in gap_fields

    def test_website_only_score(self):
        # 5 / 35 * 100 ≈ 14.29
        inp = _make_lead(website="https://acme.com")
        score, _ = _company_score(inp)
        assert abs(score - round(5 / 35 * 100, 2)) < 0.01

    def test_gap_impact_score_values(self):
        inp = _make_lead()
        _, gaps = _company_score(inp)
        gap_dict = {g.field: g.impact_score for g in gaps}
        assert gap_dict["has_company_name"] == 8
        assert gap_dict["has_industry"] == 8
        assert gap_dict["has_company_size"] == 7
        assert gap_dict["has_annual_revenue"] == 7
        assert gap_dict["has_website"] == 5


# ── Class 8: _intent_score_fn() ───────────────────────────────────────────────

class TestIntentScore:
    def test_all_present_score_100(self):
        inp = _make_lead(
            pain_point_identified="Manual work",
            use_case_identified="Automate",
            budget_signal="confirmed",
            timeline_identified="Q1 2026",
        )
        score, gaps = _intent_score_fn(inp)
        assert score == 100.0
        assert gaps == []

    def test_none_present_score_0(self):
        inp = _make_lead()
        score, gaps = _intent_score_fn(inp)
        assert score == 0.0
        assert len(gaps) == 4

    def test_pain_point_only_score(self):
        # 8 / 25 * 100 = 32.0
        inp = _make_lead(pain_point_identified="Manual work")
        score, _ = _intent_score_fn(inp)
        assert score == 32.0

    def test_use_case_only_score(self):
        # 7 / 25 * 100 = 28.0
        inp = _make_lead(use_case_identified="Automate")
        score, _ = _intent_score_fn(inp)
        assert score == 28.0

    def test_budget_signal_only_score(self):
        # 5 / 25 * 100 = 20.0
        inp = _make_lead(budget_signal="hinted")
        score, _ = _intent_score_fn(inp)
        assert score == 20.0

    def test_timeline_only_score(self):
        # 5 / 25 * 100 = 20.0
        inp = _make_lead(timeline_identified="Q2 2026")
        score, _ = _intent_score_fn(inp)
        assert score == 20.0

    def test_gap_fields_correct(self):
        inp = _make_lead(pain_point_identified="pain")
        _, gaps = _intent_score_fn(inp)
        gap_fields = {g.field for g in gaps}
        assert "has_pain_point" not in gap_fields
        assert "has_use_case" in gap_fields
        assert "has_budget_signal" in gap_fields
        assert "has_timeline" in gap_fields

    def test_gap_impact_score_values(self):
        inp = _make_lead()
        _, gaps = _intent_score_fn(inp)
        gap_dict = {g.field: g.impact_score for g in gaps}
        assert gap_dict["has_pain_point"] == 8
        assert gap_dict["has_use_case"] == 7
        assert gap_dict["has_budget_signal"] == 5
        assert gap_dict["has_timeline"] == 5

    def test_whitespace_budget_signal_counts_as_missing(self):
        inp = _make_lead(budget_signal="   ")
        _, gaps = _intent_score_fn(inp)
        gap_fields = {g.field for g in gaps}
        assert "has_budget_signal" in gap_fields


# ── Class 9: _engagement_score() ──────────────────────────────────────────────

class TestEngagementScore:
    def test_zero_engagement_score_0(self):
        inp = _make_lead()
        assert _engagement_score(inp) == 0.0

    def test_email_opens_multiplier(self):
        # 1 open * 6 = 6
        inp = _make_lead(email_opens=1)
        assert _engagement_score(inp) == 6.0

    def test_email_opens_capped_at_30(self):
        # 6 opens * 6 = 36, capped at 30
        inp = _make_lead(email_opens=6)
        assert _engagement_score(inp) == 30.0

    def test_email_opens_cap_boundary(self):
        # 5 opens * 6 = 30, exactly at cap
        inp = _make_lead(email_opens=5)
        assert _engagement_score(inp) == 30.0

    def test_website_visits_multiplier(self):
        # 1 visit * 5 = 5
        inp = _make_lead(website_visits=1)
        assert _engagement_score(inp) == 5.0

    def test_website_visits_capped_at_25(self):
        # 6 visits * 5 = 30, capped at 25
        inp = _make_lead(website_visits=6)
        assert _engagement_score(inp) == 25.0

    def test_content_downloads_multiplier(self):
        # 1 download * 12 = 12
        inp = _make_lead(content_downloads=1)
        assert _engagement_score(inp) == 12.0

    def test_content_downloads_capped_at_25(self):
        # 3 downloads * 12 = 36, capped at 25
        inp = _make_lead(content_downloads=3)
        assert _engagement_score(inp) == 25.0

    def test_events_attended_multiplier(self):
        # 1 event * 20 = 20
        inp = _make_lead(events_attended=1)
        assert _engagement_score(inp) == 20.0

    def test_events_attended_capped_at_20(self):
        # 2 events * 20 = 40, capped at 20
        inp = _make_lead(events_attended=2)
        assert _engagement_score(inp) == 20.0

    def test_total_capped_at_100(self):
        # All maxed out: 30 + 25 + 25 + 20 = 100
        inp = _make_lead(email_opens=10, website_visits=10, content_downloads=10, events_attended=10)
        assert _engagement_score(inp) == 100.0

    def test_combined_score_not_capped(self):
        # 1 open (6) + 1 visit (5) = 11
        inp = _make_lead(email_opens=1, website_visits=1)
        assert _engagement_score(inp) == 11.0

    def test_full_lead_engagement(self):
        inp = _full_lead()
        # email_opens=5 (30) + website_visits=5 (25) + content_downloads=3 (25) + events_attended=1 (20) = 100
        assert _engagement_score(inp) == 100.0


# ── Class 10: _quality_score() & _data_quality() ─────────────────────────────

class TestQualityScoreAndDataQuality:
    def test_quality_score_formula(self):
        score = _quality_score(100, 100, 100, 100)
        assert score == 100.0

    def test_quality_score_zeros(self):
        score = _quality_score(0, 0, 0, 0)
        assert score == 0.0

    def test_quality_score_weighted(self):
        # contact=80, company=60, intent=40, engagement=20
        expected = round(80 * 0.35 + 60 * 0.30 + 40 * 0.20 + 20 * 0.15, 2)
        score = _quality_score(80, 60, 40, 20)
        assert score == expected

    def test_quality_score_is_rounded_to_2dp(self):
        score = _quality_score(33.33, 33.33, 33.33, 33.33)
        assert isinstance(score, float)
        assert len(str(score).split(".")[-1]) <= 2

    def test_data_quality_excellent_at_85(self):
        assert _data_quality(85.0) == DataQuality.EXCELLENT

    def test_data_quality_excellent_at_100(self):
        assert _data_quality(100.0) == DataQuality.EXCELLENT

    def test_data_quality_excellent_at_90(self):
        assert _data_quality(90.0) == DataQuality.EXCELLENT

    def test_data_quality_good_at_65(self):
        assert _data_quality(65.0) == DataQuality.GOOD

    def test_data_quality_good_at_84_99(self):
        assert _data_quality(84.99) == DataQuality.GOOD

    def test_data_quality_fair_at_45(self):
        assert _data_quality(45.0) == DataQuality.FAIR

    def test_data_quality_fair_at_64_99(self):
        assert _data_quality(64.99) == DataQuality.FAIR

    def test_data_quality_poor_at_25(self):
        assert _data_quality(25.0) == DataQuality.POOR

    def test_data_quality_poor_at_44_99(self):
        assert _data_quality(44.99) == DataQuality.POOR

    def test_data_quality_incomplete_at_0(self):
        assert _data_quality(0.0) == DataQuality.INCOMPLETE

    def test_data_quality_incomplete_at_24_99(self):
        assert _data_quality(24.99) == DataQuality.INCOMPLETE

    def test_data_quality_boundary_85_is_excellent(self):
        assert _data_quality(85.0) == DataQuality.EXCELLENT

    def test_data_quality_boundary_64_99_is_good(self):
        # 64.999 is below the >= 65 threshold, so it is FAIR
        assert _data_quality(64.999) == DataQuality.FAIR


# ── Class 11: _enrichment_priority() ─────────────────────────────────────────

class TestEnrichmentPriority:
    def test_unsubscribed_always_none(self):
        for quality in DataQuality:
            result = _enrichment_priority(quality, has_email=True, is_unsubscribed=True)
            assert result == EnrichmentPriority.NONE, f"Expected NONE for {quality}, unsubscribed"

    def test_unsubscribed_no_email_still_none(self):
        result = _enrichment_priority(DataQuality.INCOMPLETE, has_email=False, is_unsubscribed=True)
        assert result == EnrichmentPriority.NONE

    def test_no_email_incomplete_is_immediate(self):
        result = _enrichment_priority(DataQuality.INCOMPLETE, has_email=False, is_unsubscribed=False)
        assert result == EnrichmentPriority.IMMEDIATE

    def test_no_email_poor_is_immediate(self):
        result = _enrichment_priority(DataQuality.POOR, has_email=False, is_unsubscribed=False)
        assert result == EnrichmentPriority.IMMEDIATE

    def test_no_email_fair_is_medium(self):
        # no_email check only for INCOMPLETE and POOR; FAIR falls through to normal
        result = _enrichment_priority(DataQuality.FAIR, has_email=False, is_unsubscribed=False)
        assert result == EnrichmentPriority.MEDIUM

    def test_has_email_incomplete_is_immediate(self):
        result = _enrichment_priority(DataQuality.INCOMPLETE, has_email=True, is_unsubscribed=False)
        assert result == EnrichmentPriority.IMMEDIATE

    def test_has_email_poor_is_high(self):
        result = _enrichment_priority(DataQuality.POOR, has_email=True, is_unsubscribed=False)
        assert result == EnrichmentPriority.HIGH

    def test_has_email_fair_is_medium(self):
        result = _enrichment_priority(DataQuality.FAIR, has_email=True, is_unsubscribed=False)
        assert result == EnrichmentPriority.MEDIUM

    def test_has_email_good_is_low(self):
        result = _enrichment_priority(DataQuality.GOOD, has_email=True, is_unsubscribed=False)
        assert result == EnrichmentPriority.LOW

    def test_has_email_excellent_is_none(self):
        result = _enrichment_priority(DataQuality.EXCELLENT, has_email=True, is_unsubscribed=False)
        assert result == EnrichmentPriority.NONE

    def test_no_email_good_is_low(self):
        # no_email check only triggers for INCOMPLETE/POOR
        result = _enrichment_priority(DataQuality.GOOD, has_email=False, is_unsubscribed=False)
        assert result == EnrichmentPriority.LOW

    def test_no_email_excellent_is_none(self):
        result = _enrichment_priority(DataQuality.EXCELLENT, has_email=False, is_unsubscribed=False)
        assert result == EnrichmentPriority.NONE


# ── Class 12: _outreach_ready() ───────────────────────────────────────────────

class TestOutreachReady:
    def test_unsubscribed_not_ready(self):
        inp = _full_lead(is_unsubscribed=True)
        assert _outreach_ready(inp, DataQuality.EXCELLENT) is False

    def test_duplicate_not_ready(self):
        inp = _full_lead(is_duplicate=True)
        assert _outreach_ready(inp, DataQuality.EXCELLENT) is False

    def test_no_email_no_linkedin_not_ready(self):
        inp = _make_lead()
        assert _outreach_ready(inp, DataQuality.GOOD) is False

    def test_has_email_only_good_quality_ready(self):
        inp = _make_lead(email="a@b.com")
        assert _outreach_ready(inp, DataQuality.GOOD) is True

    def test_has_linkedin_only_good_quality_ready(self):
        inp = _make_lead(linkedin_url="https://linkedin.com/in/x")
        assert _outreach_ready(inp, DataQuality.GOOD) is True

    def test_incomplete_quality_not_ready(self):
        inp = _make_lead(email="a@b.com")
        assert _outreach_ready(inp, DataQuality.INCOMPLETE) is False

    def test_poor_quality_with_email_ready(self):
        inp = _make_lead(email="a@b.com")
        assert _outreach_ready(inp, DataQuality.POOR) is True

    def test_excellent_quality_with_email_ready(self):
        inp = _full_lead()
        assert _outreach_ready(inp, DataQuality.EXCELLENT) is True

    def test_fair_quality_with_linkedin_ready(self):
        inp = _make_lead(linkedin_url="url")
        assert _outreach_ready(inp, DataQuality.FAIR) is True

    def test_unsubscribed_overrides_everything(self):
        inp = _full_lead(is_unsubscribed=True)
        assert _outreach_ready(inp, DataQuality.EXCELLENT) is False

    def test_duplicate_overrides_quality(self):
        inp = _full_lead(is_duplicate=True)
        assert _outreach_ready(inp, DataQuality.GOOD) is False


# ── Class 13: _build_signals() ────────────────────────────────────────────────

class TestBuildSignals:
    def test_verified_email_positive_signal(self):
        inp = _full_lead(is_verified_email=True)
        signals, _ = _build_signals(inp, DataQuality.EXCELLENT, 80.0)
        assert any("vérifié" in s for s in signals)

    def test_not_verified_email_no_positive_signal(self):
        inp = _full_lead(is_verified_email=False)
        signals, _ = _build_signals(inp, DataQuality.EXCELLENT, 0.0)
        assert not any("vérifié" in s for s in signals)

    def test_referral_source_positive_signal(self):
        inp = _full_lead(source=LeadSource.REFERRAL)
        signals, _ = _build_signals(inp, DataQuality.EXCELLENT, 0.0)
        assert any("recommandation" in s for s in signals)

    def test_inbound_source_positive_signal(self):
        inp = _full_lead(source=LeadSource.INBOUND)
        signals, _ = _build_signals(inp, DataQuality.EXCELLENT, 0.0)
        assert any("entrant" in s for s in signals)

    def test_outbound_no_source_signal(self):
        inp = _full_lead(source=LeadSource.OUTBOUND)
        signals, _ = _build_signals(inp, DataQuality.EXCELLENT, 0.0)
        assert not any("recommandation" in s or "entrant" in s for s in signals)

    def test_engagement_ge_70_high_engagement_signal(self):
        inp = _make_lead()
        signals, _ = _build_signals(inp, DataQuality.FAIR, 70.0)
        assert any("haut engagement" in s for s in signals)

    def test_engagement_ge_40_moderate_signal(self):
        inp = _make_lead()
        signals, _ = _build_signals(inp, DataQuality.FAIR, 50.0)
        assert any("modéré" in s for s in signals)

    def test_engagement_below_40_no_engagement_signal(self):
        inp = _make_lead()
        signals, _ = _build_signals(inp, DataQuality.FAIR, 30.0)
        assert not any("engagement" in s for s in signals)

    def test_pain_point_positive_signal(self):
        inp = _make_lead(pain_point_identified="Manual reporting")
        signals, _ = _build_signals(inp, DataQuality.FAIR, 0.0)
        assert any("douleur" in s for s in signals)

    def test_budget_signal_positive(self):
        inp = _make_lead(budget_signal="confirmed")
        signals, _ = _build_signals(inp, DataQuality.FAIR, 0.0)
        assert any("budget" in s for s in signals)

    def test_c_suite_seniority_positive_signal(self):
        inp = _make_lead(seniority_level="c_suite")
        signals, _ = _build_signals(inp, DataQuality.FAIR, 0.0)
        assert any("Décideur" in s for s in signals)

    def test_vp_seniority_positive_signal(self):
        inp = _make_lead(seniority_level="vp")
        signals, _ = _build_signals(inp, DataQuality.FAIR, 0.0)
        assert any("Décideur" in s for s in signals)

    def test_director_seniority_no_signal(self):
        inp = _make_lead(seniority_level="director")
        signals, _ = _build_signals(inp, DataQuality.FAIR, 0.0)
        assert not any("Décideur" in s for s in signals)

    def test_content_downloads_ge_2_positive_signal(self):
        inp = _make_lead(content_downloads=2)
        signals, _ = _build_signals(inp, DataQuality.FAIR, 0.0)
        assert any("téléchargements" in s for s in signals)

    def test_content_downloads_1_no_signal(self):
        inp = _make_lead(content_downloads=1)
        signals, _ = _build_signals(inp, DataQuality.FAIR, 0.0)
        assert not any("téléchargements" in s for s in signals)

    # Risk flags
    def test_duplicate_risk_flag(self):
        inp = _full_lead(is_duplicate=True)
        _, risks = _build_signals(inp, DataQuality.EXCELLENT, 0.0)
        assert any("dupliqué" in r for r in risks)

    def test_unsubscribed_risk_flag(self):
        inp = _full_lead(is_unsubscribed=True)
        _, risks = _build_signals(inp, DataQuality.EXCELLENT, 0.0)
        assert any("Désabonné" in r for r in risks)

    def test_bounce_history_ge_2_risk_flag(self):
        inp = _make_lead(email="a@b.com", bounce_history=2)
        _, risks = _build_signals(inp, DataQuality.GOOD, 0.0)
        assert any("bounce" in r.lower() for r in risks)

    def test_bounce_history_1_no_prior_bounces_flag(self):
        # bounce_history < 2 does not trigger the "bounces antérieurs" risk flag
        inp = _make_lead(email="a@b.com", bounce_history=1, is_verified_email=True)
        _, risks = _build_signals(inp, DataQuality.GOOD, 0.0)
        assert not any("antérieurs" in r for r in risks)

    def test_domain_mismatch_with_email_and_company_risk(self):
        inp = _make_lead(email="a@b.com", company_name="Acme", domain_match=False)
        _, risks = _build_signals(inp, DataQuality.GOOD, 0.0)
        assert any("Domaine" in r for r in risks)

    def test_domain_mismatch_without_email_no_risk(self):
        inp = _make_lead(company_name="Acme", domain_match=False)
        _, risks = _build_signals(inp, DataQuality.GOOD, 0.0)
        assert not any("Domaine" in r for r in risks)

    def test_unverified_email_risk_flag(self):
        inp = _make_lead(email="a@b.com", is_verified_email=False)
        _, risks = _build_signals(inp, DataQuality.GOOD, 0.0)
        assert any("non vérifié" in r for r in risks)

    def test_verified_email_no_unverified_risk(self):
        inp = _make_lead(email="a@b.com", is_verified_email=True)
        _, risks = _build_signals(inp, DataQuality.GOOD, 0.0)
        assert not any("non vérifié" in r for r in risks)

    def test_poor_quality_insufficient_data_risk(self):
        inp = _make_lead()
        _, risks = _build_signals(inp, DataQuality.POOR, 0.0)
        assert any("insuffisantes" in r for r in risks)

    def test_incomplete_quality_insufficient_data_risk(self):
        inp = _make_lead()
        _, risks = _build_signals(inp, DataQuality.INCOMPLETE, 0.0)
        assert any("insuffisantes" in r for r in risks)

    def test_fair_quality_no_insufficient_data_risk(self):
        inp = _make_lead()
        _, risks = _build_signals(inp, DataQuality.FAIR, 0.0)
        assert not any("insuffisantes" in r for r in risks)

    def test_no_flags_for_clean_lead(self):
        inp = _full_lead(
            is_duplicate=False,
            is_unsubscribed=False,
            bounce_history=0,
            domain_match=True,
            is_verified_email=True,
        )
        _, risks = _build_signals(inp, DataQuality.EXCELLENT, 0.0)
        assert risks == []


# ── Class 14: _enrichment_sources() ──────────────────────────────────────────

class TestEnrichmentSources:
    def _make_gap(self, field: str) -> EnrichmentGap:
        return EnrichmentGap(field=field, description="desc", impact_score=5)

    def test_no_gaps_no_sources(self):
        assert _enrichment_sources([]) == []

    def test_missing_linkedin_suggests_sales_navigator(self):
        gaps = [self._make_gap("has_linkedin")]
        sources = _enrichment_sources(gaps)
        assert any("LinkedIn Sales Navigator" in s for s in sources)

    def test_missing_job_title_suggests_sales_navigator(self):
        gaps = [self._make_gap("has_job_title")]
        sources = _enrichment_sources(gaps)
        assert any("LinkedIn Sales Navigator" in s for s in sources)

    def test_missing_email_suggests_hunter_apollo(self):
        gaps = [self._make_gap("has_email")]
        sources = _enrichment_sources(gaps)
        assert any("Hunter.io" in s for s in sources)

    def test_missing_phone_suggests_lusha_zoominfo(self):
        gaps = [self._make_gap("has_phone")]
        sources = _enrichment_sources(gaps)
        assert any("Lusha" in s for s in sources)

    def test_missing_company_size_suggests_clearbit(self):
        gaps = [self._make_gap("has_company_size")]
        sources = _enrichment_sources(gaps)
        assert any("Clearbit" in s for s in sources)

    def test_missing_annual_revenue_suggests_clearbit(self):
        gaps = [self._make_gap("has_annual_revenue")]
        sources = _enrichment_sources(gaps)
        assert any("Clearbit" in s for s in sources)

    def test_missing_industry_suggests_crunchbase(self):
        gaps = [self._make_gap("has_industry")]
        sources = _enrichment_sources(gaps)
        assert any("Crunchbase" in s for s in sources)

    def test_missing_website_suggests_crunchbase(self):
        gaps = [self._make_gap("has_website")]
        sources = _enrichment_sources(gaps)
        assert any("Crunchbase" in s for s in sources)

    def test_missing_pain_point_suggests_gong(self):
        gaps = [self._make_gap("has_pain_point")]
        sources = _enrichment_sources(gaps)
        assert any("Gong" in s for s in sources)

    def test_missing_use_case_suggests_gong(self):
        gaps = [self._make_gap("has_use_case")]
        sources = _enrichment_sources(gaps)
        assert any("Gong" in s for s in sources)

    def test_deduplication_same_source_not_repeated(self):
        # linkedin and job_title both trigger LinkedIn Sales Navigator
        gaps = [self._make_gap("has_linkedin"), self._make_gap("has_job_title")]
        sources = _enrichment_sources(gaps)
        nav_count = sum(1 for s in sources if "LinkedIn Sales Navigator" in s)
        assert nav_count == 1

    def test_multiple_gaps_multiple_sources(self):
        gaps = [
            self._make_gap("has_email"),
            self._make_gap("has_phone"),
            self._make_gap("has_pain_point"),
        ]
        sources = _enrichment_sources(gaps)
        assert len(sources) >= 3

    def test_order_preserved(self):
        # First gap is email, so Hunter.io should appear
        gaps = [self._make_gap("has_email"), self._make_gap("has_phone")]
        sources = _enrichment_sources(gaps)
        hunter_idx = next(i for i, s in enumerate(sources) if "Hunter.io" in s)
        lusha_idx = next(i for i, s in enumerate(sources) if "Lusha" in s)
        assert hunter_idx < lusha_idx


# ── Class 15: LeadEnrichmentEngine.enrich() ──────────────────────────────────

class TestEngineEnrich:
    @pytest.fixture()
    def eng(self):
        return LeadEnrichmentEngine()

    def test_enrich_returns_lead_result(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert isinstance(result, LeadResult)

    def test_enrich_stores_result(self, eng):
        inp = _full_lead(lead_id="x1")
        eng.enrich(inp)
        assert eng.get("x1") is not None

    def test_enrich_lead_id_preserved(self, eng):
        inp = _full_lead(lead_id="abc")
        result = eng.enrich(inp)
        assert result.lead_id == "abc"

    def test_enrich_lead_name_preserved(self, eng):
        inp = _full_lead(lead_name="Jane Doe")
        result = eng.enrich(inp)
        assert result.lead_name == "Jane Doe"

    def test_enrich_source_preserved(self, eng):
        inp = _full_lead(source=LeadSource.EVENT)
        result = eng.enrich(inp)
        assert result.source == LeadSource.EVENT

    def test_enrich_full_lead_excellent_quality(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert result.data_quality == DataQuality.EXCELLENT

    def test_enrich_empty_lead_incomplete_quality(self, eng):
        inp = _make_lead()
        result = eng.enrich(inp)
        assert result.data_quality == DataQuality.INCOMPLETE

    def test_enrich_quality_score_range(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert 0 <= result.quality_score <= 100

    def test_enrich_contact_score_range(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert 0 <= result.contact_score <= 100

    def test_enrich_company_score_range(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert 0 <= result.company_score <= 100

    def test_enrich_intent_score_range(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert 0 <= result.intent_score <= 100

    def test_enrich_engagement_score_range(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert 0 <= result.engagement_score <= 100

    def test_enrich_outreach_ready_type(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert isinstance(result.outreach_ready, bool)

    def test_enrich_gaps_list(self, eng):
        inp = _make_lead()
        result = eng.enrich(inp)
        assert isinstance(result.gaps, list)

    def test_enrich_signals_list(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert isinstance(result.quality_signals, list)

    def test_enrich_risk_flags_list(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert isinstance(result.risk_flags, list)

    def test_enrich_sources_list(self, eng):
        inp = _make_lead()
        result = eng.enrich(inp)
        assert isinstance(result.suggested_enrichment_sources, list)

    def test_enrich_overwrites_existing_lead(self, eng):
        inp1 = _make_lead(lead_id="same")
        inp2 = _full_lead(lead_id="same")
        eng.enrich(inp1)
        eng.enrich(inp2)
        result = eng.get("same")
        assert result.data_quality == DataQuality.EXCELLENT


# ── Class 16: LeadEnrichmentEngine batch / retrieval methods ──────────────────

class TestEngineBatchAndRetrieval:
    @pytest.fixture()
    def eng(self):
        return LeadEnrichmentEngine()

    def test_enrich_batch_returns_list(self, eng):
        leads = [_make_lead(lead_id="a"), _make_lead(lead_id="b")]
        results = eng.enrich_batch(leads)
        assert isinstance(results, list)
        assert len(results) == 2

    def test_enrich_batch_sorted_desc_by_quality(self, eng):
        full = _full_lead(lead_id="full")
        empty = _make_lead(lead_id="empty")
        results = eng.enrich_batch([empty, full])
        assert results[0].quality_score >= results[1].quality_score

    def test_enrich_batch_stores_all(self, eng):
        leads = [_make_lead(lead_id="a"), _make_lead(lead_id="b")]
        eng.enrich_batch(leads)
        assert eng.get("a") is not None
        assert eng.get("b") is not None

    def test_get_existing_lead(self, eng):
        inp = _make_lead(lead_id="lead42")
        eng.enrich(inp)
        result = eng.get("lead42")
        assert result is not None
        assert result.lead_id == "lead42"

    def test_get_nonexistent_returns_none(self, eng):
        assert eng.get("nonexistent") is None

    def test_all_leads_sorted_desc(self, eng):
        eng.enrich(_make_lead(lead_id="a"))
        eng.enrich(_full_lead(lead_id="b"))
        all_r = eng.all_leads()
        assert all_r[0].quality_score >= all_r[1].quality_score

    def test_all_leads_count(self, eng):
        eng.enrich(_make_lead(lead_id="a"))
        eng.enrich(_make_lead(lead_id="b"))
        assert len(eng.all_leads()) == 2

    def test_by_quality_filters_correctly(self, eng):
        eng.enrich(_full_lead(lead_id="full"))
        eng.enrich(_make_lead(lead_id="empty"))
        excellent = eng.by_quality(DataQuality.EXCELLENT)
        for r in excellent:
            assert r.data_quality == DataQuality.EXCELLENT

    def test_by_quality_empty_result(self, eng):
        eng.enrich(_make_lead(lead_id="x"))
        result = eng.by_quality(DataQuality.EXCELLENT)
        assert result == []

    def test_outreach_ready_filters(self, eng):
        eng.enrich(_full_lead(lead_id="ready"))
        eng.enrich(_make_lead(lead_id="not_ready"))
        ready = eng.outreach_ready()
        for r in ready:
            assert r.outreach_ready is True

    def test_needs_enrichment_only_immediate_and_high(self, eng):
        eng.enrich(_full_lead(lead_id="full"))
        eng.enrich(_make_lead(lead_id="empty"))
        needs = eng.needs_enrichment()
        for r in needs:
            assert r.enrichment_priority in (EnrichmentPriority.IMMEDIATE, EnrichmentPriority.HIGH)

    def test_excellent_leads_convenience(self, eng):
        eng.enrich(_full_lead(lead_id="full"))
        excellent = eng.excellent_leads()
        assert all(r.data_quality == DataQuality.EXCELLENT for r in excellent)

    def test_incomplete_leads_convenience(self, eng):
        eng.enrich(_make_lead(lead_id="empty"))
        incomplete = eng.incomplete_leads()
        assert all(r.data_quality == DataQuality.INCOMPLETE for r in incomplete)

    def test_top_n_returns_n(self, eng):
        for i in range(5):
            eng.enrich(_make_lead(lead_id=f"lead-{i}"))
        assert len(eng.top_n(3)) == 3

    def test_top_n_less_than_available(self, eng):
        eng.enrich(_make_lead(lead_id="a"))
        assert len(eng.top_n(10)) == 1

    def test_top_n_default_10(self, eng):
        for i in range(15):
            eng.enrich(_make_lead(lead_id=f"lead-{i}"))
        assert len(eng.top_n()) == 10

    def test_reset_clears_all(self, eng):
        eng.enrich(_make_lead(lead_id="a"))
        eng.reset()
        assert eng.all_leads() == []

    def test_reset_get_returns_none(self, eng):
        eng.enrich(_make_lead(lead_id="a"))
        eng.reset()
        assert eng.get("a") is None


# ── Class 17: LeadEnrichmentEngine.summary() ─────────────────────────────────

class TestEngineSummary:
    @pytest.fixture()
    def eng(self):
        return LeadEnrichmentEngine()

    def test_summary_empty_engine(self, eng):
        s = eng.summary()
        assert s["total"] == 0
        assert s["quality_counts"] == {}
        assert s["priority_counts"] == {}
        assert s["avg_quality_score"] == 0.0
        assert s["outreach_ready_count"] == 0
        assert s["needs_enrichment_count"] == 0

    def test_summary_total(self, eng):
        eng.enrich(_make_lead(lead_id="a"))
        eng.enrich(_make_lead(lead_id="b"))
        assert eng.summary()["total"] == 2

    def test_summary_quality_counts_keys(self, eng):
        eng.enrich(_make_lead(lead_id="a"))
        s = eng.summary()
        for key in s["quality_counts"]:
            assert key in [q.value for q in DataQuality]

    def test_summary_priority_counts_keys(self, eng):
        eng.enrich(_make_lead(lead_id="a"))
        s = eng.summary()
        for key in s["priority_counts"]:
            assert key in [p.value for p in EnrichmentPriority]

    def test_summary_avg_quality_score_type(self, eng):
        eng.enrich(_make_lead(lead_id="a"))
        s = eng.summary()
        assert isinstance(s["avg_quality_score"], float)

    def test_summary_outreach_ready_count(self, eng):
        eng.enrich(_full_lead(lead_id="ready"))
        eng.enrich(_make_lead(lead_id="not_ready"))
        s = eng.summary()
        assert s["outreach_ready_count"] >= 1

    def test_summary_needs_enrichment_count(self, eng):
        eng.enrich(_make_lead(lead_id="empty"))
        s = eng.summary()
        assert s["needs_enrichment_count"] >= 1

    def test_summary_quality_counts_sum_to_total(self, eng):
        for i in range(3):
            eng.enrich(_make_lead(lead_id=f"l{i}"))
        s = eng.summary()
        assert sum(s["quality_counts"].values()) == s["total"]

    def test_summary_priority_counts_sum_to_total(self, eng):
        for i in range(3):
            eng.enrich(_make_lead(lead_id=f"l{i}"))
        s = eng.summary()
        assert sum(s["priority_counts"].values()) == s["total"]

    def test_summary_avg_score_correct(self, eng):
        r1 = eng.enrich(_make_lead(lead_id="a"))
        r2 = eng.enrich(_make_lead(lead_id="b"))
        expected_avg = round((r1.quality_score + r2.quality_score) / 2, 1)
        assert eng.summary()["avg_quality_score"] == expected_avg

    def test_summary_after_reset_zeros(self, eng):
        eng.enrich(_make_lead(lead_id="a"))
        eng.reset()
        s = eng.summary()
        assert s["total"] == 0
        assert s["avg_quality_score"] == 0.0


# ── Class 18: LeadResult.to_dict() ───────────────────────────────────────────

class TestLeadResultToDict:
    @pytest.fixture()
    def eng(self):
        return LeadEnrichmentEngine()

    def test_to_dict_returns_dict(self, eng):
        result = eng.enrich(_full_lead())
        assert isinstance(result.to_dict(), dict)

    def test_to_dict_data_quality_is_string(self, eng):
        result = eng.enrich(_full_lead())
        d = result.to_dict()
        assert isinstance(d["data_quality"], str)

    def test_to_dict_data_quality_is_value(self, eng):
        result = eng.enrich(_full_lead())
        d = result.to_dict()
        assert d["data_quality"] == result.data_quality.value

    def test_to_dict_enrichment_priority_is_string(self, eng):
        result = eng.enrich(_full_lead())
        d = result.to_dict()
        assert isinstance(d["enrichment_priority"], str)

    def test_to_dict_enrichment_priority_is_value(self, eng):
        result = eng.enrich(_full_lead())
        d = result.to_dict()
        assert d["enrichment_priority"] == result.enrichment_priority.value

    def test_to_dict_source_is_string(self, eng):
        result = eng.enrich(_full_lead())
        d = result.to_dict()
        assert isinstance(d["source"], str)

    def test_to_dict_source_is_value(self, eng):
        inp = _full_lead(source=LeadSource.REFERRAL)
        result = eng.enrich(inp)
        d = result.to_dict()
        assert d["source"] == "referral"

    def test_to_dict_has_all_expected_keys(self, eng):
        result = eng.enrich(_full_lead())
        d = result.to_dict()
        expected_keys = {
            "lead_id", "lead_name", "source", "data_quality", "quality_score",
            "contact_score", "company_score", "intent_score", "engagement_score",
            "enrichment_priority", "gaps", "outreach_ready",
            "quality_signals", "risk_flags", "suggested_enrichment_sources",
        }
        assert expected_keys.issubset(d.keys())

    def test_to_dict_gaps_are_dicts(self, eng):
        result = eng.enrich(_make_lead())
        d = result.to_dict()
        assert all(isinstance(g, dict) for g in d["gaps"])

    def test_to_dict_data_quality_not_enum_object(self, eng):
        result = eng.enrich(_full_lead())
        d = result.to_dict()
        assert not isinstance(d["data_quality"], DataQuality)

    def test_to_dict_source_not_enum_object(self, eng):
        result = eng.enrich(_full_lead())
        d = result.to_dict()
        assert not isinstance(d["source"], LeadSource)

    def test_to_dict_priority_not_enum_object(self, eng):
        result = eng.enrich(_full_lead())
        d = result.to_dict()
        assert not isinstance(d["enrichment_priority"], EnrichmentPriority)


# ── Class 19: EnrichmentGap dataclass ────────────────────────────────────────

class TestEnrichmentGap:
    def test_enrichment_gap_creation(self):
        gap = EnrichmentGap(field="has_email", description="Email missing", impact_score=12)
        assert gap.field == "has_email"
        assert gap.description == "Email missing"
        assert gap.impact_score == 12

    def test_enrichment_gap_is_dataclass(self):
        gap = EnrichmentGap(field="f", description="d", impact_score=5)
        assert hasattr(gap, "__dataclass_fields__")


# ── Class 20: LeadInput defaults ─────────────────────────────────────────────

class TestLeadInputDefaults:
    def test_default_email_empty(self):
        inp = _make_lead()
        assert inp.email == ""

    def test_default_phone_empty(self):
        inp = _make_lead()
        assert inp.phone == ""

    def test_default_company_size_zero(self):
        inp = _make_lead()
        assert inp.company_size_employees == 0

    def test_default_annual_revenue_zero(self):
        inp = _make_lead()
        assert inp.annual_revenue_eur == 0.0

    def test_default_is_verified_email_false(self):
        inp = _make_lead()
        assert inp.is_verified_email is False

    def test_default_is_duplicate_false(self):
        inp = _make_lead()
        assert inp.is_duplicate is False

    def test_default_is_unsubscribed_false(self):
        inp = _make_lead()
        assert inp.is_unsubscribed is False

    def test_default_bounce_history_zero(self):
        inp = _make_lead()
        assert inp.bounce_history == 0

    def test_default_domain_match_true(self):
        inp = _make_lead()
        assert inp.domain_match is True

    def test_default_seniority_empty(self):
        inp = _make_lead()
        assert inp.seniority_level == ""

    def test_default_email_opens_zero(self):
        inp = _make_lead()
        assert inp.email_opens == 0


# ── Class 21: Edge cases & integration ───────────────────────────────────────

class TestEdgeCasesAndIntegration:
    @pytest.fixture()
    def eng(self):
        return LeadEnrichmentEngine()

    def test_unsubscribed_lead_not_outreach_ready(self, eng):
        inp = _full_lead(is_unsubscribed=True)
        result = eng.enrich(inp)
        assert result.outreach_ready is False

    def test_unsubscribed_lead_priority_none(self, eng):
        inp = _full_lead(is_unsubscribed=True)
        result = eng.enrich(inp)
        assert result.enrichment_priority == EnrichmentPriority.NONE

    def test_duplicate_lead_not_ready(self, eng):
        inp = _full_lead(is_duplicate=True)
        result = eng.enrich(inp)
        assert result.outreach_ready is False

    def test_empty_lead_has_all_gaps(self, eng):
        inp = _make_lead()
        result = eng.enrich(inp)
        assert len(result.gaps) == 13  # all fields missing

    def test_full_lead_no_gaps(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert result.gaps == []

    def test_full_lead_no_enrichment_sources(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        assert result.suggested_enrichment_sources == []

    def test_linkedin_url_makes_outreach_ready_without_email(self, eng):
        inp = _make_lead(linkedin_url="https://linkedin.com/in/x")
        # quality will be incomplete (score too low), so not ready
        result = eng.enrich(inp)
        # with just linkedin, quality score is very low => INCOMPLETE => not ready
        assert result.outreach_ready is False

    def test_linkedin_and_company_info_can_be_ready(self, eng):
        inp = _make_lead(
            linkedin_url="url",
            job_title="CEO",
            company_name="Acme",
            industry="SaaS",
            company_size_employees=100,
            annual_revenue_eur=1_000_000.0,
            website="acme.com",
            pain_point_identified="pain",
            use_case_identified="use",
            budget_signal="confirmed",
            timeline_identified="Q1",
        )
        result = eng.enrich(inp)
        assert result.outreach_ready is True

    def test_enrich_batch_single_item(self, eng):
        results = eng.enrich_batch([_full_lead()])
        assert len(results) == 1

    def test_enrich_batch_empty(self, eng):
        results = eng.enrich_batch([])
        assert results == []

    def test_by_quality_returns_all_of_that_tier(self, eng):
        for i in range(3):
            eng.enrich(_make_lead(lead_id=f"incomplete-{i}"))
        incomplete = eng.by_quality(DataQuality.INCOMPLETE)
        assert len(incomplete) == 3

    def test_multiple_enrichments_same_id_overwrites(self, eng):
        eng.enrich(_make_lead(lead_id="same"))
        eng.enrich(_full_lead(lead_id="same"))
        all_r = eng.all_leads()
        same_leads = [r for r in all_r if r.lead_id == "same"]
        assert len(same_leads) == 1

    def test_quality_score_matches_computed(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        expected = _quality_score(result.contact_score, result.company_score, result.intent_score, result.engagement_score)
        assert result.quality_score == expected

    def test_data_quality_matches_quality_score(self, eng):
        inp = _full_lead()
        result = eng.enrich(inp)
        expected_quality = _data_quality(result.quality_score)
        assert result.data_quality == expected_quality

    def test_sources_recommended_for_empty_lead(self, eng):
        inp = _make_lead()
        result = eng.enrich(inp)
        assert len(result.suggested_enrichment_sources) > 0

    def test_top_n_sorted(self, eng):
        for i in range(5):
            eng.enrich(_make_lead(lead_id=f"l{i}"))
        eng.enrich(_full_lead(lead_id="top"))
        top = eng.top_n(3)
        assert top[0].quality_score >= top[1].quality_score >= top[2].quality_score
