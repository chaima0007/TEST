#!/usr/bin/env python3
"""
Eligibility Checker Agent — Caelum Partners SPRL
Vérifie l'éligibilité de Caelum Partners aux financements belges et européens.
Produit un rapport d'éligibilité détaillé par opportunité.
"""

import json
from datetime import datetime


# ─────────────────────────────────────────────
# Profil officiel Caelum Partners SPRL
# ─────────────────────────────────────────────
CAELUM_PROFILE = {
    "nom": "Caelum Partners SPRL",
    "forme_juridique": "SPRL (Société Privée à Responsabilité Limitée)",
    "pays": "Belgique",
    "region": "Bruxelles-Capitale",
    "date_creation": "2024-09-01",
    "age_annees": 1.8,
    "secteur_principal": "Tech / SaaS",
    "sous_secteurs": ["Compliance", "ESG", "CSDDD", "LegalTech", "RegTech", "IA"],
    "taille": "micro-entreprise",
    "categorie_eu": "PME (micro)",
    "effectif_fte": 3,
    "effectif_max_prevu_2ans": 12,
    "chiffre_affaires_annuel_eur": 85000,
    "chiffre_affaires_annuel_prevu_eur": 380000,
    "total_bilan_eur": 120000,
    "capital_social_eur": 18500,
    "bpi_eligible": True,
    "tva_assujetti": True,
    "numero_tva": "BE 1234.567.890",
    "objet_social": (
        "Développement et commercialisation d'une plateforme IA multi-agents "
        "pour la conformité CSDDD EU 2024/1760, le reporting ESG et la due diligence "
        "en droits humains dans les chaînes d'approvisionnement. "
        "Clients cibles : grands groupes et ETI belges et européens (B2B SaaS)."
    ),
    "technologie": ["Next.js", "Python", "IA multi-agents", "CaelumSwarm"],
    "marche_cible": "B2B grands groupes et ETI (Europe)",
    "brevets_ip": False,
    "partenariats_univ": False,
    "certifications": [],
    "financements_anterieurs": [],
    "localisation_precise": "Bruxelles, Belgique (UE)",
}

