# 2026-09-11-14h45 — Claude (agent Caelum) — Agent RELANCE (relance de devis)

## SYNOPSIS
La boucle de vente s'arrêtait au moment où le devis part. Or c'est là que la plupart
des deals meurent : le prospect se tait, et un fondateur débutant n'ose pas relancer.
**RELANCE** comble ce trou : une séquence courte et espacée (J+3 / J+7 adaptée à
l'objection / J+14 clôture polie) pour relancer un devis sans harceler. Il RÉDIGE ;
Chaima envoie à la main (§10). Zéro dépendance à Vercel.

- **Heure réelle (Bruxelles) :** 2026-09-11 14h45 CEST (`TZ=Europe/Brussels date`)
- **Branche :** `claude/nexus-market-agents-63dlku` · **Commit :** `9df5764` (`a873155..9df5764`)

## FAIT
- **Agent** `lib/agents/relance.ts` — `PendingQuote → FollowUpSequence` (3 messages) :
  J+3 rappel léger, J+7 adapté à l'objection (`price` → réduire le périmètre ; `timing`
  → garder au chaud ; `trust` → montrer sur pièce ; `none` → dispo pour 15 min), J+14
  clôture polie qui rend la main. Heuristique + Claude optionnel (`createRelance()`, repli).
  Réutilise `CAELUM_OFFER` (DRY).
- **Route** `app/api/relance/draft` — `POST` sans état (validation + coercition de
  l'objection), aucune persistance, aucun envoi.
- **Page** `app/dashboard/relance` — formulaire (prospect + objection) → 3 blocs copiables.
- **Registre** : entrée RELANCE (FLEET = 14). **Sidebar** : « Relance » (après Devis).
- **Tests** : `relance.test.ts` (6) + `api/relance/draft/route.test.ts` (4).

## VÉRIFIÉ (preuves)
- `npm test` → **77 / 77** (15 fichiers) — était 67, +10.
- `npm run lint` → **0 erreur** (3 warnings préexistants, fichiers non touchés).
- `npx tsc --noEmit` → **0** (après `next build`).
- `npm run build` → **OK** ; `/api/relance/draft` et `/dashboard/relance` présents.
- Garde-fous testés : aucune fausse urgence (« dernière chance », « offre expire »),
  aucune survente invérifiable, clôture polie présente.

## NON VÉRIFIÉ
- **Chemin LLM (Claude)** de RELANCE : jamais exécuté (pas d'`ANTHROPIC_API_KEY`).
  Seul le repli heuristique est prouvé.
- **Rendu visuel** de `/dashboard/relance` en navigateur : non ouvert.
- **Cadence J+3/J+7/J+14** : choix de départ **PLAUSIBLE**, pas calibré sur des données
  réelles — à ajuster avec l'expérience.

## RESTE (décisions humaines — §10)
- **ICP + liste de prospects** : toujours attendu — alimente HERMES → BOUSSOLE → PACTE → RELANCE.
- **Modalités de facturation** (PACTE) : « À CONFIRMER » (voir A-DECIDER).
- **`ANTHROPIC_API_KEY`** ; **PR #1** merge = décision humaine.

## NOTE — état de la flotte
Boucle de vente Caelum désormais **complète de bout en bout** :
HERMES (prospection) → BOUSSOLE (qualification) → PACTE (devis) → RELANCE (relance).
Prochaine frontière naturelle = l'APRÈS-signature (livraison du site / onboarding client),
mais cela dépend d'un premier « oui » — donc d'un premier prospect. À voir avec Chaima.
