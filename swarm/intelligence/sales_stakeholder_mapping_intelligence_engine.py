from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class StakeholderRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class StakeholderPattern(str, Enum):
    none                = "none"
    single_threaded     = "single_threaded"
    champion_dependency = "champion_dependency"
    economic_blind_spot = "economic_blind_spot"
    blocker_ignored     = "blocker_ignored"
    org_chart_gap       = "org_chart_gap"


class StakeholderSeverity(str, Enum):
    mapped       = "mapped"
    developing   = "developing"
    fragile      = "fragile"
    exposed      = "exposed"


class StakeholderAction(str, Enum):
    no_action                        = "no_action"
    stakeholder_tracking_coaching    = "stakeholder_tracking_coaching"
    multi_thread_coaching            = "multi_thread_coaching"
    economic_buyer_coaching          = "economic_buyer_coaching"
    blocker_neutralization_coaching  = "blocker_neutralization_coaching"
    executive_sponsor_escalation     = "executive_sponsor_escalation"
    deal_rescue_intervention         = "deal_rescue_intervention"


@dataclass
class StakeholderMappingInput:
    rep_id:                          str
    region:                          str
    evaluation_period_id:            str
    avg_stakeholders_per_deal:       float   # count
    economic_buyer_identified_pct:   float   # 0-1
    champion_identified_pct:         float   # 0-1
    executive_sponsor_engaged_pct:   float   # 0-1
    blocker_identified_pct:          float   # 0-1
    multi_contact_deal_pct:          float   # 0-1 (>1 contact per deal)
    org_chart_mapped_pct:            float   # 0-1
    champion_strength_score:         float   # 0-1
    single_threaded_deal_pct:        float   # 0-1
    procurement_engaged_pct:         float   # 0-1 (when applicable)
    it_stakeholder_engaged_pct:      float   # 0-1
    legal_engaged_pct:               float   # 0-1
    end_user_engaged_pct:            float   # 0-1
    decision_process_mapped_pct:     float   # 0-1
    coach_to_champion_pct:           float   # 0-1 (coaches becoming champions)
    stakeholder_sentiment_score:     float   # 0-1
    total_active_deals:              int
    avg_deal_value_usd:              float
    avg_stakeholder_count_benchmark: float   # org benchmark


@dataclass
class StakeholderMappingResult:
    rep_id:                          str
    region:                          str
    stakeholder_risk:                StakeholderRisk
    stakeholder_pattern:             StakeholderPattern
    stakeholder_severity:            StakeholderSeverity
    recommended_action:              StakeholderAction
    coverage_score:                  float
    champion_quality_score:          float
    economic_alignment_score:        float
    process_intelligence_score:      float
    stakeholder_composite:           float
    has_stakeholder_gap:             bool
    requires_stakeholder_coaching:   bool
    estimated_deal_risk_usd:         float
    stakeholder_signal:              str

    def to_dict(self) -> Dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "stakeholder_risk":                 self.stakeholder_risk.value,
            "stakeholder_pattern":              self.stakeholder_pattern.value,
            "stakeholder_severity":             self.stakeholder_severity.value,
            "recommended_action":               self.recommended_action.value,
            "coverage_score":                   self.coverage_score,
            "champion_quality_score":           self.champion_quality_score,
            "economic_alignment_score":         self.economic_alignment_score,
            "process_intelligence_score":       self.process_intelligence_score,
            "stakeholder_composite":            self.stakeholder_composite,
            "has_stakeholder_gap":              self.has_stakeholder_gap,
            "requires_stakeholder_coaching":    self.requires_stakeholder_coaching,
            "estimated_deal_risk_usd":          self.estimated_deal_risk_usd,
            "stakeholder_signal":               self.stakeholder_signal,
        }


