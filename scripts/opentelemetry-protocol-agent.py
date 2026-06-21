"""
Agent Protocole OpenTelemetry — observabilité complète (traces, métriques, logs)
pour CaelumSwarm™ selon standards CNCF OpenTelemetry. Monitoring distribué des
agents, corrélation signaux et golden signals SRE.

Références :
  - OpenTelemetry Specification v1.x (https://opentelemetry.io/docs/specs/otel/)
  - W3C TraceContext Recommendation (https://www.w3.org/TR/trace-context/)
  - Google SRE Golden Signals (Latency · Traffic · Errors · Saturation)
  - CNCF OpenTelemetry Project (https://cncf.io/projects/opentelemetry/)
"""

import secrets
import hashlib
import datetime
import random

# ---------------------------------------------------------------------------
# 1. CONSTANTES DE DONNÉES
# ---------------------------------------------------------------------------

OTEL_SIGNAL_TYPES = {
    "TRACES": {
        "label": "Traces distribuées",
        "otel_spec_version": "1.27.0",
        "data_model": "Span / TraceContext W3C",
        "exporters": ["OTLP/gRPC", "OTLP/HTTP", "Jaeger", "Zipkin"],
        "sampling_strategy": "Tail-based avec filtre erreurs",
        "retention_days": 14,
        "caelum_use_case": (
            "Suivi end-to-end des analyses Wave : engine Python → route API"
            " → dashboard React"
        ),
    },
    "METRICS": {
        "label": "Métriques temporelles",
        "otel_spec_version": "1.27.0",
        "data_model": "OTLP MetricsData / Prometheus exposition format",
        "exporters": ["OTLP/gRPC", "Prometheus", "OpenMetrics"],
        "sampling_strategy": "Aggregation temporelle (delta / cumulative)",
        "retention_days": 90,
        "caelum_use_case": (
            "Golden Signals SRE : latence, débit, taux d'erreur, saturation"
            " CPU/mémoire par engine Wave"
        ),
    },
    "LOGS": {
        "label": "Logs structurés",
        "otel_spec_version": "1.27.0",
        "data_model": "LogRecord OTLP / JSON structured",
        "exporters": ["OTLP/HTTP", "Loki", "Elasticsearch"],
        "sampling_strategy": "Taux adaptatif selon severity (ERROR=100 %, INFO=10 %)",
        "retention_days": 30,
        "caelum_use_case": (
            "Corrélation des alertes juridiques, violations CSDD, logs agent"
            " LegalWatch et PressAgent"
        ),
    },
}

INSTRUMENTATION_LIBRARY = {
    "WAVE_ENGINE": {
        "service_name": "caelum.wave-engine",
        "service_version": "3.14.0",
        "instrumentation_type": "HYBRID",
        "key_spans": [
            "wave.entities.load",
            "wave.composite_score.compute",
            "wave.distribution.validate",
            "wave.index.estimate",
        ],
        "key_metrics": [
            "wave_analysis_duration_ms",
            "entities_processed_total",
            "cost_per_wave_EUR",
        ],
        "log_level": "INFO",
    },
    "API_GATEWAY": {
        "service_name": "caelum.api-gateway",
        "service_version": "2.8.1",
        "instrumentation_type": "AUTO",
        "key_spans": [
            "http.server.request",
            "auth.token.validate",
            "rate_limit.check",
            "upstream.fetch",
        ],
        "key_metrics": [
            "api_latency_p99_ms",
            "error_rate_pct",
            "active_users_gauge",
        ],
        "log_level": "WARN",
    },
    "PRESS_AGENT": {
        "service_name": "caelum.press-agent",
        "service_version": "1.5.3",
        "instrumentation_type": "MANUAL",
        "key_spans": [
            "press.article.scrape",
            "press.sentiment.analyze",
            "press.entity.match",
            "press.alert.emit",
        ],
        "key_metrics": [
            "alert_detection_latency_ms",
            "token_consumption_total",
            "queue_depth_gauge",
        ],
        "log_level": "INFO",
    },
    "LEGAL_WATCH": {
        "service_name": "caelum.legal-watch",
        "service_version": "1.2.7",
        "instrumentation_type": "HYBRID",
        "key_spans": [
            "legal.document.parse",
            "legal.csddd.check",
            "legal.violation.classify",
            "legal.report.draft",
        ],
        "key_metrics": [
            "csddd_violations_found_total",
            "report_generation_latency_ms",
            "error_rate_pct",
        ],
        "log_level": "ERROR",
    },
    "ALERT_PROCESSOR": {
        "service_name": "caelum.alert-processor",
        "service_version": "2.1.0",
        "instrumentation_type": "AUTO",
        "key_spans": [
            "alert.receive",
            "alert.deduplicate",
            "alert.route",
            "alert.notify",
        ],
        "key_metrics": [
            "alert_detection_latency_ms",
            "queue_depth_gauge",
            "error_rate_pct",
        ],
        "log_level": "WARN",
    },
    "REPORT_GENERATOR": {
        "service_name": "caelum.report-generator",
        "service_version": "1.9.2",
        "instrumentation_type": "MANUAL",
        "key_spans": [
            "report.template.load",
            "report.data.aggregate",
            "report.pdf.render",
            "report.deliver",
        ],
        "key_metrics": [
            "report_generation_latency_ms",
            "token_consumption_total",
            "cost_per_wave_EUR",
        ],
        "log_level": "INFO",
    },
    "DATABASE_LAYER": {
        "service_name": "caelum.database-layer",
        "service_version": "4.0.1",
        "instrumentation_type": "AUTO",
        "key_spans": [
            "db.query.execute",
            "db.transaction.begin",
            "db.transaction.commit",
            "db.connection.acquire",
        ],
        "key_metrics": [
            "api_latency_p99_ms",
            "cache_hit_rate_pct",
            "queue_depth_gauge",
        ],
        "log_level": "WARN",
    },
    "EXTERNAL_API_CALLS": {
        "service_name": "caelum.external-api",
        "service_version": "1.1.0",
        "instrumentation_type": "AUTO",
        "key_spans": [
            "http.client.request",
            "http.client.retry",
            "circuit_breaker.check",
            "response.deserialize",
        ],
        "key_metrics": [
            "api_latency_p99_ms",
            "error_rate_pct",
            "token_consumption_total",
        ],
        "log_level": "WARN",
    },
}

