#!/usr/bin/env python3
"""Swarm Memory Coordinator Agent — CaelumSwarm™
Central memory agent: reads all engines and scripts, detects duplicates,
generates docs/swarm-memory/catalog.json, and outputs a health report.
"""
import re
import json
import os
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "SwarmMemoryCoordinatorAgent"
VERSION = "1.0.0"

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
ENGINES_DIR = ROOT / "swarm" / "intelligence"
SCRIPTS_DIR = ROOT / "scripts"
MEMORY_DIR  = ROOT / "docs" / "swarm-memory"
CATALOG_OUT = MEMORY_DIR / "catalog.json"

# ---------------------------------------------------------------------------
# Engine parsing
# ---------------------------------------------------------------------------

def parse_engine_file(path: Path) -> dict:
    """Extract metadata from a CaelumSwarm engine .py file."""
    text = path.read_text(encoding="utf-8", errors="replace")

    def _get(pattern, default=None):
        m = re.search(pattern, text, re.MULTILINE)
        return m.group(1).strip() if m else default

    # Module-level constants (new-style engines)
    prefix       = _get(r'^PREFIX\s*=\s*["\']?([A-Z0-9_]+)["\']?', "")
    accent_color = _get(r'^ACCENT_COLOR\s*=\s*["\']([^"\']+)["\']', "")
    wave_raw     = _get(r'^WAVE\s*=\s*(\d+)', "")
    domain_const = _get(r'^DOMAIN\s*=\s*["\']([^"\']+)["\']', "")

    # Fallback: dataclass field domain
    if not domain_const:
        domain_const = _get(r'domain:\s*str\s*=\s*["\']([^"\']+)["\']', "")

    # Engine name from filename
    engine_name = path.stem

    # avg_composite — look for the assert or a plain assignment
    avg_composite = None
    m_assert = re.search(
        r'assert\s+60\.00\s*<=\s*avg\s*<=\s*63\.00.*avg_composite\s+([0-9.]+)',
        text,
    )
    if not m_assert:
        m_assert = re.search(
            r'avg_composite\s*=\s*([0-9]+\.[0-9]+)',
            text,
        )
    if m_assert:
        try:
            avg_composite = float(m_assert.group(1))
        except (ValueError, IndexError):
            pass

    # Entities: collect all entity_id string literals (first argument to entity constructors)
    entities = re.findall(
        r'entity_id\s*=\s*["\']([^"\']+)["\']',
        text,
    )
    if not entities:
        # Fallback: positional first string in dataclass construction
        entities = re.findall(
            r'[A-Z][A-Za-z]+Entity\s*\(\s*["\']([^"\']+)["\']',
            text,
        )

    # data_sources list
    sources_block = re.search(
        r'data_sources\s*=\s*\[(.*?)\]',
        text,
        re.DOTALL,
    )
    data_sources = []
    if sources_block:
        data_sources = re.findall(r'["\']([^"\']{5,})["\']', sources_block.group(1))

    return {
        "engine_name":   engine_name,
        "domain":        domain_const or engine_name,
        "prefix":        prefix,
        "accent_color":  accent_color,
        "wave_number":   int(wave_raw) if wave_raw else None,
        "avg_composite": avg_composite,
        "entities":      entities,
        "data_sources":  data_sources,
        "path":          str(path.relative_to(ROOT)),
    }


def scan_engines() -> list:
    if not ENGINES_DIR.exists():
        return []
    files = sorted(ENGINES_DIR.glob("*.py"))
    results = []
    for f in files:
        if f.name.startswith("__"):
            continue
        try:
            results.append(parse_engine_file(f))
        except Exception as e:
            results.append({
                "engine_name": f.stem,
                "parse_error": str(e),
                "path": str(f.relative_to(ROOT)),
            })
    return results

# ---------------------------------------------------------------------------
# Script parsing
# ---------------------------------------------------------------------------

AGENT_TYPE_PATTERNS = [
    (r'monitor|health|latency|uptime|watch',     "monitoring"),
    (r'certif|cisco|google|training',             "certification"),
    (r'infra|docker|kubernetes|k8s|provision',    "infrastructure"),
    (r'audit|compliance|security|integrity',      "support"),
    (r'dedup|coordinator|memory|catalog',         "support"),
]

