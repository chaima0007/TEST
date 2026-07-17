#!/usr/bin/env python3
"""
Market Competitors Analyzer Agent — Caelum Partners SPRL
Analyse comparative des concurrents sur le marché compliance CSDDD/ESG 2026
"""

import json
from datetime import datetime
from math import ceil

# ── Données simulées ─────────────────────────────────────────────────────────

COMPETITORS = [
    {
        "nom": "EcoVadis",
        "pays": "France",
        "fondee": 2007,
        "prix_moyen_mensuel_eur": 1_650,
        "nb_clients": 100_000,
        "fonctionnalites": [
            "Scorecard ESG fournisseurs",
            "Benchmarking sectoriel",
            "Certifications achetables",
            "Portail collaboratif acheteur-fournisseur",
            "Reporting CO₂ Scope 1-2",
        ],
        "forces": [
            "Marque très reconnue dans les grands groupes",
            "Base de données fournisseurs massive (100 k+)",
            "Intégrations SAP / Coupa",
            "Standard de facto pour les audits achats",
        ],
        "faiblesses": [
            "Questionnaires génériques, peu adaptatifs",
            "Aucune couverture spécifique CSDDD / CS3D",
            "IA limitée à du scoring statique",
            "Prix élevé pour les PME",
            "Pas de module droits humains granulaire",
        ],
        "score_menace_caelum": 82,
    },
    {
        "nom": "Sedex",
        "pays": "Royaume-Uni",
        "fondee": 2004,
        "prix_moyen_mensuel_eur": 420,
        "nb_clients": 75_000,
        "fonctionnalites": [
            "SMETA audit social (4 piliers)",
            "Partage de données supply chain",
            "Cartographie risques fournisseurs",
            "Formation e-learning éthique",
        ],
        "forces": [
            "Réseau supply chain mondial dense",
            "Coût d'entrée accessible",
            "Audit SMETA reconnu par les retailers",
            "Forte présence Asie-Pacifique",
        ],
        "faiblesses": [
            "Technologie vieillissante (UX années 2010)",
            "Pas de IA ni d'agents autonomes",
            "Faible couverture réglementation EU (CSDDD, CSRD)",
            "Peu adapté aux obligations légales belges/françaises",
            "Données peu actualisées en temps réel",
        ],
        "score_menace_caelum": 48,
    },
    {
        "nom": "Sourcemap",
        "pays": "États-Unis",
        "fondee": 2009,
        "prix_moyen_mensuel_eur": 2_100,
        "nb_clients": 3_200,
        "fonctionnalites": [
            "Cartographie chaîne d'approvisionnement multi-niveaux",
            "Traçabilité produit (Tier N)",
            "Visualisation géographique interactive",
            "API open supply chain",
            "Détection de risques géopolitiques",
        ],
        "forces": [
            "Profondeur de cartographie inégalée (Tier 4+)",
            "Visuels cartographiques très impressionnants",
            "Bonne API pour intégrations",
            "Solide pour secteurs mode/alimentation/électronique",
        ],
        "faiblesses": [
            "Pas de scoring droits humains structuré",
            "Très orienté opérations logistiques, faible compliance",
            "Peu adapté au cadre CSDDD européen",
            "Tarif enterprise hors portée des ETI",
            "Support limité en langues EU",
        ],
        "score_menace_caelum": 41,
    },
    {
        "nom": "IntegrityNext",
        "pays": "Allemagne",
        "fondee": 2016,
        "prix_moyen_mensuel_eur": 890,
        "nb_clients": 18_000,
        "fonctionnalites": [
            "Due diligence fournisseurs LkSG / CSDDD",
            "Questionnaires automatisés multi-langues",
            "Gestion des risques ESG fournisseurs",
            "Rapports réglementaires automatisés",
            "Portail fournisseur self-service",
        ],
        "forces": [
            "Aligné LkSG (loi allemande devoir de vigilance)",
            "Multi-langues EU natif",
            "Bonne adoption en DACH",
            "Questionnaires adaptatifs par secteur",
        ],
        "faiblesses": [
            "IA basique (moteur de règles, pas d'agents autonomes)",
            "Couverture droits humains thématique insuffisante",
            "Moins connu hors espace DACH",
            "Reporting CSRD partiel",
            "Scalabilité limitée pour très grands groupes",
        ],
        "score_menace_caelum": 67,
    },
    {
        "nom": "Sustainalytics (Morningstar)",
        "pays": "Pays-Bas / USA",
        "fondee": 1992,
        "prix_moyen_mensuel_eur": 4_800,
        "nb_clients": 13_000,
        "fonctionnalites": [
            "ESG Risk Ratings (entreprises cotées)",
            "Controversies Research",
            "Corporate Governance",
            "Impact Screening (ODD)",
            "Fixed Income ESG",
        ],
        "forces": [
            "Référence absolue pour les investisseurs institutionnels",
            "Couverture de 40 000+ entreprises cotées",
            "Intégration Bloomberg / FactSet",
            "Marque Morningstar = confiance maximale",
        ],
        "faiblesses": [
            "Ciblé exclusivement finance/investissement",
            "Inutilisable pour compliance opérationnelle CSDDD",
            "Pas de module supply chain",
            "Prix prohibitif pour non-institutionnels",
            "Aucune IA multi-agents",
        ],
        "score_menace_caelum": 28,
    },
    {
        "nom": "Datamaran",
        "pays": "Royaume-Uni",
        "fondee": 2014,
        "prix_moyen_mensuel_eur": 3_200,
        "nb_clients": 1_800,
        "fonctionnalites": [
            "Veille réglementaire automatisée mondiale",
            "Matérialité ESG dynamique",
            "Analyse NLP des rapports publics",
            "Benchmarking réglementaire cross-pays",
            "Intégration données non-financières",
        ],
        "forces": [
            "Veille réglementaire en temps réel très puissante",
            "NLP avancé sur textes réglementaires",
            "Idéal pour les équipes affaires publiques / legal",
            "Couvre 50+ pays",
        ],
        "faiblesses": [
            "Pas d'IA générative / agents autonomes",
            "Peu opérationnel pour la due diligence terrain",
            "Faible couverture supply chain",
            "Onboarding complexe (courbe d'apprentissage élevée)",
            "Pas de module droits humains spécifique",
        ],
        "score_menace_caelum": 55,
    },
]

