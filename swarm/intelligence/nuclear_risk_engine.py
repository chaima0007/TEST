"""
Module 326 — Nuclear Risk & Proliferation Intelligence Engine
Monitors proliferation momentum, deterrence stability, nuclear security,
and doctrine shifts across global nuclear domains.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class NuclearRiskInput:
    entity_id: str
    nuclear_domain: str
    region: str
    # 17 float fields (0.0–1.0)
    proliferation_momentum: float              # 0-1
    arms_control_erosion_rate: float           # 0-1
    nuclear_doctrine_shift: float              # 0-1
    tactical_nuclear_deployment_risk: float    # 0-1
    cyber_nuclear_vulnerability: float         # 0-1
    nuclear_terrorism_risk: float              # 0-1
    command_control_integrity: float           # 0-1, inverse: high=good
    deterrence_stability_erosion: float        # 0-1
    second_strike_vulnerability: float         # 0-1
    miscalculation_risk: float                 # 0-1
    fissile_material_security_gap: float       # 0-1
    nuclear_state_fragility_risk: float        # 0-1
    dual_use_technology_diffusion: float       # 0-1
    nuclear_taboo_erosion: float               # 0-1
    new_entrant_proliferation_risk: float      # 0-1
    nuclear_winter_probability_driver: float   # 0-1
    diplomatic_framework_collapse: float       # 0-1


@dataclass
class NuclearRiskResult:
    entity_id: str
    region: str
    nuclear_domain: str
    nuclear_risk: str
    nuclear_pattern: str
    nuclear_severity: str
    recommended_action: str
    proliferation_score: float
    stability_score: float
    security_score: float
    doctrine_score: float
    nuclear_composite: float
    is_nuclear_crisis: bool
    requires_nuclear_intervention: bool
    nuclear_signal: str

    def to_dict(self) -> Dict:
        return {
            "entity_id":                      self.entity_id,
            "region":                         self.region,
            "nuclear_domain":                 self.nuclear_domain,
            "nuclear_risk":                   self.nuclear_risk,
            "nuclear_pattern":                self.nuclear_pattern,
            "nuclear_severity":               self.nuclear_severity,
            "recommended_action":             self.recommended_action,
            "proliferation_score":            self.proliferation_score,
            "stability_score":                self.stability_score,
            "security_score":                 self.security_score,
            "doctrine_score":                 self.doctrine_score,
            "nuclear_composite":              self.nuclear_composite,
            "is_nuclear_crisis":              self.is_nuclear_crisis,
            "requires_nuclear_intervention":  self.requires_nuclear_intervention,
            "nuclear_signal":                 self.nuclear_signal,
        }


class NuclearRiskEngine:
    """
    Module 326 — Nuclear Risk & Proliferation Intelligence Engine
    Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
    """

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100)                                                  #
    # ------------------------------------------------------------------ #

    def _proliferation_score(self, i: NuclearRiskInput) -> float:
        return round(
            (
                i.proliferation_momentum * 0.4
                + i.new_entrant_proliferation_risk * 0.35
                + i.dual_use_technology_diffusion * 0.25
            ) * 100,
            2,
        )

    def _stability_score(self, i: NuclearRiskInput) -> float:
        return round(
            (
                i.deterrence_stability_erosion * 0.4
                + i.miscalculation_risk * 0.35
                + i.arms_control_erosion_rate * 0.25
            ) * 100,
            2,
        )

    def _security_score(self, i: NuclearRiskInput) -> float:
        return round(
            (
                i.fissile_material_security_gap * 0.4
                + i.nuclear_terrorism_risk * 0.35
                + (1 - i.command_control_integrity) * 0.25
            ) * 100,
            2,
        )

    def _doctrine_score(self, i: NuclearRiskInput) -> float:
        return round(
            (
                i.nuclear_doctrine_shift * 0.4
                + i.nuclear_taboo_erosion * 0.35
                + i.diplomatic_framework_collapse * 0.25
            ) * 100,
            2,
        )

    def _composite(
        self,
        proliferation: float,
        stability: float,
        security: float,
        doctrine: float,
    ) -> float:
        return round(
            proliferation * 0.30
            + stability * 0.25
            + security * 0.25
            + doctrine * 0.20,
            2,
        )

    # ------------------------------------------------------------------ #
    #  Risk classification                                                 #
    # ------------------------------------------------------------------ #

    def _risk(self, composite: float) -> str:
        if composite >= 60:
            return "critical"
        if composite >= 40:
            return "high"
        if composite >= 20:
            return "moderate"
        return "low"

    # ------------------------------------------------------------------ #
    #  Pattern detection (first match wins)                                #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: NuclearRiskInput) -> str:
        if i.proliferation_momentum >= 0.70 and i.new_entrant_proliferation_risk >= 0.65:
            return "proliferation_cascade"
        if i.deterrence_stability_erosion >= 0.70 and i.miscalculation_risk >= 0.65:
            return "deterrence_breakdown"
        if i.nuclear_terrorism_risk >= 0.70 and i.fissile_material_security_gap >= 0.65:
            return "nuclear_terrorism_event"
        if i.nuclear_doctrine_shift >= 0.70 and i.nuclear_taboo_erosion >= 0.65:
            return "doctrine_escalation"
        if i.arms_control_erosion_rate >= 0.70 and i.diplomatic_framework_collapse >= 0.65:
            return "arms_control_collapse"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity                                                            #
    # ------------------------------------------------------------------ #

    def _severity(self, composite: float) -> str:
        if composite >= 75:
            return "existential_threat"
        if composite >= 50:
            return "high_nuclear_risk"
        if composite >= 25:
            return "nuclear_tension"
        return "nuclear_stable"

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: str, pattern: str) -> str:
        if risk == "critical":
            return "existential_risk_protocol"
        if risk == "high":
            if pattern == "nuclear_terrorism_event":
                return "nuclear_security_emergency"
            return "nonproliferation_activation"
        if risk == "moderate":
            return "nuclear_monitoring"
        return "no_action"

    # ------------------------------------------------------------------ #
    #  French signal                                                       #
    # ------------------------------------------------------------------ #

    def _signal(
        self,
        i: NuclearRiskInput,
        pattern: str,
        composite: float,
    ) -> str:
        if composite < 20:
            return (
                "Domaine nucléaire stable — prolifération maîtrisée, "
                "dissuasion stable, sécurité des matières fissiles assurée, aucun risque existentiel détecté"
            )
        if composite >= 60:
            pattern_labels: Dict[str, str] = {
                "proliferation_cascade":    "Cascade de prolifération nucléaire",
                "deterrence_breakdown":     "Effondrement de la dissuasion",
                "nuclear_terrorism_event":  "Événement terroriste nucléaire imminent",
                "doctrine_escalation":      "Escalade doctrinale nucléaire",
                "arms_control_collapse":    "Effondrement du contrôle des armements",
                "none":                     "Défaillance nucléaire composite",
            }
            label = pattern_labels.get(pattern, pattern.replace("_", " ").title())
            return (
                f"Critique — risque existentiel nucléaire — {label}"
                f" — prolifération {i.proliferation_momentum:.2f}"
                f" — composite {composite:.0f}"
            )
        if composite >= 40:
            pattern_labels_high: Dict[str, str] = {
                "proliferation_cascade":    "Dynamique de prolifération en accélération",
                "deterrence_breakdown":     "Fragilisation de la dissuasion",
                "nuclear_terrorism_event":  "Risque terroriste nucléaire élevé",
                "doctrine_escalation":      "Dérive doctrinale nucléaire",
                "arms_control_collapse":    "Érosion du cadre de contrôle armements",
                "none":                     "Tension nucléaire diffuse",
            }
            label = pattern_labels_high.get(pattern, pattern.replace("_", " ").title())
            return (
                f"Risque nucléaire élevé — {label}"
                f" — érosion dissuasion {i.deterrence_stability_erosion:.2f}"
                f" — risque calcul erroné {i.miscalculation_risk:.2f}"
                f" — composite {composite:.0f}"
            )
        return (
            f"Tension nucléaire modérée — surveillance requise"
            f" — érosion contrôle armements {i.arms_control_erosion_rate:.2f}"
            f" — diffusion double usage {i.dual_use_technology_diffusion:.2f}"
            f" — composite {composite:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def _analyze_one(self, i: NuclearRiskInput) -> NuclearRiskResult:
        proliferation = self._proliferation_score(i)
        stability     = self._stability_score(i)
        security      = self._security_score(i)
        doctrine      = self._doctrine_score(i)
        composite     = self._composite(proliferation, stability, security, doctrine)
        risk          = self._risk(composite)
        pattern       = self._pattern(i)
        severity      = self._severity(composite)
        action        = self._action(risk, pattern)
        signal        = self._signal(i, pattern, composite)

        return NuclearRiskResult(
            entity_id=i.entity_id,
            region=i.region,
            nuclear_domain=i.nuclear_domain,
            nuclear_risk=risk,
            nuclear_pattern=pattern,
            nuclear_severity=severity,
            recommended_action=action,
            proliferation_score=proliferation,
            stability_score=stability,
            security_score=security,
            doctrine_score=doctrine,
            nuclear_composite=composite,
            is_nuclear_crisis=composite >= 60,
            requires_nuclear_intervention=composite >= 40,
            nuclear_signal=signal,
        )

    def analyze(self, entities: List[NuclearRiskInput]) -> Dict:
        results = [self._analyze_one(i) for i in entities]

        if not results:
            return {
                "total_entities":                     0,
                "critical_entities":                  0,
                "high_entities":                      0,
                "moderate_entities":                  0,
                "low_entities":                       0,
                "crisis_entities":                    0,
                "intervention_required":              0,
                "avg_proliferation_score":            0.0,
                "avg_stability_score":                0.0,
                "avg_security_score":                 0.0,
                "avg_doctrine_score":                 0.0,
                "avg_nuclear_composite":              0.0,
                "avg_estimated_nuclear_threat_index": 0.0,
            }

        n = len(results)

        critical_entities     = sum(1 for r in results if r.nuclear_risk == "critical")
        high_entities         = sum(1 for r in results if r.nuclear_risk == "high")
        moderate_entities     = sum(1 for r in results if r.nuclear_risk == "moderate")
        low_entities          = sum(1 for r in results if r.nuclear_risk == "low")
        crisis_entities       = sum(1 for r in results if r.is_nuclear_crisis)
        intervention_required = sum(1 for r in results if r.requires_nuclear_intervention)

        avg_proliferation = round(sum(r.proliferation_score for r in results) / n, 2)
        avg_stability     = round(sum(r.stability_score     for r in results) / n, 2)
        avg_security      = round(sum(r.security_score      for r in results) / n, 2)
        avg_doctrine      = round(sum(r.doctrine_score      for r in results) / n, 2)
        avg_composite     = round(sum(r.nuclear_composite   for r in results) / n, 2)

        return {
            "total_entities":                     n,
            "critical_entities":                  critical_entities,
            "high_entities":                      high_entities,
            "moderate_entities":                  moderate_entities,
            "low_entities":                       low_entities,
            "crisis_entities":                    crisis_entities,
            "intervention_required":              intervention_required,
            "avg_proliferation_score":            avg_proliferation,
            "avg_stability_score":                avg_stability,
            "avg_security_score":                 avg_security,
            "avg_doctrine_score":                 avg_doctrine,
            "avg_nuclear_composite":              avg_composite,
            "avg_estimated_nuclear_threat_index": round(avg_composite / 100 * 10, 2),
        }
