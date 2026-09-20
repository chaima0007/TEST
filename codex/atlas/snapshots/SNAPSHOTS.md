# ATLAS — SNAPSHOTS

> Rituel d'entrée §5, **avant toute autre tâche**. État réel **vérifié**, jamais de mémoire.
> Le plus récent en haut. Rien n'a changé → **une seule ligne**, puis silence.
> Un snapshot dit *ce qui a changé*. Il ne dit pas *si c'est cohérent* — ça, c'est `audits/`.

---

## SNAPSHOT 2026-09-20 — 11:25 UTC — Première passe de la routine : a tourné, n'a rien pu pousser. Mise en pause.

**Compteur de passes sans fiche nouvelle : 1** (la passe du 20/09, sans dépôt).

- **Routine, 1re passe** (04:06 UTC) : SUCCEEDED, 7 min, **2,51 $**, **aucun commit**. Cause
  **VÉRIFIÉE** dans sa configuration : `sources: []` — pas de dépôt attaché, donc pas de push.
  **Pas propre à ATLAS** : les consignes de tes autres routines disent la même chose, et ton
  JOURNAL du 11/09 l'avait déjà identifié. **Mise en pause** (réversible) : coût sans dépôt =
  coût dormant. Correctif structurel = attacher le dépôt à l'environnement des routines — **à toi**.
- **Le test de reprise à froid reste PLAUSIBLE, pas CONFIRMÉ** : la passe du 20/09 n'a pas
  produit le snapshot qui devait le confirmer. Pas parce que le prompt est mauvais — parce que
  la session n'avait rien où écrire.
- **Signal `intendant-couts` / `superviseur-vigie`** : ≥ 9 routines actives sur le compte, dont
  une **horaire** et une toutes les **8 h** ; la méta-surveillance a **échoué** le 19/09.
  Coût mensuel cumulé : NON VÉRIFIÉ. Ligne A-DECIDER.
- **Drive** : prompt maître v2 **amendé** recréé et relu (`1wmi71bu…`) ; ancien renommé, gardé.
- Aucune autre branche n'a bougé depuis le 19/09 14:10 UTC.

## SNAPSHOT 2026-09-19 (6) — 14:10 UTC — Test de reprise à froid : PLAUSIBLE, 8 trous bouchés

**Compteur de passes sans fiche nouvelle : 0.** *(Convention à partir d'ici : chaque snapshot porte
son heure UTC, pour que `git log --since` fonctionne.)*

- **Test de reprise à froid fait** (session neuve, prompt seul, lecture seule) : elle a repris —
  **mais par inférence** sur deux ambiguïtés (`ETAT.md` ×2, `ERREURS` ×2) et une ligne A-DECIDER
  contradictoire. Verdict **PLAUSIBLE**. Détail : `audits/AUDITS.md`.
- **8 trous de mon périmètre corrigés** avant la première passe de la routine ; **2 trous du
  périmètre partagé signalés, non corrigés** (§5) — dont un déjà signalé le 16/09.
- **Drive mis à jour** : document d'erreurs courant recréé (l'outil ne modifie pas un document
  existant), ancien conservé et renommé. Procédure écrite dans `continuite/SYNC-DRIVE.md`.
- **Passe à CONFIRMÉ** si la routine du 20/09 06h produit un snapshot juste sans toucher
  `ETAT.md` racine ni rouvrir JobYourself.

## SNAPSHOT 2026-09-19 (5) — Le Drive est lu : 906 fichiers cartographiés, 32 documents distillés

- **Chaima : « notre IA doit lire tout mon Drive pour apprendre ».** Périmètre décidé seul et
  dit : **Empire oui, privé non** (4 dossiers personnels pré-2026 comptés, jamais ouverts ;
  coffre : titres seuls). Le dépôt est public → principes seulement, filet passé sur chaque fichier.
