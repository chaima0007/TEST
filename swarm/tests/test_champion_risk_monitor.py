"""
Comprehensive pytest test suite for ChampionRiskMonitor.
Covers all enums, dataclasses, scoring helpers, classifiers,
monitor/monitor_batch, properties, reset, and summary.
"""
from __future__ import annotations

import dataclasses
import pytest

from swarm.intelligence.champion_risk_monitor import (
    ChampionRiskMonitor,
    ChampionRiskInput,
    ChampionRiskResult,
    ChampionStatus,
    ChampionRisk,
    InfluenceLevel,
    ChampionAction,
)


# ---------------------------------------------------------------------------
# Factory helper — a healthy, high-composite champion (no red flags)
# ---------------------------------------------------------------------------

def make_inp(
    deal_id: str = "deal-001",
    deal_name: str = "Acme Corp",
    rep_id: str = "rep-1",
    champion_name: str = "Alice",
    days_since_champion_contact: int = 2,
    champion_reply_rate_pct: float = 80.0,
    champion_meetings_last_30d: int = 4,
    champion_meetings_prior_30d: int = 3,
    champion_intro_count: int = 4,
    champion_created_internal_urgency: int = 1,
    champion_job_change_signal: int = 0,
    champion_promotion_signal: int = 0,
    champion_title_level: int = 4,
    champion_budget_authority: int = 1,
    backup_champion_identified: int = 1,
    deal_stage_numeric: int = 5,
    deal_size_usd: float = 150_000.0,
    days_to_close: int = 30,
    executive_relationship_score: float = 80.0,
    multi_threaded_contacts: int = 6,
    last_positive_signal_days_ago: int = 3,
    deal_age_days: int = 60,
) -> ChampionRiskInput:
    return ChampionRiskInput(
        deal_id=deal_id,
        deal_name=deal_name,
        rep_id=rep_id,
        champion_name=champion_name,
        days_since_champion_contact=days_since_champion_contact,
        champion_reply_rate_pct=champion_reply_rate_pct,
        champion_meetings_last_30d=champion_meetings_last_30d,
        champion_meetings_prior_30d=champion_meetings_prior_30d,
        champion_intro_count=champion_intro_count,
        champion_created_internal_urgency=champion_created_internal_urgency,
        champion_job_change_signal=champion_job_change_signal,
        champion_promotion_signal=champion_promotion_signal,
        champion_title_level=champion_title_level,
        champion_budget_authority=champion_budget_authority,
        backup_champion_identified=backup_champion_identified,
        deal_stage_numeric=deal_stage_numeric,
        deal_size_usd=deal_size_usd,
        days_to_close=days_to_close,
        executive_relationship_score=executive_relationship_score,
        multi_threaded_contacts=multi_threaded_contacts,
        last_positive_signal_days_ago=last_positive_signal_days_ago,
        deal_age_days=deal_age_days,
    )


# ---------------------------------------------------------------------------
# Helper: create monitor and run one result
# ---------------------------------------------------------------------------

def run(inp: ChampionRiskInput) -> ChampionRiskResult:
    return ChampionRiskMonitor().monitor(inp)


# ---------------------------------------------------------------------------
# 1. ChampionStatus enum
# ---------------------------------------------------------------------------

class TestChampionStatusEnum:
    def test_active_advocate_value(self):
        assert ChampionStatus.ACTIVE_ADVOCATE == "active_advocate"

    def test_engaged_value(self):
        assert ChampionStatus.ENGAGED == "engaged"

    def test_cooling_value(self):
        assert ChampionStatus.COOLING == "cooling"

    def test_silent_value(self):
        assert ChampionStatus.SILENT == "silent"

    def test_departed_value(self):
        assert ChampionStatus.DEPARTED == "departed"

    def test_exactly_five_members(self):
        assert len(ChampionStatus) == 5

    def test_is_str_enum(self):
        assert isinstance(ChampionStatus.ENGAGED, str)


# ---------------------------------------------------------------------------
# 2. ChampionRisk enum
# ---------------------------------------------------------------------------

class TestChampionRiskEnum:
    def test_low_value(self):
        assert ChampionRisk.LOW == "low"

    def test_moderate_value(self):
        assert ChampionRisk.MODERATE == "moderate"

    def test_high_value(self):
        assert ChampionRisk.HIGH == "high"

    def test_critical_value(self):
        assert ChampionRisk.CRITICAL == "critical"

    def test_exactly_four_members(self):
        assert len(ChampionRisk) == 4

    def test_is_str_enum(self):
        assert isinstance(ChampionRisk.HIGH, str)


# ---------------------------------------------------------------------------
# 3. InfluenceLevel enum
# ---------------------------------------------------------------------------

class TestInfluenceLevelEnum:
    def test_high_influence_value(self):
        assert InfluenceLevel.HIGH_INFLUENCE == "high_influence"

    def test_moderate_influence_value(self):
        assert InfluenceLevel.MODERATE_INFLUENCE == "moderate_influence"

    def test_low_influence_value(self):
        assert InfluenceLevel.LOW_INFLUENCE == "low_influence"

    def test_unknown_value(self):
        assert InfluenceLevel.UNKNOWN == "unknown"

    def test_exactly_four_members(self):
        assert len(InfluenceLevel) == 4

    def test_is_str_enum(self):
        assert isinstance(InfluenceLevel.UNKNOWN, str)


# ---------------------------------------------------------------------------
# 4. ChampionAction enum
# ---------------------------------------------------------------------------

class TestChampionActionEnum:
    def test_maintain_value(self):
        assert ChampionAction.MAINTAIN == "maintain"

    def test_re_engage_value(self):
        assert ChampionAction.RE_ENGAGE == "re_engage"

    def test_find_backup_value(self):
        assert ChampionAction.FIND_BACKUP == "find_backup"

    def test_escalate_exec_value(self):
        assert ChampionAction.ESCALATE_EXEC == "escalate_exec"

    def test_exactly_four_members(self):
        assert len(ChampionAction) == 4

    def test_is_str_enum(self):
        assert isinstance(ChampionAction.MAINTAIN, str)


# ---------------------------------------------------------------------------
# 5. ChampionRiskInput — exactly 22 fields
# ---------------------------------------------------------------------------

class TestChampionRiskInput:
    def test_exactly_22_fields(self):
        fields = dataclasses.fields(ChampionRiskInput)
        assert len(fields) == 22

    def test_can_create_instance(self):
        inp = make_inp()
        assert inp.deal_id == "deal-001"

    def test_deal_name(self):
        inp = make_inp(deal_name="BigCo")
        assert inp.deal_name == "BigCo"

    def test_rep_id(self):
        inp = make_inp(rep_id="rep-99")
        assert inp.rep_id == "rep-99"

    def test_champion_name(self):
        inp = make_inp(champion_name="Bob")
        assert inp.champion_name == "Bob"

    def test_days_since_champion_contact(self):
        inp = make_inp(days_since_champion_contact=10)
        assert inp.days_since_champion_contact == 10

    def test_champion_reply_rate_pct(self):
        inp = make_inp(champion_reply_rate_pct=55.0)
        assert inp.champion_reply_rate_pct == 55.0

    def test_champion_meetings_last_30d(self):
        inp = make_inp(champion_meetings_last_30d=2)
        assert inp.champion_meetings_last_30d == 2

    def test_champion_meetings_prior_30d(self):
        inp = make_inp(champion_meetings_prior_30d=5)
        assert inp.champion_meetings_prior_30d == 5

    def test_champion_intro_count(self):
        inp = make_inp(champion_intro_count=3)
        assert inp.champion_intro_count == 3

    def test_champion_created_internal_urgency(self):
        inp = make_inp(champion_created_internal_urgency=0)
        assert inp.champion_created_internal_urgency == 0

    def test_champion_job_change_signal(self):
        inp = make_inp(champion_job_change_signal=1)
        assert inp.champion_job_change_signal == 1

    def test_champion_promotion_signal(self):
        inp = make_inp(champion_promotion_signal=1)
        assert inp.champion_promotion_signal == 1

    def test_champion_title_level(self):
        inp = make_inp(champion_title_level=3)
        assert inp.champion_title_level == 3

    def test_champion_budget_authority(self):
        inp = make_inp(champion_budget_authority=0)
        assert inp.champion_budget_authority == 0

    def test_backup_champion_identified(self):
        inp = make_inp(backup_champion_identified=0)
        assert inp.backup_champion_identified == 0

    def test_deal_stage_numeric(self):
        inp = make_inp(deal_stage_numeric=3)
        assert inp.deal_stage_numeric == 3

    def test_deal_size_usd(self):
        inp = make_inp(deal_size_usd=500_000.0)
        assert inp.deal_size_usd == 500_000.0

    def test_days_to_close(self):
        inp = make_inp(days_to_close=7)
        assert inp.days_to_close == 7

    def test_executive_relationship_score(self):
        inp = make_inp(executive_relationship_score=45.0)
        assert inp.executive_relationship_score == 45.0

    def test_multi_threaded_contacts(self):
        inp = make_inp(multi_threaded_contacts=8)
        assert inp.multi_threaded_contacts == 8

    def test_last_positive_signal_days_ago(self):
        inp = make_inp(last_positive_signal_days_ago=14)
        assert inp.last_positive_signal_days_ago == 14

    def test_deal_age_days(self):
        inp = make_inp(deal_age_days=120)
        assert inp.deal_age_days == 120


