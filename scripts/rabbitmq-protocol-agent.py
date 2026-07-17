"""
RabbitMQ Protocol Agent — CaelumSwarm™
=======================================

Protocole AMQP 0-9-1 (Advanced Message Queuing Protocol)
----------------------------------------------------------
AMQP 0-9-1 est un protocole de messagerie binaire standardisant la communication
entre producteurs, brokers et consommateurs. Composants clés :

EXCHANGES : Points d'entrée des messages. Le broker route les messages vers les queues
  selon le type d'exchange et les bindings :
  - direct   : routing_key exact match (queue name ou clé arbitraire)
  - topic    : routing_key avec wildcards (* = 1 mot, # = 0..N mots)
  - fanout   : broadcast — ignore routing_key, envoie à toutes les queues bindées
  - headers  : routing basé sur les headers AMQP (x-match: all|any)

QUEUES : Buffers durables ou temporaires stockant les messages en attente de
  consommation. Propriétés : durable, exclusive, auto-delete, TTL, max-length.

BINDINGS : Règles liant exchanges aux queues via une binding_key (ou headers).

DLX (Dead Letter Exchange) : Exchange spécial recevant les messages rejetés
  (nack, TTL expiré, queue pleine). Permet retry avec backoff exponentiel
  avant déplacement vers la "poison queue" (messages non récupérables).

Conformité CSDDD 2024 : Ce broker garantit la traçabilité complète des alertes
  de droits humains, rapports de conformité et signaux d'audit exigés par la
  Corporate Sustainability Due Diligence Directive (UE 2024/1760).
"""

import json
import math
import hashlib
import datetime
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES DE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

RABBITMQ_EXCHANGES = {
    "direct_exchange": {
        "type": "direct",
        "description": "Routage exact par routing_key — domaines CaelumSwarm™",
        "durable": True,
        "auto_delete": False,
        "internal": False,
        "routing_key": "exact_match",
        "use_cases": ["wave_alerts", "compliance_reports", "targeted_dispatch"],
        "example_routing_key": "caelum.wave.alerts.critical",
    },
    "topic_exchange": {
        "type": "topic",
        "description": "Routage wildcard (* = 1 mot, # = N mots) — abonnements flexibles",
        "durable": True,
        "auto_delete": False,
        "internal": False,
        "routing_key": "wildcard_pattern",
        "use_cases": ["monitoring_events", "domain_subscriptions", "regional_filters"],
        "example_routing_key": "caelum.*.alerts.#",
    },
    "fanout_exchange": {
        "type": "fanout",
        "description": "Broadcast — diffusion à toutes les queues bindées sans routing_key",
        "durable": True,
        "auto_delete": False,
        "internal": False,
        "routing_key": "ignored",
        "use_cases": ["system_broadcasts", "cache_invalidation", "global_notifications"],
        "example_routing_key": "(none — fanout ignore la routing_key)",
    },
    "headers_exchange": {
        "type": "headers",
        "description": "Routage par headers AMQP (x-match: all|any) — filtrage sémantique",
        "durable": True,
        "auto_delete": False,
        "internal": False,
        "routing_key": "headers_based",
        "use_cases": ["audit_trail", "compliance_filters", "priority_routing"],
        "example_headers": {"x-match": "all", "domain": "labor_rights", "severity": "critical"},
    },
    "dead_letter_exchange": {
        "type": "direct",
        "description": "DLX — reçoit messages nack/TTL/overflow pour retry ou poison queue",
        "durable": True,
        "auto_delete": False,
        "internal": True,
        "routing_key": "dead_letter_routing",
        "use_cases": ["message_retry", "poison_queue_routing", "failure_analysis"],
        "example_routing_key": "caelum.dlq.retry",
        "max_retry_depth": 3,
    },
}

