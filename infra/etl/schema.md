# ETL Schema — Caelum KB

## Sources supportées
| Source | Format | Fréquence | Script |
|--------|--------|-----------|--------|
| Manuel | JSON | À la demande | `infra/etl/ingest.py --source manual` |
| EcoVadis export | JSON/CSV | Mensuel | `infra/etl/ingest.py --source ecovadis` |
| MSCI ESG export | JSON | Trimestriel | `infra/etl/ingest.py --source msci` |
| News crawl | JSONL | Hebdomadaire | `infra/etl/news_crawler.py` (config only) |

## Provenance tracking
Chaque fichier KB inclut `_meta.ingested_from` et `_meta.ingested_at`.

## PII policy
- Aucun nom de personne physique dans les fichiers KB
- Uniquement titres (CCO, VP Sustainability) et entreprises
- Contacts commerciaux -> CRM uniquement (hors repo)