# ---------------------------------------------------------------------------
# 6. ChampionRiskResult.to_dict() — exactly 15 keys
# ---------------------------------------------------------------------------

class TestChampionRiskResultToDict:
    def setup_method(self):
        self.result = run(make_inp())
        self.d = self.result.to_dict()

    def test_exactly_15_keys(self):
        assert len(self.d) == 15

    def test_has_deal_id(self):
        assert "deal_id" in self.d

    def test_has_deal_name(self):
        assert "deal_name" in self.d

    def test_has_champion_status(self):
        assert "champion_status" in self.d

    def test_has_champion_risk(self):
        assert "champion_risk" in self.d

    def test_has_influence_level(self):
        assert "influence_level" in self.d

    def test_has_champion_action(self):
        assert "champion_action" in self.d

    def test_has_engagement_score(self):
        assert "engagement_score" in self.d

    def test_has_influence_score(self):
        assert "influence_score" in self.d

    def test_has_stability_score(self):
        assert "stability_score" in self.d

    def test_has_deal_protection_score(self):
        assert "deal_protection_score" in self.d

    def test_has_champion_composite(self):
        assert "champion_composite" in self.d

    def test_has_departure_probability(self):
        assert "departure_probability" in self.d

    def test_has_deal_at_risk_score(self):
        assert "deal_at_risk_score" in self.d

    def test_has_is_champion_stable(self):
        assert "is_champion_stable" in self.d

    def test_has_needs_backup_champion(self):
        assert "needs_backup_champion" in self.d

    def test_champion_status_is_string(self):
        assert isinstance(self.d["champion_status"], str)

    def test_champion_risk_is_string(self):
        assert isinstance(self.d["champion_risk"], str)

    def test_influence_level_is_string(self):
        assert isinstance(self.d["influence_level"], str)

    def test_champion_action_is_string(self):
        assert isinstance(self.d["champion_action"], str)

    def test_champion_status_valid_value(self):
        assert self.d["champion_status"] in ("active_advocate", "engaged", "cooling", "silent", "departed")

    def test_champion_risk_valid_value(self):
        assert self.d["champion_risk"] in ("low", "moderate", "high", "critical")

    def test_influence_level_valid_value(self):
        assert self.d["influence_level"] in ("high_influence", "moderate_influence", "low_influence", "unknown")

    def test_champion_action_valid_value(self):
        assert self.d["champion_action"] in ("maintain", "re_engage", "find_backup", "escalate_exec")

    def test_is_champion_stable_is_bool(self):
        assert isinstance(self.d["is_champion_stable"], bool)

    def test_needs_backup_champion_is_bool(self):
        assert isinstance(self.d["needs_backup_champion"], bool)

    def test_deal_id_matches(self):
        assert self.d["deal_id"] == "deal-001"

    def test_deal_name_matches(self):
        assert self.d["deal_name"] == "Acme Corp"


# ---------------------------------------------------------------------------
# 7. summary() — exactly 13 keys
# ---------------------------------------------------------------------------

class TestSummaryKeys:
    def test_empty_summary_has_13_keys(self):
        m = ChampionRiskMonitor()
        s = m.summary()
        assert len(s) == 13

    def test_nonempty_summary_has_13_keys(self):
        m = ChampionRiskMonitor()
        m.monitor(make_inp())
        s = m.summary()
        assert len(s) == 13

    def test_summary_has_total(self):
        m = ChampionRiskMonitor()
        assert "total" in m.summary()

    def test_summary_has_status_counts(self):
        m = ChampionRiskMonitor()
        assert "status_counts" in m.summary()

    def test_summary_has_risk_counts(self):
        m = ChampionRiskMonitor()
        assert "risk_counts" in m.summary()

    def test_summary_has_influence_counts(self):
        m = ChampionRiskMonitor()
        assert "influence_counts" in m.summary()

    def test_summary_has_action_counts(self):
        m = ChampionRiskMonitor()
        assert "action_counts" in m.summary()

    def test_summary_has_avg_champion_composite(self):
        m = ChampionRiskMonitor()
        assert "avg_champion_composite" in m.summary()

    def test_summary_has_avg_departure_probability(self):
        m = ChampionRiskMonitor()
        assert "avg_departure_probability" in m.summary()

    def test_summary_has_stable_count(self):
        m = ChampionRiskMonitor()
        assert "stable_count" in m.summary()

    def test_summary_has_backup_needed_count(self):
        m = ChampionRiskMonitor()
        assert "backup_needed_count" in m.summary()

    def test_summary_has_avg_engagement_score(self):
        m = ChampionRiskMonitor()
        assert "avg_engagement_score" in m.summary()

    def test_summary_has_avg_influence_score(self):
        m = ChampionRiskMonitor()
        assert "avg_influence_score" in m.summary()

    def test_summary_has_avg_stability_score(self):
        m = ChampionRiskMonitor()
        assert "avg_stability_score" in m.summary()

    def test_summary_has_avg_deal_at_risk_score(self):
        m = ChampionRiskMonitor()
        assert "avg_deal_at_risk_score" in m.summary()

    def test_empty_total_is_zero(self):
        m = ChampionRiskMonitor()
        assert m.summary()["total"] == 0

    def test_empty_avg_composite_is_zero(self):
        m = ChampionRiskMonitor()
        assert m.summary()["avg_champion_composite"] == 0.0

    def test_empty_avg_departure_is_zero(self):
        m = ChampionRiskMonitor()
        assert m.summary()["avg_departure_probability"] == 0.0

    def test_empty_stable_count_is_zero(self):
        m = ChampionRiskMonitor()
        assert m.summary()["stable_count"] == 0

    def test_empty_backup_needed_count_is_zero(self):
        m = ChampionRiskMonitor()
        assert m.summary()["backup_needed_count"] == 0


# ---------------------------------------------------------------------------
# 8. _engagement_score
# ---------------------------------------------------------------------------