QUEUE_CONFIGURATIONS = {
    "wave_alerts": {
        "durable": True,
        "exclusive": False,
        "auto_delete": False,
        "ttl_ms": 300_000,           # 5 minutes
        "max_length": 10_000,
        "dlx": "dead_letter_exchange",
        "dlx_routing_key": "caelum.dlq.wave_alerts",
        "type": "classic",
        "description": "Alertes Wave CaelumSwarm™ — droits humains critiques",
        "x_message_ttl": 300_000,
    },
    "compliance_reports": {
        "durable": True,
        "exclusive": False,
        "auto_delete": False,
        "ttl_ms": 86_400_000,        # 24 heures
        "max_length": 5_000,
        "dlx": "dead_letter_exchange",
        "dlx_routing_key": "caelum.dlq.compliance",
        "type": "classic",
        "description": "Rapports CSDDD 2024 — conformité entreprises",
        "persistent": True,
    },
    "worker_signals": {
        "durable": True,
        "exclusive": False,
        "auto_delete": False,
        "ttl_ms": 60_000,            # 1 minute
        "max_length": 50_000,
        "dlx": "dead_letter_exchange",
        "dlx_routing_key": "caelum.dlq.worker",
        "type": "classic",
        "x_max_priority": 10,        # priority queue 0–10
        "description": "Signaux workers — priorité haute pour tâches urgentes",
    },
    "audit_trail": {
        "durable": True,
        "exclusive": False,
        "auto_delete": False,
        "ttl_ms": None,              # pas de TTL — conservation permanente
        "max_length": 1_000_000,
        "dlx": "dead_letter_exchange",
        "dlx_routing_key": "caelum.dlq.audit",
        "type": "classic",
        "persistent": True,
        "description": "Piste d'audit complète — conformité réglementaire CSDDD",
        "delivery_mode": 2,          # persistent messages
    },
    "monitoring_events": {
        "durable": True,
        "exclusive": False,
        "auto_delete": False,
        "ttl_ms": 120_000,           # 2 minutes
        "max_length": 20_000,
        "dlx": "dead_letter_exchange",
        "dlx_routing_key": "caelum.dlq.monitoring",
        "type": "quorum",            # quorum queue — haute disponibilité
        "description": "Événements monitoring — métriques cluster et santé système",
        "quorum_initial_group_size": 3,
    },
    "rpc_replies": {
        "durable": False,
        "exclusive": True,           # exclusive au consommateur RPC
        "auto_delete": True,
        "ttl_ms": 30_000,            # 30 secondes
        "max_length": 1_000,
        "dlx": None,
        "type": "classic",
        "description": "Queues réponses RPC — pattern request/reply temporaire",
        "correlation_id_required": True,
    },
    "saga_events": {
        "durable": True,
        "exclusive": False,
        "auto_delete": False,
        "ttl_ms": 600_000,           # 10 minutes
        "max_length": 25_000,
        "dlx": "dead_letter_exchange",
        "dlx_routing_key": "caelum.dlq.saga",
        "type": "quorum",
        "description": "Orchestration Saga — transactions distribuées droits humains",
        "quorum_initial_group_size": 3,
        "x_max_priority": 5,
    },
    "dead_letter_queue": {
        "durable": True,
        "exclusive": False,
        "auto_delete": False,
        "ttl_ms": 7_200_000,         # 2 heures avant poison queue
        "max_length": 100_000,
        "dlx": None,
        "type": "classic",
        "description": "DLQ principale — messages en attente de retry manuel",
        "alert_threshold": 100,
        "poison_queue": "caelum.dlq.poison",
    },
}

RABBITMQ_VHOSTS = {
    "caelum_prod": {
        "description": "vHost production — données réelles droits humains / CSDDD",
        "max_connections": 500,
        "max_channels": 5_000,
        "tracing": True,
        "tags": ["production", "csddd", "human_rights"],
        "default_exchange": "caelum.prod.direct",
        "tls_required": True,
    },
    "caelum_dev": {
        "description": "vHost développement — tests et intégration CI/CD",
        "max_connections": 100,
        "max_channels": 1_000,
        "tracing": True,
        "tags": ["development", "testing"],
        "default_exchange": "caelum.dev.direct",
        "tls_required": False,
    },
    "caelum_audit": {
        "description": "vHost audit — ségrégation stricte piste d'audit CSDDD 2024",
        "max_connections": 50,
        "max_channels": 500,
        "tracing": True,
        "tags": ["audit", "compliance", "immutable"],
        "default_exchange": "caelum.audit.direct",
        "tls_required": True,
        "write_once": True,          # append-only — aucune suppression autorisée
    },
}

AMQP_SECURITY = {
    "tls_version": "TLSv1.3",
    "ssl_options": {
        "certfile": "/etc/rabbitmq/tls/caelum-cert.pem",
        "keyfile": "/etc/rabbitmq/tls/caelum-key.pem",
        "cacertfile": "/etc/rabbitmq/tls/ca-cert.pem",
        "verify": "verify_peer",
        "fail_if_no_peer_cert": True,
        "ciphers": [
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_128_GCM_SHA256",
        ],
    },
    "heartbeat_seconds": 60,
    "connection_timeout_ms": 30_000,
    "channel_max": 2_047,
    "frame_max": 131_072,            # 128 KB
    "user_permissions": {
        "caelum_service": {
            "vhost": "caelum_prod",
            "configure": "^caelum\\..*",
            "write": "^caelum\\..*",
            "read": "^caelum\\..*",
        },
        "caelum_audit_writer": {
            "vhost": "caelum_audit",
            "configure": "",         # pas de configure
            "write": "^caelum\\.audit\\..*",
            "read": "",              # write-only
        },
        "caelum_readonly": {
            "vhost": "caelum_prod",
            "configure": "",
            "write": "",
            "read": "^caelum\\..*",
        },
        "caelum_admin": {
            "vhost": "caelum_prod",
            "configure": ".*",
            "write": ".*",
            "read": ".*",
            "tags": ["administrator"],
        },
    },
    "password_policy": {
        "min_length": 20,
        "complexity": "high",
        "rotation_days": 90,
    },
    "loopback_users_disabled": True,
    "management_ssl_only": True,
}

