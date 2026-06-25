#!/usr/bin/env python3
"""Task Deduplication Agent — CaelumSwarm™
Anti-repetition agent: reads catalog.json (or generates it), computes Jaccard
similarity between agents on function/variable names, alerts if >70%, and
recommends merge or specialization.
"""
import re
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "TaskDeduplicationAgent"
VERSION = "1.0.0"

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

ROOT        = Path(__file__).resolve().parent.parent
MEMORY_DIR  = ROOT / "docs" / "swarm-memory"
CATALOG_PATH = MEMORY_DIR / "catalog.json"
OUTPUT_PATH  = MEMORY_DIR / "deduplication-report.json"
SCRIPTS_DIR  = ROOT / "scripts"

# ---------------------------------------------------------------------------
# Catalog loading (or generation via coordinator)
# ---------------------------------------------------------------------------

def load_or_generate_catalog() -> dict:
    if CATALOG_PATH.exists():
        text = CATALOG_PATH.read_text(encoding="utf-8")
        return json.loads(text)
    # Try to generate by importing coordinator logic inline
    print(f"{YELLOW}[WARN] catalog.json not found — running coordinator first...{RESET}")
    coord_path = SCRIPTS_DIR / "swarm-memory-coordinator-agent.py"
    if coord_path.exists():
        result = subprocess.run(
            [sys.executable, str(coord_path)],
            capture_output=True, text=True, timeout=120,
        )
        if CATALOG_PATH.exists():
            print(f"{GREEN}[OK] Catalog generated.{RESET}")
            return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        else:
            print(f"{RED}[ERR] Coordinator failed: {result.stderr[:300]}{RESET}")
    raise FileNotFoundError(f"Cannot find or generate {CATALOG_PATH}")

# ---------------------------------------------------------------------------
# Token extraction from source files
# ---------------------------------------------------------------------------

