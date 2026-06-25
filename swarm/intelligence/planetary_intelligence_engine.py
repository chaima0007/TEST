from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class EcosystemInput:
    zone_id: str
    ecosystem_type: str  # ocean_system/forest_biome/urban_heat_island/permafrost_zone/coral_reef/freshwater_basin/atmospheric_layer/soil_microbiome
    region: str
    planetary_boundary_breach_score: float       # higher = worse
    biodiversity_loss_rate: float                # higher = worse
    carbon_sequestration_capacity: float
    tipping_point_proximity: float               # higher = worse
    ecosystem_service_value_score: float
    climate_resilience_index: float
    pollutant_concentration_risk: float          # higher = worse
    species_extinction_velocity: float           # higher = worse
    water_cycle_disruption_risk: float           # higher = worse
    soil_degradation_rate: float                 # higher = worse
    natural_capital_depletion: float             # higher = worse
    ecosystem_connectivity_score: float
    restoration_potential_score: float
    indigenous_stewardship_quality: float
    corporate_biodiversity_exposure: float
    regulatory_nature_risk: float                # higher = worse
    nature_positive_trajectory: float


def _boundary_score(inp: EcosystemInput) -> float:
    # 0.30 weight — planetary_boundary_breach_score, tipping_point_proximity, carbon_sequestration_capacity(inv)
    avg = (
        inp.planetary_boundary_breach_score
        + inp.tipping_point_proximity
        + (1.0 - inp.carbon_sequestration_capacity)
    ) / 3.0
    return round(min(avg * 100.0, 100.0), 2)


def _biodiversity_score(inp: EcosystemInput) -> float:
    # 0.25 weight — biodiversity_loss_rate, species_extinction_velocity, ecosystem_connectivity_score(inv)
    avg = (
        inp.biodiversity_loss_rate
        + inp.species_extinction_velocity
        + (1.0 - inp.ecosystem_connectivity_score)
    ) / 3.0
    return round(min(avg * 100.0, 100.0), 2)


def _degradation_score(inp: EcosystemInput) -> float:
    # 0.25 weight — soil_degradation_rate, water_cycle_disruption_risk, natural_capital_depletion
    avg = (
        inp.soil_degradation_rate
        + inp.water_cycle_disruption_risk
        + inp.natural_capital_depletion
    ) / 3.0
    return round(min(avg * 100.0, 100.0), 2)


def _exposure_score(inp: EcosystemInput) -> float:
    # 0.20 weight — corporate_biodiversity_exposure, regulatory_nature_risk, nature_positive_trajectory(inv)
    avg = (
        inp.corporate_biodiversity_exposure
        + inp.regulatory_nature_risk
        + (1.0 - inp.nature_positive_trajectory)
    ) / 3.0
    return round(min(avg * 100.0, 100.0), 2)


def _composite(bnd: float, bio: float, deg: float, exp: float) -> float:
    return round(min(bnd * 0.30 + bio * 0.25 + deg * 0.25 + exp * 0.20, 100.0), 2)


def _planetary_risk(comp: float) -> str:
    if comp >= 60:
        return "critical"
    if comp >= 40:
        return "high"
    if comp >= 20:
        return "moderate"
    return "low"


def _severity(comp: float) -> str:
    if comp >= 60:
        return "collapsed"
    if comp >= 40:
        return "critical_stress"
    if comp >= 20:
        return "degrading"
    return "thriving"


def _pattern(inp: EcosystemInput) -> str:
    if inp.tipping_point_proximity >= 0.70 and inp.planetary_boundary_breach_score >= 0.65:
        return "tipping_point_breach"
    if inp.biodiversity_loss_rate >= 0.65 and inp.species_extinction_velocity >= 0.60:
        return "biodiversity_collapse"
    if inp.carbon_sequestration_capacity <= 0.30 and inp.planetary_boundary_breach_score >= 0.60:
        return "carbon_crisis"
    if inp.water_cycle_disruption_risk >= 0.65 and inp.soil_degradation_rate >= 0.55:
        return "water_system_failure"
    if inp.ecosystem_connectivity_score <= 0.30 and inp.natural_capital_depletion >= 0.55:
        return "ecosystem_fragmentation"
    return "none"


