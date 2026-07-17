from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class IntentTier(str, Enum):
    COLD        = "cold"
    WARMING     = "warming"
    HOT         = "hot"
    BUYING_NOW  = "buying_now"


class FootprintPattern(str, Enum):
    PASSIVE_LURKER   = "passive_lurker"
    CONTENT_CONSUMER = "content_consumer"
    ACTIVE_RESEARCHER = "active_researcher"
    INTENT_SPIKER    = "intent_spiker"
    COMPETITIVE_EVALUATOR = "competitive_evaluator"
    READY_TO_BUY     = "ready_to_buy"


class EngagementVelocity(str, Enum):
    DECLINING  = "declining"
    FLAT       = "flat"
    GROWING    = "growing"
    SURGING    = "surging"


class ProspectAction(str, Enum):
    NURTURE      = "nurture"
    WARM_OUTREACH = "warm_outreach"
    IMMEDIATE_SDR = "immediate_sdr"
    EXECUTIVE_TOUCH = "executive_touch"


@dataclass
class ProspectDigitalInput:
    prospect_id:                    str
    company_name:                   str
    rep_id:                         str
    website_visits_last_30d:        int     # pages visited on your site last 30 days
    website_visits_prev_30d:        int     # pages visited 31-60 days ago (for velocity)
    pricing_page_views:             int     # pricing/plans page views (high-intent signal)
    case_study_downloads:           int     # content/case study downloads
    demo_page_views:                int     # demo request page views
    demo_requested:                 int     # 1 if demo was actually requested
    free_trial_started:             int     # 1 if free trial started
    email_opens_last_30d:           int     # marketing email opens
    email_clicks_last_30d:          int     # marketing email link clicks
    linkedin_profile_views_of_rep:  int     # prospect viewed rep's LinkedIn profile
    linkedin_company_page_visits:   int     # visits to your company's LinkedIn page
    competitor_review_site_signal:  int     # 1 if seen on G2/Capterra/Trustpilot comparing
    job_posting_signal_count:       int     # # relevant job postings (buying team signals)
    company_size_employees:         int     # company headcount
    funding_event_recent:           int     # 1 if company received funding in last 90 days
    technology_fit_score:           float   # 0-100, how well their tech stack fits our product
    days_since_first_touch:         int     # how many days since first digital engagement
    time_on_site_avg_minutes:       float   # average time per visit (engagement quality)
    return_visit_rate_pct:          float   # % of visits that are return visits (stickiness)


@dataclass
class ProspectDigitalResult:
    prospect_id:                str
    company_name:               str
    intent_tier:                IntentTier
    footprint_pattern:          FootprintPattern
    engagement_velocity:        EngagementVelocity
    prospect_action:            ProspectAction
    website_intent_score:       float   # 0-100
    content_engagement_score:   float   # 0-100
    social_signal_score:        float   # 0-100
    company_fit_score:          float   # 0-100
    digital_footprint_composite: float  # 0-100
    lead_score:                 float   # 0-100 (normalized scoring for CRM)
    days_to_outreach:           int     # recommended days before outreach
    is_high_intent:             bool
    needs_immediate_outreach:   bool

    def to_dict(self) -> dict:
        return {
            "prospect_id":                self.prospect_id,
            "company_name":               self.company_name,
            "intent_tier":                self.intent_tier.value,
            "footprint_pattern":          self.footprint_pattern.value,
            "engagement_velocity":        self.engagement_velocity.value,
            "prospect_action":            self.prospect_action.value,
            "website_intent_score":       self.website_intent_score,
            "content_engagement_score":   self.content_engagement_score,
            "social_signal_score":        self.social_signal_score,
            "company_fit_score":          self.company_fit_score,
            "digital_footprint_composite": self.digital_footprint_composite,
            "lead_score":                 self.lead_score,
            "days_to_outreach":           self.days_to_outreach,
            "is_high_intent":             self.is_high_intent,
            "needs_immediate_outreach":   self.needs_immediate_outreach,
        }


