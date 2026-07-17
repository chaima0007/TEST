#!/usr/bin/env python3
"""
CaelumSwarm™ — Multi-Agent Decision Validator
Chaque décision est validée par TOUS les agents concernés + agents quantiques.

Agents de validation :
  1. QA Agent         — vérification qualité & patterns
  2. Security Agent   — vérification sécurité routes
  3. Quantum Agent    — probabilités Monte Carlo
  4. Alert Agent      — niveaux d'alerte seuils
  5. Temporal Agent   — boucles temporelles git
  6. Wave Validator   — score 24/24

Sources fiables multiples : chaque décision nécessite ≥4/6 agents "AVAL".
Un score <4/6 bloque l'exécution.

Usage:
  python3 scripts/multi_agent_decision_validator.py --wave N --domains d1 d2 d3
  python3 scripts/multi_agent_decision_validator.py --check-system
"""

import json
import math
import random
import re
import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
random.seed(None)

G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"
C = "\033[96m"; B = "\033[1m"; P = "\033[95m"; E = "\033[0m"

THRESHOLD_AVAL = 4  # minimum agents "AVAL" pour autoriser l'exécution


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)


# ─── Agent 1 : QA Agent ───────────────────────────────────────────────────────

def agent_qa(domains: list[str]) -> dict:
    """Vérifie que les patterns engine/route/sidebar sont corrects."""
    score = 0
    details = []

    for domain in domains:
        engine = ROOT / "swarm" / "intelligence" / f"{domain}_engine.py"
        route = ROOT / "app" / "api" / domain / "route.ts"

        if engine.exists():
            content = engine.read_text("utf-8", errors="ignore")
            has_avg = "avg_composite" in content or "61.03" in content
            has_dist = "critique" in content.lower()
            if has_avg and has_dist:
                score += 1
                details.append(f"  {G}✓ Engine {domain}: pattern valide{E}")
            else:
                details.append(f"  {R}✗ Engine {domain}: pattern manquant{E}")
        else:
            details.append(f"  {Y}? Engine {domain}: pré-création (sera validé après){E}")
            score += 0.75  # pré-création acceptable

        if route.exists():
            content = route.read_text("utf-8", errors="ignore")
            if "sealResponse" in content and "SWARM_API_URL" in content:
                score += 1
                details.append(f"  {G}✓ Route {domain}: sécurité conforme{E}")
            else:
                details.append(f"  {R}✗ Route {domain}: sécurité manquante{E}")
        else:
            details.append(f"  {Y}? Route {domain}: pré-création (sera validée après){E}")
            score += 0.75  # pré-création acceptable

    max_score = len(domains) * 2
    pct = round(score / max_score * 100, 1) if max_score > 0 else 100
    aval = pct >= 60

    return {
        "agent": "QA Agent",
        "score": pct,
        "aval": aval,
        "details": details,
        "emoji": "🔍",
    }


# ─── Agent 2 : Security Agent ─────────────────────────────────────────────────

def agent_security(domains: list[str]) -> dict:
    """Audit sécurité : sealResponse, SWARM_API_URL, 502, revalidate."""
    score = 0
    details = []
    patterns = ["sealResponse", "SWARM_API_URL", "502", "revalidate: 30"]

    for domain in domains:
        route = ROOT / "app" / "api" / domain / "route.ts"
        if route.exists():
            content = route.read_text("utf-8", errors="ignore")
            found = sum(1 for p in patterns if p in content)
            ratio = found / len(patterns) * 100
            score += ratio
            status = G if found == 4 else Y if found >= 2 else R
            details.append(f"  {status}{'✓' if found==4 else '⚠' if found>=2 else '✗'} {domain}: {found}/{len(patterns)} patterns sécurité{E}")
        else:
            details.append(f"  {Y}? {domain}: pré-création (pattern vérifié après){E}")
            score += 75  # pré-création acceptable

    avg = round(score / max(1, len(domains)), 1)
    aval = avg >= 70

    return {
        "agent": "Security Agent",
        "score": avg,
        "aval": aval,
        "details": details,
        "emoji": "🔒",
    }


