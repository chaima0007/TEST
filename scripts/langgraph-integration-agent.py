"""
LangGraph Integration Agent — CaelumSwarm™
Framework: LangGraph 0.2.x (de LangChain)
Role: Graphes d'états pour workflows conformité CSDDD 2024 avec cycles et conditions
Pattern: StateGraph, nodes, edges, conditions, checkpointing, human-in-the-loop
"""

import datetime
import hashlib
import json
import secrets

# ---------------------------------------------------------------------------
# Constantes de données
# ---------------------------------------------------------------------------

LANGGRAPH_VERSION = "0.2.x"

COMPLIANCE_STATE_GRAPH = {
    "name": "caelum_compliance_workflow",
    "state_schema": {
        "entity_name": "str",
        "domain": "str",
        "documents": "List[str]",
        "risk_scores": "Dict[str, float]",
        "compliance_level": "Literal['critique', 'élevé', 'modéré', 'faible']",
        "legal_review_required": "bool",
        "human_approval_required": "bool",
        "report_draft": "str",
        "report_approved": "bool",
        "alerts_sent": "List[str]",
        "iteration_count": "int",
        "errors": "List[str]",
    },
    "nodes": {
        "document_loader": {"description": "Charge les documents fournisseur (PDF, CSV, API)"},
        "risk_analyzer": {"description": "Analyse le risque avec wave engine CaelumSwarm™"},
        "legal_reviewer": {"description": "Valide la conformité CSDDD Art.8-13"},
        "human_checkpoint": {"description": "Pause pour validation humaine si score critique"},
        "report_generator": {"description": "Génère le rapport PDF conformité"},
        "alert_dispatcher": {"description": "Dispatche les alertes via NATS/RabbitMQ"},
        "score_validator": {"description": "Vérifie la distribution 4/2/1/1 et composite_score"},
        "remediation_planner": {"description": "Génère plan d'action correctif CSDDD Art.9"},
        "blockchain_recorder": {"description": "Enregistre audit trail immuable"},
        "notifier": {"description": "Notifie les parties prenantes"},
        "END": {"description": "État terminal — workflow terminé"},
    },
    "edges": {
        "conditional_edges": {
            "risk_analyzer → ?": {
                "condition": "state['compliance_level']",
                "critique": "legal_reviewer",
                "élevé": "legal_reviewer",
                "modéré": "report_generator",
                "faible": "report_generator",
            },
            "legal_reviewer → ?": {
                "condition": "state['human_approval_required']",
                "True": "human_checkpoint",
                "False": "report_generator",
            },
            "human_checkpoint → ?": {
                "condition": "state['report_approved']",
                "True": "alert_dispatcher",
                "False": "risk_analyzer",   # CYCLE: re-analyze si refusé
            },
            "score_validator → ?": {
                "condition": "state['iteration_count'] < 3 and not valid_distribution",
                "True": "risk_analyzer",    # CYCLE: retry si distribution invalide
                "False": "report_generator",
            },
        },
        "unconditional_edges": {
            "document_loader → risk_analyzer": "toujours",
            "report_generator → alert_dispatcher": "toujours",
            "alert_dispatcher → blockchain_recorder": "toujours",
            "blockchain_recorder → notifier": "toujours",
            "notifier → END": "toujours",
        },
    },
    "entry_point": "document_loader",
    "checkpointing": {
        "enabled": True,
        "backend": "PostgresSaver",    # persist state dans PostgreSQL
        "thread_id": "entity_audit_{entity_name}_{timestamp}",
        "description": "Permet de reprendre un workflow interrompu",
    },
    "interrupt_before": ["human_checkpoint"],  # pause avant validation humaine
}

ALERT_RESPONSE_GRAPH = {
    "name": "caelum_alert_response",
    "state_schema": {
        "alert_id": "str",
        "severity": "str",
        "source_domain": "str",
        "entity_affected": "str",
        "triage_result": "dict",
        "escalation_level": "int",
        "response_actions": "List[str]",
        "resolved": "bool",
    },
    "nodes": {
        "alert_receiver": "Reçoit et valide l'alerte entrante",
        "triage_classifier": "Classifie la sévérité et route vers équipe",
        "impact_assessor": "Évalue l'impact sur la chaîne de valeur",
        "escalation_manager": "Gère les escalades selon sévérité",
        "action_executor": "Exécute les actions correctives automatisées",
        "resolution_verifier": "Vérifie que l'alerte est résolue",
        "post_mortem_recorder": "Documente l'incident pour audit CSDDD",
    },
    "special_patterns": {
        "parallel_execution": "alert_receiver → [triage_classifier, impact_assessor] en parallèle (Send API)",
        "retry_with_backoff": "resolution_verifier → action_executor (si non résolu, max 3 tentatives)",
        "dynamic_routing": "escalation_manager → route dynamique selon org_size × severity × legal_risk",
    },
}

SUBGRAPHS = {
    "supplier_audit_subgraph": {
        "description": "Sous-graphe réutilisable pour l'audit d'un fournisseur unique",
        "inputs": ["supplier_id", "domains_to_audit"],
        "outputs": ["audit_report", "risk_score", "recommended_actions"],
        "reused_in": ["compliance_workflow", "supply_chain_mapping"],
    },
    "document_processing_subgraph": {
        "description": "RAG pipeline pour analyser les documents fournisseur",
        "nodes": ["loader", "splitter", "embedder", "retriever", "summarizer"],
    },
}

LANGGRAPH_PLATFORM_CONFIG = {
    "deployment": "LangGraph Platform (cloud)",
    "api_endpoint": "https://caelum-langgraph.langchain.com",
    "crons": [
        {"schedule": "0 6 * * *", "graph": "caelum_compliance_workflow", "input": "daily_batch"},
        {"schedule": "*/15 * * * *", "graph": "caelum_alert_response", "trigger": "polling"},
    ],
    "streaming": True,        # stream les tokens + events
    "interrupt_points": ["human_checkpoint"],
    "persistence": "postgresql://caelum.internal:5432/langgraph",
    "memory_store": "InMemoryStore + PostgresSaver",
    "auth": "OAuth2 + API Key (Vault managed)",
}

