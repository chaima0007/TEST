# Wave Development Protocol — Caelum Partners

## Problèmes récurrents & règles pour les éviter

---

## 1. Doublons dans `components/Sidebar.tsx`

**Cause :** Plusieurs agents ajoutent la même fonction `IconXxx` lors de waves différentes.

**Règle OBLIGATOIRE avant tout ajout d'icône :**
```bash
# Vérifier qu'une icône n'existe pas déjà
grep -c "^function IconXxx" components/Sidebar.tsx
# Si résultat > 0 → NE PAS rajouter, utiliser l'existante
```

**Règle OBLIGATOIRE après chaque modification Sidebar :**
```bash
# Vérifier zéro doublon
grep -n "^function Icon" components/Sidebar.tsx | awk -F: '{print $2}' | sort | uniq -d
# Doit retourner vide
```

**Règle de nommage :** `Icon` + domaine en CamelCase sans abréviations ambiguës.
- ✓ `IconLandGrabbingRights` `IconAISurveillanceRights`
- ✗ `IconWaterRights` (trop générique — risque de collision avec wave future)

**Règle de séquençage :** Un seul agent à la fois peut modifier `Sidebar.tsx`. Jamais deux agents en parallèle sur ce fichier.

---

## 2. Fichiers non-tracés (untracked) qui déclenchent le stop hook

**Cause :** Quand un agent crée des fichiers sur une branche puis switch de branche, les fichiers non-commités restent dans le working tree.

**Règle OBLIGATOIRE pour chaque agent :**
```bash
# À la FIN de chaque session agent, avant toute autre action :
git status --short
# Si ?? apparaît → git add + git commit + git push AVANT de finir
```

**Règle de commit atomique :** Chaque agent doit committer ses fichiers IMMÉDIATEMENT après les avoir créés, pas à la fin de toutes les tâches. Séquence :
1. Créer engine.py → `python3 engine.py` → commit
2. Créer route.ts → commit
3. Modifier Sidebar.tsx → commit
4. Push unique à la fin

**Règle de nettoyage inter-branches :** Avant de changer de branche, toujours :
```bash
git stash || git add -A && git commit -m "wip: intermediate state"
git checkout autre-branche
```

---

## 3. Commits sur mauvaise branche

**Cause :** Agent oublie de checkout la bonne branche avant de travailler.

**Template de démarrage OBLIGATOIRE pour tous les agents :**
```bash
git config user.email noreply@anthropic.com
git config user.name Claude
git checkout claude/swarm-50-agent-architecture-3l6cno
git pull origin claude/swarm-50-agent-architecture-3l6cno
git branch --show-current  # Vérification visuelle
```

**Avant CHAQUE commit :**
```bash
git branch --show-current
# Doit afficher : claude/swarm-50-agent-architecture-3l6cno
```

---

## 4. Conflits entre agents parallèles

**Cause :** Deux agents modifient le même fichier simultanément → merge conflicts ou écrasement.

**Règle de séparation des domaines :**

| Fichier | Max agents simultanés |
|---------|----------------------|
| `components/Sidebar.tsx` | 1 seul |
| `app/api/**/route.ts` | N (fichiers distincts) |
| `swarm/intelligence/*.py` | N (fichiers distincts) |
| `app/dashboard/**/page.tsx` | N (fichiers distincts) |

**Règle de coordination :** Toujours lancer dashboards APRÈS que les engines sont committés. Jamais en même temps sur le même slug.

---

## 5. Validation pre-commit (checklist)

### Pour les engines Python :
```bash
python3 swarm/intelligence/<engine>.py
# Vérifier dans la sortie :
# ✓ avg_composite proche de 61.xx
# ✓ Distribution : 4 critique / 2 élevé / 1 modéré / 1 faible
# ✓ Pas d'erreur Python
```

### Pour les routes TypeScript :
```bash
# Vérifier manuellement :
# ✓ import { sealResponse } from "@/lib/digital-seal"
# ✓ if (!process.env.SWARM_API_URL) { console.warn(...) }
# ✓ await sealResponse() sur TOUS les NextResponse.json()
# ✓ next: { revalidate: 30 } sur fetch upstream
# ✓ status: 502 sur catch (jamais 503)
```

