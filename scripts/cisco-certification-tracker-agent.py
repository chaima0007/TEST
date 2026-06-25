#!/usr/bin/env python3
"""Cisco Certification Tracker Agent — CaelumSwarm™
Tracks free Cisco NetAcad courses relevant to Caelum Partners (tech compliance team).
Generates a 6-month learning plan prioritizing cybersecurity + Python + data analytics.
Outputs JSON to docs/swarm-memory/cisco-certifications.json.
"""
import json
import math
from pathlib import Path
from datetime import datetime, timezone

AGENT_NAME = "CiscoCertificationTrackerAgent"
VERSION = "1.0.0"

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

ROOT        = Path(__file__).resolve().parent.parent
MEMORY_DIR  = ROOT / "docs" / "swarm-memory"
OUTPUT_PATH = MEMORY_DIR / "cisco-certifications.json"

# ---------------------------------------------------------------------------
# Cisco NetAcad catalog — 2026
# ---------------------------------------------------------------------------

COURSES = [
    {
        "nom":                "Introduction to Cybersecurity",
        "plateforme":         "Cisco NetAcad",
        "duree_heures":       15,
        "certif_associee":    "Cisco Intro to Cybersecurity Badge",
        "pertinence_caelum":  9,
        "lien":               "https://www.netacad.com/courses/cybersecurity/introduction-cybersecurity",
        "statut":             "non_commencé",
        "modules_completes":  [],
        "modules_total":      5,
        "gratuit":            True,
        "note_pertinence":    (
            "Point d'entrée essentiel: menaces cyber, sécurité données, conformité RGPD/CSDDD. "
            "Recommandé pour tout le personnel Caelum."
        ),
        "priorite":           1,
        "domaines_couverts":  [
            "Threat landscape", "Network security basics", "Data protection",
            "Security principles", "Career paths in cybersecurity",
        ],
        "categorie":          "cybersecurity",
    },
    {
        "nom":                "Cybersecurity Essentials",
        "plateforme":         "Cisco NetAcad",
        "duree_heures":       30,
        "certif_associee":    "Cisco Cybersecurity Essentials Badge",
        "pertinence_caelum":  9,
        "lien":               "https://www.netacad.com/courses/cybersecurity/cybersecurity-essentials",
        "statut":             "non_commencé",
        "modules_completes":  [],
        "modules_total":      9,
        "gratuit":            True,
        "note_pertinence":    (
            "Approfondissement: cryptographie, infrastructure PKI, défense périmétrique. "
            "Critique pour sécurité API Caelum et protection des engines swarm."
        ),
        "priorite":           1,
        "domaines_couverts":  [
            "Cryptography", "Access control", "PKI", "Endpoint security",
            "Vulnerability assessment", "Network defense",
        ],
        "categorie":          "cybersecurity",
    },
    {
        "nom":                "CyberOps Associate (prépare examen 200-201)",
        "plateforme":         "Cisco NetAcad",
        "duree_heures":       70,
        "certif_associee":    "Cisco Certified CyberOps Associate (examen 200-201 payant)",
        "pertinence_caelum":  8,
        "lien":               "https://www.netacad.com/courses/cybersecurity/cyberops-associate",
        "statut":             "non_commencé",
        "modules_completes":  [],
        "modules_total":      28,
        "gratuit":            True,
        "note_gratuite":      "Formation gratuite; examen 200-201 payant (~$330 USD) pour la certification officielle",
        "note_pertinence":    (
            "Prépare aux opérations SOC: détection d'intrusion, analyse forensique, réponse aux incidents. "
            "Idéal pour le profil tech compliance de Caelum."
        ),
        "priorite":           2,
        "domaines_couverts":  [
            "Security monitoring", "Host-based analysis", "Network intrusion analysis",
            "Security policies", "Incident response", "Linux fundamentals",
        ],
        "categorie":          "cybersecurity",
    },
    {
        "nom":                "Networking Essentials",
        "plateforme":         "Cisco NetAcad",
        "duree_heures":       70,
        "certif_associee":    "Cisco Networking Essentials Badge",
        "pertinence_caelum":  6,
        "lien":               "https://www.netacad.com/courses/networking/networking-essentials",
        "statut":             "non_commencé",
        "modules_completes":  [],
        "modules_total":      20,
        "gratuit":            True,
        "note_pertinence":    (
            "Fondamentaux réseau utiles pour comprendre l'infrastructure cloud Caelum "
            "et les communications API inter-agents."
        ),
        "priorite":           4,
        "domaines_couverts":  [
            "Network protocols", "IP addressing", "Routing basics",
            "Wireless networks", "Network troubleshooting",
        ],
        "categorie":          "networking",
    },
    {
        "nom":                "Python Essentials 1",
        "plateforme":         "Cisco NetAcad",
        "duree_heures":       40,
        "certif_associee":    "PCEP — Certified Entry-Level Python Programmer (examen OpenEDG)",
        "pertinence_caelum":  10,
        "lien":               "https://www.netacad.com/courses/programming/pcap-programming-essentials-python",
        "statut":             "non_commencé",
        "modules_completes":  [],
        "modules_total":      9,
        "gratuit":            True,
        "note_pertinence":    (
            "CRITIQUE pour Caelum: tous les swarm engines sont en Python. "
            "Maîtrise Python = capacité à auditer, modifier et valider les engines de conformité."
        ),
        "priorite":           1,
        "domaines_couverts":  [
            "Python syntax", "Data types", "Control flow", "Functions",
            "Lists/tuples/dicts", "Modules", "Exceptions",
        ],
        "categorie":          "python",
    },
    {
        "nom":                "Python Essentials 2",
        "plateforme":         "Cisco NetAcad",
        "duree_heures":       40,
        "certif_associee":    "PCAP — Certified Associate in Python Programming (examen OpenEDG)",
        "pertinence_caelum":  10,
        "lien":               "https://www.netacad.com/courses/programming/pcap-programming-essentials-python",
        "statut":             "non_commencé",
        "modules_completes":  [],
        "modules_total":      8,
        "gratuit":            True,
        "note_pertinence":    (
            "Avancé Python: OOP, fichiers, générateurs, regex. "
            "Essentiel pour comprendre les dataclasses des engines CaelumSwarm."
        ),
        "priorite":           1,
        "domaines_couverts":  [
            "OOP in Python", "File I/O", "Generators", "Regex",
            "Standard library", "List comprehensions", "Decorators",
        ],
        "categorie":          "python",
    },
    {
        "nom":                "Data Analytics Essentials",
        "plateforme":         "Cisco NetAcad",
        "duree_heures":       30,
        "certif_associee":    "Cisco Data Analytics Essentials Badge",
        "pertinence_caelum":  8,
        "lien":               "https://www.netacad.com/courses/data-science/data-analytics-essentials",
        "statut":             "non_commencé",
        "modules_completes":  [],
        "modules_total":      9,
        "gratuit":            True,
        "note_pertinence":    (
            "Analyse des données de conformité, visualisation des scores ESG, "
            "compréhension statistique des risk indices."
        ),
        "priorite":           2,
        "domaines_couverts":  [
            "Data lifecycle", "Statistical analysis", "Data visualization",
            "SQL basics", "Tableau introduction", "Business intelligence",
        ],
        "categorie":          "data",
    },
    {
        "nom":                "Network Security",
        "plateforme":         "Cisco NetAcad",
        "duree_heures":       70,
        "certif_associee":    "Prépare partiellement CCNA Security",
        "pertinence_caelum":  7,
        "lien":               "https://www.netacad.com/courses/cybersecurity/network-security",
        "statut":             "non_commencé",
        "modules_completes":  [],
        "modules_total":      14,
        "gratuit":            True,
        "note_pertinence":    (
            "Sécurisation réseau avancée pour l'infrastructure Caelum: "
            "firewalls, VPN, IDS/IPS."
        ),
        "priorite":           3,
        "domaines_couverts":  [
            "Firewall configuration", "VPN", "IDS/IPS", "ACLs",
            "AAA", "Network monitoring",
        ],
        "categorie":          "cybersecurity",
    },
    {
        "nom":                "IoT Fundamentals",
        "plateforme":         "Cisco NetAcad",
        "duree_heures":       20,
        "certif_associee":    "Cisco IoT Fundamentals Badge",
        "pertinence_caelum":  5,
        "lien":               "https://www.netacad.com/courses/iot/iot-fundamentals-iot-and-digital-transformation",
        "statut":             "non_commencé",
        "modules_completes":  [],
        "modules_total":      4,
        "gratuit":            True,
        "note_pertinence":    (
            "Contexte supply chain IoT utile pour les engines traçabilité Caelum; "
            "moins prioritaire que cyber/Python/data."
        ),
        "priorite":           5,
        "domaines_couverts":  [
            "IoT architecture", "Sensors and devices", "IoT protocols",
            "IoT security", "Digital transformation",
        ],
        "categorie":          "iot",
    },
]

