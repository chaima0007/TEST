#!/usr/bin/env python3
"""Code Quality Review Agent — CaelumSwarm™ Dev Support
Analyse statique : détecte les anti-patterns, code mort, complexité cyclomatique,
fichiers trop longs, imports inutilisés, fonctions dupliquées.
"""
import os
import re
import ast
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

AGENT_NAME = "CodeQualityReviewAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

MAX_FILE_LINES = 500
MAX_FUNCTION_LINES = 80
MAX_CYCLOMATIC = 10


def count_cyclomatic(source: str) -> int:
    """Complexité cyclomatique McCabe (branches if/for/while/except/and/or)."""
    keywords = len(re.findall(r'\b(if|elif|for|while|except|and|or|assert)\b', source))
    return keywords + 1


def analyze_python_file(filepath: Path) -> dict:
    issues = []
    try:
        source = filepath.read_text(encoding="utf-8")
        lines = source.splitlines()

        # Fichier trop long
        if len(lines) > MAX_FILE_LINES:
            issues.append({"severity": "WARNING", "rule": "FILE_TOO_LONG",
                           "message": f"{len(lines)} lignes (max {MAX_FILE_LINES})"})

        # Analyse AST
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            issues.append({"severity": "CRITICAL", "rule": "SYNTAX_ERROR", "message": str(e)})
            return {"file": str(filepath), "issues": issues, "score": 0}

        # Fonctions trop longues
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_lines = (node.end_lineno or node.lineno) - node.lineno
                if func_lines > MAX_FUNCTION_LINES:
                    issues.append({"severity": "WARNING", "rule": "FUNCTION_TOO_LONG",
                                   "message": f"Fonction '{node.name}' — {func_lines} lignes (max {MAX_FUNCTION_LINES})"})

        # Complexité cyclomatique
        cc = count_cyclomatic(source)
        if cc > MAX_CYCLOMATIC:
            issues.append({"severity": "WARNING", "rule": "HIGH_COMPLEXITY",
                           "message": f"Complexité cyclomatique {cc} (max {MAX_CYCLOMATIC})"})

        # Variables non utilisées (simples heuristiques)
        assigned = re.findall(r'^(\s+)([a-z_]\w+)\s*=', source, re.MULTILINE)
        for indent, var in assigned:
            if source.count(var) == 1 and var not in ("_", "__"):
                issues.append({"severity": "INFO", "rule": "UNUSED_VARIABLE",
                               "message": f"Variable possiblement inutilisée: '{var}'"})

        # Print dans le code (hors __main__)
        prints_outside_main = re.findall(r'(?<!#)\bprint\(', source)
        main_block = source.find('if __name__')
        if main_block > 0:
            before_main = source[:main_block]
            debug_prints = len(re.findall(r'(?<!#)\bprint\(', before_main))
            if debug_prints > 5:
                issues.append({"severity": "INFO", "rule": "TOO_MANY_PRINTS",
                               "message": f"{debug_prints} print() avant __main__ (potentiel debug)"})

    except Exception as e:
        issues.append({"severity": "ERROR", "rule": "ANALYSIS_ERROR", "message": str(e)})

    score = max(0, 100 - len([i for i in issues if i["severity"] == "CRITICAL"]) * 30
                - len([i for i in issues if i["severity"] == "WARNING"]) * 10
                - len([i for i in issues if i["severity"] == "INFO"]) * 2)
    return {"file": str(filepath.relative_to(Path("/home/user/TEST"))),
            "issues": issues, "score": score}