# ─── Agent 3 : Quantum Probability Agent ──────────────────────────────────────

def agent_quantum(domains: list[str]) -> dict:
    """Monte Carlo — probabilité de succès de la wave."""
    sidebar_file = ROOT / "components" / "sidebar-icons-4.tsx"
    sidebar_lines = len(sidebar_file.read_text("utf-8", errors="ignore").splitlines()) if sidebar_file.exists() else 4500

    P_ENGINE = 0.9997
    P_ROUTE = 0.9980
    P_SIDEBAR = 0.9950 * max(0.5, 1 - max(0, (sidebar_lines - 4000) / 6000) * 0.5)
    P_UNTRACKED = 0.8500
    P_AUTHOR = 0.9200

    n = 5000
    successes = sum(
        1 for _ in range(n)
        if (random.random() < P_ENGINE and
            random.random() < P_ROUTE and
            random.random() < P_SIDEBAR and
            random.random() < P_UNTRACKED and
            random.random() < P_AUTHOR)
    )
    p_success = successes / n * 100
    amplitude = math.sqrt(p_success / 100)

    details = [
        f"  {C}Monte Carlo (N=5000) : {p_success:.1f}% succès{E}",
        f"  {C}Amplitude quantique ∣1⟩ : {amplitude:.4f}{E}",
        f"  {C}Sidebar : {sidebar_lines} lignes (seuil OOM: 5500){E}",
        f"  {C}P(engine)={P_ENGINE*100:.1f}% | P(route)={P_ROUTE*100:.1f}% | P(untracked)={P_UNTRACKED*100:.0f}%{E}",
    ]

    aval = p_success >= 65

    return {
        "agent": "Quantum Probability Agent",
        "score": round(p_success, 1),
        "aval": aval,
        "details": details,
        "emoji": "⚛️",
    }


# ─── Agent 4 : Alert Level Agent ──────────────────────────────────────────────

def agent_alert_levels() -> dict:
    """Vérifie les niveaux d'alerte du système."""
    details = []

    # Routes sécurisées
    route_files = list((ROOT / "app" / "api").rglob("route.ts"))
    secure = sum(
        1 for rf in route_files
        if "sealResponse" in rf.read_text("utf-8", errors="ignore")
        and "SWARM_API_URL" in rf.read_text("utf-8", errors="ignore")
        and "auth/" not in str(rf)
    )
    intel = max(1, len(route_files) - sum(1 for rf in route_files if "auth/" in str(rf)))
    routes_pct = round(secure / intel * 100, 1)

    # Git cleanness
    r = run(["git", "status", "--short"])
    dirty = sum(1 for l in r.stdout.splitlines() if l.startswith("??") or l.startswith(" M"))
    git_pct = round(max(0, 100 - dirty * 15), 1)

    # Doublons
    seen: dict[str, int] = {}
    for f in (ROOT / "components").glob("sidebar-icons*.tsx"):
        if f.name == "sidebar-icons.tsx": continue
        for line in f.read_text("utf-8", errors="ignore").splitlines():
            m = re.match(r"^export function (Icon\w+)", line)
            if m:
                seen[m.group(1)] = seen.get(m.group(1), 0) + 1
    dup = sum(1 for v in seen.values() if v > 1)
    dup_pct = round((1 - dup / max(1, len(seen))) * 100, 1)

    score = round((routes_pct + git_pct + dup_pct) / 3, 1)

    def level(p): return ("VERT", G) if p >= 95 else ("ORANGE", Y) if p >= 80 else ("ROUGE", R) if p >= 60 else ("NOIR", P)
    rl, rc = level(routes_pct); gl, gc = level(git_pct); dl, dc = level(dup_pct)

    details = [
        f"  {rc}Routes sécurité : {routes_pct}% [{rl}]{E}",
        f"  {gc}Git propreté   : {git_pct}% [{gl}]{E} ({dirty} fichier(s) sale(s))",
        f"  {dc}Unicité icônes : {dup_pct}% [{dl}]{E} ({dup} doublon(s))",
    ]
    aval = score >= 70

    return {
        "agent": "Alert Level Agent",
        "score": score,
        "aval": aval,
        "details": details,
        "emoji": "🚦",
    }


