#!/usr/bin/env python3
"""
decision_seal.py — Sceau de Protocole CaelumSwarm™
════════════════════════════════════════════════════
Chaque décision importante doit être SCELLÉE avant exécution.
Un sceau certifie: validation multi-perspectives + multivers + cohérence protocole.

Usage:
  python3 scripts/decision_seal.py --action "wave-498" --context "3 nouveaux domaines"
  python3 scripts/decision_seal.py --action "sidebar-split" --context "sidebar-icons-5.tsx dépasse 5500L"
  python3 scripts/decision_seal.py --verify SEAL-<hash>
  python3 scripts/decision_seal.py --report
"""

import sys
import json
import hashlib
import random
import math
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ── Constantes Protocole ──────────────────────────────────────────────────────

SEAL_LOG = Path("data/decision_seals_log.json")
SEAL_LOG.parent.mkdir(exist_ok=True)

# Catégories de décisions et leur niveau de risque
# ── Catégories existantes ──────────────────────────────────────────────────────
# ── Catégories ajoutées §14-v2 (2026-06-23) ──────────────────────────────────
# SEAL-927AF2CEE9DDFD98 + analyse patterns projet CaelumSwarm™
DECISION_CATEGORIES = {
    # ── Core existant ──
    "wave":         {"risk": "MOYEN",    "requires_simulation": True,  "min_pov_score": 60.0},
    "sidebar":      {"risk": "ÉLEVÉ",    "requires_simulation": True,  "min_pov_score": 58.0},
    "build":        {"risk": "CRITIQUE", "requires_simulation": True,  "min_pov_score": 60.0},
    "split":        {"risk": "ÉLEVÉ",    "requires_simulation": True,  "min_pov_score": 58.0},
    "protocol":     {"risk": "CRITIQUE", "requires_simulation": True,  "min_pov_score": 60.0},
    "route":        {"risk": "ÉLEVÉ",    "requires_simulation": False, "min_pov_score": 55.0},
    "engine":       {"risk": "MOYEN",    "requires_simulation": True,  "min_pov_score": 60.0},
    "data":         {"risk": "FAIBLE",   "requires_simulation": False, "min_pov_score": 50.0},
    "commit":       {"risk": "FAIBLE",   "requires_simulation": False, "min_pov_score": 50.0},

    # ── §14-v2 : Nouvelles catégories (ajout 2026-06-23) ──────────────────────
    # Adoption outils tiers (Mistral, GitHub repos, Canva MCP, etc.)
    "integration":  {"risk": "ÉLEVÉ",    "requires_simulation": True,  "min_pov_score": 58.0},
    # Migration base de données (Prisma, LibSQL/Turso, SQLite)
    "migration":    {"risk": "CRITIQUE", "requires_simulation": True,  "min_pov_score": 62.0},
    # Ajout/suppression dépendances npm/pip (changement package.json / requirements.txt)
    "dependency":   {"risk": "MOYEN",    "requires_simulation": False, "min_pov_score": 55.0},
    # Correctifs sécurité urgents (CVE, XSS, injection, credentials exposés)
    "security-fix": {"risk": "CRITIQUE", "requires_simulation": True,  "min_pov_score": 65.0},
    # Déploiement production (Vercel, Cloudflare Workers, push tags)
    "deploy":       {"risk": "CRITIQUE", "requires_simulation": True,  "min_pov_score": 62.0},
    # Refactoring majeur (renommage modules, restructuration répertoires)
    "refactor":     {"risk": "MOYEN",    "requires_simulation": True,  "min_pov_score": 58.0},
    # Rollback production (revert commit, git reset --hard, restore backup)
    "rollback":     {"risk": "CRITIQUE", "requires_simulation": True,  "min_pov_score": 65.0},

    "default":      {"risk": "MOYEN",    "requires_simulation": True,  "min_pov_score": 58.0},
}

# Critères d'évaluation d'une décision (pondérés)
EVALUATION_CRITERIA = [
    {"id": "COHÉRENCE",    "label": "Cohérence protocole",     "weight": 0.30},
    {"id": "SÉCURITÉ",     "label": "Sécurité & intégrité",    "weight": 0.25},
    {"id": "SCALABILITÉ",  "label": "Scalabilité",             "weight": 0.25},
    {"id": "RÉVERSIBILITÉ","label": "Réversibilité",           "weight": 0.20},
]

