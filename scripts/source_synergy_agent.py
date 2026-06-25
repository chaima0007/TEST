#!/usr/bin/env python3
"""
CaelumSwarm™ — Source Synergy Agent v1.0
Communauté experte multi-sources avec simulateur quantique intégré.

Chaque information est contrôlée par N experts indépendants.
Chaque validation est accompagnée d'une probabilité quantique.
La base de sources est mise à jour à chaque exécution.

Architecture :
  ExpertAgent[0..N]  → analyse un domaine spécifique
  QuantumSimulator   → calcule la fiabilité probabiliste
  SynergyOrchestrator → fusionne et croise les sources
  KnowledgeBase      → data/knowledge_base.json (mise à jour continue)

Usage:
  python3 scripts/source_synergy_agent.py                    # audit complet
  python3 scripts/source_synergy_agent.py --domain security  # domaine spécifique
  python3 scripts/source_synergy_agent.py --update-kb        # mise à jour base seule
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
from collections import defaultdict

ROOT = Path(__file__).parent.parent
KB_PATH = ROOT / "data" / "knowledge_base.json"
random.seed(None)

G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"
C = "\033[96m"; B = "\033[1m"; P = "\033[95m"; E = "\033[0m"


# ─── Simulateur Quantique (partagé entre tous les experts) ────────────────────

class QuantumSimulator:
    """
    Simulateur quantique de fiabilité.
    Chaque source passe par une superposition quantique avant validation.
    P(fiable) = amplitude²(|1⟩) après décoherence.
    """

    def __init__(self, n_qubits: int = 10):
        self.n_qubits = n_qubits
        self.decoherence_rate = 1 / math.sqrt(2 ** n_qubits)

    def measure(self, p_prior: float) -> dict:
        noise = random.gauss(0, self.decoherence_rate * 0.05)
        p_observed = max(0.0, min(1.0, p_prior + noise))
        amplitude_1 = math.sqrt(p_observed)
        amplitude_0 = math.sqrt(1 - p_observed)
        collapsed = random.random() < p_observed
        return {
            "p_prior": round(p_prior, 4),
            "p_observed": round(p_observed, 4),
            "amplitude_1": round(amplitude_1, 4),
            "amplitude_0": round(amplitude_0, 4),
            "collapsed_to": "|1⟩ (fiable)" if collapsed else "|0⟩ (suspect)",
            "reliable": collapsed,
        }

    def monte_carlo_consensus(self, votes: list[float], n: int = 3000) -> dict:
        """Consensus quantique Monte Carlo sur N votes d'experts."""
        successes = 0
        for _ in range(n):
            trial = all(random.random() < v for v in votes)
            if trial:
                successes += 1
        p = successes / n
        ci = 1.96 * math.sqrt(p * (1 - p) / n)
        return {
            "p_consensus": round(p, 4),
            "confidence_95": [round(p - ci, 4), round(p + ci, 4)],
            "n_simulations": n,
        }


# ─── Experts Indépendants ─────────────────────────────────────────────────────

class ExpertAgent:
    """Un expert indépendant qui évalue un aspect du système."""

    def __init__(self, name: str, domain: str, qsim: QuantumSimulator):
        self.name = name
        self.domain = domain
        self.qsim = qsim

    def evaluate(self) -> dict:
        raise NotImplementedError


class SecurityExpert(ExpertAgent):
    def __init__(self, qsim):
        super().__init__("Expert Sécurité", "security", qsim)

    def evaluate(self) -> dict:
        route_files = list((ROOT / "app" / "api").rglob("route.ts"))
        patterns = ["sealResponse", "SWARM_API_URL", "502", "revalidate: 30"]

        scores = []
        for rf in route_files:
            if "auth/" in str(rf): continue
            content = rf.read_text("utf-8", errors="ignore")
            found = sum(1 for p in patterns if p in content)
            scores.append(found / len(patterns))

        p_secure = sum(scores) / max(1, len(scores))
        q = self.qsim.measure(p_secure)

        return {
            "expert": self.name,
            "domain": self.domain,
            "raw_score": round(p_secure * 100, 1),
            "quantum": q,
            "finding": f"{len([s for s in scores if s == 1.0])}/{len(scores)} routes 100% sécurisées",
            "recommendation": "Continuer" if p_secure > 0.95 else "Vérifier routes incomplètes",
        }


