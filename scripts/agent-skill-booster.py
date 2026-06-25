#!/usr/bin/env python3
"""Agent Skill Booster — CaelumSwarm™
Crée des plans de formation personnalisés pour renforcer les compétences manquantes.
Usage : python3 scripts/agent-skill-booster.py
"""

import json
import os

# ---------------------------------------------------------------------------
# Catalogue de compétences et ressources de formation
# ---------------------------------------------------------------------------

COMPETENCES_CATALOGUE = {
    "CSDDD_compliance": {
        "description": "Maîtrise de la directive EU 2024/1760 (CSDDD)",
        "ressource_primaire": "EUR-Lex EU 2024/1760 (gratuit)",
        "ressource_secondaire": "Business & Human Rights Resource Centre",
        "exercice": "Résumer les 5 obligations principales CSDDD pour une entreprise de 500 salariés",
        "durée_heures": 4,
        "priorité": "haute",
    },
    "python_data_processing": {
        "description": "Traitement de données Python (json, csv, datetime)",
        "ressource_primaire": "Python Essentials 1 — Cisco NetAcad (gratuit, 70h)",
        "ressource_secondaire": "Real Python — Working with JSON",
        "exercice": "Parser le fichier output d'un engine Python et générer un rapport markdown",
        "durée_heures": 20,
        "priorité": "haute",
    },
    "nextjs_api_routes": {
        "description": "Création de routes API Next.js avec sécurité",
        "ressource_primaire": "Next.js Official Docs — Route Handlers",
        "ressource_secondaire": "Pattern sécurité CaelumSwarm (CLAUDE.md)",
        "exercice": "Créer une route API avec sealResponse + SWARM_API_URL guard",
        "durée_heures": 8,
        "priorité": "haute",
    },
    "human_rights_due_diligence": {
        "description": "Diligence raisonnable droits humains (UNGPs)",
        "ressource_primaire": "OHCHR — Guiding Principles on Business & Human Rights (PDF gratuit)",
        "ressource_secondaire": "OECD Guidelines for MNEs",
        "exercice": "Rédiger une analyse de risque droits humains pour une chaîne d'approvisionnement fictive",
        "durée_heures": 6,
        "priorité": "haute",
    },
    "monitoring_observability": {
        "description": "Monitoring systèmes, métriques, alertes",
        "ressource_primaire": "Google Cloud Monitoring (free tier)",
        "ressource_secondaire": "Prometheus + Grafana Getting Started",
        "exercice": "Configurer des alertes latence sur les routes API CaelumSwarm",
        "durée_heures": 12,
        "priorité": "moyenne",
    },
    "esg_reporting_standards": {
        "description": "Standards rapports ESG (GRI, SASB, TCFD, CSRD)",
        "ressource_primaire": "GRI Standards (gratuit, gri.org)",
        "ressource_secondaire": "CSRD Reporting Guide — EFRAG",
        "exercice": "Identifier les indicateurs GRI pertinents pour les 42 engines CaelumSwarm",
        "durée_heures": 8,
        "priorité": "haute",
    },
    "data_security": {
        "description": "Sécurité des données, chiffrement, RGPD",
        "ressource_primaire": "Introduction to Cybersecurity — Cisco NetAcad (gratuit, 15h)",
        "ressource_secondaire": "CNIL Guide RGPD Développeurs",
        "exercice": "Auditer les routes API pour absence de données personnelles non chiffrées",
        "durée_heures": 15,
        "priorité": "haute",
    },
    "react_dashboard_design": {
        "description": "Design de dashboards React accessibles et performants",
        "ressource_primaire": "React Official Docs — Hooks",
        "ressource_secondaire": "WCAG 2.1 Quick Reference (accessibilité)",
        "exercice": "Créer un dashboard Wave-pattern conforme avec GaugeRing et styles inline",
        "durée_heures": 10,
        "priorité": "moyenne",
    },
    "prometheus_metrics": {
        "description": "Exposition de métriques Prometheus dans des services Python/Node",
        "ressource_primaire": "Prometheus Official Docs — Instrumentation (gratuit)",
        "ressource_secondaire": "prometheus_client Python library README",
        "exercice": "Ajouter un endpoint /metrics sur un agent de monitoring CaelumSwarm",
        "durée_heures": 6,
        "priorité": "moyenne",
    },
    "grafana_integration": {
        "description": "Visualisation de métriques avec Grafana dashboards",
        "ressource_primaire": "Grafana Getting Started (gratuit, grafana.com)",
        "ressource_secondaire": "Grafana University — Free Courses",
        "exercice": "Créer un dashboard Grafana pour visualiser les scores des engines CaelumSwarm",
        "durée_heures": 8,
        "priorité": "basse",
    },
    "ghg_protocol_scope3": {
        "description": "Protocole GHG Scope 3 — émissions indirectes chaîne de valeur",
        "ressource_primaire": "GHG Protocol Corporate Standard (PDF gratuit, ghgprotocol.org)",
        "ressource_secondaire": "CDP Technical Note on Scope 3 Emissions",
        "exercice": "Calculer le Scope 3 catégorie 1 pour un fournisseur fictif",
        "durée_heures": 5,
        "priorité": "haute",
    },
    "eu_ai_act": {
        "description": "EU AI Act — obligations selon niveau de risque IA",
        "ressource_primaire": "EUR-Lex EU 2024/1689 — AI Act (gratuit)",
        "ressource_secondaire": "AI Act Explorer — Future of Life Institute",
        "exercice": "Classifier les agents CaelumSwarm par niveau de risque AI Act",
        "durée_heures": 5,
        "priorité": "haute",
    },
    "bias_detection": {
        "description": "Détection et correction de biais algorithmiques",
        "ressource_primaire": "Fairlearn Documentation (Microsoft, gratuit)",
        "ressource_secondaire": "AI Fairness 360 — IBM Research",
        "exercice": "Auditer les scores d'un engine pour biais démographiques",
        "durée_heures": 10,
        "priorité": "moyenne",
    },
    "static_security_analysis": {
        "description": "Analyse statique de sécurité du code Python",
        "ressource_primaire": "Bandit — Python Security Linter (docs.pyup.io)",
        "ressource_secondaire": "OWASP Python Security Project",
        "exercice": "Exécuter bandit sur le répertoire scripts/ et corriger les vulnérabilités",
        "durée_heures": 4,
        "priorité": "haute",
    },
    "secret_detection": {
        "description": "Détection de secrets et credentials dans le code",
        "ressource_primaire": "GitLeaks Documentation (gratuit, github.com/gitleaks)",
        "ressource_secondaire": "GitHub Secret Scanning Guide",
        "exercice": "Configurer un pre-commit hook de détection de secrets sur le repo CaelumSwarm",
        "durée_heures": 3,
        "priorité": "haute",
    },
    "microservices_patterns": {
        "description": "Patterns microservices avancés (CQRS, Event Sourcing, Saga)",
        "ressource_primaire": "microservices.io — Chris Richardson (gratuit)",
        "ressource_secondaire": "Building Microservices — Sam Newman (livre)",
        "exercice": "Documenter le pattern de communication entre agents CaelumSwarm",
        "durée_heures": 15,
        "priorité": "moyenne",
    },
    "tree_shaking_analysis": {
        "description": "Analyse tree-shaking et optimisation bundles JavaScript",
        "ressource_primaire": "webpack Documentation — Tree Shaking (gratuit)",
        "ressource_secondaire": "Bundle Buddy — outil d'analyse (gratuit)",
        "exercice": "Identifier les imports inutilisés dans les dashboards CaelumSwarm",
        "durée_heures": 6,
        "priorité": "basse",
    },
    "b2b_lead_scoring": {
        "description": "Scoring et qualification de leads B2B (BANT, MQL/SQL)",
        "ressource_primaire": "HubSpot Academy — Lead Scoring (gratuit)",
        "ressource_secondaire": "Salesforce Trailhead — Lead Management",
        "exercice": "Créer une grille de scoring BANT pour prospects Caelum Partners",
        "durée_heures": 4,
        "priorité": "basse",
    },
    "rgpd_prospection": {
        "description": "Cadre légal RGPD appliqué à la prospection commerciale",
        "ressource_primaire": "CNIL Guide Prospection Commerciale (gratuit, cnil.fr)",
        "ressource_secondaire": "Legifrance — Loi Informatique et Libertés",
        "exercice": "Rédiger une notice RGPD pour le module de prospection CaelumSwarm",
        "durée_heures": 3,
        "priorité": "haute",
    },
    "community_wellbeing_indicators": {
        "description": "Indicateurs bien-être et impact communautaire",
        "ressource_primaire": "OCDE Better Life Index Methodology (gratuit)",
        "ressource_secondaire": "Guide ONU Engagement Communautaire",
        "exercice": "Sélectionner 5 indicateurs bien-être pertinents pour un engine CaelumSwarm",
        "durée_heures": 5,
        "priorité": "moyenne",
    },
    "github_actions_advanced": {
        "description": "GitHub Actions — workflows réutilisables et OIDC",
        "ressource_primaire": "GitHub Actions Documentation (gratuit, docs.github.com)",
        "ressource_secondaire": "GitHub Skills — Advanced GitHub Actions",
        "exercice": "Créer un reusable workflow pour la validation des engines Python CaelumSwarm",
        "durée_heures": 8,
        "priorité": "moyenne",
    },
}

