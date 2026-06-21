#!/usr/bin/env python3
"""
Agent [95] — Caelum Intelligence Prospective
Analyse les routes API et dashboards pour prédire les erreurs futures
avant qu'elles n'atteignent le build Netlify.
"""
import os, re, sys, json
from pathlib import Path

ROOT = Path(__file__).parent.parent
ISSUES = []
FIXES = []

def warn(file, msg, fixable=False):
    ISSUES.append({"file": str(file), "msg": msg, "fixable": fixable})

def fix(file, msg):
    FIXES.append({"file": str(file), "msg": msg})

print("\n╔══════════════════════════════════════════════════╗")
print("  Agent [95] — Caelum Prédicteur d'Erreurs")
print("╚══════════════════════════════════════════════════╝\n")

# ─── Analyse des routes API ──────────────────────────────────────
api_dir = ROOT / "app" / "api"
route_files = list(api_dir.rglob("route.ts"))
print(f"  → Analyse de {len(route_files)} routes API...")

for f in route_files:
    content = f.read_text(encoding="utf-8")
    rel = f.relative_to(ROOT)

    # Prédiction 1: entity_id au lieu de id
    if "entity_id:" in content:
        warn(rel, "ENTITY_ID: utilise entity_id au lieu de id → dashboards cassés", fixable=True)

    # Prédiction 2: virgule parasite
    for i, line in enumerate(content.splitlines(), 1):
        if line.startswith(",") and "entity_id" in line:
            warn(rel, f"VIRGULE_PARASITE: ligne {i} commence par virgule", fixable=True)

    # Prédiction 3: sealResponse manquant
    if "export async function GET" in content and "sealResponse" not in content:
        warn(rel, "SEAL_MISSING: sealResponse absent — route non authentifiée")

    # Prédiction 4: 503 au lieu de 502
    if "status: 503" in content:
        warn(rel, "HTTP_503: doit être 502 (convention Caelum)", fixable=True)

    # Prédiction 5: sealResponse(MOCK) direct sans NextResponse.json
    if re.search(r'return\s+(?:await\s+)?sealResponse\s*\(\s*MOCK', content):
        warn(rel, "SEAL_PATTERN: sealResponse(MOCK) direct — retourne plain object au lieu de Response")

    # Prédiction 6: SWARM_API_URL guard manquant
    if "SWARM_API_URL" not in content and "export async function GET" in content:
        warn(rel, "NO_GUARD: SWARM_API_URL guard manquant")

    # Prédiction 7: revalidate manquant
    if "fetch(" in content and "revalidate" not in content:
        warn(rel, "NO_REVALIDATE: revalidate:30 absent sur fetch upstream")

# ─── Analyse des dashboards ──────────────────────────────────────
dash_dir = ROOT / "app" / "dashboard"
dash_files = list(dash_dir.rglob("page.tsx"))
print(f"  → Analyse de {len(dash_files)} dashboards...")

for f in dash_files:
    content = f.read_text(encoding="utf-8")
    rel = f.relative_to(ROOT)
    lines = content.splitlines()

    # Prédiction 8: "use client" pas en première ligne
    if not lines or lines[0].strip() != '"use client"':
        warn(rel, "NO_USE_CLIENT: 'use client' manquant en ligne 1")

    # Prédiction 9: entity.entity_id au lieu de entity.id
    if "entity.entity_id" in content or "entity_id" in content:
        warn(rel, "ENTITY_ID_DASH: entity.entity_id dans le dashboard → affichage cassé", fixable=True)

    # Prédiction 10: Tailwind dans dashboard (interdit)
    tailwind_patterns = [r'className="[^"]*\b(text-|bg-|border-|flex-|grid-|p-\d|m-\d)', ]
    for pat in tailwind_patterns:
        if re.search(pat, content):
            warn(rel, "TAILWIND: className Tailwind détecté — styles inline obligatoires")
            break

    # Prédiction 11: GaugeRing r=36 manquant
    if "GaugeRing" in content and "r = 36" not in content:
        warn(rel, "GAUGE_RING: GaugeRing avec r≠36 — incohérence visuelle")

    # Prédiction 12: apostrophe JSX non échappée
    jsx_blocks = re.findall(r'>[^<]*\'[^<]*<', content)
    if jsx_blocks:
        warn(rel, "JSX_APOSTROPHE: apostrophe non échappée dans JSX — utiliser &apos;", fixable=True)

# ─── Analyse Sidebar ─────────────────────────────────────────────
sidebar = ROOT / "components" / "Sidebar.tsx"
if sidebar.exists():
    content = sidebar.read_text()
    icons = re.findall(r'^function (Icon\w+)', content, re.MULTILINE)
    duplicates = [i for i in set(icons) if icons.count(i) > 1]
    if duplicates:
        warn(sidebar.relative_to(ROOT), f"SIDEBAR_DUP: icônes dupliquées: {duplicates}")
    else:
        print(f"  → Sidebar: {len(icons)} icônes, zéro doublon ✓")

# ─── Rapport final ────────────────────────────────────────────────
print(f"\n{'═'*52}")
fixable = [i for i in ISSUES if i.get("fixable")]
critical = [i for i in ISSUES if not i.get("fixable")]

if not ISSUES:
    print("  ✓ AUCUNE ERREUR PRÉDITE — plateforme en bonne santé")
else:
    print(f"  ✗ {len(ISSUES)} problème(s) détecté(s):")
    print(f"    • {len(fixable)} auto-corrigeable(s)")
    print(f"    • {len(critical)} critique(s) à corriger manuellement")
    print()

    if fixable:
        print("  AUTO-CORRIGEABLES:")
        for i in fixable[:10]:
            print(f"    [{i['msg'].split(':')[0]}] {i['file']}")

    if critical:
        print("\n  CRITIQUES:")
        for i in critical[:10]:
            print(f"    [{i['msg'].split(':')[0]}] {i['file']}")

    if len(ISSUES) > 20:
        print(f"\n  ... et {len(ISSUES)-20} autres.")

print(f"{'═'*52}\n")

# Sortir avec code d'erreur si problèmes critiques
if critical:
    sys.exit(1)
