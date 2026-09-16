# ATLAS — CORPUS (la base qui grandit)

> Demande de Chaima (2026-09-16) : *« je veux une base de données qui grandit avec le temps ».*
> C'est **ici** que ça grandit — pas dans les poids du modèle.

## Ce que ce dossier contient, et ne contient pas

**Contient :** les documents que l'IA doit pouvoir **lire pour répondre** — notes, fiches,
procédures, contrats types, documentation. Chacun **daté**, avec sa provenance.

**Ne contient pas :** des données personnelles (le dépôt est **public** — 🔴 ERR-015), des
secrets, des brouillons, des doublons, ni un document dont on ignore d'où il vient.

## Pourquoi on commence en fichiers Markdown, et pas en « vraie » base de données

C'est un choix, pas un retard. Un fichier texte se **lit à l'œil**, se **corrige à la main**,
et se répare sans outil quand ça casse. Une base vectorielle qui se corrompt à 200 documents,
pour quelqu'un qui débute, c'est un mur.

**Le passage à une base vectorielle locale se décide sur un fait, pas sur une envie.** Le
déclencheur : quand retrouver le bon extrait devient lent ou imprécis — mesuré sur le jeu d'or
(`../mesure/JEU-D-OR.md`), pas ressenti. `atlas-rag-memoire` propose alors le composant, qui
passe par le Parcours 1 (`scout` → `guardian-licences` + `sentinel-securite`).

**La migration est prévue dès maintenant** : des fichiers datés et structurés s'ingèrent dans
n'importe quelle base vectorielle. L'inverse — récupérer proprement du contenu d'une base mal
remplie — est beaucoup plus douloureux. On ne perd donc rien à commencer simple.

## Ajouter un document — procédure

Elle sera écrite **avec les commandes exactes** une fois l'OS connu (R-005). Les quatre temps
sont déjà fixés :

1. **Dater et sourcer** : d'où vient ce document, de quand.
2. **Vérifier qu'il n'existe pas déjà** : un doublon dégrade les réponses, il ne les enrichit
   pas. Croissance ≠ amélioration.
3. **Passer `gardien-donnees`** s'il touche à des personnes.
4. **Mesurer** : le jeu d'or est-il meilleur, égal ou moins bon après l'ajout ? Un ajout qui
   dégrade se retire.

## Un piège qui se voit rarement venir

**Un document daté de 2024 et un de 2026 qui se contredisent : le RAG ne tranche pas, il
ressort les deux** — avec la même assurance. D'où la date obligatoire à l'ingestion, et le
marquage **périmé** plutôt que la suppression.
