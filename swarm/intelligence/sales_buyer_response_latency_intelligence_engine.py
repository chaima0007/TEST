from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class LatencyRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class LatencyPattern(str, Enum):
    none                = "none"
    buyer_ghosting      = "buyer_ghosting"
    executive_avoidance = "executive_avoidance"
    champion_cooling    = "champion_cooling"
    commitment_fading   = "commitment_fading"
    process_stalling    = "process_stalling"


class LatencySeverity(str, Enum):
    responsive   = "responsive"
    cooling      = "cooling"
    disengaging  = "disengaging"
    ghosted      = "ghosted"


class LatencyAction(str, Enum):
    no_action                    = "no_action"
    engagement_monitoring        = "engagement_monitoring"
    re_engagement_coaching       = "re_engagement_coaching"
    executive_outreach_coaching  = "executive_outreach_coaching"
    deal_save_intervention       = "deal_save_intervention"
    champion_replacement_coaching = "champion_replacement_coaching"
    deal_abandon_escalation      = "deal_abandon_escalation"


@dataclass
class LatencyInput:
    rep_id:                            str
    region:                            str
    evaluation_period_id:              str
    avg_buyer_response_hours:          float  # avg hours buyer responds
    response_latency_trend:            float  # 0-1 (1=response time rising badly)
    no_response_rate_pct:              float  # 0-1 outreaches with no response
    avg_follow_ups_before_response:    float  # avg follow-ups needed
    ghost_rate_pct:                    float  # 0-1 deals buyer went silent
    response_time_vs_baseline_ratio:   float  # actual/baseline (>1=slower)
    executive_response_rate_pct:       float  # 0-1 exec outreach that responds
    champion_response_rate_pct:        float  # 0-1 champion outreach that responds
    meeting_acceptance_rate_pct:       float  # 0-1
    meeting_rescheduled_rate_pct:      float  # 0-1 meetings rescheduled by buyer
    meeting_no_show_rate_pct:          float  # 0-1
    demo_request_to_completion_days:   float  # days request to demo completion
    proposal_review_response_days:     float  # days to respond to proposal
    contract_review_latency_days:      float  # days in contract review
    multi_contact_response_diversity:  float  # 0-1 % contacts that respond
    outreach_channel_effectiveness:    float  # 0-1 best channel response rate
    response_quality_score:            float  # 0-1 meaningful vs stalling
    total_active_deals:                int
    avg_deal_value_usd:                float


@dataclass
class LatencyResult:
    rep_id:                       str
    region:                       str
    latency_risk:                 LatencyRisk
    latency_pattern:              LatencyPattern
    latency_severity:             LatencySeverity
    recommended_action:           LatencyAction
    latency_score:                float
    engagement_depth_score:       float
    commitment_score:             float
    process_velocity_score:       float
    latency_composite:            float
    has_latency_gap:              bool
    requires_latency_intervention: bool
    estimated_at_risk_revenue_usd: float
    latency_signal:               str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "latency_risk":                     self.latency_risk.value,
            "latency_pattern":                  self.latency_pattern.value,
            "latency_severity":                 self.latency_severity.value,
            "recommended_action":               self.recommended_action.value,
            "latency_score":                    self.latency_score,
            "engagement_depth_score":           self.engagement_depth_score,
            "commitment_score":                 self.commitment_score,
            "process_velocity_score":           self.process_velocity_score,
            "latency_composite":                self.latency_composite,
            "has_latency_gap":                  self.has_latency_gap,
            "requires_latency_intervention":    self.requires_latency_intervention,
            "estimated_at_risk_revenue_usd":    self.estimated_at_risk_revenue_usd,
            "latency_signal":                   self.latency_signal,
        }