# ─────────────────────────────────────────────
# Critères d'éligibilité par programme
# ─────────────────────────────────────────────
FUNDING_CRITERIA = [
    {
        "id": "innoviris_bridge",
        "nom": "Innoviris Bridge — Projets de transition numérique ESG",
        "organisme": "Innoviris",
        "montant_max": 250000,
        "criteres": {
            "forme_juridique": ["SPRL", "SA", "SRL", "ASBL", "SCRL"],
            "region_requise": ["Bruxelles-Capitale"],
            "age_max_annees": 7,
            "effectif_max": 250,
            "ca_max_eur": 50_000_000,
            "secteurs_eligibles": [
                "Tech", "Numérique", "ESG", "SaaS", "IA", "Compliance",
            ],
            "consortium_requis": False,
            "innovation_requise": True,
            "partenariat_univ_requis": False,
        },
        "points_forts_programme": [
            "Focalisé sur le numérique et l'ESG",
            "Accessible aux très jeunes entreprises",
            "Montant adapté au stade early-stage",
            "Pas de consortium requis",
        ],
    },
    {
        "id": "eic_accelerator",
        "nom": "EIC Accelerator 2026 — Tech for Social Impact",
        "organisme": "EIC Accelerator",
        "montant_max": 2_500_000,
        "criteres": {
            "forme_juridique": ["any_commercial"],
            "region_requise": ["UE"],
            "age_max_annees": 10,
            "effectif_max": 499,
            "ca_max_eur": 100_000_000,
            "secteurs_eligibles": [
                "IA", "LegalTech", "RegTech", "ESG", "Supply Chain", "DeepTech",
            ],
            "consortium_requis": False,
            "innovation_requise": True,
            "partenariat_univ_requis": False,
            "trl_min": 5,
            "pitch_en_anglais": True,
        },
        "points_forts_programme": [
            "Financement le plus élevé d'Europe pour startups",
            "Composante equity acceptée",
            "Réseau EU très valorisé",
            "Priorité explicite sur CSDDD et supply chain 2026",
        ],
    },
    {
        "id": "horizon_europe_cluster6",
        "nom": "Horizon Europe — Cluster 6 Droits humains & supply chain",
        "organisme": "Horizon Europe",
        "montant_max": 3_000_000,
        "criteres": {
            "forme_juridique": ["any"],
            "region_requise": ["UE"],
            "age_max_annees": None,  # pas de limite
            "effectif_max": None,
            "ca_max_eur": None,
            "secteurs_eligibles": ["Recherche", "Tech", "ESG", "Compliance"],
            "consortium_requis": True,
            "nb_partenaires_min": 3,
            "partenaires_pays_differents": True,
            "innovation_requise": True,
            "partenariat_univ_requis": True,
        },
        "points_forts_programme": [
            "Très haut financement possible",
            "Reconnaissance scientifique internationale",
            "Alignement thématique CSDDD/droits humains parfait",
        ],
    },
    {
        "id": "plan_relance_numerique",
        "nom": "Plan de Relance Belge — Axe Numérique PME",
        "organisme": "Plan de relance belge",
        "montant_max": 500_000,
        "criteres": {
            "forme_juridique": ["SPRL", "SA", "SRL", "SNC", "SCRL"],
            "region_requise": ["Belgique"],
            "age_max_annees": 10,
            "effectif_max": 249,
            "ca_max_eur": 50_000_000,
            "secteurs_eligibles": ["Numérique", "SaaS", "IA", "Compliance"],
            "consortium_requis": False,
            "innovation_requise": True,
            "partenariat_univ_requis": False,
        },
        "points_forts_programme": [
            "Ouvert à toutes les régions belges",
            "Critères PME larges",
            "Focalisé sur le numérique B2B",
            "Délai de traitement rapide",
        ],
    },
    {
        "id": "feder_brussels",
        "nom": "FEDER Brussels Invest — Innovation Sociale & Tech",
        "organisme": "FEDER/FSE+",
        "montant_max": 800_000,
        "criteres": {
            "forme_juridique": ["any"],
            "region_requise": ["Bruxelles-Capitale"],
            "age_max_annees": None,
            "effectif_max": 500,
            "ca_max_eur": None,
            "secteurs_eligibles": [
                "Tech", "Innovation sociale", "ESG", "Governance",
            ],
            "consortium_requis": False,
            "innovation_requise": True,
            "partenariat_univ_requis": False,
            "impact_social_requis": True,
        },
        "points_forts_programme": [
            "Co-financement EU robuste",
            "Impact social explicitement valorisé",
            "Ouvert aux entreprises bruxelloises sans plafond de CA",
        ],
    },
    {
        "id": "bei_investeu",
        "nom": "BEI InvestEU — RegTech & Compliance Tech",
        "organisme": "BEI",
        "montant_max": 5_000_000,
        "criteres": {
            "forme_juridique": ["any_commercial"],
            "region_requise": ["UE"],
            "age_max_annees": None,
            "effectif_max": None,
            "ca_max_eur": None,
            "secteurs_eligibles": ["RegTech", "LegalTech", "Compliance", "FinTech"],
            "consortium_requis": False,
            "ca_min_eur": 500_000,  # seuil minimum souvent attendu
            "rentabilite_proche_requise": True,
            "garanties_requises": True,
        },
        "points_forts_programme": [
            "Montant très élevé possible",
            "Prêt non-dilutif",
            "Accès réseau BEI / European Investment Fund",
        ],
    },
]


