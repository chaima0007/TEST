"""
Comprehensive pytest tests for swarm/intelligence/contact_personalizer.py
"""

from __future__ import annotations

import pytest
from typing import List, Optional

from swarm.intelligence.contact_personalizer import (
    ContactPersonalizer,
    ContactProfile,
    PersonalizationPlan,
    PersonalizationLevel,
    OutreachChannel,
    TriggerType,
    _profile_richness,
    _engagement_signals,
    _timing_fit,
    _channel_fit,
    _personalization_level,
    _select_angles,
    _opening_hook,
    _best_send_time,
    _outreach_urgency,
)


# ─── Helper ──────────────────────────────────────────────────────────────────

def make_contact(
    contact_id: str = "c001",
    full_name: str = "Jean Dupont",
    title: str = "Directeur Commercial",
    company: str = "Acme Corp",
    industry: str = "SaaS",
    company_size: str = "51-200",
    linkedin_connections: int = 300,
    website_visits_30d: int = 0,
    emails_opened_30d: int = 0,
    content_downloads: int = 0,
    event_attendances: int = 0,
    has_direct_phone: bool = False,
    has_linkedin: bool = True,
    has_personal_email: bool = False,
    crm_notes_count: int = 0,
    previous_interactions: int = 0,
    triggers: Optional[List[str]] = None,
    trigger_recency_days: int = 30,
    is_decision_maker: bool = False,
    budget_authority: bool = False,
    pain_score: float = 50.0,
    icp_score: float = 60.0,
    preferred_channel: Optional[str] = None,
    timezone_offset: int = 1,
) -> ContactProfile:
    if triggers is None:
        triggers = []
    return ContactProfile(
        contact_id=contact_id,
        full_name=full_name,
        title=title,
        company=company,
        industry=industry,
        company_size=company_size,
        linkedin_connections=linkedin_connections,
        website_visits_30d=website_visits_30d,
        emails_opened_30d=emails_opened_30d,
        content_downloads=content_downloads,
        event_attendances=event_attendances,
        has_direct_phone=has_direct_phone,
        has_linkedin=has_linkedin,
        has_personal_email=has_personal_email,
        crm_notes_count=crm_notes_count,
        previous_interactions=previous_interactions,
        triggers=triggers,
        trigger_recency_days=trigger_recency_days,
        is_decision_maker=is_decision_maker,
        budget_authority=budget_authority,
        pain_score=pain_score,
        icp_score=icp_score,
        preferred_channel=preferred_channel,
        timezone_offset=timezone_offset,
    )


# ═════════════════════════════════════════════════════════════════════════════
# _profile_richness
# ═════════════════════════════════════════════════════════════════════════════

class TestProfileRichness:
    def test_all_zeros_no_flags(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0)
        assert _profile_richness(c) == 0.0

    def test_has_direct_phone_adds_20(self):
        c = make_contact(has_linkedin=False, has_direct_phone=True, icp_score=0, pain_score=0)
        assert _profile_richness(c) == 20.0

    def test_has_linkedin_adds_15(self):
        c = make_contact(has_linkedin=True, icp_score=0, pain_score=0)
        assert _profile_richness(c) == 15.0

    def test_has_personal_email_adds_10(self):
        c = make_contact(has_linkedin=False, has_personal_email=True, icp_score=0, pain_score=0)
        assert _profile_richness(c) == 10.0

    def test_all_three_contact_flags(self):
        c = make_contact(has_direct_phone=True, has_linkedin=True, has_personal_email=True, icp_score=0, pain_score=0)
        assert _profile_richness(c) == 45.0

    def test_crm_notes_4_per_note(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0, crm_notes_count=3)
        assert _profile_richness(c) == 12.0

    def test_crm_notes_capped_at_20(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0, crm_notes_count=100)
        assert _profile_richness(c) == 20.0

    def test_crm_notes_exactly_5_gives_20(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0, crm_notes_count=5)
        assert _profile_richness(c) == 20.0

    def test_crm_notes_6_still_20(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0, crm_notes_count=6)
        assert _profile_richness(c) == 20.0

    def test_previous_interactions_5_per_each(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0, previous_interactions=3)
        assert _profile_richness(c) == 15.0

    def test_previous_interactions_capped_at_20(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0, previous_interactions=10)
        assert _profile_richness(c) == 20.0

    def test_previous_interactions_exactly_4_gives_20(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0, previous_interactions=4)
        assert _profile_richness(c) == 20.0

    def test_icp_score_contribution(self):
        c = make_contact(has_linkedin=False, icp_score=100, pain_score=0)
        assert _profile_richness(c) == 10.0

    def test_pain_score_contribution(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=100)
        assert _profile_richness(c) == 5.0

    def test_icp_and_pain_combined(self):
        c = make_contact(has_linkedin=False, icp_score=60, pain_score=50)
        expected = 60 * 0.10 + 50 * 0.05
        assert _profile_richness(c) == round(expected, 2)

    def test_total_capped_at_100(self):
        c = make_contact(
            has_direct_phone=True,
            has_linkedin=True,
            has_personal_email=True,
            crm_notes_count=100,
            previous_interactions=100,
            icp_score=100,
            pain_score=100,
        )
        assert _profile_richness(c) == 100.0

    def test_typical_rich_profile(self):
        c = make_contact(
            has_direct_phone=True,
            has_linkedin=True,
            has_personal_email=True,
            crm_notes_count=2,
            previous_interactions=2,
            icp_score=80,
            pain_score=60,
        )
        # 20 + 15 + 10 + 8 + 10 + 8 + 3 = 74
        expected = round(min(100.0, 20 + 15 + 10 + 8 + 10 + 80 * 0.10 + 60 * 0.05), 2)
        assert _profile_richness(c) == expected

    def test_return_type_is_float(self):
        c = make_contact()
        result = _profile_richness(c)
        assert isinstance(result, float)

    def test_zero_crm_notes_no_contribution(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0, crm_notes_count=0)
        assert _profile_richness(c) == 0.0

    def test_one_crm_note(self):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0, crm_notes_count=1)
        assert _profile_richness(c) == 4.0


# ═════════════════════════════════════════════════════════════════════════════
# _engagement_signals
# ═════════════════════════════════════════════════════════════════════════════

