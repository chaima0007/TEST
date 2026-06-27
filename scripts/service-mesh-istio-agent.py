"""Service Mesh Istio Agent — CaelumSwarm™
Framework: Istio 1.21.x + Envoy Proxy
Role: mTLS automatique, traffic management, observability, security policies
"""

import json
import datetime

ISTIO_VERSION = "1.21.x"

ISTIO_COMPONENTS = {
    "istiod": "Pilot + Citadel + Galley — control plane",
    "envoy_sidecars": "Data plane — proxy injecté automatiquement",
    "ingress_gateway": "Point d'entrée externe",
    "egress_gateway": "Contrôle trafic sortant (vers APIs externes)",
}

PEER_AUTHENTICATION = {
    # mTLS strict pour tous les namespaces CaelumSwarm™
    "caelum-prod": {"mtls_mode": "STRICT"},
    "caelum-monitoring": {"mtls_mode": "STRICT"},
    "caelum-system": {"mtls_mode": "PERMISSIVE"},  # migration en cours
}

AUTHORIZATION_POLICIES = {
    # 8 politiques deny-by-default avec allowlist explicite
    "deny-all-caelum-prod": {"action": "DENY", "source": {"notNamespaces": ["caelum-prod", "caelum-system"]}},
    "allow-api-to-engines": {"action": "ALLOW", "source": {"principals": ["cluster.local/ns/caelum-prod/sa/api-gateway"]}, "destination_ports": [8080]},
    "allow-monitoring": {"action": "ALLOW", "source": {"namespaces": ["caelum-monitoring"]}, "destination_ports": [9090, 9091, 8080]},
    "allow-ingress-to-api": {"action": "ALLOW", "source": {"principals": ["cluster.local/ns/istio-system/sa/istio-ingressgateway-service-account"]}, "destination_ports": [443, 80]},
    "allow-engine-to-db": {"action": "ALLOW", "source": {"principals": ["cluster.local/ns/caelum-prod/sa/wave-engine"]}, "destination_ports": [5432]},
    "allow-report-to-storage": {"action": "ALLOW", "source": {"principals": ["cluster.local/ns/caelum-prod/sa/report-service"]}, "destination_ports": [9000]},
    "allow-egress-to-external": {"action": "ALLOW", "source": {"namespaces": ["caelum-prod"]}, "destination_ports": [443]},
    "deny-cross-namespace-default": {"action": "DENY", "source": {"notNamespaces": ["caelum-prod", "caelum-system", "caelum-monitoring", "istio-system"]}},
}

VIRTUAL_SERVICES = {
    "caelum-api-gateway": {
        "hosts": ["api-gateway"],
        "http_routes": [
            {"match": {"uri": {"prefix": "/api/wave"}}, "destination": {"host": "wave-engine", "port": 8080}, "weight": 100},
            {"match": {"uri": {"prefix": "/api/reports"}}, "destination": {"host": "report-service", "port": 8081}},
        ],
        "retries": {"attempts": 3, "perTryTimeout": "5s", "retryOn": "5xx,reset,connect-failure"},
        "timeout": "30s",
    },
    "caelum-canary": {
        "hosts": ["wave-engine"],
        "http_routes": [
            {"destination": {"host": "wave-engine", "subset": "stable"}, "weight": 90},
            {"destination": {"host": "wave-engine", "subset": "canary"}, "weight": 10},
        ],
    },
}

DESTINATION_RULES = {
    "wave-engine": {
        "trafficPolicy": {
            "connectionPool": {"tcp": {"maxConnections": 100}, "http": {"h2UpgradePolicy": "UPGRADE", "http1MaxPendingRequests": 100}},
            "outlierDetection": {"consecutive5xxErrors": 3, "interval": "30s", "baseEjectionTime": "30s"},
            "loadBalancer": {"simple": "LEAST_REQUEST"},
            "tls": {"mode": "ISTIO_MUTUAL"},
        },
        "subsets": [
            {"name": "stable", "labels": {"version": "stable"}},
            {"name": "canary", "labels": {"version": "canary"}},
        ],
    },
}