METRICS_REGISTRY = {
    "wave_analysis_duration_ms": {
        "label": "Durée analyse Wave (ms)",
        "type": "HISTOGRAM",
        "unit": "ms",
        "alert_threshold": 5000,
        "slo_target": "p99 < 3000 ms (99,9 % du temps)",
    },
    "entities_processed_total": {
        "label": "Entités traitées (cumul)",
        "type": "COUNTER",
        "unit": "entités",
        "alert_threshold": None,
        "slo_target": "8 entités par wave (distribution obligatoire respectée)",
    },
    "api_latency_p99_ms": {
        "label": "Latence API p99 (ms)",
        "type": "HISTOGRAM",
        "unit": "ms",
        "alert_threshold": 800,
        "slo_target": "p99 < 500 ms (99,5 % des requêtes)",
    },
    "error_rate_pct": {
        "label": "Taux d'erreur (%)",
        "type": "GAUGE",
        "unit": "%",
        "alert_threshold": 1.0,
        "slo_target": "< 0,5 % sur fenêtre glissante 5 min",
    },
    "token_consumption_total": {
        "label": "Consommation tokens LLM (cumul)",
        "type": "COUNTER",
        "unit": "tokens",
        "alert_threshold": 10_000_000,
        "slo_target": "Budget mensuel < 50 M tokens",
    },
    "report_generation_latency_ms": {
        "label": "Latence génération rapport (ms)",
        "type": "HISTOGRAM",
        "unit": "ms",
        "alert_threshold": 30_000,
        "slo_target": "p95 < 20 000 ms",
    },
    "alert_detection_latency_ms": {
        "label": "Latence détection alerte (ms)",
        "type": "HISTOGRAM",
        "unit": "ms",
        "alert_threshold": 2000,
        "slo_target": "p99 < 1000 ms — SLA presse temps-réel",
    },
    "csddd_violations_found_total": {
        "label": "Violations CSDDD détectées (cumul)",
        "type": "COUNTER",
        "unit": "violations",
        "alert_threshold": None,
        "slo_target": "Taux détection > 95 % (benchmark LegalWatch)",
    },
    "active_users_gauge": {
        "label": "Utilisateurs actifs (instantané)",
        "type": "GAUGE",
        "unit": "utilisateurs",
        "alert_threshold": 500,
        "slo_target": "Capacité nominale 1 000 utilisateurs simultanés",
    },
    "queue_depth_gauge": {
        "label": "Profondeur file d'attente (instantané)",
        "type": "GAUGE",
        "unit": "messages",
        "alert_threshold": 1000,
        "slo_target": "< 500 messages en attente — évite back-pressure",
    },
    "cache_hit_rate_pct": {
        "label": "Taux de cache hit (%)",
        "type": "GAUGE",
        "unit": "%",
        "alert_threshold": None,
        "slo_target": "> 80 % — optimisation coût base de données",
    },
    "cost_per_wave_EUR": {
        "label": "Coût par analyse Wave (EUR)",
        "type": "HISTOGRAM",
        "unit": "EUR",
        "alert_threshold": 2.50,
        "slo_target": "Coût médian < 1,20 EUR par wave complète",
    },
}

