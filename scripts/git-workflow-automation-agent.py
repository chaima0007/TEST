#!/usr/bin/env python3
"""Git Workflow Automation Agent — CaelumSwarm™ Dev Support
Automatise les tâches git répétitives : vérification de branche,
détection de fichiers non committés, commit groupé par type de fichier,
rapport de divergence avec la branche principale.
"""
import subprocess
import re
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "GitWorkflowAutomationAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

MAIN_BRANCH = "claude/swarm-50-agent-architecture-3l6cno"
REQUIRED_EMAIL = "noreply@anthropic.com"
REQUIRED_NAME = "Claude"


def run_git(args: list[str], cwd: str = "/home/user/TEST") -> tuple[str, str, int]:
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def check_branch(cwd: str) -> dict:
    stdout, _, _ = run_git(["branch", "--show-current"], cwd)
    current = stdout.strip()
    ok = current == MAIN_BRANCH
    return {
        "current": current,
        "expected": MAIN_BRANCH,
        "ok": ok,
        "issue": f"Mauvaise branche! Attendu: {MAIN_BRANCH}" if not ok else None
    }


def check_config(cwd: str) -> dict:
    email_out, _, _ = run_git(["config", "user.email"], cwd)
    name_out, _, _ = run_git(["config", "user.name"], cwd)
    ok = email_out == REQUIRED_EMAIL and name_out == REQUIRED_NAME
    return {
        "email": email_out,
        "name": name_out,
        "ok": ok,
    }


def get_untracked_files(cwd: str) -> dict:
    stdout, _, _ = run_git(["status", "--short"], cwd)
    untracked = [l[3:].strip() for l in stdout.splitlines() if l.startswith("??")]
    modified = [l[3:].strip() for l in stdout.splitlines() if l.startswith(" M") or l.startswith("M ")]
    staged = [l[3:].strip() for l in stdout.splitlines() if l.startswith("A ") or l.startswith("AM")]
    return {"untracked": untracked, "modified": modified, "staged": staged}


def categorize_files(files: list[str]) -> dict:
    """Catégorise les fichiers pour des commits atomiques."""
    categories = {
        "engines": [],
        "routes": [],
        "dashboards": [],
        "sidebar": [],
        "scripts": [],
        "docs": [],
        "other": [],
    }
    for f in files:
        if "swarm/intelligence" in f and f.endswith(".py"):
            categories["engines"].append(f)
        elif "app/api" in f:
            categories["routes"].append(f)
        elif "app/dashboard" in f:
            categories["dashboards"].append(f)
        elif "Sidebar.tsx" in f:
            categories["sidebar"].append(f)
        elif "scripts/" in f:
            categories["scripts"].append(f)
        elif f.endswith(".md") or "docs/" in f:
            categories["docs"].append(f)
        else:
            categories["other"].append(f)
    return {k: v for k, v in categories.items() if v}


def get_ahead_behind(cwd: str) -> dict:
    stdout, _, rc = run_git(["rev-list", "--left-right", "--count", f"origin/{MAIN_BRANCH}...HEAD"], cwd)
    if rc == 0 and stdout:
        parts = stdout.split("\t")
        if len(parts) == 2:
            return {"behind": int(parts[0]), "ahead": int(parts[1])}
    return {"behind": 0, "ahead": 0}


def get_recent_commits(cwd: str, n: int = 5) -> list[str]:
    stdout, _, _ = run_git(["log", f"--oneline", f"-{n}"], cwd)
    return stdout.splitlines()


def run_status_report(cwd: str = "/home/user/TEST") -> dict:
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Git Workflow Agent v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}\n")

    # Vérifications
    branch = check_branch(cwd)
    config = check_config(cwd)
    status = get_untracked_files(cwd)
    ahead_behind = get_ahead_behind(cwd)
    recent = get_recent_commits(cwd)

    # Affichage
    branch_color = GREEN if branch["ok"] else RED
    print(f"{BOLD}Branche :{RESET} {branch_color}{branch['current']}{RESET}")
    if not branch["ok"]:
        print(f"  {RED}ERREUR: {branch['issue']}{RESET}")
        print(f"  Correction: git checkout {MAIN_BRANCH}")

    config_color = GREEN if config["ok"] else YELLOW
    print(f"{BOLD}Config   :{RESET} {config_color}{config['name']} <{config['email']}>{RESET}")

    ahead = ahead_behind["ahead"]
    behind = ahead_behind["behind"]
    print(f"{BOLD}Sync     :{RESET} {GREEN if ahead > 0 else ''}{ahead} commits ahead{RESET} | {RED if behind > 0 else ''}{behind} behind{RESET}")

    all_pending = status["untracked"] + status["modified"]
    if all_pending:
        print(f"\n{YELLOW}{BOLD}Fichiers non committés ({len(all_pending)}) :{RESET}")
        categories = categorize_files(all_pending)
        for cat, files in categories.items():
            print(f"  {cat.upper()} ({len(files)}) :")
            for f in files[:3]:
                print(f"    ?? {f}")
            if len(files) > 3:
                print(f"    ... +{len(files)-3} autres")

        print(f"\n{BOLD}Ordre de commit recommandé :{RESET}")
        order = ["engines", "routes", "sidebar", "dashboards", "scripts", "docs", "other"]
        for i, cat in enumerate(order, 1):
            if cat in categories:
                files = categories[cat]
                msg = f"feat: Wave XXX — {cat} ({len(files)} fichiers)"
                print(f"  {i}. git add {' '.join(files[:2])}{'...' if len(files) > 2 else ''}")
                print(f"     git commit -m \"{msg}\"")
    else:
        print(f"\n{GREEN}✓ Working tree propre — rien à committer{RESET}")

    print(f"\n{BOLD}Derniers commits :{RESET}")
    for commit in recent:
        print(f"  {commit}")

    print()

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "branch": branch,
        "config": config,
        "status": status,
        "ahead_behind": ahead_behind,
        "pending_categories": categorize_files(status["untracked"] + status["modified"]),
        "recent_commits": recent,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def auto_commit(cwd: str = "/home/user/TEST", message: str = "", dry_run: bool = True) -> dict:
    """Commit automatique par catégorie."""
    status = get_untracked_files(cwd)
    all_pending = status["untracked"] + status["modified"]
    categories = categorize_files(all_pending)

    if not categories:
        return {"status": "nothing_to_commit"}

    commits = []
    order = ["engines", "routes", "sidebar", "dashboards", "scripts", "docs", "other"]

    for cat in order:
        if cat not in categories:
            continue
        files = categories[cat]
        if not message:
            auto_msg = f"feat: {cat} — {len(files)} fichier(s) ajouté(s)"
        else:
            auto_msg = message

        if not dry_run:
            run_git(["add"] + files, cwd)
            _, _, rc = run_git(["commit", "-m", auto_msg], cwd)
            commits.append({"category": cat, "files": files, "message": auto_msg, "committed": rc == 0})
        else:
            commits.append({"category": cat, "files": files, "message": auto_msg, "committed": False, "dry_run": True})

    return {"commits": commits, "mode": "dry_run" if dry_run else "applied"}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CaelumSwarm Git Workflow Agent")
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--status", action="store_true", default=True, help="Afficher le statut git")
    parser.add_argument("--auto-commit", action="store_true", help="Commit automatique par catégorie")
    parser.add_argument("--apply", action="store_true", help="Appliquer (sinon dry-run)")
    parser.add_argument("--message", default="", help="Message de commit personnalisé")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.auto_commit:
        result = auto_commit(args.root, args.message, dry_run=not args.apply)
    else:
        result = run_status_report(args.root)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
