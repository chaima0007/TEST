# KB Message : openapi-generator-cli

**Date :** 2026-06-21 | **Owner :** Chaima | **Statut :** Implémenté (stub manuel)

## Commande originale
`openapi-generator-cli generate -i data/knowledge_base/openapi.yml -g python-flask -o srv/kb-api`

## Résultat
Docker daemon non disponible → Flask stub écrit manuellement dans `srv/kb-api/` (branche `feat/kb-api-stub`, PR #4).

## Next Steps
- [ ] `cd srv/kb-api && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python3 -m openapi_server`
- [ ] Tester : `./tools/kb_query.sh`