def _action(risk: str, pat: str) -> str:
    if risk == "critical":
        if pat == "tipping_point_breach":
            return "ecosystem_emergency"
        return "tipping_point_intervention"
    if risk == "high":
        if pat == "carbon_crisis":
            return "carbon_emergency"
        return "nature_positive_program"
    if risk == "moderate":
        return "ecosystem_monitoring"
    return "no_action"


def _signal(inp: EcosystemInput, pat: str, comp: float) -> str:
    if comp < 20:
        return (
            "Écosystème en bonne santé — frontières planétaires respectées, "
            "biodiversité préservée, trajectoire nature-positive confirmée"
        )
    labels: dict[str, str] = {
        "tipping_point_breach":     "Franchissement de point de bascule",
        "biodiversity_collapse":    "Effondrement de la biodiversité",
        "carbon_crisis":            "Crise carbone — séquestration critique",
        "water_system_failure":     "Défaillance du cycle de l'eau",
        "ecosystem_fragmentation":  "Fragmentation écosystémique",
    }
    label = labels.get(pat, pat.replace("_", " "))
    return (
        f"{label} — transgression frontières {inp.planetary_boundary_breach_score:.2f} "
        f"— proximité bascule {inp.tipping_point_proximity:.2f} "
        f"— perte biodiversité {inp.biodiversity_loss_rate:.2f} "
        f"— composite {round(comp)}"
    )


@dataclass
class EcosystemResult:
    zone_id: str
    ecosystem_type: str
    region: str
    planetary_risk: str
    ecosystem_pattern: str
    ecosystem_severity: str
    recommended_action: str
    boundary_score: float
    biodiversity_score: float
    degradation_score: float
    exposure_score: float
    planetary_risk_composite: float
    is_tipping_point_risk: bool
    requires_emergency_intervention: bool
    estimated_planetary_risk_index: float
    ecosystem_signal: str

    def to_dict(self) -> dict:
        return {
            "zone_id": self.zone_id,
            "ecosystem_type": self.ecosystem_type,
            "region": self.region,
            "planetary_risk": self.planetary_risk,
            "ecosystem_pattern": self.ecosystem_pattern,
            "ecosystem_severity": self.ecosystem_severity,
            "recommended_action": self.recommended_action,
            "boundary_score": self.boundary_score,
            "biodiversity_score": self.biodiversity_score,
            "degradation_score": self.degradation_score,
            "exposure_score": self.exposure_score,
            "planetary_risk_composite": self.planetary_risk_composite,
            "is_tipping_point_risk": self.is_tipping_point_risk,
            "requires_emergency_intervention": self.requires_emergency_intervention,
            "estimated_planetary_risk_index": self.estimated_planetary_risk_index,
        }


