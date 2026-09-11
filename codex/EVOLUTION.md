# /codex/EVOLUTION.md — APPEND-ONLY

> Une section par projet. Uniquement les événements SIGNIFICATIFS (jalon, décision, lancement, problème résolu). Jamais « rien de neuf » (ça, c'est le JOURNAL).

## TEST / Nexus-Market

- **2026-09-11** — Jalon : agent **PACTE** (devis / proposition commerciale, closing) — `lib/agents/pacte.ts` + route `/api/pacte/draft` + page `/dashboard/devis`. Suite de HERMES dans l'entonnoir (prospection → devis). Modalités « À CONFIRMER », jamais de paiement en ligne promis (§10/§13). 55/55 tests, `next build` OK.
- **2026-09-11** — Jalon : **HERMES branché dans l'app** — route `POST /api/hermes/draft` (sans état) + page `/dashboard/prospection` (brouillons copiables, envoi manuel §10) + entrée sidebar. `next build` OK, 44/44 tests. Reste (Chaima) : définir l'ICP + fournir la liste de prospects.
- **2026-09-11** — Jalon : agent **HERMES** (rédacteur de prospection LinkedIn, `lib/agents/hermes.ts`) — brouillons personnalisés pour l'offre 500€, envoi manuel uniquement. 39/39 tests verts.
- **2026-09-06** — PROTOCOLE CODEX (v2026-09-06) installé dans le projet (CLAUDE.md + structure §12 + agents dérivés + skill debat).
- **2026-07-17** — Problème résolu : build Vercel corrigé (`postinstall: prisma generate`) ; `test` déployé (Ready).
- **2026-07-17** — Jalon : agents premium COMMANDANT + RÉSOLVEUR ajoutés à la flotte Caelum (registre `lib/agents/`).
- **2026-06-18** — Jalon : pipeline Nexus-Market V1 (state machine 5 étapes) + agents Conseiller/Simulateur/Rédacteur/Négociateur/Auto-pilote ; PR #1 ouverte.
