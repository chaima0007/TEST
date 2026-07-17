"""Sales Activity Fabrication Detector — detects phantom calls, fake meetings,
inflated activity logs and other rep activity fraud patterns."""

from __future__ import annotations

import dataclasses
from enum import Enum


class FabricationRisk(str, Enum):
    none = "none"
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class FabricationPattern(str, Enum):
    none = "none"
    phantom_calls = "phantom_calls"
    fake_meetings = "fake_meetings"
    bulk_logging = "bulk_logging"
    no_follow_up = "no_follow_up"
    note_absence = "note_absence"
    timestamp_clustering = "timestamp_clustering"


class FabricationAction(str, Enum):
    no_action = "no_action"
    monitor = "monitor"
    audit_request = "audit_request"
    manager_review = "manager_review"
    hr_escalation = "hr_escalation"


class FabricationSeverity(str, Enum):
    clean = "clean"
    suspicious = "suspicious"
    likely_fabricated = "likely_fabricated"
    confirmed_fraud = "confirmed_fraud"


@dataclasses.dataclass
class SalesActivityFabricationInput:
    rep_id: str
    rep_name: str
    region: str
    manager_id: str
    calls_logged_count: int
    calls_with_notes_count: int
    calls_avg_duration_seconds: float
    calls_after_hours_pct: float
    meetings_logged_count: int
    meetings_with_attendees_count: int
    meetings_calendar_match_pct: float
    meetings_with_notes_pct: float
    bulk_log_events_count: int
    activities_end_of_month_pct: float
    activities_end_of_quarter_pct: float
    follow_up_email_rate_pct: float
    crm_edit_after_submission_count: int
    retroactive_log_pct: float
    prospect_response_rate_pct: float
    deal_stage_advance_rate_pct: float
    manager_verified_activity_pct: float
    peer_corroboration_score: float


