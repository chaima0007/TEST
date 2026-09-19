# ATLAS — PROFIL DE CHAIMA

> **La base qui grandit avec le temps, volet « qui je sers ».**
> Chaque ligne : le fait, la date, et **comment je l'ai su**. Une ligne sans origine est une
> supposition déguisée en connaissance — exactement ce que §13 interdit.
> Une information ne se supprime pas : elle se marque **périmée**, datée, avec le motif.

## Ce qui est VÉRIFIÉ (dit par Chaima elle-même)

| Fait | Conséquence opérationnelle | Dit le | Statut |
|---|---|---|---|
| **Ne code pas encore bien** | Tout est **copiable-collable**, **une action à la fois**, et rien ne suppose qu'elle sache réparer. Chaque étape sort en trois temps : la commande · la vérification · quoi faire si ça rate. Aucun raccourci « tu n'as qu'à… ». | 2026-09-16 | **ACTIF** |
| **Veut un système « inarrêtable »** | Requalifié avec elle : une machine s'arrête toujours ; ce qui doit être inarrêtable, c'est la **connaissance**. Voir `../continuite/RESTAURATION.md`. | 2026-09-16 | **ACTIF** |
| **Veut une base qui grandit avec le temps** | Mémoire + corpus, pas les poids du modèle. `memoire/` et `corpus/`. | 2026-09-16 | **ACTIF** |
| **Veut du rangement strict, pas de documents entremêlés** | `../ROUTAGE.md` : un type = un sous-dossier = un seul fichier vivant, ajout en tête. | 2026-09-16 | **ACTIF** |
| **Exige qu'on ne la flatte pas** | Dire la vérité même quand elle dérange ; se contredire quand c'est justifié. | 2026-09-16 | **ACTIF** |
| **Objectif final : être autonome**, pilote de son système | Chaque étape la rend capable de la refaire seule. Pas de dépendance à moi. | 2026-09-16 | **ACTIF** |
| **OS : Windows 11**, build `10.0.26200.9457` | Toutes les commandes sont Windows. **VÉRIFIÉ** par capture d'écran de l'invite de commandes, pas par déclaration. | 2026-09-16 | **ACTIF** |
| **Session utilisateur : `C:\Users\Chaima`** | C'est là que vivront le modèle, la mémoire et le corpus. | 2026-09-16 | **ACTIF** |
| **Matériel complet relevé** | 16 Go de RAM · i7-8650U · **aucune carte graphique utilisable** · 120 Go libres. Détail et conséquences : `MACHINE.md`. **Le fine-tuning est matériellement fermé.** | 2026-09-16 | **ACTIF** |
| **Ouvre l'Invite de commandes, pas PowerShell** | Ne jamais dire « ouvre PowerShell » : dire « tape `powershell` dans la fenêtre déjà ouverte », et donner le repère `PS` avant le curseur (ERR-ATLAS-001). | 2026-09-16 | **ACTIF** |

## Ce qui est PLAUSIBLE — raisonné, pas confirmé (§13)

| Fait | Fiabilité | Origine | Comment ça devient VÉRIFIÉ |
|---|---|---|---|
| **Version exacte : Windows 11 25H2** | **MODÉRÉE** | La build `26200` appartient à la série Windows 11 ; le nom commercial de cette build n'a pas été vérifié sur une source primaire datée. | Sortie de `winver` ou de `Get-CimInstance Win32_OperatingSystem`. **Sans effet sur nos choix** : ce qui compte est la RAM et la carte graphique, pas le nom commercial. |

## L'attente exprimée — et son arbitrage

**Chaima, 2026-09-16 :** *« une IA qui ressemble à Claude, que je peux tout lui demander, et
qu'elle soit autonome mais surveillée. »*

C'est l'ambition, pas un usage n°1. Elle se décompose en quatre attentes, dont **trois sont
atteignables sur sa machine et une ne l'est pas**. Les confondre mènerait à une déception
garantie dans trois mois — donc la décomposition est consignée ici, pas gommée.

