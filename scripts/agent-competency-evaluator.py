#!/usr/bin/env python3
"""Agent Competency Evaluator — CaelumSwarm™
Audit complet des compétences de chaque agent du swarm sur 8 dimensions.
Usage : python3 scripts/agent-competency-evaluator.py
"""

import json
import os
from typing import Optional

# ---------------------------------------------------------------------------
# Poids des dimensions (total = 1.0)
# ---------------------------------------------------------------------------
DIMENSION_WEIGHTS = {
    "domain_expertise": 0.25,
    "code_quality": 0.20,
    "data_accuracy": 0.20,
    "output_completeness": 0.15,
    "error_handling": 0.10,
    "performance": 0.05,
    "autonomy": 0.05,
    # improvement_potential excluded from score calc (bonus insight only)
}

# 8th dimension weight note: improvement_potential is collected but not weighted
# (it represents future capacity, not current competence)

NIVEAU_SEUILS = {
    "expert": 80,
    "avancé": 61,
    "intermédiaire": 40,
    "débutant": 0,
}

# ---------------------------------------------------------------------------
# Données simulées — 10 agents représentatifs du repo
# ---------------------------------------------------------------------------
AGENTS_SIMULES = [
    {
        "agent_name": "health-latency-monitor-agent.py",
        "type": "monitoring",
        "scores": {
            "domain_expertise": 85,
            "code_quality": 78,
            "data_accuracy": 72,
            "output_completeness": 80,
            "error_handling": 70,
            "performance": 88,
            "autonomy": 82,
            "improvement_potential": 45,
        },
        "competences_manquantes": [
            "connaissance Prometheus metrics",
            "intégration Grafana",
        ],
        "plan_amelioration": [
            "Lire doc Prometheus",
            "Implémenter /metrics endpoint",
        ],
        "certification_recommandee": "Google Cloud Monitoring",
    },
    {
        "agent_name": "compliance-audit-agent.py",
        "type": "support_agent",
        "scores": {
            "domain_expertise": 90,
            "code_quality": 85,
            "data_accuracy": 88,
            "output_completeness": 92,
            "error_handling": 80,
            "performance": 75,
            "autonomy": 88,
            "improvement_potential": 20,
        },
        "competences_manquantes": [
            "CSDDD phase 2 entreprises 250+ salariés",
        ],
        "plan_amelioration": [
            "Lire EU 2024/1760 article 37",
            "Mettre à jour seuils compliance",
        ],
        "certification_recommandee": "ISO 26000 Lead Implementer",
    },
    {
        "agent_name": "code-quality-review-agent.py",
        "type": "support_agent",
        "scores": {
            "domain_expertise": 72,
            "code_quality": 93,
            "data_accuracy": 68,
            "output_completeness": 85,
            "error_handling": 88,
            "performance": 80,
            "autonomy": 76,
            "improvement_potential": 30,
        },
        "competences_manquantes": [
            "analyse sécurité statique",
            "détection secrets dans code",
        ],
        "plan_amelioration": [
            "Intégrer bandit (Python security linter)",
            "Ajouter règles détection tokens API",
        ],
        "certification_recommandee": "OWASP Top 10 Awareness",
    },
    {
        "agent_name": "architecture-review-agent.py",
        "type": "support_agent",
        "scores": {
            "domain_expertise": 78,
            "code_quality": 82,
            "data_accuracy": 75,
            "output_completeness": 78,
            "error_handling": 72,
            "performance": 70,
            "autonomy": 80,
            "improvement_potential": 35,
        },
        "competences_manquantes": [
            "patterns microservices avancés",
            "event-driven architecture",
        ],
        "plan_amelioration": [
            "Étudier CQRS / Event Sourcing",
            "Documenter les décisions ADR (Architecture Decision Records)",
        ],
        "certification_recommandee": "AWS Solutions Architect Associate",
    },
    {
        "agent_name": "carbon-optimization-agent.py",
        "type": "support_agent",
        "scores": {
            "domain_expertise": 88,
            "code_quality": 74,
            "data_accuracy": 85,
            "output_completeness": 80,
            "error_handling": 65,
            "performance": 72,
            "autonomy": 78,
            "improvement_potential": 40,
        },
        "competences_manquantes": [
            "protocole GHG Scope 3 détaillé",
            "calcul intensité carbone sectorielle",
        ],
        "plan_amelioration": [
            "Lire GHG Protocol Corporate Standard",
            "Intégrer données ADEME pour secteurs français",
        ],
        "certification_recommandee": "CDP Carbon Disclosure Certification",
    },
    {
        "agent_name": "ai-ethics-governance-agent.py",
        "type": "support_agent",
        "scores": {
            "domain_expertise": 82,
            "code_quality": 76,
            "data_accuracy": 80,
            "output_completeness": 75,
            "error_handling": 68,
            "performance": 65,
            "autonomy": 72,
            "improvement_potential": 38,
        },
        "competences_manquantes": [
            "EU AI Act obligations par risque",
            "bias detection algorithms",
        ],
        "plan_amelioration": [
            "Lire EU AI Act Article 9-15 (systèmes haut risque)",
            "Implémenter tests de biais sur datasets",
        ],
        "certification_recommandee": "Responsible AI Practitioner (IEEE)",
    },
    {
        "agent_name": "bundle-size-monitor-agent.py",
        "type": "monitoring",
        "scores": {
            "domain_expertise": 65,
            "code_quality": 80,
            "data_accuracy": 70,
            "output_completeness": 72,
            "error_handling": 75,
            "performance": 90,
            "autonomy": 82,
            "improvement_potential": 50,
        },
        "competences_manquantes": [
            "tree-shaking analysis",
            "Core Web Vitals impact",
            "webpack bundle analyzer avancé",
        ],
        "plan_amelioration": [
            "Étudier Lighthouse CI pour automatisation",
            "Configurer seuils LCP/CLS/FID",
        ],
        "certification_recommandee": "Google Web Performance Certification",
    },
    {
        "agent_name": "automated-expert-prospecting-agent.py",
        "type": "support_agent",
        "scores": {
            "domain_expertise": 55,
            "code_quality": 70,
            "data_accuracy": 58,
            "output_completeness": 65,
            "error_handling": 50,
            "performance": 60,
            "autonomy": 62,
            "improvement_potential": 65,
        },
        "competences_manquantes": [
            "scoring qualification leads B2B",
            "RGPD prospection commerciale",
            "enrichissement données entreprises",
        ],
        "plan_amelioration": [
            "Étudier le cadre légal RGPD pour prospection",
            "Intégrer scoring BANT (Budget, Authority, Need, Timeline)",
        ],
        "certification_recommandee": "Salesforce Certified Sales Cloud Consultant",
    },
    {
        "agent_name": "community-local-impact-agent.py",
        "type": "support_agent",
        "scores": {
            "domain_expertise": 70,
            "code_quality": 65,
            "data_accuracy": 68,
            "output_completeness": 60,
            "error_handling": 55,
            "performance": 58,
            "autonomy": 65,
            "improvement_potential": 55,
        },
        "competences_manquantes": [
            "indicateurs bien-être communautaire",
            "méthodes participatives locales",
            "cartographie parties prenantes",
        ],
        "plan_amelioration": [
            "Étudier les indicateurs OCDE Better Life Index",
            "Lire Guide ONU engagement communautaire",
        ],
        "certification_recommandee": "Community Development Professional (CDP)",
    },
    {
        "agent_name": "cicd-pipeline-agent.py",
        "type": "monitoring",
        "scores": {
            "domain_expertise": 88,
            "code_quality": 85,
            "data_accuracy": 82,
            "output_completeness": 88,
            "error_handling": 85,
            "performance": 92,
            "autonomy": 90,
            "improvement_potential": 20,
        },
        "competences_manquantes": [
            "GitHub Actions advanced workflows",
        ],
        "plan_amelioration": [
            "Implémenter reusable workflows",
            "Ajouter OIDC pour authentification sécurisée",
        ],
        "certification_recommandee": "GitHub Actions Certification",
    },
]


