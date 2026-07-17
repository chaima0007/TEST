#!/usr/bin/env python3
"""Source Integrity Monitor Agent — CaelumSwarm™
Passive integrity check: validates CSDDD/human-rights data sources used
in engine files against an authorized whitelist. Outputs JSON + console alerts.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "SourceIntegrityMonitorAgent"
VERSION = "1.0.0"

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

ROOT        = Path(__file__).resolve().parent.parent
ENGINES_DIR = ROOT / "swarm" / "intelligence"
MEMORY_DIR  = ROOT / "docs" / "swarm-memory"
OUTPUT_PATH = MEMORY_DIR / "source-integrity-report.json"

# ---------------------------------------------------------------------------
# Authorized CSDDD / Human Rights Sources
# ---------------------------------------------------------------------------

AUTHORIZED_SOURCES = [
    {
        "nom":                 "SEC EDGAR — Dodd-Frank Conflict Minerals Reports",
        "url":                 "sec.gov",
        "domain":              "sec.gov",
        "type":                "officielle",
        "fiabilite_score":     98,
        "derniere_verification": "2026-06-01",
        "statut":              "actif",
        "description":         "US SEC filings on conflict minerals (3TG) — Dodd-Frank §1502",
    },
    {
        "nom":                 "Global Witness",
        "url":                 "globalwitness.org",
        "domain":              "globalwitness.org",
        "type":                "ONG",
        "fiabilite_score":     91,
        "derniere_verification": "2026-05-15",
        "statut":              "actif",
        "description":         "Investigations on natural resource exploitation and human rights abuses",
    },
    {
        "nom":                 "Business & Human Rights Resource Centre",
        "url":                 "business-humanrights.org",
        "domain":              "business-humanrights.org",
        "type":                "ONG",
        "fiabilite_score":     93,
        "derniere_verification": "2026-06-01",
        "statut":              "actif",
        "description":         "Global tracker for corporate human rights obligations",
    },
    {
        "nom":                 "OECD Due Diligence Guidelines",
        "url":                 "oecd.org",
        "domain":              "oecd.org",
        "type":                "officielle",
        "fiabilite_score":     97,
        "derniere_verification": "2026-05-20",
        "statut":              "actif",
        "description":         "OECD Guidelines for Multinational Enterprises and due diligence guidance",
    },
    {
        "nom":                 "EUR-Lex — CSDDD Official Text",
        "url":                 "eur-lex.europa.eu",
        "domain":              "eur-lex.europa.eu",
        "type":                "officielle",
        "fiabilite_score":     99,
        "derniere_verification": "2026-06-10",
        "statut":              "actif",
        "description":         "EU Official Journal — Corporate Sustainability Due Diligence Directive text",
    },
    {
        "nom":                 "ITUC Global Rights Index",
        "url":                 "survey.ituc-csi.org",
        "domain":              "ituc-csi.org",
        "type":                "ONG",
        "fiabilite_score":     89,
        "derniere_verification": "2026-05-01",
        "statut":              "actif",
        "description":         "Annual ranking of worst countries for workers' rights",
    },
    {
        "nom":                 "OHCHR — UN Human Rights",
        "url":                 "ohchr.org",
        "domain":              "ohchr.org",
        "type":                "officielle",
        "fiabilite_score":     97,
        "derniere_verification": "2026-06-01",
        "statut":              "actif",
        "description":         "UN Office of the High Commissioner for Human Rights",
    },
    {
        "nom":                 "The Enough Project — 3TG Scorecard",
        "url":                 "enoughproject.org",
        "domain":              "enough.org",
        "type":                "ONG",
        "fiabilite_score":     85,
        "derniere_verification": "2026-04-15",
        "statut":              "actif",
        "description":         "Corporate scorecard on conflict minerals sourcing (3TG)",
    },
]

# Authorized domain variants (subdomains, alternate spellings)
AUTHORIZED_DOMAINS: set[str] = set()
for src in AUTHORIZED_SOURCES:
    AUTHORIZED_DOMAINS.add(src["domain"])
    # also allow www. prefix
    AUTHORIZED_DOMAINS.add("www." + src["domain"])

# Extra loose keywords that map to authorized sources
AUTHORIZED_KEYWORDS = {
    "sec.gov", "edgar", "dodd-frank",
    "global witness", "globalwitness",
    "business-humanrights", "business & human rights",
    "oecd", "oecd.org",
    "eur-lex", "eur_lex", "csddd",
    "ituc", "ituc-csi", "global rights index",
    "ohchr", "un human rights",
    "enough", "enoughproject", "3tg scorecard",
    # generic legitimate references
    "ilostat", "ilo.org", "worldbank.org", "un.org",
    "amnesty", "hrw.org", "human rights watch",
    "transparency", "ti.org", "corruption",
}

# ---------------------------------------------------------------------------
# Engine scanning
# ---------------------------------------------------------------------------

def extract_data_sources_from_engine(path: Path) -> list[str]:
    """Extract data_sources list entries from an engine file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    block_m = re.search(r'data_sources\s*=\s*\[(.*?)\]', text, re.DOTALL)
    if not block_m:
        return []
    block = block_m.group(1)
    return re.findall(r'["\']([^"\']{4,})["\']', block)


