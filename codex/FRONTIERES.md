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
