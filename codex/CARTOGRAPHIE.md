# /codex/CARTOGRAPHIE.md — carte vivante du dépôt (rôle `cartographe`, §1)

> État réel vérifié le **2026-09-16 ~12h30 UTC** par `git fetch`, `git for-each-ref` et l'API GitHub.
> Pas de mémoire : chaque chiffre ci-dessous a été mesuré, pas rappelé.
> Cette carte se met à jour quand la réalité change — pas quand on y pense.
>
> **Ne la recopie pas de mémoire : lance `bash scripts/audit-codex.sh`** (~5 s, lecture seule).
> Il recalcule les sections 1, 4, 7 et 8 par la mesure.
>
> *Deux cartes concurrentes ont été écrites en parallèle les 16 et 19 septembre par deux
> sessions qui ne se voyaient pas. Fusionnées ici le 2026-09-19 : les sections 1 à 6 viennent
> de la version de `main`, les sections 7 à 11 de l'autre. Rien n'a été écrasé.*

---

## 1. LE CONSTAT QUI EXPLIQUE TOUT LE RESTE

**`main` est figé depuis le 2026-09-14 20h28** (`70e657b6`). Rien n'y est entré depuis.
Pendant ce temps : **38 références distantes**, **6 pull requests ouvertes**, dont trois
vieilles de presque trois mois.

Ce n'est pas une panne. C'est la conséquence directe du **§10** : *merger sur la branche
principale est strictement humain*. Les agents produisent, poussent, vérifient — et
s'arrêtent à la porte. Tant que personne ne merge, le travail s'accumule en branches.

**Le goulot n'est pas technique. Il est humain, et il est unique : Chaima.**

---

## 2. LES 6 PULL REQUESTS OUVERTES

| PR | Sujet | Ouverte depuis | Base | État |
|---|---|---|---|---|
| **#9** | Réconciliation des 21 agents CODEX | 2026-09-14 | `main` | ✅ verte, mergeable — **attend un arbitrage** (contradiction de décisions) |
| **#7** | Shopify : thème, app, dropshipping « Patchou » | 2026-07-17 | `main` | base périmée (`cbe82e0`) — projet étranger à Nexus-Market |
| **#6** | Système « Libre & Accomplis » | 2026-07-13 | `main` | base périmée (`fb150ea`) — projet étranger |
| **#5** | Commercial assets (brouillon) | 2026-06-21 | `claude/swarm-50-agent…` | brouillon, base ≠ `main` |
| **#4** | KB API stub (brouillon) | 2026-06-21 | `claude/swarm-50-agent…` | brouillon, base ≠ `main` |
| **#3** | Swarm wave-66 (brouillon) | 2026-06-21 | `main` | brouillon |

**Trois d'entre elles (#3, #4, #5) empilent sur une branche qui n'est pas `main`.** Elles ne
peuvent pas atterrir tant que leur base n'a pas atterri. C'est une pile orpheline.

---

## 3. CE QUI HABITE CE DÉPÔT

Le dépôt porte **au moins cinq projets sans rapport entre eux** : Nexus-Market/Caelum (actif),
CompeteIQ (en pause), Shopify/Patchou, Libre & Accomplis, Swarm — plus des branches
« couples-app », « gta-style-game », « foot-site », « world-cup-2026 », « moonbow », « crm-sales »…

C'est déjà consigné dans `A-DECIDER.md` (« Sortir les projets étrangers de ce dépôt »),
et c'est la cause racine d'ERR-002 et ERR-003 : les projets Vercel étrangers branchés ici
échouent à chaque commit, sur n'importe quelle PR, y compris documentaire.

---

## 4. ÉTAT DES REGISTRES — ce qui est bien rangé, ce qui ne l'est pas

| Fichier | Contenu mesuré | Verdict |
|---|---|---|
| `🔴 ERREURS.md` | 20 entrées ERR structurées | ✅ vivant et bien tenu |
| `📋 JOURNAL.md` | 13 snapshots datés | ✅ tenu, règle anti-bruit respectée |
| `codex/A-DECIDER.md` | **14 décisions en attente**, 8 tranchées | ✅ tenu — mais 14 est beaucoup |
| `codex/EVOLUTION.md` | 19 événements, append-only | ✅ tenu |
| `📒 PROPRIÉTÉ.md` | registre IP, 127 lignes | ✅ tenu |
| `codex/candidates/` | **0 fiche** | ⚠️ jamais alimenté |
| `codex/expertise/` | **0 fiche** | ⚠️ jamais alimenté — la boucle §4 n'a rien produit |
| `codex/opportunites/` | **0 fiche** | ⚠️ jamais alimenté |
| `codex/licences-sortantes/` | **0 fiche** | ⚠️ jamais alimenté |

