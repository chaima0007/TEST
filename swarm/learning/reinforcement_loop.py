"""
CaelumSwarm Reinforcement Learning Loop
Propriété exclusive Caelum Partners SPRL — Chaima Mhadbi
Améliore automatiquement les poids de chaque engine en apprenant des données générées.
"""

import json
import os
import math
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Any

INTELLIGENCE_DIR = Path(__file__).parent.parent / "intelligence"
WEIGHTS_DIR = Path(__file__).parent / "weights"
FEEDBACK_DIR = Path(__file__).parent / "feedback"
LEARNING_RATE = 0.05
MIN_WEIGHT = 0.10
MAX_WEIGHT = 0.50

# Pondérations de référence par défaut (CAE-INV-2025-003)
DEFAULT_WEIGHTS = {
    "sub1": 0.30,
    "sub2": 0.25,
    "sub3": 0.25,
    "sub4": 0.20,
}

# Seuils de classification (ComplianceIQ™)
THRESHOLDS = {"critique": 60.0, "élevé": 40.0, "modéré": 20.0, "faible": 0.0}


def classify(score: float) -> str:
    if score >= THRESHOLDS["critique"]:
        return "critique"
    if score >= THRESHOLDS["élevé"]:
        return "élevé"
    if score >= THRESHOLDS["modéré"]:
        return "modéré"
    return "faible"


def load_weights(engine_name: str) -> dict:
    path = WEIGHTS_DIR / f"{engine_name}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return DEFAULT_WEIGHTS.copy()


def save_weights(engine_name: str, weights: dict) -> None:
    WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
    path = WEIGHTS_DIR / f"{engine_name}.json"
    weights["updated_at"] = datetime.utcnow().isoformat()
    weights["engine"] = engine_name
    with open(path, "w") as f:
        json.dump(weights, f, indent=2, ensure_ascii=False)


