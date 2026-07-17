from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ObjectionRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ObjectionPattern(str, Enum):
    none                                  = "none"
    price_objection_paralysis             = "price_objection_paralysis"
    technical_objection_avoidance         = "technical_objection_avoidance"
    trust_objection_gap                   = "trust_objection_gap"
    competition_capitulation_under_objection = "competition_capitulation_under_objection"
    late_stage_objection_surprise         = "late_stage_objection_surprise"


class ObjectionSeverity(str, Enum):
    confident  = "confident"
    developing = "developing"
    reactive   = "reactive"
    paralyzed  = "paralyzed"


class ObjectionAction(str, Enum):
    no_action                       = "no_action"
    objection_handling_workshop     = "objection_handling_workshop"
    price_reframing_training        = "price_reframing_training"
    technical_proof_support         = "technical_proof_support"
    trust_building_coaching         = "trust_building_coaching"
    competitive_intelligence_training = "competitive_intelligence_training"


@dataclass
class ObjectionInput:
    rep_id: str
    region: str
    evaluation_period_id: str
    total_objections_logged: int
    objections_resolved_pct: float
    price_objection_rate_pct: float
    price_objection_resolution_rate_pct: float
    technical_objection_rate_pct: float
    technical_objection_escalation_rate_pct: float
    trust_objection_rate_pct: float
    competitive_objection_rate_pct: float
    competitive_objection_loss_rate_pct: float
    late_stage_new_objection_rate_pct: float
    avg_days_to_resolve_objection: float
    objection_repeat_rate_pct: float
    objection_documented_in_crm_pct: float
    champion_coached_on_internal_objections_pct: float
    multi_objection_deal_rate_pct: float
    deals_lost_to_unresolved_objection_pct: float
    avg_objection_response_time_hours: float
    proactive_objection_prevention_rate_pct: float
    avg_opportunity_value_usd: float


@dataclass
class ObjectionResult:
    rep_id: str
    region: str
    objection_risk: ObjectionRisk
    objection_pattern: ObjectionPattern
    objection_severity: ObjectionSeverity
    recommended_action: ObjectionAction
    objection_resolution_score: float
    objection_preparation_score: float
    objection_response_score: float
    competitive_handling_score: float
    objection_composite: float
    has_objection_gap: bool
    requires_objection_coaching: bool
    estimated_deal_loss_usd: float
    objection_signal: str

    def to_dict(self) -> dict:
        return {
            "rep_id":                           self.rep_id,
            "region":                           self.region,
            "objection_risk":                   self.objection_risk.value,
            "objection_pattern":                self.objection_pattern.value,
            "objection_severity":               self.objection_severity.value,
            "recommended_action":               self.recommended_action.value,
            "objection_resolution_score":       self.objection_resolution_score,
            "objection_preparation_score":      self.objection_preparation_score,
            "objection_response_score":         self.objection_response_score,
            "competitive_handling_score":       self.competitive_handling_score,
            "objection_composite":              self.objection_composite,
            "has_objection_gap":                self.has_objection_gap,
            "requires_objection_coaching":      self.requires_objection_coaching,
            "estimated_deal_loss_usd":          self.estimated_deal_loss_usd,
            "objection_signal":                 self.objection_signal,
        }


