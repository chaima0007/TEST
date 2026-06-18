from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class HealthRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class HealthPattern(str, Enum):
    none                   = "none"
    silent_churn_risk      = "silent_churn_risk"
    expansion_blocker      = "expansion_blocker"
    champion_departed      = "champion_departed"
    usage_collapse         = "usage_collapse"
    support_spiral         = "support_spiral"


class HealthSeverity(str, Enum):
    healthy     = "healthy"
    declining   = "declining"
    at_risk     = "at_risk"
    churning    = "churning"


class HealthAction(str, Enum):
    no_action                    = "no_action"
    health_monitoring            = "health_monitoring"
    executive_business_review    = "executive_business_review"
    champion_rebuild_plan        = "champion_rebuild_plan"
    usage_enablement_program     = "usage_enablement_program"
    support_escalation_review    = "support_escalation_review"
    churn_prevention_task_force  = "churn_prevention_task_force"


@dataclass
class HealthInput:
    rep_id:                              str
    region:                              str
    evaluation_period_id:                str
    product_usage_trend_pct:             float   # -1 to 1 (negative = dropping usage)
    nps_score_trend:                     float   # -1 to 1 (negative = declining NPS)
    support_ticket_volume_trend_pct:     float   # 0-1 (positive = more tickets)
    avg_ticket_severity_score:           float   # 0-1 (1 = all critical)
    renewal_probability_score:           float   # 0-1 (self-reported by rep)
    last_exec_engagement_days:           float   # days since last exec contact
    champion_change_events:              int     # # of champion changes in period
    contract_utilization_pct:            float   # 0-1 (% of contract being used)
    multi_product_adoption_rate_pct:     float   # 0-1
    qbr_attendance_rate_pct:             float   # 0-1
    expansion_pipeline_vs_arr_pct:       float   # 0-1 expansion pipe vs current ARR
    risk_flags_documented:               int     # # of risk flags in CRM
    competitor_evaluation_signals:       int     # # of signals of comp evaluation
    time_to_value_days:                  float   # days customer took to first value
    onboarding_completion_rate_pct:      float   # 0-1
    stakeholder_coverage_score:          float   # 0-1 (breadth of relationships)
    satisfaction_survey_response_rate:   float   # 0-1
    invoice_payment_on_time_rate_pct:    float   # 0-1
    total_accounts_managed:              int
    avg_arr_per_account_usd:             float


@dataclass
class HealthResult:
    rep_id:                          str
    region:                          str
    health_risk:                     HealthRisk
    health_pattern:                  HealthPattern
    health_severity:                 HealthSeverity
    recommended_action:              HealthAction
    engagement_score:                float
    adoption_score:                  float
    satisfaction_score:              float
    renewal_readiness_score:         float
    health_composite:                float
    has_health_gap:                  bool
    requires_health_intervention:    bool
    estimated_churn_arr_usd:         float
    health_signal:                   str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                        self.rep_id,
            "region":                        self.region,
            "health_risk":                   self.health_risk.value,
            "health_pattern":                self.health_pattern.value,
            "health_severity":               self.health_severity.value,
            "recommended_action":            self.recommended_action.value,
            "engagement_score":              self.engagement_score,
            "adoption_score":                self.adoption_score,
            "satisfaction_score":            self.satisfaction_score,
            "renewal_readiness_score":       self.renewal_readiness_score,
            "health_composite":              self.health_composite,
            "has_health_gap":                self.has_health_gap,
            "requires_health_intervention":  self.requires_health_intervention,
            "estimated_churn_arr_usd":       self.estimated_churn_arr_usd,
            "health_signal":                 self.health_signal,
        }


class SalesCustomerHealthScoreDeterioration(str, Enum):
    pass


