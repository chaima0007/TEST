from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CryptoMiningInput:
    entity_id: str
    mining_type: str
    region: str
    carbon_intensity: float
    renewable_energy_share: float
    coal_dependency: float
    energy_consumption_gwh: float
    water_usage_intensity: float
    cooling_water_stress: float
    e_waste_generation: float
    hardware_lifecycle: float
    grid_strain: float
    local_energy_price_impact: float
    regulatory_compliance: float
    community_opposition: float
    noise_pollution: float
    heat_island_effect: float
    toxic_chemical_use: float
    carbon_credit_offset: float
    energy_efficiency_rating: float


@dataclass
class CryptoMiningResult:
    entity_id: str
    mining_type: str
    region: str
    carbon_score: float
    energy_score: float
    water_score: float
    e_waste_score: float
    composite_score: float
    risk_level: str
    mining_pattern: str
    severity: str
    recommended_action: str
    signal: str
    carbon_intensity: float
    coal_dependency: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "mining_type": self.mining_type,
            "region": self.region,
            "carbon_score": self.carbon_score,
            "energy_score": self.energy_score,
            "water_score": self.water_score,
            "e_waste_score": self.e_waste_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "mining_pattern": self.mining_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "carbon_intensity": self.carbon_intensity,
            "coal_dependency": self.coal_dependency,
        }


def _carbon_score(e: CryptoMiningInput) -> float:
    raw = (
        e.carbon_intensity * 0.45
        + e.coal_dependency * 0.35
        + (1.0 - e.carbon_credit_offset) * 0.20
    ) * 100
    return round(raw * 100) / 100


def _energy_score(e: CryptoMiningInput) -> float:
    raw = (
        e.energy_consumption_gwh * 0.40
        + e.grid_strain * 0.35
        + (1.0 - e.energy_efficiency_rating) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _water_score(e: CryptoMiningInput) -> float:
    raw = (
        e.water_usage_intensity * 0.50
        + e.cooling_water_stress * 0.50
    ) * 100
    return round(raw * 100) / 100


def _e_waste_score(e: CryptoMiningInput) -> float:
    raw = (
        e.e_waste_generation * 0.50
        + (1.0 - e.hardware_lifecycle) * 0.30
        + e.toxic_chemical_use * 0.20
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    carbon: float,
    energy: float,
    water: float,
    e_waste: float,
) -> float:
    return round(
        (carbon * 0.30 + energy * 0.25 + water * 0.25 + e_waste * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _mining_pattern(e: CryptoMiningInput) -> str:
    if e.carbon_intensity > 0.85 and e.coal_dependency > 0.80:
        return "carbon_bomb_mining_operation"
    if e.coal_dependency > 0.80 and e.energy_consumption_gwh > 0.75:
        return "coal_powered_crypto_expansion"
    if e.water_usage_intensity > 0.80 and e.cooling_water_stress > 0.75:
        return "water_crisis_cooling_drain"
    if e.e_waste_generation > 0.80 and e.toxic_chemical_use > 0.75:
        return "e_waste_toxic_dumping"
    if e.grid_strain > 0.80 and e.local_energy_price_impact > 0.75:
        return "energy_grid_destabilization"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_environnementale_minage_critique"
    if composite >= 40:
        return "impact_climatique_minage_élevé"
    if composite >= 20:
        return "pression_environnementale_modérée"
    return "minage_sous_surveillance_environnementale"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_arrêt_minage_polluant"
    if risk == "high":
        return "transition_énergies_renouvelables_minage_accélérée"
    if risk == "moderate":
        return "audit_impact_environnemental_minage_requis"
    return "veille_continue_minage_cryptomonnaie"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise environnementale minage critique — impact planétaire immédiat"
    if risk == "high":
        return "🟠 Impact climatique minage élevé détecté"
    if risk == "moderate":
        return "🟡 Pression environnementale minage modérée active"
    return "🟢 Minage sous surveillance environnementale"


def analyze_crypto_mining(e: CryptoMiningInput) -> CryptoMiningResult:
    carbon = _carbon_score(e)
    energy = _energy_score(e)
    water = _water_score(e)
    e_waste = _e_waste_score(e)
    composite = _composite_score(carbon, energy, water, e_waste)
    risk = _risk_level(composite)
    pattern = _mining_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return CryptoMiningResult(
        entity_id=e.entity_id,
        mining_type=e.mining_type,
        region=e.region,
        carbon_score=carbon,
        energy_score=energy,
        water_score=water,
        e_waste_score=e_waste,
        composite_score=composite,
        risk_level=risk,
        mining_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        carbon_intensity=e.carbon_intensity,
        coal_dependency=e.coal_dependency,
    )


class CryptoMiningEngine:
    def analyze(self, entities: List[CryptoMiningInput]) -> Dict[str, Any]:
        results = [analyze_crypto_mining(e) for e in entities]

        risk_distribution: Dict[str, int] = {}
        pattern_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {}
        action_distribution: Dict[str, int] = {}

        total_composite = 0.0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        low_count = 0

        for r in results:
            risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1
            pattern_distribution[r.mining_pattern] = pattern_distribution.get(r.mining_pattern, 0) + 1
            severity_distribution[r.severity] = severity_distribution.get(r.severity, 0) + 1
            action_distribution[r.recommended_action] = action_distribution.get(r.recommended_action, 0) + 1
            total_composite += r.composite_score
            if r.risk_level == "critical":
                critical_count += 1
            elif r.risk_level == "high":
                high_count += 1
            elif r.risk_level == "moderate":
                moderate_count += 1
            else:
                low_count += 1

        n = len(results) or 1
        avg_composite = round(total_composite / n * 10) / 10

        return self.summary(
            results=results,
            risk_distribution=risk_distribution,
            pattern_distribution=pattern_distribution,
            severity_distribution=severity_distribution,
            action_distribution=action_distribution,
            avg_composite=avg_composite,
            critical_count=critical_count,
            high_count=high_count,
            moderate_count=moderate_count,
            low_count=low_count,
        )

    def summary(
        self,
        results: List[CryptoMiningResult] = None,
        risk_distribution: Dict[str, int] = None,
        pattern_distribution: Dict[str, int] = None,
        severity_distribution: Dict[str, int] = None,
        action_distribution: Dict[str, int] = None,
        avg_composite: float = 0.0,
        critical_count: int = 0,
        high_count: int = 0,
        moderate_count: int = 0,
        low_count: int = 0,
    ) -> Dict[str, Any]:
        results = results or []
        return {
            "module_id": 399,
            "module_name": "Minage Cryptomonnaie & Impact Environnemental Intelligence Engine",
            "total": len(results),
            "critical": critical_count,
            "high": high_count,
            "moderate": moderate_count,
            "low": low_count,
            "avg_composite": avg_composite,
            "pattern_distribution": pattern_distribution or {},
            "risk_distribution": risk_distribution or {},
            "severity_distribution": severity_distribution or {},
            "action_distribution": action_distribution or {},
            "avg_estimated_mining_env_index": round(avg_composite / 100 * 10, 2),
        }
