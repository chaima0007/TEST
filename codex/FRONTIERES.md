# /codex/FRONTIERES.md — chacun reste à sa place

> Créé le 2026-09-19 à la demande de Chaima : « surveille chaque projet, car ils se
> mélangent, et dis-leur que chacun reste à sa place. »
> Ce fichier est **descriptif et prescriptif** : il constate l'état réel, daté, puis pose la
> règle. Il ne supprime rien — supprimer une branche est une décision humaine (§10).

---

## 1. LA RÈGLE — trois lignes, valables pour tout agent et toute session

1. **Un projet = un dépôt = un dossier Drive.** Un travail qui ne concerne pas le projet de ce
   dépôt n'y crée **aucune branche**, **aucun fichier**, **aucun rapport**.
2. **Avant d'écrire, un agent nomme son projet.** Si le projet nommé n'est pas celui du
   `CLAUDE.md` qu'il vient de lire, il **s'arrête et le dit** — il ne « fait quand même », ni
   « range ici en attendant ».
3. **Le nom d'une branche doit décrire son contenu.** Une branche dont le nom ne correspond plus
   à ce qu'elle contient est un mélange déjà commencé.

Corollaire, qui est la raison d'être de la règle : le §4 du protocole rend `/codex/expertise/`
**transverse** — ce qu'un projet apprend, tous le savent. C'est la **connaissance** qui circule.
Le **code**, les **branches** et les **rapports**, eux, restent chez eux. Confondre les deux est
exactement ce qui produit l'état mesuré ci-dessous.

---

## 1 bis. PLAN DE RANGEMENT — les 20 branches, par TYPE de désordre

> Établi le 2026-09-19 en inspectant le **contenu réel** de chaque branche (arbre, ancêtre commun
> avec `main`, fichiers ajoutés), pas son nom. **Ceci corrige le classement du même jour**, qui
> mettait les 20 dans un seul sac : elles ne se rangent pas de la même façon, et deux d'entre
> elles ne sont même pas un problème de projet.

### TYPE 1 — Projet entier, aucun lien avec ce dépôt (4 branches)
Histoire **indépendante** : aucun ancêtre commun avec `main`. L'arbre est entièrement autre.
**Rangement = déménagement propre.** Créer un dépôt privé dédié, y pousser l'arbre tel quel.
Aucun risque : rien à démêler.

| Branche | Volume | Contenu réel | Dernier commit |
|---|---|---|---|
| `claude/gta-style-game-prototype` | 45 commits | `game/` + `presentation.html` | 2026-06-18 |
| `claude/multi-agent-migration-factory-riujie` | — | `SYSTEME_AGENTS/`, `AUDIT/`, scripts Python | 2026-07-17 |
| `claude/moonbow-website` | 9 commits | `website/` + `presentation.html` | 2026-06-16 |
| `claude/presentation-project-selection-vy1hb7` | — | `presentation.html`, `research_agent.py` | 2026-06-16 |

