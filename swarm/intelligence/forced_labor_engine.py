from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ForcedLaborInput:
    entity_id: str
    labor_sector: str
    region: str
    forced_labor_prevalence: float
    debt_bondage_intensity: float
    document_confiscation: float
    movement_restriction: float
    recruitment_deception: float
    wage_theft: float
    violence_threat: float
    detection_effectiveness: float
    prosecution_rate: float
    victim_support_access: float
    supply_chain_opacity: float
    corporate_accountability: float
    migrant_worker_vulnerability: float
    gender_based_exploitation: float
    child_labor_link: float
    corruption_protection: float
    survivor_compensation: float


@dataclass
class ForcedLaborResult:
    entity_id: str
    labor_sector: str
    region: str
    exploitation_score: float
    detection_score: float
    impunity_score: float
    vulnerability_score: float
    composite_score: float
    risk_level: str
    labor_pattern: str
    severity: str
    recommended_action: str
    signal: str
    forced_labor_prevalence: float
    migrant_worker_vulnerability: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "labor_sector": self.labor_sector,
            "region": self.region,
            "exploitation_score": self.exploitation_score,
            "detection_score": self.detection_score,
            "impunity_score": self.impunity_score,
            "vulnerability_score": self.vulnerability_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "labor_pattern": self.labor_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "forced_labor_prevalence": self.forced_labor_prevalence,
            "migrant_worker_vulnerability": self.migrant_worker_vulnerability,
        }


def _exploitation_score(e: ForcedLaborInput) -> float:
    raw = (
        e.forced_labor_prevalence * 0.4
        + e.debt_bondage_intensity * 0.35
        + e.wage_theft * 0.25
    ) * 100
    return round(raw * 100) / 100


def _detection_score(e: ForcedLaborInput) -> float:
    raw = (
        (1.0 - e.detection_effectiveness) * 0.4
        + e.supply_chain_opacity * 0.35
        + (1.0 - e.victim_support_access) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _impunity_score(e: ForcedLaborInput) -> float:
    raw = (
        (1.0 - e.prosecution_rate) * 0.4
        + e.corruption_protection * 0.35
        + (1.0 - e.corporate_accountability) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _vulnerability_score(e: ForcedLaborInput) -> float:
    raw = (
        e.migrant_worker_vulnerability * 0.4
        + e.gender_based_exploitation * 0.35
        + e.child_labor_link * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    exploitation: float,
    detection: float,
    impunity: float,
    vulnerability: float,
) -> float:
    return round(
        (exploitation * 0.30 + detection * 0.25 + impunity * 0.25 + vulnerability * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _labor_pattern(e: ForcedLaborInput) -> str:
    if e.supply_chain_opacity > 0.80 and e.corporate_accountability < 0.25:
        return "supply_chain_slavery_nexus"
    if e.debt_bondage_intensity > 0.80 and e.recruitment_deception > 0.75:
        return "debt_bondage_trap"
    if e.document_confiscation > 0.80 and e.movement_restriction > 0.75:
        return "domestic_servitude_network"
    if e.gender_based_exploitation > 0.80 and e.violence_threat > 0.75:
        return "sex_trafficking_economy"
    if e.corruption_protection > 0.75 and e.forced_labor_prevalence > 0.70:
        return "prison_labor_exploitation"
    return "supply_chain_slavery_nexus"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_esclavage_moderne_systémique"
    if composite >= 40:
        return "exploitation_grave_travail_forcé"
    if composite >= 20:
        return "vulnérabilité_structurelle_travail_forcé"
    return "surveillance_travail_forcé_active"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_esclavage_moderne_critique"
    if risk == "high":
        return "renforcement_protection_victimes_travail_forcé"
    if risk == "moderate":
        return "surveillance_renforcée_chaînes_approvisionnement"
    return "veille_travail_forcé_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise esclavage moderne systémique — intervention d'urgence requise"
    if risk == "high":
        return "🟠 Exploitation grave travail forcé détectée"
    if risk == "moderate":
        return "🟡 Vulnérabilité structurelle travail forcé active"
    return "🟢 Surveillance travail forcé continue"


def analyze_forced_labor(e: ForcedLaborInput) -> ForcedLaborResult:
    exploitation = _exploitation_score(e)
    detection = _detection_score(e)
    impunity = _impunity_score(e)
    vulnerability = _vulnerability_score(e)
    composite = _composite_score(exploitation, detection, impunity, vulnerability)
    risk = _risk_level(composite)
    pattern = _labor_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return ForcedLaborResult(
        entity_id=e.entity_id,
        labor_sector=e.labor_sector,
        region=e.region,
        exploitation_score=exploitation,
        detection_score=detection,
        impunity_score=impunity,
        vulnerability_score=vulnerability,
        composite_score=composite,
        risk_level=risk,
        labor_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        forced_labor_prevalence=e.forced_labor_prevalence,
        migrant_worker_vulnerability=e.migrant_worker_vulnerability,
    )


class ForcedLaborEngine:
    def analyze(self, entities: List[ForcedLaborInput]) -> Dict[str, Any]:
        results = [analyze_forced_labor(e) for e in entities]

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
            pattern_distribution[r.labor_pattern] = pattern_distribution.get(r.labor_pattern, 0) + 1
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
        results: List[ForcedLaborResult] = None,
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
            "module_id": 418,
            "module_name": "Travail Forcé & Esclavage Moderne Intelligence Engine",
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
            "avg_estimated_forced_labor_index": round(avg_composite / 100 * 10, 2),
        }
