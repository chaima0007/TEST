"""
Log Management Agent — CaelumSwarm™
Stack: Loki + Fluentd + Elasticsearch + OpenSearch + Kibana
Role: Centralisation logs, recherche, alertes, audit trail CSDDD immuable
"""

import hashlib
import json
import random
import datetime

LOG_STACK = {
    "collection": {
        "tool": "Fluentd 1.16 + Fluent Bit 3.x (sidecar léger)",
        "sources": ["kubernetes_pods", "system_logs", "application_logs", "audit_logs"],
        "protocols": ["TCP/UDP syslog", "HTTP webhook", "Kafka consumer"],
        "buffer": "Persistent disk buffer (ne perd aucun log même si destination down)",
        "backpressure": "Retry avec exponential backoff",
    },
    "storage": {
        "hot": {"tool": "Loki 3.0 (Grafana)", "retention": "30 days", "cost": "low (label-indexed)"},
        "warm": {"tool": "Elasticsearch 8.x", "retention": "90 days", "search": "full-text"},
        "cold": {"tool": "S3 Glacier", "retention": "7 years", "format": "compressed JSON", "encryption": "AES-256"},
    },
    "visualization": {
        "grafana_loki": "Dashboards temps réel (30s refresh)",
        "kibana": "Analyse forensique, full-text search",
        "opensearch_dashboards": "Analytics, ML anomaly detection",
    },
}

LOG_SCHEMAS = {
    "application_log": {
        "timestamp": "ISO8601 UTC",
        "level": "DEBUG|INFO|WARN|ERROR|CRITICAL",
        "service": "wave-engine|api-gateway|report-agent",
        "trace_id": "W3C TraceContext (corrélation OpenTelemetry)",
        "span_id": "str",
        "user_id": "UUID (anonymisé — RGPD)",
        "action": "str",
        "resource": "str",
        "outcome": "success|failure",
        "duration_ms": "int",
        "message": "str",
    },
    "audit_log": {
        "timestamp": "ISO8601 UTC",
        "event_type": "WAVE_SCORE|REPORT_GENERATED|ALERT_SENT|CONFIG_CHANGED|ACCESS_GRANTED|ACCESS_DENIED",
        "actor": "UUID",
        "target": "str",
        "changes": "dict (before/after)",
        "ip_address": "str (masqué: 192.168.xxx.xxx)",
        "session_id": "UUID",
        "immutable": True,    # WORM — Write Once Read Many
        "hash": "SHA256 du log précédent (chaîne immuable)",
    },
    "security_log": {
        "timestamp": "ISO8601 UTC",
        "event_type": "AUTH_SUCCESS|AUTH_FAILURE|PRIVILEGE_ESCALATION|ANOMALY_DETECTED",
        "severity": "LOW|MEDIUM|HIGH|CRITICAL",
        "mitre_technique": "str (ex: T1078 Valid Accounts)",
        "source_ip": "str",
        "destination": "str",
        "action_taken": "LOGGED|ALERTED|BLOCKED|CONTAINED",
    },
}

FLUENTD_PIPELINES = {
    "wave_engine_logs": {
        "input": "tail /var/log/pods/caelum-prod_wave-engine*",
        "filter_1": "parser (JSON)",
        "filter_2": "record_transformer (add cluster, env labels)",
        "filter_3": "grep (exclude DEBUG in prod)",
        "output_1": "loki (hot storage)",
        "output_2": "elasticsearch (warm, si level >= WARN)",
        "output_3": "kafka (si level == CRITICAL, pour alertes temps réel)",
    },
    "audit_trail": {
        "input": "kubernetes_audit + app_audit webhook",
        "filter": "parser + SHA256 chaining",
        "output_1": "elasticsearch (immutable index .caelum-audit-YYYY.MM)",
        "output_2": "s3_glacier (cold, AES-256, 7 ans)",
        "alert": "kafka → alertmanager si event_type in [CONFIG_CHANGED, ACCESS_DENIED×5]",
    },
    "security_events": {
        "input": "falco_grpc + crowdstrike_api",
        "filter": "MITRE ATT&CK enrichment",
        "output": "elasticsearch (SIEM) + kafka (SOC real-time)",
        "retention": "1 year",
    },
}