### TYPE 2 — Le code de CE projet, avec une application étrangère greffée dessus (10 branches)
Elles **partent de `main`** et ajoutent leur propre `app/`, `lib/`, `components/` — donc elles
**modifient les mêmes fichiers** que Nexus-Market. **C'est le type dangereux :** si l'une était
fusionnée dans `main`, du code étranger atterrirait dans le produit. *(Vérifié le 2026-09-19 :
aucune ne l'est.)*
**Rangement = extraction**, pas copie de branche : on ne garde que le dossier ajouté.

| Branche | Ce qu'elle ajoute par-dessus `main` |
|---|---|
| `claude/crm-sales` (47 commits) | `Dockerfile`, `docker-compose.yml`, `app/`, `lib/` |
| `claude/shopify-app-development-ri1090` (25 commits) | `EQUIPE_AGENTS.md` + registres complets |
| `claude/foot-site-business-plan-ch0jt0` (21 commits) | `feet-hub/`, `claude-mistral-duo/` |
| `claude/world-cup-2026-agents-mp6mi6` (11 commits) | `analyse-mondial-2026/` |
| `claude/empire-chaima-linux-game-54cqgy` (7 commits) | `fiches/` |
| `claude/day-trading-yahoo-finance-a0w3q8` | `app/`, `docs/`, `lib/`, `scripts/` |
| `claude/canvas-project-concept-c4htto` | `SIMULATIONS.md`, `app/`, `lib/` (Motif Studio) |
| `claude/mistral-mnwb5j` | `claude_mistral_chain.py`, `collab-ia/` |
| `claude/parents-enfants-mvp-1xwgqu` | `BULLE.md`, `app/`, `components/`, `lib/` |
| `claude/couples-app-mvp-chaima-fx3dya` | `app/`, `components/`, `lib/` |

### TYPE 3 — Pas un projet étranger : des DOCUMENTS écrits ici pour un autre projet (6 branches)
Ce sont des **sessions d'autres projets qui ont travaillé dans ce dépôt** et y ont laissé leurs
rapports. Il n'y a pas de code à déménager — quelques fichiers `.md`, parfois un dossier.
**Rangement = copier ces fichiers vers le bon dépôt / dossier Drive.** Et surtout : **la règle du
§1 empêche désormais que ça recommence** — c'est la seule prévention qui vaille ici.

| Branche | Ce qu'elle a laissé | Projet réel |
|---|---|---|
| `claude/nifty-shannon-u87dv8` | `codex/`, `scripts/` | **ATLAS** — actif le 2026-09-19 |
| `claude/wizardly-franklin-7gehzh` | `reports/` | Caelum + La Loi Avec Moi |
| `claude/beautiful-hawking-4w1zlm` | `codex/` | NON VÉRIFIÉ |
| `claude/adoring-albattani-ue4vtz` | `veille/` | Veille |
| `claude/chaima-patent-audit-ytcxq3` | `codex/` + registres | Audit brevets (transverse) |
| `claude/libre-accomplis-system-9wvsnf` | `codex/`, `docs/`, `tests/` | Libre Accomplis |

### 🔴 CORRECTION du 2026-09-19 — `beautiful-hawking` n'est PAS étranger
Son contenu est `codex/CARTOGRAPHIE.md` et `codex/agents-correspondance.md` : **la carte de CE
dépôt**, produite par le rôle `cartographe` (§1). Je l'avais classée étrangère sur la foi de son
nom. **Vérifié en l'ouvrant : elle est chez elle.** Le compte réel est donc **19 branches
étrangères, pas 20** — et la leçon vaut pour tout le classement : le nom d'une branche n'est pas
une preuve, dans un sens comme dans l'autre.

### NOMS DÉFINITIFS DES DÉPÔTS — tranché par Chaima le 2026-09-19 (« nom simple du projet »)

Tous **privés**. La branche est poussée telle quelle comme `main` du nouveau dépôt : pour le
Type 2, elle contient le squelette Next.js **plus** l'application du projet — c'est l'état
fonctionnel réel, et le découper casserait l'application.

| Branche actuelle | → Nouveau dépôt privé | Type |
|---|---|---|
| `claude/gta-style-game-prototype` | **`gta-prototype`** | 1 |
| `claude/moonbow-website` | **`moonbow`** | 1 |
| `claude/multi-agent-migration-factory-riujie` | **`migration-factory`** | 1 |
| `claude/presentation-project-selection-vy1hb7` | **`selection-projets`** | 1 |
| `claude/crm-sales` | **`crm`** | 2 |
| `claude/shopify-app-development-ri1090` | **`shopify-app`** | 2 |
| `claude/foot-site-business-plan-ch0jt0` | **`feet-hub`** | 2 |
| `claude/world-cup-2026-agents-mp6mi6` | **`mondial-2026`** | 2 |
| `claude/empire-chaima-linux-game-54cqgy` | **`fiches-linux`** | 2 |
| `claude/day-trading-yahoo-finance-a0w3q8` | **`day-trading`** | 2 |
| `claude/canvas-project-concept-c4htto` | **`motif-studio`** | 2 |
| `claude/mistral-mnwb5j` | **`collab-ia`** | 2 |
| `claude/parents-enfants-mvp-1xwgqu` | **`bulle`** | 2 |
| `claude/couples-app-mvp-chaima-fx3dya` | **`couples-app`** | 2 |
| `claude/nifty-shannon-u87dv8` | **`atlas`** | 3 → requalifié |

**`fiches-linux` — nom corrigé après ouverture :** la branche s'appelle
`empire-chaima-linux-game` mais contient `fiches/Disques.dc.html`, `Firewalld.dc.html`,
`Reseau.dc.html` — des **fiches de cours Linux/réseau**, pas un jeu.

**`atlas` — requalifié du Type 3 vers un dépôt à part entière :** la branche ne contient pas
« quelques documents » mais **toute la structure du projet ATLAS** (`codex/atlas/` : état,
routage, apprentissage, audits, continuité, corpus, délibérations dont statut légal et
encaissement). Un dossier Drive « ATLAS — IA locale (Empire Chaima) » existe déjà.

### Les 4 branches Type 3 restantes — documents, pas dépôts
`wizardly-franklin` (1 rapport d'heures Caelum + La Loi Avec Moi) · `adoring-albattani`
(3 chartes de veille) · `chaima-patent-audit` (audit brevets, transverse) ·
`libre-accomplis-system` (`docs/libre-et-accomplis/`). Destination : le dossier Drive du projet
concerné. Aucun dépôt à créer.

### ⛔ BLOCAGE CONSTATÉ le 2026-09-19 — création de dépôts impossible depuis une session d'agent
`POST https://api.github.com/user/repos` → **`403 Resource not accessible by integration`**.
L'intégration GitHub de cette session **n'a pas le droit de créer un dépôt**. Ce n'est pas un
réglage à trouver : c'est une permission absente, du même ordre que le proxy d'egress (ERR-024).
**Conséquence pratique :** les 15 dépôts doivent être créés **par Chaima**, vides, depuis
github.com/new (nom + « Private » + Create, sans README ni .gitignore). Dès qu'un dépôt existe,
le transfert de sa branche prend quelques secondes et se fait ici.

### Ce que ce classement change, concrètement
- **4 branches** se rangent en une opération simple et sans risque (Type 1).
- **10 branches** demandent une extraction soignée, une par une (Type 2) — c'est le gros du travail.
- **6 branches** ne demandent presque rien (Type 3) : ce sont des documents, et la règle du §1
  est le vrai correctif.

**Ordre recommandé :** Type 1 d'abord (preuve que la méthode marche), puis Type 3 (rapide), puis
Type 2 (le plus long, un projet à la fois). **Rien n'est supprimé à aucune étape** : on copie
vers la destination, on vérifie que la destination est complète, et le retrait d'ici — s'il a
lieu un jour — est une décision séparée de Chaima (§10).

---

## 2. ÉTAT MESURÉ — `chaima0007/TEST`, le 2026-09-19 (VÉRIFIÉ)

**38 branches distantes.** Périmètre annoncé du dépôt (`CLAUDE.md`) : TEST / Nexus-Market
(CompeteIQ), plus l'outillage Caelum qui y vit.

| | Nombre | |
|---|---|---|
| Branches **du projet** (Nexus-Market / CompeteIQ / Caelum / protocole de ce dépôt) | **18** | `main`, `chore/codex-protocole-structure`, `claude/nexus-market-agents-63dlku`, `claude/competitive-intel-saas-arch-rfh4x3`, `claude/code-review-setup-b8r9pn`, `claude/b2b-outreach-system-7ht0n9`, `claude/charming-galileo-cqhkn1`, `claude/swarm-50-agent-architecture-3l6cno`, `claude/protocole-codex-empire-wa4gp6`, les 4 `codex/*`, les 5 `feat/*` |
| Branches **d'autres projets** | **20** | jeu GTA · site moonbow · agents Coupe du Monde 2026 · day-trading · business plan foot · app parents-enfants · app couples · CRM · app Shopify · jeu Linux · Motif Studio (canvas) · classifieur PyTorch · mistral · libre-accomplis · audit brevets · migration factory · veille (`adoring-albattani`) · ATLAS (`nifty-shannon`) · rapports Caelum + La Loi Avec Moi (`wizardly-franklin`) · `beautiful-hawking` (contenu NON VÉRIFIÉ, sa pointe n'est qu'un merge de `main`) |

**Plus de la moitié du dépôt ne lui appartient pas.**

**Le mélange est ACTIF, pas historique.** Le 2026-09-14, l'audit comptait 33 branches. Le
2026-09-19 : 38. **+5 en 5 jours.** Trois ont bougé dans les 8 derniers jours :
- `claude/nifty-shannon-u87dv8` — **2026-09-19, aujourd'hui** — « feat(atlas): CAND-001 —
  verdict sécurité, Parcours 1 terminé ». Le projet **ATLAS** travaille dans ce dépôt **en ce
  moment même**.
- `claude/wizardly-franklin-7gehzh` — 2026-09-16 — rapports d'heures **Caelum + La Loi Avec Moi**.
- `claude/beautiful-hawking-4w1zlm` — 2026-09-16 — merge de `main`.

**Le cas le plus instructif :** `claude/empire-chaima-linux-game-54cqgy`, dont la pointe du
2026-09-11 est « fix(fiches): relecture technique des quatre fiches ». Une branche nommée
« jeu Linux » qui contient une relecture de fiches. Le nom ne décrit plus le contenu — c'est le
stade suivant du mélange, celui où même l'inventaire devient faux.

**Aucune de ces 20 branches n'est fusionnée dans `main`.** Chacune est donc la **seule copie**
de son travail. C'est précisément pourquoi il ne faut rien supprimer : la question est de
**déplacer**, jamais d'effacer. (Ligne déjà ouverte dans `A-DECIDER.md` depuis le 2026-09-14.)

---

## 3. CE QUI APPARTIENT À QUI — carte, à compléter par Chaima

| Projet | Dépôt attendu | Dossier Drive attendu | État |
|---|---|---|---|
| TEST / Nexus-Market (CompeteIQ) | `chaima0007/TEST` | — | En place |
| Caelum Partners | `chaima0007/keywordmoneymaker` | « Caelum Partners » (`1iMF5nd…`) | En place, mais des rapports Caelum vivent **aussi** dans `TEST` |
| La Loi Avec Moi | **NON VÉRIFIÉ** — dépôt non identifié depuis cette session | « La Loi Avec Moi » | Des rapports LLAM vivent dans `TEST` |
| ATLAS | **NON VÉRIFIÉ** | **NON VÉRIFIÉ** | Travaille dans `TEST` (branche `nifty-shannon`, active ce jour) |
| Les 17 autres | **aucun** — ils n'existent que comme branches de `TEST` | **NON VÉRIFIÉ** | À déplacer |

Cette carte est **incomplète, et je le dis plutôt que de la compléter au jugé** : je n'ai accès
qu'à `chaima0007/test` depuis cette session. Les dépôts réels des autres projets doivent être
nommés par Chaima, ou constatés depuis une session qui y a accès.

---

## 4. CE QUI EST À CHAIMA (§10) — rien ne sera fait sans elle

- **Déplacer** les 20 branches vers leurs dépôts propres (créer les dépôts, pousser, vérifier,
  et **seulement ensuite** envisager de retirer d'ici).
- **Supprimer** quoi que ce soit — branche ou fichier.
- Nommer les dépôts et dossiers Drive manquants de la carte ci-dessus.
- Adopter la règle du §1 dans le **bloc CODEX transverse**, pour qu'elle s'applique à tous les
  projets et pas seulement ici.

---

## 5. CE QUI SURVEILLE, DÉSORMAIS

L'agent **`gardien-des-frontieres`** (`.claude/agents/`) tient ce fichier à jour, recompte les
branches à chaque snapshot §5 et signale toute nouvelle entrée étrangère **le jour où elle
apparaît**, plutôt que trois mois plus tard. Il **signale, ne déplace jamais, ne supprime
jamais**.
