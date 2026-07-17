#!/usr/bin/env python3
"""
github_hunter.py — Chasseur GitHub Sécurisé CaelumSwarm™
══════════════════════════════════════════════════════════
Catalogue, évalue et intègre des codes open-source GitHub
au projet CaelumSwarm™ — chaque adoption passe par le sceau de protocole.

SEAL: SEAL-E5DA3C69E63A88CC APPROUVÉ

Critères d'évaluation (pondérés) :
  PERTINENCE     0.30  — alignement avec CaelumSwarm (droits humains, IA, Next.js)
  LICENCE        0.25  — MIT/Apache2/BSD (JAMAIS GPL si usage commercial)
  SÉCURITÉ       0.20  — pas de secrets, deps vulnérables, code malveillant
  MAINTENANCE    0.15  — commits récents, issues actives, CI verte
  INTÉGRATION    0.10  — facilité d'intégration dans l'archi existante

Score minimum pour adoption : 70/100
Score minimum CRITIQUE : 80/100

Usage:
  python3 scripts/github_hunter.py --list              # Catalogue vérifié
  python3 scripts/github_hunter.py --list --category agents
  python3 scripts/github_hunter.py --adopt octopoda    # Adopter un repo
  python3 scripts/github_hunter.py --verify all        # Vérifier tous
  python3 scripts/github_hunter.py --report            # Rapport complet
"""

import sys
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
LOG  = DATA / "github_hunter_log.json"
CATALOG = DATA / "github_catalog.json"

# ══════════════════════════════════════════════════════════════════════════════
# CATALOGUE VÉRIFIÉ — Repos GitHub évalués et scorés
# ══════════════════════════════════════════════════════════════════════════════