| Ce qui fait « Claude » | Atteignable chez Chaima ? | Par quoi |
|---|---|---|
| On lui parle naturellement, en français | **OUI** — déjà le cas | couche 2 + profil |
| Elle se souvient de qui je suis, de mes décisions | **OUI** | `memoire/` (couche 3) |
| Elle agit : lit, écrit, cherche dans mes dossiers | **OUI** | couche 5 + garde-fous |
| **Elle sait énormément de choses de tête** | **NON. Irréductible.** | — |

**La quatrième est structurellement hors d'atteinte** et aucun réglage ne la rattrapera :
3 milliards de paramètres sur un processeur mobile de 2017 contre un très grand modèle sur
ferme de calcul. Ce n'est pas un écart de configuration, c'est un écart d'ordre de grandeur.
Le prétendre serait l'affirmation *sur nous* que le §13 signale comme la plus dangereuse.

**Ce qui la remplace, et qui vaut mieux sur son terrain :** elle ne saura pas de tête, elle
saura **où chercher dans les documents de Chaima**. Sur le domaine de Chaima, un système qui
cite ses fiches datées bat un très grand modèle qui ne les a jamais lues. **Le choix réel
n'est pas « Claude ou pas Claude » : c'est généraliste médiocre ou spécialiste fiable.**

**« Tout lui demander » est précisément ce qui ne marche pas**, et c'est démontré sur ses
propres données le même jour : deux questions de droit, deux échecs, une institution inventée
(`../mesure/JEU-D-OR.md`). Un généraliste local est un généraliste qui invente partout.

**« Autonome mais surveillée » : attente RETENUE telle quelle.** C'est exactement l'
architecture déjà en place — 3 sentinelles, jeu d'or, journal d'apprentissage, règles
apprises, remontée Drive. Sur ce point Chaima avait raison avant moi ; rien à corriger.

## Le temps de Chaima — MESURÉ, faute d'avoir pu être estimé (2026-09-16)

**Chaima, 2026-09-16 :** *« ce que je pourrais faire à travers le temps que j'ai, je ne peux
pas estimer. »* Réponse honnête, et **information en soi** : un temps régulier s'estime. Un
temps qui ne s'estime pas est généralement un temps **irrégulier**.

Plutôt que de redemander, l'activité réelle a été **mesurée** sur les horodatages git — une
donnée qui existait déjà et que personne n'avait regardée.

### Ce que disent les horodatages (`git log --all --since="8 weeks ago"`)

**6 jours actifs sur 56.** Amplitude du premier au dernier commit de chaque jour :

| Jour | Amplitude | Commits |
|---|---|---|
| 2026-08-10 | instantané | 1 |
| 2026-09-06 | 20h41 → 21h23 — **42 min** | 17 |
| 2026-09-10 | 10h22 → 14h08 — **3 h 46** | 5 |
| **2026-09-11** | 10h02 → 21h19 — **11 h 17** | 40 |
| 2026-09-14 | 18h50 → 20h44 — **1 h 54** | 32 |
| 2026-09-16 | 12h25 → 16h11 — **3 h 46** (en cours) | 19 |

**Total ≈ 21 h 30 sur 8 semaines.**

### Les deux lectures, toutes deux exactes — et c'est le point

| Fenêtre | Moyenne |
|---|---|
| Les 8 semaines | **≈ 2 h 40 / semaine** |
| Les 11 derniers jours (5 des 6 jours actifs) | **≈ 13 h / semaine** |

**Le temps de Chaima n'est pas un débit hebdomadaire. Ce sont des rafales.** Cinq des six
jours actifs tiennent dans les onze derniers jours ; avant, presque rien. Aucune moyenne ne
décrit honnêtement ça — voilà pourquoi elle ne pouvait pas l'estimer. **Elle avait raison de
ne pas répondre par un chiffre.**

**Forme typique d'une rafale : 2 à 4 heures.** Une seule journée à 11 h, isolée.

### Réserves, à ne pas perdre de vue

1. **L'amplitude est un MAJORANT, pas du temps de travail.** Elle inclut les pauses. Le temps
   réellement passé est inférieur — inconnu de combien.
2. **Les commits sont produits par un agent**, pas par Chaima. Ils ne mesurent sa présence que
   parce qu'une session ne tourne pas sans elle. Proxy, pas mesure directe.
