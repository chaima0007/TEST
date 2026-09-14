# ETAT — instantané vivant

> Mis à jour à chaque livraison. Court par design. Détail : `00-LIRE-D-ABORD.md`.
> Rapports horodatés (un par événement) : `reports/`.

**Dernière mise à jour : 2026-09-14 21h30 CEST** (`TZ="Europe/Brussels" date`)

> **PR #1 : MERGÉE** dans `main` (commit de merge `9cc15c2f`, « Merge PR #1 — Nexus-Market : pipeline de matching + flotte d'agents Caelum »). La branche `claude/nexus-market-agents-63dlku` n'est plus la branche de travail. **Toute nouvelle branche part de `main`.**

> **`main` = `0c792ca3`** au 2026-09-14 21h30 CEST (vérifié par `git ls-remote`, pas de mémoire).

## État vérifié (preuve du 2026-09-11, commit `064e144`, merge de `main`)
- Tests : **77/77 verts** (`npm test`, 15 fichiers) · Lint : **0 erreur** (3 warnings préexistants) · Types : **0** (`tsc` après `next build`)
- Build local : **OK** (`npm run build`) — inclut prospection/qualification/devis/relance + leurs routes API
- **Boucle de vente Caelum complète** : HERMES (prospection) → BOUSSOLE (qualification) → PACTE (devis) → RELANCE (relance).
- **RELANCE** (commit `9df5764`) : relance de devis — route `POST /api/relance/draft` + page `/dashboard/relance`. Séquence J+3/J+7/clôture, sans fausse urgence ni remise inventée (§13). Envoi manuel (§10).
- **BOUSSOLE** (commit `05c7666`) : qualification / triage de leads — route `POST /api/boussole/qualify` + page `/dashboard/qualification`. 100 % déterministe (aucun LLM), score transparent, pas de pourcentage (§10/§13). Recommande, ne décide pas.
- **PACTE** (commit `25dc63c`) : rédacteur de devis / closing — route `POST /api/pacte/draft` + page `/dashboard/devis`. Modalités « À CONFIRMER », jamais de paiement en ligne promis (§10/§13).
- **HERMES branché dans l'app** (commit `8391052`) : route `POST /api/hermes/draft` (sans état) + page `/dashboard/prospection` (4 brouillons copiables, envoi manuel §10) + entrée sidebar.
- **Correction CI** (commit `2332776`) : `postinstall: prisma generate` — corrige l'échec de build Vercel (client Prisma gitignoré donc absent du checkout).
- Branche : `claude/nexus-market-agents-63dlku` · PR **#1 MERGÉE le 2026-09-11** (`9cc15c2f`). Les chiffres de tests ci-dessus datent du commit `064e144` et **n'ont pas été re-exécutés depuis** : fait rapporté, non reconstaté.

## Point Vercel (config compte — action Chaima)
**8 projets Vercel** sont branchés sur ce même repo → chaque push déclenche 8 déploiements → saturation du quota (plan gratuit). À nettoyer : ne garder qu'1 projet, ou tout déconnecter (Caelum vise Cloudflare Pages).

## Décidé depuis (2026-09-14)
- **ICP Caelum tranché** : consultants / coachs indépendants (seul segment réellement actif sur LinkedIn, canal de HERMES).
- **Zone géographique : question écartée**, non arbitrée — sans scraping le bassin est le réseau existant, la zone se constate après inventaire. Réunion de décision à 7 agents, consignée dans `A-DECIDER.md`.
- **Revue auto des PR désactivée** : `claude-code-review` en `workflow_dispatch` seul tant que `ANTHROPIC_API_KEY` n'est pas posée (ERR-010 close). La CI `ci.yml` reste active et inchangée.
- **Offre à 500 € jugée non défendable en l'état** : « premium », « sur-mesure », « rapide », « inclus » sont non bornés. Squelette de périmètre écrit dans `reports/2026-09-14-2115-preparation-prospection.md`, 7 points `À DÉCIDER`.

## Non vérifié (honnêteté)
- Chemin LLM (Claude) : **codé, jamais exécuté** (pas d'`ANTHROPIC_API_KEY`) — seul le repli heuristique est prouvé.
- Tests `77/77` : datent du 2026-09-11 (`064e144`), non re-exécutés au 2026-09-14.
- Registre de traitement RGPD (art. 30) : **probablement dû**, l'exemption « <250 salariés » tombe si le traitement n'est pas occasionnel. Demande un avis professionnel.
- Confirmation « vert » du déploiement Vercel : **en attente** du rebuild (je ne l'affirme pas tant que non observé).
- Aucune action réelle client (envoi, signature, encaissement) : volontaire.

## Reste
1. **Définir l'ICP + fournir 5–10 prospects réels** (app prête, il manque QUI cibler)
2. `ANTHROPIC_API_KEY` pour activer/vérifier le chemin LLM de HERMES (sinon heuristique)
3. Nettoyage Vercel (côté Chaima) / merger PR #1
4. Connecteur de source réel pour le pipeline (choix en attente)

## Derniers rapports
- `reports/2026-09-11-1445-agent-relance-devis.md`
- `reports/2026-09-11-1433-agent-boussole-qualification.md`
- `reports/2026-09-11-1353-agent-pacte-devis.md`
- `reports/2026-09-11-1342-branche-hermes-dashboard.md`
- `reports/2026-07-17-2205-fix-build-vercel-prisma.md`
- `reports/2026-07-17-2140-audit-dev-nexus-market.md`