# ─────────────────────────────────────────────
# Moteur de vérification d'éligibilité
# ─────────────────────────────────────────────
def check_eligibility(profile: dict, funding: dict) -> dict:
    """
    Vérifie l'éligibilité de Caelum Partners pour un financement donné.
    Retourne : score, blockers, avantages, recommandation.
    """
    criteres = funding["criteres"]
    blockers = []
    avantages = []
    points = 0
    max_points = 0

    # 1. Forme juridique
    max_points += 15
    formes = criteres.get("forme_juridique", [])
    if "any" in formes or "any_commercial" in formes:
        points += 15
        avantages.append("Forme juridique SPRL acceptée universellement")
    elif profile["forme_juridique"].split(" ")[0] in formes:
        points += 15
        avantages.append(f"Forme juridique {profile['forme_juridique']} compatible")
    else:
        blockers.append(
            f"Forme juridique {profile['forme_juridique']} possiblement non-listée"
        )
        points += 8  # Partial — SPRL est reconnue dans la plupart des cadres

    # 2. Région / localisation
    max_points += 20
    regions = criteres.get("region_requise", [])
    if "UE" in regions or "Belgique" in regions:
        points += 20
        avantages.append(f"Localisation Bruxelles (Belgique/UE) : pleinement éligible")
    elif "Bruxelles-Capitale" in regions and profile["region"] == "Bruxelles-Capitale":
        points += 20
        avantages.append("Localisation Bruxelles-Capitale : avantage géographique direct")
    else:
        blockers.append("Localisation ne correspond pas aux régions éligibles")

    # 3. Age de la société
    max_points += 15
    age_max = criteres.get("age_max_annees")
    if age_max is None:
        points += 15
        avantages.append("Pas de limite d'âge pour ce programme")
    elif profile["age_annees"] <= age_max:
        points += 15
        avantages.append(
            f"Age société ({profile['age_annees']}a) dans la limite ({age_max}a)"
        )
    else:
        blockers.append(
            f"Age société ({profile['age_annees']}a) dépasse la limite ({age_max}a)"
        )

    # 4. Effectif
    max_points += 10
    effectif_max = criteres.get("effectif_max")
    if effectif_max is None:
        points += 10
        avantages.append("Pas de plafond d'effectif")
    elif profile["effectif_fte"] <= effectif_max:
        points += 10
        avantages.append(
            f"Effectif ({profile['effectif_fte']} ETP) sous le plafond ({effectif_max})"
        )
    else:
        blockers.append(
            f"Effectif ({profile['effectif_fte']}) dépasse le plafond ({effectif_max})"
        )

    # 5. Chiffre d'affaires
    max_points += 10
    ca_max = criteres.get("ca_max_eur")
    ca_min = criteres.get("ca_min_eur", 0)
    if ca_max is None and ca_min == 0:
        points += 10
        avantages.append("Pas de contrainte de CA")
    elif ca_min > 0 and profile["chiffre_affaires_annuel_eur"] < ca_min:
        blockers.append(
            f"CA ({profile['chiffre_affaires_annuel_eur']:,}€) sous le minimum "
            f"attendu ({ca_min:,}€) — risque de refus".replace(",", ".")
        )
        points += 2
    elif ca_max and profile["chiffre_affaires_annuel_eur"] <= ca_max:
        points += 10
        avantages.append(
            f"CA ({profile['chiffre_affaires_annuel_eur']:,}€) dans les limites".replace(",", ".")
        )

    # 6. Secteur éligible
    max_points += 15
    secteurs = criteres.get("secteurs_eligibles", [])
    matching_sectors = [
        s for s in profile["sous_secteurs"]
        if any(s.lower() in sec.lower() or sec.lower() in s.lower() for sec in secteurs)
    ]
    if matching_sectors:
        points += 15
        avantages.append(
            f"Secteurs matchés : {', '.join(matching_sectors[:4])}"
        )
    else:
        blockers.append("Secteur d'activité peut ne pas correspondre aux critères")
        points += 5

    # 7. Consortium requis
    max_points += 10
    if criteres.get("consortium_requis"):
        nb_min = criteres.get("nb_partenaires_min", 3)
        if profile.get("partenariats_univ") or nb_min <= 1:
            points += 10
            avantages.append("Consortium : partenaires disponibles")
        else:
            blockers.append(
                f"Consortium de {nb_min} partenaires requis — à constituer"
            )
            points += 3
    else:
        points += 10
        avantages.append("Pas de consortium requis : candidature en solitaire possible")

    # 8. Partenariat universitaire
    max_points += 5
    if criteres.get("partenariat_univ_requis"):
        if profile.get("partenariats_univ"):
            points += 5
            avantages.append("Partenariat universitaire existant")
        else:
            blockers.append("Partenariat universitaire requis — à développer (ULB/VUB)")
    else:
        points += 5

    # Score final
    score = min(100, int((points / max_points) * 100)) if max_points > 0 else 0

    # Recommandation
    if blockers and any(
        "consortium" in b.lower() or "partenariat" in b.lower() for b in blockers
    ) and score >= 55:
        recommandation = "attendre"
        detail_recommandation = (
            "Score élevé mais blockers structurels à lever (consortium/partenariats). "
            "Travailler sur ces points avant de candidater."
        )
    elif score >= 70:
        recommandation = "candidater"
        detail_recommandation = (
            "Profil très compatible. Préparer le dossier en priorité."
        )
    elif score >= 45:
        recommandation = "attendre"
        detail_recommandation = (
            "Éligibilité partielle. Certains blockers peuvent être levés à court terme."
        )
    else:
        recommandation = "non-eligible"
        detail_recommandation = (
            "Trop de critères non remplis. À re-évaluer après croissance de la société."
        )

    return {
        "id_financement": funding["id"],
        "nom_financement": funding["nom"],
        "organisme": funding["organisme"],
        "montant_max": funding["montant_max"],
        "score_eligibilite": score,
        "recommandation": recommandation,
        "detail_recommandation": detail_recommandation,
        "blockers": blockers,
        "avantages": avantages,
        "points_forts_programme": funding.get("points_forts_programme", []),
    }


