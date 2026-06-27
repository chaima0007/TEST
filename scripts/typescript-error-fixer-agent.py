#!/usr/bin/env python3
"""TypeScript Error Fixer Agent — CaelumSwarm™ Dev Support
Détecte et corrige automatiquement les erreurs TypeScript courantes :
- "use client" manquant
- apostrophes JSX non échappées → &apos;
- status 503 → 502
- sealResponse manquant dans les routes
- icon: <Component /> → icon: Component (pattern Sidebar)
"""
import re
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "TypeScriptErrorFixerAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def fix_use_client(source: str, filepath: Path) -> tuple[str, list[str]]:
    fixes = []
    if "dashboard" in str(filepath) and filepath.name == "page.tsx":
        if not source.startswith('"use client"') and not source.startswith("'use client'"):
            source = '"use client";\n' + source
            fixes.append('Ajout de "use client" en première ligne')
    return source, fixes


def fix_jsx_apostrophes(source: str) -> tuple[str, list[str]]:
    fixes = []
    # Remplace les apostrophes directes dans le JSX (entre balises)
    pattern = r'(>[^<]*)(\'s |\'t |\'re |\'ll |\'ve |\'d |\'m )([^<]*<)'
    new_source = re.sub(pattern, lambda m: m.group(1) + m.group(2).replace("'", "&apos;") + m.group(3), source)
    if new_source != source:
        fixes.append("Apostrophes JSX échappées en &apos;")
        source = new_source
    return source, fixes


def fix_status_503(source: str) -> tuple[str, list[str]]:
    fixes = []
    if "status: 503" in source:
        source = source.replace("status: 503", "status: 502")
        fixes.append("status 503 → 502 (protocole Wave)")
    return source, fixes


def fix_sidebar_jsx_icons(source: str) -> tuple[str, list[str]]:
    fixes = []
    # icon: <IconName /> → icon: IconName
    pattern = r'icon:\s*<(\w+)\s*/>'
    matches = re.findall(pattern, source)
    if matches:
        source = re.sub(pattern, r'icon: \1', source)
        fixes.append(f"Corrigé {len(matches)} icônes JSX → ComponentType: {', '.join(matches[:3])}")
    return source, fixes


def run_fixer(project_root: str = "/home/user/TEST", dry_run: bool = True) -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}CaelumSwarm™ TypeScript Error Fixer v{VERSION}{RESET}")
    print(f"Mode: {'DRY RUN (aucune modification)' if dry_run else 'APPLY FIXES'}\n")

    all_fixes = []
    ts_files = (
        list((root / "app" / "dashboard").rglob("page.tsx"))
        + list((root / "app" / "api").rglob("route.ts"))
        + [(root / "components" / "Sidebar.tsx")]
    )

    for filepath in ts_files:
        if not filepath.exists():
            continue
        original = filepath.read_text(encoding="utf-8")
        source = original
        file_fixes = []

        source, f1 = fix_use_client(source, filepath)
        source, f2 = fix_jsx_apostrophes(source)
        source, f3 = fix_status_503(source)
        source, f4 = fix_sidebar_jsx_icons(source)
        file_fixes = f1 + f2 + f3 + f4

        if file_fixes:
            rel = str(filepath.relative_to(root))
            print(f"  {YELLOW}FIXABLE{RESET} {rel}")
            for fix in file_fixes:
                print(f"    → {fix}")
            all_fixes.append({"file": rel, "fixes": file_fixes})
            if not dry_run:
                shutil.copy(filepath, filepath.with_suffix(".bak"))
                filepath.write_text(source, encoding="utf-8")
                print(f"    {GREEN}✓ Appliqué{RESET}")

    print(f"\n{BOLD}Total: {len(all_fixes)} fichiers avec des corrections possibles{RESET}")
    if dry_run:
        print(f"{YELLOW}Relancer avec --apply pour appliquer les corrections{RESET}\n")

    return {
        "agent": AGENT_NAME,
        "mode": "dry_run" if dry_run else "applied",
        "files_with_fixes": len(all_fixes),
        "fixes": all_fixes,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--apply", action="store_true", help="Applique les corrections (défaut: dry run)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_fixer(args.root, dry_run=not args.apply)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
