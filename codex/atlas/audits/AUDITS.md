# ATLAS — AUDITS

> Distinct des snapshots : un snapshot dit *ce qui a changé*, un audit dit *si c'est cohérent*.
> Le plus récent en haut. **Un audit signale, il ne corrige jamais seul** (§5).
>
> **Rythme :** cohérence à chaque session (2 min, §5) · angle mort **mensuel** (§9) ·
> auto-audit du protocole **trimestriel** (§9).

---

## AUDIT DE REPRISE À FROID — 2026-09-19 14:05 UTC

**Méthode :** une session neuve, sans contexte, avec pour seule consigne `PROMPT-MAITRE-v2.md`, en
lecture seule. 19 appels d'outils. **Verdict : PLAUSIBLE** — la reprise a réussi, mais par
inférence sur des ambiguïtés. Un test qui passe « en devinant juste » n'est pas un test qui passe.

| Trou trouvé | Périmètre | Sort |
|---|---|---|
| `ETAT.md` racine (Nexus-Market) et `codex/atlas/00-ETAT-DU-PROJET.md` coexistent ; le prompt disait « l'un ou l'autre » | ATLAS | **corrigé** — chemin exact, avertissement explicite |
| `--since=<dernier snapshot>` inopérant : snapshots sans heure, 5 le même jour | ATLAS | **corrigé** — snapshots horodatés UTC, SNAPSHOTS lu avant le `--since` |
| Chemins §2 sans préfixe `codex/atlas/` | ATLAS | **corrigé** |
| Prompt suppose Exa et Drive ; la routine n'a ni l'un ni l'autre | ATLAS | **corrigé** — §0.6 |
| Ligne JobYourself encore « ouverte » au-dessus de sa ligne « CLOS » | ATLAS (ma ligne) | **corrigé** |
| `00-ETAT` listait la routine comme « proposée » ; titre « 3 choses » pour 4 | ATLAS | **corrigé** |
| `codex/atlas/README.md` : « CONCEPTION, rien installé » — périmé depuis le 16/09 | ATLAS | **corrigé** |
| Routine : son prompt ne cite pas `PROMPT-MAITRE-v2` | ATLAS | **corrigé** — trigger mis à jour |
| Cron `0 4 UTC` = 06h Bruxelles **jusqu'au 25/10**, puis 05h | ATLAS | **documenté** |
| `CLAUDE.md` §15.4 : « branche de dev » = branche close depuis le 11/09 | **partagé** | **signalé, non corrigé** (§5) |
| A-DECIDER : « Merger la PR #1 » ouverte depuis le 18/06 alors que mergée ; non trié ; 4 lignes > 14 j sans mise en évidence | **partagé** | **signalé, non corrigé** (§5) — déjà signalé le 16/09, toujours là |

**Ce qu'une session neuve risquait de faire de travers avant ces correctifs :** travailler sur
Nexus-Market en croyant travailler sur ATLAS ; rouvrir JobYourself ; « corriger » A-DECIDER seule ;
croire Exa disponible ; produire un `git log` vide ou complet selon la lecture du `--since`.

**Condition pour passer à CONFIRMÉ :** la passe de la routine du 20/09 06h produit un snapshot
juste, sans toucher `ETAT.md` racine ni rouvrir JobYourself.

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
