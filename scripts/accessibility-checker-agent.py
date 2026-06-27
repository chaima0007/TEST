#!/usr/bin/env python3
"""Accessibility Checker Agent — CaelumSwarm™ Dev Support
Vérifie l'accessibilité WCAG 2.1 AA des dashboards React :
contraste des couleurs, attributs aria, textes alternatifs,
navigation clavier, sémantique HTML.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "AccessibilityCheckerAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Couleurs de l'app et leurs ratios de contraste approximatifs sur fond sombre
COLOR_CONTRAST_DB = {
    "#ef4444": ("rouge", 3.8, "AA-large"),   # critique
    "#f97316": ("orange", 3.1, "FAIL-AA"),   # élevé — attention
    "#eab308": ("jaune", 5.2, "AA"),          # modéré
    "#22c55e": ("vert", 4.8, "AA"),           # faible
    "#94a3b8": ("gris clair", 4.5, "AA"),
    "#64748b": ("gris foncé", 2.8, "FAIL"),  # potentiellement problématique
    "#ffffff": ("blanc", 21.0, "AAA"),
    "#cbd5e1": ("gris perle", 6.1, "AAA"),
}

# Patterns WCAG à vérifier
WCAG_CHECKS = [
    (r'<button[^>]*>(?!</button>)[^<]*</button>', False, "WCAG 4.1.3", "Bouton sans texte alternatif"),
    (r'<img[^>]*>(?![^>]*alt=)', True, "WCAG 1.1.1", "Image sans attribut alt"),
    (r'onClick={[^}]+}(?![^>]*(?:aria-label|role|onKeyDown))', False, "WCAG 2.1.1", "onClick sans onKeyDown (navigation clavier)"),
    (r'style=\{[^}]*color:\s*["\']#64748b["\']', True, "WCAG 1.4.3", "Couleur #64748b contraste insuffisant (ratio 2.8:1)"),
    (r'style=\{[^}]*color:\s*["\']#f97316["\']', True, "WCAG 1.4.3", "Couleur #f97316 contraste insuffisant sur fond clair"),
    (r'<div[^>]*onClick=', True, "WCAG 4.1.2", "div cliquable sans role='button'"),
    (r'autoFocus', True, "WCAG 2.4.3", "autoFocus peut perturber l'ordre de focus"),
    (r'tabIndex={-1}', True, "WCAG 2.1.1", "tabIndex=-1 retire l'élément de la navigation clavier"),
    (r'aria-hidden="true"[^>]*>.*?</(?:button|a|input)', True, "WCAG 1.3.1", "Élément interactif aria-hidden"),
]

# Éléments sémantiques requis
SEMANTIC_CHECKS = [
    (r'<h[1-6]', True, "Structure de titres présente"),
    (r'<main|role="main"', True, "Landmark main présent"),
    (r'<nav|role="navigation"', True, "Navigation landmark présent"),
    (r'lang=', True, "Attribut lang sur html"),
]


def check_color_contrast(source: str) -> list[dict]:
    issues = []
    for hex_color, (name, ratio, level) in COLOR_CONTRAST_DB.items():
        if hex_color in source and level.startswith("FAIL"):
            count = source.count(hex_color)
            issues.append({
                "severity": "WARNING",
                "wcag": "WCAG 1.4.3",
                "color": hex_color,
                "ratio": f"{ratio}:1",
                "level": level,
                "message": f"Couleur {name} ({hex_color}) ratio {ratio}:1 — {level} (requis 4.5:1 AA)",
                "occurrences": count,
            })
    return issues


def check_file(filepath: Path) -> dict:
    source = filepath.read_text(encoding="utf-8", errors="ignore")
    issues = []
    warnings = []
    info = []

    # WCAG checks
    for pattern, is_issue, wcag_ref, message in WCAG_CHECKS:
        matches = re.findall(pattern, source, re.DOTALL)
        if matches and is_issue:
            issues.append({"severity": "WARNING", "wcag": wcag_ref, "message": message, "count": len(matches)})

    # Contraste couleurs
    color_issues = check_color_contrast(source)
    issues.extend(color_issues)

    # Alt text sur GaugeRing SVG
    if "GaugeRing" in source or "<svg" in source:
        if "aria-label" not in source and "role=" not in source:
            issues.append({
                "severity": "WARNING",
                "wcag": "WCAG 1.1.1",
                "message": "SVG GaugeRing sans aria-label — ajouter aria-label='Score: X/10'",
            })

    # Texte trop petit
    small_fonts = re.findall(r'fontSize:\s*["\']?(\d+)["\']?', source)
    for size in small_fonts:
        if int(size) < 12:
            issues.append({
                "severity": "WARNING",
                "wcag": "WCAG 1.4.4",
                "message": f"fontSize {size}px trop petit (min 12px recommandé pour lisibilité)",
            })

    score = max(0, 100 - len(issues) * 8)

    return {
        "file": filepath.parent.name + "/" + filepath.name,
        "issues": issues,
        "score": score,
        "wcag_level": "AA" if score >= 85 else "Partial-AA" if score >= 60 else "FAIL",
    }


def run_checker(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*65}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Accessibility Checker WCAG 2.1 v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*65}{RESET}\n")

    dash_files = list((root / "app" / "dashboard").rglob("page.tsx"))

    results = []
    total_issues = 0

    for filepath in dash_files[:20]:  # Limite à 20 dashboards
        result = check_file(filepath)
        results.append(result)
        total_issues += len(result["issues"])

        color = GREEN if result["score"] >= 85 else YELLOW if result["score"] >= 60 else RED
        print(f"  {color}{result['score']:3d}/100{RESET}  [{result['wcag_level']:<12}]  {result['file']}")
        for issue in result["issues"][:2]:
            print(f"    {YELLOW}⚠ {issue['wcag']}{RESET}: {issue['message'][:70]}")

    avg_score = sum(r["score"] for r in results) / len(results) if results else 0

    print(f"\n{BOLD}Score accessibilité moyen : {avg_score:.1f}/100{RESET}")
    print(f"  {total_issues} problèmes détectés sur {len(results)} dashboards")

    print(f"\n{BOLD}Recommandations globales :{RESET}")
    print(f"  1. Ajouter aria-label='Score: {{value}}/10' sur tous les SVG GaugeRing")
    print(f"  2. Remplacer la couleur #64748b par #94a3b8 pour améliorer le contraste")
    print(f"  3. Ajouter onKeyDown={{handleKeyPress}} sur tous les éléments onClick")
    print(f"  4. Vérifier les tailles de police < 12px dans les dashboards")
    print()

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "dashboards_checked": len(results),
        "total_issues": total_issues,
        "avg_score": round(avg_score, 2),
        "results": results,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_checker(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
