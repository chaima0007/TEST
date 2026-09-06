# ETAT.md — journal de passation (dépôt `TEST` / CompeteIQ)

> Journal chronologique. **Ajout uniquement**, jamais d'écrasement. Entrée la plus récente en haut.

> ⚠️ **2026-09-06 — MIGRATION :** la passation canonique de ce dépôt est désormais le protocole
> CODEX → `📋 JOURNAL.md` (snapshots §5) + `/codex/EVOLUTION.md` (jalons) + `/codex/A-DECIDER.md`
> (décisions en attente). Ce fichier `ETAT.md` est conservé pour l'historique (add-only), plus alimenté.

---

## 2026-09-06-23h18 CEST — Claude (Opus 4.8) — Installation protocole CODEX

- Bloc CODEX (v. 2026-09-06) collé en tête de `CLAUDE.md` + spécificités projet ; `@AGENTS.md` conservé.
- Structure §12 créée (`/codex/*`, `📋 JOURNAL.md`, `🔴 ERREURS.md`, `.claude/*`).
- Commité + poussé sur `claude/chaima-patent-audit-ytcxq3` (`c2dab9b`, HEAD == origin).
- **RESTE :** 21 agents + skill `debat` NON fournis (non fabriqués volontairement) → à déposer par Chaima.
- Suite → voir `📋 JOURNAL.md` et `/codex/EVOLUTION.md`.

---

## 2026-07-17-21h34 CEST — Claude (Opus 4.8) — Audit brevets + livraison protocole

**Fait :**
- Audit de brevetabilité complet de CompeteIQ. Verdict : **0 invention brevetable** (SaaS CRUD standard, aucun effet technique art. 52 CBE). Zéro brevet/antériorité inventés.
- Rapport d'audit : `docs/audits/AUDIT_BREVETS_2026-07-17_2056.md` (commit `c5154cc`, poussé sur `claude/chaima-patent-audit-ytcxq3`).
- Rapport de livraison : `reports/2026-07-17-21h34-audit-livraison-competeiq.md` + copie Google Drive.
- Passation créée : `00-LIRE-D-ABORD.md`, `ETAT.md`.

**Vérifié (preuve) :**
- Push synchronisé : `HEAD == origin` = `c5154cc`.
- Dépôt PUBLIC : API GitHub `"private": false`.
- Aucun site live : `has_pages: false`, pas de CNAME.
- Agents demandés inexistants : `grep` négatif.

**Reste :**
- ⚠️ **Chaima : passer `TEST` en privé** (Settings → Danger Zone → Make private). Pas d'outil de visibilité disponible dans la session.
- Marque « CompeteIQ » : abandonnée (décision Chaima).
- Design Caelum / La Loi : hors périmètre (autres repos).

---
