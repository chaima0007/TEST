# 📓 Protocole d'audit Drive — Libre & Accomplis

> **Règle d'or n°9.** Toute session de travail (humaine ou agent Claude) tient un
> journal d'audit sur le Drive, au fur et à mesure, horodaté à la minute,
> lisible par un tiers, sans redondance et sans doublons. Ce protocole est
> appliqué par l'orchestrateur et vérifié par les experts au même titre que
> les huit autres règles d'or.

## 1. Arborescence Drive (unique, jamais dupliquée)

```
LibreEtAccomplis/
├── audit/           # journaux d'audit, un fichier par session, datés
├── presentation/    # présentation du projet pour un tiers (qualité "grande entreprise")
└── problemes/       # copies des problèmes signalés, à traiter dans l'ordre
```

- **Avant toute création de dossier ou de fichier : rechercher s'il existe déjà.**
  On ne crée jamais un second dossier ou un second fichier pour le même usage.
- L'arborescence est plate et stable : on n'ajoute un dossier que pour un
  nouvel usage durable, pas pour une session.

## 2. Journal d'audit (dossier `audit/`)

- **Nommage** : `AAAA-MM-JJ — Journal d'audit (sujet de la session)`.
  Si une session doit produire un second fichier le même jour (le connecteur
  ne permet pas d'éditer un document existant), le suffixer : `— partie 2`.
  Deux fichiers ne couvrent **jamais** les mêmes actions.
- **Horodatage** : chaque entrée commence par l'heure à la minute, en UTC,
  dans l'ordre chronologique strict.
- **Contenu d'une entrée** : ce qui a été fait, pourquoi, la preuve
  (commit, PR, lien). Les erreurs rencontrées et leur résolution sont
  consignées — un audit qui ne montre que les succès n'est pas un audit.
- **Non-redondance** : le journal référence les sources de vérité (commits
  GitHub, documents) au lieu d'en recopier le contenu.
- **Clôture** : chaque journal se termine par un tableau d'état
  (élément / statut / preuve) et la liste de ce qui reste en attente.

## 3. Présentation du projet (dossier `presentation/`)

- Un document de présentation **autoporteur** : un dirigeant ou un partenaire
  qui découvre le projet doit pouvoir le comprendre et le présenter sans
  aucun autre contexte (standard attendu : qualité d'une grande entreprise).
- Contenu minimal : le problème, la solution, le public cible, l'architecture
  en termes simples, l'état d'avancement daté, la roadmap, les liens vers le
  dépôt et l'audit.
- **Un seul document maître**, mis à jour par remplacement versionné
  (`— v2`, `— v3` avec date) ; l'ancienne version est conservée mais le titre
  indique clairement laquelle est courante.

## 4. Problèmes inter-sessions (dossier `problemes/`)

- Les autres sessions Claude (le « collègue Claude ») déposent des fichiers de
  problèmes et de règles (ex. `🔴 ERREURS — … (à corriger dans l'ordre)`,
  `📖 LISEZ-MOI — Règles du journal`).
- **Début de session obligatoire** : lister les fichiers récents du Drive,
  lire les LISEZ-MOI et fichiers d'erreurs pertinents, et en tenir compte
  avant d'agir. Les conventions déjà établies priment sur les préférences
  de la session en cours.
- Tout problème détecté pendant une session et non résolu est consigné dans
  `problemes/` (ou dans le fichier d'erreurs existant du projet concerné),
  avec date, contexte et impact — jamais silencieusement abandonné.

## 5. Articulation avec le reste du système

- Ce protocole complète (ne remplace pas) la journalisation technique de
  l'orchestrateur (audit log → Elasticsearch en production).
- Le registre des feedbacks experts (`modeles/feedback_experts.csv`) reste la
  source de vérité des corrections d'agents ; le journal Drive y renvoie.
- La checklist de déploiement ajoute un point : **journal d'audit de la
  session à jour sur le Drive**.
