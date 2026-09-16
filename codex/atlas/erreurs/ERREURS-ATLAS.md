# 🔴 ATLAS — ERREURS

> Une erreur **réellement survenue** = une entrée datée. Le plus récent en haut.
> Format fixe : **Ce qui s'est passé · Cause (confirmée par reproduction) · Comment la détecter
> la prochaine fois · Correctif (VÉRIFIÉ)**.
>
> **Toute entrée ici est remontée dans le Drive** (`../continuite/SYNC-DRIVE.md`).
> **Si Chaima doit corriger deux fois la même chose, c'est une entrée ici** — la boucle
> d'apprentissage est cassée, et c'est un incident en soi (`sentinelle-derive`, dérive n°1).
>
> Vérité totale : seules des erreurs réelles figurent ici, avec leur preuve. Pas d'erreur
> anticipée, pas d'erreur « probable ». Les risques prévus vivent dans les chartes d'agents.

---

## ERR-ATLAS-004 — Deux agents, un outil, une fausse accusation (2026-09-16)

**L'incident le plus instructif du projet à ce jour. Il a failli détruire la confiance dans
un dossier juste.**

- **Ce qui s'est passé :** deux chercheurs lancés en parallèle sur le droit belge.
  - Le **DOSSIER-01** a consulté ses sources primaires et cité des montants précis (INASTI) et
    le CSA via Justel, daté « mise à jour au 24-12-2025 ».
  - Le **DOSSIER-02** a testé 14 domaines officiels, reçu **403 sur les 14** via `WebFetch` et
    `curl`, et conclu — honnêtement, selon ce qu'il voyait — qu'**aucune source primaire
    n'était joignable dans cette session**.
  - Il en a tiré une **accusation** : des chiffres à la décimale, dans une session où rien ne
    s'ouvre, sont « vraisemblablement relayés eux aussi », donc **à vérifier avant de servir de
    base à une décision**.
