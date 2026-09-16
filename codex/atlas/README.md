# ATLAS — IA locale, privée, qui accumule

> **Statut : CONCEPTION. Rien n'est installé.** Le diagnostic matériel (ÉTAPE 0) n'a pas encore
> de réponses — aucun choix de modèle, de runtime ou de quantification ne peut être arrêté
> avant. Ce dossier contient la **gouvernance** du projet, qui elle ne dépend pas du matériel.
> Créé le 2026-09-16.

## Le principe de vérité, écrit une fois pour toutes

**Un LLM qui se ré-entraîne tout seul sur une machine perso n'existe pas.** Ce qui grossit,
c'est la **mémoire** et le **corpus**. C'est moins spectaculaire et beaucoup plus puissant :
un petit modèle bien alimenté bat un gros modèle qui répond de mémoire.

Toute phrase de l'Empire qui laisse entendre le contraire est une survente et se corrige avant
sortie (§13 — attention particulière aux affirmations **sur nous**).

## Le rangement — un type = un dossier = UN fichier vivant

    codex/atlas/
    ├── 00-ETAT-DU-PROJET.md      ← LE SEUL FICHIER À OUVRIR POUR REPRENDRE
    ├── ROUTAGE.md                ← où va quoi, aucune exception
    ├── snapshots/SNAPSHOTS.md    ← ce qui a CHANGÉ (§5)
    ├── audits/AUDITS.md          ← si c'est COHÉRENT (§5, §9)
    ├── erreurs/ERREURS-ATLAS.md  ← les incidents réels → remontés au Drive
    ├── apprentissage/            ← JOURNAL-APPRENTISSAGE.md · REGLES-APPRISES.md
    ├── memoire/                  ← PROFIL-CHAIMA.md · DECISIONS.md      ┐ la base
    ├── corpus/                   ← les documents que l'IA doit lire     ┘ qui grandit
    ├── mesure/JEU-D-OR.md        ← la preuve que ça s'améliore vraiment
    └── continuite/               ← RESTAURATION.md · SYNC-DRIVE.md

**On AJOUTE en tête du fichier existant. On ne crée jamais un fichier daté par événement** —
`audit-2026-09-16-v2.md` et sa descendance sont exactement ce qui entremêle les documents
(règle R-007).

Règle anti-bruit (§5) : rien n'a changé → **une ligne**, puis silence. Un rapport pour dire
qu'il n'y a rien à dire est une faute contre le protocole.

## « Inarrêtable » — la contradiction assumée

Une IA locale **n'est pas** inarrêtable : elle s'arrête quand la machine s'arrête. Ce qui peut
l'être, c'est la **connaissance** — 3 copies (machine, dépôt, Drive) et une restauration
**réellement testée**, parce qu'une sauvegarde jamais restaurée n'est pas une sauvegarde.
Tout est dans `continuite/RESTAURATION.md`.

## La boucle d'apprentissage — les 4 mécanismes

**1. Correction → règle.** Chaima corrige. L'agent écrit la règle dans `REGLES-APPRISES.md`
*dans le même tour*, avec la date et le motif. Les règles se relisent **avant** chaque tâche du
domaine concerné, pas « quand on y pense ». Une correction répétée deux fois = la boucle est
cassée = **incident** (`🔴 ERREURS.md` + Drive), pas un soupir.

**2. Corpus qui grossit.** Chaque document ajouté enrichit le RAG → réponses plus pointues
**sans changer le modèle**. Chaque fiche analysée produit une FICHE EXPERTISE (§4, §7) : le
principe appris, jamais le code copié. Elle va dans `/codex/expertise/`, qui est **transverse**
— ce qu'ATLAS apprend, tous les projets de l'Empire le savent.

**3. Mesure.** `atlas-mlops` tient le jeu d'or (20–30 questions réelles + réponses attendues,
figées **avant** le premier changement) et 5 indicateurs. Sans base de comparaison d'avant, on
ne mesure rien — on raconte.

**4. Palier avancé (LoRA/QLoRA).** Refusé par défaut. Quatre conditions cumulatives dans
`.claude/agents/atlas-finetuning.md`. Le fine-tuning enseigne un **style**, pas une
connaissance : vouloir qu'un modèle « connaisse » un document se traite par le RAG.

## Profils multi-secteurs — mémoires séparées

Un profil = un prompt système + **sa** mémoire + **ses** sources. Jamais un corpus commun où
tout se mélange : un profil « juriste » qui répond technique parce que le contexte a débordé
est une panne, pas une souplesse (`sentinelle-derive`, dérive n°5). Le profil est **choisi
explicitement** par Chaima, jamais deviné.

## Sécurité — les 3 sentinelles

| Sentinelle | Surveille | Question unique |
|---|---|---|
| `sentinelle-exfiltration` | ce qui **sort** de la machine | qu'est-ce qui sort, vers où, avec quoi dedans ? |
| `sentinelle-perimetre` | les **autres projets** de l'Empire | est-ce que je casse le travail d'un voisin ? |
| `sentinelle-derive` | la **dégradation lente** du système | répond-il mieux qu'il y a un mois sur les MÊMES questions ? |

Elles complètent — sans les remplacer — `sentinel-securite` (ce qui entre),
`conservateur-secrets` (ce qui fuit en clair) et `gardien-donnees` (RGPD).

## Remontée vers le Drive

**Source de vérité = ce dépôt.** Le Drive est la **copie consultable**, pas l'original : un
document Drive modifié à la main et divergeant du dépôt est un piège. Voir `continuite/SYNC-DRIVE.md`. Dossier Drive : **ATLAS — IA locale (Empire Chaima)**.

## Ce qui reste strictement humain sur ATLAS (§10)

Installer ou supprimer un logiciel sur la machine de Chaima · acheter du matériel · ouvrir un
port vers l'extérieur · autoriser une sortie de données · lancer un entraînement · supprimer
une entrée de mémoire, un document ou une branche · merger dans `main`.

**Un agent recommande. Chaima décide.**