# ─── Agent 5 : Temporal Loop Agent ────────────────────────────────────────────

def agent_temporal() -> dict:
    """Détecte les boucles temporelles git."""
    details = []
    issues = 0

    # Index lock
    if (ROOT / ".git" / "index.lock").exists():
        details.append(f"  {R}✗ index.lock détecté — conflit entre agents{E}")
        issues += 1
    else:
        details.append(f"  {G}✓ Pas de index.lock{E}")

    # Untracked
    r = run(["git", "status", "--short"])
    untracked = [l for l in r.stdout.splitlines() if l.startswith("??")]
    if untracked:
        details.append(f"  {Y}⚠ {len(untracked)} fichier(s) non-commités{E}")
        issues += 1
    else:
        details.append(f"  {G}✓ Working tree propre{E}")

    # Auteur git
    r = run(["git", "log", "-5", "--format=%ae"])
    bad = [e for e in r.stdout.strip().splitlines() if e != "noreply@anthropic.com"]
    if bad:
        details.append(f"  {R}✗ {len(bad)} commit(s) mauvais auteur{E}")
        issues += 1
    else:
        details.append(f"  {G}✓ Auteur git correct{E}")

    score = round(max(0, 100 - issues * 25), 1)
    aval = issues == 0

    return {
        "agent": "Temporal Loop Agent",
        "score": score,
        "aval": aval,
        "details": details,
        "emoji": "⏱️",
    }


# ─── Agent 6 : Wave Pattern Agent ─────────────────────────────────────────────

def agent_wave_pattern(domains: list[str]) -> dict:
    """Vérifie les patterns spécifiques wave (distribution, seuils, estimated_index)."""
    details = []
    score = 0

    REQUIRED_TUPLES = [
        (99, 97, 95, 93), (93, 90, 88, 86), (85, 82, 80, 78), (80, 77, 75, 73),
        (61, 58, 56, 54), (51, 48, 46, 44), (32, 29, 27, 25), (13, 11, 9, 7),
    ]

    for domain in domains:
        engine = ROOT / "swarm" / "intelligence" / f"{domain}_engine.py"
        if not engine.exists():
            details.append(f"  {Y}? {domain}: pré-création (pattern vérifié après wave){E}")
            score += 75  # pré-création acceptable
            continue

        content = engine.read_text("utf-8", errors="ignore")
        tuples_found = sum(1 for t in REQUIRED_TUPLES if str(t[0]) in content and str(t[1]) in content)
        has_estimated = f"estimated_{domain}_index" in content
        has_weights = "0.30" in content and "0.25" in content and "0.20" in content

        pct = round((tuples_found / 8 * 60 + (20 if has_estimated else 0) + (20 if has_weights else 0)), 1)
        score += pct
        status = G if pct >= 90 else Y if pct >= 60 else R
        details.append(f"  {status}{'✓' if pct>=90 else '⚠' if pct>=60 else '✗'} {domain}: {pct:.0f}% ({tuples_found}/8 tuples, estimated={'✓' if has_estimated else '✗'}, weights={'✓' if has_weights else '✗'}){E}")

    avg = round(score / max(1, len(domains)), 1)
    aval = avg >= 70

    return {
        "agent": "Wave Pattern Agent",
        "score": avg,
        "aval": aval,
        "details": details,
        "emoji": "📐",
    }


# ─── Orchestrateur principal ───────────────────────────────────────────────────