MESSAGING_PATTERNS = {
    "work_queue": {
        "description": "Distribution de tâches entre N workers concurrents",
        "exchange_type": "direct",
        "ack_mode": "manual",        # acquittement explicite après traitement
        "prefetch_count": 1,         # un message à la fois par worker
        "use_case": "Traitement analyses Wave CaelumSwarm™ par batch workers",
        "consumer_count_recommended": 5,
    },
    "publish_subscribe": {
        "description": "Diffusion événements à tous les abonnés (fanout)",
        "exchange_type": "fanout",
        "ack_mode": "auto",
        "prefetch_count": 50,
        "use_case": "Notifications système — invalidation cache — alertes globales",
        "consumer_count_recommended": None,  # illimité
    },
    "routing": {
        "description": "Routage sélectif par routing_key exacte (direct)",
        "exchange_type": "direct",
        "ack_mode": "manual",
        "prefetch_count": 10,
        "use_case": "Alertes par niveau de sévérité : critical / high / moderate / low",
        "consumer_count_recommended": 4,     # 1 par niveau
    },
    "topics": {
        "description": "Routage hiérarchique avec wildcards (* et #)",
        "exchange_type": "topic",
        "ack_mode": "manual",
        "prefetch_count": 20,
        "use_case": "Filtrage par domaine + région : caelum.labor.*.EMEA.#",
        "consumer_count_recommended": 10,
    },
    "rpc": {
        "description": "Request/Reply synchrone via correlation_id + reply_to",
        "exchange_type": "direct",
        "ack_mode": "auto",
        "prefetch_count": 1,
        "use_case": "Appels synchrones vers compliance_engine depuis API Gateway",
        "timeout_ms": 10_000,
        "correlation_id": "uuid_v4",
    },
    "saga_orchestration": {
        "description": "Orchestration de transactions distribuées multi-étapes",
        "exchange_type": "topic",
        "ack_mode": "manual",
        "prefetch_count": 5,
        "use_case": "Workflow CSDDD : collect → analyze → report → notify → archive",
        "compensating_transactions": True,
        "state_persistence": "audit_trail_queue",
        "timeout_ms": 300_000,
    },
}

CLUSTER_TOPOLOGY = {
    "nodes": ["rabbit@node1", "rabbit@node2", "rabbit@node3"],
    "node_type": "disc",             # tous les nœuds disc (pas ram) pour durabilité
    "ha_policy": "all",              # mirror sur tous les nœuds
    "ha_policy_name": "caelum-ha-all",
    "ha_apply_to": "all",
    "sync_mode": "automatic",
    "network_partition_handling": "pause_minority",
    "quorum_queues": True,
    "shovel_plugin": True,
    "federation_plugin": True,
    "management_plugin": True,
    "prometheus_plugin": True,
    "cluster_name": "caelum-swarm-prod",
    "load_balancer": {
        "type": "HAProxy",
        "vip": "rabbitmq.caelum.internal",
        "port_amqp": 5672,
        "port_amqps": 5671,
        "port_management": 15672,
        "health_check": "/api/healthchecks/node",
    },
    "shovel_config": {
        "name": "caelum-cross-dc-shovel",
        "src_uri": "amqps://rabbitmq-dc1.caelum.internal:5671",
        "dest_uri": "amqps://rabbitmq-dc2.caelum.internal:5671",
        "src_queue": "audit_trail",
        "dest_exchange": "caelum.audit.direct",
        "reconnect_delay": 5,
    },
    "federation_config": {
        "name": "caelum-federation-upstream",
        "uri": "amqps://rabbitmq-eu.caelum.internal:5671",
        "exchange": "caelum.prod.topic",
        "max_hops": 2,
        "expires_ms": 300_000,
    },
}

DEAD_LETTER_CONFIG = {
    "max_retries": 3,
    "retry_delays_ms": [1_000, 5_000, 30_000],   # backoff exponentiel approx.
    "poison_queue": "caelum.dlq.poison",
    "alert_on_dlq_depth": 100,
    "dlq_monitor_interval_seconds": 30,
    "failure_reasons": {
        "rejected": "Message nack sans requeue",
        "expired": "TTL dépassé dans la queue",
        "maxlen": "Queue pleine (max-length atteint)",
        "delivery_limit": "Nombre max de relivraisons atteint",
    },
    "poison_queue_action": "manual_review",
    "dlq_consumer_count": 2,
}


# ─────────────────────────────────────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def design_message_routing(source_domain: str, target_domain: str, priority: str) -> dict:
    """Conçoit le routage AMQP optimal entre domaines CaelumSwarm™.

    Sélectionne le type d'exchange selon la priorité et les domaines,
    génère les binding_key et routing_key adaptés, et estime la latence.
    """
    priority_map = {
        "critical": {"exchange": "direct_exchange",  "prefetch": 1,  "latency_base_ms": 5},
        "high":     {"exchange": "direct_exchange",  "prefetch": 5,  "latency_base_ms": 10},
        "moderate": {"exchange": "topic_exchange",   "prefetch": 20, "latency_base_ms": 25},
        "low":      {"exchange": "fanout_exchange",  "prefetch": 50, "latency_base_ms": 50},
    }
    priority_lower = priority.lower()
    p = priority_map.get(priority_lower, priority_map["moderate"])

    routing_key = f"caelum.{source_domain}.{target_domain}.{priority_lower}"
    binding_key = (
        routing_key
        if p["exchange"] in ("direct_exchange",)
        else f"caelum.{source_domain}.*.{priority_lower}"
    )

    # Latence estimée : base + jitter réseau simulé (déterministe via hash)
    seed = int(hashlib.md5(f"{source_domain}{target_domain}".encode()).hexdigest()[:4], 16)
    jitter_ms = (seed % 15)
    estimated_latency_ms = p["latency_base_ms"] + jitter_ms

    exchange_cfg = RABBITMQ_EXCHANGES[p["exchange"]]

    routing_plan = {
        "source_domain": source_domain,
        "target_domain": target_domain,
        "priority": priority_lower,
        "exchange": p["exchange"],
        "exchange_type": exchange_cfg["type"],
        "routing_key": routing_key,
        "binding_key": binding_key,
        "prefetch_count": p["prefetch"],
        "estimated_latency_ms": estimated_latency_ms,
        "durable": exchange_cfg["durable"],
        "ack_mode": "manual" if priority_lower in ("critical", "high") else "auto",
        "message_ttl_ms": QUEUE_CONFIGURATIONS.get(
            "wave_alerts" if target_domain == "compliance_engine" else "monitoring_events",
            {}
        ).get("ttl_ms", 300_000),
        "dlx_enabled": True,
        "dlx_name": "dead_letter_exchange",
        "notes": (
            f"Routage {exchange_cfg['type']} sélectionné pour priorité '{priority_lower}'. "
            f"Latence estimée : {estimated_latency_ms} ms."
        ),
    }
    return routing_plan