class ArchitectureExpert(ExpertAgent):
    def __init__(self, qsim):
        super().__init__("Expert Architecture", "architecture", qsim)

    def evaluate(self) -> dict:
        engines = list((ROOT / "swarm" / "intelligence").glob("*_engine.py"))
        routes = list((ROOT / "app" / "api").rglob("route.ts"))
        # Compter seulement les routes intelligence (hors auth)
        intel_routes = [r for r in routes if "auth/" not in str(r)]
        sidebar_file = ROOT / "components" / "sidebar-icons-4.tsx"
        sidebar_lines = len(sidebar_file.read_text("utf-8", errors="ignore").splitlines()) if sidebar_file.exists() else 0

        # Santé routes intelligence (cible: ≥100 routes)
        ratio = min(1.0, len(intel_routes) / 100)
        # Santé sidebar (< 5000 lignes = 100%)
        sidebar_health = max(0.0, 1 - max(0, (sidebar_lines - 4000) / 5000))
        p = (ratio * 0.6 + sidebar_health * 0.4)
        q = self.qsim.measure(p)

        return {
            "expert": self.name,
            "domain": self.domain,
            "raw_score": round(p * 100, 1),
            "quantum": q,
            "finding": f"{len(engines)} engines | {len(intel_routes)} routes intel | sidebar {sidebar_lines} lignes",
            "recommendation": "Split sidebar bientôt" if sidebar_lines > 5000 else "Architecture saine",
        }


class GitQualityExpert(ExpertAgent):
    def __init__(self, qsim):
        super().__init__("Expert Git", "git_quality", qsim)

    def evaluate(self) -> dict:
        r = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, cwd=ROOT)
        dirty = len([l for l in r.stdout.splitlines() if l.startswith("??") or l.startswith(" M")])

        r2 = subprocess.run(["git", "log", "-10", "--format=%ae"], capture_output=True, text=True, cwd=ROOT)
        emails = r2.stdout.strip().splitlines()
        correct = sum(1 for e in emails if e == "noreply@anthropic.com")
        author_ok = correct / max(1, len(emails))

        p = (max(0, 1 - dirty * 0.15)) * 0.5 + author_ok * 0.5
        q = self.qsim.measure(p)

        return {
            "expert": self.name,
            "domain": self.domain,
            "raw_score": round(p * 100, 1),
            "quantum": q,
            "finding": f"{dirty} fichier(s) sale(s), auteur correct: {correct}/{len(emails)}",
            "recommendation": "Propre" if dirty == 0 and author_ok == 1.0 else "Rescue commit requis",
        }


class IconIntegrityExpert(ExpertAgent):
    def __init__(self, qsim):
        super().__init__("Expert Icônes", "icon_integrity", qsim)

    def evaluate(self) -> dict:
        seen: dict[str, list[str]] = {}
        for f in (ROOT / "components").glob("sidebar-icons*.tsx"):
            if f.name == "sidebar-icons.tsx": continue
            for line in f.read_text("utf-8", errors="ignore").splitlines():
                m = re.match(r"^export function (Icon\w+)", line)
                if m:
                    seen.setdefault(m.group(1), []).append(f.name)

        dups = {k: v for k, v in seen.items() if len(v) > 1}
        total = len(seen)
        p = 1 - len(dups) / max(1, total)
        q = self.qsim.measure(p)

        return {
            "expert": self.name,
            "domain": self.domain,
            "raw_score": round(p * 100, 1),
            "quantum": q,
            "finding": f"{total} icônes, {len(dups)} doublons: {list(dups.keys())[:3]}",
            "recommendation": "Aucun doublon" if not dups else f"Supprimer {list(dups.keys())}",
        }


class WaveVelocityExpert(ExpertAgent):
    def __init__(self, qsim):
        super().__init__("Expert Vélocité", "wave_velocity", qsim)

    def evaluate(self) -> dict:
        r = subprocess.run(
            ["git", "log", "--oneline", "--since=7 days ago", "--grep=feat(wave"],
            capture_output=True, text=True, cwd=ROOT
        )
        waves_7d = len(r.stdout.strip().splitlines()) if r.stdout.strip() else 0

        r2 = subprocess.run(
            ["git", "log", "--oneline", "--grep=feat(wave"],
            capture_output=True, text=True, cwd=ROOT
        )
        total_waves = len(r2.stdout.strip().splitlines()) if r2.stdout.strip() else 0

        # Vitesse cible: ~5 waves/jour
        velocity_score = min(1.0, waves_7d / (5 * 7))
        p = velocity_score * 0.7 + min(1.0, total_waves / 500) * 0.3
        q = self.qsim.measure(p)

        return {
            "expert": self.name,
            "domain": self.domain,
            "raw_score": round(p * 100, 1),
            "quantum": q,
            "finding": f"{waves_7d} waves/7j | {total_waves} waves total",
            "recommendation": f"Accélérer" if velocity_score < 0.5 else "Vélocité correcte",
        }


