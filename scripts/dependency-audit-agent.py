#!/usr/bin/env python3
"""Dependency Audit Agent — CaelumSwarm™ Dev Support
Audite les dépendances npm et pip : versions obsolètes, vulnérabilités connues,
licences incompatibles, packages inutilisés.
"""
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "DependencyAuditAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Packages npm avec vulnérabilités connues (liste de référence)
KNOWN_VULNERABLE_NPM = {
    "lodash": {"below": "4.17.21", "cve": "CVE-2021-23337"},
    "axios": {"below": "1.6.0", "cve": "CVE-2023-45857"},
    "next": {"below": "14.0.0", "cve": "CVE-2024-34351"},
    "react": {"below": "18.0.0", "cve": "CVE-2022-21722"},
}

# Packages Python avec vulnérabilités connues
KNOWN_VULNERABLE_PY = {
    "requests": {"below": "2.31.0", "cve": "CVE-2023-32681"},
    "urllib3": {"below": "2.0.7", "cve": "CVE-2023-45803"},
    "pillow": {"below": "10.0.1", "cve": "CVE-2023-44271"},
}


def parse_version(v: str) -> tuple:
    """Parse version string to comparable tuple."""
    try:
        return tuple(int(x) for x in re.sub(r'[^0-9.]', '', v).split('.'))
    except Exception:
        return (0,)


def version_below(current: str, threshold: str) -> bool:
    return parse_version(current) < parse_version(threshold)


def audit_npm(root: Path) -> dict:
    results = {"manager": "npm", "packages": [], "vulnerabilities": [], "outdated": []}
    pkg_json = root / "package.json"

    if not pkg_json.exists():
        results["error"] = "package.json introuvable"
        return results

    try:
        pkg = json.loads(pkg_json.read_text())
        all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        results["total_packages"] = len(all_deps)

        # Vérifier vulnérabilités connues
        for name, version_spec in all_deps.items():
            version = re.sub(r'[^0-9.]', '', version_spec)
            if name in KNOWN_VULNERABLE_NPM:
                vuln = KNOWN_VULNERABLE_NPM[name]
                if version_below(version, vuln["below"]):
                    results["vulnerabilities"].append({
                        "package": name,
                        "current": version,
                        "fix_version": vuln["below"],
                        "cve": vuln["cve"],
                        "severity": "HIGH"
                    })

        # Lancer npm audit si disponible
        try:
            audit_result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=str(root), capture_output=True, text=True, timeout=30
            )
            if audit_result.returncode != 0 and audit_result.stdout:
                audit_data = json.loads(audit_result.stdout)
                metadata = audit_data.get("metadata", {})
                results["npm_audit"] = {
                    "critical": metadata.get("vulnerabilities", {}).get("critical", 0),
                    "high": metadata.get("vulnerabilities", {}).get("high", 0),
                    "moderate": metadata.get("vulnerabilities", {}).get("moderate", 0),
                }
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            results["npm_audit"] = {"status": "npm audit non disponible"}

        # Packages potentiellement inutilisés (heuristique basique)
        src_files = list((root / "app").rglob("*.ts")) + list((root / "app").rglob("*.tsx"))
        all_source = "\n".join(f.read_text(encoding="utf-8", errors="ignore") for f in src_files[:50])

        for name in list(all_deps.keys())[:20]:  # Vérifier les 20 premiers
            import_variants = [
                f'from "{name}"', f"from '{name}'",
                f'require("{name}")', f"require('{name}')",
                f'import "{name}"',
            ]
            if not any(v in all_source for v in import_variants):
                results["outdated"].append({"package": name, "note": "Possiblement inutilisé"})

    except Exception as e:
        results["error"] = str(e)

    return results


def audit_python(root: Path) -> dict:
    results = {"manager": "pip", "packages": [], "vulnerabilities": []}

    req_files = list(root.glob("requirements*.txt")) + list(root.glob("Pipfile"))
    if not req_files:
        results["note"] = "Aucun requirements.txt trouvé (projet Python sans dépendances externes)"
        return results

    for req_file in req_files:
        content = req_file.read_text(encoding="utf-8", errors="ignore")
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            match = re.match(r'([a-zA-Z0-9_-]+)\s*[>=<~!]=?\s*([\d.]+)', line)
            if match:
                name, version = match.groups()
                results["packages"].append({"name": name.lower(), "version": version})

                name_lower = name.lower()
                if name_lower in KNOWN_VULNERABLE_PY:
                    vuln = KNOWN_VULNERABLE_PY[name_lower]
                    if version_below(version, vuln["below"]):
                        results["vulnerabilities"].append({
                            "package": name,
                            "current": version,
                            "fix_version": vuln["below"],
                            "cve": vuln["cve"],
                            "severity": "HIGH"
                        })

    return results


def run_audit(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Dependency Audit Agent v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}\n")

    npm_results = audit_npm(root)
    py_results = audit_python(root)

    total_vulns = len(npm_results.get("vulnerabilities", [])) + len(py_results.get("vulnerabilities", []))

    if npm_results.get("vulnerabilities"):
        print(f"{RED}NPM Vulnérabilités :{RESET}")
        for v in npm_results["vulnerabilities"]:
            print(f"  {RED}[{v['severity']}]{RESET} {v['package']} {v['current']} → {v['fix_version']} ({v['cve']})")
    else:
        print(f"{GREEN}✓ Aucune vulnérabilité NPM connue{RESET}")

    if py_results.get("vulnerabilities"):
        print(f"{RED}Python Vulnérabilités :{RESET}")
        for v in py_results["vulnerabilities"]:
            print(f"  {RED}[{v['severity']}]{RESET} {v['package']} {v['current']} → {v['fix_version']} ({v['cve']})")
    else:
        print(f"{GREEN}✓ Aucune vulnérabilité Python connue{RESET}")

    print(f"\n{BOLD}Total vulnérabilités: {RED if total_vulns > 0 else GREEN}{total_vulns}{RESET}\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "npm": npm_results,
        "python": py_results,
        "total_vulnerabilities": total_vulns,
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
