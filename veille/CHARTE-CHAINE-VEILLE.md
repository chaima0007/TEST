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

---

# DÉCISIONS DE CHAIMA DU 2026-09-11 — ACCEPTÉES ET INTÉGRÉES

## 6. Trois rôles ajoutés (portant la chaîne à 38 rôles)

### LE DÉPOSANT — propriété intellectuelle opérationnelle
Possède les titres qui s'appliquent **réellement**, là où les 35 rôles d'origine ne regardaient que le
brevet :
- **Marque** : recherche d'antériorité BOIP (Benelux) et EUIPO, puis dépôt (classes 35 et 42 pour du
  conseil et des services technologiques).
- **Droit d'auteur** : fichier `LICENSE` explicite et en-têtes de copyright sur chaque dépôt. Un dépôt
  public **sans licence** laisse les tiers dans le flou sur leurs droits — c'est le cas aujourd'hui du
  dépôt Caelum.
- **Droit *sui generis* des bases de données** (Dir. 96/9/CE) : fait documenter l'investissement
  substantiel, qui est la **condition** de la protection. Sans cette documentation, le droit ne
  s'exerce pas.
- Reprend les angles morts déjà relevés par l'agent `completeur-angles-morts` (qui cite déjà « marque
  BOIP ») au lieu de les redécouvrir.

*Interdit :* ne dépose jamais rien. Prépare le dossier, chiffre le coût, et s'arrête à la décision de
Chaima. Un conseil en PI humain reste requis avant tout dépôt réel.

### L'HORLOGER — chronologie probatoire
Construit et tient la preuve datée, sans laquelle les droits ci-dessus ne sont pas opposables :
- Horodatage de l'investissement dans la base de données (temps passé, vérifications, mises à jour).
- Date de première création et de première divulgation de chaque élément — établie sur l'historique
  git **complet**, jamais sur un clone superficiel.
- **i-DEPOT du BOIP** : instrument réel et bon marché pour **dater une idée sans la publier**. À
  privilégier chaque fois qu'il faut prouver une antériorité sans déclencher de divulgation.

*Interdit :* ne date jamais rien de façon approximative. Une date non vérifiée s'écrit « NON VÉRIFIÉ »,
jamais estimée en silence.

### L'ÉLAGUEUR — condition d'arrêt
Seul rôle habilité à **tuer** une piste et à libérer les ressources. Les 35 rôles d'origine poussaient
tous en avant ; le CONTRADICTEUR objecte mais ne clôt rien.
- Déclare une piste morte, par écrit, avec le motif et la date.
- Interdit sa réouverture sans élément nouveau **nommé**.
- Surveille le signal d'alarme : plusieurs cycles consécutifs sans changement d'état (voir §7.1).

*Interdit :* ne supprime aucun document. Une piste morte est archivée et datée, pas effacée. Rien n'est
supprimé définitivement sans l'accord de Chaima.

## 7. Cinq améliorations système adoptées

### 7.1 Condition d'arrêt — anti-boucle (la plus importante)
**Constat daté :** le Drive contient une trentaine de documents de juillet-août 2026 quasi identiques
(« boucle-caelum »), tous porteurs du même message : « backlog SATURÉ → 0 nouvelle pièce · SILENCE ·
rien de neuf ». La chaîne tournait à vide en produisant du bruit, et un faux positif y a survécu
environ deux semaines sans être détecté.

**Règle :** *aucun document nouveau quand l'état est inchangé.*
- État inchangé → on met à jour **un seul** document d'état courant, et on se taise.
- On n'escalade et on ne crée un document horodaté **que sur changement d'état réel**.
- Trois cycles consécutifs sans changement → l'ÉLAGUEUR se saisit du dossier et tranche : la piste
  est-elle vivante, ou la surveillance doit-elle cesser ?

### 7.2 Articulation avec le parc d'agents existant
La chaîne veille **ne se place pas à côté** des 29 agents du dépôt Caelum : elle se branche **dessous**,
comme un domaine. `meta-orchestrateur` reste le seul chef d'orchestre ; le CHEF D'ORCHESTRE de la
chaîne est son délégué pour le domaine veille/PI/capitaux et ne tranche rien hors de ce domaine.
Toute validation passe par la **qualité en 3 couches déjà écrite** au `CLAUDE.md` §2 ; tout code tiers
par la **chaîne §2 bis existante**. On ne réinvente aucune procédure en parallèle.
Table de correspondance complète : Drive, « Synergies inter-agents », document du 2026-09-11-16h20.

### 7.3 Dépôt privé pour le Coffre confidentiel
Le dépôt Caelum étant **public**, il ne peut pas sauvegarder le « 🔒 Coffre confidentiel ». Tant qu'un
dépôt privé distinct n'existe pas : **Drive + copie locale uniquement**, et rien de sensible sur GitHub.