- **Cause (CONFIRMÉE par test direct de l'orchestration) :** **asymétrie de connaissance
  d'outil**, pas de rigueur. `WebFetch` et `curl` sont bloqués ; **`mcp__Exa__web_fetch_exa`
  ne l'est pas.** DOSSIER-01 l'avait trouvé, DOSSIER-02 l'ignorait. Le second a donc pris **sa
  propre limite pour une propriété du monde.**
- **Résolution — par le test, pas par l'autorité.** L'orchestration a récupéré elle-même
  `inasti.be` et Justel via Exa. Justel a renvoyé « **mise à jour au 24-12-2025** » —
  **exactement** la date citée par DOSSIER-01. **Accusation réfutée : ses sources sont
  réelles.** `efacture.belgium.be` a été lu dans la foulée et confirme l'obligation
  d'e-facturation structurée depuis le 01-01-2026.
- **Ce qui est vraiment cassé, du coup :** le **DOSSIER-02**. Tout y est dégradé en
  « NON VÉRIFIÉ » ou « RELAYÉ » alors que les sources étaient lisibles. Sa découverte la plus
  lourde — l'obligation Peppol, qui pourrait empêcher Chaima de facturer par PDF — y est
  **non vérifiée alors qu'elle était vérifiable**. Dossier **relancé** avec le bon chemin.
- **Détection la prochaine fois :** un agent qui écrit « source inaccessible » **sans nommer
  les outils essayés**. Et tout désaccord entre deux agents où l'un affirme l'impossibilité de
  ce que l'autre a fait : **le plus souvent, celui qui a réussi a raison — l'échec ne prouve
  que son propre échec.**
- **Correctif (VÉRIFIÉ) :** R-014.

### Les trois choses que cet incident valide

1. **DOSSIER-02 a eu raison d'accuser.** Sur ce qu'il voyait, c'était le comportement correct :
   signaler, ne pas corriger le fichier d'autrui, ne pas contourner un refus de politique. **Il
   s'est trompé sans commettre de faute.** La distinction est capitale — on ne veut surtout pas
   décourager ce réflexe.
2. **La vérification tranche, pas l'ancienneté ni l'assurance.** Ni « l'accusateur a sûrement
   raison », ni « l'accusé se défend bien » : une requête, une date qui correspond, terminé.
3. **Un agent prudent peut produire un dossier inutilement faible.** Sur-marquer NON VÉRIFIÉ
   n'est pas neutre : ça rend une information exacte inutilisable. **L'excès de prudence a un
   coût, il est juste moins visible que l'excès de confiance.**

## ERR-ATLAS-003 — `printf` a dévoré le message de commit à « −10 % » (2026-09-16)

- **Ce qui s'est passé :** message de commit construit avec `printf` ; le shell s'arrête à
  `%,` et renvoie `printf: ',': invalid format character`. Le commit `c90a341` est parti avec
  **4 lignes sur 30**. Contenu des fichiers intact — seul le message est amputé.
- **Cause (CONFIRMÉE par le message d'erreur) :** dans `printf`, `%` introduit un format.
  `−10 %, sans` est lu comme la directive `%,`, qui n'existe pas. Rien à voir avec l'accent
  ou le caractère `−`.
- **Parenté :** c'est le **cousin d'🔴 ERR-017** (backticks interprétés par le shell dans un
  `commit -m`), déjà consignée sur ce dépôt. Même famille : *le texte français passe par une
  moulinette shell qui a ses propres caractères magiques.* La leçon d'ERR-017 avait été tirée
  pour les backticks seulement — trop étroitement.
- **Détection :** `printf: '…': invalid format character` juste avant un `git commit` qui
  réussit quand même. **Le commit ne rate pas** : c'est ce qui rend l'erreur silencieuse.
  Vérifier avec `git log -1 --format=%B`.
- **Correctif (VÉRIFIÉ) :** ne plus jamais construire un message de commit avec `printf`.
  Écrire le message dans un fichier par **heredoc `<<'MSG'`** (guillemets simples = aucune
  interprétation), puis `git commit -F fichier`. C'est ce qui était fait pour les premiers
  commits de ce projet, et qui marchait.
- **Non corrigé volontairement :** le message tronqué **reste tel quel**. Le réparer imposerait
  un `--amend` + `push --force`, interdits par **R-002**. Une règle qu'on contourne « juste
  cette fois » est une règle morte — et la vérité est dans les fichiers, pas dans le message.

## ERR-ATLAS-002 — Le bloc de commande invitait à être recollé (2026-09-16)

- **Ce qui s'est passé :** après le téléchargement du modèle, Chaima a collé
  `ollama run qwen2.5:3b --verbose` **dans l'invite `>>>` du modèle**, au lieu d'y écrire une
  question. Le modèle a traité la commande comme une question et a répondu à côté.
- **Cause :** l'instruction disait bien « quand tu vois `>>>`, écris-lui une vraie question ».
  Mais **le dernier élément copiable de mon message était la commande elle-même**. Face à une
  invite qui attend quelque chose, on recolle ce qu'on a sous la main. L'instruction était
  juste ; **sa mise en page disait le contraire.**
- **Détection :** le modèle répond *à propos de la commande* au lieu d'y obéir. Autrement dit,
  l'invite `>>>` n'est plus PowerShell : **elle ne prend plus de commandes, seulement du
  texte adressé au modèle.**
- **Correctif :** dire explicitement, à chaque commande qui ouvre une session interactive :
  **« cette commande est finie, ne la recolle pas — désormais tu parles au modèle. »** Et ne
  jamais laisser un bloc de commande comme dernier élément copiable avant une invite.
- **Conséquence heureuse :** l'erreur a produit le relevé le plus instructif du projet — le
  modèle a inventé un nom de modèle inexistant avec une assurance totale
  (`../mesure/JEU-D-OR.md`). Ça ne rachète pas le défaut d'instruction, mais ça se consigne.

## ERR-ATLAS-001 — L'instruction a envoyé Chaima dans la mauvaise fenêtre (2026-09-16)

- **Ce qui s'est passé :** instruction donnée — « touche Windows, taper `powershell`, Entrée ».
  Chaima s'est retrouvée dans **Invite de commandes** (`cmd.exe`), pas dans PowerShell.
  Le bloc de commandes fourni ne pouvait donc pas fonctionner.
- **Cause (CONFIRMÉE par la capture d'écran) :** l'instruction supposait que taper `powershell`
  dans la recherche Windows **ouvre** PowerShell. Selon ce qui est épinglé et ce que la
  recherche propose en premier, c'est `cmd.exe` qui s'ouvre. **L'instruction ne contenait
  aucun moyen pour Chaima de savoir dans quelle fenêtre elle était** — c'est ça, le vrai
  défaut : pas le mauvais programme, l'absence de repère pour le constater.
- **Aggravant, entièrement imputable à l'agent :** R-005 exigeait « la commande · la
  vérification · quoi faire si ça rate ». La partie « si ça rate » listait trois cas, **aucun
  n'était le bon**. Une liste d'échecs qui ne contient pas l'échec réel donne une fausse
  impression de filet de sécurité.
- **Détection la prochaine fois :** le texte avant le curseur. `C:\Users\Chaima>` = Invite de
  commandes. `PS C:\Users\Chaima>` = PowerShell. Le `PS` est le seul repère qui compte, et il
  doit être **dit à l'avance**, pas après la panne.
- **Correctif (VÉRIFIÉ sur la capture) :** ne plus demander d'**ouvrir** PowerShell, mais de
  taper `powershell` **dans la fenêtre déjà ouverte** — ça bascule dans la même fenêtre, rien
  à fermer, et le `PS` qui apparaît est la preuve visible que ça a marché. L'instruction porte
  désormais son propre test.
- **Gain collatéral :** la capture a livré `Microsoft Windows [version 10.0.26200.9457]` — l'OS
  est **VÉRIFIÉ** par l'échec lui-même. Une commande qui rate en disant qui elle est reste une
  commande utile.
