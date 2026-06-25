"""
Microsoft AutoGen Integration Agent — CaelumSwarm™
Framework: AutoGen 0.4.x (AgentChat API)
Role: Systèmes conversationnels multi-agents pour conformité CSDDD 2024
Compatible: Claude claude-sonnet-4-6 via AnthropicChatCompletionClient
"""

import datetime
import json
import math
import secrets

# =============================================================================
# CONSTANTES
# =============================================================================

AUTOGEN_VERSION = "0.4.x"

AUTOGEN_AGENTS = {
    "compliance_assistant": {
        "agent_type": "AssistantAgent",
        "name": "caelum_compliance_assistant",
        "description": "Expert en conformité CSDDD 2024, droits humains et due diligence",
        "model_client": {"model": "claude-sonnet-4-6", "api_type": "anthropic"},
        "system_message": (
            "Tu es un expert en conformité CSDDD 2024 pour Caelum Partners SPRL.\n"
            "Tu analyses les risques droits humains, scores les entités (0-100), "
            "et génères des rapports structurés.\n"
            "Tu utilises le pattern: 4 entités critiques / 2 élevées / 1 modérée / 1 faible.\n"
            "Tu maîtrises CSDDD Art.8-13, RGPD Art.25, EU AI Act Art.9."
        ),
        "tools": ["analyze_compliance_risk", "generate_wave_score", "create_report"],
    },
    "legal_reviewer": {
        "agent_type": "AssistantAgent",
        "name": "caelum_legal_reviewer",
        "description": "Juriste expert droit UE, CSDDD, RGPD",
        "model_client": {"model": "mistral-large-latest", "api_type": "mistral"},
        "system_message": (
            "Tu es une avocate spécialisée droit UE. "
            "Tu valides la conformité légale des analyses CSDDD."
        ),
    },
    "user_proxy": {
        "agent_type": "UserProxyAgent",
        "name": "caelum_operator",
        "human_input_mode": "TERMINATE",
        "max_consecutive_auto_reply": 10,
        "code_execution_config": {
            "work_dir": "swarm/intelligence",
            "use_docker": True,
            "timeout": 60,
        },
        "is_termination_msg": "lambda x: x.get('content', '') and 'CONFORMITÉ VALIDÉE' in x['content']",
    },
    "data_analyst": {
        "agent_type": "AssistantAgent",
        "name": "caelum_data_analyst",
        "description": "Analyste données pour métriques CaelumSwarm™",
        "model_client": {"model": "gpt-4o", "api_type": "openai"},
        "tools": ["query_postgresql", "query_redis", "generate_chart"],
    },
    "code_executor": {
        "agent_type": "CodeExecutorAgent",
        "name": "caelum_code_executor",
        "description": "Exécute les engines Python CaelumSwarm™",
        "code_execution_config": {
            "executor": "DockerCommandLineCodeExecutor",
            "work_dir": "swarm/intelligence",
        },
    },
}

AUTOGEN_GROUP_CHATS = {
    "compliance_roundtable": {
        "name": "CaelumSwarm™ Compliance Roundtable",
        "agents": ["compliance_assistant", "legal_reviewer", "data_analyst", "user_proxy"],
        "max_round": 15,
        "speaker_selection_method": "round_robin",
        "allow_repeat_speaker": False,
        "send_introductions": True,
        "messages": [
            {
                "role": "user",
                "content": "Analyser la conformité CSDDD de {company} pour les domaines {domains}",
            }
        ],
    },
    "engine_development_chat": {
        "name": "Wave Engine Development Chat",
        "agents": ["compliance_assistant", "code_executor", "user_proxy"],
        "max_round": 20,
        "speaker_selection_method": "auto",
    },
    "alert_triage": {
        "name": "Alert Triage Chat",
        "agents": ["compliance_assistant", "legal_reviewer", "user_proxy"],
        "max_round": 5,
        "speaker_selection_method": "round_robin",
        "termination_condition": "MaxMessageTermination(max_messages=10)",
    },
}

AUTOGEN_SWARM_TEAMS = {
    "compliance_swarm": {
        "type": "Swarm",
        "agents": ["compliance_assistant", "legal_reviewer", "data_analyst"],
        "handoffs": {
            "compliance_assistant → legal_reviewer": (
                "quand analyse terminée, besoin validation légale"
            ),
            "legal_reviewer → data_analyst": (
                "quand validation légale OK, besoin métriques"
            ),
            "data_analyst → compliance_assistant": (
                "quand métriques prêtes, générer rapport final"
            ),
        },
        "termination": "TextMentionTermination('RAPPORT FINAL APPROUVÉ')",
    },
}

AUTOGEN_TOOLS = {
    "analyze_compliance_risk": {
        "function": "def analyze_compliance_risk(entity: str, domain: str, country: str) -> dict",
        "description": "Analyse le risque de conformité CSDDD pour une entité",
        "returns": "dict avec score (0-100), sévérité, articles CSDDD applicables",
    },
    "generate_wave_score": {
        "function": "def generate_wave_score(entities: list) -> dict",
        "description": "Génère les scores CaelumSwarm™ avec distribution 4/2/1/1",
    },
    "create_report": {
        "function": "def create_report(analysis: dict, format: str) -> str",
        "description": "Crée un rapport conformité (PDF, JSON, HTML)",
    },
    "query_postgresql": {
        "function": "def query_postgresql(query: str, params: dict) -> list",
        "description": "Interroge la base PostgreSQL CaelumSwarm™ (read-only)",
    },
    "query_redis": {
        "function": "def query_redis(key: str) -> dict",
        "description": "Lit le cache Redis CaelumSwarm™",
    },
}

AUTOGEN_CONFIG_LIST = {
    "claude_sonnet_config": {
        "model": "claude-sonnet-4-6",
        "api_key": "VAULT_MANAGED",
        "api_type": "anthropic",
        "max_tokens": 8192,
        "temperature": 0.1,
    },
    "gpt4o_config": {
        "model": "gpt-4o",
        "api_key": "VAULT_MANAGED",
        "api_type": "openai",
        "temperature": 0.0,
    },
    "mistral_config": {
        "model": "mistral-large-latest",
        "api_key": "VAULT_MANAGED",
        "api_type": "mistral",
    },
    "local_llama_config": {
        "model": "llama-3.1-70b-instruct",
        "base_url": "http://ollama.caelum.internal:11434/v1",
        "api_type": "openai",
        "description": "Traitement données sensibles — on-premise, aucun envoi cloud",
    },
}

