# 📋 JOURNAL — CompeteIQ

Convention CANAL : une entrée = un événement réel. Snapshot quotidien §5 du protocole.
Rien n'a changé → une seule ligne. Pas de rapport quand il n'y a rien à rapporter.

---

## 2026-09-06

**SNAPSHOT 2026-09-06 : premier snapshot du dépôt — état de référence établi.**

État réel vérifié (tier-1, `git ls-remote origin`) :
- 39 refs distantes, dont ~20 branches `claude/*` ouvertes.
- `main` = `cbe82e0` ; branche de travail `claude/protocole-codex-empire-wa4gp6` partait
  du même commit.
- Aucun `/codex/`, aucun `JOURNAL.md`, aucun `🔴 ERREURS.md`, aucun `.claude/` :
  le protocole n'était pas encore installé sur ce dépôt.
- `package.json` : **aucun script `test`** — constat qui a motivé le rôle TESTEUR-ADVERSE (§13).

Changement : installation du PROTOCOLE CODEX v2 (2026-09-06) en tête de `CLAUDE.md`,
création de la structure `/codex/` conforme au §12, et ajout de 8 rôles complémentaires
(§13) implémentés comme sous-agents réels dans `.claude/agents/`.

Trois questions ouvertes déposées dans `/codex/A-DECIDER.md` — aucune tranchée seule.