- **`memoire/CARTE-DRIVE.md`** (cartographe) : 19 dossiers, **906 fichiers comptés** par listing
  exhaustif, portes d'entrée identifiées, 10 documents à lire en premier avec ID. Révèle :
  **7 protocoles maîtres concurrents**, LLAM en 3 copies, 28 dossiers vides, 4 index rivaux, et
  **une contradiction non tranchée** sur le statut de LLAM (gelé vs vitrine). 3 lignes A-DECIDER.
- **`expertise/methode-agents.md` + `erreurs-transverses.md`** (scout) : 32 documents lus. Six
  familles d'erreurs sur neuf ont la même forme — *un état a changé et personne ne possédait la
  question « est-ce encore vrai ? »* ; le correctif qui tient est un rôle ou un mécanisme
  bloquant, jamais une phrase. **Deux familles récidivent malgré leur fiche.** 1 ligne A-DECIDER.
- **Drive ↔ git ne se recouvrent pas** : 8 branches git sans dossier Drive, 2 projets Drive sans
  branche ici. La synchronisation LLAM (368 fiches / 3 539 commits) : NON VÉRIFIÉE.
- **Mémoire de l'IA locale régénérée** avec ce que le Drive a appris. Prochaine étape : **test
  de reprise à froid** — une session neuve, le prompt maître, rien d'autre.

## SNAPSHOT 2026-09-19 (4) — Le système tourne désormais sans Chaima

**Compteur de passes sans fiche nouvelle : 0** (initialisé pour la routine).

- **Pont vers l'IA locale livré** : `scripts/generer-modelfile-memoire.sh` →
  `memoire/atlas-memoire.Modelfile` (~3 000 tokens : règles de prudence en français + état
  complet du projet + règles apprises). Trois lignes PowerShell chez Chaima, adresse vérifiée
  (`200`). **Premier moment où ce qui est construit ici entre dans sa machine.** Chaima avait
  demandé « tu es censé créer une IA indépendante ? » — réponse consignée : elle existait,
  elle était vide ; là elle se remplit. Limite dite : elle retrouvera et citera, elle ne
  cherchera ni ne débattra.
