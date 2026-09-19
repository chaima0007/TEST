# /codex/EVOLUTION.md — APPEND-ONLY

> Une section par projet. Uniquement les événements SIGNIFICATIFS (jalon, décision, lancement, problème résolu). Jamais « rien de neuf » (ça, c'est le JOURNAL).

## TEST / Nexus-Market

- **2026-09-19** — Décision prise : **les 21 rôles de `.claude/agents/` passent au set canonique de l'Empire** (PR #9). Lève une contradiction entre deux décisions opposées du 2026-09-11 ; celle du « laisser en l'état » est supersédée. Aucun agent ajouté ni supprimé ; les 6 experts de domaine du 16/09 sont conservés. **TRANCHÉ PAR CHAIMA.**

- **2026-09-19** — Décision prise : **numérotation de `🔴 ERREURS.md` par horodatage** (`ERR-AAAAMMJJ-HHMM`), sans renommer `ERR-001` à `ERR-021`. Motif : une même entrée renumérotée quatre fois en une soirée, deux sessions écrivant en parallèle dans le registre. **TRANCHÉ PAR CHAIMA.**
- **2026-09-19** — Problème cerné (non résolu) : l'accès en écriture des Routines programmées est une **limite d'organisation**, pas un réglage — `create_trigger` refuse le paramètre `connectors` (re-mesuré ce jour). Recette de test d'interface déposée dans `/codex/routines-acces-ecriture.md`. ERR-020 reste **NON CLOSE**.

- **2026-09-16** — Jalon : **6 agents ajoutés** — `expert-nextjs`, `expert-donnees-prisma`, `expert-authentification`, `expert-cicd-deploiement`, `expert-llm-agents`, `orchestrateur`. Les 21 rôles du §1 sont des rôles de **gouvernance** ; aucun ne possédait un domaine **technique**, alors que 5 des erreurs consignées relèvent de la CI/déploiement. Quatre agents **délibérément non créés** au titre du §9 anti-bloat (doublons de `testeur-adverse`, `scribe-empire`, `gardien-donnees`, `sentinel-securite`). TRANCHÉ PAR CHAIMA.

- **2026-09-16** — Jalon : **carte vivante créée** (`codex/CARTOGRAPHIE.md`). Diagnostic mesuré : `main` figé depuis le 14/09, 6 PR ouvertes, 38 refs distantes — le goulot est le §10 (merger est humain), pas la technique. Deux écarts de tenue relevés : les 4 dossiers `/codex/` sont vides (boucle §4 jamais démarrée) et 7 obstacles d'exploitation sur 8 étaient introuvables depuis le registre (corrigé par ERR-021, en index).
- **2026-09-14** — Décision : **réunion de décision tenue (7 agents CODEX, Parcours 2)** sur la zone de prospection. Résultat : question **écartée**, la zone se constate après inventaire du réseau 1er degré. Deux lignes A-DECIDER ouvertes au passage (conformité RGPD de la prospection ; bornage écrit de l'offre à 500 €). Le vérificateur-vérité a amendé l'arbitrage sur 4 points avant sortie. TRANCHÉ PAR CHAIMA.
- **2026-09-14** — Décision : **ICP de Caelum arrêté — consultants / coachs indépendants**. Contrainte de canal identifiée : HERMES prospecte sur LinkedIn, donc l'ICP doit y être actif ; les exemples du code (restaurants, kinés) ne le sont pas. Débloque à moitié la ligne A-DECIDER ; reste la liste de prospects. TRANCHÉ PAR CHAIMA.
- **2026-09-11** — Décision : `.claude/agents/` **laissé en l'état** (set dérivé du §1 conservé, pas de remplacement par un set canonique). Prémisse d'origine erronée, décision reconfirmée après correction. Ligne sortie de A-DECIDER. TRANCHÉ PAR CHAIMA.
- **2026-09-11** — Décision : **revue automatique des PR désactivée** tant que `ANTHROPIC_API_KEY` n'est pas posé. Le check finissait en `failure` sur chaque PR, commits documentaires compris (ERR-010) ; ERR-010 laissait le choix « poser le secret OU rendre le workflow non bloquant » — c'est la seconde option, temporaire. La CI lint/build/typecheck (`ci.yml`) reste active et inchangée. TRANCHÉ PAR CHAIMA.
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

- 2026-09-19 — **Trois agents de garantie créés** : `valideur` (la prémisse tient-elle ? née d'ERR-012/013/019 et `ERR-20260914-1956`), `essayeur` (exécuter plutôt que raisonner ; ERR-008/014/016), `confirmateur` (est-ce **en vigueur** là où ça tourne ? `ERR-20260914-2033`, `ERR-20260916-1413`). Ils comblent le seul trou que les 27 rôles existants laissaient : personne ne vérifiait qu'un correctif **tourne**. Contrainte mesurée le jour même : un agent écrit pendant une session n'y est pas utilisable (registre figé au démarrage — `Agent type 'valideur' not found`).
- 2026-09-19 — **`scripts/audit-codex.sh`** : le rituel §5 exécutable en ~5 s, 7 contrôles. Premier passage : `A-DECIDER.md` n'était pas trié selon le §6 (corrigé), et « Merger la PR #1 » dormait depuis **93 jours** alors que la décision était prise depuis le 14/09 (close, preuve `9cc15c2f`). Le script a aussi trouvé un défaut **dans lui-même** — faux positif de doublon sur la nouvelle convention d'ID — corrigé en l'exécutant.
- 2026-09-19 — **Deux cartographies fusionnées.** Deux sessions qui ne se voyaient pas en avaient écrit une chacune (16 et 19 septembre). Fusion sans écrasement : sections 1-6 de la version de `main`, 7-11 de l'autre.

## CompeteIQ (dépôt chaima0007/test)

> Section intégrée depuis `main` (PR #8). Événements côté produit CompeteIQ.

- 2026-06-19 — Revue de code automatisée installée : CI (lint/build/typecheck) + revue Claude sur PR ; 5 erreurs de lint corrigées ; PR #2 mergée.
- 2026-07-17 — Landing CompeteIQ (dans keywordmoneymaker) passée en « en développement — non disponible » (produit EN PAUSE).
- 2026-09-11 — PROTOCOLE CODEX installé côté `main` (bloc CLAUDE.md + structure /codex + skill debat). Agents non créés (décision transverse parquée).
