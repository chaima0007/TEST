# CARTE DES PROJETS — les 38 branches de `chaima0007/test`

> **Demande de Chaima (2026-09-16) :** *« qu'il surveille mes projets en cours sans les supprimer
> ni entraver les agents qui créent. »*
> **Lecture seule. Aucune branche n'a été touchée.** Établi par `git ls-remote` + `git log` le
> **2026-09-19**. À rafraîchir à chaque rafale — c'est la première chose à regarder en reprise.
>
> **Un seul fichier vivant, réécrit à chaque relevé** (R-007). Le relevé précédent n'est pas
> conservé ici : l'historique git le garde.

## Comment lire

| Colonne | Signification |
|---|---|
| **État** | 🟢 activité ≤ 10 jours · 🟡 11-45 jours · ⚫ > 45 jours |
| **Écart à `main`** | nombre de commits que `main` n'a pas. ✅ ≤ 2 = travail **posé sur main** · 🔧 3-30 = en cours · 🌌 > 30 = **univers séparé** (autre projet, jamais intégré) |

**Correction à l'audit du 2026-09-14** qui disait « aucune branche mergée » : c'est trop fort.
**5 branches sont posées sur `main`** (≤ 2 commits d'écart) — leur travail y est. Ce qui est
vrai : **les univers séparés ne le seront jamais**, et ce n'est pas un défaut, c'est qu'ils
n'ont rien à faire dans ce dépôt (ligne A-DECIDER du 2026-09-14).


## 🟢 VIVANT — 15 branches

| Dernière activité | Branche | Projet | Écart à `main` | Dernier commit |
|---|---|---|---|---|
| 2026-09-19 (0 j) | `claude/nifty-shannon-u87dv8` | ATLAS (cette branche) | 🔧 en cours (18) | feat(atlas): recoupement inter-sessions — l ordre des decisions prime sur la v |
| 2026-09-19 (0 j) | `claude/charming-galileo-cqhkn1` | Caelum — capitaux & statut (CV lu le 19/09) | 🔧 en cours (6) | docs(a-decider): deux corrections majeures — Chaima est a Bruxelles, et le dip |
| 2026-09-16 (3 j) | `main` | Nexus-Market / Caelum (tronc) | ✅ posée sur main (0) | feat(agents): 5 experts de domaine + 1 orchestrateur |
| 2026-09-16 (3 j) | `codex/err-019-branche-perimee` | Caelum — correctif ERR-019 | 🔧 en cours (10) | Merge remote-tracking branch 'origin/main' into codex/err-019-branche-perimee |
| 2026-09-16 (3 j) | `claude/wizardly-franklin-7gehzh` | Caelum — session parallèle | ✅ posée sur main (1) | reports: heures réelles mesurées sur l'historique Git (Caelum + La Loi Avec Mo |
| 2026-09-16 (3 j) | `claude/beautiful-hawking-4w1zlm` | Caelum — session parallèle | 🔧 en cours (9) | Merge origin/main (7b9552dd) — 6 experts de domaine ajoutes par une autre sess |
| 2026-09-14 (5 j) | `codex/testeur-adverse-garde-fou-survente` | Caelum — tests adverses garde-fou | 🔧 en cours (4) | Merge remote-tracking branch 'origin/main' into maj-gardefou |
| 2026-09-14 (5 j) | `codex/mesure-option3` | Caelum — mesure | ✅ posée sur main (2) | Merge remote-tracking branch 'origin/main' into codex/mesure-option3 |
| 2026-09-11 (8 j) | `codex/test-ecriture-env-defaut` | test technique (à supprimer — §10) | ✅ posée sur main (1) | test(codex): verifier l'acces en ecriture depuis l'environnement par defaut |
| 2026-09-11 (8 j) | `claude/swarm-50-agent-architecture-3l6cno` | LA LOI AVEC MOI — fiches juridiques | 🌌 univers séparé (3539) | docs(codex): cloture — PR #14 mergee, 13/13 agents verifies sur main de Caelum |
| 2026-09-11 (8 j) | `claude/nexus-market-agents-63dlku` | Nexus-Market (PR #1, posée sur main) | ✅ posée sur main (1) | docs(codex): enregistrer le merge de la PR #1 dans main |
| 2026-09-11 (8 j) | `claude/empire-chaima-linux-game-54cqgy` | Jeu Linux Empire | 🔧 en cours (7) | fix(fiches): relecture technique des quatre fiches |
| 2026-09-11 (8 j) | `claude/chaima-patent-audit-ytcxq3` | Audit brevets | 🔧 en cours (5) | docs: JOURNAL snapshot 2026-09-11 (entry ritual, no project change) |
| 2026-09-11 (8 j) | `claude/adoring-albattani-ue4vtz` | session non identifiée | 🔧 en cours (11) | docs(veille): journal — consolidation, registre unifié, dossier DÉPOSANT n° |
| 2026-09-11 (8 j) | `chore/codex-protocole-structure` | install CODEX (posée sur main) | ✅ posée sur main (1) | feat(codex): installer le PROTOCOLE CODEX (protocole + structure) sur CompeteIQ/ |

## 🟡 RALENTI — 3 branches

| Dernière activité | Branche | Projet | Écart à `main` | Dernier commit |
|---|---|---|---|---|
| 2026-09-06 (13 j) | `claude/shopify-app-development-ri1090` | App Shopify | 🔧 en cours (25) | docs: rapport de livraison horodate — installation CODEX (SYNOPSIS + audit FAI |
| 2026-09-06 (13 j) | `claude/protocole-codex-empire-wa4gp6` | PROTOCOLE CODEX (source) | 🔧 en cours (7) | docs: bloc unique sans clôture de code interne, copiable d'un seul tenant |
| 2026-09-06 (13 j) | `claude/libre-accomplis-system-9wvsnf` | Libre & Accomplis | 🔧 en cours (8) | Installation du Protocole Codex — Empire Chaima (version consolidée 2026-09-0 |

## ⚫ DORMANT — 20 branches

| Dernière activité | Branche | Projet | Écart à `main` | Dernier commit |
|---|---|---|---|---|
| 2026-07-17 (64 j) | `claude/parents-enfants-mvp-1xwgqu` | App parents-enfants | ✅ posée sur main (1) | feat(bulle): MVP démontrable app Parents-Enfants (émotions, rituels, espace pa |
| 2026-07-17 (64 j) | `claude/multi-agent-migration-factory-riujie` | Usine de migration multi-agents + index Drive | 🌌 univers séparé (68) | Ajoute index du Drive (sommaire + synopsis) selon protocole |
| 2026-07-17 (64 j) | `claude/couples-app-mvp-chaima-fx3dya` | App couples | ✅ posée sur main (2) | chore: panel d'agents orchestrateurs + protocole de passation |
| 2026-07-17 (64 j) | `claude/canvas-project-concept-c4htto` | Concept canvas | ✅ posée sur main (2) | Add dated audit report + handoff (Motif Studio) |
| 2026-07-06 (75 j) | `claude/world-cup-2026-agents-mp6mi6` | Agents Coupe du Monde 2026 | 🔧 en cours (11) | Vérification: Mexique 2-3 Angleterre — vainqueur prédit juste, pari cartons  |
| 2026-07-02 (79 j) | `claude/b2b-outreach-system-7ht0n9` | Prospection B2B | 🔧 en cours (6) | Dashboard Prospection : pilotage des agents, pipeline de prospects, journal |
| 2026-06-30 (81 j) | `claude/mistral-mnwb5j` | Pont Mistral | 🔧 en cours (3) | Add local scheduler for periodic dual-control runs |
| 2026-06-30 (81 j) | `claude/foot-site-business-plan-ch0jt0` | Site foot + business plan (SOLEA) | 🔧 en cours (21) | Add SOLEA design system (Claude Design @dsCard components: colors, type, buttons |
| 2026-06-29 (82 j) | `claude/day-trading-yahoo-finance-a0w3q8` | Day-trading Yahoo Finance | 🔧 en cours (3) | feat(trading): source de données Alpaca + sélecteur avec repli automatique |
| 2026-06-21 (90 j) | `feat/kb-seed` | CompeteIQ — base de connaissance (seed) | 🌌 univers séparé (696) | chore: add KB company profiles (20 enterprise prospects) |
| 2026-06-21 (90 j) | `feat/kb-api-stub` | CompeteIQ — API KB | 🌌 univers séparé (691) | feat(kb-seed): knowledge base README, meta.json & openapi spec |
| 2026-06-21 (90 j) | `feat/infra-security` | CompeteIQ — infra/sécurité | 🌌 univers séparé (690) | feat(infra-security): CI workflow, Docker, security docs, E2E tests, observabili |
| 2026-06-21 (90 j) | `feat/commercial-gtm` | CompeteIQ — go-to-market | 🌌 univers séparé (691) | feat(commercial-gtm): engine-builder spec, billing docs, enterprise deck, prospe |
| 2026-06-21 (90 j) | `feat/commercial-assets` | CompeteIQ — assets commerciaux | 🌌 univers séparé (696) | feat(kb-seed): add CCO persona markdown |
| 2026-06-19 (92 j) | `claude/code-review-setup-b8r9pn` | CI + revue (posée sur main) | ✅ posée sur main (2) | fix: resolve lint errors blocking CI |
| 2026-06-18 (93 j) | `claude/gta-style-game-prototype` | Prototype jeu GTA | 🌌 univers séparé (45) | Ronde 25 — CityEventAgent + SecretSystem : Ville Vivante |
| 2026-06-18 (93 j) | `claude/crm-sales` | CRM ventes | 🌌 univers séparé (47) | feat: add FollowUpScheduler intelligence module + Suivi Prioritaire dashboard |
| 2026-06-18 (93 j) | `claude/competitive-intel-saas-arch-rfh4x3` | CompeteIQ — architecture | 🔧 en cours (18) | feat: pricing page upgrades + loading skeletons for all major pages |
| 2026-06-16 (95 j) | `claude/presentation-project-selection-vy1hb7` | Présentation sélection projets | 🔧 en cours (5) | Replace simulated training/eval with a real PyTorch digit classifier |
| 2026-06-16 (95 j) | `claude/moonbow-website` | Site Moonbow | 🔧 en cours (9) | Rate-limit the contact form and make the session cookie explicit about SameSite |

## Ce que la carte dit — et rien d'autre

- **15 vivantes, 3 ralenties, 20 dormantes.** La vie est concentrée sur **Caelum/Nexus-Market
  et ATLAS**. Tout le reste dort depuis plus de 45 jours.
- **9 univers séparés** (> 30 commits d'écart) : CompeteIQ (5 branches `feat/*`, ~690
  commits chacune, **toutes du 2026-06-21**, projet EN PAUSE), La Loi Avec Moi (**3 539 commits**),
  l'usine de migration (68), CRM (47), GTA (45). **Ils ne seront jamais mergés ici** — ils
  attendent leur propre dépôt (A-DECIDER, 2026-09-14).
- **Le risque de continuité n°1 de tout l'Empire** : `claude/swarm-50-agent-architecture-3l6cno`
  — **La Loi Avec Moi, 3 539 commits, une seule copie, sur une branche.** Aucun autre projet
  n'approche ce volume. `responsable-continuite` : *une sauvegarde jamais restaurée n'est pas
  une sauvegarde* — et ici il n'y a même pas de sauvegarde, il y a une branche. **Signalé, pas
  corrigé (§10).**
- **Ce que la carte ne dit pas** : la *valeur* de chaque projet. Un univers séparé de 45 commits
  peut valoir plus qu'une branche vivante. La carte mesure l'activité et l'intégration, pas
  l'intérêt. **Ne pas décider de tuer un projet là-dessus** (`croque-mort`, §10).

## Ce que ATLAS fait de cette carte

1. **En reprise** : la lire avant tout. Elle répond à « où en étais-je ? » en 30 secondes.
2. **En surveillance** : à chaque rafale, refaire le relevé. Une branche qui passe 🟢 → ⚫ sans
   décision consignée est un projet qui **s'éteint par défaut** — la seule chose que la carte
   doit empêcher.
3. **Jamais** : supprimer, forcer, réécrire. Signaler seulement.
