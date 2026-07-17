#!/usr/bin/env python3
"""
Agent Gestionnaire de Jetons & Résilience Opérationnelle — gère les crédits API,
tokens LLM, quotas services, et assure la résilience opérationnelle de CaelumSwarm™
face aux pannes et limites de ressources.
"""

import sys
from datetime import datetime, timezone
from typing import Optional

# ---------------------------------------------------------------------------
# DATA CONSTANTS
# ---------------------------------------------------------------------------

API_SERVICES = {
    "ANTHROPIC_CLAUDE": {
        "label": "Anthropic Claude (claude-3-5-sonnet / claude-3-opus)",
        "token_type": "TOKENS",
        "cost_per_1k_tokens_EUR": 0.0028,       # ~3 EUR/M tokens (blended input/output)
        "monthly_limit": 50_000_000,             # 50M tokens/mois
        "current_usage_pct": 62.4,
        "rate_limit_rpm": 4000,
        "failover_priority": 1,
    },
    "OPENAI_GPT4": {
        "label": "OpenAI GPT-4o",
        "token_type": "TOKENS",
        "cost_per_1k_tokens_EUR": 0.0046,        # ~5 EUR/M tokens blended
        "monthly_limit": 20_000_000,
        "current_usage_pct": 41.7,
        "rate_limit_rpm": 10000,
        "failover_priority": 2,
    },
    "GOOGLE_GEMINI": {
        "label": "Google Gemini 1.5 Pro",
        "token_type": "TOKENS",
        "cost_per_1k_tokens_EUR": 0.0062,        # ~6.50 EUR/M tokens blended
        "monthly_limit": 15_000_000,
        "current_usage_pct": 18.3,
        "rate_limit_rpm": 360,
        "failover_priority": 3,
    },
    "PERPLEXITY_SONAR": {
        "label": "Perplexity Sonar Pro (recherche temps réel)",
        "token_type": "REQUESTS",
        "cost_per_1k_tokens_EUR": 0.008,         # 8 EUR/1000 requêtes
        "monthly_limit": 100_000,                # 100K requêtes/mois
        "current_usage_pct": 29.5,
        "rate_limit_rpm": 50,
        "failover_priority": 4,
    },
    "COHERE_COMMAND": {
        "label": "Cohere Command R+",
        "token_type": "TOKENS",
        "cost_per_1k_tokens_EUR": 0.0014,        # ~1.50 EUR/M tokens — moins cher
        "monthly_limit": 30_000_000,
        "current_usage_pct": 11.2,
        "rate_limit_rpm": 10000,
        "failover_priority": 5,
    },
    "HUGGINGFACE_INFERENCE": {
        "label": "HuggingFace Inference API (Mixtral / Llama3)",
        "token_type": "CREDITS",
        "cost_per_1k_tokens_EUR": 0.0006,        # ~0.60 EUR/M tokens — économique
        "monthly_limit": 200_000_000,
        "current_usage_pct": 5.8,
        "rate_limit_rpm": 300,
        "failover_priority": 6,
    },
}

RESILIENCE_PATTERNS = {
    "CIRCUIT_BREAKER": {
        "label": "Disjoncteur de Circuit",
        "description": (
            "Interrompt automatiquement les appels vers un service défaillant après N "
            "échecs consécutifs et entre en mode 'ouvert' pendant une période de repos. "
            "Empêche la cascade de pannes et libère rapidement les ressources."
        ),
        "when_to_use": (
            "Taux d'erreur >10% sur 60s, latence >5x la normale, service en dégradation "
            "progressive. Idéal pour les appels LLM externes à haute fréquence."
        ),
        "implementation_overhead": "LOW",
        "effectiveness_score": 9,
    },
    "RETRY_WITH_BACKOFF": {
        "label": "Réessai avec Backoff Exponentiel",
        "description": (
            "Réessaie les requêtes échouées avec un délai croissant (1s, 2s, 4s, 8s…) "
            "et jitter aléatoire pour éviter les tempêtes de retry synchronisées. "
            "Inclut un nombre maximum de tentatives et un délai plafond."
        ),
        "when_to_use": (
            "Erreurs transitoires (429 Rate Limit, 503 Service Unavailable, timeouts réseau). "
            "Efficace pour les pics de charge temporaires des API LLM."
        ),
        "implementation_overhead": "LOW",
        "effectiveness_score": 7,
    },
    "FALLBACK_CHAIN": {
        "label": "Chaîne de Repli Ordonnée",
        "description": (
            "Définit une séquence ordonnée de services alternatifs. En cas d'échec du "
            "service primaire, bascule automatiquement vers le suivant selon la priorité "
            "de failover. Dernier recours : mode dégradé avec réponse en cache."
        ),
        "when_to_use": (
            "Pannes de service, dépassement de quota, maintenance planifiée. "
            "Garantit la continuité de service pour les opérations critiques de CaelumSwarm™."
        ),
        "implementation_overhead": "MEDIUM",
        "effectiveness_score": 10,
    },
    "BULKHEAD": {
        "label": "Cloison d'Isolation (Bulkhead)",
        "description": (
            "Isole les ressources (pool de connexions, threads, quotas tokens) par type "
            "d'opération. Empêche une opération gourmande d'épuiser les ressources "
            "nécessaires aux opérations critiques."
        ),
        "when_to_use": (
            "Coexistence d'opérations critiques (alertes, rapports urgents) et de batch "
            "lourds (analyses wave complètes). Protège les SLA des opérations P1/P2."
        ),
        "implementation_overhead": "HIGH",
        "effectiveness_score": 8,
    },
    "TIMEOUT_HEDGE": {
        "label": "Délai Limite + Requêtes Anticipées (Hedge)",
        "description": (
            "Impose un timeout strict sur chaque appel API LLM. Si la réponse tarde "
            "au-delà d'un seuil (p.ex. 80% du timeout), envoie une requête identique "
            "en parallèle vers un service secondaire et utilise la première réponse reçue."
        ),
        "when_to_use": (
            "Latence imprévisible des LLM sous charge (queuing GPU). Réduit le p99 de "
            "latence perçue pour les opérations temps réel (alertes, dashboards live)."
        ),
        "implementation_overhead": "MEDIUM",
        "effectiveness_score": 8,
    },
}

