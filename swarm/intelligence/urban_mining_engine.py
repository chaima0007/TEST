from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class UrbanMiningInput:
    entity_id: str
    electronics_sector: str
    region: str
    ewaste_volume_growth: float
    informal_recycling_rate: float
    toxic_chemical_exposure: float
    heavy_metal_leaching: float
    gold_silver_recovery_rate: float
    rare_earth_extraction: float
    battery_recycling_gap: float
    circular_economy_adoption: float
    producer_take_back_compliance: float
    child_labor_exposure: float
    cross_border_illegal_shipment: float
    consumer_awareness: float
    repair_right_access: float
    collection_infrastructure: float
    data_destruction_security: float
    recycling_technology_gap: float
    regulatory_enforcement: float


@dataclass
class UrbanMiningResult:
    entity_id: str
    electronics_sector: str
    region: str
    ewaste_score: float
    recovery_score: float
    toxicity_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    mining_pattern: str
    severity: str
    recommended_action: str
    signal: str
    ewaste_volume_growth: float
    informal_recycling_rate: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "electronics_sector": self.electronics_sector,
            "region": self.region,
            "ewaste_score": self.ewaste_score,
            "recovery_score": self.recovery_score,
            "toxicity_score": self.toxicity_score,
            "governance_score": self.governance_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "mining_pattern": self.mining_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "ewaste_volume_growth": self.ewaste_volume_growth,
            "informal_recycling_rate": self.informal_recycling_rate,
        }


def _ewaste_score(e: UrbanMiningInput) -> float:
    raw = (
        e.ewaste_volume_growth * 0.4
        + e.battery_recycling_gap * 0.35
        + e.cross_border_illegal_shipment * 0.25
    ) * 100
    return round(raw * 100) / 100


def _recovery_score(e: UrbanMiningInput) -> float:
    raw = (
        e.gold_silver_recovery_rate * 0.4
        + e.rare_earth_extraction * 0.35
        + e.circular_economy_adoption * 0.25
    ) * 100
    return round(raw * 100) / 100


def _toxicity_score(e: UrbanMiningInput) -> float:
    raw = (
        e.toxic_chemical_exposure * 0.4
        + e.heavy_metal_leaching * 0.35
        + e.child_labor_exposure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: UrbanMiningInput) -> float:
    raw = (
        e.regulatory_enforcement * 0.4
        + e.producer_take_back_compliance * 0.35
        + e.collection_infrastructure * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    ewaste: float,
    recovery: float,
    toxicity: float,
    governance: float,
) -> float:
    return round(
        (ewaste * 0.30 + recovery * 0.25 + toxicity * 0.25 + governance * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _mining_pattern(e: UrbanMiningInput) -> str:
    if e.toxic_chemical_exposure > 0.85 and e.heavy_metal_leaching > 0.80:
        return "toxic_ewaste_dumping_crisis"
    if e.gold_silver_recovery_rate > 0.85 and e.rare_earth_extraction > 0.80:
        return "critical_metal_supply_gap"
    if e.informal_recycling_rate > 0.85 and e.child_labor_exposure > 0.80:
        return "informal_sector_health_catastrophe"
    if e.producer_take_back_compliance > 0.80 and e.regulatory_enforcement > 0.75:
        return "extended_producer_responsibility_failure"
    if e.ewaste_volume_growth > 0.80 and e.recycling_technology_gap > 0.75:
        return "planned_obsolescence_acceleration"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_minage_urbain_systémique"
    if composite >= 40:
        return "crise_recyclage_déchets_électroniques_majeure"
    if composite >= 20:
        return "déficit_économie_circulaire_structurel"
    return "surveillance_filière_déchets_électroniques"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_minage_urbain_critique"
    if risk == "high":
        return "renforcement_filière_recyclage_électronique_accéléré"
    if risk == "moderate":
        return "amélioration_collecte_et_traçabilité_déchets"
    return "veille_minage_urbain_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise minage urbain systémique — recyclage déchets électroniques en péril"
    if risk == "high":
        return "🟠 Crise recyclage déchets électroniques majeure détectée"
    if risk == "moderate":
        return "🟡 Déficit économie circulaire structurel actif"
    return "🟢 Filière déchets électroniques sous surveillance"


def analyze_urban_mining(e: UrbanMiningInput) -> UrbanMiningResult:
    ewaste = _ewaste_score(e)
    recovery = _recovery_score(e)
    toxicity = _toxicity_score(e)
    governance = _governance_score(e)
    composite = _composite_score(ewaste, recovery, toxicity, governance)
    risk = _risk_level(composite)
    pattern = _mining_pattern(e)
    sev = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return UrbanMiningResult(
        entity_id=e.entity_id,
        electronics_sector=e.electronics_sector,
        region=e.region,
        ewaste_score=ewaste,
        recovery_score=recovery,
        toxicity_score=toxicity,
        governance_score=governance,
        composite_score=composite,
        risk_level=risk,
        mining_pattern=pattern,
        severity=sev,
        recommended_action=action,
        signal=sig,
        ewaste_volume_growth=e.ewaste_volume_growth,
        informal_recycling_rate=e.informal_recycling_rate,
    )


class UrbanMiningEngine:
    def analyze(self, entities: List[UrbanMiningInput]) -> Dict[str, Any]:
        results = [analyze_urban_mining(e) for e in entities]

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
        results: List[UrbanMiningResult] = None,
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
            "module_id": 410,
            "module_name": "Minage Urbain & Recyclage Déchets Électroniques Intelligence Engine",
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
            "avg_estimated_urban_mining_index": round(avg_composite / 100 * 10, 2),
        }