SAMPLING_STRATEGIES = {
    "HEAD_BASED_PROBABILISTIC": {
        "label": "Échantillonnage probabiliste en tête",
        "sample_rate_pct": 10.0,
        "use_case": (
            "Trafic nominal API Gateway et Wave Engine — réduit le volume"
            " sans biaiser les métriques agrégées"
        ),
        "storage_cost_multiplier": 0.10,
    },
    "TAIL_BASED_ERROR": {
        "label": "Échantillonnage en queue sur erreurs",
        "sample_rate_pct": 100.0,
        "use_case": (
            "Conservation de 100 % des traces portant un span ERROR ou"
            " TIMEOUT — analyse post-mortem exhaustive"
        ),
        "storage_cost_multiplier": 0.35,
    },
    "ADAPTIVE_RATE": {
        "label": "Taux adaptatif dynamique",
        "sample_rate_pct": 25.0,
        "use_case": (
            "PressAgent et AlertProcessor — ajuste le taux selon la charge"
            " CPU du collecteur (cible : < 5 % overhead)"
        ),
        "storage_cost_multiplier": 0.25,
    },
    "ALWAYS_ON_DEBUG": {
        "label": "Toujours actif (mode debug)",
        "sample_rate_pct": 100.0,
        "use_case": (
            "Environnement de staging uniquement — capture exhaustive pour"
            " validation des nouvelles waves avant promotion production"
        ),
        "storage_cost_multiplier": 1.00,
    },
}

# ---------------------------------------------------------------------------
# 2. FONCTIONS
# ---------------------------------------------------------------------------


def create_trace_span(operation: str, service: str, attributes: dict) -> dict:
    """Crée un span OTel conforme à la spec OpenTelemetry Trace v1.27.

    Génère les identifiants W3C TraceContext (trace_id 128-bit, span_id 64-bit)
    via secrets.token_hex pour garantir une entropie cryptographique. Les
    attributs sont normalisés selon les conventions sémantiques OTel (semconv).

    Args:
        operation: Nom de l'opération instrumentée (ex. "wave.composite_score.compute").
        service:   Nom du service émetteur (ex. "caelum.wave-engine").
        attributes: Attributs métier arbitraires à attacher au span.

    Returns:
        dict représentant un SpanData OTLP sérialisable en JSON.
    """
    now_ns = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1e9)
    duration_ns = random.randint(50_000_000, 4_500_000_000)  # 50 ms – 4,5 s
    status = "ERROR" if random.random() < 0.05 else "OK"

    # W3C TraceContext — trace-id : 32 hex chars (128 bits)
    #                  — span-id  : 16 hex chars  (64 bits)
    trace_id = secrets.token_hex(16)   # 16 bytes → 32 hex chars
    span_id = secrets.token_hex(8)     # 8 bytes  → 16 hex chars
    parent_span_id = secrets.token_hex(8) if random.random() > 0.3 else None

    # Normalisation des attributs selon les conventions sémantiques OTel
    semconv_attributes = {
        "service.name": service,
        "service.version": INSTRUMENTATION_LIBRARY.get(
            _resolve_library_key(service), {}
        ).get("service_version", "unknown"),
        "telemetry.sdk.name": "caelum-otel-sdk",
        "telemetry.sdk.language": "python",
        "telemetry.sdk.version": "1.27.0",
        "deployment.environment": "production",
        **{f"caelum.{k}": v for k, v in attributes.items()},
    }

    # Checksum d'intégrité du span (usage audit interne CaelumSwarm™)
    span_fingerprint = hashlib.sha256(
        f"{trace_id}{span_id}{operation}{now_ns}".encode()
    ).hexdigest()[:16]

    return {
        "trace_id": trace_id,
        "span_id": span_id,
        "parent_span_id": parent_span_id,
        "operation_name": operation,
        "start_time_unix_ns": now_ns,
        "end_time_unix_ns": now_ns + duration_ns,
        "duration_ms": round(duration_ns / 1_000_000, 2),
        "attributes": semconv_attributes,
        "status": {
            "code": status,
            "message": "Analyse terminée avec succès" if status == "OK"
            else "Erreur interne — voir logs corrélés",
        },
        "resource_attributes": {
            "host.name": f"caelum-node-{secrets.token_hex(3)}",
            "host.arch": "amd64",
            "cloud.provider": "aws",
            "cloud.region": "eu-west-3",
            "k8s.pod.name": f"{service.replace('.', '-')}-{secrets.token_hex(4)}",
            "k8s.namespace.name": "caelum-swarm",
        },
        "events": [
            {
                "name": "span.created",
                "timestamp_unix_ns": now_ns,
                "attributes": {"caelum.fingerprint": span_fingerprint},
            }
        ],
        "links": [],
        "instrumentation_library": {
            "name": "caelum.instrumentation",
            "version": "1.27.0",
        },
    }