TOKEN_BUDGETS = {
    "WAVE_ENGINE_ANALYSIS": {
        "label": "Analyse Engine Wave (8 entités × sous-scores)",
        "tokens_per_operation": 12_000,
        "priority": "CRITICAL",
        "max_daily_runs": 50,
        "cost_EUR_per_run": 0.034,
    },
    "PRESS_RELEASE_GEN": {
        "label": "Génération Communiqué de Presse",
        "tokens_per_operation": 8_000,
        "priority": "HIGH",
        "max_daily_runs": 20,
        "cost_EUR_per_run": 0.022,
    },
    "LEGAL_WATCH_SCAN": {
        "label": "Veille Juridique & Réglementaire",
        "tokens_per_operation": 15_000,
        "priority": "HIGH",
        "max_daily_runs": 30,
        "cost_EUR_per_run": 0.042,
    },
    "ALERT_PROCESSING": {
        "label": "Traitement & Qualification d'Alertes",
        "tokens_per_operation": 3_000,
        "priority": "CRITICAL",
        "max_daily_runs": 500,
        "cost_EUR_per_run": 0.008,
    },
    "REPORT_GENERATION": {
        "label": "Génération Rapport Conformité/Risque",
        "tokens_per_operation": 25_000,
        "priority": "MEDIUM",
        "max_daily_runs": 10,
        "cost_EUR_per_run": 0.070,
    },
    "STAKEHOLDER_BRIEF": {
        "label": "Note de Synthèse Parties Prenantes",
        "tokens_per_operation": 6_000,
        "priority": "LOW",
        "max_daily_runs": 15,
        "cost_EUR_per_run": 0.017,
    },
}

INCIDENT_TYPES = {
    "API_RATE_LIMIT": {
        "label": "Dépassement Limite de Débit API",
        "severity": "P3",
        "auto_mitigation": True,
        "escalation_time_minutes": 30,
        "runbook_steps": [
            "Détecter le code HTTP 429 / header Retry-After",
            "Activer RETRY_WITH_BACKOFF avec jitter 1–8 s",
            "Si persistant >5 min → activer FALLBACK_CHAIN vers service suivant",
            "Réduire la concurrence (bulkhead) de 50% sur le service impacté",
            "Notifier l'équipe technique via Slack #infra-alerts",
            "Documenter dans le registre d'incidents pour analyse tendances",
        ],
    },
    "SERVICE_OUTAGE": {
        "label": "Panne Service LLM",
        "severity": "P1",
        "auto_mitigation": True,
        "escalation_time_minutes": 5,
        "runbook_steps": [
            "Détecter échecs HTTP 5xx ou timeout total (>30 s)",
            "Ouvrir immédiatement le CIRCUIT_BREAKER (état : ouvert)",
            "Basculer intégralement sur le service failover selon failover_priority",
            "Alerter DG + CTO dans les 5 minutes",
            "Vérifier status.anthropic.com / status.openai.com",
            "Préparer réponse client si SLA menacé (uptime <99.5%)",
            "Documenter RCA (Root Cause Analysis) sous 24h",
        ],
    },
    "TOKEN_BUDGET_EXCEEDED": {
        "label": "Dépassement Budget Token Mensuel",
        "severity": "P2",
        "auto_mitigation": True,
        "escalation_time_minutes": 15,
        "runbook_steps": [
            "Détecter consommation >90% du budget mensuel alloué",
            "Activer le mode THROTTLING : suspendre opérations LOW priority",
            "Rediriger vers services moins coûteux (HuggingFace, Cohere)",
            "Recalculer projections de fin de mois via monitor_token_consumption()",
            "Alerter Finance + DG pour arbitrage budgétaire d'urgence",
            "Si >100% : suspendre toutes opérations non-CRITICAL",
        ],
    },
    "LATENCY_SPIKE": {
        "label": "Pic de Latence LLM",
        "severity": "P3",
        "auto_mitigation": True,
        "escalation_time_minutes": 20,
        "runbook_steps": [
            "Détecter p95 latence >3× la baseline (baseline: 2 s)",
            "Activer TIMEOUT_HEDGE : requêtes en parallèle dès 80% du timeout",
            "Réduire la taille des prompts de 20% (optimisation tokens contexte)",
            "Basculer les opérations non-critiques vers les heures creuses",
            "Surveiller pendant 15 min avant escalade",
            "Logger les métriques pour audit de performance mensuel",
        ],
    },
    "DATA_QUALITY_FAILURE": {
        "label": "Échec Qualité Données / Hallucinations",
        "severity": "P2",
        "auto_mitigation": False,
        "escalation_time_minutes": 10,
        "runbook_steps": [
            "Détecter via validation schema JSON des réponses LLM",
            "Rejeter la réponse et relancer avec temperature=0 et prompt enrichi",
            "Si 2e échec : escalader à un modèle supérieur (GPT-4o → Claude-3-Opus)",
            "Alerter l'équipe Data Science pour revue manuelle",
            "Mettre en quarantaine les données jusqu'à validation humaine",
            "Déclencher audit de prompt engineering sur le domaine concerné",
        ],
    },
    "SECURITY_BREACH": {
        "label": "Violation de Sécurité / Fuite de Clé API",
        "severity": "P1",
        "auto_mitigation": False,
        "escalation_time_minutes": 0,
        "runbook_steps": [
            "IMMÉDIAT : Révoquer toutes les clés API compromises via les dashboards",
            "Isoler les services impactés (couper le trafic entrant/sortant)",
            "Notifier CISO + DG + Conseil d'administration sans délai",
            "Auditer les logs d'accès des 72 dernières heures",
            "Générer de nouvelles clés API et rotation complète des secrets",
            "Déclaration RGPD à la CNIL si données personnelles exposées (<72h)",
            "Rapport d'incident complet avec timeline et mesures correctives",
        ],
    },
}

# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------

DAYS_IN_MONTH = 30


def monitor_token_consumption(services: dict, period_days: int = 30) -> dict:
    """
    Analyse la consommation de tokens sur l'ensemble des services API.

    Retourne : daily_burn_rate, projected_month_end_usage, budget_risk,
               cost_breakdown_EUR, optimization_potential_EUR.
    """
    cost_breakdown = {}
    total_cost_EUR = 0.0
    total_tokens_used = 0
    total_tokens_limit = 0

    for svc_key, svc in services.items():
        tokens_limit = svc["monthly_limit"]
        usage_pct = svc["current_usage_pct"] / 100.0
        tokens_used = int(tokens_limit * usage_pct)

        # Coût déjà consommé
        cost_consumed = (tokens_used / 1000) * svc["cost_per_1k_tokens_EUR"]

        # Taux journalier (consommation actuelle sur period_days)
        daily_tokens = tokens_used / period_days if period_days > 0 else 0
        daily_cost = (daily_tokens / 1000) * svc["cost_per_1k_tokens_EUR"]

        # Projection fin de mois (DAYS_IN_MONTH jours total)
        projected_tokens = int(daily_tokens * DAYS_IN_MONTH)
        projected_pct = (projected_tokens / tokens_limit * 100) if tokens_limit > 0 else 0.0

        cost_breakdown[svc_key] = {
            "label": svc["label"],
            "token_type": svc["token_type"],
            "tokens_used": tokens_used,
            "monthly_limit": tokens_limit,
            "current_usage_pct": svc["current_usage_pct"],
            "projected_month_end_pct": round(projected_pct, 1),
            "daily_burn_rate": round(daily_tokens, 0),
            "cost_consumed_EUR": round(cost_consumed, 2),
            "daily_cost_EUR": round(daily_cost, 2),
            "projected_monthly_cost_EUR": round(daily_cost * DAYS_IN_MONTH, 2),
            "risk_flag": (
                "CRITICAL" if projected_pct > 95
                else "WARNING" if projected_pct > 80
                else "OK"
            ),
        }

        total_cost_EUR += cost_consumed
        total_tokens_used += tokens_used
        total_tokens_limit += tokens_limit

    # Taux journalier global
    global_daily_tokens = total_tokens_used / period_days if period_days > 0 else 0
    global_daily_cost = sum(
        cb["daily_cost_EUR"] for cb in cost_breakdown.values()
    )
    global_projected_cost = global_daily_cost * DAYS_IN_MONTH

    # Budget risk global
    critical_count = sum(1 for cb in cost_breakdown.values() if cb["risk_flag"] == "CRITICAL")
    warning_count = sum(1 for cb in cost_breakdown.values() if cb["risk_flag"] == "WARNING")
    if critical_count > 0:
        budget_risk = "CRITICAL"
    elif warning_count > 0:
        budget_risk = "WARNING"
    else:
        budget_risk = "OK"

    # Potentiel d'optimisation : basculer la consommation ANTHROPIC/OPENAI vers COHERE/HUGGINGFACE
    # pour les opérations MEDIUM/LOW priority (hypothèse : 30% des tokens sont optimisables)
    top_services_cost = sum(
        cb["projected_monthly_cost_EUR"]
        for key, cb in cost_breakdown.items()
        if key in ("ANTHROPIC_CLAUDE", "OPENAI_GPT4")
    )
    optimization_potential_EUR = round(top_services_cost * 0.30, 2)

    return {
        "analysis_date": datetime.now(timezone.utc).isoformat(),
        "period_days": period_days,
        "services_monitored": len(services),
        "total_tokens_consumed": total_tokens_used,
        "global_daily_burn_rate": round(global_daily_tokens, 0),
        "projected_month_end_usage_pct": round(
            total_tokens_used / total_tokens_limit * 100 * (DAYS_IN_MONTH / period_days), 1
        ) if total_tokens_limit > 0 else 0.0,
        "budget_risk": budget_risk,
        "cost_breakdown_EUR": cost_breakdown,
        "total_cost_consumed_EUR": round(total_cost_EUR, 2),
        "global_daily_cost_EUR": round(global_daily_cost, 2),
        "projected_monthly_cost_EUR": round(global_projected_cost, 2),
        "optimization_potential_EUR": optimization_potential_EUR,
        "optimization_strategy": (
            "Migrer 30% des opérations MEDIUM/LOW vers Cohere Command R+ "
            "ou HuggingFace Inference pour réduire les coûts sans impact SLA."
        ),
        "critical_services": [
            key for key, cb in cost_breakdown.items() if cb["risk_flag"] == "CRITICAL"
        ],
        "warning_services": [
            key for key, cb in cost_breakdown.items() if cb["risk_flag"] == "WARNING"
        ],
    }


