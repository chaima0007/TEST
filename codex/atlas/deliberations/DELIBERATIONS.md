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

## 🔗 CONVERGENCE — deux sessions, deux trouvailles, une conséquence qu'aucune n'avait (2026-09-19)

> **Cas d'école pour `sentinelle-perimetre`** : communiquer avec un projet voisin **sans le
> perturber**. Rien n'a été modifié sur la branche `claude/charming-galileo-cqhkn1` — on l'a
> **lue**, et on intègre chez nous.

### Les deux moitiés

**Moitié A — trouvée ici le 2026-09-16 (VÉRIFIÉ, source primaire relue par l'orchestration).**
Depuis le 01-01-2026, un assujetti belge — **franchise de TVA comprise** — doit émettre des
factures électroniques structurées à un client assujetti. **Le PDF par e-mail ne suffit plus.**
L'ICP de Caelum étant « consultants/coachs indépendants », le modèle de facturation est bloqué
sans raccordement Peppol.

**Moitié B — trouvée le 2026-09-19 par la branche `charming-galileo` (RELAYÉ, commit `5be0a03`).**
Chaima est à **Bruxelles**. Trois voies s'offrent à elle, et **elles s'excluent mutuellement
pendant 2 ans** : Tremplin-indépendants · **JobYourself** (coopérative d'activités) · Prime
Actiris 4 000 €. L'une d'elles a une particularité : *« teste 18 mois en gardant les
allocations, **avec le n° d'entreprise ET de TVA de la coopérative** »*.

### Ce que le recoupement produit — et personne ne l'avait

**Sous une coopérative d'activités, Chaima facturerait sous le numéro de TVA de la
coopérative. L'obligation Peppol pèserait alors sur la coopérative, pas sur elle.**

Autrement dit : **la seule des trois voies qui dissout le blocage que j'ai trouvé est aussi
celle qui ferme les deux autres pour deux ans.** Ni la session A, ni la session B ne pouvaient
le voir seule.

**Statut : PLAUSIBLE, fiabilité MODÉRÉE. Ce n'est PAS vérifié.** Une coopérative peut très bien
exiger que ses membres se raccordent eux-mêmes, ou facturer sans être elle-même conforme.
**Ne pas décider là-dessus avant la réponse.**

### La question exacte à poser — une phrase, et elle vaut deux ans

> *« Si je facture via vous, les factures partent-elles sous votre numéro de TVA et via votre
> raccordement Peppol, ou dois-je me raccorder moi-même ? »*

**À poser à JobYourself avant tout engagement.** Coût : un e-mail. Enjeu : la seule décision
irréversible de deux ans du dossier.

### Ce que ça change dans l'ordre des choses

L'arbitrage D-001 recommandait de débloquer le premier encaissement. **Le recoupement montre
que l'ordre compte plus que la vitesse :** choisir un statut **avant** de savoir qui porte
l'obligation Peppol peut fermer, pour deux ans, la seule voie qui la règle.

**Aucune démarche de statut ne devrait partir avant cette réponse.** C'est un délai de
quelques jours contre un verrou de deux ans.

### Signal `gardien-donnees` — non corrigé, signalé (§5)

Le commit `5be0a03` inscrit **dans un message de commit, sur un dépôt PUBLIC**, ce qu'il
nomme la domiciliation de Chaima et sa date de naissance. Un message de commit **ne se retire
pas** sans réécrire l'historique — interdit par **R-002**, et de toute façon déjà diffusé.
**ATLAS n'y touche pas** : ce n'est ni sa branche ni sa décision (§10). Deux choses relèvent
de Chaima : savoir que c'est public, et décider si la pratique doit changer pour la suite.
Rien n'est répété ici : ce fichier dit « Bruxelles », ce qui suffit à tout le raisonnement.

---

## ⚠️ FAIT BLOQUANT — e-facturation Peppol obligatoire (2026-09-16)

> **Pas une délibération : un fait vérifié, consigné ici parce qu'il rouvre une décision.**
> Vérifié **deux fois** : par `atlas-chercheur-sources`, puis **réouvert et relu directement
> par l'orchestration** sur la source primaire — R-013 vaut d'abord pour soi.

### Ce qui est VÉRIFIÉ — pages officielles lues le 2026-09-16

**Source : `efacture.belgium.be` (portail fédéral belge).**

Article du **09-10-2024** — `/fr/article/pour-qui-la-facturation-electronique-deviendra-t-elle-obligatoire` :

> « À partir du 1er janvier 2026, toutes les entreprises belges assujetties à la TVA devront
> utiliser des factures électroniques structurées entre elles. […] **L'envoi d'une facture en
> format pdf par e-mail ou par plate-forme ne suffira donc plus.** »
>
> « **Avez-vous un numéro de TVA actif ?** Si c'est le cas, cette obligation s'applique
> également à votre entreprise. »
>
> « **L'obligation s'applique donc également si vous utilisez le régime de la franchise de
> taxe pour les petites entreprises** (si le chiffre d'affaires annuel de votre entreprise ne
> dépasse pas 25.000 euros) »

Communiqué du **07-04-2026** — `/fr/news/fin-de-la-periode-de-tolerance-pour-le-facturation` :

> « Des informations ont été récemment communiquées dans les médias concernant l'application
> de l'obligation […] pour les assujettis relevant du régime de la franchise. **Afin d'éviter
> toute mauvaise interprétation, nous souhaitons préciser que ces assujettis sont en principe
> également soumis à cette obligation.** »
>
> « La période générale de tolérance qui s'appliquait pendant les trois premiers mois de 2026
> […] **est désormais terminée.** »

**Le SPF a dû démentir publiquement** une information de presse contraire. Plusieurs sources
de rang 3 datées de 2026 propagent encore l'inverse — dont certaines en se réclamant du SPF.
**Ne jamais conclure sur du rang 3 :** ici, ça aurait produit exactement la mauvaise réponse.

### Le détail juridique qui explique la confusion — et qui vaut d'être retenu

La loi exclut les assujettis **de l'article 56** (le **forfait**), **pas ceux de l'article
56bis** (la **franchise**). Deux articles voisins, deux régimes différents. Toute la
désinformation tient à cette lettre. **On lit le numéro d'article, jamais le nom du régime.**

### Les exceptions réelles (page officielle, liste fermée)

Pas d'obligation d'**émettre** pour : assujettis **faillis** · entreprises réalisant
**uniquement** des opérations exemptées art. 44 · assujettis **non établis** en Belgique ·
assujettis **forfaitaires art. 56**.
Et surtout : **« L'une des deux parties n'est-elle pas assujettie à la TVA ? Si tel est le cas,
l'obligation ne s'applique pas à leurs transactions mutuelles. »**

### Ce que ça fait concrètement à Caelum

| Situation | Facture PDF par e-mail ? |
|---|---|
| Chaima (n° TVA actif) → **consultant/coach assujetti belge** | ❌ **NON. Peppol obligatoire.** |
| Chaima → client **particulier** | ✅ oui — mais elle doit pouvoir **recevoir** du structuré |
| Chaima → client dont l'activité est **entièrement exemptée art. 44** | ✅ oui (à vérifier client par client) |

**L'ICP tranché le 2026-09-14 est « consultants / coachs indépendants » — donc majoritairement
la première ligne.** `lib/agents/pacte.ts` produit des devis dont les modalités sont
« À CONFIRMER » : **ce trou-là est désormais chiffré et daté.**

**Ce n'est pas un mur, c'est une étape** : le raccordement Peppol passe par un logiciel de
facturation. Mais c'est une étape **avant** le premier client, pas après.

### Rapporté par l'agent, NON revérifié par l'orchestration

Amendes de **1.500 / 3.000 / 5.000 €** (AR du 08-07-2025, MB 14-07-2025). Tolérance
self-billing échue au 30-06-2026. **Tarifs** de raccordement relevés sur pages officielles des
prestataires — voir `DOSSIER-02-ENCAISSEMENT.md`. Ces points sont **RELAYÉS**, pas revérifiés
par moi : je n'ai rouvert que ce qui décide.

### Deux pièges trouvés au passage — chacun aurait produit une faute

1. **Le libellé de la mention de franchise a changé au 01-01-2025.** Le texte en vigueur dit
   **« Régime particulier de la franchise de taxe »**. La variante la plus répandue sur le web
   (« TVA non applicable, art. 56bis ») **ne figure dans aucun texte : elle est fabriquée.**
2. **La conservation est passée de 10 à SEPT ans, rétroactivement** au 01-01-2023 (loi du
   18-12-2025). Presque tout le web dit encore 10 ans — **y compris une note d'un institut
   professionnel de février 2026**. Conserver plus longtemps n'est jamais une infraction.

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

**Statut : ARBITRÉ ET VÉRIFIÉ — en attente de décision de Chaima.** Les cinq étapes du §8 ont
été faites, aucune sautée : avocat ⟂ contradicteur (même message), simulateur, arbitre,
vérificateur. Ligne inscrite dans `/codex/A-DECIDER.md`.

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

### L'arbitrage — et les amendements du vérificateur qui l'ont amputé

**Ce que l'arbitre a apporté de neuf, et qui est VÉRIFIÉ (recompté deux fois) :**
`A-DECIDER.md` compte **14 lignes ouvertes** (et non 13, comme l'avançaient l'avocat *et* le
brief), dont **4 seulement** dépassent 14 jours (et non 11, comme l'avançait le
contradicteur), et **10 ont été créées depuis le 2026-09-11** — cinq jours.
**Les deux camps se trompaient de chiffre. L'arbitre non.**

**Sa recommandation :** affecter ATLAS au **premier encaissement**, pas à la création. Sa
production n'est pas du code mais la **réduction du coût de décision de Chaima** : des dossiers
où chaque question arrive avec ses options et une option par défaut, pour qu'elle **choisisse**
au lieu de chercher. Gel de tout nouveau projet jusqu'au premier message prospect envoyé.

#### ⚠️ Son motif central a été REFUSÉ par le vérificateur

L'arbitre concluait : *« le goulot est le DÉBIT de décisions adressées à Chaima »*, en
s'appuyant sur 10 ouvertures en 5 jours et sur l'idée qu'*« aucune des 4 lignes anciennes n'a
bougé »*.

**Deux défauts, tous deux vérifiés dans `A-DECIDER.md` le 2026-09-16 :**

1. **« Aucune des 4 anciennes n'a bougé » est FAUX.** Deux portent une trace datée d'activité :
   « **Volet CI retiré le 2026-09-11** » et « Pause **reconfirmée par Chaima le 2026-09-11** ».
   Formulation correcte : aucune n'a été **close** — ce qui n'est pas la même chose.
2. **« Le goulot EST le débit » est une INFÉRENCE, pas un fait** — et un contre-fait vit dans
   le même fichier : la section « Décisions tranchées » enregistre **8 décisions TRANCHÉES PAR
   CHAIMA entre le 2026-09-11 et le 2026-09-16**. Même fenêtre de cinq jours.

| Sur 5 jours (2026-09-11 → 2026-09-16) | Compté |
|---|---|
| Décisions **ouvertes** | **10** |
| Décisions **tranchées par Chaima** | **8** |

**Le débit de sortie n'est ni nul, ni effondré.** Il est du même ordre que l'entrée. La thèse
de l'engorgement n'est **pas établie** — elle est **PLAUSIBLE, fiabilité MODÉRÉE**, et elle
deviendrait VÉRIFIÉE (ou tomberait) avec un relevé hebdomadaire sur 4 semaines.

#### Les autres amendements retenus

| Ce que disait l'arbitrage | Amendement appliqué |
|---|---|
| « les **3** blocages §10 » | **2 lignes ouvertes, 3 volets.** Le moyen d'encaissement est un volet de la ligne facturation, pas une 3e ligne. Les deux datent du **2026-09-11**. |
| « blocages **§10** » | Humains **de fait**, mais « immatriculer » et « choisir un moyen d'encaissement » ne figurent **pas littéralement** au §10 (test du découpage, `AGENTS.md`). |
| « **mesurer** les heures de Chaima » | Aucun agent ne peut mesurer ça → **demander**. |
| Garde-fou « plus de 3 lignes/semaine » | Le contradicteur écrivait « **N fixé par Chaima** ». L'arbitre a posé N=3 de lui-même, sans donnée de débit → **PROPOSÉ : N = 3, à fixer par Chaima** (§10). |
| « réduction du coût de décision » | Effet **supposé, jamais mesuré** → **NON VÉRIFIÉ**, fiabilité FAIBLE. |
| « 0 € / aucun revenu » | `VALUATION.md` porte « 0 client payant, 0 ARR, 0 MRR **au jour de l'analyse** » — **sans date de cette analyse**. Chiffre sans date (§13) → à redater. |
| « **ATLAS est affecté** à… » | Présuppose une décision **non tranchée** (« Où vit ATLAS », ouverte le 2026-09-16). Un arbitrage ne peut pas affecter ATLAS avant que Chaima ne l'ait dit. → **PROPOSÉ**. |

#### Contradiction interne relevée, et tranchée

L'arbitrage **interdisait** à ATLAS tout contenu factuel sans jeu d'or, **et** lui confiait des
dossiers « avec options chiffrées » sur le statut légal et les prix. **Un dossier chiffré EST
du contenu factuel.**
**Levée :** ces dossiers sont produits par la **chaîne d'agents CODEX** (sourcée, vérifiée,
§14), **jamais par le modèle local** — dont les 2 relevés sur 2 sont en échec, avec une
institution inventée. L'interdiction faite au modèle local tient sans réserve.

#### Ce que la recommandation devient après amendements

**Elle survit, mais pas pour la raison annoncée.** Le motif « le débit déborde » tombe. Restent,
et ils suffisent :

- **Aucun message n'a jamais été envoyé à un prospect réel.** Fait, pas interprétation.
- **Deux lignes bloquent le premier euro depuis le 2026-09-11**, et aucune n'est technique.
- **Le modèle local invente** — 2 relevés sur 2 en échec.
- **Les heures de Chaima sont inconnues**, et les deux camps s'en servaient en sens opposé.
- **§14 — le verdict le plus prudent gagne par défaut** quand les faits ne départagent pas.
  Ne pas ouvrir de front nouveau est le verdict prudent. **Aucun écart à justifier.**

**Confiance : MODÉRÉE** — abaissée par rapport à l'arbitre, qui la tenait sur une inférence.

#### Ce que chaque camp a gagné (§8 — sinon la décision est gagnée, pas arbitrée)

**AVOCAT.** (1) Rien n'est tué : le gel porte sur le **démarrage**, pas sur l'acquis ; le socle
mutualisé et `/codex/expertise/` transverse (§4) continuent d'accumuler. (2) **Son critère de
renversement devient la condition de sortie du gel** — un devis signé ou un client payant, et
la création rouvre : c'est lui qui aura eu raison. (3) Son argument 1 est **retenu comme
garde-fou** : Caelum, né *après* CompeteIQ, est précisément le projet qu'on finit — on ne mise
pas sur le mort. (4) Son argument 3 (§4) est **intact** : l'expertise transverse ne s'arrête
pas pendant le gel.

**CONTRADICTEUR.** (1) Son point 2 (l'angle Humain du §9) devient **l'action n°1**. (2) Son
garde-fou N est adopté, **mais rendu à Chaima** comme il l'écrivait. (3) Son point 4 devient
une **interdiction ferme** : aucun contenu factuel produit par le modèle local tant que le jeu
d'or n'existe pas (R-006). (4) Son objection « une IA locale n'immatricule pas une entreprise »
reçoit son garde-fou manquant : **échéance de réexamen datée au 2026-11-16** — si les dossiers
n'ont rien débloqué à cette date, l'arbitrage se rouvre.

#### Post-arbitrage — l'hypothèse centrale a été MESURÉE (2026-09-16, même jour)

Les deux camps s'appuyaient en sens opposé sur le temps de Chaima sans le connaître ; le
vérificateur en faisait son premier NON VÉRIFIÉ. Interrogée, Chaima répond qu'elle **ne peut
pas l'estimer**. L'activité a donc été **mesurée** sur les horodatages git, au lieu d'être
redemandée. Détail : `../memoire/PROFIL-CHAIMA.md`.

**Résultat : 6 jours actifs sur 56, ≈ 21 h 30 au total, en rafales de 2 à 4 h.** Cinq des six
jours tiennent dans les onze derniers. **Ce n'est pas un débit hebdomadaire, ce sont des
rafales** — d'où l'impossibilité sincère d'estimer.

**Effet sur l'arbitrage : il le renforce, mais en remplaçant encore une fois le motif.**

| Motif | Statut |
|---|---|
| « Le débit de décisions déborde » (arbitre) | **RÉFUTÉ** — 10 ouvertes / 8 tranchées |
| « Aucun message prospect jamais envoyé » + §14 prudence | **TIENT** |
| **« Le temps est fragmenté en rafales de 2-4 h »** | **NOUVEAU — PLAUSIBLE, fiabilité ÉLEVÉE** |

Une rafale de 2 à 4 heures ne permet pas de tenir plusieurs fronts : la reprise mange le début
de chaque session, et 38 branches rendent cette reprise coûteuse. **Le gel n'est plus une
mesure de discipline, c'est une conséquence arithmétique de la forme du temps disponible.**

Et cela **nomme la valeur d'ATLAS** que trois agents avaient cherchée sans la trouver : ni
écrire du code, ni savoir des choses — **rendre la reprise quasi gratuite**. Sur un temps en
rafales, c'est ce qui décide si la rafale produit quelque chose.

**Ce que l'avocat y gagne encore :** son argument du socle mutualisé se trouve confirmé par un
chemin qu'il n'avait pas emprunté — un socle qui supprime le coût de reprise **est** le seul
investissement qui rentabilise un temps fragmenté.

#### Le fait unique qui départagera

> **La date du premier message envoyé à un prospect réel.**

Absent au **2026-11-16** → la voie « créer » s'est réalisée d'elle-même, et le contradicteur
avait raison.

---

### Ce qui reste NON VÉRIFIÉ après les deux plaidoiries

| Point | Pourquoi ça bloque l'arbitrage |
|---|---|
| **Heures réellement disponibles de Chaima par semaine** | **L'hypothèse centrale.** Les deux camps s'en servent en sens opposé sans la connaître. Aucun agent ne peut la mesurer — il faut la **demander**. |
| **Le rapport réel entre entrée et sortie d'A-DECIDER** | 10 ouvertes / 8 tranchées sur 5 jours : trop proche pour conclure. Un relevé hebdomadaire sur 4 semaines trancherait. |
| **La date de l'analyse « 0 € » de `VALUATION.md`** | Le fichier dit « au jour de l'analyse » sans dire quel jour. Chiffre sans date (§13). |
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