GRAPH_PATTERNS = {
    "agent_loop": {
        "description": "LLM → Tools → LLM cycle (ReAct pattern)",
        "nodes": ["agent", "tools"],
        "edges": {
            "agent → tools": "si tool_calls present",
            "tools → agent": "toujours",
            "agent → END": "si pas de tool_calls",
        },
    },
    "multi_agent_supervisor": {
        "description": "Superviseur qui route entre sous-agents spécialisés",
        "supervisor_llm": "claude-sonnet-4-6",
        "workers": ["compliance_agent", "legal_agent", "report_agent"],
        "routing": "LLM choisit le bon agent selon la tâche",
    },
    "reflection": {
        "description": "Agent génère → critique → améliore (max N iterations)",
        "nodes": ["generate", "reflect", "revise"],
        "termination": "reflection approves OR max_iterations=3",
    },
    "plan_and_execute": {
        "description": "Planifie d'abord, exécute ensuite",
        "nodes": ["planner", "executor", "replanner"],
        "use_case": "Audit complet multi-domaines planifié avant exécution",
    },
    "human_in_the_loop": {
        "description": "Pause workflow pour approbation humaine",
        "interrupt_before": "human_checkpoint",
        "resume": "graph.invoke(null, {'configurable': {'thread_id': '...'}}) après approbation",
        "timeout_hours": 24,
    },
}

SECURITY_CONFIG = {
    "state_isolation": {
        "thread_scoping": "Chaque thread_id dispose d'un état isolé — aucune fuite inter-workflows",
        "state_encryption": "État chiffré au repos dans PostgresSaver (AES-256)",
        "state_signing": "Checkpoints signés HMAC-SHA256 pour détection de tampering",
        "tenant_isolation": "Préfixe entity_name dans thread_id — ségrégation multi-tenant",
    },
    "checkpoint_auth": {
        "backend_creds": "PostgreSQL credentials via Vault — jamais en clair dans le code",
        "ssl_mode": "require",
        "connection_pool": "max_connections=20, pool_timeout=30s",
        "read_only_replica": "Checkpoints lisibles sur réplica RO — écriture sur primaire uniquement",
    },
    "interrupt_auth": {
        "human_checkpoint_auth": "OAuth2 Bearer Token requis pour reprendre un thread interrompu",
        "approval_audit_log": "Chaque approbation/refus loggée avec user_id + timestamp + justification",
        "timeout_policy": "Thread expiré après 24h sans approbation → alerte + archivage automatique",
        "mfa_required": "MFA obligatoire pour approuver les workflows critique",
    },
    "api_security": {
        "langgraph_platform_auth": "OAuth2 + API Key (rotation automatique 90 jours)",
        "webhook_signing": "X-LangGraph-Signature : HMAC-SHA256 sur le payload",
        "rate_limiting": "100 req/min par api_key, 10 interrupts/min par user",
        "ip_allowlist": "Endpoints LangGraph Platform accessibles depuis VPN Caelum uniquement",
    },
}

NODE_EXECUTION_STATS = {
    "document_loader":    {"avg_duration_ms": 250,  "error_rate_pct": 1.2,  "retry_policy": "2 attempts"},
    "risk_analyzer":      {"avg_duration_ms": 1800, "error_rate_pct": 0.5,  "retry_policy": "3 attempts"},
    "legal_reviewer":     {"avg_duration_ms": 3200, "error_rate_pct": 0.8,  "retry_policy": "2 attempts"},
    "human_checkpoint":   {"avg_duration_ms": None, "error_rate_pct": 0.0,  "retry_policy": "N/A — attente humaine"},
    "report_generator":   {"avg_duration_ms": 4500, "error_rate_pct": 1.5,  "retry_policy": "2 attempts"},
    "alert_dispatcher":   {"avg_duration_ms": 120,  "error_rate_pct": 2.1,  "retry_policy": "5 attempts + DLQ"},
    "score_validator":    {"avg_duration_ms": 80,   "error_rate_pct": 0.3,  "retry_policy": "1 attempt"},
    "remediation_planner":{"avg_duration_ms": 2100, "error_rate_pct": 0.7,  "retry_policy": "2 attempts"},
    "blockchain_recorder":{"avg_duration_ms": 350,  "error_rate_pct": 0.4,  "retry_policy": "3 attempts"},
    "notifier":           {"avg_duration_ms": 90,   "error_rate_pct": 1.8,  "retry_policy": "3 attempts"},
}


# ---------------------------------------------------------------------------
# Fonctions
# ---------------------------------------------------------------------------

