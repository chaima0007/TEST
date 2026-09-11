# 📋 JOURNAL — chaîne Veille, Brevets, Technologies & Capitaux

> Snapshot par session de travail sur cette chaîne. Ajout en haut, jamais d'écrasement.

## 2026-09-11-17h35 (Europe/Brussels) — Points 1, 4 exécutés · 3 bloqué · 5 proposé · Caelum Partners

**Contrôle honnête (§11)** — Aucun document quasi identique : un plan (neuf) et une fiche E-17 (ajout).
La condition d'arrêt a fonctionné, et mieux que ça : ce cycle a **réduit** la duplication au lieu d'en
créer. **ÉLAGUEUR non saisi**, motif : aucune boucle, aucune piste morte.

**Point 1 — FAIT.** Les 13 agents réduits à un pointeur de 2 lignes vers `CLAUDE.md` §2 ter + la base.
Le texte normatif vivait en 14 endroits : c'était reproduire la divergence d'E-01. 8 sections par agent
désormais, contre 9.

**Point 3 — BLOQUÉ, pas oublié.** `caelum-coffre` **n'a pas pu être créé** : l'API GitHub répond
**403 « Resource not accessible by integration »**. L'intégration de cette session n'a pas le droit de
créer un dépôt. Ce n'est pas un échec transitoire (E-16 : « non autorisé », pas « en échec ») — aucune
relance ne le résoudra. À créer par Chaima, ou en élargissant les droits de l'intégration.

**Point 4 — FAIT.**
- `agents/base_erreurs.py` : passerelle de la flotte Python vers la base. Conception clé — il **lit**
  `.claude/BASE-ERREURS.md` et `CLAUDE.md`, il ne recopie rien. Preuve que ça marche : l'ajout d'E-17
  a été repris par le module **sans aucune modification de code**.
  Échec bruyant volontaire : une base illisible lève une exception au lieu de retourner vide — ne jamais
  laisser croire « aucune erreur connue » quand la réponse est « je n'ai pas pu vérifier » (E-16).
  Greffé au démarrage de `main_loop()`. Testé : import OK, 17 fiches lues,
  `pour_action("je crée un dossier au Drive")` → E-01, E-03, E-12, E-14.
- `.claude/FRONTIERE-SUBSTRATS.md` : la frontière des deux substrats, avec qui possède quoi, la règle
  d'arbitrage, les interdits croisés, et la seule chose qui traverse (la base). Référencée au
  `CLAUDE.md` §2 ter, point 3.
- Couverture réelle corrigée : la règle atteint désormais les **75** agents (42 Markdown + 33 Python),
  contre 42 auparavant.

**Point 5 — PROPOSÉ, NON EXÉCUTÉ.** Plan à 3 options au Drive (« Plans de mise en œuvre »).
En établissant les faits, une **Option 0** est apparue, non envisagée dans la demande : retirer les
autres produits de la liste blanche de publication. Elle supprime le coût réel du mélange — la dilution
du positionnement de Caelum — en ~30 minutes, sans toucher à la production. Recommandé : Option 0
maintenant, Option B (mono-repo cloisonné + contrôle CI) ensuite si besoin, Option A (3 dépôts)
seulement quand un produit gagne domaine et revenus.

**Trouvé en chemin — E-17 ajoutée à la base (17 fiches).**
Le commentaire de `deploy.yml` documente l'incident d'exposition signalé par Chaima au départ : le
workflow publiait `path: '.'`, donc `CLAUDE.md`, `ETAT.md`, `reports/`, `.claude/`, `agents/` et un CV
étaient lisibles sur `caelumpartners.agency`. Il **manquait** à la base. Cause racine : liste noire
implicite — tout publié sauf ce qu'on pense à exclure. Corrigé de longue date par liste blanche + 2
garde-fous bloquants ; la fiche existe pour qu'ils ne soient jamais affaiblis.

**Autre fait établi, qui change le point 5 :** un seul domaine (`caelumpartners.agency`) sert les trois
produits sous des sous-chemins. Et la flotte Python n'est pas séparable proprement —
`decision_simulator.py` (Caelum + CompeteIQ) et `gdpr_garde.py` (Caelum + KMM) servent deux produits.

**Vérifié (avec preuve)** — 8 sections par agent après réduction · `py_compile` sur `main.py` et
`base_erreurs.py` · import et fonctions testés hors `main.py` · contrôle sécurité du projet **VERT sur
les contrôles bloquants** après chaque modification · push vérifié · read-back Drive.

**Reste / en attente de Chaima** — création de `caelum-coffre` (droits) · résultat du check TMview ·
feu vert Option 0 et choix Option A/B · aucune PR, aucun merge.

## 2026-09-11-16h55 (Europe/Brussels) — Base d'erreurs + contrôle avant rapport · Caelum Partners