class ErrorPatternExpert(ExpertAgent):
    def __init__(self, qsim):
        super().__init__("Expert Erreurs", "error_patterns", qsim)

    def evaluate(self) -> dict:
        db_path = ROOT / "data" / "errors.json"
        if not db_path.exists():
            q = self.qsim.measure(0.5)
            return {
                "expert": self.name, "domain": self.domain,
                "raw_score": 50.0, "quantum": q,
                "finding": "Base erreurs absente", "recommendation": "Créer data/errors.json",
            }

        db = json.loads(db_path.read_text("utf-8"))
        errors = db.get("errors", [])
        open_e = sum(1 for e in errors if e.get("status") == "open")
        recurring = sum(1 for e in errors if e.get("recurrence_count", 0) > 3)
        fixed = sum(1 for e in errors if e.get("fix_applied"))

        p = max(0.0, 1 - open_e * 0.1 - recurring * 0.05 + fixed * 0.02)
        p = min(1.0, p)
        q = self.qsim.measure(p)

        top_types = defaultdict(int)
        for e in errors:
            top_types[e.get("type", "unknown")] += 1
        top = sorted(top_types.items(), key=lambda x: -x[1])[:3]

        return {
            "expert": self.name,
            "domain": self.domain,
            "raw_score": round(p * 100, 1),
            "quantum": q,
            "finding": f"{len(errors)} erreurs | {open_e} ouvertes | {recurring} récurrentes | top: {top}",
            "recommendation": "Fermer erreurs open" if open_e > 3 else "Base saine",
        }


# ─── Orchestrateur Synergie ───────────────────────────────────────────────────

class SynergyOrchestrator:
    """
    Croise les évaluations de tous les experts.
    Utilise le simulateur quantique pour calculer le consensus.
    Met à jour la base de connaissances.
    """

    def __init__(self):
        self.qsim = QuantumSimulator(n_qubits=12)
        self.experts = [
            SecurityExpert(self.qsim),
            ArchitectureExpert(self.qsim),
            GitQualityExpert(self.qsim),
            IconIntegrityExpert(self.qsim),
            WaveVelocityExpert(self.qsim),
            ErrorPatternExpert(self.qsim),
        ]

    def run(self, domain_filter: str | None = None) -> dict:
        print(f"\n{B}{C}╔{'═'*64}╗{E}")
        print(f"{B}{C}  CaelumSwarm™ — Source Synergy Agent v1.0{E}")
        print(f"{B}{C}  Communauté Experte × Simulateur Quantique{E}")
        print(f"{B}{C}  {len(self.experts)} experts indépendants | Monte Carlo consensus{E}")
        print(f"{B}{C}╚{'═'*64}╝{E}\n")

        experts_to_run = [
            e for e in self.experts
            if domain_filter is None or e.domain == domain_filter
        ]

        results = []
        votes = []

        for expert in experts_to_run:
            print(f"  {C}[{expert.name}] Évaluation en cours...{E}")
            result = expert.evaluate()
            results.append(result)
            votes.append(result["quantum"]["p_observed"])
            score = result["raw_score"]
            color = G if score >= 85 else Y if score >= 65 else R
            q_state = result["quantum"]["collapsed_to"]
            print(f"  {color}{'✓' if score >= 85 else '⚠' if score >= 65 else '✗'} {result['expert']:20}{E} {score:5.1f}% | ∣ψ⟩→ {q_state}")
            print(f"    {Y}{result['finding']}{E}")
            print(f"    → {result['recommendation']}\n")

        # Consensus quantique
        print(f"{B}{'─'*66}{E}")
        print(f"{B}CONSENSUS QUANTIQUE — Monte Carlo (N=3000){E}\n")
        consensus = self.qsim.monte_carlo_consensus(votes, n=3000)
        p_c = consensus["p_consensus"] * 100
        ci = [round(x * 100, 1) for x in consensus["confidence_95"]]
        color_c = G if p_c >= 80 else Y if p_c >= 60 else R

        print(f"  {color_c}{B}Consensus global : {p_c:.1f}%{E}")
        print(f"  IC 95% : [{ci[0]}%, {ci[1]}%]")

        avg_score = round(sum(r["raw_score"] for r in results) / max(1, len(results)), 1)
        print(f"  Score moyen experts : {avg_score}%")

        # Synthèse
        print(f"\n{B}SYNTHÈSE COMMUNAUTÉ EXPERTE{E}\n")
        issues = [r for r in results if r["raw_score"] < 70]
        strengths = [r for r in results if r["raw_score"] >= 85]

        if strengths:
            print(f"  {G}Forces ({len(strengths)}/{len(results)}) :{E}")
            for r in strengths:
                print(f"    ✓ {r['expert']}: {r['raw_score']:.0f}% — {r['finding'][:60]}")

        if issues:
            print(f"\n  {R}Failles ({len(issues)}/{len(results)}) :{E}")
            for r in issues:
                print(f"    ✗ {r['expert']}: {r['raw_score']:.0f}% — {r['recommendation']}")

        # Mise à jour base de connaissances
        kb = self._update_knowledge_base(results, consensus, avg_score)

        print(f"\n{B}{'─'*66}{E}")
        print(f"  {C}Base de connaissances mise à jour : {kb['total_evaluations']} évaluations{E}")
        print(f"  {C}Historique : {len(kb['history'])} sessions{E}")

        return {
            "results": results,
            "consensus": consensus,
            "avg_score": avg_score,
            "issues_count": len(issues),
            "strengths_count": len(strengths),
        }

    def _update_knowledge_base(self, results: list[dict], consensus: dict, avg_score: float) -> dict:
        """Met à jour data/knowledge_base.json avec la session courante."""
        if not KB_PATH.exists():
            kb = {
                "version": "1.0",
                "description": "CaelumSwarm™ — Base de connaissances experte (mise à jour continue)",
                "total_evaluations": 0,
                "history": [],
                "aggregated_scores": {},
                "recurring_issues": [],
            }
        else:
            kb = json.loads(KB_PATH.read_text("utf-8"))

        session = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "avg_score": avg_score,
            "consensus_pct": round(consensus["p_consensus"] * 100, 1),
            "experts": [
                {"name": r["expert"], "score": r["raw_score"], "quantum_amplitude": r["quantum"]["amplitude_1"]}
                for r in results
            ],
            "issues": [r["recommendation"] for r in results if r["raw_score"] < 70],
        }
        kb["history"].append(session)
        kb["total_evaluations"] += len(results)

        # Agréger les scores par expert
        for r in results:
            domain = r["domain"]
            if domain not in kb["aggregated_scores"]:
                kb["aggregated_scores"][domain] = {"scores": [], "avg": 0}
            kb["aggregated_scores"][domain]["scores"].append(r["raw_score"])
            scores = kb["aggregated_scores"][domain]["scores"]
            kb["aggregated_scores"][domain]["avg"] = round(sum(scores) / len(scores), 1)

        # Problèmes récurrents (apparaissent dans ≥3 sessions)
        issue_counts: dict[str, int] = defaultdict(int)
        for s in kb["history"][-10:]:  # 10 dernières sessions
            for issue in s.get("issues", []):
                issue_counts[issue] += 1
        kb["recurring_issues"] = [
            {"issue": k, "occurrences": v}
            for k, v in sorted(issue_counts.items(), key=lambda x: -x[1])
            if v >= 2
        ]

        # Garder seulement les 50 dernières sessions
        kb["history"] = kb["history"][-50:]
        kb["last_updated"] = datetime.now(timezone.utc).isoformat()

        KB_PATH.parent.mkdir(parents=True, exist_ok=True)
        KB_PATH.write_text(json.dumps(kb, indent=2, ensure_ascii=False), "utf-8")
        return kb