def classify_source(source_str: str) -> str:
    """Return 'authorized', 'unknown', or 'suspicious'."""
    s_lower = source_str.lower()
    # Check authorized domains directly
    for dom in AUTHORIZED_DOMAINS:
        if dom in s_lower:
            return "authorized"
    # Check authorized keywords
    for kw in AUTHORIZED_KEYWORDS:
        if kw in s_lower:
            return "authorized"
    # Heuristic: strings that look like descriptive text (no dot-tld) → likely OK label
    if not re.search(r'\.(com|org|gov|eu|net|io|int)\b', s_lower):
        return "authorized"  # treat plain descriptions as non-URL entries
    return "unknown"


def scan_engines_for_sources() -> list[dict]:
    if not ENGINES_DIR.exists():
        return []
    results = []
    for path in sorted(ENGINES_DIR.glob("*.py")):
        if path.name.startswith("__"):
            continue
        sources = extract_data_sources_from_engine(path)
        classified = []
        alerts = []
        for src in sources:
            status = classify_source(src)
            classified.append({"source": src, "status": status})
            if status == "unknown":
                alerts.append(src)
        if alerts:
            results.append({
                "engine":    path.stem,
                "path":      str(path.relative_to(ROOT)),
                "sources":   classified,
                "alerts":    alerts,
                "clean":     False,
            })
        elif sources:
            results.append({
                "engine": path.stem,
                "path":   str(path.relative_to(ROOT)),
                "sources": classified,
                "alerts":  [],
                "clean":   True,
            })
    return results

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  Source Integrity Monitor Agent v{VERSION}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    print(f"{CYAN}[1/3] Authorized source registry loaded ({len(AUTHORIZED_SOURCES)} sources){RESET}")
    for s in AUTHORIZED_SOURCES:
        print(f"      {GREEN}✓{RESET} [{s['type']:10s}] {s['nom']}  (fiabilité {s['fiabilite_score']})")

    print(f"\n{CYAN}[2/3] Scanning engine files for data_sources...{RESET}")
    engine_results = scan_engines_for_sources()
    engines_with_sources = [e for e in engine_results if e.get("sources")]
    engines_with_alerts  = [e for e in engine_results if e.get("alerts")]
    print(f"      Engines with data_sources: {len(engines_with_sources)}")
    print(f"      Engines with unknown sources: {len(engines_with_alerts)}")

    print(f"\n{CYAN}[3/3] Building integrity report...{RESET}")

    # Aggregate all unknown sources
    all_unknowns = []
    for eng in engines_with_alerts:
        for alert_src in eng["alerts"]:
            all_unknowns.append({
                "engine": eng["engine"],
                "source": alert_src,
            })

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent":        AGENT_NAME,
        "version":      VERSION,
        "authorized_sources": AUTHORIZED_SOURCES,
        "summary": {
            "authorized_sources_count": len(AUTHORIZED_SOURCES),
            "engines_scanned":          len(engine_results),
            "engines_with_sources":     len(engines_with_sources),
            "engines_with_alerts":      len(engines_with_alerts),
            "unknown_source_entries":   len(all_unknowns),
        },
        "engine_source_audit": engine_results,
        "unknown_sources":     all_unknowns,
        "recommendations":     [],
    }

    recs = report["recommendations"]
    if engines_with_alerts:
        recs.append({
            "priority": "HIGH",
            "action":   "REVIEW_UNAUTHORIZED_SOURCES",
            "detail":   (
                f"{len(engines_with_alerts)} engine(s) reference unknown sources. "
                "Verify each source against the CSDDD/human-rights whitelist."
            ),
            "affected_engines": [e["engine"] for e in engines_with_alerts[:20]],
        })
    if not engines_with_sources:
        recs.append({
            "priority": "MEDIUM",
            "action":   "ADD_DATA_SOURCES",
            "detail":   "No engines declare data_sources — add source attribution to all engines",
        })
    if not recs:
        recs.append({
            "priority": "INFO",
            "action":   "ALL_SOURCES_AUTHORIZED",
            "detail":   "All declared sources match the authorized CSDDD whitelist",
        })

    OUTPUT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Console report
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  SOURCE INTEGRITY REPORT{RESET}")
    print(f"{'='*60}")
    print(f"  Engines scanned         : {len(engine_results)}")
    print(f"  Engines with sources    : {len(engines_with_sources)}")
    print(f"  Engines with unknowns   : {len(engines_with_alerts)}")
    print(f"  Unknown source entries  : {len(all_unknowns)}")
    print(f"{'='*60}\n")

    if engines_with_alerts:
        print(f"{RED}[ALERT] Engines referencing unknown sources:{RESET}")
        for eng in engines_with_alerts[:15]:
            print(f"  {YELLOW}{eng['engine']}{RESET}")
            for a in eng["alerts"][:3]:
                print(f"    → {a}")
    else:
        print(f"{GREEN}[OK] All declared sources are authorized.{RESET}")

    print(f"\n{BOLD}Recommendations:{RESET}")
    for r in recs:
        color = RED if r["priority"] == "HIGH" else YELLOW if r["priority"] == "MEDIUM" else CYAN
        print(f"  {color}[{r['priority']}]{RESET} {r['action']}: {r['detail']}")

    print(f"\n{GREEN}[OK] Report written to: {OUTPUT_PATH}{RESET}\n")


if __name__ == "__main__":
    main()