- **Routine quotidienne CRÉÉE** (`trig_01RXTwrecsCLboaL6kMmn6Ry`, 06h00 Bruxelles) sur
  décision de Chaima — « surveille-le pour qu'il grandisse » — après signalement de la dépense
  récurrente. Elle fait le §5, intègre les branches voisines, cherche sur 2 domaines,
  **régénère le Modelfile**, pousse, se tait si rien. **Deux limites consignées** : sans
  connecteurs (pas d'Exa → RELAYÉ/NON VÉRIFIÉ seulement, consigne adaptée) ; droits de push
  à confirmer à la première exécution du 20/09.
- **Ce que « grandir » veut dire désormais, mécaniquement** : la routine enrichit
  `expertise/` et `memoire/` → régénère le Modelfile → Chaima relance 3 lignes → son IA locale
  sait plus qu'hier. Quand le RAG sera en Zone 3, la même chose, sans les 3 lignes.

## SNAPSHOT 2026-09-19 (3) — Parcours 1 terminé : le RAG a son candidat

- **CAND-001 complète** : scout (6 pistes, 3 écartées sur source) → guardian + sentinel **en
  parallèle**, verdicts concordants. **AnythingLLM Desktop v1.16.1 : VALIDÉ NON INTÉGRÉ.**
  Open WebUI Desktop et Msty : **REJETÉS**.
- **Trouvaille licence** : FFmpeg téléchargé par l'installeur est **GPL-3.0** — sans effet en
  usage, à exclure d'une licence sortante. **Trouvailles sécurité** : 19/20 avis corrigés ;
  `DISABLE_TELEMETRY` ne coupe **que** PostHog, deux sorties réseau subsistent (embedder au 1er
  document, liste de modèles au démarrage) ; **installeur et wrapper hors dépôt public** →
  signature et hashes NON VÉRIFIÉS ; « Dynamic Model Routing » = repli cloud natif (R-004).
- **Souveraineté : NON VÉRIFIÉE, et dite telle quelle.** On ne peut pas exécuter un `.exe`
  depuis ici. Procédure Zone 1 Windows écrite pour Chaima (signature, TCPView, opt-out, 10 min
  de chat → `127.0.0.1` seul), plus le verrou pare-feu sortant. Toute adresse distante = REJET.
- **Convention de nommage du corpus fixée avant le premier document** : la date du document
  dans le nom, parce que le RAG cite le fichier, pas la date.
- **Rien installé.** Installer = geste de Chaima (§10). Zone 1 → Zone 3 directement : interdit.

## SNAPSHOT 2026-09-19 (2) — « Avance un maximum » : carte, filet, candidat RAG

- **Vision reformulée par Chaima** : une IA intelligente, motivante, qui cherche toute
  l'information pour décider au mieux, qui aide à rendre les projets **financièrement
  autonomes**, apprend en permanence, sécurise et protège. Décomposée : *chercher* →
  `atlas-chercheur-sources` + routine §4 (proposée) · *décider* → Parcours 2 + fiches de
  décision · *apprendre* → `/codex/expertise/` (9 fiches, 2 domaines, maturités cohérentes) ·
  *sécuriser/protéger* → sentinelles + **filet avant push livré aujourd'hui**. « Motivante » :
  pas par flatterie (interdite par Chaima elle-même) — par la **reprise rendue gratuite** et le
  **progrès rendu visible**.
- **`memoire/CARTE-PROJETS.md` livrée** — dette du 16/09. 38 branches : **15 vivantes, 3
  ralenties, 20 dormantes, 9 univers séparés.** Corrige l'audit du 14/09 : 5 branches sont bien
  posées sur `main`. **Risque de continuité n°1 de l'Empire nommé** : La Loi Avec Moi, 3 539
  commits, une seule branche, aucune sauvegarde. Signalé, pas corrigé (§10).
- **`scripts/verifier-avant-push.sh` livré et testé** (a attrapé date de naissance, e-mail et
  clé dans un faux message). Inscrit dans `CLAUDE.md` §15.4, le skill `atlas`, et **R-015**.
  Il signale, ne bloque pas (§5). **Appliqué à ce commit-ci avant push.**
- **Parcours 1 lancé** pour la couche 4 (RAG local, Windows, sans Docker, 100 % local) :
  `scout` cherche 3 candidats sur source primaire → fiche `codex/candidates/CAND-001`. Ensuite
  `guardian-licences` + `sentinel-securite` **en parallèle**. Installation = décision de Chaima.
- **Routine quotidienne d'apprentissage : PROPOSÉE, pas créée.** Dépense récurrente = §10.
- `/codex/expertise/` vérifié : 6 + 3 fiches, maturités exactes, aucun doublon. Rien à réconcilier.

## SNAPSHOT 2026-09-19 — Recoupement inter-sessions : l'ORDRE compte plus que la vitesse

État réel vérifié par `git fetch` : branche à jour, `main` inchangé depuis le 2026-09-16
(`7b9552d`), toujours 38 branches, rien en attente de commit.

- **Activité détectée sur une branche voisine** : `claude/charming-galileo-cqhkn1`, commit
  `5be0a03` du 2026-09-19. Lu, **jamais touché** (`sentinelle-perimetre`).
- **Deux corrections majeures venues de là (RELAYÉ, non revérifié) :** Chaima est à
  **Bruxelles** — tout un volet de dispositifs **wallons** était hors sujet, et une « urgence »
  signalée le 16/09 y est reconnue **fausse** ; et l'absence de diplôme de gestion **n'est pas
  bloquante** à Bruxelles.
- **⚠️ Le recoupement que personne n'avait, et c'est le résultat du jour.** Trois voies
  bruxelloises **s'excluent pendant 2 ans** (Tremplin · JobYourself · prime Actiris). Or
  JobYourself facture **sous le n° de TVA de la coopérative** — donc **la seule voie qui
  dissoudrait l'obligation Peppol trouvée ici le 16/09 est aussi celle qui ferme les deux
  autres pour deux ans.** Ni l'une ni l'autre session ne pouvait le voir seule.
  **PLAUSIBLE, fiabilité MODÉRÉE — surtout pas une base de décision en l'état.**
- **Conséquence opérationnelle : l'ordre prime sur la vitesse.** Choisir un statut **avant**
  de savoir qui porte l'obligation Peppol peut verrouiller deux ans. Une question d'une phrase
  à poser à JobYourself lève l'incertitude. **Coût : un e-mail.**
- **Signal `gardien-donnees`, signalé et non corrigé (§5, §10)** : le commit voisin inscrit
  domiciliation et date de naissance **dans un message de commit, sur un dépôt PUBLIC**. Un
  message de commit ne se retire pas sans réécrire l'historique (**R-002**), et c'est déjà
  diffusé. ATLAS n'y touche pas et **ne répète rien** — ses propres fichiers disent
  « Bruxelles », ce qui suffit au raisonnement.
- **Valeur d'ATLAS démontrée en acte** : aucune de ces deux trouvailles n'était nouvelle. Ce
  qui était neuf, c'est de **les mettre côte à côte** — exactement la fonction « mémoire qui
  rend la reprise gratuite » identifiée le 2026-09-16.

## SNAPSHOT 2026-09-16 (10) — Un fait bloquant trouvé, vérifié deux fois

- **⚠️ e-facturation Peppol obligatoire, franchise TVA comprise. VÉRIFIÉ** par un agent, puis
  **relu directement par l'orchestration sur la source primaire** (`efacture.belgium.be`,
  article du 09-10-2024 + communiqué du 07-04-2026). Phrase officielle : *« L'envoi d'une
  facture en format pdf par e-mail ou par plate-forme ne suffira donc plus »*, et
  *« l'obligation s'applique donc également si vous utilisez le régime de la franchise »*.
