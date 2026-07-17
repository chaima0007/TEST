from dataclasses import dataclass
from typing import List, Dict, Any


MODULE_ID = 439
MODULE_NAME = "Mobilité Aérienne Urbaine & Véhicules Volants"


@dataclass
class UrbanAirMobilityInput:
    entity_id: str
    vehicle_type: str
    region: str
    collision_avoidance_gap: float
    airspace_management_failure: float
    vertiport_density_deficit: float
    battery_energy_density_risk: float
    noise_impact_residential: float
    weather_operational_limit: float
    cybersecurity_vulnerability: float
    community_acceptance_gap: float
    emergency_landing_protocol_gap: float
    insurance_framework_absence: float
    equity_access_gap: float
    carbon_lifecycle_emission: float
    pilot_certification_gap: float
    air_traffic_controller_overload: float
    regulatory_certification_delay: float
    urban_integration_planning_gap: float
    emergency_medical_use_barrier: float


@dataclass
class UrbanAirMobilityResult:
    entity_id: str
    vehicle_type: str
    region: str
    safety_score: float
    infrastructure_score: float
    regulatory_score: float
    equity_score: float
    composite_score: float
    risk_level: str
    patterns: List[str]
    collision_avoidance_gap: float
    noise_impact_residential: float
    equity_access_gap: float
    regulatory_certification_delay: float
    battery_energy_density_risk: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "vehicle_type": self.vehicle_type,
            "region": self.region,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "safety_score": self.safety_score,
            "infrastructure_score": self.infrastructure_score,
            "regulatory_score": self.regulatory_score,
            "equity_score": self.equity_score,
            "patterns": self.patterns,
            "collision_avoidance_gap": self.collision_avoidance_gap,
            "noise_impact_residential": self.noise_impact_residential,
            "equity_access_gap": self.equity_access_gap,
            "regulatory_certification_delay": self.regulatory_certification_delay,
            "battery_energy_density_risk": self.battery_energy_density_risk,
        }


def _safety_score(e: UrbanAirMobilityInput) -> float:
    raw = (
        e.collision_avoidance_gap
        + e.airspace_management_failure
        + e.battery_energy_density_risk
        + e.emergency_landing_protocol_gap
        + e.cybersecurity_vulnerability
    ) / 5 * 100 * 0.30
    return round(raw * 100) / 100


def _infrastructure_score(e: UrbanAirMobilityInput) -> float:
    raw = (
        e.vertiport_density_deficit
        + e.weather_operational_limit
        + e.urban_integration_planning_gap
        + e.air_traffic_controller_overload
        + e.carbon_lifecycle_emission
    ) / 5 * 100 * 0.25
    return round(raw * 100) / 100


def _regulatory_score(e: UrbanAirMobilityInput) -> float:
    raw = (
        e.pilot_certification_gap
        + e.regulatory_certification_delay
        + e.insurance_framework_absence
        + e.emergency_medical_use_barrier
    ) / 4 * 100 * 0.25
    return round(raw * 100) / 100


def _equity_score(e: UrbanAirMobilityInput) -> float:
    raw = (
        e.noise_impact_residential
        + e.community_acceptance_gap
        + e.equity_access_gap
    ) / 3 * 100 * 0.20
    return round(raw * 100) / 100


def _composite_score(
    safety: float,
    infrastructure: float,
    regulatory: float,
    equity: float,
) -> float:
    return round((safety + infrastructure + regulatory + equity) * 100) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critique"
    if composite >= 40:
        return "élevé"
    if composite >= 20:
        return "modéré"
    return "faible"


