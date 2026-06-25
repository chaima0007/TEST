"""
Agent Microservices API — architecture et gestion des microservices CaelumSwarm™.
Décomposition du monolithe, API gateway, service mesh, versioning et contrats d'API
pour la plateforme CSDDD.
"""

import json
import random
import math
from typing import Any

# ---------------------------------------------------------------------------
# 1. CATALOGUE DES MICROSERVICES
# ---------------------------------------------------------------------------

MICROSERVICES_CATALOG: dict[str, dict] = {
    "wave-engine-svc": {
        "label": "Moteur d'analyse de vagues CSDDD",
        "version": "v1.0.0",
        "port": 8001,
        "health_endpoint": "/health",
        "dependencies": ["data-ingestion-svc", "analytics-svc", "notification-svc"],
        "sla_uptime_pct": 99.9,
        "scaling_strategy": "HORIZONTAL",
        "team_owner": "equipe-swarm-core",
    },
    "report-generator-svc": {
        "label": "Générateur de rapports de conformité",
        "version": "v1.0.0",
        "port": 8002,
        "health_endpoint": "/health",
        "dependencies": ["wave-engine-svc", "compliance-audit-svc", "analytics-svc"],
        "sla_uptime_pct": 99.5,
        "scaling_strategy": "HORIZONTAL",
        "team_owner": "equipe-reporting",
    },
    "alert-processor-svc": {
        "label": "Processeur d'alertes et de signaux critiques",
        "version": "v1.0.0",
        "port": 8003,
        "health_endpoint": "/health",
        "dependencies": ["wave-engine-svc", "notification-svc", "user-auth-svc"],
        "sla_uptime_pct": 99.9,
        "scaling_strategy": "HORIZONTAL",
        "team_owner": "equipe-alerting",
    },
    "legal-watch-svc": {
        "label": "Veille juridique et réglementaire CSDDD",
        "version": "v1.0.0",
        "port": 8004,
        "health_endpoint": "/health",
        "dependencies": ["data-ingestion-svc", "compliance-audit-svc"],
        "sla_uptime_pct": 99.5,
        "scaling_strategy": "VERTICAL",
        "team_owner": "equipe-legal",
    },
    "press-relations-svc": {
        "label": "Service relations presse et communication",
        "version": "v1.0.0",
        "port": 8005,
        "health_endpoint": "/health",
        "dependencies": ["report-generator-svc", "user-auth-svc"],
        "sla_uptime_pct": 99.5,
        "scaling_strategy": "VERTICAL",
        "team_owner": "equipe-communication",
    },
    "compliance-audit-svc": {
        "label": "Audit de conformité et traçabilité",
        "version": "v1.0.0",
        "port": 8006,
        "health_endpoint": "/health",
        "dependencies": ["data-ingestion-svc", "user-auth-svc", "analytics-svc"],
        "sla_uptime_pct": 99.9,
        "scaling_strategy": "HORIZONTAL",
        "team_owner": "equipe-compliance",
    },
    "user-auth-svc": {
        "label": "Authentification et gestion des identités",
        "version": "v1.0.0",
        "port": 8007,
        "health_endpoint": "/health",
        "dependencies": [],
        "sla_uptime_pct": 99.9,
        "scaling_strategy": "HORIZONTAL",
        "team_owner": "equipe-securite",
    },
    "data-ingestion-svc": {
        "label": "Ingestion et normalisation des données",
        "version": "v1.0.0",
        "port": 8008,
        "health_endpoint": "/health",
        "dependencies": ["user-auth-svc"],
        "sla_uptime_pct": 99.9,
        "scaling_strategy": "HORIZONTAL",
        "team_owner": "equipe-data",
    },
    "notification-svc": {
        "label": "Notifications multi-canal (email, SMS, webhook)",
        "version": "v1.0.0",
        "port": 8009,
        "health_endpoint": "/health",
        "dependencies": ["user-auth-svc"],
        "sla_uptime_pct": 99.5,
        "scaling_strategy": "HORIZONTAL",
        "team_owner": "equipe-notifications",
    },
    "analytics-svc": {
        "label": "Analytique avancée et tableaux de bord",
        "version": "v1.0.0",
        "port": 8010,
        "health_endpoint": "/health",
        "dependencies": ["data-ingestion-svc", "user-auth-svc"],
        "sla_uptime_pct": 99.5,
        "scaling_strategy": "HORIZONTAL",
        "team_owner": "equipe-analytics",
    },
}

# ---------------------------------------------------------------------------
# 2. CONFIGURATION DE L'API GATEWAY
# ---------------------------------------------------------------------------

