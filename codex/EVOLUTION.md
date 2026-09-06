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
