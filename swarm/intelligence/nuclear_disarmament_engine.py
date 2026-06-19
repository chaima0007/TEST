from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class NuclearDisarmamentInput:
    entity_id: str
    actor_type: str
    region: str
    npt_compliance_gap: float
    arsenal_modernization_rate: float
    first_strike_doctrine_risk: float
    tactical_weapons_proliferation: float
    verification_mechanism_failure: float
    treaty_withdrawal_risk: float
    nuclear_sharing_arrangement_risk: float
    cyber_vulnerability_command: float
    miscalculation_risk: float
    civilian_population_exposure: float
    nuclear_winter_contribution: float
    iaea_safeguard_gap: float
    disarmament_commitment_gap: float
    dual_use_technology_spread: float
    space_nuclear_weapon_risk: float
    radiological_terrorism_risk: float
    nuclear_energy_weapon_nexus: float


@dataclass
class NuclearDisarmamentResult:
    entity_id: str
    actor_type: str
    region: str
    proliferation_score: float
    treaty_score: float
    deterrence_score: float
    humanitarian_score: float
    composite_score: float
    risk_level: str
    nuclear_pattern: str
    severity: str
    recommended_action: str
    signal: str
    npt_compliance_gap: float
    iaea_safeguard_gap: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "actor_type": self.actor_type,
            "region": self.region,
            "proliferation_score": self.proliferation_score,
            "treaty_score": self.treaty_score,
            "deterrence_score": self.deterrence_score,
            "humanitarian_score": self.humanitarian_score,
            "composite_score": self.composite_score,
            "risk_level": self.risk_level,
            "nuclear_pattern": self.nuclear_pattern,
            "severity": self.severity,
            "recommended_action": self.recommended_action,
            "signal": self.signal,
            "npt_compliance_gap": self.npt_compliance_gap,
            "iaea_safeguard_gap": self.iaea_safeguard_gap,
        }


def _proliferation_score(e: NuclearDisarmamentInput) -> float:
    raw = (
        e.npt_compliance_gap * 0.4
        + e.tactical_weapons_proliferation * 0.35
        + e.dual_use_technology_spread * 0.25
    ) * 100
    return round(raw * 100) / 100


def _treaty_score(e: NuclearDisarmamentInput) -> float:
    raw = (
        e.treaty_withdrawal_risk * 0.4
        + e.verification_mechanism_failure * 0.35
        + e.disarmament_commitment_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _deterrence_score(e: NuclearDisarmamentInput) -> float:
    raw = (
        e.first_strike_doctrine_risk * 0.4
        + e.miscalculation_risk * 0.35
        + e.cyber_vulnerability_command * 0.25
    ) * 100
    return round(raw * 100) / 100


def _humanitarian_score(e: NuclearDisarmamentInput) -> float:
    raw = (
        e.civilian_population_exposure * 0.4
        + e.nuclear_winter_contribution * 0.35
        + e.radiological_terrorism_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite_score(
    proliferation: float,
    treaty: float,
    deterrence: float,
    humanitarian: float,
) -> float:
    return round(
        (proliferation * 0.30 + treaty * 0.25 + deterrence * 0.25 + humanitarian * 0.20) * 100
    ) / 100


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _nuclear_pattern(e: NuclearDisarmamentInput) -> str:
    if e.treaty_withdrawal_risk > 0.85 and e.verification_mechanism_failure > 0.80:
        return "treaty_collapse_cascade"
    if e.npt_compliance_gap > 0.85 and e.tactical_weapons_proliferation > 0.80:
        return "nuclear_state_proliferation"
    if e.first_strike_doctrine_risk > 0.85 and e.nuclear_sharing_arrangement_risk > 0.80:
        return "tactical_weapon_doctrine_shift"
    if e.cyber_vulnerability_command > 0.80 and e.miscalculation_risk > 0.75:
        return "cyber_nuclear_command_risk"
    if e.civilian_population_exposure > 0.80 and e.nuclear_winter_contribution > 0.75:
        return "humanitarian_impact_denial"
    return "none"


def _severity(composite: float) -> str:
    if composite >= 60:
        return "crise_nucleaire_systemique_critique"
    if composite >= 40:
        return "risque_proliferation_majeur"
    if composite >= 20:
        return "tension_desarmement_structurelle"
    return "surveillance_controle_armements"


def _recommended_action(risk: str) -> str:
    if risk == "critical":
        return "intervention_urgente_desarmement_nucleaire"
    if risk == "high":
        return "renforcement_traites_verification_acceleree"
    if risk == "moderate":
        return "dialogue_controle_armements_renforce"
    return "veille_nucleaire_continue"


def _signal(risk: str) -> str:
    if risk == "critical":
        return "🔴 Crise nucléaire systémique — désarmement en péril immédiat"
    if risk == "high":
        return "🟠 Risque de prolifération majeur détecté"
    if risk == "moderate":
        return "🟡 Tension structurelle contrôle des armements active"
    return "🟢 Contrôle armements sous surveillance"


def analyze_nuclear_disarmament(e: NuclearDisarmamentInput) -> NuclearDisarmamentResult:
    proliferation = _proliferation_score(e)
    treaty = _treaty_score(e)
    deterrence = _deterrence_score(e)
    humanitarian = _humanitarian_score(e)
    composite = _composite_score(proliferation, treaty, deterrence, humanitarian)
    risk = _risk_level(composite)
    pattern = _nuclear_pattern(e)
    severity = _severity(composite)
    action = _recommended_action(risk)
    sig = _signal(risk)

    return NuclearDisarmamentResult(
        entity_id=e.entity_id,
        actor_type=e.actor_type,
        region=e.region,
        proliferation_score=proliferation,
        treaty_score=treaty,
        deterrence_score=deterrence,
        humanitarian_score=humanitarian,
        composite_score=composite,
        risk_level=risk,
        nuclear_pattern=pattern,
        severity=severity,
        recommended_action=action,
        signal=sig,
        npt_compliance_gap=e.npt_compliance_gap,
        iaea_safeguard_gap=e.iaea_safeguard_gap,
    )


class NuclearDisarmamentEngine:
    def analyze(self, entities: List[NuclearDisarmamentInput]) -> Dict[str, Any]:
        results = [analyze_nuclear_disarmament(e) for e in entities]

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
            pattern_distribution[r.nuclear_pattern] = pattern_distribution.get(r.nuclear_pattern, 0) + 1
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
        results: List[NuclearDisarmamentResult] = None,
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
            "module_id": 438,
            "module_name": "Désarmement Nucléaire & Contrôle des Armements Intelligence Engine",
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
            "avg_estimated_nuclear_risk_index": round(avg_composite / 100 * 10, 2),
        }
