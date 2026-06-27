"""
Module 241 — Strategic Risk & Governance Engine
Evaluates strategic health, governance quality, financial exposure,
and resilience across entities to surface board-level risks.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class GovernanceRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class RiskPattern(str, Enum):
    none                = "none"
    market_disruption   = "market_disruption"
    governance_failure  = "governance_failure"
    reputational_crisis = "reputational_crisis"
    financial_exposure  = "financial_exposure"
    strategic_drift     = "strategic_drift"


class GovernanceSeverity(str, Enum):
    sound     = "sound"
    monitored = "monitored"
    exposed   = "exposed"
    crisis    = "crisis"


class GovernanceAction(str, Enum):
    no_action               = "no_action"
    risk_monitoring         = "risk_monitoring"
    governance_review       = "governance_review"
    board_alert             = "board_alert"
    financial_restructuring = "financial_restructuring"
    strategic_pivot         = "strategic_pivot"
    reputational_intervention = "reputational_intervention"
    emergency_governance    = "emergency_governance"
    strategic_transformation = "strategic_transformation"


@dataclass
class GovernanceInput:
    entity_id: str
    entity_type: str                           # company/division/subsidiary/jv
    region: str
    strategic_goal_attainment: float           # 0-1
    market_position_trend: float               # -1 to 1
    competitive_moat_score: float              # 0-1, 1=strong
    board_effectiveness_score: float           # 0-1, 1=highly effective
    executive_alignment_score: float           # 0-1, 1=aligned
    financial_health_score: float              # 0-1, 1=healthy
    esg_compliance_score: float                # 0-1
    reputational_risk_score: float             # 0-1, 1=high risk
    regulatory_relationship_quality: float     # 0-1, 1=excellent
    strategic_initiative_completion_pct: float # 0-1
    stakeholder_trust_score: float             # 0-1, 1=high trust
    market_disruption_exposure: float          # 0-1
    scenario_planning_maturity: float          # 0-1, 1=mature
    risk_appetite_alignment_score: float       # 0-1, 1=aligned
    whistleblower_incident_count: int
    cyber_resilience_score: float              # 0-1, 1=resilient
    succession_plan_completeness: float        # 0-1


@dataclass
class GovernanceResult:
    entity_id: str
    region: str
    governance_risk: str
    risk_pattern: str
    governance_severity: str
    recommended_action: str
    strategic_score: float
    governance_score: float
    financial_risk_score: float
    resilience_score: float
    governance_composite: float
    has_governance_alert: bool
    requires_board_action: bool
    estimated_strategic_risk_index: float
    governance_signal: str

    def to_dict(self) -> Dict:
        return {
            "entity_id":                      self.entity_id,
            "region":                         self.region,
            "governance_risk":                self.governance_risk,
            "risk_pattern":                   self.risk_pattern,
            "governance_severity":            self.governance_severity,
            "recommended_action":             self.recommended_action,
            "strategic_score":                self.strategic_score,
            "governance_score":               self.governance_score,
            "financial_risk_score":           self.financial_risk_score,
            "resilience_score":               self.resilience_score,
            "governance_composite":           self.governance_composite,
            "has_governance_alert":           self.has_governance_alert,
            "requires_board_action":          self.requires_board_action,
            "estimated_strategic_risk_index": self.estimated_strategic_risk_index,
            "governance_signal":              self.governance_signal,
        }


class StrategicRiskGovernanceEngine:
    def __init__(self) -> None:
        self._results: List[GovernanceResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _strategic_score(self, i: GovernanceInput) -> float:
        s = 0
        if   i.strategic_goal_attainment <= 0.40: s += 40
        elif i.strategic_goal_attainment <= 0.60: s += 22
        elif i.strategic_goal_attainment <= 0.75: s += 8

        if   i.market_position_trend <= -0.3: s += 35
        elif i.market_position_trend <= -0.1: s += 18
        elif i.market_position_trend <= 0:    s += 6

        if   i.competitive_moat_score <= 0.30: s += 25
        elif i.competitive_moat_score <= 0.55: s += 12
        return min(s, 100)

    def _governance_score(self, i: GovernanceInput) -> float:
        s = 0
        if   i.board_effectiveness_score <= 0.40: s += 40
        elif i.board_effectiveness_score <= 0.60: s += 22
        elif i.board_effectiveness_score <= 0.75: s += 8

        if   i.executive_alignment_score <= 0.40: s += 35
        elif i.executive_alignment_score <= 0.60: s += 18
        elif i.executive_alignment_score <= 0.75: s += 6

        if   i.whistleblower_incident_count >= 5: s += 25
        elif i.whistleblower_incident_count >= 2: s += 12
        elif i.whistleblower_incident_count >= 1: s += 6
        return min(s, 100)

    def _financial_risk_score(self, i: GovernanceInput) -> float:
        s = 0
        if   i.financial_health_score <= 0.30: s += 40
        elif i.financial_health_score <= 0.55: s += 22
        elif i.financial_health_score <= 0.75: s += 8

        if   i.esg_compliance_score <= 0.40: s += 35
        elif i.esg_compliance_score <= 0.60: s += 18
        elif i.esg_compliance_score <= 0.75: s += 6

        if   i.reputational_risk_score >= 0.70: s += 25
        elif i.reputational_risk_score >= 0.45: s += 12
        elif i.reputational_risk_score >= 0.25: s += 6
        return min(s, 100)

    def _resilience_score(self, i: GovernanceInput) -> float:
        s = 0
        if   i.scenario_planning_maturity <= 0.30: s += 40
        elif i.scenario_planning_maturity <= 0.55: s += 22
        elif i.scenario_planning_maturity <= 0.70: s += 8

        if   i.cyber_resilience_score <= 0.30: s += 35
        elif i.cyber_resilience_score <= 0.55: s += 18
        elif i.cyber_resilience_score <= 0.70: s += 6

        if   i.succession_plan_completeness <= 0.30: s += 25
        elif i.succession_plan_completeness <= 0.55: s += 12
        return min(s, 100)

    def _composite(self, st: float, gov: float, fin: float, res: float) -> float:
        return min(round(st * 0.30 + gov * 0.25 + fin * 0.25 + res * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> GovernanceRisk:
        if c >= 60: return GovernanceRisk.critical
        if c >= 40: return GovernanceRisk.high
        if c >= 20: return GovernanceRisk.moderate
        return GovernanceRisk.low

    def _severity(self, c: float) -> GovernanceSeverity:
        if c >= 60: return GovernanceSeverity.crisis
        if c >= 40: return GovernanceSeverity.exposed
        if c >= 20: return GovernanceSeverity.monitored
        return GovernanceSeverity.sound

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: GovernanceInput) -> RiskPattern:
        if (i.board_effectiveness_score <= 0.35
                or i.executive_alignment_score <= 0.35
                or i.whistleblower_incident_count >= 3):
            return RiskPattern.governance_failure
        if (i.market_disruption_exposure >= 0.65
                or i.market_position_trend <= -0.25):
            return RiskPattern.market_disruption
        if (i.financial_health_score <= 0.35
                or i.esg_compliance_score <= 0.35):
            return RiskPattern.financial_exposure
        if (i.reputational_risk_score >= 0.70
                or i.stakeholder_trust_score <= 0.30):
            return RiskPattern.reputational_crisis
        if (i.strategic_goal_attainment <= 0.40
                or i.strategic_initiative_completion_pct <= 0.35):
            return RiskPattern.strategic_drift
        return RiskPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: GovernanceRisk, pat: RiskPattern) -> GovernanceAction:
        if risk == GovernanceRisk.critical:
            if pat == RiskPattern.governance_failure:  return GovernanceAction.emergency_governance
            if pat == RiskPattern.reputational_crisis: return GovernanceAction.reputational_intervention
            if pat == RiskPattern.financial_exposure:  return GovernanceAction.financial_restructuring
            return GovernanceAction.strategic_transformation
        if risk == GovernanceRisk.high:
            if pat == RiskPattern.governance_failure:  return GovernanceAction.board_alert
            if pat == RiskPattern.market_disruption:   return GovernanceAction.strategic_pivot
            if pat == RiskPattern.financial_exposure:  return GovernanceAction.governance_review
            if pat == RiskPattern.strategic_drift:     return GovernanceAction.board_alert
            return GovernanceAction.risk_monitoring
        if risk == GovernanceRisk.moderate:
            return GovernanceAction.risk_monitoring
        return GovernanceAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived booleans & indices                                          #
    # ------------------------------------------------------------------ #

    def _has_alert(self, i: GovernanceInput, comp: float) -> bool:
        return (comp >= 40
                or i.board_effectiveness_score <= 0.40
                or i.reputational_risk_score >= 0.65
                or i.financial_health_score <= 0.40)

    def _requires_board(self, i: GovernanceInput, comp: float) -> bool:
        return (comp >= 25
                or i.whistleblower_incident_count >= 2
                or i.market_disruption_exposure >= 0.60
                or i.strategic_goal_attainment <= 0.40)

    def _risk_index(self, i: GovernanceInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.risk_appetite_alignment_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: GovernanceInput, pat: RiskPattern, comp: float) -> str:
        if comp < 20:
            return "Gouvernance solide — stratégie claire, finances saines, conseil efficace, risques maîtrisés"
        labels = {
            RiskPattern.market_disruption:   "Disruption marché",
            RiskPattern.governance_failure:  "Défaillance gouvernance",
            RiskPattern.reputational_crisis: "Crise réputationnelle",
            RiskPattern.financial_exposure:  "Exposition financière",
            RiskPattern.strategic_drift:     "Dérive stratégique",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — atteinte stratégique {i.strategic_goal_attainment * 100:.0f}%"
            f" — santé financière {i.financial_health_score * 100:.0f}%"
            f" — réputation {i.reputational_risk_score * 100:.0f}%"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: GovernanceInput) -> GovernanceResult:
        st   = self._strategic_score(i)
        gov  = self._governance_score(i)
        fin  = self._financial_risk_score(i)
        res  = self._resilience_score(i)
        comp = self._composite(st, gov, fin, res)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = GovernanceResult(
            entity_id=i.entity_id,
            region=i.region,
            governance_risk=risk.value,
            risk_pattern=pat.value,
            governance_severity=sev.value,
            recommended_action=act.value,
            strategic_score=st,
            governance_score=gov,
            financial_risk_score=fin,
            resilience_score=res,
            governance_composite=comp,
            has_governance_alert=self._has_alert(i, comp),
            requires_board_action=self._requires_board(i, comp),
            estimated_strategic_risk_index=self._risk_index(i, comp),
            governance_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[GovernanceInput]) -> List[GovernanceResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_governance_composite": 0.0,
                "governance_alert_count": 0,
                "board_action_count": 0,
                "avg_strategic_score": 0.0,
                "avg_governance_score": 0.0,
                "avg_financial_risk_score": 0.0,
                "avg_resilience_score": 0.0,
                "avg_estimated_strategic_risk_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tst = tgov = tfin = tres = tcomp = tridx = 0.0
        alert_count = board_count = 0
        for r in self._results:
            rc[r.governance_risk]     = rc.get(r.governance_risk, 0)     + 1
            pc[r.risk_pattern]        = pc.get(r.risk_pattern, 0)        + 1
            sc[r.governance_severity] = sc.get(r.governance_severity, 0) + 1
            ac[r.recommended_action]  = ac.get(r.recommended_action, 0)  + 1
            tst   += r.strategic_score
            tgov  += r.governance_score
            tfin  += r.financial_risk_score
            tres  += r.resilience_score
            tcomp += r.governance_composite
            tridx += r.estimated_strategic_risk_index
            if r.has_governance_alert:  alert_count += 1
            if r.requires_board_action: board_count += 1
        return {
            "total":                              n,
            "risk_counts":                        rc,
            "pattern_counts":                     pc,
            "severity_counts":                    sc,
            "action_counts":                      ac,
            "avg_governance_composite":           round(tcomp / n, 1),
            "governance_alert_count":             alert_count,
            "board_action_count":                 board_count,
            "avg_strategic_score":                round(tst / n, 1),
            "avg_governance_score":               round(tgov / n, 1),
            "avg_financial_risk_score":           round(tfin / n, 1),
            "avg_resilience_score":               round(tres / n, 1),
            "avg_estimated_strategic_risk_index": round(tridx / n, 2),
        }