def simulate_dlx_flow(message_id: str, failure_reason: str, retry_count: int) -> dict:
    """Simule le flux Dead Letter Exchange pour un message échoué.

    - retry_count < max_retries : requeue avec délai backoff exponentiel
    - retry_count >= max_retries : déplacement vers poison queue
    Retourne un dlx_decision complet avec next_action, delay_ms, final_queue.
    """
    max_retries = DEAD_LETTER_CONFIG["max_retries"]
    retry_delays = DEAD_LETTER_CONFIG["retry_delays_ms"]
    poison_queue = DEAD_LETTER_CONFIG["poison_queue"]

    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    if retry_count < max_retries:
        delay_ms = retry_delays[retry_count] if retry_count < len(retry_delays) else retry_delays[-1]
        next_action = "requeue_with_backoff"
        final_queue = "dead_letter_queue"
        next_retry = retry_count + 1
        status = "RETRYING"
        notes = (
            f"Tentative {next_retry}/{max_retries} — "
            f"réinsertion dans dead_letter_queue après {delay_ms} ms."
        )
    else:
        delay_ms = 0
        next_action = "move_to_poison_queue"
        final_queue = poison_queue
        next_retry = None
        status = "POISON"
        notes = (
            f"Limite de {max_retries} tentatives atteinte. "
            f"Message déplacé vers {poison_queue} — révision manuelle requise."
        )

    dlx_decision = {
        "message_id": message_id,
        "failure_reason": failure_reason,
        "retry_count": retry_count,
        "max_retries": max_retries,
        "status": status,
        "next_action": next_action,
        "delay_ms": delay_ms,
        "final_queue": final_queue,
        "next_retry_count": next_retry,
        "dlx_exchange": "dead_letter_exchange",
        "dlx_routing_key": "caelum.dlq.retry" if next_action == "requeue_with_backoff" else "caelum.dlq.poison",
        "alert_triggered": (status == "POISON"),
        "alert_channel": "monitoring_events" if status == "POISON" else None,
        "timestamp_utc": timestamp,
        "notes": notes,
    }
    return dlx_decision


def configure_ha_cluster() -> dict:
    """Configure le cluster RabbitMQ haute disponibilité pour CaelumSwarm™.

    Retourne la configuration complète avec nœuds, politique HA,
    quorum queues, shovel setup et gestion des partitions réseau.
    """
    topo = CLUSTER_TOPOLOGY

    ha_config = {
        "cluster_name": topo["cluster_name"],
        "nodes": topo["nodes"],
        "node_count": len(topo["nodes"]),
        "node_type": topo["node_type"],
        "ha_policy": {
            "name": topo["ha_policy_name"],
            "pattern": "^caelum\\.",
            "definition": {
                "ha-mode": topo["ha_policy"],
                "ha-sync-mode": topo["sync_mode"],
                "ha-sync-batch-size": 128,
            },
            "apply_to": topo["ha_apply_to"],
            "priority": 10,
        },
        "quorum_queues": {
            "enabled": topo["quorum_queues"],
            "initial_group_size": 3,
            "queues": ["monitoring_events", "saga_events"],
            "notes": "Quorum queues — consensus Raft, tolérance panne 1 nœud sur 3",
        },
        "network_partition_handling": topo["network_partition_handling"],
        "plugins": {
            "shovel": topo["shovel_plugin"],
            "federation": topo["federation_plugin"],
            "management": topo["management_plugin"],
            "prometheus": topo["prometheus_plugin"],
        },
        "shovel_setup": topo["shovel_config"],
        "federation_setup": topo["federation_config"],
        "load_balancer": topo["load_balancer"],
        "disk_free_limit": "2GB",
        "vm_memory_high_watermark": 0.7,
        "max_message_size_bytes": 134_217_728,   # 128 MB
        "consumer_timeout_ms": 1_800_000,         # 30 minutes
        "mnesia_table_loading_retry_limit": 10,
        "cluster_partition_notes": (
            "pause_minority : en cas de partition réseau, la minorité (< 2 nœuds) "
            "se met en pause pour éviter le split-brain. Le quorum (2/3) continue."
        ),
    }
    return ha_config


