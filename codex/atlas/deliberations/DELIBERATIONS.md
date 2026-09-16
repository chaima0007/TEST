# ATLAS — DÉLIBÉRATIONS

> Demande de Chaima (2026-09-16) : *« il faut aussi écrire dans un dossier, comme les erreurs,
> les discussions et prises de décision, et pourquoi ils choisissent cet angle-là. »*
>
> **Un seul fichier vivant, ajout en tête** (R-007). Le plus récent en haut.
> Ici on consigne le **raisonnement**, pas seulement la conclusion : qui a plaidé quoi, sur
> quel fait, ce que chaque camp a **gagné**, et ce qui **renverserait** la décision.
>
> **Ce fichier n'est pas un compte rendu de courtoisie.** Une décision dont on ne peut plus
> reconstituer le motif six mois plus tard est une décision qu'on refera de zéro — ou pire,
> qu'on défendra sans savoir pourquoi.
>
> Distinction stricte : les **décisions** tranchées vivent dans `../memoire/DECISIONS.md`
> (une ligne), leur **raisonnement** vit ici (une section). Ce qui **attend** Chaima vit dans
> `/codex/A-DECIDER.md`.

---

## D-001 — Créer en continu, ou débloquer le premier encaissement ? (2026-09-16)

**Déclencheur.** Chaima formule son objectif réel : *« je veux une IA inarrêtable pour me
permettre d'être indépendante et riche dans l'avenir grâce aux projets créés en continu et qui
tiennent la route. »*

**Pourquoi un débat et pas une réponse.** L'affirmation « créer en continu rend riche » est une
**décision engageante** (§8, Parcours 2) : elle oriente tout le projet et du temps réel. Le
protocole interdit de la trancher d'un avis, *« même — surtout — pour une idée qui semble
évidente »*. Avocat et contradicteur ont donc été lancés **dans le même message**, en
parallèle : lancés l'un après l'autre, le second répond au premier, les positions convergent,
et le désaccord réel — la seule information utile — disparaît.

**Statut : EN COURS.** Avocat, contradicteur et simulateur ont rendu. Arbitrage lancé,
vérification à suivre.

---

### Ce que l'avocat a plaidé (POUR « créer en continu »)

1. **Le gagnant n'était pas prévisible — et c'est observé ici, pas supposé.** CompeteIQ était
   *le* projet ; il est EN PAUSE, marché dominé (pause reconfirmée le 2026-09-11). Caelum —
   l'entonnoir HERMES → BOUSSOLE → PACTE → RELANCE, construit en une journée le 2026-09-11 —
   **n'existait pas** quand il aurait fallu « finir CompeteIQ ». Une stratégie mono-projet
   aurait misé sur le mort et n'aurait jamais produit le vivant.
2. **Le coût marginal est bas parce que le socle est mutualisé.** ATLAS — 10 agents, une
   gouvernance complète — a été monté **en une journée** le 2026-09-16, parce que le PROTOCOLE
   CODEX préexistait. Le projet n+1 coûte le delta, pas le socle.
3. **Le §4 rend l'accumulation obligatoire.** `/codex/expertise/` est transverse, et le
   protocole dit lui-même que c'est *« la seule raison pour laquelle un Empire vaut mieux
   qu'une pile de dossiers séparés »*. Une expertise transverse sans plusieurs projets est un
   actif sans emploi.
4. **Créer est ce qui n'est pas bloqué.** 13 lignes ouvertes dans `A-DECIDER.md`, la plupart
   §10 : facturation, statut légal, envoi client. « Finir et vendre » bute d'abord sur des
   décisions **humaines** ; créer est la part qu'un agent peut avancer sans consommer le temps
   de Chaima.

**Ce qu'il n'a pas caché :** aucun revenu n'est consigné nulle part — et il précise que la
thèse adverse n'en a pas non plus.

**Son critère de renversement :** *un seul projet atteint un client payant ou un devis signé* →
l'option la moins chère cesse d'être « un projet de plus » et devient « répliquer la vente qui
a marché ». Il plaiderait alors l'inverse.

