"""
Agent Prometheus Monitoring — stack d'observabilité complète pour CaelumSwarm™
(droits humains / conformité CSDDD 2024).

Références :
  - Prometheus 2.51 (https://prometheus.io/docs/prometheus/2.51/)
  - PromQL — Prometheus Query Language (https://prometheus.io/docs/prometheus/latest/querying/basics/)
  - Alertmanager 0.27 (https://prometheus.io/docs/alerting/latest/alertmanager/)
  - Grafana 10.4 (https://grafana.com/docs/grafana/v10.4/)
  - Prometheus Pushgateway (https://prometheus.io/docs/instrumenting/pushing/)
  - remote_write / Thanos Receive (https://thanos.io/tip/components/receive.md/)
  - SLO/SLI monitoring — Google SRE Workbook Chapter 5
  - Golden Signals SRE : Latency · Traffic · Errors · Saturation
"""

import datetime
import hashlib
import math
import random
import secrets

# ---------------------------------------------------------------------------
# 1. CONSTANTES
# ---------------------------------------------------------------------------

PROMETHEUS_CONFIG = {
    "version": "2.51.0",
    "global": {
        "scrape_interval": "15s",
        "evaluation_interval": "15s",
        "scrape_timeout": "10s",
        "external_labels": {"cluster": "caelum-eu-west", "env": "production"},
    },
    "storage": {
        "retention_time": "30d",
        "retention_size": "50GB",
        "tsdb_path": "/prometheus/data",
    },
    "remote_write": {
        "url": "http://thanos-receive:19291/api/v1/receive",  # long-term storage
        "queue_config": {"max_samples_per_send": 10000, "max_shards": 200},
    },
}

SCRAPE_CONFIGS = {
    "wave_engines": {
        "job_name": "caelum_wave_engines",
        "scrape_interval": "10s",
        "metrics_path": "/metrics",
        "target_discovery": "consul",  # Consul service discovery
        "consul_service": "wave-engine",
        "relabel_configs": [
            {"source_labels": ["__meta_consul_service"], "target_label": "service"},
            {"source_labels": ["__meta_consul_dc"], "target_label": "datacenter"},
        ],
    },
    "api_gateway": {
        "job_name": "caelum_api_gateway",
        "scrape_interval": "15s",
        "metrics_path": "/metrics",
        "port": 8080,
    },
    "postgresql": {
        "job_name": "postgres_exporter",
        "port": 9187,
        "metrics_path": "/metrics",
        "scrape_interval": "30s",
    },
    "redis": {
        "job_name": "redis_exporter",
        "port": 9121,
        "metrics_path": "/metrics",
        "scrape_interval": "15s",
    },
    "rabbitmq": {
        "job_name": "rabbitmq_exporter",
        "port": 15692,
        "metrics_path": "/metrics",
        "scrape_interval": "15s",
    },
    "node_exporter": {
        "job_name": "node_exporter",
        "port": 9100,
        "scrape_interval": "30s",
        "metrics_path": "/metrics",
    },
    "cadvisor": {
        "job_name": "cadvisor",
        "port": 8080,
        "metrics_path": "/metrics",
        "scrape_interval": "15s",
        "container_label_safe_list": ["container_label_com_docker_swarm_service_name"],
    },
    "blackbox": {
        "job_name": "blackbox_exporter",
        "module": "http_2xx",
        "port": 9115,
        "metrics_path": "/probe",
        "targets": [
            "https://api.caelumpartners.be/health",
            "https://dashboard.caelumpartners.be",
        ],
    },
    "pushgateway": {
        "job_name": "pushgateway",
        "port": 9091,
        "metrics_path": "/metrics",
        "honor_labels": True,
        "scrape_interval": "30s",
        "note": "Réceptionne métriques batch engines Wave (push vs pull)",
    },
    "alertmanager": {
        "job_name": "alertmanager",
        "port": 9093,
        "metrics_path": "/metrics",
        "scrape_interval": "30s",
    },
    "thanos_sidecar": {
        "job_name": "thanos_sidecar",
        "port": 10902,
        "metrics_path": "/metrics",
        "scrape_interval": "30s",
        "note": "Sidecar Thanos embarqué dans le pod Prometheus",
    },
    "grafana": {
        "job_name": "grafana",
        "port": 3000,
        "metrics_path": "/metrics",
        "scrape_interval": "60s",
        "bearer_token_file": "/var/run/secrets/grafana-token",
    },
}