ISTIO_OBSERVABILITY = {
    "distributed_tracing": {"provider": "Jaeger", "sampling_rate": 1.0, "propagation": "b3,w3c-tracecontext"},
    "metrics": {"prometheus": True, "standard_metrics": ["istio_requests_total", "istio_request_duration_milliseconds", "istio_tcp_connections_opened_total"]},
    "access_logs": {"format": "JSON", "destination": "stdout → Loki"},
    "kiali": {"enabled": True, "url": "https://kiali.caelum.internal", "description": "Service mesh observability UI"},
}

CIRCUIT_BREAKER_CONFIG = {
    "consecutive_errors": 3,
    "interval_seconds": 30,
    "base_ejection_time_seconds": 30,
    "max_ejection_percent": 50,
    "min_health_percent": 30,
}

FAULT_INJECTION = {
    # Pour les tests de résilience
    "delay_fault": {"percentage": 5, "delay_ms": 2000, "target": "wave-engine"},
    "abort_fault": {"percentage": 2, "http_status": 503, "target": "report-service"},
}


# FONCTIONS

def design_mtls_policy(namespace: str, strict_mode: bool) -> dict:
    """Génère une PeerAuthentication policy Istio pour un namespace donné."""
    mode = "STRICT" if strict_mode else "PERMISSIVE"
    policy = {
        "apiVersion": "security.istio.io/v1beta1",
        "kind": "PeerAuthentication",
        "metadata": {
            "name": f"mtls-{namespace}",
            "namespace": namespace,
        },
        "spec": {
            "mtls": {
                "mode": mode,
            }
        },
    }
    return policy


def configure_traffic_routing(service: str, canary_weight: int) -> dict:
    """Configure un VirtualService pour canary deployment avec poids stable/canary."""
    if canary_weight < 0 or canary_weight > 100:
        raise ValueError(f"canary_weight doit être entre 0 et 100, reçu: {canary_weight}")
    stable_weight = 100 - canary_weight
    routing = {
        "apiVersion": "networking.istio.io/v1beta1",
        "kind": "VirtualService",
        "metadata": {
            "name": f"{service}-canary-routing",
            "namespace": "caelum-prod",
        },
        "spec": {
            "hosts": [service],
            "http": [
                {
                    "route": [
                        {
                            "destination": {"host": service, "subset": "stable"},
                            "weight": stable_weight,
                        },
                        {
                            "destination": {"host": service, "subset": "canary"},
                            "weight": canary_weight,
                        },
                    ]
                }
            ],
        },
    }
    return routing


def simulate_circuit_breaker(error_count: int, threshold: int) -> dict:
    """Simule le comportement du circuit breaker Istio (outlier detection)."""
    ejected = error_count >= threshold
    result = {
        "error_count": error_count,
        "threshold": threshold,
        "circuit_open": ejected,
        "status": "EJECTED" if ejected else "HEALTHY",
        "action": (
            f"Instance éjectée pendant {CIRCUIT_BREAKER_CONFIG['base_ejection_time_seconds']}s"
            if ejected
            else "Instance en service normal"
        ),
        "ejection_percent": CIRCUIT_BREAKER_CONFIG["max_ejection_percent"],
        "min_health_percent": CIRCUIT_BREAKER_CONFIG["min_health_percent"],
        "next_check_in_seconds": CIRCUIT_BREAKER_CONFIG["interval_seconds"] if ejected else 0,
    }
    return result