# ---------------------------------------------------------------------------
# Roadmap logic
# ---------------------------------------------------------------------------

CATEGORY_WEIGHTS = {
    "python":        1.0,
    "cybersecurity": 0.95,
    "data":          0.85,
    "networking":    0.60,
    "iot":           0.40,
}


def priority_score(course: dict) -> float:
    cat_weight = CATEGORY_WEIGHTS.get(course["categorie"], 0.5)
    prio_norm  = 1.0 / course["priorite"]
    pert_norm  = course["pertinence_caelum"] / 10.0
    # Quick-win bonus for short courses
    quick_win  = 1.0 if course["duree_heures"] <= 20 else 0.0
    return round(0.45 * pert_norm + 0.30 * cat_weight + 0.20 * prio_norm + 0.05 * quick_win, 4)


def build_6_month_plan(courses: list) -> list:
    """Assign courses to a 6-month calendar at ~20h/month."""
    sorted_courses = sorted(courses, key=priority_score, reverse=True)
    monthly_capacity = 20
    plan = []
    current_month = 1

    for course in sorted_courses:
        duration   = course["duree_heures"]
        months_req = math.ceil(duration / monthly_capacity)
        start      = current_month
        end        = min(start + months_req - 1, 6)

        plan.append({
            "cours":              course["nom"],
            "categorie":          course["categorie"],
            "mois_debut":         start,
            "mois_fin":           end if end <= 6 else "Beyond M6",
            "heures":             duration,
            "pertinence_caelum":  course["pertinence_caelum"],
            "priorite_score":     priority_score(course),
            "certif_associee":    course["certif_associee"],
            "statut":             course["statut"],
        })
        current_month = (end if isinstance(end, int) else 6) + 1

        if current_month > 6:
            for remaining in sorted_courses[sorted_courses.index(course) + 1:]:
                plan.append({
                    "cours":             remaining["nom"],
                    "categorie":         remaining["categorie"],
                    "mois_debut":        "Beyond M6",
                    "mois_fin":          "Beyond M6",
                    "heures":            remaining["duree_heures"],
                    "pertinence_caelum": remaining["pertinence_caelum"],
                    "priorite_score":    priority_score(remaining),
                    "certif_associee":   remaining["certif_associee"],
                    "statut":            remaining["statut"],
                })
            break

    return plan


