# Empire Chaima — Terminal

Jeu d'entraînement aux commandes Linux (Rocky 9, avec un labo Ubuntu/Debian).
Un seul fichier : `public/empire-chaima-linux.html`. Aucune installation, aucun
compte, aucune connexion nécessaire une fois le fichier ouvert.

## L'ouvrir

**Sur la tablette, hors-ligne** — télécharge `public/empire-chaima-linux.html`,
puis ouvre-le avec ton navigateur (dans l'application Fichiers : appui long →
Ouvrir avec → Chrome). Ajoute-le à l'écran d'accueil pour le retrouver d'un tap :
menu ⋮ → « Ajouter à l'écran d'accueil ».

**Sur un ordinateur** — double-clic sur le fichier.

## Une séance

Le bouton **Jouer** lance la série du jour : quelques rappels arrivés à échéance,
tous mondes confondus, plus des commandes nouvelles. Huit questions, une dizaine
de minutes. Quand l'objectif du jour est atteint, le récapitulatif propose
« Terminé pour aujourd'hui » — c'est fait, tu peux poser la tablette.

Tu composes chaque commande en tapant sur des blocs. Un bloc déjà posé se retire
en tapant dessus. En cas d'erreur, le jeu explique le concept en jeu, pas
seulement « faux ».

## Ce qu'il y a dedans

- **12 mondes**, 212 commandes : navigation, permissions, comptes, processus et
  services, paquets, réseau, texte, archivage et logs, disques et swap, console,
  SSH sur serveur distant (Ubuntu), pare-feu firewalld.
- **12 boss** : une panne réaliste par monde, en quatre ou cinq commandes
  enchaînées. Ils s'ouvrent à 70 % du monde.
- **Révision espacée** : une commande ratée revient tout de suite, une commande
  sue revient de plus en plus tard, puis passe en entretien toutes les deux
  semaines.
- **Fiche « mes points faibles »** : journal cumulatif de toutes tes erreurs,
  exportable en texte, avec un bouton pour t'entraîner uniquement là-dessus.
- **Simulation d'examen** : 12 questions chronométrées, sans indice, une seule
  tentative. S'ouvre à 60 commandes réussies. Les dix derniers scores sont
  conservés pour voir la courbe.

## Réglages

- **Mode de saisie** : Blocs (par défaut) · Progressif (clavier sur les commandes
  déjà sues) · Clavier libre. Les deux derniers tolèrent la dictée vocale :
  « cat slash etc slash passwd » est accepté.
- **Longueur d'une série** : 5, 8 ou 12 questions.
- **Animations réduites**, si l'affichage rame.
- **Mode examen visible**, pour masquer le bouton.

## Sauvegarder ta progression

La progression est enregistrée dans le navigateur de la tablette. **Elle
disparaît si tu vides les données de navigation.** Dans Réglages :

- **Exporter ma progression** écrit un fichier `.json` à garder.
- **Importer un fichier** la restaure, sur la tablette ou ailleurs.

Fais-le de temps en temps, surtout avant l'examen.

## Fiches à imprimer

Quatre fiches A4 complètent le jeu (équivalences Rocky/Ubuntu, firewalld,
réseau et SSH, disques et swap) : sources dans `fiches/`.

## Pour qui développe dessus

- `npm run test:jeu` — logique de correction, révision espacée, contenu
  (19 835 assertions, sans dépendance).
- `npm run test:jeu:ui` — parcours complet dans un vrai navigateur (Playwright).

Tout le contenu vit dans les tableaux `EX` (exercices) et `BOSS` (boss) du bloc
`CORE` du fichier HTML. Un exercice déclare sa solution en blocs, ses blocs
pièges, l'explication de chaque piège et le concept en jeu ; les tests refusent
un exercice dont un piège n'est pas expliqué.