- **Le modèle de facturation de Caelum est bloqué** tant qu'il n'y a pas de raccordement
  Peppol : l'ICP tranché le 2026-09-14 (consultants/coachs indépendants) est majoritairement
  assujetti à la TVA. Ligne ouverte dans `/codex/A-DECIDER.md`.
- **Le SPF Finances a dû démentir publiquement** une information de presse contraire, et
  plusieurs sources de rang 3 datées de 2026 propagent encore l'inverse **en se réclamant du
  SPF**. Conclure sur du rang 3 aurait donné ici exactement la mauvaise réponse — la règle de
  la source primaire vient de payer, en une fois, tout ce qu'elle coûte.
- **Clé juridique retenue :** la loi exclut l'**art. 56** (forfait), **pas l'art. 56bis**
  (franchise). **On lit le numéro d'article, jamais le nom du régime.**
- **Deux pièges évités** : le libellé légal de la mention de franchise a changé au 01-01-2025
  (la variante la plus répandue sur le web **n'existe dans aucun texte**) ; la conservation est
  passée de 10 à **7 ans**, rétroactivement — presque tout le web, y compris une note d'un
  institut professionnel de 2026, dit encore 10.
- **Non revérifié par l'orchestration, donc RELAYÉ** : montants d'amendes et tarifs des
  prestataires. Seul ce qui décide a été rouvert.
- **Le renversement de la journée** : l'agent qui avait conclu « aucune source accessible »
  avait tort ; celui qui a persisté a trouvé le fait qui change le plan commercial de Chaima.

## SNAPSHOT 2026-09-16 (9) — Feu vert de Chaima · deux dossiers · une fausse accusation réfutée

- **Chaima : « pourquoi tu n'avances pas sans moi ? » puis « feu vert ».** Constat accepté : la
  règle **R-001** de son propre `AGENTS.md` (livrer tout ce qui ne figure pas au §10) avait été
  enfreinte trois tours de suite. Le §10 reste à elle ; le reste avance.
- **Jeu d'or FIGÉ** (R-006, l'étape non rattrapable) : 24 questions, 5 familles, barème sur 33.
  `mesure/JEU-D-OR-QUESTIONS.md`.