# ---------------------------------------------------------------------------
# Fonctions de calcul
# ---------------------------------------------------------------------------

def compute_score_global(scores: dict) -> float:
    """Calcule le score global pondéré (dimensions hors improvement_potential)."""
    total = 0.0
    for dimension, weight in DIMENSION_WEIGHTS.items():
        total += scores.get(dimension, 0) * weight
    return round(total, 2)


def get_niveau(score: float) -> str:
    """Retourne le niveau textuel selon le score global."""
    if score > NIVEAU_SEUILS["expert"]:
        return "expert"
    if score > NIVEAU_SEUILS["avancé"]:
        return "avancé"
    if score > NIVEAU_SEUILS["intermédiaire"]:
        return "intermédiaire"
    return "débutant"


def evaluate_agent(agent_data: dict) -> dict:
    """Évalue un agent et retourne le rapport complet."""
    scores = agent_data["scores"]
    score_global = compute_score_global(scores)
    niveau = get_niveau(score_global)

    return {
        "agent_name": agent_data["agent_name"],
        "type": agent_data["type"],
        "scores": scores,
        "score_global": score_global,
        "niveau": niveau,
        "competences_manquantes": agent_data.get("competences_manquantes", []),
        "plan_amelioration": agent_data.get("plan_amelioration", []),
        "certification_recommandee": agent_data.get("certification_recommandee", "N/A"),
    }


