"""
Module 330 — Digital Democracy & Algorithmic Governance Intelligence Engine
Caelum Partners Swarm Intelligence — Propriété exclusive de Chaima Mhadbi
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class DigitalDemocracyInput:
    entity_id: str
    governance_domain: str
    region: str
    # 17 float fields (0-1)
    algorithmic_bias_in_governance: float
    digital_exclusion_index: float
    surveillance_democracy_ratio: float
    platform_political_capture: float
    misinformation_amplification_rate: float
    citizen_digital_participation: float
    e_voting_integrity_risk: float
    algorithmic_accountability_gap: float
    open_data_governance_level: float
    regulatory_tech_capture: float
    digital_rights_erosion_index: float
    AI_policy_decision_autonomy: float
    cross_platform_polarization: float
    electoral_manipulation_risk: float
    civic_tech_adoption: float
    democratic_AI_oversight: float
    digital_identity_sovereignty_risk: float


@dataclass
class DigitalDemocracyResult:
    entity_id: str
    governance_domain: str
    region: str
    exclusion_score: float
    manipulation_score: float
    accountability_score: float
    sovereignty_score: float
    composite_score: float
    risk_level: str
    democracy_pattern: str
    severity: str
    recommended_action: str
    signal: str
    e_voting_integrity_risk: float
    open_data_governance_level: float

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys."""
        return {
            "entity_id":                  self.entity_id,
            "governance_domain":          self.governance_domain,
            "region":                     self.region,
            "exclusion_score":            self.exclusion_score,
            "manipulation_score":         self.manipulation_score,
            "accountability_score":       self.accountability_score,
            "sovereignty_score":          self.sovereignty_score,
            "composite_score":            self.composite_score,
            "risk_level":                 self.risk_level,
            "democracy_pattern":          self.democracy_pattern,
            "severity":                   self.severity,
            "recommended_action":         self.recommended_action,
            "signal":                     self.signal,
            "e_voting_integrity_risk":    self.e_voting_integrity_risk,
            "open_data_governance_level": self.open_data_governance_level,
        }


