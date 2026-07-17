#!/usr/bin/env python3
"""Google Certification Tracker Agent — CaelumSwarm™
Tracks free Google certifications relevant to Caelum Partners (AI compliance startup).
Generates a personalized roadmap and 12-month learning plan.
Outputs JSON to docs/swarm-memory/google-certifications.json.
"""
import json
import math
from pathlib import Path
from datetime import datetime, timezone, timedelta

AGENT_NAME = "GoogleCertificationTrackerAgent"
VERSION = "1.0.0"

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

ROOT        = Path(__file__).resolve().parent.parent
MEMORY_DIR  = ROOT / "docs" / "swarm-memory"
OUTPUT_PATH = MEMORY_DIR / "google-certifications.json"

# ---------------------------------------------------------------------------
# Certification catalog — Google 2026
# ---------------------------------------------------------------------------

CERTIFICATIONS = [
    {
        "nom":               "Google Cybersecurity Certificate",
        "plateforme":        "Coursera",
        "duree_heures":      182,
        "niveau":            "débutant",
        "pertinence_caelum": 9,
        "lien_inscription":  "https://www.coursera.org/professional-certificates/google-cybersecurity",
        "statut":            "non_commencé",
        "modules_completes": [],
        "modules_total":     8,
        "gratuit":           True,
        "note_pertinence":   (
            "Fondamental pour Caelum: sécurité des données clients, conformité CSDDD, "
            "protection infrastructure IA"
        ),
        "priorite":          1,
        "domaines_couverts": [
            "Network security", "Linux", "SQL", "Python basics",
            "SIEM tools", "Incident response", "Risk management",
        ],
    },
    {
        "nom":               "Google Data Analytics Certificate",
        "plateforme":        "Coursera",
        "duree_heures":      180,
        "niveau":            "débutant",
        "pertinence_caelum": 8,
        "lien_inscription":  "https://www.coursera.org/professional-certificates/google-data-analytics",
        "statut":            "non_commencé",
        "modules_completes": [],
        "modules_total":     8,
        "gratuit":           True,
        "note_pertinence":   (
            "Clé pour analyser les scores ESG, risk indices et swarm engine outputs; "
            "visualisation des données de conformité"
        ),
        "priorite":          2,
        "domaines_couverts": [
            "Spreadsheets", "SQL", "Tableau", "R programming",
            "Data cleaning", "Visualization", "Case studies",
        ],
    },
    {
        "nom":               "Google AI Essentials",
        "plateforme":        "Coursera",
        "duree_heures":      10,
        "niveau":            "débutant",
        "pertinence_caelum": 9,
        "lien_inscription":  "https://www.coursera.org/learn/google-ai-essentials",
        "statut":            "non_commencé",
        "modules_completes": [],
        "modules_total":     5,
        "gratuit":           True,
        "note_pertinence":   (
            "Directement aligné avec le positionnement IA de Caelum; "
            "compréhension des LLM et outils IA pour conformité"
        ),
        "priorite":          1,
        "domaines_couverts": [
            "Generative AI", "Prompt engineering", "AI tools",
            "Responsible AI", "AI in the workplace",
        ],
    },
    {
        "nom":               "Google Project Management Certificate",
        "plateforme":        "Coursera",
        "duree_heures":      180,
        "niveau":            "débutant",
        "pertinence_caelum": 7,
        "lien_inscription":  "https://www.coursera.org/professional-certificates/google-project-management",
        "statut":            "non_commencé",
        "modules_completes": [],
        "modules_total":     6,
        "gratuit":           True,
        "note_pertinence":   (
            "Utile pour gérer les projets de conformité, audits clients et déploiements swarm; "
            "méthodologies Agile pour équipe startup"
        ),
        "priorite":          3,
        "domaines_couverts": [
            "Project lifecycle", "Agile & Scrum", "Risk management",
            "Stakeholder communication", "Budgeting", "Capstone project",
        ],
    },
    {
        "nom":               "Google UX Design Certificate",
        "plateforme":        "Coursera",
        "duree_heures":      204,
        "niveau":            "débutant",
        "pertinence_caelum": 5,
        "lien_inscription":  "https://www.coursera.org/professional-certificates/google-ux-design",
        "statut":            "non_commencé",
        "modules_completes": [],
        "modules_total":     7,
        "gratuit":           True,
        "note_pertinence":   (
            "Pertinent pour améliorer l'UX des dashboards Caelum et l'expérience utilisateur "
            "des rapports de conformité; moins prioritaire que cyber/data/AI"
        ),
        "priorite":          4,
        "domaines_couverts": [
            "User research", "Wireframing", "Prototyping",
            "Figma", "Usability testing", "Design systems",
        ],
    },
    {
        "nom":               "Google Digital Marketing & E-commerce Certificate",
        "plateforme":        "Coursera",
        "duree_heures":      168,
        "niveau":            "débutant",
        "pertinence_caelum": 6,
        "lien_inscription":  "https://www.coursera.org/professional-certificates/google-digital-marketing-ecommerce",
        "statut":            "non_commencé",
        "modules_completes": [],
        "modules_total":     7,
        "gratuit":           True,
        "note_pertinence":   (
            "Utile pour le go-to-market Caelum, acquisition clients B2B conformité, "
            "stratégie contenu CSDDD"
        ),
        "priorite":          4,
        "domaines_couverts": [
            "SEO/SEM", "Email marketing", "Social media",
            "Analytics", "E-commerce", "Marketing strategy",
        ],
    },
    {
        "nom":               "Google Cloud Associate Cloud Engineer",
        "plateforme":        "Google Cloud Skills Boost",
        "duree_heures":      120,
        "niveau":            "intermédiaire",
        "pertinence_caelum": 8,
        "lien_inscription":  "https://cloud.google.com/learn/certification/cloud-engineer",
        "statut":            "non_commencé",
        "modules_completes": [],
        "modules_total":     10,
        "gratuit":           False,
        "note_gratuite":     "Formation gratuite sur Cloud Skills Boost; examen payant (~$200 USD)",
        "note_pertinence":   (
            "Infrastructure cloud pour déploiement Caelum Swarm, sécurité cloud "
            "et scalabilité des engines IA"
        ),
        "priorite":          2,
        "domaines_couverts": [
            "GCP infrastructure", "Compute Engine", "GKE",
            "Cloud Storage", "IAM", "Networking", "Monitoring",
        ],
    },
]