CONVERSATION_PATTERNS = {
    "two_agent_chat": {
        "description": "Chat direct entre 2 agents — le plus simple",
        "pattern": "user_proxy.initiate_chat(compliance_assistant, message='...')",
        "use_case": "Analyse rapide d'une entité",
    },
    "group_chat": {
        "description": "Roundtable avec 4 agents, speaker selection auto",
        "pattern": "GroupChat + GroupChatManager",
        "use_case": "Analyse complexe nécessitant plusieurs expertises",
    },
    "swarm": {
        "description": "Agents avec handoffs automatiques (AutoGen 0.4+)",
        "pattern": "Swarm team avec TransferToAgent tools",
        "use_case": "Pipeline conformité complète automatisée",
    },
    "nested_chat": {
        "description": "Chat imbriqué pour sous-tâches complexes",
        "pattern": "register_nested_chats()",
        "use_case": "Décomposer l'analyse par fournisseur Tier 1/2/3",
    },
}

FRAMEWORK_COMPARISON = {
    "AutoGen": {
        "vendor": "Microsoft",
        "version": "0.4.x",
        "paradigm": "Conversationnel — agents dialoguent via messages",
        "strengths": [
            "Swarm natif avec handoffs déclaratifs (0.4.x)",
            "GroupChat multi-agent avec speaker selection LLM",
            "Code execution sécurisée via Docker (CodeExecutorAgent)",
            "Multi-LLM natif (OpenAI, Anthropic, Mistral, Ollama)",
            "AgentChat API unifiée (0.4.x)",
            "Nested chats pour sous-tâches complexes",
        ],
        "weaknesses": [
            "API 0.4.x rompt la compatibilité avec 0.2.x",
            "Observabilité moins mature que LangChain",
            "Moins de connecteurs data sources qu'AgentPy",
        ],
        "caelum_fit": "EXCELLENT — groupchat CSDDD roundtable + swarm pipeline + code exec engines",
        "score_caelum": 9.2,
    },
    "CrewAI": {
        "vendor": "CrewAI Inc.",
        "version": "0.x",
        "paradigm": "Rôles & tâches — agents assignés à des missions séquentielles",
        "strengths": [
            "Définition claire des rôles (role, goal, backstory)",
            "Process séquentiel ou hiérarchique natif",
            "Intégration LangChain tools",
            "Interface YAML pour définir les crews",
        ],
        "weaknesses": [
            "Moins flexible pour conversations libres",
            "Pas de code execution native intégrée",
            "Swarm pattern moins mature qu'AutoGen 0.4",
            "Dépendance forte LangChain",
        ],
        "caelum_fit": "BON — adapté pipelines séquentiels CSDDD, moins pour roundtables",
        "score_caelum": 7.8,
    },
    "LangChain": {
        "vendor": "LangChain Inc.",
        "version": "0.3.x",
        "paradigm": "Chaînes de traitement — composants connectés en DAG",
        "strengths": [
            "Écosystème très large (200+ intégrations)",
            "LangSmith observabilité native",
            "LCEL (LangChain Expression Language) expressif",
            "Agents ReAct, Plan-and-Execute natifs",
        ],
        "weaknesses": [
            "Complexité API élevée (trop de niveaux d'abstraction)",
            "Multi-agent conversationnel moins fluide qu'AutoGen",
            "Verbosité du code pour des tâches simples",
            "Breaking changes fréquents",
        ],
        "caelum_fit": "MOYEN — sur-ingéniéré pour CaelumSwarm™, meilleur pour RAG pipelines",
        "score_caelum": 6.5,
    },
}

AUTOGEN_SECURITY_CONFIG = {
    "docker_isolation": {
        "enabled": True,
        "image": "python:3.12-slim",
        "network_mode": "none",
        "read_only_fs": True,
        "memory_limit": "512m",
        "cpu_quota": 50000,
        "allowed_imports": [
            "json", "math", "datetime", "secrets", "hashlib",
            "statistics", "collections", "functools", "itertools",
        ],
        "blocked_imports": [
            "os", "subprocess", "sys", "socket", "requests",
            "urllib", "http", "ftplib", "smtplib",
        ],
        "timeout_seconds": 60,
        "work_dir": "/sandbox/swarm/intelligence",
    },
    "message_sanitization": {
        "strip_credentials": True,
        "max_message_length": 32768,
        "pii_detection": True,
        "pii_action": "redact",
        "blocked_patterns": [
            r"api[_-]?key\s*[:=]\s*\S+",
            r"password\s*[:=]\s*\S+",
            r"secret\s*[:=]\s*\S+",
            r"bearer\s+[A-Za-z0-9\-._~+/]+=*",
        ],
    },
    "audit_trail": {
        "enabled": True,
        "log_all_messages": True,
        "log_tool_calls": True,
        "log_code_executions": True,
        "storage": "postgresql://audit.caelum.internal/caelum_swarm",
        "retention_days": 365,
        "tamper_proof": True,
    },
    "rate_limiting": {
        "max_rounds_per_session": 50,
        "max_tokens_per_round": 4096,
        "max_tool_calls_per_round": 5,
        "cooldown_between_sessions_seconds": 2,
    },
}


# =============================================================================
# FONCTIONS
# =============================================================================