def extract_tokens_from_file(path: Path) -> set:
    """Return set of meaningful identifier tokens in a Python file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return set()
    # Extract function names
    funcs = set(re.findall(r'^def\s+(\w+)', text, re.MULTILINE))
    # Extract UPPER_CASE constants
    consts = set(re.findall(r'^([A-Z][A-Z0-9_]{2,})\s*=', text, re.MULTILINE))
    # Extract class names
    classes = set(re.findall(r'^class\s+(\w+)', text, re.MULTILINE))
    # Extract variable names from assignments (lower/snake_case)
    vars_ = set(re.findall(r'^([a-z][a-z0-9_]{3,})\s*=', text, re.MULTILINE))
    all_tokens = funcs | consts | classes | vars_
    # Remove very common tokens
    STOPWORDS = {
        "main", "self", "true", "false", "none", "pass", "return",
        "print", "open", "read", "write", "path", "name", "text",
        "data", "result", "results", "output", "error", "value", "values",
        "args", "kwargs", "items", "keys", "info", "json", "file",
    }
    return all_tokens - STOPWORDS


def jaccard(set_a: set, set_b: set) -> float:
    if not set_a and not set_b:
        return 1.0
    union = set_a | set_b
    if not union:
        return 0.0
    return len(set_a & set_b) / len(union)

# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def build_similarity_matrix(catalog: dict) -> tuple[list, list]:
    """
    Returns (matrix_rows, alerts)
    matrix_rows: list of {agent1, agent2, similarity, shared_tokens, alert}
    alerts:      filtered subset where similarity > 0.70
    """
    scripts = catalog.get("scripts", [])
    # Load tokens for each script
    token_cache: dict[str, set] = {}
    for s in scripts:
        rel = s.get("path", "")
        p = ROOT / rel if rel else None
        if p and p.exists():
            token_cache[s["filename"]] = extract_tokens_from_file(p)
        else:
            token_cache[s.get("filename", "?")] = set()

    matrix_rows = []
    alerts = []

    filenames = [s["filename"] for s in scripts]
    for i, s1 in enumerate(scripts):
        f1 = s1["filename"]
        t1 = token_cache.get(f1, set())
        for s2 in scripts[i + 1:]:
            f2 = s2["filename"]
            t2 = token_cache.get(f2, set())
            sim = round(jaccard(t1, t2), 4)
            shared = sorted(t1 & t2)[:20]  # cap for readability
            row = {
                "agent1":        f1,
                "agent2":        f2,
                "similarity":    sim,
                "shared_tokens": shared,
                "alert":         sim > 0.70,
            }
            matrix_rows.append(row)
            if sim > 0.70:
                rec = "MERGE" if sim > 0.90 else "SPECIALIZE"
                alerts.append({
                    **row,
                    "recommendation": rec,
                    "detail": (
                        f"Similarity {sim:.0%} — consider merging {f1} and {f2}"
                        if rec == "MERGE"
                        else f"Similarity {sim:.0%} — clearly separate responsibilities"
                    ),
                })

    return matrix_rows, alerts


def main():
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  Task Deduplication Agent v{VERSION}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    print(f"{CYAN}[1/3] Loading catalog...{RESET}")
    catalog = load_or_generate_catalog()
    n_scripts = len(catalog.get("scripts", []))
    print(f"      Catalog loaded — {n_scripts} agents")

    print(f"{CYAN}[2/3] Computing Jaccard similarity matrix ({n_scripts} agents)...{RESET}")
    print(f"      (This may take a moment for large swarms)")
    matrix, alerts = build_similarity_matrix(catalog)
    print(f"      Pairs evaluated: {len(matrix)}")
    print(f"      High-similarity pairs (>70%): {len(alerts)}")

    print(f"{CYAN}[3/3] Building report...{RESET}")

    # Top duplicates sorted by similarity desc
    top_dupes = sorted(
        [r for r in matrix if r["similarity"] > 0.40],
        key=lambda x: x["similarity"],
        reverse=True,
    )[:50]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent":        AGENT_NAME,
        "version":      VERSION,
        "summary": {
            "total_agents_evaluated": n_scripts,
            "total_pairs":            len(matrix),
            "high_similarity_alerts": len(alerts),
            "threshold":              0.70,
        },
        "alerts":            alerts,
        "top_similar_pairs": top_dupes,
        "recommendations":   [],
    }

    recs = report["recommendations"]
    merge_count = sum(1 for a in alerts if a.get("recommendation") == "MERGE")
    spec_count  = sum(1 for a in alerts if a.get("recommendation") == "SPECIALIZE")
    if merge_count:
        recs.append({
            "priority": "HIGH",
            "action":   "MERGE_AGENTS",
            "detail":   f"{merge_count} agent pair(s) with >90% similarity — strong merge candidate",
        })
    if spec_count:
        recs.append({
            "priority": "MEDIUM",
            "action":   "CLARIFY_RESPONSIBILITIES",
            "detail":   f"{spec_count} agent pair(s) with 70-90% similarity — refine domain boundaries",
        })
    if not recs:
        recs.append({
            "priority": "INFO",
            "action":   "NO_ACTION",
            "detail":   "No significant duplication detected",
        })

    OUTPUT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Console output
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  DEDUPLICATION REPORT{RESET}")
    print(f"{'='*60}")
    print(f"  Agents evaluated  : {n_scripts}")
    print(f"  Pairs analyzed    : {len(matrix)}")
    print(f"  Alerts (>70% sim) : {len(alerts)}")
    print(f"{'='*60}\n")

    if alerts:
        print(f"{RED}[ALERTS] High-similarity pairs:{RESET}")
        for a in alerts[:20]:
            color = RED if a["similarity"] > 0.90 else YELLOW
            print(
                f"  {color}[{a['recommendation']}]{RESET} "
                f"{a['agent1']} ↔ {a['agent2']}  sim={a['similarity']:.0%}"
            )
            print(f"    → {a['detail']}")
    else:
        print(f"{GREEN}[OK] No significant duplicates found.{RESET}")

    print(f"\n{BOLD}Recommendations:{RESET}")
    for r in recs:
        color = RED if r["priority"] == "HIGH" else YELLOW if r["priority"] == "MEDIUM" else CYAN
        print(f"  {color}[{r['priority']}]{RESET} {r['action']}: {r['detail']}")

    print(f"\n{GREEN}[OK] Report written to: {OUTPUT_PATH}{RESET}\n")


if __name__ == "__main__":
    main()