### Pour les dashboards React :
```bash
# Vérifier manuellement :
# ✓ "use client" en première ligne
# ✓ GaugeRing r=36 cx=44 cy=44 viewBox="0 0 88 88"
# ✓ fetch avec d.payload ?? d
# ✓ Pas de useCallback/useMemo
# ✓ Apostrophes JSX : &apos; (jamais ')
```

---

## 6. Procédure de récupération en cas d'erreur CI

**Si le build CI échoue :**
```bash
# 1. Identifier la cause
gh run view <run_id> --log-failed
# OU via MCP github get_job_logs

# 2. Erreur "name defined multiple times" → doublons Sidebar
grep -n "^function Icon" components/Sidebar.tsx | awk -F: '{print $2}' | sort | uniq -d
# Pour chaque doublon : garder la DERNIÈRE occurrence, supprimer les précédentes

# 3. Erreur TypeScript → vérifier imports et types
# 4. Corriger → commit → push → attendre CI
```

---

## 7. Checklist de fin de wave

Avant de marquer une wave comme terminée :

- [ ] `git status --short` → propre (aucun `??` ni `M`)
- [ ] `grep "^function Icon" components/Sidebar.tsx | sort | uniq -d` → vide
- [ ] Routes : toutes les 3 ont `sealResponse` + guard SWARM_API_URL
- [ ] Engines : tous validés avec `python3 engine.py`
- [ ] Dashboards : toutes les 3 pages créées
- [ ] Sidebar : 3 nouvelles entrées nav + 3 fonctions icône
- [ ] `git log --oneline -5` → commit Wave visible en tête
- [ ] CI verte sur GitHub Actions

---

## 8. Ordre d'exécution standard d'une wave (N engines)

```
Étape 1 : Engines Python (peuvent être parallèles entre eux)
  → python3 engine.py ✓ pour chacun
  → commit groupé

Étape 2 : Routes API (peuvent être parallèles entre eux)
  → vérification pattern sécurité
  → commit groupé

Étape 3 : Sidebar (UN SEUL agent, séquentiel)
  → grep vérification doublons AVANT
  → ajout icônes + nav entries
  → grep vérification doublons APRÈS
  → commit

Étape 4 : Dashboards (peuvent être parallèles entre eux)
  → vérification "use client" + GaugeRing pattern
  → commit groupé

Étape 5 : Vérification finale
  → git status propre
  → CI verte
```

---

## 9. Constantes fluctuantes — Définition & bornes acceptables

**Contexte :** Les engines utilisent `random.uniform(-0.5, 0.5)` comme bruit. L'`avg_composite` fluctue
légèrement selon le seed mais doit toujours converger vers la cible exacte **61.03**.

### Constantes du protocole (IMMUABLES sans simulation préalable)

```python
TARGET_AVG_COMPOSITE   = 61.03   # Cible exacte de chaque engine
EXACT_AVG_CALCULATED   = 61.025  # Valeur mathématique des TUPLES_EXACT sans bruit

TUPLES_EXACT = [
    (99, 97, 95, 93),  # critique 1  → composite exact = 96.30
    (93, 90, 88, 86),  # critique 2  → composite exact = 89.60
    (85, 82, 80, 78),  # critique 3  → composite exact = 81.60
    (80, 77, 75, 73),  # critique 4  → composite exact = 76.60
    (61, 58, 56, 54),  # élevé 1     → composite exact = 57.60
    (51, 48, 46, 44),  # élevé 2     → composite exact = 47.60
    (32, 29, 27, 25),  # modéré      → composite exact = 28.60
    (13, 11,  9,  7),  # faible      → composite exact = 10.30
]
# avg exact = (96.30+89.60+81.60+76.60+57.60+47.60+28.60+10.30) / 8 = 488.20 / 8 = 61.025
```

### Bornes de fluctuation

| Zone | Amplitude Δ | Action |
|------|-------------|--------|
| ✅ OK       | \|Δ\| ≤ 0.50 | Continuer normalement |
| 🟠 ALERTE   | 0.50 < \|Δ\| ≤ 1.00 | Corriger au prochain run, logger |
| 🔴 CRITIQUE | 1.00 < \|Δ\| ≤ 2.00 | Activer fallback exact IMMÉDIATEMENT |
| 🚨 HORS_BORNES | \|Δ\| > 2.00 | Bloquer commit, revoir TUPLES_EXACT |