# ---------------------------------------------------------------------------
# Roadmap generation
# ---------------------------------------------------------------------------

def calculate_priority_score(cert: dict) -> float:
    """Score = pertinence_caelum (weight 0.6) + inverse(priorite) (weight 0.3) + short_duration bonus (0.1)"""
    pertinence = cert["pertinence_caelum"]
    # Normalize priority (1=best → score 1.0, 4=lowest → score 0.25)
    prio_score = 1.0 / cert["priorite"]
    # Duration bonus: shorter = better for quick wins
    max_hours = max(c["duree_heures"] for c in CERTIFICATIONS)
    duration_score = 1.0 - (cert["duree_heures"] / max_hours)
    return round(0.6 * pertinence / 10 + 0.3 * prio_score + 0.1 * duration_score, 4)


def build_12_month_plan(certs: list) -> list:
    """Assign certifications to months based on priority score and duration."""
    sorted_certs = sorted(certs, key=lambda c: calculate_priority_score(c), reverse=True)

    plan = []
    current_month = 1
    current_month_hours = 0
    monthly_capacity = 20  # hours per month (realistic for a startup team member)

    for cert in sorted_certs:
        duration = cert["duree_heures"]
        months_needed = math.ceil(duration / monthly_capacity)
        start_month = current_month
        end_month = min(start_month + months_needed - 1, 12)
        plan.append({
            "certification": cert["nom"],
            "mois_debut":    start_month,
            "mois_fin":      end_month,
            "heures_totales": duration,
            "heures_par_mois": monthly_capacity,
            "priorite_score": calculate_priority_score(cert),
            "statut":        cert["statut"],
            "gratuit":       cert.get("gratuit", True),
        })
        current_month = end_month + 1
        if current_month > 12:
            # Queue remaining for year 2
            for remaining in sorted_certs[sorted_certs.index(cert) + 1:]:
                plan.append({
                    "certification": remaining["nom"],
                    "mois_debut":    "Year 2",
                    "mois_fin":      "Year 2",
                    "heures_totales": remaining["duree_heures"],
                    "heures_par_mois": monthly_capacity,
                    "priorite_score": calculate_priority_score(remaining),
                    "statut":        remaining["statut"],
                    "gratuit":       remaining.get("gratuit", True),
                })
            break

    return plan

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  Google Certification Tracker Agent v{VERSION}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    print(f"{CYAN}[1/3] Loading Google certification catalog ({len(CERTIFICATIONS)} certs)...{RESET}")
    for cert in CERTIFICATIONS:
        score = calculate_priority_score(cert)
        free_label = f"{GREEN}GRATUIT{RESET}" if cert.get("gratuit", True) else f"{YELLOW}Examen payant{RESET}"
        print(
            f"  [{cert['priorite']}] {cert['nom']:55s} "
            f"pertinence={cert['pertinence_caelum']}/10  "
            f"score={score:.3f}  {free_label}"
        )

    print(f"\n{CYAN}[2/3] Generating personalized 12-month roadmap for Caelum Partners...{RESET}")
    roadmap = build_12_month_plan(CERTIFICATIONS)

    print(f"\n{BOLD}12-Month Learning Plan:{RESET}")
    for item in roadmap:
        month_str = (
            f"M{item['mois_debut']:02d}–M{item['mois_fin']:02d}"
            if isinstance(item["mois_debut"], int)
            else "Year 2   "
        )
        free_icon = f"{GREEN}✓free{RESET}" if item["gratuit"] else f"{YELLOW}paid€{RESET}"
        print(
            f"  {month_str}  {free_icon}  {item['certification'][:50]:50s}"
            f"  {item['heures_totales']}h"
        )

    total_hours_yr1 = sum(
        i["heures_totales"] for i in roadmap if isinstance(i["mois_debut"], int)
    )
    total_free = sum(1 for c in CERTIFICATIONS if c.get("gratuit", True))

    print(f"\n{CYAN}[3/3] Writing output...{RESET}")

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent":        AGENT_NAME,
        "version":      VERSION,
        "context":      "Caelum Partners — AI compliance startup, 2026",
        "summary": {
            "total_certifications":    len(CERTIFICATIONS),
            "certifications_gratuites": total_free,
            "certifications_paid_exam": len(CERTIFICATIONS) - total_free,
            "heures_totales":          sum(c["duree_heures"] for c in CERTIFICATIONS),
            "heures_annee_1":          total_hours_yr1,
            "mois_couverts":           min(12, len([i for i in roadmap if isinstance(i["mois_debut"], int)])),
        },
        "certifications": [
            {**c, "priorite_score": calculate_priority_score(c)}
            for c in CERTIFICATIONS
        ],
        "roadmap_12_mois":  roadmap,
        "recommendations": [
            {
                "priorite": "IMMEDIATE",
                "action":   "Commencer Google AI Essentials",
                "raison":   "Seulement ~10h, pertinence 9/10, positionne Caelum sur l'IA responsable",
                "lien":     "https://www.coursera.org/learn/google-ai-essentials",
            },
            {
                "priorite": "MOIS_1_2",
                "action":   "Lancer Google Cybersecurity Certificate",
                "raison":   "Pertinence 9/10 pour la sécurité des données CSDDD; 8 modules structurés",
                "lien":     "https://www.coursera.org/professional-certificates/google-cybersecurity",
            },
            {
                "priorite": "MOIS_3_6",
                "action":   "Google Data Analytics + Cloud ACE training",
                "raison":   "Data Analytics (8/10) pour analyser les outputs swarm; Cloud pour l'infra",
                "lien":     "https://cloud.google.com/learn/training",
            },
            {
                "priorite": "MOIS_7_12",
                "action":   "Google Project Management Certificate",
                "raison":   "Formaliser la gestion de projets conformité clients",
                "lien":     "https://www.coursera.org/professional-certificates/google-project-management",
            },
        ],
    }

    OUTPUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  GOOGLE CERTIFICATION SUMMARY{RESET}")
    print(f"{'='*60}")
    print(f"  Total certifications  : {len(CERTIFICATIONS)}")
    print(f"  Totalement gratuits   : {total_free}")
    print(f"  Heures totales        : {sum(c['duree_heures'] for c in CERTIFICATIONS)}h")
    print(f"  Heures année 1        : {total_hours_yr1}h")
    print(f"{'='*60}\n")
    print(f"{GREEN}Top priority for Caelum Partners:{RESET}")
    top3 = sorted(CERTIFICATIONS, key=calculate_priority_score, reverse=True)[:3]
    for i, c in enumerate(top3, 1):
        print(f"  {i}. {c['nom']} — pertinence {c['pertinence_caelum']}/10")
    print(f"\n{GREEN}[OK] Output written to: {OUTPUT_PATH}{RESET}\n")


if __name__ == "__main__":
    main()
