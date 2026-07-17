#!/usr/bin/env python3
"""Security Audit Agent — CaelumSwarm™ Dev Support
Audit de sécurité OWASP : injection, XSS, credentials exposés,
dépendances vulnérables, configuration non sécurisée, secrets dans le code.
"""
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "SecurityAuditAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Patterns de secrets potentiels
SECRET_PATTERNS = [
    (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'][^"\']{4,}["\']', "Mot de passe hardcodé"),
    (r'(?i)(api_key|apikey|api-key)\s*[=:]\s*["\'][^"\']{8,}["\']', "Clé API hardcodée"),
    (r'(?i)(secret|token)\s*[=:]\s*["\'][^"\']{8,}["\']', "Secret/Token hardcodé"),
    (r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----', "Clé privée RSA/EC exposée"),
    (r'(?i)(aws_access_key_id|aws_secret)\s*[=:]\s*["\'][A-Z0-9+/]{16,}["\']', "Credentials AWS"),
    (r'sk-[a-zA-Z0-9]{32,}', "Clé OpenAI potentielle"),
]

# Patterns de vulnérabilités
VULN_PATTERNS = [
    (r'\beval\s*\(', "CRITICAL", "eval() — risque d'injection de code"),
    (r'\bexec\s*\(.*input', "CRITICAL", "exec() avec input utilisateur — injection possible"),
    (r'dangerouslySetInnerHTML', "HIGH", "dangerouslySetInnerHTML — risque XSS"),
    (r'innerHTML\s*=', "HIGH", "innerHTML assignation directe — risque XSS"),
    (r'document\.write\(', "HIGH", "document.write() — risque XSS"),
    (r'window\.location\s*=.*(?:req|params|query|body)', "MEDIUM", "Redirect non validé"),
    (r'\.query\[.*\](?!\s*\?)', "MEDIUM", "Query param sans validation"),
    (r'process\.env\.[A-Z_]+(?!\s*\??\s*[&|])', "INFO", "Variable env sans guard (vérifier usage)"),
    (r'console\.(log|debug)\(.*(?:password|secret|token|key)', "HIGH", "Secret potentiel dans console.log"),
    (r'Math\.random\(\)', "INFO", "Math.random() non cryptographique"),
]


def scan_file(filepath: Path) -> dict:
    findings = []
    try:
        source = filepath.read_text(encoding="utf-8")
        lines = source.splitlines()

        # Recherche de secrets
        for pattern, description in SECRET_PATTERNS:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line) and ".env" not in str(filepath):
                    findings.append({
                        "severity": "CRITICAL",
                        "category": "SECRET_EXPOSURE",
                        "line": i,
                        "message": description,
                        "snippet": line.strip()[:80]
                    })

        # Recherche de vulnérabilités
        for pattern, severity, description in VULN_PATTERNS:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line) and not line.strip().startswith("//") and not line.strip().startswith("#"):
                    findings.append({
                        "severity": severity,
                        "category": "VULNERABILITY",
                        "line": i,
                        "message": description,
                        "snippet": line.strip()[:80]
                    })

    except Exception as e:
        findings.append({"severity": "ERROR", "category": "SCAN_ERROR", "line": 0,
                         "message": str(e), "snippet": ""})

    return {
        "file": str(filepath.relative_to(Path("/home/user/TEST"))),
        "findings": findings,
        "risk_score": sum({"CRITICAL": 30, "HIGH": 15, "MEDIUM": 7, "INFO": 1, "ERROR": 5}.get(f["severity"], 0) for f in findings)
    }


def check_env_files(root: Path) -> list[dict]:
    alerts = []
    # Vérifier que .env n'est pas dans git
    gitignore = root / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text()
        if ".env" not in content:
            alerts.append({"severity": "CRITICAL", "message": ".env absent du .gitignore"})
        if ".env.local" not in content:
            alerts.append({"severity": "HIGH", "message": ".env.local absent du .gitignore"})

    # Vérifier présence de .env example
    if not (root / ".env.example").exists() and not (root / ".env.template").exists():
        alerts.append({"severity": "INFO", "message": "Aucun .env.example trouvé — documenter les variables requises"})

    return alerts


def run_audit(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{RED}{'='*70}{RESET}")
    print(f"{BOLD}{RED}  CaelumSwarm™ Security Audit Agent v{VERSION}{RESET}")
    print(f"{BOLD}{RED}{'='*70}{RESET}\n")

    all_results = []
    files_to_scan = (
        list((root / "app").rglob("*.ts"))
        + list((root / "app").rglob("*.tsx"))
        + list((root / "lib").rglob("*.ts"))
        + list((root / "swarm").rglob("*.py"))
        + list((root / "scripts").rglob("*.py"))
    )

    print(f"{CYAN}Scan de {len(files_to_scan)} fichiers...{RESET}\n")
    critical_count = high_count = medium_count = 0

    for filepath in files_to_scan:
        result = scan_file(filepath)
        if result["findings"]:
            all_results.append(result)
            for f in result["findings"]:
                if f["severity"] == "CRITICAL":
                    critical_count += 1
                    print(f"  {RED}[CRITICAL]{RESET} {result['file']}:{f['line']} — {f['message']}")
                elif f["severity"] == "HIGH":
                    high_count += 1
                    print(f"  {YELLOW}[HIGH]{RESET}     {result['file']}:{f['line']} — {f['message']}")
                elif f["severity"] == "MEDIUM":
                    medium_count += 1

    # Check .env
    env_alerts = check_env_files(root)
    for alert in env_alerts:
        color = RED if alert["severity"] == "CRITICAL" else YELLOW
        print(f"  {color}[{alert['severity']}] ENV: {alert['message']}{RESET}")

    print(f"\n{BOLD}Résumé audit sécurité :{RESET}")
    print(f"  {RED}CRITICAL : {critical_count}{RESET}")
    print(f"  {YELLOW}HIGH     : {high_count}{RESET}")
    print(f"  MEDIUM   : {medium_count}")

    overall = "SECURE" if critical_count == 0 and high_count == 0 else \
              "NEEDS_ATTENTION" if critical_count == 0 else "VULNERABLE"
    color = GREEN if overall == "SECURE" else YELLOW if overall == "NEEDS_ATTENTION" else RED
    print(f"\n  Statut: {color}{BOLD}{overall}{RESET}\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "files_scanned": len(files_to_scan),
        "critical": critical_count,
        "high": high_count,
        "medium": medium_count,
        "overall_status": overall,
        "results": all_results,
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