API_GATEWAY_CONFIG: dict[str, Any] = {
    "rate_limiting": {
        "per_tier": {
            "FREE": {"requests_per_minute": 60, "requests_per_day": 1_000},
            "STARTER": {"requests_per_minute": 300, "requests_per_day": 10_000},
            "PROFESSIONAL": {"requests_per_minute": 1_000, "requests_per_day": 100_000},
            "ENTERPRISE": {"requests_per_minute": 5_000, "requests_per_day": 5_000_000},
        }
    },
    "authentication": ["JWT", "API_KEY", "mTLS"],
    "routing_rules": [
        {
            "path_prefix": "/api/v1/waves",
            "service": "wave-engine-svc",
            "strip_prefix": False,
            "timeout_ms": 5_000,
            "retry_count": 3,
        },
        {
            "path_prefix": "/api/v1/reports",
            "service": "report-generator-svc",
            "strip_prefix": False,
            "timeout_ms": 30_000,
            "retry_count": 2,
        },
        {
            "path_prefix": "/api/v1/alerts",
            "service": "alert-processor-svc",
            "strip_prefix": False,
            "timeout_ms": 2_000,
            "retry_count": 3,
        },
        {
            "path_prefix": "/api/v1/legal",
            "service": "legal-watch-svc",
            "strip_prefix": False,
            "timeout_ms": 10_000,
            "retry_count": 2,
        },
        {
            "path_prefix": "/api/v1/press",
            "service": "press-relations-svc",
            "strip_prefix": False,
            "timeout_ms": 8_000,
            "retry_count": 2,
        },
        {
            "path_prefix": "/api/v1/compliance",
            "service": "compliance-audit-svc",
            "strip_prefix": False,
            "timeout_ms": 15_000,
            "retry_count": 3,
        },
        {
            "path_prefix": "/api/v1/auth",
            "service": "user-auth-svc",
            "strip_prefix": False,
            "timeout_ms": 1_000,
            "retry_count": 1,
        },
        {
            "path_prefix": "/api/v1/data",
            "service": "data-ingestion-svc",
            "strip_prefix": False,
            "timeout_ms": 20_000,
            "retry_count": 3,
        },
        {
            "path_prefix": "/api/v1/notifications",
            "service": "notification-svc",
            "strip_prefix": False,
            "timeout_ms": 3_000,
            "retry_count": 2,
        },
        {
            "path_prefix": "/api/v1/analytics",
            "service": "analytics-svc",
            "strip_prefix": False,
            "timeout_ms": 12_000,
            "retry_count": 2,
        },
    ],
    "circuit_breaker": {
        "threshold_pct": 50,
        "timeout_s": 30,
        "half_open_requests": 5,
    },
    "observability": {
        "tracing": True,
        "metrics": True,
        "logging": True,
    },
}

# ---------------------------------------------------------------------------
# 3. STRATÉGIES DE VERSIONING D'API
# ---------------------------------------------------------------------------

API_VERSIONING_STRATEGY: dict[str, dict] = {
    "URL_PATH_v1v2": {
        "label": "Versioning par chemin d'URL",
        "example": "GET /api/v2/waves/{id}",
        "backward_compat_guarantee": True,
        "deprecation_notice_months": 12,
        "caelum_choice": True,
    },
    "HEADER_VERSIONING": {
        "label": "Versioning par en-tête HTTP",
        "example": "X-API-Version: 2024-01-01",
        "backward_compat_guarantee": True,
        "deprecation_notice_months": 6,
        "caelum_choice": False,
    },
    "QUERY_PARAM": {
        "label": "Versioning par paramètre de requête",
        "example": "GET /api/waves?version=2",
        "backward_compat_guarantee": False,
        "deprecation_notice_months": 3,
        "caelum_choice": False,
    },
    "CONTENT_NEGOTIATION": {
        "label": "Versioning par négociation de contenu",
        "example": "Accept: application/vnd.caelum.v2+json",
        "backward_compat_guarantee": True,
        "deprecation_notice_months": 9,
        "caelum_choice": False,
    },
}

# ---------------------------------------------------------------------------
# 4. CONTRATS D'API
# ---------------------------------------------------------------------------

