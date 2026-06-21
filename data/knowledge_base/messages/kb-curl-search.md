# KB Message : Exemples curl

**Date :** 2026-06-21 | **Owner :** Chaima | **Statut :** Documenté dans `tools/kb_query.sh`

## Commandes
```bash
curl -s -H "Authorization: Bearer $TOKEN" "https://kb.caelumpartners.eu/v1/kb/search?q=compliance+officer&limit=5"
curl -sS -H "Authorization: Bearer $KB_TOKEN" "https://kb.caelumpartners.eu/v1/kb/search?q=CCO%20automobile%20LkSG&type=company&limit=3"
```

## Usage local
`KB_TOKEN=xxx KB_BASE=http://localhost:8080/v1 ./tools/kb_query.sh`