- **Deux dossiers de déblocage du 1er euro produits** par des chercheurs, sur le droit belge.
- **ERR-ATLAS-004 — un agent en a accusé un autre de fabriquer des chiffres.** Vérification
  faite immédiatement par l'orchestration, pas d'arbitrage d'autorité : `inasti.be` et Justel
  récupérés via Exa ; **Justel renvoie « mise à jour au 24-12-2025 », exactement la date citée
  par le dossier accusé**. **Accusation réfutée.** Cause réelle : `WebFetch`/`curl` bloqués,
  **Exa non** — asymétrie d'outil, pas de rigueur. L'accusateur a pris sa limite pour une
  propriété du monde. **Il n'a pas commis de faute** : sur ce qu'il voyait, signaler était le
  bon réflexe. Règle **R-014**.
- **VÉRIFIÉ par l'orchestration, source lue** (`efacture.belgium.be`, 2026-09-16) : « Depuis le
  1er janvier 2026, toutes les entreprises belges assujetties à la TVA devront utiliser des
  factures électroniques structurées entre elles. » **Potentiellement bloquant pour Caelum** :
  si la franchise TVA est concernée, un PDF par e-mail ne suffit plus pour facturer un
  consultant assujetti — l'ICP exact tranché le 2026-09-14.
- **La question qui décide reste NON VÉRIFIÉE** : la franchise de TVA (art. 56bis) est-elle
  concernée ? Non inférée, non devinée. `DOSSIER-02` **relancé** avec le bon outil et cette
  seule priorité.
- **Résultat contre-intuitif consigné** : l'agent prudent a produit le dossier **le plus
  faible**. Sur-marquer NON VÉRIFIÉ rend une information exacte inutilisable. **L'excès de
  prudence a un coût — juste moins visible que l'excès de confiance.**

## SNAPSHOT 2026-09-16 (8) — Parcours 2 complet : D-001 arbitré, amendé, inscrit

- **Les 5 étapes du §8 faites, aucune sautée.** Avocat ⟂ contradicteur **dans le même message**,
  puis simulateur, arbitre, vérificateur. Raisonnement intégral dans
  `deliberations/DELIBERATIONS.md` §D-001 — dossier créé aujourd'hui à la demande de Chaima.
- **Chaque étage a corrigé le précédent. C'est le résultat le plus important de la journée :**
  - le **contradicteur** a été réfuté sur son fait central (ref git non rafraîchie, ERR-011 —
    l'erreur qu'il citait lui-même) ;
  - l'**arbitre** a corrigé **les deux camps** sur les comptages : 14 lignes ouvertes et non 13,
    4 anciennes et non 11, 10 créées en 5 jours ;
  - le **vérificateur** a refusé le motif central de l'arbitre : « aucune des 4 anciennes n'a
    bougé » est **faux** (deux portent une trace datée), et « le goulot EST le débit » est une
    **inférence** — contre-fait dans le même fichier : **8 décisions tranchées par Chaima sur
    la même fenêtre de 5 jours** contre 10 ouvertes. **L'engorgement n'est pas établi.**
- **Recommandation maintenue, motif remplacé, confiance abaissée à MODÉRÉE.** Elle ne tient
  plus sur l'engorgement mais sur le §14 (verdict le plus prudent par défaut) et sur un fait
  nu : **aucun message n'a jamais été envoyé à un prospect réel**.
- **Autocritique consignée** : 2 des 10 lignes ouvertes en 5 jours ont été créées **par ATLAS
  lui-même aujourd'hui**. L'agent qui plaide contre l'encombrement y contribue.