**Contrôle honnête (nouvelle règle §11, appliquée dès cette entrée)**
- Documents quasi identiques produits récemment ? **Non.** Les 13 documents de rôle partagent une
  structure mais diffèrent en substance (mission, déclencheur et décision possédée distincts) — c'est
  la demande de Chaima, pas de la duplication. Le rectificatif de 16h40 recouvre la table de 16h20 sur
  le fond, mais il existe **parce que** l'écrasement est interdit : c'est la règle qui fonctionne.
- Condition d'arrêt fonctionnelle ? **Oui**, et vérifiable : aucun document neuf n'a été créé pour un
  état inchangé ; le `Calendrier des expirations` a été déposé à **0 entrée** plutôt que rempli de
  fiction ; aucune entrée de journal n'a été écrite sans changement d'état réel.
- **ÉLAGUEUR non saisi**, motif : aucune piste morte, aucune boucle. Un seul point de dérive signalé,
  de forme et non de fond — la charte a reçu 5 sections en un jour et devient longue (travers E-04).
  Consolidation datée à proposer par l'ARCHITECTE, inscrite en dette dans la charte §11.

**Fait — aux deux emplacements demandés**
- **Base d'erreurs : 16 fiches.** GitHub : `.claude/BASE-ERREURS.md` (dépôt Caelum, branche
  `claude/chaine-veille-13-agents`), placée à côté des agents pour qu'ils puissent la lire réellement.
  Drive : miroir dans « Synergies inter-agents ».
- Les 3 erreurs nommées par Chaima y sont : E-01 (règle anti-doublon de juillet ignorée un mois),
  E-02 (faux positif « PR#2 non mergée » répété ~30 fois), E-03 (`fileSize` trompeur → read-back).
- **13 autres erreurs ajoutées**, identifiées le même jour : titres de 300-400 caractères · index
  obsolète · deux conventions concurrentes · deux flottes d'agents dont une non documentée · dépôt
  public sans LICENSE · dépôt public inapte à sauvegarder du sensible · entité HTML littérale · clone
  superficiel pris pour l'historique · conversion Drive altérante · recherche web prise pour un
  registre · deux racines projet · contenu déposé dans le mauvais dépôt · service en échec pris pour
  inexistant.
- **6 des 16 fiches sont des fautes commises par un agent ce jour** (E-03, E-10, E-11, E-12, E-14,
  E-15). Une base qui ne contiendrait que les erreurs des autres serait fausse.
- **Règle de contrôle avant rapport** inscrite au `CLAUDE.md` **§2 ter** du dépôt Caelum — le seul
  document que les 42 agents appliquent. La charte seule n'aurait lié que les 13.
- Les 13 agents portent désormais 9 sections : + « AVANT D'AGIR — BASE D'ERREURS » et « AVANT TOUT
  RAPPORT — CONTRÔLE HONNÊTE ».

**Vérifié (avec preuve)**
- `.claude/BASE-ERREURS.md` : 19 417 octets, 16 fiches (comptage `grep`).
- 9 sections confirmées dans chacun des 13 agents.
- Contrôle sécurité du projet relancé après modification : **VERT sur les contrôles bloquants**.
- Push vérifié sur les deux dépôts. Read-back Drive effectué.

**Non fait, volontairement**
- **Les 29 agents préexistants n'ont pas été modifiés un par un.** La règle les lie via le
  `CLAUDE.md` §2 ter, ce qui suffit et évite 29 modifications dans un système qui n'est pas le mien.
- **Aucune PR, aucun merge.** `CLAUDE.md` est un fichier maître : sa modification attend l'accord de
  Chaima et reste sur la branche.

## 2026-09-11-16h40 (Europe/Brussels) — 13 agents créés sur décision de Chaima · Caelum Partners

**Décision reçue et exécutée**
- Chaima n'a pas retenu la recommandation de fusion : les 13 rôles restent **distincts et nommés**.
  Après explication du raisonnement, elle a confirmé et demandé de vrais fichiers, pas de la
  documentation. Exécuté. La recommandation de 16h20 est annulée par un rectificatif daté (le document
  d'origine n'a pas été écrasé).
- Position révisée honnêtement : deux de ses arguments implicites étaient plus forts que les miens —
  l'indépendance du CONTRÔLEUR est structurellement impossible à obtenir d'un agent unique, et
  l'asymétrie des coûts (faux GO brevet vs cycle gaspillé) justifie la redondance. Maintenu et non
  contesté : l'orchestration reste subordonnée à `meta-orchestrateur`.

**Fait — aux deux emplacements demandés**
- **GitHub** : 13 fichiers `.claude/agents/*.md` dans `chaima0007/keywordmoneymaker`, branche
  `claude/chaine-veille-13-agents`. Parc : **29 → 42 agents**. Accès en écriture obtenu en cours de
  session (le dépôt n'était accessible qu'en lecture jusque-là).
- **Drive** : 13 documents dans « Synergies inter-agents », un par rôle, + 1 rectificatif.
- Chaque agent porte 7 sections dont les 5 demandées : mission · déclencheur · décision possédée ·
  interdits · passation.
- Garde-fous inscrits dans chaque fichier : condition d'arrêt anti-boucle · rappel art. 54 CBE (ce
  dépôt est public) · subordination hors domaine · GUETTEUR strictement défensif.