SERVICE_CONTRACTS: dict[str, dict] = {
    "WAVE_ENGINE_CONTRACT": {
        "openapi_version": "3.1.0",
        "endpoints": [
            {
                "path": "/api/v1/waves",
                "method": "POST",
                "summary": "Lancer une analyse de vague CSDDD",
                "request_schema": {
                    "domain": "string",
                    "entities": "array[string]",
                    "depth": "integer",
                },
                "response_schema": {
                    "wave_id": "string",
                    "composite_score": "number",
                    "distribution": "object",
                    "estimated_index": "number",
                },
                "auth_required": True,
            },
            {
                "path": "/api/v1/waves/{wave_id}",
                "method": "GET",
                "summary": "Récupérer les résultats d'une vague",
                "request_schema": {"wave_id": "string"},
                "response_schema": {
                    "wave_id": "string",
                    "status": "string",
                    "results": "object",
                    "created_at": "string",
                },
                "auth_required": True,
            },
            {
                "path": "/api/v1/waves/{wave_id}/entities",
                "method": "GET",
                "summary": "Lister les entités d'une vague",
                "request_schema": {"wave_id": "string"},
                "response_schema": {"entities": "array[object]", "total": "integer"},
                "auth_required": True,
            },
        ],
        "breaking_change_policy": "Préavis 12 mois + migration guide obligatoire",
        "consumer_driven_tests": True,
    },
    "REPORT_CONTRACT": {
        "openapi_version": "3.1.0",
        "endpoints": [
            {
                "path": "/api/v1/reports",
                "method": "POST",
                "summary": "Générer un rapport de conformité CSDDD",
                "request_schema": {
                    "wave_ids": "array[string]",
                    "format": "enum[PDF,XLSX,JSON]",
                    "language": "enum[fr,en,de]",
                },
                "response_schema": {
                    "report_id": "string",
                    "status": "string",
                    "estimated_completion_s": "integer",
                },
                "auth_required": True,
            },
            {
                "path": "/api/v1/reports/{report_id}/download",
                "method": "GET",
                "summary": "Télécharger un rapport généré",
                "request_schema": {"report_id": "string"},
                "response_schema": {"download_url": "string", "expires_in_s": "integer"},
                "auth_required": True,
            },
        ],
        "breaking_change_policy": "Préavis 6 mois + dépréciation progressive",
        "consumer_driven_tests": True,
    },
    "ALERT_CONTRACT": {
        "openapi_version": "3.1.0",
        "endpoints": [
            {
                "path": "/api/v1/alerts",
                "method": "GET",
                "summary": "Lister les alertes actives",
                "request_schema": {
                    "severity": "enum[CRITICAL,HIGH,MEDIUM,LOW]",
                    "limit": "integer",
                },
                "response_schema": {
                    "alerts": "array[object]",
                    "total": "integer",
                    "critical_count": "integer",
                },
                "auth_required": True,
            },
            {
                "path": "/api/v1/alerts/{alert_id}/acknowledge",
                "method": "PATCH",
                "summary": "Acquitter une alerte",
                "request_schema": {"alert_id": "string", "note": "string"},
                "response_schema": {"acknowledged": "boolean", "updated_at": "string"},
                "auth_required": True,
            },
        ],
        "breaking_change_policy": "Préavis 12 mois — critique pour intégrateurs",
        "consumer_driven_tests": True,
    },
    "AUTH_CONTRACT": {
        "openapi_version": "3.1.0",
        "endpoints": [
            {
                "path": "/api/v1/auth/token",
                "method": "POST",
                "summary": "Obtenir un jeton JWT",
                "request_schema": {"client_id": "string", "client_secret": "string"},
                "response_schema": {
                    "access_token": "string",
                    "expires_in": "integer",
                    "token_type": "string",
                },
                "auth_required": False,
            },
            {
                "path": "/api/v1/auth/introspect",
                "method": "POST",
                "summary": "Valider un jeton JWT",
                "request_schema": {"token": "string"},
                "response_schema": {"active": "boolean", "scope": "string", "sub": "string"},
                "auth_required": True,
            },
            {
                "path": "/api/v1/auth/revoke",
                "method": "POST",
                "summary": "Révoquer un jeton",
                "request_schema": {"token": "string"},
                "response_schema": {"revoked": "boolean"},
                "auth_required": True,
            },
        ],
        "breaking_change_policy": "Préavis 18 mois — contrat fondamental de la plateforme",
        "consumer_driven_tests": True,
    },
    "COMPLIANCE_CONTRACT": {
        "openapi_version": "3.1.0",
        "endpoints": [
            {
                "path": "/api/v1/compliance/audit",
                "method": "POST",
                "summary": "Déclencher un audit de conformité",
                "request_schema": {
                    "entity_id": "string",
                    "regulation": "enum[CSDDD,CSRD,GDPR]",
                    "scope": "enum[FULL,PARTIAL]",
                },
                "response_schema": {
                    "audit_id": "string",
                    "score": "number",
                    "gaps": "array[object]",
                    "remediation_plan": "object",
                },
                "auth_required": True,
            },
            {
                "path": "/api/v1/compliance/audit/{audit_id}/certificate",
                "method": "GET",
                "summary": "Récupérer le certificat de conformité",
                "request_schema": {"audit_id": "string"},
                "response_schema": {
                    "certificate_url": "string",
                    "valid_until": "string",
                    "issuer": "string",
                },
                "auth_required": True,
            },
        ],
        "breaking_change_policy": "Préavis 12 mois — impact réglementaire direct",
        "consumer_driven_tests": False,
    },
}

# ---------------------------------------------------------------------------
# 5. FONCTIONS PRINCIPALES
# ---------------------------------------------------------------------------


