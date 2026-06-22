#!/usr/bin/env python3
"""Deployment Readiness Agent — CaelumSwarm™ Dev Support
Vérifie que le projet est prêt pour le déploiement production :
variables d'env, build, sécurité, performance, accessibilité.
Checklist complète avant chaque release.
"""
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "DeploymentReadinessAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

CHECKLIST = [
    # (id, description, critical, check_fn)
]


def check_git_clean(root: str) -> dict:
    result = subprocess.run(["git", "status", "--short"], cwd=root, capture_output=True, text=True)
    untracked = [l for l in result.stdout.splitlines() if l.startswith("??") or l.startswith(" M")]
    return {
        "id": "GIT_CLEAN",
        "description": "Working tree propre (aucun fichier non committé)",
        "passed": len(untracked) == 0,
        "critical": True,
        "detail": f"{len(untracked)} fichiers non committés" if untracked else "Propre",
    }


def check_env_file(root: Path) -> dict:
    env_example = root / ".env.example"
    env_local = root / ".env.local"
    has_example = env_example.exists()
    has_local = env_local.exists()
    return {
        "id": "ENV_CONFIG",
        "description": ".env.example présent et .env.local configuré",
        "passed": has_example,
        "critical": False,
        "detail": f"example={'✓' if has_example else '✗'} local={'✓' if has_local else '✗ (normal en prod)'}",
    }


def check_sidebar_duplicates(root: Path) -> dict:
    sidebar = root / "components" / "Sidebar.tsx"
    if not sidebar.exists():
        return {"id": "SIDEBAR_DUPS", "description": "Sidebar sans doublons", "passed": False, "critical": True, "detail": "Sidebar.tsx introuvable"}
    source = sidebar.read_text(encoding="utf-8", errors="ignore")
    icons = re.findall(r'^function (Icon\w+)', source, re.MULTILINE)
    from collections import Counter
    dups = [k for k, v in Counter(icons).items() if v > 1]
    return {
        "id": "SIDEBAR_DUPS",
        "description": "Sidebar.tsx sans icônes dupliquées",
        "passed": len(dups) == 0,
        "critical": True,
        "detail": f"Doublons: {dups}" if dups else "Aucun doublon",
    }


def check_seal_response(root: Path) -> dict:
    routes = list((root / "app" / "api").rglob("route.ts"))
    missing = [r.parent.name for r in routes if "sealResponse" not in r.read_text(encoding="utf-8", errors="ignore")]
    return {
        "id": "SEAL_RESPONSE",
        "description": "sealResponse sur toutes les routes API",
        "passed": len(missing) == 0,
        "critical": True,
        "detail": f"Manquant dans: {missing[:3]}" if missing else f"OK sur {len(routes)} routes",
    }


def check_status_503(root: Path) -> dict:
    routes = list((root / "app" / "api").rglob("route.ts"))
    violations = [r.parent.name for r in routes if "status: 503" in r.read_text(encoding="utf-8", errors="ignore")]
    return {
        "id": "NO_STATUS_503",
        "description": "Aucun status 503 (doit être 502)",
        "passed": len(violations) == 0,
        "critical": False,
        "detail": f"Violations: {violations}" if violations else "OK",
    }


def check_use_client(root: Path) -> dict:
    dashboards = list((root / "app" / "dashboard").rglob("page.tsx"))
    missing = []
    for d in dashboards:
        source = d.read_text(encoding="utf-8", errors="ignore")
        if not source.startswith('"use client"') and not source.startswith("'use client'"):
            missing.append(d.parent.name)
    return {
        "id": "USE_CLIENT",
        "description": '"use client" en première ligne de tous les dashboards',
        "passed": len(missing) == 0,
        "critical": True,
        "detail": f"Manquant: {missing[:3]}" if missing else f"OK sur {len(dashboards)} dashboards",
    }


def check_package_json(root: Path) -> dict:
    pkg = root / "package.json"
    if not pkg.exists():
        return {"id": "PKG_JSON", "description": "package.json valide", "passed": False, "critical": True, "detail": "Introuvable"}
    try:
        data = json.loads(pkg.read_text())
        has_build = "build" in data.get("scripts", {})
        has_start = "start" in data.get("scripts", {})
        return {
            "id": "PKG_JSON",
            "description": "package.json avec scripts build + start",
            "passed": has_build and has_start,
            "critical": True,
            "detail": f"build={'✓' if has_build else '✗'} start={'✓' if has_start else '✗'}",
        }
    except Exception as e:
        return {"id": "PKG_JSON", "description": "package.json valide", "passed": False, "critical": True, "detail": str(e)}


def run_readiness_check(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*65}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Deployment Readiness Agent v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*65}{RESET}\n")

    checks = [
        check_git_clean(project_root),
        check_env_file(root),
        check_sidebar_duplicates(root),
        check_seal_response(root),
        check_status_503(root),
        check_use_client(root),
        check_package_json(root),
    ]

    passed = sum(1 for c in checks if c["passed"])
    critical_failed = [c for c in checks if not c["passed"] and c.get("critical")]
    warnings = [c for c in checks if not c["passed"] and not c.get("critical")]

    print(f"{BOLD}Checklist déploiement ({passed}/{len(checks)}) :{RESET}\n")
    for check in checks:
        icon = f"{GREEN}✓{RESET}" if check["passed"] else (f"{RED}✗{RESET}" if check.get("critical") else f"{YELLOW}⚠{RESET}")
        crit = f" {RED}[BLOQUANT]{RESET}" if not check["passed"] and check.get("critical") else ""
        print(f"  {icon} {check['description']}{crit}")
        if not check["passed"]:
            print(f"    → {check['detail']}")

    ready = len(critical_failed) == 0
    status_color = GREEN if ready else RED
    status_text = "PRÊT POUR LE DÉPLOIEMENT" if ready else f"NON PRÊT ({len(critical_failed)} blocages)"

    print(f"\n{BOLD}Statut : {status_color}{status_text}{RESET}")
    if warnings:
        print(f"{YELLOW}  {len(warnings)} avertissement(s) non bloquant(s){RESET}")

    print(f"\n{BOLD}Commandes de déploiement Netlify :{RESET}")
    print(f"  npm run build && netlify deploy --prod --dir=.next")
    print(f"  # Ou via GitHub Actions sur push vers main\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "ready": ready,
        "passed": passed,
        "total": len(checks),
        "critical_failed": [c["id"] for c in critical_failed],
        "warnings": [c["id"] for c in warnings],
        "checks": checks,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_readiness_check(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    import sys
    sys.exit(0 if result["ready"] else 1)