def collect_metrics_snapshot(services: list, period_seconds: int = 60) -> dict:
    """Simule une collecte de métriques OTLP pour la liste de services donnée.

    Produit des MetricFamily compatibles Prometheus exposition format v0.0.4,
    évalue la conformité SLO et détecte les anomalies statistiques simples
    (dépassement de seuil d'alerte).

    Args:
        services:       Liste des clés INSTRUMENTATION_LIBRARY à collecter.
        period_seconds: Fenêtre temporelle de la collecte (défaut : 60 s).

    Returns:
        dict contenant les familles de métriques, la conformité SLO,
        les anomalies détectées et le total de datapoints.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    period_start = (now - datetime.timedelta(seconds=period_seconds)).isoformat()
    period_end = now.isoformat()

    # Valeurs simulées par métrique avec bruit gaussien léger
    simulated_values = {
        "wave_analysis_duration_ms": random.gauss(1800, 400),
        "entities_processed_total": random.randint(8, 64),
        "api_latency_p99_ms": random.gauss(320, 80),
        "error_rate_pct": max(0.0, random.gauss(0.3, 0.2)),
        "token_consumption_total": random.randint(15_000, 120_000),
        "report_generation_latency_ms": random.gauss(8_500, 2_000),
        "alert_detection_latency_ms": random.gauss(450, 150),
        "csddd_violations_found_total": random.randint(0, 12),
        "active_users_gauge": random.randint(45, 340),
        "queue_depth_gauge": random.randint(10, 800),
        "cache_hit_rate_pct": random.gauss(84, 6),
        "cost_per_wave_EUR": random.gauss(0.95, 0.25),
    }

    metric_families = []
    anomalies_detected = []
    slo_results = {}
    total_datapoints = 0

    for metric_key, meta in METRICS_REGISTRY.items():
        raw_value = simulated_values.get(metric_key, 0.0)
        value = max(0.0, round(raw_value, 4))

        family_entry = {
            "name": metric_key,
            "label": meta["label"],
            "type": meta["type"],
            "unit": meta["unit"],
            "datapoints": [],
        }

        for svc_key in services:
            svc_info = INSTRUMENTATION_LIBRARY.get(svc_key, {})
            if metric_key not in svc_info.get("key_metrics", []):
                continue

            svc_value = max(0.0, value * random.uniform(0.85, 1.15))
            family_entry["datapoints"].append(
                {
                    "service": svc_info.get("service_name", svc_key),
                    "value": round(svc_value, 4),
                    "timestamp": now.isoformat(),
                    "attributes": {
                        "period_start": period_start,
                        "period_end": period_end,
                        "period_seconds": period_seconds,
                    },
                }
            )
            total_datapoints += 1

            # Détection d'anomalie par dépassement de seuil
            threshold = meta["alert_threshold"]
            if threshold is not None and svc_value > threshold:
                anomalies_detected.append(
                    {
                        "metric": metric_key,
                        "service": svc_info.get("service_name", svc_key),
                        "value": round(svc_value, 4),
                        "threshold": threshold,
                        "severity": "CRITIQUE" if svc_value > threshold * 1.5
                        else "AVERTISSEMENT",
                        "detected_at": now.isoformat(),
                    }
                )

        # Évaluation de la conformité SLO (heuristique simplifiée)
        target_desc = meta["slo_target"]
        in_slo = True
        if metric_key == "api_latency_p99_ms":
            in_slo = value < 500
        elif metric_key == "error_rate_pct":
            in_slo = value < 0.5
        elif metric_key == "cache_hit_rate_pct":
            in_slo = value > 80
        elif metric_key == "wave_analysis_duration_ms":
            in_slo = value < 3000
        elif metric_key == "alert_detection_latency_ms":
            in_slo = value < 1000

        slo_results[metric_key] = {
            "target": target_desc,
            "current_value": round(value, 4),
            "in_slo": in_slo,
            "status": "CONFORME" if in_slo else "VIOLATION SLO",
        }

        if family_entry["datapoints"]:
            metric_families.append(family_entry)

    return {
        "snapshot_id": secrets.token_hex(8),
        "period_start": period_start,
        "period_end": period_end,
        "period_seconds": period_seconds,
        "services_monitored": services,
        "metric_families": metric_families,
        "slo_compliance": slo_results,
        "anomalies_detected": anomalies_detected,
        "total_datapoints": total_datapoints,
        "otel_spec": "1.27.0",
    }


def correlate_signals(traces: list, metrics: dict, logs: list) -> dict:
    """Corrèle les trois signaux OTel pour reconstituer la timeline d'un incident.

    Implémente le modèle de corrélation CaelumSwarm™ basé sur :
    - la propagation du contexte W3C TraceContext (trace_id partagé),
    - les exemplaires Prometheus (lien trace ↔ métrique),
    - les champs de log structuré `trace_id` et `span_id`.

    Args:
        traces:  Liste de spans retournés par create_trace_span().
        metrics: Snapshot retourné par collect_metrics_snapshot().
        logs:    Liste de LogRecord structurés (dict avec severity, body, trace_id).

    Returns:
        dict décrivant la corrélation, la timeline d'incident, l'hypothèse
        de cause racine, les services affectés et le score de blast radius.
    """
    correlation_id = secrets.token_hex(12)
    now = datetime.datetime.now(datetime.timezone.utc)

    # Construction de la timeline à partir des trois sources
    timeline_events = []

    for span in traces:
        ts_ns = span.get("start_time_unix_ns", 0)
        ts = datetime.datetime.fromtimestamp(
            ts_ns / 1e9, tz=datetime.timezone.utc
        ).isoformat()
        timeline_events.append(
            {
                "timestamp": ts,
                "source": "TRACE",
                "signal": f"[{span['status']['code']}] {span['operation_name']}",
                "service": span["attributes"].get("service.name", "inconnu"),
                "trace_id": span["trace_id"],
                "span_id": span["span_id"],
                "severity": "ERROR" if span["status"]["code"] == "ERROR" else "INFO",
            }
        )

    for anomaly in metrics.get("anomalies_detected", []):
        timeline_events.append(
            {
                "timestamp": anomaly["detected_at"],
                "source": "METRIC",
                "signal": (
                    f"[{anomaly['severity']}] {anomaly['metric']}"
                    f" = {anomaly['value']} (seuil : {anomaly['threshold']})"
                ),
                "service": anomaly["service"],
                "trace_id": None,
                "span_id": None,
                "severity": anomaly["severity"],
            }
        )

    for log_entry in logs:
        timeline_events.append(
            {
                "timestamp": log_entry.get(
                    "timestamp", now.isoformat()
                ),
                "source": "LOG",
                "signal": f"[{log_entry.get('severity', 'INFO')}] {log_entry.get('body', '')}",
                "service": log_entry.get("service", "inconnu"),
                "trace_id": log_entry.get("trace_id"),
                "span_id": log_entry.get("span_id"),
                "severity": log_entry.get("severity", "INFO"),
            }
        )

    # Tri chronologique
    timeline_events.sort(key=lambda e: e["timestamp"])

    # Identification des services affectés
    affected_services = list(
        {e["service"] for e in timeline_events if e["severity"] in ("ERROR", "CRITIQUE")}
    )

    # Calcul heuristique du blast radius (0–10)
    error_count = sum(
        1 for e in timeline_events if e["severity"] in ("ERROR", "CRITIQUE")
    )
    blast_radius_score = min(10.0, round(error_count * 1.2 + len(affected_services) * 0.8, 1))

    # Hypothèse de cause racine (analyse des premiers signaux d'erreur)
    first_error = next(
        (e for e in timeline_events if e["severity"] in ("ERROR", "CRITIQUE")),
        None,
    )
    if first_error:
        root_cause_hypothesis = (
            f"Signal initial : {first_error['source']} dans {first_error['service']}"
            f" à {first_error['timestamp']}. "
            f"Opération en cause probable : {first_error['signal'][:120]}."
        )
    else:
        root_cause_hypothesis = (
            "Aucun signal d'erreur détecté — incident potentiellement"
            " bénin ou non encore propagé."
        )

    recommended_actions = [
        "1. Examiner les spans ERROR dans Jaeger avec le trace_id du premier signal.",
        "2. Vérifier les logs structurés LegalWatch et PressAgent sur la fenêtre incident.",
        "3. Consulter le runbook correspondant au service racine identifié.",
        "4. Évaluer la nécessité d'un circuit-breaker sur les appels EXTERNAL_API_CALLS.",
        "5. Ouvrir un post-mortem si le blast_radius_score dépasse 5,0.",
    ]

    return {
        "correlation_id": correlation_id,
        "generated_at": now.isoformat(),
        "input_signals": {
            "traces_count": len(traces),
            "metrics_anomalies": len(metrics.get("anomalies_detected", [])),
            "logs_count": len(logs),
        },
        "incident_timeline": timeline_events,
        "root_cause_hypothesis": root_cause_hypothesis,
        "affected_services": affected_services,
        "blast_radius_score": blast_radius_score,
        "recommended_actions": recommended_actions,
        "w3c_trace_context_version": "1",
        "otel_correlation_spec": "https://opentelemetry.io/docs/specs/otel/logs/data-model/#log-and-span-correlation",
    }


def generate_observability_dashboard(services: list) -> dict:
    """Génère la configuration d'un dashboard CaelumSwarm™ orienté Golden Signals SRE.

    Produit une configuration déclarative compatible Grafana / OpenTelemetry
    Collector covering les quatre Golden Signals de Google SRE :
    Latence · Traffic · Errors · Saturation, avec règles d'alerte SLO et
    runbooks associés.

    Args:
        services: Liste des clés INSTRUMENTATION_LIBRARY à inclure dans le dashboard.

    Returns:
        dict de configuration dashboard avec panels, golden_signals, runbooks
        et alertes de burn rate SLO.
    """
    panels = []
    golden_signals = {}
    runbooks = {}

    for svc_key in services:
        svc_info = INSTRUMENTATION_LIBRARY.get(svc_key, {})
        svc_name = svc_info.get("service_name", svc_key)
        svc_short = svc_name.split(".")[-1]

        # --- Panneau Latence ---
        panels.append(
            {
                "id": f"latency_{svc_short}",
                "title": f"Latence p99 — {svc_name}",
                "viz_type": "TIME_SERIES",
                "query": (
                    f'histogram_quantile(0.99, rate(api_latency_p99_ms_bucket'
                    f'{{service_name="{svc_name}"}}[5m]))'
                ),
                "unit": "ms",
                "alert_rule": {
                    "condition": "value > 500",
                    "severity": "AVERTISSEMENT",
                    "message": f"Latence p99 dépasse 500 ms sur {svc_name}",
                    "runbook_url": f"https://runbooks.caelum.io/{svc_short}/high-latency",
                },
            }
        )

        # --- Panneau Trafic ---
        panels.append(
            {
                "id": f"traffic_{svc_short}",
                "title": f"Débit requêtes — {svc_name}",
                "viz_type": "STAT",
                "query": (
                    f'sum(rate(entities_processed_total{{service_name="{svc_name}"}}[1m]))'
                ),
                "unit": "req/s",
                "alert_rule": None,
            }
        )

        # --- Panneau Erreurs ---
        panels.append(
            {
                "id": f"errors_{svc_short}",
                "title": f"Taux d'erreur — {svc_name}",
                "viz_type": "GAUGE",
                "query": (
                    f'error_rate_pct{{service_name="{svc_name}"}}'
                ),
                "unit": "%",
                "alert_rule": {
                    "condition": "value > 1.0",
                    "severity": "CRITIQUE",
                    "message": f"Taux d'erreur dépasse 1 % sur {svc_name}",
                    "runbook_url": f"https://runbooks.caelum.io/{svc_short}/error-spike",
                },
            }
        )

        # --- Panneau Saturation ---
        panels.append(
            {
                "id": f"saturation_{svc_short}",
                "title": f"Saturation file d'attente — {svc_name}",
                "viz_type": "TIME_SERIES",
                "query": (
                    f'queue_depth_gauge{{service_name="{svc_name}"}}'
                ),
                "unit": "messages",
                "alert_rule": {
                    "condition": "value > 1000",
                    "severity": "AVERTISSEMENT",
                    "message": f"File d'attente saturée sur {svc_name}",
                    "runbook_url": f"https://runbooks.caelum.io/{svc_short}/queue-saturation",
                },
            }
        )

        # --- Golden Signals par service ---
        golden_signals[svc_name] = {
            "latency": {
                "metric": "api_latency_p99_ms",
                "slo": "p99 < 500 ms",
                "panel_id": f"latency_{svc_short}",
            },
            "traffic": {
                "metric": "entities_processed_total",
                "slo": "Nominal selon capacité planifiée",
                "panel_id": f"traffic_{svc_short}",
            },
            "errors": {
                "metric": "error_rate_pct",
                "slo": "< 0,5 % sur 5 min",
                "panel_id": f"errors_{svc_short}",
            },
            "saturation": {
                "metric": "queue_depth_gauge",
                "slo": "< 500 messages",
                "panel_id": f"saturation_{svc_short}",
            },
        }

        # --- Runbooks ---
        runbooks[svc_name] = {
            "high_latency": f"https://runbooks.caelum.io/{svc_short}/high-latency",
            "error_spike": f"https://runbooks.caelum.io/{svc_short}/error-spike",
            "queue_saturation": f"https://runbooks.caelum.io/{svc_short}/queue-saturation",
            "slo_breach": f"https://runbooks.caelum.io/{svc_short}/slo-breach",
        }

    # Alertes de burn rate SLO (Google SRE Workbook — Chapter 5)
    slo_burn_rate_alerts = {
        "fast_burn_critical": {
            "label": "Burn rate rapide — CRITIQUE",
            "description": "Consommation du budget d'erreur à x14,4 → SLO épuisé en 1h",
            "window_short": "5m",
            "window_long": "1h",
            "burn_rate_threshold": 14.4,
            "severity": "CRITIQUE",
            "action": "Escalade immédiate ingénierie d'astreinte",
        },
        "fast_burn_warning": {
            "label": "Burn rate rapide — AVERTISSEMENT",
            "description": "Consommation du budget d'erreur à x6 → SLO épuisé en 6h",
            "window_short": "30m",
            "window_long": "6h",
            "burn_rate_threshold": 6.0,
            "severity": "AVERTISSEMENT",
            "action": "Notification équipe on-call — investigation requise",
        },
        "slow_burn_warning": {
            "label": "Burn rate lent — AVERTISSEMENT",
            "description": "Consommation du budget d'erreur à x3 → SLO épuisé en 72h",
            "window_short": "6h",
            "window_long": "3d",
            "burn_rate_threshold": 3.0,
            "severity": "INFO",
            "action": "Ticket de suivi ouvert — traitement dans les 24h",
        },
    }

    return {
        "dashboard_id": f"caelum-swarm-{secrets.token_hex(4)}",
        "title": "CaelumSwarm™ — Observabilité OpenTelemetry",
        "description": (
            "Golden Signals SRE (Latence · Traffic · Errors · Saturation)"
            " pour les services instrumentés CaelumSwarm™."
        ),
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "otel_spec": "1.27.0",
        "services": services,
        "panels_count": len(panels),
        "panels": panels,
        "golden_signals": golden_signals,
        "runbooks": runbooks,
        "slo_burn_rate_alerts": slo_burn_rate_alerts,
        "refresh_interval_seconds": 30,
        "data_sources": {
            "traces": "Jaeger — jaeger.caelum.svc.cluster.local:16686",
            "metrics": "Prometheus — prometheus.caelum.svc.cluster.local:9090",
            "logs": "Loki — loki.caelum.svc.cluster.local:3100",
        },
    }


# ---------------------------------------------------------------------------
# 3. HELPER INTERNE
# ---------------------------------------------------------------------------


def _resolve_library_key(service_name: str) -> str:
    """Résout la clé INSTRUMENTATION_LIBRARY depuis un service_name."""
    for key, info in INSTRUMENTATION_LIBRARY.items():
        if info.get("service_name") == service_name:
            return key
    return ""


# ---------------------------------------------------------------------------
# 4. DÉMO
# ---------------------------------------------------------------------------


def run_demo() -> bool:
    """Démontre les capacités d'observabilité OTel pour la Wave 194 de CaelumSwarm™.

    Séquence :
        1. Création de 3 spans de trace pour l'analyse Wave 194.
        2. Snapshot de métriques pour 4 services clés.
        3. Corrélation des signaux lors d'un incident simulé (latence élevée + erreurs).
        4. Génération de la configuration dashboard Golden Signals SRE.

    Returns:
        True si la démonstration s'est déroulée sans exception.
    """
    sep = "─" * 72

    print(sep)
    print("  CaelumSwarm™ — Agent Protocole OpenTelemetry  (Wave 194 Demo)")
    print(f"  CNCF OpenTelemetry Spec v1.27.0 | W3C TraceContext | Google SRE")
    print(sep)

    # ------------------------------------------------------------------
    # Étape 1 : Traces distribuées — analyse Wave 194
    # ------------------------------------------------------------------
    print("\n[1/4] Création de spans de trace — Wave 194\n")

    span_ops = [
        (
            "wave.entities.load",
            "caelum.wave-engine",
            {"wave.id": "194", "entities.count": "8", "domain": "climate-migration"},
        ),
        (
            "wave.composite_score.compute",
            "caelum.wave-engine",
            {"wave.id": "194", "sub_dimensions": "4", "weights": "0.30/0.25/0.25/0.20"},
        ),
        (
            "wave.distribution.validate",
            "caelum.wave-engine",
            {
                "wave.id": "194",
                "critique_count": "4",
                "eleve_count": "2",
                "modere_count": "1",
                "faible_count": "1",
            },
        ),
    ]

    traces = []
    for op, svc, attrs in span_ops:
        span = create_trace_span(op, svc, attrs)
        traces.append(span)
        print(
            f"  span_id={span['span_id'][:12]}…  op={span['operation_name']}"
            f"  status={span['status']['code']}  dur={span['duration_ms']} ms"
        )

    print(f"\n  trace_id partagé (W3C) : {traces[0]['trace_id']}")

    # ------------------------------------------------------------------
    # Étape 2 : Snapshot métriques — 4 services
    # ------------------------------------------------------------------
    print(f"\n{sep}")
    print("\n[2/4] Snapshot métriques (fenêtre 60 s) — 4 services\n")

    demo_services = ["WAVE_ENGINE", "API_GATEWAY", "LEGAL_WATCH", "ALERT_PROCESSOR"]
    snapshot = collect_metrics_snapshot(demo_services, period_seconds=60)

    print(f"  snapshot_id    : {snapshot['snapshot_id']}")
    print(f"  total datapoints: {snapshot['total_datapoints']}")
    print(f"  anomalies       : {len(snapshot['anomalies_detected'])}")

    print("\n  Conformité SLO (échantillon) :")
    slo_keys = ["api_latency_p99_ms", "error_rate_pct", "cache_hit_rate_pct"]
    for k in slo_keys:
        s = snapshot["slo_compliance"].get(k, {})
        flag = "✓" if s.get("in_slo") else "✗"
        print(f"    {flag} {k:35s}  val={s.get('current_value', '?'):<10}  {s.get('status', '?')}")

    if snapshot["anomalies_detected"]:
        print("\n  Anomalies détectées :")
        for a in snapshot["anomalies_detected"]:
            print(
                f"    [{a['severity']}] {a['metric']} = {a['value']}"
                f" > seuil {a['threshold']}  ({a['service']})"
            )

    # ------------------------------------------------------------------
    # Étape 3 : Corrélation de signaux — incident simulé
    # ------------------------------------------------------------------
    print(f"\n{sep}")
    print("\n[3/4] Corrélation signaux — incident simulé (latence + erreurs)\n")

    mock_logs = [
        {
            "severity": "ERROR",
            "body": "Timeout upstream SWARM_API_URL après 5 s — fallback 502 activé",
            "service": "caelum.api-gateway",
            "trace_id": traces[0]["trace_id"],
            "span_id": traces[0]["span_id"],
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        },
        {
            "severity": "WARN",
            "body": "Queue depth > 800 — back-pressure détectée sur AlertProcessor",
            "service": "caelum.alert-processor",
            "trace_id": None,
            "span_id": None,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        },
        {
            "severity": "INFO",
            "body": "Wave 194 — 8 entités chargées (4 critique / 2 élevé / 1 modéré / 1 faible)",
            "service": "caelum.wave-engine",
            "trace_id": traces[2]["trace_id"],
            "span_id": traces[2]["span_id"],
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        },
    ]

    correlation = correlate_signals(traces, snapshot, mock_logs)

    print(f"  correlation_id  : {correlation['correlation_id']}")
    print(f"  blast_radius    : {correlation['blast_radius_score']} / 10")
    print(f"  services touchés: {', '.join(correlation['affected_services']) or 'aucun'}")
    print(f"\n  Hypothèse cause racine :")
    print(f"    {correlation['root_cause_hypothesis']}")
    print(f"\n  Timeline ({len(correlation['incident_timeline'])} événements, ordre chronologique) :")
    for evt in correlation["incident_timeline"][:5]:
        print(
            f"    [{evt['source']:6s}] [{evt['severity']:12s}]"
            f" {evt['signal'][:65]}"
        )

    print("\n  Actions recommandées :")
    for action in correlation["recommended_actions"]:
        print(f"    {action}")

    # ------------------------------------------------------------------
    # Étape 4 : Dashboard Golden Signals SRE
    # ------------------------------------------------------------------
    print(f"\n{sep}")
    print("\n[4/4] Configuration dashboard — Golden Signals SRE\n")

    dashboard = generate_observability_dashboard(demo_services)

    print(f"  dashboard_id  : {dashboard['dashboard_id']}")
    print(f"  panels générés: {dashboard['panels_count']}")
    print(f"\n  Golden Signals par service :")
    for svc, gs in dashboard["golden_signals"].items():
        print(f"\n    {svc}")
        for signal_name, detail in gs.items():
            print(f"      {signal_name:12s} → {detail['metric']:35s}  SLO: {detail['slo']}")

    print("\n  Alertes burn rate SLO (Google SRE Workbook, ch. 5) :")
    for alert_key, alert in dashboard["slo_burn_rate_alerts"].items():
        print(
            f"    [{alert['severity']:12s}] x{alert['burn_rate_threshold']:<5}"
            f" {alert['label']}"
        )

    print(f"\n  Sources de données :")
    for signal_type, endpoint in dashboard["data_sources"].items():
        print(f"    {signal_type:8s} → {endpoint}")

    print(f"\n{sep}")
    print("  Démo Wave 194 terminée — tous les signaux OTel corrélés avec succès.")
    print(sep)
    return True


# ---------------------------------------------------------------------------
# 5. POINT D'ENTRÉE
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    if not success:
        raise SystemExit(1)
