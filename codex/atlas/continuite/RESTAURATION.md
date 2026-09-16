# ATLAS — « INARRÊTABLE » : ce que ça veut dire vraiment

> Demande de Chaima (2026-09-16) : *« il doit être inarrêtable ».*
> Ce document existe pour tenir la promesse **au lieu de la répéter**.

## La contradiction, dite franchement

**Une IA locale n'est pas inarrêtable. C'est impossible et il faut le savoir maintenant.**
Elle s'arrête quand la machine s'éteint, quand le disque meurt, quand l'ordinateur est volé,
quand une mise à jour casse une dépendance. Promettre le contraire serait exactement
l'affirmation *sur nous* que le §13 signale comme la plus dangereuse — celle que personne ne
pense à sourcer.

**Ce qui peut être inarrêtable, c'est la connaissance.** Et ça, ce n'est pas un vœu : c'est
une mécanique, et elle se vérifie.

Formulé autrement : la machine est **remplaçable**, le corpus ne l'est pas. Tout l'effort va
donc là où la perte serait définitive.

## Les 3 copies — la règle qui rend la perte improbable

| Copie | Où | Contient | Perdue si |
|---|---|---|---|
| **1. Vivante** | la machine de Chaima | modèle, index, mémoire, corpus | disque mort, vol, incendie |
| **2. Versionnée** | dépôt git (branche ATLAS) | mémoire, règles, journaux, gouvernance — **jamais de données personnelles**, le dépôt est **public** | jamais, sauf suppression volontaire |
| **3. Consultable** | Drive | erreurs, réussites, règles | jamais, hors suppression du compte |

**Les trois ne tombent pas ensemble.** C'est toute la raison d'être du chiffre 3.

**Le modèle n'est PAS sauvegardé** — et c'est délibéré : il pèse des gigaoctets et se
re-télécharge. Ce qui est irremplaçable, ce sont la mémoire, les règles et le corpus, qui
pèsent quelques mégaoctets. Sauvegarder le lourd remplaçable au lieu du léger irremplaçable
est l'erreur classique.

## La règle qui fait la différence

> **Une sauvegarde jamais restaurée n'est pas une sauvegarde** (`responsable-continuite`).

Tant que la restauration n'a pas été **faite pour de vrai, au moins une fois**, la
sauvegarde est **NON VÉRIFIÉE** — pas « probablement bonne ». La plupart des sauvegardes qui
échouent le jour J étaient en place depuis des mois et n'avaient jamais été essayées.

## Le test de restauration — à faire une fois, puis une fois par trimestre

Il ne sera écrit **avec les commandes exactes** qu'une fois l'OS de Chaima connu (R-005 :
aucune commande sans savoir l'OS réel). La procédure, elle, est déjà fixée :

1. **Simuler la perte** : renommer le dossier de travail (ne **jamais** le supprimer — §10).
2. **Restaurer depuis la copie 2** : récupérer mémoire, règles et corpus depuis le dépôt.
3. **Re-télécharger le modèle** : il n'est pas sauvegardé, c'est prévu.
4. **Rejouer le jeu d'or** (`../mesure/JEU-D-OR.md`) : le système restauré répond-il **comme
   avant** ? C'est la seule preuve qui vaut. Un système qui redémarre mais répond moins bien
   n'est pas restauré, il est diminué.
5. **Consigner le résultat** dans `../snapshots/SNAPSHOTS.md`. Un échec va dans
   `../erreurs/ERREURS-ATLAS.md` **et** dans le Drive.

## Les 4 pannes qui arrêtent vraiment un système local

Nommées d'avance pour ne pas les découvrir en panique. Chacune a son responsable.

| Panne | Ce qui se passe | Qui la traite |
|---|---|---|
| **Disque plein** | l'index ne s'écrit plus, les réponses deviennent muettes ou fausses | `atlas-materiel` (surveiller l'espace **avant** d'ingérer) |
| **Mise à jour qui casse** | le runtime ne démarre plus après une mise à jour | `atlas-systemes-reseaux` (ne jamais mettre à jour un système qui marche sans raison, et savoir revenir en arrière) |
| **Surchauffe / ralentissement** | ça marche, mais c'est devenu inutilisable | `atlas-materiel` (mesurer après 10 min de charge, pas à froid) |
| **Corpus corrompu ou pollué** | les réponses se dégradent **sans message d'erreur** — la pire, parce qu'elle est silencieuse | `sentinelle-derive` (le jeu d'or est le seul détecteur) |

## Ce qui reste strictement humain (§10)

Supprimer quoi que ce soit · restaurer par-dessus des données existantes · acheter un disque
de sauvegarde. **Un agent prépare et vérifie. Chaima exécute.**