class TestEngagementSignals:
    def test_all_zero(self):
        c = make_contact()
        assert _engagement_signals(c) == 0.0

    def test_website_visits_10_per_visit(self):
        c = make_contact(website_visits_30d=3)
        assert _engagement_signals(c) == 30.0

    def test_website_visits_capped_at_40(self):
        c = make_contact(website_visits_30d=10)
        assert _engagement_signals(c) == 40.0

    def test_website_visits_exactly_4_gives_40(self):
        c = make_contact(website_visits_30d=4)
        assert _engagement_signals(c) == 40.0

    def test_emails_opened_8_per_open(self):
        c = make_contact(emails_opened_30d=2)
        assert _engagement_signals(c) == 16.0

    def test_emails_opened_capped_at_25(self):
        c = make_contact(emails_opened_30d=10)
        assert _engagement_signals(c) == 25.0

    def test_emails_opened_exactly_3_gives_24(self):
        c = make_contact(emails_opened_30d=3)
        assert _engagement_signals(c) == 24.0

    def test_content_downloads_10_per_download(self):
        c = make_contact(content_downloads=1)
        assert _engagement_signals(c) == 10.0

    def test_content_downloads_capped_at_20(self):
        c = make_contact(content_downloads=5)
        assert _engagement_signals(c) == 20.0

    def test_event_attendances_7_5_per_event(self):
        c = make_contact(event_attendances=2)
        assert _engagement_signals(c) == 15.0

    def test_event_attendances_capped_at_15(self):
        c = make_contact(event_attendances=5)
        assert _engagement_signals(c) == 15.0

    def test_total_capped_at_100(self):
        c = make_contact(
            website_visits_30d=100,
            emails_opened_30d=100,
            content_downloads=100,
            event_attendances=100,
        )
        assert _engagement_signals(c) == 100.0

    def test_combined_moderate(self):
        c = make_contact(
            website_visits_30d=2,
            emails_opened_30d=1,
            content_downloads=1,
            event_attendances=1,
        )
        expected = round(min(100.0, 20.0 + 8.0 + 10.0 + 7.5), 2)
        assert _engagement_signals(c) == expected

    def test_return_type_is_float(self):
        c = make_contact()
        assert isinstance(_engagement_signals(c), float)

    def test_single_website_visit(self):
        c = make_contact(website_visits_30d=1)
        assert _engagement_signals(c) == 10.0

    def test_single_email_open(self):
        c = make_contact(emails_opened_30d=1)
        assert _engagement_signals(c) == 8.0


# ═════════════════════════════════════════════════════════════════════════════
# _timing_fit
# ═════════════════════════════════════════════════════════════════════════════

class TestTimingFit:
    def test_no_triggers_gives_20_base(self):
        c = make_contact(triggers=[], trigger_recency_days=0)
        # trigger_score=20, no engagement_bonus → 20*0.70=14
        assert _timing_fit(c) == round(20.0 * 0.70, 2)

    def test_recency_0_gives_trigger_score_100(self):
        c = make_contact(triggers=[TriggerType.JOB_CHANGE.value], trigger_recency_days=0)
        # trigger_score=100, no bonus → 100*0.70=70
        assert _timing_fit(c) == round(100.0 * 0.70, 2)

    def test_recency_7_gives_trigger_score_80(self):
        c = make_contact(triggers=[TriggerType.FUNDING.value], trigger_recency_days=7)
        # 80 + (7-7)*(20/7) = 80
        expected = round(min(100.0, 80.0 * 0.70), 2)
        assert _timing_fit(c) == expected

    def test_recency_1_in_first_band(self):
        c = make_contact(triggers=[TriggerType.FUNDING.value], trigger_recency_days=1)
        trigger_score = 80.0 + (7 - 1) * (20.0 / 7.0)
        expected = round(min(100.0, trigger_score * 0.70), 2)
        assert _timing_fit(c) == expected

    def test_recency_3_in_first_band(self):
        c = make_contact(triggers=[TriggerType.HIRING.value], trigger_recency_days=3)
        trigger_score = 80.0 + (7 - 3) * (20.0 / 7.0)
        expected = round(min(100.0, trigger_score * 0.70), 2)
        assert _timing_fit(c) == expected

    def test_recency_8_in_second_band(self):
        c = make_contact(triggers=[TriggerType.HIRING.value], trigger_recency_days=8)
        trigger_score = 50.0 + (30 - 8) * (30.0 / 23.0)
        expected = round(min(100.0, trigger_score * 0.70), 2)
        assert _timing_fit(c) == expected

    def test_recency_30_boundary_second_band(self):
        c = make_contact(triggers=[TriggerType.HIRING.value], trigger_recency_days=30)
        trigger_score = 50.0 + (30 - 30) * (30.0 / 23.0)  # = 50
        expected = round(min(100.0, 50.0 * 0.70), 2)
        assert _timing_fit(c) == expected

    def test_recency_31_in_third_band(self):
        c = make_contact(triggers=[TriggerType.AWARD.value], trigger_recency_days=31)
        trigger_score = 20.0 + (60 - 31) * (30.0 / 30.0)
        expected = round(min(100.0, trigger_score * 0.70), 2)
        assert _timing_fit(c) == expected

    def test_recency_60_boundary_third_band(self):
        c = make_contact(triggers=[TriggerType.AWARD.value], trigger_recency_days=60)
        trigger_score = 20.0 + (60 - 60) * 1.0  # = 20
        expected = round(min(100.0, 20.0 * 0.70), 2)
        assert _timing_fit(c) == expected

    def test_recency_61_gives_trigger_score_10(self):
        c = make_contact(triggers=[TriggerType.AWARD.value], trigger_recency_days=61)
        expected = round(min(100.0, 10.0 * 0.70), 2)
        assert _timing_fit(c) == expected

    def test_recency_200_gives_trigger_score_10(self):
        c = make_contact(triggers=[TriggerType.AWARD.value], trigger_recency_days=200)
        expected = round(min(100.0, 10.0 * 0.70), 2)
        assert _timing_fit(c) == expected

    def test_engagement_bonus_website_adds_15(self):
        c = make_contact(triggers=[], website_visits_30d=1, emails_opened_30d=0)
        engagement_bonus = 15.0
        score = 20.0 * 0.70 + min(25.0, engagement_bonus) * 1.20
        assert _timing_fit(c) == round(min(100.0, score), 2)

    def test_engagement_bonus_email_adds_10(self):
        c = make_contact(triggers=[], emails_opened_30d=1, website_visits_30d=0)
        engagement_bonus = 10.0
        score = 20.0 * 0.70 + min(25.0, engagement_bonus) * 1.20
        assert _timing_fit(c) == round(min(100.0, score), 2)

    def test_engagement_bonus_both_adds_25(self):
        c = make_contact(triggers=[], website_visits_30d=1, emails_opened_30d=1)
        engagement_bonus = 25.0
        score = 20.0 * 0.70 + min(25.0, engagement_bonus) * 1.20
        assert _timing_fit(c) == round(min(100.0, score), 2)

    def test_engagement_bonus_capped_at_25(self):
        # Both website and email → bonus=25 exactly, no higher
        c = make_contact(triggers=[], website_visits_30d=5, emails_opened_30d=5)
        engagement_bonus = 25.0
        score = 20.0 * 0.70 + min(25.0, engagement_bonus) * 1.20
        assert _timing_fit(c) == round(min(100.0, score), 2)

    def test_score_capped_at_100(self):
        c = make_contact(
            triggers=[TriggerType.JOB_CHANGE.value],
            trigger_recency_days=0,
            website_visits_30d=5,
            emails_opened_30d=5,
        )
        assert _timing_fit(c) == 100.0

    def test_no_triggers_no_engagement_minimum(self):
        c = make_contact(triggers=[], website_visits_30d=0, emails_opened_30d=0)
        assert _timing_fit(c) == round(20.0 * 0.70, 2)

    def test_return_type_is_float(self):
        c = make_contact()
        assert isinstance(_timing_fit(c), float)