class SalesCustomerHealthScoreDeteriorationEngine:
    """Detects accounts churning silently while reps report everything as green."""

    def __init__(self) -> None:
        self._results: List[HealthResult] = []

    # ── sub-scores ─────────────────────────────────────────────────────────────

    def _engagement_score(self, inp: HealthInput) -> float:
        s = 0.0
        if   inp.last_exec_engagement_days      >= 90:  s += 40
        elif inp.last_exec_engagement_days      >= 45:  s += 22
        elif inp.last_exec_engagement_days      >= 21:  s += 8
        if   inp.qbr_attendance_rate_pct        <= 0.25: s += 35
        elif inp.qbr_attendance_rate_pct        <= 0.55: s += 18
        if   inp.stakeholder_coverage_score     <= 0.20: s += 25
        elif inp.stakeholder_coverage_score     <= 0.45: s += 12
        return min(s, 100.0)

    def _adoption_score(self, inp: HealthInput) -> float:
        s = 0.0
        if   inp.product_usage_trend_pct        <= -0.25: s += 45
        elif inp.product_usage_trend_pct        <= -0.10: s += 25
        elif inp.product_usage_trend_pct        <= 0.0:   s += 10
        if   inp.contract_utilization_pct       <= 0.30: s += 30
        elif inp.contract_utilization_pct       <= 0.60: s += 15
        if   inp.onboarding_completion_rate_pct <= 0.40: s += 25
        elif inp.onboarding_completion_rate_pct <= 0.70: s += 12
        return min(s, 100.0)

    def _satisfaction_score(self, inp: HealthInput) -> float:
        s = 0.0
        if   inp.nps_score_trend                <= -0.30: s += 40
        elif inp.nps_score_trend                <= -0.10: s += 22
        elif inp.nps_score_trend                <= 0.0:   s += 8
        if   inp.support_ticket_volume_trend_pct >= 0.50: s += 35
        elif inp.support_ticket_volume_trend_pct >= 0.25: s += 18
        if   inp.avg_ticket_severity_score       >= 0.65: s += 25
        elif inp.avg_ticket_severity_score       >= 0.40: s += 12
        return min(s, 100.0)

    def _renewal_readiness_score(self, inp: HealthInput) -> float:
        s = 0.0
        if   inp.renewal_probability_score      <= 0.30: s += 45
        elif inp.renewal_probability_score      <= 0.55: s += 25
        elif inp.renewal_probability_score      <= 0.75: s += 10
        if   inp.competitor_evaluation_signals  >= 3:    s += 30
        elif inp.competitor_evaluation_signals  >= 1:    s += 15
        if   inp.risk_flags_documented          >= 4:    s += 25
        elif inp.risk_flags_documented          >= 2:    s += 12
        return min(s, 100.0)

    # ── composite ──────────────────────────────────────────────────────────────

    def _composite(self, en: float, ad: float, sa: float, rr: float) -> float:
        return min(round(en * 0.25 + ad * 0.30 + sa * 0.25 + rr * 0.20, 2), 100.0)

    # ── pattern ────────────────────────────────────────────────────────────────

    def _pattern(self, inp: HealthInput) -> HealthPattern:
        if inp.renewal_probability_score <= 0.35 and inp.risk_flags_documented >= 2 and inp.competitor_evaluation_signals >= 1:
            return HealthPattern.silent_churn_risk
        if inp.expansion_pipeline_vs_arr_pct <= 0.05 and inp.multi_product_adoption_rate_pct <= 0.15:
            return HealthPattern.expansion_blocker
        if inp.champion_change_events >= 2 and inp.stakeholder_coverage_score <= 0.30:
            return HealthPattern.champion_departed
        if inp.product_usage_trend_pct <= -0.20 and inp.contract_utilization_pct <= 0.40:
            return HealthPattern.usage_collapse
        if inp.support_ticket_volume_trend_pct >= 0.50 and inp.avg_ticket_severity_score >= 0.55:
            return HealthPattern.support_spiral
        return HealthPattern.none

    # ── thresholds ─────────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> HealthRisk:
        if   composite >= 60: return HealthRisk.critical
        elif composite >= 40: return HealthRisk.high
        elif composite >= 20: return HealthRisk.moderate
        return HealthRisk.low

    def _severity(self, composite: float) -> HealthSeverity:
        if   composite >= 60: return HealthSeverity.churning
        elif composite >= 40: return HealthSeverity.at_risk
        elif composite >= 20: return HealthSeverity.declining
        return HealthSeverity.healthy

    def _action(self, risk: HealthRisk, pattern: HealthPattern) -> HealthAction:
        if risk == HealthRisk.critical:
            if pattern in (HealthPattern.silent_churn_risk, HealthPattern.champion_departed):
                return HealthAction.churn_prevention_task_force
            return HealthAction.executive_business_review
        if risk == HealthRisk.high:
            if pattern == HealthPattern.silent_churn_risk:
                return HealthAction.executive_business_review
            if pattern == HealthPattern.expansion_blocker:
                return HealthAction.usage_enablement_program
            if pattern == HealthPattern.champion_departed:
                return HealthAction.champion_rebuild_plan
            if pattern == HealthPattern.usage_collapse:
                return HealthAction.usage_enablement_program
            if pattern == HealthPattern.support_spiral:
                return HealthAction.support_escalation_review
            return HealthAction.executive_business_review
        if risk == HealthRisk.moderate:
            return HealthAction.health_monitoring
        return HealthAction.no_action

    # ── flags ──────────────────────────────────────────────────────────────────

    def _has_gap(self, inp: HealthInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.renewal_probability_score    <= 0.65
            or inp.product_usage_trend_pct      <= -0.05
        )

    def _requires_intervention(self, inp: HealthInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.competitor_evaluation_signals >= 1
            or inp.champion_change_events        >= 1
        )

    # ── churn arr risk ─────────────────────────────────────────────────────────

    def _churn_arr(self, inp: HealthInput, composite: float) -> float:
        churn_probability = (composite / 100) * (1.0 - inp.renewal_probability_score)
        return round(inp.total_accounts_managed * inp.avg_arr_per_account_usd * churn_probability, 2)

    # ── signal ─────────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        HealthPattern.silent_churn_risk:  "Silent churn risk",
        HealthPattern.expansion_blocker:  "Expansion blocker",
        HealthPattern.champion_departed:  "Champion departed",
        HealthPattern.usage_collapse:     "Usage collapse",
        HealthPattern.support_spiral:     "Support spiral",
    }

    def _signal(self, inp: HealthInput, pattern: HealthPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Customer health stable — usage, NPS trend, renewal probability, "
                "and engagement within healthy benchmarks"
            )
        label    = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        usage    = round(inp.product_usage_trend_pct * 100)
        renew    = round(inp.renewal_probability_score * 100)
        exec_d   = round(inp.last_exec_engagement_days)
        comp_int = round(composite)
        return (
            f"{label} — {usage:+d}% usage trend — {renew}% renewal probability — "
            f"{exec_d}d since exec contact — composite {comp_int}"
        )

    # ── public API ─────────────────────────────────────────────────────────────

    def assess(self, inp: HealthInput) -> HealthResult:
        en   = self._engagement_score(inp)
        ad   = self._adoption_score(inp)
        sa   = self._satisfaction_score(inp)
        rr   = self._renewal_readiness_score(inp)
        comp = self._composite(en, ad, sa, rr)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = HealthResult(
            rep_id                       = inp.rep_id,
            region                       = inp.region,
            health_risk                  = risk,
            health_pattern               = pattern,
            health_severity              = severity,
            recommended_action           = action,
            engagement_score             = en,
            adoption_score               = ad,
            satisfaction_score           = sa,
            renewal_readiness_score      = rr,
            health_composite             = comp,
            has_health_gap               = self._has_gap(inp, comp),
            requires_health_intervention = self._requires_intervention(inp, comp),
            estimated_churn_arr_usd      = self._churn_arr(inp, comp),
            health_signal                = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[HealthInput]) -> List[HealthResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_health_composite": 0.0,
                "health_gap_count": 0,
                "intervention_count": 0,
                "avg_engagement_score": 0.0,
                "avg_adoption_score": 0.0,
                "avg_satisfaction_score": 0.0,
                "avg_renewal_readiness_score": 0.0,
                "total_estimated_churn_arr_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_en = total_ad = total_sa = total_rr = total_ca = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.health_risk.value]         = risk_counts.get(res.health_risk.value, 0) + 1
            pattern_counts[res.health_pattern.value]   = pattern_counts.get(res.health_pattern.value, 0) + 1
            severity_counts[res.health_severity.value] = severity_counts.get(res.health_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.health_composite
            total_en   += res.engagement_score
            total_ad   += res.adoption_score
            total_sa   += res.satisfaction_score
            total_rr   += res.renewal_readiness_score
            total_ca   += res.estimated_churn_arr_usd
            if res.has_health_gap:               gap_count          += 1
            if res.requires_health_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                            n,
            "risk_counts":                      risk_counts,
            "pattern_counts":                   pattern_counts,
            "severity_counts":                  severity_counts,
            "action_counts":                    action_counts,
            "avg_health_composite":             round(total_comp / n, 1),
            "health_gap_count":                 gap_count,
            "intervention_count":               intervention_count,
            "avg_engagement_score":             round(total_en / n, 1),
            "avg_adoption_score":               round(total_ad / n, 1),
            "avg_satisfaction_score":           round(total_sa / n, 1),
            "avg_renewal_readiness_score":      round(total_rr / n, 1),
            "total_estimated_churn_arr_usd":    round(total_ca, 2),
        }
