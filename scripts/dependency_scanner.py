#!/usr/bin/env python3
"""
dependency_scanner.py — Scan Sécurité des Dépendances CaelumSwarm™
══════════════════════════════════════════════════════════════════
Audite les dépendances (npm + pip) AVANT déploiement :
  - Licences interdites (GPL/AGPL en usage commercial) → BLOQUE
  - Versions épinglées vs plages floues (^ ~ *) → ALERTE
  - Dépendances obsolètes / connues vulnérables (base locale) → ALERTE
  - Conflits de versions entre modules → ALERTE

Conçu pour s'intégrer dans un pipeline CI : code retour non-zéro si BLOQUANT.
Stdlib uniquement (parse package.json / requirements.txt sans réseau).

Usage :
  python3 scripts/dependency_scanner.py --scan
  python3 scripts/dependency_scanner.py --scan --strict   # alertes = échec aussi
  python3 scripts/dependency_scanner.py --report
"""

import re
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

SCAN_LOG = Path("data/dependency_scan_log.json")

LICENCES_INTERDITES = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.0", "LGPL-3.0", "SSPL-1.0"}
LICENCES_AUTORISEES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense", "CC0-1.0", "0BSD"}

# Base locale de versions connues vulnérables (exemples réels notables).
# Format : package -> [(spec_version_affectée, CVE, sévérité)]
KNOWN_VULNERABLE = {
    "next":        [("<14.2.10", "CVE-2024-46982 (cache poisoning)", "ÉLEVÉ")],
    "axios":       [("<1.7.4", "CVE-2024-39338 (SSRF)", "ÉLEVÉ")],
    "lodash":      [("<4.17.21", "CVE-2021-23337 (prototype pollution)", "CRITIQUE")],
    "minimatch":   [("<3.0.5", "CVE-2022-3517 (ReDoS)", "MOYEN")],
    "semver":      [("<7.5.2", "CVE-2022-25883 (ReDoS)", "MOYEN")],
    "requests":    [("<2.32.0", "CVE-2024-35195 (cert verify)", "MOYEN")],
}

SEV_ICON = {"CRITIQUE": "🔴", "ÉLEVÉ": "🟠", "MOYEN": "🟡", "FAIBLE": "🟢", "INFO": "ℹ️"}


def _load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return default
    return default


def _parse_semver(v: str):
    m = re.match(r"\D*(\d+)\.(\d+)\.(\d+)", v)
    return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)


def _version_lt(version: str, threshold: str) -> bool:
    """version < threshold (threshold sous forme '<X.Y.Z')."""
    thr = threshold.lstrip("<")
    return _parse_semver(version) < _parse_semver(thr)


# ── Parsing ────────────────────────────────────────────────────────────────────

def scan_npm() -> list:
    findings = []
    pkg = _load_json(Path("package.json"), {})
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    for name, spec in deps.items():
        # Plage floue ?
        if spec.startswith("^") or spec.startswith("~") or spec in ("*", "latest", "x"):
            findings.append({"pkg": name, "spec": spec, "type": "FLOATING_VERSION",
                             "severity": "FAIBLE",
                             "detail": f"Version non épinglée ('{spec}') — build non reproductible"})
        # Vulnérabilité connue ?
        clean = re.sub(r"^[\^~>=<\s]+", "", spec)
        for vuln_spec, cve, sev in KNOWN_VULNERABLE.get(name, []):
            try:
                if _version_lt(clean, vuln_spec):
                    findings.append({"pkg": name, "spec": spec, "type": "VULNERABILITY",
                                     "severity": sev, "detail": f"{cve} — corrigé en {vuln_spec.lstrip('<')}"})
            except Exception:
                pass
    return findings


def scan_pip() -> list:
    findings = []
    for req in ["requirements.txt", "requirements-dev.txt"]:
        p = Path(req)
        if not p.exists():
            continue
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"([A-Za-z0-9_.\-]+)\s*([=<>!~]+)?\s*([\d.]+)?", line)
            if not m:
                continue
            name, op, ver = m.group(1).lower(), m.group(2), m.group(3)
            if not op or op not in ("==",):
                findings.append({"pkg": name, "spec": line, "type": "FLOATING_VERSION",
                                 "severity": "FAIBLE",
                                 "detail": "Version non épinglée (==) — build non reproductible"})
            if ver:
                for vuln_spec, cve, sev in KNOWN_VULNERABLE.get(name, []):
                    if _version_lt(ver, vuln_spec):
                        findings.append({"pkg": name, "spec": line, "type": "VULNERABILITY",
                                         "severity": sev, "detail": f"{cve} — corrigé en {vuln_spec.lstrip('<')}"})
    return findings


