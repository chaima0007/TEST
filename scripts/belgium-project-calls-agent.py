#!/usr/bin/env python3
"""
Belgium Project Calls Agent — Caelum Partners SPRL
Surveille et analyse les appels à projets/financements en Belgique
pertinents pour une startup compliance/ESG/CSDDD basée à Bruxelles.
"""

import json
import re
from datetime import datetime, timedelta


# ─────────────────────────────────────────────
# Profil Caelum Partners — mots-clés de matching
# ─────────────────────────────────────────────
CAELUM_KEYWORDS = [
    "droits humains", "conformité", "ESG", "CSDDD", "supply chain",
    "due diligence", "technologie", "IA", "SaaS", "startup", "compliance",
    "impact social", "chaîne d'approvisionnement", "durabilité", "numérique",
    "intelligence artificielle", "gouvernance", "reporting", "transparence",
    "responsabilité", "RSE", "entreprise", "PME", "innovation",
]

# ─────────────────────────────────────────────
# Sources surveillées
# ─────────────────────────────────────────────
SOURCES = [
    "Innoviris (Bruxelles)",
    "Plan de relance belge",
    "FEDER/FSE+ Fonds structurels européens",
    "Wallonie Entreprendre",
    "Agence du Numérique",
    "BEI (Banque Européenne d'Investissement)",
    "Horizon Europe",
    "EIC Accelerator",
]


# ─────────────────────────────────────────────
# Données simulées — appels à projets réalistes 2026
# ─────────────────────────────────────────────
def get_simulated_calls():
    today = datetime.now()
    return [
        {
            "nom": "Innoviris Bridge — Projets de transition numérique ESG",
            "organisme": "Innoviris (Bruxelles)",
            "type": "subvention",
            "montant_max": 250000,
            "montant_min": 50000,
            "deadline": (today + timedelta(days=45)).strftime("%Y-%m-%d"),
            "date_ouverture": (today - timedelta(days=30)).strftime("%Y-%m-%d"),
            "url": "https://innoviris.brussels/fr/nos-soutiens/bridge",
            "description": (
                "Soutien aux PME bruxelloises développant des solutions numériques "
                "innovantes contribuant à la transition durable, la conformité ESG "
                "et la responsabilité sociale des entreprises. Priorité aux outils "
                "SaaS facilitant le reporting et la due diligence."
            ),
            "mots_cles_source": [
                "numérique", "ESG", "PME", "SaaS", "durabilité",
                "conformité", "reporting", "impact social",
            ],
            "secteurs_eligibles": ["Tech", "SaaS", "ESG", "Compliance", "IA"],
            "region": "Bruxelles-Capitale",
        },
        {
            "nom": "EIC Accelerator 2026 — Tech for Social Impact",
            "organisme": "EIC Accelerator",
            "type": "grant + equity",
            "montant_max": 2500000,
            "montant_min": 500000,
            "deadline": (today + timedelta(days=62)).strftime("%Y-%m-%d"),
            "date_ouverture": (today - timedelta(days=60)).strftime("%Y-%m-%d"),
            "url": "https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en",
            "description": (
                "Programme phare de la Commission européenne pour les startups "
                "deeptech et impact. Priorité 2026 : IA responsable, supply chain "
                "transparency, solutions CSDDD pour PME et grands groupes. "
                "Composante subvention (70%) + prise de participation (30%)."
            ),
            "mots_cles_source": [
                "startup", "IA", "CSDDD", "supply chain", "impact social",
                "due diligence", "innovation", "deeptech",
            ],
            "secteurs_eligibles": [
                "IA", "LegalTech", "RegTech", "ESG", "Supply Chain",
            ],
            "region": "Union Européenne (toutes régions)",
        },
        {
            "nom": "Horizon Europe — Cluster 6 : Systèmes alimentaires, bioéconomie & droits humains",
            "organisme": "Horizon Europe",
            "type": "subvention R&D",
            "montant_max": 3000000,
            "montant_min": 1000000,
            "deadline": (today + timedelta(days=78)).strftime("%Y-%m-%d"),
            "date_ouverture": (today - timedelta(days=14)).strftime("%Y-%m-%d"),
            "url": "https://research-and-innovation.ec.europa.eu/funding/funding-opportunities/horizon-europe_fr",
            "description": (
                "Appel à propositions pour des outils technologiques facilitant "
                "la transparence des chaînes d'approvisionnement mondiales, "
                "le respect des droits humains et la conformité avec les nouvelles "
                "directives EU (CSDDD, CSRD). Consortium minimum 3 partenaires EU requis."
            ),
            "mots_cles_source": [
                "droits humains", "chaîne d'approvisionnement", "CSDDD", "conformité",
                "transparence", "technologie", "IA", "gouvernance",
            ],
            "secteurs_eligibles": ["Recherche", "Tech", "ESG", "Compliance"],
            "region": "Union Européenne",
        },
        {
            "nom": "Plan de Relance Belge — Axe Numérique : Transformation PME",
            "organisme": "Plan de relance belge",
            "type": "subvention",
            "montant_max": 500000,
            "montant_min": 100000,
            "deadline": (today + timedelta(days=22)).strftime("%Y-%m-%d"),
            "date_ouverture": (today - timedelta(days=90)).strftime("%Y-%m-%d"),
            "url": "https://planderelance.belgique.be/fr/numerique",
            "description": (
                "Financement des projets numériques belges contribuant à la "
                "résilience économique post-COVID et à la compétitivité durable. "
                "Priorité aux solutions SaaS B2B, IA appliquée et outils de "
                "conformité réglementaire pour PME et ETI."
            ),
            "mots_cles_source": [
                "numérique", "SaaS", "PME", "IA", "conformité", "startup",
                "responsabilité", "RSE",
            ],
            "secteurs_eligibles": ["Numérique", "SaaS", "IA", "Compliance"],
            "region": "Belgique",
        },
        {
            "nom": "FEDER Brussels Invest — Innovation Sociale & Technologique",
            "organisme": "FEDER/FSE+ Fonds structurels européens",
            "type": "subvention FEDER",
            "montant_max": 800000,
            "montant_min": 200000,
            "deadline": (today + timedelta(days=110)).strftime("%Y-%m-%d"),
            "date_ouverture": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
            "url": "https://feder.brussels/fr/appels-projets",
            "description": (
                "Co-financement européen pour projets d'innovation sociale et "
                "technologique en Région de Bruxelles-Capitale. Focus 2026 : "
                "outils numériques pour l'inclusion, la gouvernance d'entreprise "
                "responsable, le reporting ESG automatisé et la due diligence "
                "en droits humains."
            ),
            "mots_cles_source": [
                "innovation", "ESG", "droits humains", "gouvernance", "numérique",
                "reporting", "due diligence", "impact social", "conformité",
            ],
            "secteurs_eligibles": ["Tech", "Innovation sociale", "ESG", "Governance"],
            "region": "Bruxelles-Capitale",
        },
        {
            "nom": "BEI — InvestEU : Financement Régtech & Compliance Tech",
            "organisme": "BEI (Banque Européenne d'Investissement)",
            "type": "prêt + garantie",
            "montant_max": 5000000,
            "montant_min": 500000,
            "deadline": (today + timedelta(days=180)).strftime("%Y-%m-%d"),
            "date_ouverture": (today - timedelta(days=120)).strftime("%Y-%m-%d"),
            "url": "https://www.eib.org/fr/products/investeu/index.htm",
            "description": (
                "Programme InvestEU de la BEI : prêts et garanties pour entreprises "
                "innovantes dans les secteurs RegTech, LegalTech et Compliance Tech. "
                "Financement de la mise à l'échelle de solutions automatisant la "
                "conformité CSDDD, CSRD, et la due diligence en droits humains."
            ),
            "mots_cles_source": [
                "compliance", "RegTech", "CSDDD", "due diligence", "innovation",
                "SaaS", "croissance", "entreprise", "gouvernance",
            ],
            "secteurs_eligibles": ["RegTech", "LegalTech", "Compliance", "Fintech"],
            "region": "Union Européenne",
        },
    ]