def evaluate_all_agents(agents: list) -> list:
    """Évalue tous les agents et retourne la liste triée par score décroissant."""
    results = [evaluate_agent(a) for a in agents]
    results.sort(key=lambda x: x["score_global"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# Affichage console
# ---------------------------------------------------------------------------

NIVEAU_COLORS = {
    "expert": "\033[92m",        # vert
    "avancé": "\033[94m",        # bleu
    "intermédiaire": "\033[93m", # jaune
    "débutant": "\033[91m",      # rouge
}
RESET = "\033[0m"
BOLD = "\033[1m"


def print_table(results: list) -> None:
    """Affiche un tableau formaté des résultats dans le terminal."""
    col_agent = 44
    col_type = 16
    col_score = 10
    col_niveau = 14

    separator = "-" * (col_agent + col_type + col_score + col_niveau + 7)

    header = (
        f"{'Agent':<{col_agent}} {'Type':<{col_type}} "
        f"{'Score':>{col_score}} {'Niveau':<{col_niveau}}"
    )

    print()
    print(f"{BOLD}{'=' * len(separator)}{RESET}")
    print(f"{BOLD}  CaelumSwarm™ — Rapport d'évaluation des compétences agents{RESET}")
    print(f"{'=' * len(separator)}")
    print(f"  {header}")
    print(f"  {separator}")

    for rank, r in enumerate(results, start=1):
        color = NIVEAU_COLORS.get(r["niveau"], "")
        score_str = f"{r['score_global']:.2f}"
        ligne = (
            f"  {rank:>2}. {r['agent_name']:<{col_agent - 5}} "
            f"{r['type']:<{col_type}} "
            f"{score_str:>{col_score}} "
            f"{color}{r['niveau']:<{col_niveau}}{RESET}"
        )
        print(ligne)

    print(f"  {separator}")
    print()


def print_detail(result: dict) -> None:
    """Affiche le détail d'un agent évalué."""
    color = NIVEAU_COLORS.get(result["niveau"], "")
    print(f"\n{BOLD}--- {result['agent_name']} ---{RESET}")
    print(f"  Type       : {result['type']}")
    print(f"  Score      : {BOLD}{result['score_global']:.2f}{RESET}")
    print(f"  Niveau     : {color}{result['niveau'].upper()}{RESET}")
    print("  Scores par dimension :")
    for dim, score in result["scores"].items():
        weight = DIMENSION_WEIGHTS.get(dim, 0)
        bar = "#" * (score // 5)
        weight_str = f"({weight * 100:.0f}%)" if weight else "(info)"
        print(f"    {dim:<28} {score:>3}  {bar:<20} {weight_str}")
    if result["competences_manquantes"]:
        print("  Competences manquantes :")
        for c in result["competences_manquantes"]:
            print(f"    - {c}")
    if result["plan_amelioration"]:
        print("  Plan d'amélioration :")
        for step in result["plan_amelioration"]:
            print(f"    * {step}")
    print(f"  Certification recommandée : {result['certification_recommandee']}")


def print_summary_stats(results: list) -> None:
    """Affiche des statistiques globales du swarm."""
    scores = [r["score_global"] for r in results]
    niveaux = [r["niveau"] for r in results]

    avg = round(sum(scores) / len(scores), 2)
    count_by_niveau = {n: niveaux.count(n) for n in ["expert", "avancé", "intermédiaire", "débutant"]}

    print(f"{BOLD}Statistiques globales du swarm{RESET}")
    print(f"  Agents évalués : {len(results)}")
    print(f"  Score moyen    : {avg}")
    print(f"  Meilleur       : {results[0]['agent_name']} ({results[0]['score_global']})")
    print(f"  Distribution   :")
    for niveau, count in count_by_niveau.items():
        bar = "*" * count
        print(f"    {niveau:<16} : {count:>2}  {bar}")
    print()


# ---------------------------------------------------------------------------
# Export JSON
# ---------------------------------------------------------------------------

def export_json(results: list, output_path: str) -> None:
    """Exporte les résultats en JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  Export JSON : {output_path}")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}CaelumSwarm™ — Agent Competency Evaluator{RESET}")
    print("  Évaluation de 10 agents représentatifs du swarm...\n")

    results = evaluate_all_agents(AGENTS_SIMULES)

    # Tableau de classement
    print_table(results)

    # Statistiques
    print_summary_stats(results)

    # Détail des 3 premiers et du dernier
    print(f"{BOLD}Détails — Top 3 + Agent en progression{RESET}")
    for r in results[:3]:
        print_detail(r)
    print_detail(results[-1])

    # Export JSON
    output_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
    os.makedirs(output_dir, exist_ok=True)
    export_path = os.path.join(output_dir, "competency-report.json")
    export_json(results, export_path)

    print(f"\n{BOLD}Evaluation terminée.{RESET}")
    print(f"  Agents certifiables (niveau expert) : "
          f"{sum(1 for r in results if r['niveau'] == 'expert')}/{len(results)}\n")


if __name__ == "__main__":
    main()
