from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class CriteriaRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CriteriaPattern(str, Enum):
    none                              = "none"
    late_criteria_discovery           = "late_criteria_discovery"
    criteria_reactive_alignment       = "criteria_reactive_alignment"
    scorecard_blind_pursuit           = "scorecard_blind_pursuit"
    competitive_criteria_disadvantage = "competitive_criteria_disadvantage"
    criteria_coaching_gap             = "criteria_coaching_gap"


class CriteriaSeverity(str, Enum):
    shaping    = "shaping"
    aligned    = "aligned"
    reactive   = "reactive"
    misaligned = "misaligned"


class CriteriaAction(str, Enum):
    no_action                        = "no_action"
    criteria_mapping_coaching        = "criteria_mapping_coaching"
    early_discovery_process_coaching = "early_discovery_process_coaching"
    competitive_reframing_coaching   = "competitive_reframing_coaching"
    champion_criteria_coaching       = "champion_criteria_coaching"
    deal_qualification_review        = "deal_qualification_review"


@dataclass
class CriteriaInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    criteria_documented_early_pct: float
    criteria_influenced_by_rep_pct: float
    criteria_first_discovered_stage_avg: float
    criteria_changed_late_in_cycle_pct: float
    rep_aware_of_all_criteria_pct: float
    criteria_mapped_to_product_strength_pct: float
    competitor_criteria_advantage_rate_pct: float
    criteria_aligned_with_champion_pct: float
    scorecard_obtained_pct: float
    criteria_gap_identified_pct: float
    criteria_coaching_provided_pct: float
    lost_deals_criteria_mismatch_pct: float
    deals_won_criteria_shaped_pct: float
    avg_criteria_count_per_deal: float
    unmet_criteria_at_close_pct: float
    criteria_revision_requested_pct: float
    customer_shared_scorecard_pct: float
    total_deals_evaluated: int
    avg_opportunity_value_usd: float


@dataclass
class CriteriaResult:
    rep_id: str
    region: str
    criteria_risk: CriteriaRisk
    criteria_pattern: CriteriaPattern
    criteria_severity: CriteriaSeverity
    recommended_action: CriteriaAction
    discovery_score: float
    influence_score: float
    alignment_score: float
    competitive_score: float
    criteria_composite: float
    has_criteria_gap: bool
    requires_criteria_coaching: bool
    estimated_lost_revenue_usd: float
    criteria_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                      self.rep_id,
            "region":                      self.region,
            "criteria_risk":               self.criteria_risk.value,
            "criteria_pattern":            self.criteria_pattern.value,
            "criteria_severity":           self.criteria_severity.value,
            "recommended_action":          self.recommended_action.value,
            "discovery_score":             self.discovery_score,
            "influence_score":             self.influence_score,
            "alignment_score":             self.alignment_score,
            "competitive_score":           self.competitive_score,
            "criteria_composite":          self.criteria_composite,
            "has_criteria_gap":            self.has_criteria_gap,
            "requires_criteria_coaching":  self.requires_criteria_coaching,
            "estimated_lost_revenue_usd":  self.estimated_lost_revenue_usd,
            "criteria_signal":             self.criteria_signal,
        }


class SalesDecisionCriteriaAlignmentIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[CriteriaResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _discovery_score(self, inp: CriteriaInput) -> float:
        score = 0.0

        if inp.criteria_documented_early_pct <= 0.25:
            score += 40.0
        elif inp.criteria_documented_early_pct <= 0.50:
            score += 22.0
        elif inp.criteria_documented_early_pct <= 0.75:
            score += 8.0

        if inp.criteria_first_discovered_stage_avg >= 3.5:
            score += 35.0
        elif inp.criteria_first_discovered_stage_avg >= 2.5:
            score += 18.0

        if inp.rep_aware_of_all_criteria_pct <= 0.40:
            score += 25.0
        elif inp.rep_aware_of_all_criteria_pct <= 0.70:
            score += 12.0

        return min(score, 100.0)

    def _influence_score(self, inp: CriteriaInput) -> float:
        score = 0.0

        if inp.criteria_influenced_by_rep_pct <= 0.20:
            score += 40.0
        elif inp.criteria_influenced_by_rep_pct <= 0.40:
            score += 22.0
        elif inp.criteria_influenced_by_rep_pct <= 0.60:
            score += 8.0

        if inp.criteria_changed_late_in_cycle_pct >= 0.40:
            score += 35.0
        elif inp.criteria_changed_late_in_cycle_pct >= 0.20:
            score += 18.0

        if inp.scorecard_obtained_pct <= 0.25:
            score += 25.0
        elif inp.scorecard_obtained_pct <= 0.50:
            score += 12.0

        return min(score, 100.0)

    def _alignment_score(self, inp: CriteriaInput) -> float:
        score = 0.0

        if inp.criteria_mapped_to_product_strength_pct <= 0.30:
            score += 40.0
        elif inp.criteria_mapped_to_product_strength_pct <= 0.55:
            score += 22.0
        elif inp.criteria_mapped_to_product_strength_pct <= 0.75:
            score += 8.0

        if inp.lost_deals_criteria_mismatch_pct >= 0.50:
            score += 35.0
        elif inp.lost_deals_criteria_mismatch_pct >= 0.30:
            score += 18.0

        if inp.unmet_criteria_at_close_pct >= 0.40:
            score += 25.0
        elif inp.unmet_criteria_at_close_pct >= 0.20:
            score += 12.0

        return min(score, 100.0)

    def _competitive_score(self, inp: CriteriaInput) -> float:
        score = 0.0

        if inp.competitor_criteria_advantage_rate_pct >= 0.60:
            score += 45.0
        elif inp.competitor_criteria_advantage_rate_pct >= 0.40:
            score += 25.0
        elif inp.competitor_criteria_advantage_rate_pct >= 0.20:
            score += 10.0

        if inp.criteria_aligned_with_champion_pct <= 0.30:
            score += 30.0
        elif inp.criteria_aligned_with_champion_pct <= 0.55:
            score += 15.0

        if inp.criteria_gap_identified_pct <= 0.20:
            score += 25.0
        elif inp.criteria_gap_identified_pct <= 0.45:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: CriteriaInput,
                          discovery: float, influence: float,
                          alignment: float, competitive: float) -> CriteriaPattern:
        # Scorecard blind pursuit: no scorecard + no criteria documented
        if inp.scorecard_obtained_pct <= 0.15 and inp.criteria_documented_early_pct <= 0.30:
            return CriteriaPattern.scorecard_blind_pursuit

        # Competitive criteria disadvantage: competitor consistently wins criteria battle
        if competitive >= 40 and inp.competitor_criteria_advantage_rate_pct >= 0.50:
            return CriteriaPattern.competitive_criteria_disadvantage

        # Late criteria discovery: discovering criteria too late in cycle
        if discovery >= 35 and inp.criteria_first_discovered_stage_avg >= 3.0:
            return CriteriaPattern.late_criteria_discovery

        # Criteria coaching gap: not coaching champion on criteria
        if inp.criteria_coaching_provided_pct <= 0.20 and inp.criteria_aligned_with_champion_pct <= 0.40:
            return CriteriaPattern.criteria_coaching_gap

        # Reactive alignment: aligning late rather than shaping early
        if influence >= 30 and inp.criteria_changed_late_in_cycle_pct >= 0.30:
            return CriteriaPattern.criteria_reactive_alignment

        return CriteriaPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> CriteriaRisk:
        if composite >= 60:
            return CriteriaRisk.critical
        if composite >= 40:
            return CriteriaRisk.high
        if composite >= 20:
            return CriteriaRisk.moderate
        return CriteriaRisk.low

    def _severity(self, composite: float) -> CriteriaSeverity:
        if composite >= 60:
            return CriteriaSeverity.misaligned
        if composite >= 40:
            return CriteriaSeverity.reactive
        if composite >= 20:
            return CriteriaSeverity.aligned
        return CriteriaSeverity.shaping

    def _action(self, risk: CriteriaRisk, pattern: CriteriaPattern) -> CriteriaAction:
        if risk == CriteriaRisk.critical:
            if pattern == CriteriaPattern.competitive_criteria_disadvantage:
                return CriteriaAction.competitive_reframing_coaching
            if pattern == CriteriaPattern.scorecard_blind_pursuit:
                return CriteriaAction.deal_qualification_review
            return CriteriaAction.deal_qualification_review
        if risk == CriteriaRisk.high:
            if pattern == CriteriaPattern.late_criteria_discovery:
                return CriteriaAction.early_discovery_process_coaching
            if pattern == CriteriaPattern.criteria_coaching_gap:
                return CriteriaAction.champion_criteria_coaching
            return CriteriaAction.criteria_mapping_coaching
        if risk == CriteriaRisk.moderate:
            return CriteriaAction.criteria_mapping_coaching
        return CriteriaAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_criteria_gap(self, composite: float, inp: CriteriaInput) -> bool:
        return (
            composite >= 40
            or inp.lost_deals_criteria_mismatch_pct >= 0.40
            or inp.criteria_influenced_by_rep_pct <= 0.25
        )

    def _requires_criteria_coaching(self, composite: float, inp: CriteriaInput) -> bool:
        return (
            composite >= 30
            or inp.criteria_documented_early_pct <= 0.40
            or inp.scorecard_obtained_pct <= 0.35
        )

    # ------------------------------------------------------------------
    # Revenue loss estimate
    # ------------------------------------------------------------------

    def _estimated_lost_revenue(self, inp: CriteriaInput, composite: float) -> float:
        return round(
            inp.total_deals_evaluated
            * inp.avg_opportunity_value_usd
            * inp.lost_deals_criteria_mismatch_pct
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: CriteriaInput,
                 pattern: CriteriaPattern, composite: float) -> str:
        if pattern == CriteriaPattern.none and composite < 20:
            return "Decision criteria alignment healthy — early discovery, influence, and competitive positioning within benchmarks"
        parts: list[str] = []
        parts.append(f"{inp.criteria_documented_early_pct * 100:.0f}% criteria documented early")
        parts.append(f"{inp.criteria_influenced_by_rep_pct * 100:.0f}% criteria influenced")
        parts.append(f"{inp.lost_deals_criteria_mismatch_pct * 100:.0f}% losses from criteria mismatch")
        label = pattern.value.replace("_", " ") if pattern != CriteriaPattern.none else "Criteria risk"
        return f"{label.capitalize()} — {' — '.join(parts)} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: CriteriaInput) -> CriteriaResult:
        discovery   = round(self._discovery_score(inp), 1)
        influence   = round(self._influence_score(inp), 1)
        alignment   = round(self._alignment_score(inp), 1)
        competitive = round(self._competitive_score(inp), 1)

        composite = round(
            discovery * 0.30 + influence * 0.30 + alignment * 0.25 + competitive * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, discovery, influence, alignment, competitive)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_criteria_gap(composite, inp)
        coach  = self._requires_criteria_coaching(composite, inp)
        loss   = self._estimated_lost_revenue(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = CriteriaResult(
            rep_id=inp.rep_id,
            region=inp.region,
            criteria_risk=risk,
            criteria_pattern=pattern,
            criteria_severity=severity,
            recommended_action=action,
            discovery_score=discovery,
            influence_score=influence,
            alignment_score=alignment,
            competitive_score=competitive,
            criteria_composite=composite,
            has_criteria_gap=gap,
            requires_criteria_coaching=coach,
            estimated_lost_revenue_usd=loss,
            criteria_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[CriteriaInput]) -> list[CriteriaResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_criteria_composite": 0.0,
                "criteria_gap_count": 0,
                "coaching_count": 0,
                "avg_discovery_score": 0.0,
                "avg_influence_score": 0.0,
                "avg_alignment_score": 0.0,
                "avg_competitive_score": 0.0,
                "total_estimated_lost_revenue_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_dis = total_inf = total_ali = total_com = total_loss = 0.0

        for r in self._results:
            risk_counts[r.criteria_risk.value]       = risk_counts.get(r.criteria_risk.value, 0) + 1
            pattern_counts[r.criteria_pattern.value] = pattern_counts.get(r.criteria_pattern.value, 0) + 1
            severity_counts[r.criteria_severity.value] = severity_counts.get(r.criteria_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.criteria_composite
            total_dis  += r.discovery_score
            total_inf  += r.influence_score
            total_ali  += r.alignment_score
            total_com  += r.competitive_score
            total_loss += r.estimated_lost_revenue_usd

        n = len(self._results)

        return {
            "total":                                  n,
            "risk_counts":                            risk_counts,
            "pattern_counts":                         pattern_counts,
            "severity_counts":                        severity_counts,
            "action_counts":                          action_counts,
            "avg_criteria_composite":                 round(total_comp / n, 1),
            "criteria_gap_count":                     sum(1 for r in self._results if r.has_criteria_gap),
            "coaching_count":                         sum(1 for r in self._results if r.requires_criteria_coaching),
            "avg_discovery_score":                    round(total_dis / n, 1),
            "avg_influence_score":                    round(total_inf / n, 1),
            "avg_alignment_score":                    round(total_ali / n, 1),
            "avg_competitive_score":                  round(total_com / n, 1),
            "total_estimated_lost_revenue_usd":       round(total_loss, 2),
        }