# ─────────────────────────────────────────────
# Calcul du score de pertinence
# ─────────────────────────────────────────────
def compute_relevance_score(call: dict) -> tuple[int, list[str]]:
    """
    Score de pertinence 0-100 basé sur la correspondance des mots-clés
    entre l'appel et le profil Caelum Partners.
    """
    text_to_search = (
        call.get("description", "").lower()
        + " "
        + " ".join(call.get("mots_cles_source", [])).lower()
        + " "
        + " ".join(call.get("secteurs_eligibles", [])).lower()
        + " "
        + call.get("nom", "").lower()
    )

    matched_keywords = []
    for kw in CAELUM_KEYWORDS:
        if kw.lower() in text_to_search:
            matched_keywords.append(kw)

    # Score brut : ratio de mots-clés matchés
    raw_score = len(matched_keywords) / len(CAELUM_KEYWORDS)

    # Bonus si mots-clés stratégiques présents
    strategic_keywords = ["CSDDD", "due diligence", "droits humains", "compliance", "ESG"]
    strategic_hits = sum(
        1 for sk in strategic_keywords if sk.lower() in text_to_search
    )
    strategic_bonus = strategic_hits * 5  # +5 par mot-clé stratégique

    # Score final 0-100
    score = min(100, int(raw_score * 70 + strategic_bonus))

    raisons = []
    if matched_keywords:
        raisons.append(f"Mots-clés matchés ({len(matched_keywords)}): {', '.join(matched_keywords[:6])}")
    if strategic_hits > 0:
        raisons.append(f"Mots-clés stratégiques ({strategic_hits}): alignement fort CSDDD/compliance")
    if "Bruxelles" in call.get("region", ""):
        raisons.append("Localisation Bruxelles : avantage géographique direct")
    if call.get("type") == "subvention":
        raisons.append("Type subvention : financement non-dilutif privilégié")

    return score, raisons