- **Ligne inscrite dans `/codex/A-DECIDER.md`** (ajout seul, périmètre partagé respecté).
  **Statut PROPOSÉ. Chaima tranche** — aucun agent n'a exécuté quoi que ce soit.
- **Réexamen daté : 2026-11-16.** Fait unique qui départagera : la date du premier message
  envoyé à un prospect réel.

## SNAPSHOT 2026-09-16 (7) — L'attente est arbitrée, pas gommée

- **Chaima exprime son attente** : « une IA qui ressemble à Claude, à qui je peux tout
  demander, autonome mais surveillée. » **Décomposée en 4 composantes** dans
  `memoire/PROFIL-CHAIMA.md` : 3 atteignables, **1 structurellement hors d'atteinte** (savoir
  énormément de choses de tête). Écart d'ordre de grandeur, pas de configuration.
- **Contradiction assumée et écrite** : « tout lui demander » est exactement ce qui ne
  fonctionne pas, et c'est **démontré le même jour sur ses propres données** — deux questions
  de droit, deux échecs, une institution inventée. Un généraliste local invente partout.
- **Ce qui remplace la 4e composante** : elle ne saura pas de tête, elle saura **où chercher
  dans les documents de Chaima**. Sur son terrain, ça vaut mieux. Le choix réel est
  « généraliste médiocre ou spécialiste fiable ».
- **« Autonome mais surveillée » : retenu tel quel.** C'est l'architecture déjà en place.
  Chaima avait raison avant moi sur ce point.
- **Ligne A-DECIDER ouverte** : premier domaine d'expertise. **PROPOSÉ** — le droit belge /
  l'asbl, parce que le corpus existe déjà et que l'écart y est mesuré. Décision de Chaima.

## SNAPSHOT 2026-09-16 (6) — Bridage CONFIRMÉ · mesure « avant » du jeu d'or établie

- **Bridage thermique : prédit, puis MESURÉ le même jour.** `eval rate` 8,10 → 7,75 → 7,29
  tokens/s en trois échanges, **−10 %**, sans rien changer d'autre que continuer à parler.
  **CONFIRMÉ.** Toute mesure future du projet doit indiquer le **numéro de l'échange**.
- **Second ralentisseur identifié** : `prompt eval count` 42 → 232 → 620 tokens. Le modèle
  relit toute la conversation à chaque tour. **Une conversation longue ralentit deux fois** —
  la machine chauffe *et* il y a plus à relire. `/bye` remet le compteur de lecture à zéro.
- **Mesure « avant » du jeu d'or établie (Q-001, Q-002)** sur du droit belge, sans corpus :
  **deux échecs**. Vocabulaire faux (actionnaires pour une ASBL, qui a des membres), droit
  **périmé d'avant la réforme de 2019**, raisonnement inventé, et surtout **une institution
  fabriquée de toutes pièces** — « la Commission des Comptes » n'existe pas. Un seul point
  réussi : le refus d'inventer un montant d'amende.
- **Le constat qui compte** : le modèle se trompe **du même ton** qu'il a raison. Sur du droit,
  qui ne connaît pas déjà la réponse ne peut pas faire la différence.
- **Réserve appliquée à moi-même** : mes corrections de droit belge sont **NON VÉRIFIÉES**
  tant qu'une source primaire datée ne les confirme pas. Remplacer une invention par une
  affirmation non sourcée n'est pas un progrès, juste un changement d'auteur.
- **Toujours manquant, et désormais bloquant** : l'usage n°1 de Chaima. Le jeu d'or ne peut
  pas être figé sans lui.

## SNAPSHOT 2026-09-16 (5) — L'IA locale RÉPOND. Première mesure, première hallucination.

- **Couche 1 complète et fonctionnelle. VÉRIFIÉ.** `qwen2.5:3b` téléchargé (1,9 Go) et
  répondant sur la machine de Chaima. Le système existe.
