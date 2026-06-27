#!/usr/bin/env python3
"""SVG Icon Generator Agent — CaelumSwarm™ Dev Support
Génère automatiquement des icônes SVG pour les nouveaux domaines CSDDD.
Basé sur Heroicons v2 (outline, 24x24, strokeWidth=1.5).
"""
import json
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "SVGIconGeneratorAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Bibliothèque d'icônes par catégorie de domaine
ICON_LIBRARY = {
    # Environnement
    "environment": '<path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />',
    # Justice/droits
    "rights": '<path strokeLinecap="round" strokeLinejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z" />',
    # Technologie/IA
    "technology": '<path strokeLinecap="round" strokeLinejoin="round" d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0V12a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 12V5.25" />',
    # Finance/argent
    "finance": '<path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />',
    # Santé
    "health": '<path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />',
    # Conflit/guerre
    "conflict": '<path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />',
    # Travail
    "labor": '<path strokeLinecap="round" strokeLinejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0112 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 01-.673-.38m0 0A2.18 2.18 0 013 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m7.5 0V5.25A2.25 2.25 0 0013.5 3h-3a2.25 2.25 0 00-2.25 2.25v.894m7.5 0a48.667 48.667 0 00-7.5 0M12 12.75h.008v.008H12v-.008z" />',
    # Ressources naturelles
    "resources": '<path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />',
    # Default
    "default": '<path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />',
}

DOMAIN_CATEGORY_MAP = {
    "environment": ["toxic", "deforestation", "water_pollution", "crypto_energy", "climate", "ocean", "fishing"],
    "rights": ["rights", "freedom", "justice", "colonial", "reparation", "asylum", "refugee"],
    "technology": ["ai", "algorithmic", "biometric", "surveillance", "digital", "genetic", "dark_pattern"],
    "finance": ["tax", "financial", "debt", "patent", "pharmaceutical", "corporate"],
    "health": ["health", "mental", "disability", "elderly"],
    "conflict": ["conflict", "war", "arms", "military", "child_soldier"],
    "labor": ["labor", "worker", "gig", "prison", "slavery", "trafficking", "migrant"],
    "resources": ["mining", "mineral", "land", "seed", "food", "water_privatisation"],
}


def get_icon_for_domain(domain_name: str) -> str:
    """Détermine la meilleure icône pour un domaine."""
    domain_lower = domain_name.lower()
    for category, keywords in DOMAIN_CATEGORY_MAP.items():
        if any(kw in domain_lower for kw in keywords):
            return ICON_LIBRARY[category]
    return ICON_LIBRARY["default"]


def generate_sidebar_icon(icon_name: str, domain_name: str) -> str:
    """Génère le code TypeScript d'une icône Sidebar."""
    path_content = get_icon_for_domain(domain_name)
    return f"""function {icon_name}({{ className }}: {{ className?: string }}) {{
  return (
    <svg className={{className}} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={{1.5}}>
      {path_content}
    </svg>
  );
}}"""


def suggest_icons_for_missing_engines(root: Path) -> list[dict]:
    """Suggère des icônes pour les engines sans entrée Sidebar."""
    sidebar = root / "components" / "Sidebar.tsx"
    if not sidebar.exists():
        return []

    sidebar_source = sidebar.read_text(encoding="utf-8", errors="ignore")
    engine_files = list((root / "swarm" / "intelligence").glob("*_engine.py"))

    suggestions = []
    for engine in engine_files:
        slug = engine.stem.replace("_", "-")
        href = f"/dashboard/{slug}"
        if href not in sidebar_source:
            # Générer nom d'icône
            icon_name = "Icon" + "".join(w.capitalize() for w in engine.stem.replace("_engine", "").split("_"))
            icon_code = generate_sidebar_icon(icon_name, engine.stem)
            suggestions.append({
                "engine": engine.stem,
                "slug": slug,
                "icon_name": icon_name,
                "icon_code": icon_code,
                "href": href,
            })

    return suggestions


def run_generator(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}CaelumSwarm™ SVG Icon Generator v{VERSION}{RESET}\n")

    suggestions = suggest_icons_for_missing_engines(root)

    if suggestions:
        print(f"Icônes à générer pour {len(suggestions)} engines sans Sidebar :\n")
        for s in suggestions[:5]:
            print(f"  {GREEN}→{RESET} {s['icon_name']} pour {s['engine']}")

        # Générer un fichier d'icônes manquantes
        output = root / "docs" / "missing-sidebar-icons.tsx"
        output.parent.mkdir(parents=True, exist_ok=True)
        content = "// Icônes manquantes — générées par SVGIconGeneratorAgent\n"
        content += '// Copier dans components/Sidebar.tsx juste avant // ─── Nav structure\n\n'
        for s in suggestions[:10]:
            content += s["icon_code"] + "\n\n"
        output.write_text(content, encoding="utf-8")
        print(f"\n{GREEN}✓ docs/missing-sidebar-icons.tsx généré{RESET}")
    else:
        print(f"{GREEN}✓ Tous les engines ont une entrée Sidebar{RESET}")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "missing_icons": len(suggestions),
        "suggestions": [{"engine": s["engine"], "icon_name": s["icon_name"]} for s in suggestions[:20]],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_generator(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
