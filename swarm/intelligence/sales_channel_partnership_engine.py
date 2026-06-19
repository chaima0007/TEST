from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ChannelRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ChannelPattern(str, Enum):
    none                    = "none"
    channel_conflict        = "channel_conflict"
    partner_underperformance = "partner_underperformance"
    coverage_gap            = "coverage_gap"
    margin_erosion          = "margin_erosion"
    channel_cannibalization = "channel_cannibalization"


class ChannelSeverity(str, Enum):
    optimized = "optimized"
    stable    = "stable"
    degraded  = "degraded"
    critical  = "critical"


class ChannelAction(str, Enum):
    no_action             = "no_action"
    channel_monitoring    = "channel_monitoring"
    partner_enablement    = "partner_enablement"
    conflict_mediation    = "conflict_mediation"
    coverage_expansion    = "coverage_expansion"
    margin_protection     = "margin_protection"
    channel_restructuring = "channel_restructuring"
    partner_termination   = "partner_termination"
    emergency_rebalancing = "emergency_rebalancing"


@dataclass
class ChannelInput:
    channel_id: str
    channel_type: str
    region: str
    channel_revenue_contribution: float
    partner_performance_score: float
    channel_coverage_score: float
    margin_per_channel: float
    conflict_index: float
    partner_engagement_score: float
    certification_compliance_pct: float
    deal_registration_rate: float
    channel_marketing_roi: float
    co_selling_effectiveness: float
    partner_churn_risk: float
    territory_overlap_score: float
    icp_alignment_score: float
    training_program_effectiveness: float
    revenue_forecast_accuracy: float
    digital_channel_adoption: float
    partner_satisfaction_score: float


@dataclass
class ChannelResult:
    channel_id: str
    region: str
    channel_risk: str
    channel_pattern: str
    channel_severity: str
    recommended_action: str
    performance_score: float
    coverage_score: float
    health_score: float
    enablement_score: float
    channel_composite: float
    has_channel_alert: bool
    requires_strategic_review: bool
    estimated_channel_risk_index: float
    channel_signal: str

    def to_dict(self) -> Dict:
        return {
            "channel_id":                    self.channel_id,
            "region":                        self.region,
            "channel_risk":                  self.channel_risk,
            "channel_pattern":               self.channel_pattern,
            "channel_severity":              self.channel_severity,
            "recommended_action":            self.recommended_action,
            "performance_score":             self.performance_score,
            "coverage_score":                self.coverage_score,
            "health_score":                  self.health_score,
            "enablement_score":              self.enablement_score,
            "channel_composite":             self.channel_composite,
            "has_channel_alert":             self.has_channel_alert,
            "requires_strategic_review":     self.requires_strategic_review,
            "estimated_channel_risk_index":  self.estimated_channel_risk_index,
            "channel_signal":                self.channel_signal,
        }


