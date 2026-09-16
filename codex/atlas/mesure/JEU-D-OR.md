# ATLAS — JEU D'OR

> **L'étape qu'on ne peut PAS rattraper après coup** (règle R-006).
> Sans mesure d'avant, « ça s'est amélioré » est une impression, pas un constat.

## À quoi ça sert, en une phrase

À répondre honnêtement à *« est-ce que mon IA est meilleure qu'il y a un mois ? »* — avec des
questions **identiques**, posées **avant** et **après** chaque changement. Sinon on compare le
souvenir d'une réponse avec l'impression d'une autre, et on se ment.

## ✅ CONSTRUIT — `JEU-D-OR-QUESTIONS.md`, figé le 2026-09-16

24 questions, 5 familles, barème sur 33 points. **D (hors corpus) et E (pièges d'invention)
comptent double** — une erreur y est invisible pour qui ne connaît pas déjà la réponse.

**Découverte qui a façonné la structure :** le modèle a refusé d'inventer un **chiffre** puis
inventé une **institution** dans la même réponse. Une famille par **type** d'invention :
chiffre · date · institution · article de loi · citation.

## Le principe de construction (conservé pour mémoire)

20 à 30 questions **réelles** de Chaima — celles qu'elle poserait vraiment, pas des questions
inventées pour être réussies. Pour chacune : la question, la réponse attendue, et la source
qui le prouve.

Il faut un mélange, sinon la mesure ment :

- des questions **faciles** (le système ne doit jamais les rater) ;
- des questions **dures** (c'est là que la quantification et le découpage se voient) ;
- des questions **dont la réponse est dans le corpus** (teste le RAG) ;
- des questions **dont la réponse n'y est pas** — le système doit répondre **« je ne sais
  pas »**. C'est le test le plus important : un système qui invente plutôt que d'avouer son
  ignorance est dangereux, pas serviable.

## Les 5 indicateurs (`atlas-mlops`)

| Indicateur | Ce qu'il attrape |
|---|---|
| Réponses correctes / jeu d'or | la qualité brute |
| Réponses **sourcées** (cite un document du corpus) | l'invention déguisée |
| Questions autrefois ratées, **maintenant réussies** | le progrès **réel** |
| **Corrections répétées** | la mémoire qui ne retient pas |
| Délai de première réponse utile | l'utilisabilité, chronométrée |

**Jamais de pourcentage** (§13) : FAIBLE / MODÉRÉE / ÉLEVÉE. Chaque relevé est **daté** et dit
sur quelle version du modèle, de l'index et du prompt il a été pris — sinon deux relevés ne
sont pas comparables.

**Le 4e indicateur prime sur tous les autres.** Si Chaima corrige deux fois la même chose, le
système n'apprend pas, quel que soit le volume de documents produits. C'est un incident :
`../erreurs/ERREURS-ATLAS.md` + Drive.

## Relevés

### 2026-09-16 — Deux questions de droit belge : le modèle SANS corpus

Modèle `qwen2.5:3b`, sans aucun corpus. **C'est la mesure de référence « avant »** — celle à
laquelle toutes les versions futures seront comparées. Elle ne se refera jamais.

#### Q-001 — « Différence entre une ASBL et une SRL en Belgique, en 4 phrases »

| | |
|---|---|
| **Débit** | 7,75 tokens/s · 341 tokens en 44 s |
| **Verdict** | **ÉCHEC** — plausible en surface, faux sur le fond |
| **Sourcé ?** | **NON** — aucune source, aucun article de loi |
| **Consigne suivie ?** | **NON** — 4 phrases demandées, ~8 produites |

Erreurs relevées (**corrections à confirmer sur source primaire**, voir réserve plus bas) :

1. **« actionnaires » pour une ASBL.** Une ASBL n'a pas d'actionnaires : elle a des **membres**.
   Erreur de vocabulaire qui révèle une erreur de concept.
2. **« actionnaires » pour une SRL.** Une SRL a des **associés** ; ce sont les SA qui ont des
   actionnaires. Le modèle emploie un seul mot pour trois réalités.
3. **« avantages fiscaux […] en raison de l'étiquetage "SRL" sur l'immatriculation »** —
   phrase **vide de sens**. Un raisonnement inventé, pas une approximation.
4. **« ASBL idéale pour des activités non commerciales »** — vision **antérieure à la réforme
   de 2019** (Code des sociétés et des associations) : une ASBL peut exercer des activités
   commerciales tant qu'elle ne **distribue** pas de bénéfices. Le modèle raisonne sur un
   droit périmé, sans le signaler.
5. **« conseil d'administration indépendant »** — « indépendant » est ajouté de nulle part.
6. **Omission majeure** : la suppression du capital minimum de la SRL par la réforme de 2019,
   qui est l'une des vraies différences pratiques.

#### Q-002 — « Date limite de dépôt des comptes d'une ASBL belge, et montant exact de l'amende »

| | |
|---|---|
| **Débit** | 7,29 tokens/s · 321 tokens en 44 s |
| **Verdict** | **ÉCHEC PARTIEL** — un point réussi, deux inventions |
| **Sourcé ?** | **NON** |

- ❌ **« 31 décembre de la deuxième année suivante »** — **inventé**. Un délai de deux ans est
  invraisemblable. L'ordre de grandeur réel est de quelques mois après la clôture.
- ❌ **« La Commission des Comptes »** — **cette institution n'existe pas**. Le modèle a
  fabriqué un organisme officiel, puis lui a prêté un pouvoir de sanction. C'est la pire
  espèce d'hallucination : **vérifiable, et invérifiable par qui ne sait pas déjà**.
- ✅ **« il n'existe pas de montant précis en euros »** — **refus d'inventer un chiffre.**
  Le seul point réussi des deux réponses, et ce n'est pas un détail : c'est précisément le
  comportement que le jeu d'or doit récompenser.

#### Ce que ces deux relevés établissent

**Le danger n'est pas que le modèle se trompe. C'est qu'il se trompe exactement du même ton
qu'il a raison.** Les réponses sont bien écrites, structurées, nuancées — et fausses. Sur du
droit, une personne qui ne connaît pas déjà la réponse **ne peut pas faire la différence**.

**Réserve que je m'applique à moi-même (§13) :** les corrections ci-dessus sont écrites de
mémoire par un agent. Elles sont **PLAUSIBLES, fiabilité ÉLEVÉE**, et **NON VÉRIFIÉES** tant
qu'une source primaire datée (Code des sociétés et des associations, site du SPF Justice,
Moniteur belge) ne les a pas confirmées — travail de `atlas-chercheur-sources`. Remplacer une
invention par une affirmation non sourcée ne serait pas un progrès, seulement un changement
d'auteur. **C'est exactement pourquoi le corpus est la seule sortie : pour que ni le modèle,
ni moi, n'ayons le dernier mot — seulement le document daté.**

### 2026-09-16 — Premier contact, et première hallucination observée

**Contexte :** `qwen2.5:3b` sur Ollama. Chaima a collé par mégarde la commande
`ollama run qwen2.5:3b --verbose` **dans** l'invite du modèle, au lieu d'une question. Le
modèle a donc reçu cette ligne comme une question.

**Ce qu'il a répondu :** que la commande était **fautive sur trois points**, et qu'il fallait
écrire `ollama run qwen-2.5-v1:3b --verbose`.

**Ce qui est vrai :** la commande de Chaima était **correcte** — elle venait de télécharger
le modèle avec. Et `qwen-2.5-v1:3b` **n'existe pas**. Le modèle a inventé un nom de modèle,
inventé trois défauts, et présenté le tout avec une assurance parfaite, en anglais alors que
le projet est en français.

**Pourquoi c'est le relevé le plus important du projet, et pas un incident :**

1. **C'est la démonstration, en direct et sur ses propres données, de ce qui fonde ATLAS.**
   Un modèle de 3 milliards de paramètres **ne sait pas**, il **produit du plausible**. Il ne
   dira jamais « je ne sais pas » spontanément. Nourri par le corpus, il cite ; laissé à sa
   mémoire, il invente — et rien dans le ton ne distingue les deux cas.
2. **C'est le 4e type de question du jeu d'or** (celles dont la réponse n'est pas dans le
   corpus) qui vient de tomber toute seule, au premier échange. Il doit y en avoir dans le
   jeu d'or définitif : **un système qui invente plutôt que d'avouer son ignorance est
   dangereux, pas serviable.**
3. **Ça referme le débat sur le fine-tuning.** Entraîner ce modèle sur les données de Chaima
   le rendrait plus sûr de lui, pas plus juste. Le palier était déjà fermé pour motif
   matériel (`../memoire/MACHINE.md`) ; il l'est désormais aussi pour motif démontré.

**Mesure de débit associée :** `eval rate` **8,10 tokens/s** — à froid, premier échange.
Détail et réserves : `../memoire/MACHINE.md`.

**FAIT depuis** : le jeu d'or est **figé** — 24 questions en 5 familles, barème sur 33 points :
`JEU-D-OR-QUESTIONS.md`. Les questions ne changeront plus (on peut en ajouter, jamais en
retirer ni en modifier : modifier une question détruit toute comparaison passée).