# ═════════════════════════════════════════════════════════════════════════════
# _channel_fit
# ═════════════════════════════════════════════════════════════════════════════

class TestChannelFit:
    def test_returns_tuple(self):
        c = make_contact()
        result = _channel_fit(c)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_score_is_float(self):
        c = make_contact()
        score, _ = _channel_fit(c)
        assert isinstance(score, float)

    def test_channel_is_outreach_channel(self):
        c = make_contact()
        _, channel = _channel_fit(c)
        assert isinstance(channel, OutreachChannel)

    def test_base_multi_beats_others_with_no_extras(self):
        # With has_linkedin=True (default), linkedin = 70, multi = 60
        # actually linkedin > multi → linkedin wins
        c = make_contact(has_linkedin=True)
        _, channel = _channel_fit(c)
        assert channel == OutreachChannel.LINKEDIN

    def test_no_extras_multi_wins_when_no_linkedin(self):
        c = make_contact(has_linkedin=False)
        _, channel = _channel_fit(c)
        assert channel == OutreachChannel.MULTI

    def test_has_linkedin_adds_20(self):
        c = make_contact(has_linkedin=True, has_direct_phone=False, has_personal_email=False)
        score, channel = _channel_fit(c)
        assert channel == OutreachChannel.LINKEDIN
        assert score == 70.0  # 50 + 20

    def test_has_direct_phone_adds_25(self):
        c = make_contact(has_linkedin=False, has_direct_phone=True, has_personal_email=False)
        score, channel = _channel_fit(c)
        assert channel == OutreachChannel.PHONE
        assert score == 75.0  # 50 + 25

    def test_has_personal_email_adds_15(self):
        c = make_contact(has_linkedin=False, has_direct_phone=False, has_personal_email=True)
        score, channel = _channel_fit(c)
        assert channel == OutreachChannel.EMAIL
        assert score == 65.0  # 50 + 15

    def test_linkedin_connections_500_adds_10(self):
        c = make_contact(has_linkedin=True, linkedin_connections=500)
        score, channel = _channel_fit(c)
        assert channel == OutreachChannel.LINKEDIN
        assert score == 80.0  # 50 + 20 + 10

    def test_linkedin_connections_499_no_bonus(self):
        c = make_contact(has_linkedin=True, linkedin_connections=499, has_direct_phone=False)
        score, channel = _channel_fit(c)
        assert score == 70.0  # 50 + 20 only

    def test_emails_opened_adds_10_to_email(self):
        c = make_contact(has_linkedin=False, emails_opened_30d=1, has_personal_email=True)
        # email = 50 + 15 + 10 = 75, linkedin=50, phone=50, multi=60
        score, channel = _channel_fit(c)
        assert channel == OutreachChannel.EMAIL
        assert score == 75.0

    def test_previous_interactions_2_adds_15_to_phone(self):
        c = make_contact(has_linkedin=False, has_direct_phone=True, previous_interactions=2)
        # phone = 50 + 25 + 15 = 90
        score, channel = _channel_fit(c)
        assert channel == OutreachChannel.PHONE
        assert score == 90.0

    def test_previous_interactions_1_no_phone_bonus(self):
        c = make_contact(has_linkedin=False, has_direct_phone=True, previous_interactions=1)
        # phone = 50 + 25 = 75
        score, channel = _channel_fit(c)
        assert score == 75.0

    def test_preferred_channel_email_adds_20(self):
        c = make_contact(has_linkedin=False, preferred_channel="email", has_personal_email=True)
        # email = 50 + 15 + 20 = 85
        score, channel = _channel_fit(c)
        assert channel == OutreachChannel.EMAIL
        assert score == 85.0

    def test_preferred_channel_linkedin_adds_20(self):
        c = make_contact(has_linkedin=True, preferred_channel="linkedin")
        # linkedin = 50 + 20 + 20 = 90
        score, channel = _channel_fit(c)
        assert channel == OutreachChannel.LINKEDIN
        assert score == 90.0

    def test_preferred_channel_phone_adds_20(self):
        c = make_contact(has_linkedin=False, has_direct_phone=True, preferred_channel="phone")
        # phone = 50 + 25 + 20 = 95
        score, channel = _channel_fit(c)
        assert channel == OutreachChannel.PHONE
        assert score == 95.0

    def test_score_capped_at_100(self):
        c = make_contact(
            has_linkedin=True,
            has_direct_phone=True,
            has_personal_email=True,
            linkedin_connections=500,
            emails_opened_30d=3,
            previous_interactions=5,
            preferred_channel="phone",
        )
        score, _ = _channel_fit(c)
        assert score == 100.0

    def test_preferred_channel_unknown_ignored(self):
        c = make_contact(has_linkedin=False, preferred_channel="fax")
        # nothing extra for fax, multi wins
        _, channel = _channel_fit(c)
        assert channel == OutreachChannel.MULTI

    def test_preferred_channel_none_no_boost(self):
        c = make_contact(has_linkedin=True, preferred_channel=None)
        score, channel = _channel_fit(c)
        assert channel == OutreachChannel.LINKEDIN
        assert score == 70.0


# ═════════════════════════════════════════════════════════════════════════════
# _personalization_level
# ═════════════════════════════════════════════════════════════════════════════

class TestPersonalizationLevel:
    def test_score_80_is_deep(self):
        assert _personalization_level(80.0) == PersonalizationLevel.DEEP

    def test_score_100_is_deep(self):
        assert _personalization_level(100.0) == PersonalizationLevel.DEEP

    def test_score_79_is_strong(self):
        assert _personalization_level(79.9) == PersonalizationLevel.STRONG

    def test_score_65_is_strong(self):
        assert _personalization_level(65.0) == PersonalizationLevel.STRONG

    def test_score_64_is_moderate(self):
        assert _personalization_level(64.9) == PersonalizationLevel.MODERATE

    def test_score_45_is_moderate(self):
        assert _personalization_level(45.0) == PersonalizationLevel.MODERATE

    def test_score_44_is_basic(self):
        assert _personalization_level(44.9) == PersonalizationLevel.BASIC

    def test_score_25_is_basic(self):
        assert _personalization_level(25.0) == PersonalizationLevel.BASIC

    def test_score_24_is_generic(self):
        assert _personalization_level(24.9) == PersonalizationLevel.GENERIC

    def test_score_0_is_generic(self):
        assert _personalization_level(0.0) == PersonalizationLevel.GENERIC

    def test_boundary_exactly_80(self):
        assert _personalization_level(80.0) == PersonalizationLevel.DEEP

    def test_boundary_exactly_65(self):
        assert _personalization_level(65.0) == PersonalizationLevel.STRONG

    def test_boundary_exactly_45(self):
        assert _personalization_level(45.0) == PersonalizationLevel.MODERATE

    def test_boundary_exactly_25(self):
        assert _personalization_level(25.0) == PersonalizationLevel.BASIC


