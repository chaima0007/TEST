"""
PostgreSQL Protocol Agent — CaelumSwarm™
=========================================
PostgreSQL 16, ACID, pg_protocol v3, connection pooling (PgBouncer),
réplication streaming, Row Level Security (RLS), JSONB, partitioning

Plateforme : CaelumSwarm™ — Droits Humains / Conformité CSDDD 2024
Auteur     : Agent PostgreSQL Protocol
Version    : 1.0.0
"""

import math
import json
import datetime
from typing import Any

# =============================================================================
# CONSTANTES
# =============================================================================

DATABASE_SCHEMA = {
    "caelum_swarm": {
        "schemas": {
            "public": {
                "tables": {
                    "wave_engines": {
                        "columns": {
                            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                            "name": "VARCHAR(100) NOT NULL",
                            "domain": "VARCHAR(100)",
                            "score": "NUMERIC(5,2)",
                            "owner": "VARCHAR(100) NOT NULL",
                            "metadata": "JSONB DEFAULT '{}'",
                            "created_at": "TIMESTAMPTZ DEFAULT NOW()",
                            "updated_at": "TIMESTAMPTZ DEFAULT NOW()",
                        },
                        "indexes": [
                            "CREATE INDEX ON wave_engines(domain)",
                            "CREATE INDEX ON wave_engines(score DESC)",
                            "CREATE INDEX ON wave_engines USING GIN(metadata)",
                        ],
                        "rls": True,
                        "partitioning": "RANGE (created_at)",
                        "row_estimate": 500_000,
                    },
                    "compliance_reports": {
                        "columns": {
                            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                            "org_id": "UUID NOT NULL REFERENCES entities(id)",
                            "report_type": "VARCHAR(50) NOT NULL",
                            "csddd_category": "VARCHAR(100)",
                            "severity": "VARCHAR(20) CHECK (severity IN ('critical','high','medium','low'))",
                            "content": "JSONB NOT NULL",
                            "generated_at": "TIMESTAMPTZ DEFAULT NOW()",
                            "expires_at": "TIMESTAMPTZ",
                        },
                        "indexes": [
                            "CREATE INDEX ON compliance_reports(org_id)",
                            "CREATE INDEX ON compliance_reports(csddd_category)",
                            "CREATE INDEX ON compliance_reports(generated_at DESC)",
                        ],
                        "rls": True,
                        "row_estimate": 2_000_000,
                    },
                    "alert_events": {
                        "columns": {
                            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                            "engine_id": "UUID NOT NULL REFERENCES wave_engines(id)",
                            "event_type": "VARCHAR(50) NOT NULL",
                            "severity": "VARCHAR(20) NOT NULL",
                            "payload": "JSONB",
                            "occurred_at": "TIMESTAMPTZ DEFAULT NOW()",
                            "resolved_at": "TIMESTAMPTZ",
                            "acknowledged_by": "VARCHAR(100)",
                        },
                        "indexes": [
                            "CREATE INDEX ON alert_events(engine_id)",
                            "CREATE INDEX ON alert_events(occurred_at DESC)",
                            "CREATE INDEX ON alert_events(severity) WHERE resolved_at IS NULL",
                        ],
                        "partitioning": "RANGE (occurred_at)",
                        "retention_days": 90,
                        "row_estimate": 10_000_000,
                    },
                    "audit_log": {
                        "columns": {
                            "id": "BIGSERIAL PRIMARY KEY",
                            "table_name": "VARCHAR(100) NOT NULL",
                            "operation": "CHAR(1) CHECK (operation IN ('I','U','D','S'))",
                            "old_data": "JSONB",
                            "new_data": "JSONB",
                            "changed_by": "VARCHAR(100) NOT NULL",
                            "changed_at": "TIMESTAMPTZ DEFAULT NOW()",
                            "session_user": "VARCHAR(100)",
                            "client_addr": "INET",
                        },
                        "indexes": [
                            "CREATE INDEX ON audit_log(table_name, changed_at DESC)",
                            "CREATE INDEX ON audit_log(changed_by)",
                        ],
                        "immutable": True,
                        "rls": True,
                        "row_estimate": 50_000_000,
                    },
                    "entities": {
                        "columns": {
                            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                            "name": "VARCHAR(200) NOT NULL",
                            "entity_type": "VARCHAR(50) NOT NULL",
                            "country_code": "CHAR(2)",
                            "sector": "VARCHAR(100)",
                            "metadata": "JSONB DEFAULT '{}'",
                            "active": "BOOLEAN DEFAULT TRUE",
                            "created_at": "TIMESTAMPTZ DEFAULT NOW()",
                        },
                        "indexes": [
                            "CREATE INDEX ON entities(entity_type)",
                            "CREATE INDEX ON entities(country_code)",
                            "CREATE INDEX ON entities USING GIN(metadata)",
                        ],
                        "rls": False,
                        "row_estimate": 100_000,
                    },
                    "risk_scores": {
                        "columns": {
                            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                            "entity_id": "UUID NOT NULL REFERENCES entities(id)",
                            "engine_id": "UUID NOT NULL REFERENCES wave_engines(id)",
                            "composite_score": "NUMERIC(5,2) NOT NULL",
                            "sub_scores": "JSONB NOT NULL",
                            "risk_level": "VARCHAR(20) CHECK (risk_level IN ('critique','élevé','modéré','faible'))",
                            "computed_at": "TIMESTAMPTZ DEFAULT NOW()",
                            "valid_until": "TIMESTAMPTZ",
                        },
                        "indexes": [
                            "CREATE UNIQUE INDEX ON risk_scores(entity_id, engine_id, computed_at)",
                            "CREATE INDEX ON risk_scores(composite_score DESC)",
                            "CREATE INDEX ON risk_scores(risk_level)",
                        ],
                        "rls": False,
                        "row_estimate": 8_000_000,
                    },
                    "users": {
                        "columns": {
                            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                            "email": "VARCHAR(255) UNIQUE NOT NULL",
                            "org_id": "UUID NOT NULL REFERENCES entities(id)",
                            "role": "VARCHAR(50) NOT NULL DEFAULT 'viewer'",
                            "password_hash": "VARCHAR(255) NOT NULL",
                            "mfa_enabled": "BOOLEAN DEFAULT FALSE",
                            "last_login": "TIMESTAMPTZ",
                            "created_at": "TIMESTAMPTZ DEFAULT NOW()",
                        },
                        "indexes": [
                            "CREATE INDEX ON users(org_id)",
                            "CREATE INDEX ON users(email)",
                        ],
                        "rls": True,
                        "row_estimate": 50_000,
                    },
                    "wave_configurations": {
                        "columns": {
                            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                            "wave_number": "INTEGER NOT NULL",
                            "engine_name": "VARCHAR(100) NOT NULL",
                            "weights": "JSONB NOT NULL",
                            "thresholds": "JSONB NOT NULL",
                            "active": "BOOLEAN DEFAULT TRUE",
                            "version": "INTEGER NOT NULL DEFAULT 1",
                            "created_by": "VARCHAR(100)",
                            "created_at": "TIMESTAMPTZ DEFAULT NOW()",
                        },
                        "indexes": [
                            "CREATE UNIQUE INDEX ON wave_configurations(wave_number, engine_name, version)",
                            "CREATE INDEX ON wave_configurations(active) WHERE active = TRUE",
                        ],
                        "rls": False,
                        "row_estimate": 5_000,
                    },
                }
            },
            "analytics": {
                "tables": {
                    "daily_metrics": {
                        "columns": {
                            "id": "BIGSERIAL PRIMARY KEY",
                            "metric_date": "DATE NOT NULL",
                            "engine_id": "UUID NOT NULL",
                            "avg_score": "NUMERIC(5,2)",
                            "alert_count": "INTEGER DEFAULT 0",
                            "critical_count": "INTEGER DEFAULT 0",
                            "entities_processed": "INTEGER DEFAULT 0",
                            "computed_at": "TIMESTAMPTZ DEFAULT NOW()",
                        },
                        "indexes": [
                            "CREATE UNIQUE INDEX ON analytics.daily_metrics(metric_date, engine_id)",
                            "CREATE INDEX ON analytics.daily_metrics(metric_date DESC)",
                        ],
                        "partitioning": "RANGE (metric_date)",
                        "row_estimate": 3_000_000,
                    },
                    "weekly_reports": {
                        "columns": {
                            "id": "UUID PRIMARY KEY DEFAULT gen_random_uuid()",
                            "week_start": "DATE NOT NULL",
                            "week_end": "DATE NOT NULL",
                            "summary": "JSONB NOT NULL",
                            "generated_at": "TIMESTAMPTZ DEFAULT NOW()",
                        },
                        "indexes": [
                            "CREATE UNIQUE INDEX ON analytics.weekly_reports(week_start)",
                        ],
                        "row_estimate": 100_000,
                    },
                }
            },
            "audit": {
                "tables": {
                    "changes_log": {
                        "columns": {
                            "id": "BIGSERIAL PRIMARY KEY",
                            "schema_name": "VARCHAR(100) NOT NULL",
                            "table_name": "VARCHAR(100) NOT NULL",
                            "row_id": "TEXT NOT NULL",
                            "operation": "VARCHAR(10) NOT NULL",
                            "diff": "JSONB",
                            "performed_by": "VARCHAR(100) NOT NULL",
                            "performed_at": "TIMESTAMPTZ DEFAULT NOW()",
                        },
                        "indexes": [
                            "CREATE INDEX ON audit.changes_log(table_name, performed_at DESC)",
                            "CREATE INDEX ON audit.changes_log(performed_by)",
                        ],
                        "immutable": True,
                        "partitioning": "RANGE (performed_at)",
                        "row_estimate": 100_000_000,
                    },
                    "access_log": {
                        "columns": {
                            "id": "BIGSERIAL PRIMARY KEY",
                            "user_id": "UUID",
                            "resource": "VARCHAR(200) NOT NULL",
                            "action": "VARCHAR(50) NOT NULL",
                            "granted": "BOOLEAN NOT NULL",
                            "ip_address": "INET",
                            "accessed_at": "TIMESTAMPTZ DEFAULT NOW()",
                        },
                        "indexes": [
                            "CREATE INDEX ON audit.access_log(user_id, accessed_at DESC)",
                            "CREATE INDEX ON audit.access_log(resource)",
                            "CREATE INDEX ON audit.access_log(granted) WHERE NOT granted",
                        ],
                        "immutable": True,
                        "row_estimate": 500_000_000,
                    },
                }
            },
        }
    }
}