class SalesBuyerResponseLatencyIntelligenceEngine:
    """Detects deal-cooling via buyer response latency patterns — ghosting, executive avoidance, champion cooling."""

    def __init__(self) -> None:
        self._results: List[LatencyResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _latency_score(self, inp: LatencyInput) -> float:
        s = 0.0
        if   inp.avg_buyer_response_hours        >= 96:  s += 40
        elif inp.avg_buyer_response_hours        >= 48:  s += 22
        elif inp.avg_buyer_response_hours        >= 24:  s += 8
        if   inp.response_time_vs_baseline_ratio >= 3.0: s += 35
        elif inp.response_time_vs_baseline_ratio >= 2.0: s += 18
        elif inp.response_time_vs_baseline_ratio >= 1.5: s += 6
        if   inp.no_response_rate_pct            >= 0.50: s += 25
        elif inp.no_response_rate_pct            >= 0.30: s += 12
        return min(s, 100.0)

    def _engagement_depth_score(self, inp: LatencyInput) -> float:
        s = 0.0
        if   inp.ghost_rate_pct                   >= 0.40: s += 40
        elif inp.ghost_rate_pct                   >= 0.25: s += 22
        elif inp.ghost_rate_pct                   >= 0.10: s += 8
        if   inp.champion_response_rate_pct       <= 0.30: s += 35
        elif inp.champion_response_rate_pct       <= 0.50: s += 18
        if   inp.executive_response_rate_pct      <= 0.15: s += 25
        elif inp.executive_response_rate_pct      <= 0.30: s += 12
        return min(s, 100.0)

    def _commitment_score(self, inp: LatencyInput) -> float:
        s = 0.0
        if   inp.meeting_no_show_rate_pct         >= 0.35: s += 40
        elif inp.meeting_no_show_rate_pct         >= 0.20: s += 22
        elif inp.meeting_no_show_rate_pct         >= 0.10: s += 8
        if   inp.meeting_rescheduled_rate_pct     >= 0.50: s += 35
        elif inp.meeting_rescheduled_rate_pct     >= 0.30: s += 18
        if   inp.meeting_acceptance_rate_pct      <= 0.30: s += 25
        elif inp.meeting_acceptance_rate_pct      <= 0.50: s += 12
        return min(s, 100.0)

    def _process_velocity_score(self, inp: LatencyInput) -> float:
        s = 0.0
        if   inp.proposal_review_response_days    >= 21:  s += 45
        elif inp.proposal_review_response_days    >= 14:  s += 25
        elif inp.proposal_review_response_days    >= 7:   s += 10
        if   inp.contract_review_latency_days     >= 30:  s += 30
        elif inp.contract_review_latency_days     >= 21:  s += 15
        if   inp.demo_request_to_completion_days  >= 21:  s += 25
        elif inp.demo_request_to_completion_days  >= 14:  s += 10
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, l: float, e: float, c: float, p: float) -> float:
        return min(round(l * 0.35 + e * 0.25 + c * 0.25 + p * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: LatencyInput) -> LatencyPattern:
        if inp.ghost_rate_pct >= 0.30 and inp.no_response_rate_pct >= 0.40:
            return LatencyPattern.buyer_ghosting
        if inp.executive_response_rate_pct <= 0.20 and inp.meeting_no_show_rate_pct >= 0.25:
            return LatencyPattern.executive_avoidance
        if inp.champion_response_rate_pct <= 0.40 and inp.response_latency_trend >= 0.60:
            return LatencyPattern.champion_cooling
        if inp.meeting_rescheduled_rate_pct >= 0.40 and inp.meeting_acceptance_rate_pct <= 0.40:
            return LatencyPattern.commitment_fading
        if inp.proposal_review_response_days >= 14 and inp.contract_review_latency_days >= 21:
            return LatencyPattern.process_stalling
        return LatencyPattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> LatencyRisk:
        if   composite >= 60: return LatencyRisk.critical
        elif composite >= 40: return LatencyRisk.high
        elif composite >= 20: return LatencyRisk.moderate
        return LatencyRisk.low

    def _severity(self, composite: float) -> LatencySeverity:
        if   composite >= 60: return LatencySeverity.ghosted
        elif composite >= 40: return LatencySeverity.disengaging
        elif composite >= 20: return LatencySeverity.cooling
        return LatencySeverity.responsive

    def _action(self, risk: LatencyRisk, pattern: LatencyPattern) -> LatencyAction:
        if risk == LatencyRisk.critical:
            if pattern in (LatencyPattern.buyer_ghosting, LatencyPattern.executive_avoidance):
                return LatencyAction.deal_abandon_escalation
            return LatencyAction.deal_save_intervention
        if risk == LatencyRisk.high:
            if pattern == LatencyPattern.buyer_ghosting:
                return LatencyAction.deal_save_intervention
            if pattern == LatencyPattern.executive_avoidance:
                return LatencyAction.executive_outreach_coaching
            if pattern == LatencyPattern.champion_cooling:
                return LatencyAction.champion_replacement_coaching
            if pattern == LatencyPattern.commitment_fading:
                return LatencyAction.re_engagement_coaching
            if pattern == LatencyPattern.process_stalling:
                return LatencyAction.executive_outreach_coaching
            return LatencyAction.re_engagement_coaching
        if risk == LatencyRisk.moderate:
            return LatencyAction.engagement_monitoring
        return LatencyAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: LatencyInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.ghost_rate_pct               >= 0.20
            or inp.avg_buyer_response_hours     >= 48
        )

    def _requires_intervention(self, inp: LatencyInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.meeting_no_show_rate_pct     >= 0.15
            or inp.champion_response_rate_pct   <= 0.55
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _at_risk_revenue(self, inp: LatencyInput, composite: float) -> float:
        at_risk_deals = inp.total_active_deals * (inp.ghost_rate_pct + inp.no_response_rate_pct * 0.5)
        at_risk_deals = min(at_risk_deals, inp.total_active_deals)
        return round(at_risk_deals * inp.avg_deal_value_usd * (composite / 100), 2)

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        LatencyPattern.buyer_ghosting:      "Buyer ghosting",
        LatencyPattern.executive_avoidance: "Executive avoidance",
        LatencyPattern.champion_cooling:    "Champion cooling",
        LatencyPattern.commitment_fading:   "Commitment fading",
        LatencyPattern.process_stalling:    "Process stalling",
    }

    def _signal(self, inp: LatencyInput, pattern: LatencyPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Buyer engagement healthy — response times, meeting attendance, "
                "champion engagement, and process velocity within benchmarks"
            )
        label     = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        resp_hrs  = round(inp.avg_buyer_response_hours)
        ghost_pct = round(inp.ghost_rate_pct * 100)
        noshow_pct = round(inp.meeting_no_show_rate_pct * 100)
        comp_int  = round(composite)
        return (
            f"{label} — {resp_hrs}h avg buyer response — "
            f"{ghost_pct}% deals ghosted — "
            f"{noshow_pct}% meeting no-shows — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: LatencyInput) -> LatencyResult:
        l  = self._latency_score(inp)
        e  = self._engagement_depth_score(inp)
        c  = self._commitment_score(inp)
        p  = self._process_velocity_score(inp)
        comp = self._composite(l, e, c, p)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = LatencyResult(
            rep_id                      = inp.rep_id,
            region                      = inp.region,
            latency_risk                = risk,
            latency_pattern             = pattern,
            latency_severity            = severity,
            recommended_action          = action,
            latency_score               = l,
            engagement_depth_score      = e,
            commitment_score            = c,
            process_velocity_score      = p,
            latency_composite           = comp,
            has_latency_gap             = self._has_gap(inp, comp),
            requires_latency_intervention = self._requires_intervention(inp, comp),
            estimated_at_risk_revenue_usd = self._at_risk_revenue(inp, comp),
            latency_signal              = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[LatencyInput]) -> List[LatencyResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_latency_composite": 0.0,
                "latency_gap_count": 0,
                "intervention_count": 0,
                "avg_latency_score": 0.0,
                "avg_engagement_depth_score": 0.0,
                "avg_commitment_score": 0.0,
                "avg_process_velocity_score": 0.0,
                "total_estimated_at_risk_revenue_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_l = total_e = total_c = total_p = total_ar = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.latency_risk.value]       = risk_counts.get(res.latency_risk.value, 0) + 1
            pattern_counts[res.latency_pattern.value] = pattern_counts.get(res.latency_pattern.value, 0) + 1
            severity_counts[res.latency_severity.value] = severity_counts.get(res.latency_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.latency_composite
            total_l    += res.latency_score
            total_e    += res.engagement_depth_score
            total_c    += res.commitment_score
            total_p    += res.process_velocity_score
            total_ar   += res.estimated_at_risk_revenue_usd
            if res.has_latency_gap:              gap_count          += 1
            if res.requires_latency_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_latency_composite":                    round(total_comp / n, 1),
            "latency_gap_count":                        gap_count,
            "intervention_count":                       intervention_count,
            "avg_latency_score":                        round(total_l / n, 1),
            "avg_engagement_depth_score":               round(total_e / n, 1),
            "avg_commitment_score":                     round(total_c / n, 1),
            "avg_process_velocity_score":               round(total_p / n, 1),
            "total_estimated_at_risk_revenue_usd":      round(total_ar, 2),
        }
