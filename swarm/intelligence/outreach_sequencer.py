"""
Outreach Sequencer — manages multi-step email outreach sequences per prospect.

A Sequence is a series of Steps (day offset + template variant).
The sequencer tracks per-prospect progress, handles stop conditions
(reply received, opt-out, max touches), and schedules the next send.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ── Enums ─────────────────────────────────────────────────────────────────────

class StepStatus(str, Enum):
    PENDING   = "pending"    # not yet due
    DUE       = "due"        # ready to send now
    SENT      = "sent"       # already dispatched
    SKIPPED   = "skipped"    # skipped (e.g. prospect replied before this step)
    FAILED    = "failed"     # delivery failure


class SequenceStatus(str, Enum):
    ACTIVE    = "active"     # running normally
    PAUSED    = "paused"     # manually paused
    COMPLETED = "completed"  # all steps done
    STOPPED   = "stopped"    # stopped early (reply / opt-out / max touches)


class StopReason(str, Enum):
    REPLY_RECEIVED = "reply_received"
    OPT_OUT        = "opt_out"
    MAX_TOUCHES    = "max_touches"
    MANUAL         = "manual"
    CONVERTED      = "converted"


# ── Step definition ───────────────────────────────────────────────────────────

@dataclass
class SequenceStep:
    step_index: int        # 0-based position in the sequence
    day_offset: int        # days after sequence start to send this step
    template_id: str       # template to render
    subject_variant: str   # subject line variant key (for A/B)
    channel: str = "email" # email | sms | linkedin

    def to_dict(self) -> dict:
        return {
            "step_index":      self.step_index,
            "day_offset":      self.day_offset,
            "template_id":     self.template_id,
            "subject_variant": self.subject_variant,
            "channel":         self.channel,
        }


# ── Sequence definition ───────────────────────────────────────────────────────

@dataclass
class Sequence:
    sequence_id: str
    name: str
    steps: List[SequenceStep]
    max_touches: int = 5         # stop after this many sent steps
    description: str = ""

    def step_count(self) -> int:
        return len(self.steps)

    def to_dict(self) -> dict:
        return {
            "sequence_id":  self.sequence_id,
            "name":         self.name,
            "description":  self.description,
            "max_touches":  self.max_touches,
            "step_count":   self.step_count(),
            "steps":        [s.to_dict() for s in self.steps],
        }


# ── Per-step execution record ─────────────────────────────────────────────────

@dataclass
class StepRecord:
    step_index:  int
    template_id: str
    scheduled_at: datetime
    status:      StepStatus = StepStatus.PENDING
    sent_at:     Optional[datetime] = None
    opened_at:   Optional[datetime] = None
    clicked_at:  Optional[datetime] = None
    error:       Optional[str] = None

    def mark_sent(self, ts: Optional[datetime] = None) -> None:
        self.status = StepStatus.SENT
        self.sent_at = ts or datetime.utcnow()

    def mark_skipped(self) -> None:
        self.status = StepStatus.SKIPPED

    def mark_failed(self, error: str) -> None:
        self.status = StepStatus.FAILED
        self.error = error

    def mark_opened(self, ts: Optional[datetime] = None) -> None:
        self.opened_at = ts or datetime.utcnow()

    def mark_clicked(self, ts: Optional[datetime] = None) -> None:
        self.clicked_at = ts or datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "step_index":   self.step_index,
            "template_id":  self.template_id,
            "scheduled_at": self.scheduled_at.isoformat(),
            "status":       self.status.value,
            "sent_at":      self.sent_at.isoformat() if self.sent_at else None,
            "opened_at":    self.opened_at.isoformat() if self.opened_at else None,
            "clicked_at":   self.clicked_at.isoformat() if self.clicked_at else None,
            "error":        self.error,
        }


# ── Per-prospect enrollment ───────────────────────────────────────────────────

@dataclass
class Enrollment:
    enrollment_id: str
    prospect_id:   str
    sequence_id:   str
    started_at:    datetime
    step_records:  List[StepRecord] = field(default_factory=list)
    status:        SequenceStatus = SequenceStatus.ACTIVE
    stop_reason:   Optional[StopReason] = None
    stopped_at:    Optional[datetime] = None

    # ── Convenience properties ────────────────────────────────────────────────

    @property
    def sent_count(self) -> int:
        return sum(1 for r in self.step_records if r.status == StepStatus.SENT)

    @property
    def opened_count(self) -> int:
        return sum(1 for r in self.step_records if r.opened_at is not None)

    @property
    def clicked_count(self) -> int:
        return sum(1 for r in self.step_records if r.clicked_at is not None)

    @property
    def next_pending(self) -> Optional[StepRecord]:
        for r in self.step_records:
            if r.status == StepStatus.PENDING:
                return r
        return None

    @property
    def is_active(self) -> bool:
        return self.status == SequenceStatus.ACTIVE

    # ── Step management ───────────────────────────────────────────────────────

    def due_steps(self, as_of: Optional[datetime] = None) -> List[StepRecord]:
        now = as_of or datetime.utcnow()
        return [
            r for r in self.step_records
            if r.status == StepStatus.PENDING and r.scheduled_at <= now
        ]

    def stop(self, reason: StopReason, ts: Optional[datetime] = None) -> None:
        self.status = SequenceStatus.STOPPED
        self.stop_reason = reason
        self.stopped_at = ts or datetime.utcnow()
        for r in self.step_records:
            if r.status == StepStatus.PENDING:
                r.mark_skipped()

    def complete(self) -> None:
        self.status = SequenceStatus.COMPLETED

    def pause(self) -> None:
        if self.status == SequenceStatus.ACTIVE:
            self.status = SequenceStatus.PAUSED

    def resume(self) -> None:
        if self.status == SequenceStatus.PAUSED:
            self.status = SequenceStatus.ACTIVE

    def to_dict(self) -> dict:
        return {
            "enrollment_id": self.enrollment_id,
            "prospect_id":   self.prospect_id,
            "sequence_id":   self.sequence_id,
            "started_at":    self.started_at.isoformat(),
            "status":        self.status.value,
            "stop_reason":   self.stop_reason.value if self.stop_reason else None,
            "stopped_at":    self.stopped_at.isoformat() if self.stopped_at else None,
            "sent_count":    self.sent_count,
            "opened_count":  self.opened_count,
            "clicked_count": self.clicked_count,
            "steps":         [r.to_dict() for r in self.step_records],
        }


# ── Built-in sequences ────────────────────────────────────────────────────────

_DEFAULT_SEQUENCES: Dict[str, Sequence] = {
    "cold_outreach_standard": Sequence(
        sequence_id="cold_outreach_standard",
        name="Prospection standard (5 touches)",
        description="Séquence froide multi-touches pour TPE/PME",
        max_touches=5,
        steps=[
            SequenceStep(0, day_offset=0,  template_id="intro_value",    subject_variant="A"),
            SequenceStep(1, day_offset=3,  template_id="follow_up_1",    subject_variant="B"),
            SequenceStep(2, day_offset=7,  template_id="social_proof",   subject_variant="A"),
            SequenceStep(3, day_offset=12, template_id="urgency_close",  subject_variant="C"),
            SequenceStep(4, day_offset=18, template_id="breakup",        subject_variant="A"),
        ],
    ),
    "warm_reactivation": Sequence(
        sequence_id="warm_reactivation",
        name="Réactivation prospects chauds (3 touches)",
        description="Pour prospects ayant déjà ouvert ou cliqué",
        max_touches=3,
        steps=[
            SequenceStep(0, day_offset=0, template_id="warm_check_in",  subject_variant="A"),
            SequenceStep(1, day_offset=4, template_id="case_study",     subject_variant="B"),
            SequenceStep(2, day_offset=9, template_id="demo_offer",     subject_variant="A"),
        ],
    ),
    "post_quote": Sequence(
        sequence_id="post_quote",
        name="Suivi post-devis (3 touches)",
        description="Après envoi du devis, relances avec valeur",
        max_touches=3,
        steps=[
            SequenceStep(0, day_offset=2,  template_id="quote_reminder", subject_variant="A"),
            SequenceStep(1, day_offset=5,  template_id="objection_faq",  subject_variant="A"),
            SequenceStep(2, day_offset=10, template_id="final_offer",    subject_variant="B"),
        ],
    ),
    "quick_ping": Sequence(
        sequence_id="quick_ping",
        name="Ping rapide (2 touches)",
        description="Séquence minimaliste pour secteurs très occupés",
        max_touches=2,
        steps=[
            SequenceStep(0, day_offset=0, template_id="intro_value",   subject_variant="A"),
            SequenceStep(1, day_offset=5, template_id="follow_up_1",   subject_variant="C"),
        ],
    ),
}


# ── Sequencer ─────────────────────────────────────────────────────────────────

class OutreachSequencer:
    """
    Manages multi-step outreach sequences across prospects.

    Usage::
        seq = OutreachSequencer()
        enr = seq.enroll("prospect_1", "cold_outreach_standard")
        due = seq.get_due_steps("prospect_1")
        seq.mark_sent("prospect_1", enr.enrollment_id, step_index=0)
        seq.handle_reply("prospect_1")   # stops the sequence
    """

    def __init__(self) -> None:
        self._sequences: Dict[str, Sequence] = dict(_DEFAULT_SEQUENCES)
        self._enrollments: Dict[str, List[Enrollment]] = {}  # prospect_id → enrollments
        self._enrollment_index: Dict[str, Enrollment] = {}   # enrollment_id → enrollment
        self._counter: int = 0

    # ── Sequence registry ─────────────────────────────────────────────────────

    def register_sequence(self, sequence: Sequence) -> None:
        self._sequences[sequence.sequence_id] = sequence

    def get_sequence(self, sequence_id: str) -> Optional[Sequence]:
        return self._sequences.get(sequence_id)

    def list_sequences(self) -> List[Sequence]:
        return list(self._sequences.values())

    # ── Enrollment ────────────────────────────────────────────────────────────

    def enroll(
        self,
        prospect_id: str,
        sequence_id: str,
        start_at: Optional[datetime] = None,
    ) -> Enrollment:
        seq = self._sequences.get(sequence_id)
        if not seq:
            raise ValueError(f"Unknown sequence: {sequence_id!r}")

        start = start_at or datetime.utcnow()
        self._counter += 1
        enr_id = f"enr_{self._counter:05d}"

        step_records = [
            StepRecord(
                step_index=step.step_index,
                template_id=step.template_id,
                scheduled_at=start + timedelta(days=step.day_offset),
            )
            for step in seq.steps
        ]

        enr = Enrollment(
            enrollment_id=enr_id,
            prospect_id=prospect_id,
            sequence_id=sequence_id,
            started_at=start,
            step_records=step_records,
        )

        self._enrollments.setdefault(prospect_id, []).append(enr)
        self._enrollment_index[enr_id] = enr
        return enr

    def get_enrollment(self, enrollment_id: str) -> Optional[Enrollment]:
        return self._enrollment_index.get(enrollment_id)

    def get_active_enrollment(self, prospect_id: str) -> Optional[Enrollment]:
        for enr in self._enrollments.get(prospect_id, []):
            if enr.is_active:
                return enr
        return None

    def all_enrollments_for(self, prospect_id: str) -> List[Enrollment]:
        return list(self._enrollments.get(prospect_id, []))

    # ── Step execution ────────────────────────────────────────────────────────

    def get_due_steps(
        self,
        prospect_id: str,
        as_of: Optional[datetime] = None,
    ) -> List[Tuple[Enrollment, StepRecord]]:
        result = []
        for enr in self._enrollments.get(prospect_id, []):
            if not enr.is_active:
                continue
            for step in enr.due_steps(as_of=as_of):
                result.append((enr, step))
        return result

    def get_all_due(self, as_of: Optional[datetime] = None) -> List[Tuple[Enrollment, StepRecord]]:
        result = []
        for enr in self._enrollment_index.values():
            if not enr.is_active:
                continue
            for step in enr.due_steps(as_of=as_of):
                result.append((enr, step))
        return result

    def mark_sent(
        self,
        enrollment_id: str,
        step_index: int,
        ts: Optional[datetime] = None,
    ) -> bool:
        enr = self._enrollment_index.get(enrollment_id)
        if not enr or not enr.is_active:
            return False
        for rec in enr.step_records:
            if rec.step_index == step_index and rec.status == StepStatus.PENDING:
                rec.mark_sent(ts)
                if all(r.status != StepStatus.PENDING for r in enr.step_records):
                    enr.complete()
                elif enr.sent_count >= self._sequences[enr.sequence_id].max_touches:
                    enr.stop(StopReason.MAX_TOUCHES)
                return True
        return False

    def mark_opened(self, enrollment_id: str, step_index: int, ts: Optional[datetime] = None) -> bool:
        enr = self._enrollment_index.get(enrollment_id)
        if not enr:
            return False
        for rec in enr.step_records:
            if rec.step_index == step_index:
                rec.mark_opened(ts)
                return True
        return False

    def mark_clicked(self, enrollment_id: str, step_index: int, ts: Optional[datetime] = None) -> bool:
        enr = self._enrollment_index.get(enrollment_id)
        if not enr:
            return False
        for rec in enr.step_records:
            if rec.step_index == step_index:
                rec.mark_clicked(ts)
                return True
        return False

    def mark_failed(self, enrollment_id: str, step_index: int, error: str) -> bool:
        enr = self._enrollment_index.get(enrollment_id)
        if not enr:
            return False
        for rec in enr.step_records:
            if rec.step_index == step_index and rec.status == StepStatus.PENDING:
                rec.mark_failed(error)
                return True
        return False

    # ── Stop conditions ───────────────────────────────────────────────────────

    def handle_reply(self, prospect_id: str, ts: Optional[datetime] = None) -> int:
        """Stop all active enrollments for a prospect when they reply."""
        stopped = 0
        for enr in self._enrollments.get(prospect_id, []):
            if enr.is_active:
                enr.stop(StopReason.REPLY_RECEIVED, ts)
                stopped += 1
        return stopped

    def handle_opt_out(self, prospect_id: str, ts: Optional[datetime] = None) -> int:
        stopped = 0
        for enr in self._enrollments.get(prospect_id, []):
            if enr.is_active:
                enr.stop(StopReason.OPT_OUT, ts)
                stopped += 1
        return stopped

    def handle_converted(self, prospect_id: str, ts: Optional[datetime] = None) -> int:
        stopped = 0
        for enr in self._enrollments.get(prospect_id, []):
            if enr.is_active:
                enr.stop(StopReason.CONVERTED, ts)
                stopped += 1
        return stopped

    def stop_enrollment(self, enrollment_id: str, reason: StopReason = StopReason.MANUAL) -> bool:
        enr = self._enrollment_index.get(enrollment_id)
        if not enr or not enr.is_active:
            return False
        enr.stop(reason)
        return True

    def pause_enrollment(self, enrollment_id: str) -> bool:
        enr = self._enrollment_index.get(enrollment_id)
        if not enr:
            return False
        enr.pause()
        return True

    def resume_enrollment(self, enrollment_id: str) -> bool:
        enr = self._enrollment_index.get(enrollment_id)
        if not enr:
            return False
        enr.resume()
        return True

    # ── Analytics ─────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        all_enr = list(self._enrollment_index.values())
        by_status: Dict[str, int] = {}
        for enr in all_enr:
            k = enr.status.value
            by_status[k] = by_status.get(k, 0) + 1

        total_sent    = sum(enr.sent_count for enr in all_enr)
        total_opened  = sum(enr.opened_count for enr in all_enr)
        total_clicked = sum(enr.clicked_count for enr in all_enr)
        open_rate  = round(total_opened  / total_sent * 100, 1) if total_sent else 0.0
        click_rate = round(total_clicked / total_sent * 100, 1) if total_sent else 0.0

        stop_reasons: Dict[str, int] = {}
        for enr in all_enr:
            if enr.stop_reason:
                k = enr.stop_reason.value
                stop_reasons[k] = stop_reasons.get(k, 0) + 1

        return {
            "total_enrollments": len(all_enr),
            "by_status":         by_status,
            "total_sent":        total_sent,
            "total_opened":      total_opened,
            "total_clicked":     total_clicked,
            "open_rate_pct":     open_rate,
            "click_rate_pct":    click_rate,
            "stop_reasons":      stop_reasons,
            "sequences_count":   len(self._sequences),
        }

    def prospect_summary(self, prospect_id: str) -> dict:
        enrollments = self._enrollments.get(prospect_id, [])
        return {
            "prospect_id":        prospect_id,
            "total_enrollments":  len(enrollments),
            "active_enrollment":  self.get_active_enrollment(prospect_id) is not None,
            "total_sent":         sum(e.sent_count for e in enrollments),
            "total_opened":       sum(e.opened_count for e in enrollments),
            "total_clicked":      sum(e.clicked_count for e in enrollments),
            "enrollments":        [e.to_dict() for e in enrollments],
        }

    # ── Reset ─────────────────────────────────────────────────────────────────

    def reset(self) -> None:
        self._enrollments.clear()
        self._enrollment_index.clear()
        self._counter = 0