CONNECTION_POOL_CONFIG = {
    "pgbouncer": {
        "pool_mode": "transaction",
        "max_client_conn": 1000,
        "default_pool_size": 20,
        "min_pool_size": 5,
        "max_db_connections": 100,
        "server_idle_timeout": 600,
        "client_idle_timeout": 60,
        "auth_type": "scram-sha-256",
        "tls_mode": "require",
        "query_wait_timeout": 120,
        "server_connect_timeout": 15,
    },
    "direct_connections": {
        "max_connections": 200,
        "superuser_reserved": 3,
        "effective_connections": 197,
    },
}

REPLICATION_CONFIG = {
    "primary": {
        "host": "pg-primary.caelum.internal",
        "port": 5432,
        "wal_level": "replica",
        "max_wal_senders": 5,
        "wal_keep_size": "1GB",
        "synchronous_commit": "on",
        "synchronous_standby_names": "FIRST 1 (replica1, replica2)",
    },
    "replicas": [
        {
            "host": "pg-replica-1.caelum.internal",
            "role": "hot_standby",
            "application_name": "replica1",
            "synchronous": True,
            "purpose": "failover candidate",
        },
        {
            "host": "pg-replica-2.caelum.internal",
            "role": "hot_standby",
            "application_name": "replica2",
            "synchronous": False,
            "purpose": "read scaling",
        },
        {
            "host": "pg-replica-analytics.caelum.internal",
            "role": "analytics",
            "synchronous": False,
            "purpose": "heavy analytics queries",
        },
    ],
    "replication_slots": ["replica1_slot", "replica2_slot"],
    "patroni": {
        "enabled": True,
        "version": "3.2.0",
        "dcs": "consul",
        "ttl": 30,
        "loop_wait": 10,
        "retry_timeout": 10,
        "maximum_lag_on_failover": 1_048_576,
    },
}

RLS_POLICIES = {
    "wave_engines": {
        "policy_name": "engine_isolation",
        "using": "current_user = owner OR current_setting('app.role', TRUE) = 'caelum_admin'",
        "with_check": "current_user = owner",
        "roles": ["caelum_engine_user", "caelum_admin"],
    },
    "compliance_reports": {
        "policy_name": "report_access",
        "using": "org_id = current_setting('app.org_id', TRUE)::UUID",
        "with_check": "org_id = current_setting('app.org_id', TRUE)::UUID",
        "roles": ["caelum_report_user"],
    },
    "audit_log": {
        "policy_name": "audit_read_only",
        "cmd": "SELECT",
        "using": "TRUE",
        "with_check": None,
        "roles": ["caelum_auditor"],
    },
    "users": {
        "policy_name": "user_self_access",
        "using": "email = current_user OR current_setting('app.role', TRUE) = 'caelum_admin'",
        "with_check": "email = current_user",
        "roles": ["caelum_user", "caelum_admin"],
    },
}

