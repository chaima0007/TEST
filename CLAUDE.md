@AGENTS.md

# Guide de collaboration — Caelum Partners

## Règles générales
- Ne modifie pas le repo sans validation explicite pour les changements architecturaux.
- Pour les patterns établis (engines, routes, sidebar) : construire en continu sur la branche dédiée.
- Valider chaque engine avec `python3 engine.py` avant tout commit.
- Lire un fichier avant de l'écraser (toujours).

## Branche de travail
`claude/swarm-50-agent-architecture-3l6cno`

## Nommage des branches feature
```
feat/wave-<N>-<slug-court>
```
Exemples : `feat/wave-58-gender-indigenous-arms`, `feat/wave-59-climate-migration`

## Template PR — Conventional Commits

**Titre :** `feat(wave-N): domaine1, domaine2 & domaine3 engines`

**Corps :**
```
## Engines
- engine1_name (avg X.XX) — description courte du domaine
- engine2_name (avg X.XX) — description courte du domaine
- engine3_name (avg X.XX) — description courte du domaine

## Sécurité
✓ sealResponse · ✓ SWARM_API_URL guard · ✓ 502 fallback · ✓ revalidate:30

## Tests
python3 engine1.py ✓ / python3 engine2.py ✓ / python3 engine3.py ✓
```

## Pattern engine Python (standard Wave)
- 8 entités, distribution OBLIGATOIRE : 4 critique / 2 élevé / 1 modéré / 1 faible
- Poids : sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20
- Seuils : critique ≥60, élevé ≥40, modéré ≥20, faible <20
- `estimated_{domain}_index = round(composite_score / 100 * 10, 2)`

## Pattern sécurité API route
- `SWARM_API_URL` guard + `console.warn` en tête de fichier
- `sealResponse` sur tous les `NextResponse.json()`
- `next: { revalidate: 30 }` sur fetch upstream
- Fallback `status: 502` sur échec upstream (jamais 503)
- Zéro credentials dans le code

## Simulation — Règle permanente
**Toujours simuler pour choisir la meilleure solution** avant toute décision non triviale.

Exemples de situations qui déclenchent une simulation comparative :
- Choix entre deux approches techniques ou organisationnelles
- Sélection des 3 domaines pour une nouvelle wave
- Paramètres SaaS / business model
- Architecture, nommage, design système

Format de simulation :
- Présenter ≥2 options avec critères explicites et scoring
- Déclarer le gagnant avec justification
- Pour les simulations numériques : paramètres exacts, sortie complète, version script
