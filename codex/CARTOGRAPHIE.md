# 🗺️ CARTOGRAPHIE — TEST / Nexus-Market · Caelum

> Carte vivante exigée par le **§1** (rôle `cartographe`). Créée le **2026-09-16** — elle
> n'existait pas jusque-là, alors que le rôle l'impose.
>
> **Règle de lecture :** ce document dit **où est quoi** et **ce qui est en vigueur**.
> Il ne dit pas ce qu'il faut décider — ça, c'est `codex/A-DECIDER.md`.
>
> **Méthode :** tout chiffre ci-dessous est **mesuré** par commande, jamais de mémoire.
> Chaque section porte la commande qui la reproduit.

---

## 1. LE TABLEAU DE BORD — « pourquoi rien n'a changé ? »

> `git fetch origin && git rev-parse --short origin/main`
> `git log --oneline origin/main..origin/<branche> | wc -l`

**Constat au 2026-09-19 : `main` = `7b9552dd`, inchangé depuis le 2026-09-16.**

> Ne recopie pas ce tableau de mémoire : **lance `bash scripts/audit-codex.sh`**, il le recalcule.

| Ce qui a été produit | Où ça vit | Sur `main` ? | Ce qui manque |
|---|---|---|---|
| ERR-020, ERR-021, ERR-022 · règle `git fetch` · audit des branches · carte · snapshots | `codex/err-019-branche-perimee` | **NON** — 9 commits | **Ton merge (§10)** |
| Garde-fou anti-survente (`lib/agents/garde-fou.ts` + tests) | `codex/testeur-adverse-garde-fou-survente` | **NON** — 4 commits | Ta décision sur le **texte de vente et le prix** (3 tests rouges), puis ton merge |
| Mesure d'accès en écriture | `codex/mesure-option3` | **NON** — 2 commits | Rien : c'était une mesure, pas une livraison |

**C'est toute la réponse.** Un agent peut écrire, tester et pousser. Il ne peut pas merger
dans `main` — le §10 le lui interdit. Tant que tu ne merges pas, `main` ne bouge pas, et
`main` est le seul état que lisent les autres sessions et les déploiements.

---

## 2. CE QUI EST RÉELLEMENT EN VIGUEUR SUR `main`

> Test appliqué à chaque correctif du registre nommant un artefact :
> `git cat-file -e origin/main:<fichier>` ou `git show origin/main:<f> | grep -q <motif>`

| Correctif annoncé | Artefact | En vigueur sur `main` |
|---|---|---|
| ERR-001 — client Prisma absent au build | `postinstall: prisma generate` | ✅ |
| ERR-005 — espace insécable dans un test | regex tolérante | ✅ |
| ERR-010 — CI revue auto en échec | workflow rendu non bloquant | ✅ |
| ERR-015 — données de prospection exposées | règles `.gitignore` | ✅ |
| ERR-018 — escalade prématurée | règle du découpage, `AGENTS.md` | ✅ |
| ERR-016/018 — garde-fou anti-survente | `lib/agents/garde-fou.ts` | ❌ **ERR-021** |
| ERR-020 — branche sur `main` périmé | règle du `git fetch`, `AGENTS.md` | ❌ **ERR-022** |

**5 sur 7.** Les deux manquants sont consignés comme erreurs à part entière, pas dissimulés.

**Conséquence à connaître :** les sessions clonent la branche par défaut. Elles chargent
donc l'`AGENTS.md` de `main` — qui contient la règle du découpage (ERR-018) mais **pas**
celle du `git fetch`. Le garde-fou censé empêcher la récidive d'ERR-011/020 ne protège
personne aujourd'hui.

---

## 2 bis. L'AUDIT EXÉCUTABLE — `scripts/audit-codex.sh`

```bash
bash scripts/audit-codex.sh        # ~5 s, lecture seule, aucune écriture
```

Le rituel §5 rendu exécutable. Il refait, par la mesure, tout ce qui précède :