CAELUM_ADVANTAGES = {
    "ia_multi_agents": {
        "titre": "IA Multi-Agents (CaelumSwarm)",
        "description": (
            "Architecture swarm avec 42+ engines spécialisés couvrant "
            "chaque domaine droits humains/ESG de façon granulaire. "
            "Aucun concurrent ne propose une IA aussi profonde et spécialisée."
        ),
        "score_differenciation": 9.5,
    },
    "droits_humains_specifique": {
        "titre": "Couverture droits humains ultra-spécifique",
        "description": (
            "50+ domaines couverts : travail des enfants, esclavage moderne, "
            "genre, peuples autochtones, défenseurs des droits, etc. "
            "Profondeur thématique inégalée sur le marché EU."
        ),
        "score_differenciation": 9.8,
    },
    "csddd_native": {
        "titre": "CSDDD-native dès la conception",
        "description": (
            "Seule plateforme conçue nativement pour la CS3D/CSDDD EU 2024. "
            "Mapping complet des obligations légales belges, françaises, "
            "luxembourgeoises. Rapport auto-généré CSRD inclus."
        ),
        "score_differenciation": 9.2,
    },
    "prix_saas_accessible": {
        "titre": "Pricing SaaS accessible (ETI / grands groupes)",
        "description": (
            "Modèle freemium → PME → Enterprise. "
            "Accès PME dès 199 EUR/mois vs 890-4 800 EUR chez les concurrents. "
            "ROI démontrable en < 3 mois grâce à l'automatisation."
        ),
        "score_differenciation": 8.7,
    },
    "temps_reel": {
        "titre": "Monitoring en temps réel (revalidate: 30s)",
        "description": (
            "Alertes live sur les risques émergents. "
            "API ultra-rapide (<200ms) vs interfaces batch hebdomadaires "
            "des concurrents traditionnels."
        ),
        "score_differenciation": 8.4,
    },
}

# ── Logique d'analyse ─────────────────────────────────────────────────────────

def compute_threat_level(score: int) -> str:
    if score >= 70:
        return "ÉLEVÉE"
    elif score >= 45:
        return "MODÉRÉE"
    else:
        return "FAIBLE"


def render_bar(value: int, max_val: int = 100, width: int = 30) -> str:
    filled = round(value / max_val * width)
    return "[" + "█" * filled + "░" * (width - filled) + f"] {value}/100"


