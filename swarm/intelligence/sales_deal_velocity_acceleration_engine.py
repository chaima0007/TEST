"""
Module 221 — Sales Deal Velocity Acceleration Engine
Detects deals losing momentum in the pipeline and surfaces the friction
causing stalls — stage aging, decision delay, stakeholder freeze, and
champion disengagement — then prescribes velocity-restoration actions.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class VelocityRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class VelocityPattern(str, Enum):
    none                  = "none"
    stage_stall           = "stage_stall"
    decision_paralysis    = "decision_paralysis"
    stakeholder_freeze    = "stakeholder_freeze"
    champion_disengagement = "champion_disengagement"
    budget_drift          = "budget_drift"


class VelocitySeverity(str, Enum):
    flowing    = "flowing"
    slowing    = "slowing"
    stalled    = "stalled"
    frozen     = "frozen"


class VelocityAction(str, Enum):
    no_action                    = "no_action"
    velocity_monitoring          = "velocity_monitoring"
    stage_acceleration_call      = "stage_acceleration_call"
    decision_criteria_alignment  = "decision_criteria_alignment"
    stakeholder_mapping_refresh  = "stakeholder_mapping_refresh"
    champion_reactivation        = "champion_reactivation"
    executive_sponsor_bridge     = "executive_sponsor_bridge"
    mutual_action_plan_reset     = "mutual_action_plan_reset"
    deal_rescue_intervention     = "deal_rescue_intervention"


@dataclass
class VelocityInput:
    deal_id: str
    region: str
    pipeline_stage: str
    # Stage momentum signals
    days_in_current_stage: int              # days since last stage progression
    expected_stage_duration_days: int       # benchmark days for this stage
    stage_regression_count: int            # times deal has moved backward
    last_activity_days_ago: int            # days since any rep activity on deal
    # Decision signals
    decision_date_pushed_count: int        # times close date has been pushed
    decision_criteria_agreed: float        # 0-1 (1 = criteria fully agreed)
    procurement_engaged: float             # 0-1 (1 = procurement fully engaged)
    legal_review_started: float            # 0-1 (1 = legal review underway)
    # Stakeholder signals
    stakeholder_response_rate_pct: float   # % of outreach stakeholders respond to
    active_stakeholder_count: int          # stakeholders active in last 14 days
    economic_buyer_engaged: float          # 0-1 (1 = economic buyer engaged)
    multithreading_score: float            # 0-1 (1 = deal well multithreaded)
    # Champion signals
    champion_last_contact_days: int        # days since champion contact
    champion_sentiment_score: float        # 0-1 (1 = very positive)
    champion_internal_advocacy: float      # 0-1 (1 = actively advocating)
    # Budget & timeline
    budget_confirmed: float                # 0-1 (1 = budget confirmed)
    deal_value_usd: float                  # deal value
    days_to_close_target: int             # days until target close date
    win_probability_pct: float            # CRM win probability 0-1


@dataclass
class VelocityResult:
    deal_id: str
    region: str
    pipeline_stage: str
    velocity_risk: str
    velocity_pattern: str
    velocity_severity: str
    recommended_action: str
    stall_score: float
    decision_score: float
    stakeholder_score: float
    champion_score: float
    velocity_composite: float
    has_velocity_gap: bool
    requires_executive_bridge: bool
    estimated_delay_days: int
    velocity_signal: str

    def to_dict(self) -> Dict:
        return {
            "deal_id":                  self.deal_id,
            "region":                   self.region,
            "pipeline_stage":           self.pipeline_stage,
            "velocity_risk":            self.velocity_risk,
            "velocity_pattern":         self.velocity_pattern,
            "velocity_severity":        self.velocity_severity,
            "recommended_action":       self.recommended_action,
            "stall_score":              self.stall_score,
            "decision_score":           self.decision_score,
            "stakeholder_score":        self.stakeholder_score,
            "champion_score":           self.champion_score,
            "velocity_composite":       self.velocity_composite,
            "has_velocity_gap":         self.has_velocity_gap,
            "requires_executive_bridge": self.requires_executive_bridge,
            "estimated_delay_days":     self.estimated_delay_days,
            "velocity_signal":          self.velocity_signal,
        }


class SalesDealVelocityAccelerationEngine:
    def __init__(self) -> None:
        self._results: List[VelocityResult] = []

    def _stall_score(self, i: VelocityInput) -> float:
        s = 0
        age_ratio = i.days_in_current_stage / max(i.expected_stage_duration_days, 1)
        if   age_ratio  >= 2.0: s += 40
        elif age_ratio  >= 1.5: s += 22
        elif age_ratio  >= 1.2: s += 8

        if   i.last_activity_days_ago >= 14: s += 35
        elif i.last_activity_days_ago >= 7:  s += 18
        elif i.last_activity_days_ago >= 4:  s += 6

        if   i.stage_regression_count >= 2:  s += 25
        elif i.stage_regression_count >= 1:  s += 12
        return min(s, 100)

    def _decision_score(self, i: VelocityInput) -> float:
        s = 0
        if   i.decision_date_pushed_count  >= 4:    s += 40
        elif i.decision_date_pushed_count  >= 2:    s += 22
        elif i.decision_date_pushed_count  >= 1:    s += 8

        if   i.decision_criteria_agreed    <= 0.30: s += 35
        elif i.decision_criteria_agreed    <= 0.55: s += 18
        elif i.decision_criteria_agreed    <= 0.75: s += 6

        if   i.procurement_engaged         <= 0.25: s += 25
        elif i.procurement_engaged         <= 0.50: s += 12
        return min(s, 100)

    def _stakeholder_score(self, i: VelocityInput) -> float:
        s = 0
        if   i.stakeholder_response_rate_pct <= 0.20: s += 40
        elif i.stakeholder_response_rate_pct <= 0.40: s += 22
        elif i.stakeholder_response_rate_pct <= 0.60: s += 8

        if   i.economic_buyer_engaged          <= 0.20: s += 35
        elif i.economic_buyer_engaged          <= 0.45: s += 18
        elif i.economic_buyer_engaged          <= 0.65: s += 6

        if   i.multithreading_score            <= 0.25: s += 25
        elif i.multithreading_score            <= 0.50: s += 12
        return min(s, 100)

    def _champion_score(self, i: VelocityInput) -> float:
        s = 0
        if   i.champion_last_contact_days  >= 21:   s += 45
        elif i.champion_last_contact_days  >= 10:   s += 25
        elif i.champion_last_contact_days  >= 5:    s += 10

        if   i.champion_sentiment_score    <= 0.30: s += 30
        elif i.champion_sentiment_score    <= 0.55: s += 15

        if   i.champion_internal_advocacy  <= 0.25: s += 25
        elif i.champion_internal_advocacy  <= 0.50: s += 12
        return min(s, 100)

    def _composite(self, st: float, de: float, sk: float, ch: float) -> float:
        return min(round(st * 0.30 + de * 0.25 + sk * 0.25 + ch * 0.20, 2), 100.0)

    def _risk(self, c: float) -> VelocityRisk:
        if c >= 60: return VelocityRisk.critical
        if c >= 40: return VelocityRisk.high
        if c >= 20: return VelocityRisk.moderate
        return VelocityRisk.low

    def _severity(self, c: float) -> VelocitySeverity:
        if c >= 60: return VelocitySeverity.frozen
        if c >= 40: return VelocitySeverity.stalled
        if c >= 20: return VelocitySeverity.slowing
        return VelocitySeverity.flowing

    def _pattern(self, i: VelocityInput) -> VelocityPattern:
        age_ratio = i.days_in_current_stage / max(i.expected_stage_duration_days, 1)
        if (age_ratio >= 1.8
                and i.last_activity_days_ago >= 10):
            return VelocityPattern.stage_stall
        if (i.decision_date_pushed_count >= 3
                and i.decision_criteria_agreed <= 0.45):
            return VelocityPattern.decision_paralysis
        if (i.stakeholder_response_rate_pct <= 0.30
                and i.economic_buyer_engaged <= 0.35):
            return VelocityPattern.stakeholder_freeze
        if (i.champion_last_contact_days >= 14
                and i.champion_sentiment_score <= 0.45):
            return VelocityPattern.champion_disengagement
        if (i.budget_confirmed <= 0.30
                and i.decision_date_pushed_count >= 2):
            return VelocityPattern.budget_drift
        return VelocityPattern.none

    def _action(self, risk: VelocityRisk, pat: VelocityPattern) -> VelocityAction:
        if risk == VelocityRisk.critical:
            if pat in (VelocityPattern.stakeholder_freeze, VelocityPattern.decision_paralysis):
                return VelocityAction.executive_sponsor_bridge
            return VelocityAction.deal_rescue_intervention
        if risk == VelocityRisk.high:
            if pat == VelocityPattern.stage_stall:             return VelocityAction.stage_acceleration_call
            if pat == VelocityPattern.decision_paralysis:      return VelocityAction.decision_criteria_alignment
            if pat == VelocityPattern.stakeholder_freeze:      return VelocityAction.stakeholder_mapping_refresh
            if pat == VelocityPattern.champion_disengagement:  return VelocityAction.champion_reactivation
            if pat == VelocityPattern.budget_drift:            return VelocityAction.mutual_action_plan_reset
            return VelocityAction.velocity_monitoring
        if risk == VelocityRisk.moderate:
            return VelocityAction.velocity_monitoring
        return VelocityAction.no_action

    def _signal(self, i: VelocityInput, pat: VelocityPattern, comp: float) -> str:
        if comp < 20:
            return "Deal velocity on track — stage progression, decision alignment and stakeholder engagement within healthy benchmarks"
        labels = {
            VelocityPattern.stage_stall:            "Stage stall",
            VelocityPattern.decision_paralysis:     "Decision paralysis",
            VelocityPattern.stakeholder_freeze:     "Stakeholder freeze",
            VelocityPattern.champion_disengagement: "Champion disengagement",
            VelocityPattern.budget_drift:           "Budget drift",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — {i.days_in_current_stage}d in stage — "
            f"{i.decision_date_pushed_count}x close date pushed — "
            f"champion {i.champion_last_contact_days}d ago — "
            f"${round(i.deal_value_usd/1000)}k deal — "
            f"composite {round(comp)}"
        )

    def _has_velocity_gap(self, i: VelocityInput, comp: float) -> bool:
        age_ratio = i.days_in_current_stage / max(i.expected_stage_duration_days, 1)
        return (comp >= 40
                or age_ratio >= 1.5
                or i.decision_date_pushed_count >= 2)

    def _requires_executive_bridge(self, i: VelocityInput, comp: float) -> bool:
        return (comp >= 25
                or i.economic_buyer_engaged <= 0.40
                or i.stakeholder_response_rate_pct <= 0.35)

    def _estimated_delay_days(self, i: VelocityInput, comp: float) -> int:
        base = i.days_in_current_stage - i.expected_stage_duration_days
        return max(0, round(base * (comp / 100)))

    def assess(self, i: VelocityInput) -> VelocityResult:
        st   = self._stall_score(i)
        de   = self._decision_score(i)
        sk   = self._stakeholder_score(i)
        ch   = self._champion_score(i)
        comp = self._composite(st, de, sk, ch)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = VelocityResult(
            deal_id=i.deal_id,
            region=i.region,
            pipeline_stage=i.pipeline_stage,
            velocity_risk=risk.value,
            velocity_pattern=pat.value,
            velocity_severity=sev.value,
            recommended_action=act.value,
            stall_score=st,
            decision_score=de,
            stakeholder_score=sk,
            champion_score=ch,
            velocity_composite=comp,
            has_velocity_gap=self._has_velocity_gap(i, comp),
            requires_executive_bridge=self._requires_executive_bridge(i, comp),
            estimated_delay_days=self._estimated_delay_days(i, comp),
            velocity_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[VelocityInput]) -> List[VelocityResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_velocity_composite": 0.0,
                "velocity_gap_count": 0,
                "executive_bridge_count": 0,
                "avg_stall_score": 0.0,
                "avg_decision_score": 0.0,
                "avg_stakeholder_score": 0.0,
                "avg_champion_score": 0.0,
                "avg_estimated_delay_days": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tst = tde = tsk = tch = tcomp = tdelay = 0.0
        gc = ec = 0
        for r in self._results:
            rc[r.velocity_risk]      = rc.get(r.velocity_risk, 0)      + 1
            pc[r.velocity_pattern]   = pc.get(r.velocity_pattern, 0)   + 1
            sc[r.velocity_severity]  = sc.get(r.velocity_severity, 0)  + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tst    += r.stall_score
            tde    += r.decision_score
            tsk    += r.stakeholder_score
            tch    += r.champion_score
            tcomp  += r.velocity_composite
            tdelay += r.estimated_delay_days
            if r.has_velocity_gap:          gc += 1
            if r.requires_executive_bridge: ec += 1
        return {
            "total":                   n,
            "risk_counts":             rc,
            "pattern_counts":          pc,
            "severity_counts":         sc,
            "action_counts":           ac,
            "avg_velocity_composite":  round(tcomp / n, 1),
            "velocity_gap_count":      gc,
            "executive_bridge_count":  ec,
            "avg_stall_score":         round(tst / n, 1),
            "avg_decision_score":      round(tde / n, 1),
            "avg_stakeholder_score":   round(tsk / n, 1),
            "avg_champion_score":      round(tch / n, 1),
            "avg_estimated_delay_days": round(tdelay / n, 1),
        }
