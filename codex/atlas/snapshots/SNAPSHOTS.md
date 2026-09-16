# ATLAS — SNAPSHOTS

> Rituel d'entrée §5, **avant toute autre tâche**. État réel **vérifié**, jamais de mémoire.
> Le plus récent en haut. Rien n'a changé → **une seule ligne**, puis silence.
> Un snapshot dit *ce qui a changé*. Il ne dit pas *si c'est cohérent* — ça, c'est `audits/`.

---

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
