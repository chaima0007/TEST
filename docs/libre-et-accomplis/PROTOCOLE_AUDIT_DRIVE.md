# 📓 Protocole d'audit Drive — Libre & Accomplis

> **Règle d'or n°9.** Toute session de travail (humaine ou agent Claude) tient un
> journal d'audit sur le Drive, au fur et à mesure, horodaté à la minute,
> lisible par un tiers, sans redondance et sans doublons. Ce protocole est
> appliqué par l'orchestrateur et vérifié par les experts au même titre que
> les huit autres règles d'or.

## 0. Rôle de l'orchestrateur : regarder le Drive et agir en conséquence

Plusieurs agents travaillent en parallèle sur des services différents
(Libre & Accomplis, Caelum, La Loi Avec Moi, KMM/CompeteIQ…). Le Drive est
leur point de coordination. **Première action obligatoire de toute session,
pilotée par l'orchestrateur :**

1. Lister les fichiers récents du Drive.
2. Lire les LISEZ-MOI, fichiers d'erreurs et journaux **du service concerné**
   par la session (pas besoin de tout lire — chaque synopsis dit si le
   document concerne la session ou non, c'est son rôle).
3. Agir en conséquence : appliquer les règles déjà établies, reprendre les
   problèmes en attente, ne jamais refaire un travail déjà journalisé.

## 1. Arborescence Drive (unique, jamais dupliquée)

```
LibreEtAccomplis/
├── audit/           # journaux d'audit, un fichier par travail effectué, datés
├── presentation/    # présentation du projet pour un tiers (qualité "grande entreprise")
└── problemes/       # copies des problèmes signalés, à traiter dans l'ordre
```

- Chaque **service** a son propre dossier racine sur le Drive (celui-ci est
  celui de Libre & Accomplis) ; on n'écrit jamais l'audit d'un service dans
  le dossier d'un autre.
- **Avant toute création de dossier ou de fichier : rechercher s'il existe déjà.**
  On ne crée jamais un second dossier ou un second fichier pour le même usage.
- L'arborescence est plate et stable : on n'ajoute un dossier que pour un
  nouvel usage durable, pas pour une session.

## 2. Journal d'audit (dossier `audit/`)

- **Un audit par travail effectué** : chaque mission terminée (ou étape
  significative d'une longue session) est déposée sur le Drive pour que les
  collègues (Chaima et les autres agents — personne d'autre, le Drive est
  interne) sachent ce qui a été fait sans avoir à le redécouvrir.
- **Nommage** : `AAAA-MM-JJ HH:MM UTC — Type — Sujet (Service)`.
  Exemple : `2026-07-13 15:31 UTC — Journal d'audit — Session complète (Libre & Accomplis)`.
  Si un second fichier est nécessaire le même jour (le connecteur ne permet
  pas d'éditer un document existant), le suffixer : `— partie 2`.
  Deux fichiers ne couvrent **jamais** les mêmes actions.
- **Synopsis obligatoire** : chaque document commence par un bloc
  `Synopsis :` de 2 à 4 lignes — ce que contient le document, quel service
  est concerné, l'état (terminé / en cours / bloqué), et ce que le lecteur
  doit en faire. C'est le synopsis qui permet aux autres agents de savoir,
  sans ouvrir le document en entier, s'il les concerne.
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
