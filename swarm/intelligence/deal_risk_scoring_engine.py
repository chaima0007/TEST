"""
Deal Risk Scoring Engine

Évalue le risque de chaque deal en pipeline : probabilité de slip, de loss,
ou de ghosting, basée sur des signaux comportementaux et contextuels.
"""

from __future__ import annotations

from dataclasses import dataclass, fields as dc_fields
from enum import Enum
from typing import Optional


class DealRisk(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


class DealRiskPattern(str, Enum):
    none = "none"
    ghost_risk = "ghost_risk"
    slip_risk = "slip_risk"
    competitive_loss_risk = "competitive_loss_risk"
    budget_freeze_risk = "budget_freeze_risk"
    champion_attrition_risk = "champion_attrition_risk"
    no_decision_risk = "no_decision_risk"


class DealRiskSeverity(str, Enum):
    healthy = "healthy"
    watchlist = "watchlist"
    at_risk = "at_risk"
    critical = "critical"


class DealRiskAction(str, Enum):
    maintain = "maintain"
    re_engage = "re_engage"
    accelerate_close = "accelerate_close"
    competitive_defense = "competitive_defense"
    executive_escalation = "executive_escalation"
    budget_requalify = "budget_requalify"


@dataclass
class DealRiskInput:
    deal_value: float = 50000.0
    deal_stage: int = 3
    days_in_current_stage: float = 18.0
    avg_days_in_stage_benchmark: float = 15.0
    days_since_last_contact: float = 8.0
    last_contact_was_outbound: bool = False
    competitor_mentioned: bool = False
    num_competitors_mentioned: int = 0
    budget_confirmed: bool = True
    budget_at_risk: bool = False
    champion_active: bool = True
    champion_seniority: int = 2
    executive_engaged: bool = True
    close_date_slipped_count: int = 1
    close_date_days_remaining: float = 25.0
    mutual_close_plan: bool = False
    next_step_defined: bool = True
    stakeholder_count: int = 3
    last_meeting_outcome: str = "positive"
    multi_threaded: bool = True
    internal_priority_score: float = 70.0
    days_in_pipeline_total: float = 45.0


@dataclass
class DealRiskResult:
    composite_score: float
    risk: DealRisk
    pattern: DealRiskPattern
    severity: DealRiskSeverity
    action: DealRiskAction
    engagement_score: float
    relationship_strength_score: float
    process_health_score: float
    competitive_exposure_score: float
    slip_probability_pct: float
    ghost_probability_pct: float
    days_overdue_in_stage: float
    signal: str
    recommended_next_step: str
    revenue_at_risk: float

    def to_dict(self) -> dict:
        return {
            "composite_score": self.composite_score,
            "risk": self.risk.value,
            "pattern": self.pattern.value,
            "severity": self.severity.value,
            "action": self.action.value,
            "engagement_score": self.engagement_score,
            "relationship_strength_score": self.relationship_strength_score,
            "process_health_score": self.process_health_score,
            "competitive_exposure_score": self.competitive_exposure_score,
            "slip_probability_pct": self.slip_probability_pct,
            "ghost_probability_pct": self.ghost_probability_pct,
            "days_overdue_in_stage": self.days_overdue_in_stage,
            "signal": self.signal,
            "recommended_next_step": self.recommended_next_step,
            "revenue_at_risk": self.revenue_at_risk,
        }


class DealRiskScoringEngine:

    def _engagement_score(self, inp: DealRiskInput) -> float:
        recency_score = max(0, 100 - inp.days_since_last_contact * 4)
        inbound_bonus = 15 if not inp.last_contact_was_outbound else 0
        meeting_bonus = {"positive": 20, "neutral": 5, "negative": -10}.get(inp.last_meeting_outcome, 0)
        raw = recency_score + inbound_bonus + meeting_bonus
        return min(max(round(raw, 1), 0.0), 100.0)

    def _relationship_strength_score(self, inp: DealRiskInput) -> float:
        champion_score = (inp.champion_seniority / 3 * 40) if inp.champion_active else 0
        exec_score = 30 if inp.executive_engaged else 0
        multi_thread_score = 20 if inp.multi_threaded else 0
        stakeholder_score = min(inp.stakeholder_count / 4 * 10, 10)
        raw = champion_score + exec_score + multi_thread_score + stakeholder_score
        return min(max(round(raw, 1), 0.0), 100.0)

    def _process_health_score(self, inp: DealRiskInput) -> float:
        next_step_score = 30 if inp.next_step_defined else 0
        close_plan_score = 25 if inp.mutual_close_plan else 0
        slip_penalty = min(inp.close_date_slipped_count * 15, 40)
        stage_overdue = max(0, inp.days_in_current_stage - inp.avg_days_in_stage_benchmark)
        overdue_penalty = min(stage_overdue / max(inp.avg_days_in_stage_benchmark, 1) * 20, 20)
        raw = 70 + next_step_score + close_plan_score - slip_penalty - overdue_penalty
        return min(max(round(raw, 1), 0.0), 100.0)

    def _competitive_exposure_score(self, inp: DealRiskInput) -> float:
        if not inp.competitor_mentioned:
            return 90.0
        competitor_penalty = min(inp.num_competitors_mentioned * 20, 60)
        raw = 90 - competitor_penalty
        return min(max(round(raw, 1), 0.0), 100.0)

    def _composite(self, e: float, r: float, p: float, c: float) -> float:
        return min(round(e * 0.25 + r * 0.30 + p * 0.30 + c * 0.15, 1), 100.0)

    def _risk_level(self, score: float) -> DealRisk:
        if score >= 70:
            return DealRisk.low
        if score >= 50:
            return DealRisk.moderate
        if score >= 30:
            return DealRisk.high
        return DealRisk.critical

    def _severity(self, risk: DealRisk) -> DealRiskSeverity:
        return {
            DealRisk.low: DealRiskSeverity.healthy,
            DealRisk.moderate: DealRiskSeverity.watchlist,
            DealRisk.high: DealRiskSeverity.at_risk,
            DealRisk.critical: DealRiskSeverity.critical,
        }[risk]

    def _detect_pattern(self, inp: DealRiskInput, e: float, r: float) -> DealRiskPattern:
        if inp.days_since_last_contact > 14 and inp.last_contact_was_outbound:
            return DealRiskPattern.ghost_risk
        if inp.close_date_slipped_count >= 2 or inp.days_in_current_stage > inp.avg_days_in_stage_benchmark * 2:
            return DealRiskPattern.slip_risk
        if inp.competitor_mentioned and inp.num_competitors_mentioned >= 2:
            return DealRiskPattern.competitive_loss_risk
        if inp.budget_at_risk or not inp.budget_confirmed:
            return DealRiskPattern.budget_freeze_risk
        if not inp.champion_active:
            return DealRiskPattern.champion_attrition_risk
        if not inp.next_step_defined and not inp.mutual_close_plan:
            return DealRiskPattern.no_decision_risk
        return DealRiskPattern.none

    def _action(self, pattern: DealRiskPattern) -> DealRiskAction:
        mapping = {
            DealRiskPattern.ghost_risk: DealRiskAction.re_engage,
            DealRiskPattern.slip_risk: DealRiskAction.accelerate_close,
            DealRiskPattern.competitive_loss_risk: DealRiskAction.competitive_defense,
            DealRiskPattern.budget_freeze_risk: DealRiskAction.budget_requalify,
            DealRiskPattern.champion_attrition_risk: DealRiskAction.executive_escalation,
            DealRiskPattern.no_decision_risk: DealRiskAction.accelerate_close,
            DealRiskPattern.none: DealRiskAction.maintain,
        }
        return mapping[pattern]

    def _slip_probability(self, inp: DealRiskInput) -> float:
        base = 10.0
        if inp.close_date_slipped_count >= 2:
            base += 30
        elif inp.close_date_slipped_count == 1:
            base += 15
        if inp.days_in_current_stage > inp.avg_days_in_stage_benchmark * 1.5:
            base += 20
        if not inp.mutual_close_plan:
            base += 10
        if inp.close_date_days_remaining < 7:
            base += 15
        return min(base, 95.0)

    def _ghost_probability(self, inp: DealRiskInput) -> float:
        base = 5.0
        if inp.days_since_last_contact > 21:
            base += 40
        elif inp.days_since_last_contact > 14:
            base += 20
        if inp.last_contact_was_outbound and inp.days_since_last_contact > 10:
            base += 20
        if not inp.champion_active:
            base += 15
        return min(base, 95.0)

    def _recommended_next_step(self, action: DealRiskAction, inp: DealRiskInput) -> str:
        steps = {
            DealRiskAction.re_engage: "Send personalized re-engagement email with new value trigger within 24h",
            DealRiskAction.accelerate_close: "Create mutual close plan with champion and get executive sign-off on timeline",
            DealRiskAction.competitive_defense: "Share competitive battlecard with champion and request evaluation criteria",
            DealRiskAction.executive_escalation: "Identify new champion or escalate to executive contact immediately",
            DealRiskAction.budget_requalify: "Schedule budget requalification call with economic buyer",
            DealRiskAction.maintain: "Continue cadence — schedule next meeting within 7 days",
        }
        return steps.get(action, "Review deal status and define clear next step")

    def _signal(self, risk: DealRisk, pattern: DealRiskPattern, score: float) -> str:
        if risk == DealRisk.low and pattern == DealRiskPattern.none:
            return f"Deal healthy — engagement, relationships and process on track (score: {score:.0f})"
        signals = {
            DealRiskPattern.ghost_risk: "Ghost risk detected — prospect unresponsive to outbound for >14 days",
            DealRiskPattern.slip_risk: "Slip risk high — close date slipped multiple times or stage overdue",
            DealRiskPattern.competitive_loss_risk: "Multiple competitors active — deal at high competitive displacement risk",
            DealRiskPattern.budget_freeze_risk: "Budget not confirmed or at risk — requalification required immediately",
            DealRiskPattern.champion_attrition_risk: "Champion no longer active — deal lost internal advocacy",
            DealRiskPattern.no_decision_risk: "No next step or close plan — no-decision outcome likely",
            DealRiskPattern.none: f"Deal {risk.value} risk (score: {score:.0f}) — monitor engagement signals",
        }
        return signals.get(pattern, "Deal requires attention")

    def assess(self, inp: DealRiskInput) -> DealRiskResult:
        e = self._engagement_score(inp)
        r = self._relationship_strength_score(inp)
        p = self._process_health_score(inp)
        c = self._competitive_exposure_score(inp)
        composite = self._composite(e, r, p, c)
        risk = self._risk_level(composite)
        severity = self._severity(risk)
        pattern = self._detect_pattern(inp, e, r)
        action = self._action(pattern)

        days_overdue = max(0.0, inp.days_in_current_stage - inp.avg_days_in_stage_benchmark)

        return DealRiskResult(
            composite_score=composite,
            risk=risk,
            pattern=pattern,
            severity=severity,
            action=action,
            engagement_score=e,
            relationship_strength_score=r,
            process_health_score=p,
            competitive_exposure_score=c,
            slip_probability_pct=self._slip_probability(inp),
            ghost_probability_pct=self._ghost_probability(inp),
            days_overdue_in_stage=round(days_overdue, 1),
            signal=self._signal(risk, pattern, composite),
            recommended_next_step=self._recommended_next_step(action, inp),
            revenue_at_risk=round(inp.deal_value * (1 - composite / 100), 2),
        )

    def batch(self, inputs: list[DealRiskInput]) -> list[DealRiskResult]:
        return [self.assess(inp) for inp in inputs]

    def summary(self, results: list[DealRiskResult]) -> dict:
        if not results:
            return {}
        scores = [r.composite_score for r in results]
        return {
            "total_deals": len(results),
            "avg_composite_score": round(sum(scores) / len(scores), 1),
            "critical_count": sum(1 for r in results if r.risk == DealRisk.critical),
            "high_risk_count": sum(1 for r in results if r.risk == DealRisk.high),
            "top_pattern": max(set(r.pattern.value for r in results), key=lambda p: sum(1 for r in results if r.pattern.value == p)),
            "total_revenue_at_risk": round(sum(r.revenue_at_risk for r in results), 2),
            "avg_slip_probability": round(sum(r.slip_probability_pct for r in results) / len(results), 1),
            "avg_ghost_probability": round(sum(r.ghost_probability_pct for r in results) / len(results), 1),
            "ghost_risk_count": sum(1 for r in results if r.pattern == DealRiskPattern.ghost_risk),
            "slip_risk_count": sum(1 for r in results if r.pattern == DealRiskPattern.slip_risk),
            "min_score": min(scores),
            "max_score": max(scores),
            "low_risk_pct": round(sum(1 for r in results if r.risk == DealRisk.low) / len(results) * 100, 1),
        }
