#!/usr/bin/env python3
"""Documentation Generator Agent — CaelumSwarm™ Dev Support
Génère automatiquement : AGENT_REGISTRY.md, API_REFERENCE.md,
WAVE_CHANGELOG.md, engine stats summaries.
"""
import re
import json
import importlib.util
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "DocumentationGeneratorAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def extract_engine_metadata(engine_path: Path) -> dict:
    """Extrait les métadonnées d'un engine Python sans l'exécuter."""
    source = engine_path.read_text(encoding="utf-8", errors="ignore")

    # Extraction du docstring
    docstring_match = re.search(r'"""([^"]+)"""', source)
    docstring = docstring_match.group(1).strip() if docstring_match else ""

    # Extraction de l'accent color
    accent_match = re.search(r'ACCENT_COLOR\s*=\s*["\']([#\w]+)["\']', source)
    accent = accent_match.group(1) if accent_match else "unknown"

    # Extraction du domaine
    domain_match = re.search(r'DOMAIN(?:_CODE)?\s*=\s*["\']([^"\']+)["\']', source)
    domain = domain_match.group(1) if domain_match else engine_path.stem

    # Wave number depuis le docstring
    wave_match = re.search(r'Wave\s+(\d+)', docstring)
    wave = wave_match.group(1) if wave_match else "?"

    # Nombre d'entités
    entity_count = source.count('"id"') or source.count('"name"') or 8

    return {
        "name": engine_path.stem,
        "slug": engine_path.stem.replace("_", "-"),
        "wave": wave,
        "domain": domain,
        "accent_color": accent,
        "docstring": docstring[:100],
        "file": str(engine_path.name),
    }


def generate_agent_registry(root: Path) -> str:
    engines = sorted((root / "swarm" / "intelligence").glob("*_engine.py"))
    scripts = sorted((root / "scripts").glob("*.py"))

    lines = [
        "# AGENT REGISTRY — CaelumSwarm™",
        f"*Dernière mise à jour : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*",
        f"*{len(engines)} engines | {len(scripts)} scripts agents*",
        "",
        "---",
        "",
        "## Engines de Conformité CSDDD",
        "",
        "| Wave | Slug | Domain | Accent | Fichier |",
        "|------|------|--------|--------|---------|",
    ]

    wave_engines = {}
    for engine_path in engines:
        meta = extract_engine_metadata(engine_path)
        wave = meta["wave"]
        if wave not in wave_engines:
            wave_engines[wave] = []
        wave_engines[wave].append(meta)

    for wave in sorted(wave_engines.keys(), key=lambda x: int(x) if x.isdigit() else 0):
        for meta in wave_engines[wave]:
            slug = meta["slug"]
            domain = meta["domain"][:25]
            accent = meta["accent_color"]
            file = meta["file"]
            lines.append(f"| {wave} | `{slug}` | {domain} | `{accent}` | `{file}` |")

    lines += [
        "",
        "---",
        "",
        "## Agents Support & Infrastructure",
        "",
        "| Agent | Description | Usage |",
        "|-------|-------------|-------|",
    ]

    SCRIPT_DESCRIPTIONS = {
        "health-latency-monitor-agent.py": ("Health & Latency Monitor", "`python scripts/health-latency-monitor-agent.py --url <URL>`"),
        "api-response-validator-agent.py": ("API Response Validator", "`python scripts/api-response-validator-agent.py`"),
        "code-quality-review-agent.py": ("Code Quality Review", "`python scripts/code-quality-review-agent.py`"),
        "typescript-error-fixer-agent.py": ("TypeScript Error Fixer", "`python scripts/typescript-error-fixer-agent.py [--apply]`"),
        "security-audit-agent.py": ("Security Audit OWASP", "`python scripts/security-audit-agent.py`"),
        "test-generator-agent.py": ("Test Generator", "`python scripts/test-generator-agent.py`"),
        "dependency-audit-agent.py": ("Dependency Audit", "`python scripts/dependency-audit-agent.py`"),
        "wave-consistency-checker-agent.py": ("Wave Consistency Check", "`python scripts/wave-consistency-checker-agent.py`"),
        "documentation-generator-agent.py": ("Documentation Generator", "`python scripts/documentation-generator-agent.py`"),
        "bundle-size-monitor-agent.py": ("Bundle Size Monitor", "`python scripts/bundle-size-monitor-agent.py`"),
        "env-config-validator-agent.py": ("Env Config Validator", "`python scripts/env-config-validator-agent.py`"),
        "git-workflow-automation-agent.py": ("Git Workflow Automation", "`python scripts/git-workflow-automation-agent.py --help`"),
        "accessibility-checker-agent.py": ("Accessibility Checker", "`python scripts/accessibility-checker-agent.py`"),
        "performance-profiler-agent.py": ("Performance Profiler", "`python scripts/performance-profiler-agent.py`"),
        "log-management-agent.py": ("Log Management", "`python scripts/log-management-agent.py`"),
        "supply-chain-digital-twin-agent.py": ("Supply Chain Digital Twin", "`python scripts/supply-chain-digital-twin-agent.py`"),
        "regulatory-compliance-monitoring-agent.py": ("Regulatory Compliance Monitor", "`python scripts/regulatory-compliance-monitoring-agent.py`"),
        "stakeholder-grievance-redress-agent.py": ("Stakeholder Grievance Redress", "`python scripts/stakeholder-grievance-redress-agent.py`"),
    }

    for script in scripts:
        name = script.name
        desc, usage = SCRIPT_DESCRIPTIONS.get(name, (name.replace(".py", "").replace("-", " ").title(), f"`python scripts/{name}`"))
        lines.append(f"| **{desc}** | Monitoring et support | {usage} |")

    lines += [
        "",
        "---",
        "",
        "## Architecture CaelumSwarm™",
        "",
        "```",
        "CaelumSwarm™",
        "├── swarm/intelligence/     # Engines Python (compliance CSDDD)",
        "├── app/api/               # Routes API Next.js (sealResponse + 502)",
        "├── app/dashboard/         # Dashboards React (\"use client\" + GaugeRing)",
        "├── components/Sidebar.tsx # Navigation (icon: ComponentType)",
        "├── lib/digital-seal.ts    # Seal cryptographique API",
        "└── scripts/               # Agents support & monitoring",
        "```",
        "",
        "## Conformité",
        "- **CSDDD** EU 2024/1760 (applicable 2027-07-26) — Art.8-13",
        "- **Dodd-Frank** Section 1502 (minerais de conflit)",
        "- **ILO Core Conventions** (travail des enfants, travail forcé)",
        "- **UNGP** (Principes Directeurs ONU Entreprises et Droits de l'Homme)",
        "",
        f"*Généré par {AGENT_NAME} v{VERSION}*",
    ]

    return "\n".join(lines)


