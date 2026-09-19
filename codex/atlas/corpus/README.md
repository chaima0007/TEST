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

## Convention de nommage — OBLIGATOIRE, fixée le 2026-09-19 avant le premier document

**Constat du scout (Parcours 1, CAND-001) :** les outils RAG candidats citent **le nom du
fichier**, pas la date du document ; leur champ « date » est la date d'**ingestion**. Une fiche
juridique de 2024 ingérée en 2026 serait citée « 2026 ». **La date doit donc être dans le nom.**

    AAAA-MM-JJ — domaine — titre court — source.md

    2026-07-28 — droit-belge — don d'organes après décès — LLAM.md
    2019-04-04 — asbl — statuts Retrouve Ton Smile — Moniteur.md
    2026-09-16 — atlas — dossier encaissement Peppol — codex.md

- **La date est celle du DOCUMENT** (publication ou dernière mise à jour connue), jamais celle
  de l'ajout. Inconnue → `0000-00-00` et le document ne sert **pas** à répondre sur du droit.
- **Le domaine** est l'un des profils (`droit-belge`, `asbl`, `caelum`, `atlas`, …) : c'est ce
  qui empêche les mémoires de se mélanger (`sentinelle-derive`, dérive n°5).
- **En tête de fichier**, deux lignes : `Source : URL ou référence` · `Consulté le : AAAA-MM-JJ`.
- **Un document mis à jour = un nouveau fichier daté**, l'ancien reste et se marque `[PÉRIMÉ]`
  en tête de nom. On ne supprime pas (§10) : le RAG doit pouvoir dire « la version de 2024
  disait autre chose ».

## Ajouter un document — procédure

Les commandes exactes viendront avec l'outil retenu (Parcours 1 en cours). Les quatre temps
sont fixés :

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
