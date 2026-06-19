"""
Module 247 — Cultural Chronology & Micro-Culture Simulation Engine
Simulates how micro-cultures evolve within organizations over time — tracking
cultural drift, generational shifts, tribal identities, narrative mutations,
and rituals to predict cultural cohesion or fragmentation.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class CulturalRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CulturalPattern(str, Enum):
    none                     = "none"
    tribal_fragmentation     = "tribal_fragmentation"
    narrative_drift          = "narrative_drift"
    ritual_erosion           = "ritual_erosion"
    generational_clash       = "generational_clash"
    identity_crisis          = "identity_crisis"


class CulturalSeverity(str, Enum):
    cohesive    = "cohesive"
    drifting    = "drifting"
    fragmented  = "fragmented"
    dissolved   = "dissolved"


class CulturalAction(str, Enum):
    no_action                        = "no_action"
    culture_pulse_monitoring         = "culture_pulse_monitoring"
    narrative_reinforcement          = "narrative_reinforcement"
    ritual_revival                   = "ritual_revival"
    generational_bridge_program      = "generational_bridge_program"
    tribe_mediation                  = "tribe_mediation"
    cultural_reset                   = "cultural_reset"
    emergency_culture_intervention   = "emergency_culture_intervention"


@dataclass
class CulturalInput:
    microculture_id: str
    cultural_cluster: str
    region: str
    cultural_cohesion_score: float
    shared_narrative_strength: float
    ritual_preservation_score: float
    generational_alignment: float
    tribal_identity_score: float
    value_drift_rate: float
    linguistic_convergence: float
    symbol_recognition_rate: float
    informal_network_strength: float
    myth_transmission_fidelity: float
    cultural_adoption_lag_days: int
    subculture_fragmentation_index: float
    psychological_safety_score: float
    counter_culture_intensity: float
    chronological_drift_score: float
    inter_tribe_communication_score: float
    cultural_resilience_score: float


@dataclass
class CulturalResult:
    microculture_id: str
    region: str
    cultural_risk: str
    cultural_pattern: str
    cultural_severity: str
    recommended_action: str
    cohesion_score: float
    narrative_score: float
    ritual_score: float
    resilience_score: float
    cultural_composite: float
    has_fragmentation_alert: bool
    requires_intervention: bool
    estimated_culture_dissolution_index: float
    cultural_signal: str

    def to_dict(self) -> Dict:
        return {
            "microculture_id":                      self.microculture_id,
            "region":                               self.region,
            "cultural_risk":                        self.cultural_risk,
            "cultural_pattern":                     self.cultural_pattern,
            "cultural_severity":                    self.cultural_severity,
            "recommended_action":                   self.recommended_action,
            "cohesion_score":                       self.cohesion_score,
            "narrative_score":                      self.narrative_score,
            "ritual_score":                         self.ritual_score,
            "resilience_score":                     self.resilience_score,
            "cultural_composite":                   self.cultural_composite,
            "has_fragmentation_alert":              self.has_fragmentation_alert,
            "requires_intervention":                self.requires_intervention,
            "estimated_culture_dissolution_index":  self.estimated_culture_dissolution_index,
            "cultural_signal":                      self.cultural_signal,
        }


class CulturalChronologyMicrocultureEngine:
    def __init__(self) -> None:
        self._results: List[CulturalResult] = []

    def _cohesion_score(self, i: CulturalInput) -> float:
        s = 0
        if   i.cultural_cohesion_score <= 0.30: s += 40
        elif i.cultural_cohesion_score <= 0.55: s += 22
        elif i.cultural_cohesion_score <= 0.70: s += 8

        if   i.tribal_identity_score >= 0.70: s += 35
        elif i.tribal_identity_score >= 0.45: s += 18
        elif i.tribal_identity_score >= 0.25: s += 6

        if   i.subculture_fragmentation_index >= 0.65: s += 25
        elif i.subculture_fragmentation_index >= 0.45: s += 12
        return min(s, 100)

    def _narrative_score(self, i: CulturalInput) -> float:
        s = 0
        if   i.shared_narrative_strength <= 0.25: s += 40
        elif i.shared_narrative_strength <= 0.50: s += 22
        elif i.shared_narrative_strength <= 0.70: s += 8

        if   i.value_drift_rate >= 0.70: s += 35
        elif i.value_drift_rate >= 0.45: s += 18
        elif i.value_drift_rate >= 0.20: s += 6

        if   i.myth_transmission_fidelity <= 0.30: s += 25
        elif i.myth_transmission_fidelity <= 0.55: s += 12
        return min(s, 100)

    def _ritual_score(self, i: CulturalInput) -> float:
        s = 0
        if   i.ritual_preservation_score <= 0.25: s += 40
        elif i.ritual_preservation_score <= 0.50: s += 22
        elif i.ritual_preservation_score <= 0.70: s += 8

        if   i.symbol_recognition_rate <= 0.30: s += 35
        elif i.symbol_recognition_rate <= 0.55: s += 18
        elif i.symbol_recognition_rate <= 0.75: s += 6

        if   i.chronological_drift_score >= 0.70: s += 25
        elif i.chronological_drift_score >= 0.45: s += 12
        return min(s, 100)

    def _resilience_score(self, i: CulturalInput) -> float:
        s = 0
        if   i.cultural_resilience_score <= 0.25: s += 40
        elif i.cultural_resilience_score <= 0.50: s += 22
        elif i.cultural_resilience_score <= 0.70: s += 8

        if   i.counter_culture_intensity >= 0.65: s += 35
        elif i.counter_culture_intensity >= 0.40: s += 18
        elif i.counter_culture_intensity >= 0.20: s += 6

        if   i.psychological_safety_score <= 0.30: s += 25
        elif i.psychological_safety_score <= 0.55: s += 12
        return min(s, 100)

    def _composite(self, coh: float, nar: float, rit: float, res: float) -> float:
        return min(round(coh * 0.30 + nar * 0.25 + rit * 0.25 + res * 0.20, 2), 100.0)

    def _risk(self, c: float) -> CulturalRisk:
        if c >= 60: return CulturalRisk.critical
        if c >= 40: return CulturalRisk.high
        if c >= 20: return CulturalRisk.moderate
        return CulturalRisk.low

    def _severity(self, c: float) -> CulturalSeverity:
        if c >= 60: return CulturalSeverity.dissolved
        if c >= 40: return CulturalSeverity.fragmented
        if c >= 20: return CulturalSeverity.drifting
        return CulturalSeverity.cohesive

    def _pattern(self, i: CulturalInput) -> CulturalPattern:
        if i.tribal_identity_score >= 0.55 or i.subculture_fragmentation_index >= 0.55:
            return CulturalPattern.tribal_fragmentation
        if i.shared_narrative_strength <= 0.35 and i.value_drift_rate >= 0.5:
            return CulturalPattern.narrative_drift
        if i.ritual_preservation_score <= 0.4 and i.symbol_recognition_rate <= 0.45:
            return CulturalPattern.ritual_erosion
        if i.generational_alignment <= 0.35 or i.cultural_adoption_lag_days >= 90:
            return CulturalPattern.generational_clash
        if i.chronological_drift_score >= 0.65 or i.counter_culture_intensity >= 0.6:
            return CulturalPattern.identity_crisis
        return CulturalPattern.none

    def _action(self, risk: CulturalRisk, pat: CulturalPattern) -> CulturalAction:
        if risk == CulturalRisk.critical:
            if pat == CulturalPattern.tribal_fragmentation:
                return CulturalAction.emergency_culture_intervention
            if pat == CulturalPattern.identity_crisis:
                return CulturalAction.cultural_reset
            return CulturalAction.tribe_mediation
        if risk == CulturalRisk.high:
            if pat == CulturalPattern.narrative_drift:
                return CulturalAction.narrative_reinforcement
            if pat == CulturalPattern.ritual_erosion:
                return CulturalAction.ritual_revival
            if pat == CulturalPattern.generational_clash:
                return CulturalAction.generational_bridge_program
            if pat == CulturalPattern.tribal_fragmentation:
                return CulturalAction.tribe_mediation
            return CulturalAction.culture_pulse_monitoring
        if risk == CulturalRisk.moderate:
            return CulturalAction.culture_pulse_monitoring
        return CulturalAction.no_action

    def _has_fragmentation_alert(self, i: CulturalInput, comp: float) -> bool:
        return (
            comp >= 40
            or i.tribal_identity_score >= 0.5
            or i.counter_culture_intensity >= 0.55
            or i.subculture_fragmentation_index >= 0.5
        )

    def _requires_intervention(self, i: CulturalInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.cultural_cohesion_score <= 0.35
            or i.value_drift_rate >= 0.65
        )

    def _dissolution_index(self, i: CulturalInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.cultural_resilience_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: CulturalInput, pat: CulturalPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Micro-culture cohésive — narrations partagées, rituels vivants, "
                "générations alignées, identité forte"
            )
        labels: Dict[CulturalPattern, str] = {
            CulturalPattern.tribal_fragmentation: "Fragmentation tribale",
            CulturalPattern.narrative_drift:      "Dérive narrative",
            CulturalPattern.ritual_erosion:       "Érosion rituelle",
            CulturalPattern.generational_clash:   "Choc générationnel",
            CulturalPattern.identity_crisis:      "Crise identitaire",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — "
            f"cohésion {round(i.cultural_cohesion_score * 100)}% — "
            f"dérive valeurs {round(i.value_drift_rate * 100)}% — "
            f"tribalisme {round(i.tribal_identity_score * 100)}% — "
            f"composite {round(comp)}"
        )

    def assess(self, i: CulturalInput) -> CulturalResult:
        coh  = self._cohesion_score(i)
        nar  = self._narrative_score(i)
        rit  = self._ritual_score(i)
        res  = self._resilience_score(i)
        comp = self._composite(coh, nar, rit, res)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = CulturalResult(
            microculture_id=i.microculture_id,
            region=i.region,
            cultural_risk=risk.value,
            cultural_pattern=pat.value,
            cultural_severity=sev.value,
            recommended_action=act.value,
            cohesion_score=coh,
            narrative_score=nar,
            ritual_score=rit,
            resilience_score=res,
            cultural_composite=comp,
            has_fragmentation_alert=self._has_fragmentation_alert(i, comp),
            requires_intervention=self._requires_intervention(i, comp),
            estimated_culture_dissolution_index=self._dissolution_index(i, comp),
            cultural_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[CulturalInput]) -> List[CulturalResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total":                                    0,
                "risk_counts":                              {},
                "pattern_counts":                           {},
                "severity_counts":                          {},
                "action_counts":                            {},
                "avg_cultural_composite":                   0.0,
                "fragmentation_alert_count":                0,
                "intervention_count":                       0,
                "avg_cohesion_score":                       0.0,
                "avg_narrative_score":                      0.0,
                "avg_ritual_score":                         0.0,
                "avg_resilience_score":                     0.0,
                "avg_estimated_culture_dissolution_index":  0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tcoh = tnar = trit = tres = tcomp = tdiss = 0.0
        frag_c = interv_c = 0
        for r in self._results:
            rc[r.cultural_risk]        = rc.get(r.cultural_risk, 0)        + 1
            pc[r.cultural_pattern]     = pc.get(r.cultural_pattern, 0)     + 1
            sc[r.cultural_severity]    = sc.get(r.cultural_severity, 0)    + 1
            ac[r.recommended_action]   = ac.get(r.recommended_action, 0)   + 1
            tcoh  += r.cohesion_score
            tnar  += r.narrative_score
            trit  += r.ritual_score
            tres  += r.resilience_score
            tcomp += r.cultural_composite
            tdiss += r.estimated_culture_dissolution_index
            if r.has_fragmentation_alert: frag_c   += 1
            if r.requires_intervention:   interv_c += 1
        return {
            "total":                                    n,
            "risk_counts":                              rc,
            "pattern_counts":                           pc,
            "severity_counts":                          sc,
            "action_counts":                            ac,
            "avg_cultural_composite":                   round(tcomp / n, 1),
            "fragmentation_alert_count":                frag_c,
            "intervention_count":                       interv_c,
            "avg_cohesion_score":                       round(tcoh  / n, 1),
            "avg_narrative_score":                      round(tnar  / n, 1),
            "avg_ritual_score":                         round(trit  / n, 1),
            "avg_resilience_score":                     round(tres  / n, 1),
            "avg_estimated_culture_dissolution_index":  round(tdiss / n, 2),
        }


MOCK_INPUTS: List[CulturalInput] = [
    CulturalInput(
        microculture_id="MC-001", cultural_cluster="founding", region="EMEA",
        cultural_cohesion_score=0.85, shared_narrative_strength=0.88,
        ritual_preservation_score=0.82, generational_alignment=0.80,
        tribal_identity_score=0.10, value_drift_rate=0.08,
        linguistic_convergence=0.90, symbol_recognition_rate=0.87,
        informal_network_strength=0.82, myth_transmission_fidelity=0.89,
        cultural_adoption_lag_days=18, subculture_fragmentation_index=0.12,
        psychological_safety_score=0.88, counter_culture_intensity=0.07,
        chronological_drift_score=0.09, inter_tribe_communication_score=0.91,
        cultural_resilience_score=0.90,
    ),
    CulturalInput(
        microculture_id="MC-002", cultural_cluster="legacy", region="NAMER",
        cultural_cohesion_score=0.38, shared_narrative_strength=0.30,
        ritual_preservation_score=0.35, generational_alignment=0.28,
        tribal_identity_score=0.68, value_drift_rate=0.62,
        linguistic_convergence=0.40, symbol_recognition_rate=0.32,
        informal_network_strength=0.35, myth_transmission_fidelity=0.28,
        cultural_adoption_lag_days=105, subculture_fragmentation_index=0.72,
        psychological_safety_score=0.30, counter_culture_intensity=0.65,
        chronological_drift_score=0.70, inter_tribe_communication_score=0.25,
        cultural_resilience_score=0.22,
    ),
    CulturalInput(
        microculture_id="MC-003", cultural_cluster="growth", region="APAC",
        cultural_cohesion_score=0.55, shared_narrative_strength=0.48,
        ritual_preservation_score=0.50, generational_alignment=0.52,
        tribal_identity_score=0.42, value_drift_rate=0.38,
        linguistic_convergence=0.58, symbol_recognition_rate=0.50,
        informal_network_strength=0.55, myth_transmission_fidelity=0.50,
        cultural_adoption_lag_days=55, subculture_fragmentation_index=0.40,
        psychological_safety_score=0.58, counter_culture_intensity=0.35,
        chronological_drift_score=0.40, inter_tribe_communication_score=0.55,
        cultural_resilience_score=0.55,
    ),
    CulturalInput(
        microculture_id="MC-004", cultural_cluster="acquired", region="LATAM",
        cultural_cohesion_score=0.25, shared_narrative_strength=0.22,
        ritual_preservation_score=0.28, generational_alignment=0.32,
        tribal_identity_score=0.75, value_drift_rate=0.80,
        linguistic_convergence=0.25, symbol_recognition_rate=0.20,
        informal_network_strength=0.28, myth_transmission_fidelity=0.18,
        cultural_adoption_lag_days=130, subculture_fragmentation_index=0.80,
        psychological_safety_score=0.20, counter_culture_intensity=0.78,
        chronological_drift_score=0.82, inter_tribe_communication_score=0.15,
        cultural_resilience_score=0.15,
    ),
    CulturalInput(
        microculture_id="MC-005", cultural_cluster="remote", region="MEA",
        cultural_cohesion_score=0.45, shared_narrative_strength=0.40,
        ritual_preservation_score=0.38, generational_alignment=0.55,
        tribal_identity_score=0.50, value_drift_rate=0.55,
        linguistic_convergence=0.48, symbol_recognition_rate=0.40,
        informal_network_strength=0.42, myth_transmission_fidelity=0.42,
        cultural_adoption_lag_days=70, subculture_fragmentation_index=0.52,
        psychological_safety_score=0.48, counter_culture_intensity=0.50,
        chronological_drift_score=0.55, inter_tribe_communication_score=0.42,
        cultural_resilience_score=0.40,
    ),
    CulturalInput(
        microculture_id="MC-006", cultural_cluster="hybrid", region="EMEA",
        cultural_cohesion_score=0.62, shared_narrative_strength=0.60,
        ritual_preservation_score=0.65, generational_alignment=0.68,
        tribal_identity_score=0.22, value_drift_rate=0.25,
        linguistic_convergence=0.70, symbol_recognition_rate=0.65,
        informal_network_strength=0.68, myth_transmission_fidelity=0.62,
        cultural_adoption_lag_days=35, subculture_fragmentation_index=0.22,
        psychological_safety_score=0.72, counter_culture_intensity=0.18,
        chronological_drift_score=0.22, inter_tribe_communication_score=0.70,
        cultural_resilience_score=0.70,
    ),
    CulturalInput(
        microculture_id="MC-007", cultural_cluster="generational_z", region="NAMER",
        cultural_cohesion_score=0.48, shared_narrative_strength=0.50,
        ritual_preservation_score=0.42, generational_alignment=0.30,
        tribal_identity_score=0.45, value_drift_rate=0.48,
        linguistic_convergence=0.52, symbol_recognition_rate=0.45,
        informal_network_strength=0.50, myth_transmission_fidelity=0.48,
        cultural_adoption_lag_days=95, subculture_fragmentation_index=0.44,
        psychological_safety_score=0.55, counter_culture_intensity=0.40,
        chronological_drift_score=0.50, inter_tribe_communication_score=0.48,
        cultural_resilience_score=0.48,
    ),
    CulturalInput(
        microculture_id="MC-008", cultural_cluster="generational_x", region="APAC",
        cultural_cohesion_score=0.72, shared_narrative_strength=0.70,
        ritual_preservation_score=0.75, generational_alignment=0.70,
        tribal_identity_score=0.18, value_drift_rate=0.15,
        linguistic_convergence=0.78, symbol_recognition_rate=0.72,
        informal_network_strength=0.75, myth_transmission_fidelity=0.72,
        cultural_adoption_lag_days=28, subculture_fragmentation_index=0.15,
        psychological_safety_score=0.80, counter_culture_intensity=0.12,
        chronological_drift_score=0.15, inter_tribe_communication_score=0.82,
        cultural_resilience_score=0.78,
    ),
]