**Écart signalé, non corrigé seul (§5.5) :** les quatre dossiers du §12 existent mais sont vides.
La structure est conforme ; la **boucle d'expertise du §4 n'a jamais tourné**. Aucun agent ne
peut « consulter /codex/expertise avant toute recherche » s'il n'y a rien à consulter.
Ce n'est pas un bug — c'est une pratique qui n'a pas démarré.

**Écart de rangement corrigé aujourd'hui :** les obstacles d'exploitation constatés le 14/09
vivaient uniquement dans `reports/2026-09-14-2130-…` ; 7 des 8 étaient introuvables depuis le
registre. Une entrée d'index les y rend accessibles (voir ERR-021), sans dupliquer le rapport
(§9, anti-bloat).

---

## 5. CE QUI TOURNE, CE QUI EST BLOQUÉ

**Ce qui fonctionne, vérifié :**
- chaîne de vérification `lint && tsc && test && build` : **77/77 tests, 0 erreur** ;
- CI GitHub `Lint, Typecheck & Build` : verte sur le head de la PR #9 ;
- écriture GitHub depuis une session interactive : **VÉRIFIÉE** (pushs réels sur les deux dépôts).

**Ce qui est bloqué, et pourquoi :**

| Quoi | Bloqué sur | Nature |
|---|---|---|
| PR #9 | contradiction entre deux décisions « TRANCHÉ PAR CHAIMA » | arbitrage humain (§10) |
| PR #3 à #7 | personne ne merge | action humaine (§10) |
| Accès en écriture des Routines | Routine à créer depuis l'interface claude.ai | limite d'outillage établie |
| Projets Vercel étrangers | compte Vercel | action humaine |
| Numérotation du registre | convention à trancher | décision, options livrées |
| Dossiers `/codex/` vides | la boucle §4 n'a jamais démarré | pratique à lancer |

---

## 6. CE QUE CETTE CARTE NE DIT PAS

- Le contenu des **19 commits** de `main` antérieurs au 2026-09-11 n'a pas été relu ligne à ligne.
- Les PR #3 à #7 n'ont pas été auditées sur le fond : seules leur date, leur base et leur état le sont.
- Rien ici n'est une recommandation de merger ou de fermer quoi que ce soit. **Un agent recommande, Chaima décide (§10).**

---

## 7. CORRECTIFS ANNONCÉS vs CORRECTIFS EN VIGUEUR

> Test appliqué à chaque entrée du registre nommant un artefact :
> `git cat-file -e origin/main:<fichier>` — recalculé par `audit-codex.sh`, section 2.

| Correctif annoncé | Artefact | En vigueur sur `main` |
|---|---|---|
| ERR-001 — client Prisma absent au build | `postinstall: prisma generate` | ✅ |
| ERR-010 — CI revue auto en échec | workflow rendu non bloquant | ✅ |
| ERR-015 — données de prospection exposées | règles `.gitignore` | ✅ |
| ERR-018 — escalade prématurée | règle du découpage, `AGENTS.md` | ✅ |
| ERR-016 — garde-fou anti-survente | `lib/agents/garde-fou.ts` | ❌ `ERR-20260914-2033` |
| `ERR-20260914-1956` — branche sur `main` périmé | règle du `git fetch`, `AGENTS.md` | ❌ `ERR-20260916-1413` |

**Trois états, jamais deux :** `ÉCRIT` (existe quelque part) · `LIVRÉ` (poussé, gate vert) ·
`EN VIGUEUR` (sur `main`, donc chargé par les sessions et les déploiements). **Seul le
troisième protège quelqu'un.** Les sessions clonent la branche par défaut : un `AGENTS.md`
qui n'est pas sur `main` n'est chargé par personne.

---

## 8. L'AUDIT EXÉCUTABLE — `scripts/audit-codex.sh`

```bash
bash scripts/audit-codex.sh        # ~5 s, lecture seule, aucune écriture
```

| # | Ce qu'il vérifie | Né de |
|---|---|---|
| 0 | `git fetch` puis l'état serveur de `main` | ERR-011 / `ERR-20260914-1956` |
| 1 | Écart branches ↔ `main` — poussé mais **pas livré** | `ERR-20260916-1413` |
| 2 | Chaque correctif est-il **en vigueur sur `main`** ? | `ERR-20260914-2033` |
| 3 | Registre : ID en double, entrée sans correctif | — |
| 4 | Structure §12 + les 21 rôles du §1 présents | §12 / §1 |
| 5 | `CLAUDE.md` et `ETAT.md` se contredisent-ils ? | §5 |
| 6 | Décisions dormantes depuis plus de 14 jours | §6 |

