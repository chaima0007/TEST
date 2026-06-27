from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class NetworkInput:
    network_id: str
    network_type: str  # supply_chain/financial_market/social_influence/infrastructure/innovation_cluster/regulatory_ecosystem/talent_market/geopolitical_alliance
    region: str
    connectivity_density: float
    cascade_vulnerability_score: float
    attractor_basin_stability: float
    phase_transition_proximity: float
    resilience_redundancy_score: float
    small_world_coefficient: float
    clustering_coefficient: float
    hub_concentration_risk: float
    information_flow_efficiency: float
    self_organized_criticality_index: float
    network_modularity_score: float
    recovery_speed_score: float
    interdependency_depth: float
    perturbation_propagation_rate: float
    adaptive_capacity_score: float
    topology_robustness: float
    emergent_behavior_predictability: float


class NetworkResult:
    def __init__(
        self,
        network_id: str,
        network_type: str,
        region: str,
        topology_score: float,
        dynamics_score: float,
        resilience_score: float,
        emergence_score: float,
        network_composite: float,
        network_risk: str,
        network_pattern: str,
        network_severity: str,
        recommended_action: str,
        network_signal: str,
        estimated_cascade_risk_index: float,
        cascade_vulnerability_score: float,
        phase_transition_proximity: float,
        hub_concentration_risk: float,
    ):
        self.network_id = network_id
        self.network_type = network_type
        self.region = region
        self.topology_score = topology_score
        self.dynamics_score = dynamics_score
        self.resilience_score = resilience_score
        self.emergence_score = emergence_score
        self.network_composite = network_composite
        self.network_risk = network_risk
        self.network_pattern = network_pattern
        self.network_severity = network_severity
        self.recommended_action = recommended_action
        self.network_signal = network_signal
        self.estimated_cascade_risk_index = estimated_cascade_risk_index
        self._cascade_vulnerability_score = cascade_vulnerability_score
        self._phase_transition_proximity = phase_transition_proximity
        self._hub_concentration_risk = hub_concentration_risk

    def to_dict(self) -> Dict[str, Any]:
        # Exactly 15 keys
        return {
            "network_id": self.network_id,
            "network_type": self.network_type,
            "region": self.region,
            "topology_score": self.topology_score,
            "dynamics_score": self.dynamics_score,
            "resilience_score": self.resilience_score,
            "emergence_score": self.emergence_score,
            "network_composite": self.network_composite,
            "network_risk": self.network_risk,
            "network_pattern": self.network_pattern,
            "network_severity": self.network_severity,
            "recommended_action": self.recommended_action,
            "network_signal": self.network_signal,
            "estimated_cascade_risk_index": self.estimated_cascade_risk_index,
            "cascade_vulnerability_score": self._cascade_vulnerability_score,
        }