class SalesStakeholderMappingIntelligenceEngine:
    """Detects per-rep stakeholder blindspots — single-threading, champion dependency, economic buyer gaps."""

    def __init__(self) -> None:
        self._results: List[StakeholderMappingResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────

    def _coverage_score(self, inp: StakeholderMappingInput) -> float:
        s = 0.0
        if   inp.multi_contact_deal_pct       <= 0.40: s += 40
        elif inp.multi_contact_deal_pct       <= 0.60: s += 22
        elif inp.multi_contact_deal_pct       <= 0.80: s += 8
        if   inp.avg_stakeholders_per_deal    <= 1.5:  s += 35
        elif inp.avg_stakeholders_per_deal    <= 2.5:  s += 18
        if   inp.org_chart_mapped_pct         <= 0.30: s += 25
        elif inp.org_chart_mapped_pct         <= 0.55: s += 12
        return min(s, 100.0)

    def _champion_quality_score(self, inp: StakeholderMappingInput) -> float:
        s = 0.0
        if   inp.champion_identified_pct      <= 0.40: s += 40
        elif inp.champion_identified_pct      <= 0.65: s += 22
        elif inp.champion_identified_pct      <= 0.85: s += 8
        if   inp.champion_strength_score      <= 0.30: s += 35
        elif inp.champion_strength_score      <= 0.55: s += 18
        if   inp.coach_to_champion_pct        <= 0.20: s += 25
        elif inp.coach_to_champion_pct        <= 0.45: s += 12
        return min(s, 100.0)

    def _economic_alignment_score(self, inp: StakeholderMappingInput) -> float:
        s = 0.0
        if   inp.economic_buyer_identified_pct <= 0.35: s += 45
        elif inp.economic_buyer_identified_pct <= 0.60: s += 25
        elif inp.economic_buyer_identified_pct <= 0.80: s += 10
        if   inp.executive_sponsor_engaged_pct <= 0.20: s += 30
        elif inp.executive_sponsor_engaged_pct <= 0.45: s += 15
        if   inp.single_threaded_deal_pct      >= 0.50: s += 25
        elif inp.single_threaded_deal_pct      >= 0.30: s += 12
        return min(s, 100.0)

    def _process_intelligence_score(self, inp: StakeholderMappingInput) -> float:
        s = 0.0
        if   inp.decision_process_mapped_pct  <= 0.30: s += 40
        elif inp.decision_process_mapped_pct  <= 0.55: s += 22
        elif inp.decision_process_mapped_pct  <= 0.75: s += 8
        if   inp.blocker_identified_pct       <= 0.25: s += 35
        elif inp.blocker_identified_pct       <= 0.50: s += 18
        if   inp.stakeholder_sentiment_score  <= 0.35: s += 25
        elif inp.stakeholder_sentiment_score  <= 0.60: s += 12
        return min(s, 100.0)

    # ── composite ─────────────────────────────────────────────────────────

    def _composite(self, co: float, cq: float, ea: float, pi: float) -> float:
        return min(round(co * 0.30 + cq * 0.25 + ea * 0.30 + pi * 0.15, 2), 100.0)

    # ── pattern ───────────────────────────────────────────────────────────

    def _pattern(self, inp: StakeholderMappingInput) -> StakeholderPattern:
        if inp.single_threaded_deal_pct >= 0.55 and inp.avg_stakeholders_per_deal <= 1.5:
            return StakeholderPattern.single_threaded
        if inp.champion_strength_score <= 0.30 and inp.coach_to_champion_pct <= 0.20:
            return StakeholderPattern.champion_dependency
        if inp.economic_buyer_identified_pct <= 0.35 and inp.executive_sponsor_engaged_pct <= 0.20:
            return StakeholderPattern.economic_blind_spot
        if inp.blocker_identified_pct <= 0.20 and inp.decision_process_mapped_pct <= 0.35:
            return StakeholderPattern.blocker_ignored
        if inp.org_chart_mapped_pct <= 0.30 and inp.multi_contact_deal_pct <= 0.45:
            return StakeholderPattern.org_chart_gap
        return StakeholderPattern.none

    # ── thresholds ────────────────────────────────────────────────────────

    def _risk(self, composite: float) -> StakeholderRisk:
        if   composite >= 60: return StakeholderRisk.critical
        elif composite >= 40: return StakeholderRisk.high
        elif composite >= 20: return StakeholderRisk.moderate
        return StakeholderRisk.low

    def _severity(self, composite: float) -> StakeholderSeverity:
        if   composite >= 60: return StakeholderSeverity.exposed
        elif composite >= 40: return StakeholderSeverity.fragile
        elif composite >= 20: return StakeholderSeverity.developing
        return StakeholderSeverity.mapped

    def _action(self, risk: StakeholderRisk, pattern: StakeholderPattern) -> StakeholderAction:
        if risk == StakeholderRisk.critical:
            if pattern in (StakeholderPattern.single_threaded, StakeholderPattern.champion_dependency):
                return StakeholderAction.deal_rescue_intervention
            return StakeholderAction.executive_sponsor_escalation
        if risk == StakeholderRisk.high:
            if pattern == StakeholderPattern.single_threaded:
                return StakeholderAction.multi_thread_coaching
            if pattern == StakeholderPattern.champion_dependency:
                return StakeholderAction.multi_thread_coaching
            if pattern == StakeholderPattern.economic_blind_spot:
                return StakeholderAction.economic_buyer_coaching
            if pattern == StakeholderPattern.blocker_ignored:
                return StakeholderAction.blocker_neutralization_coaching
            if pattern == StakeholderPattern.org_chart_gap:
                return StakeholderAction.stakeholder_tracking_coaching
            return StakeholderAction.multi_thread_coaching
        if risk == StakeholderRisk.moderate:
            return StakeholderAction.stakeholder_tracking_coaching
        return StakeholderAction.no_action

    # ── flags ─────────────────────────────────────────────────────────────

    def _has_gap(self, inp: StakeholderMappingInput, composite: float) -> bool:
        return (
            composite >= 40
            or inp.single_threaded_deal_pct         >= 0.35
            or inp.economic_buyer_identified_pct    <= 0.60
        )

    def _requires_coaching(self, inp: StakeholderMappingInput, composite: float) -> bool:
        return (
            composite >= 25
            or inp.champion_strength_score           <= 0.50
            or inp.multi_contact_deal_pct            <= 0.65
        )

    # ── dollar impact ─────────────────────────────────────────────────────

    def _deal_risk(self, inp: StakeholderMappingInput, composite: float) -> float:
        risk_multiplier = max(0.0, inp.single_threaded_deal_pct) * (composite / 100)
        return round(
            inp.total_active_deals
            * inp.avg_deal_value_usd
            * risk_multiplier,
            2,
        )

    # ── signal ────────────────────────────────────────────────────────────

    _PATTERN_LABELS = {
        StakeholderPattern.single_threaded:     "Single-threaded",
        StakeholderPattern.champion_dependency: "Champion dependency",
        StakeholderPattern.economic_blind_spot: "Economic blind spot",
        StakeholderPattern.blocker_ignored:     "Blocker ignored",
        StakeholderPattern.org_chart_gap:       "Org chart gap",
    }

    def _signal(self, inp: StakeholderMappingInput, pattern: StakeholderPattern, composite: float) -> str:
        if composite < 20:
            return (
                "Stakeholder mapping strong — multi-threading, champion quality, "
                "economic buyer alignment, and decision process within benchmarks"
            )
        label     = self._PATTERN_LABELS.get(pattern, pattern.value.replace("_", " ").title())
        thread_pct = round(inp.single_threaded_deal_pct * 100)
        eb_pct     = round(inp.economic_buyer_identified_pct * 100)
        champ_pct  = round(inp.champion_identified_pct * 100)
        comp_int   = round(composite)
        return (
            f"{label} — {thread_pct}% single-threaded deals — "
            f"{eb_pct}% economic buyers identified — "
            f"{champ_pct}% champions identified — composite {comp_int}"
        )

    # ── public API ────────────────────────────────────────────────────────

    def assess(self, inp: StakeholderMappingInput) -> StakeholderMappingResult:
        co  = self._coverage_score(inp)
        cq  = self._champion_quality_score(inp)
        ea  = self._economic_alignment_score(inp)
        pi  = self._process_intelligence_score(inp)
        comp = self._composite(co, cq, ea, pi)

        pattern  = self._pattern(inp)
        risk     = self._risk(comp)
        severity = self._severity(comp)
        action   = self._action(risk, pattern)

        result = StakeholderMappingResult(
            rep_id                      = inp.rep_id,
            region                      = inp.region,
            stakeholder_risk            = risk,
            stakeholder_pattern         = pattern,
            stakeholder_severity        = severity,
            recommended_action          = action,
            coverage_score              = co,
            champion_quality_score      = cq,
            economic_alignment_score    = ea,
            process_intelligence_score  = pi,
            stakeholder_composite       = comp,
            has_stakeholder_gap         = self._has_gap(inp, comp),
            requires_stakeholder_coaching = self._requires_coaching(inp, comp),
            estimated_deal_risk_usd     = self._deal_risk(inp, comp),
            stakeholder_signal          = self._signal(inp, pattern, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[StakeholderMappingInput]) -> List[StakeholderMappingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_stakeholder_composite": 0.0,
                "stakeholder_gap_count": 0,
                "coaching_count": 0,
                "avg_coverage_score": 0.0,
                "avg_champion_quality_score": 0.0,
                "avg_economic_alignment_score": 0.0,
                "avg_process_intelligence_score": 0.0,
                "total_estimated_deal_risk_usd": 0.0,
            }

        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        total_comp = total_co = total_cq = total_ea = total_pi = total_dr = 0.0
        gap_count = coaching_count = 0

        for res in self._results:
            risk_counts[res.stakeholder_risk.value]       = risk_counts.get(res.stakeholder_risk.value, 0) + 1
            pattern_counts[res.stakeholder_pattern.value] = pattern_counts.get(res.stakeholder_pattern.value, 0) + 1
            severity_counts[res.stakeholder_severity.value] = severity_counts.get(res.stakeholder_severity.value, 0) + 1
            action_counts[res.recommended_action.value]   = action_counts.get(res.recommended_action.value, 0) + 1
            total_comp += res.stakeholder_composite
            total_co   += res.coverage_score
            total_cq   += res.champion_quality_score
            total_ea   += res.economic_alignment_score
            total_pi   += res.process_intelligence_score
            total_dr   += res.estimated_deal_risk_usd
            if res.has_stakeholder_gap:           gap_count      += 1
            if res.requires_stakeholder_coaching:  coaching_count += 1

        n = len(self._results)
        return {
            "total":                                n,
            "risk_counts":                          risk_counts,
            "pattern_counts":                       pattern_counts,
            "severity_counts":                      severity_counts,
            "action_counts":                        action_counts,
            "avg_stakeholder_composite":            round(total_comp / n, 1),
            "stakeholder_gap_count":                gap_count,
            "coaching_count":                       coaching_count,
            "avg_coverage_score":                   round(total_co / n, 1),
            "avg_champion_quality_score":           round(total_cq / n, 1),
            "avg_economic_alignment_score":         round(total_ea / n, 1),
            "avg_process_intelligence_score":       round(total_pi / n, 1),
            "total_estimated_deal_risk_usd":        round(total_dr, 2),
        }