**Vérifié (avec preuve)**
- Contrôle de forme des 13 : frontmatter valide, `name` conforme au nom de fichier, 7 sections
  présentes dans chacun — identique à la structure des 29 existants (comparaison faite sur
  `qa-verificateur.md`).
- **Contrôle sécurité du projet** (`scripts/audit_code_sur.py`, règle §2 bis du `CLAUDE.md`) exécuté :
  **VERT sur les contrôles bloquants** (secrets, code à risque). Les 2 avertissements — 4 actions CI
  non épinglées par SHA, 3 licences non vérifiées — sont **préexistants** et sans lien avec ces fichiers.
- Read-back Drive : les 14 documents listés avec une taille réelle de 2,5 à 6,8 Ko.
- Push vérifié sur les deux dépôts.

**Non fait, volontairement**
- **Aucune PR, aucun merge vers `main`.** La fusion est une décision de Chaima. Branche poussée, prête.
- Nommage de fichier choisi `gardien-controle-final` et non `gardien`, pour ne pas entrer en collision
  avec l'agent existant `gardien-juridique-verite`. Deux gardiens, deux périmètres.

## 2026-09-11-16h20 (Europe/Brussels) — Décisions de Chaima appliquées · projet : Caelum Partners

**Décisions reçues et exécutées**
- Les **3 rôles** (DÉPOSANT · HORLOGER · ÉLAGUEUR) et les **5 améliorations** sont ACCEPTÉS.
  Intégrés à la charte, §6 et §7. La chaîne passe à **38 rôles**.
- **Arbitrage des deux racines Caelum :** Chaima retient le dossier existant déjà structuré et actif,
  « 🗂️ Caelum — Journal d'Audit (Travaux techniques) ». Exécuté : `Veille & Opportunités` et ses
  32 sous-dossiers y ont été déplacés ; le conteneur `Caelum Partners` créé plus tôt aujourd'hui,
  vérifié **vide**, a été mis à la corbeille (récupérable, non supprimé définitivement).

**Fait**
- **Amélioration n°2 livrée** — table de correspondance des **29 agents en place vs 38 rôles**
  (Drive, « Synergies inter-agents »). Résultat : le recouvrement est concentré sur **deux couches
  seulement**, l'orchestration et la vérification. 13 rôles n'ont pas à être créés comme agents
  autonomes ; **17 sont réellement nouveaux** et s'activent sans conflit ; 8 voient leur périmètre
  restreint. Règle d'articulation retenue : la chaîne veille **se branche sous** `meta-orchestrateur`
  comme un domaine, elle ne se place pas à côté.
- Charte complétée : condition d'arrêt anti-boucle (§7.1), articulation (§7.2), dépôt privé (§7.3),
  plafond de nommage à 120/60 caractères (§7.4), première vague à 5 offices (§7.5).

**Vérifié (avec preuve)**
- Les 29 agents lus un par un dans `.claude/agents/*.md` — pas résumés, lus.
- `CLAUDE.md` §2 et §2 bis lus intégralement : la qualité en 3 couches et la chaîne de vérification
  du code tiers **existent déjà**. La chaîne veille s'y rattache au lieu de les dupliquer.
- Dossier `Caelum Partners` vérifié vide (requête Drive sur ses enfants) **avant** mise à la corbeille.
- Read-back des documents Drive après création.

**Trouvé — à arbitrer par Chaima (préexistant, hors périmètre)**
- Le dépôt Caelum contient **deux flottes distinctes** : 29 agents Markdown dans `.claude/agents/`
  et ~35 modules Python dans `agents/` (`avocat.py`, `fiscaliste.py`, `innovateur.py`,
  `superviseur.py`, `commandant.py`…). Le `CLAUDE.md` ne décrit que la première. Doublon structurel
  antérieur à cette chaîne. **Rien n'a été fusionné ni supprimé.**
- Angle mort dans les deux systèmes : `accessibilite` (WCAG) n'a aucun rôle correspondant dans la
  chaîne des 38.

**Contradiction de normes trouvée (consignée, non tranchée unilatéralement)**
- Le dossier Journal d'Audit contenait déjà un « LISEZ-MOI — Règles du journal » du **2026-07-13**
  portant une convention de nommage **différente** de celle donnée par Chaima ce jour. Les deux ne
  peuvent pas coexister. Retenu en attendant arbitrage : la convention du 2026-09-11 prévaut.
  **Le document existant n'a pas été modifié.** Détail : charte §8.