def load_engine_data(engine_name: str) -> list[dict]:
    """Charge les entités d'un engine via son module Python."""
    py_path = INTELLIGENCE_DIR / f"{engine_name}.py"
    if not py_path.exists():
        return []
    spec = importlib.util.spec_from_file_location(engine_name, py_path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return []
    # Cherche ENTITIES ou entities dans le module
    for attr in ("ENTITIES", "entities", "MOCK"):
        val = getattr(mod, attr, None)
        if isinstance(val, list):
            return val
        if isinstance(val, dict) and "entities" in val:
            return val["entities"]
    return []


def compute_reward(predicted_level: str, actual_level: str) -> float:
    """Récompense +1.0 si correct, pénalité proportionnelle à l'écart."""
    order = ["faible", "modéré", "élevé", "critique"]
    if predicted_level == actual_level:
        return 1.0
    pred_idx = order.index(predicted_level) if predicted_level in order else 0
    act_idx = order.index(actual_level) if actual_level in order else 0
    gap = abs(pred_idx - act_idx)
    return max(-1.0, 1.0 - gap * 0.5)


def gradient_step(weights: dict, entities: list[dict], engine_name: str) -> tuple[dict, dict]:
    """
    Ajuste les poids par descente de gradient approximée.
    Récompense les weights qui prédisent mieux le risk_level documenté.
    """
    if not entities:
        return weights, {"message": "no entities", "delta": {}}

    deltas = {k: 0.0 for k in ["sub1", "sub2", "sub3", "sub4"]}
    total_reward = 0.0

    for entity in entities:
        if isinstance(entity, dict):
            score = entity.get("composite_score", 0)
            actual = entity.get("risk_level", "faible")
        else:
            score = getattr(entity, "composite_score", 0)
            actual = getattr(entity, "risk_level", "faible")
        predicted = classify(score)
        reward = compute_reward(predicted, actual)
        total_reward += reward

        # Si erreur, ajuste le poids du sous-score dominant
        if reward < 1.0:
            # Le sous-score qui a le plus d'influence est sub1 (0.30)
            # On perturbe chaque poids dans la direction qui réduirait l'erreur
            direction = 1.0 if actual in ["critique", "élevé"] else -1.0
            for k in deltas:
                deltas[k] += direction * LEARNING_RATE * abs(reward - 1.0) * 0.25

    # Applique les deltas et normalise pour sum=1.0
    new_weights = {}
    raw = {}
    for k in ["sub1", "sub2", "sub3", "sub4"]:
        raw[k] = max(MIN_WEIGHT, min(MAX_WEIGHT, weights[k] + deltas[k]))

    total = sum(raw.values())
    for k in raw:
        new_weights[k] = round(raw[k] / total, 4)

    avg_reward = total_reward / len(entities) if entities else 0
    metrics = {
        "engine": engine_name,
        "entities_evaluated": len(entities),
        "avg_reward": round(avg_reward, 4),
        "weight_delta": {k: round(new_weights[k] - weights[k], 4) for k in ["sub1", "sub2", "sub3", "sub4"]},
        "new_weights": new_weights,
        "timestamp": datetime.utcnow().isoformat(),
    }
    return new_weights, metrics


def run_feedback_cycle(engine_names: list[str] | None = None) -> list[dict]:
    """
    Lance un cycle d'amélioration sur tous les engines (ou une liste donnée).
    Retourne le rapport de chaque engine.
    """
    if engine_names is None:
        engine_names = [
            p.stem for p in INTELLIGENCE_DIR.glob("*_engine.py")
            if not p.stem.startswith("_")
        ]

    results = []
    for name in engine_names:
        current_weights = load_weights(name)
        entities = load_engine_data(name)
        if not entities:
            results.append({"engine": name, "status": "skipped", "reason": "no entities loaded"})
            continue
        new_weights, metrics = gradient_step(current_weights, entities, name)
        save_weights(name, new_weights)
        metrics["status"] = "updated"
        results.append(metrics)

    _save_feedback_report(results)
    return results


def _save_feedback_report(results: list[dict]) -> None:
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = FEEDBACK_DIR / f"feedback_{ts}.json"
    with open(path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    _keep_latest_n(FEEDBACK_DIR, n=30)


def _keep_latest_n(directory: Path, n: int) -> None:
    files = sorted(directory.glob("feedback_*.json"))
    for old in files[:-n]:
        old.unlink(missing_ok=True)


def get_optimized_weights(engine_name: str) -> dict:
    """API publique — retourne les poids optimisés pour un engine."""
    return load_weights(engine_name)


def improvement_summary() -> dict:
    """Résumé de l'état d'apprentissage de tous les engines."""
    weight_files = list(WEIGHTS_DIR.glob("*.json"))
    summary = {
        "total_engines_with_custom_weights": len(weight_files),
        "engines": [],
        "generated_at": datetime.utcnow().isoformat(),
    }
    for wf in weight_files:
        with open(wf) as f:
            data = json.load(f)
        deviation = sum(
            abs(data.get(k, DEFAULT_WEIGHTS[k]) - DEFAULT_WEIGHTS[k])
            for k in ["sub1", "sub2", "sub3", "sub4"]
        )
        summary["engines"].append({
            "engine": data.get("engine", wf.stem),
            "updated_at": data.get("updated_at"),
            "weights": {k: data.get(k) for k in ["sub1", "sub2", "sub3", "sub4"]},
            "deviation_from_default": round(deviation, 4),
        })
    summary["engines"].sort(key=lambda x: x["deviation_from_default"], reverse=True)
    return summary


if __name__ == "__main__":
    print("=== CaelumSwarm Reinforcement Learning Loop ===")
    print(f"Scanning engines in: {INTELLIGENCE_DIR}")
    results = run_feedback_cycle()
    updated = [r for r in results if r.get("status") == "updated"]
    skipped = [r for r in results if r.get("status") == "skipped"]
    print(f"\n✓ {len(updated)} engines mis à jour")
    print(f"  {len(skipped)} engines ignorés (pas d'entités chargées)")
    if updated:
        avg_rewards = [r["avg_reward"] for r in updated]
        print(f"  Récompense moyenne globale: {sum(avg_rewards)/len(avg_rewards):.4f}")
        best = max(updated, key=lambda x: x["avg_reward"])
        print(f"  Meilleur engine: {best['engine']} (reward={best['avg_reward']})")
    summary = improvement_summary()
    print(f"\n📊 {summary['total_engines_with_custom_weights']} engines avec poids optimisés")
    print("=== Cycle terminé ===")