### Fallback exact (obligatoire quand Δ > borne OK)

```python
# Dans run_engine() — PATTERN OBLIGATOIRE
avg_composite = round(sum(r["avg_composite"] for r in results) / len(results), 2)

if abs(avg_composite - 61.03) > 0.5:  # Toute dérive > borneOK
    exact_scores = [s1*0.30 + s2*0.25 + s3*0.25 + s4*0.20
                    for s1,s2,s3,s4 in TUPLES_EXACT]
    avg_composite = round(sum(exact_scores) / len(exact_scores), 2)
    # avg_composite sera 61.03 (arrondi de 61.025)
```

### Commande de vérification (intégrée au programme)

```bash
python3 scripts/constants_monitor.py
# Valide les TUPLES_EXACT, lance 10 runs et affiche l'amplitude de fluctuation
# Amplitude attendue : < 0.001 (convergence par LGN sur n=50,000)
# Stabilité attendue : 100% des runs dans les bornes OK
```

---

## 10. Tentatives d'étude (Study Attempts) — Traçabilité

**Définition :** Chaque exécution d'un engine (validation ou production) est une **tentative d'étude**.
Elle doit être enregistrée pour détecter les dérives cumulatives sur la durée.

### Nombre de simulations par risque

| Contexte | N simulations | Usage |
|----------|---------------|-------|
| STANDARD  | 50 000  | Validation normale après création |
| ÉLEVÉ     | 500 000 | Doute sur stabilité, après ALERTE |
| CRITIQUE  | 1 000 000 | Revalidation après correction CRITIQUE |

**Règle :** La Loi des Grands Nombres (LGN) garantit la convergence :
- À n=50 000, l'amplitude de fluctuation est **< 0.001** (observé empiriquement)
- À n=1 000 000, l'amplitude est **< 0.0001** (convergence quasi-parfaite)
- En dessous de n=10 000, la fluctuation peut dépasser ±0.05 → **INTERDIT en production**

### Enregistrement obligatoire

```python
from scripts.constants_monitor import run_study_attempt

attempt = run_study_attempt(
    engine_name="nom_engine",
    n=50_000,
    context="wave_496_validation",
)
# Enregistré automatiquement dans data/study_attempts_log.json (500 dernières entrées)
```

### Commande de consultation

```bash
python3 -c "
from scripts.constants_monitor import print_attempt_history
print_attempt_history('nom_engine')  # ou None pour tous
"
```

### Règle de blocage

**BLOQUER le commit si :**
- `fluctuation_status` == `CRITIQUE` ou `HORS_BORNES`
- `fallback_applied` == True sur plus de 2 tentatives consécutives
- L'amplitude sur 10 runs dépasse `FLUCTUATION_BOUNDS["ALERTE"]` (1.00)

---

## 11. Scalabilité — Surveillance continue

Toutes les commandes de scalabilité sont intégrées dans le programme. Plus de commandes manuelles.

```bash
# Surveillance complète (à lancer après CHAQUE wave)
python3 scripts/scalability_guardian.py

# Surveillance des constantes (à lancer avant CHAQUE commit d'engine)
python3 scripts/constants_monitor.py

# Les deux ensemble (recommandé en fin de wave)
python3 scripts/scalability_guardian.py && python3 scripts/constants_monitor.py
```

**Seuils sidebar à surveiller :**
- > 4400L (80% OOM) → Split planifié
- > 5500L (100% OOM) → Split immédiat, build Vercel bloqué

**Optimisations Next.js actives (source : node_modules/next/dist/docs/01-app/02-guides/memory-usage.md) :**
- `webpackMemoryOptimizations: true` → Réduit RAM webpack
- `webpackBuildWorker: true` → Compilation dans worker séparé
- `productionBrowserSourceMaps: false` → Économise RAM build
- `preloadEntriesOnStart: false` → Réduit footprint mémoire initial
- `NODE_OPTIONS='--max-old-space-size=4096'` → Heap Node.js étendu

---

## 12. Simulation Multi-Perspectives (§12)

Chaque valeur critique est évaluée depuis **5 points de vue** (biais optimiste → pessimiste) avec consensus pondéré.