def decompose_service(service_name: str, responsibilities: list) -> dict:
    """
    Applique la décomposition single-responsibility (SRP) sur un service donné.

    Identifie les contextes délimités (Bounded Contexts DDD), propose un découpage
    en sous-services, mappe la propriété des données et évalue la complexité
    de migration.
    """
    n = len(responsibilities)

    # Dériver les contextes délimités : regrouper les responsabilités par domaine fonctionnel
    bounded_contexts = []
    domain_keywords = {
        "calcul": "Contexte Calcul & Scoring",
        "analyse": "Contexte Analyse & Intelligence",
        "rapport": "Contexte Reporting & Diffusion",
        "alerte": "Contexte Alerting & Surveillance",
        "auth": "Contexte Identité & Sécurité",
        "donnée": "Contexte Ingestion & Stockage des Données",
        "notif": "Contexte Notifications & Communication",
        "audit": "Contexte Conformité & Audit",
        "entité": "Contexte Gestion des Entités",
        "wave": "Contexte Orchestration des Vagues",
        "compl": "Contexte Conformité Réglementaire",
        "lég": "Contexte Veille Juridique",
        "press": "Contexte Relations Médias",
    }

    seen_contexts: set[str] = set()
    for resp in responsibilities:
        resp_lower = resp.lower()
        matched = False
        for kw, ctx in domain_keywords.items():
            if kw in resp_lower and ctx not in seen_contexts:
                bounded_contexts.append(ctx)
                seen_contexts.add(ctx)
                matched = True
                break
        if not matched:
            generic_ctx = f"Contexte {resp.split()[0].capitalize()}"
            if generic_ctx not in seen_contexts:
                bounded_contexts.append(generic_ctx)
                seen_contexts.add(generic_ctx)

    # Proposer le découpage en sous-services
    suggested_split = []
    for i, resp in enumerate(responsibilities):
        slug = resp.lower().replace(" ", "-").replace("/", "-")[:30]
        sub_svc = f"{service_name}-{slug}-svc" if n > 1 else service_name
        suggested_split.append({
            "sub_service": sub_svc,
            "responsibility": resp,
            "bounded_context": bounded_contexts[i % len(bounded_contexts)],
            "estimated_pod_count": 2 if i < n // 2 else 1,
        })

    # Carte de propriété des données
    data_ownership_map = {
        svc["sub_service"]: {
            "owns_data": True,
            "data_store": "PostgreSQL" if i % 3 == 0 else ("Redis" if i % 3 == 1 else "MongoDB"),
            "shared_with": [other["sub_service"] for j, other in enumerate(suggested_split) if j != i][:2],
        }
        for i, svc in enumerate(suggested_split)
    }

    # Surface API exposée
    api_surface = {
        "internal_endpoints": len(responsibilities) * 3,
        "public_endpoints": max(1, len(responsibilities) // 2),
        "async_events": len(responsibilities),
        "protocols": ["REST/JSON", "gRPC (interne)", "AMQP (événements)"],
    }

    # Complexité de migration
    if n <= 2:
        migration_complexity = "LOW"
    elif n <= 5:
        migration_complexity = "MEDIUM"
    else:
        migration_complexity = "HIGH"

    return {
        "service_name": service_name,
        "responsibilities_count": n,
        "bounded_contexts": bounded_contexts,
        "suggested_split": suggested_split,
        "data_ownership_map": data_ownership_map,
        "api_surface": api_surface,
        "migration_complexity": migration_complexity,
    }


def generate_openapi_spec(service: str, version: str) -> dict:
    """
    Génère une structure de spécification OpenAPI 3.1 pour un microservice donné.

    Construit le document complet (info, servers, paths, composants, sécurité),
    produit un aperçu YAML simplifié et identifie les breaking changes
    par rapport à la version précédente.
    """
    svc_meta = MICROSERVICES_CATALOG.get(service, {})
    label = svc_meta.get("label", service)
    port = svc_meta.get("port", 8000)

    # Récupérer les endpoints depuis les contrats si disponibles
    contract_key = service.upper().replace("-SVC", "_CONTRACT").replace("-", "_")
    contract = SERVICE_CONTRACTS.get(contract_key, {})
    contract_endpoints = contract.get("endpoints", [])

    # Construire les paths OpenAPI
    paths: dict[str, Any] = {}
    for ep in contract_endpoints:
        path = ep["path"]
        method = ep["method"].lower()
        req_schema = ep.get("request_schema", {})
        resp_schema = ep.get("response_schema", {})

        request_properties = {
            k: {"type": v.split("[")[0] if "[" not in v else "array"}
            for k, v in req_schema.items()
        }
        response_properties = {
            k: {"type": v.split("[")[0] if "[" not in v else "array"}
            for k, v in resp_schema.items()
        }

        path_item = {
            method: {
                "summary": ep.get("summary", ""),
                "operationId": f"{method}_{path.replace('/', '_').strip('_')}",
                "security": [{"BearerAuth": []}] if ep.get("auth_required") else [],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": request_properties,
                            }
                        }
                    },
                } if method in ("post", "patch", "put") else None,
                "parameters": [
                    {
                        "name": k,
                        "in": "path" if f"{{{k}}}" in path else "query",
                        "required": f"{{{k}}}" in path,
                        "schema": {"type": "string"},
                    }
                    for k in req_schema
                    if method in ("get", "delete")
                ],
                "responses": {
                    "200": {
                        "description": "Succès",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": response_properties,
                                }
                            }
                        },
                    },
                    "400": {"description": "Requête invalide"},
                    "401": {"description": "Non authentifié"},
                    "403": {"description": "Accès refusé"},
                    "502": {"description": "Service upstream indisponible"},
                },
            }
        }
        # Nettoyer les requestBody None
        if path_item[method].get("requestBody") is None:
            del path_item[method]["requestBody"]

        if path in paths:
            paths[path].update(path_item)
        else:
            paths[path] = path_item

    # Fallback si aucun contrat trouvé
    if not paths:
        paths[f"/api/{version}/{service.replace('-svc', '')}"] = {
            "get": {
                "summary": f"Point d'entrée principal de {label}",
                "operationId": "getRoot",
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {"description": "Succès"},
                    "502": {"description": "Service upstream indisponible"},
                },
            }
        }

    openapi_document = {
        "openapi": "3.1.0",
        "info": {
            "title": f"CaelumSwarm™ — {label}",
            "version": version,
            "description": f"API officielle du microservice {service} pour la plateforme CSDDD.",
            "contact": {
                "name": "Caelum Partners API Team",
                "email": "api-support@caelum-partners.com",
            },
            "license": {"name": "Proprietary", "url": "https://caelum-partners.com/license"},
        },
        "servers": [
            {
                "url": f"https://api.caelum-partners.com",
                "description": "Production Gateway",
            },
            {
                "url": f"https://staging-api.caelum-partners.com",
                "description": "Staging Gateway",
            },
            {
                "url": f"http://localhost:{port}",
                "description": "Développement local",
            },
        ],
        "paths": paths,
        "components": {
            "schemas": {
                "Error": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "message": {"type": "string"},
                        "request_id": {"type": "string"},
                    },
                    "required": ["code", "message"],
                },
                "HealthResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": ["UP", "DOWN", "DEGRADED"]},
                        "service": {"type": "string"},
                        "version": {"type": "string"},
                        "uptime_s": {"type": "integer"},
                    },
                },
            },
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                },
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key",
                },
            },
        },
        "security": [{"BearerAuth": []}],
    }

    # Aperçu YAML simplifié (format lisible)
    spec_preview_lines = [
        f"openapi: '3.1.0'",
        f"info:",
        f"  title: 'CaelumSwarm™ — {label}'",
        f"  version: '{version}'",
        f"servers:",
        f"  - url: 'https://api.caelum-partners.com'",
        f"    description: Production Gateway",
        f"paths:",
    ]
    for path_key, path_val in paths.items():
        spec_preview_lines.append(f"  {path_key}:")
        for method_key in path_val:
            spec_preview_lines.append(f"    {method_key}:")
            spec_preview_lines.append(f"      summary: '{path_val[method_key].get('summary', '')}'")

    spec_preview_yaml = "\n".join(spec_preview_lines)
    endpoint_count = len(paths)

    # Identifier les breaking changes par rapport à la version précédente
    # On simule une logique de détection basée sur la version
    breaking_changes_vs_previous: list[str] = []
    if version.startswith("v2"):
        breaking_changes_vs_previous = [
            "Suppression du champ 'legacy_score' dans les réponses (remplacé par 'composite_score')",
            "Le paramètre 'entity_ids' devient obligatoire (était optionnel en v1)",
            "Format de date modifié : ISO 8601 strict (YYYY-MM-DDTHH:MM:SSZ) au lieu d'epoch",
        ]
    elif version.startswith("v1"):
        breaking_changes_vs_previous = []

    return {
        "openapi_document": openapi_document,
        "spec_preview_yaml": spec_preview_yaml,
        "endpoint_count": endpoint_count,
        "breaking_changes_vs_previous": breaking_changes_vs_previous,
    }


