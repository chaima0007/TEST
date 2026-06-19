from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class HyperconnectivityInput:
    entity_id: str
    infrastructure_layer: str
    region: str
    node_density: float
    interconnection_depth: float
    single_point_concentration: float
    cascading_vulnerability: float
    network_centrality_risk: float
    latency_criticality: float
    bandwidth_saturation: float
    protocol_obsolescence: float
    dependency_depth: float
    redundancy_deficit: float
    cyber_attack_surface: float
    supply_chain_digital_exposure: float
    cloud_concentration_risk: float
    data_sovereignty_gap: float
    patch_velocity: float
    zero_day_exposure: float
    infrastructure_age: float


@dataclass
class HyperconnectivityResult:
    entity_id: str
    region: str
    infrastructure_layer: str
    fragility_risk: str
    fragility_pattern: str
    fragility_severity: str
    recommended_action: str
    topology_score: float
    dependency_score: float
    security_score: float
    sovereignty_score: float
    fragility_composite: float
    is_in_fragility_crisis: bool
    requires_infrastructure_intervention: bool
    fragility_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "infrastructure_layer": self.infrastructure_layer,
            "fragility_risk": self.fragility_risk,
            "fragility_pattern": self.fragility_pattern,
            "fragility_severity": self.fragility_severity,
            "recommended_action": self.recommended_action,
            "topology_score": self.topology_score,
            "dependency_score": self.dependency_score,
            "security_score": self.security_score,
            "sovereignty_score": self.sovereignty_score,
            "fragility_composite": self.fragility_composite,
            "is_in_fragility_crisis": self.is_in_fragility_crisis,
            "requires_infrastructure_intervention": self.requires_infrastructure_intervention,
            "fragility_signal": self.fragility_signal,
        }


def _topology_score(inp: HyperconnectivityInput) -> float:
    return (
        inp.single_point_concentration * 0.4
        + inp.cascading_vulnerability * 0.35
        + inp.network_centrality_risk * 0.25
    ) * 100


def _dependency_score(inp: HyperconnectivityInput) -> float:
    return (
        inp.dependency_depth * 0.4
        + inp.redundancy_deficit * 0.35
        + inp.cloud_concentration_risk * 0.25
    ) * 100


def _security_score(inp: HyperconnectivityInput) -> float:
    return (
        inp.cyber_attack_surface * 0.35
        + inp.zero_day_exposure * 0.35
        + (1 - inp.patch_velocity) * 0.30
    ) * 100


def _sovereignty_score(inp: HyperconnectivityInput) -> float:
    return (
        inp.data_sovereignty_gap * 0.4
        + inp.supply_chain_digital_exposure * 0.35
        + inp.protocol_obsolescence * 0.25
    ) * 100


def _composite(topo: float, dep: float, sec: float, sov: float) -> float:
    return topo * 0.30 + dep * 0.25 + sec * 0.25 + sov * 0.20


def _fragility_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _fragility_pattern(inp: HyperconnectivityInput) -> str:
    if inp.cascading_vulnerability >= 0.65 and inp.single_point_concentration >= 0.60:
        return "cascade_failure_risk"
    if inp.dependency_depth >= 0.65 and inp.redundancy_deficit >= 0.60:
        return "dependency_collapse"
    if inp.cyber_attack_surface >= 0.65 and inp.zero_day_exposure >= 0.55:
        return "cyber_systemic_attack"
    if inp.data_sovereignty_gap >= 0.65 and inp.cloud_concentration_risk >= 0.55:
        return "sovereignty_breach"
    if inp.protocol_obsolescence >= 0.65 and inp.infrastructure_age >= 0.65:
        return "infrastructure_obsolescence"
    return "none"


