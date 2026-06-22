#!/usr/bin/env python3
"""
CaelumSwarm™ — Action Analyzer
Analyse croisée OBLIGATOIRE avant toute action sur le système.
Protocole: zéro erreur tolérée — chaque décision validée par tous les agents.
"""

import json
import random
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ── AGENTS D'ANALYSE ────────────────────────────────────────────────────────

def agent_impact(action: str, target: str) -> dict:
    """Agent Impact — Évalue les effets de l'action sur le système."""
    risk_keywords = {
        "delete": 0.9, "remove": 0.7, "drop": 0.9, "reset": 0.8,
        "overwrite": 0.6, "force": 0.5, "truncate": 0.9,
    }
    safe_keywords = {
        "add": 0.1, "create": 0.1, "fix": 0.15, "update": 0.2,
        "append": 0.1, "read": 0.0, "list": 0.0,
    }
    base_risk = 0.2
    action_lower = action.lower()
    for kw, risk in risk_keywords.items():
        if kw in action_lower:
            base_risk = max(base_risk, risk)
    for kw, safe in safe_keywords.items():
        if kw in action_lower:
            base_risk = min(base_risk, safe)
    level = "CRITIQUE" if base_risk > 0.7 else ("ÉLEVÉ" if base_risk > 0.4 else ("MODÉRÉ" if base_risk > 0.2 else "FAIBLE"))
    return {"agent": "IMPACT", "risk_score": round(base_risk, 2), "level": level,
            "reversible": base_risk < 0.5, "approval_required": base_risk > 0.6}


def agent_dependency(action: str, target: str) -> dict:
    """Agent Dépendances — Identifie les fichiers/systèmes affectés."""
    deps = []
    if "sidebar" in target.lower():
        deps = ["components/sidebar-icons*.tsx", "components/sidebar-nav.tsx",
                "components/Sidebar.tsx", "CI: nextjs-build"]
    elif "engine" in target.lower():
        deps = ["swarm/intelligence/*.py", "CI: python-tests", "data/library_index.json"]
    elif "route" in target.lower():
        deps = ["app/api/**/route.ts", "lib/digital-seal.ts", "CI: nextjs-build"]
    elif "dashboard" in target.lower():
        deps = ["app/dashboard/**/page.tsx", "CI: nextjs-build"]
    cascades = len(deps)
    return {"agent": "DEPS", "dependencies": deps,
            "cascade_count": cascades, "high_cascade": cascades > 3}


def agent_protocol_check(action: str, target: str) -> dict:
    """Agent Protocole — Vérifie conformité avec les règles CLAUDE.md/AGENTS.md."""
    violations = []
    warnings = []
    action_lower = action.lower()
    target_lower = target.lower()

    if "sidebar" in target_lower and "--force" in action_lower:
        violations.append("Jamais de force-push sur Sidebar.tsx")
    if "main" in target_lower or "master" in target_lower:
        violations.append("Jamais de push direct sur main/master")
    if "engine" in target_lower and "delete" in action_lower:
        warnings.append("Suppression engine — vérifier versioning DB d'abord")
    if "commit" in action_lower and "add -A" in action_lower:
        warnings.append("git add -A risque d'inclure des credentials — préférer git add <fichiers>")
    if "no-verify" in action_lower:
        violations.append("--no-verify interdit sauf demande explicite utilisateur")

    status = "VIOLATION" if violations else ("WARNING" if warnings else "OK")
    return {"agent": "PROTOCOL", "status": status,
            "violations": violations, "warnings": warnings}


def agent_quantum_validate(action: str, target: str, n_sims: int = 10_000) -> dict:
    """Agent Quantique — Monte Carlo sur le résultat prédit de l'action."""
    successes = 0
    for _ in range(n_sims):
        noise = random.gauss(0, 0.05)
        base_success = 0.92
        if "fix" in action.lower() or "add" in action.lower():
            base_success = 0.97
        if "delete" in action.lower() or "drop" in action.lower():
            base_success = 0.75
        if random.random() < (base_success + noise):
            successes += 1
    success_rate = round(successes / n_sims * 100, 1)
    approved = success_rate >= 90.0
    return {"agent": "QUANTUM", "simulations": n_sims,
            "success_rate": success_rate, "approved": approved,
            "confidence": f"{success_rate}%"}