def validate_service_health(services: list) -> dict:
    """
    Vérifie l'état de santé de tous les microservices listés.

    Simule des latences réalistes, détecte les défaillances en cascade,
    évalue l'état du circuit breaker et recommande des actions correctrices.
    """
    # Simuler des états de santé (déterministe via hash du nom)
    health_matrix: dict[str, dict] = {}
    degraded_services: list[str] = []
    circuit_breaker_state: dict[str, str] = {}

    # Simuler 2 services en échec pour le test
    forced_failures = set()
    if len(services) >= 2:
        forced_failures = {services[0], services[1]}

    for svc in services:
        svc_meta = MICROSERVICES_CATALOG.get(svc, {})
        deps = svc_meta.get("dependencies", [])

        if svc in forced_failures:
            status = "DOWN"
            latency_ms = None
        else:
            # Latence pseudo-aléatoire déterministe
            seed = sum(ord(c) for c in svc)
            base_latency = (seed % 80) + 20  # 20–100 ms
            # Dégradation si une dépendance est en panne
            dep_failures = [d for d in deps if d in forced_failures]
            if dep_failures:
                status = "DEGRADED"
                latency_ms = base_latency * 3
                degraded_services.append(svc)
            else:
                status = "UP"
                latency_ms = base_latency

        # État des dépendances
        dep_health = {}
        for dep in deps:
            if dep in forced_failures:
                dep_health[dep] = "DOWN"
            elif dep in degraded_services:
                dep_health[dep] = "DEGRADED"
            else:
                dep_health[dep] = "UP"

        health_matrix[svc] = {
            "status": status,
            "latency_ms": latency_ms,
            "dependencies": dep_health,
            "sla_uptime_pct": svc_meta.get("sla_uptime_pct", 99.5),
            "last_checked": "2026-06-21T00:00:00Z",
        }

        # Circuit breaker
        if status == "DOWN":
            circuit_breaker_state[svc] = "OPEN"
        elif status == "DEGRADED":
            circuit_breaker_state[svc] = "HALF_OPEN"
        else:
            circuit_breaker_state[svc] = "CLOSED"

    # Risque de cascade : un service DOWN avec SLA 99.9 affectant ≥3 dépendants
    cascading_failure_risk = any(
        health_matrix[svc]["status"] == "DOWN"
        and MICROSERVICES_CATALOG.get(svc, {}).get("sla_uptime_pct", 0) >= 99.9
        and sum(
            1
            for other in services
            if svc in MICROSERVICES_CATALOG.get(other, {}).get("dependencies", [])
        ) >= 2
        for svc in services
    )

    # Actions recommandées
    recommended_actions: list[str] = []
    down_svcs = [s for s, h in health_matrix.items() if h["status"] == "DOWN"]
    half_open_svcs = [s for s, st in circuit_breaker_state.items() if st == "HALF_OPEN"]

    for svc in down_svcs:
        recommended_actions.append(
            f"[CRITIQUE] Redémarrer le pod {svc} et vérifier les logs Kubernetes"
        )
    for svc in half_open_svcs:
        recommended_actions.append(
            f"[AVERTISSEMENT] Circuit breaker HALF_OPEN sur {svc} — surveiller les erreurs"
        )
    if cascading_failure_risk:
        recommended_actions.append(
            "[URGENCE] Risque de défaillance en cascade détecté — activer le mode dégradé "
            "et prioriser la restauration des services fondamentaux"
        )
    if not recommended_actions:
        recommended_actions.append("Tous les services sont opérationnels — aucune action requise")

    return {
        "health_matrix": health_matrix,
        "circuit_breaker_state": circuit_breaker_state,
        "degraded_services": degraded_services,
        "cascading_failure_risk": cascading_failure_risk,
        "recommended_actions": recommended_actions,
    }


