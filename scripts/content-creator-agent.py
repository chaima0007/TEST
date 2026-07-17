#!/usr/bin/env python3
"""Content Creator Agent — CaelumSwarm™ Dev Support
Génère du contenu multilingue (FR/EN) pour les dashboards :
descriptions d'engines, alertes critiques, labels d'entités,
textes d'interface, tooltips, rapports CSDDD narratifs.
"""
import re
import json
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "ContentCreatorAgent"
VERSION = "1.0.0"

GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

DOMAIN_DESCRIPTIONS_FR = {
    "conflict_minerals": "Suivi de la conformité CSDDD pour les minéraux de conflit (3TG) selon Dodd-Frank Section 1502 et les directives EU 2017/821.",
    "prison_labor": "Analyse des violations des droits du travail en milieu carcéral, incluant le travail forcé, les salaires inférieurs au minimum légal et les conditions dangereuses.",
    "gig_workers": "Évaluation des pratiques des plateformes d'économie de gig : classification des travailleurs, protection sociale, algorithmes de tarification.",
    "water_access": "Surveillance du droit humain à l'eau potable selon la Résolution ONU A/RES/64/292 et les obligations CSDDD Art.8.",
    "ai_algorithmic_bias": "Détection des biais algorithmiques dans les systèmes d'IA : discrimination, manque de transparence, violations RGPD Art.22.",
    "deforestation": "Traçabilité des chaînes d'approvisionnement en huile de palme et leur impact sur la déforestation selon le règlement EU sur la déforestation 2023/1115.",
    "surveillance_capitalism": "Analyse de la monétisation des données personnelles par les grandes plateformes technologiques selon RGPD et CSDDD Art.13.",
    "mental_health_social_media": "Évaluation de l'impact des réseaux sociaux sur la santé mentale, particulièrement des mineurs, selon DSA et Online Safety Act.",
    "space_mining": "Surveillance des droits relatifs à l'exploitation minière spatiale selon le Traité de l'Espace de 1967 et les législations nationales émergentes.",
    "agricultural_pesticides": "Suivi des violations des droits à la santé liées aux pesticides agricoles selon la Convention de Rotterdam et les directives EU 2009/128/CE.",
    "homelessness_housing": "Analyse des droits au logement et des politiques d'exclusion selon le PIDESC Art.11 et la Charte Sociale Européenne.",
    "water_privatisation": "Évaluation de la conformité des entreprises de privatisation de l'eau avec le droit humain à l'eau selon ONU et CSDDD.",
}

CRITICAL_ALERT_TEMPLATES_FR = {
    "sourcing_non_certifie": "{entity}: approvisionnement non certifié détecté — non-conformité CSDDD Art.9 chaîne d'approvisionnement",
    "travail_force": "{entity}: indicateurs de travail forcé documentés — violation ILO Convention 29 et CSDDD Art.8",
    "destruction_habitat": "{entity}: destruction d'habitat critique documentée — non-conformité règlement déforestation EU 2023/1115",
    "donnees_non_consenties": "{entity}: collecte de données sans consentement explicite — violation RGPD Art.6 et CSDDD Art.13",
    "salaire_minimum": "{entity}: rémunération inférieure au salaire minimum légal — violation ILO Convention 131",
}

RISK_LEVEL_DESCRIPTIONS_FR = {
    "critique": "Violations graves documentées nécessitant une action immédiate. Score CSDDD ≥60/100.",
    "élevé": "Risques significatifs identifiés avec preuves documentaires. Score CSDDD 40-59/100.",
    "modéré": "Pratiques à surveiller avec engagement partiel observé. Score CSDDD 20-39/100.",
    "faible": "Conformité globalement satisfaisante avec bonnes pratiques identifiées. Score CSDDD <20/100.",
}