# ═════════════════════════════════════════════════════════════════════════════
# _select_angles
# ═════════════════════════════════════════════════════════════════════════════

class TestSelectAngles:
    def test_returns_tuple(self):
        c = make_contact()
        result = _select_angles(c)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_primary_is_string(self):
        c = make_contact()
        primary, _ = _select_angles(c)
        assert isinstance(primary, str)

    def test_secondary_is_list(self):
        c = make_contact()
        _, secondary = _select_angles(c)
        assert isinstance(secondary, list)

    def test_job_change_trigger_highest_priority(self):
        c = make_contact(triggers=[
            TriggerType.JOB_CHANGE.value,
            TriggerType.FUNDING.value,
        ])
        primary, _ = _select_angles(c)
        assert "prise de poste" in primary or "90 premiers jours" in primary

    def test_funding_trigger_angle(self):
        c = make_contact(triggers=[TriggerType.FUNDING.value])
        primary, _ = _select_angles(c)
        assert "levée de fonds" in primary or "croissance" in primary

    def test_hiring_trigger_angle(self):
        c = make_contact(triggers=[TriggerType.HIRING.value])
        primary, _ = _select_angles(c)
        assert "recrutement" in primary or "scale" in primary

    def test_content_published_trigger(self):
        c = make_contact(triggers=[TriggerType.CONTENT_PUBLISHED.value])
        primary, _ = _select_angles(c)
        assert "contenu" in primary or "vision" in primary

    def test_event_attended_trigger(self):
        c = make_contact(triggers=[TriggerType.EVENT_ATTENDED.value])
        primary, _ = _select_angles(c)
        assert "événement" in primary or "contact" in primary

    def test_website_visit_trigger(self):
        c = make_contact(triggers=[TriggerType.WEBSITE_VISIT.value])
        primary, _ = _select_angles(c)
        assert "site" in primary or "visité" in primary

    def test_email_opened_trigger(self):
        c = make_contact(triggers=[TriggerType.EMAIL_OPENED.value])
        primary, _ = _select_angles(c)
        assert "email" in primary or "précédent" in primary

    def test_award_trigger_gives_growth_angle(self):
        c = make_contact(triggers=[TriggerType.AWARD.value])
        primary, _ = _select_angles(c)
        assert "croissance" in primary or "award" in primary or "expansion" in primary

    def test_expansion_trigger_gives_growth_angle(self):
        c = make_contact(triggers=[TriggerType.EXPANSION.value])
        primary, _ = _select_angles(c)
        assert "croissance" in primary or "expansion" in primary

    def test_no_trigger_high_pain_gives_pain_angle(self):
        c = make_contact(triggers=[], pain_score=70.0, icp_score=0)
        primary, _ = _select_angles(c)
        assert "pain point" in primary or "étude de cas" in primary

    def test_no_trigger_high_icp_gives_expertise_angle(self):
        c = make_contact(triggers=[], pain_score=0, icp_score=80.0)
        primary, _ = _select_angles(c)
        assert "expertise" in primary or "complémentarité" in primary

    def test_no_trigger_low_scores_gives_default(self):
        c = make_contact(triggers=[], pain_score=30, icp_score=30)
        primary, _ = _select_angles(c)
        # primary should be default (pain_angle template since default maps to pain_angle fallback)
        assert isinstance(primary, str)
        assert len(primary) > 0

    def test_pain_secondary_when_pain_60_and_not_primary(self):
        c = make_contact(triggers=[TriggerType.FUNDING.value], pain_score=60.0)
        _, secondary = _select_angles(c)
        assert any("pain point" in s or "étude de cas" in s for s in secondary)

    def test_pain_secondary_not_added_when_below_60(self):
        c = make_contact(triggers=[TriggerType.FUNDING.value], pain_score=59.0, icp_score=0)
        _, secondary = _select_angles(c)
        assert not any("pain point" in s for s in secondary)

    def test_peer_secondary_when_icp_75(self):
        c = make_contact(triggers=[], pain_score=30, icp_score=75.0)
        _, secondary = _select_angles(c)
        assert any("pair" in s or "social proof" in s for s in secondary)

    def test_peer_secondary_not_added_below_75(self):
        c = make_contact(triggers=[], pain_score=0, icp_score=74.0)
        _, secondary = _select_angles(c)
        assert not any("pair" in s or "social proof" in s for s in secondary)

    def test_job_change_is_primary_when_both_triggers_present(self):
        # JOB_CHANGE is #1 in trigger_priority, so it always wins primary
        # even when FUNDING is also in the trigger list
        c = make_contact(triggers=[TriggerType.FUNDING.value, TriggerType.JOB_CHANGE.value])
        primary, secondary = _select_angles(c)
        # primary must be job_change_angle (highest priority)
        assert "prise de poste" in primary or "90 premiers jours" in primary
        # job_change is primary → secondary check (primary != job_change_angle) is False → not in secondary
        assert not any("prise de poste" in s or "90 premiers" in s for s in secondary)

    def test_no_duplicate_angles_in_secondary(self):
        c = make_contact(
            triggers=[TriggerType.FUNDING.value],
            pain_score=75,
            icp_score=80,
        )
        _, secondary = _select_angles(c)
        assert len(secondary) == len(set(secondary))

    def test_primary_not_in_secondary(self):
        c = make_contact(triggers=[TriggerType.FUNDING.value], pain_score=80, icp_score=80)
        primary, secondary = _select_angles(c)
        assert primary not in secondary

    def test_secondary_max_2_items(self):
        c = make_contact(
            triggers=[TriggerType.FUNDING.value, TriggerType.JOB_CHANGE.value],
            pain_score=75,
            icp_score=80,
        )
        _, secondary = _select_angles(c)
        assert len(secondary) <= 2


# ═════════════════════════════════════════════════════════════════════════════
# _opening_hook
# ═════════════════════════════════════════════════════════════════════════════