def design_state_graph(workflow_name: str, nodes: list, has_cycles: bool) -> dict:
    """
    Conçoit un StateGraph LangGraph pour un workflow CaelumSwarm™.

    Paramètres
    ----------
    workflow_name : str
        Nom du graphe (ex. "caelum_compliance_workflow").
    nodes : list
        Liste de noms de nœuds à inclure dans le graphe.
    has_cycles : bool
        True si le graphe contient des cycles (human-in-the-loop, retry, etc.).

    Retourne
    --------
    dict avec :
        graph_definition   – structure complète du StateGraph (dict)
        edges_map          – mapping source → destination avec conditions (dict)
        entry_point        – nœud d'entrée (str)
        checkpointing_config – configuration PostgresSaver (dict)
    """
    # Construire les edges à partir des nœuds fournis
    edges_map: dict = {}
    for i, node in enumerate(nodes):
        if i < len(nodes) - 1:
            next_node = nodes[i + 1]
            # Nœuds qui génèrent des edges conditionnels
            if node in ("risk_analyzer", "legal_reviewer", "human_checkpoint", "score_validator"):
                edges_map[node] = {
                    "type": "conditional",
                    "condition_fn": f"route_from_{node}",
                    "possible_targets": [next_node, nodes[i - 1] if i > 0 and has_cycles else next_node],
                }
            else:
                edges_map[node] = {
                    "type": "unconditional",
                    "target": next_node,
                }

    # Nœud terminal
    if nodes:
        edges_map[nodes[-1]] = {"type": "unconditional", "target": "END"}

    graph_definition = {
        "name": workflow_name,
        "framework": f"LangGraph {LANGGRAPH_VERSION}",
        "class": "StateGraph",
        "node_count": len(nodes),
        "nodes": {n: {"type": "function_node", "async": True} for n in nodes},
        "has_cycles": has_cycles,
        "cycle_guard": "iteration_count < 3" if has_cycles else None,
        "parallel_nodes": [],  # nodes pouvant s'exécuter en parallèle via Send API
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    }

    # Nœuds parallélisables détectés
    if "triage_classifier" in nodes and "impact_assessor" in nodes:
        graph_definition["parallel_nodes"] = ["triage_classifier", "impact_assessor"]

    entry_point = nodes[0] if nodes else "document_loader"

    checkpointing_config = {
        "enabled": True,
        "backend": "PostgresSaver",
        "dsn": "postgresql://caelum.internal:5432/langgraph",
        "ssl_mode": "require",
        "thread_id_pattern": f"{{entity_name}}_{{domain}}_{workflow_name}_{{timestamp}}",
        "checkpoint_ns": workflow_name,
        "resume_supported": True,
        "ttl_days": 90,
        "notes": "Permet de reprendre un workflow interrompu après timeout ou refus humain.",
    }

    return {
        "graph_definition": graph_definition,
        "edges_map": edges_map,
        "entry_point": entry_point,
        "checkpointing_config": checkpointing_config,
    }


def simulate_graph_execution(graph_name: str, initial_state: dict) -> dict:
    """
    Simule l'exécution d'un graphe LangGraph avec états intermédiaires.

    Paramètres
    ----------
    graph_name    : str  – Nom du graphe à simuler (ex. "caelum_compliance_workflow").
    initial_state : dict – État initial du workflow (entity_name, domain, etc.).

    Retourne
    --------
    dict avec :
        execution_trace – liste d'états intermédiaires (list)
        nodes_visited   – nœuds exécutés dans l'ordre (list)
        cycles_count    – nombre de cycles effectués (int)
        final_state     – état final après exécution complète (dict)
    """
    entity   = initial_state.get("entity_name", "Unknown Entity")
    domain   = initial_state.get("domain", "unknown")
    # Score déterministe basé sur entity + domain
    seed_val = int(hashlib.md5(f"{entity}{domain}".encode()).hexdigest()[:6], 16)
    composite_score = round(55.0 + (seed_val % 30), 2)  # entre 55 et 84

    # Déterminer le niveau de conformité selon composite_score
    if composite_score >= 60:
        compliance_level = "critique"
    elif composite_score >= 40:
        compliance_level = "élevé"
    elif composite_score >= 20:
        compliance_level = "modéré"
    else:
        compliance_level = "faible"

    human_approval_required = compliance_level in ("critique", "élevé")
    legal_review_required   = compliance_level in ("critique", "élevé")

    # Construire la trace d'exécution pas à pas
    now = datetime.datetime.utcnow()

    def _ts(offset_ms: int) -> str:
        return (now + datetime.timedelta(milliseconds=offset_ms)).isoformat() + "Z"

    t = 0
    execution_trace = []
    nodes_visited: list = []
    cycles_count = 0

    def _step(node: str, duration_ms: int, state_patch: dict, note: str = "") -> None:
        nonlocal t
        execution_trace.append({
            "step": len(execution_trace) + 1,
            "node": node,
            "started_at": _ts(t),
            "duration_ms": duration_ms,
            "state_patch": state_patch,
            "note": note,
        })
        nodes_visited.append(node)
        t += duration_ms

    # Étape 1 : document_loader
    _step("document_loader", 250, {
        "documents": [
            f"{entity}_sustainability_report_2024.pdf",
            f"{entity}_supplier_contracts.csv",
            f"{entity}_audit_trail_2023.json",
        ],
        "iteration_count": 0,
        "errors": [],
    }, "Chargement 3 documents fournisseur")

    # Étape 2 : risk_analyzer
    risk_scores = {
        "forced_labor_index":       round(composite_score * 0.85 + seed_val % 5, 2),
        "child_labor_index":        round(composite_score * 0.70 + seed_val % 8, 2),
        "environmental_damage_idx": round(composite_score * 0.60 + seed_val % 6, 2),
        "supply_chain_opacity_idx": round(composite_score * 0.75 + seed_val % 4, 2),
    }
    _step("risk_analyzer", 1800, {
        "risk_scores": risk_scores,
        "compliance_level": compliance_level,
        "legal_review_required": legal_review_required,
        "human_approval_required": human_approval_required,
        "iteration_count": 1,
    }, f"Score composite : {composite_score} → niveau {compliance_level}")

    # Score_validator (toujours exécuté après risk_analyzer)
    valid_dist = True  # distribution simulée comme valide
    _step("score_validator", 80, {
        "score_valid": valid_dist,
        "distribution_check": "4 critique / 2 élevé / 1 modéré / 1 faible — OK",
    }, "Distribution 4/2/1/1 vérifiée")

    # Branches conditionnelles
    if legal_review_required:
        _step("legal_reviewer", 3200, {
            "legal_review_required": True,
            "legal_findings": [
                "CSDDD Art.8 : obligation due diligence identifiée",
                "CSDDD Art.9 : plan d'action correctif requis",
                "CSDDD Art.13 : rapport public annuel obligatoire",
            ],
            "human_approval_required": human_approval_required,
        }, "Revue CSDDD Art.8-13 complétée")

    if human_approval_required:
        _step("human_checkpoint", 0, {
            "interrupt_triggered": True,
            "interrupt_reason": f"Score critique ({composite_score}/100) — approbation humaine requise",
            "awaiting_approval": True,
        }, "INTERRUPT — attente approbation humaine (max 24h)")

        # Simuler l'approbation humaine (résumée)
        _step("human_checkpoint", 7200000, {
            "report_approved": True,
            "approved_by": "compliance-officer@caelum.io",
            "approval_timestamp": _ts(t + 7200000),
            "awaiting_approval": False,
        }, "Approbation humaine reçue après 2h — workflow repris")

        _step("alert_dispatcher", 120, {
            "alerts_sent": [
                f"ALERT-{secrets.token_hex(4).upper()} → NATS caelum.alerts.critique",
                f"ALERT-{secrets.token_hex(4).upper()} → RabbitMQ compliance_reports",
            ],
        }, "Alertes dispatched via NATS + RabbitMQ")
    else:
        # Pas d'approbation humaine — aller directement au report_generator
        pass

    _step("report_generator", 4500, {
        "report_draft": (
            f"RAPPORT CONFORMITÉ CSDDD 2024 — {entity}\n"
            f"Domaine : {domain}\n"
            f"Score composite : {composite_score}/100\n"
            f"Niveau : {compliance_level.upper()}\n"
            f"Généré le : {_ts(t)}"
        ),
        "report_id": f"RPT-{secrets.token_hex(6).upper()}",
    }, "Rapport PDF généré")

    if not human_approval_required:
        _step("alert_dispatcher", 120, {
            "alerts_sent": [
                f"ALERT-{secrets.token_hex(4).upper()} → NATS caelum.alerts.{compliance_level}",
            ],
        }, "Alerte dispatched via NATS")

    _step("blockchain_recorder", 350, {
        "blockchain_tx_hash": "0x" + secrets.token_hex(32),
        "blockchain_network": "Hyperledger Fabric — caelum.audit.channel",
        "audit_trail_immutable": True,
    }, "Audit trail enregistré on-chain")

    _step("notifier", 90, {
        "stakeholders_notified": [
            "compliance-team@caelum.io",
            f"legal-officer@caelum.io",
            f"supply-chain@{entity.lower().replace(' ', '-')}.com",
        ],
        "notification_channels": ["email", "slack", "webhook"],
    }, "Parties prenantes notifiées")

    # État final consolidé
    final_state = {
        "entity_name": entity,
        "domain": domain,
        "compliance_level": compliance_level,
        "composite_score": composite_score,
        "risk_scores": risk_scores,
        "legal_review_required": legal_review_required,
        "human_approval_required": human_approval_required,
        "report_approved": True,
        "alerts_sent": [e["state_patch"].get("alerts_sent", []) for e in execution_trace if "alerts_sent" in e["state_patch"]],
        "iteration_count": 1,
        "errors": [],
        "workflow_status": "COMPLETED",
        "total_duration_ms": t,
        "nodes_visited_count": len(nodes_visited),
        "cycles_count": cycles_count,
    }

    return {
        "execution_trace": execution_trace,
        "nodes_visited": nodes_visited,
        "cycles_count": cycles_count,
        "final_state": final_state,
    }


