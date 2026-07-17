from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class LifecycleRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class LifecyclePattern(str, Enum):
    none                    = "none"
    churn_trajectory        = "churn_trajectory"
    expansion_stall         = "expansion_stall"
    adoption_lag            = "adoption_lag"
    renewal_cliff           = "renewal_cliff"
    dormant_account         = "dormant_account"


class LifecycleSeverity(str, Enum):
    thriving   = "thriving"
    stable     = "stable"
    declining  = "declining"
    critical   = "critical"


class LifecycleAction(str, Enum):
    no_action                    = "no_action"
    health_monitoring            = "health_monitoring"
    adoption_coaching            = "adoption_coaching"
    expansion_play               = "expansion_play"
    churn_prevention_outreach    = "churn_prevention_outreach"
    executive_escalation         = "executive_escalation"
    emergency_save_intervention  = "emergency_save_intervention"


@dataclass
class LifecycleInput:
    rep_id:                         str
    region:                         str
    evaluation_period_id:           str
    product_adoption_score:         float   # 0-1
    feature_utilization_pct:        float   # 0-1
    login_frequency_per_week:       float   # count
    support_ticket_rate_per_month:  float   # count
    nps_score:                      float   # -100 to 100 (normalized 0-1 for scoring)
    contract_renewal_days_out:      float   # days until renewal
    days_since_last_meaningful_touch: float # days
    expansion_revenue_pct:          float   # 0-1 (upsell/cross-sell as pct of ARR)
    churn_signal_count:             int     # explicit churn signals this period
    exec_sponsor_engaged:           float   # 0-1 (bool-like)
    multi_dept_usage_pct:           float   # 0-1 departments actively using
    health_score_trend:             float   # -1 to +1 (negative = declining)
    onboarding_completion_pct:      float   # 0-1
    time_to_value_days:             float   # days
    competitive_mention_count:      int     # competitor mentions in calls
    qbr_completion_rate:            float   # 0-1
    customer_age_months:            float   # months as customer
    total_arr_usd:                  float   # annual recurring revenue
    avg_arr_per_user_usd:           float   # per seat value


@dataclass
class LifecycleResult:
    rep_id:                         str
    region:                         str
    lifecycle_risk:                 LifecycleRisk
    lifecycle_pattern:              LifecyclePattern
    lifecycle_severity:             LifecycleSeverity
    recommended_action:             LifecycleAction
    adoption_score:                 float
    engagement_score:               float
    renewal_readiness_score:        float
    expansion_potential_score:      float
    lifecycle_composite:            float
    has_lifecycle_gap:              bool
    requires_lifecycle_intervention: bool
    estimated_churn_risk_usd:       float
    lifecycle_signal:               str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "lifecycle_risk":                   self.lifecycle_risk.value,
            "lifecycle_pattern":                self.lifecycle_pattern.value,
            "lifecycle_severity":               self.lifecycle_severity.value,
            "recommended_action":               self.recommended_action.value,
            "adoption_score":                   self.adoption_score,
            "engagement_score":                 self.engagement_score,
            "renewal_readiness_score":          self.renewal_readiness_score,
            "expansion_potential_score":        self.expansion_potential_score,
            "lifecycle_composite":              self.lifecycle_composite,
            "has_lifecycle_gap":                self.has_lifecycle_gap,
            "requires_lifecycle_intervention":  self.requires_lifecycle_intervention,
            "estimated_churn_risk_usd":         self.estimated_churn_risk_usd,
            "lifecycle_signal":                 self.lifecycle_signal,
        }


