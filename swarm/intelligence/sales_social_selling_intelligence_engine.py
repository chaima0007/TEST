from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class SocialSellingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class SocialSellingPattern(str, Enum):
    none                    = "none"
    invisible_online        = "invisible_online"
    low_prospect_engagement = "low_prospect_engagement"
    inmail_abuse            = "inmail_abuse"
    competitor_following    = "competitor_following"
    content_inconsistency   = "content_inconsistency"


class SocialSellingSeverity(str, Enum):
    active      = "active"
    developing  = "developing"
    passive     = "passive"
    invisible   = "invisible"


class SocialSellingAction(str, Enum):
    no_action                   = "no_action"
    social_presence_coaching    = "social_presence_coaching"
    content_strategy_session    = "content_strategy_session"
    prospect_engagement_training = "prospect_engagement_training"
    inmail_optimization         = "inmail_optimization"
    brand_building_program      = "brand_building_program"


@dataclass
class SocialSellingInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    linkedin_ssi_score: float
    profile_views_last_30d: int
    connection_requests_sent: int
    connection_requests_accepted_count: int
    content_posts_last_30d: int
    content_engagement_rate_pct: float
    prospect_social_touches_count: int
    inmail_sent_count: int
    inmail_reply_rate_pct: float
    social_sourced_meetings_count: int
    social_sourced_pipeline_usd: float
    avg_days_to_connect_after_demo: float
    competitor_content_engagement_pct: float
    prospect_comment_response_rate_pct: float
    thought_leadership_shares_count: int
    group_participations_count: int
    network_overlap_with_icp_pct: float
    advocacy_referrals_from_social: int
    avg_opportunity_value_usd: float


@dataclass
class SocialSellingResult:
    rep_id: str
    region: str
    social_selling_risk: SocialSellingRisk
    social_selling_pattern: SocialSellingPattern
    social_selling_severity: SocialSellingSeverity
    recommended_action: SocialSellingAction
    profile_presence_score: float
    content_effectiveness_score: float
    prospect_engagement_score: float
    social_pipeline_score: float
    social_selling_composite: float
    has_social_gap: bool
    requires_social_coaching: bool
    estimated_pipeline_loss_usd: float
    social_selling_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "social_selling_risk":              self.social_selling_risk.value,
            "social_selling_pattern":           self.social_selling_pattern.value,
            "social_selling_severity":          self.social_selling_severity.value,
            "recommended_action":               self.recommended_action.value,
            "profile_presence_score":           self.profile_presence_score,
            "content_effectiveness_score":      self.content_effectiveness_score,
            "prospect_engagement_score":        self.prospect_engagement_score,
            "social_pipeline_score":            self.social_pipeline_score,
            "social_selling_composite":         self.social_selling_composite,
            "has_social_gap":                   self.has_social_gap,
            "requires_social_coaching":         self.requires_social_coaching,
            "estimated_pipeline_loss_usd":      self.estimated_pipeline_loss_usd,
            "social_selling_signal":            self.social_selling_signal,
        }


class SalesSocialSellingIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[SocialSellingResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _profile_presence_score(self, inp: SocialSellingInput) -> float:
        score = 0.0

        if inp.linkedin_ssi_score < 25.0:
            score += 40.0
        elif inp.linkedin_ssi_score < 45.0:
            score += 22.0
        elif inp.linkedin_ssi_score < 60.0:
            score += 8.0

        if inp.profile_views_last_30d < 10:
            score += 30.0
        elif inp.profile_views_last_30d < 25:
            score += 15.0

        if inp.network_overlap_with_icp_pct < 0.20:
            score += 30.0
        elif inp.network_overlap_with_icp_pct < 0.40:
            score += 15.0

        return min(score, 100.0)

    def _content_effectiveness_score(self, inp: SocialSellingInput) -> float:
        score = 0.0

        if inp.content_posts_last_30d < 2:
            score += 40.0
        elif inp.content_posts_last_30d < 4:
            score += 20.0
        elif inp.content_posts_last_30d < 8:
            score += 8.0

        if inp.content_engagement_rate_pct < 0.01:
            score += 35.0
        elif inp.content_engagement_rate_pct < 0.03:
            score += 18.0
        elif inp.content_engagement_rate_pct < 0.05:
            score += 7.0

        if inp.thought_leadership_shares_count < 1:
            score += 25.0
        elif inp.thought_leadership_shares_count < 3:
            score += 12.0

        return min(score, 100.0)

    def _prospect_engagement_score(self, inp: SocialSellingInput) -> float:
        score = 0.0

        if inp.prospect_social_touches_count < 5:
            score += 40.0
        elif inp.prospect_social_touches_count < 15:
            score += 20.0
        elif inp.prospect_social_touches_count < 30:
            score += 8.0

        total_inmails = max(inp.inmail_sent_count, 1)
        if inp.inmail_reply_rate_pct < 0.08:
            score += 30.0
        elif inp.inmail_reply_rate_pct < 0.15:
            score += 15.0

        if inp.prospect_comment_response_rate_pct < 0.30:
            score += 30.0
        elif inp.prospect_comment_response_rate_pct < 0.60:
            score += 15.0

        return min(score, 100.0)

    def _social_pipeline_score(self, inp: SocialSellingInput) -> float:
        score = 0.0

        if inp.social_sourced_meetings_count < 1:
            score += 45.0
        elif inp.social_sourced_meetings_count < 3:
            score += 25.0
        elif inp.social_sourced_meetings_count < 5:
            score += 10.0

        if inp.social_sourced_pipeline_usd < 10000.0:
            score += 30.0
        elif inp.social_sourced_pipeline_usd < 50000.0:
            score += 15.0

        if inp.advocacy_referrals_from_social < 1:
            score += 25.0
        elif inp.advocacy_referrals_from_social < 3:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: SocialSellingInput,
                          presence: float, content: float,
                          prospect: float, pipeline: float) -> SocialSellingPattern:
        if presence >= 40 and inp.linkedin_ssi_score < 30.0:
            return SocialSellingPattern.invisible_online

        if prospect >= 35 and inp.prospect_social_touches_count < 10:
            return SocialSellingPattern.low_prospect_engagement

        total_inmails = max(inp.inmail_sent_count, 1)
        if inp.inmail_sent_count >= 30 and inp.inmail_reply_rate_pct < 0.08:
            return SocialSellingPattern.inmail_abuse

        if inp.competitor_content_engagement_pct >= 0.30:
            return SocialSellingPattern.competitor_following

        if content >= 25 and inp.content_posts_last_30d < 3:
            return SocialSellingPattern.content_inconsistency

        return SocialSellingPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> SocialSellingRisk:
        if composite >= 60:
            return SocialSellingRisk.critical
        if composite >= 40:
            return SocialSellingRisk.high
        if composite >= 20:
            return SocialSellingRisk.moderate
        return SocialSellingRisk.low

    def _severity(self, composite: float) -> SocialSellingSeverity:
        if composite >= 60:
            return SocialSellingSeverity.invisible
        if composite >= 40:
            return SocialSellingSeverity.passive
        if composite >= 20:
            return SocialSellingSeverity.developing
        return SocialSellingSeverity.active

    def _action(self, risk: SocialSellingRisk,
                 pattern: SocialSellingPattern) -> SocialSellingAction:
        if risk == SocialSellingRisk.critical:
            if pattern == SocialSellingPattern.invisible_online:
                return SocialSellingAction.brand_building_program
            if pattern == SocialSellingPattern.low_prospect_engagement:
                return SocialSellingAction.prospect_engagement_training
            return SocialSellingAction.social_presence_coaching
        if risk == SocialSellingRisk.high:
            if pattern == SocialSellingPattern.inmail_abuse:
                return SocialSellingAction.inmail_optimization
            if pattern == SocialSellingPattern.content_inconsistency:
                return SocialSellingAction.content_strategy_session
            return SocialSellingAction.social_presence_coaching
        if risk == SocialSellingRisk.moderate:
            return SocialSellingAction.social_presence_coaching
        return SocialSellingAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_social_gap(self, composite: float,
                         inp: SocialSellingInput) -> bool:
        return (
            composite >= 40
            or inp.social_sourced_meetings_count < 1
            or inp.linkedin_ssi_score < 25.0
        )

    def _requires_social_coaching(self, composite: float,
                                   inp: SocialSellingInput) -> bool:
        return (
            composite >= 30
            or inp.content_posts_last_30d < 2
            or inp.prospect_social_touches_count < 5
        )

    # ------------------------------------------------------------------
    # Pipeline loss estimate
    # ------------------------------------------------------------------

    def _estimated_pipeline_loss(self, inp: SocialSellingInput,
                                  composite: float) -> float:
        benchmark_social_meetings_per_month = 3.0
        missed_meetings = max(0.0, benchmark_social_meetings_per_month - inp.social_sourced_meetings_count)
        return round(missed_meetings * inp.avg_opportunity_value_usd * (composite / 100.0) * 0.18, 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: SocialSellingInput,
                 pattern: SocialSellingPattern, composite: float) -> str:
        if pattern == SocialSellingPattern.none and composite < 20:
            return "Social selling performance healthy — prospect engagement, content reach, and pipeline generation within benchmarks"
        parts: list[str] = []
        parts.append(f"SSI {inp.linkedin_ssi_score:.0f}")
        parts.append(f"{inp.content_posts_last_30d} posts/mo")
        parts.append(f"{inp.social_sourced_meetings_count} social meetings")
        label = pattern.value.replace("_", " ") if pattern != SocialSellingPattern.none else "Social selling risk"
        summary = " — ".join(parts)
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: SocialSellingInput) -> SocialSellingResult:
        presence  = round(self._profile_presence_score(inp), 1)
        content   = round(self._content_effectiveness_score(inp), 1)
        prospect  = round(self._prospect_engagement_score(inp), 1)
        pipeline  = round(self._social_pipeline_score(inp), 1)

        composite = round(
            presence * 0.25 + content * 0.25 + prospect * 0.30 + pipeline * 0.20, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, presence, content, prospect, pipeline)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_social_gap(composite, inp)
        coach  = self._requires_social_coaching(composite, inp)
        impact = self._estimated_pipeline_loss(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = SocialSellingResult(
            rep_id=inp.rep_id,
            region=inp.region,
            social_selling_risk=risk,
            social_selling_pattern=pattern,
            social_selling_severity=severity,
            recommended_action=action,
            profile_presence_score=presence,
            content_effectiveness_score=content,
            prospect_engagement_score=prospect,
            social_pipeline_score=pipeline,
            social_selling_composite=composite,
            has_social_gap=gap,
            requires_social_coaching=coach,
            estimated_pipeline_loss_usd=impact,
            social_selling_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[SocialSellingInput]) -> list[SocialSellingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_social_selling_composite": 0.0,
                "social_gap_count": 0,
                "coaching_count": 0,
                "avg_profile_presence_score": 0.0,
                "avg_content_effectiveness_score": 0.0,
                "avg_prospect_engagement_score": 0.0,
                "avg_social_pipeline_score": 0.0,
                "total_estimated_pipeline_loss_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_pres = total_cont = total_pros = total_pipe = total_impact = 0.0

        for r in self._results:
            risk_counts[r.social_selling_risk.value]       = risk_counts.get(r.social_selling_risk.value, 0) + 1
            pattern_counts[r.social_selling_pattern.value] = pattern_counts.get(r.social_selling_pattern.value, 0) + 1
            severity_counts[r.social_selling_severity.value] = severity_counts.get(r.social_selling_severity.value, 0) + 1
            action_counts[r.recommended_action.value]      = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp   += r.social_selling_composite
            total_pres   += r.profile_presence_score
            total_cont   += r.content_effectiveness_score
            total_pros   += r.prospect_engagement_score
            total_pipe   += r.social_pipeline_score
            total_impact += r.estimated_pipeline_loss_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_social_selling_composite":             round(total_comp / n, 1),
            "social_gap_count":                         sum(1 for r in self._results if r.has_social_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_social_coaching),
            "avg_profile_presence_score":               round(total_pres / n, 1),
            "avg_content_effectiveness_score":          round(total_cont / n, 1),
            "avg_prospect_engagement_score":            round(total_pros / n, 1),
            "avg_social_pipeline_score":                round(total_pipe / n, 1),
            "total_estimated_pipeline_loss_usd":        round(total_impact, 2),
        }
