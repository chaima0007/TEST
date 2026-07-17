"""
Module 213 — Sales Buyer Intent Signal Decay Engine
Detects accounts where buyer intent signals are decaying, indicating
deals going cold before they formally stall in CRM.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class IntentRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class IntentPattern(str, Enum):
    none                    = "none"
    digital_ghost           = "digital_ghost"
    content_disengagement   = "content_disengagement"
    demo_dropout            = "demo_dropout"
    champion_signal_fade    = "champion_signal_fade"
    evaluation_abandonment  = "evaluation_abandonment"


class IntentSeverity(str, Enum):
    engaged    = "engaged"
    warming    = "warming"
    cooling    = "cooling"
    cold       = "cold"


class IntentAction(str, Enum):
    no_action                    = "no_action"
    intent_monitoring            = "intent_monitoring"
    re_engagement_outreach       = "re_engagement_outreach"
    content_nurture_activation   = "content_nurture_activation"
    demo_reactivation_campaign   = "demo_reactivation_campaign"
    champion_reactivation_call   = "champion_reactivation_call"
    deal_rescue_intervention     = "deal_rescue_intervention"
    pipeline_purge_recommendation = "pipeline_purge_recommendation"
    executive_reconnect_protocol = "executive_reconnect_protocol"


@dataclass
class IntentInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    # Digital engagement decay
    website_visit_decay_rate_pct: float       # % drop in account website visits
    email_open_rate_decay_pct: float          # % drop in email open rates
    content_download_decay_rate_pct: float    # % drop in content engagement
    avg_days_since_last_digital_touch: float  # days since any digital engagement
    # Demo / evaluation signals
    demo_no_show_rate_pct: float              # % of scheduled demos no-showed
    demo_follow_up_response_rate_pct: float   # % follow-ups after demo that get reply
    evaluation_activity_score: float          # 0-1 live evaluation activity
    trial_feature_adoption_rate_pct: float    # % of trial features actually used
    # Champion engagement signals
    champion_response_latency_days: float     # avg days for champion to reply
    champion_meeting_acceptance_rate_pct: float  # % meeting invites accepted
    champion_internal_forward_rate_pct: float    # % emails forwarded internally
    # Account-level intent
    intent_score_trend: float                 # -1 to 1 (negative = decaying)
    buying_committee_engagement_score: float  # 0-1 overall buying committee activity
    multi_contact_engagement_rate_pct: float  # % of contacts active in account
    # Signal freshness
    days_since_last_positive_signal: float    # days since any positive intent signal
    intent_data_coverage_score: float         # 0-1 quality of intent data available
    # Volume / context
    deals_with_intent_decay: int              # count of deals showing decay
    avg_deal_value_usd: float


@dataclass
class IntentResult:
    rep_id: str
    region: str
    intent_risk: str
    intent_pattern: str
    intent_severity: str
    recommended_action: str
    engagement_score: float
    signal_score: float
    champion_score: float
    freshness_score: float
    intent_composite: float
    has_intent_gap: bool
    requires_reengagement: bool
    estimated_cold_pipeline_usd: float
    intent_signal: str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "intent_risk":                  self.intent_risk,
            "intent_pattern":               self.intent_pattern,
            "intent_severity":              self.intent_severity,
            "recommended_action":           self.recommended_action,
            "engagement_score":             self.engagement_score,
            "signal_score":                 self.signal_score,
            "champion_score":               self.champion_score,
            "freshness_score":              self.freshness_score,
            "intent_composite":             self.intent_composite,
            "has_intent_gap":               self.has_intent_gap,
            "requires_reengagement":        self.requires_reengagement,
            "estimated_cold_pipeline_usd":  self.estimated_cold_pipeline_usd,
            "intent_signal":                self.intent_signal,
        }


class SalesBuyerIntentSignalDecayEngine:
    def __init__(self) -> None:
        self._results: List[IntentResult] = []

    # ── Sub-scores ────────────────────────────────────────────────────────────

    def _engagement_score(self, i: IntentInput) -> float:
        s = 0
        if   i.website_visit_decay_rate_pct   >= 0.60: s += 40
        elif i.website_visit_decay_rate_pct   >= 0.35: s += 22
        elif i.website_visit_decay_rate_pct   >= 0.18: s += 8

        if   i.email_open_rate_decay_pct      >= 0.55: s += 35
        elif i.email_open_rate_decay_pct      >= 0.30: s += 18

        if   i.avg_days_since_last_digital_touch >= 30: s += 25
        elif i.avg_days_since_last_digital_touch >= 14: s += 12
        return min(s, 100)

    def _signal_score(self, i: IntentInput) -> float:
        s = 0
        if   i.intent_score_trend                  <= -0.60: s += 45
        elif i.intent_score_trend                  <= -0.30: s += 25
        elif i.intent_score_trend                  <= -0.10: s += 10

        if   i.buying_committee_engagement_score   <= 0.20: s += 30
        elif i.buying_committee_engagement_score   <= 0.45: s += 15

        if   i.multi_contact_engagement_rate_pct   <= 0.15: s += 25
        elif i.multi_contact_engagement_rate_pct   <= 0.35: s += 12
        return min(s, 100)

    def _champion_score(self, i: IntentInput) -> float:
        s = 0
        if   i.champion_response_latency_days     >= 14.0: s += 40
        elif i.champion_response_latency_days     >= 7.0:  s += 22
        elif i.champion_response_latency_days     >= 3.5:  s += 8

        if   i.champion_meeting_acceptance_rate_pct <= 0.20: s += 35
        elif i.champion_meeting_acceptance_rate_pct <= 0.45: s += 18

        if   i.champion_internal_forward_rate_pct  <= 0.10: s += 25
        elif i.champion_internal_forward_rate_pct  <= 0.25: s += 12
        return min(s, 100)

    def _freshness_score(self, i: IntentInput) -> float:
        s = 0
        if   i.days_since_last_positive_signal  >= 45: s += 45
        elif i.days_since_last_positive_signal  >= 21: s += 25
        elif i.days_since_last_positive_signal  >= 10: s += 10

        if   i.content_download_decay_rate_pct  >= 0.55: s += 30
        elif i.content_download_decay_rate_pct  >= 0.30: s += 15

        if   i.intent_data_coverage_score       <= 0.20: s += 25
        elif i.intent_data_coverage_score       <= 0.45: s += 12
        return min(s, 100)

    # ── Composite ─────────────────────────────────────────────────────────────

    def _composite(self, en: float, si: float, ch: float, fr: float) -> float:
        return min(round(en * 0.30 + si * 0.25 + ch * 0.25 + fr * 0.20, 2), 100.0)

    # ── Risk / Severity ───────────────────────────────────────────────────────

    def _risk(self, c: float) -> IntentRisk:
        if c >= 60: return IntentRisk.critical
        if c >= 40: return IntentRisk.high
        if c >= 20: return IntentRisk.moderate
        return IntentRisk.low

    def _severity(self, c: float) -> IntentSeverity:
        if c >= 60: return IntentSeverity.cold
        if c >= 40: return IntentSeverity.cooling
        if c >= 20: return IntentSeverity.warming
        return IntentSeverity.engaged

    # ── Pattern ───────────────────────────────────────────────────────────────

    def _pattern(self, i: IntentInput) -> IntentPattern:
        if (i.website_visit_decay_rate_pct >= 0.55
                and i.avg_days_since_last_digital_touch >= 21):
            return IntentPattern.digital_ghost
        if (i.content_download_decay_rate_pct >= 0.50
                and i.buying_committee_engagement_score <= 0.25):
            return IntentPattern.content_disengagement
        if (i.demo_no_show_rate_pct >= 0.50
                and i.demo_follow_up_response_rate_pct <= 0.25):
            return IntentPattern.demo_dropout
        if (i.champion_response_latency_days >= 10.0
                and i.champion_meeting_acceptance_rate_pct <= 0.25):
            return IntentPattern.champion_signal_fade
        if (i.evaluation_activity_score <= 0.20
                and i.trial_feature_adoption_rate_pct <= 0.20):
            return IntentPattern.evaluation_abandonment
        return IntentPattern.none

    # ── Action ────────────────────────────────────────────────────────────────

    def _action(self, risk: IntentRisk, pat: IntentPattern) -> IntentAction:
        if risk == IntentRisk.critical:
            if pat in (IntentPattern.digital_ghost, IntentPattern.evaluation_abandonment):
                return IntentAction.pipeline_purge_recommendation
            if pat == IntentPattern.champion_signal_fade:
                return IntentAction.executive_reconnect_protocol
            return IntentAction.deal_rescue_intervention
        if risk == IntentRisk.high:
            if pat == IntentPattern.digital_ghost:            return IntentAction.re_engagement_outreach
            if pat == IntentPattern.content_disengagement:   return IntentAction.content_nurture_activation
            if pat == IntentPattern.demo_dropout:             return IntentAction.demo_reactivation_campaign
            if pat == IntentPattern.champion_signal_fade:    return IntentAction.champion_reactivation_call
            if pat == IntentPattern.evaluation_abandonment:   return IntentAction.deal_rescue_intervention
            return IntentAction.intent_monitoring
        if risk == IntentRisk.moderate:
            return IntentAction.intent_monitoring
        return IntentAction.no_action

    # ── Signal ────────────────────────────────────────────────────────────────

    def _signal(self, i: IntentInput, pat: IntentPattern, comp: float) -> str:
        if comp < 20:
            return "Buyer intent signals healthy — digital engagement, champion activity, and signal freshness within benchmark targets"
        labels = {
            IntentPattern.digital_ghost:          "Digital ghost",
            IntentPattern.content_disengagement:  "Content disengagement",
            IntentPattern.demo_dropout:           "Demo dropout",
            IntentPattern.champion_signal_fade:   "Champion signal fade",
            IntentPattern.evaluation_abandonment: "Evaluation abandonment",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {round(i.website_visit_decay_rate_pct*100)}% web visit decay — "
            f"{round(i.days_since_last_positive_signal)} days since positive signal — "
            f"{round(i.champion_response_latency_days, 1)}d champion latency — "
            f"composite {round(comp)}"
        )

    # ── Flags ─────────────────────────────────────────────────────────────────

    def _has_intent_gap(self, i: IntentInput, comp: float) -> bool:
        return (comp >= 40
                or i.days_since_last_positive_signal >= 21
                or i.buying_committee_engagement_score <= 0.35)

    def _requires_reengagement(self, i: IntentInput, comp: float) -> bool:
        return (comp >= 25
                or i.champion_response_latency_days >= 7.0
                or i.website_visit_decay_rate_pct >= 0.30)

    # ── Cold pipeline estimate ────────────────────────────────────────────────

    def _cold_pipeline(self, i: IntentInput, comp: float) -> float:
        return round(
            i.deals_with_intent_decay
            * i.avg_deal_value_usd
            * (1 - max(i.buying_committee_engagement_score, 0.05))
            * (comp / 100),
            2,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def assess(self, i: IntentInput) -> IntentResult:
        en  = self._engagement_score(i)
        si  = self._signal_score(i)
        ch  = self._champion_score(i)
        fr  = self._freshness_score(i)
        comp = self._composite(en, si, ch, fr)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = IntentResult(
            rep_id=i.rep_id,
            region=i.region,
            intent_risk=risk.value,
            intent_pattern=pat.value,
            intent_severity=sev.value,
            recommended_action=act.value,
            engagement_score=en,
            signal_score=si,
            champion_score=ch,
            freshness_score=fr,
            intent_composite=comp,
            has_intent_gap=self._has_intent_gap(i, comp),
            requires_reengagement=self._requires_reengagement(i, comp),
            estimated_cold_pipeline_usd=self._cold_pipeline(i, comp),
            intent_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[IntentInput]) -> List[IntentResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_intent_composite": 0.0,
                "intent_gap_count": 0,
                "reengagement_count": 0,
                "avg_engagement_score": 0.0,
                "avg_signal_score": 0.0,
                "avg_champion_score": 0.0,
                "avg_freshness_score": 0.0,
                "total_estimated_cold_pipeline_usd": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        ten = tsi = tch = tfr = tcomp = tcp = 0.0
        gc = rc2 = 0
        for r in self._results:
            rc[r.intent_risk]      = rc.get(r.intent_risk, 0)      + 1
            pc[r.intent_pattern]   = pc.get(r.intent_pattern, 0)   + 1
            sc[r.intent_severity]  = sc.get(r.intent_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            ten  += r.engagement_score
            tsi  += r.signal_score
            tch  += r.champion_score
            tfr  += r.freshness_score
            tcomp += r.intent_composite
            tcp  += r.estimated_cold_pipeline_usd
            if r.has_intent_gap:       gc  += 1
            if r.requires_reengagement: rc2 += 1
        return {
            "total":                            n,
            "risk_counts":                      rc,
            "pattern_counts":                   pc,
            "severity_counts":                  sc,
            "action_counts":                    ac,
            "avg_intent_composite":             round(tcomp / n, 1),
            "intent_gap_count":                 gc,
            "reengagement_count":               rc2,
            "avg_engagement_score":             round(ten / n, 1),
            "avg_signal_score":                 round(tsi / n, 1),
            "avg_champion_score":               round(tch / n, 1),
            "avg_freshness_score":              round(tfr / n, 1),
            "total_estimated_cold_pipeline_usd": round(tcp, 2),
        }