| # | Ce qu'il vérifie | Né de |
|---|---|---|
| 0 | `git fetch` puis l'état serveur de `main` | ERR-011 / ERR-020 |
| 1 | Écart branches ↔ `main` — le travail poussé mais **pas livré** | ERR-022 |
| 2 | Chaque correctif annoncé est-il **en vigueur sur `main`** ? | ERR-021 |
| 3 | Registre : ID en double, entrée sans correctif | — |
| 4 | Structure §12 complète + les 21 rôles du §1 présents | §12 / §1 |
| 5 | `CLAUDE.md` et `ETAT.md` se contredisent-ils ? | §5 |
| 6 | Décisions qui dorment depuis plus de 14 jours | §6 |

**Pourquoi il existe :** trois erreurs — ERR-020, 021, 022 — où une vérification de dix
secondes aurait évité des jours de travail invisible. *Un audit qu'on refait à la main est
un audit qu'on oublie de refaire.*

Les branches dont l'historique diverge de plus de 100 commits sont marquées « historique
étranger » et **exclues du total** : ce sont des projets sans lien hébergés dans ce dépôt,
les compter noierait le signal — l'erreur commise au premier audit des branches.

---

## 3. LA MACHINE — ce qui tourne

> `find app/api -name route.ts | wc -l` · `ls lib/agents/*.ts`

**Stack :** Next.js 16 · TypeScript · Prisma (SQLite/libsql) · Tailwind v4 · next-auth · Vitest.

### Boucle de vente Caelum — 4 agents en séquence

| Agent | Fichier | Route API | Page | Rôle |
|---|---|---|---|---|
| HERMES | `lib/agents/hermes.ts` | `POST /api/hermes/draft` | `/dashboard/prospection` | Brouillons de prospection LinkedIn |
| BOUSSOLE | `lib/agents/boussole.ts` | `POST /api/boussole/qualify` | `/dashboard/qualification` | Qualification du prospect |
| PACTE | `lib/agents/pacte.ts` | `POST /api/pacte/draft` | `/dashboard/devis` | Devis / proposition commerciale |
| RELANCE | `lib/agents/relance.ts` | `POST /api/relance/draft` | `/dashboard/relance` | Séquence de relance J+3 / J+7 |

**Sans état, sans persistance, sans envoi.** Chaque agent produit un brouillon copiable ;
l'envoi est manuel (§10). Deux chemins par agent : `LLM*` (nécessite `ANTHROPIC_API_KEY`,
**non posée**) et `Heuristic*` — **le seul chemin actif aujourd'hui**.

### Les agents de gouvernance — 27 au total

**Les 21 rôles du §1** (chaîne d'entrée · cœur délibératif · tenue de l'Empire · angles morts)
sont tous présents, vérifié par l'audit.

**+ 6 ajoutés le 2026-09-16** à ta demande : `expert-nextjs`, `expert-donnees-prisma`,
`expert-llm-agents`, `expert-authentification`, `expert-cicd-deploiement`, `orchestrateur`.
Chacun déclare explicitement ce dont il se distingue (§9, anti-doublon) — p. ex.
`expert-donnees-prisma` ≠ `gardien-donnees`, qui traite le RGPD et non la couche technique.

> **À savoir :** le skill `.claude/skills/debat/` **et** l'agent `orchestrateur` garantissent
> tous deux le lancement **parallèle** d'`avocat` + `contradicteur` (§8 Parcours 2). Ce n'est
> pas un doublon — `debat` exécute le parcours, `orchestrateur` aiguille vers lui — mais il
> faut savoir que les deux existent pour ne pas en chercher un troisième.

### Support
`commandant.ts` (orchestration) · `compliance.ts` (règles dures, plafond LinkedIn 25/j) ·
`registry.ts` (flotte) · `resolveur.ts`.

### Produit historique — CompeteIQ
Pipeline de veille concurrentielle : `/api/pipeline/*`, `/api/competitors/*`, `/api/alerts`,
`/api/reports`, `/api/stats` + pages `/dashboard/{pipeline,competitors,compare,alerts,reports,pricing}`.
**Statut : EN PAUSE** (marché dominé) — tranché par Chaima, réveil lié à Caelum.

---

## 4. OÙ ÉCRIT-ON QUOI — la règle anti-confusion

Deux agents qui rangent la même chose à deux endroits ne communiquent pas (§13).

