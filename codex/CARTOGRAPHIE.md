# /codex/CARTOGRAPHIE.md — carte vivante du dépôt (rôle `cartographe`, §1)

> État réel vérifié le **2026-09-16 ~12h30 UTC** par `git fetch`, `git for-each-ref` et l'API GitHub.
> Pas de mémoire : chaque chiffre ci-dessous a été mesuré, pas rappelé.
> Cette carte se met à jour quand la réalité change — pas quand on y pense.

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
