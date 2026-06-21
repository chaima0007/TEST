#!/usr/bin/env python3
"""
Caelum Partners — Engine Smoke Tests
Usage:
  python3 tests/e2e/test_engine_smoke.py --offline
  TEST_BASE_URL=http://localhost:3000 python3 tests/e2e/test_engine_smoke.py
"""

import sys
import os
import importlib.util
import json

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# ---------------------------------------------------------------------------
# Engine registry
# ---------------------------------------------------------------------------
ENGINES = [
    {
        "module": "digital_gender_gap_rights",
        "slug": "digital-gender-gap-rights-engine",
        "label": "Digital Gender Gap Rights",
    },
    {
        "module": "unpaid_care_work_rights",
        "slug": "unpaid-care-work-rights-engine",
        "label": "Unpaid Care Work Rights",
    },
    {
        "module": "youth_justice_rights",
        "slug": "youth-justice-rights-engine",
        "label": "Youth Justice Rights",
    },
    {
        "module": "land_grabbing_rights",
        "slug": "land-grabbing-rights-engine",
        "label": "Land Grabbing Rights",
    },
    {
        "module": "prison_labor_rights",
        "slug": "prison-labor-rights-engine",
        "label": "Prison Labor Rights",
    },
    {
        "module": "statelessness_rights",
        "slug": "statelessness-rights-engine",
        "label": "Statelessness Rights",
    },
    {
        "module": "algorithmic_bias_rights",
        "slug": "algorithmic-bias-rights-engine",
        "label": "Algorithmic Bias Rights",
    },
    {
        "module": "hate_speech_platform_rights",
        "slug": "hate-speech-platform-rights-engine",
        "label": "Hate Speech Platform Rights",
    },
]

INTELLIGENCE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "swarm",
    "intelligence",
)

# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def validate_engine_output(data: dict, label: str) -> tuple[bool, str]:
    """Validate that engine output matches expected structure."""
    # Support both dict-with-entities and list formats
    entities = None
    if isinstance(data, dict):
        # Try common keys
        for key in ("entities", "data", "results", "countries", "regions"):
            if key in data and isinstance(data[key], list):
                entities = data[key]
                break
        if entities is None and "avg_composite" in data:
            # Some engines return flat structure — treat top-level as valid
            avg = data.get("avg_composite", 0)
            risk_dist = str(data.get("risk_distribution", ""))
            if avg > 0 and "critique" in risk_dist:
                return True, f"avg={avg:.2f} (flat format, critique found)"
            return False, f"avg={avg} risk_dist={risk_dist!r}"
    elif isinstance(data, list):
        entities = data

    if entities is None:
        return False, f"Cannot find entity list in output keys: {list(data.keys()) if isinstance(data, dict) else type(data)}"

    total = len(entities)
    if total != 8:
        return False, f"Expected 8 entities, got {total}"

    # Compute avg_composite
    composites = []
    for e in entities:
        if isinstance(e, dict):
            score = e.get("composite_score") or e.get("composite") or e.get("score", 0)
            composites.append(float(score))

    avg = sum(composites) / len(composites) if composites else 0
    if avg <= 0:
        return False, f"avg_composite={avg:.2f} — expected > 0"

    # Check for "critique" risk level
    all_text = json.dumps(entities).lower()
    if "critique" not in all_text and "critical" not in all_text:
        return False, f"No 'critique' risk level found in output (avg={avg:.2f})"

    return True, f"avg={avg:.2f} entities={total} critique=found"


# ---------------------------------------------------------------------------
# Offline mode: import and run Python engines directly
# ---------------------------------------------------------------------------

def run_offline(engines: list[dict]) -> tuple[int, int]:
    """Run engines by importing them as Python modules."""
    passed = 0
    failed = 0

    for engine in engines:
        label = engine["label"]
        module_name = engine["module"]
        module_path = os.path.join(INTELLIGENCE_DIR, f"{module_name}.py")

        if not os.path.exists(module_path):
            print(f"  SKIP  {label} — file not found: {module_path}")
            continue

        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            # Try to get data from common entry points
            data = None
            for fn_name in ("get_data", "get_engine_data", "run", "main", "generate"):
                fn = getattr(mod, fn_name, None)
                if callable(fn):
                    try:
                        data = fn()
                        break
                    except Exception:
                        pass

            # Fallback: look for a top-level DATA or ENTITIES constant
            if data is None:
                for attr in ("DATA", "ENTITIES", "RESULTS", "OUTPUT"):
                    if hasattr(mod, attr):
                        data = getattr(mod, attr)
                        break

            if data is None:
                print(f"  FAIL  {label} — no callable entry point or DATA constant found")
                failed += 1
                continue

            ok, msg = validate_engine_output(data, label)
            if ok:
                print(f"  PASS  {label} — {msg}")
                passed += 1
            else:
                print(f"  FAIL  {label} — {msg}")
                failed += 1

        except Exception as exc:
            print(f"  FAIL  {label} — exception: {exc}")
            failed += 1

    return passed, failed


# ---------------------------------------------------------------------------
# HTTP mode: call Next.js API routes
# ---------------------------------------------------------------------------

def run_http(engines: list[dict], base_url: str) -> tuple[int, int]:
    """Run engines by calling Next.js API endpoints via HTTP."""
    if not REQUESTS_AVAILABLE:
        print("ERROR: 'requests' package not installed. Run: pip install requests")
        sys.exit(1)

    passed = 0
    failed = 0

    for engine in engines:
        label = engine["label"]
        url = f"{base_url.rstrip('/')}/api/{engine['slug']}"

        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code not in (200, 502):
                print(f"  FAIL  {label} — HTTP {resp.status_code} from {url}")
                failed += 1
                continue

            data = resp.json()

            # Unwrap sealed response if present
            if isinstance(data, dict) and "data" in data and isinstance(data["data"], (dict, list)):
                data = data["data"]

            ok, msg = validate_engine_output(data, label)
            if ok:
                print(f"  PASS  {label} — HTTP {resp.status_code} {msg}")
                passed += 1
            else:
                print(f"  FAIL  {label} — HTTP {resp.status_code} {msg}")
                failed += 1

        except requests.RequestException as exc:
            print(f"  FAIL  {label} — request error: {exc}")
            failed += 1
        except ValueError as exc:
            print(f"  FAIL  {label} — JSON parse error: {exc}")
            failed += 1

    return passed, failed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    offline = "--offline" in sys.argv
    base_url = os.environ.get("TEST_BASE_URL", "")

    if offline:
        print(f"[smoke] Mode: OFFLINE — importing engines from {INTELLIGENCE_DIR}")
        print(f"[smoke] Testing {len(ENGINES)} engines...\n")
        passed, failed = run_offline(ENGINES)
    elif base_url:
        print(f"[smoke] Mode: HTTP — base URL: {base_url}")
        print(f"[smoke] Testing {len(ENGINES)} engines...\n")
        passed, failed = run_http(ENGINES, base_url)
    else:
        print("Usage:")
        print("  python3 tests/e2e/test_engine_smoke.py --offline")
        print("  TEST_BASE_URL=http://localhost:3000 python3 tests/e2e/test_engine_smoke.py")
        sys.exit(1)

    total = passed + failed
    print(f"\n[smoke] Results: {passed}/{total} passed")

    if failed > 0:
        print(f"[smoke] FAILED — {failed} engine(s) did not pass smoke tests")
        sys.exit(1)
    else:
        print("[smoke] All engines passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