### 7.4 Discipline de nommage — plafond
La convention du §1 est complétée d'un plafond, parce que les titres existants atteignent 300 à 400
caractères et embarquent verdict, hashs de commit et état de PR :
- **titre complet ≤ 120 caractères** ; **« sujet précis » ≤ 60 caractères**.
- Le sujet nomme un **sujet**, pas un rapport d'exécution. Le verdict va dans le document, pas dans le
  titre. Un titre doit rester lisible et triable dans une liste de dossier.

### 7.5 Cadence de couverture des offices — première vague
Documenter 22 offices pour chaque trouvaille n'est pas soutenable, et c'est surtout **redondant** :
Espacenet et WIPO Patentscope donnent déjà les **familles internationales**, donc les équivalents
nationaux d'un même brevet.
- **Première vague (5 offices) :** OEB/Espacenet · WIPO Patentscope · USPTO · DPMA · CNIPA.
- **Descente au registre national** (les 17 autres juridictions) **seulement** quand une famille
  précise le justifie — et c'est alors documenté dans le dossier du pays concerné.
- Les 22 dossiers de la bibliothèque restent créés et disponibles : c'est la **cadence** qui est
  bornée, pas la couverture.

## 8. Contradiction de normes trouvée le 2026-09-11 — à arbitrer par Chaima

Le dossier Drive « 🗂️ Caelum — Journal d'Audit » contient déjà un document de règles daté du
**2026-07-13** : « 📖 LISEZ-MOI — Règles du journal (nommage, format, zéro doublon) ». Il porte une
convention **différente** de celle donnée par Chaima le 2026-09-11 :

| | Convention du 2026-07-13 (LISEZ-MOI existant) | Convention du 2026-09-11 (instruction de Chaima) |
|---|---|---|
| Format | `AAAA-MM-JJ — Journal d'audit — [sujet court]` | `AAAA-MM-JJ-HHhMM — [Projet] — [Catégorie] — [Sujet précis]` |
| Heure | absente | obligatoire (`HHhMM`) |
| Projet / catégorie | implicites | explicites |
| Même sujet le même jour | **compléter** l'entrée existante | un document **par trouvaille** |

**Tranché, en attendant l'arbitrage :** la convention du 2026-09-11 prévaut — elle est plus récente et
plus précise, et le créneau `[Catégorie]` absorbe proprement « Journal d'audit ». Les deux normes ne
doivent pas coexister durablement : c'est à Chaima de confirmer, et le LISEZ-MOI du 2026-07-13 sera
alors corrigé et daté. **Je n'ai pas modifié ce document existant.**

### Ce que cette découverte apprend sur l'amélioration §7.1
La règle anti-doublon **existait déjà** — écrite noir sur blanc le 2026-07-13 : « avant de créer un
fichier, on vérifie qu'il n'existe pas déjà », « on ne recopie pas ce qui est déjà écrit ailleurs »,
« si on retravaille le même jour sur le même sujet → on complète l'entrée existante ».

Elle a ensuite été enfreinte une trentaine de fois entre juillet et août 2026 par les journaux
« boucle-caelum ». **La condition d'arrêt du §7.1 ne crée donc pas une règle neuve : elle rétablit une
discipline déjà décidée puis abandonnée.** Le problème n'était pas l'absence de règle, mais l'absence
d'un rôle habilité à arrêter une boucle — ce que l'ÉLAGUEUR corrige.

### Autre écart signalé (rôles MONSIEUR PROPRE / ARCHITECTE)
Le LISEZ-MOI porte un « Index des entrées » censé être « mis à jour à chaque nouvelle entrée ». Il ne
contient qu'une ligne, du 2026-07-13, alors que le dossier compte au moins 9 documents postérieurs.
L'index est obsolète. **Non corrigé sans l'accord de Chaima.**

---

## 9. Décision de Chaima du 2026-09-11 (16h35) — les 13 rôles sont des agents distincts

**La recommandation de fusion du §7.2 est annulée sur sa partie « vérification ».** Chaima a tranché :
les 13 rôles existent comme agents réels et nommés. Deux arguments issus de sa conception l'ont emporté :

1. **L'indépendance ne se sous-traite pas.** Le CONTRÔLEUR doit vérifier « sans voir les conclusions
   précédentes ». C'est structurellement impossible pour un agent qui a produit le premier verdict.
   Le décompte « 4 rôles pour 1 responsabilité » était faux : ce sont **quatre moments distincts** —
   éprouver, re-vérifier à l'aveugle, barrer la route, justifier la confiance par des preuves.
2. **L'asymétrie des coûts.** Un cycle gaspillé coûte du temps ; un faux GO sur un brevet coûte des
   honoraires pour un titre rejeté, et en cas de divulgation la nouveauté est perdue définitivement.
   Face à ce déséquilibre, la redondance est une assurance, pas un gaspillage.