---

### Ce que le contradicteur a plaidé (CONTRE)

1. **Inversion de causalité.** La thèse suppose plus de projets → plus de revenus. Les données
   du dépôt montrent 38 branches, 14 jalons de production, **0 €**. Sur nos propres données,
   « créer en continu rend riche » est **NON VÉRIFIÉ**.
2. **L'angle Humain/Exécution du §9 est un trou béant.** Le temps réellement disponible de
   Chaima n'est **chiffré nulle part** — on répartit une ressource dont personne ne connaît la
   taille entre 38 fronts. *« Augmenter le débit d'entrée d'un système dont la sortie est
   bouchée aggrave l'engorgement. »*
3. **Les 3 blocages du premier euro ne sont pas techniques** : statut légal / modalités de
   facturation (ouvert depuis le 2026-09-11), moyen d'encaissement, liste de prospects jamais
   inventoriée (ouvert depuis le 2026-09-11). **Une IA locale n'immatricule pas une entreprise
   et ne recopie pas 30 noms.**
4. **L'outil ne tient pas le rôle qu'on lui prête.** 8,10 → 7,29 tokens/s, aucun GPU,
   fine-tuning fermé, **2 relevés sur 2 en échec avec une institution inventée**. Un modèle qui
   invente n'accélère pas la création : il fabrique de la vérification que Chaima paiera en
   heures.

**Ce qu'il n'a pas prétendu :** que « finir et vendre » rapporterait — jamais testé, aucun
message client jamais envoyé.

**Son garde-fou minimal** si Chaima tranche quand même pour « créer » : *aucun nouveau projet
tant que `A-DECIDER.md` compte plus de N lignes ouvertes, N fixé par Chaima.*

---

### ⚠️ Le fait central du contradicteur était FAUX — et comment on l'a su

**Il a affirmé** : *« `lib/agents/{hermes,pacte,boussole,relance}` ABSENTS de `main`, dont le
HEAD `cbe82e0` date du 2026-07-17 »* — donc *« deux mois de production dans aucune branche
livrée »*. C'était son fait le plus lourd, celui qui portait toute sa thèse F1.

**Vérification faite par l'orchestration, pas crue sur parole** (2026-09-16) :

```
git fetch origin main
git log origin/main -1   →  7b9552d  2026-09-16
git ls-tree -r origin/main | grep lib/agents
   →  hermes.ts · pacte.ts · boussole.ts · relance.ts · commandant.ts … PRÉSENTS
```

**`main` est à jour, daté d'aujourd'hui, et la boucle de vente Caelum EST livrée.** Le
contradicteur avait lu une référence `origin/main` locale **non rafraîchie** : il raisonnait
sur l'état du dépôt au 2026-07-17.

**Pourquoi cette correction compte plus que le débat lui-même :**

- **C'est exactement 🔴 ERR-011** — « branche bâtie sur un `main` périmé » — que le
  contradicteur **citait lui-même** dans sa plaidoirie. Il a commis l'erreur qu'il invoquait.
- **Elle prouve que la chaîne fonctionne.** Le §14 impose de vérifier avant de relayer ; un
  agent a été pris en défaut par la procédure, pas par chance. Sans cette étape, Chaima
  recevait une alarme fausse et grave : « ton travail n'est pas livré ».
- **Elle ne disqualifie pas le contradicteur.** Ses points 2, 3 et 4 tiennent debout sans F1 :
  0 € reste 0 €, les 3 blocages restent §10, le temps disponible reste inconnu. **Un argument
  faux ne rend pas faux les arguments voisins** — les traiter en bloc serait la faute
  symétrique.

**Règle qui en sort : R-013.**

---

### Ce que le simulateur a projeté (6 scénarios à 6 mois)

