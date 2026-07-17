# Protocole — Système de plateforme autonome (§16)

Point d'entrée unique, local, sans dépendance externe :
`python3 scripts/autonomous_platform.py`

## Ce qu'il fait (4 étapes)

1. **Corpus (vérité terrain)** — recompte modules / réponses / sources des deux projets
   depuis le dépôt. Aucune valeur inventée.
2. **Santé** — lance les protocoles RÉELS existants et capture leur état :
   `loi_reference_audit`, `source_trust_protocol`, `branch_guard --check`.
3. **Scénarios** — imagine *tous* les scénarios et les simule (Monte Carlo + modèles
   déterministes), chacun étiqueté `etat` (situation actuelle) ou `stress` (cas extrême) :
   - **Trafic** — normal → viral (modèle de latence type file d'attente ; mitigation `revalidate:30` + SSG)
   - **Sources** — rotation / refonte de portail / panne large (mitigation : détecteur de changement + 2ᵉ source)
   - **Build** — croissance des pages vs limites OOM Vercel (mitigation : heap 4 Go + `webpackMemoryOptimizations`)
   - **Déploiement** — env manquante, upstream en panne, webhook absent (mitigation : guard + fallback 502)
   - **Données** — identité placeholder, couverture sources officielles
   - **Sécurité** — payload/email abusifs (mitigation : limites + 413)
   - **Langues** — visiteur non francophone (FR/NL natifs + `/en` + traduction à la volée)
4. **Sceau de protocole** — verdict :
   - **BLOQUÉ** uniquement si l'**état actuel** (santé + scénarios `etat`) contient un `CRITIQUE`.
   - Les scénarios **`stress`** alimentent le **score de résilience** et la liste des **fragilités**
     (ils ne bloquent pas : ce sont des stress-tests).

## Sorties

- Console : tableau lisible (verdicts + métriques).
- `data/autonomous_platform_report.json` : rapport complet horodaté et traçable.
- Code retour `1` si BLOQUÉ (utilisable en pre-commit / CI), `0` sinon.

## Règles d'honnêteté

- Les « simulations » sont des **modèles** locaux clairement étiquetés — pas des appels réseau réels.
- Les volumes proviennent du dépôt (recomptés), jamais d'estimations inventées.
- Les `ALERTE` d'état actuel renvoient aux décisions humaines en attente (webhook, identité légale).

## Options

```bash
python3 scripts/autonomous_platform.py              # run complet
python3 scripts/autonomous_platform.py --fast       # scénarios seuls (sans subprocess)
python3 scripts/autonomous_platform.py --n 500000   # taille Monte Carlo (défaut 100 000)
```