MOCK_NETWORKS = [
    # NT-001 supply_chain EMEA — critical/cascade_failure
    NetworkInput(
        network_id="NT-001", network_type="supply_chain", region="EMEA",
        connectivity_density=0.75, cascade_vulnerability_score=0.88,
        attractor_basin_stability=0.15, phase_transition_proximity=0.82,
        resilience_redundancy_score=0.12, small_world_coefficient=0.20,
        clustering_coefficient=0.30, hub_concentration_risk=0.90,
        information_flow_efficiency=0.22, self_organized_criticality_index=0.85,
        network_modularity_score=0.18, recovery_speed_score=0.10,
        interdependency_depth=0.88, perturbation_propagation_rate=0.92,
        adaptive_capacity_score=0.08, topology_robustness=0.12,
        emergent_behavior_predictability=0.10,
    ),
    # NT-002 financial_market NAMER — low
    NetworkInput(
        network_id="NT-002", network_type="financial_market", region="NAMER",
        connectivity_density=0.55, cascade_vulnerability_score=0.12,
        attractor_basin_stability=0.88, phase_transition_proximity=0.10,
        resilience_redundancy_score=0.85, small_world_coefficient=0.78,
        clustering_coefficient=0.80, hub_concentration_risk=0.15,
        information_flow_efficiency=0.88, self_organized_criticality_index=0.20,
        network_modularity_score=0.82, recovery_speed_score=0.90,
        interdependency_depth=0.25, perturbation_propagation_rate=0.12,
        adaptive_capacity_score=0.88, topology_robustness=0.85,
        emergent_behavior_predictability=0.90,
    ),
    # NT-003 social_influence APAC — high/phase_transition_collapse
    NetworkInput(
        network_id="NT-003", network_type="social_influence", region="APAC",
        connectivity_density=0.60, cascade_vulnerability_score=0.55,
        attractor_basin_stability=0.35, phase_transition_proximity=0.75,
        resilience_redundancy_score=0.42, small_world_coefficient=0.52,
        clustering_coefficient=0.50, hub_concentration_risk=0.50,
        information_flow_efficiency=0.50, self_organized_criticality_index=0.62,
        network_modularity_score=0.45, recovery_speed_score=0.42,
        interdependency_depth=0.58, perturbation_propagation_rate=0.58,
        adaptive_capacity_score=0.40, topology_robustness=0.45,
        emergent_behavior_predictability=0.35,
    ),
    # NT-004 infrastructure LATAM — low
    NetworkInput(
        network_id="NT-004", network_type="infrastructure", region="LATAM",
        connectivity_density=0.50, cascade_vulnerability_score=0.18,
        attractor_basin_stability=0.82, phase_transition_proximity=0.12,
        resilience_redundancy_score=0.80, small_world_coefficient=0.72,
        clustering_coefficient=0.75, hub_concentration_risk=0.20,
        information_flow_efficiency=0.80, self_organized_criticality_index=0.22,
        network_modularity_score=0.78, recovery_speed_score=0.82,
        interdependency_depth=0.30, perturbation_propagation_rate=0.18,
        adaptive_capacity_score=0.80, topology_robustness=0.80,
        emergent_behavior_predictability=0.82,
    ),
    # NT-005 innovation_cluster EMEA — critical/hub_fragility
    NetworkInput(
        network_id="NT-005", network_type="innovation_cluster", region="EMEA",
        connectivity_density=0.70, cascade_vulnerability_score=0.72,
        attractor_basin_stability=0.20, phase_transition_proximity=0.68,
        resilience_redundancy_score=0.18, small_world_coefficient=0.25,
        clustering_coefficient=0.28, hub_concentration_risk=0.92,
        information_flow_efficiency=0.30, self_organized_criticality_index=0.78,
        network_modularity_score=0.20, recovery_speed_score=0.15,
        interdependency_depth=0.80, perturbation_propagation_rate=0.80,
        adaptive_capacity_score=0.15, topology_robustness=0.15,
        emergent_behavior_predictability=0.15,
    ),
    # NT-006 regulatory_ecosystem MEA — moderate
    NetworkInput(
        network_id="NT-006", network_type="regulatory_ecosystem", region="MEA",
        connectivity_density=0.45, cascade_vulnerability_score=0.32,
        attractor_basin_stability=0.65, phase_transition_proximity=0.30,
        resilience_redundancy_score=0.62, small_world_coefficient=0.60,
        clustering_coefficient=0.62, hub_concentration_risk=0.35,
        information_flow_efficiency=0.62, self_organized_criticality_index=0.40,
        network_modularity_score=0.60, recovery_speed_score=0.62,
        interdependency_depth=0.42, perturbation_propagation_rate=0.32,
        adaptive_capacity_score=0.60, topology_robustness=0.62,
        emergent_behavior_predictability=0.62,
    ),
    # NT-007 talent_market NAMER — high/complexity_overload
    NetworkInput(
        network_id="NT-007", network_type="talent_market", region="NAMER",
        connectivity_density=0.55, cascade_vulnerability_score=0.48,
        attractor_basin_stability=0.42, phase_transition_proximity=0.45,
        resilience_redundancy_score=0.45, small_world_coefficient=0.48,
        clustering_coefficient=0.48, hub_concentration_risk=0.52,
        information_flow_efficiency=0.48, self_organized_criticality_index=0.88,
        network_modularity_score=0.44, recovery_speed_score=0.46,
        interdependency_depth=0.55, perturbation_propagation_rate=0.48,
        adaptive_capacity_score=0.44, topology_robustness=0.46,
        emergent_behavior_predictability=0.25,
    ),
    # NT-008 geopolitical_alliance APAC — low
    NetworkInput(
        network_id="NT-008", network_type="geopolitical_alliance", region="APAC",
        connectivity_density=0.48, cascade_vulnerability_score=0.15,
        attractor_basin_stability=0.85, phase_transition_proximity=0.12,
        resilience_redundancy_score=0.82, small_world_coefficient=0.75,
        clustering_coefficient=0.78, hub_concentration_risk=0.18,
        information_flow_efficiency=0.82, self_organized_criticality_index=0.18,
        network_modularity_score=0.80, recovery_speed_score=0.85,
        interdependency_depth=0.28, perturbation_propagation_rate=0.15,
        adaptive_capacity_score=0.82, topology_robustness=0.82,
        emergent_behavior_predictability=0.85,
    ),
]


