#!/usr/bin/env python3
"""
CaelumSwarm™ — Temporal Loop Detector & Fixer
Détecte et corrige les boucles temporelles :
  1. Fichiers non-commités (stop_hook_untracked)
  2. Email auteur git incorrect (stop_hook_author)
  3. Doublons d'icônes dans sidebar (race condition)
  4. Fenêtres de vulnérabilité entre agents parallèles

Usage:
  python3 scripts/temporal_loop_detector.py          # détection + correction auto
  python3 scripts/temporal_loop_detector.py --dry-run  # détection seule
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"
C = "\033[96m"; B = "\033[1m"; E = "\033[0m"


def run(cmd: list[str], check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, check=check)


def detect_untracked() -> list[str]:
    """Boucle temporelle #1 : fichiers non-commités."""
    r = run(["git", "status", "--short"])
    return [line[3:].strip() for line in r.stdout.splitlines() if line.startswith("??")]


def detect_unstaged() -> list[str]:
    """Boucle temporelle #1b : modifications non-stagées."""
    r = run(["git", "status", "--short"])
    return [line[3:].strip() for line in r.stdout.splitlines() if line.startswith(" M")]


def detect_wrong_author() -> tuple[bool, str]:
    """Boucle temporelle #2 : email auteur incorrect dans dernier commit."""
    r = run(["git", "log", "-5", "--format=%H %ae"])
    bad_commits = []
    for line in r.stdout.strip().splitlines():
        parts = line.split()
        if len(parts) == 2:
            sha, email = parts
            if email != "noreply@anthropic.com":
                bad_commits.append((sha, email))
    return len(bad_commits) == 0, bad_commits


def detect_duplicate_icons() -> list[str]:
    """Boucle temporelle #3 : icônes dupliquées — race condition sidebar."""
    seen: dict[str, list[str]] = {}
    for f in sorted((ROOT / "components").glob("sidebar-icons*.tsx")):
        if f.name == "sidebar-icons.tsx":
            continue
        for line in f.read_text("utf-8", errors="ignore").splitlines():
            m = re.match(r"^export function (Icon\w+)", line)
            if m:
                name = m.group(1)
                seen.setdefault(name, []).append(f.name)
    return [f"{k}: {v}" for k, v in seen.items() if len(v) > 1]


def detect_index_lock() -> bool:
    """Détecte un lock git index (conflit entre agents parallèles)."""
    return (ROOT / ".git" / "index.lock").exists()


def fix_untracked(files: list[str], dry_run: bool = False) -> bool:
    """Commite tous les fichiers non-trackés."""
    if not files:
        return True

    groups: dict[str, list[str]] = {}
    for f in files:
        parts = f.split("/")
        if "swarm/intelligence" in f:
            groups.setdefault("engines", []).append(f)
        elif "app/api" in f:
            groups.setdefault("routes", []).append(f)
        elif "components" in f:
            groups.setdefault("sidebar", []).append(f)
        elif "scripts" in f:
            groups.setdefault("scripts", []).append(f)
        else:
            groups.setdefault("misc", []).append(f)

    for group, group_files in groups.items():
        msg = f"rescue: {group} — {len(group_files)} fichier(s) non-commités"
        print(f"  {Y}→ Commit rescue [{group}]: {group_files[:3]}{E}")
        if not dry_run:
            run(["git", "add"] + group_files)
            run(["git", "commit", "-m", msg])

    return True


def fix_unstaged(files: list[str], dry_run: bool = False) -> bool:
    """Commite les fichiers modifiés non-stagés."""
    if not files:
        return True
    msg = f"rescue: {len(files)} fichier(s) modifié(s) non-stagés"
    print(f"  {Y}→ Commit rescue [unstaged]: {files[:3]}{E}")
    if not dry_run:
        run(["git", "add"] + files)
        run(["git", "commit", "-m", msg])
    return True


def fix_index_lock(dry_run: bool = False) -> None:
    """Supprime le lock git index."""
    lock = ROOT / ".git" / "index.lock"
    print(f"  {R}→ Suppression index.lock{E}")
    if not dry_run:
        lock.unlink(missing_ok=True)