def design_failover_chain(primary_service: str, operation_type: str) -> dict:
    """
    Construit une chaîne de repli ordonnée lorsque le service primaire est défaillant.

    Retourne : chain (service → service → cache → degraded_mode),
               estimated_latency_ms par saut, quality_degradation_pct.
    """
    if primary_service not in API_SERVICES:
        return {"error": f"Service inconnu : {primary_service}"}

    # Construire la liste ordonnée des fallbacks (par failover_priority, excluant le primaire)
    ordered_services = sorted(
        [(key, svc) for key, svc in API_SERVICES.items() if key != primary_service],
        key=lambda x: x[1]["failover_priority"],
    )

    # Niveaux de latence de base par service (ms, p50)
    base_latency_ms = {
        "ANTHROPIC_CLAUDE": 1800,
        "OPENAI_GPT4": 1500,
        "GOOGLE_GEMINI": 2200,
        "PERPLEXITY_SONAR": 3000,
        "COHERE_COMMAND": 1200,
        "HUGGINGFACE_INFERENCE": 4500,
    }

    # Dégradation qualité relative au service primaire (en %)
    quality_map = {
        "ANTHROPIC_CLAUDE": 0,
        "OPENAI_GPT4": 5,
        "GOOGLE_GEMINI": 10,
        "PERPLEXITY_SONAR": 20,
        "COHERE_COMMAND": 25,
        "HUGGINGFACE_INFERENCE": 35,
    }
    primary_quality = quality_map.get(primary_service, 0)

    chain = []

    # Hop 1 : service primaire (défaillant — détection)
    chain.append({
        "hop": 1,
        "type": "PRIMARY",
        "service": primary_service,
        "label": API_SERVICES[primary_service]["label"],
        "status": "FAILED",
        "action": "Déclenchement détection échec → ouverture circuit breaker",
        "estimated_latency_ms": 30_000,   # timeout d'attente avant déclaration d'échec
        "quality_degradation_pct": 0,
        "cost_multiplier": 1.0,
    })

    # Hop 2 : premier service de repli disponible (usage < 90%)
    added = 0
    for key, svc in ordered_services:
        if added >= 2:
            break
        usage_ok = svc["current_usage_pct"] < 90.0
        degradation = max(0, quality_map.get(key, 50) - primary_quality)
        chain.append({
            "hop": 2 + added,
            "type": "FAILOVER",
            "service": key,
            "label": svc["label"],
            "status": "AVAILABLE" if usage_ok else "QUOTA_RISK",
            "action": f"Routage automatique vers {svc['label']}",
            "estimated_latency_ms": base_latency_ms.get(key, 3000),
            "quality_degradation_pct": degradation,
            "cost_multiplier": round(
                svc["cost_per_1k_tokens_EUR"] / API_SERVICES[primary_service]["cost_per_1k_tokens_EUR"], 2
            ),
        })
        added += 1

    # Hop N-1 : réponse depuis le cache (TTL 30 min)
    chain.append({
        "hop": len(chain) + 1,
        "type": "CACHE",
        "service": "INTERNAL_CACHE",
        "label": "Cache Redis interne CaelumSwarm™ (TTL 30 min)",
        "status": "AVAILABLE",
        "action": "Retourner la dernière réponse valide en cache si fraîcheur suffisante",
        "estimated_latency_ms": 25,
        "quality_degradation_pct": 40,
        "cost_multiplier": 0.0,
    })

    # Hop N : mode dégradé
    chain.append({
        "hop": len(chain) + 1,
        "type": "DEGRADED_MODE",
        "service": "STATIC_FALLBACK",
        "label": "Mode dégradé — Réponse statique précompilée",
        "status": "ALWAYS_AVAILABLE",
        "action": (
            "Retourner le dernier rapport Wave complet connu + message dégradation "
            "à l'utilisateur. Enregistrer l'incident pour retraitement post-panne."
        ),
        "estimated_latency_ms": 5,
        "quality_degradation_pct": 80,
        "cost_multiplier": 0.0,
    })

    # SLA de la chaîne : p99 latence = fallback 1 + switch time
    expected_recovery_ms = (
        chain[0]["estimated_latency_ms"]   # temps détection
        + chain[1]["estimated_latency_ms"] if len(chain) > 1 else 0  # premier fallback
    )

    return {
        "design_date": datetime.now(timezone.utc).isoformat(),
        "primary_service": primary_service,
        "operation_type": operation_type,
        "chain_length": len(chain),
        "chain": chain,
        "expected_recovery_latency_ms": expected_recovery_ms,
        "recommended_circuit_breaker_threshold": 5,       # échecs avant ouverture
        "recommended_circuit_breaker_timeout_s": 60,      # durée état ouvert
        "recommended_retry_attempts": 3,
        "recommended_retry_backoff_base_s": 2,
        "sla_notes": (
            f"Basculement automatique vers fallback 1 en <{expected_recovery_ms // 1000}s. "
            f"Mode cache disponible en <100ms. Mode dégradé toujours disponible."
        ),
    }