def _detect_patterns(e: UrbanAirMobilityInput) -> List[str]:
    patterns = []
    if (e.airspace_management_failure + e.collision_avoidance_gap) / 2 > 0.75:
        patterns.append("airspace_collision_risk")
    if (e.noise_impact_residential + e.community_acceptance_gap) / 2 > 0.70:
        patterns.append("noise_pollution_community_conflict")
    if e.equity_access_gap > 0.75:
        patterns.append("elite_mobility_gentrification")
    if e.battery_energy_density_risk > 0.75:
        patterns.append("battery_fire_safety_gap")
    if (e.regulatory_certification_delay + e.pilot_certification_gap) / 2 > 0.75:
        patterns.append("regulatory_certification_bottleneck")
    return patterns


def analyze_urban_air_mobility(e: UrbanAirMobilityInput) -> UrbanAirMobilityResult:
    safety = _safety_score(e)
    infrastructure = _infrastructure_score(e)
    regulatory = _regulatory_score(e)
    equity = _equity_score(e)
    composite = _composite_score(safety, infrastructure, regulatory, equity)
    risk = _risk_level(composite)
    patterns = _detect_patterns(e)

    return UrbanAirMobilityResult(
        entity_id=e.entity_id,
        vehicle_type=e.vehicle_type,
        region=e.region,
        safety_score=safety,
        infrastructure_score=infrastructure,
        regulatory_score=regulatory,
        equity_score=equity,
        composite_score=composite,
        risk_level=risk,
        patterns=patterns,
        collision_avoidance_gap=e.collision_avoidance_gap,
        noise_impact_residential=e.noise_impact_residential,
        equity_access_gap=e.equity_access_gap,
        regulatory_certification_delay=e.regulatory_certification_delay,
        battery_energy_density_risk=e.battery_energy_density_risk,
    )


class UrbanAirMobilityEngine:
    @classmethod
    def summary(cls, results: List[UrbanAirMobilityResult]) -> Dict[str, Any]:
        n = len(results) or 1
        critique = sum(1 for r in results if r.risk_level == "critique")
        eleve = sum(1 for r in results if r.risk_level == "élevé")
        modere = sum(1 for r in results if r.risk_level == "modéré")
        faible = sum(1 for r in results if r.risk_level == "faible")

        avg_composite = round(sum(r.composite_score for r in results) / n * 10) / 10
        avg_safety = round(sum(r.safety_score for r in results) / n * 10) / 10
        avg_infrastructure = round(sum(r.infrastructure_score for r in results) / n * 10) / 10
        avg_regulatory = round(sum(r.regulatory_score for r in results) / n * 10) / 10
        avg_equity = round(sum(r.equity_score for r in results) / n * 10) / 10

        all_patterns: List[str] = []
        for r in results:
            all_patterns.extend(r.patterns)
        pattern_counts: Dict[str, int] = {}
        for p in all_patterns:
            pattern_counts[p] = pattern_counts.get(p, 0) + 1
        top_patterns = sorted(pattern_counts, key=lambda k: pattern_counts[k], reverse=True)[:5]

        region_counts: Dict[str, int] = {}
        for r in results:
            region_counts[r.region] = region_counts.get(r.region, 0) + 1
        dominant_region = max(region_counts, key=lambda k: region_counts[k]) if region_counts else ""

        avg_estimated_uam_readiness_index = round(avg_composite / 100 * 10, 2)

        return {
            "total": len(results),
            "critique": critique,
            "eleve": eleve,
            "modere": modere,
            "faible": faible,
            "avg_composite": avg_composite,
            "avg_safety": avg_safety,
            "avg_infrastructure": avg_infrastructure,
            "avg_regulatory": avg_regulatory,
            "avg_equity": avg_equity,
            "top_patterns": top_patterns,
            "dominant_region": dominant_region,
            "avg_estimated_uam_readiness_index": avg_estimated_uam_readiness_index,
        }


