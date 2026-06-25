from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class IntentRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class IntentPattern(str, Enum):
    none                   = "none"
    intent_cooling          = "intent_cooling"
    ghost_prospect          = "ghost_prospect"
    competitor_evaluation   = "competitor_evaluation"
    timing_mismatch         = "timing_mismatch"
    champion_disengagement  = "champion_disengagement"


class IntentSeverity(str, Enum):
    engaged    = "engaged"
    lukewarm   = "lukewarm"
    cooling    = "cooling"
    ghosted    = "ghosted"


class IntentAction(str, Enum):
    no_action                    = "no_action"
    re_engagement_sequence       = "re_engagement_sequence"
    champion_outreach            = "champion_outreach"
    competitive_displacement     = "competitive_displacement"
    timing_nurture_sequence      = "timing_nurture_sequence"
    deal_rescue_escalation       = "deal_rescue_escalation"


@dataclass
class BuyerIntentSignalInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_prospects_tracked: int
    email_opens_last_7d_count: int
    email_opens_prior_7d_count: int
    website_visits_last_7d_count: int
    website_visits_prior_7d_count: int
    content_downloads_last_7d_count: int
    demo_requests_count: int
    pricing_page_visits_count: int
    avg_days_since_last_prospect_response: float
    prospects_no_response_14d_count: int
    prospects_no_response_30d_count: int
    champion_response_rate_pct: float
    champion_last_contact_days: float
    competitor_mentions_count: int
    multi_stakeholder_engagement_pct: float
    buying_committee_size_avg: float
    budget_confirmed_count: int
    timeline_confirmed_count: int
    avg_opportunity_value_usd: float


@dataclass
class BuyerIntentSignalResult:
    rep_id: str
    region: str
    intent_risk: IntentRisk
    intent_pattern: IntentPattern
    intent_severity: IntentSeverity
    recommended_action: IntentAction
    engagement_decay_score: float
    champion_health_score: float
    buying_signal_score: float
    competitive_threat_score: float
    buyer_intent_composite: float
    has_intent_gap: bool
    requires_re_engagement: bool
    estimated_pipeline_at_risk_usd: float
    intent_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                         self.rep_id,
            "region":                         self.region,
            "intent_risk":                    self.intent_risk.value,
            "intent_pattern":                 self.intent_pattern.value,
            "intent_severity":                self.intent_severity.value,
            "recommended_action":             self.recommended_action.value,
            "engagement_decay_score":         self.engagement_decay_score,
            "champion_health_score":          self.champion_health_score,
            "buying_signal_score":            self.buying_signal_score,
            "competitive_threat_score":       self.competitive_threat_score,
            "buyer_intent_composite":         self.buyer_intent_composite,
            "has_intent_gap":                 self.has_intent_gap,
            "requires_re_engagement":         self.requires_re_engagement,
            "estimated_pipeline_at_risk_usd": self.estimated_pipeline_at_risk_usd,
            "intent_signal":                  self.intent_signal,
        }


class SalesBuyerIntentSignalIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[BuyerIntentSignalResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _engagement_decay_score(self, inp: BuyerIntentSignalInput) -> float:
        score = 0.0

        prior_opens = max(inp.email_opens_prior_7d_count, 1)
        open_decay = (prior_opens - inp.email_opens_last_7d_count) / prior_opens
        if open_decay >= 0.60:
            score += 35.0
        elif open_decay >= 0.30:
            score += 18.0
        elif open_decay >= 0.10:
            score += 7.0

        prior_visits = max(inp.website_visits_prior_7d_count, 1)
        visit_decay = (prior_visits - inp.website_visits_last_7d_count) / prior_visits
        if visit_decay >= 0.60:
            score += 30.0
        elif visit_decay >= 0.30:
            score += 15.0

        total = max(inp.total_prospects_tracked, 1)
        no_resp_rate = inp.prospects_no_response_30d_count / total
        if no_resp_rate >= 0.40:
            score += 25.0
        elif no_resp_rate >= 0.20:
            score += 12.0

        return min(score, 100.0)

    def _champion_health_score(self, inp: BuyerIntentSignalInput) -> float:
        score = 0.0

        if inp.champion_last_contact_days >= 21.0:
            score += 40.0
        elif inp.champion_last_contact_days >= 14.0:
            score += 22.0
        elif inp.champion_last_contact_days >= 7.0:
            score += 8.0

        if inp.champion_response_rate_pct < 0.20:
            score += 35.0
        elif inp.champion_response_rate_pct < 0.40:
            score += 18.0
        elif inp.champion_response_rate_pct < 0.60:
            score += 7.0

        if inp.multi_stakeholder_engagement_pct < 0.20:
            score += 20.0
        elif inp.multi_stakeholder_engagement_pct < 0.40:
            score += 10.0

        return min(score, 100.0)

    def _buying_signal_score(self, inp: BuyerIntentSignalInput) -> float:
        score = 0.0

        total = max(inp.total_prospects_tracked, 1)
        demo_rate = inp.demo_requests_count / total
        if demo_rate < 0.05:
            score += 30.0
        elif demo_rate < 0.10:
            score += 15.0

        pricing_rate = inp.pricing_page_visits_count / total
        if pricing_rate < 0.05:
            score += 25.0
        elif pricing_rate < 0.10:
            score += 12.0

        budget_rate = inp.budget_confirmed_count / total
        timeline_rate = inp.timeline_confirmed_count / total
        if budget_rate < 0.10 and timeline_rate < 0.10:
            score += 30.0
        elif budget_rate < 0.20 or timeline_rate < 0.20:
            score += 15.0

        return min(score, 100.0)

    def _competitive_threat_score(self, inp: BuyerIntentSignalInput) -> float:
        score = 0.0

        total = max(inp.total_prospects_tracked, 1)
        competitor_rate = inp.competitor_mentions_count / total
        if competitor_rate >= 0.30:
            score += 45.0
        elif competitor_rate >= 0.15:
            score += 25.0
        elif competitor_rate >= 0.05:
            score += 10.0

        if inp.avg_days_since_last_prospect_response >= 14.0:
            score += 35.0
        elif inp.avg_days_since_last_prospect_response >= 7.0:
            score += 18.0
        elif inp.avg_days_since_last_prospect_response >= 4.0:
            score += 7.0

        no_resp_14_rate = inp.prospects_no_response_14d_count / total
        if no_resp_14_rate >= 0.30:
            score += 20.0
        elif no_resp_14_rate >= 0.15:
            score += 10.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: BuyerIntentSignalInput,
                         decay: float, champion: float,
                         signal: float, competitive: float) -> IntentPattern:
        if champion >= 40 and inp.champion_last_contact_days >= 14.0:
            return IntentPattern.champion_disengagement

        total = max(inp.total_prospects_tracked, 1)
        no_resp_rate = inp.prospects_no_response_30d_count / total
        if decay >= 40 and no_resp_rate >= 0.30:
            return IntentPattern.ghost_prospect

        competitor_rate = inp.competitor_mentions_count / total
        if competitive >= 30 and competitor_rate >= 0.15:
            return IntentPattern.competitor_evaluation

        if signal >= 30 and inp.budget_confirmed_count == 0 and inp.timeline_confirmed_count == 0:
            return IntentPattern.timing_mismatch

        if decay >= 25:
            return IntentPattern.intent_cooling

        return IntentPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> IntentRisk:
        if composite >= 60:
            return IntentRisk.critical
        if composite >= 40:
            return IntentRisk.high
        if composite >= 20:
            return IntentRisk.moderate
        return IntentRisk.low

    def _severity(self, composite: float) -> IntentSeverity:
        if composite >= 60:
            return IntentSeverity.ghosted
        if composite >= 40:
            return IntentSeverity.cooling
        if composite >= 20:
            return IntentSeverity.lukewarm
        return IntentSeverity.engaged

    def _action(self, risk: IntentRisk, pattern: IntentPattern) -> IntentAction:
        if risk == IntentRisk.critical:
            if pattern == IntentPattern.champion_disengagement:
                return IntentAction.champion_outreach
            if pattern == IntentPattern.ghost_prospect:
                return IntentAction.deal_rescue_escalation
            return IntentAction.deal_rescue_escalation
        if risk == IntentRisk.high:
            if pattern == IntentPattern.competitor_evaluation:
                return IntentAction.competitive_displacement
            if pattern == IntentPattern.timing_mismatch:
                return IntentAction.timing_nurture_sequence
            return IntentAction.re_engagement_sequence
        if risk == IntentRisk.moderate:
            return IntentAction.re_engagement_sequence
        return IntentAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_intent_gap(self, composite: float,
                         inp: BuyerIntentSignalInput) -> bool:
        total = max(inp.total_prospects_tracked, 1)
        return (
            composite >= 40
            or inp.prospects_no_response_30d_count / total >= 0.30
            or inp.champion_last_contact_days >= 21.0
        )

    def _requires_re_engagement(self, composite: float,
                                  inp: BuyerIntentSignalInput) -> bool:
        total = max(inp.total_prospects_tracked, 1)
        return (
            composite >= 30
            or inp.avg_days_since_last_prospect_response >= 10.0
            or inp.prospects_no_response_14d_count / total >= 0.25
        )

    # ------------------------------------------------------------------
    # Pipeline impact
    # ------------------------------------------------------------------

    def _estimated_pipeline_at_risk(self, inp: BuyerIntentSignalInput,
                                     composite: float) -> float:
        return round(
            inp.prospects_no_response_30d_count * inp.avg_opportunity_value_usd * (composite / 100.0), 2
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: BuyerIntentSignalInput,
                 pattern: IntentPattern, composite: float) -> str:
        if pattern == IntentPattern.none and composite < 20:
            return "Buyer intent signals healthy — prospects showing active engagement"
        parts: list[str] = []
        total = max(inp.total_prospects_tracked, 1)
        no_resp_rate = inp.prospects_no_response_30d_count / total
        if no_resp_rate >= 0.20:
            parts.append(f"{no_resp_rate*100:.0f}% prospects silent 30d")
        if inp.champion_last_contact_days >= 7.0:
            parts.append(f"{inp.champion_last_contact_days:.0f}d since champion contact")
        if inp.competitor_mentions_count > 0:
            parts.append(f"{inp.competitor_mentions_count} competitor mentions")
        label = pattern.value.replace("_", " ") if pattern != IntentPattern.none else "Intent risk"
        summary = " — ".join(parts) if parts else "engagement declining"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: BuyerIntentSignalInput) -> BuyerIntentSignalResult:
        decay       = round(self._engagement_decay_score(inp), 1)
        champion    = round(self._champion_health_score(inp), 1)
        signal      = round(self._buying_signal_score(inp), 1)
        competitive = round(self._competitive_threat_score(inp), 1)

        composite = round(
            decay * 0.30 + champion * 0.30 + signal * 0.25 + competitive * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, decay, champion, signal, competitive)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap          = self._has_intent_gap(composite, inp)
        re_engage    = self._requires_re_engagement(composite, inp)
        at_risk      = self._estimated_pipeline_at_risk(inp, composite)
        sig_str      = self._signal(inp, pattern, composite)

        result = BuyerIntentSignalResult(
            rep_id=inp.rep_id,
            region=inp.region,
            intent_risk=risk,
            intent_pattern=pattern,
            intent_severity=severity,
            recommended_action=action,
            engagement_decay_score=decay,
            champion_health_score=champion,
            buying_signal_score=signal,
            competitive_threat_score=competitive,
            buyer_intent_composite=composite,
            has_intent_gap=gap,
            requires_re_engagement=re_engage,
            estimated_pipeline_at_risk_usd=at_risk,
            intent_signal=sig_str,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[BuyerIntentSignalInput]) -> list[BuyerIntentSignalResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_buyer_intent_composite": 0.0,
                "intent_gap_count": 0,
                "re_engagement_count": 0,
                "avg_engagement_decay_score": 0.0,
                "avg_champion_health_score": 0.0,
                "avg_buying_signal_score": 0.0,
                "avg_competitive_threat_score": 0.0,
                "total_estimated_pipeline_at_risk_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_decay = total_champ = total_sig = total_comp_threat = total_risk = 0.0

        for r in self._results:
            risk_counts[r.intent_risk.value]         = risk_counts.get(r.intent_risk.value, 0) + 1
            pattern_counts[r.intent_pattern.value]   = pattern_counts.get(r.intent_pattern.value, 0) + 1
            severity_counts[r.intent_severity.value] = severity_counts.get(r.intent_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp       += r.buyer_intent_composite
            total_decay      += r.engagement_decay_score
            total_champ      += r.champion_health_score
            total_sig        += r.buying_signal_score
            total_comp_threat += r.competitive_threat_score
            total_risk       += r.estimated_pipeline_at_risk_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_buyer_intent_composite":               round(total_comp / n, 1),
            "intent_gap_count":                         sum(1 for r in self._results if r.has_intent_gap),
            "re_engagement_count":                      sum(1 for r in self._results if r.requires_re_engagement),
            "avg_engagement_decay_score":               round(total_decay / n, 1),
            "avg_champion_health_score":                round(total_champ / n, 1),
            "avg_buying_signal_score":                  round(total_sig / n, 1),
            "avg_competitive_threat_score":             round(total_comp_threat / n, 1),
            "total_estimated_pipeline_at_risk_usd":     round(total_risk, 2),
        }