**Hypothèse qu'il pose en travers des six, et qui est la clé du dossier :** les deux voies
consomment **la même ressource rare — les heures de Chaima**, pas des tokens. L'IA locale ne
produit pas le code (un agent cloud le fait). **Donc les deux voies ne s'additionnent pas.**

| Voie | Scénario | Fait observable en cours de route | Confiance |
|---|---|---|---|
| **A — créer** | optimiste : les nouveaux projets atteignent un état déployé et mergé | `EVOLUTION.md` gagne ≥ 1 jalon « déployé » daté par mois **et** le nombre de branches cesse de croître | **FAIBLE** — aucun précédent |
| **A** | **réaliste : le stock grossit, rien ne merge, 0 €** | `VALUATION.md` affiche toujours « 0 client payant » | **ÉLEVÉE** — simple prolongation de ce que le dépôt montre déjà |
| **A** | pessimiste : cascade Vercel, casses non réparées, faits inventés par le modèle local entrés dans `/codex/` | un déploiement rouge non réparé > 7 jours, ou un fait non sourcé dans une fiche | **MODÉRÉE** |
| **B — encaisser** | optimiste : les 3 blocages §10 tombent, premier euro encaissé | `EVOLUTION.md` porte un jalon « client » ou « revenu » daté | **FAIBLE** — rien dans le dépôt n'accélère 3 décisions humaines |
| **B** | réaliste : statut légal tranché, liste de prospects toujours vide, boucle de vente à vide | « statut légal » quitte A-DECIDER, « liste de prospects » y reste | **MODÉRÉE** |
| **B** | pessimiste : les 3 lignes passent 90 jours, le code de vente se périme, ni création ni revenu | les 3 lignes encore ouvertes au 2026-12-11 **et** aucun commit sur `lib/agents/` | **MODÉRÉE** |

**L'asymétrie qu'il dégage — c'est sa contribution propre :**

> **La voie A échoue sur quelque chose qu'un agent peut produire seul** (du code non mergé).
> **La voie B échoue sur trois décisions que SEULE Chaima peut poser** (§10).

**Et un fait observable unique départage les six :** *la date du premier message envoyé à un
prospect réel.* Aucun scénario ne bouge sans elle.

**Il a aussi signalé de lui-même** que le fait F1 du contradicteur était faux et qu'aucune de
ses projections ne s'appuyait dessus — la correction a donc circulé correctement dans la
chaîne, ce qui est le comportement attendu du §14.

---

### Ce qui reste NON VÉRIFIÉ après les deux plaidoiries

| Point | Pourquoi ça bloque l'arbitrage |
|---|---|
| **Heures réellement disponibles de Chaima par semaine** | C'est **l'hypothèse centrale** du dossier. Les deux camps s'en servent en sens opposé sans la connaître. |
| Qu'un euro soit jamais entré | Aucun revenu consigné. Les deux thèses sont non testées. |
| Valeur des ~16 projets étrangers | Aucun n'est évalué. « 16 projets » n'est pas « 16 actifs ». |
| Utilité réelle d'ATLAS pour Chaima | Le jeu d'or n'existe pas encore ; les 2 seuls relevés sont des échecs. |
| Palier de débit après stabilisation thermique | `MACHINE.md` : « le palier n'est pas encore connu ». |

---

### Signalement d'incohérences (§5, audit — signalé, jamais corrigé seul)

Le contradicteur relève, et ceci **reste vrai** après correction de F1 :

1. `ETAT.md` et `A-DECIDER.md` se contredisent sur l'état de la PR #1 (l'un la dit mergée, l'
   autre garde la ligne « Merger la PR #1 » ouverte depuis le 2026-06-18).
2. `A-DECIDER.md` compte 13 lignes ouvertes, dont 11 dépassent 14 jours **sans la mise en
   évidence exigée par le §6**.

**Non corrigé par ATLAS** : `A-DECIDER.md` et `ETAT.md` appartiennent au périmètre partagé de
l'Empire (`sentinelle-perimetre`), et le §5 dit de signaler, jamais de corriger seul.
