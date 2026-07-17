"""
Module 264 — Biomimetic Strategy & Evolutionary Adaptation Engine
Applies evolutionary biology and biomimetic principles to corporate strategy
adaptation — tracking adaptive mutation, environmental fitness, symbiotic
alliances, predator-prey dynamics, mycelial networks, camouflage strategies,
migration adaptation, and regenerative cycles. Provides evolutionary
recommendations for organisational survival and ecological dominance.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class BiomimeticRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class EvolutionaryPattern(str, Enum):
    none                   = "none"
    extinction_spiral      = "extinction_spiral"
    niche_collapse         = "niche_collapse"
    symbiosis_breakdown    = "symbiosis_breakdown"
    evolutionary_stagnation = "evolutionary_stagnation"
    territorial_loss       = "territorial_loss"


class BiomimeticSeverity(str, Enum):
    thriving    = "thriving"
    adapting    = "adapting"
    endangered  = "endangered"
    extinct_risk = "extinct_risk"


class BiomimeticAction(str, Enum):
    no_action                 = "no_action"
    evolution_monitoring      = "evolution_monitoring"
    symbiosis_forge           = "symbiosis_forge"
    adaptation_acceleration   = "adaptation_acceleration"
    evolutionary_pivot        = "evolutionary_pivot"
    niche_reconstruction      = "niche_reconstruction"


@dataclass
class BiometicInput:
    organism_id: str
    strategy_archetype: str
    region: str
    adaptive_mutation_rate: float
    environmental_fit_score: float
    competitive_selection_pressure: float
    symbiotic_partnership_depth: float
    resource_efficiency_ratio: float
    extinction_vulnerability: float
    niche_differentiation_score: float
    resilience_redundancy: float
    swarm_coordination_score: float
    phenotypic_plasticity: float
    territorial_defense_strength: float
    information_propagation_speed: float
    energy_metabolism_efficiency: float
    coevolution_readiness: float
    biodiversity_analog_score: float
    regeneration_capacity: float
    ecological_dominance_index: float


@dataclass
class BiomimeticResult:
    organism_id: str
    region: str
    biomimetic_risk: str
    evolutionary_pattern: str
    biomimetic_severity: str
    recommended_action: str
    fitness_score: float
    adaptation_score: float
    resilience_score: float
    synergy_score: float
    biomimetic_composite: float
    has_extinction_signal: bool
    requires_evolutionary_intervention: bool
    estimated_extinction_risk_index: float
    biomimetic_signal: str

    def to_dict(self) -> Dict:
        return {
            "organism_id":                          self.organism_id,
            "region":                               self.region,
            "biomimetic_risk":                      self.biomimetic_risk,
            "evolutionary_pattern":                 self.evolutionary_pattern,
            "biomimetic_severity":                  self.biomimetic_severity,
            "recommended_action":                   self.recommended_action,
            "fitness_score":                        self.fitness_score,
            "adaptation_score":                     self.adaptation_score,
            "resilience_score":                     self.resilience_score,
            "synergy_score":                        self.synergy_score,
            "biomimetic_composite":                 self.biomimetic_composite,
            "has_extinction_signal":                self.has_extinction_signal,
            "requires_evolutionary_intervention":   self.requires_evolutionary_intervention,
            "estimated_extinction_risk_index":      self.estimated_extinction_risk_index,
            "biomimetic_signal":                    self.biomimetic_signal,
        }


class BiomimeticStrategyEngine:
    def __init__(self) -> None:
        self._results: List[BiomimeticResult] = []

    # fitness_score (weight 0.30): higher = more risk
    # environmental_fit_score(inv), extinction_vulnerability, competitive_selection_pressure
    def _fitness_score(self, i: BiometicInput) -> float:
        s = 0
        if   i.environmental_fit_score <= 0.25: s += 40
        elif i.environmental_fit_score <= 0.50: s += 22
        elif i.environmental_fit_score <= 0.70: s += 8

        if   i.extinction_vulnerability >= 0.70: s += 35
        elif i.extinction_vulnerability >= 0.45: s += 18
        elif i.extinction_vulnerability >= 0.20: s += 6

        if   i.competitive_selection_pressure >= 0.70: s += 25
        elif i.competitive_selection_pressure >= 0.45: s += 12
        return min(s, 100)

    # adaptation_score (weight 0.25): higher = more risk
    # adaptive_mutation_rate(inv), phenotypic_plasticity(inv), coevolution_readiness(inv)
    def _adaptation_score(self, i: BiometicInput) -> float:
        s = 0
        if   i.adaptive_mutation_rate <= 0.25: s += 40
        elif i.adaptive_mutation_rate <= 0.50: s += 22
        elif i.adaptive_mutation_rate <= 0.70: s += 8

        if   i.phenotypic_plasticity <= 0.25: s += 35
        elif i.phenotypic_plasticity <= 0.50: s += 18
        elif i.phenotypic_plasticity <= 0.70: s += 6

        if   i.coevolution_readiness <= 0.25: s += 25
        elif i.coevolution_readiness <= 0.50: s += 12
        return min(s, 100)

    # resilience_score (weight 0.25): higher = more risk
    # resilience_redundancy(inv), regeneration_capacity(inv), biodiversity_analog_score(inv)
    def _resilience_score(self, i: BiometicInput) -> float:
        s = 0
        if   i.resilience_redundancy <= 0.25: s += 40
        elif i.resilience_redundancy <= 0.50: s += 22
        elif i.resilience_redundancy <= 0.70: s += 8

        if   i.regeneration_capacity <= 0.25: s += 35
        elif i.regeneration_capacity <= 0.50: s += 18
        elif i.regeneration_capacity <= 0.70: s += 6

        if   i.biodiversity_analog_score <= 0.25: s += 25
        elif i.biodiversity_analog_score <= 0.50: s += 12
        return min(s, 100)

    # synergy_score (weight 0.20): higher = more risk
    # symbiotic_partnership_depth(inv), swarm_coordination_score(inv), information_propagation_speed(inv)
    def _synergy_score(self, i: BiometicInput) -> float:
        s = 0
        if   i.symbiotic_partnership_depth <= 0.25: s += 40
        elif i.symbiotic_partnership_depth <= 0.50: s += 22
        elif i.symbiotic_partnership_depth <= 0.70: s += 8

        if   i.swarm_coordination_score <= 0.25: s += 35
        elif i.swarm_coordination_score <= 0.50: s += 18
        elif i.swarm_coordination_score <= 0.70: s += 6

        if   i.information_propagation_speed <= 0.25: s += 25
        elif i.information_propagation_speed <= 0.50: s += 12
        return min(s, 100)

    def _composite(self, fit: float, ada: float, res: float, syn: float) -> float:
        return min(round(fit * 0.30 + ada * 0.25 + res * 0.25 + syn * 0.20, 2), 100.0)

    def _risk(self, c: float) -> BiomimeticRisk:
        if c >= 60: return BiomimeticRisk.critical
        if c >= 40: return BiomimeticRisk.high
        if c >= 20: return BiomimeticRisk.moderate
        return BiomimeticRisk.low

    def _severity(self, c: float) -> BiomimeticSeverity:
        if c >= 60: return BiomimeticSeverity.extinct_risk
        if c >= 40: return BiomimeticSeverity.endangered
        if c >= 20: return BiomimeticSeverity.adapting
        return BiomimeticSeverity.thriving

    def _pattern(self, i: BiometicInput) -> EvolutionaryPattern:
        if i.extinction_vulnerability >= 0.65 and i.environmental_fit_score <= 0.35:
            return EvolutionaryPattern.extinction_spiral
        if i.niche_differentiation_score <= 0.30 and i.competitive_selection_pressure >= 0.60:
            return EvolutionaryPattern.niche_collapse
        if i.symbiotic_partnership_depth <= 0.30 and i.swarm_coordination_score <= 0.35:
            return EvolutionaryPattern.symbiosis_breakdown
        if i.adaptive_mutation_rate <= 0.30 and i.phenotypic_plasticity <= 0.35:
            return EvolutionaryPattern.evolutionary_stagnation
        if i.territorial_defense_strength <= 0.30 and i.ecological_dominance_index <= 0.35:
            return EvolutionaryPattern.territorial_loss
        return EvolutionaryPattern.none

    def _action(self, risk: BiomimeticRisk, pat: EvolutionaryPattern) -> BiomimeticAction:
        if risk == BiomimeticRisk.critical:
            if pat == EvolutionaryPattern.extinction_spiral:
                return BiomimeticAction.evolutionary_pivot
            return BiomimeticAction.niche_reconstruction
        if risk == BiomimeticRisk.high:
            if pat == EvolutionaryPattern.symbiosis_breakdown:
                return BiomimeticAction.symbiosis_forge
            return BiomimeticAction.adaptation_acceleration
        if risk == BiomimeticRisk.moderate:
            return BiomimeticAction.evolution_monitoring
        return BiomimeticAction.no_action

    def _has_extinction_signal(self, i: BiometicInput, comp: float) -> bool:
        return (
            comp >= 40
            or i.extinction_vulnerability >= 0.60
            or i.environmental_fit_score <= 0.30
            or i.niche_differentiation_score <= 0.25
        )

    def _requires_evolutionary_intervention(self, i: BiometicInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.extinction_vulnerability >= 0.45
            or i.adaptive_mutation_rate <= 0.30
        )

    def _extinction_risk_index(self, i: BiometicInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.resilience_redundancy + 0.01) * 10, 10.0), 2)

    def _signal(self, i: BiometicInput, pat: EvolutionaryPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Organisme en plein essor évolutif — fitness environnementale élevée, "
                "mutation adaptative active, résilience forte, synergies symbiotiques robustes"
            )
        labels: Dict[EvolutionaryPattern, str] = {
            EvolutionaryPattern.extinction_spiral:       "Spirale d'extinction",
            EvolutionaryPattern.niche_collapse:          "Effondrement de niche",
            EvolutionaryPattern.symbiosis_breakdown:     "Rupture symbiotique",
            EvolutionaryPattern.evolutionary_stagnation: "Stagnation évolutive",
            EvolutionaryPattern.territorial_loss:        "Perte territoriale",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — "
            f"fitness environnementale {round(i.environmental_fit_score * 100)}% — "
            f"vulnérabilité extinction {round(i.extinction_vulnerability * 100)}% — "
            f"taux mutation adaptative {round(i.adaptive_mutation_rate * 100)}% — "
            f"composite {round(comp)}"
        )

    def assess(self, i: BiometicInput) -> BiomimeticResult:
        fit  = self._fitness_score(i)
        ada  = self._adaptation_score(i)
        res  = self._resilience_score(i)
        syn  = self._synergy_score(i)
        comp = self._composite(fit, ada, res, syn)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = BiomimeticResult(
            organism_id=i.organism_id,
            region=i.region,
            biomimetic_risk=risk.value,
            evolutionary_pattern=pat.value,
            biomimetic_severity=sev.value,
            recommended_action=act.value,
            fitness_score=fit,
            adaptation_score=ada,
            resilience_score=res,
            synergy_score=syn,
            biomimetic_composite=comp,
            has_extinction_signal=self._has_extinction_signal(i, comp),
            requires_evolutionary_intervention=self._requires_evolutionary_intervention(i, comp),
            estimated_extinction_risk_index=self._extinction_risk_index(i, comp),
            biomimetic_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[BiometicInput]) -> List[BiomimeticResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total":                                    0,
                "risk_counts":                              {},
                "pattern_counts":                           {},
                "severity_counts":                          {},
                "action_counts":                            {},
                "avg_biomimetic_composite":                 0.0,
                "extinction_signal_count":                  0,
                "evolutionary_intervention_count":          0,
                "avg_fitness_score":                        0.0,
                "avg_adaptation_score":                     0.0,
                "avg_resilience_score":                     0.0,
                "avg_synergy_score":                        0.0,
                "avg_estimated_extinction_risk_index":      0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tfit = tada = tres = tsyn = tcomp = trisk = 0.0
        ext_c = interv_c = 0
        for r in self._results:
            rc[r.biomimetic_risk]       = rc.get(r.biomimetic_risk, 0)       + 1
            pc[r.evolutionary_pattern]  = pc.get(r.evolutionary_pattern, 0)  + 1
            sc[r.biomimetic_severity]   = sc.get(r.biomimetic_severity, 0)   + 1
            ac[r.recommended_action]    = ac.get(r.recommended_action, 0)    + 1
            tfit  += r.fitness_score
            tada  += r.adaptation_score
            tres  += r.resilience_score
            tsyn  += r.synergy_score
            tcomp += r.biomimetic_composite
            trisk += r.estimated_extinction_risk_index
            if r.has_extinction_signal:               ext_c    += 1
            if r.requires_evolutionary_intervention:  interv_c += 1
        return {
            "total":                                    n,
            "risk_counts":                              rc,
            "pattern_counts":                           pc,
            "severity_counts":                          sc,
            "action_counts":                            ac,
            "avg_biomimetic_composite":                 round(tcomp / n, 1),
            "extinction_signal_count":                  ext_c,
            "evolutionary_intervention_count":          interv_c,
            "avg_fitness_score":                        round(tfit  / n, 1),
            "avg_adaptation_score":                     round(tada  / n, 1),
            "avg_resilience_score":                     round(tres  / n, 1),
            "avg_synergy_score":                        round(tsyn  / n, 1),
            "avg_estimated_extinction_risk_index":      round(trisk / n, 2),
        }


MOCK_INPUTS: List[BiometicInput] = [
    BiometicInput(
        organism_id="BMS-001", strategy_archetype="swarm_intelligence", region="EMEA",
        adaptive_mutation_rate=0.12, environmental_fit_score=0.18, competitive_selection_pressure=0.82,
        symbiotic_partnership_depth=0.15, resource_efficiency_ratio=0.20, extinction_vulnerability=0.88,
        niche_differentiation_score=0.15, resilience_redundancy=0.18, swarm_coordination_score=0.20,
        phenotypic_plasticity=0.15, territorial_defense_strength=0.18, information_propagation_speed=0.15,
        energy_metabolism_efficiency=0.20, coevolution_readiness=0.12, biodiversity_analog_score=0.15,
        regeneration_capacity=0.18, ecological_dominance_index=0.15,
    ),
    BiometicInput(
        organism_id="BMS-002", strategy_archetype="evolutionary_selection", region="NAMER",
        adaptive_mutation_rate=0.88, environmental_fit_score=0.92, competitive_selection_pressure=0.10,
        symbiotic_partnership_depth=0.90, resource_efficiency_ratio=0.88, extinction_vulnerability=0.05,
        niche_differentiation_score=0.92, resilience_redundancy=0.90, swarm_coordination_score=0.88,
        phenotypic_plasticity=0.90, territorial_defense_strength=0.85, information_propagation_speed=0.90,
        energy_metabolism_efficiency=0.88, coevolution_readiness=0.90, biodiversity_analog_score=0.88,
        regeneration_capacity=0.92, ecological_dominance_index=0.90,
    ),
    BiometicInput(
        organism_id="BMS-003", strategy_archetype="predator_prey_dynamics", region="APAC",
        adaptive_mutation_rate=0.28, environmental_fit_score=0.42, competitive_selection_pressure=0.65,
        symbiotic_partnership_depth=0.35, resource_efficiency_ratio=0.48, extinction_vulnerability=0.58,
        niche_differentiation_score=0.22, resilience_redundancy=0.38, swarm_coordination_score=0.40,
        phenotypic_plasticity=0.35, territorial_defense_strength=0.42, information_propagation_speed=0.38,
        energy_metabolism_efficiency=0.45, coevolution_readiness=0.30, biodiversity_analog_score=0.35,
        regeneration_capacity=0.40, ecological_dominance_index=0.30,
    ),
    BiometicInput(
        organism_id="BMS-004", strategy_archetype="mycelial_network", region="LATAM",
        adaptive_mutation_rate=0.45, environmental_fit_score=0.55, competitive_selection_pressure=0.50,
        symbiotic_partnership_depth=0.48, resource_efficiency_ratio=0.52, extinction_vulnerability=0.35,
        niche_differentiation_score=0.55, resilience_redundancy=0.48, swarm_coordination_score=0.52,
        phenotypic_plasticity=0.55, territorial_defense_strength=0.58, information_propagation_speed=0.48,
        energy_metabolism_efficiency=0.55, coevolution_readiness=0.52, biodiversity_analog_score=0.50,
        regeneration_capacity=0.52, ecological_dominance_index=0.55,
    ),
    BiometicInput(
        organism_id="BMS-005", strategy_archetype="symbiotic_alliance", region="MEA",
        adaptive_mutation_rate=0.20, environmental_fit_score=0.40, competitive_selection_pressure=0.75,
        symbiotic_partnership_depth=0.18, resource_efficiency_ratio=0.22, extinction_vulnerability=0.80,
        niche_differentiation_score=0.55, resilience_redundancy=0.20, swarm_coordination_score=0.22,
        phenotypic_plasticity=0.18, territorial_defense_strength=0.22, information_propagation_speed=0.20,
        energy_metabolism_efficiency=0.25, coevolution_readiness=0.18, biodiversity_analog_score=0.20,
        regeneration_capacity=0.22, ecological_dominance_index=0.42,
    ),
    BiometicInput(
        organism_id="BMS-006", strategy_archetype="camouflage_strategy", region="EMEA",
        adaptive_mutation_rate=0.52, environmental_fit_score=0.58, competitive_selection_pressure=0.42,
        symbiotic_partnership_depth=0.55, resource_efficiency_ratio=0.50, extinction_vulnerability=0.38,
        niche_differentiation_score=0.55, resilience_redundancy=0.52, swarm_coordination_score=0.55,
        phenotypic_plasticity=0.50, territorial_defense_strength=0.55, information_propagation_speed=0.52,
        energy_metabolism_efficiency=0.55, coevolution_readiness=0.50, biodiversity_analog_score=0.52,
        regeneration_capacity=0.55, ecological_dominance_index=0.50,
    ),
    BiometicInput(
        organism_id="BMS-007", strategy_archetype="migration_adaptation", region="NAMER",
        adaptive_mutation_rate=0.25, environmental_fit_score=0.48, competitive_selection_pressure=0.60,
        symbiotic_partnership_depth=0.40, resource_efficiency_ratio=0.45, extinction_vulnerability=0.55,
        niche_differentiation_score=0.42, resilience_redundancy=0.40, swarm_coordination_score=0.45,
        phenotypic_plasticity=0.28, territorial_defense_strength=0.38, information_propagation_speed=0.42,
        energy_metabolism_efficiency=0.48, coevolution_readiness=0.28, biodiversity_analog_score=0.40,
        regeneration_capacity=0.42, ecological_dominance_index=0.38,
    ),
    BiometicInput(
        organism_id="BMS-008", strategy_archetype="regenerative_cycle", region="APAC",
        adaptive_mutation_rate=0.15, environmental_fit_score=0.38, competitive_selection_pressure=0.78,
        symbiotic_partnership_depth=0.55, resource_efficiency_ratio=0.18, extinction_vulnerability=0.55,
        niche_differentiation_score=0.55, resilience_redundancy=0.22, swarm_coordination_score=0.45,
        phenotypic_plasticity=0.40, territorial_defense_strength=0.15, information_propagation_speed=0.22,
        energy_metabolism_efficiency=0.18, coevolution_readiness=0.20, biodiversity_analog_score=0.18,
        regeneration_capacity=0.20, ecological_dominance_index=0.22,
    ),
]