def category_summary(courses: list) -> dict:
    from collections import defaultdict
    summary = defaultdict(lambda: {"count": 0, "heures": 0, "avg_pertinence": 0})
    for c in courses:
        cat = c["categorie"]
        summary[cat]["count"] += 1
        summary[cat]["heures"] += c["duree_heures"]
        summary[cat]["avg_pertinence"] += c["pertinence_caelum"]
    for cat in summary:
        n = summary[cat]["count"]
        summary[cat]["avg_pertinence"] = round(summary[cat]["avg_pertinence"] / n, 1)
    return dict(summary)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  Cisco Certification Tracker Agent v{VERSION}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    print(f"{CYAN}[1/3] Cisco NetAcad catalog ({len(COURSES)} courses):{RESET}")
    sorted_display = sorted(COURSES, key=priority_score, reverse=True)
    for c in sorted_display:
        score = priority_score(c)
        cat_color = (
            RED    if c["categorie"] == "python"        else
            YELLOW if c["categorie"] == "cybersecurity" else
            CYAN   if c["categorie"] == "data"          else
            RESET
        )
        print(
            f"  {cat_color}[{c['categorie']:14s}]{RESET} "
            f"{c['nom'][:48]:48s} "
            f"pert={c['pertinence_caelum']}/10  score={score:.3f}  {c['duree_heures']}h"
        )

    print(f"\n{CYAN}[2/3] Building 6-month learning plan (20h/month)...{RESET}")
    roadmap = build_6_month_plan(COURSES)
    cat_summary = category_summary(COURSES)

    print(f"\n{BOLD}6-Month Cisco Roadmap for Tech Compliance Team:{RESET}")
    for item in roadmap:
        start = item["mois_debut"]
        end   = item["mois_fin"]
        if isinstance(start, int):
            month_str = f"M{start:02d}–M{end}" if start != end else f"M{start:02d}     "
        else:
            month_str = f"After M6"
        cat_color = (
            RED    if item["categorie"] == "python"        else
            YELLOW if item["categorie"] == "cybersecurity" else
            CYAN   if item["categorie"] == "data"          else
            RESET
        )
        print(
            f"  {month_str}  {cat_color}[{item['categorie']:14s}]{RESET}  "
            f"{item['cours'][:45]:45s}  {item['heures']}h"
        )

    print(f"\n{BOLD}Category breakdown:{RESET}")
    for cat, stats in sorted(cat_summary.items(), key=lambda x: -x[1]["avg_pertinence"]):
        print(
            f"  {cat:14s}: {stats['count']} course(s), "
            f"{stats['heures']}h total, avg pertinence={stats['avg_pertinence']}/10"
        )

    print(f"\n{CYAN}[3/3] Writing output...{RESET}")

    total_hours = sum(c["duree_heures"] for c in COURSES)
    m6_courses  = [i for i in roadmap if isinstance(i["mois_debut"], int)]

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent":        AGENT_NAME,
        "version":      VERSION,
        "context":      "Caelum Partners — tech compliance team, 2026",
        "summary": {
            "total_courses":     len(COURSES),
            "all_gratuit":       all(c["gratuit"] for c in COURSES),
            "heures_totales":    total_hours,
            "heures_mois_1_6":   sum(i["heures"] for i in m6_courses),
            "courses_en_6_mois": len(m6_courses),
        },
        "category_summary": cat_summary,
        "courses": [
            {**c, "priorite_score": priority_score(c)}
            for c in COURSES
        ],
        "roadmap_6_mois": roadmap,
        "recommendations": [
            {
                "phase":    "Semaine 1 (immédiat)",
                "action":   "Introduction to Cybersecurity + Python Essentials 1",
                "raison":   "Quick wins: 15h + 40h, pertinence 9/10 et 10/10",
                "heures":   55,
            },
            {
                "phase":    "Mois 1–2",
                "action":   "Cybersecurity Essentials + Python Essentials 2",
                "raison":   "Socle complet sécurité + maîtrise Python pour auditer les engines",
                "heures":   70,
            },
            {
                "phase":    "Mois 3–4",
                "action":   "CyberOps Associate + Data Analytics Essentials",
                "raison":   "Niveau opérationnel SOC + analyse des données de conformité",
                "heures":   100,
            },
            {
                "phase":    "Mois 5–6",
                "action":   "Network Security",
                "raison":   "Sécurisation de l'infrastructure Caelum",
                "heures":   70,
            },
            {
                "phase":    "Au-delà M6",
                "action":   "Networking Essentials + IoT Fundamentals",
                "raison":   "Compléments pertinents pour supply chain et infrastructure",
                "heures":   90,
            },
        ],
        "note_exams": (
            "Tous les cours sont 100% gratuits sur netacad.com. "
            "Les certifications officielles Cisco (CyberOps 200-201) nécessitent un examen payant. "
            "Les badges Cisco NetAcad sont gratuits et partageables sur LinkedIn."
        ),
    }

    OUTPUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  CISCO CERTIFICATION SUMMARY{RESET}")
    print(f"{'='*60}")
    print(f"  Total courses         : {len(COURSES)}")
    print(f"  All free (NetAcad)    : {GREEN}YES{RESET}")
    print(f"  Total hours           : {total_hours}h")
    print(f"  Covered in 6 months   : {len(m6_courses)} courses")
    print(f"{'='*60}\n")
    print(f"{GREEN}Top 3 priorities for Caelum tech team:{RESET}")
    top3 = sorted(COURSES, key=priority_score, reverse=True)[:3]
    for i, c in enumerate(top3, 1):
        print(f"  {i}. {c['nom']} [{c['categorie']}] — pertinence {c['pertinence_caelum']}/10 — {c['duree_heures']}h")
    print(f"\n{GREEN}[OK] Output written to: {OUTPUT_PATH}{RESET}\n")


if __name__ == "__main__":
    main()