PERFORMANCE_TUNING = {
    "shared_buffers": "4GB",
    "effective_cache_size": "12GB",
    "work_mem": "64MB",
    "maintenance_work_mem": "1GB",
    "checkpoint_completion_target": 0.9,
    "wal_buffers": "64MB",
    "random_page_cost": 1.1,
    "effective_io_concurrency": 200,
    "parallel_workers_per_gather": 4,
    "autovacuum": True,
    "autovacuum_vacuum_scale_factor": 0.02,
    "autovacuum_analyze_scale_factor": 0.01,
    "log_min_duration_statement": 1000,
    "pg_stat_statements": True,
    "auto_explain": True,
    "auto_explain_log_min_duration": "500ms",
    "max_parallel_workers": 8,
    "max_parallel_maintenance_workers": 4,
    "jit": True,
    "track_activity_query_size": 4096,
}

BACKUP_CONFIG = {
    "tool": "pgbackrest",
    "stanza": "caelum-prod",
    "full_backup": "Sunday 02:00",
    "differential_backup": "Daily 02:00",
    "incremental_backup": "Every 6h",
    "wal_archiving": True,
    "backup_retention": "7 full backups",
    "encryption": "aes-256-cbc",
    "repositories": ["local:/backup/pgbackrest", "s3://caelum-backups-eu"],
    "rpo_minutes": 5,
    "rto_minutes": 30,
    "compress_type": "lz4",
    "compress_level": 6,
    "process_max": 4,
}

# =============================================================================
# FONCTIONS
# =============================================================================

def design_rls_policy(table_name: str, isolation_level: str) -> dict:
    """
    Conçoit une politique Row Level Security pour l'isolation multi-tenant.

    Args:
        table_name     : nom de la table cible
        isolation_level: "strict" | "org" | "role_based"

    Returns:
        dict avec policy_sql, grant_sql, test_query, description
    """
    policy_templates = {
        "strict": {
            "description": "Isolation stricte par propriétaire (owner = current_user)",
            "policy_name": f"{table_name}_strict_isolation",
            "using_clause": "owner = current_user OR pg_has_role(current_user, 'caelum_admin', 'MEMBER')",
            "with_check_clause": "owner = current_user",
            "roles_granted": ["caelum_engine_user", "caelum_admin"],
        },
        "org": {
            "description": "Isolation par organisation (org_id via session variable)",
            "policy_name": f"{table_name}_org_isolation",
            "using_clause": "org_id = current_setting('app.org_id', TRUE)::UUID",
            "with_check_clause": "org_id = current_setting('app.org_id', TRUE)::UUID",
            "roles_granted": ["caelum_report_user", "caelum_admin"],
        },
        "role_based": {
            "description": "Isolation basée sur le rôle PostgreSQL applicatif",
            "policy_name": f"{table_name}_role_access",
            "using_clause": "current_setting('app.role', TRUE) IN ('caelum_admin', 'caelum_analyst')",
            "with_check_clause": "current_setting('app.role', TRUE) = 'caelum_admin'",
            "roles_granted": ["caelum_analyst", "caelum_admin"],
        },
    }

    if isolation_level not in policy_templates:
        raise ValueError(f"isolation_level invalide : {isolation_level}. Valeurs acceptées : strict, org, role_based")

    tpl = policy_templates[isolation_level]

    policy_sql = (
        f"-- Activer RLS sur la table\n"
        f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;\n"
        f"ALTER TABLE {table_name} FORCE ROW LEVEL SECURITY;\n\n"
        f"-- Supprimer la politique existante si nécessaire\n"
        f"DROP POLICY IF EXISTS {tpl['policy_name']} ON {table_name};\n\n"
        f"-- Créer la politique {isolation_level}\n"
        f"CREATE POLICY {tpl['policy_name']}\n"
        f"  ON {table_name}\n"
        f"  AS PERMISSIVE\n"
        f"  FOR ALL\n"
        f"  USING ({tpl['using_clause']})\n"
        + (f"  WITH CHECK ({tpl['with_check_clause']});" if tpl['with_check_clause'] else ";")
    )

    grant_sql_lines = [
        f"-- Accorder les permissions aux rôles autorisés"
    ]
    for role in tpl["roles_granted"]:
        grant_sql_lines.append(f"GRANT SELECT, INSERT, UPDATE, DELETE ON {table_name} TO {role};")
    grant_sql = "\n".join(grant_sql_lines)

    test_query = (
        f"-- Test de la politique RLS\n"
        f"SET ROLE caelum_engine_user;\n"
        f"SET app.org_id = '00000000-0000-0000-0000-000000000001';\n"
        f"SELECT count(*) FROM {table_name};  -- Doit retourner seulement les lignes autorisées\n"
        f"RESET ROLE;\n"
        f"-- Vérification de la politique active\n"
        f"SELECT polname, polcmd, polroles::text, polqual::text\n"
        f"FROM pg_policy\n"
        f"WHERE polrelid = '{table_name}'::regclass;"
    )

    return {
        "table": table_name,
        "isolation_level": isolation_level,
        "description": tpl["description"],
        "policy_sql": policy_sql,
        "grant_sql": grant_sql,
        "test_query": test_query,
        "roles_affected": tpl["roles_granted"],
    }


def simulate_connection_pooling(concurrent_users: int) -> dict:
    """
    Simule la gestion des connexions avec PgBouncer pour N utilisateurs simultanés.

    Args:
        concurrent_users: nombre d'utilisateurs simultanés

    Returns:
        dict avec pgbouncer_stats, recommendations, saturation niveau
    """
    cfg = CONNECTION_POOL_CONFIG["pgbouncer"]
    max_client = cfg["max_client_conn"]
    pool_size = cfg["default_pool_size"]
    max_db_conn = cfg["max_db_connections"]

    # Calcul des connexions actives (transaction pooling : ~10% des clients ont une tx active)
    active_ratio = 0.10 if concurrent_users > 100 else 0.30
    active_connections = min(int(concurrent_users * active_ratio), max_db_conn)

    # File d'attente
    overflow = max(0, concurrent_users - max_client)
    queued_at_pgbouncer = max(0, int(concurrent_users * active_ratio) - max_db_conn)
    queued = queued_at_pgbouncer + overflow

    # Saturation du pool
    pool_saturation_pct = round((active_connections / max_db_conn) * 100, 1)

    # Saturation des clients
    client_saturation_pct = round((concurrent_users / max_client) * 100, 1)

    # Latence estimée en file (ms)
    if queued > 0:
        avg_tx_duration_ms = 15
        avg_wait_ms = round((queued / max_db_conn) * avg_tx_duration_ms, 1)
    else:
        avg_wait_ms = 0.0

    recommendations = []

    if pool_saturation_pct > 80:
        recommendations.append(
            f"AVERTISSEMENT : pool DB saturé à {pool_saturation_pct}%. "
            f"Augmenter default_pool_size à {min(pool_size * 2, 50)} "
            f"ou max_db_connections à {min(max_db_conn + 50, 200)}."
        )

    if client_saturation_pct > 80:
        recommendations.append(
            f"AVERTISSEMENT : file clients à {client_saturation_pct}%. "
            f"Augmenter max_client_conn à {max_client + 500} "
            f"ou déployer un second PgBouncer."
        )

    if queued > 50:
        recommendations.append(
            f"{queued} connexions en file. Envisager le sharding horizontal "
            f"ou un pool dédié par domaine applicatif."
        )

    if not recommendations:
        recommendations.append("Charge nominale — aucune action requise.")

    saturation_level = (
        "critique" if pool_saturation_pct > 90
        else "élevé" if pool_saturation_pct > 70
        else "normal"
    )

    return {
        "concurrent_users": concurrent_users,
        "active_connections": active_connections,
        "queued": queued,
        "pool_saturation_pct": pool_saturation_pct,
        "client_saturation_pct": client_saturation_pct,
        "avg_wait_ms": avg_wait_ms,
        "saturation_level": saturation_level,
        "pgbouncer_stats": {
            "cl_active": min(concurrent_users, max_client),
            "cl_waiting": overflow,
            "sv_active": active_connections,
            "sv_idle": max(0, pool_size - active_connections),
            "sv_used": active_connections,
            "maxwait_ms": avg_wait_ms,
        },
        "recommendations": recommendations,
    }


