# ETAT — instantané vivant

> Mis à jour à chaque livraison. Court par design. Détail : `00-LIRE-D-ABORD.md`.
> Rapports horodatés (un par événement) : `reports/`.

**Dernière mise à jour : 2026-09-11 13h53 CEST** (`TZ="Europe/Brussels" date`)

## État vérifié (preuve du 2026-09-11, commit `25dc63c`)
- Tests : **55/55 verts** (`npm test`, 11 fichiers) · Lint : **0 erreur** (3 warnings préexistants) · Types : **0** (`tsc` après `next build`)
- Build local : **OK** (`npm run build`) — inclut `/api/hermes/draft`, `/dashboard/prospection`, `/api/pacte/draft`, `/dashboard/devis`
- **PACTE** (commit `25dc63c`) : rédacteur de devis / closing — route `POST /api/pacte/draft` + page `/dashboard/devis`. Modalités « À CONFIRMER », jamais de paiement en ligne promis (§10/§13). Suite de HERMES.
- **HERMES branché dans l'app** (commit `8391052`) : route `POST /api/hermes/draft` (sans état) + page `/dashboard/prospection` (4 brouillons copiables, envoi manuel §10) + entrée sidebar.
- **Correction CI** (commit `2332776`) : `postinstall: prisma generate` — corrige l'échec de build Vercel (client Prisma gitignoré donc absent du checkout).
- Branche : `claude/nexus-market-agents-63dlku` · PR **#1 ouverte, non mergée**

## Point Vercel (config compte — action Chaima)
**8 projets Vercel** sont branchés sur ce même repo → chaque push déclenche 8 déploiements → saturation du quota (plan gratuit). À nettoyer : ne garder qu'1 projet, ou tout déconnecter (Caelum vise Cloudflare Pages).

## Non vérifié (honnêteté)
- Chemin LLM (Claude) : **codé, jamais exécuté** (pas d'`ANTHROPIC_API_KEY`) — seul le repli heuristique est prouvé.
- Confirmation « vert » du déploiement Vercel : **en attente** du rebuild (je ne l'affirme pas tant que non observé).
- Aucune action réelle client (envoi, signature, encaissement) : volontaire.

## Reste
1. **Définir l'ICP + fournir 5–10 prospects réels** (app prête, il manque QUI cibler)
2. `ANTHROPIC_API_KEY` pour activer/vérifier le chemin LLM de HERMES (sinon heuristique)
3. Nettoyage Vercel (côté Chaima) / merger PR #1
4. Connecteur de source réel pour le pipeline (choix en attente)

## Derniers rapports
- `reports/2026-09-11-1353-agent-pacte-devis.md`
- `reports/2026-09-11-1342-branche-hermes-dashboard.md`
- `reports/2026-07-17-2205-fix-build-vercel-prisma.md`
- `reports/2026-07-17-2140-audit-dev-nexus-market.md`
