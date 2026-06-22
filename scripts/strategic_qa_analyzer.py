#!/usr/bin/env python3
"""
CaelumSwarm™ — Strategic QA Analyzer
Analyse systématique des causes racines des erreurs récurrentes.
Détecte automatiquement les problèmes connus et les enregistre dans data/errors.json.

Usage:
  python3 scripts/strategic_qa_analyzer.py
  python3 scripts/strategic_qa_analyzer.py --fix          # tente les corrections automatiques
  python3 scripts/strategic_qa_analyzer.py --report       # rapport complet uniquement
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "data" / "errors.json"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# ─── Causes racines documentées des problèmes récurrents ─────────────────────

ROOT_CAUSES = {
    "stop_hook_untracked": {
        "why": "Les agents background créent des fichiers mais terminent avant d'exécuter git add/commit. "
               "Si le processus parent reprend sa surveillance trop tôt, le stop hook détecte ?? dans git status.",
        "systemic_cause": "Absence de séquençage strict : engines → commit → routes → commit → sidebar → commit. "
                          "Certains agents batchent tout à la fin, ce qui crée une fenêtre de vulnérabilité.",
        "prevention": "Committer IMMÉDIATEMENT après chaque groupe de fichiers. Ne jamais battre les commits.",
        "recurrence_factor": "HIGH — Se produit à chaque wave où un agent parallèle est interrompu.",
    },
    "stop_hook_author": {
        "why": "git config user.email n'est pas exécuté au démarrage de l'agent, "
               "ou est écrasé par la config globale du système.",
        "systemic_cause": "La ligne 'git config user.email noreply@anthropic.com' est dans le template "
                          "mais certains agents la sautent si git pull échoue en amont et retournent early.",
        "prevention": "Mettre git config AVANT git checkout, jamais après. Vérifier avec 'git log -1 --format=%ae'.",
        "recurrence_factor": "MEDIUM — Corrigé par rebase reset-author mais nécessite force push.",
    },
    "sidebar_oom": {
        "why": "sidebar-icons.tsx dépasse la limite mémoire TypeScript/Turbopack (~6000 lignes par fichier).",
        "systemic_cause": "Chaque wave ajoute 3 fonctions SVG (~25 lignes chacune) à sidebar-icons-4.tsx. "
                          "Après ~200 waves, le fichier dépasse le seuil critique.",
        "prevention": "Surveiller `wc -l components/sidebar-icons-4.tsx`. À 5500 lignes → créer sidebar-icons-5.tsx.",
        "recurrence_factor": "PREDICTABLE — Se produira exactement quand sidebar-icons-4.tsx > 6000 lignes.",
    },
    "deprecated_config_key": {
        "why": "Next.js 16.x a supprimé certaines clés de configuration (eslint, experimental.*) "
               "sans dépréciation graduelle.",
        "systemic_cause": "next.config.ts est rarement relu entre les waves. Les clés obsolètes "
                          "ne déclenchent pas d'erreur de build, seulement des warnings Vercel.",
        "prevention": "Lire next.config.ts à chaque changement majeur de version Next.js.",
        "recurrence_factor": "LOW — Corrigé une fois, peu probable de revenir.",
    },
    "route_missing_security": {
        "why": "Certains agents créent des routes API avec juste NextResponse.json(data) sans sealResponse.",
        "systemic_cause": "Template copié-collé incorrectement, ou agent qui improvise sans lire le pattern.",
        "prevention": "predict-errors.py scanne les routes avant commit. Ajouter ce scan au hook pre-commit.",
        "recurrence_factor": "MEDIUM — Corrigé par le scan systématique, revient si de nouveaux agents ignorent le template.",
    },
}


def _read_db() -> dict:
    if not DB_PATH.exists():
        return {"version": 1, "last_id": 0, "errors": []}
    try:
        return json.loads(DB_PATH.read_text("utf-8"))
    except Exception:
        return {"version": 1, "last_id": 0, "errors": []}


def _write_db(db: dict) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.write_text(json.dumps(db, indent=2, ensure_ascii=False), "utf-8")


def _log_error(db: dict, error_type: str, description: str, cause: str,
               file_path: str | None = None, fix_applied: str | None = None,
               wave: int | None = None) -> dict:
    existing = next(
        (e for e in db["errors"]
         if e["description"] == description and e["status"] in ("open", "recurring")),
        None
    )
    if existing:
        existing["recurrence_count"] += 1
        existing["status"] = "recurring"
        return existing

    record = {
        "id": db["last_id"] + 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error_type": error_type,
        "file_path": file_path,
        "description": description,
        "cause": cause,
        "fix_applied": fix_applied,
        "resolution_time_minutes": None,
        "wave": wave,
        "recurrence_count": 1,
        "status": "fixed" if fix_applied else "open",
    }
    db["last_id"] = record["id"]
    db["errors"].append(record)
    return record


# ─── Checks ──────────────────────────────────────────────────────────────────

def check_untracked_files() -> list[str]:
    """Détecte les fichiers non-commités dans le working tree."""
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True, text=True, cwd=ROOT
    )
    untracked = [
        line[3:].strip()
        for line in result.stdout.splitlines()
        if line.startswith("??")
    ]
    return untracked


def check_git_author() -> tuple[bool, str]:
    """Vérifie que le dernier commit a le bon auteur."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ae"],
        capture_output=True, text=True, cwd=ROOT
    )
    email = result.stdout.strip()
    return email == "noreply@anthropic.com", email


