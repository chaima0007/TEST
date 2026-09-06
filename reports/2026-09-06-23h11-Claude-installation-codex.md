# 2026-09-06-23h11 — Claude — Installation du PROTOCOLE CODEX EMPIRE CHAIMA (competeiq/Patchou)

## SYNOPSIS
**Quoi** : le PROTOCOLE CODEX (v.2026-09-06) est installé dans le dépôt selon son propre §15 — bloc en tête de `CLAUDE.md`, structure `/codex/` du §12, 21 agents de gouvernance, skill `debat`. **Pourquoi** : mettre le projet « en service sous protocole » (gouvernance, débat contradictoire, vérité sourcée). **État** : **FAIT et poussé** sur `claude/shopify-app-development-ri1090` (commits `7c84c29` + `3a12d28`, PR #7). Installation **purement additive** — les 17 agents opérationnels Shopify préexistants sont conservés (total 38). Aucune boutique n'est lancée ; rien d'engageant sans Chaima.

---

## AUDIT — FAIT / VÉRIFIÉ / RESTE

### FAIT + VÉRIFIÉ (avec preuve)
| Élément (§ CODEX) | Preuve vérifiable |
|---|---|
| §15.1 — bloc protocole en tête de `CLAUDE.md` | `head -3 CLAUDE.md` → « # PROTOCOLE CODEX — EMPIRE CHAIMA … 2026-09-06 » |
| §15.4 — spécificités projet ajoutées SOUS le bloc | section « SPÉCIFIQUE PROJET — competeiq » (stack, commandes de vérif, pièges) + `@AGENTS.md` préservé |
| §12 — structure identique | `/codex/{candidates,expertise,opportunites,licences-sortantes}` + `A-DECIDER.md` + `EVOLUTION.md` + `📋 JOURNAL.md` + `🔴 ERREURS.md` |
| §1 — les 21 agents | `ls .claude/agents | wc -l` → **38** (17 opérationnels préexistants + **21 CODEX** aux noms distincts, aucune collision) |
| §8 Parcours 2 — orchestration du débat | `.claude/skills/debat/SKILL.md` (avocat+contradicteur en parallèle → simulateur → arbitre → vérificateur → A-DECIDER) |
| §5 — snapshot d'entrée | `📋 JOURNAL.md` : SNAPSHOT 2026-09-06 23h11 CEST, état réel vérifié par git |
| §5 — passation à jour | `ETAT.md` : ligne de journal + horodatage 2026-09-06 ; `EVOLUTION.md` : jalon d'installation |
| Date réelle | `TZ="Europe/Brussels" date` → **2026-09-06 23h11 CEST** — VÉRIFIÉ, cohérent avec currentDate + en-tête protocole |
| Push | `git push` → `5a8ae37..3a12d28` (fast-forward, pas de force) |

### Correction d'un constat erroné (vérité totale, §13)
- Au début de session j'ai écrit que la passation antérieure « n'existait pas / conteneur réinitialisé ». **C'était FAUX.**
- `git fetch` a établi que la branche **distante** contenait bien tout le travail antérieur (`ETAT.md`, `00-LIRE-D-ABORD.md`, `reports/`, 17 agents). C'est le **checkout local qui était périmé** (bloqué sur `cbe82e0`).
- Correctif : base rétablie sur le distant (`git reset --hard origin/…`), commit CODEX ré-appliqué par cherry-pick, snapshot JOURNAL corrigé. Rien n'a été perdu ni écrasé.

### NON VÉRIFIÉ / limites honnêtes
- Les agents CODEX sont des **définitions** (fiches de rôle) : leur comportement en exécution réelle (Zone 1, débats) n'a **pas encore été exercé** → **PLAUSIBLE**, pas encore **CONFIRMÉ**.
- `npm run lint/typecheck/build` **non relancés** dans cette session : l'installation CODEX n'ajoute que du Markdown (`.md`) hors du code applicatif → impact build **PLAUSIBLE = nul**, non prouvé ici.

### RESTE (inchangé — bloquants humains, hors périmètre de cette tâche)
- Créer/connecter la boutique Shopify · réserver le nom (INPI + registrar) · commander l'échantillon · lancer le contenu organique. Aucun de ces gestes ne peut être fait par un agent (§10).

---

## Traçabilité
- Branche : `claude/shopify-app-development-ri1090` · PR #7 · commits `7c84c29` (install) + `3a12d28` (corrections).
- Session : https://claude.ai/code/session_019bs4H6doxQDEm1k3vFLchx