def design_human_in_the_loop(approval_threshold_score: float) -> dict:
    """
    Conçoit le pattern human-in-the-loop pour les décisions critiques.

    Paramètres
    ----------
    approval_threshold_score : float
        Score à partir duquel l'approbation humaine est requise (ex. 60.0).

    Retourne
    --------
    dict avec :
        interrupt_config  – configuration d'interruption LangGraph (dict)
        resume_procedure  – procédure pour reprendre le workflow (dict)
        timeout_config    – gestion du timeout d'approbation (dict)
        audit_log_entry   – entrée d'audit générée à chaque interruption (dict)
    """
    interrupt_config = {
        "interrupt_before": ["human_checkpoint"],
        "interrupt_condition": f"state['composite_score'] >= {approval_threshold_score} OR state['compliance_level'] in ('critique', 'élevé')",
        "interrupt_payload": {
            "thread_id": "{entity_name}_{domain}_{timestamp}",
            "entity_name": "{state['entity_name']}",
            "compliance_level": "{state['compliance_level']}",
            "composite_score": "{state['composite_score']}",
            "risk_scores": "{state['risk_scores']}",
            "legal_findings": "{state['legal_findings']}",
            "report_draft_preview": "{state['report_draft'][:500]}",
        },
        "notification_on_interrupt": {
            "channels": ["email", "slack", "webhook"],
            "recipients": ["compliance-officer@caelum.io", "legal@caelum.io"],
            "template": "CAELUM_HITL_APPROVAL_REQUEST_v2",
            "urgency": "high" if approval_threshold_score <= 60 else "normal",
        },
    }

    resume_procedure = {
        "api_call": "POST /threads/{thread_id}/runs",
        "payload_approve": {
            "input": None,
            "command": {"resume": True},
            "config": {
                "configurable": {
                    "thread_id": "{thread_id}",
                    "human_decision": "approved",
                    "approved_by": "{user_email}",
                    "approval_note": "{justification_text}",
                    "approval_timestamp": "{iso_timestamp}",
                }
            },
        },
        "payload_reject": {
            "input": None,
            "command": {"resume": True},
            "config": {
                "configurable": {
                    "thread_id": "{thread_id}",
                    "human_decision": "rejected",
                    "rejection_reason": "{reason_code}",
                    "rejected_by": "{user_email}",
                }
            },
        },
        "sdk_example_python": (
            "# Approval\n"
            "graph.invoke(None, config={'configurable': {'thread_id': thread_id}})\n"
            "# Rejection (triggers re-analyze cycle)\n"
            "graph.update_state(config, {'report_approved': False}, as_node='human_checkpoint')\n"
            "graph.invoke(None, config=config)"
        ),
        "auth_required": "OAuth2 Bearer Token + MFA",
    }

    timeout_config = {
        "timeout_hours": 24,
        "reminder_at_hours": [2, 8, 20],
        "escalation_at_hours": 12,
        "escalation_recipients": ["cco@caelum.io", "legal-director@caelum.io"],
        "on_timeout_action": "auto_reject",
        "on_timeout_note": "Workflow archivé automatiquement après 24h sans approbation — révision manuelle requise",
        "timeout_alert_channel": "caelum.alerts.hitl.timeout",
        "cron_check": "*/30 * * * *",  # vérification toutes les 30 min
    }

    audit_log_entry = {
        "event_type": "HITL_INTERRUPT",
        "thread_id": "{thread_id}",
        "entity_name": "{entity_name}",
        "domain": "{domain}",
        "composite_score": "{composite_score}",
        "threshold": approval_threshold_score,
        "interrupted_at": "{iso_timestamp}",
        "interrupted_before_node": "human_checkpoint",
        "graph_name": "caelum_compliance_workflow",
        "langgraph_version": LANGGRAPH_VERSION,
        "csddd_articles": ["Art.8", "Art.9", "Art.13"],
        "immutable": True,
        "blockchain_recorded": True,
    }

    return {
        "interrupt_config": interrupt_config,
        "resume_procedure": resume_procedure,
        "timeout_config": timeout_config,
        "audit_log_entry": audit_log_entry,
    }


