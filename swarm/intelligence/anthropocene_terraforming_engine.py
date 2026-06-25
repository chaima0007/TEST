"""
Module 248 — Anthropocene & Local Terraforming Optimization Engine
Monitors environmental impact at the local territory level — tracking ecosystem
health, urban heat islands, biodiversity corridors, carbon sequestration, soil
regeneration, water cycles, and green infrastructure. Provides optimization
recommendations for local environmental transformation.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class TerraformingRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class EcoPattern(str, Enum):
    none                  = "none"
    urban_heat_surge      = "urban_heat_surge"
    biodiversity_collapse = "biodiversity_collapse"
    soil_degradation      = "soil_degradation"
    water_stress          = "water_stress"
    carbon_debt           = "carbon_debt"


class TerraformingSeverity(str, Enum):
    regenerating = "regenerating"
    stable       = "stable"
    degraded     = "degraded"
    critical     = "critical"


class TerraformingAction(str, Enum):
    no_action                    = "no_action"
    eco_monitoring               = "eco_monitoring"
    green_corridor_activation    = "green_corridor_activation"
    soil_remediation             = "soil_remediation"
    water_cycle_restoration      = "water_cycle_restoration"
    urban_cooling_deployment     = "urban_cooling_deployment"
    biodiversity_reintroduction  = "biodiversity_reintroduction"
    emergency_terraforming       = "emergency_terraforming"
    territory_quarantine         = "territory_quarantine"


@dataclass
class TerraformingInput:
    territory_id: str
    territory_type: str
    region: str
    ecosystem_health_score: float
    biodiversity_index: float
    soil_quality_score: float
    water_cycle_integrity: float
    urban_heat_island_intensity: float
    carbon_sequestration_rate: float
    green_cover_pct: float
    air_quality_index: float
    pollutant_concentration_score: float
    rewilding_potential_score: float
    micro_climate_stability: float
    invasive_species_pressure: float
    local_food_system_resilience: float
    regenerative_practice_adoption: float
    community_eco_engagement: float
    tipping_point_proximity: float
    ecological_connectivity_score: float


@dataclass
class TerraformingResult:
    territory_id: str
    region: str
    terraforming_risk: str
    eco_pattern: str
    terraforming_severity: str
    recommended_action: str
    ecosystem_score: float
    climate_score: float
    resource_score: float
    resilience_score: float
    terraforming_composite: float
    has_ecological_alert: bool
    requires_emergency_action: bool
    estimated_ecological_risk_index: float
    terraforming_signal: str

    def to_dict(self) -> Dict:
        return {
            "territory_id":                     self.territory_id,
            "region":                           self.region,
            "terraforming_risk":                self.terraforming_risk,
            "eco_pattern":                      self.eco_pattern,
            "terraforming_severity":            self.terraforming_severity,
            "recommended_action":               self.recommended_action,
            "ecosystem_score":                  self.ecosystem_score,
            "climate_score":                    self.climate_score,
            "resource_score":                   self.resource_score,
            "resilience_score":                 self.resilience_score,
            "terraforming_composite":           self.terraforming_composite,
            "has_ecological_alert":             self.has_ecological_alert,
            "requires_emergency_action":        self.requires_emergency_action,
            "estimated_ecological_risk_index":  self.estimated_ecological_risk_index,
            "terraforming_signal":              self.terraforming_signal,
        }


class AnthropoceneTerraformingEngine:
    def __init__(self) -> None:
        self._results: List[TerraformingResult] = []

    def _ecosystem_score(self, i: TerraformingInput) -> float:
        s = 0
        if   i.ecosystem_health_score <= 0.25: s += 40
        elif i.ecosystem_health_score <= 0.50: s += 22
        elif i.ecosystem_health_score <= 0.70: s += 8

        if   i.biodiversity_index <= 0.25: s += 35
        elif i.biodiversity_index <= 0.50: s += 18
        elif i.biodiversity_index <= 0.70: s += 6

        if   i.invasive_species_pressure >= 0.70: s += 25
        elif i.invasive_species_pressure >= 0.45: s += 12
        return min(s, 100)

    def _climate_score(self, i: TerraformingInput) -> float:
        s = 0
        if   i.urban_heat_island_intensity >= 0.70: s += 40
        elif i.urban_heat_island_intensity >= 0.45: s += 22
        elif i.urban_heat_island_intensity >= 0.20: s += 8

        if   i.carbon_sequestration_rate <= 0.20: s += 35
        elif i.carbon_sequestration_rate <= 0.45: s += 18
        elif i.carbon_sequestration_rate <= 0.65: s += 6

        if   i.micro_climate_stability <= 0.25: s += 25
        elif i.micro_climate_stability <= 0.50: s += 12
        return min(s, 100)

    def _resource_score(self, i: TerraformingInput) -> float:
        s = 0
        if   i.soil_quality_score <= 0.25: s += 40
        elif i.soil_quality_score <= 0.50: s += 22
        elif i.soil_quality_score <= 0.70: s += 8

        if   i.water_cycle_integrity <= 0.25: s += 35
        elif i.water_cycle_integrity <= 0.50: s += 18
        elif i.water_cycle_integrity <= 0.70: s += 6

        if   i.pollutant_concentration_score >= 0.65: s += 25
        elif i.pollutant_concentration_score >= 0.40: s += 12
        return min(s, 100)

    def _resilience_score(self, i: TerraformingInput) -> float:
        s = 0
        if   i.tipping_point_proximity >= 0.70: s += 40
        elif i.tipping_point_proximity >= 0.45: s += 22
        elif i.tipping_point_proximity >= 0.20: s += 8

        if   i.ecological_connectivity_score <= 0.25: s += 35
        elif i.ecological_connectivity_score <= 0.50: s += 18
        elif i.ecological_connectivity_score <= 0.70: s += 6

        if   i.regenerative_practice_adoption <= 0.25: s += 25
        elif i.regenerative_practice_adoption <= 0.50: s += 12
        return min(s, 100)

    def _composite(self, eco: float, cli: float, res: float, resil: float) -> float:
        return min(round(eco * 0.30 + cli * 0.25 + res * 0.25 + resil * 0.20, 2), 100.0)

    def _risk(self, c: float) -> TerraformingRisk:
        if c >= 60: return TerraformingRisk.critical
        if c >= 40: return TerraformingRisk.high
        if c >= 20: return TerraformingRisk.moderate
        return TerraformingRisk.low

    def _severity(self, c: float) -> TerraformingSeverity:
        if c >= 60: return TerraformingSeverity.critical
        if c >= 40: return TerraformingSeverity.degraded
        if c >= 20: return TerraformingSeverity.stable
        return TerraformingSeverity.regenerating

    def _pattern(self, i: TerraformingInput) -> EcoPattern:
        if (i.urban_heat_island_intensity >= 0.55
                or (i.territory_type in ("urban", "peri_urban", "industrial")
                    and i.green_cover_pct <= 0.25)):
            return EcoPattern.urban_heat_surge
        if i.biodiversity_index <= 0.35 or i.invasive_species_pressure >= 0.6:
            return EcoPattern.biodiversity_collapse
        if i.soil_quality_score <= 0.35 and i.pollutant_concentration_score >= 0.4:
            return EcoPattern.soil_degradation
        if i.water_cycle_integrity <= 0.4:
            return EcoPattern.water_stress
        if i.carbon_sequestration_rate <= 0.3 and i.green_cover_pct <= 0.3:
            return EcoPattern.carbon_debt
        return EcoPattern.none

    def _action(self, risk: TerraformingRisk, pat: EcoPattern) -> TerraformingAction:
        if risk == TerraformingRisk.critical:
            if pat == EcoPattern.urban_heat_surge:
                return TerraformingAction.urban_cooling_deployment
            if pat == EcoPattern.biodiversity_collapse:
                return TerraformingAction.biodiversity_reintroduction
            return TerraformingAction.emergency_terraforming
        if risk == TerraformingRisk.high:
            if pat == EcoPattern.urban_heat_surge:
                return TerraformingAction.green_corridor_activation
            if pat == EcoPattern.biodiversity_collapse:
                return TerraformingAction.biodiversity_reintroduction
            if pat == EcoPattern.soil_degradation:
                return TerraformingAction.soil_remediation
            if pat == EcoPattern.water_stress:
                return TerraformingAction.water_cycle_restoration
            if pat == EcoPattern.carbon_debt:
                return TerraformingAction.green_corridor_activation
            return TerraformingAction.eco_monitoring
        if risk == TerraformingRisk.moderate:
            return TerraformingAction.eco_monitoring
        return TerraformingAction.no_action

    def _has_ecological_alert(self, i: TerraformingInput, comp: float) -> bool:
        return (
            comp >= 40
            or i.tipping_point_proximity >= 0.6
            or i.biodiversity_index <= 0.3
            or i.urban_heat_island_intensity >= 0.6
        )

    def _requires_emergency_action(self, i: TerraformingInput, comp: float) -> bool:
        return (
            comp >= 25
            or i.tipping_point_proximity >= 0.45
            or i.ecosystem_health_score <= 0.3
        )

    def _ecological_risk_index(self, i: TerraformingInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.ecological_connectivity_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: TerraformingInput, pat: EcoPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Territoire en régénération — biodiversité croissante, sols sains, "
                "cycle hydrique intact, résilience écologique forte"
            )
        labels: Dict[EcoPattern, str] = {
            EcoPattern.urban_heat_surge:      "Surchauffe urbaine",
            EcoPattern.biodiversity_collapse: "Effondrement biodiversité",
            EcoPattern.soil_degradation:      "Dégradation des sols",
            EcoPattern.water_stress:          "Stress hydrique",
            EcoPattern.carbon_debt:           "Dette carbone",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — "
            f"santé écosystème {round(i.ecosystem_health_score * 100)}% — "
            f"biodiversité {round(i.biodiversity_index * 100)}% — "
            f"proximité point basculement {round(i.tipping_point_proximity * 100)}% — "
            f"composite {round(comp)}"
        )

    def assess(self, i: TerraformingInput) -> TerraformingResult:
        eco   = self._ecosystem_score(i)
        cli   = self._climate_score(i)
        res   = self._resource_score(i)
        resil = self._resilience_score(i)
        comp  = self._composite(eco, cli, res, resil)
        risk  = self._risk(comp)
        sev   = self._severity(comp)
        pat   = self._pattern(i)
        act   = self._action(risk, pat)
        result = TerraformingResult(
            territory_id=i.territory_id,
            region=i.region,
            terraforming_risk=risk.value,
            eco_pattern=pat.value,
            terraforming_severity=sev.value,
            recommended_action=act.value,
            ecosystem_score=eco,
            climate_score=cli,
            resource_score=res,
            resilience_score=resil,
            terraforming_composite=comp,
            has_ecological_alert=self._has_ecological_alert(i, comp),
            requires_emergency_action=self._requires_emergency_action(i, comp),
            estimated_ecological_risk_index=self._ecological_risk_index(i, comp),
            terraforming_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[TerraformingInput]) -> List[TerraformingResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total":                                0,
                "risk_counts":                          {},
                "pattern_counts":                       {},
                "severity_counts":                      {},
                "action_counts":                        {},
                "avg_terraforming_composite":           0.0,
                "ecological_alert_count":               0,
                "emergency_action_count":               0,
                "avg_ecosystem_score":                  0.0,
                "avg_climate_score":                    0.0,
                "avg_resource_score":                   0.0,
                "avg_resilience_score":                 0.0,
                "avg_estimated_ecological_risk_index":  0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        teco = tcli = tres = tresil = tcomp = trisk = 0.0
        alert_c = emerg_c = 0
        for r in self._results:
            rc[r.terraforming_risk]      = rc.get(r.terraforming_risk, 0)      + 1
            pc[r.eco_pattern]            = pc.get(r.eco_pattern, 0)            + 1
            sc[r.terraforming_severity]  = sc.get(r.terraforming_severity, 0)  + 1
            ac[r.recommended_action]     = ac.get(r.recommended_action, 0)     + 1
            teco   += r.ecosystem_score
            tcli   += r.climate_score
            tres   += r.resource_score
            tresil += r.resilience_score
            tcomp  += r.terraforming_composite
            trisk  += r.estimated_ecological_risk_index
            if r.has_ecological_alert:    alert_c += 1
            if r.requires_emergency_action: emerg_c += 1
        return {
            "total":                                n,
            "risk_counts":                          rc,
            "pattern_counts":                       pc,
            "severity_counts":                      sc,
            "action_counts":                        ac,
            "avg_terraforming_composite":           round(tcomp  / n, 1),
            "ecological_alert_count":               alert_c,
            "emergency_action_count":               emerg_c,
            "avg_ecosystem_score":                  round(teco   / n, 1),
            "avg_climate_score":                    round(tcli   / n, 1),
            "avg_resource_score":                   round(tres   / n, 1),
            "avg_resilience_score":                 round(tresil / n, 1),
            "avg_estimated_ecological_risk_index":  round(trisk  / n, 2),
        }


MOCK_INPUTS: List[TerraformingInput] = [
    TerraformingInput(
        territory_id="TF-001", territory_type="urban", region="EMEA",
        ecosystem_health_score=0.30, biodiversity_index=0.25,
        soil_quality_score=0.32, water_cycle_integrity=0.38,
        urban_heat_island_intensity=0.72, carbon_sequestration_rate=0.15,
        green_cover_pct=0.12, air_quality_index=0.28,
        pollutant_concentration_score=0.70, rewilding_potential_score=0.20,
        micro_climate_stability=0.28, invasive_species_pressure=0.35,
        local_food_system_resilience=0.22, regenerative_practice_adoption=0.18,
        community_eco_engagement=0.30, tipping_point_proximity=0.78,
        ecological_connectivity_score=0.15,
    ),
    TerraformingInput(
        territory_id="TF-002", territory_type="peri_urban", region="NAMER",
        ecosystem_health_score=0.45, biodiversity_index=0.42,
        soil_quality_score=0.50, water_cycle_integrity=0.48,
        urban_heat_island_intensity=0.58, carbon_sequestration_rate=0.28,
        green_cover_pct=0.22, air_quality_index=0.50,
        pollutant_concentration_score=0.45, rewilding_potential_score=0.42,
        micro_climate_stability=0.48, invasive_species_pressure=0.28,
        local_food_system_resilience=0.45, regenerative_practice_adoption=0.38,
        community_eco_engagement=0.48, tipping_point_proximity=0.48,
        ecological_connectivity_score=0.38,
    ),
    TerraformingInput(
        territory_id="TF-003", territory_type="rural", region="APAC",
        ecosystem_health_score=0.78, biodiversity_index=0.75,
        soil_quality_score=0.80, water_cycle_integrity=0.82,
        urban_heat_island_intensity=0.08, carbon_sequestration_rate=0.75,
        green_cover_pct=0.78, air_quality_index=0.85,
        pollutant_concentration_score=0.08, rewilding_potential_score=0.80,
        micro_climate_stability=0.82, invasive_species_pressure=0.12,
        local_food_system_resilience=0.80, regenerative_practice_adoption=0.75,
        community_eco_engagement=0.80, tipping_point_proximity=0.10,
        ecological_connectivity_score=0.82,
    ),
    TerraformingInput(
        territory_id="TF-004", territory_type="coastal", region="LATAM",
        ecosystem_health_score=0.35, biodiversity_index=0.32,
        soil_quality_score=0.40, water_cycle_integrity=0.35,
        urban_heat_island_intensity=0.30, carbon_sequestration_rate=0.32,
        green_cover_pct=0.28, air_quality_index=0.42,
        pollutant_concentration_score=0.55, rewilding_potential_score=0.50,
        micro_climate_stability=0.38, invasive_species_pressure=0.62,
        local_food_system_resilience=0.35, regenerative_practice_adoption=0.30,
        community_eco_engagement=0.38, tipping_point_proximity=0.58,
        ecological_connectivity_score=0.28,
    ),
    TerraformingInput(
        territory_id="TF-005", territory_type="forest", region="MEA",
        ecosystem_health_score=0.88, biodiversity_index=0.90,
        soil_quality_score=0.88, water_cycle_integrity=0.90,
        urban_heat_island_intensity=0.02, carbon_sequestration_rate=0.92,
        green_cover_pct=0.95, air_quality_index=0.92,
        pollutant_concentration_score=0.04, rewilding_potential_score=0.90,
        micro_climate_stability=0.90, invasive_species_pressure=0.08,
        local_food_system_resilience=0.80, regenerative_practice_adoption=0.85,
        community_eco_engagement=0.85, tipping_point_proximity=0.05,
        ecological_connectivity_score=0.92,
    ),
    TerraformingInput(
        territory_id="TF-006", territory_type="wetland", region="EMEA",
        ecosystem_health_score=0.55, biodiversity_index=0.60,
        soil_quality_score=0.52, water_cycle_integrity=0.45,
        urban_heat_island_intensity=0.15, carbon_sequestration_rate=0.55,
        green_cover_pct=0.60, air_quality_index=0.62,
        pollutant_concentration_score=0.38, rewilding_potential_score=0.65,
        micro_climate_stability=0.55, invasive_species_pressure=0.42,
        local_food_system_resilience=0.55, regenerative_practice_adoption=0.50,
        community_eco_engagement=0.55, tipping_point_proximity=0.38,
        ecological_connectivity_score=0.55,
    ),
    TerraformingInput(
        territory_id="TF-007", territory_type="industrial", region="NAMER",
        ecosystem_health_score=0.18, biodiversity_index=0.15,
        soil_quality_score=0.20, water_cycle_integrity=0.22,
        urban_heat_island_intensity=0.80, carbon_sequestration_rate=0.08,
        green_cover_pct=0.08, air_quality_index=0.15,
        pollutant_concentration_score=0.85, rewilding_potential_score=0.12,
        micro_climate_stability=0.18, invasive_species_pressure=0.22,
        local_food_system_resilience=0.12, regenerative_practice_adoption=0.10,
        community_eco_engagement=0.15, tipping_point_proximity=0.90,
        ecological_connectivity_score=0.08,
    ),
    TerraformingInput(
        territory_id="TF-008", territory_type="agricultural", region="APAC",
        ecosystem_health_score=0.48, biodiversity_index=0.45,
        soil_quality_score=0.38, water_cycle_integrity=0.42,
        urban_heat_island_intensity=0.25, carbon_sequestration_rate=0.35,
        green_cover_pct=0.32, air_quality_index=0.52,
        pollutant_concentration_score=0.48, rewilding_potential_score=0.50,
        micro_climate_stability=0.48, invasive_species_pressure=0.35,
        local_food_system_resilience=0.55, regenerative_practice_adoption=0.42,
        community_eco_engagement=0.50, tipping_point_proximity=0.42,
        ecological_connectivity_score=0.40,
    ),
]