class ProspectDigitalFootprintScorer:
    def __init__(self) -> None:
        self._results: list[ProspectDigitalResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def score(self, inp: ProspectDigitalInput) -> ProspectDigitalResult:
        web_intent  = self._website_intent_score(inp)
        content_eng = self._content_engagement_score(inp)
        social      = self._social_signal_score(inp)
        fit         = self._company_fit_score(inp)
        composite   = self._composite(web_intent, content_eng, social, fit)
        velocity    = self._engagement_velocity(inp)
        tier        = self._intent_tier(composite, inp)
        pattern     = self._footprint_pattern(web_intent, content_eng, social, inp)
        lead_score  = self._lead_score(composite, velocity, inp)
        is_high     = composite >= 60.0 or inp.demo_requested == 1 or inp.free_trial_started == 1
        needs_now   = (composite >= 75.0 or inp.demo_requested == 1 or
                       (inp.pricing_page_views >= 3 and composite >= 55.0))
        days_out    = self._days_to_outreach(tier, needs_now)
        action      = self._prospect_action(tier, needs_now, inp)

        result = ProspectDigitalResult(
            prospect_id=inp.prospect_id,
            company_name=inp.company_name,
            intent_tier=tier,
            footprint_pattern=pattern,
            engagement_velocity=velocity,
            prospect_action=action,
            website_intent_score=web_intent,
            content_engagement_score=content_eng,
            social_signal_score=social,
            company_fit_score=fit,
            digital_footprint_composite=composite,
            lead_score=lead_score,
            days_to_outreach=days_out,
            is_high_intent=is_high,
            needs_immediate_outreach=needs_now,
        )
        self._results.append(result)
        return result

    def score_batch(self, inputs: list[ProspectDigitalInput]) -> list[ProspectDigitalResult]:
        return [self.score(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ──────────────────────────────────────────────────────────────

    @property
    def high_intent_prospects(self) -> list[ProspectDigitalResult]:
        return [r for r in self._results if r.is_high_intent]

    @property
    def immediate_outreach_queue(self) -> list[ProspectDigitalResult]:
        return [r for r in self._results if r.needs_immediate_outreach]

    @property
    def avg_lead_score(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.lead_score for r in self._results) / len(self._results), 1)

    @property
    def avg_digital_footprint_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.digital_footprint_composite for r in self._results) / len(self._results), 1)

    # ── scoring helpers ─────────────────────────────────────────────────────────

    def _website_intent_score(self, inp: ProspectDigitalInput) -> float:
        score = 0.0
        # Raw visit volume (up to 20)
        score += min(20.0, inp.website_visits_last_30d * 1.5)
        # Pricing page = highest intent (up to 30)
        score += min(30.0, inp.pricing_page_views * 10.0)
        # Demo page views (up to 20)
        score += min(20.0, inp.demo_page_views * 7.0)
        # Demo requested (up to 20)
        if inp.demo_requested:
            score += 20.0
        # Time on site quality signal (up to 10)
        score += min(10.0, inp.time_on_site_avg_minutes * 2.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _content_engagement_score(self, inp: ProspectDigitalInput) -> float:
        score = 0.0
        # Case study downloads = late-stage research (up to 30)
        score += min(30.0, inp.case_study_downloads * 10.0)
        # Email opens (up to 20)
        score += min(20.0, inp.email_opens_last_30d * 2.5)
        # Email clicks = higher intent than opens (up to 25)
        score += min(25.0, inp.email_clicks_last_30d * 5.0)
        # Return visit rate = stickiness (up to 15)
        score += min(15.0, inp.return_visit_rate_pct * 0.3)
        # Free trial started (up to 10)
        if inp.free_trial_started:
            score += 10.0
        return round(max(0.0, min(100.0, score)), 1)

    def _social_signal_score(self, inp: ProspectDigitalInput) -> float:
        score = 0.0
        # Rep LinkedIn profile viewed (up to 25)
        score += min(25.0, inp.linkedin_profile_views_of_rep * 12.0)
        # Company LinkedIn page visits (up to 20)
        score += min(20.0, inp.linkedin_company_page_visits * 5.0)
        # Competitor comparison site signal (up to 30)
        if inp.competitor_review_site_signal:
            score += 30.0
        # Relevant job postings (buying team signals) (up to 25)
        score += min(25.0, inp.job_posting_signal_count * 6.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _company_fit_score(self, inp: ProspectDigitalInput) -> float:
        score = inp.technology_fit_score * 0.60
        # Company size bonus (mid-market is typically ideal 100-2000 employees)
        size = inp.company_size_employees
        if 100 <= size <= 2000:
            score += 25.0
        elif 50 <= size < 100 or 2000 < size <= 5000:
            score += 15.0
        elif size > 5000:
            score += 10.0
        # Funding event = budget signal (up to 15)
        if inp.funding_event_recent:
            score += 15.0
        return round(max(0.0, min(100.0, score)), 1)

    def _composite(
        self,
        web: float,
        content: float,
        social: float,
        fit: float,
    ) -> float:
        composite = web * 0.35 + content * 0.30 + social * 0.20 + fit * 0.15
        return round(max(0.0, min(100.0, composite)), 1)

    def _engagement_velocity(self, inp: ProspectDigitalInput) -> EngagementVelocity:
        prev = inp.website_visits_prev_30d
        curr = inp.website_visits_last_30d
        if prev == 0:
            if curr >= 3:
                return EngagementVelocity.SURGING
            return EngagementVelocity.FLAT
        ratio = curr / prev
        if ratio >= 2.0:
            return EngagementVelocity.SURGING
        if ratio >= 1.2:
            return EngagementVelocity.GROWING
        if ratio <= 0.5:
            return EngagementVelocity.DECLINING
        return EngagementVelocity.FLAT

    def _intent_tier(self, composite: float, inp: ProspectDigitalInput) -> IntentTier:
        if composite >= 75 or inp.demo_requested or inp.free_trial_started:
            return IntentTier.BUYING_NOW
        if composite >= 55:
            return IntentTier.HOT
        if composite >= 30:
            return IntentTier.WARMING
        return IntentTier.COLD

    def _footprint_pattern(
        self,
        web: float,
        content: float,
        social: float,
        inp: ProspectDigitalInput,
    ) -> FootprintPattern:
        if inp.demo_requested or inp.free_trial_started:
            return FootprintPattern.READY_TO_BUY
        if inp.competitor_review_site_signal and social >= 50:
            return FootprintPattern.COMPETITIVE_EVALUATOR
        if inp.pricing_page_views >= 3 and web >= 60:
            return FootprintPattern.INTENT_SPIKER
        if content >= 50 and inp.case_study_downloads >= 2:
            return FootprintPattern.ACTIVE_RESEARCHER
        if content >= 25 or inp.email_clicks_last_30d >= 2:
            return FootprintPattern.CONTENT_CONSUMER
        return FootprintPattern.PASSIVE_LURKER

    def _lead_score(
        self,
        composite: float,
        velocity: EngagementVelocity,
        inp: ProspectDigitalInput,
    ) -> float:
        score = composite
        velocity_boost = {
            EngagementVelocity.SURGING: 15.0,
            EngagementVelocity.GROWING: 8.0,
            EngagementVelocity.FLAT:    0.0,
            EngagementVelocity.DECLINING: -10.0,
        }
        score = min(100.0, score + velocity_boost[velocity])
        # Recency bonus — engaged recently but short tenure is still valuable
        if inp.days_since_first_touch <= 14:
            score = min(100.0, score + 5.0)
        return round(max(0.0, min(100.0, score)), 1)

    def _days_to_outreach(self, tier: IntentTier, needs_now: bool) -> int:
        if needs_now or tier == IntentTier.BUYING_NOW:
            return 0
        if tier == IntentTier.HOT:
            return 2
        if tier == IntentTier.WARMING:
            return 7
        return 21

    def _prospect_action(
        self,
        tier: IntentTier,
        needs_now: bool,
        inp: ProspectDigitalInput,
    ) -> ProspectAction:
        if needs_now or tier == IntentTier.BUYING_NOW:
            company_size = inp.company_size_employees
            if company_size >= 1000 or (inp.funding_event_recent and company_size >= 200):
                return ProspectAction.EXECUTIVE_TOUCH
            return ProspectAction.IMMEDIATE_SDR
        if tier == IntentTier.HOT:
            return ProspectAction.WARM_OUTREACH
        return ProspectAction.NURTURE

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                        0,
                "tier_counts":                  {},
                "pattern_counts":               {},
                "velocity_counts":              {},
                "action_counts":                {},
                "avg_digital_footprint_composite": 0.0,
                "avg_lead_score":               0.0,
                "high_intent_count":            0,
                "immediate_outreach_count":     0,
                "avg_website_intent_score":     0.0,
                "avg_content_engagement_score": 0.0,
                "avg_social_signal_score":      0.0,
                "avg_company_fit_score":        0.0,
            }

        tier_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        velocity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp  = 0.0
        total_lead  = 0.0
        total_web   = 0.0
        total_cont  = 0.0
        total_soc   = 0.0
        total_fit   = 0.0

        for r in self._results:
            tier_counts[r.intent_tier.value]       = tier_counts.get(r.intent_tier.value, 0) + 1
            pattern_counts[r.footprint_pattern.value] = pattern_counts.get(r.footprint_pattern.value, 0) + 1
            velocity_counts[r.engagement_velocity.value] = velocity_counts.get(r.engagement_velocity.value, 0) + 1
            action_counts[r.prospect_action.value] = action_counts.get(r.prospect_action.value, 0) + 1
            total_comp += r.digital_footprint_composite
            total_lead += r.lead_score
            total_web  += r.website_intent_score
            total_cont += r.content_engagement_score
            total_soc  += r.social_signal_score
            total_fit  += r.company_fit_score

        return {
            "total":                        n,
            "tier_counts":                  tier_counts,
            "pattern_counts":               pattern_counts,
            "velocity_counts":              velocity_counts,
            "action_counts":                action_counts,
            "avg_digital_footprint_composite": round(total_comp / n, 1),
            "avg_lead_score":               round(total_lead / n, 1),
            "high_intent_count":            len(self.high_intent_prospects),
            "immediate_outreach_count":     len(self.immediate_outreach_queue),
            "avg_website_intent_score":     round(total_web / n, 1),
            "avg_content_engagement_score": round(total_cont / n, 1),
            "avg_social_signal_score":      round(total_soc / n, 1),
            "avg_company_fit_score":        round(total_fit / n, 1),
        }
