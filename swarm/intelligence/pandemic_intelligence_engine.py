"""
Module 325 — Pandemic Intelligence & Global Biosurveillance Engine
Caelum Partners — Surveillance pandémique, biosurveillance mondiale et gestion des crises épidémiques.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class PandemicIntelligenceInput:
    entity_id: str
    pathogen_category: str
    region: str
    # 17 float fields (0.0-1.0)
    transmission_velocity: float
    case_fatality_escalation_risk: float
    healthcare_capacity_saturation: float
    genomic_variant_emergence_rate: float
    vaccine_efficacy_erosion: float
    surveillance_gap_index: float
    cross_border_spread_velocity: float
    pandemic_preparedness_deficit: float
    zoonotic_spillover_risk: float
    antimicrobial_resistance_amplification: float
    supply_chain_medical_fragility: float
    public_health_compliance_erosion: float
    long_covid_economic_burden: float
    variant_immune_evasion_potential: float
    healthcare_worker_attrition: float
    global_health_governance_gap: float
    digital_health_surveillance_coverage: float  # inverse: high = good


@dataclass
class PandemicIntelligenceResult:
    entity_id: str
    region: str
    pathogen_category: str
    pandemic_risk: str
    pandemic_pattern: str
    pandemic_severity: str
    recommended_action: str
    transmission_score: float
    severity_score: float
    preparedness_score: float
    systemic_score: float
    pandemic_composite: float
    is_pandemic_crisis: bool
    requires_pandemic_intervention: bool
    pandemic_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id":                      self.entity_id,
            "region":                         self.region,
            "pathogen_category":              self.pathogen_category,
            "pandemic_risk":                  self.pandemic_risk,
            "pandemic_pattern":               self.pandemic_pattern,
            "pandemic_severity":              self.pandemic_severity,
            "recommended_action":             self.recommended_action,
            "transmission_score":             self.transmission_score,
            "severity_score":                 self.severity_score,
            "preparedness_score":             self.preparedness_score,
            "systemic_score":                 self.systemic_score,
            "pandemic_composite":             self.pandemic_composite,
            "is_pandemic_crisis":             self.is_pandemic_crisis,
            "requires_pandemic_intervention": self.requires_pandemic_intervention,
            "pandemic_signal":                self.pandemic_signal,
        }


# ---------------------------------------------------------------------------
# Sub-score helpers
# ---------------------------------------------------------------------------

def _transmission_score(inp: PandemicIntelligenceInput) -> float:
    raw = (
        inp.transmission_velocity * 0.40
        + inp.cross_border_spread_velocity * 0.35
        + inp.variant_immune_evasion_potential * 0.25
    ) * 100
    return round(raw * 100) / 100


def _severity_score(inp: PandemicIntelligenceInput) -> float:
    raw = (
        inp.case_fatality_escalation_risk * 0.40
        + inp.healthcare_capacity_saturation * 0.35
        + inp.healthcare_worker_attrition * 0.25
    ) * 100
    return round(raw * 100) / 100


def _preparedness_score(inp: PandemicIntelligenceInput) -> float:
    raw = (
        inp.pandemic_preparedness_deficit * 0.40
        + inp.surveillance_gap_index * 0.35
        + (1 - inp.digital_health_surveillance_coverage) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _systemic_score(inp: PandemicIntelligenceInput) -> float:
    raw = (
        inp.antimicrobial_resistance_amplification * 0.40
        + inp.global_health_governance_gap * 0.35
        + inp.supply_chain_medical_fragility * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    transmission: float,
    severity: float,
    preparedness: float,
    systemic: float,
) -> float:
    return round(
        transmission * 0.30
        + severity * 0.25
        + preparedness * 0.25
        + systemic * 0.20,
        2,
    )


def _pandemic_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _pandemic_pattern(inp: PandemicIntelligenceInput) -> str:
    if inp.transmission_velocity >= 0.70 and inp.surveillance_gap_index >= 0.65:
        return "pandemic_emergence"
    if inp.variant_immune_evasion_potential >= 0.70 and inp.vaccine_efficacy_erosion >= 0.65:
        return "variant_escape_cascade"
    if inp.healthcare_capacity_saturation >= 0.70 and inp.healthcare_worker_attrition >= 0.65:
        return "healthcare_system_collapse"
    if inp.antimicrobial_resistance_amplification >= 0.70 and inp.pandemic_preparedness_deficit >= 0.65:
        return "amr_catastrophe"
    if inp.zoonotic_spillover_risk >= 0.70 and inp.genomic_variant_emergence_rate >= 0.65:
        return "zoonotic_explosion"
    return "none"


def _pandemic_severity(composite: float) -> str:
    if composite >= 75:
        return "pandemic_emergency"
    if composite >= 50:
        return "epidemic_crisis"
    if composite >= 25:
        return "outbreak_developing"
    return "containment_adequate"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "pandemic_emergency_response"
    if risk == "high" and pattern == "healthcare_system_collapse":
        return "surge_capacity_activation"
    if risk == "high":
        return "enhanced_surveillance"
    if risk == "moderate":
        return "outbreak_monitoring"
    return "no_action"


def _pandemic_signal(inp: PandemicIntelligenceInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — vélocité transmission {int(inp.transmission_velocity * 100)}% "
            f"— saturation capacité sanitaire {int(inp.healthcare_capacity_saturation * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — déficit préparation pandémique {int(inp.pandemic_preparedness_deficit * 100)}% "
            f"— résistance antimicrobiens {int(inp.antimicrobial_resistance_amplification * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — indice lacune surveillance {int(inp.surveillance_gap_index * 100)}% "
            f"— composite {int(composite)}"
        )
    return "Confinement adéquat — surveillance épidémique solide, capacité sanitaire préservée, préparation pandémique robuste"


def _analyze_one(inp: PandemicIntelligenceInput) -> PandemicIntelligenceResult:
    trans = _transmission_score(inp)
    sev   = _severity_score(inp)
    prep  = _preparedness_score(inp)
    syst  = _systemic_score(inp)
    comp  = _composite(trans, sev, prep, syst)
    risk  = _pandemic_risk(comp)
    pat   = _pandemic_pattern(inp)
    severity  = _pandemic_severity(comp)
    action    = _recommended_action(risk, pat)
    signal    = _pandemic_signal(inp, risk, comp)
    return PandemicIntelligenceResult(
        entity_id=inp.entity_id,
        region=inp.region,
        pathogen_category=inp.pathogen_category,
        pandemic_risk=risk,
        pandemic_pattern=pat,
        pandemic_severity=severity,
        recommended_action=action,
        transmission_score=trans,
        severity_score=sev,
        preparedness_score=prep,
        systemic_score=syst,
        pandemic_composite=comp,
        is_pandemic_crisis=comp >= 60,
        requires_pandemic_intervention=comp >= 40,
        pandemic_signal=signal,
    )


class PandemicIntelligenceEngine:
    """Module 325 — Pandemic Intelligence & Global Biosurveillance Engine."""

    def analyze(self, entities: List[PandemicIntelligenceInput]) -> Dict[str, Any]:
        results = [_analyze_one(inp) for inp in entities]
        n = len(results)

        risk_counts: Dict[str, int]     = {}
        pattern_counts: Dict[str, int]  = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int]   = {}

        total_trans = total_sev = total_prep = total_syst = total_comp = 0.0
        crisis_count = intervention_count = 0

        for r in results:
            risk_counts[r.pandemic_risk]         = risk_counts.get(r.pandemic_risk, 0) + 1
            pattern_counts[r.pandemic_pattern]   = pattern_counts.get(r.pandemic_pattern, 0) + 1
            severity_counts[r.pandemic_severity] = severity_counts.get(r.pandemic_severity, 0) + 1
            action_counts[r.recommended_action]  = action_counts.get(r.recommended_action, 0) + 1
            total_trans += r.transmission_score
            total_sev   += r.severity_score
            total_prep  += r.preparedness_score
            total_syst  += r.systemic_score
            total_comp  += r.pandemic_composite
            if r.is_pandemic_crisis:              crisis_count += 1
            if r.requires_pandemic_intervention:  intervention_count += 1

        avg_composite = total_comp / n if n else 0.0

        # Dominant pattern: most frequent non-none; else 'none'
        non_none = {k: v for k, v in pattern_counts.items() if k != "none"}
        dominant_pattern = max(non_none, key=lambda k: non_none[k]) if non_none else "none"

        # Highest risk entity: first critical, then high, moderate, low
        highest_risk_entity = ""
        for level in ("critical", "high", "moderate", "low"):
            for r in results:
                if r.pandemic_risk == level:
                    highest_risk_entity = r.entity_id
                    break
            if highest_risk_entity:
                break

        return {
            "total_entities_analyzed":              n,
            "critical_pandemic_risks":              risk_counts.get("critical", 0),
            "high_pandemic_risks":                  risk_counts.get("high", 0),
            "moderate_pandemic_risks":              risk_counts.get("moderate", 0),
            "low_pandemic_risks":                   risk_counts.get("low", 0),
            "pandemic_crises_detected":             crisis_count,
            "pandemic_interventions_required":      intervention_count,
            "dominant_pandemic_pattern":            dominant_pattern,
            "avg_estimated_pandemic_threat_index":  round(avg_composite / 100 * 10, 2),
            "highest_risk_entity":                  highest_risk_entity,
            "results":                              [r.to_dict() for r in results],
            "analysis_timestamp":                   datetime.now(timezone.utc).isoformat(),
            "engine_version":                       "325.0.0",
        }