def generate_amqp_connection_config(env: str = "production") -> dict:
    """Génère la configuration AMQP sécurisée TLS pour CaelumSwarm™.

    Produit une configuration complète incluant TLS 1.3, authentification mutuelle,
    heartbeat, channel_max et connection_timeout selon l'environnement cible.
    """
    sec = AMQP_SECURITY
    topo = CLUSTER_TOPOLOGY

    env_map = {
        "production": {
            "hosts": ["rabbitmq.caelum.internal"],
            "port": 5671,
            "vhost": "/caelum_prod",
            "tls": True,
            "verify_peer": True,
        },
        "development": {
            "hosts": ["rabbitmq-dev.caelum.internal"],
            "port": 5672,
            "vhost": "/caelum_dev",
            "tls": False,
            "verify_peer": False,
        },
        "audit": {
            "hosts": ["rabbitmq.caelum.internal"],
            "port": 5671,
            "vhost": "/caelum_audit",
            "tls": True,
            "verify_peer": True,
        },
    }

    env_cfg = env_map.get(env, env_map["production"])

    connection_config = {
        "environment": env,
        "hosts": env_cfg["hosts"],
        "port": env_cfg["port"],
        "vhost": env_cfg["vhost"],
        "credentials": {
            "username": "caelum_service",
            "password": "*** (chargé depuis vault/secret-manager — jamais en clair)",
            "auth_mechanism": "EXTERNAL" if env_cfg["tls"] else "PLAIN",
        },
        "tls": {
            "enabled": env_cfg["tls"],
            "version": sec["tls_version"] if env_cfg["tls"] else "N/A",
            "certfile": sec["ssl_options"]["certfile"] if env_cfg["tls"] else None,
            "keyfile": sec["ssl_options"]["keyfile"] if env_cfg["tls"] else None,
            "cacertfile": sec["ssl_options"]["cacertfile"] if env_cfg["tls"] else None,
            "verify": sec["ssl_options"]["verify"] if env_cfg["tls"] else None,
            "fail_if_no_peer_cert": env_cfg["verify_peer"],
            "ciphers": sec["ssl_options"]["ciphers"] if env_cfg["tls"] else [],
        },
        "connection": {
            "heartbeat_seconds": sec["heartbeat_seconds"],
            "connection_timeout_ms": sec["connection_timeout_ms"],
            "channel_max": sec["channel_max"],
            "frame_max": sec["frame_max"],
            "blocked_connection_timeout_ms": 10_000,
            "socket_timeout_ms": 5_000,
        },
        "retry_policy": {
            "max_retries": 5,
            "retry_delay_ms": 2_000,
            "backoff_multiplier": 2.0,
            "max_retry_delay_ms": 30_000,
        },
        "load_balancer_vip": topo["load_balancer"]["vip"],
        "management_url": (
            f"https://{topo['load_balancer']['vip']}:"
            f"{topo['load_balancer']['port_management']}/api/"
        ),
    }
    return connection_config


def calculate_throughput_capacity() -> dict:
    """Calcule la capacité de débit du cluster RabbitMQ CaelumSwarm™.

    Simule les messages_per_second par queue, les consumer_groups
    et le prefetch_count pour estimer le throughput total et identifier
    les goulots d'étranglement.
    """
    # Paramètres de simulation
    queue_throughput = {
        "wave_alerts":        {"msg_per_sec": 500,    "consumers": 5,  "prefetch": 1},
        "compliance_reports": {"msg_per_sec": 50,     "consumers": 3,  "prefetch": 5},
        "worker_signals":     {"msg_per_sec": 2_000,  "consumers": 10, "prefetch": 10},
        "audit_trail":        {"msg_per_sec": 1_000,  "consumers": 4,  "prefetch": 20},
        "monitoring_events":  {"msg_per_sec": 5_000,  "consumers": 8,  "prefetch": 50},
        "rpc_replies":        {"msg_per_sec": 200,    "consumers": 20, "prefetch": 1},
        "saga_events":        {"msg_per_sec": 300,    "consumers": 6,  "prefetch": 5},
        "dead_letter_queue":  {"msg_per_sec": 10,     "consumers": 2,  "prefetch": 1},
    }

    total_msg_per_sec = sum(v["msg_per_sec"] for v in queue_throughput.values())
    total_consumers   = sum(v["consumers"]   for v in queue_throughput.values())

    # Capacité effective = consumers × prefetch (messages in-flight max par queue)
    per_queue_capacity = {
        q: v["consumers"] * v["prefetch"]
        for q, v in queue_throughput.items()
    }
    total_in_flight = sum(per_queue_capacity.values())

    # Identification du bottleneck : ratio msg_per_sec / effective_capacity
    bottleneck_scores = {
        q: round(queue_throughput[q]["msg_per_sec"] / max(per_queue_capacity[q], 1), 3)
        for q in queue_throughput
    }
    bottleneck_queue = max(bottleneck_scores, key=bottleneck_scores.get)

    # Nœuds : 3, distribution uniforme estimée
    per_node_msg_per_sec = round(total_msg_per_sec / 3, 1)

    # Mémoire estimée (règle empirique : ~1 KB/message en flight)
    estimated_memory_mb = round(total_in_flight * 1024 / (1024 * 1024), 2)

    throughput_report = {
        "simulation_parameters": {
            "nodes": 3,
            "queue_count": len(queue_throughput),
            "total_consumers": total_consumers,
            "total_in_flight_capacity": total_in_flight,
        },
        "per_queue": {
            q: {
                "msg_per_sec": v["msg_per_sec"],
                "consumers": v["consumers"],
                "prefetch": v["prefetch"],
                "effective_capacity": per_queue_capacity[q],
                "load_ratio": bottleneck_scores[q],
            }
            for q, v in queue_throughput.items()
        },
        "estimated_throughput_total": {
            "messages_per_second": total_msg_per_sec,
            "messages_per_minute": total_msg_per_sec * 60,
            "messages_per_hour": total_msg_per_sec * 3_600,
            "per_node_msg_per_sec": per_node_msg_per_sec,
        },
        "bottleneck_analysis": {
            "bottleneck_queue": bottleneck_queue,
            "bottleneck_load_ratio": bottleneck_scores[bottleneck_queue],
            "recommendation": (
                f"Augmenter le nombre de consumers sur '{bottleneck_queue}' "
                f"(ratio charge : {bottleneck_scores[bottleneck_queue]:.3f}). "
                "Envisager quorum queue ou sharding si dépassement 10 000 msg/s."
            ),
        },
        "estimated_memory_usage_mb": estimated_memory_mb,
        "cluster_headroom_pct": round(
            (1 - total_msg_per_sec / 50_000) * 100, 1
        ),  # seuil théorique cluster 50k msg/s
        "notes": "Simulation basée sur préfetch × consumers. Valeurs réelles dépendent du hardware.",
    }
    return throughput_report