# Mapping des compétences manquantes (texte libre) vers les clés du catalogue
COMPETENCE_MAPPING = {
    "connaissance prometheus metrics": "prometheus_metrics",
    "intégration grafana": "grafana_integration",
    "csddd phase 2 entreprises 250+ salariés": "CSDDD_compliance",
    "analyse sécurité statique": "static_security_analysis",
    "détection secrets dans code": "secret_detection",
    "patterns microservices avancés": "microservices_patterns",
    "event-driven architecture": "microservices_patterns",
    "protocole ghg scope 3 détaillé": "ghg_protocol_scope3",
    "calcul intensité carbone sectorielle": "ghg_protocol_scope3",
    "eu ai act obligations par risque": "eu_ai_act",
    "bias detection algorithms": "bias_detection",
    "tree-shaking analysis": "tree_shaking_analysis",
    "core web vitals impact": "tree_shaking_analysis",
    "webpack bundle analyzer avancé": "tree_shaking_analysis",
    "scoring qualification leads b2b": "b2b_lead_scoring",
    "rgpd prospection commerciale": "rgpd_prospection",
    "enrichissement données entreprises": "b2b_lead_scoring",
    "indicateurs bien-être communautaire": "community_wellbeing_indicators",
    "méthodes participatives locales": "community_wellbeing_indicators",
    "cartographie parties prenantes": "human_rights_due_diligence",
    "github actions advanced workflows": "github_actions_advanced",
}

