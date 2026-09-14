# Audit des branches distantes — périmage vs `main` (2026-09-14)

> **Méthode.** Pour chaque branche : `git fetch origin --prune`, puis
> retard = `git rev-list --count <b>..origin/main`, et **fichiers à risque** =
> fichiers modifiés par la branche ET par `main` depuis leur point de fork
> (`git merge-base`). C'est ce croisement — pas le nombre de lignes — qui produit
> un conflit ou un écrasement. `origin/main` = `75ebe4af`.
>
> **Lecture seule.** Aucune branche n'a été modifiée, supprimée ni poussée par cet audit.
> Supprimer une branche est une action humaine (`CLAUDE.md` §10).

| Branche | Retard (commits) | Fichiers à risque | Verdict |
|---|---|---|---|
| `chore/codex-protocole-structure` | 41 | 10 | **PÉRIMÉE — 10 fichier(s) en collision** |
| `claude/adoring-albattani-ue4vtz` | 41 | 0 | en retard, sans collision |
| `claude/b2b-outreach-system-7ht0n9` | 42 | 5 | **PÉRIMÉE — 5 fichier(s) en collision** |
| `claude/beautiful-hawking-4w1zlm` | 1 | 2 | **PÉRIMÉE — 2 fichier(s) en collision** |
| `claude/canvas-project-concept-c4htto` | 42 | 2 | **PÉRIMÉE — 2 fichier(s) en collision** |
| `claude/chaima-patent-audit-ytcxq3` | 41 | 11 | **PÉRIMÉE — 11 fichier(s) en collision** |
| `claude/charming-galileo-cqhkn1` | 0 | 0 | À JOUR |
| `claude/code-review-setup-b8r9pn` | 42 | 7 | **PÉRIMÉE — 7 fichier(s) en collision** |
| `claude/competitive-intel-saas-arch-rfh4x3` | 42 | 3 | **PÉRIMÉE — 3 fichier(s) en collision** |
| `claude/couples-app-mvp-chaima-fx3dya` | 41 | 8 | **PÉRIMÉE — 8 fichier(s) en collision** |
| `claude/crm-sales` | 49 | 7 | **PÉRIMÉE — 7 fichier(s) en collision** |
| `claude/day-trading-yahoo-finance-a0w3q8` | 42 | 2 | **PÉRIMÉE — 2 fichier(s) en collision** |
| `claude/empire-chaima-linux-game-54cqgy` | 41 | 2 | **PÉRIMÉE — 2 fichier(s) en collision** |
| `claude/foot-site-business-plan-ch0jt0` | 42 | 0 | en retard, sans collision |
| `claude/gta-style-game-prototype` | 69 | 2 | **PÉRIMÉE — 2 fichier(s) en collision** |
| `claude/libre-accomplis-system-9wvsnf` | 42 | 33 | **PÉRIMÉE — 33 fichier(s) en collision** |
| `claude/mistral-mnwb5j` | 42 | 0 | en retard, sans collision |
| `claude/moonbow-website` | 69 | 2 | **PÉRIMÉE — 2 fichier(s) en collision** |
| `claude/multi-agent-migration-factory-riujie` | 69 | 2 | **PÉRIMÉE — 2 fichier(s) en collision** |
| `claude/nexus-market-agents-63dlku` | 12 | 3 | **PÉRIMÉE — 3 fichier(s) en collision** |
| `claude/parents-enfants-mvp-1xwgqu` | 41 | 0 | en retard, sans collision |
| `claude/presentation-project-selection-vy1hb7` | 69 | 2 | **PÉRIMÉE — 2 fichier(s) en collision** |
| `claude/protocole-codex-empire-wa4gp6` | 41 | 32 | **PÉRIMÉE — 32 fichier(s) en collision** |
| `claude/shopify-app-development-ri1090` | 42 | 36 | **PÉRIMÉE — 36 fichier(s) en collision** |
| `claude/swarm-50-agent-architecture-3l6cno` | 42 | 15 | **PÉRIMÉE — 15 fichier(s) en collision** |
| `claude/world-cup-2026-agents-mp6mi6` | 42 | 0 | en retard, sans collision |
| `codex/err-019-branche-perimee` | 0 | 0 | À JOUR |
| `codex/mesure-option3` | 0 | 0 | À JOUR |
| `codex/test-ecriture-env-defaut` | 40 | 1 | **PÉRIMÉE — 1 fichier(s) en collision** |
| `codex/testeur-adverse-garde-fou-survente` | 3 | 0 | en retard, sans collision |
| `feat/commercial-assets` | 42 | 9 | **PÉRIMÉE — 9 fichier(s) en collision** |
| `feat/commercial-gtm` | 42 | 9 | **PÉRIMÉE — 9 fichier(s) en collision** |
| `feat/infra-security` | 42 | 9 | **PÉRIMÉE — 9 fichier(s) en collision** |
| `feat/kb-api-stub` | 42 | 9 | **PÉRIMÉE — 9 fichier(s) en collision** |
| `feat/kb-seed` | 42 | 9 | **PÉRIMÉE — 9 fichier(s) en collision** |