def analyze_competitors(competitors: list) -> dict:
    sorted_by_threat = sorted(
        competitors, key=lambda c: c["score_menace_caelum"], reverse=True
    )
    avg_price = sum(c["prix_moyen_mensuel_eur"] for c in competitors) / len(competitors)
    avg_threat = sum(c["score_menace_caelum"] for c in competitors) / len(competitors)
    return {
        "total_concurrents": len(competitors),
        "prix_moyen_marche_eur": round(avg_price, 2),
        "score_menace_moyen": round(avg_threat, 1),
        "concurrents_par_menace": sorted_by_threat,
        "concurrent_principal": sorted_by_threat[0]["nom"],
        "concurrent_moins_dangereux": sorted_by_threat[-1]["nom"],
    }


def run_agent():
    print("=" * 68)
    print("  CAELUM PARTNERS — MARKET COMPETITORS ANALYZER AGENT")
    print(f"  Analyse au : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 68)

    analysis = analyze_competitors(COMPETITORS)

    print(f"\n{'─'*68}")
    print(f"  PANORAMA CONCURRENTIEL — {analysis['total_concurrents']} acteurs analysés")
    print(f"{'─'*68}")
    print(f"  Prix moyen du marché   : {analysis['prix_moyen_marche_eur']:,.0f} EUR/mois")
    print(f"  Score menace moyen     : {analysis['score_menace_moyen']}/100")
    print(f"  Concurrent principal   : {analysis['concurrent_principal']}")
    print()

    print(f"{'─'*68}")
    print("  DÉTAIL PAR CONCURRENT (trié par menace décroissante)")
    print(f"{'─'*68}")

    for c in analysis["concurrents_par_menace"]:
        threat = compute_threat_level(c["score_menace_caelum"])
        age = 2026 - c["fondee"]
        print(f"\n  ► {c['nom']} ({c['pays']}) — fondée {c['fondee']} ({age} ans)")
        print(f"    Prix mensuel moyen : {c['prix_moyen_mensuel_eur']:,} EUR")
        print(f"    Clients            : {c['nb_clients']:,}")
        print(f"    Menace Caelum      : {render_bar(c['score_menace_caelum'])} [{threat}]")
        print(f"    Forces clés        : {' · '.join(c['forces'][:2])}")
        print(f"    Faiblesses clés    : {' · '.join(c['faiblesses'][:2])}")

    print(f"\n{'─'*68}")
    print("  AVANTAGES COMPÉTITIFS DE CAELUMSWARM")
    print(f"{'─'*68}")

    for key, adv in CAELUM_ADVANTAGES.items():
        score_pct = int(adv["score_differenciation"] / 10 * 100)
        print(f"\n  ✦ {adv['titre']}")
        print(f"    Différenciation : {render_bar(score_pct)}")
        # Wrap description at ~60 chars
        desc = adv["description"]
        words = desc.split()
        line = "    "
        for w in words:
            if len(line) + len(w) + 1 > 66:
                print(line)
                line = "    " + w + " "
            else:
                line += w + " "
        if line.strip():
            print(line)

    print(f"\n{'─'*68}")
    print("  CONCLUSION STRATÉGIQUE")
    print(f"{'─'*68}")
    print(f"  EcoVadis est le concurrent le plus dangereux (score 82/100),")
    print(f"  mais reste vulnérable sur l'axe CSDDD-native et IA multi-agents.")
    print(f"  CaelumSwarm possède un avantage structurel sur tous les acteurs")
    print(f"  grâce à sa conception droits humains + CSDDD from scratch.")
    print(f"{'─'*68}\n")

    # ── JSON output ──────────────────────────────────────────────────────────
    output = {
        "agent": "market-competitors-analyzer-agent",
        "generated_at": datetime.now().isoformat(),
        "analyse": analysis,
        "concurrents": COMPETITORS,
        "avantages_caelum": CAELUM_ADVANTAGES,
        "conclusion": {
            "concurrent_le_plus_dangereux": analysis["concurrent_principal"],
            "avantage_differenciant_principal": "IA multi-agents droits humains CSDDD-native",
            "recommandation": (
                "Positionner CaelumSwarm comme la seule plateforme "
                "CSDDD-native avec IA multi-agents dédiée aux droits humains. "
                "Attaquer EcoVadis sur la profondeur thématique et le prix ETI."
            ),
        },
    }

    output_path = "/home/user/TEST/scripts/market-competitors-analyzer-agent-output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  JSON sauvegardé → {output_path}")
    print()
    return output


if __name__ == "__main__":
    run_agent()