*Un audit qu'on refait à la main est un audit qu'on oublie de refaire.* Les branches
divergeant de plus de 100 commits sont marquées « historique étranger » et exclues du total :
les compter noierait le signal.

---

## 9. LA MACHINE — ce qui tourne techniquement

**Stack :** Next.js 16 · TypeScript · Prisma (SQLite/libsql) · Tailwind v4 · next-auth · Vitest.

### Boucle de vente Caelum — 4 agents en séquence

| Agent | Fichier | Route API | Page |
|---|---|---|---|
| HERMES | `lib/agents/hermes.ts` | `POST /api/hermes/draft` | `/dashboard/prospection` |
| BOUSSOLE | `lib/agents/boussole.ts` | `POST /api/boussole/qualify` | `/dashboard/qualification` |
| PACTE | `lib/agents/pacte.ts` | `POST /api/pacte/draft` | `/dashboard/devis` |
| RELANCE | `lib/agents/relance.ts` | `POST /api/relance/draft` | `/dashboard/relance` |

Sans état, sans persistance, **sans envoi** — l'envoi est manuel (§10). Deux chemins par
agent : `LLM*` (exige `ANTHROPIC_API_KEY`, **non posée**) et `Heuristic*`, **le seul chemin
actif aujourd'hui**. C'est pourquoi un garde-fou posé sur le seul chemin LLM ne protège rien.

**Support :** `commandant.ts` (orchestration) · `compliance.ts` (règles dures, plafond
LinkedIn 25/j) · `registry.ts` · `resolveur.ts`.

### Les agents de gouvernance — 30

Les **21 rôles du §1** + **6 experts de domaine** (2026-09-16) + **3 agents de garantie**
(2026-09-19) : `valideur` (la prémisse tient-elle ?), `essayeur` (exécuter plutôt que
raisonner), `confirmateur` (est-ce en vigueur là où ça tourne ?).

> **Contrainte mesurée le 2026-09-19 :** un agent écrit pendant une session **n'y est pas
> utilisable** — le registre des agents est figé au démarrage. Preuve : `Agent type
> 'valideur' not found`. Il faut une nouvelle session **et** un merge dans `main` pour qu'un
> agent existe pour tout le monde. Deux niveaux de « pas encore en vigueur ».

---

## 10. OÙ ÉCRIT-ON QUOI — la règle anti-confusion

Deux agents qui rangent la même chose à deux endroits ne communiquent pas (§13).

| Tu veux consigner… | Le SEUL fichier |
|---|---|
| Une **erreur réellement survenue** | `🔴 ERREURS.md` — un incident = une entrée. Nouvelle entrée : `ERR-AAAAMMJJ-HHMM` (tranché le 2026-09-19) |
| Ce qui **fonctionne**, chiffres du gate | `ETAT.md` — court, daté, ré-exécuté |
| Ce qui **attend une décision de Chaima** | `codex/A-DECIDER.md` — trié par ancienneté, > 14 j en évidence |
| Un **jalon significatif** | `codex/EVOLUTION.md` — **APPEND-ONLY** |
| Le **snapshot de session** (§5) | `📋 JOURNAL.md` — rien changé → **une ligne** |
| Un **événement daté détaillé** | `reports/AAAA-MM-JJ-*.md` |
| **Où est quoi / ce qui est en vigueur** | ce fichier |

**Le test qui tranche :** quelque chose a **mal tourné** → `ERREURS.md`. Une **décision
manque** → `A-DECIDER.md`. Un défaut qui attend une décision va dans **les deux**, avec renvoi croisé.

---

## 11. LES PIÈGES — à relire avant d'écrire du code

| Piège | Symptôme | Quoi faire |
|---|---|---|
| **Prisma** (ERR-001) | `next build` → « module not found » | `postinstall: prisma generate` — ne pas le retirer |
| **`tsc` seul** (ERR-008) | `Cannot find name 'PageProps'` | `npm run build` **avant** `tsc` — artefact, pas un défaut |
| **`node_modules`** (ERR-004) | disparaît en cours de session | `npm install` |
| **Backticks** (ERR-017) | commit `-m` mangé par le shell | heredoc à délimiteur **quoté** (`<<'EOF'`) |
| **Vercel** (ERR-002/003) | 8 déploiements par push, faux rouges | bruit connu — signaler une fois |
| **`main` périmé** (ERR-011) | branche qui ignore des commits | `git fetch` en **première** commande |
| **Collision d'ID** | deux sessions, même numéro | horodatage `ERR-AAAAMMJJ-HHMM` |

**Gate avant tout push (§8 Parcours 4) :**
```bash
npm run lint && npm run build && npx tsc --noEmit && npm test
```
> `build` **avant** `tsc`, sinon ERR-008 fausse le résultat.