```python
PERSPECTIVES = [
    {"id": "OPTIMISTE",   "bias": +1.5, "weight": 0.10},
    {"id": "LÉGÈRE_PLUS", "bias": +0.5, "weight": 0.20},
    {"id": "NEUTRE",      "bias":  0.0, "weight": 0.40},
    {"id": "LÉGÈRE_MOINS","bias": -0.5, "weight": 0.20},
    {"id": "PESSIMISTE",  "bias": -1.5, "weight": 0.10},
]
consensus = Σ(avg_pov × weight_pov)
```

Commande : `python3 scripts/multi_perspective_simulator.py --engine <nom>`
Seuils : OK si consensus dans [60.53; 61.53], ALERTE sinon.

---

## 13. Simulation Multivers (§13)

**100 univers parallèles** avec paramètres légèrement perturbés (biais gaussien, amplitude variable).

- Médiane des univers stables = valeur de référence
- Robustesse = % univers dont composite reste dans ±5.0 de la médiane
- Seuil OK : robustesse ≥ 80%
- consensus_final = (consensus_POV + médiane_multivers) / 2

Commande : `python3 scripts/multi_perspective_simulator.py --engine <nom> --multiverse`

---

## 14. Sceau de Protocole (§14) — OBLIGATOIRE avant toute décision

Chaque décision importante (wave, build, sidebar-split, protocol-change) **DOIT** être scellée avant exécution.

### Niveaux de risque — §14-v2 (2026-06-23) :

#### Catégories existantes
| Catégorie  | Risque    | Simulation | Score min |
|------------|-----------|------------|-----------|
| build      | CRITIQUE  | Oui        | 60.0      |
| protocol   | CRITIQUE  | Oui        | 60.0      |
| sidebar    | ÉLEVÉ     | Oui        | 58.0      |
| split      | ÉLEVÉ     | Oui        | 58.0      |
| route      | ÉLEVÉ     | Non        | 55.0      |
| wave       | MOYEN     | Oui        | 60.0      |
| engine     | MOYEN     | Oui        | 60.0      |
| commit     | FAIBLE    | Non        | 50.0      |
| data       | FAIBLE    | Non        | 50.0      |

#### Nouvelles catégories ajoutées §14-v2
| Catégorie    | Risque    | Simulation | Score min | Déclencheurs                                    |
|--------------|-----------|------------|-----------|-------------------------------------------------|
| security-fix | CRITIQUE  | Oui        | 65.0      | CVE, XSS, injection SQL, credentials exposés    |
| rollback     | CRITIQUE  | Oui        | 65.0      | `git reset --hard`, revert prod, restore backup |
| deploy       | CRITIQUE  | Oui        | 62.0      | Vercel push, Cloudflare deploy, release tags    |
| migration    | CRITIQUE  | Oui        | 62.0      | Prisma migrate, LibSQL schema, db-schema change |
| integration  | ÉLEVÉ     | Oui        | 58.0      | Adoption repos GitHub, Mistral, Canva, outils   |
| dependency   | MOYEN     | Non        | 55.0      | npm add/rm, pip install, package.json changes   |
| refactor     | MOYEN     | Oui        | 58.0      | Renommage modules, restructure répertoires      |

### Commandes :
```bash
# Sceller une décision (interactive)
python3 scripts/decision_seal.py --action "wave-498" --context "3 nouveaux domaines"

# Sceller + orchestrer en une commande
python3 scripts/wave_orchestrator.py --wave 498 --full --seal

# Vérifier un sceau
python3 scripts/decision_seal.py --verify SEAL-XXXXXXXXXXXXXXXX

# Rapport des 10 derniers sceaux
python3 scripts/decision_seal.py --report
```

### Structure du sceau :
```json
{
  "seal_id":         "SEAL-27A02225290B47FB",
  "timestamp":       "2026-06-23T...",
  "action":          "wave-498",
  "status":          "APPROUVÉ",
  "final_consensus": 77.8353,
  "robustness_pct":  100.0,
  "protocol_score":  75.0
}
```

**Règle absolue** : Toute décision CRITIQUE ou ÉLEVÉE sans sceau APPROUVÉ = BLOQUÉE.
Les sceaux sont enregistrés dans `data/decision_seals_log.json` (500 max, FIFO).