def design_api_migration_plan(from_monolith: str, to_microservices: list) -> dict:
    """
    Conçoit un plan de migration Strangler Fig du monolithe vers les microservices.

    Découpe la migration en phases progressives avec niveaux de risque,
    plans de rollback, durées estimées et métriques de succès.
    """
    n_services = len(to_microservices)

    # Priorité de migration : d'abord les services sans dépendances (leaf nodes)
    def _has_no_deps(svc: str) -> bool:
        return len(MICROSERVICES_CATALOG.get(svc, {}).get("dependencies", [])) == 0

    leaf_services = [s for s in to_microservices if _has_no_deps(s)]
    mid_services = [s for s in to_microservices if not _has_no_deps(s)]

    # Partitionner en vagues de migration
    phase_size = max(1, math.ceil(n_services / 4))
    phases_raw = [
        to_microservices[i: i + phase_size]
        for i in range(0, n_services, phase_size)
    ]

    phase_configs = [
        {
            "phase_name": "Phase 1 — Fondations & Services Feuilles",
            "risk_level": "LOW",
            "base_duration_weeks": 4,
        },
        {
            "phase_name": "Phase 2 — Services Métier Principaux",
            "risk_level": "MEDIUM",
            "base_duration_weeks": 6,
        },
        {
            "phase_name": "Phase 3 — Services Orchestration & Gateway",
            "risk_level": "HIGH",
            "base_duration_weeks": 8,
        },
        {
            "phase_name": "Phase 4 — Décommissionnement du Monolithe",
            "risk_level": "MEDIUM",
            "base_duration_weeks": 4,
        },
    ]

    phases = []
    cumulative_weeks = 0
    for i, batch in enumerate(phases_raw):
        cfg = phase_configs[i % len(phase_configs)]
        duration = cfg["base_duration_weeks"]
        cumulative_weeks += duration
        phases.append({
            "phase_name": cfg["phase_name"],
            "services_to_extract": batch,
            "duration_weeks": duration,
            "risk_level": cfg["risk_level"],
            "rollback_plan": (
                f"Réactiver les routes monolithe pour {', '.join(batch)} via feature flag. "
                f"Bascule DNS en moins de 5 minutes. Durée max de rollback : 30 min."
            ),
            "start_week": cumulative_weeks - duration + 1,
            "end_week": cumulative_weeks,
        })

    # Estimation de l'équipe nécessaire
    team_required = {
        "architects": 2,
        "backend_engineers": max(3, n_services // 2),
        "devops_sre": 2,
        "qa_engineers": 2,
        "product_owner": 1,
        "security_engineer": 1,
        "total": max(3, n_services // 2) + 8,
    }

    # Évaluation des risques
    risk_assessment = {
        "technical_debt_reduction": "ÉLEVÉ — le monolithe accumule ~40% de couplage fort",
        "data_consistency_risk": "MOYEN — migration progressive avec double-écriture temporaire",
        "performance_regression_risk": "FAIBLE — tests de charge requis avant chaque phase",
        "team_skill_gap_risk": "MOYEN — formation Kubernetes/service mesh requise",
        "vendor_lock_in_risk": "FAIBLE — stack cloud-agnostique (Kubernetes + Istio)",
        "overall_risk": "MOYEN",
    }

    # Métriques de succès
    success_metrics = [
        "Temps de réponse P99 < 200ms pour les APIs critiques (wave-engine, auth)",
        "Disponibilité ≥ 99.9% pour les services SLA gold pendant la migration",
        "Zéro régression fonctionnelle mesurée par les tests contrat (Pact)",
        "Réduction du Mean Time To Deploy (MTTD) de 4h → 15min par service",
        "Couverture de tests d'intégration ≥ 80% avant décommissionnement",
        "Score DORA (Deployment Frequency, Lead Time, MTTR, Change Failure Rate) en amélioration",
        f"Tous les {n_services} microservices opérationnels en production avant fin Phase 4",
    ]

    return {
        "from_monolith": from_monolith,
        "to_microservices": to_microservices,
        "pattern": "Strangler Fig (Martin Fowler, 2004)",
        "phases": phases,
        "total_duration_weeks": cumulative_weeks,
        "team_required": team_required,
        "risk_assessment": risk_assessment,
        "success_metrics": success_metrics,
    }


# ---------------------------------------------------------------------------
# 6. DÉMONSTRATION
# ---------------------------------------------------------------------------


def run_demo() -> bool:
    """
    Démonstration complète de l'agent microservices API CaelumSwarm™.

    Enchaîne : décomposition du Wave Engine, génération spec OpenAPI v2,
    validation santé des 10 services (2 pannes simulées),
    et plan de migration Strangler Fig.
    """
    separator = "=" * 72

    print(separator)
    print("  AGENT MICROSERVICES API — CaelumSwarm™  CSDDD Platform")
    print(separator)

    # ------------------------------------------------------------------ #
    # DÉMO 1 : Décomposition du Wave Engine
    # ------------------------------------------------------------------ #
    print("\n[1/4] DÉCOMPOSITION — CaelumSwarm™ Wave Engine\n")

    wave_responsibilities = [
        "Calcul des scores composites par entité",
        "Analyse de la distribution critique/élevé/modéré/faible",
        "Orchestration des agents d'analyse parallèles",
        "Gestion du cache des résultats de vague",
        "Validation et normalisation des données d'entrée",
    ]

    decomp = decompose_service("wave-engine-svc", wave_responsibilities)

    print(f"  Service source      : {decomp['service_name']}")
    print(f"  Responsabilités     : {decomp['responsibilities_count']}")
    print(f"  Complexité migration: {decomp['migration_complexity']}")
    print(f"\n  Contextes délimités ({len(decomp['bounded_contexts'])}) :")
    for ctx in decomp["bounded_contexts"]:
        print(f"    • {ctx}")
    print(f"\n  Découpage proposé ({len(decomp['suggested_split'])} sous-services) :")
    for split in decomp["suggested_split"]:
        print(f"    → {split['sub_service']}")
        print(f"       Responsabilité : {split['responsibility']}")
        print(f"       Pods estimés   : {split['estimated_pod_count']}")
    print(f"\n  Surface API totale  : {decomp['api_surface']['internal_endpoints']} endpoints internes"
          f", {decomp['api_surface']['public_endpoints']} publics")

    # ------------------------------------------------------------------ #
    # DÉMO 2 : Génération de spec OpenAPI v2
    # ------------------------------------------------------------------ #
    print(f"\n{separator}")
    print("\n[2/4] GÉNÉRATION SPEC OPENAPI — wave-engine-svc v2\n")

    spec_result = generate_openapi_spec("wave-engine-svc", "v2.0.0")

    print(f"  Version OpenAPI     : {spec_result['openapi_document']['openapi']}")
    print(f"  Titre               : {spec_result['openapi_document']['info']['title']}")
    print(f"  Endpoints générés   : {spec_result['endpoint_count']}")

    breaking = spec_result["breaking_changes_vs_previous"]
    if breaking:
        print(f"\n  Breaking changes vs v1 ({len(breaking)}) :")
        for bc in breaking:
            print(f"    ⚠  {bc}")
    else:
        print("\n  Aucun breaking change détecté.")

    print(f"\n  Aperçu spec YAML :\n")
    for line in spec_result["spec_preview_yaml"].split("\n")[:20]:
        print(f"    {line}")
    print("    ...")

    # ------------------------------------------------------------------ #
    # DÉMO 3 : Validation santé des 10 services
    # ------------------------------------------------------------------ #
    print(f"\n{separator}")
    print("\n[3/4] VALIDATION SANTÉ — 10 microservices (2 pannes simulées)\n")

    all_services = list(MICROSERVICES_CATALOG.keys())
    # Simuler user-auth-svc et data-ingestion-svc en panne (services fondamentaux)
    simulated_failures = ["user-auth-svc", "data-ingestion-svc"]
    services_to_check = simulated_failures + [s for s in all_services if s not in simulated_failures]

    health = validate_service_health(services_to_check)

    status_icons = {"UP": "✓", "DEGRADED": "~", "DOWN": "✗"}
    cb_icons = {"CLOSED": "[FERMÉ]", "HALF_OPEN": "[DEMI]", "OPEN": "[OUVERT]"}

    print(f"  {'SERVICE':<35} {'ÉTAT':<10} {'LATENCE':<12} {'CIRCUIT BREAKER'}")
    print(f"  {'-'*35} {'-'*10} {'-'*12} {'-'*20}")
    for svc, info in health["health_matrix"].items():
        icon = status_icons.get(info["status"], "?")
        lat = f"{info['latency_ms']}ms" if info["latency_ms"] is not None else "N/A"
        cb = cb_icons.get(health["circuit_breaker_state"].get(svc, "?"), "?")
        print(f"  {svc:<35} {icon} {info['status']:<8} {lat:<12} {cb}")

    print(f"\n  Services dégradés   : {health['degraded_services'] or ['aucun']}")
    print(f"  Risque de cascade   : {'OUI — action immédiate requise' if health['cascading_failure_risk'] else 'Non'}")
    print(f"\n  Actions recommandées :")
    for action in health["recommended_actions"]:
        print(f"    → {action}")

    # ------------------------------------------------------------------ #
    # DÉMO 4 : Plan de migration Strangler Fig
    # ------------------------------------------------------------------ #
    print(f"\n{separator}")
    print("\n[4/4] PLAN DE MIGRATION — Monolithe → Microservices (Strangler Fig)\n")

    migration = design_api_migration_plan(
        from_monolith="caelum-monolith-v0",
        to_microservices=list(MICROSERVICES_CATALOG.keys()),
    )

    print(f"  Monolithe source    : {migration['from_monolith']}")
    print(f"  Pattern             : {migration['pattern']}")
    print(f"  Services cibles     : {len(migration['to_microservices'])}")
    print(f"  Durée totale        : {migration['total_duration_weeks']} semaines")
    print(f"\n  Équipe requise :")
    team = migration["team_required"]
    print(f"    Architectes        : {team['architects']}")
    print(f"    Ingénieurs backend : {team['backend_engineers']}")
    print(f"    DevOps/SRE         : {team['devops_sre']}")
    print(f"    QA                 : {team['qa_engineers']}")
    print(f"    Total              : {team['total']} personnes")

    print(f"\n  Phases de migration :")
    for phase in migration["phases"]:
        risk_tag = {"LOW": "[FAIBLE]", "MEDIUM": "[MOYEN]", "HIGH": "[ÉLEVÉ]"}.get(
            phase["risk_level"], phase["risk_level"]
        )
        print(f"\n    {phase['phase_name']} — Semaines {phase['start_week']}–{phase['end_week']}")
        print(f"      Risque     : {risk_tag}")
        print(f"      Services   : {', '.join(phase['services_to_extract'])}")
        print(f"      Rollback   : {phase['rollback_plan'][:80]}...")

    print(f"\n  Risque global       : {migration['risk_assessment']['overall_risk']}")
    print(f"\n  Métriques de succès :")
    for metric in migration["success_metrics"][:4]:
        print(f"    ✓ {metric}")
    print(f"    ... et {len(migration['success_metrics']) - 4} autres métriques")

    print(f"\n{separator}")
    print("  Démonstration terminée — Agent Microservices API CaelumSwarm™")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# 7. POINT D'ENTRÉE
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    if success:
        print("\n[OK] Agent microservices-api-agent.py exécuté avec succès.")
