from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class LeadResponseRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class LeadResponsePattern(str, Enum):
    none              = "none"
    slow_response     = "slow_response"
    poor_qualification = "poor_qualification"
    low_conversion    = "low_conversion"
    lead_neglect      = "lead_neglect"
    icp_miss          = "icp_miss"


class LeadResponseSeverity(str, Enum):
    responsive = "responsive"
    delayed    = "delayed"
    lagging    = "lagging"
    critical   = "critical"


class LeadResponseAction(str, Enum):
    no_action               = "no_action"
    response_time_coaching  = "response_time_coaching"
    qualification_training  = "qualification_training"
    lead_prioritization     = "lead_prioritization"
    crm_discipline          = "crm_discipline"
    lead_cadence_reset      = "lead_cadence_reset"


@dataclass
class InboundLeadResponseInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    inbound_leads_assigned: int
    inbound_leads_contacted: int
    avg_first_response_hours: float
    leads_contacted_within_1h: int
    leads_contacted_within_5h: int
    leads_contacted_over_24h: int
    leads_never_contacted: int
    lead_to_qualified_conversion_rate_pct: float
    qualified_to_opportunity_conversion_rate_pct: float
    inbound_opportunity_close_rate_pct: float
    avg_lead_qualification_score: float
    high_icp_leads_received: int
    high_icp_leads_converted: int
    leads_disqualified_too_early: int
    leads_over_qualified_waste_count: int
    avg_response_quality_score: float
    crm_lead_entry_rate_pct: float
    avg_lead_revenue_potential_usd: float
    leads_lost_to_competitor_before_contact: int


@dataclass
class InboundLeadResponseResult:
    rep_id: str
    region: str
    lead_response_risk: LeadResponseRisk
    lead_response_pattern: LeadResponsePattern
    lead_response_severity: LeadResponseSeverity
    recommended_action: LeadResponseAction
    response_speed_score: float
    qualification_quality_score: float
    lead_conversion_score: float
    lead_discipline_score: float
    lead_response_composite: float
    has_response_gap: bool
    requires_lead_coaching: bool
    estimated_lost_pipeline_usd: float
    lead_response_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                         self.rep_id,
            "region":                         self.region,
            "lead_response_risk":             self.lead_response_risk.value,
            "lead_response_pattern":          self.lead_response_pattern.value,
            "lead_response_severity":         self.lead_response_severity.value,
            "recommended_action":             self.recommended_action.value,
            "response_speed_score":           self.response_speed_score,
            "qualification_quality_score":    self.qualification_quality_score,
            "lead_conversion_score":          self.lead_conversion_score,
            "lead_discipline_score":          self.lead_discipline_score,
            "lead_response_composite":        self.lead_response_composite,
            "has_response_gap":               self.has_response_gap,
            "requires_lead_coaching":         self.requires_lead_coaching,
            "estimated_lost_pipeline_usd":    self.estimated_lost_pipeline_usd,
            "lead_response_signal":           self.lead_response_signal,
        }