3. **Ce dépôt seulement.** Ce qu'elle fait ailleurs n'apparaît pas.
4. Verdict §13 : **PLAUSIBLE, fiabilité ÉLEVÉE** sur la *forme* (irrégulière, par rafales de
   2-4 h) ; **NON VÉRIFIÉ** sur le *volume* réel.

### Ce que ça change pour D-001 — c'est décisif

**Une personne qui travaille par rafales irrégulières de 2 à 4 heures ne peut pas tenir
plusieurs fronts.** Chaque reprise commence par se rappeler où on en était. Avec 38 branches
et une quinzaine de projets, une part importante de chaque rafale est consommée **avant** que
le travail ne commence.

**Et ça nomme enfin la valeur réelle d'ATLAS**, qui n'était jusqu'ici qu'une intuition :
sa fonction n'est ni d'écrire du code, ni de savoir des choses — **c'est de rendre la reprise
quasi gratuite.** Reprendre en cinq minutes au lieu d'une heure, sur un temps en rafales,
n'est pas un confort : **c'est ce qui décide si la rafale produit quelque chose ou pas.**

C'est exactement ce que l'arbitre recommandait — réduire le coût de décision — mais pour un
motif qu'il n'avait pas : non pas l'engorgement (réfuté), **la fragmentation**.

## Faits établis par une AUTRE session (branche `claude/charming-galileo-cqhkn1`, 2026-09-19)

**Étiquette : RELAYÉ** — lus dans le commit `5be0a03` de cette branche, **non revérifiés par
ATLAS**. Source déclarée : le CV de Chaima, lu dans son Drive à sa demande le 2026-09-19.

| Fait | Effet sur ATLAS |
|---|---|
| **Chaima est domiciliée en Région de Bruxelles-Capitale** (Schaerbeek), pas en Wallonie | **Corrige** tout raisonnement régional. Les dispositifs wallons (Airbag, chèques-entreprises, SAACE, SOWALFIN) sont **hors sujet**. |
| **Aucun diplôme de gestion**, toutes formations > 5 ans, **39 ans** | Sans effet à Bruxelles : **aucun dispositif bruxellois trouvé n'exige de diplôme de gestion**. Question close. |
| Dispositifs bruxellois réellement applicables | **Tremplin-indépendants** (fédéral) · **JobYourself** (coopérative d'activités, test 18 mois, allocations conservées) · **Prime indépendant Actiris 4 000 €** · **Prime Lancement d'entreprise** (60 %, plafond 7 500 €) |
| ⚠️ **Incompatibilité** | La prime Actiris est **refusée** si, dans les 2 ans précédents, on a bénéficié de **Tremplin** **ou** d'une **coopérative d'activités**. **Les trois voies s'excluent.** |

**Ce que ces faits impliquent, et qui n'est PAS encore confirmé (PLAUSIBLE, fiabilité
MODÉRÉE) :** Tremplin-indépendants et les primes Actiris s'adressent à des demandeurs d'emploi
ou allocataires. Si Chaima l'est, alors **l'option « indépendant à titre complémentaire » du
`DOSSIER-01` est fermée** — elle suppose une activité salariée principale. **C'était la
question bloquante n°1 du dossier ; elle est peut-être déjà résolue, mais seule Chaima peut le
confirmer.**

## Ce qui est NON VÉRIFIÉ — et le restera tant qu'elle ne l'aura pas dit

- **Son usage n°1**, le cas concret qui doit marcher en premier.
- **Budget argent** — jamais évoqué.
- **Exigence de confidentialité** : 100 % local, ou cloud toléré pour certaines tâches.
- **Où vivent ses données** sur la machine.

**Note sur le signal Drive, conservée exprès :** le `Guide_Examen_MQ06` laissait deviner
Windows, et **il se trouve que c'était juste**. Ça ne valide pas la déduction pour autant — la
preuve est venue de la capture d'écran, pas du document d'école. Une intuition confirmée par
hasard reste une intuition : c'est précisément quand elle tombe juste qu'on est tenté d'en
faire une méthode (R-009 maintenue).

## Ce qui a été cherché, et n'existe pas

- **2026-09-16** — Recherche dans le Drive de caractéristiques machine (RAM, VRAM, processeur,
  config) : **rien**. Cherché, pas supposé — la distinction compte.