MOCK_ENTITIES: List[UrbanAirMobilityInput] = [
    # UAM-001 — critique: airspace_collision_risk + battery_fire_safety_gap + regulatory_certification_bottleneck
    UrbanAirMobilityInput(
        entity_id="UAM-001",
        vehicle_type="taxi_aérien_électrique",
        region="Île-de-France",
        collision_avoidance_gap=0.90,
        airspace_management_failure=0.88,
        vertiport_density_deficit=0.78,
        battery_energy_density_risk=0.85,
        noise_impact_residential=0.72,
        weather_operational_limit=0.70,
        cybersecurity_vulnerability=0.75,
        community_acceptance_gap=0.68,
        emergency_landing_protocol_gap=0.82,
        insurance_framework_absence=0.75,
        equity_access_gap=0.70,
        carbon_lifecycle_emission=0.68,
        pilot_certification_gap=0.85,
        air_traffic_controller_overload=0.80,
        regulatory_certification_delay=0.88,
        urban_integration_planning_gap=0.72,
        emergency_medical_use_barrier=0.70,
    ),
    # UAM-002 — critique: airspace_collision_risk + noise_pollution_community_conflict + elite_mobility_gentrification
    UrbanAirMobilityInput(
        entity_id="UAM-002",
        vehicle_type="drone_cargo_urbain",
        region="Grand Paris",
        collision_avoidance_gap=0.85,
        airspace_management_failure=0.82,
        vertiport_density_deficit=0.75,
        battery_energy_density_risk=0.72,
        noise_impact_residential=0.88,
        weather_operational_limit=0.68,
        cybersecurity_vulnerability=0.70,
        community_acceptance_gap=0.80,
        emergency_landing_protocol_gap=0.75,
        insurance_framework_absence=0.70,
        equity_access_gap=0.85,
        carbon_lifecycle_emission=0.65,
        pilot_certification_gap=0.72,
        air_traffic_controller_overload=0.75,
        regulatory_certification_delay=0.70,
        urban_integration_planning_gap=0.68,
        emergency_medical_use_barrier=0.65,
    ),
    # UAM-003 — critique: battery_fire_safety_gap + regulatory_certification_bottleneck
    UrbanAirMobilityInput(
        entity_id="UAM-003",
        vehicle_type="véhicule_volant_autonome",
        region="Lyon Métropole",
        collision_avoidance_gap=0.78,
        airspace_management_failure=0.75,
        vertiport_density_deficit=0.80,
        battery_energy_density_risk=0.90,
        noise_impact_residential=0.65,
        weather_operational_limit=0.72,
        cybersecurity_vulnerability=0.80,
        community_acceptance_gap=0.62,
        emergency_landing_protocol_gap=0.78,
        insurance_framework_absence=0.82,
        equity_access_gap=0.65,
        carbon_lifecycle_emission=0.70,
        pilot_certification_gap=0.88,
        air_traffic_controller_overload=0.72,
        regulatory_certification_delay=0.85,
        urban_integration_planning_gap=0.75,
        emergency_medical_use_barrier=0.80,
    ),
    # UAM-004 — élevé: noise_pollution_community_conflict
    UrbanAirMobilityInput(
        entity_id="UAM-004",
        vehicle_type="hélicoptère_électrique",
        region="Marseille",
        collision_avoidance_gap=0.50,
        airspace_management_failure=0.48,
        vertiport_density_deficit=0.52,
        battery_energy_density_risk=0.55,
        noise_impact_residential=0.80,
        weather_operational_limit=0.52,
        cybersecurity_vulnerability=0.48,
        community_acceptance_gap=0.78,
        emergency_landing_protocol_gap=0.50,
        insurance_framework_absence=0.52,
        equity_access_gap=0.55,
        carbon_lifecycle_emission=0.50,
        pilot_certification_gap=0.52,
        air_traffic_controller_overload=0.50,
        regulatory_certification_delay=0.55,
        urban_integration_planning_gap=0.50,
        emergency_medical_use_barrier=0.48,
    ),
    # UAM-005 — élevé: elite_mobility_gentrification
    UrbanAirMobilityInput(
        entity_id="UAM-005",
        vehicle_type="aéronef_vtol_premium",
        region="Bordeaux",
        collision_avoidance_gap=0.48,
        airspace_management_failure=0.50,
        vertiport_density_deficit=0.52,
        battery_energy_density_risk=0.50,
        noise_impact_residential=0.55,
        weather_operational_limit=0.48,
        cybersecurity_vulnerability=0.50,
        community_acceptance_gap=0.58,
        emergency_landing_protocol_gap=0.48,
        insurance_framework_absence=0.55,
        equity_access_gap=0.82,
        carbon_lifecycle_emission=0.50,
        pilot_certification_gap=0.55,
        air_traffic_controller_overload=0.48,
        regulatory_certification_delay=0.52,
        urban_integration_planning_gap=0.50,
        emergency_medical_use_barrier=0.55,
    ),
    # UAM-006 — modéré: no pattern
    UrbanAirMobilityInput(
        entity_id="UAM-006",
        vehicle_type="navette_aérienne_partagée",
        region="Toulouse",
        collision_avoidance_gap=0.30,
        airspace_management_failure=0.28,
        vertiport_density_deficit=0.32,
        battery_energy_density_risk=0.30,
        noise_impact_residential=0.28,
        weather_operational_limit=0.32,
        cybersecurity_vulnerability=0.28,
        community_acceptance_gap=0.30,
        emergency_landing_protocol_gap=0.28,
        insurance_framework_absence=0.32,
        equity_access_gap=0.30,
        carbon_lifecycle_emission=0.28,
        pilot_certification_gap=0.30,
        air_traffic_controller_overload=0.32,
        regulatory_certification_delay=0.28,
        urban_integration_planning_gap=0.30,
        emergency_medical_use_barrier=0.32,
    ),
    # UAM-007 — faible: no pattern
    UrbanAirMobilityInput(
        entity_id="UAM-007",
        vehicle_type="drone_surveillance_léger",
        region="Nantes",
        collision_avoidance_gap=0.10,
        airspace_management_failure=0.12,
        vertiport_density_deficit=0.10,
        battery_energy_density_risk=0.12,
        noise_impact_residential=0.10,
        weather_operational_limit=0.12,
        cybersecurity_vulnerability=0.10,
        community_acceptance_gap=0.12,
        emergency_landing_protocol_gap=0.10,
        insurance_framework_absence=0.12,
        equity_access_gap=0.10,
        carbon_lifecycle_emission=0.12,
        pilot_certification_gap=0.10,
        air_traffic_controller_overload=0.12,
        regulatory_certification_delay=0.10,
        urban_integration_planning_gap=0.12,
        emergency_medical_use_barrier=0.10,
    ),
    # UAM-008 — faible: no pattern
    UrbanAirMobilityInput(
        entity_id="UAM-008",
        vehicle_type="planeur_urbain_silencieux",
        region="Bretagne",
        collision_avoidance_gap=0.12,
        airspace_management_failure=0.10,
        vertiport_density_deficit=0.12,
        battery_energy_density_risk=0.10,
        noise_impact_residential=0.12,
        weather_operational_limit=0.10,
        cybersecurity_vulnerability=0.12,
        community_acceptance_gap=0.10,
        emergency_landing_protocol_gap=0.12,
        insurance_framework_absence=0.10,
        equity_access_gap=0.12,
        carbon_lifecycle_emission=0.10,
        pilot_certification_gap=0.12,
        air_traffic_controller_overload=0.10,
        regulatory_certification_delay=0.12,
        urban_integration_planning_gap=0.10,
        emergency_medical_use_barrier=0.12,
    ),
]


def get_engine_data() -> Dict[str, Any]:
    results = [analyze_urban_air_mobility(e) for e in MOCK_ENTITIES]
    summary = UrbanAirMobilityEngine.summary(results)
    return {
        "entities": [r.to_dict() for r in results],
        "summary": summary,
        "module_id": MODULE_ID,
        "module_name": MODULE_NAME,
    }
