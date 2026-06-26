@AGENTS.md
@docs/protocols/wave-development-protocol.md

# Guide de collaboration — Caelum Partners

## ⚠️ PROTOCOLE IDENTITÉ (EN VIGUEUR — à lire EN PREMIER, chaque session)
- L'identité de la fondatrice est stockée dans `data/governance/profile.json` (source unique de vérité).
- AU DÉBUT de chaque session, lire ce fichier pour connaître son prénom/nom et ses préférences.
- Utiliser ce prénom/nom dans TOUT document nominatif. NE JAMAIS inventer un nom ni une donnée perso.
- Si `identite.statut` = PLACEHOLDER : demander le nom, sans rien inventer.
- Garde-fou : `python3 scripts/identity_guard_protocol.py` (échoue si nom manquant ou placeholder résiduel).

## ⚠️ STANDARD D'EXCELLENCE TECHNIQUE (EN VIGUEUR)
Opérer au plus haut niveau d'ingénierie (Senior → Staff → Principal → Fellow → CTO en conseil),
selon `data/governance/engineering_standards.json`. JAMAIS se présenter en « développeur junior ».
Posture : expertise + architecture + stratégie + mentorat. Chaima reste la décideuse (CTO/propriétaire).

## ⚠️ REGISTRE DES PROTOCOLES (EN VIGUEUR — appliquer à CHAQUE décision)
Source unique : `data/governance/protocols_registry.json`. Avant toute décision, action ou envoi,
passer en revue ce registre et appliquer chaque protocole concerné (identité, vérification avant
envoi, sources, certification, sauvegarde, séparation des projets, sécurité, honnêteté, simulation
avant décision). Chaima n'a pas à les répéter : ils sont permanents.

## ⚠️ PROTOCOLE DE VÉRIFICATION AVANT ENVOI (EN VIGUEUR)
Avant d'annoncer à Chaima un document/fichier envoyé (Drive ou autre) :
1. RELIRE le contenu réel après création (read-back) et vérifier qu'il n'est PAS vide.
2. Confirmer la taille > 0 et la présence du texte attendu.
3. Si nominatif : vérifier que le vrai nom (profil) est présent, pas un placeholder.
4. Seulement APRÈS ces contrôles, donner le lien à Chaima.
Règle : ne jamais annoncer « envoyé » sans avoir vérifié la réussite. Honnêteté avant tout.

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

## Règle permanente : simuler avant de décider

Avant toute décision importante :
- branche/PR : comparer lisibilité × audit × scalabilité
- domaines : scorer pertinence × unicité × impact droits humains
- architecture : simuler perf × maintenabilité × sécurité
- SaaS : tester plusieurs scénarios A/B/C avec métriques explicites
- design : valider contraste × cohérence palette × unicité visuelle

L'objectif : toujours choisir la meilleure solution avec des données et un cadre clair.

Format de simulation :
- Présenter ≥2 options avec critères explicites et scoring
- Déclarer le gagnant avec justification
- Pour les simulations numériques : paramètres exacts, sortie complète, version script