# ─────────────────────────────────────────────
# Filtrage et tri des appels
# ─────────────────────────────────────────────
def analyze_calls(calls: list[dict]) -> list[dict]:
    """Analyse et enrichit chaque appel avec score de pertinence."""
    results = []
    for call in calls:
        score, raisons = compute_relevance_score(call)
        # Calcul jours restants
        deadline_dt = datetime.strptime(call["deadline"], "%Y-%m-%d")
        days_left = (deadline_dt - datetime.now()).days
        urgency = "URGENT" if days_left < 30 else ("Moyen terme" if days_left < 60 else "Long terme")

        enriched = {
            "nom": call["nom"],
            "organisme": call["organisme"],
            "type": call["type"],
            "montant_max": call["montant_max"],
            "montant_min": call["montant_min"],
            "montant_max_formatte": f"{call['montant_max']:,}€".replace(",", "."),
            "deadline": call["deadline"],
            "jours_restants": days_left,
            "urgence": urgency,
            "url": call["url"],
            "description": call["description"],
            "region": call["region"],
            "secteurs_eligibles": call["secteurs_eligibles"],
            "score_pertinence": score,
            "raisons_matching": raisons,
        }
        results.append(enriched)

    # Tri par score décroissant, puis par deadline
    results.sort(key=lambda x: (-x["score_pertinence"], x["jours_restants"]))
    return results


# ─────────────────────────────────────────────
# Rapport console
# ─────────────────────────────────────────────
def print_report(calls: list[dict]):
    print("\n" + "=" * 70)
    print("  CAELUM PARTNERS — APPELS A PROJETS BELGES & EUROPEENS 2026")
    print("  Belgium Project Calls Agent")
    print("=" * 70)
    print(f"  Date d'analyse : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Sources surveillees : {len(SOURCES)}")
    print(f"  Appels identifies  : {len(calls)}")
    print(f"  Montant total potentiel : {sum(c['montant_max'] for c in calls):,}€".replace(",", "."))
    print("=" * 70)

    urgent = [c for c in calls if c["urgence"] == "URGENT"]
    if urgent:
        print(f"\n  *** {len(urgent)} APPEL(S) URGENT(S) — deadline < 30 jours ***")
        for u in urgent:
            print(f"      - {u['nom'][:50]}... ({u['jours_restants']}j restants)")

    print("\n  --- CLASSEMENT PAR PERTINENCE ---\n")
    for i, call in enumerate(calls, 1):
        print(f"  [{i}] {call['nom']}")
        print(f"      Organisme : {call['organisme']}")
        print(f"      Montant   : jusqu'a {call['montant_max_formatte']}")
        print(f"      Deadline  : {call['deadline']} ({call['jours_restants']} jours) — {call['urgence']}")
        print(f"      Score     : {call['score_pertinence']}/100")
        print(f"      URL       : {call['url']}")
        if call["raisons_matching"]:
            print(f"      Matching  : {call['raisons_matching'][0]}")
        print()

    print("=" * 70)
    high_score = [c for c in calls if c["score_pertinence"] >= 70]
    print(f"\n  RECOMMANDATION : {len(high_score)} appel(s) avec score >= 70/100")
    print("  Priorite 1 : EIC Accelerator + FEDER Brussels Invest")
    print("  Priorite 2 : Innoviris Bridge + Plan de Relance")
    print("=" * 70 + "\n")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    print("[Belgium Project Calls Agent] Analyse des appels a projets en cours...")

    raw_calls = get_simulated_calls()
    analyzed = analyze_calls(raw_calls)

    print_report(analyzed)

    output = {
        "agent": "belgium-project-calls-agent",
        "version": "1.0.0",
        "date_analyse": datetime.now().isoformat(),
        "profil_societe": {
            "nom": "Caelum Partners SPRL",
            "secteur": "Tech / Compliance / ESG / CSDDD",
            "localisation": "Bruxelles, Belgique",
        },
        "sources_surveillees": SOURCES,
        "mots_cles_matching": CAELUM_KEYWORDS,
        "statistiques": {
            "total_appels": len(analyzed),
            "score_moyen": round(sum(c["score_pertinence"] for c in analyzed) / len(analyzed), 1),
            "appels_urgents": len([c for c in analyzed if c["urgence"] == "URGENT"]),
            "montant_total_potentiel": sum(c["montant_max"] for c in analyzed),
            "appels_haute_pertinence": len([c for c in analyzed if c["score_pertinence"] >= 70]),
        },
        "appels": analyzed,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return output


if __name__ == "__main__":
    main()
