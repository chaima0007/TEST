"""
Tests for intelligence/outreach_sequencer.py
"""

import pytest
from datetime import datetime, timedelta
from intelligence.outreach_sequencer import (
    OutreachSequencer, Sequence, SequenceStep, Enrollment, StepRecord,
    StepStatus, SequenceStatus, StopReason,
    _DEFAULT_SEQUENCES,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

T0 = datetime(2025, 1, 15, 9, 0, 0)   # fixed reference time


def seq() -> OutreachSequencer:
    return OutreachSequencer()


def enroll(sequencer, prospect_id="p001", sequence_id="cold_outreach_standard", start_at=None):
    return sequencer.enroll(prospect_id, sequence_id, start_at=start_at or T0)


# ── Default sequence catalogue ────────────────────────────────────────────────

class TestDefaultSequences:
    def test_four_sequences_exist(self):
        assert len(_DEFAULT_SEQUENCES) == 4

    def test_all_ids_present(self):
        assert set(_DEFAULT_SEQUENCES.keys()) == {
            "cold_outreach_standard", "warm_reactivation",
            "post_quote", "quick_ping",
        }

    def test_cold_standard_has_5_steps(self):
        assert _DEFAULT_SEQUENCES["cold_outreach_standard"].step_count() == 5

    def test_quick_ping_has_2_steps(self):
        assert _DEFAULT_SEQUENCES["quick_ping"].step_count() == 2

    def test_steps_have_increasing_day_offsets(self):
        seq_def = _DEFAULT_SEQUENCES["cold_outreach_standard"]
        offsets = [s.day_offset for s in seq_def.steps]
        assert offsets == sorted(offsets)

    def test_to_dict_has_keys(self):
        d = _DEFAULT_SEQUENCES["cold_outreach_standard"].to_dict()
        for key in ("sequence_id", "name", "steps", "max_touches", "step_count"):
            assert key in d

    def test_step_to_dict_has_keys(self):
        step = _DEFAULT_SEQUENCES["cold_outreach_standard"].steps[0]
        d = step.to_dict()
        for key in ("step_index", "day_offset", "template_id", "subject_variant", "channel"):
            assert key in d


# ── Register custom sequence ──────────────────────────────────────────────────

class TestRegisterSequence:
    def test_register_adds_sequence(self):
        s = seq()
        custom = Sequence(
            sequence_id="custom_test",
            name="Custom",
            steps=[SequenceStep(0, 0, "intro", "A")],
        )
        s.register_sequence(custom)
        assert s.get_sequence("custom_test") is custom

    def test_overwrite_existing(self):
        s = seq()
        custom = Sequence(
            sequence_id="quick_ping",
            name="Overwritten",
            steps=[SequenceStep(0, 0, "ping_new", "A")],
        )
        s.register_sequence(custom)
        assert s.get_sequence("quick_ping").name == "Overwritten"

    def test_unknown_sequence_returns_none(self):
        assert seq().get_sequence("nonexistent") is None

    def test_list_sequences_includes_defaults(self):
        seqs = seq().list_sequences()
        ids = [s.sequence_id for s in seqs]
        assert "cold_outreach_standard" in ids


# ── Enrollment ────────────────────────────────────────────────────────────────

class TestEnrollment:
    def test_enroll_returns_enrollment(self):
        s = seq()
        enr = enroll(s)
        assert isinstance(enr, Enrollment)

    def test_enrollment_has_correct_prospect(self):
        s = seq()
        enr = enroll(s, prospect_id="p_abc")
        assert enr.prospect_id == "p_abc"

    def test_enrollment_has_correct_sequence(self):
        s = seq()
        enr = enroll(s, sequence_id="quick_ping")
        assert enr.sequence_id == "quick_ping"

    def test_enrollment_status_is_active(self):
        s = seq()
        enr = enroll(s)
        assert enr.status == SequenceStatus.ACTIVE

    def test_enrollment_id_is_unique(self):
        s = seq()
        e1 = enroll(s, "p1")
        e2 = enroll(s, "p2")
        assert e1.enrollment_id != e2.enrollment_id

    def test_step_records_created(self):
        s = seq()
        enr = enroll(s)
        assert len(enr.step_records) == 5

    def test_step_scheduled_dates(self):
        s = seq()
        enr = enroll(s, start_at=T0)
        seq_def = _DEFAULT_SEQUENCES["cold_outreach_standard"]
        for i, step in enumerate(seq_def.steps):
            expected = T0 + timedelta(days=step.day_offset)
            assert enr.step_records[i].scheduled_at == expected

    def test_unknown_sequence_raises(self):
        with pytest.raises(ValueError):
            seq().enroll("p1", "nonexistent")

    def test_multiple_enrollments_per_prospect(self):
        s = seq()
        enroll(s, "p1", "quick_ping")
        enroll(s, "p1", "warm_reactivation")
        assert len(s.all_enrollments_for("p1")) == 2

    def test_get_active_enrollment(self):
        s = seq()
        enr = enroll(s, "p1")
        assert s.get_active_enrollment("p1") is enr

    def test_no_active_when_stopped(self):
        s = seq()
        enr = enroll(s, "p1")
        enr.stop(StopReason.MANUAL)
        assert s.get_active_enrollment("p1") is None

    def test_get_enrollment_by_id(self):
        s = seq()
        enr = enroll(s, "p1")
        assert s.get_enrollment(enr.enrollment_id) is enr


# ── Due steps ─────────────────────────────────────────────────────────────────

class TestDueSteps:
    def test_step_0_due_at_start(self):
        s = seq()
        enr = enroll(s, "p1", start_at=T0)
        due = s.get_due_steps("p1", as_of=T0)
        assert len(due) == 1
        assert due[0][1].step_index == 0

    def test_no_due_steps_before_start(self):
        s = seq()
        enroll(s, "p1", start_at=T0)
        due = s.get_due_steps("p1", as_of=T0 - timedelta(hours=1))
        assert due == []

    def test_multiple_due_after_days(self):
        s = seq()
        enroll(s, "p1", start_at=T0)
        # cold_outreach_standard: offsets 0, 3, 7, 12, 18
        # At day 8: steps 0, 3, 7 are due
        due = s.get_due_steps("p1", as_of=T0 + timedelta(days=8))
        assert len(due) == 3

    def test_all_due_at_end(self):
        s = seq()
        enroll(s, "p1", start_at=T0)
        due = s.get_due_steps("p1", as_of=T0 + timedelta(days=20))
        assert len(due) == 5

    def test_get_all_due_across_prospects(self):
        s = seq()
        enroll(s, "p1", "quick_ping", start_at=T0)
        enroll(s, "p2", "quick_ping", start_at=T0)
        due = s.get_all_due(as_of=T0)
        assert len(due) == 2   # step 0 for both

    def test_stopped_enrollment_not_in_due(self):
        s = seq()
        enr = enroll(s, "p1", start_at=T0)
        enr.stop(StopReason.MANUAL)
        due = s.get_due_steps("p1", as_of=T0 + timedelta(days=20))
        assert due == []


# ── Mark sent ─────────────────────────────────────────────────────────────────

class TestMarkSent:
    def test_mark_sent_returns_true(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        assert s.mark_sent(enr.enrollment_id, step_index=0) is True

    def test_step_status_is_sent(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_sent(enr.enrollment_id, step_index=0)
        assert enr.step_records[0].status == StepStatus.SENT

    def test_sent_count_increments(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_sent(enr.enrollment_id, 0)
        assert enr.sent_count == 1

    def test_max_touches_stops_sequence(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_sent(enr.enrollment_id, 0)
        s.mark_sent(enr.enrollment_id, 1)
        # quick_ping max_touches=2, all steps sent → completed or stopped
        assert enr.status in {SequenceStatus.COMPLETED, SequenceStatus.STOPPED}

    def test_all_steps_sent_completes_sequence(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_sent(enr.enrollment_id, 0)
        s.mark_sent(enr.enrollment_id, 1)
        assert enr.status == SequenceStatus.COMPLETED

    def test_mark_already_sent_returns_false(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_sent(enr.enrollment_id, 0)
        assert s.mark_sent(enr.enrollment_id, 0) is False

    def test_unknown_enrollment_returns_false(self):
        s = seq()
        assert s.mark_sent("unknown_enr", step_index=0) is False

    def test_sent_at_timestamp_recorded(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        ts = T0 + timedelta(hours=1)
        s.mark_sent(enr.enrollment_id, 0, ts=ts)
        assert enr.step_records[0].sent_at == ts


# ── Mark opened / clicked ─────────────────────────────────────────────────────

class TestMarkOpenedClicked:
    def test_mark_opened(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_sent(enr.enrollment_id, 0)
        assert s.mark_opened(enr.enrollment_id, 0) is True
        assert enr.step_records[0].opened_at is not None

    def test_mark_clicked(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_sent(enr.enrollment_id, 0)
        assert s.mark_clicked(enr.enrollment_id, 0) is True
        assert enr.step_records[0].clicked_at is not None

    def test_opened_count(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_sent(enr.enrollment_id, 0)
        s.mark_opened(enr.enrollment_id, 0)
        assert enr.opened_count == 1

    def test_clicked_count(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_sent(enr.enrollment_id, 0)
        s.mark_clicked(enr.enrollment_id, 0)
        assert enr.clicked_count == 1

    def test_unknown_enrollment_opened_returns_false(self):
        assert seq().mark_opened("bad_id", 0) is False


# ── Mark failed ───────────────────────────────────────────────────────────────

class TestMarkFailed:
    def test_mark_failed_sets_status(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_failed(enr.enrollment_id, 0, "SMTP error")
        assert enr.step_records[0].status == StepStatus.FAILED

    def test_mark_failed_sets_error(self):
        s = seq()
        enr = enroll(s, "p1", "quick_ping", start_at=T0)
        s.mark_failed(enr.enrollment_id, 0, "Timeout")
        assert enr.step_records[0].error == "Timeout"


# ── Stop conditions ───────────────────────────────────────────────────────────

class TestStopConditions:
    def test_handle_reply_stops_active(self):
        s = seq()
        enroll(s, "p1")
        stopped = s.handle_reply("p1")
        assert stopped == 1
        assert s.get_active_enrollment("p1") is None

    def test_reply_skips_pending_steps(self):
        s = seq()
        enr = enroll(s, "p1")
        s.handle_reply("p1")
        pending = [r for r in enr.step_records if r.status == StepStatus.PENDING]
        assert pending == []

    def test_reply_sets_stop_reason(self):
        s = seq()
        enr = enroll(s, "p1")
        s.handle_reply("p1")
        assert enr.stop_reason == StopReason.REPLY_RECEIVED

    def test_handle_opt_out(self):
        s = seq()
        enr = enroll(s, "p1")
        s.handle_opt_out("p1")
        assert enr.stop_reason == StopReason.OPT_OUT

    def test_handle_converted(self):
        s = seq()
        enr = enroll(s, "p1")
        s.handle_converted("p1")
        assert enr.stop_reason == StopReason.CONVERTED

    def test_stop_enrollment_by_id(self):
        s = seq()
        enr = enroll(s, "p1")
        assert s.stop_enrollment(enr.enrollment_id, StopReason.MANUAL) is True
        assert enr.status == SequenceStatus.STOPPED

    def test_stop_already_stopped_returns_false(self):
        s = seq()
        enr = enroll(s, "p1")
        s.stop_enrollment(enr.enrollment_id)
        assert s.stop_enrollment(enr.enrollment_id) is False

    def test_reply_on_no_active_returns_0(self):
        s = seq()
        assert s.handle_reply("nonexistent") == 0

    def test_reply_stops_multiple_active(self):
        s = seq()
        enroll(s, "p1", "quick_ping")
        enroll(s, "p1", "warm_reactivation")
        stopped = s.handle_reply("p1")
        assert stopped == 2


# ── Pause / resume ────────────────────────────────────────────────────────────

class TestPauseResume:
    def test_pause_enrollment(self):
        s = seq()
        enr = enroll(s, "p1")
        s.pause_enrollment(enr.enrollment_id)
        assert enr.status == SequenceStatus.PAUSED

    def test_paused_not_in_due(self):
        s = seq()
        enr = enroll(s, "p1", start_at=T0)
        s.pause_enrollment(enr.enrollment_id)
        due = s.get_due_steps("p1", as_of=T0 + timedelta(days=20))
        assert due == []

    def test_resume_enrollment(self):
        s = seq()
        enr = enroll(s, "p1")
        s.pause_enrollment(enr.enrollment_id)
        s.resume_enrollment(enr.enrollment_id)
        assert enr.status == SequenceStatus.ACTIVE

    def test_pause_unknown_returns_false(self):
        assert seq().pause_enrollment("bad_id") is False

    def test_resume_unknown_returns_false(self):
        assert seq().resume_enrollment("bad_id") is False


# ── Summary ───────────────────────────────────────────────────────────────────

class TestSummary:
    def test_empty_summary(self):
        s = seq()
        summary = s.summary()
        assert summary["total_enrollments"] == 0
        assert summary["total_sent"] == 0
        assert summary["open_rate_pct"] == 0.0

    def test_summary_after_enrollments(self):
        s = seq()
        enroll(s, "p1", "quick_ping")
        enroll(s, "p2", "quick_ping")
        summary = s.summary()
        assert summary["total_enrollments"] == 2

    def test_summary_by_status(self):
        s = seq()
        enr1 = enroll(s, "p1", "quick_ping")
        enroll(s, "p2", "quick_ping")
        s.handle_reply("p1")
        summary = s.summary()
        assert summary["by_status"].get("active", 0) == 1
        assert summary["by_status"].get("stopped", 0) == 1

    def test_summary_stop_reasons(self):
        s = seq()
        enr = enroll(s, "p1")
        s.handle_reply("p1")
        summary = s.summary()
        assert summary["stop_reasons"].get("reply_received", 0) == 1

    def test_summary_keys(self):
        summary = seq().summary()
        for key in ("total_enrollments", "by_status", "total_sent",
                    "total_opened", "total_clicked", "open_rate_pct",
                    "click_rate_pct", "stop_reasons", "sequences_count"):
            assert key in summary

    def test_prospect_summary(self):
        s = seq()
        enroll(s, "p1", "quick_ping")
        ps = s.prospect_summary("p1")
        assert ps["prospect_id"] == "p1"
        assert ps["total_enrollments"] == 1
        assert ps["active_enrollment"] is True

    def test_prospect_summary_unknown(self):
        ps = seq().prospect_summary("nobody")
        assert ps["total_enrollments"] == 0
        assert ps["active_enrollment"] is False


# ── Enrollment.to_dict ────────────────────────────────────────────────────────

class TestEnrollmentToDict:
    def test_to_dict_has_keys(self):
        s = seq()
        enr = enroll(s, "p1")
        d = enr.to_dict()
        for key in ("enrollment_id", "prospect_id", "sequence_id",
                    "started_at", "status", "sent_count", "steps"):
            assert key in d

    def test_step_record_to_dict(self):
        s = seq()
        enr = enroll(s, "p1")
        d = enr.step_records[0].to_dict()
        for key in ("step_index", "template_id", "scheduled_at", "status"):
            assert key in d


# ── Reset ─────────────────────────────────────────────────────────────────────

class TestReset:
    def test_reset_clears_enrollments(self):
        s = seq()
        enroll(s, "p1")
        s.reset()
        assert s.all_enrollments_for("p1") == []

    def test_reset_clears_due_steps(self):
        s = seq()
        enroll(s, "p1", start_at=T0)
        s.reset()
        assert s.get_due_steps("p1", as_of=T0 + timedelta(days=20)) == []

    def test_reset_allows_fresh_enroll(self):
        s = seq()
        enroll(s, "p1")
        s.reset()
        e2 = enroll(s, "p1")
        assert isinstance(e2, Enrollment)
        assert e2.status == SequenceStatus.ACTIVE

    def test_reset_preserves_sequences(self):
        s = seq()
        enroll(s, "p1")
        s.reset()
        assert s.get_sequence("cold_outreach_standard") is not None
