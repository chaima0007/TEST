# /codex/EVOLUTION.md — APPEND-ONLY

> Une section par projet. Uniquement les événements SIGNIFICATIFS (jalon, décision, lancement, problème résolu). Jamais « rien de neuf » (ça, c'est le JOURNAL).

## TEST / Nexus-Market

- **2026-09-11** — Décision appliquée : **`.claude/agents/` réconcilié avec le set canonique** de l'Empire (21 ébauches de 11-12 lignes → 21 agents complets alignés sur `keywordmoneymaker`, socle commun identique, empreinte vérifiée). Referme la ligne A-DECIDER du 2026-09-06. TRANCHÉ PAR CHAIMA.
- **2026-09-11** — Décision : conflit de gouvernance PR #1 ↔ PR #8 (`main` = install CODEX « CompeteIQ ») tranché **Nexus-Market prioritaire** ; décisions de `main` intégrées, EVOLUTION en union. TRANCHÉ PAR CHAIMA.
- **2026-09-11** — Problème résolu : **PR #1 remise mergeable** (conflit avec `main` après l'atterrissage de PR #2 `cbe82e0` = CI + mêmes correctifs lint). Merge de `main` dans la branche, 3 conflits résolus en union (`package.json`, `seed.ts`, `settings/page.tsx`), gate vert (77/77, lint 0, tsc 0, build OK). `dirty` → `unstable`. Merge dans `main` = décision humaine.
- **2026-09-11** — Jalon : agent **RELANCE** (relance de devis, suivi post-proposition) — `lib/agents/relance.ts` + route `/api/relance/draft` + page `/dashboard/relance`. Referme la boucle après PACTE (J+3/J+7/clôture, sans harcèlement). 77/77 tests, `next build` OK. Boucle de vente Caelum complète : prospection → qualification → devis → relance.
- **2026-09-11** — Jalon : agent **BOUSSOLE** (qualification / triage de leads) — `lib/agents/boussole.ts` + route `/api/boussole/qualify` + page `/dashboard/qualification`. Maillon manquant entre HERMES et PACTE. 100 % déterministe (aucun LLM), score de règles transparent (§10/§13). 67/67 tests, `next build` OK. Entonnoir Caelum complet : prospection → qualification → devis.
- **2026-09-11** — Jalon : agent **PACTE** (devis / proposition commerciale, closing) — `lib/agents/pacte.ts` + route `/api/pacte/draft` + page `/dashboard/devis`. Suite de HERMES dans l'entonnoir (prospection → devis). Modalités « À CONFIRMER », jamais de paiement en ligne promis (§10/§13). 55/55 tests, `next build` OK.
- **2026-09-11** — Jalon : **HERMES branché dans l'app** — route `POST /api/hermes/draft` (sans état) + page `/dashboard/prospection` (brouillons copiables, envoi manuel §10) + entrée sidebar. `next build` OK, 44/44 tests. Reste (Chaima) : définir l'ICP + fournir la liste de prospects.
- **2026-09-11** — Jalon : agent **HERMES** (rédacteur de prospection LinkedIn, `lib/agents/hermes.ts`) — brouillons personnalisés pour l'offre 500€, envoi manuel uniquement. 39/39 tests verts.
- **2026-09-06** — PROTOCOLE CODEX (v2026-09-06) installé dans le projet (CLAUDE.md + structure §12 + agents dérivés + skill debat).
- **2026-07-17** — Problème résolu : build Vercel corrigé (`postinstall: prisma generate`) ; `test` déployé (Ready).
- **2026-07-17** — Jalon : agents premium COMMANDANT + RÉSOLVEUR ajoutés à la flotte Caelum (registre `lib/agents/`).
- **2026-06-18** — Jalon : pipeline Nexus-Market V1 (state machine 5 étapes) + agents Conseiller/Simulateur/Rédacteur/Négociateur/Auto-pilote ; PR #1 ouverte.

## CompeteIQ (dépôt chaima0007/test)

> Section intégrée depuis `main` (PR #8). Événements côté produit CompeteIQ.

- 2026-06-19 — Revue de code automatisée installée : CI (lint/build/typecheck) + revue Claude sur PR ; 5 erreurs de lint corrigées ; PR #2 mergée.
- 2026-07-17 — Landing CompeteIQ (dans keywordmoneymaker) passée en « en développement — non disponible » (produit EN PAUSE).
- 2026-09-11 — PROTOCOLE CODEX installé côté `main` (bloc CLAUDE.md + structure /codex + skill debat). Agents non créés (décision transverse parquée).