class PlanetaryIntelligenceEngine:
    def __init__(self) -> None:
        self._results: dict[str, EcosystemResult] = {}

    def assess(self, inp: EcosystemInput) -> EcosystemResult:
        bnd = _boundary_score(inp)
        bio = _biodiversity_score(inp)
        deg = _degradation_score(inp)
        exp = _exposure_score(inp)
        comp = _composite(bnd, bio, deg, exp)
        pat = _pattern(inp)
        risk = _planetary_risk(comp)
        sev = _severity(comp)
        act = _action(risk, pat)
        is_tipping = comp >= 60 or inp.tipping_point_proximity >= 0.70
        requires_emergency = act in ("ecosystem_emergency", "tipping_point_intervention")
        risk_index = round(
            min(comp / 100.0 * (inp.planetary_boundary_breach_score + inp.tipping_point_proximity) / 2.0 * 10.0, 10.0),
            2,
        )
        result = EcosystemResult(
            zone_id=inp.zone_id,
            ecosystem_type=inp.ecosystem_type,
            region=inp.region,
            planetary_risk=risk,
            ecosystem_pattern=pat,
            ecosystem_severity=sev,
            recommended_action=act,
            boundary_score=bnd,
            biodiversity_score=bio,
            degradation_score=deg,
            exposure_score=exp,
            planetary_risk_composite=comp,
            is_tipping_point_risk=is_tipping,
            requires_emergency_intervention=requires_emergency,
            estimated_planetary_risk_index=risk_index,
            ecosystem_signal=_signal(inp, pat, comp),
        )
        self._results[inp.zone_id] = result
        return result

    def assess_batch(self, zones: List[EcosystemInput]) -> List[EcosystemResult]:
        results = [self.assess(z) for z in zones]
        return sorted(results, key=lambda r: r.planetary_risk_composite, reverse=True)

    def all_zones(self) -> List[EcosystemResult]:
        return sorted(self._results.values(), key=lambda r: r.planetary_risk_composite, reverse=True)

    def by_risk(self, risk: str) -> List[EcosystemResult]:
        return [r for r in self._results.values() if r.planetary_risk == risk]

    def by_pattern(self, pattern: str) -> List[EcosystemResult]:
        return [r for r in self._results.values() if r.ecosystem_pattern == pattern]

    def tipping_point_zones(self) -> List[EcosystemResult]:
        return [r for r in self._results.values() if r.is_tipping_point_risk]

    def emergency_zones(self) -> List[EcosystemResult]:
        return [r for r in self._results.values() if r.requires_emergency_intervention]

    def avg_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.planetary_risk_composite for r in self._results.values()) / len(self._results), 1)

    def avg_boundary(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.boundary_score for r in self._results.values()) / len(self._results), 1)

    def avg_biodiversity(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.biodiversity_score for r in self._results.values()) / len(self._results), 1)

    def avg_degradation(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.degradation_score for r in self._results.values()) / len(self._results), 1)

    def avg_exposure(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.exposure_score for r in self._results.values()) / len(self._results), 1)

    def summary(self) -> dict:
        all_r = list(self._results.values())
        n = len(all_r)
        risk_counts = {}
        pattern_counts = {}
        severity_counts = {}
        action_counts = {}
        t_bnd = t_bio = t_deg = t_exp = t_comp = t_ridx = 0.0
        tipping_c = emergency_c = 0
        for r in all_r:
            risk_counts[r.planetary_risk]       = risk_counts.get(r.planetary_risk, 0) + 1
            pattern_counts[r.ecosystem_pattern] = pattern_counts.get(r.ecosystem_pattern, 0) + 1
            severity_counts[r.ecosystem_severity] = severity_counts.get(r.ecosystem_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            t_bnd  += r.boundary_score
            t_bio  += r.biodiversity_score
            t_deg  += r.degradation_score
            t_exp  += r.exposure_score
            t_comp += r.planetary_risk_composite
            t_ridx += r.estimated_planetary_risk_index
            if r.is_tipping_point_risk:
                tipping_c += 1
            if r.requires_emergency_intervention:
                emergency_c += 1
        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_planetary_risk_composite": round(t_comp / n, 1) if n else 0.0,
            "tipping_point_risk_count": tipping_c,
            "emergency_intervention_count": emergency_c,
            "avg_boundary_score": round(t_bnd / n, 1) if n else 0.0,
            "avg_biodiversity_score": round(t_bio / n, 1) if n else 0.0,
            "avg_degradation_score": round(t_deg / n, 1) if n else 0.0,
            "avg_exposure_score": round(t_exp / n, 1) if n else 0.0,
            "avg_estimated_planetary_risk_index": round(t_ridx / n, 2) if n else 0.0,
        }

    def reset(self) -> None:
        self._results.clear()
