# 📋 JOURNAL — competeiq

> Rituel §5. Rien n'a changé → une seule ligne « SNAPSHOT [date] : aucun changement ».
> Quelque chose a changé → une entrée datée et précise. Un événement réel = une entrée.

---

## SNAPSHOT 2026-09-06 23h11 CEST — installation du CODEX

**État réel vérifié (pas de mémoire) :**
- Branche extraite : `claude/shopify-app-development-ri1090`, HEAD `cbe82e0` (« ci: code review setup … (#2) »).
- Constat de vérité : les fichiers de passation d'anciennes sessions (`ETAT.md`, `00-LIRE-D-ABORD.md`,
  `reports/`, commits `fed6bb0`/`5a8ae37`) **n'existent PAS sur cette branche** — conteneur réinitialisé
  entre sessions. Aucune continuité présumée. CODEX installé à neuf sur l'état réel.
- Date : `2026-09-06 23h11 CEST` — VÉRIFIÉ (`TZ="Europe/Brussels" date`, cohérent avec currentDate + en-tête protocole).

**Changement de cette session :**
- Installé PROTOCOLE CODEX v.2026-09-06 en tête de `CLAUDE.md` (§15.1).
- Créé structure §12 : `/codex/{candidates,expertise,opportunites,licences-sortantes}`, `A-DECIDER.md`, `EVOLUTION.md`, `🔴 ERREURS.md`, ce JOURNAL.
- Créé les 21 agents dans `.claude/agents/` et la skill `.claude/skills/debat/`.
- Ajouté le bloc « SPÉCIFIQUE PROJET — competeiq » (stack, commandes de vérif, pièges).

**Audit de cohérence §5.5 :** CLAUDE.md porte la version à jour (2026-09-06) ✔ · structure /codex conforme §12 ✔ · 21 agents présents ✔.