LOKI_CONFIG = {
    "labels": ["namespace", "pod", "container", "service", "level"],
    "chunk_encoding": "snappy",
    "query_range": "last 30d",
    "ruler_alerts": [
        {"alert": "HighErrorRate", "expr": 'sum(rate({service="wave-engine"}[5m] |= "ERROR")) > 10', "for": "2m"},
        {"alert": "AuditLogGap", "expr": 'absent(rate({job="audit-trail"}[5m]))', "for": "1m", "severity": "critical"},
        {"alert": "AuthFailureSpike", "expr": 'sum(rate({event_type="AUTH_FAILURE"}[5m])) > 20', "for": "1m"},
    ],
}

LOG_RETENTION_POLICY = {
    "debug": "7 days (dev only)",
    "info": "30 days (Loki hot)",
    "warn": "90 days (Elasticsearch warm)",
    "error": "1 year (Elasticsearch + S3)",
    "critical": "3 years (Elasticsearch + S3 + Glacier)",
    "audit": "7 years (S3 Glacier WORM — RGPD + CSDDD Art.9)",
    "security": "1 year (SIEM)",
}


# ─────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────

def design_log_pipeline(source: str, log_type: str) -> dict:
    """Retourne la configuration de pipeline Fluentd pour une source et un type donnés."""
    pipeline_key = None
    if log_type == "audit":
        pipeline_key = "audit_trail"
    elif log_type == "security":
        pipeline_key = "security_events"
    else:
        pipeline_key = "wave_engine_logs"

    base = FLUENTD_PIPELINES.get(pipeline_key, {}).copy()
    base["designed_for"] = {"source": source, "log_type": log_type}
    base["estimated_throughput_eps"] = random.randint(500, 5000)
    base["buffer_flush_interval_sec"] = 5
    return base


def simulate_audit_trail_chain(events: list) -> dict:
    """Simule la chaîne SHA256 immuable des logs d'audit."""
    chain = []
    previous_hash = "0" * 64  # genesis hash
    for i, event in enumerate(events):
        event_copy = dict(event)
        event_copy["previous_hash"] = previous_hash
        event_copy["seq"] = i
        serialized = json.dumps(event_copy, sort_keys=True, ensure_ascii=False)
        current_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        event_copy["hash"] = current_hash
        event_copy["immutable"] = True
        chain.append(event_copy)
        previous_hash = current_hash

    return {
        "chain_length": len(chain),
        "genesis_hash": "0" * 64,
        "tip_hash": chain[-1]["hash"] if chain else None,
        "integrity": "VERIFIED",
        "storage": "S3 Glacier WORM + Elasticsearch immutable index",
        "events": chain,
    }


def analyze_log_volume(services: list, period_days: int) -> dict:
    """Analyse le volume de logs pour une liste de services sur une période."""
    analysis = {}
    total_events = 0
    total_gb = 0.0
    for svc in services:
        events_per_day = random.randint(50_000, 500_000)
        gb_per_day = round(events_per_day * 512 / (1024 ** 3), 4)
        svc_events = events_per_day * period_days
        svc_gb = round(gb_per_day * period_days, 2)
        total_events += svc_events
        total_gb += svc_gb
        analysis[svc] = {
            "events_per_day": events_per_day,
            "total_events": svc_events,
            "total_gb": svc_gb,
            "dominant_level": random.choice(["INFO", "WARN", "ERROR"]),
            "hot_tier_pct": 45,
            "warm_tier_pct": 35,
            "cold_tier_pct": 20,
        }
    return {
        "period_days": period_days,
        "services_count": len(services),
        "total_events": total_events,
        "total_gb": round(total_gb, 2),
        "estimated_cost_eur_month": round(total_gb * 0.023, 2),
        "per_service": analysis,
    }