def generate_mermaid_diagram(graph_name: str) -> str:
    """
    Génère un diagramme Mermaid du graphe d'états.

    Paramètres
    ----------
    graph_name : str – Nom du graphe ("caelum_compliance_workflow" ou "caelum_alert_response").

    Retourne
    --------
    str : diagramme Mermaid valide représentant le workflow CSDDD.
    """
    if graph_name == "caelum_compliance_workflow":
        return (
            "```mermaid\n"
            "stateDiagram-v2\n"
            "    [*] --> document_loader\n"
            "    document_loader --> risk_analyzer : toujours\n"
            "    risk_analyzer --> score_validator : toujours\n"
            "    score_validator --> risk_analyzer : iteration_count < 3 AND dist invalide [CYCLE]\n"
            "    score_validator --> legal_reviewer : critique ou élevé\n"
            "    score_validator --> report_generator : modéré ou faible\n"
            "    legal_reviewer --> human_checkpoint : human_approval_required = True\n"
            "    legal_reviewer --> report_generator : human_approval_required = False\n"
            "    human_checkpoint --> alert_dispatcher : report_approved = True\n"
            "    human_checkpoint --> risk_analyzer : report_approved = False [CYCLE]\n"
            "    report_generator --> alert_dispatcher : toujours\n"
            "    alert_dispatcher --> blockchain_recorder : toujours\n"
            "    blockchain_recorder --> notifier : toujours\n"
            "    notifier --> [*]\n"
            "\n"
            "    note right of human_checkpoint : INTERRUPT_BEFORE\\nattente approbation humaine\\nmax 24h\n"
            "    note right of score_validator : distribution 4/2/1/1\\ncomposite_score vérifiés\n"
            "    note right of blockchain_recorder : audit trail immuable\\nHyperledger Fabric\n"
            "```"
        )
    elif graph_name == "caelum_alert_response":
        return (
            "```mermaid\n"
            "stateDiagram-v2\n"
            "    [*] --> alert_receiver\n"
            "    alert_receiver --> triage_classifier : parallèle (Send API)\n"
            "    alert_receiver --> impact_assessor : parallèle (Send API)\n"
            "    triage_classifier --> escalation_manager : toujours\n"
            "    impact_assessor --> escalation_manager : toujours\n"
            "    escalation_manager --> action_executor : route dynamique\n"
            "    action_executor --> resolution_verifier : toujours\n"
            "    resolution_verifier --> action_executor : resolved = False (max 3 retry) [CYCLE]\n"
            "    resolution_verifier --> post_mortem_recorder : resolved = True\n"
            "    post_mortem_recorder --> [*]\n"
            "\n"
            "    note right of alert_receiver : parallélisme via Send API\n"
            "    note right of resolution_verifier : retry avec backoff\\nmax 3 tentatives\n"
            "```"
        )
    else:
        return (
            "```mermaid\n"
            "stateDiagram-v2\n"
            f"    [*] --> start_{graph_name}\n"
            f"    start_{graph_name} --> [*]\n"
            "    note : graphe inconnu\n"
            "```"
        )