def _topology_score(n: NetworkInput) -> float:
    s = 0.0
    # hub_concentration_risk inverted
    s += (1.0 - n.hub_concentration_risk) * 40
    s += n.clustering_coefficient * 35
    s += n.network_modularity_score * 25
    # Invert: higher raw topology quality = lower risk score
    raw_quality = s / 100.0  # 0–1
    risk_score = (1.0 - raw_quality) * 100.0
    return min(round(risk_score, 2), 100.0)


def _dynamics_score(n: NetworkInput) -> float:
    # cascade_vulnerability_score inverted, perturbation_propagation_rate inverted, phase_transition_proximity inverted
    # Higher values = higher risk
    s = (n.cascade_vulnerability_score * 40 +
         n.perturbation_propagation_rate * 35 +
         n.phase_transition_proximity * 25)
    return min(round(s, 2), 100.0)


def _resilience_score(n: NetworkInput) -> float:
    # resilience_redundancy_score, recovery_speed_score, adaptive_capacity_score — higher = better = lower risk
    quality = (n.resilience_redundancy_score * 40 +
               n.recovery_speed_score * 35 +
               n.adaptive_capacity_score * 25)
    risk_score = (1.0 - quality / 100.0) * 100.0
    return min(round(risk_score, 2), 100.0)


def _emergence_score(n: NetworkInput) -> float:
    # self_organized_criticality_index inverted (too much = risky)
    # emergent_behavior_predictability — higher = better = lower risk
    # attractor_basin_stability — higher = better = lower risk
    quality = ((1.0 - n.self_organized_criticality_index) * 40 +
               n.emergent_behavior_predictability * 35 +
               n.attractor_basin_stability * 25)
    risk_score = (1.0 - quality / 100.0) * 100.0
    return min(round(risk_score, 2), 100.0)


def _composite(topo: float, dyn: float, res: float, emg: float) -> float:
    return min(round(topo * 0.30 + dyn * 0.25 + res * 0.25 + emg * 0.20, 2), 100.0)


def _risk(c: float) -> str:
    if c >= 60:
        return "critical"
    if c >= 40:
        return "high"
    if c >= 20:
        return "moderate"
    return "low"


def _pattern(n: NetworkInput, risk: str) -> str:
    if n.cascade_vulnerability_score >= 0.80 and n.perturbation_propagation_rate >= 0.80:
        return "cascade_failure"
    if n.phase_transition_proximity >= 0.70 and n.attractor_basin_stability <= 0.40:
        return "phase_transition_collapse"
    if n.hub_concentration_risk >= 0.85:
        return "hub_fragility"
    if n.attractor_basin_stability <= 0.25 and n.self_organized_criticality_index >= 0.70:
        return "attractor_instability"
    if n.self_organized_criticality_index >= 0.85 and n.emergent_behavior_predictability <= 0.30:
        return "complexity_overload"
    return "none"


def _severity(c: float) -> str:
    if c >= 60:
        return "cascading"
    if c >= 40:
        return "critical_point"
    if c >= 20:
        return "fluctuating"
    return "stable_complex"


def _action(risk: str, pattern: str) -> str:
    if risk == "critical":
        if pattern in ("cascade_failure", "hub_fragility", "attractor_instability"):
            return "emergency_decoupling"
        return "network_partitioning"
    if risk == "high":
        if pattern in ("phase_transition_collapse", "complexity_overload"):
            return "redundancy_injection"
        return "hub_bypass"
    if risk == "moderate":
        return "topology_monitoring"
    return "no_action"


def _signal(n: NetworkInput, pattern: str, composite: float) -> str:
    if composite < 20:
        return "Réseau complexe stable — topologie robuste, dynamiques maîtrisées, résilience émergente forte"
    pattern_labels: Dict[str, str] = {
        "cascade_failure": "Défaillance en cascade",
        "phase_transition_collapse": "Effondrement par transition de phase",
        "hub_fragility": "Fragilité des nœuds centraux",
        "attractor_instability": "Instabilité des bassins attracteurs",
        "complexity_overload": "Surcharge de complexité émergente",
    }
    label = pattern_labels.get(pattern, pattern.replace("_", " "))
    return (
        f"{label} — vulnérabilité cascade {n.cascade_vulnerability_score:.2f} "
        f"— proximité transition {n.phase_transition_proximity:.2f} "
        f"— concentration hub {n.hub_concentration_risk:.2f} "
        f"— composite {round(composite)}"
    )