def allocate_token_budget(total_monthly_budget_EUR: float, operations: dict) -> dict:
    """
    Répartit le budget token mensuel entre les opérations selon leur priorité.

    Retourne : allocation_per_operation, protected_operations,
               throttling_candidates, projected_operations_per_month.
    """
    PRIORITY_WEIGHTS = {
        "CRITICAL": 0.40,
        "HIGH": 0.30,
        "MEDIUM": 0.20,
        "LOW": 0.10,
    }

    # Regrouper les opérations par priorité
    by_priority: dict = {p: [] for p in PRIORITY_WEIGHTS}
    for op_key, op in operations.items():
        prio = op.get("priority", "LOW")
        if prio in by_priority:
            by_priority[prio].append((op_key, op))

    # Budget alloué par priorité
    budget_per_priority = {
        prio: total_monthly_budget_EUR * weight
        for prio, weight in PRIORITY_WEIGHTS.items()
    }

    allocation_per_operation = {}
    protected_operations = []
    throttling_candidates = []
    projected_ops_per_month = {}

    for prio, ops_list in by_priority.items():
        if not ops_list:
            continue
        prio_budget = budget_per_priority[prio]
        # Répartition équitable au sein de chaque niveau de priorité
        share_per_op = prio_budget / len(ops_list) if ops_list else 0

        for op_key, op in ops_list:
            cost_per_run = op["cost_EUR_per_run"]
            max_daily = op["max_daily_runs"]
            max_monthly = max_daily * DAYS_IN_MONTH

            # Nombre de runs possibles avec le budget alloué
            runs_possible = int(share_per_op / cost_per_run) if cost_per_run > 0 else 0
            runs_possible = min(runs_possible, max_monthly)

            # Coût réel alloué (peut être inférieur au share si max_monthly est le plafond)
            budget_allocated = round(runs_possible * cost_per_run, 2)

            # Identifier les opérations protégées vs à réduire
            utilization_pct = (runs_possible / max_monthly * 100) if max_monthly > 0 else 0.0

            if prio in ("CRITICAL", "HIGH"):
                protected_operations.append(op_key)
            else:
                throttling_candidates.append(op_key)

            allocation_per_operation[op_key] = {
                "label": op["label"],
                "priority": prio,
                "budget_allocated_EUR": budget_allocated,
                "budget_share_EUR": round(share_per_op, 2),
                "tokens_per_operation": op["tokens_per_operation"],
                "cost_EUR_per_run": cost_per_run,
                "projected_runs_per_month": runs_possible,
                "max_daily_runs": max_daily,
                "max_monthly_runs": max_monthly,
                "utilization_pct": round(utilization_pct, 1),
                "status": (
                    "FULLY_FUNDED" if utilization_pct >= 90
                    else "PARTIALLY_FUNDED" if utilization_pct >= 50
                    else "THROTTLED"
                ),
            }
            projected_ops_per_month[op_key] = runs_possible

    # Vérification du total alloué vs budget
    total_allocated = sum(a["budget_allocated_EUR"] for a in allocation_per_operation.values())
    remaining_EUR = round(total_monthly_budget_EUR - total_allocated, 2)

    return {
        "allocation_date": datetime.now(timezone.utc).isoformat(),
        "total_monthly_budget_EUR": total_monthly_budget_EUR,
        "total_allocated_EUR": round(total_allocated, 2),
        "remaining_buffer_EUR": remaining_EUR,
        "budget_utilization_pct": round(total_allocated / total_monthly_budget_EUR * 100, 1),
        "priority_budget_breakdown": {
            prio: round(budget_per_priority[prio], 2)
            for prio in PRIORITY_WEIGHTS
        },
        "allocation_per_operation": allocation_per_operation,
        "protected_operations": protected_operations,
        "throttling_candidates": throttling_candidates,
        "projected_operations_per_month": projected_ops_per_month,
        "recommendations": [
            "Les opérations CRITICAL (Wave engines, alertes) sont protégées à 100% du budget alloué.",
            f"Budget tampon de {remaining_EUR} EUR disponible pour pics d'activité imprévus.",
            "Surveiller le ratio coût/valeur des opérations LOW priority chaque semaine.",
            "Activer le basculement vers Cohere/HuggingFace pour REPORT_GENERATION si budget tendu.",
        ],
    }


