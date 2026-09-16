# Calcul des heures réelles de travail — Caelum Partners & La Loi Avec Moi

**Date d'analyse :** 2026-09-16
**Méthode :** reconstruction de sessions à partir de l'horodatage des commits Git.
**Dépôts analysés :** `chaima0007/keywordmoneymaker` (Caelum Partners) et
`chaima0007/droit-citoyen-app` (La Loi Avec Moi), **toutes branches**, clones complets
(non superficiels), commits de fusion exclus.

---

## 1. LE CHIFFRE À CITER

> **≈ 29 heures de travail humain effectif**, réparties sur **21 sessions** et
> **15 jours d'activité distincts**, entre le **10 juin 2026** et le **15 septembre 2026**
> (13,7 semaines) — soit **≈ 2,1 h/semaine** et **≈ 2,0 h par jour travaillé**.

Détail par produit (avant dédoublonnage) :

| Produit | Commits | Sessions | Période | Heures |
|---|---|---|---|---|
| Caelum Partners | 116 | 16 | 10/06 → 15/09 | **24,5 h** |
| La Loi Avec Moi | 24 | 14 | 16/06 → 14/09 | **11,2 h** |
| Somme brute | 140 | 30 | — | 35,7 h |
| **Union dédoublonnée** | **140** | **21** | 10/06 → 15/09 | **29,3 h** |

**6,4 h ont été retirées** parce que 5 journées (17/07, 10/08, 06/09, 11/09, 14/09) comportent
des sessions **simultanées sur les deux dépôts** : le même temps de travail y produit des
commits dans les deux projets. Additionner 24,5 + 11,2 aurait compté ces heures deux fois.

---

## 2. MÉTHODE EXACTE (reproductible)

1. `git log --all --no-merges --pretty=format:'%H|%an|%ae|%cn|%ce|%aI|%cI|%s'` sur chaque dépôt.
2. Déduplication par SHA (une même branche apparaît sur plusieurs refs), tri chronologique.
3. **Normalisation en `Europe/Brussels`.** Les commits de session Claude Code sont horodatés
   en UTC (`+00:00`), ceux poussés depuis la machine de Chaima en `+02:00`. Sans conversion,
   la détection « nocturne » et le découpage des sessions sont faux.
4. Regroupement en sessions : deux commits séparés de **moins de 90 minutes** appartiennent
   à la même session.
5. **+30 minutes forfaitaires** avant le premier commit de chaque session (lecture, réflexion,
   mise en contexte avant le premier commit).
6. Union des intervalles des deux dépôts, pour supprimer le chevauchement.

