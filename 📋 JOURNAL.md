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

---

## 2026-09-06 (2)

Changement : le pipeline §8 passe de décrit à exécutable. 5 agents délibératifs +
compétence `/debat` créés ; premier débat réel mené sur la question « faut-il compléter les
21 rôles ? ». Arbitrage FAIRE MAIS RÉDUIT appliqué : 3 rôles §1 créés
(`guardian-licences`, `sentinel-securite`, `superviseur-vigie`), 5 laissés en PROPOSÉ faute
de déclencheur réel. Total : 16 agents.

Garde-fou retenu de la plaidoirie du Contradicteur, à ne pas oublier : **2026-10-06,
comptage des fichiers dans `/codex/candidates/` et `/codex/expertise/`.** Si les deux
dossiers sont vides, CROQUE-MORT est invoqué sur le protocole, pas sur le produit.

---

## 2026-09-06 (3)

Changement : décision de Chaima — implémentation complète des 13 rôles du §1, contre
l'arbitrage « FAIRE MAIS RÉDUIT » du même jour. Création de `scout`, `cartographe`,
`scribe-empire`, `eclaireur-opportunites`, `architecte-integration`. **Total : 21 agents**
(13 du §1 + 8 du §13), plus la compétence `/debat`.

Garde-fou inchangé et reporté tel quel : **2026-10-06**, comptage des fichiers dans
`/codex/candidates/` et `/codex/expertise/`.

---

## 2026-09-06 (4)

Changement : premier filet de tests du dépôt. `tests/auth.test.ts` — 16 tests sur le
parcours d'authentification (login, logout, middleware), lanceur natif `node:test` exécuté
par `tsx`, **aucune dépendance ajoutée** (donc aucune fiche candidate requise, §7).
Script `npm test` ajouté et branché dans `.github/workflows/ci.yml`.

Vérifications avant push : lint 0 erreur (3 avertissements préexistants), build OK,
typecheck OK, 16/16 tests passent.

Constat majeur remonté en priorité haute dans `A-DECIDER.md` : **la session n'authentifie
personne** — cookie à valeur constante, middleware qui n'en vérifie que la présence.
Non corrigé ici : c'est une décision d'architecture (§8), pas une correction de test.

---

## 2026-09-06 (5)

Changement : `/codex/PROMPT-UNIVERSEL.md` créé — 146 lignes, autonome, project-agnostique,
à coller en tête du CLAUDE.md de chaque projet existant. Comble le manque réel du
protocole : il disait QUI sont les rôles, jamais COMMENT ils se passent l'information.
Apporte le vocabulaire commun (B), le format de passation obligatoire (C) et les 4 parcours
standards (D).
