#!/usr/bin/env python3
"""CI/CD Pipeline Agent — CaelumSwarm™ Dev Support
Analyse et optimise le pipeline CI/CD : GitHub Actions, Netlify,
vérifie les étapes de build, génère des workflows optimisés.
"""
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "CICDPipelineAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

REQUIRED_CHECKS = [
    "python_engines_validate",
    "typescript_compile",
    "no_console_log",
    "sidebar_no_duplicates",
    "sealResponse_present",
]


def analyze_existing_workflows(root: Path) -> list[dict]:
    workflows_dir = root / ".github" / "workflows"
    if not workflows_dir.exists():
        return []

    workflows = []
    for f in workflows_dir.glob("*.yml"):
        content = f.read_text(encoding="utf-8", errors="ignore")
        has_python = "python" in content.lower()
        has_node = "node" in content.lower() or "npm" in content.lower()
        has_tests = "test" in content.lower() or "pytest" in content.lower()

        workflows.append({
            "file": f.name,
            "has_python": has_python,
            "has_node": has_node,
            "has_tests": has_tests,
        })

    return workflows


def generate_github_actions_workflow() -> str:
    return """# .github/workflows/caelum-ci.yml — CaelumSwarm™ CI Pipeline
# Généré par CICDPipelineAgent v""" + VERSION + """

name: CaelumSwarm™ CI

on:
  push:
    branches: [ claude/swarm-50-agent-architecture-3l6cno ]
  pull_request:
    branches: [ main, master ]

env:
  NODE_VERSION: '20'
  PYTHON_VERSION: '3.11'

jobs:
  # ─── Étape 1 : Validation des engines Python ───────────────
  validate-engines:
    name: Validate Python Engines
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Validate all engines
        run: |
          FAILED=0
          for engine in swarm/intelligence/*_engine.py; do
            echo "Testing $engine..."
            OUTPUT=$(python3 "$engine" 2>&1)
            if [ $? -ne 0 ]; then
              echo "FAILED: $engine"
              echo "$OUTPUT"
              FAILED=1
            else
              AVG=$(echo "$OUTPUT" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('avg_composite', d.get('summary',{}).get('avg_composite_score', 0))")
              echo "OK: $engine — avg_composite=$AVG"
            fi
          done
          exit $FAILED

      - name: Check engine distribution
        run: python3 scripts/wave-consistency-checker-agent.py --json | python3 -c "
          import sys, json
          data = json.loads(sys.stdin.read())
          score = data.get('consistency_score', 100)
          if score < 70:
            print(f'Consistency score too low: {score}/100')
            sys.exit(1)
          print(f'Consistency score: {score}/100 OK')
        "

  # ─── Étape 2 : Build Next.js ───────────────────────────────
  build-nextjs:
    name: Build Next.js
    runs-on: ubuntu-latest
    needs: validate-engines
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Check TypeScript
        run: npx tsc --noEmit

      - name: Check for sidebar duplicates
        run: |
          DUPS=$(grep "^function Icon" components/Sidebar.tsx | awk '{print $2}' | sort | uniq -d)
          if [ -n "$DUPS" ]; then
            echo "DUPLICATE ICONS FOUND: $DUPS"
            exit 1
          fi
          echo "No duplicate icons"

      - name: Build
        run: npm run build
        env:
          SWARM_API_URL: ${{ secrets.SWARM_API_URL || 'https://placeholder.example.com' }}
          NEXTAUTH_SECRET: ${{ secrets.NEXTAUTH_SECRET || 'ci-secret-placeholder-32chars-ok' }}
          NEXTAUTH_URL: ${{ secrets.NEXTAUTH_URL || 'http://localhost:3000' }}

  # ─── Étape 3 : Audit sécurité ─────────────────────────────
  security-audit:
    name: Security Audit
    runs-on: ubuntu-latest
    needs: validate-engines
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Run security audit
        run: |
          python3 scripts/security-audit-agent.py --json > security-report.json
          CRITICAL=$(cat security-report.json | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('critical', 0))")
          if [ "$CRITICAL" -gt "0" ]; then
            echo "Security audit found $CRITICAL critical issues!"
            cat security-report.json | python3 -m json.tool
            exit 1
          fi
          echo "Security audit passed"

      - name: Upload security report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: security-report
          path: security-report.json
"""


def generate_netlify_config() -> str:
    return """# netlify.toml — CaelumSwarm™ Netlify Configuration
# Généré par CICDPipelineAgent v""" + VERSION + """

[build]
  command = "npm run build"
  publish = ".next"

[build.environment]
  NODE_VERSION = "20"
  NEXT_TELEMETRY_DISABLED = "1"

[[plugins]]
  package = "@netlify/plugin-nextjs"

[functions]
  node_bundler = "esbuild"

[[headers]]
  for = "/api/*"
  [headers.values]
    Cache-Control = "public, s-maxage=30, stale-while-revalidate=60"
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/dashboard/*"
  [headers.values]
    Cache-Control = "public, s-maxage=300, stale-while-revalidate=600"

[[redirects]]
  from = "/health"
  to = "/api/health"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
  conditions = {Role = ["admin"]}
"""


def run_agent(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*65}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ CI/CD Pipeline Agent v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*65}{RESET}\n")

    existing = analyze_existing_workflows(root)
    if existing:
        print(f"{BOLD}Workflows existants :{RESET}")
        for w in existing:
            print(f"  {w['file']}: Python={w['has_python']} Node={w['has_node']} Tests={w['has_tests']}")
    else:
        print(f"{YELLOW}Aucun workflow GitHub Actions trouvé{RESET}")

    # Générer les fichiers CI/CD
    github_dir = root / ".github" / "workflows"
    github_dir.mkdir(parents=True, exist_ok=True)

    ci_file = github_dir / "caelum-ci.yml"
    if not ci_file.exists():
        ci_file.write_text(generate_github_actions_workflow(), encoding="utf-8")
        print(f"\n{GREEN}✓ Créé: {ci_file}{RESET}")
    else:
        print(f"\n{YELLOW}⚠ Existe déjà: {ci_file}{RESET}")

    netlify_file = root / "netlify.toml"
    if not netlify_file.exists():
        netlify_file.write_text(generate_netlify_config(), encoding="utf-8")
        print(f"{GREEN}✓ Créé: {netlify_file}{RESET}")
    else:
        print(f"{YELLOW}⚠ Existe déjà: {netlify_file} — non modifié{RESET}")

    print(f"\n{BOLD}Recommandations CI/CD :{RESET}")
    recs = [
        "🔐 Configurer SWARM_API_URL, NEXTAUTH_SECRET dans GitHub Secrets",
        "📊 Activer Codecov pour le suivi de la couverture de tests",
        "🚀 Configurer le déploiement automatique sur Netlify via GitHub Actions",
        "📧 Configurer les notifications Slack/email sur échec CI",
        "🔄 Ajouter un job de rollback automatique si le déploiement échoue",
        "⏱️ Mettre en cache les node_modules et pip pour accélérer le build",
    ]
    for rec in recs:
        print(f"  {rec}")
    print()

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "existing_workflows": len(existing),
        "generated": [str(ci_file), str(netlify_file)],
        "recommendations": recs,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_agent(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