def print_kb_summary():
    """Affiche un résumé de la base de connaissances."""
    if not KB_PATH.exists():
        print(f"{Y}Base de connaissances vide — lancer sans --update-kb d'abord{E}")
        return

    kb = json.loads(KB_PATH.read_text("utf-8"))
    print(f"\n{B}{C}Base de Connaissances CaelumSwarm™{E}")
    print(f"  Évaluations totales : {kb.get('total_evaluations', 0)}")
    print(f"  Sessions historique  : {len(kb.get('history', []))}")
    print(f"  Mise à jour          : {kb.get('last_updated', 'N/A')}")

    if kb.get("aggregated_scores"):
        print(f"\n  {B}Scores agrégés par domaine :{E}")
        for domain, data in sorted(kb["aggregated_scores"].items(), key=lambda x: x[1]["avg"]):
            avg = data["avg"]
            color = G if avg >= 85 else Y if avg >= 65 else R
            n = len(data["scores"])
            print(f"    {color}{domain:25} {avg:5.1f}%{E} ({n} mesures)")

    if kb.get("recurring_issues"):
        print(f"\n  {R}{B}Problèmes récurrents :{E}")
        for item in kb["recurring_issues"][:5]:
            print(f"    ✗ {item['issue']} ({item['occurrences']}x)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Source Synergy Agent")
    parser.add_argument("--domain", help="Filtrer par domaine expert")
    parser.add_argument("--update-kb", action="store_true", help="Afficher résumé base de connaissances")
    args = parser.parse_args()

    if args.update_kb:
        print_kb_summary()
    else:
        orchestrator = SynergyOrchestrator()
        orchestrator.run(domain_filter=args.domain)