def _cascade_risk_index(n: NetworkInput, composite: float) -> float:
    val = composite / 100.0 * (n.cascade_vulnerability_score + n.perturbation_propagation_rate) / 2.0 * 10.0
    return round(min(val, 10.0), 2)


class ComplexNetworkPhysicsEngine:
    def __init__(self):
        self._results: List[NetworkResult] = []

    def assess_batch(self, inputs: List[NetworkInput]) -> List[NetworkResult]:
        self._results = []
        for n in inputs:
            topo = _topology_score(n)
            dyn = _dynamics_score(n)
            res = _resilience_score(n)
            emg = _emergence_score(n)
            comp = _composite(topo, dyn, res, emg)
            risk = _risk(comp)
            pat = _pattern(n, risk)
            sev = _severity(comp)
            act = _action(risk, pat)
            sig = _signal(n, pat, comp)
            cri = _cascade_risk_index(n, comp)
            result = NetworkResult(
                network_id=n.network_id,
                network_type=n.network_type,
                region=n.region,
                topology_score=topo,
                dynamics_score=dyn,
                resilience_score=res,
                emergence_score=emg,
                network_composite=comp,
                network_risk=risk,
                network_pattern=pat,
                network_severity=sev,
                recommended_action=act,
                network_signal=sig,
                estimated_cascade_risk_index=cri,
                cascade_vulnerability_score=n.cascade_vulnerability_score,
                phase_transition_proximity=n.phase_transition_proximity,
                hub_concentration_risk=n.hub_concentration_risk,
            )
            self._results.append(result)
        return self._results

    def summary(self) -> Dict[str, Any]:
        results = self._results
        n = len(results)
        if n == 0:
            return {
                "total": 0, "risk_counts": {}, "pattern_counts": {},
                "severity_counts": {}, "action_counts": {},
                "avg_network_composite": 0.0, "cascading_count": 0,
                "critical_intervention_count": 0,
                "avg_topology_score": 0.0, "avg_dynamics_score": 0.0,
                "avg_resilience_score": 0.0, "avg_emergence_score": 0.0,
                "avg_estimated_cascade_risk_index": 0.0,
            }

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        total_composite = 0.0
        total_topo = 0.0
        total_dyn = 0.0
        total_res = 0.0
        total_emg = 0.0
        total_cri = 0.0
        cascading_count = 0
        critical_intervention_count = 0

        for r in results:
            risk_counts[r.network_risk] = risk_counts.get(r.network_risk, 0) + 1
            pattern_counts[r.network_pattern] = pattern_counts.get(r.network_pattern, 0) + 1
            severity_counts[r.network_severity] = severity_counts.get(r.network_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.network_composite
            total_topo += r.topology_score
            total_dyn += r.dynamics_score
            total_res += r.resilience_score
            total_emg += r.emergence_score
            total_cri += r.estimated_cascade_risk_index
            if r.network_severity == "cascading":
                cascading_count += 1
            if r.network_risk in ("critical", "high"):
                critical_intervention_count += 1

        # Exactly 13 keys
        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_network_composite": round(total_composite / n, 1),
            "cascading_count": cascading_count,
            "critical_intervention_count": critical_intervention_count,
            "avg_topology_score": round(total_topo / n, 1),
            "avg_dynamics_score": round(total_dyn / n, 1),
            "avg_resilience_score": round(total_res / n, 1),
            "avg_emergence_score": round(total_emg / n, 1),
            "avg_estimated_cascade_risk_index": round(total_cri / n, 2),
        }


if __name__ == "__main__":
    engine = ComplexNetworkPhysicsEngine()
    results = engine.assess_batch(MOCK_NETWORKS)
    for r in results:
        d = r.to_dict()
        assert len(d) == 15, f"Expected 15 keys, got {len(d)} for {r.network_id}"
        print(f"{r.network_id} ({r.network_type}/{r.region}): composite={r.network_composite} risk={r.network_risk} pattern={r.network_pattern} sev={r.network_severity} action={r.recommended_action} cascade_risk={r.estimated_cascade_risk_index}")
    s = engine.summary()
    assert len(s) == 13, f"Expected 13 summary keys, got {len(s)}"
    print("\nSummary:")
    for k, v in s.items():
        print(f"  {k}: {v}")