PRIORITE_ORDER = {"haute": 0, "moyenne": 1, "basse": 2}


# ---------------------------------------------------------------------------
# Fonctions principales
# ---------------------------------------------------------------------------

def resolve_competence_key(competence_libre: str) -> str:
    """Résout une compétence en texte libre vers une clé du catalogue."""
    normalized = competence_libre.lower().strip()
    for mapping_key, catalogue_key in COMPETENCE_MAPPING.items():
        if mapping_key in normalized or normalized in mapping_key:
            return catalogue_key
    # Fallback : chercher dans les descriptions du catalogue
    for key, data in COMPETENCES_CATALOGUE.items():
        if normalized in data["description"].lower():
            return key
    return None


def generate_learning_path(agent_name: str, competences_manquantes: list) -> dict:
    """Génère un plan de formation personnalisé ordonné par priorité."""
    modules = []
    seen_keys = set()

    for competence in competences_manquantes:
        key = resolve_competence_key(competence)
        if key and key not in seen_keys and key in COMPETENCES_CATALOGUE:
            seen_keys.add(key)
            data = COMPETENCES_CATALOGUE[key]
            modules.append({
                "competence_clé": key,
                "competence_libellé": competence,
                "description": data["description"],
                "ressource_primaire": data["ressource_primaire"],
                "ressource_secondaire": data["ressource_secondaire"],
                "exercice_pratique": data["exercice"],
                "durée_heures": data["durée_heures"],
                "priorité": data["priorité"],
            })
        elif not key:
            # Compétence inconnue — générer un module générique
            modules.append({
                "competence_clé": "personnalisé",
                "competence_libellé": competence,
                "description": competence,
                "ressource_primaire": "Recherche documentaire recommandée",
                "ressource_secondaire": "Consulter CLAUDE.md du projet",
                "exercice_pratique": f"Implémenter '{competence}' dans le contexte CaelumSwarm",
                "durée_heures": 4,
                "priorité": "moyenne",
            })

    # Tri par priorité (haute en premier)
    modules.sort(key=lambda m: PRIORITE_ORDER.get(m["priorité"], 99))

    plan = {
        "agent_name": agent_name,
        "nb_competences": len(modules),
        "modules": modules,
        "total_heures": estimate_total_hours(modules),
        "priorité_globale": modules[0]["priorité"] if modules else "N/A",
    }
    return plan


def estimate_total_hours(modules: list) -> int:
    """Calcule le temps total de formation en heures."""
    return sum(m.get("durée_heures", 0) for m in modules)