class DigitalDemocracyEngine:
    def __init__(self) -> None:
        self._results: List[DigitalDemocracyResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _exclusion_score(self, i: DigitalDemocracyInput) -> float:
        s = (
            i.digital_exclusion_index * 0.40
            + i.algorithmic_bias_in_governance * 0.35
            + i.digital_rights_erosion_index * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _manipulation_score(self, i: DigitalDemocracyInput) -> float:
        s = (
            i.misinformation_amplification_rate * 0.40
            + i.electoral_manipulation_risk * 0.35
            + i.platform_political_capture * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _accountability_score(self, i: DigitalDemocracyInput) -> float:
        s = (
            i.algorithmic_accountability_gap * 0.40
            + i.AI_policy_decision_autonomy * 0.35
            + i.regulatory_tech_capture * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _sovereignty_score(self, i: DigitalDemocracyInput) -> float:
        s = (
            i.digital_identity_sovereignty_risk * 0.40
            + i.surveillance_democracy_ratio * 0.35
            + i.cross_platform_polarization * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _composite(self, excl: float, manip: float, acct: float, sov: float) -> float:
        return min(round(excl * 0.30 + manip * 0.25 + acct * 0.25 + sov * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk level                                                          #
    # ------------------------------------------------------------------ #

    def _risk_level(self, c: float) -> str:
        if c >= 60: return "critical"
        if c >= 40: return "high"
        if c >= 20: return "moderate"
        return "low"

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: DigitalDemocracyInput) -> str:
        if i.algorithmic_bias_in_governance >= 0.70 and i.AI_policy_decision_autonomy >= 0.65:
            return "algorithmic_autocracy"
        if i.digital_exclusion_index >= 0.70 and i.citizen_digital_participation <= 0.35:
            return "digital_disenfranchisement"
        if i.electoral_manipulation_risk >= 0.70 and i.misinformation_amplification_rate >= 0.65:
            return "electoral_subversion"
        if i.surveillance_democracy_ratio >= 0.70 and i.digital_rights_erosion_index >= 0.65:
            return "surveillance_democracy"
        if i.platform_political_capture >= 0.70 and i.regulatory_tech_capture >= 0.65:
            return "platform_sovereignty_capture"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity, action, signal                                            #
    # ------------------------------------------------------------------ #

    def _severity(self, risk: str) -> str:
        return {
            "critical": "démocratie_numérique_compromise",
            "high":     "risque_démocratique_élevé",
            "moderate": "fragilité_gouvernance",
            "low":      "gouvernance_stable",
        }[risk]

    def _action(self, risk: str) -> str:
        return {
            "critical": "intervention_démocratique_urgente",
            "high":     "réforme_gouvernance_algorithmique",
            "moderate": "renforcement_oversight_numérique",
            "low":      "surveillance_continue",
        }[risk]

    def _signal(self, risk: str) -> str:
        return {
            "critical": "🔴 Démocratie numérique en péril — intervention urgente",
            "high":     "🟠 Risques algorithmiques majeurs détectés",
            "moderate": "🟡 Fragilités gouvernance numérique",
            "low":      "🟢 Gouvernance démocratique numérique stable",
        }[risk]

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: DigitalDemocracyInput) -> DigitalDemocracyResult:
        excl  = self._exclusion_score(i)
        manip = self._manipulation_score(i)
        acct  = self._accountability_score(i)
        sov   = self._sovereignty_score(i)
        comp  = self._composite(excl, manip, acct, sov)
        risk  = self._risk_level(comp)
        pat   = self._pattern(i)
        sev   = self._severity(risk)
        act   = self._action(risk)
        sig   = self._signal(risk)
        result = DigitalDemocracyResult(
            entity_id=i.entity_id,
            governance_domain=i.governance_domain,
            region=i.region,
            exclusion_score=excl,
            manipulation_score=manip,
            accountability_score=acct,
            sovereignty_score=sov,
            composite_score=comp,
            risk_level=risk,
            democracy_pattern=pat,
            severity=sev,
            recommended_action=act,
            signal=sig,
            e_voting_integrity_risk=i.e_voting_integrity_risk,
            open_data_governance_level=i.open_data_governance_level,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[DigitalDemocracyInput]) -> List[DigitalDemocracyResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        results = self._results
        n = len(results)
        if not results:
            return {
                "module_id":                          330,
                "module_name":                        "Digital Democracy & Algorithmic Governance Intelligence Engine",
                "total_entities":                     0,
                "critical_count":                     0,
                "high_count":                         0,
                "moderate_count":                     0,
                "low_count":                          0,
                "avg_composite":                      0.0,
                "pattern_distribution":               {},
                "risk_distribution":                  {},
                "severity_distribution":              {},
                "action_distribution":                {},
                "avg_estimated_democracy_risk_index": 0.0,
            }

        pattern_dist: Dict[str, int]  = {}
        risk_dist: Dict[str, int]     = {}
        severity_dist: Dict[str, int] = {}
        action_dist: Dict[str, int]   = {}
        total_comp = 0.0
        critical_c = high_c = moderate_c = low_c = 0

        for r in results:
            pattern_dist[r.democracy_pattern] = pattern_dist.get(r.democracy_pattern, 0) + 1
            risk_dist[r.risk_level]           = risk_dist.get(r.risk_level, 0)           + 1
            severity_dist[r.severity]         = severity_dist.get(r.severity, 0)         + 1
            action_dist[r.recommended_action] = action_dist.get(r.recommended_action, 0) + 1
            total_comp += r.composite_score
            if r.risk_level == "critical":   critical_c  += 1
            elif r.risk_level == "high":     high_c      += 1
            elif r.risk_level == "moderate": moderate_c  += 1
            else:                            low_c       += 1

        avg_comp = round(total_comp / n, 1)
        return {
            "module_id":                          330,
            "module_name":                        "Digital Democracy & Algorithmic Governance Intelligence Engine",
            "total_entities":                     n,
            "critical_count":                     critical_c,
            "high_count":                         high_c,
            "moderate_count":                     moderate_c,
            "low_count":                          low_c,
            "avg_composite":                      avg_comp,
            "pattern_distribution":               pattern_dist,
            "risk_distribution":                  risk_dist,
            "severity_distribution":              severity_dist,
            "action_distribution":                action_dist,
            "avg_estimated_democracy_risk_index": round(avg_comp / 100 * 10, 2),
        }