def _fragility_severity(composite: float) -> str:
    if composite >= 75:
        return "fragile_critical"
    if composite >= 50:
        return "high_fragility"
    if composite >= 25:
        return "developing_vulnerability"
    return "resilient_infrastructure"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "infrastructure_emergency"
    if risk == "high" and pattern == "cascade_failure_risk":
        return "cascade_circuit_breaker"
    if risk == "high":
        return "fragility_hardening"
    if risk == "moderate":
        return "infrastructure_monitoring"
    return "no_action"


def _fragility_signal(inp: HyperconnectivityInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — point unique concentration {int(inp.single_point_concentration * 100)}%"
            f" — vulnérabilité cascade {int(inp.cascading_vulnerability * 100)}%"
            f" — composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — profondeur dépendance {int(inp.dependency_depth * 100)}%"
            f" — surface cyber {int(inp.cyber_attack_surface * 100)}%"
            f" — composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — exposition souveraineté {int(inp.data_sovereignty_gap * 100)}%"
            f" — composite {comp_int}"
        )
    return "Infrastructure hyperconnectée résiliente — redondance suffisante, souveraineté préservée"


def analyze(inp: HyperconnectivityInput) -> HyperconnectivityResult:
    topo = _topology_score(inp)
    dep = _dependency_score(inp)
    sec = _security_score(inp)
    sov = _sovereignty_score(inp)
    comp = _composite(topo, dep, sec, sov)
    risk = _fragility_risk(comp)
    pattern = _fragility_pattern(inp)
    severity = _fragility_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _fragility_signal(inp, risk, comp)

    return HyperconnectivityResult(
        entity_id=inp.entity_id,
        region=inp.region,
        infrastructure_layer=inp.infrastructure_layer,
        fragility_risk=risk,
        fragility_pattern=pattern,
        fragility_severity=severity,
        recommended_action=action,
        topology_score=round(topo, 2),
        dependency_score=round(dep, 2),
        security_score=round(sec, 2),
        sovereignty_score=round(sov, 2),
        fragility_composite=round(comp, 2),
        is_in_fragility_crisis=comp >= 60,
        requires_infrastructure_intervention=comp >= 40,
        fragility_signal=signal,
    )


class HyperconnectivityFragilityEngine:
    def __init__(self) -> None:
        self.results: List[HyperconnectivityResult] = []

    def run(self, inputs: List[HyperconnectivityInput]) -> Dict[str, Any]:
        self.results = [analyze(inp) for inp in inputs]
        return self.summarize()

    def summarize(self) -> Dict[str, Any]:
        n = len(self.results)
        if n == 0:
            return {"total": 0}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_topology = 0.0
        total_dependency = 0.0
        total_security = 0.0
        total_sovereignty = 0.0
        fragility_crisis_count = 0
        infrastructure_intervention_count = 0

        for r in self.results:
            risk_counts[r.fragility_risk] = risk_counts.get(r.fragility_risk, 0) + 1
            pattern_counts[r.fragility_pattern] = pattern_counts.get(r.fragility_pattern, 0) + 1
            severity_counts[r.fragility_severity] = severity_counts.get(r.fragility_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.fragility_composite
            total_topology += r.topology_score
            total_dependency += r.dependency_score
            total_security += r.security_score
            total_sovereignty += r.sovereignty_score
            if r.is_in_fragility_crisis:
                fragility_crisis_count += 1
            if r.requires_infrastructure_intervention:
                infrastructure_intervention_count += 1

        avg_composite = total_composite / n
        avg_estimated_fragility_index = round(avg_composite / 100 * 10, 2)

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_fragility_composite": round(avg_composite, 1),
            "fragility_crisis_count": fragility_crisis_count,
            "infrastructure_intervention_count": infrastructure_intervention_count,
            "avg_topology_score": round(total_topology / n, 1),
            "avg_dependency_score": round(total_dependency / n, 1),
            "avg_security_score": round(total_security / n, 1),
            "avg_sovereignty_score": round(total_sovereignty / n, 1),
            "avg_estimated_fragility_index": avg_estimated_fragility_index,
        }