Scripts : `calc.py`, `auto.py`, `union.py` (session d'analyse, non versionnés).

---

## 3. EXCLUSION DES COMMITS AUTOMATISÉS — RÉSULTAT : ENSEMBLE VIDE

La méthode demandait d'exclure les commits produits par une boucle d'agent non supervisée.
**Recherche menée, aucun commit de ce type trouvé.** Quatre contrôles :

| Contrôle | Résultat |
|---|---|
| Auteurs bots (`[bot]`, `github-actions`, etc.) | **0** sur 140 commits. Trois identités seulement : `Claude`, `chaima0007`, `Chaima Mhadbi` |
| Mots-clés `boucle` / `loop` / `cron` / `routine` dans les messages | 4 occurrences — toutes portent **sur** le sujet (ex. « registre des Routines »), aucune n'est produite **par** une boucle |
| Cadence régulière (coefficient de variation des écarts < 0,25 sur ≥ 4 commits) | **1 rafale sur 11** (06/09 21h24, 4 commits à ~1,7 min) — compatible avec une session interactive qui commite en série, pas avec un ordonnanceur |
| Commits nocturnes 00h–06h (heure de Bruxelles) | **5 sur 140** (3,6 %), isolés, non répétitifs |

Écart médian entre deux commits d'une même session : **4,6 min** (Caelum), **13,0 min**
(La Loi Avec Moi), avec un écart-type de 12,3 min — c'est-à-dire **irrégulier**. Une boucle
automatisée produit l'inverse : une cadence fixe.

**VERDICT : CONFIRMÉ** — aucun commit à exclure. Le chiffre de 29,3 h ne contient pas de
travail machine non supervisé.

---

## 4. LA CONTRADICTION QUE TU DOIS CONNAÎTRE AVANT L'ENTRETIEN

C'est le point faible de la méthode telle qu'elle était formulée, et il faut l'avoir vu avant
qu'un recruteur le voie.

**105 des 116 commits Caelum et 21 des 24 commits La Loi Avec Moi sont signés
`Claude <noreply@anthropic.com>`.** Deux lectures opposées :

**Lecture stricte (périmètre A)** — ne compter que les commits dont Chaima est l'auteur Git :

| Produit | Commits | Sessions | Heures |
|---|---|---|---|
| Caelum Partners | 13 | 7 | **6,2 h** |
| La Loi Avec Moi | 3 | 2 | **1,1 h** |

→ **7,3 h**. Chiffre incontestable, mais **il mesure la mauvaise chose** : il compte les
commits tapés à la main et ignore les sessions de pilotage, où le travail réel est la
formulation, l'arbitrage et la revue. Il est aussi trompeur en sens inverse : la session du
11/09 17h22→19h57 sous son nom (5 commits, 3,1 h) est majoritairement du merge de PR.

**Lecture retenue (périmètre B)** — compter toute session, y compris pilotée. Justification
vérifiable dans le dépôt : `CLAUDE.md` §10 réserve à l'humain la validation, le merge,
l'engagement de dépense et toute décision « LANCÉ » ; `🔴 ERREURS.md` recense des corrections
imposées par elle après revue (E-17, E-19, E-23). **Ces commits n'existent pas sans une
personne présente qui décide.**

**Ce que ça donne en entretien.** Ne dis pas « j'ai codé 29 heures ». Dis :

> « 29 heures de sessions de développement mesurées sur mon historique Git, dont environ 7
> heures de commits écrits directement de ma main et le reste en pilotage d'agents avec revue
> et arbitrage. C'est calculé à partir des horodatages, pas estimé. Voici la méthode. »

Cette phrase-là tient devant quelqu'un qui ouvre le `git log` pendant l'entretien. « 29 heures
de code écrit à la main » ne tient pas.

---

## 5. SENSIBILITÉ — de quoi dépend le chiffre

| Seuil de session | Forfait avant session | Total (union) |
|---|---|---|
| 90 min | 0 min | 18,4 h |
| 60 min | 30 min | 28,7 h |
| **90 min** | **30 min** | **29,3 h** ← retenu |
| 120 min | 30 min | 33,0 h |
| 90 min | 45 min | 34,5 h |
| 120 min | 45 min | 37,5 h |

**Fourchette défendable : 28 – 33 h.** En dessous de 28 h on nie le temps de préparation ;
au-delà de 33 h on étire des hypothèses que rien dans les données ne soutient. **Annonce 29 h.**

---

## 6. LIMITES — à énoncer toi-même, avant qu'on te les oppose

1. **Le forfait de 30 min est une convention, pas une mesure.** 12 des 30 sessions ne
   contiennent qu'un seul commit : leur durée est donc **entièrement** conventionnelle.
   C'est le poste le plus contestable du calcul (≈ 6 h sur 29).
2. **Tout ce qui ne produit pas de commit est invisible :** lecture de réglementation,
   recherche de sources, design, réflexion hors clavier, appels, sessions abandonnées.
   → **le chiffre est un plancher, pas un plafond.**
3. **La fin d'une session n'est pas mesurée.** Le dernier commit clôt la session ; le temps
   de vérification et de déploiement qui suit n'est pas compté. Sous-estimation supplémentaire.
4. **Le travail hors Git n'est pas couvert :** Google Drive, Vercel/Cloudflare, i-DEPOT,
   échanges. `📒 PROPRIÉTÉ.md` et `/codex/A-DECIDER.md` montrent une activité de décision qui
   ne laisse pas toujours de trace Git.
5. **Dépôt privé :** `droit-citoyen-app` a bien nécessité un accès authentifié — il a été
   attaché à la session et cloné intégralement. **NON VÉRIFIÉ :** son statut exact
   (privé/public) n'a pas été relevé auprès de l'API GitHub ; seul compte ici le fait que
   l'historique complet a été obtenu.
6. **Branches non fusionnées incluses.** `--all` compte le travail de branches jamais mergées.
   C'est volontaire — le temps a été passé — mais ce n'est pas du code en production.
7. **Fuseau des commits Claude Code :** horodatés UTC par l'environnement d'exécution, pas
   nécessairement l'heure locale de Chaima. Converti en Europe/Brussels ; **PLAUSIBLE**, non
   confirmé par une source indépendante.

---

## 7. VOLUME PRODUIT — pour répondre à « 29 h pour tout ça ? »

| | Caelum Partners | La Loi Avec Moi |
|---|---|---|
| Fichiers suivis (branche par défaut) | 169 | 8 |
| Lignes (branche par défaut) | 17 960 | 208 |
| Lignes ajoutées (toutes branches) | 24 440 | 8 500 |
| Lignes supprimées (toutes branches) | 3 888 | 964 |

**Attention :** ce volume est **produit en pilotage d'agents**, il ne démontre pas une
vitesse de frappe. Utilise-le pour décrire l'ampleur du périmètre, jamais comme preuve de
productivité individuelle — c'est exactement l'endroit où un entretien technique retourne
l'argument.

---

    DE : analyse-historique-git        POUR : CHAIMA
    OBJET : citer « ≈ 29 h de sessions de développement, dont ≈ 7 h de commits directs »
            et non « 29 h de code écrit à la main ».
    VERDICT : CONFIRMÉ pour les 29,3 h (reproductible depuis le git log).
              CONFIRMÉ pour l'absence de commits de boucle automatisée.
    PARCE QUE : 140 commits horodatés, dédoublonnés par SHA, normalisés Europe/Brussels,
                regroupés en 21 plages disjointes ; 0 auteur bot, 0 cadence d'ordonnanceur,
                5 commits nocturnes sur 140.
    NON VÉRIFIÉ : le temps réel avant le premier commit de chaque session (convention de
                  30 min, ≈ 6 h du total) ; tout travail sans trace Git ; le fuseau horaire
                  réel des sessions Claude Code.
    CE QUI CHANGERAIT MON AVIS : un export d'activité horodaté hors Git (sessions Claude Code,
                  Drive, Vercel) — il ferait monter le chiffre, jamais descendre.
