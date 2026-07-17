from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PartnerTier(str, Enum):
    PLATINUM = "platinum"
    GOLD     = "gold"
    SILVER   = "silver"
    BRONZE   = "bronze"
    PROSPECT = "prospect"


class PartnerType(str, Enum):
    RESELLER     = "reseller"
    REFERRAL     = "referral"
    CO_SELL      = "co_sell"
    TECHNOLOGY   = "technology"
    SI           = "si"              # system integrator
    DISTRIBUTOR  = "distributor"


class ChannelHealth(str, Enum):
    EXCELLENT    = "excellent"
    HEALTHY      = "healthy"
    NEEDS_ATTENTION = "needs_attention"
    AT_RISK      = "at_risk"
    INACTIVE     = "inactive"


class PartnerAction(str, Enum):
    INVEST_AND_GROW   = "invest_and_grow"
    ENABLE_AND_TRAIN  = "enable_and_train"
    JOINT_CAMPAIGN    = "joint_campaign"
    REVIEW_AND_RESET  = "review_and_reset"
    REACTIVATE        = "reactivate"
    OFFBOARD          = "offboard"


@dataclass
class PartnerChannelInput:
    partner_id:               str
    partner_name:             str
    partner_type:             PartnerType
    current_tier:             PartnerTier
    region:                   str
    years_as_partner:         float
    # Pipeline metrics
    deals_registered:         int
    deals_closed_won:         int
    deals_closed_lost:        int
    pipeline_value:           float
    closed_won_value:         float
    avg_deal_size:             float
    # Engagement metrics
    certified_reps:           int
    total_partner_reps:       int
    training_completion_pct:  float      # 0–100
    last_deal_days:           int        # days since last deal registered
    last_activity_days:       int        # days since last activity (call, email, portal)
    joint_campaigns:          int
    # Channel conflict
    conflict_incidents:       int
    conflict_resolved:        int
    # Revenue performance
    quarterly_revenue_target: float
    quarterly_revenue_actual: float
    nps_score:                float       # -100 to 100
    # Program compliance
    is_portal_active:         bool
    has_completed_onboarding: bool
    contract_valid:           bool


@dataclass
class PartnerChannelResult:
    partner_id:               str
    partner_name:             str
    partner_type:             PartnerType
    current_tier:             PartnerTier
    recommended_tier:         PartnerTier
    channel_health:           ChannelHealth
    partner_action:           PartnerAction
    engagement_score:         float        # 0–100
    performance_score:        float        # 0–100
    pipeline_contribution:    float        # pipeline_value as % of target
    win_rate:                 float        # closed_won / (won + lost)
    certification_rate:       float        # certified / total reps
    conflict_resolution_rate: float        # resolved / total
    quota_attainment:         float        # actual / target × 100
    is_strategic:             bool
    needs_intervention:       bool

    def to_dict(self) -> dict:
        return {
            "partner_id":               self.partner_id,
            "partner_name":             self.partner_name,
            "partner_type":             self.partner_type.value,
            "current_tier":             self.current_tier.value,
            "recommended_tier":         self.recommended_tier.value,
            "channel_health":           self.channel_health.value,
            "partner_action":           self.partner_action.value,
            "engagement_score":         self.engagement_score,
            "performance_score":        self.performance_score,
            "pipeline_contribution":    self.pipeline_contribution,
            "win_rate":                 self.win_rate,
            "certification_rate":       self.certification_rate,
            "quota_attainment":         self.quota_attainment,
            "is_strategic":             self.is_strategic,
            "needs_intervention":       self.needs_intervention,
        }


