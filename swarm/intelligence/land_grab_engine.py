from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class LandGrabInput:
    entity_id: str
    land_type: str
    region: str
    land_concentration: float
    smallholder_displacement: float
    indigenous_rights_violation: float
    food_production_loss: float
    water_access_loss: float
    corporate_opacity: float
    contract_coercion: float
    community_consent_absence: float
    legal_protection_gap: float
    corruption_index: float
    monoculture_expansion: float
    biodiversity_loss: float
    debt_leverage: float
    export_orientation: float
    worker_exploitation: float
    climate_vulnerability: float
    conflict_intensity: float


@dataclass
class LandGrabResult:
    entity_id: str
    land_type: str
    region: str
    dispossession_score: float
    food_sovereignty_score: float
    violence_score: float
    governance_score: float
    composite_score: float
    risk_level: str
    land_pattern: str
    severity: str
    recommended_action: str
    signal: str
    land_concentration: float
    smallholder_displacement: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "land_type": self.land_type,
            "region": self.region,
            "dispossession_score": self.dispossession_score,
            "food_sovereignty_score": self.food_sovereignty_score,
            "violence_score": self.violence_score,
            "governance_score": self.governance_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "land_pattern": self.land_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "land_concentration": self.land_concentration,
            "smallholder_displacement": self.smallholder_displacement,
        }


def _dispossession_score(e: LandGrabInput) -> float:
    raw = (
        e.land_concentration * 0.4
        + e.smallholder_displacement * 0.35
        + e.indigenous_rights_violation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _food_sovereignty_score(e: LandGrabInput) -> float:
    raw = (
        e.food_production_loss * 0.4
        + e.monoculture_expansion * 0.35
        + e.export_orientation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _violence_score(e: LandGrabInput) -> float:
    raw = (
        e.conflict_intensity * 0.4
        + e.contract_coercion * 0.35
        + e.worker_exploitation * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(e: LandGrabInput) -> float:
    raw = (
        e.corruption_index * 0.4
        + e.legal_protection_gap * 0.35
        + e.community_consent_absence * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    dispossession: float,
    food_sovereignty: float,
    violence: float,
    governance: float,
) -> float:
    return round(
        (dispossession * 0.30 + food_sovereignty * 0.25 + violence * 0.25 + governance * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _land_pattern(e: LandGrabInput) -> str:
    if e.land_concentration > 0.80 and e.corporate_opacity > 0.75:
        return "foreign_sovereign_land_capture"
    if e.monoculture_expansion > 0.80 and e.smallholder_displacement > 0.75:
        return "corporate_agribusiness_displacement"
    if e.climate_vulnerability > 0.80 and e.conflict_intensity > 0.75:
        return "climate_migration_land_conflict"
    if e.indigenous_rights_violation > 0.80 and e.community_consent_absence > 0.75:
        return "indigenous_territory_seizure"
    if e.debt_leverage > 0.80 and e.export_orientation > 0.75:
        return "green_colonialism_trap"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_accaparement_terres_systémique"
    if composite >= 40:
        return "crise_souveraineté_alimentaire_majeure"
    if composite >= 20:
        return "dépossession_foncière_structurelle"
    return "pression_foncière_sous_surveillance"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_protection_terres_critiques"
    if risk == "high":
        return "réforme_foncière_accélérée_communautés_vulnérables"
    if risk == "moderate":
        return "renforcement_droits_fonciers_souveraineté_alimentaire"
    return "veille_accaparement_terres_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise accaparement terres systémique — souveraineté alimentaire en péril"
    if risk == "high":
        return "🟠 Crise souveraineté alimentaire majeure détectée"
    if risk == "moderate":
        return "🟡 Dépossession foncière structurelle active"
    return "🟢 Pression foncière sous surveillance"


def analyze_land_grab(e: LandGrabInput) -> LandGrabResult:
    dispossession = _dispossession_score(e)
    food_sovereignty = _food_sovereignty_score(e)
    violence = _violence_score(e)
    governance = _governance_score(e)
    composite = _composite_score(dispossession, food_sovereignty, violence, governance)
    risk = _risk_level(composite)
    pattern = _land_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return LandGrabResult(
        entity_id=e.entity_id,
        land_type=e.land_type,
        region=e.region,
        dispossession_score=dispossession,
        food_sovereignty_score=food_sovereignty,
        violence_score=violence,
        governance_score=governance,
        composite_score=composite,
        risk_level=risk,
        land_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        land_concentration=e.land_concentration,
        smallholder_displacement=e.smallholder_displacement,
    )


class LandGrabEngine:
    def analyze(self, entities: List[LandGrabInput]) -> Dict[str, Any]:
        results = [analyze_land_grab(e) for e in entities]

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
            pattern_distribution[r.land_pattern] = pattern_distribution.get(r.land_pattern, 0) + 1
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
        results: List[LandGrabResult] = None,
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
            "module_id": 403,
            "module_name": "Accaparement Terres & Déplacement Agricole Intelligence Engine",
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
            "avg_estimated_land_grab_index": round(avg_composite / 100 * 10, 2),
        }