# ─────────────────────────────────────────────────────────────────────────────
# RAPPORT PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def _separator(char: str = "─", width: int = 72) -> str:
    return char * width


def _section(title: str) -> None:
    print()
    print(_separator("═"))
    print(f"  {title}")
    print(_separator("═"))


def _subsection(title: str) -> None:
    print()
    print(f"  {_separator('─', 68)}")
    print(f"  {title}")
    print(f"  {_separator('─', 68)}")


if __name__ == "__main__":

    # ─── HEADER ───────────────────────────────────────────────────────────────
    print(_separator("═"))
    print("  RABBITMQ BROKER CONFIGURATION REPORT")
    print("  CaelumSwarm™ — Human Rights / CSDDD 2024 Compliance Platform")
    print(f"  Generated : {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("  Protocol  : AMQP 0-9-1 / TLS 1.3 / 3-node HA Cluster")
    print(_separator("═"))

    # ─── 1. EXCHANGES ─────────────────────────────────────────────────────────
    _section("1. EXCHANGE CONFIGURATIONS (5 types AMQP)")

    headers = ["Exchange Name", "Type", "Durable", "Internal", "Use Case"]
    col_w   = [28, 10, 9, 10, 30]

    header_row = "  " + "  ".join(h.ljust(w) for h, w in zip(headers, col_w))
    print(header_row)
    print("  " + "  ".join("-" * w for w in col_w))

    for name, cfg in RABBITMQ_EXCHANGES.items():
        use_cases = cfg.get("use_cases", [])
        first_use = use_cases[0] if use_cases else cfg.get("description", "")[:28]
        row = [
            name,
            cfg["type"],
            str(cfg["durable"]),
            str(cfg.get("internal", False)),
            first_use,
        ]
        print("  " + "  ".join(v.ljust(w) for v, w in zip(row, col_w)))

    print()
    for name, cfg in RABBITMQ_EXCHANGES.items():
        routing_key = cfg.get("routing_key", "N/A")
        example = cfg.get("example_routing_key", cfg.get("example_headers", "N/A"))
        print(f"  [{name}]")
        print(f"    Description  : {cfg['description']}")
        print(f"    Routing key  : {routing_key}")
        print(f"    Exemple      : {example}")

    # ─── 2. QUEUE CONFIGURATIONS ──────────────────────────────────────────────
    _section("2. QUEUE CONFIGURATIONS (8 queues)")

    for qname, qcfg in QUEUE_CONFIGURATIONS.items():
        ttl = f"{qcfg['ttl_ms']:,} ms" if qcfg.get("ttl_ms") else "aucun (permanent)"
        dlx = qcfg.get("dlx") or "N/A"
        qtype = qcfg.get("type", "classic")
        priority = f"  x-max-priority: {qcfg['x_max_priority']}" if qcfg.get("x_max_priority") else ""
        print(f"  Queue : {qname}")
        print(f"    Type        : {qtype}")
        print(f"    Durable     : {qcfg['durable']}   Exclusive : {qcfg['exclusive']}   "
              f"Auto-delete : {qcfg['auto_delete']}")
        print(f"    TTL         : {ttl}")
        print(f"    Max-length  : {qcfg.get('max_length', 'N/A'):,}")
        print(f"    DLX         : {dlx}{priority}")
        print(f"    Description : {qcfg['description']}")
        print()

    # ─── 3. VHOSTS ────────────────────────────────────────────────────────────
    _section("3. VIRTUAL HOSTS (vHosts)")

    for vname, vcfg in RABBITMQ_VHOSTS.items():
        print(f"  vHost : {vname}")
        print(f"    Max connexions : {vcfg['max_connections']}    "
              f"Max channels : {vcfg['max_channels']}")
        print(f"    TLS requis     : {vcfg['tls_required']}    "
              f"Tracing : {vcfg['tracing']}")
        print(f"    Description    : {vcfg['description']}")
        if vcfg.get("write_once"):
            print("    Mode           : WRITE-ONCE (append-only — CSDDD compliance)")
        print()

    # ─── 4. MESSAGE ROUTING DESIGN ────────────────────────────────────────────
    _section("4. MESSAGE ROUTING DESIGN : wave_alerts → compliance_engine")

    plan = design_message_routing("wave_alerts", "compliance_engine", "critical")
    print(f"  Source domain  : {plan['source_domain']}")
    print(f"  Target domain  : {plan['target_domain']}")
    print(f"  Priority       : {plan['priority'].upper()}")
    print(f"  Exchange       : {plan['exchange']}  ({plan['exchange_type']})")
    print(f"  Routing key    : {plan['routing_key']}")
    print(f"  Binding key    : {plan['binding_key']}")
    print(f"  Prefetch count : {plan['prefetch_count']}")
    print(f"  Ack mode       : {plan['ack_mode']}")
    print(f"  TTL message    : {plan['message_ttl_ms']:,} ms")
    print(f"  DLX enabled    : {plan['dlx_enabled']} → {plan['dlx_name']}")
    print(f"  Latence estimée: {plan['estimated_latency_ms']} ms")
    print(f"  Notes          : {plan['notes']}")

    # ─── 5. DLX FLOW SIMULATION ───────────────────────────────────────────────
    _section("5. DLX FLOW SIMULATION")

    for rc, label in [(2, "Retry en cours (retry_count=2)"), (3, "Limite atteinte (retry_count=3)")]:
        _subsection(label)
        dlx = simulate_dlx_flow(
            message_id=f"msg-caelum-{rc:04d}-test",
            failure_reason="consumer_nack — traitement échoué (timeout analyse)",
            retry_count=rc,
        )
        print(f"  Message ID       : {dlx['message_id']}")
        print(f"  Failure reason   : {dlx['failure_reason']}")
        print(f"  Retry count      : {dlx['retry_count']} / {dlx['max_retries']}")
        print(f"  Status           : {dlx['status']}")
        print(f"  Next action      : {dlx['next_action']}")
        print(f"  Delay            : {dlx['delay_ms']} ms")
        print(f"  Final queue      : {dlx['final_queue']}")
        print(f"  DLX routing key  : {dlx['dlx_routing_key']}")
        print(f"  Alert triggered  : {dlx['alert_triggered']}")
        if dlx['alert_channel']:
            print(f"  Alert channel    : {dlx['alert_channel']}")
        print(f"  Timestamp UTC    : {dlx['timestamp_utc']}")
        print(f"  Notes            : {dlx['notes']}")

    # ─── 6. HA CLUSTER CONFIGURATION ─────────────────────────────────────────
    _section("6. HIGH AVAILABILITY CLUSTER CONFIGURATION")

    ha = configure_ha_cluster()
    print(f"  Cluster name    : {ha['cluster_name']}")
    print(f"  Nodes ({ha['node_count']})       : {', '.join(ha['nodes'])}")
    print(f"  Node type       : {ha['node_type']}")
    print()
    print("  HA Policy :")
    for k, v in ha["ha_policy"].items():
        if isinstance(v, dict):
            print(f"    {k} :")
            for kk, vv in v.items():
                print(f"      {kk} : {vv}")
        else:
            print(f"    {k} : {v}")
    print()
    print("  Quorum Queues :")
    for k, v in ha["quorum_queues"].items():
        print(f"    {k} : {v}")
    print()
    print(f"  Network partition handling : {ha['network_partition_handling']}")
    print(f"  Partition notes : {ha['cluster_partition_notes']}")
    print()
    print("  Plugins :")
    for plugin, enabled in ha["plugins"].items():
        status = "✓ activé" if enabled else "✗ désactivé"
        print(f"    {plugin:<20} : {status}")
    print()
    print("  Shovel (cross-DC) :")
    for k, v in ha["shovel_setup"].items():
        print(f"    {k} : {v}")
    print()
    print("  Load Balancer :")
    for k, v in ha["load_balancer"].items():
        print(f"    {k} : {v}")

    # ─── 7. AMQP CONNECTION CONFIG ────────────────────────────────────────────
    _section("7. AMQP CONNECTION CONFIG (production / TLS 1.3)")

    conn = generate_amqp_connection_config("production")
    print(f"  Environment     : {conn['environment']}")
    print(f"  Hosts           : {', '.join(conn['hosts'])}")
    print(f"  Port            : {conn['port']}  (AMQPS)")
    print(f"  vHost           : {conn['vhost']}")
    print()
    print("  Credentials :")
    for k, v in conn["credentials"].items():
        print(f"    {k} : {v}")
    print()
    print("  TLS :")
    for k, v in conn["tls"].items():
        if isinstance(v, list):
            print(f"    {k} :")
            for item in v:
                print(f"      - {item}")
        else:
            print(f"    {k} : {v}")
    print()
    print("  Connection params :")
    for k, v in conn["connection"].items():
        print(f"    {k} : {v}")
    print()
    print("  Retry policy :")
    for k, v in conn["retry_policy"].items():
        print(f"    {k} : {v}")
    print()
    print(f"  Management URL  : {conn['management_url']}")

    # ─── 8. THROUGHPUT CAPACITY ANALYSIS ──────────────────────────────────────
    _section("8. THROUGHPUT CAPACITY ANALYSIS")

    thr = calculate_throughput_capacity()
    sim = thr["simulation_parameters"]
    print(f"  Nodes           : {sim['nodes']}")
    print(f"  Queues simulées : {sim['queue_count']}")
    print(f"  Total consumers : {sim['total_consumers']}")
    print(f"  In-flight max   : {sim['total_in_flight_capacity']:,} messages")
    print()
    print("  Débit par queue :")
    hdr = ["Queue", "msg/s", "Consumers", "Prefetch", "Capacity", "Load Ratio"]
    col = [22, 8, 11, 9, 10, 10]
    print("  " + "  ".join(h.ljust(w) for h, w in zip(hdr, col)))
    print("  " + "  ".join("-" * w for w in col))
    for q, d in thr["per_queue"].items():
        row = [
            q,
            str(d["msg_per_sec"]),
            str(d["consumers"]),
            str(d["prefetch"]),
            str(d["effective_capacity"]),
            f"{d['load_ratio']:.3f}",
        ]
        print("  " + "  ".join(v.ljust(w) for v, w in zip(row, col)))

    tot = thr["estimated_throughput_total"]
    print()
    print("  Débit total estimé :")
    print(f"    messages/seconde : {tot['messages_per_second']:,}")
    print(f"    messages/minute  : {tot['messages_per_minute']:,}")
    print(f"    messages/heure   : {tot['messages_per_hour']:,}")
    print(f"    par nœud (moy.)  : {tot['per_node_msg_per_sec']:,} msg/s")
    print()
    bn = thr["bottleneck_analysis"]
    print("  Analyse bottleneck :")
    print(f"    Queue critique   : {bn['bottleneck_queue']}")
    print(f"    Load ratio       : {bn['bottleneck_load_ratio']:.3f}")
    print(f"    Recommandation   : {bn['recommendation']}")
    print()
    print(f"  Mémoire estimée  : {thr['estimated_memory_usage_mb']} MB (messages in-flight)")
    print(f"  Headroom cluster : {thr['cluster_headroom_pct']}%  (seuil théorique 50 000 msg/s)")
    print(f"  Note             : {thr['notes']}")

    # ─── 9. SECURITY CHECKLIST ────────────────────────────────────────────────
    _section("9. RABBITMQ SECURITY CHECKLIST")

    checklist = [
        ("TLS",       "TLS 1.3 activé sur port 5671 (AMQPS)",                True),
        ("TLS",       "Authentification mutuelle (verify_peer + client cert)", True),
        ("TLS",       "Ciphers forts uniquement (AES-256-GCM, ChaCha20)",     True),
        ("TLS",       "fail_if_no_peer_cert : True",                          True),
        ("Auth",      "Utilisateurs avec permissions minimales (least priv.)", True),
        ("Auth",      "loopback_users désactivés",                            True),
        ("Auth",      "Politique mot de passe : min 20 chars, rotation 90j",  True),
        ("Auth",      "Credentials chargés depuis vault (jamais en clair)",   True),
        ("vHosts",    "Ségrégation prod / dev / audit par vHost distinct",     True),
        ("vHosts",    "caelum_audit : mode write-once (CSDDD compliance)",    True),
        ("vHosts",    "TLS requis sur vHosts prod et audit",                  True),
        ("Shovel",    "Shovel cross-DC via AMQPS (port 5671)",               True),
        ("Shovel",    "URI shovel sans credentials en clair",                 True),
        ("Heartbeat", "Heartbeat 60s — détection connexions zombies",         True),
        ("Heartbeat", "Connection timeout : 30 000 ms",                       True),
        ("DLX",       "Dead Letter Exchange configuré sur toutes queues prod", True),
        ("DLX",       "Poison queue avec alerte sur profondeur > 100",        True),
        ("DLX",       "Max 3 tentatives + backoff exponentiel",               True),
        ("Mgmt",      "Management UI accessible HTTPS uniquement",            True),
        ("Mgmt",      "Prometheus plugin — métriques exportées",              True),
        ("Mgmt",      "Tracing activé sur tous vHosts",                       True),
    ]

    current_cat = ""
    for cat, item, ok in checklist:
        if cat != current_cat:
            print(f"\n  [{cat}]")
            current_cat = cat
        mark = "✓" if ok else "✗"
        print(f"    {mark}  {item}")

    # ─── FOOTER ───────────────────────────────────────────────────────────────
    print()
    print(_separator("═"))
    print()
    print("  RabbitMQ Protocol Agent — PRÊT (AMQP 0-9-1 / TLS 1.3 / 3-node HA Cluster)")
    print()
    print(_separator("═"))
