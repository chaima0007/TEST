"""
Agent Déploiement Redis Docker — Redis 7.2, Redis Cluster (6 nodes),
Docker Compose, Redis Sentinel, AOF + RDB persistence, TLS 1.3,
Lua scripts atomiques et memory management pour CaelumSwarm™.
Déploiement production containerisé, haute disponibilité multi-AZ,
conformité CSDDD 2024 — chiffrement mTLS, secrets via Vault.
"""

import math
import random
import time
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Constantes de données
# ---------------------------------------------------------------------------

REDIS_CLUSTER_NODES = {
    "master_1": {
        "port": 7001,
        "slot_range": "0-5460",
        "memory_limit": "2GB",
        "role": "master",
        "dc": "eu-west-1a",
        "ip": "172.20.0.11",
        "bus_port": 17001,
    },
    "master_2": {
        "port": 7002,
        "slot_range": "5461-10922",
        "memory_limit": "2GB",
        "role": "master",
        "dc": "eu-west-1b",
        "ip": "172.20.0.12",
        "bus_port": 17002,
    },
    "master_3": {
        "port": 7003,
        "slot_range": "10923-16383",
        "memory_limit": "2GB",
        "role": "master",
        "dc": "eu-west-1c",
        "ip": "172.20.0.13",
        "bus_port": 17003,
    },
    "replica_1": {
        "port": 7004,
        "replicates": "master_1",
        "memory_limit": "2GB",
        "role": "replica",
        "dc": "eu-west-1b",
        "ip": "172.20.0.14",
        "bus_port": 17004,
    },
    "replica_2": {
        "port": 7005,
        "replicates": "master_2",
        "memory_limit": "2GB",
        "role": "replica",
        "dc": "eu-west-1c",
        "ip": "172.20.0.15",
        "bus_port": 17005,
    },
    "replica_3": {
        "port": 7006,
        "replicates": "master_3",
        "memory_limit": "2GB",
        "role": "replica",
        "dc": "eu-west-1a",
        "ip": "172.20.0.16",
        "bus_port": 17006,
    },
}

REDIS_CONFIG_PRODUCTION = {
    "maxmemory": "1800mb",              # 90 % de 2 GB
    "maxmemory_policy": "allkeys-lru",
    "save": ["3600 1", "300 100", "60 10000"],  # RDB snapshots
    "appendonly": "yes",                # AOF enabled
    "appendfsync": "everysec",          # fsync every second
    "aof_rewrite_incremental_fsync": "yes",
    "tls_port": 6380,
    "tls_cert_file": "/etc/redis/tls/redis.crt",
    "tls_key_file": "/etc/redis/tls/redis.key",
    "tls_ca_cert_file": "/etc/redis/tls/ca.crt",
    "tls_auth_clients": "yes",          # mTLS required
    "requirepass": "VAULT_MANAGED",
    "masterauth": "VAULT_MANAGED",
    "cluster_enabled": "yes",
    "cluster_config_file": "nodes.conf",
    "cluster_node_timeout": 5000,
    "cluster_require_full_coverage": "no",  # partial writes si node down
    "lazyfree_lazy_eviction": "yes",    # non-blocking eviction
    "latency_monitor_threshold": 10,    # ms
    "slowlog_log_slower_than": 10000,   # microseconds
    "activerehashing": "yes",
    "tcp_backlog": 511,
    "tcp_keepalive": 300,
    "loglevel": "notice",
}

DOCKER_COMPOSE_REDIS_CLUSTER = {
    "redis_master_1": {
        "image": "redis:7.2-alpine",
        "container_name": "redis-master-1",
        "ports": ["7001:7001", "17001:17001"],
        "volumes": [
            "redis_master_1_data:/data",
            "./redis.conf:/etc/redis/redis.conf",
            "./tls:/etc/redis/tls:ro",
        ],
        "command": (
            "redis-server /etc/redis/redis.conf "
            "--port 7001 --cluster-announce-port 7001 "
            "--cluster-announce-bus-port 17001"
        ),
        "networks": {"caelum_db": {"ipv4_address": "172.20.0.11"}},
        "healthcheck": {
            "test": "redis-cli -p 7001 ping",
            "interval": "5s",
            "timeout": "3s",
            "retries": 5,
        },
        "deploy": {
            "resources": {
                "limits": {"memory": "2G"},
                "reservations": {"memory": "1G"},
            }
        },
        "labels": {"prometheus_scrape": "true", "prometheus_port": "9121"},
    },
    "redis_master_2": {
        "image": "redis:7.2-alpine",
        "container_name": "redis-master-2",
        "ports": ["7002:7002", "17002:17002"],
        "volumes": [
            "redis_master_2_data:/data",
            "./redis.conf:/etc/redis/redis.conf",
            "./tls:/etc/redis/tls:ro",
        ],
        "command": (
            "redis-server /etc/redis/redis.conf "
            "--port 7002 --cluster-announce-port 7002 "
            "--cluster-announce-bus-port 17002"
        ),
        "networks": {"caelum_db": {"ipv4_address": "172.20.0.12"}},
        "healthcheck": {
            "test": "redis-cli -p 7002 ping",
            "interval": "5s",
            "timeout": "3s",
            "retries": 5,
        },
        "deploy": {
            "resources": {
                "limits": {"memory": "2G"},
                "reservations": {"memory": "1G"},
            }
        },
        "labels": {"prometheus_scrape": "true", "prometheus_port": "9122"},
    },
    "redis_master_3": {
        "image": "redis:7.2-alpine",
        "container_name": "redis-master-3",
        "ports": ["7003:7003", "17003:17003"],
        "volumes": [
            "redis_master_3_data:/data",
            "./redis.conf:/etc/redis/redis.conf",
            "./tls:/etc/redis/tls:ro",
        ],
        "command": (
            "redis-server /etc/redis/redis.conf "
            "--port 7003 --cluster-announce-port 7003 "
            "--cluster-announce-bus-port 17003"
        ),
        "networks": {"caelum_db": {"ipv4_address": "172.20.0.13"}},
        "healthcheck": {
            "test": "redis-cli -p 7003 ping",
            "interval": "5s",
            "timeout": "3s",
            "retries": 5,
        },
        "deploy": {
            "resources": {
                "limits": {"memory": "2G"},
                "reservations": {"memory": "1G"},
            }
        },
        "labels": {"prometheus_scrape": "true", "prometheus_port": "9123"},
    },
    "redis_replica_1": {
        "image": "redis:7.2-alpine",
        "container_name": "redis-replica-1",
        "ports": ["7004:7004", "17004:17004"],
        "volumes": [
            "redis_replica_1_data:/data",
            "./redis.conf:/etc/redis/redis.conf",
            "./tls:/etc/redis/tls:ro",
        ],
        "command": (
            "redis-server /etc/redis/redis.conf "
            "--port 7004 --cluster-announce-port 7004 "
            "--cluster-announce-bus-port 17004"
        ),
        "networks": {"caelum_db": {"ipv4_address": "172.20.0.14"}},
        "healthcheck": {
            "test": "redis-cli -p 7004 ping",
            "interval": "5s",
            "timeout": "3s",
            "retries": 5,
        },
        "deploy": {
            "resources": {
                "limits": {"memory": "2G"},
                "reservations": {"memory": "1G"},
            }
        },
        "labels": {"prometheus_scrape": "true", "prometheus_port": "9124"},
    },
    "redis_replica_2": {
        "image": "redis:7.2-alpine",
        "container_name": "redis-replica-2",
        "ports": ["7005:7005", "17005:17005"],
        "volumes": [
            "redis_replica_2_data:/data",
            "./redis.conf:/etc/redis/redis.conf",
            "./tls:/etc/redis/tls:ro",
        ],
        "command": (
            "redis-server /etc/redis/redis.conf "
            "--port 7005 --cluster-announce-port 7005 "
            "--cluster-announce-bus-port 17005"
        ),
        "networks": {"caelum_db": {"ipv4_address": "172.20.0.15"}},
        "healthcheck": {
            "test": "redis-cli -p 7005 ping",
            "interval": "5s",
            "timeout": "3s",
            "retries": 5,
        },
        "deploy": {
            "resources": {
                "limits": {"memory": "2G"},
                "reservations": {"memory": "1G"},
            }
        },
        "labels": {"prometheus_scrape": "true", "prometheus_port": "9125"},
    },
    "redis_replica_3": {
        "image": "redis:7.2-alpine",
        "container_name": "redis-replica-3",
        "ports": ["7006:7006", "17006:17006"],
        "volumes": [
            "redis_replica_3_data:/data",
            "./redis.conf:/etc/redis/redis.conf",
            "./tls:/etc/redis/tls:ro",
        ],
        "command": (
            "redis-server /etc/redis/redis.conf "
            "--port 7006 --cluster-announce-port 7006 "
            "--cluster-announce-bus-port 17006"
        ),
        "networks": {"caelum_db": {"ipv4_address": "172.20.0.16"}},
        "healthcheck": {
            "test": "redis-cli -p 7006 ping",
            "interval": "5s",
            "timeout": "3s",
            "retries": 5,
        },
        "deploy": {
            "resources": {
                "limits": {"memory": "2G"},
                "reservations": {"memory": "1G"},
            }
        },
        "labels": {"prometheus_scrape": "true", "prometheus_port": "9126"},
    },
}