class TestOpeningHook:
    def test_returns_string(self):
        c = make_contact()
        assert isinstance(_opening_hook(c), str)

    def test_job_change_uses_title(self):
        c = make_contact(triggers=[TriggerType.JOB_CHANGE.value], title="CEO")
        hook = _opening_hook(c)
        assert "CEO" in hook
        assert "prise de poste" in hook

    def test_funding_trigger(self):
        c = make_contact(triggers=[TriggerType.FUNDING.value])
        hook = _opening_hook(c)
        assert "levée" in hook

    def test_hiring_uses_company(self):
        c = make_contact(triggers=[TriggerType.HIRING.value], company="BigCorp")
        hook = _opening_hook(c)
        assert "BigCorp" in hook

    def test_content_published_trigger(self):
        c = make_contact(triggers=[TriggerType.CONTENT_PUBLISHED.value])
        hook = _opening_hook(c)
        assert "post" in hook or "article" in hook

    def test_event_attended_trigger(self):
        c = make_contact(triggers=[TriggerType.EVENT_ATTENDED.value])
        hook = _opening_hook(c)
        assert "événement" in hook

    def test_website_visits_fallback(self):
        c = make_contact(triggers=[], website_visits_30d=2)
        hook = _opening_hook(c)
        assert "solution" in hook or "récemment" in hook

    def test_email_opened_fallback(self):
        c = make_contact(triggers=[], emails_opened_30d=1, website_visits_30d=0)
        hook = _opening_hook(c)
        assert "précédent" in hook or "reviens" in hook

    def test_default_hook_when_no_signals(self):
        c = make_contact(triggers=[], website_visits_30d=0, emails_opened_30d=0)
        hook = _opening_hook(c)
        assert "profil" in hook or "clients" in hook

    def test_job_change_priority_over_funding(self):
        c = make_contact(triggers=[TriggerType.JOB_CHANGE.value, TriggerType.FUNDING.value])
        hook = _opening_hook(c)
        assert "prise de poste" in hook

    def test_funding_priority_over_hiring(self):
        c = make_contact(triggers=[TriggerType.FUNDING.value, TriggerType.HIRING.value])
        hook = _opening_hook(c)
        assert "levée" in hook

    def test_website_visit_priority_over_email_opened(self):
        c = make_contact(triggers=[], website_visits_30d=1, emails_opened_30d=1)
        hook = _opening_hook(c)
        assert "solution" in hook or "récemment" in hook


# ═════════════════════════════════════════════════════════════════════════════
# _best_send_time
# ═════════════════════════════════════════════════════════════════════════════

class TestBestSendTime:
    def test_tz_minus_6_returns_15h(self):
        c = make_contact(timezone_offset=-6)
        assert "15h00" in _best_send_time(c)

    def test_tz_minus_3_returns_15h(self):
        c = make_contact(timezone_offset=-3)
        assert "15h00" in _best_send_time(c)

    def test_tz_minus_4_returns_15h(self):
        c = make_contact(timezone_offset=-4)
        assert "15h00" in _best_send_time(c)

    def test_tz_8_returns_08h(self):
        c = make_contact(timezone_offset=8)
        assert "08h00" in _best_send_time(c)

    def test_tz_10_returns_08h(self):
        c = make_contact(timezone_offset=10)
        assert "08h00" in _best_send_time(c)

    def test_tz_1_returns_09h_or_14h(self):
        c = make_contact(timezone_offset=1)
        result = _best_send_time(c)
        assert "09h00" in result or "14h00" in result

    def test_tz_0_returns_default(self):
        c = make_contact(timezone_offset=0)
        result = _best_send_time(c)
        assert "09h00" in result or "14h00" in result

    def test_tz_7_returns_default(self):
        c = make_contact(timezone_offset=7)
        result = _best_send_time(c)
        assert "09h00" in result or "14h00" in result

    def test_tz_minus_7_returns_default(self):
        c = make_contact(timezone_offset=-7)
        result = _best_send_time(c)
        assert "09h00" in result or "14h00" in result

    def test_returns_string(self):
        c = make_contact()
        assert isinstance(_best_send_time(c), str)


# ═════════════════════════════════════════════════════════════════════════════
# _outreach_urgency
# ═════════════════════════════════════════════════════════════════════════════

class TestOutreachUrgency:
    def test_basic_formula(self):
        c = make_contact(is_decision_maker=False, budget_authority=False, icp_score=50)
        timing = 40.0
        engagement = 30.0
        expected = round(timing * 0.50 + engagement * 0.30 + 50 * 0.20, 2)
        assert _outreach_urgency(c, timing, engagement) == expected

    def test_decision_maker_adds_10(self):
        c = make_contact(is_decision_maker=True, budget_authority=False, icp_score=0)
        timing = 0.0
        engagement = 0.0
        assert _outreach_urgency(c, timing, engagement) == 10.0

    def test_budget_authority_adds_5(self):
        c = make_contact(is_decision_maker=False, budget_authority=True, icp_score=0)
        assert _outreach_urgency(c, 0.0, 0.0) == 5.0

    def test_both_flags_add_15(self):
        c = make_contact(is_decision_maker=True, budget_authority=True, icp_score=0)
        assert _outreach_urgency(c, 0.0, 0.0) == 15.0

    def test_capped_at_100(self):
        c = make_contact(is_decision_maker=True, budget_authority=True, icp_score=100)
        assert _outreach_urgency(c, 100.0, 100.0) == 100.0

    def test_returns_float(self):
        c = make_contact()
        assert isinstance(_outreach_urgency(c, 50.0, 50.0), float)

    def test_icp_contribution(self):
        c = make_contact(is_decision_maker=False, budget_authority=False, icp_score=80)
        result = _outreach_urgency(c, 0.0, 0.0)
        assert result == round(80 * 0.20, 2)

    def test_zero_all(self):
        c = make_contact(is_decision_maker=False, budget_authority=False, icp_score=0)
        assert _outreach_urgency(c, 0.0, 0.0) == 0.0

    def test_decision_maker_cap_respected(self):
        c = make_contact(is_decision_maker=True, budget_authority=False, icp_score=100)
        # base = 100*0.50 + 100*0.30 + 100*0.20 = 100 → +10 → min(100,110)=100
        assert _outreach_urgency(c, 100.0, 100.0) == 100.0


# ═════════════════════════════════════════════════════════════════════════════
# ContactPersonalizer
# ═════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def personalizer():
    return ContactPersonalizer()


