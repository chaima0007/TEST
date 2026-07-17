#!/usr/bin/env python3
"""Env Config Validator Agent — CaelumSwarm™ Dev Support
Valide les variables d'environnement requises, détecte les configs manquantes,
vérifie la cohérence entre .env.example et l'utilisation réelle dans le code.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "EnvConfigValidatorAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Variables d'environnement requises pour CaelumSwarm
REQUIRED_ENV_VARS = {
    "SWARM_API_URL": {
        "description": "URL de l'API upstream CaelumSwarm (ex: https://api.caelum.partners)",
        "critical": True,
        "example": "https://api.caelum.partners",
        "validation": r"^https?://",
    },
    "NEXTAUTH_SECRET": {
        "description": "Secret NextAuth.js pour les sessions",
        "critical": True,
        "example": "your-secret-here-min-32-chars",
        "validation": r".{32,}",
    },
    "NEXTAUTH_URL": {
        "description": "URL de base de l'application",
        "critical": True,
        "example": "https://astounding-haupia-16b5a6.netlify.app",
        "validation": r"^https?://",
    },
    "DIGITAL_SEAL_KEY": {
        "description": "Clé pour le scellement cryptographique des réponses API",
        "critical": False,
        "example": "caelum-seal-key-2026",
        "validation": r".{8,}",
    },
}

OPTIONAL_ENV_VARS = {
    "NEXT_PUBLIC_APP_URL": "URL publique de l'app (pour les liens absolus)",
    "VERCEL_URL": "URL Vercel (auto-injectée par Vercel)",
    "NETLIFY_URL": "URL Netlify (auto-injectée par Netlify)",
    "NODE_ENV": "Environnement (development/production/test)",
    "ANALYZE": "Activer l'analyseur de bundle Next.js (true/false)",
}


def extract_env_vars_from_code(root: Path) -> set[str]:
    """Extrait tous les process.env.XXX utilisés dans le code."""
    env_vars = set()
    files = (
        list((root / "app").rglob("*.ts"))
        + list((root / "app").rglob("*.tsx"))
        + list((root / "lib").rglob("*.ts"))
        + list((root / "components").rglob("*.tsx"))
    )

    for filepath in files:
        try:
            source = filepath.read_text(encoding="utf-8", errors="ignore")
            matches = re.findall(r'process\.env\.([A-Z][A-Z0-9_]+)', source)
            env_vars.update(matches)
        except Exception:
            pass

    return env_vars


def parse_env_file(env_path: Path) -> dict[str, str]:
    """Parse un fichier .env et retourne les variables."""
    env_vars = {}
    if not env_path.exists():
        return env_vars

    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            env_vars[key.strip()] = value.strip().strip('"').strip("'")

    return env_vars


def run_validator(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  CaelumSwarm™ Env Config Validator v{VERSION}{RESET}")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}\n")

    results = {
        "critical_missing": [],
        "optional_missing": [],
        "undocumented": [],
        "invalid_values": [],
        "valid": [],
    }

    # Lire les fichiers env
    env_local = parse_env_file(root / ".env.local")
    env_example = parse_env_file(root / ".env.example")
    env_base = parse_env_file(root / ".env")
    all_env = {**env_base, **env_local}

    # Extraire les vars utilisées dans le code
    code_env_vars = extract_env_vars_from_code(root)

    print(f"{BOLD}Variables requises :{RESET}")
    for var, config in REQUIRED_ENV_VARS.items():
        value = all_env.get(var, "")

        if not value:
            if config["critical"]:
                results["critical_missing"].append(var)
                print(f"  {RED}✗ CRITIQUE{RESET} {var} — {config['description']}")
                print(f"    Exemple: {var}={config['example']}")
            else:
                results["optional_missing"].append(var)
                print(f"  {YELLOW}⚠ ABSENT{RESET}  {var} — {config['description']}")
        else:
            # Valider le format
            if config.get("validation") and not re.match(config["validation"], value):
                results["invalid_values"].append({"var": var, "issue": f"Format invalide (attendu: {config['validation']})"})
                print(f"  {YELLOW}⚠ FORMAT{RESET}  {var}={value[:20]}... — format invalide")
            else:
                results["valid"].append(var)
                masked = value[:3] + "***" + value[-3:] if len(value) > 8 else "***"
                print(f"  {GREEN}✓ OK{RESET}      {var}={masked}")

    # Variables dans le code mais pas dans .env.example
    print(f"\n{BOLD}Variables utilisées dans le code ({len(code_env_vars)}) :{RESET}")
    known_vars = set(REQUIRED_ENV_VARS.keys()) | set(OPTIONAL_ENV_VARS.keys())
    undocumented = code_env_vars - known_vars
    if undocumented:
        print(f"  {YELLOW}Non documentées : {', '.join(sorted(undocumented))}{RESET}")
        results["undocumented"] = sorted(list(undocumented))
    else:
        print(f"  {GREEN}✓ Toutes documentées{RESET}")

    # Générer/mettre à jour .env.example
    example_path = root / ".env.example"
    example_content = "# CaelumSwarm™ — Variables d'environnement requises\n"
    example_content += f"# Généré par {AGENT_NAME} v{VERSION} — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n\n"
    example_content += "# ─── OBLIGATOIRES ───\n"
    for var, config in REQUIRED_ENV_VARS.items():
        example_content += f"# {config['description']}\n"
        example_content += f"{var}={config['example']}\n\n"
    example_content += "# ─── OPTIONNELLES ───\n"
    for var, desc in OPTIONAL_ENV_VARS.items():
        example_content += f"# {desc}\n# {var}=\n\n"

    example_path.write_text(example_content, encoding="utf-8")
    print(f"\n{GREEN}✓ .env.example mis à jour{RESET}")

    # Score
    total = len(REQUIRED_ENV_VARS)
    ok = len(results["valid"])
    score = int(ok / total * 100) if total > 0 else 0
    color = GREEN if score >= 80 else YELLOW if score >= 50 else RED
    print(f"\n{BOLD}Score config: {color}{score}/100{RESET} ({ok}/{total} vars critiques configurées)\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "score": score,
        "critical_missing": results["critical_missing"],
        "optional_missing": results["optional_missing"],
        "undocumented": results["undocumented"],
        "invalid_values": results["invalid_values"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_validator(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