def generate_engine_narrative(engine_name: str, avg_composite: float, entity_count: int = 8) -> str:
    """Génère un narratif CSDDD pour un engine."""
    domain = engine_name.replace("_engine", "").replace("_", " ")
    description = DOMAIN_DESCRIPTIONS_FR.get(engine_name.replace("_engine", ""),
        f"Analyse de conformité CSDDD pour le domaine '{domain}' selon EU 2024/1760.")

    risk_level = "critique" if avg_composite >= 60 else "élevé" if avg_composite >= 40 else "modéré"

    return f"""## Rapport {domain.title()} — CSDDD Art.8-13

{description}

**Score moyen de conformité :** {avg_composite:.1f}/100 (risque {risk_level})

**Entités analysées :** {entity_count} entreprises/organisations

**Base réglementaire :**
- Directive CSDDD EU 2024/1760 (applicable 2027-07-26)
- Articles 8-13 : Devoir de diligence raisonnable
- ILO Conventions fondamentales
- Principes Directeurs ONU (UNGP)

**Niveaux de risque CSDDD :**
{chr(10).join(f"- **{level}** : {desc}" for level, desc in RISK_LEVEL_DESCRIPTIONS_FR.items())}
"""


def generate_ui_labels() -> dict:
    """Génère les labels UI pour les dashboards."""
    return {
        "fr": {
            "engine_title": "Moteur d'analyse",
            "entities_count": "{count} entités analysées",
            "confidence": "Confiance {pct}%",
            "last_update": "MAJ {date}",
            "critical_alerts": "Alertes critiques",
            "data_sources": "Sources de données",
            "composite_score": "Score composite",
            "estimated_index": "Index estimé",
            "risk_distribution": "Distribution des risques",
            "view_details": "Voir les détails",
            "overview": "Aperçu",
            "metrics": "Métriques",
            "sources": "Sources",
            "no_data": "Données non disponibles",
            "loading": "Chargement...",
            "error_502": "Service temporairement indisponible",
        },
        "en": {
            "engine_title": "Analysis Engine",
            "entities_count": "{count} entities analyzed",
            "confidence": "Confidence {pct}%",
            "last_update": "Updated {date}",
            "critical_alerts": "Critical Alerts",
            "data_sources": "Data Sources",
            "composite_score": "Composite Score",
            "estimated_index": "Estimated Index",
            "risk_distribution": "Risk Distribution",
            "view_details": "View Details",
            "overview": "Overview",
            "metrics": "Metrics",
            "sources": "Sources",
            "no_data": "Data unavailable",
            "loading": "Loading...",
            "error_502": "Service temporarily unavailable",
        }
    }


def run_creator(project_root: str = "/home/user/TEST") -> dict:
    root = Path(project_root)
    print(f"\n{BOLD}{CYAN}CaelumSwarm™ Content Creator Agent v{VERSION}{RESET}\n")

    # Générer la documentation des descriptions
    docs_dir = root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Fichier de labels UI
    labels = generate_ui_labels()
    labels_file = root / "lib" / "i18n" / "labels.json"
    labels_file.parent.mkdir(parents=True, exist_ok=True)
    labels_file.write_text(json.dumps(labels, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  {GREEN}✓{RESET} {labels_file} (labels FR/EN)")

    # Fichier de descriptions CSDDD
    descriptions_file = docs_dir / "engine-descriptions-fr.md"
    content = "# Descriptions des Engines CaelumSwarm™ (FR)\n\n"
    for engine, desc in DOMAIN_DESCRIPTIONS_FR.items():
        content += f"## {engine.replace('_', ' ').title()}\n{desc}\n\n"
    descriptions_file.write_text(content, encoding="utf-8")
    print(f"  {GREEN}✓{RESET} {descriptions_file}")

    # Générer un exemple de rapport narratif
    sample_narrative = generate_engine_narrative("conflict_minerals_engine", avg_composite=59.55)
    narrative_file = docs_dir / "sample-csddd-narrative.md"
    narrative_file.write_text(sample_narrative, encoding="utf-8")
    print(f"  {GREEN}✓{RESET} {narrative_file}")

    print(f"\n{GREEN}✓ Contenu généré avec succès{RESET}\n")

    return {
        "agent": AGENT_NAME,
        "version": VERSION,
        "generated_files": [str(labels_file), str(descriptions_file), str(narrative_file)],
        "languages": ["fr", "en"],
        "domains_described": len(DOMAIN_DESCRIPTIONS_FR),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/user/TEST")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_creator(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
