# 2026-09-11-14h33 — Claude (agent Caelum) — Agent BOUSSOLE (qualification)

## SYNOPSIS
L'entonnoir avait un trou : HERMES obtient une réponse, puis PACTE rédige un devis —
mais rien ne disait *si ce lead vaut le temps de Chaima* ni *quoi lui demander avant*.
**BOUSSOLE** comble ce maillon : qualification / triage déterministe d'un lead →
fit + score justifié + questions de découverte + prochaine action recommandée. Il
recommande, Chaima décide (§10). Zéro dépendance à Vercel.

- **Heure réelle (Bruxelles) :** 2026-09-11 14h33 CEST (`TZ=Europe/Brussels date`)
- **Branche :** `claude/nexus-market-agents-63dlku` · **Commit :** `05c7666` (`337dc27..05c7666`)

## FAIT
- **Agent** `lib/agents/boussole.ts` — `qualify(Lead) → Qualification` : score entier
  borné (max 8) issu de règles explicites (besoin clair +2, signal budget +2, échéance
  immédiate/proche +2/+1, décideur +1, site absent/daté +1) → `fit`
  (ÉLEVÉE/MODÉRÉE/FAIBLE), `priority`, `reasons` (chaque point justifié), `questions`
  ciblées sur les manques, `recommendation`. Dérive les signaux manquants du texte
  libre du prospect (mots-clés).
- **Route** `app/api/boussole/qualify` — `POST` (validation + coercition des champs),
  aucune persistance.
- **Page** `app/dashboard/qualification` — formulaire (drapeaux + message libre) →
  bandeau fit/score + « pourquoi ce score » + questions + recommandation.
- **Registre** : entrée BOUSSOLE (FLEET = 13). **Sidebar** : « Qualification » (entre
  Prospection et Devis).
- **Tests** : `boussole.test.ts` (8) + `api/boussole/qualify/route.test.ts` (4).

## VÉRIFIÉ (preuves)
- `npm test` → **67 / 67** (13 fichiers) — était 55, +12.
- `npm run lint` → **0 erreur** (3 warnings préexistants, fichiers non touchés).
- `npx tsc --noEmit` → **0** (après `next build`).
- `npm run build` → **OK** ; `/api/boussole/qualify` et `/dashboard/qualification` présents.
- **Choix de conception protocolaire** : 100 % déterministe, **aucun LLM**. La
  qualification est un score de règles transparent et auditable — pas d'intuition
  boîte-noire, pas de pourcentage (§13), pas de certitude inventée (§10). Conséquence :
  **aucun chemin NON VÉRIFIÉ** dans cet agent (tout est prouvé par les tests).
- **Test adverse utile** : la question « enveloppe budgétaire » (avec « é ») ne
  matchait pas la regex `/budget/` du test → question reformulée « un budget ». Le test
  qui échoue avant le correctif a fait son travail (§8 Parcours 4).

## NON VÉRIFIÉ
- **Rendu visuel** de `/dashboard/qualification` en navigateur : non ouvert ; `next
  build` valide la compilation, pas l'esthétique.
- Les **seuils de score** (6 = ÉLEVÉE, 3 = MODÉRÉE) sont un choix de départ **PLAUSIBLE**,
  non calibré sur des données réelles — à ajuster quand de vrais leads seront passés.

## RESTE (décisions humaines — §10)
- **ICP + liste de prospects** : annoncée par Chaima ; alimentera HERMES → BOUSSOLE → PACTE.
- **Calibrer les seuils de BOUSSOLE** une fois quelques leads réels qualifiés.
- **Modalités de facturation** (PACTE) : toujours « À CONFIRMER » (voir A-DECIDER).
- **`ANTHROPIC_API_KEY`** (HERMES/PACTE) ; **PR #1** merge = décision humaine.