def compare_graph_architectures() -> dict:
    """
    Compare les architectures StateGraph pour différents use cases CaelumSwarm™.

    Retourne
    --------
    dict avec comparison_table listant chaque pattern avec scores
    (complexité, réutilisabilité, latence, use_case_fit, score_total).
    """
    # Critères : complexité d'implémentation (1=simple, 5=complexe),
    #            réutilisabilité, adéquation use case CSDDD, latence (1=rapide, 5=lent)
    architectures = {
        "agent_loop": {
            "label": "Agent Loop (ReAct)",
            "implementation_complexity": 2,
            "reusability": 4,
            "csddd_fit": 3,
            "latency_score": 2,
            "cycle_support": True,
            "human_in_the_loop": False,
            "parallel_nodes": False,
            "use_case": "Analyse ad-hoc — LLM appelle tools itérativement",
            "strengths": ["Simple à implémenter", "Flexible", "Bon pour tâches exploratoires"],
            "weaknesses": ["Pas de contrôle humain natif", "Difficile à auditer"],
        },
        "multi_agent_supervisor": {
            "label": "Multi-Agent Supervisor",
            "implementation_complexity": 4,
            "reusability": 5,
            "csddd_fit": 5,
            "latency_score": 3,
            "cycle_support": True,
            "human_in_the_loop": True,
            "parallel_nodes": True,
            "use_case": "Orchestration multi-domaines CSDDD — compliance + legal + reporting",
            "strengths": ["Spécialisation par agent", "Haute réutilisabilité", "HiTL natif"],
            "weaknesses": ["Complexité accrue", "Latence supervisor overhead"],
        },
        "reflection": {
            "label": "Reflection (Generate → Critique → Revise)",
            "implementation_complexity": 3,
            "reusability": 3,
            "csddd_fit": 4,
            "latency_score": 4,
            "cycle_support": True,
            "human_in_the_loop": False,
            "parallel_nodes": False,
            "use_case": "Génération rapports CSDDD haute qualité avec auto-amélioration",
            "strengths": ["Qualité output élevée", "Auto-correction", "Audit trail naturel"],
            "weaknesses": ["Latence cumulée (N itérations)", "Coût LLM multiplié"],
        },
        "plan_and_execute": {
            "label": "Plan and Execute",
            "implementation_complexity": 3,
            "reusability": 4,
            "csddd_fit": 5,
            "latency_score": 3,
            "cycle_support": True,
            "human_in_the_loop": True,
            "parallel_nodes": True,
            "use_case": "Audit multi-domaines planifié — CSDDD Art.8 due diligence complète",
            "strengths": ["Plan explicite → auditabilité", "Adaptable en cours d'exécution", "HiTL possible"],
            "weaknesses": ["Replanner coûteux si contexte change", "Plan initial peut être sous-optimal"],
        },
    }

    # Calcul score total : csddd_fit × 3 + reusability × 2 - implementation_complexity - latency_score
    for name, arch in architectures.items():
        arch["score_total"] = (
            arch["csddd_fit"] * 3
            + arch["reusability"] * 2
            - arch["implementation_complexity"]
            - arch["latency_score"]
        )

    # Classement
    ranked = sorted(architectures.items(), key=lambda x: x[1]["score_total"], reverse=True)
    winner = ranked[0][0]

    comparison_table = {
        "architectures": architectures,
        "ranking": [name for name, _ in ranked],
        "winner": winner,
        "winner_justification": (
            f"'{architectures[winner]['label']}' obtient le meilleur score total "
            f"({architectures[winner]['score_total']}/18) grâce à sa forte adéquation CSDDD "
            f"(csddd_fit={architectures[winner]['csddd_fit']}/5), sa réutilisabilité maximale "
            f"({architectures[winner]['reusability']}/5), son support natif du parallélisme "
            f"et du human-in-the-loop — idéal pour orchestrer compliance + legal + reporting "
            f"dans CaelumSwarm™."
        ),
        "caelum_recommendation": (
            "Utiliser 'multi_agent_supervisor' pour les workflows principaux CSDDD. "
            "Combiner avec 'reflection' pour la génération de rapports haute qualité. "
            "'plan_and_execute' recommandé pour les audits annuels multi-domaines planifiés."
        ),
    }
    return comparison_table


# ---------------------------------------------------------------------------
# Helpers d'affichage
# ---------------------------------------------------------------------------

def _sep(char: str = "─", width: int = 72) -> str:
    return char * width


def _section(title: str) -> None:
    print()
    print(_sep("="))
    print(f"  {title}")
    print(_sep("="))


