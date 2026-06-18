"""Customer LTV Erosion Detector — identifies when high-value customer relationships
are degrading through usage decline, engagement drop-off, expansion stall, and
executive relationship deterioration before churn occurs."""

from __future__ import annotations

import dataclasses
from enum import Enum


class ErosionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ErosionPattern(str, Enum):
    none                   = "none"
    usage_cliff            = "usage_cliff"
    exec_relationship_loss = "exec_relationship_loss"
    expansion_stall        = "expansion_stall"
    support_overload       = "support_overload"
    competitive_migration  = "competitive_migration"


class ErosionSeverity(str, Enum):
    healthy    = "healthy"
    watch      = "watch"
    degrading  = "degrading"
    critical   = "critical"


class ErosionAction(str, Enum):
    no_action             = "no_action"
    csm_outreach          = "csm_outreach"
    executive_qbr         = "executive_qbr"
    rescue_plan           = "rescue_plan"
    churn_prevention_team = "churn_prevention_team"


@dataclasses.dataclass
class CustomerLTVInput:
    customer_id:                      str
    csm_id:                           str
    evaluation_period_id:             str
    contract_arr_usd:                 float
    account_age_months:               int
    product_usage_score_last_30d:     float
    product_usage_score_prior_30d:    float
    feature_adoption_pct:             float
    benchmark_feature_adoption_pct:   float
    nps_score:                        int
    nps_score_prior:                  int
    executive_last_contact_days:      int
    executive_meetings_last_90d:      int
    executive_meetings_prior_90d:     int
    support_tickets_last_30d:         int
    support_tickets_prior_30d:        int
    critical_tickets_last_30d:        int
    expansion_revenue_last_12m_usd:   float
    expansion_revenue_prior_12m_usd:  float
    logo_at_risk_flag:                int
    competitor_evaluation_signal:     int
    renewal_days_remaining:           int


@dataclasses.dataclass
class CustomerLTVResult:
    customer_id:                  str
    csm_id:                       str
    erosion_risk:                 ErosionRisk
    erosion_pattern:              ErosionPattern
    erosion_severity:             ErosionSeverity
    recommended_action:           ErosionAction
    usage_decline_score:          float
    engagement_decay_score:       float
    expansion_health_score:       float
    relationship_risk_score:      float
    erosion_composite:            float
    is_at_churn_risk:             bool
    requires_executive_attention: bool
    estimated_arr_at_risk_usd:    float
    erosion_signal:               str

    def to_dict(self) -> dict:
        return {
            "customer_id":                  self.customer_id,
            "csm_id":                       self.csm_id,
            "erosion_risk":                 self.erosion_risk.value,
            "erosion_pattern":              self.erosion_pattern.value,
            "erosion_severity":             self.erosion_severity.value,
            "recommended_action":           self.recommended_action.value,
            "usage_decline_score":          round(self.usage_decline_score, 1),
            "engagement_decay_score":       round(self.engagement_decay_score, 1),
            "expansion_health_score":       round(self.expansion_health_score, 1),
            "relationship_risk_score":      round(self.relationship_risk_score, 1),
            "erosion_composite":            round(self.erosion_composite, 1),
            "is_at_churn_risk":             self.is_at_churn_risk,
            "requires_executive_attention": self.requires_executive_attention,
            "estimated_arr_at_risk_usd":    round(self.estimated_arr_at_risk_usd, 2),
            "erosion_signal":               self.erosion_signal,
        }


