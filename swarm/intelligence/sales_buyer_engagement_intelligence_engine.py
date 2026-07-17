from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class EngagementRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class EngagementPattern(str, Enum):
    none                = "none"
    one_way_sender      = "one_way_sender"
    low_signal_pursuer  = "low_signal_pursuer"
    engagement_ignorer  = "engagement_ignorer"
    meeting_canceler    = "meeting_canceler"
    proposal_black_hole = "proposal_black_hole"


class EngagementSeverity(str, Enum):
    engaged    = "engaged"
    responsive = "responsive"
    passive    = "passive"
    dark       = "dark"


class EngagementAction(str, Enum):
    no_action                    = "no_action"
    engagement_quality_coaching  = "engagement_quality_coaching"
    signal_response_coaching     = "signal_response_coaching"
    buyer_activation_coaching    = "buyer_activation_coaching"
    deal_review_coaching         = "deal_review_coaching"
    engagement_intervention      = "engagement_intervention"
    deal_qualification_review    = "deal_qualification_review"


@dataclass
class EngagementInput:
    rep_id:                                  str
    region:                                  str
    evaluation_period_id:                    str
    buyer_email_response_rate_pct:           float   # 0-1
    meeting_attendance_rate_pct:             float   # 0-1
    meeting_cancellation_rate_pct:           float   # 0-1
    buyer_initiated_follow_up_pct:           float   # 0-1
    proposal_open_rate_pct:                  float   # 0-1
    proposal_viewed_more_than_once_pct:      float   # 0-1
    content_shared_engagement_rate_pct:      float   # 0-1
    demo_to_next_step_commitment_rate_pct:   float   # 0-1
    stakeholder_expansion_by_buyer_pct:      float   # 0-1
    avg_days_buyer_silent_before_followup:   float   # days
    rep_response_to_buyer_signal_hours_avg:  float   # hours
    buyer_urgency_expression_rate_pct:       float   # 0-1
    multi_touch_engagement_rate_pct:         float   # 0-1
    deal_dark_more_than_14d_pct:             float   # 0-1
    executive_engagement_by_buyer_pct:       float   # 0-1
    reference_request_rate_pct:              float   # 0-1
    mutual_action_plan_adherence_pct:        float   # 0-1
    total_active_deals:                      int
    avg_opportunity_value_usd:               float


@dataclass
class EngagementResult:
    rep_id:                            str
    region:                            str
    engagement_risk:                   EngagementRisk
    engagement_pattern:                EngagementPattern
    engagement_severity:               EngagementSeverity
    recommended_action:                EngagementAction
    responsiveness_score:              float
    signal_score:                      float
    activation_score:                  float
    risk_score:                        float
    engagement_composite:              float
    has_engagement_gap:                bool
    requires_engagement_coaching:      bool
    estimated_revenue_at_dark_usd:     float
    engagement_signal:                 str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "engagement_risk":               self.engagement_risk.value,
            "engagement_pattern":            self.engagement_pattern.value,
            "engagement_severity":           self.engagement_severity.value,
            "recommended_action":            self.recommended_action.value,
            "responsiveness_score":          self.responsiveness_score,
            "signal_score":                  self.signal_score,
            "activation_score":              self.activation_score,
            "risk_score":                    self.risk_score,
            "engagement_composite":          self.engagement_composite,
            "has_engagement_gap":            self.has_engagement_gap,
            "requires_engagement_coaching":  self.requires_engagement_coaching,
            "estimated_revenue_at_dark_usd": self.estimated_revenue_at_dark_usd,
            "engagement_signal":             self.engagement_signal,
        }