- **Première mesure réelle : `eval rate` = 8,10 tokens/s** — environ 2× la vitesse de la
  parole, un paragraphe en 20 à 30 secondes. **Mesure à froid**, donc le **meilleur** cas :
  sur une puce mobile 15 W qui se bride, la mesure après 10 min de charge sera plus basse et
  reste à faire. Les estimations de `memoire/MACHINE.md` sont remplacées par ce relevé.
- **Le modèle a halluciné au premier échange** : il a déclaré fautive une commande correcte et
  inventé un nom de modèle inexistant (`qwen-2.5-v1:3b`), avec une assurance parfaite, en
  anglais. **Consigné comme le relevé le plus instructif du projet** (`mesure/JEU-D-OR.md`) :
  un 3B ne sait pas, il produit du plausible — ce qui démontre sur ses propres données
  pourquoi le corpus est le cœur d'ATLAS, et referme le débat sur le fine-tuning pour un
  second motif, démontré cette fois.
- **ERR-ATLAS-002** : mon bloc de commande était le dernier élément copiable avant l'invite du
  modèle — face à une invite, on recolle ce qu'on a sous la main. Règle **R-011** posée.
- **Décision qui approche** : rester en 3B (rapide, invente plus) ou passer en 7B (meilleur en
  français, projeté à 3-4 tokens/s). **Se tranchera sur le jeu d'or, pas sur une préférence.**

## SNAPSHOT 2026-09-16 (4) — Couche 1 posée : Ollama installé et lancé

- **Ollama installé et en fonctionnement. VÉRIFIÉ** par capture d'écran de l'application
  ouverte (une application ne s'ouvre pas si elle n'est pas installée). Premier composant du
  système local en place. **Geste de Chaima**, comme le veut le §10 — ATLAS a recommandé,
  elle a exécuté.
- **Alerte `sentinelle-exfiltration` levée à l'ouverture, avant tout clic** : la page d'accueil
  de l'application est un catalogue d'**applications tierces à connecter** (Claude Code,
  Codex CLI, Copilot CLI, Hermes, Cline…). Plusieurs sont des outils **cloud**. Le simple fait
  qu'Ollama soit installé localement **ne rend pas local** ce qui s'y branche. Point de
  vigilance inscrit : un système « local avec repli cloud » est cloud les jours où la question
  est difficile (R-004).
- **Aucun modèle téléchargé à ce stade.** Volontaire : on vérifie le moteur avant de dépenser
  2 Go et du temps de diagnostic sur deux problèmes au lieu d'un.
- **Aucune mesure de débit encore.** Les estimations de `memoire/MACHINE.md` restent
  **NON VÉRIFIÉES** jusqu'au premier relevé réel, sur secteur, après 10 minutes de charge.

## SNAPSHOT 2026-09-16 (3) — Matériel VÉRIFIÉ, un palier fermé pour de bon

- **Volet matériel de l'ÉTAPE 0 : CLOS.** Windows 11 Pro · **15,9 Go de RAM** ·
  **Intel i7-8650U** (4c/8t, puce mobile) · **Intel UHD 620 intégrée — aucune accélération
  exploitable** · **120,2 Go libres**. Preuve : sortie PowerShell en capture d'écran.
- **Conséquence dure, écrite plutôt qu'adoucie :** tout tournera **sur le processeur**. Un
  modèle de 3 à 8 milliards de paramètres quantifié, pas davantage. Pas d'images, pas de
  gros modèle, et **le palier fine-tuning LoRA/QLoRA est FERMÉ** — motif matériel définitif,
  qui s'ajoute au refus par défaut de `atlas-finetuning`.
- **La contrainte valide la stratégie au lieu de la contrarier :** le modèle ne pouvant pas
  être gros, toute la valeur doit venir du corpus et de la mémoire — exactement ce que Chaima
  demandait. Plus aucune ambiguïté sur où investir l'effort.