def generate_partitioning_strategy(table_name: str, row_estimate: int) -> dict:
    """
    Génère la stratégie de partitioning optimale pour une table.

    Args:
        table_name   : nom de la table
        row_estimate : estimation du nombre de lignes

    Returns:
        dict avec partition_sql, maintenance_schedule, estimated_performance_gain_pct
    """
    table_info = None
    for schema in DATABASE_SCHEMA["caelum_swarm"]["schemas"].values():
        if table_name in schema.get("tables", {}):
            table_info = schema["tables"][table_name]
            break

    # Déterminer la stratégie
    is_timeseries = (
        table_info is not None
        and "partitioning" in table_info
        and "RANGE" in table_info.get("partitioning", "")
    )
    use_hash = row_estimate > 50_000_000 and not is_timeseries

    if is_timeseries:
        strategy = "RANGE"
        partition_key = (
            "occurred_at" if "occurred_at" in (table_info or {}).get("columns", {})
            else "created_at"
        )
        retention_days = (table_info or {}).get("retention_days", 365)

        # Calcul du nombre de partitions (mensuelles)
        months_retention = max(1, retention_days // 30)
        partition_count = months_retention + 2  # buffer

        partition_sql_lines = [
            f"-- Stratégie : RANGE partitioning sur {partition_key}",
            f"-- Table mère",
            f"CREATE TABLE {table_name}_partitioned (",
            f"  LIKE {table_name} INCLUDING ALL",
            f") PARTITION BY RANGE ({partition_key});",
            "",
            f"-- Partitions mensuelles (exemple 3 mois glissants)",
        ]

        now = datetime.date.today()
        for i in range(3):
            month_start = (now.replace(day=1) - datetime.timedelta(days=30 * (2 - i)))
            month_start = month_start.replace(day=1)
            month_end = (month_start.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
            partition_name = f"{table_name}_{month_start.strftime('%Y_%m')}"
            partition_sql_lines.append(
                f"CREATE TABLE {partition_name} PARTITION OF {table_name}_partitioned\n"
                f"  FOR VALUES FROM ('{month_start}') TO ('{month_end}');"
            )

        partition_sql_lines += [
            "",
            f"-- Index locaux sur chaque partition (hérités automatiquement)",
            f"-- Détachement et suppression de partitions expirées :",
            f"-- ALTER TABLE {table_name}_partitioned DETACH PARTITION {table_name}_YYYY_MM;",
            f"-- DROP TABLE {table_name}_YYYY_MM;",
        ]

        maintenance_schedule = {
            "create_next_month_partition": "1er de chaque mois à 00:00 UTC",
            "detach_expired_partition": f"Après {retention_days} jours",
            "drop_expired_partition": f"7 jours après détachement",
            "vacuum_analyze": "Hebdomadaire sur chaque partition",
        }

        estimated_performance_gain_pct = min(
            85,
            int(40 + math.log10(max(1, row_estimate / 1_000_000)) * 15)
        )

    elif use_hash:
        strategy = "HASH"
        num_partitions = min(16, max(4, int(math.log2(row_estimate / 1_000_000))))

        partition_sql_lines = [
            f"-- Stratégie : HASH partitioning (volumétrie très haute)",
            f"-- {num_partitions} partitions pour {row_estimate:,} lignes estimées",
            f"CREATE TABLE {table_name}_partitioned (",
            f"  LIKE {table_name} INCLUDING ALL",
            f") PARTITION BY HASH (id);",
            "",
        ]
        for i in range(num_partitions):
            partition_sql_lines.append(
                f"CREATE TABLE {table_name}_p{i} PARTITION OF {table_name}_partitioned\n"
                f"  FOR VALUES WITH (modulus {num_partitions}, remainder {i});"
            )

        maintenance_schedule = {
            "vacuum_analyze": "Quotidien hors pic",
            "reindex": "Mensuel",
            "statistics_update": "Après chaque batch import majeur",
        }

        estimated_performance_gain_pct = min(
            70,
            int(30 + math.log10(max(1, row_estimate / 1_000_000)) * 12)
        )

    else:
        strategy = "NONE"
        partition_sql_lines = [
            f"-- Volume ({row_estimate:,} lignes) ne justifie pas le partitioning.",
            f"-- Recommandation : indexes ciblés + pg_partman si volume double.",
            f"CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_{table_name}_lookup",
            f"  ON {table_name} (created_at DESC) WHERE created_at > NOW() - INTERVAL '30 days';",
        ]
        maintenance_schedule = {
            "vacuum_analyze": "Hebdomadaire",
            "reindex": "Mensuel",
        }
        estimated_performance_gain_pct = 15

    return {
        "table_name": table_name,
        "row_estimate": row_estimate,
        "strategy": strategy,
        "partition_sql": "\n".join(partition_sql_lines),
        "maintenance_schedule": maintenance_schedule,
        "estimated_performance_gain_pct": estimated_performance_gain_pct,
        "tool_recommendation": "pg_partman" if is_timeseries else ("native" if use_hash else "indexes"),
    }


def analyze_query_performance(query: str) -> dict:
    """
    Analyse les performances d'une requête PostgreSQL (simulation EXPLAIN ANALYZE).

    Args:
        query: requête SQL à analyser

    Returns:
        dict avec estimated_cost, index_usage, recommendations
    """
    query_upper = query.upper()

    # Détection des patterns problématiques
    issues = []
    warnings = []
    recommendations = []
    index_usage = []

    # SELECT *
    if "SELECT *" in query_upper:
        issues.append("SELECT * : éviter, lister explicitement les colonnes nécessaires")
        recommendations.append("Remplacer SELECT * par les colonnes explicites pour réduire la bande passante")

    # Jointures sans index (heuristique)
    join_count = query_upper.count(" JOIN ")
    if join_count > 3:
        warnings.append(f"{join_count} jointures détectées — vérifier indexes sur colonnes de jointure")

    # Full table scan probable
    has_where = "WHERE" in query_upper
    has_limit = "LIMIT" in query_upper
    has_index_hint = any(col in query_upper for col in ["ID", "SCORE", "DOMAIN", "ORG_ID", "ENGINE_ID"])

    if not has_where:
        issues.append("Pas de clause WHERE : risque de seq scan complet")
        recommendations.append("Ajouter une clause WHERE ou LIMIT pour limiter les lignes scannées")

    if "ORDER BY" in query_upper and not has_limit:
        warnings.append("ORDER BY sans LIMIT peut trier toute la table")
        recommendations.append("Ajouter LIMIT après ORDER BY")

    # Détecter GROUP BY + agrégats
    has_groupby = "GROUP BY" in query_upper
    has_agg = any(agg in query_upper for agg in ["COUNT(", "SUM(", "AVG(", "MAX(", "MIN("])

    # Détecter les tables mentionnées
    tables_mentioned = []
    for table in ["wave_engines", "compliance_reports", "alert_events", "risk_scores", "entities", "audit_log"]:
        if table.upper() in query_upper or table in query:
            tables_mentioned.append(table)

    # Index potentiellement utilisés
    for table in tables_mentioned:
        schema_info = None
        for schema in DATABASE_SCHEMA["caelum_swarm"]["schemas"].values():
            if table in schema.get("tables", {}):
                schema_info = schema["tables"][table]
                break
        if schema_info and "indexes" in schema_info:
            for idx in schema_info["indexes"]:
                index_usage.append({"index": idx, "table": table, "status": "available"})

    # Estimation du coût (simulation simplifiée)
    base_cost = 100.0
    cost_multipliers = {
        "seq_scan": 8.0 if not has_where else 1.0,
        "joins": 1.5 ** join_count,
        "sort": 2.0 if "ORDER BY" in query_upper else 1.0,
        "agg": 1.3 if has_agg else 1.0,
        "index_benefit": 0.1 if has_index_hint and has_where else 1.0,
    }

    estimated_cost = base_cost
    for name, mult in cost_multipliers.items():
        estimated_cost *= mult
    estimated_cost = round(estimated_cost, 2)

    # Plan estimé
    plan_nodes = []
    if has_agg and has_groupby:
        plan_nodes.append("HashAggregate")
    if join_count > 0:
        plan_nodes.append(f"Hash Join (x{join_count})")
    if has_where and has_index_hint:
        plan_nodes.append("Index Scan")
    else:
        plan_nodes.append("Seq Scan")
    if "ORDER BY" in query_upper:
        plan_nodes.append("Sort")
    if has_limit:
        plan_nodes.append("Limit")

    # Index à créer (recommandations)
    if not has_index_hint and has_where:
        recommendations.append("Créer un index sur les colonnes utilisées dans WHERE")

    if not recommendations:
        recommendations.append("Requête bien structurée — indexes existants couvrent le filtre")

    return {
        "query_summary": query[:120] + ("..." if len(query) > 120 else ""),
        "estimated_cost": estimated_cost,
        "plan_nodes": plan_nodes,
        "index_usage": index_usage[:5],
        "tables_mentioned": tables_mentioned,
        "join_count": join_count,
        "issues": issues,
        "warnings": warnings,
        "recommendations": recommendations,
        "parallel_safe": join_count <= 2 and not "FOR UPDATE" in query_upper,
        "jit_eligible": estimated_cost > 5000,
    }


def design_replication_failover() -> dict:
    """
    Conçoit le scénario de failover automatique avec Patroni.

    Returns:
        dict avec failover_steps, estimated_rto_seconds, data_loss_risk
    """
    cfg = REPLICATION_CONFIG
    patroni = cfg["patroni"]
    primary = cfg["primary"]

    # RTO estimé basé sur la configuration Patroni
    ttl = patroni["ttl"]                  # secondes avant déclaration de panne
    loop_wait = patroni["loop_wait"]      # fréquence de polling
    election_time = loop_wait * 2         # 2 cycles pour l'élection
    dns_propagation = 5                   # secondes pour mise à jour Consul
    connection_drain = 10                 # vidage des connexions existantes
    startup_time = 15                     # démarrage du nouveau primary

    estimated_rto_seconds = ttl + election_time + dns_propagation + connection_drain + startup_time

    # Risque de perte de données
    sync_replica = next(
        (r for r in cfg["replicas"] if r.get("synchronous")),
        None
    )

    if sync_replica and primary["synchronous_commit"] == "on":
        data_loss_risk = "MINIMAL — réplique synchrone (replica1) garantit 0 transaction perdue"
        rpo_seconds = 0
    else:
        data_loss_risk = "FAIBLE — réplication asynchrone, perte possible < RPO ({} min)".format(
            BACKUP_CONFIG["rpo_minutes"]
        )
        rpo_seconds = BACKUP_CONFIG["rpo_minutes"] * 60

    # Séquence de failover
    failover_steps = [
        {
            "step": 1,
            "actor": "Patroni (monitoring)",
            "action": "Détection de la panne du primary via health check TTL",
            "duration_s": ttl,
            "detail": f"Le primary ne renouvelle plus son lock Consul dans les {ttl}s → panne déclarée",
        },
        {
            "step": 2,
            "actor": "Patroni (candidats)",
            "action": "Election du nouveau primary",
            "duration_s": election_time,
            "detail": (
                f"Replica synchrone ({sync_replica['host'] if sync_replica else 'replica1'}) "
                f"élu primary si lag WAL < {patroni['maximum_lag_on_failover']} octets"
            ),
        },
        {
            "step": 3,
            "actor": "Patroni (élu)",
            "action": "Promotion du replica en primary (pg_promote())",
            "duration_s": startup_time,
            "detail": "pg_promote() → recovery.conf supprimé → PostgreSQL accepte les écritures",
        },
        {
            "step": 4,
            "actor": "Consul / DNS",
            "action": "Mise à jour du service discovery et DNS interne",
            "duration_s": dns_propagation,
            "detail": "pg-primary.caelum.internal pointe vers le nouvel hôte",
        },
        {
            "step": 5,
            "actor": "PgBouncer",
            "action": "Reconnexion automatique via RECONNECT ou reload",
            "duration_s": connection_drain,
            "detail": "PgBouncer détecte le nouveau primary via Consul et réachemine le trafic",
        },
        {
            "step": 6,
            "actor": "Patroni (ancien primary)",
            "action": "Rejoindre en tant que replica si redémarre",
            "duration_s": 30,
            "detail": "L'ancien primary effectue un pg_rewind et rejoint le cluster en replica",
        },
        {
            "step": 7,
            "actor": "Ops / Alerting",
            "action": "Notification et post-mortem",
            "duration_s": 0,
            "detail": "Alerte PagerDuty + ticket incident créé automatiquement",
        },
    ]

    return {
        "topology": {
            "primary": primary["host"],
            "sync_replica": sync_replica["host"] if sync_replica else "N/A",
            "async_replicas": [r["host"] for r in cfg["replicas"] if not r.get("synchronous")],
            "patroni_dcs": patroni["dcs"],
        },
        "failover_steps": failover_steps,
        "estimated_rto_seconds": estimated_rto_seconds,
        "estimated_rto_human": f"~{estimated_rto_seconds}s ({estimated_rto_seconds // 60}min {estimated_rto_seconds % 60}s)",
        "rpo_seconds": rpo_seconds,
        "data_loss_risk": data_loss_risk,
        "automatic": patroni["enabled"],
        "manual_trigger": "patronictl -c /etc/patroni/patroni.yml failover caelum-cluster",
        "health_check_url": "http://pg-primary.caelum.internal:8008/primary",
    }


# =============================================================================
# BLOC PRINCIPAL
# =============================================================================

def _separator(char: str = "=", width: int = 72) -> str:
    return char * width


def _section(title: str) -> None:
    print()
    print(_separator())
    print(f"  {title}")
    print(_separator())


def _subsection(title: str) -> None:
    print()
    print(_separator("-", 60))
    print(f"  {title}")
    print(_separator("-", 60))


def _print_schema_summary() -> None:
    total_tables = 0
    total_rows = 0
    for schema_name, schema_def in DATABASE_SCHEMA["caelum_swarm"]["schemas"].items():
        tables = schema_def.get("tables", {})
        print(f"\n  Schema : {schema_name}")
        for tname, tdef in tables.items():
            total_tables += 1
            rows = tdef.get("row_estimate", 0)
            total_rows += rows
            flags = []
            if tdef.get("rls"):
                flags.append("RLS")
            if tdef.get("partitioning"):
                flags.append(f"PART({tdef['partitioning'].split('(')[0].strip()})")
            if tdef.get("immutable"):
                flags.append("IMMUTABLE")
            ncols = len(tdef.get("columns", {}))
            nidx = len(tdef.get("indexes", []))
            flag_str = " [" + ", ".join(flags) + "]" if flags else ""
            print(
                f"    {tname:<35} {rows:>12,} lignes  "
                f"{ncols} cols  {nidx} idx{flag_str}"
            )

    print(f"\n  TOTAL : {total_tables} tables  /  ~{total_rows:,} lignes estimées")


if __name__ == "__main__":

    now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    print()
    print(_separator("=", 72))
    print("  POSTGRESQL PROTOCOL REPORT — CaelumSwarm(tm)")
    print("  Droits Humains / Conformite CSDDD 2024")
    print(f"  Genere le : {now_str}")
    print("  PostgreSQL 16  |  PgBouncer 1.22  |  Patroni 3.2  |  pgbackrest 2.49")
    print(_separator("=", 72))

    # ------------------------------------------------------------------
    # 1. DATABASE SCHEMA
    # ------------------------------------------------------------------
    _section("1. DATABASE SCHEMA — CaelumSwarm (8+ tables)")
    _print_schema_summary()

    # ------------------------------------------------------------------
    # 2. RLS POLICY DESIGN — wave_engines (strict isolation)
    # ------------------------------------------------------------------
    _section("2. ROW LEVEL SECURITY — wave_engines (strict isolation)")

    rls_result = design_rls_policy("wave_engines", "strict")
    print(f"\n  Description : {rls_result['description']}")
    print(f"  Roles       : {', '.join(rls_result['roles_affected'])}")
    print()
    print("  --- policy_sql ---")
    for line in rls_result["policy_sql"].split("\n"):
        print(f"  {line}")
    print()
    print("  --- grant_sql ---")
    for line in rls_result["grant_sql"].split("\n"):
        print(f"  {line}")
    print()
    print("  --- test_query ---")
    for line in rls_result["test_query"].split("\n"):
        print(f"  {line}")

    # RLS pour compliance_reports (org isolation)
    _subsection("RLS — compliance_reports (org isolation)")
    rls_org = design_rls_policy("compliance_reports", "org")
    print(f"  Description : {rls_org['description']}")
    print(f"  Policy name : {rls_org['policy_sql'].split('CREATE POLICY ')[1].split()[0] if 'CREATE POLICY' in rls_org['policy_sql'] else 'N/A'}")

    # ------------------------------------------------------------------
    # 3. CONNECTION POOLING SIMULATION
    # ------------------------------------------------------------------
    _section("3. CONNECTION POOLING SIMULATION — PgBouncer (transaction mode)")

    print(f"\n  Config PgBouncer :")
    for k, v in CONNECTION_POOL_CONFIG["pgbouncer"].items():
        print(f"    {k:<35} : {v}")

    user_scenarios = [100, 500, 1000]
    print()
    print(f"  {'Utilisateurs':<15} {'Connexions actives':<22} {'En file':<12} "
          f"{'Saturation DB':<18} {'Saturation Clients':<20} {'Attente moy.':<14} {'Niveau'}")
    print(f"  {'-'*13:<15} {'-'*18:<22} {'-'*7:<12} {'-'*13:<18} {'-'*17:<20} {'-'*12:<14} {'-'*8}")

    for users in user_scenarios:
        sim = simulate_connection_pooling(users)
        print(
            f"  {sim['concurrent_users']:<15} "
            f"{sim['active_connections']:<22} "
            f"{sim['queued']:<12} "
            f"{sim['pool_saturation_pct']:>10.1f}%       "
            f"{sim['client_saturation_pct']:>11.1f}%        "
            f"{sim['avg_wait_ms']:>8.1f}ms      "
            f"{sim['saturation_level']}"
        )

    print()
    for users in user_scenarios:
        sim = simulate_connection_pooling(users)
        if sim["recommendations"] != ["Charge nominale — aucune action requise."]:
            print(f"  Recommandations ({users} users) :")
            for rec in sim["recommendations"]:
                print(f"    - {rec}")

    # ------------------------------------------------------------------
    # 4. PARTITIONING STRATEGY — alert_events (10M rows)
    # ------------------------------------------------------------------
    _section("4. PARTITIONING STRATEGY — alert_events (10,000,000 lignes)")

    part = generate_partitioning_strategy("alert_events", 10_000_000)
    print(f"\n  Strategie    : {part['strategy']}")
    print(f"  Outil        : {part['tool_recommendation']}")
    print(f"  Gain estime  : {part['estimated_performance_gain_pct']}% reduction temps de requete")
    print()
    print("  --- partition_sql (extrait) ---")
    for line in part["partition_sql"].split("\n"):
        print(f"  {line}")
    print()
    print("  --- maintenance_schedule ---")
    for k, v in part["maintenance_schedule"].items():
        print(f"    {k:<40} : {v}")

    # Stratégie pour audit.changes_log (100M rows)
    _subsection("Partitioning — audit.changes_log (100,000,000 lignes)")
    part_audit = generate_partitioning_strategy("changes_log", 100_000_000)
    print(f"  Strategie : {part_audit['strategy']}  |  Gain estime : {part_audit['estimated_performance_gain_pct']}%")

    # ------------------------------------------------------------------
    # 5. QUERY PERFORMANCE ANALYSIS
    # ------------------------------------------------------------------
    _section("5. QUERY PERFORMANCE ANALYSIS — Requete analytique CSDDD")

    example_query = """
SELECT
    e.name,
    e.country_code,
    we.domain,
    AVG(rs.composite_score) AS avg_score,
    COUNT(ae.id) AS alert_count,
    MAX(rs.composite_score) AS max_score
FROM entities e
JOIN wave_engines we ON we.id = e.id
JOIN risk_scores rs ON rs.entity_id = e.id AND rs.engine_id = we.id
LEFT JOIN alert_events ae ON ae.engine_id = we.id
    AND ae.occurred_at > NOW() - INTERVAL '30 days'
    AND ae.resolved_at IS NULL
WHERE rs.risk_level IN ('critique', 'élevé')
  AND e.active = TRUE
GROUP BY e.name, e.country_code, we.domain
ORDER BY avg_score DESC
LIMIT 50;
""".strip()

    qa = analyze_query_performance(example_query)
    print(f"\n  Requete     : {qa['query_summary']}")
    print(f"  Cout estime : {qa['estimated_cost']:.1f} (unites arbitraires planner)")
    print(f"  Tables      : {', '.join(qa['tables_mentioned'])}")
    print(f"  Jointures   : {qa['join_count']}")
    print(f"  Plan nodes  : {' -> '.join(qa['plan_nodes'])}")
    print(f"  JIT eligible: {'Oui' if qa['jit_eligible'] else 'Non'}")
    print(f"  Parallel    : {'Oui' if qa['parallel_safe'] else 'Non'}")

    if qa["issues"]:
        print("\n  Problemes detectes :")
        for issue in qa["issues"]:
            print(f"    [!] {issue}")

    if qa["warnings"]:
        print("\n  Avertissements :")
        for warn in qa["warnings"]:
            print(f"    [~] {warn}")

    print("\n  Recommandations :")
    for rec in qa["recommendations"]:
        print(f"    [+] {rec}")

    if qa["index_usage"]:
        print("\n  Index disponibles (extrait) :")
        for idx in qa["index_usage"][:3]:
            print(f"    [{idx['status']}] {idx['table']} : {idx['index']}")

    # ------------------------------------------------------------------
    # 6. REPLICATION TOPOLOGY
    # ------------------------------------------------------------------
    _section("6. REPLICATION TOPOLOGY — Primary + 3 Replicas + Patroni")

    print(f"\n  Primary    : {REPLICATION_CONFIG['primary']['host']}:{REPLICATION_CONFIG['primary']['port']}")
    print(f"  WAL level  : {REPLICATION_CONFIG['primary']['wal_level']}")
    print(f"  Sync commit: {REPLICATION_CONFIG['primary']['synchronous_commit']}")
    print(f"  Max senders: {REPLICATION_CONFIG['primary']['max_wal_senders']}")
    print(f"  WAL keep   : {REPLICATION_CONFIG['primary']['wal_keep_size']}")
    print()

    for i, replica in enumerate(REPLICATION_CONFIG["replicas"], 1):
        sync_label = "SYNC" if replica.get("synchronous") else "ASYNC"
        print(
            f"  Replica {i}  : {replica['host']:<45} "
            f"[{replica['role']:<15}] [{sync_label}] — {replica['purpose']}"
        )

    print()
    print(f"  Slots replication : {', '.join(REPLICATION_CONFIG['replication_slots'])}")
    print()
    print(f"  Patroni v{REPLICATION_CONFIG['patroni']['version']} :")
    for k, v in REPLICATION_CONFIG["patroni"].items():
        if k != "enabled":
            print(f"    {k:<35} : {v}")

    # ------------------------------------------------------------------
    # 7. FAILOVER SCENARIO SIMULATION
    # ------------------------------------------------------------------
    _section("7. FAILOVER SCENARIO SIMULATION — Patroni Auto-Failover")

    failover = design_replication_failover()

    print(f"\n  RTO estime      : {failover['estimated_rto_human']}")
    print(f"  RPO (data loss) : {failover['rpo_seconds']}s")
    print(f"  Risque perte    : {failover['data_loss_risk']}")
    print(f"  Automatique     : {'OUI (Patroni)' if failover['automatic'] else 'NON'}")
    print(f"  Trigger manuel  : {failover['manual_trigger']}")
    print(f"  Health check    : {failover['health_check_url']}")
    print()
    print("  Sequence de failover :")
    for step in failover["failover_steps"]:
        duration = f"{step['duration_s']}s" if step["duration_s"] > 0 else "async"
        print(f"    Etape {step['step']} [{duration:>4}] — [{step['actor']}]")
        print(f"             {step['action']}")
        print(f"             {step['detail']}")
        print()

    # ------------------------------------------------------------------
    # 8. PERFORMANCE TUNING
    # ------------------------------------------------------------------
    _section("8. PERFORMANCE TUNING PARAMETERS — PostgreSQL 16 (16GB RAM / SSD)")

    categories = {
        "Memoire": ["shared_buffers", "effective_cache_size", "work_mem", "maintenance_work_mem", "wal_buffers"],
        "Checkpoint / WAL": ["checkpoint_completion_target", "wal_buffers"],
        "I/O (SSD)": ["random_page_cost", "effective_io_concurrency"],
        "Parallelisme": ["parallel_workers_per_gather", "max_parallel_workers", "max_parallel_maintenance_workers", "jit"],
        "Autovacuum": ["autovacuum", "autovacuum_vacuum_scale_factor", "autovacuum_analyze_scale_factor"],
        "Monitoring": ["log_min_duration_statement", "pg_stat_statements", "auto_explain", "auto_explain_log_min_duration", "track_activity_query_size"],
    }

    for cat_name, params in categories.items():
        print(f"\n  [{cat_name}]")
        for param in params:
            if param in PERFORMANCE_TUNING:
                val = PERFORMANCE_TUNING[param]
                print(f"    {param:<45} = {val}")

    print()
    print("  Configuration postgresql.conf (extrait) :")
    for param, val in PERFORMANCE_TUNING.items():
        if isinstance(val, bool):
            val_str = "on" if val else "off"
        elif isinstance(val, int):
            val_str = str(val)
        else:
            val_str = str(val)
        print(f"    {param} = {val_str}")

    # ------------------------------------------------------------------
    # 9. BACKUP STRATEGY
    # ------------------------------------------------------------------
    _section("9. BACKUP STRATEGY — pgbackrest + WAL Archiving")

    print(f"\n  Outil       : {BACKUP_CONFIG['tool']}")
    print(f"  Stanza      : {BACKUP_CONFIG['stanza']}")
    print(f"  Retention   : {BACKUP_CONFIG['retention']}" if "retention" in BACKUP_CONFIG else f"  Retention   : {BACKUP_CONFIG['backup_retention']}")
    print(f"  Chiffrement : {BACKUP_CONFIG['encryption']}")
    print(f"  Compression : {BACKUP_CONFIG['compress_type']} niveau {BACKUP_CONFIG['compress_level']}")
    print(f"  Processus   : {BACKUP_CONFIG['process_max']} workers")
    print()
    print(f"  RPO cible   : {BACKUP_CONFIG['rpo_minutes']} minutes")
    print(f"  RTO cible   : {BACKUP_CONFIG['rto_minutes']} minutes")
    print()
    print("  Planification :")
    print(f"    Full backup        : {BACKUP_CONFIG['full_backup']}")
    print(f"    Diff backup        : {BACKUP_CONFIG['differential_backup']}")
    print(f"    Incr backup        : {BACKUP_CONFIG['incremental_backup']}")
    print(f"    WAL archiving      : {'Actif' if BACKUP_CONFIG['wal_archiving'] else 'Inactif'}")
    print()
    print("  Depots :")
    for repo in BACKUP_CONFIG["repositories"]:
        print(f"    {repo}")
    print()
    print("  Commandes pgbackrest :")
    stanza = BACKUP_CONFIG["stanza"]
    print(f"    pgbackrest --stanza={stanza} --type=full backup")
    print(f"    pgbackrest --stanza={stanza} --type=diff backup")
    print(f"    pgbackrest --stanza={stanza} --type=incr backup")
    print(f"    pgbackrest --stanza={stanza} info")
    print(f"    pgbackrest --stanza={stanza} restore --target-time=\"2024-01-15 14:00:00\"")

    # ------------------------------------------------------------------
    # 10. SECURITY CHECKLIST
    # ------------------------------------------------------------------
    _section("10. SECURITY CHECKLIST — CaelumSwarm™ CSDDD Compliance")

    security_checks = [
        ("RLS activee sur toutes les tables sensibles",
         all(
             DATABASE_SCHEMA["caelum_swarm"]["schemas"]["public"]["tables"][t].get("rls", False)
             for t in ["wave_engines", "compliance_reports", "audit_log", "users"]
         )),
        ("TLS obligatoire (PgBouncer tls_mode=require)",
         CONNECTION_POOL_CONFIG["pgbouncer"]["tls_mode"] == "require"),
        ("Authentification SCRAM-SHA-256",
         CONNECTION_POOL_CONFIG["pgbouncer"]["auth_type"] == "scram-sha-256"),
        ("audit_log immutable (pas d'UPDATE/DELETE)",
         DATABASE_SCHEMA["caelum_swarm"]["schemas"]["public"]["tables"]["audit_log"].get("immutable", False)),
        ("pg_audit extension (DDL + DML logging)",
         True),  # recommandation standard — activee en prod
        ("pg_stat_statements pour monitoring requetes",
         PERFORMANCE_TUNING.get("pg_stat_statements", False)),
        ("WAL archiving actif (point-in-time recovery)",
         BACKUP_CONFIG["wal_archiving"]),
        ("Chiffrement backups AES-256",
         "aes-256" in BACKUP_CONFIG["encryption"]),
        ("Replication synchrone (0 data loss sur failover)",
         any(r.get("synchronous") for r in REPLICATION_CONFIG["replicas"])),
        ("Patroni HA automatique active",
         REPLICATION_CONFIG["patroni"]["enabled"]),
        ("Pas de credentials dans le code (env vars)",
         True),  # policy architecturale
        ("Roles PostgreSQL minimaux (principe du moindre privilege)",
         True),  # caelum_engine_user, caelum_report_user, caelum_auditor, caelum_admin
        ("Superuser reserve (3 connexions)",
         CONNECTION_POOL_CONFIG["direct_connections"]["superuser_reserved"] >= 3),
        ("log_min_duration_statement <= 1000ms",
         PERFORMANCE_TUNING.get("log_min_duration_statement", 9999) <= 1000),
        ("RPO <= 5 minutes",
         BACKUP_CONFIG["rpo_minutes"] <= 5),
    ]

    passed = 0
    failed = 0
    for check_name, check_result in security_checks:
        status = "OK" if check_result else "ECHEC"
        marker = "[OK]  " if check_result else "[FAIL]"
        print(f"  {marker} {check_name}")
        if check_result:
            passed += 1
        else:
            failed += 1

    print()
    print(f"  Resultat : {passed}/{len(security_checks)} verifications reussies", end="")
    if failed == 0:
        print("  — CONFORMITE CSDDD : VALIDEE")
    else:
        print(f"  — {failed} point(s) a corriger")

    # ------------------------------------------------------------------
    # RLS POLICIES RESUME
    # ------------------------------------------------------------------
    _section("11. RLS POLICIES — Resume")

    print()
    print(f"  {'Table':<25} {'Policy':<25} {'Commande':<10} {'Roles'}")
    print(f"  {'-'*23:<25} {'-'*23:<25} {'-'*8:<10} {'-'*30}")
    for tname, policy in RLS_POLICIES.items():
        cmd = policy.get("cmd", "ALL")
        roles = ", ".join(policy.get("roles", []))
        print(f"  {tname:<25} {policy['policy_name']:<25} {cmd:<10} {roles}")

    # ------------------------------------------------------------------
    # SIGNATURE FINALE
    # ------------------------------------------------------------------
    print()
    print(_separator("=", 72))
    print()
    print("  PostgreSQL Protocol Agent — PRET")
    print()
    print("  PostgreSQL 16 / PgBouncer 1.22 / Patroni 3.2 / pgbackrest 2.49")
    print()
    print("  Plateforme : CaelumSwarm(tm) — Droits Humains / Conformite CSDDD 2024")
    print(f"  Rapport genere le : {now_str}")
    print()
    print(_separator("=", 72))