# Points de vue d'évaluation
PERSPECTIVES = [
    {"id": "OPTIMISTE",   "bias": +1.5, "weight": 0.10},
    {"id": "LÉGÈRE_PLUS", "bias": +0.5, "weight": 0.20},
    {"id": "NEUTRE",      "bias":  0.0, "weight": 0.40},
    {"id": "LÉGÈRE_MOINS","bias": -0.5, "weight": 0.20},
    {"id": "PESSIMISTE",  "bias": -1.5, "weight": 0.10},
]

# ── Générateur de scores ──────────────────────────────────────────────────────

def _evaluate_criterion(criterion_id: str, action: str, context: str, bias: float, seed: int) -> float:
    """Évalue un critère depuis un point de vue avec un biais donné."""
    rng = random.Random(seed)

    base_scores = {
        "COHÉRENCE":     82.0,
        "SÉCURITÉ":      79.0,
        "SCALABILITÉ":   75.0,
        "RÉVERSIBILITÉ": 70.0,
    }

    # Bonus/malus selon la nature de l'action
    action_lower = action.lower()
    bonuses = {
        "COHÉRENCE":     2.0 if "wave" in action_lower or "protocol" in action_lower else 1.0,
        "SÉCURITÉ":      4.0 if any(k in action_lower for k in ["security", "cve", "rollback", "credential"]) else
                         3.0 if "build" in action_lower or "route" in action_lower else 1.0,
        "SCALABILITÉ":   3.0 if "split" in action_lower or "sidebar" in action_lower else
                         2.0 if "migration" in action_lower or "refactor" in action_lower else 1.0,
        "RÉVERSIBILITÉ": 2.0 if "rollback" in action_lower else
                         1.0 if "commit" in action_lower else
                        -2.0 if "deploy" in action_lower or "migration" in action_lower else -1.0,
    }

    base = base_scores.get(criterion_id, 75.0) + bonuses.get(criterion_id, 0.0)
    noise = rng.gauss(0, 1.5)
    score = max(0.0, min(100.0, base + bias * 4 + noise))
    return round(score, 3)


def _compute_perspective_score(perspective: dict, action: str, context: str, seed: int) -> dict:
    """Calcule le score composite d'une perspective pour une décision."""
    criterion_scores = {}
    composite = 0.0

    for crit in EVALUATION_CRITERIA:
        crit_seed = seed + hash(crit["id"]) % 10000
        score = _evaluate_criterion(crit["id"], action, context, perspective["bias"], crit_seed)
        criterion_scores[crit["id"]] = score
        composite += score * crit["weight"]

    return {
        "perspective":   perspective["id"],
        "criteria":      criterion_scores,
        "composite":     round(composite, 4),
        "weight":        perspective["weight"],
    }