- **Estimations de débit inscrites comme NON VÉRIFIÉES** (R-003), avec leur condition de
  remplacement : une mesure réelle après 10 minutes de charge, sur secteur.
- **Rien installé.** Installer un logiciel est un geste de Chaima (§10).

## SNAPSHOT 2026-09-16 (2) — OS VÉRIFIÉ + première erreur ATLAS consignée

- **OS confirmé : Windows 11, build `10.0.26200.9457`, session `C:\Users\Chaima`.** Preuve :
  capture d'écran de l'invite de commandes. Passe de PLAUSIBLE à **VÉRIFIÉ** — et la preuve
  vient de l'échec de la commande, pas de son succès.
- **ERR-ATLAS-001 ouverte** : mon instruction a envoyé Chaima dans `cmd.exe` au lieu de
  PowerShell, et ma section « si ça rate » ne contenait pas l'échec réel. Faute d'agent, pas
  d'utilisatrice. Règle **R-010** posée : toute instruction doit porter le repère qui dit où
  on est (`PS` avant le curseur), et la liste des échecs doit contenir l'échec réel.
- **La boucle d'apprentissage a tourné pour de vrai** : une erreur réelle → une entrée datée →
  une règle qui l'empêche de se reproduire, dans le même tour. C'est le premier tour complet.
- **Toujours NON VÉRIFIÉ** : RAM, carte graphique, VRAM, disque libre. Rien n'est installé.

## SNAPSHOT 2026-09-16 — Rangement en sous-dossiers + profil de Chaima ouvert

État réel vérifié par `git ls-remote` : branche `claude/nifty-shannon-u87dv8` à `0e9240f`,
`main` inchangé.

- **Structure en sous-dossiers créée** à la demande de Chaima, avec `ROUTAGE.md` : un type
  d'information = un sous-dossier = **un seul fichier vivant**, où l'on ajoute en tête. Jamais
  un fichier daté par événement — c'est ça qui fait s'entremêler les documents.
- **Trois informations recueillies sur Chaima** et consignées dans `memoire/PROFIL-CHAIMA.md` :
  elle ne code pas encore bien (⇒ tout doit être copiable-collable, une action à la fois) ;
  elle veut un système « inarrêtable » ; elle veut du rangement strict.
- **Recherche dans le Drive : les caractéristiques machine n'y sont PAS.** Un seul document
  mentionne de la RAM — le guide d'examen MQ06 (Windows Server 2022, VM 16 Go) — c'est un
  **exercice d'école, pas la machine de Chaima**. S'en servir aurait violé R-003. L'ÉTAPE 0
  reste donc ouverte : **NON VÉRIFIÉ**.
- **Drive rangé** : dossier dédié `ATLAS — IA locale (Empire Chaima)` créé, contenant
  `01 — FICHE MACHINE — À REMPLIR` (vide, en attente de Chaima) et `02 — ERREURS ET
  RÉUSSITES — ATLAS`. Les deux contenus **relus après écriture** — une création Drive peut
  renvoyer un succès et un document vide, constaté aujourd'hui.
- **Écart connu, non corrigé** : le document Drive `02` cite les anciens chemins
  (`codex/atlas/JOURNAL-APPRENTISSAGE.md`…) d'avant le rangement en sous-dossiers. L'outil
  disponible ne modifie que le titre et l'emplacement d'un document, pas son contenu. Sans
  conséquence — le document dit lui-même que **le dépôt a raison** — et corrigé à la première
  remontée réelle. Signalé plutôt que tu, conformément au §5.
- **OS : « je pense windows » (Chaima, 2026-09-16).** Consigné **PLAUSIBLE, fiabilité
  MODÉRÉE** — pas VÉRIFIÉ. Une commande PowerShell lui a été donnée, choisie pour être **sa
  propre preuve** : si elle s'exécute, c'est Windows ; si elle échoue, ce n'en est pas. Aucune
  installation ne partira d'une impression.
- **Rien installé, rien acheté, rien engagé.**
