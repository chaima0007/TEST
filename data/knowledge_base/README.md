# Caelum Partners — Knowledge Base

Base de connaissances centralisée pour les agents commerciaux et techniques.

## Structure
- `companies/` — 20 fiches entreprises JSON (cibles prioritaires Europe)
- `personas/` — 10 profils d'interlocuteurs MD
- `playbooks/` — 5 guides de vente / post-pilote
- `templates/` — Emails, decks, accords
- `sources/` — Configs crawlers (aucune exécution automatique)
- `index/` — Index FAISS pré-calculé (généré par `tools/kb_index.py`)
- `meta.json` — Métadonnées et index global

## Usage agent
```bash
python3 tools/kb_index.py search "CCO automobile LkSG"
cat data/knowledge_base/companies/volkswagen.json | python3 -m json.tool
```

## Mise à jour
1. Modifier/ajouter un fichier dans `companies/` ou `personas/`
2. Mettre à jour `last_updated` dans le fichier
3. Ouvrir une PR avec titre `chore(kb): update <nom>` 
4. Regénérer l'index : `python3 tools/kb_index.py build`

## Gouvernance
- Owner : chaima@caelumpartners.eu
- Review requis : 1 approbation avant merge
- Retention : fiches >180j sans mise à jour → alerte automatique
- PII : aucune donnée personnelle (noms propres de contacts) dans ce repo