def check_sidebar_size() -> dict:
    """Vérifie la taille de sidebar-icons-4.tsx."""
    icons_file = ROOT / "components" / "sidebar-icons-4.tsx"
    if not icons_file.exists():
        return {"exists": False, "lines": 0, "risk": "unknown"}
    lines = len(icons_file.read_text("utf-8").splitlines())
    risk = "critical" if lines > 5500 else "high" if lines > 4500 else "ok"
    return {"exists": True, "lines": lines, "risk": risk}


def check_route_security() -> list[str]:
    """Détecte les routes API sans pattern sécurité complet."""
    bad_routes = []
    api_dir = ROOT / "app" / "api"
    for route_file in api_dir.rglob("route.ts"):
        content = route_file.read_text("utf-8", errors="ignore")
        has_seal = "sealResponse" in content
        has_guard = "SWARM_API_URL" in content
        has_502 = "502" in content
        if not (has_seal and has_guard and has_502):
            missing = []
            if not has_seal: missing.append("sealResponse")
            if not has_guard: missing.append("SWARM_API_URL guard")
            if not has_502: missing.append("502 fallback")
            bad_routes.append(f"{route_file.relative_to(ROOT)} [{', '.join(missing)}]")
    return bad_routes


def check_duplicate_icons() -> list[str]:
    """Détecte les icônes dupliquées dans les fichiers sidebar-icons."""
    all_icons = []
    for f in sorted((ROOT / "components").glob("sidebar-icons*.tsx")):
        if f.name == "sidebar-icons.tsx":
            continue
        for line in f.read_text("utf-8", errors="ignore").splitlines():
            m = re.match(r"^export function (Icon\w+)", line)
            if m:
                all_icons.append((m.group(1), f.name))
    seen: dict[str, list[str]] = {}
    for icon, fname in all_icons:
        seen.setdefault(icon, []).append(fname)
    return [f"{icon}: {files}" for icon, files in seen.items() if len(files) > 1]


def check_next_config() -> list[str]:
    """Vérifie que next.config.ts ne contient pas de clés obsolètes."""
    config_file = ROOT / "next.config.ts"
    if not config_file.exists():
        return []
    content = config_file.read_text("utf-8")
    warnings = []
    deprecated_keys = ["eslint:", "experimental.optimizePackageImports"]
    for key in deprecated_keys:
        if key in content:
            warnings.append(f"Clé obsolète détectée: {key}")
    return warnings


