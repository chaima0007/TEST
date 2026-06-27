from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ObjectionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ObjectionPattern(str, Enum):
    none                    = "none"
    price_barrier           = "price_barrier"
    timing_stall            = "timing_stall"
    competitive_displacement = "competitive_displacement"
    authority_gap           = "authority_gap"
    need_misalignment       = "need_misalignment"


class ObjectionSeverity(str, Enum):
    managed    = "managed"
    recurring  = "recurring"
    systemic   = "systemic"
    blocking   = "blocking"


class ObjectionAction(str, Enum):
    no_action          = "no_action"
    objection_coaching = "objection_coaching"
    messaging_update   = "messaging_update"
    battlecard_refresh = "battlecard_refresh"
    pricing_review     = "pricing_review"


@dataclass
class ObjectionPatternInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_deals_with_objections: int
    price_objections_count: int
    timing_objections_count: int
    competition_objections_count: int
    authority_objections_count: int
    need_fit_objections_count: int
    objections_per_deal_avg: float
    objection_overcome_rate_pct: float
    price_overcome_rate_pct: float
    competition_overcome_rate_pct: float
    timing_overcome_rate_pct: float
    objection_stall_avg_days: float
    late_stage_objections_count: int
    recurring_objection_same_account_count: int
    lost_deals_due_to_objection_count: int
    deals_lost_to_price_count: int
    deals_lost_to_competition_count: int
    objection_documentation_rate_pct: float
    avg_deal_size_usd: float


@dataclass
class ObjectionPatternResult:
    rep_id: str
    region: str
    objection_risk: ObjectionRisk
    objection_pattern: ObjectionPattern
    objection_severity: ObjectionSeverity
    recommended_action: ObjectionAction
    price_pressure_score: float
    competition_pressure_score: float
    timing_resistance_score: float
    skill_gap_score: float
    objection_burden_composite: float
    has_systemic_issue: bool
    requires_coaching_intervention: bool
    estimated_lost_revenue_usd: float
    objection_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "objection_risk":                   self.objection_risk.value,
            "objection_pattern":                self.objection_pattern.value,
            "objection_severity":               self.objection_severity.value,
            "recommended_action":               self.recommended_action.value,
            "price_pressure_score":             self.price_pressure_score,
            "competition_pressure_score":       self.competition_pressure_score,
            "timing_resistance_score":          self.timing_resistance_score,
            "skill_gap_score":                  self.skill_gap_score,
            "objection_burden_composite":       self.objection_burden_composite,
            "has_systemic_issue":               self.has_systemic_issue,
            "requires_coaching_intervention":   self.requires_coaching_intervention,
            "estimated_lost_revenue_usd":       self.estimated_lost_revenue_usd,
            "objection_signal":                 self.objection_signal,
        }


class SalesObjectionPatternIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ObjectionPatternResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100)
    # ------------------------------------------------------------------

    def _price_pressure_score(self, inp: ObjectionPatternInput) -> float:
        score = 0.0
        total = max(inp.total_deals_with_objections, 1)

        price_ratio = inp.price_objections_count / total
        if price_ratio >= 0.50:
            score += 35.0
        elif price_ratio >= 0.30:
            score += 20.0
        elif price_ratio >= 0.10:
            score += 8.0

        if inp.price_overcome_rate_pct < 0.30:
            score += 30.0
        elif inp.price_overcome_rate_pct < 0.50:
            score += 15.0

        if inp.deals_lost_to_price_count >= 4:
            score += 25.0
        elif inp.deals_lost_to_price_count >= 2:
            score += 15.0
        elif inp.deals_lost_to_price_count >= 1:
            score += 8.0

        # Undocumented price objections (hidden problem)
        if inp.objection_documentation_rate_pct < 0.50 and inp.price_objections_count >= 2:
            score += 5.0

        return min(score, 100.0)

    def _competition_pressure_score(self, inp: ObjectionPatternInput) -> float:
        score = 0.0
        total = max(inp.total_deals_with_objections, 1)

        comp_ratio = inp.competition_objections_count / total
        if comp_ratio >= 0.40:
            score += 35.0
        elif comp_ratio >= 0.20:
            score += 20.0
        elif comp_ratio >= 0.10:
            score += 8.0

        if inp.competition_overcome_rate_pct < 0.30:
            score += 30.0
        elif inp.competition_overcome_rate_pct < 0.50:
            score += 15.0

        if inp.deals_lost_to_competition_count >= 4:
            score += 25.0
        elif inp.deals_lost_to_competition_count >= 2:
            score += 15.0
        elif inp.deals_lost_to_competition_count >= 1:
            score += 8.0

        # Late stage competitive objections = battlecard failure
        if inp.late_stage_objections_count >= 3 and inp.competition_objections_count >= 2:
            score += 5.0

        return min(score, 100.0)

    def _timing_resistance_score(self, inp: ObjectionPatternInput) -> float:
        score = 0.0
        total = max(inp.total_deals_with_objections, 1)

        timing_ratio = inp.timing_objections_count / total
        if timing_ratio >= 0.40:
            score += 30.0
        elif timing_ratio >= 0.25:
            score += 18.0
        elif timing_ratio >= 0.10:
            score += 8.0

        if inp.timing_overcome_rate_pct < 0.25:
            score += 30.0
        elif inp.timing_overcome_rate_pct < 0.45:
            score += 15.0

        if inp.late_stage_objections_count >= 4:
            score += 25.0
        elif inp.late_stage_objections_count >= 2:
            score += 12.0

        if inp.objection_stall_avg_days >= 14.0:
            score += 15.0
        elif inp.objection_stall_avg_days >= 7.0:
            score += 8.0

        return min(score, 100.0)

    def _skill_gap_score(self, inp: ObjectionPatternInput) -> float:
        score = 0.0

        if inp.objections_per_deal_avg >= 3.0:
            score += 25.0
        elif inp.objections_per_deal_avg >= 2.0:
            score += 15.0
        elif inp.objections_per_deal_avg >= 1.5:
            score += 8.0

        if inp.objection_overcome_rate_pct < 0.25:
            score += 35.0
        elif inp.objection_overcome_rate_pct < 0.40:
            score += 20.0
        elif inp.objection_overcome_rate_pct < 0.55:
            score += 8.0

        if inp.recurring_objection_same_account_count >= 3:
            score += 20.0
        elif inp.recurring_objection_same_account_count >= 1:
            score += 10.0

        authority_need_combined = inp.authority_objections_count + inp.need_fit_objections_count
        if authority_need_combined >= 5:
            score += 15.0
        elif authority_need_combined >= 2:
            score += 8.0

        # Undocumented objections mask the problem
        if inp.objection_documentation_rate_pct < 0.40:
            score += 5.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ObjectionPatternInput,
                         price: float, competition: float,
                         timing: float, skill: float) -> ObjectionPattern:
        # Priority: competitive_displacement > price_barrier > timing_stall
        #           > authority_gap > need_misalignment > none
        if competition >= 35 and inp.deals_lost_to_competition_count >= 2:
            return ObjectionPattern.competitive_displacement
        if price >= 35 and inp.deals_lost_to_price_count >= 2:
            return ObjectionPattern.price_barrier
        if timing >= 30 and inp.late_stage_objections_count >= 2:
            return ObjectionPattern.timing_stall
        if inp.authority_objections_count >= 3 and skill >= 25:
            return ObjectionPattern.authority_gap
        if inp.need_fit_objections_count >= 3 and inp.objection_overcome_rate_pct < 0.40:
            return ObjectionPattern.need_misalignment
        return ObjectionPattern.none

    # ------------------------------------------------------------------
    # Risk / severity / action
    # ------------------------------------------------------------------

    def _risk_level(self, composite: float) -> ObjectionRisk:
        if composite >= 60:
            return ObjectionRisk.critical
        if composite >= 40:
            return ObjectionRisk.high
        if composite >= 20:
            return ObjectionRisk.moderate
        return ObjectionRisk.low

    def _severity(self, composite: float) -> ObjectionSeverity:
        if composite >= 60:
            return ObjectionSeverity.blocking
        if composite >= 40:
            return ObjectionSeverity.systemic
        if composite >= 20:
            return ObjectionSeverity.recurring
        return ObjectionSeverity.managed

    def _action(self, risk: ObjectionRisk, pattern: ObjectionPattern) -> ObjectionAction:
        if risk == ObjectionRisk.critical:
            if pattern == ObjectionPattern.price_barrier:
                return ObjectionAction.pricing_review
            if pattern == ObjectionPattern.competitive_displacement:
                return ObjectionAction.battlecard_refresh
            return ObjectionAction.messaging_update
        if risk == ObjectionRisk.high:
            if pattern == ObjectionPattern.price_barrier:
                return ObjectionAction.pricing_review
            if pattern == ObjectionPattern.competitive_displacement:
                return ObjectionAction.battlecard_refresh
            return ObjectionAction.objection_coaching
        if risk == ObjectionRisk.moderate:
            return ObjectionAction.objection_coaching
        return ObjectionAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_systemic_issue(self, composite: float, inp: ObjectionPatternInput) -> bool:
        return (
            composite >= 40
            or inp.lost_deals_due_to_objection_count >= 4
            or inp.recurring_objection_same_account_count >= 3
        )

    def _requires_coaching_intervention(self, composite: float, inp: ObjectionPatternInput) -> bool:
        return (
            composite >= 30
            or inp.objection_overcome_rate_pct < 0.25
            or (inp.objection_documentation_rate_pct < 0.40 and composite >= 20)
        )

    # ------------------------------------------------------------------
    # Revenue impact
    # ------------------------------------------------------------------

    def _estimated_lost_revenue(self, inp: ObjectionPatternInput, composite: float) -> float:
        return round(inp.lost_deals_due_to_objection_count * inp.avg_deal_size_usd * (composite / 100.0), 2)

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ObjectionPatternInput,
                pattern: ObjectionPattern, composite: float) -> str:
        if pattern == ObjectionPattern.none and composite < 20:
            return "Objection handling aligned with team benchmarks"
        parts: list[str] = []
        total = max(inp.total_deals_with_objections, 1)
        price_ratio = inp.price_objections_count / total
        comp_ratio  = inp.competition_objections_count / total
        if price_ratio >= 0.30:
            parts.append(f"price objections in {inp.price_objections_count}/{inp.total_deals_with_objections} deals")
        if comp_ratio >= 0.20:
            parts.append(f"competitive pressure in {inp.competition_objections_count} deals")
        if inp.late_stage_objections_count >= 2:
            parts.append(f"{inp.late_stage_objections_count} late-stage objections")
        if inp.objection_overcome_rate_pct < 0.40:
            parts.append(f"{inp.objection_overcome_rate_pct*100:.0f}% overcome rate")
        label = pattern.value.replace("_", " ") if pattern != ObjectionPattern.none else "Objection risk"
        summary = " — ".join(parts) if parts else "objection burden detected"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ObjectionPatternInput) -> ObjectionPatternResult:
        price  = round(self._price_pressure_score(inp), 1)
        comp   = round(self._competition_pressure_score(inp), 1)
        timing = round(self._timing_resistance_score(inp), 1)
        skill  = round(self._skill_gap_score(inp), 1)

        composite = round(price * 0.30 + comp * 0.25 + timing * 0.25 + skill * 0.20, 1)
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, price, comp, timing, skill)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        is_si = self._has_systemic_issue(composite, inp)
        is_ci = self._requires_coaching_intervention(composite, inp)
        revenue = self._estimated_lost_revenue(inp, composite)
        signal  = self._signal(inp, pattern, composite)

        result = ObjectionPatternResult(
            rep_id=inp.rep_id,
            region=inp.region,
            objection_risk=risk,
            objection_pattern=pattern,
            objection_severity=severity,
            recommended_action=action,
            price_pressure_score=price,
            competition_pressure_score=comp,
            timing_resistance_score=timing,
            skill_gap_score=skill,
            objection_burden_composite=composite,
            has_systemic_issue=is_si,
            requires_coaching_intervention=is_ci,
            estimated_lost_revenue_usd=revenue,
            objection_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ObjectionPatternInput]) -> list[ObjectionPatternResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_objection_burden_composite": 0.0,
                "systemic_issue_count": 0,
                "coaching_intervention_count": 0,
                "avg_price_pressure_score": 0.0,
                "avg_competition_pressure_score": 0.0,
                "avg_timing_resistance_score": 0.0,
                "avg_skill_gap_score": 0.0,
                "total_estimated_lost_revenue_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_price = total_comp_p = total_timing = total_skill = total_rev = 0.0

        for r in self._results:
            risk_counts[r.objection_risk.value]       = risk_counts.get(r.objection_risk.value, 0) + 1
            pattern_counts[r.objection_pattern.value] = pattern_counts.get(r.objection_pattern.value, 0) + 1
            severity_counts[r.objection_severity.value] = severity_counts.get(r.objection_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp    += r.objection_burden_composite
            total_price   += r.price_pressure_score
            total_comp_p  += r.competition_pressure_score
            total_timing  += r.timing_resistance_score
            total_skill   += r.skill_gap_score
            total_rev     += r.estimated_lost_revenue_usd

        n = len(self._results)

        return {
            "total":                              n,
            "risk_counts":                        risk_counts,
            "pattern_counts":                     pattern_counts,
            "severity_counts":                    severity_counts,
            "action_counts":                      action_counts,
            "avg_objection_burden_composite":     round(total_comp / n, 1),
            "systemic_issue_count":               sum(1 for r in self._results if r.has_systemic_issue),
            "coaching_intervention_count":        sum(1 for r in self._results if r.requires_coaching_intervention),
            "avg_price_pressure_score":           round(total_price / n, 1),
            "avg_competition_pressure_score":     round(total_comp_p / n, 1),
            "avg_timing_resistance_score":        round(total_timing / n, 1),
            "avg_skill_gap_score":                round(total_skill / n, 1),
            "total_estimated_lost_revenue_usd":   round(total_rev, 2),
        }