METRICS_CATALOG = {
    # Golden Signals SRE
    "latency": {
        "metric": "http_request_duration_seconds",
        "labels": ["service", "method", "endpoint", "status_code"],
        "histogram_buckets": [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
        "slo": "p99 < 500ms",
        "type": "histogram",
    },
    "traffic": {
        "metric": "http_requests_total",
        "labels": ["service", "method", "endpoint"],
        "type": "counter",
        "slo": "nominal selon capacite planifiee",
    },
    "errors": {
        "metric": "http_requests_errors_total",
        "labels": ["service", "error_type"],
        "slo": "error_rate < 0.1%",
        "type": "counter",
    },
    "saturation": {
        "metric": "process_resident_memory_bytes",
        "type": "gauge",
        "slo": "memory_usage < 80%",
        "labels": ["service", "pod"],
    },
    # Business metrics CaelumSwarm™
    "wave_engine_score": {
        "metric": "caelum_wave_engine_score",
        "labels": ["engine", "domain", "entity"],
        "type": "gauge",
        "slo": "score disponible dans < 5s apres analyse",
    },
    "compliance_alerts_total": {
        "metric": "caelum_compliance_alerts_total",
        "labels": ["severity", "domain"],
        "type": "counter",
        "slo": "alerte livree en < 60s",
    },
    "report_generation_duration": {
        "metric": "caelum_report_generation_seconds",
        "type": "histogram",
        "labels": ["report_type", "domain"],
        "slo": "p95 < 30s",
    },
    "active_agents": {
        "metric": "caelum_active_agents_total",
        "labels": ["agent_type", "status"],
        "type": "gauge",
        "slo": "nb_agents_actifs >= 1 en permanence",
    },
    "csddd_violations_detected": {
        "metric": "caelum_csddd_violations_total",
        "labels": ["domain", "article", "severity"],
        "type": "counter",
        "slo": "taux_detection > 95%",
    },
    "wave_engine_duration": {
        "metric": "caelum_wave_engine_duration_seconds",
        "type": "histogram",
        "labels": ["engine", "domain"],
        "slo": "p99 < 3s",
    },
}

ALERTING_RULES = {
    "SRE_Critical": [
        {
            "alert": "HighErrorRate",
            "expr": "rate(http_requests_errors_total[5m]) / rate(http_requests_total[5m]) > 0.05",
            "for": "2m",
            "severity": "critical",
            "annotation": "Error rate exceeds 5% for 2 minutes",
        },
        {
            "alert": "HighLatencyP99",
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1.0",
            "for": "5m",
            "severity": "critical",
            "annotation": "p99 latency exceeds 1s for 5 minutes",
        },
        {
            "alert": "ServiceDown",
            "expr": "up == 0",
            "for": "1m",
            "severity": "critical",
            "annotation": "Target is down — check service health",
        },
        {
            "alert": "HighMemoryUsage",
            "expr": "process_resident_memory_bytes / node_memory_MemTotal_bytes > 0.80",
            "for": "5m",
            "severity": "critical",
            "annotation": "Memory usage exceeds 80% for 5 minutes",
        },
        {
            "alert": "SLOBurnRateFast",
            "expr": (
                "sum(rate(http_requests_errors_total[5m])) / sum(rate(http_requests_total[5m]))"
                " > 14.4 * 0.001"
            ),
            "for": "2m",
            "severity": "critical",
            "annotation": "SLO error budget burning at x14.4 rate — exhaustion in 1h",
        },
    ],
    "Business_Alerts": [
        {
            "alert": "ComplianceAlertSpike",
            "expr": "rate(caelum_compliance_alerts_total{severity='critical'}[1h]) > 10",
            "for": "5m",
            "severity": "warning",
            "annotation": "Critical compliance alerts spiking — check CSDDD violations",
        },
        {
            "alert": "WaveEngineScoreDrop",
            "expr": "avg(caelum_wave_engine_score) < 30",
            "for": "10m",
            "severity": "warning",
            "annotation": "Average wave engine score below acceptable threshold",
        },
        {
            "alert": "ReportGenerationSlow",
            "expr": "histogram_quantile(0.95, rate(caelum_report_generation_seconds_bucket[5m])) > 30",
            "for": "5m",
            "severity": "warning",
            "annotation": "Report generation p95 exceeds 30s SLO",
        },
        {
            "alert": "ActiveAgentsCriticallyLow",
            "expr": "sum(caelum_active_agents_total{status='running'}) < 2",
            "for": "3m",
            "severity": "critical",
            "annotation": "Fewer than 2 agents running — platform degraded",
        },
        {
            "alert": "CSDDDViolationSurge",
            "expr": "rate(caelum_csddd_violations_total{severity='critical'}[30m]) > 5",
            "for": "5m",
            "severity": "warning",
            "annotation": "CSDDD critical violations surging — legal team alert",
        },
        {
            "alert": "WaveEngineDurationSLOBreach",
            "expr": "histogram_quantile(0.99, rate(caelum_wave_engine_duration_seconds_bucket[5m])) > 3",
            "for": "5m",
            "severity": "warning",
            "annotation": "Wave engine p99 duration exceeds 3s SLO",
        },
    ],
    "Infrastructure": [
        {
            "alert": "DiskSpaceLow",
            "expr": "disk_usage_percent > 85",
            "for": "5m",
            "severity": "warning",
            "annotation": "Disk usage above 85% — schedule cleanup",
        },
        {
            "alert": "MemoryPressure",
            "expr": "memory_usage_percent > 90",
            "for": "10m",
            "severity": "critical",
            "annotation": "Memory usage above 90% — OOM risk",
        },
        {
            "alert": "PrometheusTSDBCompactionFailed",
            "expr": "increase(prometheus_tsdb_compactions_failed_total[1h]) > 0",
            "for": "0m",
            "severity": "critical",
            "annotation": "Prometheus TSDB compaction failed — data integrity at risk",
        },
        {
            "alert": "ThanosReceiveLatencyHigh",
            "expr": (
                "histogram_quantile(0.99, rate(thanos_receive_forward_duration_seconds_bucket[5m]))"
                " > 5"
            ),
            "for": "5m",
            "severity": "warning",
            "annotation": "Thanos Receive forward latency p99 exceeds 5s",
        },
    ],
}

ALERTMANAGER_CONFIG = {
    "version": "0.27.0",
    "routes": {
        "receiver": "default",
        "group_by": ["alertname", "service"],
        "group_wait": "30s",
        "group_interval": "5m",
        "repeat_interval": "4h",
        "routes": [
            {"match": {"severity": "critical"}, "receiver": "pagerduty", "continue": True},
            {"match": {"severity": "critical"}, "receiver": "slack_critical"},
            {"match": {"severity": "warning"}, "receiver": "slack_warnings"},
            {"match": {"team": "compliance"}, "receiver": "compliance_team_email"},
        ],
    },
    "receivers": {
        "pagerduty": {"integration_key": "VAULT_MANAGED"},
        "slack_critical": {"webhook_url": "VAULT_MANAGED", "channel": "#caelum-critical"},
        "slack_warnings": {"webhook_url": "VAULT_MANAGED", "channel": "#caelum-alerts"},
        "compliance_team_email": {"to": "compliance@caelumpartners.be"},
        "default": {"webhook_url": "VAULT_MANAGED", "channel": "#caelum-monitoring"},
    },
    "inhibit_rules": [
        {
            "source_match": {"severity": "critical"},
            "target_match": {"severity": "warning"},
            "equal": ["service"],
        },
    ],
}

SLO_DEFINITIONS = {
    "api_availability": {
        "target": 0.999,
        "window": "30d",
        "error_budget_minutes": 43.8,
        "metric": "up",
        "description": "API Gateway disponible 99.9% du temps sur fenetre 30j",
    },
    "api_latency_p99": {
        "target_ms": 500,
        "compliance_percent": 0.99,
        "window": "30d",
        "metric": "http_request_duration_seconds",
        "description": "p99 latence API < 500ms sur 99% des periodes de 5min",
    },
    "wave_engine_uptime": {
        "target": 0.9995,
        "window": "30d",
        "error_budget_minutes": 21.6,
        "metric": "caelum_active_agents_total",
        "description": "Wave engines disponibles 99.95% du temps",
    },
    "report_generation": {
        "target_seconds": 30,
        "percentile": 0.95,
        "window": "30d",
        "metric": "caelum_report_generation_seconds",
        "description": "p95 generation rapport < 30s",
    },
    "alert_delivery": {
        "target_seconds": 60,
        "compliance_percent": 0.999,
        "window": "30d",
        "metric": "caelum_compliance_alerts_total",
        "description": "Alertes livrees en < 60s dans 99.9% des cas",
    },
}

GRAFANA_DASHBOARDS = {
    "caelum_overview": {
        "panels": 12,
        "refresh": "30s",
        "tags": ["overview", "swarm"],
        "description": "Vue globale CaelumSwarm — Golden Signals SRE + business KPIs",
        "datasource": "Prometheus",
    },
    "wave_engines_detail": {
        "panels": 20,
        "refresh": "15s",
        "tags": ["engines", "compliance"],
        "description": "Detail par engine Wave : scores, durees, distribution entites",
        "datasource": "Prometheus",
    },
    "infrastructure": {
        "panels": 15,
        "refresh": "1m",
        "tags": ["infra", "docker"],
        "description": "Metriques infra : CPU, memoire, disque, reseau (cAdvisor + Node Exporter)",
        "datasource": "Prometheus",
    },
    "slo_tracking": {
        "panels": 8,
        "refresh": "5m",
        "tags": ["slo", "sre"],
        "description": "Suivi SLO/SLI : burn rate, error budget, compliance par fenetre",
        "datasource": "Prometheus",
    },
    "business_metrics": {
        "panels": 10,
        "refresh": "5m",
        "tags": ["business", "compliance"],
        "description": "Metriques metier CSDDD : violations, rapports, alertes conformite",
        "datasource": "Prometheus",
    },
}

THANOS_CONFIG = {
    "components": ["query", "store", "compact", "receive"],
    "retention": {
        "raw": "30d",
        "5m_downsampled": "1y",
        "1h_downsampled": "5y",
    },
    "object_storage": "s3://caelum-metrics-eu",
    "query_frontend": True,  # query caching + sharding
    "query_frontend_config": {
        "cache_backend": "redis",
        "cache_host": "redis.caelum.svc.cluster.local:6379",
        "split_interval": "24h",
        "max_retries": 3,
    },
    "store_gateway": {
        "chunk_pool_size": "4GB",
        "index_cache": "250MB",
    },
    "compactor": {
        "consistency_delay": "30m",
        "retention_resolution_raw": "30d",
        "retention_resolution_5m": "365d",
        "retention_resolution_1h": "1825d",
    },
}

MONITORING_SECURITY = {
    "prometheus": {
        "tls": {
            "cert_file": "/etc/prometheus/tls/tls.crt",
            "key_file": "/etc/prometheus/tls/tls.key",
            "client_ca_file": "/etc/prometheus/tls/ca.crt",
            "client_auth_type": "RequireAndVerifyClientCert",
        },
        "basic_auth": False,
        "bearer_token": "VAULT_MANAGED",
        "web_config": "/etc/prometheus/web-config.yml",
    },
    "alertmanager": {
        "tls": {
            "cert_file": "/etc/alertmanager/tls/tls.crt",
            "key_file": "/etc/alertmanager/tls/tls.key",
        },
        "cluster_tls": True,
        "gossip_encryption": "AES-256-GCM",
    },
    "grafana": {
        "auth": {
            "oauth_provider": "generic_oauth",
            "oauth_client_id": "VAULT_MANAGED",
            "allow_sign_up": False,
            "auto_login": False,
        },
        "rbac": {
            "admin_role": "GrafanaAdmin",
            "editor_role": "CaelumEngineers",
            "viewer_role": "CaelumAnalysts",
            "compliance_role": "ComplianceTeam",
        },
        "data_source_permissions": {
            "caelum_prometheus": ["GrafanaAdmin", "CaelumEngineers"],
            "caelum_thanos": ["GrafanaAdmin", "CaelumEngineers", "ComplianceTeam"],
        },
        "tls": {
            "cert_file": "/etc/grafana/tls/tls.crt",
            "key_file": "/etc/grafana/tls/tls.key",
            "protocol": "https",
        },
        "cookie_secure": True,
        "secret_key": "VAULT_MANAGED",
    },
    "network_policies": {
        "prometheus_ingress": ["api-gateway", "grafana", "thanos-sidecar"],
        "alertmanager_ingress": ["prometheus"],
        "grafana_ingress": ["nginx-ingress"],
        "thanos_ingress": ["prometheus-sidecar", "grafana"],
    },
}

# ---------------------------------------------------------------------------
# 2. FONCTIONS
# ---------------------------------------------------------------------------


def generate_promql_query(metric_name: str, aggregation: str, window: str) -> dict:
    """Genere une requete PromQL optimisee pour un metrique CaelumSwarm(tm).

    Produit la requete string, un exemple de resultat simule et une explication
    pedagogique du fonctionnement de la requete.

    Args:
        metric_name:  Nom du metrique Prometheus (ex. "http_request_duration_seconds").
        aggregation:  Type d'agregation PromQL (rate, histogram_quantile, sum, avg, ...).
        window:       Fenetre temporelle (ex. "5m", "1h", "30d").

    Returns:
        dict avec query_string, example_result et explanation.
    """
    query_string = ""
    explanation = ""
    example_result: float = 0.0

    if aggregation == "rate":
        query_string = f"rate({metric_name}[{window}])"
        explanation = (
            f"Calcule le taux d'augmentation par seconde du compteur '{metric_name}'"
            f" sur une fenetre glissante de {window}. Utilise la regression lineaire"
            f" (least-squares) sur les echantillons — tolere les gaps de scrape."
        )
        example_result = round(random.uniform(0.5, 15.0), 4)

    elif aggregation == "histogram_quantile_p99":
        query_string = (
            f"histogram_quantile(0.99, sum(rate({metric_name}_bucket[{window}]))"
            f" by (le, service))"
        )
        explanation = (
            f"Calcule le 99e percentile de la distribution du histogramme '{metric_name}'"
            f" sur {window}. Le regroupement 'by (le, service)' preserve les buckets par"
            f" service pour une granularite optimale. Recommande sur fenetres >= 5m."
        )
        example_result = round(random.uniform(0.15, 0.85), 4)

    elif aggregation == "error_rate":
        errors_metric = metric_name.replace("_total", "_errors_total")
        query_string = (
            f"sum(rate({errors_metric}[{window}]))"
            f" / sum(rate({metric_name}[{window}]))"
        )
        explanation = (
            f"Calcule le taux d'erreur en divisant le debit d'erreurs par le debit"
            f" total de requetes sur {window}. Retourne une valeur entre 0 et 1"
            f" (multiplier par 100 pour obtenir un pourcentage). Alerte si > 0.001 (0.1%)."
        )
        example_result = round(random.uniform(0.0001, 0.005), 6)

    elif aggregation == "sum_by_service":
        query_string = f"sum by (service) (rate({metric_name}[{window}]))"
        explanation = (
            f"Somme le taux de '{metric_name}' par label 'service' sur {window}."
            f" Utile pour identifier les services les plus actifs ou ceux qui"
            f" consomment le plus de ressources."
        )
        example_result = round(random.uniform(100.0, 5000.0), 2)

    elif aggregation == "avg":
        query_string = f"avg(rate({metric_name}[{window}]))"
        explanation = (
            f"Calcule la moyenne du taux de '{metric_name}' sur l'ensemble des"
            f" instances scrapees, sur une fenetre de {window}. Utile pour les"
            f" metriques de saturation (CPU, memoire, queue depth)."
        )
        example_result = round(random.uniform(0.3, 0.75), 4)

    elif aggregation == "increase":
        query_string = f"increase({metric_name}[{window}])"
        explanation = (
            f"Calcule l'accroissement brut du compteur '{metric_name}' sur {window}."
            f" Contrairement a rate(), retourne un nombre total d'occurrences (non"
            f" normalise par secondes). Utile pour des fenetres larges (1h, 24h)."
        )
        example_result = round(random.uniform(50.0, 10000.0), 0)

    else:
        query_string = f"{aggregation}({metric_name}[{window}])"
        explanation = (
            f"Requete PromQL generique : agregation '{aggregation}' sur '{metric_name}'"
            f" avec fenetre {window}."
        )
        example_result = round(random.uniform(0.0, 100.0), 4)

    catalog_entry = METRICS_CATALOG.get(
        next((k for k, v in METRICS_CATALOG.items() if v.get("metric") == metric_name), ""),
        {},
    )

    return {
        "query_string": query_string,
        "metric": metric_name,
        "aggregation": aggregation,
        "window": window,
        "example_result": example_result,
        "explanation": explanation,
        "labels": catalog_entry.get("labels", []),
        "metric_type": catalog_entry.get("type", "unknown"),
        "slo_reference": catalog_entry.get("slo", "n/a"),
    }


def calculate_error_budget(slo_name: str, current_uptime: float) -> dict:
    """Calcule le budget d'erreur restant pour un SLO donne.

    Implemente le modele Google SRE : budget = (1 - target) * window.
    Calcule le burn rate actuel et projette la date d'epuisement si le rythme
    de consommation se maintient.

    Args:
        slo_name:        Cle dans SLO_DEFINITIONS (ex. "api_availability").
        current_uptime:  Taux de disponibilite actuel mesure (ex. 0.9985 = 99.85%).

    Returns:
        dict avec budget_remaining_minutes, burn_rate, projected_exhaustion_date,
        status et recommendations.
    """
    slo = SLO_DEFINITIONS.get(slo_name)
    if not slo:
        return {"error": f"SLO inconnu : {slo_name}"}

    now = datetime.datetime.now(datetime.timezone.utc)
    window_days = 30
    window_minutes = window_days * 24 * 60

    # Extraction de la cible selon le type de SLO
    if "target" in slo:
        target = slo["target"]
    elif "compliance_percent" in slo:
        target = slo["compliance_percent"]
    else:
        target = 0.999

    # Budget total en minutes (pour une fenetre 30j)
    total_error_budget_minutes = round((1.0 - target) * window_minutes, 2)

    # Budget consomme = (target - current_uptime) * window_minutes
    consumed_minutes = max(0.0, round((target - current_uptime) * window_minutes, 2))

    # Budget restant
    budget_remaining_minutes = round(
        max(0.0, total_error_budget_minutes - consumed_minutes), 2
    )
    budget_remaining_pct = round(
        (budget_remaining_minutes / total_error_budget_minutes) * 100, 1
    ) if total_error_budget_minutes > 0 else 0.0

    # Burn rate : rapport entre la consommation actuelle et le rythme nominal
    # Rythme nominal = consommer 100% du budget en 30j (burn rate = 1.0)
    elapsed_days = random.uniform(10, 20)  # simulation : 10-20j ecoules sur 30j
    elapsed_fraction = elapsed_days / window_days
    nominal_consumption = total_error_budget_minutes * elapsed_fraction
    burn_rate = round(
        consumed_minutes / nominal_consumption, 2
    ) if nominal_consumption > 0 else 0.0

    # Projection date epuisement
    if burn_rate > 1.0 and budget_remaining_minutes > 0:
        minutes_to_exhaustion = budget_remaining_minutes / (burn_rate - 1.0 + 0.001)
        exhaustion_date = (now + datetime.timedelta(minutes=minutes_to_exhaustion)).strftime(
            "%Y-%m-%d %H:%M UTC"
        )
    else:
        exhaustion_date = "Pas d'epuisement prevu (burn rate <= 1.0)"

    # Statut
    if budget_remaining_pct >= 50:
        status = "SAIN"
        color = "green"
    elif budget_remaining_pct >= 20:
        status = "ATTENTION"
        color = "orange"
    else:
        status = "CRITIQUE"
        color = "red"

    # Recommandations
    recommendations = []
    if burn_rate > 14.4:
        recommendations.append(
            "URGENT : burn rate x{:.1f} — epuisement budget < 1h. Escalade immediate.".format(burn_rate)
        )
    elif burn_rate > 6.0:
        recommendations.append(
            "WARNING : burn rate x{:.1f} — epuisement < 6h. Notifier equipe on-call.".format(burn_rate)
        )
    elif burn_rate > 3.0:
        recommendations.append(
            "INFO : burn rate x{:.1f} — epuisement < 72h. Ouvrir ticket prioritaire.".format(burn_rate)
        )
    if budget_remaining_pct < 20:
        recommendations.append(
            "Geler les deploiements non critiques jusqu'a retablissement du SLO."
        )
    if not recommendations:
        recommendations.append(
            "Budget SLO confortable — continuer surveillance nominale (refresh 5m)."
        )

    return {
        "slo_name": slo_name,
        "target_uptime": target,
        "current_uptime": current_uptime,
        "window_days": window_days,
        "total_error_budget_minutes": total_error_budget_minutes,
        "consumed_minutes": consumed_minutes,
        "budget_remaining_minutes": budget_remaining_minutes,
        "budget_remaining_pct": budget_remaining_pct,
        "burn_rate": burn_rate,
        "elapsed_days_simulated": round(elapsed_days, 1),
        "projected_exhaustion_date": exhaustion_date,
        "status": status,
        "status_color": color,
        "recommendations": recommendations,
    }


def simulate_alert_firing(alert_name: str, duration_minutes: int) -> dict:
    """Simule le declenchement et le routage d'une alerte Alertmanager.

    Reconstitue le cycle de vie complet d'une alerte : PENDING -> FIRING ->
    routage Alertmanager -> notifications envoyees -> inhibitions eventuelles.

    Args:
        alert_name:       Nom de l'alerte (doit figurer dans ALERTING_RULES).
        duration_minutes: Duree simulee du declenchement en minutes.

    Returns:
        dict avec alert_timeline, notifications_sent, escalation_path et
        inhibitions appliquees.
    """
    now = datetime.datetime.now(datetime.timezone.utc)

    # Recherche de la definition de l'alerte
    alert_def = None
    alert_group = None
    for group, rules in ALERTING_RULES.items():
        for rule in rules:
            if rule["alert"] == alert_name:
                alert_def = rule
                alert_group = group
                break
        if alert_def:
            break

    if not alert_def:
        return {"error": f"Alerte inconnue : {alert_name}"}

    severity = alert_def.get("severity", "warning")
    for_duration = alert_def.get("for", "0m")

    # Parse "for" duration en minutes
    for_minutes = 0
    if for_duration.endswith("m"):
        for_minutes = int(for_duration[:-1])
    elif for_duration.endswith("s"):
        for_minutes = max(1, int(for_duration[:-1]) // 60)

    # Timeline de l'alerte
    t_eval = now
    t_pending = now + datetime.timedelta(seconds=15)  # premier scrape en anomalie
    t_firing = t_pending + datetime.timedelta(minutes=for_minutes)
    t_groupwait_end = t_firing + datetime.timedelta(seconds=30)  # group_wait AM
    t_notified = t_groupwait_end + datetime.timedelta(seconds=5)   # envoi notification
    t_resolved = t_firing + datetime.timedelta(minutes=duration_minutes)

    fmt = "%H:%M:%S UTC"

    alert_timeline = [
        {
            "time": t_eval.strftime(fmt),
            "state": "NORMAL",
            "event": "Prometheus evalue la regle — condition non remplie",
        },
        {
            "time": t_pending.strftime(fmt),
            "state": "PENDING",
            "event": f"Condition remplie — attente confirmation ({for_duration})",
        },
        {
            "time": t_firing.strftime(fmt),
            "state": "FIRING",
            "event": "Alerte FIRING — envoyee a Alertmanager",
        },
        {
            "time": t_groupwait_end.strftime(fmt),
            "state": "FIRING",
            "event": f"Alertmanager group_wait expire — routage alerte {alert_name}",
        },
        {
            "time": t_notified.strftime(fmt),
            "state": "FIRING",
            "event": "Notifications dispatched a tous les receivers configures",
        },
        {
            "time": t_resolved.strftime(fmt),
            "state": "RESOLVED",
            "event": f"Alerte resolue apres {duration_minutes} min — notification RESOLVED",
        },
    ]

    # Determination des receivers selon la severite
    notifications_sent = []
    escalation_path = []

    route_config = ALERTMANAGER_CONFIG["routes"]["routes"]
    for route in route_config:
        match = route.get("match", {})
        if match.get("severity") == severity:
            receiver_name = route["receiver"]
            receiver_cfg = ALERTMANAGER_CONFIG["receivers"].get(receiver_name, {})
            channel = receiver_cfg.get("channel") or receiver_cfg.get("to", "inconnu")
            notifications_sent.append(
                {
                    "receiver": receiver_name,
                    "channel": channel,
                    "sent_at": t_notified.strftime(fmt),
                    "delivery_status": "OK" if random.random() > 0.05 else "RETRY",
                }
            )
            escalation_path.append(receiver_name)
            if not route.get("continue", False):
                break

    # Inhibitions appliquees
    inhibitions_applied = []
    if severity == "critical":
        inhibitions_applied.append(
            {
                "rule": "critical suppresses warning for same service",
                "suppressed_severity": "warning",
                "reason": "Alerte critique active — warnings redondants inhibes",
            }
        )

    # Fingerprint d'alerte (identificateur unique Alertmanager)
    fingerprint = hashlib.md5(
        f"{alert_name}{t_firing.isoformat()}".encode()
    ).hexdigest()[:10]

    return {
        "alert_name": alert_name,
        "alert_group": alert_group,
        "severity": severity,
        "fingerprint": fingerprint,
        "expr": alert_def.get("expr", ""),
        "annotation": alert_def.get("annotation", ""),
        "for_duration": for_duration,
        "simulated_duration_minutes": duration_minutes,
        "alert_timeline": alert_timeline,
        "notifications_sent": notifications_sent,
        "escalation_path": escalation_path,
        "inhibitions_applied": inhibitions_applied,
        "alertmanager_version": ALERTMANAGER_CONFIG["version"],
        "group_by": ALERTMANAGER_CONFIG["routes"]["group_by"],
    }


def design_grafana_dashboard(service_name: str) -> dict:
    """Conçoit un dashboard Grafana pour un service CaelumSwarm(tm).

    Produit une configuration declarative compatible Grafana 10.4 couvrant
    les quatre Golden Signals SRE (Latence, Traffic, Errors, Saturation)
    plus les metriques metier CaelumSwarm(tm) specifiques au service.

    Args:
        service_name: Nom court du service (ex. "wave_engines", "api_gateway").

    Returns:
        dict panels_config avec panels Golden Signals + business metrics,
        alerting rules, variables Grafana et datasource config.
    """
    dashboard_meta = GRAFANA_DASHBOARDS.get(service_name, {})
    uid = f"caelum-{service_name.replace('_', '-')}-{secrets.token_hex(4)}"

    # Variables Grafana (template variables)
    template_variables = [
        {
            "name": "cluster",
            "type": "query",
            "query": "label_values(up, cluster)",
            "current": "caelum-eu-west",
        },
        {
            "name": "service",
            "type": "query",
            "query": f"label_values(up{{job=~\"caelum.*\"}}, service)",
            "multi": True,
            "include_all": True,
        },
        {
            "name": "interval",
            "type": "interval",
            "options": ["1m", "5m", "15m", "1h"],
            "current": "5m",
        },
    ]

    # Panels Golden Signals SRE
    panels_golden = [
        {
            "id": 1,
            "title": f"[LATENCE] p50 / p95 / p99 — {service_name}",
            "type": "timeseries",
            "description": "Golden Signal #1 — Latency : percentiles de la duree de requete",
            "queries": [
                {
                    "refId": "A",
                    "expr": (
                        "histogram_quantile(0.50, sum(rate("
                        "http_request_duration_seconds_bucket"
                        "{service=~\"$service\"}[$interval])) by (le))"
                    ),
                    "legendFormat": "p50",
                },
                {
                    "refId": "B",
                    "expr": (
                        "histogram_quantile(0.95, sum(rate("
                        "http_request_duration_seconds_bucket"
                        "{service=~\"$service\"}[$interval])) by (le))"
                    ),
                    "legendFormat": "p95",
                },
                {
                    "refId": "C",
                    "expr": (
                        "histogram_quantile(0.99, sum(rate("
                        "http_request_duration_seconds_bucket"
                        "{service=~\"$service\"}[$interval])) by (le))"
                    ),
                    "legendFormat": "p99",
                },
            ],
            "unit": "s",
            "thresholds": [
                {"value": 0.5, "color": "orange"},
                {"value": 1.0, "color": "red"},
            ],
            "alert": {
                "name": "HighLatencyP99",
                "condition": "p99 > 1.0s",
                "for": "5m",
                "severity": "critical",
            },
        },
        {
            "id": 2,
            "title": f"[TRAFFIC] Debit requetes/sec — {service_name}",
            "type": "timeseries",
            "description": "Golden Signal #2 — Traffic : volume de requetes par seconde",
            "queries": [
                {
                    "refId": "A",
                    "expr": (
                        "sum(rate(http_requests_total"
                        "{service=~\"$service\"}[$interval])) by (service)"
                    ),
                    "legendFormat": "{{service}}",
                },
            ],
            "unit": "reqps",
            "thresholds": [],
            "alert": None,
        },
        {
            "id": 3,
            "title": f"[ERRORS] Taux d'erreur (%) — {service_name}",
            "type": "gauge",
            "description": "Golden Signal #3 — Errors : ratio erreurs/total",
            "queries": [
                {
                    "refId": "A",
                    "expr": (
                        "sum(rate(http_requests_errors_total"
                        "{service=~\"$service\"}[$interval]))"
                        " / sum(rate(http_requests_total"
                        "{service=~\"$service\"}[$interval])) * 100"
                    ),
                    "legendFormat": "error_rate_pct",
                },
            ],
            "unit": "percent",
            "min": 0,
            "max": 10,
            "thresholds": [
                {"value": 0.1, "color": "orange"},
                {"value": 1.0, "color": "red"},
            ],
            "alert": {
                "name": "HighErrorRate",
                "condition": "error_rate > 5%",
                "for": "2m",
                "severity": "critical",
            },
        },
        {
            "id": 4,
            "title": f"[SATURATION] Memoire RSS (%) — {service_name}",
            "type": "timeseries",
            "description": "Golden Signal #4 — Saturation : pression memoire par pod",
            "queries": [
                {
                    "refId": "A",
                    "expr": (
                        "process_resident_memory_bytes{service=~\"$service\"}"
                        " / node_memory_MemTotal_bytes * 100"
                    ),
                    "legendFormat": "{{pod}} mem%",
                },
            ],
            "unit": "percent",
            "thresholds": [
                {"value": 80, "color": "orange"},
                {"value": 90, "color": "red"},
            ],
            "alert": {
                "name": "HighMemoryUsage",
                "condition": "memory > 80%",
                "for": "5m",
                "severity": "warning",
            },
        },
    ]

    # Panels business metrics CaelumSwarm™
    panels_business = [
        {
            "id": 5,
            "title": "Scores Wave Engine (avg par domain)",
            "type": "barchart",
            "description": "Score composite moyen par domaine de droits humains",
            "queries": [
                {
                    "refId": "A",
                    "expr": "avg by (domain) (caelum_wave_engine_score)",
                    "legendFormat": "{{domain}}",
                },
            ],
            "unit": "short",
            "thresholds": [
                {"value": 40, "color": "orange"},
                {"value": 60, "color": "red"},
            ],
        },
        {
            "id": 6,
            "title": "Alertes conformite CSDDD (rate/heure)",
            "type": "timeseries",
            "description": "Alertes de conformite par niveau de severite",
            "queries": [
                {
                    "refId": "A",
                    "expr": "sum by (severity) (rate(caelum_compliance_alerts_total[1h]))",
                    "legendFormat": "{{severity}}",
                },
            ],
            "unit": "short",
        },
        {
            "id": 7,
            "title": "SLO Error Budget restant (%)",
            "type": "gauge",
            "description": "Budget d'erreur consomme pour les SLOs critiques",
            "queries": [
                {
                    "refId": "A",
                    "expr": (
                        "1 - ("
                        "sum(rate(http_requests_errors_total[30d])) / "
                        "sum(rate(http_requests_total[30d]))"
                        ") / (1 - 0.999)"
                    ),
                    "legendFormat": "api_availability_budget",
                },
            ],
            "unit": "percentunit",
            "min": 0,
            "max": 1,
            "thresholds": [
                {"value": 0.5, "color": "orange"},
                {"value": 0.2, "color": "red"},
            ],
        },
        {
            "id": 8,
            "title": "Generation rapports (p95 duree)",
            "type": "stat",
            "description": "Latence p95 de generation des rapports CSDDD",
            "queries": [
                {
                    "refId": "A",
                    "expr": (
                        "histogram_quantile(0.95, rate("
                        "caelum_report_generation_seconds_bucket[5m]))"
                    ),
                    "legendFormat": "p95_duration",
                },
            ],
            "unit": "s",
            "thresholds": [
                {"value": 20, "color": "orange"},
                {"value": 30, "color": "red"},
            ],
        },
    ]

    all_panels = panels_golden + panels_business

    return {
        "uid": uid,
        "title": f"CaelumSwarm(tm) — {service_name.replace('_', ' ').title()}",
        "description": dashboard_meta.get("description", f"Dashboard {service_name}"),
        "tags": dashboard_meta.get("tags", []),
        "refresh": dashboard_meta.get("refresh", "30s"),
        "schemaVersion": 39,
        "grafana_version": "10.4",
        "datasource": {
            "type": "prometheus",
            "uid": "caelum-prometheus",
            "url": "http://prometheus.caelum.svc.cluster.local:9090",
        },
        "template_variables": template_variables,
        "panels": all_panels,
        "panels_count": len(all_panels),
        "golden_signals_count": len(panels_golden),
        "business_panels_count": len(panels_business),
        "time_range": {"from": "now-6h", "to": "now"},
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


def generate_prometheus_yaml() -> str:
    """Genere le fichier prometheus.yml complet pour CaelumSwarm(tm).

    Produit un YAML valide pour Prometheus 2.51 incluant la configuration
    globale, tous les scrape_configs, la configuration alerting et les
    rule_files. Compatible avec remote_write Thanos et mTLS.

    Returns:
        str YAML complet pret a l'emploi.
    """
    cfg = PROMETHEUS_CONFIG
    global_cfg = cfg["global"]

    lines = [
        "# prometheus.yml — CaelumSwarm(tm) Production",
        f"# Generated: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"# Prometheus version: {cfg['version']}",
        "",
        "global:",
        f"  scrape_interval: {global_cfg['scrape_interval']}",
        f"  evaluation_interval: {global_cfg['evaluation_interval']}",
        f"  scrape_timeout: {global_cfg['scrape_timeout']}",
        "  external_labels:",
        f"    cluster: {global_cfg['external_labels']['cluster']}",
        f"    env: {global_cfg['external_labels']['env']}",
        "",
        "# Storage configuration (TSDB)",
        "storage:",
        f"  tsdb:",
        f"    path: {cfg['storage']['tsdb_path']}",
        f"    retention.time: {cfg['storage']['retention_time']}",
        f"    retention.size: {cfg['storage']['retention_size']}",
        "",
        "# Alerting — Alertmanager",
        "alerting:",
        "  alertmanagers:",
        "    - static_configs:",
        "        - targets:",
        "            - alertmanager.caelum.svc.cluster.local:9093",
        "      tls_config:",
        "        cert_file: /etc/prometheus/tls/tls.crt",
        "        key_file: /etc/prometheus/tls/tls.key",
        "",
        "# Rule files",
        "rule_files:",
        "  - /etc/prometheus/rules/sre_critical.yml",
        "  - /etc/prometheus/rules/business_alerts.yml",
        "  - /etc/prometheus/rules/infrastructure.yml",
        "  - /etc/prometheus/rules/slo_recording_rules.yml",
        "",
        "# Remote write — Thanos Receive (long-term storage)",
        "remote_write:",
        f"  - url: {cfg['remote_write']['url']}",
        "    queue_config:",
        f"      max_samples_per_send: {cfg['remote_write']['queue_config']['max_samples_per_send']}",
        f"      max_shards: {cfg['remote_write']['queue_config']['max_shards']}",
        "    tls_config:",
        "      cert_file: /etc/prometheus/tls/tls.crt",
        "      key_file: /etc/prometheus/tls/tls.key",
        "",
        "# Scrape configurations",
        "scrape_configs:",
    ]

    for job_key, job_cfg in SCRAPE_CONFIGS.items():
        lines.append(f"")
        lines.append(f"  # --- {job_key} ---")
        lines.append(f"  - job_name: {job_cfg['job_name']}")
        if "scrape_interval" in job_cfg:
            lines.append(f"    scrape_interval: {job_cfg['scrape_interval']}")
        if "metrics_path" in job_cfg:
            lines.append(f"    metrics_path: {job_cfg['metrics_path']}")
        if "honor_labels" in job_cfg:
            lines.append(f"    honor_labels: {str(job_cfg['honor_labels']).lower()}")
        if job_cfg.get("target_discovery") == "consul":
            lines.append("    consul_sd_configs:")
            lines.append("      - server: consul.caelum.svc.cluster.local:8500")
            lines.append(f"        services: [{job_cfg['consul_service']}]")
            lines.append("    relabel_configs:")
            for rl in job_cfg.get("relabel_configs", []):
                lines.append(f"      - source_labels: {rl['source_labels']}")
                lines.append(f"        target_label: {rl['target_label']}")
        else:
            port = job_cfg.get("port", 9090)
            lines.append("    static_configs:")
            lines.append("      - targets:")
            lines.append(f"          - {job_key.replace('_', '-')}.caelum.svc.cluster.local:{port}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 3. POINT D'ENTREE
# ---------------------------------------------------------------------------


def _sep(char: str = "-", width: int = 72) -> str:
    return char * width


def _section(title: str) -> None:
    print()
    print(_sep("="))
    print(f"  {title}")
    print(_sep("="))


def _subsection(title: str) -> None:
    print()
    print(_sep("-"))
    print(f"  {title}")
    print(_sep("-"))


if __name__ == "__main__":

    print(_sep("="))
    print("  PROMETHEUS MONITORING STACK — CaelumSwarm(tm)")
    print("  Prometheus 2.51 / Alertmanager 0.27 / Grafana 10.4 / Thanos")
    print("  Droits humains · Conformite CSDDD 2024 · SRE Golden Signals")
    print(_sep("="))

    # ------------------------------------------------------------------
    # 1. Prometheus config — global + scrape configs + Thanos
    # ------------------------------------------------------------------
    _section("1. PROMETHEUS CONFIG — GLOBAL + SCRAPE CONFIGS + THANOS")

    prom_cfg = PROMETHEUS_CONFIG
    print(f"\n  Version         : {prom_cfg['version']}")
    print(f"  Cluster label   : {prom_cfg['global']['external_labels']['cluster']}")
    print(f"  Environment     : {prom_cfg['global']['external_labels']['env']}")
    print(f"  Scrape interval : {prom_cfg['global']['scrape_interval']}")
    print(f"  Eval interval   : {prom_cfg['global']['evaluation_interval']}")
    print(f"  Retention time  : {prom_cfg['storage']['retention_time']}")
    print(f"  Retention size  : {prom_cfg['storage']['retention_size']}")
    print(f"  TSDB path       : {prom_cfg['storage']['tsdb_path']}")
    print(f"  Remote write    : {prom_cfg['remote_write']['url']}")

    print(f"\n  Scrape Jobs ({len(SCRAPE_CONFIGS)}) :")
    for job_key, job_cfg in SCRAPE_CONFIGS.items():
        interval = job_cfg.get("scrape_interval", PROMETHEUS_CONFIG["global"]["scrape_interval"])
        port = job_cfg.get("port", "consul")
        print(f"    {job_cfg['job_name']:<40s} interval={interval:<5s}  port={port}")

    print(f"\n  Metriques cataloguees ({len(METRICS_CATALOG)}) :")
    for cat_key, cat in METRICS_CATALOG.items():
        print(
            f"    {cat['metric']:<45s} type={cat.get('type','?'):<10s}  SLO: {cat.get('slo','n/a')}"
        )

    # ------------------------------------------------------------------
    # 2. prometheus.yml genere
    # ------------------------------------------------------------------
    _section("2. PROMETHEUS.YML GENERE")
    yaml_content = generate_prometheus_yaml()
    lines_yml = yaml_content.split("\n")
    print(f"\n  Fichier prometheus.yml ({len(lines_yml)} lignes) — extrait :\n")
    for line in lines_yml[:55]:
        print(f"    {line}")
    print(f"    ... ({len(lines_yml) - 55} lignes supplementaires)")

    # ------------------------------------------------------------------
    # 3. PromQL queries — latency p99, error rate, throughput
    # ------------------------------------------------------------------
    _section("3. PROMQL QUERIES — LATENCY P99 / ERROR RATE / THROUGHPUT")

    promql_specs = [
        ("http_request_duration_seconds", "histogram_quantile_p99", "5m"),
        ("http_requests_total", "error_rate", "5m"),
        ("http_requests_total", "sum_by_service", "1m"),
        ("caelum_wave_engine_duration_seconds", "histogram_quantile_p99", "5m"),
        ("caelum_compliance_alerts_total", "rate", "1h"),
    ]
    for metric, agg, win in promql_specs:
        result = generate_promql_query(metric, agg, win)
        print(f"\n  [{agg}]")
        print(f"    Query   : {result['query_string']}")
        print(f"    Resultat: {result['example_result']}")
        print(f"    SLO ref : {result['slo_reference']}")
        print(f"    Note    : {result['explanation'][:90]}...")

    # ------------------------------------------------------------------
    # 4. Error budget calculations — 5 SLOs
    # ------------------------------------------------------------------
    _section("4. ERROR BUDGET CALCULATIONS — 5 SLOs")

    # Uptime simules legèrement sous/sur la cible pour creer des scenarios varies
    uptime_scenarios = {
        "api_availability":    0.9987,
        "api_latency_p99":     0.9894,
        "wave_engine_uptime":  0.9996,
        "report_generation":   0.9901,
        "alert_delivery":      0.9991,
    }

    print()
    print(
        f"  {'SLO':<25s} {'Cible':>8s} {'Actuel':>8s} {'Budget restant':>15s}"
        f" {'Burn rate':>10s} {'Statut':<10s}"
    )
    print("  " + "-" * 80)

    for slo_name, uptime in uptime_scenarios.items():
        eb = calculate_error_budget(slo_name, uptime)
        target_pct = f"{eb['target_uptime']*100:.3f}%"
        current_pct = f"{uptime*100:.3f}%"
        remaining = f"{eb['budget_remaining_minutes']:.1f}m ({eb['budget_remaining_pct']:.1f}%)"
        burn = f"x{eb['burn_rate']:.2f}"
        status = eb["status"]
        print(
            f"  {slo_name:<25s} {target_pct:>8s} {current_pct:>8s}"
            f" {remaining:>15s} {burn:>10s} [{status}]"
        )
        for rec in eb["recommendations"]:
            print(f"    -> {rec}")

    # ------------------------------------------------------------------
    # 5. Alert simulation — HighErrorRate -> PagerDuty -> Slack
    # ------------------------------------------------------------------
    _section("5. SIMULATION ALERTE — HighErrorRate -> PagerDuty -> Slack")

    sim = simulate_alert_firing("HighErrorRate", duration_minutes=18)
    print(f"\n  Alerte         : {sim['alert_name']}")
    print(f"  Groupe         : {sim['alert_group']}")
    print(f"  Severite       : {sim['severity']}")
    print(f"  Fingerprint    : {sim['fingerprint']}")
    print(f"  Expr           : {sim['expr'][:70]}...")
    print(f"  For duration   : {sim['for_duration']}")
    print(f"  Annotation     : {sim['annotation']}")

    print(f"\n  Timeline alerte :")
    for evt in sim["alert_timeline"]:
        print(f"    [{evt['time']}] [{evt['state']:<8s}] {evt['event']}")

    print(f"\n  Notifications envoyees :")
    for notif in sim["notifications_sent"]:
        print(
            f"    -> {notif['receiver']:<30s} canal={notif['channel']:<30s}"
            f" status={notif['delivery_status']}"
        )

    print(f"\n  Chemin d'escalade : {' -> '.join(sim['escalation_path'])}")
    if sim["inhibitions_applied"]:
        for inh in sim["inhibitions_applied"]:
            print(f"  Inhibition : {inh['reason']}")

    # ------------------------------------------------------------------
    # 6. Alertmanager routes
    # ------------------------------------------------------------------
    _section("6. ALERTMANAGER ROUTES")

    am = ALERTMANAGER_CONFIG
    print(f"\n  Alertmanager version : {am['version']}")
    print(f"  Receiver par defaut  : {am['routes']['receiver']}")
    print(f"  Group by             : {am['routes']['group_by']}")
    print(f"  Group wait           : {am['routes']['group_wait']}")
    print(f"  Group interval       : {am['routes']['group_interval']}")
    print(f"  Repeat interval      : {am['routes']['repeat_interval']}")

    print(f"\n  Routes de routage ({len(am['routes']['routes'])}) :")
    for route in am["routes"]["routes"]:
        match_str = " & ".join(f"{k}={v}" for k, v in route["match"].items())
        cont = " [continue]" if route.get("continue") else ""
        print(f"    match({match_str}) -> {route['receiver']}{cont}")

    print(f"\n  Receivers ({len(am['receivers'])}) :")
    for recv_name, recv_cfg in am["receivers"].items():
        channel = recv_cfg.get("channel") or recv_cfg.get("to", "n/a")
        key_type = "integration_key" if "integration_key" in recv_cfg else "webhook_url"
        print(f"    {recv_name:<30s} channel={channel:<30s} credentials={key_type}=VAULT")

    print(f"\n  Inhibition rules ({len(am['inhibit_rules'])}) :")
    for rule in am["inhibit_rules"]:
        print(
            f"    source={rule['source_match']['severity']} supprime"
            f" target={rule['target_match']['severity']}"
            f" when equal={rule['equal']}"
        )

    # ------------------------------------------------------------------
    # 7. Grafana dashboards overview
    # ------------------------------------------------------------------
    _section("7. GRAFANA DASHBOARDS OVERVIEW (10.4)")

    total_panels = sum(d["panels"] for d in GRAFANA_DASHBOARDS.values())
    print(f"\n  Dashboards : {len(GRAFANA_DASHBOARDS)}  |  Total panels : {total_panels}\n")
    print(f"  {'Dashboard':<30s} {'Panels':>7s} {'Refresh':>8s}  Tags")
    print("  " + "-" * 65)
    for dash_name, dash_cfg in GRAFANA_DASHBOARDS.items():
        tags = ", ".join(dash_cfg["tags"])
        print(
            f"  {dash_name:<30s} {dash_cfg['panels']:>7d}"
            f" {dash_cfg['refresh']:>8s}  [{tags}]"
        )

    # Design detaille d'un dashboard
    print()
    dashboard_detail = design_grafana_dashboard("caelum_overview")
    print(f"  Dashboard design — '{dashboard_detail['title']}' :")
    print(f"    UID           : {dashboard_detail['uid']}")
    print(f"    Panels total  : {dashboard_detail['panels_count']}")
    print(f"      Golden Signals : {dashboard_detail['golden_signals_count']}")
    print(f"      Business KPIs  : {dashboard_detail['business_panels_count']}")
    print(f"    Variables Grafana : {len(dashboard_detail['template_variables'])}")
    for var in dashboard_detail["template_variables"]:
        print(f"      ${var['name']:<15s} type={var['type']}")
    print(f"\n    Panels ({dashboard_detail['panels_count']}) :")
    for panel in dashboard_detail["panels"]:
        alert_info = f"  alert={panel['alert']['name']}" if panel.get("alert") else ""
        print(f"      [#{panel['id']}] [{panel['type']:<12s}] {panel['title'][:55]}{alert_info}")

    # ------------------------------------------------------------------
    # 8. Thanos long-term retention config
    # ------------------------------------------------------------------
    _section("8. THANOS — STOCKAGE LONG TERME")

    thanos = THANOS_CONFIG
    print(f"\n  Composants     : {', '.join(thanos['components'])}")
    print(f"  Object storage : {thanos['object_storage']}")
    print(f"  Query frontend : {'active (cache + sharding)' if thanos['query_frontend'] else 'desactive'}")
    print(f"\n  Retention par resolution :")
    for res, ret in thanos["retention"].items():
        label = {
            "raw": "donnees brutes (15s scrape)",
            "5m_downsampled": "downsampled 5min",
            "1h_downsampled": "downsampled 1h",
        }.get(res, res)
        print(f"    {label:<35s} : {ret}")

    qfe = thanos["query_frontend_config"]
    print(f"\n  Query Frontend :")
    print(f"    Cache backend : {qfe['cache_backend']} ({qfe['cache_host']})")
    print(f"    Split interval: {qfe['split_interval']}")
    print(f"    Max retries   : {qfe['max_retries']}")

    sg = thanos["store_gateway"]
    print(f"\n  Store Gateway :")
    print(f"    Chunk pool    : {sg['chunk_pool_size']}")
    print(f"    Index cache   : {sg['index_cache']}")

    comp = thanos["compactor"]
    print(f"\n  Compactor :")
    print(f"    Consistency delay : {comp['consistency_delay']}")
    print(f"    Retention raw     : {comp['retention_resolution_raw']}")
    print(f"    Retention 5m      : {comp['retention_resolution_5m']}")
    print(f"    Retention 1h      : {comp['retention_resolution_1h']}")

    # ------------------------------------------------------------------
    # 9. SLO tracking report — toutes les SLOs
    # ------------------------------------------------------------------
    _section("9. SLO TRACKING REPORT — TOUTES LES SLOs")

    print()
    for slo_name, slo_def in SLO_DEFINITIONS.items():
        uptime_val = uptime_scenarios.get(slo_name, 0.999)
        eb = calculate_error_budget(slo_name, uptime_val)
        slo_color_icon = {"SAIN": "[OK]", "ATTENTION": "[!!]", "CRITIQUE": "[!!]"}.get(
            eb["status"], "[?]"
        )
        print(f"  {slo_color_icon} {slo_name}")
        print(f"     Description      : {slo_def.get('description', 'n/a')}")
        print(f"     Cible            : {eb['target_uptime']*100:.4f}%")
        print(f"     Uptime actuel    : {uptime_val*100:.4f}%")
        print(f"     Budget total     : {eb['total_error_budget_minutes']:.2f} min / 30j")
        print(f"     Budget consomme  : {eb['consumed_minutes']:.2f} min")
        print(f"     Budget restant   : {eb['budget_remaining_minutes']:.2f} min ({eb['budget_remaining_pct']:.1f}%)")
        print(f"     Burn rate        : x{eb['burn_rate']:.2f}")
        print(f"     Exhaustion prev. : {eb['projected_exhaustion_date']}")
        print(f"     Statut           : {eb['status']}")
        print()

    # ------------------------------------------------------------------
    # 10. Monitoring Security — TLS, auth, RBAC Grafana
    # ------------------------------------------------------------------
    _section("10. MONITORING SECURITY — TLS / AUTH / RBAC GRAFANA")

    sec = MONITORING_SECURITY

    print("\n  Prometheus TLS :")
    prom_tls = sec["prometheus"]["tls"]
    print(f"    cert_file          : {prom_tls['cert_file']}")
    print(f"    key_file           : {prom_tls['key_file']}")
    print(f"    client_ca_file     : {prom_tls['client_ca_file']}")
    print(f"    client_auth_type   : {prom_tls['client_auth_type']}")
    print(f"    bearer_token       : {sec['prometheus']['bearer_token']}")
    print(f"    web_config         : {sec['prometheus']['web_config']}")

    print("\n  Alertmanager TLS :")
    am_tls = sec["alertmanager"]["tls"]
    print(f"    cert_file          : {am_tls['cert_file']}")
    print(f"    key_file           : {am_tls['key_file']}")
    print(f"    cluster_tls        : {sec['alertmanager']['cluster_tls']}")
    print(f"    gossip_encryption  : {sec['alertmanager']['gossip_encryption']}")

    print("\n  Grafana 10.4 — Auth + RBAC :")
    gf = sec["grafana"]
    auth = gf["auth"]
    print(f"    OAuth provider     : {auth['oauth_provider']}")
    print(f"    allow_sign_up      : {auth['allow_sign_up']}")
    print(f"    auto_login         : {auth['auto_login']}")
    print(f"    TLS protocol       : {gf['tls']['protocol']}")
    print(f"    cookie_secure      : {gf['cookie_secure']}")
    print(f"    secret_key         : {gf['secret_key']}")
    print(f"\n    RBAC roles ({len(gf['rbac'])}) :")
    for role_key, role_name in gf["rbac"].items():
        print(f"      {role_key:<25s} -> {role_name}")
    print(f"\n    Datasource permissions :")
    for ds, roles in gf["data_source_permissions"].items():
        print(f"      {ds:<30s} -> {roles}")

    print("\n  Network policies :")
    for component, allowed in sec["network_policies"].items():
        print(f"    {component:<30s} ingress autorise depuis : {allowed}")

    # ------------------------------------------------------------------
    # Resume alerting rules
    # ------------------------------------------------------------------
    _subsection("RESUME ALERTING RULES")

    total_rules = sum(len(v) for v in ALERTING_RULES.values())
    print(f"\n  Total regles d'alerte : {total_rules}")
    for group_name, rules in ALERTING_RULES.items():
        print(f"\n  [{group_name}] ({len(rules)} regles) :")
        for rule in rules:
            sev = rule.get("severity", "?")
            for_d = rule.get("for", "0m")
            print(f"    {rule['alert']:<35s} severity={sev:<10s} for={for_d}")

    # ------------------------------------------------------------------
    # Bilan final
    # ------------------------------------------------------------------
    print()
    print(_sep("="))
    print(
        "  Prometheus Monitoring Agent — PRET"
        " (Prometheus 2.51 / Alertmanager 0.27 / Grafana 10.4 / Thanos)"
    )
    print(_sep("="))
    print(
        f"  Scrape jobs : {len(SCRAPE_CONFIGS)}"
        f"  |  Metriques : {len(METRICS_CATALOG)}"
        f"  |  Regles alerte : {total_rules}"
        f"  |  Dashboards Grafana : {len(GRAFANA_DASHBOARDS)}"
    )
    print(
        f"  SLOs surveilles : {len(SLO_DEFINITIONS)}"
        f"  |  Composants Thanos : {len(THANOS_CONFIG['components'])}"
        f"  |  Receivers AM : {len(ALERTMANAGER_CONFIG['receivers'])}"
    )
    print(_sep("="))