REDIS_SENTINEL_CONFIG = {
    "sentinels": 3,
    "quorum": 2,
    "down_after_milliseconds": 30000,
    "failover_timeout": 60000,
    "parallel_syncs": 1,
    "sentinel_announce_ip": "auto",
    "monitor_name": "caelum-master",
    "sentinel_ports": [26379, 26380, 26381],
    "auth_pass": "VAULT_MANAGED",
    "notification_script": "/etc/redis/sentinel-notify.sh",
    "client_reconfig_script": "/etc/redis/sentinel-reconfig.sh",
}

PERSISTENCE_STRATEGY = {
    "rdb": {
        "enabled": True,
        "snapshots": [
            {"changes": 1, "seconds": 3600},       # 1 change in 1 hour
            {"changes": 100, "seconds": 300},      # 100 changes in 5 min
            {"changes": 10000, "seconds": 60},     # 10k changes in 1 min
        ],
        "compression": True,
        "checksum": True,
        "filename": "dump.rdb",
    },
    "aof": {
        "enabled": True,
        "fsync": "everysec",                        # balance perf/durability
        "auto_rewrite_percent": 100,
        "auto_rewrite_min_size": "64mb",
        "use_rdb_preamble": True,                   # faster AOF rewrite
    },
    "backup": {
        "tool": "redis-dump",
        "schedule": "0 2 * * *",                   # daily 2am
        "retention_days": 7,
        "destination": "s3://caelum-redis-backups-eu",
        "encryption": "AES-256",
    },
}

LUA_SCRIPTS = {
    "atomic_rate_limit": {
        "description": "Rate limiting atomique avec sliding window",
        "script": """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local current_time = redis.call('TIME')
local current_ms = current_time[1] * 1000 + math.floor(current_time[2] / 1000)
local window_start = current_ms - window
redis.call('ZREMRANGEBYSCORE', key, 0, window_start)
local count = redis.call('ZCARD', key)
if count >= limit then
    return {0, limit - count, 0}
end
redis.call('ZADD', key, current_ms, current_ms)
redis.call('PEXPIRE', key, window)
return {1, limit - count - 1, current_ms}
        """,
        "keys": 1,
        "args": ["limit", "window_ms"],
    },
    "cache_aside_atomic": {
        "description": "Cache-aside pattern atomique",
        "script": """
local key = KEYS[1]
local value = ARGV[1]
local ttl = tonumber(ARGV[2])
local existing = redis.call('GET', key)
if existing then return existing end
redis.call('SET', key, value, 'PX', ttl * 1000)
return value
        """,
        "keys": 1,
        "args": ["value", "ttl_seconds"],
    },
    "distributed_lock": {
        "description": "Redlock implementation atomique",
        "script": """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
else
    return 0
end
        """,
        "keys": 1,
        "args": ["lock_token"],
    },
}

MONITORING_METRICS = {
    "critical": [
        "connected_clients",
        "used_memory_rss",
        "instantaneous_ops_per_sec",
        "keyspace_hits",
        "keyspace_misses",
    ],
    "cluster_health": [
        "cluster_state",
        "cluster_slots_assigned",
        "cluster_known_nodes",
        "cluster_size",
    ],
    "performance": [
        "latency_ms_p99",
        "slowlog_len",
        "rdb_last_save_time",
        "aof_pending_rewrite",
    ],
    "memory": [
        "used_memory_human",
        "mem_fragmentation_ratio",
        "maxmemory_human",
        "evicted_keys",
    ],
}

