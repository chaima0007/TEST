# Tests E2E — Caelum Partners

## Structure

```
tests/e2e/
├── README.md                   # Ce fichier
└── test_engine_smoke.py        # Smoke tests Python pour tous les engines
```

## Smoke Tests

Les smoke tests vérifient que chaque engine Python :
1. Produit exactement **8 entités** dans le output
2. Retourne un `avg_composite` > 0
3. Contient au moins une entité classifiée `"critique"` dans la distribution de risque

### Lancer les smoke tests (mode offline — pour CI)

```bash
python3 tests/e2e/test_engine_smoke.py --offline
```

Le mode `--offline` importe et exécute directement les engines Python sans serveur Next.js.

### Lancer les smoke tests (mode HTTP — avec serveur local)

```bash
TEST_BASE_URL=http://localhost:3000 python3 tests/e2e/test_engine_smoke.py
```

En mode HTTP, le script appelle chaque route `/api/<engine-slug>` et valide la réponse JSON.

## Load Tests

```bash
# Usage: ./tools/load_test.sh [BASE_URL] [CONCURRENCY] [REQUESTS]
./tools/load_test.sh http://localhost:3000 10 100
```

Requires `apache2-utils` for `ab` (Apache Bench). Falls back to parallel `curl` loops if `ab` is not installed.

```bash
# Install ab on Ubuntu/Debian
sudo apt-get install apache2-utils

# Install ab on macOS
brew install httpd
```

## Engines Testés

| Engine | Module Python | Route API |
|---|---|---|
| Digital Gender Gap Rights | `digital_gender_gap_rights.py` | `/api/digital-gender-gap-rights-engine` |
| Unpaid Care Work Rights | `unpaid_care_work_rights.py` | `/api/unpaid-care-work-rights-engine` |
| Youth Justice Rights | `youth_justice_rights.py` | `/api/youth-justice-rights-engine` |
| Land Grabbing Rights | `land_grabbing_rights.py` | `/api/land-grabbing-rights-engine` |
| Prison Labor Rights | `prison_labor_rights.py` | `/api/prison-labor-rights-engine` |
| Statelessness Rights | `statelessness_rights.py` | `/api/statelessness-rights-engine` |
| Algorithmic Bias Rights | `algorithmic_bias_rights.py` | `/api/algorithmic-bias-rights-engine` |
| Hate Speech Platform Rights | `hate_speech_platform_rights.py` | `/api/hate-speech-platform-rights-engine` |

## Ajouter un Nouvel Engine

1. Ajouter son nom dans la liste `ENGINES` dans `test_engine_smoke.py`
2. S'assurer que le module Python est dans `swarm/intelligence/`
3. Vérifier que la route API suit le pattern `/api/<slug>-engine`
