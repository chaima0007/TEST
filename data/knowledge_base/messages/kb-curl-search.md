# KB Message — cURL Search Examples

**Type :** Knowledge Base Message  
**Scope :** API Usage Examples  
**Caelum Partners — Internal Dev Reference**

---

## Recherche dans la Knowledge Base

### Recherche basique

```bash
curl -X POST https://caelumpartners.eu/api/kb/search \
  -H "Authorization: Bearer ${CAELUM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "travail forcé cobalt RDC",
    "limit": 10
  }'
```

### Recherche filtrée par engine

```bash
curl -X POST https://caelumpartners.eu/api/kb/search \
  -H "Authorization: Bearer ${CAELUM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "accaparement terres autochtones",
    "engine_filter": ["land-grabbing-rights-engine"],
    "severity_filter": ["critique", "élevé"],
    "limit": 20
  }'
```

### Recherche avec pagination

```bash
curl -X POST https://caelumpartners.eu/api/kb/search \
  -H "Authorization: Bearer ${CAELUM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "biais algorithmique recrutement",
    "limit": 10,
    "offset": 20
  }'
```

---

## Scores d'un Engine

### Score de toutes les entités d'un engine

```bash
curl -X GET "https://caelumpartners.eu/api/engines/land-grabbing-rights-engine/entities" \
  -H "Authorization: Bearer ${CAELUM_API_KEY}"
```

### Score d'une entité spécifique

```bash
curl -X GET "https://caelumpartners.eu/api/engines/land-grabbing-rights-engine/score?entity=cambodia" \
  -H "Authorization: Bearer ${CAELUM_API_KEY}"
```

### Filtrer entités critiques uniquement

```bash
curl -X GET "https://caelumpartners.eu/api/engines/land-grabbing-rights-engine/entities?severity=critique" \
  -H "Authorization: Bearer ${CAELUM_API_KEY}"
```

---

## Alertes Critiques

### Lister toutes les alertes actives

```bash
curl -X GET "https://caelumpartners.eu/api/alerts?acknowledged=false" \
  -H "Authorization: Bearer ${CAELUM_API_KEY}"
```

### Filtrer alertes par engine

```bash
curl -X GET "https://caelumpartners.eu/api/alerts?engine_id=prison-labor-rights-engine&acknowledged=false" \
  -H "Authorization: Bearer ${CAELUM_API_KEY}"
```

### Acquitter une alerte

```bash
curl -X PATCH "https://caelumpartners.eu/api/alerts/{alert_id}/acknowledge" \
  -H "Authorization: Bearer ${CAELUM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"acknowledged_by": "user@company.com"}'
```

---

## Génération de Rapport

### Générer un rapport PDF

```bash
curl -X POST "https://caelumpartners.eu/api/reports/generate" \
  -H "Authorization: Bearer ${CAELUM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "engine_ids": [
      "land-grabbing-rights-engine",
      "prison-labor-rights-engine",
      "digital-gender-gap-rights-engine"
    ],
    "format": "pdf",
    "language": "fr",
    "include_sources": true,
    "period": {
      "start": "2026-06-01T00:00:00Z",
      "end": "2026-06-21T23:59:59Z"
    }
  }'
```

### Réponse attendue

```json
{
  "report_id": "rpt_abc123",
  "download_url": "https://caelumpartners.eu/reports/rpt_abc123.pdf?token=xxx",
  "generated_at": "2026-06-21T14:30:00Z",
  "page_count": 18,
  "engines_covered": [
    "land-grabbing-rights-engine",
    "prison-labor-rights-engine",
    "digital-gender-gap-rights-engine"
  ]
}
```

---

## Variables d'environnement recommandées

```bash
# .env (ne jamais committer)
CAELUM_API_KEY=your_api_key_here
CAELUM_API_BASE=https://caelumpartners.eu/api

# Usage
curl -X GET "${CAELUM_API_BASE}/alerts" \
  -H "Authorization: Bearer ${CAELUM_API_KEY}"
```