class SalesCustomerLifecycleIntelligenceEngine:
    """Detects churn trajectories, expansion stalls, adoption lags, and renewal cliffs per rep/account."""

    def __init__(self) -> None:
        self._results: List[LifecycleResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _adoption_score(self, inp: LifecycleInput) -> float:
        s = 0.0
        if   inp.product_adoption_score    <= 0.30: s += 40
        elif inp.product_adoption_score    <= 0.55: s += 22
        elif inp.product_adoption_score    <= 0.75: s += 8
        if   inp.feature_utilization_pct   <= 0.25: s += 35
        elif inp.feature_utilization_pct   <= 0.50: s += 18
        if   inp.onboarding_completion_pct <= 0.60: s += 25
        elif inp.onboarding_completion_pct <= 0.80: s += 12
        return min(s, 100.0)

    def _engagement_score(self, inp: LifecycleInput) -> float:
        s = 0.0
        if   inp.days_since_last_meaningful_touch >= 60: s += 40
        elif inp.days_since_last_meaningful_touch >= 30: s += 22
        elif inp.days_since_last_meaningful_touch >= 14: s += 8
        if   inp.login_frequency_per_week          <= 1: s += 35
        elif inp.login_frequency_per_week          <= 3: s += 18
        if   inp.qbr_completion_rate               <= 0.25: s += 25
        elif inp.qbr_completion_rate               <= 0.60: s += 12
        return min(s, 100.0)

    def _renewal_readiness_score(self, inp: LifecycleInput) -> float:
        s = 0.0
        if   inp.contract_renewal_days_out <= 30:  s += 40
        elif inp.contract_renewal_days_out <= 60:  s += 22
        elif inp.contract_renewal_days_out <= 90:  s += 8
        if   inp.churn_signal_count        >= 4:   s += 35
        elif inp.churn_signal_count        >= 2:   s += 18
        if   inp.health_score_trend        <= -0.40: s += 25
        elif inp.health_score_trend        <= -0.15: s += 12
        return min(s, 100.0)

    def _expansion_potential_score(self, inp: LifecycleInput) -> float:
        s = 0.0
        if   inp.expansion_revenue_pct   <= 0.05: s += 45
        elif inp.expansion_revenue_pct   <= 0.15: s += 25
        elif inp.expansion_revenue_pct   <= 0.25: s += 10
        if   inp.multi_dept_usage_pct    <= 0.20: s += 30
        elif inp.multi_dept_usage_pct    <= 0.40: s += 15
        if   inp.exec_sponsor_engaged    <= 0.25: s += 25
        elif inp.exec_sponsor_engaged    <= 0.60: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, ad: float, en: float, rr: float, ep: float) -> float:
        return min(round(ad * 0.30 + en * 0.25 + rr * 0.25 + ep * 0.20, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: LifecycleInput) -> LifecyclePattern:
        if inp.churn_signal_count >= 3 and inp.health_score_trend <= -0.30:
            return LifecyclePattern.churn_trajectory
        if inp.expansion_revenue_pct <= 0.05 and inp.customer_age_months >= 12:
            return LifecyclePattern.expansion_stall
        if inp.product_adoption_score <= 0.35 and inp.onboarding_completion_pct <= 0.65:
            return LifecyclePattern.adoption_lag
        if inp.contract_renewal_days_out <= 45 and inp.churn_signal_count >= 1:
            return LifecyclePattern.renewal_cliff
        if inp.days_since_last_meaningful_touch >= 45 and inp.login_frequency_per_week <= 1:
            return LifecyclePattern.dormant_account
        return LifecyclePattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> LifecycleRisk:
        if   composite >= 60: return LifecycleRisk.critical
        elif composite >= 40: return LifecycleRisk.high
        elif composite >= 20: return LifecycleRisk.moderate
        return LifecycleRisk.low

    def _severity(self, composite: float) -> LifecycleSeverity:
        if   composite >= 60: return LifecycleSeverity.critical
        elif composite >= 40: return LifecycleSeverity.declining
        elif composite >= 20: return LifecycleSeverity.stable
        return LifecycleSeverity.thriving

    def _action(self, risk: LifecycleRisk, pattern: LifecyclePattern) -> LifecycleAction:
        if risk == LifecycleRisk.critical:
            if pattern in (LifecyclePattern.churn_trajectory, LifecyclePattern.renewal_cliff):
                return LifecycleAction.emergency_save_intervention
            return LifecycleAction.executive_escalation
        if risk == LifecycleRisk.high:
            if pattern == LifecyclePattern.churn_trajectory:
                return LifecycleAction.churn_prevention_outreach
            if pattern == LifecyclePattern.expansion_stall:
                return LifecycleAction.expansion_play
            if pattern == LifecyclePattern.adoption_lag:
                return LifecycleAction.adoption_coaching
            if pattern == LifecyclePattern.renewal_cliff:
                return LifecycleAction.churn_prevention_outreach
            if pattern == LifecyclePattern.dormant_account:
                return LifecycleAction.churn_prevention_outreach
            return LifecycleAction.churn_prevention_outreach
        if risk == LifecycleRisk.moderate:
            return LifecycleAction.health_monitoring
        return LifecycleAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: LifecycleInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.product_adoption_score          <= 0.50
            or inp.churn_signal_count              >= 2
        )

    def _requires_intervention(self, inp: LifecycleInput, composite: float) -> bool:
        return (
            composite >= 30
            or inp.health_score_trend              <= -0.20
            or inp.contract_renewal_days_out       <= 60
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _churn_risk(self, inp: LifecycleInput, composite: float) -> float:
        churn_prob = min(1.0, (composite / 100) * (1 + inp.churn_signal_count * 0.10))
        return round(inp.total_arr_usd * churn_prob, 2)

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        LifecyclePattern.churn_trajectory:  "Churn trajectory",
        LifecyclePattern.expansion_stall:   "Expansion stall",
        LifecyclePattern.adoption_lag:      "Adoption lag",
        LifecyclePattern.renewal_cliff:     "Renewal cliff",
        LifecyclePattern.dormant_account:   "Dormant account",
    }

    def _signal(self, inp: LifecycleInput, pattern: LifecyclePattern, composite: float) -> str:
        if composite < 20:
            return (
                "Customer lifecycle healthy — strong adoption, engagement, "
                "renewal readiness, and expansion trajectory"
            )
        label      = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        adopt_pct  = round(inp.product_adoption_score * 100)
        touch_days = round(inp.days_since_last_meaningful_touch)
        renew_days = round(inp.contract_renewal_days_out)
        comp_int   = round(composite)
        return (
            f"{label} — {adopt_pct}% adoption — "
            f"{touch_days}d since last touch — "
            f"{renew_days}d to renewal — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: LifecycleInput) -> LifecycleResult:
        ad  = self._adoption_score(inp)
        en  = self._engagement_score(inp)
        rr  = self._renewal_readiness_score(inp)
        ep  = self._expansion_potential_score(inp)
        comp = self._composite(ad, en, rr, ep)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = LifecycleResult(
            rep_id                          = inp.rep_id,
            region                          = inp.region,
            lifecycle_risk                  = risk,
            lifecycle_pattern               = pattern,
            lifecycle_severity              = severity,
            recommended_action              = action,
            adoption_score                  = ad,
            engagement_score                = en,
            renewal_readiness_score         = rr,
            expansion_potential_score       = ep,
            lifecycle_composite             = comp,
            has_lifecycle_gap               = self._has_gap(inp, comp),
            requires_lifecycle_intervention = self._requires_intervention(inp, comp),
            estimated_churn_risk_usd        = self._churn_risk(inp, comp),
            lifecycle_signal                = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[LifecycleInput]) -> List[LifecycleResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_lifecycle_composite": 0.0,
                "lifecycle_gap_count": 0,
                "intervention_count": 0,
                "avg_adoption_score": 0.0,
                "avg_engagement_score": 0.0,
                "avg_renewal_readiness_score": 0.0,
                "avg_expansion_potential_score": 0.0,
                "total_estimated_churn_risk_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_ad = total_en = total_rr = total_ep = total_cr = 0.0
        gap_count = intervention_count = 0

        for res in self._results:
            risk_counts[res.lifecycle_risk.value]       = risk_counts.get(res.lifecycle_risk.value, 0) + 1
            pattern_counts[res.lifecycle_pattern.value] = pattern_counts.get(res.lifecycle_pattern.value, 0) + 1
            severity_counts[res.lifecycle_severity.value] = severity_counts.get(res.lifecycle_severity.value, 0) + 1
            action_counts[res.recommended_action.value] = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.lifecycle_composite
            total_ad   += res.adoption_score
            total_en   += res.engagement_score
            total_rr   += res.renewal_readiness_score
            total_ep   += res.expansion_potential_score
            total_cr   += res.estimated_churn_risk_usd
            if res.has_lifecycle_gap:               gap_count          += 1
            if res.requires_lifecycle_intervention: intervention_count += 1

        n = len(self._results)
        return {
            "total":                            n,
            "risk_counts":                      risk_counts,
            "pattern_counts":                   pattern_counts,
            "severity_counts":                  severity_counts,
            "action_counts":                    action_counts,
            "avg_lifecycle_composite":          round(total_comp / n, 1),
            "lifecycle_gap_count":              gap_count,
            "intervention_count":               intervention_count,
            "avg_adoption_score":               round(total_ad / n, 1),
            "avg_engagement_score":             round(total_en / n, 1),
            "avg_renewal_readiness_score":      round(total_rr / n, 1),
            "avg_expansion_potential_score":    round(total_ep / n, 1),
            "total_estimated_churn_risk_usd":   round(total_cr, 2),
        }
