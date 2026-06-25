from dataclasses import dataclass
from typing import Optional


@dataclass
class WaterGeopoliticsInput:
    entity_id: str
    basin_type: str
    region: str
    water_stress_index: float = 0.0
    transboundary_tension: float = 0.0
    upstream_damming_rate: float = 0.0
    climate_precipitation_deficit: float = 0.0
    groundwater_depletion_rate: float = 0.0
    agricultural_water_competition: float = 0.0
    urban_water_demand_surge: float = 0.0
    desalination_dependency: float = 0.0
    treaty_compliance_gap: float = 0.0
    hydro_weapon_risk: float = 0.0
    water_privatization_risk: float = 0.0
    sanitation_collapse_index: float = 0.0
    flood_extreme_exposure: float = 0.0
    glacial_melt_velocity: float = 0.0
    water_infrastructure_fragility: float = 0.0
    cross_border_migration_water_pressure: float = 0.0
    water_data_sovereignty_gap: float = 0.0


class WaterGeopoliticsEngine:
    def _compute_stress_score(self, inp: WaterGeopoliticsInput) -> float:
        return (
            inp.water_stress_index * 0.4
            + inp.groundwater_depletion_rate * 0.35
            + inp.climate_precipitation_deficit * 0.25
        ) * 100

    def _compute_conflict_score(self, inp: WaterGeopoliticsInput) -> float:
        return (
            inp.transboundary_tension * 0.4
            + inp.hydro_weapon_risk * 0.35
            + inp.treaty_compliance_gap * 0.25
        ) * 100

    def _compute_demand_score(self, inp: WaterGeopoliticsInput) -> float:
        return (
            inp.agricultural_water_competition * 0.4
            + inp.urban_water_demand_surge * 0.35
            + inp.cross_border_migration_water_pressure * 0.25
        ) * 100

    def _compute_infrastructure_score(self, inp: WaterGeopoliticsInput) -> float:
        return (
            inp.water_infrastructure_fragility * 0.4
            + inp.sanitation_collapse_index * 0.35
            + inp.water_privatization_risk * 0.25
        ) * 100

    def _compute_composite(
        self,
        stress: float,
        conflict: float,
        demand: float,
        infrastructure: float,
    ) -> float:
        return stress * 0.30 + conflict * 0.25 + demand * 0.25 + infrastructure * 0.20

    def _get_risk(self, composite: float) -> str:
        if composite >= 60:
            return "critical"
        elif composite >= 40:
            return "high"
        elif composite >= 20:
            return "moderate"
        else:
            return "low"

    def _get_pattern(self, inp: WaterGeopoliticsInput) -> str:
        if inp.transboundary_tension >= 0.70 and inp.hydro_weapon_risk >= 0.65:
            return "water_war_imminent"
        if inp.groundwater_depletion_rate >= 0.70 and inp.water_stress_index >= 0.65:
            return "aquifer_collapse"
        if inp.upstream_damming_rate >= 0.70 and inp.treaty_compliance_gap >= 0.65:
            return "upstream_dam_coercion"
        if inp.urban_water_demand_surge >= 0.70 and inp.water_infrastructure_fragility >= 0.65:
            return "urban_water_crisis"
        if inp.glacial_melt_velocity >= 0.70 and inp.climate_precipitation_deficit >= 0.65:
            return "glacial_catastrophe"
        return "none"

    def _get_severity(self, composite: float) -> str:
        if composite >= 75:
            return "water_emergency"
        elif composite >= 50:
            return "hydro_crisis"
        elif composite >= 25:
            return "water_tension"
        else:
            return "water_secure"

    def _get_action(self, risk: str, pattern: str) -> str:
        if risk == "critical":
            return "water_emergency_protocol"
        if risk == "high" and pattern == "water_war_imminent":
            return "diplomatic_water_intervention"
        if risk == "high":
            return "water_resilience_program"
        if risk == "moderate":
            return "hydro_monitoring"
        return "no_action"

    def _get_signal(self, risk: str, pattern: str, severity: str) -> str:
        signals = {
            "critical": "🚨 Crise hydrique critique détectée — intervention immédiate requise",
            "high": "⚠️ Risque hydro-géopolitique élevé — surveillance renforcée nécessaire",
            "moderate": "📊 Tension hydrique modérée — suivi régulier recommandé",
            "low": "✅ Situation hydrique stable — aucune action immédiate requise",
        }
        pattern_signals = {
            "water_war_imminent": " | Conflit armé pour l'eau imminent",
            "aquifer_collapse": " | Effondrement de l'aquifère en cours",
            "upstream_dam_coercion": " | Coercition par barrage en amont détectée",
            "urban_water_crisis": " | Crise d'eau urbaine critique",
            "glacial_catastrophe": " | Catastrophe glaciaire accélérée",
        }
        base = signals.get(risk, "Statut inconnu")
        if pattern in pattern_signals:
            base += pattern_signals[pattern]
        return base

    def _analyze_entity(self, inp: WaterGeopoliticsInput) -> dict:
        stress = self._compute_stress_score(inp)
        conflict = self._compute_conflict_score(inp)
        demand = self._compute_demand_score(inp)
        infrastructure = self._compute_infrastructure_score(inp)
        composite = self._compute_composite(stress, conflict, demand, infrastructure)
        risk = self._get_risk(composite)
        pattern = self._get_pattern(inp)
        severity = self._get_severity(composite)
        action = self._get_action(risk, pattern)
        signal = self._get_signal(risk, pattern, severity)

        return {
            "entity_id": inp.entity_id,
            "region": inp.region,
            "basin_type": inp.basin_type,
            "hydro_risk": risk,
            "hydro_pattern": pattern,
            "hydro_severity": severity,
            "recommended_action": action,
            "stress_score": round(stress, 2),
            "conflict_score": round(conflict, 2),
            "demand_score": round(demand, 2),
            "infrastructure_score": round(infrastructure, 2),
            "hydro_composite": round(composite, 2),
            "is_hydro_crisis": composite >= 60,
            "requires_hydro_intervention": composite >= 40,
            "hydro_signal": signal,
        }

    def analyze(self, entities: list[WaterGeopoliticsInput]) -> dict:
        results = [self._analyze_entity(e) for e in entities]
        total = len(results)
        critical_count = sum(1 for r in results if r["hydro_risk"] == "critical")
        high_count = sum(1 for r in results if r["hydro_risk"] == "high")
        moderate_count = sum(1 for r in results if r["hydro_risk"] == "moderate")
        low_count = sum(1 for r in results if r["hydro_risk"] == "low")
        crisis_count = sum(1 for r in results if r["is_hydro_crisis"])
        intervention_count = sum(1 for r in results if r["requires_hydro_intervention"])
        avg_composite = sum(r["hydro_composite"] for r in results) / total if total else 0.0
        avg_stress = sum(r["stress_score"] for r in results) / total if total else 0.0
        avg_conflict = sum(r["conflict_score"] for r in results) / total if total else 0.0
        avg_demand = sum(r["demand_score"] for r in results) / total if total else 0.0
        avg_infrastructure = sum(r["infrastructure_score"] for r in results) / total if total else 0.0

        return {
            "module": "WaterGeopoliticsEngine",
            "module_id": 318,
            "total_entities": total,
            "critical_count": critical_count,
            "high_count": high_count,
            "moderate_count": moderate_count,
            "low_count": low_count,
            "hydro_crisis_count": crisis_count,
            "requires_intervention_count": intervention_count,
            "avg_composite": round(avg_composite, 2),
            "avg_estimated_hydro_conflict_index": round(avg_composite / 100 * 10, 2),
            "avg_stress_score": round(avg_stress, 2),
            "avg_conflict_score": round(avg_conflict, 2),
            "results": results,
        }