def analyze_typescript_file(filepath: Path) -> dict:
    issues = []
    try:
        source = filepath.read_text(encoding="utf-8")
        lines = source.splitlines()

        if len(lines) > MAX_FILE_LINES:
            issues.append({"severity": "WARNING", "rule": "FILE_TOO_LONG",
                           "message": f"{len(lines)} lignes (max {MAX_FILE_LINES})"})

        # "use client" manquant dans les pages dashboard
        if "dashboard" in str(filepath) and "page.tsx" in filepath.name:
            if not source.startswith('"use client"') and not source.startswith("'use client'"):
                issues.append({"severity": "CRITICAL", "rule": "MISSING_USE_CLIENT",
                               "message": '"use client" absent en première ligne'})

        # console.log laissés
        debug_logs = len(re.findall(r'\bconsole\.log\(', source))
        if debug_logs > 0:
            issues.append({"severity": "INFO", "rule": "DEBUG_CONSOLE_LOG",
                           "message": f"{debug_logs} console.log() trouvés"})

        # any type utilisé
        any_count = len(re.findall(r':\s*any\b', source))
        if any_count > 3:
            issues.append({"severity": "WARNING", "rule": "EXCESSIVE_ANY_TYPE",
                           "message": f"{any_count} utilisations de 'any' (risque sécurité typage)"})

        # sealResponse manquant dans les routes API
        if "app/api" in str(filepath) and "route.ts" in filepath.name:
            if "sealResponse" not in source:
                issues.append({"severity": "CRITICAL", "rule": "MISSING_SEAL_RESPONSE",
                               "message": "sealResponse manquant dans la route API"})
            if "SWARM_API_URL" not in source:
                issues.append({"severity": "CRITICAL", "rule": "MISSING_SWARM_GUARD",
                               "message": "Guard SWARM_API_URL manquant"})
            if "status: 503" in source:
                issues.append({"severity": "WARNING", "rule": "WRONG_STATUS_503",
                               "message": "status 503 trouvé — doit être 502 selon le protocole"})

        # Apostrophes non échappées en JSX
        jsx_apostrophes = len(re.findall(r">([^<]*'[^<]*)<", source))
        if jsx_apostrophes > 0:
            issues.append({"severity": "WARNING", "rule": "UNESCAPED_APOSTROPHE",
                           "message": f"{jsx_apostrophes} apostrophes non échappées en JSX (utiliser &apos;)"})

    except Exception as e:
        issues.append({"severity": "ERROR", "rule": "ANALYSIS_ERROR", "message": str(e)})

    score = max(0, 100 - len([i for i in issues if i["severity"] == "CRITICAL"]) * 30
                - len([i for i in issues if i["severity"] == "WARNING"]) * 10
                - len([i for i in issues if i["severity"] == "INFO"]) * 2)
    return {"file": str(filepath.relative_to(Path("/home/user/TEST"))),
            "issues": issues, "score": score}


def run_review(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Code Quality Review Agent v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*70}{RESET}\n")

    results = []
    total_issues = defaultdict(int)

    # Python engines
    py_files = list((root / "swarm" / "intelligence").glob("*.py"))
    py_files += list((root / "scripts").glob("*.py"))
    print(f"{BLUE}Analyse Python: {len(py_files)} fichiers...{RESET}")
    for f in py_files:
        r = analyze_python_file(f)
        results.append(r)
        for issue in r["issues"]:
            total_issues[issue["severity"]] += 1

    # TypeScript routes et dashboards
    ts_files = list((root / "app" / "api").rglob("route.ts"))
    ts_files += list((root / "app" / "dashboard").rglob("page.tsx"))
    print(f"{BLUE}Analyse TypeScript: {len(ts_files)} fichiers...{RESET}")
    for f in ts_files:
        r = analyze_typescript_file(f)
        results.append(r)
        for issue in r["issues"]:
            total_issues[issue["severity"]] += 1

    # Tri par score (pires en premier)
    results.sort(key=lambda x: x["score"])

    # Affichage des 10 pires fichiers
    print(f"\n{BOLD}Top 10 fichiers à améliorer :{RESET}")
    for r in results[:10]:
        color = RED if r["score"] < 60 else YELLOW if r["score"] < 80 else GREEN
        print(f"  {color}{r['score']:3d}/100{RESET}  {r['file']}")
        for issue in r["issues"][:2]:
            sev_color = RED if issue["severity"] == "CRITICAL" else YELLOW if issue["severity"] == "WARNING" else BLUE
            print(f"         {sev_color}[{issue['severity']}] {issue['rule']}: {issue['message']}{RESET}")

    avg_score = sum(r["score"] for r in results) / len(results) if results else 0
    print(f"\n{BOLD}Score global : {avg_score:.1f}/100{RESET}")
    print(f"  CRITICAL: {total_issues['CRITICAL']} | WARNING: {total_issues['WARNING']} | INFO: {total_issues['INFO']}\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "total_files": len(results),
        "avg_score": round(avg_score, 2),
        "total_issues": dict(total_issues),
        "results": results,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_review(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
