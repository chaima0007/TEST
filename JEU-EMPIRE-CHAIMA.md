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
de minutes. L'accueil annonce ce que coûte la journée avant que tu commences
(« La journée : 16 questions, environ 11 min »), puis où tu en es
(« 7 / 16 aujourd'hui »). L'objectif est fixé à la première question et ne bouge
plus. Quand il est atteint, le bouton cesse de pousser à rejouer et le
récapitulatif propose « Terminé pour aujourd'hui » — c'est fait, tu peux poser
la tablette.

Tu composes chaque commande en tapant sur des blocs. Un bloc déjà posé se retire
en tapant dessus. En cas d'erreur, le jeu explique le concept en jeu, pas
seulement « faux ».

Sur une commande que tu n'as **jamais vue**, un bouton « je ne l'ai jamais vue —
montre-moi » te la donne avant l'échec : tu la recomposes ensuite avec les
blocs. Elle rapporte moins et revient dès le lendemain — c'est voulu, se
tromper sur ce qu'on n'a jamais croisé n'apprend rien.

Après chaque bonne réponse, la commande est **découpée et nommée** : quel
morceau est la commande, lequel est une option, lequel est un chemin. C'est ce
qui permet de transposer à une autre commande au lieu d'apprendre par cœur.

## Ce qu'il y a dedans

- **12 mondes**, 217 commandes : navigation, permissions, comptes, processus et
  services, paquets, réseau, texte, archivage et logs, disques et swap, console,
  SSH sur serveur distant (Ubuntu), pare-feu firewalld.
- **12 boss** : une panne réaliste par monde, en quatre ou cinq commandes
  enchaînées. Ils s'ouvrent à 70 % du monde et le jeu te prévient quand l'un
  d'eux devient disponible. Le gros gain est pour la première victoire et pour
  le premier sans-faute ; les rejeux restent utiles mais ne rapportent plus une
  journée entière.
- **Révision espacée** : une commande ratée revient tout de suite, une commande
  sue revient de plus en plus tard, puis passe en entretien toutes les deux
  semaines.
- **Fiche « mes points faibles »** : journal cumulatif de toutes tes erreurs,
  exportable en texte, avec un bouton pour t'entraîner uniquement là-dessus.
- **Simulation d'examen** : 12 questions chronométrées, sans indice, une seule
  tentative. S'ouvre à 60 commandes réussies. Les dix derniers scores sont
  conservés pour voir la courbe. Un examen raté ne coûte jamais d'XP : les
  points gagnés question par question restent acquis, le score n'ajoute qu'un
  bonus (à partir de 60 %, puis de 80 %). Tu ne risques rien à le tenter tôt.

## Réglages

- **Mode de saisie** : Blocs (par défaut) · Progressif (clavier sur les commandes
  déjà sues) · Clavier libre. Les deux derniers tolèrent la dictée vocale :
  « cat slash etc slash passwd » est accepté.
- **Longueur d'une série** : 5, 8 ou 12 questions.
- **Animations réduites**, si l'affichage rame.
- **Mode examen visible**, pour masquer le bouton.
- **Taille du texte** : Normal · Grand · Très grand — pour lire à bout de bras
  ou en plein soleil. Rien ne déborde de l'écran, même en très grand.
- **Lecture à voix haute** : un bouton fait lire la consigne, puis
  l'explication, par la voix française de la tablette. Fonctionne hors-ligne.
- **Retour vibrant** : une vibration courte quand c'est juste, une double quand
  c'est faux. Utile quand l'écran est difficile à lire.

## Sauvegarder ta progression

La progression est enregistrée dans le navigateur de la tablette. **Elle
disparaît si tu vides les données de navigation.** Dans Réglages :

- **Exporter ma progression** écrit un fichier `.json` à garder.
- **Importer un fichier** la restaure, sur la tablette ou ailleurs.

Fais-le de temps en temps, surtout avant l'examen.

## Fiches à imprimer

Quatre fiches A4 complètent le jeu (équivalences Rocky/Ubuntu, firewalld,
réseau et SSH, disques et swap) : sources dans `fiches/`.

## Le rythme, honnêtement

Le jeu fait passer la consolidation avant la découverte : quand des rappels
s'accumulent, il ouvre moins de commandes nouvelles. À deux séries par jour,
compte environ **90 commandes vues et 40 ancrées au bout d'un mois**, les
premières ancrées vers le douzième jour. Pour aller plus vite avant une
échéance, allonge la série dans les réglages (12 questions) ou enchaîne une
deuxième série — l'objectif du jour s'adapte.

## Pour qui développe dessus

- `npm run test:jeu` — logique de correction, révision espacée, contenu
  (20 153 assertions, sans dépendance).
- `npm run test:jeu:parcours` — 30 jours d'usage simulé : arriéré de rappels,
  ancrage, ouverture des mondes et de l'examen.
- `npm run test:jeu:ui` — 188 vérifications dans un vrai navigateur
  (Playwright) : parcours complet, retour du lendemain, export et import de la
  sauvegarde, tablette sans stockage, barème d'examen et de boss, anatomie des
  commandes, voix, vibration et taille du texte.

Tout le contenu vit dans les tableaux `EX` (exercices) et `BOSS` (boss) du bloc
`CORE` du fichier HTML. Un exercice déclare sa solution en blocs, ses blocs
pièges, l'explication de chaque piège et le concept en jeu ; les tests refusent
un exercice dont un piège n'est pas expliqué.