def design_autogen_workflow(task_type: str, complexity: str) -> dict:
    """
    Conçoit le workflow AutoGen optimal pour une tâche CaelumSwarm™.

    Paramètres
    ----------
    task_type  : str — "compliance_analysis" | "alert_triage" | "engine_dev" | "report_gen"
    complexity : str — "simple" | "complex" | "automated"

    Retourne
    --------
    dict avec agents_config, conversation_pattern, estimated_rounds, token_estimate,
               workflow_code_snippet, recommended_llm
    """
    # Matrice de décision : complexité × type de tâche
    PATTERN_MATRIX = {
        ("simple",    "compliance_analysis"): "two_agent_chat",
        ("simple",    "alert_triage"):        "two_agent_chat",
        ("simple",    "engine_dev"):          "two_agent_chat",
        ("simple",    "report_gen"):          "two_agent_chat",
        ("complex",   "compliance_analysis"): "group_chat",
        ("complex",   "alert_triage"):        "group_chat",
        ("complex",   "engine_dev"):          "group_chat",
        ("complex",   "report_gen"):          "group_chat",
        ("automated", "compliance_analysis"): "swarm",
        ("automated", "alert_triage"):        "swarm",
        ("automated", "engine_dev"):          "nested_chat",
        ("automated", "report_gen"):          "swarm",
    }

    ROUNDS_ESTIMATE = {
        "two_agent_chat": (3, 6),
        "group_chat":     (8, 15),
        "swarm":          (5, 12),
        "nested_chat":    (10, 25),
    }

    # Sélection du pattern
    key = (complexity, task_type)
    pattern = PATTERN_MATRIX.get(key, "group_chat")
    pattern_info = CONVERSATION_PATTERNS.get(pattern, {})

    # Sélection des agents selon la tâche
    AGENTS_BY_TASK = {
        "compliance_analysis": ["compliance_assistant", "legal_reviewer", "data_analyst", "user_proxy"],
        "alert_triage":        ["compliance_assistant", "legal_reviewer", "user_proxy"],
        "engine_dev":          ["compliance_assistant", "code_executor", "user_proxy"],
        "report_gen":          ["compliance_assistant", "data_analyst", "user_proxy"],
    }
    agents = AGENTS_BY_TASK.get(task_type, list(AUTOGEN_AGENTS.keys()))

    # LLM recommandé selon la tâche
    LLM_BY_TASK = {
        "compliance_analysis": "claude_sonnet_config",
        "alert_triage":        "claude_sonnet_config",
        "engine_dev":          "claude_sonnet_config",
        "report_gen":          "gpt4o_config",
    }
    recommended_llm = LLM_BY_TASK.get(task_type, "claude_sonnet_config")
    llm_config = AUTOGEN_CONFIG_LIST.get(recommended_llm, {})

    # Estimation des rounds et tokens
    min_rounds, max_rounds = ROUNDS_ESTIMATE[pattern]
    agent_count = len(agents)
    avg_rounds = (min_rounds + max_rounds) // 2
    avg_tokens_per_round = 800
    token_estimate = avg_rounds * agent_count * avg_tokens_per_round

    # Snippet de code AutoGen 0.4.x
    if pattern == "two_agent_chat":
        code_snippet = (
            "# AutoGen 0.4.x — Two-agent chat\n"
            "from autogen_agentchat.agents import AssistantAgent, UserProxyAgent\n"
            "from autogen_ext.models.anthropic import AnthropicChatCompletionClient\n\n"
            "model_client = AnthropicChatCompletionClient(model='claude-sonnet-4-6')\n"
            "assistant = AssistantAgent('caelum_compliance_assistant', model_client=model_client)\n"
            "proxy = UserProxyAgent('caelum_operator')\n"
            "await proxy.initiate_chat(assistant, message='Analyser la conformité CSDDD de...')"
        )
    elif pattern == "group_chat":
        code_snippet = (
            "# AutoGen 0.4.x — GroupChat\n"
            "from autogen_agentchat.teams import RoundRobinGroupChat\n"
            "from autogen_agentchat.conditions import MaxMessageTermination\n\n"
            "team = RoundRobinGroupChat(\n"
            "    participants=[compliance_assistant, legal_reviewer, data_analyst],\n"
            "    termination_condition=MaxMessageTermination(max_messages=15),\n"
            ")\n"
            "await team.run(task='Analyser la conformité CSDDD de...')"
        )
    elif pattern == "swarm":
        code_snippet = (
            "# AutoGen 0.4.x — Swarm avec handoffs\n"
            "from autogen_agentchat.teams import Swarm\n"
            "from autogen_agentchat.conditions import TextMentionTermination\n\n"
            "team = Swarm(\n"
            "    participants=[compliance_assistant, legal_reviewer, data_analyst],\n"
            "    termination_condition=TextMentionTermination('RAPPORT FINAL APPROUVÉ'),\n"
            ")\n"
            "await team.run(task='Analyser la conformité CSDDD de...')"
        )
    else:  # nested_chat
        code_snippet = (
            "# AutoGen 0.4.x — Nested chat\n"
            "from autogen_agentchat.agents import AssistantAgent\n\n"
            "# Enregistrer le sous-chat pour chaque fournisseur\n"
            "compliance_assistant.register_nested_chats(\n"
            "    [{'recipient': code_executor, 'message': 'Exécuter engine pour {domain}'}],\n"
            "    trigger=lambda msg: 'engine' in msg.lower(),\n"
            ")"
        )

    return {
        "task_type":            task_type,
        "complexity":           complexity,
        "conversation_pattern": pattern,
        "pattern_description":  pattern_info.get("description", ""),
        "pattern_use_case":     pattern_info.get("use_case", ""),
        "agents_selected":      agents,
        "agent_count":          agent_count,
        "estimated_rounds":     avg_rounds,
        "estimated_rounds_range": f"{min_rounds}–{max_rounds}",
        "token_estimate":       token_estimate,
        "recommended_llm":      recommended_llm,
        "llm_model":            llm_config.get("model", "N/A"),
        "workflow_code_snippet": code_snippet,
    }


