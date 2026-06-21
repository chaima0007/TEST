# KB Message — API Endpoints Reference

**Type :** Knowledge Base Message  
**Scope :** Complete API Endpoint Documentation  
**Caelum Partners — Internal Dev Reference**

---

## Base URL

```
Production : https://caelumpartners.eu/api
Staging    : https://staging.caelumpartners.eu/api
```

---

## Authentification

Toutes les requêtes doivent inclure :

```
Authorization: Bearer {CAELUM_API_KEY}
Content-Type: application/json
```

---

## Endpoints Knowledge Base

### POST /kb/search
Recherche full-text dans la Knowledge Base.

**Accès :** Enterprise Premium uniquement

**Request body :**
```json
{
  "query": "string (required)",
  "engine_filter": ["string"] ,
  "severity_filter": ["critique", "élevé", "modéré", "faible"],
  "limit": 10,
  "offset": 0
}
```

**Response 200 :**
```json
{
  "results": [...],
  "total": 42,
  "query_time_ms": 23
}
```

---

## Endpoints Engines

### GET /engines
Liste tous les engines disponibles pour le compte.

**Response 200 :**
```json
{
  "engines": [
    {
      "engine_id": "land-grabbing-rights-engine",
      "engine_name": "Land Grabbing Rights Engine",
      "domain": "land_rights",
      "entity_count": 8,
      "last_updated": "2026-06-21T00:00:00Z"
    }
  ]
}
```

---

### GET /engines/{engine_id}/entities
Score de toutes les entités pour un engine.

**Path params :**
- `engine_id` : ID de l'engine (ex: `land-grabbing-rights-engine`)

**Query params :**
- `severity` : filtrer par sévérité (`critique` | `élevé` | `modéré` | `faible`)
- `sort` : `score_desc` (défaut) | `score_asc` | `entity_name`

**Response 200 :**
```json
{
  "engine_id": "land-grabbing-rights-engine",
  "entities": [
    {
      "entity_id": "cambodia",
      "entity_name": "Cambodge",
      "composite_score": 93.75,
      "severity": "critique",
      "estimated_index": 9.38,
      "primary_pattern": "Déplacement forcé sans consultation préalable"
    }
  ]
}
```

---

### GET /engines/{engine_id}/score
Score détaillé d'une entité spécifique.

**Query params :**
- `entity` : ID de l'entité (required)

**Response 200 :**
```json
{
  "engine_id": "land-grabbing-rights-engine",
  "entity_id": "cambodia",
  "entity_name": "Cambodge",
  "composite_score": 93.75,
  "severity": "critique",
  "sub_scores": [
    {
      "sub_id": "forced_displacement",
      "sub_name": "Déplacement forcé",
      "score": 95,
      "weight": 0.30,
      "weighted_contribution": 28.5
    }
  ],
  "estimated_index": 9.38,
  "primary_pattern": "Déplacement forcé sans consultation préalable",
  "data_sources": ["Global Witness 2025", "UN Special Rapporteur 2024"],
  "last_updated": "2026-06-21T00:00:00Z"
}
```

---

## Endpoints Alertes

### GET /alerts
Liste les alertes critiques.

**Query params :**
- `acknowledged` : `true` | `false` (défaut: `false`)
- `engine_id` : filtrer par engine
- `limit` : max 100 (défaut: 20)

**Response 200 :**
```json
{
  "alerts": [...],
  "total": 7,
  "unacknowledged": 3
}
```

---

### PATCH /alerts/{alert_id}/acknowledge
Acquitte une alerte.

**Request body :**
```json
{
  "acknowledged_by": "user@company.com"
}
```

**Response 200 :**
```json
{
  "alert_id": "alt_xyz",
  "acknowledged": true,
  "acknowledged_by": "user@company.com",
  "acknowledged_at": "2026-06-21T14:00:00Z"
}
```

---

## Endpoints Rapports

### POST /reports/generate
Génère un rapport PDF ou JSON.

**Request body :**
```json
{
  "engine_ids": ["string"],
  "entity_filter": ["string"],
  "severity_filter": ["string"],
  "format": "pdf",
  "language": "fr",
  "include_sources": true,
  "period": {
    "start": "2026-06-01T00:00:00Z",
    "end": "2026-06-21T23:59:59Z"
  }
}
```

**Response 200 :**
```json
{
  "report_id": "rpt_abc123",
  "download_url": "https://...",
  "generated_at": "2026-06-21T14:30:00Z",
  "page_count": 18,
  "engines_covered": ["string"]
}
```

> Note : Le `download_url` expire après 1 heure.

---

## Codes d'erreur

| Code | Signification |
|---|---|
| 400 | Requête invalide (body malformé, params manquants) |
| 401 | Token manquant ou invalide |
| 403 | Accès non autorisé (tier insuffisant) |
| 404 | Ressource non trouvée |
| 429 | Rate limit dépassé |
| 502 | Erreur upstream (service temporairement indisponible) |

---

## Sécurité API (Pattern interne)

```typescript
// Toujours vérifier SWARM_API_URL avant utilisation
const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn('[API] SWARM_API_URL not configured');
  return NextResponse.json(sealResponse({ error: 'Service unavailable' }), { status: 502 });
}

// Toujours utiliser sealResponse
return NextResponse.json(sealResponse(data), { 
  next: { revalidate: 30 } 
});
```
