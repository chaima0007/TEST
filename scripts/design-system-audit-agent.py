#!/usr/bin/env python3
"""Design System Audit Agent — CaelumSwarm™ Dev Support
Audite le système de design : cohérence des couleurs, typographie,
espacements, palette d'accents, contraste, palette CSDDD par domaine.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

AGENT_NAME = "DesignSystemAuditAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Palette de base CaelumSwarm (fond sombre)
BASE_COLORS = {
    "#020617": "background principal (slate-950)",
    "#0f172a": "card background (slate-900)",
    "#1e293b": "border/subtle (slate-800)",
    "#475569": "hover border (slate-600)",
    "#64748b": "text muted (slate-500)",
    "#94a3b8": "text secondary (slate-400)",
    "#cbd5e1": "text primary (slate-300)",
    "#ffffff": "text white",
}

# Couleurs de risque
RISK_COLORS = {
    "critique": "#ef4444",
    "élevé": "#f97316",
    "modéré": "#eab308",
    "faible": "#22c55e",
}

# Accents déjà utilisés par wave
USED_ACCENTS = [
    "#ea580c", "#6d28d9", "#0f766e", "#b45309", "#4c1d95",
    "#0369a1", "#0ea5e9", "#92400e", "#7c3aed", "#be185d",
    "#d97706", "#065f46", "#0891b2", "#dc2626", "#4338ca",
    "#c026d3", "#0d9488", "#7c2d12", "#78350f", "#1d4ed8",
    "#134e4a", "#0c4a6e", "#365314", "#581c87", "#f59e0b",
    "#6b3a2a", "#1e3a5f", "#7f1d1d", "#4a044e", "#164e63",
    "#14532d", "#713f12", "#4c0519", "#166534", "#450a0a",
    "#3d1a00", "#1a2e05", "#312e81", "#1c3d1c", "#0c1445",
    "#1a0533", "#2d1b69", "#083344", "#3b0764", "#042f2e",
]


def extract_colors_from_dashboards(root: Path) -> dict:
    """Extrait toutes les couleurs utilisées dans les dashboards."""
    color_usage = Counter()
    files = list((root / "app" / "dashboard").rglob("page.tsx"))

    for f in files:
        source = f.read_text(encoding="utf-8", errors="ignore")
        hex_colors = re.findall(r'"(#[0-9a-fA-F]{6})"', source)
        for color in hex_colors:
            color_usage[color.lower()] += 1

    return dict(color_usage.most_common(30))


def check_color_consistency(root: Path) -> list[dict]:
    issues = []
    files = list((root / "app" / "dashboard").rglob("page.tsx"))

    for f in files:
        source = f.read_text(encoding="utf-8", errors="ignore")

        # Vérifier ACCENT constant défini
        accent_match = re.search(r'const ACCENT\s*=\s*"(#[0-9a-fA-F]{6})"', source)
        if not accent_match:
            issues.append({
                "file": f.parent.name,
                "type": "NO_ACCENT_CONST",
                "severity": "WARNING",
                "message": "Constante ACCENT non définie"
            })

        # Vérifier RC (risk colors) standard
        if "RC:" not in source and "const RC" not in source:
            issues.append({
                "file": f.parent.name,
                "type": "NO_RISK_COLORS",
                "severity": "INFO",
                "message": "Constante RC (risk colors) absente — vérifier la cohérence visuelle"
            })

        # Vérifier pas de couleurs hardcodées hors des constantes
        inline_colors = re.findall(r'style=\{[^}]*color:\s*["\'](?!white|inherit|transparent)(#[0-9a-fA-F]{6})["\']', source)
        if len(set(inline_colors)) > 5:
            issues.append({
                "file": f.parent.name,
                "type": "TOO_MANY_INLINE_COLORS",
                "severity": "WARNING",
                "message": f"{len(set(inline_colors))} couleurs inline distinctes — risque d'incohérence"
            })

    return issues


def generate_color_palette_doc(root: Path) -> str:
    """Génère la documentation de la palette de couleurs."""
    lines = [
        "# CaelumSwarm™ Design System — Palette de Couleurs",
        f"*{datetime.now(timezone.utc).strftime('%Y-%m-%d')}*",
        "",
        "## Couleurs de base (fond sombre)",
        "",
        "| Variable | Hex | Usage |",
        "|----------|-----|-------|",
    ]
    for hex_val, usage in BASE_COLORS.items():
        lines.append(f"| -- | `{hex_val}` | {usage} |")

    lines += [
        "",
        "## Couleurs de risque CSDDD",
        "",
        "| Niveau | Hex | Tailwind approx |",
        "|--------|-----|-----------------|",
    ]
    tailwind_map = {"critique": "red-500", "élevé": "orange-500", "modéré": "yellow-500", "faible": "green-500"}
    for level, hex_val in RISK_COLORS.items():
        lines.append(f"| **{level}** | `{hex_val}` | `{tailwind_map.get(level, '?')}` |")

    lines += [
        "",
        "## Accents par Wave (uniques)",
        "",
        "| Wave | Hex | Domaine |",
        "|------|-----|---------|",
    ]

    engine_files = sorted((root / "swarm" / "intelligence").glob("*_engine.py"))
    for engine in engine_files[:20]:
        source = engine.read_text(encoding="utf-8", errors="ignore")
        accent = re.search(r'ACCENT_COLOR\s*=\s*["\']([#\w]+)["\']', source)
        wave = re.search(r'Wave\s+(\d+)', source)
        if accent and wave:
            lines.append(f"| {wave.group(1)} | `{accent.group(1)}` | {engine.stem[:35]} |")

    return "\n".join(lines)


def suggest_next_accents(count: int = 10) -> list[str]:
    """Suggère des accents non encore utilisés."""
    candidates = [
        "#1e3a2f", "#2a1f3d", "#0a2540", "#1a0a2e", "#0d1f2d",
        "#2d0a0a", "#0a2d1a", "#1f0a2d", "#2d1a0a", "#0a1a2d",
        "#1f2d0a", "#2d0a1f", "#0a2d2d", "#1a2d0a", "#2d0a2d",
    ]
    available = [c for c in candidates if c not in USED_ACCENTS]
    return available[:count]


def run_audit(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*65}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Design System Audit Agent v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*65}{RESET}\n")

    colors = extract_colors_from_dashboards(root)
    issues = check_color_consistency(root)

    print(f"{BOLD}Top 10 couleurs utilisées :{RESET}")
    for color, count in list(colors.items())[:10]:
        usage = BASE_COLORS.get(color, RISK_COLORS.get(color, "accent"))
        print(f"  {color}  ×{count:4d}  {usage}")

    print(f"\n{BOLD}Problèmes de cohérence ({len(issues)}) :{RESET}")
    by_severity = {"WARNING": [], "INFO": [], "ERROR": []}
    for issue in issues:
        by_severity.get(issue["severity"], by_severity["ERROR"]).append(issue)

    for sev, sev_issues in by_severity.items():
        if sev_issues:
            color = YELLOW if sev == "WARNING" else "\033[34m" if sev == "INFO" else RED
            print(f"  {color}[{sev}]{RESET} {len(sev_issues)} fichiers")
            for i in sev_issues[:3]:
                print(f"    • {i['file']}: {i['message']}")

    # Accents disponibles
    next_accents = suggest_next_accents(8)
    print(f"\n{BOLD}Accents disponibles pour les prochaines waves :{RESET}")
    print(f"  {', '.join(next_accents)}")

    # Générer doc
    docs_dir = root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    palette_doc = docs_dir / "design-palette.md"
    palette_doc.write_text(generate_color_palette_doc(root), encoding="utf-8")
    print(f"\n{GREEN}✓ docs/design-palette.md généré{RESET}\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "top_colors": colors,
        "consistency_issues": len(issues),
        "available_accents": next_accents,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_audit(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