class SalesChannelPartnershipEngine:
    def __init__(self) -> None:
        self._results: List[ChannelResult] = []

    def _performance_score(self, i: ChannelInput) -> float:
        s = 0
        if   i.partner_performance_score <= 0.30: s += 40
        elif i.partner_performance_score <= 0.55: s += 22
        elif i.partner_performance_score <= 0.75: s += 8

        if   i.channel_revenue_contribution <= 0.20: s += 35
        elif i.channel_revenue_contribution <= 0.45: s += 18
        elif i.channel_revenue_contribution <= 0.65: s += 6

        if   i.revenue_forecast_accuracy <= 0.30: s += 25
        elif i.revenue_forecast_accuracy <= 0.55: s += 12
        return min(s, 100)

    def _coverage_score(self, i: ChannelInput) -> float:
        s = 0
        if   i.channel_coverage_score <= 0.30: s += 40
        elif i.channel_coverage_score <= 0.55: s += 22
        elif i.channel_coverage_score <= 0.75: s += 8

        if   i.territory_overlap_score >= 0.70: s += 35
        elif i.territory_overlap_score >= 0.45: s += 18
        elif i.territory_overlap_score >= 0.25: s += 6

        if   i.icp_alignment_score <= 0.30: s += 25
        elif i.icp_alignment_score <= 0.55: s += 12
        return min(s, 100)

    def _health_score(self, i: ChannelInput) -> float:
        s = 0
        if   i.conflict_index >= 0.70: s += 40
        elif i.conflict_index >= 0.45: s += 22
        elif i.conflict_index >= 0.25: s += 8

        if   i.partner_churn_risk >= 0.70: s += 35
        elif i.partner_churn_risk >= 0.45: s += 18
        elif i.partner_churn_risk >= 0.25: s += 6

        if   i.partner_satisfaction_score <= 0.30: s += 25
        elif i.partner_satisfaction_score <= 0.55: s += 12
        return min(s, 100)

    def _enablement_score(self, i: ChannelInput) -> float:
        s = 0
        if   i.training_program_effectiveness <= 0.30: s += 40
        elif i.training_program_effectiveness <= 0.55: s += 22
        elif i.training_program_effectiveness <= 0.75: s += 8

        if   i.certification_compliance_pct <= 0.30: s += 35
        elif i.certification_compliance_pct <= 0.55: s += 18
        elif i.certification_compliance_pct <= 0.75: s += 6

        if   i.co_selling_effectiveness <= 0.30: s += 25
        elif i.co_selling_effectiveness <= 0.55: s += 12
        return min(s, 100)

    def _composite(self, perf: float, cov: float, hlth: float, enab: float) -> float:
        return min(round(perf * 0.30 + cov * 0.25 + hlth * 0.25 + enab * 0.20, 2), 100.0)

    def _risk(self, c: float) -> ChannelRisk:
        if c >= 60: return ChannelRisk.critical
        if c >= 40: return ChannelRisk.high
        if c >= 20: return ChannelRisk.moderate
        return ChannelRisk.low

    def _severity(self, c: float) -> ChannelSeverity:
        if c >= 60: return ChannelSeverity.critical
        if c >= 40: return ChannelSeverity.degraded
        if c >= 20: return ChannelSeverity.stable
        return ChannelSeverity.optimized

    def _pattern(self, i: ChannelInput) -> ChannelPattern:
        if i.conflict_index >= 0.5 or i.territory_overlap_score >= 0.6:
            return ChannelPattern.channel_conflict
        if i.partner_performance_score <= 0.4 and i.partner_engagement_score <= 0.4:
            return ChannelPattern.partner_underperformance
        if i.margin_per_channel <= 0.35:
            return ChannelPattern.margin_erosion
        if i.channel_coverage_score <= 0.4 or i.icp_alignment_score <= 0.35:
            return ChannelPattern.coverage_gap
        if i.territory_overlap_score >= 0.55 and i.channel_revenue_contribution >= 0.6:
            return ChannelPattern.channel_cannibalization
        return ChannelPattern.none

    def _action(self, risk: ChannelRisk, pat: ChannelPattern) -> ChannelAction:
        if risk == ChannelRisk.critical:
            if pat == ChannelPattern.channel_conflict:         return ChannelAction.emergency_rebalancing
            if pat == ChannelPattern.margin_erosion:           return ChannelAction.channel_restructuring
            if pat == ChannelPattern.partner_underperformance: return ChannelAction.partner_termination
            return ChannelAction.emergency_rebalancing
        if risk == ChannelRisk.high:
            if pat == ChannelPattern.channel_conflict:         return ChannelAction.conflict_mediation
            if pat == ChannelPattern.partner_underperformance: return ChannelAction.partner_enablement
            if pat == ChannelPattern.margin_erosion:           return ChannelAction.margin_protection
            if pat == ChannelPattern.coverage_gap:             return ChannelAction.coverage_expansion
            return ChannelAction.channel_monitoring
        if risk == ChannelRisk.moderate:
            return ChannelAction.channel_monitoring
        return ChannelAction.no_action

    def _has_alert(self, i: ChannelInput, comp: float) -> bool:
        return (comp >= 40
                or i.partner_churn_risk >= 0.55
                or i.conflict_index >= 0.5
                or i.margin_per_channel <= 0.3)

    def _requires_review(self, i: ChannelInput, comp: float) -> bool:
        return (comp >= 25
                or i.channel_coverage_score <= 0.35
                or i.partner_performance_score <= 0.35)

    def _risk_index(self, i: ChannelInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.partner_satisfaction_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: ChannelInput, pat: ChannelPattern, comp: float) -> str:
        if comp < 20:
            return "Canaux de vente performants — partenaires engagés, couverture optimale, marges protégées"
        labels = {
            ChannelPattern.channel_conflict:         "Conflit canal",
            ChannelPattern.partner_underperformance: "Sous-performance partenaire",
            ChannelPattern.margin_erosion:           "Érosion marge",
            ChannelPattern.coverage_gap:             "Lacune couverture",
            ChannelPattern.channel_cannibalization:  "Cannibalisation canal",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — performance partenaires {round(i.partner_performance_score * 100)}%"
            f" — conflits {round(i.conflict_index * 100)}%"
            f" — couverture {round(i.channel_coverage_score * 100)}%"
            f" — composite {round(comp)}"
        )

    def assess(self, i: ChannelInput) -> ChannelResult:
        perf = self._performance_score(i)
        cov  = self._coverage_score(i)
        hlth = self._health_score(i)
        enab = self._enablement_score(i)
        comp = self._composite(perf, cov, hlth, enab)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = ChannelResult(
            channel_id=i.channel_id,
            region=i.region,
            channel_risk=risk.value,
            channel_pattern=pat.value,
            channel_severity=sev.value,
            recommended_action=act.value,
            performance_score=perf,
            coverage_score=cov,
            health_score=hlth,
            enablement_score=enab,
            channel_composite=comp,
            has_channel_alert=self._has_alert(i, comp),
            requires_strategic_review=self._requires_review(i, comp),
            estimated_channel_risk_index=self._risk_index(i, comp),
            channel_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[ChannelInput]) -> List[ChannelResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_channel_composite": 0.0,
                "channel_alert_count": 0,
                "strategic_review_count": 0,
                "avg_performance_score": 0.0,
                "avg_coverage_score": 0.0,
                "avg_health_score": 0.0,
                "avg_enablement_score": 0.0,
                "avg_estimated_channel_risk_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tperf = tcov = thlth = tenab = tcomp = tridx = 0.0
        alert_count = review_count = 0
        for r in self._results:
            rc[r.channel_risk]     = rc.get(r.channel_risk, 0)     + 1
            pc[r.channel_pattern]  = pc.get(r.channel_pattern, 0)  + 1
            sc[r.channel_severity] = sc.get(r.channel_severity, 0) + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tperf += r.performance_score
            tcov  += r.coverage_score
            thlth += r.health_score
            tenab += r.enablement_score
            tcomp += r.channel_composite
            tridx += r.estimated_channel_risk_index
            if r.has_channel_alert:        alert_count  += 1
            if r.requires_strategic_review: review_count += 1
        return {
            "total":                             n,
            "risk_counts":                       rc,
            "pattern_counts":                    pc,
            "severity_counts":                   sc,
            "action_counts":                     ac,
            "avg_channel_composite":             round(tcomp / n, 1),
            "channel_alert_count":               alert_count,
            "strategic_review_count":            review_count,
            "avg_performance_score":             round(tperf / n, 1),
            "avg_coverage_score":                round(tcov / n, 1),
            "avg_health_score":                  round(thlth / n, 1),
            "avg_enablement_score":              round(tenab / n, 1),
            "avg_estimated_channel_risk_index":  round(tridx / n, 2),
        }