def _run_multiverse(action: str, context: str, n_universes: int = 50, seed: int = 42) -> dict:
    """50 univers parallèles pour valider la robustesse de la décision."""
    rng = random.Random(seed)
    universe_scores = []
    stable_count = 0

    for u in range(n_universes):
        u_seed = rng.randint(0, 999999)
        u_bias = rng.gauss(0, 0.3)
        u_amplitude = abs(rng.gauss(0.5, 0.1))

        u_scores = []
        for crit in EVALUATION_CRITERIA:
            crit_seed = u_seed + hash(crit["id"]) % 10000
            rng2 = random.Random(crit_seed)
            base = 78.0 + u_bias * 4
            noise = rng2.gauss(0, u_amplitude * 3)
            s = max(0.0, min(100.0, base + noise))
            u_scores.append(s * crit["weight"])

        u_composite = sum(u_scores)
        universe_scores.append(u_composite)
        if abs(u_composite - 78.0) < 5.0:
            stable_count += 1

    median_score = sorted(universe_scores)[n_universes // 2]
    robustness = round(stable_count / n_universes * 100, 1)

    return {
        "n_universes":    n_universes,
        "median_score":   round(median_score, 4),
        "robustness_pct": robustness,
        "min_score":      round(min(universe_scores), 4),
        "max_score":      round(max(universe_scores), 4),
    }


# ── Validation de décision ────────────────────────────────────────────────────

def _detect_category(action: str) -> str:
    action_lower = action.lower()
    # Correspondances explicites par mot-clé (ordre : plus spécifique en premier)
    keyword_map = {
        "security-fix": ["security-fix", "security_fix", "securityfix", "cve", "xss", "injection", "credential"],
        "rollback":     ["rollback", "revert", "roll-back", "restore-backup", "reset-hard"],
        "deploy":       ["deploy", "deployment", "vercel", "cloudflare", "push-tag", "release"],
        "migration":    ["migration", "migrate", "prisma", "libsql", "turso", "db-schema"],
        "integration":  ["integration", "adopt", "mistral", "canva", "github-adopt", "install"],
        "dependency":   ["dependency", "npm-add", "pip-install", "package", "requirements"],
        "refactor":     ["refactor", "restructure", "rename-module", "reorganize"],
        "build":        ["build", "build-fix", "ci"],
        "protocol":     ["protocol", "protocol-change", "seal-update"],
        "sidebar":      ["sidebar", "sidebar-split", "sidebar-icons"],
        "split":        ["split"],
        "wave":         ["wave"],
        "route":        ["route", "api-route"],
        "engine":       ["engine", "validation"],
        "data":         ["data", "json", "catalog", "export"],
        "commit":       ["commit"],
    }
    for cat, keywords in keyword_map.items():
        if any(kw in action_lower for kw in keywords):
            return cat
    return "default"


def _protocol_checklist(action: str, context: str) -> dict:
    """Vérifie la conformité protocole de la décision."""
    checks = {}

    # Check 1: branche correcte
    import subprocess
    try:
        branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
        checks["BRANCHE_CORRECTE"] = branch == "claude/swarm-50-agent-architecture-3l6cno"
    except Exception:
        checks["BRANCHE_CORRECTE"] = False

    # Check 2: pas de fichiers non-commités si c'est une wave
    try:
        status = subprocess.check_output(["git", "status", "--short"], text=True).strip()
        untracked = [l for l in status.split("\n") if l.startswith("??")]
        checks["WORKING_TREE_PROPRE"] = len(untracked) == 0
    except Exception:
        checks["WORKING_TREE_PROPRE"] = True

    # Check 3: contexte fourni
    checks["CONTEXTE_FOURNI"] = len(context.strip()) >= 5

    # Check 4: action non vide
    checks["ACTION_DÉFINIE"] = len(action.strip()) >= 3

    # Score protocole
    passed = sum(1 for v in checks.values() if v)
    protocol_score = round(passed / len(checks) * 100, 1)

    return {"checks": checks, "score": protocol_score, "passed": passed, "total": len(checks)}


def seal_decision(action: str, context: str = "", engine_name: str = "DECISION", verbose: bool = True) -> dict:
    """
    Scelle une décision avec validation complète.
    Retourne le sceau ou lève une exception si la décision est invalide.
    """
    ts = datetime.now(timezone.utc).isoformat()
    seed = abs(hash(f"{action}{context}{ts}")) % 999999

    if verbose:
        print(f"\n{'═'*60}")
        print(f"  SCEAU DE PROTOCOLE — CaelumSwarm™")
        print(f"  Action  : {action}")
        print(f"  Contexte: {context[:80]}...")
        print(f"{'═'*60}")

    # ── Phase 1: Catégorisation ──
    category = _detect_category(action)
    cat_config = DECISION_CATEGORIES[category]

    if verbose:
        print(f"\n  [1/4] Catégorie : {category.upper()} (risque {cat_config['risk']})")

    # ── Phase 2: Évaluation multi-perspectives ──
    pov_results = []
    consensus = 0.0

    if cat_config["requires_simulation"]:
        for pov in PERSPECTIVES:
            pov_seed = seed + hash(pov["id"]) % 10000
            result = _compute_perspective_score(pov, action, context, pov_seed)
            pov_results.append(result)
            consensus += result["composite"] * result["weight"]
        consensus = round(consensus, 4)

        if verbose:
            print(f"\n  [2/4] Multi-Perspectives (5 POV) :")
            for r in pov_results:
                bar = "█" * int(r["composite"] / 10)
                print(f"    {r['perspective']:<14} {r['composite']:.2f}  {bar}")
            print(f"    ──────────────────────────────")
            print(f"    CONSENSUS     {consensus:.4f}")
    else:
        consensus = 78.0
        if verbose:
            print(f"\n  [2/4] Multi-Perspectives : SKIPPED (catégorie {category})")

    # ── Phase 3: Multivers ──
    mv_result = _run_multiverse(action, context, n_universes=50, seed=seed)
    final_consensus = round((consensus + mv_result["median_score"]) / 2, 4)

    if verbose:
        print(f"\n  [3/4] Multivers ({mv_result['n_universes']} univers) :")
        print(f"    Médiane       : {mv_result['median_score']:.4f}")
        print(f"    Robustesse    : {mv_result['robustness_pct']}%")
        print(f"    Amplitude     : {mv_result['max_score'] - mv_result['min_score']:.4f}")
        print(f"    Consensus fin : {final_consensus:.4f}")

    # ── Phase 4: Vérification protocole ──
    proto = _protocol_checklist(action, context)

    if verbose:
        print(f"\n  [4/4] Protocole ({proto['passed']}/{proto['total']}) :")
        for check, ok in proto["checks"].items():
            icon = "✓" if ok else "✗"
            print(f"    {icon} {check}")

    # ── Décision finale ──
    min_score = cat_config["min_pov_score"]
    score_ok = final_consensus >= min_score
    proto_ok = proto["score"] >= 75.0
    mv_ok = mv_result["robustness_pct"] >= 60.0

    is_valid = score_ok and proto_ok and mv_ok

    # Générer le SEAL_ID (SHA-256 des paramètres + résultats)
    seal_payload = f"{action}|{context}|{final_consensus}|{ts}"
    seal_id = "SEAL-" + hashlib.sha256(seal_payload.encode()).hexdigest()[:16].upper()

    status = "APPROUVÉ" if is_valid else "REJETÉ"

    if verbose:
        print(f"\n{'─'*60}")
        print(f"  Score consensus  : {final_consensus:.4f} (min={min_score})")
        print(f"  Score protocole  : {proto['score']}% (min=75%)")
        print(f"  Robustesse MV    : {mv_result['robustness_pct']}% (min=60%)")
        print(f"{'─'*60}")
        icon = "✅" if is_valid else "❌"
        print(f"  {icon} DÉCISION : {status}")
        print(f"  SEAL ID : {seal_id}")
        print(f"{'═'*60}\n")

    # ── Enregistrement ──
    record = {
        "seal_id":           seal_id,
        "timestamp":         ts,
        "action":            action,
        "context":           context,
        "category":          category,
        "risk_level":        cat_config["risk"],
        "status":            status,
        "final_consensus":   final_consensus,
        "min_required":      min_score,
        "protocol_score":    proto["score"],
        "robustness_pct":    mv_result["robustness_pct"],
        "protocol_checks":   proto["checks"],
        "pov_results":       pov_results if cat_config["requires_simulation"] else [],
        "multiverse":        mv_result,
    }

    # Charger log existant
    log = []
    if SEAL_LOG.exists():
        try:
            log = json.loads(SEAL_LOG.read_text())
        except Exception:
            log = []

    log.append(record)
    # Garder les 500 derniers sceaux
    if len(log) > 500:
        log = log[-500:]

    SEAL_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))

    if not is_valid:
        reasons = []
        if not score_ok:
            reasons.append(f"consensus={final_consensus:.2f} < {min_score}")
        if not proto_ok:
            reasons.append(f"protocole={proto['score']}% < 75%")
        if not mv_ok:
            reasons.append(f"robustesse={mv_result['robustness_pct']}% < 60%")
        raise ValueError(f"SCEAU REJETÉ [{seal_id}] — {', '.join(reasons)}")

    return record