SECURITY_CHECKLIST = {
    "tls": {
        "label": "TLS 1.3 chiffrement en transit",
        "directive": "tls-port 6380 / tls-cert-file / tls-key-file",
        "status": "OBLIGATOIRE",
    },
    "mtls": {
        "label": "mTLS — authentification client mutuelle",
        "directive": "tls-auth-clients yes",
        "status": "OBLIGATOIRE",
    },
    "requirepass": {
        "label": "Mot de passe Redis (géré par Vault)",
        "directive": "requirepass VAULT_MANAGED / masterauth VAULT_MANAGED",
        "status": "OBLIGATOIRE",
    },
    "acl": {
        "label": "ACL utilisateurs avec permissions minimales",
        "directive": "ACL SETUSER caelum-app on >PASSWORD ~caelum:* +@read +@write",
        "status": "RECOMMANDE",
    },
    "rename_command": {
        "label": "Désactivation commandes dangereuses",
        "directive": "rename-command FLUSHALL \"\" / rename-command DEBUG \"\" / rename-command CONFIG \"\"",
        "status": "OBLIGATOIRE",
    },
    "bind": {
        "label": "Écoute sur interfaces internes uniquement",
        "directive": "bind 127.0.0.1 172.20.0.0/24",
        "status": "OBLIGATOIRE",
    },
    "protected_mode": {
        "label": "Mode protégé activé",
        "directive": "protected-mode yes",
        "status": "OBLIGATOIRE",
    },
    "network_policy": {
        "label": "Network policy Docker — isolation réseau caelum_db",
        "directive": "networks: caelum_db (internal: true, no external access)",
        "status": "OBLIGATOIRE",
    },
}


# ---------------------------------------------------------------------------
# Fonctions
# ---------------------------------------------------------------------------

def generate_redis_cluster_init_script() -> str:
    """
    Génère le script bash d'initialisation du cluster Redis 6 nœuds.

    Returns:
        str: Script bash complet avec redis-cli --cluster create,
             health check post-init et vérification des slots assignés.
    """
    masters = {k: v for k, v in REDIS_CLUSTER_NODES.items() if v["role"] == "master"}
    replicas = {k: v for k, v in REDIS_CLUSTER_NODES.items() if v["role"] == "replica"}

    node_list = " ".join(
        f"{v['ip']}:{v['port']}"
        for v in list(masters.values()) + list(replicas.values())
    )

    lines = [
        "#!/usr/bin/env bash",
        "# Script d'initialisation — Redis Cluster 6 noeuds CaelumSwarm™",
        "# Redis 7.2 | 3 masters + 3 replicas | 16384 hash slots",
        "set -euo pipefail",
        "",
        "REDIS_PASSWORD=\"${REDIS_PASSWORD:-$(vault kv get -field=password secret/caelum/redis)}\"",
        "",
        "echo '[ 1/4 ] Attente disponibilite des noeuds Redis...'",
    ]

    for name, node in REDIS_CLUSTER_NODES.items():
        node_ip = node['ip']
        node_port = node['port']
        lines.append(
            f"until redis-cli -h {node_ip} -p {node_port} -a \"$REDIS_PASSWORD\" ping | grep -q PONG; do"
        )
        lines.append(f"  echo '  Attente {name} ({node_ip}:{node_port})...' ; sleep 2")
        lines.append("done")

    lines += [
        "",
        "echo '[ 2/4 ] Creation du cluster Redis...'",
        f"redis-cli --cluster create {node_list} \\",
        "  --cluster-replicas 1 \\",
        "  -a \"$REDIS_PASSWORD\" \\",
        "  --cluster-yes",
        "",
        "echo '[ 3/4 ] Verification de l etat du cluster...'",
        f"redis-cli -h 172.20.0.11 -p 7001 -a \"$REDIS_PASSWORD\" cluster info | grep cluster_state",
        f"redis-cli -h 172.20.0.11 -p 7001 -a \"$REDIS_PASSWORD\" cluster nodes",
        "",
        "echo '[ 4/4 ] Verification slots assignes (attendu: 16384)...'",
        f"SLOTS=$(redis-cli -h 172.20.0.11 -p 7001 -a \"$REDIS_PASSWORD\" cluster info | grep cluster_slots_assigned | cut -d: -f2 | tr -d '\\r')",
        "if [ \"$SLOTS\" = \"16384\" ]; then",
        "  echo 'OK: 16384 slots assignes — cluster pret.'",
        "else",
        "  echo \"ERREUR: slots assignes=$SLOTS (attendu 16384)\" ; exit 1",
        "fi",
        "",
        "echo 'Redis Cluster 6 noeuds initialise avec succes.'",
    ]

    return "\n".join(lines)