# ─── Main ─────────────────────────────────────────────────────────────────────

def run_analysis(auto_log: bool = True) -> dict:
    print(f"\n{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ — Strategic QA Analyzer{RESET}")
    print(f"{BOLD}{CYAN}  Analyse des causes racines des erreurs récurrentes{RESET}")
    print(f"{BOLD}{CYAN}╚══════════════════════════════════════════════════════════════╝{RESET}\n")

    db = _read_db()
    issues_found = []
    issues_fixed = []

    # 1. Fichiers non-commités
    untracked = check_untracked_files()
    if untracked:
        print(f"{RED}✗ STOP HOOK RISK: {len(untracked)} fichier(s) non-commité(s){RESET}")
        for f in untracked[:5]:
            print(f"  ?? {f}")
        issues_found.append("untracked_files")
        rc = ROOT_CAUSES["stop_hook_untracked"]
        print(f"\n  {YELLOW}Cause racine:{RESET} {rc['why']}")
        print(f"  {YELLOW}Facteur systémique:{RESET} {rc['systemic_cause']}")
        print(f"  {YELLOW}Prévention:{RESET} {rc['prevention']}")
        if auto_log:
            _log_error(db, "ci",
                       "Stop hook triggered — untracked files detected in working tree",
                       rc["why"],
                       file_path=", ".join(untracked[:3]))
    else:
        print(f"{GREEN}✓ Working tree propre — aucun fichier non-commité{RESET}")

    # 2. Auteur git
    correct_author, actual_email = check_git_author()
    if not correct_author:
        print(f"\n{RED}✗ AUTEUR GIT INCORRECT: {actual_email} (attendu: noreply@anthropic.com){RESET}")
        issues_found.append("wrong_author")
        rc = ROOT_CAUSES["stop_hook_author"]
        print(f"  {YELLOW}Cause racine:{RESET} {rc['why']}")
        print(f"  {YELLOW}Prévention:{RESET} {rc['prevention']}")
        if auto_log:
            _log_error(db, "ci",
                       f"Stop hook — git commit author incorrect: {actual_email}",
                       rc["why"])
    else:
        print(f"{GREEN}✓ Auteur git correct: {actual_email}{RESET}")

    # 3. Taille sidebar
    sidebar_info = check_sidebar_size()
    print(f"\n{BOLD}Sidebar Icons (sidebar-icons-4.tsx):{RESET}")
    if sidebar_info["risk"] == "critical":
        print(f"{RED}✗ CRITIQUE: {sidebar_info['lines']} lignes — CRÉER sidebar-icons-5.tsx MAINTENANT{RESET}")
        issues_found.append("sidebar_overflow")
        rc = ROOT_CAUSES["sidebar_oom"]
        print(f"  {YELLOW}Cause racine:{RESET} {rc['why']}")
        if auto_log:
            _log_error(db, "oom",
                       f"sidebar-icons-4.tsx dépasse le seuil critique ({sidebar_info['lines']} lignes)",
                       rc["why"],
                       file_path="components/sidebar-icons-4.tsx")
    elif sidebar_info["risk"] == "high":
        print(f"{YELLOW}⚠ ATTENTION: {sidebar_info['lines']} lignes — surveiller (seuil critique: 5500){RESET}")
    else:
        print(f"{GREEN}✓ {sidebar_info['lines']} lignes — OK{RESET}")

    # 4. Sécurité routes API
    print(f"\n{BOLD}Routes API — Pattern sécurité:{RESET}")
    bad_routes = check_route_security()
    if bad_routes:
        print(f"{RED}✗ {len(bad_routes)} route(s) sans pattern sécurité complet:{RESET}")
        for r in bad_routes[:5]:
            print(f"  - {r}")
        issues_found.append("insecure_routes")
        if auto_log:
            _log_error(db, "route",
                       f"{len(bad_routes)} routes API manquent sealResponse/SWARM_API_URL/502",
                       ROOT_CAUSES["route_missing_security"]["why"])
    else:
        total_routes = len(list((ROOT / "app" / "api").rglob("route.ts")))
        print(f"{GREEN}✓ {total_routes} routes sécurisées (100%){RESET}")

    # 5. Icônes dupliquées
    print(f"\n{BOLD}Icônes sidebar — Doublons:{RESET}")
    duplicates = check_duplicate_icons()
    if duplicates:
        print(f"{RED}✗ {len(duplicates)} doublon(s) détecté(s):{RESET}")
        for d in duplicates[:5]:
            print(f"  - {d}")
        issues_found.append("duplicate_icons")
        if auto_log:
            _log_error(db, "sidebar",
                       f"Icônes dupliquées détectées dans sidebar-icons: {', '.join(d.split(':')[0] for d in duplicates[:3])}",
                       "Deux agents parallèles ont ajouté la même icône au même fichier.")
    else:
        print(f"{GREEN}✓ Aucun doublon d'icône{RESET}")

    # 6. next.config.ts
    print(f"\n{BOLD}next.config.ts — Clés obsolètes:{RESET}")
    config_warnings = check_next_config()
    if config_warnings:
        print(f"{RED}✗ {len(config_warnings)} avertissement(s):{RESET}")
        for w in config_warnings:
            print(f"  - {w}")
        issues_found.append("deprecated_config")
        if auto_log:
            _log_error(db, "build",
                       "next.config.ts contient des clés obsolètes Next.js 16.x",
                       ROOT_CAUSES["deprecated_config_key"]["why"],
                       file_path="next.config.ts")
    else:
        print(f"{GREEN}✓ next.config.ts propre{RESET}")

    # ─── Résumé DB ────────────────────────────────────────────────────────────
    if auto_log:
        _write_db(db)

    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}ANALYSE DES CAUSES RACINES SYSTÉMIQUES{RESET}")
    print(f"{'─'*60}")
    for key, rc in ROOT_CAUSES.items():
        factor = rc["recurrence_factor"]
        color = RED if "HIGH" in factor else YELLOW if "MEDIUM" in factor else GREEN
        print(f"\n  {color}[{factor}]{RESET} {key}")
        print(f"  Pourquoi ça persiste: {rc['why'][:100]}...")
        print(f"  Prévention: {rc['prevention'][:100]}...")

    # ─── Stats DB ─────────────────────────────────────────────────────────────
    total = len(db["errors"])
    recurring = sum(1 for e in db["errors"] if e["recurrence_count"] > 1)
    open_count = sum(1 for e in db["errors"] if e["status"] == "open")
    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}BASE DE DONNÉES ERREURS — data/errors.json{RESET}")
    print(f"  Total enregistrements : {total}")
    print(f"  Récurrents (x>1)      : {recurring}")
    print(f"  Ouverts               : {open_count}")
    print(f"  Nouveaux logs session : {len(db['errors']) - (total - len(issues_found))}")

    status_icon = f"{GREEN}✓ AUCUN PROBLÈME CRITIQUE{RESET}" if not issues_found else \
                  f"{RED}✗ {len(issues_found)} PROBLÈME(S) DÉTECTÉ(S){RESET}"
    print(f"\n{BOLD}RÉSULTAT: {status_icon}{RESET}")

    return {
        "issues_found": issues_found,
        "issues_fixed": issues_fixed,
        "sidebar_lines": sidebar_info.get("lines", 0),
        "total_errors_in_db": total,
    }


if __name__ == "__main__":
    mode_fix = "--fix" in sys.argv
    mode_report = "--report" in sys.argv
    result = run_analysis(auto_log=not mode_report)
    sys.exit(0 if not result["issues_found"] else 1)