- Enseignement : la règle anti-doublon **existait déjà** au 2026-07-13 (« avant de créer un fichier, on
  vérifie qu'il n'existe pas déjà »). Elle a été enfreinte une trentaine de fois en juillet-août.
  L'amélioration §7.1 ne crée donc rien de neuf — elle **rétablit** une discipline abandonnée. Le
  manque n'était pas la règle, mais un rôle habilité à arrêter la boucle : c'est l'ÉLAGUEUR.
- L'« Index des entrées » du LISEZ-MOI est obsolète (1 ligne pour ≥ 9 documents). Non corrigé sans accord.

**Reste / bloqué (inchangé depuis 15h59)**
- **Marque « Caelum Partners » : NON VÉRIFIÉ** — registres EUIPO/BOIP non interrogeables d'ici.
  Premier dossier du DÉPOSANT dès que la vérification est faite. Risque commercial actif.
- Rôle 1 SCANNER : non commencé. Cadence désormais bornée à 5 offices en première vague.
- Dépôt privé pour le Coffre : non créé — il portera un nom sous le compte GitHub de Chaima,
  j'attends son accord sur ce point précis avant de créer quoi que ce soit.
- Dépôt Caelum sans `LICENSE` : à corriger par le DÉPOSANT (accès en écriture non disponible d'ici).

## 2026-09-11-15h59 (Europe/Brussels) — Session d'amorçage · projet : Caelum Partners

**Fait**
- Structure Drive créée : `Caelum Partners/Veille & Opportunités/` + 8 catégories + bibliothèque
  brevets à 22 juridictions + « Opportunités académiques non exploitées » = **33 dossiers**.
  Placée à la racine du Drive, pas dans le dossier transversal « COMPILATION & SYNOPSIS » (règle
  « par projet, jamais mélangé »).
- Projet identifié et lu : Caelum Partners = RegTech conformité PME belges (Peppol, NIS2, RGPD,
  lanceurs d'alerte, CSRD/DORA) + simulateur « Suis-je concerné ? » calculé côté client.
  Dépôt `chaima0007/keywordmoneymaker`, HEAD `c1de9a9`.
- **Rôle 0 INSPECTEUR** — verdict n°1 rendu sur le simulateur de conformité : **NO-GO brevet**,
  trois motifs indépendants (exclusion art. 52 CBE / nouveauté détruite art. 54 / absence
  d'activité inventive art. 56). Objection du CONTRADICTEUR intégrée et traitée.
  Titres alternatifs identifiés : droit d'auteur (acquis), droit *sui generis* des bases de données
  (l'actif le plus solide), marque (à vérifier), secret d'affaires (indisponible car dépôt public).
- Charte de chaîne + convention de nommage + règle de divulgation : ce dépôt, `veille/`.
- `Calendrier des expirations à venir` créé au Drive : **0 entrée**, honnêtement vide, avec les
  colonnes obligatoires et les 4 axes de recherche retenus pour le premier passage SCANNER.

**Vérifié (avec preuve)**
- Clone anonyme du dépôt Caelum réussi → dépôt **public** confirmé.
- Scan de secrets sur le dépôt Caelum : **0 correspondance réelle** (les seules occurrences sont les
  regex du scanner du projet lui-même). Bon point.
- Read-back du document INSPECTEUR après création au Drive : contenu complet et intègre.
- Base juridique COMVIK (T 641/00) et G 1/19 confirmée sur sources publiques datées.

**Reste / bloqué**
- **Marque « Caelum Partners » : NON VÉRIFIÉ** — EUIPO eSearch et BOIP sont des applications
  JavaScript non interrogeables depuis cet environnement. Aucun résultat inventé. À faire dans un
  navigateur. **Risque commercial actif** : le nom est déjà exploité publiquement.
- Rôle 1 SCANNER : non commencé (22 offices). Axes de recherche définis, priorités posées.
- Sauvegarde GitHub du contenu sensible : **impossible en l'état** — dépôt Caelum public, dépôt privé
  requis. Accès en écriture au dépôt Caelum non disponible depuis cette session (lecture seule).
- Dépôt Caelum **sans fichier LICENSE** → ambiguïté sur les droits des tiers. À corriger.
- Recouvrement à résoudre : 29 agents déjà en place dans le dépôt Caelum vs les 35 rôles de cette
  chaîne (voir charte §5).

**Dépend de Chaima**
- Accord sur les rôles et améliorations proposés (rien n'a été ajouté sans accord).
- Vérification de la marque au registre, ou mandat pour la faire faire.
- Décision sur le dépôt privé de sauvegarde.
