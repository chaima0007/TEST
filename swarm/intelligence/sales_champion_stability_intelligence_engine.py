from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ChampionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ChampionPattern(str, Enum):
    none                         = "none"
    champion_ghosting            = "champion_ghosting"
    single_thread_fragility      = "single_thread_fragility"
    champion_role_change_blindspot = "champion_role_change_blindspot"
    internal_champion_conflict   = "internal_champion_conflict"
    false_champion_reliance      = "false_champion_reliance"


class ChampionSeverity(str, Enum):
    anchored    = "anchored"
    developing  = "developing"
    fragile     = "fragile"
    exposed     = "exposed"


class ChampionAction(str, Enum):
    no_action                      = "no_action"
    champion_re_engagement_plan    = "champion_re_engagement_plan"
    multithreading_coaching        = "multithreading_coaching"
    executive_sponsor_alignment    = "executive_sponsor_alignment"
    champion_validation_coaching   = "champion_validation_coaching"
    deal_rescue_intervention       = "deal_rescue_intervention"


@dataclass
class ChampionInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    avg_champion_response_time_days: float
    champion_engagement_drop_rate_pct: float
    deals_with_single_champion_pct: float
    champion_gone_dark_rate_pct: float
    champion_role_change_detected_rate_pct: float
    champion_re_engaged_within_7d_pct: float
    deals_lost_after_champion_change_pct: float
    deals_with_executive_sponsor_pct: float
    champion_coached_on_internal_selling_pct: float
    false_champion_identified_rate_pct: float
    champion_org_chart_mapped_pct: float
    multi_thread_depth_avg: float
    champion_nps_score_avg: float
    deal_at_risk_after_ghosting_pct: float
    champion_introduced_mobilizer_pct: float
    avg_days_to_detect_champion_change: float
    champion_internal_objection_coached_pct: float
    total_active_deals: int
    avg_opportunity_value_usd: float


@dataclass
class ChampionResult:
    rep_id: str
    region: str
    champion_risk: ChampionRisk
    champion_pattern: ChampionPattern
    champion_severity: ChampionSeverity
    recommended_action: ChampionAction
    engagement_score: float
    threading_score: float
    detection_score: float
    coaching_score: float
    champion_composite: float
    has_champion_gap: bool
    requires_champion_coaching: bool
    estimated_deal_exposure_usd: float
    champion_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                       self.rep_id,
            "region":                       self.region,
            "champion_risk":                self.champion_risk.value,
            "champion_pattern":             self.champion_pattern.value,
            "champion_severity":            self.champion_severity.value,
            "recommended_action":           self.recommended_action.value,
            "engagement_score":             self.engagement_score,
            "threading_score":              self.threading_score,
            "detection_score":              self.detection_score,
            "coaching_score":               self.coaching_score,
            "champion_composite":           self.champion_composite,
            "has_champion_gap":             self.has_champion_gap,
            "requires_champion_coaching":   self.requires_champion_coaching,
            "estimated_deal_exposure_usd":  self.estimated_deal_exposure_usd,
            "champion_signal":              self.champion_signal,
        }


class SalesChampionStabilityIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ChampionResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _engagement_score(self, inp: ChampionInput) -> float:
        score = 0.0

        if inp.champion_gone_dark_rate_pct >= 0.40:
            score += 40.0
        elif inp.champion_gone_dark_rate_pct >= 0.25:
            score += 22.0
        elif inp.champion_gone_dark_rate_pct >= 0.10:
            score += 8.0

        if inp.avg_champion_response_time_days >= 7.0:
            score += 35.0
        elif inp.avg_champion_response_time_days >= 3.0:
            score += 18.0

        if inp.deal_at_risk_after_ghosting_pct >= 0.50:
            score += 25.0
        elif inp.deal_at_risk_after_ghosting_pct >= 0.25:
            score += 12.0

        return min(score, 100.0)

    def _threading_score(self, inp: ChampionInput) -> float:
        score = 0.0

        if inp.deals_with_single_champion_pct >= 0.70:
            score += 40.0
        elif inp.deals_with_single_champion_pct >= 0.50:
            score += 22.0
        elif inp.deals_with_single_champion_pct >= 0.30:
            score += 8.0

        if inp.multi_thread_depth_avg <= 1.5:
            score += 35.0
        elif inp.multi_thread_depth_avg <= 2.5:
            score += 18.0

        if inp.deals_with_executive_sponsor_pct <= 0.15:
            score += 25.0
        elif inp.deals_with_executive_sponsor_pct <= 0.35:
            score += 12.0

        return min(score, 100.0)

    def _detection_score(self, inp: ChampionInput) -> float:
        score = 0.0

        if inp.avg_days_to_detect_champion_change >= 14.0:
            score += 40.0
        elif inp.avg_days_to_detect_champion_change >= 7.0:
            score += 22.0
        elif inp.avg_days_to_detect_champion_change >= 3.0:
            score += 8.0

        if inp.champion_re_engaged_within_7d_pct <= 0.30:
            score += 35.0
        elif inp.champion_re_engaged_within_7d_pct <= 0.60:
            score += 18.0

        if inp.deals_lost_after_champion_change_pct >= 0.60:
            score += 25.0
        elif inp.deals_lost_after_champion_change_pct >= 0.35:
            score += 12.0

        return min(score, 100.0)

    def _coaching_score(self, inp: ChampionInput) -> float:
        score = 0.0

        if inp.champion_coached_on_internal_selling_pct <= 0.20:
            score += 40.0
        elif inp.champion_coached_on_internal_selling_pct <= 0.50:
            score += 22.0
        elif inp.champion_coached_on_internal_selling_pct <= 0.75:
            score += 8.0

        if inp.false_champion_identified_rate_pct >= 0.40:
            score += 35.0
        elif inp.false_champion_identified_rate_pct >= 0.20:
            score += 18.0

        if inp.champion_introduced_mobilizer_pct <= 0.15:
            score += 25.0
        elif inp.champion_introduced_mobilizer_pct <= 0.35:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ChampionInput,
                          engagement: float, threading: float,
                          detection: float, coaching: float) -> ChampionPattern:
        # False champion reliance: high false-champion rate + low coaching
        if inp.false_champion_identified_rate_pct >= 0.35 and inp.champion_coached_on_internal_selling_pct <= 0.30:
            return ChampionPattern.false_champion_reliance

        # Internal champion conflict: champion org not mapped + low mobilizer
        if inp.champion_org_chart_mapped_pct <= 0.25 and inp.champion_introduced_mobilizer_pct <= 0.15:
            return ChampionPattern.internal_champion_conflict

        # Single thread fragility: most deals single threaded
        if threading >= 35 and inp.deals_with_single_champion_pct >= 0.60:
            return ChampionPattern.single_thread_fragility

        # Champion ghosting: high gone-dark rate
        if engagement >= 35 and inp.champion_gone_dark_rate_pct >= 0.30:
            return ChampionPattern.champion_ghosting

        # Role change blindspot: slow detection of champion changes
        if detection >= 30 and inp.avg_days_to_detect_champion_change >= 10.0:
            return ChampionPattern.champion_role_change_blindspot

        return ChampionPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ChampionRisk:
        if composite >= 60:
            return ChampionRisk.critical
        if composite >= 40:
            return ChampionRisk.high
        if composite >= 20:
            return ChampionRisk.moderate
        return ChampionRisk.low

    def _severity(self, composite: float) -> ChampionSeverity:
        if composite >= 60:
            return ChampionSeverity.exposed
        if composite >= 40:
            return ChampionSeverity.fragile
        if composite >= 20:
            return ChampionSeverity.developing
        return ChampionSeverity.anchored

    def _action(self, risk: ChampionRisk, pattern: ChampionPattern) -> ChampionAction:
        if risk == ChampionRisk.critical:
            if pattern == ChampionPattern.false_champion_reliance:
                return ChampionAction.champion_validation_coaching
            if pattern == ChampionPattern.single_thread_fragility:
                return ChampionAction.deal_rescue_intervention
            return ChampionAction.deal_rescue_intervention
        if risk == ChampionRisk.high:
            if pattern == ChampionPattern.champion_ghosting:
                return ChampionAction.champion_re_engagement_plan
            if pattern == ChampionPattern.internal_champion_conflict:
                return ChampionAction.executive_sponsor_alignment
            return ChampionAction.multithreading_coaching
        if risk == ChampionRisk.moderate:
            return ChampionAction.multithreading_coaching
        return ChampionAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_champion_gap(self, composite: float, inp: ChampionInput) -> bool:
        return (
            composite >= 40
            or inp.deals_with_single_champion_pct >= 0.60
            or inp.champion_gone_dark_rate_pct >= 0.30
        )

    def _requires_champion_coaching(self, composite: float, inp: ChampionInput) -> bool:
        return (
            composite >= 30
            or inp.champion_coached_on_internal_selling_pct <= 0.40
            or inp.false_champion_identified_rate_pct >= 0.20
        )

    # ------------------------------------------------------------------
    # Deal exposure estimate
    # ------------------------------------------------------------------

    def _estimated_deal_exposure(self, inp: ChampionInput, composite: float) -> float:
        return round(
            inp.total_active_deals
            * inp.avg_opportunity_value_usd
            * inp.champion_gone_dark_rate_pct
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ChampionInput,
                 pattern: ChampionPattern, composite: float) -> str:
        if pattern == ChampionPattern.none and composite < 20:
            return "Champion stability healthy — engagement, multithreading, and detection response within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.champion_gone_dark_rate_pct * 100:.0f}% champions gone dark")
        parts.append(f"{inp.deals_with_single_champion_pct * 100:.0f}% single-thread deals")
        parts.append(f"{inp.avg_days_to_detect_champion_change:.0f} days to detect change")
        label = pattern.value.replace("_", " ") if pattern != ChampionPattern.none else "Champion risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ChampionInput) -> ChampionResult:
        engagement = round(self._engagement_score(inp), 1)
        threading  = round(self._threading_score(inp), 1)
        detection  = round(self._detection_score(inp), 1)
        coaching   = round(self._coaching_score(inp), 1)

        composite = round(
            engagement * 0.30 + threading * 0.30 + detection * 0.25 + coaching * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, engagement, threading, detection, coaching)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_champion_gap(composite, inp)
        coach  = self._requires_champion_coaching(composite, inp)
        loss   = self._estimated_deal_exposure(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = ChampionResult(
            rep_id=inp.rep_id,
            region=inp.region,
            champion_risk=risk,
            champion_pattern=pattern,
            champion_severity=severity,
            recommended_action=action,
            engagement_score=engagement,
            threading_score=threading,
            detection_score=detection,
            coaching_score=coaching,
            champion_composite=composite,
            has_champion_gap=gap,
            requires_champion_coaching=coach,
            estimated_deal_exposure_usd=loss,
            champion_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ChampionInput]) -> list[ChampionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_champion_composite": 0.0,
                "champion_gap_count": 0,
                "coaching_count": 0,
                "avg_engagement_score": 0.0,
                "avg_threading_score": 0.0,
                "avg_detection_score": 0.0,
                "avg_coaching_score": 0.0,
                "total_estimated_deal_exposure_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_eng = total_thr = total_det = total_coa = total_loss = 0.0

        for r in self._results:
            risk_counts[r.champion_risk.value]       = risk_counts.get(r.champion_risk.value, 0) + 1
            pattern_counts[r.champion_pattern.value] = pattern_counts.get(r.champion_pattern.value, 0) + 1
            severity_counts[r.champion_severity.value] = severity_counts.get(r.champion_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.champion_composite
            total_eng  += r.engagement_score
            total_thr  += r.threading_score
            total_det  += r.detection_score
            total_coa  += r.coaching_score
            total_loss += r.estimated_deal_exposure_usd

        n = len(self._results)

        return {
            "total":                                   n,
            "risk_counts":                             risk_counts,
            "pattern_counts":                          pattern_counts,
            "severity_counts":                         severity_counts,
            "action_counts":                           action_counts,
            "avg_champion_composite":                  round(total_comp / n, 1),
            "champion_gap_count":                      sum(1 for r in self._results if r.has_champion_gap),
            "coaching_count":                          sum(1 for r in self._results if r.requires_champion_coaching),
            "avg_engagement_score":                    round(total_eng / n, 1),
            "avg_threading_score":                     round(total_thr / n, 1),
            "avg_detection_score":                     round(total_det / n, 1),
            "avg_coaching_score":                      round(total_coa / n, 1),
            "total_estimated_deal_exposure_usd":       round(total_loss, 2),
        }