def _clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class CustomerLTVErosionDetector:
    """Detects LTV erosion to enable proactive retention before churn."""

    def __init__(self) -> None:
        self._results: list[CustomerLTVResult] = []

    # ── sub-scores (HIGHER = more erosion) ──────────────────────────────────

    def _usage_decline_score(self, inp: CustomerLTVInput) -> float:
        score = 0.0
        # Product usage decline
        if inp.product_usage_score_prior_30d > 0:
            usage_delta = (inp.product_usage_score_prior_30d - inp.product_usage_score_last_30d) / inp.product_usage_score_prior_30d
            if usage_delta >= 0.40:
                score += 45.0
            elif usage_delta >= 0.25:
                score += 28.0
            elif usage_delta >= 0.10:
                score += 14.0
            elif usage_delta >= 0.05:
                score += 6.0
        # Feature adoption vs benchmark
        adoption_gap = inp.benchmark_feature_adoption_pct - inp.feature_adoption_pct
        if adoption_gap >= 40:
            score += 30.0
        elif adoption_gap >= 25:
            score += 18.0
        elif adoption_gap >= 10:
            score += 8.0
        # Support overload as usage stress indicator
        if inp.critical_tickets_last_30d >= 3:
            score += 25.0
        elif inp.critical_tickets_last_30d >= 1:
            score += 12.0
        return _clamp(score)

    def _engagement_decay_score(self, inp: CustomerLTVInput) -> float:
        score = 0.0
        # NPS decline
        nps_delta = inp.nps_score_prior - inp.nps_score
        if nps_delta >= 30:
            score += 40.0
        elif nps_delta >= 20:
            score += 25.0
        elif nps_delta >= 10:
            score += 12.0
        # Absolute NPS low
        if inp.nps_score <= 20:
            score += 30.0
        elif inp.nps_score <= 40:
            score += 15.0
        # Support ticket surge (frustration signal)
        if inp.support_tickets_prior_30d > 0:
            ticket_ratio = inp.support_tickets_last_30d / inp.support_tickets_prior_30d
            if ticket_ratio >= 3.0:
                score += 30.0
            elif ticket_ratio >= 2.0:
                score += 18.0
            elif ticket_ratio >= 1.5:
                score += 8.0
        return _clamp(score)

    def _expansion_health_score(self, inp: CustomerLTVInput) -> float:
        score = 0.0
        # Expansion revenue decline
        if inp.expansion_revenue_prior_12m_usd > 0:
            exp_delta = (inp.expansion_revenue_prior_12m_usd - inp.expansion_revenue_last_12m_usd) / inp.expansion_revenue_prior_12m_usd
            if exp_delta >= 0.5:
                score += 40.0
            elif exp_delta >= 0.3:
                score += 25.0
            elif exp_delta >= 0.1:
                score += 12.0
        elif inp.expansion_revenue_last_12m_usd == 0 and inp.account_age_months >= 24:
            score += 20.0
        # Logo at risk flag
        if inp.logo_at_risk_flag == 1:
            score += 35.0
        # Renewal urgency with low health
        if inp.renewal_days_remaining <= 30:
            score += 25.0
        elif inp.renewal_days_remaining <= 60:
            score += 12.0
        return _clamp(score)

    def _relationship_risk_score(self, inp: CustomerLTVInput) -> float:
        score = 0.0
        # Executive relationship gaps
        if inp.executive_last_contact_days >= 90:
            score += 40.0
        elif inp.executive_last_contact_days >= 60:
            score += 24.0
        elif inp.executive_last_contact_days >= 30:
            score += 10.0
        # Executive meeting decline
        if inp.executive_meetings_prior_90d > 0:
            mtg_delta = (inp.executive_meetings_prior_90d - inp.executive_meetings_last_90d) / inp.executive_meetings_prior_90d
            if mtg_delta >= 0.7:
                score += 30.0
            elif mtg_delta >= 0.4:
                score += 18.0
            elif mtg_delta >= 0.2:
                score += 8.0
        # Competitor evaluation signal
        if inp.competitor_evaluation_signal == 1:
            score += 30.0
        return _clamp(score)

    # ── classification ───────────────────────────────────────────────────────

    def _classify_risk(self, composite: float) -> ErosionRisk:
        if composite < 20:
            return ErosionRisk.low
        if composite < 40:
            return ErosionRisk.moderate
        if composite < 60:
            return ErosionRisk.high
        return ErosionRisk.critical

    def _classify_severity(self, composite: float) -> ErosionSeverity:
        if composite < 20:
            return ErosionSeverity.healthy
        if composite < 40:
            return ErosionSeverity.watch
        if composite < 60:
            return ErosionSeverity.degrading
        return ErosionSeverity.critical

    def _classify_pattern(
        self,
        inp: CustomerLTVInput,
        usage: float,
        engagement: float,
        expansion: float,
        relationship: float,
    ) -> ErosionPattern:
        # Competitive migration: actively evaluating a competitor
        if inp.competitor_evaluation_signal == 1 and relationship >= 20:
            return ErosionPattern.competitive_migration
        # Exec relationship loss: executive gone dark
        if inp.executive_last_contact_days >= 60 and relationship >= 25:
            return ErosionPattern.exec_relationship_loss
        # Support overload: tickets surging, NPS crashing
        if inp.critical_tickets_last_30d >= 2 and engagement >= 25:
            return ErosionPattern.support_overload
        # Usage cliff: product usage cratering
        if inp.product_usage_score_prior_30d > 0:
            usage_delta = (inp.product_usage_score_prior_30d - inp.product_usage_score_last_30d) / inp.product_usage_score_prior_30d
            if usage_delta >= 0.25 and usage >= 20:
                return ErosionPattern.usage_cliff
        # Expansion stall: long-tenured customer with no expansion
        if inp.account_age_months >= 18 and inp.expansion_revenue_last_12m_usd == 0:
            return ErosionPattern.expansion_stall
        return ErosionPattern.none

    def _recommended_action(
        self, risk: ErosionRisk, composite: float
    ) -> ErosionAction:
        if composite >= 60:
            return ErosionAction.churn_prevention_team
        if composite >= 50:
            return ErosionAction.rescue_plan
        if risk == ErosionRisk.high:
            return ErosionAction.executive_qbr
        if risk == ErosionRisk.moderate:
            return ErosionAction.csm_outreach
        return ErosionAction.no_action

    def _signal(
        self,
        pattern: ErosionPattern,
        composite: float,
        inp: CustomerLTVInput,
    ) -> str:
        if pattern == ErosionPattern.none:
            return "Customer health within acceptable parameters"
        msgs = {
            ErosionPattern.competitive_migration: (
                f"Competitor evaluation active — exec dark {inp.executive_last_contact_days}d"
            ),
            ErosionPattern.exec_relationship_loss: (
                f"Exec dark {inp.executive_last_contact_days}d — "
                f"{inp.executive_meetings_last_90d} meetings vs {inp.executive_meetings_prior_90d} prior"
            ),
            ErosionPattern.support_overload: (
                f"{inp.critical_tickets_last_30d} critical tickets — NPS {inp.nps_score}"
            ),
            ErosionPattern.usage_cliff: (
                f"Usage {inp.product_usage_score_last_30d:.0f} vs {inp.product_usage_score_prior_30d:.0f} prior — "
                f"adoption {inp.feature_adoption_pct:.0f}%"
            ),
            ErosionPattern.expansion_stall: (
                f"{inp.account_age_months}mo customer — $0 expansion in 12m — "
                f"{inp.renewal_days_remaining}d to renewal"
            ),
        }
        base = msgs.get(pattern, f"erosion composite {composite:.0f}")
        return f"{base} — composite {composite:.0f}"

    # ── public API ───────────────────────────────────────────────────────────

    def assess(self, inp: CustomerLTVInput) -> CustomerLTVResult:
        usage        = self._usage_decline_score(inp)
        engagement   = self._engagement_decay_score(inp)
        expansion    = self._expansion_health_score(inp)
        relationship = self._relationship_risk_score(inp)

        composite = _clamp(
            usage        * 0.30
            + engagement * 0.30
            + expansion  * 0.25
            + relationship * 0.15
        )
        composite = round(composite, 1)

        risk     = self._classify_risk(composite)
        severity = self._classify_severity(composite)
        pattern  = self._classify_pattern(inp, usage, engagement, expansion, relationship)
        action   = self._recommended_action(risk, composite)

        is_at_churn_risk = (
            composite >= 40
            or inp.logo_at_risk_flag == 1
            or (inp.renewal_days_remaining <= 30 and composite >= 20)
        )
        requires_executive_attention = (
            composite >= 30
            or inp.competitor_evaluation_signal == 1
            or inp.executive_last_contact_days >= 60
        )

        estimated_arr_at_risk_usd = inp.contract_arr_usd * (composite / 100.0)

        result = CustomerLTVResult(
            customer_id=inp.customer_id,
            csm_id=inp.csm_id,
            erosion_risk=risk,
            erosion_pattern=pattern,
            erosion_severity=severity,
            recommended_action=action,
            usage_decline_score=usage,
            engagement_decay_score=engagement,
            expansion_health_score=expansion,
            relationship_risk_score=relationship,
            erosion_composite=composite,
            is_at_churn_risk=is_at_churn_risk,
            requires_executive_attention=requires_executive_attention,
            estimated_arr_at_risk_usd=estimated_arr_at_risk_usd,
            erosion_signal=self._signal(pattern, composite, inp),
        )
        self._results.append(result)
        return result

    def assess_batch(
        self, inputs: list[CustomerLTVInput]
    ) -> list[CustomerLTVResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total":                             0,
                "risk_counts":                       {},
                "pattern_counts":                    {},
                "severity_counts":                   {},
                "action_counts":                     {},
                "avg_erosion_composite":             0.0,
                "churn_risk_count":                  0,
                "executive_attention_count":         0,
                "avg_usage_decline_score":           0.0,
                "avg_engagement_decay_score":        0.0,
                "avg_expansion_health_score":        0.0,
                "avg_relationship_risk_score":       0.0,
                "total_estimated_arr_at_risk_usd":   0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_usg = total_eng = total_exp = total_rel = 0.0
        churn = exec_att = 0
        total_arr = 0.0

        for r in self._results:
            risk_counts[r.erosion_risk.value]       = risk_counts.get(r.erosion_risk.value, 0) + 1
            pattern_counts[r.erosion_pattern.value] = pattern_counts.get(r.erosion_pattern.value, 0) + 1
            severity_counts[r.erosion_severity.value] = severity_counts.get(r.erosion_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.erosion_composite
            total_usg  += r.usage_decline_score
            total_eng  += r.engagement_decay_score
            total_exp  += r.expansion_health_score
            total_rel  += r.relationship_risk_score
            total_arr  += r.estimated_arr_at_risk_usd
            if r.is_at_churn_risk:
                churn += 1
            if r.requires_executive_attention:
                exec_att += 1

        n = len(self._results)
        return {
            "total":                             n,
            "risk_counts":                       risk_counts,
            "pattern_counts":                    pattern_counts,
            "severity_counts":                   severity_counts,
            "action_counts":                     action_counts,
            "avg_erosion_composite":             round(total_comp / n, 1),
            "churn_risk_count":                  churn,
            "executive_attention_count":         exec_att,
            "avg_usage_decline_score":           round(total_usg  / n, 1),
            "avg_engagement_decay_score":        round(total_eng  / n, 1),
            "avg_expansion_health_score":        round(total_exp  / n, 1),
            "avg_relationship_risk_score":       round(total_rel  / n, 1),
            "total_estimated_arr_at_risk_usd":   round(total_arr, 2),
        }
