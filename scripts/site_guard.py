#!/usr/bin/env python3
"""
site_guard.py — Gardien de Cohérence du Site CaelumSwarm™ / Caelum
═══════════════════════════════════════════════════════════════════
Assistant qui surveille le site et PRÉVIENT dès qu'il y a un problème :
- Anciennes marques oubliées (CompeteIQ, ancien produit)
- Incohérence du nom de marque (CaelumSwarm vs Caelum côté visiteur)
- Contenu obsolète (veille concurrentielle, faux clients, fausses stats)
- Anglicismes courants dans le texte FR visible

Code retour non-zéro si un problème est trouvé → à lancer avant chaque
publication (et intégrable au preflight).

Usage :
  python3 scripts/site_guard.py --scan
  python3 scripts/site_guard.py --scan --quiet
"""

import re
import sys
import argparse
from pathlib import Path

# Dossiers de pages visibles par les visiteurs (hors dashboard interne/api)
PUBLIC_GLOBS = ["app/page.tsx", "app/layout.tsx", "app/*/page.tsx"]

# Marque officielle attendue côté visiteur
BRAND = "Caelum"

# Motifs interdits (ancienne identité / contenu obsolète / faux)
FORBIDDEN = [
    {"id": "OLD_BRAND",     "rx": r"CompeteIQ|competeiq",            "sev": "CRITIQUE",
     "msg": "Ancienne marque 'CompeteIQ' — remplacer par Caelum"},
    {"id": "OLD_POSITION",  "rx": r"veille strat[ée]gique|avantage concurrentiel|intelligence concurrentielle",
     "sev": "CRITIQUE", "msg": "Ancien positionnement (veille concurrentielle)"},
    {"id": "FAKE_CLIENTS",  "rx": r"BNP Paribas|TotalEnergies|Legrand|Schneider|Capgemini|Sopra Steria",
     "sev": "CRITIQUE", "msg": "Faux client mentionné — interdit (mensonge commercial)"},
    {"id": "FAKE_STATS",    "rx": r"350\+|4,8x|ROI 124|12 M€",       "sev": "ÉLEVÉ",
     "msg": "Statistique non vérifiée / fabriquée"},
    {"id": "BRAND_VARIANT", "rx": r"CaelumSwarm",                    "sev": "ÉLEVÉ",
     "msg": "Variante 'CaelumSwarm' côté visiteur — utiliser 'Caelum'"},
    {"id": "ANGLICISM",     "rx": r"\bWhite-Label\b|/mo\b|\(Free\)", "sev": "MOYEN",
     "msg": "Anglicisme dans le texte FR (White-Label/mo/Free)"},
]

SEV_ICON = {"CRITIQUE": "🔴", "ÉLEVÉ": "🟠", "MOYEN": "🟡"}


def _public_files():
    seen = set()
    for g in PUBLIC_GLOBS:
        for p in Path(".").glob(g):
            if "dashboard" in str(p) or "/api/" in str(p):
                continue
            seen.add(p)
    return sorted(seen)


def _visible_text_lines(txt: str):
    """Approxime le texte visible : lignes contenant du texte entre > < ou guillemets JSX."""
    for i, line in enumerate(txt.split("\n"), 1):
        yield i, line


def scan() -> list:
    findings = []
    for p in _public_files():
        txt = p.read_text()
        for i, line in _visible_text_lines(txt):
            for rule in FORBIDDEN:
                if re.search(rule["rx"], line, re.IGNORECASE if rule["id"] != "BRAND_VARIANT" else 0):
                    findings.append({"file": str(p), "line": i, "id": rule["id"],
                                     "sev": rule["sev"], "msg": rule["msg"],
                                     "extract": line.strip()[:80]})
    return findings


def main():
    ap = argparse.ArgumentParser(description="Site Guard — cohérence du site Caelum")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not args.scan:
        ap.print_help()
        return

    findings = scan()
    if not args.quiet:
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║       SITE GUARD — Cohérence du site Caelum                 ║")
        print("╚══════════════════════════════════════════════════════════════╝\n")

    if not findings:
        print("  ✅ Site cohérent — aucune ancienne marque ni incohérence détectée.\n")
        sys.exit(0)

    by_sev = {}
    for f in findings:
        by_sev.setdefault(f["sev"], []).append(f)

    for sev in ("CRITIQUE", "ÉLEVÉ", "MOYEN"):
        items = by_sev.get(sev, [])
        if not items:
            continue
        print(f"  {SEV_ICON[sev]} {sev} ({len(items)})")
        for f in items[:20]:
            print(f"     {f['file']}:{f['line']} — {f['msg']}")
            print(f"        « {f['extract']} »")
        print()

    critical = sum(1 for f in findings if f["sev"] == "CRITIQUE")
    print("─" * 60)
    print(f"  Total : {len(findings)} problème(s) | 🔴 {critical} critique(s)")
    print("─" * 60 + "\n")
    sys.exit(1 if critical > 0 else 0)


if __name__ == "__main__":
    main()