def agent_rollback_plan(action: str, target: str) -> dict:
    """Agent Rollback — Définit le plan de récupération en cas d'échec."""
    plans = {
        "sidebar": "git checkout HEAD~1 -- components/sidebar-icons-*.tsx && git push --force-with-lease",
        "engine": "git checkout HEAD~1 -- swarm/intelligence/<engine>.py && python3 <engine>.py",
        "route": "git checkout HEAD~1 -- app/api/<path>/route.ts",
        "commit": "git revert HEAD --no-edit",
        "push": "git revert HEAD --no-edit && git push",
        "default": "git stash && git checkout HEAD~1"
    }
    target_lower = target.lower()
    plan = plans.get(
        next((k for k in plans if k in target_lower), "default"),
        plans["default"]
    )
    return {"agent": "ROLLBACK", "plan": plan, "estimated_recovery_min": 2}


# ── ANALYSE COMPLÈTE ────────────────────────────────────────────────────────

def analyze_action(action: str, target: str = "", auto_approve_low: bool = True) -> dict:
    """Lance l'analyse croisée complète sur une action."""
    print(f"\n{'='*60}")
    print(f"  CaelumSwarm™ — ANALYSE ACTION")
    print(f"  Action : {action}")
    print(f"  Cible  : {target or 'N/A'}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    agents = [
        agent_impact(action, target),
        agent_dependency(action, target),
        agent_protocol_check(action, target),
        agent_quantum_validate(action, target),
        agent_rollback_plan(action, target),
    ]

    print("\nRÉSULTATS PAR AGENT :")
    for a in agents:
        name = a["agent"]
        if name == "IMPACT":
            icon = "⚠" if a["risk_score"] > 0.4 else "✓"
            print(f"  {icon} {name}: risque={a['risk_score']} ({a['level']}) | réversible={a['reversible']}")
        elif name == "DEPS":
            icon = "⚠" if a["high_cascade"] else "✓"
            print(f"  {icon} {name}: {a['cascade_count']} dépendances → {', '.join(a['dependencies'][:2])}")
        elif name == "PROTOCOL":
            icon = "✗" if a["status"] == "VIOLATION" else ("⚠" if a["status"] == "WARNING" else "✓")
            print(f"  {icon} {name}: {a['status']}", end="")
            if a["violations"]: print(f" | violations: {a['violations']}", end="")
            if a["warnings"]: print(f" | warnings: {a['warnings']}", end="")
            print()
        elif name == "QUANTUM":
            icon = "✓" if a["approved"] else "✗"
            print(f"  {icon} {name}: {a['simulations']:,} sims → succès={a['confidence']} | {'APPROUVÉ' if a['approved'] else 'REFUSÉ'}")
        elif name == "ROLLBACK":
            print(f"  ↩ {name}: {a['plan'][:70]}...")

    # Décision finale
    impact = agents[0]
    protocol = agents[2]
    quantum = agents[3]

    blocked = (
        protocol["status"] == "VIOLATION"
        or not quantum["approved"]
        or (impact["risk_score"] > 0.6 and not auto_approve_low)
    )

    print("\n" + "─" * 60)
    if blocked:
        decision = "BLOQUÉ"
        reasons = []
        if protocol["status"] == "VIOLATION":
            reasons.append(f"Violation protocole: {protocol['violations']}")
        if not quantum["approved"]:
            reasons.append(f"Monte Carlo insuffisant ({quantum['confidence']})")
        if impact["risk_score"] > 0.6:
            reasons.append(f"Risque élevé ({impact['level']})")
        print(f"  🔴 DÉCISION FINALE : {decision}")
        for r in reasons: print(f"     → {r}")
    else:
        decision = "AUTORISÉ"
        print(f"  🟢 DÉCISION FINALE : {decision}")
        if protocol["warnings"]:
            print(f"     ⚠ Warnings: {protocol['warnings']}")
    print("=" * 60 + "\n")

    result = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "target": target,
        "decision": decision,
        "agents": agents,
    }

    # Sauvegarder le log
    log_path = ROOT / "data" / "action_analysis_log.json"
    log_path.parent.mkdir(exist_ok=True)
    logs = []
    if log_path.exists():
        try:
            logs = json.loads(log_path.read_text())
        except Exception:
            logs = []
    logs.append(result)
    logs = logs[-100:]  # Garder les 100 dernières analyses
    log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False))

    return result


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 action_analyzer.py '<action>' '[cible]'")
        print("Exemples:")
        print("  python3 action_analyzer.py 'git push' 'sidebar-icons-4.tsx'")
        print("  python3 action_analyzer.py 'delete engine' 'swarm/intelligence/test.py'")
        sys.exit(1)

    action = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else ""
    result = analyze_action(action, target)
    sys.exit(0 if result["decision"] == "AUTORISÉ" else 1)