# ─────────────────────────────────────────────
# Rapport console
# ─────────────────────────────────────────────
def print_eligibility_report(results: list[dict]):
    print("\n" + "=" * 70)
    print("  CAELUM PARTNERS — RAPPORT D'ELIGIBILITE AUX FINANCEMENTS")
    print("  Eligibility Checker Agent")
    print("=" * 70)
    print(f"  Profil analysé : {CAELUM_PROFILE['nom']}")
    print(f"  Date analyse   : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Programmes vérifiés : {len(results)}")
    print("=" * 70)

    by_rec = {"candidater": [], "attendre": [], "non-eligible": []}
    for r in results:
        by_rec[r["recommandation"]].append(r)

    print(f"\n  CANDIDATER MAINTENANT ({len(by_rec['candidater'])} programme(s)) :")
    for r in sorted(by_rec["candidater"], key=lambda x: -x["score_eligibilite"]):
        print(f"\n    [{r['score_eligibilite']}/100] {r['nom_financement']}")
        print(f"    Organisme : {r['organisme']} | Montant max : {r['montant_max']:,}€".replace(",", "."))
        print(f"    {r['detail_recommandation']}")
        if r["avantages"]:
            print(f"    Avantages  : {r['avantages'][0]}")

    print(f"\n  ATTENDRE / PRÉPARER ({len(by_rec['attendre'])} programme(s)) :")
    for r in sorted(by_rec["attendre"], key=lambda x: -x["score_eligibilite"]):
        print(f"\n    [{r['score_eligibilite']}/100] {r['nom_financement']}")
        print(f"    {r['detail_recommandation']}")
        if r["blockers"]:
            print(f"    Blocker principal : {r['blockers'][0]}")

    if by_rec["non-eligible"]:
        print(f"\n  NON-ELIGIBLE ({len(by_rec['non-eligible'])} programme(s)) :")
        for r in by_rec["non-eligible"]:
            print(f"    - {r['nom_financement']}")

    print("\n" + "=" * 70)
    scores = [r["score_eligibilite"] for r in results]
    print(f"  Score moyen d'éligibilité : {sum(scores) / len(scores):.1f}/100")
    print(
        f"  Montant total accessible  : "
        f"{sum(r['montant_max'] for r in by_rec['candidater']):,}€".replace(",", ".")
    )
    print("=" * 70 + "\n")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    print("[Eligibility Checker Agent] Analyse du profil Caelum Partners...")

    results = []
    for funding in FUNDING_CRITERIA:
        result = check_eligibility(CAELUM_PROFILE, funding)
        results.append(result)

    # Tri par score décroissant
    results.sort(key=lambda x: -x["score_eligibilite"])

    print_eligibility_report(results)

    output = {
        "agent": "eligibility-checker-agent",
        "version": "1.0.0",
        "date_analyse": datetime.now().isoformat(),
        "profil_societe": CAELUM_PROFILE,
        "statistiques": {
            "total_programmes": len(results),
            "score_moyen": round(
                sum(r["score_eligibilite"] for r in results) / len(results), 1
            ),
            "candidater": len([r for r in results if r["recommandation"] == "candidater"]),
            "attendre": len([r for r in results if r["recommandation"] == "attendre"]),
            "non_eligible": len(
                [r for r in results if r["recommandation"] == "non-eligible"]
            ),
            "montant_total_accessible": sum(
                r["montant_max"]
                for r in results
                if r["recommandation"] == "candidater"
            ),
        },
        "rapport_eligibilite": results,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return output


if __name__ == "__main__":
    main()