class PartnerChannelEngine:
    def __init__(self) -> None:
        self._results: list[PartnerChannelResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def analyze(self, inp: PartnerChannelInput) -> PartnerChannelResult:
        eng_score   = self._engagement_score(inp)
        perf_score  = self._performance_score(inp)
        pipe_contrib = self._pipeline_contribution(inp)
        win_rate    = self._win_rate(inp)
        cert_rate   = self._certification_rate(inp)
        conflict_res = self._conflict_resolution_rate(inp)
        quota_att   = self._quota_attainment(inp)
        health      = self._channel_health(inp, eng_score, perf_score, quota_att)
        rec_tier    = self._recommended_tier(inp, perf_score, eng_score, quota_att)
        action      = self._partner_action(inp, health, eng_score, perf_score)
        strategic   = self._is_strategic(inp, perf_score, eng_score)
        intervention = health in (ChannelHealth.AT_RISK, ChannelHealth.INACTIVE)

        result = PartnerChannelResult(
            partner_id=inp.partner_id,
            partner_name=inp.partner_name,
            partner_type=inp.partner_type,
            current_tier=inp.current_tier,
            recommended_tier=rec_tier,
            channel_health=health,
            partner_action=action,
            engagement_score=eng_score,
            performance_score=perf_score,
            pipeline_contribution=pipe_contrib,
            win_rate=win_rate,
            certification_rate=cert_rate,
            conflict_resolution_rate=conflict_res,
            quota_attainment=quota_att,
            is_strategic=strategic,
            needs_intervention=intervention,
        )
        self._results.append(result)
        return result

    def analyze_batch(
        self, inputs: list[PartnerChannelInput]
    ) -> list[PartnerChannelResult]:
        return [self.analyze(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def strategic_partners(self) -> list[PartnerChannelResult]:
        return [r for r in self._results if r.is_strategic]

    @property
    def at_risk_partners(self) -> list[PartnerChannelResult]:
        return [r for r in self._results
                if r.channel_health in (ChannelHealth.AT_RISK, ChannelHealth.INACTIVE)]

    @property
    def top_performers(self) -> list[PartnerChannelResult]:
        return [r for r in self._results
                if r.channel_health in (ChannelHealth.EXCELLENT, ChannelHealth.HEALTHY)]

    @property
    def total_partner_pipeline(self) -> float:
        return round(sum(r.pipeline_contribution * 0 for r in self._results), 2)

    # ── scoring helpers ────────────────────────────────────────────────────────

    def _engagement_score(self, inp: PartnerChannelInput) -> float:
        score = 0.0
        # Certification rate
        cert = self._certification_rate(inp)
        score += cert * 25.0
        # Training
        score += min(20.0, inp.training_completion_pct * 0.2)
        # Recency of last deal
        if inp.last_deal_days <= 30:   score += 20
        elif inp.last_deal_days <= 60: score += 12
        elif inp.last_deal_days <= 90: score += 5
        # Activity recency
        if inp.last_activity_days <= 7:  score += 15
        elif inp.last_activity_days <= 30: score += 8
        elif inp.last_activity_days <= 60: score += 3
        # Joint campaigns
        score += min(10.0, inp.joint_campaigns * 2.0)
        # Compliance
        if inp.is_portal_active:         score += 5
        if inp.has_completed_onboarding: score += 5
        return round(max(0.0, min(100.0, score)), 1)

    def _performance_score(self, inp: PartnerChannelInput) -> float:
        score = 0.0
        # Win rate contribution
        wr = self._win_rate(inp)
        score += wr * 30.0
        # Quota attainment
        qa = self._quota_attainment(inp)
        score += min(35.0, qa * 0.35)
        # Deal volume (normalized by tier expectation)
        tier_deal_target = {"platinum": 20, "gold": 12, "silver": 6, "bronze": 3, "prospect": 1}.get(
            inp.current_tier.value, 5
        )
        deal_ratio = min(2.0, inp.deals_registered / max(1, tier_deal_target))
        score += deal_ratio * 15.0
        # NPS
        nps_norm = (inp.nps_score + 100) / 200  # 0–1
        score += nps_norm * 10.0
        # Conflict management
        if inp.conflict_incidents == 0:
            score += 10
        else:
            res_rate = self._conflict_resolution_rate(inp)
            score += res_rate * 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _pipeline_contribution(self, inp: PartnerChannelInput) -> float:
        if inp.quarterly_revenue_target <= 0:
            return 0.0
        return round((inp.pipeline_value / inp.quarterly_revenue_target) * 100, 1)

    def _win_rate(self, inp: PartnerChannelInput) -> float:
        total = inp.deals_closed_won + inp.deals_closed_lost
        if total == 0:
            return 0.0
        return round(inp.deals_closed_won / total, 3)

    def _certification_rate(self, inp: PartnerChannelInput) -> float:
        if inp.total_partner_reps == 0:
            return 0.0
        return round(inp.certified_reps / inp.total_partner_reps, 3)

    def _conflict_resolution_rate(self, inp: PartnerChannelInput) -> float:
        if inp.conflict_incidents == 0:
            return 1.0
        return round(min(1.0, inp.conflict_resolved / inp.conflict_incidents), 3)

    def _quota_attainment(self, inp: PartnerChannelInput) -> float:
        if inp.quarterly_revenue_target <= 0:
            return 100.0
        return round((inp.quarterly_revenue_actual / inp.quarterly_revenue_target) * 100, 1)

    def _channel_health(
        self,
        inp: PartnerChannelInput,
        eng: float,
        perf: float,
        quota_att: float,
    ) -> ChannelHealth:
        if not inp.contract_valid or inp.last_activity_days > 180:
            return ChannelHealth.INACTIVE
        combined = eng * 0.4 + perf * 0.6
        if inp.last_deal_days > 120 or (not inp.is_portal_active and inp.last_activity_days > 90):
            return ChannelHealth.AT_RISK
        if combined >= 75 and quota_att >= 90:  return ChannelHealth.EXCELLENT
        if combined >= 55 and quota_att >= 70:  return ChannelHealth.HEALTHY
        if combined >= 35:                       return ChannelHealth.NEEDS_ATTENTION
        return ChannelHealth.AT_RISK

    def _recommended_tier(
        self,
        inp: PartnerChannelInput,
        perf: float,
        eng: float,
        quota_att: float,
    ) -> PartnerTier:
        combined = perf * 0.6 + eng * 0.4
        if combined >= 80 and quota_att >= 110 and inp.years_as_partner >= 2:
            return PartnerTier.PLATINUM
        if combined >= 65 and quota_att >= 90:
            return PartnerTier.GOLD
        if combined >= 45 and quota_att >= 70:
            return PartnerTier.SILVER
        if combined >= 25:
            return PartnerTier.BRONZE
        return PartnerTier.PROSPECT

    def _partner_action(
        self,
        inp: PartnerChannelInput,
        health: ChannelHealth,
        eng: float,
        perf: float,
    ) -> PartnerAction:
        if health == ChannelHealth.INACTIVE:
            return PartnerAction.OFFBOARD
        if health == ChannelHealth.AT_RISK:
            if inp.last_activity_days > 90:
                return PartnerAction.REACTIVATE
            return PartnerAction.REVIEW_AND_RESET
        if health == ChannelHealth.EXCELLENT and perf >= 75:
            return PartnerAction.INVEST_AND_GROW
        if eng < 50 and inp.certification_rate if hasattr(inp, "certification_rate") else self._certification_rate(inp) < 0.5:
            return PartnerAction.ENABLE_AND_TRAIN
        if health in (ChannelHealth.HEALTHY, ChannelHealth.NEEDS_ATTENTION) and inp.joint_campaigns == 0:
            return PartnerAction.JOINT_CAMPAIGN
        if perf < 50:
            return PartnerAction.ENABLE_AND_TRAIN
        return PartnerAction.INVEST_AND_GROW

    def _is_strategic(
        self,
        inp: PartnerChannelInput,
        perf: float,
        eng: float,
    ) -> bool:
        return (
            inp.closed_won_value >= 100_000
            and perf >= 60
            and eng >= 50
            and inp.current_tier in (PartnerTier.PLATINUM, PartnerTier.GOLD)
        )

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                      0,
                "tier_counts":                {},
                "type_counts":                {},
                "health_counts":              {},
                "action_counts":              {},
                "avg_engagement_score":       0.0,
                "avg_performance_score":      0.0,
                "avg_win_rate":               0.0,
                "avg_quota_attainment":       0.0,
                "strategic_count":            0,
                "at_risk_count":              0,
                "top_performer_count":        0,
                "needs_intervention_count":   0,
            }

        tier_counts:   dict[str, int] = {}
        type_counts:   dict[str, int] = {}
        health_counts: dict[str, int] = {}
        action_counts: dict[str, int] = {}
        total_eng  = 0.0
        total_perf = 0.0
        total_wr   = 0.0
        total_qa   = 0.0

        for r in self._results:
            tier_counts[r.current_tier.value]  = tier_counts.get(r.current_tier.value, 0) + 1
            type_counts[r.partner_type.value]  = type_counts.get(r.partner_type.value, 0) + 1
            health_counts[r.channel_health.value] = health_counts.get(r.channel_health.value, 0) + 1
            action_counts[r.partner_action.value] = action_counts.get(r.partner_action.value, 0) + 1
            total_eng  += r.engagement_score
            total_perf += r.performance_score
            total_wr   += r.win_rate
            total_qa   += r.quota_attainment

        return {
            "total":                      n,
            "tier_counts":                tier_counts,
            "type_counts":                type_counts,
            "health_counts":              health_counts,
            "action_counts":              action_counts,
            "avg_engagement_score":       round(total_eng / n, 1),
            "avg_performance_score":      round(total_perf / n, 1),
            "avg_win_rate":               round(total_wr / n, 3),
            "avg_quota_attainment":       round(total_qa / n, 1),
            "strategic_count":            len(self.strategic_partners),
            "at_risk_count":              len(self.at_risk_partners),
            "top_performer_count":        len(self.top_performers),
            "needs_intervention_count":   sum(1 for r in self._results if r.needs_intervention),
        }
