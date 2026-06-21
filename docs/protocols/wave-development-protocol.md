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