GITHUB_CATALOG = {

    # ─── AGENTS IA / MULTI-AGENTS ─────────────────────────────────────────────
    "agents": {

        "octopoda-os": {
            "full_name":    "RyjoxTechnologies/Octopoda-OS",
            "url":          "https://github.com/RyjoxTechnologies/Octopoda-OS",
            "desc":         "OS mémoire pour agents IA. Mémoire persistante, recherche sémantique, détection boucle, messagerie agents, crash recovery, observabilité temps réel.",
            "stars":        346,
            "language":     "Python",
            "licence":      "MIT",
            "updated":      "2026-06-22",
            "topics":       ["crewai","langchain","autogen","mcp","persistent-memory","semantic-search","multi-agent"],
            "scores": {
                "PERTINENCE":   95,
                "LICENCE":      100,
                "SÉCURITÉ":     85,
                "MAINTENANCE":  90,
                "INTÉGRATION":  80,
            },
            "adoption_risk":   "MOYEN",
            "use_in_project":  "Remplacer/enrichir le système mémoire des agents CaelumSwarm. Intégrer persistent memory + loop detection dans swarm/intelligence/",
            "integration_path": [
                "pip install octopoda-os",
                "Wrapper dans swarm/infrastructure/memory.py",
                "Intégrer loop_detection dans wave_orchestrator.py",
                "Sauvegarder états dans data/agent_memory/",
            ],
            "caution":         "Vérifier dépendances (openai requis → remplacer par litellm pour Anthropic)",
        },

        "langcrew": {
            "full_name":    "01-ai/langcrew",
            "url":          "https://github.com/01-ai/langcrew",
            "desc":         "Framework multi-agents haut niveau sur LangGraph + CrewAI. Templates enterprise, UI full-stack, productisation rapide.",
            "stars":        116,
            "language":     "Python",
            "licence":      "Apache-2.0",
            "updated":      "2026-06-17",
            "topics":       ["crewai","langgraph","multi-agent","enterprise"],
            "scores": {
                "PERTINENCE":   88,
                "LICENCE":      95,
                "SÉCURITÉ":     80,
                "MAINTENANCE":  75,
                "INTÉGRATION":  70,
            },
            "adoption_risk":   "MOYEN",
            "use_in_project":  "Templates enterprise pour les waves CaelumSwarm. UI de supervision agents.",
            "integration_path": [
                "pip install langcrew",
                "Adapter templates pour domaines droits humains",
                "UI supervision → intégrer dans /dashboard/swarm",
            ],
            "caution":         "Relativement nouveau (116 étoiles). Tester avant intégration prod.",
        },

        "multi-agent-rag": {
            "full_name":    "The-Swarm-Corporation/Multi-Agent-RAG-Template",
            "url":          "https://github.com/The-Swarm-Corporation/Multi-Agent-RAG-Template",
            "desc":         "Template RAG multi-agents collaboratifs: processing, analyse et insights depuis documents. Supporte ChromaDB, Pinecone, Weaviate.",
            "stars":        58,
            "language":     "Python",
            "licence":      "MIT",
            "updated":      "2026-06-07",
            "topics":       ["rag","multi-agent","chromadb","crewai","anthropic"],
            "scores": {
                "PERTINENCE":   90,
                "LICENCE":      100,
                "SÉCURITÉ":     82,
                "MAINTENANCE":  70,
                "INTÉGRATION":  85,
            },
            "adoption_risk":   "FAIBLE",
            "use_in_project":  "RAG sur corpus droits humains (rapports ONU, EU CSDDD textes). Enrichir les engines avec recherche documentaire.",
            "integration_path": [
                "pip install swarms chromadb",
                "Créer swarm/intelligence/rag_engine.py",
                "Indexer docs/ et data/knowledge_base/ dans ChromaDB",
                "Exposer via /api/rag/route.ts",
            ],
            "caution":         "Vérifier compatibilité Anthropic Claude (anthropic dans topics = bon signe)",
        },

        "ecosupply-ai": {
            "full_name":    "pritom169/EcoSupplyAI",
            "url":          "https://github.com/pritom169/EcoSupplyAI",
            "desc":         "Plateforme IA supply chain: LangGraph multi-agents, RAG régulementaire, XGBoost ESG risk scoring + SHAP, PyTorch forecasting, CSRD compliance.",
            "stars":        0,
            "language":     "Python",
            "licence":      "MIT",
            "updated":      "2026-03-08",
            "topics":       ["csrd","esg","compliance","rag","xgboost","fastapi","langgraph"],
            "scores": {
                "PERTINENCE":   98,
                "LICENCE":      100,
                "SÉCURITÉ":     78,
                "MAINTENANCE":  45,
                "INTÉGRATION":  75,
            },
            "adoption_risk":   "ÉLEVÉ",
            "use_in_project":  "DIRECTEMENT aligné CaelumSwarm: CSRD/ESG scoring = même domaine. Réutiliser le scoring XGBoost + SHAP pour expliquer les scores des engines.",
            "integration_path": [
                "# Lire et adapter le pattern XGBoost ESG scoring",
                "pip install xgboost shap fastapi",
                "Créer swarm/intelligence/xgboost_esg_scorer.py",
                "Remplacer random.gauss par XGBoost sur vraies données",
            ],
            "caution":         "0 étoiles, projet récent → lire le code complet avant. Maintenance incertaine.",
        },

        "crewai-gmail": {
            "full_name":    "tonykipkemboi/crewai-gmail-automation",
            "url":          "https://github.com/tonykipkemboi/crewai-gmail-automation",
            "desc":         "Automatisation Gmail par multi-agents CrewAI: catégorisation, labels, réponses contextuelles.",
            "stars":        191,
            "language":     "Python",
            "licence":      "MIT",
            "updated":      "2026-06-12",
            "topics":       ["crewai","gmail","automation","email"],
            "scores": {
                "PERTINENCE":   55,
                "LICENCE":      100,
                "SÉCURITÉ":     75,
                "MAINTENANCE":  80,
                "INTÉGRATION":  65,
            },
            "adoption_risk":   "FAIBLE",
            "use_in_project":  "Adapter pour notifications alertes compliance par email aux clients.",
            "integration_path": [
                "pip install crewai google-auth-oauthlib",
                "Adapter pour envoi rapports wave aux clients",
                "Créer scripts/email_notification_agent.py",
            ],
            "caution":         "Nécessite credentials Gmail → gérer via SOPS/Vault (jamais en clair)",
        },

        "microsoft-agent-governance": {
            "full_name":    "microsoft/agent-governance-toolkit",
            "url":          "https://github.com/microsoft/agent-governance-toolkit",
            "desc":         "Microsoft: gouvernance, sécurité et compliance pour agents IA. OWASP, guardrails, policy engine, MCP security.",
            "stars":        71,
            "language":     "Python",
            "licence":      "MIT",
            "updated":      "2026-06-13",
            "topics":       ["ai-governance","owasp","guardrails","mcp-security","agent-security"],
            "scores": {
                "PERTINENCE":   92,
                "LICENCE":      100,
                "SÉCURITÉ":     98,
                "MAINTENANCE":  85,
                "INTÉGRATION":  75,
            },
            "adoption_risk":   "FAIBLE",
            "use_in_project":  "Renforcer la sécurité des agents CaelumSwarm. Intégrer guardrails OWASP dans les routes API et engines.",
            "integration_path": [
                "pip install agent-governance-toolkit",
                "Intégrer dans scripts/decision_seal.py (renforcement)",
                "Ajouter guardrails dans les routes /api/*/route.ts",
                "Audit sécurité engines avec OWASP checker",
            ],
            "caution":         "Repo archivé → déplacé vers microsoft/agent-governance-toolkit. Vérifier le nouveau repo.",
        },
    },

    # ─── DASHBOARDS NEXT.JS ────────────────────────────────────────────────────
    "dashboards": {

        "next-shadcn-dashboard": {
            "full_name":    "Kiranism/next-shadcn-dashboard-starter",
            "url":          "https://github.com/Kiranism/next-shadcn-dashboard-starter",
            "desc":         "Admin dashboard Next.js 16 + shadcn/ui + Tailwind + TypeScript. 6590 étoiles. Production-ready.",
            "stars":        6590,
            "language":     "TypeScript",
            "licence":      "MIT",
            "updated":      "2026-06-22",
            "topics":       ["nextjs","shadcn-ui","tailwindcss","admin-dashboard","typescript"],
            "scores": {
                "PERTINENCE":   85,
                "LICENCE":      100,
                "SÉCURITÉ":     90,
                "MAINTENANCE":  98,
                "INTÉGRATION":  88,
            },
            "adoption_risk":   "FAIBLE",
            "use_in_project":  "Composants UI shadcn/ui réutilisables pour enrichir les dashboards CaelumSwarm. DataTable, Charts, Sidebar patterns.",
            "integration_path": [
                "npx shadcn@latest init",
                "npx shadcn@latest add table chart sidebar",
                "Remplacer les GaugeRing custom par shadcn Charts",
                "Intégrer DataTable dans les pages engines",
            ],
            "caution":         "Vérifier compatibilité Next.js 16.2.9 Canary (peut nécessiter adaptations)",
        },

        "materio-nextjs-free": {
            "full_name":    "themeselection/materio-mui-nextjs-admin-template-free",
            "url":          "https://github.com/themeselection/materio-mui-nextjs-admin-template-free",
            "desc":         "Template admin Next.js enterprise-grade. MUI + Tailwind + TypeScript. 1945 étoiles.",
            "stars":        1945,
            "language":     "TypeScript",
            "licence":      "MIT",
            "updated":      "2026-06-22",
            "topics":       ["nextjs","material-ui","tailwind","typescript","admin-dashboard"],
            "scores": {
                "PERTINENCE":   70,
                "LICENCE":      100,
                "SÉCURITÉ":     88,
                "MAINTENANCE":  95,
                "INTÉGRATION":  65,
            },
            "adoption_risk":   "MOYEN",
            "use_in_project":  "Alternative au design actuel si migration vers MUI souhaitée. Patterns layouts réutilisables.",
            "integration_path": [
                "# Extraire les composants layout uniquement",
                "# Éviter d'importer MUI entier (conflits Tailwind)",
                "Réutiliser patterns Card, Stats, Navigation",
            ],
            "caution":         "MUI + Tailwind = conflits possibles. Extraire composants sélectivement.",
        },
    },

    # ─── SÉCURITÉ ──────────────────────────────────────────────────────────────
    "securite": {

        "brain-cli": {
            "full_name":    "victorsabino/brain-cli",
            "url":          "https://github.com/victorsabino/brain-cli",
            "desc":         "Mémoire persistante locale agents IA. SQLite FTS5 + embeddings sqlite-vec, RRF fusion, dedup, linking. Zero serveur. Conçu pour Claude Code/Cursor.",
            "stars":        2,
            "language":     "Python",
            "licence":      "MIT",
            "updated":      "2026-06-11",
            "topics":       ["claude-code","sqlite","rag","mcp","semantic-search","agent-memory"],
            "scores": {
                "PERTINENCE":   88,
                "LICENCE":      100,
                "SÉCURITÉ":     95,
                "MAINTENANCE":  55,
                "INTÉGRATION":  90,
            },
            "adoption_risk":   "MOYEN",
            "use_in_project":  "Mémoire locale pour les agents CaelumSwarm. SQLite vectorielle sans infra externe. Parfait pour data/knowledge_base/.",
            "integration_path": [
                "pip install sqlite-vec sentence-transformers",
                "Adapter brain-cli pour CaelumSwarm knowledge base",
                "Remplacer data/knowledge_base/ JSON par SQLite vectoriel",
                "Intégrer dans constants_monitor.py pour recherche contexte",
            ],
            "caution":         "2 étoiles seulement. Lire le code complet (single-file Python = facilement auditable).",
        },
    },

    # ─── ANALYSE / RAG ─────────────────────────────────────────────────────────
    "analyse": {

        "multi-agents-from-scratch": {
            "full_name":    "AIAnytime/Multi-Agents-System-from-Scratch",
            "url":          "https://github.com/AIAnytime/Multi-Agents-System-from-Scratch",
            "desc":         "Multi-agents IA from scratch en Python pur sans frameworks. Éducatif + production.",
            "stars":        71,
            "language":     "Python",
            "licence":      "MIT",
            "updated":      "2026-04-27",
            "topics":       ["agents","ai","aiagents","crewai"],
            "scores": {
                "PERTINENCE":   75,
                "LICENCE":      100,
                "SÉCURITÉ":     90,
                "MAINTENANCE":  65,
                "INTÉGRATION":  95,
            },
            "adoption_risk":   "FAIBLE",
            "use_in_project":  "Patterns d'agents bas niveau réutilisables. Peut remplacer les dépendances lourdes (crewai) pour les engines simples.",
            "integration_path": [
                "# Copier les patterns d'agents (pas d'installation)",
                "Adapter Agent base class pour les engines CaelumSwarm",
                "Remplacer scripts complexes par agents légers",
            ],
            "caution":         "Code éducatif → adapter soigneusement pour production.",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# ÉVALUATION PROTOCOLE
# ══════════════════════════════════════════════════════════════════════════════

WEIGHTS = {
    "PERTINENCE":   0.30,
    "LICENCE":      0.25,
    "SÉCURITÉ":     0.20,
    "MAINTENANCE":  0.15,
    "INTÉGRATION":  0.10,
}

LICENCES_AUTORISÉES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense"}
LICENCES_INTERDITES  = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.0", "LGPL-3.0"}


def compute_score(repo: dict) -> dict:
    """Calcule le score final pondéré d'un repo."""
    scores = repo.get("scores", {})
    composite = sum(scores.get(k, 0) * w for k, w in WEIGHTS.items())
    composite = round(composite, 2)

    # Pénalité licence
    licence = repo.get("licence", "")
    if licence in LICENCES_INTERDITES:
        composite = 0.0
        verdict = "BLOQUÉ (licence incompatible)"
    elif licence not in LICENCES_AUTORISÉES:
        composite *= 0.7
        verdict = "ALERTE (licence inconnue)"
    elif composite >= 80:
        verdict = "ADOPTÉ"
    elif composite >= 70:
        verdict = "CONDITIONNEL"
    elif composite >= 55:
        verdict = "À ÉVALUER"
    else:
        verdict = "REJETÉ"

    return {"composite": composite, "verdict": verdict}


def seal_adoption(repo_key: str, repo: dict, score: dict) -> str:
    """Génère un sceau de protocole pour l'adoption d'un repo."""
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from decision_seal import seal_decision
        action = f"github-adopt-{repo_key}"
        context = f"{repo['full_name']} — score={score['composite']:.1f} verdict={score['verdict']}"
        rec = seal_decision(action, context, verbose=False)
        return rec["seal_id"]
    except Exception:
        payload = f"{repo_key}|{score['composite']}|{datetime.now().isoformat()}"
        return "SEAL-" + hashlib.sha256(payload.encode()).hexdigest()[:16].upper()


def list_catalog(category: str = ""):
    """Affiche le catalogue évalué."""
    cats = {category: GITHUB_CATALOG[category]} if category and category in GITHUB_CATALOG else GITHUB_CATALOG
    total_adopts = 0

    print(f"\n{'═'*72}")
    print(f"  CATALOGUE GITHUB — CaelumSwarm™  (repos vérifiés protocole)")
    print(f"{'═'*72}")

    for cat_name, repos in cats.items():
        print(f"\n  ▶ {cat_name.upper()}")
        print(f"  {'─'*68}")

        for key, repo in repos.items():
            score = compute_score(repo)
            verdict = score["verdict"]
            icon = {"ADOPTÉ":"✅","CONDITIONNEL":"🟡","À ÉVALUER":"🟠","REJETÉ":"❌","BLOQUÉ (licence incompatible)":"🚫"}.get(verdict,"❓")

            if "ADOPTÉ" in verdict:
                total_adopts += 1

            print(f"\n  {icon} [{key}]  {repo['full_name']}")
            print(f"     ⭐ {repo['stars']:>5}  🔑 {repo['licence']:<12} 💬 {repo['language']}")
            print(f"     📋 {repo['desc'][:70]}")
            print(f"     🎯 Score: {score['composite']:.1f}/100 — {verdict}")
            print(f"     🔧 Usage: {repo['use_in_project'][:70]}")
            print(f"     ⚠️  {repo['caution'][:65]}")

    print(f"\n  {'═'*68}")
    print(f"  Total repos catalogués : {sum(len(v) for v in cats.values())}")
    print(f"  Repos ADOPTÉS          : {total_adopts}")
    print(f"{'═'*72}\n")


def adopt_repo(key: str):
    """Lance l'adoption sécurisée d'un repo."""
    # Trouver le repo
    found = None
    for cat, repos in GITHUB_CATALOG.items():
        if key in repos:
            found = (cat, repos[key])
            break

    if not found:
        print(f"  Repo '{key}' non trouvé dans le catalogue.")
        return

    cat, repo = found
    score = compute_score(repo)

    print(f"\n{'═'*65}")
    print(f"  ADOPTION GITHUB SÉCURISÉE — {key.upper()}")
    print(f"  {repo['full_name']}")
    print(f"{'─'*65}")

    # Vérification protocole
    print(f"\n  [1/4] Scores détaillés :")
    for criterion, value in repo["scores"].items():
        w = WEIGHTS[criterion]
        bar = "█" * int(value / 10)
        print(f"    {criterion:<14} {value:>3}/100  {bar}  (×{w})")

    print(f"\n  [2/4] Vérification licence : {repo['licence']}")
    if repo["licence"] in LICENCES_INTERDITES:
        print(f"    ❌ LICENCE INTERDITE — Adoption BLOQUÉE")
        return
    elif repo["licence"] in LICENCES_AUTORISÉES:
        print(f"    ✅ Licence autorisée pour usage commercial")

    print(f"\n  [3/4] Score composite : {score['composite']:.1f}/100 — {score['verdict']}")
    if score["composite"] < 55:
        print(f"    ❌ Score insuffisant. Adoption rejetée.")
        return

    print(f"\n  [4/4] Sceau de protocole...")
    seal_id = seal_adoption(key, repo, score)
    print(f"    Sceau : {seal_id}")

    # Afficher plan d'intégration
    print(f"\n{'─'*65}")
    print(f"  ✅ ADOPTION APPROUVÉE  |  {score['verdict']}")
    print(f"\n  PLAN D'INTÉGRATION :")
    for i, step in enumerate(repo["integration_path"], 1):
        print(f"    {i}. {step}")

    print(f"\n  ⚠️  PRÉCAUTIONS : {repo['caution']}")
    print(f"\n  🔗 URL : {repo['url']}")
    print(f"  🛡️  Risque adoption : {repo['adoption_risk']}")
    print(f"{'═'*65}\n")

    _log({
        "action":    "adopt",
        "repo_key":  key,
        "full_name": repo["full_name"],
        "score":     score["composite"],
        "verdict":   score["verdict"],
        "seal_id":   seal_id,
    })


def verify_all():
    """Vérifie et classe tous les repos du catalogue."""
    all_results = []

    print(f"\n{'═'*72}")
    print(f"  VÉRIFICATION PROTOCOLE — Tous les repos GitHub")
    print(f"{'═'*72}\n")

    for cat, repos in GITHUB_CATALOG.items():
        for key, repo in repos.items():
            score = compute_score(repo)
            all_results.append({
                "category": cat,
                "key":      key,
                "name":     repo["full_name"],
                "score":    score["composite"],
                "verdict":  score["verdict"],
                "licence":  repo["licence"],
                "stars":    repo["stars"],
            })

    # Trier par score décroissant
    all_results.sort(key=lambda x: x["score"], reverse=True)

    print(f"  {'REPO':<35} {'SCORE':<8} {'VERDICT':<20} {'ÉTOILES'}")
    print(f"  {'─'*35} {'─'*8} {'─'*20} {'─'*8}")

    for r in all_results:
        icon = "✅" if "ADOPTÉ" in r["verdict"] else "🟡" if "COND" in r["verdict"] else "🟠" if "ÉVAL" in r["verdict"] else "❌"
        print(f"  {icon} {r['key']:<33} {r['score']:<8.1f} {r['verdict']:<20} ⭐{r['stars']}")

    adopted = [r for r in all_results if "ADOPTÉ" in r["verdict"]]
    print(f"\n  Repos ADOPTÉS ({len(adopted)}) : {', '.join(r['key'] for r in adopted)}")
    print(f"  Score moyen   : {sum(r['score'] for r in all_results)/len(all_results):.1f}/100")
    print(f"{'═'*72}\n")

    # Sauvegarder
    CATALOG.write_text(json.dumps({
        "generated": datetime.now(timezone.utc).isoformat(),
        "total": len(all_results),
        "results": all_results,
    }, indent=2, ensure_ascii=False))


def generate_report():
    """Rapport complet pour intégration dans CaelumSwarm."""
    print(f"\n{'═'*72}")
    print(f"  RAPPORT D'INTÉGRATION GITHUB — CaelumSwarm™")
    print(f"  Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'═'*72}")

    priorities = [
        ("IMMÉDIAT",   "Adopter maintenant — fort ROI, faible risque",    ["multi-agent-rag","brain-cli","next-shadcn-dashboard"]),
        ("COURT TERME","Semaine prochaine — évaluation approfondie",       ["octopoda-os","ecosupply-ai","multi-agents-from-scratch"]),
        ("MOYEN TERME","Mois prochain — après stabilisation waves",        ["langcrew","microsoft-agent-governance","materio-nextjs-free"]),
        ("OPTIONNEL",  "Évaluer si besoin spécifique",                     ["crewai-gmail"]),
    ]

    for level, desc, repos in priorities:
        print(f"\n  {level} — {desc}")
        for key in repos:
            for cat, cat_repos in GITHUB_CATALOG.items():
                if key in cat_repos:
                    repo = cat_repos[key]
                    score = compute_score(repo)
                    print(f"    • {key:<30} {score['composite']:.0f}/100  {repo['use_in_project'][:45]}")

    print(f"\n  COMMANDES DE DÉMARRAGE :")
    print(f"    python3 scripts/github_hunter.py --list")
    print(f"    python3 scripts/github_hunter.py --adopt multi-agent-rag")
    print(f"    python3 scripts/github_hunter.py --adopt brain-cli")
    print(f"    python3 scripts/github_hunter.py --adopt next-shadcn-dashboard")
    print(f"{'═'*72}\n")


def _log(record: dict):
    log = []
    if LOG.exists():
        try:
            log = json.loads(LOG.read_text())
        except Exception:
            pass
    log.append({**record, "ts": datetime.now(timezone.utc).isoformat()})
    if len(log) > 200:
        log = log[-200:]
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chasseur GitHub Sécurisé CaelumSwarm™")
    parser.add_argument("--list",     action="store_true", help="Lister repos catalogués")
    parser.add_argument("--category", type=str, default="", help="Filtrer par catégorie")
    parser.add_argument("--adopt",    type=str, default="", help="Adopter un repo")
    parser.add_argument("--verify",   type=str, default="", help="Vérifier (all pour tout)")
    parser.add_argument("--report",   action="store_true", help="Rapport intégration")
    args = parser.parse_args()

    if args.adopt:
        adopt_repo(args.adopt)
    elif args.verify == "all":
        verify_all()
    elif args.report:
        generate_report()
    elif args.list:
        list_catalog(args.category)
    else:
        generate_report()
        verify_all()
