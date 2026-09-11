# 2026-09-11-13h42 — Claude (agent Caelum) — HERMES branché dans le dashboard

## SYNOPSIS
HERMES ne vivait que dans `lib/` (testé mais non utilisable depuis l'app). Il est
maintenant **branché dans le produit** : une route API sans état et une page dashboard
qui transforme un prospect en 4 brouillons de prospection copiables. Envoi toujours
100 % manuel (§10). Zéro dépendance à Vercel. Poussé sur la branche de dev, jamais sur `main`.

- **Heure réelle (Bruxelles) :** 2026-09-11 13h42 CEST (`TZ=Europe/Brussels date`)
- **Branche :** `claude/nexus-market-agents-63dlku`
- **Commit :** `8391052` (poussé : `407b424..8391052`)

## FAIT
- **Route API** `app/api/hermes/draft/route.ts` — `POST` : valide le prospect (prénom +
  entreprise requis), fusionne une offre optionnelle sur l'offre Caelum par défaut
  (site web premium 500 €), appelle `createHermes().draft()`. **Sans état** : aucune
  écriture en base, aucun envoi.
- **Page** `app/dashboard/prospection/page.tsx` — formulaire prospect (prénom, entreprise,
  secteur, ville, signal) → 4 blocs copiables (note de connexion + variante A/B + 1er
  message + relance), indicateur « rédigé par Claude / heuristique », **bandeau garde-fou
  visible** : HERMES prépare, l'envoi reste manuel.
- **Sidebar** `components/Sidebar.tsx` — nouvelle section « PROSPECTION (CAELUM) ».
- **Tests** `app/api/hermes/draft/__tests__/route.test.ts` — 5 tests : JSON invalide → 400,
  champs requis → 400, génération des 4 brouillons, offre personnalisée (1500 €), prix
  non numérique ignoré (repli 500 €). `vitest.config.ts` couvre désormais `app/**/__tests__`.
- **Codex** : JOURNAL (snapshot §5), EVOLUTION (jalon), A-DECIDER (ligne HERMES resserrée).

## VÉRIFIÉ (preuves)
- `npm test` → **44 tests passés / 44** (9 fichiers) — était 39, +5 route.
- `npm run lint` → **0 erreur**, 3 warnings **préexistants** (fichiers non touchés :
  `app/page.tsx`, `app/pitch/page.tsx`).
- `npx tsc --noEmit` → **0** (après `next build`).
- `npm run build` → **OK** ; `/api/hermes/draft` et `/dashboard/prospection` présents
  dans la table de routes.

## NON VÉRIFIÉ
- **Chemin LLM (Claude)** de HERMES : jamais exécuté (pas d'`ANTHROPIC_API_KEY` fourni).
  Seul le repli **heuristique** est prouvé. La route et l'UI fonctionnent sur l'heuristique.
- **Rendu visuel** de la page dans un navigateur : non ouvert ici ; `next build` valide la
  compilation, pas l'esthétique.
- **Détail Next 16** : `PageProps` est un type global **auto-généré** par `next build`
  (dans `.next/types`). `tsc` seul échoue tant que `.next/types` est absent — artefact
  connu (AGENTS.md), pas un défaut du code.

## RESTE (décisions humaines — §10)
- **Définir l'ICP + fournir 5–10 prospects réels** : l'app est prête ; il manque QUI cibler.
- **`ANTHROPIC_API_KEY`** : pour activer et vérifier le chemin LLM (sinon heuristique).
- **PR #1** : merge = décision humaine.
- **Nettoyage Vercel** : en cours côté Chaima.