def simulate_cluster_failover(failed_node: str) -> dict:
    """
    Simule le failover Redis Cluster quand un master tombe.

    Args:
        failed_node: Nom du nœud défaillant (ex. "master_1").

    Returns:
        dict: Étapes du failover, durée estimée, nœud promu et disponibilité des données.
    """
    node_info = REDIS_CLUSTER_NODES.get(failed_node)
    if node_info is None:
        return {"error": f"Noeud inconnu : {failed_node}"}

    if node_info["role"] != "master":
        return {"error": f"{failed_node} n'est pas un master — failover non applicable"}

    # Identifier le replica correspondant
    promoted_replica = None
    for name, node in REDIS_CLUSTER_NODES.items():
        if node["role"] == "replica" and node.get("replicates") == failed_node:
            promoted_replica = (name, node)
            break

    if promoted_replica is None:
        return {"error": f"Aucun replica trouve pour {failed_node}"}

    replica_name, replica_node = promoted_replica

    # Timing réaliste Redis Cluster failover
    cluster_node_timeout = REDIS_CONFIG_PRODUCTION["cluster_node_timeout"]  # ms
    detection_ms = cluster_node_timeout                      # nœud considéré down
    election_ms = int(cluster_node_timeout * 0.5)           # election replica
    promotion_ms = random.randint(80, 200)                  # promotion effective
    slot_reassign_ms = random.randint(30, 100)              # reassignation slots
    total_ms = detection_ms + election_ms + promotion_ms + slot_reassign_ms
    total_seconds = round(total_ms / 1000, 2)

    slot_range = node_info["slot_range"]

    failover_steps = [
        {
            "step": 1,
            "phase": "DETECTION",
            "duration_ms": detection_ms,
            "description": (
                f"Les autres masters détectent {failed_node} ({node_info['ip']}:{node_info['port']}) "
                f"comme unreachable après {cluster_node_timeout} ms sans réponse PING."
            ),
            "cluster_state": "PARTIAL_DOWN",
            "slots_affected": slot_range,
        },
        {
            "step": 2,
            "phase": "ELECTION",
            "duration_ms": election_ms,
            "description": (
                f"{replica_name} ({replica_node['ip']}:{replica_node['port']}) "
                f"demande un vote de failover. Quorum obtenu : 2/2 masters actifs."
            ),
            "cluster_state": "FAILOVER_IN_PROGRESS",
            "candidate": replica_name,
        },
        {
            "step": 3,
            "phase": "PROMOTION",
            "duration_ms": promotion_ms,
            "description": (
                f"{replica_name} se promet master. Reprise des slots {slot_range} "
                f"(5461 slots). Mise à jour nodes.conf sur tous les nœuds."
            ),
            "cluster_state": "RECONFIGURING",
            "new_master": replica_name,
            "new_master_ip": f"{replica_node['ip']}:{replica_node['port']}",
        },
        {
            "step": 4,
            "phase": "SLOT_REASSIGNMENT",
            "duration_ms": slot_reassign_ms,
            "description": (
                f"Propagation cluster gossip — slots {slot_range} officiellement "
                f"assignés à {replica_name}. Clients redirigés via MOVED."
            ),
            "cluster_state": "OK",
            "slots_reassigned": slot_range,
        },
    ]

    # Estimation perte données (AOF everysec = max 1s de données)
    max_data_loss_seconds = 1 if REDIS_CONFIG_PRODUCTION["appendfsync"] == "everysec" else 0

    return {
        "failed_node": failed_node,
        "failed_node_details": {
            "ip": node_info["ip"],
            "port": node_info["port"],
            "slot_range": node_info["slot_range"],
            "dc": node_info["dc"],
        },
        "promoted_replica": replica_name,
        "promoted_replica_details": {
            "ip": replica_node["ip"],
            "port": replica_node["port"],
            "dc": replica_node["dc"],
        },
        "failover_steps": failover_steps,
        "duration_total_ms": total_ms,
        "duration_total_seconds": total_seconds,
        "data_availability": {
            "slots_affected": slot_range,
            "downtime_seconds": total_seconds,
            "write_availability_during_failover": "NON (slots non servis pendant election)",
            "read_availability_during_failover": "NON (replica promoté — non encore master)",
            "max_data_loss_seconds": max_data_loss_seconds,
            "persistence_mode": f"AOF {REDIS_CONFIG_PRODUCTION['appendfsync']} + RDB",
        },
        "cluster_state_post_failover": "OK — 3 masters actifs, 2 replicas (1 manquant jusqu'à récupération)",
        "recovery_action": (
            f"Relancer {failed_node} → il rejoindra le cluster comme replica de {replica_name} "
            f"(CLUSTER MEET + replication automatique)"
        ),
    }


def design_cache_strategy(use_case: str) -> dict:
    """
    Conçoit la stratégie de cache optimale pour un cas d'usage CaelumSwarm™.

    Args:
        use_case: Identifiant du cas d'usage parmi :
                  "api_response", "session", "rate_limit", "leaderboard", "pub_sub".

    Returns:
        dict: Structure de données Redis, TTL, politique d'éviction,
              hit rate estimé et configuration cluster_slot dédiée.
    """
    strategies = {
        "api_response": {
            "label": "Cache réponses API engines Wave",
            "data_structure": "STRING",
            "redis_command_set": "SET key value EX ttl NX",
            "redis_command_get": "GET key",
            "ttl_seconds": 30,
            "key_pattern": "caelum:api:{endpoint_slug}:{params_hash}",
            "eviction_policy": "allkeys-lru",
            "estimated_hit_rate_pct": 88,
            "memory_per_key_kb": 12,
            "max_keys_per_node": 50000,
            "caelum_benefit": "Latence <1 ms pour résultats engines (vs 120 ms upstream)",
            "invalidation": "TTL + SCAN/DEL sur événement POST /api/wave",
            "cluster_hint": "Hash tag {wave_id} pour colocaliser clés liées",
        },
        "session": {
            "label": "Sessions utilisateur persistantes",
            "data_structure": "HASH",
            "redis_command_set": "HSET session:{id} field value",
            "redis_command_get": "HGETALL session:{id}",
            "ttl_seconds": 3600,
            "key_pattern": "caelum:session:{user_id}",
            "eviction_policy": "volatile-lru",
            "estimated_hit_rate_pct": 95,
            "memory_per_key_kb": 0.5,
            "max_keys_per_node": 200000,
            "caelum_benefit": "Sessions multi-agents sans DB relationnelle, failover transparent",
            "invalidation": "EXPIRE refresh sur activité / DEL sur logout",
            "cluster_hint": "HASH tag {user_id} pour colocaliser session + préférences",
        },
        "rate_limit": {
            "label": "Rate limiting sliding window",
            "data_structure": "SORTED_SET",
            "redis_command_set": "ZADD key timestamp member / ZREMRANGEBYSCORE (via Lua)",
            "redis_command_get": "ZCARD key",
            "ttl_seconds": 60,
            "key_pattern": "caelum:ratelimit:{client_id}:{window_s}s",
            "eviction_policy": "allkeys-lru",
            "estimated_hit_rate_pct": 99,
            "memory_per_key_kb": 0.25,
            "max_keys_per_node": 500000,
            "caelum_benefit": "Protection anti-abus endpoints Swarm Intelligence — 100k ops/s",
            "invalidation": "PEXPIRE automatique sur fenêtre glissante",
            "cluster_hint": "Pas de hash tag — distribution naturelle par client_id",
        },
        "leaderboard": {
            "label": "Classements scores engines droits humains",
            "data_structure": "SORTED_SET",
            "redis_command_set": "ZADD leaderboard score member",
            "redis_command_get": "ZREVRANGE leaderboard 0 N WITHSCORES",
            "ttl_seconds": 300,
            "key_pattern": "caelum:leaderboard:{domain}:{wave_id}",
            "eviction_policy": "volatile-ttl",
            "estimated_hit_rate_pct": 92,
            "memory_per_key_kb": 1.0,
            "max_keys_per_node": 10000,
            "caelum_benefit": "Top-N entités risque en O(log N) — classement temps réel Wave",
            "invalidation": "TTL + ZADD incrémental après chaque engine run",
            "cluster_hint": "HASH tag {wave_id} pour classements multi-domaines colocolisés",
        },
        "pub_sub": {
            "label": "Pub/Sub alertes critiques temps réel",
            "data_structure": "STREAM",
            "redis_command_set": "XADD stream MAXLEN ~ 10000 * field value",
            "redis_command_get": "XREADGROUP GROUP consumers > COUNT 10",
            "ttl_seconds": 86400,
            "key_pattern": "caelum:stream:alerts:{severity}",
            "eviction_policy": "allkeys-lru",
            "estimated_hit_rate_pct": 80,
            "memory_per_key_kb": 2.0,
            "max_keys_per_node": 5000,
            "caelum_benefit": "Garantie at-least-once via consumer groups (vs Pub/Sub at-most-once)",
            "invalidation": "XACK + XTRIM MAXLEN ~ 10000 (fenêtre glissante)",
            "cluster_hint": "Stream sur un seul nœud — HASH tag {severity} pour regroupement",
        },
    }

    result = strategies.get(use_case)
    if result is None:
        available = list(strategies.keys())
        return {
            "error": f"Cas d'usage inconnu : '{use_case}'",
            "available_use_cases": available,
        }

    result["use_case"] = use_case
    result["persistence"] = PERSISTENCE_STRATEGY["aof"]["fsync"]
    result["cluster_nodes"] = len(REDIS_CLUSTER_NODES)
    result["tls_required"] = True

    return result