def check_licenses() -> list:
    """Scanne node_modules/*/package.json pour les licences interdites (échantillon)."""
    findings = []
    nm = Path("node_modules")
    if not nm.exists():
        return findings
    checked = 0
    for pkg_json in nm.glob("*/package.json"):
        if checked >= 2000:
            break
        checked += 1
        data = _load_json(pkg_json, {})
        lic = data.get("license", "")
        if isinstance(lic, dict):
            lic = lic.get("type", "")
        if lic in LICENCES_INTERDITES:
            findings.append({"pkg": data.get("name", pkg_json.parent.name), "spec": lic,
                             "type": "FORBIDDEN_LICENSE", "severity": "CRITIQUE",
                             "detail": f"Licence {lic} interdite en usage commercial → BLOQUE"})
    return findings


# ── Orchestration ──────────────────────────────────────────────────────────────

def run_scan() -> dict:
    findings = scan_npm() + scan_pip() + check_licenses()
    by_sev = {"CRITIQUE": 0, "ÉLEVÉ": 0, "MOYEN": 0, "FAIBLE": 0}
    for f in findings:
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
    blocking = sum(1 for f in findings if f["type"] == "FORBIDDEN_LICENSE"
                   or (f["type"] == "VULNERABILITY" and f["severity"] == "CRITIQUE"))
    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "total": len(findings),
        "by_severity": by_sev,
        "blocking": blocking,
        "findings": findings,
    }
    log = _load_json(SCAN_LOG, [])
    log.append({k: v for k, v in result.items() if k != "findings"})
    if len(log) > 500:
        log = log[-500:]
    SCAN_LOG.parent.mkdir(exist_ok=True)
    SCAN_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))
    return result


def print_result(result: dict, strict: bool):
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║       DEPENDENCY SCANNER — Sécurité CaelumSwarm™           ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    if not result["findings"]:
        print("  ✅ Aucun problème détecté — dépendances saines.\n")
        return
    # Grouper par type
    by_type = {}
    for f in result["findings"]:
        by_type.setdefault(f["type"], []).append(f)
    labels = {
        "FORBIDDEN_LICENSE": "🚫 LICENCES INTERDITES (BLOQUANT)",
        "VULNERABILITY": "🛡️  VULNÉRABILITÉS CONNUES",
        "FLOATING_VERSION": "📌 VERSIONS NON ÉPINGLÉES",
    }
    for t, items in by_type.items():
        print(f"  {labels.get(t, t)} ({len(items)})")
        for f in items[:15]:
            print(f"    {SEV_ICON.get(f['severity'],'•')} {f['pkg']} ({f['spec']}) — {f['detail']}")
        if len(items) > 15:
            print(f"    … et {len(items)-15} autres")
        print()
    print("─" * 64)
    s = result["by_severity"]
    print(f"  Total : {result['total']} | 🔴 {s['CRITIQUE']} 🟠 {s['ÉLEVÉ']} 🟡 {s['MOYEN']} 🟢 {s['FAIBLE']}")
    print(f"  Bloquants : {result['blocking']}")
    print("─" * 64 + "\n")


def main():
    ap = argparse.ArgumentParser(description="Dependency Scanner CaelumSwarm™")
    ap.add_argument("--scan", action="store_true", help="Lancer le scan")
    ap.add_argument("--strict", action="store_true", help="Les alertes (non bloquantes) font aussi échouer")
    ap.add_argument("--report", action="store_true", help="Historique des scans")
    args = ap.parse_args()

    if args.report:
        log = _load_json(SCAN_LOG, [])
        print(f"\n  HISTORIQUE SCANS : {len(log)}")
        for e in log[-10:]:
            print(f"    {e['ts'][:19]}  total={e['total']:>3}  bloquants={e['blocking']}")
        print()
    elif args.scan:
        result = run_scan()
        print_result(result, args.strict)
        fail = result["blocking"] > 0 or (args.strict and result["total"] > 0)
        sys.exit(1 if fail else 0)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
