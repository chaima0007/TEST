# Charte de la chaîne « Veille, Brevets, Technologies & Capitaux »

> **Portée : transversale** (infrastructure de la chaîne, tous projets).
> Les analyses propres à un projet ne vont **pas** dans ce dépôt — voir §4 « Emplacements ».
> Créée le 2026-09-11-15h59 (Europe/Brussels).

## 1. Convention de nommage — obligatoire pour tout document créé par n'importe quel agent

```
AAAA-MM-JJ-HHhMM — [Projet] — [Catégorie] — [Sujet précis]
```

Horodatage réel obligatoire, jamais estimé :

```bash
TZ="Europe/Brussels" date '+%Y-%m-%d-%Hh%M'
```

**Le « sujet précis » est un sujet, pas un rapport d'exécution.** Un titre doit rester lisible dans une
liste de dossier. Les journaux existants du Drive (« boucle-caelum », juillet-août 2026) portent des
titres de 300 à 400 caractères qui embarquent le verdict complet, les hashs de commit et l'état de la
PR : ils sont illisibles, non triables, et violent cette convention. Le rôle BIBLIOTHÉCAIRE ne doit pas
reproduire ce motif.

## 2. Règles non négociables

- Zéro invention : aucun numéro de brevet, aucun statut, aucun chiffre fabriqué.
- Chaque affirmation sourcée et datée ; **« NON VÉRIFIÉ »** écrit noir sur blanc si non confirmé.
- Un document horodaté par trouvaille. Un document = un événement. **Ajout, jamais écrasement.**
- Toute analyse de brevetabilité ≠ conseil juridique définitif : **conseil en PI humain requis avant
  tout dépôt réel**.
- Toute trouvaille validée est préparée en contenu structuré : titre · résumé en 3 points · source ·
  verdict d'audit.
- **Read-back après création**, avant d'annoncer quoi que ce soit comme fait.
- Aucun agent ne merge, ne déploie, ne signe ni n'engage quoi que ce soit sans accord explicite de Chaima.

## 3. Règle de divulgation — la plus coûteuse à enfreindre

En Europe, **il n'y a pas de délai de grâce** (art. 54 CBE ; l'art. 55 ne couvre que la divulgation
abusive et les expositions officielles reconnues). Conséquences opérationnelles :

- Un `git push` vers un dépôt **public** est une divulgation. Elle détruit la nouveauté immédiatement
  et irrémédiablement.
- Une mise en ligne de page, un article, un post LinkedIn, une démo publique : même effet.
- Donc : **rien de ce qu'on envisage de breveter ne part dans un dépôt public avant le dépôt de la
  demande.** Les rôles PROTECTEUR et REMPART vérifient ce point à chaque passage entre agents.

## 4. Emplacements et sauvegarde

Règle générale : **Drive + dépôt GitHub (privé si sensible) + copie locale synchronisée**
(rappel de l'incident du 6 septembre : CaelumSwarm v0.2 perdu faute de sauvegarde ailleurs).

Contrainte constatée le 2026-09-11 : le dépôt `chaima0007/keywordmoneymaker` (Caelum Partners) est
**public**. Il ne peut donc **pas** servir de sauvegarde au « 🔒 Coffre confidentiel » ni à aucune
trouvaille sensible. **Un dépôt privé distinct est nécessaire avant tout dépôt GitHub de contenu
sensible.** En attendant : Drive + copie locale uniquement.

Séparation par projet, jamais mélangé : les analyses Caelum vont dans
`Caelum Partners/Veille & Opportunités/` au Drive, pas dans le dépôt d'un autre projet.

## 5. Audit périodique de la chaîne elle-même (rôle GARDIEN)

À chaque audit, consigner dans un document horodaté :
les 35 rôles fonctionnent-ils encore comme prévu ? · doublons apparus ? · rôle inactif sans raison ?

**Point de vigilance connu :** le dépôt Caelum contient déjà 29 agents dans `.claude/agents/` et un
`CLAUDE.md` maître avec son propre protocole (« DRIVE D'ABORD », qualité en 3 couches, chaîne de
vérification du code tiers). Plusieurs de ces agents recouvrent des rôles de cette chaîne. Le GARDIEN
et l'ARCHITECTE doivent traiter ce recouvrement comme un doublon à résoudre, pas comme deux systèmes
parallèles. Rien n'est fusionné ni supprimé sans accord de Chaima.