| Tu veux consigner… | Le SEUL fichier | Règle |
|---|---|---|
| Une **erreur réellement survenue** | `🔴 ERREURS.md` | Un incident = une entrée datée `ERR-NNN`. Format fixe : *Ce qui s'est passé · Cause · Détection · Correctif · Prévention sous forme de test*. **Jamais** une erreur hypothétique. |
| Ce qui **fonctionne**, chiffres du gate | `ETAT.md` | Instantané vivant, court, daté, ré-exécuté — pas rapporté. |
| Ce qui **attend ta décision** | `codex/A-DECIDER.md` | Trié par ancienneté. Une ligne ne disparaît que **tranchée**, jamais parce qu'elle a vieilli. > 14 j = mis en évidence. |
| Un **jalon significatif** | `codex/EVOLUTION.md` | **APPEND-ONLY.** Jalon, décision prise, lancement, problème résolu. Jamais « rien de neuf ». |
| Le **snapshot de session** (§5) | `📋 JOURNAL.md` | Rien n'a changé → **une seule ligne**. Quelque chose a changé → une entrée datée. Un rapport pour dire qu'il n'y a rien à dire est une faute. |
| Un **événement daté détaillé** | `reports/AAAA-MM-JJ-*.md` | Un fichier par événement réel. |
| **Où est quoi / ce qui est en vigueur** | `codex/CARTOGRAPHIE.md` | Ce fichier. |

**Le test qui tranche entre `ERREURS.md` et `A-DECIDER.md` :** est-ce que **quelque chose
a mal tourné** ? → `ERREURS.md`. Est-ce qu'**une décision manque** ? → `A-DECIDER.md`.
Un défaut qui attend ta décision va **dans les deux**, avec un renvoi croisé.

---

## 5. LES BRANCHES

> `reports/2026-09-14-audit-branches-perimees.md` — audit complet, 35 branches.

- **Branche principale : `main`.** Toute nouvelle branche en part (`git checkout -b <nom> origin/main`).
- **`claude/nexus-market-agents-63dlku`** — désignée « branche de dev » par `CLAUDE.md`, mais
  **PR #1 est mergée** : `ETAT.md` dit qu'elle n'est plus la branche de travail. **`CLAUDE.md`
  n'a pas été mis à jour** → contradiction interne, consignée dans `A-DECIDER.md`.
- **~25 branches de projets étrangers** (jeux, sites, prototypes sans lien avec Caelum/CompeteIQ),
  aucune mergée : chacune est la seule copie de son travail. **Ne rien supprimer** (§10).

---

## 6. LES PIÈGES — à relire avant d'écrire du code

| Piège | Symptôme | Quoi faire |
|---|---|---|
| **Prisma** (ERR-001) | `next build` → « module not found » sur `@/lib/generated/prisma/client` | `postinstall: prisma generate` est en place — **ne pas le retirer** |
| **`tsc` seul** (ERR-008) | `Cannot find name 'PageProps'` | Lancer `npm run build` **avant** de conclure : artefact, pas un défaut |
| **`node_modules`** (ERR-004) | Disparaît en cours de session | `npm install` (le postinstall régénère Prisma) |
| **Backticks** (ERR-017) | Commit `-m` mangé par le shell | Heredoc à délimiteur **quoté** (`<<'EOF'`) |
| **Vercel** (ERR-002/003) | 8 projets déploient ce dépôt → quota saturé, faux rouges | Bruit connu — commenter une fois, ne pas répéter |
| **`main` périmé** (ERR-011/020) | Branche qui ignore des commits | `git fetch` **en première commande**, brancher sur `origin/main` |

**Gate avant tout push (§8 Parcours 4) :**
```bash
npm run lint && npm run build && npx tsc --noEmit && npm test
```
> `build` **avant** `tsc` — sinon ERR-008 se déclenche et le résultat est faux.

---

## 7. CE QUI RESTE STRICTEMENT À TOI (§10)

Merger ou pousser sur `main` · engager une dépense · envoyer quoi que ce soit à un tiers ·
signer · supprimer une branche, un fichier, un abonnement · relecture juridique du contenu
public · déclarer « LANCÉ » ou « SIGNÉ ».

**Un agent recommande. Chaima décide.** Cette frontière ne se négocie pas — et c'est elle
qui explique pourquoi `main` n'a pas bougé.
