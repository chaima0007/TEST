"""
Module 230 — PR & Crisis Management Engine
Monitors brand reputation, media escalation, social-media storm risk, regulatory
scrutiny and executive-misconduct signals — then recommends the right crisis
communications response before damage becomes irreversible.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class CrisisRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CrisisPattern(str, Enum):
    none                = "none"
    reputational_attack = "reputational_attack"
    media_escalation    = "media_escalation"
    social_media_storm  = "social_media_storm"
    regulatory_scrutiny = "regulatory_scrutiny"
    executive_misconduct = "executive_misconduct"


class CrisisSeverity(str, Enum):
    nominal   = "nominal"
    elevated  = "elevated"
    crisis    = "crisis"
    emergency = "emergency"


class CrisisAction(str, Enum):
    no_action                  = "no_action"
    media_monitoring           = "media_monitoring"
    proactive_statement        = "proactive_statement"
    stakeholder_briefing       = "stakeholder_briefing"
    crisis_communications_team = "crisis_communications_team"
    legal_hold                 = "legal_hold"
    executive_response         = "executive_response"
    media_blackout             = "media_blackout"
    crisis_war_room            = "crisis_war_room"


@dataclass
class CrisisInput:
    incident_id: str
    brand_entity: str
    region: str
    media_mention_volume_spike_pct: float    # % above baseline
    sentiment_score: float                   # 0-1 (0 = very negative)
    negative_mention_pct: float              # 0-1
    viral_content_risk_score: float          # 0-1
    key_journalist_engagement_count: int
    regulatory_inquiry_count: int
    social_media_engagement_spike_pct: float
    influencer_amplification_score: float    # 0-1
    competitor_exploitation_score: float     # 0-1
    employee_leak_risk_score: float          # 0-1
    executive_mention_negativity: float      # 0-1
    legal_exposure_score: float              # 0-1
    crisis_response_time_hours: float
    media_coverage_reach_millions: float
    public_trust_index: float                # 0-1 (1 = trusted)
    crisis_team_readiness_score: float       # 0-1
    prior_crisis_count_12m: int


@dataclass
class CrisisResult:
    incident_id: str
    region: str
    crisis_risk: str
    crisis_pattern: str
    crisis_severity: str
    recommended_action: str
    media_score: float
    social_score: float
    legal_score: float
    reputation_score: float
    crisis_composite: float
    has_active_crisis: bool
    requires_executive_response: bool
    estimated_reputation_damage_score: float
    crisis_signal: str

    def to_dict(self) -> Dict:
        return {
            "incident_id":                        self.incident_id,
            "region":                             self.region,
            "crisis_risk":                        self.crisis_risk,
            "crisis_pattern":                     self.crisis_pattern,
            "crisis_severity":                    self.crisis_severity,
            "recommended_action":                 self.recommended_action,
            "media_score":                        self.media_score,
            "social_score":                       self.social_score,
            "legal_score":                        self.legal_score,
            "reputation_score":                   self.reputation_score,
            "crisis_composite":                   self.crisis_composite,
            "has_active_crisis":                  self.has_active_crisis,
            "requires_executive_response":        self.requires_executive_response,
            "estimated_reputation_damage_score":  self.estimated_reputation_damage_score,
            "crisis_signal":                      self.crisis_signal,
        }


class PRCrisisManagementEngine:
    def __init__(self) -> None:
        self._results: List[CrisisResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _media_score(self, i: CrisisInput) -> float:
        s = 0
        if   i.media_mention_volume_spike_pct >= 1.50: s += 40
        elif i.media_mention_volume_spike_pct >= 0.75: s += 22
        elif i.media_mention_volume_spike_pct >= 0.30: s += 8

        if   i.key_journalist_engagement_count >= 5: s += 35
        elif i.key_journalist_engagement_count >= 2: s += 18
        elif i.key_journalist_engagement_count >= 1: s += 6

        if   i.media_coverage_reach_millions >= 10: s += 25
        elif i.media_coverage_reach_millions >= 3:  s += 12
        return min(s, 100)

    def _social_score(self, i: CrisisInput) -> float:
        s = 0
        if   i.social_media_engagement_spike_pct >= 2.00: s += 45
        elif i.social_media_engagement_spike_pct >= 1.00: s += 25
        elif i.social_media_engagement_spike_pct >= 0.50: s += 10

        if   i.viral_content_risk_score >= 0.70: s += 30
        elif i.viral_content_risk_score >= 0.45: s += 15

        if   i.influencer_amplification_score >= 0.70: s += 25
        elif i.influencer_amplification_score >= 0.45: s += 12
        return min(s, 100)

    def _legal_score(self, i: CrisisInput) -> float:
        s = 0
        if   i.legal_exposure_score >= 0.70: s += 40
        elif i.legal_exposure_score >= 0.45: s += 22
        elif i.legal_exposure_score >= 0.20: s += 8

        if   i.regulatory_inquiry_count >= 3: s += 35
        elif i.regulatory_inquiry_count >= 1: s += 18

        if   i.employee_leak_risk_score >= 0.60: s += 25
        elif i.employee_leak_risk_score >= 0.35: s += 12
        return min(s, 100)

    def _reputation_score(self, i: CrisisInput) -> float:
        s = 0
        if   i.sentiment_score <= 0.25: s += 40
        elif i.sentiment_score <= 0.45: s += 22
        elif i.sentiment_score <= 0.60: s += 8

        if   i.negative_mention_pct >= 0.60: s += 35
        elif i.negative_mention_pct >= 0.40: s += 18
        elif i.negative_mention_pct >= 0.20: s += 6

        if   i.public_trust_index <= 0.40: s += 25
        elif i.public_trust_index <= 0.60: s += 12
        return min(s, 100)

    def _composite(self, med: float, soc: float, leg: float, rep: float) -> float:
        return min(round(med * 0.30 + soc * 0.25 + leg * 0.25 + rep * 0.20, 2), 100.0)

    def _risk(self, c: float) -> CrisisRisk:
        if c >= 60: return CrisisRisk.critical
        if c >= 40: return CrisisRisk.high
        if c >= 20: return CrisisRisk.moderate
        return CrisisRisk.low

    def _severity(self, c: float) -> CrisisSeverity:
        if c >= 60: return CrisisSeverity.emergency
        if c >= 40: return CrisisSeverity.crisis
        if c >= 20: return CrisisSeverity.elevated
        return CrisisSeverity.nominal

    def _pattern(self, i: CrisisInput) -> CrisisPattern:
        if (i.negative_mention_pct >= 0.50
                and i.competitor_exploitation_score >= 0.50):
            return CrisisPattern.reputational_attack
        if (i.key_journalist_engagement_count >= 4
                and i.media_coverage_reach_millions >= 5):
            return CrisisPattern.media_escalation
        if (i.social_media_engagement_spike_pct >= 1.50
                and i.viral_content_risk_score >= 0.60):
            return CrisisPattern.social_media_storm
        if (i.regulatory_inquiry_count >= 2
                and i.legal_exposure_score >= 0.40):
            return CrisisPattern.regulatory_scrutiny
        if (i.executive_mention_negativity >= 0.60
                and i.employee_leak_risk_score >= 0.40):
            return CrisisPattern.executive_misconduct
        return CrisisPattern.none

    def _action(self, risk: CrisisRisk, pat: CrisisPattern) -> CrisisAction:
        if risk == CrisisRisk.critical:
            if pat in (CrisisPattern.social_media_storm,
                       CrisisPattern.executive_misconduct):
                return CrisisAction.crisis_war_room
            return CrisisAction.executive_response
        if risk == CrisisRisk.high:
            if pat == CrisisPattern.reputational_attack:
                return CrisisAction.crisis_communications_team
            if pat == CrisisPattern.media_escalation:
                return CrisisAction.executive_response
            if pat == CrisisPattern.social_media_storm:
                return CrisisAction.crisis_communications_team
            if pat == CrisisPattern.regulatory_scrutiny:
                return CrisisAction.legal_hold
            if pat == CrisisPattern.executive_misconduct:
                return CrisisAction.executive_response
            return CrisisAction.media_monitoring
        if risk == CrisisRisk.moderate:
            return CrisisAction.proactive_statement
        return CrisisAction.no_action

    def _signal(self, i: CrisisInput, pat: CrisisPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Brand reputation stable — media, social and legal indicators "
                "within normal parameters"
            )
        labels = {
            CrisisPattern.reputational_attack:  "Reputational attack detected",
            CrisisPattern.media_escalation:     "Media escalation in progress",
            CrisisPattern.social_media_storm:   "Social media storm forming",
            CrisisPattern.regulatory_scrutiny:  "Regulatory scrutiny elevated",
            CrisisPattern.executive_misconduct: "Executive misconduct signal",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — "
            f"{round(i.negative_mention_pct * 100)}% negative — "
            f"{round(i.media_coverage_reach_millions, 1)}M reach — "
            f"trust {round(i.public_trust_index * 100)}% — "
            f"composite {round(comp)}"
        )

    def _has_active_crisis(self, i: CrisisInput, comp: float) -> bool:
        return (
            comp >= 40
            or i.negative_mention_pct >= 0.40
            or i.regulatory_inquiry_count >= 1
        )

    def _requires_executive_response(self, i: CrisisInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.legal_exposure_score >= 0.35
            or i.executive_mention_negativity >= 0.40
        )

    def _reputation_damage_score(self, i: CrisisInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.public_trust_index + 0.01) * 10, 10.0), 2)

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, i: CrisisInput) -> CrisisResult:
        med  = self._media_score(i)
        soc  = self._social_score(i)
        leg  = self._legal_score(i)
        rep  = self._reputation_score(i)
        comp = self._composite(med, soc, leg, rep)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = CrisisResult(
            incident_id=i.incident_id,
            region=i.region,
            crisis_risk=risk.value,
            crisis_pattern=pat.value,
            crisis_severity=sev.value,
            recommended_action=act.value,
            media_score=med,
            social_score=soc,
            legal_score=leg,
            reputation_score=rep,
            crisis_composite=comp,
            has_active_crisis=self._has_active_crisis(i, comp),
            requires_executive_response=self._requires_executive_response(i, comp),
            estimated_reputation_damage_score=self._reputation_damage_score(i, comp),
            crisis_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[CrisisInput]) -> List[CrisisResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_crisis_composite": 0.0,
                "active_crisis_count": 0,
                "executive_response_count": 0,
                "avg_media_score": 0.0,
                "avg_social_score": 0.0,
                "avg_legal_score": 0.0,
                "avg_reputation_score": 0.0,
                "avg_estimated_reputation_damage_score": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tmed = tsoc = tleg = trep = tcomp = tdmg = 0.0
        acc = erc = 0
        for r in self._results:
            rc[r.crisis_risk]          = rc.get(r.crisis_risk, 0)          + 1
            pc[r.crisis_pattern]       = pc.get(r.crisis_pattern, 0)       + 1
            sc[r.crisis_severity]      = sc.get(r.crisis_severity, 0)      + 1
            ac[r.recommended_action]   = ac.get(r.recommended_action, 0)   + 1
            tmed  += r.media_score
            tsoc  += r.social_score
            tleg  += r.legal_score
            trep  += r.reputation_score
            tcomp += r.crisis_composite
            tdmg  += r.estimated_reputation_damage_score
            if r.has_active_crisis:           acc += 1
            if r.requires_executive_response: erc += 1
        return {
            "total":                                    n,
            "risk_counts":                              rc,
            "pattern_counts":                           pc,
            "severity_counts":                          sc,
            "action_counts":                            ac,
            "avg_crisis_composite":                     round(tcomp / n, 1),
            "active_crisis_count":                      acc,
            "executive_response_count":                 erc,
            "avg_media_score":                          round(tmed / n, 1),
            "avg_social_score":                         round(tsoc / n, 1),
            "avg_legal_score":                          round(tleg / n, 1),
            "avg_reputation_score":                     round(trep / n, 1),
            "avg_estimated_reputation_damage_score":    round(tdmg / n, 2),
        }