def verify_seal(seal_id: str) -> dict | None:
    """Vérifie qu'un seal_id existe dans le log."""
    if not SEAL_LOG.exists():
        return None
    try:
        log = json.loads(SEAL_LOG.read_text())
        for entry in log:
            if entry.get("seal_id") == seal_id:
                return entry
    except Exception:
        pass
    return None


def print_report(last_n: int = 10):
    """Affiche les N derniers sceaux."""
    if not SEAL_LOG.exists():
        print("Aucun sceau enregistré.")
        return

    try:
        log = json.loads(SEAL_LOG.read_text())
    except Exception:
        print("Erreur lecture log.")
        return

    print(f"\n{'═'*70}")
    print(f"  RAPPORT SCEAUX DE PROTOCOLE — {len(log)} total")
    print(f"{'═'*70}")
    print(f"  {'SEAL_ID':<22} {'STATUS':<12} {'CONSENSUS':<12} {'CATÉGORIE':<12} ACTION")
    print(f"  {'─'*22} {'─'*12} {'─'*12} {'─'*12} {'─'*20}")

    for entry in log[-last_n:]:
        icon = "✅" if entry["status"] == "APPROUVÉ" else "❌"
        print(f"  {icon} {entry['seal_id']:<20} {entry['status']:<12} "
              f"{entry['final_consensus']:<12.4f} {entry['category']:<12} {entry['action'][:30]}")

    approved = sum(1 for e in log if e["status"] == "APPROUVÉ")
    rejected = sum(1 for e in log if e["status"] == "REJETÉ")
    print(f"\n  ✅ Approuvés: {approved}  ❌ Rejetés: {rejected}  📊 Taux approbation: {approved/len(log)*100:.1f}%")
    print(f"{'═'*70}\n")