def _subsection(title: str) -> None:
    print()
    print(f"  {_sep('-', 68)}")
    print(f"  {title}")
    print(f"  {_sep('-', 68)}")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # ─── HEADER ──────────────────────────────────────────────────────────────
    print(_sep("="))
    print("  LANGGRAPH INTEGRATION REPORT — CaelumSwarm™")
    print("  Human Rights / CSDDD 2024 Compliance Platform")
    print(f"  Generated : {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"  Framework : LangGraph {LANGGRAPH_VERSION} / StateGraph / HiTL / PostgresSaver")
    print(_sep("="))

    # ─── 1. COMPLIANCE STATEGRAPH ────────────────────────────────────────────
    _section("1. COMPLIANCE STATEGRAPH (12 nodes, edges conditionnels)")

    csg = COMPLIANCE_STATE_GRAPH
    print(f"  Graphe        : {csg['name']}")
    print(f"  Entry point   : {csg['entry_point']}")
    print(f"  Interrupts    : {csg['interrupt_before']}")
    print(f"  Checkpointing : {csg['checkpointing']['backend']} — {csg['checkpointing']['description']}")
    print()
    print(f"  Nodes ({len(csg['nodes'])}) :")
    for node, meta in csg["nodes"].items():
        desc = meta if isinstance(meta, str) else meta.get("description", "")
        print(f"    [{node}]  {desc}")
    print()
    print("  Edges conditionnels :")
    for edge, cfg in csg["edges"]["conditional_edges"].items():
        cond = cfg.get("condition", "")
        print(f"    {edge}")
        print(f"      condition : {cond}")
        for outcome, target in cfg.items():
            if outcome == "condition":
                continue
            print(f"      {outcome} → {target}")
    print()
    print("  Edges inconditionnels :")
    for edge, note in csg["edges"]["unconditional_edges"].items():
        print(f"    {edge}  ({note})")
    print()
    print("  State schema :")
    for field, ftype in csg["state_schema"].items():
        print(f"    {field:<30} : {ftype}")

    # ─── 2. DIAGRAMME MERMAID ────────────────────────────────────────────────
    _section("2. DIAGRAMME MERMAID — caelum_compliance_workflow")

    mermaid_compliance = generate_mermaid_diagram("caelum_compliance_workflow")
    print()
    for line in mermaid_compliance.split("\n"):
        print(f"  {line}")

    # ─── 3. ALERT RESPONSE GRAPH ─────────────────────────────────────────────
    _section("3. ALERT RESPONSE GRAPH (parallélisme + retry)")

    arg = ALERT_RESPONSE_GRAPH
    print(f"  Graphe        : {arg['name']}")
    print()
    print(f"  Nodes ({len(arg['nodes'])}) :")
    for node, desc in arg["nodes"].items():
        print(f"    [{node}]  {desc}")
    print()
    print("  Patterns spéciaux :")
    for pattern, desc in arg["special_patterns"].items():
        print(f"    [{pattern}]")
        print(f"      {desc}")
    print()
    mermaid_alert = generate_mermaid_diagram("caelum_alert_response")
    print("  Diagramme Mermaid :")
    for line in mermaid_alert.split("\n"):
        print(f"    {line}")

    # ─── 4. SUBGRAPHS ────────────────────────────────────────────────────────
    _section("4. SUBGRAPHS (supplier_audit, document_processing)")

    for sg_name, sg_cfg in SUBGRAPHS.items():
        print(f"  Subgraph : {sg_name}")
        print(f"    Description : {sg_cfg['description']}")
        if "inputs" in sg_cfg:
            print(f"    Inputs      : {', '.join(sg_cfg['inputs'])}")
            print(f"    Outputs     : {', '.join(sg_cfg['outputs'])}")
            print(f"    Réutilisé   : {', '.join(sg_cfg['reused_in'])}")
        if "nodes" in sg_cfg:
            print(f"    Nodes       : {' → '.join(sg_cfg['nodes'])}")
        print()

    # ─── 5. DESIGN STATE GRAPH ───────────────────────────────────────────────
    _section("5. DESIGN StateGraph — caelum_compliance_workflow")

    nodes_list = [
        "document_loader", "risk_analyzer", "score_validator",
        "legal_reviewer", "human_checkpoint", "report_generator",
        "alert_dispatcher", "blockchain_recorder", "notifier",
    ]
    sg_design = design_state_graph(
        workflow_name="caelum_compliance_workflow",
        nodes=nodes_list,
        has_cycles=True,
    )
    gd = sg_design["graph_definition"]
    print(f"  Graphe        : {gd['name']}")
    print(f"  Framework     : {gd['framework']}")
    print(f"  Classe        : {gd['class']}")
    print(f"  Nodes         : {gd['node_count']}")
    print(f"  Cycles        : {gd['has_cycles']}  (guard: {gd['cycle_guard']})")
    print(f"  Entry point   : {sg_design['entry_point']}")
    print()
    print("  Edges map :")
    for src, edge in sg_design["edges_map"].items():
        if edge["type"] == "conditional":
            targets = edge.get("possible_targets", [])
            print(f"    {src} → {targets}  [conditional: {edge['condition_fn']}]")
        else:
            print(f"    {src} → {edge['target']}  [unconditional]")
    print()
    cp = sg_design["checkpointing_config"]
    print("  Checkpointing (PostgresSaver) :")
    for k, v in cp.items():
        print(f"    {k:<25} : {v}")

    # ─── 6. GRAPH EXECUTION SIMULATION ───────────────────────────────────────
    _section("6. SIMULATION D'EXÉCUTION — Shell Petroleum / conflict_minerals")

    initial_state = {
        "entity_name": "Shell Petroleum",
        "domain": "conflict_minerals",
        "documents": [],
        "risk_scores": {},
        "iteration_count": 0,
        "errors": [],
    }
    sim_result = simulate_graph_execution("caelum_compliance_workflow", initial_state)

    print(f"  Entité        : {initial_state['entity_name']}")
    print(f"  Domaine       : {initial_state['domain']}")
    print()
    print(f"  Trace d'exécution ({len(sim_result['execution_trace'])} étapes) :")
    for step in sim_result["execution_trace"]:
        dur = f"{step['duration_ms']:,} ms" if step["duration_ms"] else "attente humaine"
        print(f"    Étape {step['step']:2d} | [{step['node']:<22}] | {dur}")
        if step.get("note"):
            print(f"             └─ {step['note']}")
    print()
    fs = sim_result["final_state"]
    print("  État final :")
    print(f"    compliance_level   : {fs['compliance_level']}")
    print(f"    composite_score    : {fs['composite_score']}/100")
    print(f"    risk_scores        :")
    for k, v in fs["risk_scores"].items():
        print(f"      {k:<32} : {v}")
    print(f"    human_approval     : {fs['human_approval_required']}")
    print(f"    report_approved    : {fs['report_approved']}")
    print(f"    workflow_status    : {fs['workflow_status']}")
    print(f"    nodes_visited      : {fs['nodes_visited_count']}")
    print(f"    cycles             : {fs['cycles_count']}")
    print(f"    total_duration_ms  : {fs['total_duration_ms']:,} ms (~{fs['total_duration_ms'] // 60000} min)")

    # ─── 7. HUMAN-IN-THE-LOOP DESIGN ─────────────────────────────────────────
    _section("7. HUMAN-IN-THE-LOOP DESIGN (threshold: 60/100)")

    hitl = design_human_in_the_loop(approval_threshold_score=60.0)

    print("  Interrupt config :")
    ic = hitl["interrupt_config"]
    print(f"    interrupt_before   : {ic['interrupt_before']}")
    print(f"    interrupt_condition: {ic['interrupt_condition']}")
    print(f"    notification chan.  : {', '.join(ic['notification_on_interrupt']['channels'])}")
    print(f"    urgency            : {ic['notification_on_interrupt']['urgency']}")
    print()
    print("  Resume procedure :")
    rp = hitl["resume_procedure"]
    print(f"    API endpoint : {rp['api_call']}")
    print(f"    Auth required: {rp['auth_required']}")
    print()
    print("    SDK Python (exemple) :")
    for line in rp["sdk_example_python"].split("\n"):
        print(f"      {line}")
    print()
    print("  Timeout config :")
    tc = hitl["timeout_config"]
    print(f"    timeout_hours       : {tc['timeout_hours']}h")
    print(f"    reminders à         : {tc['reminder_at_hours']} h")
    print(f"    escalation à        : {tc['escalation_at_hours']} h → {', '.join(tc['escalation_recipients'])}")
    print(f"    on_timeout          : {tc['on_timeout_action']} — {tc['on_timeout_note']}")
    print(f"    cron check          : {tc['cron_check']}")
    print()
    print("  Audit log entry (extrait) :")
    al = hitl["audit_log_entry"]
    for k, v in al.items():
        print(f"    {k:<30} : {v}")

    # ─── 8. CHECKPOINTING CONFIG ─────────────────────────────────────────────
    _section("8. CHECKPOINTING CONFIG (PostgresSaver)")

    cp_cfg = COMPLIANCE_STATE_GRAPH["checkpointing"]
    print(f"  Backend         : {cp_cfg['backend']}")
    print(f"  Enabled         : {cp_cfg['enabled']}")
    print(f"  Thread ID       : {cp_cfg['thread_id']}")
    print(f"  Description     : {cp_cfg['description']}")
    print()
    print("  Détails PostgresSaver :")
    pg_details = {
        "dsn": "postgresql://caelum.internal:5432/langgraph  (via Vault — jamais en clair)",
        "ssl_mode": "require",
        "max_connections": 20,
        "pool_timeout_s": 30,
        "schema": "langgraph_checkpoints",
        "table_checkpoints": "checkpoints",
        "table_writes": "checkpoint_writes",
        "ttl_days": 90,
        "read_replica": "postgresql://caelum-ro.internal:5432/langgraph (lectures seules)",
        "backup_schedule": "pg_dump toutes les heures → S3 chiffré",
    }
    for k, v in pg_details.items():
        print(f"    {k:<22} : {v}")

    # ─── 9. GRAPH PATTERNS COMPARISON ────────────────────────────────────────
    _section("9. GRAPH PATTERNS COMPARISON")

    comparison = compare_graph_architectures()

    hdr = ["Pattern", "CSDDD Fit", "Réutilis.", "Complexité", "Latence", "HiTL", "Cycles", "Score"]
    col = [30, 10, 10, 12, 9, 6, 7, 7]
    print("  " + "  ".join(h.ljust(w) for h, w in zip(hdr, col)))
    print("  " + "  ".join("-" * w for w in col))

    for rank_i, arch_name in enumerate(comparison["ranking"]):
        arch = comparison["architectures"][arch_name]
        marker = " ← WINNER" if arch_name == comparison["winner"] else ""
        row = [
            arch["label"] + marker,
            str(arch["csddd_fit"]) + "/5",
            str(arch["reusability"]) + "/5",
            str(arch["implementation_complexity"]) + "/5",
            str(arch["latency_score"]) + "/5",
            "oui" if arch["human_in_the_loop"] else "non",
            "oui" if arch["cycle_support"] else "non",
            str(arch["score_total"]),
        ]
        print("  " + "  ".join(v.ljust(w) for v, w in zip(row, col)))

    print()
    print(f"  Gagnant       : {comparison['winner']}")
    print(f"  Justification : {comparison['winner_justification']}")
    print()
    print(f"  Recommandation CaelumSwarm™ :")
    print(f"    {comparison['caelum_recommendation']}")

    print()
    print("  Statistiques d'exécution des nodes :")
    hdr2 = ["Node", "Avg (ms)", "Error %", "Retry policy"]
    col2 = [24, 10, 10, 30]
    print("  " + "  ".join(h.ljust(w) for h, w in zip(hdr2, col2)))
    print("  " + "  ".join("-" * w for w in col2))
    for node, stats in NODE_EXECUTION_STATS.items():
        dur = str(stats["avg_duration_ms"]) if stats["avg_duration_ms"] else "N/A (HiTL)"
        row2 = [node, dur, str(stats["error_rate_pct"]) + " %", stats["retry_policy"]]
        print("  " + "  ".join(v.ljust(w) for v, w in zip(row2, col2)))

    # ─── 10. LANGGRAPH PLATFORM CRONS ────────────────────────────────────────
    _section("10. LANGGRAPH PLATFORM CRONS")

    platform = LANGGRAPH_PLATFORM_CONFIG
    print(f"  Deployment    : {platform['deployment']}")
    print(f"  API endpoint  : {platform['api_endpoint']}")
    print(f"  Streaming     : {platform['streaming']}")
    print(f"  Persistence   : {platform['persistence']}")
    print(f"  Memory store  : {platform['memory_store']}")
    print(f"  Auth          : {platform['auth']}")
    print()
    print(f"  Crons ({len(platform['crons'])}) :")
    for cron in platform["crons"]:
        print(f"    Schedule : {cron['schedule']}")
        print(f"    Graph    : {cron['graph']}")
        trigger_key = "input" if "input" in cron else "trigger"
        print(f"    {trigger_key.capitalize():<8} : {cron[trigger_key]}")
        print()
    print(f"  Interrupt points : {platform['interrupt_points']}")

    # ─── 11. LANGGRAPH SECURITY ──────────────────────────────────────────────
    _section("11. LANGGRAPH SECURITY")

    for category, items in SECURITY_CONFIG.items():
        print(f"\n  [{category}]")
        for key, value in items.items():
            print(f"    {key:<30} : {value}")

    checklist = [
        ("State",       "State isolation par thread_id — aucune fuite inter-workflows",   True),
        ("State",       "État chiffré au repos dans PostgresSaver (AES-256)",             True),
        ("State",       "Checkpoints signés HMAC-SHA256 — détection tampering",          True),
        ("State",       "Préfixe entity_name — ségrégation multi-tenant",                True),
        ("Checkpoint",  "Credentials PostgreSQL via Vault — jamais en clair",             True),
        ("Checkpoint",  "SSL mode require sur connexion PostgresSaver",                   True),
        ("Checkpoint",  "Réplica RO pour lectures — écriture primaire uniquement",       True),
        ("Interrupt",   "OAuth2 Bearer Token requis pour reprendre thread interrompu",   True),
        ("Interrupt",   "MFA obligatoire pour approuver workflows critique",             True),
        ("Interrupt",   "Chaque approbation loggée : user_id + timestamp + justif.",    True),
        ("Interrupt",   "Timeout 24h avec escalade automatique à 12h",                  True),
        ("API",         "API Key rotation automatique 90 jours",                         True),
        ("API",         "Webhook signing HMAC-SHA256 sur payload",                       True),
        ("API",         "Rate limiting : 100 req/min / 10 interrupts/min",              True),
        ("API",         "IP allowlist — accès LangGraph Platform depuis VPN uniquement", True),
    ]

    print()
    print("  Checklist sécurité :")
    current_cat = ""
    for cat, item, ok in checklist:
        if cat != current_cat:
            print(f"\n  [{cat}]")
            current_cat = cat
        mark = "+" if ok else "!"
        print(f"    {mark}  {item}")

    # ─── FOOTER ──────────────────────────────────────────────────────────────
    print()
    print(_sep("="))
    print()
    print(f"  LangGraph Integration Agent — PRET (LangGraph {LANGGRAPH_VERSION} / StateGraph / HiTL / PostgresSaver)")
    print()
    print(_sep("="))
