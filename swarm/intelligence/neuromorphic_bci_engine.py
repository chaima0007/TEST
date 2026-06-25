"""
Module 310 — Neuromorphic Computing & Brain-Computer Interface Intelligence Engine
Monitors neural interface infrastructure for privacy violations, security vulnerabilities,
neurorights breaches, and societal risks of BCI technologies.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class NeuralRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class NeuralPattern(str, Enum):
    none                       = "none"
    neural_sovereignty_breach  = "neural_sovereignty_breach"
    brain_hacking_attack       = "brain_hacking_attack"
    neurorights_violation      = "neurorights_violation"
    cognitive_inequality_crisis = "cognitive_inequality_crisis"
    military_neuroweapon       = "military_neuroweapon"


class NeuralSeverity(str, Enum):
    neural_safe      = "neural_safe"
    neural_concern   = "neural_concern"
    high_neural_risk = "high_neural_risk"
    neural_emergency = "neural_emergency"


class NeuralAction(str, Enum):
    no_action                       = "no_action"
    neural_monitoring               = "neural_monitoring"
    neurorights_protection_program  = "neurorights_protection_program"
    neural_security_lockdown        = "neural_security_lockdown"
    neural_emergency_shutdown       = "neural_emergency_shutdown"


@dataclass
class NeuromorphicBCIInput:
    entity_id: str
    technology_type: str   # consumer_bci / medical_implant / military_bci / research_bci
    region: str
    # Risk fields (0.0–1.0); higher = worse unless noted
    neural_signal_fidelity: float           # inverse: high = good
    cognitive_privacy_risk: float
    neural_manipulation_potential: float
    bci_security_vulnerability: float
    consciousness_data_extraction_risk: float
    neurorights_violation_index: float
    cognitive_enhancement_inequality: float
    neural_surveillance_risk: float
    brain_hacking_exposure: float
    regulatory_gap_index: float
    informed_consent_deficit: float
    neural_data_monetization_risk: float
    cognitive_dependency_risk: float
    neural_interface_reliability: float     # inverse: high = good
    biosafety_concern_index: float
    military_weaponization_risk: float
    societal_acceptance_gap: float


@dataclass
class NeuromorphicBCIResult:
    entity_id: str
    region: str
    technology_type: str
    neural_risk: str
    neural_pattern: str
    neural_severity: str
    recommended_action: str
    privacy_score: float
    security_score: float
    rights_score: float
    societal_score: float
    neural_composite: float
    is_neural_crisis: bool
    requires_neural_intervention: bool
    neural_signal: str

    def to_dict(self) -> Dict:
        return {
            "entity_id":                   self.entity_id,
            "region":                      self.region,
            "technology_type":             self.technology_type,
            "neural_risk":                 self.neural_risk,
            "neural_pattern":              self.neural_pattern,
            "neural_severity":             self.neural_severity,
            "recommended_action":          self.recommended_action,
            "privacy_score":               self.privacy_score,
            "security_score":              self.security_score,
            "rights_score":                self.rights_score,
            "societal_score":              self.societal_score,
            "neural_composite":            self.neural_composite,
            "is_neural_crisis":            self.is_neural_crisis,
            "requires_neural_intervention": self.requires_neural_intervention,
            "neural_signal":               self.neural_signal,
        }


class NeuromorphicBCIEngine:
    def __init__(self) -> None:
        self._results: List[NeuromorphicBCIResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _privacy_score(self, i: NeuromorphicBCIInput) -> float:
        s = (
            i.cognitive_privacy_risk * 0.40
            + i.consciousness_data_extraction_risk * 0.35
            + i.neural_data_monetization_risk * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _security_score(self, i: NeuromorphicBCIInput) -> float:
        s = (
            i.bci_security_vulnerability * 0.40
            + i.brain_hacking_exposure * 0.35
            + i.neural_manipulation_potential * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _rights_score(self, i: NeuromorphicBCIInput) -> float:
        s = (
            i.neurorights_violation_index * 0.40
            + i.regulatory_gap_index * 0.35
            + i.informed_consent_deficit * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _societal_score(self, i: NeuromorphicBCIInput) -> float:
        s = (
            i.cognitive_enhancement_inequality * 0.40
            + i.military_weaponization_risk * 0.35
            + i.cognitive_dependency_risk * 0.25
        ) * 100
        return min(round(s, 2), 100.0)

    def _composite(
        self,
        priv: float,
        sec: float,
        rights: float,
        soc: float,
    ) -> float:
        return min(
            round(priv * 0.30 + sec * 0.25 + rights * 0.25 + soc * 0.20, 2),
            100.0,
        )

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> NeuralRisk:
        if c >= 60:
            return NeuralRisk.critical
        if c >= 40:
            return NeuralRisk.high
        if c >= 20:
            return NeuralRisk.moderate
        return NeuralRisk.low

    def _severity(self, c: float) -> NeuralSeverity:
        if c >= 75:
            return NeuralSeverity.neural_emergency
        if c >= 50:
            return NeuralSeverity.high_neural_risk
        if c >= 25:
            return NeuralSeverity.neural_concern
        return NeuralSeverity.neural_safe

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: NeuromorphicBCIInput) -> NeuralPattern:
        if i.cognitive_privacy_risk >= 0.70 and i.consciousness_data_extraction_risk >= 0.65:
            return NeuralPattern.neural_sovereignty_breach
        if i.brain_hacking_exposure >= 0.70 and i.bci_security_vulnerability >= 0.65:
            return NeuralPattern.brain_hacking_attack
        if i.neurorights_violation_index >= 0.70 and i.regulatory_gap_index >= 0.65:
            return NeuralPattern.neurorights_violation
        if i.cognitive_enhancement_inequality >= 0.70 and i.informed_consent_deficit >= 0.60:
            return NeuralPattern.cognitive_inequality_crisis
        if i.military_weaponization_risk >= 0.70 and i.neural_manipulation_potential >= 0.65:
            return NeuralPattern.military_neuroweapon
        return NeuralPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: NeuralRisk, pat: NeuralPattern) -> NeuralAction:
        if risk == NeuralRisk.critical:
            return NeuralAction.neural_emergency_shutdown
        if risk == NeuralRisk.high:
            if pat == NeuralPattern.brain_hacking_attack:
                return NeuralAction.neural_security_lockdown
            return NeuralAction.neurorights_protection_program
        if risk == NeuralRisk.moderate:
            return NeuralAction.neural_monitoring
        return NeuralAction.no_action

    # ------------------------------------------------------------------ #
    #  Neural signal (French)                                              #
    # ------------------------------------------------------------------ #

    def _signal(
        self,
        i: NeuromorphicBCIInput,
        pat: NeuralPattern,
        comp: float,
    ) -> str:
        if comp < 20:
            return (
                "Interface neuronale sécurisée — intégrité du signal neural confirmée, "
                "droits neuraux respectés, aucune menace détectée"
            )
        labels: Dict[NeuralPattern, str] = {
            NeuralPattern.neural_sovereignty_breach:   "Violation souveraineté neurale",
            NeuralPattern.brain_hacking_attack:        "Attaque de piratage cérébral",
            NeuralPattern.neurorights_violation:       "Violation des neurodroits",
            NeuralPattern.cognitive_inequality_crisis: "Crise d'inégalité cognitive",
            NeuralPattern.military_neuroweapon:        "Neuroarme militaire détectée",
            NeuralPattern.none:                        "Aucun pattern critique",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — vie privée neurale {i.cognitive_privacy_risk:.2f}"
            f" — vulnérabilité BCI {i.bci_security_vulnerability:.2f}"
            f" — index neurodroits {i.neurorights_violation_index:.2f}"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def _analyze_one(self, i: NeuromorphicBCIInput) -> NeuromorphicBCIResult:
        priv   = self._privacy_score(i)
        sec    = self._security_score(i)
        rights = self._rights_score(i)
        soc    = self._societal_score(i)
        comp   = self._composite(priv, sec, rights, soc)
        risk   = self._risk(comp)
        sev    = self._severity(comp)
        pat    = self._pattern(i)
        act    = self._action(risk, pat)
        result = NeuromorphicBCIResult(
            entity_id=i.entity_id,
            region=i.region,
            technology_type=i.technology_type,
            neural_risk=risk.value,
            neural_pattern=pat.value,
            neural_severity=sev.value,
            recommended_action=act.value,
            privacy_score=priv,
            security_score=sec,
            rights_score=rights,
            societal_score=soc,
            neural_composite=comp,
            is_neural_crisis=comp >= 60,
            requires_neural_intervention=comp >= 40,
            neural_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def analyze(self, entities: List[NeuromorphicBCIInput]) -> Dict:
        results = [self._analyze_one(e) for e in entities]

        if not results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_neural_composite": 0.0,
                "neural_crisis_count": 0,
                "neural_intervention_count": 0,
                "avg_privacy_score": 0.0,
                "avg_security_score": 0.0,
                "avg_rights_score": 0.0,
                "avg_societal_score": 0.0,
                "avg_estimated_neural_risk_index": 0.0,
                "entities": [],
            }

        n = len(results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        t_priv = t_sec = t_rights = t_soc = t_comp = 0.0
        crisis_count = intervention_count = 0

        for r in results:
            rc[r.neural_risk]        = rc.get(r.neural_risk, 0)        + 1
            pc[r.neural_pattern]     = pc.get(r.neural_pattern, 0)     + 1
            sc[r.neural_severity]    = sc.get(r.neural_severity, 0)    + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            t_priv  += r.privacy_score
            t_sec   += r.security_score
            t_rights += r.rights_score
            t_soc   += r.societal_score
            t_comp  += r.neural_composite
            if r.is_neural_crisis:            crisis_count        += 1
            if r.requires_neural_intervention: intervention_count += 1

        avg_comp = t_comp / n
        return {
            "total":                            n,
            "risk_counts":                      rc,
            "pattern_counts":                   pc,
            "severity_counts":                  sc,
            "action_counts":                    ac,
            "avg_neural_composite":             round(avg_comp, 1),
            "neural_crisis_count":              crisis_count,
            "neural_intervention_count":        intervention_count,
            "avg_privacy_score":                round(t_priv / n, 1),
            "avg_security_score":               round(t_sec / n, 1),
            "avg_rights_score":                 round(t_rights / n, 1),
            "avg_societal_score":               round(t_soc / n, 1),
            "avg_estimated_neural_risk_index":  round(avg_comp / 100 * 10, 2),
            "entities":                         [r.to_dict() for r in results],
        }