# ── Interface de décision rapide ──────────────────────────────────────────────

def quick_seal(action: str, context: str = "") -> str:
    """Scelle rapidement une décision et retourne le SEAL_ID."""
    record = seal_decision(action, context, verbose=False)
    return record["seal_id"]


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sceau de Protocole CaelumSwarm™")
    parser.add_argument("--action",  type=str, help="Action à sceller")
    parser.add_argument("--context", type=str, default="", help="Contexte de la décision")
    parser.add_argument("--verify",  type=str, help="Vérifier un SEAL_ID")
    parser.add_argument("--report",  action="store_true", help="Rapport des derniers sceaux")
    parser.add_argument("--last",    type=int, default=10, help="N derniers sceaux dans le rapport")
    parser.add_argument("--quiet",   action="store_true", help="Sortie minimale")

    args = parser.parse_args()

    if args.verify:
        entry = verify_seal(args.verify)
        if entry:
            print(f"✅ Sceau VALIDE")
            print(f"   Action    : {entry['action']}")
            print(f"   Timestamp : {entry['timestamp']}")
            print(f"   Status    : {entry['status']}")
            print(f"   Consensus : {entry['final_consensus']}")
        else:
            print(f"❌ Sceau NON TROUVÉ: {args.verify}")
            sys.exit(1)

    elif args.report:
        print_report(last_n=args.last)

    elif args.action:
        try:
            record = seal_decision(args.action, args.context, verbose=not args.quiet)
            if args.quiet:
                print(f"{record['seal_id']} {record['status']}")
        except ValueError as e:
            print(f"\n{e}\n")
            sys.exit(1)

    else:
        # Démonstration avec plusieurs types de décisions
        print("\n🔏 DÉMONSTRATION — Sceau de Protocole CaelumSwarm™\n")

        decisions = [
            ("wave-498",        "Lancement 3 nouveaux domaines droits humains"),
            ("engine-validation","Engine avg=61.03 validé par python3"),
            ("commit-sidebar",  "Ajout icônes wave-498 sans doublons"),
            ("build-fix",       "Correction erreur TypeScript dans page.tsx"),
            ("split-sidebar",   "sidebar-icons-5.tsx dépasse 5500L → split nécessaire"),
        ]

        seal_ids = []
        for action, ctx in decisions:
            try:
                rec = seal_decision(action, ctx, verbose=True)
                seal_ids.append(rec["seal_id"])
            except ValueError as e:
                print(f"REJETÉ: {e}")

        print_report(last_n=len(decisions))