**Maintenu (non contesté) :** l'orchestration reste subordonnée. `meta-orchestrateur` garde l'autorité
sur le dépôt ; `chef-orchestre-veille` est son délégué pour le domaine veille et n'arbitre rien au-delà.
Principe : **la redondance protège quand elle vérifie, elle nuit quand elle commande.**

**Règle structurante qui rend la décision robuste :** *un rôle = une décision qu'il possède.* Le désordre
vient de la collision d'autorité, pas du nombre de rôles. Chaque fichier d'agent porte donc une section
« DÉCISION QUE TU POSSÈDES (et personne d'autre) » et des « INTERDITS » nommant ce qu'il ne touche pas.

**Les 13 agents créés** (parc du dépôt Caelum : 29 → 42) :
`testeur` · `controleur` · `protecteur` · `pilote` · `chef-orchestre-veille` · `sentinelles` ·
`passerelle` · `gardien-controle-final` · `guetteur` · `prophete` · `boussole` · `dechiffreur` · `garant`

Chacun porte 7 sections : charte commune · mandat de domaine · mission · déclencheur · décision possédée ·
interdits · passation. Déposés aux deux endroits demandés : `.claude/agents/*.md` dans le dépôt Caelum
(branche `claude/chaine-veille-13-agents`) et un document par rôle au Drive, « Synergies inter-agents ».

---

## 10. Base d'erreurs de la chaîne (décision de Chaima du 2026-09-11)

Une base d'erreurs existe, **à consulter avant d'agir**, pour que les mêmes fautes ne soient jamais
reproduites deux fois.

- **Copie de référence :** `.claude/BASE-ERREURS.md` dans le dépôt `chaima0007/keywordmoneymaker`
  (branche `claude/chaine-veille-13-agents`) — placée à côté des agents pour qu'ils puissent réellement
  la lire.
- **Miroir de lecture :** Drive, « Synergies inter-agents », document du 2026-09-11-16h55.
- **16 fiches** au départ, chacune avec : ce qui s'est passé (preuve datée) · cause racine · **signal de
  détection** · contre-mesure · rôle qui en répond · leçon transférable.
- **Mode d'emploi :** on ne la lit pas en entier. On lit l'index, on repère les fiches dont le signal de
  détection ressemble à l'action qu'on va faire, et on applique leur contre-mesure avant d'agir.
- **Tenue :** ajout uniquement, jamais de réécriture. Pas de blâme — on documente des causes, pas des
  coupables : une base qui accuse cesse d'être alimentée. Rien n'est supprimé sans l'accord de Chaima.
- **Les erreurs des agents y figurent au même titre** que les erreurs héritées. Six des seize fiches
  (E-03, E-10, E-11, E-12, E-14, E-15) sont des fautes commises par un agent le 2026-09-11. Une base qui
  ne contiendrait que les erreurs des autres serait fausse, et donc inutile.

## 11. Contrôle honnête avant tout rapport (règle permanente, Chaima 2026-09-11)

**S'applique aux 42 agents, pas seulement à l'assistant en session.**

Aucun rapport complet ne commence sans une **phrase de contrôle honnête** répondant à deux questions :
1. Ai-je produit récemment des documents quasi identiques, ou redit ce qui était déjà écrit ?
2. La condition d'arrêt (§7.1 — aucun document neuf quand l'état est inchangé) a-t-elle effectivement
   fonctionné ?

Si la réponse révèle un problème — répétition, boucle, état inchangé documenté plusieurs fois —
**l'ÉLAGUEUR est saisi immédiatement, avant la remise du rapport, sans attendre une demande de Chaima.**

Si tout est sain, on le dit en une phrase **avec le motif**. Un contrôle de pure forme ne vaut rien : le
but n'est pas de cocher une case, c'est d'attraper la dérive avant qu'elle ne coûte un mois — ce qui
s'est produit entre le 28/07 et le 11/08/2026 (fiches E-01 et E-02).

**Où la règle est réellement inscrite.** Pour lier les 42 agents et pas seulement les 13 de la chaîne,
elle figure au **`CLAUDE.md` §2 ter** du dépôt Caelum — le seul document que tous les agents appliquent.
Les 13 agents de la chaîne la portent en plus dans leur propre fichier.

### Dette de forme à surveiller (autocritique)
Cette charte a reçu cinq sections en une seule journée (§6 à §11), par ajouts successifs. C'est conforme
à la règle « ajout, jamais écrasement », mais sa longueur devient elle-même un risque de lisibilité —
exactement le travers de la fiche E-04. À la prochaine décision structurante, l'ARCHITECTE devra
proposer à Chaima une **consolidation datée** (un document de synthèse qui remplace la lecture des
sections empilées, sans supprimer aucune d'elles).
