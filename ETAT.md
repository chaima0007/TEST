# ETAT — instantané vivant

> Mis à jour à chaque livraison. Court par design. Détail : `00-LIRE-D-ABORD.md`.
> Rapports horodatés (un par événement) : `reports/`.

**Dernière mise à jour : 2026-07-17 22h05 CEST** (`TZ="Europe/Brussels" date`)

## État vérifié (preuve du 2026-07-17)
- Tests : **33/33 verts** (`npm test`, 7 fichiers) · Lint : **0 erreur** · Types : **0 erreur**
- Build local : **OK** (`npm run build`, 20/20 pages)
- **Correction CI** (commit `2332776`) : `postinstall: prisma generate` — corrige l'échec de build Vercel (client Prisma gitignoré donc absent du checkout). Prouvé par repro : sans le fix `next build` échoue « module not found » ; avec, `postinstall` régénère le client puis le build passe. Sur le nouveau commit, le projet Vercel `test` **rebuild** (plus l'erreur).
- Branche : `claude/nexus-market-agents-63dlku` · PR **#1 ouverte, non mergée**

## Point Vercel (config compte — action Chaima)
**8 projets Vercel** sont branchés sur ce même repo → chaque push déclenche 8 déploiements → saturation du quota (plan gratuit). À nettoyer : ne garder qu'1 projet, ou tout déconnecter (Caelum vise Cloudflare Pages).

## Non vérifié (honnêteté)
- Chemin LLM (Claude) : **codé, jamais exécuté** (pas d'`ANTHROPIC_API_KEY`) — seul le repli heuristique est prouvé.
- Confirmation « vert » du déploiement Vercel : **en attente** du rebuild (je ne l'affirme pas tant que non observé).
- Aucune action réelle client (envoi, signature, encaissement) : volontaire.

## Reste
1. Confirmer le vert Vercel sur `2332776` (ou déconnecter Vercel) / merger PR #1
2. COMMANDANT → HERMES (messages LinkedIn ciblés) · 3. RÉSOLVEUR → surveillance des runs
4. Connecteur de source réel (choix en attente) · 5. `ANTHROPIC_API_KEY` pour vérifier le LLM

## Derniers rapports
- `reports/2026-07-17-2205-fix-build-vercel-prisma.md`
- `reports/2026-07-17-2140-audit-dev-nexus-market.md`