class TestPersonalizeMethod:
    def test_returns_personalization_plan(self, personalizer):
        c = make_contact()
        plan = personalizer.personalize(c)
        assert isinstance(plan, PersonalizationPlan)

    def test_plan_stored_in_store(self, personalizer):
        c = make_contact(contact_id="x1")
        personalizer.personalize(c)
        assert personalizer.get("x1") is not None

    def test_plan_contact_matches(self, personalizer):
        c = make_contact(contact_id="x2")
        plan = personalizer.personalize(c)
        assert plan.contact.contact_id == "x2"

    def test_do_not_contact_false_by_default(self, personalizer):
        c = make_contact()
        plan = personalizer.personalize(c)
        assert plan.do_not_contact is False

    def test_personalization_score_in_range(self, personalizer):
        c = make_contact()
        plan = personalizer.personalize(c)
        assert 0.0 <= plan.personalization_score <= 100.0

    def test_plan_has_primary_angle(self, personalizer):
        c = make_contact()
        plan = personalizer.personalize(c)
        assert isinstance(plan.primary_angle, str)
        assert len(plan.primary_angle) > 0

    def test_plan_has_opening_hook(self, personalizer):
        c = make_contact()
        plan = personalizer.personalize(c)
        assert isinstance(plan.opening_hook, str)

    def test_plan_has_cta(self, personalizer):
        c = make_contact()
        plan = personalizer.personalize(c)
        assert isinstance(plan.call_to_action, str)

    def test_plan_has_send_time(self, personalizer):
        c = make_contact()
        plan = personalizer.personalize(c)
        assert isinstance(plan.best_send_time, str)

    def test_plan_has_tokens(self, personalizer):
        c = make_contact()
        plan = personalizer.personalize(c)
        assert isinstance(plan.personalization_tokens, list)

    def test_plan_has_recommended_channel(self, personalizer):
        c = make_contact()
        plan = personalizer.personalize(c)
        assert isinstance(plan.recommended_channel, OutreachChannel)

    def test_plan_overwritten_on_second_call(self, personalizer):
        c1 = make_contact(contact_id="dup")
        c2 = make_contact(contact_id="dup", icp_score=99)
        personalizer.personalize(c1)
        plan = personalizer.personalize(c2)
        assert plan.contact.icp_score == 99

    def test_dnc_applied_at_personalize(self, personalizer):
        personalizer.add_to_dnc("dnc1")
        c = make_contact(contact_id="dnc1")
        plan = personalizer.personalize(c)
        assert plan.do_not_contact is True

    def test_non_dnc_contact_not_flagged(self, personalizer):
        personalizer.add_to_dnc("dnc2")
        c = make_contact(contact_id="other")
        plan = personalizer.personalize(c)
        assert plan.do_not_contact is False


class TestAddToDnc:
    def test_dnc_flag_set_after_personalize(self, personalizer):
        c = make_contact(contact_id="a1")
        personalizer.personalize(c)
        personalizer.add_to_dnc("a1")
        # DNC is applied on personalize, so re-personalize to see effect
        plan = personalizer.personalize(c)
        assert plan.do_not_contact is True

    def test_dnc_before_personalize(self, personalizer):
        personalizer.add_to_dnc("pre1")
        c = make_contact(contact_id="pre1")
        plan = personalizer.personalize(c)
        assert plan.do_not_contact is True

    def test_dnc_does_not_affect_other_contacts(self, personalizer):
        personalizer.add_to_dnc("bad")
        c = make_contact(contact_id="good")
        plan = personalizer.personalize(c)
        assert plan.do_not_contact is False


class TestPersonalizeBatch:
    def test_returns_list(self, personalizer):
        contacts = [make_contact(contact_id=f"b{i}") for i in range(3)]
        result = personalizer.personalize_batch(contacts)
        assert isinstance(result, list)

    def test_batch_count_matches(self, personalizer):
        contacts = [make_contact(contact_id=f"c{i}") for i in range(5)]
        result = personalizer.personalize_batch(contacts)
        assert len(result) == 5

    def test_all_stored_after_batch(self, personalizer):
        contacts = [make_contact(contact_id=f"d{i}") for i in range(4)]
        personalizer.personalize_batch(contacts)
        for i in range(4):
            assert personalizer.get(f"d{i}") is not None

    def test_empty_batch(self, personalizer):
        result = personalizer.personalize_batch([])
        assert result == []

    def test_batch_applies_dnc(self, personalizer):
        personalizer.add_to_dnc("e0")
        contacts = [make_contact(contact_id=f"e{i}") for i in range(3)]
        results = personalizer.personalize_batch(contacts)
        assert results[0].do_not_contact is True
        assert results[1].do_not_contact is False


class TestGetMethod:
    def test_get_existing(self, personalizer):
        c = make_contact(contact_id="g1")
        personalizer.personalize(c)
        assert personalizer.get("g1") is not None

    def test_get_missing_returns_none(self, personalizer):
        assert personalizer.get("nonexistent") is None

    def test_get_returns_plan(self, personalizer):
        c = make_contact(contact_id="g2")
        plan = personalizer.personalize(c)
        retrieved = personalizer.get("g2")
        assert retrieved is plan


class TestAllPlans:
    def test_empty_store(self, personalizer):
        assert personalizer.all_plans() == []

    def test_sorted_by_urgency_descending(self, personalizer):
        # Create contacts with different urgency levels
        c_low = make_contact(contact_id="low", icp_score=10, is_decision_maker=False, budget_authority=False)
        c_high = make_contact(contact_id="high", icp_score=100, is_decision_maker=True, budget_authority=True,
                              triggers=[TriggerType.JOB_CHANGE.value], trigger_recency_days=0,
                              website_visits_30d=5)
        personalizer.personalize(c_low)
        personalizer.personalize(c_high)
        plans = personalizer.all_plans()
        assert plans[0].contact.contact_id == "high"
        assert plans[-1].contact.contact_id == "low"

    def test_all_plans_count(self, personalizer):
        for i in range(6):
            personalizer.personalize(make_contact(contact_id=f"ap{i}"))
        assert len(personalizer.all_plans()) == 6


class TestByLevel:
    def test_filters_by_level(self, personalizer):
        # Force a GENERIC contact (all zeros)
        c = make_contact(
            has_linkedin=False, icp_score=0, pain_score=0,
            triggers=[], website_visits_30d=0, emails_opened_30d=0
        )
        personalizer.personalize(c)
        # Check it's classified correctly then filter
        plan = personalizer.get(c.contact_id)
        level = plan.personalization_level
        result = personalizer.by_level(level)
        assert all(p.personalization_level == level for p in result)

    def test_empty_when_no_match(self, personalizer):
        c = make_contact(has_linkedin=False, icp_score=0, pain_score=0)
        personalizer.personalize(c)
        result = personalizer.by_level(PersonalizationLevel.DEEP)
        # All zeros → generic; no deep contacts
        assert result == [] or all(p.personalization_level == PersonalizationLevel.DEEP for p in result)

    def test_returns_list(self, personalizer):
        assert isinstance(personalizer.by_level(PersonalizationLevel.MODERATE), list)


class TestByChannel:
    def test_filters_by_channel(self, personalizer):
        c = make_contact(has_linkedin=True, has_direct_phone=False, preferred_channel="linkedin")
        personalizer.personalize(c)
        result = personalizer.by_channel(OutreachChannel.LINKEDIN)
        assert all(p.recommended_channel == OutreachChannel.LINKEDIN for p in result)

    def test_returns_list(self, personalizer):
        assert isinstance(personalizer.by_channel(OutreachChannel.EMAIL), list)

    def test_empty_when_no_match(self, personalizer):
        c = make_contact(has_linkedin=True)
        personalizer.personalize(c)
        result = personalizer.by_channel(OutreachChannel.PHONE)
        assert isinstance(result, list)


