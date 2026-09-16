# ATLAS — JEU D'OR

> **L'étape qu'on ne peut PAS rattraper après coup** (règle R-006).
> Sans mesure d'avant, « ça s'est amélioré » est une impression, pas un constat.

## À quoi ça sert, en une phrase

À répondre honnêtement à *« est-ce que mon IA est meilleure qu'il y a un mois ? »* — avec des
questions **identiques**, posées **avant** et **après** chaque changement. Sinon on compare le
souvenir d'une réponse avec l'impression d'une autre, et on se ment.

## Comment on le construit (quand l'ÉTAPE 0 sera close)

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

**Ce qui n'est PAS encore fait :** le jeu d'or lui-même. 20 à 30 questions réelles de Chaima,
avec les réponses attendues, à figer **avant** tout autre changement (R-006). Cette entrée est
une observation, pas un jeu d'or.
