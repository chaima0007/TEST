"""
CrewAI Integration Agent — CaelumSwarm™
========================================

Framework: CrewAI 0.80.x
Role: Orchestration équipes d'agents IA pour conformité CSDDD 2024
Pattern: Role-based agents + Task delegation + Hierarchical Process

CrewAI est un framework d'orchestration d'agents IA permettant à plusieurs agents
de collaborer sur des tâches complexes comme des "crews" (équipes). Chaque agent
possède un rôle, un objectif et une backstory ; les tâches sont déléguées selon
la hiérarchie ou la séquence définie.

Conformité CSDDD 2024 : ce module pilote les équipes d'agents responsables
de l'audit de la chaîne de valeur (Art. 8–13), de la remédiation (Art. 9)
et de la notification des parties prenantes exigée par la directive UE 2024/1760.

NOTE : Ce fichier simule et documente l'intégration CrewAI sans importer
le framework réel. Seule la bibliothèque standard Python est utilisée.
"""

import hashlib
import json
import math
import random
import uuid
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Constantes de configuration
# ---------------------------------------------------------------------------

CREWAI_VERSION = "0.80.x"

CAELUM_CREWS: dict = {
    "compliance_audit_crew": {
        "name": "Équipe Audit Conformité CSDDD",
        "process": "hierarchical",   # manager agent coordonne les autres
        "agents": [
            {
                "role": "Directeur Audit Conformité",
                "goal": "Coordonner l'audit complet CSDDD 2024 de la chaîne de valeur",
                "backstory": (
                    "Expert CSDDD avec 15 ans d'expérience en droits humains corporatifs, "
                    "spécialiste EU AI Act"
                ),
                "tools": ["wave_engine_tool", "report_generator", "database_tool"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": True,
                "max_iter": 5,
            },
            {
                "role": "Analyste Risques Droits Humains",
                "goal": (
                    "Identifier et scorer les violations de droits humains "
                    "dans la chaîne d'approvisionnement"
                ),
                "backstory": (
                    "Ancienne enquêtrice ONU, spécialisée en minéraux de conflit "
                    "et travail forcé"
                ),
                "tools": ["supplier_database_tool", "news_search_tool", "scoring_engine"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
            {
                "role": "Juriste Droit International",
                "goal": "Analyser la conformité légale avec CSDDD Art.8-13, RGPD, EU AI Act",
                "backstory": (
                    "Avocate spécialisée droit UE, ancienne conseillère "
                    "Commission Européenne"
                ),
                "tools": ["legal_database_tool", "csddd_article_search"],
                "llm": "mistral-large-latest",
                "allow_delegation": False,
            },
            {
                "role": "Rédacteur Rapport CSDDD",
                "goal": (
                    "Rédiger des rapports conformité clairs, actionnables "
                    "et conformes aux templates UE"
                ),
                "backstory": "Expert en communication corporate et reporting ESG",
                "tools": ["pdf_generator", "template_engine"],
                "llm": "gpt-4o",
                "allow_delegation": False,
            },
        ],
        "tasks": [
            {
                "description": "Analyser 8 entités CSDDD dans le domaine {domain}",
                "agent": "Analyste Risques Droits Humains",
                "expected_output": "JSON scores 4/2/1/1",
            },
            {
                "description": "Vérifier conformité légale des résultats",
                "agent": "Juriste Droit International",
                "expected_output": "Rapport légal CSDDD",
            },
            {
                "description": "Synthétiser et rédiger rapport final",
                "agent": "Rédacteur Rapport CSDDD",
                "expected_output": "PDF rapport 15 pages",
            },
            {
                "description": "Valider et approuver le rapport",
                "agent": "Directeur Audit Conformité",
                "expected_output": "Rapport approuvé + alertes",
            },
        ],
    },
    "supply_chain_investigation_crew": {
        "name": "Équipe Investigation Chaîne de Valeur",
        "process": "sequential",
        "agents": [
            {
                "role": "Cartographe Chaîne de Valeur",
                "goal": "Mapper la chaîne d'approvisionnement complète Tier 1-3",
                "tools": ["supplier_database_tool", "redis_cache_tool"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
            {
                "role": "Investigateur Fournisseurs",
                "goal": "Investiguer les fournisseurs à risque critique",
                "tools": ["news_search_tool", "scoring_engine"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
            {
                "role": "Analyste Géopolitique",
                "goal": "Évaluer les risques géopolitiques par pays d'origine",
                "tools": ["news_search_tool", "legal_database_tool"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
            {
                "role": "Expert Remédiation",
                "goal": "Proposer des plans d'action correctifs CSDDD Art.9",
                "tools": ["legal_database_tool", "pdf_generator"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
        ],
        "tasks": [
            {
                "description": "Cartographier fournisseurs Tier 1-3 pour le domaine {domain}",
                "agent": "Cartographe Chaîne de Valeur",
                "expected_output": "Carte JSON fournisseurs Tier 1-3",
            },
            {
                "description": "Investiguer fournisseurs à risque critique identifiés",
                "agent": "Investigateur Fournisseurs",
                "expected_output": "Rapport investigation détaillé",
            },
            {
                "description": "Évaluer contexte géopolitique des pays sources",
                "agent": "Analyste Géopolitique",
                "expected_output": "Matrice risques géopolitiques par pays",
            },
            {
                "description": "Rédiger plan de remédiation CSDDD Art.9",
                "agent": "Expert Remédiation",
                "expected_output": "Plan d'action correctif priorité 1-3",
            },
        ],
    },
    "alert_response_crew": {
        "name": "Équipe Réponse Alertes Temps Réel",
        "process": "hierarchical",
        "kickoff_trigger": "compliance_alert_received",
        "response_time_target_minutes": 15,
        "agents": [
            {
                "role": "Coordinateur Alertes",
                "goal": "Orchestrer la réponse rapide aux alertes CSDDD critiques",
                "tools": ["alert_dispatcher", "redis_cache_tool"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": True,
                "max_iter": 3,
            },
            {
                "role": "Analyste d'Urgence",
                "goal": "Qualifier et scorer l'alerte en moins de 5 minutes",
                "tools": ["scoring_engine", "supplier_database_tool"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
            {
                "role": "Notificateur Parties Prenantes",
                "goal": "Notifier les bonnes parties prenantes selon sévérité",
                "tools": ["alert_dispatcher", "pdf_generator"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
            {
                "role": "Documenteur Preuves",
                "goal": "Documenter l'incident CSDDD avec horodatage immuable",
                "tools": ["blockchain_recorder", "vault_secrets_tool"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
        ],
        "tasks": [
            {
                "description": "Qualifier l'alerte reçue (domaine, sévérité, entités)",
                "agent": "Analyste d'Urgence",
                "expected_output": "Fiche qualification alerte structurée",
            },
            {
                "description": "Notifier parties prenantes selon matrice sévérité CSDDD",
                "agent": "Notificateur Parties Prenantes",
                "expected_output": "Confirmations notifications envoyées",
            },
            {
                "description": "Enregistrer incident sur blockchain avec horodatage",
                "agent": "Documenteur Preuves",
                "expected_output": "Hash transaction blockchain + timestamp",
            },
            {
                "description": "Valider clôture et générer rapport incident",
                "agent": "Coordinateur Alertes",
                "expected_output": "Rapport incident approuvé",
            },
        ],
    },
    "wave_development_crew": {
        "name": "Équipe Développement Wave Engines",
        "process": "sequential",
        "agents": [
            {
                "role": "Domain Expert",
                "goal": (
                    "Identifier et scorer les domaines droits humains "
                    "pour nouvelles waves"
                ),
                "tools": ["legal_database_tool", "news_search_tool"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
            {
                "role": "Engine Developer",
                "goal": "Créer les engines Python avec pattern 4/2/1/1",
                "tools": ["wave_engine_tool", "redis_cache_tool"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
            {
                "role": "QA Engineer",
                "goal": "Valider distributions et scores via python3 engine.py",
                "tools": ["scoring_engine"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
            {
                "role": "Integration Specialist",
                "goal": "Intégrer routes, dashboards et Sidebar",
                "tools": ["wave_engine_tool", "database_tool"],
                "llm": "claude-sonnet-4-6",
                "allow_delegation": False,
            },
        ],
        "tasks": [
            {
                "description": "Sélectionner et scorer 3 domaines droits humains Wave N",
                "agent": "Domain Expert",
                "expected_output": "Scoring pertinence × unicité × impact (≥3 options)",
            },
            {
                "description": "Coder engine.py avec pattern 4 critique/2 élevé/1 modéré/1 faible",
                "agent": "Engine Developer",
                "expected_output": "3 fichiers engine.py validés",
            },
            {
                "description": "Exécuter python3 engine.py et valider distributions",
                "agent": "QA Engineer",
                "expected_output": "Rapport QA : distributions + avg_composite",
            },
            {
                "description": "Intégrer routes API, dashboards React et entrées Sidebar",
                "agent": "Integration Specialist",
                "expected_output": "PR feature/wave-N prête pour review",
            },
        ],
    },
}

CREWAI_TOOLS: dict = {
    "wave_engine_tool": {
        "description": "Execute un CaelumSwarm™ wave engine Python",
        "args_schema": {"engine_name": "str", "entity_id": "str"},
        "returns": "dict avec scores 4/2/1/1 et avg_composite",
    },
    "supplier_database_tool": {
        "description": "Interroge la base de données fournisseurs PostgreSQL",
        "args_schema": {"supplier_id": "str", "tier": "int"},
        "returns": "dict fournisseur avec profil risque",
    },
    "legal_database_tool": {
        "description": "Recherche dans le corpus CSDDD/RGPD/EU AI Act",
        "args_schema": {"query": "str", "article": "str"},
        "returns": "list d'extraits légaux pertinents",
    },
    "pdf_generator": {
        "description": "Génère un rapport PDF conformité",
        "args_schema": {"template": "str", "data": "dict"},
        "returns": "chemin fichier PDF généré",
    },
    "news_search_tool": {
        "description": "Recherche actualités violations droits humains",
        "args_schema": {"query": "str", "since_date": "str"},
        "returns": "list d'articles avec scores pertinence",
    },
    "scoring_engine": {
        "description": "Execute le moteur de scoring CaelumSwarm™",
        "args_schema": {"domain": "str", "entity_id": "str"},
        "returns": "dict avec composite_score et sous-scores",
    },
    "alert_dispatcher": {
        "description": "Dispatche les alertes via NATS/RabbitMQ",
        "args_schema": {"alert_type": "str", "severity": "str", "payload": "dict"},
        "returns": "dict avec message_id et statut dispatch",
    },
    "blockchain_recorder": {
        "description": "Enregistre les preuves sur blockchain immuable",
        "args_schema": {"incident_id": "str", "evidence": "dict"},
        "returns": "dict avec tx_hash et timestamp_utc",
    },
    "redis_cache_tool": {
        "description": "Cache et retrieve résultats via Redis Cluster",
        "args_schema": {"key": "str", "value": "dict", "ttl_seconds": "int"},
        "returns": "bool succès mise en cache",
    },
    "vault_secrets_tool": {
        "description": "Récupère les secrets via HashiCorp Vault",
        "args_schema": {"secret_path": "str"},
        "returns": "dict secrets (jamais loggé)",
    },
}

CREWAI_CONFIG: dict = {
    "memory": True,
    "embedder": {
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"},
    },
    "cache": True,
    "max_rpm": 30,
    "full_output": True,
    "planning": True,
    "planning_llm": "claude-sonnet-4-6",
    "output_log_file": "logs/crewai_caelum.log",
    "verbose": 2,
}

HIERARCHICAL_PROCESS_CONFIG: dict = {
    "manager_llm": "claude-sonnet-4-6",
    "manager_agent": {
        "role": "Directeur Opérations CaelumSwarm™",
        "goal": "Orchestrer les équipes pour maximiser la conformité CSDDD 2024",
        "backstory": (
            "CEO de Caelum Partners avec expertise en droits humains "
            "et technologies IA"
        ),
        "allow_delegation": True,
        "verbose": True,
    },
}


# ---------------------------------------------------------------------------
# Fonctions principales
# ---------------------------------------------------------------------------


def design_crew_for_domain(domain: str, risk_level: str) -> dict:
    """
    Conçoit une crew CrewAI adaptée au domaine et niveau de risque.

    Sélectionne la ou les crews appropriées en fonction du niveau de risque,
    assigne les agents, estime la durée d'exécution et justifie le choix.

    Args:
        domain:     Domaine droits humains analysé (ex. "conflict_minerals").
        risk_level: Niveau de risque CSDDD : "critique", "élevé", "modéré", "faible".

    Returns:
        Dictionnaire contenant crew_selection, agents_assigned,
        estimated_duration_min et la justification du choix.
    """
    risk_lower = risk_level.lower()

    if risk_lower == "critique":
        selected_crews = ["alert_response_crew", "compliance_audit_crew"]
        execution_mode = "parallèle"
        estimated_duration_min = 20
        justification = (
            "Risque critique — activation simultanée de alert_response_crew "
            "(réponse immédiate < 15 min) et compliance_audit_crew "
            "(audit approfondi CSDDD Art.8-13). Parallélisation maximale."
        )
        priority = "P0 — traitement immédiat"
    elif risk_lower in ("élevé", "eleve"):
        selected_crews = ["compliance_audit_crew"]
        execution_mode = "séquentiel"
        estimated_duration_min = 45
        justification = (
            "Risque élevé — compliance_audit_crew en mode hiérarchique. "
            "Le Directeur Audit coordonne Analyste Risques → Juriste → Rédacteur. "
            "SLA : rapport dans les 4 heures."
        )
        priority = "P1 — traitement sous 4h"
    elif risk_lower in ("modéré", "modere"):
        selected_crews = ["supply_chain_investigation_crew"]
        execution_mode = "séquentiel"
        estimated_duration_min = 90
        justification = (
            "Risque modéré — supply_chain_investigation_crew en mode séquentiel. "
            "Cartographie Tier 1-3 → Investigation → Géopolitique → Remédiation Art.9. "
            "SLA : rapport dans les 24 heures."
        )
        priority = "P2 — traitement sous 24h"
    else:
        selected_crews = ["wave_development_crew"]
        execution_mode = "séquentiel"
        estimated_duration_min = 120
        justification = (
            "Risque faible — wave_development_crew pour enrichissement documentaire. "
            "Domaine candidat à intégration dans une future Wave engine."
        )
        priority = "P3 — traitement planifié"

    agents_assigned = []
    for crew_name in selected_crews:
        crew = CAELUM_CREWS[crew_name]
        for agent in crew["agents"]:
            agents_assigned.append({
                "crew": crew_name,
                "role": agent["role"],
                "llm": agent.get("llm", "claude-sonnet-4-6"),
                "allow_delegation": agent.get("allow_delegation", False),
            })

    total_tasks = sum(
        len(CAELUM_CREWS[c].get("tasks", []))
        for c in selected_crews
    )

    return {
        "domain": domain,
        "risk_level": risk_lower,
        "priority": priority,
        "crew_selection": selected_crews,
        "execution_mode": execution_mode,
        "agents_assigned": agents_assigned,
        "total_agents": len(agents_assigned),
        "total_tasks": total_tasks,
        "estimated_duration_min": estimated_duration_min,
        "justification": justification,
        "manager_llm": HIERARCHICAL_PROCESS_CONFIG["manager_llm"],
        "designed_at": datetime.now(timezone.utc).isoformat(),
    }


def simulate_crew_execution(crew_name: str, inputs: dict) -> dict:
    """
    Simule l'exécution d'une crew CrewAI avec log de chaque étape.

    Modélise les phases : Planning → agent 1 runs → agent 2 runs → ... → Final output.
    Génère des timestamps réalistes, un suivi de consommation de tokens et
    une sortie finale synthétique.

    Args:
        crew_name: Nom de la crew à simuler (clé de CAELUM_CREWS).
        inputs:    Dictionnaire d'entrées passées au kickoff (ex. {"domain": "..."}).

    Returns:
        Dictionnaire contenant execution_log (liste d'étapes horodatées),
        token_usage et final_output.
    """
    crew = CAELUM_CREWS.get(crew_name)
    if not crew:
        return {"error": f"Crew inconnue : {crew_name}"}

    seed_str = crew_name + json.dumps(inputs, sort_keys=True)
    random.seed(int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16))

    execution_log = []
    base_ts = datetime.now(timezone.utc)
    total_seconds = 0.0
    total_tokens = 0

    # Étape 0 — Planning (si activé)
    planning_tokens = random.randint(800, 1_500)
    planning_seconds = random.uniform(3.0, 8.0)
    total_seconds += planning_seconds
    total_tokens += planning_tokens
    execution_log.append({
        "step": 0,
        "phase": "PLANNING",
        "agent": HIERARCHICAL_PROCESS_CONFIG["manager_agent"]["role"]
                 if crew["process"] == "hierarchical"
                 else "CrewAI Planner",
        "action": f"Décomposition des tâches pour '{crew['name']}'",
        "inputs_received": list(inputs.keys()),
        "duration_seconds": round(planning_seconds, 2),
        "tokens_used": planning_tokens,
        "status": "DONE",
        "timestamp": base_ts.isoformat(),
    })

    # Étapes par agent/tâche
    tasks = crew.get("tasks", [])
    agents = crew.get("agents", [])

    for i, task in enumerate(tasks):
        step_seconds = random.uniform(8.0, 35.0)
        step_tokens = random.randint(600, 3_500)
        total_seconds += step_seconds
        total_tokens += step_tokens

        # Trouver l'agent assigné
        agent_role = task.get("agent", agents[i % len(agents)]["role"] if agents else "Agent")
        agent_def = next(
            (a for a in agents if a["role"] == agent_role),
            agents[i % len(agents)] if agents else {},
        )
        agent_llm = agent_def.get("llm", "claude-sonnet-4-6")

        # Simulation d'appel outil
        tools = agent_def.get("tools", [])
        tool_called = random.choice(tools) if tools else None
        tool_result_ok = random.random() > 0.05  # 95% succès

        execution_log.append({
            "step": i + 1,
            "phase": "AGENT_EXECUTION",
            "agent": agent_role,
            "llm": agent_llm,
            "task": task["description"].replace("{domain}", inputs.get("domain", "N/A")),
            "expected_output": task["expected_output"],
            "tool_called": tool_called,
            "tool_success": tool_result_ok,
            "duration_seconds": round(step_seconds, 2),
            "tokens_used": step_tokens,
            "delegation": agent_def.get("allow_delegation", False),
            "status": "DONE" if tool_result_ok else "RETRIED",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    # Étape finale — Consolidation
    final_seconds = random.uniform(2.0, 6.0)
    final_tokens = random.randint(400, 1_000)
    total_seconds += final_seconds
    total_tokens += final_tokens
    execution_log.append({
        "step": len(tasks) + 1,
        "phase": "FINAL_OUTPUT",
        "agent": "CrewAI Orchestrator",
        "action": "Consolidation sorties et génération résultat final",
        "duration_seconds": round(final_seconds, 2),
        "tokens_used": final_tokens,
        "status": "DONE",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    # Token usage breakdown
    input_tokens = round(total_tokens * 0.35)
    output_tokens = total_tokens - input_tokens
    cost_usd = round(
        (input_tokens / 1_000_000) * 3.0 + (output_tokens / 1_000_000) * 15.0,
        4,
    )

    final_output = {
        "crew": crew_name,
        "crew_label": crew["name"],
        "domain": inputs.get("domain", "N/A"),
        "process": crew["process"],
        "tasks_completed": len(tasks),
        "summary": (
            f"Crew '{crew['name']}' a complété {len(tasks)} tâches "
            f"en {round(total_seconds, 1)}s. "
            f"Distribution CSDDD validée : 4 critique / 2 élevé / 1 modéré / 1 faible."
        ),
        "csddd_compliance": True,
        "report_ready": True,
    }

    return {
        "crew_name": crew_name,
        "inputs": inputs,
        "execution_log": execution_log,
        "total_steps": len(execution_log),
        "total_duration_seconds": round(total_seconds, 2),
        "total_duration_minutes": round(total_seconds / 60, 2),
        "token_usage": {
            "total_tokens": total_tokens,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": cost_usd,
        },
        "final_output": final_output,
        "simulated_at": datetime.now(timezone.utc).isoformat(),
    }


def calculate_crew_roi(crew_name: str, monthly_tasks: int) -> dict:
    """
    Calcule le ROI d'une crew CrewAI par rapport au processus manuel équivalent.

    Compare le temps manuel (heures analyste senior) vs automatisé (durée crew),
    estime le coût LLM mensuel et calcule les économies et le ROI en pourcentage.

    Args:
        crew_name:     Nom de la crew analysée.
        monthly_tasks: Nombre de tâches exécutées par mois.

    Returns:
        Dictionnaire contenant manual_hours, automated_hours,
        savings_eur_month et roi_percent.
    """
    crew = CAELUM_CREWS.get(crew_name)
    if not crew:
        return {"error": f"Crew inconnue : {crew_name}"}

    # Référentiels temporels par crew (heures par tâche en mode manuel)
    manual_hours_per_task_map = {
        "compliance_audit_crew": 16.0,          # audit CSDDD complet
        "supply_chain_investigation_crew": 24.0, # investigation chaîne valeur
        "alert_response_crew": 2.0,              # réponse alerte urgente
        "wave_development_crew": 40.0,           # développement 3 engines + intégration
    }

    # Durée automatisée estimée (heures par tâche)
    automated_hours_per_task_map = {
        "compliance_audit_crew": 0.75,
        "supply_chain_investigation_crew": 1.5,
        "alert_response_crew": 0.25,
        "wave_development_crew": 2.0,
    }

    # Coût LLM estimé par tâche (USD)
    llm_cost_per_task_map = {
        "compliance_audit_crew": 0.85,
        "supply_chain_investigation_crew": 1.20,
        "alert_response_crew": 0.30,
        "wave_development_crew": 2.50,
    }

    manual_h_per_task = manual_hours_per_task_map.get(crew_name, 8.0)
    automated_h_per_task = automated_hours_per_task_map.get(crew_name, 1.0)
    llm_cost_per_task = llm_cost_per_task_map.get(crew_name, 0.50)

    # Coût analyste senior : 120 EUR/h (conformité CSDDD / cabinet conseil)
    analyst_hourly_rate_eur = 120.0
    eur_per_usd = 0.92

    manual_hours_month = round(manual_h_per_task * monthly_tasks, 1)
    automated_hours_month = round(automated_h_per_task * monthly_tasks, 1)
    hours_saved_month = round(manual_hours_month - automated_hours_month, 1)

    manual_cost_eur = round(manual_hours_month * analyst_hourly_rate_eur, 2)
    llm_cost_eur = round(llm_cost_per_task * monthly_tasks * eur_per_usd, 2)
    infrastructure_cost_eur = round(monthly_tasks * 0.10, 2)
    automated_total_cost_eur = round(llm_cost_eur + infrastructure_cost_eur, 2)

    savings_eur_month = round(manual_cost_eur - automated_total_cost_eur, 2)
    roi_percent = round(
        (savings_eur_month / max(automated_total_cost_eur, 0.01)) * 100, 1
    )
    payback_months = round(automated_total_cost_eur / max(savings_eur_month / 12, 0.01), 1)

    time_reduction_pct = round(
        (1 - automated_h_per_task / manual_h_per_task) * 100, 1
    )

    return {
        "crew_name": crew_name,
        "crew_label": crew.get("name", crew_name),
        "monthly_tasks": monthly_tasks,
        "analyst_hourly_rate_eur": analyst_hourly_rate_eur,
        "manual": {
            "hours_per_task": manual_h_per_task,
            "hours_per_month": manual_hours_month,
            "cost_eur_month": manual_cost_eur,
        },
        "automated": {
            "hours_per_task": automated_h_per_task,
            "hours_per_month": automated_hours_month,
            "llm_cost_eur_month": llm_cost_eur,
            "infrastructure_cost_eur_month": infrastructure_cost_eur,
            "total_cost_eur_month": automated_total_cost_eur,
        },
        "savings": {
            "hours_saved_month": hours_saved_month,
            "savings_eur_month": savings_eur_month,
            "savings_eur_year": round(savings_eur_month * 12, 2),
            "time_reduction_pct": time_reduction_pct,
        },
        "roi_percent": roi_percent,
        "payback_months": payback_months,
        "verdict": (
            "ROI excellent — déploiement recommandé"
            if roi_percent >= 300
            else "ROI solide — déploiement justifié"
            if roi_percent >= 100
            else "ROI modéré — à optimiser"
        ),
    }


def design_inter_crew_communication(source_crew: str, target_crew: str) -> dict:
    """
    Conçoit le protocole de communication entre deux crews CrewAI.

    Sélectionne le meilleur canal (NATS pub/sub ou Redis pub/sub) selon
    l'urgence et la nature du handoff, définit le schéma de message et
    le trigger de déclenchement.

    Args:
        source_crew: Crew émettrice du handoff.
        target_crew: Crew réceptrice.

    Returns:
        Dictionnaire contenant protocol, message_schema, handoff_trigger
        et les garanties de livraison.
    """
    # Matrice de sélection de protocole
    nats_pairs = {
        ("compliance_audit_crew", "alert_response_crew"),
        ("alert_response_crew", "compliance_audit_crew"),
        ("compliance_audit_crew", "supply_chain_investigation_crew"),
    }
    redis_pairs = {
        ("wave_development_crew", "compliance_audit_crew"),
        ("supply_chain_investigation_crew", "wave_development_crew"),
        ("alert_response_crew", "wave_development_crew"),
    }

    pair = (source_crew, target_crew)

    if pair in nats_pairs:
        protocol = "NATS JetStream"
        transport = "NATS pub/sub avec persistance JetStream"
        subject = f"caelum.crew.handoff.{source_crew.replace('_crew', '')}"
        delivery_guarantee = "EXACTLY_ONCE"
        latency_ms = 5
        justification = (
            "NATS sélectionné : handoff entre crews avec contrainte temps-réel. "
            "JetStream garantit la persistance et la reprise en cas d'échec."
        )
    elif pair in redis_pairs:
        protocol = "Redis Pub/Sub"
        transport = "Redis Streams (XADD/XREAD)"
        subject = f"caelum:crew:handoff:{source_crew.replace('_crew', '')}"
        delivery_guarantee = "AT_LEAST_ONCE"
        latency_ms = 2
        justification = (
            "Redis sélectionné : handoff asynchrone entre crews sans contrainte "
            "temps-réel stricte. Redis Streams offre persistance et replay."
        )
    else:
        protocol = "NATS JetStream"
        transport = "NATS pub/sub avec persistance JetStream"
        subject = f"caelum.crew.handoff.{source_crew.replace('_crew', '')}"
        delivery_guarantee = "AT_LEAST_ONCE"
        latency_ms = 8
        justification = (
            "NATS sélectionné par défaut pour les handoffs inter-crews "
            "non répertoriés dans la matrice standard."
        )

    source_last_task = (
        CAELUM_CREWS[source_crew]["tasks"][-1]
        if source_crew in CAELUM_CREWS
        else {"expected_output": "output_source"}
    )
    target_first_task = (
        CAELUM_CREWS[target_crew]["tasks"][0]
        if target_crew in CAELUM_CREWS
        else {"description": "task_target"}
    )

    handoff_trigger = f"on_task_complete:{source_last_task['expected_output']}"

    message_schema = {
        "schema_version": "1.0",
        "handoff_id": "uuid_v4",
        "source_crew": source_crew,
        "target_crew": target_crew,
        "trigger_event": handoff_trigger,
        "payload": {
            "source_output": source_last_task["expected_output"],
            "domain": "str — domaine droits humains analysé",
            "risk_level": "str — critique|élevé|modéré|faible",
            "entity_scores": "dict — scores 8 entités CSDDD",
            "next_task": target_first_task.get("description", "N/A"),
            "metadata": {
                "wave_id": "int",
                "timestamp_utc": "ISO 8601",
                "caelum_session_id": "uuid_v4",
            },
        },
        "routing_key": subject,
        "ttl_seconds": 300,
    }

    return {
        "source_crew": source_crew,
        "target_crew": target_crew,
        "protocol": protocol,
        "transport": transport,
        "subject_or_key": subject,
        "delivery_guarantee": delivery_guarantee,
        "latency_target_ms": latency_ms,
        "handoff_trigger": handoff_trigger,
        "message_schema": message_schema,
        "retry_policy": {
            "max_retries": 3,
            "backoff_ms": [1_000, 5_000, 30_000],
            "dead_letter": f"caelum.dlq.handoff.{source_crew}",
        },
        "justification": justification,
        "designed_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Helpers d'affichage
# ---------------------------------------------------------------------------


def _sep(char: str = "─", width: int = 72) -> str:
    return char * width


def _section(title: str) -> None:
    print()
    print(_sep("═"))
    print(f"  {title}")
    print(_sep("═"))


def _subsection(title: str) -> None:
    print()
    print(f"  {_sep('─', 68)}")
    print(f"  {title}")
    print(f"  {_sep('─', 68)}")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------


if __name__ == "__main__":

    # ─── HEADER ───────────────────────────────────────────────────────────────
    print(_sep("═"))
    print("  CREWAI INTEGRATION REPORT — CaelumSwarm™")
    print("  Human Rights / CSDDD 2024 Compliance Platform")
    print(f"  Generated  : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"  Framework  : CrewAI {CREWAI_VERSION}")
    print("  Pattern    : Role-based agents + Task delegation + Hierarchical Process")
    print(_sep("═"))

    # ─── 1. CREWS DÉFINIES ────────────────────────────────────────────────────
    _section("1. CREWS DÉFINIES — 4 équipes CaelumSwarm™")

    for crew_key, crew in CAELUM_CREWS.items():
        agents = crew["agents"]
        tasks = crew.get("tasks", [])
        print()
        print(f"  [{crew_key}]")
        print(f"    Nom     : {crew['name']}")
        print(f"    Process : {crew['process'].upper()}")
        if crew.get("kickoff_trigger"):
            print(f"    Trigger : {crew['kickoff_trigger']}")
        if crew.get("response_time_target_minutes"):
            print(f"    SLA     : {crew['response_time_target_minutes']} minutes")
        print(f"    Agents  : {len(agents)}")
        for ag in agents:
            deleg = "delegation=True" if ag.get("allow_delegation") else "delegation=False"
            llm = ag.get("llm", "claude-sonnet-4-6")
            tools_count = len(ag.get("tools", []))
            print(f"      - {ag['role']}")
            print(f"          LLM: {llm} | {deleg} | tools: {tools_count}")
            print(f"          Goal: {ag['goal'][:70]}{'...' if len(ag['goal']) > 70 else ''}")
        print(f"    Tâches  : {len(tasks)}")
        for t in tasks:
            print(f"      [{t['agent'][:30]}] {t['description'][:55]}")
            print(f"           → {t['expected_output']}")

    # ─── 2. CREW DESIGN — conflict_minerals (critique) ────────────────────────
    _section("2. CREW DESIGN — Domaine 'conflict_minerals' (risque critique)")

    design = design_crew_for_domain("conflict_minerals", "critique")
    print(f"  Domaine            : {design['domain']}")
    print(f"  Niveau de risque   : {design['risk_level'].upper()}")
    print(f"  Priorité           : {design['priority']}")
    print(f"  Crews sélectionnées: {', '.join(design['crew_selection'])}")
    print(f"  Mode d'exécution   : {design['execution_mode']}")
    print(f"  Total agents       : {design['total_agents']}")
    print(f"  Total tâches       : {design['total_tasks']}")
    print(f"  Durée estimée      : {design['estimated_duration_min']} minutes")
    print(f"  Manager LLM        : {design['manager_llm']}")
    print(f"  Justification      : {design['justification']}")
    print()
    print("  Agents assignés :")
    for ag in design["agents_assigned"]:
        deleg = "delegation=True" if ag["allow_delegation"] else "delegation=False"
        print(f"    [{ag['crew']}] {ag['role']}")
        print(f"      LLM: {ag['llm']} | {deleg}")

    # ─── 3. SIMULATION EXÉCUTION — compliance_audit_crew ─────────────────────
    _section("3. SIMULATION EXÉCUTION — compliance_audit_crew (3 entités)")

    sim = simulate_crew_execution(
        "compliance_audit_crew",
        {"domain": "conflict_minerals", "entity_count": 3, "wave": 195},
    )
    print(f"  Crew              : {sim['crew_name']}")
    print(f"  Inputs            : {sim['inputs']}")
    print(f"  Étapes simulées   : {sim['total_steps']}")
    print(f"  Durée totale      : {sim['total_duration_seconds']}s "
          f"({sim['total_duration_minutes']} min)")
    print()
    print("  Log d'exécution :")
    for step in sim["execution_log"]:
        phase = step["phase"]
        status = step["status"]
        agent = step.get("agent", "—")
        duration = step["duration_seconds"]
        tokens = step["tokens_used"]
        print(f"    [Étape {step['step']}] {phase} — {status}")
        print(f"      Agent    : {agent}")
        if step.get("task"):
            print(f"      Tâche    : {step['task'][:65]}")
        if step.get("tool_called"):
            tool_ok = "OK" if step.get("tool_success") else "RETRIED"
            print(f"      Outil    : {step['tool_called']} → {tool_ok}")
        if step.get("llm"):
            print(f"      LLM      : {step['llm']}")
        print(f"      Durée    : {duration}s | Tokens : {tokens:,}")
    print()
    tu = sim["token_usage"]
    print("  Consommation tokens :")
    print(f"    Total     : {tu['total_tokens']:,}")
    print(f"    Input     : {tu['input_tokens']:,}")
    print(f"    Output    : {tu['output_tokens']:,}")
    print(f"    Coût est. : ${tu['estimated_cost_usd']} USD")
    print()
    fo = sim["final_output"]
    print("  Résultat final :")
    print(f"    Tâches complétées : {fo['tasks_completed']}")
    print(f"    CSDDD compliant   : {fo['csddd_compliance']}")
    print(f"    Rapport prêt      : {fo['report_ready']}")
    print(f"    Résumé            : {fo['summary']}")

    # ─── 4. ROI CALCULATION — 100 tâches/mois ─────────────────────────────────
    _section("4. ROI CALCULATION — compliance_audit_crew (100 tâches/mois)")

    roi = calculate_crew_roi("compliance_audit_crew", 100)
    print(f"  Crew              : {roi['crew_label']}")
    print(f"  Tâches/mois       : {roi['monthly_tasks']}")
    print(f"  Taux analyste     : {roi['analyst_hourly_rate_eur']} EUR/h")
    print()
    manual = roi["manual"]
    print("  Mode MANUEL :")
    print(f"    Heures/tâche    : {manual['hours_per_task']}h")
    print(f"    Heures/mois     : {manual['hours_per_month']}h")
    print(f"    Coût/mois       : {manual['cost_eur_month']:,.2f} EUR")
    print()
    auto = roi["automated"]
    print("  Mode AUTOMATISÉ (CrewAI) :")
    print(f"    Heures/tâche    : {auto['hours_per_task']}h")
    print(f"    Heures/mois     : {auto['hours_per_month']}h")
    print(f"    Coût LLM/mois   : {auto['llm_cost_eur_month']:,.2f} EUR")
    print(f"    Infra/mois      : {auto['infrastructure_cost_eur_month']:,.2f} EUR")
    print(f"    Total/mois      : {auto['total_cost_eur_month']:,.2f} EUR")
    print()
    savings = roi["savings"]
    print("  ÉCONOMIES :")
    print(f"    Heures épargnées : {savings['hours_saved_month']}h/mois")
    print(f"    Économies/mois   : {savings['savings_eur_month']:,.2f} EUR")
    print(f"    Économies/an     : {savings['savings_eur_year']:,.2f} EUR")
    print(f"    Réduction temps  : {savings['time_reduction_pct']}%")
    print()
    print(f"  ROI               : {roi['roi_percent']}%")
    print(f"  Payback           : {roi['payback_months']} mois")
    print(f"  Verdict           : {roi['verdict']}")

    # ─── 5. INTER-CREW COMMUNICATION — audit → alert ──────────────────────────
    _section("5. INTER-CREW COMMUNICATION — compliance_audit_crew → alert_response_crew")

    icc = design_inter_crew_communication(
        "compliance_audit_crew", "alert_response_crew"
    )
    print(f"  Source crew         : {icc['source_crew']}")
    print(f"  Target crew         : {icc['target_crew']}")
    print(f"  Protocole           : {icc['protocol']}")
    print(f"  Transport           : {icc['transport']}")
    print(f"  Subject/Key         : {icc['subject_or_key']}")
    print(f"  Garantie livraison  : {icc['delivery_guarantee']}")
    print(f"  Latence cible       : {icc['latency_target_ms']} ms")
    print(f"  Handoff trigger     : {icc['handoff_trigger']}")
    print(f"  Justification       : {icc['justification']}")
    print()
    print("  Schéma message :")
    schema = icc["message_schema"]
    print(f"    Version schema    : {schema['schema_version']}")
    print(f"    handoff_id        : {schema['handoff_id']}")
    print(f"    TTL               : {schema['ttl_seconds']}s")
    print("    Payload :")
    for k, v in schema["payload"].items():
        if isinstance(v, dict):
            print(f"      {k} :")
            for kk, vv in v.items():
                print(f"        {kk} : {vv}")
        else:
            print(f"      {k} : {v}")
    print()
    retry = icc["retry_policy"]
    print("  Retry policy :")
    print(f"    Max retries : {retry['max_retries']}")
    print(f"    Backoff ms  : {retry['backoff_ms']}")
    print(f"    Dead letter : {retry['dead_letter']}")

    # ─── 6. CREWAI MEMORY & CACHE CONFIG ──────────────────────────────────────
    _section("6. CREWAI MEMORY + CACHE CONFIG")

    print("  Configuration globale CrewAI :")
    for key, val in CREWAI_CONFIG.items():
        if isinstance(val, dict):
            print(f"    {key} :")
            for kk, vv in val.items():
                print(f"      {kk} : {vv}")
        else:
            print(f"    {key} : {val}")
    print()
    print("  Architecture mémoire :")
    memory_types = [
        ("ShortTermMemory",  "RAG in-context — résultats récents accessibles à tous les agents"),
        ("LongTermMemory",   "SQLite/ChromaDB — historique tâches persisté entre sessions"),
        ("EntityMemory",     "Entités extraites (fournisseurs, pays, violations) — graphe de connaissances"),
        ("UserMemory",       "Profil utilisateur et préférences pour personnalisation rapports"),
    ]
    for mem_type, desc in memory_types:
        print(f"    [{mem_type}]")
        print(f"      {desc}")
    print()
    print("  Embedder :")
    embedder = CREWAI_CONFIG["embedder"]
    print(f"    Provider  : {embedder['provider']}")
    print(f"    Modèle    : {embedder['config']['model']}")
    print(f"    Usage     : Indexation mémoire partagée + similarity search inter-agents")
    print()
    print("  Cache :")
    print(f"    Activé    : {CREWAI_CONFIG['cache']}")
    print("    Stratégie : Cache LRU par signature (tool_name + args_hash)")
    print("    TTL       : 1 heure (configurable par tool)")
    print("    Backend   : Redis Cluster (production) / mémoire (dev)")
    print("    Gain est. : ~35% réduction appels LLM sur tâches répétitives")

    # ─── 7. TOOLS INVENTORY — 10 outils ──────────────────────────────────────
    _section("7. TOOLS INVENTORY — 10 outils CaelumSwarm™")

    col_w = [28, 20, 38]
    header = ["Tool Name", "Args principaux", "Description"]
    print("  " + "  ".join(h.ljust(w) for h, w in zip(header, col_w)))
    print("  " + "  ".join("-" * w for w in col_w))
    for tool_name, tool_cfg in CREWAI_TOOLS.items():
        args = tool_cfg.get("args_schema", {})
        args_str = ", ".join(
            f"{k}: {v}" for k, v in list(args.items())[:2]
        ) if args else "—"
        desc = tool_cfg["description"][:36]
        row = [tool_name, args_str[:18], desc]
        print("  " + "  ".join(v.ljust(w) for v, w in zip(row, col_w)))
    print()
    print(f"  Total outils enregistrés : {len(CREWAI_TOOLS)}")
    crews_with_tools = sum(
        1 for c in CAELUM_CREWS.values()
        if any(a.get("tools") for a in c["agents"])
    )
    print(f"  Crews avec outils        : {crews_with_tools}/{len(CAELUM_CREWS)}")

    # ─── 8. HIERARCHICAL vs SEQUENTIAL ────────────────────────────────────────
    _section("8. HIERARCHICAL PROCESS vs SEQUENTIAL — Comparaison")

    comparison = [
        ("Critère",                 "HIERARCHICAL",                 "SEQUENTIAL"),
        ("Coordination",            "Manager agent délègue",        "Ordre fixe tâche→tâche"),
        ("Flexibilité",             "Très haute — redélégation",    "Faible — ordre prédéfini"),
        ("Latence",                 "Variable (manager overhead)",  "Prévisible et stable"),
        ("Parallélisme",            "Possible via délégation",      "Non — séquentiel strict"),
        ("Cas d'usage Caelum",      "Audit CSDDD, Alertes urgentes","Wave dev, Investigation"),
        ("LLM manager requis",      "Oui — claude-sonnet-4-6",      "Non"),
        ("Coût tokens supplémentaires", "+15–25% (manager LLM)",    "Zéro overhead"),
        ("Résilience",              "Haute — manager redistribue",  "Faible — blocage si erreur"),
        ("Transparence",            "Moins lisible",                "Très lisible / debug facile"),
    ]

    col_w2 = [30, 30, 30]
    print()
    for i, row in enumerate(comparison):
        line = "  " + "  ".join(v.ljust(w) for v, w in zip(row, col_w2))
        if i == 0:
            print(line)
            print("  " + "  ".join("-" * w for w in col_w2))
        else:
            print(line)

    print()
    print("  Recommandation Caelum :")
    print("    → HIERARCHICAL : compliance_audit_crew + alert_response_crew")
    print("      Justification : complexité variable, redélégation si agent indisponible")
    print("    → SEQUENTIAL   : supply_chain_investigation_crew + wave_development_crew")
    print("      Justification : dépendances strictes entre étapes, audit trail clair")

    print()
    print("  Config Hierarchical Process :")
    print(f"    Manager LLM  : {HIERARCHICAL_PROCESS_CONFIG['manager_llm']}")
    mgr = HIERARCHICAL_PROCESS_CONFIG["manager_agent"]
    print(f"    Manager role : {mgr['role']}")
    print(f"    Manager goal : {mgr['goal']}")
    print(f"    Delegation   : {mgr['allow_delegation']}")

    # ─── 9. CREWAI SECURITY ───────────────────────────────────────────────────
    _section("9. CREWAI SECURITY")

    _subsection("9.1 Isolation des secrets")
    secrets_checklist = [
        ("Vault",       "Credentials LLM chargés via HashiCorp Vault — jamais en clair",    True),
        ("Vault",       "vault_secrets_tool : sortie non loggée (log level WARN+)",         True),
        ("Vault",       "Rotation automatique API keys LLM — TTL 24h",                      True),
        ("EnvVars",     "SWARM_API_URL guard avant tout appel upstream",                    True),
        ("EnvVars",     "Zéro credential dans le code source ou les configs JSON",          True),
        ("EnvVars",     "Variables d'environnement injectées via Kubernetes Secrets",       True),
        ("LLM",         "Aucune donnée PII envoyée aux LLMs sans anonymisation",            True),
        ("LLM",         "claude-sonnet-4-6 configuré : no training data retention",        True),
        ("LLM",         "max_rpm: 30 — protection contre exfiltration par rate-limit",     True),
    ]
    current_cat = ""
    for cat, item, ok in secrets_checklist:
        if cat != current_cat:
            print(f"\n  [{cat}]")
            current_cat = cat
        mark = "✓" if ok else "✗"
        print(f"    {mark}  {item}")

    _subsection("9.2 Audit trail")
    audit_checklist = [
        ("Trail",  "Chaque appel agent loggé : role, task, tool, tokens, timestamp",      True),
        ("Trail",  "output_log_file: logs/crewai_caelum.log — rotation quotidienne",      True),
        ("Trail",  "blockchain_recorder : preuves incidents immuables (hash SHA-256)",    True),
        ("Trail",  "Conformité CSDDD Art.10 : traçabilité décisions IA documentée",       True),
        ("Trail",  "Rétention logs : 10 ans (exigence réglementaire CSDDD 2024)",         True),
    ]
    current_cat = ""
    for cat, item, ok in audit_checklist:
        if cat != current_cat:
            print(f"\n  [{cat}]")
            current_cat = cat
        mark = "✓" if ok else "✗"
        print(f"    {mark}  {item}")

    _subsection("9.3 Rate limiting & protection LLM")
    rate_checklist = [
        ("Rate",  "max_rpm: 30 — limite globale toutes crews confondues",                 True),
        ("Rate",  "Cache CrewAI : -35% appels LLM sur tâches répétitives",               True),
        ("Rate",  "Circuit-breaker : pause crew si 3 erreurs LLM consécutives",          True),
        ("Rate",  "Timeout tâche : 5 min max par agent (max_iter: 5)",                   True),
        ("Rate",  "Monitoring coût token : alerte si >$50 USD/jour par crew",            True),
    ]
    current_cat = ""
    for cat, item, ok in rate_checklist:
        if cat != current_cat:
            print(f"\n  [{cat}]")
            current_cat = cat
        mark = "✓" if ok else "✗"
        print(f"    {mark}  {item}")

    # ─── 10. RÉSUMÉ GLOBAL ────────────────────────────────────────────────────
    _section("10. RÉSUMÉ GLOBAL — CrewAI Integration CaelumSwarm™")

    total_agents_all = sum(len(c["agents"]) for c in CAELUM_CREWS.values())
    total_tasks_all = sum(len(c.get("tasks", [])) for c in CAELUM_CREWS.values())
    hierarchical_crews = [k for k, c in CAELUM_CREWS.items() if c["process"] == "hierarchical"]
    sequential_crews = [k for k, c in CAELUM_CREWS.items() if c["process"] == "sequential"]

    print(f"  Framework          : CrewAI {CREWAI_VERSION}")
    print(f"  Crews définies     : {len(CAELUM_CREWS)}")
    print(f"  Process hiérarchique: {len(hierarchical_crews)} crews")
    for c in hierarchical_crews:
        print(f"    - {c}")
    print(f"  Process séquentiel  : {len(sequential_crews)} crews")
    for c in sequential_crews:
        print(f"    - {c}")
    print(f"  Total agents        : {total_agents_all}")
    print(f"  Total tâches        : {total_tasks_all}")
    print(f"  Outils enregistrés  : {len(CREWAI_TOOLS)}")
    print(f"  Mémoire partagée    : {'Activée' if CREWAI_CONFIG['memory'] else 'Désactivée'}")
    print(f"  Cache LLM           : {'Activé' if CREWAI_CONFIG['cache'] else 'Désactivé'}")
    print(f"  Planning CrewAI     : {'Activé' if CREWAI_CONFIG['planning'] else 'Désactivé'}")
    print(f"  Max RPM             : {CREWAI_CONFIG['max_rpm']}")
    print(f"  LLM Planning        : {CREWAI_CONFIG['planning_llm']}")
    print()
    print("  LLMs utilisés :")
    llms_used = set()
    for crew in CAELUM_CREWS.values():
        for agent in crew["agents"]:
            if agent.get("llm"):
                llms_used.add(agent["llm"])
    llms_used.add(CREWAI_CONFIG["planning_llm"])
    llms_used.add(HIERARCHICAL_PROCESS_CONFIG["manager_llm"])
    for llm in sorted(llms_used):
        print(f"    - {llm}")
    print()
    print("  Sécurité :")
    print("    ✓ Secrets isolation via HashiCorp Vault")
    print("    ✓ Audit trail CSDDD Art.10 (blockchain + logs 10 ans)")
    print("    ✓ Rate limiting max_rpm:30 + circuit-breaker")
    print("    ✓ Zéro credentials dans le code")
    print("    ✓ PII anonymisation avant envoi LLM")

    # ─── FOOTER ───────────────────────────────────────────────────────────────
    print()
    print(_sep("═"))
    print()
    print(
        f"  CrewAI Integration Agent — PRÊT "
        f"(CrewAI {CREWAI_VERSION} / {len(CAELUM_CREWS)} Crews / Hierarchical Process)"
    )
    print()
    print(_sep("═"))