def infer_agent_type(name: str, description: str) -> str:
    combined = (name + " " + description).lower()
    for pattern, atype in AGENT_TYPE_PATTERNS:
        if re.search(pattern, combined):
            return atype
    return "support"


def parse_script_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")

    # Description from docstring
    doc_m = re.search(r'"""(.*?)"""', text, re.DOTALL)
    description = ""
    if doc_m:
        description = doc_m.group(1).strip().split("\n")[0]

    # AGENT_NAME constant
    name_m = re.search(r'^AGENT_NAME\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
    agent_name = name_m.group(1) if name_m else path.stem

    agent_type = infer_agent_type(path.stem, description)

    return {
        "agent_name":  agent_name,
        "filename":    path.name,
        "type":        agent_type,
        "description": description,
        "path":        str(path.relative_to(ROOT)),
    }


def scan_scripts() -> list:
    results = []
    for f in sorted(SCRIPTS_DIR.glob("*.py")):
        if f.name.startswith("__"):
            continue
        try:
            results.append(parse_script_file(f))
        except Exception as e:
            results.append({
                "filename":    f.name,
                "parse_error": str(e),
                "path":        str(f.relative_to(ROOT)),
            })
    return results

# ---------------------------------------------------------------------------
# Duplicate detection
# ---------------------------------------------------------------------------

def detect_engine_duplicates(engines: list) -> list:
    """Detect engines sharing the same domain string."""
    domain_map: dict[str, list[str]] = {}
    for eng in engines:
        d = eng.get("domain", "")
        if d:
            domain_map.setdefault(d, []).append(eng["engine_name"])
    return [
        {"domain": d, "engines": names}
        for d, names in domain_map.items()
        if len(names) > 1
    ]


def detect_script_duplicates(scripts: list) -> list:
    """Detect scripts with very similar names (shared root token)."""
    token_map: dict[str, list[str]] = {}
    for s in scripts:
        # tokenize filename by dashes
        tokens = frozenset(re.split(r"[-_]", s["filename"].replace(".py", "")))
        key = " ".join(sorted(tokens))
        token_map.setdefault(key, []).append(s["filename"])
    # simple: flag names sharing ≥4 common tokens
    duplicates = []
    filenames = [s["filename"] for s in scripts]
    for i, s1 in enumerate(scripts):
        t1 = set(re.split(r"[-_]", s1["filename"].replace(".py", "")))
        for s2 in scripts[i + 1:]:
            t2 = set(re.split(r"[-_]", s2["filename"].replace(".py", "")))
            overlap = t1 & t2
            if len(overlap) >= 4:
                duplicates.append({
                    "agent1": s1["filename"],
                    "agent2": s2["filename"],
                    "shared_tokens": sorted(overlap),
                })
    return duplicates

# ---------------------------------------------------------------------------
# Health checks
# ---------------------------------------------------------------------------

def check_engine_health(engines: list) -> list:
    alerts = []
    for eng in engines:
        name = eng.get("engine_name", "?")
        avg  = eng.get("avg_composite")
        ents = eng.get("entities", [])

        if avg is not None and not (60.00 <= avg <= 63.00):
            alerts.append({
                "type":    "avg_composite_out_of_range",
                "engine":  name,
                "value":   avg,
                "message": f"avg_composite {avg} outside [60.00, 63.00]",
            })
        if ents and len(ents) != 8:
            alerts.append({
                "type":    "wrong_entity_count",
                "engine":  name,
                "count":   len(ents),
                "message": f"Expected 8 entities, found {len(ents)}",
            })
    return alerts

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  Swarm Memory Coordinator Agent v{VERSION}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

    # Ensure output directory exists
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    # Scan
    print(f"{CYAN}[1/4] Scanning engines in swarm/intelligence/...{RESET}")
    engines = scan_engines()
    print(f"      Found {len(engines)} engine files")

    print(f"{CYAN}[2/4] Scanning scripts/...{RESET}")
    scripts = scan_scripts()
    print(f"      Found {len(scripts)} script files")

    # Duplicate detection
    print(f"{CYAN}[3/4] Detecting duplicates...{RESET}")
    eng_dups  = detect_engine_duplicates(engines)
    scr_dups  = detect_script_duplicates(scripts)

    # Health checks
    print(f"{CYAN}[4/4] Health checks...{RESET}")
    health_alerts = check_engine_health(engines)

    # Summary stats
    engines_with_wave = [e for e in engines if e.get("wave_number")]
    waves_found = sorted(set(e["wave_number"] for e in engines_with_wave))

    # Build catalog
    catalog = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent":        AGENT_NAME,
        "version":      VERSION,
        "summary": {
            "total_engines":        len(engines),
            "total_scripts":        len(scripts),
            "engines_with_wave":    len(engines_with_wave),
            "distinct_waves":       len(waves_found),
            "engine_duplicates":    len(eng_dups),
            "script_duplicates":    len(scr_dups),
            "health_alerts":        len(health_alerts),
        },
        "engines":          engines,
        "scripts":          scripts,
        "duplicates": {
            "engine_domain_conflicts": eng_dups,
            "script_name_conflicts":   scr_dups,
        },
        "health_alerts":    health_alerts,
        "recommendations":  [],
    }

    # Build recommendations
    recs = catalog["recommendations"]
    if eng_dups:
        recs.append({
            "priority": "HIGH",
            "action":   "MERGE_OR_RENAME",
            "detail":   f"{len(eng_dups)} domain collision(s) detected in engines",
            "targets":  [d["domain"] for d in eng_dups],
        })
    if scr_dups:
        recs.append({
            "priority": "MEDIUM",
            "action":   "REVIEW_SCRIPT_OVERLAP",
            "detail":   f"{len(scr_dups)} script pair(s) share ≥4 name tokens",
            "count":    len(scr_dups),
        })
    if health_alerts:
        recs.append({
            "priority": "HIGH",
            "action":   "FIX_ENGINE_PARAMETERS",
            "detail":   f"{len(health_alerts)} engine(s) fail health checks",
        })
    if not recs:
        recs.append({
            "priority": "INFO",
            "action":   "NO_ACTION_REQUIRED",
            "detail":   "All checks passed — swarm is healthy",
        })

    # Write catalog
    CATALOG_OUT.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Report
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  SWARM HEALTH REPORT{RESET}")
    print(f"{'='*60}{RESET}")
    print(f"  Engines scanned   : {len(engines)}")
    print(f"  Scripts scanned   : {len(scripts)}")
    print(f"  Distinct waves    : {len(waves_found)}")
    print(f"  Engine duplicates : {len(eng_dups)}")
    print(f"  Script duplicates : {len(scr_dups)}")
    print(f"  Health alerts     : {len(health_alerts)}")
    print(f"{'='*60}\n")

    if eng_dups:
        print(f"{YELLOW}[WARN] Engine domain duplicates:{RESET}")
        for d in eng_dups[:10]:
            print(f"  domain={d['domain']} → {d['engines']}")
    if scr_dups:
        print(f"{YELLOW}[WARN] Script name overlaps (≥4 shared tokens):{RESET}")
        for d in scr_dups[:10]:
            print(f"  {d['agent1']} ↔ {d['agent2']}  shared={d['shared_tokens']}")
    if health_alerts:
        print(f"{RED}[ALERT] Engine health issues:{RESET}")
        for a in health_alerts[:10]:
            print(f"  {a['engine']}: {a['message']}")

    if not eng_dups and not scr_dups and not health_alerts:
        print(f"{GREEN}[OK] All checks passed — swarm is healthy.{RESET}")

    print(f"\n{GREEN}[OK] Catalog written to: {CATALOG_OUT}{RESET}\n")

    # Cleanup recommendations
    if recs:
        print(f"{BOLD}Cleanup Recommendations:{RESET}")
        for r in recs:
            color = RED if r["priority"] == "HIGH" else YELLOW if r["priority"] == "MEDIUM" else CYAN
            print(f"  {color}[{r['priority']}]{RESET} {r['action']}: {r['detail']}")

    print()
    return catalog


if __name__ == "__main__":
    main()
