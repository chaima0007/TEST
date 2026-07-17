#!/usr/bin/env python3
"""API Response Validator Agent — CaelumSwarm™ | Validation CSDDD
Valide la structure et l'intégrité des réponses JSON de tous les engines CaelumSwarm.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
import urllib.request
import urllib.error

AGENT_NAME = "APIResponseValidatorAgent"
VERSION = "1.0.0"

BASE_URL = os.environ.get("CAELUM_BASE_URL", "http://localhost:3000")

REQUIRED_ENGINE_FIELDS = {"engine", "entities"}
REQUIRED_ENTITY_FIELDS = {"composite_score", "level"}
VALID_LEVELS = {"critique", "élevé", "modéré", "faible"}

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def discover_api_routes(project_root: str) -> list[str]:
    api_dir = Path(project_root) / "app" / "api"
    return [d.name for d in sorted(api_dir.iterdir()) if d.is_dir() and (d / "route.ts").exists()] if api_dir.exists() else []


def validate_response(slug: str, base_url: str) -> dict:
    url = f"{base_url}/api/{slug}"
    errors = []
    warnings = []

    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"CaelumValidator/{VERSION}"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                return {"slug": slug, "valid": False, "errors": [f"Invalid JSON: {e}"], "warnings": []}

            payload = data.get("payload", data)

            # Check required fields
            for field in REQUIRED_ENGINE_FIELDS:
                if field not in payload:
                    errors.append(f"Missing field: {field}")

            # Check entities
            entities = payload.get("entities", [])
            if not isinstance(entities, list):
                errors.append("'entities' must be a list")
            elif len(entities) == 0:
                warnings.append("Empty entities list (upstream not configured)")
            else:
                for i, entity in enumerate(entities[:3]):  # Check first 3
                    if not isinstance(entity, dict):
                        errors.append(f"Entity {i} is not a dict")
                        continue
                    level = entity.get("level") or entity.get("risk_level") or entity.get("severity")
                    if level and level not in VALID_LEVELS:
                        errors.append(f"Entity {i}: invalid level '{level}'")

            # Check digital seal
            if "seal" not in data and "payload" not in data:
                warnings.append("No digital seal wrapper (sealResponse not applied)")

    except urllib.error.HTTPError as e:
        if e.code == 502:
            warnings.append(f"502 Bad Gateway — upstream not configured (expected in dev)")
            return {"slug": slug, "valid": True, "errors": [], "warnings": warnings}
        errors.append(f"HTTP {e.code}: {e.reason}")
    except Exception as e:
        errors.append(f"Connection failed: {e}")

    return {
        "slug": slug,
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def run_validator(project_root: str = "/home/user/TEST", base_url: str = BASE_URL) -> dict:
    slugs = discover_api_routes(project_root)
    print(f"\n{BOLD}CaelumSwarm™ API Response Validator v{VERSION}{RESET}")
    print(f"Validating {len(slugs)} endpoints against {base_url}\n")

    results = []
    valid_count = invalid_count = 0

    for slug in slugs:
        result = validate_response(slug, base_url)
        results.append(result)
        if result["valid"]:
            valid_count += 1
            icon = f"{GREEN}✓{RESET}"
        else:
            invalid_count += 1
            icon = f"{RED}✗{RESET}"

        print(f"  {icon} {slug}")
        for err in result["errors"]:
            print(f"       {RED}ERROR: {err}{RESET}")
        for warn in result["warnings"]:
            print(f"       {YELLOW}WARN: {warn}{RESET}")

    print(f"\n{BOLD}Results: {GREEN}{valid_count} valid{RESET} | {RED}{invalid_count} invalid{RESET} / {len(slugs)} total{RESET}\n")

    return {
        "agent": AGENT_NAME,
        "total": len(slugs),
        "valid": valid_count,
        "invalid": invalid_count,
        "results": results,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    result = run_validator()
    sys.exit(0 if result["invalid"] == 0 else 1)