@dataclasses.dataclass
class SalesActivityFabricationResult:
    rep_id: str
    rep_name: str
    fabrication_risk: FabricationRisk
    fabrication_severity: FabricationSeverity
    primary_fabrication_pattern: FabricationPattern
    recommended_action: FabricationAction
    call_authenticity_score: float
    meeting_authenticity_score: float
    timing_anomaly_score: float
    corroboration_score: float
    fabrication_composite: float
    is_likely_fabricating: bool
    requires_audit: bool
    estimated_fake_activity_pct: float
    fabrication_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                      self.rep_id,
            "rep_name":                    self.rep_name,
            "fabrication_risk":            self.fabrication_risk.value,
            "fabrication_severity":        self.fabrication_severity.value,
            "primary_fabrication_pattern": self.primary_fabrication_pattern.value,
            "recommended_action":          self.recommended_action.value,
            "call_authenticity_score":     round(self.call_authenticity_score, 1),
            "meeting_authenticity_score":  round(self.meeting_authenticity_score, 1),
            "timing_anomaly_score":        round(self.timing_anomaly_score, 1),
            "corroboration_score":         round(self.corroboration_score, 1),
            "fabrication_composite":       round(self.fabrication_composite, 1),
            "is_likely_fabricating":       self.is_likely_fabricating,
            "requires_audit":              self.requires_audit,
            "estimated_fake_activity_pct": round(self.estimated_fake_activity_pct, 1),
            "fabrication_signal":          self.fabrication_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class SalesActivityFabricationDetector:
    """Detects fake/fabricated sales activity in CRM logs."""

    def __init__(self) -> None:
        self._results: list[SalesActivityFabricationResult] = []

    # ── sub-scores ──────────────────────────────────────────────────────────

    def _call_authenticity(self, inp: SalesActivityFabricationInput) -> float:
        """Higher score = more suspicious call activity."""
        score = 0.0
        if inp.calls_logged_count > 0:
            note_rate = inp.calls_with_notes_count / inp.calls_logged_count
        else:
            note_rate = 1.0
        # No notes on calls is suspicious
        score += (1.0 - note_rate) * 40.0
        # Very short average calls
        if inp.calls_avg_duration_seconds < 30:
            score += 35.0
        elif inp.calls_avg_duration_seconds < 90:
            score += 15.0
        # High after-hours calls
        if inp.calls_after_hours_pct > 60:
            score += 25.0
        elif inp.calls_after_hours_pct > 40:
            score += 12.0
        return _clamp(score)

    def _meeting_authenticity(self, inp: SalesActivityFabricationInput) -> float:
        """Higher score = more suspicious meeting activity."""
        score = 0.0
        if inp.meetings_logged_count > 0:
            attendee_rate = inp.meetings_with_attendees_count / inp.meetings_logged_count
        else:
            attendee_rate = 1.0
        score += (1.0 - attendee_rate) * 35.0
        # Calendar mismatch
        score += (1.0 - inp.meetings_calendar_match_pct / 100.0) * 35.0
        # No meeting notes
        score += (1.0 - inp.meetings_with_notes_pct / 100.0) * 30.0
        return _clamp(score)

    def _timing_anomaly(self, inp: SalesActivityFabricationInput) -> float:
        """Higher score = more suspicious timing patterns."""
        score = 0.0
        # Bulk logging events (many activities logged at once)
        if inp.bulk_log_events_count >= 5:
            score += 40.0
        elif inp.bulk_log_events_count >= 3:
            score += 20.0
        # Heavy end-of-period logging
        if inp.activities_end_of_month_pct > 50:
            score += 25.0
        elif inp.activities_end_of_month_pct > 35:
            score += 12.0
        if inp.activities_end_of_quarter_pct > 60:
            score += 20.0
        # Retroactive logging
        if inp.retroactive_log_pct > 40:
            score += 30.0
        elif inp.retroactive_log_pct > 20:
            score += 15.0
        return _clamp(score)

    def _corroboration(self, inp: SalesActivityFabricationInput) -> float:
        """Higher score = lower external corroboration = more suspicious."""
        score = 0.0
        # Low follow-up email rate after calls
        score += (1.0 - inp.follow_up_email_rate_pct / 100.0) * 25.0
        # Low prospect response rate suggests no real contact
        score += (1.0 - inp.prospect_response_rate_pct / 100.0) * 30.0
        # Low manager verified activity
        score += (1.0 - inp.manager_verified_activity_pct / 100.0) * 25.0
        # Low peer corroboration
        score += (1.0 - inp.peer_corroboration_score / 100.0) * 20.0
        return _clamp(score)

    # ── classification helpers ───────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> FabricationRisk:
        if composite < 15:
            return FabricationRisk.none
        if composite < 30:
            return FabricationRisk.low
        if composite < 50:
            return FabricationRisk.moderate
        if composite < 70:
            return FabricationRisk.high
        return FabricationRisk.critical

    def _classify_severity(self, composite: float, requires_audit: bool) -> FabricationSeverity:
        if composite >= 70:
            return FabricationSeverity.confirmed_fraud
        if composite >= 50:
            return FabricationSeverity.likely_fabricated
        if requires_audit:
            return FabricationSeverity.suspicious
        return FabricationSeverity.clean

    def _primary_pattern(
        self,
        inp: SalesActivityFabricationInput,
        call_score: float,
        meeting_score: float,
        timing_score: float,
        corr_score: float,
    ) -> FabricationPattern:
        if call_score == 0 and meeting_score == 0 and timing_score == 0 and corr_score == 0:
            return FabricationPattern.none
        scores = {
            FabricationPattern.phantom_calls:        call_score    if inp.calls_avg_duration_seconds < 30 else 0,
            FabricationPattern.fake_meetings:        meeting_score if inp.meetings_calendar_match_pct < 50 else 0,
            FabricationPattern.bulk_logging:         timing_score  if inp.bulk_log_events_count >= 3 else 0,
            FabricationPattern.no_follow_up:         corr_score    if inp.follow_up_email_rate_pct < 20 else 0,
            FabricationPattern.note_absence:         call_score    if inp.calls_with_notes_count == 0 and inp.calls_logged_count > 5 else 0,
            FabricationPattern.timestamp_clustering: timing_score  if inp.activities_end_of_month_pct > 50 else 0,
        }
        best = max(scores, key=lambda k: scores[k])
        if scores[best] == 0:
            return FabricationPattern.none
        return best

    def _recommended_action(self, risk: FabricationRisk, composite: float) -> FabricationAction:
        if risk == FabricationRisk.none:
            return FabricationAction.no_action
        if risk == FabricationRisk.low:
            return FabricationAction.monitor
        if risk == FabricationRisk.moderate:
            return FabricationAction.audit_request
        if risk == FabricationRisk.high:
            return FabricationAction.manager_review
        return FabricationAction.hr_escalation

    def _signal(
        self,
        risk: FabricationRisk,
        pattern: FabricationPattern,
        composite: float,
        inp: SalesActivityFabricationInput,
    ) -> str:
        if risk == FabricationRisk.none:
            return "activity patterns authentic — all indicators within normal range"
        msgs = {
            FabricationPattern.phantom_calls: (
                f"phantom call pattern — avg {inp.calls_avg_duration_seconds:.0f}s call duration, "
                f"{inp.calls_with_notes_count}/{inp.calls_logged_count} calls with notes"
            ),
            FabricationPattern.fake_meetings: (
                f"meeting fabrication risk — {inp.meetings_calendar_match_pct:.0f}% calendar match, "
                f"{inp.meetings_with_notes_pct:.0f}% with notes"
            ),
            FabricationPattern.bulk_logging: (
                f"bulk logging detected — {inp.bulk_log_events_count} bulk events, "
                f"{inp.activities_end_of_month_pct:.0f}% end-of-month activity"
            ),
            FabricationPattern.no_follow_up: (
                f"no follow-up pattern — {inp.follow_up_email_rate_pct:.0f}% follow-up rate after contacts"
            ),
            FabricationPattern.note_absence: (
                f"note absence anomaly — {inp.calls_logged_count - inp.calls_with_notes_count} calls with no notes"
            ),
            FabricationPattern.timestamp_clustering: (
                f"timestamp clustering — {inp.activities_end_of_month_pct:.0f}% of activities end-of-month"
            ),
        }
        base = msgs.get(pattern, f"fabrication risk composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: SalesActivityFabricationInput) -> SalesActivityFabricationResult:
        call_score    = self._call_authenticity(inp)
        meeting_score = self._meeting_authenticity(inp)
        timing_score  = self._timing_anomaly(inp)
        corr_score    = self._corroboration(inp)

        composite = _clamp(
            call_score * 0.30
            + meeting_score * 0.25
            + timing_score * 0.25
            + corr_score * 0.20
        )
        composite = round(composite, 1)

        risk = self._classify_risk(composite)

        is_likely_fabricating = (
            composite >= 45
            or inp.bulk_log_events_count >= 5
            or (inp.calls_avg_duration_seconds < 20 and inp.calls_logged_count > 10)
        )
        requires_audit = (
            composite >= 35
            or inp.crm_edit_after_submission_count >= 5
            or inp.retroactive_log_pct >= 40
        )

        severity = self._classify_severity(composite, requires_audit)
        pattern  = self._primary_pattern(inp, call_score, meeting_score, timing_score, corr_score)
        action   = self._recommended_action(risk, composite)

        estimated_fake_pct = _clamp(composite * 0.8)

        result = SalesActivityFabricationResult(
            rep_id=inp.rep_id,
            rep_name=inp.rep_name,
            fabrication_risk=risk,
            fabrication_severity=severity,
            primary_fabrication_pattern=pattern,
            recommended_action=action,
            call_authenticity_score=call_score,
            meeting_authenticity_score=meeting_score,
            timing_anomaly_score=timing_score,
            corroboration_score=corr_score,
            fabrication_composite=composite,
            is_likely_fabricating=is_likely_fabricating,
            requires_audit=requires_audit,
            estimated_fake_activity_pct=estimated_fake_pct,
            fabrication_signal=self._signal(risk, pattern, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[SalesActivityFabricationInput]
    ) -> list[SalesActivityFabricationResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "severity_counts": {},
                "pattern_counts": {},
                "action_counts": {},
                "avg_fabrication_composite": 0.0,
                "likely_fabricating_count": 0,
                "audit_required_count": 0,
                "avg_call_authenticity_score": 0.0,
                "avg_meeting_authenticity_score": 0.0,
                "avg_timing_anomaly_score": 0.0,
                "avg_corroboration_score": 0.0,
                "avg_estimated_fake_activity_pct": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_call = total_meeting = total_timing = total_corr = total_fake = 0.0
        likely = audit = 0

        for r in self._results:
            risk_counts[r.fabrication_risk.value]            = risk_counts.get(r.fabrication_risk.value, 0) + 1
            severity_counts[r.fabrication_severity.value]    = severity_counts.get(r.fabrication_severity.value, 0) + 1
            pattern_counts[r.primary_fabrication_pattern.value] = pattern_counts.get(r.primary_fabrication_pattern.value, 0) + 1
            action_counts[r.recommended_action.value]        = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp    += r.fabrication_composite
            total_call    += r.call_authenticity_score
            total_meeting += r.meeting_authenticity_score
            total_timing  += r.timing_anomaly_score
            total_corr    += r.corroboration_score
            total_fake    += r.estimated_fake_activity_pct
            if r.is_likely_fabricating:
                likely += 1
            if r.requires_audit:
                audit += 1

        n = len(self._results)
        return {
            "total":                            n,
            "risk_counts":                      risk_counts,
            "severity_counts":                  severity_counts,
            "pattern_counts":                   pattern_counts,
            "action_counts":                    action_counts,
            "avg_fabrication_composite":        round(total_comp    / n, 1),
            "likely_fabricating_count":         likely,
            "audit_required_count":             audit,
            "avg_call_authenticity_score":      round(total_call    / n, 1),
            "avg_meeting_authenticity_score":   round(total_meeting / n, 1),
            "avg_timing_anomaly_score":         round(total_timing  / n, 1),
            "avg_corroboration_score":          round(total_corr    / n, 1),
            "avg_estimated_fake_activity_pct":  round(total_fake    / n, 1),
        }
