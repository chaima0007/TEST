# 📋 JOURNAL — competeiq / Patchou

> Rituel §5. Rien n'a changé → une seule ligne « SNAPSHOT [date] : aucun changement ».
> Quelque chose a changé → une entrée datée et précise. Un événement réel = une entrée.

---

## SNAPSHOT 2026-09-06 23h11 CEST — installation du CODEX

**État réel vérifié (git, pas mémoire) — avec correction d'un constat erroné :**
- Au démarrage de session, le checkout LOCAL était **périmé** (bloqué sur `cbe82e0`, vieille lignée « competeiq premium »).
  J'ai d'abord écrit à tort que la passation antérieure « n'existait pas / conteneur réinitialisé ».
  **C'était FAUX.** `git fetch` l'a montré : la branche **distante** `origin/claude/shopify-app-development-ri1090`
  (tip `5a8ae37`, 22 commits) **contient bien** tout le travail antérieur — `ETAT.md`, `00-LIRE-D-ABORD.md`,
  `reports/`, `EQUIPE_AGENTS.md`, et **17 agents opérationnels Shopify** (`store-builder`, `connecteur-shopify`,
  `security-guardian`, `seo-strategist`, `dropship-ops`, …). Rien n'avait été perdu ; c'est mon clone local qui était en retard.
- Base de travail rétablie sur le distant réel (`git reset --hard origin/…`), puis commit CODEX ré-appliqué par cherry-pick.
- Date : `2026-09-06 23h11 CEST` — VÉRIFIÉ (`TZ="Europe/Brussels" date`, cohérent avec currentDate + en-tête protocole).
  (Les dates `2026-07-17` de `ETAT.md` viennent de la dérive d'horloge du bac à sable, déjà notée.)

**Changement de cette session (purement ADDITIF, zéro écrasement) :**
- Installé PROTOCOLE CODEX v.2026-09-06 en tête de `CLAUDE.md` (§15.1) — l'ancien `CLAUDE.md` ne contenait que `@AGENTS.md`, aucune perte.
- Créé structure §12 : `/codex/{candidates,expertise,opportunites,licences-sortantes}`, `A-DECIDER.md`, `EVOLUTION.md`, `🔴 ERREURS.md`, ce JOURNAL. (`/codex/` n'existait pas sur origin.)
- Ajouté **21 agents CODEX** dans `.claude/agents/` (noms distincts des 17 existants → aucune collision ; total 38). Ce sont la **couche de gouvernance** (§1 : scout, guardian-licences, sentinel-securite, avocat, contradicteur, arbitre-expert, verificateur-verite, …), au-dessus des 17 agents **opérationnels** Shopify déjà en place.
- Ajouté la skill `.claude/skills/debat/` (orchestration du Parcours 2).
- Ajouté le bloc « SPÉCIFIQUE PROJET — competeiq » (stack Next 16.2.9 / Prisma 7.8 / next-auth 5, commandes de vérif, pièges).

**Audit de cohérence §5.5 :** CLAUDE.md porte la version 2026-09-06 ✔ · structure /codex conforme §12 ✔ · 21 agents CODEX présents ✔ · coexistence avec les 17 agents opérationnels documentée ✔.