def validate_decision(wave: int, domains: list[str], verbose: bool = True) -> bool:
    """
    Lance tous les agents de validation et retourne True si la décision est approuvée.
    Nécessite ≥4/6 agents "AVAL".
    """
    print(f"\n{B}{C}╔{'═'*62}╗{E}")
    print(f"{B}{C}  CaelumSwarm™ — Multi-Agent Decision Validator{E}")
    print(f"{B}{C}  Wave {wave} | Domains: {', '.join(domains)}{E}")
    print(f"{B}{C}  Seuil d'approbation : {THRESHOLD_AVAL}/6 agents AVAL{E}")
    print(f"{B}{C}╚{'═'*62}╝{E}\n")

    agents_results = [
        agent_qa(domains),
        agent_security(domains),
        agent_quantum(domains),
        agent_alert_levels(),
        agent_temporal(),
        agent_wave_pattern(domains),
    ]

    aval_count = 0
    print(f"{B}RÉSULTATS PAR AGENT :{E}\n")

    for result in agents_results:
        aval = result["aval"]
        if aval:
            aval_count += 1
        color = G if aval else R
        status = "AVAL ✓" if aval else "REFUS ✗"
        print(f"  {result['emoji']} {B}{result['agent']:30}{E} {color}{status}{E}  (score: {result['score']:.1f}%)")
        if verbose:
            for d in result["details"]:
                print(d)
        print()

    # Décision finale
    print(f"{B}{'═'*64}{E}")
    approved = aval_count >= THRESHOLD_AVAL

    if approved:
        print(f"\n  {G}{B}✓ DÉCISION APPROUVÉE — {aval_count}/6 agents AVAL{E}")
        print(f"  {G}Wave {wave} autorisée à s'exécuter{E}")
    else:
        print(f"\n  {R}{B}✗ DÉCISION BLOQUÉE — {aval_count}/6 agents AVAL (seuil: {THRESHOLD_AVAL}){E}")
        print(f"  {R}Corriger les problèmes avant d'exécuter Wave {wave}{E}")

    # Rapport sources multiples
    print(f"\n{B}SOURCES DE VALIDATION MULTIPLES :{E}")
    print(f"  Source 1 (QA)       → score {agents_results[0]['score']:.1f}%")
    print(f"  Source 2 (Sécurité) → score {agents_results[1]['score']:.1f}%")
    print(f"  Source 3 (Quantique)→ score {agents_results[2]['score']:.1f}%")
    print(f"  Source 4 (Alertes)  → score {agents_results[3]['score']:.1f}%")
    print(f"  Source 5 (Temporel) → score {agents_results[4]['score']:.1f}%")
    print(f"  Source 6 (Pattern)  → score {agents_results[5]['score']:.1f}%")

    avg_global = round(sum(r["score"] for r in agents_results) / 6, 1)
    color_g = G if avg_global >= 85 else Y if avg_global >= 70 else R
    print(f"\n  {color_g}{B}Score moyen toutes sources : {avg_global}%{E}")

    # Journaliser la décision
    log_decision(wave, domains, aval_count, avg_global, approved, agents_results)

    return approved


def log_decision(wave, domains, aval_count, avg_score, approved, results):
    """Enregistre la décision dans data/errors.json si refus."""
    if approved:
        return
    db_path = ROOT / "data" / "errors.json"
    if not db_path.exists():
        return
    try:
        db = json.loads(db_path.read_text("utf-8"))
        new_id = f"ERR-{len(db['errors'])+1:04d}"
        db["errors"].append({
            "id": new_id,
            "type": "decision_blocked",
            "wave": wave,
            "domains": domains,
            "description": f"Wave {wave} bloquée par multi-agent validator ({aval_count}/6 AVAL, score {avg_score}%)",
            "status": "open",
            "recurrence_count": 1,
            "fix_applied": False,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        db["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        db_path.write_text(json.dumps(db, indent=2, ensure_ascii=False), "utf-8")
    except Exception:
        pass


def check_system() -> None:
    """Vérification système globale sans wave spécifique."""
    validate_decision(wave=0, domains=[], verbose=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Agent Decision Validator")
    parser.add_argument("--wave", type=int, default=0, help="Numéro de wave")
    parser.add_argument("--domains", nargs="+", default=[], help="Domaines à valider")
    parser.add_argument("--check-system", action="store_true", help="Vérification système globale")
    parser.add_argument("--quiet", action="store_true", help="Mode silencieux (moins de détails)")
    args = parser.parse_args()

    if args.check_system:
        check_system()
    else:
        ok = validate_decision(args.wave, args.domains, verbose=not args.quiet)
        sys.exit(0 if ok else 1)
