<!-- BEGIN:wave-safety-rules -->
# WAVE SAFETY — Run these checks every time, no exceptions

## 0. Startup (copy-paste this block at the start of EVERY wave task)
```bash
git config user.email noreply@anthropic.com && git config user.name Claude
git checkout claude/swarm-50-agent-architecture-3l6cno
git pull origin claude/swarm-50-agent-architecture-3l6cno
git branch --show-current   # MUST print: claude/swarm-50-agent-architecture-3l6cno
```

## 1. Before touching Sidebar.tsx — check for existing icon
```bash
grep -c "^function IconYourNewName" components/Sidebar.tsx
# 0 → safe to add   |   1+ → REUSE existing, do NOT add again
```

## 2. After editing Sidebar.tsx — verify zero duplicates
```bash
grep "^function Icon" components/Sidebar.tsx | awk -F'[{ ]' '{print $3}' | sort | uniq -d
# Must return EMPTY. If not → remove the earlier duplicate before committing.
```

## 3. Before every commit — working tree must be clean
```bash
git status --short
# ?? lines → git add + commit those files first
# M lines  → stage and include in commit
```

## 4. Sidebar.tsx rule — ONE agent at a time
Never edit Sidebar.tsx in parallel with another running agent.
Always `git pull` immediately before editing Sidebar.tsx.

## 5. Commit immediately after each file group is done
Do NOT batch everything at the end. Commit engines → commit routes → commit sidebar → commit dashboards.

## 6. Scalability Guardian — run after EVERY wave (intégré au programme)
```bash
python3 scripts/scalability_guardian.py
# CRITIQUE → bloquer le commit, corriger immédiatement
# ALERTE   → planifier split avant la wave suivante
# OK       → continuer
```
Rapport sauvegardé automatiquement dans data/scalability_report.json

## 7. Sidebar icons — split automatique si ALERTE
Si un fichier sidebar-icons-N.tsx dépasse 4400L (80% OOM Vercel) :
```bash
# Le guardian détecte et recommande le split
# Créer sidebar-icons-Nb.tsx + mettre à jour sidebar-icons.tsx barrel
# Vérifier 0 doublon entre TOUS les fichiers après split
grep -h "^export function Icon" components/sidebar-icons-*.tsx | sort | uniq -d
# Doit retourner VIDE
```
Source officielle : node_modules/next/dist/docs/01-app/02-guides/memory-usage.md

## 8. Build memory — NODE_OPTIONS obligatoire
package.json doit avoir : `NODE_OPTIONS='--max-old-space-size=4096' next build`
next.config.ts doit avoir : webpackMemoryOptimizations + webpackBuildWorker + productionBrowserSourceMaps:false
Source officielle : node_modules/next/dist/docs/01-app/02-guides/memory-usage.md

## 9. Constantes fluctuantes — Vérification obligatoire avant commit d'engine
```bash
python3 scripts/constants_monitor.py
# ✓ STABLE + 100% OK → commit autorisé
# ALERTE            → logger, continuer avec fallback exact
# CRITIQUE/HORS_BORNES → BLOQUER commit, revoir TUPLES_EXACT
```
Bornes : OK=±0.50 | ALERTE=±1.00 | CRITIQUE=±2.00 | HORS_BORNES=>±2.00
Fallback exact OBLIGATOIRE si |Δ| > 0.50 (pattern dans run_engine())

## 10. Tentatives d'étude — N simulations minimum
- STANDARD (validation) : n=50_000  → amplitude < 0.001 garanti par LGN
- ÉLEVÉ (doute)         : n=500_000 → amplitude < 0.0001
- CRITIQUE (correction) : n=1_000_000
- INTERDIT en production : n < 10_000 (fluctuation trop haute)
Toutes les tentatives enregistrées dans data/study_attempts_log.json (500 entrées max)
<!-- END:wave-safety-rules -->

<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->