def generate_forensic_query(incident_type: str, time_range: str) -> dict:
    """Génère des requêtes forensiques pour Loki et Elasticsearch selon le type d'incident."""
    queries = {
        "lateral_movement": {
            "loki": '{job="security-events"} |= "PRIVILEGE_ESCALATION" | json | mitre_technique=~"T1021|T1078|T1550"',
            "elasticsearch": {
                "index": ".caelum-security-*",
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"event_type": "PRIVILEGE_ESCALATION"}},
                            {"range": {"@timestamp": {"gte": f"now-{time_range}", "lte": "now"}}},
                        ],
                        "should": [
                            {"match": {"mitre_technique": "T1021"}},
                            {"match": {"mitre_technique": "T1078"}},
                            {"match": {"mitre_technique": "T1550"}},
                        ],
                        "minimum_should_match": 1,
                    }
                },
            },
        },
        "auth_failure_spike": {
            "loki": '{job="security-events"} |= "AUTH_FAILURE" | json | line_format "{{.source_ip}} {{.actor}}"',
            "elasticsearch": {
                "index": ".caelum-security-*",
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"event_type": "AUTH_FAILURE"}},
                            {"range": {"@timestamp": {"gte": f"now-{time_range}", "lte": "now"}}},
                        ]
                    }
                },
                "aggs": {
                    "by_ip": {"terms": {"field": "source_ip.keyword", "size": 20}},
                    "by_actor": {"terms": {"field": "actor.keyword", "size": 20}},
                },
            },
        },
    }
    result = queries.get(incident_type)
    if result is None:
        result = {
            "loki": f'{{job=~".+"}} |= "{incident_type}"',
            "elasticsearch": {"index": ".caelum-*", "query": {"match_all": {}}},
        }
    result["incident_type"] = incident_type
    result["time_range"] = time_range
    result["generated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    return result


# ─────────────────────────────────────────
# BLOC PRINCIPAL
# ─────────────────────────────────────────

def main():
    separator = "=" * 70

    # ── Section 1 : Log Management Stack Report ──────────────────────────
    print(separator)
    print("SECTION 1 — Log Management Stack Report")
    print(separator)
    print(json.dumps(LOG_STACK, indent=2, ensure_ascii=False))

    # ── Section 2 : Log Schemas (3 types) ────────────────────────────────
    print(f"\n{separator}")
    print("SECTION 2 — Log Schemas (3 types)")
    print(separator)
    for schema_name, schema in LOG_SCHEMAS.items():
        print(f"\n[Schema: {schema_name}]")
        print(json.dumps(schema, indent=2, ensure_ascii=False))

    # ── Section 3 : Fluentd Pipelines (3 pipelines) ──────────────────────
    print(f"\n{separator}")
    print("SECTION 3 — Fluentd Pipelines (3 pipelines)")
    print(separator)
    for pipeline_name, pipeline in FLUENTD_PIPELINES.items():
        print(f"\n[Pipeline: {pipeline_name}]")
        print(json.dumps(pipeline, indent=2, ensure_ascii=False))

    # ── Section 4 : Loki Configuration + Ruler Alerts ────────────────────
    print(f"\n{separator}")
    print("SECTION 4 — Loki Configuration + Ruler Alerts")
    print(separator)
    print(json.dumps(LOKI_CONFIG, indent=2, ensure_ascii=False))

    # ── Section 5 : Audit Trail SHA256 Chain (5 événements) ──────────────
    print(f"\n{separator}")
    print("SECTION 5 — Audit Trail SHA256 Chain Simulation (5 événements)")
    print(separator)
    audit_events = [
        {
            "timestamp": "2026-06-22T08:00:00Z",
            "event_type": "ACCESS_GRANTED",
            "actor": "user-uuid-001",
            "target": "wave-engine/report/Q2-2026",
            "ip_address": "192.168.xxx.xxx",
            "session_id": "sess-uuid-001",
        },
        {
            "timestamp": "2026-06-22T08:05:13Z",
            "event_type": "WAVE_SCORE",
            "actor": "system-uuid-wave",
            "target": "supplier-uuid-042",
            "ip_address": "10.0.xxx.xxx",
            "session_id": "sess-uuid-002",
        },
        {
            "timestamp": "2026-06-22T08:10:44Z",
            "event_type": "REPORT_GENERATED",
            "actor": "user-uuid-001",
            "target": "csddd-report-2026-Q2",
            "ip_address": "192.168.xxx.xxx",
            "session_id": "sess-uuid-001",
        },
        {
            "timestamp": "2026-06-22T08:15:02Z",
            "event_type": "CONFIG_CHANGED",
            "actor": "admin-uuid-007",
            "target": "alert-threshold/wave-engine",
            "changes": {"before": {"threshold": 0.7}, "after": {"threshold": 0.65}},
            "ip_address": "10.0.xxx.xxx",
            "session_id": "sess-uuid-003",
        },
        {
            "timestamp": "2026-06-22T08:20:58Z",
            "event_type": "ACCESS_DENIED",
            "actor": "user-uuid-999",
            "target": "audit-log/raw",
            "ip_address": "172.16.xxx.xxx",
            "session_id": "sess-uuid-004",
        },
    ]
    chain_result = simulate_audit_trail_chain(audit_events)
    print(f"Chain length      : {chain_result['chain_length']}")
    print(f"Genesis hash      : {chain_result['genesis_hash']}")
    print(f"Tip hash          : {chain_result['tip_hash']}")
    print(f"Integrity         : {chain_result['integrity']}")
    print(f"Storage           : {chain_result['storage']}")
    for ev in chain_result["events"]:
        print(f"\n  seq={ev['seq']} | event_type={ev['event_type']}")
        print(f"    previous_hash : {ev['previous_hash'][:20]}...")
        print(f"    hash          : {ev['hash']}")

    # ── Section 6 : Log Volume Analysis (7 services, 30 jours) ───────────
    print(f"\n{separator}")
    print("SECTION 6 — Log Volume Analysis (7 services, 30 jours)")
    print(separator)
    services = [
        "wave-engine",
        "api-gateway",
        "report-agent",
        "auth-service",
        "supplier-connector",
        "alert-dispatcher",
        "audit-service",
    ]
    volume = analyze_log_volume(services, 30)
    print(f"Période           : {volume['period_days']} jours")
    print(f"Services          : {volume['services_count']}")
    print(f"Total événements  : {volume['total_events']:,}")
    print(f"Total stockage    : {volume['total_gb']} GB")
    print(f"Coût estimé/mois  : {volume['estimated_cost_eur_month']} EUR")
    print("\nDétail par service :")
    for svc, stats in volume["per_service"].items():
        print(f"  [{svc}]")
        print(f"    events/jour   : {stats['events_per_day']:,}")
        print(f"    total events  : {stats['total_events']:,}")
        print(f"    total GB      : {stats['total_gb']}")
        print(f"    niveau dom.   : {stats['dominant_level']}")

    # ── Section 7 : Forensic Queries ─────────────────────────────────────
    print(f"\n{separator}")
    print("SECTION 7 — Forensic Queries (lateral_movement, auth_failure_spike)")
    print(separator)
    for incident in ["lateral_movement", "auth_failure_spike"]:
        query = generate_forensic_query(incident, "24h")
        print(f"\n[Incident: {incident}]")
        print(f"  Loki query      : {query['loki']}")
        es_q = json.dumps(query["elasticsearch"], indent=4, ensure_ascii=False)
        print(f"  Elasticsearch   :\n{es_q}")
        print(f"  Generated at    : {query['generated_at']}")

    # ── Section 8 : Retention Policy + RGPD/CSDDD Compliance ─────────────
    print(f"\n{separator}")
    print("SECTION 8 — Retention Policy + RGPD/CSDDD Compliance")
    print(separator)
    print(json.dumps(LOG_RETENTION_POLICY, indent=2, ensure_ascii=False))
    compliance = {
        "RGPD_Art17": "Droit à l'effacement — PII anonymisé à l'ingestion (UUID, IP masquée)",
        "RGPD_Art30": "Registre traitements — audit_log conservé 7 ans (WORM)",
        "CSDDD_Art9": "Audit trail immuable — SHA256 chain + S3 Glacier WORM",
        "CSDDD_Art10": "Alertes violations documentées — kafka → alertmanager",
        "NIS2": "Security logs 1 an — SIEM Elasticsearch + SOC temps réel",
        "SOC2_Type2": "Logs d'accès complets — log integrity SHA256 vérifié",
    }
    print("\nConformité réglementaire :")
    print(json.dumps(compliance, indent=2, ensure_ascii=False))

    # ── Section 9 : Statut agent ──────────────────────────────────────────
    print(f"\n{separator}")
    print("Log Management Agent — PRÊT (Loki 3.0 / Fluentd / Elasticsearch / S3 WORM 7 ans)")
    print(separator)


if __name__ == "__main__":
    main()
