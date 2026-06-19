"""
Module 254 — Bio-Computational Intelligence & Digital Organoid Simulation Engine
Simulates biological computing systems — digital organoids, neural tissue emulation,
synthetic biology circuits, DNA computing nodes — monitoring computational viability,
bio-stability, emergence patterns, and cross-substrate compatibility.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class BioRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class BioPattern(str, Enum):
    none                    = "none"
    biological_collapse     = "biological_collapse"
    computational_drift     = "computational_drift"
    mutation_cascade        = "mutation_cascade"
    substrate_incompatibility = "substrate_incompatibility"
    emergence_suppression   = "emergence_suppression"


class BioSeverity(str, Enum):
    thriving   = "thriving"
    adapting   = "adapting"
    degrading  = "degrading"
    collapsing = "collapsing"


class BioAction(str, Enum):
    no_action               = "no_action"
    viability_monitoring    = "viability_monitoring"
    bio_circuit_reset       = "bio_circuit_reset"
    mutation_containment    = "mutation_containment"
    emergency_stabilization = "emergency_stabilization"
    substrate_isolation     = "substrate_isolation"


@dataclass
class BioComputInput:
    organoid_id: str
    substrate_type: str   # neural_organoid/dna_circuit/synthetic_synapse/mycelium_network/
                          # protein_computer/quantum_bio/membrane_processor/hybrid_wetware
    region: str
    viability_score: float               # 0-1
    computational_coherence: float       # 0-1
    biological_stability_rate: float     # 0-1
    emergence_complexity_index: float    # 0-1
    substrate_efficiency_score: float    # 0-1
    mutation_drift_rate: float           # 0-1, higher=worse
    cross_substrate_compatibility: float # 0-1
    signal_propagation_fidelity: float   # 0-1
    metabolic_overhead_ratio: float      # 0-1, higher=worse
    self_repair_capacity: float          # 0-1
    information_density_score: float     # 0-1
    temporal_resolution_score: float     # 0-1
    noise_tolerance_level: float         # 0-1
    bio_digital_interface_quality: float # 0-1
    replication_accuracy: float          # 0-1
    environmental_sensitivity: float     # 0-1, higher=more fragile
    evolutionary_adaptability: float     # 0-1


@dataclass
class BioComputResult:
    organoid_id: str
    substrate_type: str
    region: str
    bio_risk: str
    bio_pattern: str
    bio_severity: str
    recommended_action: str
    viability_sub_score: float
    computation_sub_score: float
    stability_sub_score: float
    emergence_sub_score: float
    bio_composite: float
    critical_collapse_risk: bool
    requires_emergency: bool
    estimated_collapse_index: float
    bio_signal: str

    def to_dict(self) -> Dict:
        return {
            "organoid_id":             self.organoid_id,
            "substrate_type":          self.substrate_type,
            "region":                  self.region,
            "bio_risk":                self.bio_risk,
            "bio_pattern":             self.bio_pattern,
            "bio_severity":            self.bio_severity,
            "recommended_action":      self.recommended_action,
            "viability_sub_score":     self.viability_sub_score,
            "computation_sub_score":   self.computation_sub_score,
            "stability_sub_score":     self.stability_sub_score,
            "emergence_sub_score":     self.emergence_sub_score,
            "bio_composite":           self.bio_composite,
            "critical_collapse_risk":  self.critical_collapse_risk,
            "requires_emergency":      self.requires_emergency,
            "estimated_collapse_index": self.estimated_collapse_index,
        }


class BioComputationalIntelligenceEngine:
    def __init__(self) -> None:
        self._results: List[BioComputResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100, capped)                                          #
    # ------------------------------------------------------------------ #

    def _viability_score(self, i: BioComputInput) -> float:
        raw = (i.viability_score + i.biological_stability_rate + i.self_repair_capacity) / 3
        return min(round((1 - raw) * 100, 2), 100.0)

    def _computation_score(self, i: BioComputInput) -> float:
        raw = (i.computational_coherence + i.information_density_score + i.signal_propagation_fidelity) / 3
        return min(round((1 - raw) * 100, 2), 100.0)

    def _stability_score(self, i: BioComputInput) -> float:
        # mutation_drift_rate and environmental_sensitivity are already "higher=worse"
        # replication_accuracy is "higher=better" so invert it
        raw = (i.mutation_drift_rate + i.environmental_sensitivity + (1 - i.replication_accuracy)) / 3
        return min(round(raw * 100, 2), 100.0)

    def _emergence_score(self, i: BioComputInput) -> float:
        raw = (i.emergence_complexity_index + i.evolutionary_adaptability + i.cross_substrate_compatibility) / 3
        return min(round((1 - raw) * 100, 2), 100.0)

    def _composite(self, v: float, c: float, s: float, e: float) -> float:
        return min(round(v * 0.30 + c * 0.25 + s * 0.25 + e * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, comp: float) -> BioRisk:
        if comp >= 60: return BioRisk.critical
        if comp >= 40: return BioRisk.high
        if comp >= 20: return BioRisk.moderate
        return BioRisk.low

    def _severity(self, comp: float) -> BioSeverity:
        if comp >= 60: return BioSeverity.collapsing
        if comp >= 40: return BioSeverity.degrading
        if comp >= 20: return BioSeverity.adapting
        return BioSeverity.thriving

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: BioComputInput) -> BioPattern:
        if i.viability_score <= 0.30 and i.biological_stability_rate <= 0.30:
            return BioPattern.biological_collapse
        if i.computational_coherence <= 0.35 or i.signal_propagation_fidelity <= 0.35:
            return BioPattern.computational_drift
        if i.mutation_drift_rate >= 0.65 or i.replication_accuracy <= 0.35:
            return BioPattern.mutation_cascade
        if i.cross_substrate_compatibility <= 0.35 and i.substrate_efficiency_score <= 0.35:
            return BioPattern.substrate_incompatibility
        if i.emergence_complexity_index <= 0.30 and i.evolutionary_adaptability <= 0.30:
            return BioPattern.emergence_suppression
        return BioPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: BioRisk, pat: BioPattern) -> BioAction:
        if risk == BioRisk.critical:
            if pat == BioPattern.biological_collapse: return BioAction.emergency_stabilization
            return BioAction.substrate_isolation
        if risk == BioRisk.high:
            if pat == BioPattern.mutation_cascade:        return BioAction.mutation_containment
            if pat == BioPattern.substrate_incompatibility: return BioAction.bio_circuit_reset
            return BioAction.bio_circuit_reset
        if risk == BioRisk.moderate:
            return BioAction.viability_monitoring
        return BioAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived indices & signals                                           #
    # ------------------------------------------------------------------ #

    def _collapse_index(self, i: BioComputInput, comp: float) -> float:
        return round(min(comp / 100 * (i.mutation_drift_rate + i.environmental_sensitivity) / 2 * 10, 10.0), 2)

    def _signal(self, i: BioComputInput, pat: BioPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Organoïde bio-computationnel stable — viabilité confirmée, "
                "cohérence maximale, émergence contrôlée"
            )
        labels = {
            BioPattern.biological_collapse:      "Effondrement biologique",
            BioPattern.computational_drift:      "Dérive computationnelle",
            BioPattern.mutation_cascade:         "Cascade mutationnelle",
            BioPattern.substrate_incompatibility: "Incompatibilité substrat",
            BioPattern.emergence_suppression:    "Suppression d'émergence",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — viabilité {i.viability_score:.2f}"
            f" — cohérence {i.computational_coherence:.2f}"
            f" — dérive mutation {i.mutation_drift_rate:.2f}"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: BioComputInput) -> BioComputResult:
        vs   = self._viability_score(i)
        cs   = self._computation_score(i)
        ss   = self._stability_score(i)
        es   = self._emergence_score(i)
        comp = self._composite(vs, cs, ss, es)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = BioComputResult(
            organoid_id=i.organoid_id,
            substrate_type=i.substrate_type,
            region=i.region,
            bio_risk=risk.value,
            bio_pattern=pat.value,
            bio_severity=sev.value,
            recommended_action=act.value,
            viability_sub_score=vs,
            computation_sub_score=cs,
            stability_sub_score=ss,
            emergence_sub_score=es,
            bio_composite=comp,
            critical_collapse_risk=(risk == BioRisk.critical),
            requires_emergency=(act in (BioAction.emergency_stabilization, BioAction.substrate_isolation)),
            estimated_collapse_index=self._collapse_index(i, comp),
            bio_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[BioComputInput]) -> List[BioComputResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_bio_composite": 0.0,
                "critical_collapse_count": 0,
                "emergency_count": 0,
                "avg_viability_score": 0.0,
                "avg_computation_score": 0.0,
                "avg_stability_score": 0.0,
                "avg_emergence_score": 0.0,
                "avg_estimated_collapse_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tv = tc = ts = te = tcomp = tci = 0.0
        collapse_count = emergency_count = 0
        for r in self._results:
            rc[r.bio_risk]          = rc.get(r.bio_risk, 0)          + 1
            pc[r.bio_pattern]       = pc.get(r.bio_pattern, 0)       + 1
            sc[r.bio_severity]      = sc.get(r.bio_severity, 0)      + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tv    += r.viability_sub_score
            tc    += r.computation_sub_score
            ts    += r.stability_sub_score
            te    += r.emergence_sub_score
            tcomp += r.bio_composite
            tci   += r.estimated_collapse_index
            if r.critical_collapse_risk: collapse_count  += 1
            if r.requires_emergency:     emergency_count += 1
        return {
            "total":                       n,
            "risk_counts":                 rc,
            "pattern_counts":              pc,
            "severity_counts":             sc,
            "action_counts":               ac,
            "avg_bio_composite":           round(tcomp / n, 1),
            "critical_collapse_count":     collapse_count,
            "emergency_count":             emergency_count,
            "avg_viability_score":         round(tv / n, 1),
            "avg_computation_score":       round(tc / n, 1),
            "avg_stability_score":         round(ts / n, 1),
            "avg_emergence_score":         round(te / n, 1),
            "avg_estimated_collapse_index": round(tci / n, 2),
        }


# ------------------------------------------------------------------ #
#  Mock data                                                           #
# ------------------------------------------------------------------ #

MOCK_ORGANOIDS = [
    # OR-001 neural_organoid EMEA — critical/biological_collapse
    BioComputInput("OR-001","neural_organoid","EMEA",
        viability_score=0.12, computational_coherence=0.20, biological_stability_rate=0.15,
        emergence_complexity_index=0.22, substrate_efficiency_score=0.18,
        mutation_drift_rate=0.80, cross_substrate_compatibility=0.20,
        signal_propagation_fidelity=0.18, metabolic_overhead_ratio=0.85,
        self_repair_capacity=0.10, information_density_score=0.15,
        temporal_resolution_score=0.20, noise_tolerance_level=0.18,
        bio_digital_interface_quality=0.12, replication_accuracy=0.15,
        environmental_sensitivity=0.88, evolutionary_adaptability=0.12),
    # OR-002 dna_circuit NAMER — low
    BioComputInput("OR-002","dna_circuit","NAMER",
        viability_score=0.92, computational_coherence=0.90, biological_stability_rate=0.88,
        emergence_complexity_index=0.85, substrate_efficiency_score=0.90,
        mutation_drift_rate=0.08, cross_substrate_compatibility=0.88,
        signal_propagation_fidelity=0.92, metabolic_overhead_ratio=0.10,
        self_repair_capacity=0.90, information_density_score=0.88,
        temporal_resolution_score=0.92, noise_tolerance_level=0.90,
        bio_digital_interface_quality=0.88, replication_accuracy=0.95,
        environmental_sensitivity=0.08, evolutionary_adaptability=0.90),
    # OR-003 synthetic_synapse APAC — high/computational_drift
    BioComputInput("OR-003","synthetic_synapse","APAC",
        viability_score=0.55, computational_coherence=0.28, biological_stability_rate=0.52,
        emergence_complexity_index=0.48, substrate_efficiency_score=0.45,
        mutation_drift_rate=0.52, cross_substrate_compatibility=0.50,
        signal_propagation_fidelity=0.30, metabolic_overhead_ratio=0.58,
        self_repair_capacity=0.48, information_density_score=0.32,
        temporal_resolution_score=0.45, noise_tolerance_level=0.42,
        bio_digital_interface_quality=0.40, replication_accuracy=0.55,
        environmental_sensitivity=0.58, evolutionary_adaptability=0.45),
    # OR-004 mycelium_network LATAM — low
    BioComputInput("OR-004","mycelium_network","LATAM",
        viability_score=0.85, computational_coherence=0.82, biological_stability_rate=0.88,
        emergence_complexity_index=0.80, substrate_efficiency_score=0.85,
        mutation_drift_rate=0.12, cross_substrate_compatibility=0.82,
        signal_propagation_fidelity=0.85, metabolic_overhead_ratio=0.15,
        self_repair_capacity=0.88, information_density_score=0.80,
        temporal_resolution_score=0.85, noise_tolerance_level=0.88,
        bio_digital_interface_quality=0.80, replication_accuracy=0.90,
        environmental_sensitivity=0.12, evolutionary_adaptability=0.85),
    # OR-005 protein_computer EMEA — critical/mutation_cascade
    BioComputInput("OR-005","protein_computer","EMEA",
        viability_score=0.25, computational_coherence=0.30, biological_stability_rate=0.22,
        emergence_complexity_index=0.28, substrate_efficiency_score=0.20,
        mutation_drift_rate=0.82, cross_substrate_compatibility=0.25,
        signal_propagation_fidelity=0.28, metabolic_overhead_ratio=0.80,
        self_repair_capacity=0.18, information_density_score=0.25,
        temporal_resolution_score=0.28, noise_tolerance_level=0.22,
        bio_digital_interface_quality=0.20, replication_accuracy=0.20,
        environmental_sensitivity=0.82, evolutionary_adaptability=0.22),
    # OR-006 quantum_bio MEA — moderate
    BioComputInput("OR-006","quantum_bio","MEA",
        viability_score=0.62, computational_coherence=0.58, biological_stability_rate=0.60,
        emergence_complexity_index=0.55, substrate_efficiency_score=0.60,
        mutation_drift_rate=0.38, cross_substrate_compatibility=0.55,
        signal_propagation_fidelity=0.60, metabolic_overhead_ratio=0.42,
        self_repair_capacity=0.58, information_density_score=0.55,
        temporal_resolution_score=0.60, noise_tolerance_level=0.58,
        bio_digital_interface_quality=0.55, replication_accuracy=0.65,
        environmental_sensitivity=0.38, evolutionary_adaptability=0.58),
    # OR-007 membrane_processor NAMER — high/substrate_incompatibility
    BioComputInput("OR-007","membrane_processor","NAMER",
        viability_score=0.48, computational_coherence=0.50, biological_stability_rate=0.45,
        emergence_complexity_index=0.42, substrate_efficiency_score=0.28,
        mutation_drift_rate=0.55, cross_substrate_compatibility=0.28,
        signal_propagation_fidelity=0.50, metabolic_overhead_ratio=0.62,
        self_repair_capacity=0.42, information_density_score=0.45,
        temporal_resolution_score=0.48, noise_tolerance_level=0.40,
        bio_digital_interface_quality=0.38, replication_accuracy=0.48,
        environmental_sensitivity=0.58, evolutionary_adaptability=0.40),
    # OR-008 hybrid_wetware APAC — low
    BioComputInput("OR-008","hybrid_wetware","APAC",
        viability_score=0.88, computational_coherence=0.85, biological_stability_rate=0.90,
        emergence_complexity_index=0.82, substrate_efficiency_score=0.88,
        mutation_drift_rate=0.10, cross_substrate_compatibility=0.85,
        signal_propagation_fidelity=0.88, metabolic_overhead_ratio=0.12,
        self_repair_capacity=0.92, information_density_score=0.85,
        temporal_resolution_score=0.88, noise_tolerance_level=0.90,
        bio_digital_interface_quality=0.85, replication_accuracy=0.92,
        environmental_sensitivity=0.10, evolutionary_adaptability=0.88),
]