def generate_istio_manifest(component: str, config: dict) -> str:
    """Génère un manifest YAML Istio lisible à partir d'un dict de configuration."""
    lines = [f"# Istio Manifest — {component}", f"# Generated by CaelumSwarm™ Istio Agent", ""]

    def dict_to_yaml(d: dict, indent: int = 0) -> list:
        yaml_lines = []
        prefix = "  " * indent
        for key, value in d.items():
            if isinstance(value, dict):
                yaml_lines.append(f"{prefix}{key}:")
                yaml_lines.extend(dict_to_yaml(value, indent + 1))
            elif isinstance(value, list):
                yaml_lines.append(f"{prefix}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        first = True
                        for k, v in item.items():
                            marker = "- " if first else "  "
                            yaml_lines.append(f"{prefix}  {marker}{k}: {v}")
                            first = False
                    else:
                        yaml_lines.append(f"{prefix}  - {item}")
            else:
                yaml_lines.append(f"{prefix}{key}: {value}")
        return yaml_lines

    lines.extend(dict_to_yaml(config))
    return "\n".join(lines)


# BLOC PRINCIPAL

if __name__ == "__main__":
    sep = "=" * 70

    # 1. Istio Service Mesh Report
    print(sep)
    print("  ISTIO SERVICE MESH REPORT — CaelumSwarm™")
    print(f"  Version Istio : {ISTIO_VERSION}")
    print(f"  Date          : {datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(sep)
    print()
    print("COMPOSANTS ISTIO :")
    for component, description in ISTIO_COMPONENTS.items():
        print(f"  [{component}] {description}")
    print()

    # 2. mTLS strict configuration (tous namespaces)
    print(sep)
    print("  mTLS CONFIGURATION — PEER AUTHENTICATION")
    print(sep)
    for namespace, auth_config in PEER_AUTHENTICATION.items():
        mode = auth_config["mtls_mode"]
        status_icon = "STRICT" if mode == "STRICT" else "PERMISSIVE (migration)"
        policy = design_mtls_policy(namespace, strict_mode=(mode == "STRICT"))
        print(f"  Namespace : {namespace}")
        print(f"    Mode mTLS  : {status_icon}")
        print(f"    Policy     : {policy['metadata']['name']}")
    print()

    # 3. Authorization policies (8)
    print(sep)
    print("  AUTHORIZATION POLICIES (8 politiques)")
    print(sep)
    for i, (policy_name, policy_config) in enumerate(AUTHORIZATION_POLICIES.items(), 1):
        action = policy_config["action"]
        ports = policy_config.get("destination_ports", ["*"])
        print(f"  [{i:02d}] {policy_name}")
        print(f"        Action : {action} | Ports : {ports}")
    print()

    # 4. Virtual Services (routing + canary 90/10)
    print(sep)
    print("  VIRTUAL SERVICES — ROUTING + CANARY")
    print(sep)
    for vs_name, vs_config in VIRTUAL_SERVICES.items():
        print(f"  VirtualService : {vs_name}")
        print(f"    Hosts   : {vs_config['hosts']}")
        routes = vs_config.get("http_routes", [])
        for route in routes:
            dst = route.get("destination", {})
            weight = route.get("weight", "")
            weight_str = f" (weight: {weight}%)" if weight != "" else ""
            if "match" in route:
                prefix = route["match"].get("uri", {}).get("prefix", "")
                print(f"    Route   : {prefix} → {dst.get('host', '?')}:{dst.get('port', '?')}{weight_str}")
            else:
                print(f"    Route   : → {dst.get('host', '?')} subset={dst.get('subset', '?')}{weight_str}")
        if "retries" in vs_config:
            r = vs_config["retries"]
            print(f"    Retries : {r['attempts']} tentatives / timeout {r['perTryTimeout']} / on {r['retryOn']}")
        if "timeout" in vs_config:
            print(f"    Timeout : {vs_config['timeout']}")
    print()

    # 5. Destination Rules (circuit breaker + outlier detection)
    print(sep)
    print("  DESTINATION RULES — CIRCUIT BREAKER + OUTLIER DETECTION")
    print(sep)
    for svc_name, dr_config in DESTINATION_RULES.items():
        policy = dr_config["trafficPolicy"]
        od = policy.get("outlierDetection", {})
        lb = policy.get("loadBalancer", {})
        tls = policy.get("tls", {})
        cp = policy.get("connectionPool", {})
        subsets = dr_config.get("subsets", [])
        print(f"  Service        : {svc_name}")
        print(f"    Load Balancer    : {lb.get('simple', 'N/A')}")
        print(f"    TLS Mode         : {tls.get('mode', 'N/A')}")
        print(f"    Max Connections  : {cp.get('tcp', {}).get('maxConnections', 'N/A')}")
        print(f"    Outlier Detection: {od.get('consecutive5xxErrors', 'N/A')} erreurs → éjection ({od.get('interval', 'N/A')} interval)")
        print(f"    Subsets          : {[s['name'] for s in subsets]}")
    print()

    # 6. Traffic management simulation (canary wave-engine)
    print(sep)
    print("  TRAFFIC MANAGEMENT SIMULATION — CANARY wave-engine (90/10)")
    print(sep)
    canary_vs = configure_traffic_routing("wave-engine", canary_weight=10)
    routes = canary_vs["spec"]["http"][0]["route"]
    total_requests = 1000
    print(f"  Simulation sur {total_requests} requêtes :")
    for route in routes:
        subset = route["destination"]["subset"]
        weight = route["weight"]
        requests = int(total_requests * weight / 100)
        print(f"    [{subset:10s}] {weight:3d}% → {requests:4d} requêtes")
    print(f"  Manifest VirtualService généré : {canary_vs['metadata']['name']}")
    print()

    # 7. Circuit breaker simulation (3 erreurs → éjection)
    print(sep)
    print("  CIRCUIT BREAKER SIMULATION — OUTLIER DETECTION")
    print(sep)
    threshold = CIRCUIT_BREAKER_CONFIG["consecutive_errors"]
    test_cases = [
        (0, "Aucune erreur"),
        (2, "Sous le seuil"),
        (3, "Seuil atteint"),
        (5, "Dépassement"),
    ]
    for error_count, label in test_cases:
        result = simulate_circuit_breaker(error_count, threshold)
        status = result["status"]
        action = result["action"]
        print(f"  Erreurs={error_count:2d} ({label:20s}) → {status:10s} | {action}")
    print()

    # 8. Fault injection (tests résilience)
    print(sep)
    print("  FAULT INJECTION — TESTS DE RESILIENCE")
    print(sep)
    delay = FAULT_INJECTION["delay_fault"]
    abort = FAULT_INJECTION["abort_fault"]
    print(f"  Delay Fault :")
    print(f"    Target     : {delay['target']}")
    print(f"    Pourcentage: {delay['percentage']}% des requêtes")
    print(f"    Délai      : {delay['delay_ms']}ms injecté")
    print(f"  Abort Fault :")
    print(f"    Target     : {abort['target']}")
    print(f"    Pourcentage: {abort['percentage']}% des requêtes")
    print(f"    HTTP Status: {abort['http_status']} retourné")
    print()

    # 9. Observability (Jaeger + Kiali + Prometheus)
    print(sep)
    print("  OBSERVABILITY — JAEGER + KIALI + PROMETHEUS")
    print(sep)
    tracing = ISTIO_OBSERVABILITY["distributed_tracing"]
    metrics = ISTIO_OBSERVABILITY["metrics"]
    logs = ISTIO_OBSERVABILITY["access_logs"]
    kiali = ISTIO_OBSERVABILITY["kiali"]
    print(f"  Distributed Tracing :")
    print(f"    Provider    : {tracing['provider']}")
    print(f"    Sampling    : {tracing['sampling_rate'] * 100:.0f}% des traces")
    print(f"    Propagation : {tracing['propagation']}")
    print(f"  Metrics (Prometheus) : {'actif' if metrics['prometheus'] else 'inactif'}")
    for metric in metrics["standard_metrics"]:
        print(f"    - {metric}")
    print(f"  Access Logs :")
    print(f"    Format      : {logs['format']}")
    print(f"    Destination : {logs['destination']}")
    print(f"  Kiali :")
    print(f"    Enabled     : {kiali['enabled']}")
    print(f"    URL         : {kiali['url']}")
    print(f"    Description : {kiali['description']}")
    print()

    # 10. Manifest exemple généré
    print(sep)
    print("  EXEMPLE MANIFEST ISTIO GENERE")
    print(sep)
    sample_manifest = generate_istio_manifest(
        "PeerAuthentication/caelum-prod",
        {
            "apiVersion": "security.istio.io/v1beta1",
            "kind": "PeerAuthentication",
            "metadata": {"name": "mtls-caelum-prod", "namespace": "caelum-prod"},
            "spec": {"mtls": {"mode": "STRICT"}},
        },
    )
    print(sample_manifest)
    print()

    print(sep)
    print("  Service Mesh Istio Agent — PRET (Istio 1.21 / mTLS / Circuit Breaker / Kiali)")
    print(sep)
