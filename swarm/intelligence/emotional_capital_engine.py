"""
Module 267 — Emotional Capital & Wellbeing Economy Engine
Measures emotional capital as a strategic organisational asset, tracking wellbeing
economics and psychological safety at scale.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class WellbeingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class EmotionalPattern(str, Enum):
    none                     = "none"
    burnout_crisis           = "burnout_crisis"
    meaning_collapse         = "meaning_collapse"
    isolation_epidemic       = "isolation_epidemic"
    safety_erosion           = "safety_erosion"
    joy_deficit              = "joy_deficit"


class WellbeingSeverity(str, Enum):
    flourishing = "flourishing"
    recovering  = "recovering"
    depleted    = "depleted"
    crisis      = "crisis"


class WellbeingAction(str, Enum):
    no_action              = "no_action"
    wellbeing_monitoring   = "wellbeing_monitoring"
    meaning_restoration    = "meaning_restoration"
    connection_program     = "connection_program"
    emergency_wellbeing    = "emergency_wellbeing"
    burnout_intervention   = "burnout_intervention"


class WorkforceSegment(str, Enum):
    executive_layer  = "executive_layer"
    frontline_workers = "frontline_workers"
    remote_workforce = "remote_workforce"
    creative_teams   = "creative_teams"
    technical_staff  = "technical_staff"
    customer_facing  = "customer_facing"
    caregiving_roles = "caregiving_roles"
    gig_workforce    = "gig_workforce"


@dataclass
class WellbeingInput:
    unit_id: str
    workforce_segment: str
    region: str
    psychological_safety_score: float       # 0-1, 1 = highly safe
    burnout_prevalence_rate: float          # 0-1, higher = worse
    emotional_exhaustion_index: float       # 0-1, higher = worse
    meaning_alignment_score: float          # 0-1, 1 = strong alignment
    social_connection_quality: float        # 0-1, 1 = excellent
    autonomy_satisfaction_score: float      # 0-1, 1 = high autonomy
    recognition_adequacy: float             # 0-1, 1 = well recognised
    resilience_capital_score: float         # 0-1, 1 = highly resilient
    grief_processing_support: float         # 0-1, 1 = well supported
    somatic_health_score: float             # 0-1, 1 = excellent
    financial_anxiety_exposure: float       # 0-1, higher = worse
    purpose_clarity_score: float            # 0-1, 1 = clear purpose
    community_belonging_index: float        # 0-1, 1 = strong belonging
    leadership_empathy_score: float         # 0-1, 1 = highly empathic
    work_life_integration_score: float      # 0-1, 1 = well integrated
    emotional_contagion_awareness: float    # 0-1, 1 = high awareness
    joy_at_work_index: float                # 0-1, 1 = high joy


@dataclass
class WellbeingResult:
    unit_id: str
    region: str
    wellbeing_risk: str
    emotional_pattern: str
    wellbeing_severity: str
    recommended_action: str
    burnout_score: float
    safety_score: float
    meaning_score: float
    connection_score: float
    emotional_composite: float
    has_burnout_alert: bool
    requires_emergency_support: bool
    estimated_burnout_risk_index: float
    wellbeing_signal: str

    def to_dict(self) -> Dict:
        return {
            "unit_id":                      self.unit_id,
            "region":                       self.region,
            "wellbeing_risk":               self.wellbeing_risk,
            "emotional_pattern":            self.emotional_pattern,
            "wellbeing_severity":           self.wellbeing_severity,
            "recommended_action":           self.recommended_action,
            "burnout_score":                self.burnout_score,
            "safety_score":                 self.safety_score,
            "meaning_score":                self.meaning_score,
            "connection_score":             self.connection_score,
            "emotional_composite":          self.emotional_composite,
            "has_burnout_alert":            self.has_burnout_alert,
            "requires_emergency_support":   self.requires_emergency_support,
            "estimated_burnout_risk_index": self.estimated_burnout_risk_index,
            "wellbeing_signal":             self.wellbeing_signal,
        }


class EmotionalCapitalEngine:
    def __init__(self) -> None:
        self._results: List[WellbeingResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _burnout_score(self, i: WellbeingInput) -> float:
        """weight 0.30 — higher = worse (burnout risk indicators)"""
        s = 0
        if   i.burnout_prevalence_rate >= 0.65: s += 40
        elif i.burnout_prevalence_rate >= 0.40: s += 22
        elif i.burnout_prevalence_rate >= 0.20: s += 8

        if   i.emotional_exhaustion_index >= 0.65: s += 35
        elif i.emotional_exhaustion_index >= 0.40: s += 18
        elif i.emotional_exhaustion_index >= 0.20: s += 6

        if   i.financial_anxiety_exposure >= 0.65: s += 25
        elif i.financial_anxiety_exposure >= 0.40: s += 12
        return min(s, 100)

    def _safety_score(self, i: WellbeingInput) -> float:
        """weight 0.25 — inverted inputs (low value = high risk)"""
        s = 0
        if   i.psychological_safety_score <= 0.35: s += 40
        elif i.psychological_safety_score <= 0.55: s += 22
        elif i.psychological_safety_score <= 0.70: s += 8

        if   i.leadership_empathy_score <= 0.35: s += 35
        elif i.leadership_empathy_score <= 0.55: s += 18
        elif i.leadership_empathy_score <= 0.70: s += 6

        if   i.recognition_adequacy <= 0.35: s += 25
        elif i.recognition_adequacy <= 0.55: s += 12
        return min(s, 100)

    def _meaning_score(self, i: WellbeingInput) -> float:
        """weight 0.25 — inverted inputs"""
        s = 0
        if   i.meaning_alignment_score <= 0.35: s += 40
        elif i.meaning_alignment_score <= 0.55: s += 22
        elif i.meaning_alignment_score <= 0.70: s += 8

        if   i.purpose_clarity_score <= 0.35: s += 35
        elif i.purpose_clarity_score <= 0.55: s += 18
        elif i.purpose_clarity_score <= 0.70: s += 6

        if   i.autonomy_satisfaction_score <= 0.35: s += 25
        elif i.autonomy_satisfaction_score <= 0.55: s += 12
        return min(s, 100)

    def _connection_score(self, i: WellbeingInput) -> float:
        """weight 0.20 — inverted inputs"""
        s = 0
        if   i.social_connection_quality <= 0.35: s += 40
        elif i.social_connection_quality <= 0.55: s += 22
        elif i.social_connection_quality <= 0.70: s += 8

        if   i.community_belonging_index <= 0.35: s += 35
        elif i.community_belonging_index <= 0.55: s += 18
        elif i.community_belonging_index <= 0.70: s += 6

        if   i.work_life_integration_score <= 0.35: s += 25
        elif i.work_life_integration_score <= 0.55: s += 12
        return min(s, 100)

    def _composite(self, bn: float, sf: float, mn: float, cn: float) -> float:
        return min(round(bn * 0.30 + sf * 0.25 + mn * 0.25 + cn * 0.20, 2), 100.0)

    def _risk(self, c: float) -> WellbeingRisk:
        if c >= 60: return WellbeingRisk.critical
        if c >= 40: return WellbeingRisk.high
        if c >= 20: return WellbeingRisk.moderate
        return WellbeingRisk.low

    def _severity(self, c: float) -> WellbeingSeverity:
        if c >= 60: return WellbeingSeverity.crisis
        if c >= 40: return WellbeingSeverity.depleted
        if c >= 20: return WellbeingSeverity.recovering
        return WellbeingSeverity.flourishing

    def _pattern(self, i: WellbeingInput) -> EmotionalPattern:
        if i.burnout_prevalence_rate >= 0.60 or i.emotional_exhaustion_index >= 0.65:
            return EmotionalPattern.burnout_crisis
        if i.meaning_alignment_score <= 0.35 or i.purpose_clarity_score <= 0.30:
            return EmotionalPattern.meaning_collapse
        if i.social_connection_quality <= 0.35 or i.community_belonging_index <= 0.30:
            return EmotionalPattern.isolation_epidemic
        if i.psychological_safety_score <= 0.35 or i.leadership_empathy_score <= 0.30:
            return EmotionalPattern.safety_erosion
        if i.joy_at_work_index <= 0.30 and i.resilience_capital_score <= 0.40:
            return EmotionalPattern.joy_deficit
        return EmotionalPattern.none

    def _action(self, risk: WellbeingRisk, pat: EmotionalPattern) -> WellbeingAction:
        if risk == WellbeingRisk.critical:
            if pat == EmotionalPattern.burnout_crisis:
                return WellbeingAction.burnout_intervention
            return WellbeingAction.emergency_wellbeing
        if risk == WellbeingRisk.high:
            if pat in (EmotionalPattern.meaning_collapse, EmotionalPattern.joy_deficit):
                return WellbeingAction.meaning_restoration
            return WellbeingAction.connection_program
        if risk == WellbeingRisk.moderate:
            return WellbeingAction.wellbeing_monitoring
        return WellbeingAction.no_action

    def _has_burnout_alert(self, i: WellbeingInput, comp: float) -> bool:
        return (
            comp >= 40
            or i.burnout_prevalence_rate >= 0.50
            or i.emotional_exhaustion_index >= 0.60
            or i.joy_at_work_index <= 0.25
        )

    def _requires_emergency_support(self, i: WellbeingInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.burnout_prevalence_rate >= 0.65
            or i.psychological_safety_score <= 0.25
            or i.emotional_exhaustion_index >= 0.70
        )

    def _burnout_risk_index(self, i: WellbeingInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.resilience_capital_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: WellbeingInput, pat: EmotionalPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Capital émotionnel florissant — bien-être optimal, "
                "sécurité psychologique forte, sens et connexion préservés"
            )
        labels: Dict[EmotionalPattern, str] = {
            EmotionalPattern.burnout_crisis:     "Crise de burnout",
            EmotionalPattern.meaning_collapse:   "Effondrement du sens",
            EmotionalPattern.isolation_epidemic: "Épidémie d'isolement",
            EmotionalPattern.safety_erosion:     "Érosion de la sécurité",
            EmotionalPattern.joy_deficit:        "Déficit de joie au travail",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — "
            f"burnout {i.burnout_prevalence_rate * 100:.0f}% — "
            f"épuisement {i.emotional_exhaustion_index * 100:.0f}% — "
            f"sécurité psy. {i.psychological_safety_score * 100:.0f}% — "
            f"composite {comp:.0f}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, i: WellbeingInput) -> WellbeingResult:
        bn   = self._burnout_score(i)
        sf   = self._safety_score(i)
        mn   = self._meaning_score(i)
        cn   = self._connection_score(i)
        comp = self._composite(bn, sf, mn, cn)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = WellbeingResult(
            unit_id=i.unit_id,
            region=i.region,
            wellbeing_risk=risk.value,
            emotional_pattern=pat.value,
            wellbeing_severity=sev.value,
            recommended_action=act.value,
            burnout_score=bn,
            safety_score=sf,
            meaning_score=mn,
            connection_score=cn,
            emotional_composite=comp,
            has_burnout_alert=self._has_burnout_alert(i, comp),
            requires_emergency_support=self._requires_emergency_support(i, comp),
            estimated_burnout_risk_index=self._burnout_risk_index(i, comp),
            wellbeing_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[WellbeingInput]) -> List[WellbeingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total":                              0,
                "risk_counts":                        {},
                "pattern_counts":                     {},
                "severity_counts":                    {},
                "action_counts":                      {},
                "avg_emotional_composite":            0.0,
                "burnout_alert_count":                0,
                "emergency_support_count":            0,
                "avg_burnout_score":                  0.0,
                "avg_safety_score":                   0.0,
                "avg_meaning_score":                  0.0,
                "avg_connection_score":               0.0,
                "avg_estimated_burnout_risk_index":   0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tbn = tsf = tmn = tcn = tcomp = trisk = 0.0
        alert_c = emerg_c = 0
        for r in self._results:
            rc[r.wellbeing_risk]      = rc.get(r.wellbeing_risk, 0)      + 1
            pc[r.emotional_pattern]   = pc.get(r.emotional_pattern, 0)   + 1
            sc[r.wellbeing_severity]  = sc.get(r.wellbeing_severity, 0)  + 1
            ac[r.recommended_action]  = ac.get(r.recommended_action, 0)  + 1
            tbn   += r.burnout_score
            tsf   += r.safety_score
            tmn   += r.meaning_score
            tcn   += r.connection_score
            tcomp += r.emotional_composite
            trisk += r.estimated_burnout_risk_index
            if r.has_burnout_alert:           alert_c  += 1
            if r.requires_emergency_support:  emerg_c  += 1
        return {
            "total":                              n,
            "risk_counts":                        rc,
            "pattern_counts":                     pc,
            "severity_counts":                    sc,
            "action_counts":                      ac,
            "avg_emotional_composite":            round(tcomp / n, 1),
            "burnout_alert_count":                alert_c,
            "emergency_support_count":            emerg_c,
            "avg_burnout_score":                  round(tbn  / n, 1),
            "avg_safety_score":                   round(tsf  / n, 1),
            "avg_meaning_score":                  round(tmn  / n, 1),
            "avg_connection_score":               round(tcn  / n, 1),
            "avg_estimated_burnout_risk_index":   round(trisk / n, 2),
        }