def analyze_memory_fragmentation(used_memory_mb: float, rss_mb: float) -> dict:
    """
    Analyse la fragmentation mémoire Redis et recommande des actions correctives.

    Args:
        used_memory_mb: Mémoire logique utilisée par Redis (used_memory, en MB).
        rss_mb: Mémoire physique allouée par l'OS (used_memory_rss, en MB).

    Returns:
        dict: Ratio de fragmentation, statut (ok/warning/critical),
              recommandations et configuration activedefrag suggérée.
    """
    if used_memory_mb <= 0:
        return {"error": "used_memory_mb doit être > 0"}

    ratio = rss_mb / used_memory_mb
    ratio_rounded = round(ratio, 3)
    wasted_mb = round(rss_mb - used_memory_mb, 2)

    # Classification
    if ratio < 1.0:
        status = "SWAP"
        severity = "CRITICAL"
        interpretation = (
            "Ratio < 1.0 indique que Redis utilise le swap — performances dégradées. "
            "Redis écrit en swap : latences en ms voire secondes."
        )
    elif ratio < 1.15:
        status = "OK"
        severity = "INFO"
        interpretation = (
            "Fragmentation normale. Redis gère efficacement sa mémoire. Aucune action requise."
        )
    elif ratio < 1.30:
        status = "WARNING"
        severity = "WARNING"
        interpretation = (
            f"Fragmentation modérée ({ratio_rounded:.2f}). "
            f"{wasted_mb} MB gaspillés. Surveiller la tendance — activer activedefrag en prévention."
        )
    elif ratio < 1.60:
        status = "ELEVATED"
        severity = "WARNING"
        interpretation = (
            f"Fragmentation élevée ({ratio_rounded:.2f}). "
            f"{wasted_mb} MB gaspillés. Activer activedefrag immédiatement."
        )
    else:
        status = "CRITICAL"
        severity = "CRITICAL"
        interpretation = (
            f"Fragmentation critique ({ratio_rounded:.2f}). "
            f"{wasted_mb} MB gaspillés. Redémarrage planifié recommandé après BGSAVE."
        )

    recommendations = []

    if status in ("WARNING", "ELEVATED"):
        recommendations.append(
            "Activer activedefrag : CONFIG SET activedefrag yes"
        )
        recommendations.append(
            "Ajuster seuils : active-defrag-ignore-bytes 100mb / active-defrag-threshold-lower 10"
        )

    if status == "CRITICAL" and ratio >= 1.60:
        recommendations.append(
            "Planifier BGSAVE puis redémarrage Redis en fenêtre de maintenance"
        )
        recommendations.append(
            "MEMORY PURGE (bloquant en prod) — préférer activedefrag en rolling restart"
        )

    if status == "SWAP":
        recommendations.append(
            "URGENCE : augmenter maxmemory ou ajouter nœud cluster immédiatement"
        )
        recommendations.append(
            "Vérifier vm.overcommit_memory=1 sur l'hôte Docker (sysctl)"
        )

    if not recommendations:
        recommendations.append(
            "Aucune action requise. Vérifier ratio toutes les heures via Prometheus."
        )

    # Configuration activedefrag suggérée
    activedefrag_config = {
        "activedefrag": "yes" if ratio >= 1.15 else "no",
        "active_defrag_ignore_bytes": "100mb",
        "active_defrag_threshold_lower": 10,     # % fragmentation minimale
        "active_defrag_threshold_upper": 100,    # % fragmentation max avant max CPU
        "active_defrag_cycle_min": 1,            # % CPU min pour defrag
        "active_defrag_cycle_max": 25,           # % CPU max pour defrag
        "active_defrag_max_scan_fields": 1000,
    }

    # Projection post-defrag
    estimated_post_defrag_ratio = max(1.05, ratio - 0.25) if ratio > 1.30 else ratio
    estimated_post_defrag_rss_mb = round(used_memory_mb * estimated_post_defrag_ratio, 2)
    memory_savings_mb = round(rss_mb - estimated_post_defrag_rss_mb, 2)

    return {
        "used_memory_mb": round(used_memory_mb, 2),
        "rss_mb": round(rss_mb, 2),
        "fragmentation_ratio": ratio_rounded,
        "wasted_memory_mb": wasted_mb,
        "status": status,
        "severity": severity,
        "interpretation": interpretation,
        "recommendations": recommendations,
        "activedefrag_config": activedefrag_config,
        "projection_post_defrag": {
            "estimated_ratio": round(estimated_post_defrag_ratio, 3),
            "estimated_rss_mb": estimated_post_defrag_rss_mb,
            "potential_savings_mb": memory_savings_mb,
        },
        "maxmemory_headroom_pct": round(
            (1 - used_memory_mb / 1800) * 100, 1  # 1800 MB = maxmemory prod
        ),
    }