class TestHotContacts:
    def test_default_threshold_70(self, personalizer):
        c = make_contact(contact_id="hot1", icp_score=100, is_decision_maker=True,
                         budget_authority=True, triggers=[TriggerType.JOB_CHANGE.value],
                         trigger_recency_days=0, website_visits_30d=5)
        personalizer.personalize(c)
        hot = personalizer.hot_contacts()
        ids = [p.contact.contact_id for p in hot]
        assert "hot1" in ids

    def test_excludes_dnc(self, personalizer):
        personalizer.add_to_dnc("dnchot")
        c = make_contact(contact_id="dnchot", icp_score=100, is_decision_maker=True,
                         budget_authority=True, triggers=[TriggerType.JOB_CHANGE.value],
                         trigger_recency_days=0, website_visits_30d=5)
        personalizer.personalize(c)
        hot = personalizer.hot_contacts()
        ids = [p.contact.contact_id for p in hot]
        assert "dnchot" not in ids

    def test_sorted_descending(self, personalizer):
        for i, icp in enumerate([30, 80, 60]):
            c = make_contact(contact_id=f"hs{i}", icp_score=icp,
                             is_decision_maker=True, budget_authority=True,
                             triggers=[TriggerType.JOB_CHANGE.value], trigger_recency_days=0,
                             website_visits_30d=5)
            personalizer.personalize(c)
        hot = personalizer.hot_contacts()
        urgencies = [p.outreach_urgency for p in hot]
        assert urgencies == sorted(urgencies, reverse=True)

    def test_custom_threshold(self, personalizer):
        c = make_contact(contact_id="lowu", icp_score=0, is_decision_maker=False,
                         budget_authority=False, triggers=[], website_visits_30d=0)
        personalizer.personalize(c)
        # Low urgency contact should not appear at threshold=10 if urgency is 0
        plan = personalizer.get("lowu")
        hot = personalizer.hot_contacts(threshold=plan.outreach_urgency + 1)
        ids = [p.contact.contact_id for p in hot]
        assert "lowu" not in ids

    def test_returns_list(self, personalizer):
        assert isinstance(personalizer.hot_contacts(), list)


class TestTopPriority:
    def test_returns_n_items(self, personalizer):
        for i in range(15):
            personalizer.personalize(make_contact(contact_id=f"tp{i}"))
        result = personalizer.top_priority(5)
        assert len(result) == 5

    def test_default_n_10(self, personalizer):
        for i in range(15):
            personalizer.personalize(make_contact(contact_id=f"tp2{i}"))
        result = personalizer.top_priority()
        assert len(result) == 10

    def test_fewer_than_n_returns_all(self, personalizer):
        for i in range(3):
            personalizer.personalize(make_contact(contact_id=f"tp3{i}"))
        result = personalizer.top_priority(10)
        assert len(result) == 3

    def test_sorted_descending(self, personalizer):
        for i in range(5):
            personalizer.personalize(make_contact(contact_id=f"tp4{i}", icp_score=i * 20))
        result = personalizer.top_priority(5)
        urgencies = [p.outreach_urgency for p in result]
        assert urgencies == sorted(urgencies, reverse=True)


class TestDeepPersonalizationContacts:
    def test_returns_only_deep(self, personalizer):
        # Create a genuinely deep contact
        c = make_contact(
            contact_id="deep1",
            has_direct_phone=True,
            has_linkedin=True,
            has_personal_email=True,
            crm_notes_count=5,
            previous_interactions=4,
            icp_score=100,
            pain_score=100,
            triggers=[TriggerType.JOB_CHANGE.value],
            trigger_recency_days=0,
            website_visits_30d=4,
            emails_opened_30d=3,
            content_downloads=2,
            event_attendances=2,
            linkedin_connections=500,
            preferred_channel="linkedin",
        )
        personalizer.personalize(c)
        result = personalizer.deep_personalization_contacts()
        for p in result:
            assert p.personalization_level == PersonalizationLevel.DEEP

    def test_returns_list(self, personalizer):
        assert isinstance(personalizer.deep_personalization_contacts(), list)


class TestSummary:
    def test_empty_summary(self, personalizer):
        s = personalizer.summary()
        assert s["total"] == 0
        assert s["avg_personalization_score"] == 0.0
        assert s["avg_urgency"] == 0.0
        assert s["hot_count"] == 0
        assert s["dnc_count"] == 0

    def test_empty_summary_level_counts_all_zero(self, personalizer):
        s = personalizer.summary()
        for level in PersonalizationLevel:
            assert s["level_counts"][level.value] == 0

    def test_empty_summary_channel_counts_all_zero(self, personalizer):
        s = personalizer.summary()
        for channel in OutreachChannel:
            assert s["channel_counts"][channel.value] == 0

    def test_non_empty_total(self, personalizer):
        for i in range(3):
            personalizer.personalize(make_contact(contact_id=f"sum{i}"))
        s = personalizer.summary()
        assert s["total"] == 3

    def test_non_empty_level_counts_sum_to_total(self, personalizer):
        for i in range(4):
            personalizer.personalize(make_contact(contact_id=f"sum2{i}"))
        s = personalizer.summary()
        assert sum(s["level_counts"].values()) == s["total"]

    def test_non_empty_channel_counts_sum_to_total(self, personalizer):
        for i in range(4):
            personalizer.personalize(make_contact(contact_id=f"sum3{i}"))
        s = personalizer.summary()
        assert sum(s["channel_counts"].values()) == s["total"]

    def test_dnc_count_counted(self, personalizer):
        personalizer.add_to_dnc("sdnc1")
        c = make_contact(contact_id="sdnc1")
        personalizer.personalize(c)
        personalizer.personalize(make_contact(contact_id="notdnc"))
        s = personalizer.summary()
        assert s["dnc_count"] == 1

    def test_hot_count_excluded_dnc(self, personalizer):
        personalizer.add_to_dnc("hotdnc")
        c = make_contact(contact_id="hotdnc", icp_score=100, is_decision_maker=True,
                         budget_authority=True, triggers=[TriggerType.JOB_CHANGE.value],
                         trigger_recency_days=0, website_visits_30d=5)
        personalizer.personalize(c)
        s = personalizer.summary()
        assert s["hot_count"] == 0

    def test_avg_score_computed(self, personalizer):
        contacts = [make_contact(contact_id=f"avg{i}") for i in range(3)]
        plans = personalizer.personalize_batch(contacts)
        s = personalizer.summary()
        expected = round(sum(p.personalization_score for p in plans) / 3, 2)
        assert s["avg_personalization_score"] == expected

    def test_avg_urgency_computed(self, personalizer):
        contacts = [make_contact(contact_id=f"urg{i}") for i in range(3)]
        plans = personalizer.personalize_batch(contacts)
        s = personalizer.summary()
        expected = round(sum(p.outreach_urgency for p in plans) / 3, 2)
        assert s["avg_urgency"] == expected

    def test_summary_has_all_required_keys(self, personalizer):
        s = personalizer.summary()
        required = {"total", "level_counts", "channel_counts",
                    "avg_personalization_score", "avg_urgency", "hot_count", "dnc_count"}
        assert required.issubset(s.keys())