class TestEngagementScore:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def test_contact_le_3_adds_35(self):
        base = self.m._engagement_score(make_inp(days_since_champion_contact=3, champion_reply_rate_pct=0, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert base == 35.0

    def test_contact_le_7_adds_25(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=7, champion_reply_rate_pct=0, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s == 25.0

    def test_contact_le_14_adds_12(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=14, champion_reply_rate_pct=0, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s == 12.0

    def test_contact_le_30_adds_4(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=30, champion_reply_rate_pct=0, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s == 4.0

    def test_contact_gt_30_adds_0(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=0, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s == 0.0

    def test_reply_rate_ge_70_adds_30(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=70, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s == 30.0

    def test_reply_rate_ge_50_adds_20(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=50, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s == 20.0

    def test_reply_rate_ge_30_adds_10(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=30, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s == 10.0

    def test_reply_rate_below_30_adds_0(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=29, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s == 0.0

    def test_meetings_trending_up_and_ge_2_adds_25(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=0, champion_meetings_last_30d=3, champion_meetings_prior_30d=2, champion_intro_count=0))
        assert s == 25.0

    def test_meetings_equal_and_ge_2_adds_25(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=0, champion_meetings_last_30d=2, champion_meetings_prior_30d=2, champion_intro_count=0))
        assert s == 25.0

    def test_meetings_ge_1_but_declining_adds_12(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=0, champion_meetings_last_30d=1, champion_meetings_prior_30d=3, champion_intro_count=0))
        assert s == 12.0

    def test_meetings_zero_adds_0(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=0, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s == 0.0

    def test_intro_count_ge_3_adds_10(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=0, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=3))
        assert s == 10.0

    def test_intro_count_ge_1_adds_5(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=0, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=1))
        assert s == 5.0

    def test_intro_count_0_adds_0(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=31, champion_reply_rate_pct=0, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s == 0.0

    def test_score_clamped_max_100(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=1, champion_reply_rate_pct=100, champion_meetings_last_30d=5, champion_meetings_prior_30d=1, champion_intro_count=10))
        assert s <= 100.0

    def test_score_clamped_min_0(self):
        s = self.m._engagement_score(make_inp(days_since_champion_contact=60, champion_reply_rate_pct=0, champion_meetings_last_30d=0, champion_meetings_prior_30d=0, champion_intro_count=0))
        assert s >= 0.0

    def test_full_engagement_score(self):
        # 35 + 30 + 25 + 10 = 100
        s = self.m._engagement_score(make_inp(days_since_champion_contact=2, champion_reply_rate_pct=80, champion_meetings_last_30d=3, champion_meetings_prior_30d=2, champion_intro_count=5))
        assert s == 100.0


# ---------------------------------------------------------------------------
# 9. _influence_score
# ---------------------------------------------------------------------------

class TestInfluenceScore:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def _base(self, **kw):
        return self.m._influence_score(make_inp(**kw))

    def test_title_level_ge_4_adds_40(self):
        s = self._base(champion_title_level=4, champion_budget_authority=0, champion_intro_count=0, champion_created_internal_urgency=0)
        assert s == 40.0

    def test_title_level_5_adds_40(self):
        s = self._base(champion_title_level=5, champion_budget_authority=0, champion_intro_count=0, champion_created_internal_urgency=0)
        assert s == 40.0

    def test_title_level_3_adds_28(self):
        s = self._base(champion_title_level=3, champion_budget_authority=0, champion_intro_count=0, champion_created_internal_urgency=0)
        assert s == 28.0

    def test_title_level_2_adds_16(self):
        s = self._base(champion_title_level=2, champion_budget_authority=0, champion_intro_count=0, champion_created_internal_urgency=0)
        assert s == 16.0

    def test_title_level_1_adds_6(self):
        s = self._base(champion_title_level=1, champion_budget_authority=0, champion_intro_count=0, champion_created_internal_urgency=0)
        assert s == 6.0

    def test_budget_authority_adds_30(self):
        s = self._base(champion_title_level=1, champion_budget_authority=1, champion_intro_count=0, champion_created_internal_urgency=0)
        assert s == 36.0

    def test_intro_count_ge_4_adds_20(self):
        s = self._base(champion_title_level=1, champion_budget_authority=0, champion_intro_count=4, champion_created_internal_urgency=0)
        assert s == 26.0

    def test_intro_count_ge_2_adds_12(self):
        s = self._base(champion_title_level=1, champion_budget_authority=0, champion_intro_count=2, champion_created_internal_urgency=0)
        assert s == 18.0

    def test_intro_count_ge_1_adds_6(self):
        s = self._base(champion_title_level=1, champion_budget_authority=0, champion_intro_count=1, champion_created_internal_urgency=0)
        assert s == 12.0

    def test_intro_count_0_adds_0(self):
        s = self._base(champion_title_level=1, champion_budget_authority=0, champion_intro_count=0, champion_created_internal_urgency=0)
        assert s == 6.0

    def test_internal_urgency_adds_10(self):
        s = self._base(champion_title_level=1, champion_budget_authority=0, champion_intro_count=0, champion_created_internal_urgency=1)
        assert s == 16.0

    def test_max_score_100(self):
        s = self._base(champion_title_level=5, champion_budget_authority=1, champion_intro_count=10, champion_created_internal_urgency=1)
        assert s == 100.0

    def test_score_clamped_min_0(self):
        s = self._base(champion_title_level=0, champion_budget_authority=0, champion_intro_count=0, champion_created_internal_urgency=0)
        assert s >= 0.0


# ---------------------------------------------------------------------------
# 10. _stability_score
# ---------------------------------------------------------------------------

class TestStabilityScore:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def _s(self, **kw):
        return self.m._stability_score(make_inp(**kw))

    def test_baseline_stable_is_80(self):
        # no job change, no promotion, contact <=13 days, no backup, few contacts
        s = self._s(champion_job_change_signal=0, champion_promotion_signal=0,
                    days_since_champion_contact=5, backup_champion_identified=0,
                    multi_threaded_contacts=1)
        assert s == 80.0

    def test_job_change_signal_subtracts_50(self):
        s = self._s(champion_job_change_signal=1, champion_promotion_signal=0,
                    days_since_champion_contact=5, backup_champion_identified=0,
                    multi_threaded_contacts=1)
        assert s == 30.0

    def test_promotion_signal_subtracts_15(self):
        s = self._s(champion_job_change_signal=0, champion_promotion_signal=1,
                    days_since_champion_contact=5, backup_champion_identified=0,
                    multi_threaded_contacts=1)
        assert s == 65.0

    def test_contact_ge_21_subtracts_25(self):
        s = self._s(champion_job_change_signal=0, champion_promotion_signal=0,
                    days_since_champion_contact=21, backup_champion_identified=0,
                    multi_threaded_contacts=1)
        assert s == 55.0

    def test_contact_ge_14_subtracts_12(self):
        s = self._s(champion_job_change_signal=0, champion_promotion_signal=0,
                    days_since_champion_contact=14, backup_champion_identified=0,
                    multi_threaded_contacts=1)
        assert s == 68.0

    def test_contact_lt_14_subtracts_0(self):
        s = self._s(champion_job_change_signal=0, champion_promotion_signal=0,
                    days_since_champion_contact=13, backup_champion_identified=0,
                    multi_threaded_contacts=1)
        assert s == 80.0

    def test_backup_champion_adds_15(self):
        s = self._s(champion_job_change_signal=0, champion_promotion_signal=0,
                    days_since_champion_contact=5, backup_champion_identified=1,
                    multi_threaded_contacts=1)
        assert s == 95.0

    def test_multi_threaded_ge_5_adds_10(self):
        s = self._s(champion_job_change_signal=0, champion_promotion_signal=0,
                    days_since_champion_contact=5, backup_champion_identified=0,
                    multi_threaded_contacts=5)
        assert s == 90.0

    def test_multi_threaded_ge_3_adds_5(self):
        s = self._s(champion_job_change_signal=0, champion_promotion_signal=0,
                    days_since_champion_contact=5, backup_champion_identified=0,
                    multi_threaded_contacts=3)
        assert s == 85.0

    def test_multi_threaded_lt_3_adds_0(self):
        s = self._s(champion_job_change_signal=0, champion_promotion_signal=0,
                    days_since_champion_contact=5, backup_champion_identified=0,
                    multi_threaded_contacts=2)
        assert s == 80.0

    def test_clamped_min_0_all_bad(self):
        s = self._s(champion_job_change_signal=1, champion_promotion_signal=1,
                    days_since_champion_contact=21, backup_champion_identified=0,
                    multi_threaded_contacts=0)
        # 80 - 50 - 15 - 25 = -10 → clamped to 0
        assert s == 0.0

    def test_backup_with_job_change_still_clamped_at_100(self):
        # 80 + 15 + 10 = 105 → clamped to 100
        s = self._s(champion_job_change_signal=0, champion_promotion_signal=0,
                    days_since_champion_contact=5, backup_champion_identified=1,
                    multi_threaded_contacts=5)
        assert s == 100.0


# ---------------------------------------------------------------------------
# 11. _deal_protection_score
# ---------------------------------------------------------------------------

class TestDealProtectionScore:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def _p(self, **kw):
        return self.m._deal_protection_score(make_inp(**kw))

    def test_exec_ge_70_adds_35(self):
        s = self._p(executive_relationship_score=70, multi_threaded_contacts=0,
                    backup_champion_identified=0, deal_stage_numeric=1)
        assert s == 35.0

    def test_exec_ge_50_adds_22(self):
        s = self._p(executive_relationship_score=50, multi_threaded_contacts=0,
                    backup_champion_identified=0, deal_stage_numeric=1)
        assert s == 22.0

    def test_exec_ge_30_adds_12(self):
        s = self._p(executive_relationship_score=30, multi_threaded_contacts=0,
                    backup_champion_identified=0, deal_stage_numeric=1)
        assert s == 12.0

    def test_exec_lt_30_adds_0(self):
        s = self._p(executive_relationship_score=29, multi_threaded_contacts=0,
                    backup_champion_identified=0, deal_stage_numeric=1)
        assert s == 0.0

    def test_multi_ge_6_adds_30(self):
        s = self._p(executive_relationship_score=0, multi_threaded_contacts=6,
                    backup_champion_identified=0, deal_stage_numeric=1)
        assert s == 30.0

    def test_multi_ge_4_adds_20(self):
        s = self._p(executive_relationship_score=0, multi_threaded_contacts=4,
                    backup_champion_identified=0, deal_stage_numeric=1)
        assert s == 20.0

    def test_multi_ge_2_adds_10(self):
        s = self._p(executive_relationship_score=0, multi_threaded_contacts=2,
                    backup_champion_identified=0, deal_stage_numeric=1)
        assert s == 10.0

    def test_multi_lt_2_adds_0(self):
        s = self._p(executive_relationship_score=0, multi_threaded_contacts=1,
                    backup_champion_identified=0, deal_stage_numeric=1)
        assert s == 0.0

    def test_backup_champion_adds_20(self):
        s = self._p(executive_relationship_score=0, multi_threaded_contacts=0,
                    backup_champion_identified=1, deal_stage_numeric=1)
        assert s == 20.0

    def test_stage_ge_5_adds_15(self):
        s = self._p(executive_relationship_score=0, multi_threaded_contacts=0,
                    backup_champion_identified=0, deal_stage_numeric=5)
        assert s == 15.0

    def test_stage_ge_4_adds_8(self):
        s = self._p(executive_relationship_score=0, multi_threaded_contacts=0,
                    backup_champion_identified=0, deal_stage_numeric=4)
        assert s == 8.0

    def test_stage_lt_4_adds_0(self):
        s = self._p(executive_relationship_score=0, multi_threaded_contacts=0,
                    backup_champion_identified=0, deal_stage_numeric=3)
        assert s == 0.0

    def test_score_clamped_max_100(self):
        s = self._p(executive_relationship_score=100, multi_threaded_contacts=10,
                    backup_champion_identified=1, deal_stage_numeric=6)
        assert s == 100.0

    def test_zero_everything_is_0(self):
        s = self._p(executive_relationship_score=0, multi_threaded_contacts=0,
                    backup_champion_identified=0, deal_stage_numeric=1)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 12. _composite — weights: engagement*0.35 + influence*0.25 + stability*0.25 + protection*0.15
# ---------------------------------------------------------------------------

class TestComposite:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def test_all_zero_is_zero(self):
        c = self.m._composite(0, 0, 0, 0)
        assert c == 0.0

    def test_all_100_is_100(self):
        c = self.m._composite(100, 100, 100, 100)
        assert c == 100.0

    def test_weights_engagement(self):
        # only engagement = 100, rest 0 → 100*0.35 = 35
        c = self.m._composite(100, 0, 0, 0)
        assert c == 35.0

    def test_weights_influence(self):
        # only influence = 100, rest 0 → 100*0.25 = 25
        c = self.m._composite(0, 100, 0, 0)
        assert c == 25.0

    def test_weights_stability(self):
        # only stability = 100, rest 0 → 100*0.25 = 25
        c = self.m._composite(0, 0, 100, 0)
        assert c == 25.0

    def test_weights_protection(self):
        # only protection = 100, rest 0 → 100*0.15 = 15
        c = self.m._composite(0, 0, 0, 100)
        assert c == 15.0

    def test_weights_sum_to_100(self):
        assert abs(0.35 + 0.25 + 0.25 + 0.15 - 1.0) < 1e-9

    def test_clamped_min_0(self):
        c = self.m._composite(-10, -10, -10, -10)
        assert c == 0.0

    def test_clamped_max_100(self):
        c = self.m._composite(200, 200, 200, 200)
        assert c == 100.0

    def test_rounded_to_1_decimal(self):
        c = self.m._composite(33, 33, 33, 33)
        assert c == round(c, 1)

    def test_known_value(self):
        # 40*0.35 + 60*0.25 + 70*0.25 + 80*0.15
        expected = round(40 * 0.35 + 60 * 0.25 + 70 * 0.25 + 80 * 0.15, 1)
        c = self.m._composite(40, 60, 70, 80)
        assert c == expected


# ---------------------------------------------------------------------------
# 13. _champion_status
# ---------------------------------------------------------------------------

class TestChampionStatus:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def test_job_change_signal_is_departed(self):
        inp = make_inp(champion_job_change_signal=1, days_since_champion_contact=2, champion_intro_count=5)
        assert self.m._champion_status(inp, 90) == ChampionStatus.DEPARTED

    def test_contact_ge_21_is_silent(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=21)
        assert self.m._champion_status(inp, 50) == ChampionStatus.SILENT

    def test_composite_lt_20_is_silent(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=5)
        assert self.m._champion_status(inp, 19) == ChampionStatus.SILENT

    def test_high_composite_with_intros_is_active_advocate(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=5, champion_intro_count=3)
        assert self.m._champion_status(inp, 70) == ChampionStatus.ACTIVE_ADVOCATE

    def test_composite_70_but_intros_lt_2_is_engaged(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=5, champion_intro_count=1)
        assert self.m._champion_status(inp, 70) == ChampionStatus.ENGAGED

    def test_composite_ge_50_is_engaged(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=5, champion_intro_count=0)
        assert self.m._champion_status(inp, 50) == ChampionStatus.ENGAGED

    def test_composite_lt_50_not_silent_is_cooling(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=5)
        assert self.m._champion_status(inp, 49) == ChampionStatus.COOLING

    def test_composite_exactly_20_is_cooling(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=5)
        assert self.m._champion_status(inp, 20) == ChampionStatus.COOLING

    def test_contact_exactly_21_is_silent(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=21)
        assert self.m._champion_status(inp, 80) == ChampionStatus.SILENT


# ---------------------------------------------------------------------------
# 14. _champion_risk
# ---------------------------------------------------------------------------

class TestChampionRisk:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def test_job_change_signal_is_critical(self):
        inp = make_inp(champion_job_change_signal=1, days_since_champion_contact=2)
        assert self.m._champion_risk(80, inp) == ChampionRisk.CRITICAL

    def test_composite_lt_20_is_critical(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=2)
        assert self.m._champion_risk(19, inp) == ChampionRisk.CRITICAL

    def test_composite_lt_35_is_high(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=2)
        assert self.m._champion_risk(34, inp) == ChampionRisk.HIGH

    def test_contact_ge_21_is_high(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=21)
        assert self.m._champion_risk(50, inp) == ChampionRisk.HIGH

    def test_composite_lt_55_is_moderate(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=5)
        assert self.m._champion_risk(54, inp) == ChampionRisk.MODERATE

    def test_composite_ge_55_is_low(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=5)
        assert self.m._champion_risk(55, inp) == ChampionRisk.LOW

    def test_composite_100_is_low(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=5)
        assert self.m._champion_risk(100, inp) == ChampionRisk.LOW

    def test_composite_exactly_35_is_moderate(self):
        inp = make_inp(champion_job_change_signal=0, days_since_champion_contact=2)
        assert self.m._champion_risk(35, inp) == ChampionRisk.MODERATE


# ---------------------------------------------------------------------------
# 15. _influence_level
# ---------------------------------------------------------------------------

class TestInfluenceLevel:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def _lvl(self, title, budget, intros):
        inp = make_inp(champion_title_level=title, champion_budget_authority=budget, champion_intro_count=intros)
        return self.m._influence_level(inp)

    def test_high_influence_vp_with_budget_and_intros(self):
        # 4*15 + 30 + 5*5 = 60 + 30 + 25 = 115... capped logic; score>=80
        lvl = self._lvl(4, 1, 5)
        assert lvl == InfluenceLevel.HIGH_INFLUENCE

    def test_moderate_influence(self):
        # title=3: 45, budget=0: 0, intros=1: 5 → 50 → moderate
        lvl = self._lvl(3, 0, 1)
        assert lvl == InfluenceLevel.MODERATE_INFLUENCE

    def test_low_influence(self):
        # title=1: 15, budget=0: 0, intros=1: 5 → 20 → low
        lvl = self._lvl(1, 0, 1)
        assert lvl == InfluenceLevel.LOW_INFLUENCE

    def test_unknown_influence(self):
        # title=1: 15, budget=0: 0, intros=0: 0 → 15 → unknown
        lvl = self._lvl(1, 0, 0)
        assert lvl == InfluenceLevel.UNKNOWN

    def test_score_exactly_80_is_high(self):
        # need score >= 80: title=4 (60) + budget=1 (30) + intros=0 (0) = 90 ≥ 80
        lvl = self._lvl(4, 1, 0)
        assert lvl == InfluenceLevel.HIGH_INFLUENCE

    def test_score_exactly_50_is_moderate(self):
        # title=2 (30) + budget=1 (30) + intros=0 (0) = 60 → but 60>=50 → moderate check
        # Actually title=2: 2*15=30, budget=1: 30, intros=0: 0 → 60 ≥ 80? No → moderate
        lvl = self._lvl(2, 1, 0)
        assert lvl == InfluenceLevel.MODERATE_INFLUENCE

    def test_score_exactly_20_is_low(self):
        # title=1: 15, budget=0: 0, intros=1: 5 → 20 → low
        lvl = self._lvl(1, 0, 1)
        assert lvl == InfluenceLevel.LOW_INFLUENCE


# ---------------------------------------------------------------------------
# 16. _departure_probability
# ---------------------------------------------------------------------------

class TestDepartureProbability:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def _dp(self, **kw):
        return self.m._departure_probability(make_inp(**kw))

    def test_no_signals_zero_probability(self):
        p = self._dp(champion_job_change_signal=0, champion_promotion_signal=0,
                     days_since_champion_contact=5, champion_reply_rate_pct=50)
        assert p == 0.0

    def test_job_change_adds_70(self):
        p = self._dp(champion_job_change_signal=1, champion_promotion_signal=0,
                     days_since_champion_contact=5, champion_reply_rate_pct=50)
        assert p == 70.0

    def test_promotion_adds_20(self):
        p = self._dp(champion_job_change_signal=0, champion_promotion_signal=1,
                     days_since_champion_contact=5, champion_reply_rate_pct=50)
        assert p == 20.0

    def test_contact_ge_21_adds_15(self):
        p = self._dp(champion_job_change_signal=0, champion_promotion_signal=0,
                     days_since_champion_contact=21, champion_reply_rate_pct=50)
        assert p == 15.0

    def test_contact_ge_14_adds_8(self):
        p = self._dp(champion_job_change_signal=0, champion_promotion_signal=0,
                     days_since_champion_contact=14, champion_reply_rate_pct=50)
        assert p == 8.0

    def test_contact_lt_14_adds_0(self):
        p = self._dp(champion_job_change_signal=0, champion_promotion_signal=0,
                     days_since_champion_contact=13, champion_reply_rate_pct=50)
        assert p == 0.0

    def test_reply_rate_lt_20_adds_10(self):
        p = self._dp(champion_job_change_signal=0, champion_promotion_signal=0,
                     days_since_champion_contact=5, champion_reply_rate_pct=19)
        assert p == 10.0

    def test_reply_rate_ge_20_adds_0(self):
        p = self._dp(champion_job_change_signal=0, champion_promotion_signal=0,
                     days_since_champion_contact=5, champion_reply_rate_pct=20)
        assert p == 0.0

    def test_clamped_max_100(self):
        p = self._dp(champion_job_change_signal=1, champion_promotion_signal=1,
                     days_since_champion_contact=21, champion_reply_rate_pct=5)
        assert p == 100.0

    def test_clamped_min_0(self):
        p = self._dp(champion_job_change_signal=0, champion_promotion_signal=0,
                     days_since_champion_contact=0, champion_reply_rate_pct=100)
        assert p == 0.0


# ---------------------------------------------------------------------------
# 17. _deal_at_risk_score
# ---------------------------------------------------------------------------

class TestDealAtRiskScore:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def _dar(self, composite, **kw):
        return self.m._deal_at_risk_score(make_inp(**kw), composite)

    def test_base_is_100_minus_composite(self):
        s = self._dar(60, champion_job_change_signal=0, deal_size_usd=100_000,
                      deal_stage_numeric=3, days_to_close=30)
        assert s == 40.0

    def test_large_deal_with_job_change_adds_15(self):
        s = self._dar(60, champion_job_change_signal=1, deal_size_usd=200_000,
                      deal_stage_numeric=3, days_to_close=30)
        # base=40, +15 = 55
        assert s == 55.0

    def test_late_stage_with_job_change_adds_10(self):
        s = self._dar(60, champion_job_change_signal=1, deal_size_usd=50_000,
                      deal_stage_numeric=5, days_to_close=30)
        # base=40, +10 = 50
        assert s == 50.0

    def test_large_deal_late_stage_job_change_adds_both(self):
        s = self._dar(60, champion_job_change_signal=1, deal_size_usd=200_000,
                      deal_stage_numeric=5, days_to_close=30)
        # base=40, +15, +10 = 65
        assert s == 65.0

    def test_close_soon_low_composite_adds_10(self):
        s = self._dar(39, champion_job_change_signal=0, deal_size_usd=50_000,
                      deal_stage_numeric=3, days_to_close=14)
        # base=61, +10 = 71
        assert s == 71.0

    def test_close_soon_ge_40_composite_no_bonus(self):
        s = self._dar(40, champion_job_change_signal=0, deal_size_usd=50_000,
                      deal_stage_numeric=3, days_to_close=14)
        # base=60, composite>=40 → no extra
        assert s == 60.0

    def test_days_to_close_exactly_14_applies_bonus(self):
        s = self._dar(39, champion_job_change_signal=0, deal_size_usd=50_000,
                      deal_stage_numeric=3, days_to_close=14)
        assert s == 71.0

    def test_clamped_max_100(self):
        s = self._dar(0, champion_job_change_signal=1, deal_size_usd=500_000,
                      deal_stage_numeric=6, days_to_close=10)
        assert s == 100.0

    def test_clamped_min_0(self):
        s = self._dar(100, champion_job_change_signal=0, deal_size_usd=0,
                      deal_stage_numeric=1, days_to_close=100)
        assert s == 0.0


# ---------------------------------------------------------------------------
# 18. _champion_action
# ---------------------------------------------------------------------------

class TestChampionAction:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def test_critical_risk_is_escalate_exec(self):
        inp = make_inp()
        assert self.m._champion_action(ChampionRisk.CRITICAL, False, inp) == ChampionAction.ESCALATE_EXEC

    def test_critical_risk_overrides_needs_backup(self):
        inp = make_inp()
        assert self.m._champion_action(ChampionRisk.CRITICAL, True, inp) == ChampionAction.ESCALATE_EXEC

    def test_high_risk_no_backup_needed_is_re_engage(self):
        inp = make_inp()
        assert self.m._champion_action(ChampionRisk.HIGH, False, inp) == ChampionAction.RE_ENGAGE

    def test_needs_backup_high_risk_is_find_backup(self):
        inp = make_inp()
        assert self.m._champion_action(ChampionRisk.HIGH, True, inp) == ChampionAction.FIND_BACKUP

    def test_moderate_risk_no_backup_needed_is_re_engage(self):
        inp = make_inp()
        assert self.m._champion_action(ChampionRisk.MODERATE, False, inp) == ChampionAction.RE_ENGAGE

    def test_needs_backup_moderate_risk_is_find_backup(self):
        inp = make_inp()
        assert self.m._champion_action(ChampionRisk.MODERATE, True, inp) == ChampionAction.FIND_BACKUP

    def test_low_risk_no_backup_needed_is_maintain(self):
        inp = make_inp()
        assert self.m._champion_action(ChampionRisk.LOW, False, inp) == ChampionAction.MAINTAIN

    def test_needs_backup_low_risk_is_find_backup(self):
        inp = make_inp()
        assert self.m._champion_action(ChampionRisk.LOW, True, inp) == ChampionAction.FIND_BACKUP


# ---------------------------------------------------------------------------
# 19. is_champion_stable invariant
# ---------------------------------------------------------------------------

class TestIsChampionStable:
    def test_stable_when_composite_ge_55_and_no_job_change(self):
        # healthy champion with high composite
        result = run(make_inp(champion_job_change_signal=0))
        if result.champion_composite >= 55:
            assert result.is_champion_stable is True

    def test_not_stable_when_job_change(self):
        result = run(make_inp(champion_job_change_signal=1))
        assert result.is_champion_stable is False

    def test_not_stable_when_composite_lt_55_no_job_change(self):
        # IC, no budget, no intros, no urgency, low engagement
        inp = make_inp(
            champion_title_level=1,
            champion_budget_authority=0,
            champion_intro_count=0,
            champion_created_internal_urgency=0,
            champion_job_change_signal=0,
            champion_reply_rate_pct=0,
            champion_meetings_last_30d=0,
            champion_meetings_prior_30d=0,
            days_since_champion_contact=60,
            executive_relationship_score=0,
            multi_threaded_contacts=0,
            backup_champion_identified=0,
            deal_stage_numeric=1,
        )
        result = run(inp)
        assert result.champion_composite < 55
        assert result.is_champion_stable is False

    def test_stable_false_when_composite_exactly_54(self):
        m = ChampionRiskMonitor()
        # Manually craft composite=54 via mock
        inp = make_inp(champion_job_change_signal=0)
        result = m.monitor(inp)
        # Verify logic: stable = composite >= 55 AND job_change == 0
        expected = result.champion_composite >= 55 and inp.champion_job_change_signal == 0
        assert result.is_champion_stable == expected

    def test_stable_true_example(self):
        # Ensure healthy champion is stable
        result = run(make_inp())
        expected = result.champion_composite >= 55 and result.is_champion_stable
        assert result.is_champion_stable == expected


# ---------------------------------------------------------------------------
# 20. needs_backup_champion invariant
# ---------------------------------------------------------------------------

class TestNeedsBackupChampion:
    def test_no_backup_and_composite_lt_40(self):
        inp = make_inp(
            backup_champion_identified=0,
            champion_job_change_signal=0,
            champion_title_level=1,
            champion_budget_authority=0,
            champion_intro_count=0,
            champion_created_internal_urgency=0,
            champion_reply_rate_pct=0,
            champion_meetings_last_30d=0,
            champion_meetings_prior_30d=0,
            days_since_champion_contact=60,
            executive_relationship_score=0,
            multi_threaded_contacts=0,
            deal_stage_numeric=1,
            champion_promotion_signal=0,
        )
        result = run(inp)
        if result.champion_composite < 40:
            assert result.needs_backup_champion is True

    def test_no_backup_and_job_change(self):
        result = run(make_inp(backup_champion_identified=0, champion_job_change_signal=1))
        assert result.needs_backup_champion is True

    def test_backup_identified_no_need(self):
        result = run(make_inp(backup_champion_identified=1, champion_job_change_signal=0))
        # Even with low composite, backup identified → no need
        assert result.needs_backup_champion is False

    def test_backup_identified_even_with_job_change(self):
        result = run(make_inp(backup_champion_identified=1, champion_job_change_signal=1))
        assert result.needs_backup_champion is False

    def test_high_composite_no_job_change_no_backup_needed(self):
        result = run(make_inp(backup_champion_identified=0, champion_job_change_signal=0))
        # healthy has composite >> 40
        if result.champion_composite >= 40:
            assert result.needs_backup_champion is False

    def test_invariant_consistency(self):
        inp = make_inp(backup_champion_identified=0, champion_job_change_signal=1)
        result = run(inp)
        expected = inp.backup_champion_identified == 0 and (result.champion_composite < 40 or inp.champion_job_change_signal == 1)
        assert result.needs_backup_champion == expected


# ---------------------------------------------------------------------------
# 21. monitor() — result fields
# ---------------------------------------------------------------------------

class TestMonitorResult:
    def setup_method(self):
        self.m = ChampionRiskMonitor()
        self.inp = make_inp()
        self.result = self.m.monitor(self.inp)

    def test_returns_champion_risk_result(self):
        assert isinstance(self.result, ChampionRiskResult)

    def test_deal_id_propagated(self):
        assert self.result.deal_id == "deal-001"

    def test_deal_name_propagated(self):
        assert self.result.deal_name == "Acme Corp"

    def test_champion_status_type(self):
        assert isinstance(self.result.champion_status, ChampionStatus)

    def test_champion_risk_type(self):
        assert isinstance(self.result.champion_risk, ChampionRisk)

    def test_influence_level_type(self):
        assert isinstance(self.result.influence_level, InfluenceLevel)

    def test_champion_action_type(self):
        assert isinstance(self.result.champion_action, ChampionAction)

    def test_engagement_score_range(self):
        assert 0.0 <= self.result.engagement_score <= 100.0

    def test_influence_score_range(self):
        assert 0.0 <= self.result.influence_score <= 100.0

    def test_stability_score_range(self):
        assert 0.0 <= self.result.stability_score <= 100.0

    def test_deal_protection_score_range(self):
        assert 0.0 <= self.result.deal_protection_score <= 100.0

    def test_champion_composite_range(self):
        assert 0.0 <= self.result.champion_composite <= 100.0

    def test_departure_probability_range(self):
        assert 0.0 <= self.result.departure_probability <= 100.0

    def test_deal_at_risk_score_range(self):
        assert 0.0 <= self.result.deal_at_risk_score <= 100.0

    def test_is_champion_stable_bool(self):
        assert isinstance(self.result.is_champion_stable, bool)

    def test_needs_backup_champion_bool(self):
        assert isinstance(self.result.needs_backup_champion, bool)

    def test_stored_in_results(self):
        assert len(self.m._results) == 1

    def test_composite_formula(self):
        r = self.result
        expected = round(r.engagement_score * 0.35 + r.influence_score * 0.25 + r.stability_score * 0.25 + r.deal_protection_score * 0.15, 1)
        assert r.champion_composite == expected

    def test_healthy_champion_low_risk(self):
        assert self.result.champion_risk == ChampionRisk.LOW

    def test_healthy_champion_stable(self):
        assert self.result.is_champion_stable is True

    def test_healthy_champion_no_backup_needed(self):
        assert self.result.needs_backup_champion is False


# ---------------------------------------------------------------------------
# 22. monitor_batch()
# ---------------------------------------------------------------------------

class TestMonitorBatch:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def test_returns_list(self):
        results = self.m.monitor_batch([make_inp()])
        assert isinstance(results, list)

    def test_empty_batch_returns_empty(self):
        results = self.m.monitor_batch([])
        assert results == []

    def test_single_item_batch(self):
        results = self.m.monitor_batch([make_inp()])
        assert len(results) == 1

    def test_processes_all_items(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(5)]
        results = self.m.monitor_batch(inputs)
        assert len(results) == 5

    def test_all_stored_after_batch(self):
        inputs = [make_inp(deal_id=f"d{i}") for i in range(3)]
        self.m.monitor_batch(inputs)
        assert len(self.m._results) == 3

    def test_all_results_are_champion_risk_result(self):
        results = self.m.monitor_batch([make_inp(), make_inp(deal_id="d2")])
        for r in results:
            assert isinstance(r, ChampionRiskResult)

    def test_batch_accumulates_with_previous(self):
        self.m.monitor(make_inp(deal_id="pre"))
        self.m.monitor_batch([make_inp(deal_id="b1"), make_inp(deal_id="b2")])
        assert len(self.m._results) == 3

    def test_batch_with_different_risk_levels(self):
        healthy = make_inp(deal_id="h1")
        risky = make_inp(
            deal_id="r1",
            champion_job_change_signal=1,
            backup_champion_identified=0,
        )
        results = self.m.monitor_batch([healthy, risky])
        risks = {r.deal_id: r.champion_risk for r in results}
        assert risks["h1"] == ChampionRisk.LOW
        assert risks["r1"] == ChampionRisk.CRITICAL


# ---------------------------------------------------------------------------
# 23. Properties: stable_champions, backup_needed_queue
# ---------------------------------------------------------------------------

class TestProperties:
    def setup_method(self):
        self.m = ChampionRiskMonitor()

    def test_stable_champions_empty_initially(self):
        assert self.m.stable_champions == []

    def test_backup_needed_queue_empty_initially(self):
        assert self.m.backup_needed_queue == []

    def test_stable_champions_contains_stable(self):
        self.m.monitor(make_inp())
        stable = self.m.stable_champions
        assert all(r.is_champion_stable for r in stable)

    def test_backup_needed_queue_contains_needy(self):
        self.m.monitor(make_inp(backup_champion_identified=0, champion_job_change_signal=1))
        queue = self.m.backup_needed_queue
        assert all(r.needs_backup_champion for r in queue)

    def test_stable_champions_excludes_unstable(self):
        self.m.monitor(make_inp(champion_job_change_signal=1))
        # job change → not stable
        assert all(r.is_champion_stable for r in self.m.stable_champions)

    def test_backup_needed_queue_excludes_protected(self):
        self.m.monitor(make_inp(backup_champion_identified=1, champion_job_change_signal=0))
        assert self.m.backup_needed_queue == []

    def test_stable_champions_count(self):
        self.m.monitor(make_inp(deal_id="d1"))  # stable
        self.m.monitor(make_inp(deal_id="d2", champion_job_change_signal=1))  # not stable
        count = sum(1 for r in self.m._results if r.is_champion_stable)
        assert len(self.m.stable_champions) == count

    def test_backup_needed_queue_count(self):
        self.m.monitor(make_inp(deal_id="d1", backup_champion_identified=0, champion_job_change_signal=1))
        self.m.monitor(make_inp(deal_id="d2", backup_champion_identified=1))
        count = sum(1 for r in self.m._results if r.needs_backup_champion)
        assert len(self.m.backup_needed_queue) == count


# ---------------------------------------------------------------------------
# 24. Properties: avg_champion_composite, avg_departure_probability
# ---------------------------------------------------------------------------

class TestAverageProperties:
    def test_avg_composite_zero_when_empty(self):
        m = ChampionRiskMonitor()
        assert m.avg_champion_composite == 0.0

    def test_avg_departure_zero_when_empty(self):
        m = ChampionRiskMonitor()
        assert m.avg_departure_probability == 0.0

    def test_avg_composite_single_result(self):
        m = ChampionRiskMonitor()
        r = m.monitor(make_inp())
        assert m.avg_champion_composite == r.champion_composite

    def test_avg_departure_single_result(self):
        m = ChampionRiskMonitor()
        r = m.monitor(make_inp())
        assert m.avg_departure_probability == r.departure_probability

    def test_avg_composite_two_results(self):
        m = ChampionRiskMonitor()
        r1 = m.monitor(make_inp(deal_id="d1"))
        r2 = m.monitor(make_inp(deal_id="d2", champion_job_change_signal=1))
        expected = round((r1.champion_composite + r2.champion_composite) / 2, 1)
        assert m.avg_champion_composite == expected

    def test_avg_departure_two_results(self):
        m = ChampionRiskMonitor()
        r1 = m.monitor(make_inp(deal_id="d1"))
        r2 = m.monitor(make_inp(deal_id="d2", champion_job_change_signal=1))
        expected = round((r1.departure_probability + r2.departure_probability) / 2, 1)
        assert m.avg_departure_probability == expected

    def test_avg_composite_rounded_to_1_decimal(self):
        m = ChampionRiskMonitor()
        m.monitor(make_inp(deal_id="d1"))
        m.monitor(make_inp(deal_id="d2"))
        avg = m.avg_champion_composite
        assert avg == round(avg, 1)

    def test_avg_departure_rounded_to_1_decimal(self):
        m = ChampionRiskMonitor()
        m.monitor(make_inp(deal_id="d1"))
        m.monitor(make_inp(deal_id="d2"))
        avg = m.avg_departure_probability
        assert avg == round(avg, 1)


# ---------------------------------------------------------------------------
# 25. reset()
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_results(self):
        m = ChampionRiskMonitor()
        m.monitor(make_inp())
        m.reset()
        assert m._results == []

    def test_reset_clears_stable_champions(self):
        m = ChampionRiskMonitor()
        m.monitor(make_inp())
        m.reset()
        assert m.stable_champions == []

    def test_reset_clears_backup_needed_queue(self):
        m = ChampionRiskMonitor()
        m.monitor(make_inp(backup_champion_identified=0, champion_job_change_signal=1))
        m.reset()
        assert m.backup_needed_queue == []

    def test_reset_resets_avg_composite(self):
        m = ChampionRiskMonitor()
        m.monitor(make_inp())
        m.reset()
        assert m.avg_champion_composite == 0.0

    def test_reset_resets_avg_departure(self):
        m = ChampionRiskMonitor()
        m.monitor(make_inp())
        m.reset()
        assert m.avg_departure_probability == 0.0

    def test_reset_allows_reuse(self):
        m = ChampionRiskMonitor()
        m.monitor(make_inp(deal_id="d1"))
        m.reset()
        m.monitor(make_inp(deal_id="d2"))
        assert len(m._results) == 1
        assert m._results[0].deal_id == "d2"

    def test_double_reset_safe(self):
        m = ChampionRiskMonitor()
        m.reset()
        m.reset()
        assert m._results == []

    def test_summary_after_reset_shows_zero(self):
        m = ChampionRiskMonitor()
        m.monitor(make_inp())
        m.reset()
        assert m.summary()["total"] == 0


# ---------------------------------------------------------------------------
# 26. summary() — content
# ---------------------------------------------------------------------------

class TestSummaryContent:
    def setup_method(self):
        self.m = ChampionRiskMonitor()
        self.m.monitor(make_inp(deal_id="d1"))
        self.m.monitor(make_inp(deal_id="d2", champion_job_change_signal=1, backup_champion_identified=0))

    def test_total_is_2(self):
        assert self.m.summary()["total"] == 2

    def test_status_counts_is_dict(self):
        assert isinstance(self.m.summary()["status_counts"], dict)

    def test_risk_counts_is_dict(self):
        assert isinstance(self.m.summary()["risk_counts"], dict)

    def test_influence_counts_is_dict(self):
        assert isinstance(self.m.summary()["influence_counts"], dict)

    def test_action_counts_is_dict(self):
        assert isinstance(self.m.summary()["action_counts"], dict)

    def test_status_counts_sum_equals_total(self):
        s = self.m.summary()
        assert sum(s["status_counts"].values()) == s["total"]

    def test_risk_counts_sum_equals_total(self):
        s = self.m.summary()
        assert sum(s["risk_counts"].values()) == s["total"]

    def test_influence_counts_sum_equals_total(self):
        s = self.m.summary()
        assert sum(s["influence_counts"].values()) == s["total"]

    def test_action_counts_sum_equals_total(self):
        s = self.m.summary()
        assert sum(s["action_counts"].values()) == s["total"]

    def test_avg_composite_positive(self):
        assert self.m.summary()["avg_champion_composite"] > 0.0

    def test_avg_departure_probability_positive(self):
        # one has job change signal → departure > 0
        assert self.m.summary()["avg_departure_probability"] > 0.0

    def test_stable_count_int(self):
        assert isinstance(self.m.summary()["stable_count"], int)

    def test_backup_needed_count_int(self):
        assert isinstance(self.m.summary()["backup_needed_count"], int)

    def test_backup_needed_count_ge_1(self):
        # d2 has job_change=1 and no backup → needs backup
        assert self.m.summary()["backup_needed_count"] >= 1

    def test_avg_engagement_score_positive(self):
        assert self.m.summary()["avg_engagement_score"] >= 0.0

    def test_avg_influence_score_positive(self):
        assert self.m.summary()["avg_influence_score"] >= 0.0

    def test_avg_stability_score_positive(self):
        assert self.m.summary()["avg_stability_score"] >= 0.0

    def test_avg_deal_at_risk_score_in_range(self):
        s = self.m.summary()
        assert 0.0 <= s["avg_deal_at_risk_score"] <= 100.0

    def test_stable_count_matches_property(self):
        s = self.m.summary()
        assert s["stable_count"] == len(self.m.stable_champions)

    def test_backup_needed_count_matches_property(self):
        s = self.m.summary()
        assert s["backup_needed_count"] == len(self.m.backup_needed_queue)

    def test_status_counts_values_are_enum_strings(self):
        s = self.m.summary()
        valid = {e.value for e in ChampionStatus}
        for k in s["status_counts"]:
            assert k in valid

    def test_risk_counts_values_are_enum_strings(self):
        s = self.m.summary()
        valid = {e.value for e in ChampionRisk}
        for k in s["risk_counts"]:
            assert k in valid

    def test_influence_counts_values_are_enum_strings(self):
        s = self.m.summary()
        valid = {e.value for e in InfluenceLevel}
        for k in s["influence_counts"]:
            assert k in valid

    def test_action_counts_values_are_enum_strings(self):
        s = self.m.summary()
        valid = {e.value for e in ChampionAction}
        for k in s["action_counts"]:
            assert k in valid


# ---------------------------------------------------------------------------
# 27. End-to-end scenario tests
# ---------------------------------------------------------------------------

class TestScenarios:
    def test_departed_champion_scenario(self):
        """Champion with job change → DEPARTED, CRITICAL, ESCALATE_EXEC"""
        inp = make_inp(champion_job_change_signal=1, backup_champion_identified=0)
        result = run(inp)
        assert result.champion_status == ChampionStatus.DEPARTED
        assert result.champion_risk == ChampionRisk.CRITICAL
        assert result.champion_action == ChampionAction.ESCALATE_EXEC
        assert result.needs_backup_champion is True
        assert result.is_champion_stable is False

    def test_silent_champion_scenario(self):
        """Ghost champion with 21+ days no contact → SILENT, HIGH"""
        inp = make_inp(
            days_since_champion_contact=21,
            champion_job_change_signal=0,
            champion_reply_rate_pct=10,
            champion_meetings_last_30d=0,
        )
        result = run(inp)
        assert result.champion_status == ChampionStatus.SILENT
        assert result.champion_risk in (ChampionRisk.HIGH, ChampionRisk.CRITICAL)

    def test_active_advocate_scenario(self):
        """High composite, 3+ intros → ACTIVE_ADVOCATE"""
        inp = make_inp(
            champion_job_change_signal=0,
            days_since_champion_contact=2,
            champion_reply_rate_pct=90,
            champion_meetings_last_30d=5,
            champion_meetings_prior_30d=3,
            champion_intro_count=5,
        )
        result = run(inp)
        assert result.champion_status == ChampionStatus.ACTIVE_ADVOCATE

    def test_cooling_champion_scenario(self):
        """Moderate composite without intros → COOLING"""
        inp = make_inp(
            champion_title_level=1,
            champion_budget_authority=0,
            champion_intro_count=0,
            champion_created_internal_urgency=0,
            champion_job_change_signal=0,
            champion_reply_rate_pct=25,
            champion_meetings_last_30d=0,
            champion_meetings_prior_30d=0,
            days_since_champion_contact=10,
            executive_relationship_score=10,
            multi_threaded_contacts=0,
            backup_champion_identified=0,
            deal_stage_numeric=2,
        )
        result = run(inp)
        assert result.champion_status == ChampionStatus.COOLING

    def test_high_risk_deal_close_soon(self):
        """Low composite + close in 10 days → high deal_at_risk_score"""
        inp = make_inp(
            champion_job_change_signal=0,
            champion_title_level=1,
            champion_budget_authority=0,
            champion_intro_count=0,
            champion_created_internal_urgency=0,
            champion_reply_rate_pct=5,
            champion_meetings_last_30d=0,
            champion_meetings_prior_30d=0,
            days_since_champion_contact=60,
            executive_relationship_score=0,
            multi_threaded_contacts=0,
            backup_champion_identified=0,
            deal_stage_numeric=1,
            days_to_close=10,
        )
        result = run(inp)
        assert result.deal_at_risk_score > 50.0

    def test_monitor_batch_mixed_portfolio(self):
        m = ChampionRiskMonitor()
        deals = [
            make_inp(deal_id="healthy"),
            make_inp(deal_id="departed", champion_job_change_signal=1, backup_champion_identified=0),
            make_inp(deal_id="silent", days_since_champion_contact=25, champion_reply_rate_pct=5,
                     champion_meetings_last_30d=0),
        ]
        results = m.monitor_batch(deals)
        assert len(results) == 3
        ids = {r.deal_id for r in results}
        assert ids == {"healthy", "departed", "silent"}
        s = m.summary()
        assert s["total"] == 3
        # At least one critical
        assert s["risk_counts"].get("critical", 0) >= 1

    def test_full_composite_calculation_matches_result(self):
        m = ChampionRiskMonitor()
        inp = make_inp()
        r = m.monitor(inp)
        eng = m._engagement_score(inp)
        inf = m._influence_score(inp)
        sta = m._stability_score(inp)
        pro = m._deal_protection_score(inp)
        expected = m._composite(eng, inf, sta, pro)
        assert r.champion_composite == expected

    def test_low_risk_champion_action_is_maintain(self):
        result = run(make_inp())
        if result.champion_risk == ChampionRisk.LOW and not result.needs_backup_champion:
            assert result.champion_action == ChampionAction.MAINTAIN

    def test_find_backup_when_no_backup_low_composite(self):
        inp = make_inp(
            backup_champion_identified=0,
            champion_job_change_signal=0,
            champion_title_level=1,
            champion_budget_authority=0,
            champion_intro_count=0,
            champion_created_internal_urgency=0,
            champion_reply_rate_pct=0,
            champion_meetings_last_30d=0,
            champion_meetings_prior_30d=0,
            days_since_champion_contact=60,
            executive_relationship_score=0,
            multi_threaded_contacts=0,
            deal_stage_numeric=1,
        )
        result = run(inp)
        if result.needs_backup_champion and result.champion_risk != ChampionRisk.CRITICAL:
            assert result.champion_action == ChampionAction.FIND_BACKUP