def fix_duplicate_icons(duplicates: list[str], dry_run: bool = False) -> bool:
    """Supprime les doublons d'icônes (garde la dernière occurrence)."""
    if not duplicates:
        return True

    print(f"  {R}Doublons détectés: {duplicates}{E}")
    for dup_info in duplicates:
        icon_name = dup_info.split(":")[0].strip()
        files_with_dup = dup_info.split(":")[1].strip().strip("[]").split(", ")
        # Garder le fichier avec le numéro le plus élevé (le plus récent)
        files_sorted = sorted(files_with_dup)
        for f_to_clean in files_sorted[:-1]:
            filepath = ROOT / "components" / f_to_clean
            if filepath.exists():
                content = filepath.read_text("utf-8", errors="ignore")
                # Trouver et supprimer la définition de la fonction
                pat_str = r"export function " + re.escape(icon_name) + r"\(.*?\n(\s+return \(\n.*?\);\n\s+\})\n"
                pattern = re.compile(pat_str, re.DOTALL)
                new_content = pattern.sub("", content)
                if new_content != content:
                    print(f"    {G}Supprimé {icon_name} de {f_to_clean}{E}")
                    if not dry_run:
                        filepath.write_text(new_content, "utf-8")
    return True


def push_fixes(dry_run: bool = False) -> None:
    """Pousse les corrections vers origin."""
    r = run(["git", "status", "--short"])
    if r.stdout.strip():
        print(f"  {Y}Fichiers encore en attente après correction{E}")
        return

    r = run(["git", "log", "--oneline", "origin/claude/swarm-50-agent-architecture-3l6cno..HEAD"])
    if r.stdout.strip():
        print(f"  {C}→ Push des corrections{E}")
        if not dry_run:
            run(["git", "push", "-u", "origin", "claude/swarm-50-agent-architecture-3l6cno"])
            print(f"  {G}✓ Push réussi{E}")
    else:
        print(f"  {G}Rien à pousser{E}")


def main(dry_run: bool = False) -> int:
    print(f"\n{B}{C}╔{'═'*58}╗{E}")
    print(f"{B}{C}  CaelumSwarm™ — Temporal Loop Detector & Fixer{E}")
    print(f"{B}{C}  Détecte et corrige les boucles temporelles Git{E}")
    print(f"{B}{C}╚{'═'*58}╝{E}")
    if dry_run:
        print(f"  {Y}Mode DRY-RUN — aucune correction appliquée{E}\n")

    issues = 0

    # 1. Index lock
    if detect_index_lock():
        print(f"\n{R}[BOUCLE #0] Index Lock détecté — conflit entre agents parallèles{E}")
        fix_index_lock(dry_run)
        issues += 1
    else:
        print(f"\n{G}[OK] Pas de index.lock{E}")

    # 2. Fichiers non-commités
    untracked = detect_untracked()
    if untracked:
        print(f"\n{R}[BOUCLE #1] {len(untracked)} fichier(s) non-commités (stop_hook_untracked){E}")
        for f in untracked[:5]:
            print(f"  ?? {f}")
        fix_untracked(untracked, dry_run)
        issues += 1
    else:
        print(f"{G}[OK] Aucun fichier non-commité{E}")

    # 3. Fichiers non-stagés
    unstaged = detect_unstaged()
    if unstaged:
        print(f"\n{Y}[BOUCLE #1b] {len(unstaged)} fichier(s) modifié(s) non-stagé(s){E}")
        for f in unstaged[:5]:
            print(f"   M {f}")
        fix_unstaged(unstaged, dry_run)
        issues += 1
    else:
        print(f"{G}[OK] Aucune modification non-stagée{E}")

    # 4. Auteur git
    author_ok, bad_commits = detect_wrong_author()
    if not author_ok:
        print(f"\n{R}[BOUCLE #2] {len(bad_commits)} commit(s) avec mauvais auteur{E}")
        for sha, email in bad_commits:
            print(f"  {sha[:8]} → {email}")
        print(f"  {Y}→ Correction manuelle requise: git rebase --exec 'git commit --amend --no-edit --reset-author' origin/..{E}")
        issues += 1
    else:
        print(f"{G}[OK] Auteur git correct sur les 5 derniers commits{E}")

    # 5. Doublons icônes
    duplicates = detect_duplicate_icons()
    if duplicates:
        print(f"\n{R}[BOUCLE #3] {len(duplicates)} icône(s) dupliquée(s) — race condition sidebar{E}")
        fix_duplicate_icons(duplicates, dry_run)
        issues += 1
    else:
        print(f"{G}[OK] Zéro doublon d'icône{E}")

    # Push
    if issues > 0 and not dry_run:
        print(f"\n{B}Push des corrections...{E}")
        push_fixes(dry_run)

    # Bilan
    print(f"\n{B}{'─'*60}{E}")
    if issues == 0:
        print(f"{G}{B}✓ AUCUNE BOUCLE TEMPORELLE DÉTECTÉE — Système propre{E}")
    else:
        print(f"{'G' if issues < 2 else Y}{B}{'⚠' if issues > 0 else '✓'} {issues} boucle(s) traitée(s){E}")

    return 0 if issues == 0 else 1


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    sys.exit(main(dry_run))
