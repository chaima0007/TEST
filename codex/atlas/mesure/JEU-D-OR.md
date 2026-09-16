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

*(Aucun. Le jeu d'or sera figé juste après l'installation de la couche 1, avant tout autre
changement. Le figer plus tard n'aurait aucune valeur : il n'y aurait plus d'« avant ».)*
