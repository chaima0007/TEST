# KB Message — OpenAPI Generator

**Type :** Knowledge Base Message  
**Scope :** API Documentation & Client Generation  
**Caelum Partners — Internal Dev Reference**

---

## Objectif

Ce document décrit comment générer la documentation OpenAPI de la plateforme Caelum Partners et comment les clients Enterprise Premium peuvent générer leurs propres clients API à partir de cette spec.

---

## Endpoint OpenAPI Spec

```
GET /api/openapi.json
Authorization: Bearer {SWARM_API_KEY}
```

Retourne la spec OpenAPI 3.0 complète de tous les endpoints publics.

---

## Génération de client TypeScript

```bash
# Installation
npm install -g @openapitools/openapi-generator-cli

# Génération client TypeScript (axios)
openapi-generator-cli generate \
  -i https://caelumpartners.eu/api/openapi.json \
  -g typescript-axios \
  -o ./caelum-client \
  --additional-properties=supportsES6=true,npmName=caelum-client,npmVersion=1.0.0
```

---

## Génération de client Python

```bash
# Génération client Python
openapi-generator-cli generate \
  -i https://caelumpartners.eu/api/openapi.json \
  -g python \
  -o ./caelum-python-client \
  --additional-properties=packageName=caelum_client
```

---

## Endpoints disponibles (Enterprise Premium)

| Endpoint | Méthode | Description |
|---|---|---|
| `/api/kb/search` | POST | Recherche full-text dans la Knowledge Base |
| `/api/engines/{engine_id}/score` | GET | Score composite d'un engine pour une entité |
| `/api/engines/{engine_id}/entities` | GET | Liste des entités scorées par un engine |
| `/api/reports/generate` | POST | Génération d'un rapport PDF |
| `/api/alerts` | GET | Liste des alertes critiques (score ≥ 60) |

---

## Authentification

Tous les endpoints nécessitent un token Bearer :

```
Authorization: Bearer {SWARM_API_KEY}
```

Les clés API sont générées depuis le tableau de bord (Settings > API Keys).  
Durée de vie : 90 jours. Rotation recommandée mensuelle.

---

## Rate Limiting

| Tier | Requests/min | Requests/jour |
|---|---|---|
| Easy Access | N/A (pas d'API) | N/A |
| Enterprise Premium | 60 req/min | 10 000 req/jour |
| Custom (sur devis) | Illimité | Illimité |

---

## Notes de sécurité

- Ne jamais exposer la clé API dans le code frontend
- Utiliser des variables d'environnement : `CAELUM_API_KEY`
- HTTPS obligatoire — les requêtes HTTP sont rejetées
- CORS : liste blanche de domaines configurée par Caelum Partners