class SalesObjectionIntelligenceEngine:

    def __init__(self) -> None:
        self._results: list[ObjectionResult] = []

    # ------------------------------------------------------------------
    # Sub-scores (0–100, higher = more risk)
    # ------------------------------------------------------------------

    def _objection_resolution_score(self, inp: ObjectionInput) -> float:
        score = 0.0

        if inp.objections_resolved_pct <= 0.30:
            score += 40.0
        elif inp.objections_resolved_pct <= 0.60:
            score += 22.0
        elif inp.objections_resolved_pct <= 0.80:
            score += 8.0

        if inp.avg_days_to_resolve_objection >= 14.0:
            score += 35.0
        elif inp.avg_days_to_resolve_objection >= 7.0:
            score += 18.0

        if inp.deals_lost_to_unresolved_objection_pct >= 0.30:
            score += 25.0
        elif inp.deals_lost_to_unresolved_objection_pct >= 0.15:
            score += 12.0

        return min(score, 100.0)

    def _objection_preparation_score(self, inp: ObjectionInput) -> float:
        score = 0.0

        if inp.objection_repeat_rate_pct >= 0.60:
            score += 40.0
        elif inp.objection_repeat_rate_pct >= 0.35:
            score += 22.0
        elif inp.objection_repeat_rate_pct >= 0.20:
            score += 8.0

        if inp.objection_documented_in_crm_pct <= 0.20:
            score += 35.0
        elif inp.objection_documented_in_crm_pct <= 0.50:
            score += 18.0

        if inp.proactive_objection_prevention_rate_pct <= 0.10:
            score += 25.0
        elif inp.proactive_objection_prevention_rate_pct <= 0.30:
            score += 12.0

        return min(score, 100.0)

    def _objection_response_score(self, inp: ObjectionInput) -> float:
        score = 0.0

        if inp.avg_objection_response_time_hours >= 48.0:
            score += 40.0
        elif inp.avg_objection_response_time_hours >= 24.0:
            score += 22.0
        elif inp.avg_objection_response_time_hours >= 8.0:
            score += 8.0

        if inp.late_stage_new_objection_rate_pct >= 0.50:
            score += 35.0
        elif inp.late_stage_new_objection_rate_pct >= 0.25:
            score += 18.0

        if inp.champion_coached_on_internal_objections_pct <= 0.15:
            score += 25.0
        elif inp.champion_coached_on_internal_objections_pct <= 0.40:
            score += 12.0

        return min(score, 100.0)

    def _competitive_handling_score(self, inp: ObjectionInput) -> float:
        score = 0.0

        if inp.competitive_objection_loss_rate_pct >= 0.60:
            score += 45.0
        elif inp.competitive_objection_loss_rate_pct >= 0.35:
            score += 25.0
        elif inp.competitive_objection_loss_rate_pct >= 0.20:
            score += 10.0

        if inp.price_objection_resolution_rate_pct <= 0.20:
            score += 30.0
        elif inp.price_objection_resolution_rate_pct <= 0.50:
            score += 15.0

        if inp.trust_objection_rate_pct >= 0.40:
            score += 25.0
        elif inp.trust_objection_rate_pct >= 0.20:
            score += 12.0

        return min(score, 100.0)

    # ------------------------------------------------------------------
    # Pattern detection
    # ------------------------------------------------------------------

    def _detect_pattern(self, inp: ObjectionInput,
                          resolution: float, preparation: float,
                          response: float, competitive: float) -> ObjectionPattern:
        if competitive >= 30 and inp.price_objection_resolution_rate_pct <= 0.30:
            return ObjectionPattern.price_objection_paralysis

        if resolution >= 30 and inp.technical_objection_escalation_rate_pct >= 0.60:
            return ObjectionPattern.technical_objection_avoidance

        if preparation >= 30 and inp.trust_objection_rate_pct >= 0.40:
            return ObjectionPattern.trust_objection_gap

        if competitive >= 40 and inp.competitive_objection_loss_rate_pct >= 0.50:
            return ObjectionPattern.competition_capitulation_under_objection

        if response >= 30 and inp.late_stage_new_objection_rate_pct >= 0.35:
            return ObjectionPattern.late_stage_objection_surprise

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
            return ObjectionSeverity.paralyzed
        if composite >= 40:
            return ObjectionSeverity.reactive
        if composite >= 20:
            return ObjectionSeverity.developing
        return ObjectionSeverity.confident

    def _action(self, risk: ObjectionRisk,
                 pattern: ObjectionPattern) -> ObjectionAction:
        if risk == ObjectionRisk.critical:
            if pattern == ObjectionPattern.technical_objection_avoidance:
                return ObjectionAction.technical_proof_support
            if pattern == ObjectionPattern.trust_objection_gap:
                return ObjectionAction.trust_building_coaching
            return ObjectionAction.objection_handling_workshop
        if risk == ObjectionRisk.high:
            if pattern == ObjectionPattern.price_objection_paralysis:
                return ObjectionAction.price_reframing_training
            if pattern == ObjectionPattern.competition_capitulation_under_objection:
                return ObjectionAction.competitive_intelligence_training
            return ObjectionAction.objection_handling_workshop
        if risk == ObjectionRisk.moderate:
            return ObjectionAction.objection_handling_workshop
        return ObjectionAction.no_action

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    def _has_objection_gap(self, composite: float, inp: ObjectionInput) -> bool:
        return (
            composite >= 40
            or inp.deals_lost_to_unresolved_objection_pct >= 0.25
            or inp.competitive_objection_loss_rate_pct >= 0.50
        )

    def _requires_objection_coaching(self, composite: float, inp: ObjectionInput) -> bool:
        return (
            composite >= 30
            or inp.objections_resolved_pct <= 0.50
            or inp.objection_repeat_rate_pct >= 0.40
        )

    # ------------------------------------------------------------------
    # Deal loss estimate
    # ------------------------------------------------------------------

    def _estimated_deal_loss(self, inp: ObjectionInput, composite: float) -> float:
        return round(
            inp.total_objections_logged
            * inp.deals_lost_to_unresolved_objection_pct
            * inp.avg_opportunity_value_usd
            * (composite / 100.0),
            2,
        )

    # ------------------------------------------------------------------
    # Signal string
    # ------------------------------------------------------------------

    def _signal(self, inp: ObjectionInput,
                 pattern: ObjectionPattern, composite: float) -> str:
        if pattern == ObjectionPattern.none and composite < 20:
            return "Objection handling healthy — resolution rate, preparation, and competitive handling within benchmarks"
        parts: list[str] = []
        if inp.objections_resolved_pct < 1.0:
            parts.append(f"{inp.objections_resolved_pct*100:.0f}% objections resolved")
        if inp.competitive_objection_loss_rate_pct < 1.0:
            parts.append(f"{inp.competitive_objection_loss_rate_pct*100:.0f}% competitive losses")
        parts.append(f"{inp.avg_days_to_resolve_objection:.0f} avg days to resolve")
        label = pattern.value.replace("_", " ") if pattern != ObjectionPattern.none else "Objection risk"
        summary = " — ".join(parts) if parts else "objection handling gap"
        return f"{label.capitalize()} — {summary} — composite {composite:.0f}"

    # ------------------------------------------------------------------
    # Assess
    # ------------------------------------------------------------------

    def assess(self, inp: ObjectionInput) -> ObjectionResult:
        resolution    = round(self._objection_resolution_score(inp), 1)
        preparation   = round(self._objection_preparation_score(inp), 1)
        response      = round(self._objection_response_score(inp), 1)
        competitive   = round(self._competitive_handling_score(inp), 1)

        composite = round(
            resolution * 0.35 + preparation * 0.25 + response * 0.25 + competitive * 0.15, 1
        )
        composite = min(composite, 100.0)

        pattern  = self._detect_pattern(inp, resolution, preparation, response, competitive)
        risk     = self._risk_level(composite)
        severity = self._severity(composite)
        action   = self._action(risk, pattern)

        gap    = self._has_objection_gap(composite, inp)
        coach  = self._requires_objection_coaching(composite, inp)
        loss   = self._estimated_deal_loss(inp, composite)
        signal = self._signal(inp, pattern, composite)

        result = ObjectionResult(
            rep_id=inp.rep_id,
            region=inp.region,
            objection_risk=risk,
            objection_pattern=pattern,
            objection_severity=severity,
            recommended_action=action,
            objection_resolution_score=resolution,
            objection_preparation_score=preparation,
            objection_response_score=response,
            competitive_handling_score=competitive,
            objection_composite=composite,
            has_objection_gap=gap,
            requires_objection_coaching=coach,
            estimated_deal_loss_usd=loss,
            objection_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ObjectionInput]) -> list[ObjectionResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_objection_composite": 0.0,
                "objection_gap_count": 0,
                "coaching_count": 0,
                "avg_objection_resolution_score": 0.0,
                "avg_objection_preparation_score": 0.0,
                "avg_objection_response_score": 0.0,
                "avg_competitive_handling_score": 0.0,
                "total_estimated_deal_loss_usd": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp = total_res = total_pre = total_rsp = total_cmp = total_loss = 0.0

        for r in self._results:
            risk_counts[r.objection_risk.value]       = risk_counts.get(r.objection_risk.value, 0) + 1
            pattern_counts[r.objection_pattern.value] = pattern_counts.get(r.objection_pattern.value, 0) + 1
            severity_counts[r.objection_severity.value] = severity_counts.get(r.objection_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.objection_composite
            total_res  += r.objection_resolution_score
            total_pre  += r.objection_preparation_score
            total_rsp  += r.objection_response_score
            total_cmp  += r.competitive_handling_score
            total_loss += r.estimated_deal_loss_usd

        n = len(self._results)

        return {
            "total":                                    n,
            "risk_counts":                              risk_counts,
            "pattern_counts":                           pattern_counts,
            "severity_counts":                          severity_counts,
            "action_counts":                            action_counts,
            "avg_objection_composite":                  round(total_comp / n, 1),
            "objection_gap_count":                      sum(1 for r in self._results if r.has_objection_gap),
            "coaching_count":                           sum(1 for r in self._results if r.requires_objection_coaching),
            "avg_objection_resolution_score":           round(total_res / n, 1),
            "avg_objection_preparation_score":          round(total_pre / n, 1),
            "avg_objection_response_score":             round(total_rsp / n, 1),
            "avg_competitive_handling_score":           round(total_cmp / n, 1),
            "total_estimated_deal_loss_usd":            round(total_loss, 2),
        }
