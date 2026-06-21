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