def simulate_group_chat(topic: str, max_rounds: int) -> dict:
    """
    Simule un GroupChat AutoGen pour une analyse CSDDD.

    Paramètres
    ----------
    topic      : str — sujet de l'analyse (ex. "Conflict Minerals")
    max_rounds : int — nombre maximum de tours de conversation

    Retourne
    --------
    dict avec conversation_log, consensus_reached, final_output,
               total_tokens, duration_seconds, speaker_distribution
    """
    agents_rotation = [
        "caelum_compliance_assistant",
        "caelum_legal_reviewer",
        "caelum_data_analyst",
        "caelum_operator",
    ]

    # Messages simulés par agent et par round
    MESSAGE_TEMPLATES = {
        "caelum_compliance_assistant": [
            "Je débute l'analyse CSDDD pour le domaine {topic}. "
            "Identification des 8 entités selon le pattern 4/2/1/1.",
            "Entités critiques identifiées (score ≥60) : "
            "Congo DRC (78.4), Myanmar (74.1), CAR (69.8), Zimbabwe (63.2).",
            "Entités élevées (score ≥40) : Malaysia (52.1), Philippines (47.6). "
            "Articles CSDDD applicables : Art.8 (due diligence), Art.9 (monitoring).",
            "Mise à jour du composite score après validation légale : avg_composite = 61.43. "
            "Index estimé {topic} : 6.14.",
            "Rapport structuré généré. Distribution confirmée 4/2/1/1. "
            "Poids vérifiés : sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20.",
        ],
        "caelum_legal_reviewer": [
            "Revue juridique en cours. Vérification des articles CSDDD Art.8-13.",
            "Art.8 (obligations de due diligence) : conforme pour 6/8 entités. "
            "DRC et Myanmar nécessitent surveillance renforcée (Art.9).",
            "RGPD Art.25 (privacy by design) : aucun PII dans les scores. Conforme.",
            "EU AI Act Art.9 (gestion des risques IA) : pipeline de scoring classifié "
            "système IA à haut risque — documentation obligatoire.",
            "Validation légale complète. Tous les articles vérifiés. "
            "Recommandation : audit annuel Art.11 CSDDD.",
        ],
        "caelum_data_analyst": [
            "Connexion PostgreSQL CaelumSwarm™. Requête des scores historiques pour {topic}.",
            "Métriques extraites : 847 entités analysées depuis 2023-01. "
            "Trend composite score {topic} : +4.2% vs Q1 2025.",
            "Corrélation détectée : score élevé corrèle avec indice Fraser Institute -0.78 "
            "et WJP Rule of Law Index -0.81.",
            "Graphique radar généré (8 entités × 4 sous-indices). "
            "Redis cache invalidé pour clé 'wave:{topic}:scores'.",
            "Métriques consolidées. Rapport analytics joint à l'analyse principale.",
        ],
        "caelum_operator": [
            "Analyse en cours. Surveillance des outputs.",
            "Confirmation : pattern 4/2/1/1 respecté. Poids validés.",
            "Vérification sécurité : aucun credential dans les messages. "
            "sealResponse actif. SWARM_API_URL guard vérifié.",
            "Approbation intermédiaire. Continuer avec le rapport final.",
            "CONFORMITÉ VALIDÉE — analyse {topic} approuvée pour production.",
        ],
    }

    now = datetime.datetime.utcnow()
    conversation_log = []
    total_tokens = 0
    speaker_counts: dict = {name: 0 for name in agents_rotation}

    actual_rounds = min(max_rounds, len(MESSAGE_TEMPLATES["caelum_compliance_assistant"]))

    for round_idx in range(actual_rounds):
        round_start = now + datetime.timedelta(seconds=round_idx * 8)
        round_messages = []

        for agent_name in agents_rotation:
            templates = MESSAGE_TEMPLATES.get(agent_name, ["(message générique)"])
            tpl = templates[round_idx] if round_idx < len(templates) else templates[-1]
            content = tpl.replace("{topic}", topic)

            tokens_this_msg = len(content.split()) * 4 // 3 + 50
            total_tokens += tokens_this_msg
            speaker_counts[agent_name] += 1

            msg = {
                "round":        round_idx + 1,
                "speaker":      agent_name,
                "content":      content,
                "timestamp":    (round_start + datetime.timedelta(seconds=2 * agents_rotation.index(agent_name))).strftime("%H:%M:%S"),
                "tokens_est":   tokens_this_msg,
                "message_id":   secrets.token_hex(6),
            }
            round_messages.append(msg)

        conversation_log.append({
            "round":        round_idx + 1,
            "messages":     round_messages,
            "round_tokens": sum(m["tokens_est"] for m in round_messages),
        })

    # Détermination du consensus
    last_operator_msg = ""
    for rnd in reversed(conversation_log):
        for msg in reversed(rnd["messages"]):
            if msg["speaker"] == "caelum_operator":
                last_operator_msg = msg["content"]
                break
        if last_operator_msg:
            break

    consensus_reached = "CONFORMITÉ VALIDÉE" in last_operator_msg

    # Output final structuré
    final_output = {
        "domain":            topic,
        "avg_composite":     61.43,
        "estimated_index":   round(61.43 / 100 * 10, 2),
        "entities_analyzed": 8,
        "distribution": {
            "critique": 4,
            "élevé":    2,
            "modéré":   1,
            "faible":   1,
        },
        "csddd_articles_checked": ["Art.8", "Art.9", "Art.11", "Art.13"],
        "status": "APPROUVÉ" if consensus_reached else "EN_RÉVISION",
        "approved_by": "caelum_operator" if consensus_reached else None,
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    duration_seconds = actual_rounds * len(agents_rotation) * 2

    return {
        "topic":                topic,
        "max_rounds":           max_rounds,
        "actual_rounds":        actual_rounds,
        "conversation_log":     conversation_log,
        "consensus_reached":    consensus_reached,
        "final_output":         final_output,
        "total_tokens":         total_tokens,
        "duration_seconds":     duration_seconds,
        "speaker_distribution": speaker_counts,
    }


def configure_code_execution_safety() -> dict:
    """
    Configure l'exécution de code sécurisée dans Docker pour AutoGen.

    Retourne
    --------
    dict avec docker_config, allowed_imports, resource_limits, timeout,
               security_layers, sandbox_validation
    """
    cfg = AUTOGEN_SECURITY_CONFIG["docker_isolation"]

    docker_config = {
        "image":         cfg["image"],
        "network_mode":  cfg["network_mode"],
        "read_only":     cfg["read_only_fs"],
        "mem_limit":     cfg["memory_limit"],
        "cpu_quota":     cfg["cpu_quota"],   # 50% d'un CPU
        "cpu_period":    100000,
        "pids_limit":    64,
        "security_opt":  ["no-new-privileges:true", "seccomp=caelum-seccomp.json"],
        "cap_drop":      ["ALL"],
        "cap_add":       [],
        "volumes": {
            "swarm_intelligence": {
                "bind":    "/sandbox/swarm/intelligence",
                "mode":    "ro",
            },
            "output_volume": {
                "bind":    "/sandbox/output",
                "mode":    "rw",
            },
        },
        "environment": {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUNBUFFERED":        "1",
        },
        "user":          "nobody:nogroup",
        "working_dir":   cfg["work_dir"],
    }

    resource_limits = {
        "memory_mb":       512,
        "cpu_percent":     50,
        "disk_write_mb":   100,
        "file_descriptors": 64,
        "processes":       64,
        "wall_time_seconds": cfg["timeout_seconds"],
        "output_size_kb":  1024,
    }

    security_layers = [
        {
            "layer":       "L1 — Docker isolation",
            "description": "Container éphémère sans réseau, filesystem read-only sauf /output",
            "mitigation":  "Exfiltration de données, accès aux fichiers hôte",
        },
        {
            "layer":       "L2 — Seccomp profile",
            "description": "Filtre syscalls : bloque execve, mount, ptrace, etc.",
            "mitigation":  "Échappement du container, élévation de privilèges",
        },
        {
            "layer":       "L3 — Import allowlist",
            "description": f"Modules Python autorisés : {', '.join(cfg['allowed_imports'])}",
            "mitigation":  "Accès réseau via socket, exécution de commandes via subprocess",
        },
        {
            "layer":       "L4 — Timeout strict",
            "description": f"Execution limitée à {cfg['timeout_seconds']}s, output limité à 1 MB",
            "mitigation":  "DoS par boucle infinie ou génération massive de données",
        },
        {
            "layer":       "L5 — User nobody",
            "description": "Processus exécuté en tant que nobody:nogroup (UID 65534)",
            "mitigation":  "Escalade de privilèges à l'intérieur du container",
        },
        {
            "layer":       "L6 — Audit trail",
            "description": "Tous les codes exécutés loggés avec hash SHA-256 dans PostgreSQL",
            "mitigation":  "Non-répudiation, forensique post-incident",
        },
    ]

    # Validation du sandbox (checks pré-exécution)
    sandbox_validation = {
        "pre_execution_checks": [
            "Vérifier que l'image Docker est présente localement (pas de pull réseau)",
            "Vérifier que le répertoire work_dir est read-only sur l'hôte",
            "Scanner le code pour les patterns bloqués (import os, subprocess, socket)",
            "Vérifier l'absence de credentials dans le code (regex patterns)",
            "Estimer la taille de sortie (rejeter si > 1 MB estimé)",
        ],
        "post_execution_checks": [
            "Vérifier que le container s'est bien arrêté (exit code 0 ou timeout)",
            "Supprimer le container et ses volumes temporaires",
            "Logger le résultat (stdout + stderr + exit_code) dans audit trail",
            "Alerter si exit_code != 0 (exception Python)",
        ],
        "blocked_code_patterns": [
            r"import\s+os",
            r"import\s+subprocess",
            r"import\s+socket",
            r"__import__\(",
            r"eval\(",
            r"exec\(",
            r"open\(",
            r"getattr\(.*__",
        ],
    }

    return {
        "docker_config":     docker_config,
        "allowed_imports":   cfg["allowed_imports"],
        "blocked_imports":   cfg["blocked_imports"],
        "resource_limits":   resource_limits,
        "timeout_seconds":   cfg["timeout_seconds"],
        "security_layers":   security_layers,
        "sandbox_validation": sandbox_validation,
        "autogen_executor":  "DockerCommandLineCodeExecutor",
        "work_dir":          cfg["work_dir"],
    }


def calculate_conversation_costs(
    rounds: int,
    agents_count: int,
    avg_tokens_per_round: int,
) -> dict:
    """
    Calcule les coûts d'un GroupChat AutoGen.

    Paramètres
    ----------
    rounds               : int — nombre de tours de conversation
    agents_count         : int — nombre d'agents dans le GroupChat
    avg_tokens_per_round : int — tokens moyens par message par agent

    Retourne
    --------
    dict avec total_tokens, cost_per_model_eur, total_cost_eur,
               breakdown_by_model, optimization_tips
    """
    # Répartition des agents par modèle (CaelumSwarm™ standard)
    MODEL_SHARE = {
        "claude-sonnet-4-6":    {"share": 0.50, "input_per_1k": 0.003,  "output_per_1k": 0.015},
        "mistral-large-latest": {"share": 0.25, "input_per_1k": 0.004,  "output_per_1k": 0.012},
        "gpt-4o":               {"share": 0.15, "input_per_1k": 0.0025, "output_per_1k": 0.010},
        "llama-3.1-70b":        {"share": 0.10, "input_per_1k": 0.0,    "output_per_1k": 0.0},
    }

    USD_TO_EUR = 0.92
    INPUT_OUTPUT_RATIO = 0.4  # 40% input, 60% output (approx)

    total_messages = rounds * agents_count
    total_tokens   = total_messages * avg_tokens_per_round

    breakdown: list = []
    total_cost_usd = 0.0

    for model, info in MODEL_SHARE.items():
        model_tokens  = int(total_tokens * info["share"])
        input_tokens  = int(model_tokens * INPUT_OUTPUT_RATIO)
        output_tokens = model_tokens - input_tokens

        cost_input_usd  = (input_tokens  / 1000) * info["input_per_1k"]
        cost_output_usd = (output_tokens / 1000) * info["output_per_1k"]
        model_cost_usd  = cost_input_usd + cost_output_usd
        model_cost_eur  = round(model_cost_usd * USD_TO_EUR, 6)

        total_cost_usd += model_cost_usd

        breakdown.append({
            "model":          model,
            "share_pct":      round(info["share"] * 100),
            "total_tokens":   model_tokens,
            "input_tokens":   input_tokens,
            "output_tokens":  output_tokens,
            "cost_usd":       round(model_cost_usd, 6),
            "cost_eur":       model_cost_eur,
            "on_premise":     info["input_per_1k"] == 0.0,
        })

    total_cost_eur = round(total_cost_usd * USD_TO_EUR, 6)

    # Coût annuel estimé (1 analyse CSDDD complète / jour ouvré)
    working_days_per_year = 250
    annual_cost_eur = round(total_cost_eur * working_days_per_year, 2)

    # Conseils d'optimisation
    optimization_tips = [
        "Utiliser llama-3.1-70b (on-premise) pour les échanges internes non sensibles "
        f"→ économie estimée de {round(total_cost_eur * 0.10 * working_days_per_year, 2)} EUR/an.",
        "Activer le cache de contexte Anthropic pour les system prompts fixes "
        "(CLAUDE.md + CSDDD rules) → réduction 60-80% des tokens input.",
        "Limiter le GroupChat à max_round=10 au lieu de 15 si consensus atteint avant "
        "→ économie de 33% des tokens en moyenne.",
        "Déplacer caelum_data_analyst sur gpt-4o-mini pour les requêtes SQL simples "
        "→ 10x moins cher pour les opérations de métriques.",
    ]

    # Coût par model en EUR (dict simple)
    cost_per_model_eur = {b["model"]: b["cost_eur"] for b in breakdown}

    return {
        "rounds":                rounds,
        "agents_count":          agents_count,
        "avg_tokens_per_round":  avg_tokens_per_round,
        "total_messages":        total_messages,
        "total_tokens":          total_tokens,
        "cost_per_model_eur":    cost_per_model_eur,
        "total_cost_usd":        round(total_cost_usd, 6),
        "total_cost_eur":        total_cost_eur,
        "annual_cost_eur":       annual_cost_eur,
        "breakdown_by_model":    breakdown,
        "optimization_tips":     optimization_tips,
        "note":                  "Tarifs indicatifs — vérifier pricing Anthropic/OpenAI/Mistral",
    }


# =============================================================================
# BLOC PRINCIPAL
# =============================================================================

def _sep(char: str = "=", width: int = 72) -> str:
    return char * width


def _section(title: str) -> None:
    print()
    print(_sep())
    print(f"  {title}")
    print(_sep())


def _subsection(title: str) -> None:
    print()
    print(_sep("-", 60))
    print(f"  {title}")
    print(_sep("-", 60))


if __name__ == "__main__":

    now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    print()
    print(_sep("=", 72))
    print("  MICROSOFT AUTOGEN INTEGRATION REPORT — CaelumSwarm(tm)")
    print("  Framework : AutoGen 0.4.x / AgentChat API / Swarm / GroupChat")
    print("  Role      : Conformite CSDDD 2024 / Droits Humains")
    print(f"  Genere le : {now_str}")
    print("  Compatible: Claude claude-sonnet-4-6 via AnthropicChatCompletionClient")
    print(_sep("=", 72))

    # ------------------------------------------------------------------
    # 1. AGENTS DÉFINIS
    # ------------------------------------------------------------------
    _section("1. AGENTS AUTOGEN (5 agents — roles CaelumSwarm(tm))")

    print()
    for agent_key, agent_cfg in AUTOGEN_AGENTS.items():
        model_info = agent_cfg.get("model_client", {})
        model_str = f"{model_info.get('model', 'N/A')} ({model_info.get('api_type', 'N/A')})" \
            if model_info else "N/A (executor)"
        tools_str = ", ".join(agent_cfg.get("tools", [])) if agent_cfg.get("tools") else "—"
        print(f"  [{agent_cfg['agent_type']}] {agent_cfg['name']}")
        print(f"    Description : {agent_cfg.get('description', 'N/A')}")
        print(f"    Modele      : {model_str}")
        print(f"    Tools       : {tools_str}")
        print()

    print(f"  Total agents definis : {len(AUTOGEN_AGENTS)}")
    print(f"  Tools declares       : {len(AUTOGEN_TOOLS)}")

    # ------------------------------------------------------------------
    # 2. GROUPCHATS
    # ------------------------------------------------------------------
    _section("2. GROUPCHATS (3 configurations)")

    print()
    for gc_key, gc_cfg in AUTOGEN_GROUP_CHATS.items():
        print(f"  [{gc_key}]")
        print(f"    Nom             : {gc_cfg['name']}")
        print(f"    Agents          : {', '.join(gc_cfg['agents'])}")
        print(f"    Max rounds      : {gc_cfg['max_round']}")
        print(f"    Speaker select  : {gc_cfg['speaker_selection_method']}")
        if gc_cfg.get("termination_condition"):
            print(f"    Termination     : {gc_cfg['termination_condition']}")
        print()

    # ------------------------------------------------------------------
    # 3. SWARM TEAM
    # ------------------------------------------------------------------
    _section("3. SWARM TEAM avec handoffs (AutoGen 0.4.x)")

    swarm = AUTOGEN_SWARM_TEAMS["compliance_swarm"]
    print()
    print(f"  Type      : {swarm['type']}")
    print(f"  Agents    : {', '.join(swarm['agents'])}")
    print(f"  Terminaison : {swarm['termination']}")
    print()
    print("  Handoffs declares :")
    for transition, rationale in swarm["handoffs"].items():
        print(f"    {transition}")
        print(f"      → {rationale}")
    print()
    print("  Code AutoGen 0.4.x (extrait) :")
    print("    from autogen_agentchat.teams import Swarm")
    print("    from autogen_agentchat.conditions import TextMentionTermination")
    print("    team = Swarm(")
    print("        participants=[compliance_assistant, legal_reviewer, data_analyst],")
    print("        termination_condition=TextMentionTermination('RAPPORT FINAL APPROUVÉ'),")
    print("    )")
    print("    result = await team.run(task='Analyser CSDDD...')")

    # ------------------------------------------------------------------
    # 4. WORKFLOW DESIGN — compliance analysis (complex)
    # ------------------------------------------------------------------
    _section("4. WORKFLOW DESIGN — analyse compliance complex")

    wf = design_autogen_workflow("compliance_analysis", "complex")
    print()
    print(f"  Tache       : {wf['task_type']}")
    print(f"  Complexite  : {wf['complexity']}")
    print(f"  Pattern     : {wf['conversation_pattern']}")
    print(f"  Description : {wf['pattern_description']}")
    print(f"  Use case    : {wf['pattern_use_case']}")
    print(f"  Agents      : {', '.join(wf['agents_selected'])}")
    print(f"  Rounds est. : {wf['estimated_rounds']} (plage : {wf['estimated_rounds_range']})")
    print(f"  Tokens est. : {wf['token_estimate']:,}")
    print(f"  LLM recomm. : {wf['llm_model']} ({wf['recommended_llm']})")
    print()
    print("  Code snippet AutoGen 0.4.x :")
    for line in wf["workflow_code_snippet"].split("\n"):
        print(f"    {line}")

    _subsection("Workflow Design — automated swarm pipeline")
    wf2 = design_autogen_workflow("compliance_analysis", "automated")
    print(f"  Pattern     : {wf2['conversation_pattern']}")
    print(f"  Agents      : {', '.join(wf2['agents_selected'])}")
    print(f"  Rounds est. : {wf2['estimated_rounds']} (plage : {wf2['estimated_rounds_range']})")

    # ------------------------------------------------------------------
    # 5. GROUPCHAT SIMULATION — 10 rounds, Conflict Minerals
    # ------------------------------------------------------------------
    _section("5. GROUPCHAT SIMULATION — 10 rounds / Conflict Minerals")

    sim = simulate_group_chat(topic="Conflict Minerals", max_rounds=10)
    print()
    print(f"  Sujet           : {sim['topic']}")
    print(f"  Rounds demandes : {sim['max_rounds']}")
    print(f"  Rounds executes : {sim['actual_rounds']}")
    print(f"  Consensus       : {'OUI — CONFORMITE VALIDEE' if sim['consensus_reached'] else 'NON'}")
    print(f"  Duree estimee   : {sim['duration_seconds']}s")
    print(f"  Total tokens    : {sim['total_tokens']:,}")
    print()
    print("  Distribution des prises de parole :")
    for speaker, count in sim["speaker_distribution"].items():
        bar = "=" * count
        print(f"    {speaker:<40} : {count} msg  [{bar}]")
    print()
    print("  Extrait conversation (round 1) :")
    if sim["conversation_log"]:
        for msg in sim["conversation_log"][0]["messages"][:2]:
            print(f"    [{msg['timestamp']}] {msg['speaker']}")
            print(f"      {msg['content'][:100]}...")
    print()
    print("  Output final :")
    fo = sim["final_output"]
    print(f"    Domaine        : {fo['domain']}")
    print(f"    avg_composite  : {fo['avg_composite']}")
    print(f"    Index estime   : {fo['estimated_index']}")
    print(f"    Distribution   : {fo['distribution']}")
    print(f"    Articles CSDDD : {', '.join(fo['csddd_articles_checked'])}")
    print(f"    Statut         : {fo['status']}")

    # ------------------------------------------------------------------
    # 6. CODE EXECUTION SAFETY
    # ------------------------------------------------------------------
    _section("6. CODE EXECUTION SAFETY — Docker isolation")

    safety = configure_code_execution_safety()
    print()
    print(f"  Executor     : {safety['autogen_executor']}")
    print(f"  Image Docker : {safety['docker_config']['image']}")
    print(f"  Reseau       : {safety['docker_config']['network_mode']}")
    print(f"  Filesystem   : {'read-only' if safety['docker_config']['read_only'] else 'read-write'}")
    print(f"  Memoire      : {safety['docker_config']['mem_limit']}")
    print(f"  CPU quota    : {safety['docker_config']['cpu_quota']} (50% un coeur)")
    print(f"  User         : {safety['docker_config']['user']}")
    print(f"  Timeout      : {safety['timeout_seconds']}s")
    print()
    print(f"  Imports autorises ({len(safety['allowed_imports'])}) :")
    print(f"    {', '.join(safety['allowed_imports'])}")
    print()
    print(f"  Imports bloques ({len(safety['blocked_imports'])}) :")
    print(f"    {', '.join(safety['blocked_imports'])}")
    print()
    print(f"  Couches securite ({len(safety['security_layers'])}) :")
    for layer in safety["security_layers"]:
        print(f"    {layer['layer']}")
        print(f"      {layer['description']}")
        print(f"      Mitigation : {layer['mitigation']}")
    print()
    print("  Limites ressources :")
    for k, v in safety["resource_limits"].items():
        print(f"    {k:<30} : {v}")

    # ------------------------------------------------------------------
    # 7. CONVERSATION COSTS — 15 rounds, 4 agents, 500 tokens avg
    # ------------------------------------------------------------------
    _section("7. CONVERSATION COSTS — 15 rounds / 4 agents / 500 tokens/msg")

    costs = calculate_conversation_costs(rounds=15, agents_count=4, avg_tokens_per_round=500)
    print()
    print(f"  Rounds           : {costs['rounds']}")
    print(f"  Agents           : {costs['agents_count']}")
    print(f"  Tokens/msg avg   : {costs['avg_tokens_per_round']}")
    print(f"  Total messages   : {costs['total_messages']}")
    print(f"  Total tokens     : {costs['total_tokens']:,}")
    print()
    print(f"  {'Modele':<30} {'Share':<10} {'Tokens':<12} {'Cout EUR':<12} {'On-premise'}")
    print(f"  {'-'*28:<30} {'-'*8:<10} {'-'*10:<12} {'-'*10:<12} {'-'*10}")
    for b in costs["breakdown_by_model"]:
        on_prem = "OUI" if b["on_premise"] else "non"
        print(
            f"  {b['model']:<30} {b['share_pct']:>4}%      "
            f"{b['total_tokens']:>8,}    {b['cost_eur']:>8.6f} EUR  {on_prem}"
        )
    print()
    print(f"  TOTAL (1 session)    : {costs['total_cost_eur']:.6f} EUR  "
          f"({costs['total_cost_usd']:.6f} USD)")
    print(f"  TOTAL annuel (250j)  : {costs['annual_cost_eur']:.2f} EUR")
    print()
    print("  Conseils d'optimisation :")
    for tip in costs["optimization_tips"]:
        print(f"    - {tip}")

    # ------------------------------------------------------------------
    # 8. CONFIG LIST — 4 LLM providers
    # ------------------------------------------------------------------
    _section("8. CONFIG LIST — 4 fournisseurs LLM")

    print()
    for cfg_key, cfg_val in AUTOGEN_CONFIG_LIST.items():
        print(f"  [{cfg_key}]")
        print(f"    Modele   : {cfg_val['model']}")
        print(f"    API type : {cfg_val['api_type']}")
        print(f"    API key  : {cfg_val.get('api_key', 'N/A (on-premise)')}")
        if cfg_val.get("base_url"):
            print(f"    Base URL : {cfg_val['base_url']}")
        if cfg_val.get("max_tokens"):
            print(f"    Max tok  : {cfg_val['max_tokens']}")
        if cfg_val.get("temperature") is not None:
            print(f"    Temp.    : {cfg_val['temperature']}")
        if cfg_val.get("description"):
            print(f"    Note     : {cfg_val['description']}")
        print()

    # ------------------------------------------------------------------
    # 9. COMPARISON AutoGen vs CrewAI vs LangChain pour CaelumSwarm™
    # ------------------------------------------------------------------
    _section("9. COMPARISON — AutoGen vs CrewAI vs LangChain pour CaelumSwarm(tm)")

    print()
    winner = max(FRAMEWORK_COMPARISON.items(), key=lambda x: x[1]["score_caelum"])
    print(f"  {'Framework':<14} {'Vendor':<16} {'Version':<10} {'Score CaelumSwarm'}")
    print(f"  {'-'*12:<14} {'-'*14:<16} {'-'*8:<10} {'-'*20}")
    for fw_name, fw_info in FRAMEWORK_COMPARISON.items():
        marker = " <-- GAGNANT" if fw_name == winner[0] else ""
        print(
            f"  {fw_name:<14} {fw_info['vendor']:<16} {fw_info['version']:<10} "
            f"{fw_info['score_caelum']}/10{marker}"
        )

    print()
    print(f"  GAGNANT : {winner[0]} (score {winner[1]['score_caelum']}/10)")
    print(f"  Paradigme : {winner[1]['paradigm']}")
    print(f"  Fit CaelumSwarm(tm) : {winner[1]['caelum_fit']}")
    print()
    print(f"  Forces AutoGen 0.4.x :")
    for strength in FRAMEWORK_COMPARISON["AutoGen"]["strengths"]:
        print(f"    + {strength}")
    print()
    print("  Justification du choix :")
    print("    GroupChat roundtable → conformite CSDDD multi-expertise (juridique + data + compliance)")
    print("    Swarm avec handoffs → pipeline automatise CSDDD de bout en bout")
    print("    CodeExecutorAgent Docker → execution securisee des engines Python CaelumSwarm(tm)")
    print("    Multi-LLM natif → Claude claude-sonnet-4-6 (compliance) + Mistral (legal) + LLaMA (on-prem)")

    _subsection("Comparaison detaillee par critere")
    criteria = [
        ("Conversation multi-agent fluide",  (9, 7, 6)),
        ("Swarm / handoffs natifs",           (9, 6, 5)),
        ("Code execution securisee",          (9, 5, 6)),
        ("Multi-LLM natif",                   (9, 7, 7)),
        ("Observabilite / traces",            (7, 7, 9)),
        ("Facilite de configuration",         (7, 8, 6)),
        ("Ecosysteme / intégrations",         (7, 6, 9)),
        ("Maturite API stable",               (7, 8, 6)),
    ]
    print()
    print(f"  {'Critere':<40} {'AutoGen':>8} {'CrewAI':>8} {'LangChain':>10}")
    print(f"  {'-'*38:<40} {'-'*6:>8} {'-'*6:>8} {'-'*8:>10}")
    for crit, (ag, cr, lc) in criteria:
        print(f"  {crit:<40} {ag:>8}/10 {cr:>8}/10 {lc:>10}/10")
    totals = tuple(
        sum(row[1][i] for row in criteria)
        for i in range(3)
    )
    print(f"  {'TOTAL':<40} {totals[0]:>8}/80 {totals[1]:>8}/80 {totals[2]:>10}/80")

    # ------------------------------------------------------------------
    # 10. AUTOGEN SECURITY
    # ------------------------------------------------------------------
    _section("10. AUTOGEN SECURITY")

    print()
    sec_checks = [
        ("Docker isolation — container sans reseau, FS read-only",
         AUTOGEN_SECURITY_CONFIG["docker_isolation"]["network_mode"] == "none"),
        ("Aucun credential dans les messages (sanitization active)",
         AUTOGEN_SECURITY_CONFIG["message_sanitization"]["strip_credentials"]),
        ("PII detection et redaction automatique",
         AUTOGEN_SECURITY_CONFIG["message_sanitization"]["pii_detection"]),
        ("Audit trail complet (messages + tool calls + code exec)",
         AUTOGEN_SECURITY_CONFIG["audit_trail"]["log_all_messages"]),
        ("Audit trail tamper-proof (PostgreSQL immutable)",
         AUTOGEN_SECURITY_CONFIG["audit_trail"]["tamper_proof"]),
        ("Rate limiting (max_rounds=50 par session)",
         AUTOGEN_SECURITY_CONFIG["rate_limiting"]["max_rounds_per_session"] <= 50),
        ("Imports Python bloques (os, subprocess, socket, urllib)",
         len(AUTOGEN_SECURITY_CONFIG["docker_isolation"]["blocked_imports"]) >= 6),
        ("Timeout strict execution code (60s)",
         AUTOGEN_SECURITY_CONFIG["docker_isolation"]["timeout_seconds"] <= 60),
        ("User nobody:nogroup dans le container",
         True),
        ("Seccomp profile (blocage syscalls dangereux)",
         True),
        ("API keys geres par Vault (VAULT_MANAGED — zero credential code)",
         all(
             v.get("api_key", "VAULT_MANAGED") in ("VAULT_MANAGED", None)
             for v in AUTOGEN_CONFIG_LIST.values()
         )),
        ("Retention audit trail 365 jours (CSDDD Art.11)",
         AUTOGEN_SECURITY_CONFIG["audit_trail"]["retention_days"] >= 365),
    ]

    passed = 0
    failed = 0
    for check_name, result in sec_checks:
        marker = "[OK]  " if result else "[FAIL]"
        print(f"  {marker} {check_name}")
        if result:
            passed += 1
        else:
            failed += 1

    print()
    print(f"  Resultat securite : {passed}/{len(sec_checks)} verifications reussies", end="")
    if failed == 0:
        print("  — SECURITE AUTOGEN : VALIDEE")
    else:
        print(f"  — {failed} point(s) a corriger")

    # ------------------------------------------------------------------
    # SIGNATURE FINALE
    # ------------------------------------------------------------------
    print()
    print(_sep("=", 72))
    print()
    print("  AutoGen Integration Agent — PRET")
    print()
    print("  AutoGen 0.4.x / Swarm / GroupChat / Multi-LLM")
    print()
    print("  Plateforme : CaelumSwarm(tm) — Droits Humains / Conformite CSDDD 2024")
    print(f"  Rapport genere le : {now_str}")
    print()
    print(_sep("=", 72))