def export_plan(agent_name: str, plan: dict) -> str:
    """Sauvegarde le plan dans docs/training/<agent_name>_plan.md."""
    training_dir = os.path.join(
        os.path.dirname(__file__), "..", "docs", "training"
    )
    os.makedirs(training_dir, exist_ok=True)

    safe_name = agent_name.replace(".py", "").replace(" ", "-")
    filepath = os.path.join(training_dir, f"{safe_name}_plan.md")

    lines = [
        f"# Plan de formation — {agent_name}",
        "",
        f"**Total heures :** {plan['total_heures']}h  ",
        f"**Modules :** {plan['nb_competences']}  ",
        f"**Priorité globale :** {plan['priorité_globale']}",
        "",
        "---",
        "",
        "## Modules de formation",
        "",
    ]

    for i, module in enumerate(plan["modules"], start=1):
        lines += [
            f"### Module {i} — {module['description']}",
            "",
            f"- **Compétence :** {module['competence_libellé']}",
            f"- **Priorité :** {module['priorité'].upper()}",
            f"- **Durée :** {module['durée_heures']}h",
            f"- **Ressource primaire :** {module['ressource_primaire']}",
            f"- **Ressource secondaire :** {module['ressource_secondaire']}",
            "",
            f"**Exercice pratique :**",
            f"> {module['exercice_pratique']}",
            "",
            "---",
            "",
        ]

    lines += [
        "## Récapitulatif",
        "",
        f"| Priorité | Modules |",
        "| -------- | ------- |",
    ]

    for p in ["haute", "moyenne", "basse"]:
        count = sum(1 for m in plan["modules"] if m["priorité"] == p)
        if count:
            lines.append(f"| {p.capitalize()} | {count} module(s) |")

    lines += [
        "",
        f"*Généré automatiquement par agent-skill-booster.py — CaelumSwarm™*",
    ]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filepath


# ---------------------------------------------------------------------------
# Affichage console
# ---------------------------------------------------------------------------

BOLD = "\033[1m"
RESET = "\033[0m"
PRIORITE_COLORS = {
    "haute": "\033[91m",    # rouge
    "moyenne": "\033[93m",  # jaune
    "basse": "\033[94m",    # bleu
}


def print_plan(plan: dict) -> None:
    """Affiche le plan de formation dans le terminal."""
    print(f"\n{BOLD}Plan de formation — {plan['agent_name']}{RESET}")
    print(f"  Modules       : {plan['nb_competences']}")
    print(f"  Total heures  : {plan['total_heures']}h")
    print(f"  Priorité glob : {plan['priorité_globale'].upper()}\n")

    for i, module in enumerate(plan["modules"], start=1):
        color = PRIORITE_COLORS.get(module["priorité"], "")
        print(f"  {BOLD}Module {i}{RESET} — {module['description']}")
        print(f"    Competence      : {module['competence_libellé']}")
        print(f"    Priorité        : {color}{module['priorité'].upper()}{RESET}")
        print(f"    Durée           : {module['durée_heures']}h")
        print(f"    Ressource 1     : {module['ressource_primaire']}")
        print(f"    Ressource 2     : {module['ressource_secondaire']}")
        print(f"    Exercice        : {module['exercice_pratique']}")
        print()


def print_catalogue_stats() -> None:
    """Affiche les statistiques du catalogue de compétences."""
    by_priorite = {}
    total_heures = 0
    for data in COMPETENCES_CATALOGUE.values():
        p = data["priorité"]
        by_priorite[p] = by_priorite.get(p, 0) + 1
        total_heures += data["durée_heures"]

    print(f"\n{BOLD}Catalogue de compétences CaelumSwarm™{RESET}")
    print(f"  Total compétences : {len(COMPETENCES_CATALOGUE)}")
    print(f"  Total heures pot. : {total_heures}h")
    for p in ["haute", "moyenne", "basse"]:
        count = by_priorite.get(p, 0)
        color = PRIORITE_COLORS.get(p, "")
        print(f"  {color}{p.capitalize():<8}{RESET} : {count} compétence(s)")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}CaelumSwarm™ — Agent Skill Booster{RESET}")
    print("  Génération de plans de formation personnalisés...\n")

    # Statistiques du catalogue
    print_catalogue_stats()

    # Demo : plan pour health-latency-monitor-agent
    demo_agent = "health-latency-monitor-agent.py"
    demo_lacunes = [
        "connaissance Prometheus metrics",
        "intégration Grafana",
        "monitoring_observability",
    ]

    print(f"\n{BOLD}Demo — Génération du plan pour : {demo_agent}{RESET}")
    plan = generate_learning_path(demo_agent, demo_lacunes)
    print_plan(plan)

    # Export fichier markdown
    filepath = export_plan(demo_agent, plan)
    print(f"  Plan exporté : {filepath}")

    # Export JSON du plan
    print(f"\n{BOLD}Plan JSON complet :{RESET}")
    print(json.dumps(plan, ensure_ascii=False, indent=2))

    # Demo additionnelle : agent avec lacunes multiples
    demo2_agent = "compliance-audit-agent.py"
    demo2_lacunes = [
        "CSDDD phase 2 entreprises 250+ salariés",
        "esg_reporting_standards",
    ]
    plan2 = generate_learning_path(demo2_agent, demo2_lacunes)
    filepath2 = export_plan(demo2_agent, plan2)
    print(f"\n  Plan compliance exporté : {filepath2}")
    print(f"  Temps total formation   : {plan2['total_heures']}h")

    print(f"\n{BOLD}Skill Booster terminé.{RESET}\n")


if __name__ == "__main__":
    main()
