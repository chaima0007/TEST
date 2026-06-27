from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CivilizationalMemoryInput:
    entity_id: str
    heritage_category: str
    region: str
    # 17 float fields (0.0–1.0)
    memory_preservation_rate: float
    cultural_transmission_fidelity: float
    knowledge_erosion_rate: float
    digital_archival_completeness: float
    intergenerational_transfer: float
    linguistic_vitality: float
    oral_tradition_preservation: float
    artifact_integrity: float
    collective_identity_coherence: float
    cultural_innovation_rate: float
    heritage_monetization_potential: float
    diaspora_network_strength: float
    institutional_fragility: float
    memory_distortion_rate: float
    cultural_resilience: float
    knowledge_accessibility: float
    narrative_coherence: float


@dataclass
class CivilizationalMemoryResult:
    entity_id: str
    region: str
    heritage_category: str
    memory_risk: str
    memory_pattern: str
    memory_severity: str
    recommended_action: str
    preservation_score: float
    transmission_score: float
    identity_score: float
    resilience_score: float
    memory_composite: float
    is_in_memory_crisis: bool
    requires_heritage_intervention: bool
    memory_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id":                    self.entity_id,
            "region":                       self.region,
            "heritage_category":            self.heritage_category,
            "memory_risk":                  self.memory_risk,
            "memory_pattern":               self.memory_pattern,
            "memory_severity":              self.memory_severity,
            "recommended_action":           self.recommended_action,
            "preservation_score":           self.preservation_score,
            "transmission_score":           self.transmission_score,
            "identity_score":               self.identity_score,
            "resilience_score":             self.resilience_score,
            "memory_composite":             self.memory_composite,
            "is_in_memory_crisis":          self.is_in_memory_crisis,
            "requires_heritage_intervention": self.requires_heritage_intervention,
            "memory_signal":                self.memory_signal,
        }


def _preservation_score(e: CivilizationalMemoryInput) -> float:
    """0.30 weight — higher = worse risk"""
    raw = (
        e.knowledge_erosion_rate * 0.4
        + e.memory_distortion_rate * 0.3
        + (1 - e.memory_preservation_rate) * 0.3
    ) * 100
    return round(raw, 2)


def _transmission_score(e: CivilizationalMemoryInput) -> float:
    """0.25 weight — inverted: low transmission = high risk"""
    raw = (
        (1 - e.cultural_transmission_fidelity) * 0.4
        + (1 - e.intergenerational_transfer) * 0.35
        + (1 - e.oral_tradition_preservation) * 0.25
    ) * 100
    return round(raw, 2)


def _identity_score(e: CivilizationalMemoryInput) -> float:
    """0.25 weight — inverted: low identity coherence = high risk"""
    raw = (
        (1 - e.collective_identity_coherence) * 0.4
        + (1 - e.linguistic_vitality) * 0.35
        + (1 - e.narrative_coherence) * 0.25
    ) * 100
    return round(raw, 2)


def _resilience_score(e: CivilizationalMemoryInput) -> float:
    """0.20 weight — inverted: low resilience = high risk"""
    raw = (
        (1 - e.cultural_resilience) * 0.4
        + e.institutional_fragility * 0.35
        + (1 - e.knowledge_accessibility) * 0.25
    ) * 100
    return round(raw, 2)


def _composite(pres: float, trans: float, ident: float, resil: float) -> float:
    return round(pres * 0.30 + trans * 0.25 + ident * 0.25 + resil * 0.20, 2)


def _risk_level(comp: float) -> str:
    if comp >= 60: return "critical"
    if comp >= 40: return "high"
    if comp >= 20: return "moderate"
    return "low"


def _pattern(e: CivilizationalMemoryInput) -> str:
    if e.knowledge_erosion_rate >= 0.65 and (1 - e.memory_preservation_rate) >= 0.55:
        return "civilizational_amnesia"
    if (1 - e.collective_identity_coherence) >= 0.65 and (1 - e.narrative_coherence) >= 0.55:
        return "cultural_fragmentation"
    if (1 - e.intergenerational_transfer) >= 0.65 and (1 - e.cultural_transmission_fidelity) >= 0.55:
        return "transmission_collapse"
    if (1 - e.linguistic_vitality) >= 0.70:
        return "linguistic_extinction"
    if e.heritage_monetization_potential >= 0.70 and (1 - e.artifact_integrity) >= 0.55:
        return "heritage_commodification_risk"
    return "none"


