"""
Module 272 — Information Fluid Dynamics & Chaos Theory Engine
Applies fluid dynamics and chaos theory to model information flows, market turbulence,
organizational entropy, and bifurcation points in complex adaptive systems.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ChaosRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class ChaosPattern(str, Enum):
    none                   = "none"
    turbulent_cascade      = "turbulent_cascade"
    entropy_collapse       = "entropy_collapse"
    bifurcation_crisis     = "bifurcation_crisis"
    vortex_lock            = "vortex_lock"
    strange_attractor_trap = "strange_attractor_trap"


class FlowSeverity(str, Enum):
    laminar      = "laminar"
    transitional = "transitional"
    turbulent    = "turbulent"
    chaotic      = "chaotic"


class ChaosAction(str, Enum):
    no_action              = "no_action"
    flow_monitoring        = "flow_monitoring"
    entropy_reduction      = "entropy_reduction"
    attractor_stabilization = "attractor_stabilization"
    chaos_containment      = "chaos_containment"
    flow_restructuring     = "flow_restructuring"


@dataclass
class FluidSystemInput:
    system_id: str
    system_type: str   # information_market/organizational_network/supply_flow/capital_stream/
                       # social_cascade/regulatory_pipeline/innovation_diffusion/knowledge_vortex
    region: str
    flow_velocity_index: float          # 0-1
    turbulence_coefficient: float       # 0-1, higher=worse
    entropy_level: float                # 0-1, higher=worse
    bifurcation_proximity: float        # 0-1, higher=worse — how close to tipping point
    information_viscosity: float        # 0-1, higher=worse — resistance to flow
    attractor_stability_score: float    # 0-1
    vortex_formation_risk: float        # 0-1, higher=worse
    laminar_flow_efficiency: float      # 0-1
    reynolds_number_analog: float       # 0-1, higher=worse — chaos risk
    phase_transition_readiness: float   # 0-1
    dissipative_structure_score: float  # 0-1
    strange_attractor_detection: float  # 0-1
    fractal_dimension_risk: float       # 0-1, higher=worse
    butterfly_effect_sensitivity: float # 0-1, higher=worse
    self_organization_capacity: float   # 0-1
    resilience_basin_depth: float       # 0-1
    chaos_recovery_speed: float         # 0-1


@dataclass
class FluidSystemResult:
    system_id: str
    region: str
    chaos_risk: str
    chaos_pattern: str
    flow_severity: str
    recommended_action: str
    turbulence_score: float
    entropy_score: float
    flow_score: float
    resilience_score: float
    chaos_composite: float
    has_chaos_signal: bool
    requires_restructuring: bool
    estimated_chaos_index: float
    chaos_signal: str

    def to_dict(self) -> Dict:
        return {
            "system_id":              self.system_id,
            "region":                 self.region,
            "chaos_risk":             self.chaos_risk,
            "chaos_pattern":          self.chaos_pattern,
            "flow_severity":          self.flow_severity,
            "recommended_action":     self.recommended_action,
            "turbulence_score":       self.turbulence_score,
            "entropy_score":          self.entropy_score,
            "flow_score":             self.flow_score,
            "resilience_score":       self.resilience_score,
            "chaos_composite":        self.chaos_composite,
            "has_chaos_signal":       self.has_chaos_signal,
            "requires_restructuring": self.requires_restructuring,
            "estimated_chaos_index":  self.estimated_chaos_index,
            "chaos_signal":           self.chaos_signal,
        }


class InformationFluidDynamicsEngine:
    def __init__(self) -> None:
        self._results: List[FluidSystemResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _turbulence_score(self, i: FluidSystemInput) -> float:
        """0.30 weight — turbulence_coefficient, reynolds_number_analog, vortex_formation_risk"""
        s = 0.0
        if   i.turbulence_coefficient >= 0.70: s += 40
        elif i.turbulence_coefficient >= 0.50: s += 22
        elif i.turbulence_coefficient >= 0.30: s += 8

        if   i.reynolds_number_analog >= 0.75: s += 35
        elif i.reynolds_number_analog >= 0.55: s += 18
        elif i.reynolds_number_analog >= 0.35: s += 6

        if   i.vortex_formation_risk >= 0.65: s += 25
        elif i.vortex_formation_risk >= 0.45: s += 12
        return min(s, 100.0)

    def _entropy_score(self, i: FluidSystemInput) -> float:
        """0.25 weight — entropy_level, fractal_dimension_risk, butterfly_effect_sensitivity"""
        s = 0.0
        if   i.entropy_level >= 0.70: s += 40
        elif i.entropy_level >= 0.50: s += 22
        elif i.entropy_level >= 0.30: s += 8

        if   i.fractal_dimension_risk >= 0.70: s += 35
        elif i.fractal_dimension_risk >= 0.50: s += 18
        elif i.fractal_dimension_risk >= 0.30: s += 6

        if   i.butterfly_effect_sensitivity >= 0.70: s += 25
        elif i.butterfly_effect_sensitivity >= 0.50: s += 12
        return min(s, 100.0)

    def _flow_score(self, i: FluidSystemInput) -> float:
        """0.25 weight — information_viscosity, laminar_flow_efficiency(inv), bifurcation_proximity"""
        s = 0.0
        if   i.information_viscosity >= 0.70: s += 40
        elif i.information_viscosity >= 0.50: s += 22
        elif i.information_viscosity >= 0.30: s += 8

        # laminar_flow_efficiency is inverted (low efficiency = bad)
        inv_lfe = 1.0 - i.laminar_flow_efficiency
        if   inv_lfe >= 0.70: s += 35
        elif inv_lfe >= 0.50: s += 18
        elif inv_lfe >= 0.30: s += 6

        if   i.bifurcation_proximity >= 0.70: s += 25
        elif i.bifurcation_proximity >= 0.50: s += 12
        return min(s, 100.0)

    def _resilience_score(self, i: FluidSystemInput) -> float:
        """0.20 weight — attractor_stability_score(inv), resilience_basin_depth(inv), chaos_recovery_speed(inv)"""
        s = 0.0
        # All three are inverted (low = bad)
        inv_att = 1.0 - i.attractor_stability_score
        if   inv_att >= 0.70: s += 40
        elif inv_att >= 0.50: s += 22
        elif inv_att >= 0.30: s += 8

        inv_rbd = 1.0 - i.resilience_basin_depth
        if   inv_rbd >= 0.70: s += 35
        elif inv_rbd >= 0.50: s += 18
        elif inv_rbd >= 0.30: s += 6

        inv_crs = 1.0 - i.chaos_recovery_speed
        if   inv_crs >= 0.70: s += 25
        elif inv_crs >= 0.50: s += 12
        return min(s, 100.0)

    def _composite(self, turb: float, entr: float, flow: float, res: float) -> float:
        return min(round(turb * 0.30 + entr * 0.25 + flow * 0.25 + res * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> ChaosRisk:
        if c >= 60: return ChaosRisk.critical
        if c >= 40: return ChaosRisk.high
        if c >= 20: return ChaosRisk.moderate
        return ChaosRisk.low

    def _severity(self, c: float) -> FlowSeverity:
        if c >= 60: return FlowSeverity.chaotic
        if c >= 40: return FlowSeverity.turbulent
        if c >= 20: return FlowSeverity.transitional
        return FlowSeverity.laminar

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: FluidSystemInput) -> ChaosPattern:
        if i.turbulence_coefficient >= 0.65 and i.reynolds_number_analog >= 0.60:
            return ChaosPattern.turbulent_cascade
        if i.entropy_level >= 0.70 and i.fractal_dimension_risk >= 0.60:
            return ChaosPattern.entropy_collapse
        if i.bifurcation_proximity >= 0.70:
            return ChaosPattern.bifurcation_crisis
        if i.vortex_formation_risk >= 0.65 and i.information_viscosity >= 0.55:
            return ChaosPattern.vortex_lock
        if i.strange_attractor_detection >= 0.65 and i.butterfly_effect_sensitivity >= 0.55:
            return ChaosPattern.strange_attractor_trap
        return ChaosPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: ChaosRisk, pat: ChaosPattern) -> ChaosAction:
        if risk == ChaosRisk.critical:
            if pat == ChaosPattern.turbulent_cascade: return ChaosAction.chaos_containment
            return ChaosAction.flow_restructuring
        if risk == ChaosRisk.high:
            if pat in (ChaosPattern.entropy_collapse, ChaosPattern.bifurcation_crisis):
                return ChaosAction.entropy_reduction
            return ChaosAction.attractor_stabilization
        if risk == ChaosRisk.moderate:
            return ChaosAction.flow_monitoring
        return ChaosAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived booleans & index                                            #
    # ------------------------------------------------------------------ #

    def _has_chaos_signal(self, i: FluidSystemInput, comp: float) -> bool:
        return (comp >= 40
                or i.turbulence_coefficient >= 0.60
                or i.bifurcation_proximity >= 0.65
                or i.entropy_level >= 0.60)

    def _requires_restructuring(self, i: FluidSystemInput, comp: float) -> bool:
        return (comp >= 25
                or i.reynolds_number_analog >= 0.65
                or i.information_viscosity >= 0.65
                or i.vortex_formation_risk >= 0.65)

    def _chaos_index(self, i: FluidSystemInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.attractor_stability_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: FluidSystemInput, pat: ChaosPattern, comp: float) -> str:
        if comp < 20:
            return "Flux laminaire stable — dynamique fluide équilibrée, attracteurs stables, entropie maîtrisée"
        labels = {
            ChaosPattern.turbulent_cascade:      "Cascade turbulente",
            ChaosPattern.entropy_collapse:        "Effondrement entropique",
            ChaosPattern.bifurcation_crisis:      "Crise de bifurcation",
            ChaosPattern.vortex_lock:             "Verrouillage vortex",
            ChaosPattern.strange_attractor_trap:  "Piège attracteur étrange",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — coefficient Reynolds {i.reynolds_number_analog:.2f}"
            f" — proximité bifurcation {i.bifurcation_proximity * 100:.0f}%"
            f" — entropie composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: FluidSystemInput) -> FluidSystemResult:
        turb  = self._turbulence_score(i)
        entr  = self._entropy_score(i)
        flow  = self._flow_score(i)
        res   = self._resilience_score(i)
        comp  = self._composite(turb, entr, flow, res)
        risk  = self._risk(comp)
        sev   = self._severity(comp)
        pat   = self._pattern(i)
        act   = self._action(risk, pat)
        result = FluidSystemResult(
            system_id=i.system_id,
            region=i.region,
            chaos_risk=risk.value,
            chaos_pattern=pat.value,
            flow_severity=sev.value,
            recommended_action=act.value,
            turbulence_score=turb,
            entropy_score=entr,
            flow_score=flow,
            resilience_score=res,
            chaos_composite=comp,
            has_chaos_signal=self._has_chaos_signal(i, comp),
            requires_restructuring=self._requires_restructuring(i, comp),
            estimated_chaos_index=self._chaos_index(i, comp),
            chaos_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[FluidSystemInput]) -> List[FluidSystemResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total":                       0,
                "risk_counts":                 {},
                "pattern_counts":              {},
                "severity_counts":             {},
                "action_counts":               {},
                "avg_estimated_chaos_index":   0.0,
                "chaos_signal_count":          0,
                "restructuring_required_count": 0,
                "avg_turbulence_score":        0.0,
                "avg_entropy_score":           0.0,
                "avg_flow_score":              0.0,
                "avg_resilience_score":        0.0,
                "avg_chaos_composite":         0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tturb = tentr = tflow = tres = tcomp = tidx = 0.0
        chaos_count = restruct_count = 0
        for r in self._results:
            rc[r.chaos_risk]         = rc.get(r.chaos_risk, 0)         + 1
            pc[r.chaos_pattern]      = pc.get(r.chaos_pattern, 0)      + 1
            sc[r.flow_severity]      = sc.get(r.flow_severity, 0)      + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tturb += r.turbulence_score
            tentr += r.entropy_score
            tflow += r.flow_score
            tres  += r.resilience_score
            tcomp += r.chaos_composite
            tidx  += r.estimated_chaos_index
            if r.has_chaos_signal:       chaos_count    += 1
            if r.requires_restructuring: restruct_count += 1
        return {
            "total":                        n,
            "risk_counts":                  rc,
            "pattern_counts":               pc,
            "severity_counts":              sc,
            "action_counts":                ac,
            "avg_estimated_chaos_index":    round(tidx  / n, 2),
            "chaos_signal_count":           chaos_count,
            "restructuring_required_count": restruct_count,
            "avg_turbulence_score":         round(tturb / n, 1),
            "avg_entropy_score":            round(tentr / n, 1),
            "avg_flow_score":               round(tflow / n, 1),
            "avg_resilience_score":         round(tres  / n, 1),
            "avg_chaos_composite":          round(tcomp / n, 1),
        }