def generate_docker_compose_redis_cluster() -> str:
    """
    Génère le docker-compose.yml complet pour le cluster Redis 6 nœuds.

    Returns:
        str: YAML string complet avec tous les services, volumes, réseaux
             et healthchecks pour Docker Compose v3.8.
    """
    indent2 = "  "
    indent4 = "    "
    indent6 = "      "
    indent8 = "        "

    lines = [
        "# docker-compose.yml — Redis Cluster 6 noeuds CaelumSwarm™",
        "# Redis 7.2-alpine | 3 masters + 3 replicas | TLS 1.3 | AOF+RDB",
        "# Generé par redis-docker-service-agent.py",
        "version: '3.8'",
        "",
        "services:",
    ]

    service_order = [
        "redis_master_1",
        "redis_master_2",
        "redis_master_3",
        "redis_replica_1",
        "redis_replica_2",
        "redis_replica_3",
    ]

    for svc_key in service_order:
        svc = DOCKER_COMPOSE_REDIS_CLUSTER[svc_key]
        svc_name = svc_key.replace("_", "-")
        lines += [
            f"{indent2}{svc_name}:",
            f"{indent4}image: {svc['image']}",
            f"{indent4}container_name: {svc['container_name']}",
            f"{indent4}restart: unless-stopped",
            f"{indent4}ports:",
        ]
        for port in svc["ports"]:
            lines.append(f"{indent6}- \"{port}\"")

        lines.append(f"{indent4}volumes:")
        for vol in svc["volumes"]:
            lines.append(f"{indent6}- {vol}")

        lines += [
            f"{indent4}command: >",
            f"{indent6}{svc['command']}",
            f"{indent4}environment:",
            f"{indent6}REDIS_PASSWORD: ${{REDIS_PASSWORD}}",
            f"{indent4}networks:",
            f"{indent6}caelum_db:",
        ]

        ip = svc["networks"]["caelum_db"]["ipv4_address"]
        lines.append(f"{indent8}ipv4_address: {ip}")

        hc = svc["healthcheck"]
        lines += [
            f"{indent4}healthcheck:",
            f"{indent6}test: [\"{hc['test'].split()[0]}\", "
            + ", ".join(f"\"{t}\"" for t in hc["test"].split()[1:]) + "]",
            f"{indent6}interval: {hc['interval']}",
            f"{indent6}timeout: {hc['timeout']}",
            f"{indent6}retries: {hc['retries']}",
            f"{indent6}start_period: 10s",
        ]

        deploy = svc["deploy"]
        lines += [
            f"{indent4}deploy:",
            f"{indent6}resources:",
            f"{indent8}limits:",
            f"{indent6}{indent4}memory: {deploy['resources']['limits']['memory']}",
            f"{indent8}reservations:",
            f"{indent6}{indent4}memory: {deploy['resources']['reservations']['memory']}",
        ]

        labels = svc["labels"]
        lines += [
            f"{indent4}labels:",
        ]
        for k, v in labels.items():
            lines.append(f"{indent6}{k}: \"{v}\"")

        lines.append("")

    # Réseaux
    lines += [
        "networks:",
        f"{indent2}caelum_db:",
        f"{indent4}driver: bridge",
        f"{indent4}internal: true",
        f"{indent4}ipam:",
        f"{indent6}config:",
        f"{indent8}- subnet: 172.20.0.0/24",
        f"{indent6}  gateway: 172.20.0.1",
        "",
    ]

    # Volumes
    lines.append("volumes:")
    for svc_key in service_order:
        vol_name = svc_key + "_data"
        lines += [
            f"{indent2}{vol_name}:",
            f"{indent4}driver: local",
            f"{indent4}driver_opts:",
            f"{indent6}type: none",
            f"{indent6}o: bind",
            f"{indent6}device: /mnt/redis-data/{vol_name}",
        ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Démonstration
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """
    Démonstration complète — Redis Docker Service Agent pour CaelumSwarm™.

    Couvre : topologie cluster 6 nœuds, configuration production, Docker Compose,
    script init cluster, simulation failover, stratégies de cache, scripts Lua,
    persistance, fragmentation mémoire, métriques monitoring et checklist sécurité.
    """
    separator = "=" * 72
    subsep = "-" * 50

    print(separator)
    print("  REDIS CLUSTER DEPLOYMENT — CaelumSwarm™ Docker Service")
    print("  Redis 7.2 | 6-node Cluster | Docker Compose | AOF+RDB | TLS 1.3")
    print(separator)
    print()

    # ------------------------------------------------------------------
    # 1. Cluster topology
    # ------------------------------------------------------------------
    print("[ 1/12 ] TOPOLOGIE CLUSTER — 6 NOEUDS REDIS 7.2")
    print(subsep)

    masters = {k: v for k, v in REDIS_CLUSTER_NODES.items() if v["role"] == "master"}
    replicas = {k: v for k, v in REDIS_CLUSTER_NODES.items() if v["role"] == "replica"}

    print(f"  Masters  : {len(masters)}")
    print(f"  Replicas : {len(replicas)}")
    print(f"  Hash slots total : 16 384 (CRC16 % 16384)")
    print()
    print(f"  {'NOM':<12} {'ROLE':<8} {'PORT':<6} {'IP':<14} {'SLOTS':<14} {'DC'}")
    print(f"  {'-'*12} {'-'*8} {'-'*6} {'-'*14} {'-'*14} {'-'*12}")
    for name, node in REDIS_CLUSTER_NODES.items():
        slot_info = node.get("slot_range", f"replica de {node.get('replicates', '?')}")
        print(
            f"  {name:<12} {node['role']:<8} {node['port']:<6} "
            f"{node['ip']:<14} {slot_info:<14} {node['dc']}"
        )

    print()
    print(f"  Memoire limite par noeud : 2 GB (maxmemory effectif : 1 800 MB)")
    print(f"  Memoire cluster totale   : {6 * 2} GB brut / {6 * 1800 // 1024:.1f} GB utilisable")
    print()

    # ------------------------------------------------------------------
    # 2. Redis production config
    # ------------------------------------------------------------------
    print("[ 2/12 ] CONFIGURATION REDIS PRODUCTION (redis.conf)")
    print(subsep)

    key_params = [
        "maxmemory", "maxmemory_policy", "appendonly", "appendfsync",
        "tls_port", "tls_auth_clients", "requirepass", "cluster_enabled",
        "cluster_node_timeout", "cluster_require_full_coverage",
        "lazyfree_lazy_eviction", "latency_monitor_threshold",
        "slowlog_log_slower_than", "loglevel",
    ]
    for param in key_params:
        val = REDIS_CONFIG_PRODUCTION.get(param, "—")
        print(f"  {param:<40} {val}")

    save_rules = REDIS_CONFIG_PRODUCTION.get("save", [])
    print(f"  {'save (RDB snapshots)':<40} {' | '.join(save_rules)}")
    print()

    # ------------------------------------------------------------------
    # 3. Docker Compose cluster configuration
    # ------------------------------------------------------------------
    print("[ 3/12 ] DOCKER COMPOSE — CONFIGURATION CLUSTER")
    print(subsep)

    for svc_key, svc in DOCKER_COMPOSE_REDIS_CLUSTER.items():
        svc_name = svc_key.replace("_", "-")
        ip = svc["networks"]["caelum_db"]["ipv4_address"]
        ports_str = ", ".join(svc["ports"])
        print(f"  {svc_name:<22} image: {svc['image']:<22} IP: {ip}  ports: {ports_str}")

    print()
    print("  Réseau : caelum_db (bridge, internal: true, subnet 172.20.0.0/24)")
    print("  Volumes : bind-mount /mnt/redis-data/* (persistence hors container)")
    print("  Deploy  : limits 2G / reservations 1G par noeud")
    print("  Labels  : prometheus_scrape=true (metrics via redis_exporter :9121-9126)")
    print()

    # ------------------------------------------------------------------
    # 4. Cluster init script
    # ------------------------------------------------------------------
    print("[ 4/12 ] SCRIPT D'INITIALISATION CLUSTER")
    print(subsep)

    init_script = generate_redis_cluster_init_script()
    script_lines = init_script.split("\n")
    print(f"  Script génère : {len(script_lines)} lignes bash")
    print()
    # Afficher les premières lignes significatives
    for line in script_lines[:20]:
        print(f"  {line}")
    if len(script_lines) > 20:
        print(f"  ... ({len(script_lines) - 20} lignes supplémentaires)")
    print()

    # ------------------------------------------------------------------
    # 5. Failover simulation
    # ------------------------------------------------------------------
    print("[ 5/12 ] SIMULATION FAILOVER — master_1 DOWN")
    print(subsep)

    failover = simulate_cluster_failover("master_1")

    print(f"  Noeud défaillant : {failover['failed_node']}")
    print(f"    IP/Port    : {failover['failed_node_details']['ip']}:{failover['failed_node_details']['port']}")
    print(f"    Slots      : {failover['failed_node_details']['slot_range']}")
    print(f"    Datacenter : {failover['failed_node_details']['dc']}")
    print()
    print(f"  Replica promu   : {failover['promoted_replica']}")
    print(f"    IP/Port    : {failover['promoted_replica_details']['ip']}:{failover['promoted_replica_details']['port']}")
    print(f"    Datacenter : {failover['promoted_replica_details']['dc']} (AZ différente — cross-AZ HA)")
    print()
    print("  Etapes failover :")
    for step in failover["failover_steps"]:
        print(f"    [{step['step']}] {step['phase']:<20} +{step['duration_ms']} ms — {step['description'][:60]}")
    print()

    da = failover["data_availability"]
    print(f"  Durée totale      : {failover['duration_total_ms']} ms ({failover['duration_total_seconds']}s)")
    print(f"  Perte données max : {da['max_data_loss_seconds']}s (AOF everysec)")
    print(f"  Persistance       : {da['persistence_mode']}")
    print(f"  État post-failover: {failover['cluster_state_post_failover']}")
    print(f"  Recovery          : {failover['recovery_action'][:70]}")
    print()

    # ------------------------------------------------------------------
    # 6. Cache strategies
    # ------------------------------------------------------------------
    print("[ 6/12 ] STRATEGIES DE CACHE — 4 CAS D'USAGE")
    print(subsep)

    use_cases = ["api_response", "session", "rate_limit", "leaderboard"]
    for uc in use_cases:
        cs = design_cache_strategy(uc)
        print(f"  [{uc.upper():<14}] {cs['label']}")
        print(f"    Structure  : {cs['data_structure']} — TTL: {cs['ttl_seconds']}s")
        print(f"    Hit rate   : {cs['estimated_hit_rate_pct']} % (estimé)")
        print(f"    Eviction   : {cs['eviction_policy']}")
        print(f"    Clé        : {cs['key_pattern']}")
        print(f"    Bénéfice   : {cs['caelum_benefit'][:65]}")
        print(f"    Cluster    : {cs['cluster_hint'][:65]}")
        print()

    # ------------------------------------------------------------------
    # 7. Lua scripts
    # ------------------------------------------------------------------
    print("[ 7/12 ] SCRIPTS LUA — ATOMICITE REDIS")
    print(subsep)

    for script_name, script_info in LUA_SCRIPTS.items():
        script_lines_count = len([
            l for l in script_info["script"].strip().split("\n") if l.strip()
        ])
        print(f"  {script_name}")
        print(f"    Description : {script_info['description']}")
        print(f"    KEYS        : {script_info.get('keys', 1)}")
        print(f"    ARGV        : {script_info.get('args', [])}")
        print(f"    Lignes Lua  : {script_lines_count}")
        print(f"    Garantie    : ACID atomique — exécution single-threaded Redis")
        print()

    # ------------------------------------------------------------------
    # 8. Persistence strategy
    # ------------------------------------------------------------------
    print("[ 8/12 ] STRATEGIE DE PERSISTANCE — RDB + AOF")
    print(subsep)

    rdb = PERSISTENCE_STRATEGY["rdb"]
    aof = PERSISTENCE_STRATEGY["aof"]
    bkp = PERSISTENCE_STRATEGY["backup"]

    print("  RDB (Redis Database — snapshots binaires) :")
    print(f"    Enabled       : {rdb['enabled']}")
    print(f"    Compression   : {rdb['compression']} (LZF)")
    print(f"    Checksum      : {rdb['checksum']} (CRC64)")
    print(f"    Fichier       : {rdb['filename']}")
    print("    Règles snapshot :")
    for snap in rdb["snapshots"]:
        print(f"      {snap['changes']:>6} changements en {snap['seconds']:>5}s → BGSAVE déclenché")
    print()

    print("  AOF (Append-Only File — journal des commandes) :")
    print(f"    Enabled            : {aof['enabled']}")
    print(f"    fsync              : {aof['fsync']} (max 1s de perte en cas de crash)")
    print(f"    auto-rewrite       : à +{aof['auto_rewrite_percent']} % (min {aof['auto_rewrite_min_size']})")
    print(f"    RDB preamble       : {aof['use_rdb_preamble']} (AOF rewrite rapide)")
    print()

    print("  Backup automatique :")
    print(f"    Outil      : {bkp['tool']}")
    print(f"    Planning   : {bkp['schedule']} (cron — quotidien 2h00 UTC)")
    print(f"    Rétention  : {bkp['retention_days']} jours")
    print(f"    Destination: {bkp['destination']}")
    print(f"    Chiffrement: {bkp['encryption']}")
    print()

    # ------------------------------------------------------------------
    # 9. Memory analysis simulation
    # ------------------------------------------------------------------
    print("[ 9/12 ] ANALYSE FRAGMENTATION MEMOIRE")
    print(subsep)

    scenarios = [
        ("Noeud stable (faible fragmentation)", 1420.0, 1550.0),
        ("Noeud sous pression (fragmentation modérée)", 1600.0, 2100.0),
        ("Noeud critique (fragmentation élevée)", 1200.0, 2040.0),
    ]

    for scenario_label, used_mb, rss_mb in scenarios:
        analysis = analyze_memory_fragmentation(used_mb, rss_mb)
        print(f"  {scenario_label}")
        print(f"    used_memory : {analysis['used_memory_mb']} MB")
        print(f"    rss         : {analysis['rss_mb']} MB")
        print(f"    ratio       : {analysis['fragmentation_ratio']}"
              f" → statut {analysis['status']} [{analysis['severity']}]")
        print(f"    Gaspillage  : {analysis['wasted_memory_mb']} MB")
        print(f"    Headroom    : {analysis['maxmemory_headroom_pct']} % (vs maxmemory 1 800 MB)")
        print(f"    activedefrag: {analysis['activedefrag_config']['activedefrag']}")
        print(f"    Post-defrag : ratio estimé {analysis['projection_post_defrag']['estimated_ratio']}"
              f" → économie {analysis['projection_post_defrag']['potential_savings_mb']} MB")
        for rec in analysis["recommendations"]:
            print(f"    Recommand.  : {rec[:68]}")
        print()

    # ------------------------------------------------------------------
    # 10. Monitoring metrics
    # ------------------------------------------------------------------
    print("[ 10/12 ] METRIQUES MONITORING")
    print(subsep)

    for category, metrics in MONITORING_METRICS.items():
        print(f"  [{category.upper()}]")
        for metric in metrics:
            print(f"    redis-cli INFO {metric}")
        print()

    print("  Alertes Prometheus recommandées :")
    print("    redis_connected_clients > 1000       → alert ConnectedClientsHigh")
    print("    redis_mem_fragmentation_ratio > 1.5  → alert MemFragmentationCritical")
    print("    redis_keyspace_hit_rate < 0.85       → alert CacheHitRateLow")
    print("    redis_cluster_state != ok            → alert ClusterStateUnhealthy")
    print("    redis_evicted_keys > 0               → alert EvictionStarted")
    print()

    # ------------------------------------------------------------------
    # 11. Docker Compose YAML (extrait)
    # ------------------------------------------------------------------
    print("[ 11/12 ] DOCKER COMPOSE YAML GENERE (extrait)")
    print(subsep)

    compose_yaml = generate_docker_compose_redis_cluster()
    compose_lines = compose_yaml.split("\n")
    print(f"  YAML généré : {len(compose_lines)} lignes")
    print()
    for line in compose_lines[:35]:
        print(f"  {line}")
    print(f"  ... ({len(compose_lines) - 35} lignes supplémentaires — volumes, networks complets)")
    print()

    # ------------------------------------------------------------------
    # 12. Security checklist
    # ------------------------------------------------------------------
    print("[ 12/12 ] CHECKLIST SECURITE REDIS — CSDDD 2024")
    print(subsep)

    all_ok = True
    for check_key, check in SECURITY_CHECKLIST.items():
        status_icon = "OK" if check["status"] in ("OBLIGATOIRE", "RECOMMANDE") else "WARN"
        if check["status"] == "RECOMMANDE":
            priority = "[ RECOMMANDE ]"
        else:
            priority = "[ OBLIGATOIRE ]"
            if status_icon != "OK":
                all_ok = False
        print(f"  {priority} {check['label']}")
        print(f"    Directive : {check['directive']}")
        print()

    sentinel = REDIS_SENTINEL_CONFIG
    print("  Sentinel (mode standalone HA) :")
    print(f"    Sentinels       : {sentinel['sentinels']} instances")
    print(f"    Quorum          : {sentinel['quorum']} (majorité requise pour failover)")
    print(f"    down-after-ms   : {sentinel['down_after_milliseconds']} ms")
    print(f"    failover-timeout: {sentinel['failover_timeout']} ms")
    print(f"    parallel-syncs  : {sentinel['parallel_syncs']}")
    print(f"    Ports Sentinel  : {sentinel['sentinel_ports']}")
    print()

    # ------------------------------------------------------------------
    # Récapitulatif final
    # ------------------------------------------------------------------
    print(separator)
    print("  RECAPITULATIF — REDIS DOCKER SERVICE CAELUMSWARM™")
    print(separator)
    print()
    print("  Infrastructure déployée :")
    print(f"    Redis version      : 7.2-alpine (image Docker officielle)")
    print(f"    Topologie          : 6 noeuds — 3 masters + 3 replicas")
    print(f"    Hash slots         : 16 384 (0-5460 | 5461-10922 | 10923-16383)")
    print(f"    Haute disponibilité: Cross-AZ (eu-west-1a/1b/1c)")
    print(f"    Failover auto      : ~{REDIS_CONFIG_PRODUCTION['cluster_node_timeout']} ms détection")
    print(f"    Memoire par noeud  : 2 GB (maxmemory 1 800 MB)")
    print(f"    Memoire cluster    : {6 * 1800 // 1024:.1f} GB utilisable")
    print()
    print("  Persistence et durabilité :")
    print(f"    RDB snapshots      : 3600/1 — 300/100 — 60/10000")
    print(f"    AOF fsync          : everysec (RPO max 1 seconde)")
    print(f"    AOF RDB preamble   : oui (rewrite rapide)")
    print(f"    Backup S3          : quotidien 2h00, rétention 7j, AES-256")
    print()
    print("  Sécurité :")
    print(f"    TLS                : 1.3 (port 6380)")
    print(f"    mTLS               : oui (tls-auth-clients yes)")
    print(f"    Secrets            : Vault-managed (0 credential en clair)")
    print(f"    ACL                : permissions minimales par rôle applicatif")
    print(f"    Commandes désact.  : FLUSHALL, DEBUG, CONFIG (rename-command)")
    print()
    print("  Observabilité :")
    print(f"    Métriques          : Prometheus via redis_exporter (ports 9121-9126)")
    print(f"    Latence monitor    : seuil {REDIS_CONFIG_PRODUCTION['latency_monitor_threshold']} ms")
    print(f"    Slow log           : >{REDIS_CONFIG_PRODUCTION['slowlog_log_slower_than']} µs")
    print(f"    Catégories metrics : {len(MONITORING_METRICS)} ({', '.join(MONITORING_METRICS.keys())})")
    print()
    print("  Scripts Lua atomiques :")
    for script_name, info in LUA_SCRIPTS.items():
        print(f"    {script_name:<28} — {info['description']}")
    print()
    print(separator)
    print("  Redis Docker Service Agent — PRET")
    print("  Redis 7.2 / 6-node Cluster / Docker / AOF+RDB")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    raise SystemExit(0 if success else 1)
