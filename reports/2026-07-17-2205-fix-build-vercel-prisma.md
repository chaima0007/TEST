# 2026-07-17-22h05 — [Claude Code / Caelum] — Fix build Vercel (client Prisma)

## SYNOPSIS
Quoi : correction de l'échec de build Vercel de la PR #1. Pourquoi : `next build`
échouait car le client Prisma (gitignoré) était absent du checkout. État : corrigé
(`postinstall: prisma generate`, commit `2332776`), prouvé en local ; sur Vercel les
projets qui correspondent au code (`test`, `test-sa1q`) rebuildent ; confirmation
« vert » en attente.

## Cause racine (confirmée, pas supposée)
`lib/generated/prisma` est gitignoré → absent d'un checkout neuf (Vercel/clone).
`lib/prisma.ts` importe `@/lib/generated/prisma/client` → build échoue :
`Module not found: Can't resolve '@/lib/generated/prisma/client'`.
Preuve : `rm -rf lib/generated/prisma && npm run build` → échec reproduit.

## Correctif
`package.json` : `"postinstall": "prisma generate"`. Vercel exécute `npm install`
→ `postinstall` régénère le client avant `next build`. Bénéficie aussi à tout
clone neuf (reprise par d'autres agents). Indépendant de la cible de déploiement.

## VÉRIFIÉ (preuve — 2026-07-17 22h05 CEST)
- `npm run postinstall` → `✔ Generated Prisma Client (7.8.0)`
- `npm run build` (client absent au départ) → `✓ Compiled successfully · 20/20 pages`
- Sur Vercel : `test` et `test-sa1q` repassés en « Building » sur le commit `2332776`.

## NON VÉRIFIÉ / hors périmètre
- Confirmation « vert » Vercel : EN ATTENTE du rebuild (non affirmé tant que non observé).
- 6 autres projets Vercel (`caelumpartners`, `laloiavecmoi`, `caelum-rh-app`,
  `caelumpartners-app`, `caelumswarm2024`, `caelum-partners-app`) : échouent car
  **liés à ce repo mais attendant un rootDirectory absent de cette branche**
  (ex. `laloiavecmoi/`). MAUVAISE CONFIG COMPTE VERCEL — non corrigeable depuis
  ce dépôt. Action requise côté Chaima : déconnecter ces projets de ce repo.
- Effet de bord : les 8 projets redéploient à chaque push → quota saturé. Ne garder
  qu'1 projet (ou tout déconnecter, Caelum étant sur Cloudflare Pages).

## RESTE
1. Chaima : nettoyer les projets Vercel (déconnecter les 6 mal configurés). 2. Confirmer le vert sur `test`. 3. Merger PR #1.

— L'équipe Caelum Partners · vérité stricte.