class TestReset:
    def test_reset_clears_store(self, personalizer):
        personalizer.personalize(make_contact(contact_id="r1"))
        personalizer.reset()
        assert personalizer.get("r1") is None

    def test_reset_clears_dnc(self, personalizer):
        personalizer.add_to_dnc("rdnc")
        personalizer.reset()
        c = make_contact(contact_id="rdnc")
        plan = personalizer.personalize(c)
        assert plan.do_not_contact is False

    def test_all_plans_empty_after_reset(self, personalizer):
        for i in range(5):
            personalizer.personalize(make_contact(contact_id=f"rst{i}"))
        personalizer.reset()
        assert personalizer.all_plans() == []

    def test_summary_empty_after_reset(self, personalizer):
        personalizer.personalize(make_contact(contact_id="rst_sum"))
        personalizer.reset()
        assert personalizer.summary()["total"] == 0

    def test_hot_contacts_empty_after_reset(self, personalizer):
        personalizer.personalize(make_contact(contact_id="rst_hot", icp_score=100,
                                              is_decision_maker=True))
        personalizer.reset()
        assert personalizer.hot_contacts() == []


# ═════════════════════════════════════════════════════════════════════════════
# Integration / end-to-end tests
# ═════════════════════════════════════════════════════════════════════════════

class TestIntegration:
    def test_personalization_plan_to_dict(self):
        p = ContactPersonalizer()
        c = make_contact()
        plan = p.personalize(c)
        d = plan.to_dict()
        assert isinstance(d, dict)
        assert "personalization_level" in d
        assert "recommended_channel" in d
        assert "personalization_score" in d

    def test_contact_profile_to_dict(self):
        c = make_contact()
        d = c.to_dict()
        assert isinstance(d, dict)
        assert d["contact_id"] == c.contact_id

    def test_full_profile_rich_contact_gets_high_score(self):
        p = ContactPersonalizer()
        c = make_contact(
            has_direct_phone=True,
            has_linkedin=True,
            has_personal_email=True,
            crm_notes_count=5,
            previous_interactions=4,
            icp_score=100,
            pain_score=100,
            triggers=[TriggerType.JOB_CHANGE.value],
            trigger_recency_days=0,
            website_visits_30d=4,
            emails_opened_30d=3,
        )
        plan = p.personalize(c)
        assert plan.personalization_score >= 65  # At least STRONG

    def test_bare_contact_gets_low_score(self):
        p = ContactPersonalizer()
        c = make_contact(
            has_linkedin=False,
            icp_score=0,
            pain_score=0,
            triggers=[],
            website_visits_30d=0,
            emails_opened_30d=0,
        )
        plan = p.personalize(c)
        assert plan.personalization_score < 50

    def test_composite_score_formula(self):
        p = ContactPersonalizer()
        c = make_contact()
        plan = p.personalize(c)
        richness = _profile_richness(c)
        engagement = _engagement_signals(c)
        timing = _timing_fit(c)
        channel_score, _ = _channel_fit(c)
        expected = round(richness * 0.30 + engagement * 0.25 + timing * 0.25 + channel_score * 0.20, 2)
        assert plan.personalization_score == expected

    def test_personalization_level_matches_score(self):
        p = ContactPersonalizer()
        c = make_contact()
        plan = p.personalize(c)
        expected_level = _personalization_level(plan.personalization_score)
        assert plan.personalization_level == expected_level

    def test_tokens_include_first_name(self):
        p = ContactPersonalizer()
        c = make_contact(full_name="Alice Martin")
        plan = p.personalize(c)
        assert any("Alice" in t for t in plan.personalization_tokens)

    def test_tokens_include_company(self):
        p = ContactPersonalizer()
        c = make_contact(company="TechCo")
        plan = p.personalize(c)
        assert any("TechCo" in t for t in plan.personalization_tokens)

    def test_tokens_include_trigger_when_present(self):
        p = ContactPersonalizer()
        c = make_contact(triggers=[TriggerType.FUNDING.value])
        plan = p.personalize(c)
        assert any("funding" in t.lower() or "Déclencheur" in t for t in plan.personalization_tokens)

    def test_tokens_include_pain_when_high(self):
        p = ContactPersonalizer()
        c = make_contact(pain_score=80)
        plan = p.personalize(c)
        assert any("Pain" in t or "pain" in t for t in plan.personalization_tokens)

    def test_cta_matches_level(self):
        from swarm.intelligence.contact_personalizer import _CTA_BY_LEVEL
        p = ContactPersonalizer()
        c = make_contact()
        plan = p.personalize(c)
        assert plan.call_to_action == _CTA_BY_LEVEL[plan.personalization_level]

    def test_multiple_batch_then_filter(self):
        p = ContactPersonalizer()
        contacts = [
            make_contact(contact_id="f1", has_linkedin=True, preferred_channel="linkedin"),
            make_contact(contact_id="f2", has_direct_phone=True, preferred_channel="phone"),
            make_contact(contact_id="f3", has_personal_email=True, preferred_channel="email"),
        ]
        p.personalize_batch(contacts)
        linkedin_plans = p.by_channel(OutreachChannel.LINKEDIN)
        assert any(pl.contact.contact_id == "f1" for pl in linkedin_plans)

    def test_urgency_stored_in_plan(self):
        p = ContactPersonalizer()
        c = make_contact(icp_score=70, is_decision_maker=True)
        plan = p.personalize(c)
        timing = _timing_fit(c)
        engagement = _engagement_signals(c)
        expected_urgency = _outreach_urgency(c, timing, engagement)
        assert plan.outreach_urgency == expected_urgency

    def test_enum_values_serializable(self):
        p = ContactPersonalizer()
        c = make_contact()
        plan = p.personalize(c)
        d = plan.to_dict()
        assert isinstance(d["personalization_level"], str)
        assert isinstance(d["recommended_channel"], str)

    def test_reset_then_use_again(self):
        p = ContactPersonalizer()
        p.personalize(make_contact(contact_id="before"))
        p.reset()
        p.personalize(make_contact(contact_id="after"))
        assert p.get("before") is None
        assert p.get("after") is not None

    def test_trigger_type_enum_values(self):
        assert TriggerType.JOB_CHANGE.value == "job_change"
        assert TriggerType.FUNDING.value == "funding"
        assert TriggerType.HIRING.value == "hiring"
        assert TriggerType.CONTENT_PUBLISHED.value == "content_published"
        assert TriggerType.EVENT_ATTENDED.value == "event_attended"
        assert TriggerType.WEBSITE_VISIT.value == "website_visit"
        assert TriggerType.EMAIL_OPENED.value == "email_opened"
        assert TriggerType.AWARD.value == "award"
        assert TriggerType.EXPANSION.value == "expansion"
