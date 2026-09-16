# ATLAS — AUDITS

> Distinct des snapshots : un snapshot dit *ce qui a changé*, un audit dit *si c'est cohérent*.
> Le plus récent en haut. **Un audit signale, il ne corrige jamais seul** (§5).
>
> **Rythme :** cohérence à chaque session (2 min, §5) · angle mort **mensuel** (§9) ·
> auto-audit du protocole **trimestriel** (§9).

---

## AUDIT DE COHÉRENCE — 2026-09-16

| Point vérifié | Constat |
|---|---|
| `CLAUDE.md` porte-t-il la version à jour du protocole ? | **OUI** — v2026-09-06 |
| La structure `/codex/` est-elle conforme au §12 ? | **OUI** — `candidates/`, `expertise/`, `opportunites/`, `licences-sortantes/`, `A-DECIDER.md`, `EVOLUTION.md` présents. `atlas/` est un **ajout**, pas une variante : aucun dossier du §12 n'est renommé ni déplacé. |
| Un agent ATLAS redouble-t-il un rôle du §1 ? | **NON** — frontière écrite dans chaque charte. RGPD reste à `gardien-donnees`, les CVE à `sentinel-securite`, les fuites de clés à `conservateur-secrets`, la conduite de projet à `orchestrateur`/`arbitre-expert`. |
| Les lignes de `/codex/A-DECIDER.md` de plus de 14 jours sont-elles en évidence ? | **ÉCART SIGNALÉ, NON CORRIGÉ** (§5 : signaler, jamais corriger seul). Plusieurs lignes datées du 2026-06 / 2026-07 dépassent 14 jours sans être mises en évidence — notamment « Merger la PR #1 » (2026-06-18) et « Nettoyer les projets Vercel » (2026-07-17). C'est à Chaima de trancher, pas à un agent de réordonner son fichier de décisions. |
| Le principe de vérité d'ATLAS est-il écrit quelque part de lisible ? | **OUI** — `README.md` et document Drive : ce qui grossit est la mémoire et le corpus, pas les poids. |

**Angle le moins documenté à ce jour :** **Financier**. Aucun chiffre de coût électrique, aucun
coût de stockage, aucun seuil. Normal — sans machine connue, tout chiffre serait inventé. À
rescanner dès que l'ÉTAPE 0 est close. Prochain audit d'angle mort dû : **2026-10-16**.
