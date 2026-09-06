# EVOLUTION — jalons réels de l'Empire

APPEND-ONLY (§6.5). Une section par projet. **Uniquement les événements significatifs** :
jalon, décision prise, lancement, problème résolu. Jamais "rien de neuf" ici — ça, c'est
le JOURNAL.

---

## CompeteIQ

### 2026-09-06 — Protocole CODEX v2 installé
Le dépôt passe sous protocole. `CLAUDE.md` porte la version du 2026-09-06, structure
`/codex/` conforme au §12, 8 rôles complémentaires ajoutés (§13) et implémentés comme
sous-agents dans `.claude/agents/`. Trois questions ouvertes déposées dans A-DECIDER.md.
Aucune décision engageante prise par un agent.

### 2026-09-06 — Le pipeline de décision §8 devient exécutable
Cœur délibératif implémenté en sous-agents (`avocat`, `contradicteur`,
`simulateur-scenarios`, `arbitre-expert`, `verificateur-verite`) et orchestré par la
compétence `/debat`, qui impose l'indépendance des deux plaidoiries et oblige l'arbitrage à
retenir ce que chaque camp a gagné. Premier débat réel mené sur le protocole lui-même
(fiche DEB-2026-09-06-01) : verdict FAIRE MAIS RÉDUIT — 16 agents au lieu de 21, avec une
condition de révision datée au 2026-10-06. Chaîne d'entrée (`guardian-licences`,
`sentinel-securite`) et vigie (`superviseur-vigie`) implémentées à ce titre.

### 2026-09-06 — Les 21 agents sont en place
Chaima tranche la fiche DEB-2026-09-06-01 en faveur de l'implémentation complète, contre la
réduction recommandée par l'Arbitre (§10 : la décision humaine prime). Les 13 rôles du §1
et les 8 du §13 existent désormais comme sous-agents invocables. Le garde-fou du
2026-10-06 est maintenu : comptage de `/codex/candidates/` et `/codex/expertise/`, et
invocation de CROQUE-MORT sur le protocole s'ils sont vides.

### 2026-09-06 — Premier filet de tests, et une faille d'authentification mise au jour
16 tests de non-régression sur login / logout / middleware (`tests/auth.test.ts`), sans
aucune dépendance ajoutée, branchés dans la CI. En les écrivant : le cookie de session a une
valeur constante et le middleware n'en vérifie que la présence — tout accès « protégé » est
en réalité public. Remonté en priorité haute dans A-DECIDER.md, non corrigé sur place
(décision d'architecture, §8).

### 2026-09-06 — Prompt universel de l'Empire
`/codex/PROMPT-UNIVERSEL.md` : bloc unique et portable à coller dans chaque projet. Il ajoute
ce qui manquait au protocole pour que les agents circulent entre projets — un vocabulaire
commun sans variante, un **format de passation** unique que tout agent doit émettre, et les
4 parcours standards (entrée d'un composant, décision, publication, push de code).