def generate_wave_changelog(root: Path) -> str:
    engines = sorted((root / "swarm" / "intelligence").glob("*_engine.py"))

    wave_map = {}
    for engine_path in engines:
        meta = extract_engine_metadata(engine_path)
        wave = meta["wave"]
        if wave not in wave_map:
            wave_map[wave] = []
        wave_map[wave].append(meta)

    lines = [
        "# WAVE CHANGELOG — CaelumSwarm™",
        f"*{len(engines)} engines actifs | {datetime.now(timezone.utc).strftime('%Y-%m-%d')}*",
        "",
    ]

    for wave in sorted(wave_map.keys(), key=lambda x: int(x) if x.isdigit() else 0, reverse=True):
        lines.append(f"## Wave {wave}")
        for meta in wave_map[wave]:
            lines.append(f"- `{meta['name']}` ({meta['accent_color']}) — {meta['docstring'][:60]}")
        lines.append("")

    return "\n".join(lines)


def run_generator(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}CaelumSwarm™ Documentation Generator v{VERSION}{RESET}\n")

    generated = []

    # AGENT_REGISTRY.md
    registry_content = generate_agent_registry(root)
    registry_path = root / "AGENT_REGISTRY.md"
    registry_path.write_text(registry_content, encoding="utf-8")
    print(f"  {GREEN}✓{RESET} {registry_path}")
    generated.append(str(registry_path))

    # WAVE_CHANGELOG.md
    changelog_content = generate_wave_changelog(root)
    changelog_path = root / "docs" / "WAVE_CHANGELOG.md"
    changelog_path.parent.mkdir(parents=True, exist_ok=True)
    changelog_path.write_text(changelog_content, encoding="utf-8")
    print(f"  {GREEN}✓{RESET} {changelog_path}")
    generated.append(str(changelog_path))

    print(f"\n{GREEN}✓ {len(generated)} documents générés{RESET}\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "generated_files": generated,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_generator(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