class SalesInboundLeadResponseEngine:

    def __init__(self) -> None:
        self._results: list[InboundLeadResponseResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _response_speed_score(self, inp: InboundLeadResponseInput) -> float:
        score = 0.0

        if inp.avg_first_response_hours >= 24:
            score += 45.0
        elif inp.avg_first_response_hours >= 8:
            score += 25.0
        elif inp.avg_first_response_hours >= 2:
            score += 10.0

        total = max(inp.inbound_leads_assigned, 1)
        over_24_rate = inp.leads_contacted_over_24h / total
        if over_24_rate >= 0.40:
            score += 30.0
        elif over_24_rate >= 0.25:
            score += 15.0
        elif over_24_rate >= 0.10:
            score += 5.0

        within_1h_rate = inp.leads_contacted_within_1h / total
        if within_1h_rate < 0.20:
            score += 15.0
        elif within_1h_rate < 0.40:
            score += 7.0

        return min(score, 100.0)

    def _qualification_quality_score(self, inp: InboundLeadResponseInput) -> float:
        score = 0.0

        if inp.avg_lead_qualification_score < 4.0:
            score += 40.0
        elif inp.avg_lead_qualification_score < 6.0:
            score += 20.0
        elif inp.avg_lead_qualification_score < 7.5:
            score += 8.0

        if inp.avg_response_quality_score < 4.0:
            score += 30.0
        elif inp.avg_response_quality_score < 6.0:
            score += 15.0

        total = max(inp.inbound_leads_assigned, 1)
        disq_rate = inp.leads_disqualified_too_early / total
        if disq_rate >= 0.20:
            score += 20.0
        elif disq_rate >= 0.10:
            score += 10.0

        return min(score, 100.0)

    def _lead_conversion_score(self, inp: InboundLeadResponseInput) -> float:
        score = 0.0

        if inp.lead_to_qualified_conversion_rate_pct < 0.20:
            score += 35.0
        elif inp.lead_to_qualified_conversion_rate_pct < 0.35:
            score += 18.0
        elif inp.lead_to_qualified_conversion_rate_pct < 0.50:
            score += 7.0

        if inp.qualified_to_opportunity_conversion_rate_pct < 0.40:
            score += 30.0
        elif inp.qualified_to_opportunity_conversion_rate_pct < 0.60:
            score += 15.0

        icp_denom = max(inp.high_icp_leads_received, 1)
        icp_conv = inp.high_icp_leads_converted / icp_denom
        if inp.high_icp_leads_received > 0 and icp_conv < 0.30:
            score += 25.0
        elif inp.high_icp_leads_received > 0 and icp_conv < 0.55:
            score += 12.0

        return min(score, 100.0)

    def _lead_discipline_score(self, inp: InboundLeadResponseInput) -> float:
        score = 0.0
        total = max(inp.inbound_leads_assigned, 1)

        never_rate = inp.leads_never_contacted / total
        if never_rate >= 0.20:
            score += 40.0
        elif never_rate >= 0.10:
            score += 20.0
        elif never_rate >= 0.05:
            score += 8.0

        if inp.crm_lead_entry_rate_pct < 0.50:
            score += 30.0
        elif inp.crm_lead_entry_rate_pct < 0.75:
            score += 15.0

        if inp.leads_lost_to_competitor_before_contact >= 3:
            score += 20.0
        elif inp.leads_lost_to_competitor_before_contact >= 1:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: InboundLeadResponseInput,
                          speed: float, quality: float,
                          conversion: float, discipline: float) -> LeadResponsePattern:
        # Priority: lead_neglect > slow_response > icp_miss > low_conversion
        #           > poor_qualification > none
        total = max(inp.inbound_leads_assigned, 1)
        never_rate = inp.leads_never_contacted / total
        if discipline >= 35 and never_rate >= 0.15:
            return LeadResponsePattern.lead_neglect

        if speed >= 35 and inp.avg_first_response_hours >= 12:
            return LeadResponsePattern.slow_response

        icp_denom = max(inp.high_icp_leads_received, 1)
        icp_conv = inp.high_icp_leads_converted / icp_denom
        if conversion >= 30 and inp.high_icp_leads_received >= 3 and icp_conv < 0.40:
            return LeadResponsePattern.icp_miss

        if conversion >= 30 and inp.lead_to_qualified_conversion_rate_pct < 0.30:
            return LeadResponsePattern.low_conversion

        if quality >= 30 and inp.avg_lead_qualification_score < 5.5:
            return LeadResponsePattern.poor_qualification

        return LeadResponsePattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> LeadResponseRisk:
        if composite >= 60:
            return LeadResponseRisk.critical
        if composite >= 40:
            return LeadResponseRisk.high
        if composite >= 20:
            return LeadResponseRisk.moderate
        return LeadResponseRisk.low

    def _severity(self, composite: float) -> LeadResponseSeverity:
        if composite >= 60:
            return LeadResponseSeverity.critical
        if composite >= 40:
            return LeadResponseSeverity.lagging
        if composite >= 20:
            return LeadResponseSeverity.delayed
        return LeadResponseSeverity.responsive

    def _action(self, risk: LeadResponseRisk, pattern: LeadResponsePattern) -> LeadResponseAction:
        if risk == LeadResponseRisk.critical:
            if pattern == LeadResponsePattern.lead_neglect:
                return LeadResponseAction.lead_cadence_reset
            if pattern == LeadResponsePattern.slow_response:
                return LeadResponseAction.response_time_coaching
            return LeadResponseAction.lead_prioritization
        if risk == LeadResponseRisk.high:
            if pattern == LeadResponsePattern.poor_qualification:
                return LeadResponseAction.qualification_training
            if pattern == LeadResponsePattern.icp_miss:
                return LeadResponseAction.lead_prioritization
            return LeadResponseAction.crm_discipline
        if risk == LeadResponseRisk.moderate:
            return LeadResponseAction.response_time_coaching
        return LeadResponseAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_response_gap(self, composite: float,
                           inp: InboundLeadResponseInput) -> bool:
        total = max(inp.inbound_leads_assigned, 1)
        never_rate = inp.leads_never_contacted / total
        return (
            composite >= 40
            or inp.avg_first_response_hours >= 12
            or never_rate >= 0.10
        )

    def _requires_lead_coaching(self, composite: float,
                                  inp: InboundLeadResponseInput) -> bool:
        return (
            composite >= 30
            or inp.avg_lead_qualification_score < 5.0
            or inp.lead_to_qualified_conversion_rate_pct < 0.30
        )

    # ------------------------------------------------------------------
    # Lost pipeline
    # ------------------------------------------------------------------

    def _estimated_lost_pipeline(self, inp: InboundLeadResponseInput,
                                   composite: float) -> float:
        return round(
            inp.leads_never_contacted * inp.avg_lead_revenue_potential_usd * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: InboundLeadResponseInput,
                 pattern: LeadResponsePattern, composite: float) -> str:
        if pattern == LeadResponsePattern.none and composite < 20:
            return "Inbound lead response rate and quality within benchmarks"
        parts: list[str] = []
        if inp.leads_never_contacted >= 1:
            parts.append(f"{inp.leads_never_contacted} leads never contacted")
        if inp.avg_first_response_hours >= 4:
            parts.append(f"{inp.avg_first_response_hours:.0f}h avg response time")
        if inp.leads_lost_to_competitor_before_contact >= 1:
            parts.append(f"{inp.leads_lost_to_competitor_before_contact} lost to competitor")
        label = pattern.value.replace("_", " ") if pattern != LeadResponsePattern.none else "Lead response risk"
        summary = " — ".join(parts) if parts else "lead response quality degrading"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: InboundLeadResponseInput) -> InboundLeadResponseResult:
        speed      = round(self._response_speed_score(inp), 1)
        quality    = round(self._qualification_quality_score(inp), 1)
        conversion = round(self._lead_conversion_score(inp), 1)
        discipline = round(self._lead_discipline_score(inp), 1)

        composite = round(speed * 0.30 + quality * 0.30 + conversion * 0.25 + discipline * 0.15, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, speed, quality, conversion, discipline)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap      = self._has_response_gap(composite, inp)
        coaching = self._requires_lead_coaching(composite, inp)
        lost     = self._estimated_lost_pipeline(inp, composite)
        signal   = self._signal(inp, pattern, composite)

        result = InboundLeadResponseResult(
            rep_id=inp.rep_id,
            region=inp.region,
            lead_response_risk=risk,
            lead_response_pattern=pattern,
            lead_response_severity=severity,
            recommended_action=action,
            response_speed_score=speed,
            qualification_quality_score=quality,
            lead_conversion_score=conversion,
            lead_discipline_score=discipline,
            lead_response_composite=composite,
            has_response_gap=gap,
            requires_lead_coaching=coaching,
            estimated_lost_pipeline_usd=lost,
            lead_response_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[InboundLeadResponseInput]) -> list[InboundLeadResponseResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_lead_response_composite": 0.0,
                "response_gap_count": 0,
                "lead_coaching_count": 0,
                "avg_response_speed_score": 0.0,
                "avg_qualification_quality_score": 0.0,
                "avg_lead_conversion_score": 0.0,
                "avg_lead_discipline_score": 0.0,
                "total_estimated_lost_pipeline_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_sp = total_qu = total_co = total_di = total_lost = 0.0

        for r in self._results:
            risk_counts[r.lead_response_risk.value]       = risk_counts.get(r.lead_response_risk.value, 0) + 1
            pattern_counts[r.lead_response_pattern.value] = pattern_counts.get(r.lead_response_pattern.value, 0) + 1
            severity_counts[r.lead_response_severity.value] = severity_counts.get(r.lead_response_severity.value, 0) + 1
            action_counts[r.recommended_action.value]        = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.lead_response_composite
            total_sp   += r.response_speed_score
            total_qu   += r.qualification_quality_score
            total_co   += r.lead_conversion_score
            total_di   += r.lead_discipline_score
            total_lost += r.estimated_lost_pipeline_usd

        n = len(self._results)

        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_lead_response_composite":          round(total_comp / n, 1),
            "response_gap_count":                   sum(1 for r in self._results if r.has_response_gap),
            "lead_coaching_count":                  sum(1 for r in self._results if r.requires_lead_coaching),
            "avg_response_speed_score":             round(total_sp / n, 1),
            "avg_qualification_quality_score":      round(total_qu / n, 1),
            "avg_lead_conversion_score":            round(total_co / n, 1),
            "avg_lead_discipline_score":            round(total_di / n, 1),
            "total_estimated_lost_pipeline_usd":    round(total_lost, 2),
        }
