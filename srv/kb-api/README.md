# Caelum KB API — Stub Serveur Flask

Serveur REST sémantique (connexion + FAISS) pour la Knowledge Base Caelum Partners.

## Démarrage rapide

```bash
cd srv/kb-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && nano .env  # configure KB_TOKEN
python3 -m openapi_server
```

## Endpoints

- `GET /v1/kb/search?q=<query>&type=company&limit=5` — recherche sémantique
- `GET /v1/kb/companies/{slug}` — fiche entreprise
- `GET /v1/kb/personas/{slug}` — profil persona
- `GET /v1/kb/health` — health check (sans auth)

## Construction index FAISS

```bash
cd /path/to/repo
python3 tools/kb_index.py build
```

## Swagger UI

http://localhost:8080/v1/ui/