def generate_resilience_report(
    incident_history: list,
    current_uptime_pct: float,
) -> dict:
    """
    Calcule les métriques de résilience opérationnelle de CaelumSwarm™.

    Retourne : MTTR, MTBF, SLA_compliance, single_points_of_failure,
               recommended_patterns, estimated_cost_of_downtime_EUR_hour.
    """
    SLA_TARGET_PCT = 99.5
    SWARM_REVENUE_EUR_MONTH = 85_000  # Revenu mensuel CaelumSwarm™ (hypothèse SaaS)
    HOURS_PER_MONTH = 730

    # Calculer MTTR (Mean Time To Recover) en minutes
    resolved_incidents = [
        inc for inc in incident_history if inc.get("resolved") and inc.get("duration_minutes", 0) > 0
    ]
    if resolved_incidents:
        mttr_minutes = sum(inc["duration_minutes"] for inc in resolved_incidents) / len(resolved_incidents)
    else:
        mttr_minutes = 0.0

    # Calculer MTBF (Mean Time Between Failures) en heures
    if len(incident_history) > 1:
        # Utiliser la durée couverte par l'historique
        total_period_hours = 720  # 30 jours en heures (supposé)
        mtbf_hours = total_period_hours / len(incident_history)
    elif len(incident_history) == 1:
        mtbf_hours = 720.0
    else:
        mtbf_hours = float("inf")

    # SLA compliance
    sla_compliant = current_uptime_pct >= SLA_TARGET_PCT
    sla_gap_pct = round(current_uptime_pct - SLA_TARGET_PCT, 3)
    allowed_downtime_minutes_month = (1 - SLA_TARGET_PCT / 100) * HOURS_PER_MONTH * 60
    actual_downtime_minutes = (1 - current_uptime_pct / 100) * HOURS_PER_MONTH * 60

    # Coût de l'indisponibilité
    hourly_revenue_EUR = SWARM_REVENUE_EUR_MONTH / HOURS_PER_MONTH
    # Inclure aussi le coût réputationnel (multiplié par 2.5×)
    cost_of_downtime_EUR_hour = round(hourly_revenue_EUR * 2.5, 2)

    # Single Points of Failure
    single_points_of_failure = []

    # Services LLM sans failover configuré (usage > 80%)
    for svc_key, svc in API_SERVICES.items():
        if svc["current_usage_pct"] > 80 and svc["failover_priority"] == 1:
            single_points_of_failure.append({
                "component": svc_key,
                "label": svc["label"],
                "risk": f"Usage à {svc['current_usage_pct']}% — proche de la limite, failover insuffisant",
                "mitigation": "Activer FALLBACK_CHAIN + réduire la consommation de 15%",
            })

    # Patterns recommandés basés sur les types d'incidents
    incident_type_counts: dict = {}
    for inc in incident_history:
        t = inc.get("type", "UNKNOWN")
        incident_type_counts[t] = incident_type_counts.get(t, 0) + 1

    recommended_patterns = []
    pattern_reasons = {
        "API_RATE_LIMIT": ("RETRY_WITH_BACKOFF", "Réessais exponentiels sur erreurs 429"),
        "SERVICE_OUTAGE": ("CIRCUIT_BREAKER", "Isolation rapide du service défaillant"),
        "TOKEN_BUDGET_EXCEEDED": ("BULKHEAD", "Isolation des budgets par priorité d'opération"),
        "LATENCY_SPIKE": ("TIMEOUT_HEDGE", "Requêtes parallèles pour réduire le p99 latence"),
        "DATA_QUALITY_FAILURE": ("FALLBACK_CHAIN", "Escalade vers modèle supérieur en cas d'hallucination"),
    }

    seen_patterns = set()
    for inc_type, count in sorted(incident_type_counts.items(), key=lambda x: -x[1]):
        if inc_type in pattern_reasons:
            pattern_key, reason = pattern_reasons[inc_type]
            if pattern_key not in seen_patterns:
                pattern_cfg = RESILIENCE_PATTERNS.get(pattern_key, {})
                recommended_patterns.append({
                    "pattern": pattern_key,
                    "label": pattern_cfg.get("label", pattern_key),
                    "reason": reason,
                    "triggered_by_incident_type": inc_type,
                    "occurrence_count": count,
                    "effectiveness_score": pattern_cfg.get("effectiveness_score", 0),
                    "implementation_overhead": pattern_cfg.get("implementation_overhead", "UNKNOWN"),
                })
                seen_patterns.add(pattern_key)

    # Trier par effectiveness_score décroissant
    recommended_patterns.sort(key=lambda x: -x["effectiveness_score"])

    # Distribution des sévérités
    severity_counts: dict = {}
    for inc in incident_history:
        sev = inc.get("severity", "P4")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    return {
        "report_date": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Token Manager & Resilience Agent v1.0",
        "period_analyzed": "30 derniers jours",
        "metrics": {
            "mttr_minutes": round(mttr_minutes, 1),
            "mtbf_hours": round(mtbf_hours, 1),
            "current_uptime_pct": current_uptime_pct,
            "sla_target_pct": SLA_TARGET_PCT,
            "sla_compliant": sla_compliant,
            "sla_gap_pct": sla_gap_pct,
            "allowed_downtime_minutes_month": round(allowed_downtime_minutes_month, 1),
            "actual_downtime_minutes": round(actual_downtime_minutes, 1),
        },
        "incident_summary": {
            "total_incidents": len(incident_history),
            "resolved": len(resolved_incidents),
            "unresolved": len(incident_history) - len(resolved_incidents),
            "by_severity": severity_counts,
            "by_type": incident_type_counts,
        },
        "sla_compliance": {
            "status": "CONFORME" if sla_compliant else "NON-CONFORME",
            "target": f"{SLA_TARGET_PCT}% uptime mensuel",
            "actual": f"{current_uptime_pct}% uptime",
            "assessment": (
                f"SLA respecté avec une marge de {sla_gap_pct:+.3f}%."
                if sla_compliant
                else f"SLA VIOLÉ : déficit de {abs(sla_gap_pct):.3f}% ({round(actual_downtime_minutes - allowed_downtime_minutes_month, 1)} min au-delà du seuil)."
            ),
        },
        "single_points_of_failure": single_points_of_failure,
        "recommended_patterns": recommended_patterns,
        "financial_impact": {
            "estimated_cost_of_downtime_EUR_hour": cost_of_downtime_EUR_hour,
            "cost_basis": f"Revenu mensuel {SWARM_REVENUE_EUR_MONTH} EUR × 2.5× (impact réputationnel)",
            "downtime_cost_current_period_EUR": round(
                (actual_downtime_minutes / 60) * cost_of_downtime_EUR_hour, 2
            ),
        },
        "action_plan": [
            "Implémenter CIRCUIT_BREAKER sur tous les services LLM (priorité haute).",
            "Configurer alertes PagerDuty pour uptime <99.7% (buffer avant violation SLA).",
            f"Réduire MTTR cible à <{max(5, int(mttr_minutes * 0.7))} min via runbooks automatisés.",
            "Revoir mensuellement la chaîne de failover et tester les basculements.",
        ],
    }


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """Démonstration complète du Token Manager & Resilience Agent."""
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — TOKEN MANAGER & RESILIENCE AGENT")
    print("  Gestionnaire de Jetons & Résilience Opérationnelle")
    print("=" * 70)

    # ------------------------------------------------------------------
    # 1. Surveillance de la consommation de tokens
    # ------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("  [1/4] SURVEILLANCE CONSOMMATION TOKENS")
    print("-" * 60)

    consumption = monitor_token_consumption(API_SERVICES, period_days=21)

    print(f"\n  Période analysée          : {consumption['period_days']} jours")
    print(f"  Services surveillés       : {consumption['services_monitored']}")
    print(f"  Tokens consommés (total)  : {consumption['total_tokens_consumed']:,}")
    print(f"  Taux journalier global    : {int(consumption['global_daily_burn_rate']):,} tokens/jour")
    print(f"  Projection fin de mois    : {consumption['projected_month_end_usage_pct']}%")
    print(f"  Budget risk               : {consumption['budget_risk']}")
    print(f"  Coût consommé à ce jour   : {consumption['total_cost_consumed_EUR']} EUR")
    print(f"  Projection coût mensuel   : {consumption['projected_monthly_cost_EUR']} EUR")
    print(f"  Potentiel d'optimisation  : {consumption['optimization_potential_EUR']} EUR/mois")

    print(f"\n  Détail par service :")
    for key, cb in consumption["cost_breakdown_EUR"].items():
        flag = {"CRITICAL": "[!CRITICAL]", "WARNING": "[WARNING] ", "OK": "[OK]      "}.get(cb["risk_flag"], "")
        print(f"    {flag} {key:25} {cb['current_usage_pct']:5.1f}%  "
              f"proj {cb['projected_month_end_pct']:5.1f}%  "
              f"coût {cb['projected_monthly_cost_EUR']:6.2f} EUR/mois")

    if consumption["critical_services"]:
        print(f"\n  SERVICES CRITIQUES : {', '.join(consumption['critical_services'])}")
    if consumption["warning_services"]:
        print(f"  SERVICES EN ALERTE : {', '.join(consumption['warning_services'])}")

    # ------------------------------------------------------------------
    # 2. Chaîne de failover pour Wave Engine Analysis
    # ------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("  [2/4] CHAÎNE DE FAILOVER — WAVE ENGINE ANALYSIS")
    print("-" * 60)

    failover = design_failover_chain("ANTHROPIC_CLAUDE", "WAVE_ENGINE_ANALYSIS")

    print(f"\n  Service primaire   : {failover['primary_service']}")
    print(f"  Type d'opération   : {failover['operation_type']}")
    print(f"  Longueur de chaîne : {failover['chain_length']} hops")
    print(f"  Recovery latency   : {failover['expected_recovery_latency_ms']:,} ms")
    print(f"  Seuil disjoncteur  : {failover['recommended_circuit_breaker_threshold']} échecs")
    print(f"  Timeout disjoncteur: {failover['recommended_circuit_breaker_timeout_s']} s")

    print(f"\n  Chaîne de repli :")
    for hop in failover["chain"]:
        status_icon = {
            "FAILED": "✗", "AVAILABLE": "✓", "QUOTA_RISK": "~", "ALWAYS_AVAILABLE": "✓"
        }.get(hop["status"], "?")
        degradation = f"  dégradation +{hop['quality_degradation_pct']}%" if hop["quality_degradation_pct"] > 0 else ""
        print(f"    Hop {hop['hop']} [{status_icon} {hop['type']:14}] "
              f"{hop['label'][:45]:<45} "
              f" latence ~{hop['estimated_latency_ms']:>6} ms{degradation}")

    print(f"\n  Note SLA : {failover['sla_notes']}")

    # ------------------------------------------------------------------
    # 3. Allocation budget 5 000 EUR/mois
    # ------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("  [3/4] ALLOCATION BUDGET TOKENS — 5 000 EUR/MOIS")
    print("-" * 60)

    budget_result = allocate_token_budget(5000.0, TOKEN_BUDGETS)

    print(f"\n  Budget mensuel total  : {budget_result['total_monthly_budget_EUR']:,.0f} EUR")
    print(f"  Budget alloué         : {budget_result['total_allocated_EUR']:,.2f} EUR")
    print(f"  Buffer disponible     : {budget_result['remaining_buffer_EUR']:,.2f} EUR")
    print(f"  Utilisation budget    : {budget_result['budget_utilization_pct']}%")

    print(f"\n  Répartition par priorité :")
    for prio, amt in budget_result["priority_budget_breakdown"].items():
        bar_len = int(amt / 5000 * 30)
        print(f"    {prio:10} {'█' * bar_len:<30} {amt:,.0f} EUR")

    print(f"\n  Allocation par opération :")
    for op_key, alloc in budget_result["allocation_per_operation"].items():
        status_icon = {"FULLY_FUNDED": "✓", "PARTIALLY_FUNDED": "~", "THROTTLED": "✗"}.get(alloc["status"], "?")
        print(f"    [{status_icon} {alloc['status']:18}] [{alloc['priority']:8}] "
              f"{op_key:25} "
              f"{alloc['projected_runs_per_month']:>5} runs/mois  "
              f"{alloc['budget_allocated_EUR']:>7.2f} EUR")

    print(f"\n  Opérations protégées    : {', '.join(budget_result['protected_operations'])}")
    print(f"  Candidats throttling    : {', '.join(budget_result['throttling_candidates'])}")

    print(f"\n  Recommandations :")
    for rec in budget_result["recommendations"]:
        print(f"    • {rec}")

    # ------------------------------------------------------------------
    # 4. Rapport de résilience avec 3 incidents simulés
    # ------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("  [4/4] RAPPORT DE RÉSILIENCE OPÉRATIONNELLE")
    print("-" * 60)

    mock_incidents = [
        {
            "id": "INC-2026-0601-001",
            "type": "API_RATE_LIMIT",
            "severity": "P3",
            "service": "ANTHROPIC_CLAUDE",
            "started_at": "2026-06-01T09:14:00Z",
            "duration_minutes": 12,
            "resolved": True,
            "description": "Dépassement limite 4000 RPM pendant pic d'analyse Wave 198.",
            "mitigation_applied": "RETRY_WITH_BACKOFF activé + réduction concurrence",
        },
        {
            "id": "INC-2026-0610-001",
            "type": "SERVICE_OUTAGE",
            "severity": "P1",
            "service": "OPENAI_GPT4",
            "started_at": "2026-06-10T14:32:00Z",
            "duration_minutes": 47,
            "resolved": True,
            "description": "Panne OpenAI — HTTP 503 sur toutes les requêtes GPT-4o pendant 47 min.",
            "mitigation_applied": "Basculement automatique vers ANTHROPIC_CLAUDE (failover chain)",
        },
        {
            "id": "INC-2026-0618-001",
            "type": "LATENCY_SPIKE",
            "severity": "P3",
            "service": "GOOGLE_GEMINI",
            "started_at": "2026-06-18T21:05:00Z",
            "duration_minutes": 8,
            "resolved": True,
            "description": "Latence Gemini 1.5 Pro à 18 s (baseline 2.2 s) — saturation datacenter EU.",
            "mitigation_applied": "TIMEOUT_HEDGE activé — requêtes parallèles vers Cohere",
        },
    ]

    resilience = generate_resilience_report(mock_incidents, current_uptime_pct=99.61)

    metrics = resilience["metrics"]
    print(f"\n  Période analysée  : {resilience['period_analyzed']}")
    print(f"  MTTR              : {metrics['mttr_minutes']} min (cible : <15 min)")
    print(f"  MTBF              : {metrics['mtbf_hours']} h")
    print(f"  Uptime actuel     : {metrics['current_uptime_pct']}%")
    print(f"  Cible SLA         : {metrics['sla_target_pct']}%")
    print(f"  Conformité SLA    : {resilience['sla_compliance']['status']}")
    print(f"  Évaluation        : {resilience['sla_compliance']['assessment']}")

    fin = resilience["financial_impact"]
    print(f"\n  Coût indisponibilité : {fin['estimated_cost_of_downtime_EUR_hour']} EUR/heure")
    print(f"  Impact période       : {fin['downtime_cost_current_period_EUR']} EUR")
    print(f"  Base de calcul       : {fin['cost_basis']}")

    print(f"\n  Incidents :")
    inc_sum = resilience["incident_summary"]
    print(f"    Total       : {inc_sum['total_incidents']}")
    print(f"    Résolus     : {inc_sum['resolved']}")
    for sev, count in sorted(inc_sum["by_severity"].items()):
        print(f"    {sev}         : {count} incident(s)")

    spof = resilience["single_points_of_failure"]
    if spof:
        print(f"\n  Points de défaillance uniques détectés :")
        for s in spof:
            print(f"    • {s['component']} — {s['risk']}")
            print(f"      Mitigation : {s['mitigation']}")
    else:
        print(f"\n  Aucun point de défaillance unique critique détecté.")

    print(f"\n  Patterns recommandés :")
    for pat in resilience["recommended_patterns"]:
        print(f"    • {pat['pattern']:25} [score {pat['effectiveness_score']}/10 | "
              f"overhead {pat['implementation_overhead']:6}] — {pat['reason']}")

    print(f"\n  Plan d'action :")
    for action in resilience["action_plan"]:
        print(f"    • {action}")

    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — Token Manager & Resilience Agent — Demo complétée")
    print("=" * 70 + "\n")

    return True


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)
