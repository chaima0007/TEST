"""
Module 236 — Organizational Health & Culture Engine
Tracks employee engagement, leadership effectiveness, psychological safety, cultural
alignment and wellbeing signals — then prescribes targeted culture or leadership
interventions before dysfunction becomes systemic.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class HealthRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CulturePattern(str, Enum):
    none                = "none"
    toxic_culture       = "toxic_culture"
    disengagement_spiral = "disengagement_spiral"
    leadership_void     = "leadership_void"
    change_resistance   = "change_resistance"
    diversity_gap       = "diversity_gap"


class HealthSeverity(str, Enum):
    thriving   = "thriving"
    stable     = "stable"
    concerning = "concerning"
    critical   = "critical"


class HealthAction(str, Enum):
    no_action                    = "no_action"
    culture_monitoring           = "culture_monitoring"
    engagement_initiative        = "engagement_initiative"
    leadership_coaching          = "leadership_coaching"
    change_management_program    = "change_management_program"
    diversity_inclusion_program  = "diversity_inclusion_program"
    culture_transformation       = "culture_transformation"
    executive_intervention       = "executive_intervention"
    organizational_restructuring = "organizational_restructuring"


@dataclass
class OrgHealthInput:
    unit_id: str
    department: str
    region: str
    employee_engagement_score: float        # 0-1, 1 = highly engaged
    voluntary_turnover_rate: float          # 0-1
    manager_effectiveness_score: float      # 0-1, 1 = excellent
    psychological_safety_score: float       # 0-1, 1 = safe
    inclusion_belonging_score: float        # 0-1, 1 = strong
    collaboration_quality_score: float      # 0-1, 1 = excellent
    change_adoption_rate: float             # 0-1
    cultural_alignment_score: float         # 0-1, 1 = aligned
    conflict_frequency_score: float         # 0-1, 1 = frequent
    absenteeism_rate_pct: float             # 0-1
    productivity_trend_score: float         # 0-1, 1 = improving
    burnout_prevalence_score: float         # 0-1, 1 = high burnout
    promotion_equity_score: float           # 0-1, 1 = equitable
    communication_effectiveness_score: float  # 0-1, 1 = effective
    knowledge_sharing_index: float          # 0-1, 1 = high sharing
    innovation_culture_score: float         # 0-1, 1 = innovative
    values_alignment_score: float           # 0-1, 1 = aligned


@dataclass
class OrgHealthResult:
    unit_id: str
    region: str
    health_risk: str
    culture_pattern: str
    health_severity: str
    recommended_action: str
    engagement_score: float
    leadership_score: float
    culture_score: float
    wellbeing_score: float
    health_composite: float
    has_culture_alert: bool
    requires_executive_intervention: bool
    estimated_culture_risk_index: float
    health_signal: str

    def to_dict(self) -> Dict:
        return {
            "unit_id":                          self.unit_id,
            "region":                           self.region,
            "health_risk":                      self.health_risk,
            "culture_pattern":                  self.culture_pattern,
            "health_severity":                  self.health_severity,
            "recommended_action":               self.recommended_action,
            "engagement_score":                 self.engagement_score,
            "leadership_score":                 self.leadership_score,
            "culture_score":                    self.culture_score,
            "wellbeing_score":                  self.wellbeing_score,
            "health_composite":                 self.health_composite,
            "has_culture_alert":                self.has_culture_alert,
            "requires_executive_intervention":  self.requires_executive_intervention,
            "estimated_culture_risk_index":     self.estimated_culture_risk_index,
            "health_signal":                    self.health_signal,
        }


class OrganizationalHealthCultureEngine:
    def __init__(self) -> None:
        self._results: List[OrgHealthResult] = []

    # ── sub-scores ────────────────────────────────────────────────────────────

    def _engagement_score(self, i: OrgHealthInput) -> float:
        s = 0
        if   i.employee_engagement_score <= 0.40: s += 40
        elif i.employee_engagement_score <= 0.60: s += 22
        elif i.employee_engagement_score <= 0.75: s += 8

        if   i.voluntary_turnover_rate >= 0.25: s += 35
        elif i.voluntary_turnover_rate >= 0.15: s += 18
        elif i.voluntary_turnover_rate >= 0.08: s += 6

        if   i.collaboration_quality_score <= 0.40: s += 25
        elif i.collaboration_quality_score <= 0.60: s += 12
        return min(s, 100)

    def _leadership_score(self, i: OrgHealthInput) -> float:
        s = 0
        if   i.manager_effectiveness_score <= 0.40: s += 40
        elif i.manager_effectiveness_score <= 0.60: s += 22
        elif i.manager_effectiveness_score <= 0.75: s += 8

        if   i.promotion_equity_score <= 0.40: s += 35
        elif i.promotion_equity_score <= 0.60: s += 18
        elif i.promotion_equity_score <= 0.75: s += 6

        if   i.change_adoption_rate <= 0.40: s += 25
        elif i.change_adoption_rate <= 0.60: s += 12
        return min(s, 100)

    def _culture_score(self, i: OrgHealthInput) -> float:
        s = 0
        if   i.cultural_alignment_score <= 0.40: s += 40
        elif i.cultural_alignment_score <= 0.60: s += 22
        elif i.cultural_alignment_score <= 0.75: s += 8

        if   i.psychological_safety_score <= 0.40: s += 35
        elif i.psychological_safety_score <= 0.60: s += 18
        elif i.psychological_safety_score <= 0.75: s += 6

        if   i.conflict_frequency_score >= 0.60: s += 25
        elif i.conflict_frequency_score >= 0.35: s += 12
        return min(s, 100)

    def _wellbeing_score(self, i: OrgHealthInput) -> float:
        s = 0
        if   i.burnout_prevalence_score >= 0.60: s += 40
        elif i.burnout_prevalence_score >= 0.35: s += 22
        elif i.burnout_prevalence_score >= 0.15: s += 8

        if   i.absenteeism_rate_pct >= 0.12: s += 35
        elif i.absenteeism_rate_pct >= 0.07: s += 18
        elif i.absenteeism_rate_pct >= 0.03: s += 6

        if   i.productivity_trend_score <= 0.40: s += 25
        elif i.productivity_trend_score <= 0.60: s += 12
        return min(s, 100)

    def _composite(self, eng: float, lead: float, cult: float, well: float) -> float:
        return min(round(eng * 0.30 + lead * 0.25 + cult * 0.25 + well * 0.20, 2), 100.0)

    def _risk(self, c: float) -> HealthRisk:
        if c >= 60: return HealthRisk.critical
        if c >= 40: return HealthRisk.high
        if c >= 20: return HealthRisk.moderate
        return HealthRisk.low

    def _severity(self, c: float) -> HealthSeverity:
        if c >= 60: return HealthSeverity.critical
        if c >= 40: return HealthSeverity.concerning
        if c >= 20: return HealthSeverity.stable
        return HealthSeverity.thriving

    def _pattern(self, i: OrgHealthInput) -> CulturePattern:
        if (i.psychological_safety_score <= 0.35
                or i.conflict_frequency_score >= 0.65):
            return CulturePattern.toxic_culture
        if (i.employee_engagement_score <= 0.35
                or i.voluntary_turnover_rate >= 0.25):
            return CulturePattern.disengagement_spiral
        if (i.manager_effectiveness_score <= 0.35
                or i.promotion_equity_score <= 0.35):
            return CulturePattern.leadership_void
        if (i.change_adoption_rate <= 0.35
                and i.cultural_alignment_score <= 0.55):
            return CulturePattern.change_resistance
        if i.inclusion_belonging_score <= 0.40:
            return CulturePattern.diversity_gap
        return CulturePattern.none

    def _action(self, risk: HealthRisk, pat: CulturePattern) -> HealthAction:
        if risk == HealthRisk.critical:
            if pat == CulturePattern.toxic_culture:
                return HealthAction.executive_intervention
            if pat == CulturePattern.disengagement_spiral:
                return HealthAction.organizational_restructuring
            return HealthAction.culture_transformation
        if risk == HealthRisk.high:
            if pat == CulturePattern.toxic_culture:
                return HealthAction.culture_transformation
            if pat == CulturePattern.disengagement_spiral:
                return HealthAction.engagement_initiative
            if pat == CulturePattern.leadership_void:
                return HealthAction.leadership_coaching
            if pat == CulturePattern.change_resistance:
                return HealthAction.change_management_program
            if pat == CulturePattern.diversity_gap:
                return HealthAction.diversity_inclusion_program
            return HealthAction.culture_monitoring
        if risk == HealthRisk.moderate:
            return HealthAction.culture_monitoring
        return HealthAction.no_action

    def _has_culture_alert(self, i: OrgHealthInput, comp: float) -> bool:
        return (
            comp >= 40
            or i.voluntary_turnover_rate >= 0.20
            or i.burnout_prevalence_score >= 0.55
            or i.employee_engagement_score <= 0.40
        )

    def _requires_executive_intervention(self, i: OrgHealthInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.psychological_safety_score <= 0.30
            or i.manager_effectiveness_score <= 0.35
            or i.voluntary_turnover_rate >= 0.25
        )

    def _culture_risk_index(self, i: OrgHealthInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.values_alignment_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: OrgHealthInput, pat: CulturePattern, comp: float) -> str:
        if comp < 20:
            return (
                "Culture organisationnelle saine — engagement fort, "
                "leadership solide, bien-être optimal"
            )
        labels: Dict[CulturePattern, str] = {
            CulturePattern.toxic_culture:        "Culture toxique",
            CulturePattern.disengagement_spiral: "Spirale de désengagement",
            CulturePattern.leadership_void:      "Vide de leadership",
            CulturePattern.change_resistance:    "Résistance au changement",
            CulturePattern.diversity_gap:        "Écart de diversité",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — "
            f"engagement {i.employee_engagement_score * 100:.0f}% — "
            f"turnover {i.voluntary_turnover_rate * 100:.0f}% — "
            f"manager eff. {i.manager_effectiveness_score * 100:.0f}% — "
            f"composite {comp:.0f}"
        )

    # ── public API ────────────────────────────────────────────────────────────

    def assess(self, i: OrgHealthInput) -> OrgHealthResult:
        eng  = self._engagement_score(i)
        lead = self._leadership_score(i)
        cult = self._culture_score(i)
        well = self._wellbeing_score(i)
        comp = self._composite(eng, lead, cult, well)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = OrgHealthResult(
            unit_id=i.unit_id,
            region=i.region,
            health_risk=risk.value,
            culture_pattern=pat.value,
            health_severity=sev.value,
            recommended_action=act.value,
            engagement_score=eng,
            leadership_score=lead,
            culture_score=cult,
            wellbeing_score=well,
            health_composite=comp,
            has_culture_alert=self._has_culture_alert(i, comp),
            requires_executive_intervention=self._requires_executive_intervention(i, comp),
            estimated_culture_risk_index=self._culture_risk_index(i, comp),
            health_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[OrgHealthInput]) -> List[OrgHealthResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total":                          0,
                "risk_counts":                    {},
                "pattern_counts":                 {},
                "severity_counts":                {},
                "action_counts":                  {},
                "avg_health_composite":           0.0,
                "culture_alert_count":            0,
                "executive_intervention_count":   0,
                "avg_engagement_score":           0.0,
                "avg_leadership_score":           0.0,
                "avg_culture_score":              0.0,
                "avg_wellbeing_score":            0.0,
                "avg_estimated_culture_risk_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        teng = tlead = tcult = twell = tcomp = trisk = 0.0
        alert_c = exec_c = 0
        for r in self._results:
            rc[r.health_risk]          = rc.get(r.health_risk, 0)          + 1
            pc[r.culture_pattern]      = pc.get(r.culture_pattern, 0)      + 1
            sc[r.health_severity]      = sc.get(r.health_severity, 0)      + 1
            ac[r.recommended_action]   = ac.get(r.recommended_action, 0)   + 1
            teng  += r.engagement_score
            tlead += r.leadership_score
            tcult += r.culture_score
            twell += r.wellbeing_score
            tcomp += r.health_composite
            trisk += r.estimated_culture_risk_index
            if r.has_culture_alert:               alert_c += 1
            if r.requires_executive_intervention: exec_c  += 1
        return {
            "total":                              n,
            "risk_counts":                        rc,
            "pattern_counts":                     pc,
            "severity_counts":                    sc,
            "action_counts":                      ac,
            "avg_health_composite":               round(tcomp / n, 1),
            "culture_alert_count":                alert_c,
            "executive_intervention_count":       exec_c,
            "avg_engagement_score":               round(teng  / n, 1),
            "avg_leadership_score":               round(tlead / n, 1),
            "avg_culture_score":                  round(tcult / n, 1),
            "avg_wellbeing_score":                round(twell / n, 1),
            "avg_estimated_culture_risk_index":   round(trisk / n, 2),
        }