def _severity(comp: float) -> str:
    if comp >= 75: return "civilizational_crisis"
    if comp >= 50: return "high_erosion"
    if comp >= 25: return "developing_loss"
    return "vibrant_heritage"


def _action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "civilizational_emergency"
    if risk == "high":
        if pattern == "civilizational_amnesia":
            return "emergency_archival"
        return "cultural_preservation_program"
    if risk == "moderate":
        return "heritage_monitoring"
    return "no_action"


def _signal(e: CivilizationalMemoryInput, risk: str, comp: float) -> str:
    if risk == "critical":
        return (
            f"Critique — préservation mémoire {int(e.memory_preservation_rate * 100)}% "
            f"— transmission culturelle {int(e.cultural_transmission_fidelity * 100)}% "
            f"— composite {int(comp)}"
        )
    if risk == "high":
        return (
            f"Élevé — vitalité linguistique {int(e.linguistic_vitality * 100)}% "
            f"— cohérence identitaire {int(e.collective_identity_coherence * 100)}% "
            f"— composite {int(comp)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — taux d'érosion {int(e.knowledge_erosion_rate * 100)}% "
            f"— composite {int(comp)}"
        )
    return "Mémoire civilisationnelle préservée — transmission culturelle forte, identité collective cohérente"


def _assess(e: CivilizationalMemoryInput) -> CivilizationalMemoryResult:
    pres  = _preservation_score(e)
    trans = _transmission_score(e)
    ident = _identity_score(e)
    resil = _resilience_score(e)
    comp  = _composite(pres, trans, ident, resil)
    pat   = _pattern(e)
    risk  = _risk_level(comp)
    sev   = _severity(comp)
    act   = _action(risk, pat)
    sig   = _signal(e, risk, comp)
    return CivilizationalMemoryResult(
        entity_id=e.entity_id,
        region=e.region,
        heritage_category=e.heritage_category,
        memory_risk=risk,
        memory_pattern=pat,
        memory_severity=sev,
        recommended_action=act,
        preservation_score=pres,
        transmission_score=trans,
        identity_score=ident,
        resilience_score=resil,
        memory_composite=comp,
        is_in_memory_crisis=comp >= 60,
        requires_heritage_intervention=comp >= 40,
        memory_signal=sig,
    )


class CivilizationalMemoryEngine:
    def __init__(self, entities: List[CivilizationalMemoryInput]):
        self.entities = entities
        self._results: List[CivilizationalMemoryResult] = []

    def assess_batch(self) -> List[CivilizationalMemoryResult]:
        self._results = [_assess(e) for e in self.entities]
        return self._results

    def summary(self) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        if not self._results:
            self.assess_batch()
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        t_comp = t_pres = t_trans = t_ident = t_resil = 0.0
        crisis_c = intervention_c = 0
        for r in self._results:
            rc[r.memory_risk]        = rc.get(r.memory_risk, 0) + 1
            pc[r.memory_pattern]     = pc.get(r.memory_pattern, 0) + 1
            sc[r.memory_severity]    = sc.get(r.memory_severity, 0) + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            t_comp  += r.memory_composite
            t_pres  += r.preservation_score
            t_trans += r.transmission_score
            t_ident += r.identity_score
            t_resil += r.resilience_score
            if r.is_in_memory_crisis:          crisis_c += 1
            if r.requires_heritage_intervention: intervention_c += 1
        n = len(self._results)
        avg_comp = t_comp / n
        return {
            "total":                            n,
            "risk_counts":                      rc,
            "pattern_counts":                   pc,
            "severity_counts":                  sc,
            "action_counts":                    ac,
            "avg_memory_composite":             round(avg_comp, 1),
            "memory_crisis_count":              crisis_c,
            "heritage_intervention_count":      intervention_c,
            "avg_preservation_score":           round(t_pres / n, 1),
            "avg_transmission_score":           round(t_trans / n, 1),
            "avg_identity_score":               round(t_ident / n, 1),
            "avg_resilience_score":             round(t_resil / n, 1),
            "avg_estimated_memory_loss_index":  round(avg_comp / 100 * 10, 2),
        }
