# Vector Store — Recommandations

## Option retenue : FAISS local (dev) → Weaviate (prod)

### FAISS (développement / offline)
- Lib Python pure, zéro infra
- `pip install faiss-cpu sentence-transformers`
- Script : `python3 tools/kb_index.py build`
- Limite : pas de mise à jour incrémentale, rebuild complet nécessaire

### Weaviate (production recommandée)
- Self-hosted via Docker ou Weaviate Cloud
- Mise à jour incrémentale, filtres hybrides (BM25 + vecteurs)
- Config minimale : `infra/vector/weaviate-docker-compose.yml`
- Coût cloud : ~50€/mois (10M vecteurs)

### Pinecone (alternative SaaS)
- Zéro infra, latence <100ms
- Coût : ~70€/mois (1M vecteurs, 1M requêtes)
- Intégration : `pip install pinecone-client`

## Choix recommandé
- Dev/staging : FAISS local via `tools/kb_index.py`
- Prod (>1000 docs) : Weaviate self-hosted (Docker)
- Prod (scale >100K requêtes/mois) : Pinecone

## Weaviate docker-compose minimal
```yaml
# infra/vector/weaviate-docker-compose.yml
version: "3.9"
services:
  weaviate:
    image: semitechnologies/weaviate:1.24.0
    ports: ["8080:8080"]
    environment:
      QUERY_DEFAULTS_LIMIT: "20"
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: "false"
      PERSISTENCE_DATA_PATH: "/var/lib/weaviate"
      DEFAULT_VECTORIZER_MODULE: "text2vec-transformers"
      ENABLE_MODULES: "text2vec-transformers"
    volumes:
      - weaviate_data:/var/lib/weaviate
volumes:
  weaviate_data:
```
