#!/usr/bin/env python3
"""Test Generator Agent — CaelumSwarm™ Dev Support
Génère automatiquement des tests unitaires pytest pour tous les engines Python.
Vérifie : distribution (4c/2é/1m/1f), avg_composite (60-63), formule, index.
"""
import ast
import json
import importlib.util
import sys
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "TestGeneratorAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

TEST_TEMPLATE = '''#!/usr/bin/env python3
"""Tests auto-générés pour {engine_name} — CaelumSwarm™"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

# Import dynamique de l'engine
spec = importlib.util.spec_from_file_location("{module}", "{engine_path}")
engine_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine_module)
import importlib.util


@pytest.fixture(scope="module")
def engine_result():
    return engine_module.run_engine()


def test_engine_runs_without_error(engine_result):
    """L\'engine doit s\'exécuter sans erreur."""
    assert engine_result is not None


def test_total_entities(engine_result):
    """Doit avoir exactement 8 entités."""
    entities = engine_result.get("entities", [])
    assert len(entities) == 8, f"Attendu 8 entités, obtenu {{len(entities)}}"


def test_distribution_4_2_1_1(engine_result):
    """Distribution obligatoire : 4 critique, 2 élevé, 1 modéré, 1 faible."""
    from collections import Counter
    entities = engine_result.get("entities", [])
    levels = [e.get("level") or e.get("severity") or e.get("risk_level") for e in entities]
    counts = Counter(levels)
    assert counts.get("critique", 0) == 4, f"Attendu 4 critique, obtenu {{counts.get('critique', 0)}}"
    assert counts.get("élevé", 0) == 2, f"Attendu 2 élevé, obtenu {{counts.get('élevé', 0)}}"
    assert counts.get("modéré", 0) == 1, f"Attendu 1 modéré, obtenu {{counts.get('modéré', 0)}}"
    assert counts.get("faible", 0) == 1, f"Attendu 1 faible, obtenu {{counts.get('faible', 0)}}"


def test_avg_composite_in_range(engine_result):
    """avg_composite doit être entre 60.00 et 63.00."""
    avg = engine_result.get("avg_composite") or engine_result.get("summary", {{}}).get("avg_composite_score", 0)
    assert 60.0 <= avg <= 63.0, f"avg_composite {{avg}} hors plage [60.00, 63.00]"


def test_composite_scores_are_numbers(engine_result):
    """Tous les composite_score doivent être des nombres."""
    entities = engine_result.get("entities", [])
    for e in entities:
        score = e.get("composite_score")
        assert isinstance(score, (int, float)), f"composite_score invalide pour {{e.get('entity', e.get('name', '?'))}}: {{score}}"


def test_index_field_present(engine_result):
    """Chaque entité doit avoir un champ estimated_*_index."""
    entities = engine_result.get("entities", [])
    for e in entities:
        index_fields = [k for k in e.keys() if k.startswith("estimated_") and k.endswith("_index")]
        assert len(index_fields) >= 1, f"Champ estimated_*_index manquant pour {{e.get('entity', '?')}}"


def test_critique_scores_above_60(engine_result):
    """Les entités \'critique\' doivent avoir composite_score >= 60."""
    entities = engine_result.get("entities", [])
    for e in entities:
        level = e.get("level") or e.get("severity") or e.get("risk_level")
        score = e.get("composite_score", 0)
        if level == "critique":
            assert score >= 60, f"Entité critique {{e.get('entity', '?')}} a score {{score}} < 60"


def test_faible_scores_below_20(engine_result):
    """Les entités \'faible\' doivent avoir composite_score < 20."""
    entities = engine_result.get("entities", [])
    for e in entities:
        level = e.get("level") or e.get("severity") or e.get("risk_level")
        score = e.get("composite_score", 0)
        if level == "faible":
            assert score < 20, f"Entité faible {{e.get('entity', '?')}} a score {{score}} >= 20"


def test_index_formula(engine_result):
    """estimated_*_index doit être ≈ composite_score / 100 * 10."""
    entities = engine_result.get("entities", [])
    for e in entities:
        score = e.get("composite_score", 0)
        index_fields = {{k: v for k, v in e.items() if k.startswith("estimated_") and k.endswith("_index")}}
        for field, index_val in index_fields.items():
            expected = round(score / 100 * 10, 2)
            assert abs(index_val - expected) < 0.05, f"Index {{field}}={{index_val}}, attendu {{expected}}"
'''


def generate_test_for_engine(engine_path: Path, output_dir: Path) -> dict:
    engine_name = engine_path.stem
    module_name = engine_name.replace("-", "_")

    test_content = TEST_TEMPLATE.format(
        engine_name=engine_name,
        module=module_name,
        engine_path=str(engine_path),
    )

    output_file = output_dir / f"test_{module_name}.py"
    output_file.write_text(test_content, encoding="utf-8")

    return {"engine": engine_name, "test_file": str(output_file), "status": "generated"}


def run_generator(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    output_dir = root / "tests" / "engines"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Créer conftest.py si absent
    conftest = output_dir / "conftest.py"
    if not conftest.exists():
        conftest.write_text('"""Pytest configuration for CaelumSwarm™ engine tests."""\n')

    # Créer __init__.py
    (output_dir / "__init__.py").write_text("")

    print(f"\n{BOLD}CaelumSwarm™ Test Generator v{VERSION}{RESET}")

    engine_files = list((root / "swarm" / "intelligence").glob("*_engine.py"))
    print(f"Génération de tests pour {len(engine_files)} engines...\n")

    results = []
    for engine_path in sorted(engine_files):
        result = generate_test_for_engine(engine_path, output_dir)
        results.append(result)
        print(f"  {GREEN}✓{RESET} {result['test_file']}")

    # Générer un runner global
    runner = root / "tests" / "run_all_engine_tests.sh"
    runner.write_text(
        "#!/bin/bash\n"
        "# CaelumSwarm™ Engine Test Runner — auto-généré\n"
        "cd /home/user/TEST\n"
        "python -m pytest tests/engines/ -v --tb=short 2>&1 | tee tests/last_run.log\n"
    )
    runner.chmod(0o755)

    print(f"\n{GREEN}✓ {len(results)} fichiers de tests générés dans {output_dir}{RESET}")
    print(f"{GREEN}✓ Runner: {runner}{RESET}")
    print(f"\nPour exécuter: bash tests/run_all_engine_tests.sh\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "engines_tested": len(results),
        "output_dir": str(output_dir),
        "results": results,
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