class SalesBuyerEngagementIntelligenceEngine:
    """Detects per-rep buyer engagement gaps — signal strength, responsiveness, activation, and deal darkening."""

    def __init__(self) -> None:
        self._results: List[EngagementResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _responsiveness_score(self, inp: EngagementInput) -> float:
        s = 0.0
        if   inp.buyer_email_response_rate_pct  <= 0.25: s += 40
        elif inp.buyer_email_response_rate_pct  <= 0.45: s += 22
        elif inp.buyer_email_response_rate_pct  <= 0.60: s += 8
        if   inp.meeting_attendance_rate_pct    <= 0.55: s += 35
        elif inp.meeting_attendance_rate_pct    <= 0.75: s += 18
        if   inp.buyer_initiated_follow_up_pct  <= 0.10: s += 25
        elif inp.buyer_initiated_follow_up_pct  <= 0.25: s += 12
        return min(s, 100.0)

    def _signal_score(self, inp: EngagementInput) -> float:
        s = 0.0
        if   inp.proposal_open_rate_pct               <= 0.40: s += 40
        elif inp.proposal_open_rate_pct               <= 0.60: s += 22
        elif inp.proposal_open_rate_pct               <= 0.75: s += 8
        if   inp.content_shared_engagement_rate_pct   <= 0.20: s += 35
        elif inp.content_shared_engagement_rate_pct   <= 0.40: s += 18
        if   inp.multi_touch_engagement_rate_pct      <= 0.20: s += 25
        elif inp.multi_touch_engagement_rate_pct      <= 0.40: s += 12
        return min(s, 100.0)

    def _activation_score(self, inp: EngagementInput) -> float:
        s = 0.0
        if   inp.demo_to_next_step_commitment_rate_pct <= 0.35: s += 45
        elif inp.demo_to_next_step_commitment_rate_pct <= 0.55: s += 25
        elif inp.demo_to_next_step_commitment_rate_pct <= 0.70: s += 10
        if   inp.stakeholder_expansion_by_buyer_pct    <= 0.10: s += 30
        elif inp.stakeholder_expansion_by_buyer_pct    <= 0.25: s += 15
        if   inp.mutual_action_plan_adherence_pct      <= 0.30: s += 25
        elif inp.mutual_action_plan_adherence_pct      <= 0.55: s += 12
        return min(s, 100.0)

    def _risk_score(self, inp: EngagementInput) -> float:
        s = 0.0
        if   inp.deal_dark_more_than_14d_pct         >= 0.40: s += 40
        elif inp.deal_dark_more_than_14d_pct         >= 0.20: s += 22
        elif inp.deal_dark_more_than_14d_pct         >= 0.10: s += 8
        if   inp.meeting_cancellation_rate_pct       >= 0.35: s += 35
        elif inp.meeting_cancellation_rate_pct       >= 0.20: s += 18
        if   inp.avg_days_buyer_silent_before_followup >= 20: s += 25
        elif inp.avg_days_buyer_silent_before_followup >= 12: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, rs: float, ss: float, ac: float, rk: float) -> float:
        return min(round(rs * 0.30 + ss * 0.30 + ac * 0.25 + rk * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: EngagementInput) -> EngagementPattern:
        if inp.buyer_email_response_rate_pct <= 0.20 and inp.buyer_initiated_follow_up_pct <= 0.08:
            return EngagementPattern.one_way_sender
        if inp.proposal_open_rate_pct <= 0.30 and inp.content_shared_engagement_rate_pct <= 0.15:
            return EngagementPattern.low_signal_pursuer
        if inp.deal_dark_more_than_14d_pct >= 0.45 and inp.rep_response_to_buyer_signal_hours_avg >= 48:
            return EngagementPattern.engagement_ignorer
        if inp.meeting_cancellation_rate_pct >= 0.40 and inp.meeting_attendance_rate_pct <= 0.55:
            return EngagementPattern.meeting_canceler
        if inp.proposal_viewed_more_than_once_pct <= 0.15 and inp.proposal_open_rate_pct <= 0.50:
            return EngagementPattern.proposal_black_hole
        return EngagementPattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> EngagementRisk:
        if   composite >= 60: return EngagementRisk.critical
        elif composite >= 40: return EngagementRisk.high
        elif composite >= 20: return EngagementRisk.moderate
        return EngagementRisk.low

    def _severity(self, composite: float) -> EngagementSeverity:
        if   composite >= 60: return EngagementSeverity.dark
        elif composite >= 40: return EngagementSeverity.passive
        elif composite >= 20: return EngagementSeverity.responsive
        return EngagementSeverity.engaged

    def _action(self, risk: EngagementRisk, pattern: EngagementPattern) -> EngagementAction:
        if risk == EngagementRisk.critical:
            if pattern == EngagementPattern.one_way_sender:
                return EngagementAction.deal_qualification_review
            if pattern == EngagementPattern.engagement_ignorer:
                return EngagementAction.engagement_intervention
            return EngagementAction.deal_qualification_review
        if risk == EngagementRisk.high:
            if pattern == EngagementPattern.low_signal_pursuer:
                return EngagementAction.signal_response_coaching
            if pattern == EngagementPattern.meeting_canceler:
                return EngagementAction.buyer_activation_coaching
            if pattern == EngagementPattern.proposal_black_hole:
                return EngagementAction.deal_review_coaching
            return EngagementAction.engagement_quality_coaching
        if risk == EngagementRisk.moderate:
            return EngagementAction.engagement_quality_coaching
        return EngagementAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: EngagementInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.deal_dark_more_than_14d_pct       >= 0.25
            or inp.buyer_email_response_rate_pct     <= 0.40
        )

    def _requires_coaching(self, inp: EngagementInput, composite: float) -> bool:
        return (
            composite >= 30
            or inp.meeting_attendance_rate_pct       <= 0.65
            or inp.demo_to_next_step_commitment_rate_pct <= 0.50
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _at_dark(self, inp: EngagementInput, composite: float) -> float:
        return round(
            inp.total_active_deals
            * inp.avg_opportunity_value_usd
            * inp.deal_dark_more_than_14d_pct
            * (composite / 100),
            2,
        )

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        EngagementPattern.one_way_sender:      "One-way sender",
        EngagementPattern.low_signal_pursuer:  "Low signal pursuer",
        EngagementPattern.engagement_ignorer:  "Engagement ignorer",
        EngagementPattern.meeting_canceler:    "Meeting canceler",
        EngagementPattern.proposal_black_hole: "Proposal black hole",
    }

    def _signal(self, inp: EngagementInput, pattern: EngagementPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Buyer engagement strong — response rates, signal quality, "
                "and deal activation within benchmarks"
            )
        label     = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        resp_pct  = round(inp.buyer_email_response_rate_pct * 100)
        attend_pct = round(inp.meeting_attendance_rate_pct * 100)
        dark_pct  = round(inp.deal_dark_more_than_14d_pct * 100)
        comp_int  = round(composite)
        return (
            f"{label} — {resp_pct}% buyer email response — "
            f"{attend_pct}% meeting attendance — "
            f"{dark_pct}% deals gone dark — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: EngagementInput) -> EngagementResult:
        rs  = self._responsiveness_score(inp)
        ss  = self._signal_score(inp)
        ac  = self._activation_score(inp)
        rk  = self._risk_score(inp)
        comp = self._composite(rs, ss, ac, rk)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = EngagementResult(
            rep_id                       = inp.rep_id,
            region                       = inp.region,
            engagement_risk              = risk,
            engagement_pattern           = pattern,
            engagement_severity          = severity,
            recommended_action           = action,
            responsiveness_score         = rs,
            signal_score                 = ss,
            activation_score             = ac,
            risk_score                   = rk,
            engagement_composite         = comp,
            has_engagement_gap           = self._has_gap(inp, comp),
            requires_engagement_coaching = self._requires_coaching(inp, comp),
            estimated_revenue_at_dark_usd = self._at_dark(inp, comp),
            engagement_signal            = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[EngagementInput]) -> List[EngagementResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_engagement_composite": 0.0,
                "engagement_gap_count": 0,
                "coaching_count": 0,
                "avg_responsiveness_score": 0.0,
                "avg_signal_score": 0.0,
                "avg_activation_score": 0.0,
                "avg_risk_score": 0.0,
                "total_estimated_revenue_at_dark_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_rs = total_ss = total_ac = total_rk = total_dark = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.engagement_risk.value]       = risk_counts.get(res.engagement_risk.value, 0) + 1
            pattern_counts[res.engagement_pattern.value] = pattern_counts.get(res.engagement_pattern.value, 0) + 1
            severity_counts[res.engagement_severity.value] = severity_counts.get(res.engagement_severity.value, 0) + 1
            action_counts[res.recommended_action.value]  = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.engagement_composite
            total_rs   += res.responsiveness_score
            total_ss   += res.signal_score
            total_ac   += res.activation_score
            total_rk   += res.risk_score
            total_dark += res.estimated_revenue_at_dark_usd
            if res.has_engagement_gap:        gap_count      += 1
            if res.requires_engagement_coaching: coaching_count += 1

        n = len(self._results)
        return {
            "total":                                 n,
            "risk_counts":                           risk_counts,
            "pattern_counts":                        pattern_counts,
            "severity_counts":                       severity_counts,
            "action_counts":                         action_counts,
            "avg_engagement_composite":              round(total_comp / n, 1),
            "engagement_gap_count":                  gap_count,
            "coaching_count":                        coaching_count,
            "avg_responsiveness_score":              round(total_rs / n, 1),
            "avg_signal_score":                      round(total_ss / n, 1),
            "avg_activation_score":                  round(total_ac / n, 1),
            "avg_risk_score":                        round(total_rk / n, 1),
            "total_estimated_revenue_at_dark_usd":   round(total_dark, 2),
        }