---

## Ce qui compte réellement

**35 branches distantes. 26 sont périmées avec collision, 1 est à jour hors les miennes.**
Mais le nombre est trompeur : la plupart sont des branches abandonnées d'autres projets
(jeux, sites, prototypes) qui ne seront jamais mergées. Les classer « à risque » serait
du bruit.

**Une seule est opérationnellement dangereuse :**

### `claude/nexus-market-agents-63dlku` — la branche de dev déclarée du projet

`CLAUDE.md` la désigne comme **branche de dev** de TEST/Nexus-Market. Elle est **12 commits
en retard** sur `main` et entre en collision sur exactement les trois fichiers de
gouvernance du protocole CODEX :

| Fichier | Rôle | Conséquence d'un travail en aveugle |
|---|---|---|
| `codex/A-DECIDER.md` | §6 — le seul fichier à ouvrir | Décisions déjà tranchées par Chaima réaffichées comme en attente, ou lignes en attente perdues |
| `codex/EVOLUTION.md` | §6.5 — **APPEND-ONLY** | Une réécriture depuis l'état périmé **viole la règle append-only** : des jalons disparaissent |
| `📋 JOURNAL.md` | §5 — snapshots | Snapshots comparés à une base périmée → §5 conclut « aucun changement » alors que 12 commits ont eu lieu |

C'est le mécanisme exact d'ERR-011 et d'ERR-019 : ce ne sont pas des lignes de code,
ce sont les fichiers **qui portent les décisions**. Une session qui les réécrit depuis
l'état périmé efface des arbitrages humains — le seul dommage que le protocole traite
comme irréversible.

**Recommandation (§14 — je recommande, Chaima décide) :** `git merge origin/main` dans
`claude/nexus-market-agents-63dlku` avant la prochaine session qui y travaille. Merge et
non rebase : la branche est partagée. Conflit attendu sur les trois fichiers ci-dessus,
à résoudre en **union** pour `EVOLUTION.md` (append-only) et `A-DECIDER.md` (une ligne ne
disparaît que si Chaima a tranché, §6).

**Les 25 autres** : aucune action recommandée. Elles sont inertes tant que personne ne les
reprend. Si une session en reprend une, la règle `git fetch` désormais dans `AGENTS.md`
la corrigera à l'ouverture. Leur suppression est une action humaine (§10) et n'est **pas**
recommandée ici : je n'ai pas audité leur contenu, seulement leur position.

**NON VÉRIFIÉ :** lesquelles de ces 25 branches sont abandonnées pour de bon. Classement
fondé sur leur nom et leur retard (41-69 commits), pas sur une confirmation de Chaima.
